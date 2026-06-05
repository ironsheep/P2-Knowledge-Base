# P2-Knowledge-Base overlay — sprint-start

> **DRAFT (pre-brainstorm, 2026-06-05).** Depends on the Work Type Routing
> brainstorm; will be dialed in after.

## Augments Step 0a — establish the head before resolving sentinels

A sprint here targets **one element of one head** (a manual, the P2KB YAML
set, or an ingestion source). Establish the head/element first, then
resolve every per-head sentinel (`PLAN_DIR`, `BUILD_VERSION_*`,
`PUNCH_LIST_DOC`, `RELEASE_NOTES_DOC`, `SPEC_DOC`) for that element via
`.claude/skills/HEAD-DISPATCH-DRAFT.md`. Record the resolved head/element
in the sprint context so downstream skills (`plan-to-tasks`,
`baseline-health`, `build-wrapup`, `sprint-closeout`) resolve to the same
element.

## Augments the entry baseline — what "green" means per head

`baseline-health`'s entry baseline maps to the **YAML head's** local
validators (see `skill-conventions.md` BUILD/TEST). For a **MANUAL** sprint
there is no local build gate (manuals render on PDF Forge — handback
model), so the entry "baseline" is the document's audit state, not a
compiler result. For an **INGESTION** sprint the baseline is the
quality/cross-ref/audit gates + completeness dashboard, not a version or
test count. Name which baseline applies in the plan doc so the exit
no-regression assertion compares like with like.
