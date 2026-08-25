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

EVERY CHECK IS PER-REGISTER, IN THAT REGISTER'S OWN VOCABULARY
    The ID families and the counter LABEL are read off the file being audited --
    `**Next finding ID: F-357**` in the corrections register, `**Next erratum ID:
    E-011**` in the ingestion errata register. Before 2026-08-25 both were
    hard-coded to `Next finding ID` / `F-`, so the errata register was invisible
    to every check below and its monotonic allocator was ungoverned (F-355). The
    fix was NOT to rename that counter to match: two registers claiming one
    allocator name is a worse defect than the one it closes.

CHECKS
    1  next-ID counter is ahead of every allocated ID      (allocation drift)
       -- for EVERY series the register declares, and a series that is allocated
          with no counter declared is itself a violation
    2  no finding ID appears as two entries                (protocol says: STOP)
    3  no CLOSED finding sits in a live open-work register (scan noise)
    4  every finding carries a status                      (unreadable state)
    4b prose claims "fixed" while the status does not       (status needs deciding)
       -- declare PENDING-VALIDATION when the fix IS applied and only its
          validation (a render, a release) is owed; that is a decision, not a dodge
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

    WIDENED 2026-08-25 («#302»), AND IT HAD NEVER FIRED. The matcher required
    `**Status:**` at column 0. The corrections register declares its verdict four
    other ways — indented under a bullet entry, inside a blockquote, bold or bare,
    and sometimes as `**Disposition.**`. Measured then: 20 status-declaration
    lines, 5 visible to this check, 15 invisible. Both live disagreements in the
    file were in the invisible 15 (F-355 headline `CONFIRMED` / body `RESOLVED`;
    F-347 headline `PENDING-VALIDATION` / disposition `PARTIAL`). The check
    designed to catch exactly that had been reporting CLEAN on three quarters of
    the bodies, and it had NO negative-control case, so nothing ever asked it to
    fail. It now has three (both failing spellings, plus an agreeing one so an
    over-eager matcher is caught on the other side).

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
import contextlib
import io
import os
import re
import subprocess
import sys

# Statuses appear backticked (`DONE`) and bare (DONE (2026-08-16) — ...). Match both,
# but only as whole words, so "RESOLVED" inside prose does not read as a status.
CLOSED_WORDS = ("DONE", "WONTFIX", "RESOLVED-INVALID")
# `RESEARCHING` is the ingestion errata register's middle lifecycle state
# (OPEN -> RESEARCHING -> RESOLVED | GAP). Its two neighbours are DELIBERATELY
# absent: `OPEN` and `GAP` are ordinary English in the corrections register's
# prose (8 whole-word uppercase occurrences today — "This file carries OPEN work
# only", "Recorded as a GAP, not restored"), and admitting them as status tokens
# would let a finding that carries NO status pass check 4 on a stray word. A
# vocabulary that silences a check is worse than one that is short.
STATUS_WORDS = CLOSED_WORDS + ("CONFIRMED", "NEEDS-VERIFICATION", "PARTIAL",
                               "PENDING-VALIDATION", "NOTED", "RESOLVED", "TRACKED",
                               "RESEARCHING")
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
# An explicitly-declared still-owed state vetoes both the embedded-DONE read
# ("manual DONE - KB DONE - one decision open" is PARTIAL) and the fixed-prose check.
# PENDING-VALIDATION exists because the register already HAD this state and no token
# for it: "a fix applied but not yet validated is NOT done". Nine findings carried
# `CONFIRMED` + "render owed" prose, so 4b fired on all nine, every run, forever --
# and a gate that reports nine things you are meant to ignore is training to ignore
# the gate. Naming the state makes it machine-readable and silences nothing real.
OWED_RE = re.compile(r"\b(PARTIAL|PENDING-VALIDATION)\b")
# A body-level status line. This is the finding's own considered verdict, written
# after the analysis; the headline is the scannable summary. When they disagree the
# register misreports itself to every reader who scans.
#
# EVERY SPELLING THE REGISTER ACTUALLY USES, not just the one this pattern started
# with (widened 2026-08-25, «#302»). It matched `**Status:**` at column 0 only, and
# the corrections register writes its verdict four other ways: indented under a
# bullet entry (`  Status: `RESOLVED``), inside a blockquote (`> Status: …`), bold
# or bare, and occasionally as `**Disposition.**`. Measured at the time of the
# widening: **20 status-declaration lines, of which check 10 could see 5.** The 15
# it could not see included both live disagreements in the file — F-355 (headline
# `CONFIRMED`, body `RESOLVED`) and F-347 (headline `PENDING-VALIDATION`,
# disposition `PARTIAL`) — so the check that exists precisely to catch a headline
# out of step with its body had been blind to three quarters of the bodies.
# A check that cannot fail has not been verified, it has been RUN.
BODY_STATUS = re.compile(
    r"^[ \t>]*(?:\*\*)?(?:Status:|Disposition\.)(?:\*\*)?[ \t]*`?\s*([A-Z][A-Z-]*)", re.M)


def lead_status(s):
    """The first status token in a string, or None."""
    m = STATUS_RE.search(s)
    if not m:
        return None
    return (m.group(1) or m.group(0)).strip("` ")

# THE SERIES A REGISTER ALLOCATES ARE READ OFF THE REGISTER, NOT HARD-CODED.
#
# This tool knew exactly two letters, `F` and `G`, and one counter spelling,
# `**Next finding ID: F-NNN**`. So `engineering/ingestion/SOURCE-ERRATA.md` --
# which declares `**Next erratum ID: `E-011`**` and allocates `E-NNN` -- was
# invisible to every check here: counter drift, duplicate IDs, orphaned section
# headers, unaccounted coverage, all simply absent for it (F-355). The whole
# reason this project re-checks the next-ID before every dispatch is that two
# agents allocating from a stale number collide silently, and that register is a
# live input to every ingestion.
#
# The fix is NOT to rename that register's counter to `Next finding ID:` -- two
# registers claiming one allocator name is a worse defect than the one it closes.
# It is to take (label, prefix) FROM THE FILE: the counter line declares both,
# and the ID shapes are built from the series actually present. A register that
# introduces a third family is covered on the day it is written.
COUNTER_RE = re.compile(r"\*\*Next\s+(\w+)\s+ID:\s*`?([A-Z])-0*(\d+)`?\*\*")
_ENTRY_HEAD = (r"^(?:#{2,4}\s+(<P>-\d+[a-z]?)\s*[—-]"
               r"|-\s+\*\*(<P>-\d+[a-z]?)\s+[—-])")


def series_in(text, declared=None):
    """Every ID family a register uses: the one its counter declares, plus any
    that actually HEAD an entry. Restricted to letters seen in those two
    positions, so a stray `P-2` in prose cannot invent a family."""
    found = set(declared or ())
    found.update(re.findall(r"^#{2,4}\s+([A-Z])-\d+", text, re.M))
    found.update(re.findall(r"^-\s+\*\*([A-Z])-\d+\s+[—-]", text, re.M))
    return found or {"F"}


def build_id_res(series):
    """(FINDING_START, ID_RANGE, ID_ONE) for one register's series set.

    `#{2,4}`, not `#{3,4}`: the corrections register heads a finding with `###`,
    the errata register with `##`. An entry heading is tested BEFORE a section
    heading (see parse), so `## E-001 -- ...` reads as a finding rather than a
    section -- which is what lets checks 8 and 9 work on both files."""
    cls = "[" + "".join(sorted(series)) + "]"
    return (re.compile(_ENTRY_HEAD.replace("<P>", cls)),
            re.compile(r"\b(" + cls + r")-0*(\d+)\s*(?:…|\.{3})\s*" + cls + r"-0*(\d+)\b"),
            re.compile(r"\b(" + cls + r")-0*(\d+)\b"),
            # Guardrail IDs are matched WHOLE, letter suffix included: the
            # register retains `F-114b` as a do-not-re-file guardrail, and an ID
            # regex that drops the `b` stops exempting it -- which reads as a
            # brand-new unaccounted finding.
            re.compile(r"\b" + cls + r"-\d+[a-z]?\b"))


# Defaults, replaced per-register in main() once the file has been read. The
# corrections register's two families (F-### corrections, G-### gap/enrichment)
# stay SEPARATE NUMBER SPACES: counted, gap-checked and reported apart, never
# merged into one range. G was absent from this tool until 2026-08-21, which made
# every G finding invisible to every check -- G-004 sat live and `DONE` through a
# sweep looking for exactly that.
FINDING_START, ID_RANGE, ID_ONE, GUARD_RE = build_id_res({"F", "G"})

# A `##` section header, not a finding entry.
SECTION_START = re.compile(r"^##\s+(?!#)")


def canon(fid):
    """'G-004' -> 'G-4'; 'F-302' -> 'F-302'. Strips padding and any letter suffix.

    ANY single-letter series, not just F and G. While this hard-coded `[FG]` the
    errata register's `E-001` fell through unchanged, so the canonical live set
    held `E-001` while the gap scan looked for `E-1` — and all ten entries were
    reported as "went silent" while sitting in plain view. A canonicaliser that
    silently declines to canonicalise is worse than one that raises."""
    m = re.match(r"([A-Z])-0*(\d+)", fid)
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
    starts = [i for i, ln in enumerate(lines, 1)
              if SECTION_START.match(ln) and not FINDING_START.match(ln)]
    out = []
    for k, i in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else len(lines) + 1
        header = lines[i - 1]
        if not header_ids(header):
            continue                     # a generic header claims nothing; nothing to drift
        out.append((i, header, [b for b in blocks if i < b["line"] < end]))
    return out


def parse(path, finding_start=None):
    """Split a register into (id, headline, body, line_no) blocks."""
    finding_start = finding_start or FINDING_START
    lines = open(path, encoding="utf-8").read().splitlines()
    blocks, cur = [], None
    for i, ln in enumerate(lines, 1):
        m = finding_start.match(ln)
        if m:
            fid = m.group(1) or m.group(2)
            if cur:
                blocks.append(cur)
            cur = {"id": fid, "line": i, "headline": ln, "body": [ln]}
        elif SECTION_START.match(ln):
            # A new `##` section ENDS the finding above it. Without this a block ran
            # on until the next finding and absorbed whatever lay between -- which is
            # how F-283 passed the status check for months: it carries `FIXED`, which
            # is not a status token, and borrowed the word TRACKED out of the heading
            # "## Open -- TRACKED in the ingestion head" two sections below it.
            if cur:
                blocks.append(cur); cur = None
        elif cur:
            cur["body"].append(ln)
    if cur:
        blocks.append(cur)
    return lines, blocks


def scannable_head(block):
    """The whole headline a reader scans, not just its first physical line.

    A `###` finding heading is one line and is returned unchanged. A bullet-form
    entry (`- **F-357 — …**  — `RESOLVED``) routinely WRAPS, and the register puts
    the status token at the end of the bold lead-in -- which lands on line 2, 3 or
    4. Everything above read `block["headline"]`, i.e. line 1 only, so for a wrapped
    entry the headline status was simply absent: `lead_status` returned None, check
    10 skipped the entry entirely, and 4b had nothing to test.

    That is the OTHER half of the check-10 blind spot found 2026-08-25 («#302»).
    F-355 carried `CONFIRMED` on line 2 of its headline and `RESOLVED` in its body:
    invisible on the body side (column-0-only matcher) AND invisible on the headline
    side (line-1-only read). Widening only one of the two would have left the
    disagreement undetected and the fix falsely reported as complete.

    The lead-in ends where its bold closes, so accumulate lines until the `**`
    markers balance."""
    lines_ = block["body"]
    if not lines_ or not lines_[0].lstrip().startswith("-"):
        return block["headline"]
    acc = []
    for ln in lines_:
        acc.append(ln)
        joined = " ".join(acc)
        if joined.count("**") >= 2 and joined.count("**") % 2 == 0:
            break
    return " ".join(acc)


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
            ids.update(GUARD_RE.findall(ln))
    return ids



def negative_control():
    """A check that cannot fail has not been verified, it has been RUN.

    Every case below is a register defect this tool exists to catch, built as a
    throwaway file and fed through the real `parse`/`series_in`/counter path --
    not through a re-implementation, which would prove only that the copy agrees
    with itself."""
    import tempfile
    print("NEGATIVE CONTROL -- proving the gate can fail, on both register dialects\n")
    ok = True
    cases = [
        # Numbered from 1 with no archive: check 6 (no allocated ID went silent)
        # is real, and a fixture starting at F-299 with nothing archived is a
        # register with 298 genuinely missing IDs, not a clean one.
        ("corrections dialect, counter AHEAD — MUST BE CLEAN",
         "> **Next finding ID: `F-002`**\n\n"
         "## A section — F-001\n\n### F-001 — a thing · `CONFIRMED`\n\nbody\n", False),
        ("corrections dialect, counter BEHIND — MUST FAIL",
         "> **Next finding ID: `F-001`**\n\n"
         "## A section — F-001\n\n### F-001 — a thing · `CONFIRMED`\n\nbody\n", True),
        ("errata dialect, counter AHEAD — MUST BE CLEAN",
         "> **Next erratum ID: `E-003`**\n\n"
         "## E-001 — a thing · `RESOLVED`\n\nbody\n"
         "## E-002 — another · `RESEARCHING`\n\nbody\n", False),
        ("errata dialect, counter BEHIND — MUST FAIL",
         "> **Next erratum ID: `E-002`**\n\n"
         "## E-001 — a thing · `RESOLVED`\n\nbody\n"
         "## E-002 — another · `RESEARCHING`\n\nbody\n", True),
        ("errata dialect, NO counter at all — MUST FAIL",
         "## E-001 — a thing · `RESOLVED`\n\nbody\n", True),
        ("a series allocated with no counter declared — MUST FAIL",
         "> **Next finding ID: `F-002`**\n\n"
         "### F-001 — a thing · `CONFIRMED`\n\nbody\n"
         "### D-001 — an open question · `CONFIRMED`\n\nbody\n", True),
        ("an entry carrying no status token — MUST FAIL",
         "> **Next erratum ID: `E-002`**\n\n## E-001 — a thing\n\nbody\n", True),
        ("a duplicate ID — MUST FAIL",
         "> **Next erratum ID: `E-002`**\n\n"
         "## E-001 — a thing · `RESOLVED`\n\nbody\n"
         "## E-001 — again · `RESOLVED`\n\nbody\n", True),
        # CHECK 10 HAD NO CONTROL AT ALL, which is how its column-0-only matcher
        # stayed blind through two live disagreements (F-355, F-347). These three
        # pin the widened matcher: the two spellings the register actually uses
        # must FAIL when they contradict the headline, and must stay CLEAN when
        # they agree -- an over-eager matcher is the failure mode on the other side.
        ("check 10, INDENTED `Status:` disagreeing with the headline — MUST FAIL",
         "> **Next finding ID: `F-002`**\n\n"
         "## A section — F-001\n\n"
         "- **F-001 — a thing.** — `CONFIRMED`\n\n  body\n\n  Status: `RESOLVED`\n", True),
        ("check 10, blockquoted `**Disposition.**` disagreeing — MUST FAIL",
         "> **Next finding ID: `F-002`**\n\n"
         "## A section — F-001\n\n"
         "- **F-001 — a thing.** — `PENDING-VALIDATION`\n\n  body\n\n"
         "> **Disposition.** `PARTIAL` — the rest is owed.\n", True),
        ("check 10, indented `Status:` AGREEING with the headline — MUST BE CLEAN",
         "> **Next finding ID: `F-002`**\n\n"
         "## A section — F-001\n\n"
         "- **F-001 — a thing.** — `PARTIAL`\n\n  body\n\n  Status: `PARTIAL` — rest owed.\n", False),
        # THE OTHER HALF OF THE SAME BLIND SPOT. A wrapped bullet headline puts its
        # status token on line 2+, and the checks read line 1 only -- so F-355 was
        # invisible on the headline side as well as the body side, and widening
        # either one alone would have left it undetected while reporting the fix
        # complete. `scannable_head` reads the whole bold lead-in; this pins it.
        ("check 10, WRAPPED headline whose status is on line 2 — MUST FAIL",
         "> **Next finding ID: `F-002`**\n\n"
         "## A section — F-001\n\n"
         "- **F-001 — a thing whose headline wraps onto\n"
         "  a second line where the status lives.** — `CONFIRMED`\n\n"
         "  body\n\n  Status: `RESOLVED`\n", True),
    ]
    for label, text, want_fail in cases:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as fh:
            fh.write(text)
            path = fh.name
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = _audit_register(path, [], quiet=True, sweep_rev=None, extra_series=[])
        os.unlink(path)
        good = (rc != 0) == want_fail
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label}: exit={rc}")

    # "The file was not examined at all" must be a DISTINCT non-zero exit, not a
    # pass and not an ordinary violation -- the standing lesson from the
    # digit-density gate, which shipped able to exit 0 having measured nothing.
    missing = os.path.join(tempfile.gettempdir(), "no-such-register-negative-control.md")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = main_on(missing)
    good = rc == 2
    ok &= good
    print(f"  [{'PASS' if good else 'FAIL'}] an unreadable register exits 2, "
          f"distinct from a violation: exit={rc}")

    print("\n" + ("Negative control PASSED -- the gate fails on a stale counter, an "
                   "undeclared allocator, a missing status and a duplicate ID, in BOTH "
                   "register dialects, and refuses to pass a file it never read."
                   if ok else "Negative control FAILED -- do not trust this run."))
    return 0 if ok else 1


def main_on(register):
    """Run the gate on one path exactly as the CLI would. Used by the control so
    the control exercises the shipped entry point, not a copy of it."""
    if not os.path.isfile(register):
        return 2
    return _audit_register(register, [], quiet=True, sweep_rev=None, extra_series=[])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("register", nargs="?",
                    help="the register to audit (omit only with --negative-control)")
    ap.add_argument("--archive", action="append", default=[],
                    help="archive file holding closed findings (repeatable); "
                         "default: read them from the register header")
    ap.add_argument("--quiet", action="store_true", help="print violations + summary only")
    ap.add_argument("--series", action="append", default=[], metavar="LETTER",
                    help="an ID family this register allocates that has no entries "
                         "and no counter yet (repeatable). Series are normally read "
                         "off the register itself; this is for a family declared "
                         "before its first filing.")
    ap.add_argument("--negative-control", action="store_true",
                    help="prove the tool can fail; audits no register")
    ap.add_argument("--sweep-check", metavar="REV",
                    help="prove an archive sweep lost nothing: every substantive line of the "
                         "register AT REV must still exist in the live file or an archive. "
                         "Reads REV from git, independently of whatever did the sweep. "
                         "RUN IT AT SWEEP TIME, against the pre-sweep commit, with nothing "
                         "else changed — run retrospectively it reports every later in-place "
                         "rewrite as unaccounted, which is churn, not loss.")
    args = ap.parse_args()

    if args.negative_control:
        return negative_control()
    if not args.register:
        ap.error("a register path is required unless --negative-control is given")

    return _audit_register(args.register, args.archive, quiet=args.quiet,
                           sweep_rev=args.sweep_check, extra_series=args.series)


def _audit_register(register, archive_paths, quiet=False, sweep_rev=None,
                    extra_series=None):
    """The whole gate, on one register. `main` is a thin CLI over this so the
    negative control can drive the SHIPPED path rather than a copy of it."""
    class _A:
        pass
    args = _A()
    args.register = register
    args.archive = list(archive_paths or [])
    args.quiet = quiet
    args.sweep_check = sweep_rev
    args.series = list(extra_series or [])

    reg = args.register
    if not os.path.isfile(reg):
        print(f"ERROR  {reg}: not a readable file — the register was NOT examined. "
              f"That is a tooling failure, never a pass.")
        return 2

    # Read the register's OWN allocator vocabulary before parsing it (F-355).
    # `**Next finding ID: F-357**` and `**Next erratum ID: `E-011`**` are two
    # legitimate spellings of the same contract; a tool that knows only the first
    # reports nothing at all about the second, which is how the errata register
    # ended up with an ungoverned monotonic allocator.
    global FINDING_START, ID_RANGE, ID_ONE, GUARD_RE
    raw = open(reg, encoding="utf-8").read()
    counters = {p: (label, int(n)) for label, p, n in COUNTER_RE.findall(raw)}
    FINDING_START, ID_RANGE, ID_ONE, GUARD_RE = build_id_res(
        series_in(raw, declared=set(counters) | set(args.series or ())))

    lines, blocks = parse(reg, FINDING_START)
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
        archived_ids.update(f"{p}-{int(n)}" for p, n in ID_ONE.findall(
            open(a, encoding="utf-8", errors="replace").read()))
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
    # Each series is its own number space. EVERY counter the register declares is
    # checked, in whatever label it uses -- so `Next erratum ID: E-011` is
    # governed exactly as `Next finding ID: F-357` is.
    live_by_series = {}
    for fid in seen:
        pre, n = canon(fid).split("-")
        live_by_series.setdefault(pre, set()).add(int(n))
    if not counters:
        viol.append(("no-counter",
                     "register declares no `**Next <thing> ID: X-NNN**` line — its "
                     "allocator is ungoverned and two filers will collide silently"))
    for pre, (label, nxt) in sorted(counters.items()):
        nums = sorted(live_by_series.get(pre, set()))
        if not nums:
            say(f"next-ID counter   : {pre}-{nxt} (`Next {label} ID`; no live "
                f"{pre}- entries)")
            continue
        top = max(nums)
        say(f"next-ID counter   : {pre}-{nxt} (`Next {label} ID`; highest "
            f"allocated {pre}-{top})")
        if nxt <= top:
            viol.append(("counter-behind",
                         f"counter reads {pre}-{nxt} but {pre}-{top} is already "
                         f"allocated — the next filing collides"))
    ungoverned = sorted(set(live_by_series) - set(counters))
    if ungoverned:
        viol.append(("no-counter",
                     f"register allocates {', '.join(f'{p}-NNN' for p in ungoverned)} "
                     f"but declares no counter for {'it' if len(ungoverned) == 1 else 'them'} "
                     f"— that allocator is ungoverned"))

    # --- 3 + 4: closed-but-live, and missing status -----------------------------
    closed_live = []
    for b in blocks:
        if b["id"] in guards:
            continue
        body = "\n".join(b["body"])
        if not STATUS_RE.search(body):
            viol.append(("no-status", f"{b['id']} (:{b['line']}) carries no status token"))
        head = scannable_head(b)

        # --- 10: the scannable layer must agree with the authoritative one ------
        body_tokens = {t for t in BODY_STATUS.findall(body) if t in STATUS_WORDS}
        head_token = lead_status(head)
        if body_tokens and head_token and head_token not in body_tokens:
            viol.append(("status-disagrees-with-body",
                         f"{b['id']} (:{b['line']}) headline reads {head_token} but its own "
                         f"Status/Disposition line reads {'/'.join(sorted(body_tokens))} — a reader "
                         f"scanning headlines gets the wrong answer; reconcile the two, and if "
                         f"the body is right the headline is what needs rewriting"))

        if OWED_RE.search(head):
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
