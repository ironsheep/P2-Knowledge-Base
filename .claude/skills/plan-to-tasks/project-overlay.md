# P2-Knowledge-Base overlay — plan-to-tasks

> **Status (2026-06-22).** Work Type Routing model adopted; `PLAN_DIR` resolved
> to the unified dir (below). No open dependencies.

## Augments Step 0a — `PLAN_DIR` is a single unified dir

`PLAN_DIR` resolved to **one shared directory for all engineering heads** —
`engineering/planning/` (decided 2026-06-11; supersedes the former per-head
sentinel). Write plan artifacts there regardless of head, and name the
head/element in the filename so the single dir stays navigable; the archive is
`PLAN_ARCHIVE_DIR` (`engineering/history/sprints/`). The *other* per-head
sentinels (`BUILD_VERSION_*`, `PUNCH_LIST_DOC`, …) still resolve via
`.claude/skills/HEAD-DISPATCH-DRAFT.md`.

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
