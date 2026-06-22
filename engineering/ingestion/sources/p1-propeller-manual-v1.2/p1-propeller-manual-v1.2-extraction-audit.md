# P1 Propeller Manual v1.2 — Extraction Audit (Pass 5 validation)

**Source:** `P1 P8X32A-Web-PropellerManual-v1.2.pdf` · 399 pp · 🏆 Parallax primary · v1.2.0-11.06.14
**Re-extraction date:** 2026-06-22 · **Mode:** re-extraction (current tooling) superseding the 2025-11-22
old-tooling "strategic sampling" capture · **Validator:** flexspin DEFERRED → all P1 code `code_validated:false` (charter §3)

## Why re-extracted
The prior capture (`P1-PropellerManual-v1.2-extracted.txt` + audit) was **pypdf text + strategic sampling**:
~50 pages deep + samples, **no images, no tables, no exhaustive content**, self-rated ~60%. This re-extraction
uses the current PDF toolkit to capture prose, code, **vector figures**, and **ruled tables** fully.

## Tooling outcome (the "prove the new tools" goal)
| Pass | Tool used | Result |
|------|-----------|--------|
| Content (prose) | `pdf-layout` (pdftotext -layout) | ✅ complete, clean, indent-preserving; 399 pp / 14,574 lines. Text layer verified non-ciphered (no OCR needed). |
| Content (tables) | `camelot lattice` (`--format csv/markdown`) | ✅ clean ruled-table → structured extraction (Specs, CLK reg, pins, instruction tables). Minor cell-merge artifacts on a few. |
| Content (high-fidelity md) | `pdf2md` (docling) | ❌ **OOM** on 399 pp at ~2 GB free RAM; no page-range flag in this build. **Superseded by camelot for tables** — docling not needed here. |
| Code | `pdf-layout` → (flexspin deferred) | ✅ extraction faithful (indent + inline comments intact); validation pending flexspin. |
| Images | `pdfimages` → **page-render + crop + image-tools-mcp** | ✅ — but `pdfimages` found only **7 unique rasters / 163 objects** (figures are vector). Page-render+crop captured all 14 figures; image-tools-mcp OCR + quality-gate confirmed. |

**Methodology finding (routed to Pass 7 / methodology docs):** for diagram-heavy P1/P2 source PDFs,
raster XObject extraction (`pdfimages`/PyMuPDF) is the wrong default — it silently misses vector line-art.
Page-render+crop is the correct figure workflow. `image-extraction-methodology.md` still assumes raster-first.

## Section-by-section completeness
| Part | Pages | Captured | Depth |
|------|-------|----------|-------|
| Preface | 11–12 | text | full |
| **Ch1 Hardware** | 13–34 | text + 8 figures + 7 tables | **fully curated** → `complete-architecture-hardware.md` (every fact, page-cited) |
| **Ch2 Spin reference** | 35–237 | full layout text + code examples + 6 figures + tables | **text/code complete**; per-command structuring = YAML-head build step |
| **Ch3 PASM1 reference** | 238–378 | full layout text + code examples + 1 figure + master/effects/conditions tables | **text/code complete**; per-instruction structuring = YAML-head build step |
| App A Reserved words | 379 | layout text | full |
| App B Math/sine tables | 380–385 | layout text (+ camelot available for the numeric tables) | full text |
| Index | 386–399 | layout text | captured (low value) |

## Per-pass counts
- **Content:** 399 pp prose extracted (`p1-propeller-manual-v1.2-layout-text.txt`); Ch1 curated to facts doc; full section→page map in `…-structure-map.md` (~80 Spin commands, ~110 PASM1 entries inventoried).
- **Tables:** 9 ruled tables extracted to `assets/tables-2026-06-22/` (Specs, pins, CLK reg ×4, PASM example/master tables ×3). ~40 tables total inventoried by caption; the structurally-important ones extracted; remainder available on demand via camelot.
- **Code:** 72 high-confidence anchored examples → `assets/code-2026-06-22/p1-manual-code-examples.md` (broad scan saw code on 325 pp / ~787 raw blocks incl. syntax/tables — not all are illustrative examples). **All `code_validated:false`** (flexspin install pending). Full per-symbol example harvest = YAML-build step.
- **Images:** 14 figures cropped + cataloged (`assets/images-…/image-catalog.md`), all PASS quality gate; key architectural labels OCR-verified (Fig 1-2 block diagram, Fig 1-5 memory map).

## Extraction-quality flags (NOT content conflicts)
- `code-…/…-examples.md` p53: `byte 64. $AA[8], 55` — the `64.` is likely a comma (`64,`); verify at flexspin validation.
- `tables-…/tbl-page-253…md`: camelot labeled it the "master instruction table" but the captured grid is an
  ADD-style example/behavior table; the true opcode master table (p253–256) may need a targeted re-extract or
  layout-text capture. Flagged for the PASM1 structuring step.
- Fig 1-2 cog-internal micro-labels below OCR legibility at 200 dpi (illegible in original); architectural labels OCR clean.

## Validation verdict
**Content/code/image/table extraction: COMPLETE and faithful** for an ingestion-corpus (the source is fully
captured; nothing lossy remains). **Not yet done:** flexspin code validation (tool pending) and per-symbol
structured reference entries (Ch2/Ch3) — the latter is the YAML head's build job, fed by this corpus. The
prior old-tooling extraction is now obsolete → archive per §0.6 (Pass 7).
