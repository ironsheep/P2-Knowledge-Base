# P2AN002 — CORDIC for Real Work — Changelog

## v1.0.0 (2026-07-03)

Initial release for community review. An application note for putting the Propeller 2's shared
hardware CORDIC solver to real work — the engine that turns a rotation, a sine, a square root, or
a full 64-bit multiply into a single queued operation with a fixed 55-clock latency. Six runnable
recipes the reader selects among — distance and heading, point rotation, circle layout, sine/cosine
waves, 64-bit-safe fixed-point scaling, and pipelining to retire one result every eight clocks —
plus a field-oriented motor-control reference ceiling. Every recipe verifies against a closed-form
answer you can derive by hand, with no bench instruments. All worked programs compile clean
under `pnut_ts`. Ships with a downloadable example library of every recipe.
