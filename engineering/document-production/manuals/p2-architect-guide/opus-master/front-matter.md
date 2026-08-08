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
{\fontsize{36}{42}\selectfont\bfseries The P2 Architect's Guide\par}
\vspace{0.3cm}
{\Large\itshape Thinking in Cogs, Pins, and Forces\par}
\vspace{0.35cm}
{\large July 2026\par}
\vspace{0.2cm}
{\large Version 1.0.3\par}

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
\textbf{From a project idea to a realized build — designing the system, decomposing it onto the P2, and doing it with an AI agent's help.}

\vspace{0.1cm}
{\footnotesize
\begin{minipage}[t]{0.46\textwidth}
\textbf{The Three Acts}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Act I — Getting a Project Off the Ground
\item Act II — Thinking in P2 (Functional Decomposition)
\item Act III — The Same Work, with an Agent
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.46\textwidth}
\textbf{Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Appendix A — Computing in Space and Time
\item Appendix B — Further Reading
\item Glossary
\item Where to Next
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

This guide is a distillation, not a primary source. It draws on, and points you back to, these trusted P2 documents:

- **Getting Started with the Propeller 2** — this guide's companion and **prerequisite**; it teaches the orientation (the chip, and how to read its code) that this guide assumes.
- **The Parallax Propeller 2 Documentation (v35, Rev B/C)** (Chip Gracey, Parallax Inc.) — the architectural ground truth behind the hardware design of Act I and the decomposition of Act II.
- **The P2 reference manuals** (Assembly Language, I/O & Smart Pins, Streamer, Debug) — the depth this guide deliberately leaves to them (see *Where to Next*).

## How to Use This Guide

This is a short, narrative guide, not a reference manual — it is meant to be *read*. It assumes you have already met the Propeller 2; if you haven't, its companion **Getting Started with the Propeller 2** is the place to begin. This guide moves in **three acts**, and different readers can enter at different doors:

- **Building a real system?** Read straight through. **Act I** gets the project off the ground — choosing the hardware and buses, spending the pin budget, getting the parts to talk. **Act II** derives the software architecture — which cog owns what, how the pieces talk. **Act III** walks the whole process again with an AI agent at your side.
- **Already have a hardware design and need the software architecture?** Go straight to **Part II** (Chapter 5) — the functional-decomposition method — and use Part I as reference.
- **Curious how an AI agent changes the work?** **Part III** (Chapters 10–14) revisits every step of the process with an agent in the loop — where it helps, and where judgment stays yours.
- **Coming from the Propeller 1?** Follow the bronze **"P1 note"** sidebars wherever a design decision differs from the P1.

## Conventions

A few conventions run through the whole guide:

- **"cog," never "CPU" or "core."** The P2 community treats a cog as *the computer*, and so do we.
- **Code shows named constants, not raw numbers.** Examples use the compiler's symbolic constants (a pin's name, `_clkfreq`) the way you'd actually write them — and every code example compiles.
- **Code blocks are colored by language** — Spin2 in **blue**, PASM2 (assembly) in **green** — the same IDE-aligned scheme as the rest of the P2 manual family, so code is recognizable at a glance.
- **"P1 note" sidebars** (bronze boxes) are short asides for readers migrating from the Propeller 1, each labeled *same as P1*, *changed in P2*, or *new in P2*. A newcomer can skip every one of them without losing the thread.
- **Inline markers are used sparingly** — 💡 **Tip** for a non-obvious orientation insight, ⚠️ **Watch out** for a genuine pitfall. This is a narrative guide, not a reference peppered with boxes.

```{=latex}
\clearpage
```
