#!/usr/bin/env python3
"""
audit-spin2-ascii.py - enforce spin2-authoring-guide Sec 1.1 on AUTHORED .spin2 source.

WHY THIS EXISTS
    `pnut-ts` is an ASCII-only compiler. A non-ASCII character in code, a string
    or a signature causes silent corruption or a compile error -- and the guide
    forbids the punctuation set (em dash, en dash, curly quotes, ellipsis) in
    COMMENTS too, because those are the characters an editor or a paste silently
    substitutes.

    Until this script existed the rule was documented at strength `gate` with no
    instrument behind it, which the guide itself calls out: "conform to the style
    guide" with nothing enforcing it "degrades into reading it and hoping." A
    clean `pnut-ts` compile proves legality only -- it has never proven style, and
    an em dash inside a comment compiles perfectly.

WHAT IT ENFORCES (Sec 1.1, exactly as the guide states it)
    Any codepoint above 127 is a FAIL, wherever it appears, EXCEPT the two
    box-drawing ranges the guide explicitly preserves:

        U+2500-U+257F  box drawing
        U+2580-U+259F  block elements

    That exception is ecosystem compatibility, not decoration: those characters
    ship with the Propeller Tool and a large part of the published P1/P2 code base
    draws diagrams with them. The guide says do not propose removing it. They are
    permitted ONLY inside comments; in code they are a FAIL like anything else.

SCOPE -- authored source only, and the exclusions are printed by name
    The repo holds ~2400 .spin2 files and we WROTE a small fraction of them.
    Restyling the rest would be both wrong and meaningless, so the default roots
    are the trees this project actually authors:

        manuals/<slug>/examples-library/         shipped to readers in a .zip
        manuals/<slug>/audit/verification-tests/ the hardware-rig source
        manuals/<slug>/figure-generators/        authored to produce figures
        app-notes/<n>/examples-library/          same contract as a manual's

    Deliberately NOT audited, and why:
        code-validation/   extracted FROM the manuals by a script, then compiled;
                           regenerated on demand, never hand-edited
        REF/ REF-NO-COMMIT/ NO-COMMIT/  third-party or vendor reference material
        engineering/ingestion/          ingested sources -- not ours to restyle
        OBEX/                           community objects, published as received
        archive/ .backups/              frozen records
        extracted_examples/             lifted out of PDFs by tooling

USAGE
    audit-spin2-ascii.py [--quiet] [--list-files] [<path> ...]

    With no path, audits the default roots above. A path may be a file or a
    directory (searched recursively).

EXIT STATUS
    0  every audited file is conformant
    1  one or more violations (gate failure)
    2  usage error

FIX
    Replace with the ASCII form the guide names: `-` for an em or en dash, `'`
    and `"` for curly quotes, `...` for an ellipsis. If the character is carrying
    meaning that ASCII cannot (a real diagram), use the box-drawing ranges, which
    are permitted in comments.
"""

import argparse
import pathlib
import sys
import unicodedata

# The two ranges Sec 1.1 preserves, permitted in COMMENTS only.
BOX_RANGES = [(0x2500, 0x257F), (0x2580, 0x259F)]

# The substitutions an editor makes silently, with the replacement the guide names.
SUGGEST = {
    0x2014: "-",    0x2013: "-",    0x2012: "-",   0x2010: "-",   0x2011: "-",
    0x2018: "'",    0x2019: "'",    0x201A: "'",   0x201B: "'",
    0x201C: '"',    0x201D: '"',    0x201E: '"',   0x201F: '"',
    0x2026: "...",  0x2212: "-",    0x00A0: " ",   0x2007: " ",   0x202F: " ",
    0x00D7: "*",    0x00F7: "/",    0x2192: "->",  0x2190: "<-",  0x21D2: "=>",
    0x00B0: " deg", 0x00B5: "u",    0x03BC: "u",   0x2264: "<=",  0x2265: ">=",
    0x2260: "<>",   0x00B1: "+/-",  0x2022: "*",   0x00AB: '"',   0x00BB: '"',
}

DEFAULT_GLOBS = [
    "engineering/document-production/manuals/*/examples-library/**/*.spin2",
    "engineering/document-production/manuals/*/audit/verification-tests/**/*.spin2",
    "engineering/document-production/manuals/*/figure-generators/**/*.spin2",
    "engineering/document-production/app-notes/*/examples-library/**/*.spin2",
]

# A path containing any of these is never audited, whatever root reached it.
EXCLUDE_PARTS = ("/archive/", "/.backups/", "/REF/", "/REF-NO-COMMIT/",
                 "/NO-COMMIT/", "/code-validation/", "/extracted_examples/")


def in_box_range(cp):
    return any(lo <= cp <= hi for lo, hi in BOX_RANGES)


def comment_mask(text):
    """Per-character 'is inside a comment' mask for the WHOLE file.

    Spin2 comments come in two shapes and only one of them is line-bounded:
        '  ''        to end of line
        { } {{ }}    BRACE form -- nests, and SPANS LINES

    The brace form is the one that matters here: a box-drawing diagram is almost
    always a multi-line { } block, which is exactly the shape the guide's own
    example uses. A single-line approximation rejected every such diagram --
    caught by the negative control, not by reading the code.

    Strings are tracked so a brace inside "..." cannot open a phantom comment.
    """
    mask = bytearray(len(text))
    i, n = 0, len(text)
    depth = 0                       # brace-comment nesting depth
    while i < n:
        ch = text[i]
        if depth:
            mask[i] = 1
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            i += 1
            continue
        if ch == "'":               # line comment, to end of line
            j = text.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                mask[k] = 1
            i = j
            continue
        if ch == "{":
            depth = 1
            mask[i] = 1
            i += 1
            continue
        if ch == '"':               # string literal -- single line in Spin2
            j = i + 1
            while j < n and text[j] != '"' and text[j] != "\n":
                j += 1
            i = j + 1 if j < n and text[j] == '"' else j
            continue
        i += 1
    return mask


def audit_file(path: pathlib.Path):
    """Return a list of (lineno, col, char, reason, suggestion)."""
    hits = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [(0, 0, "", "file is not valid UTF-8 -- cannot be ASCII either", "")]
    mask = comment_mask(text)
    lineno, col, base = 1, 1, 0
    for idx, ch in enumerate(text):
        if ch == "\n":
            lineno, col = lineno + 1, 1
            continue
        cp = ord(ch)
        if cp >= 128:
            if in_box_range(cp):
                if not mask[idx]:
                    hits.append((lineno, col, ch,
                                 "box-drawing character OUTSIDE a comment", ""))
            else:
                hits.append((lineno, col, ch,
                             unicodedata.name(ch, "unnamed codepoint"),
                             SUGGEST.get(cp, "")))
        col += 1
    return hits


def collect(paths, root: pathlib.Path):
    files, roots_used = [], []
    if paths:
        for p in paths:
            q = pathlib.Path(p)
            if q.is_file():
                files.append(q)
            elif q.is_dir():
                files.extend(sorted(q.rglob("*.spin2")))
            else:
                print(f"ERROR: not a file or directory: {q}")
                return None, None
        roots_used = [str(p) for p in paths]
    else:
        for g in DEFAULT_GLOBS:
            files.extend(sorted(root.glob(g)))
        roots_used = DEFAULT_GLOBS
    keep = [f for f in files
            if not any(part in str(f) for part in EXCLUDE_PARTS)]
    return sorted(set(keep)), roots_used


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", metavar="PATH",
                    help="file or directory; default = the authored roots")
    ap.add_argument("--quiet", action="store_true",
                    help="print only violations and the summary line")
    ap.add_argument("--list-files", action="store_true",
                    help="print every audited path, then exit")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parents[3]
    files, roots_used = collect(args.paths, root)
    if files is None:
        return 2

    if args.list_files:
        for f in files:
            print(f.relative_to(root) if root in f.resolve().parents else f)
        print(f"\n{len(files)} file(s)")
        return 0

    if not files:
        print("ERROR: no .spin2 files matched -- check the path or the roots")
        return 2

    total = 0
    for f in files:
        hits = audit_file(f)
        if not hits:
            continue
        total += len(hits)
        rel = f.relative_to(root) if root in f.resolve().parents else f
        for lineno, col, ch, why, fix in hits:
            tail = f"  ->  use {fix!r}" if fix else ""
            print(f"{rel}:{lineno}:{col}: U+{ord(ch):04X} {ch!r} {why}{tail}"
                  if ch else f"{rel}: {why}")

    # Say what was audited. A gate whose coverage is invisible is a gate that can
    # silently stop covering the thing most likely to be wrong.
    if not args.quiet:
        print()
        if not args.paths:
            print("roots audited:")
            for g in roots_used:
                print(f"  {g}")
            print("excluded by rule: " + ", ".join(p.strip('/') for p in EXCLUDE_PARTS))
    if total:
        print(f"\nFAIL  {total} violation(s) across {len(files)} audited file(s)")
        return 1
    print(f"PASS  {len(files)} file(s) conformant "
          f"(spin2-authoring-guide Sec 1.1: ASCII only, "
          f"box drawing U+2500-257F / U+2580-259F permitted in comments)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
