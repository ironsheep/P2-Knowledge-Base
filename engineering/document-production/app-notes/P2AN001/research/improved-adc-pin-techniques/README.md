# Research capture — "Improved ADC Pin Techniques" (Parallax forum)

Local study material for **P2AN001** (P2 instrumentation-ADC app note). Gathered 2026-06-27
from https://forums.parallax.com/discussion/175609/improved-adc-pin-techniques (4 pages).

## Read this first
- **`STUDY-improved-adc-pin-techniques.md`** — the analysis: speaker-credibility map, content
  classified by *driving the chip* (Axis A) vs *broader sampling technique* (Axis B), the code
  hunt result, KB reconciliation, open questions, and how it maps onto the app note.

## Raw captures (verbatim)
- `thread-p1.md … thread-p4.md` — every post, verbatim, attribution preserved.
  - p1–p2 = the core ADC investigation (Chip + evanh + Tubular + Christof + TonyB_).
  - p3 = the advanced code drops (incl. EightPinADC) then drift toward motor use case.
  - p4 = BLDC/PMSM motor theory tangent (not ADC — captured for completeness).

## Code (verbatim attachments) — `code/`
| File | Source post | What |
|---|---|---|
| `OnePinADC.spin2` | p1.28 | Single-pin instrumentation ADC (cleanest teaching base) |
| `ThreePinADC.spin2` | p1.24 | 3-pin constant-impedance, 3× accuracy |
| `ThreePinADC_SampleFiltering-4.9K.spin2` | p3.4 | + N-stage time-halving filter |
| `ThreePinADC_SampleFiltering-8K.spin2` | p3.15 | Chip's working file w/ idea-comments (PNut_v43) |
| `EightPinADC.spin2` | p3.17 | **8 pins via PASM2 bytecode interpreter — the advanced ADC** |
| `trapezoid-adc/` | p3.21 | SaucySoliton's trapezoid-window SINC3 alternative |
| `P2_ADC_Schematic.pdf` | p3.1 | Chip-released P2 ADC front-end schematic |

## Provenance / fidelity
- Pages + code fetched 2026-06-27. Forum blocks bare `curl` (403); pages via WebFetch,
  code via `curl` with full browser headers (Referer = the discussion URL). Code files are
  byte-exact (sizes match forum). Inline waveform/FFT images were NOT captured (placeholders
  noted in the page files); the schematic PDF was.
- **Not yet `pnut_ts`-validated by us.** Every example we publish must be compile-certified
  and brought to a datasheet-legal clock (≤300 MHz). See STUDY §4 caveats.
