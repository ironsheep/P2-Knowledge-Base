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
{\fontsize{36}{42}\selectfont\bfseries P2 Assembly Language Reference Manual\par}
\vspace{0.3cm}
{\Large\itshape Complete PASM2 Instruction Set Documentation\par}
\vspace{0.6cm}
{\large January 2026\par}
\vspace{0.2cm}
{\large\color{blue}Version 2.1\par}

\vfill
\begin{tcolorbox}[
  colback=gray!5,
  colframe=gray!40,
  boxrule=1pt,
  width=0.85\textwidth,
  center,
  title={\bfseries\color{black} Reference Manual Organization},
  colbacktitle=gray!15,
  coltitle=black
]
\textbf{Complete P2 Assembly Language Documentation}

\vspace{0.3cm}
\begin{minipage}[t]{0.45\textwidth}
\textbf{Part I: Architecture}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item P2 Architecture Overview
\item Instruction Format \& Encoding
\item Addressing Modes
\item Flags \& Conditional Execution
\item Program Flow
\end{itemize}
\end{minipage}%
\hfill%
\begin{minipage}[t]{0.50\textwidth}
\textbf{Part II: Language Reference}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=2pt]
\item Instructions (A-Z)
\item Directives
\item Constants \& Special Registers
\item Smart Pin Modes
\item CORDIC Functions
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

Copyright © 2025 Iron Sheep Productions, LLC and Parallax Inc.

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

This manual would not exist without the contributions of many individuals and organizations:

**Parallax Inc.** for creating the Propeller 2 microcontroller and providing comprehensive reference documentation that forms the foundation of this work.

**Chip Gracey** for the brilliant design of the P2 architecture and for maintaining detailed technical specifications.

**The P2 Community** for extensive testing, feedback, and real-world usage that has refined our understanding of the instruction set and identified critical details worth documenting.

**Open Source Contributors** who have developed tools, compilers, and applications that demonstrate the power and flexibility of PASM2.

This manual is a community-developed resource, created to make the P2's assembly language more accessible to developers at all skill levels.


## How to Use This Manual

This manual serves multiple audiences and use cases. The organization is designed to support both learning and reference workflows.

### For Different Reader Types

**New to P2**: Start with Part I, Chapters 1-2 to understand the P2 architecture and instruction format fundamentals. These chapters provide essential context for understanding how PASM2 instructions work. Then explore Part II selectively based on what you need to accomplish.

**Experienced P1 Users**: See "For P1 Developers" below for a specification comparison and overview of new capabilities. Then use Part II as the primary reference—the instruction-by-instruction format will feel familiar.

**Looking Up a Specific Instruction**: Go directly to Part II, which is organized alphabetically by instruction name. Each entry provides complete syntax, encoding, behavior, and examples.

**Quick Reference Needed**: Part III appendices provide dense lookup tables organized by category, encoding pattern, and flag effects for rapid consultation.

### For P1 Developers

The Propeller 2 preserves the core Propeller philosophy—eight symmetric COGs sharing Hub memory—while dramatically expanding capabilities.

**Specification Comparison**

| | P1 | P2 |
|---|---|---|
| Clock | 80 MHz | 180 MHz nominal; 320 MHz max¹ |
| Clocks/Instruction | 4 | 2 |
| Hub RAM | 32 KB | 512 KB |
| COG RAM | 512 longs | 512 + 512 LUT |
| I/O | 32 pins | 64 Smart Pins |
| Math | Software | CORDIC |
| Interrupts | None | 3 per COG |
| Instructions | ~60 | ~360 |

¹ Per P2 Datasheet. Higher frequencies are achievable with adequate thermal management and reduced workload.

**Architecture That Transfers**

- Eight independent COGs with true parallel execution
- Shared Hub memory with round-robin deterministic access
- Private COG RAM for fast local operations
- Wired-OR I/O model preventing pin contention
- Hardware locks for inter-COG synchronization
- Spin/PASM language structure

**New in P2**

- **Smart Pins** — 64 pins with autonomous ADC, DAC, PWM, serial protocols, USB
- **Lookup RAM** — 512 additional longs per COG for tables and overflow code execution
- **CORDIC** — Hardware math: multiply, divide, square root, trig, logarithms
- **Streamer** — Background DMA between Hub, LUT, and pins
- **Digital Video** — Hardware HDMI/DVI output via Streamer
- **FIFO** — Hardware FIFO for high-bandwidth hub streaming and hub execution
- **Interrupts** — Three levels per COG (plus hidden debug interrupt) with 16 event sources
- **Debug Interrupt** — Hidden hardware interrupt for single-stepping and breakpoints
- **COGATN** — Hardware inter-COG attention signaling
- **Register Indirection** — ALTS, ALTD, ALTR for dynamic register addressing
- **Instruction Skipping** — SKIP, SKIPF, EXECF for conditional block execution
- **Hub Execution** — Run code directly from 512 KB Hub RAM

**Changed from P1**

- **Counters**: CTRA/CTRB replaced by Smart Pin event system
- **Video**: VCFG/VSCL/WAITVID replaced by Streamer and DAC capabilities
- **ROM Tables**: Sine/log/antilog tables replaced by CORDIC operations
- **Boot Pins**: P28-P31 changed to P58-P63

**Instruction Format Comparison**

The 32-bit instruction word changed between P1 and P2:

| Field | P1 | P2 | Notes |
|-------|----|----|-------|
| Condition | Bits 21:18 (4 bits) | Bits 31:28 (4 bits) | Moved to MSBs |
| Opcode | 6 bits | 7 bits | Expanded for more instructions |
| CZI/ZCRI | ZCRI (4 bits) | CZI (3 bits) | R bit removed |
| D/S | 9 bits each | 9 bits each | Unchanged |

The R (result) bit from P1's ZCRI field was removed in P2. Result writing is now controlled differently depending on the instruction.

Begin with Chapter 1 to understand the P2 execution model. Part II serves as the alphabetical instruction reference—a format familiar from P1 documentation.

### Manual Structure

**Part I: Architectural Foundation** — Six chapters explaining how the P2 works:

- Chapter 1: The P2 Execution Model
- Chapter 2: The Instruction Format
- Chapter 3: Flags and Conditional Execution
- Chapter 4: Timing and Determinism
- Chapter 5: Special Hardware Overview
- Chapter 6: Address Modes

**Part II: Language Reference** — Complete documentation of all PASM2 elements:

- Instructions (alphabetically organized)
- Directives (assembly-time commands)
- Constants (predefined values)
- Special Registers (hardware registers)

**Part III: Appendices** — Quick reference materials:

- Appendix A: Instruction Encoding Summary
- Appendix B: Condition Code Reference
- Appendix C: Categorical Instruction Index
- Appendix D: Special Registers Reference
- Appendix E: Predefined Constants
- Appendix F: Smart Pin Mode Constants
- Appendix G: Streamer Mode Constants
- Appendix H: Reserved Words Reference
- Appendix I: Glossary
- Appendix J: Known Bugs

### Quick Navigation Guide

**"I need to find instruction X"** → Part II, Instructions section, alphabetically organized

**"I need to understand the architecture"** → Part I, read Chapters 1-2 sequentially

**"I need encoding details"** → Appendix A (encoding summary tables)

**"I need to find instructions by category"** → Appendix C (grouped by function: arithmetic, logic, memory, etc.)

**"I need to understand condition codes"** → Appendix B (complete IF_x reference with all aliases)

**"I need to know what flags an instruction affects"** → Part II (each instruction entry) or Appendix D (summary table)

**"I need Smart Pin configuration values"** → Appendix E (Smart Pin Mode Constants)

**"I need CORDIC operations"** → Chapter 5.1 (CORDIC Coprocessor) or Part II instruction entries (QMUL, QDIV, etc.)


## Conventions Used in This Manual

### Typography

`Monospace font` is used for code examples, instruction names in syntax descriptions, register names, and literal values.

**Bold text** is used for instruction names when mentioned in prose, emphasis of important concepts, and section headings.

*Italic text* is used for emphasis, the first use of technical terms, and parameter names in descriptions.

UPPERCASE is used for instruction mnemonics, register names (PA, PTRA, DIRA), and condition codes (IF_C, IF_Z).

### Code Examples

PASM2 code examples follow standard formatting conventions:

```pasm2
label           instruction     D,S             ' Comment
                instruction     D,#immediate    ' Indented code
        IF_C    instruction     D,S     WCZ     ' With condition and effects
```

- Labels are flush left
- Instructions are indented to column 16 (two tabs or 8 spaces)
- Operands follow the instruction
- Conditions precede the instruction; effects follow operands (see Chapter 3)
- Comments start with a single quote (') and explain the operation
- 8-character column alignment for readability

### Special Markers

Throughout this manual, special markers highlight important information:

**Pitfall**: Common mistakes or non-obvious behavior that can cause errors. Pay careful attention to these to avoid debugging challenges.

**Tip**: Useful techniques, optimization opportunities, or best practices that experienced P2 developers have discovered.

**Hardware**: Hardware-specific considerations, timing constraints, or interactions with P2 peripherals that affect instruction behavior.

### Instruction Encoding Tables

Part II instruction entries include encoding tables with the following columns:

**EEEE** — Condition code field (4 bits). Determines when instruction executes based on flag states.

**Opcode** — Opcode bits. The instruction-specific portion of the 32-bit encoding.

**CZI** — Flag effects field (3 bits). Controls which flags are updated and how.

**Dest** — Destination register (9 bits). Where the result is written.

**Src** — Source register or immediate value (9 bits). Second operand for the instruction.

**C** — Effect on the Carry flag: set (1), cleared (0), modified based on result, or unchanged (---).

**Z** — Effect on the Zero flag: set (1), cleared (0), modified based on result, or unchanged (---).

**Result** — What value gets written to the destination register.

**Clks** — Execution time in system clock cycles.

### Cross-References

This manual uses consistent cross-reference formats:

**[MOV](#mov)** — Hyperlink to a Part II instruction entry (in digital versions)

**"See Chapter X"** — Reference to Part I chapters for architectural context

**"See Appendix X"** — Reference to Part III appendices for quick reference tables

**"Compare: OTHER_INSTRUCTION"** — Points to related or contrasting instructions


## About This Manual

This manual represents a comprehensive effort to document the P2 Assembly Language (PASM2) in a format optimized for both human learning and AI-assisted development. The content is derived from official Parallax documentation, community expertise, and extensive verification against the P2 silicon behavior.

The manual is designed to be:

**Complete** — Every documented instruction, directive, constant, and special register is included with full details.

**Accurate** — Information has been verified against official sources and tested on actual P2 hardware.

**Accessible** — Content is organized for multiple skill levels and use cases, from learning to quick reference.

**Structured** — Consistent formatting enables both human reading and programmatic parsing for tool development.

We welcome feedback, corrections, and suggestions for improvement. This is a living document that will evolve with the P2 community's growing expertise.


*You are now ready to explore the P2 Assembly Language. Whether you are learning for the first time or looking up specific details, this manual is designed to support your journey into P2 development.*
