# P2AN004 — Working Notes

**Status:** boundary DECIDED 2026-06-30 (mine-and-delineate fan-out, IOSP campaign §1c); ready for authoring (§3b)
**Created:** 2026-06-30
**Topic:** Frequency / Period / Pulse Measurement (roster item **A2**, Smart-Pin Instrumentation family)
**Owning manual (enrichment fork):** P2 I/O & Smart Pins User Guide (IOSP)
**Campaign:** IOSP Release Campaign (`engineering/planning/IOSP-RELEASE-CAMPAIGN-SPRINT-PLAN.md`)

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

## Boundary delineation (DECIDED 2026-06-30)

Outcome of the `mine-and-delineate` fan-out (IOSP campaign §1c). **This region mirrors
P2AN002/CORDIC: the foundational fork is EMPTY (IOSP already covers every measurement mode);
the advanced fork narrows to three sensor-class instruments** (Stephen's scope call, below).

### Foundational → IOSP : **EMPTY (no fork)**
IOSP **Ch.13 (time measurement)**, **Ch.14 (counting/quadrature)**, and **Ch.15 (frequency/
period)** already document every measurement mode the donors rely on — registers, formulas,
modifiers, and worked examples. **Cite, don't reproduce.** Mode→location map (the app note links
these; IOSP gains no new content): %10000 P_STATE_TICKS §13.2 · %10001 P_HIGH_TICKS §13.3 ·
%10010 P_EVENTS_TICKS §13.4 · %10011–%10111 period/count modes §15.2–§15.3 · %01011 P_QUADRATURE
§14.2 · %01100–%01111 counting §14.3–§14.6.
- *Deferred courtesy backlink (NOT a content gap):* when P2AN004 ships, add a one-line
  "complete worked instrument → P2AN004" back-pointer in §13.3 / §14.2 / §15.3 — handled at
  P2AN004 release, not now.

### Scope decision (Stephen, 2026-06-30) — **narrow P2AN004 to the sensor-class instruments**
The fan-out surfaced a **scope collision:** IOSP **already works** the instruments the roster had
pencilled in for P2AN004 — frequency counter (Ch.15 Ex1), RPM/tachometer (Ch.14 Ex4 + Ch.15 Ex2),
ultrasonic time-of-flight (Ch.13 Ex2). To avoid duplicating IOSP, **P2AN004 is narrowed to the
three sensor-class recipes R1–R3** (none worked in IOSP); IOSP keeps its existing worked
instruments. P2AN004's distinct value = reading real transducers.

### Advanced → P2AN004 : **R1–R3** — archetype **techniques-catalog**
| # | recipe / technique | foundation (cited in IOSP) | donor | status |
|---|---|---|---|---|
| R1 | **RC-decay resistive/capacitive sensor reader ("rctime")** — charge → float → time discharge to Schmitt threshold → R·C reading (CdS / thermistor / pot); ship the **polled** form | P_HIGH_TICKS, Ch.13.3 | OBEX **#2831** P2_rctime | compiles `-d` ✓ |
| R2 | **Light-to-frequency sensor reader (TSL235R)** — gate-window selection + Hz→irradiance (µW/cm²) | period/freq counting, Ch.15.3 | QB TSL235R | code fetched (compile at authoring) |
| R3 | **Production quadrature-encoder instrument** — range clamp + preset/zero + det4x + debounced button (drop-in encoder-knob UI) | P_QUADRATURE, Ch.14.2 | OBEX **#2829** quadrature | compiles ✓ |

**Described-not-rebuilt ceiling:** P2_rctime's terminate-stay-resident **REGEXEC background ISR**
(PASM at `org $1B0`, interrupt-driven via `reti1`) — describe + link to OBEX #2831; R1 ships the
simpler polled form (parallels P2AN001's 8-pin interpreter, P2AN002's Park/FOC).

### Verification model — **rig-gated Tier 0/1/2** (P2AN001-style, NOT P2AN002 known-answer)
- **Tier 0 (functional):** P2 Edge + jumpers. Encoder self-stimulates A/B from a second pin pair
  (transition/NCO loopback) → known-answer position count, no external hw. rctime: fixed R/C net.
- **Tier 1 (calibrated):** 0.1 % R + film C (rctime); reference light + lux meter (TSL235R) →
  absolute accuracy / calibration curve.
- **Tier 2 (applied sensors):** CdS/thermistor, TSL235R under known irradiance, detented encoder.
- R3 + the functional layer ship Tier-0 verified; sensor-accuracy claims defer to a hardware run
  (→ EF ledger when accepted). `pnut_ts -d` is the floor gate for every code block.

## Sources mined (located + captured)

| Source | OBEX/QB | Role | Status |
|---|---|---|---|
| P2_rctime (phonoclese, MIT) | OBEX **#2831** | R1 donor (RC-decay) + REGEXEC ceiling | captured (fan-out); compiles `-d` ✓ |
| Quadrature Encoder (jonnymac, MIT) | OBEX **#2829** | R3 donor (production encoder) | captured (fan-out); compiles ✓ |
| QB TSL235R (Bauer / McPhalen / C. Gracey) | QB | R2 donor (light→freq) | **fetched** → `engineering/ingestion/external-inputs/appNote-fodder-NO-COMMIT/quickbytes/tsl235r/` |
| `deliverables/ai/P2/` timing-mode YAMLs + IOSP Ch.13/14/15 | KB | 🏆 primary reference (cite, don't reproduce) | in repo |

## Open questions (for authoring)

- **OQ-1 (RESOLVED — code fetched):** TSL235R source is now in-repo (above); R2 must be authored
  + `pnut_ts -d`-verified at authoring time (was BLOCKED on download-gated code).
- **Verification accuracy** is hardware-pending for R1/R2 (real RC net / sensor + reference);
  R3 + functional layer ship Tier-0 self-stimulated.
- **YAML companion schema** — shares the P2AN001+P2AN002 pilot shape; **FLAG the schema before
  authoring the companion** (design-decision gate, per `APP-NOTE-DESIGN-DECISIONS.md`).
- **Corrections:** none proposed from this region (IOSP Ch.13/14/15 mode facts match the KB).

## Canonical source

Body will live in `opus-master/P2AN004.md` (+ `opus-master/front-matter.md` cover),
authored per `../APP-NOTE-CREATION-GUIDE.md` after the split is decided. Edit there;
the production workspace render is generated and overwrites edits.
