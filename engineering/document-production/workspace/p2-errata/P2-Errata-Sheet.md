```{=latex}
\pagestyle{empty}
\begin{center}
{\fontsize{26}{30}\selectfont\bfseries \DocTitle\par}
\vspace{0.15cm}
{\large\itshape \DocSubtitle\par}
\vspace{0.15cm}
{\normalsize \DocDate\ \textperiodcentered\ {\color{blue}Version \DocVersion}\par}
\vspace{0.1cm}
{\normalsize\bfseries\color{red!70!black} Community Review Draft \textperiodcentered\ Build 2026-10-03\par}
\vspace{0.1cm}
{\scriptsize Copyright \textcopyright\ 2026 Iron Sheep Productions, LLC and Parallax Inc. Licensed under CC BY-SA 4.0 (\url{https://creativecommons.org/licenses/by-sa/4.0/}). Parallax, Propeller, Spin and the Parallax logo are trademarks of Parallax Inc.\par}
\end{center}
\vspace{0.2cm}
```

This sheet lists the silicon errata of the Propeller 2 found so far, and for each one, who meets it, what it looks like and what to do. Each erratum has the same number and the same summary in the guide *P2 Errata*, which explains it, prints a workaround proven on P2 hardware, and says how it was confirmed. Every erratum here was confirmed on Rev C silicon. Erratum numbers are permanent.

# Which errata can affect your program {#sh-which}

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

# Find an erratum by symptom {#sh-symptoms}

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

# The errata {#sh-errata}

## Erratum E1: SETQ Block Transfers Lose Their Pointer Step {#sh-e1}

::: caution
**Who meets it:** PASM2 that places an instruction between a `SETQ` or `SETQ2` and the block `RDLONG`, `WRLONG` or `WMLONG` it prepares, when the transfer updates `PTRx` (for example `ptra++`). Parallax names `ALTx`, `AUGS` and `AUGD` in that position. A `##` operand on the transfer puts one there without your writing it: the assembler places its `AUGS` directly before the transfer, after the `SETQ`.

**What you see:** the whole block moves, but `PTRx` steps as for a single long (`ptra++` moves it by 4), not past the block.

**What to do:** write the `SETQ` or `SETQ2` directly before the transfer, and keep `##` operands off a block transfer that updates `PTRx`.
:::

## Erratum E2: An Immediate ALTx Takes a Pending AUGS {#sh-e2}

::: caution
**Who meets it:** PASM2 that writes an `AUGS` explicitly and places an `ALTx` with an immediate `#S` (such as `ALTD idx,#base`, or the one-operand `ALTD idx`) between it and the instruction it was written for. A `##` literal never produces this arrangement: the assembler places its `AUGS` directly before the instruction that carries the `##`.

**What you see:** the `ALTx` takes the augment as well, and its `D` register moves by bits 17:9 of the augmented value. The redirect and the target's value are correct.

**What to do:** give that `ALTx` a register `S`.
:::

## Erratum E3: GETCT Returns a Stale Upper Long {#sh-e3}

::: caution
**Who meets it:** a program that reads a 64-bit time (`GETCT WC`, `GETMS()`, `GETSEC()`, or a `DEBUG_TIMESTAMP` stamp) in a cog of 4-7 that it starts more than 2^32^ clocks after reset (21.47 s at 200 MHz). The same applies to either group of four cogs once all of its cogs have stopped and a cog starts there again after a wrap of the counter's lower long.

**What you see:** that time reads behind by 2^32^ clocks for each wrap the group missed, until the group's next wrap, at most 2^32^ clocks later. Plain `GETCT` and every wait on the counter time correctly.

**What to do:** start a cog in 4-7 on the first line of `main()` and never stop it.
:::

## Erratum E4: GETXACC Clears Only During a Goertzel Burst {#sh-e4}

::: caution
**Who meets it:** PASM2 that runs DDS/Goertzel bursts one at a time, with the streamer idle between them, and relies on `GETXACC` to clear the accumulators.

**What you see:** with the streamer idle, `GETXACC` returns the sums but clears nothing, so each burst adds to what earlier bursts left and each reading is a running total.

**What to do:** take each burst's sums as the difference of two readings taken with the streamer idle, one before the burst and one after it. The `burst_sums` routine does this, and steps around Erratum E5 as well.
:::

## Erratum E5: The Goertzel Accumulators Trail by One Clock {#sh-e5}

::: caution
**Who meets it:** the same programs as Erratum E4: a `GETXACC` reading taken after each DDS/Goertzel burst.

**What you see:** each reading lacks the burst's last term. That term is added on the first clock of the next Goertzel burst.

**What to do:** run a short burst whose terms are all zero before you read. The `burst_sums` routine, shared with Erratum E4, does this in SINC1 mode.
:::

## Erratum E6: In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC {#sh-e6}

::: caution
**Who meets it:** a pin in a DAC smart-pin mode (`%SSSSS` = `%00001` to `%00011`) configured with `TT` = `%00`, whose ADC the program switches on with `OUT`.

**What you see:** raising `OUT` does not start the ADC.

**What to do:** set `TT` bit 0 (`$40` in the `WRPIN` word, `P_TT_01` in Spin2). The pin's DAC then drives the pin while the ADC runs.
:::

## Erratum E7: After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early {#sh-e7}

::: caution
**Who meets it:** PASM2 that starts the hub FIFO with a no-wait `RDFAST` (`D[31]` = 1) and starts another hub instruction fewer than 16 clocks later: a hub read or write, a `SETQ` block read, or a waiting `RDFAST`. Code that does other work in between, or uses the waiting form, does not meet it.

**What you see:** that instruction can complete early. A read returns the previous hub read's data, with that value's flags; a write is lost if a hub read follows it at once; a block read writes wrong data, or the cog stops responding; a waiting `RDFAST` does not wait. Whether it happens depends on hub alignment, so the same code can work on one pass and fail on the next.

**What to do:** allow at least 16 clocks from the start of the no-wait `RDFAST` to the next hub instruction (`WAITX #12` directly after it, or seven two-clock instructions), or use the waiting form.
:::
