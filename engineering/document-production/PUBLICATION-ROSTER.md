# Publication Roster

Tracks every **manual-shaped** publication and document instrument in
`engineering/document-production/`, by category. The categories drive both
**consistency scope** (only the live set must stay mutually consistent) and
**how skills resume work** (e.g. `whats-next` reads this roster to decide
resume-vs-revive-vs-new).

Categories: **Live** (in front of the community) · **In development / parked**
(intended; may be a pre-production walk-away — *not* orphaned) · **Instruments**
(test/standards harnesses, not publications) · **Orphaned** (not carrying
forward). The discriminator between *parked* and *orphaned* is **intent**, not
state — a started-then-paused doc is parked if we still mean to ship it.

**Invariant:** every `workspace|manuals|outbound/<name>` manual folder — and every
`app-notes/<P2ANxxx>/` note in production — appears in exactly **one** section below. A
folder with no entry is an **anomaly to reconcile** (classify it), not a silent guess.

*Established: 2026-05-28 — Updated: 2026-06-09 (Platform column corrected against
on-disk reality: I/O & Smart Pins / Assembly / DeSilva are bespoke forks ⏳ — NOT
yet migrated; Single-Step / Streamer confirmed ✅ on the shared platform stack).
2026-06-05: categorized into live / parked / instruments / orphaned; Green Book
retired in favor of the I/O & Smart Pins guide.*

---

## Live publications

These are the live working set. Any shared visual or editorial convention MUST be
kept consistent across the live set — a change to one that affects a shared
convention is a change to all of them.

**Status pipeline** — each manual migrates left → right through these gates. `Chip`
and `Community` review are **independent** (a manual can be released and
community-reviewed while chip review is still outstanding — see Assembly / DeSilva).
Markers: ✅ done · 🔄 in review / in progress · ⏳ awaiting · — n/a · _(blank)_ not yet reached.
`Platform` = migrated onto the shared **`p2kb-platform`** display stack and its
cross-publication conventions (the **Rule** at the bottom); `—` = a different class
that does not ride the shared stack.

| Publication | Slug | Draft | Assets | Platform | Chip review | Community review | Released | Notes |
|-------------|------|:--:|:--:|:--:|:--:|:--:|:--:|-------|
| Getting Started with the Propeller 2 | `p2-getting-started-guide` | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | **v1.0.0 (2026-06-24)** — initial community-review release. The orientation on-ramp, split 2026-06-24 from the P2 Architect's Guide first draft (orientation Chs 1–3 "Meet the Propeller 2" / "Reading P2 Code" / "Putting It to Work" + Where-to-Next); born on the shared platform stack with `p2kb-getting-started-*` locals; release-gate audited (drain GREEN) + finalized; 25pp. Links out to the reference manuals + the Architect's Guide. chip review outstanding |
| P2 I/O & Smart Pins User Guide | `p2-io-and-smart-pins-user-guide` | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | **v1.0.0 released 2026-07-03** (396pp, Community Review Edition) — MAIDEN release; 19 chapters covering all 32 smart-pin modes + Appendices A-G + 15-program example ZIP. Terminal step of the IOSP Release Campaign (folded in the USB study + P2AN003 DAC + P2AN004 Freq/Period/Pulse boundary-enrichment). Release-gate audited: 5 HIGH + ~12 MED + ~14 LOW resolved via document-finalize; drain gate GREEN (F-191 shipped in KB v1.13.3); cross-ref filter PILOT (adopted + visually audited); render-verified (compile-clean, 0 heading widows, Appendix A links 42->0, full outline). Chip-review expert-queue items parked (external). "Blue Book" reference |
| P2 Assembly Language Reference | `p2-assembly-language-manual` | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | **v3.1.1 (2026-06-29)** — Ch.1 execution-model refinements (cog/LUT as one space + §1.4.4 streamer/blocking-transfer), §2.8.3 Operation:-line guidance + CMP family-consistency fix; uppercase mnemonics in prose; 503pp, render-verified. chip review outstanding |
| DeSilva PASM2 Tutorial | `p2-pasm-desilva-style` | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | **v3.0.1 (2026-06-25)** — accuracy re-audit (every PASM2/Spin2 example compile-checked with `pnut-ts` against the current compiler), typography refresh on the shared platform stack (Plex, no line-number gutter, 8.5pt code boxes; ✓/✗/θ glyph fallbacks), lowercase house-style sweep, and a companion example-library ZIP (first-blink, multicog-blink, hub-counters). **Resolves both prior DEFERRALS:** the Cog-Anatomy diagram is repaired ("Each Cog Contains:") and the full pnut-ts compile-cert is done. Regenerated clean (162pp; 172→162 from the denser typography, outline verified complete). Release-gate audit: local `audit/release-gate-2026-06-25.md`. Prior **v3.0.0 (2026-06-10)** absorbed the ~33-error content re-audit + Ch2 egg-beater fix. chip review outstanding. |
| P2 Debug Window Manual | `p2-debug-window-manual` | ✅ | ✅ | ✅ | | ✅ | ✅ | **v1.0.1 (2026-06-26)** — accuracy + typography refresh: DEBUG-output quoting examples corrected data-set-wide, FFT/run-up worked programs fixed, per-window details tightened (trigger offsets, defaults/ranges, PLOT polar, ALT, MIDI), IBM Plex typography (156pp); 32-demo example library refreshed (source ZIP). Prior **v1.0.0 (2026-06-16)** initial community-review release. |
| P2 Single-Step Debugger Manual | `p2-single-step-debugger-manual` | ✅ | ✅ | ✅ | ⏳ | ⏳ | | on shared platform stack (foundation/content/diagrams); awaiting chip + community review |
| P2 Streamer Programming Guide | `p2-streamer-programming-guide` | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | **v1.0.3 (2026-07-03)** community-review edition — Wave-3 designer-authoritative additions (SINC2 constant-iteration constraint §10.4 · HDMI/DVI blanking guidance §15.2 · capture-to-spectrum pointer §9.2, all grounded in KB HEAD YAML) + cross-ref filter adopted (82 links, 0 dead); release-gate audited (`audit/release-gate-2026-07-03.md`), render-verified 75pp/0 glyph drops. Prior v1.0.2 (2026-06-26) IBM Plex refresh + LUMA8 table. chip review outstanding |
| AI Privacy Guide | `ai-privacy-guide` | ✅ | ✅ | — | ✅ | ✅ | ✅ | released; both reviews complete; presentation-class (rides pristine `p2kb-foundation.sty`) |

**Slug** is the one folder name each manual uses across all three trees —
`manuals/<slug>/`, `workspace/<slug>/`, and `outbound/<slug>/`. When a manual needs
more detail than fits in **Notes**, add a slim `↳` continuation row (markers blank,
detail in Notes).

## In development / parked (NOT live)

Intended for production but not released — actively progressing or a
pre-production walk-away we still mean to ship. Free to evolve independently;
they do **not** constrain the live set and are **not** constrained by it until
promoted. Reconcile conventions against this roster at promotion.

| Publication | Workspace | State |
|-------------|-----------|-------|
| Spin2 Reference Manual | `workspace/spin2-reference-manual/` | parked; may go forward |
| **P2 XBYTE Programming Guide** | `manuals/p2-xbyte-programming-guide/` + `workspace/p2-xbyte-programming-guide/` | **in development — STOOD UP 2026-06-26, v0.1.0 first-draft authored.** New manual modeled on the Streamer guide (layout/richness/two-register voice), twin on the shared `p2kb-platform-*` stack. Teaches the XBYTE hardware bytecode engine + the skip family (SKIP/SKIPF/EXECF) + FIFO/LUT dispatch, then builds a minimal custom VM and a tiny illustrative **6502** emulator (+ a 6809 SETQ2 vignette). **Scope narrowed with Stephen (PLANNING.md §0):** external P2 projects (Arc8de, Yume suite) → **Appendix C links only**, not narrative; "systems similar to the P2" (IBM Series/1 EDL anchor, Transputer/Occam, XMOS, GreenArrays, Cell SPE) **DEFERRED** out of this edition. Full triad stood up (creation-/voice-guide, MANUAL-DESCRIPTOR, CHANGELOG, opus-master, grounding digest) + workspace wiring. NEXT: prepare-manual → Stephen generates the v0.1.0 review PDF on the Forge. Subtitle "Building Interpreters and Emulators on the Propeller 2". |
| **The P2 Architect's Guide** (design book) | `manuals/p2-architect-guide/` + `workspace/p2-architect-guide/` | **in development — SPLIT in progress (2026-06-24).** The v0.1.0 first draft (4 ch, 48pp, born on the unified `p2kb-platform-*` stack) is being divided into two books after a walkthrough review (`manuals/p2-architect-guide/audit/walkthrough-feedback-2026-06-24.md`). **This folder retains the design / realization book** — *The P2 Architect's Guide — Designing Real Systems on the Propeller 2* — keeping Ch4 (functional decomposition) + a new front-end (peripherals → buses → pin budget) + a realization / AI-assist pillar. Orientation Chs 1–3 split out to **Getting Started**, now released v1.0.0 (see the Live table). Charter / voice / changelog to be re-cut to the design scope. |

## Instruments (not publications)

Test / standards harnesses. Manual-shaped (full folder triad, generate PDFs) but
never released; each serves an **effort**, not the community. Not
consistency-bound. Resume into the effort it serves. **An instrument's analysis
IS its product** — unlike a publication's transient release-audit, its `audit/`
is **git-tracked** alongside its cases (see the `.gitignore` exception), so the
instrument, its analysis, and the fixes it drives version together.

| Instrument | Workspace | Serves |
|------------|-----------|--------|
| P2 Layout Torture Test | `workspace/p2-layout-torture-test/` | the manual layout-standards effort (`methodology/manual-layout-standards-*`) |

## Orphaned (not carrying forward)

Started, then retired by decision — superseded or abandoned. Kept for history;
**not** resumed without an explicit revive decision; never consistency-bound.

| Publication | Workspace | Why retired |
|-------------|-----------|-------------|
| Smart Pins Tutorial ("Green Book") | `workspace/p2-smart-pins-tutorial/` | superseded by the I/O & Smart Pins User Guide (newer generation) |

## Application Notes (`P2ANxxx`)

A distinct document class (see `app-notes/README.md`) — application-driven,
single-technique, one runnable example, each shipping a **YAML companion** (the
four-artifact model). Canonical source lives in `app-notes/<P2ANxxx>/opus-master/`; each
note in production also has a `workspace/<P2ANxxx>/` render folder (covered by the folder
invariant above). Notes ride the shared `p2kb-platform-*` stack (K = 76) and are therefore
bound by the **shared conventions below**, but they are **not** part of the live-publication
consistency set until released.

**The candidate backlog + production plan is its own register** —
[`engineering/analysis/p2-app-note-roster.md`](../analysis/p2-app-note-roster.md) (families
A/B/C, the standalone USB note, the disposition ledger). The table here tracks only notes
**in production** (folder stood up); candidates stay in that register until they enter
production.

| App note | Slug | State |
|----------|------|-------|
| **P2AN001 — Single-Pin ADC Instrumentation** | `P2AN001` | ✅ **v1.0.0 released 2026-07-03** (20pp) — foundational first note + doc-class & companion-schema exemplar (Family A0); techniques-catalog on the enriched IOSP Ch.16; ships a YAML companion (`application-notes/p2an001-single-pin-instrumentation-adc.yaml`) + example ZIP. First app-note release. |
| **P2AN002 — CORDIC for Real Work** | `P2AN002` | ✅ **v1.0.0 released 2026-07-03** (14pp) — lead of the Math family (B1); techniques-catalog (6 recipes + FOC/Park ceiling, OBEX #2811); ships a YAML companion + example ZIP. |
| **P2AN003 — DAC & Analog Signal Generation** | `P2AN003` | 🔴 **planned — stood up 2026-06-30** (Family A1; output sibling to ADC). Committed to production as Input 2 of the **IOSP Release Campaign**; boundary-determination pending → enriches IOSP DAC content + authored to PDF. |
| **P2AN004 — Frequency / Period / Pulse Measurement** | `P2AN004` | 🔴 **planned — stood up 2026-06-30** (Family A2; timing instrumentation). Committed to production as Input 3 of the **IOSP Release Campaign**; boundary-determination pending → enriches IOSP measurement content + authored to PDF. |

---

## Shared conventions across the live set

### Code-block color = language (IDE-aligned)

One color = one language, so a reader moving between the live publications never
has to relearn the palette. Values match the Propeller Tool / FlexProp IDEs.

| Block | Color | Background | Border |
|-------|-------|-----------|--------|
| Spin2 | blue | `E3F2FD` | `1976D2` |
| PASM2 | green | `EBFCEB` | `4CB04C` |
| CORDIC | purple | `F8F5FF` | `A785C2` |
| Multi-COG | blue-gray | `F5F9FC` | `7FA8C9` |
| Antipattern | pink/red | `FFF5F5` | `C08080` |

Geometry (all five): `boxrule=2pt`, `leftrule=4pt` (accessibility), other rules
`0.5pt`, rounded corners, `left=30pt` (clears inset line numbers), `right=10pt`,
`top/bottom=8pt`, `before/after skip=15pt`, `breakable`.

Defined **once** in the shared platform content package for every reconciled live
publication:
- `platform/templates/p2kb-platform-content.sty` — used by **Assembly Language
  Reference**, **Debug Window**, **Single-Step Debugger**, **Streamer**, **DeSilva**,
  and **I/O & Smart Pins** (all six live technical publications).

> All live technical publications are now reconciled onto the shared
> `p2kb-platform-*` stack — the **Assembly Language Reference** completed migration in
> **v3.0.0 (2026-06-10)**, retiring the last bespoke fork (`p2kb-pasm2-*`; its
> `p2kb-pasm2-content.sty` is now vestigial). The AI Privacy Guide is
> presentation-class and does not ride the shared stack.

> **Note:** In the I/O & Smart Pins guide the assembly/PASM2 code-block
> environment is named `IOSPBlock` (guide-specific name) but is colored **green**
> — the PASM2 color — for cross-publication consistency, NOT yellow.

**Rule:** Do not diverge a shared convention in one live publication without
updating all reconciled live publications together. When a dormant publication is
promoted to live, reconcile its conventions against this roster as part of the
promotion.

---

## Platform Freshness Ledger — which manuals need reproduction

Because the manuals share one `platform/` stack (see the column pipeline above), a
manual's PDF goes stale the moment a **platform file it consumes** is changed after
that PDF was generated. This ledger is the detector.

**How it works — a push-down list, newest on top:**
- **Append a `PLATFORM` line** every time a `platform/` file is modified.
- **Append a `PUBLISH` line** every time a manual's PDF is generated (record it when
  the generation is *confirmed clean*, not merely staged).
- **A manual is OUT OF DATE** if any `PLATFORM` line for a file *it consumes* sits
  **above** (newer than) that manual's most-recent `PUBLISH` line.
- **Prune to stay short:** collapse same-item duplicates to the latest; **drop a
  `PLATFORM` line once every consuming manual has a `PUBLISH` above it** (fully
  absorbed — git keeps the permanent modification history, so the ledger only carries
  what is still live). When all platform changes are absorbed, only `PUBLISH` lines
  remain → everything is current.

> **Source (2026-06-10):** `PUBLISH` datetimes are the **actual PDF mtimes from the
> Forge outbox** (the authoritative generation times); `PLATFORM` datetimes are the git
> commit that last modified each file. Two fully-absorbed platform lines (`tables.lua`
> 2026-06-06, `mnemonic-bold.lua` 2026-06-06 — every manual generated after them) were
> pruned on seeding. The **Assembly Language Reference** completed its platform
> migration on 2026-06-10 (v3.0.0) and now appears in the ledger like the others.

```
2026-07-03 18:53  PUBLISH   P2AN002                          (v1.0.0, 14pp — app-note #2: CORDIC techniques-catalog (6 recipes + FOC ceiling); app-note-class templates over the shared platform; render-verified, 0 missing chars, no empty ToC, all recipes present)
2026-07-03 18:21  PUBLISH   P2AN001                          (v1.0.0, 20pp — FIRST app-note release: single-pin instrumentation-ADC techniques-catalog; app-note-class templates over the shared platform stack; render-verified, 0 missing chars, no empty ToC, all recipes present)
2026-07-03 17:45  PUBLISH   p2-streamer-programming-guide    (v1.0.3, 75pp — Wave-3 designer-authoritative additions: SINC2 constant-iteration constraint §10.4, HDMI/DVI blanking guidance §15.2, capture-to-spectrum pointer §9.2; cross-ref filter adopted, 82 links/0 dead; render-verified, 0 missing chars, outline complete)
2026-07-03 05:06  PUBLISH   p2-io-and-smart-pins-user-guide  (v1.0.0, 396pp — MAIDEN release: 19 chapters covering all 32 smart-pin modes + Appendices A-G + 15-program example ZIP; document-finalize resolved 5 HIGH + ~12 MED + ~14 LOW release-gate findings; cross-ref filter adopted (pilot); render-verified: compile-clean, 0 heading widows, Appendix A links 42->0, full outline; drain gate GREEN — F-191 shipped in KB v1.13.3)
2026-07-02 22:51  PLATFORM  filters/p2kb-platform-figures.lua         (emit_reserve(): a keep-together \needspace reserved before a lead-in+box/table pair now goes BEFORE a preceding heading, so the heading migrates with its unit instead of widowing — the real fix for the heading-at-page-bottom class. Benefits every manual; IOSP proved 11->0 widows.)
2026-07-02 22:51  PLATFORM  filters/p2kb-platform-crossref.lua        (Table cell-walker: links "Chapter N"/§ refs inside table cells when crossref runs BEFORE the tables filter — IOSP Quick-Mode-Matrix piloting; harmless no-op otherwise. Adopting manuals must list crossref before tables in request.json.)
2026-07-02 22:51  PLATFORM  templates/p2kb-platform-foundation.sty    (heading keep-with-next: \needspace on \section only (removed from subsection — it stranded sections) + Shaded code-box bound to its lead-in with \nobreak; completes the widow fix with figures.lua.)
2026-07-02 06:07  PLATFORM  filters/p2kb-platform-pagination.lua      (escape LaTeX specials & % $ # _ in the \chaptersubtitle{} argument — a raw & in an em-dash chapter subtitle (IOSP Ch.15 "Periods, Duty & Reciprocal Counting") reached xelatex unescaped and aborted the build. Benefits every manual using em-dash chapter subtitles.)
2026-07-02 06:07  PLATFORM  filters/p2kb-platform-crossref.lua        (F4: add "Ch" as a Form-A keyword so "Ch N" table-cell refs auto-link alongside "Chapter"; IOSP Quick-Mode-Matrix piloting.)
2026-07-02 06:07  PLATFORM  templates/p2kb-platform-foundation.sty    (F7: \needspace keep-with-next on section/subsection/subsubsection star-form titleformats so a heading cannot widow at page bottom — fixes IOSP §9.3.)
2026-07-02 06:07  PLATFORM  templates/p2kb-platform-content.sty       (F10: ModeBlock top rule "borderline north" 4pt->1.5pt — thins the Appendix-F mode-card corner marker's horizontal stroke; vertical west stays 4pt.)
2026-06-29 19:58  PUBLISH   p2-assembly-language-manual      (v3.1.1, 503pp — Ch.1 execution-model refinements + §1.4.4 streamer/blocking-transfer + CMP Operation: line; uppercase mnemonics in prose; render-verified, 0 missing glyphs, clean compile log)
2026-06-29 19:00  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (v3.0 STYLE POLICY: prose mnemonics now render UPPERCASE, NOT bold — uppercase carries the token's identity and matches its code appearance; bold is reserved for genuine emphasis. Also ends the uneven-bold bug where punctuation-adjacent mnemonics ("(ALTS", "RDFAST/WRFAST") bolded only partially. AUTOMATIC for EVERY manual on its NEXT render — a visible prose-style change, but NOT a forced re-release. First absorbed by Assembly Language Reference v3.1.1.)
2026-06-26 18:15  PLATFORM  filters/p2kb-platform-crossref.lua        (NEW: auto-links "Chapter N"/"Appendix X"/"Section N.N"/"§N.N" prose refs to anchors; opt-in per request.json, IOSP piloting. OTHER MANUALS: adopt + visual-audit on NEXT release — NOT a forced release; tracker: CROSSREF-FILTER-ADOPTION.md)
2026-06-26 05:09  PUBLISH   p2-debug-window-manual           (v1.0.1, 156pp — accuracy + typography refresh: DEBUG-quoting examples + FFT/run-up programs + per-window details; IBM Plex, 0 missing chars; outline verified complete)
2026-06-25 23:31  PUBLISH   p2-pasm-desilva-style            (v3.0.1, 162pp — accuracy re-audit + Plex typography refresh; ✓/✗/θ glyph fallbacks clean, 0 missing chars; outline verified complete)
2026-06-25 23:22  PLATFORM  templates/p2kb-platform-foundation.sty   (glyph fallbacks via newunicodechar + listings literate: ✅/✓/❌ → green \checkmark / red \times, and θ → \rmfamily Greek theta; collapses the 03:53 Ω/μ/µ line, file now carries all; daemon-verified clean on deSilva v3.0.1 — 0 missing chars)
2026-06-24 22:36  PUBLISH   p2-getting-started-guide         (v1.0.0, 25pp — initial Community Review Edition; release-gate audited + finalized; clean compile log, 0 overfull)
2026-06-24 21:01  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (AG-01: English-collision handling for call/push/ones/test — daemon-verified on Getting Started; other manuals low-urgency regen)
2026-06-23 05:30  PUBLISH   p2-architect-guide               (v0.1.0 first draft, 48pp — FOUR chapters + back matter + 5 figures; IN DEVELOPMENT, not a public release)
2026-06-19 20:41  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (do not bold the English verb "fit" — subject-pronoun + article-object contexts)
2026-06-19 19:10  PLATFORM  templates/p2kb-platform-content.sty       (add HardwareBlock graphite callout)
2026-06-19 19:10  PLATFORM  filters/p2kb-platform-code-coloring.lua   (map ::: hardware -> HardwareBlock)
2026-06-16 20:47  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (0ddf83f — stop bolding English-collision words: adds/byte/word/long)
2026-06-12 18:39  PLATFORM  templates/p2kb-platform-content.sty       (a149b8e — ::: tip/caution callouts)
2026-06-12 18:39  PLATFORM  filters/p2kb-platform-code-coloring.lua   (a149b8e — ::: tip/caution callouts)
2026-06-10 23:33  PUBLISH   p2-single-step-debugger-manual   (regression rebuild on the latest platform)
2026-06-09 22:50  PLATFORM  filters/p2kb-platform-figures.lua
2026-06-08 08:32  PLATFORM  templates/p2kb-platform-foundation.sty
2026-06-08 08:32  PLATFORM  filters/p2kb-platform-pagination.lua
2026-06-07 06:58  PLATFORM  templates/p2kb-platform-diagrams.sty
2026-06-07 03:04  PUBLISH   p2-layout-torture-test
```

**Currently out of date (read off the list above):**

**Cross-ref filter adoption (out-of-date flag, 2026-06-26).** The new
`p2kb-platform-crossref.lua` (clickable Chapter/Appendix/§ references) is opt-in per manual.
No manual is force-released for it; but every manual must **adopt + visually audit** it at its
next release. Per-manual status lives in `CROSSREF-FILTER-ADOPTION.md` (IOSP is the pilot;
all released manuals are PENDING AUDIT).

**Regeneration status (updated 2026-06-15).** A previously-unrecorded 2026-06-12
platform edit (`a149b8e` — `content.sty` + `code-coloring.lua`, advisory callouts) now
sits ABOVE the 2026-06-10 rebuild wave, so those four are technically behind it (the
callout change is cosmetic for manuals that use no `::: tip` / `::: caution` blocks — a
regen wave is due but low-urgency for them). Only `p2-debug-window-manual` was built on
top of the 06-12 platform.

| Manual | Status | Notes |
|--------|--------|----------------------------------------------------|
| `p2-debug-window-manual` | ✅ current | **v1.0.1 released 2026-06-26** (156pp); accuracy + typography refresh; built on the latest platform (06-25 glyph-fallback foundation + Plex) |
| `p2-assembly-language-manual` | ✅ current | **v3.1.1 released 2026-06-29** (503pp); first to render the uppercase-mnemonic platform filter |
| `p2-pasm-desilva-style` | ✅ current | **v3.0.1 released 2026-06-25** (162pp); built on the latest platform (incl. the 06-25 ✓/✗/θ glyph fallback) |
| `p2-streamer-programming-guide` | ✅ current | **v1.0.3 released 2026-07-03** (75pp); Wave-3 designer-authoritative additions + cross-ref filter adopted; built on the latest platform; release-gate audited, 0 missing chars, outline verified complete |
| `p2-single-step-debugger-manual` | ⏳ behind 06-12 | regression rebuild 06-10; predates the 06-12 platform edit |
| `p2-io-and-smart-pins-user-guide` | ✅ current | **v1.0.0 released 2026-07-03** (396pp); maiden release; built on the latest platform (heading-widow figures.lua fix + cross-ref filter pilot) |
| `p2-layout-torture-test` | ⏳ stale (instrument) | behind several platform files + `diagrams.sty` |

**Maintenance discipline (must be honored or the ledger lies):** `prepare-manual`
appends/updates a `PUBLISH` line when a generation is confirmed clean; any edit to a
`platform/` file appends/updates a `PLATFORM` line. (Wiring this into those skills so
it is automatic — rather than hand-maintained — is an open follow-up.)
