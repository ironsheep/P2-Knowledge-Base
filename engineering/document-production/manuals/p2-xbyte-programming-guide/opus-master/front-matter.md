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
{\Large\itshape Skip Patterns, Bytecode Dispatch, and the XBYTE Engine on the Propeller 2\par}
\vspace{0.35cm}
{\large August 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.1.0\par}

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
\item What This Kind of Emulation Asks of You
\end{itemize}
\vspace{0.03cm}
\textbf{Part II: Dispatch on the P2}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Understanding XBYTE
\item The Skip Family
\item The Bytecode Stream
\item LUT Dispatch
\end{itemize}
\vspace{0.03cm}
\textbf{Part III: Choosing Your Rung}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item The Three Decisions
\item What Will Hurt — A Guest-CPU Survey
\end{itemize}
\vspace{0.03cm}
\textbf{Part IV: The XBYTE Engine}
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
\textbf{Part V: Building Interpreters and Emulators}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item A Minimal Custom VM
\item Growing the VM
\item A Tiny CPU Emulator (6502)
\item Servicing Guest Interrupts
\item Prefixes and Alternate Tables
\item XBYTE Beyond Interpreters
\end{itemize}
\vspace{0.03cm}
\textbf{Part VI: Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Instruction Reference
\item Configuration Constants \& Patterns
\end{itemize}
\vspace{0.03cm}
\textbf{Part VII: Appendices}
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

This guide serves developers building interpreters, virtual machines, and CPU emulators on the Propeller 2. It assumes familiarity with P2 cog/hub/LUT architecture, basic PASM2, and the hub FIFO (`RDFAST` and the `RFxxxx` reads).

**Structure:**

- **Part I (The Landscape)** builds the picture before any mechanism — what this kind of emulation is, why the P2 is unusually good at it, and what it will ask of you. It names no P2 machinery. Read it first; skim it if you have built emulators before.
- **Part II (Dispatch on the P2)** teaches the machinery that *both* dispatch approaches share — XBYTE in outline, the skip family (SKIP/SKIPF/EXECF), the bytecode stream, and LUT dispatch. It is named for the machinery rather than the engine on purpose.
- **Part III (Choosing Your Rung)** is the decision. With the machinery understood, it walks the three-rung dispatch ladder and surveys what each classic guest CPU will cost you. **Most P2 emulator authors land on rung 2 — hand-rolled dispatch — and this Part is where you find out whether you are one of them.**
- **Part IV (The XBYTE Engine)** is the engine reference for a reader whose decision landed on rung 3: the dispatch cycle, arming, the table-size and compression modes, the rules a bytecode routine follows, and how to debug a hardware dispatch loop.
- **Part V (Building Interpreters and Emulators)** builds, in rungs of difficulty: a minimal VM, that same VM grown until its dispatch table has to work for a living, a tiny 6502, guest interrupts, prefix bytes, and then the same engine used well outside interpreters.
- **Part VI (Reference)** is quick lookup for the instructions and the configuration bits.
- **Part VII (Appendices)** holds the quick-reference cards, the encoding summary, pointers to community implementations, and troubleshooting.

The 6502 emulator in Part V is deliberately **tiny and illustrative** — enough to show the technique end to end, not a faithful or complete emulator. Three programs in this guide are complete and compile: the minimal VM of Chapter 14, the grown VM of Chapter 15, and the display-list engine of Chapter 19.

### Three ways in

**Path 1 — you are new to dispatch on the P2.** Read Part I, then Part II, then Part III, in order. That is the shortest route to knowing what XBYTE is and whether you want it. Part IV becomes reference material you return to; Part V is where you build.

**Path 2 — you have a project in mind.** Go to the **Intent Index** below, find the thing you are building, and start where it points. Come back to Part III before you commit to an approach — it is the Part that will tell you to *not* use the full engine, which is the answer for more projects than not.

**Path 3 — you have a specific question.** Part IV is the engine reference and Part VI is the instruction and configuration lookup. **Appendix A** is the one-page card: the dispatch cycle, every table-size operand, and the arming checklist. If you know the mechanism and want the numbers, start there and ignore the rest of the book.

## The engine in brief

The rest of this guide takes its time. This page does not — it is the whole mechanism in one place, for a reader who wants the shape before the detail.

**XBYTE is a hardware bytecode dispatch loop.** Once armed, the cog repeats a cycle you never write: fetch the next byte from the hub FIFO, use it to index a table in LUT RAM, and jump to the handler that entry names — carrying a skip pattern that tailors the handler as it runs. Your handler ends in `RET`, and that return is what triggers the next fetch. There is **no loop body**, because the loop is the silicon.

The cycle costs **8 clocks, 6 of them overhead** (Chapter 9), against 9 for the tightest equivalent written by hand. That margin — 6 versus 9 — is the whole economic argument for the engine, and Chapter 7 is where you decide whether it applies to you.

Arming takes four steps, and the shape rarely varies:

```pasm2
                setq2   #256-1              ' load the dispatch table
                rdlong  $100, ##disp_table  '   into LUT $100..$1FF
                rdfast  #0, ##program       ' FIFO -> the bytecode stream
                push    #$1ff               ' the return target every
                                            '   handler comes back to
        _ret_   setq    #$100               ' arm - XBYTE runs from here
' Execution never returns here; a handler leaves the loop by not returning.

h_example                                   ' a handler is ordinary PASM2
                rfvar   value               ' read an inline operand
        _ret_   add     total, value        ' _RET_ = back to dispatch
```

The `PUSH #$1FF` is not optional and a `CALL` will not substitute for it (§10.1). The value handed to `SETQ` is the **mode operand**, which packs three independent choices — where the table sits in LUT, how big it is, and whether dispatch writes the flags (Chapter 11).

That is the engine. **Appendix A** carries the same material as a lookup card — the cycle clock by clock, every table-size operand, and the arming checklist — and Chapters 9 through 12 are the full reference.

## Intent Index

Find what you are building. The chapters named are the ones to read closely first; everything else can wait.

> **I want to build a bytecode VM or scripting language**
> → **Chapter 14: A Minimal Custom VM**, then **Chapter 15: Growing the VM**
> → Specifically: the whole engine, which is what it was designed for
> → Also consider: Chapter 12 for the rules a handler follows

> **I want to emulate a CPU**
> → **Chapter 7: The Three Decisions**, then **Chapter 8: What Will Hurt**
> → Specifically: read these *before* writing a line — for many guests you can take only one of the engine's two assets
> → Also consider: Chapter 16 for the worked 6502, Chapter 17 for guest interrupts

> **I want to parse a terminal or ANSI escape stream**
> → **§19.3** — the table as state
> → Specifically: `ESC` borrows an alternate table for the next byte
> → Also consider: Chapter 18, which is what alternate tables are for

> **I want to decode MIDI or a protocol**
> → **§19.4** — the byte as data
> → Specifically: the channel or message type rides in `PA`
> → Also consider: §11.3, compression, when a family of codes shares one handler

> **I want to drive a graphics display list**
> → **§19.5** — the stream as a movable cursor
> → Specifically: a "jump" command is an `RDFAST` to a new address
> → Also consider: Chapter 5, for reading inline parameters out of the stream

> **I want to decode a binary format or TLV structure**
> → **§19.2** — the byte as a type tag
> → Also consider: §19.7, which is honest about when this is the wrong tool

> **I want to sequence events or animation**
> → **§19.2** — seek, so the read cursor loops and branches for free
> → Also consider: §12.3, re-pointing the stream from inside a handler

> **I want to do something else that walks a byte stream**
> → **§3.5** for the general test, then **§19.7** for where it stops paying
> → Also consider: Appendix C, for what working projects chose *not* to use the engine for

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
