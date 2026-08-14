# Campaign — 2026-08 manual corrections bench session

**Purpose:** settle the three questions that gate manual edits in the
`MANUAL-CORRECTIONS-AND-RETIRED-DOC-CLEANUP` sprint. Everything else in that sprint is already
grounded in our own sources and does **not** need the bench.

**All three probes compile clean under `pnut-ts -d` (1.55.3).** Run them in the order below.

| # | Probe | Finding | Rig | Gates |
|---|---|---|---|---|
| 1 | `test-f263-cordic-pipeline-depth.spin2` | F-263 | bare board | whether the Assembly ch.5 CORDIC example gets rewritten **at all** |
| 2 | `test-f256-retcall-xbyte.spin2` | F-256 | bare board | whether XBYTE §15.3 is patched or restructured |
| 3 | `test-f259-f260-dac-and-goertzel.spin2` | F-259, F-260 | **one jumper: pin 0 → pin 1** | whether the Streamer DDS mode can be presented as buildable |

Probe 3 is last because it is the only one needing a jumper.

**Each probe ends with an explicit terminator** so you are never left wondering whether more
output is coming:

```
@@@ TEST COMPLETE: <probe name> @@@
@@@ nothing further will print - safe to stop the session @@@
```

If you run headless, `@@@ TEST COMPLETE` works directly as PNut-Term-TS's `--end-marker`, so the
session closes itself instead of needing a timeout.

---

## Every probe carries a control that must fail

This is deliberate and it is the part not to skip. A rig that cannot fail proves nothing, so each
probe reports its control **first** and tells you when the rest of its output is void:

- **F-263** — **queue one operation, then retrieve it immediately.** Per Chip's clarification this
  **must stall** (~54 clocks). If it returns fast, the rig cannot detect the failure mode under
  test. (Round 1 retrieved from an *empty* pipeline instead — with nothing in flight there is
  nothing to wait for, so that control never exercised the stall at all.)
- **F-256** — a bytecode handler that deliberately leaves XBYTE. The progress counter **must stop
  at 2**. If it keeps climbing, the counter is lying.
- **F-259** — the no-`P_OE` row and the `P_OE` row **must differ substantially**. If every row reads
  alike, the jumper is missing or the ADC is not converting — and a dead rig's null result looks
  exactly like the broken-mode null result Part 2 is hunting.

## Round 1 (2026-08-13) — all three VOID, all three fixed

Round 1 produced **no usable finding about any manual**; two probes declared their own results void,
which is the controls working as designed. Fixes now in place:

| Probe | Round-1 failure | Round-2 fix |
|---|---|---|
| F-256 | `progress=0`, scribbled hub — used `##@disp1` / `##@prog1`, but in an `ORGH` block the symbol **is** the hub address, so `@` double-offset it and XBYTE armed on garbage | `@` removed, matching the guide's own working §12.2 VM |
| F-263 | control retrieved from a pipeline never fed, so GETQX had nothing to wait for and returned instantly | control now **queues one op then retrieves it** — that must stall ~54 clocks |
| F-259/260 | every DAC row read alike (jumper was not fitted); Part 2 then **hung in `WAITXFI`** | pins moved to **0 → 1** for the small Edge carrier; `WAITXFI` replaced with a bounded `WAITX` so a dead streamer cannot hang the run |

**Round 1's CORDIC data changed that probe's shape.** Both arms came back offset by *exactly* 4 —
ARM B returned 14²/15²/16² for inputs 10/11/12 — while ground truth was correct. A clean index shift
in both arms at `FILL = 6` is what you would see if the CORDIC buffers **fewer completed results
than we queued and silently drops the oldest**. That is the community reporter's claim, and it
contradicts both Chip's clarification and our released P2AN002. So round 2 **sweeps FILL from 1 to
7**: the largest value that returns clean is the real usable depth, and where it breaks decides
whether this closes as harness error or escalates into a finding against a shipped app note.

---

## What each answer changes

**F-263 — CORDIC.** The reporter says deep pipelining scrambles output. **Our own authority says
otherwise:** Chip's `CORDIC-pipeline-theory.md` documents the fill/steady/drain model with "6-7
operations in flight" and says GETQX/GETQY **stall** rather than return garbage, and our released
P2AN002 ships a `FILL = 6` example of the same shape. The probe runs **both shapes side by side**
against single-op ground truth (Spin2 `ROTXY`), so it separates three outcomes:

- **A dirty / B clean** → the Assembly ch.5 example specifically is wrong; fix it.
- **both dirty** → deep pipelining itself is suspect. **Escalate — do not edit.** This would
  contradict a Chip-sourced clarification and a shipped app note.
- **both clean** → the report is not reproduced; the manual stands and F-263 closes as
  `RESOLVED-INVALID`.

**F-256 — `_RET_ CALL`.** The idiom assembles clean, so the reader's objection is wrong as stated;
what is unproven is the *semantics*. The probe distinguishes "helper ran and dispatch resumed"
(guide stands) from "helper ran but dispatch died" (§15.3 plus `:416`, `:793` and the `:879`
explanation all need rework) from "helper never ran."

**F-259 — cog-DAC gating.** The documentation fix is **already grounded** in our own
`wrpin.yaml:49`, which lists DAC under `p_oe_required_for`. This probe exists so we can cite the
measurement as ours rather than someone else's, and to settle a question the manual should answer
outright: does **OE**, **OUT**, or both gate the drive? The six-row sweep separates them.

**F-260 — DDS/Goertzel.** Two documentation defects are already confirmed from source (the
undeclared `dds_s` operand, and `adc_pin<<17` colliding with the required `%111` in D[18:16]) and do
not need silicon. What needs silicon is whether the mode runs at all. The probe builds the command
**exactly as documented — collision included** — then sweeps the same fields the reporter swept, so
we do not repeat blind. If every row returns zero, this becomes a question for Chip with our own
logs attached.

---

## After the run

Save the terminal output as a log per campaign convention. Results go to
`P2-EMPIRICAL-FINDINGS.md` as EF entries **for what we observed on our own board** — the community
bench remains a lead, not an EF source. Then update F-256, F-259, F-260, F-263 in
`P2KB-CORRECTION-FINDINGS.md` in the same pass; a register whose statuses lag the bench lies.

Raw logs are not versioned (regenerable from the versioned `.spin2`); the accepted finding is what
gets kept.
