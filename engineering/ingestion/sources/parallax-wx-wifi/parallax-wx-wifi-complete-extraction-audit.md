# Parallax WX Wi-Fi Module (#32420) — Extraction Audit (Pass-5 Validation)

**Source:** `32420-Parallax-WX-WiFi-Module-Guide-v1.0.pdf` — v1.0, 05/12/2016, 12 pp, 4.9 MB
**Mode:** RE-EXTRACTION (replaces lossy PDF-era capture w/ unaddressed 12+-image debt)
**Extraction date:** 2026-06-27
**Tooling:** `pdftotext -layout` · `docling` (md table) · `camelot lattice` (CSV cross-check) ·
`pdfimages -png` · `image-tools-mcp` (quality gate + OCR)

## Section-by-section completeness

| # | Section (page) | Captured? | Notes |
|---|---|---|---|
| Cover / contacts | 1 | YES | Contacts, part #s, intro paragraph |
| Form factors (SIP/DIP) | 1 | YES | #32420S / #32420D; XBee-incompatibility note |
| Features | 2 | YES | All bullets (modes, web server, OTA, HTTP/WS/TCP, LEDs) |
| Application ideas | 2–3 | YES | Boe-Bot, Activity Board WX, TCP-to-Internet |
| Specifications | 3 | YES | Protocols, security, voltages, logic levels, current, form factor, dims, temp |
| Functional description (1–10) | 4–5 | YES | All 10 numbered components + ASC LED-behavior table |
| Configuration pages | 6–9 | YES | AP join, /PGM 4× re-AP, 192.168.4.1, 4 sub-pages, STA+AP→STA security note, file URLs |
| Firmware / OTA | 10 | YES | `.ota` upload flow |
| Pin Map (diagram) | 10 | YES | Figure wx-016 (illustrative) |
| Pin Descriptions (table) | 11 | YES | 12-row table, authoritative (docling + camelot + text cross-checked) |
| PCB Dimensions | 12 | YES | Mechanical drawing wx-017 |
| Revision History | 12 | YES | "Version 1.0: Original release" |

**Structural completeness: 100%** — every titled section captured.

## Per-pass counts

- **Pass 1 (content):** ~12 pages → clean text (344 layout lines / 17.6 KB); ~30 prose paragraphs;
  **3 tables** captured (Specifications-as-list, ASC LED-behavior 5-row, Pin Descriptions 12-row).
  Text layer verified clean (not ciphered) — no OCR forced.
- **Pass 2 (code):** **0 extracted / 0 validated / 0 failed** — no code in a Wi-Fi product guide
  (expected). `pnut_ts` not invoked.
- **Pass 3 (images):** **18 raster objects → 15 content images + 3 soft-masks**; 15/15 content
  images quality-passed; 2 OCR'd for evidence (config-home wx-010, pinout wx-016).

## Cross-validation of fact-bearing fields

- **Pin table** triangulated across 3 extractions (docling markdown, camelot lattice CSV, pdftotext
  layout) — all agree on Module-Pin / Direction / SIP / DIP / ESP8266 / Function. HIGH confidence.
- **Pinout schematic (wx-016)** OCR is noisy (low confidence on `/ESPIO14`, `i6`); used only to
  corroborate the table, never as primary. Flagged OCR-risk, non-load-bearing (table is authority).
- **Specifications / logic levels / current** captured verbatim from clean text. HIGH confidence.

## Fragile / OCR-risk fields flagged

- wx-016 schematic labels (low-confidence OCR) — **do not** source pin facts from the figure;
  the table is authoritative.
- UI-screenshot field labels (wx-011..015) not exhaustively OCR'd — captured as prose from the
  document body; high-res re-OCR only if a downstream manual needs exact button text.

## Verdict

**EXTRACTION COMPLETE.** Content + tables + the full image set recovered; the prior baseline's
"12+ images expected" debt is cleared. No code to validate. Trust tier proposal and findings are
in `HANDBACK.md` (proposals only — not applied in this staged MAP run).
