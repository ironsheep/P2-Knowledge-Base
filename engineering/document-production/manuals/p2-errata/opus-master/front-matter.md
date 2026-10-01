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
{\large\bfseries\color{red!70!black} Community Review Draft \textperiodcentered\ Build 2026-10-01\par}

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
**The clean-room design study** for predicting errata E3, E4, E5 and E6 from the design material alone, and for the classification of findings this manual follows. The study read the design without Parallax's documentation or a bench; the predictions were then tested on P2 hardware, independently, for this manual. Erratum E7 was first found on the bench, by a test built to measure something else; the study then predicted that the same condition reaches every hub read and write, and the bench confirmed it.

## Sources

- **Parallax Propeller 2 Documentation** (Chip Gracey, Parallax Inc.), the v35 edition (Rev B/C) and the current online edition, which adds the 2024 note on Goertzel SINC2 mode: what the design says, including its KNOWN BUGS section.
- **Parallax Spin2 Language Documentation** (Chip Gracey, Parallax Inc.), v55: what Spin2's `GETMS()` and `GETSEC()` return, and what `DEBUG_TIMESTAMP` stamps (Erratum E3).

These two are the only documents this manual cites for what the P2 is meant to do.
- **Tests on P2 hardware** (P2 Knowledge Base Project): every erratum in this manual was confirmed on **Rev C** silicon, the revision in production, by a test program that is included in the examples archive.
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
| **E3** | GETCT Returns a Stale Upper Long | `GETCT WC`, `GETMS()`, `GETSEC()` and `DEBUG_TIMESTAMP` stamps in a cog whose group of four had no cog running at a wrap of the counter's lower long, until the group's next wrap | No | No 64-bit time inside that window: a cog of the group running at every wrap, or one wrap waited out (a keeper cog started first; one-time startup workaround) |
| **E4** | GETXACC Clears Only During a Goertzel Burst | `GETXACC` while the streamer is idle or in any mode other than Goertzel | No | Take each burst's sums as a difference of idle reads (the `burst_sums` routine, SINC1; helper routine) |
| **E5** | The Goertzel Accumulators Trail by One Clock | every Goertzel burst: its last term is added to the next burst | No | Deliver the held term before reading (the `burst_sums` routine, SINC1; helper routine) |
| **E6** | In a DAC Smart-Pin Mode, OUT Needs TT Bit 0 to Run the ADC | a DAC smart-pin mode with `TT` = `%00` whose ADC is switched with `OUT` | No | `TT` bit 0 set in the `WRPIN` word (rule at each use) |
| **E7** | After a No-Wait RDFAST, the Next Hub Instruction Can Complete Early | a hub read, hub write, `SETQ` block `RDLONG` or waiting `RDFAST` started fewer than 16 clocks after a no-wait `RDFAST` | No | The waiting form of `RDFAST`, or at least 16 clocks from the no-wait `RDFAST` to the next hub instruction (`WAITX #12` directly after the no-wait one; rule at each use) |

## Find an Erratum by Symptom

Each row is a symptom a program can show, and the erratum that produces it. An erratum with several symptoms has a row for each; its CAUTION box names them all.

| Symptom | Erratum |
|---|---|
| After a `SETQ` or `SETQ2` block transfer through `PTRx++`, with an `ALTx`, `AUGS` or `AUGD` between the `SETQ` and the transfer, the pointer moved by one long's step, not the block's | **E1** |
| An `ALTx` with an immediate `#S`, between an `AUGS` and its target, changes its `D` register by bits 17:9 of the augmented value | **E2** |
| `GETCT WC`, `GETMS()`, `GETSEC()` or a `DEBUG_TIMESTAMP` stamp reads behind by 2^32^ clocks (21.47 s at 200 MHz) or a multiple of it | **E3** |
| `GETXACC` read while the streamer is idle does not clear the Goertzel sums, and each burst adds to what the last one left | **E4** |
| A Goertzel burst's sum lacks its last term, and holds the last term of the burst before it | **E5** |
| In a DAC smart-pin mode with `TT` = `%00`, raising `OUT` does not run the pin's ADC | **E6** |
| A `RDBYTE`, `RDWORD` or `RDLONG` after a no-wait `RDFAST` returns the previous hub read's data, with that value's flags | **E7** |
| A `WRBYTE`, `WRWORD` or `WRLONG` after a no-wait `RDFAST` is lost | **E7** |
| A `SETQ` block `RDLONG` after a no-wait `RDFAST` writes one wrong long and changes cog registers outside its destination, or the cog stops responding | **E7** |
| An `RFLONG` returns `$0000_0000` after a waiting `RDFAST` that followed a no-wait `RDFAST` | **E7** |

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
