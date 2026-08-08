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
{\fontsize{36}{42}\selectfont\bfseries Getting Started with the Propeller 2\par}
\vspace{0.3cm}
{\Large\itshape Meet the Chip, Read Its Code, Put It to Work\par}
\vspace{0.35cm}
{\large July 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.0.3 — Community Review Edition\par}

\vspace{0.25cm}
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Guide Organization},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{A short, friendly orientation to the Propeller 2 — meet the chip, learn to read its code, and put it to work.}

\vspace{0.1cm}
{\footnotesize
\begin{minipage}[t]{0.46\textwidth}
\textbf{The Three Chapters}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Ch 1 — Meet the Propeller 2
\item Ch 2 — Reading P2 Code
\item Ch 3 — Putting It to Work
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.46\textwidth}
\textbf{Back Matter \& Next}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Where to Next — the reference library
\item Then: \textit{The P2 Architect's Guide}
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

This guide stands on work done by others:

**Parallax Inc.** for the Propeller 2 microcontroller and the reference documentation that defines its behavior.

**Chip Gracey** for designing the P2 — the eight-cog architecture, the smart pins, the CORDIC solver, and the streamer this guide teaches you to think with.

**The P2 community** whose drivers, projects, and hard-won design habits shaped how this guide frames "thinking in P2."

## Sources

This guide is a distillation, not a primary source. It draws on, and points you back to, these trusted P2 reference documents:

- **The Parallax Propeller 2 Documentation v35 - Rev B/C** (Chip Gracey, Parallax Inc.) — the architectural ground truth behind Chapter 1.
- **The Spin2 Reference Manual and the P2 Assembly Language Reference** — the language facts behind Chapter 2 ("Reading P2 Code").
- **The P2 reference manuals** (Assembly Language, I/O & Smart Pins, Streamer, Debug) — the depth this orientation deliberately leaves to them (see *Where to Next*).

## How to Use This Guide

This is a short, narrative guide, not a reference manual — it is meant to be *read*, and it is built so different readers can enter at different doors. Four paths:

- **New to the Propeller 2?** Read straight through: Chapter 1 builds the mental picture, Chapter 2 teaches you to *read* P2 code (so the examples ahead aren't a mystery), and Chapter 3 puts it to work in real (compiling) code. Take the chapters in order; each earns the next.
- **Coming from the Propeller 1?** You already own the model — and Spin2 will look familiar. Skim Chapter 1 following the bronze **"P1 note"** sidebars — they call out exactly what's *the same*, *changed*, or *new* on the P2 — skim Chapter 2 for what's new in the language, then read Chapter 3 as a hands-on refresher.
- **Already writing P2 code?** Use this guide as a fast orientation and a reference for the chip and its code. When you're ready to design a *whole system* on the P2 — deriving the right set of cooperating cogs and objects rather than an accidental sequential program on parallel silicon — that's the companion volume, *The P2 Architect's Guide*.
- **An AI agent or tool?** Read this guide for the narrative and the mental model — the way an experienced P2 developer thinks. The P2 reference manuals carry the exhaustive, authoritative facts the design decisions rest on.

## Conventions

A few conventions run through the whole guide:

- **"cog," never "CPU" or "core."** The P2 community treats a cog as *the computer*, and so do we.
- **Code shows named constants, not raw numbers.** Examples use the compiler's symbolic constants (a pin's name, `_clkfreq`) the way you'd actually write them — and every code example compiles.
- **Code blocks are colored by language** — Spin2 in **blue**, PASM2 (assembly) in **green** — the same IDE-aligned scheme as the rest of the P2 manual family, so code is recognizable at a glance.
- **"P1 note" sidebars** (bronze boxes) are short asides for readers migrating from the Propeller 1, each labeled *same as P1*, *changed in P2*, or *new in P2*. A newcomer can skip every one of them without losing the thread.
- **Callouts are used sparingly** — the occasional **Tip** box flags a non-obvious orientation insight. This is a narrative guide, not a reference peppered with boxes.

```{=latex}
\clearpage
```
