# Spin2 v55 operator table: re-extraction audit (note of record)

**Date:** 2026-10-09 · **Task:** «#405» · **Study rows:** S-267, S-268, S-269, S-276, S-277 (`engineering/analysis/2026-10-08-p2kb-close-out-study.md`)
**Source:** `Parallax Spin2 Documentation v55.docx` (md5 `69c8a7a9cea8efd003095449a9ec1bf5`), `word/document.xml`, operator table (section "Operators").
**Output:** `spin2-v55-operator-reference.md` (this folder). It supersedes `../spin2-v51/complete-spin2-operators.md` (see `../spin2-v51/SUPERSEDED-BY-spin2-v55-operator-reference.md`).
**Status of other files:** no existing file was edited. This note corrects, in a new file, statements made in earlier files.

## What was extracted

Every row of the operator table, taken from the DOCX XML: table cells are `w:tc`, a cell's `w:t` runs are concatenated with no separator (paragraphs inside a cell joined by one space), entities decoded. Columns as the DOCX has them: operator token(s), term usage, term priority, assign usage, assign priority, description, floating-point/CON note. The DOCX states block scope in each section header row ("Term (PUB/PRI only)", "Term (All blocks)", "Assign (CON only)", and so on); the reference carries those statements per row. The three CON float footnotes are reproduced verbatim.

## Counts (computed by the generator; also in the reference's "Counts" section)

| Measure | Value |
|---|---|
| Table rows (all) | 93 |
| Section header rows | 9 (Var-Prefix, Var-Postfix, Address, Unary, Binary, Ternary, Assign, Equate, Float Conversions) |
| **Data rows** | **84** |
| Distinct priority values over Term and Assign priority cells | **17** (1 to 17) |
| Distinct term priorities | 16 (1 to 16) |
| Distinct assign priorities | 2 (1 and 17) |
| Compile probes (pnut-ts v1.55.8) | 138 table-derived: 137 PASS, 1 REJECT; 7 negative controls, all REJECT |

The one REJECT is the bare-statement assign form `var\x` (row 8): `v\3` and `v\w` both fail with "Variable needs an operator", while the term form `w := v\3` compiles. It is reported in the reference, not dropped.

## Correction of `spin2-v55-complete-extraction-audit.md:54`

That file (not edited) says, under "Questions ANSWERED", **"Complete operator precedence table (16 levels)" ... CLOSED**, citing `spin2-v55-text.txt:409-494`. Correction, stated here as the audit of record:

- The count "16 levels" was inherited from the superseded authored summary (`complete-spin2-operators.md:4`: "52 operators ... 16 precedence levels"), not read from the table.
- The DOCX table has priority values **1 to 17**. The Term Priority column spans 1 to 16; the assign/equate level is 17 (every binary assign form, `:=` and `=`); the Assign Priority column holds only 1 and 17. The union over both columns is 17 levels.
- The table has **84 data rows**, not 52 operators.
- The line's "CLOSED" status rested on the miscount; the gap (`gaps-consolidated.md #7`) is closed by the new reference, not by the earlier audit.
- Same file, `:55`: the "Full ladder present (`POW LOG2 EXP2 LOG10 EXP10 FSQRT FABS ROUND TRUNC`)" is not borne out by the operator table: it has no `POW`, `LOG2`, `EXP2`, `LOG10` or `EXP10` row (`FSQRT`, `FABS` are rows 27 and 21; `ROUND()` and `TRUNC()` are rows 83 and 84). Whether those five exist elsewhere in the v55 text was not checked in this task.

## Text-extraction run-join defect (for the next full re-ingest)

`spin2-v55-text.txt` inserts a space at DOCX run boundaries inside operator-table cells. The DOCX cells are whole words:

| Text file | DOCX cell (joined without separator) |
|---|---|
| `:414-420` `p ost-increment`, `p ost-decrement`, `p ost-logical-NOT`, `p ost-bitwise-NOT`, `p ost-assign`, `p ost-clear`, `p ost-set` (7 rows) | `post-...` |
| `:434` `ENCOD = var` | `ENCOD= var` |
| `:471` `var ADDPINS = y` | `var ADDPINS= y` |
| `:440` `{ 5'whole , 27'fraction }` (found in this task; not in S-276) | `{5'whole, 27'fraction}` |

No operator is lost or glued; the defect is spacing inside cells (a token such as `ENCOD=` reads as `ENCOD =`). The text file is not edited. **Re-extraction of `spin2-v55-text.txt` with runs joined without a separator is owed to the next full re-ingest.** The text file also collapses doubled spaces that the DOCX keeps (for example "Logical AND  (x <> 0 ..."); the reference keeps them verbatim.

## Source typo in the DOCX

Row 46, `//` (signed divide, return remainder): the term-usage cell reads **`x // 7`**; every other binary row reads `x <op> y`. Recorded as erratum **E-018** in `engineering/ingestion/SOURCE-ERRATA.md` (`CONFIRMED`). The reference reproduces it verbatim; the compiler accepts `x // y` (`CON x = 3 // 5`, PASS).

## Verification summary

All 84 rows were compile-probed (term form in CON for unary, binary, ternary and float-conversion rows; term and assign forms in a PUB for the var-prefix, var-postfix, address and assign rows; each alternate spelling `NOT`, `AND`, `XOR`, `OR` separately). Compiler-rejected table entries: one (`var\x` as a bare statement, row 8). The seven tokens the superseded summary lists that the table does not (`+<=>`, `===`, `<>>`, `!&&`, `!||`, unary `||x`, unary `^^x`) are all rejected by pnut-ts. Details and per-token results: `spin2-v55-operator-reference.md`, "Verification".

## Not done here

- DOCUMENT-LINEAGE entry (arbiter's).
- Re-pointing of the inbound references to the superseded summary (listed in the redirect file) and the KB-wide sweeps (S-268 and S-270 to S-275): close-out sprint.
- Re-extraction of `spin2-v55-text.txt` (above).
