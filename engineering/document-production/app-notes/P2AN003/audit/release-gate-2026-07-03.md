# P2AN003 — Release-Gate Deep Audit (2026-07-03)

**Doc:** P2AN003 "DAC & Analog Signal Generation" (Generate Analog Waveforms and Audio on a P2 Pin)
**For:** v1.0.0 first release
**Verdict:** **GO** — 1 HIGH defect found and FIXED (Recipe 4 scaling); all other claims CONFIRMED.

## Method

Exhaustive fan-out (4 independent verification agents, each on a distinct claim cluster)
against the authoritative P2KB (p2kb-mcp), the Silicon Doc v35 ingestion extracts, the IOSP
opus-master (companion manual), P2AN001/P2AN002 (consistency anchors), the OBEX MCP, and live
`pnut-ts` v1.55 compilation. Every agent finding was **hand-verified** before action (fan-out
findings can invert). All 6 code programs compile (`-d` where they use `debug()`); the doc's 5
recipe blocks are verbatim-identical to the `examples-library/` files (drift check = 1.000).

## Findings

### HIGH — Recipe 4 (ADC→DAC passthrough) `shl smp, #8` scaling railed the DAC — FIXED
The passthrough scaled the SINC2 differential with `shl smp, #8` and a mental model of a small
"count." A **256-clock SINC2 _filtering_** differential is already **full-scale 16-bit** (raw
width = 2·log2(N); N=256 → 16 bits — from IOSP §16.3 normalization "right-shift LOG2(N)−1 to
right-justify" + the IOSP resolution table 128 clocks→8-bit). Multiplying an already-16-bit
value by 256 overflowed every period, firing the `if_a mov smp,##$FFFF` clamp → the DAC railed
to full scale instead of reconstructing the input. The bad scaling was P2AN003's own invention;
P2AN001 (hardware-verified) sidesteps absolute scaling by reading ratiometrically.
**Fix (opus-master + examples-library, recompiled clean):** drop `shl smp,#8` — the raw 27-bit
modular differential drives the DAC directly; corrected the "How this works" prose accordingly.

### LOW — Recipe 4 first-period warm-up not discarded — FIXED (bundled)
`last` initialized to 0 → first `sub` yielded garbage (one railed period) before self-correcting.
IOSP §16.3: a SINC2 difference is valid only from the 2nd period. **Fix:** prime the differencer
with one discarded `waitse1`/`rdpin last` before the loop.

### CONFIRMED (no defect)
- **DAC mechanism (12/12):** 8-bit DAC dithered to nominal 16-bit; `P_DAC_DITHER_PWM`=%00011 /
  `P_DAC_DITHER_RND`=%00010 / DAC-noise %00001; four output configs (990R_3V/600R_2V/124R_3V/
  75R_2V) + 3.3 V/2.0 V pairings; PWM ×256 constraint; PRNG X=1; voltage math V=(code/65536)×Vfs
  ($8000→1.65 V, $4000→0.825 V). The **Fclock/256 @ −48 dB** figure is SOURCED verbatim in the
  Silicon Doc (part4-smart-pins) + Titus — not a fabrication. All IOSP cross-refs (Ch.10, §18.3,
  §10.1–10.2, §10.4, §10.7/§10.10, Ch.8 NCO, Ch.16 ADC) resolve correctly.
- **Spin2/CORDIC/PASM2 (9/9):** QSIN(len,angle,period), `frac`=(x<<32)/y, MULDIV64=a·b/c,
  QROTATE→GETQY=sin/GETQX=cos (matches P2AN002), SETSE1 %001=IN-rising, sawtooth/triangle fold,
  signed→offset-binary +$8000, zerox #26. **FGES/FLES are integer signed-limit (Force ≥/≤ Signed),
  NOT floating-point** — Recipe 5's clamp to ±$7FFF is correct.
- **Recipe 4 ADC config (headline):** `wxpin #%01_1000` = SINC2 filtering (X[5:4]=%01) + 2⁸=256
  clocks (X[3:0]=8) is CORRECT and consistent with the hardware-verified P2AN001 (%01_0111=128
  clocks); the software differential matches P2AN001's read; ADC/DAC periods both 256, matched.
- **Attributions/OBEX (7/7):** reSound = OBEX #2861, Johannes Ahlebrand (verified in source
  copyright header), 955 lines, 32-stream/1–8-pin claims correct; EZ Sound = OBEX #2860 (jonnymac),
  NCO/FREQ not DAC; Mulholland+Gracey demo credits traceable; v35 / Datasheet version strings
  consistent with the series. All name uses are legitimate authorship/provenance credits.

## Gates
- `pnut-ts -d` compile: all 6 programs clean (5 recipes + Tier-0). ✓
- Code-line-length K=76: clean. ✓  Inline-code ASCII: clean. ✓  U+FE0F: none. ✓
- Red-flag prose sweep: none. ✓
- Drain gate (P2KB-CORRECTION-FINDINGS, DAC/audio domain): GREEN — F-175 (IN-flag mask) and
  G-003 (DAC 16-bit ENOB caveat) both DONE; P2AN003 uses the correct SETSE1/WAITSE1 idiom and
  prints no ENOB figure (defers to hardware). ✓
- Doc↔examples-library drift: verbatim (1.000). ✓
