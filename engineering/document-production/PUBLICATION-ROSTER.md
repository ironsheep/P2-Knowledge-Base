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
| Getting Started | manual | 1.0.3 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| I/O & Smart Pins | manual | 1.0.8 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Assembly Reference | manual | 3.1.5 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| DeSilva Tutorial | manual | 3.0.6 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| Debug Window | manual | 1.1.2 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| Streamer Guide | manual | 1.0.8 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| Architect's Guide | manual | 1.0.3 | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ |
| Interpreters & Emulators (XBYTE) | manual | 1.0.1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| P2AN001 — ADC Instrumentation | app-note | 1.0.4 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN002 — CORDIC for Real Work | app-note | 1.0.3 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN003 — DAC & Signal Generation | app-note | 1.0.2 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN004 — Freq / Rotation / RC-Timing | app-note | 1.0.2 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN005 — Cooperative Multitasking / TASK (C1) | app-note | 1.0.2 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN006 — Sizing Cog & Task Stacks (C3) | app-note | 1.0.1 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| P2AN007 — Data Structures, in-cog + cross-cog (C2) | app-note | 1.0.1 | ✅ | ✅ | ✅ | — | ✅ | ✅ |
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
**v1.0.2 released 2026-07-21** (25pp) — readability pass: a recurring summarizing frame varied for smoother narration; no technical content changed. Render-verified 25pp (= prior), outline complete, compile-clean.
Prior **v1.0.1 released 2026-07-12** (25pp) — accuracy refinement: most register-to-register PASM2 instructions execute in two clocks, while branches and hub accesses take more.
Prior **v1.0.0 (2026-06-24)** — initial community-review release. The orientation on-ramp, split 2026-06-24 from the P2 Architect's Guide first draft (orientation Chs 1–3 "Meet the Propeller 2" / "Reading P2 Code" / "Putting It to Work" + Where-to-Next); born on the shared platform stack with `p2kb-getting-started-*` locals; release-gate audited (drain GREEN) + finalized; 25pp. Links out to the reference manuals + the Architect's Guide. chip review outstanding.

**P2 I/O & Smart Pins User Guide** · `p2-io-and-smart-pins-user-guide` · manual
**v1.0.5 released 2026-07-12** (398pp) — hardware-grounded accuracy pass: smart-pin and pin behavior documented as measured on real P2 silicon, every worked example runs as written and matches its in-text listing line-for-line, and instruction/pin timings, bit-field encodings, and value ranges read per the datasheet and Silicon Doc.
**v1.0.7 released 2026-07-16** (396pp) — Ch.9 §9.1 "Complementary Outputs and Dead-Band" note (twin of KB v1.14.5, F-225): a complementary half-bridge pair is two coordinated Smart Pins (one per side, low side inverted via `P_INVERT_OUTPUT`, dead-band produced in software by offsetting the two duty values) — the P2 has no single-pin complementary/dead-band mode. Chip-confirmed + grounded in `isp_bldc_motor.spin2`. Render-verified: 396pp (= v1.0.6, new note absorbed in reflow not a drop — §9.1 text-present p139 + eyeballed), outline complete, compile-clean. **Chip expert-queue now DRAINED** — the parked dead-band (Q1) + DAC-ENOB (Q5, unmeasured → qualitative caveat only, F-226) items are both resolved, so the Chip gate flips ✅. Prior **v1.0.6 released 2026-07-15** (396pp) — three Silicon-Doc-grounded scope/DAC clarifications (twin of KB v1.14.4): scope-mode filter DC dynamic range ~5–6 bits/filter (ch16 §16.5 + App F, RA-31/Q2 resolved from KB authority), DAC dither fed every clock vs the separate sample-period timer (ch10 §10.4, RA-37), X=0 low-power rationale for DAC noise (ch18 §18.3, RA-17). Render-verified: outline complete, all three callouts present, compile-clean; the −2pp vs v1.0.5 is reflow (content grew +1.6k chars). Prior **v1.0.5 released 2026-07-11** (398pp) — hardware-grounded accuracy pass: smart-pin/pin behavior measured on real P2, examples run-as-written, timings/encodings aligned to datasheet + Silicon Doc. Prior **v1.0.4 released 2026-07-07** (396pp, Community Review Edition) — correction wave: ADC input-mode windows measured on real P2 (F-202/EF-024, gain modes center on ~VIO/2), ch02 ~17Ω fast-drive + ch18 9-16 hub-access datasheet fixes, five unsourced specifics softened to qualitative guidance (§7.5 clock, §10.9 DAC min-load, §12.10 input buffer, §16.8 impedance/abs-error), example-heading de-inflation. Prior **v1.0.3 (2026-07-06)** — ADC resolution tables (Ch.16 §16.3 + App D) read in nominal bits; ENOB presented as the measured, hardware-characterized figure (F-201, matches KB v1.14.2). Prior v1.0.2 (2026-07-05): Ch.13 P_STATE_TICKS state-timing examples single-read (state in bit 31, count in low bits; F-195, matches KB v1.14.1). Prior v1.0.1 (2026-07-04): Ch.5 SETQ-armed event-wait timeout (F-193/EF-020) + Ch.15 concurrent A+B input routing (F-192/EF-017). Maiden release v1.0.0 (2026-07-03): 19 chapters covering all 32 smart-pin modes + Appendices A-G + 15-program example ZIP. Terminal step of the IOSP Release Campaign (folded in the USB study + P2AN003 DAC + P2AN004 Freq/Period/Pulse boundary-enrichment). Release-gate audited: 5 HIGH + ~12 MED + ~14 LOW resolved via document-finalize; drain gate GREEN (F-191 shipped in KB v1.13.3); cross-ref filter PILOT (adopted + visually audited); render-verified (compile-clean, 0 heading widows, Appendix A links 42->0, full outline). Chip-review expert-queue items parked (external). "Blue Book" reference.

**P2 Assembly Language Reference** · `p2-assembly-language-manual` · manual
**v3.1.4 released 2026-07-14** (505pp) — render-only patch: hyphenated compound names print exactly as authored, so the cross-reference to the P2 I/O & Smart Pins User Guide names the guide that actually exists (F-214; zero content change from v3.1.3).

Prior **v3.1.3 (2026-07-12, 505pp)** — silicon- and hardware-grounded accuracy pass: instruction semantics, flag effects, and timing verified against the P2 documentation and real-hardware measurement — the AUGS/AUGD augment survives intervening instructions before its immediate; TEST, interrupt-priority, COGINIT, and QEXP semantics read as the silicon defines; and a GETCT-pair bracket carries a fixed 2-clock overhead, hardware-confirmed on real P2.
Prior **v3.1.2 (2026-07-04)** — F-193 patch: event-wait instructions (WAITSE1-4, WAITCT1-3, WAITPAT, WAITATN, WAITxxx family) document the SETQ-armed timeout (EF-020, HW-verified); 505pp, render-verified. Prior v3.1.1 (2026-06-29): Ch.1 execution-model refinements + §2.8.3 Operation:-line guidance. chip review outstanding.

**DeSilva PASM2 Tutorial** · `p2-pasm-desilva-style` · manual
**v3.0.6 released 2026-08-17** (166pp) — an honest platform comparison and the multi-cog pin hazard: Appendix A gains the RP2350 (Pico 2) with PIO set against a full cog, a software axis (two languages, a smaller ecosystem, a higher cost of entry), and an argument from growth — the eighth job on one processor changes the timing of the seven already there, per-cog it does not. Chapter 16 teaches that DIR and OUT are OR'd across cogs, so two drivers produce a result resembling neither, unreported, with `RQPIN` named as the safe multi-cog pin read. Render-verified 166pp (+2), chapter run contiguous 1..16 + Appendix A, 233 outline entries, compile-clean, `.tex` leak sweep clean. Prior **v3.0.5 released 2026-08-11** (164pp) — worked-example correctness, reader-reported and **bench-verified on real silicon**: the Ch.1 fading experiment drives its pin (`P_OE`), the async-serial TX/RX examples assemble as printed (`byte`/`send`/`recv` are reserved words), and the quadrature example routes its B phase from the next pin up (`P_PLUS1_B`). Two new Ch.1 asides give the per-board LED pin map (P56/P57 Edge vs **P38/P39** 32MB, where P56/P57 are PSRAM CLK/CE#) and explain the buffered-LED touch sensitivity; the Ch.14 Quick Reference now names `P_OE` on every output mode. Render-verified 164pp (+2, an increase), 231 outline entries, 0 blank pages; p131 eyeballed after a first build rendered a tofu glyph (U+2611 → ASCII `[OE]`). Prior **v3.0.3 released 2026-07-12** (164pp) — technical-accuracy pass: PASM2 semantics and timing read as the silicon defines (the CORDIC is one solver the cogs share through hub slots, `MUL` is a 16×16→32 multiply, RCFAST runs a nominal ~24 MHz), and the `TESTP` WZ pin-state and async-serial `P_OE`-drive worked examples now behave as the text describes.
Prior **v3.0.2 released 2026-07-07** (163pp) — correction wave: three event-table encodings match silicon (SETSE %000 = LUT read/write & hub-lock event, EVENT_INT %0000, EVENT_QMT %1111) + dedicated-cog servo example rename. Prior **v3.0.1 (2026-06-25)** — accuracy re-audit (every PASM2/Spin2 example compile-checked with `pnut-ts` against the current compiler), typography refresh on the shared platform stack (Plex, no line-number gutter, 8.5pt code boxes; ✓/✗/θ glyph fallbacks), lowercase house-style sweep, and a companion example-library ZIP (first-blink, multicog-blink, hub-counters). **Resolves both prior DEFERRALS:** the Cog-Anatomy diagram is repaired ("Each Cog Contains:") and the full pnut-ts compile-cert is done. Regenerated clean (162pp; 172→162 from the denser typography, outline verified complete). Release-gate audit: local `audit/release-gate-2026-06-25.md`. Prior **v3.0.0 (2026-06-10)** absorbed the ~33-error content re-audit + Ch2 egg-beater fix. chip review outstanding.

**P2 Debug Window Manual** · `p2-debug-window-manual` · manual
**v1.1.1 released 2026-07-27** (168pp) — **run-verification patch.** All 34 example programs run against **PNut v55 on real silicon**; the four that failed are fixed, and both causes were systemic. **F-227** — the three `PC_KEY`/`PC_MOUSE` examples omitted the command's own **escape backtick**, so the compiler transmitted the characters `PC_KEY(@key` to the window and compiled *no command*: the pointer was never written and the control loops responded to nothing (proven by reading the emitted display strings out of two `pnut-ts -d` binaries). The **manual itself taught the broken form** (ch12 ×6, ch15, App A) and so did the KB (`pc_key`/`pc_mouse` yaml) — all corrected; the bench-certified reference (`REF/robot-dog/test_dog_panel.spin2`) had it right all along. **F-228** — a display **named after a display keyword** is never declared, isolated by a six-way probe in which five SCOPE creates opened and the one named `Trace` did not, from byte-identical create lines. Stephen then supplied the **definitive naming rules from a PNut v55 `p2com.asm` study** (now `REF/DEBUG-WINDOW-NAME-RULES.md` + `debug.yaml` `window_name_rules`): legal iff leading letter/`_`, not one of the **103** reserved display words, not a currently-open name, case-insensitive, 30-character truncation. ch02 teaches all five; App A corrected — it had implied its own directive list *was* the reserved set. Also new: the mouse-vs-artwork Y flip (ch15), from the same bench-certified panel code. Render-verified 168pp — one *fewer* than v1.1.0, so it was investigated rather than accepted: heading set identical, every diffed line accounted for, word count +709, and the −1 traces to this build absorbing the 07-20 mnemonic-bold `test`/`fit` fix, which v1.1.0 had shipped as **7 visible corruptions** ("does not FIT", "a bit TEST"). Example ZIP rebuilt and the **released `DOCs/` copy refreshed — it had still been shipping the broken code**. Prior **v1.1.0 released 2026-07-14** (169pp) — **silicon-verification sweep.** The whole DEBUG-window fact set re-tested on real P2/PNut (EF-041…EF-052), draining **F-216** (six ship-blockers, three of them live in *shipped, hardware-run example code*) and the manual half of **F-212**; the KB half ships as **v1.14.3**. Corrected: the PLOT worked example's sine wave (a signed `/` made it a flat line lying on the axis it draws), the ch13 packed-data twins (MSB-first against the host's LSB-first unpack — the bug survived a silicon run because the payload was `getrnd()`), and the LOGIC opening example (32 channels, not 4 — it had *no example file*, which is why it was never compiled; one now exists). New material: `PC_MOUSE` returns **raw client pixels** in 5 of 9 windows (any hit-test built on the on-screen readout is wrong), the four `SAVE` traps, the `CLOSE`/`DEBUG_END_SESSION` lifecycle, and the named-color keyword system. Example library 32→**34** programs, all compile-clean and byte-identical to their manual code blocks. **Two render defects caught by reading the rendered pages** (not the log, which was clean): a superscript-n that printed as nothing — turning "multiplies by 2ⁿ" into the falsehood "multiplies by 2" — and a blockquote heading that printed a literal "###". Both are now gated by `tools/validation/audit-font-glyphs.py`. Prior **v1.0.1 (2026-06-26)** — accuracy + typography refresh: DEBUG-output quoting examples corrected data-set-wide, FFT/run-up worked programs fixed, per-window details tightened (trigger offsets, defaults/ranges, PLOT polar, ALT, MIDI), IBM Plex typography (156pp); 32-demo example library refreshed (source ZIP). Prior **v1.0.0 (2026-06-16)** initial community-review release.

**P2 Streamer Programming Guide** · `p2-streamer-programming-guide` · manual
**v1.0.7 released 2026-07-21** (72pp) — readability pass: a reader-as-foil aside and two self-referential flourishes removed from chapter openers; no mode encodings or technical content changed. Render-verified 72pp (was 75; −3 benign section-keep reflow, all 18 ch + Parts I–V + App A–D + Index present), compile-clean.
Prior **v1.0.6 released 2026-07-12** (75pp) — Silicon-Doc accuracy pass: the NCO phase accumulator resolves to sysclk/2^31 (essentially exact at any sysclk), the VGA field-timing, DAC-routed RGB, and SPI-clock worked examples drive correct signals, the FIFO wrap-mode buffer start is long-aligned, and the Appendix-A RFBYTE mode encodings read per the Silicon Doc.
Prior **v1.0.5 released 2026-07-07** (75pp) — correction wave: §12.2 sub-pin selection documents the silicon's per-pin-count field widths (1-pin uses D[19:17], 2-pin D[19:18]+DAC-config bit, 4-pin D[19]+DAC-config bits; higher pins via the group field D[22:20]). Prior **v1.0.4 (2026-07-04)** community-review edition — forum-provenance patch (HDMI-audio blanking budget sourced to the HDMI data-island spec §15.2 · DVI/HDMI blanking floors framed as display-specific observations · SINC2 measurement-period bound reframed §10.4); render-verified 75pp = prior, 0 glyph drops; `audit/forum-provenance-audit-2026-07-04.md`. Prior v1.0.3 (2026-07-03) Wave-3 designer-authoritative additions + cross-ref filter (82 links/0 dead). chip review outstanding.

**The P2 Architect's Guide** · `p2-architect-guide` · manual
**v1.0.2 released 2026-07-21** (52pp) — readability pass: closing-cadence evened (the weakest section-ending beats flattened, the opening metronome broken); the method, the two worked derivations, and every design point are unchanged. Render-verified 52pp (was 53; −1 benign reflow, full outline Parts I–III + In Closing + App A/B + Glossary + Where to Next), compile-clean.
Prior **v1.0.1 released 2026-07-12** (53pp) — accuracy refinement: PSRAM is named as an external resource, distinct from the P2's on-chip LUT RAM, CORDIC, and streamer.
Prior **v1.0.0 released 2026-07-08** (53pp) — MAIDEN release. The design/realization companion to the reference manuals (*Getting Started* is the prerequisite): a three-act narrative — get a real project off the ground (Part I, distilled from 12 real projects), *derive* its architecture from physical forces (Part II, the functional-decomposition method + two worked derivations, robot dog + streaming pipeline), then walk the whole process again with an AI agent (Part III, synthesized from the same 12 projects). Teaches a method, not a catalogue. 4 TikZ figures; ships **no example ZIP** (0 embedded code — orphaned examples-library archived). Render-verified 53pp, full TOC (Parts I-III + In Closing + appendices), 0 LaTeX errors, compile-clean. chip review outstanding.

**P2 Interpreters & Emulators Guide** · `p2-xbyte-programming-guide` · manual
**v1.0.0 released 2026-07-20** (100pp) — INITIAL community-review release. The guide to the P2's XBYTE hardware bytecode engine — the skip family (SKIP/SKIPF/EXECF), the FIFO bytecode stream, and LUT dispatch — from what the engine is through a minimal custom VM and a compact, illustrative CPU emulator, plus servicing guest interrupts, prefix/alternate tables, and using the engine beyond interpreters. Two-register voice (teaching + reference), twin on the shared `p2kb-platform-*` stack. Subtitle "The XBYTE Engine and Bytecode Dispatch on the Propeller 2". **Chip Gracey reviewed the v0.4.0 draft** — CG-1 in-place examples, CG-2 voice/stance pass, CG-3 GETBRK correction — all applied (∴ Chip gate ✅). Pre-render changeset-integrity audit of the review delta (5-agent adversarial hunk-walk, 100% coverage — `audit/changeset-integrity-2026-07-20.md`) caught + fixed one delta-introduced false universal (§12.4); App C citations hand-verified against the live emulator sources (Maccaferri's `simple_i8086` EXECF/rung-2 vs `i8086_xt` plain-JMP/rung-1, ~100-of-8000-line hub-vs-PSRAM diff). Render-verified: 100pp, full outline (6 Parts / 20 Ch / App A–D), key sections present, §19.1 SKIPF row = 32, compile-clean. Ships a 2-program example ZIP (§12.2 VM + §18.5 display list, both `pnut-ts`-clean). First consumer of the mnemonic-bold "test"/"fit" English-default platform fix. §C.8 forum URL Cloudflare-blocked → human-eyeball at publish. Reframed from the v0.1.0 draft (grew 15→20 ch across the v0.2.0/v0.3.0 reworks; XBYTE reframed as one rung of a dispatch ladder). Slug/filename stay `p2-xbyte-*`.

**P2AN001 — Single-Pin ADC Instrumentation** · `P2AN001` · app-note
**v1.0.4 released 2026-08-17** (20pp) — the pin power domain a measurement actually references: I/O domains are isolated groups of FOUR (P0–3, P4–7, … P60–63), each sharing the one VIO/GIO pair its ADC references; the eight-pin grouping on a P2 Edge is the LDO/header layer for current budgeting (300 mA per header group), not the ADC's reference domain, because one 3.3 V regulator feeds two four-pin domains that reach the die through separate VIO pins. The ~15 mV pin-to-pin error floor names its source as a designer-stated figure rather than a characterized specification. Render-verified 20pp (= prior), compile-clean; example ZIP verified byte-identical to `examples-library/`; the YAML companion carries the same provenance qualifier (F-287). Prior **v1.0.3 released 2026-08-08** (20pp) — licensing patch, CC BY-SA 4.0 restored; zero technical content change. Prior **v1.0.2 released 2026-07-12** (20pp) — technical-precision pass on the ADC recipes: the P2 powers its I/O in eight groups of eight sharing one VIO/GIO pair (a multi-pin shared-node measurement stays within a single group), SINC2 filtering accepts any sample period (not only powers of two), and the below-ground self-check reads build-dependent.
Prior **v1.0.1 (2026-07-03, 20pp)** — foundational first note + doc-class & companion-schema exemplar (Family A0); techniques-catalog on the enriched IOSP Ch.16. v1.0.1 = editorial compile-status wording patch.

**P2AN002 — CORDIC for Real Work** · `P2AN002` · app-note
**v1.0.3 released 2026-08-17** (15pp) — the pipelining recipe keeps hub access out of both CORDIC loops, the shape measured clean on real silicon at 200 MHz: Recipe 6 and its example-library program are rewritten together (SETQ block read, REP loops, ALTS/ALTD indexing a cog-RAM buffer), and a pitfall carries the measured rule — hub access inside either loop loses results, and the failure is SILENT (plausible numbers, some fraction stale). Every OBEX number, title and author checked against the live catalog. Render-verified 15pp (+1), all recipes present, compile-clean; the YAML companion was brought into agreement on four entries (F-283). Prior **v1.0.2 released 2026-08-08** (14pp) — licensing patch, CC BY-SA 4.0 restored; zero technical content change. Prior **v1.0.1 released 2026-07-12** (14pp) — derivation and attribution refinement: the circle-layout step-size uses the halved `$8000_0000 / (STEPS / 2)` form to stay within 32 bits, and the OBEX Resources match the catalog (#2812 ersmith, #5361 James Smith).
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

**P2AN007 — Data Structures with the New Language Facilities** · `P2AN007` · app-note
**v1.0.0 (2026-07-13, 16pp) — INITIAL release.** Family **C2**. Techniques-catalog: the Spin2 `STRUCT` facility + the worked code for sharing records safely across cogs, through 6 recipes — in-cog record/array, lock-free SPSC ring buffer, latest-wins mailbox, locked multi-writer queue (real P2 `LOCKNEW`/`LOCKTRY`/`LOCKREL`), plus the two STRUCT facilities added since v45: **R5** member bitfields (`{Spin2_v54}`) packing a whole record into one atomically-published long, and **R6** `OFFSETOF` (`{Spin2_v53}`) for computed offsets under raw addressing. R1–R4 stay `{Spin2_v45}`. **The only reader-facing P2 doc covering `OFFSETOF` or struct bitfields.** Every cross-cog claim **hardware-confirmed on real P2 silicon** (two cogs contending; each discipline measured against a deliberately-broken control that was REQUIRED to fail — EF-036…EF-040). Headline empirical result: a record packed into one long is **not** atomic unless published in one store (in-place field writes tore 116,452 / 200,000; staged one-store publish tore 0). First render carrying the F-214 mnemonic-bold hyphen fix. Implementation-only; the contract decision is cited to the Architect's Guide.

**AI Privacy Guide** · `ai-privacy-guide` · guide
Released; both reviews complete; presentation-class (rides pristine `p2kb-foundation.sty`).

## In progress — actively being built

Not part of the live consistency set until released; free to evolve independently, reconciled
against the shared conventions at promotion. (`P2 Layout Torture Test` is an **instrument** — a
tool serving an effort, never released — carried here while it's actively used.)

| Document | Type | Ver | Draft | Assets | Platform | Chip | Comm | Released |
|----------|------|-----|:--:|:--:|:--:|:--:|:--:|:--:|
| Single-Step Debugger | manual | draft | ✅ | ✅ | ✅ | ⏳ | ⏳ | |
| PNut-Term-TS User Guide | guide | 0.1.0 | | | | — | | |
| P2 Layout Torture Test | instrument | — | ✅ | ✅ | ✅ | — | — | — |

### Detail

**P2 Single-Step Debugger Manual** · `p2-single-step-debugger-manual` · manual
On shared platform stack (foundation/content/diagrams); awaiting chip + community review.

**PNut-Term-TS User Guide** · `pnut-term-ts-user-guide` · guide
User guide for **PNut-Term-TS**, the cross-platform desktop debug terminal for the P2 — a *tool* guide (`doc_class: behavior`), not a P2 silicon/language reference. Subtitle: *The Cross-Platform Downloader, Terminal, and Debug Display for the Propeller 2*. **Purpose = positioning within the P2 agentic tool chain** (P2KB MCP + `pnut_ts` + `pnut_term_ts`, optional Spin2 VS Code extension); delivers the agentic usability that **The P2 Architect's Guide, Part 3** describes. Identity = **three tools in one** (downloader · Parallax Serial Terminal replacement · PNut debug-window replacement/production, now cross-platform). Pedagogy = **shared orientation trunk → fork by intent** (GUI vs headless). Seeded 2026-07-21 (standing structure only, no content drafted); grounded on two feeds snapshotted from the PNut-Term-TS repo (v0.10.3) in its `REF-NO-COMMIT/`. Chip review n/a (no P2 silicon claims). Expected to ride the `p2kb-platform` stack (ships code + screenshots), unlike the off-platform AI Privacy Guide — Forge template wiring TBD at first render. Closest sibling for voice/scaffolding: the Single-Step Debugger Manual (same host application). **Release gate: co-releases with the P2 Single-Step Debugger Manual, timed to PNut-Term-TS v1.0** (Debug Window Manual already released).

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

*(Family C complete: C1/C3 — **P2AN005/P2AN006 released v1.0.0 2026-07-07**; C2 — **P2AN007 released v1.0.0 2026-07-13**. All three in Done.)*

## Abandoned — retired, not carrying forward (last)

Started, then retired by decision — superseded or abandoned. Kept for history; **not** resumed
without an explicit revive decision; never consistency-bound.

| Document | Type | Why retired |
|----------|------|-------------|
| Smart Pins Tutorial · `p2-smart-pins-tutorial` | manual | superseded by the I/O & Smart Pins User Guide (newer generation). **Archived out of the live tree 2026-08-16** to `archive/2026-08-16-smart-pins-tutorial/` (gitignored, local; git history retains every version) — its `manuals/`, `workspace/` and the orphaned `p2kb-sp-semantic.lua` filter fork all moved together. **This row stays**: it is the authority the guide-conformance instrument reads to build its exclusion list, and deleting it would silently un-exclude four files. |

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
2026-08-17 18:25  PLATFORM  filters/{p2kb-platform-pagination,p2kb-platform-figures,p2kb-platform-code-coloring,p2kb-platform-tables}.lua  (F-286: every site where a filter emits `stringify()`'d text into a raw LaTeX position now escapes it, via a module-level helper with the invariant stated at its definition. A raw argument bypasses pandoc's escaping entirely, so `&` there IS an alignment tab and `%` silently comments out the rest of the line WITH A CLEAN LOG — F-284 was one instance of the class; this closes the other five (Part title, figure caption, sidetrack TOC entry, table-caption stringify fallback, three cell-renderer pandoc.write fallbacks). The rule already existed in-tree with its rationale in a comment, and was applied at ONE call site in four, because escaping was a decision re-made per call site. **BENIGN FOR EVERY MANUAL — no re-render owed by anyone.** Blast radius measured, not assumed: all 38 `# Part` headings and every `figurecaption` div across the live masters were scanned for `&` and `%`, and the only hit is in a creation-guide that renders nothing; deSilva's 6 emitted sidetrack titles are clean; the app notes carry no Parts, captions or sidetracks at all. The escapes fire only on characters that are already broken today, so a re-render would be byte-equivalent. NOT collapsed into the 04:56 tables.lua line below: that one is F-284, a different change-set, and its adjudication explains why Assembly alone owed a re-render.)
2026-08-17 04:56  PLATFORM  filters/p2kb-platform-tables.lua  (the 9-column instruction-encoding table path now escapes `&`, `%`, `#` and `_` in cell text, which it never did — the 6-column path beside it always had. An unescaped `&` in a cell is read as a LaTeX alignment tab: it ends the cell early, shifts every later column right, and pushes the row past the table's right border. CAUGHT IN THE RENDERED PDF, not the log — the v3.1.6 build reported 0 errors while Assembly pp.326/329 printed the TEST and TESTN rows as "Parity of (D" | "S)", losing the AND operator from a bit-level instruction definition, and it had been shipping that way since at least v3.1.5. `%` is the worse latent case: it would silently comment out the rest of the row. Blast radius measured, not assumed — 281 encoding tables across the manual, exactly 2 corrupted cells, and zero `%`/`#`/`_` exposure anywhere in that path, so Assembly is the only affected document. First consumer: **p2-assembly-language-manual v3.1.6**, which must RE-RENDER before release; the other five wave elements were verified unaffected and do not need one. Benign for every other manual — the escapes only fire on characters that are already broken today.)
2026-08-17 04:38  PUBLISH   p2-pasm-desilva-style            (v3.0.6, 166pp — an honest platform comparison and the multi-cog pin hazard: Appendix A gains the RP2350 and a software axis, and Chapter 16 teaches that DIR/OUT are OR'd across cogs. Render-verified 166pp (was 164): chapter run contiguous 1..16 + Appendix A, 233 outline entries, all key sections text-present, compile log 0 serious signatures, final-pass page count matches the PDF exactly (the log's first pass reads 160 — early passes are short until the TOC settles). `.tex` leak sweep clean. Max overfull 20.6pt (3 at/over 20pt, cosmetic).)
2026-08-17 04:33  PUBLISH   P2AN002                          (v1.0.3, 15pp — the pipelining recipe keeps hub access out of both CORDIC loops, the shape measured clean on silicon; the released v1.0.2 taught `rdlong` inside the fill loop, which loses results SILENTLY. Recipe 6 and its example-library program rewritten together (SETQ block read, REP loops, ALTS/ALTD cog-RAM indexing), and every OBEX number, title and author checked against the live catalog. Render-verified 15pp (was 14), all recipes present, compile-clean, max overfull 0.6pt, `.tex` sweep clean. YAML companion brought into agreement (F-283) — four entries, not the two the finding named.)
2026-08-17 04:31  PUBLISH   P2AN001                          (v1.0.4, 20pp — the pin power domain a measurement actually references: I/O domains are isolated groups of FOUR sharing one VIO/GIO pair, and the eight-pin grouping on an Edge is the LDO/header layer, not the ADC's reference domain. The ~15 mV pin-to-pin error floor now names its source as a designer-stated figure rather than a characterized specification. Render-verified 20pp (= prior), all recipes present, compile-clean, 0 overfull ≥20pt, `.tex` sweep clean. Example ZIP verified byte-identical to `examples-library/`. YAML companion carried the same provenance qualifier (F-287).)
2026-08-08 22:47  PUBLISH   p2-assembly-language-manual      (v3.1.5, 503pp — licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified: 503pp (was 505; the -2 investigated, not accepted — whole-document content intact, front matter + all 6 Part-I chapters + Part II @p128 + Part III @p404 on their expected pages, 490 outline entries, and the instruction-letter run complete at 22 letters ABCDEFGHIJLMNOPQRSTWXZ; K/U/V/Y absent because no PASM2 instruction begins with them — source carries exactly those 22 files and the KB confirms 0 entries for each. The -2 is the same tighter table packing DeSilva shows, a platform improvement absorbed at this render). Page count matches the compile log exactly; 0 LaTeX errors; licence page p15 eyeballed — CC BY-SA with the restored Adapt bullet, joint Iron Sheep + Parallax copyright, single-period "Parallax Inc.")
2026-08-08 22:33  PUBLISH   p2-io-and-smart-pins-user-guide  (v1.0.8, 396pp — licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 396pp (= v1.0.7, no shift — the largest manual absorbed the longer licence block with no downstream movement), 31 outline entries, compile log clean and its page count matches, licence section present + correct.)
2026-08-08 22:28  PUBLISH   p2-getting-started-guide         (v1.0.3, 25pp — licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 25pp (= v1.0.2), only p1 and the licence page differ from the prior release, compile-clean.)
2026-08-08 22:26  PUBLISH   p2-streamer-programming-guide    (v1.0.8, 73pp — licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 73pp (was 72; +1 is the longer BY-SA block, which pushes "Enhancement Markers" onto its own p9 — a sparse but complete page, NOT an orphan; flagged to Stephen as a layout judgement call, recommendation was to leave it). Compile-clean, licence section p7.)
2026-08-08 22:24  PUBLISH   p2-xbyte-programming-guide       (v1.0.1, 100pp — licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 100pp (= v1.0.0, no shift), 30 outline entries, compile-clean, licence section p8.)
2026-08-08 22:23  PUBLISH   p2-debug-window-manual           (v1.1.2, 168pp — licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 168pp (= v1.1.1, no shift), 18 outline entries, compile-clean with no "Unable to load picture" (its figures all resolved), licence section p7.)
2026-08-08 22:19  PUBLISH   p2-architect-guide               (v1.0.3, 52pp — licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 52pp (= v1.0.2, no shift), 19 outline entries, compile-clean, licence section p4.)
2026-08-08 21:46  PUBLISH   P2AN007                          (v1.0.1, 16pp — app-note licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 16pp, licence section present, compile-clean.)
2026-08-08 21:44  PUBLISH   P2AN006                          (v1.0.1, 13pp — app-note licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 13pp (was 12; +1 = the longer BY-SA block), licence section complete, compile-clean.)
2026-08-08 21:44  PUBLISH   P2AN005                          (v1.0.2, 12pp — app-note licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 12pp; content confirmed complete against an independent daemon build (zero words lost) — production packs the Revision History and the full licence block onto one page.)
2026-08-08 21:43  PUBLISH   P2AN004                          (v1.0.2, 15pp — app-note licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 15pp (was 14; +1 = the longer BY-SA block), licence section complete, compile-clean.)
2026-08-08 21:38  PUBLISH   P2AN003                          (v1.0.2, 19pp — app-note licensing patch, CC BY-SA 4.0 restored; ZERO technical content change. Render-verified 19pp, licence section complete, compile-clean.)
2026-07-27 00:33  PUBLISH   p2-debug-window-manual           (v1.1.1, 168pp — run-verification patch: Stephen ran ALL 34 example programs against PNut v55 on real silicon; 4 failed and are fixed. F-227 — the three PC_KEY/PC_MOUSE examples omitted the command's own escape backtick, so the compiler transmitted the characters "PC_KEY(@key" to the window and compiled NO command (proven by reading the emitted display strings out of two pnut-ts -d binaries); the pointer was never written, so the control loops polled forever and responded to nothing. Class-wide: the MANUAL TAUGHT the broken form (ch12 x6, ch15, App A) and so did the KB (pc_key/pc_mouse yaml) — all corrected. F-228 — a display NAMED AFTER a display keyword is never declared; isolated by a 6-way probe where five SCOPE creates opened and the one named `Trace` did not, from byte-identical create lines. Stephen then supplied the DEFINITIVE naming rules from a PNut v55 p2com.asm study (now REF/DEBUG-WINDOW-NAME-RULES.md + debug.yaml window_name_rules): legal iff leading letter/_, not one of the 103 reserved display words, not a currently-open name, case-insensitive, 30-char truncation. ch02 teaches all five; App A corrected (it had implied its own directive list WAS the reserved set — it is 103 words incl. the 9 types, GREY+GRAY, color modes, packed modes). Render-verified: 168pp (was 169; investigated rather than accepted — heading set IDENTICAL, every diffed line accounted for, word count +709, and the -1 is explained by this build ABSORBING the 07-20 mnemonic-bold test/fit fix, which v1.1.0 had shipped as 7 visible "does not FIT"/"a bit TEST" corruptions — that answers the fleet-sweep follow-up on the PLATFORM line below for THIS manual), outline complete (15 ch + 3 app), compile-clean 0 LaTeX errors, 0 missing glyphs, pp.18/19/119/146/149 eyeballed. Example ZIP rebuilt: 34 programs, all compile-clean, all byte-identical to their manual code blocks, and the RELEASED DOCs/ zip refreshed — it had still been shipping the broken code.)
2026-07-21 22:55  PUBLISH   p2-streamer-programming-guide    (v1.0.7, 72pp — readability pass: a reader-as-foil aside and two self-referential flourishes removed from chapter openers, no technical change; render-verified 72pp (was 75, −3 benign section-keep reflow, no drop — all 18 ch + Parts I–V + App A–D + Index present), edited openers text-present, compile-clean)
2026-07-21 22:53  PUBLISH   p2-architect-guide               (v1.0.2, 52pp — readability pass: closing-cadence evened (7 weakest section-ending beats flattened, opening metronome broken), refrains + send-off intact, no technical change; render-verified 52pp (was 53, −1 benign reflow, no drop — full outline Parts I–III + In Closing + App A/B + Glossary + Where to Next), compile-clean)
2026-07-21 22:52  PUBLISH   p2-getting-started-guide         (v1.0.2, 25pp — readability pass: a recurring summarizing frame varied for smoother narration, no technical change; render-verified 25pp (= prior), outline complete, compile-clean)
2026-07-20 21:53  PUBLISH   p2-xbyte-programming-guide       (v1.0.0, 100pp — INITIAL community-review release: the P2 XBYTE hardware bytecode engine, the skip family (SKIP/SKIPF/EXECF), FIFO/LUT dispatch → a minimal custom VM + a compact illustrative CPU emulator. First consumer to render after — and thus absorbing — the 21:00 mnemonic-bold "test"/"fit" English-default fix below. Chip Gracey reviewed (CG-1/2/3 applied); pre-render changeset-integrity audit of the review delta (5-agent adversarial hunk-walk, 100% coverage) fixed one §12.4 false universal, plus an Appendix-D blank-page layout fix. Render-verified: 100pp, full outline (6 Parts / 20 Ch / App A-D), NO blank pages (App C→D transition eyeballed), §19.1 SKIPF row = 32, compile-clean. Ships a 2-program example ZIP.)
2026-07-20 21:00  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua  (the ambiguous words "test" and "fit" now DEFAULT to English prose, matching the and/or/not/add/long/word/byte rules — previously they defaulted to the instruction, so bare-prose English fell through and was wrongly uppercased. A genuine TEST/FIT instruction reference still uppercases via code (`TEST`/`FIT`, unchanged) or the explicit "TEST instruction" / "FIT directive|statement" guards (retained). Fixes English words rendered as instructions in inline prose ("the intuitive TEST", "a poor FIT", "these FIT", "FIT is graded"). Surfaced by the XBYTE guide review (v0.5.0), which is the first consumer on its next render. Live-but-benign for released manuals: the flip only lowercases English test/fit that was wrongly capitalised — it cannot corrupt real code or a properly-marked instruction reference — so each absorbs it at its next natural render, same standing as the 2026-07-13 hyphenated-compound and 2026-07-07 "ones" fixes. A fleet PDF text-sweep for stray " TEST "/" FIT " in released manuals is the follow-up to confirm which, if any, carry a visible instance worth a render-only patch.)
2026-07-16 23:18  PUBLISH   p2-io-and-smart-pins-user-guide  (v1.0.7, 396pp — Ch.9 §9.1 "Complementary Outputs and Dead-Band": a complementary half-bridge pair is TWO coordinated Smart Pins (one per side, low side inverted via P_INVERT_OUTPUT, dead-band produced in software), not a single-pin mode — Chip-confirmed; KB twin v1.14.5 (F-225). Render-verified: 396pp (= v1.0.6; the new note absorbed in reflow, not a drop — §9.1 text-present p139 + page image eyeballed), outline complete (19 ch + A-G), compile-clean 0 LaTeX errors. Examples unchanged.)
2026-07-14 17:53  PUBLISH   p2-assembly-language-manual      (v3.1.4, 505pp — RENDER-ONLY patch absorbing the F-214 mnemonic-bold fix; ZERO content change (opus-master diff since v3.1.3 = the version bump + this changelog entry, nothing else). Fixes the three hyphenated names the released v3.1.3 PDF printed wrong: not-taken x4, 1..4-byte x2, and — the reason this shipped as a release rather than a nit — the cross-reference "p2-io-AND-smart-pins-user-guide", which named a manual that does not exist. Verified against the released v3.1.3 PDF by full text-diff: EXACTLY 8 lines differ (1 version + the 7 corruption sites) and nothing else; 505pp unchanged, 45,999 text lines unchanged, outline complete (6 ch + 22 instruction letters + 10 appendices), 0 LaTeX errors, 0 missing glyphs, cover + p.99 eyeballed. Mnemonics still uppercase (RDLONG/SETQ/AUGS) — the fix does not over-correct.)
2026-07-14 07:40  PUBLISH   p2-debug-window-manual           (v1.1.0, 169pp — silicon-verification sweep: the DEBUG-window fact set re-tested on real P2/PNut (EF-041..EF-052). SIX ship-blockers (F-216), THREE of them in shipped, hardware-run example code: the PLOT sine wave was a flat line (signed `/`), ch13 packed MSB-first against the host's LSB-first unpack, and the LOGIC opening example declared 32 channels not 4 (no example file existed — one now does). Plus the corrections wave (PRECISE default, COLOR-before-TEXT, SPECTRO axes) and the new material (PC_MOUSE raw-client-pixels in 5 of 9 windows, the four SAVE traps, CLOSE/DEBUG_END_SESSION lifecycle, named colors). Rides KB v1.14.3 (F-212 + addendum). Render-verified 160->169pp (+9 = new material; page-count INCREASE, no drop), outline complete (15 ch + 3 app), compile-clean, 0 missing glyphs, pp.13/56/88/97 eyeballed. TWO render defects caught in review and fixed before release: a superscript-n that printed nothing ("multiplies by 2" — a NEW falsehood inside a correction) and a blockquote heading that printed literal "###". Both now gated by tools/validation/audit-font-glyphs.py. Example ZIP: 34 programs, all compile-clean + byte-identical to their manual code blocks.)
2026-07-13 20:13  PUBLISH   P2AN007                          (v1.0.0, 16pp — app-note, INITIAL release: STRUCT records + safe cross-cog sharing, 6 recipes (in-cog record, lock-free SPSC ring, latest-wins mailbox, locked multi-writer queue, whole record packed into one atomically-published long via {Spin2_v54} member bitfields, {Spin2_v53} OFFSETOF computed offsets). First reader-facing doc covering OFFSETOF or struct bitfields. Every cross-cog claim hardware-confirmed on real P2 silicon, two cogs contending, each discipline measured against a deliberately-broken control that was REQUIRED to fail (EF-036..EF-040). Carries the F-214 mnemonic-bold fix (hyphenated compound tokens no longer uppercased — filenames/slugs render correctly); render-verified 16pp, all sections present, compile-clean, no content-drop)
2026-07-13 20:00  PLATFORM  filters/p2kb-platform-mnemonic-bold.lua  (F-214: a mnemonic inside a HYPHENATED compound token is no longer uppercased — the guard now treats a hyphen joining two alphanumeric runs as an identifier connector. Fixes corrupted filenames/slugs in rendered inline code (single-long-packed-record.spin2 -> single-LONG-..., not-taken -> NOT-taken, p2-io-and-smart-pins-user-guide -> p2-io-AND-...). Real Spin2 code is untouched: subtraction, unary minus, standalone LONG[@ptr], and the .long[5] pointer size-override all still uppercase. Benefits every manual; first consumed by P2AN007 v1.0.0. ADJUDICATED 2026-07-14 — the fleet was swept by text-extracting ALL 14 released PDFs, and the Assembly Language Manual was the ONLY one carrying the corruption; it is now absorbed (v3.1.4, PUBLISH above). Every other consumer's released PDF is content-clean, so this line is NOT a forced re-release for them — they absorb it at their next natural render (same standing as the 2026-06-29 uppercase-policy and 2026-06-26 crossref lines). The line stays until every consumer has a PUBLISH above it, per the prune rule; it is live-but-benign, not outstanding debt.)
2026-07-12 04:36  PUBLISH   p2-assembly-language-manual      (v3.1.3, 505pp — silicon/hardware-grounded accuracy pass: instruction semantics + flag effects read as the silicon defines (AUGS/AUGD augment surviving intervening instructions, TEST/interrupt-priority/COGINIT/QEXP), GETCT-pair bracketing carries a fixed 2-clock overhead HW-confirmed on real P2; render-verified 505pp, outline complete, compile-clean, no content-drop)
2026-07-12 03:48  PUBLISH   P2AN003                          (v1.0.1, 19pp — DAC precision refinement: the PWM-dither spectral component sits at a fixed sysclock/256, independent of the sample period; render-verified 19pp, all recipes present, compile-clean, no content-drop)
2026-07-12 03:48  PUBLISH   P2AN004                          (v1.0.1, 14pp — spec-accuracy + titling refinement (retitled Frequency / Rotation / RC-Timing Measurement): programs run at 200 MHz (top of the PLL VCO 100-200 MHz range), P_FILT1_AB routes A/B through the global FILT1 ~600 ns low-pass; render-verified 14pp, all instruments present, compile-clean, no content-drop)
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
| `p2-assembly-language-manual` | 3.1.5 | ✅ current | rebuilt 08-08 (licensing wave; 503pp) |
| `p2-io-and-smart-pins-user-guide` | 1.0.8 | ✅ current | rebuilt 08-08 (licensing wave; 396pp) |
| `p2-debug-window-manual` | 1.1.2 | ✅ current | rebuilt 08-08 (licensing wave; 168pp) |
| `p2-pasm-desilva-style` | 3.0.5 | ✅ current | rebuilt 08-11 (example-correctness; 164pp) |
| `p2-xbyte-programming-guide` | 1.0.1 | ✅ current | rebuilt 08-08 (licensing wave; 100pp) |
| `p2-streamer-programming-guide` | 1.0.8 | ✅ current | rebuilt 08-08 (licensing wave; 73pp) |
| `p2-architect-guide` | 1.0.3 | ✅ current | rebuilt 08-08 (licensing wave; 52pp) |
| `p2-getting-started-guide` | 1.0.3 | ✅ current | rebuilt 08-08 (licensing wave; 25pp) |
| `P2AN001`…`P2AN007` | see roster | ✅ current | all seven rebuilt 08-08 (licensing wave) |
| `p2-single-step-debugger-manual` | draft | ⏳ behind 06-12 | regression rebuild 06-10; predates the 06-12 edit. **Release is imminent** — co-releases with PNut-Term-TS, now that the tool has shipped |
| `pnut-term-ts-user-guide` | 0.1.0 | ⏳ never published | drafted; co-releases with the Single-Step Debugger Manual |
| `p2-layout-torture-test` | — | ⏳ stale (instrument) | behind several platform files + `diagrams.sty` |

> **Prune status after the 2026-08-08 licensing wave: nothing is prunable yet, and that is
> correct.** All 15 live documents now carry a `PUBLISH` above every `PLATFORM` line, but the
> prune rule requires *every consuming manual* to sit above — and `p2-single-step-debugger-manual`
> (last built 2026-06-10) plus the never-published `pnut-term-ts-user-guide` still sit below
> everything from 2026-06-12 onward. **Releasing those two collapses this ledger substantially**
> — every `PLATFORM` line from 06-12 through 07-20 becomes fully absorbed and can be dropped in
> one pass. Worth doing as the closing step of that release rather than piecemeal.

**Pending platform change — 2026-07-07 (`mnemonic-bold.lua` "ones" fix):** every live
manual consumes `p2kb-platform-mnemonic-bold.lua` — **without exception since 2026-08-16**,
when the retired Smart Pins Tutorial and its `p2kb-sp-` filter fork left the live tree for
the local archive. The prune rule is simpler for it: no live document uses a `p2kb-sp-`
filter, so the fork family can be treated as gone rather than as a carve-out. By the
detector's rule each manual sits
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
