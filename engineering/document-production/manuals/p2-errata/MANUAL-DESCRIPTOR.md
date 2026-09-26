---
manual_slug: p2-errata
doc_class: reference                              # bench-proven errata reference; Assembly Reference voice
code_line_budget_K: 76                            # inherits platform reference K (creation-guide §Code Line Budget)
spin2_blocking_rules: 2.1, 2.1.4, 2.4, 2.5, 3.1, 3.2, 4.1, 4.2, 4.2.1, 4.5, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4.1   # «#360» 2026-09-26: armed for THIS manual's examples-library (0 sites when armed); §3.4 (worded "preferred"), §5.7 and §6.4 (T1+T2 / Part 6) stay advisory
last_published_tag: none                          # never released; v0.1.0 / v0.2.0 are community-review drafts
guide_paths:
  creation_guide: ./creation-guide.md
  voice_guide: ./voice-guide.md
  style_guide: ./voice-guide.md                   # voice-guide adopts the Assembly Reference guide by reference
  classification: ./CLASSIFICATION-GUIDANCE.md    # governs what may enter (class 1 only)
authoritative_sources: see ./creation-guide.md §6 # EF ledger EF-066..074 + fix-run entries (PRIMARY) + raw logs + rigs; P2 Documentation; KB YAML from disk
high_risk_tables:
  - "Front-matter summary table — erratum number ↔ title ↔ published-by ↔ workaround condition; numbers are permanent"
  - "Each chapter's Status table — published-by / found-by / confirmed / workaround-proven must match the ledger"
  - "Each chapter's CAUTION box and A proven workaround — the printed block must be byte-identical to the marked block of the archive test program that ran it"
  - "Terminology: WORKAROUND, never fix (a fix is a silicon revision); A proven workaround, never THE (Stephen, 2026-09-26)"
  - "E1 pointer-delta table (control vs hazard per SETQ form) — transposition-prone"
high_risk_quant:
  - "E1: control vs hazard PTRx deltas (+16 vs +12, +32 vs +4) — read from the log, never recomputed"
  - "E3: D = 1 / 0 / 2 across wraps in run A; D = 0 throughout run B"
  - "E4: 50 of 50 idle reads unchanged; 255 = 29 + 226 terms × 61"
  - "E5: d1 = (N−1)·C, d2 = C, carry arm N·C; N = 64, C = −19 → −1,197"
fragile_areas:
  - "Classification: class 2 items (the no-wait RDFAST readiness boundary; any documentation gap) must never enter — peer manual only. E7 is the BLOCKING RDFAST case and must say it is not the no-wait one"
  - "SINC2: the iteration-count corruption is DOCUMENTED (P2 Documentation note on Goertzel SINC2 mode) — not an erratum, not part of E5 (EF-072 corrected 2026-09-26); E5 names it only as the scope limit of its SINC1 fix"
  - "No HDL quotation, signal/module names or line refs from the clean-room design material (decision 5)"
  - "No internal ids in reader text (EF/VO/F/brief names); the chip revision (Rev C) stated once, in the front matter"
  - "Scope qualifiers the bench earned: E1 tested ALTD only as the intervening instruction; E3 conditions (four-cog group, wraps missed while no cog of the group ran)"
  - "KB lag: E3–E7 not yet in the KB YAML (F-462..466, F-471..473); the manual cites silicon, the KB must follow"
---

# P2 Errata — Descriptor

Thin per-manual overlay read by document-audit (and prepare-/release-/finalize-manual).
Everything not listed above is inherited from the central skill body and the guides above.

- **Grounding model:** `reference`, **bench-first**. Every claim about what the part does is
  verified against the hardware-verification ledger (`P2-EMPIRICAL-FINDINGS.md` EF-066..074)
  and the raw log lines, then against the P2 Documentation for what the design says. Each
  chapter carries a verification sidecar in `verification/` (tracked; see its README).
- **Structure (Dimension #10):** front matter (incl. the three classes defined once and the
  summary table) · Chapter N = erratum EN · Appendix A, the test programs. Numbers permanent.
- **Voice (Dimension #9):** the Assembly Reference voice, with the errata-specific rules in
  `voice-guide.md` §2.
- **Code (Dimensions #3/#3b):** PASM2/Spin2 fences; walkthrough excerpts verbatim from
  bench-run rigs; every printed workaround byte-identical to a bench-run block (`pnut-ts` 1.55.8); K=76.
- **Chip revision:** Rev C (Stephen, 2026-09-26), stated once in the front matter's Sources.
- **Open before public release:** the study's formal credit name;
  Parallax review of the whole manual; a small standalone reproducer per erratum, bench-run,
  in the examples archive.
