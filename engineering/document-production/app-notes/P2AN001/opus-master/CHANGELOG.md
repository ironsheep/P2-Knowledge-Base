# P2AN001 — Single-Pin Instrumentation ADC — Changelog

## v1.0.2 (2026-07-11)

A technical-precision pass on the ADC recipes. No recipes added.

- **Pin power domains** — the P2 powers its I/O in eight groups of eight (P0–7, P8–15, … P56–63), each group sharing one VIO/GIO pair; a multi-pin shared-node measurement stays within a single group.
- **SINC2 filtering period** — the SINC2 *filtering* mode the recipes use accepts any sample period, not only powers of two: a `WYPIN` after `WXPIN` sets any period up to about 11,585 clocks, trading sample rate for per-sample resolution.
- **Below-ground self-check** — the reading is build-dependent: the CORDIC recipe carries the sign and reads negative below ground, while the unsigned `muldiv64` recipes peg off-scale high.

## v1.0.1 (2026-07-03)

Editorial correction to the compile-status wording. No technical content changed.

## v1.0.0 (2026-07-03)

Initial release for community review. A techniques-catalog application note for reading an
absolute voltage in microvolts on a single P2 pin using only the built-in smart-pin sigma-delta
ADC — no external converter. A shared ratiometric base build (measure the chip's own GIO/VIO
references alongside the pin and take a ratio, so supply and temperature drift divide out) plus
four recipes the reader selects among — three pins for lower noise, a filter cascade for every
rate at once, a series resistor for voltages above 3.3 V, and mains-cycle averaging — and an
eight-channel reference ceiling. Every worked program compiles clean under `pnut_ts`;
resolution figures are qualitative pending hardware characterization. Ships with a downloadable
example library of every worked program.
