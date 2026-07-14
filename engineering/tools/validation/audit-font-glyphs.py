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

USAGE
    python3 audit-font-glyphs.py <assembled.md> [--source-dir <opus-master>]

EXIT
    0 = clean    1 = offending glyphs found    2 = bad usage
"""
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

# Ranges text fonts do not carry. Superscript DIGITS (U+00B2/B3/B9) are Latin-1
# and DO render, so they are deliberately not in these ranges.
DENY_RANGES = [
    (0x2070, 0x209F, "superscript/subscript letters"),
    (0x1F300, 0x1FAFF, "emoji"),
    (0x2600, 0x27BF, "misc symbols / dingbats"),
    (0xFE00, 0xFE0F, "variation selectors"),
]


def offending(ch: str):
    cp = ord(ch)
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
            why = offending(ch)
            if why:
                hits.append((lineno, col, ch, why, line.strip()[:70]))
        # A heading nested in a blockquote ("> ### Title") does NOT survive the
        # LaTeX escape: the '#' is not at column 0, so latex-escape-all.sh escapes
        # it and the reader sees a literal "### Title" on the page. Shipped this
        # way once (Debug Window Manual ch08, 2026-07-14). Use a bold lead-in
        # ("> **Title.**") for a callout heading instead.
        if line.lstrip().startswith(">") and line.lstrip(" >").startswith("#"):
            bq_headings.append((lineno, line.strip()[:70]))

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
