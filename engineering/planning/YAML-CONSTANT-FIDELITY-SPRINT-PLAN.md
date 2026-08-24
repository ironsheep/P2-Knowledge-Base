# P2KB Correctness Sprint — plan

**Head/element:** `yaml:p2kb`
**Authored:** 2026-08-24 (rewritten from the 2026-08-24 first draft; scope restored, ordering inverted)
**Register:** `engineering/operations/P2KB-CORRECTION-FINDINGS.md`. This plan **names**
findings and their status; it never restates their verdicts or evidence.

## § Open Questions

**None.** Every question raised in planning reached resolution:

| # | Question | Resolution |
|---|---|---|
| D1 | Where do the missing constant definitions live? | Extend `spin2-builtin-symbols-complete.yaml` (already worded from source) + one concept page. Duplicates are removed, not corrected. |
| D2 | Gate threshold — block now, or tolerate existing debt? | **Block, no baseline, no grandfathering.** A ratchet was proposed and rejected: this content is served live to agents, so the debt is not inert. Removal moves first, which leaves nothing to grandfather. |
| D3 | `P_HIGH_1MA` — match source, or add clarification? | Match the source. R9, no inference. |
| D4 | Document unstated idioms (open-drain, keeper)? | No. Ship only what the source states; file a gap for a hardware-verified idiom set. |
| D5 | Add a `CONFORMANCE_GUIDES` row for the KB? | Done during planning — `strength: gate`, guide authored. |
| D6 | Promotion filter — one file, or whole KB? | **Whole KB.** |

---

## 1. Why this sprint exists

**An agent failed at a basic task against the shipped KB, and reported contradictions.**
That is not a hypothesis about quality; it is an observed failure of the deliverable's
stated purpose. `deliverables/ai/P2/README.md` says the set is *"optimized for AI code
generation."* An agent could not determine how to configure a pull-up from it.

Investigation found seven defects (F-321…F-327) that had passed every release, because
nothing in the release path asked whether the KB says **true** things — only whether it
parses and its keys resolve. Two instruments built during planning then found the class
is far larger than the reported symptom.

The sprint goal: **the shipped KB stops misleading the agents that consume it.**

## 1a. The binding constraint — breadth never buys itself with inference

**"Fix all we can" and "every fix grounded in truth" are not in tension; the second
bounds the first.** Where they appear to collide, grounding wins and the breadth is
recorded as a gap. A sprint that closes 51 findings by guessing at some of them has not
fixed 51 findings — it has replaced defects we could see with defects we cannot.

This is stated as its own rule because **volume is the specific pressure that produces
inference.** 51 findings, 155 flagged blocks and 41 undefined constants create a real pull
toward batch-fixing by pattern — and the pattern will be right most of the time, which is
what makes it dangerous. Every defect in this sprint's own origin story was written by
someone reasoning plausibly: `P_HIGH_15K` *behaves a bit like* a pull-up; a drive ladder
*ought to* have current steps; `M[6:0]` *looks like* the drive field. None of it was
malicious and all of it was confident.

**Three rules, and they are mechanical rather than attitudinal:**

1. **Every correction carries its source trace** — `file:line` of the authority — written
   into the register annotation in the same pass. A fix with no trace is not a fix; it is
   an edit. This is checkable after the fact, which is the point.
2. **When a fix cannot be grounded, the outcome is removal or a gap — never a plausible
   value.** "We could not verify it" and "it is wrong" are different findings and get
   different dispositions, but neither one produces invented content.
3. **A source's silence is not permission.** If no authority states it, we do not state it.
   Aligning an entry to an authority it contradicts is correct; supplying what the authority
   omits is not. (Guide R9; the register's standing no-inference rule.)

**The success measure is therefore not "51 closed."** It is: every finding either fixed
with a trace, removed with a reason, or recorded as a gap with what would settle it. A
smaller number of grounded fixes is a better sprint outcome than a larger number of
confident ones, and the closeout reports it that way.

## 2. Entry baseline — measured 2026-08-24

| Gate | Result |
|---|---|
| `verify-yaml-format.py` | exit 0 |
| `validate-crossref-keys.py` | exit 0 |
| `audit-register-hygiene.py` | exit 0 — clean, 51 live findings |
| `audit-guide-conformance.py` | PASS, 45 guide files |
| `audit-constant-fidelity.py` | **exit 1** — 42 Tier 1, 23 Tier 2 |
| `audit-yaml-claim-sourcing.py` | **exit 1** — 113 Tier 1, 91 Tier 2 |

The first four are green and must still be green at exit. The last two are new; driving
them to exit 0 with **no tolerance recorded** is the sprint.

## 3. Scope

**IN — everything we can fix.** All 51 open register findings, both instrument backlogs,
the whole-KB promotion filter, the datasheet extraction, both gates, and the release-notes
gap. The scope is set by the observed failure, not by convenience.

**OUT — named deliberately**
- Manual and app-note prose. **Class-wide sweep run 2026-08-24: clean.** No opus-master
  carries the mislabel, the fabricated ladder, or a pin slew-rate claim. Nothing to do,
  and that is a measured result rather than an assumption.
- Renaming or re-encoding constants. Every name is legal (2026-07-01 audit) and stays so.
- P1 content.

---

## 4. Purge the unsourced and fabricated content — FIRST, not last

**Why first.** The shipped set is served live by `p2kb-mcp`. Every day a fabricated claim
stays, some agent generates code against a mechanism the P2 does not have. **Absence is
strictly safer than error**: an agent that does not find a fact asks, omits, or falls back;
an agent that finds a wrong one emits broken code confidently and nothing signals it.

Doing this first also removes the need for any gate tolerance (§10) — there is nothing left
to grandfather.

**Starting point.** `audit-yaml-claim-sourcing.py` Tier 1 (113 blocks) and Tier 2 (91).
Worst single file `architecture/io_pin_timing.yaml` — nine uncited quantitative blocks,
including `timing_specifications:90` (45 quantities) and the two proven-fabricated blocks
`drive_strength_configurations:200` and `slew_rate_control:234` (F-327).

**Target.** Every unsourced quantitative block is **removed from the shipped tree**, not
rewritten and not marked provisional. Guide R3: an unsourced claim is deleted, because a
rewritten fabrication is still a fabrication. Nothing is destroyed — git holds every block,
and §8 restores what verification earns.

**Not in this section:** deciding whether a number is *true*. That is §8. This section acts
on *unsourced*, which is decidable today.

**Verification.**
- *Normal:* `audit-yaml-claim-sourcing.py` Tier 1 → 0.
- *Edge:* a block that is uncited but whose content is pure structure (no physical claim) is
  a tool false positive — **stop and confirm the measurement** against the block itself
  before deleting, and fix the detector rather than the file.
- *Error:* deleting a block must not orphan a cross-reference. `validate-crossref-keys.py`
  exits 0 after every removal batch.

## 5. Correct the drive-strength mislabel class

**Findings:** F-321, F-322, F-323, F-324.

**Starting point.** 23 sites across 6 files, located by `audit-constant-fidelity.py`:
`language/spin2/concepts/basic-io.yaml:204-230`, `language/pasm2/concepts/basic-io.yaml:272-291`,
`architecture/smart-pins/smart-pin-00000-normal-mode.yaml:53,84`,
`language/spin2/conventions/johnny-mac-documentation-style.yaml:303`,
`language/spin2/conventions/spin2-docs-jonnymac.yaml:196`, plus `pinfloat.yaml`'s
external-resistors-only framing.

**Target.** The P2 has no pull-up or pull-down resistors. `P_HIGH_*`/`P_LOW_*` are
drive-strength selectors. **Correction is by deletion** — the `pull_up_modes:`/
`pull_down_modes:` blocks are removed and the files point at the single definition home
(§6), because F-321 and F-323 both exist from one fact being written twice. Also fix
`bits_M_6_0` → drive-high `M[5:3]`, drive-low `M[2:0]`, polarity `M[6]`.

**Governing guide:** `P2KB-YAML-AUTHORING-GUIDE.md` R1, R4, R7 — `strength: gate`.

**Verification.**
- *Normal:* `audit-constant-fidelity.py` Tier 2 → 0 for this family.
- *Edge:* the two `conventions/*.yaml` files are style documents quoting real code — confirm
  the fix belongs in the quoted example, not the surrounding prose.
- *Error:* every rewritten example compiles under `pnut-ts` (`-d` where it carries `debug()`),
  **and** is read for semantics: a clean compile proves legality, never that the code does
  what its comment claims. F-322 is exactly that failure — eight examples compiled fine and
  every one shipped a dead pull-up.

## 6. Define the constants the KB uses

**Findings:** F-325, F-326.

**Starting point.** 41 constants referenced across the shipped set and defined in none of it
(`P_ADC_1X` in 7 files; `P_ADC_GIO`, `P_ADC_VIO` in 7 each). Source tables exist at
`smart-pins-catalog/ingestionSources/basic-io/spin2-v51-extract.md:150-195` and
`sources/spin2-v51/spin2-builtin-symbols-tables.md`.

**Target (D1).** Extend `language/spin2/symbols/spin2-builtin-symbols-complete.yaml` from 68
records to cover all 122 referenced constants — it already words them from the source
(`description: "Drive high 100μA"`). Add `architecture/pin-drive-configuration.yaml` for the
13-bit field's real sub-fields and the **idioms** an agent searches for, each as a
composition of drive settings with DIR stated. Expand or repoint `wrpin.yaml`'s stubbed `M`
field (F-326) — a deferral in a source is a work item, not an answer.

**Verification.**
- *Normal:* `audit-constant-fidelity.py` UNDEFINED → 0.
- *Edge:* a constant the KB references that **no** source defines is not a definition gap —
  it is a possible fabricated name. Route to the register, do not invent a definition.
- *Error:* new `related:` entries use full paths, never bare names, and
  `validate-crossref-keys.py` exits 0.

## 7. Whole-KB promotion filter — does it change the emitted code?

**Why.** The KB's own README states its purpose: optimized for AI code generation. Nothing
enforces that. `io_pin_timing.yaml` demonstrates the failure — `instruction_to_pin_timing`
gives `clock_cycles: 3` and names the instructions it applies to (an agent acts on it),
while `timing_specifications` gives propagation delay `typ: "3.5 ns"` at 25 °C. **At 160 MHz
one clock is 6.25 ns; a 3.5 ns delay is below one clock.** No generated source can respond
to it.

**Target.** Every Tier 1 and Tier 2 block gets one of three dispositions: **actionable**
(keep, cite), **correct but not actionable** (belongs in ingestion, not the shipped set), or
**wrong/unsourced** (§4). The middle disposition is new and is the point of this section.

**This is a judgment call per block and no instrument can make it.** The test is stated so
it is applied consistently, not so it is automated.

**Verification.**
- *Normal:* every disposition recorded, with the one-line reason.
- *Edge:* board-level facts in `hardware/` (pin maps, what is wired where) **pass** — they
  change which pin numbers appear in code. Do not mistake "hardware fact" for "not
  actionable."
- *Error:* a block ruled not-actionable must exist in the ingestion tree before it leaves the
  KB, or the sprint destroys information. Confirm presence, then remove.

## 8. Extract the datasheet electrical tables — and restore what verifies

**Why.** `io_pin_timing.yaml`'s header claims `Datasheet Reference: pages 42-45, 76-78` and
`Layer 1: Direct extraction`. Those numbers are **not** in the ingested datasheet text —
zero hits for `2.5 ns`/`3.5 ns`/`5.0 ns`. The source is ingested at 94% with a known
broken-tables problem (`identified-broken-tables.md`), so the numbers are currently
**unverifiable, not disproven**.

**Target.** Extract the electrical-characteristics tables with
`camelot --pages all --format csv lattice` (ruled tables; `pdf2md` mangles them) from
`external-inputs/archive/Propeller2-P2X8C4M64P-Datasheet-20221101.pdf`. Cross-check against
the second candidate source, `sources/p2-hardware-manual/hardware-manual-2022-extraction.md`.
Then restore into the KB **only** blocks that both verify and pass §7 — each carrying its
citation.

**Ingestion completeness is its own goal here.** Everything extracted lands in the ingestion
tree whether or not it is promoted.

**Dashboards are deliverables, not follow-up** — an extraction that does not move them
leaves them lying about coverage: the `p2-datasheet` row in `engineering/ingestion/README.md`
(currently 94%), its scheduled-work table, `datasheet-audit-report.md`,
`identified-broken-tables.md`, and the source's extraction-audit.

**Verification.**
- *Normal:* the header's page claim is confirmed or refuted, and said out loud either way.
- *Edge:* a table that resists `camelot lattice` falls back to `pdf-layout`; if both fail,
  record the gap rather than transcribing by eye.
- *Error:* **stop and confirm the measurement** before concluding a number is fabricated —
  a table the extractor mangled looks exactly like a number that was never there. Two
  independent extraction paths, or it is recorded unverified and stays out.

## 9. Drain the 51 open register findings

All of them, not the six this investigation raised. **26 predate it.** Findings whose token
is `PENDING-VALIDATION` (4) close on a render or release, not a YAML edit; the one
`NEEDS-VERIFICATION` is verified before anything is done to it. Classify by **status token,
never headline prose** — a headline reading "source fixed" over a `CONFIRMED` token is open.

**Verification.** *Normal:* every finding annotated in the same pass as its fix.
*Edge:* a finding that turns out invalid becomes `RESOLVED-INVALID` with the reason, never a
silent deletion. *Error:* `audit-register-hygiene.py` exits 0.

## 10. Land the gates — blocking, no baseline

**Target.** `audit-constant-fidelity.py` and `audit-yaml-claim-sourcing.py` run in
`release-yamls` and `validate-dod-release.py`, **failing the release on any Tier 1
violation**. No grandfathered baseline and no tolerance value: §4 removes the existing
population first, so there is nothing to tolerate. Close the known heading-form harvest gap
in the fidelity tool (its one false ORPHAN).

**Verification.** *Normal:* both exit 0 in the release path. *Edge:* each tool's
`--negative-control` passes in CI — a check that cannot fail has not been verified, it has
been run. *Error:* a tool that errors (exit 2) fails the release; "nothing audited" is never
a pass.

## 11. Give the KB a release-notes home

**Why.** `deliverables/ai/` has no CHANGELOG, and the `build-wrapup` overlay records the YAML
head's version and release-notes homes as `TBD`. This sprint deletes blocks, adds 41
definitions and corrects 23 sites — reaching every `p2kb-mcp` consumer with **nothing saying
what changed**. A sprint that materially rewrites the deliverable is the one that must fix it.

**Governing guide:** `central:changelog-voicing` §1–§4 plus the retained class profile.
Resolve the `TBD` in `.claude/skills/HEAD-DISPATCH-DRAFT.md` in the same pass.

**Verification.** *Normal:* a release note exists and carries the mandatory theme line.
*Edge:* the KB is always "latest" — no version citations inside the content itself.
*Error:* `audit-changelog` reads clean.

---

## Documentation Blast Radius

`{{DOC_AUDIT_COMMAND}}` run at plan time: **PASS, 45 guide files** — the prose-guide layer is
clean and is not disturbed by this sprint. It does not cover the standards tree (a known
open punch-list item), so the rest of this section is enumerated by hand and by instrument.

| Artifact | Why it is in the radius |
|---|---|
| `deliverables/ai/P2/**.yaml` | the deliverable itself |
| `guides/spin2-getting-started.yaml:33,500` · `guides/pasm2-getting-started.yaml:33,645` | **cite `concepts/basic-io.yaml` as "REQUIRED before any I/O work"** — they route every new agent into the file carrying the broken examples. Found by producer/consumer inventory; absent from the first draft's file table. |
| `deliverables/ai/P2/README.md` · `deliverables/ai/README.md` | describe the set to consumers |
| KB release notes | does not exist — §11 creates it |
| `engineering/ingestion/README.md` (p2-datasheet row, scheduled-work table) | §8 moves coverage |
| `datasheet-audit-report.md` · `identified-broken-tables.md` · the source extraction-audit | §8 changes what they report |
| `P2KB-YAML-AUTHORING-GUIDE.md` | any rule this sprint revises |
| `.claude/skill-conventions.md` `CONFORMANCE_GUIDES` | the gate row names the instruments |
| `P2KB-CORRECTION-FINDINGS.md` | 51 findings annotated |
| Manuals / app notes | **swept: clean.** Checked, not assumed. |

**Counts stated anywhere:** none found in the consumer-facing READMEs. The instrument
outputs are recomputed, never transcribed.

**Duplication:** the sprint's method is one canonical copy with pointers (§5, §6). No
deliverable here corrects the same fact in two files.

---

## Definition of done

1. **Every correction carries a source trace** (§1a) — `file:line` of the authority, in the
   register annotation. This is the first condition because it is the one volume erodes, and
   it is auditable after the fact: a spot-check of closed findings must find a trace on each.
2. **No finding closed by inference.** Anything ungroundable is removed with a reason or
   recorded as a gap naming what would settle it. Both are complete outcomes; a plausible
   value is not.
3. Both new instruments exit 0, **no tolerance recorded**.
4. The four entry gates still exit 0. A regression against entry baseline is a stop.
5. Every touched example compiles (`pnut-ts`, `-d` for `debug()`) **and** is read for semantics.
6. All 51 findings carry accurate status tokens, annotated in the same pass as the fix.
7. Ingestion dashboards moved to match what was actually extracted.
8. The KB has a release-notes home and this sprint's entry in it.

**Closeout reports grounded fixes, gaps, and removals as three separate numbers** — never one
"findings closed" total. A single number cannot distinguish the outcome we want from the one
§1a exists to prevent.

## What a green exit does not certify

These instruments check **named constants** and **quantitative claims**. Prose that describes
a behaviour without naming a constant or stating a number passes untouched — which is exactly
how F-327 sat in a released file until a human read it. Guide rules R6, R7 and R9 have no
instrument and are held by review.

**Name coverage is not semantic coverage, and neither is description coverage.** A clean run
means *not caught by these checks*, never *correct*. Say so at closeout, or the green will be
read as a guarantee nobody made.
