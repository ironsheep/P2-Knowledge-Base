# XBYTE Guide — Structural Restructure Sprint Plan

**Head:** manual production · **Element:** `p2-xbyte-programming-guide`
**Ships as:** **v1.1.0** — one public release, no intermediate releases
**Public baseline:** v1.0.1 (101pp, tag `p2-xbyte-programming-guide-v1.0.1`, 2026-08-08)
**Created:** 2026-08-18

**Why this sprint exists.** Community review of the first release showed experienced
readers failing to reach material the guide already contains: one could not locate
answers and fell back to a four-page primary source; another, highly expert in the
field, finished the book holding the opposite of its central thesis; a third read it
end to end and proposed that its subject order was wrong. None of this is a content
gap. It is a delivery failure with measurable structural causes, and the remedy is
structural.

**Source analysis.** The measurements and diagnosis behind this plan are held
privately outside the repository. This plan restates conclusions in its own words and
attributes none of them to individuals; that is deliberate and must be preserved in
any revision.

**Already landed (not in this sprint's scope, committed `e29d2218`):** the
§3.5/§18.7-versus-Chapter-16 contradiction repair, the complete community 6502 in
Appendix C, the §4.5 metadata-bits generalisation, the Appendix C scope note, and an
ASCII sweep of code blocks and the shipped example source.

---

## Open Questions

**None blocking.** The one scheduled decision, §11, was taken on 2026-08-18 and is now
build work rather than a question.

---

## Sprint start — build number, tree audit, entry checks

**Started:** 2026-08-18 · **Head/element:** manual · `p2-xbyte-programming-guide`

**Build number — agreed: v1.1.0** (Stephen, 2026-08-18). For a manual the version lives
in three places, all set at §8: the cover (`front-matter.md`), `request.json`, and the
CHANGELOG heading. The CHANGELOG already carries `## v1.1.0 (unreleased)`.

**Working-tree audit (sprint-start §2).** The sprint's blast radius —
`manuals/p2-xbyte-programming-guide/`, `workspace/p2-xbyte-programming-guide/`,
`engineering/planning/` — is **clean and committed**; no untracked source. One item
outside it needs a decision: `deliverables/documents/DOCs/P2-XBYTE-Programming-Guide.pdf`
is modified-uncommitted — a v1.0.2 render of a version that will now never ship.
*Needs Stephen's accept-or-fix: revert to HEAD so the public tree matches the published
v1.0.1, or keep.* Not discarded pending his call.

**Entry baseline (sprint-start §4, per the project overlay).** A manual sprint has **no
local build gate** — manuals render on PDF Forge under the handback model — so the entry
baseline is the **document's audit state**, not a compiler result. Measured 2026-08-18:

| Gate | Entry state |
|---|---|
| Published baseline | v1.0.1, 101pp, tag `p2-xbyte-programming-guide-v1.0.1` |
| Guide layer (`DOC_AUDIT_COMMAND`) | **PASS** across 45 files; all printed lines are annotated exceptions |
| Cross-references | **387 resolvable, 0 dangling** |
| Code-line column budget (K=76) | clean |
| Non-ASCII in code blocks | clean |
| Example byte-identity + compile | both examples identical to their blocks; both compile clean under `pnut-ts -d` |

The exit assertion at closeout compares against **this** table, not against a test count.

**Tracking readiness (sprint-start §3).** 28 completed tasks archived to
`tasks/archives/archive_20260818_042144.md`. No stranded `task_#N_*` context keys — the
per-action hygiene fired. Context 57 keys (under the 75 audit threshold); `MEMORY.md`
147 lines (under the 150 threshold). One superseded key pruned. Leftover board items and
one standing-constraint question are recorded below as needing Stephen's decision.

---

## 0. Execution order, and why it is not the section order

Sections below are deliverables; `plan-to-tasks` maps tasks to them. **They are not in
execution order**, and one ordering constraint is load-bearing:

**The governing documents are updated first.** `creation-guide.md` §2 is what an author
reads *before* writing into this manual, and it is **stale today** — it still describes
the v0.1.0 fourteen-chapter, four-Part shape. Executing the cut while the creation guide
describes a structure that has not existed since v0.1.0 means authoring against a
document that is wrong in a *new* way. So §7 splits, and its first half leads:

| Order | Work | Constraint |
|---|---|---|
| **1** | §7a — `PLANNING.md` records the target structure as a LOCKED decision; `creation-guide.md` §2 rewritten to it | governs authoring; must precede the cut |
| **2** | §1 — the chapter permutation and Part boundaries | — |
| **3** | §2 — Part intros, chapter openers, transitions | needs the new order to exist |
| **4** | §3 — cross-reference sweep, flipped-direction adjudication, Index rebuild | needs the cut complete |
| **5** | §11 — insert new Ch.15 "Growing the VM", renumber old 15–20 → 16–21, re-sweep | **decided 2026-08-18**; must precede §4/§5/§6/§7b, which encode chapter numbers |
| **6** | §4, §5, §6 — navigation layer, apparatus, diagrams | **structure-dependent**; built before the cut they would be built twice |
| **7** | §7b — `voice-guide.md` citations, `MANUAL-DESCRIPTOR.md` chapter pins | cite *content locations*, so they follow the cut |
| **8** | §8 — front matter, cover title, `request.json` | title wording fixed once structure is final |
| **9** | §10 — draft render → diagram review → audit → release render | — |

§11 was the scheduled decision; it was taken on 2026-08-18 and became build work that
runs at order 5 — see §11. §12 (hygiene) is order-independent.

---

## 1. The reorder — Part boundaries and the chapter permutation

**Why.** The book argues that most P2 emulator authors land on rung 2 (`EXECF`
dispatch with a hand-rolled fetch) and that the full engine serves a narrower case,
then organises itself as though the engine were the destination. The decision
framework that resolves this — today's Chapters 13 and 14 — begins on **p54 of 101**,
after 43 pages of engine reference a rung-2 reader will never use. A reader who wants
"should I use this?" must either read half the book or follow a forward pointer out of
Chapter 3.

**Current starting point.** `opus-master/xbyte-body.md` — 20 chapters in 6 Parts:

- Part I The Landscape — Ch.1–2 · Part II XBYTE Fundamentals — Ch.3–6
- Part III The XBYTE Engine — Ch.7–11 · Part IV Building — Ch.12–18
- Part V Reference — Ch.19–20 · Part VI Appendices A–D + Index

**Target.** The decision Part moves ahead of the engine Part. Chapter *count* is
unchanged; this is a permutation, not a rewrite.

| New | Title | From | Part |
|---|---|---|---|
| 1 | Why Emulate on the P2 | 1 | **I — The Landscape** |
| 2 | What This Kind of Emulation Asks of You | 2 | I |
| 3 | Understanding XBYTE | 3 | **II — Dispatch on the P2** |
| 4 | The Skip Family | 4 | II |
| 5 | The Bytecode Stream | 5 | II |
| 6 | LUT Dispatch | 6 | II |
| **7** | **The Three Decisions** | **13** | **III — Choosing Your Rung** |
| **8** | **What Will Hurt — A Guest-CPU Survey** | **14** | **III** |
| 9 | The Dispatch Cycle | 7 | **IV — The XBYTE Engine** |
| 10 | Arming XBYTE | 8 | IV |
| 11 | Table-Size & Compression Modes | 9 | IV |
| 12 | Bytecode Routines | 10 | IV |
| 13 | Debugging XBYTE | 11 | IV |
| 14 | A Minimal Custom VM | 12 | **V — Building Interpreters and Emulators** |
| 15 | A Tiny CPU Emulator (6502) | 15 | V |
| 16 | Servicing Guest Interrupts | 16 | V |
| 17 | Prefixes and Alternate Tables | 17 | V |
| 18 | XBYTE Beyond Interpreters | 18 | V |
| 19 | Instruction Reference | 19 | **VI — Reference** |
| 20 | Configuration Constants & Patterns | 20 | VI |

**Eight chapters renumber (7–14). Twelve keep their numbers (1–6, 15–20).**

**The appendices Part renumbers VI → VII.** The table above numbers only the
chapter-bearing Parts; the appendices keep their own numbered Part, as the shipped book
and the model manual (the Streamer guide's `Part V: Appendices`) both do, and inserting
Part III pushes it down one. So the finished book carries **seven** Part headings.
Appendix letters A–D and their `{#app-x}` anchors do not move.

**Design decision — the Bytecode Stream stays in Part II.** An earlier sketch moved
the FIFO chapter into the engine Part, on the reasoning that auto-fetch is rung-3
machinery. **Rejected:** §6.4's hand-written dispatch loop — the passage that teaches
rung 2 — issues `RFBYTE`, so LUT Dispatch cannot precede the stream chapter without
breaking a dependency. Part II therefore keeps its four chapters and is retitled
*Dispatch on the P2*, naming what it actually teaches: the machinery both rungs share.

**Design decision — who owns the dispatch ladder.** The three-rung ladder currently
lives at §13.2, which under the new order is §7.2 and still arrives after Part II has
taught the machinery. Chapter 3 **introduces** the ladder in one short passage so
Part II's reader knows what the machinery is for; Chapter 7 **decides** with it.
Chapter 3 does not restate the rung table — one canonical copy, in Chapter 7.

**Integration points.** Part opener prose (§2), every cross-reference (§3), the Index
(§3), front matter (§8), the guide layer (§7).

**Verification.**
- *Normal:* all 20 chapter headings present, in the target order, with the target
  numbers; seven Part headings in the target sequence (I–VI chapter-bearing, VII the
  appendices); anchors `{#ch-N}` / `{#sec-N-M}`
  consistent with their new numbers.
- *Edge:* Chapters 15–20 keep their numbers, so their anchors must **not** drift; a
  find-and-replace that renumbers them is a defect.
- *Error:* no chapter appears twice, none is lost, and the chapter count is exactly 20
  before and after. Compare a sorted heading inventory taken before and after the cut.

---

## 2. Chapter openers, Part intros, and transitions

**Why.** Openers and closers are written for the current sequence and name it
explicitly. Part IV's intro (`xbyte-body.md:954`) opens *"Parts II and III explained
the engine…"*; Chapter 13's opener says *"Everything so far has taught the engine"* —
false once it precedes the engine. Reordering without rewriting these produces a book
that contradicts its own table of contents.

**Current starting point.** Six Part intros (`xbyte-body.md:1, 105, 515, 954, 1913,
1988` at pre-reorder line numbers) and 20 chapter openers.

**Target.** Each Part intro states what its Part teaches and what the reader arrives
with, consistent with the new order. Chapter 7's opener changes from
"everything so far has taught the engine" to the honest new framing: the reader has
the machinery, has not yet met the engine, and is about to decide whether they need
it. Chapter 9's opener picks up from the decision rather than from Part II.

**Conformance.** Manual prose is governed by
`engineering/standards/documentation-standards/documentation-voices-catalog.md`
(house canon, rules R1–R4), then this manual's `voice-guide.md`. Read both before
authoring; re-read at finalize. Strength: reference.

**Verification.**
- *Normal:* every Part intro and chapter opener describes the sequence that now exists.
- *Edge:* the two-register voice is preserved — teaching register in openers, reference
  register in tables; a rewritten opener must not drift into reference voice.
- *Error:* grep for sequence claims (`Parts? [IVX]+`, `so far`, `earlier`, `the previous
  chapter`, `you have now`) and confirm each is true under the new order.

---

## 3. Cross-reference re-verification and the Index rebuild

**Why.** The body carries **387 resolvable cross-references** (`§N.M`, `Chapter N`,
`Ch. N`, `§C.N`), currently **0 dangling**. Renumbering eight chapters invalidates
every reference into them. Separately, the Index has two defects independent of the
reorder: its last eight entries are out of alphabetical order, and its
*"When to reach for XBYTE"* entry routes to §3.5/§3.7/§18.7 while omitting the two
chapters that actually answer the question.

**Current starting point.** `opus-master/xbyte-body.md` Index at `# Index {#index}`;
**58 entries**, section-pointers only.

**Target.** Zero dangling references after the cut. Index sorted, routed to the
decision chapters, and extended with reader vocabulary (hub · LUT · PSRAM · rung 2 ·
where to poll · complete emulators) alongside our own.

**Computed at plan time — the references that flip direction.** Some backward
references become forward ones and vice versa. A flipped reference **still resolves
perfectly**, so no link checker will report it; what changes is whether it promises the
reader something they have already read or something they have not. Direction is
`sign(target − container)`, computed before and after the permutation. **The complete
set is seven**, and each is adjudicated — accept as a forward pointer, or reword —
never silently repointed:

| Body line | Old | New | Was → becomes | Site |
|---|---|---|---|---|
| 857 | Ch.11→13 | Ch.13→7 | fwd → **back** | §11 opener, "there is no loop body" |
| 961 | Ch.—→13 | Ch.—→7 | fwd → **back** | **Part IV intro** — rewritten wholesale by §2 anyway |
| 961 | Ch.—→14 | Ch.—→8 | fwd → **back** | same passage |
| 1202 | Ch.13→11 | Ch.7→13 | back → **fwd** | §13.4, the debugging consequence |
| 1223 | Ch.13→12 | Ch.7→14 | back → **fwd** | §13.6, cites the minimal VM |
| 1260 | Ch.14→9 | Ch.8→11 | back → **fwd** | §14.2 CHIP-8 row cites compression |
| 1306 | Ch.14→9 | Ch.8→11 | back → **fwd** | §14.5 tip cites the F bit |

Three of the four back→fwd cases (1223, 1260, 1306) read acceptably as forward pointers
— they name where a thing will be explained. **1202 is the one to watch**: it currently
reads as a recap of debugging the reader has done, and after the move the reader has not
done it. That one is reworded, not accepted.

**The Index — measured.** 58 entries. **36 need repointing**; 22 are unaffected.
**Three are out of alphabetical order** (`Bit 1`, `6502 emulator`, `65816`), which is a
defect independent of the reorder and is fixed in the same pass.

**Verification.**
- *Normal:* the cross-reference checker reports 0 dangling, and the resolvable count is
  ≥ 387 (entries are added, none removed).
- *Edge:* Appendix references `§C.1`–`§C.9` are unaffected by chapter renumbering and
  must be spot-confirmed as unchanged rather than assumed.
- *Error:* **if the checker reports dangling references, stop and confirm the
  measurement before treating it as a finding** — re-run against a known-good commit
  first. The checker parses headings; a heading whose format the reorder altered can
  make correct references look broken.

---

## 4. The navigation layer

**Why.** The reader who could not find things needed navigation, not reordering. Three
pieces are missing and the material for all three already exists in the book.

**Current starting point.**
- §3.7 *"If you're building…"* (`xbyte-body.md:190`) is already an intent table, sitting
  inside a chapter as narrative rather than as navigation apparatus.
- Appendix A (`p91` of the released PDF) is close to the concise engine summary a reader
  wanting a short primary source would use — positioned at the back.
- `opus-master/front-matter.md` *"How to Use This Guide"* offers two prose on-ramps.

**Target.**
1. **Intent index** — §3.7's table promoted to a front-of-book or Appendix-A position in
   the form the I/O & Smart Pins Guide already ships
   (`manuals/p2-io-and-smart-pins-user-guide/opus-master/front-matter.md:147`):
   *I want to… → Chapter N → Specifically → Also consider.*
2. **A brief engine opener** — a short front-of-book summary (dispatch cycle, mode
   operand, arming, one complete tiny example), so the reader who wants the concise
   version gets it early instead of leaving. Derived from Appendix A and Chapter 9; the
   appendix stays where it is for lookup.
3. **Explicit reading paths** replacing the two prose on-ramps, in the three-path table
   form the I/O guide uses.

**Verification.**
- *Normal:* each reading path names chapters that exist at the numbers given, post-reorder.
- *Edge:* the intent index and §3.7 must not become two divergent copies — one is
  canonical and the other links to it. Decide which at authoring time and record it.
- *Error:* every chapter/section pointer in the new apparatus is included in §3's
  cross-reference sweep, not exempted from it.

---

## 5. Apparatus rebalance

**Why.** The book carries **45 `:::` boxes and 35 tables holding 27% of its prose**,
against **4 diagrams**. Load-bearing material sits in boxed asides that scanning readers
treat as optional — an in-place example was missed in review for exactly this reason,
four lines from the explanation it served. The two decision chapters carry **2,517 and
2,142 words with 8 and 0 lines of code** between them.

**Current starting point — measured at plan time.** 45 boxes: 15 `caution`, 16
`hardware`, 14 `tip`. **Six carry code.** **Fifteen run to 120 words or more** — essay
length, which is the population most likely to hold argument rather than aside, and the
population a scanning reader is most likely to skip:

| Chapter | Kind | Words | Opens with |
|---|---|---|---|
| 4 | caution | 183 | a skip pattern counts instructions, not source lines (`##` → two longs) |
| 4 | hardware | 220 | the spare bit in a table entry |
| 6 | hardware | 140 | the table is *this* cog's LUT — 256 is the ceiling |
| 6 | tip | 151 | "this loop is not a stepping stone" |
| 7 | caution | 177 | fencing an atomic sequence with `REP` |
| 8 | hardware | 144 | bit 1 selects the index form |
| 8 | caution | 175 | `SETQ2` does two entirely different jobs |
| 10 | hardware | 195 | recovering the stream from `PB` after a hub call |
| 10 | caution | 184 | reclaim the `$1FF` before re-arming |
| 11 | hardware | 120 | `CALL` depth suspends skipping |
| 11 | caution | 191 | the landing pad prevents a specific trap |
| 15 | hardware | 197 | do not fold the return into the call |
| 15 | tip | 150 | the addressing-mode matrix wants a second dispatch |
| 17 | hardware | 141 | what a modifier prefix costs under XBYTE |
| 18 | hardware | 128 | do not interpret at all — the JIT option |

**Highest-value relocations**, both already identified: Ch.4's `##`-counts-two-longs rule
(183w) and Ch.13's auto-fetch-welds-you-to-hub caution — the book's central architectural
claim, currently a 51-word boxed aside. Note the asymmetry that shows the problem: the
central claim gets 51 words in a box while the spare-bit trick gets 220.

**The test for each box**, applied per box rather than by size: does the surrounding text
still carry the fact if the box is skipped? If not, the fact moves into the text and the
box keeps only the aside.

**Target.** Load-bearing content moves into running text; boxes keep genuine asides. The
decision chapters gain code — §13.2's rung-1/rung-2 contrast is the model, because it
works precisely by showing two short fragments differing in one instruction.

**Conformance.** Any `.spin2` added or edited is governed by
`central:spin2-authoring-guide` at **gate** strength. `STYLE_GATE_COMMAND` is **unset —
the gate is owed, not waived**: `pnut-ts` proves legality only, never style and never
semantics. Every fragment added here is read against the guide by hand, and that is
recorded as done.

**Verification.**
- *Normal:* box count falls; no box contains a fact the surrounding text does not carry.
- *Edge:* code-line column budget **K=76** (the `{=latex}` passthrough is exempt) and
  plain-ASCII code, both already instrumented; new fragments pass both.
- *Error:* any fragment mirrored in `examples/*.spin2` stays byte-identical to its file,
  and both example programs still compile clean under `pnut-ts -d`.

---

## 6. Diagrams

**Why.** Four figures for a subject that is a pipeline, a bit-packed operand, a
three-rung decision and a two-kinds-of-prefix taxonomy is too few, and the reader who
reported failing to find things described his own method as building a structural map.

**Current starting point.** Four `\Diag*` macros — `\DiagXbyteLoop`, `\DiagLutEntry`,
`\DiagDispatchCycle`, `\DiagModeOperand`.

**Target.** Three new figures: the **dispatch ladder** (the book's central idea, today
only a table), the **three decisions** flow, and the **two kinds of prefix** taxonomy.

**Review model (Stephen's call).** Diagrams are reviewed **in the first draft PDF**, in
place at their real size and position — not as separate sketches. The sprint therefore
produces a draft render for review before the release render.

**Verification.**
- *Normal:* each figure appears in the rendered PDF and in the list of figures.
- *Edge:* figures render in place, not floated pages away from their referring text.
- *Error:* font glyph coverage clean; no figure is the sole carrier of a fact — each
  restates something the prose also states.

---

## 7. Guide layer and descriptor currency

**Why.** The guide layer describes the book's architecture, and one part of it is
**already stale before this sprint touches anything**: `creation-guide.md` §2 Document
Architecture still describes the v0.1.0 shape — 14 chapters in 4 Parts, with a "6809
SETQ2 Vignette" chapter — while the shipped book is 20 chapters in 6 Parts. Left alone,
an author reading it before writing is misdirected.

**This section splits, and the halves run at different times** (§0).

**§7a — leads the sprint. These govern authoring.**

| File | Refs | Work |
|---|---|---|
| `PLANNING.md` | 37 | standing design record with LOCKED/OPEN markers — **add** the target structure as a LOCKED decision; do not rewrite history |
| `creation-guide.md` | 19 | §2 architecture is **stale today** (describes the v0.1.0 14-chapter/4-Part shape); rewrite to the target structure |

**§7b — follows the cut. These cite content *locations*, so they cannot be written until
the content has moved.**

| File | Refs | Work |
|---|---|---|
| `voice-guide.md` | 11 | chapter citations in voice rules |
| `MANUAL-DESCRIPTOR.md` | 6 | `high_risk_tables` and `fragile_areas` pin chapter numbers; the Structure line states "20 chapters in 6 parts"; `last_published_tag` advances at release |

`PLANNING.md` already records the title/slug decision of record — *"Slug + PDF filename
stay `p2-xbyte-programming-guide` / `P2-XBYTE-Programming-Guide` (XBYTE = the durable
identifier)"* — which is consistent with this sprint's §8.

**Conformance.** The guide layer is itself a governed surface at **gate** strength:
`documentation-voices-catalog.md` R1–R4, instrument `DOC_AUDIT_COMMAND`, which must read
0 findings.

**Verification.**
- *Normal:* `DOC_AUDIT_COMMAND` passes; every chapter reference in the guide layer
  resolves to the chapter that now holds that content.
- *Edge:* `MANUAL-DESCRIPTOR.md`'s `last_published_tag` advances to the tag being created
  **as part of this release**, not afterwards — a stale descriptor after release is a
  known repeat failure across this fleet.
- *Error:* a guide-layer chapter reference that silently points at the right *number* but
  the wrong *content* passes any mechanical check; each is confirmed by reading the target.

---

## 8. Front matter, cover title, and the workspace request

**Why.** Front matter carries a Guide Organization panel that lists every Part and
chapter, plus the structure prose in "How to Use This Guide" — 12 structural references
that describe the old shape.

**Current starting point.** `opus-master/front-matter.md` — the `\begin{tcolorbox}`
Guide Organization panel and the "Structure:" list. `workspace/.../request.json:22-25`
carries title, subtitle, and `"version": "v1.0.2"`.

**Target.**
- Guide Organization panel and structure prose rewritten to the target six Parts.
- **Cover title revised** — wording fixed at this point, once the structure is final.
  Constraint: **"XBYTE" stays in the title or subtitle**, because it is the term readers
  search for. **The PDF filename `P2-XBYTE-Programming-Guide.pdf` and the slug
  `p2-xbyte-programming-guide` do not change** (Stephen's call, consistent with the
  standing `PLANNING.md` decision) — so no published link breaks and no deliverables,
  roster, or KB path moves.
- `request.json` title/subtitle updated to match the cover; version to `v1.1.0`.

**Verification.**
- *Normal:* the rendered cover, the `request.json` title, and the roster display name agree.
- *Edge:* three version locations agree — cover, `request.json`, and the CHANGELOG entry.
- *Error:* the published filename is byte-identical to the previous release's, confirmed
  against `deliverables/documents/DOCs/` before the release commit.

---

## 9. Documentation Blast Radius

`DOC_AUDIT_COMMAND` — `python3 engineering/tools/validation/audit-guide-conformance.py
--inventory` — run 2026-08-18 at plan time:

```
PASS  guide layer conformant across 45 file(s)
```

Every line it printed is an annotated exception (lineage references to the retired Smart
Pins Tutorial, the `pnut_ts` name quoted in order to forbid it, rules quoted as records of
their own correction). **No new guide-layer findings.** Note the instrument's scope: it
audits the *guide layer*, not manual bodies — the body's own gates are the code-line,
inline-ASCII, font-glyph, byte-identity and cross-reference checks named per section above.

Artifacts that describe behavior this sprint changes:

| Artifact | Why in radius |
|---|---|
| `opus-master/xbyte-body.md` | the reorder itself; Index; 387 cross-references |
| `opus-master/front-matter.md` | Guide Organization panel, structure prose, cover title, reading paths |
| `opus-master/CHANGELOG.md` | **always in scope**; v1.1.0 entry already open and accumulating |
| `creation-guide.md` | §2 architecture — stale today, plus 19 chapter references |
| `voice-guide.md` | 11 chapter references |
| `MANUAL-DESCRIPTOR.md` | structure line, `high_risk_tables`, `fragile_areas`, `last_published_tag` |
| `PLANNING.md` | 37 references; gains the structure decision as LOCKED |
| `examples/README.md` | 2 section references |
| `workspace/.../request.json` | title, subtitle, version |
| `PUBLICATION-ROSTER.md` | status row + a PUBLISH ledger line at release |
| `deliverables/documents/README.md` | the release index entry |

**Counts stated anywhere** — "20 chapters in 6 parts" in the descriptor and the roster —
are in radius and re-checked against the artifact, not from memory.

**Duplication watch.** §3.7's intent table and the new intent index are the one genuine
duplication risk this sprint creates; §4 requires one canonical copy with the other
linking to it.

---

## 10. Render, audit, and release

**Why.** A clean compile log has repeatedly failed to predict a correct page in this
fleet, and a 100%-success Forge report has been seen on a build that silently dropped
content.

**Target sequence.**
1. `document-finalize` — gather every finding to sign-off, resolve in a rework-safe
   order, render once.
2. **Draft render** for diagram review (§6) and page-level inspection.
3. `document-audit` at **release depth** — enforces the publish gate, the YAML-HEAD drain
   gate, and the changeset-integrity audit against the v1.0.1 baseline.
4. `audit-changelog` on the v1.1.0 entry.
5. `prepare-manual` → Stephen moves outbound to Forge → PDF.
6. **Read the rendered pages.** Page count, outline, the restructured Parts, the copyright
   page, the new figures.
7. `release-manual` — CHANGELOG promotion, deliverables release index, roster row and
   PUBLISH ledger line, descriptor `last_published_tag`.

**Verification.**
- *Normal:* outline shows six Parts and 20 chapters in the target order; both render gates
  (overfull worklist and PDF margin-overflow) run — **neither is a superset of the other**.
- *Edge:* the example ZIP is rebuilt only if example content changed, and the published
  ZIP is checked against the corpus by bytes.
- *Error:* **if a gate reports a defect, open the page and judge by measured overlap before
  acting** — magnitude has repeatedly failed to predict whether an overfull actually
  spills, in both directions.

---

## 11. DECIDED — the middle rung: a second worked build

**Decided 2026-08-18 (Stephen): take it, and shape it by the story, not by its cost.**
The scheduled decision resolves to *yes with a different shape than the suggestion*, for a
reason that only became visible after §1's cut put Part V in its final order.

### What the review actually found

Community review asked for "a small constructed bytecode machine" as an additional worked
build. Read literally that is **Chapter 14** — the four-bytecode stack machine
(`PUSHC`/`ADD`/`SUB`/`HALT`) is a constructed bytecode machine, it is complete, and it
compiles. A second one at the same size would be a duplicate, not an addition.

The real gap is a **step size**. Part V goes from the smallest thing that exercises the
engine once, straight to an illustrative slice of a 6502 that is deliberately *not* a whole
program. Between them sits everything the book recommends and never shows working:

| Technique | Where the book states it | Where a reader can watch it run |
|---|---|---|
| shared body + skip pattern across a family | §4.4, and §14.3 as a fragment | **nowhere** — Ch.14's program writes ADD and SUB out separately, on purpose |
| a guest branch as `RDFAST` to a new address | asserted in §15.1, leaned on by Ch.16 | only Ch.18's display list — a graphics stream, not an interpreter |
| a second operand width off the FIFO | Chapter 5 | Ch.14 uses one form |
| exit and re-arm between jobs | §12.4, §14.4 | described, never exercised end to end |

So the addition is not another minimal machine. It is **the same machine grown up** — the
rung between "smallest" and "real CPU."

### The chapter

**New Chapter 15: "Growing the VM"**, between Ch. 14 (which stays minimal — that is its
charter and its value to a reader who wants the floor) and the 6502.

It takes Chapter 14's stack machine and grows it to roughly a dozen bytecodes: variables
addressed by an operand rather than immediates only, a compare, a conditional branch, and an
ALU family folded onto one shared body with skip patterns. Complete, compiling, shipped as a
third `examples/` file byte-identical to its code block.

**Deliberately NOT in it:** prefix bytes (Chapter 18 after the renumber owns those; this
chapter forward-references once and builds nothing), and guest interrupts (Chapter 17). The
chapter earns its place by making a *table* work hard, not by collecting features.

### What it moves

Inserting at 15 renumbers six chapters — old 15–20 become 16–21 — and Part V's charter
paragraph, which today names "the two complete programs," now brackets the Part with three.
That paragraph gets rewritten: the charter was always about *faithfulness* (no complete
6502), never about size, and it should say so.

### Ordering — this runs BEFORE §4, §5, §6 and §7b

Load-bearing, and the reason the decision could not wait for the wrap after all: §4 (the
navigation layer), §5, §6 and §7b all encode **chapter numbers**. Built before this insert,
every one of them is built twice. The insert therefore takes the slot right after §3, and
inherits §1's atomic-green-unit shape — the renumber leaves the cross-reference checker red
by construction, and a re-sweep restores it.

---

## 12. Workspace hygiene

`workspace/p2-xbyte-programming-guide/` holds four hand-named `.backup` files of the
assembled render (`P2-XBYTE-Programming-Guide.md.backup.*`). These violate the backup
convention on two counts: backups are never hand-named, and **regenerable artifacts are
never backed up** — the workspace render is rebuilt from opus-master on every prepare.
Remove them.

**Verification.** The workspace assembles cleanly from opus-master afterwards, proving
nothing depended on them.

---

## Section ↔ task cross-reference

Generated by `plan-to-tasks`, 2026-08-18. Sprint tag: `xbyte-restructure`.
Execution order is `seq`, not section number — see §0 for why they differ.

| seq | Plan § | Deliverable | Task |
|-----|--------|-------------|------|
| 1 | §7a | Governing documents — PLANNING.md LOCKED entry + creation-guide §2 rewrite | «#251» |
| 2 | §12 | Workspace hygiene — remove four hand-named render backups | «#252» |
| 3 | §1 | **The cut** — chapter permutation and Part boundaries | «#253» |
| 4 | §2 | Part intros, chapter openers, transitions | «#254» |
| 5 | §3 | **Cross-reference sweep, flipped-direction adjudication, Index rebuild** | «#255» |
| 6 | §11 | **The middle rung** — new Ch.15 "Growing the VM" + renumber old 15–20 → 16–21 | «#263» |
| 7 | §11b | **Re-sweep** — cross-references green again after the insert | «#265» |
| 8 | §4 | Navigation layer — intent index, brief opener, reading paths | «#256» |
| 9 | §5 | Apparatus rebalance — boxes into running text, code into the decision chapters | «#257» |
| 10 | §6 | Diagrams — dispatch ladder, three decisions, two kinds of prefix | «#258» |
| 11 | §7b | Trailing guide-layer currency — voice-guide, MANUAL-DESCRIPTOR | «#259» |
| 12 | §8 | Front matter, cover title, `request.json` | «#260» |
| 13 | §9 | Documentation blast radius — the four artifacts no other task owns | «#261» |
| 14 | §10a | Draft render + page-level review (diagrams reviewed here) | «#262» |
| 15 | §10b | Audit, render, **release v1.1.0** | «#264» |

**Two atomic green-units, same shape: «#253» → «#255», and «#263» → «#265».** Each renumbers
chapters, which leaves the cross-reference checker red at the first task's completion *by
construction*; the second restores it. All four tasks say so in their own text. Do not treat
either red as a regression, and do not "fix" it by reverting the structural change.

**Sprint grew from 14 tasks to 15 on 2026-08-18**, when §11's scheduled decision was taken and
became build work — see §11.

**Not in this sprint, deliberately.** The fancyvrb `breaklines` platform fix («#250») is a
set-wide render change carried out of the closed «#249». Adopting it mid-sprint would mean
re-checking this manual's code lines against a changed wrapping model for no benefit — its K=76
budget is already clean. The Streamer Guide («#235») follows this manual; one at a time.
