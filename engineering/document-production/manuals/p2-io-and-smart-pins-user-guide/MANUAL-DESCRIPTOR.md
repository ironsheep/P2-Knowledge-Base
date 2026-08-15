---
manual_slug: p2-io-and-smart-pins-user-guide
doc_class: reference
code_line_budget_K: 76
last_published_tag: unreleased            # maiden release — Dimension #15 baseline is the whole doc
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md           # no separate style-guide; voice-guide carries style rules
authoritative_sources: see ./creation-guide.md §"Verification Requirements"
  # Primary: P2 Documentation v35 (engineering/ingestion/sources/silicon-doc/), hardware-verification
  #          ledger (engineering/ingestion/external-sources/hardware-verification/ — 🏆), P2 instruction
  #          spreadsheet, pnut-ts. Derived: KB YAML deliverables/ai/P2/ (architecture/smart-pins/,
  #          language/pasm2/, language/spin2/). Cross-check-only (community/derived, NOT primary):
  #          Jon Titus smart-pin extracts.
high_risk_tables:                         # transposition-prone — Dimension #7
  - "Per-mode Register Usage tables (X[..]/Y[..]/Z/IN rows) — every chapter 6-19"
  - "Appendix F Complete Mode Reference (Register Usage + Key Constants per %mode)"
  - "Appendix B P_ Constants Quick Reference (Constant | Value | Description)"
  - "Quick Mode Selection Matrix (front-matter) — mode bits <-> chapter"
  - "Appendix D Mode Comparison Charts"
  - "Colored bit-field 'ruler' tables (Ch4 config-value format, Ch2 P_ constant table)"
fragile_areas:                            # known-thin / historically-buggy — weight heavily
  - "%00101 Transition Output — Y=0 semantics (RA-10/F-135; just corrected — verify no regression)"
  - "ADC modes Ch16 — X[5:4] SCP_ADDR encoding, ENOB/dither figures (expert-queue items parked)"
  - "Reciprocal counting / period-frequency Ch15/16 (F-186/187/188/189 MULDIV64 class)"
  - "USB Ch19 — FPGA-resistor pointer (F9), transmit-pacing community claim (no silicon source)"
  - "Smart-pin init order (Reset->Setup->Enable->Operate; WYPIN after enable; pinstart unsafe for triggers)"
  - "DAC dither modes Ch10 (cadence/ENOB — some expert-parked)"
  - "Waiting Strategies Ch5 §5.1 (F1 — newly authored SETSE/WAITSE/POLLCT1)"
---

# P2 I/O & Smart Pins User Guide — Descriptor

Thin per-manual overlay read by document-audit (and prepare-/release-/finalize-manual).
Everything not listed above is inherited from the central skill body + the guides above.

**Notes for the auditor:**
- **First release (v1.0.0).** No prior published tag, so Dimension #15 baseline is the entire
  document; scope-completeness is judged against the union of the build efforts recorded in
  `engineering/planning/` + `./audit/` + the git history of `./opus-master/`.
- **No `CHANGELOG.md` yet** — must be authored before `release-manual` (release prerequisite, not
  an audit defect per se; Dimension #13 records the absence).
- `AUDIT-PROCESS.md` in this folder is **superseded by the central document-audit skill** — queue
  for the consolidation pass; do NOT delete during an audit run.
- Rich `./audit/` history exists (periodic 2026-05-25, titus-cross-audit 2026-06-12, code-compile
  2026-06-20, usb-boundary 2026-06-30, visual-review 2026-06-26) — Dimension #12 reads these for
  prior-finding closure.
