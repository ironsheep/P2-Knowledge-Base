#!/usr/bin/env python3
"""Generate a single PASM2 disassembly reference from the per-instruction YAMLs.
Source of truth: deliverables/ai/P2/language/pasm2/*.yaml
Output: a grouped markdown table with each instruction's 32-bit encoding pattern.
"""
import glob, os, sys, yaml, re

SRC = "/workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2"
CONDSRC = os.path.join(SRC, "concepts", "conditional_execution.yaml")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/pasm2-ref.md"

# Load the authoritative EEEE condition-code table from the KB.
cond_rows = []
try:
    with open(CONDSRC) as f:
        cdata = yaml.safe_load(f)
    for c in (cdata.get("condition_codes") or []):
        val = str(c.get("value", "")).replace("%", "")
        primary = c.get("primary") or (c.get("aliases") or [""])[0]
        aliases = ", ".join(a for a in (c.get("aliases") or []) if a != primary)
        cond_rows.append((val, primary, c.get("condition", ""), aliases))
except Exception as e:
    cond_rows = []

recs = []
missing_encoding = []
skipped = []

for path in sorted(glob.glob(os.path.join(SRC, "*.yaml"))):
    fn = os.path.basename(path)
    try:
        with open(path) as f:
            d = yaml.safe_load(f)
    except Exception as e:
        skipped.append((fn, f"parse error: {e}"))
        continue
    if not isinstance(d, dict) or "instruction" not in d:
        skipped.append((fn, "no 'instruction' key"))
        continue

    mnem = str(d.get("instruction", "")).strip()
    cat = (d.get("category") or d.get("compiler_category") or "Uncategorized").strip()
    syntax = (d.get("syntax") or "").strip()
    oneliner = (d.get("oneliner") or d.get("brief_description") or "").strip()
    operand = ""
    cof = d.get("compiler_operand_format")
    if isinstance(cof, dict):
        operand = (cof.get("pattern") or cof.get("name") or "").strip()

    # encoding bit patterns (may be multiple forms)
    bits_list = []
    enc = d.get("encoding")
    if isinstance(enc, list):
        for e in enc:
            if isinstance(e, dict) and e.get("bits"):
                bits_list.append(str(e["bits"]).strip())
    elif isinstance(enc, dict) and enc.get("bits"):
        bits_list.append(str(enc["bits"]).strip())
    if not bits_list:
        missing_encoding.append(mnem or fn)

    # flags the instruction can write
    # NOTE: flags_affected is a dict {C: <desc>, Z: <desc>}; a key is present even when
    # the value is "No effect". Test the VALUE, not key presence (see F-047).
    flags = []
    fa = d.get("flags_affected")
    _no_effect = ("no effect", "—", "-", "--", "none", "")
    if isinstance(fa, dict):
        for k in ("C", "Z"):
            v = fa.get(k)
            if v is not None and str(v).strip().lower() not in _no_effect:
                flags.append(k)
    flags_s = ",".join(flags) if flags else "--"

    cycles = ""
    t = d.get("timing")
    if isinstance(t, dict) and t.get("cycles") is not None:
        cycles = str(t["cycles"])
    elif bits_list and isinstance(enc, list) and enc and enc[0].get("clocks"):
        cycles = str(enc[0]["clocks"])

    recs.append(dict(mnem=mnem, cat=cat, syntax=syntax, oneliner=oneliner,
                     operand=operand, bits=bits_list, flags=flags_s, cycles=cycles))

# group by category
groups = {}
for r in recs:
    groups.setdefault(r["cat"], []).append(r)
for g in groups.values():
    g.sort(key=lambda r: r["mnem"])

def esc(s):
    return s.replace("|", "\\|") if s else ""

lines = []
lines.append("# PASM2 Instruction Encoding Reference (for disassembly)\n")
lines.append("**Generated from** `deliverables/ai/P2/language/pasm2/*.yaml` — the per-instruction")
lines.append("knowledge-base YAMLs. Regenerate with `engineering/tools/gen-pasm2-encoding-reference.py`.")
lines.append("One row per instruction;")
lines.append("the **Encoding** column is the authoritative 32-bit bit pattern.\n")
lines.append("## How to read the encoding\n")
lines.append("Each instruction word is 32 bits, written MSB→LSB as space-separated fields:\n")
lines.append("| Field | Bits | Meaning |")
lines.append("|-------|------|---------|")
lines.append("| `EEEE` | 31..28 | Condition code (execute-if); `1111` = always. |")
lines.append("| opcode | 27..21 (typically 7 bits) | Fixed instruction-selector bits — the primary decode key. |")
lines.append("| `C` `Z` `I` (`CZI`) | per instruction | C-effect (WC), Z-effect (WZ), and I = immediate-S select. Some instructions use `L` for immediate-D, or repurpose these bits. |")
lines.append("| `DDDDDDDDD` | 9 bits | Destination register (or 9-bit immediate when `L`=1, or a sub-opcode/field). |")
lines.append("| `SSSSSSSSS` | 9 bits | Source register (or 9-bit immediate when `I`=1, or a sub-opcode/field). |\n")
lines.append("> Literal `0`/`1` digits in a pattern are fixed opcode bits — match these to decode.")
lines.append("> Letter runs (`D`, `S`, `A`, `R`, `N`, `W`, etc.) are operand/field bits. Branch and")
lines.append("> augment instructions replace `D`/`S` with wide immediate fields (e.g. `AAAAAAAAA`")
lines.append("> address bits, 23-bit `AUGS`/`AUGD` literals); the pattern shown is exact per instruction.\n")
if cond_rows:
    lines.append("## Condition codes (`EEEE`, bits 31..28)\n")
    lines.append("The 4-bit `EEEE` prefix selects conditional execution (sourced from")
    lines.append("`language/pasm2/concepts/conditional_execution.yaml`):\n")
    lines.append("| EEEE | Mnemonic | Condition | Aliases |")
    lines.append("|------|----------|-----------|---------|")
    for val, primary, cond, aliases in cond_rows:
        lines.append(f"| `{val}` | {esc(primary)} | {esc(cond)} | {esc(aliases)} |")
    lines.append("")
    lines.append("> `%0000` is exclusively the `_RET_` prefix (always-execute + return); it is NOT")
    lines.append("> the encoding for `IF_NEVER`. `IF_NEVER` assembles to EEEE=`%1111` (always),")
    lines.append("> identical to the bare no-prefix form, regardless of whether `WC`/`WZ` are written")
    lines.append("> (pnut-ts boundary-probed). `%1111` is the default (always), printed with no `IF_` prefix.\n")
lines.append("---\n")
lines.append(f"**Coverage:** {len(recs)} instructions, {len(recs)-len(missing_encoding)} with an encoding pattern"
             f"{'' if not missing_encoding else f', {len(missing_encoding)} WITHOUT (listed at end)'}.\n")
lines.append("---\n")

for cat in sorted(groups):
    rows = groups[cat]
    lines.append(f"## {cat}  ({len(rows)})\n")
    lines.append("| Mnemonic | Encoding | Operands | Flags | Cyc | Summary |")
    lines.append("|----------|----------|----------|-------|-----|---------|")
    for r in rows:
        enc = "<br>".join(f"`{b}`" for b in r["bits"]) if r["bits"] else "**(missing)**"
        lines.append(f"| **{esc(r['mnem'])}** | {enc} | {esc(r['operand'])} | {r['flags']} | {esc(r['cycles'])} | {esc(r['oneliner'])} |")
    lines.append("")

if missing_encoding:
    lines.append("---\n")
    lines.append("## Instructions missing an encoding pattern in the YAMLs\n")
    lines.append("These need their `encoding.bits` cross-filled (the v35 CSV spreadsheet has them):\n")
    lines.append(", ".join(f"`{m}`" for m in sorted(missing_encoding)))
    lines.append("")

with open(OUT, "w") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUT}")
print(f"instructions: {len(recs)}")
print(f"with encoding: {len(recs)-len(missing_encoding)}")
print(f"MISSING encoding: {len(missing_encoding)} -> {sorted(missing_encoding)[:40]}")
print(f"categories: {sorted(groups)}")
print(f"skipped non-instruction files ({len(skipped)}): {[s[0] for s in skipped][:20]}")
