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
{\Large\itshape Silicon Defects of the Propeller 2 Found So Far, Proven on Real Parts\par}
\vspace{0.35cm}
{\large September 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 0.1.0\par}
\vspace{0.25cm}
{\large\bfseries\color{red!70!black} Community Review Draft \textperiodcentered\ Build 2026-09-25\par}

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
\end{itemize}
\vspace{0.05cm}
Each erratum: what the design says, what the part does, the symptom, the workaround,
why it happens, and how it was proven on a real P2.
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

**The clean-room design study** for predicting errata E3, E4 and E5 from the design material alone, and for the classification of findings this manual follows. The study read the design without Parallax's documentation or a bench; the predictions were then tested on real parts, independently, for this manual.

## Sources

- **Parallax Propeller 2 Documentation v35 (Rev B/C)** (Chip Gracey, Parallax Inc.): what the design says, including its KNOWN BUGS section.
- **Tests on real P2 parts** (P2 Knowledge Base Project): every erratum in this manual was confirmed on silicon by a test program that is included in the examples archive.
- **P2 Knowledge Base YAML** (Iron Sheep Productions / P2 Knowledge Base Project): instruction semantics and encodings.

## About This Draft

This is a **community review draft**. Its errata are confirmed on silicon; its wording, its structure and its explanations are open for review. Further behaviours are on the bench now, and any that the tests show to be silicon errata will be added as E6 onward.

Erratum numbers are **permanent**. A number is never reused or reassigned, so E3 means the same defect in every edition.

## What Counts as an Erratum

Every finding describes something the P2 does when a program runs, and each belongs to exactly one of three classes. What decides the class is what the chip's own design material says, not how bad the effect is.

| Class | Definition |
|---|---|
| **Silicon erratum** | The part does not do what its own design says it should. |
| **Anti-pattern** | Legal code that does something other than what it appears to do. |
| **Open question** | The delivered material cannot settle it. |

**This manual lists silicon errata only.** For an erratum there has to be a specific written statement of intent, in the design or in Parallax's published documentation, that the part contradicts on a real chip. Anti-patterns are documented, with their safe forms, in the companion manual *P2 Anti-Patterns*. An open question is published as neither.

The list is open-ended. These are the silicon errata **found so far**.

## How Each Chapter Is Built

Chapter *N* describes erratum E*N*. Every chapter has the same sections, in the same order:

| Section | What it gives |
|---|---|
| **What the design says** | the written statement the part contradicts, and where it is written |
| **What the part does** | the defect, stated precisely |
| **The symptom** | what the defect looks like in a program, and what it does not affect |
| **The workaround** | how to write around it, with code, and whether the workaround was proven on silicon |
| **Why it happens** | the mechanism, at the level of the programmer's model |
| **How it was proven** | the test on real silicon, its controls, and the measured values |
| **The test program** | a walkthrough of the test, and its filename in the examples archive |
| **Status** | who published it, who found it, what is confirmed, and what it affects |

## Summary

| E | Erratum | Affects | Published by Parallax | Workaround |
|---|---|---|:--:|---|
| **E1** | SETQ Block Transfers Lose Their Pointer Step | `SETQ`/`SETQ2` block `RDLONG`/`WRLONG`/`WMLONG` with a `PTRx` expression, when an `ALTx`, `AUGS` or `AUGD` sits between them | Yes | Keep `SETQ` adjacent to the transfer |
| **E2** | An Immediate ALTx Takes a Pending AUGS | an `ALTx` with an immediate `#S` between `AUGS` and its target | Yes | Give the `ALTx` a register `S` |
| **E3** | GETCT Returns a Stale Upper Long | `GETCT WC` in a cog group that had no cog running when the counter's lower long wrapped | No | Keep a cog of the group running from before the first wrap |
| **E4** | GETXACC Clears Only During a Goertzel Burst | `GETXACC` while the streamer is idle or in any mode other than Goertzel | No | Read with the streamer idle before and after the burst, and subtract |
| **E5** | The Goertzel Accumulators Trail by One Clock | every Goertzel burst: its last term is added to the next burst | No | End each burst with a short zero-term burst before reading |

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


# Chapter 1: SETQ Block Transfers Lose Their Pointer Step {#ch-e1}

When an `ALTD` sits between a `SETQ` or `SETQ2` and the block `RDLONG` or `WRLONG` it prepares, and that transfer uses a `PTRx` update expression such as `ptra++`, the whole block still moves, to or from the registers the `ALTD` selects, but `PTRx` changes by the step the expression gives a single long instead of by the size of the block. After `setq #3`, `altd` and `rdlong 0-0, ptra++`, `PTRA` has advanced by 4 bytes, not 16. Parallax lists this defect, for `ALTx`, `AUGS` and `AUGD`, among the known bugs in the P2 Documentation; it was confirmed on silicon here with `ALTD` as the intervening instruction.

## What the design says {#sec-e1-design}

A `SETQ` or `SETQ2` placed before `RDLONG`, `WRLONG` or `WMLONG` turns that instruction into a fast block move. The P2 Documentation, in its section *FAST BLOCK MOVES*, states what a `PTRx` expression does in a block move:

> For fast block moves, PTRx expressions cannot have arbitrary index values, since the index will be overridden with the number of longs, with bit 4 of the encoded index value serving as the `++`/`--` indicator.

Its example for `SETQ #x` followed by `RDLONG first_reg,PTRA++` reads x+1 longs from `PTRA` and gives the update as `PTRA += (x+1)*4`: the pointer moves past the whole block. Outside a block move, the same document defines a `PTRx` update as `PTRx += INDEX*SCALE`, where `SCALE` is 4 for `RDLONG`, `WRLONG` and `WMLONG`. A plain `ptra++` therefore moves `PTRA` by 4, and `ptra++[3]` moves it by 12.

The P2 Documentation records the departure from the block rule in its KNOWN BUGS section:

> Intervening ALTx/​AUGS/​AUGD instructions between SETQ/​SETQ2 and RDLONG/​WRLONG/​WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas. The expected number of longs will transfer, but PTRx will only be modified according to normal PTRx expression behavior:

The example that follows loads 16 longs with `SETQ #16-1`, alters the start register with `ALTD start_reg`, and issues `RDLONG 0,ptra++`. Its comment gives the result: `ptra` is incremented by 4 (1 long), not by 16*4.

## What the part does {#sec-e1-part}

With an `ALTD` between `SETQ` or `SETQ2` and a block `RDLONG` or `WRLONG` that carries a post-increment `PTRx` expression, one instruction does two things:

- **The transfer completes as written, and the redirect holds.** The number of longs set by `SETQ` or `SETQ2` moves, to or from the registers the `ALTD` selects. The block is read from, or written to, the hub address `PTRx` held before the instruction.
- **`PTRx` takes the plain expression's step.** The pointer changes by the amount the same expression gives without a `SETQ`: +4 for `ptra++` and `ptrb++`, +12 for `ptra++[3]`. The step does not depend on the block length. An 8-long block moved `PTRA` by +4, the same as a 4-long block.

This held for every form tested: `SETQ` with `RDLONG` into cog registers at 4 and at 8 longs, `SETQ2` with `RDLONG` into lookup RAM, and `SETQ` with `WRLONG` from cog registers, through `PTRA` and through `PTRB`, with `ptra++` and with `ptra++[3]`. The measured values are in *How it was proven*.

The confirmation is narrower than Parallax's statement. **Only `ALTD` was tested as the intervening instruction; Parallax names `ALTx`, `AUGS` and `AUGD`.** `WMLONG`, `SETQ2` with `WRLONG`, and the decrement and pre-modify forms (`ptra--`, `++ptra`, `--ptra`) were not tested. In the pre-modify forms the expression also sets the hub address the block starts from, so what the part does with that address under this erratum is not established here.

An `ALTD` on its own does not disturb the pointer. A single `RDLONG` with `ptra++`, redirected by `ALTD` and with no `SETQ` before it, moved `PTRA` by +4, as it does without the `ALTD`.

## The symptom {#sec-e1-symptom}

The data is right and the pointer is not. Every long of the block lands where the `ALTD` sends it, the longs on either side of the block are untouched, and the hub side of the transfer starts at the address `PTRx` held. Only the value left in `PTRx` differs: after a 4-long block through `ptra++`, `PTRA` points 4 bytes past the start of the block instead of 16.

The effect appears at the next access through that pointer. A loop that walks a hub buffer block by block with `SETQ`, `ALTD` and `RDLONG ..., ptra++` starts each block 4 bytes after the start of the previous one, not after its end: the reads return overlapping data. The same loop built on `WRLONG` writes each block over all but the first long of the block before it. Any address computed from `PTRx` after the transfer carries the same error. A transfer whose pointer is reloaded before the next use is not affected.

## The workaround {#sec-e1-workaround}

**Keep `SETQ` or `SETQ2` immediately before the transfer.** With nothing between them, the pointer takes the full block step. This is the form of every control in the test program, and it is proven on silicon: `PTRA` advanced by +16 for 4 longs and by +32 for 8 longs, `PTRB`, `SETQ2` into lookup RAM and `WRLONG` each advanced by +16 for 4 longs, and `ptra++[3]` advanced by +16 for 4 longs, as the block rule states.

```pasm2
        setq    #NLONGS - 1         ' block of NLONGS longs
        rdlong  buf, ptra++         ' PTRA += NLONGS * 4
```

The cost is the redirect. Without an `ALTD`, the first register of the block is the one named in the instruction's `D` field. No workaround that keeps the redirect has been tested on silicon yet.

## Why it happens {#sec-e1-why}

A block transfer depends on the cog knowing that a `SETQ` or `SETQ2` came before it, and the cog keeps that knowledge in two forms.

The first form is held across an intervening `ALTx`, `AUGS` or `AUGD`, so that those instructions can sit between a `SETQ` and the transfer it prepares. The transfer takes its long count from this held form, which is why the full block still moves.

The pointer update does not use the held form. It asks only whether the instruction immediately before the `RDLONG`, `WRLONG` or `WMLONG` was a `SETQ` or `SETQ2`. With an `ALTD` in that position the answer is no, so the pointer is updated as for a single-long access: by the index encoded in the `PTRx` expression, times 4. For `ptra++` the index is 1, giving 4; for `ptra++[3]` it is 3, giving 12.

By the same reasoning an `AUGS` or `AUGD` in that position also breaks the adjacency the pointer update looks for. The test program did not exercise them.

## How it was proven {#sec-e1-proof}

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

In the `wrlong` row, the four longs that reached hub RAM are the ones in the registers the `ALTD` selected. The single-long references read +4 for `rdlong ..., ptra++`, +4 for the same instruction redirected by `ALTD`, and +12 for `rdlong ..., ptra++[3]`.

Every round of every arm gave the same value. In every arm the trap region was untouched: it held the sentinel after each read arm, and the write arm's trap registers kept their initial values `$7E7E_0000` + *k*. For the first row, round 0 printed `before=$0000_23C8 after=$0000_23D8 delta=16` for the control and `before=$0000_23C8 after=$0000_23CC delta=4` for the hazard arm, with `$A5A0_0004` to `$A5A0_0007` in destination slots 2 to 5 in both.

The test was run twice on 2026-09-24, from two builds of the program: as first written, and after a style revision that left the measuring code unchanged. The hub addresses differ between the builds (the read arms' pointer started at `$0000_23B8` in the first run and `$0000_23C8` in the second), and every pointer change and every data result matched. The values above are read from the per-round raw lines, not from the program's own verdict line.

## The test program {#sec-e1-program}

The test program is `e1-setq-block-pointer-step-test.spin2` in the examples archive. Its measuring cog is one PASM routine that runs the 15 arms in sequence. Each arm has the same frame: `prep_cog` refills the destination region `dst` and the trap region `trp` with the sentinel; the pointer is loaded from `c_rsrc`, the hub address of source long 4; `c_before` and `c_after` capture the pointer around the transfer; and `dump_cog` writes the pointer pair and both regions to a record in hub RAM.

The control for the primary pair, `SETQ` directly before `RDLONG`:

```pasm2
                call    #prep_cog
                mov     ptra, c_rsrc
                mov     c_before, ptra
                setq    #4 - 1
                rdlong  dst + 2, ptra++
                mov     c_after, ptra
                call    #dump_cog
```

The hazard arm places the `ALTD` between them. Its `RDLONG` names the trap region, `trp + 2`; the register `c_hidx` holds the address `dst + 2`, so a working `ALTD` sends the block to the same registers the control uses:

```pasm2
'--- arm 3  H_BLK4 : PRIMARY hazard -- SETQ / ALTD / RDLONG ptra++
                call    #prep_cog
                mov     ptra, c_rsrc
                mov     c_before, ptra
                setq    #4 - 1
                altd    c_hidx
                rdlong  trp + 2, ptra++
                mov     c_after, ptra
                call    #dump_cog
```

The other arms follow the same frame: `setq #8 - 1` for the 8-long pair, `ptra++[3]` and `ptrb++` for the index and pointer pairs, `wrlong` from the cog registers `wsrc` with the trap `wtrp` for the write pair, and `setq2` into lookup RAM for the last pair. In the listing the three instructions of every hazard arm are consecutive longs, so nothing else sits between the `SETQ`, the `ALTD` and the transfer.

Cog 0 computes each arm's pointer change from the record:

```spin2
PRI delta(armIdx, rp) : deltaVal | pRec
  pRec := recaddr(armIdx, rp)
  deltaVal := long[pRec][1] - long[pRec][0]
```

For every arm and round the program prints the pointer before and after, the change, a data class (`FULL` when the block is complete and correctly placed and both regions are otherwise untouched), and the raw contents of both regions. It then prints one line confirming that every control passed, one verdict line per hazard arm, and the verdict for the primary pair last. The program runs once, in well under a second, from RAM with DEBUG enabled; its output is on the DEBUG terminal.

## Status {#sec-e1-status}

| Field | Content |
|---|---|
| Erratum | E1 |
| Published by Parallax | Yes, *P2 Documentation*, KNOWN BUGS |
| Found by | Parallax |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes, for `SETQ`/`SETQ2` directly before the transfer |
| Affects | a `SETQ`/`SETQ2` block `RDLONG`/`WRLONG`/`WMLONG` with a `PTRx` update expression, when an `ALTx`, `AUGS` or `AUGD` sits between them (confirmed with `ALTD`) |
| Test program | `e1-setq-block-pointer-step-test.spin2` |


# Chapter 2: An Immediate ALTx Takes a Pending AUGS {#ch-e2}

An `ALTx` instruction written with an immediate `#S`, placed between an `AUGS` and the
instruction the `AUGS` was written for, uses the augment for its own `S` and does not
cancel it, so the intended target receives the augment as well. The augment's bits 17:9
become the `ALTx`'s auto-increment, and the `ALTx`'s `D` register moves by that amount.
Giving the `ALTx` a register `S` avoids the defect; that workaround is confirmed on
silicon.

## What the design says {#sec-e2-what-the-design-says}

An `AUGS` holds 23 bits for the next instruction that carries a literal `#S`. That
instruction takes them as bits 31:9 of its `S`, keeps its own 9-bit field as bits 8:0,
and the augment is cancelled. The `ALTx` instructions take part in this by design: their
`S` may be a register, a 9-bit literal or an augmented literal, and it is read as two
fields, a base in `S[8:0]` and a signed auto-increment in `S[17:9]` that is added to the
`ALTx`'s `D` register after the `ALTx` executes.

Parallax publishes the defect in the *P2 Documentation*, under KNOWN BUGS:

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

## What the part does {#sec-e2-what-the-part-does}

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

## The symptom {#sec-e2-the-symptom}

The `ALTx`'s `D` register changes when the program expects it to stay put. A 9-bit
immediate `#S` has bits 17:9 clear, so an immediate-`S` `ALTx` on its own has an
auto-increment of 0; in this arrangement it takes bits 17:9 of the augment instead. Any
later instruction that uses that register, such as the next pass of a loop that indexes
with it, sees the moved value.

What does not go wrong, in the tested cases:

- The instruction after the `ALTx` is redirected to the register the program names.
- The target receives the full augmented value.
- No other register in a 32-register window around the target was written.

The size of the move is set by bits 17:9 of the augment, which the documented field
split makes the auto-increment; by that split, an augment whose bits 17:9 are zero moves
nothing. The only value measured was 5.

The `##` literal syntax does not by itself produce this arrangement: the assembler places
the `AUGS` immediately before the instruction that carries the `##`. The arrangement
arises when an `AUGS` is written explicitly and an `ALTx` is placed between it and its
target, as in Parallax's example.

## The workaround {#sec-e2-the-workaround}

Give the intervening `ALTx` a register `S`, as Parallax's statement directs. The base,
and any auto-increment, go in a register:

```pasm2
                augs    #$3C5C_0A55     ' meant for the MOV below
                altd    idx, rbase      ' S from a register: no augment
                mov     0-0, #$055      ' table[idx] := $3C5C_0A55
                jmp     #$

rbase           long    table           ' S[8:0] = table, S[17:9] = 0
idx             long    3               ' index into table
table           long    0[8]
```

With a register `S`, the `ALTD` has no immediate `S` for the `AUGS` to augment; `idx`
is left as it was, and the augment reaches the `MOV`.

**Confirmed on silicon.** The test program runs the same arrangement with a register
holding 4 as the `ALTD`'s `S`: the `MOV` was redirected four registers along, to
`win[12]`, which received `$3C5C_0A55`, and `idx` did not move. The snippet above was
compiled with `pnut-ts` 1.55.8, not run; it differs from the tested arrangement only in
its register names and base value.

**The one-operand form is not a register form.** `ALTD idx` assembles to the same
instruction word as `ALTD idx,#0`: immediate bit set, `S` = 0. That is the arrangement
the test showed affected. The one-operand form of every `ALTx` instruction is encoded
with the immediate bit set, so none of them is a workaround.

## Why it happens {#sec-e2-why-it-happens}

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

The damage is confined to the auto-increment because of how an `ALTx` reads its `S`.
The augment supplies bits 31:9 and leaves bits 8:0 alone. Bits 8:0 are the base, so the
redirection is unaffected. Bits 17:9 are the auto-increment, so the `D` register moves.

`AUGD` is the corresponding mechanism for a literal `#D`. The `ALTx` instructions have
no immediate form for `D`: their encodings carry an immediate bit for `S` only, and
their `D` is always a register. An `ALTx` therefore has no immediate `D` to receive a
pending `AUGD`, and the `AUGD` passes to its target.

## How it was proven {#sec-e2-how-it-was-proven}

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
field an augment of `$3C5C_0A55` would fill. A5 is the workaround. A6 and A7 are the defect: the
`ALTx` moved `idx` by 5, and the target still wrote `$3C5C_0A55`.

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
was read back from the assembler listing and its encoding confirmed; the program's
header records each word. The `AUGS` assembled to `$FF1E2E05`.

## The test program {#sec-e2-the-test-program}

The test program is `e2-altx-takes-pending-augs-test.spin2`, a single Spin2 file that
runs the measuring cog in PASM and prints its results with `debug()`. Compile it with
DEBUG enabled (`pnut-ts -d`, or PNut) and run it with the debug terminal open; it prints
about 40 lines and ends in one `VERDICT:` line, or a `RIG FAIL:` line and no verdict if
any control is wrong.

The augment is chosen so that its two fields can be told apart:

```spin2
  AUGV       = $3C5C_0A55          ' AUGS payload: [17:9] = 5, [8:0] = $055
  LO         = AUGV & $1FF         ' $055 = the target's own 9-bit #S
  AUTOINC    = (AUGV >> 9) & $1FF  ' 5 (bit 8 clear -> +5 after sign-extend)
```

The workaround arm and the `ALTD` test arm differ only in the form of the `ALTD`'s `S`.
Each arm fills the window, runs its sequence, and dumps the window and `idx` to hub RAM:

```pasm2
' ---- A5 ctrl: WORKAROUND -- register-S ALTD between AUGS and target ----
                mov     armn, #5
                call    #fill
                augs    #AUGV
                altd    idx, sreg4
                mov     0-0, #LO
                call    #dump

' ---- A6 TEST: immediate-#S ALTD between AUGS and target ----
                mov     armn, #6
                call    #fill
                augs    #AUGV
                altd    idx, #0
                mov     0-0, #LO
                call    #dump
```

The two register `S` values used by the controls hold the auto-increment and the base
in their separate fields:

```pasm2
sinc            long    AUTOINC << 9     ' register S: base 0, auto-index +5
sreg4           long    S4               ' register S: base 4, auto-index 0
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
| Workaround proven on silicon | Yes |
| Affects | an `ALTx` with an immediate `#S` between `AUGS` and its target; tested with `ALTD` and `ALTR` |
| Test program | `e2-altx-takes-pending-augs-test.spin2` |


# Chapter 3: GETCT Returns a Stale Upper Long {#ch-e3}

`GETCT WC` reads the upper long of the 64-bit system counter from a copy kept
by the reading cog's group of four cogs, and that copy advances at a wrap of the
lower long only if a cog of the group is running at the wrap. A cog started in a
group that had no running cog at one or more wraps reads an upper long that is
behind by one for each wrap missed, while plain `GETCT` returns a current lower
long. From reset only cog 0 runs, so the first cog a program starts among cogs
4-7 reads a stale upper long if it starts after the first wrap, 2^32^ clocks
after reset (21.47 s at 200 MHz).

## What the design says {#sec-e3-design}

The P2 Documentation, in its list of what the hub provides the cogs, describes
one counter:

> 64-bit free-running counter which increments every clock, cleared on reset

Its list of the improvements made to the chip states how a cog reads the upper
half of that counter:

> System counter extended to 64 bits. GETCT WC retrieves upper 32-bits.

and its description of the counter events names the lower half:

> Event 1 = CT passed CT1 (CT is the lower 32-bits of the free-running 64-bit global counter)

The documentation describes a single counter. It does not qualify the value
`GETCT WC` returns by cog number, or by which other cogs are running.

## What the part does {#sec-e3-part}

The eight cogs form two groups of four: cogs 0-3 and cogs 4-7. `GETCT` does not
read the counter itself; each group reads its own copy of the counter's two
longs, and the two halves of that copy behave differently.

- **The lower long is current.** In every pair the test took, including every
  pair in which the upper long was stale, the lower long a sampling cog read
  with plain `GETCT` lay between cog 0's own lower-long reads taken just before
  and just after it.
- **The upper long advances at a wrap of the lower long only while at least one
  cog of the group is running.** A group with no running cog at a wrap keeps its
  previous upper long.

Measured on cog 4, in the cogs 4-7 group, against cog 0 and cog 1 in the cogs
0-3 group:

- A cog started in a group that missed wraps reads an upper long behind cog 0's
  by the number of wraps missed. Cog 4, first started after its group had
  missed one wrap, read 1 behind; started again after its group had missed two
  more, it read 2 behind.
- Starting a cog does not bring its group's upper long up to date. The reading
  taken just after the start was already behind, and a reading late in the same
  2^32^-clock span was behind by the same amount.
- The first wrap the group runs through restores the correct value in one step.
  Cog 4, 1 behind, ran through the next wrap and then read the same upper long
  as cog 0.
- A group whose only running cog stops is exposed again. Cog 4 was stopped after
  it had caught up; its group then missed two wraps with no cog running, and cog
  4, started again, read 2 behind.

At reset only cog 0 runs, so the cogs 4-7 group has no running cog until the
program starts one, and its upper long stays at zero through every wrap until
then. The first wrap comes 2^32^ clocks after reset: 21.47 s at 200 MHz.

The defect was confirmed at 200 MHz, for one and for two missed wraps. The test
sampled cog 1 and cog 4; the other cogs of each group were not sampled
separately, and the cogs 0-3 group was not tested with every one of its cogs
stopped.

## The symptom {#sec-e3-symptom}

In a cog of a group that missed wraps, `GETCT WC` followed by `GETCT` yields a
64-bit time that is short by 2^32^ clocks for each wrap missed. In one pair of
the test, cog 0 read its own counter immediately before and immediately after
cog 4 read:

| Read by | Upper long (`GETCT WC`) | Lower long (`GETCT`) |
|---|---|---|
| cog 0, before | `$0000_0001` | `$1020_DB39` |
| cog 4 | `$0000_0000` | `$1020_DB59` |
| cog 0, after | `$0000_0001` | `$1020_DBA1` |

The three lower longs are in order; the upper long is one behind, a gap of 2^32^
clocks, which is 21.47 s at 200 MHz.

In a program this shows up in two ways:

- A 64-bit time stamp taken in the stale cog and one taken in a cog of an
  up-to-date group disagree by 2^32^ clocks for each wrap missed.
- The stale cog's upper long advances by more than one at the next wrap it runs
  through, as its group's copy catches up. Cog 4 read `$0000_0000_$E013_C141`
  late in one span and `$0000_0002_$1001_4D69` early in the next: its upper long
  went from 0 to 2 across one wrap. A 64-bit interval that cog times across that
  wrap includes 2^32^ clocks that did not pass, one for the wrap its group had
  missed.

What does not go wrong:

- Plain `GETCT` returned a current lower long in every pair of every reading, in
  both groups.
- A cog of a group that had a running cog at every wrap read the same upper long
  as cog 0: cog 1 in every reading of both runs, and cog 4 throughout the run in
  which it ran from the start of the program.
- The stale value is steady. All ten pairs of each reading agreed, early and
  late in the span.
- Before the first wrap the correct upper long is zero, and a group's copy
  starts from zero at reset, so a program that has run for fewer than 2^32^
  clocks since reset is not exposed.
- Only `GETCT` was exercised. The counter events, which the documentation
  defines on the lower long, were not tested.

## The workaround {#sec-e3-workaround}

Keep at least one cog of each group the program uses running from before the
first wrap, 2^32^ clocks after reset (21.47 s at 200 MHz), and do not let every
cog of that group stop afterward. Cogs 0-3 are covered for as long as cog 0,
which runs from reset, keeps running. For cogs 4-7, start the cog there at the
beginning of the program and do not stop it:

```spin2
PUB main()
  ' start the cog that reads the counter in cogs 4-7 at once,
  ' before 2^32 clocks have run, and never stop it
  coginit(4, @worker, 0)

DAT
                org
worker          getct   hi      wc      ' upper long: current
                getct   lo              ' lower long
                ' ... the cog's work ...
                jmp     #worker
hi              res     1
lo              res     1
```

The workaround is proven on silicon. In the second test program (Run B, under
*How it was proven*), cog 4 was started at the beginning of the program, while the lower long read `$00DB_96FF`, and kept
running; its upper long matched cog 0's before the first wrap, early and late
after it, and after the second wrap.

What the proof covers: the cog kept running was the cog that read the counter,
held in a polling loop. Two variants follow from the same group rule but were
not tested on silicon: a separate cog held running only to keep its group
current while other cogs of the group are started and stopped, and reading the
upper long in a cog of cogs 0-3 and passing it to cogs 4-7 through hub RAM.

## Why it happens {#sec-e3-why}

The P2 has one 64-bit counter, but a cog does not read it directly. Each group
of four cogs holds its own copy of the counter's two longs, and `GETCT` reads
the group's copy: the lower long without `WC`, the upper long with it. The group
refreshes the two halves of its copy on different schedules.

The lower half is refreshed on every clock on which any cog of the group is
running. If the group has been idle, the first clock on which one of its cogs
runs brings the lower half up to date, so a newly started cog reads a current
lower long.

The upper half is refreshed only once in 2^32^ clocks, at the wrap of the lower
long, and only if a cog of the group is running at that moment. Nothing else
refreshes it: not a cog start, and not the clocks that pass between wraps. A
group with no running cog at a wrap keeps its previous upper long. At the next
wrap it runs through, it takes the counter's upper long as it is then, which is
why the error closes in a single step rather than shrinking by one.

The counter and both groups' copies start from zero at reset, and at reset only
cog 0 runs. The cogs 0-3 group therefore refreshes at every wrap from the start,
for as long as cog 0 runs; the cogs 4-7 group refreshes at none until a program
starts a cog there.

Running here means the state a cog is in between its start and its stop, the
state `COGCHK` reports. In the design, what a running cog is executing does not
enter into it; the test kept its cogs in a polling loop and did not try a cog
held in a wait instruction such as `WAITX`.

## How it was proven {#sec-e3-proof}

Two programs, Run A and Run B, were each downloaded to RAM with a chip reset and
run on a bare P2 board at 200 MHz, with the debugger confined to cog 0. Each was run twice, from two builds: as first written, and with its
comments and layout conformed to house style and its measuring code unchanged.
Every D value and every verdict matched between the two builds.

**Arrangement.** Cog 0 is the reference. Cog 1, in the cogs 0-3 group, and cog 4,
in the cogs 4-7 group, run the same sampler: on each new request from cog 0 it
executes `GETCT WC` then `GETCT`, writes both longs to hub RAM, then writes an
acknowledgment. One **pair** is taken as follows: cog 0 reads its own counter
(`GETCT WC`, `GETCT`), writes a request, waits for the acknowledgment, reads the
sampler's two longs, and reads its own counter again. The sampler's reads
therefore fall between cog 0's two reads.

- A pair counts only if cog 0's two upper longs agree and all three lower longs
  lie between `$1000_0000` and `$F000_0000`, clear of any wrap.
- **D** is cog 0's upper long minus the sampler's upper long.
- Each pair also checks that the sampler's lower long lies strictly between cog
  0's two lower longs.
- A reading is ten counted pairs, and all ten must give the same D.

**Controls.** Any failure stops the run with no verdict.

- Cog 1, running from the start of the program, must give D = 0 in every
  reading.
- Cog 0's own upper long must equal the number of wraps of its lower long that
  cog 0 has watched since reset, checked on every poll.
- The set of running cogs, polled throughout every wait, must be exactly the
  cogs the program started; in Run A, no cog of 4-7 may run before cog 4 is
  started.
- At start the upper long must read 0 and only cog 0 may be running, which
  shows the download reset the part.
- Every request must be answered within 100 ms.

The expected D of every reading, for the defect present and for it absent, was
fixed in each program before the run.

**Run A** holds cogs 4-7 idle until cog 0's upper long reads 1, starts cog 4,
and reads it just after the start and again late in the same span. Cog 4 then
runs through the next wrap and is read again. Cog 4 is then stopped, its group
misses two wraps with no cog running, and cog 4 is started again and read just
after the restart and late in the span. **Run B** starts cog 4 at the beginning
of the program, beside cog 1, and reads it before the first wrap, early and late
after it, and after the second wrap.

Wrap *n* below is the wrap after which cog 0's upper long reads *n*. An early
reading is taken with the lower long past `$1000_0000`, a late one past
`$E000_0000`.

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

In every reading of both runs all ten pairs agreed on D, and the lower-long
check held in every pair. Each program's verdict line read `CONFIRMED`, in both
builds.

## The test program {#sec-e3-program}

The two files are `e3-getct-stale-upper-long-runA.spin2` (Run A) and
`e3-getct-stale-upper-long-runB.spin2` (Run B). They share the sampler, the
pair protocol and the controls, and differ only in when cog 4 starts and which
readings are taken.

The sampler is started explicitly in cog 1 and in cog 4 (`COGINIT #1` and
`COGINIT #4`), with its hub mailbox address in `PTRA`. On each new request
number it reads the counter and writes both longs:

```pasm2
sampler         mov     s_last, #0
s_loop          rdlong  s_req, ptra
                cmp     s_req, s_last   wz
        if_z    jmp     #s_loop
                mov     s_last, s_req
                getct   s_hi            wc      ' this group's UPPER copy
                getct   s_lo                    ' this group's LOWER copy
                wrlong  s_hi, ptra[1]
                wrlong  s_lo, ptra[2]
```

It then writes the request number back as its acknowledgment and returns to
`s_loop`. Cog 0's side of a pair, in the method `take_pair`, is inline PASM2 that
executes `GETCT WC` and `GETCT` before writing the request, and again after
seeing the acknowledgment and reading the sampler's two longs. From those six
longs each reading computes D and the lower-long check (`+<` is the unsigned
less-than):

```spin2
    dd := rhb - shi
    br := (rlb +< slo) and (slo +< rla)
    if not br
      rbf[slotIdx]++
```

Run A's defect step: cogs 4-7 stay idle while cog 0 waits for its upper long to
read 1, with the running-cog set polled throughout the wait; then cog 4 is
started and read, with cog 1 read beside it:

```spin2
  ' ---- hazard: group 1 idle across wrap 0->1 --------------------------
  debug("--- waiting for CT hi=1 with cogs 4-7 idle (~21 s) ---")
  wait_until(1, LOWIN, M_C1)
  start_cog4(@mb4)
  waitms(10)
  expect_mask(M_C1C4)
  debug("--- cog 4 started (first group-1 cog since reset) ---")
  reading(R_A1A, string("A1a cog4 hi=1"), @mb4)
  reading(R_C1A, string("C1a cog1 hi=1"), @mb1)
```

Later in the same file, `cogstop(4)` at upper long 2 and a second `start_cog4`
at upper long 4 take the two-missed-wrap readings.

Run B changes the arrangement in one place: both samplers start at the beginning
of the program.

```spin2
  ' ---- both samplers from program start: cog 1 (group 0), cog 4 (group 1)
  start_cog1(@mb1)
  start_cog4(@mb4)
  waitms(10)
  expect_mask(M_C1C4)
```

Each file prints every pair raw, a summary line per reading, and a one-line
verdict. Both are compiled with `pnut-ts` 1.55.8 with DEBUG enabled (`-d`) and
downloaded to RAM; the download must reset the part, since the program checks
that the counter starts from zero. Run A ends about 105 s after reset and Run B
about 44 s after reset.

## Status {#sec-e3-status}

| Field | Content |
|---|---|
| Erratum | E3 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes |
| Affects | `GETCT WC` in a cog of a four-cog group that had no running cog at one or more wraps of the lower long (measured on cogs 4-7); plain `GETCT` is not affected |
| Test program | `e3-getct-stale-upper-long-runA.spin2`, `e3-getct-stale-upper-long-runB.spin2` |


# Chapter 4: GETXACC Clears Only During a Goertzel Burst {#ch-e4}

`GETXACC` is documented to read the streamer's Goertzel cosine and sine accumulators and to
clear them. On the part, the clear takes effect only while a DDS/Goertzel streamer command is
running. With the streamer idle, or running the other streamer mode tested, `GETXACC` returns
the accumulators and leaves them unchanged, so each Goertzel burst adds to whatever earlier
bursts left behind. A reading taken after a burst measures that burst only when the reading
taken before it is subtracted.

## What the design says {#sec-e4-design}

The P2 Documentation states the clear in its streamer instruction table and again in its
description of the DDS/Goertzel mode. The instruction table's entry for `GETXACC` reads:

> Get Goertzel X into D and Y into next S, clear X and Y

The DDS/Goertzel mode description reads:

> After some number of complete NCO cycles, both accumulators can be simultaneously captured
> into holding registers and cleared using the GETXACC instruction. GETXACC writes the captured
> cosine accumulation into D and places the captured sine accumulation into the next
> instruction's S value. Subsequent GETXACC instructions will return the same values until a
> new streamer command executes.

The SINC1/SINC2 table that follows that description carries the column heading:

> Accumulations (SIN_ACC/COS_ACC are read and cleared by GETXACC)

None of the three places makes the clear depend on the streamer's mode or on whether a
streamer command is running.

## What the part does {#sec-e4-part}

In this chapter a *Goertzel burst* is one DDS/Goertzel streamer command for the clocks it
runs, and a *term* is the product the streamer adds to each accumulator on each of those
clocks.

- **Streamer idle.** `GETXACC` returns the current value of the accumulators and leaves them
  as they were. Repeated reads return the same value, bit for bit.
- **Streamer running another mode.** One other mode was tested: the immediate-to-pins mode,
  one pin wide, with its output disabled, started by `XINIT`. A `GETXACC` issued as the next
  instruction after that `XINIT`, and another issued 100 clocks later with the command still
  running, both returned the value from before the `XINIT` and cleared nothing.
- **A new Goertzel burst.** The burst adds its terms to the value the accumulators already
  hold. Starting a streamer command does not reset them.
- **During a Goertzel burst.** The clear acts. `GETXACC` returns everything accumulated so
  far, including what earlier bursts left, and the accumulation continues from the clear. The
  read plus the next read hold exactly what the same burst gives when it is not read: no term
  is lost and none is counted twice.

The sine accumulator behaved as the cosine accumulator did in every case measured.

## The symptom {#sec-e4-symptom}

A program that relies on the documented clear, issues one `GETXACC` after each burst, and
treats the reading as that burst's result gets a running total instead: each reading holds the
burst plus everything accumulated since the last clear. In one repetition of the test program,
the reading before a 256-clock burst was 14,823 and the reading after it was 30,378; the burst
itself contributed 15,555.

A `GETXACC` issued before an `XINIT` in order to zero the accumulators returns the running
total and zeroes nothing.

A `GETXACC` inside a Goertzel burst returns the leftover from earlier bursts together with the
part of the burst run so far. In the test program, a read 29 terms into a burst that started
from 17,080 returned 18,849.

What does not go wrong: the accumulation itself is exact. Every difference the test program
measured was a whole multiple of the per-clock term, the same burst gave the same difference
from every starting value, and a read inside a burst split it into two parts that sum
exactly to the unread burst. Consecutive idle reads return the same value, as the documentation
says they do.

## The workaround {#sec-e4-workaround}

**Measured on silicon.** Read the accumulators with the streamer idle immediately before the
burst and again after it has ended, and subtract. The test program did this for every burst it
scored. For a 256-clock burst the before-and-after difference was 15,555 in all eight
repetitions, from starting values of 976, 14,823, 12,871, 10,919 and 8,967.

```pasm2
' Per-burst sums: read idle before and after, take the difference
        getxacc x0                ' idle: the running total so far
        mov     y0, 0-0           ' sine arrives as this S value
        xinit   gmode, gsel       ' one Goertzel burst
        waitx   ##4000            ' wait until well past its end
        getxacc x1                ' idle again
        mov     y1, 0-0
        sub     x1, x0            ' cosine sum of this burst
        sub     y1, y0            ' sine sum of this burst

gmode   long    $F007_0100        ' Goertzel, SINC1, P0-P3, count 256
gsel    long    $0008_80A5        ' P3 inverted, summed; LUT offset $0A5
```

The values in `gmode` and `gsel` are the ones the test program used. The 4,000-clock wait is
also the test program's; the longest Goertzel burst it ran was 256 clocks, at an NCO frequency
of `$8000_0000`. The condition the measurement supports is that both reads fall outside the
burst; a longer burst needs a longer wait.

**Measured on silicon.** When a `GETXACC` does fall inside the burst, the burst's total is
still recoverable: the read inside the burst, minus the reading taken before the burst, plus
the reading taken after it, equalled the unread burst in every repetition.

The difference holds one term fewer than the burst has clocks. That is a separate erratum,
with its own workaround, in [Chapter 5](#ch-e5).

**Not tested:** SINC2 accumulation, more than one input pin, bursts started by `XZERO` or
`XCONT`, continuous `XCONT` loops, and accumulator values near the 32-bit limit. The largest
value any read returned in the runs was 36,600.

## Why it happens {#sec-e4-why}

The clean-room design study traces the behaviour to how the accumulators are updated. Each
accumulator is rewritten only on the clocks of a running DDS/Goertzel command; on every other
clock it holds its value, whatever instruction the cog executes. The clear in `GETXACC` is not
a separate action on the accumulator. It is folded into that same per-clock update: on the
clock the clear arrives, the update starts the accumulator over instead of adding to its old
value. When no update happens, because the streamer is idle or running a different mode, the
clear has nothing to act through, and the accumulator keeps its value.

The read does not depend on the update. `GETXACC` returns the accumulator's current value,
which is why idle reads repeat exactly and why a read inside a burst returns the running sum.
When the clear does act, the accumulator starts over from the one term that has been formed but
not yet added ([Chapter 5](#ch-e5)), and that term appears in the next reading. That is why a
read inside a burst and the read after it partition the burst exactly.

By the study's reading, every mode other than DDS/Goertzel behaves as the idle streamer does.
One such mode was tested.

## How it was proven {#sec-e4-proof}

The test program runs on a P2 board at 200 MHz with nothing connected to pins P0 to P7. One
cog, started from a `DAT` block, does all streamer work and issues every `GETXACC`; the
debugger is confined to cog 0, which only waits for the results and prints them. The measuring
cog drives P3 low as a plain output with its smart pin off, so the streamer's input bit for P3
holds a fixed level.

**Construction.** All 512 LUT longs hold `$173D_0000`, and the NCO frequency is `$8000_0000`.
Each Goertzel burst is an `XINIT` whose `D` is `$F007_0000` plus a count (SINC1, no DAC output,
input pins P0 to P3) and whose `S` is `$0008_80A5` (P3 inverted and summed, the other three
pins ignored). With P3 low, each active clock adds 61 to the cosine accumulator and 23 to the
sine accumulator. Every phase starts from the same preamble: an 8-clock Goertzel burst, a
4-clock burst whose terms are all zero (`S` of `$0008_00A5`), and an idle `GETXACC` whose value,
B, must be nonzero, so that a clear which wrongly acted would show.

**Controls**, all passed in both runs: the 512 LUT longs read back unchanged; P3 read at its
driven level at every check; `POLLXFI` reported the streamer finished after every wait and still
running at every read meant to fall inside a command; and a calibration pair of 64-clock bursts
moved the cosine accumulator by +3,843 with P3 low and by −3,843 with P3 high (63 × 61 each
way), which shows the term follows the pin and is a whole multiple of 61.

**Idle and non-Goertzel reads.** In each of eight repetitions, after the preamble: a read with
the streamer idle; an `XINIT` of `$4000_0400` (immediate-to-pins, one pin, output disabled,
count `$0400`) followed at once by a read; a read 100 clocks later, with that command
confirmed still running; and a read after it ended. Each of those reads, and the idle read
taken before each calibration burst and before each burst of the two runs below, was compared
with its preamble's B. All 50 reads equalled B bit for bit, and none returned zero. In the
first repetition, B and the four reads were all 488.

**Reads inside a burst.** Each repetition ran two 256-clock bursts, each after its own
preamble. Run A: an idle read P, the burst with no read inside it, a 4,000-clock wait, and a
read RA. Run B: the same, with one `GETXACC` issued a fixed `WAITX` delay after the `XINIT`
(read R1), and after the wait a read R2. The delays were 30 in the first four repetitions, then
62, 94, 126 and 190. The outcomes were fixed before the run: run B's R1 + R2 − P equal to run
A's RA − P confirms the partition; a result 61 short would mean the clear lost a term; 61 over,
that a term was counted twice; a difference equal to R1, that the clear did not act during the
burst.

Results for the first repetition:

| Quantity | Value | Terms of 61 |
|---|---|---|
| Run A: RA − P (16,531 − 976) | 15,555 | 255 |
| Run B: R1 − P (18,849 − 17,080) | 1,769 | 29 |
| Run B: R2 | 13,786 | 226 |
| Run B: R1 + R2 − P | 15,555 | 29 + 226 = 255 |

In all eight repetitions RA − P was 15,555 and R1 + R2 − P equalled it exactly, while the read
point moved from term 29 to term 189, one term behind the `WAITX` operand each time. R2 was
13,786 in each of the first four repetitions, although run B started from 17,080 in the first
and from 30,927 in the next three: the read inside the burst discarded everything before it.
The sine accumulator, recorded for information, moved on no idle read and split the same way
(5,865 in both runs of every repetition). That a 256-clock burst gives 255 terms is the lag of
[Chapter 5](#ch-e5).

The program was run twice on 2026-09-24, from two builds with identical measuring code; every
value printed was the same in both runs.

## The test program {#sec-e4-program}

The test program is `e4-getxacc-clear-gating-test.spin2`. Its measuring code is a `DAT`
block started by `COGINIT`; the Spin2 method `main` waits for it, prints every raw value, checks
the controls, and prints one verdict for the idle and non-Goertzel reads and one for the reads
inside a burst.

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
dlytab          long    30, 30, 30, 30, 62, 94, 126, 190
```

`dch_` and `dzero_` are the preamble's 8-clock and zero-term bursts, `dcal_` the 64-clock
calibration burst, `drun_` the 256-clock burst of runs A and B, and `dimm_` the non-Goertzel
command. `dlytab` holds run B's eight `WAITX` delays.

The before-and-after pattern, as the calibration block runs it. The `call #xfi_end` checks with
`POLLXFI` that the streamer has finished before the second read:

```pasm2
                call    #preamble
                getxacc p_
                mov     py_, 0-0
                xinit   dcal_, son_
                waitx   ##WAIT_IDLE
                mov     site_, #2
                call    #xfi_end
                getxacc r_
                mov     ry_, 0-0
```

Run A is the same pattern with `drun_`. Run B's read inside the burst follows; the delay is
loaded from `dlytab` before the preamble, so only the `WAITX` separates the `XINIT` from the
`GETXACC`:

```pasm2
                call    #preamble
                getxacc p_
                mov     py_, 0-0
                xinit   drun_, son_
                waitx   dly_
                getxacc r1_                     ' R1: mid-burst
                mov     r1y_, 0-0
```

The non-Goertzel reads follow the same shape in the block marked `phase (i)`: an `XINIT` of
`dimm_` with the next instruction a `GETXACC`, a `WAITX` of 100 clocks and a second
`GETXACC`, then a `POLLXFI` check that the command is still running.

## Status {#sec-e4-status}

| Field | Content |
|---|---|
| Erratum | E4 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes: the before-and-after difference, measured in every repetition; the one-clock lag of Chapter 5 still applies to it |
| Affects | `GETXACC` with the streamer idle or in a non-Goertzel mode: it returns the Goertzel accumulators without clearing them. Measured with SINC1 bursts started by `XINIT`, one input pin |
| Test program | `e4-getxacc-clear-gating-test.spin2` |


# Chapter 5: The Goertzel Accumulators Trail by One Clock {#ch-e5}

In the streamer's DDS/Goertzel mode, the sine and cosine accumulators trail the products they sum by one active clock. A `GETXACC` reading taken after a burst of N clocks holds the burst's first `N-1` products; the last one waits in an internal register that no instruction reads, and is added on the first active clock of the next Goertzel burst. Ending each burst with a short burst of zero terms, in the same mode, before reading delivers the held product and leaves nothing to spill into the next burst.

## What the design says {#sec-e5-design}

The P2 Documentation describes the DDS/Goertzel mode as working on every clock of the command:

> This mode is unique, in that it outputs and inputs on every clock in which the command is active.

It then states what becomes of each clock's lookup values:

> The 8-bit sine (byte 3) and cosine (byte 2) values from the lookup RAM will each be multiplied by the bitstream sum (an integer from -3 to +3) and then added into their respective 32-bit accumulators.

Its table of accumulation modes gives the SINC1 case (D[23] = `%0`) as `SIN_ACC += SIN_MUL` and `COS_ACC += COS_MUL`, where each `_MUL` is the bitstream sum times the lookup value. By that description, a command that is active for N clocks adds N products to each accumulator, and a `GETXACC` issued after it returns all N.

The KNOWN BUGS section of the P2 Documentation does not list this behaviour. The clean-room design study found the same intent stated inside the design material as well: notes in the design describe the per-clock product as feeding the accumulator, with both valid on the same clock. That material is not quoted here.

## What the part does {#sec-e5-part}

On each active clock of a Goertzel burst, each accumulator adds the product formed on the **previous** active clock, not the product formed on that clock. After a burst of N active clocks:

- the accumulator holds the burst's first `N-1` products, plus the last product of the previous Goertzel burst if one was still held when this burst began;
- the burst's last product is held in an internal register. `GETXACC` does not return it, and it does not change while the streamer is idle;
- the first active clock of the next Goertzel burst adds the held product to the accumulator, ahead of that burst's own products.

Both accumulations behave this way: the cosine accumulation that `GETXACC` writes into D, and the sine accumulation it places into the next instruction's S. No product is lost; the last product of each burst arrives one burst late.

This was confirmed on silicon in SINC1 mode (D[23] = `%0`), with one input pin summed, for bursts of 64 and 65 clocks, each started by `XINIT` from an idle streamer and read with the streamer idle. The test ran no other streamer mode between bursts, so whether a command in another mode disturbs the held product is not established.

## The symptom {#sec-e5-symptom}

A program that runs a Goertzel burst of N clocks, waits for it to end and reads with `GETXACC` gets a sum short by exactly the burst's last product. Reading again later does not recover it: in the test, a second reading 1000 clocks after the first had moved by 0 in all 16 sequences. The missing product appears in the next Goertzel burst's reading, which is one product long.

When every product is the same (a steady input and one lookup value), the carried product stands in for the missing one from the second burst on: in the test, a burst that directly followed another burst read `N*C`, where a burst that followed a zero burst read `(N-1)*C`. When the input or the lookup value changes from clock to clock, each reading is the previous burst's last product plus the first `N-1` products of its own burst.

The shortfall was one product at both burst lengths tested. The idle reading is stable, and every product reaches the accumulator eventually.

## The workaround {#sec-e5-workaround}

Follow every burst with a short zero-term burst before reading. The zero burst uses the same mode bits in `XINIT`'s D operand, with the four pin-summation bits of its S operand, S[15:12], all clear, so that every product it forms is zero. Its first active clock adds the held product to the accumulator, and it leaves a zero product held. The reading after it holds all N products of the measured burst, and nothing spills into the next burst. The test used a zero burst of 4 clocks.

```pasm2
        getxacc base_x          ' reading before the burst
        mov     base_y, 0-0     ' sine accumulation follows
        xinit   dburst, imm_on  ' N-clock burst, pin inputs on
        waitx   ##500           ' wait until the burst has ended
        xinit   dzero, imm_off  ' zero-term burst: S[15:12] = 0
        waitx   ##500           ' adds the held term; leaves 0 held
        getxacc x               ' now all N terms are in
        mov     y, 0-0
        sub     x, base_x       ' cosine sum of the N clocks
        sub     y, base_y       ' sine sum of the N clocks
```

Here `dburst` is the Goertzel mode word with a count of N, `dzero` is the same mode word with a count of 4, and `imm_on` and `imm_off` differ only in S[15:12]. Three conditions come with the code:

- The reading is taken as the difference of two readings because `GETXACC` does not clear the accumulators while the streamer is idle; [Chapter 4](#ch-e4) covers that erratum.
- The baseline reading holds no pending product only if the burst before it also ended with a zero burst. The test ran one zero burst before its first measurement for this reason.
- `XINIT` issues its command immediately, so each `XINIT` waits for the previous burst to end. The test waited a fixed 500 clocks after each `XINIT`, which is well past the end of a 64- or 65-clock burst at one NCO rollover per clock; a longer burst or a lower NCO frequency needs a longer wait. The test did not use `WAITXFI`.

**The workaround was proven on silicon.** In all 16 sequences the reading after the zero burst had gained exactly N products over the reading before the measured burst, and the next burst read `(N-1)*C`, so no product was carried past the zero burst. The test had no DAC output enabled. With DAC channels enabled, the zero burst is a DDS/Goertzel command like any other and, by the description quoted above, outputs on each of its clocks; that case was not tested.

## Why it happens {#sec-e5-why}

The account below is the clean-room design study's reading of the mechanism, stated at the level of the programmer's model. The measurements in the next section match it.

On each active clock of a Goertzel burst, two registers update together. One is an internal product register: it takes the product formed on that clock from the lookup value and the pin sum. The other is the accumulator that `GETXACC` reads: it adds the value the product register held going into that clock, which is the product formed on the previous active clock. Both update on the same clock edge, so the accumulator is always one product behind the product register.

When a burst ends, both registers stop updating. The last product formed stays in the product register. No instruction reads that register and nothing changes it while the streamer is idle, so waiting does not deliver it. On the first active clock of the next Goertzel burst the accumulator adds it, while the product register takes that burst's first product.

A zero-term burst works for the same reason. Its first clock moves the held product into the accumulator, and its own products are all zero, so it leaves zero behind.

In SINC1 mode the product register is replaced on every clock. The study's reading does not settle the size of the shortfall in SINC2 mode (D[23] = `%1`), and SINC2 was not tested.

## How it was proven {#sec-e5-proven}

**The arrangement.** One P2 board at 200 MHz, nothing attached to P3.

- All streamer work and every `GETXACC` ran in a measuring cog started by `COGINIT`. The debugger was confined to cog 0 (`DEBUG_COGS = %0000_0001`), so no debug interrupt ran in the measuring cog (cog 1 in the run). Cog 0 only collected and printed the results.
- The measuring cog drove P3 as a plain output, low for half the run and high for the other half, in place of an ADC bitstream. The streamer took its inputs from pin group 0 (P0 to P3) with only base pin +3 summed.
- All 512 LUT longs held `$2513_0000`: cosine byte `$13` (19) and sine byte `$25` (37). Every cosine product was therefore +19 or -19 and every sine product +37 or -37, the sign set by P3. With S[19] clear, the P2 Documentation's summation table counts a 0 as -1 and a 1 as +1, so the cosine product C is -19 with P3 low and +19 with P3 high.
- `SETXFRQ` was set to `$8000_0000`, one NCO rollover per clock, so a command count of N is a burst of N clocks.
- The mode word was `$F007_0000` plus the count: DDS/Goertzel, SINC1, no DAC output, pin group 0. A product burst used S = `$0000_80C3` (S[15] set: base pin +3 summed); a zero burst used S = `$0000_00C3` (S[15:12] clear) and a count of 4.
- Every reading was taken 500 clocks after the `XINIT` that preceded it, with the streamer idle.

**One sequence**, run for N = 64 and N = 65, each from its own start:

| Step | Streamer command | Then read |
|---|---|---|
| 1 | zero burst | `B` |
| 2 | burst of N clocks | `R1`; 1000 clocks later, `R1b` |
| 3 | zero burst (the workaround) | `R2` |
| 4 | burst of N clocks | `R3` |
| 5 | burst of N clocks | `R4` |
| 6 | zero burst | `R5` |

The quantities are `d1 = R1-B`, `d2 = R2-R1`, `d3 = R3-R2`, `d4 = R4-R3` and `d5 = R5-R4`. Steps 4 to 6 test the carry: two bursts back to back, then a zero burst. The run was four repetitions of both lengths at P3 low, then the same at P3 high: 16 sequences.

**The outcomes, written into the program before the run**, in units of the per-clock product C:

| Hypothesis | `d1` | `d2` | `d3`, `d4`, `d5` |
|---|---|---|---|
| One-clock lag (the prediction) | `(N-1)*C` | `C` | `(N-1)*C`, `N*C`, `C` |
| No lag | `N*C` | 0 | `N*C`, `N*C`, 0 |
| Last product lost | `(N-1)*C` | 0 | `(N-1)*C`, `(N-1)*C`, 0 |

A nonzero `R1b-R1` under any of them would mean the accumulator moved while the streamer was idle, which none of the three allows.

**The controls**, each of which had to pass before the program would print a verdict:

- the LUT read back `$2513_0000` at addresses `$0C3`, `0` and `$1FF`;
- `TESTP` read P3 at its driven level before and after every sequence;
- a zero burst following a zero burst added nothing (the reading before step 1 equalled `B`);
- every one of `d1` to `d5` was a whole multiple of 19;
- C was measured without assuming any hypothesis, as `R2-B` at N = 65 minus `R2-B` at N = 64, which is one product under all three. It had to be 19 in magnitude, the same in every repetition, and opposite in sign between P3 low and P3 high.

**The results.** Every control passed. C measured -19 in all four repetitions at P3 low and 19 in all four at P3 high. The first repetition at each level and length read:

| P3 | N | `d1` | `R1b-R1` | `d2` | `d3` | `d4` | `d5` |
|---|---|---|---|---|---|---|---|
| low | 64 | `-1_197` | 0 | `-19` | `-1_197` | `-1_216` | `-19` |
| low | 65 | `-1_216` | 0 | `-19` | `-1_216` | `-1_235` | `-19` |
| high | 64 | `1_197` | 0 | `19` | `1_197` | `1_216` | `19` |
| high | 65 | `1_216` | 0 | `19` | `1_216` | `1_235` | `19` |

The other three repetitions of each row read the same values. All 16 sequences match the one-clock-lag row of the outcomes table: `d1 = (N-1)*C`, `d2 = C`, `R1b-R1 = 0`, and the carry steps `(N-1)*C`, `N*C`, `C`. The sine accumulation shows the same pattern with a product of 37: at P3 low and N = 64 it read `d1=-2_331`, `d2=-37`, `d3=-2_331`, `d4=-2_368`, `d5=-37`, and it read the lag pattern and the carry pattern in 16 of 16 sequences.

The test ran on 2026-09-24, twice, from two builds of the same program with identical measuring code. Every measured value matched between the two runs.

## The test program {#sec-e5-program}

The test program is `e5-goertzel-one-clock-lag-test.spin2` in the examples archive. Its Spin2 code in cog 0 starts the measuring cog, waits for it to finish, prints every raw reading and delta, checks the controls, and prints the verdict. The measuring cog is PASM2 in the program's DAT block and is the only code that touches the streamer.

The four command words sit at the end of the measuring code. `dmode_` is the Goertzel mode word without a count; each sequence ORs N into it to make the burst word. `dz_` is the zero burst's word with its count of 4, and `imz_` and `imk_` are the two S operands:

```pasm2
dmode_          long    MODE_G
dz_             long    MODE_G | ZCOUNT
imz_            long    IMM_Z
imk_            long    IMM_K
```

Each sequence runs the burst and the workaround like this. The program's comments call a product burst a K burst and the S operand `imm`, and `dk_` holds the burst word for the current N. `GETXACC` places the sine accumulation into the S field of the next instruction, so each `GETXACC` is followed by `mov ..., 0-0`, which receives it:

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

The carry steps follow directly, with no zero burst between the two product bursts:

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

## Status {#sec-e5-status}

| Field | Content |
|---|---|
| Erratum | E5 |
| Published by Parallax | No |
| Found by | Predicted by the clean-room design study; confirmed here |
| Confirmed on silicon | Yes — 2026-09-24, on a P2 board at 200 MHz, run twice |
| Workaround proven on silicon | Yes |
| Affects | `GETXACC` readings after a DDS/Goertzel burst, sine and cosine; tested in SINC1 mode with bursts of 64 and 65 clocks started by `XINIT` |
| Test program | `e5-goertzel-one-clock-lag-test.spin2` |


# Appendix A: The Test Programs {#app-a}

Every erratum in this manual was confirmed on silicon by a test program, and each program is in the examples archive. They are the programs that ran, with their internal header notes removed; their code is unchanged.

## What each program decides {#sec-a-list}

| Erratum | File | What it decides |
|---|---|---|
| E1 | `e1-setq-block-pointer-step-test.spin2` | the `PTRx` step of a `SETQ`/`SETQ2` block transfer with and without an `ALTD` between them, for six transfer forms, with three single-long references |
| E2 | `e2-altx-takes-pending-augs-test.spin2` | whether an immediate-`#S` `ALTD` or `ALTR` between `AUGS` and its target takes the augment; the register-`S` workaround; `AUGD` across an immediate-`S` `ALTS` |
| E3 | `e3-getct-stale-upper-long-runA.spin2` | the upper long `GETCT WC` returns in cogs 4-7 after that group has missed one wrap, and after it has missed two |
| E3 | `e3-getct-stale-upper-long-runB.spin2` | the same readings with a cog of cogs 4-7 running from the start: the workaround |
| E4 | `e4-getxacc-clear-gating-test.spin2` | whether `GETXACC` clears the accumulators with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst |
| E5 | `e5-goertzel-one-clock-lag-test.spin2` | how many terms a reading after a Goertzel burst holds, where the last term goes, and the zero-burst workaround |

## How they are built and run {#sec-a-run}

All six programs share one construction:

- **One file each.** Spin2 in cog 0; the measurement itself is PASM2 in a cog of its own, started by `COGINIT` from the program's `DAT` block.
- **The debugger stays out of the measurement.** `DEBUG_COGS = %0000_0001` confines the debug interrupt to cog 0, which only collects the results from hub RAM and prints them.
- **Controls before verdicts.** Each program checks its controls first. If any control fails, it prints a `RIG FAIL` line and no verdict.
- **Outcomes written in advance.** The result each program would print if the erratum were present, and if it were absent, is written into the program before it runs.
- **Raw values printed.** Every measured value is printed, not only the verdict, so the verdict can be re-derived from the output.

To run one:

1. Compile with DEBUG enabled: `pnut-ts -d <file>.spin2` (or PNut with DEBUG).
2. Download to RAM on a bare P2 board, with a reset. The E3 programs check that the counter starts from zero, so the download must reset the part.
3. Watch the DEBUG terminal. The program ends with its verdict line.

Pin use: the E4 and E5 programs drive P3 from the measuring cog, so P3 must be free. The others use no pins.

Running time: the E3 programs wait for the counter's lower long to wrap, which takes 2^32^ clocks (21.47 s at 200 MHz); Run A ends about 105 s after reset and Run B about 44 s after reset. The E1, E2, E4 and E5 programs each printed their whole output in about one second.

All six ran on 2026-09-24 on a P2 board at 200 MHz, each twice, from two builds with identical measuring code, and every measured value matched between the runs.


