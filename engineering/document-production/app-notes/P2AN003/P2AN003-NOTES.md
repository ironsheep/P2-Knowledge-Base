# P2AN003 — Working Notes

**Status:** boundary DECIDED 2026-06-30 (mine-and-delineate fan-out, IOSP campaign §1b); ready for authoring (§3a)
**Created:** 2026-06-30
**Topic:** DAC & Analog Signal Generation (roster item **A1**, Smart-Pin Instrumentation family)
**Owning manual (enrichment fork):** P2 I/O & Smart Pins User Guide (IOSP)
**Campaign:** IOSP Release Campaign (`engineering/planning/IOSP-RELEASE-CAMPAIGN-SPRINT-PLAN.md`)

## Purpose

P2AN003 is the **output sibling to P2AN001 (ADC)** and the second Family-A
(Smart-Pin Instrumentation) note. Per the roster
(`engineering/analysis/p2-app-note-roster.md` §A1): the *basic* DAC smart-pin modes
are reference (→ IOSP); the *advanced worked technique* — dithering, audio/waveform
streaming, signal synthesis — is taught nowhere and becomes this note.

It is authored **as part of the IOSP Release Campaign**: its boundary-determination
pass decides the IOSP-vs-note split for the DAC region, and the **foundational fork
augments IOSP** before IOSP releases. Taken all the way through PDF.

## Topic — DAC & Analog Signal Generation

The P2's DAC capabilities through worked recipes: DAC output modes, dithering for
effective resolution, streaming waveforms (DDS / sample playback), and analog signal
synthesis. The *output* counterpart to the ADC instrumentation note.

## Boundary delineation (DECIDED 2026-06-30)

Outcome of the `mine-and-delineate` fan-out (IOSP campaign §1b). **This region mirrors
P2AN002/CORDIC: the foundational fork is EMPTY (IOSP already covers the basic DAC surface),
the advanced fork is PRESENT.**

### Foundational → IOSP : **EMPTY (no fork)**
IOSP **Chapter 10 (DAC Output)** + **§18.3 (DAC noise)** already document the entire basic DAC
surface — 4 resistor configs + selection guide (§10.1–10.2, §10.10), direct 8-bit / BIT_DAC
(§10.3), PRNG dither %00010 + PWM dither %00011 with the ×256 constraint (§10.4), DAC noise
%00001 (§18.3), voltage math (§10.7, §10.10), NCO+DAC / PWM+DAC fixed waveforms (§10.5), ADC
feedback during DAC (§10.6), output impedance / RC filtering (§10.9). **Cite, don't reproduce.**
Unlike P2AN001 (which *added* basic ADC modes to IOSP Ch.16 because they were missing), the DAC
counterpart was already authored — proposing any of it would duplicate existing content.
- *One optional non-fork item:* a forward cross-reference IOSP Ch.10 → P2AN003 (+ Streamer
  Guide for streamer-fed DAC). A cross-reference, **not** a content gap — route to the
  cross-ref-filter adoption pass / handle at P2AN003 release, not as a foundational fork.

### Advanced → P2AN003 : **PRESENT** — archetype **techniques-catalog** (like P2AN001/002)
Shared base (DAC modes + dither + voltage math) is **cited from IOSP Ch.10**, not reproduced;
then a decision table + runnable recipes:

| # | recipe / technique | foundation (cited in IOSP) | source seed | status |
|---|---|---|---|---|
| R1 | **Single-pin sample playback (DDS)** — phase accumulator → 16-bit dither DAC, IN-flag synced | §10.4 dither, §10.5 | reSound primitive; probe | primitive **compiles** ✓ |
| R2 | **Arbitrary waveform synthesis** — sine (CORDIC QSIN)/saw/tri/wavetable via DDS | §10.5 | QB "Analog Frequency to DAC" | code fetched (compile at authoring) |
| R3 | **Dithering for effective resolution** — PRNG vs PWM choice, sample-period tradeoffs, RC filter + effective-bits honesty | §10.4, §10.9 | KB dither modes; IOSP | seed ✓ |
| R4 | **Real-time ADC→DAC passthrough** — sample-pump read→write loop (ties to P2AN001 ADC) | §10.6 | QB "Digital Sample ADC to DAC" | code fetched (compile at authoring) |
| R5 | **Multi-channel mixing & panning** — sum N software streams → 1–8 pins, volume/pan | §10.4 | reSound `mainLoop` | seed ✓ |
| Going Further | **Streamer-fed continuous DAC playback** → pointer to the **Streamer Programming Guide** (cross-reference, not a recipe — mirrors P2AN002's CORDIC→streamer pointer) | — | reference exists | pointer-only |

**Described-not-rebuilt ceilings:** reSound full 32-stream engine (OBEX **#2861**, ~955 lines) and
the MOD/tracker player (QB "Simple Sound Engine Demo", Ahle2) — described + linked, not rebuilt
(parallels P2AN001's 8-pin interpreter, P2AN002's Park/FOC). Out-of-region: EZ Sound (OBEX #2860)
is NCO/FREQ tones, **not** DAC — routed to an IOSP Ch.8 one-line contrast, not a P2AN003 recipe.

### Verification model — **rig-gated Tier 0/1/2** (mirrors P2AN001, NOT P2AN002's known-answer)
- **Tier 0 (functional / known-answer):** DAC pin → ADC pin loopback jumper; a fixed 16-bit DAC
  value gives the computable DC `V=(val/65536)×Vfs` and the ADC reads it back — proves the *code*
  with no external gear (reuses the P2AN001 Tier-0 rig).
- **Tier 1 (waveform fidelity):** scope / audio interface + RC filter — shape, frequency, dither
  cleanliness (SNR/THD), effective bits.
- **Tier 2 (applied audio):** speaker/amp + multi-pin surround — mixing, panning, playback in situ.
- Recipes ship **qualitative** claims + the Tier-0 DC known-answer now; numeric SNR/THD/effective-
  bit figures **defer to a hardware run** (→ EF ledger when accepted), exactly as P2AN001's
  ENOB-pending table. `pnut_ts -d` compile is the floor gate for every code block.

### Cross-region note (handled in the reduce)
R4 (ADC→DAC passthrough) and the Tier-0 DAC→ADC loopback rig share the analog-pin/loopback
surface with the **ADC region (P2AN001 / IOSP Ch.16)** — reconcile at authoring time so the
loopback rig + analog-pin config are described once, cross-referenced, not duplicated.

## Sources mined (located + captured)

| Source | OBEX/QB | Role | Status |
|---|---|---|---|
| QB "Digital Sample ADC to DAC + Analog Frequency to DAC" (Chip Gracey, M. Mulholland) | QB | seeds R2 + R4 | **fetched** → `engineering/ingestion/external-inputs/appNote-fodder-NO-COMMIT/quickbytes/digital-sample-adc-dac/` |
| reSound (Johannes Ahlebrand) | OBEX **#2861** | primary advanced exemplar (32-stream mixer); R1/R5 seed + capstone | captured (fan-out) |
| EZ Sound (jonnymac) | OBEX #2860 | out-of-region (NCO/FREQ tones) → IOSP Ch.8 contrast | captured (fan-out) |
| QB "Simple Sound Engine Demo" (Ahle2) | QB | MOD-player capstone face (described-not-rebuilt) | optional; reSound #2861 covers it |
| `deliverables/ai/P2/` DAC mode YAMLs + IOSP Ch.10/§18.3 | KB | 🏆 primary reference (cite, don't reproduce) | in repo |

## Open questions (for authoring)

- **OQ-1 (RESOLVED — code fetched):** the QB source is now in-repo (above); R2/R4 must be
  authored + `pnut_ts -d`-verified at authoring time (untested QB code → not asserted until compiled).
- **OQ-2:** confirm the Tier-0 DAC→ADC-loopback known-answer DC check + Tier-1/2 waveform table;
  numeric audio-quality figures defer to hardware (no published SNR/THD without measurement).
- **OQ-3:** keep streamer-fed DAC as a Streamer-Guide pointer only (recommended) vs. one
  streamer-DAC recipe — authoring-time call.
- **OQ-4:** optional forward cross-ref IOSP Ch.10 → P2AN003 (+ Streamer Guide) — cross-ref pass.
- **YAML companion schema** — shares the P2AN001+P2AN002 pilot shape; **FLAG the schema before
  authoring the companion** (design-decision gate, per `APP-NOTE-DESIGN-DECISIONS.md`).
- **Corrections:** none proposed from this region (published DAC content verified consistent).

## Canonical source

Body will live in `opus-master/P2AN003.md` (+ `opus-master/front-matter.md` cover),
authored per `../APP-NOTE-CREATION-GUIDE.md` after the split is decided. Edit there;
the production workspace render is generated and overwrites edits.
