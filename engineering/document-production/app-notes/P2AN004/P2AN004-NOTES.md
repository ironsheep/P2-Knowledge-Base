# P2AN004 — Working Notes

**Status:** stood up 2026-06-30 — committed to production; boundary-determination pending
**Created:** 2026-06-30
**Topic:** Frequency / Period / Pulse Measurement (roster item **A2**, Smart-Pin Instrumentation family)
**Owning manual (enrichment fork):** P2 I/O & Smart Pins User Guide (IOSP)
**Campaign:** IOSP Release Campaign (`engineering/planning/IOSP-RELEASE-CAMPAIGN-PLAN.md`)

## Purpose

P2AN004 is the **timing-instrumentation** Family-A note. Per the roster
(`engineering/analysis/p2-app-note-roster.md` §A2): the smart-pin timing region
(frequency, period, duty, rctime, pulse/edge count, quadrature) has *many* modes that
are non-obvious and recurring (tachometer, frequency counter, time-of-flight). Basic
mode setup is reference (→ IOSP); the *worked instruments* become this note.

It is authored **as part of the IOSP Release Campaign**: its boundary-determination
pass decides the IOSP-vs-note split for the measurement region, and the **foundational
fork augments IOSP** before IOSP releases. Taken all the way through PDF.

## Topic — Frequency / Period / Pulse Measurement

Smart-pin measurement modes through worked recipes: frequency counting, period /
high-time / duty measurement, RC decay timing (rctime), pulse/edge counting, and
quadrature decoding — built into reusable instruments.

## The §2 playbook — boundary determination (NEXT WORK)

`candidate → examples-located → boundary-delineated → [enrichment + app-note]`

1. **Locate + download** the example sources below.
2. **Study** them.
3. **Delineate** foundational (→ IOSP measurement content) from advanced technique
   (→ this note).
4. **Fork:**
   - **IOSP-enrichment fork** — fold the foundational measurement additions into IOSP
     (the campaign's "augment IOSP content" step — *this is a release-blocking input
     to IOSP*).
   - **App-note fork** — author the advanced-technique recipes here (+ YAML companion,
     four-artifact model).

> The split is **not yet decided** — that is the next pass. Capture the decision in a
> "Boundary delineation" section here once the examples are studied.

## Sources to mine (from the roster — to locate + download)

| Source | Role | Status |
|---|---|---|
| Quick Bytes TSL235R | frequency measurement (light→freq sensor) | to locate |
| OBEX P2_rctime | RC decay / pulse timing | to locate |
| Quadrature decoder example(s) | position/velocity measurement | to locate |
| `deliverables/ai/P2/` smart-pin timing-mode YAMLs + IOSP Ch.16 | primary reference (cite, don't reproduce) | in repo |

## Open questions (resolve during boundary-determination)

- Archetype (techniques-catalog — likely) + recipe set + capstone.
- Exact IOSP measurement enrichment scope (what foundational additions IOSP wants).
- Verification model (hardware-independent known-answer vs rig-gated recipes).
- YAML companion schema — shares the P2AN001+P2AN002 pilot shape.

## Canonical source

Body will live in `opus-master/P2AN004.md` (+ `opus-master/front-matter.md` cover),
authored per `../APP-NOTE-CREATION-GUIDE.md` after the split is decided. Edit there;
the production workspace render is generated and overwrites edits.
