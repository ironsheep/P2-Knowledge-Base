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

## Augments §2 code-research — coverage/gap analysis factors IN-DEVELOPMENT scope

When the sprint is a **coverage or gap analysis** (what's documented vs. missing
— e.g. an app-note roster, a manual-coverage audit), the research pass MUST count
not just **shipped** coverage but the **planned scope of in-development docs** —
read their charters / `PLANNING.md` / creation-guides, not only their current
render. An in-flight manual can already *own* a gap (its capstone or a planned
chapter), so treating "not shipped yet" as "uncovered" over-states the gap and
proposes work that duplicates an active effort. *(Certified 2026-06-30: the
App-Note Roster's first cut over-stated the compute-model gap by counting only
shipped manuals — the in-development P2 Architect's Guide Act II + decomposition
YAML layer already owned it; Stephen caught it.)*

## Augments §2 code-research — scope boundaries come from the artifact, never from prose

**Any date or commit that bounds an investigation's scope must be derived from the
artifact under investigation — never inherited from a narrative that cites it.**

Run the pickaxe on the *actual text* of the thing being investigated before you
fix a window:

```
git log --oneline --date=short --format='%h %ad %s' -S'<the rule/claim text>' -- <the file>
```

**A cited SHA is evidence that something changed then. It is never evidence that
nothing changed before.** The two are constantly confused, and the confusion is
invisible in the finished plan — the window simply looks authoritative.

*Certified 2026-08-15 («#214»).* The study and the task body both scoped a damage
investigation to "since `acf3b4a2` (2026-07-20)". Pickaxing the rule text instead
dated it to each guide's **birth** — Streamer `10bb35d5` (2026-01-22), Assembly
`1e51f086` (2025-11-26); `acf3b4a2` was the **corrective**, not the cause. Real
window 7–9 months, not 3–4 weeks. Executed as written the task would have scanned
~1 commit instead of ~120 and returned a NIL that cleared nothing. Cost of the
check: one command.
