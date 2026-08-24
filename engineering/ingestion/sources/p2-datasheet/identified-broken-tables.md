# Identified Broken Tables in P2 Datasheet Narrative

**Status: CLOSED 2026-08-24 — all ten resolved.** Eight recovered with their structure intact, two
determined not to be tables in this document. Full method, evidence and per-cell reconciliations:
`p2-datasheet-complete-extraction-audit.md` and `complete-tables-reference.md`.

**Original list, 2025-09-05.** These tables lost their column structure during the 2025 extraction
(`p2-datasheet-narrative.txt`). Each item below keeps its original text; the disposition line is
what 2026-08-24 measured.

**Extraction ladder used** (per table, until it came out): `camelot lattice` → `camelot stream` →
`pdf-layout` → rendered-page read (`pdftoppm`) → `pdf2md`. **No OCR was needed** — the PDF has a
complete text layer. No table required all five.

---

## 1. **Memory Configuration Table** (Page 1)
- Should show: Region | Depth | Width | PC Address Range | PASM Address Range
- Currently: Just headers with no alignment

✅ **RECOVERED — `camelot lattice`, first pass, 5 x 5 clean.** Page 1 confirmed. In
`complete-tables-reference.md` § *Page 1 — RAM Memory Configuration*. Column headers are actually
*Program Counter Address Range (Hex)* and *PASM Instruction D/S Address Range (Hex)*.

## 2. **Pin Descriptions Table** (Page 5)
- Should have: Pin Name | Direction | V(typ) | Description
- Currently: Mixed up with descriptions flowing into wrong columns

✅ **RECOVERED — `camelot lattice`, 10 x 4.** **Page correction: the table is on page 6.** The
*section* "Pin Descriptions" begins on page 5 (the datasheet's own TOC says `Pin Descriptions | 5`)
and carries three bullets about the pinout; the table itself is overleaf. Both page claims are right
about different things. Cross-checks identical to P2 Hardware Manual Table 4.

## 3. **Smart Pin Mode Configuration** (around line 1736+)
- Completely incomprehensible - just shows:
  ```
  OUT
  CIOHHHLLL
  DIR
  ```
- Should probably be a mode number with bit field descriptions?

✅ **RECOVERED — this is the (M) Pin Mode table on page 24**, 24 rows x 9 columns.
`camelot lattice` recovered the cell structure but space-joined the single-character columns; the
rows were re-paired and then **machine-verified**: every non-empty cell (204 of 216) found verbatim in the independent
`pdf-layout` capture, with a negative control proving the check can fail. Identical to Hardware
Manual Table 18. The page-24 *Pin Mode Legend* (which `lattice` interleaved into one cell) is
recovered alongside it from `pdf-layout`.

## 4. **DC Characteristics Table** (Page 34)
- Headers visible but data not aligned
- Should show: Parameter | Min | Typ | Max | Units

✅ **RECOVERED — `camelot lattice`, corroborated by `pdf-layout`, a rendered-page read, and
`pdf2md`; all four agree.** **Page correction: pages 47-48, not page 34.** The datasheet's own TOC
reads `DC Characteristics | 47`. Columns are Symbol | Parameter | Conditions | Min | Typ | Max |
Units. Four rows on p.47 (`Vdd`, `Vxxyy`, `Vih`, `Iil`) and four continuation rows on p.48 (`Vol`,
`Voh`, `Iq Vdd`, `Iq Vxxyy`).

## 5. **AC Characteristics Table** (Page 35)
- Similar to DC - structure lost
- Missing clock frequency ranges, timing parameters

✅ **RECOVERED — all four paths agree.** **Page correction: page 48, not page 35.** The TOC reads
`AC Characteristics | 48`.

🔴 **The clock frequency ranges are there; the "timing parameters" are not, and never were.** The
table contains **exactly two symbols** — `Freq` (five oscillator sources, with Min/Typ/Max) and
`Cin` (four XI/XO capacitance modes). There is no propagation-delay row, no rise-time row and no
input-timing row. Page 48 was **rendered and read** to establish that this is the source being
silent rather than the extractor failing — the distinction that the whole recovery exists to make.
See the audit's §5.

## 6. **I/O Pin Equivalent Circuit Table**
- Seems to be completely missing or reduced to text descriptions

✅ **RESOLVED — it is not a table.** Pages 26-32 carry one I/O-pin circuit diagram plus **24
equivalent schematics**, four to a page, as raster figures. Both table paths correctly report
nothing there; those pages' text layer is the heading and the footer only. Already captured as 25
images in `assets/images-20250906/`. The on-figure drive legend was read off the rendered image and
is transcribed in `complete-tables-reference.md`.

## 7. **Smart Pin Mode Summary**
- Should be a comprehensive table of all Smart Pin modes
- Currently scattered text descriptions

✅ **RECOVERED — the (S) Smart Pin Modes table, pages 34-35, 35 rows.**

🔴 **This is the one that would have shipped wrong.** `camelot lattice` fused each `%SSSSS` value to
its superscript footnote marker, emitting **six-digit values for a five-bit field** (`001001`,
`110111`, `111001`, …). `pdf-layout`, a rendered-page read, and `pdf2md` each independently show
`00100¹`, `11011¹`, `11100¹` … with footnote 1 = *"OUT signal overridden"*. Ten mode numbers were
corrected this way.

## 8. **Clock Mode Settings**
- The %DDDDDD patterns suggest a bit field table that's been linearized

✅ **RECOVERED — page 18, three tables.** `%E` / `%DDDDDD` / `%MMMMMMMMMM` / `%PPPP` (PLL Setting);
`%CC` (XI/XO configuration); `%SS` (clock source). `%PPPP`'s 16 value→effect pairs (`0`→`VCO / 2` …
`15`→`VCO / 1`) were rebuilt from `pdf-layout` after `lattice` linearized the value column.

⚠️ **A cross-source conflict was found in this table and filed as F-330:** the datasheet says the
VCO *"should be kept within 100 MHz to 200 MHz"* (and repeats it on p.19); the P2 Hardware Manual's
equivalent table says **350 MHz**. The Silicon Doc agrees with the datasheet and identifies 350 MHz
as the *overclock* ceiling.

## 9. **Boot Source Selection**
- Probably was a table showing boot pins and their functions

✅ **RESOLVED — there is no such table in this document**, and the 2025 note's own "probably" was
the right instinct. The datasheet's boot treatment is page-11 prose (*"the Bootloader checks the boot
pattern (configuration) on pins P59-P61"*) closing with *"See Propeller 2 Hardware Manual's Boot Up
procedure section for more information."* Page 10 shows boot-mode selection as a **switch in a
schematic** plus two bullets (closed = SPI Flash, open = microSD), read off the rendered page.
`lattice` finds no table on pp.8-11; `stream` returns only the bullet prose.

**The table the note expected exists — in the P2 Hardware Manual** (its 9-row *Boot Pattern* table,
`sources/p2-hardware-manual/complete-tables-reference.md` Table 5), exactly where the datasheet
points. Nothing is lost.

## 10. **HUBSET Bit Fields**
- Register bit assignments lost their columnar format

✅ **RECOVERED — page 18.** The instruction format line
`HUBSET ##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS` plus the three field tables of item 8. Items 8
and 10 are the same content filed twice.

---

## The question this file used to end on

> *"Would it help if I showed you specific line numbers where these broken tables appear? Or would
> you prefer to explain how one of these tables should actually be structured?"*

**Answered by doing the work, not by asking.** Neither was needed: the tables were recovered
mechanically from the PDF by four independent tools and reconciled against each other, and the
disputed cells were settled by rendering the page and looking at it. The question is why this file
sat unresolved for eleven months, and it is the reason a table recovery should never terminate in a
request for human input that no one is waiting to answer.
