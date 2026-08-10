# P2AN002 Changelog: CORDIC for Real Work

## v1.0.2 (2026-08-08)

A licensing change. No technical content changed.

- **Licensed CC BY-SA 4.0**: share and adapt this note, including commercially, with attribution and under the same terms.


## v1.0.1 (2026-07-11)

A derivation and attribution refinement. No recipes added.

- **Step-size derivation**: the circle-layout recipe explains why the direct `$1_0000_0000 / STEPS` form won't compile (a 33-bit dividend literal) and how the halved `$8000_0000 / (STEPS / 2)` form reaches the same quotient within 32 bits.
- **OBEX attributions**: the Resources list matches the catalog: #2812 Binary Floating-Point (ersmith) and #5361 FFT/IFFT (James Smith).

## v1.0.0 (2026-07-03)

Initial release for community review. An application note for putting the Propeller 2's shared
hardware CORDIC solver to real work, the engine that turns a rotation, a sine, a square root, or
a full 64-bit multiply into a single queued operation with a fixed 55-clock latency. Six runnable
recipes the reader selects among, distance and heading, point rotation, circle layout, sine/cosine
waves, 64-bit-safe fixed-point scaling, and pipelining to retire one result every eight clocks,
plus a field-oriented motor-control reference ceiling. Every recipe verifies against a closed-form
answer you can derive by hand, with no bench instruments. All worked programs compile clean
under `pnut_ts`. Ships with a downloadable example library of every recipe.
