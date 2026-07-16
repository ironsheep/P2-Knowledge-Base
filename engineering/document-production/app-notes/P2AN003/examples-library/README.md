# P2AN003 — Example Library

The complete, runnable source for the worked builds in **Application Note P2AN003,
"Generate Analog Waveforms and Audio on a P2 Pin."** Each file is extracted verbatim
from the opus-master so the download and the document never drift.

| File | Recipe | Demonstrates |
|---|---|---|
| `dac-sample-playback.spin2` | Recipe 1 | phase-accumulator playback of a stored sample buffer at any pitch |
| `dac-waveform-synthesis.spin2` | Recipe 2 | computed sine (CORDIC), sawtooth, and triangle from the DDS phase |
| `dac-dithering.spin2` | Recipe 3 | PRNG-vs-PWM dither choice, swept across the full 16-bit code range |
| `dac-adc-passthrough.spin2` | Recipe 4 | real-time sample pump: ADC read → DAC write, period-matched |
| `dac-mixing-panning.spin2` | Recipe 5 | three voices summed and panned to a stereo pair of DAC pins |

**The shared output stage** (configure the dithered DAC, pace it from the smart pin's
IN event) is taught once in the note and reused inside every file above — there is no
separate "base" program. The Tier-0 known-answer loopback shown in the note's Verify
section is a short DAC-drive snippet, not a separate recipe file.

**The ceiling is a reference, not a rebuild.** The full 32-stream **reSound** engine
(OBEX #2861) and a MOD/tracker player are described and linked in the note, not
reproduced here — they are scaled-up compositions of these same primitives.

**Verification.** Every file compiles clean under `pnut-ts` v1.55 (`_clkfreq =
200_000_000`). Recipes 1–5 use no `debug()`, so they build with a plain `pnut-ts
<file>`; the note's Tier-0 verify snippet uses `debug()` and needs `pnut-ts -d`. To
hear or see the output, add an RC low-pass (or a headphone/line coupling capacitor)
on the DAC pin per the note's Hardware section.

**Packaging.** At release, these files are published as `P2AN003-src.zip`
beside the PDF in `deliverables/documents/DOCs/`, with a download link in the
publication roster (per the app-note production convention — see
`../../APP-NOTE-CREATION-GUIDE.md` §6).
