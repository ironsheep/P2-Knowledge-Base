# Spin2 v55 operator reference (extracted from the DOCX operator table)

- **Source file:** `engineering/ingestion/sources/spin2-v55/Parallax Spin2 Documentation v55.docx`, `word/document.xml`, the table whose first cell is "Var-Prefix Operators" (section "Operators").
- **Source md5:** `69c8a7a9cea8efd003095449a9ec1bf5`
- **Generated:** 2026-10-09
- **Generator:** a one-off parser (`parse.py` + `gen.py`) kept in the session scratchpad, **not kept in the repo**. Table cells are `w:tc`; a cell's `w:t` runs are concatenated with **no separator** (paragraphs inside one cell are joined by a single space); XML entities decoded. Nothing was transcribed by hand.
- **Compiler used for the Verification section:** `pnut-ts` v1.55.8.
- **Supersedes** `sources/spin2-v51/complete-spin2-operators.md` (an authored summary, not an extraction; see `sources/spin2-v51/SUPERSEDED-BY-spin2-v55-operator-reference.md`).
- Block scope: the DOCX states it in each section's header row (for example "Term (PUB/PRI only)", "Term (All blocks)", "Assign (CON only)"); the Scope columns below reproduce those header statements verbatim. The final DOCX column ("Floating-Point Operator") is reproduced as "Floating-point / CON note". A scope is shown only where the row has the corresponding usage cell. An em dash (—) in any cell means the DOCX cell is blank. Cell text is otherwise verbatim, including doubled spaces.

## Section header rows (verbatim)

| Section | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 | Col 7 |
|---|---|---|---|---|---|---|
| Var-Prefix Operators | Term (PUB/PRI only) | Term Priority | Assign (PUB/PRI only) | Assign Priority | Description | — |
| Var-Postfix Operators | Term (PUB/PRI only) | Term Priority | Assign (PUB/PRI only) | Assign Priority | Description | — |
| Address Operators | Term (PUB/PRI only) | Term Priority | — | — | Description | — |
| Unary Operators | Term (All blocks) | Term Priority | Assign (PUB/PRI only) | Assign Priority | Description | Floating-Point  Operator |
| Binary Operators | Term (All blocks) | Term Priority | Assign (PUB/PRI only) | Assign Priority | Description | Floating-Point  Operator |
| Ternary Operator | Term (All blocks) | Priority (term) | — | — | Description | — |
| Assign Operator | — | — | Assign (PUB/PRI only) | Priority | Description | — |
| Equate Operator | — | — | Assign (CON only) | Priority | Description | — |
| Float Conversions | Term (All blocks) | — | — | — | Description | Floating-Point  Operator |

## Operator table (one row per DOCX data row)

| # | Section | Operator token(s) | Term usage | Term priority | Assign usage | Assign priority | Description | Floating-point / CON note | Term scope | Assign scope |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Var-Prefix Operators | `++ (pre)` | `++var` | 1 | `++var` | 1 | Pre-increment var, return var | — | PUB/PRI only | PUB/PRI only |
| 2 | Var-Prefix Operators | `-- (pre)` | `--var` | 1 | `--var` | 1 | Pre-decrement var, return var | — | PUB/PRI only | PUB/PRI only |
| 3 | Var-Prefix Operators | `?? (pre)` | `??var` | 1 | `??var` | 1 | Iterate long var per XORO32, return pseudo-random value | — | PUB/PRI only | PUB/PRI only |
| 4 | Var-Postfix Operators | `(post) ++` | `var++` | 1 | `var++` | 1 | Return var, post-increment var | — | PUB/PRI only | PUB/PRI only |
| 5 | Var-Postfix Operators | `(post) --` | `var--` | 1 | `var--` | 1 | Return var, post-decrement var | — | PUB/PRI only | PUB/PRI only |
| 6 | Var-Postfix Operators | `(post) !!` | `var!!` | 1 | `var!!` | 1 | Return var, post-logical-NOT var (0 → -1, non-0 → 0) | — | PUB/PRI only | PUB/PRI only |
| 7 | Var-Postfix Operators | `(post) !` | `var!` | 1 | `var!` | 1 | Return var, post-bitwise-NOT var | — | PUB/PRI only | PUB/PRI only |
| 8 | Var-Postfix Operators | `(post) \` | `var\x` | 1 | `var\x` | 1 | Return var, post-assign x to var | — | PUB/PRI only | PUB/PRI only |
| 9 | Var-Postfix Operators | `(post) ~` | `var~` | 1 | `var~` | 1 | Return var, post-clear all bits in var | — | PUB/PRI only | PUB/PRI only |
| 10 | Var-Postfix Operators | `(post) ~~` | `var~~` | 1 | `var~~` | 1 | Return var, post-set all bits in var | — | PUB/PRI only | PUB/PRI only |
| 11 | Address Operators | `^@` | `^@anyvar` | 1 | — | — | Field pointer to any hub or register variable, including bitfield | — | PUB/PRI only | — |
| 12 | Address Operators | `@` | `@hubvar` | 1 | — | — | Hub address of VAR/PUB/PRI/DAT variable | — | PUB/PRI only | — |
| 13 | Address Operators | `@` | `@method` | 1 | — | — | Pointer to method, may be  @object{[i]}.method | — | PUB/PRI only | — |
| 14 | Address Operators | `@@` | `@@x` | 1 | — | — | Hub address of this object + x,  'DAT x long @dat_symbol' | — | PUB/PRI only | — |
| 15 | Address Operators | `#` | `#reg_symbol` | 1 | — | — | Register address of cog/LUT symbol | — | PUB/PRI only | — |
| 16 | Unary Operators | `!!, NOT` | `!!x` | 12 | `!!= var` | 1 | Logical NOT (0 → -1, non-0 → 0) | — | All blocks | PUB/PRI only |
| 17 | Unary Operators | `!` | `!x` | 2 | `!= var` | 1 | Bitwise NOT (1's complement) | — | All blocks | PUB/PRI only |
| 18 | Unary Operators | `-` | `-x` | 2 | `-= var` | 1 | Negate (2's complement) | CON only * | All blocks | PUB/PRI only |
| 19 | Unary Operators | `-.` | `-.x` | 2 | — | — | Floating-point negate (toggles MSB) | All blocks | All blocks | — |
| 20 | Unary Operators | `ABS` | `ABS x` | 2 | `ABS= var` | 1 | Absolute value | CON only * | All blocks | PUB/PRI only |
| 21 | Unary Operators | `FABS` | `FABS x` | 2 | — | — | Floating-point absolute value (clears MSB) | All blocks | All blocks | — |
| 22 | Unary Operators | `ENCOD` | `ENCOD x` | 2 | `ENCOD= var` | 1 | Encode MSB, 0..31 | — | All blocks | PUB/PRI only |
| 23 | Unary Operators | `DECOD` | `DECOD x` | 2 | `DECOD= var` | 1 | Decode, 1 << (x & $1F) | — | All blocks | PUB/PRI only |
| 24 | Unary Operators | `BMASK` | `BMASK x` | 2 | `BMASK= var` | 1 | Bitmask, (2 << (x & $1F)) - 1 | — | All blocks | PUB/PRI only |
| 25 | Unary Operators | `ONES` | `ONES x` | 2 | `ONES= var` | 1 | Sum all '1' bits, 0..32 | — | All blocks | PUB/PRI only |
| 26 | Unary Operators | `SQRT` | `SQRT x` | 2 | `SQRT= var` | 1 | Square root of unsigned value | — | All blocks | PUB/PRI only |
| 27 | Unary Operators | `FSQRT` | `FSQRT x` | 2 | — | — | Floating-point square root | — | All blocks | — |
| 28 | Unary Operators | `QLOG` | `QLOG x` | 2 | `QLOG= var` | 1 | Unsigned value to logarithm {5'whole, 27'fraction} | — | All blocks | PUB/PRI only |
| 29 | Unary Operators | `QEXP` | `QEXP x` | 2 | `QEXP= var` | 1 | Logarithm to unsigned value | — | All blocks | PUB/PRI only |
| 30 | Binary Operators | `>>` | `x >> y` | 3 | `var >>= y` | 17 | Shift x right by y bits, insert 0's | — | All blocks | PUB/PRI only |
| 31 | Binary Operators | `<<` | `x << y` | 3 | `var <<= y` | 17 | Shift x left by y bits, insert 0's | — | All blocks | PUB/PRI only |
| 32 | Binary Operators | `SAR` | `x SAR y` | 3 | `var SAR= y` | 17 | Shift x right by y bits, insert MSB's | — | All blocks | PUB/PRI only |
| 33 | Binary Operators | `ROR` | `x ROR y` | 3 | `var ROR= y` | 17 | Rotate x right by y bits | — | All blocks | PUB/PRI only |
| 34 | Binary Operators | `ROL` | `x ROL y` | 3 | `var ROL= y` | 17 | Rotate x left by y bits | — | All blocks | PUB/PRI only |
| 35 | Binary Operators | `REV` | `x REV y` | 3 | `var REV= y` | 17 | Reverse order of bits 0..y of x and zero-extend | — | All blocks | PUB/PRI only |
| 36 | Binary Operators | `ZEROX` | `x ZEROX y` | 3 | `var ZEROX= y` | 17 | Zero-extend above bit y | — | All blocks | PUB/PRI only |
| 37 | Binary Operators | `SIGNX` | `x SIGNX y` | 3 | `var SIGNX= y` | 17 | Sign-extend from bit y | — | All blocks | PUB/PRI only |
| 38 | Binary Operators | `&` | `x & y` | 4 | `var &= y` | 17 | Bitwise AND | — | All blocks | PUB/PRI only |
| 39 | Binary Operators | `^` | `x ^ y` | 5 | `var ^= y` | 17 | Bitwise XOR | — | All blocks | PUB/PRI only |
| 40 | Binary Operators | `\|` | `x \| y` | 6 | `var \|= y` | 17 | Bitwise OR | — | All blocks | PUB/PRI only |
| 41 | Binary Operators | `*` | `x * y` | 7 | `var *= y` | 17 | Signed multiply | CON only * | All blocks | PUB/PRI only |
| 42 | Binary Operators | `*.` | `x *. y` | 7 | — | — | Floating-point multiply | All blocks | All blocks | — |
| 43 | Binary Operators | `/` | `x / y` | 7 | `var /= y` | 17 | Signed divide, return quotient | CON only * | All blocks | PUB/PRI only |
| 44 | Binary Operators | `/.` | `x /. y` | 7 | — | — | Floating-point divide | All blocks | All blocks | — |
| 45 | Binary Operators | `+/` | `x +/ y` | 7 | `var +/= y` | 17 | Unsigned divide, return quotient | — | All blocks | PUB/PRI only |
| 46 | Binary Operators | `//` | `x // 7` | 7 | `var //= y` | 17 | Signed divide, return remainder | — | All blocks | PUB/PRI only |
| 47 | Binary Operators | `+//` | `x +// y` | 7 | `var +//= y` | 17 | Unsigned divide, return remainder | — | All blocks | PUB/PRI only |
| 48 | Binary Operators | `SCA` | `x SCA y` | 7 | `var SCA= y` | 17 | Unsigned scale, (x * y) >> 32 | — | All blocks | PUB/PRI only |
| 49 | Binary Operators | `SCAS` | `x SCAS y` | 7 | `var SCAS= y` | 17 | Signed scale, (x * y) >> 30 | — | All blocks | PUB/PRI only |
| 50 | Binary Operators | `FRAC` | `x FRAC y` | 7 | `var FRAC= y` | 17 | Unsigned fraction, (x << 32) / y | — | All blocks | PUB/PRI only |
| 51 | Binary Operators | `+` | `x + y` | 8 | `VAR += y` | 17 | Add | CON only * | All blocks | PUB/PRI only |
| 52 | Binary Operators | `+.` | `x +. y` | 8 | — | — | Floating-point add | All blocks | All blocks | — |
| 53 | Binary Operators | `-` | `x - y` | 8 | `var -= y` | 17 | Subtract | CON only * | All blocks | PUB/PRI only |
| 54 | Binary Operators | `-.` | `x -. y` | 8 | — | — | Floating-point subtract | All blocks | All blocks | — |
| 55 | Binary Operators | `#>` | `x #> y` | 9 | `var #>= y` | 17 | Force x => y, signed | CON only * | All blocks | PUB/PRI only |
| 56 | Binary Operators | `<#` | `x <# y` | 9 | `var <#= y` | 17 | Force x <= y, signed | CON only * | All blocks | PUB/PRI only |
| 57 | Binary Operators | `ADDBITS` | `x ADDBITS y` | 10 | `var ADDBITS= y` | 17 | Make bitfield, (x & $1F) \| (y & $1F) << 5 | — | All blocks | PUB/PRI only |
| 58 | Binary Operators | `ADDPINS` | `x ADDPINS y` | 10 | `var ADDPINS= y` | 17 | Make pinfield, (x & $3F) \| (y & $1F) << 6 | — | All blocks | PUB/PRI only |
| 59 | Binary Operators | `<` | `x < y` | 11 | — | — | Signed less than (returns 0 or -1) | CON only ** | All blocks | — |
| 60 | Binary Operators | `+<` | `x +< y` | 11 | — | — | Unsigned less than (returns 0 or -1) | — | All blocks | — |
| 61 | Binary Operators | `<.` | `x <. y` | 11 | — | — | Floating-point less than (returns 0 or -1) | All blocks | All blocks | — |
| 62 | Binary Operators | `<=` | `x <= y` | 11 | — | — | Signed less than or equal (returns 0 or -1) | CON only ** | All blocks | — |
| 63 | Binary Operators | `+<=` | `x +<= y` | 11 | — | — | Unsigned less than or equal (returns 0 or -1) | — | All blocks | — |
| 64 | Binary Operators | `<=.` | `x <=. y` | 11 | — | — | Floating-point less than or equal (returns 0 or -1) | All blocks | All blocks | — |
| 65 | Binary Operators | `==` | `x == y` | 11 | — | — | Equal (returns 0 or -1) | CON only ** | All blocks | — |
| 66 | Binary Operators | `==.` | `x ==. y` | 11 | — | — | Floating-point equal (returns 0 or -1) | All blocks | All blocks | — |
| 67 | Binary Operators | `<>` | `x <> y` | 11 | — | — | Not equal (returns 0 or -1) | CON only ** | All blocks | — |
| 68 | Binary Operators | `<>.` | `x <>. y` | 11 | — | — | Floating-point not equal (returns 0 or -1) | All blocks | All blocks | — |
| 69 | Binary Operators | `>=` | `x >= y` | 11 | — | — | Signed greater than or equal (returns 0 or -1) | CON only ** | All blocks | — |
| 70 | Binary Operators | `+>=` | `x +>= y` | 11 | — | — | Unsigned greater than or equal (returns 0 or -1) | — | All blocks | — |
| 71 | Binary Operators | `>=.` | `x >=. y` | 11 | — | — | Floating-point greater than or equal (returns 0 or -1) | All blocks | All blocks | — |
| 72 | Binary Operators | `>` | `x > y` | 11 | — | — | Signed greater than (returns 0 or -1) | CON only ** | All blocks | — |
| 73 | Binary Operators | `+>` | `x +> y` | 11 | — | — | Unsigned greater than (returns 0 or -1) | — | All blocks | — |
| 74 | Binary Operators | `>.` | `x >. y` | 11 | — | — | Floating-point greater than (returns 0 or -1) | All blocks | All blocks | — |
| 75 | Binary Operators | `<=>` | `x <=> y` | 11 | — | — | Signed comparison (<,=,> returns -1,0,1) | CON only *** | All blocks | — |
| 76 | Binary Operators | `&&, AND` | `x && y` | 13 | `var &&= y` | 17 | Logical AND  (x <> 0 AND y <> 0, returns 0 or -1) | — | All blocks | PUB/PRI only |
| 77 | Binary Operators | `^^, XOR` | `x ^^ y` | 14 | `var ^^= y` | 17 | Logical XOR  (x <> 0 XOR y <> 0, returns 0 or -1) | — | All blocks | PUB/PRI only |
| 78 | Binary Operators | `\|\|, OR` | `x \|\| y` | 15 | `var \|\|= y` | 17 | Logical OR   (x <> 0 OR  y <> 0, returns 0 or -1) | — | All blocks | PUB/PRI only |
| 79 | Ternary Operator | `? :` | `x ? y : z` | 16 | — | — | If x <> 0 then return y, else return z | — | All blocks | — |
| 80 | Assign Operator | `:=` | — | — | `var := x v1,v2 := x,y` | 17 | Set var to x Set v1 to x, set v2 to y, etc. ( '_' on left = ignore) | — | — | PUB/PRI only |
| 81 | Equate Operator | `=` | — | — | `symbol = x` | 17 | Set symbol to x in CON block | — | — | CON only |
| 82 | Float Conversions | `FLOAT()` | `FLOAT(x)` | — | — | — | Convert integer x to float | All blocks | All blocks | — |
| 83 | Float Conversions | `ROUND()` | `ROUND(x)` | — | — | — | Convert float x to rounded integer | All blocks | All blocks | — |
| 84 | Float Conversions | `TRUNC()` | `TRUNC(x)` | — | — | — | Convert float x to truncated integer | All blocks | All blocks | — |

## Footnotes (verbatim from the DOCX)

- *,**,*** In CON blocks, this operator will take on floating-point functionality when applied to floating-point constants and symbols.
- ** In CON blocks, relational operators (<, <=, ==, <>, >=, >) will return 1.0 or 0.0, instead of integer -1 or 0, when applied to floating-point constants and symbols.
- *** In CON blocks, the <=> operator will return -1.0, 0.0, or 1.0, instead of integer -1, 0, or 1, when applied to floating-point constants and symbols.

## Counts (computed by the generator)

- Header/section rows: 9; data rows: **84** (table rows in total: 93).
- Distinct priority levels across Term and Assign priority cells: **17** (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17).
- Distinct term priorities: 16 (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16). Distinct assign priorities: 2 (1, 17).
- Rows with a non-numeric priority cell: none.
- Probes run: 145 (table-derived: 138, negative controls: 7).

## Verification (pnut-ts compile probes)

Each token/form was compiled with `pnut-ts -q` in a minimal file (`CON` probe, or a `PUB` statement for forms the DOCX scopes to PUB/PRI). Binary and unary operators are probed as `CON x = 3 <op> 5` / `CON x = <op> 5` (floating-point operators the DOCX marks "All blocks" use `3.5` / `5.5`); assign forms are probed in a PUB with `var`→`v` and `x`,`y`→`3`. PASS = exit 0; REJECT = compiler error (first error text shown). A PASS shows the form is accepted by the compiler; it does not check the folded value.

| Row | Token | Kind | Block | Form from table | Probe | Result | Compiler message |
|---|---|---|---|---|---|---|---|
| 1 | `++` | term | PUB | `++var` | `w := ++v` | PASS |  |
| 1 | `++` | assign | PUB | `++var` | `++v` | PASS |  |
| 2 | `--` | term | PUB | `--var` | `w := --v` | PASS |  |
| 2 | `--` | assign | PUB | `--var` | `--v` | PASS |  |
| 3 | `??` | term | PUB | `??var` | `w := ??v` | PASS |  |
| 3 | `??` | assign | PUB | `??var` | `??v` | PASS |  |
| 4 | `++` | term | PUB | `var++` | `w := v++` | PASS |  |
| 4 | `++` | assign | PUB | `var++` | `v++` | PASS |  |
| 5 | `--` | term | PUB | `var--` | `w := v--` | PASS |  |
| 5 | `--` | assign | PUB | `var--` | `v--` | PASS |  |
| 6 | `!!` | term | PUB | `var!!` | `w := v!!` | PASS |  |
| 6 | `!!` | assign | PUB | `var!!` | `v!!` | PASS |  |
| 7 | `!` | term | PUB | `var!` | `w := v!` | PASS |  |
| 7 | `!` | assign | PUB | `var!` | `v!` | PASS |  |
| 8 | `\` | term | PUB | `var\x` | `w := v\3` | PASS |  |
| 8 | `\` | assign | PUB | `var\x` | `v\3` | **REJECT** | 3:error:Variable needs an operator |
| 9 | `~` | term | PUB | `var~` | `w := v~` | PASS |  |
| 9 | `~` | assign | PUB | `var~` | `v~` | PASS |  |
| 10 | `~~` | term | PUB | `var~~` | `w := v~~` | PASS |  |
| 10 | `~~` | assign | PUB | `var~~` | `v~~` | PASS |  |
| 11 | `^@` | term | PUB | `^@anyvar` | `w := ^@v` | PASS |  |
| 12 | `@` | term | PUB | `@hubvar` | `w := @v` | PASS |  |
| 13 | `@` | term | PUB | `@method` | `w := @main` | PASS |  |
| 14 | `@@` | term | PUB | `@@x` | `w := @@3` | PASS |  |
| 15 | `#` | term | PUB | `#reg_symbol` | `w := #rg` | PASS |  |
| 16 | `!!` | term | CON | `!!x` | `x = !!5` | PASS |  |
| 16 | `NOT` | term | CON | `NOT x` | `x = NOT 5` | PASS |  |
| 16 | `!!` | assign | PUB | `!!= var` | `!!= v` | PASS |  |
| 17 | `!` | term | CON | `!x` | `x = !5` | PASS |  |
| 17 | `!` | assign | PUB | `!= var` | `!= v` | PASS |  |
| 18 | `-` | term | CON | `-x` | `x = -5` | PASS |  |
| 18 | `-` | assign | PUB | `-= var` | `-= v` | PASS |  |
| 19 | `-.` | term | CON | `-.x` | `x = -.5.5` | PASS |  |
| 20 | `ABS` | term | CON | `ABS x` | `x = ABS 5` | PASS |  |
| 20 | `ABS` | assign | PUB | `ABS= var` | `ABS= v` | PASS |  |
| 21 | `FABS` | term | CON | `FABS x` | `x = FABS 5.5` | PASS |  |
| 22 | `ENCOD` | term | CON | `ENCOD x` | `x = ENCOD 5` | PASS |  |
| 22 | `ENCOD` | assign | PUB | `ENCOD= var` | `ENCOD= v` | PASS |  |
| 23 | `DECOD` | term | CON | `DECOD x` | `x = DECOD 5` | PASS |  |
| 23 | `DECOD` | assign | PUB | `DECOD= var` | `DECOD= v` | PASS |  |
| 24 | `BMASK` | term | CON | `BMASK x` | `x = BMASK 5` | PASS |  |
| 24 | `BMASK` | assign | PUB | `BMASK= var` | `BMASK= v` | PASS |  |
| 25 | `ONES` | term | CON | `ONES x` | `x = ONES 5` | PASS |  |
| 25 | `ONES` | assign | PUB | `ONES= var` | `ONES= v` | PASS |  |
| 26 | `SQRT` | term | CON | `SQRT x` | `x = SQRT 5` | PASS |  |
| 26 | `SQRT` | assign | PUB | `SQRT= var` | `SQRT= v` | PASS |  |
| 27 | `FSQRT` | term | CON | `FSQRT x` | `x = FSQRT 5` | PASS |  |
| 28 | `QLOG` | term | CON | `QLOG x` | `x = QLOG 5` | PASS |  |
| 28 | `QLOG` | assign | PUB | `QLOG= var` | `QLOG= v` | PASS |  |
| 29 | `QEXP` | term | CON | `QEXP x` | `x = QEXP 5` | PASS |  |
| 29 | `QEXP` | assign | PUB | `QEXP= var` | `QEXP= v` | PASS |  |
| 30 | `>>` | term | CON | `x >> y` | `x = 3 >> 5` | PASS |  |
| 30 | `>>` | assign | PUB | `var >>= y` | `v >>= 3` | PASS |  |
| 31 | `<<` | term | CON | `x << y` | `x = 3 << 5` | PASS |  |
| 31 | `<<` | assign | PUB | `var <<= y` | `v <<= 3` | PASS |  |
| 32 | `SAR` | term | CON | `x SAR y` | `x = 3 SAR 5` | PASS |  |
| 32 | `SAR` | assign | PUB | `var SAR= y` | `v SAR= 3` | PASS |  |
| 33 | `ROR` | term | CON | `x ROR y` | `x = 3 ROR 5` | PASS |  |
| 33 | `ROR` | assign | PUB | `var ROR= y` | `v ROR= 3` | PASS |  |
| 34 | `ROL` | term | CON | `x ROL y` | `x = 3 ROL 5` | PASS |  |
| 34 | `ROL` | assign | PUB | `var ROL= y` | `v ROL= 3` | PASS |  |
| 35 | `REV` | term | CON | `x REV y` | `x = 3 REV 5` | PASS |  |
| 35 | `REV` | assign | PUB | `var REV= y` | `v REV= 3` | PASS |  |
| 36 | `ZEROX` | term | CON | `x ZEROX y` | `x = 3 ZEROX 5` | PASS |  |
| 36 | `ZEROX` | assign | PUB | `var ZEROX= y` | `v ZEROX= 3` | PASS |  |
| 37 | `SIGNX` | term | CON | `x SIGNX y` | `x = 3 SIGNX 5` | PASS |  |
| 37 | `SIGNX` | assign | PUB | `var SIGNX= y` | `v SIGNX= 3` | PASS |  |
| 38 | `&` | term | CON | `x & y` | `x = 3 & 5` | PASS |  |
| 38 | `&` | assign | PUB | `var &= y` | `v &= 3` | PASS |  |
| 39 | `^` | term | CON | `x ^ y` | `x = 3 ^ 5` | PASS |  |
| 39 | `^` | assign | PUB | `var ^= y` | `v ^= 3` | PASS |  |
| 40 | `\|` | term | CON | `x \| y` | `x = 3 \| 5` | PASS |  |
| 40 | `\|` | assign | PUB | `var \|= y` | `v \|= 3` | PASS |  |
| 41 | `*` | term | CON | `x * y` | `x = 3 * 5` | PASS |  |
| 41 | `*` | assign | PUB | `var *= y` | `v *= 3` | PASS |  |
| 42 | `*.` | term | CON | `x *. y` | `x = 3.5 *. 5.5` | PASS |  |
| 43 | `/` | term | CON | `x / y` | `x = 3 / 5` | PASS |  |
| 43 | `/` | assign | PUB | `var /= y` | `v /= 3` | PASS |  |
| 44 | `/.` | term | CON | `x /. y` | `x = 3.5 /. 5.5` | PASS |  |
| 45 | `+/` | term | CON | `x +/ y` | `x = 3 +/ 5` | PASS |  |
| 45 | `+/` | assign | PUB | `var +/= y` | `v +/= 3` | PASS |  |
| 46 | `//` | term | CON | `x // 7` | `x = 3 // 5` | PASS |  |
| 46 | `//` | assign | PUB | `var //= y` | `v //= 3` | PASS |  |
| 47 | `+//` | term | CON | `x +// y` | `x = 3 +// 5` | PASS |  |
| 47 | `+//` | assign | PUB | `var +//= y` | `v +//= 3` | PASS |  |
| 48 | `SCA` | term | CON | `x SCA y` | `x = 3 SCA 5` | PASS |  |
| 48 | `SCA` | assign | PUB | `var SCA= y` | `v SCA= 3` | PASS |  |
| 49 | `SCAS` | term | CON | `x SCAS y` | `x = 3 SCAS 5` | PASS |  |
| 49 | `SCAS` | assign | PUB | `var SCAS= y` | `v SCAS= 3` | PASS |  |
| 50 | `FRAC` | term | CON | `x FRAC y` | `x = 3 FRAC 5` | PASS |  |
| 50 | `FRAC` | assign | PUB | `var FRAC= y` | `v FRAC= 3` | PASS |  |
| 51 | `+` | term | CON | `x + y` | `x = 3 + 5` | PASS |  |
| 51 | `+` | assign | PUB | `VAR += y` | `v += 3` | PASS |  |
| 52 | `+.` | term | CON | `x +. y` | `x = 3.5 +. 5.5` | PASS |  |
| 53 | `-` | term | CON | `x - y` | `x = 3 - 5` | PASS |  |
| 53 | `-` | assign | PUB | `var -= y` | `v -= 3` | PASS |  |
| 54 | `-.` | term | CON | `x -. y` | `x = 3.5 -. 5.5` | PASS |  |
| 55 | `#>` | term | CON | `x #> y` | `x = 3 #> 5` | PASS |  |
| 55 | `#>` | assign | PUB | `var #>= y` | `v #>= 3` | PASS |  |
| 56 | `<#` | term | CON | `x <# y` | `x = 3 <# 5` | PASS |  |
| 56 | `<#` | assign | PUB | `var <#= y` | `v <#= 3` | PASS |  |
| 57 | `ADDBITS` | term | CON | `x ADDBITS y` | `x = 3 ADDBITS 5` | PASS |  |
| 57 | `ADDBITS` | assign | PUB | `var ADDBITS= y` | `v ADDBITS= 3` | PASS |  |
| 58 | `ADDPINS` | term | CON | `x ADDPINS y` | `x = 3 ADDPINS 5` | PASS |  |
| 58 | `ADDPINS` | assign | PUB | `var ADDPINS= y` | `v ADDPINS= 3` | PASS |  |
| 59 | `<` | term | CON | `x < y` | `x = 3 < 5` | PASS |  |
| 60 | `+<` | term | CON | `x +< y` | `x = 3 +< 5` | PASS |  |
| 61 | `<.` | term | CON | `x <. y` | `x = 3.5 <. 5.5` | PASS |  |
| 62 | `<=` | term | CON | `x <= y` | `x = 3 <= 5` | PASS |  |
| 63 | `+<=` | term | CON | `x +<= y` | `x = 3 +<= 5` | PASS |  |
| 64 | `<=.` | term | CON | `x <=. y` | `x = 3.5 <=. 5.5` | PASS |  |
| 65 | `==` | term | CON | `x == y` | `x = 3 == 5` | PASS |  |
| 66 | `==.` | term | CON | `x ==. y` | `x = 3.5 ==. 5.5` | PASS |  |
| 67 | `<>` | term | CON | `x <> y` | `x = 3 <> 5` | PASS |  |
| 68 | `<>.` | term | CON | `x <>. y` | `x = 3.5 <>. 5.5` | PASS |  |
| 69 | `>=` | term | CON | `x >= y` | `x = 3 >= 5` | PASS |  |
| 70 | `+>=` | term | CON | `x +>= y` | `x = 3 +>= 5` | PASS |  |
| 71 | `>=.` | term | CON | `x >=. y` | `x = 3.5 >=. 5.5` | PASS |  |
| 72 | `>` | term | CON | `x > y` | `x = 3 > 5` | PASS |  |
| 73 | `+>` | term | CON | `x +> y` | `x = 3 +> 5` | PASS |  |
| 74 | `>.` | term | CON | `x >. y` | `x = 3.5 >. 5.5` | PASS |  |
| 75 | `<=>` | term | CON | `x <=> y` | `x = 3 <=> 5` | PASS |  |
| 76 | `&&` | term | CON | `x && y` | `x = 3 && 5` | PASS |  |
| 76 | `AND` | term | CON | `x && y` | `x = 3 AND 5` | PASS |  |
| 76 | `&&` | assign | PUB | `var &&= y` | `v &&= 3` | PASS |  |
| 77 | `^^` | term | CON | `x ^^ y` | `x = 3 ^^ 5` | PASS |  |
| 77 | `XOR` | term | CON | `x ^^ y` | `x = 3 XOR 5` | PASS |  |
| 77 | `^^` | assign | PUB | `var ^^= y` | `v ^^= 3` | PASS |  |
| 78 | `\|\|` | term | CON | `x \|\| y` | `x = 3 \|\| 5` | PASS |  |
| 78 | `OR` | term | CON | `x \|\| y` | `x = 3 OR 5` | PASS |  |
| 78 | `\|\|` | assign | PUB | `var \|\|= y` | `v \|\|= 3` | PASS |  |
| 79 | `? :` | term | CON | `x ? y : z` | `x = 1 ? 2 : 3` | PASS |  |
| 80 | `:=` | assign | PUB | `var := x` | `v := 3` | PASS |  |
| 80 | `:=` | assign (multi) | PUB | `v1,v2 := x,y` | `v1, v2 := 3, 4` | PASS |  |
| 81 | `=` | assign | CON | `symbol = x` | `x = 3` | PASS |  |
| 82 | `FLOAT()` | term | CON | `FLOAT(x)` | `x = FLOAT(3)` | PASS |  |
| 83 | `ROUND()` | term | CON | `ROUND(x)` | `x = ROUND(3.5)` | PASS |  |
| 84 | `TRUNC()` | term | CON | `TRUNC(x)` | `x = TRUNC(3.5)` | PASS |  |

**Tally (table-derived probes):** 138 probes, 137 PASS, 1 REJECT.

**Table entries the compiler rejects (reported, not dropped):**

- Row 8, `\` (assign, PUB): `v\3` — 3:error:Variable needs an operator

Note on row 8: the term form `w := v\3` compiles (PASS above); the bare-statement assign form `var\x` listed in the DOCX's Assign column is rejected by pnut-ts v1.55.8 as a statement (a second probe with a variable operand, `v\w`, is rejected with the same message). Reported as found; no interpretation of intent is made here.

### Negative controls (tokens the v51 summary lists that the DOCX table does not)

| Token | Probe | Result | Compiler message |
|---|---|---|---|
| `+<=>` | `x = 3 +<=> 5` | REJECT | 2:error:Expected a constant, unary operator, or "(" |
| `===` | `x = 3 === 5` | REJECT | 2:error:Expected a constant, unary operator, or "(" |
| `<>>` | `x = 3 <>> 5` | REJECT | 2:error:Expected a constant, unary operator, or "(" |
| `!&&` | `x = 3 !&& 5` | REJECT | 2:error:Expected "," or end of line |
| `!\|\|` | `x = 3 !\|\| 5` | REJECT | 2:error:Expected "," or end of line |
| `unary \|\|` | `x = \|\| 5` | REJECT | 2:error:Expected a constant, unary operator, or "(" |
| `unary ^^` | `x = ^^ 5` | REJECT | 2:error:Expected a constant, unary operator, or "(" |

## Known source typo

Row for `//` (signed divide, return remainder): the DOCX Term-usage cell reads `x // 7`, not `x // y` (erratum E-018 in `engineering/ingestion/SOURCE-ERRATA.md`). Reproduced verbatim above.
