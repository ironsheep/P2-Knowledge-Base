# P2AN005 — Example Library

The complete, runnable source for the worked recipes in **Application Note
P2AN005, "Cooperative Multitasking with Spin2 TASK Methods."** Each file is
extracted verbatim from the opus-master so the download and the document never
drift.

| File | Recipe | Demonstrates |
|---|---|---|
| `two-task-round-robin.spin2` | R1 (round-robin) | two independent blinkers from one cog via `TASKSPIN` + `TASKNEXT` |
| `cooperative-yield.spin2` | R2 (cooperative yield) | a long computation that stays responsive by yielding on a cadence |
| `halt-resume-flow.spin2` | R3 (halt / resume) | producer/consumer flow control + synchronized start (`TASKHALT`/`TASKCONT`/`TASKCHK`/`THISTASK`) |
| `task-dashboard.spin2` | R4 (task dashboard) | live `TASKCHK`/`TASKHLT` census + `TASKID` self-ID + clean `TASKSTOP` shutdown |

**Version gate.** Every file opens with `{Spin2_v47}` as its first line — the TASK
methods are a Spin2 v47 language feature and will not compile without it.

**Verification.** Every file compiles clean under `pnut-ts -d` (v1.55, `_clkfreq =
200_000_000`). Build with DEBUG enabled (`-d`) so the `debug()` output stream
appears. Live scheduling behavior (true interleaving, halt/resume timing) is
confirmed on a P2 board; the programs report their state over DEBUG so you can
watch each recipe work.

- **R1** blinks onboard LEDs 56 and 57; add a `debug()` to watch it without LEDs.
- **R2/R3/R4** are pure DEBUG — no external parts. R2's `YIELD_EVERY` and R3's
  consumer pace are the knobs to experiment with (see the note's Verify sections).

**Packaging.** At release these files are published as `P2AN005-src-<YYMMDD>.zip`
beside the PDF in `deliverables/documents/DOCs/`, with a download link in the
publication roster (per the app-note production convention — see
`../../APP-NOTE-CREATION-GUIDE.md` §6).
