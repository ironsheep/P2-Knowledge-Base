# P2AN001 — Single-Pin Instrumentation ADC — Changelog

## v1.0.0 (2026-07-03)

Initial release for community review. A techniques-catalog application note for reading an
absolute voltage in microvolts on a single P2 pin using only the built-in smart-pin sigma-delta
ADC — no external converter. A shared ratiometric base build (measure the chip's own GIO/VIO
references alongside the pin and take a ratio, so supply and temperature drift divide out) plus
four recipes the reader selects among — three pins for lower noise, a filter cascade for every
rate at once, a series resistor for voltages above 3.3 V, and mains-cycle averaging — and an
eight-channel reference ceiling. Every worked program compiles under `pnut_ts` at 200 MHz;
resolution figures are qualitative pending hardware characterization. Ships with a downloadable
example library of every worked program.
