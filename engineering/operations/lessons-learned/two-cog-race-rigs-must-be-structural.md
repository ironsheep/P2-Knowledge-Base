# Two-Cog Race Rigs: Make the Race Structural, Not Incidental

**Incident:** 2026-07-13 — P2AN007 hardware verification, rigs VT2 and VT3
**Cost:** two hardware runs and a nearly-banked false PASS
**Applies to:** any verification test where two or more cogs contend

## What happened

VT3 tests that a hardware lock serializes two writers into one queue. It runs two
arms: locked (expect zero anomalies) and unlocked (expect many). On run 1 the
unlocked arm reported **14,976 anomalies** — a clean PASS. On run 2 the same arm
reported **0**, and the rig declared itself INCONCLUSIVE.

Between those runs the rig's *logic did not change*. The only edits were debug
strings and an added `DONE` line.

VT2 showed the same disease from the other side: its "no ack" arm reported **zero**
torn commands on two consecutive runs, across two different rig revisions, and had
to be called INCONCLUSIVE both times.

## Root cause

Two cogs running deterministic Spin2 loops of equal length hold a **nearly fixed
relative phase**. Their period is set by the code, not by anything that jitters, so
whichever phase relationship they land in at `cogspin` time is roughly the one they
keep. Whether writer B ever walks into writer A's critical section — or whether the
worker's reads ever straddle the writer's write — is therefore **decided once, at
launch, and then never re-sampled**.

Adding a single `debug()` line shifted the launch timing enough to reroll that dice
throw. Run 1 rolled "collide." Run 2 rolled "never collide."

The window in both rigs was 1µs — comparable to the loop bodies around it. That
made the overlap a coin flip on phase rather than a property of the design.

## The rule

**A race that the rig only *sometimes* exercises is not a test.** Do not rely on two
cogs happening to interleave. Make the interleaving **structural** — guaranteed by
construction, not by luck:

- **Hold the contended window open longer than the other cog's entire loop.** If
  writer A sits in the critical section for 10µs and writer B's whole loop is 3µs,
  B cannot avoid walking in. (VT3's fix.)
- **Make the reader's exposure longer than the writer's full cycle.** If the worker
  holds a half-read record for 25µs and the writer produces a new one every ~3µs,
  the writer *must* land inside the read. (VT2's fix.)
- Apply the widened window **identically in every arm**, so the arms still differ in
  exactly one thing — the protocol under test. Widening the window changes the
  *observability* of the failure, never the thing being compared.

## The guard that saved it

Both rigs required the broken arm to report **> 0** before declaring PASS, and
reported `INCONCLUSIVE` otherwise. Without that, run 2's VT3 would have read
"locked arm: 0 anomalies" and been banked as a clean PASS — a false green, from a
run in which the detector never fired at all.

**Every dual-tail rig must fail loudly when its negative control does not fail.**
Zero-in-both-arms means the experiment did not run, and it must never be reported as
success.

## Related

- The house dual-tail (prove-true + prove-false) design, and the entry-phase sweep in
  `p2-assembly-language-manual/audit/verification-tests/hub-rdlong-shapes-timing/SPEC.md`,
  which sweeps phases 0–7 for exactly this reason.
- `engineering/ingestion/external-sources/hardware-verification/` — the EF ledger,
  where accepted results land.
