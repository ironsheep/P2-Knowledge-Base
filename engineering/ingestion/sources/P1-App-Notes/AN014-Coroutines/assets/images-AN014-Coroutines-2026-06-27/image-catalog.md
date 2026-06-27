# Image Catalog — AN014 Coroutines

**Extracted:** 2026-06-27 · **Source:** `AN014-Coroutines-v1.0.pdf` (5 pp, letter)

## Summary

| # | File | Type | Page | Quality gate | Cataloged |
|---|------|------|------|--------------|-----------|
| 1 | `figure-01-coroutines-flowchart.png` | Figure (vector flowchart) | 1 | PASS | yes |
| — | `page1-1.png` | Provenance: full page-1 render (120 dpi) | 1 | (working render — crop source) | n/a |

**Embedded raster images:** none. `pdfimages -list` returned zero objects — Figure 1 is **vector** line art. Per the KB PDF-tooling finding (pdfimages misses vector figures), it was recovered by **page-render (`pdftoppm` 120 dpi) + crop**, not raster extraction. No OCR forced (text layer clean); figure labels read directly.

## Figure 1 — Coroutines Flowchart

- **File:** `figure-01-coroutines-flowchart.png` (590×530 px, cropped from `page1-1.png`)
- **Caption (from prose):** "Figure 1: Coroutines Flowchart"
- **Purpose:** Visualizes the ping-pong execution-interleaving principle that the whole note describes.
- **Content (read off the figure):**
  - Three columns, left-to-right: **Coroutine 1**, **Coroutine 2**, **Result**, with top headers *Start*, *Flow of Control*, *Result*.
  - *Coroutine 1* column: stacked blocks **A, B, C, D, A, B, C, D**.
  - *Coroutine 2* column: stacked blocks **a, b, c, a, b, c, a**.
  - Diagonal "Flow of Control" arrows bounce between the two columns, showing each coroutine yielding to the other.
  - *Result* column shows the interleaved execution order: **A, a, B, b, C, c, D, a, …** (alternating uppercase = Coroutine 1 steps, lowercase = Coroutine 2 steps).
- **Quality gate:** PASS — discrete figure (not a full-page mis-capture); not `#000000`-dominant; labels legible. Crop includes a thin slice of the page-footer rule at the bottom edge (cosmetic only).
- **Consumer references:** `complete-AN014-reference.md` § Coroutine Principle.
- **Enhancement debt:** none required. (Optional future: re-crop 2px higher to drop the footer rule; or vectorize for a clean redraw if reused in a P2 manual.)
