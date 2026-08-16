---
manual_slug: P2AN003
doc_class: reference                              # app note — YAML/Silicon-backed; verifies claims against KB YAML (§3 grounding)
element_type: application-note                    # ships doc + first-party YAML companion (four-artifact model)
code_line_budget_K: 76                            # inherits platform K (creation-guide §6.3); Dimension #3b
last_published_tag: unreleased                    # first release (v1.0.0); Dimension #15 baseline = whole doc
guide_paths:
  creation_guide: ../APP-NOTE-CREATION-GUIDE.md
  voice_guide: ../APP-NOTE-VOICE-GUIDE.md
  style_guide: ../APP-NOTE-VOICE-GUIDE.md
companion_yaml: deliverables/ai/P2/application-notes/p2an003-dac-analog-signal-generation.yaml
authoritative_sources: see ../APP-NOTE-CREATION-GUIDE.md §5.1 # P2 Documentation v35 (Smart Pins: DAC modes %00001/%00010/%00011) + P2 Datasheet (DAC electrical) + Spin2 docs (WRPIN/WXPIN/WYPIN, QSIN, QROTATE, MULDIV64, frac) + IOSP Ch.10/§18.3 (companion manual) + OBEX (#2861 reSound, #2860 EZ Sound) + pnut-ts
high_risk_quant:
  - "DAC is physically 8-bit; the dither modes reach a NOMINAL 16-bit output averaged over time — no ENOB/SNR/THD number printed (G-003 resolved; figures defer to a hardware run)"
  - "PWM dither adds a Fclock/256 (sysclock/256) spectral line at -48 dB — SOURCED (P2 Documentation v35, part4-smart-pins; Titus corroborates); do not restate as an unqualified fabrication"
  - "PWM dither X period MUST be a multiple of 256 clocks (256 minimum, X[7:0]=0); PRNG dither X=1 updates every clock"
  - "Voltage math V = (code/65536) x Vfs; $8000->1.65V, $4000->0.825V at Vfs=3.3V; muldiv64(CODE,VFS_UV,$10000)"
  - "Output configs: P_DAC_990R_3V / P_DAC_600R_2V / P_DAC_124R_3V (123.75 ohm) / P_DAC_75R_2V (990/600/124/75 ohm; 3.3V or 2.0V peak)"
  - "DDS phase increment inc = f x 2^32 / sample_rate via Spin2 `frac` (unsigned (x<<32)/y); 200MHz/256 = 781_250 Hz sample rate"
fragile_areas:
  - "FGES/FLES are INTEGER signed-limit (Force >=/<= Signed), NOT floating-point — Recipe 5's clamp to +/-$7FFF is correct; never 're-fix' it into a bug"
  - "QROTATE(ampl, phase) with no preceding SETQ => input (ampl,0); GETQY = ampl*sin(phase), GETQX = ampl*cos(phase) — must not swap (matches P2AN002)"
  - "ADC in Recipe 4 uses SINC2 FILTERING (X[5:4]=%01), so the per-period value is the DIFFERENCE of two rdpin reads — matches the hardware-verified P2AN001; wxpin #%01_1000 = SINC2 + 2^8=256 clocks (X[3:0]=exponent), period-matched to the DAC's 256"
  - "reSound (OBEX #2861, Johannes Ahlebrand, 955 lines) 32-stream engine + MOD player = DESCRIBED/LINKED only, not rebuilt"
  - "EZ Sound (OBEX #2860) is NCO/FREQ tones, NOT a DAC technique — a one-line contrast (IOSP Ch.8), never a recipe"
  - "add $8000 = signed->offset-binary for WYPIN; applied to the bipolar sine/sample paths, correctly omitted from the already-unipolar saw/triangle"
---

# P2AN003 — DAC & Analog Signal Generation — Descriptor

Thin per-note overlay read by document-audit (and prepare-/release-/finalize-manual).
Third app-note release; reuses the companion schema piloted on [[P2AN001]] and [[P2AN002]].
The output sibling to the ADC note [[P2AN001]]; the shared DAC surface is owned by the
I/O & Smart Pins User Guide (IOSP) and CITED, not reproduced (boundary decided in the
IOSP-campaign mine-and-delineate — foundational fork EMPTY, advanced fork PRESENT).

- **Grounding model:** `reference` — verify against the DAC-mode YAMLs
  (`architecture/smart-pins/smart-pin-000{01,10,11}-*.yaml`), the ADC mode
  (`smart-pin-11000-adc-internal-clock.yaml`, for Recipe 4), the PASM2 instruction pages
  (`wrpin/wxpin/wypin/rdpin/setse1/waitse1/qrotate/getqx/getqy/zerox/muls/sar/fges/fles`),
  the Spin2 method/operator pages (`qsin/muldiv64/op_FRAC`), and the **Parallax Propeller 2 Documentation v35 - Rev B/C**
  Smart Pins DAC section. IOSP Ch.10 (DAC Output) + §18.3 (DAC noise) own the mechanism.
- **App-note agreement gate:** doc and `companion_yaml` must AGREE (composition recipe, key
  parameters, gotchas). Companion is a digest+links, never a prose clone.
- **Structure (Dimension #10):** techniques-catalog per creation-guide §1.1/§4 — shared output
  stage (Abstract -> Prereqs -> Idea -> How It Works) then decision table + Recipes 1-5 + the
  reSound ceiling (described) + Going Further, then Verify -> Pitfalls -> Conclusion -> Resources
  -> References -> Revision History -> Copyright/Acknowledgments. **No ToC.**
- **Verification model:** rig-gated Tier 0/1/2 (mirrors [[P2AN001]]). Tier-0 = DAC->ADC loopback
  known-answer (fixed code -> computable DC V=(code/65536)xVfs, read back by a P2AN001 ADC, one
  jumper, no bench gear). Numeric audio-quality figures (SNR/THD/effective bits) DEFER to a
  hardware run (-> EF ledger when accepted), exactly as P2AN001's ENOB-pending table.
- **Code (Dimensions #3/#3b):** every embedded block + every `examples-library/*.spin2` compiles
  under `pnut-ts` (Recipes 1-5 plain; the Tier-0 verify snippet uses `debug()` so needs `-d`);
  K=76; inline code ASCII-only.
