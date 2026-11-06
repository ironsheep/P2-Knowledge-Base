#!/usr/bin/env python3
"""
audit-commit-silos.py - a commit carries one silo, and YAML is committed at its release.

WHY THIS EXISTS
    A push publishes every commit beneath it, so work committed early decides the
    order the fronts can release in. On 2026-11-05 one YAML commit and one commit
    mixing fvar.yaml with three manuals sat under P2AN007's release and blocked its
    push at kb-content-released. The hard rule "a commit carries only the work in
    hand" already existed and said nothing that a commit could fail against.

WHAT IT CHECKS
    Each path is classed into a silo:
        kb          deliverables/ai/ and the KB compile manifest
        doc:<slug>  one document: its manual, app-note, workspace and outbound folders,
                    and its PDF, ZIP and changelog under deliverables/documents/DOCs/
        (none)      everything else, including shared files such as the register and
                    the roster; explicit-path staging and hunk review govern those
    A commit fails when:
      - it holds kb and any document;
      - it holds more than one document, unless it names a release wave Stephen called.
    With --staged, a commit holding kb also fails unless it is declared part of a KB
    release, because YAML is committed when its own release starts.

USAGE
    audit-commit-silos.py                  commits ahead of upstream (the release gate)
    audit-commit-silos.py --staged         the index (the pre-commit hook)
    audit-commit-silos.py --commit SHA     one commit
    audit-commit-silos.py --negative-control

    A wave is declared by a "Release-wave: <name>" trailer in the commit message, or
    P2KB_RELEASE_WAVE=<name> at commit time, which the pre-commit hook reads because a
    hook cannot see the message. A KB release commit is declared by P2KB_KB_RELEASE=<version>.

EXIT STATUS
    0  every commit holds one silo
    1  a commit mixes silos, or holds YAML outside a KB release
    2  could not run (never treat as clean)
"""

import argparse
import os
import re
import subprocess
import sys

KB_PREFIXES = ("deliverables/ai/", "engineering/tools/validation/kb-compile-manifest/")
DOC_FOLDER = re.compile(
    r"^engineering/document-production/(?:manuals|app-notes|workspace|outbound)/([^/]+)/")
DOC_RELEASED = re.compile(r"^deliverables/documents/DOCs/([^/]+?)(?:-src|-changelog)?\.[^./]+$")
WAVE_TRAILER = re.compile(r"^Release-wave:\s*\S", re.M)


def git(*args):
    """Run git. A git that cannot run exits 2, never a pass."""
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"UNKNOWN: git {' '.join(args)} failed: {r.stderr.strip()}")
        sys.exit(2)
    return r.stdout


def silo_of(path):
    """The silo a path belongs to, or None for shared ground."""
    if path.startswith(KB_PREFIXES):
        return "kb"
    m = DOC_FOLDER.match(path) or DOC_RELEASED.match(path)
    return f"doc:{m.group(1).lower()}" if m else None


def silos_of(paths):
    return {s for s in map(silo_of, paths) if s}


def violation(silos, wave, kb_release=None, staged=False):
    """Why this set of silos may not be one commit, or None."""
    docs = sorted(s for s in silos if s != "kb")
    if "kb" in silos and docs:
        return f"mixes KB work with {', '.join(docs)}"
    if len(docs) > 1 and not wave:
        return f"mixes documents without a declared wave: {', '.join(docs)}"
    if staged and "kb" in silos and not kb_release:
        return ("holds KB work outside a KB release: YAML stays uncommitted until "
                "release-yamls starts (P2KB_KB_RELEASE=<version>)")
    return None


def check_commit(sha):
    subject = git("log", "-1", "--format=%h %s", sha).strip()
    message = git("log", "-1", "--format=%B", sha)
    paths = git("show", "--name-only", "--format=", sha).split()
    why = violation(silos_of(paths), bool(WAVE_TRAILER.search(message)))
    if why:
        print(f"FAIL  {subject[:100]}\n      {why}")
    return why is None


def negative_control():
    """The checker must be able to fail, and must pass what is allowed."""
    kb = "deliverables/ai/P2/language/pasm2/fvar.yaml"
    a = "engineering/document-production/manuals/p2-assembly-language-manual/opus-master/CHANGELOG.md"
    x = "engineering/document-production/manuals/p2-xbyte-programming-guide/opus-master/CHANGELOG.md"
    p = "engineering/document-production/app-notes/P2AN007/opus-master/P2AN007.md"
    pdf = "deliverables/documents/DOCs/P2AN007.pdf"
    zip_ = "deliverables/documents/DOCs/P2AN007-src.zip"
    log = "deliverables/documents/DOCs/p2an007-changelog.md"
    shared = "engineering/operations/P2KB-CORRECTION-FINDINGS.md"
    cases = [
        ("kb + document", [kb, p], {}, True),
        ("two documents", [a, x], {}, True),
        ("two documents, wave", [a, x], {"wave": True}, False),
        ("kb + document, wave", [kb, p], {"wave": True}, True),
        ("kb staged, no release", [kb], {"staged": True}, True),
        ("kb staged, in release", [kb, shared], {"staged": True, "kb_release": "v1"}, False),
        ("one document's files", [p, pdf, zip_, log, shared], {}, False),
        ("shared only", [shared], {}, False),
    ]
    ok = True
    for name, paths, kw, expect_fail in cases:
        kw = {"wave": False, **kw}
        failed = violation(silos_of(paths), **kw) is not None
        if failed != expect_fail:
            ok = False
            print(f"NEGATIVE CONTROL: wrong answer for {name}")
    print("NEGATIVE CONTROL: PASS" if ok else "NEGATIVE CONTROL: FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staged", action="store_true", help="check the index")
    ap.add_argument("--commit", help="check one commit")
    ap.add_argument("--negative-control", action="store_true")
    a = ap.parse_args()

    if a.negative_control:
        return negative_control()

    if a.staged:
        paths = git("diff", "--cached", "--name-only").split()
        why = violation(silos_of(paths), bool(os.environ.get("P2KB_RELEASE_WAVE")),
                        os.environ.get("P2KB_KB_RELEASE"), staged=True)
        if why:
            print(f"COMMIT REFUSED: this commit {why}.")
            print("  A commit carries one silo (.claude/doctrine-overlay.md, "
                  "A commit carries only the work in hand).")
            return 1
        return 0

    if a.commit:
        return 0 if check_commit(a.commit) else 1

    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}").strip()
    shas = git("rev-list", f"{upstream}..HEAD").split()
    ok = all([check_commit(s) for s in shas])
    hooks = subprocess.run(["git", "config", "core.hooksPath"],
                           capture_output=True, text=True).stdout.strip()
    if hooks != "engineering/tools/git-hooks":
        print("WARNING: the pre-commit silo check is not armed in this clone. Run: "
              "git config core.hooksPath engineering/tools/git-hooks")
    if ok:
        print(f"GREEN: {len(shas)} commit(s) ahead of {upstream}, each holding one silo")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
