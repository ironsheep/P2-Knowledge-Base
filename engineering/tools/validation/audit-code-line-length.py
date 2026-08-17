#!/usr/bin/env python3
"""
audit-code-line-length.py - flag code lines that exceed a manual's column budget K.

WHY THIS EXISTS
    Code boxes in the P2 manuals do NOT wrap. A typeset wrap cannot break a comment
    and re-indent it, nor insert the language's line-continuation for a split
    statement, so an auto-wrap renders wrong-looking code AND hides the problem.
    Therefore an over-long code line is an AUTHORSHIP defect: it must be shortened
    in the source (break the comment + re-indent, or continue the statement). This
    tool detects those lines so the author can fix them.

THE BUDGET K
    K is the widest code line the box prints - it is font/box specific, so it is
    measured per code-box style (see the calibration ruler in the P2 Layout Torture
    Test, case 2.2). Each manual records its K in creation-guide.md as a tagged line:

        **Max code columns (K): 76**

    This tool reads that line (or takes --budget) and flags any source code line
    whose display width exceeds K.

USAGE
    audit-code-line-length.py [options] <markdown-file> [<markdown-file> ...]

OPTIONS
    --budget N           Override K (else read from the manual's config).
    --creation-guide P   Config file to read K from. If omitted, it is
                         auto-derived: the nearest creation-guide.md OR
                         MANUAL-DESCRIPTOR.md at, or above, each markdown file's
                         directory — covering both the manuals/<name>/opus-master/
                         layout (K in creation-guide.md as the tagged line above)
                         and app-notes/<id>/opus-master/ (K in that note's
                         MANUAL-DESCRIPTOR.md as "code_line_budget_K: 76", since
                         app notes share one class-wide creation guide).
    --tabstop N          Tab width in columns for display-width counting
                         (default 8 - the fancyvrb Verbatim default the colored
                         code boxes render with).
    --quiet              Print only violations and the summary (suppress per-file OK).

SCOPE
    Every fenced ``` (or ~~~) code block whose info string is empty or a code
    language (pasm2/spin2/cordic/multicog/antipattern/iosp/...) - i.e. anything that
    renders in a code box. Raw passthrough fences (```{=latex}, ```{=html}) are
    skipped: they are LaTeX/HTML, not code in a box.

EXIT STATUS
    0  no code line exceeds K  (also: an EXEMPT instrument doc — over-budget lines
       reported for information but not gated; see --exempt / "Code-line gate: EXEMPT")
    1  one or more lines exceed K (so this can gate prepare-manual / a release)
    2  usage / configuration error (e.g. no budget found)
"""

import argparse
import os
import re
import sys

CODE_BUDGET_RE = re.compile(r'Max\s+code\s+columns\s*\(K\)\s*:\s*(\d+)', re.IGNORECASE)
# An INSTRUMENT doc (e.g. the layout torture test) deliberately carries
# over-budget code lines as fixtures, so its creation guide opts OUT of the gate
# with a tagged line: "Code-line gate: EXEMPT (instrument)". Over-budget lines are
# then reported for information but do NOT fail the run (exit stays 0).
CODE_GATE_EXEMPT_RE = re.compile(r'Code[-\s]line\s+gate\s*:\s*EXEMPT', re.IGNORECASE)

# PER-LINE WAIVER, narrow on purpose.
#
# A window-CREATE line carries every config keyword the window needs, and those are
# not divisible: TERM's COLOR and SPECTRO's SAMPLES/DEPTH/RANGE/RATE are accepted
# ONLY by the Configure phase, so they cannot move to a later feed the way channel
# defs and text can. In a manual about DEBUG windows a fully-configured create line
# simply does not fit 76 columns — that is a property of the subject, not sloppiness.
#
# So a line may carry a waiver naming its MEASURED width:
#
#     ' {K-waiver: 81 cols, create line, inside the 86-col box}
#
# The waiver is honored only if the line is at or under HARD_CEILING. 76 stays the
# default for all ordinary code; 86 is where text begins spilling past the code box
# into the margin (calibrated 2026-08-17: a 97-col line produced a 57.66pt overfull
# and an 88-col line 12.85pt, i.e. ~5.24pt per column past 86). Beyond 86 no waiver
# applies, because the defect is then visible on the page.
#
# The waiver lives in the SOURCE, next to the line it excuses, and must state the
# width — so every exception is auditable and none can hide in a guide.
WAIVER_RE = re.compile(r"\{K-waiver:\s*(\d+)\s*cols?\b", re.IGNORECASE)
HARD_CEILING = 86
# App notes carry no creation-guide.md — the app-note doc class shares one
# (APP-NOTE-CREATION-GUIDE.md) and each note records its own K in its
# MANUAL-DESCRIPTOR.md front matter as "code_line_budget_K: 76".
DESCRIPTOR_BUDGET_RE = re.compile(r'^\s*code_line_budget_K\s*:\s*(\d+)', re.MULTILINE)
# Config files that can carry K, in resolution order within a directory.
BUDGET_CONFIG_NAMES = ('creation-guide.md', 'MANUAL-DESCRIPTOR.md')
FENCE_RE = re.compile(r'^(\s*)(`{3,}|~{3,})(.*)$')


def find_creation_guide(md_path):
    """Walk up from the markdown file's directory looking for a config that
    carries K — creation-guide.md (manuals) or MANUAL-DESCRIPTOR.md (app notes).
    Within a directory, creation-guide.md wins."""
    d = os.path.dirname(os.path.abspath(md_path))
    prev = None
    while d and d != prev:
        for name in BUDGET_CONFIG_NAMES:
            candidate = os.path.join(d, name)
            if os.path.isfile(candidate):
                return candidate
        prev, d = d, os.path.dirname(d)
    return None


def read_budget(creation_guide_path):
    """Extract K from the config's tagged line, or None if absent. Accepts both
    the creation-guide form ("Max code columns (K): 76") and the app-note
    descriptor form ("code_line_budget_K: 76")."""
    try:
        with open(creation_guide_path, encoding='utf-8') as fh:
            text = fh.read()
    except OSError:
        return None
    m = CODE_BUDGET_RE.search(text) or DESCRIPTOR_BUDGET_RE.search(text)
    return int(m.group(1)) if m else None


def read_exempt(creation_guide_path):
    """True if the creation guide declares the code-line gate EXEMPT — an instrument
    doc that deliberately carries over-budget lines as fixtures (e.g. the layout
    torture test's case-2.2 column ruler). Over-budget lines are then reported but
    do not fail the gate."""
    if not creation_guide_path:
        return False
    try:
        with open(creation_guide_path, encoding='utf-8') as fh:
            text = fh.read()
    except OSError:
        return False
    return bool(CODE_GATE_EXEMPT_RE.search(text))


def display_width(line, tabstop):
    """Display columns occupied by a line, expanding tabs to the tab stop."""
    w = 0
    for ch in line:
        if ch == '\t':
            w += tabstop - (w % tabstop)
        else:
            w += 1
    return w


def is_code_fence(info):
    """True if a fence info string denotes a code box (not a raw passthrough).

    ONLY ```{=format} is a raw passthrough (```{=latex}, ```{=html}) — its content
    is handed to the writer verbatim and never lands in a code box, so line width
    is not this gate's business there.

    Pandoc ATTRIBUTE syntax — ```{.spin2 caption="foo.spin2"} — IS a code box. It
    is the captioned form, which is exactly the form paired with an examples-library
    file under the byte-identity rule.

    This function used to skip every info string starting with '{', which silently
    excluded all 56 captioned blocks across the fleet (Debug Window 34, IOSP 15,
    Getting Started 4, deSilva 3). That is how F-281 shipped: two Debug Window pages
    lost a whole SCOPE/LOGIC channel to an over-wide line while this gate reported
    the manual clean, because both offending lines sat in captioned fences. A gate
    that silently passes is worse than no gate — nobody goes looking.
    """
    info = info.strip()
    if info.startswith('{='):
        return False
    return True


def scan_markdown(md_path, budget, tabstop):
    """Return a list of (lineno, cols, text) for code lines over budget."""
    with open(md_path, encoding='utf-8') as fh:
        lines = fh.readlines()

    violations = []
    fence = None  # (marker, indent_len) when inside a code fence we audit
    in_raw = False  # inside a fence we skip (raw passthrough)

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip('\n')
        m = FENCE_RE.match(line)
        if fence is None and not in_raw:
            # not in any fence: a fence line opens one
            if m:
                marker, info = m.group(2), m.group(3)
                if is_code_fence(info):
                    fence = (marker[0], len(marker))
                else:
                    in_raw = (marker[0], len(marker))
            continue
        # inside a fence: a closing fence is same char, >= length, no info
        if m:
            marker, info = m.group(2), m.group(3)
            active = fence if fence is not None else in_raw
            if marker[0] == active[0] and len(marker) >= active[1] and info.strip() == '':
                fence = None
                in_raw = False
                continue
        # a content line inside a fence
        if fence is not None:
            cols = display_width(line, tabstop)
            if cols > budget:
                # Honor a per-line waiver only if it names THIS line's measured width
                # and the line stays inside the box (see WAIVER_RE / HARD_CEILING).
                # A waiver whose number has drifted from reality is no waiver — the
                # point is that the exception states, and keeps stating, the truth.
                # WHERE THE WAIVER LIVES, and why it is not in the code.
                #
                # First attempt put it in the code block as a Spin2 comment. It
                # RENDERED — "' {K-waiver: 81 cols...}" printed in the manual on p29,
                # leaking build metadata into reader-facing output. A manual is the
                # human face; production plumbing must never print.
                #
                # So the waiver is an HTML comment placed ABOVE the fence, which pandoc
                # drops (verified on the Forge: the text is absent from the PDF while
                # the code still renders). It stays in the source next to the block it
                # excuses, so it remains auditable, and the examples-library file stays
                # pure code — which byte-identity requires.
                #
                # Search back past the fence for it; also accept it inline/preceding for
                # non-rendered files.
                w = WAIVER_RE.search(line)
                if w is None:
                    for back in range(idx - 2, max(-1, idx - 12), -1):
                        if back < 0 or back >= len(lines):
                            continue
                        w = WAIVER_RE.search(lines[back])
                        if w:
                            break
                if w and int(w.group(1)) == cols and cols <= HARD_CEILING:
                    continue
                violations.append((idx, cols, line))
    return violations


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='Flag code lines exceeding a manual\'s column budget K.')
    ap.add_argument('files', nargs='+', help='manual markdown source file(s)')
    ap.add_argument('--budget', type=int, default=None,
                    help='override K (else read from the creation guide)')
    ap.add_argument('--creation-guide', default=None,
                    help='creation-guide.md to read K from (else auto-derived)')
    ap.add_argument('--tabstop', type=int, default=8,
                    help='tab width in columns (default 8)')
    ap.add_argument('--quiet', action='store_true',
                    help='print only violations and the summary')
    ap.add_argument('--exempt', action='store_true',
                    help='treat over-budget lines as informational, not a gate '
                         'failure — for INSTRUMENT docs that carry deliberate '
                         'over-budget fixtures. Auto-detected from the creation '
                         'guide\'s "Code-line gate: EXEMPT" line.')
    args = ap.parse_args(argv)

    total_violations = 0
    files_with_violations = 0
    exempt_lines = 0
    exempt_files = 0

    for md in args.files:
        if not os.path.isfile(md):
            print(f'error: not a file: {md}', file=sys.stderr)
            return 2

        budget = args.budget
        source = 'budget flag'
        cg = args.creation_guide
        if budget is None:
            cg = args.creation_guide or find_creation_guide(md)
            if not cg:
                print(f'error: no creation-guide.md or MANUAL-DESCRIPTOR.md found '
                      f'for {md} and no --budget given', file=sys.stderr)
                return 2
            budget = read_budget(cg)
            if budget is None:
                print(f'error: no "Max code columns (K): N" / "code_line_budget_K: N" '
                      f'line in {cg}', file=sys.stderr)
                return 2
            source = cg

        # An instrument doc opts out of the GATE (CLI flag or creation-guide tag):
        # over-budget lines are still reported, but they do not fail the run.
        exempt = args.exempt or read_exempt(cg)

        violations = scan_markdown(md, budget, args.tabstop)
        if violations and exempt:
            exempt_files += 1
            exempt_lines += len(violations)
            print(f'\n{md}  (budget K={budget}, from {source}) — EXEMPT (instrument):')
            for lineno, cols, text in violations:
                shown = text if len(text) <= 90 else text[:87] + '...'
                print(f'  {md}:{lineno}: {cols} cols (>{budget})  | {shown}')
            print(f'  ^ {len(violations)} over-budget line(s) are declared instrument '
                  f'fixtures ("Code-line gate: EXEMPT") — reported, NOT gated.')
        elif violations:
            files_with_violations += 1
            total_violations += len(violations)
            print(f'\n{md}  (budget K={budget}, from {source}):')
            for lineno, cols, text in violations:
                shown = text if len(text) <= 90 else text[:87] + '...'
                print(f'  {md}:{lineno}: {cols} cols (>{budget})  | {shown}')
        elif not args.quiet:
            print(f'{md}: OK (no code line over K={budget})')

    if total_violations:
        print(f'\nFAIL: {total_violations} code line(s) over budget in '
              f'{files_with_violations} file(s). Shorten them in source: break the '
              f'comment and re-indent, or continue the statement.')
        return 1
    if exempt_lines and not args.quiet:
        print(f'\nEXEMPT: {exempt_lines} over-budget line(s) in {exempt_files} '
              f'instrument file(s) reported for information; gate not triggered (exit 0).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
