---
manual_slug: P2AN001
doc_class: reference                              # app note — YAML/Silicon/IOSP-backed; verifies claims against KB YAML (§3 grounding)
element_type: application-note                    # ships doc + first-party YAML companion (four-artifact model)
code_line_budget_K: 76                            # inherits platform K (creation-guide §6.3); Dimension #3b
last_published_tag: unreleased                    # first release (v1.0.0); Dimension #15 baseline = whole doc
guide_paths:
  creation_guide: ../APP-NOTE-CREATION-GUIDE.md   # shared app-note class guide (governs all P2ANxxx)
  voice_guide: ../APP-NOTE-VOICE-GUIDE.md         # shared app-note voice
  style_guide: ../APP-NOTE-VOICE-GUIDE.md         # voice guide carries house style
companion_yaml: deliverables/ai/P2/application-notes/p2an001-single-pin-instrumentation-adc.yaml
authoritative_sources: see ../APP-NOTE-CREATION-GUIDE.md §5.1 # P2 Documentation v35 (Chip Gracey) + KB YAML (smart-pin ADC, muldiv64, cordic, wrpin/rdpin/setse1) + IOSP Ch.16 (mechanism owner) + "Improved ADC Pin Techniques" forum thread + pnut-ts (compile-cert)
high_risk_tables:                                 # Dimension #7 — transposition-prone
  - "Choosing a Technique decision table (need -> recipe) — recipe/what-it-adds columns"
  - "Revision History table"
high_risk_quant:                                  # Dimension #5 hot spots
  - "SINC2 encoding X=%01_0111 (mode %01 filtering + 128-clock period %0111)"
  - "Sample-rate math: 200 MHz / 128 = 1,562,500 sps"
  - "Ratiometric formula: uV = (pin - GIO)/(VIO - GIO) * 3_300_000"
  - "Flush count: 3 settling (2 SINC2 + 1 front-end) + 8 summed"
  - "~15 mV matched-resistor absolute-error floor (designer-stated; NOT re-measured)"
  - "Recipe 5 SUMS math: _clkfreq / (MAINS_HZ * 3*11*128) -> ~789 @60Hz / ~947 @50Hz @200MHz"
  - "Legal-clock guard: 200 MHz build; 300 MHz spec max (research code's 320 MHz is over-spec)"
fragile_areas:
  - "ENOB claims are QUALITATIVE by design (mechanism only) — hardware characterization pending. Any *measured* ENOB number is a FINDING (not yet run). Guard against inflation to measured figures."
  - "P_ADC_GIO/VIO/1X source-select constants — must name the real symbols, not fabricate"
  - "4-pin power-domain grouping (pins 0-3..60-63) — Recipe 2 correctness depends on it"
  - "muldiv64 arg order (Spin2) — (a, b, c) = a*b/c with 64-bit intermediate"
  - "8-pin capstone is described/linked ONLY (not rebuilt) — must not imply it's a runnable build in-note"
---

# P2AN001 — Single-Pin Instrumentation ADC — Descriptor

Thin per-note overlay read by document-audit (and prepare-/release-/finalize-manual).
Everything not listed above is inherited from the central skill body + the shared app-note
guides above. This is the **first app-note release** and the **companion-schema pilot**.

- **Grounding model:** `reference` — verify claims against KB YAML under
  `deliverables/ai/P2/` (smart-pin ADC `architecture/smart-pins/smart-pin-11000-adc-internal-clock.yaml`,
  `language/spin2/methods/muldiv64.yaml`, `architecture/cordic.yaml`, the smart-pin config
  instructions), the **Parallax Propeller 2 Documentation v35 - Rev B/C** (ADC front end), and the **I/O & Smart Pins User Guide
  Ch.16** (the mechanism owner this note *applies* — the note must cite, not re-teach). The
  "Improved ADC Pin Techniques" forum thread (Chip Gracey, designer) is the technique source;
  designer-stated figures (e.g. the 15 mV floor) are trust-stamped as designer-authoritative.
- **App-note agreement gate (Dimension — element_type=application-note):** the shipped doc and
  its `companion_yaml` must AGREE — the companion's composition recipe, key parameters, code
  reference, and gotchas match the doc; the companion is a digest+links, never a prose clone. A
  divergence is release-blocking.
- **Structure (Dimension #10):** techniques-catalog archetype per creation-guide §1.1/§4 —
  shared base (Abstract → Prereqs → The Idea → How It Works → Test Harness → Base Build) then
  a decision table + Recipes 2–5 + the 8-pin ceiling (described), then Verify → Pitfalls →
  Conclusion → Resources → References → Revision History → Copyright/Acknowledgments. **No ToC.**
- **Voice (Dimension #9):** per APP-NOTE-VOICE-GUIDE.md; consolidated markers (⚠/💡/🔧/🔍);
  "cog" lowercase; symbolic constants taught not raw numbers; avoid bare mnemonic-words as
  plain English (mnemonic-bold false-bolds them).
- **Code (Dimensions #3/#3b):** every embedded block + every `examples-library/*.spin2` compiles
  under `pnut-ts` (`-d`, it uses `debug()`); K=76; inline code spans ASCII-only.
