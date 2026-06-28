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
| SINC2-manual mode + diff computation | `p2kbArchSmartPin11000AdcInternalClock` (KB) | KB ✓ / re-cert pending |
| GIO/VIO/pin ratiometric µV math | forum (cgracey) — `research/.../STUDY` §B2 | NOT verified (compile-cert pending) |
| 3-sample SINC2 flush on source switch | forum (cgracey/evanh) — STUDY §A4 | NOT verified |
| 15 mV absolute-error limit (resistor mismatch) | forum (cgracey, designer) — STUDY §A6 | designer-stated; not re-measured |
| _(more as drafted)_ | | |

## Open questions (for the note + for Stephen)

- Confirm topic = instrumentation ADC, and confirm **scope**: single-pin only, or include the
  3-pin / 8-pin progression? (See report.)
- Legal-clock target (note must use ≤300 MHz, not Chip's 320 MHz).
- ENOB framing — what do we claim? Chip's numbers are bench/rig, not guaranteed (STUDY §6).
- Reconcile Silicon-Doc ENOB-doubling wording + input-impedance figure vs forum (STUDY §5) →
  possible `P2KB-CORRECTION-FINDINGS.md` items.

## Canonical source

The note's markdown will live in `opus-master/P2AN000.md`. Edit there; the production
workspace render is generated and overwrites edits.
