#!/usr/bin/env python3
"""
audit-unpushed-releases.py - a release that has not been pushed has not happened.

WHY THIS EXISTS
    KB v1.18.1 was committed and tagged on 2026-09-10 and sat LOCAL-ONLY for a day.
    Every consumer -- p2kb-mcp, every agent, every reader -- was still being served
    v1.18.0, so F-416/F-419 stayed PENDING-VALIDATION and agents kept reading the
    wrong CORDIC result formats. The repo looked released. Nothing was.

    The cause is a process shape, not an oversight. `release-yamls` step 6e correctly
    treats the push as a sprint stop -- it is irreversible, and it needs Stephen's go
    EVERY time, never once. What it did wrong was END there: it printed the commands,
    the session wrote "his to push" into a resume key, and the release's unfinished
    half became a line in a note rather than a state anything could see. That is the
    F-301 shape exactly -- a fact recorded where nothing reads it.

    So this exists to be READ, by a runner, at a moment someone is already looking.

WHAT IT CHECKS
    Local release tags that are absent from the remote, and local commits on the
    current branch that are ahead of its upstream. Release tags are the two shapes
    this repo publishes under:
        vX.Y.Z              the knowledge base
        <slug>-vX.Y.Z       a document (p2an001-v1.0.5, p2-streamer-...-v1.1.0)

WHAT IT DOES NOT DO
    It does not push. Pushing is irreversible and stays Stephen's call every time;
    this only makes the un-pushed state impossible to lose track of.

OFFLINE / NETWORK FAILURE
    `git ls-remote` needs the network. If it cannot run, this reports UNKNOWN and
    exits 2 -- it NEVER reports clean. A checker that answers "fine" when it could
    not look is worse than no checker, and this repo has paid for that lesson once
    already (sync-manual-examples.py's git fallback, 2026-08-22).

USAGE
    audit-unpushed-releases.py [--kb-only] [--remote origin]

EXIT STATUS
    0  every local release tag is on the remote, and the branch is not ahead
    1  something is unpushed -- the detail lines name it
    2  could not reach the remote (UNKNOWN, never treat as clean)
"""

import argparse
import re
import subprocess
import sys

KB_TAG = re.compile(r"^v\d+\.\d+\.\d+$")
DOC_TAG = re.compile(r"^[a-z0-9][a-z0-9.-]*-v\d+\.\d+(\.\d+)?$")


def git(*args, check=True):
    """Run git. A git that CANNOT RUN is never silently defaulted -- see the
    module docstring; that conflation is the bug this file was written after."""
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0 and check:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--kb-only", action="store_true",
                    help="only the knowledge base's own vX.Y.Z tags")
    a = ap.parse_args()

    local = [t for t in git("tag").split("\n") if t]
    wanted = [t for t in local
              if KB_TAG.match(t) or (not a.kb_only and DOC_TAG.match(t))]
    if not wanted:
        print("no release tags exist locally — nothing to publish")
        return 0

    try:
        raw = git("ls-remote", "--tags", a.remote)
    except RuntimeError as e:
        print(f"UNKNOWN: cannot reach {a.remote} — {e}")
        print("  This is NOT a pass. Re-run where the remote is reachable.")
        return 2

    remote = {ln.split("refs/tags/")[-1].removesuffix("^{}")
              for ln in raw.split("\n") if "refs/tags/" in ln}

    missing = sorted(t for t in wanted if t not in remote)

    ahead = ""
    try:
        upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
        n = git("rev-list", "--count", f"{upstream}..HEAD")
        if n and n != "0":
            ahead = f"{n} commit(s) ahead of {upstream}"
    except RuntimeError:
        ahead = "no upstream configured for the current branch"

    if not missing and not ahead:
        print(f"GREEN: all {len(wanted)} release tag(s) are on {a.remote}, "
              f"branch not ahead")
        return 0

    print(f"UNPUBLISHED WORK — checked {len(wanted)} local release tag(s) "
          f"against {a.remote}")
    for t in missing:
        kind = "knowledge base" if KB_TAG.match(t) else "document"
        print(f"  TAG NOT ON REMOTE  {t}  ({kind})")
        if KB_TAG.match(t):
            print("        p2kb-mcp serves the published state, so every agent is "
                  "still reading the PREVIOUS release.")
    if ahead:
        print(f"  BRANCH             {ahead}")
    print("\n  Push IS publish. Until these land, the release has not happened —")
    print("  whatever the local repo, the CHANGELOG or a resume note says.")
    print("  The push stays Stephen's call; this only refuses to let it go quiet.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
