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
\vspace{0.3cm}
{\fontsize{36}{42}\selectfont\bfseries P2 Diagnostics Handbook\par}
\vspace{0.3cm}
{\Large\itshape Getting Output Out, Supervising a Run, and Trusting What You Measure\par}
\vspace{0.3cm}

\begin{tcolorbox}[
  colback=red!5,
  colframe=red!60!black,
  boxrule=1.5pt,
  width=0.85\textwidth,
  center,
  halign=center
]
{\Large\bfseries\color{red!60!black} PROTOTYPE --- SHAPE REVIEW\par}
\vspace{0.1cm}
{\large Build \DocDate{} \quad\textperiodcentered\quad Version \DocVersion{}\par}
\vspace{0.1cm}
{\small This build shows the handbook's full outline, its Symptom Map, and one
finished chapter (Chapter 2). The other chapters are outlined, not written.
It is not a release.\par}
\end{tcolorbox}

\vspace{0.2cm}
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Handbook Organization},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{Start at the Symptom Map: find what you are seeing, and it sends you to the section that deals with it.}

\vspace{0.1cm}
{\footnotesize
\begin{minipage}[t]{0.46\textwidth}
\textbf{The Three Parts}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Part I --- Getting Output Out (Ch 1--4)
\item Part II --- Supervising a Run (Ch 5--10)
\item Part III --- Trusting What You Measure (Ch 11--18)
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.46\textwidth}
\textbf{Front Door \& Next}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Symptom Map --- the way in
\item Where to Next --- the companion guides
\end{itemize}
\end{minipage}
}
\end{tcolorbox}
\vspace{0.1cm}

{\small Iron Sheep Productions, LLC\par}
{\small P2 Knowledge Base Project\par}
\end{center}

\clearpage
\pagestyle{fancy}

\tableofcontents
\clearpage
```

# Copyright and License

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

This handbook stands on work done by others:

**Parallax Inc.** for the Propeller 2 microcontroller, its Spin2 language and debugger, and the reference documentation that defines their behavior.

**Chip Gracey** for designing the P2 and its built-in debugging system.

**The P2 developers** who shared the debugging and instrumentation techniques they learned the hard way, so that others need not learn them the same way.

## Sources

The facts in this handbook come from, and point back to:

- **Parallax Propeller 2 Spin2 Language Documentation (v55)** (Parallax Inc.) — the DEBUG system, its configuration symbols, and its use of hub memory, pins and locks.
- **The pnut-ts compiler** — its listing is the authority for the debug limits, which this handbook deliberately does not state as numbers (see *Conventions*).

## How to Use This Handbook

This is a handbook for the moment something has gone wrong: a board that prints nothing, a run that seems to hang, a number that cannot be right. It is built to be entered at the symptom, not read from the front.

- **Something is wrong right now?** Go to the **Symptom Map**. Find the row that matches what you are seeing; it names the section that deals with it.
- **Building a debug build for a large program?** Read **Part I**, *Getting Output Out*, before you need it. Chapter 2 shows how to stay inside the compiler's debug limits without giving up the information you need.
- **Building a test rig or a long-running characterization?** Read **Part II**, *Supervising a Run*: how to build a run that reports what happened, even when what happened is a failure.
- **About to believe a measurement?** Read **Part III**, *Trusting What You Measure*: how the debugger, the build, the instrument and the transcript can each mislead, and how to check them.
- **An AI agent or tool?** Use the Symptom Map the same way: match the symptom, then read the section it names before acting.

Pin, smart-pin and streamer techniques belong to their own guides. Where a diagnosis turns on them, this handbook points you there (see *Where to Next*).

## Conventions

- **"cog," never "CPU" or "core."**
- **The compiler states its own limits.** The number of debug records, the size of one record and the total DEBUG data are limited by the compiler, and the figures can change from one release to the next. This handbook never quotes them: read them from your own compiler's listing, as Chapter 2 shows.
- **Code compiles.** Every Spin2 example compiles with `pnut-ts`; examples that use `debug()` compile with `pnut-ts -d`. Each example's file name appears under its listing.
- **Code blocks are colored by language** — Spin2 in **blue**, PASM2 in **green** — and terminal commands are shown in their own style.

```{=latex}
\clearpage
```
