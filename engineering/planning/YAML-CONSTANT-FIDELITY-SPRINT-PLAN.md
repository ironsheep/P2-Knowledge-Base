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
inference.** 51 findings, 155 flagged blocks and 50 undefined constants create a real pull
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

**Post-«#292» restatement — the fidelity figure above is the ENTRY measurement and stays
as the historical record; it is no longer the live one.** Closing §10a's heading-form
harvest gap did what fixing a detector is supposed to do: it made the truth side see
definitions it had been blind to, and the Tier-1 count went **42 → 50** (the one false
`[ORPHAN]` cleared, `[UNDEFINED]` 41 → 50). The nine additions were verified on three legs
before being accepted: each is a genuine Spin2 constant carried by the v55 symbol table, each
is **used** by the shipped KB, and none is **defined** by it. They were not created by the
fix; they were unmasked by it, which is precisely why §10a runs first. Tier 2 held at 23 and
the Tier-2 block is byte-identical. **§6's workload is therefore 50 constants, not 41** — §6
carries the roster and the source lines.

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

**Starting point.** **50** constants referenced across the shipped set and defined in none of
it (`P_ADC_1X` in 7 files; `P_ADC_GIO`, `P_ADC_VIO` in 7 each). Source tables exist at
`smart-pins-catalog/ingestionSources/basic-io/spin2-v51-extract.md:150-195` and
`sources/spin2-v51/spin2-builtin-symbols-tables.md`.

**This was 41 at entry and is 50 after «#292».** The nine the detector fix unmasked —
`P_STATE_TICKS`, `P_HIGH_TICKS`, `P_EVENTS_TICKS`, `P_PERIODS_TICKS`, `P_PERIODS_HIGHS`,
`P_COUNTER_TICKS`, `P_COUNTER_HIGHS`, `P_COUNTER_PERIODS`, `P_DAC_DITHER_RND` — are the
time/counter and DAC-dither families, and their definitions are in the v55 symbol table at
`sources/spin2-v55/spin2-v55-text.txt:1532` and `:1546-1553` (verified 2026-08-24). They are
in scope here on exactly the same terms as the original 41; do not treat the growth as a
regression or as licence to stop at 41. See §2's post-«#292» restatement.

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
`camelot lattice -p all -f csv -o <out.csv>` (ruled tables; `pdf2md` mangles them) from
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

All of them, not the seven this investigation raised. **26 predate it.** Findings whose token
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
population first, so there is nothing to tolerate. ~~Close the known heading-form harvest gap
in the fidelity tool (its one false ORPHAN).~~ **DONE in «#292»** — the heading-form gap is
closed and the false `[ORPHAN]` is gone.

~~**One harvest gap remains OPEN and «#305» must dispose of it before arming.**~~
**CLOSED in «#305», 2026-08-25.** The truth side globbed `*.md` only and required the
constant in **column 1** of a line beginning with `|`; the current-edition Spin2 v55 symbol
table satisfies neither (a `.txt`, tab-indented, `%value` in column 1 and the name in column
2), so the instrument audited the KB against the **superseded** v51 edition and could not
say so. Closed by reading `.txt` as well and parsing pipe rows **by cell**, with **edition
precedence** so a later edition of the same source family supersedes an earlier one.
`TRUTH_ROOTS` was **not** widened.

Measured, not estimated:

| | Stated at planning | Measured 2026-08-25 |
|---|---|---|
| v55 `P_` constants | 100 | **116** over 114 rows (two rows carry a name *and* a brevity alias) — F-339 |
| constants v55 **adds** | "added or re-described" | **0** — every one was already on the truth side |
| constants v55 **re-describes** | — | **20**; 19 visibly, plus `P_OR_AB` invisibly (`strip_desc` truncates "Select A \| B, B" identically in both editions — self-cancelling, not a defect) |
| truth-side merge | 120 | **120**, unchanged |
| Tier 1 / Tier 2 | 0 / 0 | **0 / 0**, unchanged — the KB side was already on the v55 wording |

**And the gap woke a latent one (F-341).** Six of our own derived analysis documents sit at
the top level of `ingestion/sources/`. They contributed 0 truth entries under the old row
shape; under the repaired one, `p2-complete-signal-flow-matrix.md:100` — a *signal-flow*
table whose last cell happens to be a constant name — defined `P_PWM_SAWTOOTH` as **"P38"**.
Closed structurally rather than by a list of six names: **an ingested source is a directory**,
so a loose file at the root of a truth root is not one. Two guards, both with controls: the
depth rule, and a name cell bounded to the first two columns (a constant in the last column
is a *use*, not a definition).

**Verification.** *Normal:* both exit 0 in the release path. *Edge:* each tool's
`--negative-control` runs **inside** the release path — `validate-dod-release.py` proves the
instrument still discriminates before it trusts the instrument's pass, because a check that
cannot fail has not been verified, it has been run. *Error:* a tool that errors (exit 2)
fails the release; "nothing audited" is never a pass.

**Armed, 2026-08-25.** Both instruments run as blocking checks in
`engineering/tools/validate-dod-release.py` (`validate_constant_fidelity`,
`validate_claim_sourcing`, each running its negative control first) and are listed in
`release-yamls` at Step 1 and in the Step 5.5 pre-flight certification gate. No baseline, no
tolerance, no ratchet.

**What arming cost on the content side, and why it was not a regression.** Recognising the
`documentation:` → `primary:` citation spelling (F-335a) moved **20 blocks across 7 board
files** out of the advisory lane and into blocking Tier 1 — blocks that had been exempt from
the gate for a reason nobody chose. They were drained source-first, the same way «#307»
drained the Goertzel board: 17 gained a per-block `source:` naming the #64006 / #64009 /
#64007 guide with a line range, and three unsourced inferences were removed outright
(`~4 mA, ~2.0 V LED drop` and a `~20 ms` debounce interval on the Control board, whose guide
states **470 Ω and nothing else**; the `current_per_led_ma` / `total_current_ma` pair from
the same inference). Nothing supported by a source was deleted.

## 11. Give the KB a release-notes home

**Why.** `deliverables/ai/` has no CHANGELOG, and the `build-wrapup` overlay records the YAML
head's version and release-notes homes as `TBD`. This sprint deletes blocks, adds 50
definitions and corrects 23 sites — reaching every `p2kb-mcp` consumer with **nothing saying
what changed**. A sprint that materially rewrites the deliverable is the one that must fix it.

**Governing guide:** `central:changelog-voicing` §1–§4 plus the retained class profile.
Resolve the `TBD` in `engineering/operations/process/HEAD-DISPATCH-DRAFT.md` in the same pass.

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
| `guides/spin2-getting-started.yaml:33,500` · `guides/pasm2-getting-started.yaml:33,631` | **cite `concepts/basic-io.yaml` as "REQUIRED before any I/O work"** — they route every new agent into the file carrying the broken examples. Found by producer/consumer inventory; absent from the first draft's file table. |
| `deliverables/ai/P2/README.md` · `deliverables/ai/README.md` | describe the set to consumers |
| KB release notes | does not exist — §11 creates it |
| `engineering/ingestion/README.md` (p2-datasheet row, scheduled-work table) | §8 moves coverage |
| `datasheet-audit-report.md` · `identified-broken-tables.md` · the source extraction-audit | §8 changes what they report |
| `P2KB-YAML-AUTHORING-GUIDE.md` | any rule this sprint revises |
| `skill-conventions.md` `CONFORMANCE_GUIDES` (agent-side) | the gate row names the instruments |
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

**Three more things the green does not certify, added when the gates were armed («#305»):**

1. **The sourcing gate checks that a citation is PRESENT, never that it is RIGHT.** Nothing
   reads the cited document. A block citing the wrong page passes.
2. **Tier 2 is advisory and its population is not zero** — 49 blocks in wholly-uncited files
   at arming. The release is green with those outstanding, by design.
3. **`validate-crossref-keys.py` walks TOP-LEVEL fields only (F-340).** Measured 2026-08-25:
   3161 reference sites read, **688 nested sites not read** — 82% coverage. The invisible
   share is where F-338's two fabricated constant names hid. The validator now **counts and
   prints** what it cannot see, and its banner reads *"ALL TOP-LEVEL CROSS-REFERENCES
   RESOLVE"* rather than the former *"ALL CROSS-REFERENCES VALIDATED SUCCESSFULLY"*.
   **"3161 refs, 0 unresolved" must never be reported as "cross-references are clean."**
   The traversal repair remains owed under F-340; measured cost of landing it today is **54
   nested references that do not resolve**, which is content triage, not instrument work.

---

## Section ↔ task cross-reference

Generated by `plan-to-tasks` 2026-08-24. Sprint tag `yaml-fidelity`. `seq` is the only
ordering signal; `todo_next` walks it. Total estimate **48h 45m** across 17 tasks.

_Revised twice the same day, both on Stephen's reading of the task set: ordering changes 4-6
below. «#308» was raised as a proposal and **approved 2026-08-24**._

| Plan § | Deliverable | Task | seq | est |
|---|---|---|---|---|
| §10a | Close the fidelity tool's heading-form harvest gap | «#292» | 1 | 45m |
| §9 / F-250 | **Re-ingest `p2-eval-board`, forced OCR** | «#306» | 2 | 2h 30m |
| §8 / new | **Ingest `p2-hardware-manual` from the staged DOCX** — approved 2026-08-24 | «#308» | 3 | 5h |
| §8 (1/2) | **Complete the `p2-datasheet` ingestion** — all ten broken tables | «#297» | 4 | 5h |
| §4 (1/2) | Remove ALL uncited blocks — `architecture` · `language` · `guides` · `application-notes` (65) | «#293» | 5 | 4h |
| §4 (2/2) | Remove ALL uncited blocks — `hardware/` (48) | «#294» | 6 | 3h |
| §6 | Define the 50 constants; one definition home **(two-phase)** | «#295» | 7 | 3h |
| §5 | Correct the drive-strength mislabel class by deletion + repoint | «#296» | 8 | 2h 30m |
| §7 | Promotion filter — survivors **and** every repopulation candidate | «#298» | 9 | 3h |
| §8 (2/2) | **Repopulate** `architecture` · `language` · `guides` · `application-notes` | «#299» | 10 | 3h |
| §8 (2/2) | **Repopulate** `hardware/` | «#307» | 11 | 3h |
| §9 (1/3) | Drain the KB/ingestion pre-existing findings; verify F-218 first | «#300» | 12 | 2h 30m |
| §9 (2/3) | Drain the manual/app-note-prose pre-existing findings | «#301» | 13 | 5h |
| §11 | Give the KB a release-notes home; resolve both routing `TBD`s | «#303» | 14 | 1h |
| Blast radius | The mandatory documentation task | «#304» | 15 | 1h 30m |
| §10b | Arm both gates — blocking, no baseline | «#305» | 16 | 1h |
| §9 (3/3) | Render-gated findings + the all-51 status reconciliation | «#302» | 17 | 3h |

### Ordering changes the rework pass made to the plan's section order

Three, each with its reason. The plan's section numbering is argument order, not
execution order.

1. **§10 split, and its detector half moved to first.** `audit-constant-fidelity.py`
   carries one known false `[ORPHAN]`, and that false positive sits inside the Tier-1
   count §6 has to drive to zero. A detector is fixed before anything trusts its zero.
   **Vindicated on execution («#292», 2026-08-24):** the fix cleared the false `[ORPHAN]`
   *and* unmasked nine genuine `[UNDEFINED]` constants the incomplete harvest had been
   hiding, taking Tier 1 from 42 to 50. Had §6 run first it would have driven a count that
   was wrong in both directions to a zero that meant nothing.
2. **§6 moved before §5.** §5's target is *"the files point at the single definition
   home (§6)"*. Run in section order, §5 would repoint at a file that does not exist
   yet, fail `validate-crossref-keys.py`, and could not end at a protection point.
3. **§8's extraction moved before §7.** §7's error check requires that a block ruled
   not-actionable *already exist in the ingestion tree before it leaves the KB*.
   Extracting first is what makes that check satisfiable; §8's restore half stays after
   §7, which resolves the circular reference between the two sections.
4. **F-250's re-ingestion pulled out of §9 and moved ahead of the §4 purge** (Stephen,
   2026-08-24, on reading the first task set). F-250's own filed disposition is an ordering
   instruction — *"re-ingest this source with forced OCR, re-verify every numeric claim
   already derived from it"* — and the first tasking inverted it, scheduling the re-ingest
   after the `hardware/` purge that consumes those facts. It matters more here than in the
   datasheet case because **§8b restores datasheet blocks only**: a board fact deleted for
   want of an authority that arrives one task later has no route back. Scope is one
   document, established by running the spot-check F-250 asks for: `p2-eval-board` carries a
   digit on 13% of its extracted lines against a peer band of 29–58% across eleven other
   board/hardware sources, and its narrative still measures 91/1315 exactly as filed. That
   sweep is recorded in «#306» so it is not re-run.

5. **Both re-ingestions moved ahead of the §4 purge, and §4 hardened to remove-all**
   (Stephen, 2026-08-24). This supersedes the "datasheet class is deliberately not reordered"
   position that ordering change 4 recorded — that position lasted about an hour, and this is
   the amendment.

   **What he decided:** option 2 (extraction first) *with a guard* — *"decide remove all then
   repopulate after the reingestions complete."* So §4 becomes literal: every uncited block is
   removed, with **no cite-in-place disposition**, and content returns only through a
   repopulation step («#299», «#307») that reads the **source** first rather than the removed
   block.

   **Why the guard is stronger than what was tasked.** Cite-in-place is *claim-first*: it opens
   a block, then goes looking for an authority that supports it — which is how a loosely-related
   citation gets stapled onto a wrong claim, and every defect in this sprint's origin story
   could have produced a citation. Repopulation is *source-first*: the block returns only if the
   repaired source states it, in the source's wording. That is §1a rule 3 with an enforcement
   mechanism instead of an instruction.

   **What it costs, stated plainly:** removal of the known fabrications now happens at seq 5
   rather than seq 2 — roughly twelve hours of work later — and §4's *"the damaged set is being
   served while we fix it"* argument pays that. The trade was put to Stephen with that cost
   named, and he took it.

6. **An ingestion that hits trouble now GATES the sprint** (Stephen, 2026-08-24):
   *"stop if we have ingestion problems, see if we can complete ingestions before continuing."*
   This closes the hole that remove-all opens — under cite-in-place a weak ingestion meant a
   weak citation, but under remove-all it means the content is **permanently absent**. So
   ingestion completeness is now a precondition of the purge, not a best effort.

   Written into «#306», «#308» and «#297» in the roster's vocabulary, not as a new stop:
   exhausting the extraction paths is a **step halt** (diagnose and re-route, never an
   interruption); only genuinely unrecoverable content reaches Stephen, as **sprint stop 1 — a
   decision he owns**. A *capability limit* stays a named non-stop. The roster's tie-breaker is
   met: continuing would lose quality that stopping buys.

### What that instruction surfaced — two sources, both incompletely ingested

Both of §8's named sources turned out to be weaker than the plan assumed, and remove-all is
what makes it matter:

- **`p2-datasheet`** — the plan said "94% with a known broken-tables problem." The file it cites,
  `sources/p2-datasheet/identified-broken-tables.md`, lists **ten** structurally-lost tables, of
  which the electrical ones are two. It also ends with an unanswered question to a human, which
  is why it stalled. «#297» is rescoped from a surgical grab to completing the source, 3h → 5h.
  It also records a page discrepancy to settle: `io_pin_timing.yaml`'s header claims pages
  42-45 / 76-78 while that file puts DC at p34 and AC at p35.
- **`p2-hardware-manual`** — §8's cross-check partner, and itself at **~65%** with no image
  catalog. `Propeller 2 Hardware Manual - 20221101.docx` (6.7 MB) has been **staged since
  2026-06-22 and never ingested**, with the dashboard already carrying the queued work item.
  A DOCX carries real table structure, so ingesting it should give clean tables by construction
  rather than by fighting `camelot` — it converts «#297» from an extraction fight into a
  corroboration. Raised as «#308» because it widens scope (stop 1, his call), and **approved
  2026-08-24**. Two copies of that DOCX exist with **different byte counts** — 6,751,607 in
  `sources/p2-hardware-manual/` and ~~6,993,299~~ **6,697,923** in `external-inputs/p2/` — so
  which is canonical is determined at ingestion, on evidence, not assumed from the dashboard's
  note.

  **SETTLED 2026-08-24 at «#308», and this paragraph was itself wrong twice over.** (1) The
  6,993,299 figure was a **misattribution**: it is the size of `Parallax Spin2 Documentation
  v51.docx`, a different document sitting in the same `external-inputs/p2/` folder. The real
  second copy is 6,697,923 bytes. The wrong number was written here at planning time and then
  carried verbatim into the «#308» dispatch — a fabricated-by-misattribution quantity in the
  sprint's own plan, which is precisely the defect class the sprint exists to remove. (2) The
  dashboard's "older export" note was **also** wrong: the two copies are the **same edition
  exported twice**. Verified independently by the arbiter — extracted text byte-identical
  (md5 match, 144,300 chars by `w:t` concatenation, 5,209 digits), identical structure
  (3,198 paragraphs · 53 tables · 280 rows), identical tracked changes (10 `w:ins`, 3 `w:del`),
  identical media md5 *set* across 39 files. Only the container differs: fonts re-embedded,
  media renumbered, `styles.xml`/`settings.xml` re-serialized. **Canonical = the `sources/`
  copy.** *Lesson: a byte count is a measurement of a path, and a path is easy to mis-copy —
  neither number here had been read off disk since it was written down.*

**And there is no DOCX edition of the datasheet.** Every `.docx` in the ingestion tree was
enumerated at tasking; the datasheet is not among them. So «#297» has no structured-source
escape hatch and PDF extraction is its only path — which is what makes the stop-1 gate its real
backstop rather than a formality, and what makes «#308»'s corroboration worth the 5h.

### Green-ordering — what a non-zero instrument means during this sprint

No atomic green-unit was needed. The **four entry gates**
(`verify-yaml-format.py` · `validate-crossref-keys.py` · `audit-register-hygiene.py` ·
`audit-guide-conformance.py --inventory`) exit 0 at entry and must exit 0 at the end of
**every** task — that is the protection point each one ends at.

The **two new instruments exit 1 at entry by design** (42 / 23 and 113 / 91; the fidelity
figure is **50 / 23** from «#292» onward — see §2). A task that leaves them non-zero has not
broken anything: it is counting down against a recorded baseline, and the gates are not armed
until «#305». Every task states this so an executor does not read progress as regression, or
"fix" it by weakening the change just made.

**A count that goes UP is not automatically a regression either.** «#292» raised Tier 1 from
42 to 50 by repairing the harvest behind it, and that was the intended effect of running the
detector fix first. The test is not the direction the number moved — it is whether the move
is explained and the explanation is verified against the source.

### Dispatch shape

`DISPATCH_MODEL` for this head is **`arbiter-serial`**, and this sprint does not differ
from it. The reason is on the `EXCLUSIVE_RESOURCES` roster, not a preference:
`P2KB-CORRECTION-FINDINGS.md` is a single-file artifact that **every** task in this set
writes into, and `F-NNN` is a monotonic allocator sitting at F-327 with F-328 next. One
writer at a time. `conductor-parallel` belongs to the ingestion head, which built the
allocate-before-fan-out and single-writer-reduce machinery that makes it safe; this head
has not.

🔴 **`arbiter-serial` means ONE AGENT AT A TIME — not that the arbiter does the work.**
That misreading is `inline`, and `inline` is the verdict only when no Agent tool exists
(`task-execution` contract §6). **Every one of the 17 tasks is dispatched to a fresh
agent**, one after another. The task body IS the dispatch prompt — that is what §2's
standalone requirement was buying all along. What the arbiter keeps is fixed by contract
§2 and is not negotiable under time pressure: todo-mcp protocol and the resume key, the
plan and dispatch order, **verification**, the boundary commit, and any decision that is
Stephen's.

**Verification is the carve-out, and it is unusually cheap here.** `baseline-health` §2c
splits re-verification by cost because a clean build plus full suite after every task is
unaffordable in most projects. **This project is the exception**: the four entry gates are
Python validators over a YAML tree — seconds, no build, no test fleet — and so are the two
new instruments. So the arbiter re-runs *all six* after every task rather than batching
them into block audits. `relay nothing, re-run it` (§1b) costs us almost nothing, and the
§2c trade-off of bisecting two-to-four commits after a red block audit does not need to be
taken.

The §2c free-list rule still bites, though: the list of per-task greps is **overlay
material**, and this project has **no `task-execution` project-overlay**. Its anchor case
is already documented — `BUILD_COMMAND` was `validate-yaml-syntax.py` until 2026-08-15 and
reported *"0 files checked / ALL VALID"* over the content tree, a textbook green-because-it-
never-ran. Standing that overlay up is separable from this sprint and is named here rather
than folded in.

🔴 **DISPATCH DOES NOT TRANSFER A STOP.** Three tasks — «#306», «#308», «#297» — carry the
D8 ingestion gate, whose escalation is **sprint stop 1, a decision Stephen owns**. A
dispatched agent that exhausts its extraction paths escalates to the **arbiter**, not to
Stephen; the arbiter judges whether the paths are genuinely exhausted and only then raises
it. Contract §2: dispatch does not transfer authority it never had.

**Two-phase:** «#295» only. Its shape — where a definition lives, what a definition record
looks like, what the idiom pages contain — is what «#296», «#298» and «#299» build on.
Design first, review, then implement.

**Environment split.** `EXEC_ENV_LIMITED` (this container) does all 14 tasks' authoring.
`EXEC_ENV_CANONICAL` (Stephen's host) owns two verdicts this sprint needs and cannot
produce itself: **rendered PDFs** (PDF Forge) for «#302»'s render-gated findings, and
**real P2 silicon** for F-202's campaign. Both are scheduled last, so the container-side
work runs during those waits rather than queuing behind them. Stopping at a corrected
master or a prepared outbound bundle is a complete outcome, not a shortfall.
