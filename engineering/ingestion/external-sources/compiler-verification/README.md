# P2 Compiler-Verification Evidence

**What this is.** The register of **facts our own compile proved** about what the Spin2/PASM2
compiler accepts and rejects. Each record is a small `.spin2` program we wrote, the exact
`pnut-ts` command we ran on it, and the compiler's **verbatim** output. The register is
[`COMPILE-PROOFS.md`](COMPILE-PROOFS.md); its records are `CP-NNN`.

It is the sibling of the bench ledger
([`../hardware-verification/P2-EMPIRICAL-FINDINGS.md`](../hardware-verification/P2-EMPIRICAL-FINDINGS.md),
`EF-NNN`). The two are kept apart on purpose: an `EF` record says what the **chip** did when a
program ran; a `CP` record says what the **compiler** said about a program. Neither stands in for
the other.

## Why this exists — Stephen's decision (Q12)

Recorded in the close-out study (`engineering/analysis/2026-10-08-p2kb-close-out-study.md`,
*Stephen's decisions*, row Q12, 2026-10-09), verbatim:

> | Q12 | S-147, S-251, S-280, S-345, S-157 (proof home) | **A separate compile-proof register** (`CP-NNN`), not the bench ledger: "to keep our registers pure this should likely be a separate register". Legality facts stay CP; a behaviour fact moves to EF when a P2 run proves it. The sourcing gate accepts CP and EF as the two self-created citations; citations are internal provenance. |

Row Q9 (same table) says when a proof is needed and what it is measured with, verbatim:

> | Q9 | S-147, S-251, S-280, S-345, S-157 (PASM half), S-354 | **A, "if we have proven the errata".** Where the Spin2 v55 document and `pnut-ts` disagree on legality, the KB teaches what compiles and the document's error is filed in `SOURCE-ERRATA.md` with the source line, the command and the compiler output — only once our compile proves it. No PNut checks: `pnut-ts` emits PNut's binary (Stephen's 700+ regression tests); a PNut check is a last resort for a real suspicion. The punch-list "check first: PNut" lines (items 7–11) are struck. S-354 is checked here with `pnut-ts`. |

## The two classes

- **Legality** — whether the compiler accepts a form, and what it says when it does not (a
  symbol's length, a statement form, an escape sequence, a keyword's version gate). The compiler
  is the authority for legality, so a legality record is complete as it stands. **It stays `CP`.**
- **Behaviour** — what compiled code *does* when it runs. A compile cannot show that: it can only
  show that the program builds. A behaviour record holds only what the compiler printed; the
  run-time claim is **not proven by it** and is not taught from it. When a P2 run proves the
  behaviour, the bench ledger gets the `EF-NNN` entry and the `CP` record gains `→ EF-NNN`. From
  then on the KB cites the `EF` for the behaviour; the `CP` stays as the record of the compile.

## Lifecycle of a record

```
write the proof (.spin2 in proofs/) ─▶ run pnut-ts ─▶ record verbatim ─▶ name the KB home
                                                                            │
                                     legality: done, stays CP ◀─────────────┤
                                     behaviour: waits for a P2 run ─▶ EF-NNN; CP gains → EF-NNN
```

1. **Write the proof** in [`proofs/`](proofs/), named `cp-NNN-<topic>.spin2`. One file per
   outcome: a failing file stops at its first error, so a record that needs a pass and a fail
   (or two fails) has one file for each, differing only in the form under test. Each file opens
   with a comment naming its record, its outcome, its command and the expected result.
2. **Run it** with `pnut-ts` from the repository root, passing the repository-relative path, so
   the recorded output reproduces exactly (the compiler prints the path it was given). Use `-d`
   only when the proof needs DEBUG. The `.bin` a passing run writes is git-ignored here
   (`.gitignore`) and never committed.
3. **Record it** in `COMPILE-PROOFS.md`: the command and the compiler's full output, verbatim —
   every line, the exit status included. Never a paraphrase.
4. **Name the KB home** — the YAML the fact belongs in, or `not a KB fact — <reason>`.
5. **Behaviour only:** when a P2 run proves it, add `→ EF-NNN` to the record. Legality never
   moves.
6. **Re-run on demand.** Each record names the `pnut-ts` version it was measured under. A re-run
   under a later version that gives different output is appended under the original, dated, with
   its version; the original output is never edited. *(This is a house rule, matching the bench
   ledger's frozen-record convention; it is not in Q12's words.)*

## A record's fields

Each record in `COMPILE-PROOFS.md` carries, in this order:

| Field | Holds |
|-------|-------|
| heading | `### CP-NNN · <the fact> — \`LEGALITY\`` or `— \`BEHAVIOUR\`` (`BEHAVIOUR → EF-NNN` once proved on a P2) |
| `*KB:*` | the first line under the heading: the KB home, a backticked path relative to `deliverables/ai/P2/`, or `not a KB fact — <reason>` (the same form as the bench ledger's line) |
| `*Class:*` | legality or behaviour, and what the compiler's answer does and does not show |
| `*Source:*` | the proof file(s) in `proofs/` |
| `*Compiler:*` | the `pnut-ts` version and build date, from its banner |
| `*Command:*` + `*Output:*` | for each proof file: the exact command, then the verbatim output and exit status, measured on the date given |
| `**Grounds:**` | what the record decides: the source line it confirms or contradicts (quoted), the study rows or findings it settles |
| `*Limits:*` | what the proof does not cover |
| `*→ EF:*` | the bench entry that proved a behaviour fact; for legality, `none — legality stays CP` |

## How to cite a record

A KB entry whose fact rests on a record cites `CP-NNN` in its stripped provenance field
(`source:` / `sources:`), never in content that ships — the id is internal provenance, which this
repository's gates and auditors resolve and a consumer cannot. Errata filed in `SOURCE-ERRATA.md`
from a record name its `CP-NNN`.

## Structure

```
engineering/ingestion/external-sources/compiler-verification/
  README.md            # this file
  COMPILE-PROOFS.md    # the register: CP-NNN records
  .gitignore           # *.bin, *.lst — compiler output is never committed
  proofs/              # the .spin2 proof programs (versioned)
```

## Conventions

- **Versioned:** the `.spin2` proofs and the `*.md` files.
- **Never committed:** `.bin`, `.lst` and any other compiler output; they are regenerable from the
  proof by re-running its command.
- **Verbatim or nothing.** The output block is what the compiler printed. A record whose proof no
  longer reproduces its output is re-measured, not edited to match.
- **Disproven counts.** "The document says X compiles and it does not" is a record like any
  other; it is what stops the wrong claim coming back.

## Relationship to other locations

| Location | Holds |
|----------|-------|
| **here** (`compiler-verification/`) | the compile proof: proof programs, commands, verbatim output |
| `../hardware-verification/P2-EMPIRICAL-FINDINGS.md` | the bench proof (`EF-NNN`): what the chip did |
| `engineering/ingestion/SOURCE-ERRATA.md` | errors in ingested documents; an erratum a compile proved names its `CP-NNN` |
| `engineering/operations/P2KB-CORRECTION-FINDINGS.md` | the to-fix register for the KB |
| `engineering/ingestion/sources/` | the documentary sources, frozen; a record quotes them, never edits them |
