# P2-Knowledge-Base overlay — sprint-plan

> **DRAFT (pre-brainstorm, 2026-06-05).** The per-head section depends on
> the Work Type Routing brainstorm and will be dialed in after.

## Augments Step 0a — resolving the per-head `PLAN_DIR` sentinel

`PLAN_DIR` is a per-head routing sentinel. Before writing the plan doc,
identify the head/element under sprint and resolve the plan location from
`.claude/skills/HEAD-DISPATCH-DRAFT.md` (manual → co-located with the
manual; YAML set → its own home; ingestion → with the source). Several
target homes are still `TBD` in that table — when you hit one, ask
{{USER_NAME}} rather than guessing a location.

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
