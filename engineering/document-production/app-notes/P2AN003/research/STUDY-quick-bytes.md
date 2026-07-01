# STUDY — Quick Bytes (DAC region)

Capture: `research/quick-bytes/` (catalog YAMLs, verbatim). The QB **source code** is
distributed via Parallax's `parallax-download-manager` (auth-free but interactive download
behind `parallax.com`), **not retrievable inside this container** — see open-question OQ-1.
What follows is mined from the catalog metadata + article/video descriptors + the documented
P2 DAC mechanism in the KB/IOSP. Untested QB code = open-question, not a claim.

## QB "Digital Sample ADC to DAC + Analog Frequency to DAC"
- File: `digital-sample-adc-to-dac-analog-frequency-to-dac.yaml`
- Authors: Ken Gracey (article); **code: Chip Gracey, Michael Mulholland**. Pub 2022-11-01.
  Article + video (`youtube _qPpqEd8goA`). `type: reusable-object`, tags adc-dac/audio/smart-pins.
- **Two techniques bundled:**
  1. **Digital Sample ADC → DAC** — round-trip analog: read a pin's ADC, re-emit it on a DAC
     pin (live "analog loopback"/passthrough). The DAC half is the **16-bit dither DAC**
     output stage (foundational, IOSP Ch.10 §10.4); the ADC half is the ADC region
     (P2AN001/IOSP Ch.16). The *applied* technique = a real-time sample pump (read→write loop),
     which is the streaming-DAC pattern → P2AN003.
  2. **Analog Frequency to DAC** — generate an analog signal at a chosen frequency on the DAC.
     The DAC frequency-synthesis story: either **NCO+DAC** (IOSP Ch.10 §10.5, already present)
     for fixed waveforms, or **phase-accumulator DDS feeding the dither DAC** (advanced) for
     arbitrary waveforms at arbitrary pitch → P2AN003.
- **Boundary verdict:** the DAC *modes* exercised are all foundational and **already in IOSP
  Ch.10**; the *applied* round-trip and frequency-synthesis patterns are the advanced layer →
  P2AN003 recipes. No IOSP gap surfaced. Code not in-hand (OQ-1) — recipes will be authored +
  `pnut_ts`-verified at P2AN003 authoring time, seeded by the probe.

## QB "Simple Sound Engine Demo"
- File: `simple-sound-engine-demo.yaml`. Author Ken Gracey (article); **code: Ahle2** (=
  Johannes Ahlebrand, the reSound author). Pub 2021-02-13. A **MOD/tracker player** demo
  (Protracker/`.mod` references). Same lineage as OBEX 2861 reSound — the QB is the demo face
  of that mixing engine.
- **Boundary verdict:** identical to reSound — advanced streaming/mixing/synthesis → P2AN003;
  the DAC output stage is foundational (IOSP Ch.10). Treated together with 2861 (do not
  double-count). The full tracker player is a **described-not-rebuilt** ceiling.

## QB "Simple Analog Input" (adjacent, captured for completeness)
- File: `simple-analog-input.yaml`. ADC-side — belongs to the ADC region (P2AN001 / IOSP
  Ch.16), **not** the DAC region. Captured only to document it was reviewed and routed away.

## Net
No QB surfaced a DAC *mode/configuration* fact that IOSP Ch.10 lacks. Every QB DAC technique is
either (a) a foundational mode already documented, or (b) an applied streaming/synthesis pattern
that is P2AN003's domain. The QB code bodies remain un-inspected (OQ-1); nothing here is asserted
as a verified claim beyond the catalog metadata + the KB-grounded DAC mechanism.
