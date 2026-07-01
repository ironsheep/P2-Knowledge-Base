# STUDY — OBEX #2831 P2_rctime (RC-decay timing)

**Source:** OBEX #2831 "P2_rctime" — author **phonoclese**, created 19-JUL-2023, License **MIT**.
**Captured:** `research/2831-p2-rctime/` (P2_rctime.spin2 [UTF-16/CRLF], README.md).
**Role:** primary applied donor for the RC-decay sensor recipe.
**Compile:** ✅ `pnut-ts -d` (v1.55, UTF-8 conversion) → `P2_rctime_u8.bin` clean.

## What it does
Ports the P1-library `rctime` idiom to P2. Charges a capacitor through a resistor
(I/O pin drives high, ~220 Ω + C network), then floats the pin and **times how long
the node stays above the Schmitt threshold** as the cap discharges through the sensor
resistance. The discharge time ∝ R·C, so the clock count is the sensor reading
(classic resistive/capacitive-sensor measurement: CdS photocell, thermistor, pot, etc.).

## Mechanism it relies on (KB-validated)
- **Smart-pin mode %10001 P_HIGH_TICKS** ("Time A-input high states") — the smart pin
  counts system clocks while the (Schmitt-conditioned) input is high; on the
  high→low transition it latches the count and raises IN.
  - KB: `p2kbArchSmartPin10001TimeAHighs` (category `smart_pins_timing`). ✓
  - IOSP: **Ch.13 §13.3** documents this mode fully (function, registers, masking,
    P_SCHMITT_A / P_INVERT_A modifiers, worked pulse/servo/ultrasonic examples).
- Pin config: `P_HIGH_TICKS | P_SCHMITT_A | P_OE | P_LOW_FLOAT`. Schmitt trigger gives
  the clean threshold crossing the RC ramp needs. (All these modifiers are in IOSP
  Ch.3/Ch.13.)

## The *applied* layer (beyond IOSP)
1. **The charge→float→time-discharge instrument cycle** itself — drive high to charge,
   `addct1`/`waitct1` a fixed charge delay (5 ms here), float, then read the high-time
   count. IOSP teaches the *mode*; it does not work this resistive-sensor cycle.
2. **Background terminate-stay-resident (TSR) pattern** — a small PASM ISR is loaded
   via `REGEXEC` into high cogRAM (`org $1B0`), arms `SETSE1`/`SETINT1` on the pin
   IN-rise event, and from then on services each measurement in the **background of the
   Spin2 interpreter** (`reti1`), continuously updating a hub long. This is an advanced
   cog-resident technique — a **ceiling**, candidate described-not-rebuilt.

## Delineation call
- Foundation (P_HIGH_TICKS timing) → **already in IOSP Ch.13.3**, cite-not-reproduce.
- RC-sensor instrument cycle → **advanced recipe → P2AN004** (R1).
- REGEXEC background-ISR TSR mechanism → **described-not-rebuilt ceiling**; recipe
  should ship a simpler *polled* version and link the TSR object as the ceiling.
