# P2-Knowledge-Base overlay — plan-to-tasks

> **DRAFT (pre-brainstorm, 2026-06-05).** Depends on the Work Type Routing
> brainstorm; will be dialed in after.

## Augments Step 0a — resolving the per-head `PLAN_DIR` sentinel

`PLAN_DIR` is a per-head routing sentinel. Identify the head/element the
plan belongs to and resolve the plan location from
`.claude/skills/HEAD-DISPATCH-DRAFT.md` before reading/writing plan
artifacts. Target homes marked `TBD` there → ask {{USER_NAME}} rather than
guess.

## Note — per-task detail artifacts stay off

`TASK_DETAIL_DIR` / `TASK_DETAIL_TEMPLATE` are intentionally unset in
conventions, so the per-task-detail step is skipped: all per-task context
lives in the todo-mcp task ledger. (Confirm during the brainstorm whether
any head — e.g. the YAML correction batches — wants a per-task detail doc;
if so, both slots get set together.)
