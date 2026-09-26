#!/usr/bin/env python3
"""
audit-pdf-margin-overflow.py - measure text that crosses the right text margin.

WHY THIS EXISTS
    The compile log tells you where TeX was UNHAPPY. It does not tell you where
    ink actually crosses the margin, and the two are not the same set:

      - a 45pt overfull can print entirely clean (TeX disliked the line-break
        badly; nothing protrudes)
      - a 30pt overfull can put a whole identifier into the margin
      - and a line TeX never complained about at all can still stick out

    Worse, the step after "read the log" was ME OPENING PAGES AND JUDGING. That
    judgement moved: the same protruding identifier on the same page was called
    "a cosmetic overhang" in one pass and a defect in the next. Nothing had
    changed except the threshold in my head. A measurement has no threshold in
    anyone's head.

    So this reads the finished PDF, establishes each page's text-block right
    edge from the document's own body text, and reports every span whose ink
    crosses it. It measures what SHOWS, which is the only thing a reader sees.

HOW THE MARGIN IS ESTABLISHED
    Not from the template - from the document. In a justified book the vast
    majority of full lines end exactly at the right margin, so the modal span
    right-edge across the whole document IS the margin, to within rounding. That
    makes the check self-calibrating: it works on any manual in the set without
    being told the geometry, and it cannot drift out of sync with a template
    change.

KNOWN-WIDER ELEMENTS
    Code boxes are drawn wider than the prose measure on purpose, so spans in a
    monospace face are measured against their own modal edge rather than the
    prose one. Anything past THAT is a code line leaving its box - the worst
    case, and called out separately.

WHERE THE 20pt DEFAULT COMES FROM
    Measured, not chosen. Six pages of one manual had already been opened and
    judged by eye - four called defective, two called clean. Running every span
    in that document through this tool put the four defects at 59.4, 28.3, 24.8
    and 24.1pt, the two clean pages at 9.0 and 8.8pt, and NOTHING AT ALL in
    between: the 20-24pt band was empty across 151 crossing spans. The threshold
    sits in that gap, so it reproduces the human verdict on every page where a
    human verdict exists.

    Lower it to see marginal cases (deliberate right-aligned furniture like the
    "continues on next page" marker lands around 17pt, and wide tables put
    several cells in the 10-17pt band). Those are worth a look when a page is
    already suspect; they are not defects on their own evidence.

USAGE
    audit-pdf-margin-overflow.py [--tolerance PT] [--first N] [--last N] <file.pdf>

EXIT STATUS
    0  nothing crosses the margin beyond tolerance
    1  one or more spans cross
    2  usage error (or PyMuPDF unavailable)
"""

import argparse
import collections
import sys

try:
    import pymupdf as fitz
except ImportError:  # older installs expose the same library as `fitz`
    try:
        import fitz
    except ImportError:
        print('PyMuPDF is required: this gate reads the rendered PDF.',
              file=sys.stderr)
        sys.exit(2)

# Rounding bucket for finding the modal edge. Half a point is finer than any
# real margin difference and coarse enough to absorb glyph-metric noise.
BUCKET = 0.5


def spans(doc, first, last):
    for pno in range(first - 1, min(last, doc.page_count)):
        page = doc[pno]
        info = page.get_text('dict')
        for block in info.get('blocks', []):
            for line in block.get('lines', []):
                for sp in line.get('spans', []):
                    txt = sp.get('text', '')
                    if not txt.strip():
                        continue
                    yield pno + 1, sp, txt


def is_mono(span):
    name = (span.get('font') or '').lower()
    return 'mono' in name or 'cour' in name or 'consol' in name


def modal_edge(values):
    if not values:
        return None
    hist = collections.Counter(round(v / BUCKET) * BUCKET for v in values)
    # The margin is the LARGEST heavily-populated edge, not simply the most
    # common one: short lines cluster at many inner positions, but only lines
    # that reach the margin cluster at the margin.
    top = hist.most_common()
    peak = max(c for _, c in top)
    candidates = [v for v, c in top if c >= peak * 0.25]
    return max(candidates) if candidates else None


def bottom_edge(page_bottoms):
    """The text block's bottom: the most common lowest-line position among the
    lower-reaching half of the pages (full pages cluster there; pages that end a
    chapter early do not). modal_edge() does not fit here: it takes the LARGEST
    bucket holding a quarter of the peak, and with one value per page the peak is
    small enough that a single overflowing page becomes the 'edge' it hides."""
    if not page_bottoms:
        return None
    ordered = sorted(page_bottoms)
    upper = ordered[len(ordered) // 2:]
    hist = collections.Counter(round(v) for v in upper)
    best = max(hist.values())
    return min(v for v, c in hist.items() if c == best)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pdf')
    ap.add_argument('--tolerance', type=float, default=20.0,
                    help='points past the edge before reporting (default 20; '
                         'see the calibration note in this file)')
    ap.add_argument('--bottom-margin', type=float, default=54.0,
                    help='bottom margin in points (default 54 = the platform '
                         'geometry\'s 0.75in)')
    ap.add_argument('--first', type=int, default=1)
    ap.add_argument('--last', type=int, default=10 ** 9)
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    try:
        doc = fitz.open(args.pdf)
    except Exception as exc:                      # noqa: BLE001
        print(f'cannot open {args.pdf}: {exc}', file=sys.stderr)
        return 2

    collected = list(spans(doc, args.first, args.last))
    prose_x = [sp['bbox'][2] for _, sp, _ in collected if not is_mono(sp)]
    mono_x = [sp['bbox'][2] for _, sp, _ in collected if is_mono(sp)]

    prose_edge = modal_edge(prose_x)
    mono_edge = modal_edge(mono_x)
    if prose_edge is None:
        print('no text found', file=sys.stderr)
        return 2
    # A code box is wider than the prose measure, never narrower; if the sample
    # says otherwise the document has little code and the prose edge governs.
    if mono_edge is None or mono_edge < prose_edge:
        mono_edge = prose_edge

    hits = []
    for pno, sp, txt in collected:
        edge = mono_edge if is_mono(sp) else prose_edge
        over = sp['bbox'][2] - edge
        if over > args.tolerance:
            hits.append((over, pno, txt.strip(), is_mono(sp)))

    # BOTTOM EDGE (added 2026-09-26). The right-edge check above passed a PDF whose
    # last table ran 37pt off the bottom of the PAPER (P2 Errata v0.2.0 Appendix A:
    # a 12-row non-breaking table the filter did not route to a breaking one). The
    # text block's bottom is measured the same way as its right edge -- the modal
    # lowest text line per page -- and any text line or drawn element (table rules,
    # code-box frames) that ends more than --tolerance below it, or below the paper
    # itself, is reported.
    page_bottoms, low = [], []
    first, last = max(1, args.first), min(doc.page_count, args.last)
    for pno in range(first, last + 1):
        page = doc[pno - 1]
        ys = [ln['bbox'][3] for bl in page.get_text('dict')['blocks']
              for ln in bl.get('lines', [])]
        if ys:
            page_bottoms.append(max(ys))
        for bl in page.get_text('dict')['blocks']:
            for ln in bl.get('lines', []):
                t = ''.join(s['text'] for s in ln['spans']).strip()
                low.append((pno, ln['bbox'][3], 'text', t))
        for dr in page.get_drawings():
            low.append((pno, dr['rect'].y1, 'drawing', ''))
    # The platform geometry fixes the bottom margin (foundation.sty: bottom=0.75in),
    # so the edge is KNOWN, not estimated: a statistical estimate from one value per
    # page is fragile (a manual of short pages put it 85pt too high). The cover
    # (page 1) is its own layout and is not measured.
    measured = bottom_edge(page_bottoms)
    paper = doc[0].rect.height
    body_bottom = paper - args.bottom_margin
    bottom_hits = []
    if True:
        for pno, y1, kind, t in low:
            if pno == 1:
                continue
            if y1 > paper or y1 - body_bottom > args.tolerance:
                bottom_hits.append((y1 - body_bottom, pno, kind, t, y1 > paper))
    worst = {}
    for over, pno, kind, t, off in bottom_hits:       # one line per page, the worst
        if pno not in worst or over > worst[pno][0]:
            worst[pno] = (over, kind, t, off)

    print(f'text-block right edge: prose {prose_edge:.1f}pt, '
          f'code {mono_edge:.1f}pt   (tolerance {args.tolerance:g}pt)')
    print(f'text-block bottom edge: {body_bottom:.1f}pt from the platform geometry '
          f'(measured {measured if measured is not None else "n/a"}pt; '
          f'paper {paper:.1f}pt; cover page not measured)')
    if worst:
        print(f'\n{len(worst)} page(s) with content below the text block — '
              f'COMPLETE LIST, not a top-N\n')
        for pno in sorted(worst):
            over, kind, t, off = worst[pno]
            where = 'OFF THE PAPER' if off else 'below the text block'
            print(f'  p{pno:<4} +{over:6.1f}pt  [{kind}]  {where}  {t[:60]}')
    if not hits and not worst:
        print(f'CLEAN  nothing crosses the margin '
              f'({doc.page_count} pages measured)')
        return 0
    if not hits:
        return 1

    hits.sort(key=lambda h: -h[0])
    print(f'\n{len(hits)} span(s) cross the right margin — '
          f'COMPLETE LIST, not a top-N\n')
    for over, pno, txt, mono in hits:
        kind = 'CODE' if mono else 'prose'
        print(f'  p{pno:<4} +{over:6.1f}pt  [{kind}]  {txt[:70]}')
    if any(m for _, _, _, m in hits):
        print('\nCODE spans past the code-box edge are the worst case: a code '
              'line is leaving its box and may be CUT at the paper edge.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
