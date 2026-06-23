# Doc Style-Change Sprint — Plan

*A cross-cutting "next revision" style pass over the live P2 manuals. Five elements,
one shared corpus survey feeding three of them. This is a **plan** (a commitment to ship
specific changes across the manuals), not a study.*

**Head:** Manual production (cross-cutting — not a single manual).
**Status:** STARTED 2026-06-23 (sprint-start complete; see record below). All decisions + questions
resolved; research complete for all five elements.
**Date:** 2026-06-23.

---

## Sprint-start record (2026-06-23)

- **Build number — bump only already-released documents, on approval.** This is a cross-cutting
  manual sprint, so there is no single outgoing number. **When the style change is approved, bump
  version numbers ONLY for documents that are already released** (a MINOR bump, re-shipped with the
  style pass). **Unreleased / in-development manuals do not bump** — they absorb the style change and
  receive their version at first release. The two pilots (P2 Architect's Guide, P2 I/O & Smart Pins
  User Guide) are unreleased → no bump; their pilot regens are verification renders, not releases.
- **Working tree — clean.** Three commits landed at start (plan + capitalization standard; Architect
  Blue Book scrub; Silicon Doc DOCX source). No untracked files in the platform/manual blast radius.
- **Tracking readiness.** 3 paused IOSP tasks (#54 expert-queue, #46 RECOMMEND_ADD disposition, #47
  IOSP audit regen) are a **separate, externally-gated effort — left paused**, not folded into this
  sprint. No completed tasks to archive; no in-progress leftovers.
- **Entry baseline.** Manual head = no local build gate (PDF Forge handback). Baseline = each in-scope
  manual's current clean render/audit state; the closeout exit assertion is **no render/audit
  regression**. (baseline-health's YAML validators do not apply.)

---

## Decisions to confirm before execution (one-pass)

Each carries my recommended answer. Confirm or redirect; once settled this section becomes the
binding scope.

- **D1 — Typography scope (Element 1).** The Plex Sans change reaches only the **unified
  XeLaTeX stack** (7 live manuals + torture instrument). Three manuals sit on a separate
  pdflatex/`lmodern` stack and cannot inherit it without a stack conversion: **ai-privacy-guide**
  (live, presentation-class), **spin2-reference-manual** (dormant), **smart-pins-tutorial**
  (dormant, retired Green Book). **Recommendation: exclude all three from this sprint**; note
  them as out-of-scope (ai-privacy is presentation-class by design; the other two are dormant).
- **D2 — Dead `.sty` cleanup (Element 1).** Every workspace still carries a per-manual
  `p2kb-<slug>-foundation.sty` / `-content.sty` that is **no longer loaded** (leftover from the
  pre-unification fork era; they still say "Latin Modern" and look authoritative). **Recommendation:
  bundle their deletion into this sprint** — leaving stale font files next to a font change is a
  foot-gun, and the quality bar favors the cleanup. (Sacred-rule note: deletion of *unreferenced*
  duplicates, history preserved in git.)
- **D3 — "silicon documentation" rule (Element 4).** Some hits are the capitalized title-reference
  ("the **Silicon Doc**", "(Source: Silicon Doc v35)") — clearly must-fix. Others are generic
  lowercase common-noun descriptions ("maintaining the detailed silicon documentation that defines
  their behavior"). **Recommendation: fix the capitalized title-references and explicit citations;
  leave generic lowercase descriptive uses** (they are not pointing at a specific document).
- **D4 — Frozen records left alone (Element 4).** **Recommendation: exclude** CHANGELOG history
  entries, the retired Green Book workspace scaffolding (~50 nickname hits), and `*-backup*.md`
  snapshots — editing them rewrites frozen records for no reader benefit. (Consistent with the
  `/history/` + `/archive/` leave-alone convention.)
- **D5 — Assembly-manual cross-reference to a retired doc (Element 4).** The Assembly manual body
  tells readers smart-pin details "appear in the **P2 Smart Pins Tutorial**" — a *retired* doc.
  **Recommendation: redirect to "P2 I/O & Smart Pins User Guide"** (fixes both the stale target and
  the nickname); verify the opus-master, then mirror.
- **D6 — Element 3 (copy-paste UX) — RESOLVED 2026-06-23.** **Remove line numbers from ALL code
  examples**, platform-wide. They are no longer needed now that code blocks continue across page
  breaks with visible framing (line numbers had been the page-continuation anchor). This is a
  platform `.sty` edit (the `Highlighting` Verbatim env + the `listings` path both carry the line
  numbering) and **bundles with Element 1**'s foundation edit. Bonus: dropping the line-number
  gutter reclaims horizontal room, partly offsetting Plex Mono's extra width vs. the K budget.
  *(Two residual questions this opens — Q1 prose line-number references, Q2 example-library
  still-in-scope — are in the Open Questions section below.)*

---

## Shared pre-work — one corpus survey, three consumers

Elements 2, 4, and 5 all ride a single pass over reader-facing manual text. Element 2's authority
(the capitalization rule table) is **already produced and confirmed**; Elements 4 and 5 inventories
are **already produced** (below). No further survey work is needed before execution — the sweep is
scoped.

Reader-facing scope = the opus-masters (`manuals/*/opus-master/*.md`) **and** their workspace render
twins (`workspace/*/*.md`). The opus-master is the authored source; the workspace copy is a generated
mirror. **Always edit the opus-master, then re-prepare** to regenerate the mirror — for **every**
manual, no exceptions. (The I/O & Smart Pins guide was once thought to be an exception with the body
living in the workspace render; that is wrong — its opus-master is a multi-file source
[`opus-master/front-matter.md` + `part-N/<chapter>.md`] that `assemble-manual.sh` `rm`+`cat`s into the
workspace render, so a workspace edit is destroyed on the next assemble. Edit the opus-master parts.)
Every per-master edit in Elements 4/5 has a mirror line to verify.

---

## 1. Typography / look-and-feel — adopt IBM Plex Sans

**Why.** Move the manuals from Latin Modern to a modern technical face (decided: font "B", IBM Plex
Sans), with a tuned heading scale and a code-block size that fits Plex Mono's wider glyphs.

**Current code starting point** (all in
`engineering/document-production/platform/templates/p2kb-platform-foundation.sty`):
- `:37` `\RequirePackage{fontspec}` — XeLaTeX stack, so by-filename loading is viable.
- `:38-40` body/sans/mono set **by name**: `\setmainfont{Latin Modern Roman}`,
  `\setsansfont{Latin Modern Sans}`, `\setmonofont{Latin Modern Mono}`.
- `:165-167` `\titlespacing*` for `\section`/`\subsection`/`\subsubsection` — **spacing only, no
  font size today** (chapter uses `\Huge`, subtitle `\LARGE`).
- `:347-356` `\DefineVerbatimEnvironment{Highlighting}{Verbatim}{…}` — **no `fontsize=`**, so fenced
  code currently renders at body size.
- `p2kb-platform-content.sty` holds code-box colors/geometry only — **no font declarations**.

**Target behavior.**
- Body/sans → **IBM Plex Sans**, mono → **IBM Plex Mono**, loaded **by FILENAME** (kpathsea:
  `Extension=.otf`, `UprightFont=*-Regular`, etc.) per the Forge font-loading rule — Plex is present
  on the Forge; by-name fails for it.
- **Add** `\titleformat` font sizes: section **17.3pt**, subsection **14.4pt** (net-new — today only
  spacing exists; verify no collision with the chapter `\Huge` / subtitle `\LARGE` hierarchy).
- **Add** block-code shrink to **8.5pt** via a single foundation-level `\fvset{fontsize=…}` (or a
  `fontsize=` key on the `Highlighting` env) — Plex Mono runs ~15% wider than LM Mono, so the shrink
  keeps code within the per-manual line budget K.

**Blast radius.** One edit to `p2kb-platform-foundation.sty` propagates to **all 7 live manuals +
the torture instrument** (all load the platform pair by package name). `content.sty` is touched only
if the 8.5pt shrink is sited on the code boxes instead of a global `\fvset`. The three pdflatex
outliers (D1) are not reached.

**Verification (pilot before rolling to all).** Per the standing decision, regenerate **two** real
production manuals on the new platform and review the renders:
1. **P2 Architect's Guide** (Architecture doc)
2. **P2 I/O & Smart Pins User Guide** (the live Smart Pins document)
- Normal case: body/heading/code look holds across full docs (not just a 3-chapter demo).
- Edge case: the **widest code listings** stay within budget K at 8.5pt (no wrap) — Plex-Mono-width
  regression check per the code-line audit.
- Error case: fonts resolve on the Forge (by-filename load succeeds; no fallback-to-default silent
  substitution). A clean pilot green-lights the rest; then certify on the torture instrument (it
  ships the exact platform bytes).

---

## 2. Capitalization discipline — apply the derived rule table

**Why.** De-ritualize habitual prose capitals, following **Parallax's own observed discipline** (not
an invented house style). Authority already built.

**Authority (done).** `engineering/standards/documentation-standards/capitalization-and-terminology-standard.md`
— the rule table derived from the Silicon Doc v35, Spin2 v55, and P1 Manual corpus, with all four
edge decisions (hub=lowercase, keep PASM2, hyphenated hub-exec, lowercase egg beater) **confirmed**.

**Target behavior — the 3-bucket sweep** over reader-facing manual text:
1. **DE-CAP** prose capitals on generic component nouns: cog, hub, smart pin, pin, streamer, lock,
   event, interrupt, flag, register, bytecode, method, object, operator, hub-exec, egg beater —
   leaving headings, table/label cells, named registers, numbered instances, and sentence-initial
   caps untouched.
2. **KEEP** product/language/proper names: Spin2, PASM2, Propeller 2, P2, Parallax, Goertzel.
3. **KEEP** true acronyms & code mnemonics verbatim: LUT, CORDIC, FIFO, DAC, ADC, PLL, NCO, RAM, ROM,
   PWM, instruction mnemonics, register names. Acronym plurals = caps + lowercase s (DACs, RAMs).
   Compounds = lowercase descriptor + caps acronym (hub RAM, cog RAM, LUT RAM).

**Integration / risk.** This is the highest-volume, highest-judgment edit — it touches every manual
body. It must run as a **reviewed sweep**, not a blind regex: the de-cap bucket depends on
distinguishing prose from headings/labels/named-things, which a raw substitution cannot do. Run
per-manual, produce a located change list, and self-review before the render.

**Verification.**
- Normal: spot-check that prose "the cog", "a smart pin", "hub RAM" read correctly post-sweep.
- Edge: confirm headings/table cells/`LOCK[n]` notation/numbered "Cog 0" were **not** de-capped.
- Error: no acronym got lowercased; no product name (Spin2/PASM2) got touched.

---

## 3. Code examples — remove line numbers (+ browser-routed example library, pending Q2)

**Why.** Line numbers were the page-continuation anchor for code blocks. Now that blocks continue
across page breaks with visible framing, the numbers are no longer needed — and they were one of the
two things that broke in-PDF copy (line-number text leaked into the copied selection). Removing them
platform-wide simplifies every code block and reclaims the gutter's horizontal room.

**Current code starting point** (line numbering lives in two places, both in
`p2kb-platform-foundation.sty`):
- `:347-356` `\DefineVerbatimEnvironment{Highlighting}{Verbatim}{…}` — carries the `numbers` key for
  fenced/Verbatim code (the colored Spin2Block/IOSPBlock boxes wrap this).
- `:255-276` `\lstset{…}` — the `listings` path's line-number settings (used by filters that emit
  `lstlisting`).

**Target behavior.**
- Drop line numbering from **both** paths so no code example renders a number gutter, platform-wide
  (reaches all unified manuals — bundles with the Element 1 foundation edit).
- Confirm block-continuation framing reads correctly across a page break without the numbers.

**Example-library ZIPs — distributed via the roster, NOT linked inside the document (RESOLVED
2026-06-23).** macOS Preview **drops whitespace** on in-PDF copy independent of line numbers, so clean
copy still needs the file route — the ZIPs stay. But the distribution model changes from the earlier
"auto-download link inside the PDF" design:
- **No download links inside the PDF documents.** The earlier in-document auto-download link is removed.
- **Per-manual EXAMPLE-LIBRARY ZIP published alongside the document PDF** in the public deliverables
  area (next to where the PDF is downloaded).
- **The link to each ZIP lives in the public manuals roster / release index** (the
  reader-facing "which manuals are available" download listing), not in the document body.
- **Inside the document: only the per-block filename caption** stays — it maps a printed block to its
  file in the ZIP, but is a caption, not a link.
- **Per-example individual file links: NOT included** (decided 2026-06-23). Distribution is the
  whole-manual ZIP via the roster only; there are no per-example file links, inside or outside the
  document. The filename caption + the ZIP is the entire mechanism.

> **Mechanism established #102 (2026-06-23) — see
> `engineering/document-production/methodology/example-library-mechanism.md`.** The library is
> **curated, not auto-extracted**: only complete runnable worked examples get a file, reconciling with
> the convention already shipped by the DEBUG Window Manual (semantic `chNN-description.spin2` names, a
> README index). The naming is `chNN-description.spin2` (NOT the placeholder `example_NNN` this plan
> first sketched). An example is marked by a **filename caption attribute on its code fence**
> (` ```{.spin2 caption="chNN-…spin2"} `), which is the single source of truth for both the printed
> caption (rendered by the code-coloring filter) and the extracted file
> (`engineering/tools/conversion/build-example-library.py` → files + ZIP). Snippets stay uncaptioned
> and unextracted. Proven end-to-end before rollout.

**Integration point.** This adds a companion-artifact step to the release path: the release/roster
process must publish each manual's example-library ZIP beside its PDF and add the ZIP link to the
public download index (alongside the existing PDF force-download link). See the release-process note
in the skill-evolution candidates.

**Verification.**
- Normal: no code block shows a line-number gutter; framed blocks continue cleanly across page breaks;
  each manual's ZIP downloads from the roster link and its files match the printed filename captions
  (`chNN-description.spin2`), whitespace intact.
- Edge (Q1): any prose that referenced a code line number ("on line 12") has been reworded — a block
  with no numbers must not be referenced by number.
- Error: no example renders a stray gutter or mis-wrapped line; **no ZIP/download link appears inside
  any PDF**; no roster entry points at a missing ZIP.

---

## 4. Naming discipline — official titles, no nicknames

**Why.** Every doc has an official title from day one; reader text must use it. No internal codenames;
no stale cross-doc names.

**Authoritative title list** (use verbatim when one doc references another):
P2 Architect's Guide · P2 I/O & Smart Pins User Guide · **P2 Assembly Language Reference** · DeSilva
PASM2 Tutorial · P2 Debug Window Manual · P2 Single-Step Debugger Manual · P2 Streamer Programming
Guide · AI Privacy Guide · Spin2 Reference Manual. Retired → redirect: Smart Pins Tutorial ("Green
Book") → P2 I/O & Smart Pins User Guide.

**Inventory (reader-facing must-fix, ~8 files).** Each opus-master edit mirrors to its workspace twin.
- **"Silicon Doc / Silicon Documentation"** → "Parallax Propeller 2 Documentation v35 - Rev B/C":
  Architect (front-matter.md:115; body 166, 216, 302, 1680 + workspace mirror), Streamer
  (front-matter.md:144; body 205, 673 + mirror), I/O & Smart Pins (opus-master: front-matter.md:135;
  ch07-pulse-transition:274, ch19-usb:117 — DONE #104), DeSilva (COMPLETE-OPUS-MASTER.md:5818 +
  mirror). ~30 line-hits.
- **"P2 Assembly Language Manual"** → **"P2 Assembly Language Reference"**: Architect
  (front-matter.md:116; body 108, 166, 270, 510, 672, 725, 972, 1668 + mirror). ~22 line-hits.
- **"Spin2 Language Reference" / "Spin2 documentation"** → "Spin2 Reference Manual": Architect
  (body 725, 868; front-matter 116). ~6 line-hits.
- **Stale cross-ref to retired doc** (D5): Assembly manual body "P2 Smart Pins Tutorial" → "P2 I/O &
  Smart Pins User Guide" (P2-Assembly-Language-Manual-PartI.md:2308 / .md:3119 — verify opus-master).

**Out of scope (D3/D4).** Generic lowercase "silicon documentation" descriptions; CHANGELOG history;
retired Green Book scaffolding; `*-backup*.md` snapshots; the broad `engineering/` supporting tree
(~229 hits in process docs) — not reader text.

**Verification.**
- Normal: each fixed reference reads with the official title; the doc still scans naturally.
- Edge: master and workspace mirror both updated (no half-fixed twin); generic descriptive uses left
  intact per D3.
- Error: no official title mistyped; no live reference still points at a retired doc.

---

## 5. No KB/YAML/MCP plumbing in reader text

**Why.** The manuals are the human face of the knowledge base; reader prose references concepts and
other human docs, never the internal store/YAML/MCP machinery.

**Inventory — 6 confirmed leaks, all in the P2 Architect's Guide** (edit masters, mirror to
workspace). The pattern is "lives in the decomposition layer of the knowledge base / golden home /
consume the YAML":
- `opus-master/front-matter.md:113` — "trusted documents of the **P2 Knowledge Base**" → "trusted P2
  reference documents".
- `front-matter.md:117` — "**decomposition reasoning layer** … the chapter derives from it" → recast
  as the human concept (the design method Chapter 4 teaches), or drop the bullet.
- `front-matter.md:127` — **"consume the YAML for the facts"** (worst leak; addresses tooling inside a
  human manual) → remove the bullet, or "the reference manuals carry the exhaustive facts".
- `architect-guide-body.md:871` — "has its own reference in the **knowledge base**" → "in the P2
  reference manuals".
- `architect-guide-body.md:970` — "lives in the **decomposition layer of the knowledge base**" →
  point at Appendix A / the design-method references (the sentence already cites a human doc for the
  other half — make both halves human-facing).
- `architect-guide-body.md:1412` — "lives in the decomposition layer of the P2 knowledge base, the
  **golden home** for this theory" → point at Appendix A + the reading list.

**Borderline (your call).** DeSilva acknowledgments "AI-optimized knowledge base" (COMPLETE-OPUS-MASTER.md:121)
describes the project's mission/provenance, not where P2 facts live — defensible to leave.

**Leave alone (false positives, verified).** The title-page "P2 Knowledge Base Project" imprint byline
(authorship/provenance, every manual); intra-manual "documented in its chapter" cross-references; DSP
"aliases" / "category" used in their genuine P2 senses.

**Verification.**
- Normal: each reworded passage points the reader at a real human resource (a manual, an appendix).
- Edge: the imprint byline and legitimate cross-references untouched.
- Error: no remaining reader prose names the YAML, the store, the MCP, or "download-on-demand".

---

## Execution order (when the sprint runs)

1. **Element 1 typography** edit → pilot regen (Architect + I/O & Smart Pins) → review → certify on
   torture instrument → (on green) it's live for all unified manuals. D2 dead-`.sty` cleanup rides here.
2. **Elements 2 + 4 + 5 sweep** over reader-facing text, per manual, reviewed not blind — they share
   the same files, so sweep each manual once for all three, produce a located change list, self-review.
3. **Element 3** unblocked parts; hold the line-number call for the v7 result (D6).
4. **Re-prepare + regenerate** each touched manual; verify renders; promote per the normal
   release path (each manual owns its CHANGELOG/version).

Per-manual CHANGELOG entries for the style pass are deliverables of step 4.

---

## Open Questions

Each carries a recommended resolution; the plan is final once these are settled.

- **Q1 — RESOLVED 2026-06-23: magnitude is ~zero — global removal is safe.** Surveyed all
  reader-facing manual text (opus-master bodies + workspace render copies) for numeric line
  references (`line N`, `lines N–M`, `line #N`, "on/see/at line N", "line number(s)"). **No manual
  body prose references printed code line numbers.** The only `line N` body hits are the PLOT `LINE`
  drawing command in the Debug Window manual (a P2 primitive, unrelated). The only numeric "lines
  N–M" references in the whole tree are in **internal scaffolding** (punch-lists, Green-Book audit
  matrices) pointing at *source-file* line ranges (e.g. "p2-documentation.txt lines 6660–6850") —
  those don't render and aren't affected. So line numbers can be removed globally with no orphaned
  references; no selective retention needed, and the "reword prose refs" sub-task is effectively
  empty (a confirm-pass during the sweep, expected zero edits).
- **Q2 — RESOLVED 2026-06-23: keep the ZIPs, distribute via the roster.** Whitespace-drop in Preview
  is real, so the example-library ZIPs stay — but published alongside the PDFs with the link in the
  public roster/release index, never inside the document. See Element 3 for the full revised model.

## Open dependencies (must be clear within execution)

- **Element 1** — K (code-line budget) is LM-Mono-calibrated; the 8.5pt Plex-Mono render-verify on the
  widest listings is a gating check inside the pilot, not an afterthought. The reclaimed line-number
  gutter (Element 3) partly offsets Plex Mono's extra width.
- All other research is complete; no element carries an unresolved "figure it out later".

---

## Section ↔ task cross-reference (tag: `doc-style-change`)

Elements 2/4/5 share one reviewed pass per manual, so they are delivered **distributed across the
per-manual tasks** rather than as standalone tasks. Element 1's line-number removal rides the platform
task; Element 3's library mechanism is its own task, then applied per-manual.

| Plan § | Deliverable | Task(s) | seq |
| --- | --- | --- | --- |
| §1 Typography | Platform Plex/heading/8.5pt edit + D2 cleanup, pilot-verified | «#100» | 1 |
| §1 Typography | Torture-instrument certification | «#101» | 2 |
| §3 Code examples | Line-number removal (platform) | «#100» | 1 |
| §3 Code examples | Example-library mechanism (convention + ZIP build + roster distribution) | «#102» | 3 |
| §2+§4+§5+§3 | Per-manual style pass — Architect's Guide (E2+E4+E5+captions) | «#103» | 4 |
| §2+§4+§3 | Per-manual style pass — I/O & Smart Pins User Guide | «#104» | 5 |
| §2+§4+§3 | Per-manual style pass — Assembly Language Reference (incl. D5 redirect) | «#105» | 6 |
| §2+§3 | Per-manual style pass — Debug Window Manual | «#106» | 7 |
| §2+§4+§3 | Per-manual style pass — DeSilva PASM2 Tutorial | «#107» | 8 |
| §2+§3 | Per-manual style pass — Single-Step Debugger Manual | «#108» | 9 |
| §2+§4+§3 | Per-manual style pass — Streamer Programming Guide | «#109» | 10 |
| §1+§3 close | Regen + release (already-released only) + roster ZIP links | «#110» | 11 |

Per-manual coverage: **§2 (capitalization)** = all 7 passes; **§4 (titles)** = Architect, I/O & Smart
Pins, Assembly, DeSilva, Streamer; **§5 (plumbing)** = Architect only.
