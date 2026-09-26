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
- **Tests on real P2 parts** (P2 Knowledge Base Project): every erratum in this manual was confirmed on **Rev C** silicon, the revision in production, by a test program that is included in the examples archive.
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
