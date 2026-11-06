#!/usr/bin/env python3
"""
audit-kb-pending.py — what KB repair is pending, and has each item been decided?

WHY THIS EXISTS
    A repair seen and set aside is served wrong until someone comes back to it, and
    costs a second release when someone does. This gate puts the question at the two
    moments it can still be acted on: the start of a YAML session, when pending work
    can join the batch, and the start of a release, when a late discovery can.

WHAT COUNTS AS PENDING
    * uncommitted changes under deliverables/ai/P2/
    * commits touching deliverables/ai/P2/ since the latest KB tag
    * every open entry in the corrections register that names a KB path or a .yaml

A DECISION IS A LINE IN THE ENTRY
    > **KB decision:** in batch v1.25.2
    > **KB decision:** held (bench): the question the run must answer
    > **KB decision:** held (document): the document we do not hold
    > **KB decision:** held (Stephen): the call that is his
    > **KB decision:** not KB: where the owed work is

    "held" takes exactly those three blockers, and each needs its reason. "The next
    release" is not one of them.

MODES
    --session              List everything pending. Exit 0: it informs the batch.
    --release vX.Y.Z       Exit 1 on any open KB entry with no valid decision, or an
                           "in batch" for a version older than this release.
    --final                Exit 1 if deliverables/ai/P2/ has uncommitted changes.
                           Combines with --release; alone it is the check after the
                           live read that nothing was left in the tree.
    --negative-control     Prove the checks can fail.

LIMIT
    This reads what the register and git record. It does not know about a defect
    nobody wrote down, and it does not judge whether a stated blocker is true.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REGISTER = Path("engineering/operations/P2KB-CORRECTION-FINDINGS.md")
KB_TREE = "deliverables/ai/P2/"

CLOSED = ("DONE", "WONTFIX", "RESOLVED", "RESOLVED-INVALID")
OPEN = ("CONFIRMED", "NEEDS-VERIFICATION", "PARTIAL", "PARTIALLY CONFIRMED",
        "PENDING-VALIDATION", "TRACKED")

ENTRY_HEAD = re.compile(r"^(?:#{2,4} |- \*\*)(F-\d+)\b", re.M)
SECTION = re.compile(r"^## (?!#)", re.M)
KB_NAMED = re.compile(r"deliverables/ai/P2|[\w./-]+\.yaml\b")
DECISION = re.compile(r"^> \*\*KB decision:\*\*\s*(.+)$", re.M)
IN_BATCH = re.compile(r"^in batch v(\d+)\.(\d+)\.(\d+)\s*$")
HELD = re.compile(r"^held \((bench|document|Stephen)\):\s*\S")
NOT_KB = re.compile(r"^not KB:\s*\S")
SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


def status_of(head):
    """The entry's status from the backticked tokens on its first line; None if absent."""
    found = None
    for token in re.findall(r"`([^`]+)`", head):
        word = token.strip().rstrip(":)")
        if word in CLOSED or word in OPEN or word.startswith("TRACKED"):
            found = word
    return found


def entries(text):
    """Yield (id, status, body) for each entry; a body stops at the next entry or section."""
    heads = list(ENTRY_HEAD.finditer(text))
    headed = {m.group(1) for m in heads if m.group(0).startswith("#")}
    for n, m in enumerate(heads):
        is_bullet = m.group(0).startswith("-")
        # A bullet naming an entry that has its own heading, or several IDs, is a digest line.
        if is_bullet and (m.group(1) in headed or text[m.end():m.end() + 2] == ", "):
            continue
        end = heads[n + 1].start() if n + 1 < len(heads) else len(text)
        section = SECTION.search(text, m.end())
        if section and section.start() < end:
            end = section.start()
        body = text[m.start():end]
        # A bullet entry wraps, so its status can sit on any line of its first paragraph.
        lead = body.split("\n\n", 1)[0] if is_bullet else body.split("\n", 1)[0]
        yield m.group(1), status_of(lead), body


def open_kb_entries(text):
    """Open entries naming the KB. An unreadable status counts as open: unknown is not closed."""
    return [(fid, status, body) for fid, status, body in entries(text)
            if status not in CLOSED and KB_NAMED.search(body)]


def judge(body, release):
    """Why this entry fails the release, or None if its decision stands."""
    m = DECISION.search(body)
    if not m:
        return "no decision"
    decision = m.group(1).strip()
    if HELD.match(decision) or NOT_KB.match(decision):
        return None
    batch = IN_BATCH.match(decision)
    if batch:
        if tuple(int(x) for x in batch.groups()) < release:
            return f"stale decision: {decision}"
        return None
    return f"not a valid decision: {decision}"


def git_lines(*args):
    out = subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout
    return [ln for ln in out.split("\n") if ln.strip()]


def dirty_kb():
    return git_lines("status", "--porcelain", "--", KB_TREE)


def latest_tag():
    tags = [t for t in git_lines("tag", "--list") if re.fullmatch(r"v\d+\.\d+\.\d+", t)]
    return max(tags, key=lambda t: tuple(int(x) for x in t[1:].split("."))) if tags else None


def session(text):
    tag = latest_tag()
    dirty = dirty_kb()
    commits = git_lines("log", "--oneline", f"{tag}..HEAD", "--", KB_TREE) if tag else []
    pending = open_kb_entries(text)
    print(f"Latest KB tag: {tag}")
    print(f"Uncommitted under {KB_TREE}: {len(dirty)}")
    for ln in dirty:
        print(f"  {ln}")
    print(f"Commits touching it since the tag: {len(commits)}")
    for ln in commits:
        print(f"  {ln}")
    print(f"Open register entries naming the KB: {len(pending)}")
    for fid, status, body in pending:
        m = DECISION.search(body)
        print(f"  {fid} [{status or 'no status'}] {m.group(1).strip() if m else 'UNDECIDED'}")
    print("PASS: listed. Add what can be fixed to this batch before editing anything else.")
    return 0


def release_check(text, version):
    m = SEMVER.match(version)
    if not m:
        print(f"ERROR: not a version: {version}")
        return 2
    release = tuple(int(x) for x in m.groups())
    pending = open_kb_entries(text)
    bad = [(fid, why) for fid, _, body in pending for why in [judge(body, release)] if why]
    for fid, why in bad:
        print(f"  {fid}: {why}")
    if bad:
        print(f"FAIL: {len(bad)} of {len(pending)} open KB entries undecided for v{version.lstrip('v')}")
        return 1
    print(f"PASS: all {len(pending)} open KB entries decided for v{version.lstrip('v')}")
    return 0


def final_check():
    dirty = dirty_kb()
    for ln in dirty:
        print(f"  {ln}")
    if dirty:
        print(f"FAIL: {len(dirty)} uncommitted change(s) under {KB_TREE}")
        return 1
    print(f"PASS: nothing uncommitted under {KB_TREE}")
    return 0


def negative_control():
    release = (1, 25, 2)
    cases = [
        ("no decision", "### F-1 — x.yaml — `CONFIRMED`\nbody\n", True),
        ("next release is not a blocker",
         "### F-1 — x.yaml — `CONFIRMED`\n> **KB decision:** held (next release): later\n", True),
        ("held with no reason", "### F-1 — x.yaml — `CONFIRMED`\n> **KB decision:** held (bench):\n", True),
        ("stale batch", "### F-1 — x.yaml — `PENDING-VALIDATION`\n> **KB decision:** in batch v1.25.1\n", True),
        ("no status counts as open", "### F-1 — x.yaml\nbody\n", True),
        ("this batch", "### F-1 — x.yaml — `CONFIRMED`\n> **KB decision:** in batch v1.25.2\n", False),
        ("bench blocker", "### F-1 — x.yaml — `CONFIRMED`\n> **KB decision:** held (bench): what happens\n", False),
        ("his call", "### F-1 — x.yaml — `CONFIRMED`\n> **KB decision:** held (Stephen): the name\n", False),
        ("not KB", "### F-1 — x.yaml — `PARTIAL`\n> **KB decision:** not KB: the manual\n", False),
    ]
    wrong = []
    for label, text, should_fail in cases:
        found = open_kb_entries(text)
        failed = any(judge(body, release) for _, _, body in found)
        if failed != should_fail or not found:
            wrong.append(label)
    closed = open_kb_entries("### F-1 — x.yaml — `RESOLVED`\n")
    unrelated = open_kb_entries("### F-1 — a manual page — `CONFIRMED`\n")
    if closed:
        wrong.append("closed entry read as open")
    if unrelated:
        wrong.append("entry naming no KB path read as KB")
    if len(open_kb_entries("- **F-1** x.yaml\n\n### F-1 — x.yaml — `CONFIRMED`\n")) != 1:
        wrong.append("digest bullet counted beside its entry")
    if open_kb_entries("- **F-1, F-2** x.yaml\n"):
        wrong.append("multi-ID digest bullet read as an entry")
    if open_kb_entries("- **F-1 — x.yaml wraps\n  to here — `RESOLVED`\n"):
        wrong.append("status on a bullet's second line missed")
    if wrong:
        print(f"FAIL: negative control wrong on: {', '.join(wrong)}")
        return 1
    print("Negative control: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--session", action="store_true")
    ap.add_argument("--release", metavar="VERSION")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--negative-control", action="store_true")
    ap.add_argument("--register", type=Path, default=REGISTER)
    args = ap.parse_args()

    if args.negative_control:
        return negative_control()
    if not (args.session or args.release or args.final):
        ap.error("name a mode: --session, --release VERSION or --final")
    if not args.register.exists():
        print(f"ERROR: register not found: {args.register}")
        return 2
    text = args.register.read_text(encoding="utf-8")

    if args.session:
        return session(text)
    code = 0
    if args.release:
        code = max(code, release_check(text, args.release))
    if args.final:
        code = max(code, final_check())
    return code


if __name__ == "__main__":
    sys.exit(main())
