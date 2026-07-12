---
manual_slug: P2AN004
doc_class: reference                              # app note — YAML/Silicon-backed; verifies claims against KB YAML (§3 grounding)
element_type: application-note                    # ships doc + first-party YAML companion (four-artifact model)
code_line_budget_K: 76                            # inherits platform K (creation-guide §6.3); Dimension #3b
last_published_tag: unreleased                    # first release (v1.0.0); Dimension #15 baseline = whole doc
guide_paths:
  creation_guide: ../APP-NOTE-CREATION-GUIDE.md
  voice_guide: ../APP-NOTE-VOICE-GUIDE.md
  style_guide: ../APP-NOTE-VOICE-GUIDE.md
companion_yaml: deliverables/ai/P2/application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml
authoritative_sources: see ../APP-NOTE-CREATION-GUIDE.md §5.1 # Silicon Doc v35 (Smart Pins: measurement modes %10001 P_HIGH_TICKS / %10101 P_COUNTER_TICKS / %10111 P_COUNTER_PERIODS / %01011 P_QUADRATURE + A/B input routing) + TSL235R datasheet (ams/TAOS, 3rd-party = cross-check tier) + Spin2 docs (pinstart/wrpin/wxpin/rdpin/pinread/pinh/pinl/pinf/pinw/muldiv64) + IOSP Ch.13-15 (companion manual) + OBEX (#2831 P2_rctime, #2829 Quadrature Encoder) + pnut_ts
high_risk_quant:
  - "Reciprocal frequency counter (R2): frequency = periods x clkfreq / ticks via MULDIV64; %10101 (ticks) + %10111 (periods) run over the SAME X window; worked check 50 kHz/100 ms/200 MHz -> 5000 periods, 20e6 ticks -> 50_000 Hz"
  - "TSL235R (datasheet, cross-check tier): fO = 250 kHz typ at Ee = 430 uW/cm^2, lambda_p = 635 nm, VDD = 5 V; 2.7-5.5 V operating; dark output 0.4-10 Hz; Ee = freq * 430 / 250_000"
  - "Quadrature (R3): P_QUADRATURE %01011, continuous totalizer X=0 (Z holds live signed count), 4 counts/detent -> sar 2 to normalize; zero by pulsing DIR low (pinf/pinl)"
  - "R1: P_HIGH_TICKS %10001 latches the high duration in clocks and raises IN on the high->low crossing only; us = clocks / (clkfreq / 1_000_000)"
  - "Single-pin reciprocal routing: signal pin uses default-local A/B in P_COUNTER_TICKS; the periods pin on SIG_PIN+1 routes BOTH inputs back one pin (P_MINUS1_A | P_MINUS1_B) so it watches the same signal"
fragile_areas:
  - "P_B_A_INPUT does NOT exist (undefined in pnut_ts, F-176) — single-pin count/quadrature routing is the BARE mode constant (A/B default local) plus P_MINUS1_A|P_MINUS1_B (reciprocal) or P_PLUS1_B (quadrature); never re-introduce P_B_A_INPUT"
  - "A period is A-input rise to B-input rise (Silicon Doc): a neighbour cell watching the signal must route BOTH A and B (P_MINUS1_A|P_MINUS1_B) or its idle B never rises and the window hangs — R2 routes both, correctly (see corrections register F-192 re: the YAML idiom)"
  - "R1 depends on P_LOW_FLOAT: OUT=1 drives (charge), OUT=0 floats (discharge through sensor). P_OE keeps the driver enabled regardless of DIR, so the DIR pulse (pinf/pinl) resets/starts the smart pin WITHOUT disturbing the charge — do not 're-fix' the pinf/pinl order"
  - "An open sensor / too-short charge HANGS the R1 poll loop (IN rises only on high->low); it does NOT read $8000_0000. Near-zero = missing P_LOW_FLOAT (low output drives to ground)"
  - "R2 irradiance scale is folded into the constant (muldiv64(freq, CAL_UW*100, CAL_HZ)) so the x100 lands in the 64-bit path — do NOT revert to freq*100 (32-bit pre-multiply, overflows above ~21 MHz for the generalized-sensor case)"
  - "TSL235R figures are a 3rd-party datasheet (cross-check tier), not Parallax-primary; the built-in irradiance conversion is a starting point pending calibration, stated as such"
---

# P2AN004 — Frequency / Rotation / RC-Timing Measurement — Descriptor

Thin per-note overlay read by document-audit (and prepare-/release-/finalize-manual).
Fourth app-note release; reuses the companion schema piloted on [[P2AN001]] and [[P2AN002]]
and carried by [[P2AN003]]. The timing-instrumentation sibling (Family A2) to the ADC note
[[P2AN001]]; the smart-pin measurement modes are owned by the I/O & Smart Pins User Guide
(IOSP) and CITED, not reproduced (boundary decided in the IOSP-campaign mine-and-delineate —
foundational fork EMPTY, advanced fork PRESENT).

- **Grounding model:** `reference` — verify against the measurement-mode YAMLs
  (`architecture/smart-pins/smart-pin-{10001,10101,10111,01011}-*.yaml`), the Spin2
  method/PASM2 pages (`pinstart/wrpin/wxpin/rdpin/pinread/pinhigh/pinlow/pinfloat/pinwrite/
  muldiv64`), the **Silicon Doc v35** Smart Pins measurement section (period = A-rise to
  B-rise + A/B routing), and the **TSL235R datasheet** (ams/TAOS, cross-check tier) for the
  transducer facts. IOSP Ch.13 (time), Ch.14 (counting/quadrature), Ch.15 (frequency/period)
  own the mechanism.
- **App-note agreement gate:** doc and `companion_yaml` must AGREE (composition recipe, key
  parameters, gotchas). Companion is a digest+links, never a prose clone.
- **Structure (Dimension #10):** techniques-catalog per creation-guide §1.1/§4 — shared idea
  (Abstract -> Prereqs -> Idea -> How It Works) then decision table + Recipes R1-R3 + Going
  Further, then See-It-Work/Verify -> Pitfalls -> Conclusion -> Resources -> References ->
  Revision History -> Copyright/Acknowledgments. **No ToC.** Three rendered figures (R1 RC-decay
  schematic, R2 TSL235R hookup, R3 quadrature timing) via the shared app-note diagram library.
- **Verification model:** rig-gated tiers (mirrors [[P2AN001]]). R3 is Tier-0 self-verified — a
  two-jumper stimulus drives a known detent count (5 fwd, 2 back -> reads 5 then 3) on a bare
  board, no encoder. R1/R2 show correct *behavior* now (count moves with sensor R; frequency
  moves with light); absolute calibration (lux, temperature, irradiance) DEFERS to a hardware
  run (-> EF ledger when accepted). No invented sensor readings.
- **Code (Dimensions #3/#3b):** every embedded block + every `examples-library/*.spin2` compiles
  under `pnut_ts` (all three use `debug()` so need `-d`); K=76; inline code ASCII-only.
