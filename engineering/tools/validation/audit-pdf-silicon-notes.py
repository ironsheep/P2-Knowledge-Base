#!/usr/bin/env python3
"""
audit-pdf-silicon-notes.py - a silicon-note index must point at its notes.

WHY THIS EXISTS
    The Assembly Reference v3.1.11 (05:19 build) printed its Silicon Notes index
    with one entry a page early: the WMLONG note sat at the top of p353 and the
    index said 352. The compile log was clean, every release gate was green, and
    the page count was right -- the defect lives in a page NUMBER, which nothing
    compared against the page it names. It was found by hand during release.
    Cause: the note's anchor rode the vertical list ahead of its paragraph, and a
    page break fell between them (fixed in p2kb-platform-content.sty, 2026-10-05).
    A fix is only a fix while something keeps checking it, so this gate reads the
    artifact.

WHAT IT CHECKS
    1  every index line "<topic> — <chapter>; <section> — page N" names a page
       that carries a Rev C chip AND the section it names
    2  the index has one line per silicon note in the source (when --source is
       given): a short index is a dropped note, a long one a duplicate
    3  a source that asks for an index (::: silicon-note-index) whose PDF prints
       no index lines is a FAILURE, never a pass

    A document with no index has nothing to check and passes, saying so.

USAGE
    python3 audit-pdf-silicon-notes.py <rendered.pdf> [--source <md> ...]

EXIT
    0 = clean    1 = violations    2 = bad usage / unreadable PDF
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ENTRY = re.compile(r"• (.+?) — (.+?); (.+?) — page (\d+)")
NOTE_SPAN = re.compile(r"\]\{\.silicon-note\b")
INDEX_DIV = re.compile(r"^:::\s*silicon-note-index\s*$", re.M)


def pages_of(pdf: Path):
    try:
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"ERROR  cannot read {pdf}: {e}")
        sys.exit(2)
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()                     # pdftotext ends every page, the last too, with \f
    return pages


def index_entries(pages):
    entries = []
    for text in pages:
        flat = " ".join(text.split())
        entries += ENTRY.findall(flat)
    return entries


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--source", nargs="*", default=[],
                    help="the markdown the PDF was built from (counts notes, "
                         "and says whether an index was asked for)")
    a = ap.parse_args()
    pdf = Path(a.pdf)
    if not pdf.is_file():
        print(f"ERROR  no such PDF: {pdf}")
        return 2

    src = "".join(Path(s).read_text(encoding="utf-8") for s in a.source)
    asked = bool(INDEX_DIV.search(src)) if a.source else None
    notes = len(NOTE_SPAN.findall(src)) if a.source else None

    pages = pages_of(pdf)
    entries = index_entries(pages)
    bad = []

    if not entries:
        if asked:
            print(f"FAIL   the source asks for a silicon-note index; the PDF prints none "
                  f"({notes} notes in the source)")
            return 1
        print(f"CLEAN  no silicon-note index in this document ({len(pages)} pages read)")
        return 0

    for topic, chapter, section, n in entries:
        n = int(n)
        text = " ".join(pages[n - 1].split()) if 0 < n <= len(pages) else ""
        if "Rev C" not in text or section not in text:
            near = [p for p in (n - 1, n + 1)
                    if 0 < p <= len(pages) and "Rev C" in pages[p - 1]
                    and section in " ".join(pages[p - 1].split())]
            bad.append(f"{topic} — {section}: index says page {n}, "
                       f"which does not carry it"
                       + (f" (it is on page {near[0]})" if near else ""))

    if notes is not None and notes != len(entries):
        bad.append(f"the index lists {len(entries)} notes; the source has {notes}")

    if bad:
        print(f"FAIL   {len(bad)} of {len(entries)} silicon-note index entries:")
        for b in bad:
            print(f"         - {b}")
        return 1
    print(f"CLEAN  all {len(entries)} index entries name the page their note is on"
          + (f"; {notes} notes in the source" if notes is not None else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
