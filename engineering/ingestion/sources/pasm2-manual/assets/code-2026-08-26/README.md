# pasm2-manual — code extraction, 2026-08-26

**Source:** `Propeller 2 Assembly Language (PASM2) Manual - 20221101.docx` (DOCX-primary).
**Validated with:** `pnut-ts v1.55.3 -d`.

## What was found

| Category | Count |
|---|---|
| Paragraph-hosted monospace blocks | 25 |
| **Cell-hosted listings** | **5** |
| **Total extracted** | **30** |

Cell-hosted listings were looked for deliberately: the silicon-doc pass proved that a
paragraphs-only extractor misses a document's best code when it lives in table cells.

## Validation

| Result | Count |
|---|---|
| **Compile clean** under a `CON`/`DAT`/`org 0` harness with referenced symbols declared | **10 / 30** |
| Do not compile | 20 / 30 |

## The 20 — what they actually are

Every one was inspected. **None is an extraction defect.**

- **4 instruction summary tables** (`block-001`…`block-004`) — `SETQ⇥Set Q register for companion
  instruction`. Mnemonic plus a prose description; the manual's own quick-reference listings. They
  match a code-shaped pattern because every line starts with a mnemonic.
- **2 alphabetical mnemonic indexes** (`cell-01`, `cell-03`) — `AUGS / BACKCOLOR / BITC …`,
  `DIRH / DIRL / DIRNC …`. Index columns, not listings.
- **5 mixed prose + code** (`block-008`, `-009`, `-013`, `-020`, `-021`) — a narrative sentence
  sharing a monospace block with real instructions. The `;` in the prose is what the compiler
  reports (`Unrecognized character []($3b)`), not anything wrong with the code beneath it.
- **9 harness limits** — chiefly Spin2 built-in constants (`#COGEXEC_NEW` in `block-016`) and the
  auto-declarer guessing wrong on a line the compiler reports by number without naming the symbol.

## Caveat carried forward

This is a **PRELIMINARY** Parallax draft. A block compiling clean says the *extraction* is
faithful; it does not make the draft's prose authoritative. Where this manual disagrees with
`pnut-ts` or the Silicon Doc, it does **not** automatically win — and **E-016** records one place
where its prose contradicts its own table.
