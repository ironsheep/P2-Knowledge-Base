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
{\fontsize{36}{42}\selectfont\bfseries \DocTitle\par}
\vspace{0.3cm}
{\Large\itshape \DocSubtitle\par}
\vspace{0.35cm}
{\large \DocDate\par}
\vspace{0.2cm}
{\large\color{blue}Version \DocVersion\par}
\vspace{0.25cm}
{\large\bfseries\color{red!70!black} Community Review Draft \textperiodcentered\ Build 2026-10-03\par}

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
\item \textbf{E7} \enspace After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early
\end{itemize}
\vspace{0.05cm}
Each erratum opens with who meets it, what it looks like and what to do,
then gives one workaround proven on P2 hardware.
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

# Preface {#ch-preface}

This guide is for a programmer writing code for the Propeller 2. It covers the places where the chip does not do what Parallax's documentation says it does: whether each one can reach your program, what it looks like when it does, and what to write instead. Every erratum in it was confirmed on **Rev C** silicon, the revision in production, and every workaround it prints ran on P2 hardware.

Start with the *Errata Quick Reference*. It shows which errata can reach your program and finds an erratum from a symptom. The P2 Errata sheet carries the same quick reference and each erratum's summary on a few pages.

## How an erratum is laid out {#sec-preface-layout}

Each erratum has a chapter headed with its number: *Erratum E3* describes E3. The chapter opens with a box of three lines: who meets it, what you see, and what to do. For a reader who needs only the rule, the box is the whole erratum. Two sections follow:

- **What happens:** what Parallax's documentation states, what the part does instead, and what is not affected.
- **A proven workaround:** the rule any workaround must meet, then one way that meets it, printed exactly as it ran on silicon. A workaround is one of three kinds: a *one-time startup workaround*, added once when the program starts; a *rule at each use*, followed wherever the affected instruction is used; or a *helper routine*, called in place of the affected sequence.

A closing line says who found the erratum and whether Parallax publishes it. Appendix A lists the test programs that confirmed each erratum, and what they measured.

The part keeps its defect, so this guide offers workarounds, never fixes. Each workaround is one way to meet its rule, not the only way.

## What counts as an erratum {#sec-preface-classes}

An erratum is behaviour of the part that contradicts a specific written statement in Parallax's documentation. Behaviour the documentation states is not an erratum, however surprising it is. Legal code that does something other than what it appears to do, where the documentation does not say otherwise, is an anti-pattern; anti-patterns and their safe forms are documented in the companion manual *P2 Anti-Patterns*.

These are the errata found so far. Any further erratum that a test on P2 hardware confirms is added as E8 onward. Erratum numbers are **permanent**: a number is never reused or reassigned, so E3 means the same erratum in every edition.

This is a **community review draft**. Its errata and workarounds are confirmed on silicon; its wording and its explanations are open for review.

## Sources {#sec-preface-sources}

- **Parallax Propeller 2 Documentation** (Chip Gracey, Parallax Inc.): the v35 edition (Rev B/C), and the current online edition, which adds the 2024 note on Goertzel SINC2 mode. It is the source for what the part is meant to do, and for its KNOWN BUGS section.
- **Parallax Spin2 Language Documentation** (Chip Gracey, Parallax Inc.), v55: what Spin2's `GETMS()` and `GETSEC()` return and what `DEBUG_TIMESTAMP` stamps (Erratum E3).

These two are the only documents this guide cites for what the P2 is meant to do.

- **Tests on P2 hardware** (P2 Knowledge Base Project): each erratum was confirmed on Rev C silicon by a test program in the examples archive (Appendix A).

## Acknowledgments {#sec-preface-ack}

**Parallax Inc.** for the Propeller 2, and for publishing its known silicon defects in the P2 Documentation. Errata E1 and E2 are Parallax's own findings.

**Chip Gracey** for the design of the Propeller 2 and for the silicon documentation that states what the part is meant to do. Every erratum here is measured against that statement.

**The clean-room design study** for predicting errata E3, E4, E5 and E6 from the design material alone, and for the classification of findings this guide follows. The study read the design without Parallax's documentation or a bench; each prediction was then tested on P2 hardware, independently. Erratum E7 was first found on the bench, by a test built to measure something else; the study then predicted that the same condition reaches every hub read and write, and the bench confirmed it.

## Document conventions {#sec-preface-conventions}

| Element | Format | Example |
|---------|--------|---------|
| Instructions | Uppercase in running text, lowercase in code | `SETQ`, `setq` |
| Registers / symbols | Monospace | `PTRA`, `CT` |
| Bit fields | Brackets | D[31:0], `imm[15:12]` |
| Hexadecimal | Dollar prefix | `$3C5C_0A55` |
| Binary | Percent prefix | `%1111` |


# Errata Quick Reference {#ch-quick-reference}

## Which errata can affect your program {#sec-qr-which}

The seven errata found so far are not equally likely to reach a program, and the table lists them in the order a programmer is likely to meet them. E3 is the one that ordinary multi-cog code can meet. Each of the others needs an unusual arrangement of instructions or a specialist feature.

| Erratum | Your program meets it if it… | How often that comes up |
|---|---|---|
| **E3** GETCT Returns a Stale Upper Long | reads `GETCT WC`, `GETMS()`, `GETSEC()` or DEBUG time stamps in a cog of 4-7 that it starts more than 2^32^ clocks (21.47 s at 200 MHz) after reset | Often: ordinary multi-cog code that runs for more than 21.47 s |
| **E7** After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early | starts a hub instruction fewer than 16 clocks after a no-wait `RDFAST` | Rarely: code normally does other work after a no-wait `RDFAST` |
| **E1** SETQ Block Transfers Lose Their Pointer Step | places an `ALTx`, `AUGS` or `AUGD`, or a `##` operand, between a `SETQ` and a block transfer that updates `PTRx` | Rarely: an unusual arrangement |
| **E2** An Immediate ALTx Takes a Pending AUGS | writes an `AUGS` explicitly and places an immediate-`#S` `ALTx` before its target | Rarely: only with an explicit `AUGS` |
| **E4** GETXACC Clears Only During a Goertzel Burst | runs DDS/Goertzel bursts one at a time and clears the sums with `GETXACC` | Only Goertzel measurements |
| **E5** The Goertzel Accumulators Trail by One Clock | reads the DDS/Goertzel sums with `GETXACC` after each burst | Only Goertzel measurements |
| **E6** In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC | switches the ADC of a DAC smart-pin mode with `OUT`, with `TT` = `%00` | Only that pin configuration |

## Find an erratum by symptom {#sec-qr-symptoms}

Each row is a symptom a program can show, and the erratum that produces it. An erratum with several symptoms has a row for each.

| Symptom | Erratum |
|---|---|
| `GETCT WC`, `GETMS()`, `GETSEC()` or a `DEBUG_TIMESTAMP` stamp reads behind by 2^32^ clocks (21.47 s at 200 MHz), or a multiple of it, in one group of cogs | **E3** |
| DEBUG messages from different cogs carry time stamps out of order by 21.47 s at 200 MHz | **E3** |
| A `RDBYTE`, `RDWORD` or `RDLONG` returns the previous hub read's data, with that value's flags | **E7** |
| A `WRBYTE`, `WRWORD` or `WRLONG` is lost | **E7** |
| A `SETQ` block `RDLONG` writes one wrong long and changes other cog registers, or the cog stops responding | **E7** |
| An `RFLONG` after a waiting `RDFAST` returns `$0000_0000` | **E7** |
| After a `SETQ` block transfer through `PTRx++`, the pointer moved by one long, not by the block | **E1** |
| An `ALTx` with an immediate `#S` moves its `D` register | **E2** |
| `GETXACC` read with the streamer idle does not clear the Goertzel sums | **E4** |
| A Goertzel burst's sum lacks its last term and holds the last term of the burst before it | **E5** |
| In a DAC smart-pin mode with `TT` = `%00`, raising `OUT` does not run the pin's ADC | **E6** |


# Erratum E1: SETQ Block Transfers Lose Their Pointer Step {#ch-e1}

::: caution
**Who meets it:** PASM2 that places an instruction between a `SETQ` or `SETQ2` and the block `RDLONG`, `WRLONG` or `WMLONG` it prepares, when the transfer updates `PTRx` (for example `ptra++`). Parallax names `ALTx`, `AUGS` and `AUGD` in that position. A `##` operand on the transfer puts one there without your writing it: the assembler places its `AUGS` directly before the transfer, after the `SETQ`.

**What you see:** the whole block moves, but `PTRx` steps as for a single long (`ptra++` moves it by 4), not past the block.

**What to do:** write the `SETQ` or `SETQ2` directly before the transfer, and keep `##` operands off a block transfer that updates `PTRx`.
:::

## What happens {#sec-e1-actual}

A `SETQ` or `SETQ2` placed before `RDLONG`, `WRLONG` or `WMLONG` makes it a block transfer. The P2 Documentation, in its section *FAST BLOCK MOVES*, gives the pointer update for one: `SETQ #x` followed by `RDLONG first_reg,PTRA++` reads x+1 longs and updates `PTRA += (x+1)*4`, past the whole block. Parallax publishes the exception in the KNOWN BUGS section of the same document:

> Intervening ALTx/​AUGS/​AUGD instructions between SETQ/​SETQ2 and RDLONG/​WRLONG/​WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas. The expected number of longs will transfer, but PTRx will only be modified according to normal PTRx expression behavior:

On P2 hardware, with an `ALTD` between the `SETQ` and the transfer, every long of the block moved, to the registers the `ALTD` selected and from the hub address `PTRx` held. `PTRx` then changed by the step the same expression gives without a `SETQ`: +4 for `ptra++` and `ptrb++`, +12 for `ptra++[3]`, whatever the length of the block. An 8-long block moved `PTRA` by 4, as a 4-long block did. This held for `SETQ` with `RDLONG` at 4 and 8 longs, `SETQ2` into lookup RAM, and `SETQ` with `WRLONG`, through `PTRA` and through `PTRB`.

Your data is right and your pointer is not. A loop that walks a hub buffer one block at a time starts each block 4 bytes after the start of the one before, so its reads overlap; built on `WRLONG`, each block overwrites all but the first long of the one before it. Code that reloads the pointer before its next use is not affected.

The arrangement is unusual: the reason to write an `ALTD` there is to redirect the block's first register. The `##` path in the box is the one that is easy to miss, because no `AUGS` appears in the source: with `pnut-ts`, `setq #3` followed by `rdlong buf, ptra++[##100]` assembles to `SETQ`, `AUGS`, `RDLONG`.

Only `ALTD` was tested as the intervening instruction; Parallax names `AUGS` and `AUGD` as well. `WMLONG`, `SETQ2` with `WRLONG`, and the decrement and pre-modify forms (`ptra--`, `++ptra`, `--ptra`) were not tested.

## A proven workaround {#sec-e1-workaround}

**What any workaround must do:** nothing may sit between the `SETQ` or `SETQ2` and the block transfer it prepares.

**One way, proven on P2 hardware:** write the `SETQ` or `SETQ2` directly before the transfer.

```pasm2
CON ' ---- E1 Workaround: Block Length ----
  BLOCK_LONGS   = 4                     ' longs in your block

DAT ' ---- E1 Workaround: Block Transfer ----
                setq    #BLOCK_LONGS - 1        ' directly before RDLONG
                rdlong  block_first, ptra++     ' block's first register
```

With the `SETQ` or `SETQ2` as the instruction directly before the transfer, the whole block moves and `PTRx` steps past all of it: a *rule at each use*. In your code, `BLOCK_LONGS - 1` is your block length minus one and `block_first` is the first register of your block. A hub address or offset too large for nine bits goes into `PTRx` before the `SETQ`, so that the transfer carries no `##` operand.

On silicon these two lines advanced `PTRA` by 16 with all four longs in place, and the same adjacent form gave the full block step for an 8-long read, through `PTRB`, for a `WRLONG`, for `SETQ2` into lookup RAM, and with `ptra++[3]`.

The cost is the redirect: without the `ALTD`, the block's first register is fixed when the code is assembled. No form that keeps the redirect has been run on silicon.

**Found by** Parallax, and published in the P2 Documentation's KNOWN BUGS section. Confirmed on P2 hardware on 2026-09-24.


# Erratum E2: An Immediate ALTx Takes a Pending AUGS {#ch-e2}

::: caution
**Who meets it:** PASM2 that writes an `AUGS` explicitly and places an `ALTx` with an immediate `#S` (such as `ALTD idx,#base`, or the one-operand `ALTD idx`) between it and the instruction it was written for. A `##` literal never produces this arrangement: the assembler places its `AUGS` directly before the instruction that carries the `##`.

**What you see:** the `ALTx` takes the augment as well, and its `D` register moves by bits 17:9 of the augmented value. The redirect and the target's value are correct.

**What to do:** give that `ALTx` a register `S`.
:::

## What happens {#sec-e2-actual}

An `AUGS` holds 23 bits for the next instruction that carries a literal `#S`, which takes them as bits 31:9 of its `S`. An `ALTx` uses its `S` in two fields: bits 8:0 are the base added to `D[8:0]` to form the substituted address, and bits 17:9 are sign-extended and added to the `D` register as an auto-increment. The P2 Documentation, in its section *REGISTER INDIRECTION*, notes that a nine-bit immediate leaves that second field zero, "so that D is unaffected". Parallax publishes the exception in the KNOWN BUGS section of the same document:

> Intervening ALTx instructions with an immediate #S operand, between AUGS and the AUGS'
> intended target instruction (which would have an immediate #S operand), will use the
> AUGS value, but not cancel it. So, the intended AUGS target instruction will use and
> cancel the AUGS value, as expected, but the intervening ALTx instruction will also use
> the AUGS value (if it has an immediate #S operand). To avoid problems in these
> circumstances, use a register for the S operand of the ALTx instruction, and not an
> immediate #S operand.

On P2 hardware, with `AUGS #$3C5C_0A55` (bits 17:9 = 5) followed by `ALTD idx,#0` or `ALTR idx,#3` and then the target, the `ALTx` moved `idx` by 5. Its redirect was unaffected, since bits 8:0 are still its own field, and the target received the full value `$3C5C_0A55`. No other register in a 32-register window around the target changed. The effect is confined to the `ALTx`'s `D` register, which a later pass of an indexing loop then reads with the wrong value.

The one-operand form counts as immediate: `ALTD idx` assembles to the same instruction word as `ALTD idx,#0`. A pending `AUGD` is not affected: with an immediate-`S` `ALTS` between `AUGD` and its target, the target received the full value and the `ALTS`'s register did not move.

The arrangement is uncommon. It needs an `AUGS` written explicitly, as in Parallax's own example. A `##` literal never produces it, because the assembler places the `AUGS` it generates directly before the instruction that carries the `##`.

`ALTD` and `ALTR` were tested as the intervening instruction, each directly after the `AUGS`, with one augment value.

## A proven workaround {#sec-e2-workaround}

**What any workaround must do:** no `ALTx` with an immediate `#S` may stand between an `AUGS` and the instruction the `AUGS` was written for.

**One way, proven on P2 hardware:** give that `ALTx` a register `S`, as Parallax directs.

```pasm2
                augs    #AUGV
                altd    idx, sreg4
                mov     0-0, #LO
```

With a register `S` on the `ALTD`, the `ALTD` takes nothing from the `AUGS`, `idx` does not move, and the augment reaches the target: a *rule at each use*.

In these lines `AUGV` is the 32-bit value the `AUGS` carries for the `MOV`, `LO` is its low 9 bits, and `sreg4` is a cog register holding the `ALTD`'s `S`: the base, 4, in bits 8:0 and a zero auto-increment in bits 17:9. In your code, the base and any auto-increment that were in the immediate `#S` go into that register. On silicon, the `MOV` was redirected to the register four along from the one `idx` addressed, which received `$3C5C_0A55`, and `idx` did not move. The cost is one cog register for each distinct `S` value.

**Found by** Parallax, and published in the P2 Documentation's KNOWN BUGS section. Confirmed on P2 hardware on 2026-09-24.


# Erratum E3: GETCT Returns a Stale Upper Long {#ch-e3}

::: caution
**Who meets it:** a program that reads a 64-bit time (`GETCT WC`, `GETMS()`, `GETSEC()`, or a `DEBUG_TIMESTAMP` stamp) in a cog of 4-7 that it starts more than 2^32^ clocks after reset (21.47 s at 200 MHz). The same applies to either group of four cogs once all of its cogs have stopped and a cog starts there again after a wrap of the counter's lower long.

**What you see:** that time reads behind by 2^32^ clocks for each wrap the group missed, until the group's next wrap, at most 2^32^ clocks later. Plain `GETCT` and every wait on the counter time correctly.

**What to do:** start a cog in 4-7 on the first line of `main()` and never stop it.
:::

## What happens {#sec-e3-actual}

The P2 Documentation describes one counter, a "64-bit free-running counter which increments every clock, cleared on reset", and states that "GETCT WC retrieves upper 32-bits". The Spin2 Language Documentation (v55) says that `GETMS()` and `GETSEC()` use the 64-bit system counter, and that with `DEBUG_TIMESTAMP` declared "each DEBUG message will be time-stamped with the 64-bit CT value". Neither document qualifies these values by cog number, or by which other cogs are running.

What the part does follows from one model, measured on P2 hardware. The eight cogs form two groups of four, cogs 0-3 and cogs 4-7, and each group reads its own copy of the counter. The lower long of that copy is always current. The upper long advances at a wrap of the lower long, once every 2^32^ clocks (21.47 s at 200 MHz), and only if at least one cog of the group is running at that moment. A group with no running cog at a wrap keeps its previous upper long. A cog held in a wait counts as running: a cog held in `WAITATN`, in `WAITX` or in `WAITCT1`, alone in its group, kept the group current.

At reset only cog 0 runs, so cogs 0-3 stay current for as long as one of them runs. Cogs 4-7 have no running cog until the program starts one, and their upper long stays at zero through every wrap until then. A cog started there after the first wrap reads behind by 2^32^ clocks for each wrap missed; starting it does not bring the group up to date. That error is a **stale window** with a known end: it closes at the first wrap the group runs through, in one step, whatever the lag (measured from one, two and eight missed wraps). After that the group stays current for as long as one of its cogs runs. Either group opens a new window if all four of its cogs stop and a wrap passes before one starts again; cogs 0-3 did the same as cogs 4-7.

In a program, `GETMS()` called in Spin2 cog 5 after its group had missed eight wraps (171,798 ms at 200 MHz), at the same moment as in cog 0:

| Called in | `GETMS()` | `GETSEC()` |
|---|---|---|
| cog 0 | 190,617 | 190 |
| cog 5, in the stale window | 18,819 | 18 |
| cog 0, after the window closed | 194,637 | 194 |
| cog 5, after the window closed | 194,637 | 194 |

A `DEBUG_TIMESTAMP` stamp shows the same error, so in a log that mixes messages from both groups, messages sent from the window carry times out of order. An interval timed in 64 bits across the closing wrap includes 2^32^ clocks that did not pass for each wrap the group missed.

Nothing that works on the lower long alone is affected, inside the window or across the wrap that closes it. In PASM2, these time as in an up-to-date group: plain `GETCT`, `ADDCT1`-`ADDCT3` with `WAITCT1`-`WAITCT3`, `POLLCT1`-`POLLCT3`, `JCT1`-`JCT3`, `JNCT1`-`JNCT3`, interrupts on the CT1-CT3 events, the `SETQ` timeout of a wait, and `WAITX`. In Spin2, so do `GETCT()`, `WAITCT()`, `POLLCT()`, `WAITMS()` and `WAITUS()`.

This is the erratum ordinary code meets. A program meets it as soon as it starts a cog of 4-7 after running for more than 21.47 s and takes a 64-bit time there.

## A proven workaround {#sec-e3-workaround}

**What any workaround must do:** take no 64-bit time, a `DEBUG_TIMESTAMP` stamp included, inside a stale window. Either keep a cog of the group running at every wrap from the first wrap on, so that the window never opens, or wait it out: take no 64-bit time in the group until it has run through one wrap since its first cog started.

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

The keeper keeps a cog of 4-7 running through every wrap, so the stale window never opens in cogs 4-7, and a cog your program starts there at any later time reads the same upper long as cog 0: a *one-time startup workaround*. Put the block at the top of your top-level object, ahead of every other `PUB` method, since Spin2 runs the first `PUB` method of the top-level object at start; your own `main()` body follows the `coginit` line. `KEEPER_COG` must be a cog of 4-7 that nothing else in your program starts or stops.

On silicon, with the keeper running, cogs 4, 5 and 6, started after one or two wraps, read the same upper long as cog 0 in every reading. With the keeper stopped, cog 6 read one behind.

**Other ways that meet the condition:**

- **A cog of your own.** A cog your program already starts in 4-7 before the first wrap and never stops does what the keeper does, even if it spends its time waiting. The P2 Documentation does not say which cog a free-cog start chooses, so start that cog in 4-7 by number, or check the cog number the start returns.
- **Waiting it out.** Once the group's first cog has run through one wrap, at most 2^32^ clocks after it starts, the group reads current.

**The cost** is one cog for the life of the program. A program that needs all eight cogs meets the condition if one of its own cogs of 4-7 starts before the first wrap and never stops. The block covers cogs 4-7. Cogs 0-3 stay current through cog 0, which runs `main()`; a program that stops every cog of 0-3 needs the same care there.

**Found by** the clean-room design study, as a prediction, and confirmed on P2 hardware on 2026-09-24. Parallax does not list it.


# Erratum E4: GETXACC Clears Only During a Goertzel Burst {#ch-e4}

::: caution
**Who meets it:** PASM2 that runs DDS/Goertzel bursts one at a time, with the streamer idle between them, and relies on `GETXACC` to clear the accumulators.

**What you see:** with the streamer idle, `GETXACC` returns the sums but clears nothing, so each burst adds to what earlier bursts left and each reading is a running total.

**What to do:** take each burst's sums as the difference of two readings taken with the streamer idle, one before the burst and one after it. The `burst_sums` routine does this, and steps around Erratum E5 as well.
:::

## What happens {#sec-e4-actual}

The P2 Documentation's streamer instruction table gives `GETXACC` as:

> Get Goertzel X into D and Y into next S, clear X and Y

Its description of the DDS/Goertzel mode says the same, and neither makes the clear depend on the streamer's mode or on whether a streamer command is running.

In this erratum a *Goertzel burst* is one DDS/Goertzel streamer command for the clocks it runs, and a *term* is what it adds to each accumulator on each of those clocks. On P2 hardware the clear acts only while a Goertzel burst is running:

- **With the streamer idle**, `GETXACC` returns the accumulators and leaves them as they were. Repeated reads return the same value. The same held with the streamer running another mode (immediate-to-pins was tested).
- **A new Goertzel burst** adds its terms to whatever the accumulators hold. Starting a streamer command does not reset them.
- **During a Goertzel burst**, the clear acts as documented: a read returns everything accumulated so far, earlier bursts included, and the accumulation continues from the clear. No term is lost and none is counted twice.

So a program that issues one `GETXACC` after each burst and treats it as that burst's result gets a running total: in the test, the reading before a 256-clock burst was 14,823 and the reading after it was 30,378, of which the burst contributed 15,555. A `GETXACC` issued before an `XINIT` to zero the sums zeroes nothing. The accumulation itself is exact; only the clear is missing.

The difference of two idle readings is still one term short of the burst, because the burst's last term is held back until the next Goertzel burst. That is Erratum E5, and the routine below steps around both.

Only programs that measure with the Goertzel mode meet this erratum, and among them only those that run one burst at a time from an idle streamer. A continuous stream of commands chained with `XCONT`, read during each command, clears as documented.

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

Each call leaves in `cos_sum` and `sin_sum` the sums of your burst alone, all N of its terms, whatever the accumulators held before the call: a *helper routine*. To use it, put your `XINIT` D operand (the Goertzel mode word with your count) in `burst_mode` and your S operand in `burst_sel`, set `SETXFRQ` as your program already does, and `CALL #burst_sums` with the streamer idle. The values printed in `burst_mode` and `burst_sel` are the test program's.

The two zero bursts are your mode word with a count of 4 and every input switched off (`S[15:12]` clear), so every term they form is zero. The first delivers any term an earlier burst left held, and the second delivers your burst's last term (Erratum E5).

On silicon, the routine returned exactly N terms on both sums in all 60 calls of its test program, for bursts of 1 to 1001 clocks, at both input levels.

**The cost:** two zero bursts of 4 NCO rollovers each per call, besides your burst; 17 instructions and 8 longs of cog RAM.

**The limits:** SINC1 mode only, and one burst at a time from an idle streamer, since the routine starts each command with `XINIT`. It ran from cog RAM at 200 MHz with one input pin and no DAC output; DAC output, more than one input pin, other NCO frequencies and hub execution were not tested.

**Found by** the clean-room design study, as a prediction, and confirmed on P2 hardware on 2026-09-24. Parallax does not list it.


# Erratum E5: The Goertzel Accumulators Trail by One Clock {#ch-e5}

::: caution
**Who meets it:** the same programs as Erratum E4: a `GETXACC` reading taken after each DDS/Goertzel burst.

**What you see:** each reading lacks the burst's last term. That term is added on the first clock of the next Goertzel burst.

**What to do:** run a short burst whose terms are all zero before you read. The `burst_sums` routine, shared with Erratum E4, does this in SINC1 mode.
:::

## What happens {#sec-e5-actual}

The P2 Documentation describes the DDS/Goertzel mode as one that "outputs and inputs on every clock in which the command is active", and its table of accumulation modes gives the SINC1 case as `SIN_ACC += SIN_MUL` and `COS_ACC += COS_MUL` on each of those clocks. By that description a command active for N clocks adds N terms to each accumulator, and a `GETXACC` issued after it returns all N.

On P2 hardware, each active clock adds the term formed on the **previous** active clock. After a Goertzel burst of N clocks:

- the accumulators hold the burst's first N-1 terms;
- the last term is held internally. `GETXACC` does not return it, and waiting does not deliver it: a second reading 1,000 clocks after the first had not moved;
- the first clock of the next Goertzel burst adds the held term, ahead of that burst's own terms.

No term is lost; each burst's last term arrives one burst late. With a steady input the carried term stands in for the missing one from the second burst on, so a burst that directly followed another read N terms, while a burst that followed a zero burst read N-1. When the input changes from clock to clock, each reading is the previous burst's last term plus the first N-1 terms of its own.

Like Erratum E4, this reaches only programs that measure with the Goertzel mode, and a reading taken with `GETXACC` after each burst.

The confirmation is for SINC1 mode, with one input pin summed, for bursts of 64 and 65 clocks started by `XINIT` from an idle streamer. Whether a command in another streamer mode between bursts disturbs the held term was not tested.

## A proven workaround {#sec-e5-workaround}

**What any workaround must do:** deliver the burst's held last term to the accumulators before reading them, in SINC1 mode.

**One way, proven on P2 hardware:** the helper routine printed in Erratum E4, `burst_sums`. It ends every burst with a short burst whose terms are all zero before it reads, so each call returns all N terms of your burst and leaves no term held for the next. One call steps around both errata. On silicon it returned exactly N terms in all 60 calls of its test program, including the 6 calls made while an earlier burst's term was still held.

**Another way:** any Goertzel burst whose terms are all zero, run after your burst and before the reading, delivers the held term. The kind measured is the routine's own: a count of 4 with `S[15:12]` clear.

**The limits:** SINC1 only. The routine's zero burst has not been tested as a flush in SINC2 mode. SINC2 has its own documented constraint, which is not this erratum: the P2 Documentation's note on Goertzel SINC2 mode states that a varying number of iterations in a Goertzel cycle corrupts the current and next samples. Its two remedies, a constant iteration count or commands issued with `XZERO`, held on P2 hardware.

**Found by** the clean-room design study, as a prediction, and confirmed on P2 hardware on 2026-09-24. Parallax does not list it.


# Erratum E6: In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC {#ch-e6}

::: caution
**Who meets it:** a pin in a DAC smart-pin mode (`%SSSSS` = `%00001` to `%00011`) configured with `TT` = `%00`, whose ADC the program switches on with `OUT`.

**What you see:** raising `OUT` does not start the ADC.

**What to do:** set `TT` bit 0 (`$40` in the `WRPIN` word, `P_TT_01` in Spin2). The pin's DAC then drives the pin while the ADC runs.
:::

## What happens {#sec-e6-actual}

The P2 Documentation, section SMART PINS, describes the `%TT` field of the `WRPIN` word (bits 7:6) with one rule for every smart-pin mode and a second for the DAC smart-pin modes:

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

The two rules act on different bits: bit 0 sets the output enable, and bit 1 chooses whether `OUT` or `OTHER` switches the ADC. By the table, `TT` = `%00` is a pin with its output disabled whose ADC `OUT` switches.

On P2 hardware, in DAC noise mode (`$0014_0002`, `TT` = `%00`), raising `OUT` did not run the ADC: the pin's read state stayed exactly as it was with `OUT` low, 0 in every one of 4,096 reads, in every sample. With `TT` = `%01` (`$0014_0042`), raising `OUT` ran the ADC as the table states, and the read state toggled, high in 1,958 to 2,093 of 4,096 reads. In the mode tested, `OUT` switches the ADC only while `TT` bit 0 also enables the pin's output.

Only programs that use the ADC of a DAC smart-pin mode, switched by `OUT`, with `TT` bit 0 clear, meet this erratum. A pin configured with `P_TT_01` or `P_OE` (the same value) is not affected.

Only DAC noise (`%00001`), the `P_DAC_990R_3V` setting, and `TT` = `%00` and `%01` were tested. The ADC was observed through the pin's read state; its accumulation was not read with `RDPIN`.

## A proven workaround {#sec-e6-workaround}

**What any workaround must do:** set `TT` bit 0 in the `WRPIN` word of a pin in a DAC smart-pin mode whose ADC you switch with `OUT`.

**One way, proven on P2 hardware:** the tested DAC noise word with `TT` = `%01`.

```spin2
  CFG_DAC_TT01      = $0014_0042        ' DAC_MODE, DAC noise, TT = %01
```

Written to the pin with `WRPIN` in place of `$0014_0002`, this word makes `OUT` run the pin's ADC: a *rule at each use*. The change is one bit, bit 6 (`$40`); in Spin2 symbols the word is `P_DAC_990R_3V | P_TT_01 | P_DAC_NOISE`. In another DAC smart-pin word the change is the same bit, but only this word was tested.

**The cost** is the pin's output. With `TT` bit 0 set, the output is enabled regardless of `DIR`, and in DAC noise mode the pin's DAC drives it while the ADC runs, so use a pin that nothing else drives. No tested setting runs the ADC in these modes with the pin undriven.

**Found by** the clean-room design study, as a prediction, and confirmed on P2 hardware on 2026-09-25. Parallax does not list it.


# Erratum E7: After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early {#ch-e7}

::: caution
**Who meets it:** PASM2 that starts the hub FIFO with a no-wait `RDFAST` (`D[31]` = 1) and starts another hub instruction fewer than 16 clocks later: a hub read or write, a `SETQ` block read, or a waiting `RDFAST`. Code that does other work in between, or uses the waiting form, does not meet it.

**What you see:** that instruction can complete early. A read returns the previous hub read's data, with that value's flags; a write is lost if a hub read follows it at once; a block read writes wrong data, or the cog stops responding; a waiting `RDFAST` does not wait. Whether it happens depends on hub alignment, so the same code can work on one pass and fail on the next.

**What to do:** allow at least 16 clocks from the start of the no-wait `RDFAST` to the next hub instruction (`WAITX #12` directly after it, or seven two-clock instructions), or use the waiting form.
:::

## What happens {#sec-e7-actual}

The P2 Documentation, section FAST SEQUENTIAL FIFO INTERFACE, gives `RDFAST` two modes, chosen by bit 31 of D. For the waiting mode:

> If D[31] = 0, RDFAST/WRFAST will wait for any previous WRFAST to finish and then reconfigure the hub FIFO interface for reading or writing. In the case of RDFAST, it will additionally wait until the FIFO has begun receiving hub data, so that it can start being used in the next instruction.

For the no-wait mode:

> If D[31] = 1, RDFAST/WRFAST will not wait for FIFO reconfiguration, taking only two clocks. In this case, your code must allow a sufficient number of clocks before any attempt is made to read or write FIFO data.

That requirement concerns FIFO data, which the cog reads with `RFLONG` and its kin. Neither paragraph restricts a hub read or write at its own address after a no-wait `RDFAST`, or makes an exception for a waiting `RDFAST` that follows one. A FIFO read too soon after a no-wait `RDFAST` is the case the no-wait paragraph does cover, and it is not this erratum.

On P2 hardware, in cog execution, a hub instruction started fewer than 16 clocks after the start of a no-wait `RDFAST` can complete before its own hub access. Counted from the start of the `RDFAST`, its own 2 clocks included:

- a `RDBYTE`, `RDWORD` or `RDLONG` returns the previous hub read's data instead of the data at its own address, and its `WC`/`WZ` flags agree with that wrong value;
- a `WRBYTE`, `WRWORD` or `WRLONG` is lost if a hub read follows it at once;
- a `SETQ` block `RDLONG` writes one wrong long and changes cog registers outside its destination, or the cog stops responding;
- a waiting `RDFAST` takes 2 clocks without waiting, and the `RFLONG` after it returns `$0000_0000`.

Nothing flags any of these. Whether an instruction is affected depends on the hub alignment of the two addresses, so the same code can work on one pass and fail on the next. The release coincides with the arrival of the FIFO's first long, 8 to 15 clocks after the `RDFAST` starts: at 2 clocks a `RDLONG` was released in 43 of the 64 alignments, at 8 clocks in all 64, at 14 in 16, and from 16 clocks on in none. A no-wait `WRFAST` released nothing.

The condition is narrow. It needs a hub instruction within seven two-clock instructions of a no-wait `RDFAST`, and code normally does other work there. Code that uses only the waiting form never meets it, and `RDFAST` cannot be used in hub execution.

## A proven workaround {#sec-e7-workaround}

**What any workaround must do:** after a no-wait `RDFAST`, start no hub instruction until at least 16 clocks have passed from the start of the `RDFAST`; or use the waiting form of `RDFAST`.

**One way, proven on P2 hardware:** a `WAITX #HUB_SPACING_WAITX` (12) directly after the no-wait `RDFAST`, with the constant in a `CON` block:

```pasm2
  HUB_SPACING_WAITX = 12                ' RDFAST 2 + WAITX 2+12 = 16 clocks
```

```pasm2
        rdfast  nowait, hub_stream      ' no-wait RDFAST (D[31] = 1)
        waitx   #HUB_SPACING_WAITX      ' E7: >= 16 clocks to next hub op
        rdlong  value, hub_addr  wcz    ' hub_addr's long, and its flags
```

The `WAITX` makes the spacing to the next hub instruction 16 clocks: a *rule at each use*, applied wherever a hub instruction follows a no-wait `RDFAST`. In your code, `nowait` is a register holding `$8000_0000`, `hub_stream` holds the FIFO's start address, `hub_addr` the address read, and `value` receives the long. On silicon this block returned the long at `hub_addr` with its own flags in all 64 hub alignments, 16 trials each; the same spacing before a `WRLONG`, `WRWORD` or `WRBYTE` landed every write.

**Another way, proven on P2 hardware: the waiting form.** A `RDFAST` with `D[31]` = 0 needs no spacing:

```pasm2
        rdfast  #0, hub_stream          ' waiting RDFAST (D[31] = 0)
        wrlong  value, hub_addr         ' lands at hub_addr
        rdlong  check, hub_addr  wcz    ' reads value back, and its flags
```

In every test that ran it, for every instruction above, the waiting form released nothing. Its cost is the wait for the FIFO, 10 to 17 clocks where a no-wait `RDFAST` takes 2.

**Other instructions in the window** meet the condition just as well, since the release depends only on the spacing: seven two-clock instructions after the no-wait `RDFAST` released nothing (`NOP`s were tested), and before a `SETQ` block `RDLONG` the `SETQ` counts as one of the seven.

**The limits:** tested in cog execution, one cog, 200 MHz, for the instructions listed above. `WMLONG`, `SETQ2` block reads, `SETQ` block writes, the instructions that read the hub stack, an interrupt taken inside the window, and the streamer were not tested.

**Found by** a bench test built to measure something else, on 2026-09-25. The clean-room design study then predicted that the condition reaches every hub read and write, and P2 hardware confirmed it on 2026-10-01. Parallax does not list it.


# Appendix A: How Each Erratum Was Confirmed {#app-a}

Every erratum in this guide was confirmed on a P2 board (Rev C) at 200 MHz by a test program, and every workaround it prints ran on silicon inside a test program. Every program is in the examples archive. Each one checks its controls before it gives a verdict, had the result for the erratum present and for it absent written in before it ran, and prints every measured value, so its verdict can be re-derived from its output. Each workaround test also reproduces its erratum in the same run, so a clean result cannot come from a test that is unable to see the defect.

## The evidence {#sec-a-evidence}

| Erratum | Test programs | What was measured | Result |
|---|---|---|---|
| **E1** | `e1-setq-block-pointer-step-test.spin2` | The `PTRx` step of six block transfers, with and without an `ALTD` after the `SETQ`; its control arms are the workaround | With the `ALTD`, every block moved but `PTRx` took the single-long step (+4, or +12 for `ptra++[3]`); without it, the full block step. 2026-09-24, run twice |
| **E2** | `e2-altx-takes-pending-augs-test.spin2` | An immediate-`#S` `ALTD` or `ALTR` between `AUGS` and its target; the register-`S` workaround; `AUGD` across an `ALTS` | The `ALTx` moved `idx` by bits 17:9 of the augment (5); the target got the full value. With a register `S`, `idx` did not move. `AUGD` was unaffected. 2026-09-24, run twice |
| **E3** | `e3-getct-stale-upper-long-runA.spin2`, `e3-getct-stale-upper-long-runB.spin2`, `e3-cogs-0-3-stale-window-test.spin2`, `e3-stale-window-closes-test.spin2` | The upper long, `GETMS()` and `GETSEC()` in a group that missed one, two and eight wraps, in cogs 4-7 and in cogs 0-3, before and after the group's next wrap | Behind by one wrap per wrap missed, in every pair; current after one wrap run through. 2026-09-24 and 2026-09-27 |
| **E3** | `e3-pasm2-counter-targets-test.spin2`, `e3-spin2-counter-methods-test.spin2`, `e3-debug-timestamp-test.spin2` (with `e3-debug-timestamp-verdict.py`) | Every counter wait, event and timeout in PASM2 and Spin2, inside the stale window and across its closing wrap; `DEBUG_TIMESTAMP` stamps | Every wait timed as in an up-to-date group; stamps sent from the window were one wrap behind. 2026-09-29 |
| **E3** | `e3-workaround-keeper-cog-test.spin2`, `e3-workaround-waiting-cog-test.spin2` | The keeper, and keepers held in `WAITATN` and `WAITX` | Cogs of 4-7 started after one and two wraps read current; with no keeper, one behind. 2026-09-26 and 2026-09-27 |
| **E4** | `e4-getxacc-clear-gating-test.spin2` | `GETXACC` with the streamer idle, in a non-Goertzel mode, and inside a Goertzel burst | All 50 idle and non-Goertzel reads returned the accumulators unchanged; a read inside a burst cleared, and split the burst exactly. 2026-09-24, run twice |
| **E5** | `e5-goertzel-one-clock-lag-test.spin2` | How many terms a reading after a burst holds, and where the last term goes | N-1 terms, in all 16 sequences; the last term arrived with the next Goertzel burst. 2026-09-24, run twice |
| **E5** | `e5-goertzel-sinc2-iteration-count-test.spin2` | Not an erratum: the documented SINC2 constraint, and its two remedies | Both remedies held. 2026-09-25, run twice |
| **E4, E5** | `e4-e5-workaround-read-sums-test.spin2` | `burst_sums` for bursts of 1 to 1001 clocks, at both input levels | Exactly N terms on both sums in all 60 calls. 2026-09-26 |
| **E6** | `e6-dac-mode-adc-enable-test.spin2` | Whether `OUT` runs the ADC in DAC noise mode at `TT` = `%00` and at `%01`; the `%01` word is the workaround | At `%00` the ADC never ran; at `%01` it ran in every sample. 2026-09-25, run twice |
| **E7** | `e7-rdfast-blocking-after-no-wait-test.spin2`, `e7-next-hub-instruction-test.spin2`, `e7-every-hub-width-test.spin2` | Hub reads, writes, block reads and a waiting `RDFAST`, 2 to 44 clocks after a no-wait `RDFAST`, in every hub alignment | Released below 16 clocks, by alignment; none from 16 clocks on; the waiting form released nothing. 2026-09-25 and 2026-10-01 |
| **E7** | `e7-workaround-hub-access-test.spin2`, `e7-workaround-rdfast-spacing-test.spin2`, `e7-workaround-setq-block-test.spin2` | The printed blocks, the waiting form, and 16 to 20 clocks before a block read | Correct in every alignment and trial. 2026-09-26 and 2026-10-01 |

The archive copies are the programs that ran, prepared for readers: each carries a new file header, and internal labels are replaced by erratum numbers. Every measuring routine assembles to the same bytes as the program that ran. The archive copies were run again on P2 hardware, and every analysed value, class and verdict matched the original runs. The only other differences were the ones any two runs show: the E6 test's count of the running ADC's toggles, and the SINC2 test's deliberately jittered arms.

## How to run them {#sec-a-run}

1. Compile with DEBUG enabled: `pnut-ts -d <file>.spin2` (or PNut with DEBUG).
2. Download to RAM on a bare P2 board, with a reset. The E3 programs check that the counter starts from zero, so the download must reset the part.
3. Watch the DEBUG terminal. Each program ends with its verdict line, or prints `RIG FAIL` and no verdict if a control fails.
4. For `e3-debug-timestamp-test.spin2` only: save the DEBUG log and run `python3 e3-debug-timestamp-verdict.py` on it. The program cannot read its own stamps; the script prints their verdict.

**Pins.** The E4 and E5 programs drive P3, so P3 must be free. The E6 test drives P4 and reads it through P5, so both must be free and unconnected. The others use no pins.

**Running time.** The E3 programs wait for the counter's lower long to wrap, 2^32^ clocks (21.47 s at 200 MHz) each time, and run for 44 s to 216 s after reset. The others finish within about 25 s, most within a second or two.


