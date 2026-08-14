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

## Bench leg — COMPLETE 2026-08-14 (results, and what they change)

The sequencing note's batched bench session (§3, §7a re-proof, §7b, §7e) ran on 2026-08-14.
Full evidence: `campaigns/2026-08-manual-corrections/`, findings register F-253..F-266.

| plan item | finding | bench outcome |
|-----------|---------|---------------|
| §7a | F-259 | **REVISED — the guide is RIGHT.** TT=%01 drives (6,737 vs 1,408 off). The community report is not reproduced. The real defect is `+` composition of pin constants, which carries `%01+%01` into `%10`. Class sweep: 281 lines use `\|`, exactly 2 use `+`, both in the Streamer Guide (`:1238`, `:1306`), both currently computing correctly — a latent trap, not a live bug. Reproduced 3x. |
| §7b | F-260 | **RESOLVED — the mode WORKS.** On-target magnitude 1,059,000 vs 2,575 (2x detune), 286 (0.5x detune), 430 (null). **The missing protocol: the Goertzel accumulators are never zeroed** — a fresh cog inherits the previous cog's value and successive commands add, so read before, read after, take the difference. That is what Chip's shipped demo's `xcal`/`ycal` really does. Doc corrections still required: undeclared `dds_s`; `adc_pin<<17` valid only for multiples of 4; and the protocol itself. |
| §7b sibling | `:607` | **CONFIRMED — mode corruption, bench-proven.** Byte-count signature 1024 / 2048 / 4096 as `adc_pin` rises, because the shift carries into `D[19:16]`. Reproduced 4x. **Needs a confirming run** — see below. |
| §7e | F-263 | **CONFIRMED with cause.** No hub access inside either CORDIC loop; Chip's model vindicated. 7 consistent runs. P2AN002 and Assembly ch.5 both violate it. |
| §3 | F-256 | **ANSWERED — and the answer triggers this section's own error clause.** `_RET_ CALL` does **not** return to XBYTE; it behaves as a plain `CALL` and execution falls through into the following code. `pnut-ts` does emit the `_RET_` form, so this is silicon, not a compiler bug. **§4 therefore needs restructuring, not just a `set_nz` definition** — exactly the contingency Open Question 2 flagged. |

**New findings this leg, not previously in the plan:** F-264 (`wrpin.yaml`'s `tt_field` flattens
four context-dependent `%TT` meanings and tells readers to add `P_OE` to DAC outputs, which kills a
level-driven DAC), F-265 (**resolved** — Goertzel ADC pins are raw, no smart-pin mode, no DIR), and
F-266 (**the debug interrupt disrupts the streamer; `DEBUG_COGS` defaults to all eight cogs**, and
nothing warns a streamer author).

### Authoring source

The bench leg produced more than corrections: it produced **positive teaching material** about how
these features actually work, most of it absent from every doc we ship. That is written up for
authoring in
`campaigns/2026-08-manual-corrections/BENCH-FINDINGS-FOR-AUTHORING.md` — each test with its
question, rig, measured results and discovery path, and every outcome tagged **CORRECTION** (the
doc says something wrong), **TEACH** (the doc omits something the reader needs) or **TRAP**
(something that will bite a reader, found by being bitten).

The highest-value TEACH items, none of which are defects in the ordinary sense:

- **The Goertzel accumulators are never zeroed** — read before, read after, take the difference.
  Without this the mode looks completely dead while returning large, stable, plausible numbers.
- **Debugging streamer code with `-d` puts the P2's highest-priority interrupt inside your
  streaming cog** by default. One CON line fixes it; nothing warns anyone.
- **`%TT` is four different fields** depending on smart-pin and DAC_MODE state — and our own
  `wrpin.yaml` currently teaches only one of the four.
- **Pin-mode constants are bit fields**: combine with `|`, never `+`.
- **`##hubsymbol` inside a Spin2 object's DAT resolves against `$400`**, not the object's load
  address.

### Confirming runs required before §4 and the `:607` edit

F-266 was discovered *after* the F-256 and `:607` measurements were taken, and both were made with
the debug interrupt live inside the launched cog — the confound that produced 1,000,000–7,000,000 of
pure corruption in our Goertzel accumulators. XBYTE and the streamer are both hardware sequencers;
neither can be assumed immune. **§3's error clause already demands an independent confirmation of a
"the idiom is broken" result before restructuring a chapter, and this is that path.** Both probes now
carry `DEBUG_COGS = %0000_0001` and need one short bench session before their sections are written.

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

> **`DOC_AUDIT_COMMAND` is unset for this project — there is no doc-audit instrument yet.**
> This section is composed **by hand this once**, as the skill directs. `plan-to-tasks` should
> generate a task to build one. Unset means *owed*, not exempt.

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
| `.claude/skills/HEAD-DISPATCH-DRAFT.md` | References the slug; check whether as live or historical | 5 |

**Duplication watch.** The current-manual list appears in several process docs
(`TEMPLATE-CATALOG.md`, `PDF-PRODUCTION-ARCHITECTURE.md`, `manual-production-working-set.md`,
`document-pipeline-queue.md`). Per the skill's rule the fix is **one canonical copy plus links** —
`PUBLICATION-ROSTER.md` is already the declared source of truth, so these should reference it rather
than restate it. Editing four copies and hoping they stay aligned is exactly how this drifted.

---

## 7. Community bench review (refaQtor) — five defects in RELEASED manuals · **F-259…F-263**

**Source:** `p2-manuals-review-findings.md` (the posted zip), P2 Rev C @ 300 MHz, `pnut_ts` 1.55,
committed harness + logs, manuals as downloaded 2026-08-13. **All five verified against our own
sources.** Full detail in the corrections register.

> **Trust handling.** A third party's bench is a **high-quality lead**, not an accepted P2KB
> empirical finding. Fix the documentation defects the *source* proves; **replicate on our bench**
> anything we intend to cite as ground truth. His §5 "confirmations" are corroboration — they do
> **not** go into `P2-EMPIRICAL-FINDINGS.md` as our own tests.

**These outrank §1–§2 in severity: they are technically wrong content in shipped manuals.**

### 7a. Streamer Guide — cog-DAC examples output nothing (F-259) · RELEASED

`streamer-body.md:1306–1307` ships `wrpin ##P_DAC_124R_3V + P_CHANNEL, dac_pins` + `drvl`. Bench
proves output needs **all three** of `P_CHANNEL`, **`P_OE`**, and **DIR high** (no-OE → 1,228
counts = ground; +`P_OE` → 6,707 = full scale). Fix: `| P_OE` and `drvh`, and state which of OUT/OE
gates the drive.

**This is a recurrence of the F-245…F-247 `P_OE` class** — that sweep fixed the **YAML** and never
reached the **manuals**. So the deliverable is not one example: **sweep `P_OE` across every live
manual and app-note.** Treat the single fix as insufficient.

### 7b. Streamer §17.1 DDS/Goertzel — unbuildable as published (F-260) · RELEASED

Two confirmed doc defects: **`dds_s` is used at `:1324` and never declared** (one occurrence in the
whole guide — the example cannot assemble), and **`adc_pin<<17` at `:607`/`:990` collides with the
required `%111` in D[18:16]**. Fix both now.

Separately, the mode itself did not work on the reporter's bench (runs, no DAC output, no
accumulation) across a wide sweep. That needs **our** bench, and if it stays unresolved becomes a
**question for Chip**. Until settled, the guide must not present this mode as buildable.

### 7c. IOSP Guide — power groups of four, one month after we corrected it to eight (F-261) · RELEASED

`chapter-16-adc.md:263` and `:382` say *"isolated groups of four — pins 0–3, 4–7, …"*. **F-211**
settled this as **8 groups of 8** and shipped in **KB v1.15.0 on 2026-07-11**; our own **P2AN001
says eight**. The reporter caught us contradicting ourselves.

Three repairs, not one: the group size and boundary list; the **layout rule** built on it (with
wrong boundaries it misleads — it implies 3/4 straddle when 7/8 do); and `:382`'s **worked example
reasoning** (*"pins 40–47 — two full groups"* — that is **one** group; the conclusion survives, the
reasoning does not).

**Process deliverable:** F-211 swept YAML and missed manuals. Any correction landing in the KB must
carry a manual-side sweep, or this recurs.

### 7d. Debug Window Manual — FFT chapter has no channel defaults (F-262) · RELEASED

`ch07-scope.md:86` has an `If omitted` column; `ch09-fft.md` has none for `high`/`tall`. The manual
calls the arguments optional and never says what omitting them does. Reporter ties this to a real
**pnut-term-ts strict-parser divergence** he filed separately — the gap has already caused a tool
disagreement. Fix: add the column — **verify values against PNut**, do not assume FFT matches SCOPE.

### 7e. Assembly Manual — CORDIC fill-6-then-drain example is bench-disproven (F-263) · RELEASED

`chapter-05-hardware.md:~100–126` queues 6, runs steady state, drains 6. Bench: **two-in-flight
retrieval scrambled all outputs.** What makes it actionable: the same chapter's *other* CORDIC
statements matched his silicon exactly, so the chapter holds a correct rule and an example that
violates it. **Replicate on our bench first**, then either fix the example or state the conditions
under which deep pipelining is valid.

**Verification (all of 7a–7e).**
*Normal:* each corrected example compiles, and the ones with silicon claims run correctly on our
bench.
*Edge:* 7a's fix is applied **class-wide**, not just at `:1306`; 7c's three repairs all land, not
just the number.
*Error:* where our bench and the reporter's disagree, **confirm the measurement by an independent
path before acting** — do not rewrite a released manual on a single external log.

---

## 8. Release wave

§1, §2, §7a–7e touch **five released manuals** — deSilva, Streamer, IOSP, Debug Window, Assembly.
Per the wave rules: **stage shortest-first**, and any changed shared common-named file rides
**one** manual only. Each manual takes its own patch version and CHANGELOG entry (current-state
voice, never prior-wrong-state). `release-manual` owns the roster rows and the Platform Freshness
Ledger `PUBLISH` lines.

---

## Sequencing (revised — the bench findings reorder this)

1. **§7c** (IOSP 4→8) — highest severity: a released manual contradicting our own published KB and
   app note, on a fact we already settled. No new research needed; the answer is in F-211.
2. **§7a** (Streamer `P_OE`) + its **class-wide manual sweep** — bench-proven broken examples.
3. **§7b doc defects** (`dds_s`, field collision) — source-verified, fix now; the silicon question
   goes to the bench queue.
4. **§3** (our `_RET_ CALL` bench test) — batch with §7b's and §7e's bench work into **one bench
   session**, since all three need Stephen and the board.
5. **§7d** (FFT defaults) — needs a PNut check, otherwise small.
6. **§7e** (CORDIC) — after its bench replication.
7. **§4** (XBYTE §15.3) — after §3 returns.
8. **§1 + §2** (deSilva) — independent; land together in one v3.0.6 render.
9. **§5** (retired-doc cleanup) — independent; any time.
10. **§8** — the release wave, once the above land.

**Bench session batching:** §3, §7b, §7e (and any 7a re-proof) all want the board. Group them.
