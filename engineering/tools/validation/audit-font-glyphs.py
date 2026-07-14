#!/usr/bin/env python3
"""Audit an ASSEMBLED manual markdown for characters the render fonts cannot draw.

WHY THIS EXISTS
---------------
xelatex does NOT fail on a character the font lacks. It emits a
"Missing character:" warning to the log and then **prints nothing at all** —
the glyph silently vanishes from the page. The compile log still reports
0 errors, every other gate passes, and the PDF ships with a hole in it.

That is not cosmetic. It shipped this defect in the Debug Window Manual
(2026-07-14, caught in review before release):

    "MAG gain: multiplies by 2^n"     <- source (superscript n, U+207F)
    "Magnitude gain: multiplies by 2" <- what the PDF actually printed

The superscript n did not render, so a correction to the FFT MAG semantics
turned into a NEW falsehood on the page. A clean compile log proved nothing.

WHAT IT CHECKS
--------------
The ASSEMBLED markdown (what actually goes to the Forge) — not the opus-master
tree — so files that exist but are never assembled (e.g. README-SACRED.md)
cannot raise a false positive. Offending lines are mapped back to their
opus-master chapter so the report points at what the author edits.

The denylist is seeded from characters OBSERVED missing in real Forge compile
logs, plus the emoji/superscript-letter ranges that text fonts do not carry.
When a new "Missing character:" warning appears in a compile log, add the
codepoint here so the next document never reships it.

TEMPLATE GLYPH FALLBACKS (--templates)
-------------------------------------
A codepoint the FONT cannot draw still renders correctly if a template the
document loads declares a \newunicodechar fallback for it. Coverage is therefore
a property of the DOCUMENT's .sty stack, not a global fact -- e.g. U+26A0 WARNING
SIGN is genuinely missing in the Debug Window Manual (which loads only the
platform templates) but renders as a colored triangle in every app note, because
p2kb-appnote-local.sty maps it. Flagging it there is a FALSE POSITIVE, and a gate
that cries wolf on every app note is a gate that gets ignored -- which is exactly
how the next silent glyph-hole ships.

So: pass --templates with the .sty directories the document actually loads. Every
\newunicodechar{X} found is treated as COVERED and will not be flagged. Omit the
flag and the audit stays conservative (font-only), which can over-report.

USAGE
    python3 audit-font-glyphs.py <assembled.md> [--source-dir <opus-master>]
                                                [--templates <dir> [<dir> ...]]

EXIT
    0 = clean    1 = offending glyphs found    2 = bad usage
"""
import re
import sys
import pathlib
import unicodedata

# Codepoints confirmed absent from the render fonts (IBM Plex family).
# Seeded from real "Missing character:" warnings in Forge compile logs.
DENY_CODEPOINTS = {
    0x207F,  # SUPERSCRIPT LATIN SMALL LETTER N   -- observed missing 2026-07-14
    0x26A0,  # WARNING SIGN                       -- observed missing 2026-07-14
    0xFE0F,  # VARIATION SELECTOR-16 (emoji form) -- observed missing 2026-07-14
}

# Ranges text fonts do not carry.
#
# SUPERSCRIPTS/SUBSCRIPTS -- LETTERS only, NOT digits. The U+2070..U+209F block
# mixes them, and the render font (IBM Plex) carries the DIGITS but not the
# LETTERS. Proven both ways in SHIPPED PDFs:
#   renders   -- '2⁶ and 2⁷' and 'log₂' print correctly in P2AN002 v1.0.1
#   missing   -- 'ⁿ' (superscript n) printed NOTHING in the Debug Window Manual,
#                silently turning "MAG multiplies by 2^n" into "multiplies by 2"
# A blanket 2070..209F range flagged the digits too, which would have forced
# correct, well-rendering math to be butchered into prose ("to the power 6") --
# a false positive that DEGRADES the document. Deny only what is actually absent:
#   U+2071        superscript i
#   U+207F        superscript n
#   U+2090..209C  subscript letters (a e o x schwa h k l m n p s t)
# Latin-1 superscript digits (U+00B2/B3/B9) render and are likewise not denied.
DENY_RANGES = [
    (0x2071, 0x2071, "superscript letter"),
    (0x207F, 0x207F, "superscript letter"),
    (0x2090, 0x209C, "subscript letters"),
    (0x1F300, 0x1FAFF, "emoji"),
    (0x2600, 0x27BF, "misc symbols / dingbats"),
    (0xFE00, 0xFE0F, "variation selectors"),
]


# \newunicodechar{X}{...} -- the template supplying a glyph the font lacks.
_NEWUNICODECHAR = re.compile(r"\\newunicodechar\s*\{(.)\}")


def covered_by_templates(dirs):
    """Codepoints a loaded template explicitly draws via \\newunicodechar.

    These render correctly even though the font cannot draw them, so they are
    NOT defects. Scans *.sty in each given directory (non-recursive: a template
    stack is flat).
    """
    covered = {}
    for d in dirs:
        p = pathlib.Path(d)
        if not p.is_dir():
            continue
        for sty in sorted(p.glob("*.sty")):
            for line in sty.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.lstrip().startswith("%"):      # a commented-out mapping does not render
                    continue
                for m in _NEWUNICODECHAR.finditer(line):
                    covered.setdefault(ord(m.group(1)), sty.name)
    return covered


def offending(ch: str, covered=None):
    cp = ord(ch)
    if covered and cp in covered:
        return None                                    # the template draws it
    if cp in DENY_CODEPOINTS:
        return "known-missing glyph"
    for lo, hi, why in DENY_RANGES:
        if lo <= cp <= hi:
            return why
    return None


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2

    assembled = pathlib.Path(args[0])
    if not assembled.is_file():
        print(f"ERROR: not a file: {assembled}")
        return 2

    source_dir = None
    if "--source-dir" in sys.argv:
        source_dir = pathlib.Path(sys.argv[sys.argv.index("--source-dir") + 1])

    # --templates <dir> [<dir> ...] : .sty stacks this document loads. Any
    # \newunicodechar they declare supplies a glyph the font lacks, so it renders.
    template_dirs = []
    if "--templates" in sys.argv:
        for a in sys.argv[sys.argv.index("--templates") + 1:]:
            if a.startswith("--"):
                break
            template_dirs.append(a)
    covered = covered_by_templates(template_dirs)

    # Map each offending character back to the chapter that authored it.
    def chapters_containing(ch: str):
        if not source_dir or not source_dir.is_dir():
            return []
        return sorted(
            p.name for p in source_dir.glob("*.md")
            if ch in p.read_text(encoding="utf-8")
        )

    hits = []
    bq_headings = []
    for lineno, line in enumerate(assembled.read_text(encoding="utf-8").splitlines(), 1):
        for col, ch in enumerate(line, 1):
            why = offending(ch, covered)
            if why:
                hits.append((lineno, col, ch, why, line.strip()[:70]))
        # A heading nested in a blockquote ("> ### Title") does NOT survive the
        # LaTeX escape: the '#' is not at column 0, so latex-escape-all.sh escapes
        # it and the reader sees a literal "### Title" on the page. Shipped this
        # way once (Debug Window Manual ch08, 2026-07-14). Use a bold lead-in
        # ("> **Title.**") for a callout heading instead.
        if line.lstrip().startswith(">") and line.lstrip(" >").startswith("#"):
            bq_headings.append((lineno, line.strip()[:70]))

    # State the exemptions out loud -- a silent exemption is how a real defect
    # hides behind a template fallback that was later removed.
    if covered:
        chars = " ".join(sorted(chr(cp) for cp in covered))
        print(f"{assembled.name}: template fallbacks honored ({len(covered)}): {chars}")

    if not hits and not bq_headings:
        print(f"{assembled.name}: OK (no non-renderable glyphs, no blockquote headings)")
        return 0

    if bq_headings:
        print(f"\n{assembled.name}: HEADING INSIDE A BLOCKQUOTE\n")
        for lineno, ctx in bq_headings:
            print(f"  line {lineno}: {ctx}")
        print(
            "\nThese print as LITERAL '###' on the page -- the '#' is not at column 0,\n"
            "so the LaTeX escape step escapes it instead of pandoc making a heading.\n"
            "Use a bold lead-in for a callout heading:  > **Title.**\n"
        )
        if not hits:
            return 1

    print(f"\n{assembled.name}: NON-RENDERABLE GLYPHS FOUND\n")
    for lineno, col, ch, why, ctx in hits:
        try:
            name = unicodedata.name(ch)
        except ValueError:
            name = "?"
        if not source_dir or not source_dir.is_dir():
            where = "(no --source-dir given)"
        else:
            where = ", ".join(chapters_containing(ch)) or "(not in source - stale assembly? re-run assemble)"
        print(f"  line {lineno}:{col}  {ch!r} U+{ord(ch):04X} {name}  [{why}]")
        print(f"      authored in: {where}")
        print(f"      context: {ctx}")

    print(
        f"\nFAIL: {len(hits)} character(s) the render font cannot draw.\n"
        "xelatex will NOT error -- it prints NOTHING and leaves a hole in the page,\n"
        "so the compile log will look clean. Replace each character with a form the\n"
        "font carries (e.g. 'to the power n' instead of a superscript n; drop the emoji).\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
