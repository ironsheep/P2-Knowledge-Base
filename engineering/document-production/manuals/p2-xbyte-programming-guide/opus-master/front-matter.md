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
{\fontsize{36}{42}\selectfont\bfseries P2 Interpreters \& Emulators Guide\par}
\vspace{0.3cm}
{\Large\itshape The XBYTE Engine and Bytecode Dispatch on the Propeller 2\par}
\vspace{0.35cm}
{\large July 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.0.0\par}

\vspace{0.1cm}
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
\textbf{The P2's Hardware Bytecode-Execution Engine}

\vspace{0.08cm}
{\footnotesize
\begin{minipage}[t]{0.45\textwidth}
\textbf{Part I: The Landscape}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Why Emulate on the P2
\item What Emulation Asks of You
\end{itemize}
\vspace{0.03cm}
\textbf{Part II: XBYTE Fundamentals}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Understanding XBYTE
\item The Skip Family
\item The Bytecode Stream
\item LUT Dispatch
\end{itemize}
\vspace{0.03cm}
\textbf{Part III: The XBYTE Engine}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item The Dispatch Cycle
\item Arming XBYTE
\item Table-Size \& Compression Modes
\item Bytecode Routines
\item Debugging XBYTE
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.50\textwidth}
\textbf{Part IV: Building Interpreters and Emulators}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item A Minimal Custom VM
\item The Three Decisions
\item What Will Hurt — A Guest-CPU Survey
\item A Tiny CPU Emulator (6502)
\item Servicing Guest Interrupts
\item Prefixes \& Alternate Tables
\item XBYTE Beyond Interpreters
\end{itemize}
\vspace{0.03cm}
\textbf{Part V: Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Instruction Reference
\item Configuration Constants \& Patterns
\end{itemize}
\vspace{0.03cm}
\textbf{Part VI: Appendices}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item A: XBYTE Quick Reference
\item B: Instruction Encoding Summary
\item C: Further Implementations
\item D: Troubleshooting
\item Index
\end{itemize}
\end{minipage}
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
\listoffigures
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

This guide would not exist without the contributions of many individuals and organizations:

**Parallax Inc.** for creating the Propeller 2 microcontroller and providing the comprehensive reference documentation that forms the foundation of this work.

**Chip Gracey** for the design of XBYTE, the skip family, and the LUT/FIFO hardware, and for maintaining the detailed silicon documentation that defines their behavior.

**The P2 Community** for the interpreters, virtual machines, and CPU emulators whose real-world use proves what the engine makes possible.

## Sources

This guide draws on the following primary sources:

- **Parallax Propeller 2 Documentation v35 - Rev B/C** (Chip Gracey, Parallax Inc.) — the XBYTE dispatch cycle, overhead figures, table-size and compression modes, and the F bit
- **P2 Knowledge Base YAML** (Iron Sheep Productions / P2 Knowledge Base Project) — the XBYTE engine reference and the per-instruction encodings for the skip family, the FIFO read instructions, and SETQ/SETQ2

## How to Use This Guide

This guide serves developers building interpreters, virtual machines, and CPU emulators on the Propeller 2. It assumes familiarity with P2 cog/hub/LUT architecture, basic PASM2, and the hub FIFO (RDFAST and the RFxxxx reads).

**Structure:**

- **Part I (The Landscape)** builds the picture before any mechanism — what emulation is, why the P2 is unusually good at it, and the handful of concerns any emulator must handle. It names no P2 machinery. Read it first; skim it if you have built emulators before.
- **Part II (Fundamentals)** builds the mental model of the engine — it teaches the skip family (SKIP/SKIPF/EXECF) before the XBYTE engine, because the engine is built out of them.
- **Part III (The Engine)** is the reference for the dispatch cycle, arming, the table-size and compression modes, the rules bytecode routines follow, and how to debug a hardware dispatch loop.
- **Part IV (Building Interpreters and Emulators)** proves the engine by building — a minimal custom VM — then steps back to the decisions that come *before* any emulator: which of the engine's assets you can take, what each classic guest CPU will cost you, and how to service guest interrupts and prefix bytes. It closes by widening the frame beyond interpreters entirely.
- **Part V (Reference)** is quick lookup for the instructions and the configuration bits.
- **Appendices** contain quick-reference cards, the encoding summary, pointers to community implementations, and troubleshooting.

The 6502 emulator in Part IV is deliberately **tiny and illustrative** — enough to show the technique end to end, not a faithful or complete emulator. The guide's two complete programs — the minimal VM and the display-list engine — do compile.

## Document Conventions

| Element | Format | Example |
|---------|--------|---------|
| Instructions | Bold uppercase | **EXECF**, **SETQ** |
| Registers / symbols | Monospace | `PA`, `PB`, `_RET_` |
| Bit fields | Brackets | D[31:10], D[9:0], b[7:4] |
| Binary | Percent + underscores | `%A000000xF` |
| Hexadecimal | Dollar prefix | `$1F6`, `$1FF` |

## Enhancement Markers

Three colored callout boxes set "things to know" apart from the running text:

- **CAUTION** (amber) — common mistakes with non-obvious consequences
- **TIP** (teal) — non-obvious techniques or optimizations
- **HARDWARE** (graphite) — silicon-level details affecting usage

```{=latex}
\clearpage
```
