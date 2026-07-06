# P2AN005 — Working Notes

**Status:** stood up + drafted 2026-07-06 (Family C app-notes sprint); v0.1.0 draft ready for PDF review
**Created:** 2026-07-06
**Topic:** Cooperative Multitasking with Spin2 TASK Methods (roster item **C1**, Concurrency & New Language Features family)
**Owning manual (enrichment fork):** Spin2 Reference Manual — **PARKED**, so this note is the guided home (no foundational fork)
**Companion note:** P2AN006 (Sizing Cog & Task Stacks) — authored in the same sprint; bidirectional cross-refs
**Sprint plan:** `engineering/planning/FAMILY-C-APP-NOTES-SPRINT-PLAN.md`

## Purpose

The `{Spin2_v47}` TASK\* family (cooperative, non-preemptive multitasking of up to 32 tasks in
one cog) is documented in the P2KB only as atomic method/constant/register YAMLs plus one
implementation pattern — there is no end-to-end guided home. This note is that home, and the P2
successor (lineage only) to Parallax P1 AN014 (Coroutines): a fragile hand-coded `JMPRET`/`swap`
PASM idiom becomes a handful of first-class language methods.

## Archetype & structure

Techniques-catalog (P2AN001/P2AN004 shape): one shared conceptual base (the cooperative model +
the method-family table + version gate + the register-collision hardware note), a decision table,
then four runnable recipes R1–R4, each with a 🔍 Verify. No ToC.

## Boundary delineation

**Foundational → owning manual: EMPTY (no fork).** The Spin2 Reference Manual is parked; there is
no shipped chapter teaching cooperative multitasking. Nothing here belongs in a currently-shipping
manual. Advanced-fork-only, like P2AN002/P2AN004.

## Recipes (all compile `pnut_ts -d` v1.55.0)

| # | Recipe | Methods exercised | File |
|---|---|---|---|
| R1 | Two-task round-robin | TASKSPIN(NEWTASK), TASKNEXT, the-last-job-runs-inline idiom | `two-task-round-robin.spin2` |
| R2 | Cooperative yield in a long computation | TASKNEXT cadence (`YIELD_EVERY`), atomic-long publish | `cooperative-yield.spin2` |
| R3 | Halt/resume flow control + synchronized start | TASKSPIN expression-return, TASKHALT(THISTASK), TASKCONT, TASKCHK | `halt-resume-flow.spin2` |
| R4 | Task coordination + status dashboard | TASKCHK, TASKID, TASKHLT (reversed bits), TASKSTOP(THISTASK) | `task-dashboard.spin2` |

Adapt-It capstone: multi-cadence-on-one-bus (50/100/1 Hz on one I²C bus) — *cited* from the
`spin2_cooperative_tasking.yaml` pattern, not rebuilt (keeps the note short + ties to C3 stacks).

## Sources (all P2-native — no P1 content read or cited)

- `deliverables/ai/P2/language/spin2/methods/task{spin,next,halt,cont,chk,id,stop}.yaml`
- `deliverables/ai/P2/language/spin2/constants/{newtask,thistask}.yaml`, `registers/taskhlt.yaml`
- `deliverables/ai/P2/language/spin2/patterns/implementation/spin2_cooperative_tasking.yaml`
  (the "finish the transaction before you yield" discipline + the many-cadences example)
- Spin2 v55 keyword table `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt:39,149`
- Ground truth: `pnut_ts` v1.55.0 compile-probes.

The "successor to AN014" is **roster lineage metadata only** (`p2-app-note-roster.md`,
`P1-DOCUMENT-LINEAGE.md`). No P1 document was read or cited; the coroutine-gotcha ("finish before
you yield / no flag reliance across a switch") is sourced from the P2 pattern YAML.

## P2KB findings logged (register; YAML fixes DEFERRED to after PDF review)

- **F-196 (CONFIRMED)** — `taskwait.yaml` documents `TASKWAIT`, which **does not compile** (proved
  with `pnut_ts -d`: "Expected an instruction or variable"). Excluded from this note. Deferred fix:
  stub `taskwait.yaml` invalid (like `taskresume.yaml`).
- **F-197 (CONFIRMED)** — `taskspin.yaml` `returns: void` omits the expression-return (task # / −1)
  form the note uses.
- **F-198 (NEEDS-VERIFICATION)** — "main task is typically ID 0" (taskid/taskhlt YAMLs) is unsourced;
  the note relies on no fixed main-task id.

## Open questions (for authoring / audit)

- Live scheduling (true interleaving), the "all-halted → wait-for-interrupt" edge, and
  "last task's return frees the cog" are runtime behaviors — described from v55, hardware
  confirmation deferred (Stephen runs silicon externally; → EF ledger if a run is accepted).
- YAML companion: `deliverables/ai/P2/application-notes/p2an005-cooperative-multitasking-tasks.yaml`
  — established P2ANxxx schema; agreement-gated against this body.

## Canonical source

Body: `opus-master/P2AN005.md` (+ `opus-master/front-matter.md` cover). Edit here; the workspace
render is generated and overwrites edits.
