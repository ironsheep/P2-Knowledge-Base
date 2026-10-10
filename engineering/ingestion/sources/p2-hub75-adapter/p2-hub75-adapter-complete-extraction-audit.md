# P2 Eval HUB75 Adapter (#64032) — Extraction Audit (audit of record)

**Sources ingested**:
- `hub75-adaptor-v1.4-schematic.pdf` — *"HUB75E Adapter for P2 Eval"*, Iron Sheep Productions, LLC,
  **H/W Rev 1.4, 2020-11-25**, KiCad 5.1.7, 1 page US Letter landscape, 581,634 B,
  md5 `f497ec00ca8bb923df886d76537c5c92`. Staged 2026-10-07. The PDF is git-ignored (repo-wide
  `*.pdf` rule); the reading is checkable against the committed renders.
- The designer's statement of 2026-10-10 (`p2-hub75-adapter-designer-statement-2026-10-10.md`):
  board size (hand-measured), current draw, maximum clock.

**Mode**: first true ingestion. The folder was **registered, not ingested** (2026-08-27): it held three
authored captures and no primary document. This run supersedes them (re-extraction flavour,
`ingest-source` §0.6).
**Authority**: 🏆 golden source: the designer's own documents for his own board (Stephen,
2026-10-10; `AUTHORITATIVE-SOURCES.md` admission route 2).
**Extraction date**: 2026-10-10 · **Tooling**: `pdftotext`/`pdffonts` (text-layer probe),
`pdfimages`, `pdftoppm` 200/400 dpi, `image-tools-mcp image_ocr_full`, visual read.

## Pre-flight: what the file carries

| Probe | Result | Meaning |
|---|---|---|
| `pdftotext` | 1 byte | **no text layer at all**; not even the title block |
| `pdffonts` | no fonts | every glyph is a path (KiCad printed through macOS Quartz) |
| `pdfimages -list` | 2 rasters | the HUB75 DATA-IN connector picture (546x684) and a photo of the P2 Eval header pair (205x804) |

No text-extraction tool (`pdf2md`, `pdf-layout`, `camelot`) can recover this sheet. The extraction
ladder used instead: OCR of the 400 dpi render as one leg, the rendered page read directly as the
leg of record (same path as `p2-click-adapter`, #64008).

## Passes

| # | Pass | Result |
|---|---|---|
| 1 | Content | `p2-hub75-adapter-text.txt` (raw OCR of the 400 dpi render, 61 lines, noisy as schematic OCR always is) + `p2-hub75-adapter-netlist.md` (the curated reading: title block, printed notes, 10 components, power, header-pin→offset, the full offset→buffer→connector path, J7/J3 pinout, spares) |
| 2 | Code examples | **0.** A schematic carries no code. The captures' Spin2 snippets (pin-map `CON` blocks, a driver-API example) are not carried forward: the pin maps are wrong (below) and the driver API is not this board's to document (the driver is OBEX 2850) |
| 3 | Images | 9 images under `assets/images-p2-hub75-adapter-2026-10-10/`: the 200 dpi sheet, six 400 dpi region crops, the two embedded rasters. All discrete figures with legible content; the crops are the evidence for every row of the netlist |
| 4 | Post-processing | the offset map and the signal-path table in the netlist (derived from the header table + U1/U2 wiring) |
| 5 | Validation | below |
| 6 | Q&A + conflicts | below |
| 7 | Registration | dashboard row, `AUTHORITATIVE-SOURCES.md` (🏆, admission route 2 created), `DOCUMENT-LINEAGE.md`, `KNOWLEDGE-GAPS.md` |

## Digit-density gate (§2a)

`python3 engineering/tools/validation/audit-extraction-digit-density.py engineering/ingestion/sources/p2-hub75-adapter`
→ `p2-hub75-adapter-text.txt`: 45 of 47 substantive lines carry a digit, **95.7%** (floor 20%),
exit 0. The tool's own caveat applies: it catches **total** numeral loss only, never partial, and is
not a completeness certificate. Here the raw text is OCR and is not the reading of record; the
netlist was confirmed against the rendered page region by region.

## Validation — coverage of the sheet

| Sheet element | Captured | Evidence |
|---|---|---|
| Title block | YES, verbatim | `schematic-page1-200dpi.png`; OCR lines 57–62 agree |
| J1, J2 + the 3.3 V note | YES | `crop-400dpi-hdr.png` |
| U1 + C1 | YES, all 20 pins | `crop-400dpi-u1.png` |
| U2 + C2 | YES, all 20 pins | `crop-400dpi-u2.png` |
| J3, J7 | YES, all 16 pins each | `crop-400dpi-conn.png` |
| DATA-IN picture + "GND here is Really E" | YES | `crop-400dpi-idc.png`, `embedded-hub75-data-in-connector.png` |
| J4, J5, J6 + the through-hole note | YES | `crop-400dpi-spare.png` |
| P2 Eval header silkscreen (photo) | YES | `embedded-p2-eval-header-photo.png` |

**Coverage: 100% of the sheet.** Every netlist value was read on the 200 dpi sheet and again on the
400 dpi crop. Internal consistency check: J1's own net labels (`IO+15` at pin 2, `IO+14` at pin 8)
agree with the photo's silkscreen reading of the header, so the header-pin→offset mapping rests on
two independent signals.

## Cross-source reconciliation — the captures against the schematic

The three captures (authored 2025-09, never a document extraction) were the folder's only content
and the source behind `hardware/hub75_adapter.yaml`. Against the designer's schematic:

**Confirmed (4):** offsets 0–13 = CLK, OE#, LAT, A–E, R1, G1, B1, R2, G2, B2
(`complete-pinout.md:12-25`); 3.3 V to 5 V level shifting on every HUB75 signal
(`official-specs.md:23`); the level shifters run from the P2 board's 5 V (`complete-pinout.md:114`);
every signal is a P2 output (`complete-pinout.md:110`).

**Wrong (6):**

| # | Capture says | Schematic shows |
|---|---|---|
| X1 | `complete-pinout.md:113` "5V power passed through from P2 board to HUB75 connector" | +5VA reaches U1/U2 VCC and nothing else; J7 carries no +5 V |
| X2 | `official-specs.md:81` HUB75 pin 4 = GND | pin 4 = `H75_UNUSED_OUT`, wired only to through-hole J6; not grounded |
| X3 | `official-specs.md:85, :95` pin 8 = GND; "E signal (if needed) is typically on a separate connection" | pin 8 = **E_OUT**; the sheet: "GND here is Really E" |
| X4 | `complete-pinout.md:26-27` offsets 14, 15 "(unused)" | buffered to 5 V by U1 and brought out on J5; also brought out unbuffered on J4 |
| X5 | `complete-pinout.md:31-36` upper header = P16–P27, lower = P28–P33 | each 2x6 header carries 8 I/O: J2 = offsets 0–7, J1 = offsets 8–15 |
| X6 | `official-specs.md:99-120`, `preliminary-knowledge.md:37-58` pin map R1=0 … CLK=6 … E=13 | CLK=0, OEb=1, LATCH=2, A–E=3–7, R1–B2=8–13 |

Also internally inconsistent: `preliminary-knowledge.md:32` puts E at "32+ row panels" where the
other two captures say 64-row. The schematic is silent on panel row counts.

**Not decided by the schematic (held for the designer):** the host-board list, the
address-line → panel-row mapping (A-B-C → 16-row, A-B-C-D → 32-row, A-B-C-D-E → 64-row), the
header form ("female pass-through"), and the retiring/limited-stock status. Routed to
`KNOWLEDGE-GAPS.md` Part B (Stephen) as Q-012 — **answered the same day: all four confirmed**
(designer's statement, *Product facts confirmed*). The captures' generic panel material (scan
rates, resolutions, pixel pitches, daisy-chaining, wiring advice, toolchain list) was not
confirmed and is removed from the KB.

**Confirmed by the designer (2026-10-10):** board size 1.9 x 2.8 in (48 x 71 mm, hand-measured),
under 50 mA, 70 MHz maximum clock limited by the level shifters; and the four product facts above.

**Disposition of the captures:** superseded. Each claim is either confirmed above (and now cites the
schematic or the designer's statement), proven wrong, or held for the designer. Moved to
`archived/` in this folder (tracked; git history keeps the originals too). Nothing downstream
cites them by path any more.

## Published-KB conflicts routed

`hardware/hub75_adapter.yaml` carried X1 (5 V "and the connector") and X4 (offsets 14, 15 "Not
connected to a HUB75 signal"). It also omits the 74HCT244 buffers, the always-on output enables,
the J3 probe header and the J4/J5/J6 through-holes. Routed to F-567 in
`P2KB-CORRECTION-FINDINGS.md` and applied by the YAML head in the same session.

## Source errata

**None.** The one place the sheet could mislead, the DATA-IN picture labelling pin 8 GND, is
annotated on the sheet itself ("GND here is Really E").

## Trust

**🏆 — golden.** The designer's own schematic, read directly from the rendered sheet, with the
reading archived as committed images and the header mapping held by two independent signals. The
three figures the sheet lacks are the designer's own, recorded verbatim and dated.
