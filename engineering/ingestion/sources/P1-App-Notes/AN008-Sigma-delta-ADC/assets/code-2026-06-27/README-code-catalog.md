# AN008 Sigma-delta ADC — Code Catalog (in-PDF listings)

**Source:** Parallax Semiconductor Application Note **AN008 v1.0** (2011), "Sigma-delta Analog to Digital Conversion."
**Platform:** Propeller 1 / **P8X32A** — Spin1 + PASM1.
**Companion archive:** NONE shipped to this ingestion. AN008's *Resources* section references a downloadable code-archive ZIP (`www.parallaxsemiconductor.com/an008`) but no separate code folder was provided. These files are the **in-PDF listings**, transcribed verbatim from the PDF text layer.

## Validation status: NOT VALIDATED — `code_validated: false`

No P1 compiler is installed in this environment (`pnut_ts` is **P2-only**; P1 `flexspin`/`bstc` not present). Per the ingestion code rule, in-PDF P1 listings are **captured-not-processed**: transcribed and cataloged, **not compiled**. Do not treat these as compile-verified.

## Catalog

| File | Listing | Lines | Purpose | Notes |
|---|---|---|---|---|
| `Listing1-sigma-delta-adc-basic.pasm1` | Listing 1 (p.5) | ~38 | Minimal sigma-delta acquisition loop: configure CTRA (positive-w/-feedback), repeatedly sample PHSA over `interval` clocks, write result to hub via PAR. | Self-contained CON + DAT. |
| `Listing2-sigma-delta-adc-calibrated.pasm1` | Listing 2 (pp.7-8) | ~55 | Adds a **binary-search self-calibration** of `interval` against Vss/Vdd endpoints (toggling a calibration pin), with a `soak` settle delay, then offset-corrected acquisition. | Verbatim: references CON symbols (`ADC_INTERVAL0`, `ADC_RANGE`, `CALIB_PIN`, `INP_PIN`, `FB_PIN`) not re-declared in the printed listing; assumed from Listing 1's CON. Not patched. |

## Inline code fragments (in prose, not standalone listings)
- **Cog start (p.5):** `cognew(@adc_cog, @value)` — Spin1.
- **Scaling expression (p.6, Spin1):** `scaled := (raw - vlo) * RANGE / (vhi - vlo) #> 0 <# RANGE` — clips to `[0, RANGE]` via Spin1 limit operators `#>` (limit-minimum) and `<#` (limit-maximum).
- **Clamp idiom (p.7, PASM1):** `maxs acc,range` / `mins acc,#0`.

## P1 PASM1 constructs worth noting (for the downstream P1→P2 analog)
- Counter setup via `MOVI/MOVD/MOVS` into `CTRA` — packs mode (`%01001`, positive-with-feedback), feedback (dest) pin, input (src) pin.
- `FRQA = 1`, accumulate in `PHSA`; sample window timed with `WAITCNT time,interval` then `WAITCNT time,#0`.
- `SUMNC` used as the conditional add/subtract step of the binary search (P1-specific instruction).
