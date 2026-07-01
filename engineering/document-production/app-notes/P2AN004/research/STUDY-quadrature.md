# STUDY — OBEX #2829 Quadrature Encoder (jm_quadrature)

**Source:** OBEX #2829 "Quadrature Encoder" — author **Jon "JonnyMac" McPhalen**,
created 29-JUN-2020, License **MIT**.
**Captured:** `research/2829-quadrature-encoder/` (jm_quadrature.spin2 [CR endings],
jm_quadrature_demo.zip, README.md).
**Role:** primary applied donor for the production-encoder recipe.
**Compile:** ✅ `pnut-ts` (v1.55) via a top-level harness (object is `pub null` /
not-top-level) → clean. (CR→LF conversion needed.)

## What it does
A reusable A/B quadrature-encoder driver object. Configures one smart pin in
quadrature mode, then wraps it with production niceties:
- `start(a,b,btn,d4x,preset,lo,hi)` — validates B within ±3 of A, sets the mode.
- `value()` — reads position, applies an offset (preset/zero), and **clamps to a
  lo..hi range**.
- `det4x` handling — divides the raw 4×-per-detent count down to detents.
- integrated **button debounce** (`button(delay)`), `set(preset)` zero/preset.
- `raw()` returns the un-offset count (`rdpin sar mod4x`).

## Mechanism it relies on (KB-validated)
- **Smart-pin mode %01011 P_QUADRATURE** — decodes A/B transitions to a signed 32-bit
  count; 4 counts/detent; continuous (X=0) totalizer or periodic (X>0) velocity.
  - KB: `p2kbArchSmartPin01011QuadratureEncoder` (category `smart_pins_counting`),
    incl. the `sar 2` detent divide, P_PLUS1_B routing, dual-pin position+velocity. ✓
  - IOSP: **Ch.14 §14.2** documents this mode thoroughly — position (continuous),
    velocity (periodic), dual-encoder setup, the **4×/detent `~> 2` / `sar #2`**
    signed-shift rule, P_PLUS1_B, plus a motor-position-control worked example (Ex2).
- `pinstart(apin, P_QUADRATURE | dif.[2..0]<<24, 0, 0)` — encodes the A↔B pin delta
  into the B-routing field; equivalent to IOSP's `P_PLUS1_B`/`P_MINUS1_B` constants.

## The *applied* layer (beyond IOSP)
IOSP teaches the mode + position/velocity/4×/motor-control. The donor adds the
**instrument wrapper** IOSP does not: range limiting (lo/hi clamp), preset/zero offset
bookkeeping, det4x normalization toggle, and an integrated debounced button — i.e. a
drop-in *encoder UI component*, not just the mode.

## Delineation call
- Foundation (P_QUADRATURE position/velocity/4×/routing) → **already in IOSP Ch.14.2**
  (and KB), cite-not-reproduce. IOSP coverage is *richer* than the bare donor.
- Production wrapper (limits + preset + det4x + button) → **advanced recipe → P2AN004**
  (R3): "a reusable encoder-knob instrument."
