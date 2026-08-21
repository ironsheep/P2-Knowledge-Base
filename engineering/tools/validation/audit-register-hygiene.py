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
    4b prose claims "fixed" while the status does not       (status needs deciding)
    5  every archive the header names actually exists      (dangling history)
    6  no allocated ID is missing from live + archives     (a finding went silent)
    7  --sweep-check REV: NOTHING from the pre-sweep revision vanished
    8  no `##` section header outlives every finding it names   (dead scaffolding)
    9  no live finding sits under a header that does not name it (mis-filed entry)
   10  a finding's HEADLINE status agrees with its body `**Status:**` line

CHECK 10 — THE UNDERSTATING DIRECTION  (learned 2026-08-21, from F-271)
    4b catches a headline claiming MORE than the status token supports. Nothing
    caught the reverse, and the reverse is the one that wastes work: F-271's
    headline reads `CONFIRMED — scope decision owed, deliberately NOT swept`
    while its own body ends `**Status:** RESOLVED — DECIDED AND PUNCH-LISTED`,
    with Stephen's decision recorded in full and the work carried to a punch-list
    item. Anyone scanning headlines — which is what the register is FOR — reads a
    decision as still owed and re-opens a settled question. The scannable layer
    and the authoritative layer must not disagree in EITHER direction.

SECTION STRUCTURE — WHY 8 AND 9 EXIST  (learned 2026-08-21)
    Checks 1-7 read `###` finding entries and never looked at the `##` section
    headers above them. A trim-style archive sweep removes entries; it does not
    remove the section header and origin prose that introduced them. What is left
    is a header, in a register that declares it carries OPEN work only, asserting
    a defect that was closed months ago — e.g. "`architecture/xbyte_engine.yaml` —
    all three programming examples are broken", whose findings all closed
    2026-07-14/16. Every check above passed on it, because there was no entry left
    to check. A reader scanning for "what is still owed" reads the header.
    The mirror failure is 9: when a section's own findings are archived but LATER
    findings were appended beneath it, those inherit a header about something else
    entirely — 14 platform/escaper findings reading as part of a community bench
    review. Both are invisible to an entry-level check and obvious to a span-level
    one.

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
# THE STATUS TOKEN IS AUTHORITATIVE. Prose is not a status.
# Learned in the 2026-08-19 sweep: 16 findings whose headline read "source fixed" /
# "tool fixed" were still `CONFIRMED`, and most added "render owed" — a fix applied but
# not yet validated is NOT done, by this register's own rule. Treating the prose as a
# verdict would have archived all sixteen with work still owed. So a prose-vs-status
# mismatch is its own finding (a status that needs deciding), never a licence to sweep.
FIXED_PROSE = re.compile(
    r"\*\*(?:ALL [A-Z]+ FIXED|FIXED\b|RESOLVED\b|MECHANISM LANDED|source fixed|tool fixed|"
    r"no longer blocks)", re.I)
# PARTIAL vetoes an embedded DONE ("manual DONE - KB DONE - one decision open" is PARTIAL).
PARTIAL_RE = re.compile(r"\bPARTIAL\b")
# A body-level `**Status:** X` line. This is the finding's own considered verdict,
# written after the analysis; the headline is the scannable summary. When they
# disagree the register misreports itself to every reader who scans.
BODY_STATUS = re.compile(r"^\*\*Status:\*\*\s*`?\s*([A-Z][A-Z-]*)", re.M)


def lead_status(s):
    """The first status token in a string, or None."""
    m = STATUS_RE.search(s)
    if not m:
        return None
    return (m.group(1) or m.group(0)).strip("` ")

# Both series the register allocates: F-### corrections and G-### gap/enrichment
# entries. G was absent here until 2026-08-21, which made every G finding invisible
# to every check — G-004 sat live and `DONE` through a sweep that was looking for
# exactly that. The two are SEPARATE NUMBER SPACES: they are counted, gap-checked
# and reported apart, never merged into one range.
FINDING_START = re.compile(
    r"^(?:#{3,4}\s+([FG]-\d+[a-z]?)\s*[—-]"         # heading form:  ### F-300 — ...
    r"|-\s+\*\*([FG]-\d+[a-z]?)\s+[—-])")           # bulleted ENTRY: - **F-250 — ...
                                                    # (NOT "- **F-256** — ", a reference)

# A `##` section header, not a `###` finding entry.
SECTION_START = re.compile(r"^##\s+(?!#)")
# IDs a section header claims, including ranges: "F-303…F-305", "G-001…G-005",
# "F-217, F-218". Leading zeros are stripped so a header's `G-001…G-005` and an
# entry's `### G-004` compare equal — the padding differs in the register today.
ID_RANGE = re.compile(r"\b([FG])-0*(\d+)\s*(?:…|\.{3})\s*[FG]-0*(\d+)\b")
ID_ONE = re.compile(r"\b([FG])-0*(\d+)\b")


def canon(fid):
    """'G-004' -> 'G-4'; 'F-302' -> 'F-302'. Strips padding and any letter suffix."""
    m = re.match(r"([FG])-0*(\d+)", fid)
    return f"{m.group(1)}-{int(m.group(2))}" if m else fid


def header_ids(header):
    """The set of canonical IDs a section header claims, ranges expanded."""
    ids = set()
    for pre, lo, hi in ID_RANGE.findall(header):
        ids.update(f"{pre}-{n}" for n in range(int(lo), int(hi) + 1))
    for pre, n in ID_ONE.findall(header):
        ids.add(f"{pre}-{int(n)}")
    return ids


def sections(lines, blocks):
    """[(line_no, header, [blocks inside its span])] for headers that name IDs."""
    starts = [i for i, ln in enumerate(lines, 1) if SECTION_START.match(ln)]
    out = []
    for k, i in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines) + 1
        header = lines[i - 1]
        if not header_ids(header):
            continue                     # a generic header claims nothing; nothing to drift
        out.append((i, header, [b for b in blocks if i < b["line"] < end]))
    return out


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
    archived_ids = set()                 # canonical ids, e.g. {"F-302", "G-4"}
    for a in archives:
        if not os.path.exists(a):
            viol.append(("dangling-archive", f"header names `{a}` but it does not exist"))
            continue
        archived_ids.update(f"{p}-{int(n)}" for p, n in re.findall(
            r"\b([FG])-0*(\d+)\b", open(a, encoding="utf-8", errors="replace").read()))
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
    # F and G are separate number spaces; the declared counter governs F only.
    live_by_series = {}
    for fid in seen:
        pre, n = canon(fid).split("-")
        live_by_series.setdefault(pre, set()).add(int(n))
    nums = sorted(live_by_series.get("F", set()))
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

        # --- 10: the scannable layer must agree with the authoritative one ------
        body_tokens = {t for t in BODY_STATUS.findall(body) if t in STATUS_WORDS}
        head_token = lead_status(head)
        if body_tokens and head_token and head_token not in body_tokens:
            viol.append(("status-disagrees-with-body",
                         f"{b['id']} (:{b['line']}) headline reads {head_token} but its own "
                         f"`**Status:**` line reads {'/'.join(sorted(body_tokens))} — a reader "
                         f"scanning headlines gets the wrong answer; reconcile the two, and if "
                         f"the body is right the headline is what needs rewriting"))

        if PARTIAL_RE.search(head):
            continue                      # still owed, whatever else the headline says
        if CLOSED_RE.search(head):
            closed_live.append((b["id"], b["line"]))
        elif FIXED_PROSE.search(head):
            viol.append(("status-hygiene",
                         f"{b['id']} (:{b['line']}) headline claims it is fixed but its status "
                         f"token is not DONE/WONTFIX/RESOLVED-INVALID — decide the status "
                         f"deliberately; do NOT sweep on the prose"))
    for fid, ln in closed_live:
        viol.append(("closed-but-live",
                     f"{fid} (:{ln}) is closed but still in a register that declares "
                     f"it carries OPEN work only — sweep it to an archive"))

    # --- 6: no allocated ID went silent -----------------------------------------
    # Per series, so an F gap is never masked by a G that happens to share a number.
    live_ids = {canon(f) for f in seen}
    known = live_ids | archived_ids
    gaps = []
    for pre, live_nums in sorted(live_by_series.items()):
        ceiling = max(live_nums | {int(n.split("-")[1]) for n in archived_ids
                                   if n.startswith(pre + "-")} or {0})
        gaps += [f"{pre}-{n}" for n in range(1, ceiling + 1)
                 if f"{pre}-{n}" not in known]
    if live_ids:
        say(f"ID coverage       : {len(live_ids)} live, {len(archived_ids)} archived, "
            f"{len(gaps)} unaccounted")
        if gaps:
            viol.append(("id-went-silent",
                         f"{len(gaps)} allocated IDs are in neither the register nor any "
                         f"archive: {', '.join(gaps[:12])}"
                         f"{' …' if len(gaps) > 12 else ''}"))

    # --- 8 + 9: section structure -----------------------------------------------
    # A `##` header that names IDs is a CLAIM about what lives under it. Both
    # failures below are invisible to every entry-level check above, because the
    # evidence is the header, not any entry.
    for ln, header, kids in sections(lines, blocks):
        named = header_ids(header)
        inside = {canon(b["id"]) for b in kids}
        label = header[3:].strip()
        label = (label[:88] + "…") if len(label) > 88 else label
        if not (named & inside):
            viol.append(("orphaned-section",
                         f"(:{ln}) names {', '.join(sorted(named))} — NONE is a live entry, "
                         f"so the header and its origin prose are all that is left of closed "
                         f"work, in a register that carries OPEN work only: {label!r}"))
        stray = sorted({canon(b["id"]) for b in kids} - named)
        if stray:
            viol.append(("section-scope-drift",
                         f"(:{ln}) names {', '.join(sorted(named))} but {len(stray)} live "
                         f"{'entry' if len(stray) == 1 else 'entries'} beneath it "
                         f"{'is' if len(stray) == 1 else 'are'} outside that set "
                         f"({', '.join(stray)}) — extend the header's range, or move them: "
                         f"{label!r}"))

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
             "id-went-silent", "dangling-archive", "no-status", "closed-but-live",
             "status-disagrees-with-body", "orphaned-section", "section-scope-drift",
             "status-hygiene"]
    for kind in order:
        hits = [v for k, v in viol if k == kind]
        if hits:
            print(f"\n  {kind}  ({len(hits)})")
            for h in hits:
                print(f"    - {h}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
