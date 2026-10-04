#!/usr/bin/env python3
"""
audit-request-metadata-latex.py - request.json metadata must be safe to drop raw into LaTeX.

WHY THIS EXISTS
    2026-10-04. The P2 Interpreters & Emulators Guide adopted metadata
    single-sourcing: its template now binds \\renewcommand{\\DocTitle}{$title$}
    and the cover prints \\DocTitle. The Forge passes request.json metadata to
    pandoc as --variable, and pandoc inserts a variable RAW -- it does not
    escape it the way it escapes document metadata. The title
    "P2 Interpreters & Emulators Guide" therefore reached xelatex as a bare &,
    and the production build failed: "! Misplaced alignment tab character &."
    at \\DocTitle. The I/O & Smart Pins guide had met the same thing and writes
    its title "P2 I/O \\\\& Smart Pins User Guide" in request.json; nothing
    carried that rule to the next document. Every prepare gate read the
    markdown; none read the directive, so a full Forge build was spent finding it.

    This gate runs at PREPARE, before the render, where the fix is free.

WHAT IT CHECKS
    Every string value under documents[*].metadata in the slug's request.json.
    A LaTeX special character  & % $ # _ { } ~ ^  not preceded by a backslash is
    a finding. Write it escaped in the JSON source ("\\\\&" in JSON = \\& in
    LaTeX). hyperref turns \\& back into & for the PDF Title, so the PDF
    properties still read correctly (I/O & Smart Pins, verified on its PDF).

EXIT
    0  clean      1  findings      2  could not run (no request.json, bad JSON)

    --negative-control runs the checker on a known-bad value and exits 0 only if
    it is caught: a gate that cannot fail has been run, not verified.
"""
import argparse
import json
import re
import sys
from pathlib import Path

SPECIALS = re.compile(r'(?<!\\)[&%$#_{}~^]')


def repo_root() -> Path:
    for p in Path(__file__).resolve().parents:
        if (p / ".git").exists() and (p / "engineering").is_dir():
            return p
    sys.exit("ERROR: could not locate the repository root.")


def findings_for(metadata: dict, where: str):
    out = []
    for key, val in metadata.items():
        if not isinstance(val, str):
            continue
        for m in SPECIALS.finditer(val):
            out.append(f"{where} metadata.{key}: unescaped '{m.group(0)}' at col "
                       f"{m.start() + 1} in {val!r} -- write it as \\\\{m.group(0)} in the JSON")
    return out


def audit(req: Path):
    data = json.loads(req.read_text(encoding="utf-8"))
    found = []
    for i, doc in enumerate(data.get("documents", [])):
        found += findings_for(doc.get("metadata", {}) or {}, f"documents[{i}]")
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", help="document slug (workspace/<slug>/request.json)")
    ap.add_argument("--negative-control", action="store_true")
    args = ap.parse_args()

    if args.negative_control:
        bad = findings_for({"title": "A & B"}, "control")
        good = findings_for({"title": r"A \& B", "license": "CC BY-SA 4.0"}, "control")
        if bad and not good:
            print("NEGATIVE CONTROL: PASS (a bare & is caught; an escaped one is not)")
            return 0
        print("NEGATIVE CONTROL: FAIL")
        return 1

    if not args.slug:
        ap.error("--slug is required")
    req = repo_root() / "engineering/document-production/workspace" / args.slug / "request.json"
    if not req.is_file():
        print(f"ERROR: {req} not found")
        return 2
    try:
        found = audit(req)
    except json.JSONDecodeError as e:
        print(f"ERROR: {req}: {e}")
        return 2
    if found:
        print(f"FINDINGS ({len(found)}) -- pandoc inserts --variable values raw into LaTeX:")
        for f in found:
            print(f"  {f}")
        return 1
    print(f"CLEAN  {args.slug}: request.json metadata is LaTeX-safe")
    return 0


if __name__ == "__main__":
    sys.exit(main())
