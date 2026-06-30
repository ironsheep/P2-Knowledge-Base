# P2AN003 — Working Notes

**Status:** stood up 2026-06-30 — committed to production; boundary-determination pending
**Created:** 2026-06-30
**Topic:** DAC & Analog Signal Generation (roster item **A1**, Smart-Pin Instrumentation family)
**Owning manual (enrichment fork):** P2 I/O & Smart Pins User Guide (IOSP)
**Campaign:** IOSP Release Campaign (`engineering/planning/IOSP-RELEASE-CAMPAIGN-PLAN.md`)

## Purpose

P2AN003 is the **output sibling to P2AN001 (ADC)** and the second Family-A
(Smart-Pin Instrumentation) note. Per the roster
(`engineering/analysis/p2-app-note-roster.md` §A1): the *basic* DAC smart-pin modes
are reference (→ IOSP); the *advanced worked technique* — dithering, audio/waveform
streaming, signal synthesis — is taught nowhere and becomes this note.

It is authored **as part of the IOSP Release Campaign**: its boundary-determination
pass decides the IOSP-vs-note split for the DAC region, and the **foundational fork
augments IOSP** before IOSP releases. Taken all the way through PDF.

## Topic — DAC & Analog Signal Generation

The P2's DAC capabilities through worked recipes: DAC output modes, dithering for
effective resolution, streaming waveforms (DDS / sample playback), and analog signal
synthesis. The *output* counterpart to the ADC instrumentation note.

## The §2 playbook — boundary determination (NEXT WORK)

`candidate → examples-located → boundary-delineated → [enrichment + app-note]`

1. **Locate + download** the example sources below.
2. **Study** them.
3. **Delineate** foundational (→ IOSP DAC content) from advanced technique (→ this note).
4. **Fork:**
   - **IOSP-enrichment fork** — fold the foundational DAC additions into IOSP
     (the campaign's "augment IOSP content" step — *this is a release-blocking
     input to IOSP*).
   - **App-note fork** — author the advanced-technique recipes here (+ YAML companion,
     four-artifact model).

> The split is **not yet decided** — that is the next pass. Capture the decision in a
> "Boundary delineation" section here (mirror P2AN002-NOTES §"Boundary delineation")
> once the examples are studied.

## Sources to mine (from the roster — to locate + download)

| Source | Role | Status |
|---|---|---|
| Quick Bytes "ADC→DAC" | round-trip analog | to locate |
| Quick Bytes "Analog Frequency to DAC" | frequency→analog | to locate |
| Sound-engine OBEX object(s) | audio streaming / waveform synth | to locate |
| `deliverables/ai/P2/` smart-pin DAC YAMLs + IOSP Ch.16 | primary reference (cite, don't reproduce) | in repo |

## Open questions (resolve during boundary-determination)

- Archetype (techniques-catalog, like P2AN001/002 — likely) + recipe set + capstone.
- Exact IOSP DAC enrichment scope (what foundational additions IOSP wants).
- Verification model (which recipes are hardware-independent vs rig-gated, like the
  ADC ENOB-pending table).
- YAML companion schema — shares the P2AN001+P2AN002 pilot shape.

## Canonical source

Body will live in `opus-master/P2AN003.md` (+ `opus-master/front-matter.md` cover),
authored per `../APP-NOTE-CREATION-GUIDE.md` after the split is decided. Edit there;
the production workspace render is generated and overwrites edits.
