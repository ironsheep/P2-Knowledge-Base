---
manual_slug: p2-assembly-language-manual
doc_class: reference                              # YAML-backed (PASM2 instruction reference)
code_line_budget_K: 76                            # platform-inherited; LM-Mono calibrated (creation-guide v1.2)
last_published_tag: p2-assembly-language-manual-v3.1.6   # baseline for Dimension #15 (released 2026-08-18, 502pp)
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md                   # v1.1 (user-suggestions sprint)
  style_guide: ./style-guide.md
authoritative_sources: see ./creation-guide.md    # canonical source list lives there; key tiers below
source_highlights:
  - deliverables/ai/P2/language/pasm2/             # primary derived YAML (per-instruction)
  - deliverables/ai/P2/language/spin2/             # inline-PASM / Spin2 interop
  - engineering/ingestion/sources/silicon-doc/     # silicon truth
  - "Parallax P2 Instructions v35 - Rev B_C Silicon CSV"   # encoding + Operation-line source (col 5)
  - pnut-ts                                        # compiler validation (use -d for DEBUG-window code)
high_risk_tables:
  - "Per-instruction encoding tables (COND / INSTR / FX / DEST / SRC / Write / C / Z / Clocks) — Part II + Appendix A"
  - "Appendix C categorical index (instruction → category groupings)"
fragile_areas:
  - "Operation: pseudocode lines (206, added in the user-suggestions sprint Phase 2) — source = Parallax CSV col 5; verify NO inference"
  - "_RET_ encoding (EEEE=0000) — prior CRITICAL-error analysis in ./audit/_RET_-CRITICAL-ERROR-ANALYSIS.md"
  - "Multi-precision flag chains (ADDX / SUBX / SUBSX) and cancelled-conditional cycle accounting (§3.5.3 fixed in Phase 3)"
  - "LUT immediate-addressing limit (#0-#255) — OBS-09 / KB finding F-161; §1.3.2 + RDLUT/WRLUT"
  - "Phase-3 cross-refs + faster-instruction alternatives (FLE/FGE, SCA/SCAS, etc.) — verify each cross-ref target exists and each cycle delta is sourced"
  - "Ch.3 FLAG-BEHAVIOR narrative + branchless idiom examples (§3.2 effects, §3.3 conditional-execution timing, §3.4 flag-by-category tables, §3.5 idioms) — worked examples ARE claims; 2026-07-09 forum report found fabrications here (§3.5.4 ABS 'C indicates edge case' — WRONG, C = original sign; §3.2.6 'TEST*' over-generalized; §3.3.x cycle-count-vs-instruction-count)"
  - "Ch.4 TIMING narrative, esp. hub-access/latency-hiding prose (§4.6) — 2026-07-09: §4.6.2 'pipelined hub access' FABRICATION (a plain RDLONG blocks; only FIFO/streamer + SETQ-burst hide latency; CORDIC §4.6.3 is the real parallel case). Watch parallel/overlap/pipelined claims (methodology §2.1)"
  - "Operator notation in flag/behavior descriptions AND Spin2 code examples — comparison predicates must be '==' not '=' (methodology §6.4); 'receives' '=' stays; ':='/'==' strict in fenced Spin2 code"
  - "Appendix G mode-table DESCRIPTIONS (the Value column has always been right; the prose gloss was not). 2026-08-22: 31 of 36 rows decoded `_kDACb` as \"k pins, b DAC channels\" instead of \"k DAC channels, b bits each\", and every Usage Example put a rate in XINIT's S operand and set no D[15:0] count. Re-derive any row from Silicon Doc part2-pixel-ops.txt:139-227; the decode rule now heads the appendix"
  - "PART I NARRATIVE PROSE was never claim-level audited (prior Part I audit = curated 8-feature checklist over-attested as 'examined ALL'; see ./audit/root-cause-2026-07-09-part-i-prose-never-claim-audited.md). Ch.1-6 need exhaustive claim extraction per methodology §5.4"
---

# P2 Assembly Language Reference — Manual Descriptor

Thin per-manual overlay read by `document-audit` (and, going forward, `prepare-manual` /
`release-manual` / `document-finalize`). Everything not listed in the front matter is inherited
from the central `document-audit` skill body + the guides referenced above.

**Doc-class note:** `reference` / YAML-backed — factual dimensions (A, B, #1, #5, C) verify against
`deliverables/ai/P2/language/` read from disk, not `p2kb-mcp` (which serves the lagging published
index). Tutorial voice is NOT permitted here (Dimension #9).

**Unreleased efforts since `last_published_tag`** (the changeset-integrity baseline, Dimension #15):
**IN FLIGHT — streamer-correctness co-release (v3.1.7, opened 2026-08-22).** The Assembly
half of the Streamer Guide v1.1.0 sweep: F-303 (RGBI8), F-305 (DAC pin setup) and F-308
(`X_PINS_ON` needs `DIRH`), plus F-318 — the Appendix G mode-table decode defect those
three surfaced. Also adopts three platform features owed at this release: metadata
single-sourcing (F-300), rights metadata (F-316) and the cross-reference filter (F-301).
Next release deltas against the **v3.1.6** tag. Inventory:
`engineering/analysis/2026-08-22-assembly-v3.1.7-finalize-inventory.md`.

The 2026-07-09 fabrication-audit sprint referenced here previously **shipped** in v3.1.3–v3.1.6;
its "deltas against the v3.1.2 tag" line was stale from v3.1.3 onward.
