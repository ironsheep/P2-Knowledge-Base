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

    And KB CONTENT that no KB release has published: commits under
    deliverables/ai/P2/ on the current branch after the latest vX.Y.Z tag it
    contains. (F-476, 2026-09-28: F-475's YAML was committed, then pushed to main
    by two MANUAL releases -- a push sends every commit on the branch. The
    published index still carried the old sha256 for those five files, so the MCP
    refused them to every uncached client: "temporarily unavailable -- verification
    failed". The tag check above passed throughout; it asked whether TAGS reached
    the remote, never whether CONTENT sat past the last tag.) This half needs no
    network: it is a question about the local history, answered by `git log`.

WHAT IT DOES NOT DO
    It does not push. Pushing is irreversible and stays Stephen's call every time;
    this only makes the un-pushed state impossible to lose track of. It does not
    release the KB either: the remedy for unreleased KB content is `release-yamls`,
    which regenerates the index against the committed content before the push.

OFFLINE / NETWORK FAILURE
    `git ls-remote` needs the network. If it cannot run, this reports UNKNOWN and
    exits 2 -- it NEVER reports clean. A checker that answers "fine" when it could
    not look is worse than no checker, and this repo has paid for that lesson once
    already (sync-manual-examples.py's git fallback, 2026-08-22).

USAGE
    audit-unpushed-releases.py [--kb-only] [--remote origin]
    audit-unpushed-releases.py --kb-content      # only the F-476 question; no network

EXIT STATUS
    0  every local release tag is on the remote, the branch is not ahead, and no
       KB content sits past the latest KB tag
    1  something is unpushed or unreleased -- the detail lines name it
    2  could not reach the remote (UNKNOWN, never treat as clean)
"""

import argparse
import re
import subprocess
import sys

KB_TAG = re.compile(r"^v\d+\.\d+\.\d+$")
DOC_TAG = re.compile(r"^[a-z0-9][a-z0-9.-]*-v\d+\.\d+(\.\d+)?$")
KB_CONTENT = "deliverables/ai/P2/"


def git(*args, check=True):
    """Run git. A git that CANNOT RUN is never silently defaulted -- see the
    module docstring; that conflation is the bug this file was written after."""
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0 and check:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def unreleased_kb_content():
    """(latest KB tag on this branch, [commit lines under KB_CONTENT after it]).
    The tag is the highest vX.Y.Z REACHABLE from HEAD, compared as numbers --
    string order puts v1.9.0 above v1.21.1."""
    tags = [t for t in git("tag", "--merged", "HEAD").split("\n") if KB_TAG.match(t)]
    if not tags:
        return None, []
    latest = max(tags, key=lambda t: tuple(int(x) for x in t[1:].split(".")))
    log = git("log", "--format=%h %cs %s", f"{latest}..HEAD", "--", KB_CONTENT)
    return latest, [ln for ln in log.split("\n") if ln]


def report_kb_content(latest, commits):
    print(f"UNRELEASED KB CONTENT — {len(commits)} commit(s) under {KB_CONTENT} "
          f"after {latest}")
    for c in commits:
        print(f"    {c}")
    print("  The published index still describes these files as they were at "
          f"{latest}. Pushed as they stand, p2kb-mcp refuses them")
    print("  (\"verification failed\" — F-476). Release the KB first: "
          "`release-yamls` regenerates the index against this content.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--kb-only", action="store_true",
                    help="only the knowledge base's own vX.Y.Z tags")
    ap.add_argument("--kb-content", action="store_true",
                    help="only ask whether KB content sits past the latest KB tag "
                         "(F-476); local history, no network")
    a = ap.parse_args()

    latest, kb_commits = unreleased_kb_content()
    if a.kb_content:
        if latest is None:
            print("no vX.Y.Z tag on this branch — the KB has never been released here")
            return 0
        if not kb_commits:
            print(f"GREEN: no KB content past {latest} — the published index "
                  "describes every committed KB file")
            return 0
        report_kb_content(latest, kb_commits)
        return 1

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

    if not missing and not ahead and not kb_commits:
        print(f"GREEN: all {len(wanted)} release tag(s) are on {a.remote}, "
              f"branch not ahead, no KB content past {latest}")
        return 0

    if kb_commits:
        report_kb_content(latest, kb_commits)
        if not missing and not ahead:
            return 1
        print()

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
