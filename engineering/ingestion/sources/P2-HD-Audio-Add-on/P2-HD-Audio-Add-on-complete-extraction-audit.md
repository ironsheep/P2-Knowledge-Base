# Extraction Audit — P2 HD Audio Add-on Set (#64014)

**Mode:** new / greenfield · **Passes run:** 1–5 (stage-only; no pass 6/7, no canonical writes, no ID allocation)
**Wave:** addon-wave-2026-06 · **Date:** 2026-06-27
**Two-input structure:** PRIMARY board guide (🏆) + AK5704 codec datasheet (🟡 cross-check).

## Inputs
| Input | Pages | Text layer | Role | Tier (proposed) |
|---|---|---|---|---|
| `64014-P2-HD-Audio-Add-on-Set-Guide.pdf` | 6 | clean (no cipher) | PRIMARY board guide | 🏆 primary |
| `ak5704en-en-datasheet.pdf` (AKM AK5704) | 109 | clean (no cipher) | cross-check companion (component datasheet) | 🟡 cross-check |

Text-layer sanity: `pdftotext -f 1 -l 1` on both PDFs returned clean readable English (not ciphered) → **no OCR forced**; `pdftotext -layout` used for content/tables.

## Pass 1 — Content (board guide PRIMARY)
- **Method:** `pdf2md` (docling) for structure/tables + `pdftotext -layout` for the authoritative clean text (`P2-HD-Audio-Add-on-text.txt`, 191 lines). docling cleanly recovered the ADC pin table; the **DAC pin table column-bled** in docling → reconstructed from the layout extract (lines 135–169).
- **Captured:** product overview, ADC features + key specs (10 specs) + 11-row pin table, DAC features + key specs (7 specs) + pin table + drive-strength design notes, board dimensions, resources, revision history (v1.0).
- **Paragraphs:** ~24 prose blocks · **Tables:** 2 (ADC pin map, DAC pin map) both captured · curated → `complete-P2-HD-Audio-Add-on-reference.md`.

## Pass 1 — Content (AK5704 cross-check)
- **Method:** `pdftotext -layout` (`ak5704-crosscheck-text.txt`, full 109-pg extract). **Non-exhaustive by design** — pulled only corroborating fields.
- **Captured for cross-check:** part identity/ordering, 28-pin QFN pinout (28 pins), audio interface format + register 0EH bitfields, register-map index (00H–34H+), I²C control, MIC-amp gain registers, VAD registers, clock/PLL registers → curated `ak5704-crosscheck-reference.md`.
- **Tables:** pinout + register map captured at index granularity (not every bit).

## Pass 2 — Code examples
- **Board guide contains NO embedded code** (it points to example code on the product page only). DAC "example" (31-ohm headphone Ohm's-law calc) is prose arithmetic, not a code listing.
- **Extracted: 0 · validated: 0 · failed: 0.** `pnut_ts` not invoked (nothing to compile). `assets/code-2026-06-27/` left empty.

## Pass 3 — Images (board guide)
- **Method:** `pdfimages -png` + `image-tools-mcp` quality gate.
- **Extracted: 7 · unique: 6 · quality-passed: 7/7 · OCR'd: 2** (board-004 ADC photo → silkscreen labels legible & matched pin table; board-005 dimension drawing → OCR-risk, rotated dimension text).
- Catalog: `assets/images-P2-HD-Audio-Add-on-2026-06-27/image-catalog.md`. Duplicate: board-001 == board-003 (md5).
- **AK5704 datasheet images:** NOT extracted (cross-check tier; register/timing diagrams not needed as images — bitfield facts captured as text).

## Pass 4 — Post-processing / relationships
- **Codec identity:** AKM AK5704EN (28-pin QFN), ADC board only. DAC board = pure P2 Smart Pin DACs (no codec IC).
- **I²S/TDM wiring (ADC):** MCKI / BCLK / LRCK / SDTO1 (MIC) / SDTO2 (Line); I²C control SDA/SCL @ 400 kHz; PDN power-down; WINTN interrupt (unpopulated). Header-pin → signal map captured in both refs.
- **DAC wiring:** 4 paralleled Smart-Pin outputs per channel — DAC_L = header +7..+4, DAC_R = header +3..+0; drive impedance set by # of channels combined (18.75–990 Ω, 16 steps; 2 V/3 V Vpp).
- **Header-signal ↔ codec-pin map** built (primary board signal names ↔ AK5704 pin names) — see audit §Cross-source below.

## Pass 5 — Validation / completeness
- Board guide is fully extracted (6/6 pages accounted; every section + both tables captured). **Board-guide completeness ≈ 100%** of textual content; the only non-text gaps are mechanical-drawing dimension callouts (corroborated by the spec table) and off-doc example code (lives on product page).
- AK5704 cross-check completeness: **intentionally partial** (~corroboration subset of a 109-pg datasheet) — sufficient to corroborate every board-guide codec claim.

---

## Cross-source corroboration matrix (board guide 🏆 vs AK5704 datasheet 🟡)
| Fact | Board guide says | AK5704 datasheet says | Verdict |
|---|---|---|---|
| Codec part | "AK5704EN 32-bit 4ch ADC w/ MIC pre-amp" | AK5704EN, 28-pin QFN, 4-ch 32-bit ADC + MIC amp | ✅ MATCH |
| Sampling freq | 8 k–192 kHz | 8 kHz–192 kHz | ✅ MATCH |
| Max S/N | 105 dB | 105 dB dynamic range | ✅ MATCH |
| Control I/F | I²C 400 kHz | I²C-bus 400 kHz | ✅ MATCH |
| MIC amp gain | +30..0 dB, 3 dB step | MG[3:0] gain regs 05H/06H (programmable) | ✅ consistent |
| VAD | "VAD reduces power" | VAD Setting regs 1BH–24H | ✅ MATCH |
| Ultrasonic | "supports ultrasonic recording" | up to 192 kHz fs (ultrasonic-capable) | ✅ consistent |
| Audio I/F signals | MCKI/BCLK/LRCK/SDTO1/SDTO2 | pins 5–10 + reg 0EH I²S/TDM | ✅ MATCH (1:1 pin names) |
| I²C signals | SDA(+7)/SCL(+6) | pins 2–3 SCL/SDA | ✅ MATCH |
| Power-down | PDN (+0) "L=down,H=up" | pin 14 PDN "L:Power-down,H:Power-Up" | ✅ MATCH (verbatim) |
| Interrupt | WINTN (unpopulated) | pin 4 WINTN Interrupt Output | ✅ MATCH |
| Temp range | −40..+85 °C | AK5704EN −40..+85 °C | ✅ MATCH |

**Conflicts: NONE.** Every codec-level claim in the board guide is corroborated by the datasheet. Adjudication authority where it mattered: the AK5704 datasheet is the authority for codec-internal facts; the board guide is authority for the P2 accessory-header mapping. They agree on the overlap.

> Reminder: AK5704 facts are cross-check tier — they corroborate the primary; they are NOT promoted as P2 knowledge.

## OCR-risk flags
- board-005 mechanical dimension drawing: dimension callouts not machine-readable (rotated text). Mitigated — numeric dims corroborated by the spec table. No fact at risk.

## Notes for pass 6/7 (NOT performed here — proposals only, see HANDBACK.md)
- Candidate dashboard row, AUTHORITATIVE-SOURCES tiers (🏆 board / 🟡 AK5704), DOCUMENT-LINEAGE entry, and any gap/expert-Q proposals are in `HANDBACK.md`. No F-/G-/Q- IDs allocated.
