#!/usr/bin/env python3
"""Detect LaTeX internals (\\@foo) used while `@` is catcode 12 ("other").

WHY THIS EXISTS — F-319, closed 2026-09-11.
-------------------------------------------
`p2kb-platform-foundation.sty` carried a guard meant to suppress the PDF Keywords
field for a document that had not adopted the \\Doc* rights macros:

    \\ifx\\DocCopyright\\@empty ... \\else ... \\fi

It never once fired. The block sat BELOW the file's line-166 `\\makeatother` and
ABOVE its line-425 `\\makeatletter`, so `@` was catcode 12 there. `\\@empty` then
tokenises not as the kernel's empty macro but as the control sequence `\\@`
followed by the four letters `e m p t y` — so the test was really
`\\ifx<macro>\\@`, comparing a rights value against LaTeX's end-of-sentence macro.
False for anything, forever. Every unadopted document took the both-values-present
branch and emitted the malformed `"; licensed under "`.

Nothing in the source LOOKS wrong; the mechanism is invisible to reading, which is
why it survived one confident fix. Only the catcode shows it, and only a real TeX
engine reports the catcode. This script is the cheap static stand-in.

A worse variant of the same class, found by the sweep that followed:

    \\providecommand{\\subtitle}[1]{\\gdef\\@subtitle{#1}}

with `@` at catcode 12 this parses as `\\gdef\\@` with delimiter text `subtitle` —
it GLOBALLY CLOBBERS LaTeX's `\\@` instead of defining `\\@subtitle`.

CATCODE MODEL
-------------
  *.sty  — loaded by \\usepackage, so `@` starts as a LETTER (11).
  *.latex — a pandoc template forming the document body; `@` starts OTHER (12).
  \\makeatletter -> 11, \\makeatother -> 12, tracked in source order.

LIMITS (stated, not hidden): this is a lexical scan. It does not model conditional
branches, `\\input`, or verbatim/listing environments, so a `\\makeatletter` printed
inside a code sample would be miscounted. Treat a hit as "read this line", not as
a verdict — a tool's FAIL is a claim, not a fact.

EXIT: 0 = no findings, 1 = findings, 2 = usage error.
"""
import re
import sys

TOKEN = re.compile(r'\\makeatletter|\\makeatother|\\@[A-Za-z]+')


def scan(path):
    """Yield (lineno, token, source_line) for \\@internals seen while @ is 'other'."""
    cat = 11 if path.endswith('.sty') else 12
    findings = []
    try:
        lines = open(path, encoding='utf-8', errors='replace').readlines()
    except (IsADirectoryError, FileNotFoundError, PermissionError):
        return None
    for n, line in enumerate(lines, 1):
        code = '' if line.lstrip().startswith('%') else line.split('%')[0]
        for m in TOKEN.finditer(code):
            tok = m.group(0)
            if tok == r'\makeatletter':
                cat = 11
            elif tok == r'\makeatother':
                cat = 12
            elif cat == 12:
                findings.append((n, tok, line.rstrip()))
    return findings


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        print("usage: audit-latex-at-catcode.py <file.sty|file.latex> ...", file=sys.stderr)
        return 2
    total = 0
    for path in argv[1:]:
        findings = scan(path)
        if findings is None:
            print(f"SKIP (unreadable): {path}", file=sys.stderr)
            continue
        if findings:
            total += len(findings)
            print(f"\n{path}")
            print(f"  {len(findings)} LaTeX internal(s) used while @ is catcode 12 — "
                  f"these do NOT mean what they appear to mean")
            for n, tok, line in findings:
                print(f"    line {n:>4}  {tok:<18} | {line[:100]}")
    if total:
        print(f"\nFAIL: {total} finding(s). Wrap each site in \\makeatletter ... \\makeatother.")
        return 1
    print(f"PASS: {len(argv) - 1} file(s), no \\@internals outside a \\makeatletter region.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
