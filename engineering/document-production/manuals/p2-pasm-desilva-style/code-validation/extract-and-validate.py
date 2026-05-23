#!/usr/bin/env python3
"""
Extract every PASM2 / Spin2 code block from the manual, compile each with
pnut_ts, and produce a per-block pass/fail report with source file:line
traceability.

Usage:
    python3 extract-and-validate.py [manual_root] [output_dir]

Defaults:
    manual_root = ../opus-master
    output_dir  = extracted
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path

PNUT_TS = shutil.which("pnut_ts") or "/usr/local/bin/pnut_ts"

# Skip backup files and other non-source files (matches .backup, .bak, -backup-)
SKIP_PATTERNS = re.compile(r"(\.(backup|bak)(\.|$)|-backup-)")
# Skip directories whose name suggests archived/legacy content
SKIP_DIRS = {"archived-2025", "archive", "archived", "old", "legacy", "deprecated"}

# Standard fenced opener: ```pasm2 or ```spin2
FENCE_OPEN = re.compile(r"^```(pasm2|spin2)\s*$")
FENCE_CLOSE = re.compile(r"^```\s*$")
# Pandoc fenced-div opener: ::: pasm2 or ::: spin2 (often wraps an untagged ``` block)
DIV_OPEN = re.compile(r"^:::\s+(pasm2|spin2)\s*$")
DIV_CLOSE = re.compile(r"^:::\s*$")


def extract_blocks(md_path: Path):
    """Yield (lang, start_line, end_line, code_text) tuples.

    Recognizes two block styles:
      1. ```pasm2 ... ```                  (standard fenced code block)
      2. ::: pasm2 / ``` / body / ``` / :::  (Pandoc div wrapping an untagged fence)
    """
    with md_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    i, n = 0, len(lines)
    while i < n:
        m = FENCE_OPEN.match(lines[i])
        if m:
            lang = m.group(1)
            start = i + 1
            j = i + 1
            body = []
            while j < n and not FENCE_CLOSE.match(lines[j]):
                body.append(lines[j].rstrip("\n"))
                j += 1
            end = j + 1
            yield lang, start, end, "\n".join(body)
            i = j + 1
            continue
        m = DIV_OPEN.match(lines[i])
        if m:
            lang = m.group(1)
            start = i + 1
            j = i + 1
            while j < n and not lines[j].strip().startswith("```") and not DIV_CLOSE.match(lines[j]):
                j += 1
            if j >= n or DIV_CLOSE.match(lines[j]):
                i = j + 1
                continue
            j += 1
            body = []
            while j < n and not FENCE_CLOSE.match(lines[j]):
                body.append(lines[j].rstrip("\n"))
                j += 1
            k = j + 1
            while k < n and not DIV_CLOSE.match(lines[k]):
                k += 1
            end = (k if k < n else j) + 1
            yield lang, start, end, "\n".join(body)
            i = k + 1
            continue
        i += 1


# Common placeholder/template identifiers in PASM2 examples.
# These get stubbed so syntax-demonstration fragments compile.
PLACEHOLDER_SYMS = {
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "n", "x", "y", "z",
    "src", "source", "dest", "dst", "temp", "tmp", "val", "value", "result",
    "mask", "addr", "address", "ptr", "pointer", "count", "counter", "index",
    "idx", "num", "len", "length", "size", "buf", "buffer", "data", "byte_val",
    "word_val", "long_val", "limit", "angle", "radius", "degrees", "pin",
    "pins", "rgb_mask", "rgb_data", "scl", "sda", "tix", "sclpin", "mybit",
    "myreg", "first", "last", "start", "end", "low", "high", "lo", "hi",
    "bit", "byte_pos", "bits", "operand", "instruction", "label",
} - {"end"}  # 'end' is the END directive keyword

# Code lines that look like template syntax (e.g. INSTR D, S) — keywords
# used as placeholders.
TEMPLATE_KEYWORDS = {"instr", "instruction", "inst"}

# Identifiers that are Spin2 built-in constants — recognized by pnut_ts
# automatically. We never stub these (doing so causes "already defined" errors).
SPIN2_BUILTIN_CONSTS = {
    "POSX", "NEGX", "PI", "TRUE", "FALSE", "COGEXEC", "HUBEXEC",
    "CLKMODE", "CLKFREQ", "_CLKFREQ", "_CLKMODE",
}

# Match identifiers (case-sensitive for stubbing decisions later).
IDENT = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\b")


def looks_complete(code: str, lang: str) -> bool:
    """Heuristic: does this block already declare a top-level structure?"""
    lower = code.lower()
    if lang == "spin2":
        return any(tok in lower for tok in ("pub ", "pri ", "con\n", "dat\n", "obj\n", "var\n"))
    # pasm2
    return any(tok in lower for tok in ("dat\n", "\norg ", "\norg\t", "pub ", "pri ", "con\n", "obj\n", "var\n"))


def looks_hub_mode(code: str) -> bool:
    """Detect fragments that should run in hub mode rather than cog mode.

    Heuristic: bare BYTE/WORD/LONG data declarations (no preceding ORG), or
    ORGH usage, or FILE include — these need hub mode."""
    lower = code.lower()
    if "orgh" in lower:
        return True
    # If first non-comment line is a data label with byte/word/long
    for line in code.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("'") or stripped.startswith("'"):
            continue
        # Skip leading "        " indented instructions — they're code
        if line.startswith(("\t", "    ")) and stripped.split()[0].lower() not in {"byte", "word", "long", "file"}:
            return False
        # First content line — if it starts with a label and has BYTE/WORD/LONG, it's data
        toks = stripped.split()
        if len(toks) >= 2 and toks[1].lower() in {"byte", "word", "long", "file"}:
            return True
        return False
    return False


def collect_undefined_placeholders(code: str):
    """Find placeholder identifiers used in the fragment that aren't likely
    defined elsewhere in it. Returns a list of (name, kind) pairs."""
    defined = set()
    # First pass: collect anything that looks like a label declaration
    for line in code.splitlines():
        if not line:
            continue
        if not line[0].isspace() and not line.startswith("'"):
            # Bare-at-column-0 starts a label or directive
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)", line)
            if m:
                defined.add(m.group(1))
    # Second pass: collect referenced identifiers
    referenced = set()
    for line in code.splitlines():
        # Strip comments
        line_nocomment = re.sub(r"'.*$", "", line)
        for m in IDENT.finditer(line_nocomment):
            referenced.add(m.group(1))
    needed_placeholders = []
    for sym in referenced - defined:
        if sym in SPIN2_BUILTIN_CONSTS:
            continue  # pnut_ts knows these already
        if sym.lower() in PLACEHOLDER_SYMS:
            needed_placeholders.append(sym)
    return needed_placeholders


def make_testable(code: str, lang: str, example_id: str) -> str:
    """Wrap a fragment so it can compile."""
    if looks_complete(code, lang):
        return code
    if lang == "spin2":
        return (
            f"' Generated test wrapper for {example_id}\n"
            f"PUB main()\n"
            + "\n".join("  " + line if line.strip() else line for line in code.splitlines())
            + "\n"
        )
    # pasm2 fragment — figure out mode and stubs
    placeholders = collect_undefined_placeholders(code)
    stub_lines = ""
    if placeholders:
        # Stubs in their own DAT block after the fragment to avoid colliding
        # with the fragment's own ORG. Long-aligned RES 1 declarations.
        stub_lines = "\nDAT\n        ORG     $100\n" + "\n".join(
            f"{p}        RES     1" for p in placeholders
        ) + "\n"
    if looks_hub_mode(code):
        body = (
            f"' Generated test wrapper for {example_id} (hub mode)\n"
            f"DAT\n"
            f"        ORGH    $400\n"
            f"{code}\n"
            f"{stub_lines}"
        )
    else:
        body = (
            f"' Generated test wrapper for {example_id} (cog mode)\n"
            f"DAT\n"
            f"        ORG     0\n"
            f"{code}\n"
            f"        JMP     #$\n"
            f"{stub_lines}"
        )
    return body


def write_block(out_dir: Path, example_id: str, lang: str, source: Path, start: int, end: int, raw: str, wrapped: str):
    """Write the wrapped block plus a sidecar meta file."""
    ext = "spin2"  # pnut_ts compiles both as .spin2
    src_file = out_dir / f"{example_id}.{ext}"
    src_file.write_text(wrapped, encoding="utf-8")
    meta = {
        "id": example_id,
        "lang": lang,
        "source_file": str(source.relative_to(source.parents[2])),
        "source_lines": [start, end],
        "wrapped": wrapped != raw,
        "raw_size": len(raw),
    }
    (out_dir / f"{example_id}.meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


ANSI_ESC = re.compile(r"\x1b\[[0-9;]*m")
ERROR_LINE = re.compile(r":error:", re.IGNORECASE)
UNDEF_SYM_AT = re.compile(r":(\d+):error:Undefined symbol")

# PASM2 / Spin2 reserved words we must never stub.
# Opcodes are loaded from the YAML KB at runtime; rest are hardcoded.
RESERVED_WORDS = set()


def load_reserved_words():
    """Populate RESERVED_WORDS from the YAML KB + hardcoded keywords."""
    global RESERVED_WORDS
    if RESERVED_WORDS:
        return
    kb = Path("/workspaces/P2-Knowledge-Base/deliverables/ai/P2/language/pasm2")
    if kb.exists():
        for y in kb.glob("*.yaml"):
            RESERVED_WORDS.add(y.stem.upper())
    RESERVED_WORDS.update({
        # Conditions
        "IF_C", "IF_NC", "IF_Z", "IF_NZ", "IF_C_AND_Z", "IF_C_AND_NZ",
        "IF_NC_AND_Z", "IF_NC_AND_NZ", "IF_C_OR_Z", "IF_C_OR_NZ",
        "IF_NC_OR_Z", "IF_NC_OR_NZ", "IF_C_NE_Z", "IF_C_EQ_Z",
        "IF_LT", "IF_LE", "IF_EQ", "IF_NE", "IF_GT", "IF_GE",
        "IF_A", "IF_AE", "IF_B", "IF_BE", "IF_00", "IF_01", "IF_10", "IF_11",
        "IF_RET", "IF_ALWAYS", "IF_NEVER", "_RET_",
        # Effects
        "WC", "WZ", "WCZ", "ANDC", "ANDZ", "ORC", "ORZ", "XORC", "XORZ",
        # Special registers
        "DIRA", "DIRB", "OUTA", "OUTB", "INA", "INB", "PA", "PB",
        "PTRA", "PTRB", "IJMP1", "IRET1", "IJMP2", "IRET2", "IJMP3", "IRET3",
        # Built-in symbols
        "POSX", "NEGX", "PI", "TRUE", "FALSE", "COGEXEC", "HUBEXEC",
        "CLKFREQ", "CLKMODE", "_CLKFREQ", "_CLKMODE", "_AUTOCLK",
        "NEWCOG", "COGEXEC_NEW", "HUBEXEC_NEW", "COGEXEC_NEW_PAIR", "HUBEXEC_NEW_PAIR",
        # Spin2/PASM2 keywords
        "CON", "DAT", "VAR", "OBJ", "PUB", "PRI", "RES", "FIT",
        "BYTE", "WORD", "LONG", "ORG", "ORGH", "ORGF",
        "ALIGNL", "ALIGNW", "DITTO", "FILE", "END",
        "BYTEFIT", "WORDFIT", "LONGFIT",
        # Spin2 control-flow words occasionally seen in CON expressions
        "FROM", "TO", "STEP", "REPEAT", "UNTIL", "WHILE", "CASE",
        "ABORT", "RETURN", "NEXT", "QUIT", "OTHER", "IF", "IFNOT",
        "ELSE", "ELSEIF",
    })


def find_undef_symbol_on_line(file_path: Path, lineno: int, already_stubbed: set):
    """Read the source file and return the leftmost non-reserved identifier
    that isn't already stubbed. pnut_ts reports only line (no column), so the
    leftmost is the most likely candidate."""
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return None
    lines = text.splitlines()
    if lineno < 1 or lineno > len(lines):
        return None
    line = re.sub(r"'.*$", "", lines[lineno - 1])  # strip comment
    # Collect every identifier already defined anywhere in the file.
    defined = set(already_stubbed)
    for ln in lines:
        ln_nc = re.sub(r"'.*$", "", ln)
        # Bare-at-column-0 label
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s", ln_nc)
        if m:
            defined.add(m.group(1))
        # CON-block style "NAME = value"
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=", ln_nc)
        if m:
            defined.add(m.group(1))
        # RES/LONG/WORD/BYTE declaration with leading label
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s+(?:RES|LONG|WORD|BYTE)\b", ln_nc, re.IGNORECASE)
        if m:
            defined.add(m.group(1))
    for m in IDENT.finditer(line):
        sym = m.group(1)
        if sym.upper() in RESERVED_WORDS:
            continue
        if sym in defined:
            continue
        if sym.startswith("_"):
            continue
        if sym.upper() in {"D", "S", "C", "Z"}:
            continue
        return sym  # leftmost candidate
    return None


def add_stub(wrapped: str, symbol: str) -> str:
    """Append a stub DAT entry for the given symbol to a wrapped fragment."""
    stub_marker = "\n' === auto-stubs ===\n"
    if stub_marker not in wrapped:
        wrapped += stub_marker + "DAT\n        ORG     $1A0\n"
    return wrapped + f"{symbol}        RES     1\n"


def compile_block(example_path: Path, max_iters: int = 40):
    """Run pnut_ts. If 'Undefined symbol' errors occur, iteratively stub the
    offending symbol and retry. Returns (success, output, iterations, stubs)."""
    load_reserved_words()
    stubs = []
    iters = 0
    while iters < max_iters:
        try:
            proc = subprocess.run(
                [PNUT_TS, str(example_path)],
                cwd=example_path.parent,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return False, "TIMEOUT after 30s", iters, stubs
        except FileNotFoundError as e:
            return False, f"pnut_ts not found: {e}", iters, stubs
        out = ((proc.stdout or "") + (proc.stderr or "")).strip()
        out_clean = ANSI_ESC.sub("", out)
        has_error = bool(ERROR_LINE.search(out_clean))
        ok = (proc.returncode == 0) and not has_error
        if ok:
            return True, out_clean, iters, stubs
        # Try to recover from "Undefined symbol" by stubbing
        m = UNDEF_SYM_AT.search(out_clean)
        if not m:
            return False, out_clean, iters, stubs
        lineno = int(m.group(1))
        sym = find_undef_symbol_on_line(example_path, lineno, set(stubs))
        if not sym or sym in stubs:
            return False, out_clean, iters, stubs
        stubs.append(sym)
        current = example_path.read_text(encoding="utf-8")
        example_path.write_text(add_stub(current, sym), encoding="utf-8")
        iters += 1
    return False, "MAX_ITERS exceeded", iters, stubs


def main():
    here = Path(__file__).resolve().parent
    manual_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (here / ".." / "opus-master").resolve()
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else (here / "extracted").resolve()

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    md_files = []
    for path in sorted(manual_root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if SKIP_PATTERNS.search(path.name):
            continue
        md_files.append(path)

    print(f"Manual root: {manual_root}")
    print(f"Output dir:  {out_dir}")
    print(f"Markdown files scanned: {len(md_files)}")
    print(f"pnut_ts: {PNUT_TS}")
    print()

    seq = 0
    results = []
    by_source = {}

    for md in md_files:
        blocks = list(extract_blocks(md))
        if not blocks:
            continue
        by_source.setdefault(str(md.relative_to(manual_root.parent)), 0)
        for lang, start, end, code in blocks:
            seq += 1
            example_id = f"ex{seq:04d}"
            wrapped = make_testable(code, lang, example_id)
            write_block(out_dir, example_id, lang, md, start, end, code, wrapped)
            ok, output, iters, stubs = compile_block(out_dir / f"{example_id}.spin2")
            results.append({
                "id": example_id,
                "lang": lang,
                "source": str(md.relative_to(manual_root.parent)),
                "line_open": start,
                "line_close": end,
                "wrapped": wrapped != code,
                "ok": ok,
                "output": output,
                "auto_stubs": stubs,
                "iterations": iters,
            })
            by_source[str(md.relative_to(manual_root.parent))] += 1
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {example_id}  {md.name}:{start}-{end}  ({lang})")

    # Write JSON of full results
    (out_dir / "RESULTS.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["ok"])
    failed = total - passed
    print()
    print(f"Total: {total}   Pass: {passed}   Fail: {failed}")
    print(f"Results JSON: {out_dir / 'RESULTS.json'}")


if __name__ == "__main__":
    main()
