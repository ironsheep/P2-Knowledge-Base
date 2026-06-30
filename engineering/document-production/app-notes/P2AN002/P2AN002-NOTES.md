# P2AN002 — Working Notes

**Status:** authoring (plan agreed 2026-06-30)
**Created:** 2026-06-30
**Topic:** CORDIC for Real Work (roster item **B1 LEAD**, Math family)

## Purpose

P2AN002 is the **second** note in the P2 application-note series and the **lead of
the Math family** (`engineering/analysis/p2-app-note-roster.md` §B1). It teaches the
*applied* use of the P2's hardware CORDIC solver — the layer the roster identifies as
"reference assembled but applied guidance taught nowhere."

Per Stephen's plan (2026-06-30): author this note **all the way through PDF
production**, then use **P2AN001 + P2AN002 together** to settle the final app-note
doc-class shape (cover, section spine, voice, code-box treatment, and the YAML
companion schema) before releasing the two **together**. Two concrete examples set
the shape; this is the second.

## Topic — CORDIC for Real Work

The P2's 54-stage pipelined CORDIC solver, taught through worked recipes: rotation,
distance+heading, polar↔cartesian, transcendentals (sin/cos/log/exp), fixed-point
scale/multiply-divide, and pipelining the solver for throughput. Reference for the
*ops* already exists (PASM2 manual + `cordic.yaml` + Spin2 operators); this note owns
the **applied** layer.

## Archetype & scope (agreed 2026-06-30)

**Archetype:** techniques-catalog (same as P2AN001) — one shared conceptual base +
a decision table + runnable recipes the reader selects among.

**Skeleton:**
- Shared base: Abstract / What You'll Build / Prereqs / **The Idea** (queue→work→
  retrieve; the 32-bit binary angle; Spin2 auto-manages vs PASM2 you pipeline) /
  **How It Works** (the 8 ops + Spin2 wrappers + GETQX/GETQY/POLLQMT — cite the
  manual for full enumeration)
- Decision table (need → recipe)
- **R1 Distance & heading** — QVECTOR / XYPOL (flagship/base; verify dist(3,4)=5)
- **R2 Rotate a point** — QROTATE / ROTXY (verify (100,0)→90°→(0,100))
- **R3 Polar→Cartesian: draw a circle** — POLXY in a DEBUG PLOT window (visual)
- **R4 Sine/cosine waveform** — QSIN / QCOS (verify sin(90°)×1000=1000)
- **R5 Fixed-point scale & magnitude** — QMUL/QDIV/QFRAC/MULDIV64; QLOG/QEXP
- **R6 Pipelining for throughput** — fill / steady-state / drain; transform an array
- **Capstone (the ceiling):** Park/Clarke FOC transform (OBEX 2811) — *described &
  linked*, not rebuilt (parallels P2AN001's 8-pin interpreter ceiling)
- Going Further: CORDIC→streamer DDS as a **pointer to the Streamer Programming
  Guide** (the guide-promotion-trigger management — keep it a cross-reference, not a
  full recipe) + the polynomial-atan2 contrast (OBEX 5278)
- Verify / Pitfalls / Conclusion / Resources / References / Revision History

### Boundary delineation (the §2 playbook payoff)
- **Foundational → PASM2 manual + `cordic.yaml` (cited, not reproduced):** per-op
  encodings, the 54-stage/55-clock pipeline architecture, GETQX/GETQY semantics.
- **Applied → this note:** the worked recipes, fixed-point format choices, the
  pipelining pattern, the gotchas.
- **No manual-enrichment fork.** Unlike the ADC note (which drove IOSP Ch.16), the
  CORDIC reference is already adequate — this is an app-note-pipeline-only item.

## Design decisions (flagged → resolved by Stephen 2026-06-30)

1. **Streamer-interaction = pointer, not recipe.** The Streamer Programming Guide
   exists and owns streamer mechanics; CORDIC→streamer DDS is a "Going Further"
   cross-reference. Respects the reference-exists boundary + the guide-promotion
   trigger (don't bloat the Math note toward a guide). ✅
2. **Distance & heading = flagship/base build.** Most useful CORDIC application,
   exactly verifiable. ✅
3. **Verification is hardware-independent.** CORDIC results are *exact known math* —
   every recipe verifies against a closed-form answer in a DEBUG window via
   `pnut_ts -d`. **No Tier-1 rig gating** (contrast with P2AN001's ENOB-pending
   table). This lets P2AN002 ship fully verified, strengthening the joint release. ✅
4. **Capstone added.** Park/FOC (OBEX 2811) as the described-not-rebuilt ceiling. ✅

## Sources to mine (located + studied 2026-06-30)

| Source | Role | Location |
|---|---|---|
| `architecture/cordic.yaml` | primary reference (ops, pipeline) | `deliverables/ai/P2/architecture/cordic.yaml` |
| `pasm2/concepts/cordic_solver.yaml` | PASM2 pipeline patterns (fill/steady/drain, REP protect) | `deliverables/ai/P2/language/pasm2/concepts/` |
| `spin2/concepts/cordic_solver.yaml` | Spin2 wrappers (QSIN/ROTXY/POLXY/XYPOL/QLOG/QEXP/MULDIV64) | `deliverables/ai/P2/language/spin2/concepts/` |
| Silicon Doc v35 | hard pipeline facts (54-stage, 55-clock, 8-clock slot, "several") | `engineering/ingestion/sources/silicon-doc/part3-end.txt:346-352` |
| P2 Datasheet | "one result every 8 clocks" steady state | `engineering/ingestion/sources/p2-datasheet/p2-datasheet-narrative.txt:1424` |
| **OBEX 2811** Park transform (ManAtWork, MIT) | flagship applied QROTATE + 3-op pipelining + 32-bit-circle angles | `research/2811-*` |
| **OBEX 2812** BinFloat (ersmith, MIT) | fixed-point Q-format discipline; muldiv64/mulsqrt64; atan2 via XYPOL | `research/2812-*` |
| OBEX 5278 compass (m.k. borri, MIT) | **contrast** — chose polynomial atan2 over CORDIC | `research/5278-*` |
| Goertzel QB (Chip Gracey) | CORDIC+smart-pin magnitude detection (catalog link) | `deliverables/ai/P2/community/quick-bytes/goertzel-operation-with-ultrasonic-transducers.yaml` |

## Source traceability (fill as the note is built)

| Claim / number / code | Source | Verified |
|---|---|---|
| 8 CORDIC ops (QMUL/QDIV/QFRAC/QSQRT/QROTATE/QVECTOR/QLOG/QEXP) | `cordic.yaml`; Silicon Doc OVERVIEW | KB ✓ |
| 32-bit binary angle ($4000_0000 = 90°, full circle = 2³²) | `spin2/concepts/cordic_solver.yaml`; `qrotate.yaml` angle_format | KB ✓ (see F-169 precedent) |
| 54-stage pipeline, 55-clock latency, hub slot every 8 clocks | Silicon Doc v35 `part3-end.txt:346-352` (verbatim) | source ✓ |
| Overlap "several" ops; ~6-7 derived (54/8) — NOT "7-8" | Silicon Doc "several" + 54/8; **see F-171** | source ✓; YAML flagged |
| QROTATE operands `SETQ y / QROTATE x, angle` | `qrotate.yaml` (post-F-166/F-169 fix) | KB ✓ |
| muldiv64 idiom (SETQ-hi before QDIV) | `cordic.yaml` divide_64_32; OBEX 2812 | KB ✓ + community |
| Q-format discipline (2.30 trig, 1.27 log/exp, 0.32 angle) | OBEX 2812 BinFloat (ersmith) | community; KB-cross-checked |
| Park/FOC 3-QROTATE pipelining + $5555_5555=120° | OBEX 2811 (ManAtWork) | community (capstone, linked not rebuilt) |
| Every code block (6 recipes) | `pnut_ts -d` compile | ✓ verified (pnut_ts v1.55, 200 MHz, `-d`); all lines ≤ K=76; hardware-run pending visual pass |
| Expected Verify values (dist=5, (0,100), 1000, 97_408_265, mag 798_612, log2 whole=16) | arithmetic (python) | ✓ derived |

## Open questions

- ~~Archetype + recipe set + capstone + streamer-as-pointer + verification model.~~
  **RESOLVED 2026-06-30** (design decisions above).
- F-171 (ops-in-flight "7-8" overstatement) flagged to the corrections register; the
  note uses the sourced facts + "several"/~7-derived framing regardless.
- YAML companion schema: **deferred to the joint P2AN001+P2AN002 shape/review** (per
  `APP-NOTE-DESIGN-DECISIONS.md` Decision 2 — schema piloted across the two notes).

## Verification model (hardware-independent)

CORDIC results are deterministic exact math — no analog, no rig. Every recipe ships a
**known-answer** check (closed-form result in a DEBUG window, `pnut_ts -d`). No ENOB /
Tier-1 dependency. The capstone (FOC) is described/linked only, not benchmarked.

## Canonical source

The note's markdown lives in `opus-master/P2AN002.md` (+ `opus-master/front-matter.md`
cover). Edit there; the production workspace render is generated and overwrites edits.
