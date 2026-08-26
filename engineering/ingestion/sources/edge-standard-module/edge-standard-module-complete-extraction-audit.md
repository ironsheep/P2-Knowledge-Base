# P2 Edge Module (#P2-EC) Rev D — Extraction Audit

**Source:** `P2-EC-Edge-Module-RevD-Product-Guide-3.0.pdf` — Parallax Inc., v3.0, 2022-06-03,
13 pp, 1,526,389 bytes. **PDF-only** — no DOCX exists for this guide.
**Mode:** completion. The row carried **~80%** and was *"the only row with X but no A"* — an
extraction with **no audit document**. This supplies it.
**Extraction date:** 2026-08-26
**Tooling:** `pdftotext -layout` · `camelot lattice` · `pdfimages -all -p` · `tesseract` ·
`audit-extraction-digit-density.py`

## Pre-flight — the F-250 check

`pdftotext -f 1 -l 1` returns clean English **with digits intact** (`(888) 512-1024`,
`(916) 701-8625`). **No invisible numeral loss.** This matters more than usual here: this is a
board Product Guide, the exact document class where F-250 shipped a capture with every digit
silently deleted at `100% (stated)`.

## Digit-density gate (§2a)

| artifact | lines | w/digit | density |
|---|---|---|---|
| `edge-standard-module-text.txt` (new) | 300 | 196 | **65.3%** |
| `edge-standard-module-narrative.txt` (prior) | 327 | 202 | 61.8% |

**Exit 0.** Carrying the tool's caveat rather than paraphrasing it: this detects **total** numeral
loss only, is **blind to partial loss**, and is **never a completeness certificate**.

## Coverage

13/13 pages. **4 ruled tables** recovered by `camelot lattice`, archived under
`assets/tables-2026-08-26/`:

| Table | Page | Content |
|---|---|---|
| `edge-page-6-table-1.csv` | 6 | **Boot Mode Selection** — 6 rows, `FLASH / △ / ▽` |
| `edge-page-10-table-1.csv` | 10 | I/O Pin descriptions |
| `edge-page-11-table-1.csv` | 11 | Other specifications |
| `edge-page-11-table-2.csv` | 11 | **Electrical** — `Symbol / Quantity / Recommended / Maximum / Units` |

Electrical values, read from the table: `5-16 VIN` DC supply **5 / 16 V** · `P0-P63` any I/O pin
**3.3 / 3.6 V** · `RESn` reset input, active low **3.3 / 3.6 V**.

**6/6 images** extracted and catalogued (`assets/images-edge-standard-module-2026-08-26/`).

## Pass 2 — code

**No code.** This is a board Product Guide; it contains no Spin2 or PASM2 listings. `pnut-ts` was
not run because there is nothing to run it on. Stated explicitly rather than left as an empty
folder.

## Triangulation — and a live demonstration of why it is required

The boot-mode table was recovered by **three independent legs**, and the third is what makes the
first two trustworthy:

1. `camelot lattice` — triangles intact as `△` / `▽`.
2. The PDF text layer — same 6 rows, same glyphs, plus the narrative.
3. The narrative's own tip, which pins the glyphs to hardware.

**Why this was not optional.** Tesseract reads the module's boot-mode silkscreen as
`BOOT MODE JFLasH] a v SERIAL ONLY` — it turns **`△` into `a` and `▽` into `v`**. That is exactly
the F-250 substitution, reproduced here on a different document. An OCR-derived boot table would
have carried silently wrong switch labels, and a wrong boot table is discovered by a user with a
board that will not boot.

## Pass 6 — findings

**G-026 CLOSED (ANSWERED).** *"What pin condition selects microSD boot?"* — raised from the Silicon
Doc's omission (E-014), where reviewer comment [25] proposed *a pulldown at P60*.

**The pin is P59, not P60.** Verbatim (`edge-standard-module-text.txt:204-206`):

> *"△ and ▽ are both connected to the Propeller 2 I/O pin **P59**; one with a pull-up resistor to
> 3.3V, and the other with a pull-down resistor to GND. You may see these boot mode selection pins
> referred to in other documentation as **P59 up and P59 down**."*

SD-card boot is **FLASH=OFF**: with ▽ ON, *SD only, no serial window*; with all three OFF, *SD with
a 60 s serial fallback*. Rows 1 and 5 share the all-OFF setting and are disambiguated by **card
presence** — the guide's own wording, not a reconciliation.

**E-014 stands unchanged** — the Silicon Doc still omits microSD boot entirely; this closes the
*mechanism* question, not the omission.

**Cross-check against shipped YAML — no conflict.** `hardware/edge-standard-module.yaml boot_modes`
already carries the full 6-row table, the P59 note, and the row-1-vs-5 disambiguation, correctly
cited. It was simply never connected to G-026.

**Gap ledger, both halves.** Opened: none. Closed: **G-026**.

## Trust

**🏆** — official Parallax Product Guide, clean text layer, tables independently recovered by two
paths and reconciled with a third. No fabrications found. The one hazard in this document is its
silkscreen glyphs, and it was handled by not using OCR for any recorded value.
