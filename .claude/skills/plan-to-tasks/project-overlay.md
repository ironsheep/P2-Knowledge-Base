# P2-Knowledge-Base overlay — plan-to-tasks

## Augments Step 0a — resolving the per-head sentinels

`PLAN_DIR` and `PLAN_ARCHIVE_DIR` are literal values in conventions; read them
there. Name the head/element in every plan filename so the one shared directory
stays navigable.

The slots that are still **routing sentinels** (`BUILD_VERSION_*`,
`PUNCH_LIST_DOC`, `RELEASE_NOTES_DOC`, `SPEC_DOC`) resolve per head via
`.claude/skills/HEAD-DISPATCH-DRAFT.md`, keyed off the `active_element` pointer.

## Augments §3a-ii — the two-environment split as a scheduling resource

Central schedules limited-environment work into the wait windows the canonical
side creates. Here the windows are long and predictable: **every PDF is a
round-trip through Stephen** (stage outbound → he runs Forge → the PDF comes
back), and so is every hardware-verification run. Schedule container-side work —
YAML edits, validator runs, audit passes, the next manual's prep — into those
windows rather than idling on the render. The correctness constraint still binds:
a content change must land *before* the render that is supposed to show it, and
editing a manual after its PDF was verified decertifies that verification.

## Note — per-task detail artifacts stay off

`TASK_DETAIL_DIR` / `TASK_DETAIL_TEMPLATE` are intentionally unset in
conventions, so the per-task-detail step is skipped: all per-task context
lives in the todo-mcp task ledger. (Confirm during the brainstorm whether
any head — e.g. the YAML correction batches — wants a per-task detail doc;
if so, both slots get set together.)

## Augments §3a ordering — an instrument's first run is a planning input, not just a gate

When a sprint builds a **measuring instrument**, ordering it first is necessary
but **not sufficient**: no downstream task's **scope or estimate** may be fixed
until that instrument has **run once**. Write those tasks with their fix-lists
marked explicitly as *subsets pending first measurement*, and re-size after.

Ordering-first without deferring the estimates just means the hand count gets
committed to task text a few hours earlier.

*Certified 2026-08-15 («#206»).* The instrument's first run returned **176
findings against a planned ~100**, with the excess concentrated in a class the
hand pass barely sampled — **62 codename sites** against the 5 the plan named by
hand. `«#207»`/`«#208»` had already been sized against the subset. The same plan
had ordered the instrument first *precisely because* hand counts had been wrong
four times in that study, and still inherited their numbers.
