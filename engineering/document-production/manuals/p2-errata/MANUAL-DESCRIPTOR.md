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
authoritative_sources: see ./creation-guide.md §6 # EF ledger EF-066..087 incl. workaround runs (PRIMARY) + raw logs + rigs; P2 Documentation; KB YAML from disk
high_risk_tables:
  - "Quick-reference triage (shared-triage.md) — erratum number ↔ title ↔ who meets it ↔ likelihood; numbers are permanent; printed in BOTH the guide and the sheet"
  - "Each erratum's summary box (shared-eN.md) — printed in BOTH documents; refers to no guide section"
  - "Each chapter's closing line and Appendix A's evidence row — found-by / published-by / confirmed date / test programs must match the ledger"
  - "Each A proven workaround — the printed block must be byte-identical to the marked block of the archive test program that ran it"
  - "Terminology: WORKAROUND, never fix (a fix is a silicon revision); A proven workaround, never THE (Stephen, 2026-09-26)"
high_risk_quant:
  - "E1: PTRx step +4 (+12 for ptra++[3]) with the ALTD, +16 without — read from the log, never recomputed"
  - "E3: 2^32 clocks = 21.47 s at 200 MHz; the GETMS()/GETSEC() table (190,617 / 18,819 / 194,637)"
  - "E4: 14,823 → 30,378, burst 15,555; 50 idle reads unchanged; 60 of 60 burst_sums calls exact"
  - "E7: released alignments 43 / 64 / 16 / 0 at 2 / 8 / 14 / 16 clocks; WAITX #12 = 16 clocks"
fragile_areas:
  - "Classification: class 2 items (the no-wait RDFAST readiness boundary — a FIFO read too soon after a no-wait RDFAST alone; any documentation gap) must never enter — peer manual only. E7 is the hub instruction AFTER a no-wait RDFAST completing early (hub reads, writes, SETQ block reads, a waiting RDFAST; merged 2026-10-01) and must say the FIFO-read case is not it"
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
  verified against the hardware-verification ledger (`P2-EMPIRICAL-FINDINGS.md` EF-066..087)
  and the raw log lines, then against the P2 Documentation for what the design says. Each
  chapter carries a verification sidecar in `verification/` (tracked; see its README).
- **Structure (Dimension #10), since v0.3.0** (`RESHAPE-SPEC.md`): front matter (cover,
  licence, Preface) · Errata Quick Reference (triage + symptom lookup) · Chapter N = erratum EN
  (summary box · *What happens* · *A proven workaround* · closing line) · Appendix A, the
  evidence. A second PDF, the errata sheet, is built from the same shared text at the same
  version. Numbers permanent.
- **Voice (Dimension #9):** the Assembly Reference voice, with the errata-specific rules in
  `voice-guide.md` §2.
- **Code (Dimensions #3/#3b):** PASM2/Spin2 fences, each a verbatim excerpt of an archive
  program (`corpus-identity`); every printed workaround byte-identical to a bench-run block
  (`pnut-ts` 1.55.8); K=76.
- **Chip revision:** Rev C (Stephen, 2026-09-26), stated once in the front matter's Sources.
- **Open before public release:** the study's formal credit name;
  Parallax review of the whole manual; a small standalone reproducer per erratum, bench-run,
  in the examples archive.
