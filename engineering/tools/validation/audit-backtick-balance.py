#!/usr/bin/env python3
"""
audit-backtick-balance.py - flag prose paragraphs with unbalanced inline-code backticks.

WHY THIS EXISTS
    F-294. A single-backtick span whose BODY contains a backtick does not fail;
    it inverts. Pandoc closes a single-backtick span at the first backtick it
    meets, so

        (`debug(`Waves TRIGGER 0 -500 500 256)`)

    parses as the span `debug(`, then plain text, then a NEW span opened by the
    next backtick that runs on until the following one - swallowing whole lines
    of prose into code, and flipping every span after it in the paragraph. In
    the shipped page this printed two lines of ordinary prose in monospace,
    fused words without spaces, and a stray leading period.

    NOTHING ELSE CATCHES IT. The escape processor passes the span through, the
    .tex is legal, the compile log is clean, and the code-line gate measures
    fenced blocks. The only signal was an overfull box - which had been
    explained away as an unbreakable \\lstinline run. This gate is that missing
    instrument, and it runs on the MASTERS, before a render is spent.

    The correct form for backtick-bearing content is the double-backtick span,
    ``debug(`Waves ...)``, which this manual set already uses elsewhere.

WHY PARAGRAPH-WISE, NOT LINE-WISE
    A code span may legally wrap across a newline inside one paragraph
    (`TEXTSIZE size`, `TEXTSTYLE\\nstyle`). A line-wise check calls those
    broken; they are not. Balance is a property of the paragraph.

USAGE
    audit-backtick-balance.py [--quiet] <markdown-file> [<markdown-file> ...]

EXIT STATUS
    0  every prose paragraph balances
    1  one or more unbalanced paragraphs (gate failure)
    2  usage error (a path that is not a file)

FIX
    Find the single-backtick span whose body contains a backtick and promote it
    to a double-backtick span. If the body also ends with a backtick, pad the
    span with one space inside each delimiter.
"""

import argparse
import os
import re
import sys

FENCE_RE = re.compile(r'^\s*(?:```|~~~)')
# Double-backtick spans are the CORRECT form for backtick-bearing content;
# remove them before counting so they never register as an imbalance.
DOUBLE_SPAN_RE = re.compile(r'``.+?``', re.DOTALL)
# Authoring headers live in HTML comments and never reach the page.
COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)


def unbalanced_paragraphs(path):
    """Return [(line_no, paragraph_text)] for prose paragraphs with odd backticks."""
    text = open(path, encoding='utf-8', errors='replace').read()
    # Blank out HTML comments, preserving line structure so numbers stay true.
    text = COMMENT_RE.sub(lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text)

    findings = []
    in_fence = False
    para, start = [], 0

    def flush():
        if not para:
            return
        body = ' '.join(para)
        rest = DOUBLE_SPAN_RE.sub('', body)
        if rest.count('`') % 2 == 1:
            findings.append((start, body.strip()))

    for i, line in enumerate(text.split('\n'), 1):
        # Strip blockquote markers before the fence test - a fenced block inside
        # a blockquote is still a fenced block (the F-291 lesson).
        probe = line.lstrip()
        while probe.startswith('>'):
            probe = probe[1:].lstrip()
        if FENCE_RE.match(probe):
            flush()
            para = []
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not line.strip():
            flush()
            para = []
            continue
        if not para:
            start = i
        para.append(line)
    flush()
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--quiet', action='store_true',
                    help='print only failures')
    ap.add_argument('files', nargs='+')
    args = ap.parse_args()

    total = 0
    for path in args.files:
        if not os.path.isfile(path):
            print(f'not a file: {path}', file=sys.stderr)
            return 2
        hits = unbalanced_paragraphs(path)
        if hits:
            total += len(hits)
            print(f'FINDINGS  {os.path.basename(path)}  ({len(hits)})')
            for line_no, body in hits:
                print(f'  {path}:{line_no}: unbalanced inline-code backticks')
                print(f'      {body[:160]}')
        elif not args.quiet:
            print(f'CLEAN  {os.path.basename(path)}')

    if total:
        print(f'\n{total} unbalanced paragraph(s)')
        print('FIX: promote the single-backtick span whose body contains a '
              'backtick to a ``double-backtick`` span.')
        return 1
    if not args.quiet:
        print('\nCLEAN')
    return 0


if __name__ == '__main__':
    sys.exit(main())
