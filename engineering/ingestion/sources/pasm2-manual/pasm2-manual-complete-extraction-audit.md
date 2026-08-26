# PASM2 Manual — Extraction Audit (DOCX re-extraction)

**Source:** `Propeller 2 Assembly Language (PASM2) Manual - 20221101.docx` — Parallax Inc.,
Nov 1 2022 release, 2,049,128 bytes. **PRELIMINARY draft.**
**Mode:** re-extraction, DOCX-primary. **Extraction date:** 2026-08-26.
**Tooling:** `engineering/tools/extraction/docx_walk.py` · `pnut-ts v1.55.3 -d` ·
`audit-extraction-digit-density.py`

> **Predecessor.** The 2025-08-15 audit of the same name recorded a `.docx` extraction, but **no
> DOCX was ever in the source folder** — only the PDF. The DOCX was found in
> `engineering/ingestion/external-inputs/p2/` during this pass and is now staged alongside the PDF.
> That folder turning out to hold un-staged originals is **F-367**.

## The dashboard's "64%" was measuring the wrong thing

The row read **64%** in a column that means *extraction completeness*. Its source is the 2025
audit's line **"Instructions Documented: 315 of 491 (64.2%)"** — a property of **the document**
(a preliminary draft covering 315 of the P2's 491 instructions), not of our capture of it.

**These are different quantities and must not share a cell.** Our extraction of this document is
now essentially complete; the document's own coverage of PASM2 is 64% and cannot be improved by
any amount of ingestion. Corrected in the dashboard row.

## Pre-flight

Text layer probed with `pdftotext -f 1 -l 1` on the PDF: clean English **with digits intact**
(`+1 888-512-1024`, `2022/11/01`) — no F-250-class invisible numeral loss. DOCX used regardless,
being the better source for tables and whitespace.

| | |
|---|---|
| `<w:p>` paragraphs | 10,867 |
| `<w:tbl>` tables | **219** |
| `word/media` | 2 |
| `word/comments.xml` | **present — 2 comments** |

## Digit-density gate (§2a)

| artifact | lines | w/digit | density |
|---|---|---|---|
| `pasm2-manual-text.txt` (DOCX, new) | 5,529 | 3,388 | **61.3%** |
| `complete-pasm2-manual-reference.md` (new) | 5,310 | 2,947 | 55.5% |
| `pasm2-manual-narrative.txt` (prior, PDF-derived) | 6,023 | 3,035 | 50.4% |

**Exit 0.** The tool's own caveat travels with the number: this detects **total** numeral loss
only, is **blind to partial loss**, and is **never a completeness certificate**.

**The DOCX capture carries more words in fewer characters** than the PDF-derived narrative —
77,248 words / 424,536 chars against 72,228 / 552,998 — i.e. more content with less layout padding.

## Coverage

219/219 tables, 259 headings, document order preserved, intra-cell newlines preserved (26 tables
have multi-line cells and are rendered as fenced blocks rather than squeezed into table rows).

## Pass 2 — code

30 blocks extracted (25 paragraph-hosted, **5 cell-hosted**), **10 compile clean** under a harness.
All 20 non-compiling blocks were inspected and none is an extraction defect — 4 instruction summary
tables, 2 alphabetical mnemonic indexes, 5 mixed prose+code, 9 harness limits. Detail in
`assets/code-2026-08-26/README.md`.

## Pass 3 — images

2/2 media extracted. This is a text-and-table manual; it carries almost no figures.

## Pass 6 — findings

**2 reviewer comments, both by Wuerfel21, both substantive — a 100% signal rate.**

- **[0]** → **E-016**. Anchored to the ADDS explanation: *"Incorrect, is WC is result sign bit"*.
  Verified — the manual's prose says C is **signed overflow** while its own Table 8 says
  **`sign of (D + S)`**, a dozen lines apart. Our KB already had this right and explicitly rebuts
  the prose; what was missing was the **record** of a deliberate divergence.
- **[1]** → strengthens **E-001**. Anchored to the `%` in `COGATN #%00100010`. The PASM2 Manual
  prints this **correctly**, where the Hardware Manual drops the `%` and does not assemble. Two
  Parallax documents, same construct, one right and one wrong — which settles E-001 as a typo
  rather than an alternative notation.

**Gap ledger, both halves.** Opened: none unique to this source. Closed: none — this is a
preliminary draft superseded as the PASM2 reference by our own Assembly manual, so it is a
corroboration source rather than a gap-filler. Stated explicitly rather than omitted.

## Trust

**🏆 with a standing qualification.** Official Parallax, but **PRELIMINARY** and superseded as the
PASM2 reference by our Assembly manual. It does not automatically win against `pnut-ts` or the
Silicon Doc, and E-016 is a worked example of it being wrong against its own table.
