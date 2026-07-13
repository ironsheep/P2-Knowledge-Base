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
| Getting Started | manual | 1.0.1 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| I/O & Smart Pins | manual | 1.0.5 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| Assembly Reference | manual | 3.1.3 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| DeSilva Tutorial | manual | 3.0.3 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| Debug Window | manual | 1.0.2 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| Streamer Guide | manual | 1.0.6 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| Architect's Guide | manual | 1.0.1 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| P2AN001 — ADC Instrumentation | app-note | 1.0.2 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN002 — CORDIC for Real Work | app-note | 1.0.1 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN003 — DAC & Signal Generation | app-note | 1.0.1 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN004 — Freq / Rotation / RC-Timing | app-note | 1.0.1 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN005 — Cooperative Multitasking / TASK (C1) | app-note | 1.0.1 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
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
**v1.0.1 released 2026-07-12** (25pp) — accuracy refinement: most register-to-register PASM2 instructions execute in two clocks, while branches and hub accesses take more.
Prior **v1.0.0 (2026-06-24)** — initial community-review release. The orientation on-ramp, split 2026-06-24 from the P2 Architect's Guide first draft (orientation Chs 1–3 "Meet the Propeller 2" / "Reading P2 Code" / "Putting It to Work" + Where-to-Next); born on the shared platform stack with `p2kb-getting-started-*` locals; release-gate audited (drain GREEN) + finalized; 25pp. Links out to the reference manuals + the Architect's Guide. chip review outstanding.

**P2 I/O & Smart Pins User Guide** · `p2-io-and-smart-pins-user-guide` · manual
**v1.0.5 released 2026-07-12** (398pp) — hardware-grounded accuracy pass: smart-pin and pin behavior documented as measured on real P2 silicon, every worked example runs as written and matches its in-text listing line-for-line, and instruction/pin timings, bit-field encodings, and value ranges read per the datasheet and Silicon Doc.
Prior **v1.0.4 released 2026-07-07** (396pp, Community Review Edition) — correction wave: ADC input-mode windows measured on real P2 (F-202/EF-024, gain modes center on ~VIO/2), ch02 ~17Ω fast-drive + ch18 9-16 hub-access datasheet fixes, five unsourced specifics softened to qualitative guidance (§7.5 clock, §10.9 DAC min-load, §12.10 input buffer, §16.8 impedance/abs-error), example-heading de-inflation. Prior **v1.0.3 (2026-07-06)** — ADC resolution tables (Ch.16 §16.3 + App D) read in nominal bits; ENOB presented as the measured, hardware-characterized figure (F-201, matches KB v1.14.2). Prior v1.0.2 (2026-07-05): Ch.13 P_STATE_TICKS state-timing examples single-read (state in bit 31, count in low bits; F-195, matches KB v1.14.1). Prior v1.0.1 (2026-07-04): Ch.5 SETQ-armed event-wait timeout (F-193/EF-020) + Ch.15 concurrent A+B input routing (F-192/EF-017). Maiden release v1.0.0 (2026-07-03): 19 chapters covering all 32 smart-pin modes + Appendices A-G + 15-program example ZIP. Terminal step of the IOSP Release Campaign (folded in the USB study + P2AN003 DAC + P2AN004 Freq/Period/Pulse boundary-enrichment). Release-gate audited: 5 HIGH + ~12 MED + ~14 LOW resolved via document-finalize; drain gate GREEN (F-191 shipped in KB v1.13.3); cross-ref filter PILOT (adopted + visually audited); render-verified (compile-clean, 0 heading widows, Appendix A links 42->0, full outline). Chip-review expert-queue items parked (external). "Blue Book" reference.

**P2 Assembly Language Reference** · `p2-assembly-language-manual` · manual
**v3.1.3 released 2026-07-12** (505pp) — silicon- and hardware-grounded accuracy pass: instruction semantics, flag effects, and timing verified against the P2 documentation and real-hardware measurement — the AUGS/AUGD augment survives intervening instructions before its immediate; TEST, interrupt-priority, COGINIT, and QEXP semantics read as the silicon defines; and a GETCT-pair bracket carries a fixed 2-clock overhead, hardware-confirmed on real P2.
Prior **v3.1.2 (2026-07-04)** — F-193 patch: event-wait instructions (WAITSE1-4, WAITCT1-3, WAITPAT, WAITATN, WAITxxx family) document the SETQ-armed timeout (EF-020, HW-verified); 505pp, render-verified. Prior v3.1.1 (2026-06-29): Ch.1 execution-model refinements + §2.8.3 Operation:-line guidance. chip review outstanding.

**DeSilva PASM2 Tutorial** · `p2-pasm-desilva-style` · manual
**v3.0.3 released 2026-07-12** (164pp) — technical-accuracy pass: PASM2 semantics and timing read as the silicon defines (the CORDIC is one solver the cogs share through hub slots, `MUL` is a 16×16→32 multiply, RCFAST runs a nominal ~24 MHz), and the `TESTP` WZ pin-state and async-serial `P_OE`-drive worked examples now behave as the text describes.
Prior **v3.0.2 released 2026-07-07** (163pp) — correction wave: three event-table encodings match silicon (SETSE %000 = LUT read/write & hub-lock event, EVENT_INT %0000, EVENT_QMT %1111) + dedicated-cog servo example rename. Prior **v3.0.1 (2026-06-25)** — accuracy re-audit (every PASM2/Spin2 example compile-checked with `pnut-ts` against the current compiler), typography refresh on the shared platform stack (Plex, no line-number gutter, 8.5pt code boxes; ✓/✗/θ glyph fallbacks), lowercase house-style sweep, and a companion example-library ZIP (first-blink, multicog-blink, hub-counters). **Resolves both prior DEFERRALS:** the Cog-Anatomy diagram is repaired ("Each Cog Contains:") and the full pnut-ts compile-cert is done. Regenerated clean (162pp; 172→162 from the denser typography, outline verified complete). Release-gate audit: local `audit/release-gate-2026-06-25.md`. Prior **v3.0.0 (2026-06-10)** absorbed the ~33-error content re-audit + Ch2 egg-beater fix. chip review outstanding.

**P2 Debug Window Manual** · `p2-debug-window-manual` · manual
**v1.0.2 released 2026-07-07** (160pp) — correction wave: TEXTSTYLE align/weight + TERM TEXTSIZE default aligned to Spin2 v55, ch14 shared-lock number + throughput figure softened (156→160pp = benign platform reflow, first rebuild absorbing the 07-02 heading-widow fix + 07-07 mnemonic-"ones" fix; word-count unchanged confirms no content change). Prior **v1.0.1 (2026-06-26)** — accuracy + typography refresh: DEBUG-output quoting examples corrected data-set-wide, FFT/run-up worked programs fixed, per-window details tightened (trigger offsets, defaults/ranges, PLOT polar, ALT, MIDI), IBM Plex typography (156pp); 32-demo example library refreshed (source ZIP). Prior **v1.0.0 (2026-06-16)** initial community-review release.

**P2 Streamer Programming Guide** · `p2-streamer-programming-guide` · manual
**v1.0.6 released 2026-07-12** (75pp) — Silicon-Doc accuracy pass: the NCO phase accumulator resolves to sysclk/2^31 (essentially exact at any sysclk), the VGA field-timing, DAC-routed RGB, and SPI-clock worked examples drive correct signals, the FIFO wrap-mode buffer start is long-aligned, and the Appendix-A RFBYTE mode encodings read per the Silicon Doc.
Prior **v1.0.5 released 2026-07-07** (75pp) — correction wave: §12.2 sub-pin selection documents the silicon's per-pin-count field widths (1-pin uses D[19:17], 2-pin D[19:18]+DAC-config bit, 4-pin D[19]+DAC-config bits; higher pins via the group field D[22:20]). Prior **v1.0.4 (2026-07-04)** community-review edition — forum-provenance patch (HDMI-audio blanking budget sourced to the HDMI data-island spec §15.2 · DVI/HDMI blanking floors framed as display-specific observations · SINC2 measurement-period bound reframed §10.4); render-verified 75pp = prior, 0 glyph drops; `audit/forum-provenance-audit-2026-07-04.md`. Prior v1.0.3 (2026-07-03) Wave-3 designer-authoritative additions + cross-ref filter (82 links/0 dead). chip review outstanding.

**The P2 Architect's Guide** · `p2-architect-guide` · manual
**v1.0.1 released 2026-07-12** (53pp) — accuracy refinement: PSRAM is named as an external resource, distinct from the P2's on-chip LUT RAM, CORDIC, and streamer.
Prior **v1.0.0 released 2026-07-08** (53pp) — MAIDEN release. The design/realization companion to the reference manuals (*Getting Started* is the prerequisite): a three-act narrative — get a real project off the ground (Part I, distilled from 12 real projects), *derive* its architecture from physical forces (Part II, the functional-decomposition method + two worked derivations, robot dog + streaming pipeline), then walk the whole process again with an AI agent (Part III, synthesized from the same 12 projects). Teaches a method, not a catalogue. 4 TikZ figures; ships **no example ZIP** (0 embedded code — orphaned examples-library archived). Render-verified 53pp, full TOC (Parts I-III + In Closing + appendices), 0 LaTeX errors, compile-clean. chip review outstanding.

**P2AN001 — Single-Pin ADC Instrumentation** · `P2AN001` · app-note
**v1.0.2 released 2026-07-12** (20pp) — technical-precision pass on the ADC recipes: the P2 powers its I/O in eight groups of eight sharing one VIO/GIO pair (a multi-pin shared-node measurement stays within a single group), SINC2 filtering accepts any sample period (not only powers of two), and the below-ground self-check reads build-dependent.
Prior **v1.0.1 (2026-07-03, 20pp)** — foundational first note + doc-class & companion-schema exemplar (Family A0); techniques-catalog on the enriched IOSP Ch.16. v1.0.1 = editorial compile-status wording patch.

**P2AN002 — CORDIC for Real Work** · `P2AN002` · app-note
**v1.0.1 released 2026-07-12** (14pp) — derivation and attribution refinement: the circle-layout step-size uses the halved `$8000_0000 / (STEPS / 2)` form to stay within 32 bits, and the OBEX Resources match the catalog (#2812 ersmith, #5361 James Smith).
Prior **v1.0.0 (2026-07-03, 14pp)** — lead of the Math family (B1); techniques-catalog (6 recipes + FOC/Park ceiling, OBEX #2811).

**P2AN003 — DAC & Analog Signal Generation** · `P2AN003` · app-note
**v1.0.1 released 2026-07-12** (19pp) — DAC precision refinement: the PWM-dither spectral component sits at a fixed sysclock/256, independent of the sample period.
Prior **v1.0.0 (2026-07-03, 19pp)** — Family A1 (output sibling to ADC); shared dithered-DAC output stage + 5 recipes (sample playback, waveform synthesis, dithering, ADC→DAC passthrough, mixing & panning) + reSound 32-stream ceiling (OBEX #2861). Deep audit (4-agent fan-out + hand-verify) caught + fixed a HIGH Recipe-4 scaling bug pre-release. Cites IOSP Ch.10/§18.3.

**P2AN004 — Frequency / Rotation / RC-Timing Measurement** · `P2AN004` · app-note
**v1.0.1 released 2026-07-12** (14pp) — specification-accuracy and titling refinement (retitled Frequency / Rotation / RC-Timing Measurement): the programs run at 200 MHz (top of the PLL VCO's 100–200 MHz range) and `P_FILT1_AB` routes the A/B inputs through the global FILT1 ~600 ns low-pass filter.
Prior **v1.0.0 (2026-07-03, 14pp)** — Family A2 (timing instrumentation); 3 recipes (RC-decay reader, TSL235R light-to-frequency reciprocal counter, quadrature-knob). First app note with rendered circuit/timing diagrams (new shared `p2kb-appnote-diagrams` library — circuitikz). Cites IOSP Ch.13-15.

**P2AN005 — Cooperative Multitasking with Spin2 TASK Methods** · `P2AN005` · app-note
**v1.0.1 released 2026-07-12** (12pp) — wording refinement: keeping a shared bus inside its single owning cog lets cooperative tasks service devices at different cadences while the bus stays coherent, sidestepping cross-cog lock coordination.
Prior **v1.0.0 (2026-07-07, 12pp)** — Family C1 (Concurrency & New Language Features); techniques-catalog: the `{Spin2_v47}` TASK\* family through 4 recipes (two-task round-robin, cooperative yield, halt/resume flow, task dashboard). `TASKWAIT` compile-probed + excluded (F-196); cog-local task IDs hardware-verified (EF-023, KB v1.14.2). Companion to P2AN006. First render on the mnemonic-"ones" platform fix.

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
| XBYTE Guide | manual | v0.1.0 draft | ✅ | ⏳ | ✅ | | | |
| Single-Step Debugger | manual | draft | ✅ | ✅ | ✅ | ⏳ | ⏳ | |
| P2AN007 — Data Structures, in-cog + cross-cog (C2) | app-note | v1.0.0 pre-release | ✅ | ✅ | ⏳ | | | |
| P2 Layout Torture Test | instrument | — | ✅ | ✅ | ✅ | — | — | — |

### Detail

**P2 XBYTE Programming Guide** · `p2-xbyte-programming-guide` · manual
**in development — STOOD UP 2026-06-26, v0.1.0 first-draft authored.** New manual modeled on the Streamer guide (layout/richness/two-register voice), twin on the shared `p2kb-platform-*` stack. Teaches the XBYTE hardware bytecode engine + the skip family (SKIP/SKIPF/EXECF) + FIFO/LUT dispatch, then builds a minimal custom VM and a tiny illustrative **6502** emulator (+ a 6809 SETQ2 vignette). **Scope narrowed with Stephen (PLANNING.md §0):** external P2 projects (Arc8de, Yume suite) → **Appendix C links only**, not narrative; "systems similar to the P2" (IBM Series/1 EDL anchor, Transputer/Occam, XMOS, GreenArrays, Cell SPE) **DEFERRED** out of this edition. Full triad stood up (creation-/voice-guide, MANUAL-DESCRIPTOR, CHANGELOG, opus-master, grounding digest) + workspace wiring. NEXT: prepare-manual → Stephen generates the v0.1.0 review PDF on the Forge. Subtitle "Building Interpreters and Emulators on the Propeller 2".

**P2 Single-Step Debugger Manual** · `p2-single-step-debugger-manual` · manual
On shared platform stack (foundation/content/diagrams); awaiting chip + community review.

**P2AN007 — Data Structures with the New Language Facilities** · `P2AN007` · app-note
**drafted 2026-07-06; extended + bumped to v1.0.0 pre-release 2026-07-13.** Family **C2**. Techniques-catalog: the Spin2 `{Spin2_v45}` STRUCT facility + worked cross-cog sharing through **6** recipes — in-cog record/array, lock-free SPSC ring buffer, latest-wins mailbox, locked multi-writer queue (real P2 `LOCKNEW/LOCKTRY/LOCKREL`, never P1 `lockset/lockclr`), plus the two STRUCT facilities added since v45: **R5** member bitfields (`{Spin2_v54}`) packing a whole record into one atomically-published long, and **R6** `OFFSETOF` (`{Spin2_v53}`) for computed offsets under raw addressing. R1–R4 stay `{Spin2_v45}`; the newer floors apply only to the files that use them. **This is the only reader-facing P2 doc covering `OFFSETOF` or struct bitfields** (the Spin2 Reference Manual is parked). Implementation-only; the *contract decision* (which structure, why) is cited to the Architect's Guide. All 6 `pnut_ts -d`-clean. **F-213 fixed here:** v0.1.0's R3 invited dropping the seq/ack handshake, which reintroduces a torn read — replaced with a pitfall + the two safe non-blocking alternatives. NEXT: Stephen runs the 5 hardware-verification rigs (`audit/verification-tests/`) → Claude certifies logs → EF ledger → prepare-manual → Forge v1.0.0 PDF → release.

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
2026-07-12 04:36  PUBLISH   p2-assembly-language-manual      (v3.1.3, 505pp — silicon/hardware-grounded accuracy pass: instruction semantics + flag effects read as the silicon defines (AUGS/AUGD augment surviving intervening instructions, TEST/interrupt-priority/COGINIT/QEXP), GETCT-pair bracketing carries a fixed 2-clock overhead HW-confirmed on real P2; render-verified 505pp, outline complete, compile-clean, no content-drop)
2026-07-12 04:22  PUBLISH   p2-io-and-smart-pins-user-guide  (v1.0.5, 398pp — hardware-grounded accuracy pass: smart-pin & pin behavior documented as measured on real P2, every worked example runs as written and matches its in-text listing line-for-line, quantitative timings/bit-field encodings/ranges aligned to the datasheet + Silicon Doc; example ZIP rebuilt (-src-260712); render-verified 398pp, outline complete, compile-clean, no content-drop)
2026-07-12 04:06  PUBLISH   p2-pasm-desilva-style            (v3.0.3, 164pp — technical-accuracy pass: the CORDIC is one solver the cogs share through hub slots, MUL is a 16×16→32 multiply, RCFAST runs ~24 MHz, TESTP WZ reflects pin state, async-serial transmit drives its P_OE output; example ZIP rebuilt (-src-260712); render-verified 164pp, outline complete, compile-clean, no content-drop)
2026-07-12 04:05  PUBLISH   p2-streamer-programming-guide    (v1.0.6, 75pp — Silicon-Doc accuracy pass: NCO resolves to sysclk/2^31 (essentially exact), VGA field-timing + DAC-routed RGB + SPI clock worked examples corrected, FIFO wrap-mode buffer start is long-aligned, Appendix-A RFBYTE mode encodings read per Silicon Doc; render-verified 75pp, outline complete, compile-clean, no content-drop)
2026-07-12 03:53  PUBLISH   p2-architect-guide               (v1.0.1, 53pp — accuracy refinement: PSRAM named as an external resource, distinct from the P2's on-chip LUT RAM, CORDIC, and streamer; render-verified 53pp, outline complete, compile-clean, no content-drop)
2026-07-12 03:51  PUBLISH   p2-getting-started-guide         (v1.0.1, 25pp — accuracy refinement: most register-to-register PASM2 instructions execute in two clocks, while branches and hub accesses take more; render-verified 25pp, outline complete, compile-clean, no content-drop)
2026-07-12 03:49  PUBLISH   P2AN001                          (v1.0.2, 20pp — technical-precision pass on the ADC recipes: I/O powered in eight groups of eight sharing one VIO/GIO pair (multi-pin shared-node stays in-group), SINC2 filtering accepts any sample period (not only powers of two), below-ground self-check is build-dependent; render-verified 20pp, all recipes present, compile-clean, no content-drop)
2026-07-12 03:48  PUBLISH   P2AN003                          (v1.0.1, 19pp — DAC precision refinement: the PWM-dither spectral component sits at a fixed sysclock/256, independent of the sample period; render-verified 19pp, all recipes present, compile-clean, no content-drop)
2026-07-12 03:48  PUBLISH   P2AN004                          (v1.0.1, 14pp — spec-accuracy + titling refinement (retitled Frequency / Rotation / RC-Timing Measurement): programs run at 200 MHz (top of the PLL VCO 100-200 MHz range), P_FILT1_AB routes A/B through the global FILT1 ~600 ns low-pass; render-verified 14pp, all instruments present, compile-clean, no content-drop)
2026-07-12 03:47  PUBLISH   P2AN002                          (v1.0.1, 14pp — derivation + attribution refinement: circle-layout step-size uses the halved $8000_0000/(STEPS/2) form to stay within 32 bits, OBEX Resources match the catalog (#2812 ersmith, #5361 James Smith); render-verified 14pp, all recipes present, compile-clean, no content-drop)
2026-07-12 03:45  PUBLISH   P2AN005                          (v1.0.1, 12pp — wording refinement: keeping a shared bus inside its single owning cog lets cooperative tasks service devices at different cadences while the bus stays coherent, sidestepping cross-cog lock coordination; render-verified 12pp, all recipes present, compile-clean, no content-drop)
2026-07-07 20:33  PUBLISH   p2-debug-window-manual           (v1.0.2, 160pp — correction wave: TEXTSTYLE align/weight + TERM TEXTSIZE default aligned to Spin2 v55, ch14 shared-lock/throughput softened; render-verified 156->160pp (+4 = benign platform reflow, first rebuild absorbing the 07-02 heading-widow fix + 07-07 mnemonic-"ones" fix; word-count 47057->47109 confirms no content change), outline complete, compile-clean)
2026-07-07 00:48  PUBLISH   P2AN006                          (v1.0.0, 12pp — app-note: sizing cog & task stacks techniques-catalog (4 recipes: instrument new-cog stack, high-water mark, pinpoint overflow, size task stack) built around the MIT isp_stack_check utility; render-verified 12pp, all recipes present, compile-clean; first render carrying the mnemonic-"ones" platform fix)
2026-07-07 00:11  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua  (the ambiguous-word "ones" now defaults to English prose, only rendering as the ONES popcount instruction on an explicit "ones instruction/count" signal — replaces a fragile adjective allowlist that leaked "ONES" into prose like "the short ones". Consistent with the and/or/not rules. Benefits every manual; first consumed by P2AN005/P2AN006 v1.0.0.)
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
2026-06-24 21:01  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua   (AG-01: English-collision handling for call/push/ones/test — daemon-verified on Getting Started; other manuals low-urgency regen)
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
| `p2-assembly-language-manual` | 3.1.3 | ✅ current | rebuilt 07-12 (fleet correction wave) |
| `p2-pasm-desilva-style` | 3.0.3 | ✅ current | rebuilt 07-12 (fleet correction wave) |
| `p2-streamer-programming-guide` | 1.0.6 | ✅ current | rebuilt 07-12 (fleet correction wave) |
| `p2-single-step-debugger-manual` | draft | ⏳ behind 06-12 | regression rebuild 06-10; predates the 06-12 edit |
| `p2-io-and-smart-pins-user-guide` | 1.0.5 | ✅ current | rebuilt 07-12 (fleet correction wave) |
| `p2-layout-torture-test` | — | ⏳ stale (instrument) | behind several platform files + `diagrams.sty` |

**Pending platform change — 2026-07-07 (`mnemonic-bold.lua` "ones" fix):** every live
manual consumes `p2kb-platform-mnemonic-bold.lua` (the lone exception is the retired
Smart Pins Tutorial, on its own `p2kb-sp-` fork), so by the detector's rule each sits
below this `PLATFORM` line until its next render. The fix is **cosmetic** — it only
changes how a bare "<adjective> ones" reads in prose (e.g. "the short ones") — so **no
forced re-render is scheduled**; each manual **picks it up automatically on its next
natural release**, and is marked current then. **P2AN005 / P2AN006 v1.0.0 carried it
first; the 2026-07-07 correction wave (Streamer v1.0.5, Debug v1.0.2, deSilva v3.0.2,
IOSP v1.0.4) has since absorbed it; the 2026-07-12 fleet correction wave then carried it across the
rest of the live set (Assembly v3.1.3, IOSP v1.0.5, deSilva v3.0.3, Streamer v1.0.6,
Architect v1.0.1, Getting Started v1.0.1, P2AN001-005).** Still pending only on the
manuals that haven't rebuilt since (single-step, torture-test). The
rows above stay ✅ for the substantive platform stack; this is the one pending cosmetic
delta, tracked here so it isn't lost.

**Maintenance discipline (must be honored or the ledger lies):** `prepare-manual`
appends/updates a `PUBLISH` line when a generation is confirmed clean; any edit to a
`platform/` file appends/updates a `PLATFORM` line. (Wiring this into those skills so
it is automatic — rather than hand-maintained — is an open follow-up.)
