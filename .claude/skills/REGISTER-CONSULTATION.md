# Consulting a tracking register — the protocol

**Stated once here. Overlays point at this file; none of them restate it** — a restated rule
drifts from its original, which is the exact defect this protocol exists to prevent.

Applies to every **tracking register** in this repo: `P2KB-CORRECTION-FINDINGS.md`,
`PUBLICATION-ROSTER.md`, the ingestion dashboard, the punch lists, `VERIFICATION-OPPORTUNITIES.md`,
`P2-EMPIRICAL-FINDINGS.md`.

Origin: 2026-08-15. An 18-task sprint was generated from a superseded plan section while the
register held the current answers, and a KB defect already filed as F-264 was re-derived from
scratch. Every rule below is one of the specific things that went wrong.

---

## 1. Status before content — and quote it

**Read the finding's status field before its body.** The body is the argument; the status is
whether the argument is still live. In `P2KB-CORRECTION-FINDINGS.md` the status sits at the
**end** of a finding, so a top-down read of the body reaches a conclusion before it reaches the
line that invalidates it.

**Evidence requirement:** you may not cite a finding without also citing **its status and its line
number**. `F-264` is not a citation. `F-264 (NOTED — resolution deferred, :3130)` is.

If that costs you nothing, the rule cost nothing. If you cannot produce it, you had not read the
status — which is the case this rule exists for.

## 2. A finding ID appearing twice is a STOP

If a finding ID resolves to **more than one entry**, do not choose between them, do not prefer the
later one, and do not proceed. **The duplicate is itself a finding about the register.** Surface it
to {{USER_NAME}} and stop work that depends on it.

Live example, unresolved as of 2026-08-15: `F-260` carries `NEEDS-VERIFICATION (silicon)` at
`:2926` and `RESOLVED ON THE BENCH` at `:3035`.

Corollary — **a register entry that opens by correcting an earlier entry means the earlier entry is
still there.** `F-259`'s revision opens *"the original filing above was wrong to accept it."* The
wrong filing was left in place, unmarked, and is what a reader lands on first.

## 3. Search the register before researching a fact

Before investigating any P2 fact, **grep the register for it.** The answer is often already filed,
measured, and better-evidenced than the one you are about to derive.

On 2026-08-15 the `P_OE` / `P_CHANNEL` / `P_TT_01` identity was re-derived from the v55 text as
fresh research. F-264 already carried it — source-verified, bench-corroborated, with a measured
consequence (adding `P_CHANNEL` to a level-driven DAC dropped its output from 1,305 of 2,000
samples to 25). The re-derivation was slower and weaker than the filed answer.

## 4. Never restate a register verdict in another document

A plan, study, or task **points at** a finding; it does not summarise the finding's conclusion.
A restatement cannot be kept in sync and becomes a second, competing answer.

Live example: the sprint plan's bench-results table restated the register and contradicted it
**within one day** on whether the Goertzel accumulators are ever cleared — the plan says not
established, the register carries the measurement (five passes across `COGINIT`; two identical
commands giving exactly twice one command's total).

Naming the finding and its status (§1) is not a restatement. Reproducing its verdict, its
reasoning, or its numbers is.

## 5. Read the register whole, or read a derived view whole

Grep **locates**; it never **concludes**. No claim about state may rest on a windowed read.

This is affordable only while the active register is small, which is why the archival lifecycle is
not optional housekeeping — it is what makes this rule obeyable. An active register past a few
hundred lines is a defect in its own right: report it rather than working around it with a
narrower grep.
