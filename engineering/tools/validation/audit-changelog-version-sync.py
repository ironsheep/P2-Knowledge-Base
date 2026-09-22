#!/usr/bin/env python3
"""
audit-changelog-version-sync.py - the version on the cover must have a changelog entry.

WHY THIS EXISTS
    2026-09-22. Three manuals released in one evening, and ALL THREE reached the
    promote step with a changelog that did not describe the version printed on
    their own cover:

        Assembly     request.json 3.1.10, CHANGELOG top entry v3.1.9, and that
                     entry carried none of the twelve corrections in the batch
                     that caused the bump.
        deSilva      request.json 3.0.8, CHANGELOG top entry v3.0.7 - the already
                     tagged release. No v3.0.8 entry existed at all.
        Single-Step  request.json bumped to 1.0.1 with no entry, caught only
                     because the two before it had made the pattern obvious.

    The mechanism is the same every time: a render needs a version, request.json
    is where the version lives, so it gets bumped -- and the changelog is a
    different file that nothing requires you to touch. The two drift silently
    and agree again only by accident.

    NOTHING ELSE CATCHES IT IN TIME. `audit-changelog` reads the top entry well,
    but release-manual runs it at PROMOTE -- after the Forge render is already
    spent. Every other prepare-phase gate reads the markdown body and has no
    opinion about the directive. So the defect was free to travel all the way to
    the last step before publication, three times in one evening, and each time
    the fix was mine to make under time pressure at exactly the wrong moment.

    This gate runs at PREPARE, before the render, where the fix is free.

WHAT IT CHECKS
    request.json  documents[*].metadata.version
    CHANGELOG.md  the FIRST `## v<X.Y.Z>` heading

    Both normalised to three-part semver ("1.0" -> "1.0.0"), then compared. A
    mismatch, a missing heading, or a missing version is a finding.

    SECOND CHECK -- the SHAPE of metadata.version. It must be a bare number:
    "1.1.3", never "Version 1.1.3" and never "v1.1.0". The cover supplies the
    word "Version" itself, so a decorated value renders "Version Version 1.1.3".
    Found on the first fleet sweep this gate ever ran (2026-09-22): TWO of the
    ten manuals carried a decorated value. Both were invisible because neither
    had adopted metadata single-sourcing yet -- their covers come from hardcoded
    markdown and the value only reached the PDF properties. It is a landmine, not
    a defect, until the day that manual adopts single-sourcing, which the
    standing rule requires at its next release. That is precisely the shape worth
    catching while it is still free.

WHAT IT DELIBERATELY DOES NOT CHECK
    Whether the entry is any GOOD -- whether it is complete, correctly voiced,
    or supported by the diff. That is `audit-changelog`'s job and it is a real
    one; this gate is the cheap structural precondition underneath it. An entry
    can satisfy this gate and still be unfit to publish. Passing here is not a
    statement about the entry's contents.

USAGE
    audit-changelog-version-sync.py [--quiet] --slug <manual-slug>
    audit-changelog-version-sync.py --negative-control

EXIT STATUS
    0  the cover version has a matching changelog entry
    1  they disagree, or one of them is missing (gate failure)
    2  usage error, or an artifact could not be read/parsed

FIX
    Add (or re-head) the top CHANGELOG.md entry in opus-master so it names the
    version request.json is about to render. If the version being replaced was
    never tagged, RENAME that entry rather than adding a second one --
    never-shipped versions are never mentioned (changelog-voicing.md 1.7).
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DOCPROD = REPO / "engineering" / "document-production"

# `## v3.1.10 (2026-09-22)`, `## [v1.2.0] (...)`, `## v1.0.0 (2026-09-10): Initial ...`
HEADING = re.compile(r"^##\s+\[?v(\d+(?:\.\d+)*)\]?\b")

# A metadata.version the cover can print verbatim behind the word "Version".
BARE = re.compile(r"^\d+(?:\.\d+)*$")

# What a decorated value looks like, so the comparison can still be made.
DECOR = re.compile(r"^\s*(?:version\s+)?v?", re.IGNORECASE)


def normalise(v: str) -> str:
    """Three-part semver, tolerating decoration so a shape defect does not also
    masquerade as a changelog mismatch. '1.0' -> '1.0.0'."""
    parts = DECOR.sub("", v.strip()).split(".")
    while len(parts) < 3:
        parts.append("0")
    return ".".join(parts)


def request_versions(path: Path):
    """Every documents[*].metadata.version in a request.json, in order."""
    data = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for doc in data.get("documents", []):
        v = (doc.get("metadata") or {}).get("version")
        if v is not None:
            out.append(str(v))
    return out


def top_changelog_version(path: Path):
    """The first `## v<X.Y.Z>` heading, or None."""
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = HEADING.match(line)
        if m:
            return m.group(1)
    return None


def check(slug: str, quiet: bool) -> int:
    req = DOCPROD / "workspace" / slug / "request.json"
    log = DOCPROD / "manuals" / slug / "opus-master" / "CHANGELOG.md"

    if not req.is_file():
        print(f"ERROR: no request.json at {req}", file=sys.stderr)
        return 2
    if not log.is_file():
        print(f"ERROR: no CHANGELOG.md at {log}", file=sys.stderr)
        return 2

    try:
        versions = request_versions(req)
    except json.JSONDecodeError as e:
        print(f"ERROR: {req} is not valid JSON: {e}", file=sys.stderr)
        return 2

    if not versions:
        print(f"FINDING  {slug}")
        print(f"  {req}: no documents[*].metadata.version")
        print("\nFIX: give the document a metadata.version -- the cover renders "
              "from it.")
        return 1

    findings = 0

    decorated = [v for v in versions if not BARE.match(v.strip())]
    if decorated:
        findings += 1
        print(f"FINDING  {slug}  (version shape)")
        for v in decorated:
            print(f"  {req}: metadata.version = {v!r}")
        print("      the cover supplies the word \"Version\" itself, so this "
              "renders it twice")
        print("  FIX: make it a bare number -- \"1.1.3\", not \"Version 1.1.3\" "
              "and not \"v1.1.0\".")
        print()

    top = top_changelog_version(log)
    if top is None:
        print(f"FINDING  {slug}")
        print(f"  {log}: no `## v<X.Y.Z>` heading found")
        print(f"      request.json is about to render version {versions[0]}")
        print("\nFIX: add a top entry naming that version.")
        return 1

    top_n = normalise(top)
    bad = [v for v in versions if normalise(v) != top_n]
    if bad:
        print(f"FINDING  {slug}")
        for v in bad:
            print(f"  {req}: renders version {v} (reads {normalise(v)})")
        print(f"  {log}: top entry is v{top} (reads {top_n})")
        print("\nThe cover will print a version the changelog does not describe.")
        print("FIX: add or re-head the top CHANGELOG entry to name the rendered "
              "version. If the version being replaced was never tagged, RENAME "
              "that entry rather than adding a second one.")
        return 1

    if findings:
        return 1
    if not quiet:
        print(f"CLEAN  {slug}: request.json {versions[0]} == CHANGELOG v{top}")
    return 0


def negative_control() -> int:
    """Prove the comparison can fail. A check that cannot fail has not been
    verified, it has been run."""
    cases = [
        ("3.1.10", "3.1.9", False, "the Assembly shape: entry one patch behind"),
        ("3.0.8", "3.0.7", False, "the deSilva shape: no entry for the bump"),
        ("1.0.1", "1.0", False, "a two-part entry against a three-part bump"),
        ("1.0", "1.0.0", True, "two-part request against a three-part entry"),
        ("3.1.10", "3.1.10", True, "the passing case"),
        ("Version 1.1.3", "1.1.3", True,
         "a DECORATED value still compares equal -- a shape defect must not "
         "also masquerade as a changelog mismatch"),
    ]
    ok = True
    for req, log, want_equal, why in cases:
        got_equal = normalise(req) == normalise(log)
        verdict = "ok" if got_equal == want_equal else "WRONG"
        if got_equal != want_equal:
            ok = False
        print(f"  {verdict:5} request {req:14} vs entry {log:8} -> "
              f"{'match' if got_equal else 'MISMATCH':8}  ({why})")

    print()
    shapes = [("1.1.3", True), ("1.0", True), ("Version 1.1.3", False),
              ("v1.1.0", False), ("1.0.1-rc1", False)]
    for v, want_bare in shapes:
        got_bare = bool(BARE.match(v.strip()))
        verdict = "ok" if got_bare == want_bare else "WRONG"
        if got_bare != want_bare:
            ok = False
        print(f"  {verdict:5} shape   {v:14} -> "
              f"{'bare' if got_bare else 'DECORATED'}")

    print()
    if ok:
        print("NEGATIVE CONTROL: PASS -- both checks distinguish both ways.")
        return 0
    print("NEGATIVE CONTROL: FAIL -- a check does not mean what it says.")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--slug", help="manual slug")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--negative-control", action="store_true",
                    help="prove the gate can fail, then exit")
    args = ap.parse_args()

    if args.negative_control:
        return negative_control()
    if not args.slug:
        ap.error("--slug is required")
    return check(args.slug, args.quiet)


if __name__ == "__main__":
    sys.exit(main())
