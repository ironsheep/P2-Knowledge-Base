# Smart Pins (Titus) rev 5 — Mode Reference (curated, pass 1)

Curated structural summary of `Smart Pins rev 5.docx`. Raw extract: `smart-pins-titus-text.txt`.
Role: 🟡 cross-check. **Authority for bit-fields/encodings is the Silicon Doc, not this doc.**

## Document structure
1. **STANDARD I/O PINS** — DIRA/DIRB, OUTA/OUTB, INA/INB registers; the pin instruction families
   (DIR*/OUT*/FLT*/DRV* with `{#}D` span operand + ADDPINS); input instructions.
2. **Input-Output-Bit Timing** — system-clock-period timing of register transfers (3 timing figures).
3. **Smart Pins** — WRPIN/WXPIN/WYPIN/RDPIN/RQPIN/AKPIN; the WRPIN mode-control word layout
   `%AAAA_BBBB_FFF_PPPPPPPPPPPPP_TT_MMMMM_0`; then all 32 modes (%MMMMM).

## WRPIN mode-control word (as documented here)
`D/# = %AAAA_BBBB_FFF_PPPPPPPPPPPPP_TT_MMMMM_0`
- **AAAA / BBBB** — A-/B-input logic selectors (bit3=invert; low-3 select relative pin).
  ⚠️ **Titus rev5 mislabels the relative-pin values** (x101/x111 swapped) — see audit. Correct
  (Silicon Doc): `x000`=this pin, `x001..x011`=+1..+3, `x100`=this pin's OUT, `x101`=−3, `x110`=−2, `x111`=−1.
- **FFF** — pin-output filtering/logic config · **P…** — 13-bit pin config · **TT** — DIR/output control
  (`x0`=output disabled regardless of DIR, `x1`=output enabled) · **MMMMM** — the 5-bit mode.

## The 32 modes (coverage from this source)
`P`=prose ✅ all 32 · `K`=# code examples (pnut-ts-validated) · `I`=# figures.

| Mode | Name | K | I |
|------|------|---|---|
| %00000 | Smart pin off / long repository (non-DAC %00001–00011) | 0 | 0 |
| %00001 | DAC noise | 2 | 0 |
| %00010 | DAC 16-bit, pseudo-random dither | 2 | 0 |
| %00011 | DAC 16-bit, PWM dither | 1 | 1 |
| %00100 | Pulse/cycle output | 2 | 2 |
| %00101 | Transition output | 0 | 0 |
| %00110 | NCO frequency | 1 | 2 |
| %00111 | NCO duty | 1 | 1 |
| %01000 | PWM triangle | 1 | 1 |
| %01001 | PWM sawtooth | 1 | 1 |
| %01010 | PWM SMPS (V/I feedback) | **0** | 0 |
| %01011 | A/B quadrature encoder | 2 | 1 |
| %01100 | Count A-pos edges when B-high | 0 | 0 |
| %01101 | Accumulate A-edges, B inc/dec | 0 | 0 |
| %01110 | Count / up-down A-input edges | 1 | 0 |
| %01111 | Count / up-down A-input highs | 2 | 0 |
| %10000 | Time A-input states | 1 | 1 |
| %10001 | Time A-input high states | 1 | 0 |
| %10010 | Time/timeout A highs/rises/edges (Y[2]) | 1 | 3 |
| %10011 | For X periods, count time | 1 | 1 |
| %10100 | Sum pulse duration over X pulses | 0 | 0 |
| %10101 | X+ clock periods, count time | 0 | 0 |
| %10110 | X+ clock periods, count states | 0 | 0 |
| %10111 | X+ clock periods, count periods | 0 | 0 |
| %11000 | ADC sample/filter/convert, internally clocked | 0 | 0 |
| %11001 | ADC sample/filter/convert, externally clocked | 4 | 0 |
| %11010 | ADC Scope with trigger | 1 | 0 |
| %11011 | USB host/device | 0 | 0 |
| %11100 | Synchronous serial transmit | 0 | 2 |
| %11101 | Synchronous serial receive | 3 | 0 |
| %11110 | Asynchronous serial transmit | 1 | 2 |
| %11111 | Asynchronous serial receive | 1 | 0 |

**Totals:** 32/32 prose · 30 code examples (28 pnut-ts-validated + 2 conceptual fragments) · 21 figures
(18 mode-mapped + 3 I/O-timing). Modes with `K=0` rely on cross-references ("use the example shown
previously") or are flagged as needing an example (%01010 SMPS — reviewer #20).
