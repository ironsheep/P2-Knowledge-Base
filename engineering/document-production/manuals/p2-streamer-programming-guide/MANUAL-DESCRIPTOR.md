---
manual_slug: p2-streamer-programming-guide
doc_class: reference                              # YAML-backed + Silicon-Doc-backed reference (§3 grounding model)
code_line_budget_K: 76                            # inherits platform reference K (creation-guide §Code Line Budget); Dimension #3b
last_published_tag: p2-streamer-programming-guide-v1.1.0   # baseline for Dimension #15 (released 2026-08-22, 91pp)
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md                   # no separate style-guide; voice-guide §4 carries terminology/format standards
authoritative_sources: see ./creation-guide.md §4 # P2 Documentation v35 (PRIMARY hardware truth) + Spin2 symbol reference + KB YAML under deliverables/ai/P2/{architecture/streamer,language/spin2/symbols,language/pasm2}
high_risk_tables:                                 # transposition-prone (Dimension #7) — F-154/F-155 history lives exactly here
  - "§4.2 Mode Field D[31:28] table (streamer-body.md) — mode→source→dest rows"
  - "§4.3 DAC Routing Field D[27:24] + §4.5 Pin Group Field D[22:20]"
  - "Per-mode reference tables: IMM (Ch.5), RDFAST/RFxxxx (Ch.6), WRFAST/WFxxxx (Ch.7) — pin-count vs DAC-channel-count vs DAC-bit columns"
  - "Appendix A complete mode-encoding table"
  - "Appendix B symbol quick reference (X_* constants → pin/DAC decode)"
  - "Ch.13 Programming Constants (Symbols) tables"
high_risk_quant:                                  # Dimension #5 hot spots
  - "NCO frequency formula + SETXFRQ 2^32 basis (F-016/F-157 history)"
  - "Pin-group ranges (§4.5: %000=31..0 … wrap-around groups; F-155 was %101=32 pins)"
  - "Pixel-rate / jitter sysclk-ratio table (§3.4) and clock-accuracy figures (§3.5)"
fragile_areas:                                    # known-thin / historically-buggy — weight heavily
  - "EXAMPLE CONTRACT (creation-guide §5.2) — every ```pasm2/```spin2 block is a worked example OR carries a **Pattern**/**Fragment** lead-in naming what the reader supplies. Audit each block against the five diagnostics defined there: undefined symbol · phantom data · no output path · false constraint · no declared storage. An unlabelled block failing any test is a finding; a LABELLED pattern is not — do not 'fix' patterns into fake completeness (nine such findings were refuted 2026-08-19). THE CONTRACT HAS TWO HOMES AND THEY MUST AGREE: creation-guide §5.2 states it for the AUTHOR and carries the five diagnostics; front-matter.md's 'Code Blocks' section states it for the READER and deliberately omits them. Changing the label form in one is a finding unless the other moves with it. The reader half must not acquire the diagnostics, and must not promise more than the contract does — an unlabelled block promises nothing is left for the reader to supply, NOT that it is a standalone program (§11.0's setup excerpt is unlabelled and correct)"
  - "Mode reference pin/DAC-channel columns — origin of F-154 (streamer-symbols transposition) + manual H-4/M-1"
  - "§3.4 Choosing a Pixel Rate + §3.5 Clock Accuracy and Jitter — rewritten in v1.0.1, verify still grounded"
  - "§15.1 VGA sync/blank mode-long — resolved 2026-06-03 (commit bdddd12) vs OBEX vga_tile_driver.spin2; verify intact"
  - "XCONT/XZERO/XINIT phase-continuity wording (§4.7, Ch.4) — F-003 history"
---

# P2 Streamer Programming Guide — Descriptor

Thin per-manual overlay read by document-audit (and prepare-/release-/finalize-manual).
Everything not listed above is inherited from the central skill body + the guides above.

- **Grounding model:** `reference` — verify claims against KB YAML under
  `deliverables/ai/P2/architecture/streamer/`, `language/spin2/symbols/streamer-symbols.yaml`,
  the relevant `language/pasm2/` streamer instructions (RDFAST/WRFAST/RFxxxx/WFxxxx/XINIT/
  XCONT/XZERO/SETXFRQ), and **P2 Documentation v35** (PRIMARY hardware truth,
  `engineering/ingestion/sources/silicon-doc/`). Read YAML from disk, not p2kb-mcp (currency).
- **Structure (Dimension #10):** 18 chapters in 5 parts + Appendices A–D + clickable Index,
  per creation-guide §2.1. Front matter = house standard.
- **Voice (Dimension #9):** banned patterns derive from voice-guide §2.2 "What We DON'T Say"
  + §2.3 (Never: *vague* hedging / celebration / tutorial-voice / questions /
  "simply"/"basically"). A qualifier that reflects partial evidence is R1 compliance,
  not vagueness — never strip a calibrated one.
  Third person (component names), authoritative-precise register.
- **Terminology (Dimension #8):** voice-guide §4.1 canonical terms (NCO not oscillator/clock;
  rollover not overflow; command not instruction; count/mode/phase fields; "streamer" the
  component, not "DMA"); "cog" lowercase in prose.
- **Code (Dimensions #3/#3b):** PASM2/Spin2 fenced blocks; compile with `pnut-ts`; K=76.
