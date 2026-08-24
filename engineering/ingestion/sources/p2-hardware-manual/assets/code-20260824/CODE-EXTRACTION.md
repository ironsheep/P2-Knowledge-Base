# P2 Hardware Manual (2022/11/01) — Code-Example Extraction & Validation

Pass 2 of the `ingest-source` 7-pass ingestion. Extracted DOCX-primary from
`Propeller 2 Hardware Manual - 20221101.docx`, validated with `pnut-ts v1.55.3`.

## How code was identified

This document has **no named `.spin2` listings and no complete programs**. Its code is
inline illustrative fragments, marked out by font rather than by a code style:

- The `Title` **paragraph style resolves to `Roboto Mono Medium`** in `word/styles.xml`.
  That, not the style name, is what makes a paragraph code here — a font-blind reading
  of style names alone misses ~128 code paragraphs.
- Inline runs in `Courier New` / `Roboto Mono` / `Roboto Mono Medium` are also monospace,
  but this document sets **whole prose paragraphs in monospace too**, so font alone
  over-selects. Each monospace line was then classified against the 358-mnemonic PASM2
  set (`p2-instructions-csv`).

## Validation harness

Every fragment is an excerpt, so none compiles standalone. Each was wrapped in the
minimal harness below and compiled; undefined operand symbols were declared `RES 1`
(deduplicated case-insensitively, since PASM2 symbols are case-insensitive):

```
CON
  _clkfreq = 180_000_000
DAT
        ORG
<fragment lines>
<undefined symbols>	RES	1
```

`pnut-ts -d` is used for any fragment containing `debug()`. **No fragment in this document
contains `debug()`**, so the `-d` path was never exercised here.

## Result summary

| Class | Blocks | Disposition |
|---|---:|---|
| `code` — compiles under the harness | 24 | **PASS** — staged as `blkNNN.spin2` beside this file |
| `code` — does not compile | 2 | source errata — see below |
| `illustrative-fragment` | 1 | deliberately incomplete; not compilable as printed |
| `syntax-notation` | 14 | instruction-syntax templates (`D/#,S/#`, `{WC}`) — not code |
| `bitfield-template` | 1 | binary literal with letter placeholders — not code |
| `prose-in-monospace` | 9 | dropped: prose set in a monospace font, not an example |
| **Total monospace blocks examined** | **51** | |

Per `ingest-source` §2 (*"validate, then filter"*), prose-in-monospace and syntax notation
are **dropped from the example set rather than counted as validation failures**.

## Source errata found by compiling (not present in our published YAML)

Both were confirmed verbatim in `word/document.xml` first, so neither is extraction damage.
Neither appears in `deliverables/ai/P2/`, so they are gap-ledger items, not corrections-register entries.

### Block #18 — Cog Attention

```
COGATN   #00001100			'Get attention of cogs 2 and 3
```

`pnut-ts`: `blk018.spin2:5:error:Constant must be from 0 to 511 (m130)`

SOURCE ERRATUM: '#00001100' is decimal 1100 (exceeds the 0..511 immediate range). The comment 'Get attention of cogs 2 and 3' requires bits 2 and 3, i.e. %00001100 = 12. A '%' is missing.

### Block #114 — SCOPE Data Pipe

```
        RQPIN   x,#pinblock | 3     'read pin3 long into x
        ROLBYTE y,x                 'rotate pin3 byte into y
        RQPIN   x,#pinblock | 2     'read pin2 long into x
        ROLBYTE y,x                 'rotate pin2 byte into y
        RQPIN   x,#pinblock | 1     'read pin1 long into x
        ROLBYTE y,x                 'rotate pin1 byte into y
        RQPIN   x,#pinblock | 0     'read pin0 long into x
        ROLBYTE y,x                 'rotate pin0 byte into y
```

`pnut-ts`: `blk114.spin2:6:error:Expected ","`

SOURCE ERRATUM: 'ROLBYTE y,x' is a 2-operand form. ROLBYTE has only ROLBYTE D,{#}S,#N and the ALTGB-alias ROLBYTE D (P2 Instructions v35 rows 94/95). Intent per the comments ('rotate pinN byte into y', reading the RDPIN lower byte) is ROLBYTE y,x,#0. Occurs 4x in this block.

## Deliberately incomplete

### Block #60 — Smart Modes

```
       WRPIN                           'acknowledge smart pin, releases IN from high
       NOP                             'elapse 2 clocks (or more)
       TESTP   pin     WC              'IN can now be polled again
```

bare WRPIN: operands deliberately omitted to stand for 'a WRPIN acknowledge of any pin'. WRPIN has only the form WRPIN {#}D,{#}S (P2 Instructions v35 row 217) - no zero-operand alias, so it cannot compile as printed.

## Validated fragments

| File | Section | Lines | Symbols declared by the harness |
|---|---|---:|---|
| `blk013.spin2` | Starting And Stopping Cogs | 1 | addr, id |
| `blk014.spin2` | Starting And Stopping Cogs | 1 | — |
| `blk015.spin2` | Starting And Stopping Cogs | 2 | addr, ptra_val |
| `blk016.spin2` | Starting And Stopping Cogs | 1 | myID |
| `blk017.spin2` | Starting And Stopping Cogs | 2 | myID |
| `blk019.spin2` | Cog Attention | 4 | addr |
| `blk020.spin2` | System Counter | 1 | X |
| `blk021.spin2` | System Counter | 5 | X, Y |
| `blk023.spin2` | Pseudo-Random Number Generator | 1 | x |
| `blk031.spin2` | PLL Example | 4 | — |
| `blk033.spin2` | Lock Usage | 2 | write_lock |
| `blk037.spin2` | Multiply | 2 | lower_long, upper_long |
| `blk042.spin2` | Divide | 2 | quotient, remainder |
| `blk100.spin2` | About SINC2 and SINC3 filtering | 4 | adcpin, diff, x |
| `blk101.spin2` | About SINC2 and SINC3 filtering | 4 | adcpin, diff, x |
| `blk103.spin2` | SINC2 Sampling Mode (%00) | 3 | adcpin |
| `blk104.spin2` | SINC2 Sampling Mode (%00) | 1 | adcpin, sample |
| `blk105.spin2` | SINC2 Filtering Mode (%01) | 3 | adcpin |
| `blk106.spin2` | SINC2 Filtering Mode (%01) | 10 | adcpin |
| `blk107.spin2` | SINC3 Filtering Mode (%10) | 3 | adcpin |
| `blk108.spin2` | SINC3 Filtering Mode (%10) | 13 | adcpin |
| `blk110.spin2` | Bitstream Capturing Mode (%11) | 4 | adcpin, bitstream |
| `blk130.spin2` | Asynchronous Serial Transmit (%11110) | 4 | txpin, x |
| `blk140.spin2` | Prop_Hex | 5 | — |

## Not code, kept for the record

| Class | Section |
|---|---|
| `bitfield-template` | System Clock Configuration |
| `syntax-notation` | Locks (Semaphores) |
| `syntax-notation` | Multiply |
| `syntax-notation` | Divide |
| `syntax-notation` | Divide |
| `syntax-notation` | Divide |
| `syntax-notation` | Divide |
| `syntax-notation` | Square Root |
| `syntax-notation` | Rotation |
| `syntax-notation` | Cartesian to Polar |
| `syntax-notation` | Polar to Cartesian |
| `syntax-notation` | Integer to Logarithm |
| `syntax-notation` | Logarithm to Integer |
| `syntax-notation` | Smart Modes |
| `syntax-notation` | USB Host/Device (%11011) |

