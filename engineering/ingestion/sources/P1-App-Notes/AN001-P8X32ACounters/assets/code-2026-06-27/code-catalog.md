# AN001 P8X32A Counters — Companion Code Catalog

**Source:** Parallax Application Note AN001 *Propeller P8X32A Counters* v2.0 (companion example archive, downloaded from the app-note's web page `parallaxsemiconductor.com/an001`).
**Platform:** Propeller 1 (P8X32A) — Spin1 + PASM1.
**Validation status:** `code_validated: false` — **NOT compiled.** `pnut_ts` is a P2 compiler and will not build P1 Spin1/PASM1; the P1 validator (flexspin) is not installed in this container. These files are **documentary-extracted, captured verbatim, and cataloged only** (P1 charter §3). No edits, normalization, or compilation performed.

**Files captured:** 5 (verbatim copies in this folder).
**Encoding note:** `ADC.spin` and `ScalingDuty(DAC).spin` are UTF-16 encoded (Propeller Tool default for files using extended characters such as Ω, μ); the other three are ASCII. Copied byte-for-byte regardless.

| File | LOC | Counter mode demonstrated | Top object / driver | P1 dependencies (OBJ / library) |
|------|-----|---------------------------|---------------------|---------------------------------|
| `NCO.spin` | 12 | NCO single-ended `%00100` (Spin-only, sets `ctra`/`frqa`/`dira`) | Top object (standalone, no cog launch beyond setup) | none |
| `ScalingPWM.spin` | 37 | NCO `%00100` used as PWM (Spin launcher + PASM1 cog updating `phsa` via `neg phsa,value`) | Top object | none (self-contained `DAT` cog) |
| `ScalingDuty(DAC).spin` | 39 | DUTY differential `%00111` for DAC (Spin launcher + PASM1 cog updating `frqa`) | Top object | none (self-contained `DAT` cog); RC filter on APIN |
| `FrequencyCount.spin` | 41 | POSEDGE detector `%01010` for frequency counting (Spin launcher + PASM1 counter cog) | Top object | `OBJ txt : "VGA_Text"` (Propeller Tool library object) |
| `ADC.spin` | 115 | POS-detector-with-feedback `%01001` for Σ∆ ADC (Spin launcher + PASM1 sampling cog) | Top object | `OBJ txt1 : "VGA_Text"` (Propeller Tool library object) |

**External/library dependencies referenced but NOT included in the archive:**
- `VGA_Text.spin` — Propeller Tool software library object (used by `FrequencyCount.spin` and `ADC.spin` for on-screen display). The app note's Resources section states `CTR.spin` and `VGA_Text.spin` ship with the Propeller Tool library.
- `CTR.spin` — Propeller Tool library counter helper object (mentioned in Resources; not used by these 5 examples directly, which set `CTRA`/`FRQA`/`PHSA` registers manually).

**Notes on fidelity vs. the in-PDF listings:**
- The PDF body prints slightly abbreviated/edited versions of these same programs (e.g. the in-PDF NCO inline example names the method `NCO_single_ended_mode`; the companion `NCO.spin` names it `NCO_PWM_single_ended_mode`). Companion files are the downloadable authoritative code; the PDF listings are the teaching excerpts. Both captured.
- `ADC.spin` carries a richer header comment block (sample-rate table 5–14 bits, dual-counter expansion note up to 16/14 practical ADC circuits, current-sense technique) than the PDF excerpt.
- All five use the P1 `_clkmode = xtal1 + pll16x`, `_xinfreq = 5_000_000` (→ 80 MHz) clock idiom.

**P1-specific PASM1 idioms present (do NOT P2-translate blindly):** `cognew(@entry, @param)`, `waitcnt`, `rdlong/wrlong ... par`, `movs/movd/movi ctra` field-poking, `phsa`/`frqa`/`ctra` cog special registers, `|< pin` (decode/bitmask), local label `:loop`, `res` reserved longs.
