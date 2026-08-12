#!/usr/bin/env python3
"""
audit-review-scaffolding.py — fail if review-draft scaffolding would ship.

WHAT THIS GUARDS
----------------
A "tool developer review" box is a question put to a named outside tool author
inside a draft that circulates only to those authors (see the ToolReviewBlock
definition in p2kb-platform-content.sty). Every one of them is meant to be
answered and DELETED before the document is published.

There is deliberately NO template switch that hides them, because a hidden box
is one that nobody remembers to answer. What protects the release is this gate.

Publishing one would be worse than an ordinary typo: it puts our private
question to a third-party developer, and our provisional description of THEIR
product, in front of the public.

WHAT IT LOOKS FOR
-----------------
  markdown  ::: {.tool-review ...}   the authored fence
  latex     \\begin{ToolReviewBlock}  the rendered box (also catches boxes
                                     hand-written in raw-LaTeX front matter)

Run it over the opus-master sources AND the generated .tex, because either one
alone can miss a case: a box hand-written in raw LaTeX never appears as a
fence, and a stale .tex never appears in the source.

USAGE
    audit-review-scaffolding.py <file-or-dir> [<file-or-dir> ...]

    exit 0  clean — nothing would ship
    exit 1  scaffolding found (locations printed)
    exit 2  bad invocation

Intended for the release gate. A REVIEW draft is expected to fail this check —
that is the point, so do not run it as a pre-render gate on a draft build.
"""

import sys
from pathlib import Path

MARKERS = (
    ("markdown fence", ":::", ".tool-review"),
    ("rendered box", r"\begin{ToolReviewBlock}", None),
)

SCAN_SUFFIXES = {".md", ".tex", ".latex", ".sty"}


def scan(path: Path):
    """Yield (path, lineno, label, line) for every scaffolding marker found."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"  ! could not read {path}: {exc}", file=sys.stderr)
        return
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, needle, also in MARKERS:
            if needle in line and (also is None or also in line):
                yield path, lineno, label, line.strip()
                break


def collect(target: Path):
    if target.is_file():
        return [target]
    return sorted(p for p in target.rglob("*") if p.is_file() and p.suffix in SCAN_SUFFIXES)


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2

    targets = [Path(a) for a in argv[1:]]
    missing = [t for t in targets if not t.exists()]
    if missing:
        for t in missing:
            print(f"ERROR: no such file or directory: {t}", file=sys.stderr)
        return 2

    files = []
    for t in targets:
        files.extend(collect(t))

    findings = [f for path in files for f in scan(path)]

    if not findings:
        print(f"PASS  no review scaffolding in {len(files)} file(s) scanned")
        return 0

    print(f"FAIL  {len(findings)} review-scaffolding marker(s) — this document "
          f"is NOT releasable\n")
    for path, lineno, label, line in findings:
        print(f"  {path}:{lineno}  ({label})")
        print(f"      {line[:110]}")
    print("\nEach one is an unanswered question to an outside tool author.")
    print("Write the answer into the prose and delete the box, then re-run.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
