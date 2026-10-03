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
