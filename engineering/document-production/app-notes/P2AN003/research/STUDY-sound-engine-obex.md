# STUDY — Sound-engine OBEX objects (DAC region)

Region: DAC & Analog Signal Generation · owning manual IOSP · app-note fork P2AN003.
Capture: `research/sound-engine-obex/`. KB validated FIRST, code is applied evidence.

## OBEX 2861 — reSound (Johannes Ahlebrand, MIT-style/OBEX license) — PRIMARY exemplar
- **What it does:** single-cog software audio mixer. Mixes **up to 32 input streams**,
  per-channel **volume, panning, frequency (pitch), and sample format** (signed/unsigned,
  8/16-bit), to **1–8 analog output pins** (mono / stereo / up to 8-pin surround), CD-quality.
  Demos: `reSound_sample_demo.zip`, `reSound_music_demo.zip` (MOD-style music).
- **Output stage (mechanism — `reSound.spin2`):** configures the **16-bit dithered DAC
  smart-pin modes** and pushes each mixed sample with `wypin`:
  - CON block lines 21–33: builds mode words from the documented fields — `M[12:10]=%101`
    DAC enable (`DIR_ENABLE_OUTPUT`), the four resistor configs (990R/600R/123R/75R), and
    `DAC_16BIT_PWM_DITHER` / `DAC_16BIT_NOISE_DITHER` / `DAC_8BIT_NOISE`. (Note: reSound's
    two `_DITHER` *comments* are swapped vs the mode bits; the **bit values** `%00010`/`%00011`
    are correct and match the KB — a source comment quirk, not a fact conflict.)
  - `initExplicit` (line 128–135): if `forceHq`, masks the sample period to a **multiple of
    256** to qualify for the **HQ PWM-dither** mode; else falls back to PRNG dither. This is
    exactly the IOSP Ch.10 / KB `%00011` constraint "X[15:0] must be a multiple of 256."
  - PASM cog `RESOUND` (line 459+): `wrpin smartpinConfig` / `wxpin samplePeriod` to set up
    each pin (lines 502/504); the steady-state `mainLoop` emits the mixed sample to up to 8
    pins via `wypin outSample+N, pinDefinitions+N` (lines 679–693). `rdfast` (lines 461/540)
    is used for fast **hub** reads of config + sample buffers, **not** streamer DAC output.
- **Advanced layer (taught nowhere → P2AN003):** the **software DDS/resampling** —
  phase-accumulator per channel (`encod`, per-input shift amount = `33 - encod(maxBufferSize)`,
  lines 185–199) drives sample-buffer playback at an arbitrary pitch decoupled from the DAC
  sample rate; multi-channel summing/mixing; volume + panning; multi-pin surround fan-out;
  the mixing-frequency-vs-DAC-sample-period relationship. None of this is DAC *mode* mechanics.
- **Foundational layer (all already in IOSP Ch.10 / KB):** the dithered DAC modes themselves,
  the four resistor configs, `M[12:10]=%101`, OE, the WXPIN-period / WYPIN-value / IN-flag
  sync. reSound *uses* these as primitives; it does not teach anything new about them.
- **Boundary verdict:** reSound is a pure **advanced-technique** exemplar. Too large to rebuild
  (955 lines, full engine) → **described-not-rebuilt capstone** (parallels P2AN001 8-pin
  interpreter, P2AN002 Park/FOC). Its *decomposable primitive* (single-channel DDS playback →
  dither DAC) is the seed for the P2AN003 streaming/synthesis recipes.

## OBEX 2860 — EZ Sound (Jon "jonnymac" McPhalen, MIT) — CONTRAST, not DAC
- **What it does:** beeps/boops and monotonic tunes through a piezo; BASIC-Stamp-style
  `SOUND`/`FREQOUT`/`play_tune`, with a full musical-note frequency table.
- **Mechanism (`jm_ez_sound.spin2` line 82):** `pinstart(pin, P_NCO_FREQ | P_OE, 10, fr01 frac
  clkfreq)` — this is the **NCO frequency** smart-pin mode (`%00110`), a *square-wave tone*
  generator. **It does not use the DAC at all.**
- **Boundary verdict:** **out of the DAC region.** It is the "simple tones" floor and its
  mechanism is foundational NCO-frequency output → **already covered by IOSP Ch.8 (NCO
  Frequency)**. Record only as a cross-reference contrast: "for simple beeps you don't need
  the DAC — NCO/FREQ (Ch.8) drives a piezo directly." No DAC enrichment, no P2AN003 recipe.

## Buildability probe (advanced-fork primitive)
`research/probe-dds-dac.spin2` — minimal single-pin DDS (phase accumulator → CORDIC `QSIN` →
16-bit PWM-dither DAC, IN-flag synced) → **compiles clean, `pnut-ts v1.55`** (`probe-dds-dac.bin`,
6372 B; binary removed after verify). Proves the P2AN003 streaming/synthesis recipe layer is
buildable from documented primitives — the recipes are not speculative.
