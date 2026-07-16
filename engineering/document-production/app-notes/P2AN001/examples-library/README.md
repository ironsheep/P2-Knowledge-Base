# P2AN001 — Example Library

The complete, runnable source for the worked builds in **Application Note P2AN001,
"Measure an Absolute Voltage in Microvolts on a P2 Pin."** Each file is extracted
verbatim from the opus-master so the download and the document never drift.

| File | Recipe | Demonstrates |
|---|---|---|
| `adc-single-pin-base.spin2` | Recipe 1 (base build) | single-pin absolute-µV instrumentation ADC |
| `adc-three-pin.spin2` | Recipe 2 | three pins, constant impedance, 3× the data |
| `adc-filter-cascade.spin2` | Recipe 3 | time-halving filter cascade (every rate at once, CORDIC divide) |

**Recipes 4 and 5 are base-build modifications**, not separate programs — Recipe 4
(range extension) changes only the divider constants + one scaling line, and Recipe
5 (mains averaging) changes only how `SUMS` is computed. The note shows the exact
deltas; apply them to `adc-single-pin-base.spin2`. The eight-channel capstone is a
*reference* design (described, not rebuilt — see the note).

**Verification.** Every file compiles clean under `pnut-ts -d` (v1.55, `_clkfreq =
200_000_000`). Build with DEBUG enabled (`-d`) so the `debug()` `SCOPE` window
appears, and jumper the DAC pin to the ADC pin per the note. The expected reading is
~1,650,000 µV (the loopback half-scale); see the note's Verify steps.

**Packaging.** At release, these files are published as `P2AN001-src.zip`
beside the PDF in `deliverables/documents/DOCs/`, with a download link in the
publication roster (per the app-note production convention — see
`../../APP-NOTE-CREATION-GUIDE.md` §6).
