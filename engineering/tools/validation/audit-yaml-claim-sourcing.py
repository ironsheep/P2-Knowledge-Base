#!/usr/bin/env python3
"""
audit-yaml-claim-sourcing.py - a quantitative claim in the shipped KB must say
where it came from.

WHY THIS EXISTS
    `audit-constant-fidelity.py` compares the KB's description of a NAMED
    CONSTANT against the source's. Within an hour of it shipping, F-327 was
    found -- and that tool was structurally blind to it, because the defect
    named no constants at all:

        drive_strength_configurations:
          current_modes:
            - mode: "1.5mA"
              impedance: "~2000Ohm"
            ...
        slew_rate_control:
          fast_slew:
            rise_fall: "< 2ns with strong drive"

    None of that exists. The P2 has no 1.5mA/3.0mA/15mA/75mA/150mA drive ladder,
    no impedance table, and no programmable slew rate -- the string "slew"
    appears ZERO times across the Silicon Doc, the Spin2 sources, and the
    smart-pins catalog. It is not a mislabel of a real mechanism; it is a
    mechanism that does not exist, stated in six numbers and a feature name.

    This is the "information that should no longer be in the files" half of the
    release gate, and the fidelity tool cannot see it. Name coverage is not
    semantic coverage, and that cuts both ways.

THE TELL, AND WHY IT IS MECHANICAL
    The file that carried F-327 cites its sources -- three sections up:

        absolute_maximum_ratings:
          source: "Parallax P2 Datasheet (Absolute Maximum Electrical Ratings...)"
        special_timing_modes:
          source: "P2 Silicon Doc v35"

    ...and then states a drive ladder, an impedance table and a whole feature
    with no `source:` field anywhere near them.

    That asymmetry IS the signal, and it needs no judgement about content. A
    file that demonstrably knows the citing convention, and then abandons it for
    a block full of physical quantities, is flagging itself. This tool does
    nothing cleverer than notice that.

    It is deliberately NOT "every claim must be cited" -- that would fire on the
    entire corpus at once, be triaged as noise, and get switched off. It asks
    the narrower question the evidence actually supports.

TWO TIERS
  Tier 1 -- BLOCKS. `UNCITED_IN_CITING_FILE`: the file cites somewhere, and a
      block carrying physical quantities does not. This is the F-327 shape
      exactly, and the file's own other sections are the control.

  Tier 2 -- ADVISORY. `UNCITED_FILE`: the file carries physical quantities and
      cites nothing, anywhere. Could be wholesale fabrication; could equally be
      a file authored before the convention existed. There is no in-file control
      to compare against, so a human decides. Advisory rather than blocking
      because the population is large and mostly historical, and a gate that
      fires on hundreds of legacy files on day one is a gate that gets disabled.

WHAT COUNTS AS A QUANTITY -- and what deliberately does not
    Counted: currents, resistances, voltages, times, frequencies, capacitances,
    data rates -- claims about the physical world that must come from somewhere.

    NOT counted, because they are structure rather than measurement:
      * bare integers and hex -- pin numbers, indices, counts
      * P2 BINARY literals (`%0000_0000_000_...`). In Spin2 `%` is the binary
        prefix, NOT a percent sign. Reading it as a unit would flag every mode
        word in the knowledge base.
      * version numbers, dates, byte/bit widths

EXIT STATUS
    0  no Tier 1 violations
    1  one or more Tier 1 violations
    2  the KB tree was not found -- nothing audited, which is never a pass

USAGE
    audit-yaml-claim-sourcing.py [--inventory] [--advisory] [--negative-control]
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
KB_ROOT = REPO / "deliverables" / "ai" / "P2"

# A citation, in any of the spellings the corpus actually uses.
CITE_RE = re.compile(
    r"^\s*(source|sources|source_document|source_documents|citation|citations|"
    r"reference|references|authority|derived_from|verified_against)\s*:",
    re.IGNORECASE)

# Physical quantities. Unit REQUIRED -- a bare number is structure, not a claim.
QTY_RE = re.compile(
    r"(?<![\w%$])"                       # not inside a %binary or $hex literal
    r"~?\d+(?:\.\d+)?\s*"
    r"(mA|uA|µA|μA|nA|A|kΩ|kOhm|kohm|Ω|Ohm|ohm|mV|uV|µV|V|"
    r"ns|us|µs|μs|ms|MHz|kHz|Hz|dB|pF|nF|uF|µF|Mbps|kbps|bps)"
    r"(?![\w])")

# P2 binary literal -- masked out before scanning so `%0000_0000` never reads
# as a percentage and `%01` never reads as a quantity.
BINARY_RE = re.compile(r"%[01_]+")
HEX_RE = re.compile(r"\$[0-9A-Fa-f_]+")

# A quantity inside an EXAMPLE is a chosen parameter, not a claim about the
# silicon. `WAITX ##25_000_000` and `_clkfreq = 180 MHz` are the author picking
# numbers for a demo; nobody needs to cite their own example. Flagging them
# buried the real findings under example code, so code regions are skipped.
CODE_KEY_RE = re.compile(
    r"^(\s*)-?\s*(code|example|examples|runnable_code|snippet|snippets|usage|"
    r"spin2|pasm2|listing|sample|demo)\s*:\s*[|>]?\s*$", re.IGNORECASE)

# An INLINE attribution is a citation. The question this tool asks is "does this
# claim say where it came from", and `"343.75ns at 160MHz (55 clocks per Silicon
# Doc v35 verbatim)"` answers it perfectly well without a `source:` field.
# Demanding one particular spelling would turn a correctly-attributed claim into
# a violation, which teaches people the gate is wrong rather than that the claim
# was.
INLINE_CITE_RE = re.compile(
    r"(silicon\s*doc|datasheet|data\s*sheet|spin2\s*v\d|p2\s*documentation|"
    r"hardware[- ]verified|empirical|EF-\d+|per\s+the\s+doc|verbatim|"
    r"parallax\s+p2|rev\s*[BC]\b)", re.IGNORECASE)


def top_level_blocks(lines):
    """Split a YAML file into top-level key blocks. Line-based on purpose:
    these files must be auditable even when a block is malformed."""
    blocks, name, start = [], None, 0
    for i, line in enumerate(lines):
        if re.match(r"^[A-Za-z_][\w-]*\s*:", line):
            if name is not None:
                blocks.append((name, start, i))
            name, start = line.split(":", 1)[0].strip(), i
    if name is not None:
        blocks.append((name, start, len(lines)))
    return blocks


def strip_code_regions(lines):
    """Drop block-scalar example bodies. A demo's chosen numbers are not claims."""
    out, skip_indent = [], None
    for line in lines:
        if skip_indent is not None:
            bare = line.strip()
            indent = len(line) - len(line.lstrip())
            if bare and indent <= skip_indent:
                skip_indent = None
            else:
                out.append("")
                continue
        m = CODE_KEY_RE.match(line)
        if m:
            skip_indent = len(m.group(1))
            out.append("")
            continue
        out.append(line)
    return out


def quantities_in(text):
    masked = HEX_RE.sub(" ", BINARY_RE.sub(" ", text))
    return QTY_RE.findall(masked)


def audit():
    if not KB_ROOT.is_dir():
        return None, None, 0
    tier1, tier2, scanned = [], [], 0
    for path in sorted(KB_ROOT.rglob("*.yaml")):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        scanned += 1
        rel = path.relative_to(REPO)
        file_cites = (any(CITE_RE.match(ln) for ln in lines)
                      or bool(INLINE_CITE_RE.search("\n".join(lines))))
        prose = strip_code_regions(lines)

        for name, start, end in top_level_blocks(lines):
            body = "\n".join(prose[start:end])
            qty = quantities_in(body)
            if not qty:
                continue
            block_cites = (any(CITE_RE.match(ln) for ln in lines[start:end])
                           or bool(INLINE_CITE_RE.search(body)))
            if block_cites:
                continue
            units = sorted({u for u in qty})
            detail = (f"{rel}:{start + 1} block `{name}` states "
                      f"{len(qty)} quantit{'y' if len(qty) == 1 else 'ies'} "
                      f"({', '.join(units[:6])}) with no source")
            if file_cites:
                tier1.append((name, f"{detail}; this file DOES cite elsewhere "
                                    f"— its own other sections are the control"))
            else:
                tier2.append((name, f"{detail}; file cites nothing anywhere"))
    return tier1, tier2, scanned


def negative_control():
    """A check that cannot fail has not been verified, it has been run."""
    print("NEGATIVE CONTROL -- proving the tool discriminates\n")
    cases = [
        ("the F-327 shape (mA + ohms, uncited)", 'mode: "1.5mA"\nimpedance: "~2000Ohm"', True),
        ("slew claim (ns, uncited)", 'rise_fall: "< 2ns with strong drive"', True),
        ("P2 binary literal — MUST NOT fire", 'bit_pattern: "%0000_0000_000_0000000101000_00_00000_0"', False),
        ("pin numbers and counts — MUST NOT fire", 'pins: 64\nrange: "0-63"\ncogs: 8', False),
        ("hex constant — MUST NOT fire", 'value: "$0000_2800"', False),
    ]
    ok = True
    for label, text, want in cases:
        fired = bool(quantities_in(text))
        good = fired == want
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: fired={fired} expected={want}")
    print("\n" + ("Negative control PASSED -- quantities detected, P2 syntax not "
                  "mistaken for units." if ok else
                  "Negative control FAILED -- do not trust this run."))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--inventory", action="store_true", help="print coverage first")
    ap.add_argument("--advisory", action="store_true", help="also print Tier 2 in full")
    ap.add_argument("--negative-control", action="store_true",
                    help="prove the tool can fail; audits nothing")
    args = ap.parse_args()

    if args.negative_control:
        return negative_control()

    tier1, tier2, scanned = audit()
    if tier1 is None:
        print(f"ERROR  {KB_ROOT} not found — nothing audited. Not a pass.")
        return 2

    if args.inventory:
        print(f"scanned   {scanned} YAML file(s) under {KB_ROOT.relative_to(REPO)}")
        print(f"Tier 1    {len(tier1)} uncited quantitative block(s) in citing files")
        print(f"Tier 2    {len(tier2)} uncited quantitative block(s) in non-citing files\n")

    if tier1:
        print(f"TIER 1 -- UNCITED IN A CITING FILE ({len(tier1)}) -- these block\n")
        for name, detail in sorted(tier1, key=lambda t: t[1]):
            print(f"  [UNCITED_IN_CITING_FILE] {name}\n        {detail}")
        print()
    else:
        print("TIER 1: none\n")

    if args.advisory and tier2:
        print(f"TIER 2 -- WHOLLY UNCITED FILES ({len(tier2)}) -- advisory\n")
        for name, detail in sorted(tier2, key=lambda t: t[1]):
            print(f"  [UNCITED_FILE] {name}\n        {detail}")
        print()
    elif tier2:
        print(f"TIER 2 -- ADVISORY: {len(tier2)} block(s) in wholly-uncited files "
              f"(run with --advisory to list)\n")

    if tier1:
        print(f"FAIL  {len(tier1)} Tier 1 violation(s) across {scanned} file(s)")
        return 1
    print(f"PASS  no Tier 1 violations across {scanned} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
