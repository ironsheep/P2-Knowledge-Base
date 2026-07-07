# Publication Roster

Tracks every **manual-shaped** publication and document instrument in
`engineering/document-production/`, **by lifecycle status** — shipped work reads at
the top, abandoned work last:

**Done** (shipped) → **In progress** (actively being built) → **Upcoming** (planned,
not started) → **Abandoned** (retired, last).

Within each status, the **Type** column groups the three kinds of document —
**manual · app-note · guide · instrument**. Every tracked document keeps its
**checkbox gate row** (Draft · Assets · Platform · Chip · Comm · Released), so you can
still scan any gate down a column.

Two properties the layout preserves: **consistency scope** — the released + in-progress
technical manuals on the shared platform stack (see **Shared conventions** below) must
stay mutually consistent — and **how skills resume work** (`whats-next` reads a
document's status + type to decide resume-vs-revive-vs-new: Done/In-progress → resume,
Upcoming → resume-or-add-new, Abandoned → confirm-revive, instrument → resume into its
effort).

**Invariant:** every `workspace|manuals|outbound/<name>` manual folder — and every
`app-notes/<P2ANxxx>/` note in production — appears in exactly **one** status section
below. A folder with no entry is an **anomaly to reconcile** (classify it), not a silent guess.

*Established 2026-05-28. **Restructured 2026-07-05** from category-first
(live/parked/instrument/orphaned) to **status-first** (done/in-progress/upcoming/abandoned)
with a Type column, so shipped work is on top and every tracked document keeps its checkbox
gate row.*

---

## Done — shipped (and the state each is in)

The released set. The technical manuals here (all on the shared `p2kb-platform` stack) are the
**consistency-bound live set** — a change to a shared convention in one is a change to all (see
**Shared conventions** below). Every document is one checkbox row; per-document detail follows.

| Document | Type | Ver | Draft | Assets | Platform | Chip | Comm | Released |
|----------|------|-----|:--:|:--:|:--:|:--:|:--:|:--:|
| Getting Started | manual | 1.0.0 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| I/O & Smart Pins | manual | 1.0.4 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| Assembly Reference | manual | 3.1.2 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| DeSilva Tutorial | manual | 3.0.2 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| Debug Window | manual | 1.0.2 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| Streamer Guide | manual | 1.0.5 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| P2AN001 — ADC Instrumentation | app-note | 1.0.1 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN002 — CORDIC for Real Work | app-note | 1.0.0 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN003 — DAC & Signal Generation | app-note | 1.0.0 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN004 — Freq / Period / Pulse | app-note | 1.0.0 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN005 — Cooperative Multitasking / TASK (C1) | app-note | 1.0.0 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN006 — Sizing Cog & Task Stacks (C3) | app-note | 1.0.0 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| AI Privacy Guide | guide | — | ✅ | ✅ | — | ✅ | ✅ | ✅ |

Legend: ✅ done · 🔄 in progress · ⏳ awaiting · — n/a · _(blank)_ not yet reached. `Chip`/`Comm`
review are **independent** gates (a manual can be released with chip review still outstanding — see
Assembly/DeSilva). `Platform` ✅ = on the shared `p2kb-platform` stack (`—` = a class that doesn't
ride it, e.g. the presentation-class AI Privacy Guide). App notes carry no separate chip-review gate
(`—`) and ship a YAML companion + example ZIP (the four-artifact model — see `app-notes/README.md`).

### Detail

Each document's slug is its folder name across `manuals/<slug>/`, `workspace/<slug>/`,
`outbound/<slug>/` (app notes: `app-notes/<P2ANxxx>/`, companion YAML under `deliverables/ai/P2/`).

**Getting Started with the Propeller 2** · `p2-getting-started-guide` · manual
**v1.0.0 (2026-06-24)** — initial community-review release. The orientation on-ramp, split 2026-06-24 from the P2 Architect's Guide first draft (orientation Chs 1–3 "Meet the Propeller 2" / "Reading P2 Code" / "Putting It to Work" + Where-to-Next); born on the shared platform stack with `p2kb-getting-started-*` locals; release-gate audited (drain GREEN) + finalized; 25pp. Links out to the reference manuals + the Architect's Guide. chip review outstanding.

**P2 I/O & Smart Pins User Guide** · `p2-io-and-smart-pins-user-guide` · manual
**v1.0.4 released 2026-07-07** (396pp, Community Review Edition) — correction wave: ADC input-mode windows measured on real P2 (F-202/EF-024, gain modes center on ~VIO/2), ch02 ~17Ω fast-drive + ch18 9-16 hub-access datasheet fixes, five unsourced specifics softened to qualitative guidance (§7.5 clock, §10.9 DAC min-load, §12.10 input buffer, §16.8 impedance/abs-error), example-heading de-inflation. Prior **v1.0.3 (2026-07-06)** — ADC resolution tables (Ch.16 §16.3 + App D) read in nominal bits; ENOB presented as the measured, hardware-characterized figure (F-201, matches KB v1.14.2). Prior v1.0.2 (2026-07-05): Ch.13 P_STATE_TICKS state-timing examples single-read (state in bit 31, count in low bits; F-195, matches KB v1.14.1). Prior v1.0.1 (2026-07-04): Ch.5 SETQ-armed event-wait timeout (F-193/EF-020) + Ch.15 concurrent A+B input routing (F-192/EF-017). Maiden release v1.0.0 (2026-07-03): 19 chapters covering all 32 smart-pin modes + Appendices A-G + 15-program example ZIP. Terminal step of the IOSP Release Campaign (folded in the USB study + P2AN003 DAC + P2AN004 Freq/Period/Pulse boundary-enrichment). Release-gate audited: 5 HIGH + ~12 MED + ~14 LOW resolved via document-finalize; drain gate GREEN (F-191 shipped in KB v1.13.3); cross-ref filter PILOT (adopted + visually audited); render-verified (compile-clean, 0 heading widows, Appendix A links 42->0, full outline). Chip-review expert-queue items parked (external). "Blue Book" reference.

**P2 Assembly Language Reference** · `p2-assembly-language-manual` · manual
**v3.1.2 (2026-07-04)** — F-193 patch: event-wait instructions (WAITSE1-4, WAITCT1-3, WAITPAT, WAITATN, WAITxxx family) document the SETQ-armed timeout (EF-020, HW-verified); 505pp, render-verified. Prior v3.1.1 (2026-06-29): Ch.1 execution-model refinements + §2.8.3 Operation:-line guidance. chip review outstanding.

**DeSilva PASM2 Tutorial** · `p2-pasm-desilva-style` · manual
**v3.0.2 released 2026-07-07** (163pp) — correction wave: three event-table encodings match silicon (SETSE %000 = LUT read/write & hub-lock event, EVENT_INT %0000, EVENT_QMT %1111) + dedicated-cog servo example rename. Prior **v3.0.1 (2026-06-25)** — accuracy re-audit (every PASM2/Spin2 example compile-checked with `pnut-ts` against the current compiler), typography refresh on the shared platform stack (Plex, no line-number gutter, 8.5pt code boxes; ✓/✗/θ glyph fallbacks), lowercase house-style sweep, and a companion example-library ZIP (first-blink, multicog-blink, hub-counters). **Resolves both prior DEFERRALS:** the Cog-Anatomy diagram is repaired ("Each Cog Contains:") and the full pnut-ts compile-cert is done. Regenerated clean (162pp; 172→162 from the denser typography, outline verified complete). Release-gate audit: local `audit/release-gate-2026-06-25.md`. Prior **v3.0.0 (2026-06-10)** absorbed the ~33-error content re-audit + Ch2 egg-beater fix. chip review outstanding.

**P2 Debug Window Manual** · `p2-debug-window-manual` · manual
**v1.0.2 released 2026-07-07** (160pp) — correction wave: TEXTSTYLE align/weight + TERM TEXTSIZE default aligned to Spin2 v55, ch14 shared-lock number + throughput figure softened (156→160pp = benign platform reflow, first rebuild absorbing the 07-02 heading-widow fix + 07-07 mnemonic-"ones" fix; word-count unchanged confirms no content change). Prior **v1.0.1 (2026-06-26)** — accuracy + typography refresh: DEBUG-output quoting examples corrected data-set-wide, FFT/run-up worked programs fixed, per-window details tightened (trigger offsets, defaults/ranges, PLOT polar, ALT, MIDI), IBM Plex typography (156pp); 32-demo example library refreshed (source ZIP). Prior **v1.0.0 (2026-06-16)** initial community-review release.

**P2 Streamer Programming Guide** · `p2-streamer-programming-guide` · manual
**v1.0.5 released 2026-07-07** (75pp) — correction wave: §12.2 sub-pin selection documents the silicon's per-pin-count field widths (1-pin uses D[19:17], 2-pin D[19:18]+DAC-config bit, 4-pin D[19]+DAC-config bits; higher pins via the group field D[22:20]). Prior **v1.0.4 (2026-07-04)** community-review edition — forum-provenance patch (HDMI-audio blanking budget sourced to the HDMI data-island spec §15.2 · DVI/HDMI blanking floors framed as display-specific observations · SINC2 measurement-period bound reframed §10.4); render-verified 75pp = prior, 0 glyph drops; `audit/forum-provenance-audit-2026-07-04.md`. Prior v1.0.3 (2026-07-03) Wave-3 designer-authoritative additions + cross-ref filter (82 links/0 dead). chip review outstanding.

**P2AN001 — Single-Pin ADC Instrumentation** · `P2AN001` · app-note
**v1.0.1 (2026-07-03, 20pp)** — foundational first note + doc-class & companion-schema exemplar (Family A0); techniques-catalog on the enriched IOSP Ch.16. v1.0.1 = editorial compile-status wording patch.

**P2AN002 — CORDIC for Real Work** · `P2AN002` · app-note
**v1.0.0 (2026-07-03, 14pp)** — lead of the Math family (B1); techniques-catalog (6 recipes + FOC/Park ceiling, OBEX #2811).

**P2AN003 — DAC & Analog Signal Generation** · `P2AN003` · app-note
**v1.0.0 (2026-07-03, 19pp)** — Family A1 (output sibling to ADC); shared dithered-DAC output stage + 5 recipes (sample playback, waveform synthesis, dithering, ADC→DAC passthrough, mixing & panning) + reSound 32-stream ceiling (OBEX #2861). Deep audit (4-agent fan-out + hand-verify) caught + fixed a HIGH Recipe-4 scaling bug pre-release. Cites IOSP Ch.10/§18.3.

**P2AN004 — Frequency / Period / Pulse Measurement** · `P2AN004` · app-note
**v1.0.0 (2026-07-03, 14pp)** — Family A2 (timing instrumentation); 3 recipes (RC-decay reader, TSL235R light-to-frequency reciprocal counter, quadrature-knob). First app note with rendered circuit/timing diagrams (new shared `p2kb-appnote-diagrams` library — circuitikz). Cites IOSP Ch.13-15.

**P2AN005 — Cooperative Multitasking with Spin2 TASK Methods** · `P2AN005` · app-note
**v1.0.0 (2026-07-07, 12pp)** — Family C1 (Concurrency & New Language Features); techniques-catalog: the `{Spin2_v47}` TASK\* family through 4 recipes (two-task round-robin, cooperative yield, halt/resume flow, task dashboard). `TASKWAIT` compile-probed + excluded (F-196); cog-local task IDs hardware-verified (EF-023, KB v1.14.2). Companion to P2AN006. First render on the mnemonic-"ones" platform fix.

**P2AN006 — Sizing Cog & Task Stacks** · `P2AN006` · app-note
**v1.0.0 (2026-07-07, 12pp)** — Family C3 (companion to C1); techniques-catalog: sizing `cogspin`/`TASKSPIN` stack buffers (silent overflow → corruption) through 4 recipes built around the MIT-licensed `isp_stack_check` sentinel-fill utility (Stephen M. Moraco, in the example library). All `pnut_ts -d`-clean.

**AI Privacy Guide** · `ai-privacy-guide` · guide
Released; both reviews complete; presentation-class (rides pristine `p2kb-foundation.sty`).

## In progress — actively being built

Not part of the live consistency set until released; free to evolve independently, reconciled
against the shared conventions at promotion. (`P2 Layout Torture Test` is an **instrument** — a
tool serving an effort, never released — carried here while it's actively used.)

| Document | Type | Ver | Draft | Assets | Platform | Chip | Comm | Released |
|----------|------|-----|:--:|:--:|:--:|:--:|:--:|:--:|
| Architect's Guide | manual | v0.2.0 draft | ✅ | ⏳ | ✅ | | | |
| XBYTE Guide | manual | v0.1.0 draft | ✅ | ⏳ | ✅ | | | |
| Single-Step Debugger | manual | draft | ✅ | ✅ | ✅ | ⏳ | ⏳ | |
| P2AN007 — Data Structures, in-cog + cross-cog (C2) | app-note | v0.1.0 draft | ✅ | ✅ | ⏳ | | | |
| P2 Layout Torture Test | instrument | — | ✅ | ✅ | ✅ | — | — | — |

### Detail

**The P2 Architect's Guide** (design book) · `p2-architect-guide` · manual
**in development — v0.2.0 draft; SPLIT completed (2026-06-24).** The v0.1.0 first draft (4 ch, 48pp, born on the unified `p2kb-platform-*` stack) was divided into two books after a walkthrough review (`manuals/p2-architect-guide/audit/walkthrough-feedback-2026-06-24.md`). **This folder retains the design / realization book** — *The P2 Architect's Guide — Designing Real Systems on the Propeller 2* — keeping Ch4 (functional decomposition) + a new front-end (peripherals → buses → pin budget) + a realization / AI-assist pillar. Orientation Chs 1–3 split out to **Getting Started** (now released v1.0.0, in Done). v0.2.0 draft PDF staged for review.

**P2 XBYTE Programming Guide** · `p2-xbyte-programming-guide` · manual
**in development — STOOD UP 2026-06-26, v0.1.0 first-draft authored.** New manual modeled on the Streamer guide (layout/richness/two-register voice), twin on the shared `p2kb-platform-*` stack. Teaches the XBYTE hardware bytecode engine + the skip family (SKIP/SKIPF/EXECF) + FIFO/LUT dispatch, then builds a minimal custom VM and a tiny illustrative **6502** emulator (+ a 6809 SETQ2 vignette). **Scope narrowed with Stephen (PLANNING.md §0):** external P2 projects (Arc8de, Yume suite) → **Appendix C links only**, not narrative; "systems similar to the P2" (IBM Series/1 EDL anchor, Transputer/Occam, XMOS, GreenArrays, Cell SPE) **DEFERRED** out of this edition. Full triad stood up (creation-/voice-guide, MANUAL-DESCRIPTOR, CHANGELOG, opus-master, grounding digest) + workspace wiring. NEXT: prepare-manual → Stephen generates the v0.1.0 review PDF on the Forge. Subtitle "Building Interpreters and Emulators on the Propeller 2".

**P2 Single-Step Debugger Manual** · `p2-single-step-debugger-manual` · manual
On shared platform stack (foundation/content/diagrams); awaiting chip + community review.

**P2AN007 — Data Structures with the New Language Facilities** · `P2AN007` · app-note
**stood up + drafted 2026-07-06, v0.1.0.** Family **C2**. Techniques-catalog: the Spin2 `{Spin2_v45}` STRUCT facility + worked cross-cog sharing through 4 recipes — in-cog record/array, lock-free SPSC ring buffer, latest-wins mailbox, locked multi-writer queue (real P2 `LOCKNEW/LOCKTRY/LOCKREL`, never P1 `lockset/lockclr`). Implementation-only; the *contract decision* (which structure, why) is cited to the Architect's Guide. All `pnut_ts -d`-clean. NEXT: prepare-manual → Forge v0.1.0 review PDF.

**P2 Layout Torture Test** · `p2-layout-torture-test` · instrument
Test / standards harness — manual-shaped (full folder triad, generates PDFs) but **never released**; serves the manual layout-standards effort (`methodology/manual-layout-standards-*`), not the community. Not consistency-bound. **Its analysis IS its product** — its `audit/` is git-tracked alongside its cases (the `.gitignore` exception), so the instrument, its analysis, and the fixes it drives version together. Resume into the effort it serves.

## Upcoming — planned, not yet started

Manuals and app notes we intend to build. **App-note candidates — full rationale, examples-to-mine,
and production sequence — live in the planning register**
[`analysis/p2-app-note-roster.md`](../analysis/p2-app-note-roster.md); the rows here are that
pipeline at a glance (blank gates = not started).

| Document | Type | Ver | Draft | Assets | Platform | Chip | Comm | Released |
|----------|------|-----|:--:|:--:|:--:|:--:|:--:|:--:|
| Spin2 Reference Manual | manual | — | | | | | | |
| Extended-Precision Integer Math (B2) | app-note | — | | | | | | |
| Fixed-Point Math (B3) | app-note | — | | | | | | |
| USB Device/Host, standalone | app-note | — | | | | | | |

### Detail

**Spin2 Reference Manual** · `spin2-reference-manual` · manual — parked; may go forward.

**App-note candidates** (full detail + production sequence → the [planning register](../analysis/p2-app-note-roster.md)):
- **B2 · Extended-Precision Integer Math** — 64/96/128-bit composed from carry-chain ADDX/SUBX + `muldiv64` (OBEX #5189).
- **B3 · Fixed-Point Math on the P2** — fractional math with no FPU; recurring P2-specific technique.
- **USB Device/Host (standalone)** — high value, hard; its example-mining ran early as the IOSP Release Campaign's USB study.

*(Family C: C1/C3 — **P2AN005/P2AN006 — released v1.0.0 2026-07-07** (now in Done); C2 — P2AN007 remains In progress.)*

## Abandoned — retired, not carrying forward (last)

Started, then retired by decision — superseded or abandoned. Kept for history; **not** resumed
without an explicit revive decision; never consistency-bound.

| Document | Type | Why retired |
|----------|------|-------------|
| Smart Pins Tutorial ("Green Book") · `p2-smart-pins-tutorial` | manual | superseded by the I/O & Smart Pins User Guide (newer generation) |

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
2026-07-07 20:39  PUBLISH   p2-io-and-smart-pins-user-guide  (v1.0.4, 396pp — correction wave: ADC input-mode windows measured on real P2 (F-202/EF-024), ch02 ~17Ω + ch18 9-16 datasheet fixes, 5 unsourced specifics softened to qualitative guidance (§7.5/§10.9/§12.10/§16.8), example-heading de-inflation; render-verified 396pp = prior, outline complete (5 parts + appendices), edits text-present, compile-clean)
2026-07-07 20:34  PUBLISH   p2-pasm-desilva-style            (v3.0.2, 163pp — correction wave: 3 event-table encodings match silicon (SETSE %000, EVENT_INT %0000, EVENT_QMT %1111) + dedicated-cog servo example rename; render-verified 163pp, Ch1-16 + App A + Index complete, edits text-present, compile-clean)
2026-07-07 20:33  PUBLISH   p2-debug-window-manual           (v1.0.2, 160pp — correction wave: TEXTSTYLE align/weight + TERM TEXTSIZE default aligned to Spin2 v55, ch14 shared-lock/throughput softened; render-verified 156->160pp (+4 = benign platform reflow, first rebuild absorbing the 07-02 heading-widow fix + 07-07 mnemonic-"ones" fix; word-count 47057->47109 confirms no content change), outline complete, compile-clean)
2026-07-07 20:30  PUBLISH   p2-streamer-programming-guide    (v1.0.5, 75pp — correction wave: §12.2 sub-pin selection documents the silicon's per-pin-count field widths (1/2/4-pin DAC-config bits, group-field D[22:20] for higher pins); render-verified 75pp = prior, outline complete, §12.2 text-present, compile-clean)
2026-07-07 00:48  PUBLISH   P2AN006                          (v1.0.0, 12pp — app-note: sizing cog & task stacks techniques-catalog (4 recipes: instrument new-cog stack, high-water mark, pinpoint overflow, size task stack) built around the MIT isp_stack_check utility; render-verified 12pp, all recipes present, compile-clean; first render carrying the mnemonic-"ones" platform fix)
2026-07-07 00:47  PUBLISH   P2AN005                          (v1.0.0, 12pp — app-note: cooperative multitasking with Spin2 TASK methods techniques-catalog (4 recipes: two-task round-robin, cooperative yield, halt/resume flow, task dashboard); TASKWAIT excluded (F-196); render-verified 12pp, all recipes present, compile-clean)
2026-07-07 00:11  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua  (the ambiguous-word "ones" now defaults to English prose, only rendering as the ONES popcount instruction on an explicit "ones instruction/count" signal — replaces a fragile adjective allowlist that leaked "ONES" into prose like "the short ones". Consistent with the and/or/not rules. Benefits every manual; first consumed by P2AN005/P2AN006 v1.0.0.)
2026-07-04 21:42  PUBLISH   p2-assembly-language-manual      (v3.1.2, 505pp — F-193 doc patch: the event-wait instructions (WAITSE1-4, WAITCT1-3, WAITPAT, WAITATN, WAITxxx event family) document the SETQ-armed timeout — a preceding SETQ bounds a single wait on the event OR a CT deadline, C/Z reports which; no-SETQ form clears the flags as a free flag-clear (EF-020, HW-verified). Render-verified: 505pp vs 503 prior (+2, additive), outline complete (Ch.1-6 + Instr A-Z + App A-J), changed sections text-present (p336), compile-clean)
2026-07-03 23:39  PUBLISH   P2AN004                          (v1.0.0, 14pp — app-note #4: frequency/period/pulse measurement techniques-catalog (3 recipes: RC-decay reader, TSL235R light-to-frequency reciprocal counter, quadrature-knob); deep audit 4-agent fan-out + hand-verify (0 code defects); first app note with 3 rendered circuit/timing diagrams via a NEW shared app-note diagram library (circuitikz); render-verified, 0 missing chars, no empty ToC, all recipes present)
2026-07-03 20:08  PUBLISH   P2AN003                          (v1.0.0, 19pp — app-note #3: DAC & analog signal generation techniques-catalog (5 recipes + reSound ceiling); deep audit caught+fixed a HIGH Recipe-4 scaling bug (SINC2 differential already 16-bit); render-verified, 0 missing chars, no empty ToC, all recipes present)
2026-07-03 19:30  PUBLISH   P2AN001                          (v1.0.1, 20pp — editorial patch: compile-status wording corrected to be clock-independent; content otherwise identical to v1.0.0; render-verified, 0 missing chars, no empty ToC, all recipes present)
2026-07-03 18:53  PUBLISH   P2AN002                          (v1.0.0, 14pp — app-note #2: CORDIC techniques-catalog (6 recipes + FOC ceiling); app-note-class templates over the shared platform; render-verified, 0 missing chars, no empty ToC, all recipes present)
2026-07-02 22:51  PLATFORM  filters/p2kb-platform-figures.lua         (emit_reserve(): a keep-together \needspace reserved before a lead-in+box/table pair now goes BEFORE a preceding heading, so the heading migrates with its unit instead of widowing — the real fix for the heading-at-page-bottom class. Benefits every manual; IOSP proved 11->0 widows.)
2026-07-02 22:51  PLATFORM  filters/p2kb-platform-crossref.lua        (Table cell-walker: links "Chapter N"/§ refs inside table cells when crossref runs BEFORE the tables filter — IOSP Quick-Mode-Matrix piloting; harmless no-op otherwise. Adopting manuals must list crossref before tables in request.json.)
2026-07-02 22:51  PLATFORM  templates/p2kb-platform-foundation.sty    (heading keep-with-next: \needspace on \section only (removed from subsection — it stranded sections) + Shaded code-box bound to its lead-in with \nobreak; completes the widow fix with figures.lua.)
2026-07-02 06:07  PLATFORM  filters/p2kb-platform-pagination.lua      (escape LaTeX specials & % $ # _ in the \chaptersubtitle{} argument — a raw & in an em-dash chapter subtitle (IOSP Ch.15 "Periods, Duty & Reciprocal Counting") reached xelatex unescaped and aborted the build. Benefits every manual using em-dash chapter subtitles.)
2026-07-02 06:07  PLATFORM  filters/p2kb-platform-crossref.lua        (F4: add "Ch" as a Form-A keyword so "Ch N" table-cell refs auto-link alongside "Chapter"; IOSP Quick-Mode-Matrix piloting.)
2026-07-02 06:07  PLATFORM  templates/p2kb-platform-foundation.sty    (F7: \needspace keep-with-next on section/subsection/subsubsection star-form titleformats so a heading cannot widow at page bottom — fixes IOSP §9.3.)
2026-07-02 06:07  PLATFORM  templates/p2kb-platform-content.sty       (F10: ModeBlock top rule "borderline north" 4pt->1.5pt — thins the Appendix-F mode-card corner marker's horizontal stroke; vertical west stays 4pt.)
2026-06-29 19:00  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (v3.0 STYLE POLICY: prose mnemonics now render UPPERCASE, NOT bold — uppercase carries the token's identity and matches its code appearance; bold is reserved for genuine emphasis. Also ends the uneven-bold bug where punctuation-adjacent mnemonics ("(ALTS", "RDFAST/WRFAST") bolded only partially. AUTOMATIC for EVERY manual on its NEXT render — a visible prose-style change, but NOT a forced re-release. First absorbed by Assembly Language Reference v3.1.1.)
2026-06-26 18:15  PLATFORM  filters/p2kb-platform-crossref.lua        (NEW: auto-links "Chapter N"/"Appendix X"/"Section N.N"/"§N.N" prose refs to anchors; opt-in per request.json, IOSP piloting. OTHER MANUALS: adopt + visual-audit on NEXT release — NOT a forced release; tracker: CROSSREF-FILTER-ADOPTION.md)
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

Freshness = is the manual's PDF built on the current `platform/` stack? (Release history
lives in the Live-section detail above — not repeated here.)

| Manual | Ver | Freshness | Why |
|--------|-----|:--:|-----|
| `p2-debug-window-manual` | 1.0.2 | ✅ current | rebuilt 07-07 on latest platform (absorbed 07-02 widow fix + 07-07 mnemonic-"ones") |
| `p2-assembly-language-manual` | 3.1.2 | ✅ current | first to render the uppercase-mnemonic filter |
| `p2-pasm-desilva-style` | 3.0.2 | ✅ current | rebuilt 07-07 on latest platform |
| `p2-streamer-programming-guide` | 1.0.5 | ✅ current | rebuilt 07-07 on latest platform (carried the mnemonic-"ones" seed) |
| `p2-single-step-debugger-manual` | draft | ⏳ behind 06-12 | regression rebuild 06-10; predates the 06-12 edit |
| `p2-io-and-smart-pins-user-guide` | 1.0.4 | ✅ current | rebuilt 07-07 on latest platform (cross-ref filter pilot) |
| `p2-layout-torture-test` | — | ⏳ stale (instrument) | behind several platform files + `diagrams.sty` |

**Pending platform change — 2026-07-07 (`mnemonic-bold.lua` "ones" fix):** every live
manual consumes `p2kb-platform-mnemonic-bold.lua` (the lone exception is the retired
Smart Pins Tutorial, on its own `p2kb-sp-` fork), so by the detector's rule each sits
below this `PLATFORM` line until its next render. The fix is **cosmetic** — it only
changes how a bare "<adjective> ones" reads in prose (e.g. "the short ones") — so **no
forced re-render is scheduled**; each manual **picks it up automatically on its next
natural release**, and is marked current then. **P2AN005 / P2AN006 v1.0.0 carried it
first; the 2026-07-07 correction wave (Streamer v1.0.5, Debug v1.0.2, deSilva v3.0.2,
IOSP v1.0.4) has since absorbed it.** Still pending on the manuals that haven't rebuilt
since (Getting Started, Assembly, the P2AN001-004 notes, single-step, torture-test). The
rows above stay ✅ for the substantive platform stack; this is the one pending cosmetic
delta, tracked here so it isn't lost.

**Maintenance discipline (must be honored or the ledger lies):** `prepare-manual`
appends/updates a `PUBLISH` line when a generation is confirmed clean; any edit to a
`platform/` file appends/updates a `PLATFORM` line. (Wiring this into those skills so
it is automatic — rather than hand-maintained — is an open follow-up.)
