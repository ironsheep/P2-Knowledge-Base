# P1 Propeller Manual v1.1 Supplement & Errata — Extraction Audit

**Source:** `122-32000-Propeller-Manual-v1.1-Supp-Errata.pdf` · 8 pp · 🏆 Parallax · © 2011 · ingested 2026-06-22
**Tool:** `pdf-layout` (text layer clean). Full text → `p1-manual-errata-v1.1-layout-text.txt`.

## Role finding — this is the v1.1→v1.2 CHANGELOG, not a correction layer over v1.2
The document's own header: *"This document tracks the technical content changes between Propeller Manual
**v1.1 and v1.2** … all significant changes noted here have been marked with comments on the web PDF of
**Version 1.2**."* Our backbone is **v1.2**, which already incorporates every change here.

**Consequence (overturns charter §1's "errata supersedes the base Manual" framing for THIS doc):**
- It does **not** outrank or correct our v1.2 corpus — v1.2 already contains these edits.
- Its value is **(a)** an independent **QA checklist** confirming our v1.2 extraction fidelity, **(b)** the
  **v1.1→v1.2 change provenance** for `P1-DOCUMENT-LINEAGE`, **(c)** a few timing facts that enrich a gap.
- → **No `F-P1-` corrections routed** (nothing supersedes v1.2). The charter's correction-layer assumption
  held for a *hypothetical* errata-over-current-edition; here the errata predates our edition.

## QA cross-check — every change-item verified present in the v1.2 extraction (0 defects)
Spot-verified across Ch1/Ch2/Ch3 against `…/p1-propeller-manual-v1.2-layout-text.txt`:
| Errata item (page) | In v1.2 extraction? |
|--------------------|---------------------|
| Table 1-2 RAM/ROM organization (p16) | ✅ (spec table) |
| Cog RAM para + SPR interfaces (p23) | ✅ |
| Hub 8–23 cycle text + 15-instruction hub list (p24) | ✅ |
| Figs 1-3/1-4 replaced (p25) | ✅ (extracted figures) |
| Locks atomic para (p30) | ✅ |
| XTAL3 500 Ω/16 pF/20–60 MHz (p68) | ✅ (CLK OSCMx table) |
| COGINIT CogID 8–15 → next-available (p76) | ✅ (layout text 2539) |
| "~>" = Bitwise Shift arithmetic right (p43,144,158-9,249,326) | ✅ |
| CON/OBJ/VAR "column 1" + indent guidance (p85,141,210) | ✅ |
| Master table "Clocks" 8..23 for 15 hub instrs (p252,254-5) | ✅ (master table in layout text 253-256) |
| WAITCNT/PEQ/PNE = 6+; WAITVID = 4+¹ + Note 5 (p255-6,371) | ✅ |
| Note 1 detailed hub-timing explanation (p256) | ✅ |
| ENC marked reserved-for-future (`#`) in Reserved Word List (p379) | ✅ |
| CMPSUB "special … D, S" (p380) | ✅ |
| "no call stack" CALL/JMPRET return-address (p268,300) | ✅ |

**Result: 100% of documented changes are present in the v1.2 extraction → backbone validated, no extraction defects.**

## Gap implications
- **G-P1-001** (PASM1 per-instruction timing + encodings): the **Instruction Master Table** with full encoding
  columns AND the "Clocks" column **is in the v1.2 layout text (pp253–256)** — camelot mislabeled it but
  `pdf-layout` captured it. The errata pins the hub-instruction timing at **8..23**, **WAITCNT/WAITPEQ/WAITPNE
  = 6+**, **WAITVID = 4+** (Note 5: 4 clocks itself, full frame handoff needs 7 — or 6 at some freqs). → G-P1-001
  is largely *answerable from the v1.2 master table*; remaining = structured per-instruction parse (YAML step).

## Extraction completeness
8/8 pages extracted, all ~35 change-items cataloged. No images of value (the errata's "replaced figures"
are the same Fig 1-3/1-4 already captured from v1.2). Trust tier 🏆 (Parallax). Lineage role recorded.
