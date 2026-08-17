#!/usr/bin/env python3
"""Audit a generated .tex for markup that leaked through the pipeline.

WHY THIS EXISTS
---------------
Two defects shipped in the Assembly manual and were invisible to every gate we
owned, because both produce a CLEAN COMPILE LOG and CORRECT-LOOKING SOURCE:

  F-284  an unescaped '&' in a table cell became an alignment tab, eating the
         AND out of a bit-level instruction definition. Shipped ~2 releases.
  F-285  '&nbsp;' in prose printed literally, 16 times. Shipped 1 release.

The .tex handed back by the Forge is the ONLY artifact where "what LaTeX
actually received" is visible. This tool sweeps it for the whole class.

DESIGN RULE: ZERO FALSE POSITIVES, OR IT GETS IGNORED
-----------------------------------------------------
The first hand-run of this sweep (2026-08-17, across all 8 outbound .tex)
produced exactly ONE true finding and a pile of false positives. Every FP is
encoded as an exclusion here, because a gate that cries wolf is a gate that
gets ignored -- which is how the next real hole ships:

  ``            LaTeX's opening double-quote, NOT literal markdown.
  \\textbackslash{}   legitimate P2 '#\\label' absolute-address syntax (x15 in Assembly).
  [text](url)   real DEBUG[DBG_INIT]("...") code sitting inside Verbatim.
  {#1}          macro parameters in the preamble, not a markdown heading anchor.

Verbatim/lstlisting regions are excluded wholesale: they are code, and code
legitimately contains almost every signature below.

Exit 0 = clean. Exit 1 = findings. Exit 2 = usage/IO error.
"""
import re
import sys
from pathlib import Path

# Regions whose contents are code and must never be scanned.
VERBATIM_ENVS = ("Verbatim", "verbatim", "lstlisting", "minted", "alltt")
_BEGIN = re.compile(r"\\begin\{(" + "|".join(VERBATIM_ENVS) + r")\}")
_END = re.compile(r"\\end\{(" + "|".join(VERBATIM_ENVS) + r")\}")

# --- checks -----------------------------------------------------------------
# Each: (id, human description, compiled regex, preamble_ok)
# preamble_ok=True means "also scan before \begin{document}".
CHECKS = [
    # F-285's exact signature. The escaper turns & into \&, so a source entity
    # arrives here as '\&name;'. Match the bare form too, in case escaping is
    # ever reordered.
    ("html-entity",
     "HTML entity printing literally on the page (F-285)",
     re.compile(r"\\&(?:[A-Za-z][A-Za-z0-9]{1,10}|\#[0-9]{1,6}|\#[xX][0-9A-Fa-f]{1,5});"
                r"|(?<!\\)&(?:nbsp|amp|lt|gt|quot|apos|ndash|mdash|hellip|deg|times);"),
     False),

    # Raw HTML that pandoc did not convert. Anchored to real tag shapes so a
    # bare '<' or a math '<' never matches.
    ("raw-html-tag",
     "raw HTML tag emitted into LaTeX",
     re.compile(r"</?(?:div|span|br|hr|p|b|i|u|em|strong|code|pre|table|tr|td|th|"
                r"ul|ol|li|h[1-6]|img|a)(?:\s[^<>\n]{0,120})?/?>"),
     False),

    # A markdown heading that never became a sectioning command. After escaping
    # these appear as '\#\#\# Title' at line start.
    #
    # The trailing \s+ is REQUIRED, and is spec-correct rather than a fudge:
    # CommonMark only recognizes an ATX heading when whitespace follows the
    # hashes. Without it this fires on legitimate PASM2 AUGS syntax -- Assembly
    # prose carries '##Label for a 20-bit signed offset', where '##' is the
    # 32-bit-immediate prefix, not a heading. That was this check's only false
    # positive across all eight outbound .tex.
    #
    # The count is 2..6 (H2-H6), not 1..6, for the same reason: a table header
    # row whose first cell is '#' meaning "number" emits '\# & Region & ...',
    # which a 1..6 form flags three times in the Single-Step Debugger manual. A
    # leaked H1 is not a real risk here anyway -- the pagination filter converts
    # every level-1 header, and a missed one shows up as a missing chapter in the
    # TOC check, which release-manual already performs.
    ("literal-md-heading",
     "markdown heading left as literal text",
     re.compile(r"^\s*(?:\\\#){2,6}\s+\S"),
     False),

    # A fence that never became an environment.
    ("literal-md-fence",
     "markdown code fence left as literal text",
     re.compile(r"^\s*(?:```|\\`\\`\\`)"),
     False),

    # Unconverted emphasis. Requires non-space content and a closing pair on the
    # same line, so a lone '**' or a math '*' does not match.
    ("literal-md-bold",
     "markdown bold left as literal text",
     re.compile(r"\*\*[^\s*][^*\n]{0,120}\*\*"),
     False),

    # Escaping applied twice: the reader sees a backslash.
    ("double-escape",
     "double-escaped special character",
     re.compile(r"\\textbackslash\{\}\\[&%#_$]|\\\\[&%#_](?![a-zA-Z])"),
     False),

    # A raw-latex passthrough block that leaked its own marker.
    ("latex-passthrough-leak",
     "'{=latex}' passthrough marker leaked into output",
     re.compile(r"\{=latex\}"),
     True),

    # Unresolved cross-reference. LaTeX prints '??' when a \ref finds no label.
    ("unresolved-ref",
     "'??' unresolved reference marker",
     re.compile(r"(?<![?\\])\?\?(?!\?)"),
     False),

    # Authoring markers that must never ship.
    ("todo-marker",
     "TODO/FIXME/XXX marker in shipped text",
     re.compile(r"\b(?:TODO|FIXME|XXX|TBD|PLACEHOLDER)\b"),
     False),
]


def scan(path):
    """Return a list of (check_id, description, line_no, line_text)."""
    text = Path(path).read_text(errors="replace")
    lines = text.splitlines()

    # Locate \begin{document} so preamble-only noise can be skipped.
    doc_start = 0
    for i, ln in enumerate(lines):
        if "\\begin{document}" in ln:
            doc_start = i
            break

    findings = []
    depth = 0
    for i, ln in enumerate(lines, start=1):
        # Track verbatim nesting; the begin/end lines themselves are structural.
        if _BEGIN.search(ln):
            depth += 1
            continue
        if _END.search(ln):
            depth = max(0, depth - 1)
            continue
        if depth > 0:
            continue

        in_preamble = i <= doc_start
        for cid, desc, rx, preamble_ok in CHECKS:
            if in_preamble and not preamble_ok:
                continue
            if rx.search(ln):
                findings.append((cid, desc, i, ln.strip()[:160]))
    return findings


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        print("Usage: audit-tex-artifacts.py <file.tex> [more.tex ...]")
        return 2

    total = 0
    for p in argv[1:]:
        if not Path(p).is_file():
            print(f"SKIP (not a file): {p}")
            continue
        try:
            findings = scan(p)
        except OSError as e:
            print(f"ERROR reading {p}: {e}")
            return 2
        name = Path(p).name
        if not findings:
            print(f"CLEAN  {name}")
            continue
        total += len(findings)
        print(f"\nFINDINGS  {name}  ({len(findings)})")
        by_id = {}
        for cid, desc, ln, txt in findings:
            by_id.setdefault((cid, desc), []).append((ln, txt))
        for (cid, desc), hits in sorted(by_id.items()):
            print(f"  [{cid}] {desc} -- {len(hits)}")
            for ln, txt in hits[:8]:
                print(f"      {p}:{ln}: {txt}")
            if len(hits) > 8:
                print(f"      ... and {len(hits) - 8} more")

    print(f"\n{'CLEAN' if total == 0 else f'{total} finding(s)'}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
