# edge-standard-module — image catalog, 2026-08-26

**Source:** `P2-EC-Edge-Module-RevD-Product-Guide-3.0.pdf` (13 pp, Google Docs renderer).
**Method:** `pdfimages -all -p` (PDF-only source; no DOCX exists). **OCR:** `tesseract --psm 6`.

**Quality control is OCR yield, not dominant colour.** The `#000000` test is unreliable on this
corpus — see the silicon-doc catalog, where transparent line art scored 100% black while reading fine.
All 6 assets returned substantive text.

| Asset | Page | Dim | Content (OCR locator) |
|---|---|---|---|
| `edge-001-000.png` | 1 | 904 x 152 | PARALLAX  |
| `edge-001-001.png` | 1 | 1789 x 1312 | e s = © = ano? oe) i i i ee rn ce C peras = = > = rT BGay Sorre |
| `edge-001-002.png` | 1 | 1789 x 1312 | e P57 P56 «=Ss« P2-EC REV D Ps BOOT MODE JFLasH] a v SERIAL ON |
| `edge-003-003.png` | 3 | 1664 x 1202 | PARALLAX F3o,FR/ e i ‘ssa @, _ etm = Prt rim 17 BB Soneee= GUH |
| `edge-009-004.png` | 9 | 1527 x 1513 | o o re) = SEnunS-oO0nonGbRHOOntAmMAdD-oOBoODD eeerSerSerSereSerS |
| `edge-012-005.png` | 12 | 2048 x 1642 | - 4 P57 P56 P2-EC REV D \ \ e e BOOT MODE JFtasH] « v_ [SERIAL  |

## The F-250 failure, demonstrated live on this corpus

`edge-001-002.png` and `edge-012-005.png` are photographs of the module showing the boot-mode
silkscreen. **Tesseract reads that silkscreen as `BOOT MODE JFLasH] a v SERIAL ONLY`.**

The board is printed `FLASH △ ▽`. **OCR turned `△` into `a` and `▽` into `v`** — precisely the
substitution F-250 records from the #64000 Eval Board guide, reproduced here on a different
document. Had the boot-mode table been recovered by OCR, the switch labels would have been
silently wrong, and a wrong boot-mode table is the kind of error a user discovers with a board
that will not boot.

**It was not recovered by OCR.** Three independent legs agree:

1. **`camelot lattice`** → `edge-page-6-table-1.csv`, triangles intact as `△` / `▽`.
2. **The PDF text layer** (`pdftotext -layout`) → `edge-standard-module-text.txt:195-225`, same
   6 rows, same glyphs, plus the narrative that pins them down.
3. **The narrative's own tip** → *"△ and ▽ are both connected to the Propeller 2 I/O pin P59; one
   with a pull-up resistor to 3.3V, and the other with a pull-down resistor to GND."*

OCR was used **only** as a locator for cataloguing the photographs, and no value in this source's
records comes from it.
