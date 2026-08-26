# P2 to mikroBUS Click Adapter (#64008) — Extraction Audit

**Sources**:
- `64008-RevA-P2-Click-Adapter-SCHEMATIC-OS.pdf` — Rev A, 10 Aug 2020, 1 p A4, 59,249 B.
  Parallax Inc., **Open Source Hardware, CC BY-SA 4.0** (stated in the sheet's title block).
- `64008-RevA-P2-Click-Adapter-SCHEMATIC-OS.docx` — 7,181 B, title-block template only.
- `p2-click-adapter-catalog-page.txt` — product-page narrative, supplied by Stephen 2026-08-26
  from https://www.parallax.com/product/p2-to-mikrobus-click-adapter

**Mode**: new ingestion (no prior extraction; #64008 had **no** source folder and **no** hardware YAML)
**Extraction date**: 2026-08-26
**Tooling**: `pdftotext` (text-layer probe) - `pdfimages`/XObject census - `pdftoppm` 200/600 dpi
(rendered-page visual read) - `unzip` + `document.xml` inspection (DOCX)

## Pre-flight: what each file actually carries

This is the finding that shaped the whole pass. **Neither file carries the schematic as
extractable content.**

| File | Bytes | Text chars | Media / XObjects | Verdict |
|---|---|---|---|---|
| `...SCHEMATIC-OS.pdf` | 59,249 | **407** | **0 image XObjects** | Title block only in text layer; body is **vector art, text converted to curves** |
| `...SCHEMATIC-OS.docx` | 7,181 | 468 | **0 media, 0 drawing objects** | Title-block template. Carries **no schematic at all** |

The DOCX was confirmed empty of drawings by inspecting `word/document.xml` for `w:drawing`,
`v:shape`, `pic:pic`, and `w:object` markers — **zero of each**. It is not a lossy copy of the
schematic; it is the title block that was used to produce the sheet.

**Negative control on the PDF text layer** (`pdftotext <file> - | grep -c <token>`):

| token | count |
|---|---|
| `AN` `RST` `MISO` `MOSI` `SCK` `PWM` `SDA` `SCL` `J100` `J102` | **0** each |
| `mikroBUS` | 2 (title block) |

Every net name, signal name, and reference designator returns zero. **No text-extraction tool can
recover this sheet** — `pdf2md`, `pdf-layout`, and `camelot` all read the same empty body — and
`pdf-ocr` has no raster to work on (0 image XObjects). Forced OCR of a *rendered* page was
unnecessary because the vector art rasterises cleanly and was read directly.

## Extraction path taken

Rendered with `pdftoppm` and read visually:
- whole sheet at 200 dpi -> `assets/render-2026-08-26/sheet-full-200dpi.png`
- each connector at 600 dpi -> three crops under the same folder

All four renders are committed, so the netlist below is **checkable against the archived image**
without re-rendering the PDF. Every value in `p2-click-adapter-netlist.md` was confirmed twice:
once on the 200 dpi whole-sheet read, once on the 600 dpi per-connector crop.

## Coverage

| Sheet element | Captured | Notes |
|---|---|---|
| Title block (part no., rev, date, copyright, license) | YES | from the text layer |
| `J100` — P2 header A, 12 pins | YES | 600 dpi crop |
| `J101` — P2 header B, 12 pins (4 marked no-connect) | YES | 600 dpi crop |
| `J102` — mikroBUS left row, 8 pins | YES | 600 dpi crop |
| `J103` — mikroBUS right row, 8 pins | YES | 600 dpi crop |
| Orientation note (orange, centre) | YES | transcribed verbatim |
| Catalog narrative (features, specs, compatibility) | YES | separate file |

**Coverage: 100%** of the sheet. There is nothing else on it — no revision history table, no
notes block, no BOM, no second page.

## Cross-source reconciliation

**1. The catalog's "12 signals (with 4 spare I/Os)" is confirmed by the sheet, with mechanism.**
The adapter spans two 2x6 headers = 16 I/O positions; `J101` pins 7/8/9/10 are drawn as no-connect,
which is exactly `IO+12`..`IO+15`. Two independent statements, reconciled exactly.

**2. The twelve offsets confirm `architecture/click_module_integration.yaml`, which until now was
`documentation_source: code_analysis`.** All twelve offsets shipped in that file (derived from the
`P2-Click-eInk` driver) match the schematic **exactly** — AN+6, RST+7, CS+8, SCK+9, MISO+10,
MOSI+11, SDA+0, SCL+1, TX+2, RX+3, INT+4, PWM+5. The inference was correct; it now has a primary
source. **0 corrections, 0 conflicts.**

**3. New fact not previously held anywhere in the KB:** the SPI four (CS/SCK/MISO/MOSI) sit in
**header B** while all eight other signals sit in **header A**. On boards where accessory headers
map to separate pin-power groups, the Click socket therefore straddles two groups.

## Gaps routed

- **TX/RX direction semantics are not settled by this sheet.** It gives net names only. The
  MikroElektronika mikroBUS standard is the authority and is **not held in this repo**. The
  existing KB claim that Click `TX` maps to P2 `RX` traces to driver code (`P2-Click-eInk`), a
  peer derivation, not an authority. Routed as a knowledge gap.
- **`5V_B` / `VIO_3V3_B` commoning** with the `_A` rails is not drawn. Not asserted.

## Trust

**GREEN** — official Parallax schematic, explicitly Open Source Hardware (CC BY-SA 4.0), read
directly from the rendered sheet with the extraction path's blind spot proven by negative control
and the reading archived as committed images. Every offset independently corroborated by a driver
implementation that predates this ingestion. No fabrications. The two things the sheet does not
establish are recorded as gaps rather than inferred.
