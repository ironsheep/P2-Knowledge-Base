# P2AN000 — Working Notes

**Status:** topic-pending (experimental first note)
**Created:** 2026-06-27

## Purpose

P2AN000 is the **first experiment** in the P2 application-note series — the note that
shakes out the structure (`../APP-NOTE-CREATION-GUIDE.md`) and voice
(`../APP-NOTE-VOICE-GUIDE.md`) before the series numbering is settled. The `000` number
is deliberate: it marks "not yet placed in the published sequence." When the topic and
published number are fixed, this folder is renamed (e.g. `P2AN007-smart-pin-pwm/`) and the
front-matter updated.

## Topic — emerging: P2 instrumentation ADC (single-pin absolute voltage)

Stephen's research feed (2026-06-27) points the experiment at the **smart-pin instrumentation
ADC**: reading an *absolute* voltage in microvolts on a P2 pin with no external ADC, using
the GIO/VIO/pin three-source rotation + SINC2-manual LSB accumulation. Aligns with the P1
lineage candidate (← AN008 Sigma-Delta ADC) and the smart-pin (← AN001) recreation.
**Topic not yet formally confirmed by Stephen** — awaiting his go-ahead before drafting.

Research is gathered + studied under `research/improved-adc-pin-techniques/` (Chip Gracey's
4-page forum thread, verbatim posts + 7 code attachments + schematic; see that folder's
`STUDY-…md`). The advanced "8 ADC pins via bytecode interpreter" source Stephen was hunting
for IS captured: `research/improved-adc-pin-techniques/code/EightPinADC.spin2`.

## Source traceability (fill as the note is built)

| Claim / number / code | Source (EF ledger / P2KB key / pnut_ts / silicon) | Verified |
|---|---|---|
| SINC2-manual mode + diff computation | `p2kbArchSmartPin11000AdcInternalClock` (KB) | KB ✓ / compile ✓ (pnut_ts 1.55, 200 MHz, `-d`) — hardware pending |
| GIO/VIO/pin ratiometric µV math (`muldiv64`) | IOSP Ch.16 §16.3 + forum (cgracey) STUDY §B2 | compile ✓ (P2AN000 base build) — hardware pending |
| 3-sample SINC2 flush on source switch | forum (cgracey/evanh) — STUDY §A4 | encoded in base-build `measure` routine; compile ✓ — hardware pending |
| 15 mV absolute-error limit (resistor mismatch) | forum (cgracey, designer) — STUDY §A6 | designer-stated; not re-measured |
| _(more as drafted)_ | | |

## Open questions (for the note + for Stephen)

- Confirm topic = instrumentation ADC, and confirm **scope**: single-pin only, or include the
  3-pin / 8-pin progression? (See report.)
- Legal-clock target (note must use ≤300 MHz, not Chip's 320 MHz).
- ENOB framing — what do we claim? Chip's numbers are bench/rig, not guaranteed (STUDY §6).
  **Resolved:** claim *mechanism* qualitatively; defer every ENOB number to the measurement-table
  stub below (Hardware-measurement readiness), filled from a Tier-1 rig run.
- Reconcile Silicon-Doc ENOB-doubling wording + input-impedance figure vs forum (STUDY §5) →
  possible `P2KB-CORRECTION-FINDINGS.md` items.

## Hardware-measurement readiness (qualitative now, numbers later)

The note ships with **qualitative** ceiling claims — mechanism, not measured ENOB. Stephen will
run the recipes on a bench rig to upgrade them to measured numbers; once accepted, those numbers
become **empirical** (top of the trust chain — replicate to the EF ledger per CLAUDE.md). This
section specs the rig + procedure now so the data slots in cleanly later.

### Rig tiers

| Tier | Equipment | What it proves |
|---|---|---|
| **Tier 0 — functional** | P2 Edge board + one jumper (DAC pin → ADC pin loopback) | The build runs: a DAC-driven known on-chip voltage, and the µV reading tracks it. No external gear — proves the *code*, not the accuracy. |
| **Tier 1 — absolute / ENOB** | Precision voltage reference + 6.5-digit DMM (truth) + 0.1% resistors + LDO-fed VIO | Absolute-voltage error vs the DMM; noise floor and ENOB per technique/clock. The numbers that fill the table below. |
| **Tier 2 — applied sources** | Low-µV source (thermistor bridge / precision divider) + analog mux (for the SaucySoliton multi-source / motor variant) | The recipes against real transducer signals; range-extension + mains-averaging in situ. |

### Measurement-table stub (fill from Tier 1)

Each row is a published **qualitative** claim awaiting a measured ENOB. Until a number lands, the
note cites the *mechanism* only — every qualitative claim in the note maps to one row here.

| Technique (recipe) | Clock | Sample rate | Integration window | Measured ENOB | Status |
|---|---|---|---|---|---|
| 1 · single-pin absolute µV | 200 MHz | TBD | TBD | — | qualitative pending hardware |
| 2 · 3-pin constant-impedance ×3 | 200 MHz | TBD | TBD | — | qualitative pending hardware |
| 3 · N-stage time-halving filter | 200 MHz | per-stage | per-stage | — | qualitative pending hardware |
| 4 · range extension (series R) | 200 MHz | TBD | TBD | — | qualitative pending hardware |
| 5 · mains-cycle averaging | 200 MHz | TBD | one mains cycle | — | qualitative pending hardware |
| capstone · 8-pin bytecode (reference only) | — | — | — | — | not benchmarked (described, not built here) |

### Per-recipe test procedure (apply → read → compare)

| Recipe | Apply | Read | Expected (qualitative) | Measured (Tier 1) |
|---|---|---|---|---|
| 1 single-pin | DAC-loopback a known voltage (Tier 0), then a precision reference (Tier 1); also drive the pin to GND | DEBUG SCOPE µV from `read_microvolts()` | tracks the applied voltage; ~0 when driven to GND; negative below GIO, over-range above VIO | absolute error vs DMM; noise band |
| 2 3-pin | same references, 3 pins tied to the node | per-source accumulators → µV | ~3× lower noise than recipe 1 at equal time | ENOB delta vs recipe 1 |
| 3 N-stage filter | steady reference | each filter-stage output | higher stages = lower rate, more resolution; consumer picks the stage | ENOB per stage |
| 4 range extension | a voltage beyond 3.3 V through the matched series R | µV scaled by the external divider | reads the divided value; tempco-matched R holds across temperature | absolute error + tempco drift |
| 5 mains averaging | a signal with deliberate 50/60 Hz pickup | µV averaged over exactly one mains cycle | AC pickup nulled; noise drops sharply vs un-averaged | residual ripple |

**Self-check baked into every recipe:** drive the measured pin to GND and confirm the reading
collapses toward 0 µV — the cheap, no-instrument sanity test the note's Verify step uses.

## Canonical source

The note's markdown will live in `opus-master/P2AN000.md`. Edit there; the production
workspace render is generated and overwrites edits.
