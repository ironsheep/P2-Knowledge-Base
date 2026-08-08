#!/usr/bin/env python3
"""
audit-license-block.py — publish gate for the document license block.

License drift reached 17 documents and shipped publicly for two months because
nothing checked it. Every other class of render defect we have been bitten by
has a gate; this is that gate.

Checks each document source against the canonical text in
engineering/standards/LICENSING-DECISION.md §5:

  REQUIRED  the CC BY-SA 4.0 statement, the Share and Adapt grants, the
            Attribution and ShareAlike terms, the by-sa license URL, and the
            trademark sentence limiting the grant to copyright.
  FORBIDDEN any NC/ND wording, the by-nc-nd URL, and the "contact us for
            commercial use" clause (BY-SA already grants commercial use, so a
            clause inviting people to ask permission for it is contradictory).

Copyright YEARS are intentionally per-document and are never checked.

Usage:
    audit-license-block.py                 # audit every known document source
    audit-license-block.py FILE [FILE...]  # audit specific files
    audit-license-block.py --list          # show the document set

Exit status: 0 = all clean, 1 = at least one violation, 2 = usage error.
"""

import sys
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DECISION = "engineering/standards/LICENSING-DECISION.md"

# --- canonical fragments (LICENSING-DECISION.md §5) -------------------------

# Required of EVERY document, whatever its class (§5.1 and §5.2 both).
REQUIRED = [
    (
        "BY-SA statement",
        re.compile(
            r"licensed under the Creative Commons Attribution[–-]ShareAlike 4\.0 "
            r"International License \(CC BY-SA 4\.0\)",
            re.I,
        ),
    ),
    ("by-sa license URL", re.compile(r"creativecommons\.org/licenses/by-sa/4\.0/", re.I)),
    (
        "trademark scope sentence",
        re.compile(r"grants permissions under copyright only", re.I),
    ),
]

# Required only of the FULL block (§5.1). App notes state the same terms
# compactly (§5.2), which is deliberate — a 5-20 page note does not carry a
# manual's front matter. Keyed off the phrase that opens the bullet grant, so
# a document is held to the form it actually uses.
FULL_BLOCK_MARKER = re.compile(r"^You are free to:", re.M)
FULL_BLOCK_REQUIRED = [
    ("Share grant", re.compile(r"\*\*Share\*\*\s*—\s*copy and redistribute", re.I)),
    (
        "Adapt grant (incl. commercial)",
        re.compile(r"\*\*Adapt\*\*\s*—\s*remix, transform, and build upon.*even commercially", re.I),
    ),
    ("Attribution term", re.compile(r"\*\*Attribution\*\*\s*—", re.I)),
    ("ShareAlike term", re.compile(r"\*\*ShareAlike\*\*\s*—", re.I)),
]

FORBIDDEN = [
    ("NC-ND license name", re.compile(r"BY-NC-ND", re.I)),
    ("NonCommercial term", re.compile(r"NonCommercial", re.I)),
    ("NoDerivatives term", re.compile(r"NoDerivatives", re.I)),
    ("by-nc-nd URL", re.compile(r"creativecommons\.org/licenses/by-nc-nd", re.I)),
    (
        "commercial-permission clause",
        re.compile(r"\*\*Commercial use:\*\*|for separate permission", re.I),
    ),
    # The 2026-08-08 sweep appended the trademark-scope sentence to a holder
    # name that already ended in a period, printing "Parallax Inc.." in sixteen
    # documents. The gate reported all seventeen green: it was checking that
    # required phrases were PRESENT, not that the result read correctly. Cheap
    # to check, and it would have caught a typo bound for every published PDF.
    ("doubled period", re.compile(r"(Inc|LLC)\.\.")),
]


# Manuals the publication roster marks retired (superseded / abandoned). They
# are not in the live consistency set, so holding them to the current canonical
# text would make this gate cry wolf — and a gate that cries wolf gets ignored.
# Keyed by manual folder slug; check PUBLICATION-ROSTER.md before adding.
RETIRED = {
    "p2-smart-pins-tutorial",  # superseded by the I/O & Smart Pins User Guide
}


BACKUP_NAME = re.compile(
    r"(\.bak$|\.backup|[-.]backup[-.]|[-.]pre-[a-z]+-backup|~$|\.orig$)", re.I
)


def is_backup_name(name: str) -> bool:
    """True for anything that looks like a safety copy rather than a master."""
    return bool(BACKUP_NAME.search(name))


def document_sources():
    """Every source that must carry the block — masters only, never renders.

    workspace/ is deliberately excluded: those files are regenerated from
    opus-master by prepare-manual, so auditing them would report the same
    defect twice and invite someone to 'fix' a derived file.

    The master-folder glob is 'opus-master*', not 'opus-master': the Smart Pins
    Tutorial keeps its real master in 'opus-master-green-book/', and a narrower
    glob would silently hide a document from this gate. Hiding a document is
    exactly the failure the gate exists to prevent, so the glob is wide and
    retirement is stated explicitly above.
    """
    found = []
    manuals = REPO / "engineering/document-production/manuals"
    for d in sorted(manuals.glob("*/opus-master*")):
        if not d.is_dir() or d.parent.name in RETIRED:
            continue
        fm = d / "front-matter.md"
        if fm.exists():
            found.append(fm)
            continue
        # Some manuals keep their front matter inside a combined master. Take
        # every candidate rather than the first match, and never a backup: a
        # naive first-match glob here selected
        # COMPLETE-OPUS-MASTER-backup-2025-12-06-pre-backport.md over the real
        # master, which is precisely the adjacent-backup confusion that
        # BACKUP-CONVENTION.md exists to prevent.
        for alt in sorted(d.glob("*.md")):
            if is_backup_name(alt.name):
                continue
            found.append(alt)

    notes = REPO / "engineering/document-production/app-notes"
    for d in sorted(notes.glob("P2AN*/opus-master")):
        for f in sorted(d.glob("P2AN*.md")):
            found.append(f)

    return found


def audit(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:  # unreadable is a failure, not a skip
        return [f"unreadable: {exc}"]

    # Only audit files that actually carry a license block. The second pattern
    # catches the raw-LaTeX heading form (the PNut-Term-TS guide styles its
    # front-matter headings directly); a markdown-only test silently skipped it.
    has_block = re.search(r"^#+\s*Copyright\s*(and|&)\s*License", text, re.I | re.M) or re.search(
        r"\\bfseries\s+Copyright\s+and\s+License", text, re.I
    )
    if not has_block:
        return None

    problems = []
    for label, pat in FORBIDDEN:
        for m in pat.finditer(text):
            line = text[: m.start()].count("\n") + 1
            problems.append(f"line {line}: FORBIDDEN {label} — {m.group(0)!r}")

    checks = list(REQUIRED)
    if FULL_BLOCK_MARKER.search(text):
        checks += FULL_BLOCK_REQUIRED
    for label, pat in checks:
        if not pat.search(text):
            problems.append(f"MISSING {label}")
    return problems


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0

    targets = document_sources() if not argv else [Path(a).resolve() for a in argv]

    if "--list" in argv:
        for p in document_sources():
            print(p.relative_to(REPO))
        return 0

    checked = failed = skipped = 0
    for p in targets:
        result = audit(p)
        rel = p.relative_to(REPO) if p.is_relative_to(REPO) else p
        if result is None:
            skipped += 1
            continue
        checked += 1
        if result:
            failed += 1
            print(f"FAIL  {rel}")
            for problem in result:
                print(f"        {problem}")
        else:
            print(f"ok    {rel}")

    print()
    print(f"{checked} document(s) checked, {failed} failing, {skipped} without a license block.")
    if failed:
        print(f"Canonical text: {DECISION} §5")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
