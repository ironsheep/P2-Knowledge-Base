# P2AN001 Changelog: Single-Pin Instrumentation ADC

## v1.0.4 (2026-08-16)

**The pin power domain a measurement actually references.** No recipes added.

### Changed

- **I/O power domains are isolated groups of four** — P0–3, P4–7, … P60–63 — each sharing the one VIO/GIO pair its ADC references
- **A shared-node multi-pin measurement stays inside one group**; Recipe 2's pins 32–35 are exactly one
- **Why the boards suggest eight** (Pitfalls): one Edge 3.3 V regulator feeds *two* four-pin domains, which reach the die through separate VIO pins
- **The eight-pin figure is for current budgeting** on an Edge — 300 mA per header group — not for choosing which pins share a reference
- **The error floor names its source**: the ~15 mV pin-to-pin figure is the P2 designer's, marked as a designer-stated figure rather than a characterized specification
- **The §16.8 pointer** goes to what that section carries: the front-end limits and the calibration guidance
- **The three programs in `P2AN001-src.zip`** are byte-identical to the code blocks printed in the note, and compile clean under `pnut-ts -d`

## v1.0.3 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this note, including commercially, with attribution and under the same terms.


## v1.0.2 (2026-07-11)

A technical-precision pass on the ADC recipes. No recipes added.

- **Pin power domains**: I/O power-domain grouping and its effect on a multi-pin shared-node measurement, which stays within a single group. (The group size stated in this release was wrong; it is corrected in v1.0.4.)
- **SINC2 filtering period**: the SINC2 *filtering* mode the recipes use accepts any sample period, not only powers of two; a `WYPIN` after `WXPIN` sets any period up to about 11,585 clocks, trading sample rate for per-sample resolution.
- **Below-ground self-check**: the reading is build-dependent, so the CORDIC recipe carries the sign and reads negative below ground, while the unsigned `muldiv64` recipes peg off-scale high.

## v1.0.1 (2026-07-03)

Editorial correction to the compile-status wording. No technical content changed.

## v1.0.0 (2026-07-03)

Initial release for community review. A techniques-catalog application note for reading an
absolute voltage in microvolts on a single P2 pin using only the built-in smart-pin sigma-delta
ADC, no external converter. A shared ratiometric base build (measure the chip's own GIO/VIO
references alongside the pin and take a ratio, so supply and temperature drift divide out) plus
four recipes the reader selects among, three pins for lower noise, a filter cascade for every
rate at once, a series resistor for voltages above 3.3 V, and mains-cycle averaging, and an
eight-channel reference ceiling. Every worked program compiles clean under `pnut-ts`;
resolution figures are qualitative pending hardware characterization. Ships with a downloadable
example library of every worked program.
