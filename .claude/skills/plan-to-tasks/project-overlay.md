# P2-Knowledge-Base overlay — plan-to-tasks

## Augments Step 0a — resolving the per-head sentinels

`PLAN_DIR` and `PLAN_ARCHIVE_DIR` are literal values in conventions; read them
there. Name the head/element in every plan filename so the one shared directory
stays navigable.

The slots that are still **routing sentinels** (`BUILD_VERSION_*`,
`PUNCH_LIST_DOC`, `RELEASE_NOTES_DOC`, `SPEC_DOC`) resolve per head via
`.claude/skills/HEAD-DISPATCH-DRAFT.md`, keyed off the `active_element` pointer.

## Augments §1 — the CURRENCY GATE: prove the plan is current before creating any task

Central §1 says read the plan top to bottom before creating anything. That instruction is
self-assessed, and on 2026-08-15 it was self-assessed wrongly: an 18-task sprint was generated from
plan §7 — pre-bench prose — while a block superseding it sat **680 lines above**, and the findings
register held verdicts that reversed four of the tasks. Entering at §Open Questions and reading
*forward* is what did it, so **drop that entry pattern: the entry point is always the head of the
document, never the section the skill happens to gate on.**

**Before creating the first task, post a four-line currency check.** It is short by design, and it
cannot be produced without doing the reading:

1. **Plan span and head** — the plan's total line count, and the line number + date of its newest
   state block. If the newest state block is *below* where you started reading, you started in the
   wrong place.
2. **Sections superseded** — any section whose content a later block contradicts, by number. "None"
   is a valid answer only if you can say what you compared.
3. **Register state for every finding in scope** — each finding ID with **its status and line
   number**, per `.claude/skills/REGISTER-CONSULTATION.md` §1. This is the line that would have
   caught 2026-08-15: F-259 REVISED, F-260 resolved-and-duplicated, F-256 answered, F-263 confirmed
   with cause — all filed, none read.
4. **Blocking standing rules** — any recorded rule that gates the work. On 2026-08-15 two findings
   read `resolution deferred until the bench campaign closes` ({{USER_NAME}}'s standing rule), which
   blocked most of the sprint being tasked.

**Any contradiction found is a STOP, not an input to weigh.** Surface it and wait. Choosing the
entry that suits the plan is how a duplicate becomes a decision.

**Why this shape:** an instruction to "read carefully" cannot be checked by anyone, including the
agent following it. A required artifact can — a missing or vague currency check is visible in the
output, and it cannot be written without having read the head, the register, and the statuses.
That is the whole difference between a rule and a rule that is hard to avoid.
(See [[feedback_drop_techniques_that_lower_quality]].)

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
