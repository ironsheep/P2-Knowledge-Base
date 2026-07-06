# P2AN006 — Working Notes

**Status:** stood up + drafted 2026-07-06 (Family C app-notes sprint); v0.1.0 draft ready for PDF review
**Created:** 2026-07-06
**Topic:** Sizing Cog & Task Stacks (roster item **C3**, Concurrency & New Language Features family)
**Owning manual (enrichment fork):** Spin2 Reference Manual — **PARKED**, so this note is the guided home (no foundational fork)
**Companion note:** P2AN005 (Cooperative Multitasking) — authored in the same sprint; bidirectional cross-refs
**Sprint plan:** `engineering/planning/FAMILY-C-APP-NOTES-SPRINT-PLAN.md`

## Purpose

Both `cogspin` (new-cog method) and `TASKSPIN` (intra-cog task) require the caller to hand over a
hub stack buffer, and the interpreter gives ZERO overflow protection — an undersized buffer
silently overwrites following hub memory. This note is the worked recipe for sizing both, and the
P2 successor (lineage only) to Parallax P1 AN019 (Measuring Stack Space). It answers the question
P2AN005 raises: "how big must each cog/task stack be?"

## Archetype & structure

Techniques-catalog (P2AN001/P2AN004 shape): one shared conceptual base (why overflow is silent, the
two stack contexts, the sentinel technique + `isp_stack_check` API + the sizing method), a decision
table, then four runnable recipes R1–R4, each with a 🔍 Verify. No ToC. No rendered figures.

## Centerpiece instrument — `isp_stack_check` (Stephen M. Moraco, MIT)

The note is built around Stephen's `isp_stack_check.spin2` utility. Two constants — `NOT_WRITTEN_MARK`
($a5a50df0) fill pattern + `DO_NOT_WRITE_MARK` ($addee5e5) sentinel — plus four API methods
(`prepStackForCheck` / `checkStack` / `getStackDepth` / `reportStackUse`). Shipped **verbatim** into
`examples-library/` (MIT, license header retained) — a deliberate, tracked copy, distinct from the
NO-COMMIT source fodder it was read from.

## Boundary delineation

**Foundational → owning manual: EMPTY (no fork).** Spin2 Reference is parked; stack sizing has no
other released-manual home. Advanced-fork-only.

## Recipes (all compile `pnut_ts -d` v1.55.0; each OBJ-includes isp_stack_check.spin2)

| # | Recipe | Instrument methods | File | Directive |
|---|---|---|---|---|
| R1 | Instrument a new-cog stack | prepStackForCheck, checkStack | `instrument-cog-stack.spin2` | none (cogspin) |
| R2 | Find the high-water mark, right-size | reportStackUse / getStackDepth | `high-water-mark.spin2` | none (cogspin) |
| R3 | Pinpoint the overflowing routine | granular checkStack | `pinpoint-overflow.spin2` | none (cogspin) |
| R4 | Size a TASKSPIN task stack | checkStack + reportStackUse | `size-task-stack.spin2` | `{Spin2_v47}` |

Sizing method taught: start 128 → exercise the deepest path → `reportStackUse` reads high-water N →
set buffer ≈ 1.5×N → keep `checkStack` as a guard. Cog stack floor ~32, typical 64–128 (KB `cogspin`).

## Two-context model

new-cog stack (cogspin, one call stack per cog) vs intra-cog task stack (TASKSPIN, one per task). The
instrument only watches a hub buffer, so it is context-agnostic — R4 proves the technique is identical.
Distinct from the P2 hardware 8-level call stack (PASM CALL/RET) — the note says so explicitly, does
NOT conflate (guarded against `stack_operations.yaml`'s PTRA/PTRB scope).

## Honest framings carried into the note

- `checkStack` detects the boundary was crossed, not arbitrary corruption (contiguous growth clobbers
  the sentinel first → detection sound) — stated as a pitfall.
- Reentrancy: `isp_stack_check` keeps working values in shared object DAT vars → built for ONE checker
  at a time. Every recipe has a single thread do the checking; stated as a 🔧 Hardware note.
- High-water mark only counts paths that actually ran → "measure the worst case" pitfall.

## Sources (P2-native + Stephen's utility — no P1 content read or cited)

- `deliverables/ai/P2/language/spin2/methods/{taskspin,cogspin}.yaml` (stack params, "overflow not detected")
- `deliverables/ai/P2/language/pasm2/concepts/stack_operations.yaml` (hardware-stack distinction — cited to keep the two separate)
- Spin2 v55 stack-packing (`spin2-v55-text.txt:284`: params→results→locals in declaration order)
- `isp_stack_check.spin2` + `isp_stack_check_UserGuide.md` (read READ-ONLY from the NO-COMMIT fodder; the object shipped verbatim, the guide informed the recipes)
- Ground truth: `pnut_ts` v1.55.0 compiles.

"Successor to AN019" is **roster lineage metadata only**. No P1 document read or cited. AN019 PDF is
un-ingested (`external-inputs/P1/AppNotes/AN019-StackSpace-v1.0.pdf`) — not needed; the note is
P2-native + built on Stephen's utility.

## P2KB findings

None new from this region (cogspin/taskspin/stack YAMLs are correct as used). Cross-cutting Family C
findings F-196..F-200 logged from the C1/C2 regions.

## Open questions (for authoring / audit)

- Actual overflow detection + the halt/lockup are runtime behaviors observed on silicon (Stephen runs
  hardware externally); described from the utility's design, confirmation deferred (→ EF ledger if a
  run is accepted). No invented DEBUG captures.
- YAML companion: `deliverables/ai/P2/application-notes/p2an006-sizing-cog-task-stacks.yaml` —
  established schema; agreement-gated against this body.

## Canonical source

Body: `opus-master/P2AN006.md` (+ `opus-master/front-matter.md` cover). Edit here; the workspace
render is generated and overwrites edits.
