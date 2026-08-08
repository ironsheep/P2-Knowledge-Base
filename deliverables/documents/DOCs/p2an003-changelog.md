# P2AN003 — DAC & Analog Signal Generation — Changelog

## v1.0.2 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0** — share and adapt this note, including commercially, with attribution and under the same terms.


## v1.0.1 (2026-07-11)

A DAC precision refinement. No recipes added.

- **PWM dither tone** — the PWM-dither spectral component sits at a fixed sysclock/256, independent of the sample period, so raising the period lowers the sample rate without moving the dither tone.

## v1.0.0 (2026-07-03)

Initial release for community review. A techniques-catalog application note for generating analog
waveforms and audio on a single P2 pin using only the built-in smart-pin DAC — no external
converter. A shared output stage (a dithered 16-bit DAC paced by the pin's own sample clock) built
once as a clean, reusable base, then five recipes the reader selects among — sample playback and
waveform synthesis from a DDS phase accumulator, deliberate dither-mode and filter choice for
effective resolution, a real-time ADC-to-DAC passthrough, and multi-voice mixing with stereo
panning — plus a 32-stream reference ceiling. Every worked program compiles clean under `pnut_ts`;
audio-quality figures (signal-to-noise, distortion, effective bits) are qualitative pending hardware
characterization, with a Tier-0 known-answer DC check that proves the signal path with one jumper.
Ships with a downloadable example library of every worked program.
