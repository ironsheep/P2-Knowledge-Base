#!/usr/bin/env python3
"""
audit-inline-run-width.py - flag inline-code runs too long to break in a line.

WHY THIS EXISTS
    An inline code span becomes \\lstinline, which LaTeX treats as one unbreakable
    box. Several spans glued by `/` or an ellipsis become one longer box, because
    there is no break opportunity between them either. When such a box lands at a
    line end, justification cannot absorb it and it protrudes into the margin.

    This shipped in two manuals at once:
        WORDS_1BIT/2BIT/4BIT/8BIT                                 (25 rendered chars)
        P_PASS_AB/P_AND_AB/P_OR_AB/P_XOR_AB/P_FILT0_AB…P_FILT3_AB (57 rendered chars)

    The second was found only after a render, because the sweep that should have
    caught it was an interactive `grep | head` whose output happened to fill with
    a different manual's short, harmless matches. THE LIST WAS SORTED BY NOTHING
    AND CUT AT TEN. This tool exists so that sweep is never ad hoc again: it
    reports EVERY run, sorted longest-first, with the total count stated up front.

WHAT THE THRESHOLD MEANS
    A long run is a RISK, not a certain defect - whether it protrudes depends on
    where the line breaks land, so a 25-char run can spill on one page while a
    longer one sits mid-line and prints clean. The threshold marks what to
    restructure preemptively rather than discover in a render.

    The converse also holds and is worth stating: a SHORT span can protrude too,
    if it lands at a line end with nothing to absorb it (a 15-character span did,
    in one of these manuals). So this gate reduces render round-trips; it does not
    replace reading the overfull list. That is `audit-render-overfulls.py`.

THE FIX FOR A FLAGGED RUN
    Give LaTeX somewhere to break: separate the alternatives with commas and the
    word "and", or name a range ("`LONGS_1BIT` through `LONGS_16BIT`"). Both read
    better than slash-gluing, which also asks the reader to infer that "/2BIT"
    means "WORDS_2BIT".

USAGE
    audit-inline-run-width.py [--max-chars N] [--quiet] <markdown-file> ...

EXIT STATUS
    0  no run at or above the threshold
    1  one or more runs at or above the threshold
    2  usage error
"""

import argparse
import os
import re
import sys

DEFAULT_MAX = 24

FENCE_RE = re.compile(r'^\s*(?:```|~~~)')
COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)
GLUE = ('/', '…', '...')


def code_runs(line):
    """Runs of 2+ inline-code spans joined only by glue, with rendered width.

    Backticks are TOKENIZED PAIRWISE rather than pattern-matched, because a
    regex has no notion of which backtick opens and which closes. A pattern-based
    version of this check matched interstitial PROSE as a span — in
    "`+/`, not `/` — Spin2's plain `/`" it read ", not " as code and reported a
    38-character run that does not exist. Three of its five findings were that
    same illusion. Splitting on backticks and taking odd indices as code is the
    only way to be sure what is inside a span and what is between two of them.

    Scope is the GLUED run specifically: it has no break opportunity anywhere
    inside it and a trivial fix (commas, or a named range). A single over-long
    span is equally unbreakable but is usually a URL or path the stack already
    handles — that belongs to the render-side overfull check, not here.
    """
    parts = line.split('`')
    if len(parts) < 2:
        return []
    runs, cur, width = [], 0, 0
    # parts[odd] is span content; parts[even] is the text between spans.
    for idx in range(1, len(parts), 2):
        span = parts[idx]
        between = parts[idx - 1] if idx > 1 else None
        if cur and between is not None and between in GLUE:
            cur += 1
            width += len(between) + len(span)
        else:
            if cur >= 2:
                runs.append(width)
            cur, width = 1, len(span)
        if idx + 1 >= len(parts):      # last span closes the line
            break
    if cur >= 2:
        runs.append(width)
    return runs


def run_texts(line):
    """The rendered text of each glued run, parallel to code_runs()."""
    parts = line.split('`')
    out, cur = [], []
    for idx in range(1, len(parts), 2):
        span = parts[idx]
        between = parts[idx - 1] if idx > 1 else None
        if cur and between is not None and between in GLUE:
            cur.append(between)
            cur.append(span)
        else:
            if len(cur) >= 3:
                out.append(''.join(cur))
            cur = [span]
    if len(cur) >= 3:
        out.append(''.join(cur))
    return out


def scan(path, max_chars):
    """Every inline-code run >= max_chars rendered width. Never truncated."""
    text = COMMENT_RE.sub(lambda m: re.sub(r'[^\n]', ' ', m.group(0)),
                          open(path, encoding='utf-8', errors='replace').read())
    hits, in_fence = [], False
    for i, line in enumerate(text.split('\n'), 1):
        probe = line.lstrip()
        while probe.startswith('>'):
            probe = probe[1:].lstrip()
        if FENCE_RE.match(probe):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for rendered in run_texts(line):
            if len(rendered) >= max_chars:
                hits.append((i, len(rendered), rendered))
    return hits


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--max-chars', type=int, default=DEFAULT_MAX,
                    help=f'rendered-width threshold (default {DEFAULT_MAX})')
    ap.add_argument('--quiet', action='store_true', help='print only failures')
    ap.add_argument('files', nargs='+')
    args = ap.parse_args()

    all_hits = []
    for path in args.files:
        if not os.path.isfile(path):
            print(f'not a file: {path}', file=sys.stderr)
            return 2
        for line_no, width, text in scan(path, args.max_chars):
            all_hits.append((width, path, line_no, text))

    if not all_hits:
        if not args.quiet:
            print(f'CLEAN  no inline-code run >= {args.max_chars} chars '
                  f'({len(args.files)} file(s) scanned)')
        return 0

    # Count FIRST, sorted longest-first, and never cut. The whole point.
    all_hits.sort(key=lambda h: -h[0])
    print(f'{len(all_hits)} inline-code run(s) >= {args.max_chars} chars — '
          f'COMPLETE LIST, not a top-N\n')
    for width, path, line_no, text in all_hits:
        print(f'{width:3}ch  {path}:{line_no}')
        print(f'       {text[:90]}')
    print('\nFIX: give LaTeX a break opportunity — separate the alternatives with')
    print('commas and "and", or name a range ("`LONGS_1BIT` through `LONGS_16BIT`").')
    return 1


if __name__ == '__main__':
    sys.exit(main())
