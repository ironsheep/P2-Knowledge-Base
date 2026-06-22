# P2-Knowledge-Base overlay — sprint-plan

> **Status (2026-06-22).** Work Type Routing model adopted; `PLAN_DIR` resolved
> to the unified dir (below). No open dependencies.

## Augments Step 0a — `PLAN_DIR` is a single unified dir

`PLAN_DIR` resolved to **one shared directory for all engineering heads** —
`engineering/planning/` (decided 2026-06-11; supersedes the former per-head
sentinel). Write the plan doc there regardless of head, naming the
head/element in the filename. The *other* per-head sentinels
(`BUILD_VERSION_*`, `PUNCH_LIST_DOC`, …) still resolve via
`.claude/skills/HEAD-DISPATCH-DRAFT.md`.

## Augments §plan-authoring — flag design decisions before large YAML changes

When the sprint will **edit 3+ YAML files in the P2KB set, or introduce a
new concept/file**, the plan doc must carry, *before any editing begins*:

1. A compact **file table** — each file to update/create with a one-line
   scope.
2. A **"design decisions to flag"** section naming the non-obvious calls
   the sprint will make — e.g. new-file-vs-extend-existing, how to
   represent a non-enforced/version-gated directive accurately, the scope
   of a cross-reference change.
3. An explicit **wait for per-decision confirmation** before edits start.

Skip this for single-file fixes, typo corrections, or mechanical steps
(index regeneration). Rationale and the validated example are in
[[feedback_plan_before_yaml_changes]]; this pairs with the data-set-wide
correction discipline in [[feedback_no_unsourced_claims]] and the
findability mandate in [[feedback_yaml_findability_continual]].
