#!/usr/bin/env python3
"""
audit-inline-code-ascii.py - flag non-ASCII characters inside INLINE code spans.

WHY THIS EXISTS
    The P2 manuals render with pandoc's `--listings`. An inline code span
    (`like this`) becomes \\lstinline, and xelatex's listings package is STRICT:
    a non-ASCII character inside \\lstinline aborts the build with
    "! Undefined control sequence" (e.g. a U+2212 MINUS or U+2026 ELLIPSIS that
    crept in via a smart editor / paste). The pandoc -> .tex step succeeds, so the
    failure only shows up after a full PDF Forge round-trip - exactly the wasted
    cycle this gate prevents. Code is ASCII; inline code spans must be ASCII.

    SCOPE IS INLINE ONLY, ON PURPOSE. Fenced code BLOCKS (```pasm2 / ```formula /
    ```layout ...) become lstlisting, which tolerates the non-ASCII this stack
    actually uses (x MULTIPLICATION, -> ARROW, u MICRO, deg, box-drawing in
    formula/diagram blocks) - those render correctly and are intentional, so
    flagging them would be false positives. Only \\lstinline is strict.

USAGE
    audit-inline-code-ascii.py [--quiet] <markdown-file> [<markdown-file> ...]

EXIT STATUS
    0  no non-ASCII inside any inline code span
    1  one or more non-ASCII characters inside inline code (gate failure)
    2  usage error (a path that is not a file)

FIX
    Replace the character with its ASCII equivalent (- for U+2212, ... for U+2026,
    " ' for smart quotes, etc.), or move it out of the code span into prose.
"""

import argparse
import os
import re
import sys
import unicodedata

# A fenced code/raw block opens with 3+ backticks or tildes at (indented) line
# start. We SKIP everything inside a fence - inline scanning is for prose lines.
FENCE_RE = re.compile(r'^(\s*)(`{3,}|~{3,})(.*)$')
# An inline code span: a run of N backticks, content, the same run of N backticks.
INLINE_CODE_RE = re.compile(r'(`+)(.+?)\1')


def scan_markdown(md_path):
    """Return [(lineno, col, char, codepoint, name, line)] for non-ASCII in inline code."""
    with open(md_path, encoding='utf-8') as fh:
        lines = fh.readlines()

    hits = []
    in_fence = None  # (marker_char, marker_len) while inside a fenced block
    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip('\n')
        m = FENCE_RE.match(line)
        if in_fence is None:
            if m:                      # opens a fenced block -> skip its contents
                in_fence = (m.group(2)[0], len(m.group(2)))
            else:
                _scan_inline_spans(line, idx, hits)
            continue
        # inside a fence: a same-char, >=length, info-less fence closes it
        if m and m.group(2)[0] == in_fence[0] and len(m.group(2)) >= in_fence[1] \
                and m.group(3).strip() == '':
            in_fence = None
    return hits


def _scan_inline_spans(line, lineno, hits):
    for span in INLINE_CODE_RE.finditer(line):
        content, base = span.group(2), span.start(2)
        for off, ch in enumerate(content):
            if ord(ch) > 127:
                hits.append((lineno, base + off + 1, ch, ord(ch),
                             unicodedata.name(ch, '?'), line.strip()))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='Flag non-ASCII characters inside inline code spans '
                    '(they break xelatex \\lstinline).')
    ap.add_argument('files', nargs='+', help='manual markdown source file(s)')
    ap.add_argument('--quiet', action='store_true',
                    help='print only violations and the summary')
    args = ap.parse_args(argv)

    total = 0
    files_hit = 0
    for md in args.files:
        if not os.path.isfile(md):
            print(f'error: not a file: {md}', file=sys.stderr)
            return 2
        hits = scan_markdown(md)
        if hits:
            files_hit += 1
            total += len(hits)
            print(f'\n{md}:')
            for lineno, col, ch, cp, name, text in hits:
                shown = text if len(text) <= 80 else text[:77] + '...'
                print(f'  {md}:{lineno}:{col}: {ch!r} U+{cp:04X} {name}  | {shown}')
        elif not args.quiet:
            print(f'{md}: OK (inline code is ASCII)')

    if total:
        print(f'\nFAIL: {total} non-ASCII char(s) inside inline code in '
              f'{files_hit} file(s). Replace with ASCII (- for minus, ... for '
              f'ellipsis, plain quotes) or move out of the code span — xelatex '
              f'\\lstinline aborts the PDF build on these.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
