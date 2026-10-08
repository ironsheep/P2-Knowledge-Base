# P2KB close-out study

**Status:** SCOPE AGREED by Stephen 2026-10-08 (group E dropped at his word). Reading has not
started.
**Skill:** central `study`. The hand-off seeds the close-out sprint plan (`sprint-plan`).
**Element:** `yaml:p2kb`.

## Why this study exists

KB releases have been frequent (40 since 2026-06-13), and every one has shipped with known work
still open. Two causes, both addressed in process on 2026-10-08:

- **We set seen defects aside.** On 2026-10-07, F-548 to F-551 were each logged mid-fix in a file
  that was already open. Doctrine now says: *On the KB, what we see wrong we fix in the same pass,
  and we search wider than the target.*
- **Fixes we only partly made came back as new findings.** Five of the seven defects in the
  2026-10-07 pre-release audit were siblings of fixes made that same day.

Stephen's ordering (2026-10-08):

1. Research every YAML change first.
2. That research yields the bench questions.
3. The bench questions yield the test files.
4. Run the bench.
5. Processing the results closes planning.
6. Only then task the changes, with every answer in hand.

Every task then applies a known answer, so no task has to investigate.

---

## 1. Scope — AGREED 2026-10-08

**The question.** For every open YAML-scoped item, what exactly must change in
`deliverables/ai/P2/`, and on what authority? The authority is an ingested source (`file:line`)
or a bench result (EF/XF).

### In scope

| Group | Items | What the study produces |
|---|---|---|
| **A. Decided 2026-10-08** | F-359 · F-375 · F-398 · F-381 · F-547 (the operator-ingestion audit) · ENH-03 | A change spec per the recorded decision (register notes "DECIDED by Stephen 2026-10-08") |
| **B. Open YAML corrections** | F-550 · F-551 · F-548 · F-545 · F-562 · F-560 · F-392 · F-386 (the ten mode pages) · F-372 · F-354 (three board facts) · F-336 · F-337 (remainder) · F-561 (the YAML companion half only) | A change spec, a bench question, or a blocker that is not a bench question |
| **C. Open knowledge gaps** (`KNOWLEDGE-GAPS.md`) | G-002 · G-004 · G-005 · G-006 · G-009 · G-012 · G-015 · G-019 · G-020 · G-022 · G-023 · G-024 · G-025 · G-027 · G-028 · G-029 | Each is answered from the sources, becomes a bench question, or is declared out of reach (e.g. it needs a document we do not hold) |
| **D. Bench queue already filed** | VO-J-005 (written, not run) · VO-J-006 (not written) · VO-J-028 (not written) | Each is re-checked against the sources first (see the bench rule below), then the test is written or the question retired |
| ~~E. Field-report reconciliation~~ | **Dropped 2026-10-08.** Stephen: *"field reports should already be done. there are no remaining unprocessed that i've given you."* | — |
| **F. YAML-head gates** | F-364 (the gate that reads `yaml_file:`) · F-405 (a stale gzip passes) · F-441 (index sha256 vs the committed blob) · F-454 (an absolute max without its board revision) · F-389 (the key generator drops path components) | A build spec for each gate |
| **G. Class sweeps** | For every row in A–D and F, the wider search: the same wrong claim, pattern or shape anywhere in `deliverables/ai/P2/` | Every sibling found is added to its row |

### The parallel track: the ENH-03 compile gate

Stephen decided it is built **first** and stays a permanent release gate. It is tooling, not
research, so it runs as its own track from day one, under its own tasks, built from the
register's ENH-03 design points:

1. the per-block markers;
2. fix the prototype's collision bug;
3. a hard gate in `release-yamls`;
4. an edit-time check in `yaml-knowledge-base-maintenance`.

The study's "is this example correct?" reads (F-381 reading 1) wait on it.

### Excluded, each with its reason

| Excluded | Why |
|---|---|
| The ~22 `PENDING-VALIDATION` entries (F-546, 547, 543, 549, 542, 525, 421, 436, 377, 383, 393, 387, 320, 552–559), plus F-361 and F-544 | Already applied and independently verified. They close when a release serves them, so there is nothing to research. A class sweep in G that touches their files reads them as it passes. |
| Manual and PDF-head items: F-299, F-300, F-301, F-316, F-317, F-280, F-356, F-424, the manual halves of F-202 and F-268, the F-561 app-note prose, F-418 (torture test) | Not YAML. They are fixed and committed with each document's release. |
| Ingestion-tree artifacts: F-332, F-341, F-344, F-367, F-123 | ⛔ Ingested docs are never edited. These are findings for the ingestion head (`ingest-source`). The study notes whether any of them drives a KB claim. |
| MCP server: F-439, F-544 | They close in the server release (task «#398»), not in this repo. |
| ENH-01 (Architect's Guide harvest) and ENH-02 (platform line overflow) | New content and platform work, not corrections. |
| F-218 | The register already says no KB work is owed. It is swept closed at the hand-off. |

### The bench rule (Stephen, 2026-10-08)

**We only do bench runs for things that are not covered in our ingested source documentation.**

- A row becomes a bench question only after an exhaustive search of the ingested sources finds
  them silent, or finds them contradicting each other on that point.
- Every bench question records that search: the terms, the files, and a control hit.
- Already-filed items (D, F-336, the G-rows) are re-checked against the sources first. A source
  that answers one retires its bench question.
- A question about a tool's limit is never a bench question. Tool limits are not KB facts
  (doctrine).

### Severity scale (agent-consumer framing)

| Severity | Meaning |
|---|---|
| **drives wrong code** | An agent writing code from this produces a wrong program |
| **wrong, not code-driving** | False, but nothing an agent writes depends on it |
| **latent** | Not wrong yet; wrong under a condition (a missing gate, an unsourced claim that happens to be true) |
| **hygiene** | Findability, provenance, structure |

### Freeze rule

Field reports keep arriving. A report that touches a file already in the study joins the study.
Anything else goes to the next cycle, so the close-out has a fixed finish line.

### What done means

The study is done when every in-scope row ends in one of three states:

1. **A complete change spec** — file, block, current text, correct text, and its authority
   (source `file:line`, or an EF/XF result).
2. **A decided bench result** that produced (1).
3. **A recorded reclassification.** Untestable and unsourceable means removed (F-381 reading 4).
   A missing document is named. A call that is Stephen's is answered.

Planning closes at that point. Tasking follows.

### Open questions for the scope (to settle before reading)

1. ~~v1.24.0: ship now, or fold into the close-out release?~~ **DECIDED 2026-10-08: fold in
   (option B).** Stephen: *"we need the new full closeout process."* There is no separate
   v1.24.0. Its 24 commits (the 22 applied fixes, plus the delivery-filter rule at schema 3.6.0)
   ship in the single close-out release, under the §1.5 change-set audit. The MCP go-live
   («#398», F-439) waits for that release.
2. **F-359's debug claims vs the tool-limits principle.** `trace_buffer` ("4–16 KB in hub") and
   possibly `debug_state` describe debugger and application memory rather than silicon. Doctrine
   says tool limits are not KB facts. The research reads the debugger and interpreter as decided,
   and if the answer turns out to be a tool limit, it is put to Stephen rather than stated.

---

## 2. Read order — written before reading (tick as covered)

0. [ ] **Ingestion prerequisites** (through `ingest-source` only):
   - (a) ingest the v55 Spin2 interpreter (now only in the XBYTE guide's `REF-NO-COMMIT/pnut-ts-parts/`);
   - (b) confirm which debugger is current (the copy we hold is byte-identical to v51);
   - (c) audit the operator ingestion: glued, missing or invented operators, and the `&lt;`/`&gt;`
     entities in `spin2-v55-text.txt`.
1. ~~Group E, field-report reconciliation~~ (dropped: every field report has been processed).
2. [ ] **Group A**, decided items: F-359, F-375, F-398, F-381 (24 files), F-547 cascade.
3. [ ] **Group B** by KB area: architecture, then language/spin2, then language/pasm2, then
   hardware, then guides.
4. [ ] **Group C**, knowledge gaps: the sources searched exhaustively for each one.
5. [ ] **Group D**, the bench queue: re-checked against the sources.
6. [ ] **Group F**, gate specs.
7. [ ] **Group G**, a class sweep per row (done as each row is read, and ticked here when the last
   row's sweep is in).
8. [ ] **Bench specification**: tests written to house style. Each starts as a
   VERIFICATION-OPPORTUNITIES row, is written in the owning manual's `audit/verification-tests/`,
   and is reviewed adversarially by a fresh agent before the run.
9. [ ] **Bench run, round 1 (Stephen)**: his run, with everything around it ours.
10. [ ] **Results**: an EF entry for each result, rows updated. An inconclusive run or a new
    question gets a round-2 test.
11. [ ] **Planning closes**: every row in a done state (§1). Hand-off to `sprint-plan`.

After the sprint's tasks, the single close-out release goes through `release-yamls` **§1.5,
the change-set audit** (added 2026-10-08). Every hunk since the last tag is audited
adversarially by agents that made none of the changes: wanted, warranted and correct against a
source or bench result, removals justified, siblings complete. Stephen then reviews the audited
set before any tag.

Reading is dispatched per group to fresh read-only agents. Each return is a claim, and the
arbiter verifies its cited lines before a row enters the register. **Nothing in
`deliverables/ai/P2/` changes during the study.**

---

## 3. Findings register

| # | Group | Item | Severity | Finding | Evidence | Mark | Root cause | Resolution (change spec / bench Q / reclass) | Trivially safe? |
|---|---|---|---|---|---|---|---|---|---|
| | | | | *(empty until the scope is agreed)* | | | | | |

## 4. Root-cause groups

*(filled as rows accrue)*

## 5. Bench questions

| VO id | Row(s) | Question | Sources-silent proof (terms · files · control hit) | Test file | Status |
|---|---|---|---|---|---|

## 6. Not read, and why

*(filled at hand-off)*

## 7. Hand-off to `sprint-plan`

*(filled when planning closes)*
