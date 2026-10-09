# SUPERSEDED: `complete-spin2-operators.md`

**Superseded by:** `engineering/ingestion/sources/spin2-v55/spin2-v55-operator-reference.md` (generated 2026-10-09 directly from the operator table in `Parallax Spin2 Documentation v55.docx`; every token compile-probed with pnut-ts).
**Audit note of record:** `engineering/ingestion/sources/spin2-v55/spin2-v55-operator-reextraction-audit.md`.
**Study rows:** S-267, S-268, S-269 (and S-276, S-277) in `engineering/analysis/2026-10-08-p2kb-close-out-study.md`; task «#405».

## What the superseded file is

`complete-spin2-operators.md` in this folder is an **authored summary, not an extraction**. It was never produced from the DOCX table, and it carries P1 carry-over and invented tokens. It is **kept unedited, for lineage only**. Do not cite it as a source; do not edit it. Use the v55 operator reference above.

## Known defects (line numbers in the superseded file)

| Lines | Defect | Evidence |
|---|---|---|
| `:25` | Lists `+<=>` (unsigned comparison). No such operator. | pnut-ts rejects `CON x = 3 +<=> 5` |
| `:26`, `:174` | Lists `===`. No such operator. | pnut-ts rejects `CON x = 3 === 5` |
| `:26`, `:175` | Lists `<>>`. No such operator. | pnut-ts rejects `CON x = 3 <>> 5` |
| `:27`, `:185` | Lists `!&&` ("NAND"). No such operator. | pnut-ts rejects `CON x = 3 !&& 5` |
| `:28`, `:189` | Lists `!\|\|` ("NOR"). No such operator. | pnut-ts rejects `CON x = 3 !\|\| 5` |
| `:164` | Shows `a +<=> b`. No such operator (same as `:25`). | as `:25` |
| `:15`, `:71-72` | Lists unary `\|\|x` ("Encode") and `^^x` ("Decode"), which are P1 forms. In v55 `\|\|` and `^^` are binary logical OR / XOR. | pnut-ts rejects `CON x = \|\| 5` and `CON x = ^^ 5` |
| `:15`, `:58-59` | Swaps `!` and `NOT`: states `!` is logical NOT and `NOT` is bitwise NOT. The DOCX has `!` = bitwise NOT (priority 2) and `!!` / `NOT` = logical NOT (priority 12). | v55 reference rows 16-17 |
| `:15` | Puts `NOT` at priority 2 (the DOCX gives `!!`, `NOT` priority 12). | v55 reference row 16 |
| `:343` | States that float operators "can mix with integer operations (auto-conversion)". The DOCX has no such statement; FLOAT(), ROUND() and TRUNC() are the conversions. | v55 reference rows 82-84 and footnotes |
| `:4`, `:384` | Counts "52 operators" / "52+" in "16 precedence levels". The DOCX operator table has 84 data rows and priority values 1-17. | v55 reference "Counts" |
| `:21-28` | Priority levels 8-13 are shifted. The DOCX gives `/` `//` `+/` `+//` priority 7 (summary: 8); `+` `-` priority 8 (summary: 9 and 10); `#>` `<#` priority 9 (summary: 11); comparisons and equality all priority 11 (summary: 12 and 13); `&&` 13 (summary: 14); `^^` 14 (summary: listed as `XOR` at 15). | v55 reference rows 41-78 |
| `:14`, `:49` | Treats `++` `--` `??` as "pre/post" with a post-`??` form; the DOCX has only the pre form of `??`. | v55 reference rows 1-10 |
| `:14-30` | Omits the float compares (`<.`, `<=.`, `==.`, `<>.`, `>=.`, `>.`) from the precedence table. | v55 reference rows 61, 64, 66, 68, 71, 74 |
| `:273-274` | Gives ADDBITS / ADDPINS no priority (they are absent from the table at `:14-30`); the DOCX gives both priority 10. `ADDBITS` is described as "OR pin masks together", while the DOCX says "Make bitfield, (x & $1F) \| (y & $1F) << 5". | v55 reference rows 57-58 |
| `:29`, `:207`, `:294` | Says the ternary `? :` is "PUB/PRI only" and "NO ternary in CON". The DOCX header says "Term (All blocks)" and pnut-ts accepts `CON x = 1 ? 2 : 3`. | v55 reference row 79 |
| `:30`, `:237-239` | Lists `AND=`, `OR=`, `XOR=` as assign forms; the DOCX lists `&&=`, `^^=`, `\|\|=`. | v55 reference rows 76-78 |
| `:369` | Uses `\|<` ("create single-bit mask"), which is not in the DOCX operator table (the table has `DECOD`). | v55 reference row 23 |

The subset of these tokens the compiler rejects was probed by the arbiter (study S-267) and again, with the commands recorded, in the v55 reference "Verification" section (negative controls).

## Inbound references that still point at the superseded file

Not re-pointed now; they are re-pointed in the close-out sprint. `git grep -n complete-spin2-operators` at 2026-10-09 finds:

**KB (`deliverables/ai/P2/`)**
- `deliverables/ai/P2/language/spin2/operators/op_addmodulo.yaml:21` and `:145` (cite `complete-spin2-operators.md:715`, and `:62` / `:103`; the superseded file has only 384 lines, so `:715` does not exist in it).
- `deliverables/ai/P2/language/spin2/spin2-language-schema.yaml:19` (lists the file as a source).

**Engineering**
- `engineering/knowledge-base/P2-support/extractors/spin2-operators-extractor.py:3`, `:13` (an extractor that reads the summary).
- `engineering/operations/P2KB-CORRECTION-FINDINGS.md:139`, `:150`, `:334`, `:360`, `:369` (register entries, including the reverted F-547 edit).
- `engineering/operations/correction-sweeps/2026-10-05-register-reconciliation-P2KB-CORRECTION-FINDINGS-archive.md:1313` (archived).
- `engineering/analysis/2026-10-08-p2kb-close-out-study.md:566`, `:569`, `:580` (the study).
- `engineering/analysis/archived/2026-08-27-yaml-release-change-ledger.md:251`, `:1525` (archived).
