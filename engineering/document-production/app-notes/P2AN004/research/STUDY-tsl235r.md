# STUDY — Quick Bytes TSL235R (light-to-frequency)

**Source:** Parallax Quick Bytes "Using Smart Pins to Measure Frequency Output of
TSL235R Light-to-Frequency Sensor" — article author **Ken Gracey**; code authors
**Francis Bauer, Jon McPhalen, Chip Gracey**; published 2021-03-14.
**Captured:** QB metadata `deliverables/ai/P2/community/quick-bytes/smart-pins-tsl235r.yaml`
(verbatim in HANDBACK); KB key `p2kbCommunitySmartPinsTsl235r`.
**Role:** applied donor for the light-to-frequency sensor recipe.

## ⚠️ Source-code NOT captured
The QB entry is metadata only — the Spin2 source is behind Parallax's
**download-manager** (`download_mechanism: parallax-download-manager`,
`get_from: https://www.parallax.com/smart-pins-tsl235r/`); it is **not in this repo**
and was not retrievable by the OBEX tools (this is a Quick Byte, not an OBEX object —
`cross_links.obex_object_ids: []`). **Untested / un-captured → recorded as an
open-question, not a claim** (per the skill's discipline).

## What it does (from metadata + sensor knowledge — to be confirmed against code)
The **TSL235R** is a light-to-**frequency** converter: it outputs a 50 % square wave
whose frequency is proportional to incident irradiance. Reading it = measuring that
frequency with a smart pin and converting Hz → irradiance.

## Mechanism it relies on (KB-validated at the mode level)
- **Frequency / period counting** — any of IOSP Ch.15's modes fits: most directly
  **%10111 P_COUNTER_PERIODS** (count cycles in a fixed gate → direct Hz), or
  **%01110 P_COUNT_RISES** gated (Ch.14). KB: `p2kbArchSmartPin10111CountPeriodsInXClocks`,
  `p2kbArchSmartPin01110CountAEdgesOptionalBDec`. ✓
- IOSP Ch.15 §15.3/§15.6 already works a **1-second-gate frequency counter** — the exact
  foundation this sensor needs.

## The *applied* layer (beyond IOSP)
The **sensor application**: choosing the integration/gate window for the expected
irradiance range, and the **Hz → irradiance (µW/cm²)** conversion using the TSL235R's
output-scaling spec. IOSP shows generic Hz counting, not this sensor's applied layer.

## Delineation call
- Foundation (frequency counting) → **already in IOSP Ch.15** (+ KB), cite-not-reproduce.
- Light-sensor applied layer (gate selection + Hz→irradiance) → **advanced recipe →
  P2AN004** (R2) — **BLOCKED until the QB source is obtained + compiled.** Open question.
