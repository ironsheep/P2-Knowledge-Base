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
{\large June 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 0.1.0 — First Draft\par}

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
\textbf{A short orientation to the Propeller 2 — and how to think in its parallel grain.}

\vspace{0.1cm}
{\footnotesize
\begin{minipage}[t]{0.46\textwidth}
\textbf{The Three Chapters}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Ch 1 — Meet the Propeller 2
\item Ch 2 — Putting It to Work
\item Ch 3 — Thinking in P2 (Functional Decomposition)
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

This work is licensed under the Creative Commons Attribution–NonCommercial–NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made (for example, formatting or excerpting).
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, translate, or build upon the material, you may not distribute the modified material.

**Commercial use:** For uses that may be commercial (including paid courses, kits, or redistribution with products), please contact Iron Sheep Productions, LLC and Parallax Inc. (info@ironsheep.biz) for separate permission.

To view the full license, visit: https://creativecommons.org/licenses/by-nc-nd/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.

## Acknowledgments

This guide stands on work done by others:

**Parallax Inc.** for the Propeller 2 microcontroller and the reference documentation that defines its behavior.

**Chip Gracey** for designing the P2 — the eight-COG architecture, the smart pins, the CORDIC solver, and the streamer this guide teaches you to think with.

**The P2 community** whose drivers, projects, and hard-won design habits shaped how this guide frames "thinking in P2."

## Sources

This guide is a distillation, not a primary source. It draws on, and points you back to, the trusted documents of the P2 Knowledge Base:

- **The P2 Silicon Documentation** (Chip Gracey, Parallax Inc.) — the architectural ground truth behind Chapters 1–2.
- **The P2 Knowledge Base decomposition reasoning layer** — the golden home for Chapter 3's forces, planes, and worked derivation; the chapter derives from it and does not drift.
- **The P2 reference manuals** (Assembly Language, I/O & Smart Pins, Streamer, Debug) — the depth this orientation deliberately leaves to them (see *Where to Next*).

## How to Use This Guide

This is a short, narrative guide, not a reference manual — it is meant to be *read*, and it is built so different readers can enter at different doors. Four paths:

- **New to the Propeller 2?** Read straight through: Chapter 1 builds the mental picture, Chapter 2 puts it to work in real (compiling) code, and Chapter 3 — the decomposition method — is there when you're ready for it. Take the chapters in order; each earns the next.
- **Coming from the Propeller 1?** You already own the model. Skim Chapter 1 following the bronze **"P1 note"** sidebars — they call out exactly what's *the same*, *changed*, or *new* on the P2 — then jump to Chapter 3 for the decomposition method, using Chapter 2 as a Spin2/PASM2 refresher.
- **Already writing P2 code?** Go straight to Chapter 3. It's the reason this guide exists: how to look at a whole machine and derive the right set of cooperating COGs and objects, rather than build an accidental sequential program on parallel silicon. Keep Chapters 1–2 as reference.
- **An AI agent or tool?** The authoritative, machine-readable form of this material is the P2 Knowledge Base itself — in particular the decomposition reasoning layer that is Chapter 3's golden home. Read this guide for the narrative; consume the YAML for the facts.

## Conventions

A few conventions run through the whole guide:

- **"COG," never "CPU" or "core."** The P2 community treats a COG as *the computer*, and so do we.
- **Code shows named constants, not raw numbers.** Examples use the compiler's symbolic constants (a pin's name, `_clkfreq`) the way you'd actually write them — and every code example compiles.
- **Code blocks are colored by language** — Spin2 in **blue**, PASM2 (assembly) in **green** — the same IDE-aligned scheme as the rest of the P2 manual family, so code is recognizable at a glance.
- **"P1 note" sidebars** (bronze boxes) are short asides for readers migrating from the Propeller 1, each labeled *same as P1*, *changed in P2*, or *new in P2*. A newcomer can skip every one of them without losing the thread.
- **Inline markers are used sparingly** — 💡 **Tip** for a non-obvious orientation insight, ⚠️ **Watch out** for a genuine pitfall. This is a narrative guide, not a reference peppered with boxes.

```{=latex}
\clearpage
```
