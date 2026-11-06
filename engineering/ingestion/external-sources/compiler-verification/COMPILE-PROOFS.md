# P2 Compile Proofs — Register

**What a record is.** Each entry is a fact about what the Spin2/PASM2 compiler accepts or
rejects, **proved by our own compile**, not by reading a document. A record carries the fact, its
class, the proof program in [`proofs/`](proofs/), the exact command, the `pnut-ts` version, the
compiler's **verbatim** output, and the fact's KB home. The lifecycle and field rules are in
[`README.md`](README.md).

> **Authority note.** For legality, the compiler is the authority: `pnut-ts` emits PNut's binary,
> so where it and a document disagree on what compiles, the record decides (study Q9). A record
> says only what the compiler printed. What compiled code *does* is the bench ledger's to prove
> ([`../hardware-verification/P2-EMPIRICAL-FINDINGS.md`](../hardware-verification/P2-EMPIRICAL-FINDINGS.md),
> `EF-NNN`).

**Class legend:** `LEGALITY` (whether the compiler accepts a form; stays CP) · `LAYOUT` (what the
compiler emits for a form it accepts: image bytes, object-image counts, DEBUG listing figures, an
assembled word; stays CP) · `BEHAVIOUR` (what
compiled code does; the compile does not prove it) · `BEHAVIOUR → EF-NNN` (a P2 run has since
proved it; the KB cites the EF).

**Next record ID: `CP-028`** — take the number from this line and advance it in the same edit
that files the record.

**Commands** are run from the repository root with the repository-relative path, so each output
reproduces exactly. The `.bin` a passing run writes is git-ignored here and never committed.

---

## Symbols

### CP-001 · A Spin2 symbol may be at most 30 characters: CON, method, VAR, local and DAT-label names of 30 compile; 31 (and, for CON, 32) are rejected with `Symbol exceeds 30 characters` — `LEGALITY`
*KB:* `language/fundamentals/identifier-rules.yaml`
*Class:* legality. The compiler accepts a 30-character name of each kind tested and rejects a
31-character one; each failing run stops with exit status 1 at the name's first appearance.
*Source:* minimal pairs in `proofs/`, each pair the same program differing only in the name.
The names are `abcdefgh10abcdefgh20abcdefgh30` (30; each `NN` ends at character NN), the same plus
`x` (31), and plus `xy` (32).
- CON name: `cp-001-symbol-30.spin2`, `cp-001-symbol-31.spin2`, `cp-001-symbol-32.spin2`
- method name: `cp-001-method-30.spin2`, `cp-001-method-31.spin2`
- VAR name: `cp-001-var-30.spin2`, `cp-001-var-31.spin2`
- local-variable name: `cp-001-local-30.spin2`, `cp-001-local-31.spin2`
- DAT label: `cp-001-datlabel-30.spin2`, `cp-001-datlabel-31.spin2`

*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (CON, 30):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-30.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-30.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-30.bin (6292 bytes)
pnut-ts: Done
```
*Command (CON, 31):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-31.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-31.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-31.spin2:8:error:Symbol exceeds 30 characters
```
*Command (CON, 32):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-32.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-32.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-symbol-32.spin2:8:error:Symbol exceeds 30 characters
```
*Command (method, 30):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-method-30.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-method-30.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-method-30.bin (6292 bytes)
pnut-ts: Done
```
*Command (method, 31):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-method-31.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-method-31.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-method-31.spin2:6:error:Symbol exceeds 30 characters
```
*Command (VAR, 30):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-var-30.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-var-30.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-var-30.bin (6296 bytes)
pnut-ts: Done
```
*Command (VAR, 31):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-var-31.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-var-31.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-var-31.spin2:7:error:Symbol exceeds 30 characters
```
*Command (local, 30):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-local-30.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-local-30.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-local-30.bin (6292 bytes)
pnut-ts: Done
```
*Command (local, 31):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-local-31.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-local-31.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-local-31.spin2:6:error:Symbol exceeds 30 characters
```
*Command (DAT label, 30):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-datlabel-30.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-datlabel-30.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-datlabel-30.bin (6300 bytes)
pnut-ts: Done
```
*Command (DAT label, 31):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-datlabel-31.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-datlabel-31.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-001-datlabel-31.spin2:7:error:Symbol exceeds 30 characters
```
Each error line points at the name's first appearance: the CON declaration (line 8), the `PUB`
line (6), the `long` declaration in VAR (7), the `PUB` line's local list (6), the DAT label (7).

**Grounds:** contradicts the Parallax *Spin2 Language Documentation* v55 (2026-05-07), which says
"Symbolic names can be up to 32 characters in length." (`spin2-v55-text.txt:166`). Decides study
rows S-251 (v55 says 32, the compiler enforces 30) and S-147 (a 31-character method name is
rejected). Filed as erratum E-020 in `engineering/ingestion/SOURCE-ERRATA.md`. The KB home still
teaches 32 (`identifier-rules.yaml`, S-251); writing 30 there is plan §6 item 3.
*Limits:* 32 characters is run for CON names only; the other kinds are run at 30 and 31. Not run:
method parameter and result names, OBJ instance names, STRUCT names, PASM local labels
(`.name`), and preprocessor symbols (`#define`, `-D`) — the KB claims 32 for the last two
(`preprocessor/define.yaml`, `preprocessor/external-symbols.yaml`), and this record does not
decide them. One compiler version.
*→ EF:* none — legality stays CP.

---

## Operators

### CP-002 · The post-assign operator `var\x` compiles as a term (`w := v\3`) but not alone as a statement (`v\3` → `Variable needs an operator`) — `LEGALITY`
*KB:* `language/spin2/concepts/operators.yaml`
*Class:* legality. The compiler accepts `v\3` where its value is used and rejects it written
alone; the failing run stops with exit status 1. A control shows `v++`, from the same table, is
accepted alone. What `v\3` returns and assigns at run time is not shown.
*Source:* `proofs/cp-002-post-assign-term.spin2` (`w := v\3`), `proofs/cp-002-post-assign-statement.spin2`
(`v\3` alone), `proofs/cp-002-control-post-increment-statement.spin2` (`v++` alone). The three
differ only in the last line.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (term):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-post-assign-term.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-post-assign-term.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-post-assign-term.bin (6296 bytes)
pnut-ts: Done
```
*Command (statement):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-post-assign-statement.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-post-assign-statement.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-post-assign-statement.spin2:7:error:Variable needs an operator
```
*Command (control, `v++` alone):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-control-post-increment-statement.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-control-post-increment-statement.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-002-control-post-increment-statement.bin (6296 bytes)
pnut-ts: Done
```
**Grounds:** contradicts the Parallax *Spin2 Language Documentation* v55 (2026-05-07), Operators
table, Var-Postfix Operators, whose `\` row lists `var\x` in both the "Term (PUB/PRI only)" and
the "Assign (PUB/PRI only)" columns: `| (post) \ | var\x | 1 | var\x | 1 | Return var, p ost-assign x to var |`
(`spin2-v55-text.txt:418`; column heads at `:413`; "p ost" is the extraction's split). The
sibling rows read the same way, and the control shows their Assign form (`v++` alone) compiles;
the `\` row's does not. Decides study row S-280. Filed as erratum E-021. No KB page carries
`var\x` today: the only mention is `\` in the level-1 list of `operators/precedence.yaml`; the
named home is the page that describes the other postfix var-modify operators (`~`, `~~`, `++`,
`--`, `??`) and should teach the term form (plan §6 item 3).
*Limits:* one variable kind (a method local) and one value (3); `x` as an expression other than a
constant is not run. One compiler version.
*→ EF:* none — legality stays CP.

---

## Strings

### CP-003 · In an `@\"..."` string, an unknown escape (`\d`) is rejected with `Expected end of line (m281)`; `\n`, `\\`, `\x01` and `\x00` compile — `LEGALITY`
*KB:* `language/spin2/constructs/escape-strings.yaml`
*Class:* legality. The compiler rejects `\d` (exit status 1) and accepts the four escapes in one
file. What bytes each escape produces, and what `\x00` does to the string, are not shown.
*Source:* `proofs/cp-003-unknown-escape.spin2` (`p := @\"a\db"`), `proofs/cp-003-known-escapes.spin2`
(`@\"a\nb"`, `@\"a\\b"`, `@\"a\x01b"`, `@\"a\x00b"`, each assigned in turn). The unknown-escape
string has the same shape as the four that compile.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (unknown escape):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-003-unknown-escape.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-003-unknown-escape.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-003-unknown-escape.spin2:6:error:Expected end of line (m281)
```
*Command (known escapes):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-003-known-escapes.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-003-known-escapes.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-003-known-escapes.bin (6320 bytes)
pnut-ts: Done
```
**Grounds:** contradicts the Parallax *Spin2 Language Documentation* v55 (2026-05-07), version
history v50, the `@\"string\n"` escape list, which ends "Unknown sequences are just passed
verbatim (i.e. \d = "\d" )." (`spin2-v55-text.txt:59`; the extraction renders the quotes as
`&quot;`). The same list gives "\x01 to \xFF = $01 to $FF" (`:58`); `\x00` compiling lies outside
that range and is not a contradiction — the document is silent on it. Decides study row S-345
(legality half). Filed as erratum E-022. The KB home says the opposite on both points:
unknown escapes "pass through" (`escape-strings.yaml` `restrictions`, `notes`) and `\x00` is
"Not allowed"; correcting it is plan §6 item 3.
*Limits:* one unknown escape (`\d`); other unlisted letters, and `\"`, are not run. One compiler
version.
*→ EF:* none — legality stays CP.

---

## DEBUG

### CP-004 · `DEBUG(C_Z)` compiles in Spin2 only under `{Spin2_v46}` or later, and is rejected inside PASM (a DAT block or inline `ORG`..`END`) with `Expected "("` under `{Spin2_v46}` and `{Spin2_v55}` — `LEGALITY`
*KB:* `language/spin2/debug-commands/c-z.yaml`
*Class:* legality — which DEBUG sites accept `C_Z`, under which version directive, when compiled
with DEBUG (`-d`). Every failing run stops with exit status 1. What `C_Z` prints, in any context,
is behaviour and is not shown (study row S-157 asks it of Spin2; it waits for the bench).
*Source:* in `proofs/`:
- Spin2 method: `cp-004-spin2-none.spin2` (no directive), `cp-004-spin2-v45.spin2`, `cp-004-spin2-v46.spin2`
- DAT PASM block: `cp-004-pasm-v46.spin2`, `cp-004-pasm-v55.spin2`, and the control
  `cp-004-pasm-v55-control.spin2` (the same site with `UHEX(entry)` in place of `C_Z`)
- inline PASM: `cp-004-inline-v55.spin2`

*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d`.

*Command (Spin2, no directive):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-none.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-none.spin2
pnut-ts: Compiling with DEBUG
engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-none.spin2:6:error:Expected an expression term (m172)
```
*Command (Spin2, `{Spin2_v45}`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-v45.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-v45.spin2
pnut-ts: Compiling with DEBUG
engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-v45.spin2:7:error:Expected an expression term (m172)
```
*Command (Spin2, `{Spin2_v46}`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-v46.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-v46.spin2
pnut-ts: Compiling with DEBUG
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-spin2-v46.bin (9235 bytes)
pnut-ts: Done
```
*Command (DAT PASM, `{Spin2_v46}`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v46.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v46.spin2
pnut-ts: Compiling with DEBUG
engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v46.spin2:11:error:Expected "("
```
*Command (DAT PASM, `{Spin2_v55}`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v55.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v55.spin2
pnut-ts: Compiling with DEBUG
engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v55.spin2:11:error:Expected "("
```
*Command (DAT PASM control, `UHEX`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v55-control.spin2`
*Output (2026-10-09; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v55-control.spin2
pnut-ts: Compiling with DEBUG
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-pasm-v55-control.bin (9256 bytes)
pnut-ts: Done
```
*Command (inline PASM, `{Spin2_v55}`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-inline-v55.spin2`
*Output (2026-10-09; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-inline-v55.spin2
pnut-ts: Compiling with DEBUG
engineering/ingestion/external-sources/compiler-verification/proofs/cp-004-inline-v55.spin2:8:error:Expected "("
```
Each error line is the `debug(c_z)` line.

**Grounds:** contradicts the Parallax *Spin2 Language Documentation* v55 (2026-05-07), DEBUG
section: "For PASM, DEBUG() statements can output register values/arrays, hub byte/word/long
arrays, C/Z flags, and constants. PASM syntax is used: implied register or #immediate."
(`spin2-v55-text.txt:913`), and the Miscellaneous commands table row "| C_Z | Output the C and Z
flags as "C=? Z=?". Useful in PASM code." (`:1006`; quotes rendered `&quot;` in the extraction).
The control shows the PASM DEBUG site itself compiles; only `C_Z` there is rejected. The Spin2
version gate agrees with the same document's version history, v46: "New DEBUG command C_Z will
output the states of the C and Z flags, such as "C=0 Z=1"." (`:38`; quotes likewise), and with the KB home's
`requires_version: "Spin2_v46"`. Decides the PASM half of
study row S-157. Filed as erratum E-023.
*Limits:* every command uses `-d`; this records the DEBUG compile only, and says nothing about a
build without `-d`. Version directives run: none, v45, v46 (Spin2); v46, v55 (DAT PASM); v55
(inline PASM). `C_Z` is run alone in each `DEBUG()`; combined with other commands it is not run.
One compiler version.
*→ EF:* none — legality stays CP.

---

## Preprocessor

### CP-005 · `pnut-ts` accepts a `#DEFINE` symbol of 30, 31, 32, 33 and 100 characters and a `-D` symbol of 100, and sees each as defined: it enforces no 32-character limit on preprocessor symbols — `LEGALITY`
*KB:* `language/spin2/preprocessor/define.yaml`
*Class:* legality. Each run compiles with exit status 0. Every proof file names its symbol twice,
in `#define` (or on the command line for the `-D` run) and in `#ifdef`, and carries an `#else`
branch that names an undefined identifier (`no_such_name`), so the file compiles only if `#ifdef`
takes the defined branch. What the preprocessor does with the symbol beyond that is not shown.
*Source:* in `proofs/`, one file per length, differing only in the symbol: `cp-005-define-30.spin2`,
`cp-005-define-31.spin2`, `cp-005-define-32.spin2`, `cp-005-define-33.spin2`,
`cp-005-define-100.spin2`; and `cp-005-dflag-100.spin2` (no `#define`; the symbol arrives by `-D`).
The 30- to 33-character symbols are `abcdefgh10abcdefgh20abcdefgh30` followed by nothing, `x`,
`xy`, `xyz`; the 100-character symbol is nine groups `abcdefghNN` (NN = 10 to 90) then `abcdefg100`.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (`#DEFINE`, 30):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-30.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-30.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-30.bin (6292 bytes)
pnut-ts: Done
```
*Command (`#DEFINE`, 31):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-31.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-31.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-31.bin (6292 bytes)
pnut-ts: Done
```
*Command (`#DEFINE`, 32):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-32.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-32.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-32.bin (6292 bytes)
pnut-ts: Done
```
*Command (`#DEFINE`, 33):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-33.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-33.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-33.bin (6292 bytes)
pnut-ts: Done
```
*Command (`#DEFINE`, 100):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-100.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-100.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-define-100.bin (6292 bytes)
pnut-ts: Done
```
*Command (`-D`, 100):* `pnut-ts -D abcdefgh10abcdefgh20abcdefgh30abcdefgh40abcdefgh50abcdefgh60abcdefgh70abcdefgh80abcdefgh90abcdefg100 engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-dflag-100.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -D abcdefgh10abcdefgh20abcdefgh30abcdefgh40abcdefgh50abcdefgh60abcdefgh70abcdefgh80abcdefgh90abcdefg100 engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-dflag-100.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-005-dflag-100.bin (6292 bytes)
pnut-ts: Done
```
**Grounds:** contradicts the KB home's claim that a preprocessor symbol name is at most 32
characters (`preprocessor/define.yaml` notes; `preprocessor/external-symbols.yaml`, the `-D` parameter
description, `limits.max_name_length` and a note). That claim has no compile behind it; the
compiler, which is the authority for legality, accepts names to 100 characters. Contrast CP-001:
Spin2 symbols (CON, method, VAR, local, DAT label names) stop at 30.
*Limits:* `pnut-ts` only. 100 characters is the longest run; nothing is said about longer names.
`-D` is run once (100), `-U` and `#UNDEF` are not run, and whether the original PNut limits
preprocessor symbols is not tested here. The `#ifdef` proof shows the symbol is defined, not
that it is stored untruncated (a name that differed after character 32 is not run). One
compiler version.
*→ EF:* none — legality stays CP.

### CP-013 · `#PRAGMA EXPORTDEF` defines its symbol in the child objects and not in the file that holds the pragma; `-D` defines it in that file too — `LEGALITY`
*KB:* `language/spin2/preprocessor/pragma-exportdef.yaml`
*Class:* legality — which files see the symbol as defined. The parent's `#ifdef` branch and the
child's `#else` branch each name an undefined identifier, so the program compiles only if the
symbol is undefined in the parent **and** defined in the child.
*Source:* `proofs/cp-013-exportdef-parent.spin2` (holds `#pragma exportdef CP013_FLAG`) and
`proofs/cp-013-exportdef-child.spin2`.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (pragma only):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-013-exportdef-parent.spin2`
*Output (2026-10-13; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-013-exportdef-parent.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-013-exportdef-parent.bin (6316 bytes)
pnut-ts: Done
```
*Command (the same files with `-D`):* `pnut-ts -D CP013_FLAG engineering/ingestion/external-sources/compiler-verification/proofs/cp-013-exportdef-parent.spin2`
*Output (2026-10-13; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -D CP013_FLAG engineering/ingestion/external-sources/compiler-verification/proofs/cp-013-exportdef-parent.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-013-exportdef-parent.spin2:11:error:Expected an expression term (m172)
```
Line 11 is the parent's `#ifdef` branch: with `-D` the symbol is defined in the top file too.
**Grounds:** none ingested — `#PRAGMA` is a PNut-TS extension that no Parallax document covers,
so this record is the proof.
*Command (grandchild arm):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-013-exportdef-grandparent.spin2`
— exit status 0 (`Wrote … cp-013-exportdef-grandparent.bin (9274 bytes)`): the pragma is held in
`cp-013-exportdef-grandparent.spin2`, `cp-013-exportdef-mid.spin2` only passes the call down, and
the same `cp-013-exportdef-child.spin2` (legal only if the symbol is defined) compiles two levels
below. *Limits:* two levels; one compiler version.
*→ EF:* none — legality stays CP.

---

## Operators (continued)

### CP-006 · `POW` binds at the level of `+` `-` `+.` `-.`, left to right: `2.0 POW 3.0 +. 1.0` folds to 9.0, `1.0 +. 3.0 POW 2.0` to 16.0, `2.0 POW 3.0 POW 2.0` to 64.0, and `*.` binds tighter (`2.0 *. 3.0 POW 2.0` folds to about 36.0) — `LEGALITY`
*KB:* `language/spin2/operators/op_POW.yaml`
*Class:* legality — how the compiler groups and folds a constant expression containing `POW`
(compile-time value, read from the listing). It does not show how `POW` evaluates a run-time
operand.
*Source:* `proofs/cp-006-pow-precedence.spin2`, five `DAT` longs under `{Spin2_v51}`, compiled
with `-l`. The listing holds one long per expression, in order.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-l`.

*Command:* `pnut-ts -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-006-pow-precedence.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-006-pow-precedence.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-006-pow-precedence.lst
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-006-pow-precedence.bin (6312 bytes)
pnut-ts: Done
```
*Listing (`cp-006-pow-precedence.lst`, the data lines, verbatim):*
```text
00000- 1C 00 00 80 1E 00 00 00 00 00 10 41 00 00 80 41   '...........A...A'
00010- 00 00 80 42 01 00 10 42 00 00 00 41 00 04 00 00   '...B...B...A....'
```
Reading it: after the 8-byte object header (`1C 00 00 80 1E 00 00 00`), the five longs
are little-endian `$41100000` (9.0), `$41800000` (16.0), `$42800000` (64.0), `$42100001`
(36.000004), `$41000000` (8.0, the control `2.0 POW 3.0`). The IEEE-754 decodings are
arithmetic on those bit patterns, not printed by the compiler.
**Grounds:** the Parallax *Spin2 Language Documentation* v55 operator table has no `POW` row
(`spin2-v55-text.txt`: `POW` appears only in the version history, `:75`, and the new-keywords list, `:151`), so its precedence
is not given by the document. The folded values are consistent only with `POW` at the `+ -`
level, left-associative: `2.0 POW 3.0 +. 1.0` is (2^3)+1 = 9 (if `POW` were looser it would be
2^(3+1) = 16), `1.0 +. 3.0 POW 2.0` is (1+3)^2 = 16 (if tighter it would be 10), and
`2.0 POW 3.0 POW 2.0` is (2^3)^2 = 64 (right-associative would be 2^9 = 512). Settles the
«#416» statement of level 8, left-associative.
*Limits:* constant folding only; run-time evaluation of `POW` is not run. Four expressions;
`POW` against operators other than `+.` and `*.` is not run. The `*.` value is approximate
(`$42100001`, one unit in the last place above 36.0). One compiler version.
*→ EF:* none — legality stays CP.

### CP-007 · A typed pointer cannot be an array: `^BYTE pArray[10]` is rejected in a VAR block (`Pointers cannot be arrays (m480)`) and in a method's local list (`Pointers cannot be arrays (m481)`) — `LEGALITY`
*KB:* `language/spin2/operators/typed-pointers.yaml`
*Class:* legality. Both failing runs stop with exit status 1 at the declaration; a control with
`^BYTE pByte` (no array size) and a `LONG ptrTable[10]` array compiles.
*Source:* `proofs/cp-007-pointer-array-var.spin2`, `proofs/cp-007-pointer-array-local.spin2`,
`proofs/cp-007-pointer-control.spin2`; all under `{Spin2_v45}`.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (VAR):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-array-var.spin2`
*Output (2026-10-10; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-array-var.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-array-var.spin2:8:error:Pointers cannot be arrays (m480)
```
*Command (local):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-array-local.spin2`
*Output (2026-10-10; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-array-local.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-array-local.spin2:8:error:Pointers cannot be arrays (m481)
```
*Command (control):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-control.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-control.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-007-pointer-control.bin (6296 bytes)
pnut-ts: Done
```
Each error line is the declaration line (VAR line 8; local list line 8).
**Grounds:** the KB home already states "Pointers cannot be arrays" and `^BYTE pArray[10]` as an
error; no ingested Parallax document was found that says it, so the compile is its only
backing («#416» carried it from `pnut-ts`'s message). The compiler's two message numbers
differ by site (m480 VAR, m481 local).
*Limits:* `^BYTE` only; `^WORD`, `^LONG`, `^structName` arrays are not run, nor a method
parameter or result declared as a pointer array. One compiler version.
*→ EF:* none — legality stays CP.

---

## DEBUG (continued)

### CP-008 · `pnut-ts -d` raises no error for a DEBUG window named `Trace` (a SPECTRO and BITMAP directive) or `Field` (a Spin2 reserved word), and stores the name as text exactly as it stores `A` — `LEGALITY`
*KB:* `language/spin2/statements/debug.yaml`
*Class:* legality. Three programs that differ only in the window name (`A`, `Trace`, `Field`) each
compile with exit status 0, and the DEBUG text each binary holds carries the name unchanged in the
create message and in the channel message. Whether a host opens the window is not shown: the
compiler gives the three the same treatment.
*Source:* `proofs/cp-008-name-control.spin2` (`A`), `proofs/cp-008-name-directive.spin2` (`Trace`),
`proofs/cp-008-name-spin2-keyword.spin2` (`Field`): a SCOPE create, a channel message and one value
feed. Contrast `proofs/cp-008-field-as-variable.spin2`: `FIELD` as a Spin2 local-variable name.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d` (the contrast without it).

*Command (control):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-control.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-control.spin2
pnut-ts: Compiling with DEBUG
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-control.bin (9291 bytes)
pnut-ts: Done
```
*Command (`Trace`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-directive.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-directive.spin2
pnut-ts: Compiling with DEBUG
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-directive.bin (9303 bytes)
pnut-ts: Done
```
*Command (`Field`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-spin2-keyword.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-spin2-keyword.spin2
pnut-ts: Compiling with DEBUG
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-spin2-keyword.bin (9303 bytes)
pnut-ts: Done
```
*Command (the stored text):* ``grep -a -o "`SCOPE [A-Za-z]* SIZE 400 220\|`[A-Za-z]* 'S' -1000 1000" engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-control.bin engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-directive.bin engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-spin2-keyword.bin``
*Output (2026-10-10; the three `.bin` files just written):*
```text
engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-control.bin:`SCOPE A SIZE 400 220
engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-control.bin:`A 'S' -1000 1000
engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-directive.bin:`SCOPE Trace SIZE 400 220
engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-directive.bin:`Trace 'S' -1000 1000
engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-spin2-keyword.bin:`SCOPE Field SIZE 400 220
engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-name-spin2-keyword.bin:`Field 'S' -1000 1000
```
The two longer binaries are 12 bytes larger than the control: the name is 4 characters longer and
sits in three messages.
*Command (contrast, no `-d`):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-field-as-variable.spin2`
*Output (2026-10-10; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-field-as-variable.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-008-field-as-variable.spin2:5:error:Expected a unique variable name, STRUCT name, BYTE, WORD, LONG, "^", ALIGNW, or ALIGNL (m241)
```
The error line is the `| field` local list (line 5).
**Grounds:** no ingested Parallax document states what a DEBUG window name may be (the Spin2
Documentation v55 DEBUG tables give display types and directives, and no naming rule). The record
shows only that the compiler does not check a window name: a directive word and a Spin2 reserved
word are accepted and stored like any other. That a host then declines to open a window named
`Trace` is the bench's finding, EF-103.
*Limits:* three names, one display type (SCOPE). Digit-led names, names of 30 characters or more,
colour, colour-mode and packed-mode words, the other directives, and the reuse of a name after
`CLOSE` are not run here. One compiler version.
*→ EF:* none — legality stays CP; the run-time result is EF-103.

### CP-014 · A parent sets a child object's `DEBUG_MASK` where it declares the object (`OBJ c : "child" | DEBUG_MASK = %1`), and the child's channel-0 statement is then compiled — `LEGALITY`
*KB:* `language/spin2/constants/debug-mask.yaml`, `language/spin2/debug-commands/debug-strategy-guide.yaml`
*Class:* legality and listing — the override is accepted, and the child's `debug[0]()` record
appears in the program's `DEBUG records:` count. Whether it prints is behaviour and is not shown.
*Source:* `proofs/cp-014-mask-child.spin2` (`DEBUG_MASK = 0`, one `debug[0]()`),
`proofs/cp-014-mask-override.spin2` (declares it with `| DEBUG_MASK = %1`), and the control
`proofs/cp-014-mask-no-override.spin2` (the same parent without the override). Each parent has one
plain `debug()` of its own.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d -l`.

*Command (override):* `pnut-ts -d -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-014-mask-override.spin2` — exit status 0; listing:
```text
DEBUG records:           2 of 255 (0.8%)
DEBUG data:             13 of 15872 bytes (0.1%)
```
*Command (control):* `pnut-ts -d -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-014-mask-no-override.spin2` — exit status 0; listing:
```text
DEBUG records:           1 of 255 (0.4%)
DEBUG data:              5 of 15872 bytes (0.0%)
```
**Grounds:** Spin2 v55 says `DEBUG_MASK` is defined "for the file/object" (`spin2-v55-text.txt:38`,
`:1027`) and that object parameters "override CON symbols by the same name within the child
object" (`:29`); it does not name `DEBUG_MASK` as one. *Limits:* one child, one channel. The listing figures are this compiler's and
are never carried into the KB. One compiler version. *→ EF:* none — legality stays CP.

### CP-015 · With `DEBUG_MASK = 0`, a plain `debug()` is still compiled and a `debug[0]()` is not — `LEGALITY`
*KB:* `language/spin2/constants/debug-mask.yaml`, `language/spin2/debug-commands/debug-strategy-guide.yaml`
*Class:* listing — which statements become records. That a compiled statement prints when reached
is the documented meaning of `debug()` (v55, DEBUG); the record shows only that it is compiled.
*Source:* `proofs/cp-015-mask0-plain-debug.spin2` (one plain `debug("plain")`, one `debug[0]()`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d -l`.

*Command:* `pnut-ts -d -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-015-mask0-plain-debug.spin2` — exit status 0; listing:
```text
DEBUG records:           1 of 255 (0.4%)
DEBUG data:              9 of 15872 bytes (0.1%)
```
One record: the plain statement. **Grounds:** v55 gates only the bracketed form,
`DEBUG[bitnumber]{(parameters…)}` (`spin2-v55-text.txt:38`, `:1027`). *Limits:* one of each form.
One compiler version. *→ EF:* none — legality stays CP.

### CP-017 · DEBUG `BOOL` and `BOOL_` compile only under `{Spin2_v45}` or later: with no directive they are not recognised, and the `{Spin2_v44}` gate the v55 table names is refused — `LEGALITY`
*KB:* `language/spin2/debug-commands/debug-formatters-complete.yaml`
*Class:* legality, compiled with DEBUG (`-d`). The failing runs stop with exit status 1.
*Source:* `proofs/cp-017-bool-none.spin2` (no directive), `proofs/cp-017-bool-v44.spin2`,
`proofs/cp-017-bool-v45.spin2` (`debug(bool(x), bool_(x))`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d`.

*Command (no directive):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-017-bool-none.spin2`
*Output (2026-10-13; exit status 1):*
```text
engineering/ingestion/external-sources/compiler-verification/proofs/cp-017-bool-none.spin2:4:error:Expected an expression term (m172)
```
*Command (`{Spin2_v44}`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-017-bool-v44.spin2`
*Output (2026-10-13; exit status 1):*
```text
engineering/ingestion/external-sources/compiler-verification/proofs/cp-017-bool-v44.spin2:3:error:{Spin2_v44} is no longer supported due to changes in data structures beginning in v45]
```
*Command (`{Spin2_v45}`):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-017-bool-v45.spin2` — exit status 0 (`Wrote … cp-017-bool-v45.bin (9242 bytes)`).
(Banner lines omitted, as in CP-016.) **Grounds:** the Parallax *Spin2 Language Documentation* v55,
symbol table by version, row v44: "BOOL, BOOL_ … DEBUG" (`spin2-v55-text.txt:146`) — the same
refused-gate shape as CP-011. *Limits:* one site; one compiler version.
*→ EF:* none — legality stays CP.

---

## Comments

### CP-009 · A double-brace documentation comment between two terms of an expression is rejected (`Expected end of line (m281)`); the same comment after a complete statement, and a single-brace comment between the same terms, compile — `LEGALITY`
*KB:* `language/spin2/conventions/vscode-pnut-documentation-style.yaml`
*Class:* legality. The failing run stops with exit status 1 at the statement; the two controls compile.
Whether the compiled result differs is not shown (the controls differ in form).
*Source:* `proofs/cp-009-doc-brace-between-terms.spin2` (`result := speed {{comment between terms}} + 1`),
`proofs/cp-009-brace-between-terms.spin2` (the same with single braces),
`proofs/cp-009-doc-brace-after-statement.spin2` (`result := speed * 2 {{documentation comment after the statement}}`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (double brace between terms):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-doc-brace-between-terms.spin2`
*Output (2026-10-10; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-doc-brace-between-terms.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-doc-brace-between-terms.spin2:7:error:Expected end of line (m281)
```
*Command (single brace between terms):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-brace-between-terms.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-brace-between-terms.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-brace-between-terms.bin (6296 bytes)
pnut-ts: Done
```
*Command (double brace after a statement):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-doc-brace-after-statement.spin2`
*Output (2026-10-10; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-doc-brace-after-statement.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-009-doc-brace-after-statement.bin (6296 bytes)
pnut-ts: Done
```
The error line is the `result :=` line (7).
**Grounds:** the Parallax *Spin2 Language Documentation* v55 (2026-05-07), Comments table, row
"Intra-line or multi-line (documentation)", gives the example `x := 4, {{comment here}} y := 5` and
says "Everything within double braces is ignored" (`spin2-v55-text.txt:336`). That example places the
comment after a comma between two assignments, not between two terms of one expression, and is not itself a
compiling program; the record decides only the between-terms placement.
*Limits:* one expression shape (`:=` with `+`); a double-brace comment between statements on one
line is not run; the multi-line double-brace form is run only in the KB example, not here. One
compiler version.
*→ EF:* none — legality stays CP.

## Symbols (continued)

### CP-010 · A method local named `field` is rejected (`Expected a unique variable name, STRUCT name, BYTE, WORD, LONG, "^", ALIGNW, or ALIGNL (m241)`); the same local list with `field` renamed compiles — so OBEX 2842's `jm_fullduplexserial.spin2`, whose `format()` declares that local, does not compile — `LEGALITY`
*KB:* `language/spin2/operators/FIELD.yaml` (notes: FIELD cannot name a method local). Found compiling
OBEX 2842; the object's entry carries no compile verdict — an OBEX entry mirrors the catalog, it
does not rate the object (Stephen, 2026-10-11).
*Class:* legality. `FIELD` is a Spin2 language word, and the name is not free for a local. The failing
run stops with exit status 1 at the method line; the control compiles.
*Source:* `proofs/cp-010-local-named-field.spin2` (the local list of `jm_fullduplexserial.spin2`
`format()`, line 403 of the object as published in OBEX 2842: `pub format(p_str, p_args) | idx, c,
asc, field, digits`), `proofs/cp-010-local-named-fld.spin2` (the same with `fld`). The whole
object was also compiled from the copy held in the ingestion tree and fails with the same message
at its line 403.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (local named `field`):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-010-local-named-field.spin2`
*Output (2026-10-11; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-010-local-named-field.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-010-local-named-field.spin2:4:error:Expected a unique variable name, STRUCT name, BYTE, WORD, LONG, "^", ALIGNW, or ALIGNL (m241)
```
*Command (control, `fld`):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-010-local-named-fld.spin2`
*Output (2026-10-11; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-010-local-named-fld.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-010-local-named-fld.bin (6296 bytes)
pnut-ts: Done
```
**Grounds:** the Parallax *Spin2 Language Documentation* v55 defines `FIELD` as a language
construct, `FIELD[fieldpointer]` (FIELD POINTERS, `spin2-v55-text.txt:871-876`); it does not say
whether the word may also be a local name. The record decides only that it may not.
*Limits:* one local position; VAR and CON names called `field` are not run here. One compiler
version.
*→ EF:* none — legality stays CP.

### CP-016 · A cog register name in any case cannot be a method parameter (`m220`) or a local variable (`m241`) — `LEGALITY`
*KB:* `language/fundamentals/case-sensitivity.yaml`
*Class:* legality. Each failing run stops with exit status 1; the control compiles.
*Source:* `proofs/cp-016-register-param.spin2` (`PRI m(pA)`), `proofs/cp-016-register-local.spin2`
(`PUB main() | dira`), and the control `proofs/cp-016-control-param.spin2` (`PRI m(pinA)`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (parameter):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-016-register-param.spin2`
*Output (2026-10-13; exit status 1):*
```text
engineering/ingestion/external-sources/compiler-verification/proofs/cp-016-register-param.spin2:5:error:Expected a unique parameter name (m220)
```
*Command (local):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-016-register-local.spin2`
*Output (2026-10-13; exit status 1):*
```text
engineering/ingestion/external-sources/compiler-verification/proofs/cp-016-register-local.spin2:2:error:Expected a unique variable name, STRUCT name, BYTE, WORD, LONG, "^", ALIGNW, or ALIGNL (m241)
```
*Command (control):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-016-control-param.spin2` — exit status 0 (`Wrote … cp-016-control-param.bin (6300 bytes)`).
(The banner lines of each run are omitted; they are the same three lines as every record above.)
Also run in scratch, as parameters, with the same `m220`: `pb`, `ptra`, `dirA`, `outb`, `ina`,
`ijmp1`. **Grounds:** v55, "Source code is case-insensitive" (Spin2 Overview); it does not say
register names are taken as local names. *Limits:* the names listed; one compiler version.
*→ EF:* none — legality stays CP.

## Version gating

### CP-011 · BYTESWAP and LONGCOMP do not compile under `{Spin2_v44}` (`{Spin2_v44} is no longer supported due to changes in data structures beginning in v45]`); the same program compiles under `{Spin2_v45}` — the earliest gate that enables the COMP/SWAP methods is v45, not the v44 the v55 symbol table names — `LEGALITY`
*KB:* `language/spin2/methods/byteswap.yaml`, `language/spin2/methods/wordswap.yaml`,
`language/spin2/methods/longswap.yaml`, `language/spin2/methods/bytecomp.yaml`,
`language/spin2/methods/wordcomp.yaml`, `language/spin2/methods/longcomp.yaml`
*Class:* legality. The `{Spin2_v44}` run stops with exit status 1; the message refuses the gate
itself, not the methods, so no program can select v44. The `{Spin2_v45}` control compiles.
*Source:* `proofs/cp-011-comp-swap-gate-v44.spin2`, `proofs/cp-011-comp-swap-gate-v45.spin2`
(identical programs, `BYTESWAP(@a, @b, 4)` and `r := LONGCOMP(@a, @b, 2)`, differing only in the
gate line).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (`{Spin2_v44}`):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-011-comp-swap-gate-v44.spin2`
*Output (2026-10-11; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-011-comp-swap-gate-v44.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-011-comp-swap-gate-v44.spin2:4:error:{Spin2_v44} is no longer supported due to changes in data structures beginning in v45]
```
*Command (`{Spin2_v45}`):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-011-comp-swap-gate-v45.spin2`
*Output (2026-10-11; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-011-comp-swap-gate-v45.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-011-comp-swap-gate-v45.bin (6308 bytes)
pnut-ts: Done
```
The error is reported at line 4 (the VAR line), the first line after the gate that the compiler parses.
**Grounds:** the Parallax *Spin2 Language Documentation* v55, symbol table by version, row v44:
"BYTESWAP WORDSWAP LONGSWAP BYTECOMP WORDCOMP LONGCOMP … Minimum to Enable {Spin2_v44}"
(`spin2-v55-text.txt:146`). The document names a gate the compiler no longer accepts.
*Limits:* BYTESWAP and LONGCOMP are run; the other four methods of the row share it and are not run
one by one. One compiler version.
*→ EF:* none — legality stays CP.

## Assembly directives

### CP-012 · ORGH limits: a limit beyond $100000 is rejected (`Hub address exceeds $100000 ceiling (m361)`); a bare ORGH address beyond the default limit is rejected at the next instruction (`Hub address exceeds limit (m372)`); `ORGH $FC000,$FC800` compiles in a Spin2+PASM program and fails in a PASM-only program (`Program requirement exceeds 512KB hub RAM by …`) — `LEGALITY`
*KB:* `language/pasm2/orgh.yaml`
*Class:* legality. The three failing runs stop with exit status 1; the Spin2+PASM control compiles.
*Source:* `proofs/cp-012-orgh-limit-beyond-ceiling.spin2` (`ORGH $400, $100004` in a Spin2 program),
`proofs/cp-012-orgh-address-beyond-limit.spin2` (`ORGH $100004`), `proofs/cp-012-orgh-debug-mirror-pasm-only.spin2`
(a PASM-only program: `ORG`, `JMP #$`, then `ORGH $FC000, $FC800`), `proofs/cp-012-orgh-debug-mirror-spin2.spin2`
(the same ORGH in a Spin2 program).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (limit beyond the ceiling):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-limit-beyond-ceiling.spin2`
*Output (2026-10-11; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-limit-beyond-ceiling.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-limit-beyond-ceiling.spin2:4:error:Hub address exceeds $100000 ceiling (m361)
```
*Command (bare address beyond the limit):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-address-beyond-limit.spin2`
*Output (2026-10-11; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-address-beyond-limit.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-address-beyond-limit.spin2:5:error:Hub address exceeds limit (m372)
```
*Command (debug mirror, PASM-only):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-debug-mirror-pasm-only.spin2`
*Output (2026-10-11; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-debug-mirror-pasm-only.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-debug-mirror-pasm-only.spin2:6:error:Program requirement exceeds 512KB hub RAM by 507908 bytes
```
*Command (debug mirror, Spin2+PASM):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-debug-mirror-spin2.spin2`
*Output (2026-10-11; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-debug-mirror-spin2.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-012-orgh-debug-mirror-spin2.bin (6296 bytes)
pnut-ts: Done
```
**Grounds:** the Parallax *Spin2 Language Documentation* v55, DAT Blocks, Hub-exec, gives the $100000
default limit and `ORGH $FC000,$FC800` as a syntax illustration, and says ORGH in a PASM-only program
fills hub memory with zeros up to the address (`spin2-v55-text.txt:322-327`). It names no error
messages; the record supplies them.
*Limits:* one address of each kind; the debug-mirror case is run at its first address only. One
compiler version.

## Debug-techniques proofs («#430» batch 2)

Entries CP-018 to CP-025. A listing figure, byte count or image count below is evidence for the
record only and is never carried into the KB (tool limits are not KB facts). The `.bin`, `.lst` and
`.map` files each run writes are not kept; only the `.spin2` sources are.

### CP-018 · `DEBUG_COGS` is compiled into the program image: two otherwise identical programs, one setting `DEBUG_COGS = %0000_0001` and one leaving it default, produce binaries that differ — `LAYOUT`
*KB:* `language/spin2/constants/special-configuration-symbols.yaml` (`DEBUG_COGS`)
*Class:* layout — the setting reaches the binary. What the mask does at run time (a cog with its bit
clear takes no debug interrupt) is the documented meaning (Spin2 v55, `DEBUG_COGS`), not shown here.
*Source:* `proofs/cp-018-cogs-set.spin2` (`DEBUG_COGS = %0000_0001`), `proofs/cp-018-cogs-default.spin2`
(the same program without the symbol — the control). Both: `debug("hello", udec(1))`.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d`.

*Command (set):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-018-cogs-set.spin2`
*Output (2026-10-13; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-018-cogs-set.spin2
pnut-ts: Compiling with DEBUG
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-018-cogs-set.bin (9244 bytes)
pnut-ts: Done
```
*Command (control, default):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-018-cogs-default.spin2`
*Output (2026-10-13; exit status 0):* the same three banner lines, then `Compiling with DEBUG`,
`Wrote … cp-018-cogs-default.bin (9244 bytes)`, `Done`.
*Command (compare):* `cmp -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-018-cogs-set.bin engineering/ingestion/external-sources/compiler-verification/proofs/cp-018-cogs-default.bin`
*Output (2026-10-13; exit status 1, the files differ):*
```text
 233   1 377
```
One byte differs (byte 233, octal values: `1` with the symbol set, `377` = $FF by default). The two
binaries have the same size. **Grounds:** Spin2 v55 gives `DEBUG_COGS` a default of all cogs
(`spin2-v55-text.txt:1011`). The byte offset is this compiler's and is not carried into the KB; the
KB states only that the value is compiled into the image, so two builds with different values give
different binaries. *Limits:* one value; one program; one compiler version. *→ EF:* none.

### CP-019 · A child's VAR is per instance and its DAT is shared, yet the memory map's image count is the same either way — `LAYOUT`
*KB:* `language/spin2/concepts/object-image-dedup.yaml`
*Class:* layout — the `-m` memory map of two builds that differ only in where the child keeps its ledger.
*Source:* `proofs/cp-019-parent-var.spin2` and `proofs/cp-019-parent-dat.spin2` (each: `OBJ a, b` both
the same child; `x := a.bump()`, `x += b.bump()`), `proofs/cp-019-child-var.spin2` (`VAR long ledger`)
and `proofs/cp-019-child-dat.spin2` (`DAT ledger long 0`). The two children are otherwise identical.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-m`.

*Command (VAR ledger):* `pnut-ts -m engineering/ingestion/external-sources/compiler-verification/proofs/cp-019-parent-var.spin2`
*Output (2026-10-13; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -m engineering/ingestion/external-sources/compiler-verification/proofs/cp-019-parent-var.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-019-parent-var.map
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-019-parent-var.bin (6336 bytes)
pnut-ts: Done
```
*Command (DAT ledger):* `pnut-ts -m engineering/ingestion/external-sources/compiler-verification/proofs/cp-019-parent-dat.spin2`
*Output (2026-10-13; exit status 0):* the same shape, writing `cp-019-parent-dat.map` and
`cp-019-parent-dat.bin (6344 bytes)`.
The map's SUMMARY line, identical in both:
```text
  The top object and 2 OBJ declarations became 3 instances, built from 2 images; 1 image is shared by more than one instance.
```
What differs is the ledger. VAR build — one `LEDGER` entry per instance, in the map's VAR section:
```text
  A         LONG  LEDGER     4  +$00004  $00040
  B         LONG  LEDGER     4  +$00004  $00048
```
DAT build — one `LEDGER` entry, in the map's DAT section, for the one shared image:
```text
  LONG  LEDGER  +$00008  $00030
```
**Grounds:** Spin2 v55 says each object instance has its own VAR and that DAT is shared
(`spin2-v55-text.txt:174`, `:181`, `:238`). The record adds what the map shows: the image count does
not separate the two cases, so a split VAR ledger cannot be seen from the count; the map's VAR
entries show it. *Limits:* one child shape; one compiler version. *→ EF:* none.

### CP-020 · Inline PASM reaches only the first 16 longs of a method's locals: a 17th local used by the PASM is rejected (`Local variable must be LONG and within first 16 longs (m451)`) at the PASM line; declared first, it compiles — `LEGALITY`
*KB:* `language/spin2/constructs/inline_pasm.yaml`
*Class:* legality. The failing run stops with exit status 1; both controls compile.
*Source:* `proofs/cp-020-loc16-ok.spin2` (16 locals, the PASM uses the 16th), `proofs/cp-020-loc17-bad.spin2`
(17 locals, the PASM uses the 17th), `proofs/cp-020-loc17-first.spin2` (the same 17 locals with the one the
PASM uses declared first).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (17th local, used by the PASM):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-020-loc17-bad.spin2`
*Output (2026-10-13; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-020-loc17-bad.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-020-loc17-bad.spin2:3:error:Local variable must be LONG and within first 16 longs (m451)
```
The error line is the PASM instruction that names the variable (`mov a17, #1`, line 3), not the method line.
*Command (control, 16 locals):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-020-loc16-ok.spin2` — exit status 0 (`Wrote … cp-020-loc16-ok.bin (6304 bytes)`).
*Command (control, declared first):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-020-loc17-first.spin2` — exit status 0 (`Wrote … cp-020-loc17-first.bin (6304 bytes)`).
(Banner lines of the two controls omitted, as in CP-016.) **Grounds:** Spin2 v55 limits inline PASM to
the first 16 long variables of the method (`spin2-v55-text.txt:285`). The record adds the error
text and where it is reported. *Limits:* long locals only; one compiler version. *→ EF:* none — legality stays CP.

### CP-021 · `=>` and `=<` are not Spin2 operators and are rejected (`Expected end of line (m281)`); `>=` and `<=` compile — `LEGALITY`
*KB:* `language/spin2/operators/precedence.yaml`, `language/spin2/concepts/operators.yaml`
*Class:* legality. The two failing runs stop with exit status 1; the control compiles.
*Source:* `proofs/cp-021-op-ge-bad.spin2` (`r := x => y`), `proofs/cp-021-op-le-bad.spin2` (`r := x =< y`),
and the control `proofs/cp-021-op-ok.spin2` (`r := x >= y`, `r += x <= y`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026.

*Command (`=>`):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-021-op-ge-bad.spin2`
*Output (2026-10-13; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-021-op-ge-bad.spin2
engineering/ingestion/external-sources/compiler-verification/proofs/cp-021-op-ge-bad.spin2:2:error:Expected end of line (m281)
```
*Command (`=<`):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-021-op-le-bad.spin2`
*Output (2026-10-13; exit status 1):* the same banner, then
`engineering/ingestion/external-sources/compiler-verification/proofs/cp-021-op-le-bad.spin2:2:error:Expected end of line (m281)`.
*Command (control):* `pnut-ts engineering/ingestion/external-sources/compiler-verification/proofs/cp-021-op-ok.spin2` — exit status 0 (`Wrote … cp-021-op-ok.bin (6300 bytes)`).
**Grounds:** the Spin2 v55 operator table lists `>=` and `<=` (`spin2-v55-text.txt:482`) and no reversed forms. *Limits:* signed
forms only (not `+>=` `+<=`); one compiler version. *→ EF:* none — legality stays CP.

### CP-022 · Text moved out of a `debug()` string into DAT and emitted with `zstr_` leaves the DEBUG data budget: the same message costs 226 bytes of DEBUG data inline and 3 bytes from DAT, one record each — `LAYOUT`
*KB:* `language/spin2/debug-commands/debug-strategy-guide.yaml` (`over_on_bytes`)
*Class:* listing — which figures the compiler reports for DEBUG. The figures are this compiler's and
never go into the KB; the KB states only that moved text leaves the budget.
*Source:* `proofs/cp-022-text-in-debug.spin2` (the message as a string in `debug("…")`),
`proofs/cp-022-text-in-dat.spin2` (the message in DAT, `debug(zstr_(@msg))`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d -l`.

*Command (inline):* `pnut-ts -d -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-022-text-in-debug.spin2` — exit status 0; listing:
```text
DEBUG records:           1 of 255 (0.4%)
DEBUG data:            226 of 15872 bytes (1.4%)
```
*Command (in DAT):* `pnut-ts -d -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-022-text-in-dat.spin2` — exit status 0; listing:
```text
DEBUG records:           1 of 255 (0.4%)
DEBUG data:              3 of 15872 bytes (0.0%)
```
*Coalescing and IF (2026-11-05, `pnut-ts` v1.55.10, `-d -l`):* `proofs/cp-022-coalesce-two.spin2` 1 record, 4 bytes; `proofs/cp-022-coalesce-one.spin2` 1 record, 3 bytes; `proofs/cp-022-if-absent.spin2` 1 record, 5 bytes; `proofs/cp-022-if-present.spin2` 1 record, 6 bytes.
**Grounds:** none beyond the compile; the DEBUG budget is the compiler's. *Limits:* one message of
about 200 characters on v1.55.8; one small case each for coalescing and IF on v1.55.10. *→ EF:* none.

### CP-023 · A streamer count above $FFFF is accepted silently: `XINIT`'s count spills into the command field, and a count of 131,072 assembles to the word for the next pin with count 0 — `LAYOUT`
*KB:* `language/pasm2/xinit.yaml` (notes)
*Class:* layout — an assembled word. What the streamer then does with that word is not shown.
*Source:* `proofs/cp-023-streamer-count-spill.spin2`: three DAT longs built from `X_IMM_32X1_1DAC1 +
X_PINS_ON` plus a pin field at bit 17 plus a count — $FFFE (control, fits), 131,072, and the control
for the spill, "pin + 1, count 0".
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-l`.

*Command:* `pnut-ts -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-023-streamer-count-spill.spin2`
*Output (2026-10-13; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-023-streamer-count-spill.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-023-streamer-count-spill.lst
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-023-streamer-count-spill.bin (6304 bytes)
pnut-ts: Done
```
The listing's three DAT longs, as bytes: `FE FF 90 40` ($4090_FFFE, count $FFFE), `00 00 92 40` ($4092_0000, count
131,072) and `00 00 92 40` ($4092_0000, pin + 1 with count 0). The spilled word equals the
pin-plus-one, count-0 word. No error or warning is printed. **Grounds:** Propeller 2 Documentation
v35 gives the command field above the 16-bit count (`silicon-doc-text.txt:1313`, `:1327`, `:1401`,
`:1403`). *Limits:* one mode; one count; one compiler version. *→ EF:* none; what the streamer does
with the word is the bench's (the instruction's own EF records).

### CP-024 · `pnut-ts` shares one object image among declarations that compile to the same bytes; a constant override that changes the child's bytes forks a second image with its own DAT, and an override on one of two siblings splits a DAT singleton — `LAYOUT`
*KB:* `language/spin2/concepts/object-image-dedup.yaml`
*Class:* layout — the `-m` memory map's image counts and DAT entries.
*Source:* `proofs/cp-024-child.spin2` (`CON INC = 1`; `DAT ledger long 0`; `bump()` adds `INC`);
three parents each declaring the child twice: `proofs/cp-024-parent-control.spin2` (no override, the
control), `proofs/cp-024-parent-one-override.spin2` (`a` with `| INC = 2`, `b` plain),
`proofs/cp-024-parent-same-override.spin2` (both with `| INC = 2`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-m`.

*Command (control):* `pnut-ts -m engineering/ingestion/external-sources/compiler-verification/proofs/cp-024-parent-control.spin2`
*Output (2026-10-13; exit status 0):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -m engineering/ingestion/external-sources/compiler-verification/proofs/cp-024-parent-control.spin2
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-024-parent-control.map
pnut-ts: Wrote engineering/ingestion/external-sources/compiler-verification/proofs/cp-024-parent-control.bin (6344 bytes)
pnut-ts: Done
```
*Command (one override):* `pnut-ts -m engineering/ingestion/external-sources/compiler-verification/proofs/cp-024-parent-one-override.spin2`
*Output (2026-10-13; exit status 0):* the same shape, `cp-024-parent-one-override.bin (6368 bytes)`.
*Command (both override):* `pnut-ts -m engineering/ingestion/external-sources/compiler-verification/proofs/cp-024-parent-same-override.spin2`
*Output (2026-10-13; exit status 0):* the same shape, `cp-024-parent-same-override.bin (6344 bytes)`.

The map's SUMMARY line and object tree, per build:
```text
control:   3 instances, built from 2 images; 1 image is shared by more than one instance.
             A #2 -, B #2 -            one DAT entry (LEDGER), in image #2
one:       3 instances, built from 3 images; no image is shared.
             A #2 INC=2, B #3 -        two DAT entries (LEDGER), one in each of images #2 and #3
both:      3 instances, built from 2 images; 1 image is shared by more than one instance.
             A #2 INC=2, B #2 INC=2    one DAT entry (LEDGER), in image #2
```
**Grounds:** Spin2 v55 says object parameters override CON symbols within the child
(`spin2-v55-text.txt:29`); it does not describe how identical children are shared. The record shows
the sharing follows the compiled content: two declarations of one child share an image and its DAT;
an override that changes the bytes forks an image (and a DAT); an override applied identically to
both siblings does not. *Limits:* one constant, one child, two siblings; one compiler version.
*→ EF:* none.

### CP-025 · `debug[N]()` with no `DEBUG_MASK` defined is rejected (`DEBUG_MASK symbol must be defined for DEBUG[0..31] usage`); with `DEBUG_MASK` defined it compiles — `LEGALITY`
*KB:* `language/spin2/constants/debug-mask.yaml`
*Class:* legality, compiled with DEBUG (`-d`). The failing run stops with exit status 1; the control compiles.
*Source:* `proofs/cp-025-index-no-mask.spin2` (`debug[3]("indexed")`, no `DEBUG_MASK`),
`proofs/cp-025-index-with-mask.spin2` (the same with `CON DEBUG_MASK = %1000`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d`.

*Command (no mask):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-025-index-no-mask.spin2`
*Output (2026-10-13; exit status 1):*
```text
pnut-ts: * Propeller Spin2/PASM2 Compiler 'pnut_ts' (c) 2024-2026 Iron Sheep Productions, LLC., Parallax Inc.
pnut-ts: * Version 1.55.8, Build date: 9/19/2026
pnut-ts: * pnut_ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-025-index-no-mask.spin2
pnut-ts: Compiling with DEBUG
engineering/ingestion/external-sources/compiler-verification/proofs/cp-025-index-no-mask.spin2:2:error:DEBUG_MASK symbol must be defined for DEBUG[0..31] usage
```
*Command (control, mask defined):* `pnut-ts -d engineering/ingestion/external-sources/compiler-verification/proofs/cp-025-index-with-mask.spin2` — exit status 0 (`Wrote … cp-025-index-with-mask.bin (9243 bytes)`).
(Banner lines of the control omitted, as in CP-016.) The error line is the `debug[3]` statement (line 2).
*No version directive (2026-10-13):* `proofs/cp-025-index-with-mask.spin2` (and CP-014's and CP-015's `.spin2`
files) carry no `{Spin2_v##}` line (`grep -n -i "{Spin2_v"` over them finds nothing), and `debug[N]()` with
`DEBUG_MASK` defined compiles — so neither `DEBUG_MASK` nor `debug[N]()` needs a version directive.
**Grounds:** Spin2 v55 gates `DEBUG[bitnumber]` on `DEBUG_MASK` (`spin2-v55-text.txt:38`, `:1027`);
it names no error text; the record supplies it. *Limits:* one index; one compiler version.
*→ EF:* none — legality stays CP.

### CP-026 · `DEBUG_DISABLE = 0` compiles a file's `debug()` statements exactly as when the symbol is undefined; `DEBUG_DISABLE = 1` compiles none; a float value is rejected (`DEBUG_DISABLE can only be defined as an integer constant`) — `LAYOUT` + `LEGALITY`
*KB:* `language/spin2/constants/special-configuration-symbols.yaml` (`DEBUG_DISABLE.behavior`)
*Class:* layout, compiled with DEBUG (`-d`) and a listing (`-l`); the figures are the listing's
`DEBUG records` / `DEBUG data` lines. All three runs exit 0.
*Source:* `proofs/cp-026-disable-undefined.spin2` (one `debug("disable undefined")`, no symbol),
`proofs/cp-026-disable-zero.spin2` (`CON DEBUG_DISABLE = 0`, one `debug("disable zero")`),
`proofs/cp-026-disable-one.spin2` (`CON DEBUG_DISABLE = 1`, one `debug("disable one")`).
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-d -l`.

*Commands (2026-10-15):* `pnut-ts -d -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-026-disable-<undefined|zero|one>.spin2`
*Output (the listing's DEBUG lines):*
```text
undefined:  DEBUG records:           1 of 255 (0.4%)    DEBUG data:             21 of 15872 bytes (0.1%)
zero:       DEBUG records:           1 of 255 (0.4%)    DEBUG data:             16 of 15872 bytes (0.1%)
one:        DEBUG records:           0 of 255 (0.0%)    DEBUG data:              0 of 15872 bytes (0.0%)
```
(The undefined and zero data figures differ by the five-character difference in their strings.)
*Float value (2026-10-15):* `pnut-ts -d -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-026-disable-float.spin2`
(`CON DEBUG_DISABLE = 1.0`) — exit status 1:
```text
engineering/ingestion/external-sources/compiler-verification/proofs/cp-026-disable-float.spin2:4:error:DEBUG_DISABLE can only be defined as an integer constant
```
(The compiler reports line 4 of a three-line file.)
**Grounds:** Spin2 v55 states only the non-0 case ("Assigning a non-0 value to this symbol will
disable all DEBUG statements in the file/object", `spin2-v55-text.txt:1028`); the record supplies the
0 case. *Limits:* one statement per file; one compiler version.
*→ EF:* none — layout stays CP.

### CP-027 · `FVAR` and `FVARS` are per-item overrides that follow `BYTE`/`WORD`/`LONG`, emit 1 to 4 bytes whatever the line's size, pad nothing, take no `[count]` and reject values outside their ranges (`FVAR/FVARS data is too big`) — `LAYOUT` + `LEGALITY`
*KB:* `language/pasm2/fvar.yaml`
*Class:* layout (the image bytes) and legality (the rejections).
*Source:* `proofs/cp-027-accepted.spin2`, and one file for each rejection:
`proofs/cp-027-fvar-too-big.spin2`, `cp-027-fvar-negative.spin2`, `cp-027-fvar-float.spin2`,
`cp-027-fvars-too-big.spin2`, `cp-027-fvar-repeat.spin2`, `cp-027-fvar-no-size.spin2`.
*Compiler:* `pnut-ts` v1.55.8, build date 9/19/2026, with `-l`.

*Command (2026-11-05):* `pnut-ts -l engineering/ingestion/external-sources/compiler-verification/proofs/cp-027-accepted.spin2`, exit status 0. The 41 image bytes, by labelled line:
```text
unsigned   7F | 80 01 | AC 02 | F0 A2 04 | FF FF FF FF
signed     7F | D4 7D | 80 80 80 80
one_item   AC 02 | 90
in_long    AC 02 | 01 00 00 00
in_word    01 00 | AC 02 | 02 00
mixed      01 | AC 02 | 02 | D4 7D | 03
```
The listing types the labels `DAT_BYTE`, `DAT_LONG` and `DAT_WORD` after the line's declared size,
and places `in_long` at a non-long offset.

*Rejections (2026-11-05):* `pnut-ts -l <the file>`, exit status 1 each:
```text
cp-027-fvar-too-big.spin2:3:error:FVAR/FVARS data is too big (m351)
cp-027-fvar-negative.spin2:3:error:FVAR/FVARS data is too big (m351)
cp-027-fvar-float.spin2:3:error:FVAR/FVARS data is too big (m351)
cp-027-fvars-too-big.spin2:3:error:FVAR/FVARS data is too big (m350)
cp-027-fvar-repeat.spin2:3:error:Expected "," or end of line
cp-027-fvar-no-size.spin2:3:error:Expected a unique name, BYTE, WORD, LONG, or assembly instruction
```
*ORG section (2026-11-05):* `pnut-ts -l .../proofs/cp-027-org-padding.spin2`, exit status 0. An
instruction after the data starts on the next long; long data does not:
```text
a          AC 02 | 7F | 00        (one zero byte, then b on the next long)
b          00 00 00 00
c          AC 02
(long 1)   01 00 00 00            (no fill before it)
```
This is the behaviour Spin2 v55's version history v44 describes. It is not specific to `FVAR`: `byte 1`
followed by `nop` under `org` fills the same way; outside `org`, `byte FVAR 300` followed by `nop` emits
`AC 02 00 00 00 00` with no fill.
**Grounds:** Spin2 v55 states only that these overrides exist and can be read by `RFVAR`/`RFVARS`
(DAT Symbols and Data).
*Values the compiler can size (2026-11-05):* `pnut-ts` v1.55.10. `pnut-ts -l .../proofs/cp-027-fvars-later-label.spin2`, exit status 1: `cp-027-fvars-later-label.spin2:3:error:Undefined symbol`, for a label on the next line. `pnut-ts -l .../proofs/cp-027-fvars-known-value.spin2`, exit status 0, with a CON constant of -200 and two earlier labels 3 bytes apart: `08 | B8 7E | 7D | B5 7E`. `pnut-ts -l .../proofs/cp-027-fvars-later-constant.spin2`, exit status 0: a constant in a CON block after the DAT is accepted, so the limit is on labels, not on every symbol defined later.
*Non-negative `FVARS` (2026-11-05):* `pnut-ts` v1.55.10, `pnut-ts -l .../proofs/cp-027-fvars-nonnegative.spin2`, exit status 0:
```text
FVARS 0          00
FVARS 63         3F
FVARS 64         C0 00
FVARS 100        E4 00
FVARS 1000       E8 07
FVARS $0FFF_FFFF FF FF FF 7F
```
v1.55.8 rejected this file with `FVAR/FVARS data is too big (m350)`; v1.55.10 carries the PNut-TS
project's fix. `cp-027-accepted` and `cp-027-org-padding` give the same bytes under both, and the
six rejections print the same errors under both.
*Limits:* two compiler versions.
*→ EF:* none — layout and legality stay CP.

### CP-028 · Assigning a method's `^StructName` result to a bare pointer variable is rejected for a structure of 5 bytes or more, in a child object and in the same object; the bracket form is accepted at every size — `LEGALITY`
*KB:* `language/spin2/keywords/STRUCT.yaml`, `language/spin2/operators/typed-pointers.yaml`, `application-notes/p2an007-data-structures-new-facilities.yaml`
*Class:* legality.
*Source:* `proofs/cp-028-child-{1,8,16}.spin2` (the called objects), `proofs/cp-028-bare-child-{1,8,16}.spin2`, `proofs/cp-028-bare-same-{1,8,16}.spin2`, `proofs/cp-028-bracket-child-{1,8,16}.spin2`, where the number is the structure's size in longs; `proofs/cp-028-bare-same-4bytes.spin2`, `cp-028-bare-same-5bytes.spin2`.
*Compiler:* `pnut-ts` v1.55.10, build date 11/5/2026.

*Command (2026-11-06):* `pnut-ts <the file>`, from `proofs/`:
```text
cp-028-bare-child-1      exit 0
cp-028-bare-same-1       exit 0
cp-028-bare-same-4bytes  exit 0
cp-028-bare-same-5bytes  exit 1  :7:error:Expected ","
cp-028-bare-child-8      exit 1  :5:error:Expected ","
cp-028-bare-same-8       exit 1  :7:error:Expected ","
cp-028-bare-child-16     exit 1  :5:error:Expected a variable (m251)
cp-028-bare-same-16      exit 1  :7:error:Expected a variable (m251)
cp-028-bracket-child-1   exit 0
cp-028-bracket-child-8   exit 0
cp-028-bracket-child-16  exit 0
```
The first version of this record named the boundary as two longs, and an audit's compiles of 5, 6 and 7 bytes showed it is in bytes. The same runs tried 2, 3, 4, 15 and 20 longs, byte and word structures, and pointers held in a VAR, a local and a parameter, with the same results by size. The failure belongs to the multi-long target: a plain-long method result fails the same way, and two results assigned to an 8-byte target compile. Spin2 v55 gives the reading: a bare pointer variable is the pointed-to variable, a structure up to 1 long passes as a single long, and one up to 15 longs takes multi-long assignment.
*Limits:* legality only; nothing was run. One compiler version.
*→ EF:* none — legality stays CP.

### CP-029 · Every `CON` clock-setup form in `pasm2-getting-started.yaml` is accepted in a PASM-only file, the three PLL forms also without `_errfreq`; `_xtlfreq` with `_xinfreq` is rejected — `LEGALITY`
*KB:* `guides/pasm2-getting-started.yaml`
*Class:* legality.
*Source:* `proofs/cp-029-form-{1..7}.spin2` (the seven `CON` rows of the page's table, in order), `proofs/cp-029-no-errfreq-{1,2,3}.spin2`, `proofs/cp-029-both.spin2`.
*Compiler:* `pnut-ts` v1.55.10, build date 11/5/2026.

*Command (2026-11-06):* `pnut-ts <the file>`. All ten of the form and no-`_errfreq` files exit 0.
```text
cp-029-both.spin2:7:error:Conflicting or deficient _CLKFREQ/_XTLFREQ/_XINFREQ/_RCFAST/_RCSLOW symbol
```
*Limits:* legality only. It says nothing about the effect and `%CC_SS` columns, which are the Spin2 documentation's statements. One compiler version.
*→ EF:* none — legality stays CP.
