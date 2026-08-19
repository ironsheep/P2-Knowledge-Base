#!/usr/bin/env python3
"""
audit-register-hygiene.py — mechanical checks on a tracking register.

WHY THIS EXISTS
    Every register failure this project has had shares one shape: the record was
    CORRECT, and nothing was forced to consult it at the moment a decision was made.
      * the cross-ref adopt-at-next-release rule, correct since 2026-06-26, passed
        over ~12 releases (F-301)
      * a rejected fix (F-281 breaklines) whose retirement never reached the task
        that had been cut from it, and which then reached the session front door
      * the register's own next-ID counter left behind an allocation, which is how
        the F-260 duplicate happened in the first place
    Prose cannot fix that class. A check that RUNS can. Everything below is a rule
    the register already states about itself, made executable.

    "We can't afford to use a process that misses things, ever." — so the rules
    that must not be missed stop being things a reader has to notice.

CHECKS
    1  next-ID counter is ahead of every allocated ID      (allocation drift)
    2  no finding ID appears as two entries                (protocol says: STOP)
    3  no CLOSED finding sits in a live open-work register (scan noise)
    4  every finding carries a status                      (unreadable state)
    5  every archive the header names actually exists      (dangling history)
    6  no allocated ID is missing from live + archives     (a finding went silent)
    7  --sweep-check REV: NOTHING from the pre-sweep revision vanished

ARCHIVING WITHOUT LOSING CONTENT  (learned 2026-08-15, the expensive way)
    Do the sweep as RENAME-THEN-TRIM, never build-the-output:
      1. `engineering/tools/backup-file.sh <register>`
      2. `git mv` the register to the dated archive path — the archive is now
         complete BY CONSTRUCTION, a tracked rename of the original.
      3. Recreate the register and remove from the archive only what stays open.
         Everything afterwards is SUBTRACTION from a preserved copy.
      4. `--sweep-check <pre-sweep-rev>` to prove nothing vanished.
    The first attempt at that sweep built the new files instead of subtracting,
    silently lost 223 lines and an entire section, AND PASSED ITS OWN VERIFICATION
    — because the check was computed from the same block model that had dropped
    them. That is the general trap: a check derived from the thing it is checking
    proves nothing. --sweep-check reads the original out of git, independently.

EXIT
    0 = clean, 1 = violations. Intended as a gate, not a report you skim.
"""

import argparse
import os
import re
import subprocess
import sys

# Statuses appear backticked (`DONE`) and bare (DONE (2026-08-16) — ...). Match both,
# but only as whole words, so "RESOLVED" inside prose does not read as a status.
CLOSED_WORDS = ("DONE", "WONTFIX", "RESOLVED-INVALID")
STATUS_WORDS = CLOSED_WORDS + ("CONFIRMED", "NEEDS-VERIFICATION", "PARTIAL",
                               "NOTED", "RESOLVED", "TRACKED")
CLOSED_RE = re.compile(r"`?\b(" + "|".join(CLOSED_WORDS) + r")\b`?")
STATUS_RE = re.compile(r"`?\b(" + "|".join(STATUS_WORDS) + r")\b`?|TRACKED → ingestion")
# Headline phrasings that mean "this finding is finished" even when the status
# token still reads CONFIRMED — the register writes its verdict in bold prose.
RESOLVED_HEADLINE = re.compile(
    r"\*\*(?:ALL [A-Z]+ FIXED|FIXED\b|RESOLVED\b|MECHANISM LANDED|source fixed|tool fixed|"
    r"POLISH, NOT A GATE|no longer blocks)", re.I)

FINDING_START = re.compile(
    r"^(?:#{3,4}\s+(F-\d+[a-z]?)\s*[—-]"          # heading form:  ### F-300 — ...
    r"|-\s+\*\*(F-\d+[a-z]?)\s+[—-])")          # bulleted ENTRY: - **F-250 — ...
                                                    # (NOT "- **F-256** — ", a reference)


def parse(path):
    """Split a register into (id, headline, body, line_no) blocks."""
    lines = open(path, encoding="utf-8").read().splitlines()
    blocks, cur = [], None
    for i, ln in enumerate(lines, 1):
        m = FINDING_START.match(ln)
        if m:
            fid = m.group(1) or m.group(2)
            if cur:
                blocks.append(cur)
            cur = {"id": fid, "line": i, "headline": ln, "body": [ln]}
        elif cur:
            cur["body"].append(ln)
    if cur:
        blocks.append(cur)
    return lines, blocks


def guardrail_ids(lines):
    """IDs deliberately retained in the live file as do-not-re-file guardrails."""
    ids, inside = set(), False
    for ln in lines:
        if ln.startswith("## ") and "guardrail" in ln.lower():
            inside = True
            continue
        if inside and ln.startswith("## "):
            break
        if inside:
            ids.update(re.findall(r"F-\d+[a-z]?", ln))
    return ids


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("register")
    ap.add_argument("--archive", action="append", default=[],
                    help="archive file holding closed findings (repeatable); "
                         "default: read them from the register header")
    ap.add_argument("--quiet", action="store_true", help="print violations + summary only")
    ap.add_argument("--sweep-check", metavar="REV",
                    help="prove an archive sweep lost nothing: every substantive line of the "
                         "register AT REV must still exist in the live file or an archive. "
                         "Reads REV from git, independently of whatever did the sweep. "
                         "RUN IT AT SWEEP TIME, against the pre-sweep commit, with nothing "
                         "else changed — run retrospectively it reports every later in-place "
                         "rewrite as unaccounted, which is churn, not loss.")
    args = ap.parse_args()

    reg = args.register
    lines, blocks = parse(reg)
    text = "\n".join(lines)
    guards = guardrail_ids(lines)
    viol = []

    def say(msg):
        if not args.quiet:
            print(msg)

    # --- resolve archives (header-declared unless overridden) -------------------
    archives = list(args.archive)
    if not archives:
        base = os.path.dirname(os.path.abspath(reg))
        for rel in re.findall(r"→\s+`([^`]+archive[^`]*\.md)`", text):
            archives.append(os.path.normpath(os.path.join(base, rel)))

    # --- 5: archives exist ------------------------------------------------------
    archived_ids = set()
    for a in archives:
        if not os.path.exists(a):
            viol.append(("dangling-archive", f"header names `{a}` but it does not exist"))
            continue
        archived_ids.update(int(n) for n in re.findall(
            r"F-0*(\d+)", open(a, encoding="utf-8", errors="replace").read()))
    say(f"archives          : {len(archives)} declared, "
        f"{len(archived_ids)} archived IDs seen")

    # --- 2: duplicate entries ---------------------------------------------------
    seen = {}
    for b in blocks:
        seen.setdefault(b["id"], []).append(b["line"])
    for fid, at in sorted(seen.items()):
        if len(at) > 1:
            viol.append(("duplicate-id",
                         f"{fid} has {len(at)} entries at lines {at} — "
                         f"the protocol says STOP, do not choose between them"))

    # --- 1: next-ID counter ahead of every allocation ---------------------------
    nums = [int(re.sub(r"\D", "", f)) for f in seen]
    m = re.search(r"\*\*Next finding ID:\s*`?F-(\d+)`?\*\*", text)
    if not m:
        viol.append(("no-counter", "register declares no `Next finding ID:` line"))
    elif nums:
        nxt, top = int(m.group(1)), max(nums)
        say(f"next-ID counter   : F-{nxt} (highest allocated F-{top})")
        if nxt <= top:
            viol.append(("counter-behind",
                         f"counter reads F-{nxt} but F-{top} is already allocated — "
                         f"the next filing collides"))

    # --- 3 + 4: closed-but-live, and missing status -----------------------------
    closed_live = []
    for b in blocks:
        if b["id"] in guards:
            continue
        body = "\n".join(b["body"])
        if not STATUS_RE.search(body):
            viol.append(("no-status", f"{b['id']} (:{b['line']}) carries no status token"))
        head = b["headline"]
        if CLOSED_RE.search(head) or RESOLVED_HEADLINE.search(head):
            closed_live.append((b["id"], b["line"]))
    for fid, ln in closed_live:
        viol.append(("closed-but-live",
                     f"{fid} (:{ln}) is closed but still in a register that declares "
                     f"it carries OPEN work only — sweep it to an archive"))

    # --- 6: no allocated ID went silent -----------------------------------------
    if nums:
        live = {int(re.sub(r"\D", "", f)) for f in seen}
        known = live | archived_ids
        gaps = [f"F-{n}" for n in range(1, max(nums) + 1) if n not in known]
        say(f"ID coverage       : {len(live)} live, {len(archived_ids)} archived, "
            f"{len(gaps)} unaccounted")
        if gaps:
            viol.append(("id-went-silent",
                         f"{len(gaps)} allocated IDs are in neither the register nor any "
                         f"archive: {', '.join(gaps[:12])}"
                         f"{' …' if len(gaps) > 12 else ''}"))

    # --- 7: sweep-loss check, read independently out of git ---------------------
    if args.sweep_check:
        try:
            old = subprocess.run(["git", "show", f"{args.sweep_check}:{reg}"],
                                 capture_output=True, text=True, check=True).stdout
        except subprocess.CalledProcessError as e:
            print(f"ERROR: cannot read {reg} at {args.sweep_check}: {e.stderr.strip()}")
            return 1
        haystack = text
        for a in archives:
            if os.path.exists(a):
                haystack += "\n" + open(a, encoding="utf-8", errors="replace").read()
        # Substantive lines only: blanks and short scaffolding lines re-occur
        # everywhere and would drown a real loss in noise.
        old_lines = [l.strip() for l in old.splitlines() if len(l.strip()) > 40]
        lost = [l for l in old_lines if l not in haystack]
        say(f"sweep-check       : {len(old_lines)} substantive lines at {args.sweep_check}, "
            f"{len(lost)} now unaccounted")
        if lost:
            viol.append(("sweep-lost-content",
                         f"{len(lost)} substantive lines present at {args.sweep_check} are in "
                         f"NEITHER the live register nor any archive — first: "
                         f"{lost[0][:90]!r}\n      NOTE: meaningful ONLY at sweep time against the "
                         f"pre-sweep commit. If commits landed in between, in-place rewrites (which "
                         f"this register REQUIRES) read as unaccounted. Confirm each against git "
                         f"before calling it loss."))

    # --- report -----------------------------------------------------------------
    say(f"findings          : {len(blocks)} entries, {len(seen)} distinct IDs "
        f"({len(guards)} carry-forward guardrails exempt)")
    if not viol:
        print(f"CLEAN  {reg}: no register-hygiene violations")
        return 0

    print(f"\nVIOLATIONS ({len(viol)}) — {reg}")
    order = ["sweep-lost-content", "duplicate-id", "counter-behind", "no-counter",
             "id-went-silent", "dangling-archive", "no-status", "closed-but-live"]
    for kind in order:
        hits = [v for k, v in viol if k == kind]
        if hits:
            print(f"\n  {kind}  ({len(hits)})")
            for h in hits:
                print(f"    - {h}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
