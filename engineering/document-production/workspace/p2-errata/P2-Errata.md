```{=latex}
% Banner image at top (full width) with drop shadow for visual balance
\begin{tcolorbox}[
  enhanced,
  boxrule=1.5pt,
  colframe=gray!60,
  colback=white,
  drop shadow southeast,
  shadow={3pt}{-3pt}{1mm}{black!15},
  left=0pt, right=0pt, top=0pt, bottom=0pt,
  width=\textwidth,
  arc=0pt,
  outer arc=0pt
]
\includegraphics[width=\linewidth]{inbox/assets/book-artwork.png}
\end{tcolorbox}

\begin{center}
\vspace{0.35cm}
{\fontsize{36}{42}\selectfont\bfseries P2 Errata\par}
\vspace{0.3cm}
{\Large\itshape Silicon Defects of the Propeller 2 Found So Far, Proven on P2 Hardware\par}
\vspace{0.35cm}
{\large September 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 0.2.0\par}
\vspace{0.25cm}
{\large\bfseries\color{red!70!black} Community Review Draft \textperiodcentered\ Build 2026-09-26\par}

\vspace{0.3cm}
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} The Errata Found So Far},
  colbacktitle=gray!15,
  coltitle=black
]
{\small
\begin{itemize}[leftmargin=*, itemsep=2pt, topsep=2pt]
\item \textbf{E1} \enspace SETQ Block Transfers Lose Their Pointer Step
\item \textbf{E2} \enspace An Immediate ALTx Takes a Pending AUGS
\item \textbf{E3} \enspace GETCT Returns a Stale Upper Long
\item \textbf{E4} \enspace GETXACC Clears Only During a Goertzel Burst
\item \textbf{E5} \enspace The Goertzel Accumulators Trail by One Clock
\item \textbf{E6} \enspace In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC
\item \textbf{E7} \enspace A Blocking RDFAST Can Skip Its Wait After a No-Wait RDFAST
\end{itemize}
\vspace{0.05cm}
Each erratum opens with what to expect, what happens instead, and what any
workaround must do, then gives one workaround proven on P2 hardware.
}
\end{tcolorbox}
\vspace{0.05cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}

\tableofcontents
\clearpage
```

# Copyright and License

```{=latex}
\markboth{}{}
```

Copyright © 2026 Iron Sheep Productions, LLC and Parallax Inc.

This work is licensed under the Creative Commons Attribution–ShareAlike 4.0 International License (CC BY-SA 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

To view the full license, visit: https://creativecommons.org/licenses/by-sa/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc. This license grants permissions under copyright only; it does not grant rights to use these trademarks, and adapted or redistributed copies must not imply endorsement by, or official status with, Iron Sheep Productions, LLC or Parallax Inc.

## Acknowledgments

**Parallax Inc.** for the Propeller 2, and for publishing its known silicon defects in the P2 Documentation. Errata E1 and E2 are Parallax's own findings.

**Chip Gracey** for the design of the Propeller 2 and for the detailed silicon documentation that states what the part is meant to do. Every erratum here is measured against that statement.
**The clean-room design study** for predicting errata E3, E4, E5 and E6 from the design material alone, and for the classification of findings this manual follows. The study read the design without Parallax's documentation or a bench; the predictions were then tested on P2 hardware, independently, for this manual. Erratum E7 was not predicted: it was found on the bench, by a test built to measure something else.

## Sources

- **Parallax Propeller 2 Documentation v35 (Rev B/C)** (Chip Gracey, Parallax Inc.): what the design says, including its KNOWN BUGS section.
- **Tests on P2 hardware** (P2 Knowledge Base Project): every erratum in this manual was confirmed on **Rev C** silicon, the revision in production, by a test program that is included in the examples archive.
- **P2 Knowledge Base YAML** (Iron Sheep Productions / P2 Knowledge Base Project): instruction semantics and encodings.

## About This Draft

This is a **community review draft**. Its errata are confirmed on silicon, and so is every workaround it prints; its wording, its structure and its explanations are open for review. Any further behaviour that a test on P2 hardware shows to be a silicon erratum will be added as E8 onward.

Erratum numbers are **permanent**. A number is never reused or reassigned, so E3 means the same defect in every edition.

## What Counts as an Erratum

Every finding describes something the P2 does when a program runs, and each belongs to exactly one of three classes. What decides the class is what the chip's own design material says, not how bad the effect is.

| Class | Definition |
|---|---|
| **Silicon erratum** | The part does not do what its own design says it should. |
| **Anti-pattern** | Legal code that does something other than what it appears to do. |
| **Open question** | The delivered material cannot settle it. |

**This manual lists silicon errata only.** For an erratum there has to be a specific written statement of intent, in the design or in Parallax's published documentation, that P2 hardware contradicts. Anti-patterns are documented, with their safe forms, in the companion manual *P2 Anti-Patterns*. An open question is published as neither.

The list is open-ended. These are the silicon errata **found so far**.

## How Each Erratum Is Built

Each erratum has a chapter of its own, headed with its number: *Erratum E3* describes E3. It opens with a CAUTION box of three lines: what the P2 Documentation says to expect, what the part does instead, and the workaround: the condition any way of avoiding the erratum must meet. The sections that follow are the same in every erratum, in the same order:

| Section | What it gives |
|---|---|
| **What the P2 is documented to do** | the written statement the part contradicts, whose it is, and where it is written |
| **What the P2 does** | the defect: which instructions, in what arrangement, with what result |
| **What your program sees** | what the defect looks like in a program, and what it does not affect |
| **A proven workaround** | what any workaround must do, then one way that meets it: a drop-in block of code proven on P2 hardware, what it guarantees, and what it costs |
| **Why it happens** | the mechanism, at the level of the programmer's model |
| **How it was proven on P2 hardware** | the test on P2 hardware, its controls, and the measured values |
| **The test program** | a walkthrough of the test, and its filename in the examples archive |
| **Status** | who published it, who found it, what is confirmed, and what it affects |

The part keeps its defect, so this manual offers workarounds, never fixes: code that steps around the erratum. Each workaround printed is **one** way to meet the condition, not the only way, and it is printed exactly as it ran on silicon. Each is one of three kinds: a **one-time startup workaround**, added once when the program starts; a **rule at each use**, followed wherever the affected instruction is used; or a **helper routine**, called in place of the affected sequence.

## Summary

| E | Erratum | Affects | Published by Parallax | What any workaround must do (proven way) |
|---|---|---|:--:|---|
| **E1** | SETQ Block Transfers Lose Their Pointer Step | `SETQ`/`SETQ2` block `RDLONG`/`WRLONG`/`WMLONG` with a `PTRx` expression, when an `ALTx`, `AUGS` or `AUGD` sits between them | Yes | Nothing between `SETQ` and the transfer (keep them adjacent; rule at each use) |
| **E2** | An Immediate ALTx Takes a Pending AUGS | an `ALTx` with an immediate `#S` between `AUGS` and its target | Yes | No immediate-`#S` `ALTx` between `AUGS` and its target (give the `ALTx` a register `S`; rule at each use) |
| **E3** | GETCT Returns a Stale Upper Long | `GETCT WC` in a cog of 4-7 whose group had no cog running when the counter's lower long wrapped | No | A cog of 4-7 running at every wrap of the lower long (a keeper cog started first; one-time startup workaround) |
| **E4** | GETXACC Clears Only During a Goertzel Burst | `GETXACC` while the streamer is idle or in any mode other than Goertzel | No | Take each burst's sums as a difference of idle reads (the `burst_sums` routine, SINC1; helper routine) |
| **E5** | The Goertzel Accumulators Trail by One Clock | every Goertzel burst: its last term is added to the next burst | No | Deliver the held term before reading (the `burst_sums` routine, SINC1; helper routine) |
| **E6** | In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC | a DAC smart-pin mode with `TT` = `%00` whose ADC is switched with `OUT` | No | `TT` bit 0 set in the `WRPIN` word (rule at each use) |
| **E7** | A Blocking RDFAST Can Skip Its Wait After a No-Wait RDFAST | a blocking `RDFAST` issued 8 to 15 clocks after a no-wait `RDFAST` | No | At least 16 clocks between the two `RDFAST`s (`WAITX #12` directly after the no-wait one; rule at each use) |

## Document Conventions

| Element | Format | Example |
|---------|--------|---------|
| Instructions | Uppercase in running text, lowercase in code | `SETQ`, `setq` |
| Registers / symbols | Monospace | `PTRA`, `CT` |
| Bit fields | Brackets | D[31:0], `imm[15:12]` |
| Hexadecimal | Dollar prefix | `$3C5C_0A55` |
| Binary | Percent prefix | `%1111` |

```{=latex}
\clearpage
```


# Erratum E1: SETQ Block Transfers Lose Their Pointer Step {#ch-e1}

::: caution
**Expected:** A `SETQ` or `SETQ2` block `RDLONG` or `WRLONG` through `ptra++` moves `PTRA` past the whole block, 4 bytes per long (P2 Documentation, *FAST BLOCK MOVES*).

**Actual:** With an `ALTD` between the `SETQ` and the transfer, every long still moves, but `PTRA` moves only 4 bytes, the step `ptra++` gives a single long.

**Workaround:** Nothing may sit between the `SETQ` or `SETQ2` and the transfer it prepares; see *A proven workaround*.
:::

The erratum affects PASM code that places an `ALTD` between a `SETQ` or `SETQ2` and the block transfer it prepares, to redirect the block's first register, and then uses `PTRx` after the transfer: a loop that walks a hub buffer one block at a time, or an address computed from the pointer. Code that reloads the pointer before its next use is not affected. Parallax publishes the defect in the P2 Documentation.

## What the P2 is documented to do {#sec-e1-documented}

A `SETQ` or `SETQ2` placed before `RDLONG`, `WRLONG` or `WMLONG` turns that instruction into a fast block move. The P2 Documentation, in its section *FAST BLOCK MOVES*, states what a `PTRx` expression does in a block move:

> For fast block moves, PTRx expressions cannot have arbitrary index values, since the index will be overridden with the number of longs, with bit 4 of the encoded index value serving as the `++`/`--` indicator.

Its example for `SETQ #x` followed by `RDLONG first_reg,PTRA++` reads x+1 longs from `PTRA` and gives the update as `PTRA += (x+1)*4`: the pointer moves past the whole block. Outside a block move, the same document defines a `PTRx` update as `PTRx += INDEX*SCALE`, where `SCALE` is 4 for `RDLONG`, `WRLONG` and `WMLONG`. A plain `ptra++` therefore moves `PTRA` by 4, and `ptra++[3]` moves it by 12.

The P2 Documentation records the departure from the block rule in its KNOWN BUGS section:

> Intervening ALTx/​AUGS/​AUGD instructions between SETQ/​SETQ2 and RDLONG/​WRLONG/​WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas. The expected number of longs will transfer, but PTRx will only be modified according to normal PTRx expression behavior:

The example that follows loads 16 longs with `SETQ #16-1`, alters the start register with `ALTD start_reg`, and issues `RDLONG 0,ptra++`. Its comment gives the result: `ptra` is incremented by 4 (1 long), not by 16*4.

## What the P2 does {#sec-e1-actual}

With an `ALTD` between `SETQ` or `SETQ2` and a block `RDLONG` or `WRLONG` that carries a post-increment `PTRx` expression, one instruction does two things:

- **The transfer completes as written, and the redirect holds.** The number of longs set by `SETQ` or `SETQ2` moves, to or from the registers the `ALTD` selects. The block is read from, or written to, the hub address `PTRx` held before the instruction.
- **`PTRx` takes the plain expression's step.** The pointer changes by the amount the same expression gives without a `SETQ`: +4 for `ptra++` and `ptrb++`, +12 for `ptra++[3]`. The step does not depend on the block length. An 8-long block moved `PTRA` by +4, the same as a 4-long block.

This held for every form tested: `SETQ` with `RDLONG` into cog registers at 4 and at 8 longs, `SETQ2` with `RDLONG` into lookup RAM, and `SETQ` with `WRLONG` from cog registers, through `PTRA` and through `PTRB`, with `ptra++` and with `ptra++[3]`. The measured values are in *How it was proven on P2 hardware*.

The confirmation is narrower than Parallax's statement. **Only `ALTD` was tested as the intervening instruction; Parallax names `ALTx`, `AUGS` and `AUGD`.** `WMLONG`, `SETQ2` with `WRLONG`, and the decrement and pre-modify forms (`ptra--`, `++ptra`, `--ptra`) were not tested. In the pre-modify forms the expression also sets the hub address the block starts from, so what the part does with that address under this erratum is not established here.

An `ALTD` on its own does not disturb the pointer. A single `RDLONG` with `ptra++`, redirected by `ALTD` and with no `SETQ` before it, moved `PTRA` by +4, as it does without the `ALTD`.

## What your program sees {#sec-e1-sees}

Your data is right and your pointer is not. Every long of the block lands where the `ALTD` sends it, the longs on either side of the block are untouched, and the hub side of the transfer starts at the address `PTRx` held. Only the value left in `PTRx` differs: after a 4-long block through `ptra++`, `PTRA` points 4 bytes past the start of the block instead of 16.

You see the effect at the next access through that pointer. A loop that walks a hub buffer block by block with `SETQ`, `ALTD` and `RDLONG ..., ptra++` starts each block 4 bytes after the start of the previous one, not after its end, so its reads return overlapping data. The same loop built on `WRLONG` writes each block over all but the first long of the block before it. Any address your code computes from `PTRx` after the transfer carries the same error.

## A proven workaround {#sec-e1-workaround}

**What any workaround must do:** nothing may sit between the `SETQ` or `SETQ2` and the block transfer it prepares, so that the transfer is the instruction directly after it.

**One way, proven on P2 hardware:** write the `SETQ` or `SETQ2` directly before the transfer.

```pasm2
CON ' ---- E1 Workaround: Block Length ----
  BLOCK_LONGS   = 4                     ' longs in your block

DAT ' ---- E1 Workaround: Block Transfer ----
                setq    #BLOCK_LONGS - 1        ' directly before RDLONG
                rdlong  block_first, ptra++     ' block's first register
```

With the `SETQ` or `SETQ2` as the instruction directly before the transfer, the whole block moves and `PTRx` steps past all of it: a *rule at each use*. In your code, `BLOCK_LONGS - 1` is your block length minus one and `block_first` is the first register of your block.

These two lines are the test program's control for the 4-long read, and on silicon they advanced `PTRA` by +16 in every round, with all four longs in place. The same adjacent form gave the full block step for an 8-long read (+32), through `PTRB`, for a `WRLONG` from cog registers, for `SETQ2` into lookup RAM, and with `ptra++[3]` (+16 each, for 4 longs); in the last, the block count overrides the index, as the P2 Documentation states.

The cost is the redirect. Without the `ALTD`, the block's first register is the one named in the instruction's `D` field, set when the code is assembled. No form that keeps the redirect has been run on silicon, so none is printed here. The adjacent form was run for the six transfers above; the forms named as untested in *What the P2 does* were not run in it either.

## Why it happens {#sec-e1-why}

A block transfer depends on the cog knowing that a `SETQ` or `SETQ2` came before it, and the cog keeps that knowledge in two forms.

The first form is held across an intervening `ALTx`, `AUGS` or `AUGD`, so that those instructions can sit between a `SETQ` and the transfer it prepares. The transfer takes its long count from this held form, which is why the full block still moves.

The pointer update does not use the held form. It asks only whether the instruction immediately before the `RDLONG`, `WRLONG` or `WMLONG` was a `SETQ` or `SETQ2`. With an `ALTD` in that position the answer is no, so the pointer is updated as for a single-long access: by the index encoded in the `PTRx` expression, times 4. For `ptra++` the index is 1, giving 4; for `ptra++[3]` it is 3, giving 12.

By the same reasoning an `AUGS` or `AUGD` in that position also breaks the adjacency the pointer update looks for. The test program did not exercise them.

## How it was proven on P2 hardware {#sec-e1-proof}

The test runs on a bare P2 board at 200 MHz. The measurement runs in a PASM cog of its own, started with `COGINIT`, because the Spin2 interpreter in cog 0 uses `PTRA` as its stack pointer. The debugger's interrupt is confined to cog 0 (`DEBUG_COGS = %0000_0001`), so it never enters the measuring cog. Cog 0 reads the results from hub RAM and does all checking and printing.

The measuring cog runs 15 arms, one after another, as one round, and runs 4 rounds, interleaved. Each arm loads the pointer, copies it to a register, executes one transfer, and copies the pointer again; the change in the pointer is the second copy minus the first. Before every arm, the destination region and a separate trap region are refilled with the sentinel `$5E5E_5E5E` and the pointer is reloaded, so no arm inherits another's data. Hub source long *k* holds `$A5A0_0000` + *k*, and each read starts at source long 4, so a complete block read from there holds `$A5A0_0004` onward.

Each hazard arm (`SETQ`, `ALTD`, transfer) is paired with a control arm that is the same transfer with no `ALTD`. The hazard arm's own `D` field names the trap region, and its `ALTD` redirects the block to the place the control writes. A lost `ALTD` would put the block in the trap; a lost `SETQ` would move one long. Both possible pointer changes were written into the program before the run: the plain expression's step if the erratum holds, the block step if it does not. Three single-long references establish the plain steps on this part, and every control had to read its required change and a complete, correctly placed block in every round before any verdict was given.

The results, from the second run, in bytes:

| Transfer | Longs | Without `ALTD` | With `ALTD` | Longs at the `ALTD` destination |
|---|:--:|:--:|:--:|:--:|
| `setq #3` + `rdlong ..., ptra++` | 4 | +16 | **+4** | 4/4 |
| `setq #7` + `rdlong ..., ptra++` | 8 | +32 | **+4** | 8/8 |
| `setq #3` + `rdlong ..., ptra++[3]` | 4 | +16 | **+12** | 4/4 |
| `setq #3` + `rdlong ..., ptrb++` | 4 | +16 | **+4** | 4/4 |
| `setq #3` + `wrlong ..., ptra++` | 4 | +16 | **+4** | 4/4 |
| `setq2 #3` + `rdlong` (lookup RAM) `..., ptra++` | 4 | +16 | **+4** | 4/4 |

The *Without `ALTD`* column is the workaround: each control is the same transfer with the `SETQ` or `SETQ2` directly before it, and the first row's control is the two lines printed in *A proven workaround*. In the `wrlong` row, the four longs that reached hub RAM are the ones in the registers the `ALTD` selected. The single-long references read +4 for `rdlong ..., ptra++`, +4 for the same instruction redirected by `ALTD`, and +12 for `rdlong ..., ptra++[3]`.

Every round of every arm gave the same value. In every arm the trap region was untouched: it held the sentinel after each read arm, and the write arm's trap registers kept their initial values `$7E7E_0000` + *k*. For the first row, round 0 printed `before=$0000_23C8 after=$0000_23D8 delta=16` for the control and `before=$0000_23C8 after=$0000_23CC delta=4` for the hazard arm, with `$A5A0_0004` to `$A5A0_0007` in destination slots 2 to 5 in both.

The test was run twice on 2026-09-24, from two builds of the program: as first written, and after a style revision that left the measuring code unchanged. The hub addresses differ between the builds (the read arms' pointer started at `$0000_23B8` in the first run and `$0000_23C8` in the second), and every pointer change and every data result matched. The values above are read from the per-round raw lines, not from the program's own verdict line.

## The test program {#sec-e1-program}

The test program is `e1-setq-block-pointer-step-test.spin2` in the examples archive. Its measuring cog is one PASM routine that runs the 15 arms in sequence. Each arm has the same frame: `prep_cog` refills the destination region `dst` and the trap region `trp` with the sentinel; the pointer is loaded from `c_rsrc`, the hub address of source long 4; `c_before` and `c_after` capture the pointer around the transfer; and `dump_cog` writes the pointer pair and both regions to a record in hub RAM.

The control for the primary pair, `SETQ` directly before `RDLONG`, carries the workaround in this frame:

```pasm2
                call    #prep_cog
                mov     ptra, c_rsrc
                mov     c_before, ptra
' ---- DROP-IN BEGIN ----
CON ' ---- E1 Workaround: Block Length ----
  BLOCK_LONGS   = 4                     ' longs in your block

DAT ' ---- E1 Workaround: Block Transfer ----
                setq    #BLOCK_LONGS - 1        ' directly before RDLONG
                rdlong  block_first, ptra++     ' block's first register
' ---- DROP-IN END ----
                mov     c_after, ptra
                call    #dump_cog
```

The hazard arm places the `ALTD` between them. Its `RDLONG` names the trap region, `trap_first`; the register `c_hidx` holds the address `block_first`, so a working `ALTD` sends the block to the same registers the control uses:

```pasm2
'--- arm 3  H_BLK4 : PRIMARY hazard -- SETQ / ALTD / RDLONG ptra++
                call    #prep_cog
                mov     ptra, c_rsrc
                mov     c_before, ptra
                setq    #BLOCK_LONGS - 1
                altd    c_hidx
                rdlong  trap_first, ptra++
                mov     c_after, ptra
                call    #dump_cog
```

The other arms follow the same frame: `setq #WIDE_BLOCK_LONGS - 1` for the 8-long pair, `ptra++[3]` and `ptrb++` for the index and pointer pairs, `wrlong` from the cog registers `wsrc` with the trap `wtrp` for the write pair, and `setq2` into lookup RAM for the last pair. In the listing the three instructions of every hazard arm are consecutive longs, so nothing else sits between the `SETQ`, the `ALTD` and the transfer.

Cog 0 computes each arm's pointer change from the record:

```spin2
  pRec := recaddr(armIdx, rp)
  deltaVal := long[pRec][REC_AFTER] - long[pRec][REC_BEFORE]
```

For every arm and round the program prints the pointer before and after, the change, a data class (`FULL` when the block is complete and correctly placed and both regions are otherwise untouched), and the raw contents of both regions. It then prints one line confirming that every control passed, one verdict line per hazard arm, and the verdict for the primary pair last. The program runs once, in well under a second, from RAM with DEBUG enabled; its output is on the DEBUG terminal.

## Status {#sec-e1-status}

| Field | Content |
|---|---|
| Erratum | E1 |
| Published by Parallax | Yes, *P2 Documentation*, KNOWN BUGS |
| Found by | Parallax |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes — 2026-09-24, rule at each use: `SETQ`/`SETQ2` directly before the transfer |
| Affects | a `SETQ`/`SETQ2` block `RDLONG`/`WRLONG`/`WMLONG` with a `PTRx` update expression, when an `ALTx`, `AUGS` or `AUGD` sits between them (confirmed with `ALTD`) |
| Test program | `e1-setq-block-pointer-step-test.spin2` |


# Erratum E2: An Immediate ALTx Takes a Pending AUGS {#ch-e2}

::: caution
**Expected:** An `ALTx` with a nine-bit immediate `#S` leaves its `D` register unchanged
(P2 Documentation, *REGISTER INDIRECTION*).

**Actual:** Between an `AUGS` and the instruction the `AUGS` was written for, the `ALTx`
takes the augment too, and its `D` register moves by bits 17:9 of the augmented value.

**Workaround:** No `ALTx` with an immediate `#S` may sit between an `AUGS` and the
instruction the `AUGS` was written for; see *A proven workaround*.
:::

The erratum affects PASM code that writes an `AUGS` explicitly and places an `ALTx` with
an immediate `#S` between it and the instruction it was written for, as in Parallax's own
example. The `##` literal syntax does not produce this arrangement by itself: the
assembler places the `AUGS` it generates immediately before the instruction that carries
the `##`. Parallax publishes the defect in the P2 Documentation.

## What the P2 is documented to do {#sec-e2-documented}

An `AUGS` holds 23 bits for the next instruction that carries a literal `#S`. That
instruction takes them as bits 31:9 of its `S`, keeps its own 9-bit field as bits 8:0,
and the augment is cancelled. The `ALTx` instructions accept an augmented `S`: their `S`
may be a register, a 9-bit literal or an augmented literal.

The P2 Documentation, in its section *REGISTER INDIRECTION*, describes how `ALTS`, `ALTD`
and `ALTR` use that `S`: the sum of `D[8:0]` and `S[8:0]` is the address substituted into
the next instruction, so `S` serves as a register base and `D` as an index. It continues:

> Additionally, S[17:9] is always sign-extended and added to the D register for index
> updating. Normally, a nine-bit #address will be used for S, causing S[17:9] to be zero,
> so that D is unaffected:

The same document publishes the defect, under KNOWN BUGS:

> Intervening ALTx instructions with an immediate #S operand, between AUGS and the AUGS'
> intended target instruction (which would have an immediate #S operand), will use the
> AUGS value, but not cancel it. So, the intended AUGS target instruction will use and
> cancel the AUGS value, as expected, but the intervening ALTx instruction will also use
> the AUGS value (if it has an immediate #S operand). To avoid problems in these
> circumstances, use a register for the S operand of the ALTx instruction, and not an
> immediate #S operand.

Parallax's example places `ALTD index,#base` between `AUGS #$FFFFF123` and the
`ADD 0-0,#$123` the `AUGS` was written for, and marks the `ALTD` line "Look out! AUGS
will affect #base, too. Use a register, instead." The published statement does not say
what the `ALTx` does with the value it takes, and it names `AUGS` only; it says nothing
about `AUGD` in this arrangement.

## What the P2 does {#sec-e2-actual}

The arrangement is `AUGS #value`, then an `ALTx` with an immediate `#S`, then the target
instruction with an immediate `#S`. On the part:

- The `ALTx` receives the augmented 32-bit `S`: bits 31:9 from the `AUGS`, bits 8:0 from
  its own 9-bit field.
- The augment is not cancelled. The target receives the same augmented value.
  Parallax's statement adds that the target then cancels it; the test did not check an
  instruction after the target.

Because `S[8:0]` is still the `ALTx`'s own field, its base is unchanged and the
instruction after it is redirected to the register the program names. What changes is
the auto-increment: `S[17:9]` now comes from the `AUGS` value, and after the `ALTx`
executes, its `D` register has moved by the sign-extended value of those bits. With an
augment of `$3C5C_0A55`, whose bits 17:9 are 5, `ALTD idx,#0` and `ALTR idx,#3` each
moved `idx` by 5, and in each case the target wrote the full augmented value
`$3C5C_0A55` into the register aimed at.

The bench tested `ALTD` and `ALTR` as the intervening instruction; Parallax's statement
covers the `ALTx` instructions generally. In every tested case the `ALTx` sat directly
after the `AUGS` and the target directly after the `ALTx`; other spacings were not
tested. One augment value was used. An `AUGS` written for the `ALTx` itself (the
augmented-literal form of its `S`) was not tested.

**`AUGD` in the same position.** A pending `AUGD` survived an intervening
immediate-`S` `ALTx`. `AUGD #$1357_9B3C`, then `ALTS idxs,#0`, then `WRLONG #$13C` wrote
`$1357_9B3C`, the full augmented value, and `idxs` did not move. One `ALTx` (`ALTS`) and
one augment value were tested for this half.

## What your program sees {#sec-e2-sees}

Your `ALTx`'s `D` register changes when your program expects it to stay put. A 9-bit
immediate `#S` has bits 17:9 clear, so an immediate-`S` `ALTx` on its own has an
auto-increment of 0; in this arrangement it takes bits 17:9 of the augment instead. Any
later instruction that uses that register, such as the next pass of a loop that indexes
with it, sees the moved value.

What does not go wrong, in the tested cases:

- The instruction after the `ALTx` is redirected to the register your program names.
- The target receives the full augmented value.
- No other register in a 32-register window around the target was written.

The size of the move is set by bits 17:9 of the augment, which the documented field
split makes the auto-increment; by that split, an augment whose bits 17:9 are zero moves
nothing. The only value measured was 5.

## A proven workaround {#sec-e2-workaround}

**What any workaround must do:** no `ALTx` with an immediate `#S` may stand between an
`AUGS` and the instruction the `AUGS` was written for.

**One way, proven on P2 hardware:** give that `ALTx` a register `S`.

```pasm2
                augs    #AUGV
                altd    idx, sreg4
                mov     0-0, #LO
```

With a register `S` on the `ALTD`, the `ALTD` takes nothing from the `AUGS`, `idx` does
not move, and the augment reaches the target: a *rule at each use*.

In these lines `AUGV` is the 32-bit value the `AUGS` carries for the `MOV`, `LO` is its
low 9 bits, and `sreg4` is a cog register that holds the `ALTD`'s `S`: the base, 4, in
bits 8:0 and a zero auto-increment in bits 17:9. In your code, the base and any
auto-increment that were in the immediate `#S` go into that register. On silicon, with
`AUGV` = `$3C5C_0A55`, the `MOV` was redirected to the register four along from the one
`idx` addressed, which received `$3C5C_0A55`, and `idx` did not move. This way costs one
cog register for each distinct `S` value.

**The one-operand form is not a register form.** `ALTD idx` assembles to the same
instruction word as `ALTD idx,#0`: immediate bit set, `S` = 0. That is the arrangement
the test showed affected. The one-operand form of every `ALTx` instruction is encoded
with the immediate bit set, so writing it does not meet the condition.

Any other arrangement that keeps every immediate-`#S` `ALTx` out of the span from an
`AUGS` to its target meets the same condition. None other was run on silicon.

This way was run with `ALTD` as the intervening instruction, one augment value and one
base. Parallax's statement directs a register `S` for any `ALTx` in this position; no
other `ALTx` was run with one.

## Why it happens {#sec-e2-why}

An `AUGS` changes nothing in memory. It holds its 23 bits pending, and the next
instruction that fetches an immediate `S` receives them as the upper bits of that `S`.
Using the augment normally ends the pending state.

The `ALTx` instructions are a planned exception to that last step. An `ALTx` may stand
between an `AUGS` and its target without ending the pending state, so that an augment
can reach an instruction that follows an `ALTx`; Parallax's statement that the target
"will use and cancel the AUGS value, as expected" describes that intent. The exception
covers only the ending of the pending state. The choice of which instruction receives
the augmented value has no such exception: to that choice, an `ALTx` with an immediate
`#S` is one more instruction with an immediate `S`, so it receives the augment for
itself. Because it is an `ALTx`, it then leaves the augment pending, and the target,
the next instruction with an immediate `S`, receives the same value.

An `ALTx` with a register `S` has no immediate `S` to augment. It neither receives the
value nor ends the pending state, which is why the workaround holds.

The effect is confined to the auto-increment because of how an `ALTx` reads its `S`.
The augment supplies bits 31:9 and leaves bits 8:0 alone. Bits 8:0 are the base, so the
redirection is unaffected. Bits 17:9 are the auto-increment, so the `D` register moves.

`AUGD` is the corresponding mechanism for a literal `#D`. The `ALTx` instructions have
no immediate form for `D`: their encodings carry an immediate bit for `S` only, and
their `D` is always a register. An `ALTx` therefore has no immediate `D` to receive a
pending `AUGD`, and the `AUGD` passes to its target.

## How it was proven on P2 hardware {#sec-e2-proof}

**Arrangement.** A P2 board with nothing connected to its pins, at 200 MHz. The
measuring code is PASM, started in a fresh cog with `COGINIT` from the program's `DAT`
section. The debug interrupt was enabled in cog 0 only (`DEBUG_COGS = %0000_0001`) and
the measuring cog enabled no interrupts, so nothing could split a sequence; cog 0 only
read the results from hub RAM and printed them. Before each arm, the measuring cog
filled a window of 32 cog registers, `win[0]` to `win[31]`, with a sentinel unique to
the arm and the slot (for arm A6, slot 8: `$5E5E_0608`), and set `idx` to the cog
address of `win[8]`. After each arm it copied the window and `idx` to hub RAM. The
augment was `$3C5C_0A55`: bits 8:0 are `$055`, the target's own 9-bit field, and bits
17:9 are 5, so an `ALTx` that received it would move `idx` by 5.

**Arms and results** (the program's own arm labels; "moved" is `idx` after the arm minus
`idx` before):

| Arm | Sequence | Written | Value | Moved |
|---|---|---|---|---|
| A0 | `MOV win[8],#$055` | `win[8]` | `$0000_0055` | 0 |
| A1 | `AUGS`, `MOV win[8],#$055` | `win[8]` | `$3C5C_0A55` | 0 |
| A2 | `ALTD idx,#0`, `MOV 0-0,#$055` | `win[8]` | `$0000_0055` | 0 |
| A3 | `ALTD idx,sinc` (`$A00`), `MOV 0-0,#$055` | `win[8]` | `$0000_0055` | 5 |
| A4 | `ALTR idx,#3`, `MOV win[0],#$055` | `win[11]` | `$0000_0055` | 0 |
| A5 | `AUGS`, `ALTD idx,sreg4` (4), `MOV 0-0,#$055` | `win[12]` | `$3C5C_0A55` | 0 |
| A6 | `AUGS`, `ALTD idx,#0`, `MOV 0-0,#$055` | `win[8]` | `$3C5C_0A55` | 5 |
| A7 | `AUGS`, `ALTR idx,#3`, `MOV win[0],#$055` | `win[11]` | `$3C5C_0A55` | 5 |

In every arm exactly one window register changed. A0 to A5 are controls, and the
program issues no verdict unless all of them read exactly as expected. A1 shows the
augment reaching an adjacent target. A2 and A4 show that an immediate-`S` `ALTx` with no
`AUGS` pending leaves `idx` unchanged. A3 shows, on this part, that an `S` whose bits
17:9 are 5 moves `idx` by 5 and leaves the redirected register at `win[8]`: the same
field an augment of `$3C5C_0A55` would fill. A5 is the workaround: its three instructions
are the lines printed in *A proven workaround*. A6 and A7 are the defect: the `ALTx` moved `idx` by 5,
and the target still wrote `$3C5C_0A55`.

**The `AUGD` half.** Before each of these two arms the measuring cog wrote
`$D5D5_D5D5` to the hub long the arm writes. The control, `AUGD #$1357_9B3C` directly
before `WRLONG #$13C`, wrote `$1357_9B3C`. The test, with `ALTS idxs,#0` between the
`AUGD` and the `WRLONG`, also wrote `$1357_9B3C`; `idxs` read `$0000_0061` before and after. `idxs` held the cog
address of the register the `WRLONG` takes its hub address from, so the `ALTS`
substitution left the `WRLONG`'s address unchanged.

**Repetition.** Nothing in this test depends on timing, so the plan was repetition: the
whole battery ran three times, each in a freshly started cog, and the three hub records
were compared long for long. They were identical. The program was run twice on
2026-09-24, from two builds of the same measuring code, and every measured value matched
between the runs.

**Assembly checked.** Before the run, every `AUGS`, `AUGD` and `ALTx` instruction word
was read back from the assembler listing and its encoding confirmed. The `AUGS`
assembled to `$FF1E2E05`.

## The test program {#sec-e2-program}

The test program is `e2-altx-takes-pending-augs-test.spin2`, a single Spin2 file that
runs the measuring cog in PASM and prints its results with `debug()`. Compile it with
DEBUG enabled (`pnut-ts -d`, or PNut) and run it with the debug terminal open; it prints
about 40 lines and ends in one `VERDICT:` line, or a `RIG FAIL:` line and no verdict if
any control is wrong.

The augment is chosen so that its two fields can be told apart:

```spin2
  AUGV       = $3C5C_0A55          ' AUGS payload: [17:9] = 5, [8:0] = $055
  LO         = AUGV & $1FF         ' $055 = the target's own 9-bit #S
```

A third constant, `AUTOINC`, shifts `AUGV` right by `ALT_INC_SHIFT` (9) and masks it with `$1FF`, which leaves bits 17:9: the value 5, the step by which the erratum moves `idx`.

The workaround arm and the `ALTD` test arm differ only in the form of the `ALTD`'s `S`.
Each arm fills the window, runs its sequence, and dumps the window and `idx` to hub RAM:

```pasm2
' ---- A5 ctrl: WORKAROUND -- register-S ALTD between AUGS and target ----
                mov     armn, #ARM_WORKAROUND
                call    #fill
                augs    #AUGV
                altd    idx, sreg4
                mov     0-0, #LO
                call    #dump

' ---- A6 TEST: immediate-#S ALTD between AUGS and target ----
                mov     armn, #ARM_TD
                call    #fill
                augs    #AUGV
                altd    idx, #0
                mov     0-0, #LO
                call    #dump
```

The two register `S` values used by the controls hold the auto-increment and the base
in their separate fields: `sinc` is `AUTOINC` shifted into bits 17:9 by `ALT_INC_SHIFT` (base 0, auto-index +5); `sreg4` is the plain base `ALTD_REG_BASE` (4, no auto-increment):

```pasm2
sreg4           long    ALTD_REG_BASE    ' register S: base 4, auto-index 0
```

The `AUGD` test places an immediate-`S` `ALTS` between the `AUGD` and its `#D` target,
and records `idxs` before and after:

```pasm2
' ---- D2 TEST: immediate-#S ALTS between AUGD and its #D target ----
                wrlong  sentd, hubd2
                mov     idxs, #hubd2
                wrlong  idxs, ptra[H_IDXS0]
                augd    #AUGVD
                alts    idxs, #0
                wrlong  #LOD, hubd2
                wrlong  idxs, ptra[H_IDXS]
```

## Status {#sec-e2-status}

| Field | Content |
|---|---|
| Erratum | E2 |
| Published by Parallax | Yes, *P2 Documentation*, KNOWN BUGS |
| Found by | Parallax |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes — 2026-09-24, rule at each use: a register `S` on the `ALTx` (run with `ALTD`) |
| Affects | an `ALTx` with an immediate `#S` between `AUGS` and its target; tested with `ALTD` and `ALTR` |
| Test program | `e2-altx-takes-pending-augs-test.spin2` |


# Erratum E3: GETCT Returns a Stale Upper Long {#ch-e3}

::: caution
**Expected:** `GETCT WC` returns the upper 32 bits of the P2's one 64-bit free-running counter, whichever cog executes it.

**Actual:** in a cog of cogs 4-7 started after that group of four cogs has had no running cog at a wrap of the lower long (the first wrap comes 2^32^ clocks after reset), `GETCT WC` returns an upper long that is behind by one for each wrap missed.

**Workaround:** a cog of 4-7 must be running at every wrap of the lower long, from the first wrap on; see *A proven workaround*.
:::

This erratum affects a program that takes a 64-bit time with `GETCT WC` in a cog of cogs 4-7 and starts its first cog there more than 2^32^ clocks after reset, 21.47 s at 200 MHz. It affects in the same way a program that stops every cog of 4-7 and starts one there again after a wrap has passed. Plain `GETCT`, which reads the lower long, is not affected.

## What the P2 is documented to do {#sec-e3-documented}

The P2 Documentation (Parallax) describes one counter. Its overview of the chip lists, among what the hub provides the cogs:

> 64-bit free-running counter which increments every clock, cleared on reset

Its list of the improvements made to the chip states how a cog reads the upper half of that counter:

> System counter extended to 64 bits. GETCT WC retrieves upper 32-bits.

and its section EVENTS names the lower half:

> Event 1 = CT passed CT1 (CT is the lower 32-bits of the free-running 64-bit global counter)

The documentation does not qualify the value `GETCT WC` returns by cog number, or by which other cogs are running. The KNOWN BUGS section of the P2 Documentation does not list this behaviour.

## What the P2 does {#sec-e3-actual}

The eight cogs form two groups of four: cogs 0-3 and cogs 4-7. `GETCT` does not read the counter itself; each group reads its own copy of the counter's two longs, and the two halves of that copy behave differently.

- **The lower long is current.** In every pair the test took, including every pair in which the upper long was stale, the lower long a sampling cog read with plain `GETCT` lay between cog 0's own lower-long reads taken just before and just after it.
- **The upper long advances at a wrap of the lower long only while at least one cog of the group is running.** A group with no running cog at a wrap keeps its previous upper long.

Measured on cog 4, in the cogs 4-7 group, against cog 0 and cog 1 in the cogs 0-3 group:

- A cog started in a group that missed wraps reads an upper long behind cog 0's by the number of wraps missed. Cog 4, first started after its group had missed one wrap, read 1 behind; started again after its group had missed two more, it read 2 behind.
- Starting a cog does not bring its group's upper long up to date. The reading taken just after the start was already behind, and a reading late in the same 2^32^-clock span was behind by the same amount.
- The first wrap the group runs through restores the correct value in one step. Cog 4, 1 behind, ran through the next wrap and then read the same upper long as cog 0.
- A group whose only running cog stops is exposed again. Cog 4 was stopped after it had caught up; its group then missed two wraps with no cog running, and cog 4, started again, read 2 behind.

At reset only cog 0 runs, so the cogs 4-7 group has no running cog until the program starts one, and its upper long stays at zero through every wrap until then. The first wrap comes 2^32^ clocks after reset: 21.47 s at 200 MHz.

The defect was confirmed at 200 MHz, for one and for two missed wraps. The test sampled cog 1 and cog 4; the other cogs of each group were not sampled separately, and the cogs 0-3 group was not tested with every one of its cogs stopped.

## What your program sees {#sec-e3-sees}

In a cog of a group that missed wraps, `GETCT WC` followed by `GETCT` gives your program a 64-bit time that is short by 2^32^ clocks for each wrap missed. In one pair of the test, cog 0 read its own counter immediately before and immediately after cog 4 read:

| Read by | Upper long (`GETCT WC`) | Lower long (`GETCT`) |
|---|---|---|
| cog 0, before | `$0000_0001` | `$1020_DB39` |
| cog 4 | `$0000_0000` | `$1020_DB59` |
| cog 0, after | `$0000_0001` | `$1020_DBA1` |

The three lower longs are in order; the upper long is one behind, a gap of 2^32^ clocks, which is 21.47 s at 200 MHz.

In your program this shows up in two ways:

- A 64-bit time stamp you take in the stale cog and one you take in a cog of an up-to-date group disagree by 2^32^ clocks for each wrap missed.
- The stale cog's upper long advances by more than one at the next wrap it runs through, as its group's copy catches up. Cog 4 read `$0000_0000_$E013_C141` late in one span and `$0000_0002_$1001_4D69` early in the next: its upper long went from 0 to 2 across one wrap. A 64-bit interval that cog times across that wrap includes 2^32^ clocks that did not pass, one for the wrap its group had missed.

What does not go wrong:

- Plain `GETCT` returned a current lower long in every pair of every reading, in both groups.
- A cog of a group that had a running cog at every wrap read the same upper long as cog 0: cog 1 in every reading of both runs, and cog 4 throughout the run in which it ran from the start of the program.
- The stale value is steady. All ten pairs of each reading agreed, early and late in the span.
- Before the first wrap the correct upper long is zero, and a group's copy starts from zero at reset, so a program that has run for fewer than 2^32^ clocks since reset is not exposed.
- Only `GETCT` was exercised. The counter events, which the documentation defines on the lower long, were not tested.

## A proven workaround {#sec-e3-workaround}

**What any workaround must do:** a cog of 4-7 must be running at every wrap of the lower long, from the first wrap on, so that the cogs 4-7 group's copy of the upper long advances with the counter.

**One way, proven on P2 hardware:** a keeper cog, started by the first line of `main()` and never stopped.

```spin2
CON ' ---- E3 Workaround: Keeper Cog ----
  KEEPER_COG = 7                ' a cog of 4-7 the program never uses

DAT ' ---- E3 Workaround: Keeper Code ----
                org
keeper          jmp     #keeper         ' loop forever; never stop this cog

PUB main()
'' Start the keeper before anything else, then run the program.
''

  coginit(KEEPER_COG, @keeper, 0)       ' first line: before the first wrap
```

Started by the first line of `main()` and never stopped, the keeper keeps a cog of 4-7 running through every wrap of the lower long, so a cog your program starts in 4-7 at any later time reads the same upper long as cog 0: this is a one-time startup workaround.

The block was confirmed on silicon on 2026-09-26, on a P2 board at 200 MHz, run once: with the keeper running, cogs 5 and 6 started after one wrap and cogs 4 and 5 started after two each read the same upper long as cog 0 in all ten pairs of their readings, and with the keeper stopped, cog 6 read one behind.

**Where it goes.** Put the block at the top of your top-level object, ahead of every other `PUB` method: Spin2 runs the first `PUB` method of the top-level object at start, so this `main()` runs first. Your own `main()` body follows the `coginit` line. If your object already has a `main()`, move its body there and remove its old `PUB main()` line. In the test program, the line that follows is the call that runs the rest of the test.

`KEEPER_COG` names the keeper's cog. It must be a cog of 4-7 that nothing else in your program starts or stops.

**Other ways that meet the condition.** The condition asks for a running cog in 4-7 at every wrap, not for a keeper. A cog your program already starts in 4-7 before the first wrap and never stops meets it as well, and then no keeper is needed. Run B, under *How it was proven on P2 hardware*, is the evidence for that arrangement: cog 4, started at the beginning of that program while the lower long read `$00DB_96FF` and kept running, read the same upper long as cog 0 before the first wrap and after each of the first two. In Run B the cog kept running was the cog that read the counter; in the workaround's test program a separate cog, the keeper, was kept running while the cogs that read the counter started and stopped. Both arrangements met the condition, and both read current. The cogs tested were executing code at every wrap: a polling loop in Run B, a jump to itself for the keeper.

**The cost.** The keeper takes one cog for the life of the program: it holds cog 7, and seven cogs remain for your program. A program that already needs all eight cogs cannot add the keeper, but meets the condition if one of its own cogs of 4-7 is running from before the first wrap and is never stopped. The keeper executes a jump to itself and nothing else.

**What it covers.** The block covers cogs 4-7 only. Cogs 0-3 are kept current by cog 0, which runs your `main()` from reset, for as long as it or another cog of 0-3 keeps running; the cogs 0-3 group was not tested with every one of its cogs stopped.

**The limits of the proof:**

- The keeper was tested only as the loop above, a jump to itself. Whether a cog held in a wait instruction such as `WAITX` at a wrap keeps its group current was not tested, so do not replace the loop with a wait; the same holds for a cog of your own that you rely on in place of the keeper.
- Only cog 7 was tested as the keeper. The cogs of 4-7 that read the counter after a wrap were cogs 4, 5 and 6, each started after one or two wraps and stopped again after its reading.
- The keeper ran alone in cogs 4-7 through two wraps. The test program then stopped it, as a positive control.
- The test ran once, at 200 MHz, with the program downloaded to RAM with a reset.

## Why it happens {#sec-e3-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

The P2 has one 64-bit counter, but a cog does not read it directly. Each group of four cogs holds its own copy of the counter's two longs, and `GETCT` reads the group's copy: the lower long without `WC`, the upper long with it. The group refreshes the two halves of its copy on different schedules.

The lower half is refreshed on every clock on which any cog of the group is running. If the group has been idle, the first clock on which one of its cogs runs brings the lower half up to date, so a newly started cog reads a current lower long.

The upper half is refreshed only once in 2^32^ clocks, at the wrap of the lower long, and only if a cog of the group is running at that moment. Nothing else refreshes it: not a cog start, and not the clocks that pass between wraps. A group with no running cog at a wrap keeps its previous upper long. At the next wrap it runs through, it takes the counter's upper long as it is then, which is why the error closes in a single step rather than shrinking by one.

The counter and both groups' copies start from zero at reset, and at reset only cog 0 runs. The cogs 0-3 group therefore refreshes at every wrap from the start, for as long as cog 0 runs; the cogs 4-7 group refreshes at none until a program starts a cog there. A keeper cog in 4-7 that runs from before the first wrap gives that group a running cog at every wrap, so its upper long advances with the counter's, and a cog started there later reads it current.

Running here means the state a cog is in between its start and its stop, the state `COGCHK` reports. By the study's reading, what a running cog is executing does not enter into it. The tests kept their cogs in a polling loop or, for the keeper, a jump to itself, and did not try a cog held in a wait instruction such as `WAITX`.

## How it was proven on P2 hardware {#sec-e3-proof}

Two programs, Run A and Run B, confirmed the erratum. Each was downloaded to RAM with a chip reset and run on a bare P2 board at 200 MHz, with the debugger confined to cog 0. Each was run twice, from two builds: as first written, and with its comments and layout conformed to house style and its measuring code unchanged. Every D value and every verdict matched between the two builds. A third program, run once, confirmed the workaround; it is described after them.

**Arrangement.** Cog 0 is the reference. Cog 1, in the cogs 0-3 group, and cog 4, in the cogs 4-7 group, run the same sampler: on each new request from cog 0 it executes `GETCT WC` then `GETCT`, writes both longs to hub RAM, then writes an acknowledgment. One **pair** is taken as follows: cog 0 reads its own counter (`GETCT WC`, `GETCT`), writes a request, waits for the acknowledgment, reads the sampler's two longs, and reads its own counter again. The sampler's reads therefore fall between cog 0's two reads.

- A pair counts only if cog 0's two upper longs agree and all three lower longs lie between `$1000_0000` and `$F000_0000`, clear of any wrap.
- **D** is cog 0's upper long minus the sampler's upper long.
- Each pair also checks that the sampler's lower long lies strictly between cog 0's two lower longs, compared unsigned.
- A reading is ten counted pairs, and all ten must give the same D.

**Controls.** Any failure stops the run with no verdict.

- Cog 1, running from the start of the program, must give D = 0 in every reading.
- Cog 0's own upper long must equal the number of wraps of its lower long that cog 0 has watched since reset, checked on every poll.
- The set of running cogs, polled throughout every wait, must be exactly the cogs the program started; in Run A, no cog of 4-7 may run before cog 4 is started.
- At start the upper long must read 0 and only cog 0 may be running, which shows the download reset the part.
- Every request must be answered within 100 ms.

The expected D of every reading, for the defect present and for it absent, was written into each program before the run.

**Run A** holds cogs 4-7 idle until cog 0's upper long reads 1, starts cog 4, and reads it just after the start and again late in the same span. Cog 4 then runs through the next wrap and is read again. Cog 4 is then stopped, its group misses two wraps with no cog running, and cog 4 is started again and read just after the restart and late in the span. **Run B** starts cog 4 at the beginning of the program, beside cog 1, and reads it before the first wrap, early and late after it, and after the second wrap.

Wrap *n* below is the wrap after which cog 0's upper long reads *n*. An early reading is taken with the lower long past `$1000_0000`, a late one past `$E000_0000`.

| Run | Cog 0 upper | Reading | Cogs 4-7 before the reading | Cog 4 D | Cog 1 D |
|---|---|---|---|---|---|
| A | 0 | early | no cog running | not read | 0 |
| A | 1 | just after cog 4 started | no cog running at wrap 1 | **1** | 0 |
| A | 1 | late | cog 4 running since after wrap 1 | **1** | 0 |
| A | 2 | early | cog 4 ran through wrap 2 | 0 | 0 |
| A | 4 | just after cog 4 restarted | cog 4 stopped; no cog running at wraps 3 and 4 | **2** | 0 |
| A | 4 | late | cog 4 running since after wrap 4 | **2** | 0 |
| B | 0 | early | cog 4 running since program start | 0 | 0 |
| B | 1 | early | cog 4 ran through wrap 1 | 0 | 0 |
| B | 1 | late | cog 4 ran through wrap 1 | 0 | 0 |
| B | 2 | early | cog 4 ran through wrap 2 | 0 | 0 |

In every reading of both runs all ten pairs agreed on D, and the lower-long check held in every pair. Each program's verdict line read `CONFIRMED`, in both builds.

**The workaround.** The workaround's test program decided the block printed under *A proven workaround*. It carries that block byte for byte, with the same sampler, pair protocol, D and pair rules as Run A and Run B, at 200 MHz, with the debugger confined to cog 0. The keeper starts in cog 7 at the first line of `main()`. Cog 1 samples the cogs 0-3 group from start to end. The program's own cogs of 4-7 are cogs 4, 5 and 6: each is started as a sampler just before one reading and stopped again just after it, so every cog of 4-7 that reads the counter after a wrap was started after one or two wraps through which the keeper ran alone in that group. Every reading of cogs 4-7 is paired with a reading of cog 1.

| Cog 0 upper | Reading | Sampler | Cogs 4-7 before the reading | D written in advance | Sampler D | Cog 1 D |
|---|---|---|---|---|---|---|
| 0 | early | cog 4 | the keeper, since the first line of `main()` | 0 (control) | 0 | 0 |
| 1 | early | cog 5 | the keeper alone through wrap 1 | 0 with the keeper; 1 without | 0 | 0 |
| 1 | late | cog 6 | the keeper alone through wrap 1 | 0 with the keeper; 1 without | 0 | 0 |
| 2 | early | cog 4 | the keeper alone through wraps 1 and 2 | 0 with the keeper; 1 or 2 without | 0 | 0 |
| 2 | late | cog 5 | the keeper alone through wraps 1 and 2 | 0 with the keeper; 1 or 2 without | 0 | 0 |
| 3 | early | cog 6 | the keeper stopped after the reading above; no cog running at wrap 3 | 1 (positive control) | **1** | 0 |

In every reading all ten pairs agreed on D, and the lower-long check held in every pair.

The controls of Run A and Run B apply, with these differences. At start the running cogs must be cog 0 and the keeper only. The keeper must be seen running on every poll up to the positive control, and stopped after it. The reading at upper long 0 must give D = 0. The positive control must give D = 1: it shows that the program, on this part and in this run, sees the erratum when the keeper is absent, so a D of 0 with the keeper running cannot come from a test that is blind to it. Cog 6 reads both with the keeper running and, in the positive control, with it stopped: the same cog and the same code, with only the keeper changed.

The verdict rule was set before the run. The workaround is confirmed if the four readings taken after a wrap with the keeper running all give D = 0, with all ten pairs of each agreeing and the lower-long check holding in every pair. A reading whose ten pairs agree on a D other than 0, or a failed lower-long check, refutes it. A reading whose pairs disagree, or that gets too few valid pairs, leaves it inconclusive. A control failure gives no verdict.

**Result.** The workaround's test program ran once, on 2026-09-26, on a P2 board at 200 MHz, downloaded to RAM with a reset. At start the upper long read 0 and the running cogs were cog 0 and the keeper in cog 7. Every control passed, and no `RIG FAIL` line was printed. The running-cog set showed the keeper on every poll until it was stopped, with cog 0's counter at `$0000_0002_$E088_2186`, and did not show it on any poll after. With the keeper running, the four readings taken after a wrap gave D = 0. In the positive control, with the keeper stopped and wrap 3 missed, cog 6 read an upper long of `$0000_0002` beside cog 0's `$0000_0003`: D = 1, the erratum as in Run A. The verdict line read `CONFIRMED`.

## The test program {#sec-e3-program}

The erratum's two files are `e3-getct-stale-upper-long-runA.spin2` (Run A) and `e3-getct-stale-upper-long-runB.spin2` (Run B). They share the sampler, the pair protocol and the controls, and differ only in when cog 4 starts and which readings are taken. The workaround's test program is `e3-workaround-keeper-cog-test.spin2`.

The sampler is started explicitly in cog 1 and in cog 4 (`COGINIT #1` and `COGINIT #4`), with its hub mailbox address in `PTRA`. On each new request number it reads the counter and writes both longs:

```pasm2
sampler         mov     s_last, #0
s_loop          rdlong  s_req, ptra
                cmp     s_req, s_last   wz
        if_z    jmp     #s_loop
                mov     s_last, s_req
                getct   s_hi            wc      ' this group's UPPER copy
                getct   s_lo                    ' this group's LOWER copy
                wrlong  s_hi, ptra[MB_HI_IDX]
                wrlong  s_lo, ptra[MB_LO_IDX]
```

It then writes the request number back as its acknowledgment and returns to `s_loop`. Cog 0's side of a pair, in the method `take_pair`, is inline PASM2 that executes `GETCT WC` and `GETCT` before writing the request, and again after seeing the acknowledgment and reading the sampler's two longs. From those six longs each reading computes D and the lower-long check, and every pair is printed.

Run A's defect step: cogs 4-7 stay idle while cog 0 waits for its upper long to read 1, with the running-cog set polled throughout the wait; then cog 4 is started and read, with cog 1 read beside it:

```spin2
  ' ---- hazard: group 1 idle across wrap 0->1 --------------------------
  if bHalted == FALSE
    debug("--- waiting for CT hi=1 with cogs 4-7 idle (~21 s) ---")
    wait_until(HI_A1, LOWIN, M_C1)
  if bHalted == FALSE
    start_cog4(@mailboxGroup1)
    waitms(COG_SETTLE_MS)
    expect_mask(M_C1C4)
  if bHalted == FALSE
    debug("--- cog 4 started (first group-1 cog since reset) ---")
    reading(R_A1A, string("A1a cog4 hi=1"), @mailboxGroup1)
    reading(R_C1A, string("C1a cog1 hi=1"), @mailboxControl)
```

Later in the same file, `cogstop(SMP_COG)` at upper long 2 and a second `start_cog4` at upper long 4 take the two-missed-wrap readings.

Run B changes the arrangement in one place: both samplers start at the beginning of the program.

```spin2
  ' ---- both samplers from program start: cog 1 (group 0), cog 4 (group 1)
  if status == SUCCESS
    start_cog1(@mailboxControl)
    start_cog4(@mailboxGroup1)
    waitms(COG_SETTLE_MS)
    status := expect_mask(M_C1C4)
```

The workaround's test program carries the block of *A proven workaround* unchanged, between the comments `BEGIN DROP-IN` and `END DROP-IN`; its `main()` goes on to call the rest of the test. It uses the same sampler instructions and the same pair protocol as Run A and Run B. Every reading of cogs 4-7 goes through the method `arm`, which starts the sampler in the named cog, checks the running-cog set, takes the reading, stops the cog, and checks the set again:

```spin2
  longfill(@mailboxGroup1, 0, MB_LONGS)
  coginit(smpCog, @sampler, @mailboxGroup1)
  waitms(COG_SETTLE_MS)
  expect_mask(baseMask | (1 << smpCog))
  if bHalted == FALSE
    reading(slotIdx, pLabel, @mailboxGroup1)
    cogstop(smpCog)
    waitms(COG_SETTLE_MS)
    expect_mask(baseMask)
```

The readings run in the order of the table under *How it was proven on P2 hardware*. After the late reading at upper long 2, `cogstop(KEEPER_COG)` stops the keeper, and the positive control is read in cog 6 after wrap 3.

Each file prints every pair raw, a summary line per reading, and a one-line verdict. All three are compiled with `pnut-ts` 1.55.8 with DEBUG enabled (`-d`) and downloaded to RAM; the download must reset the part, since each program checks that the counter starts from zero. Run A ends about 105 s after reset, Run B about 44 s after reset, and the workaround's test program about 67 s after reset.

## Status {#sec-e3-status}

| Field | Content |
|---|---|
| Erratum | E3 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; a one-time startup workaround: a keeper cog in cog 7 started by the first line of `main()` |
| Affects | `GETCT WC` in a cog of a four-cog group that had no running cog at one or more wraps of the lower long (measured on cogs 4-7); plain `GETCT` is not affected |
| Test program | `e3-getct-stale-upper-long-runA.spin2`, `e3-getct-stale-upper-long-runB.spin2`, `e3-workaround-keeper-cog-test.spin2` |


# Erratum E4: GETXACC Clears Only During a Goertzel Burst {#ch-e4}

::: caution
**Expected:** `GETXACC` reads the streamer's Goertzel cosine and sine accumulators and clears them (P2 Documentation, *STREAMER* and *DDS/Goertzel*).

**Actual:** The clear acts only while a DDS/Goertzel command is running; with the streamer idle, `GETXACC` clears nothing, and each burst adds to what earlier bursts left.

**Workaround:** Take each burst's sums as the difference of two readings taken with the streamer idle, one before the burst and one after it; see *A proven workaround*.
:::

The erratum affects PASM code that runs DDS/Goertzel bursts one at a time, with the streamer idle between them, and relies on `GETXACC` to clear the accumulators: a reading taken after each burst, or a `GETXACC` issued before an `XINIT` to start from zero. A `GETXACC` issued while a Goertzel command is running clears as documented. The erratum was predicted by the clean-room design study and confirmed on silicon; Parallax does not list it.

## What the P2 is documented to do {#sec-e4-documented}

The P2 Documentation states the clear in its streamer instruction table and again in its description of the DDS/Goertzel mode. The instruction table's entry for `GETXACC` reads:

> Get Goertzel X into D and Y into next S, clear X and Y

The DDS/Goertzel mode description reads:

> After some number of complete NCO cycles, both accumulators can be simultaneously captured into holding registers and cleared using the GETXACC instruction. GETXACC writes the captured cosine accumulation into D and places the captured sine accumulation into the next instruction's S value. Subsequent GETXACC instructions will return the same values until a new streamer command executes.

The SINC1/SINC2 table that follows that description carries the column heading:

> Accumulations (SIN_ACC/COS_ACC are read and cleared by GETXACC)

None of the three places makes the clear depend on the streamer's mode or on whether a streamer command is running.

## What the P2 does {#sec-e4-actual}

In this erratum a *Goertzel burst* is one DDS/Goertzel streamer command for the clocks it runs, and a *term* is the product the streamer adds to each accumulator on each of those clocks.

- **Streamer idle.** `GETXACC` returns the current value of the accumulators and leaves them as they were. Repeated reads return the same value, bit for bit.
- **Streamer running another mode.** One other mode was tested: the immediate-to-pins mode, one pin wide, with its output disabled, started by `XINIT`. A `GETXACC` issued as the next instruction after that `XINIT`, and another issued 100 clocks later with the command still running, both returned the value from before the `XINIT` and cleared nothing.
- **A new Goertzel burst.** The burst adds its terms to the value the accumulators already hold. Starting a streamer command does not reset them.
- **During a Goertzel burst.** The clear acts. `GETXACC` returns everything accumulated so far, including what earlier bursts left, and the accumulation continues from the clear. The read plus the next read hold exactly what the same burst gives when it is not read: no term is lost and none is counted twice.

The sine accumulator behaved as the cosine accumulator did in every case measured.

The clear during a running command also held in continuous streams. In the SINC1 streams of the test program `e5-goertzel-sinc2-iteration-count-test.spin2` (a check of the P2 Documentation's SINC2 constraint, run on 2026-09-25), commands were chained with `XCONT` and one `GETXACC` was issued per command; every reading analysed (all but the first three of each stream) equalled the per-clock term times the number of clocks since the previous reading.

## What your program sees {#sec-e4-sees}

If your program issues one `GETXACC` after each burst and treats the reading as that burst's result, it gets a running total instead: each reading holds the burst plus everything accumulated since the last clear. In one repetition of the test program, the reading before a 256-clock burst was 14,823 and the reading after it was 30,378; the burst itself contributed 15,555.

A `GETXACC` issued before an `XINIT` in order to zero the accumulators returns the running total and zeroes nothing.

A `GETXACC` inside a Goertzel burst returns the leftover from earlier bursts together with the part of the burst run so far. In the test program, a read 29 terms into a burst that started from 17,080 returned 18,849.

What does not go wrong: the accumulation itself is exact. Every difference the test program measured was a whole multiple of the per-clock term, the same burst gave the same difference from every starting value, and a read inside a burst split it into two parts that sum exactly to the unread burst. Consecutive idle reads return the same value, as the documentation says they do.

The difference of two idle readings is still one term short of your burst: the burst's last term is held back until the next Goertzel burst. That is Erratum E5, and the workaround below steps around both.

## A proven workaround {#sec-e4-workaround}

**What any workaround must do:** take each burst's sums as the difference of two readings taken with the streamer idle, one before the burst and one after it. An idle `GETXACC` clears nothing, so the difference holds your burst whatever the accumulators held before it.

**One way, proven on P2 hardware:** the `burst_sums` helper routine, which also steps around Erratum E5.

```pasm2
{ Runs one DDS/Goertzel burst (SINC1 only) and returns its exact
  sums. Put your XINIT D and S in burst_mode and burst_sel, then
  CALL #burst_sums with the streamer idle. It leaves the burst's
  cosine sum in cos_sum and its sine sum in sin_sum.
}
CON
  ZERO_COUNT = 4    ' each zero burst: a count of 4
  INPUT_NIB  = 3    ' S nibble 3 = S[15:12], the summed inputs
DAT
burst_sums  mov     zero_mode, burst_mode       ' zero burst: your mode,
            setword zero_mode, #ZERO_COUNT, #0  '   count 4,
            mov     zero_sel, burst_sel         '   your S with every
            setnib  zero_sel, #0, #INPUT_NIB    '   input off: S[15:12]=0
            xinit   zero_mode, zero_sel         ' adds any held term
            waitxfi
            getxacc cos_base                    ' idle read: no clear
            mov     sin_base, 0-0
            xinit   burst_mode, burst_sel       ' your burst
            waitxfi
            xinit   zero_mode, zero_sel         ' adds its last term
            waitxfi
            getxacc cos_sum                     ' idle read again
            mov     sin_sum, 0-0
            sub     cos_sum, cos_base           ' cosine sum, all N terms
            sub     sin_sum, sin_base           ' sine sum, all N terms
            ret

burst_mode  long    $F007_0100                  ' your D (count 256 here)
burst_sel   long    $0008_80A5                  ' your S
zero_mode   long    0                           ' built: the zero burst's D
zero_sel    long    0                           ' built: the zero burst's S
cos_base    long    0                           ' before reading, cosine
sin_base    long    0                           ' before reading, sine
cos_sum     long    0                           ' result: cosine sum
sin_sum     long    0                           ' result: sine sum
```

Each call leaves in `cos_sum` and `sin_sum` the sums of your burst alone, all N of its terms, whatever the accumulators held before the call: a *helper routine*.

On silicon, this block returned exactly N terms on both sums in all 60 calls of its test program, for bursts of 1 to 1001 clocks at both input levels, including 6 calls made while an earlier burst's term was still held; see *How it was proven on P2 hardware*.

To use it, put your `XINIT` D operand (the Goertzel mode word with your count) in `burst_mode` and your S operand in `burst_sel`, set `SETXFRQ` as your program already does, and `CALL #burst_sums` with the streamer idle. The values printed in `burst_mode` and `burst_sel` are the test program's: SINC1, no DAC output, input pins P0 to P3, a count of 256, with P3 inverted and summed and a lookup offset of `$0A5`.

The routine takes its two readings with the streamer idle, where `GETXACC` clears nothing, so their difference is your burst whatever came before it. The zero bursts deal with Erratum E5: each is your mode word with a count of `ZERO_COUNT` (4) and `S` nibble `INPUT_NIB` ([15:12]) clear, so every term it forms is zero. The first delivers any term an earlier burst left held, so the before reading is complete; the second delivers your burst's last term before the after reading.

**Other ways that meet the condition.** Any code that takes the two idle readings and subtracts meets this erratum's condition without the routine. The erratum test's run A did exactly that: it read 15,555 for a 256-clock burst in all eight repetitions, from five different starting values (see *How it was proven on P2 hardware*). That difference is 255 terms, not 256: it steps around this erratum but not Erratum E5, whose held last term only a later Goertzel burst delivers. The zero bursts in `burst_sums` are what add that term.

**Cost.** Each call runs two zero bursts of 4 NCO rollovers each, at your `SETXFRQ` rate, besides your burst, and the cog waits in `WAITXFI` until each command has finished. The routine is 17 instructions, and 8 longs of cog RAM hold its operands and results.

**Limits.**

- **SINC1 only.** In SINC2 mode the zero burst has not been tested as a flush, and the routine is not recommended there; *A proven workaround* of Erratum E5 notes the P2 Documentation's separate SINC2 constraint.
- **One burst at a time, from an idle streamer.** The routine starts every command with `XINIT`, which issues it at once, so it does not fit a continuous stream of commands chained with `XCONT`. A `GETXACC` inside a running Goertzel command clears as documented.
- **Conditions of the test.** The workaround's test program ran the routine once, from cog RAM on a P2 board at 200 MHz, with an NCO frequency of `$8000_0000`, one input pin, no DAC output, and bursts of 1 to 1001 clocks. With DAC channels enabled, the zero bursts are DDS/Goertzel commands like any other and, by the P2 Documentation, output on each of their clocks; that case, more than one input pin, other NCO frequencies, hub execution, and accumulator values near the 32-bit limit were not tested.

## Why it happens {#sec-e4-why}

The clean-room design study traces the behaviour to how the accumulators are updated. Each accumulator is rewritten only on the clocks of a running DDS/Goertzel command; on every other clock it holds its value, whatever instruction the cog executes. The clear in `GETXACC` is not a separate action on the accumulator. It is folded into that same per-clock update: on the clock the clear arrives, the update starts the accumulator over instead of adding to its old value. When no update happens, because the streamer is idle or running a different mode, the clear has nothing to act through, and the accumulator keeps its value.

The read does not depend on the update. `GETXACC` returns the accumulator's current value, which is why idle reads repeat exactly and why a read inside a burst returns the running sum. When the clear does act, the accumulator starts over from the one term that has been formed but not yet added (Erratum E5), and that term appears in the next reading. That is why a read inside a burst and the read after it partition the burst exactly.

By the study's reading, every mode other than DDS/Goertzel behaves as the idle streamer does. One such mode was tested.

## How it was proven on P2 hardware {#sec-e4-proof}

The test program runs on a P2 board at 200 MHz with nothing connected to pins P0 to P7. One cog, started from a `DAT` block, does all streamer work and issues every `GETXACC`; the debugger is confined to cog 0, which only waits for the results and prints them. The measuring cog drives P3 low as a plain output with its smart pin off, so the streamer's input bit for P3 holds a fixed level.

**Construction.** All 512 LUT longs hold `$173D_0000`, and the NCO frequency is `$8000_0000`. Each Goertzel burst is an `XINIT` whose `D` is `$F007_0000` plus a count (SINC1, no DAC output, input pins P0 to P3) and whose `S` is `$0008_80A5` (P3 inverted and summed, the other three pins ignored). With P3 low, each active clock adds 61 to the cosine accumulator and 23 to the sine accumulator. Every phase starts from the same preamble: an 8-clock Goertzel burst, a 4-clock burst whose terms are all zero (`S` of `$0008_00A5`), and an idle `GETXACC` whose value, B, must be nonzero, so that a clear which wrongly acted would show.

**Controls**, all passed in both runs: the 512 LUT longs read back unchanged; P3 read at its driven level at every check; `POLLXFI` reported the streamer finished after every wait and still running at every read meant to fall inside a command; and a calibration pair of 64-clock bursts moved the cosine accumulator by +3,843 with P3 low and by -3,843 with P3 high (63 × 61 each way), which shows the term follows the pin and is a whole multiple of 61.

**Idle and non-Goertzel reads.** In each of eight repetitions, after the preamble: a read with the streamer idle; an `XINIT` of `$4000_0400` (immediate-to-pins, one pin, output disabled, count `$0400`) followed at once by a read; a read 100 clocks later, with that command confirmed still running; and a read after it ended. Each of those reads, and the idle read taken before each calibration burst and before each burst of the two runs below, was compared with its preamble's B. All 50 reads equalled B bit for bit, and none returned zero. In the first repetition, B and the four reads were all 488.

**Reads inside a burst.** Each repetition ran two 256-clock bursts, each after its own preamble. Run A: an idle read P, the burst with no read inside it, a 4,000-clock wait, and a read RA. Run B: the same, with one `GETXACC` issued a fixed `WAITX` delay after the `XINIT` (read R1), and after the wait a read R2. The delays were 30 in the first four repetitions, then 62, 94, 126 and 190. The outcomes were written into the program before the run: run B's R1 + R2 - P equal to run A's RA - P confirms the partition; a result 61 short would mean the clear lost a term; 61 over, that a term was counted twice; a difference equal to R1, that the clear did not act during the burst.

Results for the first repetition:

| Quantity | Value | Terms of 61 |
|---|---|---|
| Run A: RA - P (16,531 - 976) | 15,555 | 255 |
| Run B: R1 - P (18,849 - 17,080) | 1,769 | 29 |
| Run B: R2 | 13,786 | 226 |
| Run B: R1 + R2 - P | 15,555 | 29 + 226 = 255 |

In all eight repetitions RA - P was 15,555 and R1 + R2 - P equalled it exactly, while the read point moved from term 29 to term 189, one term behind the `WAITX` operand each time. R2 was 13,786 in each of the first four repetitions, although run B started from 17,080 in the first and from 30,927 in the next three: the read inside the burst discarded everything before it. The sine accumulator, recorded for information, moved on no idle read and split the same way (5,865 in both runs of every repetition). That a 256-clock burst gives 255 terms is Erratum E5.

Run A is also the before-and-after difference the workaround is built on: it read 15,555 in all eight repetitions, from starting values of 976, 14,823, 12,871, 10,919 and 8,967. The largest value any read returned was 36,600.

The program was run twice on 2026-09-24, from two builds with identical measuring code; every value printed was the same in both runs.

### The workaround's test {#sec-e4-workaround-proof}

The workaround ran in its own test program, on the same construction: the LUT, the NCO frequency, the mode word and the `S` operand above, with P3 driven by the measuring cog, low for the first half of the run and high for the second. The printed block is the routine the test program calls, byte for byte, and the program checks before it starts that `burst_mode` carries the printed mode bits and `burst_sel` the printed `S`. Every wait on a burst is `WAITXFI`, as in the routine.

At each P3 level the program runs three records, each of four parts:

- **Calibration.** The per-clock term C, measured without assuming either erratum, as the difference between a 65-clock and a 64-clock burst, each read from a flushed start to a flushed end.
- **The documented use, without the workaround.** A `GETXACC` "to clear", a 64-clock burst and a reading; a second `GETXACC` "to clear", a 65-clock burst right after and a reading; a zero burst alone and a reading; then a 7-clock burst read with no zero burst, which leaves its last term held for the next part. This part must show both errata in the same run: the second "clear" reading equals the first reading (Erratum E4), and the bursts read 63 × C, 65 × C, C and 6 × C (Erratum E5). If it does not, the program prints `RIG FAIL` and no verdict.
- **The workaround.** Ten consecutive calls of `burst_sums`, with N = 1, 2, 3, 4, 7, 64, 65, 255, 256 and 1001, set by the program with `SETWORD` in `burst_mode`, the first call starting with the 7-clock burst's term still held. After each call the program waits 1,000 clocks and takes its own idle reading.
- **Pin checks.** P3 at its driven level before and after the record.

The outcome was written into the program before the run: every one of the 60 calls returns exactly N × C on the cosine and on the sine sum; the before reading of each record's first call has gained exactly C (the held term the first zero burst delivered), and that of every other call nothing; and the program's own reading after each call equals the before reading plus the returned sum. A miss of exactly -C would mean the zero burst did not deliver the last term; +C, that an older term was counted.

**The results.** Every control passed. The printed words read `$F007_0100` and `$0008_80A5`; the routine built its zero-burst words as `$F007_0004` and `$0008_00A5`; the 512 LUT longs read back unchanged; and P3 read at its driven level before and after every record. The calibration gave C = 61 on the cosine sum and 23 on the sine sum in all three records at P3 low, and -61 and -23 in all three at P3 high.

The documented use, without the workaround, showed both errata in all 12 rows (6 records, cosine and sine): the second "clear" reading equalled the first, and the bursts read 63 × C, 65 × C, C and 6 × C. In the first record, on the cosine sum: P = 68,869, R1 = 72,712 (3,843, which is 63 × 61), the second "clear" 72,712, R2 = 76,677 (3,965, which is 65 × 61), the zero burst alone 76,738 (61), and the 7-clock burst 77,104 (366, which is 6 × 61).

All 60 calls of `burst_sums` returned exactly N × C on both sums. At P3 low, for N = 1, 2, 3, 4, 7, 64, 65, 255, 256 and 1001, the cosine sums were 61, 122, 183, 244, 427, 3,904, 3,965, 15,555, 15,616 and 61,061, and the sine sums 23, 46, 69, 92, 161, 1,472, 1,495, 5,865, 5,888 and 23,023; at P3 high, the same values negated. The 256-clock call returned 15,616 (256 × 61), where the difference alone, in the erratum test above, read 15,555 (255 × 61). Each record's first call found its before reading moved by exactly C from the reading after the 7-clock burst (77,165 against 77,104 in the first record); every later call's before reading equalled the program's own reading after the previous call; and every one of the program's own readings, 1,000 clocks after a call, equalled the call's before reading plus its returned sum. No call returned (N-1) × C or (N+1) × C. The largest accumulator value read was 412,909.

The test program was run once, on 2026-09-26, on a P2 board at 200 MHz. The values above are read from its raw lines, not from its verdict line.

## The test program {#sec-e4-program}

The test program is `e4-getxacc-clear-gating-test.spin2`. Its measuring code is a `DAT` block started by `COGINIT`; the Spin2 method `main` waits for it, prints every raw value, checks the controls, and prints one verdict for the idle and non-Goertzel reads and one for the reads inside a burst.

The streamer command words sit at the end of the measuring cog's code:

```pasm2
dch_            long    MODE_G | N_CHARGE
dzero_          long    MODE_G | N_ZERO
dcal_           long    MODE_G | N_CAL
drun_           long    MODE_G | N_RUN
dimm_           long    D_IMM
son_            long    S_ON
szero_          long    S_ZERO
simm_           long    0
lutv_           long    LUTVAL
frq_            long    FRQ
' run B's WAITX delay per rep, indexed by rep_: reps 0-3 read 30, reps 4-7
' read 62, 94, 126 and 190 (the mid-burst read point moves later)
dlytab          long    30, 30, 30, 30, 62, 94, 126, 190
```

`dch_` and `dzero_` are the preamble's 8-clock and zero-term bursts, `dcal_` the 64-clock calibration burst, `drun_` the 256-clock burst of runs A and B, and `dimm_` the non-Goertzel command. `dlytab` holds run B's eight `WAITX` delays.

The before-and-after pattern, as the calibration block runs it. The `call #xfi_end` checks with `POLLXFI` that the streamer has finished before the second read:

```pasm2
                call    #preamble
                getxacc p_
                mov     py_, 0-0
                xinit   dcal_, son_
                waitx   ##WAIT_IDLE
                mov     site_, #SITE_CAL_LO_END
                call    #xfi_end
                getxacc r_
                mov     ry_, 0-0
```

Run A is the same pattern with `drun_`. Run B's read inside the burst follows; the delay is loaded from `dlytab` before the preamble, so only the `WAITX` separates the `XINIT` from the `GETXACC`:

```pasm2
                call    #preamble
                getxacc p_
                mov     py_, 0-0
                xinit   drun_, son_
                waitx   dly_
                getxacc r1_                     ' R1: mid-burst
                mov     r1y_, 0-0
```

The non-Goertzel reads follow the same shape in the block marked `phase (i)`: an `XINIT` of `dimm_` with the next instruction a `GETXACC`, a `WAITX` of 100 clocks and a second `GETXACC`, then a `POLLXFI` check that the command is still running.

The workaround's test program is `e4-e5-workaround-read-sums-test.spin2`; Erratum E5 shares it. The printed routine sits between the comment lines `' ---- DROP-IN BEGIN ----` and `' ---- DROP-IN END ----`, a `CON` part for its two constants ahead of its `DAT` block. The program calls it the way a reader would, setting only the count:

```pasm2
wkr_arm         mov     widx_, #0
.call           alts    widx_, #wkrn_
                mov     nn_, 0-0                ' N for this call
                setword burst_mode, nn_, #0     ' the reader's count
                call    #burst_sums             ' THE DROP-IN
                waitx   ##WAIT_REREAD
                getxacc qx_                     ' Q: the rig's own idle read
                mov     qy_, 0-0
```

`wkrn_` holds the ten burst lengths, and `WAIT_REREAD` is 1,000 clocks. The program prints every raw reading, the controls, the uncorrected readings in units of the measured C, one line per call with its sums, and one `VERDICT:` line; it drives P3 and releases it at the end, so P3 must be free.

## Status {#sec-e4-status}

| Field | Content |
|---|---|
| Erratum | E4 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; helper routine |
| Affects | `GETXACC` with the streamer idle or in a non-Goertzel mode: it returns the Goertzel accumulators without clearing them. Measured with SINC1 bursts started by `XINIT`, one input pin |
| Test program | `e4-getxacc-clear-gating-test.spin2`; the workaround: `e4-e5-workaround-read-sums-test.spin2` |


# Erratum E5: The Goertzel Accumulators Trail by One Clock {#ch-e5}

::: caution
**Expected:** A `GETXACC` reading after a DDS/Goertzel burst of N clocks holds all N of the burst's terms (P2 Documentation, *DDS/Goertzel*).

**Actual:** It holds the first N-1; the last term is held back and added on the first clock of the next Goertzel burst.

**Workaround:** Deliver the burst's held last term to the accumulators before you read them (SINC1 mode); see *A proven workaround*.
:::

The erratum affects PASM code that runs DDS/Goertzel bursts and reads the accumulators with `GETXACC` after each one: every reading is short by the burst's last term, and the next burst's reading carries it. The erratum was predicted by the clean-room design study and confirmed on silicon.

## What the P2 is documented to do {#sec-e5-documented}

The P2 Documentation describes the DDS/Goertzel mode as working on every clock of the command:

> This mode is unique, in that it outputs and inputs on every clock in which the command is active.

It then states what becomes of each clock's lookup values:

> The 8-bit sine (byte 3) and cosine (byte 2) values from the lookup RAM will each be multiplied by the bitstream sum (an integer from -3 to +3) and then added into their respective 32-bit accumulators.

Its table of accumulation modes gives the SINC1 case (D[23] = `%0`) as `SIN_ACC += SIN_MUL` and `COS_ACC += COS_MUL`, where each `_MUL` is the bitstream sum times the lookup value. By that description, a command that is active for N clocks adds N terms to each accumulator, and a `GETXACC` issued after it returns all N.

The KNOWN BUGS section of the P2 Documentation does not list this behaviour.

## What the P2 does {#sec-e5-actual}

On each active clock of a Goertzel burst, each accumulator adds the term formed on the **previous** active clock, not the term formed on that clock. After a burst of N active clocks:

- the accumulator holds the burst's first N-1 terms, plus the last term of the previous Goertzel burst if one was still held when this burst began;
- the burst's last term is held in an internal register. `GETXACC` does not return it, and it does not change while the streamer is idle;
- the first active clock of the next Goertzel burst adds the held term to the accumulator, ahead of that burst's own terms.

Both accumulations behave this way: the cosine accumulation that `GETXACC` writes into D, and the sine accumulation it places into the next instruction's S. No term is lost; the last term of each burst arrives one burst late.

This was confirmed on silicon in SINC1 mode, with one input pin summed, for bursts of 64 and 65 clocks, each started by `XINIT` from an idle streamer and read with the streamer idle. The test ran no other streamer mode between bursts, so whether a command in another mode disturbs the held term is not established.

## What your program sees {#sec-e5-sees}

If your program runs a Goertzel burst of N clocks, waits for it to end and reads with `GETXACC`, you get a sum short by exactly the burst's last term. Reading again later does not recover it: in the test, a second reading 1000 clocks after the first had moved by 0 in all 16 sequences. The missing term appears in the next Goertzel burst's reading, which is one term long.

When every term is the same (a steady input and one lookup value), the carried term stands in for the missing one from the second burst on: in the test, a burst that directly followed another burst read `N*C`, where a burst that followed a zero burst read `(N-1)*C`. When the input or the lookup value changes from clock to clock, each reading is the previous burst's last term plus the first N-1 terms of its own burst.

The shortfall was one term at both burst lengths tested. The idle reading is stable, and every term reaches the accumulator eventually.

The difference of two idle readings is still needed as well, because `GETXACC` does not clear the accumulators while the streamer is idle; that is Erratum E4, and the workaround below steps around both.

## A proven workaround {#sec-e5-workaround}

**What any workaround must do:** deliver the burst's held last term to the accumulators before reading them, in SINC1 mode.

**One way, proven on P2 hardware:** the `burst_sums` helper routine, which ends every burst with a zero-term burst before reading and also steps around Erratum E4.

```pasm2
{ Runs one DDS/Goertzel burst (SINC1 only) and returns its exact
  sums. Put your XINIT D and S in burst_mode and burst_sel, then
  CALL #burst_sums with the streamer idle. It leaves the burst's
  cosine sum in cos_sum and its sine sum in sin_sum.
}
CON
  ZERO_COUNT = 4    ' each zero burst: a count of 4
  INPUT_NIB  = 3    ' S nibble 3 = S[15:12], the summed inputs
DAT
burst_sums  mov     zero_mode, burst_mode       ' zero burst: your mode,
            setword zero_mode, #ZERO_COUNT, #0  '   count 4,
            mov     zero_sel, burst_sel         '   your S with every
            setnib  zero_sel, #0, #INPUT_NIB    '   input off: S[15:12]=0
            xinit   zero_mode, zero_sel         ' adds any held term
            waitxfi
            getxacc cos_base                    ' idle read: no clear
            mov     sin_base, 0-0
            xinit   burst_mode, burst_sel       ' your burst
            waitxfi
            xinit   zero_mode, zero_sel         ' adds its last term
            waitxfi
            getxacc cos_sum                     ' idle read again
            mov     sin_sum, 0-0
            sub     cos_sum, cos_base           ' cosine sum, all N terms
            sub     sin_sum, sin_base           ' sine sum, all N terms
            ret

burst_mode  long    $F007_0100                  ' your D (count 256 here)
burst_sel   long    $0008_80A5                  ' your S
zero_mode   long    0                           ' built: the zero burst's D
zero_sel    long    0                           ' built: the zero burst's S
cos_base    long    0                           ' before reading, cosine
sin_base    long    0                           ' before reading, sine
cos_sum     long    0                           ' result: cosine sum
sin_sum     long    0                           ' result: sine sum
```

Each call leaves in `cos_sum` and `sin_sum` the sums of your burst alone, all N of its terms, and leaves no term held for the next burst: a *helper routine*, for SINC1 mode.

On silicon, this block returned exactly N terms on both sums in all 60 calls of its test program, for bursts of 1 to 1001 clocks at both input levels; in the 6 calls made while an earlier burst's term was still held, it added that term before its first reading, and it left no term for any later call; see *How it was proven on P2 hardware*.

The routine is for SINC1 mode. In SINC2 mode its zero burst has not been tested as a flush, and the routine is not recommended there. SINC2 has its own, separate constraint, which is documented and is not this erratum: the P2 Documentation's note on Goertzel SINC2 mode, by Chip Gracey (2024.12.16), states that a varying number of iterations in a Goertzel cycle corrupts the current and next samples. Its two remedies held on P2 hardware in the test program `e5-goertzel-sinc2-iteration-count-test.spin2` (2026-09-25, at 200 MHz, run twice). With every NCO cycle the same length (`SETXFRQ` of `$0080_0000`, 256 clocks per cycle, 2,048-clock commands chained with `XCONT`), 0 of 1,020 SINC2 samples were off. With each command issued by `XZERO`, at a `SETXFRQ` value of `$0080_0040` with 8 NCO cycles per command and of `$00A3_D70C` with 100 and with 25,000, every command kept one length and 0 of 1,020, 0 of 2,044 and 0 of 12 samples changed, where `XCONT` at the same settings gave 30, 12 and 4 corrupted samples.

This is the same routine Erratum E4 prints, because one call steps around both errata. To use it, put your `XINIT` D operand (the Goertzel mode word with your count) in `burst_mode` and your S operand in `burst_sel`, set `SETXFRQ` as your program already does, and `CALL #burst_sums` with the streamer idle. The values printed in `burst_mode` and `burst_sel` are the test program's.

The zero bursts are your mode word with a count of `ZERO_COUNT` (4) and `S` nibble `INPUT_NIB` ([15:12]) clear, so every term they form is zero. The first one's first clock adds whatever term an earlier burst left held, so the before reading is complete; the second adds your burst's last term, and leaves a zero term held. Both readings are taken with the streamer idle, where `GETXACC` clears nothing (Erratum E4), so their difference is your burst.

**Other ways that meet the condition.** By the mechanism under *Why it happens*, a Goertzel burst whose terms are all zero, run after your burst and before the reading, delivers the held term without the rest of the routine. The kind measured is the routine's own, a count of 4 with S[15:12] clear: in the erratum test such a zero burst, started by `XINIT` and read after a wait of 500 clocks rather than after `WAITXFI`, left the reading exactly N terms above the reading taken before the measured burst, in all 16 sequences. Other zero bursts were not tested.

**Cost.** Each call runs two zero bursts of 4 NCO rollovers each, at your `SETXFRQ` rate, besides your burst, and the cog waits in `WAITXFI` until each command has finished. The routine is 17 instructions, and 8 longs of cog RAM hold its operands and results.

**Limits.**

- **One burst at a time, from an idle streamer.** The routine starts every command with `XINIT`, which issues it at once, so it does not fit a continuous stream of commands chained with `XCONT`.
- **Conditions of the test.** The workaround's test program ran the routine once, from cog RAM on a P2 board at 200 MHz, with an NCO frequency of `$8000_0000`, one input pin, no DAC output, and bursts of 1 to 1001 clocks, the first call of each record made with an earlier burst's term still held. With DAC channels enabled, the zero bursts are DDS/Goertzel commands like any other and, by the P2 Documentation, output on each of their clocks; that case, more than one input pin, other NCO frequencies and hub execution were not tested.

## Why it happens {#sec-e5-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

On each active clock of a Goertzel burst, two registers update together. One is an internal term register: it takes the term formed on that clock from the lookup value and the pin sum. The other is the accumulator that `GETXACC` reads: it adds the value the term register held going into that clock, which is the term formed on the previous active clock. Both update on the same clock edge, so the accumulator is always one term behind the term register.

When a burst ends, both registers stop updating. The last term formed stays in the term register. No instruction reads that register and nothing changes it while the streamer is idle, so waiting does not deliver it. On the first active clock of the next Goertzel burst the accumulator adds it, while the term register takes that burst's first term.

A zero-term burst works for the same reason. Its first clock moves the held term into the accumulator, and its own terms are all zero, so it leaves zero behind.

## How it was proven on P2 hardware {#sec-e5-proof}

**The arrangement.** One P2 board at 200 MHz, nothing attached to P3.

- All streamer work and every `GETXACC` ran in a measuring cog started by `COGINIT`. The debugger was confined to cog 0 (`DEBUG_COGS = %0000_0001`), so no debug interrupt ran in the measuring cog (cog 1 in the run). Cog 0 only collected and printed the results.
- The measuring cog drove P3 as a plain output, low for half the run and high for the other half, in place of an ADC bitstream. The streamer took its inputs from pin group 0 (P0 to P3) with only base pin +3 summed.
- All 512 LUT longs held `$2513_0000`: cosine byte `$13` (19) and sine byte `$25` (37). Every cosine term was therefore +19 or -19 and every sine term +37 or -37, the sign set by P3. With S[19] clear, the P2 Documentation's summation table counts a 0 as -1 and a 1 as +1, so the cosine term C is -19 with P3 low and +19 with P3 high.
- `SETXFRQ` was set to `$8000_0000`, one NCO rollover per clock, so a command count of N is a burst of N clocks.
- The mode word was `$F007_0000` plus the count: DDS/Goertzel, SINC1, no DAC output, pin group 0. A term burst used S = `$0000_80C3` (S[15] set: base pin +3 summed); a zero burst used S = `$0000_00C3` (S[15:12] clear) and a count of 4.
- Every reading was taken 500 clocks after the `XINIT` that preceded it, with the streamer idle.

**One sequence**, run for N = 64 and N = 65, each from its own start:

| Step | Streamer command | Then read |
|---|---|---|
| 1 | zero burst | `B` |
| 2 | burst of N clocks | `R1`; 1000 clocks later, `R1b` |
| 3 | zero burst | `R2` |
| 4 | burst of N clocks | `R3` |
| 5 | burst of N clocks | `R4` |
| 6 | zero burst | `R5` |

The quantities are `d1 = R1-B`, `d2 = R2-R1`, `d3 = R3-R2`, `d4 = R4-R3` and `d5 = R5-R4`. Steps 4 to 6 test the carry: two bursts back to back, then a zero burst. The run was four repetitions of both lengths at P3 low, then the same at P3 high: 16 sequences.

**The outcomes, written into the program before the run**, in units of the per-clock term C:

| Hypothesis | `d1` | `d2` | `d3`, `d4`, `d5` |
|---|---|---|---|
| One-clock lag (the prediction) | `(N-1)*C` | `C` | `(N-1)*C`, `N*C`, `C` |
| No lag | `N*C` | 0 | `N*C`, `N*C`, 0 |
| Last term lost | `(N-1)*C` | 0 | `(N-1)*C`, `(N-1)*C`, 0 |

A nonzero `R1b-R1` under any of them would mean the accumulator moved while the streamer was idle, which none of the three allows.

**The controls**, each of which had to pass before the program would print a verdict:

- the LUT read back `$2513_0000` at addresses `$0C3`, `0` and `$1FF`;
- `TESTP` read P3 at its driven level before and after every sequence;
- a zero burst following a zero burst added nothing (the reading before step 1 equalled `B`);
- every one of `d1` to `d5` was a whole multiple of 19;
- C was measured without assuming any hypothesis, as `R2-B` at N = 65 minus `R2-B` at N = 64, which is one term under all three. It had to be 19 in magnitude, the same in every repetition, and opposite in sign between P3 low and P3 high.

**The results.** Every control passed. C measured -19 in all four repetitions at P3 low and 19 in all four at P3 high. The first repetition at each level and length read:

| P3 | N | `d1` | `R1b-R1` | `d2` | `d3` | `d4` | `d5` |
|---|---|---|---|---|---|---|---|
| low | 64 | `-1_197` | 0 | `-19` | `-1_197` | `-1_216` | `-19` |
| low | 65 | `-1_216` | 0 | `-19` | `-1_216` | `-1_235` | `-19` |
| high | 64 | `1_197` | 0 | `19` | `1_197` | `1_216` | `19` |
| high | 65 | `1_216` | 0 | `19` | `1_216` | `1_235` | `19` |

The other three repetitions of each row read the same values. All 16 sequences match the one-clock-lag row of the outcomes table: `d1 = (N-1)*C`, `d2 = C`, `R1b-R1 = 0`, and the carry steps `(N-1)*C`, `N*C`, `C`. The sine accumulation shows the same pattern with a term of 37: at P3 low and N = 64 it read `d1=-2_331`, `d2=-37`, `d3=-2_331`, `d4=-2_368`, `d5=-37`, and it read the lag pattern and the carry pattern in 16 of 16 sequences.

The zero burst of step 3 is the kind the workaround uses: a count of 4 with S[15:12] clear. In all 16 sequences the reading after it had gained exactly N terms over the reading before the measured burst, and the next burst read `(N-1)*C`, so no term was carried past the zero burst. This test waited a fixed 500 clocks after each `XINIT` rather than using `WAITXFI`, and had no DAC output enabled.

The test ran on 2026-09-24, twice, from two builds of the same program with identical measuring code. Every measured value matched between the two runs.

### The workaround's test {#sec-e5-workaround-proof}

The workaround ran in the test program described in Erratum E4, which calls the printed routine byte for byte. For this erratum its checks are these. The uncorrected part of each record must show the lag in the same run: a 64-clock burst read 63 × C, the 65-clock burst right after it read 65 × C, a zero burst alone read C, and a 7-clock burst read 6 × C, with its last term left held. The first call of `burst_sums` in each record starts with that term held, so its before reading must have gained exactly C, and every later call's nothing; every call must return N × C, for N = 1 to 1001. A result of (N-1) × C would mean the zero burst did not deliver the last term.

**The results.** Every control passed, and the per-clock term measured C = 61 on the cosine sum and 23 on the sine sum at P3 low, -61 and -23 at P3 high, in every record. The uncorrected part showed the lag in all 12 rows (6 records, cosine and sine): at P3 low, on the cosine sum, the 64-clock burst read 3,843 (63 × 61), the 65-clock burst right after it 3,965 (65 × 61), the zero burst alone 61, and the 7-clock burst 366 (6 × 61); on the sine sum 1,449, 1,495, 23 and 138; at P3 high the same values negated. The first call of each record found exactly C waiting: its before reading was 61 above the 7-clock burst's reading at P3 low (77,165 against 77,104 in the first record) and 61 below it at P3 high (396,744 against 396,805 in the fourth). Every later call's before reading equalled the program's own reading after the previous call, so no call left a term behind. Every one of the 60 calls returned N × C on both sums, from 61 for N = 1 to 61,061 for N = 1001 on the cosine sum at P3 low, and -23 to -23,023 on the sine sum at P3 high; none returned (N-1) × C.

The test program was run once, on 2026-09-26, on a P2 board at 200 MHz. The values above are read from its raw lines, not from its verdict line.

## The test program {#sec-e5-program}

The test program is `e5-goertzel-one-clock-lag-test.spin2` in the examples archive. Its Spin2 code in cog 0 starts the measuring cog, waits for it to finish, prints every raw reading and delta, checks the controls, and prints the verdict. The measuring cog is PASM2 in the program's DAT block and is the only code that touches the streamer.

Each sequence runs the burst and the zero burst like this. The program's comments call a term burst a K burst and the S operand `imm`, and `dk_` holds the burst word for the current N; `dz_` is the zero burst's word with its count of 4, and `imz_` and `imk_` are the two S operands. `GETXACC` places the sine accumulation into the S field of the next instruction, so each `GETXACC` is followed by `mov ..., 0-0`, which receives it:

```pasm2
                xinit   dk_, imk_               ' BURST: count N, imm[15]=1
                waitx   ##WAIT_IDLE
                getxacc r1x_                    ' R1
                mov     r1y_, 0-0
                waitx   ##WAIT_R1B
                getxacc r1bx_                   ' R1b, 1000 clocks later
                mov     r1by_, 0-0

                xinit   dz_, imz_               ' IDIOM: zero burst
                waitx   ##WAIT_IDLE
                getxacc r2x_                    ' R2
                mov     r2y_, 0-0
```

The carry steps follow directly, with no zero burst between the two term bursts:

```pasm2
                xinit   dk_, imk_               ' CARRY ARM: K burst
                waitx   ##WAIT_IDLE
                getxacc r3x_                    ' R3
                mov     r3y_, 0-0

                xinit   dk_, imk_               ' second K burst right after
                waitx   ##WAIT_IDLE
                getxacc r4x_                    ' R4
                mov     r4y_, 0-0

                xinit   dz_, imz_               ' zero burst flushes
                waitx   ##WAIT_IDLE
                getxacc r5x_                    ' R5
                mov     r5y_, 0-0
```

`WAIT_IDLE` is 500 clocks and `WAIT_R1B` is 1000. Before the first sequence the measuring cog fills all 512 LUT longs, reads three of them back for the LUT control, drives P3 and runs one zero burst.

To run it, compile with `pnut-ts -d` and load it with DEBUG enabled (2 Mbaud). P3 must be free: the program drives it. A run that decides the question prints no `RIG FAIL` lines, a `C measured` line showing -19 and 19, and one `VERDICT:` line. Every raw reading is printed as well, so the verdict can be re-derived from the output rather than taken from the program.

The workaround's test program is `e4-e5-workaround-read-sums-test.spin2`, described in Erratum E4. Its uncorrected part shows this erratum in the same run as the workaround; the second half of it reads like this, a `GETXACC` "to clear" followed by the 65-clock burst, whose reading carries the 64-clock burst's held term:

```pasm2
                mov     dk_, dmode_
                setword dk_, #N_NAIVE_B, #0
                getxacc ax_                     ' P2: "clear" again
                mov     ay_, 0-0
                xinit   dk_, son_               ' burst N2, right after
                waitxfi
                getxacc bx_                     ' R2
                mov     by_, 0-0
                wrlong  ax_, ptrb++             ' R_P2X
                wrlong  ay_, ptrb++
                wrlong  bx_, ptrb++             ' R_R2X
                wrlong  by_, ptrb++
```

The test program `e5-goertzel-sinc2-iteration-count-test.spin2`, cited in *A proven workaround*, is the check of the P2 Documentation's separate SINC2 constraint, not of this erratum.

## Status {#sec-e5-status}

| Field | Content |
|---|---|
| Erratum | E5 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; helper routine (SINC1) |
| Affects | `GETXACC` readings after a DDS/Goertzel burst in SINC1 mode, sine and cosine; tested with bursts of 64 and 65 clocks started by `XINIT` |
| Test program | `e5-goertzel-one-clock-lag-test.spin2`; the workaround: `e4-e5-workaround-read-sums-test.spin2` |


# Erratum E6: In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC {#ch-e6}

::: caution
**Expected:** in a DAC smart-pin mode with `TT` = `%00`, the pin's output is off and raising `OUT` turns on the pin's ADC.

**Actual:** with `TT` = `%00`, raising `OUT` runs nothing: the ADC stays off, and the pin reads exactly as it does with `OUT` low.

**Workaround:** `TT` bit 0 must be set in your `WRPIN` word (`$0014_0042` in place of `$0014_0002`), and the pin's DAC then drives the pin while the ADC runs; see *A proven workaround*.
:::

This erratum affects a program that configures a pin for one of the DAC smart-pin modes (`%SSSSS` = `%00001` to `%00011`, with `M[12:10]` = `%101`) with `TT` bit 0 clear, and relies on `OUT` to run the pin's ADC. A pin configured with `TT` = `%01`, the value of the Spin2 symbols `P_TT_01` and `P_OE`, is not affected. Of the three DAC smart-pin modes, only DAC noise (`%00001`) was tested.

## What the P2 is documented to do {#sec-e6-documented}

The P2 Documentation (Parallax), section SMART PINS, describes the `%TT` field of the `WRPIN` configuration word (bits 7:6) in a table that gives one rule for every smart-pin mode and a second rule for the DAC smart-pin modes:

> for all smart pin modes (%SSSSS > %00000):
>
> x0 = output disabled, regardless of DIR
>
> x1 = output enabled, regardless of DIR
>
> for DAC smart pin modes (%SSSSS = %00001..%00011):
>
> 0x = OUT enables ADC in DAC_MODE, M[7:0] overridden
>
> 1x = OTHER enables ADC in DAC_MODE, M[7:0] overridden

The same table defines the pin state the second rule refers to: "'DAC_MODE' is enabled when M[12:10] = %101". The two rules act on different bits. Bit 0 of `TT` sets the output enable; bit 1 chooses whether `OUT` or `OTHER` switches the ADC. By the table, `TT` = `%00` in a DAC smart-pin mode is a pin whose output is disabled and whose ADC `OUT` switches, and `TT` = `%01` is the same with the output enabled. Nothing in the table makes the ADC depend on the output enable.

The mode descriptions in the section SMART PIN MODES say what the ADC provides. For DAC noise, the mode tested here:

> RDPIN/RQPIN can be used to retrieve the 16-bit ADC accumulation from the last sample period.

For the two dithered DAC modes, `%00010` and `%00011`, each description carries the same sentence, which names `OUT` as the switch:

> If OUT is high, the ADC will be enabled and RDPIN/RQPIN can be used to retrieve the 16-bit ADC accumulation from the last sample period.

The KNOWN BUGS section of the P2 Documentation does not list this behaviour.

## What the P2 does {#sec-e6-actual}

The part was tested in DAC noise mode (`%SSSSS` = `%00001`) with `M[12:10]` = `%101` and `M[9:8]` = `%00`, the setting the Spin2 symbol `P_DAC_990R_3V` names: a 990-ohm DAC of 3.3 V peak, with the ADC feeding the pin's input. The two configuration words differ only in bit 6, which is `TT` bit 0:

- `$0014_0002`: `TT` = `%00`. Raising `OUT` does not run the ADC. The pin's read state stays exactly as it is with `OUT` low: 0 in every one of 4,096 reads, in every sample taken.
- `$0014_0042`: `TT` = `%01`. Raising `OUT` runs the ADC, as the table states. The pin's read state toggles, high in 1,958 to 2,093 of 4,096 reads per sample across the two runs. With `OUT` low the ADC is off and the read state is 0 in every read.

So in the mode tested, and at the two `TT` settings tested, `OUT` switches the ADC only while `TT` bit 0 also enables the pin's output. The two settings in which `OTHER` switches the ADC, `TT` = `%10` and `%11`, were not tested.

## What your program sees {#sec-e6-sees}

If your program configures a DAC smart-pin mode with `TT` = `%00` and raises `OUT` to start the ADC, the ADC does not start. The pin behaves as it does with `OUT` low: in the test, its read state held at 0 through every read.

The test program read the pin's state through its neighbouring pin, and did not issue `RDPIN` or `RQPIN`. What `RDPIN` returns in DAC noise mode at `TT` = `%00` with `OUT` high was not measured here.

## A proven workaround {#sec-e6-workaround}

**What any workaround must do:** set `TT` bit 0 in the `WRPIN` word of a pin in a DAC smart-pin mode whose ADC you switch with `OUT`.

**One way, proven on P2 hardware:** the tested DAC noise word with `TT` = `%01`.

```spin2
  CFG_DAC_TT01      = $0014_0042        ' DAC_MODE, DAC noise, TT = %01
```

Written to the pin with `WRPIN` in place of `$0014_0002`, this word makes `OUT` run the pin's ADC; it is a rule at each use, applied wherever you configure a pin for a DAC smart-pin mode and switch its ADC with `OUT`.

The change is one bit: bit 6 of the `WRPIN` word, `TT` bit 0, value `$40`. In Spin2 symbols the word is `P_DAC_990R_3V | P_TT_01 | P_DAC_NOISE`; `P_OE` is another name for the same value as `P_TT_01`. The test program checked at run time that this composition equals `$0014_0042`. In another DAC smart-pin word the corresponding change is the same bit 6; only the word above was tested (limits below).

**Other ways that meet the condition.** Written with the Spin2 symbols above, or as the literal, the word is the same change. `TT` = `%11` also sets bit 0, but by the table it gives the ADC switch to `OTHER` in place of `OUT`, and it was not tested.

The cost is the pin's output. With `TT` bit 0 set, the table's first rule enables the pin's output regardless of `DIR`, and in DAC noise mode the P2 Documentation says the mode feeds "the pin's 8-bit DAC pseudo-random data on every clock". While the ADC runs, the pin is driven by its DAC. Use a pin that nothing else drives. The test pin had nothing attached, so the drive itself was not observed on the bench.

The limits of the proof:

- Only DAC noise (`%00001`) was tested. The dithered DAC modes (`%00010`, `%00011`) share the table rows quoted above but were not tested.
- Only the `M[9:8]` = `%00` DAC setting (`P_DAC_990R_3V`) was tested.
- Only `TT` = `%00` and `%01` were tested. `TT` = `%10` and `%11`, where `OTHER` switches the ADC, were not.
- The ADC was observed through the pin's read state. Its accumulation was not read with `RDPIN`, and no `WXPIN` or `WYPIN` was issued to the pin.
- The rows of the table for a DAC pin with the smart pin off (`%SSSSS` = `%00000`) are a different case and were not tested.

No setting tested runs the ADC in these modes with the pin's output disabled. A program that needs the ADC with the pin undriven has no tested setting in the DAC smart-pin modes.

## Why it happens {#sec-e6-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

In every smart-pin mode, `TT` bit 0 is the pin's output enable, as the table's first rule says; the P2 Documentation adds that "while a smart pin is configured, the %TT bits, explained above, will govern the pin's output enable, regardless of the DIR state". `OUT` reaches the I/O pin circuit as the pin's output bit: in the DAC smart-pin modes the smart pin does not take the output bit over, and with `TT` bit 1 clear it is not replaced by `OTHER`.

In the DAC pin state (`M[12:10]` = `%101`), the I/O pin circuit runs its DAC only while the output enable is high, and runs its ADC only while the output enable and the output bit are both high. With the output enable low, nothing in the circuit runs. The table's second rule describes the ADC switch as depending only on the bit that `TT` bit 1 selects; the circuit adds the output enable as a second condition. With `TT` = `%00`, raising `OUT` sets the output bit, but the output enable stays low, and the ADC does not start.

The same reading gives the cost of the workaround. Setting `TT` bit 0 raises the output enable, which turns on the DAC as well, so the ADC runs only while the DAC drives the pin.

The study left open what the pin's read state carries in the DAC pin state while the ADC is off. The test measured it rather than assuming it; the values are in the next section.

## How it was proven on P2 hardware {#sec-e6-proof}

**The arrangement.** One P2 board at 200 MHz, with nothing attached to P4 or P5.

- P4 is the pin under test. P5 observes it.
- Every pin operation and every read ran in a measuring cog started by `COGINIT` (cog 1 in both runs). The debugger was confined to cog 0 (`DEBUG_COGS = %0000_0001`), which only collected the results from hub RAM and printed them.
- P4's own `IN` bit cannot show the ADC: in a smart-pin mode, `IN` is the smart pin's flag. P5 was configured once with `$7000_0000` and left with `DIR` low for the whole run, so it never drove. That word selects "relative -1 pin's read state" as P5's A input (`%AAAA` = `%0111`) with P5's smart pin off, and in that case "The resultant 'A' will drive the IN signal". Bit 5 of `INA` therefore carries P4's read state.
- One sample is 4,096 consecutive reads of `INA` in a three-instruction `REP` loop (6 clocks per read), counting the reads in which bit 5 is 1.

**The conditions.** Each condition sets P4 afresh, in this order: `DIRL` (smart pin held in reset while it is configured); `WRPIN` with the condition's word; `DIRH`; `OUTL` or `OUTH`, set explicitly whatever the previous condition left; a `WAITX` of 10,000 clocks; one sample.

| Condition | `WRPIN` word | `TT` | `OUT` |
|---|---|---|---|
| C1 | `$0014_0042` | `%01` | low |
| C2 | `$0014_0042` | `%01` | high |
| C3 | `$0014_0002` | `%00` | low |
| C4 | `$0014_0002` | `%00` | high |

The run was five rounds of C1, C2, C3, C4 in that order, which spreads each condition's five samples across the run.

**The outcomes, written into the program before the run.** Condition X *separates* from condition Y when every sample of X lies outside the range from the smallest to the largest sample of Y.

- C2 must separate from C1, or the reading does not show the ADC at all and the run decides nothing.
- The defect: C4 does not separate from C3, and C4 separates from C2. `OUT` does nothing at `TT` = `%00`.
- The documented behaviour: C4 separates from C3, and C4 does not separate from C2. `OUT` runs the ADC at `TT` = `%00`.
- Any other pattern is inconclusive.

No value was predicted for C1 and C3; they were measured and printed.

**The controls**, each of which had to pass before the program would print a verdict:

- each configuration word, decoded into its published `WRPIN` fields, had the expected values, and equalled its Spin2 symbol composition (`P_DAC_990R_3V | P_TT_00 | P_DAC_NOISE`, `P_DAC_990R_3V | P_TT_01 | P_DAC_NOISE`, `P_MINUS1_A | P_LOGIC_A | P_TT_00 | P_NORMAL`);
- before the rounds and again after them, P4 as a plain pin (`WRPIN #0`) driven high by `DRVH` had to read 4,096 of 4,096 at P5, and driven low by `DRVL` had to read 0. This shows that P5 follows P4's read state and that the loop counts every read.

**The results.** Every control passed in both runs: the path control read 4,096 and 0 before the rounds and 4,096 and 0 after them. The samples, as counts of reads with bit 5 high out of 4,096:

| Condition | Run | Round 1 | Round 2 | Round 3 | Round 4 | Round 5 |
|---|---|---|---|---|---|---|
| C2: `TT` = `%01`, `OUT` high | 1 | 1,963 | 2,093 | 2,025 | 1,986 | 2,056 |
| C2: `TT` = `%01`, `OUT` high | 2 | 2,006 | 2,017 | 1,958 | 1,985 | 2,016 |
| C1, C3 and C4 | 1 and 2 | 0 | 0 | 0 | 0 | 0 |

In both runs, C2 separated from C1, C4 did not separate from C3, and C4 separated from C2: the pattern written down in advance for the defect. With `TT` = `%00`, `OUT` high read the same as `OUT` low in every sample, and never as the running ADC.

The same run proves the workaround. C2 is the workaround: with `$0014_0042`, `OUT` high ran the ADC in all ten samples of the two runs, and with `OUT` low (C1) the ADC was off in all ten.

The test ran on 2026-09-25, twice. Apart from the C2 samples and the C2 range computed from them, the two runs printed the same values.

## The test program {#sec-e6-program}

The test program is `e6-dac-mode-adc-enable-test.spin2` in the examples archive. Its Spin2 code in cog 0 decodes and checks the three configuration words, starts the measuring cog, waits for it to finish, prints every sample, checks the path control, and prints the separation tests and one verdict. The measuring cog is PASM2 in the program's `DAT` block and is the only code that touches the pins.

The measuring cog runs the four conditions in a loop of five rounds. `cfg_` holds the `WRPIN` word and `outlvl_` the `OUT` level for the next condition:

```pasm2
                mov     round_, #ROUNDS
.round          mov     cfg_, cfg_tt01_         ' C1: TT = %01, OUT low
                mov     outlvl_, #OUT_LOW
                call    #do_cond
                mov     outlvl_, #OUT_HIGH      ' C2: TT = %01, OUT high
                call    #do_cond
                mov     cfg_, cfg_tt00_         ' C3: TT = %00, OUT low
                mov     outlvl_, #OUT_LOW
                call    #do_cond
                mov     outlvl_, #OUT_HIGH      ' C4: TT = %00, OUT high
                call    #do_cond
                djnz    round_, #.round
```

`cfg_tt01_` and `cfg_tt00_` are `DAT` longs holding `$0014_0042` and `$0014_0002`. The routine `do_cond` issues `DIRL`, `WRPIN cfg_`, `DIRH`, then `OUTL` or `OUTH` by the value of `outlvl_`, and calls `sample`. Every sample waits 10,000 clocks, then counts the reads of `INA` in which bit 5 (`PIN_NBR`) is 1:

```pasm2
' One sample: settle, then READS_PER_SAMPLE reads of INA, counting bit P+1.
sample          waitx   ##SETTLE_CLK
                mov     count_, #0
                rep     @.read_end, reads_
                mov     insnap_, ina
                testb   insnap_, #PIN_NBR       wc
        if_c    add     count_, #1
.read_end       wrlong  count_, ptrb
                add     ptrb, #4
                ret
```

`reads_` holds 4,096. The path control runs before and after the rounds, with P4 returned to a plain pin:

```pasm2
' Control K: pin P as a plain pin (smart pin off, DIR enables the output),
' one sample driven high, one driven low.
path_control    dirl    #PIN_P
                wrpin   #0, #PIN_P
                drvh    #PIN_P                  ' DIR = 1, OUT = 1
                call    #sample
                drvl    #PIN_P                  ' DIR = 1, OUT = 0
                call    #sample
                ret
```

At the end the measuring cog returns both pins to the smart-pin-off state with `DIRL`, `WRPIN #0` and `OUTL` before it signals that it is done.

To run it, compile with `pnut-ts -d` and load it with DEBUG enabled. P4 and P5 must be free: the program drives P4, and a device attached to either pin can fail the path control. A run that decides the question prints no `RIG FAIL` lines, the path-control counts 4,096 and 0, and one `VERDICT:` line. Every sample is printed as well, so the verdict can be re-derived from the output rather than taken from the program.

## Status {#sec-e6-status}

| Field | Content |
|---|---|
| Erratum | E6 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-25, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes — 2026-09-25; a rule at each use: set `TT` bit 0 in the `WRPIN` word |
| Affects | a pin in a DAC smart-pin mode with `TT` = `%00`: raising `OUT` does not run its ADC. Tested in DAC noise mode (`%00001`), `P_DAC_990R_3V`, `TT` = `%00` and `%01` only |
| Test program | `e6-dac-mode-adc-enable-test.spin2` |


# Erratum E7: A Blocking RDFAST Can Skip Its Wait After a No-Wait RDFAST {#ch-e7}

::: caution
**Expected:** a blocking `RDFAST` (`D[31]` = 0) waits until the FIFO has begun receiving hub data, so the next instruction can read the first long at its address.

**Actual:** issued 8 to 15 clocks after a no-wait `RDFAST` (`D[31]` = 1), at one spacing that depends on the hub alignment, the blocking `RDFAST` takes 2 clocks without waiting, and the next `RFLONG` returns `$0000_0000`.

**Workaround:** at least 16 clocks must pass from the start of the no-wait `RDFAST` to the start of the blocking one; see *A proven workaround*.
:::

This erratum affects a cog that starts the hub FIFO with a no-wait `RDFAST` and then, a few clocks later, restarts it at another address with a blocking `RDFAST` and reads in the next instruction. The failure needs both instructions, in that order, 8 to 15 clocks apart; a cog that uses only blocking `RDFAST`s, or only no-wait ones, does not meet it. It was measured in cog execution, with `RFLONG` as the read.

## What the P2 is documented to do {#sec-e7-documented}

The P2 Documentation (Parallax), section FAST SEQUENTIAL FIFO INTERFACE, gives `RDFAST` and `WRFAST` two modes, chosen by bit 31 of the D operand. For the blocking mode:

> If D[31] = 0, RDFAST/WRFAST will wait for any previous WRFAST to finish and then reconfigure the hub FIFO interface for reading or writing. In the case of RDFAST, it will additionally wait until the FIFO has begun receiving hub data, so that it can start being used in the next instruction.

For the no-wait mode:

> If D[31] = 1, RDFAST/WRFAST will not wait for FIFO reconfiguration, taking only two clocks. In this case, your code must allow a sufficient number of clocks before any attempt is made to read or write FIFO data.

The blocking paragraph names one thing the instruction waits for first, a previous `WRFAST`, and makes no exception for a `RDFAST` that follows a no-wait `RDFAST`. By it, a blocking `RDFAST` issued at any time after a no-wait one still waits until the FIFO has begun receiving the new address's data, and the next instruction can read that data.

The no-wait paragraph's requirement describes a different case, and that case is not this erratum. In the same test, a read issued too soon after a no-wait `RDFAST` alone returned `$0000_0000`, and the first spacing at which such a read was correct was 8 to 15 clocks, depending on hub alignment. The documentation states the requirement for that case, and the case belongs to the companion manual *P2 Anti-Patterns*. This erratum is the blocking `RDFAST` failing its own promise: the read follows a blocking `RDFAST`, which is documented to wait.

The KNOWN BUGS section of the P2 Documentation does not list this behaviour. In the reviewers' comments attached to that section of the document, replying to a note that an `RDFAST` corruption bug should be listed there, Chip Gracey wrote: "Yes, but I can't explain it well." The comments do not describe the conditions or the symptom. The defect in this chapter is plausibly that bug; nothing in the comments establishes it.

## What the P2 does {#sec-e7-actual}

The arrangement tested, in cog execution: a no-wait `RDFAST` (D = `$8000_0000`), then either nothing or a `WAITX`, then a blocking `RDFAST #0` to a different hub address, then `RFLONG` as the next instruction. The spacing is counted from the start of the no-wait `RDFAST` to the start of the blocking one, the no-wait `RDFAST`'s own 2 clocks included. It was swept over 2 and 4 to 44 clocks (3 cannot be reached, since every instruction takes at least 2 clocks) in each of 64 hub alignments: the 8 hub RAM slices the blocking `RDFAST`'s address can lie in, each at 8 starting points in the hub's rotation.

- In every alignment, exactly one spacing failed, in all 16 trials. At that spacing the blocking `RDFAST` took 2 clocks, the time of a no-wait `RDFAST`, and the `RFLONG` returned `$0000_0000`: not the first long at the blocking `RDFAST`'s address, not data from the no-wait `RDFAST`'s address, and not the FIFO's earlier contents.
- The failing spacing was between 8 and 15 clocks, set by the hub alignment. Each spacing from 8 to 15 clocks was the failing one in exactly 8 of the 64 alignments.
- At every other spacing tested, the blocking `RDFAST` waited 10 to 17 clocks, and the `RFLONG` returned the correct first long.

In total, 1,024 of 43,008 reads were wrong, every one `$0000_0000`, and the other 41,984 were correct.

The failure needs the no-wait `RDFAST` before the blocking one. In the same test, a blocking `RDFAST` with no `RDFAST` before it gave the correct next-instruction read in all 3,072 trials (with `RFLONG`, `RFWORD` and `RFBYTE`), taking 10 to 17 clocks. A second no-wait `RDFAST` in the blocking one's place, with a `WAITX #200` before the read, moved the FIFO to its own address in all 43,008 trials.

## What your program sees {#sec-e7-sees}

If your program issues a blocking `RDFAST` 8 to 15 clocks after a no-wait `RDFAST`, the `RFLONG` that follows can return `$0000_0000` in place of the first long at the new address. Nothing else marks the failure: the read does not stall, and with `WCZ` the flags were those of a zero long (C clear, Z set) in every failing trial the test printed.

Whether it happens depends on the spacing and on the hub alignment at the moment your code runs. Each spacing from 8 to 15 clocks failed in 8 of the 64 alignments tested and read correctly in the other 56, so the same code can read correctly on one pass and return zero on another if its hub alignment differs between them. Spacings of 2 and 4 to 7 clocks, and of 16 to 44 clocks, read correctly in every alignment tested.

The long after the zero is not the second long either. The test printed the second `RFLONG` for one trial in each failing alignment: where the new address lay in hub slice 0, 1 or 2, it returned the first long at that address; in slices 3 to 7 it returned `$0000_0000` again. Reads past the second were not made. The test's data regions in hub RAM were unchanged: it re-checked them after every alignment.

## A proven workaround {#sec-e7-workaround}

**What any workaround must do:** let at least 16 clocks pass from the start of the no-wait `RDFAST` to the start of the blocking one.

**One way, proven on P2 hardware:** a `WAITX #RDFAST_SPACING_WAITX` (12) directly after the no-wait `RDFAST`.

```pasm2
CON
  RDFAST_SPACING_WAITX = 12            ' RDFAST 2 + WAITX 2+12 = 16 clocks
DAT
        rdfast  nowait, hub_first      ' no-wait RDFAST (D[31] = 1)
        waitx   #RDFAST_SPACING_WAITX  ' E7: >= 16 clocks, RDFAST to RDFAST
        rdfast  #0, hub_next           ' blocking RDFAST: now it waits
        rflong  first_long             ' reads hub_next's first long
```

The `WAITX #RDFAST_SPACING_WAITX` (12) makes the spacing from the start of the no-wait `RDFAST` to the start of the blocking one 16 clocks, one more than the largest failing spacing measured, so that the blocking `RDFAST` waits and the `RFLONG` after it reads the first long at `hub_next`; it is a rule at each use, applied wherever your code issues a blocking `RDFAST` after a no-wait one.

In your code, `nowait` is a register holding `$8000_0000` (`D[31]` = 1, and a block count of 0, so no wrap); `hub_first` and `hub_next` hold the two hub addresses, and `first_long` receives the first long at `hub_next`.

The rule is the spacing: at least 16 clocks from the start of the no-wait `RDFAST` to the start of the blocking one. The no-wait `RDFAST` takes 2 clocks and `WAITX #RDFAST_SPACING_WAITX` takes 2 + 12 = 14. The basis is measured: in the erratum test, every spacing from 16 to 44 clocks read correctly in all 64 alignments and all 16 trials of each, and the blocking `RDFAST` then waited its usual 10 to 17 clocks. There the spacing was set by a `WAITX` whose register operand held 12 to 40. The block above, with `RDFAST_SPACING_WAITX` = 12, ran in the workaround test on 2026-09-26: in all 64 alignments, 16 trials each, `first_long` received the first long at `hub_next`, and the next `RFLONG` the long after it, in 1,024 of 1,024 trials, with the blocking `RDFAST` waiting 10 to 17 clocks. In the same run the unspaced arrangement failed as described above in all 64 alignments.

**Other ways that meet the condition.** Other instructions that fill at least 16 clocks from the start of the no-wait `RDFAST` to the start of the blocking one meet the same condition, since the measurements tie the failure to the spacing, not to the `WAITX`. They have not been run: only `WAITX` was placed between the two `RDFAST`s, and instructions that wait for hub RAM there were not tested (limits below).

The cost is the 14 clocks of the `WAITX`, each time a blocking `RDFAST` follows a no-wait one.

The limits of the proof:

- Only `WAITX` was tested between the two `RDFAST`s. Other instructions there, in particular instructions that wait for hub RAM, were not.
- The `WRFAST` counterpart of this arrangement was not tested.
- Making the first `RDFAST` blocking, in place of the spacing, was not tested as a workaround.
- Only `RFLONG` was tested as the read after the blocking `RDFAST`. The streamer was not used.
- The no-wait `RDFAST`'s address was a long in hub slice 0 in every trial; the blocking `RDFAST`'s address was a long in each of the 8 slices. Both used a block count of 0.
- Spacings above 44 clocks were not tested.
- Only cog execution was tested, with one cog using its FIFO, at 200 MHz.

## Why it happens {#sec-e7-why}

No account of the mechanism is available. The clean-room design study did not predict this defect, and the P2 Documentation does not describe it. What follows is what the bench shows about its timing, and what it leaves open.

The failing spacing follows the no-wait `RDFAST`, not the blocking one. The no-wait `RDFAST`'s address was the same long of hub slice 0 in every alignment tested, and at each of the 8 starting points in the hub's rotation the failing spacing was the same for all 8 slices of the blocking `RDFAST`'s address.

It also coincides with the arrival of the no-wait `RDFAST`'s data. In the same test, a no-wait `RDFAST` of a slice-0 address followed by an `RFLONG` alone first read correctly at a spacing equal, at every one of the 8 starting points, to the failing spacing here (table in the next section). The blocking `RDFAST` fails when it is issued on the clock at which the no-wait `RDFAST`'s first long has just become readable. One clock earlier and one clock later, it waits as usual. In slice 0 at the first starting point, it waited 11 clocks at a spacing of 9, took 2 at a spacing of 10, and waited 17 at a spacing of 11.

What is not known: why the wait ends at once on that clock, where the zero comes from, and whether a blocking `WRFAST`, or the streamer, is affected in the same way.

## How it was proven on P2 hardware {#sec-e7-proof}

**Where it came from.** The test was built to measure something else: when the hub FIFO can first be used after `RDFAST` and `WRFAST`, in both modes. The arrangement of this erratum was one of its secondary arrangements, expected to show the blocking promise holding. The defect was not predicted.

**The arrangement.** One P2 board at 200 MHz; no pins used.

- Every FIFO operation ran in a measuring cog started by `COGINIT` (cog 1 in both runs), in cog execution. The debugger was confined to cog 0 (`DEBUG_COGS = %0000_0001`), which sent the commands, classified the results from hub RAM and printed them.
- Three data regions, each starting on a 32-byte boundary, so that long k of a region lies in hub slice k mod 8: the no-wait `RDFAST`'s region, long k = `$3C3C_00C0` + k; the blocking `RDFAST`'s region, `$A5A5_0080` + k; and a third region, `$0D0D_0040` + k, that the FIFO was loaded from before every trial. A wrong read can therefore be traced to its source.
- Each trial loaded the FIFO from the third region with a blocking `RDFAST`, a `WAITX #64`, two `RFLONG`s and a second `WAITX #64`, so that a stale read would show as `$0D0D_0042`. It then read a slice-0 long with `RDLONG`, which ties the cog to the hub rotation, and waited the starting point, 0 to 7 clocks. Between two `GETCT`s came the no-wait `RDFAST` of the first region's long 0, the spacing, the blocking `RDFAST #0` of long s of the second region, and `RFLONG` with `WCZ`. A second `RFLONG` followed.
- The sweep: 8 slices s times 8 starting points gives 64 alignments; 42 spacings (2, and 4 to 44 clocks); 16 trials of each, 43,008 trials in all. The 8 starting points span a whole hub rotation: a blocking `RDFAST` alone took 8 different times over them, in every slice.
- The blocking `RDFAST`'s own clocks are the `GETCT` difference less the `GETCT` overhead, the spacing and the `RFLONG`.

**The outcome, written into the program before the run.** The program expected the first long of the blocking `RDFAST`'s address at every spacing, and reported any other read as a deviation.

**The controls**, each of which had to pass before the program would print a verdict:

- a `GETCT` pair costs 2 clocks, and `WAITX` D costs 2 + D clocks at every delay the sweep used;
- plain `RDLONG`s read every pattern long at every slice;
- with no new `RDFAST`, the loaded FIFO returned `$0D0D_0042` and then the long after it;
- a no-wait `RDFAST`, then `WAITX #200`, then `RFLONG`, returned the right longs.

The program's write controls ran as well. Every control was correct in every trial of both runs.

**The results.** The failing spacing at each starting point, and the spacing at which an `RFLONG` after a no-wait `RDFAST` alone first read correctly, in clocks:

| Starting point (clocks) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Failing spacing, every slice | 10 | 9 | 8 | 15 | 14 | 13 | 12 | 11 |
| First correct no-wait read, slice 0 | 10 | 9 | 8 | 15 | 14 | 13 | 12 | 11 |

At each failing spacing, all 16 trials read `$0000_0000`, and the blocking `RDFAST` took 2 clocks. Over the whole sweep, 1,024 of 43,008 reads were wrong, all `$0000_0000`, and 41,984 were correct; none returned the no-wait `RDFAST`'s data or the FIFO's stale contents. Every spacing from 16 to 44 clocks read correctly in every alignment and trial. Around the failure, in slice 0 at starting point 0:

| Spacing (clocks) | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|
| Blocking `RDFAST` (clocks) | 13 | 12 | 11 | 2 | 17 | 16 |
| `RFLONG` returned | correct | correct | correct | `$0000_0000` | correct | correct |

The test ran on 2026-09-25, twice. The two runs printed the same result for every alignment and spacing.

**The workaround.** The workaround test ran on 2026-09-26, once, on a P2 board at 200 MHz, with the same regions, the same loading of the FIFO before every trial and the same 64 alignments.

- Its controls were the four above and one more: `WAITX #RDFAST_SPACING_WAITX` (12) between two `GETCT`s measured 16 clocks, 2 for the `GETCT` pair and 14 for the `WAITX`, in every trial. Every control was correct in every trial.
- As a positive control, the same run swept the unspaced arrangement over the same 42 spacings. It failed at exactly one spacing in each of the 64 alignments, at the same spacings as in the erratum test (table above), with all 16 trials reading `$0000_0000` and the blocking `RDFAST` taking 2 clocks: 1,024 of 43,008 reads wrong. At every spacing from 16 to 44 clocks, the first read and the long after it were correct in all 29,696 trials.
- The block printed in *A proven workaround*, with nothing else between its lines, read the first long at `hub_next` and then the long after it in 1,024 of 1,024 trials. Its blocking `RDFAST` waited 10 to 17 clocks, taking 8 different times over the 8 starting points in every slice.

## The test program {#sec-e7-program}

The erratum test is `e7-rdfast-blocking-after-no-wait-test.spin2` in the examples archive. Its Spin2 code in cog 0 starts the measuring cog, sends it one command per arrangement, slice and starting point, classifies every trial, prints every row, checks the controls, and prints the verdicts. The measuring cog is PASM2 in the program's `DAT` block and is the only code that touches the FIFO. Besides this erratum's arrangement, the program measures blocking and no-wait `RDFAST` and `WRFAST` on their own, and a second no-wait `RDFAST` in place of the blocking one.

Each trial of this erratum's arrangement starts after the FIFO has been loaded. It ties the cog to the hub rotation, waits the starting point, and starts the timing:

```pasm2
v_rebn          rdlong  c_junk, c_oldb
                waitx   c_phase
                getct   c_t0
```

The next three lines, whose comments run past this page's width, are `rdfast c_nowait, c_midb` (the no-wait `RDFAST`; `c_nowait` holds `$8000_0000`), `waitx c_dly` (the spacing), and `rdfast #0, c_new` (the blocking `RDFAST`). Then the read, in the next instruction:

```pasm2
                rflong  c_r1                            wcz
                getct   c_t1
                wrc     c_r3
                bitz    c_r3, #FLAG_Z_BIT
                rflong  c_r2
                jmp     #post_read
```

`c_r3` records C in bit 0 and Z in bit 1, and the second `RFLONG` reads the long after. A second copy of the sequence, with no `WAITX`, gives the 2-clock spacing. The Spin2 side turns the spacing index j into clocks:

```spin2
  if distIdx == 0
    distClks := INSTR_CLK
  else
    distClks := NW_WAITX_OFFSET + distIdx - 1
```

`INSTR_CLK` is 2 and `NW_WAITX_OFFSET` is 4, and the measuring cog loads `c_dly` with j - 1, so j = 1 to 41 gives 4 to 44 clocks.

To run it, compile with `pnut-ts -d` and load it to RAM with DEBUG enabled. It uses no pins. A run that decides the question prints no `RIG FAIL` lines; this erratum shows as the second `ARM-VERDICT` line, which reads `DEVIATES` with 1,024 of 43,008 reads wrong. Every row is printed, so the result can be re-derived from the output rather than taken from the program.

The workaround test is `e7-workaround-rdfast-spacing-test.spin2`. It uses the same construction and the same trial, and runs the block printed in *A proven workaround*, between two marker comments, in all 64 alignments. Alongside, it runs this erratum's arrangement at every spacing from 2 to 44 clocks: a clean result for the block counts only if that sweep shows the erratum in every alignment, and otherwise the program reports the workaround as inconclusive. Its controls include that `WAITX #RDFAST_SPACING_WAITX` (12) takes 14 clocks. It ends with a `VERDICT E7 WORKAROUND:` line.

## Status {#sec-e7-status}

| Field | Content |
|---|---|
| Erratum | E7 |
| Published by Parallax | No |
| Found by | Found on the bench here, by a test built to measure something else |
| Confirmed on silicon | Yes — 2026-09-25, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes — 2026-09-26, on a P2 board at 200 MHz, run once; a rule at each use: at least 16 clocks from the start of the no-wait `RDFAST` to the start of the blocking one |
| Affects | a blocking `RDFAST` issued 8 to 15 clocks after a no-wait `RDFAST`, at the one spacing its hub alignment selects: the next `RFLONG` returns `$0000_0000`. Tested in cog execution, with `RFLONG` as the read |
| Test program | `e7-rdfast-blocking-after-no-wait-test.spin2`; the workaround: `e7-workaround-rdfast-spacing-test.spin2` |


# Appendix A: The Test Programs {#app-a}

Every erratum in this manual was confirmed on silicon by a test program, and every workaround it prints ran on silicon inside a test program. Each program is in the examples archive. They are the programs that ran, prepared for readers: each carries a new file header, and internal labels in its comments and in its printed output are replaced with the erratum they refer to. Every measuring routine assembles to the same bytes as the program that ran. The Spin2 code in cog 0 that starts each run, checks its controls and prints the results was brought to the Spin2 authoring guide, so some printed labels and hub addresses differ from the original run. The archive copies themselves were run on P2 hardware on 2026-09-26, and every value the programs analyse, every class and every verdict matched the original runs. Beyond labels, hub addresses and counter timestamps, two things differed, as they differ between any two runs: the E6 test's count of the running ADC's toggles, and the SINC2 test's two deliberately jittered arms. One start-up sample, which the SINC2 test excludes from its analysis (the first sample of its first `XZERO` arm), read differently from both original runs; the cause is not yet known.

## What each program decides {#sec-a-list}

The erratum tests decide whether the defect is present. The workaround tests run the block that *A proven workaround* prints, byte for byte, and each also reproduces the erratum in the same run, so that a clean result cannot come from a test that is unable to see the defect. The workarounds for E1, E2 and E6 are arms of the erratum test itself.

| Erratum | File | What it decides |
|---|---|---|
| E1 | `e1-setq-block-pointer-step-test.spin2` | the `PTRx` step of a `SETQ`/`SETQ2` block transfer with and without an `ALTD` between them, for six transfer forms, with three single-long references; its control arms are the workaround |
| E2 | `e2-altx-takes-pending-augs-test.spin2` | whether an immediate-`#S` `ALTD` or `ALTR` between `AUGS` and its target takes the augment; the register-`S` workaround; `AUGD` across an immediate-`S` `ALTS` |
| E3 | `e3-getct-stale-upper-long-runA.spin2` | the upper long `GETCT WC` returns in cogs 4-7 after that group has missed one wrap, and after it has missed two |
| E3 | `e3-getct-stale-upper-long-runB.spin2` | the same readings with a cog of cogs 4-7 running from the start |
| E3 | `e3-workaround-keeper-cog-test.spin2` | the workaround: with the keeper cog started first, whether cogs of 4-7 started after one and after two wraps read the current upper long; then, with the keeper stopped, that the erratum returns |
| E4 | `e4-getxacc-clear-gating-test.spin2` | whether `GETXACC` clears the accumulators with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst |
| E5 | `e5-goertzel-one-clock-lag-test.spin2` | how many terms a reading after a Goertzel burst holds, and where the last term goes |
| E5 (scope) | `e5-goertzel-sinc2-iteration-count-test.spin2` | not an erratum test: the documented SINC2 constraint that E5's workaround does not cover; which samples a varying iteration count corrupts, whether one clock of read jitter does the same, and whether `XZERO` or a constant count keeps every sample clean |
| E4, E5 | `e4-e5-workaround-read-sums-test.spin2` | the workaround: whether the `burst_sums` helper routine returns exactly *N* terms for bursts of 1 to 1001 clocks, back to back, at both input levels; alongside, the uncorrected reads that show both errata |
| E6 | `e6-dac-mode-adc-enable-test.spin2` | whether raising `OUT` runs the ADC in a DAC smart-pin mode with `TT` = `%00` and with `TT` = `%01`; the `TT` = `%01` word is the workaround |
| E7 | `e7-rdfast-blocking-after-no-wait-test.spin2` | how many clocks a `RDFAST` needs before its first read, in every hub alignment, for blocking and no-wait `RDFAST` and `WRFAST`, and what a blocking `RDFAST` does when issued while a no-wait one is still arming |
| E7 | `e7-workaround-rdfast-spacing-test.spin2` | the workaround: whether the printed `WAITX` line between the two `RDFAST`s gives a correct first read in every hub alignment; alongside, the unspaced sweep that shows the erratum |

## How they are built and run {#sec-a-run}

Every program shares one construction:

- **One file each.** Spin2 in cog 0; the measurement itself is PASM2 in a cog of its own, started by `COGINIT`.
- **The debugger stays out of the measurement.** `DEBUG_COGS = %0000_0001` confines the debug interrupt to cog 0, which only collects the results from hub RAM and prints them.
- **Controls before verdicts.** Each program checks its controls first. If any control fails, it prints a `RIG FAIL` line and no verdict.
- **Outcomes written in advance.** The result each program would print if the erratum were present, and if it were absent, is written into the program before it runs.
- **Raw values printed.** Every measured value is printed, not only the verdict, so the verdict can be re-derived from the output.

To run one:

1. Compile with DEBUG enabled: `pnut-ts -d <file>.spin2` (or PNut with DEBUG).
2. Download to RAM on a bare P2 board, with a reset. The E3 programs check that the counter starts from zero, so the download must reset the part.
3. Watch the DEBUG terminal. The program ends with its verdict line.

Pin use: the E4 and E5 programs, including the SINC2 test and the E4/E5 workaround test, drive P3 from the measuring cog, so P3 must be free. The E6 test drives P4 and reads it through P5, so both must be free and unconnected. The others use no pins.

Running time: the E3 erratum programs wait for the counter's lower long to wrap, which takes 2^32^ clocks (21.47 s at 200 MHz); Run A ends about 105 s after reset and Run B about 44 s after reset. The E7 erratum test printed its output over about 23 s, the SINC2 test over about 5 s. The E1, E2, E4, E5 and E6 erratum programs each printed their whole output in about one second. Of the workaround tests, the E3 test ends about 67 s after reset, since it waits through three wraps; the E7 test printed its output over about 8 s, and the E4/E5 test in about one second.

The E1 to E5 erratum programs ran on 2026-09-24 on a P2 board at 200 MHz, each twice, from two builds with identical measuring code, and every measured value matched between the runs. The E5 SINC2, E6 and E7 erratum programs ran on 2026-09-25, each twice. The three workaround tests ran on 2026-09-26, once each, on the same board at 200 MHz; each reproduced its erratum and passed every control in the same run.


