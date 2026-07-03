# P2AN004 — Frequency / Period / Pulse Measurement — Changelog

## v1.0.0 (2026-07-03)

Initial release for community review. A techniques-catalog application note for reading real-world
sensors by timing, counting, and decoding directly on a single P2 pin — no external counter or ADC.
One shared idea (let a smart pin time or count the signal so the cog never watches an edge) applied
through three runnable instruments the reader selects among by transducer: an RC-decay reader that
times a capacitor's discharge for any resistive or capacitive sensor, a light-to-frequency reader
that turns a TSL235R's output frequency into an irradiance with a reciprocal frequency counter, and
a drop-in quadrature-knob instrument with detent normalization, preset, range clamp, and a debounced
button. Every worked program compiles clean under `pnut_ts`; the encoder recipe self-verifies on a
bare board with two jumper wires and a known-answer detent count, while the analog recipes' absolute
calibration defers to a hardware pass and carries no invented readings. Circuit schematics (RC-decay
network, TSL235R hookup) and a quadrature timing diagram are rendered inline. Ships with a
downloadable example library of every worked program.
