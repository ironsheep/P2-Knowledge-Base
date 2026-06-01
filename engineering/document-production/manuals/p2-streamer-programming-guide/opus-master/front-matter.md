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
\vspace{0.6cm}
{\fontsize{36}{42}\selectfont\bfseries P2 Streamer Programming Guide\par}
\vspace{0.3cm}
{\Large\itshape Comprehensive Reference for Propeller 2 Streamer Hardware\par}
\vspace{0.6cm}
{\large June 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.0\par}

\vfill
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
\textbf{High-Speed I/O, Video, and Signal Processing with the P2 Streamer}

\vspace{0.3cm}
\begin{minipage}[t]{0.45\textwidth}
\textbf{Part I: Streamer Fundamentals}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Introduction and Overview
\item Architecture
\item NCO and Timing
\item Command Structure
\end{itemize}
\vspace{0.3cm}
\textbf{Part II: Mode Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Immediate Modes
\item RDFAST Modes
\item RGB Video Modes
\item WRFAST Input Modes
\item ADC Sampling Modes
\item DDS/Goertzel Mode
\end{itemize}
\vspace{0.3cm}
\textbf{Part III: Configuration Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item DAC Channel Configuration
\item Pin Selection and Control
\item Programming Constants
\item Events and Synchronization
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.50\textwidth}
\textbf{Part IV: Applications}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Video Output (VGA, HDMI, Composite)
\item High-Speed Serial (SPI)
\item Signal Processing
\item Integration Patterns
\end{itemize}
\vspace{0.3cm}
\textbf{Part V: Appendices}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Complete Mode Encoding Table
\item Symbol Quick Reference
\item Frequency Calculation Tables
\item Troubleshooting Guide
\item Index
\end{itemize}
\end{minipage}
\end{tcolorbox}
\vspace{0.5cm}

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

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

To view the full license, visit: https://creativecommons.org/licenses/by-sa/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.

## Acknowledgments

This guide would not exist without the contributions of many individuals and organizations:

**Parallax Inc.** for creating the Propeller 2 microcontroller and providing the comprehensive reference documentation that forms the foundation of this work.

**Chip Gracey** for the design of the P2 streamer, NCO, and colorspace converter, and for maintaining the detailed silicon documentation that defines their behavior.

**The P2 Community** for the video, audio, and signal-processing drivers whose real-world usage informed the examples and patterns in this guide.

## Sources

This guide draws on the following primary and community sources:

- **P2 Silicon Documentation v35** (Chip Gracey, Parallax Inc.) — streamer architecture, mode encodings, NCO and DDS/Goertzel behavior
- **Spin2 Documentation v51** (Parallax Inc.) — built-in streamer symbols and language integration
- **P2 Flash Loader source** (official P2 ROM) — verified instruction usage
- **Community video and Goertzel drivers** (Parallax OBEX) — application patterns

## How to Use This Guide

This reference serves developers implementing high-speed I/O on the Propeller 2. It assumes familiarity with P2 COG/Hub architecture, basic PASM2 instructions, and RDFAST/WRFAST FIFO operations.

**Structure:**

- **Part I (Fundamentals)** establishes the mental model — read this first to understand how the streamer operates
- **Part II (Mode Reference)** documents all streamer modes — use for specific mode lookup
- **Part III (Configuration)** covers cross-cutting concerns — DAC routing, pin selection, symbols
- **Part IV (Applications)** provides implementation patterns — video, SPI, signal processing
- **Appendices** contain quick-reference tables and troubleshooting guidance

## Document Conventions

| Element | Format | Example |
|---------|--------|---------|
| Instructions | Bold uppercase | **XINIT**, **XCONT** |
| Symbols | Monospace | `X_RFWORD_RGB16` |
| Bit fields | Brackets | D[31:28], S[19:16] |
| Binary | Percent + underscores | `%1011_0000` |
| Hexadecimal | Dollar prefix | `$B085_0000` |

## Enhancement Markers

- ⚠️ **Pitfall:** Common mistakes with non-obvious consequences
- 💡 **Tip:** Non-obvious techniques or optimizations
- 🔧 **Hardware:** Silicon-level details affecting usage

```{=latex}
\clearpage
```
