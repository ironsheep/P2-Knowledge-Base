#!/usr/bin/env python3
"""
audit-extraction-digit-density.py — did the extraction actually recover the numbers?

WHY THIS EXISTS  (F-250, 2026-08-24)
    The #64000 P2 Eval Board Rev C Guide was ingested in 2025 with `pdftotext`.
    The tool exited 0. Its output was fluent English. Its dashboard row read
    `100% (stated)` for eleven months. And every single numeral was gone --
    that PDF's body font does not map digits, so `pdftotext` silently deleted
    them. Shipped lines read:

        "The Propeller has cores, KB of hub RAM, and Smart I/O pins"

    8 / 512 / 64 are simply absent. "Buffered LEDs on top eight I/O pins"
    survived only because "eight" is spelled out.

    Two consequences, both bad:
      * the LED pin map sat as `TBD` in `hardware/p2-eval-board.yaml` for months
        while the answer was in the repo -- no grep for `P56` can hit a document
        that contains no digits (F-248);
      * the extraction audit and the cross-source analysis both listed "LED pins"
        as a GAP, so a tooling failure was mistaken for the source being silent.

    That last inversion is the whole point. A mangled extraction looks EXACTLY
    like a fact that was never there. Nothing in a seven-pass ingestion looked at
    the artifact and asked whether the numbers came through, so nothing could
    tell the two apart.

    A hardware document whose extraction is nearly digit-free has FAILED, not
    been read.

WHAT IT MEASURES
    Per text artifact: the share of NON-BLANK lines that carry at least one
    digit. Crude on purpose -- it needs no knowledge of the document.

    Measured 2026-08-24 across twelve board/hardware sources:

        p2-eval-board           10%   <-- broken (digit-free body font)
        p2-hardware-manual      29%
        p2-universal-motor-drv  30%
        p2-datasheet            31%
        parallax-wx-wifi        32%
        propplug-rev-e          36%
        p2-microSD-addon        40%
        p2-eval-add-on-boards   44%
        p2-wx-adapter           45%
        hyperRam-n-hyperFlash   48%
        P2-RTC-Add-on           57%
        P2-HD-Audio-Add-on      58%

    One outlier, unmistakable. Hence the default floor of 20% for a hardware
    source -- comfortably under the observed band, comfortably over the failure.

WHAT IT IS NOT
    A SMOKE ALARM, NEVER A CERTIFICATE.

    It detects TOTAL numeral loss. It cannot detect PARTIAL loss -- a table whose
    digits came through while a figure's did not, a page that OCR'd badly, a
    single transposed value. Passing this check is NOT evidence that a source is
    completely extracted, and must never be reported as one. The eleven peers
    above are not certified by their scores; they are merely not obviously broken.

    Prose is allowed to be digit-light. A narrative chapter, a style guide, a
    voice guide will legitimately score low. That is why the failing verdict is
    scoped to HARDWARE/spec sources, where numbers ARE the content, and why the
    check names the artifact rather than the source folder: the disposition is a
    human's.

USAGE
    audit-extraction-digit-density.py <path> [<path> ...]     # dirs or files
    audit-extraction-digit-density.py --all                   # every source folder
    audit-extraction-digit-density.py --floor 25 <path>
    audit-extraction-digit-density.py --json <path>

EXIT
    0  every measured artifact is at or above the floor
    1  at least one artifact is below the floor, OR produced no substantive lines
       at all -- the extraction is suspect and must be repaired, not gapped
    2  NOTHING WAS MEASURED -- no recognised extraction artifact under the given
       path. A tooling failure, never a pass: the path is wrong, or the thing this
       gate was pointed at does not exist. An unrun check must not report success.
       (Same convention as audit-constant-fidelity.py.)
"""

import argparse
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SOURCES = os.path.join(REPO, "engineering", "ingestion", "sources")

DEFAULT_FLOOR = 20.0

# Raw/curated extraction artifacts. `archive/` holds capture that has ALREADY been
# judged lossy and retired -- measuring it would report a known failure forever.
TEXT_SUFFIXES = ("-text.txt", "-narrative.txt", "-ocr-text.txt")
CURATED_PREFIXES = ("complete-",)
CURATED_SUFFIXES = ("-reference.md",)
SKIP_DIR_PARTS = {"archive", "assets", ".git", "__pycache__"}

# A line needs some substance before its digit-lessness means anything: page
# furniture, single words and table rules are noise in both directions.
MIN_LINE_CHARS = 12

# EXEMPTIONS — artifacts that are NOT extractions of a document.
#
# Each of these is a hand-written *description of a source folder* produced by the
# 2025-09-02 narrative-generation pass ("Created descriptive narrative" in
# `engineering/ingestion/NARRATIVE-GENERATION-COMPLETE.md`). They describe what a
# source contains; they never carried the source's numbers, so a low score says
# nothing about extraction health. Exempting them is what keeps this check from
# becoming four permanent false alarms that a reader learns to scroll past.
#
# Each entry names WHY and WHEN it was checked. Re-audit with --no-exempt.
# Do NOT add an entry because a real extraction scores low. That is the finding.
EXEMPT = {
    "engineering/ingestion/sources/marketing-materials/marketing-materials-narrative.txt":
        "hand-written folder description, not an extraction (verified 2026-08-24)",
    "engineering/ingestion/sources/p2-instructions-csv/p2-instructions-csv-narrative.txt":
        "hand-written description of a CSV's columns; the CSV itself is the data "
        "(verified 2026-08-24)",
    "engineering/ingestion/sources/p2docs-github-io/p2docs-github-io-narrative.txt":
        "hand-written description of a website, not an extraction (verified 2026-08-24)",
    "engineering/ingestion/sources/rom-booter/rom-booter-narrative.txt":
        "hand-written description of the .lst listings; the .lst files are the data "
        "(verified 2026-08-24)",
}


def measure(path):
    """Return (substantive_lines, with_digit, pct, err) for one text artifact.

    pct is None when the artifact has NO substantive lines at all -- which is a
    FAILED extraction, not an unscorable one. main() treats it as such.
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        return None, None, None, str(exc)
    nonblank = [l for l in lines if len(l.strip()) >= MIN_LINE_CHARS]
    if not nonblank:
        return 0, 0, None, None
    digits = sum(1 for l in nonblank if re.search(r"\d", l))
    return len(nonblank), digits, 100.0 * digits / len(nonblank), None


def is_artifact(name):
    if name.endswith(TEXT_SUFFIXES):
        return True
    if name.endswith(CURATED_SUFFIXES) and name.startswith(CURATED_PREFIXES):
        return True
    return False


def collect(target):
    """Yield artifact paths under a directory, or the file itself."""
    if os.path.isfile(target):
        yield target
        return
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_PARTS]
        for f in sorted(files):
            if is_artifact(f):
                yield os.path.join(root, f)


def main():
    ap = argparse.ArgumentParser(
        description="Flag an extraction that lost its numerals (F-250).")
    ap.add_argument("paths", nargs="*", help="source folders or text artifacts")
    ap.add_argument("--all", action="store_true",
                    help="measure every folder under engineering/ingestion/sources/")
    ap.add_argument("--floor", type=float, default=DEFAULT_FLOOR,
                    help=f"minimum %% of substantive lines carrying a digit "
                         f"(default {DEFAULT_FLOOR:g})")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--no-exempt", action="store_true",
                    help="measure the exempted descriptive narratives too (re-audit the list)")
    args = ap.parse_args()

    targets = list(args.paths)
    if args.all:
        targets += [os.path.join(SOURCES, d) for d in sorted(os.listdir(SOURCES))
                    if os.path.isdir(os.path.join(SOURCES, d))]
    if not targets:
        ap.error("give a path, or --all")

    rows, failures, unreadable, exempted = [], [], [], []
    for t in targets:
        if not os.path.exists(t):
            unreadable.append((t, "no such path"))
            continue
        for art in collect(t):
            rel = os.path.relpath(art, REPO)
            if rel in EXEMPT and not args.no_exempt:
                exempted.append((rel, EXEMPT[rel]))
                continue
            nb, dg, pct, err = measure(art)
            if err:
                unreadable.append((art, err))
                continue
            rows.append((rel, nb, dg, pct))
            # pct is None => the artifact has no substantive lines at all. That is
            # the most complete extraction failure there is, so it FAILS. Scoring
            # it "n/a" and passing would be the exact hole this gate exists to
            # close: an extraction that produced nothing, reported as clean.
            if pct is None or pct < args.floor:
                failures.append((rel, nb, dg, pct))

    if args.json:
        print(json.dumps({
            "floor": args.floor,
            "artifacts": [{"path": r, "substantive_lines": nb,
                           "lines_with_digit": dg, "pct": pct} for r, nb, dg, pct in rows],
            "below_floor": [r for r, _, _, _ in failures],
            "exempt": [{"path": p, "reason": r} for p, r in exempted],
            "unreadable": [{"path": p, "error": e} for p, e in unreadable],
        }, indent=2))
        if not rows:
            return 2          # nothing audited is never a pass — see below
        return 1 if failures else 0

    if not rows:
        # "Nothing audited" is NEVER a pass. Exit 2 = tooling failure, matching
        # audit-constant-fidelity.py's convention. A gate pointed at the wrong
        # path, or at artifacts whose names this tool does not recognise, must
        # not hand back a green -- that is an unrun check reporting success.
        print("NOTHING MEASURED — no extraction artifacts found under the given path(s).")
        print("  (looked for *-text.txt, *-narrative.txt, *-ocr-text.txt, complete-*-reference.md)")
        print("  This is a TOOLING FAILURE, not a pass: either the path is wrong, or the")
        print("  extraction this gate was meant to check does not exist under it.")
        return 2

    width = max(len(r) for r, _, _, _ in rows)
    print(f"{'artifact'.ljust(width)}   lines  w/digit   density")
    for rel, nb, dg, pct in rows:
        shown = "  EMPTY " if pct is None else f"{pct:6.1f}% "
        mark = "" if (pct is not None and pct >= args.floor) else "  <-- BELOW FLOOR"
        print(f"{rel.ljust(width)}  {nb:6d}  {dg:7d}  {shown}{mark}")

    for p, e in unreadable:
        print(f"UNREADABLE  {p}: {e}")
    for p, r in exempted:
        print(f"EXEMPT      {p}  —  {r}")

    print()
    print(f"floor: {args.floor:g}% of substantive lines (>= {MIN_LINE_CHARS} chars) must carry a digit")
    if not failures:
        print(f"CLEAN  {len(rows)} artifact(s) at or above the floor.")
        print("       NOT a completeness certificate — this catches TOTAL numeral loss only,")
        print("       never partial. Say so wherever you record the result.")
        return 0

    print(f"\nBELOW FLOOR ({len(failures)}) — treat these extractions as FAILED, not as sources that are silent:")
    for rel, nb, dg, pct in failures:
        if pct is None:
            print(f"  - {rel}: NO substantive lines at all — the extraction produced nothing")
        else:
            print(f"  - {rel}: {dg}/{nb} substantive lines carry a digit ({pct:.1f}%)")
    print("""
WHAT TO DO — do not gap it, repair it. Exhaust the ladder (SOURCE-REPAIR-ORDER.md §4):
    pdf-ocr --force-ocr <in.pdf> <out.pdf>   then re-extract from the OCR'd PDF
    camelot lattice / stream                 for a ruled table
    pdf-layout                               for column/indent-sensitive pages
    a DOCX edition if one is staged          it carries table structure a PDF text layer cannot
    render the page and READ it              figures carry pin maps no text layer holds
Then triple-validate: OCR text ∩ the original text layer ∩ the rendered page.
A source can be present, ingested and dashboard-green and still be unable to carry the fact
you are citing. Citing into it is not grounding.""")
    return 1


if __name__ == "__main__":
    sys.exit(main())
