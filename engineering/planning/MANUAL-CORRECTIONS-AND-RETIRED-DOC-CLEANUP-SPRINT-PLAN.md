# Manual Corrections + Retired-Doc Cleanup — Sprint Plan

**Head:** manual production (deSilva, XBYTE) + repo hygiene
**Origin:** the 2026-08-14 forum docs-feedback sweep — findings **F-254…F-258** in
`engineering/operations/P2KB-CORRECTION-FINDINGS.md` — plus the retired-doc archive cleanup.
**Analysis:** `engineering/document-production/FORUM-NO-COMMMIT/Docs-findings-360813/DOCS-FINDINGS-ANALYSIS.md`
(gitignored; find by path).

**Community bench review:** `p2-manuals-review-findings.md` (the posted zip) — folded in as **§7**,
findings **F-259…F-263**, all five verified and all five in **RELEASED** manuals.

**Not in this sprint:** F-253 (P2KB YAML, accumulating for the next YAML flush per Stephen);
F-258 (RESOLVED-INVALID, no work); the findability pass and TonyB_'s restructure proposal (editorial
decisions — see §Open Question 5).

---

> ## LIFECYCLE — this plan is HALF CLOSED
>
> This plan carries **two sprints**, split by Stephen on 2026-08-15.
>
> **SPRINT 1 — guide normalization — CLOSED 2026-08-15.** All 11 tasks `«#205»`–`«#215»` certified.
> Audit: `engineering/history/sprints/2026-08-15-guide-normalization-sprint-1-CLOSEOUT.md`.
> Exit: instrument **PASS 0/28**, three entry validators unchanged, **zero opus-master edits**.
> No versioned artifact shipped. See *Sprint 1 — OUTCOME* and *Carried into Sprint 2* at the end.
>
> **SPRINT 2 — the manual work — OPEN.** Sections **§1–§5, §6, §7, §8** and the *Sequencing* block
> are Sprint 2's, plus the six carry-forwards Sprint 1 produced. Nine targets, seven version bumps.
>
> **This plan is therefore NOT archived.** It stays in `engineering/planning/` until Sprint 2 closes.

---

## Bench leg — COMPLETE 2026-08-14 (results, and what they change)

The sequencing note's batched bench session (§3, §7a re-proof, §7b, §7e) ran on 2026-08-14.
Full evidence: `campaigns/2026-08-manual-corrections/`, findings register F-253..F-266.

| plan item | finding | bench outcome |
|-----------|---------|---------------|
| §7a | F-259 | **REVISED — the guide is RIGHT.** TT=%01 drives (6,737 vs 1,408 off). The community report is not reproduced. The real defect is `+` composition of pin constants, which carries `%01+%01` into `%10`. Class sweep: 281 lines use `\|`, exactly 2 use `+`, both in the Streamer Guide (`:1238`, `:1306`), both currently computing correctly — a latent trap, not a live bug. Reproduced 3x. |
| §7b | F-260 | **RESOLVED — the mode WORKS.** On-target magnitude 1,059,000 vs 2,575 (2x detune), 286 (0.5x detune), 430 (null). **The missing protocol** — with a discrete `XINIT`/`WAITXFI`/`GETXACC` sequence, absolute accumulator reads do not track the input; the difference across one command does. Author the protocol, **not** a mechanism: we have NOT established that the accumulators are never cleared, and Chip's `XCONT`-loop demo is evidence against that reading. Doc corrections still required: undeclared `dds_s`; `adc_pin<<17` valid only for multiples of 4; and the protocol itself. |
| §7b sibling | `:607` | **CONFIRMED — mode corruption, bench-proven.** Byte-count signature 1024 / 2048 / 4096 as `adc_pin` rises, because the shift carries into `D[19:16]`. Reproduced 4x. **Needs a confirming run** — see below. |
| §7e | F-263 | **CONFIRMED with cause.** No hub access inside either CORDIC loop; Chip's model vindicated. 7 consistent runs. P2AN002 and Assembly ch.5 both violate it. |
| §3 | F-256 | **ANSWERED — and the answer triggers this section's own error clause.** `_RET_ CALL` does **not** return to XBYTE; it behaves as a plain `CALL` and execution falls through into the following code. `pnut-ts` does emit the `_RET_` form, so this is silicon, not a compiler bug. **§4 therefore needs restructuring, not just a `set_nz` definition** — exactly the contingency Open Question 2 flagged. |

**New findings this leg, not previously in the plan:** F-264 (`wrpin.yaml`'s `tt_field` flattens
four context-dependent `%TT` meanings and tells readers to add `P_OE` to DAC outputs, which kills a
level-driven DAC), F-265 (**resolved** — Goertzel ADC pins are raw, no smart-pin mode, no DIR), and
F-266 (**the debug interrupt disrupts the streamer; `DEBUG_COGS` defaults to all eight cogs**, and
nothing warns a streamer author).

### SPLIT INTO TWO SPRINTS *(Stephen, 2026-08-15)*

This plan is being split. The voice work is not a sub-task of the manual work — it is the
**standard** the manual work is measured against, and it currently contains contradictions that
would misdirect that work.

| | sprint | contents | release model |
|---|--------|----------|---------------|
| **1** | **Normalize the guides** | all voice guides + creation guides + the house layer (voices catalog, app-note voice guide); the E1 reconciliation sweep; E2/E3 adoption decisions; the damage *investigation* | no renders, no PDF wave, no manual version bumps |
| **2** | **The manual work** | the nine correction targets below; any text repair the damage investigation turns up | full renders, version bumps, coordinated release wave |

**Why the split is forced, not tidy.** P2 — the divergence audit that *scopes* the manual work —
cannot run against a moving standard. And the guides today would actively misdirect an author: one
following IOSP's *"Never hedge"* rule would strip exactly the qualifiers §2.2a requires. Fixing the
standard first is the only order that does not waste the measurement.

**Damage placement:** the *investigation* (did the word-blacklist checklists cause qualifier
removals in released text?) sits in Sprint 1, because Sprint 1 artifacts caused it. Any *text
repair* is Sprint 2 work.

---

### SETTLED 2026-08-15 — the voice-guide tree *(Stephen approved)*

The sizing question this section previously left open — *"define once in the catalog"* vs *"copy
into all eleven"* — **was a false binary, and the catalog had already answered it.** Commit
`3d8a653c` (2026-07-20, *"voices-catalog: add per-voice failure modes + shared discipline"*) added a
normative **"The Shared Discipline — applies to every voice"** section that states the rules and then
says: *"The write-time counterparts live in each manual's voice-guide (template: the XBYTE guide's
§2.2a … and §2.4)."* Six of ten guides already cite the catalog as canonical. **The model is
canonical statement in the catalog, local adaptation in each guide** — one house edit plus ten
adaptations, not eleven parallel authorings.

**The tree:**

| Layer | File(s) | Owns | Boundary rule |
|-------|---------|------|---------------|
| **House canon** | `engineering/standards/documentation-standards/documentation-voices-catalog.md` | the seven voices + failure modes; the Shared Discipline rules stated once, normatively | rules are **stated** here and nowhere else |
| **Class** | `app-notes/APP-NOTE-VOICE-GUIDE.md` (the `P2ANxxx` series) | register blend for a document class | adapts house rules for the class; never restates them |
| **Document** | each manual's `voice-guide.md` | reader, register(s), terminology, section-specific voice, **and the local adaptation of each house rule** | per rule: **ADOPT / ADAPT / REJECT, with a reason** |
| *(adjacent)* | each manual's `creation-guide.md`, `style-guide.md` | what goes where; presentation | **may reference voice rules, never restate them** |

**Three structural rules hold it together:**

1. **Never restate a shared rule — adapt it.** A restatement goes stale; an adaptation with a reason
   does not.
2. **Record rejections.** An undocumented rejection reads as an oversight and gets "fixed" by the
   next sweep — this is how DeSilva would lose its voice.
3. **Quality checklists point at rules; they never re-encode them.** This single rule would have
   prevented every contradiction catalogued in the study.

**The house layer goes to FOUR named rules.** The catalog's Shared Discipline and Chip's three tweaks
are not the same three things — the catalog has {calibrated confidence · payoff-sentence test ·
cadence}, the origin has {calibrated confidence *(payoff folded in)* · anti-pattern rows · cadence}.
**E2 is missing from the house layer**, existing only as prose inside the Claude Voice failure-mode
paragraph, although seven of ten guides already carry the rows. Sprint 1 promotes it:

| | rule | maps to |
|---|------|---------|
| **R1** | Calibrated confidence — never state a claim above its evidence | E1 |
| **R2** | The payoff-sentence test — strip the flourish, read what remains as a bare claim | E1 (second half) |
| **R3** | The anti-pattern family — tutorial filler · reader-as-foil · self-admiration · staged reveal | **E2 (promoted)** |
| **R4** | Cadence budget — the metronome problem | E3 |

Every guide then declares against **R1–R4**.

**Sprint 1 scope, as settled:** one house edit (catalog → four rules, E2 promoted) · ten guide
adaptations covering **21 unreconciled sites** · one new DeSilva `voice-guide.md` · the app-note
guide's mislabelled row · a creation-guide pass under *reference, never restate* · the damage
investigation. This **supersedes** the "Open for Stephen" question in §B below (propagate only where
we are editing vs all ten): **all ten, plus the app-note guide** — the house edit makes the
remainder cheap, and leaving four guides unreconciled re-creates the drift.

---

### SPRINT 1 — STARTED 2026-08-15 (`sprint-start` record)

**Head / element.** Sprint 1 is **cross-cutting standards work**, not one element of one head.
Its target is the **guide layer itself** — the house voices catalog, the app-note class guides, and
every manual's `voice-guide.md` / `creation-guide.md`. `active_element` is therefore **left pointing
at the manual-corrections effort** and is not repointed; per `whats-next`, operations/standards work
has no `active_element` form.

**Build number: N/A — Sprint 1 ships no versioned artifact** (Stephen, 2026-08-15). It edits no
manual text, triggers no render, and bumps no version. The seven version bumps all belong to Sprint 2.
`BUILD_VERSION_*` therefore does not resolve for this sprint, by design rather than omission.

**Working-tree audit (§2).** `git status --short` **clean**; no untracked files anywhere in the blast
radius (`document-production/`, `standards/`, `planning/`). Nothing to commit, stash, or review first.

**Tracking readiness (§3) — READY.** Task board **empty** (no leftovers, nothing stranded, nothing to
archive). Context pruned **92 → 73 keys** (out of the audit band): deleted 19 superseded
resume/session-close/sprint-state snapshots, all of which declared themselves closed
(`nextup_session_close_*` ×6, `sprint_fabrication_audit_*` ×2, `nextup_fleet_*` ×2, five closed
Debug-Window pointers, the F-214/F-215 pair, the hub-RDLONG study, and the closed DeSilva P_OE
session). Snapshot taken first: `tasks/backups/project_dump_20260815_195233.json`. `MEMORY.md` 134
lines (under the ~150 threshold).

**Deliberately KEPT** — these are live or unrecoverable, not clutter:

| key | why kept |
|-----|----------|
| `nextup_preprocessor_p2kb_request` | live pending work — "STUDIED + SCOPED, **NOT STARTED**" |
| `nextup_asm_forum_response_post` | Stephen's to own; drafts live in gitignored `DRAFTS/` |
| `nextup_debug_outbound_docs` | awaiting Stephen's routing **and** gitignored — context is the only record |
| `donna_manuscript_state` | that tree is gitignored and unversioned — **git cannot recover it** |

*Cross-audit note (§4):* 19 resume-shaped snapshots had accumulated, i.e. supersede-and-delete is not
firing at session close. **First recorded occurrence — data, not yet a methodology candidate.** If the
same shape appears at closeout, it earns an entry in `feedback_skill_evolution_candidates.md`.

**Entry baseline (§4) — GREEN, and it is a *substitute* gate.**

| gate | result |
|------|--------|
| `verify-yaml-format.py` (true content-syntax gate per the overlay) | **1129 scanned · 1129 clean · 0 failed** |
| `validate-crossref-keys.py` | **ALL RESOLVED — 100%** (1823 `related:`, 717 `see_also:`, …) |
| `validate-dod-release.py` | **ALL VALIDATIONS PASSED** |

Per the overlay, `validate-yaml-syntax.py` was **not** used — it scans `manifests/` +
`knowledge-base/` and reports a green that verifies almost nothing of the content tree.

**Two honesty qualifiers on this baseline, both load-bearing:**

1. **It is a substitute gate, not a test suite.** It proves the YAML *parses and resolves*; it proves
   nothing *behavioral*. Behavioral verification for this project lives on the bench
   (`P2-EMPIRICAL-FINDINGS.md`), and none is in Sprint 1's scope.
2. **Sprint 1 touches no YAML at all**, so this baseline is a **no-regression anchor**, not a gate on
   the work. A green YAML baseline says nothing about the guide layer this sprint edits — **the guide
   layer currently has no automated gate whatsoever**, which is exactly why the plan's §6 owes a
   doc-audit instrument. `plan-to-tasks` §2a makes that a mandatory task.

**No failure groups. Nothing deferred. Exit baseline must match all three greens at closeout.**

---

### Planning-phase research — the two audits that scope this sprint

**These are planning work, not sprint work.** We cannot task the voice dimension without walking a
dependency chain, and each link is a research question:

> **propagation decision → what each guide will say → how far the shipped text diverges → the size
> of the job**

So two audits belong in the planning phase, before any task list is written.

#### P1 — Voice-guide propagation audit *(per gaining guide)*

**In progress: `VOICE-GUIDE-PROPAGATION-STUDY-2026-08.md`.** IOSP and Debug Window decided;
DeSilva and the partial set pending. It has already returned two results that change the work:

- **§2.2a is a RECONCILIATION, not an addition, for IOSP and Debug Window.** Both guides carry
  *"Never hedge"* as an explicit rule, which §2.2a corrects. Appending §2.2a would leave each
  guide self-contradictory, and an author obeying the older rule would strip exactly the
  qualifiers that keep claims honest — the failure this sprint's bench leg exists to remedy.
- **The Debug Window Manual has a large PRE-EXISTING voice debt**, documented in its own guide's
  migration note: the shipped v2 master is in an enthusiastic "Discovery Guide" voice the guide
  calls out of conformance with the entire house standard, and says *"bringing v2 into conformance
  … is a substantial rewrite."* Not created by this sweep, and it must not be silently absorbed
  into this sprint. P2 counts it separately from anything we introduce.

For each guide that would gain elements from the XBYTE audit, study each element against that
manual's voice and produce a written decision: **adopted · adapted (and how) · rejected (and why)**.
Rejections carry the most weight — an undocumented rejection reads as an oversight and gets
"fixed" by the next sweep, quietly converting a deliberate choice into a defect.

Deliverable: the **future text** of each target voice guide, decided. Until that exists, P2 cannot
run, because there is no standard to measure against.

Note the current propagation table below is a **keyword survey**, not a read. It says where to
look, not what is there — the Assembly guide shows more anti-pattern hits than XBYTE, which may be
extra local patterns or the same ones worded differently. P1 must read, not grep.

#### P2 — Manual-vs-new-guide divergence audit *(per manual we are touching)*

With P1's answer in hand, measure how far each manual's **existing** text sits from its **new**
guide. This is the number that scopes the sprint, and it separates two very different jobs:

| job | scope | negotiable? |
|-----|-------|-------------|
| **New prose we write** conforms to the new guide | small — our corrections only | **No.** Mandatory. |
| **Legacy shipped text** conformed to a newly-tightened guide | potentially large | **Yes — a scope decision, and Stephen's.** |

Conflating those two would turn a correction sprint into a fleet-wide re-edit. They must be
counted separately.

**Tooling already exists, and it carries fleet data.** `document-audit` **Dimension #4c —
payoff-sentence sweep** was created by this very XBYTE audit (2026-07-20). Its guidance is directly
relevant to scoping:

- It extracts **by position, not vocabulary** — every last sentence before a heading and before a
  closing `:::`.
- *"Reference-voice documents — entry-per-instruction, table-driven — do not produce this defect; a
  fleet probe over **65,509 master lines** found it concentrated in a **single document**."*
  So the legacy-remediation risk for our reference-voice targets is probably small. **P2 should
  confirm that by measurement rather than assume it in either direction.**
- **Run #4c before the tone pass** — it produces the falsifiable subset, and the tone findings fall
  out as a by-product.
- **A `#4c` finding is never closed by rewording.** If a beat carries a false claim, the *claim* is
  corrected or removed — not softened. That rule matters here: our own §17.1 rewrite will be
  written to a cadence budget, and we must not let tone work paper over accuracy work.

#### P3 — Output of the planning phase

1. The decided future text of each affected voice guide (from P1).
2. A per-manual divergence count separating *new-prose conformance* from *legacy remediation* (P2).
3. A scope recommendation for the legacy half, for Stephen's decision.

Only then is the correction map below tasked.

---

### Voice-guide conformance and the in-flight propagation sweep

**Two requirements sit on top of every edit in this sprint, and one of them reorders the work.**

#### A. Every edit must conform to its manual's own voice guide

Each manual carries its own: `voice-guide.md` for most, `desilva-style-guide.md` (plus
`why-desilva-voice-works.md`) for DeSilva, `style-guide.md` alongside the voice guide for the
Assembly manual and the Smart Pins Tutorial.

> **Sprint 1 closes the DeSilva exception.** DeSilva is the one element where the conventional
> `<element>/voice-guide.md` lookup returns nothing — which is precisely why it sat outside the
> propagation, and why the next sweep would miss it too. Sprint 1 authors a **thin new
> `voice-guide.md`** there: reader/register identity, the R1–R4 declaration table with per-row
> reasons, and pointers out to `why-desilva-voice-works.md` (rationale, including its standing
> *"DON'T Add These Modern 'Improvements'"* guard) and `desilva-style-guide.md` (presentation). The
> style guide keeps its formatting remit — it calls itself the source of truth for *formatting*
> decisions, so that boundary is already clean — and gains one back-pointer under *reference, never
> restate*. **Our corrections are new prose in released documents
and must read as though the original author wrote them.** This matters most for the Streamer
Guide's §17.1, which is not a token fix but real new teaching content.

Practically: before editing a manual, read its voice guide; after editing, re-read the new prose
against it. A correction that is factually right and tonally foreign is still a defect.

#### B. A voice-guide propagation sweep is part-way done, and it collides with the correction map

The XBYTE guide's audit produced three voice-guide changes (commit `acf3b4a2`, *"three tweaks from
Chip's voice critique"*): the **anti-pattern rows** (tutorial filler · reader-as-foil ·
self-admiration · staged reveal), **§2.2a calibrated confidence is required — it is not hedging**,
and **§2.4 cadence budget** (the "metronome" problem — at most ~half of section closings may be
beats, never more than ~4 in a row, chapter closers worst). Those have been propagating outward,
unevenly.

**State of the sweep** — **superseded TWICE, and now CLOSED.** First by the read-based survey in
`VOICE-GUIDE-PROPAGATION-STUDY-2026-08.md`, then by the mechanical inventory «#206» built — and as
of **2026-08-15 the sweep is finished**: the instrument reports **PASS, 0 findings across 28 files**
(`python3 engineering/tools/validation/audit-guide-conformance.py --inventory`). Every row below now
reads ✅ ✅ ✅. **Do not read the table for current state — run the instrument.** It is kept only as
the record of what the original keyword pass claimed, and of how badly a keyword pass can miss:

| manual | calibrated confidence | cadence budget | anti-patterns | state |
|--------|----------------------|----------------|---------------|-------|
| XBYTE | ✅ | ✅ | ✅ | **origin** |
| Streamer | ✅ | ✅ | ✅ | full |
| Assembly | ✅ | ✅ | ✅ | full |
| Architect | ✅ | — | ✅ | partial |
| Getting Started | ✅ | — | ✅ | partial |
| Single-Step Debugger | ✅ | — *(WRONG — present, added `04f6e4e2` 2026-08-11)* | ✅ | partial |
| PNut-Term-TS | ✅ | — *(WRONG — present, added `04f6e4e2` 2026-08-11)* | ✅ | partial |
| **I/O & Smart Pins** | — | — | — | **none** (guide untouched since 2026-01-25) |
| **Debug Window** | — | — | — | **none** (untouched since 2026-06-01) |
| **DeSilva** | — | — | — | none, and deliberately so |

**The corrections both shrink the sprint.** Cadence (R4) is present in **five** guides, not three;
Single-Step and PNut-Term-TS each drop to a one-line fix. The keyword pass also undercounted the
anti-pattern rows in Architect and Getting Started (they write "reader-as-foil" where XBYTE writes
"besserwisser"). **Grep misled four times across this study — read, do not grep.**

**The collision.** I/O & Smart Pins (target #2) and Debug Window (target #5) are both correction
targets *and* have entirely un-propagated voice guides. Editing them first would write new prose to
a stale standard that a later sweep flags — our own corrections failing the audit.

**Sequencing rule that follows: a manual's voice-guide propagation is decided and applied BEFORE
its text is edited.** For IOSP that means the propagation study comes ahead of the F-261 fix.

#### C. Propagation is a study, not a copy

The elements are not equally portable. Proposed discriminator, to be confirmed per target:

- **Accuracy elements propagate everywhere, including highly stylized manuals.** §2.2a's rule —
  *never state a claim above its evidence* — is about truthfulness, not register. It applies to a
  chatty tutorial exactly as it applies to a reference, and this sprint is the case in point: the
  bench leg exists because claims outran evidence.
- **Register elements are voice-dependent.** Cadence budget, reader-as-foil, staged reveal,
  self-admiration. In DeSilva several of these might be *the voice itself*, which is why
  `why-desilva-voice-works.md` exists as its own rationale — propagating them blindly would flatten
  the thing that makes the manual valuable.

  **DECIDED per-row 2026-08-15 (see the study).** The evidence overturned the working hypothesis:
  reader-as-foil and self-admiration **reinforce** rules DeSilva already has, tutorial filler is
  **rejected** (the origin's own §2.3 permits it here), and **staged reveal is adopted as a defect
  but not as a phrase ban** — a read of all reveal-vocabulary hits in the 6,176-line master found
  **zero instances of the actual defect** (withholding across a boundary) and three signposts where
  the fact lands in the same sentence. Banning the phrases would flag three false positives and
  catch nothing. **R4 (cadence) is rejected for DeSilva**, reasons recorded in the study.

**Per-target deliverable.** For each gaining voice guide, a short written decision: which elements
are adopted, which are adapted (and how), which are rejected (and why). The rejections matter most
— an undocumented rejection reads as an oversight and gets "fixed" by the next sweep.

**RESOLVED 2026-08-15 — all ten, plus the app-note guide.** This question ("propagate only where we
are editing, or run to completion?") assumed eleven parallel authorings. Once the catalog is the
canonical statement, the remaining guides are cheap adaptations, and leaving four unreconciled
re-creates exactly the drift we are fixing. See **SETTLED — the voice-guide tree** above; the whole
sweep is Sprint 1, and Sprint 2 edits no guides.

### Correction map — which documents, and in what order

Nine targets. Released versions from `PUBLICATION-ROSTER.md`.

| # | target | released | findings | size of job |
|---|--------|----------|----------|-------------|
| 1 | **P2KB YAML** `deliverables/ai/P2/` | continuous | F-264 (`wrpin.yaml` `tt_field` + `p_oe_required_for`), F-265 + `usage_pattern` defects (`dds-goertzel.yaml`), F-266 surfacing, F-253 | medium, no render |
| 2 | **P2 I/O & Smart Pins User Guide** | v1.0.8, 396pp | F-261 — power groups FOUR→EIGHT, three repairs (`chapter-16-adc.md:263`, `:382`, and the layout rule built on it) | small, answer already in F-211 |
| 3 | **P2 Streamer Programming Guide** | v1.0.8, 73pp | F-259 (`:1238`, `:1306`), F-260 §17.1 (`:1324`, `:990`), `:607`, F-266 warning, `##hubsym` ENH | **largest — real new prose** |
| 4 | **P2 Assembly Language Reference** + **P2AN002** | v3.1.5 503pp / v1.0.2 14pp | F-263 — `chapter-05-hardware.md:~100-126` and `examples-library/cordic-pipeline-throughput.spin2` | medium; same finding, two docs |
| 5 | **P2 Debug Window Manual** | v1.1.2, 168pp | F-262 — FFT chapter channel-default column | small |
| 6 | **DeSilva PASM2 Tutorial** | v3.0.5, 164pp | F-254 Acknowledgments, F-257 Appendix A | small |
| 7 | **P2 Interpreters & Emulators Guide** | v1.0.1, 100pp | F-256 (`:879`, `:416`, `:793`, `:1391`, `:1400`), F-255 §15.3 | **gated** — shape depends on the confirming run |
| 8 | **Retired-doc cleanup** | — | §5, Smart Pins Tutorial out of the search path | independent |
| 9 | **Release wave** | — | §8 | after the above |

**Why this order.**

1. **YAML first — it is upstream.** F-264 is the root of a class: `wrpin.yaml`'s `tt_field` is the
   file F-245 was resolved against, and its `p_oe_required_for` is what would tell an author to add
   `P_OE` to a cog-DAC config and break it. Correct the source before correcting the documents that
   cite it, per the trust chain. No render, so it costs little.
2. **IOSP next — highest-severity manual defect.** A RELEASED manual contradicting our own
   published KB (v1.15.0) *and* our own app note P2AN001, on a fact we settled a month ago. No
   research needed. It is also the cleanest demonstration of the process finding: F-211 landed in
   the YAML and never reached the manuals.
3. **Streamer Guide third** — the biggest authoring job, and where most of the new TEACH content
   lands. Doing it after the YAML means §17.1 is written against a corrected `dds-goertzel.yaml`
   rather than the reverse.
4. **Assembly ch.5 + P2AN002 together** — one finding, two documents; writing them in one sitting
   keeps the wording consistent and the rule stated identically in both.
5–6. **Debug Window and DeSilva** — small and independent; either can be pulled forward to ride a
   render if scheduling favours it. Note the sprint's Open Question 1 recommends DeSilva re-release
   as **v3.0.6** rather than waiting, since F-254 is a public-facing credit claim.
7. **XBYTE last of the content work** — §4's shape depends on the `_RET_ CALL` confirming run. Do
   not start it early and write it twice.

**All seven content targets are PAST RELEASES** — IOSP v1.0.8, Streamer v1.0.8, Assembly v3.1.5,
P2AN002 v1.0.2, Debug Window v1.1.2, DeSilva v3.0.5, XBYTE v1.0.1. Every one needs a version bump
and re-release, and every one corrects text readers already hold. The two exceptions are #8
(retired-doc cleanup — repo hygiene, not a released document) and #1 (the YAML — published, but on
the KB commit/tag/push cadence rather than a PDF render).

**Voice-guide gate:** for IOSP and Debug Window, the propagation decision (§B above) precedes the
text edit.

**Decisions that are Stephen's, not mine:** whether DeSilva re-releases on its own or rides the
wave; whether the cross-cutting TEACH items (bit-field composition, `DEBUG_COGS`, the `$400` hub
address) live in each manual or in one place referenced from several; and how wide the F-259 `+`
class sweep goes beyond the two known lines.

### Authoring source

The bench leg produced more than corrections: it produced **positive teaching material** about how
these features actually work, most of it absent from every doc we ship. That is written up for
authoring in
`campaigns/2026-08-manual-corrections/BENCH-FINDINGS-FOR-AUTHORING.md` — each test with its
question, rig, measured results and discovery path, and every outcome tagged **CORRECTION** (the
doc says something wrong), **TEACH** (the doc omits something the reader needs) or **TRAP**
(something that will bite a reader, found by being bitten).

The highest-value TEACH items, none of which are defects in the ordinary sense:

- **Absolute Goertzel accumulator reads are not a per-command measurement** (in the discrete
  `XINIT`/`WAITXFI` pattern) — take the difference across a command, or follow the shipped demo's
  `XCONT` loop with an initial baseline. Without this the mode looks dead while returning large,
  stable, plausible numbers. **Do not write "the accumulators are never zeroed" — unproven.**
- **Debugging streamer code with `-d` puts the P2's highest-priority interrupt inside your
  streaming cog** by default. One CON line fixes it; nothing warns anyone.
- **`%TT` is four different fields** depending on smart-pin and DAC_MODE state — and our own
  `wrpin.yaml` currently teaches only one of the four.
- **Pin-mode constants are bit fields**: combine with `|`, never `+`.
- **`##hubsymbol` inside a Spin2 object's DAT resolves against `$400`**, not the object's load
  address.

### Confirming runs required before §4 and the `:607` edit

F-266 was discovered *after* the F-256 and `:607` measurements, and both were made with the debug
interrupt live inside the launched cog. **Neither is in doubt, and neither blocks authoring:**

- **`:607`** — debug interference causes jitter and dropped samples; it cannot turn one byte per
  rollover into exactly two or exactly four, since the write width is set by the mode field. The
  counts hit the a-priori prediction exactly, four times.
- **`_RET_ CALL`** — a differential test whose reference arm ran in the same cog and same run under
  identical conditions and behaved correctly, corroborated by the pushed return address matching
  the map and by the compiler emitting the `_RET_` form.

The confirming session is **cheap insurance plus the §3 error clause** — a process gate we set
ourselves, requiring an independent path before restructuring a chapter. Both probes carry
`DEBUG_COGS = %0000_0001` and can ride the next time the board is out. **Do not hold the rest of
the sprint for it;** the only thing genuinely gated is §4's final shape.

## Open Questions — resolve before tasking

Per the sprint-plan gate, these are unresolved and each carries my recommendation.

**1. Does deSilva re-release, or do the fixes ride the next natural release?**
deSilva shipped **v3.0.5 on 2026-08-11** — three days ago. Sections 1 and 2 both change it.
*Recommendation: **re-release as v3.0.6.*** F-254's reviewer-credit block may assert a review
process that did not happen, in a publicly downloadable PDF, and it is the specific thing a
community member objected to. Holding a known-defective credit claim for an unspecified later
release is the "mentioning a known defect without fixing it" failure our own quality bar names. The
fix is small, the render is cheap, and the goodwill return is immediate.

**2. Is the `_RET_ CALL` bench test (F-256) inside this sprint — and does §3 gate §4?**
They are coupled and I do not think the plan can pretend otherwise: **if `_RET_ CALL` does not
behave as the guide asserts, §15.3's handlers need restructuring, not just a `set_nz` definition.**
*Recommendation: **yes, include it, and run it first.*** It is a jumper-free single-board test
needing only your bench. Sequencing it ahead of §4 avoids writing the fix twice.

**3. How aggressive is the retired-doc reference cleanup?**
The reference count is **49 files / ~130 hits** — far more than the "~20" I quoted you, and the
majority are **legitimate history** (closed sprint plans, closeouts, a dated forge snapshot, the
canonical-naming migration plan). *Recommendation: **classify, do not purge.*** Fix only the docs
that present the tutorial as a **current, live manual**; leave historical records untouched; leave
lineage citations in other manuals' creation-guides ("adopted from Smart Pins") alone, since that
provenance is true. Detail in §5.

**4. RESOLVED — the bench review is in hand and folded in as §7.**
All five findings verified against our sources and filed as F-259…F-263. **They outrank §1–§2 in
severity** — technically wrong content in five released manuals, versus a credits block. The
sequencing section is reordered accordingly. Two follow-on calls this raises:
*(a)* **§7a and §7c are both class-wide sweep failures** — F-245's `P_OE` fix and F-211's 4→8 fix
each landed in the YAML and never reached the manuals. *Recommendation: make "does this correction
have a manual-side sweep?" a standing step, not a per-finding remembering.*
*(b)* **§7b's silicon question may need Chip.** *Recommendation: give our bench one pass first; if
the DDS/Goertzel mode still will not run from the documented command word, it goes to
`DRAFTS/QUESTIONS-FOR-CHIP-GRACEY.md`.*

**5. Findability work and TonyB_'s restructure — out of scope, confirm?**
Both are editorial judgment calls, not defects. F-258 established the XBYTE technical framing is
already correct; the problem is that readers are not reaching it. *Recommendation: **out of this
sprint**, tracked in the analysis doc for a separate decision.*

---

## 1. deSilva Acknowledgments — remove the self-listing, the unearned credit, and the false AI claim

**Finding:** F-254 · **Doc:** deSilva (**SHIPPED v3.0.5**) ·
`manuals/p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER.md:113–160`

**Why.** Four defects in one block, in a published document. A community member raised the first
publicly; the other three were found while verifying it.

**Current state → target:**

| `:line` | Current | Target |
|---|---|---|
| `:113` | *"This manual stands on the shoulders of giants. We gratefully acknowledge:"* | Delete the opener. Plain `# Acknowledgments` heading, matching every other manual in the set. |
| `:115` | `### Primary Contributors` | Delete the heading. |
| `:119` | **Iron Sheep Productions LLC (Stephen M Moraco)** listed among those thanked | **Remove entirely** — the author belongs on the title page, not the thank-you list. |
| `:129–135` | `### Technical Reviewers` + three generic placeholders (*"The P2 Documentation Team at Parallax"*, *"Community members who beta-tested examples"*, *"Everyone who reported errors"*) | **Delete the block** — unless real named reviewers can replace it, which is strictly better. |
| `:137–143` | `### Inspiration` — MIT AI Lab, Knuth, Demoscene | Delete. None contributed to this work. |
| `:150` | *"AI-assisted content generation **trained on** deSilva's writing style"* | **Factually false — nothing was trained.** Replace with what is true: AI-assisted authorship *in the style of* deSilva's P1 tutorial, with every example compiled. |
| `:154` | Closing Newton quotation (a second use of the same idiom) | Delete. |

**Keep:** deSilva and Chip Gracey, acknowledged plainly. The target shape is the one every other
live manual already uses — Parallax, Chip Gracey, the P2 community.

**Verification.**
*Normal:* the rendered PDF's Acknowledgments page shows no author self-listing, no giants line, no
generic reviewer credits, no AI-training claim.
*Edge:* the two inert in-folder copies (`opus-master/archived-2025/COMBINED-COMPLETE-MASTER.md`,
`initial-chapter-generation/00-acknowledgments.md`) are **not** assembled into the render — confirm
they stay out rather than editing them.
*Error:* re-run the F-254 class sweep across the live set after the edit and confirm it returns
clean, so the fix does not merely relocate the text.

---

## 2. deSilva Appendix A — add the missing competitor and the software axis

**Finding:** F-257 · **Doc:** deSilva (**SHIPPED**) · `COMPLETE-OPUS-MASTER.md:5876+`

**Why.** Three concrete gaps, all raised by a critic who is right about them:

1. **RP2040/RP2350 (Pico 2 / 2 W) is absent** from a table listing STM32, ESP32, Arduino/AVR,
   PIC32, P2. It is the current default for a large share of hobby projects, and its PIO is the
   nearest real competitor to the P2's pin-level story. Omitting it reads as avoidance.
2. **The comparison is hardware-only** — cores, peripheral location, timing — and never mentions
   libraries, ecosystem, or language. Arduino / ESP-IDF / MicroPython versus learning Spin2 + PASM2
   is, for many readers, *the* deciding factor. A comparison that omits the axis where we are
   weakest earns the "marketing leaflet" charge.
3. **Price is unmentioned** (Edge modules) — independently echoed by a second community member.

**Target.** Add the RP2350 row. Add a software/ecosystem dimension that **states plainly where the
P2 loses**. Keep the existing technical claims — they are accurate and already properly hedged
(the "2 clocks" passage correctly calls itself a lower bound; do not touch it).

**Consider adopting Christof's framing**, which is sharper than ours and comes from a critic:
> *"the probability to succeed in a project is higher, because you can always fall back to dedicate
> a core to some time critical part — much more easy than working with interrupts."*

That is a **risk-of-failure** argument, which is what an engineer choosing a platform actually
weighs. He also notes the eight-cores line "has been said so often already in these manuals."

**Verification.**
*Normal:* the table carries RP2350; a software/ecosystem subsection exists and names concrete
weaknesses.
*Edge:* the honest-weakness text survives a hostile read — no weakness is stated and then
immediately neutralized by a rebuttal clause.
*Error:* every retained technical claim still traces to an authority (this is a shipped doc; no
unsourced comparative claims).

---

## 3. Verify `_RET_ CALL` on silicon — gates §4

**Finding:** F-256 · **Status:** NEEDS-VERIFICATION · **Requires: Stephen's bench**

**Why.** `xbyte-body.md:879` states *"Chapter 15's `_RET_ CALL #set_nz` idiom depends entirely on
this,"* and the idiom is used at `:416`, `:793`, `:1391`, `:1400`. It **assembles clean** under
`pnut-ts` 1.55.3 — so the reader's "you can't combine a CALL with ret" is wrong as stated — but
**the compiler proves legality, not semantics.** Unresolved: when one instruction both pushes a
return address and returns, does control reach the helper and then return to `$1FF` with XBYTE
re-entry intact, or does the push/pop ordering break dispatch? Not answerable from the KB or the
Silicon Doc.

**Work.** Write a jumper-free probe: arm XBYTE, run a handler ending in `_RET_ CALL`, report whether
dispatch continues and the helper's effect landed. Single board, minutes.

**Deliverable.** An **EF-NNN entry** in `P2-EMPIRICAL-FINDINGS.md` either way — a load-bearing idiom
in a guide under community review must not remain unverified. Add the probe to the VO-J queue in
`VERIFICATION-OPPORTUNITIES.md`.

**Verification.**
*Normal:* the probe runs and reports a definite verdict.
*Edge:* **establish control first** — prove the rig reports a *known-good* handler correctly before
trusting its verdict on the `_RET_ CALL` case; a rig that cannot fail proves nothing.
*Error:* **if the result says the idiom is broken, stop and confirm the measurement** by an
independent path before acting — do not restructure a chapter on a single probe.

**Gate:** §4's shape depends on this answer. Run §3 first.

---

## 4. XBYTE §15.3 — define `set_nz`, and show the skip patterns the text claims

**Finding:** F-255 · **Doc:** XBYTE Guide (**in community review**, not released) ·
`manuals/p2-xbyte-programming-guide/opus-master/xbyte-body.md:1388–1401`

**Why — two defects.**

1. **`set_nz` is never defined anywhere in the manual**, yet `:1293` asserts *"A single shared
   `set_nz` helper serves most of the instruction set."* The two call sites need flags from
   **different registers** — `op_lda_imm` after loading `a`, `op_inx` after incrementing `x` — and
   the helper takes **no operand**. No shared result register, no calling convention. As written
   the pattern cannot do what the text claims.
2. **No handler shown carries a skip pattern**, yet §15.3's closing paragraph credits them with
   *"each opcode's table entry supplying the SKIPF pattern."* The examples do not demonstrate the
   mechanism the prose attributes to them.

**Target.** Define `set_nz` and make its calling convention explicit — a shared result register the
handlers load before calling, or an operand. Show at least one handler family with real skip
patterns so the section demonstrates its own claim. **Compile the slice.**

**Scope guard — do not inflate.** A sweep found **12 of 13 `call`/`jmp` targets in the guide are
undefined as labels**. **Only `set_nz` is a defect.** The other eleven (`pop_two`, `push_a`,
`push_value`, `read_opcode`, `hub_write_port`, `next_op`, `idle`, `int_ignore`, `odd_variant`,
`special_case`, `voice_on`) are legitimate illustrative stand-ins whose names carry their meaning
and whose internals are irrelevant to the lesson. `set_nz` differs *only* because the surrounding
prose makes a claim about the helper's shareability, which makes its contract load-bearing.
**Do not "fix" the other eleven.**

**Corroboration that the guide is not broadly broken:** the complete VM in §12.2 (`:975–1044`) was
extracted and **compiles clean** under `pnut-ts`.

**Verification.**
*Normal:* the revised §15.3 extract compiles clean; `set_nz`'s operand source is unambiguous from
the code alone, without reading the prose.
*Edge:* the handler family shown actually exercises a non-zero skip pattern.
*Error:* if §3 returned "idiom does not work," the handlers are restructured rather than patched —
and `:879`'s explanation and the other three `_RET_ CALL` uses (`:416`, `:793`) are revisited too.

---

## 5. Retired-doc cleanup — get the Smart Pins Tutorial out of the search path

**Origin:** it keeps surfacing in class-wide sweeps and reports. The durable fix is physical
removal from the live tree, not discipline.

**Current state.** Folders `manuals/p2-smart-pins-tutorial/` and `workspace/p2-smart-pins-tutorial/`
— **144 tracked files** — plus **49 referencing files / ~130 hits** across the repo. Roster status:
`## Abandoned — retired, not carrying forward`.

**5a. Archive the folders.** Move both to the gitignored `archive/` per
[[feedback_archive_retired_docs_locally]]. **Non-destructive** — git history retains everything, so
Sacred Rule #1 is satisfied. This is what removes it from every future grep.

**5b. Classify the references — fix only the live ones.** Three buckets:

| Bucket | Examples | Action |
|---|---|---|
| **Live process/reference docs** that present it as a current manual | `TEMPLATE-CATALOG.md` (15 hits), `PDF-PRODUCTION-ARCHITECTURE.md`, `pdf-generation-format-guide.md`, `REMOTE-TESTING-GUIDE.md` (7), `work-modes/production-pdf-generation.md`, `document-pipeline-queue.md`, `manual-production-working-set.md`, `STRUCTURE-GUIDE.md`, `document-production/README.md` | **FIX** — remove it from current-manual lists, or mark it retired inline |
| **Historical records** where the reference is true history | `engineering/history/sprints/**`, `forge-status-snapshot-2026-06-04.md` (17), `canonical-naming-plan.md`, closed sprint plans | **LEAVE** — rewriting history is worse than the noise |
| **Lineage citations** in other manuals' guides | IOSP / Assembly / Streamer / Debug Window creation- and voice-guides ("adopted from Smart Pins") | **LEAVE** — the provenance is accurate |

**5c. Orphaned filter fork.** `shared-assets/filters/p2kb-sp-semantic.lua` is consumed by **no live
manual** — the only `request.json` naming it is the retired tutorial's. Retire it with the folder.

**5d. Vestigial skip-list entry.** `engineering/tools/validation/audit-license-block.py:93` already
**excludes** the tutorial as superseded, so the archive move does **not** break it. The entry
becomes vestigial — remove it, with a comment noting the doc is archived.

**5e. Roster.** Keep the single `## Abandoned` row — that row *is* the history, and it is the
authority a sweep should consult. Note the archive location in it.

**Bonus unlocked.** `PUBLICATION-ROSTER.md:363` records that every live manual consumes
`p2kb-platform-mnemonic-bold.lua` *"the lone exception is the retired Smart Pins Tutorial, on its
own `p2kb-sp-` fork."* Archiving removes that exception, simplifying the platform-file prune rule.

**Verification.**
*Normal:* a class-wide grep for the slug returns only roster + history; no live process doc lists it
as current.
*Edge:* `audit-license-block.py` still runs clean over the live set after its skip entry is removed.
*Error:* `git log` still reaches the archived content — confirm before declaring done.

---

## 6. Documentation Blast Radius

> **RESOLVED 2026-08-15.** `DOC_AUDIT_COMMAND` was unset when this section was written, so the
> table below was composed **by hand**, as the skill directs — and the debt it recorded ("`plan-to-
> tasks` should generate a task to build one") became `«#206»`. The instrument now exists
> (`engineering/tools/validation/audit-guide-conformance.py`) and the slot is set
> (`.claude/skill-conventions.md:63`). It scans the **guide layer only**; it does not yet cover the
> artifacts below.
>
> **This section is SPRINT 2's blast radius and remains OPEN.** Sprint 1's `«#215»` carries the same
> name but covered a different artifact set (planning docs, `MANUAL-DESCRIPTOR.md` files, the
> structural proof). Exactly one row overlaps — the `HEAD-DISPATCH-DRAFT.md` check, now discharged.
> **Do not read the `Plan §6 → «#215»` cross-reference row as marking this section done.**

| Artifact | Why in radius | Section |
|---|---|---|
| deSilva `CHANGELOG.md` | Always in scope. New entry for v3.0.6 — and per the changelog style guide it describes **current state, never prior wrong state**: no "removed incorrect credits." | 1, 2 |
| deSilva rendered PDF + `-src.zip` in `deliverables/documents/DOCs/` | The shipped artifacts carry the defective text | 1, 2 |
| `deliverables/documents/README.md` release index | Version bump on re-release | 1, 2 |
| `PUBLICATION-ROSTER.md` — deSilva row + Platform Freshness Ledger `PUBLISH` line | Owned by `release-manual` at release | 1, 2 |
| XBYTE `CHANGELOG.md` | In-review draft; entry for the §15.3 correction | 4 |
| `P2-EMPIRICAL-FINDINGS.md` + `VERIFICATION-OPPORTUNITIES.md` | New EF entry and VO-J queue row | 3 |
| `P2KB-CORRECTION-FINDINGS.md` | **Annotate as you fix, same pass** — flip F-254…F-257 to `DONE` with applied-notes. A stale register lies. | all |
| Live process docs listing current manuals | Enumerated in §5b bucket 1 | 5 |
| `audit-license-block.py` | Skip-list entry removed | 5 |
| ~~`.claude/skills/HEAD-DISPATCH-DRAFT.md`~~ | **CHECKED «#215» — no action.** The row was wrong: the file does not reference the slug, and `git log -S` shows it never has. A hand-survey artifact. | 5 |

**Duplication watch.** The current-manual list appears in several process docs
(`TEMPLATE-CATALOG.md`, `PDF-PRODUCTION-ARCHITECTURE.md`, `manual-production-working-set.md`,
`document-pipeline-queue.md`). Per the skill's rule the fix is **one canonical copy plus links** —
`PUBLICATION-ROSTER.md` is already the declared source of truth, so these should reference it rather
than restate it. Editing four copies and hoping they stay aligned is exactly how this drifted.

---

## 7. Community bench review (refaQtor) — SETTLED ON OUR BENCH · F-259…F-263

> **REWRITTEN 2026-08-15.** This section previously carried ~120 lines of pre-bench analysis that
> read as live while the bench had already answered it, and an 18-task sprint was generated from it.
> Four of the five findings came back **different from the filing** — one was reversed outright. The
> stale text is deleted rather than banner-ed, and the per-finding verdicts are **not restated here**:
> a plan that summarises the register drifts from it, which is how this section and the register came
> to disagree within a day.
>
> **The register is the authority.** Read each finding there, status first, per
> `.claude/skills/REGISTER-CONSULTATION.md`. Evidence and authoring guidance live in
> `campaigns/2026-08-manual-corrections/BENCH-FINDINGS-FOR-AUTHORING.md`; measurements are ledger
> entries **EF-053…EF-060**.

**What each one turned into — pointers only, so this cannot drift:**

| § | Finding | Where it now lives | Head |
|---|---|---|---|
| 7a | F-259 | register + EF-054 | Streamer — **the guide's recipe is CORRECT**; the defect is `+` composition, 2 sites |
| 7b | F-260 | register + EF-056 | Streamer — **the mode WORKS**; author the protocol it never states |
| 7c | F-261 | register | IOSP — three repairs; needs no bench |
| 7d | F-262 | register | Debug Window — still needs the PNut observation |
| 7e | F-263 | register + EF-053 | Assembly ch.5 **and P2AN002** both violate the rule |
| — | F-256 | register + EF-058 | XBYTE §15.3 — **restructure**, not patch |
| — | F-264/265/266 | register + EF-055/056/057 | **KB** — these are the early YAML pass |

**Two consequences that change the sprint's shape, and they are the reason to read the register
before tasking anything:**

1. **An early YAML pass is now a real, scoped deliverable** — eight KB corrections, every one traced
   to an EF entry or a primary source and every one verified *absent* from the YAML tree. It runs
   **first**, because the manual text for Streamer §17.1 and Assembly ch.5 should derive from a KB
   that already carries the corrected facts rather than being written in parallel with it.
2. **P2AN002 joins the release wave** — its `examples-library/cordic-pipeline-throughput.spin2`
   violates EF-053 (`rdlong` in fill, `wrlong` in steady state). It was not in the original wave; the
   bench put it there.

---


## 7f. SPRINT 2 START — agreed versions, commit gate, entry checks (2026-08-15)

### ⛔ COMMIT GATE — opus-master edits are NOT committed by the agent

**Stephen's hard constraint, given at sprint-start.** Every change under any
`manuals/<slug>/opus-master/` or `app-notes/<n>/opus-master/` tree — the document prose
itself, which is this sprint's entire content deliverable (§1, §2, §4, §7a–7e) — is left
**uncommitted**. At the end of the opus-master work, stop and hand over the diff. Stephen wants
one opportunity to review the commit differences **before** anything is committed.

**This suspends central `task-handoff` §3c for those tasks.** Committing at the task boundary
to protect the work is normally right and is explicitly off here. Do not work around it by
committing one task's opus-master edits while "waiting" on another.

Still committable without asking, because none of it is the document: plan / punch-list /
register / standing-doc updates · tooling and instrument changes · `.claude/` skill and
convention changes · analysis artifacts. **A task that mixes both commits the non-opus-master
half only, and says so.**

Hand-back shape: the located change list (chapter + within-chapter section per item, per the
diagram-review-locations rule) alongside `git diff --stat` and the diff itself — so Stephen
reviews differences rather than reconstructs them. Then wait for his go.

### Agreed outgoing versions — every affected manual takes a PATCH bump

Stephen's call, 2026-08-15. Current versions from `PUBLICATION-ROSTER.md`:

| Manual | Sections | Now | Ships as |
|---|---|---|---|
| DeSilva Tutorial | §1, §2 | 3.0.5 | **3.0.6** |
| Streamer Guide | §7a, §7b | 1.0.8 | **1.0.9** |
| I/O & Smart Pins (IOSP) | §7c | 1.0.8 | **1.0.9** |
| Debug Window | §7d | 1.1.2 | **1.1.3** |
| Assembly Reference | §7e | 3.1.5 | **3.1.6** |
| Interpreters & Emulators (XBYTE) | §4 | 1.0.1 | **1.0.2** |

**Six are pinned; the final count is not, and that is by design.** §7a's deliverable is a
**class-wide `P_OE` sweep across every live manual and app-note**, so which *additional*
elements bump is decided by that sweep's first run — the certified rule that an instrument's
first run is a planning input, applied to a sweep. Measured candidate set (2026-08-15,
`P_CHANNEL|P_DAC_` across live opus-masters): Streamer · IOSP · Assembly — all three already
bumping — plus **P2AN001 (1.0.3) and P2AN003 (1.0.2)**, which are *candidates only*. Many hits
will be constant tables, appendices and indexes that carry no defect. **Do not pre-commit
those two to a bump; size and confirm them after the sweep reads its sites.**
(`p2-smart-pins-tutorial` also matches and is **roster-Abandoned — never swept**.)

Also riding these renders, from the punch list: the front-matter `\markboth{}{}` one-liner that
**Streamer and Debug Window** are missing.

### Entry checks — both recorded, both green

**Working tree (sprint-start §2):** clean at `68b2bd5c`; no uncommitted edits and no untracked
files anywhere in the blast radius.

**Baseline (sprint-start §4)** — per the `sprint-start` overlay this is a **manual** sprint, so
there is no local build gate for the documents themselves (they render on PDF Forge); the
measurable entry baseline is the YAML head's validators, and it is **identical to Sprint 1's
exit**, so the exit assertion compares like with like:

- `verify-yaml-format.py` — **1129 parsed clean / 0 failed**
- `validate-crossref-keys.py` — **all cross-references validated**
- `validate-dod-release.py` — **ALL VALIDATIONS PASSED**

`BUILD_COMMAND` now names `verify-yaml-format.py`; it named `validate-yaml-syntax.py` until
2026-08-15, which returns a hollow green over the content tree. Never quote that script as the
baseline.

**Tracking (sprint-start §3):** board clean — Sprint 1's eleven tasks archived, nothing
stranded. Context pruned 73 → 55 keys (18 closed-work keys deleted, snapshot
`project_dump_20260815_223820.json` taken first). Two pending tasks «#216» «#217» are
skills-infrastructure from the v5→v8 reconcile and are **deliberately NOT folded into this
sprint** — they serve the toolchain, not the documentation release.

---

## 8. Release wave

§1, §2, §7a–7e touch **five released manuals** — deSilva, Streamer, IOSP, Debug Window, Assembly.
Per the wave rules: **stage shortest-first**, and any changed shared common-named file rides
**one** manual only. Each manual takes its own patch version and CHANGELOG entry (current-state
voice, never prior-wrong-state). `release-manual` owns the roster rows and the Platform Freshness
Ledger `PUBLISH` lines.

---

## Sequencing — the bench is DONE; the KB leads

> **REWRITTEN 2026-08-15.** The previous ordering batched a bench session that had already run on
> 2026-08-14, and ordered repairs against findings whose verdicts had since changed. Deleted, not
> annotated.

**The shape now, and the one structural rule behind it: the knowledge base leads the documents.**

1. **The early YAML pass** — eight KB corrections (F-259, F-260, F-263, F-264, F-265, F-266, G-004,
   EF-060). Every one traced to an EF entry or a primary source, and every one verified absent from
   `deliverables/ai/P2/` before being scoped. **Then release it** — patch bump, validators, index
   regenerated after the content commit, tag, push. Pushing is publishing.
2. **The manual repairs that need no further input** — IOSP §7c first on severity (a released manual
   contradicting our own published KB), then Streamer `+`→`|` and §17.1, deSilva §1 + §2, Assembly
   ch.5 and P2AN002 CORDIC, XBYTE §15.3 (a **restructure**, per EF-058).
3. **The one thing still owed from the canonical side** — §7d's FFT channel defaults, which need a
   PNut observation. Everything else proceeds around it; it does not gate the wave.
4. **The non-document work**, scheduled into any wait: retired-doc archive + reference classification,
   the descriptor-glob widening, the suppression probe.
5. **Blast radius + register annotation**, then the **⛔ review gate** — Stephen reads the accumulated
   opus-master diff before anything is committed.
6. **The release wave**, shortest-first.

**Why the KB leads, concretely.** Streamer §17.1's protocol text and Assembly ch.5's CORDIC rule are
*the same facts* as the KB entries for F-260 and F-263. Written in parallel they drift; written from
a published KB they cannot. This is also the standing fix for the recurrence §7c records — F-211 and
F-245 both landed in the YAML and never reached the manuals. Here the order is reversed on purpose.

**No bench session is scheduled.** The campaign completed 2026-08-14; its results are EF-053…EF-060.
The only canonical-side item left is the §7d PNut observation.

---


## Sprint 2 — section ↔ task cross-reference

Tag: **`manual-corrections-2`** · 20 tasks, seq 1–20 · est. **~34h**.
**Respecified 2026-08-15** after the original set was generated from pre-bench text. Rewritten in
place, not re-created, so these IDs stay valid as references. «#216»/«#217» (seq 21–22) are
skills-infrastructure and deliberately outside this sprint.

| seq | Task | Deliverable | Commit? |
|---|---|---|---|
| 1 | «#218» | **KB corrections ×8** — F-264 · G-004 · F-265 · F-260 · F-263 · F-266 · F-259 · EF-060 | ✅ |
| 2 | «#237» | **KB patch release** — publish so the manuals can cite it | ✅ |
| 3 | «#219» | IOSP ADC power groups, three repairs (F-261) | ⛔ |
| 4 | «#220» | Streamer `+`→`\|` at 2 sites + the composition rule (F-259) | ⛔ |
| 5 | «#221» | Streamer §17.1 — the mode WORKS; author the protocol (F-260) | ⛔ |
| 6 | «#222» | deSilva Acknowledgments (F-254) | ⛔ |
| 7 | «#223» | deSilva Appendix A + the line-167 R1 finding (F-257) | ⛔ |
| 8 | «#227» | XBYTE §15.3 — **restructure**, plus `set_nz` (F-255/F-256) | ⛔ |
| 9 | «#228» | Assembly ch.5 CORDIC — hub I/O out of both loops (F-263) | ⛔ |
| 10 | «#236» | **P2AN002 CORDIC** — same rule, shipped app note, four artifacts | ⛔ |
| 11 | «#229» | Debug Window FFT channel defaults (F-262) — needs the PNut observation | ⛔ |
| 12 | «#231» | Tool-name / codename / COG sweep in the releasing manuals | ⛔ |
| 13 | «#233» | Front-matter `\markboth{}{}` for Streamer + Debug Window | ⛔ |
| 14 | «#224» | Archive the retired Smart Pins Tutorial | ✅ |
| 15 | «#225» | Classify the 130 references; canonicalise the manual list | ✅ |
| 16 | «#226» | Widen the guide-conformance glob to descriptors, drive to zero | ✅ |
| 17 | «#230» | Suppression-at-write-time probe — IOSP first | ✅ |
| 18 | «#232» | Blast radius: changelogs, indexes, register applied-notes | ✅ |
| 19 | «#234» | **⛔ REVIEW GATE — hand Stephen the opus-master diff and WAIT** | n/a |
| 20 | «#235» | Release wave — **seven elements**, shortest-first | ✅ after go |

**What the respec changed, and why each was wrong before.** «#218» was "build the bench package" for
a bench that had already run — it is now the early YAML pass. «#220» ordered a P_OE sweep against a
finding our bench **reversed**. «#221» told an author to mark a working mode unbuildable. «#227» was
gated on a branch the bench had already decided — it is a restructure. «#228» was gated on a
replication that had already happened. «#236» is new scope the bench created: P2AN002 was not in the
wave until EF-053 put it there. «#229» lost its §7b half and is now the sprint's only
canonical-side item.

**The one structural rule the order encodes:** the KB leads. Streamer §17.1's protocol and Assembly
ch.5's CORDIC rule are the same facts as the KB entries at «#218» — written in parallel they drift,
written from a published KB they cannot.


## Sprint 1 — section ↔ task cross-reference

Tag: **`guide-normalization`** · 11 tasks, `«#205»`–`«#215»`, seq 1–11 · est. **11h 0m**.
Source sections: the plan's **SETTLED — the voice-guide tree** block and
`VOICE-GUIDE-PROPAGATION-STUDY-2026-08.md` §00 / §0c / §0d / §0e / §1.

| Source § | Deliverable | Task | seq | est |
|----------|-------------|------|-----|-----|
| SETTLED (house canon) · study §00 | Voices catalog → **R1–R4**, E2 promoted, 3 structural rules | `«#205»` | 1 | 60m |
| Plan §6 (instrument owed) · study §1 | **Guide-layer conformance instrument** + `DOC_AUDIT_COMMAND` | `«#206»` | 2 | 90m |
| Study §1.5 **D2** | `pnut_ts` → `pnut-ts` fleet sweep (~70 occurrences) | `«#207»` | 3 | 45m |
| Study §1.5 **D1** · §1.6 · plan §5b | Dead authority paths · retired-doc refs · codenames | `«#208»` | 4 | 45m |
| Study §0e · §1.5 **D3/D4** | **DeSilva** new `voice-guide.md` + the Sprint-2 gate | `«#209»` | 5 | 75m |
| Study §0c (🔴 HIGH tier) | **IOSP + Debug Window** — 10 voice sites + 1 creation checklist | `«#210»` | 6 | 90m |
| Study §1.3 (**Class B**) | Debug Window creation guide — retire the Discovery-Guide voice | `«#211»` | 7 | 75m |
| Study §0c (🔴 blacklists) · §1.4 (**Class C**) · §1.6 | **Assembly + Streamer** + the un-swept cog-casing fix + 3 collateral | `«#212»` | 8 | 75m |
| Study §0c (🟡/🟢 tail) | XBYTE · app-note · SSDB · PNut-Term-TS · Architect · Getting Started | `«#213»` | 9 | 60m |
| Study "Damage assessment" | **Damage investigation** (research only; repair is Sprint 2) | `«#214»` | 10 | 60m |
| Plan §6 | **Documentation blast radius** (owns every downstream artifact) | `«#215»` | 11 | 45m |

**Ordering rationale (rework pass, `plan-to-tasks` §3a).**
*Standards before application* — `«#205»` writes the canon everything else adapts to, so it is
unconditionally first. *Audit before execution* — `«#206»` builds the instrument **before** the
sweeps it verifies, which also replaces a hand count that has been wrong four times in this study
with a mechanically-derived one. *Discovery before utilization* — the mechanical class-wide sweeps
(`«#207»`, `«#208»`) run before the per-guide authoring so those passes see clean tool names and live
paths. `«#209»` sits early because **D4 gates Sprint 2**. The per-guide work then descends by
severity: 🔴 no-R1 → Class B → 🔴 blacklists → 🟡/🟢 tail.

**Atomic green-unit (`plan-to-tasks` §3b) — `«#206»` + `«#207»`…`«#213»`.**
`«#206»` switches detection on and will report roughly a hundred latent instances **at its own
completion**. That red is **by design, not a regression**, and must not be resolved by weakening the
detections — `«#207»`–`«#213»` clear the instances, and `«#213»` closes the unit. Both ends of this
are written into the task text so an executing agent does not "fix" its own correct work.

**Exit condition.** All three entry validators still green (`verify-yaml-format` ·
`validate-crossref-keys` · `validate-dod-release`), the instrument reports clean across the guide
layer, and `git diff --stat` shows **zero opus-master edits** — the structural proof Sprint 1 stayed
inside the guide layer.

### Sprint 1 — OUTCOME (2026-08-15, all 11 tasks complete)

| Task | Landed as | Result |
|---|---|---|
| `«#205»` | `add7da6c` | Catalog states R1–R4 as their sole home; R3 promoted to a 4-row family |
| `«#206»` | `2fb2be3d` | `audit-guide-conformance.py` — the guide layer's first automated gate; `DOC_AUDIT_COMMAND` set |
| `«#207»` | `e33d9cc8` | 66 `pnut_ts` → `pnut-ts` across 15 files |
| `«#208»` | `79695df7` | Dead authority paths · retired-doc pointers · 62 codenames |
| `«#209»` | `a62a5a40` | DeSilva gains a thin `voice-guide.md`; the Sprint-2 edit-vs-regenerate gate; the `::: your-turn` fence |
| `«#210»` | `bf3e14cd` | IOSP + Debug Window — 11 sites *reconciled* (not appended to), each gaining §3.4 + a shown R1 example |
| `«#211»` | `77d5c33c` | Debug Window creation guide stops teaching the voice it forbids |
| `«#212»` | `4e6da1c6` | Assembly + Streamer word blacklists deleted; cog-casing fix → **D6 added** |
| `«#213»` | `3a78a36a` | The tail; **green unit closes — guide layer reports PASS** |
| `«#214»` | `ac7124b9` | Damage investigation — **NIL**, count 0, severity none |
| `«#215»` | *this task* | Blast radius; descriptors repaired; structural proof produced |

**Exit condition MET.** `validate-crossref-keys` all-resolved (Sprint 1 touched no YAML); instrument
**PASS 0/28, D1–D6 all zero**; `git diff --stat add7da6c^..HEAD -- '*opus-master*'` **empty**.
Detection trajectory **176 → 113 → 45 → 43 → 0**, against an instrument that got *harder* mid-sweep
(three detections strengthened, D6 added, file set 27 → 28). **No versioned artifact shipped** —
no CHANGELOG entry, no version bump, per Stephen's decision at sprint start.

### Carried into Sprint 2 (from «#214» and «#215»)

1. **Suppression at write time — the open question «#214» surfaced.** The damage hypothesis tested
   removal, which diffs can see; the likelier exposure is qualifiers *never written*. Density per 1k
   body lines: blacklist manuals **1.31** (Streamer 0.56 · IOSP 0.82 · Assembly 2.55) vs **5.23**
   without. **Correlation only — confounded by genre, length and era; not a finding.** Test at
   content level. **IOSP is the priority probe.**
2. **Instrument coverage gap — RESOLVED 2026-08-15: widen to DESCRIPTORS ONLY.** Stephen's call.
   `MANUAL-DESCRIPTOR.md` (17 files) comes into the glob in Sprint 2; the
   `engineering/standards/documentation-standards/` tree does **not** — that half is punch-listed
   (*Guide-conformance instrument — standards-tree coverage*). The line was drawn on what serves a
   documentation release: `document-audit` resolves per-manual overlays **from the descriptors**, so
   a descriptor defect misdirects the audits that gate the releases; the standards tree is authoring
   infrastructure that reaches no shipped PDF.

   **Measured before tasking, per the certified rule that an instrument's first run is a planning
   input** (scratch copy, both globs widened, 2026-08-15): 28 files/**0** findings →
   63 files/**60** findings across 19 files. Split: **descriptors 38** (11 files) · standards tree
   22 (8 files). By detection: D2 `pnut_ts` 22 · D4 codename 31 · D6 all-caps COG 5 · D1 restated
   rule 2.

   **Size the descriptor task from the shape, not the 38.** 32 of the 38 are in the seven app-note
   descriptors (4–5 each) and are overwhelmingly **D2 — one cloned template defect**, not 32
   independent findings; they were bootstrapped from a common descriptor. The remaining 6 are spread
   across four manual descriptors. `p2-architect-guide/MANUAL-DESCRIPTOR.md` scores **0**, so this is
   a bounded, fixable class. The D2 work here also derisks carry-forward #4 below — same defect,
   bigger blast radius.

   **This does not re-open Sprint 1's green unit.** The instrument never scanned these files, so its
   zero was true about a smaller layer than it read as. State it that way in the closeout and the
   176→0 trajectory stays honest.
3. **Extraction-era standards-tree cleanup — RESOLVED 2026-08-15: PUNCH-LISTED IN FULL.** Stephen's
   call — the goal is releasing repaired documentation, and this effort serves none of it. Moved to
   `engineering/document-production/PUNCH-LIST.md` (*Extraction-era standards-tree cleanup*), where
   the inventory was also corrected: it is **six** files, not four (`style-guide-extraction-tasks.md`,
   `documentation-generation-planning.md` and `instruction-documentation-template.md` have **zero**
   referrers), and archiving them changes nothing measured while the glob covers descriptors only.

   **One carve-out is still open and is NOT hygiene:** `desilva-style-guide.md` is not an orphan —
   it is a **stale 207-line fork of the live 282-line guide** in `manuals/p2-pasm-desilva-style/`,
   which a **released** manual's descriptor and Sprint-1 voice-guide both depend on. Live pointers
   are relative and resolve correctly; the exposure is a filename lookup finding the stale copy. This
   project has been bitten by superseded DeSilva copies before. Cost to close: one `git mv`. Awaiting
   Stephen's call on whether it rides with the punch list or is pulled forward.
4. **299 files repo-wide still carry `pnut_ts`/`pnut_term_ts`** (opus-masters, CHANGELOGs, READMEs,
   workflow docs) — out of Sprint 1's charter by design. The D4/D6 classes almost certainly extend
   into manual text the same way D2 does.
5. **DeSilva master line 167** — study §0e flags it as a live R1 finding in released text.
6. **Overlay rules recommended for central promotion — RESOLVED 2026-08-15: recommendation only,
   and out of Sprint 2's path.** Not a sprint deliverable and not gating anything. Three candidates,
   all verified central-absent during the v5→v8 overlay reconcile:
   (a) *an instrument's first run is a planning input, not just a gate* (`plan-to-tasks` overlay);
   (b) *scope boundaries come from the artifact, never from prose* (`sprint-plan` overlay);
   (c) *the payoff sentence* (`document-finalize` overlay, promotion-pending since 2026-07-20).
   (a) and (b) are already stated generally and each carries a certified, measured origin; (c) is
   written in narrative-documentation vocabulary and needs generalizing before it could travel.
   **Promotion is Stephen's alone** — under every route (convergence, reconciliation contribution,
   owner judgment) an agent proposes and never self-authorizes, central is the maintenance agent's
   tree, and the install is fleet-wide distribution gated on Stephen every time. Nothing to do here
   but keep the candidates flagged.
