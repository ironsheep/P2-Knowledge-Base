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
{\large Version \DocVersion\par}

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
\textbf{The Three Parts}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Part I — Getting a Project Off the Ground
\item Part II — Thinking in P2 (Functional Decomposition)
\item Part III — The Same Work, with an Agent
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

{\small \DocAuthor\par}
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
- **The Parallax Propeller 2 Documentation (v35, Rev B/C)** (Chip Gracey, Parallax Inc.) — the architectural ground truth behind the hardware design of Part I and the decomposition of Part II.
- **The P2 reference manuals** (Assembly Language, I/O & Smart Pins, Streamer, Debug) — the depth this guide deliberately leaves to them (see *Where to Next*).

# Preface

The Propeller 2 is well documented at the level of its parts. There is a reference for the Spin2 language and one for the PASM2 instruction set, a user guide for the smart pins, one for the streamer, manuals for the debug windows and the single-step debugger, and Parallax's own documentation for the silicon underneath all of them. Between them they will tell you what every instruction does, what every pin mode does, and what each one costs in time.

None of them will tell you which cog should own what.

That question — how a whole embedded application gets carved across eight independent cogs and sixty-four smart pins — is the one the reference shelf cannot answer, and it is where a P2 design most often goes wrong. It cannot be answered there because the answer is different for every application: it comes from *that* application's wires, rates, and deadlines. What generalizes is not the answer but the **method for deriving one**. Teaching that method is what this book is for.

By the end of it you should be able to sit down with hardware you have never seen — a new sensor, an unfamiliar bus, a deadline tighter than the last one — and derive a sound architecture for it: which cog owns which resource, what each seam between cogs promises, what adapts where two cadences meet, how deep each branch layers, and whether the whole thing fits on the chip. Not recall an architecture that resembles it. Derive one.

The book walks a single journey three times.

**Part I** is the front of a real project — deciding what to build, learning parts nobody documented well, wiring them, proving they talk, making them fast, and shipping them so someone else can pick them up. Not one cog is assigned anywhere in it. It is the work that hands the decomposition its raw material: the parts, the pin map, the rates, and the deadlines.

**Part II** takes that wired-up, understood application and derives its software architecture from it. Four forces do the cutting; a handful of objects guard the whole application rather than sitting in it; a resource budget says when a cut is wrong; four tools judge one candidate cut against another; and a nine-step procedure puts them in order, watched running end to end on two deliberately different applications.

**Part III** walks both of those again with an AI agent in the loop, asking one question at each step: what changes when you have one? The answer is never that the agent decides. It is that most steps get cheaper, and a few things that were out of reach come within it.

Three parts, three acts of one story — but not three equal ones. **Part II is the book's center of gravity**, and considerably its longest; Part I is its approach and Part III its amplifier. That proportion is deliberate, and it is worth knowing before you start.

A few things this book deliberately is not. It is not an orientation manual: **Getting Started with the Propeller 2** is its prerequisite, and this book opens where that one ends — it assumes you can already launch a cog, drive a pin, share data through hub, and choose between Spin2 and PASM2 for a given job. It is not a Spin2 or PASM2 reference and it does not duplicate the subsystem manuals; where you need depth, it names the manual that carries it. It contains no code at all, by design — the mechanics belong to those manuals, and the design reasoning is what this one is for. And it is not prescriptive: it will not tell you what to build, or hand you an architecture to copy. Every worked example in it is one application's answer, shown to make the method visible.

## How to Use This Guide

This is a short, narrative guide, not a reference manual — it is meant to be *read*. It assumes you have already met the Propeller 2; if you haven't, its companion **Getting Started with the Propeller 2** is the place to begin. Different readers can enter at different doors:

- **Building a real system?** Read straight through. **Part I** gets the project off the ground — choosing the hardware and buses, spending the pin budget, getting the parts to talk. **Part II** derives the software architecture — which cog owns what, how the pieces talk. **Part III** walks the whole process again with an AI agent at your side.
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
