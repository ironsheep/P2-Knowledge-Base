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

**Any contradiction found is not an input to weigh.** It is **sprint stop 4** — *a contradiction
of what planning assumed* (*the stop roster*, `skills-docs/SKILLS-AUTHORING.md`); the roster is
closed and this overlay cites it rather than minting one. Surface it and wait. Choosing the entry
that suits the plan is how a duplicate becomes a decision.

The check itself failing is **not** a stop: a register you cannot parse or a plan whose newest
block you cannot date is a *step halt* — diagnose it and re-route. Only a genuine contradiction
between the plan and the register reaches {{USER_NAME}}.

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

## Augments §3a — a seventh rework pattern: source repair before destructive sweep

Central §3a lists six conflict patterns the rework pass checks for. This project needs a
seventh, and it is the one that cost a re-task on 2026-08-24:

> **Source repair before destructive sweep** — a task that REPAIRS a source (re-ingestion,
> forced OCR, a structured-format re-extraction) scheduled *after* a task that DELETES content
> the source is supposed to ground. The deletion then decides dispositions against a damaged
> authority, and where the purged class has no repopulation route the loss is permanent.

It reads like central's *discovery before utilization*, and it is not the same check. Discovery
asks whether a needed **fact** arrives before its consumer. This asks whether the **authority
itself** is repaired before a step that destroys what it grounds — and it can fire even when
every fact is nominally available, because an ingested-but-lossy source looks available.

**How to run the check.** For each destructive task in the set: name the authorities it will
decide against; confirm each is fully ingested; confirm a **restore path exists for that class**.
Where one class has a repopulation route and another does not, that asymmetry is the finding.
On 2026-08-24 the datasheet class had one and the board-guide class did not, and the ordering
was a defect rather than a preference precisely because of it.

**A register finding can BE an ordering instruction.** F-250 read *"re-ingest this source with
forced OCR, re-verify every numeric claim already derived from it"* — the first tasking read
that as a work item and scheduled it nine tasks after the sweep that consumed those facts. When
a finding's disposition names a sequence, honor the sequence.

**The full rule is `.claude/skills/SOURCE-REPAIR-ORDER.md`** — stated once there, including why
cite-in-place is claim-first, and the completeness gate's stop vocabulary. Do not restate it in
a plan or a task; point at it, the way tasks point at the register.

---

## Augments §2 — the ingestion-task deliverable shape: the gap ledger is never optional

**Every task whose subject is a source — an ingestion, a re-ingestion, an extraction repair —
names `engineering/ingestion/KNOWLEDGE-GAPS.md` in its deliverables, with BOTH halves stated:
the holes this source OPENS, and the holes it now CLOSES in sources already ingested.**

**Why this has to live here rather than in the skill.** `ingest-source`'s completion checklist
already requires it, and has for months. It still did not happen — three times in one day:

| 2026-08-24 | dug | filled |
|---|---|---|
| «#306» `p2-eval-board` forced-OCR re-ingest (`8167f233`) | — | — |
| «#308» `p2-hardware-manual` DOCX-primary (`ece5c74a`) | G-016/017/018 | — |
| «#297» `p2-datasheet` table recovery | — | — |

Under `DISPATCH_MODEL: arbiter-serial` **the task body IS the dispatch prompt**, and a
dispatched agent reads the body, not the skill. So a requirement that lives only in a skill
checklist is a requirement a dispatch silently drops — every time, invisibly, and the executor
is not at fault. A requirement that must survive the context boundary has to be **in the body**,
and the body is generated here. This is the same shape as fixing the `Dockerfile` rather than
the README it bakes: repair the generator, not the artifact.

**What the deliverable must demand — the part that makes it real.** Naming the file is not
enough; "reviewed the ledger, nothing applied" is the exact sentence that produced the table
above. The task must require the agent to report, per row it examined:

- rows **moved** OPEN→ANSWERED, each with the source **@ edition** and a `file:line` trace
  (the ledger's own header requires this so a later supersession can RE-OPEN the row); and
- rows **re-tested and deliberately LEFT open**, naming what was read and why it fell short.

The second list is the load-bearing one. It is the only thing that distinguishes a pass that ran
from a pass that was skipped, and it is what a soft closure cannot fake. A ledger padded with
weak closures is worse than one left stale, because it stops anyone looking again.

**The failure mode to name in the task body.** «#308» wrote *"G-001..G-015 are Smart-Pins-detail
and add-on-board questions this document does not address; it is a hardware overview, not a
smart-pin reference"* (`p2-hardware-manual-complete-extraction-audit.md:262-263`). Its own
extract carries the (S) Smart Pin Modes table, per-mode narrative for every `%SSSSS` mode, and
Table 16 — the `%AAAA`/`%BBBB` input selector that closes G-001 outright, cell-identical to the
datasheet's. **One confident sentence, written without opening the artifact, cost six rows.**
Require the check to be run against the extract, not against a belief about what the document is.
