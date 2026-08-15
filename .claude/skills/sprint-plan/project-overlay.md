# P2-Knowledge-Base overlay — sprint-plan

## Augments Step 0a — resolving the per-head sentinels

`PLAN_DIR` is a literal in conventions; write the plan doc there regardless of
head, naming the head/element in the filename. The slots that are still routing
sentinels (`BUILD_VERSION_*`, `PUNCH_LIST_DOC`, `RELEASE_NOTES_DOC`, `SPEC_DOC`)
resolve per head via `.claude/skills/HEAD-DISPATCH-DRAFT.md`.

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

## Augments §2 code-research — SCOPE INPUTS come from the artifact, never from prose

**Any input that bounds or defines a sprint's scope must be derived from the artifact under
investigation — never inherited from a narrative that cites it.** Dates and commits, yes; and
equally **which findings are open, what a finding's verdict is, whether a test has already run,
and what state a document is in.**

*Widened 2026-08-15, and the widening is the point.* This rule previously read "any **date or
commit**." It was written around the instance that produced it instead of the shape, so when the
same defect recurred in a different guise — an entire finding set taken from a superseded plan
section while the register held the current verdicts — **reading the rule triggered nothing.** A
rule scoped to its origin story only fires on its origin story. State the shape.

Before any scope claim, name the artifact and derive from it:

| Scope input | The artifact — never the narrative |
|---|---|
| a date or commit window | `git log -S'<the actual text>' -- <the file>` |
| whether a finding is open, and its verdict | the register entry + **its status field** — see `.claude/skills/REGISTER-CONSULTATION.md` |
| whether a bench/verification run has happened | the register status and `P2-EMPIRICAL-FINDINGS.md`, not a plan's summary of them |
| a document's version or lifecycle status | `PUBLICATION-ROSTER.md` |
| a defect count or file set | the instrument's own output |

**A cited SHA is evidence that something changed then. It is never evidence that nothing changed
before.** The same asymmetry holds for every row: a narrative citing a finding is evidence the
finding existed, never evidence of its current state.

*Certified 2026-08-15 («#214»).* The study and the task body both scoped a damage investigation to
"since `acf3b4a2` (2026-07-20)". Pickaxing the rule text instead dated it to each guide's **birth**
— Streamer `10bb35d5` (2026-01-22), Assembly `1e51f086` (2025-11-26); `acf3b4a2` was the
**corrective**, not the cause. Real window 7–9 months, not 3–4 weeks. Executed as written the task
would have scanned ~1 commit instead of ~120 and returned a NIL that cleared nothing. Cost of the
check: one command.

*Re-certified 2026-08-15, on the widened form.* Sprint 2's entire task set was generated from plan
§7 — pre-bench prose — while a superseding bench-results block sat 680 lines above it and the
register carried the current verdicts. Four findings were tasked backwards, one already-filed KB
defect was re-derived from scratch, and the wrong app note was placed in the release wave.

## Augments §plan-authoring — plans POINT at registers, they never restate them

A plan names a finding and its status; it does not reproduce the finding's verdict, reasoning, or
numbers. See `.claude/skills/REGISTER-CONSULTATION.md` §4 for why, with the live example — this
plan's own bench-results table contradicted the register within a day.

**Applies retroactively:** when revising a plan that already carries restated register state,
**delete the restatement** rather than updating it. Updating it preserves the shape that drifts.

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
