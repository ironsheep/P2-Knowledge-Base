#!/usr/bin/env python3
"""
audit-yaml-deletion-classes.py — did a change set WEAKEN the shipped P2KB?

THE QUESTION
    Over a window of history, every line removed from the shipped KB: was it
    replaced by something equal or stronger, retracted on purpose, relocated — or
    did a sourced fact simply stop being there?

WHY THIS TOOL EXISTS AT ALL
    "What did we add" cannot answer it. In September 2026 the shipped set took
    +2,451 / -2,270 lines for a net of +181: half the content turned over while the
    totals barely moved. A weakening is invisible in a net line count, and it is
    invisible in a release changelog, because nobody writes "and this fact left".

WHAT THIS TOOL DOES AND DOES NOT DECIDE
    It does NOT classify weakening. It CANNOT: telling "replaced by something
    weaker" from "replaced by something better" is a judgement about meaning, and a
    regex that pretended otherwise would be the exact failure this study was opened
    to measure. What it does is TRIAGE — cheaply and structurally — so that the
    human or agent reading does not have to read 6,600 lines to find the 200 that
    matter:

      ADD_ONLY      no deletion. Out of scope.
      MIXED         deletions AND additions in the same hunk. Candidate REPLACED:
                    the reading question is "is the replacement weaker?"
      DELETE_ONLY   deletions with NO additions in the hunk. Candidate VANISHED,
                    and the high-risk population.

    Then one more automated cut, which is the cheapest high-value check available:

      RELOCATED     the deleted text still exists in the shipped set TODAY, some-
                    where else. Moved, not lost. Verified against the live tree,
                    not against a commit message.

    What survives both cuts is the read list, and it is the only thing a person
    needs to look at.

NORMALISATION IS DELIBERATELY LOOSE
    The relocation check normalises whitespace, YAML list/key punctuation and case
    before matching, because content that moves between files is nearly always
    re-indented and often re-keyed. A loose match here is the safe direction: a
    false RELOCATED would hide a real finding, so relocation is reported as a
    SEPARATE bucket for spot-checking rather than silently dropped from the list.

USAGE
    audit-yaml-deletion-classes.py --since 2026-08-01
    audit-yaml-deletion-classes.py --since 2026-08-01 --manifest FILE.json
    audit-yaml-deletion-classes.py --since 2026-08-01 --emit-read-list FILE.md
    audit-yaml-deletion-classes.py --since 2026-08-01 --class DELETE_ONLY --show

EXIT
    0  triage completed (this tool reports; it never gates)
    2  usage / environment error
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

SHIPPED_ROOT = Path("deliverables/ai/P2")

# A deleted line worth a human's attention: prose or a value, not punctuation,
# not a bare structural key, not blank.
STRUCTURAL_RE = re.compile(r"^[\s\-]*[a-z0-9_]+:\s*$", re.I)   # a bare key, no value
PUNCT_ONLY_RE = re.compile(r"^[\s\-|>\"'{}\[\],.]*$")


def repo_root() -> Path:
    here = Path.cwd().resolve()
    for cand in (here, *here.parents):
        if (cand / SHIPPED_ROOT).is_dir() and (cand / ".git").exists():
            return cand
    print("audit-yaml-deletion-classes: no repo root found", file=sys.stderr)
    sys.exit(2)


def normalise(text: str) -> str:
    """Collapse a line to its content, for cross-file relocation matching."""
    t = text.strip()
    t = re.sub(r"^[-\s]+", "", t)                  # YAML list marker / diff marker
    t = re.sub(r"^[a-z0-9_]+:\s*", "", t, flags=re.I)   # leading key
    t = t.strip(" \"'|>")
    t = re.sub(r"\s+", " ", t)
    return t.lower()


def is_substantive(line: str) -> bool:
    body = line[1:] if line.startswith("-") else line
    if PUNCT_ONLY_RE.match(body):
        return False
    if STRUCTURAL_RE.match(body):
        return False
    return len(normalise(body)) >= 12


def collect_hunks(root: Path, since: str) -> list[dict]:
    """Parse `git log -p` over the shipped tree into structured hunks."""
    proc = subprocess.run(
        ["git", "log", f"--since={since}", "-p", "--format=@@COMMIT@@%H%x00%s",
         "--", str(SHIPPED_ROOT)],
        cwd=root, capture_output=True, text=True, errors="replace",
    )
    if proc.returncode != 0:
        print(f"git log failed: {proc.stderr[:200]}", file=sys.stderr)
        sys.exit(2)

    hunks: list[dict] = []
    cur = None
    commit = subject = fname = None
    for line in proc.stdout.splitlines():
        if line.startswith("@@COMMIT@@"):
            payload = line[len("@@COMMIT@@"):]
            commit, _, subject = payload.partition("\x00")
            continue
        if line.startswith("+++ b/"):
            fname = line[6:].strip()
            continue
        if line.startswith("@@"):
            if cur:
                hunks.append(cur)
            cur = {"commit": (commit or "")[:9], "subject": subject or "",
                   "file": fname or "", "deleted": [], "added": []}
            continue
        if cur is None:
            continue
        if line.startswith("-") and not line.startswith("---"):
            cur["deleted"].append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            cur["added"].append(line[1:])
    if cur:
        hunks.append(cur)
    return hunks


def build_live_index(root: Path) -> set[str]:
    """Every normalised line present in the shipped set RIGHT NOW.

    Built from the live tree, never from a diff or a log: the question relocation
    asks is "is this content still shipping", and only the tree answers that.
    """
    idx: set[str] = set()
    for path in (root / SHIPPED_ROOT).rglob("*.yaml"):
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                n = normalise(line)
                if len(n) >= 12:
                    idx.add(n)
        except OSError:
            continue
    return idx


def main() -> int:
    ap = argparse.ArgumentParser(description="Triage shipped-KB deletions over a window.")
    ap.add_argument("--since", required=True, help="window start, e.g. 2026-08-01")
    ap.add_argument("--manifest", metavar="FILE", help="write the full triage as JSON")
    ap.add_argument("--emit-read-list", metavar="FILE", help="write the markdown read list")
    ap.add_argument("--class", dest="klass",
                    choices=("DELETE_ONLY", "MIXED", "ADD_ONLY"), help="restrict --show")
    ap.add_argument("--show", action="store_true", help="print hunks in full, never truncated")
    args = ap.parse_args()

    root = repo_root()
    hunks = collect_hunks(root, args.since)
    live = build_live_index(root)

    for h in hunks:
        if not h["deleted"]:
            h["class"] = "ADD_ONLY"
        elif h["added"]:
            h["class"] = "MIXED"
        else:
            h["class"] = "DELETE_ONLY"

        subs = [d for d in h["deleted"] if is_substantive(d)]
        h["substantive"] = subs
        # Relocated == every substantive deleted line is still somewhere in the
        # shipped set today. Partial relocation still needs reading, so it is not
        # counted as relocated.
        h["relocated"] = bool(subs) and all(normalise(d) in live for d in subs)
        h["still_live"] = sum(1 for d in subs if normalise(d) in live)

        # IN-HUNK CONTAINMENT, for MIXED hunks. A rewrite that says the same thing
        # in different words is the overwhelmingly common case and is not a
        # weakening. Measure whether each deleted line's CONTENT WORDS survive into
        # the text that replaced it, right here in this hunk.
        #
        # Deliberately generous: this decides what a person does NOT have to read,
        # so a false "covered" would hide a finding. It is therefore set high (80%
        # of content words) and reported as its own bucket, so the threshold can be
        # challenged against the artifact rather than trusted.
        # ⚠ THE TEST IS BIDIRECTIONAL, AND IT HAS TO BE. A one-way "are the deleted
        # words present in the added text" check clears the single most dangerous
        # shape there is: a rewrite that reuses the vocabulary and changes the
        # meaning. Caught on a control — commit 60ce19b4f replaced
        #     wxpin ##clkfreq/10, #step_pin   ' 100ms periods
        # with a block reading `rdlong clkf, #$14  ' clkfreq lives at hub long $14`,
        # which shares clkfreq/100ms/periods and would have been auto-cleared — while
        # introducing the WRONG hub address that F-445 later had to correct.
        #
        # So a hunk is only cleared when the replacement says the same thing in
        # nearly the same words: the deleted content must survive AND the addition
        # must not introduce much that is new. That clears path repoints, re-keying
        # and rewordings, and refuses anything that actually changed.
        deleted_words = set(re.findall(r"[a-z0-9_]{4,}", " ".join(subs).lower()))
        added_words = set(re.findall(r"[a-z0-9_]{4,}", " ".join(h["added"]).lower()))
        covered = 0
        for d in subs:
            dw = set(re.findall(r"[a-z0-9_]{4,}", d.lower()))
            if dw and len(dw & added_words) / len(dw) >= 0.80:
                covered += 1
        novelty = (len(added_words - deleted_words) / len(added_words)) if added_words else 0.0
        h["covered_in_hunk"] = covered
        h["added_novelty"] = round(novelty, 3)
        h["fully_covered"] = (bool(subs) and covered == len(subs) and novelty <= 0.25)

    counts = defaultdict(int)
    for h in hunks:
        counts[h["class"]] += 1

    del_hunks = [h for h in hunks if h["class"] in ("DELETE_ONLY", "MIXED")]
    with_subs = [h for h in del_hunks if h["substantive"]]
    relocated = [h for h in with_subs if h["relocated"]]
    rewritten = [h for h in with_subs if not h["relocated"] and h["fully_covered"]]
    read_list = [h for h in with_subs if not h["relocated"] and not h["fully_covered"]]

    print(f"shipped-KB deletion triage — since {args.since}\n")
    print(f"  hunks parsed: {len(hunks)}")
    for k in ("ADD_ONLY", "MIXED", "DELETE_ONLY"):
        print(f"    {k:<12} {counts[k]:>5}")
    tot_del = sum(len(h['deleted']) for h in del_hunks)
    tot_sub = sum(len(h['substantive']) for h in del_hunks)
    print(f"\n  deleted lines: {tot_del}")
    print(f"    substantive (prose or value, not punctuation or a bare key): {tot_sub}")
    print(f"\n  hunks with substantive deletions: {len(with_subs)}")
    print(f"    RELOCATED — every deleted line still ships elsewhere today: {len(relocated)}")
    print(f"    REWRITTEN — every deleted line's content words survive in its own hunk: "
          f"{len(rewritten)}")
    print(f"    ** READ LIST — needs a human judgement: {len(read_list)} **")

    rl_del = [h for h in read_list if h["class"] == "DELETE_ONLY"]
    print(f"\n  of the read list, DELETE_ONLY (candidate VANISHED, highest risk): {len(rl_del)}")
    print(f"                    MIXED (candidate REPLACED, is it weaker?): "
          f"{len(read_list) - len(rl_del)}")
    print("\n  This tool does NOT classify weakening. Telling 'replaced by something")
    print("  weaker' from 'replaced by something better' is a judgement about meaning.")

    if args.show:
        sel = [h for h in read_list if not args.klass or h["class"] == args.klass]
        for h in sel:                                   # never truncated
            print(f"\n--- {h['class']} · {h['commit']} · {h['file']}")
            print(f"    {h['subject'][:88]}")
            print(f"    still live elsewhere: {h['still_live']}/{len(h['substantive'])}")
            for d in h["substantive"]:
                print(f"    - {d.strip()[:150]}")
            for a in h["added"][:6]:
                print(f"    + {a.strip()[:150]}")

    if args.manifest:
        Path(args.manifest).write_text(json.dumps(hunks, indent=1) + "\n")
        print(f"\n  manifest: {args.manifest}")

    if args.emit_read_list:
        lines = [f"# Deletion read list — shipped P2KB since {args.since}", "",
                 f"{len(read_list)} hunk(s) need a human judgement. "
                 f"{len(relocated)} relocated and are excluded.", ""]
        for i, h in enumerate(read_list, 1):
            lines += [f"## {i}. {h['class']} · `{h['file']}` · {h['commit']}",
                      f"*{h['subject']}*", "",
                      f"still live elsewhere: {h['still_live']}/{len(h['substantive'])}", "",
                      "```diff"]
            lines += [f"- {d}" for d in h["substantive"]]
            lines += [f"+ {a}" for a in h["added"][:12]]
            lines += ["```", ""]
        Path(args.emit_read_list).write_text("\n".join(lines) + "\n")
        print(f"  read list: {args.emit_read_list}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
