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


CODE, COMMENT, STRING, DEBUG_STRING = 0, 1, 2, 3

CONTEXT_NAME = {
    CODE:         "in CODE",
    COMMENT:      "in a comment",
    STRING:       "in a STRING LITERAL",
    DEBUG_STRING: "in a DEBUG() STRING",
}

# Why the context matters, and why a clean compile does not settle it.
#
#   DEBUG_STRING  the byte goes out the debug link at RUNTIME. A codepoint above
#                 127 arrives as multi-byte UTF-8, so the terminal can take the
#                 stream as BINARY rather than ASCII, mis-render, or act on an
#                 escape it was never sent. The expected output is destroyed and
#                 nothing in the build says so.
#   STRING        same class wherever the string is finally emitted.
#   CODE          identifier / operator position: the compiler's problem.
#   COMMENT       never reaches the P2; the cost is the reader's own editor, and
#                 byte-identity with the printed block in the manual.
#
# `pnut-ts` exiting 0 proves NONE of the first three are harmless -- it proves the
# file parsed. Severity is a runtime property, so the report states the context
# and lets the reader weigh it.
CONTEXT_SEVERITY = {
    DEBUG_STRING: "RUNTIME - corrupts debug output / terminal state",
    STRING:       "RUNTIME - corrupts emitted text",
    CODE:         "COMPILE / semantics",
    COMMENT:      "portability - reader's editor + printed-block identity",
}


def context_mask(text):
    """Per-character context code for the WHOLE file (CODE/COMMENT/STRING/DEBUG_STRING).

    Spin2 comments come in two shapes and only one of them is line-bounded:
        '  ''        to end of line
        { } {{ }}    BRACE form -- nests, and SPANS LINES

    The brace form is the one that matters here: a box-drawing diagram is almost
    always a multi-line { } block, which is exactly the shape the guide's own
    example uses. A single-line approximation rejected every such diagram --
    caught by the negative control, not by reading the code.

    Strings are tracked so a brace inside "..." cannot open a phantom comment --
    and so a non-ASCII byte inside one can be reported as the runtime defect it is
    rather than lumped in with comment prose.

    A string counts as a DEBUG string when it sits inside a `debug(...)` call.
    `debug()` cannot be continued across lines, so its span is found per line.
    """
    mask = bytearray(len(text))     # default CODE (0)
    debug_spans = []
    pos = 0
    for line in text.splitlines(keepends=True):
        low = line.lower()
        k = 0
        while True:
            k = low.find("debug", k)
            if k < 0:
                break
            j = k + 5
            while j < len(line) and line[j] in " \t":
                j += 1
            # `debug(` or `debug[n](` both count
            if j < len(line) and line[j] in "([":
                depth, m = 0, j
                while m < len(line):
                    if line[m] in "([":
                        depth += 1
                    elif line[m] in ")]":
                        depth -= 1
                        if depth == 0:
                            break
                    m += 1
                debug_spans.append((pos + k, pos + min(m + 1, len(line))))
            k += 5
        pos += len(line)

    def in_debug(idx):
        return any(lo <= idx < hi for lo, hi in debug_spans)

    i, n = 0, len(text)
    depth = 0                       # brace-comment nesting depth
    while i < n:
        ch = text[i]
        if depth:
            mask[i] = COMMENT
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
                mask[k] = COMMENT
            i = j
            continue
        if ch == "{":
            depth = 1
            mask[i] = COMMENT
            i += 1
            continue
        if ch == '"':               # string literal -- single line in Spin2
            kind = DEBUG_STRING if in_debug(i) else STRING
            j = i + 1
            while j < n and text[j] != '"' and text[j] != "\n":
                mask[j] = kind
                j += 1
            mask[i] = kind
            if j < n and text[j] == '"':
                mask[j] = kind
                i = j + 1
            else:
                i = j
            continue
        i += 1

    # INSIDE debug(...) NOTHING IS A COMMENT ({{USER_NAME}}, 2026-08-22).
    # Everything between the parens is payload bound for the debug link, so text
    # that merely LOOKS like commentary is transmitted, not stripped. Marking the
    # whole span DEBUG_STRING does two things at once: it raises the severity to
    # runtime, and it withdraws the box-drawing exception there -- a diagram is
    # fine in a comment and is multi-byte UTF-8 down the wire in a debug().
    for lo, hi in debug_spans:
        for idx in range(lo, min(hi, n)):
            mask[idx] = DEBUG_STRING
    return mask


def audit_file(path: pathlib.Path):
    """Return a list of (lineno, col, char, reason, suggestion)."""
    hits = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [(0, 0, "", "file is not valid UTF-8 -- cannot be ASCII either", "")]
    mask = context_mask(text)
    lineno, col = 1, 1
    for idx, ch in enumerate(text):
        if ch == "\n":
            lineno, col = lineno + 1, 1
            continue
        cp = ord(ch)
        if cp >= 128:
            ctx = mask[idx]
            if in_box_range(cp):
                # Permitted ONLY in a comment. In a string it still reaches the
                # terminal as multi-byte UTF-8, so the exception does not apply.
                if ctx != COMMENT:
                    hits.append((lineno, col, ch, ctx,
                                 "box-drawing character " + CONTEXT_NAME[ctx], ""))
            else:
                hits.append((lineno, col, ch, ctx,
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
    by_ctx = {}
    for f in files:
        hits = audit_file(f)
        if not hits:
            continue
        total += len(hits)
        rel = f.relative_to(root) if root in f.resolve().parents else f
        for lineno, col, ch, ctx, why, fix in hits:
            if not ch:                      # file-level problem (bad encoding)
                print(f"{rel}: {why}")
                continue
            by_ctx[ctx] = by_ctx.get(ctx, 0) + 1
            tail = f"  ->  use {fix!r}" if fix else ""
            print(f"{rel}:{lineno}:{col}: U+{ord(ch):04X} {ch!r} {why} "
                  f"[{CONTEXT_NAME[ctx]}]{tail}")

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
        # Severity is a property of WHERE the byte sits, not of the count. A
        # debug string reaches the terminal at runtime; a comment never leaves
        # the repo. Break the total out so the reader can triage.
        print(f"\nFAIL  {total} violation(s) across {len(files)} audited file(s)")
        for ctx in (DEBUG_STRING, STRING, CODE, COMMENT):
            if by_ctx.get(ctx):
                print(f"      {by_ctx[ctx]:4d}  {CONTEXT_NAME[ctx]:<22} "
                      f"{CONTEXT_SEVERITY[ctx]}")
        return 1
    print(f"PASS  {len(files)} file(s) conformant "
          f"(spin2-authoring-guide Sec 1.1: ASCII only, "
          f"box drawing U+2500-257F / U+2580-259F permitted in comments)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
