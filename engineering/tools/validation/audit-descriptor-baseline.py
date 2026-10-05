#!/usr/bin/env python3
"""
audit-descriptor-baseline.py - a document's MANUAL-DESCRIPTOR names the release it was last published as.

WHY THIS EXISTS
    `last_published_tag` in each MANUAL-DESCRIPTOR.md is the baseline every
    diff-since-published audit measures from (Dimension #15, `audit-changelog`).
    Nothing in a release advanced it automatically, so every release made its own
    descriptor stale the moment it tagged. F-282 found and fixed that once
    (2026-08-25: eight stale) and put the step in the release skill's overlay as
    prose. Six weeks later twelve of seventeen were stale again, including four
    released the same day the check ran (2026-10-05): the overlay was never loaded
    with the skill, so the step was never read. Prose is a reminder; a runner is a
    gate. This is the gate.

MODES
    --slug S --version V   RELEASE mode (blocking in validate-manual-release.py's
                           release phase). The descriptor of S must name the tag
                           THIS release creates: `<s>-v<V>`, compared case-
                           insensitively (the app-note tag namespace is case-split,
                           F-282). Run before the tag exists, so it cannot be read
                           from git -- it is read from request.json's version.
    (no args)              FLEET mode. Every descriptor under manuals/ and
                           app-notes/ must name its latest existing tag; a document
                           with no tag must carry an empty value or `none`.

EXIT
    0 = every checked descriptor current    1 = stale    2 = bad usage / unreadable
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCPROD = ROOT / "engineering" / "document-production"
FIELD = re.compile(r"^last_published_tag:\s*([^\s#]*)", re.M)


def recorded(desc: Path):
    m = FIELD.search(desc.read_text(encoding="utf-8"))
    return None if m is None else m.group(1)


def latest_tag(slug: str) -> str:
    tags = subprocess.run(["git", "-C", str(ROOT), "tag"], capture_output=True,
                          text=True, check=True).stdout.split()
    mine = [t for t in tags if t.lower().startswith(slug.lower() + "-v")]

    def key(t):
        return [int(x) if x.isdigit() else x for x in re.split(r"[.\-v]", t.lower())]
    return sorted(mine, key=key)[-1] if mine else ""


def descriptors():
    return sorted(list(DOCPROD.glob("manuals/*/MANUAL-DESCRIPTOR.md")) +
                  list(DOCPROD.glob("app-notes/*/MANUAL-DESCRIPTOR.md")))


def release_mode(slug, version):
    hits = [d for d in descriptors() if d.parent.name.lower() == slug.lower()]
    if not hits:
        print(f"SKIP   {slug}: no MANUAL-DESCRIPTOR.md")
        return 0
    want = f"{slug}-v{version}".lower()
    rec = recorded(hits[0])
    if rec is None:
        print(f"FAIL   {hits[0].relative_to(ROOT)}: no last_published_tag field")
        return 1
    if rec.lower() != want:
        print(f"FAIL   {hits[0].relative_to(ROOT)}: last_published_tag is {rec!r}; this release "
              f"creates {want!r}. Advance it (date and page count from git, per the "
              f"release-manual overlay) before tagging.")
        return 1
    print(f"CLEAN  {slug}: last_published_tag names this release ({rec})")
    return 0


def fleet_mode():
    stale = []
    for d in descriptors():
        slug, rec, act = d.parent.name, recorded(d), latest_tag(d.parent.name)
        if act:
            if (rec or "").lower() != act.lower():
                stale.append(f"{slug}: records {rec!r}, latest tag {act!r}")
        elif rec not in ("", "none", None):
            stale.append(f"{slug}: records {rec!r} but has no release tag")
    if stale:
        print(f"FAIL   {len(stale)} stale descriptor(s):")
        for s in stale:
            print(f"         - {s}")
        return 1
    print(f"CLEAN  all {len(descriptors())} descriptors name their latest release")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug")
    ap.add_argument("--version")
    a = ap.parse_args()
    if bool(a.slug) != bool(a.version):
        ap.error("--slug and --version go together")
    return release_mode(a.slug, a.version) if a.slug else fleet_mode()


if __name__ == "__main__":
    sys.exit(main())
