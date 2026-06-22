# P2 Eval Add-on Boards (#64006) — Complete Extraction Audit

**Sources:** `64006-P2-Eval-Add-on-Boards-Product-Guide.pdf` (v2.0, 1/12/2021, 12pp — **authoritative**) +
`64006-ES P2-ES Eval Board Accessory Set Guide-OLD.pdf` (2020 set edition, 13pp — **cross-check**)
**Re-ingested:** 2026-06-22 · **Skill:** `ingest-source` (cross-edition) · **Auth:** 🏆 (Parallax primary)
**Supersedes:** the fabricated Aug-2025 extraction (see "Fabrication rescue" below).

## ⚠️ Fabrication rescue (the reason for this redo)
The prior Aug-2025 extraction **invented the entire board lineup** — LED Array / Switch Array /
Potentiometer / Servo Header / Sensor / Prototyping / Digital I/O / Analog I/O. **None of those appear in
the actual Product Guide.** The real lineup (verified against both editions' PDFs):

| # | Real board | Fabricated claim (removed) |
|---|-----------|----------------------------|
| A | Control | LED Array |
| B | Serial Host | Switch Array |
| C | LED Matrix | Potentiometer |
| D | Digital Video Out | Servo Header |
| E | Mini Prototyping | Sensor |
| F | Serial Device | Prototyping |
| G | Goertzel | Digital I/O |
| H | A/V Breakout | Analog I/O |

The fabrications leaked into published YAML (`hardware/addon-*.yaml`) — routed to the YAML head via
**F-121** (the spurious `addon-digital-io-board` / `addon-servo-header` entries trace directly here).

## Pass-by-pass
| # | Pass | Result |
|---|------|--------|
| 1 | **Content** | ✅ 2025: `pdf2md` / `pdftotext -layout` (clean text layer). 2020: **forced OCR** (`docling --force-ocr` — Quartz export had a corrupt text layer; 2nd case of the ladder refinement). Texts: `p2-eval-add-on-boards-text.txt`, `…-2020-edition-ocr-text.txt`. |
| 2 | **Code** | ✅ none in source (the guide has no Spin2/PASM2 listings — pin tables + Charlieplex lookup only). |
| 3 | **Images** | ⏳ deferred — board photos/PCB-dimension drawings are illustrative; the fact-bearing data (pin maps) is text. Image debt logged, not blocking. |
| 4 | **Post-processing** | ✅ per-board pin maps → 8 per-board source docs (`boards/addon-*.md`) + overview/index. |
| 5 | **Validation** | ✅ all 8 board sections + overview captured; pin maps cross-edition-validated. |
| 6 | **Cross-source / conflict** | ✅ see below. |
| 7 | **Registration** | ✅ dashboard, AUTHORITATIVE-SOURCES (🏆 + part-number aliases), DOCUMENT-LINEAGE; F-121 updated. |

## Per-board source documents (the requested structure)
One source doc per discrete board, each with its pin map + specs + cross-edition note:
`boards/addon-control-64006a.md` · `addon-serial-host-64006b.md` · `addon-led-matrix-64006c.md` ·
`addon-digital-video-out-64006d.md` · `addon-mini-prototyping-64006e.md` · `addon-serial-device-64006f.md` ·
`addon-goertzel-64006g.md` · `addon-av-breakout-64006h.md`. Shared facts → `complete-p2-eval-add-on-boards-reference.md`.

## Pass-6 — cross-edition reconciliation (F-121)
- **Both editions agree** on the 8-board lineup, functions, and **every pin map** — high confidence
  (2025 clean text ∩ 2020 forced-OCR).
- **Deltas:** 2020 `#64006-ES` = set-only, for the limited-edition `#64000-ES` Eval Board; 2025 `#64006` =
  individual + set, for the production `#64000` + Edge modules. **Goertzel** changed probe-posts (2020) →
  touch-pads (2025 Rev B). Recorded per board.
- **F-121 action for the YAML head:** replace the fabricated `hardware/addon-*.yaml` board set with the
  8 real boards from `boards/`; the 4 part-number-less orphans (`7_segment_display`, `buttons_board`,
  `switches_and_leds`, `switches_board`) are **not** #64006 boards — remove or re-home.

## Completeness: **90%** — gates
**C** ✅ (both editions) · **K** — n/a · **I** ⏳ (image debt) · **A** ✅ · **X** ✅ (cross-edition).
Not 100%: board photos / PCB-dimension images not yet extracted (low fact-value).
