#!/usr/bin/env python3
"""
audit-render-overfulls.py - derive the COMPLETE page-verify worklist from a render.

WHY THIS EXISTS
    Every other gate in this repo reads markdown. Overfull boxes do not exist
    until xelatex has typeset the document, so the one defect class with no
    pre-render gate is also the one whose only signal is the compile log.

    Twice in one session that signal was misread, and both times the same two
    habits did it:

      1. TRUNCATION. The overfull list was ranked with `sort -rn | head -8`.
         A 30pt defect sat just below the cutoff, and because nothing said the
         list was capped, the output read as complete. A silent cap is
         indistinguishable from completeness.

      2. A MOVING BAR. A protruding identifier on one page was opened, seen,
         and written off as "a cosmetic overhang." One round later the same
         pixels were called a defect. Case-by-case adjudication with no written
         threshold gives different verdicts on identical evidence, so each pass
         "discovers" what the last pass dismissed.

    This tool removes both. It enumerates EVERY overfull at or above the
    threshold - never a top-N - maps each to a printed page, and emits a
    worklist with one row per site. The count is stated up front, so a capped
    reading is impossible to mistake for a complete one.

WHAT IT DOES NOT DO
    It does not judge. An overfull is a POINTER TO A PAGE, not a defect: a 45pt
    overfull can print clean while a 30pt one spills into the margin, because
    the magnitude is the badness of the line-break, not the size of what shows.
    So this tool tells you exactly which pages to open and refuses to guess the
    verdict. You open every page it names and record a verdict for each.

    THE THRESHOLD IS THE ONLY THING THAT MAKES THIS ONE-AND-DONE. Fix it in
    writing, apply it to every row, and a later pass cannot re-promote what an
    earlier pass dismissed.

USAGE
    audit-render-overfulls.py <compile.log> [--tex FILE] [--pdf FILE]
                              [--min-pt N] [--verdicts FILE]

    --tex/--pdf together map each overfull to a printed page number by pulling a
    distinctive phrase from the .tex source range and locating it in the PDF
    text. Without them you still get the complete ranked list with source lines.

    --verdicts takes a file of "page: verdict" lines from a previous pass and
    flags any row lacking one, so an unjudged site cannot pass silently.

EXIT STATUS
    0  no overfull at or above the threshold, or every row has a recorded verdict
    1  rows need a verdict (open the pages)
    2  usage error
"""

import argparse
import os
import re
import subprocess
import sys

OVERFULL_RE = re.compile(
    r'Overfull \\hbox \((?P<pt>[0-9.]+)pt too wide\) in '
    r'(?P<kind>paragraph|alignment) at lines (?P<start>\d+)--(?P<end>\d+)'
)
# A Verbatim/code environment: an overfull pointing into one is a code line
# running out of its box, which is a different (worse) defect than prose.
CODE_ENV_RE = re.compile(r'\\begin\{(Verbatim|lstlisting)')


def parse_log(path, min_pt):
    """Every overfull >= min_pt, deduplicated across xelatex passes."""
    seen, rows = set(), []
    with open(path, encoding='utf-8', errors='replace') as fh:
        for m in OVERFULL_RE.finditer(fh.read()):
            pt = float(m.group('pt'))
            if pt < min_pt:
                continue
            key = (m.group('start'), m.group('end'), f'{pt:.2f}')
            if key in seen:          # xelatex reports once per pass
                continue
            seen.add(key)
            rows.append({'pt': pt, 'kind': m.group('kind'),
                         'start': int(m.group('start')), 'end': int(m.group('end'))})
    return sorted(rows, key=lambda r: -r['pt'])


def tex_context(tex_lines, start, end):
    """The source text an overfull covers, plus whether it is inside code."""
    chunk = tex_lines[start - 1:end]
    in_code = any(CODE_ENV_RE.search(l) for l in chunk)
    return chunk, in_code


def probe_phrases(chunk):
    """Candidate phrases for locating this paragraph in the PDF, best first.

    Yields several, because one probe is a single point of failure: a verbatim
    line must be taken LITERALLY (stripping markup mangles code into something
    that appears nowhere), while a prose line must have its markup removed. An
    earlier version used one strategy for both and silently failed to resolve a
    page — reporting "page=?" for a site that was perfectly findable.
    """
    cands, verbatim = [], False
    for line in chunk:
        if re.search(r'\\begin\{(Verbatim|lstlisting)', line):
            verbatim = True
            continue
        if re.search(r'\\end\{(Verbatim|lstlisting)', line):
            verbatim = False
            continue
        if verbatim:
            # literal code: use as-is, it appears verbatim in the PDF text
            s = ' '.join(line.split())
            if len(s) > 12:
                cands.append(s[:60])
            continue
        s = re.sub(r'\\passthrough\{\\lstinline!([^!]*)!\}', r'\1', line)
        s = re.sub(r'\\[a-zA-Z]+\*?(\[[^]]*\])?(\{[^}]*\})?', ' ', s)
        s = s.replace('---', '—').replace('``', '"').replace("''", '"')
        s = re.sub(r'[{}\\]', ' ', s)
        words = [w for w in ' '.join(s.split()).split() if len(w) > 3]
        if len(words) >= 4:
            cands.append(' '.join(words[:5]))
    return cands


def pdf_pages(pdf):
    out = subprocess.run(['pdftotext', '-layout', pdf, '-'],
                         capture_output=True, text=True)
    return out.stdout.split('\f') if out.returncode == 0 else None


def find_page(pages, phrase):
    if not pages or not phrase:
        return None
    norm = lambda s: ' '.join(s.split())
    target = norm(phrase)
    for i, pg in enumerate(pages, 1):
        if target in norm(pg):
            return i
    # fall back to a shorter prefix - line-wrapping can split the phrase
    short = ' '.join(target.split()[:3])
    for i, pg in enumerate(pages, 1):
        if short in norm(pg):
            return i
    return None


def load_verdicts(path):
    v = {}
    if not path or not os.path.isfile(path):
        return v
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#') or ':' not in line:
            continue
        page, verdict = line.split(':', 1)
        if page.strip().lstrip('p').isdigit():
            v[int(page.strip().lstrip('p'))] = verdict.strip()
    return v


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('log')
    ap.add_argument('--tex')
    ap.add_argument('--pdf')
    ap.add_argument('--min-pt', type=float, default=20.0,
                    help='threshold in points (default 20 - the repo standard)')
    ap.add_argument('--verdicts', help='file of "page: verdict" lines')
    args = ap.parse_args()

    if not os.path.isfile(args.log):
        print(f'not a file: {args.log}', file=sys.stderr)
        return 2

    rows = parse_log(args.log, args.min_pt)
    if not rows:
        print(f'CLEAN  no overfull >= {args.min_pt:g}pt')
        return 0

    tex_lines = open(args.tex, encoding='utf-8', errors='replace').read().split('\n') \
        if args.tex and os.path.isfile(args.tex) else None
    pages = pdf_pages(args.pdf) if args.pdf and os.path.isfile(args.pdf) else None
    verdicts = load_verdicts(args.verdicts)

    # State the count FIRST. This list is never truncated.
    print(f'{len(rows)} overfull site(s) >= {args.min_pt:g}pt — '
          f'COMPLETE LIST, not a top-N\n')

    unjudged, code_hits = 0, 0
    for i, r in enumerate(rows, 1):
        page, note, phrase = None, '', None
        if tex_lines:
            chunk, in_code = tex_context(tex_lines, r['start'], r['end'])
            if in_code:
                note = '  [spans a code environment — code does not wrap]'
                code_hits += 1
            for cand in probe_phrases(chunk):
                page = find_page(pages, cand)
                if page:
                    phrase = cand
                    break
            if phrase is None:
                phrase = next(iter(probe_phrases(chunk)), None)

        loc = f'p{page}' if page else 'page=?'
        mark = ''
        if page and page in verdicts:
            mark = f'  verdict: {verdicts[page]}'
        else:
            unjudged += 1
            mark = '  ** NEEDS A VERDICT — OPEN THE PAGE **'
        print(f'{i:3}. {r["pt"]:7.2f}pt  {loc:>7}  tex {r["start"]}--{r["end"]}'
              f'  ({r["kind"]}){note}{mark}')
        if phrase:
            print(f'      "{phrase}…"')

    print()
    if code_hits:
        print(f'{code_hits} site(s) point INSIDE a code environment — '
              f'treat those as defects until proven otherwise.')
    print('An overfull is a POINTER TO A PAGE, not a defect. Magnitude is the badness')
    print('of the line-break, not the size of what shows: a 45pt site can print clean')
    print('and a 30pt one can spill. Open every page above and record a verdict.')
    if unjudged:
        print(f'\n{unjudged} site(s) still need a verdict.')
        return 1
    print('\nEvery site has a recorded verdict.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
