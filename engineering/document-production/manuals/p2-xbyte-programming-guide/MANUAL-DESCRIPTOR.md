---
manual_slug: p2-xbyte-programming-guide
doc_class: reference                              # YAML-backed + Silicon-Doc-backed reference + teaching (two-register), Streamer model
code_line_budget_K: 76                            # inherits platform reference K (creation-guide §Code Line Budget)
last_published_tag: none                          # NOT yet released — v0.1.0 is the first-draft review build
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md                   # no separate style-guide; voice-guide §4 carries terminology/format standards
  planning: ./PLANNING.md                         # seed/design doc — scope decisions of record
authoritative_sources: see ./creation-guide.md §4 # Silicon Doc v35 XBYTE section (PRIMARY hardware truth) + KB YAML deliverables/ai/P2/architecture/xbyte_engine.yaml + language/pasm2/{skip,skipf,execf,setq,setq2,rdfast,rfbyte,rfvar,rfvars,getptr}.yaml ; grounding digest in ./audit/xbyte-source-grounding-digest-2026-06-26.md
high_risk_tables:                                 # transposition-prone — weight heavily on audit
  - "§7 / Ch.7 Table-Size & Compression Modes — the 256/128/64/32/16 (+alt) bit-pattern table; index-calc columns"
  - "Ch.4 / Ch.14 LUT entry format ([9:0] address vs [31:10] SKIPF pattern) — do not transpose the field split"
  - "Appendix B Instruction Encoding Summary (SKIP/SKIPF/EXECF/SETQ/SETQ2/RDFAST/RFxxxx/GETPTR)"
  - "Ch.5 the 8-clock dispatch-cycle table (clock→activity rows)"
high_risk_quant:                                  # hot spots
  - "6-clock overhead vs 9-clock software dispatch vs 8-clock minimum loop (Silicon Doc verbatim — cite, never round/restate)"
  - "Mode-operand bit layout %A…F (table base / %BBBB compression threshold / F bit)"
  - "PA = $1F6, PB = $1F7 ; LUT routine range $200–$3FF, COG range $000–$1FF ; hardware stack 8 levels"
fragile_areas:                                    # known-thin / discipline-sensitive
  - "Capstone 6502 emulator (Ch.11) + 6809 SETQ2 vignette (Ch.12) — TINY & ILLUSTRATIVE by charter; guest-CPU ISA facts are historical, but all PASM2 must pnut-ts compile"
  - "Appendix C external-implementation links (Arc8de, Yume suite) — links + author + what-it-emulates + license ONLY; never claim XBYTE use unless sourced; NO narrative use elsewhere (scope decision of record)"
  - "Banned-class discipline: no Spin2-method interpreter clock timings; the 6-clock HARDWARE overhead is the only citable timing"
  - "SCOPE GUARD (v0.1.0): no 'systems similar to the P2' content (EDL/Series-1, Transputer, XMOS, GreenArrays, Cell) — cut by decision; do not reintroduce without Stephen"
---

# P2 XBYTE Programming Guide — Descriptor

Thin per-manual overlay read by document-audit (and prepare-/release-/finalize-manual).
Everything not listed above is inherited from the central skill body + the guides above.

- **Grounding model:** `reference` — verify every XBYTE / skip-family / FIFO claim against
  the **Silicon Doc v35** XBYTE section (`engineering/ingestion/sources/silicon-doc/`,
  PRIMARY hardware truth) and the KB YAML under `deliverables/ai/P2/architecture/xbyte_engine.yaml`
  + `language/pasm2/` (skip/skipf/execf/setq/setq2/rdfast/rfbyte/rfvar/rfvars/getptr). Read YAML
  from disk, not p2kb-mcp (currency). The compiled grounding digest is in `./audit/`.
- **Structure (Dimension #10):** 14 chapters in 4 parts + Appendices A–D + clickable Index,
  per creation-guide §2. Front matter = house standard. Modeled on the Streamer guide.
- **Voice (Dimension #9):** two registers (teaching + reference) per voice-guide. Teaching
  register (Ch.1, chapter openers) allows "you" + analogy; reference register (tables,
  encodings, per-instruction detail) is third-person, no hedging. Banned patterns from
  voice-guide §2.2. "cog" lowercase in prose.
- **Terminology (Dimension #8):** voice-guide §4 canonical terms (bytecode not "opcode" for
  the stream; dispatch not "decode"; routine/handler not "function"; the skip *family*).
- **Code (Dimensions #3/#3b):** PASM2/Spin2 fenced blocks; compile with `pnut-ts`; K=76;
  no breaklines.
