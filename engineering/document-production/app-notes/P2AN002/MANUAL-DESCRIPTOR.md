---
manual_slug: P2AN002
doc_class: reference                              # app note — YAML/Silicon-backed; verifies claims against KB YAML (§3 grounding)
element_type: application-note                    # ships doc + first-party YAML companion (four-artifact model)
code_line_budget_K: 76                            # inherits platform K (creation-guide §6.3); Dimension #3b
last_published_tag: unreleased                    # first release (v1.0.0); Dimension #15 baseline = whole doc
guide_paths:
  creation_guide: ../APP-NOTE-CREATION-GUIDE.md
  voice_guide: ../APP-NOTE-VOICE-GUIDE.md
  style_guide: ../APP-NOTE-VOICE-GUIDE.md
companion_yaml: deliverables/ai/P2/application-notes/p2an002-cordic-for-real-work.yaml
authoritative_sources: see ../APP-NOTE-CREATION-GUIDE.md §5.1 # Silicon Doc v35 (CORDIC Solver section) + P2 Datasheet + Spin2 docs (ROTXY/POLXY/XYPOL/QSIN/QCOS/MULDIV64) + PASM2 Reference (companion manual) + OBEX (#2811/#2812/#5278/#5361) + pnut_ts
high_risk_quant:
  - "Pipeline geometry: 54-stage pipeline, 55-clock result latency, issue every 8 clocks, ~6-7 in flight (54/8) — F-171 territory; mirror the Silicon 'several' framing, no hard in-flight count"
  - "Binary angle convention: full circle = 2^32; $4000_0000=90, $8000_0000=180, $C000_0000=270, $5555_5555=120, $AAAA_AAAA=240"
  - "QLOG/QEXP = 5.27 fixed-point (5 whole + 27 fractional)"
  - "Trig precision ~28 bits; integer ops (QMUL/QDIV/QSQRT) exact"
  - "Worked numbers: XYPOL(3,4)=5 heading ~$25C8 (~53); muldiv64(123456,789012,1000)=97,408,265; mag(123456,789012)=798,612; log2(123456) whole part 16"
fragile_areas:
  - "QMUL/QDIV/QFRAC/QSQRT are UNSIGNED; QVECTOR/QROTATE are signed — must not swap (register F-166/F-171 history)"
  - "QFRAC is a DIVIDE (fractional), not a multiply (register CRITICAL correction)"
  - "GETQX = X/length/quotient, GETQY = Y/angle/remainder — must not swap"
  - "ops-in-flight is DERIVED (~6-7), Silicon says 'several' — never assert a hard count (F-171)"
  - "The 3-phase-motor/Park ceiling is described/linked (OBEX #2811) ONLY — not rebuilt in-note"
---

# P2AN002 — CORDIC for Real Work — Descriptor

Thin per-note overlay read by document-audit (and prepare-/release-/finalize-manual).
Second app-note release; reuses the companion schema piloted on [[P2AN001]].

- **Grounding model:** `reference` — verify against `architecture/cordic.yaml`, the PASM2
  CORDIC instruction pages (`language/pasm2/q*.yaml`, `getqx/getqy`), the Spin2 method pages
  (`rotxy/polxy/xypol/qsin/qcos/muldiv64`), and the **Silicon Doc v35** CORDIC Solver section.
  The note *applies* the solver; the PASM2 Reference owns the full encoding.
- **App-note agreement gate:** doc and `companion_yaml` must AGREE (composition recipe, key
  parameters, gotchas). Companion is a digest+links, never a prose clone.
- **Structure (Dimension #10):** techniques-catalog per creation-guide §1.1/§4 — shared base
  (Abstract → Prereqs → Idea → How It Works) then decision table + Recipes 1-6 + the FOC ceiling
  (described) + Going Further, then Verify → Pitfalls → Conclusion → Resources → References →
  Revision History → Copyright/Acknowledgments. **No ToC.**
- **Verification model:** the CORDIC computes deterministic math, so every recipe's expected
  output is closed-form and checkable by hand — the note's Verify steps cite exact answers
  (XYPOL(3,4)=5, etc.). No bench instruments; DEBUG-window confirmation only.
- **Code (Dimensions #3/#3b):** every embedded block + every `examples-library/*.spin2` compiles
  under `pnut_ts` (`-d`, uses `debug()`); K=76; inline code ASCII-only.
