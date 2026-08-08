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
{\fontsize{36}{42}\selectfont\bfseries P2 I/O \& Smart Pins User Guide\par}
\vspace{0.3cm}
{\Large\itshape Complete P2 Pin I/O and Smart Pin Reference\par}
\vspace{0.6cm}
{\large July 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.0.8\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} User Guide Organization},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{Complete P2 Smart Pin Documentation}

\vspace{0.3cm}
\begin{minipage}[t]{0.45\textwidth}
\textbf{Part I: Fundamentals}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Direct I/O Basics
\item Enhanced Direct I/O
\item Smart Pin Architecture
\item Configuration Instructions
\item Working with Smart Pins
\end{itemize}
\vspace{0.3cm}
\textbf{Part II: Output Modes}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Digital Output
\item Pulse \& Transition
\item NCO Frequency/Duty
\item PWM Triangle/Sawtooth/SMPS
\item DAC Output
\item Serial Transmit
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.50\textwidth}
\textbf{Part III: Input Modes}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Digital Input
\item Timing Measurement
\item Counting Modes
\item Period/Frequency
\item ADC Input
\item Serial Receive
\end{itemize}
\vspace{0.3cm}
\textbf{Part IV: Special Modes}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Repository Mode
\item USB Support
\end{itemize}
\vspace{0.3cm}
\textbf{Part V: Appendices}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Intent Index
\item P\_ Constants Reference
\item Formulas \& Reference Tables
\item Mode Comparison Charts
\item Troubleshooting Guide
\item Complete Mode Reference
\item FPGA Board Differences
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
\listoffigures
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

## Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc. This license grants permissions under copyright only; it does not grant rights to use these trademarks, and adapted or redistributed copies must not imply endorsement by, or official status with, Iron Sheep Productions, LLC or Parallax Inc.


# Acknowledgments

This guide would not exist without the contributions of many individuals and organizations:

**Parallax Inc.** for creating the Propeller 2 microcontroller and providing comprehensive reference documentation that forms the foundation of this work.

**Chip Gracey** for the brilliant design of the P2 smart pin system and for maintaining detailed technical specifications.

**The P2 Community** for extensive testing, feedback, and real-world usage that has refined our understanding of the smart pin modes and identified critical details worth documenting.

**Jon Titus** for the *Propeller 2 Smart Pin Supplementary Documentation* — a commenting-enabled Google Doc that supplements the *Parallax Propeller 2 Documentation v35 - Rev B/C* with examples and further explanation — whose detailed smart pin mode descriptions informed and enriched much of this guide. Titus is also the historical designer of the 1974 Mark-8, one of the world's earliest personal hobbyist microcomputers.

This guide is a community-developed resource, created to make the P2's smart pin system more accessible to developers at all skill levels.


# How to Use This Guide

The P2 I/O & Smart Pins User Guide supports three distinct reading paths, each designed for different needs:

## Path 1: Learning Path (New to P2 I/O)

Readers unfamiliar with the P2 pin system should progress through Part I sequentially:

1. **Chapter 1: Direct I/O** - Fundamental pin control via DIR, OUT, and IN registers
2. **Chapter 2: Enhanced Direct I/O** - P_ constants for drive strength, input conditioning, and basic analog
3. **Chapter 3: Smart Pin Architecture** - The autonomous I/O concept and state machine
4. **Chapter 4: Smart Pin Configuration** - Configuration instructions and patterns
5. **Chapter 5: Working with Smart Pins** - Common patterns and debugging

After completing Part I, proceed to specific mode chapters in Parts II-IV as needed, using the appendices for reference.

## Path 2: Task-Oriented Path (Know What to Accomplish)

Readers who know what they want to accomplish but not which mode to use should start with **Appendix A: Intent Index**. The Intent Index provides entries in the form:

> **I want to... [task]**  
> → Chapter N: [chapter name]  
> → Specifically: [mode or technique]  
> → Also consider: [alternatives]

The Intent Index covers common tasks including:

- Generating signals (clocks, PWM, analog, serial)
- Measuring signals (timing, counting, analog, serial)
- Controlling outputs (digital, DAC)
- Reading inputs (digital, ADC)
- Communication protocols (SPI, I²C, UART, USB)

## Path 3: Reference Path (Know the Mode)

Readers who know which mode or feature they need can navigate directly:

- **Quick Mode Selection Matrix** (below) - Visual overview of all 32 smart pin modes
- **Appendix F: Complete Mode Reference** - Condensed reference for all modes
- **Chapter index** - Direct chapter access by topic

Each mode chapter stands alone with complete configuration details, all applicable P_ constants, working examples in both Spin2 and PASM2, and decision guidance.


# Document Conventions

## Typography

| Element | Convention | Example |
|---------|------------|---------|
| PASM2 instructions | Bold uppercase | **DRVH**, **WRPIN**, **RDPIN** |
| Spin2 methods | Bold mixed case | **PINHIGH**, **PINREAD**, **WRPIN** |
| P_ constants | Monospace | `P_NCO_FREQ`, `P_HIGH_15K`, `P_OE` |
| Register references | Name with bit range | X[15:0], Z[31] |
| Mode values | Binary with percent prefix | %00110, %11110 |
| Numeric values | Underscores for readability | 200_000_000, 4_294_967_296 |

## Register Notation

The P2 smart pin system uses three internal registers:

| Register | Notation | Description |
|----------|----------|-------------|
| X register | X[31:0] or X[range] | Configuration and parameters |
| Y register | Y[31:0] or Y[range] | Input data or secondary configuration |
| Z register | Z[31:0] or Z[range] | Accumulator / working register |

Bit ranges use the notation X[high:low], where X[31:0] indicates all 32 bits and X[15:0] indicates the lower 16 bits.

## Code Examples

All code examples appear in both Spin2 and PASM2:

**Spin2 Example:**
```spin2
' Example description
WRPIN(PIN, mode_value)    ' Configuration step
WXPIN(PIN, x_value)       ' Parameter setting
PINL(PIN)                 ' Enable Smart Pin
```

**PASM2 Example:**
```pasm2
' Example description
              wrpin     ##mode_value, pin   ' Configuration step
              wxpin     ##x_value, pin      ' Parameter setting
              drvl      pin                 ' Enable Smart Pin
```

## Terminology

| Term | Definition |
|------|------------|
| Direct I/O | Fundamental pin control via DIR, OUT, and IN registers |
| Smart Pin | Autonomous pin mode providing hardware-based I/O functions |
| DIR bit | Direction control (0 = input/disabled, 1 = output/enabled) |
| OUT bit | Output state when DIR = 1 |
| IN bit | Input state or Smart Pin status flag |
| sysclk | System clock frequency (typically 200 MHz) |
| mode bits | The %SSSSS field, bits [5:1] of the WRPIN D value, selecting Smart Pin mode (bit [0] is a separate trailing bit) |

## Cross-References

Cross-references use the format:

- "See Chapter N: Title" for chapter references
- "See Appendix X" for appendix references
- "See MODE_NAME (%XXXXX)" for mode references


# Quick Mode Selection Matrix

The following matrix provides a one-page overview of all 32 smart pin modes organized by function. Use this for quick navigation to the appropriate chapter.

## Output Modes

| Mode | P_ Constant | Mode Bits | Chapter | Description |
|------|-------------|-----------|---------|-------------|
| Normal | `P_NORMAL` | %00000 | Ch 2 | Direct I/O, no Smart Pin (Enhanced Direct I/O) |
| Repository/DAC Noise | `P_REPOSITORY` / `P_DAC_NOISE` | %00001 | Ch 18, Ch 10 | Long repository or DAC noise output |
| DAC Dither RND | `P_DAC_DITHER_RND` | %00010 | Ch 10 | DAC 16-bit random dither |
| DAC Dither PWM | `P_DAC_DITHER_PWM` | %00011 | Ch 10 | DAC 16-bit PWM dither |
| Pulse/Cycle | `P_PULSE` | %00100 | Ch 7 | Pulse or cycle output |
| Transition | `P_TRANSITION` | %00101 | Ch 7 | Timed transition output |
| NCO Frequency | `P_NCO_FREQ` | %00110 | Ch 8 | NCO frequency output (square wave) |
| NCO Duty | `P_NCO_DUTY` | %00111 | Ch 8 | NCO duty cycle output |
| PWM Triangle | `P_PWM_TRIANGLE` | %01000 | Ch 9 | PWM triangle wave output |
| PWM Sawtooth | `P_PWM_SAWTOOTH` | %01001 | Ch 9 | PWM sawtooth wave output |
| PWM SMPS | `P_PWM_SMPS` | %01010 | Ch 9 | Switch-mode power supply PWM |
| Sync Serial TX | `P_SYNC_TX` | %11100 | Ch 11 | Synchronous serial transmit |
| Async Serial TX | `P_ASYNC_TX` | %11110 | Ch 11 | Asynchronous serial transmit |

## Input Modes

| Mode | P_ Constant | Mode Bits | Chapter | Description |
|------|-------------|-----------|---------|-------------|
| Quadrature | `P_QUADRATURE` | %01011 | Ch 14 | A-B quadrature encoder input (within Counting chapter) |
| Reg Up | `P_REG_UP` | %01100 | Ch 14 | Increment on A-rise when B-high |
| Reg Up/Down | `P_REG_UP_DOWN` | %01101 | Ch 14 | Increment/decrement accumulator |
| Count Rises | `P_COUNT_RISES` | %01110 | Ch 14 | Count A-rises, optionally subtract B-rises |
| Count Highs | `P_COUNT_HIGHS` | %01111 | Ch 14 | Count A-high ticks, optionally subtract B-high |
| State Ticks | `P_STATE_TICKS` | %10000 | Ch 13 | Measure A-low and A-high durations |
| High Ticks | `P_HIGH_TICKS` | %10001 | Ch 13 | Measure A-high duration |
| Events/Timeout | `P_EVENTS_TICKS` | %10010 | Ch 13 | Count events or timeout detection |
| Periods Ticks | `P_PERIODS_TICKS` | %10011 | Ch 15 | For X periods, count ticks |
| Periods Highs | `P_PERIODS_HIGHS` | %10100 | Ch 15 | For X periods, count highs |
| Counter Ticks | `P_COUNTER_TICKS` | %10101 | Ch 15 | For periods in X+ ticks, count ticks |
| Counter Highs | `P_COUNTER_HIGHS` | %10110 | Ch 15 | For periods in X+ ticks, count highs |
| Counter Periods | `P_COUNTER_PERIODS` | %10111 | Ch 15 | For periods in X+ ticks, count periods |
| ADC Internal | `P_ADC` | %11000 | Ch 16 | ADC sample/filter, internal clock |
| ADC External | `P_ADC_EXT` | %11001 | Ch 16 | ADC sample/filter, external clock |
| ADC Scope | `P_ADC_SCOPE` | %11010 | Ch 16 | ADC oscilloscope with trigger |
| Sync Serial RX | `P_SYNC_RX` | %11101 | Ch 17 | Synchronous serial receive |
| Async Serial RX | `P_ASYNC_RX` | %11111 | Ch 17 | Asynchronous serial receive |

## Special Modes

| Mode | P_ Constant | Mode Bits | Chapter | Description |
|------|-------------|-----------|---------|-------------|
| USB Pair | `P_USB_PAIR` | %11011 | Ch 19 | USB host/device pin pair |

## Mode Categories Quick Reference

| Category | Modes | Chapters |
|----------|-------|----------|
| **Digital Output** | Pulse, Transition | Ch 7 |
| **Frequency Generation** | NCO Freq, NCO Duty | Ch 8 |
| **PWM Output** | Triangle, Sawtooth, SMPS | Ch 9 |
| **DAC Output** | Repository/Noise, Dither RND, Dither PWM | Ch 10 |
| **Serial Transmit** | Sync TX, Async TX | Ch 11 |
| **Timing Measurement** | State Ticks, High Ticks, Events/Timeout | Ch 13 |
| **Counting** | Reg Up, Reg Up/Down, Count Rises, Count Highs | Ch 14 |
| **Quadrature Encoder** | Quadrature | Ch 14 |
| **Period/Frequency Measurement** | Periods Ticks/Highs, Counter Ticks/Highs/Periods | Ch 15 |
| **ADC Input** | ADC, ADC Ext, ADC Scope | Ch 16 |
| **Serial Receive** | Sync RX, Async RX | Ch 17 |
| **Inter-Cog Sharing** | Repository | Ch 18 |
| **USB** | USB Pair | Ch 19 |


*This front matter provides navigation tools for all readers. Proceed to Part I for foundational knowledge, or use the Intent Index (Appendix A) for task-oriented guidance.*
