#!/usr/bin/env python3
"""Decide the DEBUG_TIMESTAMP verdict of e3-debug-timestamp-test.spin2 from its log.

P2 Errata, Erratum E3 -- an example from the manual's examples archive (Appendix A).
The test program cannot read its own stamps: the debugger adds them to each DEBUG
message on its way to the terminal. So the program decides whether the stale window
was where the test needs it, and this script, run on the saved log, decides what the
stamps show:

    python3 e3-debug-timestamp-verdict.py <saved DEBUG log>

The rules below were fixed before the test ran.

Input: a pnut-term-ts debug log (or a raw capture).  Every DEBUG line the test sends is
expected as
    [host time] CogN  $HHHH_HHHH_LLLL_LLLL  <text>
where $HHHH_HHHH_LLLL_LLLL is the DEBUG_TIMESTAMP stamp (the host-time prefix is optional;
the format is the v55 debugger's: cognout "CogN  ", hexout "$" + 8 digits with "_" after
the fourth, "_", hexout_digits, "  ").

The test sends, per pair id:
    Cog0 ... REF id=<id> b pay_hi=$XXXX_XXXX pay_lo=$XXXX_XXXX   (cog 0, before)
    CogP ... PRB id=<id> pay_hi=$XXXX_XXXX pay_lo=$XXXX_XXXX     (the probe)
    Cog0 ... REF id=<id> a pay_hi=... pay_lo=...                 (cog 0, after)
    Cog0 ... PAIR id=<id> <LABEL> valid=1 p<n> D=<d>             (the program's own check)
Only pairs the program marked valid=1 are judged.

Per pair:
    COG         both REF lines from cog 0; the PRB line from the label's probe cog
                (C* = 1, B4*/X4* = 4, B7*/X7* = 7)
    Dpay        REF(b) payload hi - PRB payload hi (32-bit): the window, recomputed here
                from the payloads (the program's own D is not trusted as text)
    SELF(line)  stamp64 - payload64 in [-SLACK, TOL_T): the stamp is the sending cog's own
                counter copy, read at the message (SLACK covers the debugger's 62-clock trim
                against a payload read a few clocks before the BRK, in PASM)
    STALE(PRB)  stamp64 - payload64 in [2^32 - SLACK, 2^32 + TOL_T): the stamp is one wrap
                LATER than the cog's own (stale) counter copy -- i.e. current
    Dts         REF(b) stamp hi - PRB stamp hi   (32-bit)
    LO-ORDER    REF(b) stamp hi == REF(a) stamp hi and
                REF(b) stamp lo < PRB stamp lo < REF(a) stamp lo  (unsigned): the lower long
                of every stamp is current
    ORDER       REF(b) stamp64 < PRB stamp64 < REF(a) stamp64: the stamps are in the order
                the lines were sent

Readings (labels): C0 C1E C1L C2E = cog 1, group 0 (control); B4E B4L = cog 4 Spin2 and
B7E B7L = cog 7 PASM2 in the stale window; X4E X7E = the same cogs after it closed.

RIG FAIL (no verdict):
    no stamped line at all (the terminal did not pass the stamp through)
    the program printed a RIG FAIL or HALTED line, or no VERDICT WINDOW line
    a reading with fewer than MIN_PAIRS judged pairs, or a valid pair with a line missing
    any pair: COG fails, a REF line fails SELF, or LO-ORDER fails
    a control pair: Dpay <> 0, SELF(PRB) fails, Dts <> 0, or ORDER fails
NO VERDICT (window): the program's VERDICT WINDOW line is not AS NEEDED, or Dpay is not 1
    in every window pair and 0 in every closed pair: the silicon did not give the window the
    stamps must be judged in
Verdicts, per probe kind (Spin2 cog 4, PASM2 cog 7):
    AFFECTED       every window pair: Dts = 1 and SELF(PRB); every closed pair: Dts = 0 and
                   SELF(PRB).  The count of window pairs that fail ORDER is printed
                   (predicted: all)
    NOT AFFECTED   every window pair: Dts = 0 and STALE(PRB); every closed pair: Dts = 0 and
                   SELF(PRB)
    INCONCLUSIVE   anything else (printed)
"""

import re
import sys

TOL_T = 200_000          # clocks: a stamp read within 1 ms (at 200 MHz) after its payload
SLACK = 256              # clocks: a stamp may read up to this much BEFORE its payload
MIN_PAIRS = 10           # valid pairs per reading, as the program takes
WRAP = 1 << 32

CONTROL = ["C0", "C1E", "C1L", "C2E"]
WINDOW = {"Spin2 debug() (cog 4)": ["B4E", "B4L"], "PASM2 DEBUG (cog 7)": ["B7E", "B7L"]}
CLOSED = {"Spin2 debug() (cog 4)": ["X4E"], "PASM2 DEBUG (cog 7)": ["X7E"]}
PROBE_COG = {"C0": 1, "C1E": 1, "C1L": 1, "C2E": 1,
             "B4E": 4, "B4L": 4, "X4E": 4, "B7E": 7, "B7L": 7, "X7E": 7}

STAMP_RE = re.compile(
    r"Cog(?P<cog>[0-7])\s+\$(?P<h1>[0-9A-Fa-f]{4})_(?P<h2>[0-9A-Fa-f]{4})_"
    r"(?P<l1>[0-9A-Fa-f]{4})_(?P<l2>[0-9A-Fa-f]{4})\s+(?P<text>.*)$")
PAY_RE = re.compile(r"pay_hi=\$(?P<ph>[0-9A-Fa-f_]+)\s+pay_lo=\$(?P<pl>[0-9A-Fa-f_]+)")
REF_RE = re.compile(r"^REF id=(?P<id>[\d_]+) (?P<side>[ab]) ")
PRB_RE = re.compile(r"^PRB id=(?P<id>[\d_]+) ")
PAIR_RE = re.compile(r"^PAIR id=(?P<id>[\d_]+) (?P<label>\w+) valid=1 ")


def hexval(text):
    return int(text.replace("_", ""), 16)


def idval(text):
    return int(text.replace("_", ""))


def parse(path):
    """Return (refs, prbs, pairs, window_line, stamped_lines, program_fail_lines)."""
    refs, prbs, pairs = {}, {}, {}
    window_line = None
    stamped = 0
    fails = []
    with open(path, encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if "VERDICT WINDOW:" in line:
                window_line = line[line.index("VERDICT WINDOW:"):]
            if "RIG FAIL:" in line or "HALTED" in line:
                fails.append(line)
            match = STAMP_RE.search(line)
            if not match:
                continue
            stamped += 1
            text = match["text"].strip()
            pay = PAY_RE.search(text)
            entry = None
            if pay:
                entry = {"cog": int(match["cog"]),
                         "sh": hexval(match["h1"] + match["h2"]),
                         "sl": hexval(match["l1"] + match["l2"]),
                         "ph": hexval(pay["ph"]), "pl": hexval(pay["pl"])}
            ref = REF_RE.match(text)
            prb = PRB_RE.match(text)
            pair = PAIR_RE.match(text)
            if ref and entry:
                refs[(idval(ref["id"]), ref["side"])] = entry
            elif prb and entry:
                prbs[idval(prb["id"])] = entry
            elif pair:
                pairs.setdefault(pair["label"], []).append(idval(pair["id"]))
    return refs, prbs, pairs, window_line, stamped, fails


def stamp_minus_pay(entry):
    return (((entry["sh"] << 32) | entry["sl"]) - ((entry["ph"] << 32) | entry["pl"]))


def self_ok(entry):
    return -SLACK <= stamp_minus_pay(entry) < TOL_T


def stale_ok(entry):
    return WRAP - SLACK <= stamp_minus_pay(entry) < WRAP + TOL_T


def judge_pair(pid, label, refs, prbs):
    """Return a dict for one pair, or None if a line is missing."""
    before, after, prb = refs.get((pid, "b")), refs.get((pid, "a")), prbs.get(pid)
    if before is None or after is None or prb is None:
        return None
    stamp64 = [(e["sh"] << 32) | e["sl"] for e in (before, prb, after)]
    return {
        "id": pid,
        "cog": prb["cog"],
        "cog_ok": before["cog"] == 0 and after["cog"] == 0 and prb["cog"] == PROBE_COG[label],
        "dpay": (before["ph"] - prb["ph"]) % WRAP,
        "self_ref": self_ok(before) and self_ok(after),
        "self_prb": self_ok(prb),
        "stale_prb": stale_ok(prb),
        "dts": (before["sh"] - prb["sh"]) % WRAP,
        "lo_order": before["sh"] == after["sh"] and before["sl"] < prb["sl"] < after["sl"],
        "order": stamp64[0] < stamp64[1] < stamp64[2],
        "prb_stamp": f"${prb['sh']:08X}_{prb['sl']:08X}",
        "prb_pay": f"${prb['ph']:08X}_{prb['pl']:08X}",
        "ref_stamp": f"${before['sh']:08X}_{before['sl']:08X}",
    }


def main():
    if len(sys.argv) != 2:
        print("usage: e3-debug-timestamp-verdict.py <debug log>")
        return 2
    refs, prbs, pairs, window_line, stamped, fails = parse(sys.argv[1])
    print(f"stamped DEBUG lines found: {stamped}")
    if stamped == 0:
        print("RIG FAIL: no line carries a $HHHH_HHHH_LLLL_LLLL stamp after CogN -- the terminal "
              "did not pass the stamp through (a rig finding, not a verdict)")
        return 1

    rig_bad = False
    for line in fails:
        print(f"RIG FAIL (program): {line}")
        rig_bad = True

    judged = {}
    labels = CONTROL + [l for ls in WINDOW.values() for l in ls] + [l for ls in CLOSED.values() for l in ls]
    for label in labels:
        results = [judge_pair(pid, label, refs, prbs) for pid in pairs.get(label, [])]
        missing = sum(1 for r in results if r is None)
        results = [r for r in results if r is not None]
        judged[label] = results
        print(f"{label}: {len(results)} valid pairs (missing lines {missing}); "
              f"Dpay {sorted({r['dpay'] for r in results})}; Dts {sorted({r['dts'] for r in results})}; "
              f"COG {sum(r['cog_ok'] for r in results)}/{len(results)}, "
              f"SELF ref {sum(r['self_ref'] for r in results)}/{len(results)}, "
              f"SELF prb {sum(r['self_prb'] for r in results)}/{len(results)}, "
              f"STALE prb {sum(r['stale_prb'] for r in results)}/{len(results)}, "
              f"LO-ORDER {sum(r['lo_order'] for r in results)}/{len(results)}, "
              f"ORDER {sum(r['order'] for r in results)}/{len(results)}")
        for r in results:
            print(f"    id {r['id']} cog {r['cog']}: REF(b) stamp {r['ref_stamp']}  PRB stamp "
                  f"{r['prb_stamp']} pay {r['prb_pay']}  Dpay {r['dpay']} Dts {r['dts']}  "
                  f"self {int(r['self_prb'])} stale {int(r['stale_prb'])} lo-order "
                  f"{int(r['lo_order'])} order {int(r['order'])}")
        if len(results) < MIN_PAIRS or missing:
            print(f"RIG FAIL: {label} has {len(results)} judged pairs ({missing} with a line "
                  f"missing); need {MIN_PAIRS}")
            rig_bad = True
        if not all(r["cog_ok"] for r in results):
            print(f"RIG FAIL: {label}: a REF line not from cog 0, or a PRB line not from cog "
                  f"{PROBE_COG[label]}")
            rig_bad = True
        if not all(r["self_ref"] for r in results):
            print(f"RIG FAIL: {label}: a REF line's stamp is not its own payload + [-{SLACK}, {TOL_T})")
            rig_bad = True
        if not all(r["lo_order"] for r in results):
            print(f"RIG FAIL: {label}: a stamp's lower long fell outside cog 0's two (LO-ORDER)")
            rig_bad = True
        if label in CONTROL and not all(r["dpay"] == 0 and r["self_prb"] and r["dts"] == 0
                                        and r["order"] for r in results):
            print(f"RIG FAIL: control {label}: expected Dpay 0, SELF, Dts 0 and ORDER in every pair")
            rig_bad = True

    if window_line is None:
        print("RIG FAIL: the program printed no VERDICT WINDOW line")
        rig_bad = True
    if rig_bad:
        print("NO VERDICT: rig failed (see RIG FAIL lines)")
        return 1

    print(window_line)
    win_all = [r for ls in WINDOW.values() for l in ls for r in judged[l]]
    closed_all = [r for ls in CLOSED.values() for l in ls for r in judged[l]]
    if (not window_line.startswith("VERDICT WINDOW: AS NEEDED")
            or not all(r["dpay"] == 1 for r in win_all)
            or not all(r["dpay"] == 0 for r in closed_all)):
        print("NO VERDICT (window): the silicon did not give the window the stamps must be judged "
              f"in (window Dpay {sorted({r['dpay'] for r in win_all})}, closed Dpay "
              f"{sorted({r['dpay'] for r in closed_all})}, program: {window_line!r})")
        return 1

    for kind, kind_labels in WINDOW.items():
        win = [r for l in kind_labels for r in judged[l]]
        closed = [r for l in CLOSED[kind] for r in judged[l]]
        closed_ok = all(r["dts"] == 0 and r["self_prb"] for r in closed)
        out_of_order = sum(1 for r in win if not r["order"])
        if all(r["dts"] == 1 and r["self_prb"] for r in win) and closed_ok:
            print(f"VERDICT DEBUG_TIMESTAMP, {kind}: AFFECTED - every stamp sent in the window is "
                  f"the cog's own stale counter, one wrap early (Dts 1 in {len(win)} of {len(win)} "
                  f"pairs; {out_of_order} of {len(win)} printed earlier than the REF line sent "
                  f"before them); current after the closing wrap (Dts 0 in {len(closed)} of "
                  f"{len(closed)})")
        elif all(r["dts"] == 0 and r["stale_prb"] for r in win) and closed_ok:
            print(f"VERDICT DEBUG_TIMESTAMP, {kind}: NOT AFFECTED - every stamp sent in the window is "
                  f"current (Dts 0 in {len(win)} of {len(win)} pairs), one wrap later than the "
                  f"cog's own stale GETCT WC")
        else:
            print(f"VERDICT DEBUG_TIMESTAMP, {kind}: INCONCLUSIVE - window Dts "
                  f"{sorted({r['dts'] for r in win})}, SELF {sum(r['self_prb'] for r in win)}/"
                  f"{len(win)}, STALE {sum(r['stale_prb'] for r in win)}/{len(win)}; closed Dts "
                  f"{sorted({r['dts'] for r in closed})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# ---------------------------------------------------------------------------
#  MIT License -- Copyright (c) 2026 Iron Sheep Productions, LLC
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED. See the repository LICENSE file for the full text.
# ---------------------------------------------------------------------------
