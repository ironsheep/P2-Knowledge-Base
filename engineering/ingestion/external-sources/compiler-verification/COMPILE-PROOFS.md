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

**Class legend:** `LEGALITY` (whether the compiler accepts a form; stays CP) · `BEHAVIOUR` (what
compiled code does; the compile does not prove it) · `BEHAVIOUR → EF-NNN` (a P2 run has since
proved it; the KB cites the EF).

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
