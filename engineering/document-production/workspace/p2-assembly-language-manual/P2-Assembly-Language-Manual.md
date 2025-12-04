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
{\large December 2025\par}
\vspace{0.2cm}
{\large\color{blue}Version 1.0 - Technical Review\par}

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

Copyright 2025 P2 Knowledge Base Project

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original

Propeller 2, P2, and Parallax are trademarks of Parallax Inc. This manual is an independent community resource and is not officially endorsed by Parallax Inc.


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

**Experienced P1 Users**: Review Chapter 1 for key differences between P1 and P2, particularly the enhanced instruction set and Smart Pin capabilities. Then use Part II as your primary reference, as the instruction-by-instruction format will feel familiar.

**Looking Up a Specific Instruction**: Go directly to Part II, which is organized alphabetically by instruction name. Each entry provides complete syntax, encoding, behavior, and examples.

**Quick Reference Needed**: Part III appendices provide dense lookup tables organized by category, encoding pattern, and flag effects for rapid consultation.

### Manual Structure

**Part I: Architectural Foundation** — Five chapters explaining how the P2 works:

- Chapter 1: P2 Architecture Overview
- Chapter 2: Instruction Format and Encoding
- Chapter 3: Addressing Modes and Register Usage
- Chapter 4: Flags and Conditional Execution
- Chapter 5: Program Flow and Subroutines

**Part II: Language Reference** — Complete documentation of all PASM2 elements:

- Instructions (alphabetically organized)
- Directives (assembly-time commands)
- Constants (predefined values)
- Special Registers (hardware registers)

**Part III: Appendices** — Quick reference materials:

- Appendix A: Instruction Encoding Summary
- Appendix B: Instructions by Category
- Appendix C: Flag Effects Reference
- Appendix D: Smart Pin Modes
- Appendix E: CORDIC Functions
- Appendix F: Opcode Map
- Appendix G: Glossary
- Appendix H: Index

### Quick Navigation Guide

**"I need to find instruction X"** → Part II, Instructions section, alphabetically organized

**"I need to understand the architecture"** → Part I, read Chapters 1-2 sequentially

**"I need encoding details"** → Appendix A (summary tables) or Appendix F (complete opcode map)

**"I need to find instructions by category"** → Appendix B (grouped by function: arithmetic, logic, memory, etc.)

**"I need to know what flags an instruction affects"** → Part II (each instruction entry) or Appendix C (summary table)

**"I need Smart Pin configuration values"** → Appendix D

**"I need CORDIC function codes"** → Appendix E


## Conventions Used in This Manual

### Typography

`Monospace font` is used for code examples, instruction names in syntax descriptions, register names, and literal values.

**Bold text** is used for instruction names when mentioned in prose, emphasis of important concepts, and section headings.

*Italic text* is used for emphasis, the first use of technical terms, and parameter names in descriptions.

UPPERCASE is used for instruction mnemonics, register names (PA, PTRA, DIRA), and condition codes (IF_C, IF_Z).

### Code Examples

PASM2 code examples follow standard formatting conventions:

```pasm
label           instruction     D,S             ' Comment
                instruction     D,#immediate    ' Indented code
```

- Labels are flush left
- Instructions are indented to column 16 (two tabs or 8 spaces)
- Operands follow the instruction
- Comments start with a single quote (') and explain the operation
- 8-character column alignment for readability

### Special Markers

Throughout this manual, special markers highlight important information:

**Pitfall**: Common mistakes or non-obvious behavior that can cause errors. Pay careful attention to these to avoid debugging challenges.

**Tip**: Useful techniques, optimization opportunities, or best practices that experienced P2 developers have discovered.

**Hardware**: Hardware-specific considerations, timing constraints, or interactions with P2 peripherals that affect instruction behavior.

### Instruction Encoding Tables

Part II instruction entries include encoding tables with the following columns:

**COND** — Condition code field (4 bits, EEEE). Determines when instruction executes based on flag states.

**INSTR** — Opcode bits. The instruction-specific portion of the 32-bit encoding.

**FX** — Flag effects field (3 bits, CZI). Controls which flags are updated and how.

**DEST** — Destination register (9 bits). Where the result is written.

**SRC** — Source register or immediate value (9 bits). Second operand for the instruction.

**Write** — What value gets written to the destination register.

**C Flag** — Effect on the Carry flag: set (1), cleared (0), modified based on result, or unchanged (-).

**Z Flag** — Effect on the Zero flag: set (1), cleared (0), modified based on result, or unchanged (-).

**Clocks** — Execution time in system clock cycles.

### Cross-References

This manual uses consistent cross-reference formats:

**[INSTRUCTION](#instruction)** — Hyperlink to a Part II instruction entry (in digital versions)

**"See Chapter X"** — Reference to Part I chapters for architectural context

**"See Appendix X"** — Reference to Part III appendices for quick reference tables

**"Compare: OTHER_INSTRUCTION"** — Points to related or contrasting instructions


## Document Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11 | Initial release. Complete coverage of PASM2 instruction set, directives, constants, and special registers. Includes architectural foundation chapters and comprehensive appendices. |


## About This Manual

This manual represents a comprehensive effort to document the P2 Assembly Language (PASM2) in a format optimized for both human learning and AI-assisted development. The content is derived from official Parallax documentation, community expertise, and extensive verification against the P2 silicon behavior.

The manual is designed to be:

**Complete** — Every documented instruction, directive, constant, and special register is included with full details.

**Accurate** — Information has been verified against official sources and tested on actual P2 hardware.

**Accessible** — Content is organized for multiple skill levels and use cases, from learning to quick reference.

**Structured** — Consistent formatting enables both human reading and programmatic parsing for tool development.

We welcome feedback, corrections, and suggestions for improvement. This is a living document that will evolve with the P2 community's growing expertise.


*You are now ready to explore the P2 Assembly Language. Whether you are learning for the first time or looking up specific details, this manual is designed to support your journey into P2 development.*


# Part I: Architectural Foundation

# Chapter 1: The P2 Execution Model

<!-- Chapter establishing the foundational mental model for the P2 architecture -->

The Propeller 2 microcontroller implements a unique multi-processor architecture that differs fundamentally from conventional microcontrollers. Understanding this architecture is essential for effective PASM2 programming.


## 1.1 The Eight-COG Architecture

```{=latex}
\EightCogOverviewDiagram
```

The P2 contains eight identical processors called COGs (Cog Processors). Each COG:

- Executes instructions independently and simultaneously
- Has its own dedicated memory and registers
- Operates at full clock speed with deterministic timing
- Shares access to a common Hub memory

### 1.1.1 COG Independence

Unlike conventional microcontrollers that use time-slicing or task switching, the P2 implements true parallel execution. Each COG runs at full clock speed simultaneously with all other COGs. There is no scheduler, no context switching overhead, and no need for traditional interrupts to handle multiple tasks.

This architecture provides deterministic timing. The same code executing on a COG takes exactly the same number of clock cycles every time it runs. This predictability makes the P2 ideal for real-time applications such as video generation, motor control, and protocol implementation where precise timing is essential.

Each COG operates independently. One COG can execute a tight control loop while another manages communications and a third handles user interface tasks. All eight COGs run simultaneously without interfering with each other's timing.

### 1.1.2 COG Identification

Each COG has a unique identifier from 0 to 7. A COG can determine its own identifier using the `COGID` instruction, which writes the COG number to the destination register. This capability allows the same code to run on multiple COGs while behaving differently based on COG identity.

COGs communicate through shared Hub memory, hardware locks, and attention signals. The `COGATN` instruction allows one COG to signal another COG through hardware attention flags, providing fast inter-COG notification without polling shared memory locations.

### 1.1.3 Starting and Stopping COGs

The `COGINIT` instruction starts a new COG or restarts an existing one. COGINIT specifies which COG to start (0-7), where the code resides in Hub memory, and optionally passes a parameter to the new COG. The parameter value appears in the new COG's PTRB register, providing a simple mechanism for initialization data.

The `COGSTOP` instruction halts a running COG. A COG can stop itself or another COG by specifying the target COG number. Stopped COGs consume no power and can be restarted later with different code.


## 1.2 COG Memory

```{=latex}
\CogMemoryMapDiagram
```

Each COG has 512 longs (2048 bytes) of dedicated RAM addressed from $000 to $1FF. This memory is private to each COG and provides single-cycle read and write access. Unlike Hub memory, COG memory stores 32-bit longs only and uses long-addressing rather than byte-addressing.

### 1.2.1 General Purpose Registers ($000-$1EF)

The first 496 longs ($000-$1EF) serve as general-purpose registers available for code and data storage. In PASM2, these locations function as registers rather than traditional memory. Instructions specify source and destination operands by register address, and the assembler translates symbolic names to these addresses.

Programs can use this space flexibly. A small program might dedicate most of the space to data storage and lookup tables. A larger program uses more space for code and less for data. The programmer controls this allocation through the assembler's ORG directive and RES directive for reserving data space.

### 1.2.2 Special Purpose Registers ($1F0-$1FF)

```{=latex}
\SpecialRegistersMapDiagram
```

The final 16 registers ($1F0-$1FF) have special hardware functions:

| Address | Register | Purpose |
|---------|----------|---------|
| $1F0 | IJMP3 | Interrupt 3 jump address |
| $1F1 | IRET3 | Interrupt 3 return address |
| $1F2 | IJMP2 | Interrupt 2 jump address |
| $1F3 | IRET2 | Interrupt 2 return address |
| $1F4 | IJMP1 | Interrupt 1 jump address |
| $1F5 | IRET1 | Interrupt 1 return address |
| $1F6 | PA | Port A scratch / pointer register |
| $1F7 | PB | Port B scratch / pointer register |
| $1F8 | PTRA | Pointer A register |
| $1F9 | PTRB | Pointer B register |
| $1FA | DIRA | Direction for pins 31-0 |
| $1FB | DIRB | Direction for pins 63-32 |
| $1FC | OUTA | Output for pins 31-0 |
| $1FD | OUTB | Output for pins 63-32 |
| $1FE | INA | Input from pins 31-0 (read-only) |
| $1FF | INB | Input from pins 63-32 (read-only) |

Registers $1F0-$1F7 serve dual purposes. When their associated hardware functions (interrupts, parameter passing) are not enabled, these registers function as ordinary general-purpose RAM. Registers $1F8-$1FF are fixed special-purpose registers that always provide their hardware functions when accessed.

### 1.2.3 Register Addressing

PASM2 instructions use 9-bit fields to specify source (S) and destination (D) register addresses. Nine bits provide 512 possible values, addressing the complete COG RAM space from $000 to $1FF. The instruction encoding dedicates specific bit positions to these address fields, and the assembler automatically encodes symbolic register names into the appropriate bit patterns.


## 1.3 Hub Memory

```{=latex}
\HubMemoryDiagram
```

The Hub provides 512KB of shared RAM accessible by all COGs. Unlike COG memory, Hub memory is byte-addressable and stores programs, data, and resources shared among COGs.

### 1.3.1 Hub Address Space

Hub memory spans addresses $00000 through $7FFFF, providing 524,288 bytes of storage. All eight COGs can read and write any location in this space. Hub memory stores bytes, words (16-bit), and longs (32-bit) with appropriate address alignment.

Programs use Hub memory to share data between COGs, store large lookup tables, hold program code for Hub execution mode, and buffer data for I/O operations. Each COG accesses Hub memory through dedicated Hub instructions that handle the shared access timing automatically.

### 1.3.2 Hub Access Timing

The P2 uses an "egg-beater" access pattern to arbitrate Hub memory access among the eight COGs. Each COG receives a dedicated access window every eighth clock cycle. The Hub controller rotates through COGs 0-7 continuously, giving each COG one access slot per rotation.

This pattern creates deterministic but variable timing. A Hub access completes immediately if the requesting COG's window is currently active. Otherwise, the COG waits 0-7 clock cycles for its next window. This variability means Hub instructions take 2-9 clocks depending on when the instruction executes relative to the egg-beater rotation.

Despite this variability, the timing remains deterministic. The maximum wait is always seven clocks, and timing patterns repeat every eight clocks. Programs that require precise timing use COG execution mode for critical sections and Hub memory only for data storage and inter-COG communication.

### 1.3.3 Hub Instructions

PASM2 provides six instructions for Hub memory access. `RDBYTE` reads a byte, `RDWORD` reads a word, and `RDLONG` reads a long from Hub memory to a COG register. `WRBYTE`, `WRWORD`, and `WRLONG` write the corresponding data sizes from a COG register to Hub memory.

The `SETQ` instruction enhances Hub access efficiency by enabling burst transfers. SETQ followed by a Hub read instruction loads multiple consecutive values in a single operation, amortizing the Hub window wait time across many transfers.


## 1.4 LUT Memory

```{=latex}
\LutMemoryMapDiagram
```

Each COG has a dedicated 512-long Lookup Table (LUT) providing additional fast memory separate from the main COG RAM space. The LUT serves as auxiliary storage for lookup tables, waveform data, additional code space, or working memory.

### 1.4.1 LUT Characteristics

LUT memory provides single-cycle access like COG RAM but occupies a separate address space. Programs access LUT memory at addresses $200-$3FF (relative to COG addressing) through dedicated LUT instructions. This separation doubles the available fast memory per COG from 512 longs to 1024 longs total.

The LUT integrates with the P2's streamer and cordic subsystems. The streamer can directly output LUT contents to pins for waveform generation, and cordic operations can store results in LUT memory. This integration makes the LUT particularly valuable for signal generation and digital signal processing applications.

### 1.4.2 LUT Instructions

`RDLUT` reads a value from LUT memory to a COG register. `WRLUT` writes a value from a COG register to LUT memory. These instructions work similarly to regular COG memory operations but target the separate LUT address space.

Programs often load the LUT with data from Hub memory at initialization using `SETQ` for burst transfers, then access the LUT repeatedly during time-critical operations. This pattern keeps frequently-accessed data in fast LUT memory while larger datasets remain in Hub memory.

### 1.4.3 LUT Sharing Between COGs

The `SETLUTS` instruction enables LUT sharing between COG pairs. Adjacent COGs (0-1, 2-3, 4-5, 6-7) can share their LUT memory, effectively giving one COG 1024 longs of LUT space while the paired COG uses the shared space as well. This feature supports applications where one COG generates data that another COG consumes, eliminating the need to transfer data through Hub memory.


## 1.5 The Execution Pipeline

The P2 implements a simple two-stage pipeline that balances execution speed with hardware simplicity. The first stage fetches and decodes the instruction. The second stage reads operands, executes the operation, and writes results. This streamlined pipeline provides predictable timing without the complexity of deeper pipelines.

Most instructions complete in two clock cycles once the pipeline fills. The first instruction takes two clocks to reach completion. Subsequent instructions complete at a rate of one per two clocks, giving an effective throughput of one instruction every two clocks in steady-state execution.

Hub memory instructions add variable delays waiting for Hub access windows. The egg-beater pattern means a Hub instruction might execute immediately or wait up to seven clocks for its COG's access slot. This variability affects only Hub memory operations; pure COG operations maintain consistent two-clock timing.

Branch instructions incur additional overhead when taken. A conditional branch that is not taken completes in two clocks like other instructions. A taken branch requires four clocks as the pipeline flushes and refills from the branch target address.

The P2 handles data dependencies internally through forwarding logic. An instruction that depends on the result of the immediately preceding instruction receives the correct value without requiring explicit programmer intervention or NOP insertion. This hardware forwarding eliminates a major class of pipeline hazards present in simpler architectures.


## 1.6 Execution Modes

The P2 supports two distinct execution modes that offer different trade-offs between speed and capacity. Programs can use either mode exclusively or mix both modes within a single application.

### 1.6.1 COG Execution Mode

COG execution mode runs code from COG RAM. Instructions execute in the consistent two-clock pipeline with no additional delays. This mode provides the fastest possible execution and deterministic timing, making it ideal for time-critical code such as communication protocols, motor control loops, and signal generation.

COG execution mode limits programs to the available COG RAM space. After accounting for special registers and data storage, typically 200-400 longs remain for code. Programs that fit in this space achieve maximum performance. Larger programs must use Hub execution mode or implement code overlays that load different code sections into COG RAM as needed.

Time-critical inner loops often execute in COG mode even when the main program runs from Hub memory. The program loads the critical code section to COG RAM, executes the loop, then returns to Hub-based code. This hybrid approach combines the performance of COG execution with the capacity of Hub storage.

### 1.6.2 Hub Execution Mode

Hub execution mode runs code directly from Hub RAM without loading it to COG memory first. The COG fetches instructions from Hub memory using the same egg-beater access pattern used for data transfers. This adds variable delay to instruction fetch, slowing execution compared to COG mode.

Hub execution mode provides access to the full 512KB Hub address space, enabling programs far larger than COG memory could hold. The mode suits applications where code size exceeds available COG RAM and deterministic timing is less critical. User interface code, data processing algorithms, and high-level control logic typically run well in Hub execution mode.

`COGINIT` determines execution mode when starting a COG. The initialization parameter specifies either COG execution (code loaded from Hub to COG RAM, then executed) or Hub execution (code executed directly from Hub RAM). The `ORGH` assembler directive marks code intended for Hub execution, while `ORG` marks code for COG execution.

### 1.6.3 Switching Between Modes

Programs switch between execution modes using `CALL` or `JMP` instructions. A COG executing from COG RAM can call or jump to Hub addresses, and Hub-executing code can call or jump to COG addresses. The program counter determines current mode: addresses $000-$3FF indicate COG/LUT execution, while higher addresses indicate Hub execution.

The hardware automatically handles mode transitions. The programmer simply specifies the target address, and the COG switches to the appropriate execution mode. This seamless transition enables hybrid programs that place performance-critical code in COG RAM while maintaining larger program logic in Hub RAM.


```{=latex}
\begin{keyconcepts}
\item The P2 has 8 independent COGs executing in true parallel
\item Each COG has 512 longs of private RAM plus 512 longs of LUT
\item Hub memory (512KB) is shared among all COGs with deterministic access timing
\item Special registers at \$1F0-\$1FF provide hardware I/O functions
\item COGs can execute from COG RAM (fast) or Hub RAM (larger capacity)
\item The pipeline provides single-cycle execution for most instructions
\item No interrupts are required due to true parallel execution
\end{keyconcepts}
```


<!-- End of Chapter 1 -->

# Chapter 2: The Instruction Format

Every PASM2 instruction is encoded in a 32-bit word with a consistent structure. Understanding this format enables reading the encoding tables in Part II and manually encoding or decoding instructions when needed.


## 2.1 The 32-Bit Instruction Word

Every PASM2 instruction occupies exactly one 32-bit long with this structure:

```{=latex}
\InstructionEncoding{Generic}{EEEE}{OOOOOOO}{CZI}{DDDDDDDDD}{SSSSSSSSS}
```

### 2.1.1 Field Summary

| Field | Bits | Width | Purpose |
|-------|------|-------|---------|
| EEEE | 31-28 | 4 | Condition code for conditional execution |
| OOOOOOO | 27-21 | 7 | Opcode identifying the instruction |
| CZI | 20-18 | 3 | Flag effects and immediate mode |
| DDDDDDDDD | 17-9 | 9 | Destination register address |
| SSSSSSSSS | 8-0 | 9 | Source operand (register or immediate) |

### 2.1.2 The CZI Field

The three bits at positions 20-18 control flag behavior and operand mode:

| Bit | Position | Purpose |
|-----|----------|---------|
| C | 20 | C flag write enable (1 = update C flag) |
| Z | 19 | Z flag write enable (1 = update Z flag) |
| I | 18 | Immediate mode (1 = S is immediate value) |

When WC is specified in source code, the assembler sets bit 20 to 1. When WZ is specified, bit 19 is set. When # prefixes the source operand, bit 18 is set.


## 2.2 Condition Codes (EEEE Field)

The condition field enables conditional execution of any instruction. The instruction executes only if the specified condition is true based on the current C and Z flags.

### 2.2.1 Condition Code Table

| EEEE | Mnemonic | Condition | Description |
|------|----------|-----------|-------------|
| 0000 | _RET_ | (special) | Return from subroutine |
| 0001 | IF_NC_AND_NZ | C=0 AND Z=0 | Neither carry nor zero |
| 0010 | IF_NC_AND_Z | C=0 AND Z=1 | No carry and zero |
| 0011 | IF_NC | C=0 | No carry (unsigned less than) |
| 0100 | IF_C_AND_NZ | C=1 AND Z=0 | Carry and not zero |
| 0101 | IF_NZ | Z=0 | Not zero |
| 0110 | IF_C_NE_Z | C≠Z | Carry not equal to zero |
| 0111 | IF_NC_OR_NZ | C=0 OR Z=0 | No carry or not zero |
| 1000 | IF_C_AND_Z | C=1 AND Z=1 | Carry and zero |
| 1001 | IF_C_EQ_Z | C=Z | Carry equals zero |
| 1010 | IF_Z | Z=1 | Zero |
| 1011 | IF_NC_OR_Z | C=0 OR Z=1 | No carry or zero |
| 1100 | IF_C | C=1 | Carry (unsigned greater than or equal) |
| 1101 | IF_C_OR_NZ | C=1 OR Z=0 | Carry or not zero |
| 1110 | IF_C_OR_Z | C=1 OR Z=1 | Carry or zero |
| 1111 | (always) | Always | Unconditional execution |

### 2.2.2 The _RET_ Condition

The condition code 0000 (_RET_) has special behavior. When an instruction has EEEE=0000, it functions as a return from subroutine:

- The instruction field is ignored
- PC is loaded from the return address stored in PA (for CALL) or from the stack

This encoding allows any instruction mnemonic to become a conditional return when prefixed with _RET_:

```pasm
_ret_   add     x, y                    ' Return, ADD is not executed
```

The _RET_ prefix is primarily used with CALLA, CALLB, and related call instructions that use the condition field for return control.

### 2.2.3 Conditional Execution Patterns

Conditional execution eliminates branches, providing deterministic timing:

```pasm
' Instead of branching:
                cmp     a, b            wc wz
        if_z    jmp     #equal_handler          ' 4 cycles if taken
                mov     result, #0

' Use conditional execution:
                cmp     a, b            wc wz
        if_z    mov     result, #1              ' Always 2 cycles
        if_nz   mov     result, #0              ' Always 2 cycles
```

Common patterns:

**Minimum/Maximum:**
```pasm
                cmp     a, b            wc      ' Compare unsigned
        if_c    mov     min, a                  ' min = a if a < b
        if_nc   mov     min, b                  ' min = b if a >= b
```

**Conditional Assignment:**
```pasm
                test    flags, #MASK    wz      ' Test bit
        if_nz   mov     mode, #1                ' Set if bit present
```

**Multi-way Selection:**
```pasm
                cmp     selector, #0    wz
        if_z    mov     result, value0
                cmp     selector, #1    wz
        if_z    mov     result, value1
                cmp     selector, #2    wz
        if_z    mov     result, value2
```


## 2.3 Reading Encoding Tables

Each instruction entry in Part II includes an encoding table with nine columns. The table shows the instruction's binary encoding on the left and its effects on the right.

### 2.3.1 Encoding Columns (Left Five)

The left five columns show the 32-bit instruction encoding:

| Column | Content | Description |
|--------|---------|-------------|
| COND | EEEE | Condition field (4 bits, always EEEE for conditional instructions) |
| INSTR | 7 bits | The instruction's unique opcode (positions 27-21) |
| FX | CZI variant | Flag modification and immediate bits (positions 20-18) |
| DEST | DDDDDDDDD | Destination field pattern (positions 17-9) |
| SRC | SSSSSSSSS | Source field pattern (positions 8-0) |

### 2.3.2 Result Columns (Right Four)

The right four columns describe instruction effects:

| Column | Content | Description |
|--------|---------|-------------|
| Write | What's written | Which register(s) receive output (D, PC, etc.) |
| C Flag | C behavior | How C flag is affected, or "---" for no change |
| Z Flag | Z behavior | How Z flag is affected, or "---" for no change |
| Clocks | Cycle count | Execution time in clock cycles |

### 2.3.3 The FX Field Variations

The FX column shows which flag and immediate options are available:

| FX Pattern | Meaning |
|------------|---------|
| CZI | C modifiable (WC), Z modifiable (WZ), Immediate allowed (#) |
| 0ZI | C not modifiable, Z modifiable, Immediate allowed |
| C0I | C modifiable, Z not modifiable, Immediate allowed |
| 00I | Neither flag modifiable, Immediate allowed |
| CZ0 | Flags modifiable, Immediate not allowed (register only) |
| NNI | NN bits encode sub-function (e.g., byte number), Immediate allowed |
| LLI | LL bits encode sub-function, Immediate allowed |

When FX shows fixed bits (like `000` or `01I`), those bits have fixed values and the corresponding options are not available.

### 2.3.4 Special Values in Columns

**Write column:**
- `D` - Destination register is written
- `D and PC` - Both destination and program counter written (for jumps/calls)
- `PC` - Only PC written
- `---` - Nothing written (compare, test instructions)
- `LUT` - LUT memory written
- `Hub` - Hub memory written

**Flag columns:**
- `---` - Flag is not changed
- Descriptive text - Describes condition that sets/clears the flag

**Clocks column:**
- `2` - Always 2 clock cycles
- `2+` - Minimum 2 cycles, may be more
- `2 or 4` - 2 if condition false/not taken, 4 if true/taken
- `2 / 8-23` - COG mode cycles / Hub mode cycles
- `9..35` - Variable range depending on operands


## 2.4 Understanding Multiple Encoding Rows

Some instruction entries show multiple rows in the encoding table. Each row represents a unique machine code encoding.

### 2.4.1 Instruction Families

When related instructions share an entry (e.g., DIRZ/DIRNZ), each instruction gets its own row:

**DIRZ / DIRNZ**


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001000100 | D | --- | Orig bit | 2 |
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001000101 | D | --- | Orig bit | 2 |


The first row is DIRZ (S = 001000100), the second is DIRNZ (S = 001000101). Both share the same opcode but differ in the SRC field.

### 2.4.2 Multiple Syntax Forms

When one instruction has multiple syntax forms with different encodings:

**GETBYTE**

Syntax 1: `GETBYTE  Dest, {#}Src, #Num`

Syntax 2: `GETBYTE  Dest`


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1000111 | NNI | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1000111 | 000 | DDDDDDDDD | 000000000 | --- | --- | D | 2 |


The first row shows the standard form with Src and Num operands (NN encodes the byte number 0-3). The second row shows the ALTGB-compatible form where Dest is both read and written.

### 2.4.3 Key Principle

Each unique machine code encoding = one table row. If two mnemonics produce different bit patterns, they appear as separate rows. If one mnemonic has multiple valid encodings (different syntax forms), each encoding appears as a row.


## 2.5 Destination and Source Fields

### 2.5.1 The Destination Field (D)

The 9-bit D field (bits 17-9) addresses a COG register from $000 to $1FF:

- **Read and written:** Most ALU instructions read D, compute, and write result back to D
- **Read only:** Compare instructions (CMP, CMPS, TEST) read D but do not modify it
- **Write only:** Some move instructions write D without reading its previous value

The D field can also specify:
- Hub addresses (for ALTD-modified instructions)
- LUT addresses (for LUT instructions)
- Pin numbers (for certain I/O instructions)

### 2.5.2 The Source Field (S)

The 9-bit S field (bits 8-0) has two modes controlled by the I bit:

**Register mode (I = 0):**
- S is a COG register address ($000-$1FF)
- The value in that register is used as the operand

**Immediate mode (I = 1):**
- S is a 9-bit unsigned value (0-511)
- This value is used directly as the operand

```pasm
        add     result, counter         ' S = register address (I=0)
        add     result, #100            ' S = immediate 100 (I=1)
```

### 2.5.3 When S is Fixed

Some encodings show fixed S values instead of SSSSSSSSS. These instructions use the S field to encode which specific operation to perform:

```{=latex}
\encodingsnippetannotated{EEEE}{1101011}{CZI}{DDDDDDDDD}{001000100}{Fixed value selects DIRZ}
```

The fixed value distinguishes this instruction from others sharing the same opcode. The programmer does not specify this value; it is implicit in the instruction mnemonic.


## 2.6 Immediate Operands

### 2.6.1 The # Prefix (9-bit Immediate)

The `#` prefix before an operand indicates an immediate value:

```pasm
        add     result, #100            ' Add immediate 100
        add     result, value           ' Add contents of register 'value'
        mov     x, #$1FF                ' Load maximum 9-bit value (511)
```

When `#` is used:
- The assembler sets the I bit (bit 18) to 1
- The S field contains the 9-bit value

### 2.6.2 Immediate Range

9-bit immediates can represent:

- Unsigned: 0 to 511 ($000 to $1FF)
- Signed (when interpreted): -256 to +255

Values outside this range require augmentation (see Section 2.7).

### 2.6.3 The $ Prefix for Current Address

The `$` symbol represents the current assembly address:

```pasm
loop    add     counter, #1
        djnz    count, #$-1             ' Jump back one instruction
```

When used with `#`, it becomes an immediate representing the address.


## 2.7 Augmented Immediates

### 2.7.1 The ## Prefix (32-bit Immediate)

The `##` prefix indicates a full 32-bit immediate value:

```pasm
        mov     dest, ##$12345678       ' Load full 32-bit value
        add     counter, ##1000000      ' Add 1 million
        mov     ptr, ##hub_data         ' Load 20-bit Hub address
```

### 2.7.2 AUGS and AUGD Instructions

The assembler implements 32-bit immediates by inserting AUG instructions:

- **AUGS** - Augments the Source field for the following instruction
- **AUGD** - Augments the Destination field for the following instruction

The AUG instruction provides the upper 23 bits, which combine with the lower 9 bits from the next instruction:

```pasm
' What the programmer writes:
        mov     dest, ##$12345678

' What the assembler generates:
        augs    #$12345                 ' Upper 23 bits: $12345
        mov     dest, #$678             ' Lower 9 bits: $678
                                        ' Combined: $12345678
```

### 2.7.3 Augmentation Behavior

The AUG instruction must immediately precede the instruction it augments:

1. The AUG executes, storing the 23-bit value internally
2. The next instruction combines this with its 9-bit field
3. The combined 32-bit value is used for that instruction only
4. The augmentation is consumed (one-shot)

If any instruction intervenes (including a conditional NOP), the augmentation is lost.

### 2.7.4 When Augmentation is Required

Augmentation is needed when:
- Values exceed 9 bits (> 511 for unsigned)
- Hub addresses are used (20-bit address space)
- 32-bit constants are needed
- Pin masks exceed 9 bits

```pasm
        wrlong  value, ##$1000          ' Hub address $1000 (> 511)
        mov     mask, ##$FFFF0000       ' 32-bit mask
        waitx   ##1000000               ' Delay > 511 cycles
```


## 2.8 How to Use This Manual

### 2.8.1 Looking Up an Instruction

1. **Find the instruction** alphabetically in Part II
2. **Read the syntax** to understand valid operand forms
3. **Check the Result** line for what the instruction produces
4. **Review Parameters** for operand requirements and constraints
5. **Use the Encoding table** when you need machine code details
6. **Read Related** instructions for alternatives and family members
7. **Study Explanation** for complete behavioral description

### 2.8.2 Example: Understanding ADD

Consider the ADD instruction entry:

::: {.notebox}
**ADD** --- Math Instruction --- Add two unsigned values.

`ADD  Dest, {#}Src  {WC|WZ|WCZ}`

**Result:** Sum of unsigned Src and unsigned Dest is stored in Dest.

- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.
:::


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001000 | CZI | DDDDDDDDD | SSSSSSSSS | D | carry of (D + S) | Result = 0 | 2 |


From this entry:

- **Category:** Math Instruction - this is arithmetic
- **Syntax:** `{#}Src` means Src can be register or immediate; `{WC|WZ|WCZ}` means flag effects are optional
- **Result:** The sum goes into Dest (Dest is modified)
- **Encoding:** Opcode is 0001000 (7 bits); FX is CZI meaning all options available; takes 2 cycles
- **C Flag:** Set if addition overflows (unsigned carry)
- **Z Flag:** Set if result is zero

### 2.8.3 Using Categories for Discovery

Instructions are grouped by category in Appendix B. When looking for "an instruction that does X," consult the categorical index:

- **Math Instructions:** ADD, SUB, MUL, etc.
- **Logic Instructions:** AND, OR, XOR, etc.
- **Branch/Jump Instructions:** JMP, CALL, DJNZ, etc.
- **Hub Memory Instructions:** RDLONG, WRLONG, etc.

### 2.8.4 Using Related Instructions

The Related line shows instructions in the same family or with similar purpose:

```
**Related:** ADDX, ADDS, ADDSX, SUB
```

This tells you:
- ADDX: ADD with carry-in (for multi-precision)
- ADDS: Signed addition
- ADDSX: Signed addition with carry-in
- SUB: The opposite operation


```{=latex}
\begin{keyconcepts}
\item Every instruction is exactly 32 bits: 4-bit condition, 7-bit opcode, 3-bit flags, 9-bit D, 9-bit S
\item The EEEE condition field enables conditional execution based on C and Z flags
\item The I bit (position 18) determines whether S is a register address (0) or immediate value (1)
\item 9-bit immediates range 0-511; larger values require \#\# augmentation
\item AUGS/AUGD extend immediates to full 32 bits by inserting an extra instruction before the target
\item Encoding tables show both the bit pattern (left 5 columns) and the effects (right 4 columns)
\item Multiple table rows indicate instruction families or syntax variants with different encodings
\item The \_RET\_ condition (EEEE=0000) transforms any instruction into a subroutine return
\end{keyconcepts}
```


<!-- End of Chapter 2 -->

# Chapter 3: Flags and Conditional Execution

<!-- Chapter covering C and Z flags, WC/WZ/WCZ effects, and IF_x conditions -->

The P2 has two status flags that enable conditional execution and multi-precision arithmetic. Understanding flag behavior is essential for writing efficient, branching-free code.

The P2's flag system differs from many processors in two important ways. First, flags persist until explicitly modified—an instruction without WC or WZ effects leaves flags unchanged, allowing flag values to be used by multiple subsequent instructions. Second, any instruction can be made conditional using IF_x prefixes, enabling deterministic branchless programming where instruction timing remains constant regardless of data values.

These two features combine to create a powerful programming model where complex decision logic can be expressed without branches, maintaining cycle-accurate timing while reducing code size and improving readability.


## 3.1 The C and Z Flags

Each COG maintains two independent status flags that track computation results and enable conditional execution. These flags are named C (Carry) and Z (Zero), but their meanings extend beyond these basic interpretations depending on the instruction that sets them.

### 3.1.1 The C Flag (Carry/Borrow)

The C flag serves multiple purposes depending on instruction context:

**For arithmetic operations**, C indicates **unsigned overflow** after addition (carry out of bit 31) or **unsigned borrow** after subtraction (when the subtrahend exceeds the minuend). This enables multi-precision arithmetic where carries or borrows propagate between 32-bit operations.

**For shift and rotate operations**, C captures the **bit value shifted out** of the result. A left shift stores bit 31 in C; a right shift stores bit 0 in C. This enables implementing shifts wider than 32 bits by chaining operations.

**For comparison operations**, C indicates the **relationship between operands**. After an unsigned comparison (CMP), C=1 means the first operand is below (less than) the second. After a signed comparison (CMPS), C=1 means the first operand is less than the second using signed interpretation.

**For logical operations**, C indicates **parity**—whether the result contains an odd number of 1 bits. This specialized behavior supports error detection and certain bit manipulation patterns.

### 3.1.2 The Z Flag (Zero)

The Z flag indicates **zero result** or **equality** across most instructions:

**For arithmetic and logical operations**, Z=1 when the result equals zero. This enables testing for zero values, detecting exhausted counters, or identifying cleared registers.

**For comparison operations**, Z=1 when the operands are equal. This works for both signed (CMPS) and unsigned (CMP) comparisons—equality has the same meaning regardless of interpretation.

**For bit test operations**, Z=1 when the tested bits are all clear. The TEST instruction ANDs its operands and sets Z based on whether the result is zero, effectively testing whether any specified bits are set.

### 3.1.3 Flag Persistence and Independence

Flags retain their values until explicitly modified by a WC, WZ, or WCZ effect. This persistence is a deliberate design feature that enables powerful programming patterns:

```pasm
                cmp     a, b            wc wz   ' Set flags once
        if_c    mov     min, a                  ' Use C here
        if_nc   mov     min, b                  ' And here
        if_z    mov     equal, #1               ' And use Z here
```

In this example, one comparison sets both flags, and three subsequent instructions each test the preserved flag values. No instruction between them modifies the flags, so the flag state from the comparison remains available.

Each COG maintains its own C and Z flags completely independently. Flag values in COG 0 have no relationship to flag values in COG 1. This independence ensures parallel execution across COGs operates without interference.


## 3.2 Flag Modification Effects

Every instruction can optionally specify which flags to update using effect modifiers. These modifiers—WC, WZ, and WCZ—control whether the instruction modifies the C flag, the Z flag, both flags, or neither flag. The operation always executes; effects only determine whether flags are updated.

### 3.2.1 The WC Effect

```pasm
        add     result, value   wc      ' Update C flag based on carry
```

When WC (Write C) is specified, the instruction updates the C flag according to its specific C condition while leaving Z unchanged. For ADD, this means C is set if the addition produces a carry out of bit 31. For CMP, this means C is set if the first operand is less than the second. Each instruction defines its own C condition as documented in the instruction reference.

The key insight: WC means "update C according to this instruction's C rule." The rule varies by instruction, but the WC effect itself is consistent—it enables C modification.

### 3.2.2 The WZ Effect

```pasm
        add     result, value   wz      ' Update Z flag based on result
```

When WZ (Write Z) is specified, the instruction updates the Z flag based on whether the result equals zero, while leaving C unchanged. Z=1 indicates a zero result; Z=0 indicates a non-zero result. This behavior is consistent across nearly all instructions—the Z flag always reflects "is the result zero?"

This consistency makes WZ predictable. After any arithmetic, logical, or shift operation with WZ, checking IF_Z tests whether the result was zero. After a comparison with WZ, checking IF_Z tests whether the operands were equal.

### 3.2.3 The WCZ Effect

```pasm
        add     result, value   wcz     ' Update both flags
```

When WCZ (Write C and Z) is specified, both flags are updated according to their respective conditions. This is exactly equivalent to specifying both WC and WZ, but requires less typing and produces more readable code.

WCZ is common after comparisons where both the ordering (C) and equality (Z) matter, or after arithmetic operations where both carry detection and zero detection are needed.

### 3.2.4 No Effect (Default)

```pasm
        add     result, value           ' Execute operation, preserve flags
```

When no effect is specified, the instruction executes normally but leaves both C and Z unchanged. This is not a "do nothing" mode—the operation completes, the destination is written, and timing is identical to the flagged version. Only the flags are preserved.

This behavior enables using flag values across multiple instructions without interference:

```pasm
                cmp     a, b            wc      ' Set C based on comparison
                mov     temp, c                 ' Does not modify C
                add     temp, d                 ' Does not modify C
        if_c    mov     result, temp            ' Tests original C
```

The comparison sets C, and two subsequent operations execute without modifying it. The conditional instruction tests the comparison result even though two operations occurred in between.


## 3.3 Conditional Execution

The P2 allows any instruction to execute conditionally based on the current flag values. This conditional execution mechanism enables branchless programming—expressing decision logic without jump instructions—which maintains deterministic timing and often reduces code size.

### 3.3.1 The IF_x Prefix

Any instruction can be made conditional by prefixing with an IF_x condition. When the condition is false, the instruction does not execute, but still consumes its normal execution time (typically one clock cycle). When the condition is true, the instruction executes normally:

```pasm
                cmp     a, b            wc wz   ' Compare, set flags
        if_z    mov     result, #1              ' Only if Z=1 (equal)
        if_nz   mov     result, #0              ' Only if Z=0 (not equal)
```

This three-instruction sequence sets `result` to 1 if `a` equals `b`, or 0 if they differ. It takes exactly three clock cycles regardless of the comparison result. The unconditional CMP always executes, then exactly one of the two conditional MOVs executes.

The timing predictability is crucial. Traditional branch-based code has variable timing depending on which path is taken. Conditional execution eliminates this variation—the instruction stream is fixed, and timing is constant.

### 3.3.2 Conditional Execution Timing

When a conditional instruction's condition is false, the instruction does not execute but still consumes one clock cycle. This behavior might seem wasteful, but it provides deterministic timing—critical for real-time operations, protocol timing, and cycle-accurate code.

Consider this example:

```pasm
                test    flags, #BIT_READY  wz   ' Check ready bit
        if_nz   rdlong  data, ptr               ' Read if ready
        if_nz   add     ptr, #4                 ' Advance if read occurred
```

This sequence takes exactly three clock cycles whether the ready bit is set or clear. If implementing the same logic with branches:

```pasm
                test    flags, #BIT_READY  wz
        if_z    jmp     #skip
                rdlong  data, ptr
                add     ptr, #4
skip
```

The branch version takes 2 cycles when not ready (test + jump) or 4 cycles when ready (test + not-jump + rdlong + add). The timing varies by 100%. The conditional version maintains constant 3-cycle timing.

For real-time code, deterministic timing often matters more than average speed.

### 3.3.3 Complete Condition Table

The P2 provides sixteen conditions that cover all possible combinations of the C and Z flag states, plus two special cases (always and never). Many conditions have multiple names—aliases that make code more readable in different contexts:

| Condition | Aliases | C | Z | True When |
|-----------|---------|---|---|-----------|
| IF_ALWAYS | (none) | * | * | Always executes (unconditional) |
| IF_NEVER | (none) | - | - | Never executes (acts as NOP) |
| IF_C | IF_B | 1 | * | C = 1 (carry set, below) |
| IF_NC | IF_AE, IF_NB | 0 | * | C = 0 (no carry, above or equal) |
| IF_Z | IF_E | * | 1 | Z = 1 (zero, equal) |
| IF_NZ | IF_NE | * | 0 | Z = 0 (not zero, not equal) |
| IF_C_AND_Z | IF_BE | 1 | 1 | C = 1 AND Z = 1 (below or equal) |
| IF_C_AND_NZ | (none) | 1 | 0 | C = 1 AND Z = 0 |
| IF_NC_AND_Z | (none) | 0 | 1 | C = 0 AND Z = 1 |
| IF_NC_AND_NZ | IF_A, IF_NE | 0 | 0 | C = 0 AND Z = 0 (above) |
| IF_C_OR_Z | (none) | 1 or * | * or 1 | C = 1 OR Z = 1 |
| IF_C_OR_NZ | (none) | 1 or * | 0 or * | C = 1 OR Z = 0 |
| IF_NC_OR_Z | (none) | 0 or * | * or 1 | C = 0 OR Z = 1 |
| IF_NC_OR_NZ | (none) | 0 or * | 0 or * | C = 0 OR Z = 0 |
| IF_C_EQ_Z | (none) | same | same | C equals Z (both 0 or both 1) |
| IF_C_NE_Z | (none) | diff | diff | C differs from Z (one 0, one 1) |

The asterisk (*) in the C or Z column means "don't care"—the condition is true regardless of that flag's value. For OR conditions, the notation "1 or *" means C=1 makes the condition true regardless of Z, or Z matching the specified pattern makes it true regardless of C.

### 3.3.4 Comparison Condition Aliases

After a comparison instruction, certain IF_x conditions correspond to familiar relational operators. The aliases make comparison-based conditionals read naturally:

**Unsigned Comparisons (CMP)**

After `CMP a, b WC WZ`, the flags indicate the relationship between unsigned values:

| Condition | Alias | Relational Operator | Meaning |
|-----------|-------|---------------------|---------|
| IF_C | IF_B | < | a is below (less than) b |
| IF_NC | IF_AE | >= | a is above or equal to b |
| IF_Z | IF_E | == | a equals b |
| IF_NZ | IF_NE | != | a not equal to b |
| IF_NC_AND_NZ | IF_A | > | a is above (greater than) b |
| IF_C_OR_Z | IF_BE | <= | a is below or equal to b |

The aliases IF_B (below), IF_AE (above or equal), IF_BE (below or equal), and IF_A (above) correspond exactly to unsigned relational operators. After comparing two unsigned values, these aliases express the intended test clearly.

**Signed Comparisons (CMPS)**

After `CMPS a, b WC WZ`, the same condition names apply but with signed interpretation:

| Condition | Relational Operator | Meaning |
|-----------|---------------------|---------|
| IF_C | < | a is less than b (signed) |
| IF_NC | >= | a is greater or equal to b (signed) |
| IF_Z | == | a equals b |
| IF_NZ | != | a not equal to b |
| IF_NC_AND_NZ | > | a is greater than b (signed) |
| IF_C_OR_Z | <= | a is less or equal to b (signed) |

The conditions are identical, but the comparison instruction (CMP vs. CMPS) determines whether the interpretation is unsigned or signed. Equality (IF_Z) and inequality (IF_NZ) work identically for both—the bit patterns either match or they don't.


## 3.4 Flag Behavior by Instruction Category

Flag meanings vary by instruction category. Understanding these patterns helps predict flag behavior without consulting the instruction reference for each operation.

### 3.4.1 Arithmetic Instructions

Arithmetic instructions set C based on unsigned overflow (carry or borrow) and set Z when the result equals zero:

| Instruction | C Flag (with WC) | Z Flag (with WZ) |
|-------------|------------------|------------------|
| ADD | Unsigned carry out of bit 31 | Result = 0 |
| ADDS | Signed overflow occurred | Result = 0 |
| SUB | Unsigned borrow (A < B) | Result = 0 |
| SUBS | Signed overflow occurred | Result = 0 |
| CMP | Unsigned borrow (A < B) | A = B |
| CMPS | Sign mismatch (signed A < B) | A = B |

For ADD, C=1 indicates that adding the operands produced a value larger than 32 bits can represent—a carry occurred. For SUB and CMP, C=1 indicates the first operand is less than the second (a borrow would be required). The result is always written to the destination (for ADD/SUB) or the flags are set (for CMP/CMPS).

ADDS and SUBS handle signed overflow detection. Signed overflow occurs when adding two positive values produces a negative result, or adding two negative values produces a positive result. The C flag captures this condition with WC.

### 3.4.2 Logic Instructions

Logical instructions set C based on parity and set Z based on whether the result is zero:

| Instruction | C Flag (with WC) | Z Flag (with WZ) |
|-------------|------------------|------------------|
| AND | Parity (odd # of 1 bits) | Result = 0 |
| OR | Parity (odd # of 1 bits) | Result = 0 |
| XOR | Parity (odd # of 1 bits) | Result = 0 |
| NOT | Parity (odd # of 1 bits) | Result = 0 |

Parity means C=1 when the result contains an odd number of 1 bits, and C=0 when the result contains an even number of 1 bits. This enables parity checking for error detection—XOR all data bits together, and C indicates odd parity.

The Z flag behavior is straightforward: Z=1 when the entire 32-bit result is zero. For AND, this occurs when the operands share no common 1 bits. For OR, this occurs when both operands are zero. For XOR, this occurs when the operands are identical.

### 3.4.3 Shift and Rotate Instructions

Shift and rotate instructions capture the bit shifted or rotated out in the C flag:

| Instruction | C Flag (with WC) | Z Flag (with WZ) |
|-------------|------------------|------------------|
| SHL | Bit 31 (MSB shifted out) | Result = 0 |
| SHR | Bit 0 (LSB shifted out) | Result = 0 |
| ROL | Bit 31 (MSB rotated out) | Result = 0 |
| ROR | Bit 0 (LSB rotated out) | Result = 0 |

For left operations (SHL, ROL), the most significant bit (bit 31) moves into C. For right operations (SHR, ROR), the least significant bit (bit 0) moves into C. This enables multi-precision shifts where the bit shifted out of one word becomes the bit shifted into the next word.

The difference between shift and rotate: shifts fill the vacated bit position with 0, while rotates fill it with the bit shifted out (creating a circular rotation). Both capture the bit that exits the register in C.


## 3.5 Common Flag Patterns

Understanding common flag usage patterns accelerates learning and provides templates for solving typical programming problems. These patterns demonstrate how flags enable elegant, efficient solutions.

### 3.5.1 Testing a Bit

Testing whether a specific bit is set uses TEST with WZ:

```pasm
                test    value, #%00000100  wz   ' Test bit 2
        if_nz   jmp     #bit_set                ' Jump if bit is set
```

TEST performs a bitwise AND of its operands but writes the result nowhere—it only sets flags. The mask `%00000100` isolates bit 2. If bit 2 is set, the AND produces a non-zero result (specifically, the value 4), so Z=0. If bit 2 is clear, the AND produces zero, so Z=1.

The condition IF_NZ tests "not zero," which corresponds to "bit is set." This pattern works for testing any single bit or combination of bits—just construct the appropriate mask.

### 3.5.2 Multi-Precision Addition

Adding values wider than 32 bits requires propagating the carry between word additions:

```pasm
        add     x_lo, y_lo      wc      ' Add low words, capture carry
        addx    x_hi, y_hi              ' Add high words plus carry
```

The first ADD adds the low 32 bits and sets C if the addition carries out. The ADDX instruction (Add with Carry) adds the high 32 bits plus the carry from the first addition. This extends to any number of words:

```pasm
        add     x0, y0          wc      ' Add word 0
        addx    x1, y1          wc      ' Add word 1 plus carry
        addx    x2, y2          wc      ' Add word 2 plus carry
        addx    x3, y3                  ' Add word 3 plus carry
```

Each ADDX uses the carry from the previous addition and generates a new carry for the next addition. The result is 128-bit (4 × 32-bit) addition with correct carry propagation.

### 3.5.3 Conditional Assignment

Selecting between two values based on a comparison uses conditional moves:

```pasm
                cmp     a, b            wc      ' Compare a and b
        if_c    mov     result, a               ' If a < b, result = a
        if_nc   mov     result, b               ' If a >= b, result = b
```

This implements `result = min(a, b)` without branches. The comparison sets C if `a < b` (unsigned). Exactly one of the two conditional moves executes, storing the smaller value in result. The sequence takes exactly three clock cycles regardless of which value is smaller.

For maximum of two values, invert the conditions:

```pasm
                cmp     a, b            wc      ' Compare a and b
        if_c    mov     result, b               ' If a < b, result = b
        if_nc   mov     result, a               ' If a >= b, result = a
```

### 3.5.4 Branchless Absolute Value

Computing the absolute value of a signed number uses the ABS instruction with conditional negation:

```pasm
                abs     result, value   wc      ' Absolute value, C = negative
        if_c    neg     result                  ' Correct if was negative
```

Wait—this looks wrong. If ABS already computes the absolute value, why negate it afterward?

The issue is a quirk of two's complement: the most negative value (-2,147,483,648 or $8000_0000) has no positive representation in 32 bits. Its absolute value cannot be represented. The ABS instruction handles this by leaving the value unchanged and setting C to indicate the exceptional case.

For all other negative values, ABS correctly computes the absolute value and clears C. For -2,147,483,648, ABS leaves it unchanged and sets C, and the conditional NEG negates it back to itself (since negating $8000_0000 produces $8000_0000).

Most code doesn't care about this edge case and can simply use `ABS result, value` without the conditional correction.

### 3.5.5 Conditional Increment/Decrement

Updating a counter only when a condition is met uses conditional arithmetic:

```pasm
                test    flags, #FLAG_READY  wz  ' Test ready flag
        if_nz   add     count, #1               ' Increment if ready
```

This increments `count` only when the ready flag is set. No branches are needed, and timing is deterministic—two clock cycles regardless of flag state.

### 3.5.6 Bounds Checking

Checking whether a value falls within a range combines comparison and logical conditions:

```pasm
                cmp     value, min      wc      ' Check if value < min
        if_c    jmp     #out_of_range           ' Too small
                cmp     value, max      wc      ' Check if value >= max
        if_nc   jmp     #out_of_range           ' Too large
                ' Value is in range [min, max)
```

This checks whether `value` is in the range [min, max). The first comparison tests for too small; the second tests for too large. If either condition fails, the value is out of range.


## 3.6 Advanced Flag Usage

Beyond basic conditional execution, the P2 provides specialized instructions for manipulating flags directly and using flags to control data flow. These advanced techniques enable sophisticated flag-based algorithms.

### 3.6.1 Direct Flag Manipulation

The MODC and MODZ instructions modify flags directly without performing computations:

```pasm
        modc    #1              ' Set C flag to 1
        modz    #0              ' Clear Z flag to 0
```

MODC sets C to the specified bit value (0 or 1), and MODZ sets Z to the specified bit value. These instructions are useful when you need to establish specific flag states for subsequent conditional operations, or when implementing custom flag-based protocols.

The MODCZ instruction can modify both flags simultaneously with more complex rules:

```pasm
        modcz   _clr, _set      ' Clear C, set Z
        modcz   _set, _set      ' Set both flags
```

MODCZ accepts operands that specify operations: `_clr` (clear to 0), `_set` (set to 1), `_nc` (copy from C inverted), `_nz` (copy from Z inverted), and others. This enables complex flag manipulation in a single instruction.

### 3.6.2 Flag-Based Bit Manipulation

The MUX family of instructions uses flag values to conditionally modify individual bits:

```pasm
        muxc    value, #mask    ' C=1: set bits; C=0: clear bits
        muxnc   value, #mask    ' C=0: set bits; C=1: clear bits
        muxz    value, #mask    ' Z=1: set bits; Z=0: clear bits
        muxnz   value, #mask    ' Z=0: set bits; Z=1: clear bits
```

These instructions conditionally set or clear bits based on flag values. For example, MUXC sets the masked bits if C=1, or clears them if C=0. This enables building up bit patterns based on multiple flag tests:

```pasm
        test    input, #BIT0    wc      ' Test bit 0 of input
        muxc    output, #%0001          ' Copy bit 0 to output bit 0
        test    input, #BIT1    wc      ' Test bit 1 of input
        muxc    output, #%0010          ' Copy bit 1 to output bit 1
```

This pattern extracts and repositions bits based on flag tests, enabling bit-field manipulation.

### 3.6.3 Flag Preservation Patterns

Sometimes you need to preserve flag values across operations that might modify them. The P2 does not provide a dedicated flag save/restore mechanism, but you can use register operations:

```pasm
        ' Save flags
        wrc     temp            ' Write C to temp[0]
        wrz     temp            ' Write Z to temp[1]

        ' ... operations that modify flags ...

        ' Restore flags
        testb   temp, #0        wc      ' Read temp[0] into C
        testb   temp, #1        wz      ' Read temp[1] into Z
```

The WRC instruction writes C to the specified bit of a register (typically bit 0), and WRZ writes Z to a specified bit (typically bit 1). TESTB tests a specific bit and sets C or Z accordingly, effectively restoring the saved flag values.

An alternative approach uses MODCZ with computed values, but the TESTB pattern is more common and more readable.

### 3.6.4 Flag-Driven State Machines

Flags can encode state transitions in compact state machines. Instead of comparing state variables and branching, use flags to select the next state:

```pasm
                ' Current state determines which flags are set
                test    state, #STATE_IDLE      wz
        if_z    jmp     #handle_idle
                test    state, #STATE_ACTIVE    wz
        if_z    jmp     #handle_active
                test    state, #STATE_DONE      wz
        if_z    jmp     #handle_done
```

This pattern tests state bits and branches to handlers. Each TEST sets Z if the state bit is set, and the conditional jump executes for that state. While this uses jumps (not purely branchless), it demonstrates using flags to encode complex state without comparison operations.


```{=latex}
\begin{keyconcepts}
\item The C flag indicates carry, borrow, bit shifted out, or parity depending on instruction category
\item The Z flag indicates a zero result or equality across nearly all instructions
\item Flags persist until explicitly modified—instructions without WC/WZ/WCZ preserve flag values
\item WC, WZ, and WCZ effects control which flags are updated; the operation always executes
\item Any instruction can be conditional using IF\_x prefixes for deterministic branchless programming
\item 16 conditions cover all combinations of C and Z states, with comparison-friendly aliases
\item Conditional instructions consume one clock cycle whether they execute or not, maintaining deterministic timing
\item Multi-precision arithmetic chains flag results between instructions using ADDX and SUBX
\item Flag-based bit manipulation (MUXC, MUXZ) enables building bit patterns from sequential flag tests
\item Each COG maintains independent C and Z flags with no cross-COG interaction
\end{keyconcepts}
```


<!-- End of Chapter 3 -->

# Chapter 4: Timing and Determinism

<!-- Chapter covering clock cycles, hub windows, and deterministic timing -->

The P2 provides deterministic instruction timing, enabling precise real-time control. Understanding timing characteristics is essential for time-critical applications and optimizing code performance.


## 4.1 Clock Sources and Configuration

Before examining instruction timing, understanding clock configuration is essential—the system clock frequency determines all timing calculations. The P2 supports multiple clock sources, from simple internal oscillators to PLL-multiplied crystals running at 320 MHz.

### 4.1.1 Available Clock Sources

The P2 provides four clock source options, each suited to different application requirements:

**RCFAST** is the internal fast RC oscillator, running at approximately 20-25 MHz. This is the default clock source at power-on and reset. RCFAST requires no external components and provides immediate operation, though its frequency varies with temperature and process. Use RCFAST for applications where precise timing is not critical or as a bootstrap clock while configuring a more accurate source.

**RCSLOW** is the internal slow RC oscillator, running at approximately 20 kHz. This ultra-low-power clock serves sleep modes and real-time clock applications. RCSLOW frequency varies significantly with temperature (±50%), making it unsuitable for precision timing but ideal for power-sensitive applications.

**Crystal oscillator** mode connects an external crystal (typically 10-20 MHz) between the XI and XO pins. The P2 includes internal feedback resistors and programmable loading capacitors, simplifying crystal circuit design. Crystal sources provide the stability needed for precise timing, communication protocols, and frequency synthesis.

**External clock** mode accepts an external clock signal on the XI pin, supporting frequencies from DC to 350 MHz. This mode allows the P2 to synchronize with external timing sources or use specialized oscillators.

### 4.1.2 PLL Multiplication

The Phase-Locked Loop (PLL) multiplies a reference clock to achieve higher frequencies. The PLL takes the crystal or external clock as input and produces an output frequency according to three parameters:

- **Input divider** (1-64): Divides the reference frequency before the VCO
- **VCO multiplier** (1-1024): Multiplies to produce the VCO frequency
- **Post divider** (1-30, even values): Divides the VCO output to the final frequency

The output frequency follows the equation: f_out = (f_ref / input_div) × multiplier / post_div

For example, a 20 MHz crystal with input divider 1, multiplier 16, and post divider 2 produces: (20 MHz / 1) × 16 / 2 = 160 MHz.

The VCO operates optimally between 100-200 MHz. Higher frequencies are possible but may reduce stability. The recommended maximum system clock is 180 MHz; overclocking to 250-320 MHz is possible but application-dependent.

### 4.1.3 The HUBSET Instruction

Clock configuration uses the HUBSET instruction with a 32-bit configuration value:

```pasm
        hubset  ##config_value          ' Configure clock system
```

The configuration value contains fields for crystal mode, clock source selection, and PLL parameters. Key fields include:

| Bits | Field | Purpose |
|------|-------|---------|
| 1:0 | CC | Crystal configuration (loading capacitors) |
| 3:2 | SS | Source select (RCFAST/RCSLOW/crystal/PLL) |
| 7:4 | DDDD | Post divider selection |
| 9 | - | PLL power enable |
| 8 | - | Crystal oscillator enable |
| 27:24 | PPPP | Input divider |
| 23:14 | MMMM | VCO multiplier |

### 4.1.4 Clock Switching Sequence

Switching clock sources requires a careful sequence to ensure glitch-free transitions:

1. **Enable the new source**: Configure crystal oscillator or PLL, but keep the current clock source active
2. **Wait for stabilization**: Crystal oscillators need approximately 10 ms to stabilize; PLL lock requires approximately 10 µs
3. **Switch sources**: Change the SS field to select the new clock source
4. **Optionally disable the old source**: Turn off unused oscillators to save power

```pasm
        hubset  ##%0000_0000_0000_0000_0000_0000_0001_0010  ' Enable xtal
        waitx   ##20_000_000/100                            ' Wait ~10ms
        hubset  ##%0000_0000_0000_0000_0000_0000_0010_0010  ' Switch
```

The P2 provides automatic fallback to RCFAST if the selected clock source fails, preventing system lockup from clock problems.

### 4.1.5 Power Considerations

Clock frequency directly affects power consumption. Lower frequencies reduce power but also reduce performance. For battery-powered applications, consider:

- Use RCSLOW during sleep periods when only basic timekeeping is needed
- Disable the PLL when not required—it consumes power even when not selected
- Run at the lowest frequency that meets timing requirements
- Stop unused COGs to eliminate their clock-related power consumption


## 4.2 Instruction Timing

### 4.2.1 The System Clock

The P2 operates from a system clock that can run up to 320 MHz. All instruction execution, memory access, and I/O operations occur in relation to this master clock. The clock source can be an internal RC oscillator for standalone operation, an external crystal for precision timing, or a PLL-multiplied clock for maximum performance.

Every timing measurement in the P2 is expressed in clock cycles. At 320 MHz, one clock cycle represents 3.125 nanoseconds. This means that a two-cycle instruction completes in 6.25 nanoseconds—fast enough for demanding real-time applications like video generation, high-speed communication protocols, and precision motor control.

Understanding cycle counts is fundamental to P2 programming because the processor provides cycle-accurate timing guarantees. When a program executes the same instruction sequence under the same conditions, it takes exactly the same number of clock cycles every time. This determinism distinguishes the P2 from processors with caches, speculative execution, or variable-latency memory systems.

### 4.2.2 Instruction Cycle Counts

Most COG instructions execute in exactly 2 clock cycles. This consistency simplifies timing calculations and makes hand-optimized assembly code practical. The processor can execute one instruction per two-cycle period, achieving an effective instruction rate of 160 million instructions per second at 320 MHz.

The following table shows typical cycle counts for different instruction categories:

| Instruction Type | Typical Cycles |
|------------------|----------------|
| Register-to-register ALU | 2 |
| Immediate ALU | 2 |
| Branches (not taken) | 2 |
| Branches (taken) | 4 |
| Hub access | 2-16+ |
| CORDIC operations | 2 (start), 54 (wait) |

Register operations like ADD, SUB, AND, and OR complete in 2 cycles whether they operate on registers or immediate values. This uniformity means that choosing between a register operand and an immediate operand has no performance impact—the decision is purely about code clarity and register pressure.

Branch instructions take 2 cycles when the branch is not taken and 4 cycles when taken. This predictable variation allows precise timing of both paths through conditional code. Programmers can eliminate this variation entirely by using conditional execution instead of branches.

Hub memory access instructions have variable timing because they must wait for the COG's hub access window. The base instruction time is 2 cycles, but the wait for hub access adds 0 to 7 additional cycles depending on when the instruction executes relative to the hub rotation pattern.

CORDIC operations use a two-phase execution model. The instruction that starts a CORDIC operation (like QMUL for multiplication) completes in 2 cycles, but the result is not available until 54 cycles after the operation starts. Programs can perform other work during this 54-cycle computation period and retrieve the result later with GETQX or GETQY.

### 4.2.3 Reading Cycle Counts

The instruction encoding table in the P2 documentation provides precise cycle counts in its Clocks column. Understanding the notation used in this column is essential for accurate timing analysis:

| Notation | Meaning |
|----------|---------|
| 2 | Always 2 cycles |
| 2+ | Minimum 2 cycles, may be more |
| 2 or 4 | 2 if not taken, 4 if taken |
| 2 / 8-23 | COG mode / Hub mode |
| 9..35 | Variable range |

A simple "2" means the instruction always takes exactly 2 cycles regardless of operands or conditions. This applies to most arithmetic, logical, and data movement instructions.

The "2+" notation indicates a base time of 2 cycles plus additional variable time. This typically appears for hub access instructions, where the "+" represents the hub window wait time. RDLONG might show "2+~" indicating 2 cycles plus hub wait (the ~ symbol represents hub-related timing).

Branch instructions show "2 or 4" to reflect their dual timing behavior. When the branch condition is false, the processor continues to the next instruction in 2 cycles. When the condition is true, the processor loads a new program counter and takes 4 cycles total.

The "2 / 8-23" notation distinguishes between COG execution mode and hub execution mode. In COG mode (when executing from COG RAM), the instruction takes the first number. In hub execution mode (when executing from hub RAM), the instruction takes longer because the processor must fetch each instruction through the hub access mechanism. The range "8-23" reflects the variability of hub access timing.

Variable range notation like "9..35" indicates that execution time depends on the instruction's parameters or the processor state. For example, REP (repeat) shows variable timing because the total time depends on how many iterations the repeat block executes.


## 4.3 Hub Access Timing

### 4.3.1 The Egg Beater Pattern

```{=latex}
\EggBeaterDiagram
```

Hub memory access uses a round-robin "egg beater" pattern that gives each COG fair access to the shared hub RAM. The name comes from the visual similarity to a rotating egg beater, with each COG's access window spinning through the rotation in sequence.

The hub controller divides time into eight-cycle periods. Within each period, every COG gets exactly one cycle to access hub memory. The access windows rotate continuously through COGs 0, 1, 2, 3, 4, 5, 6, 7, then back to COG 0, repeating this pattern indefinitely. This rotation never stops and never changes—it runs continuously from the moment the chip powers on.

When a COG executes an instruction that accesses hub memory (RDLONG, WRLONG, RDWORD, WRWORD, RDBYTE, or WRBYTE), the instruction waits until that COG's window arrives, performs the memory access during the window, then completes. The wait time depends on when the instruction executes relative to the rotation pattern.

This deterministic rotation means hub access timing is predictable. While the wait time varies from 0 to 7 cycles, the variation follows a fixed pattern. A program that knows its phase relationship to the egg beater can achieve minimum wait times by scheduling hub access to align with its windows.

### 4.3.2 Hub Access Latency

When a COG executes a hub instruction, the actual wait time depends on timing relative to the egg beater rotation. Three scenarios illustrate the range of possibilities:

**Best case:** The instruction executes just as the COG's hub window arrives. The memory access occurs immediately with zero wait cycles. The total instruction time equals the base instruction time (2 cycles) plus the memory access itself (1 cycle), for 3 cycles total.

**Worst case:** The instruction executes just after the COG's hub window has passed. The instruction must wait for the rotation to complete—seven more COGs must take their turns before this COG's window comes around again. This adds 7 wait cycles to the instruction time, for 10 cycles total (2 base + 7 wait + 1 access).

**Average case:** On average, an instruction that executes at a random time relative to the egg beater waits 3.5 cycles for its hub window. This average assumes no deliberate scheduling to align with windows.

The hub access latency directly impacts program performance when hub memory access is frequent. Programs that minimize hub access (by keeping frequently-accessed data in COG registers or COG RAM) avoid this latency. Programs that must access hub memory frequently achieve better performance by organizing hub access into bursts, which amortize the window wait time across multiple memory transfers.

### 4.3.3 Hub Burst Transfers

SETQ enables burst transfers that read or write multiple consecutive longs in a single hub access sequence. This feature dramatically improves hub memory throughput by eliminating the window wait time for all but the first transfer.

The SETQ instruction takes one parameter specifying how many additional longs to transfer. The hub access instruction that follows SETQ performs a burst of that many consecutive transfers:

```pasm
        setq    #15                     ' Transfer 16 longs total
        rdlong  buffer, ptr             ' Burst read from Hub
```

This code reads 16 consecutive longs from hub memory starting at address `ptr` and stores them in COG RAM starting at address `buffer`. The first long experiences normal hub window wait (0-7 cycles), but each subsequent long transfers in just one additional cycle. The total time is approximately 2 (SETQ) + 2 (RDLONG base) + wait (0-7) + 1 + 15 (subsequent longs) = 20-27 cycles—far faster than 16 separate RDLONG instructions, which would average 16 × (2 + 3.5 + 1) = 104 cycles.

Burst transfers work because once a COG has started transferring data during its hub window, it can continue occupying subsequent windows in the rotation. The hub controller grants consecutive windows to a COG performing a burst, allowing continuous transfers without interruption.

SETQ affects only the next hub instruction. If that instruction is not a hub access instruction, SETQ has no effect (some non-hub instructions use SETQ for other purposes). After the hub instruction completes, SETQ must be reissued to enable another burst.

### 4.3.4 FIFO Operations

The P2 includes a hardware FIFO (First In, First Out) buffer that provides the highest-bandwidth method for sequential hub data transfer. Unlike individual hub access instructions that wait for hub windows, the FIFO continuously moves data between hub memory and the COG in the background. The hardware prefetches data before the COG needs it (for reads) or buffers data until hub windows become available (for writes), hiding hub access latency from the program.

**FIFO Architecture:**

Each COG has access to a shared FIFO buffer that can operate in either read mode or write mode (not both simultaneously). The FIFO holds 16 longs (64 bytes) of data, providing substantial buffering to smooth out hub access timing. When reading, the FIFO stays filled by automatically fetching ahead; when writing, the FIFO drains to hub memory during available hub windows.

**Setting Up the Read FIFO:**

RDFAST configures the FIFO for reading from hub memory. The instruction takes two parameters: a block count (or 0 for continuous operation) and the starting hub address:

```pasm
        rdfast  #0, ptr                 ' Start continuous read FIFO
loop
        rflong  data                    ' Read from FIFO (fast, no hub wait)
        ' ... process data ...
        jmp     #loop                   ' Continue reading
```

The RFLONG, RFWORD, and RFBYTE instructions read from the FIFO without waiting for hub windows—if data is available in the FIFO buffer, the read completes immediately. The FIFO refills automatically in the background using whatever hub windows become available.

**Setting Up the Write FIFO:**

WRFAST configures the FIFO for writing to hub memory:

```pasm
        wrfast  #0, ptr                 ' Start continuous write FIFO
loop
        ' ... generate data ...
        wflong  data                    ' Write to FIFO (fast, no hub wait)
        jmp     #loop                   ' Continue writing
```

The WFLONG, WFWORD, and WFBYTE instructions write to the FIFO buffer. If buffer space is available, the write completes immediately without waiting for a hub window. The FIFO drains to hub memory automatically.

**Circular Buffer Mode:**

The FIFO supports circular buffer operation for continuous streaming. When configured with a block count, the FIFO wraps back to the starting address after transferring the specified number of longs:

```pasm
        rdfast  #256, audio_buffer      ' Read 256 longs, then wrap to start
```

This creates a 1KB circular buffer. The program can continuously read from the FIFO while another process (perhaps on a different COG) refills the buffer behind the read pointer. Circular buffers enable double-buffering and continuous streaming without explicit pointer management.

**FIFO Events:**

The FIFO generates events that programs can monitor for buffer management:

- **EVENT_FBW** (FIFO Block Wrap) signals when the FIFO wraps around in circular buffer mode. Programs use this event to know when to refill the next section of a circular buffer or to synchronize with buffer boundaries.

Programs can wait for this event using WAITSE or poll it using POLLSE after configuring a selectable event source. This enables efficient ping-pong buffering where one COG fills buffers while another consumes them.

**FIFO and the Streamer:**

The Streamer subsystem (described in Chapter 5) uses the FIFO for high-bandwidth data transfer to and from I/O pins. When the Streamer is active, it shares the FIFO with FIFO access instructions. RDFAST/WRFAST configure the FIFO source or destination in hub memory; the Streamer then moves data between the FIFO and pins at rates matching the system clock. This combination enables video generation, audio streaming, and high-speed data acquisition without per-sample CPU intervention.

**Performance Considerations:**

FIFO access provides near-instantaneous data transfer from the program's perspective—no hub window waiting, no variable latency. However, the FIFO has finite depth. If a program reads faster than the FIFO can refill (or writes faster than it can drain), the FIFO stalls waiting for hub access. For sustained maximum throughput, balance data production/consumption rate with the hub's aggregate bandwidth.

The FIFO access instructions (RFLONG, RFWORD, RFBYTE, WFLONG, WFWORD, WFBYTE) complete in 2 cycles when the FIFO has data available or space available, respectively. This makes FIFO access ideal for streaming applications: video pixel generation, audio sample processing, high-speed communication protocols, and bulk data movement.


## 4.4 Deterministic Timing

### 4.4.1 What Determinism Means

The P2's deterministic timing guarantees that the same instruction sequence, executing under the same conditions, takes exactly the same number of clock cycles every time it runs. This guarantee holds across all executions—there are no cache misses, no speculative execution failures, no memory controller delays, and no unpredictable pipeline stalls.

Determinism provides several critical benefits for embedded systems programming:

**Predictable performance:** When a routine takes 1,000 cycles during testing, it takes 1,000 cycles in production. Performance measurements made during development remain accurate in the deployed system.

**Reliable timing:** Real-time systems can meet hard timing deadlines because worst-case execution time equals actual execution time. If an interrupt handler must complete within 500 cycles, testing that it does so once proves it always will.

**Reproducible behavior:** Timing-related bugs are reproducible because timing is consistent. A race condition that appears during development will appear in the same way in production, making debugging practical.

**Simplified analysis:** Programmers can calculate execution time by hand, adding up cycle counts from the instruction table. This makes optimization straightforward—identify the critical path, count cycles, improve the slow parts.

The P2 achieves determinism through architectural choices: no instruction cache (COG RAM provides fast local storage without cache complexity), no data cache (hub access uses predictable round-robin scheduling), no branch prediction (conditional execution eliminates branches), and no speculative execution (instructions execute in program order).

### 4.4.2 Sources of Timing Variation

While the P2 provides deterministic timing, four sources of variation exist. These variations are predictable and controllable, not random like cache misses or memory arbitration in complex processors:

| Source | Variation | Mitigation |
|--------|-----------|------------|
| Hub access wait | 0-7 cycles | HUBSET sync, careful scheduling |
| Branches | 2 vs 4 cycles | Conditional execution instead |
| CORDIC wait | Up to 54 cycles | Interleave other work |
| WAITX | Variable | Intentional delays |

**Hub access wait** varies from 0 to 7 cycles depending on when a hub instruction executes relative to the egg beater rotation. This variation is deterministic—if a program executes a hub instruction at the same point in the egg beater cycle, the wait time is identical. Programs can eliminate this variation by synchronizing with the egg beater using HUBSET, or by scheduling hub access to occur at aligned points in loops.

**Branch timing** varies because taken branches require 4 cycles while not-taken branches require only 2 cycles. This variation is completely predictable—the same branch decision always takes the same time. Programs can eliminate this variation by using conditional execution instead of branches, trading the variable 2-or-4-cycle branch for a fixed 2-cycle conditional instruction.

**CORDIC wait** varies because different CORDIC operations take different amounts of time to compute. Multiplication, division, square root, and trigonometric functions each have specific completion times. The variation is deterministic—the same operation always takes the same time. Programs hide CORDIC latency by issuing the operation early and performing other work during the computation period.

**WAITX** provides intentional variable delay. This is the only case where variation is desired rather than avoided—WAITX exists specifically to introduce precise, controlled timing delays for applications like bit-banging protocols or pulse generation.

### 4.4.3 Eliminating Branches

Conditional execution provides an alternative to branching that eliminates timing variation. Instead of using a compare instruction followed by a conditional jump, code can use a compare instruction followed by conditionally-executed instructions.

The branching approach introduces timing variation:

```pasm
' With branch (2 or 4 cycles):
        cmp     a, b            wz
        if_z    jmp     #equal_case
        ' Not-equal path continues here
```

When `a` equals `b`, this code takes 2 (CMP) + 4 (JMP taken) = 6 cycles. When `a` differs from `b`, the code takes 2 (CMP) + 2 (JMP not taken) = 4 cycles. The 2-cycle variation complicates timing analysis.

The conditional execution approach provides constant timing:

```pasm
' Without branch (2 cycles always):
        cmp     a, b            wz
        if_z    mov     result, #1
        if_nz   mov     result, #0
```

This code takes 2 (CMP) + 2 (first MOV, executed if Z set) + 2 (second MOV, executed if Z clear) = 6 cycles when Z is set, or 2 (CMP) + 2 (first MOV, skipped) + 2 (second MOV, executed) = 6 cycles when Z is clear. Both paths take exactly 6 cycles.

The key insight is that conditionally-skipped instructions still consume their execution time slot—the processor evaluates the condition and skips the instruction's effect, but the instruction still occupies 2 cycles. This behavior ensures that all execution paths through conditionally-executed code take the same time.

Conditional execution works for simple cases where both branches are short. For longer code sequences or cases where only one branch performs work, traditional branching may be more efficient despite the timing variation. The choice depends on whether consistent timing or shorter average time is more important for the specific application.


## 4.5 Synchronization

### 4.5.1 WAITX - Precise Delays

WAITX provides precise, cycle-accurate delays by pausing execution for a specified number of clock cycles:

```pasm
        waitx   ##100                   ' Wait exactly 100 cycles
```

The instruction accepts a value specifying the delay duration. Execution resumes exactly after that many cycles have elapsed. This precision makes WAITX essential for timing-critical operations like bit-banging communication protocols, generating precise pulse widths, or synchronizing with external events.

WAITX delays are relative to when the instruction executes. If a program needs to generate a pulse every 1,000 cycles, using WAITX alone accumulates timing drift because the WAITX instruction itself consumes time, and the instructions between WAITX calls add additional cycles. For precise periodic timing without drift, the counter-based wait instructions provide better alternatives.

### 4.5.2 Counter-Based Waiting

The P2 provides a global cycle counter that increments every clock cycle. COGs can read this counter with GETCT and wait for specific counter values using the WAITCT family of instructions. This mechanism enables drift-free periodic timing.

Each COG has three independent counter match registers (CT1, CT2, CT3). Programs load target counter values into these registers using ADDCT1, ADDCT2, or ADDCT3, then wait for the counter to reach those values using WAITCT1, WAITCT2, or WAITCT3:

```pasm
        getct   time                    ' Read current time
        addct1  time, ##1000            ' Set CT1 = time + 1000
        ' ... do work ...
        waitct1                         ' Wait until counter reaches CT1
```

This pattern ensures that the wait completes exactly 1,000 cycles after the GETCT instruction, regardless of how long the intervening work takes. If the work completes in 800 cycles, WAITCT1 waits 200 more cycles. If the work takes 1,200 cycles, WAITCT1 returns immediately (the deadline has already passed).

For periodic operations, adding a fixed delta to the counter match register each iteration eliminates drift:

```pasm
        getct   time                    ' Initialize time base
loop
        addct1  time, ##1000            ' Next deadline = previous + 1000
        ' ... generate pulse or process data ...
        waitct1                         ' Wait for next period
        jmp     #loop
```

Each iteration runs exactly 1,000 cycles from the previous iteration, maintaining perfect periodicity regardless of small variations in the work performed each cycle.

### 4.5.3 Hub Slot Synchronization

Programs that need predictable hub access timing can synchronize with the egg beater rotation using HUBSET. This instruction provides control over hub timing parameters and can align a COG's execution with its hub access windows.

While HUBSET's primary purpose is configuring hub execution mode, it also provides synchronization side effects. When a COG enters hub execution mode, it aligns with the hub rotation, ensuring that subsequent hub access occurs at known phases of the egg beater cycle.

For applications that need consistent hub access timing without entering hub execution mode, careful scheduling provides an alternative. If a loop performs hub access at regular intervals aligned with the 8-cycle egg beater period, the hub wait time remains consistent across iterations:

```pasm
loop
        ' ... exactly 8 cycles of work ...
        rdlong  data, ptr               ' Hub access occurs at same phase
        ' ... more work ...
        jmp     #loop                   ' Loop maintains 8-cycle alignment
```

This technique requires precise cycle counting and works only when the loop body contains an integer multiple of 8 cycles.

### 4.5.4 Pin-Based Synchronization

Several instructions synchronize with pin state changes, enabling precise timing relative to external events:

**WAITATN** waits for any pin to make a low-to-high transition (attention flag). Smart Pins can be configured to set their ATN flags on specific conditions, making WAITATN useful for waiting on external events with minimal COG overhead.

**WAITSE1, WAITSE2, WAITSE3, WAITSE4** wait for streamer events. The streamer can transfer data to or from pins with precise timing, and these wait instructions synchronize code execution with streamer operations.

**WAITPAT** waits for a pin pattern match. Programs configure a pattern and mask, then WAITPAT suspends execution until the pin states match the specified pattern. This enables synchronization with parallel interfaces or detection of specific pin combinations.

**POLLATE, POLLCT1, POLLCT2, POLLCT3** provide polling-based alternatives to waiting. Instead of blocking until a condition occurs, these instructions check whether an event has occurred and set flags accordingly. This allows code to perform useful work while watching for events, rather than waiting idly.


## 4.6 Timing-Critical Patterns

### 4.6.1 Cycle-Exact Loops

Many real-time applications require loops that execute with precise, predictable timing. The P2's deterministic instruction timing makes cycle-exact loops practical and reliable.

Consider a loop that reads data from hub memory, processes it, and repeats:

```pasm
' 8-cycle loop body (fits in one Hub window period)
loop
        rdlong  data, ptr               ' 2 + wait cycles
        add     ptr, #4                 ' 2 cycles
        djnz    count, #loop            ' 4 cycles (taken)
```

This loop body must account for hub access timing variation. If the loop starts aligned with the COG's hub window, RDLONG waits 0 cycles and the loop takes 2 + 2 + 4 = 8 cycles. If the loop starts just after the hub window, RDLONG waits 7 cycles and the loop takes 9 + 2 + 4 = 15 cycles.

For truly cycle-exact timing, loops must either eliminate hub access or align hub access with the egg beater rotation. One approach uses COG RAM for all data, avoiding hub access entirely:

```pasm
loop
        add     data, #1                ' 2 cycles
        djnz    count, #loop            ' 4 cycles (taken)
        ' Exactly 6 cycles per iteration
```

Another approach aligns the loop body to an 8-cycle boundary and ensures hub access occurs at the same phase each iteration:

```pasm
loop
        rdlong  data, ptr               ' 2 + wait (same wait each time)
        add     result, data            ' 2 cycles
        add     ptr, #4                 ' 2 cycles
        djnz    count, #loop            ' 4 cycles (taken)
        nop                             ' 2 cycles - padding to 16 total
        ' Loop body = 16 cycles (2× hub period)
```

If the first iteration experiences 3 cycles of hub wait, every subsequent iteration also experiences 3 cycles of wait because the 16-cycle loop maintains alignment with the 8-cycle hub period.

### 4.6.2 Pipelined Hub Access

Programs can hide hub access latency by overlapping computation with hub waiting. Instead of waiting for one hub operation to complete before starting the next computation, a program can issue a hub access and immediately begin computing with data already available, allowing the hub access to proceed in parallel.

The SETQ-based burst transfer provides one form of pipelining—while later longs transfer, the program can begin processing earlier longs. A more general approach separates hub access from computation:

```pasm
loop
        rdlong  next_data, next_ptr     ' Start fetching next data
        add     next_ptr, #4
        ' Process current_data while hub fetch proceeds
        add     result, current_data
        sub     current_data, offset
        mov     current_data, next_data ' Previous fetch is now ready
        djnz    count, #loop
```

This pattern keeps hub access and computation overlapped—the RDLONG for iteration N+1 occurs while iteration N's computation proceeds. The technique works best when computation time roughly equals hub access time, maximizing overlap.

### 4.6.3 CORDIC Pipelining

CORDIC operations take 54 cycles to compute results, but the instruction that starts a CORDIC operation completes in just 2 cycles. This creates an opportunity for pipelining: start a CORDIC operation, perform other work during the 54-cycle computation period, then retrieve the result.

A simple example shows the pattern:

```pasm
        qmul    a, b                    ' Start multiply
        ' ... 54 cycles of other work ...
        getqx   result                  ' Get result (low 32 bits)
```

For maximum efficiency, interleave multiple CORDIC operations with other work:

```pasm
        qmul    a1, b1                  ' Start first multiply
        ' ... some work ...
        qmul    a2, b2                  ' Start second multiply
        ' ... more work ...
        getqx   result1                 ' Get first result
        ' ... more work ...
        getqx   result2                 ' Get second result
```

The key constraint is that at least 54 cycles must elapse between starting a CORDIC operation and retrieving its result. If GETQX executes too early, it retrieves an incomplete result. If it executes later, the result remains available—CORDIC results persist until the next CORDIC operation starts.

Multiple CORDIC operations can be in flight simultaneously, with results retrieved in order. Starting a new CORDIC operation does not invalidate results from previous operations until their results have been read.

### 4.6.4 Deterministic I/O

Bit-banging—directly controlling I/O pins with software timing—requires cycle-accurate execution. The P2's deterministic timing makes bit-banging practical for protocols like WS2812 LED control, custom serial formats, or precise pulse generation.

A WS2812 LED protocol example demonstrates the precision required:

```pasm
' WS2812 requires precise pulse widths:
' 0 bit: 400ns high, 850ns low
' 1 bit: 800ns high, 450ns low
' At 200 MHz (5ns per cycle):
' 0 bit: 80 cycles high, 170 cycles low
' 1 bit: 160 cycles high, 90 cycles low

send_bit
        test    data, #31       wc      ' Get high bit into C flag
        drvh    pin                     ' Start pulse (high)
        if_c    waitx   ##160           ' 1-bit: wait 160 cycles
        if_nc   waitx   ##80            ' 0-bit: wait 80 cycles
        drvl    pin                     ' End pulse (low)
        if_c    waitx   ##90            ' 1-bit: wait 90 cycles
        if_nc   waitx   ##170           ' 0-bit: wait 170 cycles
        rol     data, #1                ' Shift to next bit
        djnz    count, #send_bit
```

This code generates precise pulse widths using WAITX for delays and conditional execution to avoid branch timing variation. The DRVH and DRVL instructions change pin states, and the WAITX instructions maintain exact timing between transitions.

Deterministic timing eliminates the jitter and uncertainty common in systems with caches or interrupts. Each pulse width is exactly the specified duration, enabling reliable communication with timing-sensitive devices.


## 4.7 Measuring Execution Time

### 4.7.1 The Cycle Counter

The P2 provides a global 32-bit cycle counter that increments every clock cycle. This counter runs continuously from power-on and wraps around after reaching its maximum value. COGs read the counter using the GETCT instruction, which returns the current counter value.

Measuring code execution time involves reading the counter before and after the code section of interest:

```pasm
        getct   start_time              ' Read cycle counter
        ' ... code to measure ...
        getct   end_time                ' Read cycle counter again
        sub     end_time, start_time    ' Elapsed cycles
```

The difference between the two readings gives the exact number of cycles elapsed. This measurement includes the cycles consumed by GETCT itself (2 cycles each), so precise measurements should account for this overhead.

For short code sequences, the measurement overhead matters. Measuring a 10-cycle sequence with two GETCT instructions reports 14 cycles (2 + 10 + 2). For longer sequences, the 4-cycle overhead becomes negligible.

The cycle counter is global across all COGs—all COGs read the same counter value. This enables synchronization and coordination between COGs. One COG can mark a time value and pass it to another COG via hub memory, allowing the second COG to measure time relative to events in the first COG.

### 4.7.2 Counter Wrap-Around

The 32-bit cycle counter wraps around every 2³² cycles. At 320 MHz, this occurs every 13.4 seconds. Code that measures elapsed time must handle wrap-around correctly.

Subtraction using unsigned arithmetic naturally handles wrap-around. When end_time is less than start_time (because wrap-around occurred), the subtraction `end_time - start_time` produces the correct elapsed time due to modular arithmetic:

```pasm
        mov     start_time, ##$FFFF_FFF0  ' Near wrap-around
        mov     end_time,   ##$0000_0010  ' After wrap-around
        sub     end_time, start_time      ' Result: $20 (32 cycles)
```

This automatic wrap-around handling works for elapsed times up to 2³¹ cycles (half the counter range). For longer measurements, code must count wrap-around events explicitly or use multiple counter values.

### 4.7.3 Profiling Techniques

GETCT enables detailed performance profiling of assembly code. By measuring execution time for different code paths, programmers can identify performance bottlenecks and verify that optimizations achieve expected speedups.

A common profiling pattern measures loop iteration time:

```pasm
        mov     iterations, ##1000
        getct   start_time
loop
        ' ... code to profile ...
        djnz    iterations, #loop
        getct   end_time
        sub     elapsed, end_time, start_time
```

The total elapsed time divided by the iteration count gives the average time per iteration. For more detailed profiling, place multiple GETCT measurements within the loop to identify which parts of the loop consume the most time:

```pasm
loop
        getct   time1
        ' ... section A ...
        getct   time2
        ' ... section B ...
        getct   time3
        sub     timeA, time2, time1       ' Section A timing
        sub     timeB, time3, time2       ' Section B timing
        ' Store or accumulate timing data
        djnz    iterations, #loop
```

This approach provides cycle-accurate timing for each code section, enabling precise optimization. The overhead of GETCT instructions affects absolute timing but not the relative timing between sections.

Profiling can reveal unexpected timing variations. If a loop shows inconsistent timing across iterations, the variation likely comes from hub access timing, branch behavior, or CORDIC latency. Identifying these variations guides optimization efforts toward the actual bottlenecks rather than presumed slow code.


## 4.8 COG vs Hub Execution Mode Timing

### 4.8.1 COG Execution Mode

COG execution mode—often called "COG mode"—executes instructions from the COG's local 512-long (2KB) RAM. This provides the fastest possible execution because instruction fetch occurs from the COG's private memory without any shared resource contention.

In COG mode, most instructions complete in exactly 2 clock cycles. The processor fetches an instruction and executes it without waiting for memory access arbitration, cache lookups, or bus conflicts. This predictable timing makes COG mode ideal for timing-critical code like interrupt handlers, real-time control loops, and I/O bit-banging.

COG mode execution begins when a COG starts via COGINIT with a COG RAM address (0-$1FF). The program counter points to COG RAM locations, and instruction fetch proceeds at full speed. All 512 longs of COG RAM are available for code and data, though programs typically reserve some locations for data and use the remainder for code.

The limitation of COG mode is size—only 512 longs of code and data combined. Programs that need more code space must use hub execution mode or carefully manage code overlays.

### 4.8.2 Hub Execution Mode

Hub execution mode—often called "HUBEXEC mode"—executes instructions from hub RAM. This allows programs to exceed the 512-long COG RAM size limit, supporting much larger code bases at the cost of slower instruction fetch.

In hub execution mode, each instruction fetch waits for the COG's hub access window. This adds 0-7 cycles of wait time per instruction, similar to how hub data access works. The average instruction fetch time becomes 2 (base) + 3.5 (average hub wait) = 5.5 cycles, roughly 2.75× slower than COG mode.

Hub execution mode begins when a COG starts via COGINIT with a hub RAM address ($200 or higher). The program counter points to hub RAM locations, and the processor fetches instructions through the egg beater hub access mechanism. Code can be megabytes in size, limited only by available hub RAM.

Despite the slower instruction fetch, hub mode remains useful for several scenarios:

**Large programs:** When code exceeds 512 longs, hub mode is the only option short of implementing code overlays.

**Non-critical code:** Initialization routines, background tasks, and other code without tight timing requirements run acceptably in hub mode.

**Mixed execution:** Programs can start in hub mode and copy time-critical sections to COG RAM for execution at full speed. COGINIT can switch a running COG between hub and COG mode dynamically.

### 4.8.3 Timing Comparison

The following table shows typical execution times for common operations in both execution modes:

| Operation | COG Mode | Hub Mode |
|-----------|----------|----------|
| Simple ALU | 2 cycles | 8-23 cycles |
| Branch taken | 4 cycles | 12-27 cycles |
| Hub access | 2 + hub wait | 2 + hub wait |
| CORDIC start | 2 cycles | 8-23 cycles |

Simple ALU operations (ADD, SUB, AND, OR, etc.) take 2 cycles in COG mode but 8-23 cycles in hub mode. The hub mode time includes instruction fetch delay—the actual execution is still 2 cycles, but fetching the instruction adds the variable hub wait. The range 8-23 represents minimum (just hit hub window) to maximum (just missed hub window) timing.

Branch instructions take 4 cycles in COG mode when taken. In hub mode, the taken branch must fetch the target instruction through the hub, adding 8-21 cycles for a total of 12-27 cycles.

Hub access instructions show the same timing in both modes because the data access (as opposed to instruction fetch) uses the hub window mechanism regardless of where the instruction itself came from. A RDLONG takes 2 + hub wait whether executing from COG RAM or hub RAM.

CORDIC operations start in 2 cycles in COG mode but take 8-23 cycles to start in hub mode (the 54-cycle computation time is the same in both modes). The instruction that starts the CORDIC operation must be fetched before it can execute, incurring hub fetch delay in hub mode.

The dramatic timing difference between modes—often 4× or more—makes COG mode strongly preferred for timing-critical code. Programs typically keep inner loops, interrupt handlers, and time-sensitive operations in COG RAM while using hub mode for larger, less-critical code sections.


```{=latex}
\begin{keyconcepts}
\item System clock configurable from 20 kHz (RCSLOW) to 320 MHz (PLL) via HUBSET
\item Most COG instructions execute in exactly 2 clock cycles
\item Branch instructions take 2 cycles if not taken, 4 cycles if taken
\item Hub access uses round-robin timing with 0-7 cycle wait for window
\item Burst transfers (via SETQ) amortize Hub access overhead
\item The P2 provides deterministic timing with no cache or speculative execution
\item Conditional execution eliminates branch timing variation
\item GETCT reads the cycle counter for precise timing measurement
\item Hub execution mode adds instruction fetch latency
\end{keyconcepts}
```


<!-- End of Chapter 4 -->

# Chapter 5: Special Hardware Overview

The P2 includes specialized hardware subsystems that extend beyond basic instruction execution. Understanding these subsystems enables advanced applications: the CORDIC coprocessor accelerates mathematical operations, Smart Pins provide programmable I/O peripherals, the Streamer enables high-speed data movement, events support responsive programming, hardware locks coordinate multi-COG applications, and debug hardware assists development. This chapter provides an overview of each subsystem; detailed instruction usage is covered in Part II, and complete subsystem documentation is available in specialized manuals.


## 5.1 CORDIC Coprocessor

The CORDIC (Coordinate Rotation Digital Computer) coprocessor provides hardware-accelerated mathematical operations. While the P2's instruction set includes basic arithmetic, the CORDIC handles operations that would otherwise require hundreds of instructions: 32×32-bit multiplication producing 64-bit results, division with quotient and remainder, square root extraction, trigonometric computations, and logarithmic functions. The CORDIC operates as a queue-based coprocessor—your code initiates an operation, performs other useful work for 54 clock cycles while the CORDIC computes, then retrieves the results.

### 5.1.1 CORDIC Capabilities

The CORDIC provides eight categories of operations, each accessed through dedicated queue instructions:

| Operation | Instruction | Output |
|-----------|-------------|--------|
| Multiply | QMUL | 64-bit product (low 32 bits in X, high 32 bits in Y) |
| Divide | QDIV | Quotient in X, remainder in Y |
| Fractional divide | QFRAC | Fractional quotient in X, remainder in Y |
| Square root | QSQRT | Integer square root in X |
| Rotate | QROTATE | Rotated X coordinate, rotated Y coordinate |
| Vector | QVECTOR | Magnitude in X, angle in Y (Cartesian to polar) |
| Logarithm | QLOG | Natural log approximation in X |
| Exponential | QEXP | e^x approximation in X |

Each operation produces one or two 32-bit results, retrieved through GETQX and GETQY instructions. The multiply operation (QMUL) is particularly valuable for fixed-point arithmetic, providing the full 64-bit product that would otherwise require complex multi-instruction sequences.

### 5.1.2 CORDIC Operation Flow

CORDIC operations follow a three-step pattern: queue the operation, wait for computation, retrieve results. The critical timing constraint is the 54-cycle computation period—attempting to retrieve results before this period completes produces undefined values.

```pasm
        qmul    multiplicand, multiplier    ' Start 32x32 multiply
        ' ... 54 cycles of other useful work ...
        getqx   product_lo                  ' Get low 32 bits
        getqy   product_hi                  ' Get high 32 bits
```

The 54-cycle computation period is fixed for all CORDIC operations. Efficient code interleaves CORDIC computations with other processing, ensuring the CPU remains productive while the coprocessor works. The CORDIC operates independently once queued, allowing the COG to execute unrelated instructions during the computation period.

### 5.1.3 CORDIC Pipelining

The CORDIC queue depth is one operation—queueing a second operation before retrieving the first operation's results discards the first results. However, the queue-and-wait pattern enables a form of software pipelining:

```pasm
loop    qmul    current_a, current_b        ' Start operation N
        ' ... process previous results ...
        getqx   prev_lo                     ' Get operation N-1 results
        getqy   prev_hi
        ' ... prepare next operands ...
        jmp     #loop                       ' Cycle repeats
```

This pattern maintains one CORDIC operation in flight while processing previous results and preparing next operands. The 54-cycle latency becomes hidden when operations repeat in a loop structure.

### 5.1.4 CORDIC Instructions Reference

**Queue Operations:** QMUL, QDIV, QFRAC, QSQRT, QROTATE, QVECTOR, QLOG, QEXP

**Result Retrieval:** GETQX, GETQY

Full instruction details, including operand formats and result interpretations, appear in Part II under each instruction's entry.


## 5.2 Smart Pins

The P2 provides 64 Smart Pins, one per I/O pin, each containing a complete programmable peripheral. Smart Pins eliminate the need for external support chips in many applications—a single Smart Pin can implement a UART transmitter and receiver, generate PWM signals, measure pulse widths, read quadrature encoders, or convert analog signals. Each Smart Pin contains local state machines, DAC and ADC hardware, timing circuits, and configuration registers, all controlled through PASM2 instructions. The Smart Pin architecture offloads I/O processing from the COG, allowing precise timing and continuous operation without software intervention.

### 5.2.1 Smart Pin Architecture

Each Smart Pin integrates multiple hardware components that work together to implement various I/O functions:

- **Configurable I/O circuitry:** Programmable pull-up/down resistors, output drivers, and high-impedance (floating) modes
- **Mode selection logic:** 64 distinct operating modes covering digital, analog, serial, and timing applications
- **Local state machine:** Autonomous operation once configured, generating events when data is ready
- **DAC hardware:** 8-bit digital-to-analog converter for analog output and sigma-delta modulation
- **ADC hardware:** Analog-to-digital conversion using sigma-delta and comparator techniques
- **Timing hardware:** Counters and comparators for precise edge detection and pulse generation

The Smart Pin's autonomous operation is particularly significant. Once configured, a Smart Pin operates independently of the COG—a UART Smart Pin transmits and receives bytes, a PWM Smart Pin generates continuous waveforms, an encoder Smart Pin tracks position changes, all without ongoing CPU attention. The COG interacts with Smart Pins only when new data arrives or new output is needed.

### 5.2.2 Smart Pin Modes

Smart Pins support 64 distinct modes organized into functional categories. Each mode transforms the pin into a specialized peripheral:

| Category | Example Modes | Typical Applications |
|----------|---------------|----------------------|
| Digital I/O | Repository mode, registered input, long pulse accumulator | Debounced buttons, event counting, pulse measurement |
| Serial | UART transmit/receive, synchronous serial, SPI | Communication with peripherals and other systems |
| PWM | PWM/duty mode, triangle/sawtooth mode, incremental mode | Motor control, LED dimming, audio generation |
| Analog | DAC output, ADC sampling, comparator | Sensor interfacing, analog signal generation |
| Timing | Period measurement, pulse width measurement, timeout | Frequency measurement, event timing, watchdog |
| Quadrature | Quadrature encoder input | Rotary encoder reading, motor position feedback |

Mode selection determines the pin's complete behavior: input vs. output, edge sensitivity, data format, timing parameters, and event generation. The mode value, written through WRPIN, configures all aspects of the Smart Pin's operation.

### 5.2.3 Smart Pin Instructions

Smart Pin operation involves three phases: configuration, communication, and direction/output control. PASM2 provides dedicated instructions for each phase.

**Configuration Instructions:**

Configuration establishes the Smart Pin's operating mode and parameters:

- **WRPIN** - Write pin mode (selects one of 64 operating modes)
- **WXPIN** - Write X parameter (mode-specific configuration value)
- **WYPIN** - Write Y parameter (mode-specific configuration value or output data)

The three-register configuration pattern (mode, X, Y) provides each mode with sufficient parameters. For example, UART mode uses X for bit timing and Y for transmit data; PWM mode uses X for period and Y for duty cycle.

**Communication Instructions:**

Communication instructions transfer data between the COG and Smart Pin:

- **RDPIN** - Read Smart Pin data and acknowledge (clears ready flag)
- **RQPIN** - Read Smart Pin data without acknowledge (preserves ready flag)
- **AKPIN** - Acknowledge only (clears ready flag without reading)

The read-and-acknowledge pattern prevents missing data. A Smart Pin sets its ready flag when new data arrives; RDPIN retrieves the data and clears the flag in one atomic operation. RQPIN allows checking values without consuming data, useful for monitoring inputs.

**Direction and Output Control Instructions:**

Direction and output control manage the physical pin state. The P2 provides six instruction families, each with six variants (set-low, set-high, clear, not-clear, zero, not-zero):

- **DIR** family - Set pin direction (input vs. output)
- **OUT** family - Set output value (when pin is output)
- **FLT** family - Float pin to high-impedance (tri-state)
- **DRV** family - Drive pin (opposite of float)

Each family includes suffix variants: `L` (low/0), `H` (high/1), `C` (clear if condition), `NC` (not-clear if condition), `Z` (set if zero), `NZ` (set if not-zero). This provides fine-grained control: `DIRL` forces pin low, `DIRZ` sets direction to input only if condition is zero.

### 5.2.4 Smart Pin Documentation

Smart Pin modes vary significantly in configuration and operation. The mode value, X parameter, and Y parameter have different meanings for each mode—UART mode parameters differ completely from PWM mode parameters. Complete Smart Pin mode documentation, including configuration values, timing diagrams, and usage examples, appears in the **P2 Smart Pins Tutorial** (`p2-smart-pins-tutorial`). That manual provides essential reference material for Smart Pin programming.


## 5.3 Streamer

The Streamer provides DMA-like high-speed data movement between Hub memory and I/O pins. While Smart Pins handle byte-level serial I/O, the Streamer specializes in bulk data transfer at rates matching the system clock—transferring pixels to displays, streaming audio samples to DACs, generating complex waveforms, or receiving high-speed ADC data. The Streamer operates autonomously once configured, fetching data from Hub memory and delivering it to output pins (or capturing from input pins) without COG intervention. This frees the COG to perform computations while data flows continuously.

### 5.3.1 Streamer Capabilities

The Streamer excels at applications requiring continuous data flow at precise timing:

- **RGB/pixel streaming:** Driving LED panels, VGA displays, or other parallel pixel interfaces requiring continuous refresh
- **ADC/DAC streaming:** Audio applications where sample streams flow continuously between Hub memory and audio hardware
- **Waveform generation:** Creating complex analog waveforms through DAC output, including modulated signals
- **High-speed data acquisition:** Capturing parallel data from external ADCs or digital sensors

The Streamer's key characteristic is autonomy—once initialized with a Hub memory address and transfer parameters, it fetches and outputs data without further CPU involvement. The COG can prepare the next buffer, perform signal processing on captured data, or execute unrelated tasks while the Streamer handles data movement.

### 5.3.2 Streamer Instructions

Streamer operation involves configuration, initiation, and control. The instruction set provides precise control over transfer timing and data flow.

**Configuration and Control:**

- **SETXFRQ** - Set streamer frequency (controls output sample rate)
- **XINIT** - Initialize streamer transfer (configures mode and starts first transfer)
- **XCONT** - Continue streamer operation (starts next transfer using current configuration)
- **XZERO** - Zero-fill streamer output (outputs zeros without fetching Hub data)
- **XSTOP** - Stop streamer (halts transfer operation)

The typical pattern initializes the Streamer with XINIT for the first buffer, then uses XCONT to chain subsequent buffers. SETXFRQ establishes the output timing, critical for audio sample rates or display refresh timing. XZERO allows inserting silence in audio streams or blanking periods in video signals without transferring Hub data.

### 5.3.3 Streamer Modes

The Streamer supports multiple operating modes, each optimized for specific data transfer patterns:

| Mode | Purpose | Typical Application |
|------|---------|---------------------|
| LUT mode | Transfer data through lookup table | Color palette mapping, gamma correction |
| NCO mode | Numerically controlled oscillator | Waveform synthesis, signal generation |
| RF mode | Radio frequency output generation | RF signal generation, modulation |
| Goertzel mode | DSP filtering during transfer | Frequency detection, tone decoding |

Mode selection appears in the XINIT instruction's mode parameter, along with configuration bits controlling data width, pin selection, and transfer direction. Each mode interprets Hub memory data differently—LUT mode uses data as lookup indices, NCO mode uses data as frequency control words, RF mode uses data as modulation patterns. Complete mode documentation, including configuration bit fields and timing parameters, appears in the P2 hardware documentation.


## 5.4 Events and Interrupts

The P2 supports event-driven programming through a comprehensive event system. Events notify code when specific conditions occur: counters reach target values, I/O pins match patterns, the Streamer completes transfers, the CORDIC finishes computations, or other COGs request attention. The P2 provides two response mechanisms: polling (checking event flags in code) and interrupts (automatic vectoring to handler code). The architecture favors polling—with 8 COGs available, dedicating one COG to event monitoring often provides better response than interrupt overhead. Interrupts remain available when needed, offering three priority levels for nested interrupt handling.

### 5.4.1 Event Sources

The P2 defines numerous event sources, each representing a distinct hardware condition:

| Event | Source | Typical Use |
|-------|--------|-------------|
| INT1, INT2, INT3 | Software-triggered interrupts | Inter-COG signaling, priority events |
| CT1, CT2, CT3 | Counter events | Periodic timing, scheduled events |
| SE1, SE2, SE3, SE4 | Selectable events | Pin edges, lock status, configurable conditions |
| PAT | Pattern match on pins | Multi-pin state detection, port monitoring |
| FBW | FIFO buffer wrapped | Hub FIFO overflow detection |
| XMT | Streamer transfer complete | DMA completion notification |
| XFI | Streamer FIFO interrupt | Buffer refill timing |
| XRO | Streamer rollover | Circular buffer management |
| XRL | Streamer read level | Data available threshold |
| ATN | Attention from another COG | Inter-COG communication |
| QMT | CORDIC operation complete | Math coprocessor completion |

Each event source sets a corresponding flag when its condition occurs. Code responds to events through wait instructions (blocking until event occurs), poll instructions (testing event flag without blocking), or interrupt configuration (automatic handler invocation).

### 5.4.2 Event Configuration

Event configuration establishes which conditions trigger events and how events invoke responses.

**Selectable Event Configuration:**

The four selectable events (SE1-SE4) can monitor various conditions:

- **SETSE1, SETSE2, SETSE3, SETSE4** - Configure selectable event sources

Each SETSE instruction selects one condition from dozens of options: pin edges (rising/falling on any pin), lock states (locked/unlocked), counter comparisons, or other hardware events. This flexibility allows tailoring event detection to application requirements.

**Interrupt Configuration:**

Interrupt setup involves two steps: configuring the interrupt source and enabling interrupt processing:

- **SETINT1, SETINT2, SETINT3** - Configure interrupt handlers (sets handler address and event source)
- **STALLI** - Enable/disable interrupt processing

Each interrupt level (1, 2, 3) has independent configuration. Level 3 can interrupt level 2; level 2 can interrupt level 1; level 1 can interrupt normal execution. This provides priority-based interrupt handling when multiple urgent events require service.

### 5.4.3 Event Waiting

Wait instructions block execution until the specified event occurs. The COG halts, consuming minimal power, until the event flag sets:

- **WAITSE1, WAITSE2, WAITSE3, WAITSE4** - Wait for selectable event
- **WAITINT** - Wait for any interrupt to occur
- **WAITCT1, WAITCT2, WAITCT3** - Wait for counter event
- **WAITATN** - Wait for attention from another COG
- **WAITPAT** - Wait for pin pattern match

Wait instructions provide deterministic event response—the next instruction executes immediately after the event occurs. This pattern works well for COGs dedicated to event handling, where blocking behavior is acceptable.

### 5.4.4 Event Polling

Poll instructions test event flags without blocking. If the event has occurred, the instruction sets condition flags; if not, execution continues immediately:

- **POLLSE1, POLLSE2, POLLSE3, POLLSE4** - Poll selectable event status
- **POLLINT** - Poll interrupt status
- **POLLCT1, POLLCT2, POLLCT3** - Poll counter event status
- **POLLATN** - Poll attention status
- **POLLPAT** - Poll pattern match status

Polling enables responsive event handling within loops. Code can check multiple events in sequence, responding to whichever occurred, without blocking on any single event. The pattern `POLLSE1 WC; IF_C JMP #handler` branches to handler code only when the event occurred.

### 5.4.5 Interrupt Philosophy

The P2's 8-COG architecture fundamentally changes interrupt philosophy. Traditional single-processor systems use interrupts because no other mechanism provides responsive event handling—the single CPU must interrupt current work to handle urgent events. The P2 offers an alternative: dedicate a COG to event monitoring. A COG waiting for events responds with zero latency when events occur, requires no context save/restore overhead, and introduces no interrupt-related bugs. The COG dedicated to event handling becomes the "interrupt handler," continuously available.

Interrupts remain valuable in specific scenarios:

- **Emergency response:** Hardware failure detection requiring immediate response across all COGs
- **Resource constraints:** When 8 COGs are fully utilized and event handling must share a COG
- **Legacy patterns:** When porting code from single-processor architectures

When interrupts are necessary, the P2's three priority levels enable nested interrupt handling. A high-priority interrupt can preempt a low-priority handler, ensuring critical events receive immediate attention even during other interrupt processing.


## 5.5 Locks and Synchronization

The P2 provides 16 hardware locks for inter-COG synchronization. When multiple COGs access shared resources—Hub memory data structures, Smart Pin configurations, or hardware peripherals—locks ensure mutual exclusion, preventing race conditions and data corruption. Hardware locks offer atomic test-and-set operations that software alone cannot provide. A COG attempting to acquire a held lock receives immediate notification rather than unknowingly accessing contested resources. The 16 locks support complex applications where multiple COGs coordinate access to numerous shared resources.

### 5.5.1 Lock Operations

Four instructions manage the complete lock lifecycle: allocation, acquisition, release, and deallocation.

| Instruction | Purpose | Condition Flag Behavior |
|-------------|---------|------------------------|
| LOCKNEW | Allocate a new lock from the pool | C=0 if lock allocated, C=1 if pool empty |
| LOCKRET | Return a lock to the pool | Lock becomes available for reallocation |
| LOCKTRY | Try to acquire a lock | C=0 if already held/failed, C=1 if now acquired |
| LOCKREL | Release a held lock | Lock becomes available for other COGs |

The allocation model prevents lock ID conflicts. LOCKNEW returns a lock ID from the pool of available locks; LOCKRET returns the lock for reuse. This ensures lock IDs remain valid—if COG A uses lock 5, no other COG receives lock 5 from LOCKNEW until COG A returns it via LOCKRET.

### 5.5.2 Lock Usage Pattern

Typical lock usage follows a four-phase pattern: allocate, acquire-use-release loop, deallocate:

```pasm
                locknew lock_id         wc      ' Allocate lock from pool
        if_c    jmp     #no_locks               ' Handle pool exhaustion

critical_section
                locktry lock_id         wc      ' Try to acquire lock
        if_nc   jmp     #critical_section       ' Retry if lock held

                ' ... exclusive access to shared resource ...
                wrlong  data, hub_addr          ' Safe: we hold the lock

                lockrel lock_id                 ' Release for other COGs

                ' ... additional work ...
                jmp     #critical_section       ' Repeat access cycle

done            lockret lock_id                 ' Return lock to pool
```

The LOCKTRY/LOCKREL pair forms the critical section boundary. Between LOCKTRY success and LOCKREL, this COG has exclusive access—all other COGs executing LOCKTRY on the same lock will fail (C=0) until LOCKREL executes. The retry loop (`if_nc jmp #critical_section`) implements busy-waiting, appropriate when lock hold times are short.

### 5.5.3 Lock Synchronization Use Cases

Locks solve multiple classes of multi-COG coordination problems:

**Shared Data Structures:**

When multiple COGs read and modify Hub memory data structures (queues, buffers, linked lists), locks prevent partial updates:

```pasm
                locktry queue_lock      wc
        if_nc   jmp     #retry
                rdlong  head, queue_head        ' Read
                add     head, #1                ' Modify
                wrlong  head, queue_head        ' Write back
                lockrel queue_lock              ' Complete atomic update
```

Without the lock, two COGs might simultaneously read the same `head` value, increment independently, and write back the same result—losing one increment.

**Hardware Resource Arbitration:**

When multiple COGs share hardware resources (specific Smart Pin, display controller, audio output), locks coordinate exclusive access:

```pasm
                locktry display_lock    wc      ' Acquire display
        if_nc   jmp     #retry
                ' ... draw graphics, write text ...
                lockrel display_lock            ' Release for other COGs
```

**Producer/Consumer Synchronization:**

Lock status serves as a signaling mechanism. A producer holds a lock while data is invalid; releasing the lock signals data ready. A consumer waits via LOCKTRY, acquiring the lock when data becomes valid.

The 16-lock limit rarely constrains applications—complex systems typically need fewer than 16 distinct critical sections. Applications requiring more synchronization points often combine locks with other mechanisms (event flags, shared memory flags) for fine-grained coordination.


## 5.6 Debug Hardware

The P2 includes built-in debugging capabilities through the DEBUG instruction and debug display system. Traditional debugging with print statements requires UART configuration, pin assignment, and format code; the P2's debug system provides formatted output with minimal code. A single DEBUG instruction outputs decimal numbers, hexadecimal values, binary patterns, strings, and graphical data to debug windows in the development environment. Debug output operates independently of application I/O—debugging a UART application doesn't interfere with the UART being debugged. Debug windows provide real-time visualization of program state, register values, pin activity, and custom graphics.

### 5.6.1 DEBUG Instruction

The DEBUG instruction combines formatting specification and data output in a single statement:

```pasm
        debug(`Counter value = `, udec(counter))    ' Decimal output
        debug(`Status = `, uhex(status))            ' Hexadecimal output
        debug(`Pins = `, ubin(ina))                 ' Binary output
```

The backtick-delimited strings contain literal text and format specifiers. Format specifiers (udec, uhex, ubin, and others) convert register values to human-readable representations. The debug system transmits this formatted data to the development environment, where it appears in debug windows or serial terminal output.

DEBUG instructions compile to executable code but can be conditionally compiled—production builds can exclude all debug code through conditional assembly, ensuring zero runtime overhead in final applications.

### 5.6.2 Debug Display Options

Debug output appears through multiple display mechanisms, depending on development environment support:

**Serial Terminal:**

The simplest debug output mode sends formatted text to a serial terminal. The development environment's serial monitor displays DEBUG output as text lines, suitable for basic value monitoring and program flow tracing. This mode works universally—any terminal program receives and displays the output.

**Graphical Debug Windows:**

When the development environment supports debug windows, DEBUG output can drive specialized displays: logic analyzer windows showing pin timing, oscilloscope windows plotting analog values, memory dump windows displaying buffer contents, and custom graphics windows for application-specific visualization. Each debug window type interprets DEBUG data according to its display purpose.

### 5.6.3 Debug Window Documentation

Debug window types, format specifiers, and configuration options vary by development environment. The DEBUG instruction supports dozens of format codes and window modes, each optimized for specific debugging tasks. Complete documentation of debug capabilities, including window types, format specifier syntax, and real-time plotting features, appears in the **P2 Debug Window Manual** (`p2-debug-window-manual`). That manual provides essential reference for effective debugging with the P2's built-in debug hardware.


## 5.7 XBYTE Bytecode Engine

The P2 includes a hardware bytecode execution engine called XBYTE that accelerates interpreted languages and virtual machines. Traditional software interpreters spend 20-40 clock cycles dispatching each bytecode—reading the bytecode, looking up a handler address, and jumping to the handler. XBYTE reduces this overhead to just 6 clock cycles through dedicated hardware that automates the fetch-lookup-dispatch cycle. This acceleration makes the P2 practical for running bytecode interpreters at speeds approaching native code performance.

### 5.7.1 XBYTE Operation

XBYTE operates by reading bytecodes from the hub FIFO and using each bytecode as an index into a lookup table stored in LUT RAM. Each LUT entry contains a routine address and optional skip pattern. The hardware automatically fetches the bytecode, retrieves the corresponding LUT entry, and dispatches to the routine using EXECF—all in 6 clock cycles plus the routine's own execution time.

The execution cycle proceeds through eight clock phases: fetch bytecode from FIFO, write bytecode to the PA register, read routine address from LUT, begin EXECF dispatch, write FIFO pointer to PB register, flush pipeline, reload pipeline, and execute the first instruction of the bytecode routine. This overlapped operation achieves the 6-cycle dispatch overhead.

When a bytecode routine completes and returns, XBYTE automatically fetches the next bytecode and repeats the cycle. The bytecode stream flows continuously from hub memory through the FIFO, enabling sustained interpretation without explicit fetching in the bytecode routines themselves.

### 5.7.2 Configuration Options

XBYTE supports multiple configuration modes that trade bytecode count against LUT space requirements:

| Mode | Bytecodes | LUT Usage | Index Calculation |
|------|-----------|-----------|-------------------|
| Full | 256 | 256 longs | bytecode[7:0] |
| Half | 128 | 128 longs | bytecode[6:0] |
| Quarter | 64 | 64 longs | bytecode[5:0] |
| Eighth | 32 | 32 longs | bytecode[4:0] |
| Sixteenth | 16 | 16 longs | bytecode[3:0] |

The full 256-bytecode mode uses the entire LUT for dispatch tables. Smaller modes leave LUT space available for other purposes—data tables, waveforms, or additional code. A compressed mode also exists that provides 16 primary bytecodes with full dispatch plus 240 extended bytecodes using a secondary lookup, balancing bytecode variety against LUT consumption.

### 5.7.3 Starting XBYTE

XBYTE mode begins through a specific instruction sequence. The SETQ instruction configures the bytecode mode and LUT base address. A RET instruction with $1FF on the hardware stack triggers XBYTE activation:

```pasm
        call    #xbyte_start            ' Push $1FF to stack
        ' ... XBYTE runs until stopped ...

xbyte_start
_RET_   setq    #%00000001              ' Configure 256 bytecodes, set flags
```

The configuration value in SETQ specifies the LUT base address, bytecode count, and whether bytecode bits should set the C and Z flags. The flags option allows bytecode routines to receive up to 4 states encoded in the flag bits, enabling compact opcode families.

### 5.7.4 XBYTE Applications

XBYTE enables efficient implementation of virtual machines and interpreters. Java bytecode interpreters, Forth threaded code systems, BASIC interpreters, and custom scripting languages all benefit from the reduced dispatch overhead. At 160 MHz, XBYTE can dispatch over 26 million bytecodes per second (considering only dispatch overhead), making interpreted languages practical for real-time applications.

Bytecode routines reside in COG or LUT RAM and must end with RET or _RET_ to return control to the XBYTE engine. The PA register ($1F6) contains the current bytecode value, available as an operand within routines. The PB register ($1F7) contains the FIFO read pointer, enabling routines to track their position in the bytecode stream or read inline parameters following the bytecode.

Complete XBYTE programming details, including LUT table construction, skip pattern usage, and advanced dispatch techniques, appear in specialized virtual machine documentation.


```{=latex}
\begin{keyconcepts}
\item The CORDIC coprocessor provides 54-cycle hardware math (multiply, divide, sqrt, trig)
\item Smart Pins are 64 programmable I/O peripherals with local state machines
\item The Streamer enables DMA-like high-speed data movement
\item Events provide non-interrupt notification; interrupts are available when needed
\item 16 hardware locks enable safe inter-COG synchronization
\item DEBUG instruction provides built-in debugging output
\item XBYTE provides 6-cycle bytecode dispatch for interpreters and virtual machines
\item The 8-COG architecture often eliminates the need for interrupts
\item Each subsystem is controlled through dedicated PASM2 instructions
\end{keyconcepts}
```


<!-- End of Chapter 5 -->


# Part II: Instruction Set Reference

# Instructions: A

This section contains all PASM2 instructions beginning with the letter A.



## ABS {#abs}

Absolute
[Math and Logic](#math-and-logic) - Get the absolute value of a number.

**ABS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**ABS**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Absolute Src (or Dest) value is stored in Dest.

- Dest is the register in which to write the absolute value of Dest or Src.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose absolute value is written to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0110010 | CZI | DDDDDDDDD | SSSSSSSSS | D | S[31] | Result = 0 | 2 |
| EEEE | 0110010 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | D[31] | Result = 0 | 2 |


**Related:** [NEG](#neg)

**Explanation:**

ABS determines the absolute value of Src or Dest and writes the result into Dest. The first syntax form computes the absolute value of Src, while the second syntax form (without Src) computes the absolute value of Dest itself.

If the WC or WCZ effect is specified, the C flag is set (1) if the original Src or Dest value was negative (the sign bit was 1), or is cleared (0) if it was positive. This preserves information about the original sign of the value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

Literal Src values are zero-extended, so ABS is best used with register Src (or augmented Src) values for meaningful signed operations.



## ADD {#add}

Add
[Math and Logic](#math-and-logic) - Add two unsigned values.

**ADD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Sum of unsigned Src and unsigned Dest is stored in Dest.

- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001000 | CZI | DDDDDDDDD | SSSSSSSSS | D | carry of (D + S) | Result = 0 | 2 |


**Related:** [ADDX](#addx), [ADDS](#adds), [ADDSX](#addsx), [SUB](#sub)

**Explanation:**

ADD sums the two unsigned values of Dest and Src together and stores the result into the Dest register.

If the WC or WCZ effect is specified, the C flag is set (1) if the summation results in a 32-bit overflow (unsigned carry), or is cleared (0) if no overflow. This indicates that the result exceeded the maximum unsigned 32-bit value of $FFFF_FFFF.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result of Dest + Src equals zero, or is cleared (0) if it is non-zero.

To add unsigned multi-long values (64-bit or larger), use ADD for the least significant long, then ADDX for each subsequent long. ADDX carries the overflow from the previous addition into the current one. For example, to add two 64-bit values:

```pasm
        add     value_lo, addend_lo  wc    ' Add low longs, capture carry
        addx    value_hi, addend_hi        ' Add high longs with carry-in
```

ADD and ADDX are also used for adding signed multi-long values, with ADDSX ending the sequence to properly handle sign extension.



## ADDCT1 / ADDCT2 / ADDCT3 {#addct1}

Add and set counter event trigger (1, 2, or 3)
[Event](#event) - Set CTn counter event trigger time.

**ADDCT1**  *Dest, {#}Src*
**ADDCT2**  *Dest, {#}Src*
**ADDCT3**  *Dest, {#}Src*

---

**Result:** The Src value is added into Dest and the result is also stored in the hidden CTn event trigger register.

- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010011 | 00I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1010011 | 01I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1010011 | 10I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [POLLCT1/2/3](#pollct1), [WAITCT1/2/3](#waitct1), [JCT1/2/3](#jct1), [JNCT1/2/3](#jnct1)

**Explanation:**

ADDCT1, ADDCT2, and ADDCT3 set their respective hidden counter event trigger registers to the value of Dest + Src. The result is also written to Dest. These instructions are used to schedule time-based events that will trigger when the System Counter (CT) reaches the specified value.

The P2 provides three independent counter event triggers (CT1, CT2, CT3), allowing a cog to manage multiple simultaneous time-based operations. Use the corresponding POLLCTn, WAITCTn, JCTn, and JNCTn instructions to process each counter's time-based events. This enables precise timing control for periodic operations, delays, and synchronized activities.



## ADDPIX {#addpix}

Add pixels
[Pixel Mixer](#pixel-mixer) - Add RGB colors with full saturation.

**ADDPIX**  *Dest, {#}Src*

---

**Result:** Src color value bytes are added into Dest color value bytes with full saturation.

- Dest is a register containing the RGB color value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose RGB color value bytes are added into Dest.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010010 | 00I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 7 |


**Related:** [SUBPIX](#subpix), [MULPIX](#mulpix), [BLNPIX](#blnpix)

**Explanation:**

ADDPIX sums individual RGB (red, green, blue) color values of Src into that of Dest and stores the result in the Dest register. Each byte is treated as a separate color channel and is saturated to prevent wraparound.

Saturation means that if the sum of a color channel exceeds 255, the result is clamped to 255 rather than wrapping around to a low value. This prevents color distortion when combining bright colors and produces visually correct results for color blending operations.

The instruction processes all three color channels (and alpha if present) in parallel, completing in 7 clock cycles.



## ADDS {#adds}

Add signed
[Math and Logic](#math-and-logic) - Add two signed values.

**ADDS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Sum of signed Src and signed Dest is stored in Dest.

- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001010 | CZI | DDDDDDDDD | SSSSSSSSS | D | sign of (D + S) | Result = 0 | 2 |


**Related:** [ADD](#add), [ADDX](#addx), [ADDSX](#addsx), [SUBS](#subs)

**Explanation:**

ADDS sums the two signed values of Dest and Src together and stores the result into the Dest register.

If Src is a 9-bit literal, its value is interpreted as positive (0-511; it is not sign-extended). Use ##Value (or insert a prior AUGS instruction) for a 32-bit signed value, negative or positive.

If the WC or WCZ effect is specified, the C flag is set (1) if the summation results in a signed overflow (signed carry), or is cleared (0) if no overflow. Signed overflow occurs when the result cannot be represented in 32 bits using two's complement notation.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result of Dest + Src is zero, or is cleared (0) if it is non-zero.

To add signed multi-long values, use ADD (not ADDS) followed possibly by ADDX, and finally ADDSX as the last operation to properly handle sign extension.



## ADDSX {#addsx}

Add signed, extended
[Math and Logic](#math-and-logic) - Add two signed extended values.

**ADDSX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Sum of signed Src plus C and signed Dest is stored in Dest.

- Dest is a register containing the value to add Src plus C to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001011 | CZI | DDDDDDDDD | SSSSSSSSS | D | sign of (D+S+C) | Z AND (Result = 0) | 2 |


**Related:** [ADD](#add), [ADDX](#addx), [ADDS](#adds), [SUBSX](#subsx)

**Explanation:**

ADDSX sums the signed values of Dest and Src plus C together and stores the result into the Dest register. The ADDSX instruction is used to perform signed multi-long (extended) addition, such as 64-bit addition.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative (Result[31] = 1), or is cleared (0) if positive. Use WC or WCZ on preceding ADD and ADDX instructions for proper final C flag state.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Z was previously set and the result of Dest + Src + C is zero, or it is cleared (0) if non-zero. Use WZ or WCZ on preceding ADD and ADDX instructions for proper final Z flag state. This allows detection of a zero result across the entire multi-long value.

To add signed multi-long values, use ADD (not ADDS) followed possibly by ADDX, and finally ADDSX as the last operation. ADDSX properly handles the sign extension for the most significant portion of the multi-long value.



## ADDX {#addx}

Add extended
[Math and Logic](#math-and-logic) - Add two unsigned extended values.

**ADDX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Sum of unsigned Src plus C and unsigned Dest is stored in Dest.

- Dest is a register containing the value to add Src plus C to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001001 | CZI | DDDDDDDDD | SSSSSSSSS | D | carry of (D + S + C) | Z AND (Result = 0) | 2 |


**Related:** [ADD](#add), [ADDS](#adds), [ADDSX](#addsx), [SUBX](#subx)

**Explanation:**

ADDX sums the unsigned values of Dest and Src plus C together and stores the result into the Dest register. The ADDX instruction is used to perform unsigned multi-long (extended) addition, such as 64-bit addition.

If the WC or WCZ effect is specified, the C flag is set (1) if the summation resulted in an unsigned carry, or is cleared (0) if no carry. Use WC or WCZ on preceding ADD and ADDX instructions for proper final C flag state. If C is set after the last ADDX in a multi-long addition, it indicates unsigned overflow.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Z was previously set and the result of Dest + Src + C is zero, or it is cleared (0) if non-zero. Use WZ or WCZ on preceding ADD and ADDX instructions for proper final Z flag state. This allows detection of a zero result across the entire multi-long value.

To add unsigned multi-long values, use ADD followed by one or more ADDX instructions. Each ADDX carries the overflow from the previous addition into the current one.



## AKPIN {#akpin}

Acknowledge pin
[Smart Pin](#smart-pin) - Acknowledge smart pin(s).

**AKPIN**  *{#}Src*

---

**Result:** One or more Smart Pins is acknowledged; lowering their corresponding IN signal(s).

- Src is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the Smart Pin(s) to acknowledge.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100000 | 01I | 000000001 | SSSSSSSSS | Ack Bus | --- | --- | 2 |


**Related:** [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin), [RDPIN](#rdpin)

**Explanation:**

AKPIN acknowledges the Smart Pin(s) designated by Src. This lowers the corresponding IN signal(s) so that future Smart Pin events may raise them again later.

Src[5:0] indicates the pin number (0-63). For a range of Smart Pins, Src[5:0] indicates the first pin number (0-63) and Src[10:6] indicates how many contiguous pins beyond the first should be affected (1-31).

A 9-bit literal Src is enough to express the starting pin (Src[5:0]) and a range of up to 8 contiguous pins (Src[8:6]). If needed, use the augmented literal feature (##Src) to augment Src to the required 11-bit literal value, which automatically inserts an AUGS instruction prior.

When Src is a register, the register's value bits [10:0] are used as-is to form the 11-bit Smart Pin range, unless a SETQ instruction immediately precedes the AKPIN instruction; in that case, SETQ's Dest[4:0] substitutes for value bits[10:6] for AKPIN's use.

The range calculation (from Src[5:0] up to Src[5:0]+Src[10:6]) wraps within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.



## ALLOWI {#allowi}

Allow interrupts
[Interrupt](#interrupt) - Allow interrupts.

```
ALLOWI
```

**Result:** Any stalled and future interrupts are allowed.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | 000100000 | 000100100 | --- | --- | --- | 2 |


**Related:** [STALLI](#stalli)

**Explanation:**

ALLOWI re-enables interrupt branching; the default on COG start. ALLOWI is the complement of the STALLI instruction. Both are used to protect short, vital sections of main code from timing jitter or state loss caused by asynchronous interrupt handling.

When ALLOWI is executed, any interrupts that were stalled by a previous STALLI instruction are allowed to proceed, and future interrupts are also enabled. This allows the COG to respond to interrupt events normally.



## ALTB {#altb}

Alter bit
[Register Indirection](#register-indirection) - Alter subsequent BITxxx instruction.

**ALTB**  *Dest, {#}Src*
**ALTB**  *Dest*

---

**Result:** The next instruction's pipelined Dest value is altered to be (Src + Dest[13:5]) & $1FF, or just Dest[13:5] for syntax 2.

- Dest is the register whose 14-bit value is the index, or the full bit address, for the BITxxx instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[13:5]) for BITxxx) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001100 | 11I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001100 | 111 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTD](#altd), [ALTS](#alts), [ALTR](#altr), [ALTI](#alti)

**Explanation:**

ALTB should be followed by a BITxxx instruction. It modifies the BITxxx instruction's Dest value, enabling code to iterate through multiple bits of data across a range of register RAM.

BITxxx's Dest value is changed to (Src + Dest[13:5]) & $1FF (for syntax 1), or to Dest[13:5] (for syntax 2). Dest[13:5] corresponds to the target long register's 9-bit address and Dest[4:0] is the bit ID within it; values of 0-31 identify individual bits, by position, in least-significant bit order.

Iteratively executing ALTB followed by a BITxxx instruction, and each time incrementing ALTB's 14-bit Dest value by one, effectively writes a stream of bit values to register RAM as if it were all made of bit-sized registers.

Warning: BITxxx instructions optionally operate on a range of bits, encoded in the Src value. They don't limit themselves to only reading Src[4:0] for the bit number. For this reason, care must be taken when using ALTB with BITxxx or the index value (often used for the Src of the altered instruction) will be misinterpreted as multiple bits to affect. One way to solve this is to use a SETQ #0 followed by the ALTB then BITxxx instructions to force BITxxx's Src[9:5] bits to 0; that is, no extra bits beyond the single bit described by Src[4:0].

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of bits begins. ALTB adds the long index (Dest[13:5]) to the base (Src[8:0]) to locate the register holding the target bit. The bit ID (Dest[4:0]) identifies the bit's position within that long register. At the end of ALTB execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 14-bit index (Dest) for a future ALTB+BITxxx iteration.

In syntax 2, Dest serves as the full bit address. It is the same format as in syntax 1, but represents the target long's absolute address and its bit index instead of the long's relative index (to add to a base) and bit index.

The instruction following ALTB is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTD {#altd}

Alter destination
[Register Indirection](#register-indirection) - Alter D field of next instruction.

**ALTD**  *Dest, {#}Src*
**ALTD**  *Dest*

---

**Result:** The next instruction's pipelined Dest value is altered to be (Src + Dest) & $1FF, or just Dest[8:0] in syntax 2.

- Dest is the register whose 9-bit value is the offset, or the full value, for the next instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base (Src[8:0]; added to offset (Dest) for the next instruction) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001100 | 01I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001100 | 011 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTS](#alts), [ALTR](#altr), [ALTB](#altb), [ALTI](#alti)

**Explanation:**

ALTD modifies the next instruction's Dest value to be (Src + Dest) & $1FF (for syntax 1), or to Dest[8:0] (for syntax 2).

In syntax 1, Src consists of two 9-bit fields: a base value (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base represents a starting point. ALTD adds the offset (Dest[8:0]) to the base (Src[8:0]) to determine the next instruction's Dest value. At the end of ALTD execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the offset (Dest) for a future ALTD+instruction iteration.

In syntax 2, Dest serves as the full value. It is used as-is for the next instruction's substitute Dest value.

The instruction following ALTD is shielded from interrupt. ALTD alters the next instruction regardless of its kind. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTGB {#altgb}

Alter get byte
[Register Indirection](#register-indirection) - Alter subsequent GETBYTE / ROLBYTE instruction.

**ALTGB**  *Dest, {#}Src*
**ALTGB**  *Dest*

---

**Result:** The next instruction's pipelined Src and Num fields are altered to be (Src + Dest[10:2]) & $1FF, or just Dest[10:2] for syntax 2, and Dest[1:0], respectively.

- Dest is the register whose 11-bit value is the index, or the full byte address, for the GETBYTE / ROLBYTE instruction to read.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[10:2]) for GETBYTE / ROLBYTE) and also an optional auto-indexer value (Src[17:9]; added to Dest at end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001011 | 01I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001011 | 011 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTGN](#altgn), [ALTGW](#altgw), [ALTSB](#altsb), [GETBYTE](#getbyte), [ROLBYTE](#rolbyte)

**Explanation:**

ALTGB should be followed by GETBYTE or ROLBYTE. It modifies the GETBYTE / ROLBYTE instruction's Src and Num values, enabling code to iterate through multiple bytes of data across a range of register RAM.

GETBYTE / ROLBYTE's Src value is changed to (Src + Dest[10:2]) & $1FF (for syntax 1), or to Dest[10:2] (for syntax 2), and its Num value is changed to Dest[1:0]. Dest[10:2] corresponds to the target long register's 9-bit address and Dest[1:0] is the byte ID within it; values of 0-3 identify individual bytes, by position, in least-significant byte order.

Iteratively executing ALTGB followed by GETBYTE or ROLBYTE, and each time incrementing ALTGB's 11-bit Dest value by one, effectively reads a stream of byte values from register RAM as if it were all made of byte-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of bytes begins. ALTGB adds the long index (Dest[10:2]) to the base (Src[8:0]) to locate the register holding the target byte. The byte ID (Dest[1:0]) identifies the byte's position within that long register. At the end of ALTGB execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 11-bit index (Dest) for a future ALTGB+GETBYTE or ROLBYTE iteration.

In syntax 2, Dest serves as the full byte address. It is the same format as in syntax 1, but represents the target long's absolute address and its byte index instead of the long's relative index (to add to a base) and byte index.

The instruction following ALTGB is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTGN {#altgn}

Alter get nibble
[Register Indirection](#register-indirection) - Alter subsequent GETNIB / ROLNIB instruction.

**ALTGN**  *Dest, {#}Src*
**ALTGN**  *Dest*

---

**Result:** The next instruction's pipelined Src and Num values are altered to be (Src + Dest[11:3]) & $1FF, or just Dest[11:3] for syntax 2, and Dest[2:0], respectively.

- Dest is the register whose 12-bit value is the index, or the full nibble address, for the next GETNIB / ROLNIB instruction to read.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[11:3]) for GETNIB / ROLNIB) and also an optional auto-indexer value (Src[17:9]; added to Dest at end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001010 | 11I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001010 | 111 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTGB](#altgb), [ALTGW](#altgw), [ALTSN](#altsn), [GETNIB](#getnib), [ROLNIB](#rolnib)

**Explanation:**

ALTGN should be followed by GETNIB or ROLNIB. It modifies the GETNIB / ROLNIB instruction's Src and Num values, enabling code to iterate through multiple nibbles of data across a range of register RAM.

GETNIB / ROLNIB's Src value is changed to (Src + Dest[11:3]) & $1FF (for syntax 1), or to Dest[11:3] (for syntax 2), and its Num value is changed to Dest[2:0]. Dest[11:3] corresponds to the target long register's 9-bit address and Dest[2:0] is the nibble ID within it; values of 0-7 identify individual nibbles, by position, in least-significant nibble order.

Iteratively executing ALTGN followed by GETNIB or ROLNIB, and each time incrementing ALTGN's 12-bit Dest value by one, effectively reads a stream of nibble values from register RAM as if it were all made of nibble-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of nibbles begins. ALTGN adds the long index (Dest[11:3]) to the base (Src[8:0]) to locate the register holding the target nibble. The nibble ID (Dest[2:0]) identifies the nibble's position within that long register. At the end of ALTGN execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 12-bit index (Dest) for a future ALTGN+GETNIB or ROLNIB iteration.

In syntax 2, Dest serves as the full nibble address. It is the same format as in syntax 1, but represents the target long's absolute address and its nibble index instead of the long's relative index (to add to a base) and nibble index.

The instruction following ALTGN is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTGW {#altgw}

Alter get word
[Register Indirection](#register-indirection) - Alter subsequent GETWORD / ROLWORD instruction.

**ALTGW**  *Dest, {#}Src*
**ALTGW**  *Dest*

---

**Result:** The next instruction's pipelined Src and Num fields are altered to be (Src + Dest[9:1]) & $1FF, or just Dest[9:1] for syntax 2, and Dest[0], respectively.

- Dest is the register whose 10-bit value is the index, or the full word address for the GETWORD / ROLWORD instruction to read.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[9:1]) for GETWORD / ROLWORD) and also an optional auto-indexer value (Src[17:9]; added to Dest at end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001011 | 11I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001011 | 111 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTGB](#altgb), [ALTGN](#altgn), [ALTSW](#altsw), [GETWORD](#getword), [ROLWORD](#rolword)

**Explanation:**

ALTGW should be followed by GETWORD or ROLWORD. It modifies the GETWORD / ROLWORD instruction's Src and Num values, enabling code to iterate through multiple words of data across a range of register RAM.

GETWORD / ROLWORD's Src value is changed to (Src + Dest[9:1]) & $1FF (for syntax 1), or to Dest[9:1] (for syntax 2), and its Num value is changed to Dest[0]. Dest[9:1] corresponds to the target long register's 9-bit address and Dest[0] is the word ID within it; values of 0-1 identify individual words, by position, in least-significant word order.

Iteratively executing ALTGW followed by GETWORD or ROLWORD, and each time incrementing ALTGW's 10-bit Dest value by one, effectively reads a stream of word values from register RAM as if it were all made of word-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of words begins. ALTGW adds the long index (Dest[9:1]) to the base (Src[8:0]) to locate the register holding the target word. The word ID (Dest[0]) identifies the word's position within that long register. At the end of ALTGW execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 10-bit index (Dest) for a future ALTGW+GETWORD or ROLWORD iteration.

In syntax 2, Dest serves as the full word address. It is the same format as in syntax 1, but represents the target long's absolute address and its word index instead of the long's relative index (to add to a base) and word index.

The instruction following ALTGW is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTI {#alti}

Alter instruction
[Register Indirection](#register-indirection) - Substitute next instruction's field values from template, per configuration.

**ALTI**  *Dest, {#}Src*
**ALTI**  *Dest*

---

**Result:** The next instruction's pipelined field values are substituted from the Dest template, and Dest is modified per Src configuration.

- Dest is the register whose value contains one or more of the next instruction's field substitutes or an entire 32-bit opcode for full substitution.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value describes the substitutions and Dest modifications to perform.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001101 | 00I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001101 | 001 | DDDDDDDDD | 101100100 | --- | --- | --- | 2 |


**Related:** [SETD](#setd), [SETS](#sets), [SETR](#setr), [ALTD](#altd), [ALTS](#alts), [ALTR](#altr)

**Explanation:**

ALTI substitutes fields from Dest for one or more of the next instruction's pipelined Dest, Src, Result, Instr, FX, and/or Cond values, and ALTI's Dest is then modified per Src configuration (syntax 1), or the entire Dest opcode (instruction) is executed in place of the next instruction (syntax 2).

The Dest register contains the ALTI template; a 32-bit value with format similar to an opcode with Condition (31:28), Result (27:19), Indirect I (18), Dest D (17:9), and Source S (8:0) fields.

In syntax 1, Src consists of six 3-bit fields (%rrr_ddd_sss_RRR_DDD_SSS) that describe field substitution and Dest modification. The mask size fields (%rrr, %ddd, %sss) control increment/decrement masking from unlimited 9-bit (000) to 2-bit (111). The control fields (%RRR, %DDD, %SSS) control field substitution and adjustment.

In syntax 2, Dest serves as the full opcode value. It is executed as-is in place of the next instruction and Dest remains unaltered afterward.

The instruction following ALTI is shielded from interrupt. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTR {#altr}

Alter result
[Register Indirection](#register-indirection) - Alter Result register address of next instruction.

**ALTR**  *Dest, {#}Src*
**ALTR**  *Dest*

---

**Result:** The next instruction's pipelined Result address (Dest address by default) is altered to be (Src + Dest) & $1FF, or just Dest[8:0] in syntax 2.

- Dest is the register whose 9-bit value is the offset, or the full value, for the next instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base (Src[8:0]; added to offset (Dest) for the next instruction) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001100 | 00I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001100 | 001 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTD](#altd), [ALTS](#alts), [ALTB](#altb), [ALTI](#alti)

**Explanation:**

ALTR modifies the next instruction's Result address to be (Src + Dest) & $1FF (for syntax 1), or to Dest[8:0] (for syntax 2).

The Result address is the Dest address by default. It identifies where the result value from the instruction's execution is written at the end of execution. During execution, the pipeline holds an instruction's Dest address and the Result address as two separate entities, normally set to the same location. ALTR causes the next instruction's Result to redirect to a different address; changing an instruction from a destructive (operand overwriting) operation to a non-destructive (operand preserving) operation.

In syntax 1, Src consists of two 9-bit fields: a base value (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base represents a starting point. ALTR adds the offset (Dest[8:0]) to the base (Src[8:0]) to determine the next instruction's Result address. At the end of ALTR execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the offset (Dest) for a future ALTR+instruction iteration.

In syntax 2, Dest serves as the full value. It is used as-is for the next instruction's substitute Result address.

The instruction following ALTR is shielded from interrupt. ALTR alters the next instruction regardless of its kind. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTS {#alts}

Alter source
[Register Indirection](#register-indirection) - Alter S field of next instruction.

**ALTS**  *Dest, {#}Src*
**ALTS**  *Dest*

---

**Result:** The next instruction's pipelined Src value is altered to be (Src + Dest) & $1FF, or just Dest[8:0] in syntax 2.

- Dest is the register whose 9-bit value is the offset, or the full value, for the next instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base (Src[8:0]; added to offset (Dest) for the next instruction) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001100 | 10I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001100 | 101 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTD](#altd), [ALTR](#altr), [ALTB](#altb), [ALTI](#alti)

**Explanation:**

ALTS modifies the next instruction's Src value to be (Src + Dest) & $1FF (for syntax 1), or to Dest[8:0] (for syntax 2).

In syntax 1, Src consists of two 9-bit fields: a base value (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base represents a starting point. ALTS adds the offset (Dest[8:0]) to the base (Src[8:0]) to determine the next instruction's Src value. At the end of ALTS execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the offset (Dest) for a future ALTS+instruction iteration.

In syntax 2, Dest serves as the full value. It is used as-is for the next instruction's substitute Src value.

The instruction following ALTS is shielded from interrupt. ALTS alters the next instruction regardless of its kind. Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTSB {#altsb}

Alter set byte
[Register Indirection](#register-indirection) - Alter subsequent SETBYTE instruction.

**ALTSB**  *Dest, {#}Src*
**ALTSB**  *Dest*

---

**Result:** The next instruction's pipelined Dest and Num values are altered to be (Src + Dest[10:2]) & $1FF (syntax 1), or just Dest[10:2] (syntax 2), and Num is set to Dest[1:0]. Dest is post-adjusted by auto-indexer.

- Dest is the register whose 11-bit value is the index (Dest[10:2] = long address, Dest[1:0] = byte ID) or the full byte address for SETBYTE to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal containing base long address (Src[8:0]) and optional auto-indexer value (Src[17:9]).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001011 | 00I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001011 | 001 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTGB](#altgb), [ALTSN](#altsn), [ALTSW](#altsw), [SETBYTE](#setbyte)

**Explanation:**

ALTSB should be followed by SETBYTE. It modifies the SETBYTE instruction's Dest and Num values, enabling code to iterate through multiple bytes across register RAM.

SETBYTE's Dest is changed to (Src + Dest[10:2]) & $1FF (syntax 1), or to Dest[10:2] (syntax 2), and its Num value is changed to Dest[1:0]. Dest[10:2] is the target long register's 9-bit address; Dest[1:0] is the byte ID (0-3) within it.

Iteratively executing ALTSB followed by SETBYTE while incrementing the 11-bit Dest value writes a stream of bytes to register RAM as if it were byte-sized registers.

In syntax 1, Src contains a base address (Src[8:0]) and signed auto-indexer (Src[17:9]). In syntax 2, Dest serves as the full byte address.

The instruction following ALTSB is shielded from interrupt. ALTSB alters the next instruction regardless of its kind (intended for SETBYTE). Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTSN {#altsn}

Alter set nibble
[Register Indirection](#register-indirection) - Alter subsequent SETNIB instruction.

**ALTSN**  *Dest, {#}Src*
**ALTSN**  *Dest*

---

**Result:** The next instruction's pipelined Dest and Num values are altered to be (Src + Dest[11:3]) & $1FF, or just Dest[11:3] for syntax 2, and Dest[2:0], respectively.

- Dest is the register whose 12-bit value is the index, or the full nibble address, for the SETNIB instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[11:3]) for SETNIB) and also an optional auto-indexer value (Src[17:9]; added to Dest at the end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001010 | 10I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001010 | 101 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTGN](#altgn), [ALTSB](#altsb), [ALTSW](#altsw), [SETNIB](#setnib)

**Explanation:**

ALTSN should be followed by SETNIB. It modifies the SETNIB instruction's Dest and Num values, enabling code to iterate through multiple nibbles of data across a range of register RAM.

SETNIB's Dest value is changed to (Src + Dest[11:3]) & $1FF (for syntax 1), or to Dest[11:3] (for syntax 2), and its Num value is changed to Dest[2:0]. Dest[11:3] corresponds to the target long register's 9-bit address and Dest[2:0] is the nibble ID within it; values of 0-7 identify individual nibbles, by position, in least-significant nibble order.

Iteratively executing ALTSN followed by SETNIB, and each time incrementing ALTSN's 12-bit Dest value by one, effectively writes a stream of nibble values to register RAM as if it were all made of nibble-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of nibbles begins. ALTSN adds the long index (Dest[11:3]) to the base (Src[8:0]) to locate the register holding the target nibble. The nibble ID (Dest[2:0]) identifies the nibble's position within that long register. At the end of ALTSN execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 12-bit index (Dest) for a future ALTSN+SETNIB iteration.

In syntax 2, Dest serves as the full nibble address. It is the same format as in syntax 1, but represents the target long's absolute address and its nibble index instead of the long's relative index (to add to a base) and nibble index.

The instruction following ALTSN is shielded from interrupt. ALTSN alters the next instruction regardless of its kind (intended for SETNIB). Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## ALTSW {#altsw}

Alter set word
[Register Indirection](#register-indirection) - Alter subsequent SETWORD instruction.

**ALTSW**  *Dest, {#}Src*
**ALTSW**  *Dest*

---

**Result:** The next instruction's pipelined Dest and Num fields are altered to be (Src + Dest[9:1]) & $1FF, or just Dest[9:1] for syntax 2, and Dest[0], respectively.

- Dest is the register whose 10-bit value is the index, or the full word address, for the SETWORD instruction to operate on.
- Src is an optional register, 9-bit literal, or 18-bit augmented literal whose value contains a base long address (Src[8:0]; added to index (Dest[9:1]) for SETWORD) and also an optional auto-indexer value (Src[17:9]; added to Dest at end of execution).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001011 | 10I | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | --- | --- | 2 |
| EEEE | 1001011 | 101 | DDDDDDDDD | 000000000 | D\textsuperscript{1} | --- | --- | 2 |

```{=latex}
\textsuperscript{1} Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. In syntax 2, the auto-indexer value is 0.
```


**Related:** [ALTGW](#altgw), [ALTSB](#altsb), [ALTSN](#altsn), [SETWORD](#setword)

**Explanation:**

ALTSW should be followed by SETWORD. It modifies the SETWORD instruction's Dest and Num values, enabling code to iterate through multiple words of data across a range of register RAM.

SETWORD's Dest value is changed to (Src + Dest[9:1]) & $1FF (for syntax 1), or to Dest[9:1] (for syntax 2), and its Num value is changed to Dest[0]. Dest[9:1] corresponds to the target long register's 9-bit address and Dest[0] is the word ID within it; values of 0-1 identify individual words, by position, in least-significant word order.

Iteratively executing ALTSW followed by SETWORD, and each time incrementing ALTSW's 10-bit Dest value by one, effectively writes a stream of word values to register RAM as if it were all made of word-sized registers.

In syntax 1, Src consists of two 9-bit fields: a base address (Src[8:0]) and a signed auto-indexer (Src[17:9]). The base is the register RAM address where the series of words begins. ALTSW adds the long index (Dest[9:1]) to the base (Src[8:0]) to locate the register holding the target word. The word ID (Dest[0]) identifies the word's position within that long register. At the end of ALTSW execution, the optional auto-indexer value (usually 0, 1, or -1) is added to the 10-bit index (Dest) for a future ALTSW+SETWORD iteration.

In syntax 2, Dest serves as the full word address. It is the same format as in syntax 1, but represents the target long's absolute address and its word index instead of the long's relative index (to add to a base) and word index.

The instruction following ALTSW is shielded from interrupt. ALTSW alters the next instruction regardless of its kind (intended for SETWORD). Field value modification occurs in the instruction pipeline only; code is not altered, values do not persist. SETQ/SETQ2 does not affect ALTx instructions; the Q value passes through to the next instruction.



## AND {#and}

Bitwise AND
[Math and Logic](#math-and-logic) - Bitwise AND a value with another, or with the NOT of another.

**AND**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Bitwise AND of Dest and Src is stored in Dest.

- Dest is the register containing the value to bitwise AND with Src and is the destination in which to write the result.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value will be bitwise ANDed with Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0101000 | CZI | DDDDDDDDD | SSSSSSSSS | D | parity of result | Result = 0 | 2 |


**Related:** [ANDN](#andn), [OR](#or), [XOR](#xor), [TEST](#test)

**Explanation:**

AND performs a bitwise AND of the value in Src into that of Dest, storing the result in Dest. Each bit in the result is 1 only if the corresponding bits in both Dest and Src are 1.

If the WC or WCZ effect is specified, the C flag is set (1) if the result contains an odd number of high (1) bits, or is cleared (0) if it contains an even number of high bits. This parity calculation is useful for error detection.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.



## ANDN {#andn}

And not
[Math and Logic](#math-and-logic) - Bitwise AND a value with the NOT of another.

**ANDN**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Bitwise AND of Dest with inverse of Src is stored in Dest.

- Dest is the register containing the value to bitwise AND with the inverse of Src and is the destination in which to write the result.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose inverse value will be bitwise ANDed with Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0101001 | CZI | DDDDDDDDD | SSSSSSSSS | D | parity of result | Result = 0 | 2 |


**Related:** [AND](#and), [OR](#or), [XOR](#xor), [TEST](#test)

**Explanation:**

ANDN performs a bitwise AND of Dest with the inverse of Src (!Src), storing the result in Dest. This effectively clears bits in Dest wherever the corresponding bits in Src are set.

ANDN is particularly useful for clearing specific bits while leaving others unchanged. For example, to clear bits 7:4 of a register while preserving all other bits, use ANDN with a mask that has 1s in positions 7:4.

If the WC or WCZ effect is specified, the C flag is set (1) if the result contains an odd number of high (1) bits, or is cleared (0) if it contains an even number of high bits.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.



## ASMCLK {#asmclk}

Assembly clock instruction
[System Control](#system-control) - Assembly clock instruction.

```
ASMCLK
```

**Result:** Controls assembly-time clock operations.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000000 | 000 | 000000000 | 000000000 | --- | --- | --- | 2 |


**Related:** [GETCT](instructions-g.md#getct), [POLLCT1/2/3](instructions-p.md#pollct1)

**Explanation:**

ASMCLK controls assembly-time clock operations. This instruction is used during the assembly process to manage timing-related assembly directives.



## AUGD {#augd}

Augment destination
[Miscellaneous](#miscellaneous) - Augment next literal Dest to 32-bits.

**AUGD**  *#Dest*

---

**Result:** The 23-bit value formed from Dest is queued to prefix the next literal Dest occurrence (#Dest) to form a 32-bit literal for that instruction; interrupts are also temporarily disabled.

- Dest is a 32-bit literal whose upper 23 bits are prepended to the next literal Dest occurrence.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 11111DD | DDD | DDDDDDDDD | DDDDDDDDD | Hidden D Queue | --- | --- | 2 |


**Related:** [AUGS](#augs)

**Explanation:**

AUGD is an assistant instruction to aid with literal values that exceed 9 bits. Most PASM2 instructions have 9 bits available for literal Dest values; enough for many uses, but not all. AUGD augments the next occurrence of a literal Dest value to be a full 32-bits.

When the instruction with the soon-to-be-augmented literal is later executed, the COG uses the lower 9 bits encoded in the instruction's Dest field and prepends AUGD's 23 bits to it.

All instructions following AUGD are shielded from interrupt until after the instruction with the newly-augmented literal Dest value is executed. Dest value augmentation occurs in the instruction pipeline only; code is not altered, value does not persist. SETQ/SETQ2 does not affect AUGD; the Q value passes through to the next instruction.

Though AUGD may be manually entered wherever needed, the Parallax P2 compiler supports a convenient way to use this feature. In the target instruction's Dest field, use "##" followed by the desired 32-bit literal (instead of "#" followed by a 9-bit literal); the compiler will automatically invoke AUGD immediately before. When counting clock cycles, make sure to account for 2 extra clock cycles for instructions containing ## augmented literals.



## AUGS {#augs}

Augment source
[Miscellaneous](#miscellaneous) - Augment next literal Src to 32-bits.

**AUGS**  *#Src*

---

**Result:** The 23-bit value formed from Src is queued to prefix the next literal Src occurrence (#Src) to form a 32-bit literal for that instruction; interrupts are also temporarily disabled.

- Src is a 32-bit literal whose upper 23 bits are prepended to the next literal Src occurrence.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 11110SS | SSS | SSSSSSSSS | SSSSSSSSS | Hidden S Queue | --- | --- | 2 |


**Related:** [AUGD](#augd)

**Explanation:**

AUGS is an assistant instruction to aid with literal values that exceed 9 bits. Most PASM2 instructions have 9 bits available for literal Src values; enough for many uses, but not all. AUGS augments the next occurrence of a literal Src value to be a full 32-bits.

When the instruction with the soon-to-be-augmented literal is later executed, the COG uses the lower 9 bits encoded in the instruction's Src field and prepends AUGS's 23 bits to it.

All instructions following AUGS are shielded from interrupt until after the instruction with the newly-augmented literal Src value is executed. Src value augmentation occurs in the instruction pipeline only; code is not altered, value does not persist. SETQ/SETQ2 does not affect AUGS; the Q value passes through to the next instruction.

Though AUGS may be manually entered wherever needed, the Parallax P2 compiler supports a convenient way to use this feature. In the target instruction's Src field, use "##" followed by the desired 32-bit literal (instead of "#" followed by a 9-bit literal); the compiler will automatically invoke AUGS immediately before. When counting clock cycles, make sure to account for 2 extra clock cycles for instructions containing ## augmented literals.



# Instructions: B

This section contains all PASM2 instructions beginning with the letter B.



## BITC / BITNC / BITZ / BITNZ {#bitc}

Set bit(s) to flag state {#bitnc} {#bitz} {#bitnz}
[Math and Logic](#math-and-logic) - Set bit(s) to C, NC, Z, or NZ flag state.

**BITC**  *Dest, {#}Src*  **{WCZ}**
**BITNC**  *Dest, {#}Src*  **{WCZ}**
**BITZ**  *Dest, {#}Src*  **{WCZ}**
**BITNZ**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are set to the specified flag state:

| Instruction | Sets bits to |
|-------------|--------------|
| BITC | C flag value |
| BITNC | !C (inverted C) |
| BITZ | Z flag value |
| BITNZ | !Z (inverted Z) |

- Dest is a register whose value will have bit(s) set to the flag state.
- Src identifies the bit(s) to modify: Src[4:0] = bit number, Src[9:5] = additional contiguous bits.
- WCZ is an optional effect to update the Z flag to the original bit state.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100010 | CZI | DDDDDDDDD | SSSSSSSSS | D | --- | orig bit | 2 |
| EEEE | 0100011 | CZI | DDDDDDDDD | SSSSSSSSS | D | --- | orig bit | 2 |
| EEEE | 0100100 | CZI | DDDDDDDDD | SSSSSSSSS | D | --- | orig bit | 2 |
| EEEE | 0100101 | CZI | DDDDDDDDD | SSSSSSSSS | D | --- | orig bit | 2 |


**Related:** [BITH](#bith), [BITL](#bitl), [BITNOT](#bitnot), [BITRND](#bitrnd)

**Explanation:**

These instructions set designated bit(s) in Dest to the specified flag value. BITC and BITZ copy the direct flag state; BITNC and BITNZ copy the inverted flag state.

Src[4:0] indicates the bit number (0-31). For a range, Src[9:5] specifies additional contiguous bits (1-31). A SETQ instruction preceding these can substitute its Dest[4:0] for Src[9:5].

If WCZ is specified, the Z flag is set (1) if the original base bit was set, or cleared (0) if it was clear.



## BITH {#bith}

Bit high
[Math and Logic](#math-and-logic) - Set bit(s) to high (1).

**BITH**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are set to high (1).

- Dest is a register whose value will have one or more bits set high.
- Src is a register, 9-bit literal, or 10-bit augmented literal whose value identifies the bit(s) to modify.
- WCZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100001 | CZI | DDDDDDDDD | SSSSSSSSS | D | --- | original D[S[4:0]] | 2 |


**Related:** [BITL](#bitl), [BITNOT](#bitnot), [BITC](#bitc), [BITNC](#bitnc), [BITZ](#bitz), [BITNZ](#bitnz)

**Explanation:**

BITH sets the Dest bit(s) designated by Src to high (1). All other bits are left unchanged.

Src[4:0] indicates the bit number (0-31). For a range of bits, Src[4:0] indicates the base bit number and Src[9:5] indicates how many contiguous bits beyond the base should be affected (1-31). A 9-bit literal Src is enough to express the base bit (Src[4:0]) and a range of up to 16 contiguous bits (Src[8:5]). If needed, use the augmented literal feature (##Src) to augment Src to a 10-bit literal value.

When Src is a register, the register's value bits [9:0] are used as-is, unless a SETQ instruction immediately precedes BITH, substituting SETQ's Dest[4:0] in place of value bits[9:5].

If the WCZ effect is specified, the Z flag is set (1) if the original Dest base bit (before modification) was set, or is cleared (0) if it was clear. This preserves information about the original bit state before it was set high.



## BITL {#bitl}

Bit low
[Math and Logic](#math-and-logic) - Set bit(s) to low (0).

**BITL**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are set to low (0).

- Dest is a register whose value will have one or more bits set low.
- Src is a register, 9-bit literal, or 10-bit augmented literal whose value identifies the bit(s) to modify.
- WCZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100000 | CZI | DDDDDDDDD | SSSSSSSSS | D | --- | original D[S[4:0]] | 2 |


**Related:** [BITH](#bith), [BITNOT](#bitnot), [BITC](#bitc), [BITNC](#bitnc), [BITZ](#bitz), [BITNZ](#bitnz)

**Explanation:**

BITL sets the Dest bit(s) designated by Src to low (0). All other bits are left unchanged.

Src[4:0] indicates the bit number (0-31). For a range of bits, Src[4:0] indicates the base bit number and Src[9:5] indicates how many contiguous bits beyond the base should be affected (1-31). A 9-bit literal Src is enough to express the base bit (Src[4:0]) and a range of up to 16 contiguous bits (Src[8:5]). If needed, use the augmented literal feature (##Src) to augment Src to a 10-bit literal value.

When Src is a register, the register's value bits [9:0] are used as-is, unless a SETQ instruction immediately precedes BITL, substituting SETQ's Dest[4:0] in place of value bits[9:5].

If the WCZ effect is specified, the Z flag is set (1) if the original Dest base bit (before modification) was set, or is cleared (0) if it was clear. This preserves information about the original bit state before it was cleared to low.



## BITNOT {#bitnot}

Bit not
[Math and Logic](#math-and-logic) - Toggle bit(s) to the opposite state.

**BITNOT**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are toggled to their opposite state(s).

- Dest is a register whose value will have one or more bits toggled.
- Src is a register, 9-bit literal, or 10-bit augmented literal whose value identifies the bit(s) to modify.
- WCZ is an optional effect to update the C and Z flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100111 | CZI | DDDDDDDDD | SSSSSSSSS | D | --- | original D[S[4:0]] | 2 |


**Related:** [BITH](#bith), [BITL](#bitl), [BITC](#bitc), [BITNC](#bitnc), [BITZ](#bitz), [BITNZ](#bitnz), [BITRND](#bitrnd)

**Explanation:**

BITNOT alters the Dest bit(s) designated by Src to their inverse state. All other bits are left unchanged.

Src[4:0] indicates the bit number (0-31). For a range of bits, Src[4:0] indicates the base bit number and Src[9:5] indicates how many contiguous bits beyond the base should be affected (1-31). A 9-bit literal Src is enough to express the base bit (Src[4:0]) and a range of up to 16 contiguous bits (Src[8:5]). If needed, use the augmented literal feature (##Src) to augment Src to a 10-bit literal value.

When Src is a register, the register's value bits [9:0] are used as-is, unless a SETQ instruction immediately precedes BITNOT, substituting SETQ's Dest[4:0] in place of value bits[9:5].

If the WCZ effect is specified, the C and Z flags are set (1) if the original Dest base bit (before modification) was set, or are cleared (0) if it was clear. This preserves information about the original bit state.



## BITRND {#bitrnd}

Bit random
[Math and Logic](#math-and-logic) - Set bit(s) to random low or high values.

**BITRND**  *Dest, {#}Src*  **{WCZ}**

---

**Result:** Dest bit(s) designated by Src are each set randomly to low or high.

- Dest is a register whose value will have one or more bits set randomly low or high.
- Src is a register, 9-bit literal, or 10-bit augmented literal whose value identifies the bit(s) to modify.
- WCZ is an optional effect to update the C and Z flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100110 | CZI | DDDDDDDDD | SSSSSSSSS | D | original D[S[4:0]] | original D[S[4:0]] | 2 |


**Related:** [BITZ](#bitz), [BITNZ](#bitnz), [BITC](#bitc), [BITNC](#bitnc), [BITH](#bith), [BITL](#bitl), [BITNOT](#bitnot)

**Explanation:**

BITRND alters the Dest bit(s) designated by Src to each be an independent random low or high value, based on bit(s) from the Xoroshiro128** PRNG. All other bits are left unchanged.

Src[4:0] indicates the bit number (0-31). For a range of bits, Src[4:0] indicates the base bit number and Src[9:5] indicates how many contiguous bits beyond the base should be affected (1-31). A 9-bit literal Src is enough to express the base bit (Src[4:0]) and a range of up to 16 contiguous bits (Src[8:5]). If needed, use the augmented literal feature (##Src) to augment Src to a 10-bit literal value.

When Src is a register, the register's value bits [9:0] are used as-is, unless a SETQ instruction immediately precedes BITRND, substituting SETQ's Dest[4:0] in place of value bits[9:5].

If the WCZ effect is specified, the C and Z flags are set (1) if the original Dest base bit (before modification) was set, or are cleared (0) if it was clear. This preserves information about the original state of the base bit before randomization.

Each bit in the range is set independently from the PRNG, producing true random values suitable for cryptographic initialization vectors, random number generation, and simulation applications.



## BLNPIX {#blnpix}

Blend pixels
[Pixel Mixer](#pixel-mixer) - Alpha-blend RGB bytes using SETPIV value.

**BLNPIX**  *Dest, {#}Src*

---

**Result:** Src color value bytes are alpha-blended into Dest color value bytes using the SETPIV blend factor.

- Dest is a register containing the RGB color value to blend Src into, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose RGB color value bytes are blended into Dest.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010010 | 10I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 7 |


**Related:** [ADDPIX](#addpix), [SUBPIX](#subpix), [MULPIX](#mulpix), [SETPIV](#setpiv)

**Explanation:**

BLNPIX alpha-blends the individual RGB (red, green, blue) color values of Src into that of Dest and stores the result in the Dest register. The blend factor is set by a previous SETPIV instruction.

The alpha-blending operation combines the two color values based on the blend factor, allowing smooth color transitions and transparency effects. A blend factor of 0 leaves Dest unchanged, while a blend factor of 255 completely replaces Dest with Src. Values between 0 and 255 produce proportional blends.

The instruction processes all three color channels (and alpha if present) in parallel, completing in 7 clock cycles. This enables efficient pixel manipulation for graphics applications, user interfaces, and visual effects.



## BMASK {#bmask}

Bit mask
[Math and Logic](#math-and-logic) - Generate an LSB-justified bit mask.

**BMASK**  *Dest, {#}Src*
**BMASK**  *Dest*

---

**Result:** Bit mask of size Src+1, or Dest+1 (1 to 32 bits) is stored into Dest.

- Dest is a register in which to store the generated bit mask and optionally contains the 5-bit mask size (second syntax).
- Src is a register or 5-bit literal whose value is the size of the bit mask to generate.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001110 | 01I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001110 | 010 | DDDDDDDDD | DDDDDDDDD | D | --- | --- | 2 |


**Related:** [ENCOD](#encod), [DECOD](#decod), [ONES](#ones), [ZEROX](#zerox)

**Explanation:**

BMASK generates an LSB-justified bit mask (all ones) of Src+1 or Dest+1 length and stores it in Dest. The size value, whether specified by Src or Dest, is in the range 0-31 to generate 1 to 32 bits of bit mask.

In effect, Dest becomes (%10 << size) - 1 via the BMASK instruction. A size value of 0 generates a 1-bit mask (%1), a size value of 5 generates a 6-bit mask (%111111), and a size value of 15 generates a 16-bit mask (%1111_1111_1111_1111).

A bit mask is often useful in bitwise operations (AND, OR, XOR) to filter out or affect special groups of bits. For example:

```pasm
        bmask   mask, #7               ' Create 8-bit mask ($FF)
        and     data, mask             ' Keep only lower 8 bits
```

The first syntax form uses Src to specify the size, while the second syntax form (without Src) uses the value already in Dest to determine the mask size. Both forms write the resulting mask back to Dest.



## BRK {#brk}

Break
[Interrupt](#interrupt) - Trigger breakpoint in current COG.

**BRK**  *{#}Dest*

---

**Result:** If debug interrupts are enabled, a debug interrupt is triggered in the current COG and Dest's value becomes the debug code or the next debug condition.

- Dest is a register, 9-bit literal, or 32-bit augmented literal whose value becomes the debug code or condition depending on the state of execution (outside or inside of a Debug ISR).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110110 | --- | --- | --- | 2 |


**Related:** [GETBRK](#getbrk), [COGBRK](#cogbrk)

**Explanation:**

BRK triggers a breakpoint in the current COG and either defines a breakpoint code or the next breakpoint condition(s). The COG must have debug interrupts enabled, and if BRK is to be executed within the normal program (outside the Debug ISR), the "BRK instruction" interrupt must first be enabled from within a prior Debug ISR.

During normal program execution, the BRK instruction is used to generate a debug interrupt with an 8-bit code (from Dest[7:0]) which can be read within the Debug ISR using a GETBRK instruction. This allows the program to communicate debug information or trigger specific breakpoint handlers.

During a Debug ISR, the BRK instruction is used instead to establish the next debug interrupt condition(s) and to select INA/INB, instead of the IJMP0/IRET0 registers exposed during the ISR, so that the pins' inputs states may be read.

The format of Dest for Debug ISR use is %AAAAAAAAAAAAAAAAAAAA_BCDEFGHIJKLM where A is the 20-bit breakpoint address or 4-bit event code, and bits B-M control various interrupt enable conditions.

BRK is essential for interactive debugging, allowing precise control over program execution and inspection of program state at specific points or conditions.



# Instructions: C

This section contains all PASM2 instructions beginning with the letter C.



## CALL {#call}

Call subroutine
[Branch](#branch) - Call a subroutine; store return context on the stack.

**CALL**  *#Addr*
**CALL**  *#\Addr*
**CALL**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Current C and Z flags and address of the next instruction are pushed onto the hardware stack, PC is set to the new address, and optionally C and Z are updated to new states.

- Addr is a symbolic reference to the target subroutine; the location to set PC to. Relative addressing is the default; use '\' to force absolute addressing.
- Dest is a register containing the 20-bit absolute address to set PC to and optional new C and Z states.
- WC, WZ, or WCZ are optional effects to update the flags from Dest's upper bit states.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101101 | RAA | AAAAAAAAA | AAAAAAAAA | K and PC | --- | --- | 4 / 13-20 |
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101101 | K and PC | D[31] | D[30] | 4 / 13-20 |


**Related:** [RET](#ret), [CALLA](#calla), [CALLB](#callb), [CALLD](#calld), [CALLPA](#callpa), [CALLPB](#callpb)

**Explanation:**

CALL records the current state of the C and Z flags and the address of the next instruction (PC + 1 if COG/LUT execution; PC + 4 if Hub execution) by pushing to the stack (K), potentially updates the C and Z flags with new given states, and jumps to the given address or offset. The routine at the new address should eventually execute a RET instruction, or an instruction with a _RET_ condition, to return to the recorded address (the instruction following the CALL) and optionally restore the C and Z flag state as it was prior.

In the first syntax form, `#Addr` and `#\Addr` encodes the instruction with relative and absolute addressing, respectively. The relative form (the default) is vital for creating relocatable code. In either case, use symbolic references for Addr and the assembler will encode it properly. Examples: `CALL #SendBit` or `CALL #\DebugStatus`.

In the second syntax form, the format of the value at Dest is `CZxxxxxx_xxxxAAAA_AAAAAAAA_AAAAAAAA`. C is the new C flag state, Z is the new Z flag state, A is the new 20-bit address to jump to, and x are don't-care bits. This syntax effectively swaps the flags and PC with the value in the Dest register (and RET swaps them back), making it convenient for switching between two threads.

If the WC or WCZ effect is specified, the C flag is updated to match D[31], after its original state is recorded.

If the WZ or WCZ effect is specified, the Z flag is updated to match D[30], after its original state is recorded.

The instruction takes 4 cycles for COG/LUT execution, or 13-20 cycles for Hub execution.



## CALLA {#calla}

Call subroutine via PTRA
[Branch](#branch) - Call a subroutine; store return context in the Hub long at PTRA++.

**CALLA**  *#Addr*
**CALLA**  *#\Addr*
**CALLA**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Current C and Z flags and address of the next instruction are written to Hub RAM at PTRA, PTRA is incremented by 4, PC is set to the new address, and optionally C and Z are updated to new states.

- Addr is a symbolic reference to the target subroutine; the location to set PC to. Relative addressing is the default; use '\' to force absolute addressing.
- Dest is a register containing the 20-bit absolute address to set PC to and optional new C and Z states.
- WC, WZ, or WCZ are optional effects to update the flags from Dest's upper bit states.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101110 | RAA | AAAAAAAAA | AAAAAAAAA | --- | --- | --- | 5...12 |
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101110 | --- | D[31] | D[30] | 5...12 |


**Related:** [CALL](#call), [CALLB](#callb), [CALLD](#calld), [RETA](#reta)

**Explanation:**

CALLA writes the current C and Z flags and the address of the next instruction into the 4-byte Hub RAM location at PTRA, then increments PTRA by 4, sets PC to the new relative or absolute address, and optionally updates C and Z to new states.

In the first syntax form, `#Addr` and `#\Addr` encodes the instruction with relative and absolute addressing, respectively. The relative form (the default) is vital for creating relocatable code. In either case, use symbolic references for Addr and the assembler will encode it properly.

In the second syntax form, the format of the value at Dest is `CZxxxxxx_xxxxAAAA_AAAAAAAA_AAAAAAAA`. C is the new C flag state, Z is the new Z flag state, A is the new 20-bit address to jump to, and x are don't-care bits.

If the WC or WCZ effect is specified, the C flag is set to D[31] after the original state is recorded.

If the WZ or WCZ effect is specified, the Z flag is set to D[30] after the original state is recorded.

CALLA is used for subroutine calls when Hub RAM is being used as the call stack instead of the hardware stack. This is useful for deep nesting or when preserving the hardware stack for other purposes. The instruction takes 5-12 cycles depending on Hub memory timing.



## CALLB {#callb}

Call subroutine via PTRB
[Branch](#branch) - Call a subroutine; store return context in the Hub long at PTRB++.

**CALLB**  *#Addr*
**CALLB**  *#\Addr*
**CALLB**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Current C and Z flags and address of the next instruction are written to Hub RAM at PTRB, PTRB is incremented by 4, PC is set to the new address, and optionally C and Z are updated to new states.

- Addr is a symbolic reference to the target subroutine; the location to set PC to. Relative addressing is the default; use '\' to force absolute addressing.
- Dest is a register containing the 20-bit absolute address to set PC to and optional new C and Z states.
- WC, WZ, or WCZ are optional effects to update the flags from Dest's upper bit states.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101111 | RAA | AAAAAAAAA | AAAAAAAAA | --- | --- | --- | 5...12 |
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101111 | --- | D[31] | D[30] | 5...12 |


**Related:** [CALL](#call), [CALLA](#calla), [CALLD](#calld), [RETB](#retb)

**Explanation:**

CALLB writes the current C and Z flags and the address of the next instruction into the 4-byte Hub RAM location at PTRB, then increments PTRB by 4, sets PC to the new relative or absolute address, and optionally updates C and Z to new states.

In the first syntax form, `#Addr` and `#\Addr` encodes the instruction with relative and absolute addressing, respectively. The relative form (the default) is vital for creating relocatable code. In either case, use symbolic references for Addr and the assembler will encode it properly.

In the second syntax form, the format of the value at Dest is `CZxxxxxx_xxxxAAAA_AAAAAAAA_AAAAAAAA`. C is the new C flag state, Z is the new Z flag state, A is the new 20-bit address to jump to, and x are don't-care bits.

If the WC or WCZ effect is specified, the C flag is set to D[31] after the original state is recorded.

If the WZ or WCZ effect is specified, the Z flag is set to D[30] after the original state is recorded.

CALLB operates identically to CALLA except it uses PTRB as the stack pointer instead of PTRA. This allows for maintaining separate call stacks or using both pointers for different purposes. The instruction takes 5-12 cycles depending on Hub memory timing.



## CALLD {#calld}

Call with destination register
[Branch](#branch) - Call a subroutine; store return context in PA/PB/PTRA/PTRB/D.

**CALLD**  *PA|PB|PTRA|PTRB, #Addr*
**CALLD**  *PA|PB|PTRA|PTRB, #\Addr*
**CALLD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Current C and Z flags and address of the next instruction are written to the specified register (PA, PB, PTRA, PTRB, or Dest), PC is set to the new address, and optionally C and Z are updated to new states.

- PA|PB|PTRA|PTRB is the special register to store the current C and Z flags and next address into.
- Addr is a symbolic reference to the target subroutine; the location to set PC to. Relative addressing is the default; use '\' to force absolute addressing.
- Dest is a register to write the current C and Z flags and the address of the next instruction into.
- Src is a register, 9-bit literal, or 32-bit augmented literal that contains the relative or absolute address to set PC to and optional new C and Z states. Use # for relative addressing; omit # for absolute addressing.
- WC, WZ, or WCZ are optional effects to update the flags from Src's upper bit states.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 11100WW | RAA | AAAAAAAAA | AAAAAAAAA | Pxxx and PC | --- | --- | 4 / 13-20 |
| EEEE | 1011001 | CZI | DDDDDDDDD | SSSSSSSSS | D and PC | S[31] | S[30] | 4 / 13-20 |


**Related:** [CALL](#call), [CALLPA](#callpa), [CALLPB](#callpb), [RET](#ret), [PA](#pa), [PB](#pb), [PTRA](#ptra), [PTRB](#ptrb)

**Explanation:**

CALLD records the current state of the C and Z flags and the address of the next instruction (PC + 1 if COG/LUT execution; PC + 4 if Hub execution) by writing them to the PA, PB, PTRA, PTRB, or Dest register, potentially updates the C and Z flags with new given states, and jumps to the given address or offset. The routine at the new address should eventually execute another CALLD instruction to return to the recorded address (the instruction following the original CALLD), optionally restore the C and Z flag state as it was prior, and optionally prep for another CALLD.

This instruction is typically used for the P2 DEBUG function.

In the first syntax form, `#Addr` and `#\Addr` encodes the instruction with relative and absolute addressing, respectively. The relative form (the default) is vital for creating relocatable code. In either case, use symbolic references for Addr and the assembler will encode it properly. Examples: `CALLD PA, #SendBit` or `CALLD PB, #\DebugStatus`.

In the second syntax form, the format of the value at Src is `CZxxxxxx_xxxxAAAA_AAAAAAAA_AAAAAAAA`. C is the new C flag state, Z is the new Z flag state, A is the new 20-bit address to jump to, and x are don't-care bits. If Src is a 9-bit literal (immediate), it will be sign-extended to 20 bits and used as a relative offset, giving a range of -256 to +255 instructions relative to the instruction following the CALLD. When relative, PC is adjusted by signed(Src) if COG/LUT execution, or by signed(Src * 4) if Hub execution.

If the WC or WCZ effect is specified, the C flag is updated to match S[31], after its original state is recorded.

If the WZ or WCZ effect is specified, the Z flag is updated to match S[30], after its original state is recorded.

The instruction takes 4 cycles for COG/LUT execution, or 13-20 cycles for Hub execution.



## CALLPA {#callpa}

Call subroutine with PA parameter
[Branch](#branch) - Call a subroutine; store return context on the stack and copy D into PA.

**CALLPA**  *{#}Dest, {#}Src*

---

**Result:** Current C and Z flags and address of the next instruction are pushed onto the hardware stack, Dest is copied to PA, and PC is set to the address specified by Src.

- Dest is a register, 9-bit literal, or 32-bit augmented literal whose value is copied to PA.
- Src is a register, 9-bit literal, or 32-bit augmented literal that contains the relative or absolute address to set PC to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011010 | 0LI | DDDDDDDDD | SSSSSSSSS | K, PA and PC | --- | --- | 4 / 13-20 |


**Related:** [CALL](#call), [CALLPB](#callpb), [CALLD](#calld), [RET](#ret), [PA](#pa)

**Explanation:**

CALLPA records the current state of the C and Z flags and the address of the next instruction (PC + 1 if COG/LUT execution; PC + 4 if Hub execution) by pushing to the stack (K), copies the value of Dest to PA, and jumps to the address specified by Src. The routine at the new address should eventually execute a RET instruction to return to the recorded address and restore the flags.

This instruction is useful for passing a parameter to a subroutine via the PA register while simultaneously calling that subroutine. The parameter can be an immediate value, making it convenient for subroutines that need a single argument.

The Src operand determines the target address. If Src is preceded by #, it is treated as a relative address; otherwise it is an absolute address. If Src is a register, its lower 20 bits specify the absolute address to jump to.

The instruction takes 4 cycles for COG/LUT execution, or 13-20 cycles for Hub execution.



## CALLPB {#callpb}

Call subroutine with PB parameter
[Branch](#branch) - Call a subroutine; store return context on the stack and copy D into PB.

**CALLPB**  *{#}Dest, {#}Src*

---

**Result:** Current C and Z flags and address of the next instruction are pushed onto the hardware stack, Dest is copied to PB, and PC is set to the address specified by Src.

- Dest is a register, 9-bit literal, or 32-bit augmented literal whose value is copied to PB.
- Src is a register, 9-bit literal, or 32-bit augmented literal that contains the relative or absolute address to set PC to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011010 | 1LI | DDDDDDDDD | SSSSSSSSS | K, PB and PC | --- | --- | 4 / 13-20 |


**Related:** [CALL](#call), [CALLPA](#callpa), [CALLD](#calld), [RET](#ret), [PB](#pb)

**Explanation:**

CALLPB records the current state of the C and Z flags and the address of the next instruction (PC + 1 if COG/LUT execution; PC + 4 if Hub execution) by pushing to the stack (K), copies the value of Dest to PB, and jumps to the address specified by Src. The routine at the new address should eventually execute a RET instruction to return to the recorded address and restore the flags.

This instruction operates identically to CALLPA except it uses the PB register instead of PA. This is useful for passing a parameter to a subroutine via the PB register, or when both PA and PB need to be set by using CALLPA followed by CALLPB, or when the subroutine convention uses PB for parameters.

The Src operand determines the target address. If Src is preceded by #, it is treated as a relative address; otherwise it is an absolute address. If Src is a register, its lower 20 bits specify the absolute address to jump to.

The instruction takes 4 cycles for COG/LUT execution, or 13-20 cycles for Hub execution.



## CMP {#cmp}

Compare
[Math and Logic](#math-and-logic) - Compare two unsigned values.

**CMP**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010000 | CZI | DDDDDDDDD | SSSSSSSSS | --- | Unsigned (D < S) | D=S | 2 |


**Related:** [CMPR](#cmpr), [CMPX](#cmpx), [CMPS](#cmps), [CMPSX](#cmpsx), [CMPM](#cmpm)

**Explanation:**

CMP compares the unsigned values of Dest and Src by subtracting Src from Dest and optionally setting the C and Z flags accordingly. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest is less than Src (unsigned comparison), or is cleared (0) if Dest is greater than or equal to Src. This indicates that the subtraction would require a borrow.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Dest equals Src, or is cleared (0) if they are not equal.

To compare unsigned multi-long values (64-bit or larger), use CMP for the least significant long, then CMPX for each subsequent long. For example, to compare two 64-bit values:

```pasm
        cmp     value_lo, other_lo  wc    ' Compare low longs
        cmpx    value_hi, other_hi  wcz   ' Compare high longs with borrow
        ' C and Z now reflect the 64-bit comparison result
```

CMP is fundamental for implementing conditional logic and control flow based on numeric comparisons.



## CMPM {#cmpm}

Compare most significant bit
[Math and Logic](#math-and-logic) - Compare two unsigned values, get MSB of difference.

**CMPM**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010101 | CZI | DDDDDDDDD | SSSSSSSSS | --- | Result[31] | D=S | 2 |


**Related:** [CMP](#cmp), [CMPS](#cmps)

**Explanation:**

CMPM compares the unsigned values of Dest and Src by subtracting Src from Dest and optionally setting the C and Z flags accordingly. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is updated to the MSB (bit 31) of the result of Dest - Src. This is different from CMP, which sets C based on whether a borrow occurred. CMPM's C flag directly reflects the sign bit of the difference.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Dest equals Src, or is cleared (0) if they are not equal.

CMPM is useful when the most significant bit of the difference carries semantic meaning for the algorithm being implemented, such as certain mathematical operations or specialized comparison logic.



## CMPR {#cmpr}

Compare reverse
[Math and Logic](#math-and-logic) - Compare two unsigned values (in reverse order to CMP).

**CMPR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010100 | CZI | DDDDDDDDD | SSSSSSSSS | --- | borrow of (S - D) | D == S | 2 |


**Related:** [CMP](#cmp)

**Explanation:**

CMPR compares the unsigned values of Dest and Src by subtracting Dest from Src (the reverse of CMP) and optionally setting the C and Z flags accordingly. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if Src is less than Dest (unsigned comparison), or is cleared (0) if Src is greater than or equal to Dest. This is the opposite condition from CMP.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Dest equals Src, or is cleared (0) if they are not equal.

CMPR is useful when the natural order of operands in your code is reversed from what CMP expects, avoiding the need to swap operands or reverse the logic. Note that for unsigned multi-long comparisons, use CMP (not CMPR) followed by CMPX.



## CMPS {#cmps}

Compare signed
[Math and Logic](#math-and-logic) - Compare two signed values.

**CMPS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010010 | CZI | DDDDDDDDD | SSSSSSSSS | --- | Signed (D < S) | D=S | 2 |


**Related:** [CMP](#cmp), [CMPX](#cmpx), [CMPSX](#cmpsx)

**Explanation:**

CMPS compares the signed values of Dest and Src by subtracting Src from Dest and optionally setting the C and Z flags to indicate the comparison and operation results. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if signed Dest is less than signed Src, or is cleared (0) if signed Dest is greater than or equal to signed Src. The comparison properly accounts for the sign bit.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Dest equals Src, or is cleared (0) if they are not equal.

To compare signed multi-long values (64-bit or larger), use CMP (not CMPS) for the least significant long, optionally followed by CMPX for middle longs, and finally CMPSX for the most significant long. The final CMPSX accounts for sign extension properly. For example, to compare two 64-bit signed values:

```pasm
        cmp     value_lo, other_lo  wc    ' Compare low longs unsigned
        cmpsx   value_hi, other_hi  wcz   ' Compare high signed w/borrow
        ' C and Z now reflect the signed 64-bit comparison result
```



## CMPSUB {#cmpsub}

Compare and subtract
[Math and Logic](#math-and-logic) - Compare two unsigned values and subtract the second if it is lesser or equal.

**CMPSUB**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Dest is decremented by Src unless it is less than Src, and the comparison results are optionally written to the C and Z flags.

- Dest is the register containing the value to compare with Src and is the destination written to if a subtraction is performed.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared with and possibly subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010111 | CZI | DDDDDDDDD | SSSSSSSSS | D\textsuperscript{1} | Unsigned(D >= S) | Result = 0 | 2 |


\textsuperscript{1} Dest is only written if Dest >= Src (subtraction was performed).

**Related:** [CMP](#cmp), [SUB](#sub)

**Explanation:**

CMPSUB compares the unsigned values of Dest and Src, and if Src is less than or equal to Dest, then Src is subtracted from Dest. Optionally, the C and Z flags are set to indicate the comparison and operation results.

The operation performs the comparison first. If Dest >= Src (unsigned), then Dest is updated to Dest - Src. If Dest < Src, then Dest is left unchanged.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was greater than or equal to Src (subtraction was performed), or is cleared (0) if Dest was less than Src (no subtraction).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals 0, or is cleared (0) if non-zero. Note that if no subtraction was performed (Dest < Src), Z reflects whether Dest was already zero.

CMPSUB is particularly useful for implementing division algorithms, modulo operations, and other mathematical routines where conditional subtraction based on magnitude is needed.



## CMPSX {#cmpsx}

Compare signed, extended
[Math and Logic](#math-and-logic) - Compare two signed values plus carry flag.

**CMPSX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is the register containing the value to compare with that of Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010011 | CZI | DDDDDDDDD | SSSSSSSSS | --- | correct sign of (D - (S + C)) | Z AND (D == S + C) | 2 |


**Related:** [CMP](#cmp), [CMPX](#cmpx), [CMPS](#cmps)

**Explanation:**

CMPSX compares the signed values of Dest and Src plus C by subtracting Src + C from Dest and optionally setting the C and Z flags accordingly. The CMPSX instruction is used to perform signed multi-long comparisons, such as 64-bit comparisons. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest is less than Src + C (as multi-long signed values), or is cleared (0) otherwise. Use WC or WCZ on preceding CMP and CMPX instructions for proper final C flag. The comparison properly accounts for sign extension.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Z was previously set and the result of Dest - (Src + C) is zero, or it is cleared (0) if non-zero. This allows the Z flag to cascade through multi-long comparisons, remaining set only if all compared longs are equal.

For signed multi-long comparisons, use CMP for the least significant long, optionally CMPX for middle longs, and CMPSX for the most significant long:

```pasm
        cmp     value_lo, other_lo  wc    ' Compare low longs
        cmpsx   value_hi, other_hi  wcz   ' Compare high signed w/borrow
        ' C=1 if signed value < other, Z=1 if equal
```



## CMPX {#cmpx}

Compare extended
[Math and Logic](#math-and-logic) - Compare two unsigned values plus carry flag.

**CMPX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Greater/lesser and equality status is optionally written to the C and Z flags.

- Dest is a register containing the value to compare with that of Src plus C.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is compared to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010001 | CZI | DDDDDDDDD | SSSSSSSSS | --- | borrow of (D - (S + C)) | Z AND (D == S + C) | 2 |


**Related:** [CMP](#cmp), [CMPS](#cmps), [CMPSX](#cmpsx)

**Explanation:**

CMPX compares the unsigned values of Dest and Src plus C by subtracting Src + C from Dest and optionally setting the C and Z flags accordingly. The CMPX instruction is used to perform unsigned multi-long comparisons, such as 64-bit comparisons. The result of the subtraction is discarded; only the flags are affected. Dest is not modified.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest is less than Src plus C (unsigned comparison), or is cleared (0) otherwise. Use WC or WCZ on preceding CMP and CMPX instructions for proper final C flag.

If the WZ or WCZ effect is specified, the Z flag is set (1) if Z was previously set and Dest equals Src + C, or it is cleared (0) otherwise. This allows the Z flag to cascade through multi-long comparisons, remaining set only if all compared longs are equal.

For unsigned multi-long comparisons, use CMP for the least significant long, then CMPX for each subsequent long:

```pasm
        cmp     value_lo, other_lo  wc    ' Compare low longs
        cmpx    value_hi, other_hi  wcz   ' Compare high longs with borrow
        ' C=1 if unsigned value < other, Z=1 if equal
```



## COGATN {#cogatn}

Cog attention
[Event](#event) - Get the attention of one or more other cogs.

**COGATN**  *{#}Dest*

---

**Result:** The attention signal of one or more cogs is strobed.

- Dest is the register or 9-bit literal whose value (lower 8-bit pattern) indicates which cogs to signal.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111111 | --- | --- | --- | 2 |


**Related:** [POLLATN](#pollatn), [WAITATN](#waitatn), [JATN](#jatn), [JNATN](#jnatn)

**Explanation:**

COGATN strobes the attention signal for one or more cogs. Dest bit positions 7:0 represent cogs 7 through 0; high (1) bits indicate the cog(s) to signal. The receiving cog(s) then latch the signal, setting an internal flag, and can use any of the attention monitor instructions (JATN, JNATN, POLLATN, WAITATN) or interrupts to respond and clear the flag.

In the intended use case, the cog receiving an attention request knows which other cog is strobing it and how to respond. In cases where multiple cogs may request the attention of a single cog, some messaging structure may need to be implemented in Hub RAM to differentiate requests.

For example, to signal cog 3:

```pasm
        cogatn  #%0000_1000           ' Signal cog 3 (bit 3 = 1)
```

To signal multiple cogs simultaneously:

```pasm
        cogatn  #%0001_0010           ' Signal cogs 1 and 4
```

COGATN is useful for implementing inter-cog communication, synchronization, and event notification without requiring polling of shared memory.



## COGBRK {#cogbrk}

Cog break
[Miscellaneous](#miscellaneous) - Trigger breakpoint in specified cog.

**COGBRK**  *{#}Dest*

---

**Result:** If in the Debug ISR, trigger an asynchronous breakpoint in cog identified by Dest.

- Dest is the register or 9-bit literal whose value (lower 3-bits) indicates which cog to trigger.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110101 | --- | --- | --- | 2 |


**Related:** [CALLD](#calld), [BRK](#brk)

**Explanation:**

COGBRK triggers an asynchronous breakpoint in a designated cog. The COGBRK instruction must be executed from within a Debug ISR (interrupt service routine) and the designated cog must already have its asynchronous breakpoint interrupt enabled. Dest[2:0] indicates the ID of the desired cog (0-7).

This instruction is part of the P2's debugging infrastructure and is typically used by debug monitors or development tools to halt a running cog for inspection. When executed, the target cog will interrupt its current execution and vector to its debug interrupt handler, allowing the debugging system to examine or modify the cog's state.

For example, to trigger a breakpoint in cog 2:

```pasm
        cogbrk  #2                    ' Break cog 2 (must be in debug ISR)
```

COGBRK is a specialized instruction primarily used by development and debugging tools rather than in typical application code.



## COGID {#cogid}

Cog identification
[Hub Control](#hub-control) - Get current cog's ID or any cog's status by ID.

**COGID**  *{#}Dest*  **{WC}**

---

**Result:** Current cog's ID is written to Dest or C is set (1) or cleared (0) if the Dest cog is running or stopped.

- Dest is the register where the current cog's ID will be written, or is the register or 9-bit literal whose value (lower 3-bits) indicates which cog to get the status for.
- WC is an optional effect to update the C flag with the Dest cog's running status.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C0L | DDDDDDDDD | 000000001 | D if reg and !WC | Cog Running | --- | 2-9, +2 if result |


**Related:** [COGINIT](#coginit), [COGSTOP](#cogstop)

**Explanation:**

COGID writes the current cog's ID into Dest (if Dest is a register and WC is omitted) or sets/clears the C flag according to the running/stopped state of the cog indicated by Dest[2:0] (if WC is given).

When used without the WC effect, COGID stores the current cog's ID (0-7) in the Dest register. This is useful when code needs to know which cog it is running on, for example when accessing cog-specific resources or implementing cog-aware algorithms.

When used with the WC effect, COGID checks the status of the cog specified by Dest[2:0]. If the WC effect is specified, the C flag is set (1) if the specified cog is running, or is cleared (0) if stopped. In this mode, Dest is not written.

For example, to get the current cog's ID:

```pasm
        cogid   myid                  ' Store this cog's ID in myid
```

To check if cog 3 is running:

```pasm
        cogid   #3              wc    ' C=1 if cog 3 is running
```



## COGINIT {#coginit}

Cog initialize
[Hub Control](#hub-control) - Start an available cog, or restart a cog by ID.

**COGINIT**  *{#}Dest, {#}Src*  **{WC}**

---

**Result:** Target cog is started according to Dest to execute code from Src. The code pointer (Src) is written to the target cog's PTRB, and optionally a data pointer is written to its PTRA if SETQ preceded COGINIT.

- Dest is the register or 9-bit literal describing the type of launch and possibly the ID of the desired cog to launch. If Dest is a register and WC is given, Dest is also where the ID of the launched cog will be written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value (lower 20 bits) is the target RAM address (for code) and the new cog's PTRB value.
- WC is an optional effect to update the C flag with the success (0) or fail (1) status and triggers Dest to be overwritten with new cog's ID.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100111 | CLI | DDDDDDDDD | SSSSSSSSS | D if reg and WC | No cog available | --- | 2-9, +2 if result |


**Related:** [COGID](#cogid), [COGSTOP](#cogstop)

**Explanation:**

COGINIT starts a new (unused) cog, a new pair of cogs (that may share LUT memory), or a specific cog by ID, to load code from Hub RAM to be executed within COG/LUT RAM or to be executed right from Hub RAM.

The format of Dest is `%E_N_xVVV` where:
- E controls loading (0=load from Hub, 1=no load/Hub exec)
- N controls target selection (0=specific cog ID, 1=find free cog)
- VVV is the cog ID or mode

The lower 20 bits of Src is the code address; the entire 32-bit Src is written to the target cog's PTRB. If COGINIT is preceded by SETQ, that value is written to the target cog's PTRA.

If the WC effect is specified, C is set (1) on failure or cleared (0) on success. When WC is given and Dest is a register, Dest receives the launched cog's ID (or $F on failure).

Common usage examples:

Load and start a specific cog from Hub RAM:

```pasm
        coginit #1, #$100             ' Load and start cog 1 from Hub $100
```

Start a free cog:

```pasm
                coginit #COGEXEC_NEW, addr  wc  ' Find free cog, load, start
        if_c    jmp     #no_cog_available       ' Branch if no cog available
```

Skip load and execute from Hub RAM:

```pasm
        coginit #HUBEXEC+3, addr      ' Cog 3 hub exec mode
```

Start a cog pair for LUT sharing:

```pasm
        coginit #HUBEXEC_NEW_PAIR, addr   ' Start free cog pair
```



## COGSTOP {#cogstop}

Cog stop
[Hub Control](#hub-control) - Stop a cog by ID.

**COGSTOP**  *{#}Dest*

---

**Result:** Cog indicated by Dest is terminated (stopped).

- Dest is the register or 9-bit literal indicating (in lowest 3 bits) which cog to stop.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000000011 | --- | --- | --- | 2-9 |


**Related:** [COGINIT](#coginit), [COGID](#cogid)

**Explanation:**

COGSTOP terminates the cog identified by Dest[2:0]. In this dormant state, the cog ceases to execute code and power consumption is greatly reduced.

The cog specified by the lower 3 bits of Dest (0-7) is immediately halted. All registers and state in that cog are lost. The cog can be restarted later using COGINIT, which will reload it with new code and reset its state.

For example, to stop cog 4:

```pasm
        cogstop #4                    ' Stop cog 4
```

To stop the current cog (terminate self):

```pasm
        cogid   myid                  ' Get my cog ID
        cogstop myid                  ' Stop myself
```

COGSTOP is useful for managing cog resources dynamically, shutting down cogs that are no longer needed, or resetting a cog before restarting it with new code. Note that stopping a cog does not free any Hub memory it may have been using.



## CRCBIT {#crcbit}

CRC iterate bit
[Math and Logic](#math-and-logic) - Iterate CRC value in D using C and polynomial in S.

**CRCBIT**  *Dest, {#}Src*

---

**Result:** Dest is updated with the next CRC iteration using the C flag and polynomial in Src.

- Dest is a register containing the current CRC value and is where the updated CRC is written.
- Src is a register or 9-bit literal containing the CRC polynomial.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001110 | 10I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [CRCNIB](#crcnib), [REV](#rev)

**Explanation:**

CRCBIT iterates the CRC value in Dest using the current C flag and the polynomial in Src. This instruction is designed for computing cyclic redundancy check (CRC) values bit by bit.

The operation performs a single bit iteration of a CRC calculation. The C flag represents the input bit, and Src contains the CRC polynomial. Dest contains the running CRC value and is updated with the result of this iteration.

The exact algorithm follows the standard CRC bit-wise computation:
1. Shift the CRC value in Dest left by one bit
2. If the original MSB XOR the input bit (C) is 1, XOR with the polynomial in Src

CRCBIT is typically used in a loop to process data one bit at a time:

```pasm
        mov     crc, #0               ' Initialize CRC
.loop   rcl     data, #1        wc    ' Get next bit into C
        crcbit  crc, poly             ' Update CRC with bit
        djnz    count, #.loop         ' Repeat for all bits
```

For processing nibbles (4 bits) at a time instead, use CRCNIB.



## CRCNIB {#crcnib}

CRC iterate nibble
[Math and Logic](#math-and-logic) - Iterate CRC value in D for a nibble using polynomial in S.

**CRCNIB**  *Dest, {#}Src*

---

**Result:** Dest is updated with CRC iterations for a nibble, and Q is shifted left by 4 bits.

- Dest is a register containing the current CRC value and is where the updated CRC is written.
- Src is a register or 9-bit literal containing the CRC polynomial.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001110 | 11I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [CRCBIT](#crcbit), [REV](#rev)

**Explanation:**

CRCNIB iterates the CRC value in Dest for a nibble (4 bits) using the polynomial in Src, and shifts the Q register left by 4 bits. This instruction accelerates CRC calculations by processing 4 bits per instruction instead of 1.

The instruction performs four CRC bit iterations in sequence, using the lowest 4 bits from Q as input bits (processed from LSB to MSB). After the operation, Q is shifted left by 4 bits, positioning the next nibble for processing.

The typical usage pattern is:

```pasm
        setq    data                  ' Load data into Q
        mov     crc, #0               ' Initialize CRC
.loop   crcnib  crc, poly             ' Process 4 bits from Q[3:0]
        ' Q is automatically shifted left by 4
        djnz    count, #.loop         ' Repeat for all nibbles
```

CRCNIB is more efficient than CRCBIT when processing byte-oriented data, providing a 4x speedup for CRC calculations. The automatic Q shift simplifies the loop logic for multi-nibble processing.



# Instructions: D

This section contains all PASM2 instructions beginning with the letter D.

<!-- DEBUG instruction removed - will be covered in a dedicated narrative chapter with examples -->



## DECMOD {#decmod}

Decrement modulus
[Math and Logic](#math-and-logic) - Decrement with modulus wrapping.

**DECMOD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** If Dest was not equal to 0, it is decremented by 1; otherwise Dest is reset to Src.

- Dest is a register containing the value to decrement down to 0 with modulus, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is the modulus limit to apply to Dest's decrement operation.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111001 | CZI | DDDDDDDDD | SSSSSSSSS | D | Modulus triggered | Result = 0 | 2 |


**Related:** [INCMOD](#incmod)

**Explanation:**

DECMOD compares Dest with 0—if not equal, it decrements Dest; otherwise it sets Dest equal to Src. If Dest begins in the range 0 to Src, iterations of DECMOD will decrement Dest repetitively from Src to 0.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was equal to 0 and subsequently reset to Src, or is cleared (0) if not reset. This indicates that the modulus wrapping occurred.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or is cleared (0) if it is non-zero.

DECMOD does not limit Dest within the specified range—if Dest begins as greater than Src, iterations will continue to decrement it down through Src before cycling from Src to 0. This instruction is useful for implementing circular buffers and modular counters that wrap from 0 back to a maximum value.



## DECOD {#decod}

Decode bit position to single-bit mask
[Math and Logic](#math-and-logic) - Decode value (0-31) into single-high-bit long.

**DECOD**  *Dest, {#}Src*
**DECOD**  *Dest*

---

**Result:** A 32-bit value, with the bit position corresponding to Src or Dest value (0-31) set high, is stored in Dest.

- Dest is the register in which to store the decoded value and optionally begins by containing the 5-bit bit position value it is requesting (syntax 2).
- Src is an optional register or 5-bit literal whose value is the bit position to set high in the decoded value.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001110 | 00I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001110 | 000 | DDDDDDDDD | DDDDDDDDD | D | --- | --- | 2 |


**Related:** [ENCOD](#encod), [BMASK](#bmask)

**Explanation:**

DECOD generates a 32-bit value with just one bit high, corresponding to the Src or Dest value (0-31) and stores that result in Dest. In effect, Dest becomes %1 << value via the DECOD instruction, where value is Src[4:0] or Dest[4:0].

Examples of decoded values:
- A value of 0 generates %00000000_00000000_00000000_00000001
- A value of 5 generates %00000000_00000000_00000000_00100000
- A value of 15 generates %00000000_00000000_10000000_00000000

The first syntax form uses Src to specify the bit position, while the second syntax form uses Dest[4:0] as both the input bit position and the destination for the result.

DECOD is the complement of ENCOD. It is commonly used to generate bit masks for testing or setting individual bits within registers or memory locations.



## DIRC / DIRNC {#dirc}

Set pin direction if C / not C
[Pin](#pin) - Set pin(s) direction to input/output according to C or !C.

**DIRC**  *{#}Dest*  **{WCZ}**
**DIRNC**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin direction bit(s), described by Dest, are set to output/input according to C or !C; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output or input.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000010 | DIRx | --- | DIR bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000011 | DIRx | --- | DIR bit | 2 |


**Related:** [DIRZ](#dirz), [DIRNZ](#dirnz), [DIRL](#dirl), [DIRH](#dirh), [DIRNOT](#dirnot), [DIRRND](#dirrnd)

**Explanation:**

DIRC or DIRNC alters the direction register's bit(s) designated by Dest to equal the state, or inverse state, of the C flag. All other bits are left unchanged.

DIRC sets the pin(s) to the direction indicated by the C flag: high (1) sets the pin(s) to output, low (0) to input. DIRNC inverts this relationship, setting the pin(s) according to the inverse of the C flag (!C).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRC or DIRNC instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRC or DIRNC's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



## DIRH {#dirh}

Set pin direction high
[Pin](#pin) - Set pin(s) direction to output (high; 1).

**DIRH**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to output direction; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000001 | DIRx | --- | DIR bit | 2 |


**Related:** [DIRL](#dirl), [DIRC](#dirc), [DIRNC](#dirnc), [DIRZ](#dirz), [DIRNZ](#dirnz)

**Explanation:**

DIRH sets the direction register's bit(s) designated by Dest to high (1), making the pin(s) outputs. All other direction bits are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

If the WCZ effect is specified, the Z flag is set to the state of the direction bit before modification.



## DIRL {#dirl}

Set pin direction low
[Pin](#pin) - Set pin(s) direction to input (low; 0).

**DIRL**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to input direction; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to input.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000000 | DIRx | --- | DIR bit | 2 |


**Related:** [DIRH](#dirh), [DIRC](#dirc), [DIRNC](#dirnc), [DIRZ](#dirz), [DIRNZ](#dirnz)

**Explanation:**

DIRL alters the direction register's bit(s) designated by Dest to be low (0), setting the I/O pin(s) to input mode. The rest of the direction bits are left as-is.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

If the WCZ effect is specified, the Z flag is updated to the original state of the target direction bit.



## DIRNOT {#dirnot}

Direction not
[Pin](#pin) - Toggle pin(s) to the opposite direction.

**DIRNOT**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin direction bit(s), described by Dest, are toggled to their opposite state(s); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to toggle to the opposite direction.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000111 | DIRx | --- | DIR bit | 2 |


**Related:** [DIRRND](#dirrnd), [DIRL](#dirl), [DIRH](#dirh), [DIRC](#dirc), [DIRNC](#dirnc), [DIRZ](#dirz), [DIRNZ](#dirnz)

**Explanation:**

DIRNOT alters the direction register's bit(s) designated by Dest to their inverse state. All other bits are left unchanged. Pins that were outputs become inputs, and pins that were inputs become outputs.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRNOT instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRNOT's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



## DIRZ / DIRNZ {#dirz}

Set pin direction if Z / not Z
[Pin](#pin) - Set pin(s) direction to input/output according to Z or !Z.

**DIRZ**  *{#}Dest*  **{WCZ}**
**DIRNZ**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin direction bit(s), described by Dest, are set to output/input according to Z or !Z; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output or input.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000100 | DIRx | --- | DIR bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000101 | DIRx | --- | DIR bit | 2 |


**Related:** [DIRC](#dirc), [DIRNC](#dirnc), [DIRNOT](#dirnot), [DIRRND](#dirrnd), [DIRL](#dirl), [DIRH](#dirh)

**Explanation:**

DIRZ or DIRNZ alters the direction register's bit(s) designated by Dest to equal the state, or inverse state, of the Z flag. All other bits are left unchanged.

DIRZ sets the pin(s) to the direction indicated by the Z flag: high (1) sets the pin(s) to output, low (0) to input. DIRNZ inverts this relationship, setting the pin(s) according to the inverse of the Z flag (!Z).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRZ or DIRNZ instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRZ or DIRNZ's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest.



## DIRRND {#dirrnd}

Direction random
[Pin](#pin) - Set pin(s) direction to random input/output.

**DIRRND**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin direction bit(s), described by Dest, are each set randomly low or high (input or output); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set randomly to input or output.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000110 | DIRx | Original DIRx base bit | Original DIRx base bit | 2 |


**Related:** [DIRC](#dirc), [DIRNC](#dirnc), [DIRZ](#dirz), [DIRNZ](#dirnz), [DIRNOT](#dirnot), [DIRL](#dirl), [DIRH](#dirh)

**Explanation:**

DIRRND alters the direction register's bit(s) designated by Dest to be random low and high (input and output), based on bit(s) from the Xoroshiro128** PRNG. All other bits are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DIRRND instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DIRRND's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of DIRA / DIRB's base bit, identified by Dest, before the random modification occurs.



## DJF {#djf}

Decrement and jump if full
[Branch](#branch) - Decrement value and jump if full (-1; $FFFF_FFFF).

**DJF**  *Dest, {#}Src*

---

**Result:** Dest is decremented. If the result equals $FFFF_FFFF (full), PC is set to a new relative (#Src) or absolute (Src) address; otherwise execution continues with the next instruction.

- Dest is a register whose value is decremented and tested for full or not full.
- Src is a register, 9-bit literal, or 20-bit augmented literal whose value is the absolute or relative address to set PC to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011011 | 10I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 or 4 |


**Related:** [DJNF](#djnf), [DJZ](#djz), [DJNZ](#djnz)

**Explanation:**

DJF decrements the value in Dest, writes the result, and jumps to the address described by Src if the result is full ($FFFF_FFFF, or -1 signed).

This instruction is useful for implementing loops that count down until a register wraps from 0 to -1. Use # prefix on Src for relative addressing; omit # for absolute addressing.

The instruction executes in 2 clock cycles when the branch is not taken, and 4 clock cycles when the branch is taken.



## DJNF {#djnf}

Decrement and jump if not full
[Branch](#branch) - Decrement value and jump if not full (<> -1; <> $FFFF_FFFF).

**DJNF**  *Dest, {#}Src*

---

**Result:** Dest is decremented. If the result does NOT equal $FFFF_FFFF (not full), PC is set to a new relative (#Src) or absolute (Src) address; otherwise execution continues with the next instruction.

- Dest is a register whose value is decremented and tested for full or not full.
- Src is a register, 9-bit literal, or 20-bit augmented literal whose value is the absolute or relative address to set PC to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011011 | 11I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 or 4 |


**Related:** [DJF](#djf), [DJZ](#djz), [DJNZ](#djnz)

**Explanation:**

DJNF decrements the value in Dest, writes the result, and jumps to the address described by Src if the result is NOT full (not equal to $FFFF_FFFF).

This instruction is useful for implementing loops that continue until a register wraps from 0 to -1 (full). Use # prefix on Src for relative addressing; omit # for absolute addressing.

Dest is always written with the decremented value. PC is written only when the result in Dest is not full.

The instruction executes in 2 clock cycles when the branch is not taken, and 4 clock cycles when the branch is taken.



## DJZ / DJNZ {#djz}

Decrement and jump if zero / not zero {#djnz}
[Branch](#branch) - Decrement a register and jump based on zero/non-zero result.

**DJZ**  *Dest, {#}Src*
**DJNZ**  *Dest, {#}Src*

---

**Result:** Dest is decremented by 1, and conditionally jumps:

| Instruction | Jumps when |
|-------------|------------|
| DJZ | Result = 0 |
| DJNZ | Result ≠ 0 |

- Dest is a register whose value is decremented and tested.
- Src is the jump address: use # for relative, omit for absolute.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011011 | 00I | DDDDDDDDD | SSSSSSSSS | D + PC* | --- | --- | 2 or 4 |
| EEEE | 1011011 | 01I | DDDDDDDDD | SSSSSSSSS | D + PC* | --- | --- | 2 or 4 |

```{=latex}
*PC is written only when the jump condition is met.
```


**Related:** [DJF](#djf), [DJNF](#djnf), [IJZ](#ijz), [IJNZ](#ijnz), [TJZ](#tjz), [TJNZ](#tjnz)

**Explanation:**

DJZ and DJNZ decrement Dest and conditionally jump based on whether the result is zero or non-zero.

DJNZ is one of the most commonly used loop instructions—it continues looping while the counter is non-zero.

Example loop:
```pasm
        mov     count, #10              ' Set loop counter to 10
.loop   ' loop body here
        djnz    count, #.loop           ' Decrement and loop if not zero
```

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



## DRVC / DRVNC {#drvc}

Drive pins if C / not C
[Pin](#pin) - Set pin(s) direction to output and output level to low/high according to C or !C.

**DRVC**  *{#}Dest*  **{WCZ}**
**DRVNC**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low/high according to C or !C; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and output levels of low or high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011010 | DIRx* + OUTx | --- | OUT bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011011 | DIRx* + OUTx | --- | OUT bit | 2 |


**Related:** [DRVZ](#drvz), [DRVNZ](#drvnz), [DRVH](#drvh), [DRVL](#drvl), [DRVNOT](#drvnot), [DRVRND](#drvrnd)

**Explanation:**

DRVC or DRVNC sets the I/O pin(s) designated by Dest to the output direction and to a low/high output level according to the C flag or its inverse (!C). All other pins are left unchanged.

DRVC sets the pin(s) to the output direction and to the level indicated by the C flag: high (1) for high output, low (0) for low output. DRVNC inverts this relationship, setting the output level according to the inverse of the C flag (!C).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the state of the OUT bit before modification.



## DRVH {#drvh}

Drive pins high
[Pin](#pin) - Set pin(s) direction to output and output level high (1).

**DRVH**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of high; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and high output level.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011001 | DIRx* + OUTx | --- | OUT bit | 2 |


**Related:** [DRVL](#drvl), [DRVC](#drvc), [DRVNC](#drvnc), [DRVZ](#drvz), [DRVNZ](#drvnz)

**Explanation:**

DRVH sets the I/O pin(s) designated by Dest to the output direction and to a high output level. All other pins are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the state of the OUT bit before modification.



## DRVL {#drvl}

Drive pins low
[Pin](#pin) - Set pin(s) direction to output and output level low (0).

**DRVL**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and low output level.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011000 | DIRx* + OUTx | --- | OUT bit | 2 |


**Related:** [DRVH](#drvh), [DRVC](#drvc), [DRVNC](#drvnc), [DRVZ](#drvz), [DRVNZ](#drvnz)

**Explanation:**

DRVL sets the I/O pin(s) designated by Dest to the output direction and to a low output level. All other pins are left unchanged.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the state of the OUT bit before modification.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.



## DRVNOT {#drvnot}

Drive not
[Pin](#pin) - Set pin(s) direction to output and toggle to the opposite output level.

**DRVNOT**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to their opposite output level(s); the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the output direction and toggle to opposite output levels.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011111 | DIRx* + OUTx | --- | OUT bit | 2 |


**Related:** [DRVRND](#drvrnd), [DRVH](#drvh), [DRVL](#drvl), [DRVC](#drvc), [DRVNC](#drvnc), [DRVZ](#drvz), [DRVNZ](#drvnz)

**Explanation:**

DRVNOT sets the I/O pin(s) designated by Dest to the output direction and toggles their output level(s) to the opposite state. All other pins are left unchanged. This instruction achieves the same effect as two instructions—OUTNOT followed by DIRH.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DRVNOT instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DRVNOT's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB and OUTA or OUTB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA / OUTB's base bit, identified by Dest.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.



## DRVZ / DRVNZ {#drvz}

Drive pins if Z / not Z
[Pin](#pin) - Set pin(s) direction to output and output level to low/high according to Z or !Z.

**DRVZ**  *{#}Dest*  **{WCZ}**
**DRVNZ**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the output direction and to an output level of low/high according to Z or !Z; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to output direction and output levels of low or high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011100 | DIRx* + OUTx | --- | OUT bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011101 | DIRx* + OUTx | --- | OUT bit | 2 |


**Related:** [DRVC](#drvc), [DRVNC](#drvnc), [DRVH](#drvh), [DRVL](#drvl), [DRVNOT](#drvnot), [DRVRND](#drvrnd)

**Explanation:**

DRVZ or DRVNZ sets the I/O pin(s) designated by Dest to the output direction and to a low/high output level according to the Z flag or its inverse (!Z). All other pins are left unchanged.

DRVZ sets the pin(s) to the output direction and to the level indicated by the Z flag: high (1) for high output, low (0) for low output. DRVNZ inverts this relationship, setting the output level according to the inverse of the Z flag (!Z).

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group; it will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the state of the OUT bit before modification.



## DRVRND {#drvrnd}

Drive random
[Pin](#pin) - Set pin(s) direction to output and output level to random low/high.

**DRVRND**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the output direction and each output level is set randomly low or high; the rest are left as-is.

- Dest is the register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the output direction and with output level(s) set randomly to low or high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001011110 | DIRx + OUTx | Original OUTx base bit | Original OUTx base bit | 2 |


**Related:** [DRVH](#drvh), [DRVL](#drvl), [DRVC](#drvc), [DRVNC](#drvnc), [DRVZ](#drvz), [DRVNZ](#drvnz), [DRVNOT](#drvnot)

**Explanation:**

DRVRND sets the I/O pin(s) designated by Dest to the output direction and with output level(s) set randomly low and high, based on bit(s) from the Xoroshiro128** PRNG. All other pins are left unchanged. This instruction can affect one or more of the bits within the DIRA or DIRB and OUTA or OUTB registers.

DRVRND achieves the same effect as two instructions—OUTRND followed by DIRH.

Dest[5:0] indicates the pin number (0-63). For a range of pins, Dest[5:0] indicates the base pin number (0-63) and Dest[10:6] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest[5:0]) and a range of up to 8 contiguous pins (Dest[8:6]). If needed, use the augmented literal feature (##Dest) to augment Dest to an 11-bit literal value—this inserts an AUGD instruction prior.

When Dest is a register, the register's value bits [10:0] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the DRVRND instruction; substituting SETQ's Dest[4:0] in place of value bits[10:6], for DRVRND's use.

The range calculation (from Dest[5:0] up to Dest[5:0]+Dest[10:6]) will wrap within the same 32-pin group (DIRA or DIRB and OUTA or OUTB); it will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA / OUTB's base bit, identified by Dest, before the random modification occurs.

Note that the new DIRx state is not data-forwarded; the next pipelined instruction sees the old state.



# Instructions: E

This section contains all PASM2 instructions beginning with the letter E.



## ENCOD {#encod}

Encode
[Math and Logic](#math-and-logic) - Get bit position of top-most 1 of Src or Dest into Dest.

**ENCOD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**ENCOD**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The bit position value of the top-most high bit (1) in Src, or Dest, is stored in Dest.

- Dest is a register in which to store the encoded bit position value and optionally contains the 32-bit value to encode (syntax 2).
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is to be encoded into a bit position.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111100 | CZI | DDDDDDDDD | SSSSSSSSS | D | S != 0 | Result = 0 | 2 |
| EEEE | 0111100 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | Original D != 0 | Result = 0 | 2 |


**Related:** [DECOD](#decod)

**Explanation:**

ENCOD stores the bit position value (0-31) of the top-most high bit (1) of Src, or Dest, into Dest. The instruction scans from the most significant bit (bit 31) down to the least significant bit (bit 0) and returns the position of the first 1 bit encountered.

If the WC or WCZ effect is specified, the C flag is set (1) if Src (or original Dest in syntax 2) was not zero, or is cleared (0) if it was zero. This allows distinguishing between an input value of 1 (which encodes to 0) versus an input value of 0 (which also produces a result of 0).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if not zero.

For example:
- `%00000000_00000000_00000000_00000001` encodes to 0 (bit position of the only 1)
- `%00000000_00000000_00000000_00100000` encodes to 5 (bit position 5 is the top-most 1)
- `%00000000_00000000_10000001_01000000` encodes to 15 (bit position 15 is the top-most 1)
- `%00000000_00000000_00000000_00000000` encodes to 0 with C flag cleared to 0

If the value to encode may be 0, use the WC or WCZ effect and check the resulting C flag to distinguish between the cases of input = 1 versus input = 0. Without this flag check, both cases would produce a Dest value of 0.

ENCOD is the complement of DECOD. Where DECOD converts a bit position (0-31) into a 32-bit value with a single bit set, ENCOD performs the reverse operation, converting a 32-bit value into the position of its highest set bit.



## EXECF {#execf}

Call and skip
[Branch](#branch) - Jump to address in COG/LUT and set SKIPF pattern.

**EXECF**  *{#}Dest*

---

**Result:** PC is set to Dest[9:0] and the SKIPF pattern is set to Dest[31:10].

- Dest is a register or 10-bit literal specifying the target address in bits [9:0] and the skip pattern in bits [31:10].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00I | DDDDDDDDD | 000110011 | --- | --- | --- | 4 |


**Related:** [CALL](#call), [SKIPF](#skipf), [SKIP](#skip)

**Explanation:**

EXECF performs a combined jump and skip pattern operation. The instruction sets the program counter (PC) to the 10-bit address specified in Dest[9:0] and simultaneously loads the SKIPF pattern register with the value from Dest[31:10].

The PC is set to the address formed by zero-extending Dest[9:0] to create a COG/LUT address: PC = {10'b0, Dest[9:0]}. This allows jumping to any location within the 1024-address COG/LUT memory space (addresses 0-511 for COG, 512-1023 for LUT).

The SKIPF pattern in Dest[31:10] provides a 22-bit pattern that controls which subsequent instructions will be skipped after the jump. Like SKIPF, this allows the PC to leap over instructions rather than cancelling them, providing fast conditional execution without the overhead of traditional branch instructions.

EXECF combines the functionality of CALL (jumping to a new address) and SKIPF (setting a skip pattern), enabling efficient implementation of computed branches with conditional execution. This is particularly useful for jump tables and state machines where both the target address and subsequent execution pattern need to be determined dynamically.

The instruction takes 4 clock cycles to execute, regardless of whether it executes from COG/LUT or Hub memory.



# Instructions: F

This section contains all PASM2 instructions beginning with the letter F.



## FBLOCK {#fblock}

Set next block for when block wraps
[Hub FIFO](#hub-fifo) - Configure the next Hub memory block for FIFO wraparound.

**FBLOCK**  *{#}Dest, {#}Src*

---

**Result:** The next block parameters are configured for FIFO wraparound operations.

- Dest is a register or 9-bit literal whose value specifies the block size in 64-byte units (0 = maximum size).
- Src is a register or 9-bit literal whose value specifies the block start address in Hub memory.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100100 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [RDFAST](#rdfast), [WRFAST](#wrfast), [RFLONG](#rflong), [WFLONG](#wflong)

**Explanation:**

FBLOCK configures the parameters for the next Hub FIFO block that will be used when the current block wraps around. This instruction is used to set up circular buffering in Hub memory for streaming read and write operations.

Dest\[13:0\] specifies the block size in 64-byte units. A value of 0 represents the maximum block size. The block size determines how many bytes can be transferred before the FIFO wraps to the beginning of the block.

Src\[19:0\] specifies the starting address of the block in Hub memory. This address marks where the FIFO will wrap to when it reaches the end of the current block.

FBLOCK is typically used in conjunction with RDFAST/WRFAST for setting up high-throughput data streaming between Hub memory and COG/LUT memory. The block configuration takes effect when the current FIFO operation completes and wraps around.



## FGE {#fge}

Force greater or equal
[Math and Logic](#math-and-logic) - Force unsigned value to be greater than or equal to another.

**FGE**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Unsigned Dest is set to unsigned Src if Dest was less than Src.

- Dest is a register containing the unsigned value to limit to a minimum of unsigned Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose unsigned value is the lower limit to force upon Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011000 | CZI | DDDDDDDDD | SSSSSSSSS | D | limit enforced | Result = 0 | 2 |


**Related:** [FLE](#fle), [FGES](#fges), [FLES](#fles)

**Explanation:**

FGE sets unsigned Dest to unsigned Src if Dest is less than Src. This is a limit minimum function that prevents Dest from sinking below the value of Src. If Dest is already greater than or equal to Src, Dest remains unchanged.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was limited (Dest was less than Src and is now equal to Src), or is cleared (0) if not limited (Dest was already greater than or equal to Src).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

FGE is useful for clamping values to a minimum threshold, ensuring that a value never falls below a specified floor. This is commonly used in digital signal processing, graphics calculations, and boundary checking where values must stay within valid ranges.



## FGES {#fges}

Force greater or equal, signed
[Math and Logic](#math-and-logic) - Force signed value to be greater than or equal to another.

**FGES**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Signed Dest is set to signed Src if Dest was less than Src.

- Dest is a register containing the signed value to limit to a minimum of signed Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose signed value is the lower limit to force upon Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011010 | CZI | DDDDDDDDD | SSSSSSSSS | D | limit enforced | Result = 0 | 2 |


**Related:** [FLES](#fles), [FGE](#fge), [FLE](#fle)

**Explanation:**

FGES sets signed Dest to signed Src if Dest is less than Src. This is a limit minimum function that prevents Dest from sinking below the signed value of Src. If Dest is already greater than or equal to Src, Dest remains unchanged. The comparison and limiting are performed treating both operands as signed 32-bit values.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was limited (Dest was less than Src and is now equal to Src), or is cleared (0) if not limited (Dest was already greater than or equal to Src).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

FGES is the signed counterpart to FGE and is used when working with signed values that need to be clamped to a minimum threshold. This is particularly useful in audio processing, control systems, and any application where signed values must be constrained within bounds.



## FLE {#fle}

Force lesser or equal
[Math and Logic](#math-and-logic) - Force unsigned value to be less than or equal to another.

**FLE**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Unsigned Dest is set to unsigned Src if Dest was greater than Src.

- Dest is a register containing the unsigned value to limit to a maximum of unsigned Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose unsigned value is the upper limit to force upon Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011001 | CZI | DDDDDDDDD | SSSSSSSSS | D | limit enforced | Result = 0 | 2 |


**Related:** [FGE](#fge), [FLES](#fles), [FGES](#fges)

**Explanation:**

FLE sets unsigned Dest to unsigned Src if Dest is greater than Src. This is a limit maximum function that prevents Dest from rising above the value of Src. If Dest is already less than or equal to Src, Dest remains unchanged.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was limited (Dest was greater than Src and is now equal to Src), or is cleared (0) if not limited (Dest was already less than or equal to Src).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

FLE is useful for clamping values to a maximum threshold, ensuring that a value never exceeds a specified ceiling. This is commonly used in digital signal processing, graphics calculations, and boundary checking where values must stay within valid ranges.



## FLES {#fles}

Force lesser or equal, signed
[Math and Logic](#math-and-logic) - Force signed value to be less than or equal to another.

**FLES**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Signed Dest is set to signed Src if Dest was greater than Src.

- Dest is a register containing the signed value to limit to a maximum of signed Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose signed value is the upper limit to force upon Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011011 | CZI | DDDDDDDDD | SSSSSSSSS | D | limit enforced | Result = 0 | 2 |


**Related:** [FGES](#fges), [FLE](#fle), [FGE](#fge)

**Explanation:**

FLES sets signed Dest to signed Src if Dest is greater than Src. This is a limit maximum function that prevents Dest from rising above the signed value of Src. If Dest is already less than or equal to Src, Dest remains unchanged. The comparison and limiting are performed treating both operands as signed 32-bit values.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was limited (Dest was greater than Src and is now equal to Src), or is cleared (0) if not limited (Dest was already less than or equal to Src).

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

FLES is the signed counterpart to FLE and is used when working with signed values that need to be clamped to a maximum threshold. This is particularly useful in audio processing, control systems, and any application where signed values must be constrained within bounds.



## FLTC / FLTNC / FLTZ / FLTNZ {#fltc}

Float with output preset by flag {#fltnc} {#fltz} {#fltnz}
[Pin](#pin) - Set pin(s) to input direction with output preset according to C, NC, Z, or NZ flag.

**FLTC**  *{#}Dest*  **{WCZ}**
**FLTNC**  *{#}Dest*  **{WCZ}**
**FLTZ**  *{#}Dest*  **{WCZ}**
**FLTNZ**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins are set to input direction with output preset according to flag state:

| Instruction | Presets output high when |
|-------------|--------------------------|
| FLTC | C = 1 |
| FLTNC | C = 0 |
| FLTZ | Z = 1 |
| FLTNZ | Z = 0 |

- Dest identifies the I/O pin(s): Dest[5:0] = base pin (0-63), Dest[10:6] = additional contiguous pins.
- WCZ is an optional effect to set Z to the original output state.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010010 | DIRx + OUTx | --- | OUT bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010011 | DIRx + OUTx | --- | OUT bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010100 | DIRx + OUTx | --- | OUT bit | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010101 | DIRx + OUTx | --- | OUT bit | 2 |


**Related:** [FLTH](#flth), [FLTL](#fltl), [FLTNOT](#fltnot), [FLTRND](#fltrnd)

**Explanation:**

These instructions set pin(s) to input direction (floating) while pre-setting the output register based on flag state. When the pin is later driven as output, it will immediately be at the desired level.

FLTC and FLTZ preset output high when their flag is set; FLTNC and FLTNZ preset output high when their flag is clear.

If WCZ is specified, the Z flag is set to the original output state of the base pin.



## FLTH {#flth}

Float high
[Pin](#pin) - Set pin(s) direction to input and to an output level of high.

**FLTH**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the input direction and to an output level of high.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to input direction and output level of high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010001 | DIRx + OUTx | --- | OUT bit | 2 |


**Related:** [FLTL](#fltl), [FLTC](#fltc), [FLTNC](#fltnc), [FLTZ](#fltz), [FLTNZ](#fltnz)

**Explanation:**

FLTH sets the I/O pin(s) designated by Dest to the input direction (floating) and to a high output level. All other pins are left unchanged. This pre-sets the output register so that when the pin is later driven as output, it will immediately be high.

Dest\[5:0\] indicates the pin number (0-63). For a range of pins, Dest\[5:0\] indicates the base pin number (0-63) and Dest\[10:6\] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest\[5:0\]) and a range of up to 8 contiguous pins (Dest\[8:6\]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value, which inserts an AUGD instruction prior.

The range calculation (from Dest\[5:0\] up to Dest\[5:0\]+Dest\[10:6\]) wraps within the same 32-pin group and will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the original state of the OUTA/OUTB base bit identified by Dest.



## FLTL {#fltl}

Float low
[Pin](#pin) - Set pin(s) direction to input and to an output level of low.

**FLTL**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the input direction and to an output level of low.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to input direction and output level of low.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010000 | DIRx + OUTx | --- | OUT bit | 2 |


**Related:** [FLTH](#flth), [FLTC](#fltc), [FLTNC](#fltnc), [FLTZ](#fltz), [FLTNZ](#fltnz)

**Explanation:**

FLTL sets the I/O pin(s) designated by Dest to the input direction (floating) and to a low output level. All other pins are left unchanged. This pre-sets the output register so that when the pin is later driven as output, it will immediately be low.

Dest\[5:0\] indicates the pin number (0-63). For a range of pins, Dest\[5:0\] indicates the base pin number (0-63) and Dest\[10:6\] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest\[5:0\]) and a range of up to 8 contiguous pins (Dest\[8:6\]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value, which inserts an AUGD instruction prior.

The range calculation (from Dest\[5:0\] up to Dest\[5:0\]+Dest\[10:6\]) wraps within the same 32-pin group and will not cross the port boundary.

If the WCZ effect is specified, the Z flag is set to the original state of the OUTA/OUTB base bit identified by Dest.



## FLTNOT {#fltnot}

Float not
[Pin](#pin) - Set pin(s) direction to input and toggle to the opposite output level.

**FLTNOT**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the input direction and to their opposite output level(s).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the input direction and toggle to opposite output levels.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010111 | DIRx + OUTx | --- | OUT bit | 2 |


**Related:** [FLTC](#fltc), [FLTNC](#fltnc), [FLTZ](#fltz), [FLTNZ](#fltnz), [FLTRND](#fltrnd)

**Explanation:**

FLTNOT sets the I/O pin(s) designated by Dest to the input direction (floating) and toggles their output level(s) to the opposite state. All other pins are left unchanged. FLTNOT achieves the same effect as two instructions: DIRL followed by OUTNOT.

Dest\[5:0\] indicates the pin number (0-63). For a range of pins, Dest\[5:0\] indicates the base pin number (0-63) and Dest\[10:6\] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest\[5:0\]) and a range of up to 8 contiguous pins (Dest\[8:6\]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value, which inserts an AUGD instruction prior.

When Dest is a register, the register's value bits \[10:0\] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the FLTNOT instruction, in which case SETQ's Dest\[4:0\] substitutes in place of value bits\[10:6\] for FLTNOT's use.

The range calculation (from Dest\[5:0\] up to Dest\[5:0\]+Dest\[10:6\]) wraps within the same 32-pin group (DIRA or DIRB and OUTA or OUTB) and will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA/OUTB's base bit identified by Dest.



## FLTRND {#fltrnd}

Float random
[Pin](#pin) - Set pin(s) direction to input and to an output level of random low/high.

**FLTRND**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pins described by Dest are set to the input direction and each output level is set randomly low or high.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to the input direction and with output level(s) set randomly to low or high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001010110 | DIRx + OUTx | Original OUTx base bit | Original OUTx base bit | 2 |


**Related:** [FLTC](#fltc), [FLTNC](#fltnc), [FLTZ](#fltz), [FLTNZ](#fltnz), [FLTH](#flth), [FLTL](#fltl), [FLTNOT](#fltnot)

**Explanation:**

FLTRND sets the I/O pin(s) designated by Dest to the input direction and with output level(s) set randomly low and high, based on bit(s) from the Xoroshiro128\*\* PRNG. All other pins are left unchanged. This instruction can affect one or more of the bits within the DIRA or DIRB and OUTA or OUTB registers.

FLTRND achieves the same effect as two instructions: DIRL followed by OUTRND.

Dest\[5:0\] indicates the pin number (0-63). For a range of pins, Dest\[5:0\] indicates the base pin number (0-63) and Dest\[10:6\] indicates how many contiguous pins beyond the base should be affected (1-31).

A 9-bit literal Dest is enough to express the base pin (Dest\[5:0\]) and a range of up to 8 contiguous pins (Dest\[8:6\]). If needed, use the augmented literal feature (\#\#Dest) to augment Dest to an 11-bit literal value, which inserts an AUGD instruction prior.

When Dest is a register, the register's value bits \[10:0\] are used as-is to form the 11-bit ID range, unless a SETQ instruction immediately precedes the FLTRND instruction, in which case SETQ's Dest\[4:0\] substitutes in place of value bits\[10:6\] for FLTRND's use.

The range calculation (from Dest\[5:0\] up to Dest\[5:0\]+Dest\[10:6\]) wraps within the same 32-pin group (DIRA or DIRB and OUTA or OUTB) and will not cross the port boundary.

If the WCZ effect is specified, the C and Z flags are updated to the original state of OUTA/OUTB's base bit identified by Dest.




# Instructions: G

This section contains all PASM2 instructions beginning with the letter G.



## GETBRK {#getbrk}

Get breakpoint status
[Miscellaneous](#miscellaneous) - Get breakpoint/cog status into D according to WC/WZ/WCZ.

**GETBRK**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Breakpoint or COG status information is retrieved into Dest based on the flag effect specified.

- Dest is a register where the status information is written.
- WC, WZ, or WCZ are optional effects that determine which status information is retrieved.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000110101 | D | --- | --- | 2 |


**Related:** [BRK](#brk), [SETBRK](#setbrk), [COGBRK](#cogbrk)

**Explanation:**

GETBRK retrieves various breakpoint and COG status information into the Dest register. The specific information retrieved depends on which flag effect is specified.

When the WCZ effect is specified, GETBRK retrieves the full 32-bit ISR call address into Dest. This is the address where the debug interrupt service routine will resume execution after handling the breakpoint.

When the WC effect is specified, GETBRK retrieves the 8-bit COG ID into Dest[7:0]. This identifies which COG triggered the breakpoint, useful in multi-COG debugging scenarios where a debug ISR needs to determine the calling COG.

When the WZ effect is specified, GETBRK retrieves the 8-bit breakpoint code into Dest[7:0]. This code was set by the BRK instruction and can be used for conditional breakpoint handling or to distinguish between different types of breakpoints.

When no flag effects are specified, GETBRK retrieves the 16-bit skip pattern into Dest[15:0]. This pattern is used with the SKIPF instruction to selectively execute or skip subsequent instructions, typically within an ISR context.

GETBRK is essential for implementing debug infrastructure and coordinating multi-COG debugging systems. It works in conjunction with BRK and SETBRK to provide comprehensive breakpoint support.



## GETBYTE {#getbyte}

Get byte
[Math and Logic](#math-and-logic) - Get a byte from a value.

**GETBYTE**  *Dest, {#}Src, #Num*
**GETBYTE**  *Dest*

---

**Result:** Byte Num (0-3) of Src, or a byte from a source described by prior ALTGB instruction, is written to Dest.

- Dest is the register in which to store the byte.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value contains the target byte to read.
- Num is a 2-bit literal identifying the byte ID (0-3) of Src to read.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1000111 | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1000111 | 000 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ALTGB](#altgb), [GETNIB](#getnib), [GETWORD](#getword), [SETBYTE](#setbyte), [ROLBYTE](#rolbyte)

**Explanation:**

GETBYTE reads the byte identified by Num (0-3) from Src and writes it to Dest. The Num parameter identifies which of the four bytes in the 32-bit value to extract, numbered in least-significant byte order.

Num 0 selects bits [7:0], Num 1 selects bits [15:8], Num 2 selects bits [23:16], and Num 3 selects bits [31:24]. The extracted byte is zero-extended to 32 bits when written to Dest.

The second syntax form (GETBYTE Dest) is intended for use after an ALTGB instruction. This form is useful in loops that iteratively read a series of byte values from contiguous long registers. The ALTGB instruction modifies the subsequent GETBYTE instruction's source register and byte index automatically, enabling efficient sequential byte extraction without explicitly specifying the source and index on each iteration.



## GETCT {#getct}

Get system counter
[Miscellaneous](#miscellaneous) - Get the current system counter value into D.

**GETCT**  *Dest*  **{WC}**

---

**Result:** The current value of the system counter CT is written to Dest.

- Dest is a register where the system counter value is written.
- WC is an optional effect that preserves the current C flag state.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C00 | DDDDDDDDD | 000011010 | D | same | --- | 2 |


**Related:** [ADDCT1/2/3](instructions-a.md#addct1), [WAITCT1/2/3](instructions-w.md#waitct1)

**Explanation:**

GETCT retrieves the current value of the system counter CT into the Dest register. The system counter is a 32-bit counter that is reset to zero on system reset and increments by one on every clock cycle.

The CT counter provides a continuous, monotonic time reference that wraps around from $FFFF_FFFF to $0000_0000. This counter is shared across all COGs and provides the foundation for timing operations and synchronization.

If the WC effect is specified, the C flag is preserved and remains unchanged by this instruction. This allows GETCT to be used in sequences where the C flag state must be maintained across operations.

GETCT is commonly used with the ADDCT and WAITCT instruction families to implement precise timing, delays, and event scheduling. The retrieved counter value serves as a time reference for calculating future wait points or measuring elapsed time intervals.



## GETNIB {#getnib}

Get nibble
[Math and Logic](#math-and-logic) - Get a nibble from a value.

**GETNIB**  *Dest, {#}Src, #Num*
**GETNIB**  *Dest*

---

**Result:** Nibble Num (0-7) of Src, or a nibble from a source described by prior ALTGN instruction, is written to Dest.

- Dest is the register in which to store the nibble.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value contains the target nibble to read.
- Num is a 3-bit literal identifying the nibble ID (0-7) of Src to read.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 100001N | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1000010 | 000 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ALTGN](#altgn), [GETBYTE](#getbyte), [GETWORD](#getword), [SETNIB](#setnib), [ROLNIB](#rolnib)

**Explanation:**

GETNIB reads the nibble identified by Num (0-7) from Src and writes it to Dest. The Num parameter identifies which of the eight nibbles in the 32-bit value to extract, numbered in least-significant nibble order.

Num 0 selects bits [3:0], Num 1 selects bits [7:4], Num 2 selects bits [11:8], and so on up to Num 7 which selects bits [31:28]. The extracted nibble is zero-extended to 32 bits when written to Dest.

The second syntax form (GETNIB Dest) is intended for use after an ALTGN instruction. This form is useful in loops that iteratively read a series of nibble values from contiguous long registers. The ALTGN instruction modifies the subsequent GETNIB instruction's source register and nibble index automatically, enabling efficient sequential nibble extraction without explicitly specifying the source and index on each iteration.



## GETPTR {#getptr}

Get FIFO hub pointer
[Hub RAM](#hub-ram) - Get current FIFO hub pointer into D.

**GETPTR**  *Dest*

---

**Result:** The current FIFO hub pointer is written to Dest.

- Dest is a register where the FIFO hub pointer is written.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 000110100 | D | --- | --- | 2 |


**Related:** [RDFAST](#rdfast), [WRFAST](#wrfast), [RFBYTE](#rfbyte), [RFWORD](#rfword), [RFLONG](#rflong), [WFBYTE](#wfbyte), [WFWORD](#wfword), [WFLONG](#wflong)

**Explanation:**

GETPTR retrieves the current position of the hub FIFO pointer into the Dest register. This pointer tracks the current hub memory address for FIFO read and write operations initiated by RDFAST or WRFAST.

The hub FIFO pointer advances automatically as data is read from or written to the hub FIFO using the RFBYTE, RFWORD, RFLONG, WFBYTE, WFWORD, or WFLONG instructions. Each FIFO access increments the pointer by the size of the data transferred (1 byte, 2 bytes, or 4 bytes).

GETPTR is useful for monitoring FIFO transfer progress, calculating how much data has been transferred, or determining the current position within a buffer. The retrieved pointer value represents the hub memory address that will be accessed by the next FIFO read or write operation.



## GETQX {#getqx}

Get CORDIC X result
[CORDIC Solver](#cordic-solver) - Retrieve CORDIC result X into D.

**GETQX**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The CORDIC X result is written to Dest after waiting if necessary for the computation to complete.

- Dest is a register where the CORDIC X result is written.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000011000 | D | X[31] | Result = 0 | 2...58 |


**Related:** [GETQY](#getqy), [QROTATE](#qrotate), [QVECTOR](#qvector), [QMUL](#qmul), [QDIV](#qdiv), [QFRAC](#qfrac), [QSQRT](#qsqrt), [QLOG](#qlog), [QEXP](#qexp)

**Explanation:**

GETQX retrieves the X result from the CORDIC solver into the Dest register. If the CORDIC computation is not yet complete when GETQX executes, the instruction waits until the result is ready before retrieving it and continuing execution.

The CORDIC solver performs various mathematical operations including rotation, vectoring, multiplication, division, square root, logarithm, and exponentiation. Each operation produces two results, X and Y, which are retrieved using GETQX and GETQY respectively.

If the WC or WCZ effect is specified, the C flag is set to X[31], which is the sign bit of the result. This allows immediate determination of whether the result is negative (C = 1) or non-negative (C = 0) when interpreting the result as a signed value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

The timing for GETQX varies from 2 to 58 clock cycles depending on whether the result is immediately available or the instruction must wait for the CORDIC computation to complete. Most CORDIC operations complete in 54 clock cycles.



## GETQY {#getqy}

Get CORDIC Y result
[CORDIC Solver](#cordic-solver) - Retrieve CORDIC result Y into D.

**GETQY**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The CORDIC Y result is written to Dest after waiting if necessary for the computation to complete.

- Dest is a register where the CORDIC Y result is written.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000011001 | D | Y[31] | Result = 0 | 2...58 |


**Related:** [GETQX](#getqx), [QROTATE](#qrotate), [QVECTOR](#qvector), [QMUL](#qmul), [QDIV](#qdiv), [QFRAC](#qfrac), [QSQRT](#qsqrt), [QLOG](#qlog), [QEXP](#qexp)

**Explanation:**

GETQY retrieves the Y result from the CORDIC solver into the Dest register. If the CORDIC computation is not yet complete when GETQY executes, the instruction waits until the result is ready before retrieving it and continuing execution.

The CORDIC solver performs various mathematical operations including rotation, vectoring, multiplication, division, square root, logarithm, and exponentiation. Each operation produces two results, X and Y, which are retrieved using GETQX and GETQY respectively.

If the WC or WCZ effect is specified, the C flag is set to Y[31], which is the sign bit of the result. This allows immediate determination of whether the result is negative (C = 1) or non-negative (C = 0) when interpreting the result as a signed value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero.

The timing for GETQY varies from 2 to 58 clock cycles depending on whether the result is immediately available or the instruction must wait for the CORDIC computation to complete. Most CORDIC operations complete in 54 clock cycles.



## GETRND {#getrnd}

Get random value
[Miscellaneous](#miscellaneous) - Get RND into D or C/Z flags.

**GETRND**  *Dest*  **{WC|WZ|WCZ}**
**GETRND**  **{WC|WZ|WCZ}**

---

**Result:** The current pseudo-random value is written to Dest, or the random bits are stored in the C and Z flags.

- Dest is a register where the full 32-bit random value is written (first syntax).
- WC, WZ, or WCZ are optional effects to retrieve random bits into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000011011 | D | RND[31] | RND[30], unique per cog | 2 |
| EEEE | 1101011 | CZ1 | 000000000 | 000011011 | --- | RND[31] | RND[30], unique per cog | 2 |


**Related:** [SETQ](#setq), [SETQ2](#setq2)

**Explanation:**

GETRND retrieves the current value from the pseudo-random number generator (RNG) that is unique to each COG. Each COG maintains its own independent RNG state that advances continuously.

The first syntax form (GETRND Dest) writes the full 32-bit random value to the Dest register. This provides a complete random word for applications requiring random data, random seeds, or probabilistic algorithms.

The second syntax form (GETRND without Dest) is used when only random flag bits are needed. This form requires at least one flag effect to be specified, otherwise the instruction has no visible effect.

If the WC or WCZ effect is specified, the C flag is set to RND[31], which is the most significant bit of the current random value.

If the WZ or WCZ effect is specified, the Z flag is set to RND[30]. Notably, RND[30] is unique per COG, meaning each COG's RNG produces independent bit sequences at this position, useful for multi-COG systems requiring independent randomness.

The random number generator uses a maximal-length linear feedback shift register (LFSR) to produce a deterministic but statistically random sequence. The sequence repeats with a period of 2^32 - 1 values.



## GETSCP {#getscp}

Get oscilloscope samples
[Smart Pin](#smart-pin) - Get four-channel oscilloscope samples into D.

**GETSCP**  *Dest*

---

**Result:** Four 8-bit oscilloscope samples are written to Dest as D = {ch3[7:0], ch2[7:0], ch1[7:0], ch0[7:0]}.

- Dest is a register where the four oscilloscope samples are written.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001110001 | D | --- | --- | 2 |


**Related:** [SETSCP](#setscp), [RDPIN](#rdpin), [WXPIN](#wxpin)

**Explanation:**

GETSCP retrieves the current samples from the four-channel digital oscilloscope into the Dest register. The oscilloscope continuously samples four independent channels and packs the 8-bit sample values into a single 32-bit word.

The four samples are arranged in the Dest register with channel 0 in bits [7:0], channel 1 in bits [15:8], channel 2 in bits [23:16], and channel 3 in bits [31:24]. Each channel provides an 8-bit unsigned sample value ranging from 0 to 255.

The oscilloscope is configured using the SETSCP instruction to specify which pins or signals each channel monitors. Once configured, the oscilloscope continuously updates its samples based on the monitored signals, and GETSCP can retrieve the latest samples at any time.

This instruction is useful for real-time signal monitoring, debugging, and creating oscilloscope-like functionality for analyzing digital signals or pin states within the P2 system.



## GETWORD {#getword}

Get word
[Math and Logic](#math-and-logic) - Get a word from a value.

**GETWORD**  *Dest, {#}Src, #Num*
**GETWORD**  *Dest*

---

**Result:** Word Num (0-1) of Src, or a word from a source described by prior ALTGW instruction, is written to Dest.

- Dest is the register in which to store the word.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value contains the target word to read.
- Num is a 1-bit literal identifying the word ID (0-1) of Src to read.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001001 | 1NI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001001 | 100 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ALTGW](#altgw), [GETNIB](#getnib), [GETBYTE](#getbyte), [SETWORD](#setword), [ROLWORD](#rolword)

**Explanation:**

GETWORD reads the word identified by Num (0-1) from Src and writes it to Dest. The Num parameter identifies which of the two words in the 32-bit value to extract, numbered in least-significant word order.

Num 0 selects bits [15:0] (the lower word), and Num 1 selects bits [31:16] (the upper word). The extracted word is zero-extended to 32 bits when written to Dest.

The second syntax form (GETWORD Dest) is intended for use after an ALTGW instruction. This form is useful in loops that iteratively read a series of word values from contiguous long registers. The ALTGW instruction modifies the subsequent GETWORD instruction's source register and word index automatically, enabling efficient sequential word extraction without explicitly specifying the source and index on each iteration.



## GETXACC {#getxacc}

Get Goertzel accumulators
[Streamer](#streamer-category) - Get streamer's Goertzel X/Y accumulators into D and next S.

**GETXACC**  *Dest*

---

**Result:** The streamer's Goertzel X accumulator is written to Dest, the Y accumulator is written to the next instruction's S field, and both accumulators are cleared.

- Dest is a register where the Goertzel X accumulator value is written.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 000011110 | D | --- | --- | 2 |


**Related:** [XCONT](#xcont), [XINIT](#xinit), [XZERO](#xzero)

**Explanation:**

GETXACC retrieves the two Goertzel accumulators from the streamer, which are used for frequency detection and digital signal processing applications. The Goertzel algorithm accumulates signal correlation data that can be used to detect specific frequencies in an input signal.

The X accumulator value is written directly to the Dest register. The Y accumulator value is written to the S field of the immediately following instruction, utilizing the P2's next-instruction operand modification capability. After both values are retrieved, the X and Y accumulators are automatically cleared to zero.

This dual-retrieval mechanism allows both accumulator values to be captured in a compact instruction sequence. The following instruction must have an S field that can receive the Y accumulator value. Typically, this is a MOV or similar instruction where the S operand receives the Y accumulator data.

GETXACC is used in conjunction with the streamer's Goertzel mode, configured via XINIT and controlled via XCONT. The retrieved accumulator values represent the correlation between the input signal and the reference frequency configured in the Goertzel algorithm.



# Instructions: H

This section contains all PASM2 instructions beginning with the letter H.



## HUBSET {#hubset}

Set hub configuration
[Hub Control](#hub-control) - Configure system clock and hub parameters.

**HUBSET**  *{#}D*

---

**Result:** Hub configuration is updated according to the value in D, controlling clock source, crystal settings, and PLL configuration.

- D is a register or 9-bit literal (or 32-bit augmented literal) containing the configuration value for the hub system.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000000000 | --- | --- | --- | 2 |


**Related:** [COGINIT](#coginit), [COGID](#cogid), [CLKSET](#clkset)

**Explanation:**

HUBSET configures the P2's clock system and hub parameters. The 32-bit value in D specifies clock source selection, crystal oscillator settings, and PLL configuration to control the system clock frequency.

The D value contains multiple fields that control different aspects of the clock system:

**Clock Source Selection (D[3:2]):**
- `%00` - RCFAST internal oscillator (~20-25 MHz, boot default)
- `%01` - RCSLOW internal oscillator (~20 kHz, low power mode)
- `%10` - Crystal or external clock on XI pin
- `%11` - PLL output

**Crystal Configuration (D[1:0]):**
- `%00` - XI/XO pins disabled (Hi-Z)
- `%01` - XI/XO with 1MΩ feedback, no capacitors
- `%10` - XI/XO with 1MΩ feedback, 15pF capacitors
- `%11` - XI/XO with 1MΩ feedback, 30pF capacitors

**PLL Configuration:**
- D[27:24] - Input divider (PPPP field, divides XI input by 1-64)
- D[23:14] - VCO multiplier (10-bit field, multiplies by 1-1024)
- D[7:4] - Post divider (DDDD field, divides VCO by 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30)
- D[9] - PLL power enable
- D[8] - Crystal oscillator enable

**System Reset:**
- D[31] - Write 1 to reset the entire chip

The clock switching is glitch-free, and the system automatically falls back to RCFAST if the selected clock source fails. Proper timing must be observed when switching clock sources to allow for oscillator stabilization.

Example: Enable a 20 MHz crystal with 15pF capacitors:

```pasm
        hubset  ##%00_10              ' Enable crystal with 15pF caps
        waitx   ##20_000_000/100      ' Wait 10ms for stabilization
        hubset  ##%10_10              ' Switch to crystal clock
```

Example: Configure PLL to generate 160 MHz from a 20 MHz crystal:

```pasm
        hubset  ##%00_10                        ' Enable crystal
        waitx   ##20_000_000/100                ' Wait 10ms
        hubset  ##%10_10                        ' Switch to crystal
        hubset  ##%0001_0000_0000_00001010_10  ' PLL: /1 * 16 / 2
        waitx   ##20_000_000/10000              ' Wait 100µs for PLL lock
        hubset  ##%0001_0000_0000_00001010_11  ' Switch to PLL output
```

In this PLL example, the VCO runs at 20 MHz * 16 = 320 MHz, then the post divider divides by 2 to produce 160 MHz system clock.

HUBSET takes 2 clock cycles to execute, but switching to a new clock source may take additional time for oscillator stabilization and PLL lock. Always allow appropriate wait periods when changing clock sources.



# Instructions: I

This section contains all PASM2 instructions beginning with the letter I.



## IJZ / IJNZ {#ijz}

Increment and jump if zero / not zero {#ijnz}
[Branch](#branch) - Increment a register and jump based on zero/non-zero result.

**IJZ**  *Dest, {#}Src*
**IJNZ**  *Dest, {#}Src*

---

**Result:** Dest is incremented by 1, and conditionally jumps:

| Instruction | Jumps when |
|-------------|------------|
| IJZ | Result = 0 |
| IJNZ | Result ≠ 0 |

- Dest is a register whose value is incremented and tested.
- Src is the jump address: use # for relative, omit for absolute.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011100 | 00I | DDDDDDDDD | SSSSSSSSS | D + PC* | --- | --- | 2 or 4 |
| EEEE | 1011100 | 01I | DDDDDDDDD | SSSSSSSSS | D + PC* | --- | --- | 2 or 4 |

```{=latex}
*PC is written only when the jump condition is met.
```


**Related:** [DJZ](#djz), [DJNZ](#djnz), [TJZ](#tjz), [TJNZ](#tjnz)

**Explanation:**

IJZ and IJNZ increment Dest and conditionally jump based on whether the result is zero or non-zero.

IJZ is useful for counting until overflow to zero (from $FFFF_FFFF to 0). IJNZ is useful for counting up from a negative value until reaching zero.

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



## INCMOD {#incmod}

Increment with modulus
[Math and Logic](#math-and-logic) - Increment a value with automatic wrap-around at a specified modulus.

**INCMOD**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** If Dest was not equal to Src, it is incremented by 1; otherwise Dest is reset to 0.

- Dest is a register containing the value to increment up to Src with modulus, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is the modulus limit to apply to Dest's increment operation.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111000 | CZI | DDDDDDDDD | SSSSSSSSS | D | D = S, set D = 0 and C = 1, else D = D + 1 and C = 0 | Result = 0 | 2 |


**Related:** [DECMOD](#decmod), [ADDCT1/2/3](instructions-a.md#addct1)

**Explanation:**

INCMOD compares Dest with Src. If they are not equal, INCMOD increments Dest by 1. If they are equal, INCMOD sets Dest to 0. This provides automatic wrap-around behavior for circular counting sequences.

If Dest begins in the range 0 to Src, repeated iterations of INCMOD will increment Dest cyclically from 0 to Src, then wrap back to 0, over and over. This makes INCMOD ideal for round-robin scheduling, circular buffer indexing, and other modulo-arithmetic operations.

If the WC or WCZ effect is specified, the C flag is set (1) if Dest was equal to Src and subsequently reset to 0 (the modulus was triggered), or is cleared (0) if Dest was simply incremented. This allows detecting when the cycle completes.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.

INCMOD does not limit Dest within the specified range. If Dest begins at a value greater than Src, iterations of INCMOD will continue to increment it through the 32-bit rollover point ($FFFF\_FFFF wrapping to $0000\_0000) before it will effectively cycle from 0 to Src.

A common usage pattern for INCMOD is managing circular buffers:

```pasm
                ' Increment tail index with modulo for circular buffer
                incmod  tail_idx, #BUF_SIZE-1  wc
        if_c    jmp     #buffer_wrapped

                ' Safe to add data at tail
                add     buffer_ptr, tail_idx
                wrbyte  new_data, buffer_ptr
```

INCMOD is also ideal for round-robin scheduling across a fixed number of resources:

```pasm
                ' Round-robin through 8 ports (0-7)
.loop
                ' Service current port
                ' ... port service code ...

                ' Move to next port
                incmod  portctr, #7            wc
        if_nc   jmp     #.loop

                ' All ports serviced, continue
```



# Instructions: J

This section contains all PASM2 instructions beginning with the letter J.



## JATN {#jatn}

Jump if ATN event flag is set
[Event](#event) - Jump to S if ATN (attention) event flag is set.

**JATN**  *{#}S*

---

**Result:** If the ATN event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001110 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNATN](#jnatn), [COGATN](#cogatn), [POLLATT](#pollatt)

**Explanation:**

JATN checks the ATN (attention) event flag and conditionally jumps to the address specified by S if the flag is set. The ATN event flag indicates that one or more other cogs are requesting this cog's attention via the COGATN instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the ATN event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JATN is useful for implementing inter-cog communication mechanisms where one cog needs to signal and get the attention of another cog for coordination or data exchange purposes.



## JCT1 / JCT2 / JCT3 {#jct1}

Jump if counter event flag is set (1, 2, or 3)
[Event](#event) - Jump to S if CTn event flag is set.

**JCT1**  *{#}S*
**JCT2**  *{#}S*
**JCT3**  *{#}S*

---

**Result:** If the CTn event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000001 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000010 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000011 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |

```{=latex}
\textsuperscript{1} PC is written only when the CTn event flag is set.
```


**Related:** [JNCT1/2/3](#jnct1), [ADDCT1/2/3](#addct1), [POLLCT1/2/3](#pollct1), [WAITCT1/2/3](#waitct1)

**Explanation:**

JCT1, JCT2, and JCT3 check their respective counter event flags and conditionally jump to the address specified by S if the flag is set. Each CTn event flag is automatically set when the system counter reaches the CTn target value that was previously configured using the corresponding ADDCTn instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CTn event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

The P2 provides three independent hardware counters for timing operations, allowing a cog to manage multiple simultaneous time-based events without software overhead. These instructions are commonly used for timing loops, delays, and periodic task scheduling.



## JFBW {#jfbw}

Jump if FIFO block wrap event flag is set
[Event](#event) - Jump to S if FIFO interface block wrap event flag is set.

**JFBW**  *{#}S*

---

**Result:** If the FIFO interface block wrap event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001001 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNFBW](#jnfbw), [RFBYTE](#rfbyte), [WFBYTE](#wfbyte), [SETQ2](#setq2)

**Explanation:**

JFBW checks the FIFO interface block wrap event flag and conditionally jumps to the address specified by S if the flag is set. This event flag is set when a FIFO read or write operation wraps around the configured block boundary.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the FIFO interface block wrap event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JFBW is useful for implementing circular buffer operations and managing block-based data transfers through the FIFO interface, allowing code to respond immediately when a block boundary has been crossed.



## JINT {#jint}

Jump if INT event flag is set
[Event](#event) - Jump to S if INT (interrupt) event flag is set.

**JINT**  *{#}S*

---

**Result:** If the INT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000000 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNINT](#jnint), [POLLINT](#pollint), [SETINT1/2/3](instructions-s.md#setint1)

**Explanation:**

JINT checks the INT (interrupt) event flag and conditionally jumps to the address specified by S if the flag is set. The INT event flag indicates that a hardware interrupt condition is pending, as configured by one of the SETINT instructions.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the INT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JINT provides a polling-based mechanism for handling hardware interrupts, allowing code to check for interrupt conditions at convenient points in the program flow rather than using asynchronous interrupt handling.



## JMP {#jmp}

Jump
[Branch](#branch) - Unconditional jump to address.

**JMP**  *D*  **{WC/WZ/WCZ}**
**JMP**  *#A*
**JMP**  *#\A*

---

**Result:** PC is set to the address specified by D or A.

- D is a register containing the absolute jump address, and optionally flag values in bits [31:30].
- A is a 20-bit absolute or PC-relative address. Use \ prefix to force absolute addressing when using #.
- WC, WZ, or WCZ are optional effects to set C flag to D[31] and/or Z flag to D[30].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101100 | PC | D[31] | D[30] | 4 |
| EEEE | 1101100 | RAA | AAAAAAAAA | AAAAAAAAA | PC | --- | --- | 4 |


**Related:** [CALL](#call), [RET](#ret), [JMPREL](#jmprel), [CALLD](#calld)

**Explanation:**

JMP performs an unconditional jump to a new address, setting the PC to either the value in register D or the immediate address A.

The first syntax form (JMP D) reads the jump address from register D and sets PC to that value. When the WC or WCZ effect is specified, the C flag is set to bit 31 of D. When the WZ or WCZ effect is specified, the Z flag is set to bit 30 of D. This allows flags to be restored as part of a jump, which is useful for return-from-subroutine operations where both PC and flags need to be restored.

The second syntax form (JMP #A) jumps to an immediate address. The R bit in the encoding determines whether the address is PC-relative (R=1) or absolute (R=0). By default, the assembler uses PC-relative addressing for # jumps. The backslash prefix (\) forces absolute addressing: JMP #\address.

For PC-relative jumps in COG execution mode, the 20-bit address field is added to PC. For Hub execution mode, the lower 18 bits are shifted left by 2 (multiplied by 4) before being added to PC, since Hub addresses are long-aligned.

The instruction executes in 4 clock cycles in COG execution mode. In Hub execution mode, jumps take 13-20 clock cycles depending on Hub access timing.



## JMPREL {#jmprel}

Jump relative
[Branch](#branch) - Jump ahead or back by D instructions.

**JMPREL**  *{#}D*

---

**Result:** PC is incremented or decremented by the value in D.

- D is a register or 9-bit literal specifying the signed offset in instructions. For COG execution, PC += D[19:0]. For Hub execution, PC += D[17:0] << 2.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110000 | PC | --- | --- | 4 |


**Related:** [JMP](#jmp), [CALL](#call), [DJNZ](#djnz), [IJMP](#ijmp)

**Explanation:**

JMPREL performs a relative jump by adding or subtracting the value in D to the current PC value. This allows position-independent code that can jump forward or backward by a specified number of instructions without knowing the absolute address.

For COG execution mode, the lower 20 bits of D are added to PC. Positive values jump forward, negative values (in two's complement) jump backward. The offset is in units of instructions (longs).

For Hub execution mode, the lower 18 bits of D are shifted left by 2 bits (multiplied by 4) before being added to PC. This accounts for the fact that Hub addresses are byte addresses and each instruction occupies 4 bytes. The offset is still conceptually in units of instructions.

The instruction executes in 4 clock cycles in COG execution mode. In Hub execution mode, jumps take 13-20 clock cycles depending on Hub access timing.

JMPREL is useful for implementing position-independent code, jump tables, and dynamic control flow where the jump offset is computed at runtime.



## JNATN {#jnatn}

Jump if ATN event flag is clear
[Event](#event) - Jump to S if ATN (attention) event flag is clear.

**JNATN**  *{#}S*

---

**Result:** If the ATN event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011110 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JATN](#jatn), [COGATN](#cogatn), [POLLATT](#pollatt)

**Explanation:**

JNATN checks the ATN (attention) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JATN, allowing code to jump when no other cog is requesting attention.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the ATN event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNATN is useful for implementing polling loops that wait until the ATN flag is clear before proceeding with other operations.



## JNCT1 / JNCT2 / JNCT3 {#jnct1}

Jump if counter event flag is clear (1, 2, or 3)
[Event](#event) - Jump to S if CTn event flag is clear.

**JNCT1**  *{#}S*
**JNCT2**  *{#}S*
**JNCT3**  *{#}S*

---

**Result:** If the CTn event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000010001 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010010 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010011 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |

```{=latex}
\textsuperscript{1} PC is written only when the CTn event flag is clear.
```


**Related:** [JCT1/2/3](#jct1), [ADDCT1/2/3](#addct1), [POLLCT1/2/3](#pollct1), [WAITCT1/2/3](#waitct1)

**Explanation:**

JNCT1, JNCT2, and JNCT3 check their respective counter event flags and conditionally jump to the address specified by S if the flag is clear. These are the logical complements of JCT1/2/3, allowing code to jump when the corresponding counter event has not yet occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CTn event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

These instructions are useful for implementing polling loops that continue until a counter event occurs, or for skipping code that should only execute before a specific time. The P2's three independent counter event polling mechanisms enable sophisticated timing control with minimal code overhead.



## JNFBW {#jnfbw}

Jump if FIFO block wrap event flag is clear
[Event](#event) - Jump to S if FIFO interface block wrap event flag is clear.

**JNFBW**  *{#}S*

---

**Result:** If the FIFO interface block wrap event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011001 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JFBW](#jfbw), [RFBYTE](#rfbyte), [WFBYTE](#wfbyte), [SETQ2](#setq2)

**Explanation:**

JNFBW checks the FIFO interface block wrap event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JFBW, allowing code to jump when no block wrap has occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the FIFO interface block wrap event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNFBW is useful for polling loops that wait until a block wrap occurs, or for conditional code that should only execute when within a block boundary.



## JNINT {#jnint}

Jump if INT event flag is clear
[Event](#event) - Jump to S if INT (interrupt) event flag is clear.

**JNINT**  *{#}S*

---

**Result:** If the INT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000010000 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JINT](#jint), [POLLINT](#pollint), [SETINT1/2/3](instructions-s.md#setint1)

**Explanation:**

JNINT checks the INT (interrupt) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JINT, allowing code to jump when no interrupt is pending.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the INT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNINT is useful for polling loops that wait until an interrupt occurs, or for implementing interrupt-safe critical sections that should only execute when interrupts are not pending.



## JNPAT {#jnpat}

Jump if pattern match event flag is clear
[Event](#event) - Jump to S if PAT (pattern match) event flag is clear.

**JNPAT**  *{#}S*

---

**Result:** If the PAT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011000 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JPAT](#jpat), [SETPAT](#setpat), [POLLPAT](#pollpat)

**Explanation:**

JNPAT checks the PAT (pattern match) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JPAT, allowing code to jump when no pattern match has occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the PAT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNPAT is useful for polling loops that wait until a specific pattern appears on the I/O pins, or for conditional logic that should execute only when the pattern has not yet matched.



## JNQMT {#jnqmt}

Jump if CORDIC empty event flag is clear
[Event](#event) - Jump to S if CORDIC-read-but-empty event flag is clear.

**JNQMT**  *{#}S*

---

**Result:** If the CORDIC-read-but-empty event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011111 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JQMT](#jqmt), [QMUL](#qmul), [QROTATE](#qrotate), [GETQX](#getqx), [GETQY](#getqy)

**Explanation:**

JNQMT checks the CORDIC-read-but-empty event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JQMT, allowing code to jump when the CORDIC result is ready or has not been prematurely read.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CORDIC-read-but-empty event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNQMT is useful for ensuring CORDIC results are read at the correct time, helping to detect and handle timing errors in mathematical operations.



## JNSE1 / JNSE2 / JNSE3 / JNSE4 {#jnse1}

Jump if selectable event flag is clear (1, 2, 3, or 4)
[Event](#event) - Jump to S if SEn event flag is clear.

**JNSE1**  *{#}S*
**JNSE2**  *{#}S*
**JNSE3**  *{#}S*
**JNSE4**  *{#}S*

---

**Result:** If the SEn event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000010100 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010101 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010110 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000010111 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |

```{=latex}
\textsuperscript{1} PC is written only when the SEn event flag is clear.
```


**Related:** [JSE1/2/3/4](#jse1), [SETSE1/2/3/4](#setse1), [POLLSE1/2/3/4](#pollse1), [WAITSE1/2/3/4](#waitse1)

**Explanation:**

JNSE1, JNSE2, JNSE3, and JNSE4 check their respective selectable event flags and conditionally jump to the address specified by S if the flag is clear. These are the logical complements of JSE1/2/3/4, allowing code to jump when the corresponding selectable event has not occurred.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SEn event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

The P2 provides four selectable event sources, each configurable via SETSE instructions to detect various hardware conditions. These polling mechanisms provide maximum flexibility for event-driven control flows.



## JNXFI {#jnxfi}

Jump if streamer finished event flag is clear
[Event](#event) - Jump to S if XFI (streamer finished) event flag is clear.

**JNXFI**  *{#}S*

---

**Result:** If the XFI event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011011 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JXFI](#jxfi), [XINIT](#xinit), [XCONT](#xcont), [POLLXFI](#pollxfi)

**Explanation:**

JNXFI checks the XFI (streamer finished) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXFI, allowing code to jump when the streamer has not yet finished.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XFI event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXFI is useful for polling loops that wait until the streamer completes its operation, synchronizing code execution with streamer activity.



## JNXMT {#jnxmt}

Jump if streamer empty event flag is clear
[Event](#event) - Jump to S if XMT (streamer empty) event flag is clear.

**JNXMT**  *{#}S*

---

**Result:** If the XMT event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011010 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JXMT](#jxmt), [XINIT](#xinit), [XCONT](#xcont), [POLLXMT](#pollxmt)

**Explanation:**

JNXMT checks the XMT (streamer empty) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXMT, allowing code to jump when the streamer still has data to transmit.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XMT event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXMT is useful for maintaining continuous streamer operation by reloading data only when the streamer buffer still contains data, avoiding underrun conditions.



## JNXRL {#jnxrl}

Jump if streamer LUT rollover event flag is clear
[Event](#event) - Jump to S if XRL (streamer LUT RAM rollover) event flag is clear.

**JNXRL**  *{#}S*

---

**Result:** If the XRL event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011101 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JXRL](#jxrl), [XINIT](#xinit), [XCONT](#xcont), [POLLXRL](#pollxrl)

**Explanation:**

JNXRL checks the XRL (streamer LUT RAM rollover) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXRL, allowing code to jump when the streamer LUT RAM address has not rolled over.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRL event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXRL is useful for implementing circular buffer management for streamer operations using LUT RAM, allowing code to detect when a buffer boundary has not yet been crossed.



## JNXRO {#jnxro}

Jump if streamer NCO rollover event flag is clear
[Event](#event) - Jump to S if XRO (streamer NCO rollover) event flag is clear.

**JNXRO**  *{#}S*

---

**Result:** If the XRO event flag is clear, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000011100 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JXRO](#jxro), [XINIT](#xinit), [XCONT](#xcont), [POLLXRO](#pollxro)

**Explanation:**

JNXRO checks the XRO (streamer NCO rollover) event flag and conditionally jumps to the address specified by S if the flag is clear. This is the logical complement of JXRO, allowing code to jump when the streamer's NCO (numerically controlled oscillator) has not rolled over.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRO event flag is set, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JNXRO is useful for timing-sensitive streamer applications where code needs to synchronize with or detect the absence of NCO rollovers in the streaming operation.



## JPAT {#jpat}

Jump if pattern match event flag is set
[Event](#event) - Jump to S if PAT (pattern match) event flag is set.

**JPAT**  *{#}S*

---

**Result:** If the PAT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001000 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNPAT](#jnpat), [SETPAT](#setpat), [POLLPAT](#pollpat)

**Explanation:**

JPAT checks the PAT (pattern match) event flag and conditionally jumps to the address specified by S if the flag is set. The PAT event flag is set when the I/O pins match a pattern previously configured with the SETPAT instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the PAT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JPAT is useful for implementing hardware-triggered control flow where code execution branches based on specific pin state patterns, enabling efficient event-driven programming without continuous polling.



## JQMT {#jqmt}

Jump if CORDIC empty event flag is set
[Event](#event) - Jump to S if CORDIC-read-but-empty event flag is set.

**JQMT**  *{#}S*

---

**Result:** If the CORDIC-read-but-empty event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001111 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNQMT](#jnqmt), [QMUL](#qmul), [QROTATE](#qrotate), [GETQX](#getqx), [GETQY](#getqy)

**Explanation:**

JQMT checks the CORDIC-read-but-empty event flag and conditionally jumps to the address specified by S if the flag is set. This event flag is set when code attempts to read CORDIC results before the calculation has completed, indicating a timing error.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the CORDIC-read-but-empty event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JQMT is useful for error handling in CORDIC operations, allowing code to detect and respond to premature reads of calculation results, which can help debug timing issues in mathematical code.



## JSE1 / JSE2 / JSE3 / JSE4 {#jse1}

Jump if selectable event flag is set (1, 2, 3, or 4)
[Event](#event) - Jump to S if SEn event flag is set.

**JSE1**  *{#}S*
**JSE2**  *{#}S*
**JSE3**  *{#}S*
**JSE4**  *{#}S*

---

**Result:** If the SEn event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000000100 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000101 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000110 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |
| EEEE | 1011110 | 01I | 000000111 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |

```{=latex}
\textsuperscript{1} PC is written only when the SEn event flag is set.
```


**Related:** [JNSE1/2/3/4](#jnse1), [SETSE1/2/3/4](#setse1), [POLLSE1/2/3/4](#pollse1), [WAITSE1/2/3/4](#waitse1)

**Explanation:**

JSE1, JSE2, JSE3, and JSE4 check their respective selectable event flags and conditionally jump to the address specified by S if the flag is set. Each selectable event can be configured to detect various hardware conditions using the corresponding SETSE instruction.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the SEn event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

The P2 provides four independent selectable event sources, enabling multiple concurrent hardware event detection mechanisms for sophisticated event-driven applications.



## JXFI {#jxfi}

Jump if streamer finished event flag is set
[Event](#event) - Jump to S if XFI (streamer finished) event flag is set.

**JXFI**  *{#}S*

---

**Result:** If the XFI event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001011 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNXFI](#jnxfi), [XINIT](#xinit), [XCONT](#xcont), [POLLXFI](#pollxfi)

**Explanation:**

JXFI checks the XFI (streamer finished) event flag and conditionally jumps to the address specified by S if the flag is set. The XFI event flag is set when the streamer completes its current operation.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XFI event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXFI is useful for chaining streamer operations or triggering code execution immediately when a streaming operation completes, enabling efficient streamer-driven workflows.



## JXMT {#jxmt}

Jump if streamer empty event flag is set
[Event](#event) - Jump to S if XMT (streamer empty) event flag is set.

**JXMT**  *{#}S*

---

**Result:** If the XMT event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001010 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNXMT](#jnxmt), [XINIT](#xinit), [XCONT](#xcont), [POLLXMT](#pollxmt)

**Explanation:**

JXMT checks the XMT (streamer empty) event flag and conditionally jumps to the address specified by S if the flag is set. The XMT event flag is set when the streamer's internal buffer becomes empty and needs to be refilled.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XMT event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXMT is useful for implementing continuous streaming operations where the code needs to reload data into the streamer when the buffer empties, preventing gaps or underruns in the output stream.



## JXRL {#jxrl}

Jump if streamer LUT rollover event flag is set
[Event](#event) - Jump to S if XRL (streamer LUT RAM rollover) event flag is set.

**JXRL**  *{#}S*

---

**Result:** If the XRL event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001101 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNXRL](#jnxrl), [XINIT](#xinit), [XCONT](#xcont), [POLLXRL](#pollxrl)

**Explanation:**

JXRL checks the XRL (streamer LUT RAM rollover) event flag and conditionally jumps to the address specified by S if the flag is set. The XRL event flag is set when the streamer's LUT RAM address pointer rolls over from the end back to the beginning of the configured range.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRL event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXRL is useful for implementing circular buffer operations with the streamer using LUT RAM, allowing code to detect when a complete cycle through the buffer has occurred.



## JXRO {#jxro}

Jump if streamer NCO rollover event flag is set
[Event](#event) - Jump to S if XRO (streamer NCO rollover) event flag is set.

**JXRO**  *{#}S*

---

**Result:** If the XRO event flag is set, PC is set to the address specified by S.

- S is a register, 9-bit literal, or 20-bit augmented literal specifying the absolute or relative address to jump to. Use # for relative addressing; omit # for absolute addressing.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 01I | 000001100 | SSSSSSSSS | PC\textsuperscript{1} | --- | --- | 2 or 4 |


**Related:** [JNXRO](#jnxro), [XINIT](#xinit), [XCONT](#xcont), [POLLXRO](#pollxro)

**Explanation:**

JXRO checks the XRO (streamer NCO rollover) event flag and conditionally jumps to the address specified by S if the flag is set. The XRO event flag is set when the streamer's numerically controlled oscillator (NCO) rolls over, which occurs at regular intervals determined by the NCO frequency setting.

When the # prefix is used with S, the jump is relative to the current PC value. When # is omitted, the jump is to the absolute address specified by S. If the XRO event flag is clear, execution continues with the next instruction and the jump is not taken.

The instruction executes in 2 clock cycles if the jump is not taken, or 4 clock cycles if the jump is taken (in COG execution mode). In Hub execution mode, taken jumps require 13-20 clock cycles depending on Hub timing.

JXRO is useful for timing-critical streamer applications where code needs to synchronize with the NCO rollovers, such as sample-rate based operations or periodic streamer updates.



# Instructions: L

This section contains all PASM2 instructions beginning with the letter L.



## LOC {#loc}

Load address
[Hub RAM](#hub-ram) - Load address into PA, PB, PTRA, or PTRB.

**LOC**  *PA/PB/PTRA/PTRB, #A*
**LOC**  *PA/PB/PTRA/PTRB, #\A*

---

**Result:** Address is loaded into the specified pointer register.

- PA, PB, PTRA, or PTRB is the destination pointer register.
- A is a 20-bit address value.
- The optional backslash (\) prefix forces absolute addressing (R=0). Without it, relative addressing is used (R=1).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 11101WW | RAA | AAAAAAAAA | AAAAAAAAA | Per W | --- | --- | 2 |


**Related:** [PA](#pa), [PB](#pb), [PTRA](#ptra), [PTRB](#ptrb), [CALLD](#calld), [CALLPA](#callpa), [CALLPB](#callpb)

**Explanation:**

LOC loads an address into one of the four pointer registers: PA, PB, PTRA, or PTRB. These pointer registers are used by various memory operations and call instructions.

The instruction supports two addressing modes, controlled by the R bit in the encoding. By default, LOC uses relative addressing (R=1), where the address is calculated as PC + A. This allows position-independent code, as the address is computed relative to the current program counter. To force absolute addressing (R=0), prefix the address with a backslash (\), making the address equal to A directly.

The WW field in the encoding selects which pointer register to load: 00 for PA, 01 for PB, 10 for PTRA, and 11 for PTRB. The address field A is 20 bits wide, providing access to the full Hub memory space.

LOC is commonly used to set up pointer registers before memory operations, call sequences, or when establishing base addresses for data structures. The relative addressing mode is particularly useful for creating position-independent code blocks that can execute correctly regardless of where they are loaded in Hub memory.



## LOCKNEW {#locknew}

Allocate new lock
[Hub Control](#hub-control) - Request a new LOCK from the hardware lock pool.

**LOCKNEW**  *D*  **{WC}**

---

**Result:** D is written with an available lock number (0-15), or remains unchanged if no lock is available.

- D is a register where the allocated lock number is written.
- WC is an optional effect to update the C flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C00 | DDDDDDDDD | 000000100 | D | 1 if no LOCK available | --- | 4...11 |


**Related:** [LOCKTRY](#locktry), [LOCKREL](#lockrel), [LOCKRET](#lockret)

**Explanation:**

LOCKNEW requests a lock from the P2's hardware lock pool. The P2 provides 16 hardware locks (numbered 0-15) for inter-COG synchronization and resource protection. LOCKNEW searches the lock pool for an available lock and, if one is found, returns its number in the D register.

If the WC effect is specified, the C flag is set (1) if no lock is available, or cleared (0) if a lock was successfully allocated. This allows the calling code to detect allocation failure and take appropriate action.

Once a lock is allocated with LOCKNEW, it remains assigned until explicitly returned to the pool with LOCKRET. The allocated lock can then be used with LOCKTRY to acquire exclusive access and LOCKREL to release it. This allocation-try-release-return pattern ensures proper resource management in multi-COG systems.

LOCKNEW is essential for dynamic lock allocation in systems where the number of required locks is not known at compile time, or where locks are allocated and deallocated as resources are created and destroyed. The instruction completes in 4 to 11 clock cycles depending on lock availability and contention.



## LOCKREL {#lockrel}

Release lock
[Hub Control](#hub-control) - Release a previously acquired LOCK.

**LOCKREL**  *{#}D*  **{WC}**

---

**Result:** The lock specified by D[3:0] is released for other COGs to acquire.

- D is a register or 4-bit literal (0-15) specifying the lock number to release.
- When D is a register and WC is specified, D is written with the previous owner's COG ID and the C flag indicates lock status.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C0L | DDDDDDDDD | 000000111 | --- | --- | --- | 2...9, +2 if result |


**Related:** [LOCKTRY](#locktry), [LOCKNEW](#locknew), [LOCKRET](#lockret), [COGID](#cogid)

**Explanation:**

LOCKREL releases a lock that was previously acquired with LOCKTRY, making it available for other COGs to acquire. The lock to release is specified by the lower 4 bits of D (D[3:0]), allowing lock numbers 0 through 15.

When D is a register (not an immediate) and the WC effect is specified, LOCKREL performs an additional operation: it writes the COG ID of the previous lock owner into D and sets the C flag based on whether the lock was held. This diagnostic feature allows verification of lock ownership and debugging of synchronization issues.

LOCKREL is safe to call even if the lock was not held by the current COG. Releasing an unheld lock simply has no effect. This property simplifies error recovery code, as locks can be released without checking ownership first.

Proper lock management requires that every LOCKTRY that successfully acquires a lock is balanced with a corresponding LOCKREL. Failure to release locks leads to deadlocks and resource starvation. The instruction completes in 2 to 9 clock cycles, with an additional 2 cycles if the result is written back to D.



## LOCKRET {#lockret}

Return lock to pool
[Hub Control](#hub-control) - Return a LOCK to the pool for reallocation.

**LOCKRET**  *{#}D*

---

**Result:** The lock specified by D[3:0] is returned to the pool and becomes available for LOCKNEW.

- D is a register or 4-bit literal (0-15) specifying the lock number to return.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000000101 | --- | --- | --- | 2...9 |


**Related:** [LOCKNEW](#locknew), [LOCKTRY](#locktry), [LOCKREL](#lockrel)

**Explanation:**

LOCKRET returns a lock to the hardware lock pool, making it available for future allocation by LOCKNEW. This instruction completes the lifecycle of a dynamically allocated lock: first allocated with LOCKNEW, then used with LOCKTRY and LOCKREL for synchronization, and finally returned with LOCKRET when no longer needed.

The lock to return is specified by the lower 4 bits of D (D[3:0]), allowing lock numbers 0 through 15. Unlike LOCKREL, which only releases ownership of a lock while keeping it allocated, LOCKRET deallocates the lock entirely, allowing LOCKNEW to assign it to a different purpose.

LOCKRET should only be called on locks that are not currently held by any COG. Before returning a lock, ensure it has been released with LOCKREL. Returning a lock that is still held can cause synchronization failures in other COGs that may be waiting for or using that lock.

The proper pattern for dynamic lock usage is: LOCKNEW to allocate, LOCKTRY/LOCKREL for each critical section, and LOCKRET when the lock is no longer needed for any purpose. This ensures efficient use of the limited pool of 16 hardware locks. The instruction completes in 2 to 9 clock cycles depending on Hub access contention.



## LOCKTRY {#locktry}

Try to acquire lock
[Hub Control](#hub-control) - Attempt to acquire a LOCK with atomic test-and-set.

**LOCKTRY**  *{#}D*  **{WC}**

---

**Result:** Attempts to acquire the lock specified by D[3:0]. The C flag indicates success.

- D is a register or 4-bit literal (0-15) specifying the lock number to acquire.
- WC is an optional effect to update the C flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C0L | DDDDDDDDD | 000000110 | --- | 1 if got LOCK | --- | 2...9, +2 if result |


**Related:** [LOCKREL](#lockrel), [LOCKNEW](#locknew), [LOCKRET](#lockret), [COGID](#cogid)

**Explanation:**

LOCKTRY attempts to acquire a lock using an atomic test-and-set operation. The lock to acquire is specified by the lower 4 bits of D (D[3:0]), allowing lock numbers 0 through 15. The P2 provides 16 hardware locks for inter-COG synchronization and resource protection.

If the WC effect is specified, the C flag is set (1) if the lock was successfully acquired, or cleared (0) if the lock is already held by another COG. This non-blocking behavior allows the calling code to make immediate decisions: proceed with the protected operation if the lock was acquired, or take alternative action if it was not.

LOCKTRY implements the critical section entry point in the standard lock pattern: try to acquire the lock, and only proceed if successful. The lock must be released with LOCKREL when the critical section completes. This ensures mutual exclusion, preventing multiple COGs from simultaneously accessing shared resources.

The instruction is non-blocking and returns immediately regardless of lock availability. For spin-lock behavior (waiting until the lock is acquired), LOCKTRY must be called repeatedly in a loop. Lock 15 is traditionally reserved for debug monitor use. The instruction completes in 2 to 9 clock cycles, with an additional 2 cycles if a result is returned.



# Instructions: M

This section contains all PASM2 instructions beginning with the letter M.



## MERGEB {#mergeb}

Merge bits of bytes
[Math and Logic](#math-and-logic) - Rearrange bits from each byte into a merged pattern.

**MERGEB**  *D*

---

**Result:** Bits from each byte in D are rearranged into a specific merged pattern.

- D is a register containing the value whose byte bits will be merged.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100001 | D | --- | --- | 2 |


**Related:** [MERGEW](#mergew), [SPLITB](#splitb), [SPLITW](#splitw)

**Explanation:**

MERGEB rearranges the bits within D by extracting one bit from each byte and merging them into a specific pattern. The result is: D = {D[31], D[23], D[15], D[7], D[30], D[22], D[14], D[6], ..., D[24], D[16], D[8], D[0]}.

This operation takes the most significant bit from each of the four bytes in D and places them in the upper nibble of the result, then the next most significant bit from each byte into the next nibble, and so on. Each group of four bits in the result contains one bit from each of the four original bytes.

MERGEB is useful for bit-plane conversions, graphics operations, and data transformations where bits need to be regrouped across byte boundaries. It performs the inverse operation of SPLITB, which distributes bits back into their original byte positions.



## MERGEW {#mergew}

Merge bits of words
[Math and Logic](#math-and-logic) - Rearrange bits from each word into a merged pattern.

**MERGEW**  *D*

---

**Result:** Bits from each word in D are rearranged into a specific merged pattern.

- D is a register containing the value whose word bits will be merged.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100011 | D | --- | --- | 2 |


**Related:** [MERGEB](#mergeb), [SPLITB](#splitb), [SPLITW](#splitw)

**Explanation:**

MERGEW rearranges the bits within D by extracting corresponding bits from each of the two 16-bit words and interleaving them. The result is: D = {D[31], D[15], D[30], D[14], D[29], D[13], ..., D[17], D[1], D[16], D[0]}.

This operation interleaves the bits from the upper and lower words of D, alternating between taking a bit from the upper word and a bit from the lower word. The most significant bit of the result comes from the most significant bit of the upper word, the next bit from the most significant bit of the lower word, and so on.

MERGEW is useful for word-level bit-plane conversions, graphics operations requiring word-aligned data transformations, and encoding operations. It performs the inverse operation of SPLITW, which de-interleaves the bits back into their original word positions.



## MIXPIX {#mixpix}

Mix pixels
[Pixel Mixer](#pixel-mixer) - Blend bytes of source into destination using pixel mixer configuration.

**MIXPIX**  *D,{#}S*

---

**Result:** Bytes of S are blended into bytes of D according to the SETPIX and SETPIV configuration.

- D is a register containing the destination pixel bytes to be modified.
- S is a register, 9-bit literal, or 32-bit augmented literal containing the source pixel bytes.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010010 | 11I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 7 |


**Related:** [SETPIX](#setpix), [SETPIV](#setpiv), [ADDPIX](#addpix), [MULPIX](#mulpix), [BLNPIX](#blnpix)

**Explanation:**

MIXPIX performs pixel blending operations on the four bytes of D using the four bytes of S, according to the mixing parameters previously configured by SETPIX and SETPIV instructions. Each byte is treated as a separate pixel component (typically used for red, green, blue, and alpha channels in RGBA color format).

The SETPIX instruction configures the pixel mixer mode, which determines how the source and destination bytes are combined (such as multiply, add, or blend operations). The SETPIV instruction provides additional configuration values that affect the mixing calculation.

This instruction executes in 7 clock cycles to perform the pixel arithmetic on all four bytes in parallel. The exact blending formula depends on the mode set by SETPIX, but typically implements standard pixel compositing operations used in graphics rendering, such as alpha blending, color multiplication, or additive blending.

MIXPIX is essential for high-performance graphics operations, enabling real-time color mixing, transparency effects, and color space transformations without requiring multiple individual byte operations.



## MODC {#modc}

Modify C flag
[Math and Logic](#math-and-logic) - Set or clear the C flag based on a modifier and current flag state.

**MODC**  *c*  **{WC}**

---

**Result:** The C flag is set or cleared according to the modifier and current C and Z flag states.

- c is a 4-bit modifier value that selects which combination of current C and Z flag states produces a 1 result for the C flag.
- WC is an optional effect to make the modification visible to subsequent flag reads.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | C01 | 0cccc0000 | 001101111 | --- | cccc[\{C,Z\}] | --- | 2 |


**Related:** [MODZ](#modz), [MODCZ](#modcz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODC provides conditional modification of the C flag based on a 4-bit modifier value and the current state of both the C and Z flags. The modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifier is applied as: C = cccc[{C,Z}], where {C,Z} forms a 2-bit index into the 4-bit modifier value. For example, if the current C flag is 1 and Z flag is 0, the index is binary 10 (2 decimal), and the C flag is set to bit 2 of the modifier value.

Common modifier values enable useful operations: $F (binary 1111) always sets C to 1, $0 (binary 0000) always clears C to 0, $C (binary 1100) copies C to itself (if Z=0) or clears it (if Z=1), and $3 (binary 0011) sets C if Z=1.

MODC is typically used after comparison or test instructions to create complex conditional logic without branching. It provides a mechanism to compute a boolean result based on multiple flag conditions in a single instruction.

If the WC effect is specified, the flag modification becomes visible to subsequent instructions; otherwise, the modification may be used internally without affecting the architectural flag state.



## MODCZ {#modcz}

Modify C and Z flags
[Math and Logic](#math-and-logic) - Set or clear both C and Z flags based on modifiers and current flag states.

**MODCZ**  *c,z*  **{WC/WZ/WCZ}**

---

**Result:** Both C and Z flags are set or cleared according to their modifiers and the current C and Z flag states.

- c is a 4-bit modifier value that selects which combination of current C and Z flag states produces a 1 result for the C flag.
- z is a 4-bit modifier value that selects which combination of current C and Z flag states produces a 1 result for the Z flag.
- WC, WZ, or WCZ are optional effects to make the modifications visible to subsequent flag reads.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 0cccczzzz | 001101111 | --- | cccc[\{C,Z\}] | zzzz[\{C,Z\}] | 2 |


**Related:** [MODC](#modc), [MODZ](#modz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODCZ provides simultaneous conditional modification of both the C and Z flags based on 4-bit modifier values and the current state of both flags. Each modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifiers are applied as: C = cccc[{C,Z}] and Z = zzzz[{C,Z}], where {C,Z} forms a 2-bit index into each 4-bit modifier value. Both flags are updated simultaneously based on the same initial C and Z states, allowing complex boolean operations to be computed in parallel.

This instruction enables sophisticated conditional logic operations without branching. For example, modifier values can implement logical operations like AND, OR, XOR between the flags, or conditional moves where one flag's new value depends on the other flag's current state.

Common uses include implementing state machines where both flags represent state bits, performing multi-condition tests after comparison operations, and creating compact conditional code sequences that would otherwise require multiple instructions or branches.

If the WC, WZ, or WCZ effects are specified, the flag modifications become visible to subsequent instructions. Without these effects, the modifications may be used internally without affecting the architectural flag state visible to later code.

The simultaneous update of both flags makes MODCZ more powerful than using separate MODC and MODZ instructions, as it allows each flag's new value to be based on the same initial flag state rather than having one flag update affect the other's calculation.



## MODZ {#modz}

Modify Z flag
[Math and Logic](#math-and-logic) - Set or clear the Z flag based on a modifier and current flag state.

**MODZ**  *z*  **{WZ}**

---

**Result:** The Z flag is set or cleared according to the modifier and current C and Z flag states.

- z is a 4-bit modifier value that selects which combination of current C and Z flag states produces a 1 result for the Z flag.
- WZ is an optional effect to make the modification visible to subsequent flag reads.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 0Z1 | 00000zzzz | 001101111 | --- | --- | zzzz[\{C,Z\}] | 2 |


**Related:** [MODC](#modc), [MODCZ](#modcz), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

MODZ provides conditional modification of the Z flag based on a 4-bit modifier value and the current state of both the C and Z flags. The modifier value acts as a lookup table, where each of the four bits corresponds to one of the four possible combinations of the current C and Z flag states: 00, 01, 10, and 11.

The modifier is applied as: Z = zzzz[{C,Z}], where {C,Z} forms a 2-bit index into the 4-bit modifier value. For example, if the current C flag is 0 and Z flag is 1, the index is binary 01 (1 decimal), and the Z flag is set to bit 1 of the modifier value.

Common modifier values enable useful operations: $F (binary 1111) always sets Z to 1, $0 (binary 0000) always clears Z to 0, $A (binary 1010) copies Z to itself (preserving current state), and $C (binary 1100) sets Z if C=1.

MODZ is typically used after comparison or test instructions to create complex conditional logic without branching. It provides a mechanism to compute a boolean result based on multiple flag conditions in a single instruction.

If the WZ effect is specified, the flag modification becomes visible to subsequent instructions; otherwise, the modification may be used internally without affecting the architectural flag state.



## MOV {#mov}

Move
[Math and Logic](#math-and-logic) - Copy a value from source to destination.

**MOV**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The Src value is stored in Dest.

- Dest is a register where the Src value will be written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is copied to Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0110000 | CZI | DDDDDDDDD | SSSSSSSSS | D | S[31] | Result = 0 | 2 |


**Related:** [MOVBYTS](#movbyts), [MUXNIBS](#muxnibs), [MUXNITS](#muxnits), [SETQ](#setq)

**Explanation:**

MOV copies the value from Src into the Dest register, providing the fundamental data movement operation in PASM2. This is one of the most frequently used instructions, enabling register initialization, value copying, and data transfer between registers.

If the WC or WCZ effect is specified, the C flag is set to the most significant bit of the source value (Src[31]), which represents the sign bit when Src is interpreted as a signed 32-bit value. This allows MOV to simultaneously copy a value and test its sign.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result written to Dest equals zero, or is cleared (0) if the result is non-zero. This enables immediate testing of whether the moved value is zero without requiring a separate comparison instruction.

MOV with immediate values is commonly used for register initialization:

```pasm
        mov     counter, #100           ' Initialize counter to 100
        mov     mask, ##$FFFF_0000      ' Load 32-bit constant using AUGS
```

MOV between registers is used for preserving values and working with temporary copies:

```pasm
        mov     temp, value             ' Save value in temp
        add     value, increment        ' Modify value
        mov     result, value           ' Copy final result
```

When combined with flag effects, MOV enables efficient value testing:

```pasm
                mov     data, source  wz        ' Copy and test if zero
        if_nz   call    #process                ' Process only if non-zero
                mov     signed, value  wc       ' Copy and test sign bit
        if_c    neg     signed, signed          ' Make positive if negative
```



## MOVBYTS {#movbyts}

Move bytes
[Math and Logic](#math-and-logic) - Rearrange bytes within a register according to a control pattern.

**MOVBYTS**  *D,{#}S*

---

**Result:** Bytes within D are rearranged according to the byte selection pattern in S.

- D is a register containing the bytes to be rearranged.
- S is a register, 9-bit literal, or 32-bit augmented literal containing the byte selection pattern.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001111 | 11I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [MOVBYTS](#movbyts), [MERGEB](#mergeb), [SPLITB](#splitb), [ROLBYTE](#rolbyte)

**Explanation:**

MOVBYTS rearranges the four bytes within D according to a selection pattern specified in the lower 8 bits of S. The result is: D = {D.BYTE[S[7:6]], D.BYTE[S[5:4]], D.BYTE[S[3:2]], D.BYTE[S[1:0]]}.

Each 2-bit field in S selects which of the four original bytes in D will appear in each position of the result. S[1:0] selects the byte for the least significant position, S[3:2] for the second byte, S[5:4] for the third byte, and S[7:6] for the most significant byte. The 2-bit values 0, 1, 2, and 3 select bytes 0 (bits 7:0), 1 (bits 15:8), 2 (bits 23:16), and 3 (bits 31:24) respectively.

For example, to swap the high and low words of D, use S = $4E (binary 01_00_11_10), which places byte 2 in position 0, byte 3 in position 1, byte 0 in position 2, and byte 1 in position 3. To reverse all four bytes, use S = $1B (binary 00_01_10_11).

MOVBYTS is useful for byte-order conversions (endianness swapping), color channel reordering in pixel data, and general byte permutation operations. It executes in 2 clock cycles, making it an efficient alternative to multiple shift and mask operations.

Common patterns include:
- S = $E4 (binary 11_10_01_00): No change (identity)
- S = $1B (binary 00_01_10_11): Reverse bytes (big/little endian swap)
- S = $B1 (binary 10_11_00_01): Swap words
- S = $4E (binary 01_00_11_10): Swap bytes within each word



## MUL {#mul}

Multiply
[Math and Logic](#math-and-logic) - Multiply two unsigned 16-bit values to produce a 32-bit result.

**MUL**  *Dest, {#}Src*  **{WZ}**

---

**Result:** The 32-bit unsigned product of the lower 16 bits of Dest and Src is stored in Dest.

- Dest is a register containing the 16-bit value to multiply with Src, and is where the 32-bit result is written.
- Src is a register, 9-bit literal, or 16-bit augmented literal whose lower 16 bits are multiplied with Dest.
- WZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010000 | 0ZI | DDDDDDDDD | SSSSSSSSS | D | --- | (D = 0) \| (S = 0) | 2 |


**Related:** [MULS](#muls), [QMUL](#qmul), [SCA](#sca), [SCAS](#scas)

**Explanation:**

MUL performs an unsigned 16-bit by 16-bit multiplication, taking only the lower 16 bits from each of Dest and Src, multiplying them together, and storing the full 32-bit unsigned product into Dest. This is a fast 2-clock multiplication operation suitable for small integer arithmetic and fixed-point calculations.

The operation is: D = unsigned(D[15:0] * S[15:0]). The upper 16 bits of both Dest and Src are ignored during the multiplication, but the full 32-bit result can utilize all bits in the destination register. For example, multiplying $0001_8000 by $0002_4000 produces $2000_0000 (using only the $8000 and $4000 values).

If the WZ effect is specified, the Z flag is set (1) if either Dest or Src equals zero before the multiplication, or is cleared (0) if both are non-zero. Note that this tests the pre-multiplication values, not the result, providing a quick way to detect zero operands.

MUL is commonly used for scaling operations in fixed-point arithmetic:

```pasm
        mov     value, ##1000           ' Value = 1000
        mul     value, #25              ' Multiply by 25: value = 25000
```

For fixed-point math with 16-bit fractional parts:

```pasm
        ' Multiply two 16.16 fixed-point numbers
        ' Result in upper 16 bits needs shifting
        mov     temp, frac1
        mul     temp, frac2             ' temp = product (low 16 of each)
        shr     temp, #16               ' Adjust for fixed-point scale
```

For multiplications larger than 16x16 bits, use the CORDIC solver QMUL instruction, which can multiply full 32-bit values and produces a 64-bit result accessible through the upper and lower result registers. MUL's 2-clock speed makes it ideal when the operands are known to fit in 16 bits.



## MULPIX {#mulpix}

Multiply pixels
[Pixel Mixer](#pixel-mixer) - Multiply corresponding bytes treating them as fractional values.

**MULPIX**  *D,{#}S*

---

**Result:** Each byte of S is multiplied with the corresponding byte of D, with results stored in D.

- D is a register containing four pixel bytes to be multiplied.
- S is a register, 9-bit literal, or 32-bit augmented literal containing four pixel bytes as multipliers.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010010 | 01I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 7 |


**Related:** [ADDPIX](#addpix), [BLNPIX](#blnpix), [MIXPIX](#mixpix), [SETPIX](#setpix)

**Explanation:**

MULPIX performs parallel multiplication on four byte pairs, treating each byte as a fractional value where $FF represents 1.0 and $00 represents 0.0. Each of the four bytes in S is multiplied with the corresponding byte in D, and the results replace the bytes in D.

The multiplication treats bytes as 8-bit fractional values in the range 0.0 to 1.0. For each byte position, the operation computes: D.BYTE[n] = (D.BYTE[n] * S.BYTE[n]) / 255. The division by 255 is implicit in the fractional representation, where $FF * $FF = $FF (1.0 * 1.0 = 1.0).

This instruction is essential for pixel color multiplication operations used in graphics rendering. For example, multiplying an RGB color by a brightness value: if D contains $80_60_40_20 (RGBA values) and S contains $80_80_80_FF (50% brightness on RGB, full alpha), each color component is reduced to 50% of its original value.

MULPIX executes in 7 clock cycles to perform all four parallel multiplications. This is significantly faster than performing four separate multiply and scale operations, making it practical for real-time graphics processing.

Common uses include:
- Color modulation (tinting): Multiply each color channel by a tint value
- Brightness adjustment: Multiply RGB by a brightness factor
- Alpha premultiplication: Multiply RGB by alpha for compositing
- Texture filtering: Combine texel colors with interpolation weights

The instruction treats all bytes independently, so it can be used for any four-byte parallel multiply operation, not just color processing.



## MULS {#muls}

Multiply signed
[Math and Logic](#math-and-logic) - Multiply two signed 16-bit values to produce a signed 32-bit result.

**MULS**  *Dest, {#}Src*  **{WZ}**

---

**Result:** The 32-bit signed product of the signed lower 16 bits of Dest and Src is stored in Dest.

- Dest is a register containing the signed 16-bit value to multiply with Src, and is where the signed 32-bit result is written.
- Src is a register, 9-bit literal, or signed 16-bit augmented literal whose lower 16 bits are multiplied with Dest.
- WZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010000 | 1ZI | DDDDDDDDD | SSSSSSSSS | D | --- | (D = 0) \| (S = 0) | 2 |


**Related:** [MUL](#mul), [QMUL](#qmul), [SCA](#sca), [SCAS](#scas)

**Explanation:**

MULS performs a signed 16-bit by 16-bit multiplication, taking only the lower 16 bits from each of Dest and Src as signed values, multiplying them together, and storing the full signed 32-bit product into Dest. This is a fast 2-clock multiplication operation suitable for signed integer arithmetic and signed fixed-point calculations.

The operation is: D = signed(D[15:0] * S[15:0]). The upper 16 bits of both Dest and Src are ignored during the multiplication. The lower 16 bits are treated as signed values (using two's complement representation), so values from $8000 (-32768) to $7FFF (+32767) are valid inputs. The 32-bit result is properly sign-extended to represent the full range of products.

For example, multiplying $FFFF_8000 (-32768 in lower 16 bits) by $0000_0002 (+2) produces $FFFF_0000 (-65536 as a signed 32-bit value). The upper 16 bits of the operands are ignored, and the result is correctly signed.

If the WZ effect is specified, the Z flag is set (1) if either Dest or Src equals zero before the multiplication, or is cleared (0) if both are non-zero. Note that this tests the pre-multiplication values, not the result, providing a quick way to detect zero operands.

MULS is commonly used for signed arithmetic and physics calculations:

```pasm
        mov     velocity, signed_speed
        muls    velocity, time          ' velocity = speed * time (signed)
```

For signed fixed-point math with 16-bit fractional parts:

```pasm
        ' Multiply two signed 16.16 fixed-point numbers
        mov     temp, signed_frac1
        muls    temp, signed_frac2      ' Signed multiplication
        sar     temp, #16               ' Arithmetic shift to preserve sign
```

MULS differs from MUL only in that it treats the 16-bit operands as signed values rather than unsigned. The choice between them depends on whether the values being multiplied represent signed or unsigned quantities.

For multiplications larger than 16x16 bits, use the CORDIC solver QMUL instruction, which can multiply full signed 32-bit values and produces a signed 64-bit result accessible through the upper and lower result registers.



## MUXC / MUXNC / MUXZ / MUXNZ {#muxc}

Multiplex flag to bits {#muxnc} {#muxz} {#muxnz}
[Math and Logic](#math-and-logic) - Set selected bits of destination to C, NC, Z, or NZ flag value.

**MUXC**  *D,{#}S*  **{WC|WZ|WCZ}**
**MUXNC**  *D,{#}S*  **{WC|WZ|WCZ}**
**MUXZ**  *D,{#}S*  **{WC|WZ|WCZ}**
**MUXNZ**  *D,{#}S*  **{WC|WZ|WCZ}**

---

**Result:** Each bit position in D where S has a 1 is set to the specified flag value:

| Instruction | Sets bits to |
|-------------|--------------|
| MUXC | C flag value |
| MUXNC | !C (inverted C) |
| MUXZ | Z flag value |
| MUXNZ | !Z (inverted Z) |

- D is a register whose bits will be set to the flag value where S has 1 bits.
- S is a register, 9-bit literal, or 32-bit augmented literal that selects which bits to modify.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0101100 | CZI | DDDDDDDDD | SSSSSSSSS | D | Parity | Result = 0 | 2 |
| EEEE | 0101101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Parity | Result = 0 | 2 |
| EEEE | 0101110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Parity | Result = 0 | 2 |
| EEEE | 0101111 | CZI | DDDDDDDDD | SSSSSSSSS | D | Parity | Result = 0 | 2 |


**Related:** [MUXQ](#muxq), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

These instructions modify selected bits in D based on a flag value. For each bit position where S contains a 1, the corresponding bit in D is replaced with the flag value (or its inverse). All other bits in D remain unchanged. The operation is: D = (!S & D) | (S & {32{flag}}).

MUXC and MUXZ copy the direct flag value; MUXNC and MUXNZ copy the inverted flag value.

Example: Conditionally set bits based on a comparison:

```pasm
        cmp     value, limit  wc        ' Set C if value < limit
        muxc    status, #$01            ' Set bit 0 if less than
        muxnc   status, #$02            ' Set bit 1 if greater or equal
```

If the WC or WCZ effect is specified, the C flag is set to the parity of the result. If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero.

These instructions provide an efficient alternative to conditional branches when setting bits based on flag states.



## MUXNIBS {#muxnibs}

Multiplex nibbles
[Math and Logic](#math-and-logic) - Copy non-zero nibbles from source to destination.

**MUXNIBS**  *Dest, {#}Src*

---

**Result:** Each non-zero nibble in Src replaces the corresponding nibble in Dest.

- Dest is a register whose nibbles will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing nibble values to copy.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001111 | 01I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [MUXNITS](#muxnits), [MUXQ](#muxq), [MOVBYTS](#movbyts), [SPLITB](#splitb)

**Explanation:**

MUXNIBS selectively copies nibbles (4-bit fields) from Src to Dest based on whether each nibble in Src is non-zero. For each of the eight nibble positions, if the nibble in Src is non-zero, that nibble value is copied to the corresponding position in Dest. If the nibble in Src is zero, the corresponding nibble in Dest remains unchanged.

For example, if Dest = $1234_5678 and Src = $0A00_0C0D, the result is Dest = $1A34_5C7D. The nibbles at positions 6 ($A), 2 ($C), and 0 ($D) from Src are copied because they are non-zero, while positions 7, 5, 4, 3, and 1 remain unchanged in Dest because the corresponding Src nibbles are zero.

This instruction is useful for sparse updates where only certain nibbles need modification:

```pasm
        ' Update only the changed nibbles in a configuration register
        mov     config, current_config
        muxnibs config, changes         ' Apply non-zero changes only
```

MUXNIBS is commonly used in graphics operations for palette updates, bit-field modifications where fields are naturally nibble-aligned, and efficient sparse data updates. It provides a single-instruction way to perform selective nibble replacement that would otherwise require multiple mask and merge operations.

The instruction treats nibbles independently, enabling parallel conditional updates across all eight nibble positions in a single 2-clock operation.



## MUXNITS {#muxnits}

Multiplex nits
[Math and Logic](#math-and-logic) - Copy non-zero bit pairs from source to destination.

**MUXNITS**  *Dest, {#}Src*

---

**Result:** Each non-zero bit pair in Src replaces the corresponding bit pair in Dest.

- Dest is a register whose bit pairs will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing bit pair values to copy.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001111 | 00I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [MUXNIBS](#muxnibs), [MUXQ](#muxq), [MOVBYTS](#movbyts), [SPLITB](#splitb)

**Explanation:**

MUXNITS selectively copies bit pairs (2-bit fields, called "nits") from Src to Dest based on whether each bit pair in Src is non-zero. For each of the sixteen bit pair positions, if the bit pair in Src is non-zero (01, 10, or 11), that bit pair value is copied to the corresponding position in Dest. If the bit pair in Src is zero (00), the corresponding bit pair in Dest remains unchanged.

For example, if Dest = $5555_5555 (binary 01_01_01_01... in bit pairs) and Src = $00A0_0002 (containing non-zero bit pairs at positions 11, 9, and 0), only those three bit pairs are updated in Dest while the others remain as 01.

This instruction is particularly useful for pixel graphics operations where 2-bit values represent pixel data (such as in 4-color graphics modes), sparse bit-field updates, and state machine implementations where state variables are represented as 2-bit fields.

MUXNITS provides parallel conditional updates across all sixteen bit pair positions in a single 2-clock operation:

```pasm
        ' Update specific 2-bit fields in a packed structure
        mov     state, current_state
        muxnits state, updates          ' Apply non-zero updates only
```

The name "nits" comes from "nibble bits" or 2-bit fields, representing the next smaller grouping after nibbles (4-bit fields). This instruction complements MUXNIBS by operating at a finer granularity.



## MUXQ {#muxq}

Multiplex Q
[Math and Logic](#math-and-logic) - Copy selected bits from source to destination based on Q register mask.

**MUXQ**  *Dest, {#}Src*

---

**Result:** Bits from Src are copied to Dest at positions where Q has 1 bits.

- Dest is a register whose bits will be updated from Src.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing bit values to copy.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001111 | 10I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [SETQ](#setq), [MUXC](#muxc), [MUXZ](#muxz), [MUXNIBS](#muxnibs), [MUXNITS](#muxnits)

**Explanation:**

MUXQ performs selective bit copying from Src to Dest based on a mask previously loaded into the Q register using SETQ. For each bit position where Q contains a 1, the corresponding bit from Src is copied into Dest. For bit positions where Q contains a 0, the corresponding bit in Dest remains unchanged. The operation is: D = (!Q & D) | (Q & S).

MUXQ must be preceded by SETQ to load the mask into Q:

```pasm
        setq    mask                    ' Load mask into Q
        muxq    dest, source            ' Copy masked bits from source
```

This provides atomic masked bit updates that are more efficient than separate AND and OR operations:

```pasm
        ' Traditional approach (3 instructions):
        andn    dest, mask              ' Clear masked bits
        and     temp, source, mask      ' Extract source bits
        or      dest, temp              ' Merge into dest

        ' MUXQ approach (2 instructions):
        setq    mask                    ' Set mask
        muxq    dest, source            ' Atomic masked copy
```

MUXQ is critical for parallel I/O operations, especially driving multiple pins simultaneously:

```pasm
        ' Update multiple RGB LED pins atomically
        setq    rgb_mask                ' Mask for RGB pins
        muxq    outa, rgb_data          ' Update all RGB pins together
```

The Q register mask enables sophisticated bit manipulation:

```pasm
        ' Update specific configuration bits
        setq    ##$00FF_FF00            ' Mask for middle bytes
        muxq    config, new_values      ' Update only those bytes
```

MUXQ is particularly valuable for HUB75 RGB panel driving and other applications requiring atomic multi-pin updates. It executes in 2 clock cycles, providing high-performance parallel bit operations essential for real-time graphics and control applications.

Unlike MUXC and MUXZ which replicate a single flag bit to all selected positions, MUXQ copies the actual corresponding bits from the source, enabling true parallel bit transfer operations.




# Instructions: N

This section contains all PASM2 instructions beginning with the letter N.



## NEG {#neg}

Negate
[Math and Logic](#math-and-logic) - Negate a value.

**NEG**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEG**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The Src or Dest value is negated and stored into Dest.

- Dest is a register to receive the -Src value (syntax 1), or contains the value to negate (syntax 2).
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose negated value is stored into Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0110011 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign of result | Result = 0 | 2 |
| EEEE | 0110011 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | Sign of result | Result = 0 | 2 |


**Related:** [ABS](#abs), [NEGC](#negc), [NEGNC](#negnc), [NEGZ](#negz), [NEGNZ](#negnz)

**Explanation:**

NEG negates the value in Src (syntax 1) or Dest (syntax 2) and stores the result in the Dest register. The negation flips the value's sign; for example, 78 becomes -78, or -306 becomes 306.

When using syntax 1, NEG negates the Src operand and stores the result into Dest. When using syntax 2 (where Src is omitted), NEG negates the value already in Dest and stores the result back into Dest.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative, or is cleared (0) if positive.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.



## NEGC / NEGNC / NEGZ / NEGNZ {#negc}

Conditional negate {#negnc} {#negz} {#negnz}
[Math and Logic](#math-and-logic) - Negate value according to C, NC, Z, or NZ flag.

**NEGC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEGC**  *Dest*  **{WC|WZ|WCZ}**

**NEGNC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEGNC**  *Dest*  **{WC|WZ|WCZ}**

**NEGZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEGZ**  *Dest*  **{WC|WZ|WCZ}**

**NEGNZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NEGNZ**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The Src or Dest value, conditionally negated based on flag state, is stored into Dest.

| Instruction | Negates when |
|-------------|--------------|
| NEGC | C = 1 |
| NEGNC | C = 0 |
| NEGZ | Z = 1 |
| NEGNZ | Z = 0 |

- Dest is a register to receive the result.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0110100 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0110100 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | Sign | Result = 0 | 2 |
| EEEE | 0110101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0110101 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | Sign | Result = 0 | 2 |
| EEEE | 0110110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0110110 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | Sign | Result = 0 | 2 |
| EEEE | 0110111 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0110111 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | Sign | Result = 0 | 2 |


**Related:** [NEG](#neg)

**Explanation:**

These instructions conditionally negate the value in Src (two-operand form) or Dest (single-operand form) based on the specified flag condition. If the condition is true, the value is negated (sign flipped) before being stored in Dest. If the condition is false, the value is stored unchanged.

NEGC and NEGZ negate when their flag is set (1). NEGNC and NEGNZ negate when their flag is clear (0), providing complementary behavior.

If the WC or WCZ effect is specified, the C flag is set (1) if the result is negative, or cleared (0) if positive.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result is zero, or cleared (0) if non-zero.



## NIXINT1 / NIXINT2 / NIXINT3 {#nixint1}

Cancel interrupt (1, 2, or 3)
[Event](#event) - Cancel INTn interrupt.

**NIXINT1**
**NIXINT2**
**NIXINT3**

---

**Result:** The specified interrupt event (INT1, INT2, or INT3) is cancelled.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | 000100101 | 000100100 | --- | --- | --- | 2 |
| EEEE | 1101011 | 000 | 000100110 | 000100100 | --- | --- | --- | 2 |
| EEEE | 1101011 | 000 | 000100111 | 000100100 | --- | --- | --- | 2 |


**Related:** [SETINT1/2/3](instructions-s.md#setint1), [TRGINT1/2/3](instructions-t.md#trgint1), [RETI0/1/2/3](instructions-r.md#reti0), [RESI0/1/2/3](instructions-r.md#resi0)

**Explanation:**

NIXINT1, NIXINT2, and NIXINT3 cancel any pending interrupt events for their respective interrupt levels. These instructions prevent the interrupt from occurring even if its event condition has been met.

The P2 provides three independent interrupt levels, and each NIXINT instruction cancels only its corresponding level. Use these instructions when an interrupt that was previously configured is no longer needed or when the program needs to explicitly clear a pending interrupt condition before it can trigger cog execution flow changes.



## NOP {#nop}

No operation
[Miscellaneous](#miscellaneous) - No operation, just elapse two cycles.

**NOP**

---

**Result:** Two clock cycles are consumed.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| 0000 | 0000000 | 000 | 000000000 | 000000000 | --- | --- | --- | 2 |


**Related:** [WAITX](#waitx), [WAITCNT](#waitcnt)

**Explanation:**

NOP simply consumes two clock cycles without performing any operation. No registers are modified, no flags are affected, and no memory is accessed.

NOP is primarily used for timing adjustments, creating precise delays, or as a placeholder during development. It can also be used to align code for performance optimization or to fill instruction slots in pipelined operations.



## NOT {#not}

Not
[Math and Logic](#math-and-logic) - Bitwise NOT a value.

**NOT**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**NOT**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The bitwise NOT of Src or Dest is stored in Dest.

- Dest is the register containing the value to bitwise NOT (syntax 2) or to be replaced by the bitwise NOT of Src (syntax 1).
- Src is an optional register, 9-bit literal, or 32-bit augmented literal whose value will be bitwise NOTed and stored into Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0110001 | CZI | DDDDDDDDD | SSSSSSSSS | D | !S[31] | Result = 0 | 2 |
| EEEE | 0110001 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | !D[31] | Result = 0 | 2 |


**Related:** [AND](#and), [OR](#or), [XOR](#xor), [ANDN](#andn)

**Explanation:**

NOT performs a bitwise NOT operation, inverting all bits of the value in Src (syntax 1) or Dest (syntax 2), and stores the result into Dest. Each 0 bit becomes 1, and each 1 bit becomes 0.

When using syntax 1, NOT inverts the Src operand and stores the result into Dest. When using syntax 2 (where Src is omitted), NOT inverts the value already in Dest and stores the result back into Dest.

If the WC or WCZ effect is specified, the C flag is set to the inverse of bit 31 of the source operand. For syntax 1, this is the inverse of S[31]; for syntax 2, this is the inverse of D[31].

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if it is non-zero.



# Instructions: O

This section contains all PASM2 instructions beginning with the letter O.



## ONES {#ones}

Ones
[Math and Logic](#math-and-logic) - Count the number of high bits (1s) in a value.

**ONES**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**ONES**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The number of high bits (1s) in Src, or Dest, is stored in Dest.

- Dest is a register where the count of high bits is stored, and optionally contains the value to check (second syntax form).
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is checked for ones.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Result is odd | Result = 0 | 2 |
| EEEE | 0111101 | CZ0 | DDDDDDDDD | DDDDDDDDD | D | Result is odd | Result = 0 | 2 |


**Related:** [TEST](#test), [TESTB](#testb), [TESTBN](#testbn), [BITNOT](#bitnot)

**Explanation:**

ONES tallies the number of high bits (1s) in the specified value and stores the count in Dest. This is a population count (popcount) operation commonly used for bit manipulation and analysis.

When Src is provided in the first syntax form, ONES counts the high bits in Src and stores the result (0 to 32) in Dest. When Src is omitted in the second syntax form, ONES counts the high bits in Dest itself and replaces Dest with the count.

If the WC or WCZ effect is specified, the C flag is set (1) if the count is odd, or is cleared (0) if the count is even. This provides a parity check on the number of high bits.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero (no high bits were found), or is cleared (0) if the result is non-zero (at least one high bit exists).

ONES is useful for analyzing bit patterns, counting enabled flags, and implementing parity checks in data transmission protocols.



## OR {#or}

Or
[Math and Logic](#math-and-logic) - Perform bitwise OR operation.

**OR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Dest OR Src is stored in Dest.

- Dest is a register containing the value to bitwise OR with Src, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is bitwise ORed into Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0101010 | CZI | DDDDDDDDD | SSSSSSSSS | D | Parity of Result | Result = 0 | 2 |


**Related:** [AND](#and), [XOR](#xor), [ANDN](#andn), [NOT](#not)

**Explanation:**

OR performs a bitwise OR operation between the values in Dest and Src, storing the result in Dest. Each bit position in the result is set (1) if the corresponding bit in either Dest or Src (or both) is set, and is cleared (0) only if both corresponding bits are cleared.

The bitwise OR operation follows this truth table for each bit position:

```
Dest  Src   Result
  0    0      0
  0    1      1
  1    0      1
  1    1      1
```

If the WC or WCZ effect is specified, the C flag is set (1) if the result contains an odd number of high bits, or is cleared (0) if it contains an even number of high bits. This provides a parity indication of the result.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if the result is non-zero. Note that the result can only be zero if both Dest and Src were zero.

OR is commonly used for setting specific bits in a value, combining bit masks, and implementing logical operations in algorithms.



## OUTC / OUTNC / OUTZ / OUTNZ {#outc}

Output by flag state {#outnc} {#outz} {#outnz}
[Pin](#pin) - Set pin output level according to C, NC, Z, or NZ flag state.

**OUTC**  *{#}Dest*  **{WCZ}**
**OUTNC**  *{#}Dest*  **{WCZ}**
**OUTZ**  *{#}Dest*  **{WCZ}**
**OUTNZ**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are set according to the flag state:

| Instruction | Drives high when |
|-------------|------------------|
| OUTC | C = 1 |
| OUTNC | C = 0 |
| OUTZ | Z = 1 |
| OUTNZ | Z = 0 |

- Dest identifies the I/O pin(s): Dest[5:0] = base pin (0-63), Dest[10:6] = additional contiguous pins.
- WCZ is an optional effect to set Z to the original output state.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001010 | OUTx | --- | orig out | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001011 | OUTx | --- | orig out | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001100 | OUTx | --- | orig out | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001101 | OUTx | --- | orig out | 2 |


**Related:** [OUTH](#outh), [OUTL](#outl), [OUTNOT](#outnot), [OUTRND](#outrnd)

**Explanation:**

These instructions set pin output level(s) based on flag state. OUTC and OUTZ drive high when their flag is set; OUTNC and OUTNZ drive high when their flag is clear.

If WCZ is specified, the Z flag is set to the original output state of the base pin before modification.



## OUTH {#outh}

Output high
[Pin](#pin) - Set pin output level to high.

**OUTH**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are set high (1).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set high.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001001 | OUTx | --- | Original OUTx base bit | 2 |


**Related:** [OUTL](#outl), [OUTNOT](#outnot), [OUTC](#outc), [OUTNC](#outnc), [DIRH](#dirh)

**Explanation:**

OUTH sets the output level of the pin(s) specified by Dest to high (1), driving them to the high voltage level. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTH is commonly used to turn on LEDs, assert control signals, or drive pins high for any digital output purpose. For the output level change to affect the actual pin voltage, the pin must also be configured as an output using the direction control instructions.



## OUTL {#outl}

Output low
[Pin](#pin) - Set pin output level to low.

**OUTL**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are set low (0).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set low.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001000 | OUTx | --- | Original OUTx base bit | 2 |


**Related:** [OUTH](#outh), [OUTNOT](#outnot), [OUTC](#outc), [OUTNC](#outnc), [DIRL](#dirl)

**Explanation:**

OUTL sets the output level of the pin(s) specified by Dest to low (0), driving them to the low voltage level (typically ground). All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTL is commonly used to turn off LEDs, de-assert control signals, or drive pins low for any digital output purpose. For the output level change to affect the actual pin voltage, the pin must also be configured as an output using the direction control instructions.



## OUTNOT {#outnot}

Output not (toggle)
[Pin](#pin) - Toggle pin output level to opposite state.

**OUTNOT**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are toggled to their opposite state(s).

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to toggle.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001111 | OUTx | --- | Original OUTx base bit | 2 |


**Related:** [OUTH](#outh), [OUTL](#outl), [OUTRND](#outrnd), [NOT](#not), [DRVNOT](#drvnot)

**Explanation:**

OUTNOT toggles the output level of the pin(s) specified by Dest to their opposite state. Pins that were high (1) become low (0), and pins that were low become high. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only these lower 6 bits matter. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6]). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

If the WCZ effect is specified, the Z flag is set to the original state of the output level bit for the base pin, before the instruction executes. The C flag is not affected by this instruction.

OUTNOT is commonly used for blinking LEDs, generating clock signals, or toggling any output that needs to alternate states. It is particularly efficient for creating square waves or implementing state machines that alternate between two states.



## OUTRND {#outrnd}

Output random
[Pin](#pin) - Set pin output level(s) to random values.

**OUTRND**  *{#}Dest*  **{WCZ}**

---

**Result:** The I/O pin output level bit(s) described by Dest are each set randomly to low or high.

- Dest is a register, 9-bit literal, or 11-bit augmented literal whose value identifies the I/O pin(s) to set to random output levels.
- WCZ is an optional effect to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001001110 | OUTx | Original OUTx base bit | Original OUTx base bit | 2 |


**Related:** [OUTC](#outc), [OUTNC](#outnc), [OUTZ](#outz), [OUTNZ](#outnz), [OUTH](#outh), [OUTL](#outl), [OUTNOT](#outnot)

**Explanation:**

OUTRND sets the output level of the pin(s) specified by Dest to random low and high states, using bits from the hardware Xoroshiro128** pseudo-random number generator (PRNG). Each affected pin is independently set to either low (0) or high (1) based on successive bits from the PRNG. All other output level bits remain unchanged.

Dest[5:0] specifies the base pin number (0-63). For controlling a single pin, only this lower 6-bit value matters. For controlling a range of contiguous pins, Dest[10:6] specifies how many additional pins beyond the base should be affected (0-31, where 0 means just the base pin, 1 means base plus one additional pin, etc.).

A 9-bit literal Dest can express the base pin (bits [5:0]) and up to 7 additional pins (bits [8:6], allowing control of 1 to 8 contiguous pins). To specify a wider range, use the augmented literal prefix (##Dest) to provide an 11-bit value, which allows controlling up to 32 contiguous pins.

When Dest is a register, the register's bits [10:0] are used directly to form the 11-bit pin range specification. However, if a SETQ instruction immediately precedes OUTRND, then SETQ's Dest[4:0] is substituted for the register's bits [10:6], allowing dynamic control of the pin range.

If the WCZ effect is specified, both the C and Z flags are set to the original state of the output level bit for the base pin, before the instruction executes.

OUTRND is useful for generating random visual patterns on LEDs, creating noise signals for testing or audio applications, or implementing randomized control sequences. The quality of randomness depends on proper initialization of the PRNG using the SETRAND instruction.




# Instructions: P

This section contains all PASM2 instructions beginning with the letter P.



## POLLATN {#pollatn}

Poll attention event
[Event](#event) - Check attention event flag without waiting.

**POLLATN**  **{WC|WZ|WCZ}**

---

**Result:** Attention event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001110 | 000100100 | --- | ATN Event | ATN Event | 2 |


**Related:** [COGATN](#cogatn), [WAITATN](#waitatn), [JATN](#jatn), [JNATN](#jnatn)

**Explanation:**

POLLATN copies the state of the attention event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the attention event flag prior to clearing it.

The attention event flag is set whenever another cog issues an attention request for this cog using COGATN. The flag is cleared upon cog start, or execution of POLLATN, WAITATN, JATN, or JNATN instructions.

This instruction enables inter-cog communication by allowing a cog to check whether another cog has requested its attention without blocking execution.



## POLLCT1 / POLLCT2 / POLLCT3 {#pollct1}

Poll counter event (1, 2, or 3)
[Event](#event) - Check counter event flag without waiting.

**POLLCT1**  **{WC|WZ|WCZ}**
**POLLCT2**  **{WC|WZ|WCZ}**
**POLLCT3**  **{WC|WZ|WCZ}**

---

**Result:** CTn event flag state is optionally copied into C and/or Z, then the flag is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000001 | 000100100 | --- | CT1 Event | CT1 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000010 | 000100100 | --- | CT2 Event | CT2 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000011 | 000100100 | --- | CT3 Event | CT3 Event | 2 |


**Related:** [ADDCT1/2/3](#addct1), [WAITCT1/2/3](#waitct1), [JCT1/2/3](#jct1), [JNCT1/2/3](#jnct1)

**Explanation:**

POLLCT1, POLLCT2, and POLLCT3 copy the state of their respective counter event flags into C and/or Z and then clear the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the counter event flag prior to clearing it.

Each counter event flag is set whenever the System Counter (CT) passes the value in that counter's event trigger register; that is, the MSB of (CT - CTn) is 0. The counter event flag is cleared upon execution of ADDCTn, POLLCTn, WAITCTn, JCTn, or JNCTn.

These instructions enable time-based event polling without blocking execution. The P2 provides three independent counter event triggers (CT1, CT2, CT3) allowing a cog to simultaneously track multiple timing requirements.



## POLLFBW {#pollfbw}

Poll FIFO block wrap event
[Event](#event) - Check FIFO block wrap event flag without waiting.

**POLLFBW**  **{WC|WZ|WCZ}**

---

**Result:** FIFO-interface-block-wrap event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001001 | 000100100 | --- | FBW Event | FBW Event | 2 |


**Related:** [RDFAST](#rdfast), [WRFAST](#wrfast), [FBLOCK](#fblock), [WAITFBW](#waitfbw), [JFBW](#jfbw), [JNFBW](#jnfbw)

**Explanation:**

POLLFBW copies the state of the FIFO-interface-block-wrap event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The FIFO-interface-block-wrap event flag is set whenever the Hub RAM FIFO interface exhausts its block count and reloads its block count and start address. The flag is cleared upon execution of RDFAST, WRFAST, FBLOCK, POLLFBW, WAITFBW, JFBW, or JNFBW instructions.

This instruction enables circular buffer management for high-speed Hub RAM transfers.



## POLLINT {#pollint}

Poll interrupt event
[Event](#event) - Check interrupt event flag without waiting.

**POLLINT**  **{WC|WZ|WCZ}**

---

**Result:** Interrupt-occurred event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000000 | 000100100 | --- | INT Event | INT Event | 2 |


**Related:** [WAITINT](#waitint), [JINT](#jint), [JNINT](#jnint)

**Explanation:**

POLLINT copies the state of the interrupt-occurred event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The interrupt-occurred event flag is set whenever interrupt 1, 2, or 3 occurs. Debug interrupts are ignored. The flag is cleared upon cog start, or execution of POLLINT, WAITINT, JINT, or JNINT instructions.

This instruction enables non-blocking interrupt handling.



## POLLPAT {#pollpat}

Poll pin pattern event
[Event](#event) - Check pin pattern event flag without waiting.

**POLLPAT**  **{WC|WZ|WCZ}**

---

**Result:** Pin-pattern-detected event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001000 | 000100100 | --- | PAT Event | PAT Event | 2 |


**Related:** [SETPAT](#setpat), [WAITPAT](#waitpat), [JPAT](#jpat), [JNPAT](#jnpat)

**Explanation:**

POLLPAT copies the state of the pin-pattern-detected event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The pin-pattern-detected event flag is set whenever the masked input pins match or don't match the pattern described by a previous SETPAT instruction. The flag is cleared upon execution of SETPAT, POLLPAT, WAITPAT, JPAT, or JNPAT instructions.

This instruction enables non-blocking pattern detection on input pins.



## POLLQMT {#pollqmt}

Poll CORDIC empty event
[Event](#event) - Check CORDIC-read-but-empty event flag without waiting.

**POLLQMT**  **{WC|WZ|WCZ}**

---

**Result:** CORDIC-read-but-empty event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001111 | 000100100 | --- | QMT Event | QMT Event | 2 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [JQMT](#jqmt), [JNQMT](#jnqmt)

**Explanation:**

POLLQMT copies the state of the CORDIC-read-but-empty event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The CORDIC-read-but-empty event flag is set whenever GETQX or GETQY executes without any CORDIC results available or in progress. The flag is cleared upon cog start or execution of POLLQMT, WAITQMT, JQMT, or JNQMT instructions.

This instruction enables error detection for CORDIC operations.



## POLLSE1 / POLLSE2 / POLLSE3 / POLLSE4 {#pollse1}

Poll selectable event (1, 2, 3, or 4)
[Event](#event) - Check selectable event flag without waiting.

**POLLSE1**  **{WC|WZ|WCZ}**
**POLLSE2**  **{WC|WZ|WCZ}**
**POLLSE3**  **{WC|WZ|WCZ}**
**POLLSE4**  **{WC|WZ|WCZ}**

---

**Result:** SEn event flag state is optionally copied into C and/or Z, then the flag is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000000100 | 000100100 | --- | SE1 Event | SE1 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000101 | 000100100 | --- | SE2 Event | SE2 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000110 | 000100100 | --- | SE3 Event | SE3 Event | 2 |
| EEEE | 1101011 | CZ0 | 000000111 | 000100100 | --- | SE4 Event | SE4 Event | 2 |


**Related:** [SETSE1/2/3/4](#setse1), [WAITSE1/2/3/4](#waitse1), [JSE1/2/3/4](#jse1), [JNSE1/2/3/4](#jnse1)

**Explanation:**

POLLSE1, POLLSE2, POLLSE3, and POLLSE4 copy the state of their respective selectable event flags into C and/or Z and then clear the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the selectable event flag prior to clearing it.

Each selectable event flag is set whenever the corresponding configured event occurs. The flag is cleared upon execution of SETSEn, POLLSEn, WAITSEn, JSEn, or JNSEn instructions.

The P2 provides four independent selectable event generators that can be configured to monitor various hardware conditions.



## POLLXFI {#pollxfi}

Poll streamer finished event
[Event](#event) - Check streamer-finished event flag without waiting.

**POLLXFI**  **{WC|WZ|WCZ}**

---

**Result:** Streamer-finished event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001011 | 000100100 | --- | XFI Event | XFI Event | 2 |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XCONT](#xcont), [WAITXFI](#waitxfi), [JXFI](#jxfi), [JNXFI](#jnxfi)

**Explanation:**

POLLXFI copies the state of the streamer-finished event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-finished event flag is set whenever the streamer runs out of commands to process. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXFI, WAITXFI, JXFI, or JNXFI instructions.

This instruction enables non-blocking management of the streamer subsystem.



## POLLXMT {#pollxmt}

Poll streamer empty event
[Event](#event) - Check streamer-empty event flag without waiting.

**POLLXMT**  **{WC|WZ|WCZ}**

---

**Result:** Streamer-empty event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001010 | 000100100 | --- | XMT Event | XMT Event | 2 |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XCONT](#xcont), [WAITXMT](#waitxmt), [JXMT](#jxmt), [JNXMT](#jnxmt)

**Explanation:**

POLLXMT copies the state of the streamer-empty event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-empty event flag is set whenever the streamer is ready for a new command. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXMT, WAITXMT, JXMT, or JNXMT instructions.

This instruction enables pipelined streamer operations.



## POLLXRL {#pollxrl}

Poll streamer LUT rollover event
[Event](#event) - Check streamer LUT rollover event flag without waiting.

**POLLXRL**  **{WC|WZ|WCZ}**

---

**Result:** Streamer-LUT-RAM-rollover event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001101 | 000100100 | --- | XRL Event | XRL Event | 2 |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XCONT](#xcont), [WAITXRL](#waitxrl), [JXRL](#jxrl), [JNXRL](#jnxrl)

**Explanation:**

POLLXRL copies the state of the streamer-LUT-RAM-rollover event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-LUT-RAM-rollover event flag is set whenever location $1FF of the Lookup RAM is read by the streamer. The flag is cleared upon cog start or upon execution of POLLXRL, WAITXRL, JXRL, or JNXRL instructions.

This instruction enables circular buffer management when using LUT RAM as a streamer data source.



## POLLXRO {#pollxro}

Poll streamer NCO rollover event
[Event](#event) - Check streamer NCO rollover event flag without waiting.

**POLLXRO**  **{WC|WZ|WCZ}**

---

**Result:** Streamer-NCO-rollover event flag is optionally copied into C and/or Z, then it is cleared.

- WC, WZ, or WCZ are optional effects to capture the event state into flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000001100 | 000100100 | --- | XRO Event | XRO Event | 2 |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XCONT](#xcont), [WAITXRO](#waitxro), [JXRO](#jxro), [JNXRO](#jnxro)

**Explanation:**

POLLXRO copies the state of the streamer NCO rollover event flag into C and/or Z and then clears the flag (unless it's being set again by the event sensor). If the WC, WZ, or WCZ effect is specified, the C flag and/or Z flag is updated to the state of the event flag prior to clearing it.

The streamer-NCO-rollover event flag is set whenever the streamer's numerically-controlled oscillator (NCO) rolls over. The flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXRO, WAITXRO, JXRO, or JNXRO instructions.

This instruction enables precise timing control for streamer operations that use the NCO for rate control.



## POP {#pop}

Pop from internal stack
[Miscellaneous](#miscellaneous) - Pop a value from the internal K register stack.

**POP**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Dest receives the value from the K register.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000101011 | D | K[31] | Result = 0 | 2 |


**Related:** [PUSH](#push), [POPA](#popa), [POPB](#popb)

**Explanation:**

POP pops the internal stack register K into the destination register Dest. The P2 provides a single-level internal stack register K that is automatically used by CALL instructions to store the return address.

If the WC or WCZ effect is specified, the C flag is set to bit 31 of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

POP retrieves this value, typically as part of a return sequence, though it can also be used to retrieve any value previously stored with PUSH.



## POPA {#popa}

Pop from Hub stack A
[Hub RAM](#hub-ram) - Pop a long value from Hub RAM using PTRA as stack pointer.

**POPA**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Dest receives the long value from Hub address --PTRA.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZ1 | DDDDDDDDD | 101011111 | D | MSB of long | Result = 0 | 9...16 |


**Related:** [PUSHA](#pusha), [POPB](#popb), [POP](#pop)

**Explanation:**

POPA reads a long from Hub address --PTRA into the destination register Dest. PTRA is automatically decremented by 4 before the read occurs (pre-decrement), implementing a descending stack model where the stack grows downward in memory.

If the WC or WCZ effect is specified, the C flag is set to the MSB (bit 31) of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

This instruction enables Hub RAM-based stacks for deep subroutine nesting and large temporary storage.



## POPB {#popb}

Pop from Hub stack B
[Hub RAM](#hub-ram) - Pop a long value from Hub RAM using PTRB as stack pointer.

**POPB**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** Dest receives the long value from Hub address --PTRB.

- Dest is the register to receive the popped value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZ1 | DDDDDDDDD | 111011111 | D | MSB of long | Result = 0 | 9...16 |


**Related:** [PUSHB](#pushb), [POPA](#popa), [POP](#pop)

**Explanation:**

POPB reads a long from Hub address --PTRB into the destination register Dest. PTRB is automatically decremented by 4 before the read occurs (pre-decrement), implementing a descending stack model where the stack grows downward in memory.

If the WC or WCZ effect is specified, the C flag is set to the MSB (bit 31) of the popped value.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the popped value equals zero, or is cleared (0) if non-zero.

Having two independent Hub stack pointers (PTRA and PTRB) allows a cog to manage separate stacks for different purposes.



## PUSH {#push}

Push to internal stack
[Miscellaneous](#miscellaneous) - Push a value onto the internal K register stack.

**PUSH**  *{#}Dest*

---

**Result:** The value from Dest (or immediate value) is stored in the K register.

- Dest is a register or 9-bit immediate value (0-511) to push.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000101010 | --- | --- | --- | 2 |


**Related:** [POP](#pop), [PUSHA](#pusha), [PUSHB](#pushb)

**Explanation:**

PUSH pushes the value in Dest (or an immediate value 0-511) onto the internal stack register K. This instruction does not affect any flags.

The P2 provides a single-level internal stack register K that is automatically used by CALL instructions to store the return address. PUSH can be used to save other values in K, though this overwrites any return address that may be stored there.



## PUSHA {#pusha}

Push to Hub stack A
[Hub RAM](#hub-ram) - Push a long value to Hub RAM using PTRA as stack pointer.

**PUSHA**  *{#}Dest*

---

**Result:** The long value from Dest is written to Hub address PTRA++.

- Dest is a register or 9-bit immediate value to push.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0L1 | DDDDDDDDD | 101100001 | --- | --- | --- | 3...10 |


**Related:** [POPA](#popa), [PUSHB](#pushb), [PUSH](#push)

**Explanation:**

PUSHA writes the long value in Dest (or a 9-bit immediate value) to Hub address PTRA++. PTRA is automatically incremented by 4 after the write occurs (post-increment).

This instruction does not affect any flags. The post-increment model means PTRA always points to the next available stack location after the push operation.

PUSHA paired with POPA implements a descending stack in Hub RAM.



## PUSHB {#pushb}

Push to Hub stack B
[Hub RAM](#hub-ram) - Push a long value to Hub RAM using PTRB as stack pointer.

**PUSHB**  *{#}Dest*

---

**Result:** The long value from Dest is written to Hub address PTRB++.

- Dest is a register or 9-bit immediate value to push.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0L1 | DDDDDDDDD | 111100001 | --- | --- | --- | 3...10 |


**Related:** [POPB](#popb), [PUSHA](#pusha), [PUSH](#push)

**Explanation:**

PUSHB writes the long value in Dest (or a 9-bit immediate value) to Hub address PTRB++. PTRB is automatically incremented by 4 after the write occurs (post-increment).

This instruction does not affect any flags. The post-increment model means PTRB always points to the next available stack location after the push operation.

Having two independent Hub stack pointers (PTRA and PTRB) allows a cog to manage separate stacks for different purposes.


# Instructions: Q

This section contains all PASM2 instructions beginning with the letter Q. The Q instructions are part of the CORDIC coprocessor family.



## QDIV {#qdiv}

Queue divide
[CORDIC Solver](#cordic-solver) - Perform 64÷32 unsigned division with 32-bit quotient and remainder.

**QDIV**  *{#}Dest, {#}Src*

---

**Result:** Divides a 64-bit numerator by a 32-bit denominator, producing a 32-bit quotient (GETQX) and remainder (GETQY) 55 clocks later.

- Dest is a register or literal containing the lower 32 bits of the 64-bit numerator.
- Src is a register or literal containing the 32-bit denominator (divisor).
- Use SETQ before QDIV to specify the upper 32 bits of the numerator (defaults to 0 if not used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101000 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QFRAC](#qfrac), [QMUL](#qmul)

**Explanation:**

QDIV performs high-precision unsigned division using the P2's 54-stage pipelined CORDIC solver. It divides a 64-bit numerator by a 32-bit denominator, producing both a 32-bit quotient and 32-bit remainder.

The 64-bit numerator is formed by concatenating the SETQ value (or 0 if SETQ not used) as the upper 32 bits with the Dest operand as the lower 32 bits: {SETQ, Dest}. The denominator is specified in the Src operand. After 55 clocks, the quotient can be retrieved using GETQX and the remainder using GETQY.

::: pasm2
        QDIV    #1000000, #3   ' {0, 1000000} / 3
        ' Wait 55 clocks...
        GETQX   quotient       ' Get 333333
        GETQY   remainder      ' Get 1
:::

Division by zero produces undefined results. Each cog can issue one CORDIC instruction per hub window (every 8 clocks).



## QEXP {#qexp}

Queue exponential
[CORDIC Solver](#cordic-solver) - Convert 5:27-bit logarithm to 32-bit unsigned integer.

**QEXP**  *{#}Dest*

---

**Result:** Converts a 5:27-bit logarithm format into a 32-bit unsigned integer, retrieved via GETQX 55 clocks later.

- Dest is a register or literal containing the 5:27-bit logarithm (5-bit exponent in bits [31:27], 27-bit fraction in bits [26:0]).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000001111 | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [QLOG](#qlog), [QMUL](#qmul)

**Explanation:**

QEXP performs logarithm to integer conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 5:27-bit logarithm format into a 32-bit unsigned integer, effectively computing the exponential (antilog) of the input.

The instruction takes the logarithm value in the Dest operand, which must be in P2's 5:27 format where bits [31:27] contain the 5-bit whole exponent and bits [26:0] contain the 27-bit fractional exponent. After 55 clocks, the integer result can be retrieved using GETQX.

QEXP is the complement of QLOG and is commonly used together with QLOG to perform power calculations.

::: pasm2
        QEXP    log_value      ' Begin exponential conversion
        ' Wait 55 clocks...
        GETQX   integer_result ' Get 32-bit integer
:::



## QFRAC {#qfrac}

Queue fractional divide
[CORDIC Solver](#cordic-solver) - Perform 64÷32 unsigned fractional division.

**QFRAC**  *{#}Dest, {#}Src*

---

**Result:** Divides a 64-bit numerator by a 32-bit denominator, producing a 32-bit quotient (GETQX) and remainder (GETQY) 55 clocks later.

- Dest is a register or literal containing the upper 32 bits of the 64-bit numerator.
- Src is a register or literal containing the 32-bit denominator (divisor).
- Use SETQ before QFRAC to specify the lower 32 bits of the numerator (defaults to 0 if not used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101001 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QDIV](#qdiv), [QMUL](#qmul)

**Explanation:**

QFRAC performs fractional division using the P2's 54-stage pipelined CORDIC solver. It divides a 64-bit numerator by a 32-bit denominator, but differs from QDIV in the operand arrangement: Dest forms the upper 32 bits while SETQ (or 0) forms the lower 32 bits.

The 64-bit numerator is formed as {Dest, SETQ}. This arrangement makes QFRAC particularly suitable for fractional arithmetic where the integer part is in Dest and the fractional part is in SETQ.

::: pasm2
        SETQ    #$C0000000     ' 0.75 in 32-bit fraction format
        QFRAC   #5, #2         ' {5, 0.75} / 2 = 2.875
        ' Wait 55 clocks...
        GETQX   quotient       ' Get integer quotient
        GETQY   remainder      ' Get fractional remainder
:::



## QLOG {#qlog}

Queue logarithm
[CORDIC Solver](#cordic-solver) - Convert 32-bit unsigned integer to 5:27-bit logarithm.

**QLOG**  *{#}Dest*

---

**Result:** Converts a 32-bit unsigned integer into a 5:27-bit logarithm format, retrieved via GETQX 55 clocks later.

- Dest is a register or literal containing the 32-bit unsigned integer input.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000001110 | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [QEXP](#qexp)

**Explanation:**

QLOG performs integer to logarithm conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 32-bit unsigned integer into a 5:27-bit logarithm format, where the result contains a 5-bit whole exponent in bits [31:27] and a 27-bit fractional exponent in bits [26:0].

The instruction takes the unsigned integer value in the Dest operand. After 55 clocks, the logarithm result can be retrieved using GETQX.

::: pasm2
        QLOG    #1000          ' Begin log conversion
        ' Wait 55 clocks...
        GETQX   log_result     ' Get 5:27 logarithm
:::



## QMUL {#qmul}

Queue multiply
[CORDIC Solver](#cordic-solver) - Perform 32×32 unsigned multiplication producing 64-bit result.

**QMUL**  *{#}Dest, {#}Src*

---

**Result:** Multiplies two 32-bit unsigned values, producing a 64-bit result with lower 32 bits via GETQX and upper 32 bits via GETQY, 55 clocks later.

- Dest is a register or literal containing the first 32-bit multiplicand.
- Src is a register or literal containing the second 32-bit multiplicand.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101000 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [QDIV](#qdiv), [QFRAC](#qfrac)

**Explanation:**

QMUL performs high-precision unsigned multiplication using the P2's 54-stage pipelined CORDIC solver. It multiplies two 32-bit unsigned integers (Dest × Src) and produces a full 64-bit product, avoiding the precision loss that would occur with standard 32-bit multiplication.

After 55 clocks, the 64-bit result can be retrieved using GETQX for the lower 32 bits and GETQY for the upper 32 bits.

::: pasm2
        QMUL    #1000000, #2000000
        ' Wait 55 clocks...
        GETQX   lower_32       ' Get lower 32 bits
        GETQY   upper_32       ' Get upper 32 bits
:::

Each cog can issue one CORDIC instruction per hub window (every 8 clocks), allowing efficient pipelining.



## QROTATE {#qrotate}

Queue rotate
[CORDIC Solver](#cordic-solver) - Rotate a 32-bit signed (X, Y) point around origin by specified angle.

**QROTATE**  *{#}Dest, {#}Src*

---

**Result:** Rotates a coordinate pair around the origin, producing new X (GETQX) and Y (GETQY) coordinates 55 clocks later.

- Dest is a register or literal containing the X coordinate (32-bit signed).
- Src is a register or literal containing the rotation angle in P2 angle units ($00000000 = 0°, $40000000 = 90°, $80000000 = 180°, $C0000000 = 270°).
- Use SETQ before QROTATE to specify the Y coordinate (defaults to 0 if not used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101010 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QVECTOR](#qvector)

**Explanation:**

QROTATE performs point rotation using the P2's 54-stage pipelined CORDIC solver. It rotates a 32-bit signed (X, Y) coordinate pair around the origin (0, 0) by a specified angle, producing new 32-bit signed (X, Y) results.

The instruction takes the X coordinate from Dest and the Y coordinate from the SETQ value (or 0 if SETQ was not used). The rotation angle is specified in Src using P2's standard angle units.

This instruction can also be used for polar to cartesian conversion by setting X (Dest) to the length, Y (SETQ) to 0, and the angle (Src) to the desired angle.

::: pasm2
        SETQ    #200           ' Set Y coordinate
        QROTATE #100, #$20000000  ' X=100, angle=45 degrees
        ' Wait 55 clocks...
        GETQX   new_x          ' Get rotated X
        GETQY   new_y          ' Get rotated Y
:::



## QSQRT {#qsqrt}

Queue square root
[CORDIC Solver](#cordic-solver) - Calculate square root of 64-bit unsigned number.

**QSQRT**  *{#}Dest, {#}Src*

---

**Result:** Calculates the square root of a 64-bit value, producing a 32-bit result via GETQX 55 clocks later.

- Dest is a register or literal containing the lower 32 bits of the 64-bit input value.
- Src is a register or literal containing the upper 32 bits of the 64-bit input value.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101001 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [QMUL](#qmul)

**Explanation:**

QSQRT performs square root calculation using the P2's 54-stage pipelined CORDIC solver. It calculates the square root of a 64-bit unsigned value and produces a 32-bit result.

The 64-bit input is formed by concatenating the Src operand as the upper 32 bits with the Dest operand as the lower 32 bits, creating the value {Src, Dest}. After 55 clocks, the 32-bit square root result can be retrieved using GETQX.

The result is the largest integer whose square does not exceed the input value.

::: pasm2
        QSQRT   #1000000, #0   ' sqrt(1000000) = 1000
        ' Wait 55 clocks...
        GETQX   sqrt_result    ' Get 1000
:::

For 32-bit square roots, use Src=0.



## QVECTOR {#qvector}

Queue vector
[CORDIC Solver](#cordic-solver) - Convert cartesian coordinates (X, Y) to polar coordinates (length, angle).

**QVECTOR**  *{#}Dest, {#}Src*

---

**Result:** Converts cartesian coordinates to polar form, producing length (GETQX) and angle (GETQY) 55 clocks later.

- Dest is a register or literal containing the X coordinate (32-bit signed).
- Src is a register or literal containing the Y coordinate (32-bit signed).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101010 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [QROTATE](#qrotate)

**Explanation:**

QVECTOR performs cartesian to polar coordinate conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 32-bit signed (X, Y) cartesian coordinate pair into a 32-bit (length, angle) polar coordinate pair.

The instruction takes the X coordinate in Dest and Y coordinate in Src, both as 32-bit signed values. After 55 clocks, the results can be retrieved using GETQX for the length and GETQY for the angle.

The angle result uses P2's standard angle units where $00000000 = 0°, $40000000 = 90°, $80000000 = 180°, and $C0000000 = 270°.

QVECTOR is the inverse operation of QROTATE.

::: pasm2
        QVECTOR #100, #200     ' Begin conversion
        ' Wait 55 clocks...
        GETQX   length         ' Get polar length
        GETQY   angle          ' Get polar angle
:::


# Instructions: R

This section contains all PASM2 instructions beginning with the letter R.



## RCL {#rcl}

Rotate carry left
[Math and Logic](#math-and-logic) - Rotate bits left, inserting carry flag as new LSBs.

**RCL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by Src bits, inserting C as new LSBs.

- Dest is a register containing the value to rotate carry left.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [RCR](#rcr), [ROL](#rol), [ROR](#ror)

**Explanation:**

RCL shifts Dest's binary value left by Src places (0-31 bits) and sets the new LSBs to C. The carry flag acts as an extension of the register, allowing 33-bit rotations.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit shifted out if Src is 1-31, or to Dest[31] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero.

This instruction is useful for multi-precision arithmetic operations where the carry from one word needs to be propagated into the next word.



## RCR {#rcr}

Rotate carry right
[Math and Logic](#math-and-logic) - Rotate bits right, inserting carry flag as new MSBs.

**RCR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by Src bits, inserting C as new MSBs.

- Dest is a register containing the value to rotate carry right.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000100 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [RCL](#rcl), [ROL](#rol), [ROR](#ror)

**Explanation:**

RCR shifts Dest's binary value right by Src places (0-31 bits) and sets the new MSBs to C. The carry flag acts as an extension of the register, allowing 33-bit rotations.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit shifted out if Src is 1-31, or to Dest[0] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero.

This instruction is useful for multi-precision arithmetic operations where the carry needs to be propagated through multiple words.



## RCZL {#rczl}

Rotate carry and zero left
[Math and Logic](#math-and-logic) - Rotate left by two bits, inserting C and Z flags as new LSBs.

**RCZL**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by two places and C and Z are inserted as new LSBs.

- Dest is a register containing the value to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001101011 | D | D[31] | D[30] | 2 |


**Related:** [RCZR](#rczr), [RCL](#rcl), [RCR](#rcr)

**Explanation:**

RCZL shifts Dest's binary value left by two places and sets Dest[1] to C and Dest[0] to Z.

If the WC or WCZ effect is specified, the C flag is updated to the original Dest[31] state.

If the WZ or WCZ effect is specified, the Z flag is updated to the original Dest[30] state.

This instruction provides a compact way to shift two flag states into a register while simultaneously extracting two bits from the register into the flags, enabling efficient state serialization and deserialization.



## RCZR {#rczr}

Rotate carry and zero right
[Math and Logic](#math-and-logic) - Rotate right by two bits, inserting C and Z flags as new MSBs.

**RCZR**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by two places and C and Z are inserted as new MSBs.

- Dest is a register containing the value to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001101010 | D | D[1] | D[0] | 2 |


**Related:** [RCZL](#rczl), [RCL](#rcl), [RCR](#rcr)

**Explanation:**

RCZR shifts Dest's binary value right by two places and sets Dest[31] to C and Dest[30] to Z.

If the WC or WCZ effect is specified, the C flag is updated to the original Dest[1] state.

If the WZ or WCZ effect is specified, the Z flag is updated to the original Dest[0] state.

This instruction provides a compact way to shift two flag states into a register while simultaneously extracting two bits from the register into the flags, enabling efficient state serialization and deserialization.



## RDBYTE {#rdbyte}

Read byte from Hub
[Hub RAM](#hub-ram) - Read a zero-extended byte from Hub memory into a register.

**RDBYTE**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended byte from Hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the byte value.
- Src/Ptr is a Hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010110 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of byte | Result = 0 | 9...16 |


**Related:** [RDWORD](#rdword), [RDLONG](#rdlong), [WRBYTE](#wrbyte)

**Explanation:**

RDBYTE reads a byte from Hub memory at the address specified by Src (or pointer register) and loads it into Dest with zero extension (bits 31:8 are cleared to 0). The operation takes 9-16 clock cycles depending on Hub timing, as the cog must wait for its Hub access window.

If preceded by a SETQ instruction, burst reads of multiple bytes can be performed.

If the WC or WCZ effect is specified, C is set to the MSB of the byte.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot. The actual latency depends on when the request arrives relative to the cog's assigned slot.



## RDFAST {#rdfast}

Read fast via FIFO
[Hub RAM](#hub-ram) - Begin fast sequential read from Hub memory into FIFO buffer.

**RDFAST**  *{#}Dest, {#}Src*

---

**Result:** A fast read operation begins, filling the FIFO with data from Hub memory starting at address Src.

- Dest is a configuration value: Dest[31] = no-wait mode, Dest[13:0] = block size in 64-byte units (0 = maximum).
- Src is the Hub memory start address (Src[19:0]) for the read operation.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 or WRFAST finish + 10...17 |


**Related:** [RFBYTE](#rfbyte), [RFWORD](#rfword), [RFLONG](#rflong), [WRFAST](#wrfast), [FBLOCK](#fblock)

**Explanation:**

RDFAST begins a new fast Hub read operation via the FIFO. The instruction configures automatic sequential reading from Hub memory with background FIFO refill, enabling high-throughput streaming data processing.

Dest[31] = 1 enables no-wait mode, which prevents stalls when the FIFO is being filled. Dest[13:0] specifies the block size in 64-byte units, with 0 indicating maximum size (16384 longs). Src[19:0] specifies the starting Hub address. The FIFO automatically wraps at the block boundary.

After RDFAST is executed, subsequent RFBYTE, RFWORD, or RFLONG instructions read data from the FIFO. The FIFO is automatically refilled in the background, making this ideal for checksums, CRC calculations, data processing, and block copy operations.



## RDLONG {#rdlong}

Read long from Hub
[Hub RAM](#hub-ram) - Read a long (32-bit value) from Hub memory into a register.

**RDLONG**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

---

**Result:** A long from Hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the long value.
- Src/Ptr is a Hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011000 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of long | --- | 9...16 |


**Related:** [RDBYTE](#rdbyte), [RDWORD](#rdword), [WRLONG](#wrlong)

**Explanation:**

RDLONG reads a long from Hub memory at the address specified by Src (or pointer register) and loads it into Dest. The operation takes 9-16 clock cycles depending on Hub timing, as the cog must wait for its Hub access window.

If preceded by a SETQ instruction, burst reads of multiple longs can be performed.

If the WC or WCZ effect is specified, C is set to the MSB of the long.

Hub memory operations follow a round-robin access pattern where each cog gets a regular time slot.



## RDLUT {#rdlut}

Read from LUT
[Lookup Table](#lookup-table) - Read a long from the Lookup Table into a register.

**RDLUT**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

---

**Result:** Data from LUT address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the data.
- Src/Ptr is a LUT address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010101 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of data | Result = 0 | 3 |


**Related:** [WRLUT](#wrlut), [RDLONG](#rdlong)

**Explanation:**

RDLUT reads data from the Lookup Table at the address specified by Src (or pointer register) and loads it into Dest. The LUT is a 512-long (2KB) memory area in each cog that can be used for lookup tables, buffers, or general-purpose memory. The operation takes 3 clock cycles.

If the WC or WCZ effect is specified, C is set to the MSB of the data.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The LUT provides fast local memory access for frequently accessed data structures, making it ideal for sin/cos tables, gamma correction tables, and small data buffers.



## RDPIN {#rdpin}

Read Smart Pin
[Smart Pin](#smart-pin) - Read a Smart Pin's result value and acknowledge the pin.

**RDPIN**  *Dest, {#}Src*  **{WC}**

---

**Result:** Smart Pin Src[5:0] result is loaded into Dest, and the pin is acknowledged.

- Dest is the register to receive the pin result.
- Src is a register or literal identifying the pin number (Src[5:0]) to read from.
- WC is an optional effect to write the modal result to C.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010100 | C1I | DDDDDDDDD | SSSSSSSSS | D | Modal result | --- | 2 |


**Related:** [RQPIN](#rqpin), [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin)

**Explanation:**

RDPIN reads the result value from the specified Smart Pin and acknowledges the pin, clearing its "ready" flag. The result value depends on the pin's configured mode and represents measurement data such as pulse width, period, edge count, ADC value, or serial data.

If the WC effect is specified, the C flag is set to the modal result, which provides mode-specific status information.

Smart Pins are powerful autonomous I/O processors that can measure timing, count edges, perform A/D conversion, generate PWM, and communicate serially without continuous CPU intervention. RDPIN retrieves the measured or received data after the pin signals completion.



## RDWORD {#rdword}

Read word from Hub
[Hub RAM](#hub-ram) - Read a zero-extended word (16-bit value) from Hub memory into a register.

**RDWORD**  *Dest, {#}Src/Ptr*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended word from Hub address Src or pointer (PTRA/PTRB) is loaded into Dest.

- Dest is the register to receive the word value.
- Src/Ptr is a Hub address from register, immediate value, or pointer register (PTRA/PTRB).
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010111 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of word | Result = 0 | 9...16 |


**Related:** [RDBYTE](#rdbyte), [RDLONG](#rdlong), [WRWORD](#wrword)

**Explanation:**

RDWORD reads a word from Hub memory at the address specified by Src (or pointer register) and loads it into Dest with zero extension (bits 31:16 are cleared to 0). The operation takes 9-16 clock cycles depending on Hub timing, as the cog must wait for its Hub access window.

If preceded by a SETQ instruction, burst reads of multiple words can be performed.

If the WC or WCZ effect is specified, C is set to the MSB of the word.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.



## REP {#rep}

Repeat block
[Branch](#branch) - Execute a block of instructions repeatedly with hardware loop.

**REP**  *{#}Dest, {#}Src*

---

**Result:** The next Dest[8:0] instructions are executed Src times.

- Dest is the number of instructions to repeat (Dest[8:0], 0-511). If Dest[8:0] = 0, nothing repeats.
- Src is the number of repetitions. If Src = 0, instructions repeat infinitely.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100110 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [DJNZ](#djnz), [JNCT1/2/3](#jnct1)

**Explanation:**

REP creates a hardware-implemented loop that executes the next Dest[8:0] instructions Src times. If Src = 0, the instructions repeat infinitely (useful for main loops). If Dest[8:0] = 0, nothing repeats.

The REP instruction itself takes 2 cycles, and the repeated instructions execute with zero overhead—no jump penalty, no counter decrement. This makes REP ideal for time-critical inner loops.

REP blocks can be nested up to 3 levels deep, allowing complex loop structures. Interrupts are blocked during REP execution to maintain timing precision. The zero-overhead nature of REP makes it essential for high-performance applications like DSP algorithms, graphics rendering, and precise timing operations.



## RESI0 / RESI1 / RESI2 / RESI3 {#resi0}

Resume from interrupt (0, 1, 2, or 3)
[Interrupt](#interrupt) - Resume execution after returning from interrupt.

**RESI0**
**RESI1**
**RESI2**
**RESI3**

---

**Result:** Execution resumes from the interrupted location for the specified interrupt level.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011001 | 110 | 111111110 | 111111111 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110100 | 111110101 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110010 | 111110011 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111110000 | 111110001 | --- | --- | --- | 4 (COG), 13...20 (Hub) |


**Related:** [RETI0/1/2/3](#reti0), [SETINT1/2/3](#setint1), [NIXINT1/2/3](#nixint1)

**Explanation:**

RESI0, RESI1, RESI2, and RESI3 resume execution from their respective interrupt levels. Each instruction is functionally equivalent to a CALLD instruction that restores the program counter, C flag, and Z flag from the corresponding interrupt return address registers.

Unlike RETIx instructions which return from the interrupt handler, RESIx instructions resume interrupted execution, used when an interrupt handler needs to yield to another interrupt priority level before completion.



## RET {#ret}

Return from subroutine
[Branch](#branch) - Return from subroutine by popping the hardware stack.

**RET**  **{WC|WZ|WCZ}**

---

**Result:** The program counter, C flag, and Z flag are restored from the top of the hardware stack.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101101 | --- | K[31] | K[30] | 4 |


**Related:** [CALL](#call), [CALLA](#calla), [CALLB](#callb), [RETA](#reta), [RETB](#retb)

**Explanation:**

RET returns from a subroutine by popping the hardware stack (K register). The program counter is restored from K[19:0].

If the WC or WCZ effect is specified, the C flag is restored from K[31].

If the WZ or WCZ effect is specified, the Z flag is restored from K[30].

The operation takes 4 cycles minimum, with variable timing depending on Hub access if the return location is in Hub memory (13-20 cycles).

The P2 provides an 8-level hardware stack for fast subroutine calls. RET is paired with CALL, CALLPA, CALLPB, CALLA, and CALLB instructions.



## RETA {#reta}

Return via PTRA stack
[Branch](#branch) - Return from subroutine by reading return address from Hub via PTRA.

**RETA**  **{WC|WZ|WCZ}**

---

**Result:** The program counter, C flag, and Z flag are restored from Hub memory at --PTRA.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101110 | --- | L[31] | L[30] | 11...18 |


**Related:** [CALLA](#calla), [RET](#ret), [RETB](#retb)

**Explanation:**

RETA returns from a subroutine by reading a Hub long from --PTRA. PTRA is pre-decremented by 4 bytes, then a long is read from that address. The program counter is restored from L[19:0].

If the WC or WCZ effect is specified, the C flag is restored from L[31].

If the WZ or WCZ effect is specified, the Z flag is restored from L[30].

RETA is paired with CALLA for implementing software stacks in Hub memory, enabling deep call nesting beyond the 8-level hardware stack limit.



## RETB {#retb}

Return via PTRB stack
[Branch](#branch) - Return from subroutine by reading return address from Hub via PTRB.

**RETB**  **{WC|WZ|WCZ}**

---

**Result:** The program counter, C flag, and Z flag are restored from Hub memory at --PTRB.

- WC, WZ, or WCZ are optional effects to restore flags from the stack.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ1 | 000000000 | 000101111 | --- | L[31] | L[30] | 11...18 |


**Related:** [CALLB](#callb), [RET](#ret), [RETA](#reta)

**Explanation:**

RETB returns from a subroutine by reading a Hub long from --PTRB. PTRB is pre-decremented by 4 bytes, then a long is read from that address. The program counter is restored from L[19:0].

If the WC or WCZ effect is specified, the C flag is restored from L[31].

If the WZ or WCZ effect is specified, the Z flag is restored from L[30].

RETB is paired with CALLB for implementing software stacks in Hub memory, enabling deep call nesting beyond the 8-level hardware stack limit.



## RETI0 / RETI1 / RETI2 / RETI3 {#reti0}

Return from interrupt (0, 1, 2, or 3)
[Interrupt](#interrupt) - Return from interrupt handler, restoring execution to interrupted code.

**RETI0**
**RETI1**
**RETI2**
**RETI3**

---

**Result:** Execution returns from the specified interrupt level to the interrupted location.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011001 | 110 | 111111111 | 111111111 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110101 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110011 | --- | --- | --- | 4 (COG), 13...20 (Hub) |
| EEEE | 1011001 | 110 | 111111111 | 111110001 | --- | --- | --- | 4 (COG), 13...20 (Hub) |


**Related:** [RESI0/1/2/3](#resi0), [SETINT1/2/3](#setint1), [NIXINT1/2/3](#nixint1)

**Explanation:**

RETI0, RETI1, RETI2, and RETI3 return from their respective interrupt handlers. Each instruction is functionally equivalent to a CALLD instruction that restores the program counter, C flag, and Z flag from the corresponding interrupt return address registers.

The P2 provides four interrupt levels (INT0-INT3), with INT0 being the lowest priority and INT3 being the highest. Each RETI instruction completes its interrupt handler and resumes normal execution at the point where the interrupt occurred.



## REV {#rev}

Reverse bits
[Math and Logic](#math-and-logic) - Reverse the bit pattern in a register.

**REV**  *Dest*

---

**Result:** The 32-bit pattern in Dest is reversed (bits 31:0 become bits 0:31).

- Dest is the register containing the bit pattern to reverse.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101001 | D | --- | --- | 2 |


**Related:** [ROL](#rol), [ROR](#ror), [ZEROX](#zerox)

**Explanation:**

REV performs a complete bitwise reverse of the value in Dest, storing the result back into Dest. Bit 31 becomes bit 0, bit 30 becomes bit 1, and so on through bit 0 becoming bit 31. The operation takes 2 cycles and does not affect any flags.

This instruction is useful for processing binary data in different MSB/LSB order than it is transmitted with, such as serial protocols that send least-significant bit first but need processing in most-significant bit first order. It is also used in bit-reversal algorithms for FFT operations.



## RFBYTE {#rfbyte}

Read byte via FIFO
[Hub RAM](#hub-ram) - Read a zero-extended byte from the FIFO after RDFAST.

**RFBYTE**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended byte from the FIFO is loaded into Dest.

- Dest is the register to receive the byte value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010000 | D | MSB of byte | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFWORD](#rfword), [RFLONG](#rflong), [RFVAR](#rfvar)

**Explanation:**

RFBYTE is used after RDFAST to read zero-extended bytes from the FIFO. The byte is loaded into Dest with bits 31:8 cleared to 0.

If the WC or WCZ effect is specified, C is set to the MSB of the byte.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available. The FIFO is automatically refilled in the background by the RDFAST operation.



## RFLONG {#rflong}

Read long via FIFO
[Hub RAM](#hub-ram) - Read a long (32-bit value) from the FIFO after RDFAST.

**RFLONG**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A long from the FIFO is loaded into Dest.

- Dest is the register to receive the long value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010010 | D | MSB of long | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFWORD](#rfword), [RFVAR](#rfvar)

**Explanation:**

RFLONG is used after RDFAST to read longs from the FIFO.

If the WC or WCZ effect is specified, C is set to the MSB of the long.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available. The FIFO is automatically refilled in the background by the RDFAST operation.



## RFVAR {#rfvar}

Read variable via FIFO
[Hub RAM](#hub-ram) - Read a zero-extended 1-4 byte variable-length value from the FIFO.

**RFVAR**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended 1-4 byte value from the FIFO is loaded into Dest.

- Dest is the register to receive the variable-length value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010011 | D | 0 | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFVARS](#rfvars)

**Explanation:**

RFVAR is used after RDFAST to read variable-length values (1-4 bytes) from the FIFO with zero extension. The value is loaded into Dest with upper bits cleared to 0.

If the WC or WCZ effect is specified, C is always cleared to 0.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The length of each value read is determined by the streamer configuration set up before the RDFAST operation.



## RFVARS {#rfvars}

Read signed variable via FIFO
[Hub RAM](#hub-ram) - Read a sign-extended 1-4 byte variable-length value from the FIFO.

**RFVARS**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A sign-extended 1-4 byte value from the FIFO is loaded into Dest.

- Dest is the register to receive the sign-extended value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010100 | D | MSB of value | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFVAR](#rfvar), [RFBYTE](#rfbyte)

**Explanation:**

RFVARS is used after RDFAST to read variable-length values (1-4 bytes) from the FIFO with sign extension. The value is loaded into Dest with upper bits set according to the MSB of the value (sign extension).

If the WC or WCZ effect is specified, C is set to the MSB of the value.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.



## RFWORD {#rfword}

Read word via FIFO
[Hub RAM](#hub-ram) - Read a zero-extended word (16-bit value) from the FIFO after RDFAST.

**RFWORD**  *Dest*  **{WC|WZ|WCZ}**

---

**Result:** A zero-extended word from the FIFO is loaded into Dest.

- Dest is the register to receive the word value.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 000010001 | D | MSB of word | Result = 0 | 2 |


**Related:** [RDFAST](#rdfast), [RFBYTE](#rfbyte), [RFLONG](#rflong), [RFVAR](#rfvar)

**Explanation:**

RFWORD is used after RDFAST to read zero-extended words from the FIFO. The word is loaded into Dest with bits 31:16 cleared to 0.

If the WC or WCZ effect is specified, C is set to the MSB of the word.

If the WZ or WCZ effect is specified, Z is set (1) if the result equals zero, or is cleared (0) if non-zero.

The operation takes 2 cycles when the FIFO has data available.



## RGBEXP {#rgbexp}

Expand RGB color
[Pixel Mixer](#pixel-mixer) - Expand a 5:6:5 RGB color value into 8:8:8 format.

**RGBEXP**  *Dest*

---

**Result:** The 5:6:5 RGB value in Dest[15:0] is expanded into 8:8:8 format in Dest[31:8].

- Dest contains 5:6:5 RGB in Dest[15:0], receives 8:8:8 RGB in Dest[31:8].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100111 | D | --- | --- | 2 |


**Related:** [RGBSQZ](#rgbsqz)

**Explanation:**

RGBEXP expands a compact 5:6:5 RGB color value (commonly used in 16-bit color displays) into full 8:8:8 RGB format (24-bit true color). The input 5:6:5 value is in Dest[15:0] with 5 bits red, 6 bits green, and 5 bits blue. The output 8:8:8 value is placed in Dest[31:8] with 8 bits each for red, green, and blue. The expansion replicates the most significant bits into the lower bits to maintain color accuracy.

This instruction is useful when converting between 16-bit and 24-bit color formats for graphics processing.



## RGBSQZ {#rgbsqz}

Squeeze RGB color
[Pixel Mixer](#pixel-mixer) - Compress an 8:8:8 RGB color value into 5:6:5 format.

**RGBSQZ**  *Dest*

---

**Result:** The 8:8:8 RGB value in Dest[31:8] is compressed into 5:6:5 format in Dest[15:0].

- Dest contains 8:8:8 RGB in Dest[31:8], receives 5:6:5 RGB in Dest[15:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100110 | D | --- | --- | 2 |


**Related:** [RGBEXP](#rgbexp)

**Explanation:**

RGBSQZ compresses a full 8:8:8 RGB color value (24-bit true color) into compact 5:6:5 format (16-bit color). The input 8:8:8 value is in Dest[31:8] with 8 bits each for red, green, and blue. The output 5:6:5 value is placed in Dest[15:0] with 5 bits red, 6 bits green, and 5 bits blue. The compression keeps the most significant bits of each color channel.

This instruction is useful when converting from 24-bit to 16-bit color formats for display output.



## ROL {#rol}

Rotate left
[Math and Logic](#math-and-logic) - Rotate the bits of a register left.

**ROL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are rotated left by Src positions; departing MSBs are moved into LSBs.

- Dest is the register containing the value to rotate left.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000001 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [ROR](#ror), [RCL](#rcl), [RCR](#rcr), [SHL](#shl)

**Explanation:**

ROL rotates Dest's binary value left by Src places (0-31 bits). All MSBs rotated out are moved into the new LSBs.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit rotated out if Src is 1-31, or to Dest[31] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero. Since no bits are lost by this operation, the result will only be zero if Dest started at zero.

Rotation is useful for bit manipulation, circular buffers, hash functions, and cryptographic operations.



## ROLBYTE {#rolbyte}

Rotate byte left into register
[Math and Logic](#math-and-logic) - Read a byte from source and rotate it left into destination.

**ROLBYTE**  *Dest, {#}Src, #N*
**ROLBYTE**  *Dest*

---

**Result:** Byte N (0-3) of Src, or a byte from a source described by prior ALTGB instruction, is rotated left into Dest.

- Dest is the register into which the byte is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target byte.
- N is a 2-bit literal (0-3) identifying the byte position in Src.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001000 | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001000 | 000 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ROLNIB](#rolnib), [ROLWORD](#rolword), [GETBYTE](#getbyte), [SETBYTE](#setbyte), [ALTGB](#altgb)

**Explanation:**

ROLBYTE reads the byte identified by N (0-3) from Src, or a byte from the source described by a prior ALTGB instruction, and rotates it left into Dest. ROLBYTE achieves the same effect as two instructions: an 8-bit SHL followed by SETBYTE into byte 0.

The second syntax form is intended for use after an ALTGB instruction in a loop to iteratively read a series of byte values within contiguous long registers.



## ROLNIB {#rolnib}

Rotate nibble left into register
[Math and Logic](#math-and-logic) - Read a nibble from source and rotate it left into destination.

**ROLNIB**  *Dest, {#}Src, #N*
**ROLNIB**  *Dest*

---

**Result:** Nibble N (0-7) of Src, or a nibble from a source described by prior ALTGN instruction, is rotated left into Dest.

- Dest is the register into which the nibble is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target nibble.
- N is a 3-bit literal (0-7) identifying the nibble position in Src.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 100010N | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1000100 | 000 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ROLBYTE](#rolbyte), [ROLWORD](#rolword), [GETNIB](#getnib), [SETNIB](#setnib), [ALTGN](#altgn)

**Explanation:**

ROLNIB reads the nibble identified by N (0-7) from Src, or a nibble from the source described by a prior ALTGN instruction, and rotates it left into Dest. ROLNIB achieves the same effect as two instructions: a 4-bit SHL followed by SETNIB into nibble 0.

The second syntax form is intended for use after an ALTGN instruction in a loop to iteratively read a series of nibble values within contiguous long registers.



## ROLWORD {#rolword}

Rotate word left into register
[Math and Logic](#math-and-logic) - Read a word from source and rotate it left into destination.

**ROLWORD**  *Dest, {#}Src, #N*
**ROLWORD**  *Dest*

---

**Result:** Word N (0-1) of Src, or a word from a source described by prior ALTGW instruction, is rotated left into Dest.

- Dest is the register into which the word is rotated.
- Src is a register, 9-bit literal, or 32-bit augmented literal containing the target word.
- N is a 1-bit literal (0-1) identifying the word position in Src.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001010 | 0NI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001010 | 000 | DDDDDDDDD | 000000000 | D | --- | --- | 2 |


**Related:** [ROLBYTE](#rolbyte), [ROLNIB](#rolnib), [GETWORD](#getword), [SETWORD](#setword), [ALTGW](#altgw)

**Explanation:**

ROLWORD reads the word identified by N (0-1) from Src, or a word from the source described by a prior ALTGW instruction, and rotates it left into Dest. ROLWORD achieves the same effect as two instructions: a 16-bit SHL followed by SETWORD into word 0.

The second syntax form is intended for use after an ALTGW instruction in a loop to iteratively read a series of word values within contiguous long registers.



## ROR {#ror}

Rotate right
[Math and Logic](#math-and-logic) - Rotate the bits of a register right.

**ROR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are rotated right by Src positions; departing LSBs are moved into MSBs.

- Dest is the register containing the value to rotate right.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to rotate.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000000 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [ROL](#rol), [RCL](#rcl), [RCR](#rcr), [SHR](#shr)

**Explanation:**

ROR rotates Dest's binary value right by Src places (0-31 bits). All LSBs rotated out are moved into the new MSBs.

If the WC or WCZ effect is specified, the C flag is updated to the value of the last bit rotated out if Src is 1-31, or to Dest[0] if Src is 0.

If the WZ or WCZ effect is specified, the Z flag is set (1) if the result equals zero, or is cleared (0) if non-zero. Since no bits are lost by this operation, the result will only be zero if Dest started at zero.

Rotation is useful for bit manipulation, circular buffers, hash functions, and cryptographic operations.



## RQPIN {#rqpin}

Read Smart Pin without acknowledge
[Smart Pin](#smart-pin) - Read a Smart Pin's result value without clearing its ready flag.

**RQPIN**  *Dest, {#}Src*  **{WC}**

---

**Result:** Smart Pin Src[5:0] result is loaded into Dest without clearing the pin's ready flag.

- Dest is the register to receive the pin result.
- Src is a register or literal identifying the pin number (Src[5:0]) to read from.
- WC is an optional effect to write the modal result to C.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010100 | C0I | DDDDDDDDD | SSSSSSSSS | D | Modal result | --- | 2 |


**Related:** [RDPIN](#rdpin), [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin)

**Explanation:**

RQPIN reads the result value from the specified Smart Pin without acknowledging the pin. Unlike RDPIN, this instruction does not clear the pin's "ready" flag, allowing the same result to be read multiple times or checked before being consumed.

If the WC effect is specified, the C flag is set to the modal result, which provides mode-specific status information.

This instruction is useful when you need to check a pin's result value without consuming it, such as polling for completion before actually processing the result.


# Instructions: S

This section contains all PASM2 instructions beginning with the letter S.



## SAL {#sal}

Shift arithmetic left
[Math and Logic](#math-and-logic) - Shift bits left, extending original LSB into new rightmost positions.

**SAL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by Src bits, extending Dest[0] into new rightmost bits.

- Dest is a register containing the value to arithmetically left shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000111 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [SAR](#sar), [SHL](#shl), [SHR](#shr)

**Explanation:**

SAL shifts the destination's binary value left by the source number of places (0-31 bits) and sets the new LSBs to that of the original Dest[0]. SAL is the complement of SAR for bit streams but not for math operations. For swift 32-bit integer multiplication by a power-of-two, use SHL instead.

::: pasm2
        SAL     data, #4       ' Shift left 4 bits, extending LSB
:::



## SAR {#sar}

Shift arithmetic right
[Math and Logic](#math-and-logic) - Shift bits right, extending sign bit into new leftmost positions.

**SAR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by Src bits, extending Dest[31] (the sign bit) into new leftmost bits.

- Dest is a register containing the value to arithmetically right shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [SAL](#sal), [SHL](#shl), [SHR](#shr)

**Explanation:**

SAR shifts the destination's binary value right by the source number of places (0-31 bits) and sets the new MSBs to that of the original Dest[31], preserving the sign of a signed integer. This is useful for bit stream manipulation and for swift division. It is similar to SHR for swift division by a power-of-two, but is safe for both signed and unsigned integers.

::: pasm2
        SAR     value, #3      ' Divide signed value by 8
:::



## SCA {#sca}

Scale
[Math and Logic](#math-and-logic) - Multiply 16-bit values and scale result for next instruction.

**SCA**  *Dest, {#}Src*  **{WZ}**

---

**Result:** The upper 16 bits of the unsigned product from the 16-bit Dest and Src multiplication is substituted as the next instruction's S value.

- Dest is a register containing the 16-bit value to multiply with Src.
- Src is a register, 9-bit literal, or 16-bit augmented literal to multiply with Dest.
- WZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010001 | 0ZI | DDDDDDDDD | SSSSSSSSS | --- | --- | Product = 0 | 2 |


**Related:** [SCAS](#scas)

**Explanation:**

SCA multiplies the lower 16 bits of each of Dest and Src together, right shifts the 32-bit product by 16 (to scale down the result), and substitutes this value as the next instruction's S value. This is useful for creating scaled unsigned 16-bit values for subsequent operations.

::: pasm2
        SCA     factor, #$8000  ' Scale by 0.5 (32768/65536)
        ADD     result, #0      ' Add scaled value
:::



## SCAS {#scas}

Scale signed
[Math and Logic](#math-and-logic) - Multiply signed 16-bit values and scale result for next instruction.

**SCAS**  *Dest, {#}Src*  **{WZ}**

---

**Result:** The upper 18 bits of the signed product from the 16-bit Dest and Src multiplication is substituted as the next instruction's S value.

- Dest is a register containing the signed 16-bit value to multiply with Src.
- Src is a register, 9-bit literal, or signed 16-bit augmented literal to multiply with Dest.
- WZ is an optional effect to update the Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010001 | 1ZI | DDDDDDDDD | SSSSSSSSS | --- | --- | Result = 0 | 2 |


**Related:** [SCA](#sca)

**Explanation:**

SCAS multiplies the lower signed 16 bits of each of Dest and Src together, right shifts the 32-bit product by 14 (to scale down the result), and substitutes this value as the next instruction's S value. This is useful for creating scaled signed values for subsequent operations.



## SETBYTE {#setbyte}

Set byte
[Math and Logic](#math-and-logic) - Store an 8-bit value into a specified byte position within a register.

**SETBYTE**  *Dest, {#}Src, #N*
**SETBYTE**  *{#}Src*

---

**Result:** Src[7:0] is written to byte N (0-3) of Dest, or to another register byte described by prior ALTSB instruction.

- Dest is a register in which to modify a byte.
- Src is a register or 8-bit literal whose bits [7:0] will be stored in the designated location.
- N is a 2-bit literal (0-3) identifying the byte of Dest to modify.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1000110 | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1000110 | 00I | 000000000 | SSSSSSSSS | D* | --- | --- | 2 |


*Dest and byte ID specified by prior ALTSB instruction.

**Related:** [ALTSB](#altsb), [SETNIB](#setnib), [SETWORD](#setword), [GETBYTE](#getbyte)

**Explanation:**

SETBYTE stores Src[7:0] into the byte identified by N within Dest, or the byte and register described by a prior ALTSB instruction. No other bits are modified. N (0-3) identifies a value's individual bytes by position in least-significant byte order. The second syntax is intended for use after an ALTSB instruction in a loop to iteratively affect a series of byte values within contiguous long registers.

::: pasm2
        SETBYTE data, #$FF, #2  ' Set byte 2 of data to $FF
:::



## SETCFRQ {#setcfrq}

Set colorspace converter frequency
[Color Space Converter](#color-space-converter) - Configure the colorspace converter CFRQ parameter.

**SETCFRQ**  *{#}Dest*

---

**Result:** The colorspace converter CFRQ parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CFRQ parameter.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111011 | --- | --- | --- | 2 |


**Related:** [SETCI](#setci), [SETCMOD](#setcmod), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CFRQ parameter to the value in Dest. This instruction configures the frequency parameter for the colorspace conversion hardware.



## SETCI {#setci}

Set colorspace converter CI
[Color Space Converter](#color-space-converter) - Configure the colorspace converter CI parameter.

**SETCI**  *{#}Dest*

---

**Result:** The colorspace converter CI parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CI parameter.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111001 | --- | --- | --- | 2 |


**Related:** [SETCFRQ](#setcfrq), [SETCMOD](#setcmod), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CI parameter to the value in Dest. This instruction configures the CI parameter for the colorspace conversion hardware.



## SETCMOD {#setcmod}

Set colorspace converter mode
[Color Space Converter](#color-space-converter) - Configure the colorspace converter mode parameter.

**SETCMOD**  *{#}Dest*

---

**Result:** The colorspace converter CMOD parameter is set to Dest[8:0].

- Dest is a register or literal value (0-511) to set as CMOD parameter.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111100 | --- | --- | --- | 2 |


**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCQ](#setcq), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CMOD parameter to Dest[8:0]. This instruction configures the mode parameter for the colorspace conversion hardware.



## SETCQ {#setcq}

Set colorspace converter CQ
[Color Space Converter](#color-space-converter) - Configure the colorspace converter CQ parameter.

**SETCQ**  *{#}Dest*

---

**Result:** The colorspace converter CQ parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CQ parameter.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111010 | --- | --- | --- | 2 |


**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCMOD](#setcmod), [SETCY](#setcy)

**Explanation:**

Sets the colorspace converter CQ parameter to the value in Dest. This instruction configures the CQ parameter for the colorspace conversion hardware.



## SETCY {#setcy}

Set colorspace converter CY
[Color Space Converter](#color-space-converter) - Configure the colorspace converter CY parameter.

**SETCY**  *{#}Dest*

---

**Result:** The colorspace converter CY parameter is set to Dest[31:0].

- Dest is a register or literal value (0-511) to set as CY parameter.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111000 | --- | --- | --- | 2 |


**Related:** [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCMOD](#setcmod), [SETCQ](#setcq)

**Explanation:**

Sets the colorspace converter CY parameter to the value in Dest. This instruction configures the CY parameter for the colorspace conversion hardware.



## SETD {#setd}

Set destination field
[Register Indirection](#register-indirection) - Modify the D field of an instruction template for use with ALTI.

**SETD**  *Dest, {#}Src*

---

**Result:** The D field [17:9] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the D field of Dest.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001101 | 10I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [SETS](#sets), [SETR](#setr), [ALTI](#alti)

**Explanation:**

SETD copies Src[8:0] to the D field of the template Dest to be used with an ALTI instruction. Bits outside the D field remain unaffected. The D field holds the address of a register (or sometimes a literal value) for the instruction to use as its destination value, and usually as its result destination, during its execution.

SETD can also be used in self-modifying register RAM code. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



## SETDACS {#setdacs}

Set DACs
[Smart Pin](#smart-pin) - Simultaneously set all four DAC channels.

**SETDACS**  *{#}Dest*

---

**Result:** DAC3 = Dest[31:24], DAC2 = Dest[23:16], DAC1 = Dest[15:8], DAC0 = Dest[7:0].

- Dest is a register or literal value (0-511) containing four 8-bit DAC values.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000011100 | --- | --- | --- | 2 |


**Explanation:**

Sets all four DAC channels simultaneously from the four bytes in Dest. DAC3 receives bits [31:24], DAC2 receives bits [23:16], DAC1 receives bits [15:8], and DAC0 receives bits [7:0].



## SETINT1 {#setint1}

Set interrupt 1 source
[Interrupt](#interrupt) - Configure the interrupt 1 source.

**SETINT1**  *{#}Dest*

---

**Result:** The INT1 interrupt source is set to Dest[3:0].

- Dest is a register or literal value (0-511) containing interrupt source in bits [3:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100101 | --- | --- | --- | 2 |


**Related:** [SETINT2](#setint2), [SETINT3](#setint3), [NIXINT1](#nixint1), [TRGINT1](#trgint1), [RETI0](#reti0)

**Explanation:**

SETINT1 configures which event will trigger interrupt 1. The interrupt source is specified in Dest[3:0]. The P2 provides three configurable interrupt levels (INT1-INT3), each of which can be independently configured to respond to different event sources.



## SETINT2 {#setint2}

Set interrupt 2 source
[Interrupt](#interrupt) - Configure the interrupt 2 source.

**SETINT2**  *{#}Dest*

---

**Result:** The INT2 interrupt source is set to Dest[3:0].

- Dest is a register or literal value (0-511) containing interrupt source in bits [3:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100110 | --- | --- | --- | 2 |


**Related:** [SETINT1](#setint1), [SETINT3](#setint3), [NIXINT2](#nixint2), [TRGINT2](#trgint2), [RETI0](#reti0)

**Explanation:**

SETINT2 configures which event will trigger interrupt 2. The interrupt source is specified in Dest[3:0].



## SETINT3 {#setint3}

Set interrupt 3 source
[Interrupt](#interrupt) - Configure the interrupt 3 source.

**SETINT3**  *{#}Dest*

---

**Result:** The INT3 interrupt source is set to Dest[3:0].

- Dest is a register or literal value (0-511) containing interrupt source in bits [3:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100111 | --- | --- | --- | 2 |


**Related:** [SETINT1](#setint1), [SETINT2](#setint2), [NIXINT3](#nixint3), [TRGINT3](#trgint3), [RETI0](#reti0)

**Explanation:**

SETINT3 configures which event will trigger interrupt 3. The interrupt source is specified in Dest[3:0].



## SETLUTS {#setluts}

Set LUT sharing
[Lookup Table](#lookup-table) - Enable or disable LUT sharing between adjacent cogs.

**SETLUTS**  *{#}Dest*

---

**Result:** If Dest[0] = 1, LUT sharing is enabled where LUT writes within the adjacent odd/even companion cog are copied to this cog's LUT.

- Dest is a register or literal value (0-511) with enable bit in Dest[0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110111 | --- | --- | --- | 2 |


**Related:** [RDLUT](#rdlut), [WRLUT](#wrlut)

**Explanation:**

Enables or disables LUT sharing based on Dest[0]. When enabled (Dest[0] = 1), LUT writes within the adjacent odd/even companion cog are automatically copied to this cog's LUT, allowing cogs to share lookup table data.



## SETNIB {#setnib}

Set nibble
[Math and Logic](#math-and-logic) - Store a 4-bit value into a specified nibble position within a register.

**SETNIB**  *Dest, {#}Src, #N*
**SETNIB**  *{#}Src*

---

**Result:** Src[3:0] is written to nibble N (0-7) of Dest, or to another register nibble described by prior ALTSN instruction.

- Dest is a register in which to modify a nibble.
- Src is a register or 4-bit literal whose bits [3:0] will be stored in the designated location.
- N is a 3-bit literal (0-7) identifying the nibble of Dest to modify.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 100000N | NNI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1000000 | 00I | 000000000 | SSSSSSSSS | D* | --- | --- | 2 |


*Dest and nibble ID specified by prior ALTSN instruction.

**Related:** [ALTSN](#altsn), [SETBYTE](#setbyte), [SETWORD](#setword), [GETNIB](#getnib)

**Explanation:**

SETNIB stores Src[3:0] into the nibble identified by N within Dest, or the nibble and register described by a prior ALTSN instruction. No other bits are modified. N (0-7) identifies a value's individual nibbles by position in least-significant nibble order. The second syntax is intended for use after an ALTSN instruction in a loop to iteratively affect a series of nibble values within contiguous long registers.

::: pasm2
        SETNIB  data, #$A, #5   ' Set nibble 5 of data to $A
:::



## SETPAT {#setpat}

Set pin pattern
[Pin](#pin) - Configure pin pattern matching for PAT event detection.

**SETPAT**  *{#}Dest, {#}Src*

---

**Result:** Pin pattern for PAT event is configured. C selects INA/INB, Z selects =/!=, Dest provides mask value, Src provides match value.

- Dest is a register or immediate containing mask value.
- Src is a register or immediate containing match value.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011111 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [POLLPAT](#pollpat), [WAITPAT](#waitpat)

**Explanation:**

Sets pin pattern for PAT event detection. The C flag selects INA or INB for monitoring, the Z flag selects equality (=) or inequality (!=) matching, Dest provides the mask value to select which pins to monitor, and Src provides the match value to compare against.



## SETPIV {#setpiv}

Set pixel blend factor
[Pixel Mixer](#pixel-mixer) - Set the blend factor for pixel mixing operations.

**SETPIV**  *{#}Dest*

---

**Result:** BLNPIX/MIXPIX blend factor is set to Dest[7:0].

- Dest is a register or literal value (0-511) containing 8-bit blend factor in bits [7:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111101 | --- | --- | --- | 2 |


**Related:** [SETPIX](#setpix), [BLNPIX](#blnpix), [MIXPIX](#mixpix)

**Explanation:**

Sets the blend factor for BLNPIX and MIXPIX operations to Dest[7:0]. This controls the blending ratio for pixel mixing operations.



## SETPIX {#setpix}

Set pixel mixer mode
[Pixel Mixer](#pixel-mixer) - Configure the pixel mixer operating mode.

**SETPIX**  *{#}Dest*

---

**Result:** MIXPIX mode is set to Dest[5:0].

- Dest is a register or literal value (0-511) containing 6-bit mode in bits [5:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000111110 | --- | --- | --- | 2 |


**Related:** [SETPIV](#setpiv), [MIXPIX](#mixpix)

**Explanation:**

Sets the MIXPIX operating mode to Dest[5:0]. This configures how the pixel mixer combines pixel values.



## SETQ {#setq}

Set Q register
[Hub RAM](#hub-ram) - Set the Q register for use by subsequent instructions.

**SETQ**  *{#}Dest*

---

**Result:** Q register is set to Dest.

- Dest is a register or literal value (0-511) to load into Q.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000101000 | --- | --- | --- | 2 |


**Related:** [SETQ2](#setq2), [RDLONG](#rdlong), [WRLONG](#wrlong)

**Explanation:**

Sets Q register to Dest. Use before RDLONG/WRLONG/WMLONG to set block transfer count. Also used before MUXQ/COGINIT/QDIV/QFRAC/QROTATE/WAITxxx instructions to provide additional parameters.

::: pasm2
        SETQ    #16-1          ' Set up for 16-long block transfer
        RDLONG  buffer, ptra   ' Read 16 longs from hub
:::



## SETQ2 {#setq2}

Set Q for LUT transfers
[Hub RAM](#hub-ram) - Set the Q register for LUT block transfers.

**SETQ2**  *{#}Dest*

---

**Result:** Q register is set to Dest for LUT block transfers.

- Dest is a register or literal value (0-511) to load into Q.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000101001 | --- | --- | --- | 2 |


**Related:** [SETQ](#setq), [RDLONG](#rdlong), [WRLONG](#wrlong), [RDLUT](#rdlut), [WRLUT](#wrlut)

**Explanation:**

Sets Q register to Dest. Use before RDLONG/WRLONG/WMLONG to set LUT block transfer. SETQ2 enables block transfers to/from LUT RAM instead of COG RAM: SETQ2 + RDLONG performs block read from HUB to LUT, while SETQ2 + WRLONG performs block write from LUT to HUB. This is essential for fast bulk data movement for lookup tables, waveform tables, and large datasets.

::: pasm2
        SETQ2   #256-1         ' Set up for 256-long LUT transfer
        RDLONG  0, ptra        ' Read 256 longs from hub into LUT
:::



## SETR {#setr}

Set result field
[Register Indirection](#register-indirection) - Modify the Result field of an instruction template for use with ALTI.

**SETR**  *Dest, {#}Src*

---

**Result:** The Result field [27:19] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the Result field of Dest.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001101 | 01I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [SETD](#setd), [SETS](#sets), [ALTI](#alti)

**Explanation:**

SETR copies Src[8:0] to the Result field of the template Dest to be used with an ALTI instruction. Bits outside the Result field remain unaffected. The Result field does not exist in instruction opcodes, but takes its value from the D field, holding the address of a register for the instruction to use as its result destination upon execution.

SETR can also be used in self-modifying register RAM code, though it affects the Instr field and upper two bits of the FX field rather than a non-existent Register field. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



## SETS {#sets}

Set source field
[Register Indirection](#register-indirection) - Modify the S field of an instruction template for use with ALTI.

**SETS**  *Dest, {#}Src*

---

**Result:** The S field [8:0] of template Dest is set to Src[8:0].

- Dest is a register whose 32-bit value is a template for use with an ALTI instruction.
- Src is a register or 9-bit literal whose value (Src[8:0]) is copied to the S field of Dest.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001101 | 11I | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |


**Related:** [SETD](#setd), [SETR](#setr), [ALTI](#alti)

**Explanation:**

SETS copies Src[8:0] to the S field of the template Dest to be used with an ALTI instruction. Bits outside the S field remain unaffected. The S field holds the address of a register or literal value for an instruction to use as its source value during its execution.

SETS can also be used in self-modifying register RAM code. Unlike with ALTx instructions, when used this way, field value modification occurs in the program code itself (not the instruction pipeline); code is altered, values persist. Due to the instruction pipeline nature, after modifying a code register, it is necessary to elapse at least two instructions before executing the modified register.



## SETSCP {#setscp}

Set oscilloscope
[Miscellaneous](#miscellaneous) - Configure the four-channel oscilloscope.

**SETSCP**  *{#}Dest*

---

**Result:** Four-channel oscilloscope enable is set to Dest[6] and input pin base is set to Dest[5:2].

- Dest is a register or literal value (0-511) containing enable bit [6] and pin base [5:2].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 001110000 | --- | --- | --- | 2 |


**Explanation:**

Sets the four-channel oscilloscope enable to Dest[6] and sets the input pin base to Dest[5:2]. This configures the hardware oscilloscope feature for debugging and signal monitoring.



## SETSE1 {#setse1}

Set selectable event 1
[Event](#event) - Configure selectable event 1 detection.

**SETSE1**  *{#}Dest*

---

**Result:** The SE1 selectable event configuration is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100000 | --- | --- | --- | 2 |


**Related:** [SETSE2](#setse2), [SETSE3](#setse3), [SETSE4](#setse4), [POLLSE1](#pollse1), [WAITSE1](#waitse1)

**Explanation:**

SETSE1 configures selectable event 1's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.

The P2 provides four independent selectable events, each of which can be configured to detect various conditions including pin states, hub operations, CORDIC completion, and other system events. Once configured, these events can be polled with POLLSE1, waited upon with WAITSE1, or used for conditional jumps with JSE1 and JNSE1.



## SETSE2 {#setse2}

Set selectable event 2
[Event](#event) - Configure selectable event 2 detection.

**SETSE2**  *{#}Dest*

---

**Result:** The SE2 selectable event configuration is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100001 | --- | --- | --- | 2 |


**Related:** [SETSE1](#setse1), [SETSE3](#setse3), [SETSE4](#setse4), [POLLSE2](#pollse2), [WAITSE2](#waitse2)

**Explanation:**

SETSE2 configures selectable event 2's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.



## SETSE3 {#setse3}

Set selectable event 3
[Event](#event) - Configure selectable event 3 detection.

**SETSE3**  *{#}Dest*

---

**Result:** The SE3 selectable event configuration is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100010 | --- | --- | --- | 2 |


**Related:** [SETSE1](#setse1), [SETSE2](#setse2), [SETSE4](#setse4), [POLLSE3](#pollse3), [WAITSE3](#waitse3)

**Explanation:**

SETSE3 configures selectable event 3's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.



## SETSE4 {#setse4}

Set selectable event 4
[Event](#event) - Configure selectable event 4 detection.

**SETSE4**  *{#}Dest*

---

**Result:** The SE4 selectable event configuration is set to Dest[8:0].

- Dest is a register or literal value (0-511) containing event configuration in bits [8:0].


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000100011 | --- | --- | --- | 2 |


**Related:** [SETSE1](#setse1), [SETSE2](#setse2), [SETSE3](#setse3), [POLLSE4](#pollse4), [WAITSE4](#waitse4)

**Explanation:**

SETSE4 configures selectable event 4's detection criteria. The Dest[8:0] operand specifies which condition will trigger the event.



## SETWORD {#setword}

Set word
[Math and Logic](#math-and-logic) - Store a 16-bit value into a specified word position within a register.

**SETWORD**  *Dest, {#}Src, #N*
**SETWORD**  *{#}Src*

---

**Result:** Src[15:0] is written to word N (0-1) of Dest, or to another register word described by prior ALTSW instruction.

- Dest is a register in which to modify a word.
- Src is a register, 9-bit literal, or 16-bit augmented literal whose bits [15:0] will be stored in the designated location.
- N is a 1-bit literal (0-1) identifying the word of Dest to modify.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1001001 | 0NI | DDDDDDDDD | SSSSSSSSS | D | --- | --- | 2 |
| EEEE | 1001001 | 00I | 000000000 | SSSSSSSSS | D* | --- | --- | 2 |


*Dest and word ID specified by prior ALTSW instruction.

**Related:** [ALTSW](#altsw), [SETNIB](#setnib), [SETBYTE](#setbyte), [GETWORD](#getword)

**Explanation:**

SETWORD stores Src[15:0] into the word identified by N within Dest, or the word and register described by a prior ALTSW instruction. No other bits are modified. N (0-1) identifies a value's individual words by position in least-significant word order. The second syntax is intended for use after an ALTSW instruction in a loop to iteratively affect a series of word values within contiguous long registers.

::: pasm2
        SETWORD data, #$ABCD, #1  ' Set high word of data to $ABCD
:::



## SETXFRQ {#setxfrq}

Set streamer frequency
[Streamer](#streamer-category) - Set the streamer NCO frequency.

**SETXFRQ**  *{#}Dest*

---

**Result:** Streamer NCO frequency is set to Dest.

- Dest is a register or literal value (0-511) containing frequency value.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000011101 | --- | --- | --- | 2 |


**Related:** [XINIT](#xinit), [XCONT](#xcont)

**Explanation:**

Sets the streamer NCO (Numerically Controlled Oscillator) frequency to Dest. This controls the frequency at which the streamer outputs data.



## SEUSSF {#seussf}

Seuss forward
[Math and Logic](#math-and-logic) - Relocate and periodically invert bits using forward pattern.

**SEUSSF**  *Dest*

---

**Result:** Dest is transformed by relocating and periodically inverting bits. Returns to original value on 32nd iteration.

- Dest is a register to transform.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100100 | D | --- | --- | 2 |


**Related:** [SEUSSR](#seussr)

**Explanation:**

Relocates and periodically inverts bits within Dest using a forward pattern. The transformation returns to the original value after 32 iterations. This is useful for pseudo-random bit scrambling and data obfuscation.



## SEUSSR {#seussr}

Seuss reverse
[Math and Logic](#math-and-logic) - Relocate and periodically invert bits using reverse pattern.

**SEUSSR**  *Dest*

---

**Result:** Dest is transformed by relocating and periodically inverting bits. Returns to original value on 32nd iteration.

- Dest is a register to transform.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100101 | D | --- | --- | 2 |


**Related:** [SEUSSF](#seussf)

**Explanation:**

Relocates and periodically inverts bits within Dest using a reverse pattern. The transformation returns to the original value after 32 iterations. This is useful for pseudo-random bit scrambling and data obfuscation, providing the inverse operation of SEUSSF.



## SHL {#shl}

Shift left
[Math and Logic](#math-and-logic) - Shift bits left, inserting zeros as new rightmost bits.

**SHL**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted left by Src bits, inserting zeros (0) as new rightmost bits.

- Dest is a register containing the value to left shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000011 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [SHR](#shr), [SAL](#sal), [SAR](#sar), [ROL](#rol)

**Explanation:**

SHL shifts the destination's binary value left by the source number of places (0-31 bits) and sets the new LSBs to 0. This is useful for bit-stream manipulation as well as for swift multiplication; signed or unsigned 32-bit integer multiplication by a power-of-two. Care must be taken for power-of-two multiplications since upper bits shift through the MSB (sign bit), mangling large signed values.

::: pasm2
        SHL     value, #2      ' Multiply by 4
:::



## SHR {#shr}

Shift right
[Math and Logic](#math-and-logic) - Shift bits right, inserting zeros as new leftmost bits.

**SHR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The bits of Dest are shifted right by Src bits, inserting zeros (0) as new leftmost bits.

- Dest is a register containing the value to right shift.
- Src is a register or 5-bit literal (0-31) specifying the number of bit positions to shift.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0000010 | CZI | DDDDDDDDD | SSSSSSSSS | D | Last bit out\textsuperscript{1} | Result = 0 | 2 |


**Related:** [SHL](#shl), [SAR](#sar), [ROR](#ror)

**Explanation:**

SHR shifts the destination's binary value right by the source number of places (0-31 bits) and sets the new MSBs to 0. This is useful for bit-stream manipulation as well as for swift division; unsigned 32-bit integer division by a power-of-two. For similar division of a signed value, use SAR instead.

::: pasm2
        SHR     value, #3      ' Divide unsigned by 8
:::



## SIGNX {#signx}

Sign extend
[Math and Logic](#math-and-logic) - Sign-extend a value beyond a designated bit position.

**SIGNX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The Dest value is sign-extended above the bit indicated by Src and is stored in Dest. Optionally the C and Z flags are updated to the resulting MSB and zero status.

- Dest is a register containing the value to sign-extend above bit Src[4:0] and where the result is written.
- Src is a register or 9-bit literal whose value (lower 5 bits) identifies the bit of Dest to sign-extend beyond.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111011 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB of result | Result = 0 | 2 |


**Related:** [ZEROX](#zerox)

**Explanation:**

SIGNX fills the bits of Dest above the bit indicated by Src[4:0] with the value of that identified bit, i.e. sign-extending the value. This is handy when converting encoded or received signed values from a small bit width to a large bit width, i.e. 32 bits.

::: pasm2
        SIGNX   value, #7      ' Sign-extend 8-bit value to 32 bits
:::



## SKIP {#skip}

Skip instructions
[Branch](#branch) - Skip subsequent instructions based on a bitmask.

**SKIP**  *{#}Dest*

---

**Result:** Subsequent instructions 0-31 are cancelled for each '1' bit in Dest[0]-Dest[31].

- Dest is a register or literal value (0-511) containing skip pattern bitmask.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110001 | --- | --- | --- | 2 |


**Related:** [SKIPF](#skipf)

**Explanation:**

Skips instructions based on Dest bitmask. Subsequent instructions 0-31 get cancelled for each '1' bit in Dest[0]-Dest[31]. Each set bit causes the corresponding sequential instruction to be cancelled (replaced with NOP).

::: pasm2
        SKIP    #%10101        ' Skip instructions 0, 2, 4
        NOP                    ' Skipped (bit 0)
        ADD     x, #1          ' Executed (bit 1 = 0)
        NOP                    ' Skipped (bit 2)
:::



## SKIPF {#skipf}

Skip instructions fast
[Branch](#branch) - Rapidly skip over instructions by jumping the program counter.

**SKIPF**  *{#}Dest*

---

**Result:** Program counter leaps over cog/LUT instructions based on Dest bitmask.

- Dest is a register or literal value (0-511) containing skip pattern bitmask.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000110010 | --- | --- | --- | 2 |


**Related:** [SKIP](#skip)

**Explanation:**

Like SKIP, but instead of cancelling instructions, the PC leaps over them. This provides faster execution when skipping multiple instructions, as the skipped instructions are never fetched or executed.



## SPLITB {#splitb}

Split bits to bytes
[Math and Logic](#math-and-logic) - Reorganize bits by extracting every 4th bit into separate bytes.

**SPLITB**  *Dest*

---

**Result:** Dest = {Dest[31], Dest[27], Dest[23], Dest[19], ...Dest[12], Dest[8], Dest[4], Dest[0]}.

- Dest is a register to transform.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100000 | D | --- | --- | 2 |


**Related:** [SPLITW](#splitw), [MERGEB](#mergeb)

**Explanation:**

Splits every 4th bit of Dest into bytes. The bits at positions 0, 4, 8, 12, 16, 20, 24, 28 become the new low byte, the bits at positions 1, 5, 9, 13, 17, 21, 25, 29 become the second byte, and so on. This is useful for bit reordering and data unpacking operations.



## SPLITW {#splitw}

Split bits to words
[Math and Logic](#math-and-logic) - Reorganize bits by separating odd and even bits into separate words.

**SPLITW**  *Dest*

---

**Result:** Dest = {Dest[31], Dest[29], Dest[27], Dest[25], ...Dest[6], Dest[4], Dest[2], Dest[0]}.

- Dest is a register to transform.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001100010 | D | --- | --- | 2 |


**Related:** [SPLITB](#splitb), [MERGEW](#mergew)

**Explanation:**

Splits odd and even bits of Dest into separate words. The even bits (0, 2, 4, ...30) become the low word, and the odd bits (1, 3, 5, ...31) become the high word. This is useful for bit reordering and data unpacking operations.



## STALLI {#stalli}

Disallow interrupts
[Interrupt](#interrupt) - Disable interrupt branching to protect critical code sections.

**STALLI**

---

**Result:** All future interrupts are disallowed.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | 000100001 | 000100100 | --- | --- | --- | 2 |


**Related:** [ALLOWI](#allowi)

**Explanation:**

STALLI disables interrupt branching. STALLI is the complement of the ALLOWI instruction; both are used to protect short, vital sections of main code from timing jitter or state loss caused by asynchronous interrupt handling.

::: pasm2
        STALLI                 ' Disable interrupts
        ' Critical section...
        ALLOWI                 ' Re-enable interrupts
:::



## SUB {#sub}

Subtract
[Math and Logic](#math-and-logic) - Subtract one unsigned value from another.

**SUB**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Dest and unsigned Src is stored in Dest and optionally the C and Z flags are updated to the borrow and zero status.

- Dest is a register containing the value to subtract Src from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001100 | CZI | DDDDDDDDD | SSSSSSSSS | D | Borrow of (D - S) | Result = 0 | 2 |


**Related:** [SUBX](#subx), [SUBS](#subs), [SUBSX](#subsx), [SUBR](#subr), [ADD](#add)

**Explanation:**

SUB subtracts the unsigned Src from the unsigned Dest and stores the result into the Dest register. To subtract unsigned multi-long values, use SUB followed by SUBX as described in Subtracting Two Multi-Long Values. SUB and SUBX are also used in subtracting signed multi-long values with SUBSX ending the sequence.

::: pasm2
        SUB     count, #1 WZ   ' Decrement count, set Z if zero
:::



## SUBR {#subr}

Subtract reverse
[Math and Logic](#math-and-logic) - Subtract the destination from the source (reverse order).

**SUBR**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Src and unsigned Dest is stored in Dest and optionally the C and Z flags are updated to the borrow and zero status.

- Dest is a register containing the value to subtract from Src, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted by Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0010110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Borrow of (S - D) | Result = 0 | 2 |


**Related:** [SUB](#sub)

**Explanation:**

SUBR subtracts the unsigned Dest from the unsigned Src and stores the result into the Dest register. This is the reverse of the subtraction order of SUB, computing Src - Dest instead of Dest - Src.



## SUBS {#subs}

Subtract signed
[Math and Logic](#math-and-logic) - Subtract one signed value from another.

**SUBS**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of signed Dest and signed Src is stored in Dest and optionally the C and Z flags are updated to the sign and zero status.

- Dest is a register containing the value to subtract Src from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign of (D - S) | Result = 0 | 2 |


**Related:** [SUB](#sub), [SUBX](#subx), [SUBSX](#subsx)

**Explanation:**

SUBS subtracts the signed Src from the signed Dest and stores the result into the Dest register. If Src is a 9-bit literal, its value is interpreted as positive (0-511; it is not sign-extended). Use ##Value (or insert a prior AUGS instruction) for a 32-bit signed value; negative or positive. To subtract signed multi-long values, use SUB (not SUBS) followed possibly by SUBX, and finally SUBSX.



## SUBSX {#subsx}

Subtract signed extended
[Math and Logic](#math-and-logic) - Subtract one signed extended value from another using carry.

**SUBSX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of signed Dest and signed Src (plus C) is stored in Dest and optionally the C and Z flags are updated to the extended sign and zero status.

- Dest is a register containing the value to subtract Src plus C from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001111 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign of D-(S+C) | Z AND (Result = 0) | 2 |


**Related:** [SUB](#sub), [SUBX](#subx), [SUBS](#subs)

**Explanation:**

SUBSX subtracts the signed value of Src plus C from the signed Dest and stores the result into the Dest register. The SUBSX instruction is used to perform signed multi-long (extended) subtraction, such as 64-bit subtraction. Use WC or WCZ on preceding SUB and SUBX instructions for proper final C flag. Use WZ or WCZ on preceding SUB and SUBX instructions for proper final Z flag. To subtract signed multi-long values, use SUB (not SUBS) followed possibly by SUBX, and finally SUBSX.



## SUBX {#subx}

Subtract extended
[Math and Logic](#math-and-logic) - Subtract one unsigned extended value from another using carry.

**SUBX**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Difference of unsigned Dest and unsigned Src (plus C) is stored in Dest and optionally the C and Z flags are updated to the extended borrow and zero status.

- Dest is a register containing the value to subtract Src plus C from, and where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value plus C is subtracted from Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Borrow of (D - (S + C)) | Z AND (result = 0) | 2 |


**Related:** [SUB](#sub), [SUBSX](#subsx)

**Explanation:**

SUBX subtracts the unsigned value of Src plus C from the unsigned Dest and stores the result into the Dest register. The SUBX instruction is used to perform unsigned multi-long (extended) subtraction, such as 64-bit subtraction. Use WC or WCZ on preceding SUB and SUBX instructions for proper final C flag. If C is set after the last SUBX in a multi-long subtraction, it indicates unsigned underflow. Use WZ or WCZ on preceding SUB and SUBX instructions for proper final Z flag. To subtract unsigned multi-long values, use SUB followed by one or more SUBX instructions.



## SUMC / SUMNC / SUMZ / SUMNZ {#sumc}

Conditional sum {#sumnc} {#sumz} {#sumnz}
[Math and Logic](#math-and-logic) - Conditionally add or subtract based on C, NC, Z, or NZ flag.

**SUMC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**SUMNC**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**SUMZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**
**SUMNZ**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** Conditionally adds or subtracts Src from Dest based on flag state:

| Instruction | Subtracts when | Adds when |
|-------------|----------------|-----------|
| SUMC | C = 1 | C = 0 |
| SUMNC | C = 0 | C = 1 |
| SUMZ | Z = 1 | Z = 0 |
| SUMNZ | Z = 0 | Z = 1 |

- Dest is a register containing the value to adjust.
- Src is a register, 9-bit literal, or 32-bit augmented literal.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0011100 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0011101 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0011110 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |
| EEEE | 0011111 | CZI | DDDDDDDDD | SSSSSSSSS | D | Sign | Result = 0 | 2 |


**Explanation:**

These instructions conditionally add or subtract Src from Dest based on the specified flag state. The C flag (with WC) is updated to reflect the correct sign of the result.

SUMC and SUMZ subtract when their flag is set (1). SUMNC and SUMNZ subtract when their flag is clear (0), providing complementary behavior.


# Instructions: T

This section contains all PASM2 instructions beginning with the letter T.



## TEST {#test}

Test
[Math and Logic](#math-and-logic) - Test the parity and zero state of a register value.

**TEST**  *Dest*  **{WC|WZ|WCZ}**
**TEST**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The parity and zero-state of Dest, or of Dest bitwise ANDed with Src, is stored in the C and Z flags.

- Dest is a register whose value will be tested.
- Src is an optional register, 9-bit literal, or 32-bit augmented literal to AND with Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111110 | CZ0 | DDDDDDDDD | DDDDDDDDD | --- | Parity of D | D = 0 | 2 |
| EEEE | 0111110 | CZI | DDDDDDDDD | SSSSSSSSS | --- | Parity of (D \& S) | (D \& S) = 0 | 2 |


**Related:** [TESTN](#testn), [TESTB](#testb), [TESTBN](#testbn), [TESTP](#testp), [TESTPN](#testpn)

**Explanation:**

TEST determines the parity (number of high bits) and the zero or non-zero state of Dest, or of Dest bitwise ANDed with Src, and stores the results in the C and/or Z flag.

If the WC or WCZ effect is specified, the C flag is set to 1 if the number of high bits in Dest (or Dest ANDed with Src) is odd, or is cleared to 0 if it is even.

If the WZ or WCZ effect is specified, the Z flag is set to 1 if Dest (or Dest ANDed with Src) is zero, or is cleared to 0 if it is not zero.

TEST is non-destructive—it does not modify Dest.

::: pasm2
        TEST    flags WCZ      ' Test all bits for parity and zero
        TEST    value, #$FF WZ ' Test low byte for zero
:::



## TESTB {#testb}

Test bit
[Math and Logic](#math-and-logic) - Test a single bit in a register and write the result to C or Z.

**TESTB**  *Dest, {#}Src*  **WC/WZ**
**TESTB**  *Dest, {#}Src*  **ANDC/ANDZ**
**TESTB**  *Dest, {#}Src*  **ORC/ORZ**
**TESTB**  *Dest, {#}Src*  **XORC/XORZ**

---

**Result:** The state of bit Src[4:0] of Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register whose bit will be tested.
- Src is a register or 5-bit literal (0-31) specifying bit position.
- WC/WZ writes bit state directly to C or Z flag.
- ANDC/ANDZ ANDs bit state with C or Z flag.
- ORC/ORZ ORs bit state with C or Z flag.
- XORC/XORZ XORs bit state with C or Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100000 | CZI | DDDDDDDDD | SSSSSSSSS | --- | D[S[4:0]] | D[S[4:0]] | 2 |
| EEEE | 0100010 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z AND D[S[4:0]] | C/Z AND D[S[4:0]] | 2 |
| EEEE | 0100100 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z OR D[S[4:0]] | C/Z OR D[S[4:0]] | 2 |
| EEEE | 0100110 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z XOR D[S[4:0]] | C/Z XOR D[S[4:0]] | 2 |


**Related:** [TESTBN](#testbn), [TESTP](#testp), [TESTPN](#testpn)

**Explanation:**

TESTB reads the state (0 or 1) of a bit in Dest designated by Src, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The bit position is specified by Src[4:0] (0-31). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the bit state is applied to the selected flag.

TESTB is useful for examining individual bits without modifying the register value.

::: pasm2
        TESTB   flags, #7 WC   ' Test bit 7, store in C
        TESTB   mask, #3 ANDC  ' AND bit 3 with current C
:::



## TESTBN {#testbn}

Test bit negated
[Math and Logic](#math-and-logic) - Test a single bit in a register, invert the result, and write to C or Z.

**TESTBN**  *Dest, {#}Src*  **WC/WZ**
**TESTBN**  *Dest, {#}Src*  **ANDC/ANDZ**
**TESTBN**  *Dest, {#}Src*  **ORC/ORZ**
**TESTBN**  *Dest, {#}Src*  **XORC/XORZ**

---

**Result:** The inverted state of bit Src[4:0] of Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register whose bit will be tested.
- Src is a register or 5-bit literal (0-31) specifying bit position.
- WC/WZ writes inverted bit state to C or Z flag.
- ANDC/ANDZ ANDs inverted bit state with C or Z flag.
- ORC/ORZ ORs inverted bit state with C or Z flag.
- XORC/XORZ XORs inverted bit state with C or Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0100001 | CZI | DDDDDDDDD | SSSSSSSSS | --- | !D[S[4:0]] | !D[S[4:0]] | 2 |
| EEEE | 0100011 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z AND !D[S[4:0]] | C/Z AND !D[S[4:0]] | 2 |
| EEEE | 0100101 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z OR !D[S[4:0]] | C/Z OR !D[S[4:0]] | 2 |
| EEEE | 0100111 | CZI | DDDDDDDDD | SSSSSSSSS | --- | C/Z XOR !D[S[4:0]] | C/Z XOR !D[S[4:0]] | 2 |


**Related:** [TESTB](#testb), [TESTP](#testp), [TESTPN](#testpn)

**Explanation:**

TESTBN reads the state (0 or 1) of a bit in Dest designated by Src, inverts that result, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. The bit position is specified by Src[4:0] (0-31). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the inverted bit state is applied to the selected flag.

TESTBN is useful for testing whether a bit is clear (0) rather than set (1).



## TESTN {#testn}

Test not
[Math and Logic](#math-and-logic) - Test the parity and zero state of a register ANDed with an inverted value.

**TESTN**  *Dest, {#}Src*  **{WC|WZ|WCZ}**

---

**Result:** The parity and zero-state of Dest bitwise ANDed with !Src is stored in the C and Z flags.

- Dest is a register whose value will be tested.
- Src is a register, 9-bit literal, or 32-bit augmented literal to invert and AND with Dest.
- WC, WZ, or WCZ are optional effects to update flags.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111111 | CZI | DDDDDDDDD | SSSSSSSSS | --- | Parity of (D \& !S) | (D \& !S) = 0 | 2 |


**Related:** [TEST](#test), [TESTB](#testb), [TESTBN](#testbn)

**Explanation:**

TESTN determines the parity (number of high bits) and the zero or non-zero state of Dest bitwise ANDed with !Src and stores the results in the C and/or Z flag.

If the WC or WCZ effect is specified, the C flag is set to 1 if the number of high bits in Dest ANDed with !Src is odd, or is cleared to 0 if it is even.

If the WZ or WCZ effect is specified, the Z flag is set to 1 if Dest ANDed with !Src is zero, or is cleared to 0 if it is not zero.

TESTN is non-destructive—it does not modify Dest. It is useful for testing which bits in Dest are set while masking out specific bits defined by Src.



## TESTP / TESTPN {#testp}

Test pin / Test pin negated {#testpn}
[Pin](#pin) - Test the state of an I/O pin and write the result (or inverted result) to C or Z.

**TESTP**  *{#}Dest*  **WC/WZ**
**TESTP**  *{#}Dest*  **ANDC/ANDZ**
**TESTP**  *{#}Dest*  **ORC/ORZ**
**TESTP**  *{#}Dest*  **XORC/XORZ**

**TESTPN**  *{#}Dest*  **WC/WZ**
**TESTPN**  *{#}Dest*  **ANDC/ANDZ**
**TESTPN**  *{#}Dest*  **ORC/ORZ**
**TESTPN**  *{#}Dest*  **XORC/XORZ**

---

**Result:** The state (TESTP) or inverted state (TESTPN) of the I/O pin described by Dest is read and either stored as-is, or bitwise ANDed, ORed, or XORed into C or Z.

- Dest is a register or 6-bit literal (0-63) identifying the I/O pin.
- WC/WZ writes pin state to C or Z flag.
- ANDC/ANDZ ANDs pin state with C or Z flag.
- ORC/ORZ ORs pin state with C or Z flag.
- XORC/XORZ XORs pin state with C or Z flag.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000000 | --- | IN | IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000001 | --- | !IN | !IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000010 | --- | C/Z AND IN | C/Z AND IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000011 | --- | C/Z AND !IN | C/Z AND !IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000100 | --- | C/Z OR IN | C/Z OR IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000101 | --- | C/Z OR !IN | C/Z OR !IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000110 | --- | C/Z XOR IN | C/Z XOR IN | 2 |
| EEEE | 1101011 | CZL | DDDDDDDDD | 001000111 | --- | C/Z XOR !IN | C/Z XOR !IN | 2 |


IN = pin state at Dest[5:0]; !IN = inverted pin state.

**Related:** [TESTB](#testb), [TESTBN](#testbn), [DRVL](#drvl), [DRVH](#drvh)

**Explanation:**

TESTP reads the state (0 or 1) of the I/O pin designated by Dest, and either stores it as-is, or bitwise ANDs, ORs, or XORs it into C or Z. TESTPN does the same but inverts the pin state first. The pin number is specified by Dest[5:0] (0-63). The WC, WZ, ANDC, ANDZ, ORC, ORZ, XORC, or XORZ effect determines how the pin state is applied to the selected flag.

Both instructions read the actual pin state from the IN register, not the output register. This makes them useful for reading sensor inputs, detecting edges, and building multi-bit values from pin states. TESTPN is particularly useful for active-low signals where a low pin state (0) indicates an active condition.

::: pasm2
        TESTP   #10 WC         ' Read pin 10 state into C
        TESTP   sensor_pin WZ  ' Test sensor pin, store in Z
        TESTPN  #button WC     ' C=1 if active-low button pressed
:::



## TJF {#tjf}

Test and jump if full
[Branch](#branch) - Test a register value and jump if it equals $FFFF_FFFF.

**TJF**  *Dest, {#}Src*

---

**Result:** Dest is tested and if it is full ($FFFF_FFFF), PC is set to a new relative (#Src) or absolute (Src) address.

- Dest is a register whose value is tested for full.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011101 | 00I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |


**Related:** [TJNF](#tjnf), [TJZ](#tjz), [TJNZ](#tjnz)

**Explanation:**

TJF tests the value in Dest and jumps to the address described by Src if the result is full (= -1; = $FFFF_FFFF).

The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset (a range of -256 to +255 instructions) or use ##Label (or insert a prior AUGS instruction) for a 20-bit signed offset (a range of -524288 to +524287). Offsets are relative to the instruction following the TJF.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken (13-20 cycles for Hub execution when taken).



## TJNF {#tjnf}

Test and jump if not full
[Branch](#branch) - Test a register value and jump if it does not equal $FFFF_FFFF.

**TJNF**  *Dest, {#}Src*

---

**Result:** Dest is tested and if it is not full (<> $FFFF_FFFF), PC is set to a new relative (#Src) or absolute (Src) address.

- Dest is a register whose value is tested for not full.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011101 | 01I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |


**Related:** [TJF](#tjf), [TJZ](#tjz), [TJNZ](#tjnz), [TJS](#tjs), [TJNS](#tjns)

**Explanation:**

TJNF tests the value in Dest and jumps to the address described by Src if the result is not full (<> -1; <> $FFFF_FFFF).

The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset or use ##Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJNF.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.



## TJNS {#tjns}

Test and jump if not signed
[Branch](#branch) - Test a register value and jump if bit 31 is clear (positive/unsigned).

**TJNS**  *Dest, {#}Src*

---

**Result:** Dest is tested and if it is not signed (Dest[31] = 0), PC is set to a new relative (#Src) or absolute (Src) address.

- Dest is a register whose value is tested for sign bit.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011101 | 11I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |


**Related:** [TJS](#tjs), [TJZ](#tjz), [TJNZ](#tjnz)

**Explanation:**

TJNS tests the value in Dest and jumps to the address described by Src if the value is not signed (Dest[31] = 0). The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset or use ##Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJNS.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.



## TJZ / TJNZ {#tjz}

Test and jump if zero / not zero {#tjnz}
[Branch](#branch) - Test a register value and jump based on zero/non-zero result.

**TJZ**  *Dest, {#}Src*
**TJNZ**  *Dest, {#}Src*

---

**Result:** Dest is tested (not modified), and conditionally jumps:

| Instruction | Jumps when |
|-------------|------------|
| TJZ | Dest = 0 |
| TJNZ | Dest ≠ 0 |

- Dest is a register whose value is tested (unchanged).
- Src is the jump address: use # for relative, omit for absolute.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011100 | 10I | DDDDDDDDD | SSSSSSSSS | PC* | --- | --- | 2 or 4 |
| EEEE | 1011100 | 11I | DDDDDDDDD | SSSSSSSSS | PC* | --- | --- | 2 or 4 |

```{=latex}
*PC is written only when the jump condition is met.
```


**Related:** [TJF](#tjf), [TJNF](#tjnf), [TJS](#tjs), [TJNS](#tjns), [TJV](#tjv), [DJZ](#djz), [DJNZ](#djnz)

**Explanation:**

TJZ and TJNZ test Dest (without modifying it) and conditionally jump based on whether the value is zero or non-zero.

Unlike DJZ/DJNZ which decrement before testing, these instructions only test.

::: pasm2
        TJNZ    count, #loop   ' Loop while count <> 0
        TJZ     count, #done   ' Exit when count = 0
:::

Takes 2 clocks when not jumping, 4 clocks when jumping (pipeline flush).



## TJS {#tjs}

Test and jump if signed
[Branch](#branch) - Test a register value and jump if bit 31 is set (negative).

**TJS**  *Dest, {#}Src*

---

**Result:** Dest is tested and if it is signed (Dest[31] = 1), PC is set to a new relative (#Src) or absolute (Src) address.

- Dest is a register whose value is tested for sign bit.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011101 | 10I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |


**Related:** [TJNS](#tjns), [TJF](#tjf), [TJNF](#tjnf), [TJZ](#tjz), [TJNZ](#tjnz)

**Explanation:**

TJS tests the value in Dest and jumps to the address described by Src if the result is signed (Dest[31] = 1).

The address (Src) can be absolute or relative. To specify an absolute address, Src must be a register containing a 20-bit address value. To specify a relative address, use #Label for a 9-bit signed offset or use ##Label for a 20-bit signed offset. Offsets are relative to the instruction following the TJS.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.

::: pasm2
        TJS     value, #negative_handler  ' Jump if negative
:::



## TJV {#tjv}

Test and jump if overflow
[Branch](#branch) - Test a register value against the C flag and jump if overflow occurred.

**TJV**  *Dest, {#}Src*

---

**Result:** Dest is tested against C and if it has overflowed (Dest[31] != C), PC is set to a new relative (#Src) or absolute (Src) address.

- Dest is a register whose value is tested for overflow.
- Src is a register, 9-bit literal, or 20-bit augmented literal specifying jump address.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1011110 | 00I | DDDDDDDDD | SSSSSSSSS | PC (conditional) | --- | --- | 2 or 4 |


**Related:** [ADDS](#adds), [ADDSX](#addsx), [SUBS](#subs), [SUBSX](#subsx)

**Explanation:**

TJV tests the value in Dest against C and jumps to the address described by Src if Dest has overflowed (Dest[31] != C). This instruction requires that C be updated (to the correct sign) by the previous ADDS, ADDSX, SUBS, SUBSX, CMPS, CMPSX, or SUMx instruction. The address (Src) can be absolute or relative.

The instruction takes 2 cycles if the jump is not taken, or 4 cycles if taken.

::: pasm2
        ADDS    result, delta WC  ' Signed add, update C
        TJV     result, #overflow_handler
:::






## TRGINT1 {#trgint1}

Trigger interrupt 1
[Interrupt](#interrupt) - Software-trigger interrupt handler 1.

**TRGINT1**

---

**Result:** The INT1 interrupt handler is triggered regardless of STALLI mode.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | 000100010 | 000100100 | --- | --- | --- | 2 |


**Related:** [TRGINT2](#trgint2), [TRGINT3](#trgint3), [SETINT1](#setint1), [NIXINT1](#nixint1), [RETI0](#reti0)

**Explanation:**

TRGINT1 software-triggers interrupt handler 1, regardless of STALLI mode. This allows code to explicitly invoke the INT1 service routine without waiting for external events.



## TRGINT2 {#trgint2}

Trigger interrupt 2
[Interrupt](#interrupt) - Software-trigger interrupt handler 2.

**TRGINT2**

---

**Result:** The INT2 interrupt handler is triggered regardless of STALLI mode.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | 000100011 | 000100100 | --- | --- | --- | 2 |


**Related:** [TRGINT1](#trgint1), [TRGINT3](#trgint3), [SETINT2](#setint2), [NIXINT2](#nixint2), [RETI0](#reti0)

**Explanation:**

TRGINT2 software-triggers interrupt handler 2, regardless of STALLI mode. This allows code to explicitly invoke the INT2 service routine without waiting for external events.



## TRGINT3 {#trgint3}

Trigger interrupt 3
[Interrupt](#interrupt) - Software-trigger interrupt handler 3.

**TRGINT3**

---

**Result:** The INT3 interrupt handler is triggered regardless of STALLI mode.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | 000100100 | 000100100 | --- | --- | --- | 2 |


**Related:** [TRGINT1](#trgint1), [TRGINT2](#trgint2), [SETINT3](#setint3), [NIXINT3](#nixint3), [RETI0](#reti0)

**Explanation:**

TRGINT3 software-triggers interrupt handler 3, regardless of STALLI mode. This allows code to explicitly invoke the INT3 service routine without waiting for external events.


# Instructions: W

This section contains all PASM2 instructions beginning with the letter W.



## WAITATN {#waitatn}

Wait for attention
[Event](#event) - Wait for attention event from another cog.

**WAITATN**  **{WC|WZ|WCZ}**

---

**Result:** Waits for an attention event to occur (unless the event flag is already set), then clears the event flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011110 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [COGATN](#cogatn), [POLLATN](#pollatn), [JATN](#jatn), [JNATN](#jnatn)

**Explanation:**

WAITATN waits for an attention event to occur, stalling the pipeline until the event flag is set. The attention event flag is set whenever another cog issues an attention request for this cog using COGATN. The flag is cleared upon cog start or execution of POLLATN, WAITATN, JATN, or JNATN instructions.

To set an optional timeout, insert a SETQ instruction (with a future System Counter target value) immediately before WAITATN. The WC, WZ, or WCZ effect is recommended only when timeout is specified. Flags are set (1) if timeout occurred before the event, or cleared (0) if the event occurred before timeout.

During a wait, the pipeline is stalled—no instructions execute and no interrupts are processed in the cog until the wait condition ends.

::: pasm2
        WAITATN                ' Wait for attention from another cog
:::



## WAITCT1 / WAITCT2 / WAITCT3 {#waitct1}

Wait for counter event {#waitct2} {#waitct3}
[Event](#event) - Wait for counter event 1, 2, or 3 flag.

**WAITCT1**  **{WC|WZ|WCZ}**
**WAITCT2**  **{WC|WZ|WCZ}**
**WAITCT3**  **{WC|WZ|WCZ}**

---

**Result:** Waits for the specified counter event flag (CT1, CT2, or CT3) to be set, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010001 | 000100100 | --- | Timeout | Timeout | 2+ |
| EEEE | 1101011 | CZ0 | 000010010 | 000100100 | --- | Timeout | Timeout | 2+ |
| EEEE | 1101011 | CZ0 | 000010011 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [ADDCT1](#addct1), [ADDCT2](#addct2), [ADDCT3](#addct3), [POLLCT1](#pollct1), [POLLCT2](#pollct2), [POLLCT3](#pollct3), [JCT1](#jct1), [JCT2](#jct2), [JCT3](#jct3)

**Explanation:**

WAITCT1, WAITCT2, and WAITCT3 wait for counter events 1, 2, or 3 respectively, stalling the pipeline until the corresponding event flag is set. Each counter event flag is set whenever the System Counter (CT) passes the value in the corresponding event trigger register (CT1, CT2, or CT3).

The flags are cleared by execution of ADDCT*n*, POLLCT*n*, WAITCT*n*, JCT*n*, or JNCT*n* instructions (where *n* is 1, 2, or 3).

To set an optional timeout, insert a SETQ instruction immediately before the WAITCTn instruction.



## WAITFBW {#waitfbw}

Wait for FIFO block wrap
[Event](#event) - Wait for FIFO-interface-block-wrap event.

**WAITFBW**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a FIFO-interface-block-wrap event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011001 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [RDFAST](#rdfast), [WRFAST](#wrfast), [FBLOCK](#fblock), [POLLFBW](#pollfbw)

**Explanation:**

WAITFBW waits for a FIFO-interface-block-wrap event to occur, stalling the pipeline until the event flag is set. The FIFO-interface-block-wrap event flag is set whenever the Hub RAM FIFO interface exhausts its block count and reloads its block count and start address.

The FIFO-interface-block-wrap event flag is cleared upon execution of RDFAST, WRFAST, FBLOCK, POLLFBW, WAITFBW, JFBW, or JNFBW instructions.



## WAITINT {#waitint}

Wait for interrupt
[Event](#event) - Wait for interrupt-occurred event.

**WAITINT**  **{WC|WZ|WCZ}**

---

**Result:** Waits for an interrupt-occurred event, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010000 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [POLLINT](#pollint), [JINT](#jint), [JNINT](#jnint)

**Explanation:**

WAITINT waits for an interrupt-occurred event to occur, stalling the pipeline until the event flag is set. The interrupt-occurred event flag is set whenever interrupt 1, 2, or 3 occurs—debug interrupts are ignored.

The interrupt-occurred event flag is cleared upon cog start or execution of POLLINT, WAITINT, JINT, or JNINT instructions.



## WAITPAT {#waitpat}

Wait for pattern
[Event](#event) - Wait for pin-pattern-detected event.

**WAITPAT**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a pin-pattern-detected event, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011000 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [SETPAT](#setpat), [POLLPAT](#pollpat), [JPAT](#jpat), [JNPAT](#jnpat)

**Explanation:**

WAITPAT waits for a pin-pattern-detected event to occur, stalling the pipeline until the event flag is set. The pin-pattern-detected event flag is set whenever the masked input pins match or don't match the pattern described by a previous SETPAT instruction.

The pin-pattern-detected event flag is cleared upon execution of SETPAT, POLLPAT, WAITPAT, JPAT, or JNPAT instructions.

::: pasm2
        SETPAT  mask, pattern  ' Set up pattern detector
        WAITPAT                ' Wait for pattern match
:::



## WAITSE1 {#waitse1}

Wait for selectable event 1
[Event](#event) - Wait for selectable event 1 flag.

**WAITSE1**  **{WC|WZ|WCZ}**

---

**Result:** Waits for the SE1 selectable event flag to be set, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010100 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITSE2](#waitse2), [WAITSE3](#waitse3), [WAITSE4](#waitse4), [SETSE1](#setse1), [POLLSE1](#pollse1)

**Explanation:**

WAITSE1 waits for selectable event 1 to occur, stalling the pipeline until the SE1 event flag is set. The flag is cleared by execution of SETSE1, POLLSE1, WAITSE1, JSE1, or JNSE1 instructions.



## WAITSE2 {#waitse2}

Wait for selectable event 2
[Event](#event) - Wait for selectable event 2 flag.

**WAITSE2**  **{WC|WZ|WCZ}**

---

**Result:** Waits for the SE2 selectable event flag to be set, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010101 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITSE1](#waitse1), [WAITSE3](#waitse3), [WAITSE4](#waitse4), [SETSE2](#setse2), [POLLSE2](#pollse2)

**Explanation:**

WAITSE2 waits for selectable event 2 to occur, stalling the pipeline until the SE2 event flag is set. The flag is cleared by execution of SETSE2, POLLSE2, WAITSE2, JSE2, or JNSE2 instructions.



## WAITSE3 {#waitse3}

Wait for selectable event 3
[Event](#event) - Wait for selectable event 3 flag.

**WAITSE3**  **{WC|WZ|WCZ}**

---

**Result:** Waits for the SE3 selectable event flag to be set, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010110 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITSE1](#waitse1), [WAITSE2](#waitse2), [WAITSE4](#waitse4), [SETSE3](#setse3), [POLLSE3](#pollse3)

**Explanation:**

WAITSE3 waits for selectable event 3 to occur, stalling the pipeline until the SE3 event flag is set. The flag is cleared by execution of SETSE3, POLLSE3, WAITSE3, JSE3, or JNSE3 instructions.



## WAITSE4 {#waitse4}

Wait for selectable event 4
[Event](#event) - Wait for selectable event 4 flag.

**WAITSE4**  **{WC|WZ|WCZ}**

---

**Result:** Waits for the SE4 selectable event flag to be set, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000010111 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITSE1](#waitse1), [WAITSE2](#waitse2), [WAITSE3](#waitse3), [SETSE4](#setse4), [POLLSE4](#pollse4)

**Explanation:**

WAITSE4 waits for selectable event 4 to occur, stalling the pipeline until the SE4 event flag is set. The flag is cleared by execution of SETSE4, POLLSE4, WAITSE4, JSE4, or JNSE4 instructions.



## WAITX {#waitx}

Wait cycles
[Event](#event) - Wait for Dest+1 clock cycles.

**WAITX**  *{#}Dest*  **{WC|WZ|WCZ}**

---

**Result:** Stalls the cog for Dest+1 clock cycles, providing precise timing delays. Sets C and Z to 0 after completion.

- Dest is the number of cycles minus 1 to wait (0-511 for immediate).
- WC, WZ, or WCZ are optional; always set to 0 after completion.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZL | DDDDDDDDD | 000011111 | --- | 0 | 0 | 2 + D |


**Related:** [WAITCT1](#waitct1), [WAITCT2](#waitct2), [WAITCT3](#waitct3)

**Explanation:**

WAITX stalls the cog for precise timing delays. The actual wait time is Dest+1 cycles minimum. This instruction is critical for bit-banging protocols, PWM generation, and timing-sensitive operations where precise delays are required.

WAITX blocks cog execution completely—no instructions execute and no interrupts are processed during the wait period. For long delays, consider using WAITCT instructions instead.

::: pasm2
        WAITX   #99            ' Wait 100 clock cycles
:::



## WAITXFI {#waitxfi}

Wait for streamer finished
[Event](#event) - Wait for streamer-finished event.

**WAITXFI**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a streamer-finished event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011011 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITXMT](#waitxmt), [WAITXRL](#waitxrl), [WAITXRO](#waitxro), [XINIT](#xinit), [XCONT](#xcont)

**Explanation:**

WAITXFI waits for a streamer-finished event to occur, stalling the pipeline until the event flag is set. The streamer-finished event flag is set whenever the streamer runs out of commands to process.

The streamer-finished event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXFI, WAITXFI, JXFI, or JNXFI instructions.



## WAITXMT {#waitxmt}

Wait for streamer empty
[Event](#event) - Wait for streamer-empty event.

**WAITXMT**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a streamer-empty event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011010 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXRL](#waitxrl), [WAITXRO](#waitxro), [XINIT](#xinit), [XCONT](#xcont)

**Explanation:**

WAITXMT waits for a streamer-empty event to occur, stalling the pipeline until the event flag is set. The streamer-empty event flag is set whenever the streamer is ready for a new command.

The streamer-empty event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXMT, WAITXMT, JXMT, or JNXMT instructions.



## WAITXRL {#waitxrl}

Wait for streamer LUT rollover
[Event](#event) - Wait for streamer-LUT-RAM-rollover event.

**WAITXRL**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a streamer-LUT-RAM-rollover event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011101 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXMT](#waitxmt), [WAITXRO](#waitxro), [POLLXRL](#pollxrl)

**Explanation:**

WAITXRL waits for a streamer-LUT-RAM-rollover event to occur, stalling the pipeline until the event flag is set. The streamer-LUT-RAM-rollover event flag is set whenever location $1FF of the Lookup RAM is read by the streamer.

The streamer-LUT-RAM-rollover event flag is cleared upon cog start or execution of POLLXRL, WAITXRL, JXRL, or JNXRL instructions.



## WAITXRO {#waitxro}

Wait for streamer NCO rollover
[Event](#event) - Wait for streamer-NCO-rollover event.

**WAITXRO**  **{WC|WZ|WCZ}**

---

**Result:** Waits for a streamer-NCO-rollover event to occur, then clears the flag and resumes execution.

- WC, WZ, or WCZ are optional effects to set flags on timeout.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | 000011100 | 000100100 | --- | Timeout | Timeout | 2+ |


**Related:** [WAITXFI](#waitxfi), [WAITXMT](#waitxmt), [WAITXRL](#waitxrl), [POLLXRO](#pollxro)

**Explanation:**

WAITXRO waits for a streamer-NCO-rollover event to occur, stalling the pipeline until the event flag is set. The streamer-NCO-rollover event flag is set whenever the streamer's numerically-controlled oscillator (NCO) rolls over.

The streamer-NCO-rollover event flag is cleared upon execution of XINIT, XZERO, XCONT, POLLXRO, WAITXRO, JXRO, or JNXRO instructions.



## WFBYTE {#wfbyte}

Write FIFO byte
[Hub FIFO](#hub-fifo) - Write byte to FIFO.

**WFBYTE**  *{#}Dest*

---

**Result:** Writes the byte in Dest[7:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the byte value to write (bits 7:0 used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010101 | --- | --- | --- | 2 |


**Related:** [WFWORD](#wfword), [WFLONG](#wflong), [WRFAST](#wrfast)

**Explanation:**

WFBYTE writes a byte from Dest[7:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes.

Only the lower 8 bits of Dest are written. WFBYTE executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.



## WFLONG {#wflong}

Write FIFO long
[Hub FIFO](#hub-fifo) - Write long to FIFO.

**WFLONG**  *{#}Dest*

---

**Result:** Writes the long in Dest[31:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the long value to write (all 32 bits used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010111 | --- | --- | --- | 2 |


**Related:** [WFBYTE](#wfbyte), [WFWORD](#wfword), [WRFAST](#wrfast)

**Explanation:**

WFLONG writes a long (32-bit value) from Dest[31:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes.

All 32 bits of Dest are written. WFLONG executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.



## WFWORD {#wfword}

Write FIFO word
[Hub FIFO](#hub-fifo) - Write word to FIFO.

**WFWORD**  *{#}Dest*

---

**Result:** Writes the word in Dest[15:0] into the FIFO. Must be used after WRFAST has configured the FIFO.

- Dest is the word value to write (bits 15:0 used).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000010110 | --- | --- | --- | 2 |


**Related:** [WFBYTE](#wfbyte), [WFLONG](#wflong), [WRFAST](#wrfast)

**Explanation:**

WFWORD writes a word (16-bit value) from Dest[15:0] into the Hub FIFO interface. This instruction must be used after WRFAST has configured the FIFO for fast Hub memory writes.

Only the lower 16 bits of Dest are written. WFWORD executes in 2 clock cycles when the FIFO is ready. If the FIFO is full, execution stalls until space becomes available.



## WMLONG {#wmlong}

Write masked long
[Hub RAM](#hub-ram) - Write masked long to hub RAM (non-zero bytes only).

**WMLONG**  *Dest, {#}Src/P*

---

**Result:** Writes only non-$00 bytes in Dest[31:0] to hub address Src/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer.

- Dest is the long value with bytes to write (non-zero bytes only).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1010011 | 11I | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 |


**Related:** [WRLONG](#wrlong), [WRBYTE](#wrbyte), [WRWORD](#wrword)

**Explanation:**

WMLONG writes only non-zero bytes from Dest to Hub RAM at address Src. Each byte in Dest is examined: if the byte is $00, that byte position in Hub RAM is not modified; if the byte is non-zero, it is written to Hub RAM.

This masked write capability is useful for sprite graphics, text overlay, and other applications where selective pixel/byte updates are needed without affecting other data in the same long.

Prior execution of SETQ or SETQ2 invokes cog or LUT block transfer mode.



## WRBYTE {#wrbyte}

Write byte
[Hub RAM](#hub-ram) - Write byte to hub RAM.

**WRBYTE**  *{#}Dest, {#}Src/P*

---

**Result:** Writes the byte in Dest[7:0] to hub address Src/PTRx.

- Dest is the byte value to write (bits 7:0 used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100010 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 |


**Related:** [WRWORD](#wrword), [WRLONG](#wrlong), [RDBYTE](#rdbyte)

**Explanation:**

WRBYTE writes the byte in Dest[7:0] to Hub RAM at address Src/PTRx. Only the lower 8 bits of Dest are written.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. When Src specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes can be applied for sequential access.

::: pasm2
        WRBYTE  value, ptra++  ' Write byte, increment pointer
:::



## WRC / WRNC / WRZ / WRNZ {#wrc}

Write flag to register {#wrnc} {#wrz} {#wrnz}
[Math and Logic](#math-and-logic) - Write C, NC, Z, or NZ flag value to register.

**WRC**  *Dest*
**WRNC**  *Dest*
**WRZ**  *Dest*
**WRNZ**  *Dest*

---

**Result:** Writes 0 or 1 to Dest based on the specified flag condition:

| Instruction | Dest value |
|-------------|------------|
| WRC | 1 if C=1, else 0 |
| WRNC | 1 if C=0, else 0 |
| WRZ | 1 if Z=1, else 0 |
| WRNZ | 1 if Z=0, else 0 |

- Dest is the destination register. Upper 31 bits are cleared to zero.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101100 | D | --- | --- | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101101 | D | --- | --- | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101110 | D | --- | --- | 2 |
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101111 | D | --- | --- | 2 |


**Explanation:**

These instructions copy flag states to a register, providing a convenient way to convert flag conditions into numeric values for computation or storage.

WRC and WRZ write the direct flag state (C or Z), while WRNC and WRNZ write the inverted flag state. The result is always 0 or 1; the upper 31 bits of Dest are cleared.



## WRFAST {#wrfast}

Write FIFO setup
[Hub FIFO](#hub-fifo) - Begin new fast hub write via FIFO.

**WRFAST**  *{#}Dest, {#}Src*

---

**Result:** Initializes the Hub FIFO for fast writes. Dest[31] = no wait, Dest[13:0] = block size in 64-byte units (0 = max), Src[19:0] = block start address.

- Dest contains configuration: bit 31 = nowait, bits 13:0 = block size.
- Src contains Hub RAM start address (bits 19:0).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100100 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 or WRFAST finish + 3 |


**Related:** [WFBYTE](#wfbyte), [WFWORD](#wfword), [WFLONG](#wflong), [RDFAST](#rdfast)

**Explanation:**

WRFAST configures the Hub FIFO interface for fast streaming writes to Hub RAM. After WRFAST executes, use WFBYTE, WFWORD, or WFLONG to write data through the FIFO.

Dest[13:0] specifies the block size in 64-byte units. A value of 0 selects the maximum block size. Dest[31] controls wait behavior: if set, FIFO writes proceed without stalling.

Src[19:0] specifies the starting Hub RAM address. The FIFO automatically increments the address as data is written.

::: pasm2
        WRFAST  #0, buffer_addr  ' Set up FIFO write to buffer
        WFLONG  data               ' Write data to FIFO
:::



## WRLONG {#wrlong}

Write long
[Hub RAM](#hub-ram) - Write long to hub RAM.

**WRLONG**  *{#}Dest, {#}Src/P*

---

**Result:** Writes the long in Dest[31:0] to hub address Src/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer.

- Dest is the long value to write (all 32 bits used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100011 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 |


**Related:** [WRBYTE](#wrbyte), [WRWORD](#wrword), [WMLONG](#wmlong), [RDLONG](#rdlong)

**Explanation:**

WRLONG writes the 32-bit value in Dest to Hub RAM at address Src/PTRx. All 32 bits of Dest are written.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. When Src specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes can be applied for sequential access.

Prior execution of SETQ or SETQ2 invokes block transfer mode, writing multiple longs from cog or LUT RAM to Hub RAM in a burst transfer.

::: pasm2
        SETQ    #16-1          ' Set up for 16-long block transfer
        WRLONG  buffer, ptra   ' Write 16 longs to hub
:::



## WRLUT {#wrlut}

Write LUT
[Lookup Table](#lookup-table) - Write Dest to LUT address.

**WRLUT**  *{#}Dest, {#}Src/P*

---

**Result:** Writes Dest to LUT address Src/PTRx.

- Dest is the value to write.
- Src/P is the LUT address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100001 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [RDLUT](#rdlut), [WRLONG](#wrlong), [SETQ](#setq)

**Explanation:**

WRLUT writes the value in Dest to the Lookup Table (LUT) at address Src/PTRx. The LUT is a 512-long (2KB) fast memory space.

When Src specifies PTRA or PTRB, the pointer value is used as the LUT address. Only the lower 9 bits of the address are used (0-511).

WRLUT executes in 2 clock cycles, providing fast access to LUT RAM for lookup tables, buffers, and temporary storage.

::: pasm2
        WRLUT   value, #100    ' Write to LUT address 100
:::



## WRPIN {#wrpin}

Write pin mode
[Smart Pin](#smart-pin) - Configure smart pin mode.

**WRPIN**  *{#}Dest, {#}Src*

---

**Result:** Sets the mode of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the smart pin mode configuration.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100000 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WXPIN](#wxpin), [WYPIN](#wypin), [RDPIN](#rdpin), [AKPIN](#akpin)

**Explanation:**

WRPIN configures the operating mode of one or more Smart Pins. Each of the P2's 64 pins has a dedicated Smart Pin module capable of autonomous operation for PWM, serial I/O, pulse measurement, ADC, and many other functions.

**CRITICAL REQUIREMENT**: Smart pins MUST be reset (DIR=0) before configuring with WRPIN.

The standard configuration sequence is:
1. DIRL pin — Reset smart pin (required)
2. WRPIN mode, pin — Configure smart pin mode
3. WXPIN x, pin — Set X parameter
4. WYPIN y, pin — Set Y parameter
5. DIRH pin — Enable smart pin

WRPIN #0, pin clears all smart pin configuration.

::: pasm2
        DIRL    #10            ' Reset pin 10
        WRPIN   pwm_mode, #10  ' Configure for PWM
        WXPIN   period, #10    ' Set period
        DIRH    #10            ' Enable
:::



## WRWORD {#wrword}

Write word
[Hub RAM](#hub-ram) - Write word to hub RAM.

**WRWORD**  *{#}Dest, {#}Src/P*

---

**Result:** Writes the word in Dest[15:0] to hub address Src/PTRx.

- Dest is the word value to write (bits 15:0 used).
- Src/P is the hub address or pointer (PTRA/PTRB).


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100010 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 3...10 |


**Related:** [WRBYTE](#wrbyte), [WRLONG](#wrlong), [RDWORD](#rdword)

**Explanation:**

WRWORD writes the word (16-bit value) in Dest[15:0] to Hub RAM at address Src/PTRx. Only the lower 16 bits of Dest are written.

The instruction takes 3 to 10 clock cycles depending on Hub RAM timing. When Src specifies PTRA or PTRB, the pointer value is used as the Hub address. Pointer auto-increment modes can be applied for sequential access.



## WXPIN {#wxpin}

Write pin X parameter
[Smart Pin](#smart-pin) - Set smart pin X parameter.

**WXPIN**  *{#}Dest, {#}Src*

---

**Result:** Sets the X register of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the X parameter value.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100000 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WRPIN](#wrpin), [WYPIN](#wypin), [RDPIN](#rdpin)

**Explanation:**

WXPIN sets the X parameter of one or more Smart Pins. The X register meaning depends on the smart pin mode:

- For PWM modes: Sets frame period or duty cycle parameter
- For serial modes: Controls bit timing and configuration
- For pulse measurement: Sets measurement parameters
- For transition modes: Controls timebase

Writing the X register also acknowledges the smart pin, clearing any completion flags.



## WYPIN {#wypin}

Write pin Y parameter
[Smart Pin](#smart-pin) - Set smart pin Y parameter.

**WYPIN**  *{#}Dest, {#}Src*

---

**Result:** Sets the Y register of smart pins Src[10:6]+Src[5:0]..Src[5:0] to Dest, acknowledges smart pins. Wraps within A/B pins. Prior SETQ overrides Src[10:6].

- Dest is the Y parameter value.
- Src is the pin number or pin range.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100001 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [WRPIN](#wrpin), [WXPIN](#wxpin), [RDPIN](#rdpin)

**Explanation:**

WYPIN sets the Y parameter of one or more Smart Pins. The Y register serves multiple purposes depending on smart pin mode:

- For PWM modes: Sets the base period
- For SPI/serial modes: Controls data to transmit
- For counter modes: Sets count value
- For ADC modes: Initiates conversions

Writing the Y register also acknowledges pin completion, clearing any completion flags. This dual purpose makes WYPIN essential for continuous smart pin operation—it both provides new data and signals that previous results have been processed.

::: pasm2
        WYPIN   pwm_value, #10  ' Set PWM duty and acknowledge
:::


# Instructions: X

This section contains all PASM2 instructions beginning with the letter X. The X instructions include the XOR logic operation, the xoroshiro32+ PRNG instruction, and the streamer control family.



## XCONT {#xcont}

Execute continue
[Streamer](#streamer-category) - Buffer new streamer command to continue from current phase.

**XCONT**  *{#}Dest, {#}Src*

---

**Result:** Buffers a new streamer command to execute when the current command completes its final NCO rollover, continuing from current phase.

- Dest is the streamer mode configuration.
- Src is the data value or hub address for the streamer operation.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100110 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2+ |


**Related:** [XINIT](#xinit), [XZERO](#xzero), [XSTOP](#xstop), [WAITXFI](#waitxfi)

**Explanation:**

XCONT buffers a new streamer command that executes automatically when the current command completes. Unlike XINIT and XZERO, XCONT preserves the phase accumulator, allowing seamless continuation of streamer operations without phase discontinuities.

This instruction enables chaining multiple streamer operations together while maintaining phase coherence. The buffered command waits for the current command's NCO (numerically controlled oscillator) to complete its final rollover before activation.

The mode word in Dest specifies the streamer configuration including pin assignments, data direction, and transfer format. The Src parameter provides either immediate data or a hub memory address depending on the mode configuration.



## XINIT {#xinit}

Execute initialize
[Streamer](#streamer-category) - Issue streamer command immediately, zeroing phase.

**XINIT**  *{#}Dest, {#}Src*

---

**Result:** Issues a streamer command immediately with the phase accumulator reset to zero.

- Dest is the streamer mode configuration.
- Src is the data value or hub address for the streamer operation.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100101 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2 |


**Related:** [XCONT](#xcont), [XZERO](#xzero), [XSTOP](#xstop), [WAITXFI](#waitxfi), [SETXFRQ](#setxfrq)

**Explanation:**

XINIT starts a streamer operation immediately, resetting the phase accumulator to zero. This provides a clean starting point for high-speed data transfers between the cog and hub memory or I/O pins.

The streamer operates as a hardware DMA engine, transferring data without CPU intervention. The mode word in Dest configures critical parameters:
- Transfer direction (input from pins to hub, output from hub to pins, or cog-only operations)
- Number of pins involved in the transfer
- Data formatting (bit order, byte packing, word sizes)

The Src parameter provides either the data source (for immediate transfers) or a hub memory address (for hub-based transfers).

XINIT commonly coordinates with smart pins to achieve maximum I/O throughput:

::: pasm2
        XINIT   mode, data         ' Start data transfer
        WYPIN   count, #clk_pin    ' Start clock generation
        WAITXFI                    ' Wait for completion
:::

This parallel operation eliminates CPU intervention, enabling sustained high-speed data rates limited only by the configured clock frequency.



## XOR {#xor}

Exclusive or
[Math and Logic](#math-and-logic) - Bitwise XOR a value with another.

**XOR**  *Dest, {#}Src*  **{WC/WZ/WCZ}**

---

**Result:** Dest XOR Src is stored in Dest. Optionally sets C to parity of result and Z if result equals zero.

- Dest is the register containing the value to XOR with Src.
- Src is a register or 9-bit literal whose value is XORed with Dest.
- WC sets C to the parity (odd number of 1 bits) of the result.
- WZ sets Z if the result equals zero.
- WCZ sets both C and Z.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0101011 | CZI | DDDDDDDDD | SSSSSSSSS | D | Parity | Zero | 2 |


**Related:** [AND](#and), [OR](#or), [ANDN](#andn), [TEST](#test)

**Explanation:**

XOR performs a bitwise exclusive OR operation between Dest and Src, storing the result in Dest. Each bit position in the result is set to 1 if the corresponding bits in Dest and Src differ, or 0 if they match.

The exclusive OR operation has several important properties:
- XORing a value with itself produces zero (useful for clearing registers)
- XORing a value with all 1s produces the bitwise complement
- XORing twice with the same value returns the original (useful for simple encryption)
- XOR is commutative: A XOR B equals B XOR A

When the WC effect is specified, the C flag receives the parity of the result—set to 1 if the result contains an odd number of 1 bits, or cleared to 0 for an even number. This provides a fast parity calculation.

When the WZ effect is specified, the Z flag is set if the result equals zero (meaning Dest and Src were identical), or cleared if the result is non-zero (Dest and Src differ in at least one bit).



## XORO32 {#xoro32}

Xoroshiro 32
[Math and Logic](#math-and-logic) - Iterate Dest with xoroshiro32+ PRNG algorithm.

**XORO32**  *Dest*

---

**Result:** Dest is updated with the next PRNG state. The generated random value is placed into the S field of the next instruction.

- Dest is the register containing the 32-bit PRNG state.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 000 | DDDDDDDDD | 001101000 | D | --- | --- | 2 |


**Related:** [GETRND](#getrnd), [SETQ](#setq)

**Explanation:**

XORO32 implements one iteration of the xoroshiro32+ algorithm, a fast, high-quality pseudo-random number generator. The instruction updates the generator state in Dest and simultaneously makes the generated random value available to the next instruction by injecting it into that instruction's S field.

The xoroshiro32+ algorithm provides excellent statistical properties for a 32-bit generator:
- Long period (2^32 - 1 values before repeating)
- Good distribution across all output bits
- Fast execution (2 clocks per random number)
- Small state requirement (single 32-bit value)

::: pasm2
        MOV     seed, initial_value  ' Initialize with non-zero seed

.loop   XORO32  seed                 ' Advance PRNG state
        MOV     random_val, 0        ' Next instruction receives random in S
        ' Process random_val...
:::

The random value appears in the S field of the instruction immediately following XORO32. This means the next instruction must be one that reads from S, and the value specified for S in that instruction's encoding is ignored—it gets replaced by the random value.

The seed value in Dest must be non-zero. A seed of zero will produce only zero values. For best results, initialize the seed with a value from GETRND or another entropy source.



## XSTOP {#xstop}

Execute stop
[Streamer](#streamer-category) - Stop streamer immediately.

**XSTOP**

---

**Result:** The currently active streamer operation terminates immediately.

- Takes no operands.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100101 | 011 | 000000000 | 000000000 | --- | --- | --- | 2 |


**Related:** [XINIT](#xinit), [XCONT](#xcont), [XZERO](#xzero), [WAITXFI](#waitxfi)

**Explanation:**

XSTOP immediately halts any active streamer operation. This provides programmatic control to abort streamer transfers before completion.

When XSTOP executes, the streamer hardware stops all data movement and pin activity. Any buffered streamer command (from XCONT or XZERO) is also discarded.

XSTOP is useful when:
- Error conditions require aborting a transfer
- Dynamic control flow needs to terminate streaming based on data content
- Cleanup is required before reconfiguring the streamer

After XSTOP, the streamer remains idle until a new XINIT command is issued. The phase accumulator state is undefined after XSTOP—use XINIT (which zeros the phase) rather than XCONT to restart operations.



## XZERO {#xzero}

Execute zero
[Streamer](#streamer-category) - Buffer new streamer command, zeroing phase.

**XZERO**  *{#}Dest, {#}Src*

---

**Result:** Buffers a new streamer command to execute when the current command completes, resetting phase to zero.

- Dest is the streamer mode configuration.
- Src is the data value or hub address for the streamer operation.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1100101 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2+ |


**Related:** [XINIT](#xinit), [XCONT](#xcont), [XSTOP](#xstop), [WAITXFI](#waitxfi)

**Explanation:**

XZERO buffers a new streamer command that executes automatically when the current command completes, with the phase accumulator reset to zero. This combines the buffering behavior of XCONT with the phase-zeroing behavior of XINIT.

The buffered command waits for the current streamer operation's NCO (numerically controlled oscillator) to complete its final rollover before activation. When activation occurs, the phase accumulator resets to zero, providing a clean starting point for the new operation.

This instruction enables chaining multiple streamer operations where each operation should start from a known phase state. This is particularly useful when switching between different streamer modes or when phase coherence between operations is not required.

The mode word in Dest specifies the streamer configuration including pin assignments, data direction, and transfer format. The Src parameter provides either immediate data or a hub memory address depending on the mode configuration.


# Instructions: Z

This section contains all PASM2 instructions beginning with the letter Z. There is currently one Z instruction: ZEROX for zero extension.



## ZEROX {#zerox}

Zero extend
[Math and Logic](#math-and-logic) - Zero-extend a value beyond a designated bit.

**ZEROX**  *Dest, {#}Src*  **{WC/WZ/WCZ}**

---

**Result:** Dest is zero-extended above the bit indicated by Src[4:0]. Optionally sets C to MSB of result and Z if result equals zero.

- Dest is the register containing the value to zero-extend.
- Src is a register or 9-bit literal identifying the bit position (0-31) beyond which to zero-extend.
- WC sets C to the MSB (bit 31) of the result.
- WZ sets Z if the result equals zero.
- WCZ sets both C and Z.


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0111010 | CZI | DDDDDDDDD | SSSSSSSSS | D | MSB | Zero | 2 |


**Related:** [SIGNX](#signx)

**Explanation:**

ZEROX fills the bits of Dest, above the bit indicated by Src[4:0], with zeros, effectively zero-extending the value. This is useful when converting encoded or received unsigned values from a smaller bit width to 32 bits.

For example, if Dest contains $FFFF_FFFF and Src contains 7, ZEROX clears bits 31 down to bit 8, leaving only bits 7-0 intact. The result in Dest becomes $0000_00FF.

The instruction examines only the lower 5 bits of Src (Src[4:0]), allowing bit positions 0 through 31 to be specified. This makes ZEROX particularly useful for extracting and zero-extending bit fields from packed data structures or network protocols.

::: pasm2
        ' Extract lower byte and zero-extend
        MOV     data, big_value
        ZEROX   data, #7         ' Keep bits 7-0, clear bits 31-8
                                 ' If big_value was $FFFF_FFFF,
                                 ' data becomes $0000_00FF
:::

ZEROX is the complement to SIGNX. While ZEROX fills upper bits with zeros (for unsigned values), SIGNX fills upper bits with the value of the designated bit (for signed values). Use ZEROX when working with unsigned data, and SIGNX when working with signed data that needs proper sign extension.


# Assembler Directives

Assembler directives control the assembly process itself. Unlike instructions that generate executable code, directives guide the assembler in organizing memory, reserving space, and verifying code constraints. Directives execute at assembly time, not runtime.

The P2 assembler provides 13 directives organized into five functional categories: origin control, memory definition, size verification, alignment, and space management.



## Origin Control Directives

Origin directives set the memory address where subsequent code or data will be assembled. The P2 distinguishes between cog RAM (0-$1FF) and hub RAM addresses.

### ORG

Set the assembly origin to a specific cog RAM address. All subsequent instructions assemble starting from this address.

#### Syntax
```pasm
        ORG     address
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Cog RAM address (0-$1FF, range 0-511 decimal) |

#### Usage
Use ORG to position code or data at specific cog RAM addresses. This is essential for creating interrupt vectors, placing time-critical code at optimal locations, or organizing cog memory layout.

#### Example
```pasm
        ORG     0               ' Start at cog RAM address 0
entry   jmp     #main           ' First instruction at address 0

        ORG     $100            ' Start at cog address $100
table   long    1, 2, 3         ' Data table at specific address
```

#### Notes
- ORG affects cog RAM addresses only (range 0-$1FF)
- For hub RAM addresses, use ORGH
- To fill gaps between addresses with zeros, use ORGF
- ORG simply sets the address counter without generating any bytes

#### Related Directives
- [ORGH](#orgh) — Set hub RAM origin
- [ORGF](#orgf) — Set origin with zero-fill
- [FIT](#fit) — Verify code fits within address limit



### ORGF

Set origin with fill—advance to specified address, filling intervening space with zeros. Unlike ORG which simply sets the address counter, ORGF fills the gap between the current address and the target address with zero bytes.

#### Syntax
```pasm
        ORGF    address
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Target address to advance to (cog 0-$1FF or hub address) |

#### Usage
Use ORGF when you need contiguous binary output with guaranteed zero-filled gaps. This ensures data structures start at exact addresses while maintaining a complete memory image. Essential for interrupt vector tables, memory-mapped structures, and fixed-layout binary formats.

#### Example
```pasm
DAT
        ORG     0
entry   jmp     #main
        ' ... some code ...

        ORGF    $100            ' Fill with zeros up to address $100
table   long    1, 2, 3         ' Table starts exactly at $100

        ' Create fixed-size code block
        ORG     0
block_start
        ' ... code ...
        ORGF    block_start + 64   ' Ensure block is exactly 64 longs
block_end
```

#### Notes
- ORGF fills the gap with zero bytes/longs to reach the target address
- Generates assembly error if target address is less than current address
- ORG only changes the address counter without filling
- Useful for creating fixed-layout binary structures
- Essential for interrupt vector tables and memory-mapped structures

#### Related Directives
- [ORG](#org) — Set origin without fill
- [ORGH](#orgh) — Set hub RAM origin
- [FIT](#fit) — Verify code fits
- [RES](#res) — Reserve space without initialization



### ORGH

Set the assembly origin to a hub RAM address. All subsequent code and data assemble for hub execution starting at the specified address.

#### Syntax
```pasm
        ORGH    [address]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Hub RAM address (optional, defaults to $400) |

#### Usage
Use ORGH when switching from cog-exec code to hub-exec code, or when defining data that resides in hub RAM. If no address is specified, ORGH defaults to $400, the standard starting location for hub-exec code.

#### Example
```pasm
        ORGH    $400            ' Start at hub address $400
        ' Hub-exec code here

        ORGH                    ' Default: start at hub $400
```

#### Notes
- ORGH sets hub RAM addresses for hub-exec code and hub data
- Default address is $400 if not specified
- Hub-exec code executes directly from hub RAM without loading into cog
- After ORGH, use ORG to switch back to cog RAM addresses

#### Related Directives
- [ORG](#org) — Set cog RAM origin
- [ORGF](#orgf) — Set origin with fill
- HUBEXEC constant — Hub execution mode flag



## Memory Definition Directives

Memory definition directives allocate and initialize data in memory. Each directive specifies the size of data elements (byte, word, or long) and their initial values.

### BYTE

Declare byte data in memory. Stores 8-bit values at the current address.

#### Syntax
```pasm
[label] BYTE    value[, value...]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 8-bit value or string literal |

#### Usage
Use BYTE to define individual bytes, byte arrays, or strings. Each value occupies exactly 1 byte. Strings are stored as individual bytes in sequence. BYTE provides no automatic alignment—data appears at the current address.

#### Example
```pasm
text    byte    "Hello P2", 0   ' String with null terminator
data    byte    $FF, $00, $55   ' Hex values
nums    byte    1, 2, 3, 4, 5   ' Decimal values
```

#### Notes
- Each value occupies exactly 1 byte
- Strings are stored as individual bytes without alignment
- No automatic alignment—use ALIGNW or ALIGNL if needed
- Values outside 0-255 range will be truncated to 8 bits

#### Related Directives
- [WORD](#word) — Declare 16-bit word data
- [LONG](#long) — Declare 32-bit long data
- [BYTEFIT](#bytefit) — Verify value fits in byte range
- [RES](#res) — Reserve uninitialized space



### LONG

Declare long data in memory. Stores 32-bit values at the current address.

#### Syntax
```pasm
[label] LONG    value[, value...]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 32-bit value, expression, or address reference |

#### Usage
Use LONG to define 32-bit integers, addresses, or any data requiring full 32-bit precision. Each value occupies 4 bytes. In hub RAM, LONG data is automatically long-aligned for optimal access efficiency.

#### Example
```pasm
counter long    0               ' Single long
table   long    $1234_5678      ' Hex value with underscores for readability
ptrs    long    @start, @end    ' Address pointers
```

#### Notes
- Each value occupies 4 bytes
- Automatically long-aligned in hub RAM
- Supports full 32-bit range (0 to $FFFFFFFF)
- Standard size for P2 registers and instructions

#### Related Directives
- [BYTE](#byte) — Declare 8-bit byte data
- [WORD](#word) — Declare 16-bit word data
- [ALIGNL](#alignl) — Force long alignment
- [RES](#res) — Reserve uninitialized longs



### WORD

Declare word data in memory. Stores 16-bit values at the current address.

#### Syntax
```pasm
[label] WORD    value[, value...]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 16-bit value or expression |

#### Usage
Use WORD to define 16-bit integers or data elements. Each value occupies 2 bytes. In hub RAM, WORD data is automatically word-aligned for efficient 16-bit access.

#### Example
```pasm
counts  word    1000, 2000, 3000    ' Decimal values
addr    word    @buffer             ' Address reference (lower 16 bits)
```

#### Notes
- Each value occupies 2 bytes
- Automatically word-aligned in hub RAM
- Range: 0 to 65535 (unsigned)
- Values outside this range will be truncated to 16 bits

#### Related Directives
- [BYTE](#byte) — Declare 8-bit byte data
- [LONG](#long) — Declare 32-bit long data
- [WORDFIT](#wordfit) — Verify value fits in word range
- [ALIGNW](#alignw) — Force word alignment



## Size Verification Directives

Size verification directives provide compile-time checking that values fit within specified bit ranges. These directives generate assembly errors when constraints are violated, catching overflow errors before runtime.

### BYTEFIT

Constrain expression to fit within byte range (0-255). Generates assembly error if expression value exceeds byte range.

#### Syntax
```pasm
        BYTEFIT(expression)
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| expression | Constant expression that must evaluate to 0-255 |

#### Usage
Use BYTEFIT to ensure compile-time verification that values fit in 8 bits. This catches overflow errors during assembly, preventing runtime data corruption. The expression must be resolvable at compile time.

#### Example
```pasm
        byte    BYTEFIT(100)        ' OK: 100 fits in a byte

CON
    SMALL_VAL = BYTEFIT(200)        ' OK: 200 fits in byte range

DAT
        byte    BYTEFIT(256)        ' ERROR: 256 exceeds byte range
```

#### Notes
- Compile-time constraint only—no runtime overhead
- Useful for catching overflow errors during assembly
- Expression must be resolvable at compile time (no runtime values)
- Generates error if value is negative or exceeds 255
- Returns the expression value if constraint is satisfied

#### Related Directives
- [WORDFIT](#wordfit) — Constrain to word range (0-65535)
- [BYTE](#byte) — Declare byte data



### WORDFIT

Constrain expression to fit within word range (0-65535). Generates assembly error if expression value exceeds word range.

#### Syntax
```pasm
        WORDFIT(expression)
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| expression | Constant expression that must evaluate to 0-65535 |

#### Usage
Use WORDFIT to ensure compile-time verification that values fit in 16 bits. This catches overflow errors during assembly before they cause runtime problems. The expression must be resolvable at compile time.

#### Example
```pasm
        word    WORDFIT(1000)       ' OK: 1000 fits in a word

CON
    MED_VAL = WORDFIT(50000)        ' OK: 50000 fits in word range

DAT
        word    WORDFIT(70000)      ' ERROR: 70000 exceeds word range
```

#### Notes
- Compile-time constraint only—no runtime overhead
- Useful for catching overflow errors during assembly
- Expression must be resolvable at compile time (no runtime values)
- Generates error if value is negative or exceeds 65535
- Returns the expression value if constraint is satisfied

#### Related Directives
- [BYTEFIT](#bytefit) — Constrain to byte range (0-255)
- [WORD](#word) — Declare word data



## Alignment Directives

Alignment directives insert padding bytes to align the next data or instruction to specified boundaries. Proper alignment improves memory access efficiency and is required for certain P2 operations.

### ALIGNL

Align to long boundary (4-byte alignment). Inserts zero bytes as needed to align the next data or instruction to a long boundary.

#### Syntax
```pasm
        ALIGNL
```

#### Usage
Use ALIGNL before data declarations or code sections that require long alignment for efficient access or hardware requirements. The P2 requires long alignment for certain operations and achieves optimal performance when accessing long-aligned data in hub RAM.

#### Example
```pasm
        ALIGNL                  ' Align to next long boundary
mydata  long    0               ' This starts on a long-aligned address
```

#### Notes
- Inserts 0-3 bytes of padding as needed to reach next 4-byte boundary
- P2 requires long alignment for certain operations
- Critical for hub memory access efficiency
- No effect if already on a long boundary

#### Related Directives
- [ALIGNW](#alignw) — Align to word boundary
- [LONG](#long) — Declare long data (auto-aligned in hub)
- [ORG](#org) — Set origin address



### ALIGNW

Align to word boundary (2-byte alignment). Inserts zero bytes as needed to align the next data or instruction to a word boundary.

#### Syntax
```pasm
        ALIGNW
```

#### Usage
Use ALIGNW before data declarations that require word alignment for efficient 16-bit access. Proper word alignment improves performance when accessing word-sized data in hub RAM.

#### Example
```pasm
        ALIGNW                  ' Align to next word boundary
myword  word    0               ' This starts on a word-aligned address
```

#### Notes
- Inserts 0-1 bytes of padding as needed to reach next 2-byte boundary
- Important for 16-bit data access efficiency
- No effect if already on a word boundary

#### Related Directives
- [ALIGNL](#alignl) — Align to long boundary
- [WORD](#word) — Declare word data (auto-aligned in hub)
- [ORG](#org) — Set origin address



## Space Management Directives

Space management directives control memory allocation and verify size constraints. These directives either reserve space without initialization or verify that code fits within specified limits.

### DITTO

Repeat the previous instruction. Inserts a copy of the immediately preceding instruction at the current location.

#### Syntax
```pasm
        DITTO
```

#### Usage
Use DITTO to create repeated instruction sequences without copy-paste. Useful for loop unrolling, repeated initialization sequences, and creating multiple instances of the same operation. DITTO was introduced in Spin2/PASM2 version 50 and later.

#### Example
```pasm
        nop                     ' First NOP
        ditto                   ' Second NOP (repeat of previous)
        ditto                   ' Third NOP (repeat of previous)

        wrlong  data, ptra++    ' Write and increment pointer
        ditto                   ' Repeat the wrlong with ptra++
        ditto                   ' And again
        ditto                   ' Four total writes

' Initialize 8 consecutive registers to zero
        mov     reg+0, #0
        ditto                   ' reg+1
        ditto                   ' reg+2
        ditto                   ' reg+3
        ditto                   ' reg+4
        ditto                   ' reg+5
        ditto                   ' reg+6
        ditto                   ' reg+7
```

#### Notes
- Introduced in Spin2/PASM2 version 50 and later
- DITTO copies the exact previous instruction including all operands and effects
- Useful for loop unrolling and repeated initialization sequences
- Must follow a valid instruction—cannot be first in a DAT block
- The repeated instruction appears in listing output for clarity
- Each DITTO generates a full instruction word (same size as original)

#### Related Directives
- REP instruction — Hardware-assisted instruction repeat
- [ORG](#org) — Set origin address



### FIT

Verify that code fits within specified address limit. Generates assembly error if current address exceeds specified limit.

#### Syntax
```pasm
        FIT     [address]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Maximum allowed address (optional, defaults to $200 for cog RAM limit) |

#### Usage
Use FIT to verify that code doesn't exceed available space. This is essential for cog code, which must fit within 512 longs (addresses 0-$1FF). FIT generates an assembly error if the current address exceeds the specified limit, catching size overflow during assembly rather than at runtime.

#### Example
```pasm
' Cog code
        ORG     0
        ' ... code ...
        FIT     $1F0            ' Ensure fits before special regs

        FIT                     ' Default: ensure fits in cog RAM (< $200)
```

#### Notes
- FIT without parameter checks for cog RAM limit ($200 / 512 longs)
- Generates assembly error if limit exceeded
- Essential for cog code size verification
- Special registers occupy cog addresses $1F0-$1FF
- Use FIT $1F0 to ensure code doesn't overwrite special registers

#### Related Directives
- [ORG](#org) — Set origin address
- [RES](#res) — Reserve space
- [ORGF](#orgf) — Fill to address



### RES

Reserve space in cog RAM without initializing. Allocates memory space but doesn't generate any data.

#### Syntax
```pasm
[label] RES     count
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| count | Number of longs to reserve |

#### Usage
Use RES to allocate variables and buffers in cog RAM without initializing them. This advances the address counter by the specified number of longs without generating any bytes in the binary. RES is only valid in cog RAM—hub RAM variables must use LONG with initial values or be allocated at runtime.

#### Example
```pasm
buffer  res     16              ' Reserve 16 longs
temp    res     1               ' Reserve 1 long for temporary storage
```

#### Notes
- RES only reserves space in cog RAM (not hub RAM)
- No hub memory is allocated or affected
- Useful for variables and buffers that will be initialized at runtime
- Advances address counter by count longs without generating binary data
- Use LONG to reserve initialized space in hub RAM

#### Related Directives
- [LONG](#long) — Declare initialized long data
- [ORG](#org) — Set origin address
- [FIT](#fit) — Verify space fits within limit



## Summary

The P2 assembler's 13 directives provide complete control over memory layout and assembly constraints:

**Origin Control**: ORG, ORGH, ORGF set assembly addresses
**Memory Definition**: BYTE, WORD, LONG allocate and initialize data
**Size Verification**: BYTEFIT, WORDFIT catch overflow at compile time
**Alignment**: ALIGNL, ALIGNW optimize memory access
**Space Management**: RES, FIT, DITTO control allocation and verify constraints

These directives execute at assembly time, shaping the binary output without affecting runtime execution. Understanding and using directives effectively is essential for efficient P2 assembly programming.

# Predefined Constants

PASM2 provides a set of predefined constants that the assembler substitutes at compile time. These constants do not generate code themselves but provide standardized values for common operations including boolean logic, numeric bounds, mathematical calculations, and execution mode control.

## Boolean Constants

### TRUE

Logical true constant with all bits set.

#### Value
| Representation | Value |
|----------------|-------|
| Hexadecimal | $FFFFFFFF |
| Decimal | -1 |
| Binary | %11111111_11111111_11111111_11111111 |

#### Description
The TRUE constant represents a boolean true condition with all 32 bits set to 1. In two's complement signed representation, this equals -1. The all-bits-set pattern makes TRUE particularly useful for bitwise masking operations where a true condition must affect all bits.

#### Usage
```pasm
' Using TRUE in conditional logic
                cmp     x, #0       wz      ' Compare x with 0
                mov     result, TRUE        ' Default to TRUE
        if_z    mov     result, FALSE       ' Set to FALSE if x was 0
```

#### Notes
- Standard boolean true value in PASM2
- Compatible with bitwise operations due to all-bits-set pattern
- Commonly used with conditional execution suffixes

#### Related Constants
- [FALSE](#false) — Logical false constant



### FALSE

Logical false constant with all bits cleared.

#### Value
| Representation | Value |
|----------------|-------|
| Hexadecimal | $00000000 |
| Decimal | 0 |
| Binary | %00000000_00000000_00000000_00000000 |

#### Description
The FALSE constant represents a boolean false condition with all 32 bits cleared to 0. This zero value serves as the standard false representation in PASM2 and provides a clean starting state for flag initialization.

#### Usage
```pasm
' Using FALSE for initialization
        mov     flag, FALSE     ' Initialize flag to FALSE
        ' ... some operations ...
        cmp     x, y        wz  ' Compare x and y
        if_e mov  flag, TRUE    ' Set flag to TRUE if equal
```

#### Notes
- Standard boolean false value in PASM2
- Used for clearing flags and initialization
- All bits cleared makes it safe for bitwise operations

#### Related Constants
- [TRUE](#true) — Logical true constant



## Numeric Limit Constants

### NEGX

Most negative value in 32-bit signed integer representation.

#### Value
| Representation | Value |
|----------------|-------|
| Hexadecimal | $80000000 |
| Decimal | -2,147,483,648 |
| Binary | %10000000_00000000_00000000_00000000 |

#### Description
NEGX represents the maximum negative integer value in 32-bit two's complement representation (-2³¹). This constant marks the lower boundary of the signed integer range and serves as a critical reference point for underflow detection and saturation arithmetic.

#### Usage
```pasm
' Checking for negative underflow
                cmps    value, NEGX     wc      ' Check if below min negative
        if_c    jmp     #underflow              ' Jump if underflow

' Using NEGX as lower limit
                mov     limit, NEGX             ' Set limit to max negative
                maxs    value, limit            ' Clamp to not go below NEGX
```

#### Notes
- Represents -2³¹ in decimal notation
- Bit 31 set, bits 30-0 clear
- Used for saturation arithmetic and bounds checking
- Special case: `abs(NEGX) = NEGX` due to two's complement representation (no positive equivalent exists)

#### Related Constants
- [POSX](#posx) — Maximum positive integer constant



### POSX

Most positive value in 32-bit signed integer representation.

#### Value
| Representation | Value |
|----------------|-------|
| Hexadecimal | $7FFFFFFF |
| Decimal | +2,147,483,647 |
| Binary | %01111111_11111111_11111111_11111111 |

#### Description
POSX represents the maximum positive integer value in 32-bit two's complement representation (2³¹ - 1). This constant marks the upper boundary of the signed integer range and serves as a critical reference point for overflow detection and saturation arithmetic.

#### Usage
```pasm
' Checking for positive overflow
                cmp     value, POSX     wc      ' Check if exceeds max positive
        if_nc   jmp     #overflow               ' Jump if overflow

' Using POSX as upper limit
                mov     limit, POSX             ' Set limit to max positive
                mins    value, limit            ' Clamp to not exceed POSX
```

#### Notes
- Represents 2³¹ - 1 in decimal notation
- Bit 31 clear, bits 30-0 set
- Used for saturation arithmetic and bounds checking
- One less than 2³¹ due to zero occupying one value in the range

#### Related Constants
- [NEGX](#negx) — Maximum negative integer constant



## Mathematical Constants

### PI

IEEE 754 single-precision floating-point representation of π.

#### Value
| Representation | Value |
|----------------|-------|
| Hexadecimal | $40490FDB |
| Decimal | 3.141593 |
| Actual Value | ≈ 3.141592653589793 |

#### Description
The PI constant provides the mathematical constant π encoded in IEEE 754 single-precision floating-point format. This encoding allows direct use with the P2's CORDIC operations and floating-point calculations without runtime conversion overhead.

#### Usage
```pasm
' Using PI with CORDIC rotation
        mov     angle, PI           ' Load PI constant
        shr     angle, #1           ' Divide by 2 for PI/2 (90 degrees)
        qrotate angle, radius       ' Rotate by PI/2 radians

' Converting radians to degrees using PI
        mov     x, PI               ' Start with PI
        qmul    x, ##180            ' Multiply PI by 180
        qdiv    x, ##$80000000      ' Divide by 2³¹ for scaling
        getqx   degrees             ' Get degrees conversion factor
```

#### Notes
- IEEE 754 single-precision format provides approximately 7 decimal digits of precision
- Used primarily with CORDIC and floating-point operations
- For CORDIC angular operations, a full circle equals $80000000 (2³¹)
- The constant stores the floating-point encoding, not a fixed-point representation

#### Related Constants
None (unique mathematical constant)



## Execution Mode Constants

### COGEXEC

Execution mode constant for loading code from hub RAM to cog RAM.

#### Value
| Representation | Value |
|----------------|-------|
| Binary | %0_0_0000 |
| Hexadecimal | $00 |

#### Description
COGEXEC specifies cog execution mode for the COGINIT instruction. When used, COGINIT loads 496 longs from hub RAM into cog RAM registers $000-$1F7 and begins execution at cog address $000. This mode provides maximum execution speed since all instructions execute from fast cog RAM.

#### Usage
```pasm
' Start specific cog with code load
        COGINIT #COGEXEC+1, #$100   ' Load and start Cog 1 from Hub RAM $100

' Start Cog 5 with code at label
        COGINIT #COGEXEC+5, @code   ' Load and start Cog 5 from @code
```

#### Syntax
```
COGINIT #COGEXEC+id, #address
```
Where `id` specifies the target cog (0-7) and `address` points to the code in hub RAM.

#### Notes
- Loads cog RAM registers $000-$1F7 (496 longs) from hub RAM
- Begins execution at cog register address $000
- Must specify target cog ID (0-7)
- Fastest execution mode due to cog RAM access speeds
- Code size limited to 496 longs (2KB minus register space)

#### Related Constants
- [HUBEXEC](#hubexec) — Hub execution mode constant
- [COGEXEC_NEW](#cogexec_new) — Auto-select available cog variant
- [COGEXEC_NEW_PAIR](#cogexec_new_pair) — Auto-select adjacent cog pair variant



### HUBEXEC

Execution mode constant for executing code directly from hub RAM.

#### Value
| Representation | Value |
|----------------|-------|
| Binary | %0_1_0000 |
| Hexadecimal | $10 |

#### Description
HUBEXEC specifies hub execution mode for the COGINIT instruction. When used, COGINIT starts the target cog executing instructions directly from hub RAM without loading code to cog RAM. This mode removes code size restrictions at the cost of slower instruction fetch times.

#### Usage
```pasm
' Start specific cog with hub execution
        COGINIT #HUBEXEC+1, #$400   ' Cog 1 from Hub RAM $400

' Start Cog 5 with hub execution at label
        COGINIT #HUBEXEC+5, @code   ' Cog 5 from @code in hub
```

#### Syntax
```
COGINIT #HUBEXEC+id, #address
```
Where `id` specifies the target cog (0-7) and `address` points to the code in hub RAM.

#### Notes
- Executes instructions directly from hub RAM (no cog RAM load required)
- Hub execution allows unlimited code size (not limited to 496 longs)
- Slower than cog execution due to hub RAM access timing and FIFO overhead
- Instruction fetching occurs through FIFO/streamer mechanism
- Must specify target cog ID (0-7)
- Each cog maintains its own program counter for hub execution

#### Related Constants
- [COGEXEC](#cogexec) — Cog execution mode constant
- [HUBEXEC_NEW](#hubexec_new) — Auto-select available cog variant
- [HUBEXEC_NEW_PAIR](#hubexec_new_pair) — Auto-select adjacent cog pair variant



## Execution Mode Variants

The execution mode constants include additional variants for automatic cog selection:

### COGEXEC_NEW
Value: Automatically selects the next available cog for COGEXEC mode. Eliminates the need to manually specify cog ID when any available cog will suffice.

### COGEXEC_NEW_PAIR
Value: Automatically selects an adjacent pair of available cogs for COGEXEC mode. Used when paired cog operations require two adjacent cogs.

### HUBEXEC_NEW
Value: Automatically selects the next available cog for HUBEXEC mode. Eliminates the need to manually specify cog ID when any available cog will suffice.

### HUBEXEC_NEW_PAIR
Value: Automatically selects an adjacent pair of available cogs for HUBEXEC mode. Used when paired cog operations require two adjacent cogs.

These variants simplify cog management by allowing the system to automatically assign available cogs rather than requiring explicit cog ID specification.



## Hardware Configuration Constants

The P2 provides extensive predefined constants for configuring its sophisticated hardware subsystems. These constants are documented in dedicated reference sections:

### SmartPin Constants

The P2's 64 Smart Pins each function as independent hardware peripherals. Over 50 predefined constants configure input selection, filtering, output control, and the 32 operating modes including DAC, ADC, PWM, serial communication, and counters.

**See:** [SmartPin Configuration Constants](smartpin-constants.md)

### Streamer Constants

The Streamer is the P2's DMA-like engine for high-bandwidth data transfer between hub RAM, LUT, pins, and DAC outputs. Over 80 predefined constants configure data sources, destinations, formats, color modes, and control flags.

**See:** [Streamer Configuration Constants](streamer-constants.md)



## Constants Summary

| Category | Count | Purpose |
|----------|-------|---------|
| Boolean | 2 | TRUE, FALSE for logical operations |
| Numeric Limits | 2 | NEGX, POSX for bounds checking |
| Mathematical | 1 | PI for CORDIC and floating-point |
| Execution Mode | 6 | COGEXEC, HUBEXEC and variants |
| SmartPin | 59 | Pin configuration and modes |
| Streamer | 85 | Data streaming and video |
| **Total** | **155** | Core predefined constants |

*Note: Clock configuration constants (RCFAST, RCSLOW, XI, PLL, XDIV*, XMUL*, etc.) add over 1,000 additional symbols for system clock setup.*

# Special Registers

The P2 provides a set of special-purpose registers that enable critical system functions including Hub RAM access, I/O control, interrupt handling, and timing operations. These registers fall into three categories: dual-purpose registers that can also serve as general RAM, fixed special registers with dedicated hardware functions, and non-memory-mapped registers accessed through specific instructions.

## Register Architecture

The P2's special register architecture provides a balance between functionality and flexibility. Each cog has its own independent copy of all special registers, allowing parallel operation without interference. Changes to these registers take effect immediately, enabling precise control over timing-critical operations.

### Memory Map ($1F0-$1FF)

The top 16 locations of cog RAM are reserved for special registers:

| Address | Register | Type | Function |
|---------|----------|------|----------|
| $1F0 | IJMP3 | Dual-purpose | Interrupt 3 call address |
| $1F1 | IRET3 | Dual-purpose | Interrupt 3 return address |
| $1F2 | IJMP2 | Dual-purpose | Interrupt 2 call address |
| $1F3 | IRET2 | Dual-purpose | Interrupt 2 return address |
| $1F4 | IJMP1 | Dual-purpose | Interrupt 1 call address |
| $1F5 | IRET1 | Dual-purpose | Interrupt 1 return address |
| $1F6 | PA | Dual-purpose | Multi-purpose register A |
| $1F7 | PB | Dual-purpose | Multi-purpose register B |
| $1F8 | PTRA | Fixed special | Pointer A to Hub RAM |
| $1F9 | PTRB | Fixed special | Pointer B to Hub RAM |
| $1FA | DIRA | Fixed special | Direction register A (pins 0-31) |
| $1FB | DIRB | Fixed special | Direction register B (pins 32-63) |
| $1FC | OUTA | Fixed special | Output register A (pins 0-31) |
| $1FD | OUTB | Fixed special | Output register B (pins 32-63) |
| $1FE | INA | Fixed special | Input register A (pins 0-31) |
| $1FF | INB | Fixed special | Input register B (pins 32-63) |

### Dual-Purpose vs. Fixed Registers

**Dual-purpose registers** ($1F0-$1F7) can be used as general-purpose cog RAM when their special functions are not enabled. This provides eight additional general-purpose registers for programs that do not use interrupts or the PA/PB facilities.

**Fixed special registers** ($1F8-$1FF) always provide their special functions when accessed. These registers implement hardware behaviors that activate whenever the register is read or written.

## Dual-Purpose Registers

### IJMP3 — Address $1F0

Interrupt 3 call address. Stores the address where execution jumps when interrupt 3 is triggered.

**Access**: Read/Write

**Usage**: When the INT3 event is triggered, the cog saves the current PC in IRET3 and jumps to the address stored in IJMP3. This register can be used as general RAM when interrupt 3 is not enabled.

**Example**:
```pasm
        mov     IJMP3, ##int3_handler   ' Set INT3 handler address
        setint3 #event_ct1              ' Enable INT3 for CT1 event
```

**Related**: [IRET3](#iret3--address-1f1), SETINT3, RETI3



### IRET3 — Address $1F1

Interrupt 3 return address. Stores the return address when interrupt 3 is triggered.

**Access**: Read/Write

**Usage**: When INT3 is triggered, the hardware automatically saves the interrupted PC value to this register. The RETI3 instruction uses this address to return from the interrupt handler. This register can be used as general RAM when interrupt 3 is not enabled.

**Example**:
```pasm
int3_handler
        ' Handle interrupt...
        reti3                           ' Return to saved address in IRET3
```

**Related**: [IJMP3](#ijmp3--address-1f0), SETINT3, RETI3



### IJMP2 — Address $1F2

Interrupt 2 call address. Stores the address where execution jumps when interrupt 2 is triggered.

**Access**: Read/Write

**Usage**: When the INT2 event is triggered, the cog saves the current PC in IRET2 and jumps to the address stored in IJMP2. This register can be used as general RAM when interrupt 2 is not enabled.

**Example**:
```pasm
        mov     IJMP2, ##int2_handler   ' Set INT2 handler address
        setint2 #event_ct2              ' Enable INT2 for CT2 event
```

**Related**: [IRET2](#iret2--address-1f3), SETINT2, RETI2



### IRET2 — Address $1F3

Interrupt 2 return address. Stores the return address when interrupt 2 is triggered.

**Access**: Read/Write

**Usage**: When INT2 is triggered, the hardware automatically saves the interrupted PC value to this register. The RETI2 instruction uses this address to return from the interrupt handler. This register can be used as general RAM when interrupt 2 is not enabled.

**Example**:
```pasm
int2_handler
        ' Handle interrupt...
        reti2                           ' Return to saved address in IRET2
```

**Related**: [IJMP2](#ijmp2--address-1f2), SETINT2, RETI2



### IJMP1 — Address $1F4

Interrupt 1 call address. Stores the address where execution jumps when interrupt 1 is triggered.

**Access**: Read/Write

**Usage**: When the INT1 event is triggered, the cog saves the current PC in IRET1 and jumps to the address stored in IJMP1. This register can be used as general RAM when interrupt 1 is not enabled.

**Example**:
```pasm
        mov     IJMP1, ##int1_handler   ' Set INT1 handler address
        setint1 #event_ct3              ' Enable INT1 for CT3 event
```

**Related**: [IRET1](#iret1--address-1f5), SETINT1, RETI1



### IRET1 — Address $1F5

Interrupt 1 return address. Stores the return address when interrupt 1 is triggered.

**Access**: Read/Write

**Usage**: When INT1 is triggered, the hardware automatically saves the interrupted PC value to this register. The RETI1 instruction uses this address to return from the interrupt handler. This register can be used as general RAM when interrupt 1 is not enabled.

**Example**:
```pasm
int1_handler
        ' Handle interrupt...
        reti1                           ' Return to saved address in IRET1
```

**Related**: [IJMP1](#ijmp1--address-1f4), SETINT1, RETI1



### PA — Address $1F6

Multi-purpose register A. Serves multiple special functions or can be used as general RAM.

**Access**: Read/Write

**Usage**: PA serves three primary special functions:

1. **CALLD immediate return address storage**: When using CALLD with PA as the destination, return information is stored here.
2. **CALLPA parameter passing**: The CALLPA instruction copies a value to PA before calling a routine.
3. **LOC address storage**: The LOC instruction can store an address in PA.

When these functions are not needed, PA can be used as general-purpose cog RAM.

**Example**:
```pasm
        calld   PA, #subroutine         ' Return info in PA, call
        callpa  param, #handler         ' Copy param to PA, call
        loc     PA, #label              ' Store label address in PA

        ' Using PA as general RAM
        mov     PA, #42                 ' Regular register usage
```

**Related**: [PB](#pb--address-1f7), CALLD, CALLPA, LOC



### PB — Address $1F7

Multi-purpose register B. Serves multiple special functions or can be used as general RAM.

**Access**: Read/Write

**Usage**: PB serves three primary special functions:

1. **CALLD immediate return address storage**: When using CALLD with PB as the destination, return information is stored here.
2. **CALLPB parameter passing**: The CALLPB instruction copies a value to PB before calling a routine.
3. **LOC address storage**: The LOC instruction can store an address in PB.

When these functions are not needed, PB can be used as general-purpose cog RAM.

**Example**:
```pasm
        calld   PB, #subroutine         ' Return info in PB, call
        callpb  param, #handler         ' Copy param to PB, call
        loc     PB, #label              ' Store label address in PB

        ' Using PB as general RAM
        mov     PB, ##hub_addr          ' Regular register usage
```

**Related**: [PA](#pa--address-1f6), CALLD, CALLPB, LOC



## Fixed Special Registers

### PTRA — Address $1F8

Pointer A to Hub RAM. Primary pointer register for Hub RAM access with automatic increment/decrement support.

**Access**: Read/Write

**Usage**: PTRA is the primary pointer for Hub RAM operations. It supports indexed addressing modes with automatic pre- and post-increment/decrement, making it ideal for sequential memory access patterns. The pointer is 20 bits wide, addressing the full Hub RAM space.

**Addressing Modes**:
- `PTRA++` — Post-increment by 4 bytes (one long)
- `PTRA--` — Post-decrement by 4 bytes
- `++PTRA` — Pre-increment by 4 bytes
- `--PTRA` — Pre-decrement by 4 bytes
- `PTRA[offset]` — Indexed access (offset in longs)

**Example**:
```pasm
        mov     ptra, ##hub_buffer      ' Set PTRA to Hub address
        rdlong  data, ptra++            ' Read long, post-increment
        wrlong  data, ptra[4]           ' Write long to Hub at PTRA+16 bytes

        ' Block transfer using SETQ
        setq    #15                     ' Transfer 16 longs
        rdlong  cog_buffer, ptra++      ' Read 16 longs, auto-inc
```

**Related**: [PTRB](#ptrb--address-1f9), RDLONG, WRLONG, RDBYTE, RDWORD, SETQ



### PTRB — Address $1F9

Pointer B to Hub RAM. Secondary pointer register for Hub RAM access with automatic increment/decrement support.

**Access**: Read/Write

**Usage**: PTRB is the secondary pointer for Hub RAM operations, providing the same capabilities as PTRA. Having two independent pointers enables efficient dual-buffer operations and complex memory access patterns. COGINIT writes the code start address to the target cog's PTRB, enabling position-independent code.

**Addressing Modes**:
- `PTRB++` — Post-increment by 4 bytes (one long)
- `PTRB--` — Post-decrement by 4 bytes
- `++PTRB` — Pre-increment by 4 bytes
- `--PTRB` — Pre-decrement by 4 bytes
- `PTRB[offset]` — Indexed access (offset in longs)

**Example**:
```pasm
        mov     ptrb, ##hub_source      ' Set PTRB to source address
        rdlong  data, ptrb++            ' Read long, post-increment
        wrlong  data, ptrb[8]           ' Write long to Hub at PTRB+32 bytes

        ' COGINIT sets PTRB in launched cog
        coginit cognumber, ##code_addr  ' PTRB in target cog gets code_addr
```

**Related**: [PTRA](#ptra--address-1f8), RDLONG, WRLONG, COGINIT



### DIRA — Address $1FA

Direction register A for pins 0-31. Controls whether each pin is an input or output.

**Access**: Read/Write

**Bit Field**:
| Bits | Name | Description |
|------|------|-------------|
| 31:0 | DIR | Direction for each pin: 1 = output, 0 = input |

**Usage**: DIRA controls the direction of pins 0-31. Setting a bit to 1 configures the corresponding pin as an output, while 0 configures it as an input. Changes take effect immediately. When a pin is configured as an output, the value in the corresponding OUTA bit is driven onto the pin. When configured as an input, the pin state can be read from INA.

**Example**:
```pasm
        mov     DIRA, ##$00FF_0000      ' Set pins 16-23 as outputs
        or      DIRA, #1                ' Set pin 0 as output
        andn    DIRA, ##$0000_00FF      ' Set pins 0-7 as inputs

        ' Atomic direction change
        mov     DIRA, new_directions    ' Change all 32 directions
```

**Related**: [DIRB](#dirb--address-1fb), [OUTA](#outa--address-1fc), [INA](#ina--address-1fe), DIRC, DIRH, DIRL



### DIRB — Address $1FB

Direction register B for pins 32-63. Controls whether each pin is an input or output.

**Access**: Read/Write

**Bit Field**:
| Bits | Name | Description |
|------|------|-------------|
| 31:0 | DIR | Direction for each pin: 1 = output, 0 = input |

**Usage**: DIRB controls the direction of pins 32-63. Setting a bit to 1 configures the corresponding pin as an output, while 0 configures it as an input. The bit positions map to pins 32-63, where bit 0 controls pin 32 and bit 31 controls pin 63.

**Example**:
```pasm
        mov     DIRB, #0                ' Set all pins 32-63 as inputs
        or      DIRB, ##$8000_0000      ' Set pin 63 as output
        andn    DIRB, ##$0000_FFFF      ' Set pins 32-47 as inputs
```

**Related**: [DIRA](#dira--address-1fa), [OUTB](#outb--address-1fd), [INB](#inb--address-1ff)



### OUTA — Address $1FC

Output register A for pins 0-31. Sets the output state for pins configured as outputs.

**Access**: Read/Write

**Bit Field**:
| Bits | Name | Description |
|------|------|-------------|
| 31:0 | OUT | Output state for each pin: 1 = high, 0 = low |

**Usage**: OUTA sets the output state for pins 0-31. Only affects pins configured as outputs via DIRA. Reading OUTA returns the current output register state, not the actual pin states (use INA to read pin states). When multiple cogs drive the same pin, the outputs are OR'd together—if any cog outputs high, the pin goes high.

**Example**:
```pasm
        mov     OUTA, #0                ' Clear all outputs 0-31
        or      OUTA, #1                ' Set pin 0 high
        xor     OUTA, ##$0000_00FF      ' Toggle pins 0-7
        andn    OUTA, pin_mask          ' Clear specific outputs

        ' Atomic pattern change
        mov     OUTA, new_pattern       ' Change all 32 outputs atomically
```

**Related**: [OUTB](#outb--address-1fd), [DIRA](#dira--address-1fa), [INA](#ina--address-1fe), OUTC, OUTH, OUTL



### OUTB — Address $1FD

Output register B for pins 32-63. Sets the output state for pins configured as outputs.

**Access**: Read/Write

**Bit Field**:
| Bits | Name | Description |
|------|------|-------------|
| 31:0 | OUT | Output state for each pin: 1 = high, 0 = low |

**Usage**: OUTB sets the output state for pins 32-63. Only affects pins configured as outputs via DIRB. The bit positions map to pins 32-63, where bit 0 controls pin 32 and bit 31 controls pin 63. When multiple cogs drive the same pin, the outputs are OR'd together.

**Example**:
```pasm
        mov     OUTB, pattern           ' Set output pattern for pins 32-63
        andn    OUTB, mask              ' Clear specific outputs
        or      OUTB, ##$8000_0000      ' Set pin 63 high
        xor     OUTB, toggle_mask       ' Toggle specific pins
```

**Related**: [OUTA](#outa--address-1fc), [DIRB](#dirb--address-1fb), [INB](#inb--address-1ff)



### INA — Address $1FE

Input register A for pins 0-31. Reads the current state of pins regardless of direction setting.

**Access**: Read-only for pin states (also serves as debug interrupt call address)

**Bit Field**:
| Bits | Name | Description |
|------|------|-------------|
| 31:0 | IN | Current state of each pin: 1 = high, 0 = low |

**Usage**: INA returns the actual electrical state of pins 0-31, regardless of whether they are configured as inputs or outputs. This allows output pins to be read back to verify their state. Reading INA captures the pin states at the moment the instruction executes, providing a consistent snapshot of all 32 pins. INA also serves as the debug interrupt call address when debug interrupts are enabled.

**Example**:
```pasm
                mov     state, INA              ' Read all pins 0-31
                test    INA, #1             wz  ' Test if pin 0 is high
        if_nz   jmp     #pin_high

                and     inputs, INA             ' Mask input pins

                ' Wait for pin high
.wait           test    INA, pin_mask       wz
        if_z    jmp     #.wait
```

**Related**: [INB](#inb--address-1ff), [DIRA](#dira--address-1fa), [OUTA](#outa--address-1fc)



### INB — Address $1FF

Input register B for pins 32-63. Reads the current state of pins regardless of direction setting.

**Access**: Read-only for pin states (also serves as debug interrupt return address)

**Bit Field**:
| Bits | Name | Description |
|------|------|-------------|
| 31:0 | IN | Current state of each pin: 1 = high, 0 = low |

**Usage**: INB returns the actual electrical state of pins 32-63, regardless of whether they are configured as inputs or outputs. The bit positions map to pins 32-63, where bit 0 represents pin 32 and bit 31 represents pin 63. INB also serves as the debug interrupt return address when debug interrupts are enabled.

**Example**:
```pasm
                mov     state, INB              ' Read all pins 32-63
                test    INB, ##$8000_0000   wz  ' Test if pin 63 is high
        if_z    jmp     #pin_low

                ' Copy input pattern to output
                mov     OUTB, INB
```

**Related**: [INA](#ina--address-1fe), [DIRB](#dirb--address-1fb), [OUTB](#outb--address-1fd)



## Non-Memory-Mapped Registers

Several critical registers exist outside the cog RAM address space and are accessed only through specific instructions.

### Program Counter (PC)

The program counter is a 20-bit register that holds the Hub RAM address of the currently executing instruction.

**Access**: Read via GETPC, modified implicitly by jumps and calls

**Range**: $00000-$FFFFF (full Hub address space)

**Usage**: The PC automatically increments by 4 after each instruction execution, pointing to the next long-aligned instruction in Hub RAM. Jump and call instructions modify the PC to change program flow. The PC wraps at the 20-bit boundary when incremented beyond $FFFFF.

**Example**:
```pasm
        getpc   current_addr            ' Read current PC value

        ' PC modified by control flow
        jmp     #target                 ' Sets PC to target address
        call    #subroutine             ' Saves PC+4, jumps to subroutine
```

**Related**: GETPC, JMP, CALL, CALLD



### Q Register

The Q register is a 32-bit auxiliary register used for CORDIC operations, division results, and block transfer setup.

**Access**: Read via GETQX/GETQY, write via SETQ/SETQ2

**Usage**: The Q register serves multiple purposes:

1. **CORDIC results**: After CORDIC operations (QROTATE, QVECTOR, etc.), results are read from Q using GETQX and GETQY.
2. **Division quotient**: Division instructions place the quotient in Q.
3. **Block operations**: SETQ and SETQ2 configure the Q register to enable multi-long transfers with RDxxxx/WRxxxx instructions.

The Q register contents are volatile—CORDIC and division operations overwrite previous values. Read results immediately after the operation completes.

**Example**:
```pasm
        qrotate x, y, angle             ' Perform rotation
        getqx   result_x                ' Get X result from Q
        getqy   result_y                ' Get Y result from Q

        ' Block transfer setup
        setq    #15                     ' Setup for 16-long transfer
        rdlong  buffer, ptra++          ' Read 16 longs using Q count

        ' Division
        qdiv    dividend, divisor       ' Quotient goes to Q
        getqx   quotient                ' Read quotient from Q
        getqy   remainder               ' Read remainder from Q
```

**Related**: GETQX, GETQY, SETQ, SETQ2, QROTATE, QVECTOR, QDIV



### System Counter (CT)

The system counter is a free-running 32-bit counter that increments on every system clock cycle. It is global across all cogs—all cogs reading CT simultaneously receive the same value.

**Access**: Read via GETCT, used by ADDCT1/ADDCT2/ADDCT3 and WAITCT1/WAITCT2/WAITCT3

**Resolution**: System clock cycles (typically 200 MHz = 5ns resolution)

**Usage**: CT provides precise timing for delays, timeouts, and event synchronization. The counter wraps at 32 bits. For precise waits, read the current CT value, add the desired delay to compute a target time, and wait for CT to reach that target. This approach compensates for instruction execution time between reading CT and initiating the wait.

**Example**:
```pasm
                getct   target                  ' Get current time
                addct1  target, ##delay_cycles  ' target = now + delay
                waitct1                         ' Wait for CT to reach it

                ' Timeout pattern
                getct   timeout
                add     timeout, ##max_cycles
.loop           ' ... do work ...
                getct   now
                cmp     now, timeout        wc  ' Check if timeout exceeded
        if_nc   jmp     #timed_out
                jmp     #.loop
```

**Related**: GETCT, ADDCT1, ADDCT2, ADDCT3, WAITCT1, WAITCT2, WAITCT3



### Hardware Random Number Generator (RANDOM)

The hardware random number generator produces true random numbers based on thermal noise, providing a new random value on each read.

**Access**: Read via GETRND

**Features**: True random number generation (not pseudo-random), continuously generates new values

**Usage**: Each execution of GETRND returns a new 32-bit random value. The generator runs continuously in hardware, so consecutive reads produce different values. The randomness quality is suitable for cryptographic applications.

**Example**:
```pasm
        getrnd  random_value            ' Get 32-bit random number

        ' Generate random in range 0-99
        getrnd  temp
        qmul    temp, #100              ' Multiply by 100
        getqy   random_0_99             ' High 32 bits = value*100/2^32

        ' Random bit
        getrnd  temp
        shr     temp, #31               ' Get bit 31 (random 0 or 1)
```

**Related**: GETRND, QMUL (for scaling random values)



### C and Z Flags

The carry (C) and zero (Z) flags are 1-bit condition flags that store the results of tests and arithmetic operations.

**Access**: Set by instructions with WC, WZ, or WCZ effects; tested by conditional instruction execution

**Persistence**: Flags maintain their values until explicitly modified by another instruction with WC/WZ/WCZ

**Usage**: The C and Z flags enable conditional execution and branching. Most ALU instructions can update these flags based on their results. Conditional prefixes (IF_Z, IF_NZ, IF_C, IF_NC, etc.) determine whether an instruction executes based on flag states.

**Flag Setting**:
- **WZ**: Sets Z flag based on result (Z=1 if result is zero)
- **WC**: Sets C flag based on operation (carry out, bit shifted out, etc.)
- **WCZ**: Sets both flags

**Example**:
```pasm
                cmp     value, #100         wz  ' Compare, set Z if equal
        if_z    jmp     #equal

                test    flags, ##$8000_0000 wc  ' Test bit 31, put in C
        if_c    jmp     #bit_set

                add     sum, addend         wc  ' Add, set C if overflow
        if_c    jmp     #overflow

                shr     data, #1            wc  ' Shift right, C = bit out
```

**Related**: All conditional execution (IF_xx), CMP, TEST, and ALU instructions with WC/WZ/WCZ



## Common Usage Patterns

### Pin Control

Toggle a pin:
```pasm
        xor     OUTA, pin_mask          ' Toggle pin atomically
```

Wait for pin high:
```pasm
.wait           test    INA, pin_mask       wz
        if_z    jmp     #.wait
```

Copy inputs to outputs:
```pasm
        mov     OUTA, INA               ' Mirror inputs to outputs
```

Set multiple pins atomically:
```pasm
        mov     OUTA, new_pattern       ' All 32 pins change simultaneously
```



### Hub RAM Access

Block read with pointer:
```pasm
        mov     ptra, ##hub_buffer
        setq    #count-1                ' Transfer 'count' longs
        rdlong  cog_buffer, ptra++      ' Read block, auto-increment PTRA
```

Dual buffer operation:
```pasm
        mov     ptra, ##source_buffer
        mov     ptrb, ##dest_buffer
        setq    #15                     ' Transfer 16 longs
        rdlong  temp, ptra++            ' Read from PTRA
        setq    #15
        wrlong  temp, ptrb++            ' Write to PTRB
```



### Interrupt Setup

Configure interrupt handler:
```pasm
        mov     IJMP1, ##handler_addr   ' Set handler address
        setint1 #event_ct1              ' Enable INT1 for CT1 event

handler_addr
        ' ... handle interrupt ...
        reti1                           ' Return to interrupted code
```



### Timing Operations

Precise delay:
```pasm
        getct   target                  ' Get current time
        addct1  target, ##delay_cycles  ' Add delay
        waitct1                         ' Wait until target time
```

Timeout detection:
```pasm
                getct   deadline
                add     deadline, ##max_time
.loop           ' ... do work ...
                getct   now
                cmp     now, deadline       wc
        if_nc   jmp     #timeout
                ' ... continue if not timed out ...
                jmp     #.loop
```



## Important Behaviors

**Multi-Cog Pin Control**: When multiple cogs drive the same pin as an output, the pin outputs are OR'd together. If any cog outputs high, the pin goes high. This enables cooperative control but requires coordination to avoid conflicts.

**Smart Pin Override**: When a pin is configured for smart pin operation, the smart pin mode overrides the basic DIRA/OUTA/INA functions for that pin. The pin is controlled through smart pin registers and commands rather than the basic I/O registers.

**Immediate Effect**: Changes to DIR and OUT registers take effect immediately—the hardware updates pin states on the same clock cycle as the register write.

**Input Reading**: INA and INB always return actual pin states, regardless of direction settings. This allows outputs to be read back for verification.

**Pointer Auto-Modification**: When using PTRA++ or PTRB++ addressing modes, the pointer update occurs after the memory access completes. The modification affects subsequent operations using that pointer.

**PC Wrap Behavior**: The program counter wraps at the 20-bit boundary ($FFFFF → $00000). Code executing near the top of Hub RAM must account for this wrap behavior.

**Per-Cog Independence**: Each cog has its own independent copy of all special registers. Changes in one cog do not affect other cogs' registers, enabling parallel independent operation.


# Part III: Reference Tables

# Appendix A: Instruction Encoding Master Table

This appendix provides the complete encoding reference for all PASM2 instructions in alphabetical order.

## Reading This Table

| Column | Description |
|--------|-------------|
| Instruction | Mnemonic name |
| Opcode | 7-bit binary pattern (bits 25-31 of instruction word) |
| CZI | Available effects (C=WC, Z=WZ, I=immediate) |
| Cycles | Execution time in clock cycles |
| C Effect | What C flag indicates after instruction execution |
| Z Effect | What Z flag indicates after instruction execution |

**Flag Effect Notation:**

- `---` indicates the flag is not affected by the instruction
- `Result = 0` means the flag is set if the result equals zero
- Specific conditions are described where applicable



## Instruction Encodings

| Instruction | Opcode | CZI | Cycles | C Effect | Z Effect |
|-------------|--------|-----|--------|----------|----------|
| ABS | `0110010` | CZI | 2 | S[31] | Result = 0 |
| ADD | `0001000` | CZI | 2 | carry of (D + S) | Result = 0 |
| ADDCT1 | `1010011` | — | 2 | — | — |
| ADDCT2 | `1010011` | — | 2 | — | — |
| ADDCT3 | `1010011` | — | 2 | — | — |
| ADDPIX | `1010010` | — | 7 | — | — |
| ADDS | `0001010` | CZI | 2 | sign of (D + S) | Result = 0 |
| ADDSX | `0001011` | CZI | 2 | sign of (D+S+C) | Z AND (Result = 0) |
| ADDX | `0001001` | CZI | 2 | carry of (D + S + C) | Z AND (result == 0) |
| AKPIN | `1100000` | — | 2 | — | — |
| ALLOWI | `1101011` | — | 2 | — | — |
| ALTB | `1001100` | — | 2 | — | — |
| ALTD | `1001100` | — | 2 | — | — |
| ALTGB | `1001011` | — | 2 | — | — |
| ALTGN | `1001010` | — | 2 | — | — |
| ALTGW | `1001011` | — | 2 | — | — |
| ALTI | `1001101` | — | 2 | — | — |
| ALTR | `1001100` | — | 2 | — | — |
| ALTS | `1001100` | — | 2 | — | — |
| ALTSB | `1001011` | — | 2 | — | — |
| ALTSN | `1001010` | — | 2 | — | — |
| ALTSW | `1001011` | — | 2 | — | — |
| AND | `0101000` | CZI | 2 | parity of result | Result = 0 |
| ANDN | `0101001` | CZI | 2 | parity of result | Result = 0 |
| ASMCLK | `---` | — | — | — | — |
| AUGD | `1111100` | — | 2 | — | — |
| AUGS | `1111000` | — | 2 | — | — |
| BITC | `0100010` | CZI | 2 | — | original D[S[4:0]] |
| BITH | `0100001` | CZI | 2 | — | original D[S[4:0]] |
| BITL | `0100000` | CZI | 2 | — | original D[S[4:0]] |
| BITNC | `0100011` | CZI | 2 | — | original D[S[4:0]] |
| BITNOT | `0100111` | CZI | 2 | — | original D[S[4:0]] |
| BITNZ | `0100101` | CZI | 2 | — | original D[S[4:0]] |
| BITRND | `0100110` | CZI | 2 | Original D base bit | Original D base bit |
| BITZ | `0100100` | CZI | 2 | — | original D[S[4:0]] |
| BLNPIX | `1010010` | — | 7 | — | — |
| BMASK | `1001110` | — | 2 | — | — |
| BRK | `1101011` | — | 2 | — | — |
| CALL | `1101101` | — | 4 / 13-20 | — | — |
| CALLA | `1101011` | CZ | 5...12 * | D[31] | D[30] |
| CALLB | `1101011` | CZ | 5...12 * | D[31] | D[30] |
| CALLD | `---` | — | 4 / 13-20 | — | — |
| CALLPA | `1011010` | — | 4 / 13–20 | — | — |
| CALLPB | `1011010` | — | 4 / 13–20 | — | — |
| CMP | `0010000` | CZI | 2 | Unsigned (D < S) | D=S |
| CMPM | `0010101` | CZI | 2 | Result[31] | D=S |
| CMPR | `0010100` | CZI | 2 | borrow of (S - D) | (D == S) |
| CMPS | `0010010` | CZI | 2 | Signed (D < S) | D=S |
| CMPSUB | `0010111` | CZI | 2 | Unsigned(D => S) | Result = 0 |
| CMPSX | `0010011` | CZI | 2 | correct sign of (D - (S + C)) | Z AND (D == S + C) |
| CMPX | `0010001` | CZI | 2 | borrow of (D - (S + C)) | Z AND (D == S + C) |
| COGATN | `1101011` | — | 2 | — | — |
| COGBRK | `1101011` | — | 2 | — | — |
| COGID | `1101011` | C | 2–9, +2 if result | Cog Running | — |
| COGINIT | `1100111` | C | 2–9, +2 if result | No cog available | — |
| COGSTOP | `1101011` | — | 2–9 | — | — |
| CRCBIT | `1001110` | — | 2 | — | — |
| CRCNIB | `1001110` | — | 2 | — | — |
| DEBUG | `---` | — | — | — | — |
| DECMOD | `0111001` | CZI | 2 | Modulus triggered | Result = 0 |
| DECOD | `1001110` | — | 2 | — | — |
| DIRC | `1101011` | CZ | 2 | — | DIR bit |
| DIRH | `1101011` | CZ | 2 | — | DIR bit |
| DIRL | `1101011` | CZ | 2 | — | DIR bit |
| DIRNC | `1101011` | CZ | 2 | — | DIR bit |
| DIRNOT | `1101011` | CZ | 2 | — | DIR bit |
| DIRNZ | `1101011` | CZ | 2 | — | DIR bit |
| DIRRND | `1101011` | CZ | 2 | Original DIRx base bit | Original DIRx base bit |
| DIRZ | `1101011` | CZ | 2 | — | DIR bit |
| DJF | `1011011` | — | 2 or 4 | — | — |
| DJNF | `1011011` | — | 2 or 4 | — | — |
| DJNZ | `1011011` | — | 2 or 4 | — | — |
| DJZ | `1011011` | — | 2 or 4 | — | — |
| DRVC | `1101011` | CZ | 2 | — | OUT bit |
| DRVH | `1101011` | CZ | 2 | — | OUT bit |
| DRVL | `1101011` | CZ | 2 | — | OUT bit |
| DRVNC | `1101011` | CZ | 2 | — | OUT bit |
| DRVNOT | `1101011` | CZ | 2 | — | OUT bit |
| DRVNZ | `1101011` | CZ | 2 | — | OUT bit |
| DRVRND | `1101011` | CZ | 2 | Original OUTx base bit | Original OUTx base bit |
| DRVZ | `1101011` | CZ | 2 | — | OUT bit |
| ENCOD | `0111100` | CZI | 2 | S != 0 | Result = 0 |
| EXECF | `1101011` | — | 4 | — | — |
| FBLOCK | `1100100` | — | 2 | — | — |
| FGE | `0011000` | CZI | 2 | limit enforced | Result = 0 |
| FGES | `0011010` | CZI | 2 | limit enforced | Result = 0 |
| FLE | `0011001` | CZI | 2 | limit enforced | Result = 0 |
| FLES | `0011011` | CZI | 2 | limit enforced | Result = 0 |
| FLTC | `1101011` | CZ | 2 | — | OUT bit |
| FLTH | `1101011` | CZ | 2 | — | OUT bit |
| FLTL | `1101011` | CZ | 2 | — | OUT bit |
| FLTNC | `1101011` | CZ | 2 | — | OUT bit |
| FLTNOT | `1101011` | CZ | 2 | — | OUT bit |
| FLTNZ | `1101011` | CZ | 2 | — | OUT bit |
| FLTRND | `1101011` | CZ | 2 | Original OUTx base bit | Original OUTx base bit |
| FLTZ | `1101011` | CZ | 2 | — | OUT bit |
| GETBRK | `1101011` | CZ | 2 | — | — |
| GETBYTE | `1000111` | — | 2 | — | — |
| GETCT | `1101011` | C | 2 | same | — |
| GETNIB | `1000010` | — | 2 | — | — |
| GETPTR | `1101011` | — | 2 | — | — |
| GETQX | `1101011` | CZ | 2...58 | X[31] | Result = 0 |
| GETQY | `1101011` | CZ | 2...58 | Y[31] | Result = 0 |
| GETRND | `1101011` | CZ | 2 | RND[31] | RND[30], unique per cog |
| GETSCP | `1101011` | — | 2 | — | — |
| GETWORD | `1001001` | — | 2 | — | — |
| GETXACC | `1101011` | — | 2 | — | — |
| HUBSET | `1101011` | — | 2...9 | — | — |
| IJNZ | `1011100` | — | 2 or 4 | — | — |
| IJZ | `1011100` | — | 2 or 4 | — | — |
| INCMOD | `0111000` | CZI | 2 | 1, else D = D + 1 and C = 0 | Result = 0 |
| JATN | `1011110` | — | 2 or 4 | — | — |
| JCT1 | `1011110` | — | 2 or 4 | — | — |
| JCT2 | `1011110` | — | 2 or 4 | — | — |
| JCT3 | `1011110` | — | 2 or 4 | — | — |
| JFBW | `1011110` | — | 2 or 4 | — | — |
| JINT | `1011110` | — | 2 or 4 | — | — |
| JMP | `1101011` | CZ | 4 | D[31] | D[30] |
| JMPREL | `1101011` | — | 4 | — | — |
| JNATN | `1011110` | — | 2 or 4 | — | — |
| JNCT1 | `1011110` | — | 2 or 4 | — | — |
| JNCT2 | `1011110` | — | 2 or 4 | — | — |
| JNCT3 | `1011110` | — | 2 or 4 | — | — |
| JNFBW | `1011110` | — | 2 or 4 | — | — |
| JNINT | `1011110` | — | 2 or 4 | — | — |
| JNPAT | `1011110` | — | 2 or 4 | — | — |
| JNQMT | `1011110` | — | 2 or 4 | — | — |
| JNSE1 | `1011110` | — | 2 or 4 | — | — |
| JNSE2 | `1011110` | — | 2 or 4 | — | — |
| JNSE3 | `1011110` | — | 2 or 4 | — | — |
| JNSE4 | `1011110` | — | 2 or 4 | — | — |
| JNXFI | `1011110` | — | 2 or 4 | — | — |
| JNXMT | `1011110` | — | 2 or 4 | — | — |
| JNXRL | `1011110` | — | 2 or 4 | — | — |
| JNXRO | `1011110` | — | 2 or 4 | — | — |
| JPAT | `1011110` | — | 2 or 4 | — | — |
| JQMT | `1011110` | — | 2 or 4 | — | — |
| JSE1 | `1011110` | — | 2 or 4 | — | — |
| JSE2 | `1011110` | — | 2 or 4 | — | — |
| JSE3 | `1011110` | — | 2 or 4 | — | — |
| JSE4 | `1011110` | — | 2 or 4 | — | — |
| JXFI | `1011110` | — | 2 or 4 | — | — |
| JXMT | `1011110` | — | 2 or 4 | — | — |
| JXRL | `1011110` | — | 2 or 4 | — | — |
| JXRO | `1011110` | — | 2 or 4 | — | — |
| LOC | `---` | — | 2 | — | — |
| LOCKNEW | `1101011` | C | 4...11 | 1 if no LOCK available | — |
| LOCKREL | `1101011` | C | 2...9, +2 if result | — | — |
| LOCKRET | `1101011` | — | 2...9 | — | — |
| LOCKTRY | `1101011` | C | 2...9, +2 if result | 1 if got LOCK | — |
| MERGEB | `1101011` | — | 2 | — | — |
| MERGEW | `1101011` | — | 2 | — | — |
| MIXPIX | `1010010` | — | 7 | — | — |
| MODC | `1101011` | — | 2 | cccc[{C,Z}] | — |
| MODCZ | `1101011` | — | 2 | cccc[{C,Z}] | zzzz[{C,Z}] |
| MODZ | `1101011` | — | 2 | — | zzzz[{C,Z}] |
| MOV | `0110000` | CZI | 2 | S[31] | Result = 0 |
| MOVBYTS | `1001111` | — | 2 | — | — |
| MUL | `1010000` | I | 2 | — | (D = 0) | (S = 0) |
| MULPIX | `1010010` | — | 7 | — | — |
| MULS | `1010000` | I | 2 | — | (D = 0) | (S = 0) |
| MUXC | `0101100` | CZI | 2 | parity of result | Result = 0 |
| MUXNC | `0101101` | CZI | 2 | parity of result | Result = 0 |
| MUXNIBS | `1001111` | — | 2 | — | — |
| MUXNITS | `1001111` | — | 2 | — | — |
| MUXNZ | `0101111` | CZI | 2 | parity of result | Result = 0 |
| MUXQ | `1001111` | — | 2 | — | — |
| MUXZ | `0101110` | CZI | 2 | parity of result | Result = 0 |
| NEG | `0110011` | CZI | 2 | Sign of result | Result = 0 |
| NEGC | `0110100` | CZI | 2 | Sign of result | Result = 0 |
| NEGNC | `0110101` | CZI | 2 | Sign of result | Result = 0 |
| NEGNZ | `0110111` | CZI | 2 | Sign of result | Result = 0 |
| NEGZ | `0110110` | CZI | 2 | Sign of result | Result = 0 |
| NIXINT1 | `1101011` | — | 2 | — | — |
| NIXINT2 | `1101011` | — | 2 | — | — |
| NIXINT3 | `1101011` | — | 2 | — | — |
| NOP | `0000000` | — | 2 | — | — |
| NOT | `0110001` | CZI | 2 | !S[31] | Result = 0 |
| ONES | `0111101` | CZI | 2 | Result is odd | Result = 0 |
| OR | `0101010` | CZI | 2 | Parity of Result | Result = 0 |
| OUTC | `1101011` | CZ | 2 | — | OUT bit |
| OUTH | `1101011` | CZ | 2 | — | OUT bit |
| OUTL | `1101011` | CZ | 2 | — | OUT bit |
| OUTNC | `1101011` | CZ | 2 | — | OUT bit |
| OUTNOT | `1101011` | CZ | 2 | — | OUT bit |
| OUTNZ | `1101011` | CZ | 2 | — | OUT bit |
| OUTRND | `1101011` | CZ | 2 | Original OUTx base bit | Original OUTx base bit |
| OUTZ | `1101011` | CZ | 2 | — | OUT bit |
| POLLATN | `1101011` | — | 2 | ATN Event | ATN Event |
| POLLCT1 | `1101011` | — | 2 | CT1 Event | CT1 Event |
| POLLCT2 | `1101011` | — | 2 | CT2 Event | CT2 Event |
| POLLCT3 | `1101011` | — | 2 | CT3 Event | CT3 Event |
| POLLFBW | `1101011` | — | 2 | FBW Event | FBW Event |
| POLLINT | `1101011` | — | 2 | INT Event | INT Event |
| POLLPAT | `1101011` | — | 2 | PAT Event | PAT Event |
| POLLQMT | `1101011` | — | 2 | QMT Event | QMT Event |
| POLLSE1 | `1101011` | — | 2 | SE1 Event | SE1 Event |
| POLLSE2 | `1101011` | — | 2 | SE2 Event | SE2 Event |
| POLLSE3 | `1101011` | — | 2 | SE3 Event | SE3 Event |
| POLLSE4 | `1101011` | — | 2 | SE4 Event | SE4 Event |
| POLLXFI | `1101011` | — | 2 | XFI Event | XFI Event |
| POLLXMT | `1101011` | — | 2 | XMT Event | XMT Event |
| POLLXRL | `1101011` | — | 2 | XRL Event | XRLEvent |
| POLLXRO | `1101011` | — | 2 | XRO Event | XRO Event |
| POP | `1101011` | CZ | 2 | K[31] | Result = 0 |
| POPA | `1011000` | CZ | 9...16 * | MSB of long | Result = 0 |
| POPB | `1011000` | CZ | 9...16 * | MSB of long | Result = 0 |
| PUSH | `1101011` | — | 2 | — | — |
| PUSHA | `1100011` | — | 3...10* | — | — |
| PUSHB | `1100011` | — | 3...10* | — | — |
| QDIV | `1101000` | — | 2...9 | — | — |
| QEXP | `1101011` | — | 2...9 | — | — |
| QFRAC | `1101001` | — | 2...9 | — | — |
| QLOG | `1101011` | — | 2...9 | — | — |
| QMUL | `1101000` | — | 2...9 | — | — |
| QROTATE | `1101010` | — | 2...9 | — | — |
| QSQRT | `1101001` | — | 2...9 | — | — |
| QVECTOR | `1101010` | — | 2...9 | — | — |
| RCL | `0000101` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 |
| RCR | `0000100` | CZI | 2 | Last bit out1 | Result = 0 |
| RCZL | `1101011` | CZ | 2 | D[31] | D[30] |
| RCZR | `1101011` | CZ | 2 | D[1] | D[0] |
| RDBYTE | `1010110` | CZI | 9...16 | MSB of byte | Result = 0 |
| RDFAST | `1100011` | — | 2 or WRFAST finish + 10...17 | — | — |
| RDLONG | `1011000` | CZI | 9...16 * | MSB of long | — |
| RDLUT | `1010101` | CZI | 3 | MSB of data | Result = 0 |
| RDPIN | `1010100` | C | 2 | modal result | — |
| RDWORD | `1010111` | CZI | 9...16 * | MSB of word | Result = 0 |
| REP | `1100110` | — | 2 | — | — |
| RESI0 | `1011001` | — | 4 | — | — |
| RESI1 | `1011001` | — | 4 | — | — |
| RESI2 | `1011001` | — | 4 | — | — |
| RESI3 | `1011001` | — | 4 | — | — |
| RET | `1101011` | — | 4 | K[31] | K[30] |
| RETA | `1101011` | — | 11...18 * | L[31] | L[30] |
| RETB | `1101011` | — | 11...18 * | L[31] | L[30] |
| RETI0 | `1011001` | — | 4 | — | — |
| RETI1 | `1011001` | — | 4 | — | — |
| RETI2 | `1011001` | — | 4 | — | — |
| RETI3 | `1011001` | — | 4 | — | — |
| REV | `1101011` | — | 2 | — | — |
| RFBYTE | `1101011` | CZ | 2 | MSB of byte | Result = 0 |
| RFLONG | `1101011` | CZ | 2 | MSB of long | Result = 0 |
| RFVAR | `1101011` | CZ | 2 | 0 | Result = 0 |
| RFVARS | `1101011` | CZ | 2 | MSB of value | Result = 0 |
| RFWORD | `1101011` | CZ | 2 | MSB of word | Result = 0 |
| RGBEXP | `1101011` | — | 2 | — | — |
| RGBSQZ | `1101011` | — | 2 | — | — |
| ROL | `0000001` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 |
| ROLBYTE | `1001000` | — | 2 | — | — |
| ROLNIB | `1000100` | — | 2 | — | — |
| ROLWORD | `1001010` | — | 2 | — | — |
| ROR | `0000000` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[0] | Result = 0 |
| RQPIN | `1010100` | C | 2 | modal result | — |
| SAL | `0000111` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 |
| SAR | `0000110` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[0] | Result = 0 |
| SCA | `1010001` | I | 2 | — | Product = 0 |
| SCAS | `1010001` | I | 2 | — | Result = 0 |
| SETBYTE | `1000110` | — | 2 | — | — |
| SETCFRQ | `1101011` | — | 2 | — | — |
| SETCI | `1101011` | — | 2 | — | — |
| SETCMOD | `1101011` | — | 2 | — | — |
| SETCQ | `1101011` | — | 2 | — | — |
| SETCY | `1101011` | — | 2 | — | — |
| SETD | `1001101` | — | 2 | — | — |
| SETDACS | `1101011` | — | 2 | — | — |
| SETINT1 | `1101011` | — | 2 | — | — |
| SETINT2 | `1101011` | — | 2 | — | — |
| SETINT3 | `1101011` | — | 2 | — | — |
| SETLUTS | `1101011` | — | 2 | — | — |
| SETNIB | `1000000` | — | 2 | — | — |
| SETPAT | `1011111` | — | 2 | — | — |
| SETPIV | `1101011` | — | 2 | — | — |
| SETPIX | `1101011` | — | 2 | — | — |
| SETQ | `1101011` | — | 2 | — | — |
| SETQ2 | `1101011` | — | 2 | — | — |
| SETR | `1001101` | — | 2 | — | — |
| SETS | `1001101` | — | 2 | — | — |
| SETSCP | `1101011` | — | 2 | — | — |
| SETSE1 | `1101011` | — | 2 | — | — |
| SETSE2 | `1101011` | — | 2 | — | — |
| SETSE3 | `1101011` | — | 2 | — | — |
| SETSE4 | `1101011` | — | 2 | — | — |
| SETWORD | `1001001` | — | 2 | — | — |
| SETXFRQ | `1101011` | — | 2 | — | — |
| SEUSSF | `1101011` | — | 2 | — | — |
| SEUSSR | `1101011` | — | 2 | — | — |
| SHL | `0000011` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 |
| SHR | `0000010` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[0] | Result = 0 |
| SIGNX | `0111011` | CZI | 2 | MSB of result | Result = 0 |
| SKIP | `1101011` | — | 2 | — | — |
| SKIPF | `1101011` | — | 2 | — | — |
| SPLITB | `1101011` | — | 2 | — | — |
| SPLITW | `1101011` | — | 2 | — | — |
| STALLI | `1101011` | — | 2 | — | — |
| SUB | `0001100` | CZI | 2 | borrow of (D - S) | Result = 0 |
| SUBR | `0010110` | CZI | 2 | borrow of (S - D) | Result = 0 |
| SUBS | `0001110` | CZI | 2 | sign of (D - S) | Result = 0 |
| SUBSX | `0001111` | CZI | 2 | sign of D-(S+C) | Z AND (Result = 0) |
| SUBX | `0001101` | CZI | 2 | borrow of (D - (S + C)) | Z AND (result == 0) |
| SUMC | `0011100` | CZI | 2 | 1 then D = D - S, else D = D + S. C = correct sign of (D +/- S) | Result = 0 |
| SUMNC | `0011101` | CZI | 2 | 0 then D = D - S, else D = D + S. C = correct sign of (D +/- S) | Result = 0 |
| SUMNZ | `0011111` | CZI | 2 | correct sign of (D +/- S) | 0 then D = D - S, else D = D + S |
| SUMZ | `0011110` | CZI | 2 | correct sign of (D +/- S) | 1 then D = D - S, else D = D + S |
| TEST | `0111110` | CZ | 2 | Parity of D | D = 0 |
| TESTB | `0100000` | CZI | 2 | D[S[4:0]] | D[S[4:0]] |
| TESTBN | `0100001` | CZI | 2 | !D[S[4:0]] | !D[S[4:0]] |
| TESTN | `0111111` | CZI | 2 | Parity of (D & !S) | (D & !S) = 0 |
| TESTP | `1101011` | CZ | 2 | IN[D[5:0]] | IN[D[5:0]] |
| TESTPN | `1101011` | CZ | 2 | !IN[D[5:0]] | !IN[D[5:0]] |
| TJF | `1011101` | — | 2 or 4 | — | — |
| TJNF | `1011101` | — | 2 or 4 / 2 or 13-20 | — | — |
| TJNS | `1011101` | — | 2 or 4 | — | — |
| TJNZ | `1011100` | — | 2 or 4 | — | — |
| TJS | `1011101` | — | 2 or 4 / 2 or 13-20 | — | — |
| TJV | `1011110` | — | 2 or 4 / 2 or 13–20 | — | — |
| TJZ | `1011100` | — | 2 or 4 | — | — |
| TRGINT1 | `1101011` | — | 2 | — | — |
| TRGINT2 | `1101011` | — | 2 | — | — |
| TRGINT3 | `1101011` | — | 2 | — | — |
| WAITATN | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITCT1 | `1101011` | — | 2+ | timeout | timeout |
| WAITCT2 | `1101011` | — | 2+ | timeout | timeout |
| WAITCT3 | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITFBW | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITINT | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITPAT | `1101011` | — | 2+ | timeout | timeout |
| WAITSE1 | `1101011` | — | 2+ | timeout | timeout |
| WAITSE2 | `1101011` | — | 2+ | timeout | timeout |
| WAITSE3 | `1101011` | — | 2+ | timeout | timeout |
| WAITSE4 | `1101011` | — | 2+ | timeout | timeout |
| WAITX | `1101011` | CZ | 2 + D | 0 | 0 |
| WAITXFI | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITXMT | `1101011` | — | 2+ | timeout | timeout |
| WAITXRL | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITXRO | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WFBYTE | `1101011` | — | 2 | — | — |
| WFLONG | `1101011` | — | 2 | — | — |
| WFWORD | `1101011` | — | 2 | — | — |
| WMLONG | `1010011` | — | 3...10 * | — | — |
| WRBYTE | `1100010` | — | 3...10 | — | — |
| WRC | `1101011` | — | 2 | — | — |
| WRFAST | `1100100` | — | 2 or WRFAST finish + 3 | — | — |
| WRLONG | `1100011` | — | 3...10* | — | — |
| WRLUT | `1100001` | — | 2 | — | — |
| WRNC | `1101011` | — | 2 | — | — |
| WRNZ | `1101011` | — | 2 | — | — |
| WRPIN | `1100000` | — | 2 | — | — |
| WRWORD | `1100010` | — | 3...10* | — | — |
| WRZ | `1101011` | — | 2 | — | — |
| WXPIN | `1100000` | — | 2 | — | — |
| WYPIN | `1100001` | — | 2 | — | — |
| XCONT | `1100110` | — | 2+ | — | — |
| XINIT | `1100101` | — | 2 | — | — |
| XOR | `0101011` | CZI | 2 | Parity of Result | Result = 0 |
| XORO32 | `1101011` | — | 2 | — | — |
| XSTOP | `1100101` | — | 2 | — | — |
| XZERO | `1100101` | — | 2+ | — | — |
| ZEROX | `0111010` | CZI | 2 | MSB of result | Result = 0 |

**Total Instructions:** 359



**Notes:**

- This table shows the primary encoding for each instruction
- Instructions with multiple encoding forms show only the most common variant
- Multi-cycle instructions show ranges (e.g., `2...9`) where timing depends on:
  - Hub synchronization (variable wait for hub access)
  - Operation parameters (CORDIC solver iterations, streamer operations)
  - Memory location (cog vs. LUT vs. hub execution)
- The `*` symbol indicates hub memory access with variable timing
- See Part II (Instruction Reference) for complete encoding details and all variants
- Special instructions (ASMCLK, DEBUG) are compiler directives, not executable instructions

# Appendix B: Categorical Instruction Index

This appendix organizes P2 instructions by functional category, helping you find instructions based on what you want to accomplish rather than by alphabetical order.

Each instruction name links to its detailed reference in Part II.


## Arithmetic Operations

| Instruction | Description |
|-------------|-------------|
| [ABS](#abs) | Get absolute value of D into D |
| [ADD](#add) | Add S into D |
| [ADDS](#adds) | Add S into D, signed |
| [ADDSX](#addsx) | Add (S + C) into D, signed and extended |
| [ADDX](#addx) | Add (S + C) into D, extended |
| [AND](#and) | AND S into D |
| [ANDN](#andn) | AND !S into D |
| [BITC](#bitc) | Bits D[S[9:5]+S[4:0]:S[4:0]] = C |
| [BITH](#bith) | Bits D[S[9:5]+S[4:0]:S[4:0]] = 1 |
| [BITL](#bitl) | Bits D[S[9:5]+S[4:0]:S[4:0]] = 0 |
| [BITNC](#bitnc) | Bits D[S[9:5]+S[4:0]:S[4:0]] = !C |
| [BITNOT](#bitnot) | Toggle bits D[S[9:5]+S[4:0]:S[4:0]] |
| [BITNZ](#bitnz) | Bits D[S[9:5]+S[4:0]:S[4:0]] = !Z |
| [BITRND](#bitrnd) | Bits D[S[9:5]+S[4:0]:S[4:0]] = RNDs |
| [BITZ](#bitz) | Bits D[S[9:5]+S[4:0]:S[4:0]] = Z |
| [BMASK](#bmask) | Get LSB-justified bit mask of size (D[4:0] + 1) into D |
| [CMP](#cmp) | Compare D to S |
| [CMPM](#cmpm) | Compare D to S, get MSB of difference into C |
| [CMPR](#cmpr) | Compare S to D (reverse) |
| [CMPS](#cmps) | Compare D to S, signed |
| [CMPSUB](#cmpsub) | Compare and subtract S from D if D >= S |
| [CMPSX](#cmpsx) | Compare D to (S + C), signed and extended |
| [CMPX](#cmpx) | Compare D to (S + C), extended |
| [CRCBIT](#crcbit) | Iterate CRC value in D using C and polynomial in S |
| [CRCNIB](#crcnib) | Iterate CRC value in D using Q[31:28] and polynomial in S |
| [DECMOD](#decmod) | Decrement with modulus |
| [DECOD](#decod) | Decode D[4:0] into D |
| [ENCOD](#encod) | Get bit position of top-most '1' in D into D |
| [FGE](#fge) | Force D >= S |
| [FGES](#fges) | Force D >= S, signed |
| [FLE](#fle) | Force D <= S |
| [FLES](#fles) | Force D <= S, signed |
| [GETBYTE](#getbyte) | Get byte established by prior ALTGB instruction into D. |
| [GETNIB](#getnib) | Get nibble established by prior ALTGN instruction into D. |
| [GETWORD](#getword) | Get word established by prior ALTGW instruction into D. |
| [INCMOD](#incmod) | Increment with modulus |
| [LOC](#loc) | Get {12'b0, address[19:0]} into PA/PB/PTRA/PTRB (per W) |
| [MERGEB](#mergeb) | Merge bits of bytes in D |
| [MERGEW](#mergew) | Merge bits of words in D |
| [MODC](#modc) | Modify C according to cccc |
| [MODCZ](#modcz) | Modify C and Z according to cccc and zzzz |
| [MODZ](#modz) | Modify Z according to zzzz |
| [MOV](#mov) | Move S into D |
| [MOVBYTS](#movbyts) | Move bytes within D, per S |
| [MUL](#mul) | D = unsigned (D[15:0] * S[15:0]) |
| [MULS](#muls) | D = signed (D[15:0] * S[15:0]) |
| [MUXC](#muxc) | Mux C into each D bit that is '1' in S |
| [MUXNC](#muxnc) | Mux !C into each D bit that is '1' in S |
| [MUXNIBS](#muxnibs) | For each non-zero nibble in S, copy that nibble into the corresponding D nibble, else leave that D nibble the same. |
| [MUXNITS](#muxnits) | For each non-zero bit pair in S, copy that bit pair into the corresponding D bits, else leave that D bit pair the same. |
| [MUXNZ](#muxnz) | Mux !Z into each D bit that is '1' in S |
| [MUXQ](#muxq) | Used after SETQ |
| [MUXZ](#muxz) | Mux Z into each D bit that is '1' in S |
| [NEG](#neg) | Negate D |
| [NEGC](#negc) | Negate D by C |
| [NEGNC](#negnc) | Negate D by !C |
| [NEGNZ](#negnz) | Negate D by !Z |
| [NEGZ](#negz) | Negate D by Z |
| [NOT](#not) | Get !D into D |
| [ONES](#ones) | Get number of '1's in D into D |
| [OR](#or) | OR S into D |
| [RCL](#rcl) | Rotate carry left |
| [RCR](#rcr) | Rotate carry right |
| [RCZL](#rczl) | Rotate C,Z left through D |
| [RCZR](#rczr) | Rotate C,Z right through D |
| [REV](#rev) | Reverse D bits |
| [RGBEXP](#rgbexp) | Expand 5:6:5 RGB value in D[15:0] into 8:8:8 value in D[31:8] |
| [RGBSQZ](#rgbsqz) | Squeeze 8:8:8 RGB value in D[31:8] into 5:6:5 value in D[15:0] |
| [ROL](#rol) | Rotate left |
| [ROLBYTE](#rolbyte) | Rotate-left byte established by prior ALTGB instruction into D. |
| [ROLNIB](#rolnib) | Rotate-left nibble established by prior ALTGN instruction into D. |
| [ROLWORD](#rolword) | Rotate-left word established by prior ALTGW instruction into D. |
| [ROR](#ror) | Rotate right |
| [SAL](#sal) | Shift arithmetic left |
| [SAR](#sar) | Shift arithmetic right |
| [SCA](#sca) | Next instruction's S value = unsigned (D[15:0] * S[15:0]) >> 16 |
| [SCAS](#scas) | Next instruction's S value = signed (D[15:0] * S[15:0]) >> 14 |
| [SETBYTE](#setbyte) | Set S[7:0] into byte established by prior ALTSB instruction. |
| [SETD](#setd) | Set D field of D to S[8:0] |
| [SETNIB](#setnib) | Set S[3:0] into nibble established by prior ALTSN instruction. |
| [SETR](#setr) | Set R field of D to S[8:0] |
| [SETS](#sets) | Set S field of D to S[8:0] |
| [SETWORD](#setword) | Set S[15:0] into word established by prior ALTSW instruction. |
| [SEUSSF](#seussf) | Relocate and periodically invert bits within D |
| [SEUSSR](#seussr) | Relocate and periodically invert bits within D |
| [SHL](#shl) | Shift left |
| [SHR](#shr) | Shift right |
| [SIGNX](#signx) | Sign-extend D from bit S[4:0] |
| [SPLITB](#splitb) | Split every 4th bit of D into bytes |
| [SPLITW](#splitw) | Split odd/even bits of D into words |
| [SUB](#sub) | Subtract S from D |
| [SUBR](#subr) | Subtract D from S (reverse) |
| [SUBS](#subs) | Subtract S from D, signed |
| [SUBSX](#subsx) | Subtract (S + C) from D, signed and extended |
| [SUBX](#subx) | Subtract (S + C) from D, extended |
| [SUMC](#sumc) | Sum +/-S into D by C |
| [SUMNC](#sumnc) | Sum +/-S into D by !C |
| [SUMNZ](#sumnz) | Sum +/-S into D by !Z |
| [SUMZ](#sumz) | Sum +/-S into D by Z |
| [TEST](#test) | Test D |
| [TESTB](#testb) | Test bit S[4:0] of D, XOR into C/Z |
| [TESTBN](#testbn) | Test bit S[4:0] of !D, XOR into C/Z |
| [TESTN](#testn) | Test D with !S |
| [WRC](#wrc) | Write 0 or 1 to D, according to C |
| [WRNC](#wrnc) | Write 0 or 1 to D, according to !C |
| [WRNZ](#wrnz) | Write 0 or 1 to D, according to !Z |
| [WRZ](#wrz) | Write 0 or 1 to D, according to Z |
| [XOR](#xor) | XOR S into D |
| [XORO32](#xoro32) | Iterate D with xoroshiro32+ PRNG algorithm and put PRNG result into next instruction's S. |
| [ZEROX](#zerox) | Zero-extend D above bit S[4:0] |


## Branching and Flow Control


### Branch A - Jump

| Instruction | Description |
|-------------|-------------|
| [JMP](#jmp) | Jump to A |


### Branch A - Call

| Instruction | Description |
|-------------|-------------|
| [CALL](#call) | Call to A by pushing {C, Z, 10'b0, PC[19:0]} onto stack |
| [CALLA](#calla) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRA++ |
| [CALLB](#callb) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRB++ |
| [CALLD](#calld) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to PA/PB/PTRA/PTRB (per W) |


### Branch D - Jump

| Instruction | Description |
|-------------|-------------|
| [JMPREL](#jmprel) | Jump ahead/back by D instructions |


### Branch D - Jump+Skip

| Instruction | Description |
|-------------|-------------|
| [SKIPF](#skipf) | Skip cog/LUT instructions fast per D |


### Branch D - Call+Skip

| Instruction | Description |
|-------------|-------------|
| [EXECF](#execf) | Jump to D[9:0] in cog/LUT and set SKIPF pattern to D[31:10] |


### Branch D - Skip

| Instruction | Description |
|-------------|-------------|
| [SKIP](#skip) | Skip instructions per D |


### Branch S - Call

| Instruction | Description |
|-------------|-------------|
| [CALLPA](#callpa) | Call to S** by pushing {C, Z, 10'b0, PC[19:0]} onto stack, copy D to PA. |
| [CALLPB](#callpb) | Call to S** by pushing {C, Z, 10'b0, PC[19:0]} onto stack, copy D to PB. |


### Branch S - Test

| Instruction | Description |
|-------------|-------------|
| [TJF](#tjf) | Test D and jump to S** if D is full (D = $FFFF_FFFF). |
| [TJNF](#tjnf) | Test D and jump to S** if D is not full (D != $FFFF_FFFF). |
| [TJNS](#tjns) | Test D and jump to S** if D is not signed (D[31] = 0). |
| [TJNZ](#tjnz) | Test D and jump to S** if D is not zero. |
| [TJS](#tjs) | Test D and jump to S** if D is signed (D[31] = 1). |
| [TJV](#tjv) | Test D and jump to S** if D overflowed (D[31] != C, C = 'correct sign' from last addition/subtraction). |
| [TJZ](#tjz) | Test D and jump to S** if D is zero. |


### Branch S - Mod & Test

| Instruction | Description |
|-------------|-------------|
| [DJF](#djf) | Decrement D and jump to S** if result is $FFFF_FFFF. |
| [DJNF](#djnf) | Decrement D and jump to S** if result is not $FFFF_FFFF. |
| [DJNZ](#djnz) | Decrement D and jump to S** if result is not zero. |
| [DJZ](#djz) | Decrement D and jump to S** if result is zero. |
| [IJNZ](#ijnz) | Increment D and jump to S** if result is not zero. |
| [IJZ](#ijz) | Increment D and jump to S** if result is zero. |


### Branch Return

| Instruction | Description |
|-------------|-------------|
| [RET](#ret) | Return by popping stack (K) |
| [RETA](#reta) | Return by reading hub long (L) at --PTRA |
| [RETB](#retb) | Return by reading hub long (L) at --PTRB |


### Branch S - Return

| Instruction | Description |
|-------------|-------------|
| [RETI0](#reti0) | Return from INT0 |
| [RETI1](#reti1) | Return from INT1 |
| [RETI2](#reti2) | Return from INT2 |
| [RETI3](#reti3) | Return from INT3 |


### Branch S - Resume

| Instruction | Description |
|-------------|-------------|
| [RESI0](#resi0) | Resume from INT0 |
| [RESI1](#resi1) | Resume from INT1 |
| [RESI2](#resi2) | Resume from INT2 |
| [RESI3](#resi3) | Resume from INT3 |


### Branch Repeat

| Instruction | Description |
|-------------|-------------|
| [REP](#rep) | Execute next D[8:0] instructions S times |


## Hub Memory Access


### Hub RAM - Read

| Instruction | Description |
|-------------|-------------|
| [POPA](#popa) | Read long from hub address --PTRA into D |
| [POPB](#popb) | Read long from hub address --PTRB into D |
| [RDBYTE](#rdbyte) | Read zero-extended byte from hub address {#}S/PTRx into D |
| [RDLONG](#rdlong) | Read long from hub address {#}S/PTRx into D |
| [RDWORD](#rdword) | Read zero-extended word from hub address {#}S/PTRx into D |


### Hub RAM - Write

| Instruction | Description |
|-------------|-------------|
| [PUSHA](#pusha) | Write long in D[31:0] to hub address PTRA++. |
| [PUSHB](#pushb) | Write long in D[31:0] to hub address PTRB++. |
| [WMLONG](#wmlong) | Write only non-$00 bytes in D[31:0] to hub address {#}S/PTRx |
| [WRBYTE](#wrbyte) | Write byte in D[7:0] to hub address {#}S/PTRx. |
| [WRLONG](#wrlong) | Write long in D[31:0] to hub address {#}S/PTRx |
| [WRWORD](#wrword) | Write word in D[15:0] to hub address {#}S/PTRx. |


### Hub FIFO

| Instruction | Description |
|-------------|-------------|
| [GETPTR](#getptr) | Get current FIFO hub pointer into D. |


### Hub FIFO - New Read

| Instruction | Description |
|-------------|-------------|
| [RDFAST](#rdfast) | Begin new fast hub read via FIFO |


### Hub FIFO - New Write

| Instruction | Description |
|-------------|-------------|
| [WRFAST](#wrfast) | Begin new fast hub write via FIFO |


### Hub FIFO - New Block

| Instruction | Description |
|-------------|-------------|
| [FBLOCK](#fblock) | Set next block for when block wraps |


### Hub FIFO - Read

| Instruction | Description |
|-------------|-------------|
| [RFBYTE](#rfbyte) | Used after RDFAST |
| [RFLONG](#rflong) | Used after RDFAST |
| [RFVAR](#rfvar) | Used after RDFAST |
| [RFVARS](#rfvars) | Used after RDFAST |
| [RFWORD](#rfword) | Used after RDFAST |


### Hub FIFO - Write

| Instruction | Description |
|-------------|-------------|
| [WFBYTE](#wfbyte) | Used after WRFAST |
| [WFLONG](#wflong) | Used after WRFAST |
| [WFWORD](#wfword) | Used after WRFAST |


## Lookup Table

| Instruction | Description |
|-------------|-------------|
| [RDLUT](#rdlut) | Read data from LUT address {#}S/PTRx into D |
| [SETLUTS](#setluts) | If D[0] = 1 then enable LUT sharing, where LUT writes within the adjacent odd/even companion cog are copied to this cog's LUT. |
| [WRLUT](#wrlut) | Write D to LUT address {#}S/PTRx. |


## Pin I/O and Smart Pins


### Pins

| Instruction | Description |
|-------------|-------------|
| [DIRC](#dirc) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = C |
| [DIRH](#dirh) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = 1 |
| [DIRL](#dirl) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = 0 |
| [DIRNC](#dirnc) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = !C |
| [DIRNOT](#dirnot) | Toggle DIR bits of pins D[10:6]+D[5:0]..D[5:0] |
| [DIRNZ](#dirnz) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = !Z |
| [DIRRND](#dirrnd) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs |
| [DIRZ](#dirz) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = Z |
| [DRVC](#drvc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C |
| [DRVH](#drvh) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1 |
| [DRVL](#drvl) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0 |
| [DRVNC](#drvnc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C |
| [DRVNOT](#drvnot) | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0] |
| [DRVNZ](#drvnz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z |
| [DRVRND](#drvrnd) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs |
| [DRVZ](#drvz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z |
| [FLTC](#fltc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C |
| [FLTH](#flth) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1 |
| [FLTL](#fltl) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0 |
| [FLTNC](#fltnc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C |
| [FLTNOT](#fltnot) | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0] |
| [FLTNZ](#fltnz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z |
| [FLTRND](#fltrnd) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs |
| [FLTZ](#fltz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z |
| [OUTC](#outc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C |
| [OUTH](#outh) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1 |
| [OUTL](#outl) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0 |
| [OUTNC](#outnc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C |
| [OUTNOT](#outnot) | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0] |
| [OUTNZ](#outnz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z |
| [OUTRND](#outrnd) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs |
| [OUTZ](#outz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z |
| [TESTP](#testp) | Test IN bit of pin D[5:0], XOR into C/Z |
| [TESTPN](#testpn) | Test !IN bit of pin D[5:0], XOR into C/Z |


### Smart Pins

| Instruction | Description |
|-------------|-------------|
| [AKPIN](#akpin) | Acknowledge smart pins S[10:6]+S[5:0]..S[5:0] |
| [GETSCP](#getscp) | Get four-channel oscilloscope samples into D |
| [RDPIN](#rdpin) | Read smart pin S[5:0] result "Z" into D, acknowledge smart pin |
| [RQPIN](#rqpin) | Read smart pin S[5:0] result "Z" into D, don't acknowledge smart pin ("Q" in RQPIN means "quiet") |
| [SETDACS](#setdacs) | DAC3 = D[31:24], DAC2 = D[23:16], DAC1 = D[15:8], DAC0 = D[7:0]. |
| [SETSCP](#setscp) | Set four-channel oscilloscope enable to D[6] and set input pin base to D[5:2]. |
| [WRPIN](#wrpin) | Set mode of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins |
| [WXPIN](#wxpin) | Set "X" of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins |
| [WYPIN](#wypin) | Set "Y" of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins |


## Events and Timing


### Events - Configuration

| Instruction | Description |
|-------------|-------------|
| [ADDCT1](#addct1) | Set CT1 event to trigger on CT = D + S |
| [ADDCT2](#addct2) | Set CT2 event to trigger on CT = D + S |
| [ADDCT3](#addct3) | Set CT3 event to trigger on CT = D + S |
| [SETPAT](#setpat) | Set pin pattern for PAT event |
| [SETSE1](#setse1) | Set SE1 event configuration to D[8:0]. |
| [SETSE2](#setse2) | Set SE2 event configuration to D[8:0]. |
| [SETSE3](#setse3) | Set SE3 event configuration to D[8:0]. |
| [SETSE4](#setse4) | Set SE4 event configuration to D[8:0]. |


### Events - Poll

| Instruction | Description |
|-------------|-------------|
| [POLLATN](#pollatn) | Get ATN event flag into C/Z, then clear it. |
| [POLLCT1](#pollct1) | Get CT1 event flag into C/Z, then clear it. |
| [POLLCT2](#pollct2) | Get CT2 event flag into C/Z, then clear it. |
| [POLLCT3](#pollct3) | Get CT3 event flag into C/Z, then clear it. |
| [POLLFBW](#pollfbw) | Get FBW event flag into C/Z, then clear it. |
| [POLLINT](#pollint) | Get INT event flag into C/Z, then clear it. |
| [POLLPAT](#pollpat) | Get PAT event flag into C/Z, then clear it. |
| [POLLQMT](#pollqmt) | Get QMT event flag into C/Z, then clear it. |
| [POLLSE1](#pollse1) | Get SE1 event flag into C/Z, then clear it. |
| [POLLSE2](#pollse2) | Get SE2 event flag into C/Z, then clear it. |
| [POLLSE3](#pollse3) | Get SE3 event flag into C/Z, then clear it. |
| [POLLSE4](#pollse4) | Get SE4 event flag into C/Z, then clear it. |
| [POLLXFI](#pollxfi) | Get XFI event flag into C/Z, then clear it. |
| [POLLXMT](#pollxmt) | Get XMT event flag into C/Z, then clear it. |
| [POLLXRL](#pollxrl) | Get XRL event flag into C/Z, then clear it. |
| [POLLXRO](#pollxro) | Get XRO event flag into C/Z, then clear it. |


### Events - Wait

| Instruction | Description |
|-------------|-------------|
| [WAITATN](#waitatn) | Wait for ATN event flag, then clear it |
| [WAITCT1](#waitct1) | Wait for CT1 event flag, then clear it |
| [WAITCT2](#waitct2) | Wait for CT2 event flag, then clear it |
| [WAITCT3](#waitct3) | Wait for CT3 event flag, then clear it |
| [WAITFBW](#waitfbw) | Wait for FBW event flag, then clear it |
| [WAITINT](#waitint) | Wait for INT event flag, then clear it |
| [WAITPAT](#waitpat) | Wait for PAT event flag, then clear it |
| [WAITSE1](#waitse1) | Wait for SE1 event flag, then clear it |
| [WAITSE2](#waitse2) | Wait for SE2 event flag, then clear it |
| [WAITSE3](#waitse3) | Wait for SE3 event flag, then clear it |
| [WAITSE4](#waitse4) | Wait for SE4 event flag, then clear it |
| [WAITXFI](#waitxfi) | Wait for XFI event flag, then clear it |
| [WAITXMT](#waitxmt) | Wait for XMT event flag, then clear it |
| [WAITXRL](#waitxrl) | Wait for XRL event flag, then clear it |
| [WAITXRO](#waitxro) | Wait for XRO event flag, then clear it |


### Events - Branch

| Instruction | Description |
|-------------|-------------|
| [JATN](#jatn) | Jump to S** if ATN event flag is set. |
| [JCT1](#jct1) | Jump to S** if CT1 event flag is set. |
| [JCT2](#jct2) | Jump to S** if CT2 event flag is set. |
| [JCT3](#jct3) | Jump to S** if CT3 event flag is set. |
| [JFBW](#jfbw) | Jump to S** if FBW event flag is set. |
| [JINT](#jint) | Jump to S** if INT event flag is set. |
| [JNATN](#jnatn) | Jump to S** if ATN event flag is clear. |
| [JNCT1](#jnct1) | Jump to S** if CT1 event flag is clear. |
| [JNCT2](#jnct2) | Jump to S** if CT2 event flag is clear. |
| [JNCT3](#jnct3) | Jump to S** if CT3 event flag is clear. |
| [JNFBW](#jnfbw) | Jump to S** if FBW event flag is clear. |
| [JNINT](#jnint) | Jump to S** if INT event flag is clear. |
| [JNPAT](#jnpat) | Jump to S** if PAT event flag is clear. |
| [JNQMT](#jnqmt) | Jump to S** if QMT event flag is clear. |
| [JNSE1](#jnse1) | Jump to S** if SE1 event flag is clear. |
| [JNSE2](#jnse2) | Jump to S** if SE2 event flag is clear. |
| [JNSE3](#jnse3) | Jump to S** if SE3 event flag is clear. |
| [JNSE4](#jnse4) | Jump to S** if SE4 event flag is clear. |
| [JNXFI](#jnxfi) | Jump to S** if XFI event flag is clear. |
| [JNXMT](#jnxmt) | Jump to S** if XMT event flag is clear. |
| [JNXRL](#jnxrl) | Jump to S** if XRL event flag is clear. |
| [JNXRO](#jnxro) | Jump to S** if XRO event flag is clear. |
| [JPAT](#jpat) | Jump to S** if PAT event flag is set. |
| [JQMT](#jqmt) | Jump to S** if QMT event flag is set. |
| [JSE1](#jse1) | Jump to S** if SE1 event flag is set. |
| [JSE2](#jse2) | Jump to S** if SE2 event flag is set. |
| [JSE3](#jse3) | Jump to S** if SE3 event flag is set. |
| [JSE4](#jse4) | Jump to S** if SE4 event flag is set. |
| [JXFI](#jxfi) | Jump to S** if XFI event flag is set. |
| [JXMT](#jxmt) | Jump to S** if XMT event flag is set. |
| [JXRL](#jxrl) | Jump to S** if XRL event flag is set. |
| [JXRO](#jxro) | Jump to S** if XRO event flag is set. |


### Events - Attention

| Instruction | Description |
|-------------|-------------|
| [COGATN](#cogatn) | Strobe "attention" of all cogs whose corresponging bits are high in D[15:0]. |


## Interrupts

| Instruction | Description |
|-------------|-------------|
| [ALLOWI](#allowi) | Allow interrupts (default). |
| [BRK](#brk) | If in debug ISR, set next break condition to D |
| [COGBRK](#cogbrk) | If in debug ISR, trigger asynchronous breakpoint in cog D[3:0] |
| [GETBRK](#getbrk) | Get breakpoint/cog status into D according to WC/WZ/WCZ |
| [NIXINT1](#nixint1) | Cancel INT1. |
| [NIXINT2](#nixint2) | Cancel INT2. |
| [NIXINT3](#nixint3) | Cancel INT3. |
| [SETINT1](#setint1) | Set INT1 source to D[3:0]. |
| [SETINT2](#setint2) | Set INT2 source to D[3:0]. |
| [SETINT3](#setint3) | Set INT3 source to D[3:0]. |
| [STALLI](#stalli) | Stall Interrupts. |
| [TRGINT1](#trgint1) | Trigger INT1, regardless of STALLI mode. |
| [TRGINT2](#trgint2) | Trigger INT2, regardless of STALLI mode. |
| [TRGINT3](#trgint3) | Trigger INT3, regardless of STALLI mode. |


## COG Control and Locks


### Hub Control - Cogs

| Instruction | Description |
|-------------|-------------|
| [COGID](#cogid) | If D is register and no WC, get cog ID (0 to 15) into D |
| [COGINIT](#coginit) | Start cog selected by D |
| [COGSTOP](#cogstop) | Stop cog D[3:0]. |


### Hub Control - Locks

| Instruction | Description |
|-------------|-------------|
| [LOCKNEW](#locknew) | Request a LOCK |
| [LOCKREL](#lockrel) | Release LOCK D[3:0] |
| [LOCKRET](#lockret) | Return LOCK D[3:0] for reallocation. |
| [LOCKTRY](#locktry) | Try to get LOCK D[3:0] |


### Hub Control - Multi

| Instruction | Description |
|-------------|-------------|
| [HUBSET](#hubset) | Set hub configuration to D. |


## CORDIC Coprocessor

| Instruction | Description |
|-------------|-------------|
| [GETQX](#getqx) | Retrieve CORDIC result X into D |
| [GETQY](#getqy) | Retrieve CORDIC result Y into D |
| [QDIV](#qdiv) | Begin CORDIC unsigned division of {SETQ value or 32'b0, D} / S |
| [QEXP](#qexp) | Begin CORDIC logarithm-to-number conversion of D |
| [QFRAC](#qfrac) | Begin CORDIC unsigned division of {D, SETQ value or 32'b0} / S |
| [QLOG](#qlog) | Begin CORDIC number-to-logarithm conversion of D |
| [QMUL](#qmul) | Begin CORDIC unsigned multiplication of D * S |
| [QROTATE](#qrotate) | Begin CORDIC rotation of point (D, SETQ value or 32'b0) by angle S |
| [QSQRT](#qsqrt) | Begin CORDIC square root of {S, D} |
| [QVECTOR](#qvector) | Begin CORDIC vectoring of point (D, S) |


## Streamer

| Instruction | Description |
|-------------|-------------|
| [GETXACC](#getxacc) | Get the streamer's Goertzel X accumulator into D and the Y accumulator into the next instruction's S, clear accumulators. |
| [SETXFRQ](#setxfrq) | Set streamer NCO frequency to D. |
| [XCONT](#xcont) | Buffer new streamer command to be issued on final NCO rollover of current command, continuing phase. |
| [XINIT](#xinit) | Issue streamer command immediately, zeroing phase. |
| [XSTOP](#xstop) | Stop streamer immediately. |
| [XZERO](#xzero) | Buffer new streamer command to be issued on final NCO rollover of current command, zeroing phase. |


## Color Space and Pixel Operations


### Color Space Converter

| Instruction | Description |
|-------------|-------------|
| [SETCFRQ](#setcfrq) | Set the colorspace converter "CFRQ" parameter to D[31:0]. |
| [SETCI](#setci) | Set the colorspace converter "CI" parameter to D[31:0]. |
| [SETCMOD](#setcmod) | Set the colorspace converter "CMOD" parameter to D[8:0]. |
| [SETCQ](#setcq) | Set the colorspace converter "CQ" parameter to D[31:0]. |
| [SETCY](#setcy) | Set the colorspace converter "CY" parameter to D[31:0]. |


### Pixel Mixer

| Instruction | Description |
|-------------|-------------|
| [ADDPIX](#addpix) | Add bytes of S into bytes of D, with $FF saturation. |
| [BLNPIX](#blnpix) | Alpha-blend bytes of S into bytes of D, using SETPIV value. |
| [MIXPIX](#mixpix) | Mix bytes of S into bytes of D, using SETPIX and SETPIV values. |
| [MULPIX](#mulpix) | Multiply bytes of S into bytes of D, where $FF = 1.0 and $00 = 0.0. |
| [SETPIV](#setpiv) | Set BLNPIX/MIXPIX blend factor to D[7:0]. |
| [SETPIX](#setpix) | Set MIXPIX mode to D[5:0]. |


## Register Indirection

| Instruction | Description |
|-------------|-------------|
| [ALTB](#altb) | Alter D field of next instruction to D[13:5]. |
| [ALTD](#altd) | Alter D field of next instruction to D[8:0]. |
| [ALTGB](#altgb) | Alter subsequent GETBYTE/ROLBYTE instruction |
| [ALTGN](#altgn) | Alter subsequent GETNIB/ROLNIB instruction |
| [ALTGW](#altgw) | Alter subsequent GETWORD/ROLWORD instruction |
| [ALTI](#alti) | Execute D in place of next instruction |
| [ALTR](#altr) | Alter result register address (normally D field) of next instruction to D[8:0]. |
| [ALTS](#alts) | Alter S field of next instruction to D[8:0]. |
| [ALTSB](#altsb) | Alter subsequent SETBYTE instruction |
| [ALTSN](#altsn) | Alter subsequent SETNIB instruction |
| [ALTSW](#altsw) | Alter subsequent SETWORD instruction |


## Miscellaneous

| Instruction | Description |
|-------------|-------------|
| [AUGD](#augd) | Queue |
| [AUGS](#augs) | Queue |
| [GETCT](#getct) | Get CT[31:0] or CT[63:32] if WC into D |
| [GETRND](#getrnd) | Get RND into C/Z |
| [NOP](#nop) | No operation. |
| [POP](#pop) | Pop stack (K) |
| [PUSH](#push) | Push D onto stack. |
| [SETQ](#setq) | Set Q to D |
| [SETQ2](#setq2) | Set Q to D |
| [WAITX](#waitx) | Wait 2 + D clocks if no WC/WZ/WCZ |


# Appendix C: Special Registers Quick Reference

## Register Summary

| Address | Hex | Register | Access | Purpose |
|---------|-----|----------|--------|---------|
| 496 | $1F0 | IJMP3 | R/W | Interrupt 3 jump address |
| 497 | $1F1 | IRET3 | R/W | Interrupt 3 return address |
| 498 | $1F2 | IJMP2 | R/W | Interrupt 2 jump address |
| 499 | $1F3 | IRET2 | R/W | Interrupt 2 return address |
| 500 | $1F4 | IJMP1 | R/W | Interrupt 1 jump address |
| 501 | $1F5 | IRET1 | R/W | Interrupt 1 return address |
| 502 | $1F6 | PA | R/W | Multi-purpose register A |
| 503 | $1F7 | PB | R/W | Multi-purpose register B |
| 504 | $1F8 | PTRA | R/W | Hub pointer A |
| 505 | $1F9 | PTRB | R/W | Hub pointer B |
| 506 | $1FA | DIRA | R/W | Pin direction 0-31 |
| 507 | $1FB | DIRB | R/W | Pin direction 32-63 |
| 508 | $1FC | OUTA | R/W | Pin output 0-31 |
| 509 | $1FD | OUTB | R/W | Pin output 32-63 |
| 510 | $1FE | INA | R/O | Pin input 0-31 |
| 511 | $1FF | INB | R/O | Pin input 32-63 |

## Dual-Purpose Register Functions

| Register | Primary | Alternate Functions |
|----------|---------|---------------------|
| PA ($1F6) | General | CALLD return, CALLPA param, LOC address |
| PB ($1F7) | General | CALLD return, CALLPB param, LOC address |
| INA ($1FE) | Pin input | Debug interrupt call address |
| INB ($1FF) | Pin input | Debug interrupt return address |

## Memory Map

```
$1FF ┌─────────┐
     │   INB   │ ← Read-only: pins 32-63
$1FE ├─────────┤
     │   INA   │ ← Read-only: pins 0-31
$1FD ├─────────┤
     │  OUTB   │
$1FC ├─────────┤  Fixed Special
     │  OUTA   │  Registers
$1FB ├─────────┤
     │  DIRB   │
$1FA ├─────────┤
     │  DIRA   │
$1F9 ├─────────┤
     │  PTRB   │
$1F8 ├─────────┤
     │  PTRA   │
$1F7 ├─────────┤
     │   PB    │
$1F6 ├─────────┤  Dual-Purpose
     │   PA    │  Registers
$1F5 ├─────────┤
     │  IRET1  │
$1F4 ├─────────┤
     │  IJMP1  │
$1F3 ├─────────┤
     │  IRET2  │
$1F2 ├─────────┤
     │  IJMP2  │
$1F1 ├─────────┤
     │  IRET3  │
$1F0 └─────────┘
     │  IJMP3  │
     └─────────┘
```

*For complete documentation, see Part II: Special Registers.*

# Appendix D: Predefined Constants Quick Reference

## Boolean Constants

| Constant | Hex Value | Decimal | Description |
|----------|-----------|---------|-------------|
| TRUE | $FFFFFFFF | -1 | All bits set (boolean true) |
| FALSE | $00000000 | 0 | All bits clear (boolean false) |

## Numeric Limit Constants

| Constant | Hex Value | Decimal | Description |
|----------|-----------|---------|-------------|
| NEGX | $80000000 | -2,147,483,648 | Most negative signed 32-bit |
| POSX | $7FFFFFFF | +2,147,483,647 | Most positive signed 32-bit |

## Mathematical Constants

| Constant | Hex Value | Approximate | Description |
|----------|-----------|-------------|-------------|
| PI | $40490FDB | 3.14159265 | IEEE 754 single-precision π |

## Execution Mode Constants

| Constant | Pattern | Description |
|----------|---------|-------------|
| COGEXEC | %0_0_0000 | Execute from COG RAM after loading |
| HUBEXEC | %0_1_0000 | Execute directly from Hub RAM |
| COGEXEC_NEW | %1_0_0000 | Auto-select COG, execute from COG |
| COGEXEC_NEW_PAIR | %1_0_0001 | Auto-select COG pair, execute from COG |
| HUBEXEC_NEW | %1_1_0000 | Auto-select COG, execute from Hub |
| HUBEXEC_NEW_PAIR | %1_1_0001 | Auto-select COG pair, execute from Hub |

## COGINIT Usage Example

```pasm
        ' Start COG 2 executing from COG RAM
        COGINIT #COGEXEC, ptra, #2

        ' Start any available COG executing from Hub
        COGINIT #HUBEXEC_NEW, ##@hub_code wc
        IF_C    jmp     #no_cogs_available
```

*For complete documentation, see Part II: Constants.*

# Appendix E: Reserved Words Reference

This appendix lists all reserved words in PASM2. These identifiers cannot be used as user-defined labels, symbols, or variable names. Attempting to use a reserved word as a label will result in an assembly error.

**Total Reserved Words: 449**

## Categories

Reserved words fall into six main categories:

1. **Instruction Mnemonics** (358 words) - All instruction names
2. **Assembly Directives** (14 words) - Assembly-time directives
3. **Predefined Constants** (11 words) - Built-in constant values
4. **Special Register Names** (16 words) - Special-purpose registers
5. **Condition Keywords** (41 words) - Conditional execution prefixes
6. **Effect Keywords** (9 words) - Flag modification suffixes



## Instruction Mnemonics (358 words)

All PASM2 instruction names are reserved. These appear in alphabetical order for quick reference:

```
ABS         ADD         ADDCT1      ADDCT2      ADDCT3      ADDPIX
ADDS        ADDSX       ADDX        AKPIN       ALLOWI      ALTB
ALTD        ALTGB       ALTGN       ALTGW       ALTI        ALTR
ALTS        ALTSB       ALTSN       ALTSW       AND         ANDN
ASMCLK      AUGD        AUGS        BITC        BITH        BITL
BITNC       BITNOT      BITNZ       BITRND      BITZ        BLNPIX
BMASK       BRK         CALL        CALLA       CALLB       CALLD
CALLPA      CALLPB      CMP         CMPM        CMPR        CMPS
CMPSUB      CMPSX       CMPX        COGATN      COGBRK      COGID
COGINIT     COGSTOP     CRCBIT      CRCNIB      DECMOD      DECOD
DIRC        DIRH        DIRL        DIRNC       DIRNOT      DIRNZ
DIRRND      DIRZ        DJF         DJNF        DJNZ        DJZ
DRVC        DRVH        DRVL        DRVNC       DRVNOT      DRVNZ
DRVRND      DRVZ        ENCOD       EXECF       FBLOCK      FGE
FGES        FLE         FLES        FLTC        FLTH        FLTL
FLTNC       FLTNOT      FLTNZ       FLTRND      FLTZ        GETBRK
GETBYTE     GETCT       GETNIB      GETPTR      GETQX       GETQY
GETRND      GETSCP      GETWORD     GETXACC     HUBSET      IJNZ
IJZ         INCMOD      JATN        JCT1        JCT2        JCT3
JFBW        JINT        JMP         JMPREL      JNATN       JNCT1
JNCT2       JNCT3       JNFBW       JNINT       JNPAT       JNQMT
JNSE1       JNSE2       JNSE3       JNSE4       JNXFI       JNXMT
JNXRL       JNXRO       JPAT        JQMT        JSE1        JSE2
JSE3        JSE4        JXFI        JXMT        JXRL        JXRO
LOC         LOCKNEW     LOCKREL     LOCKRET     LOCKTRY     MERGEB
MERGEW      MIXPIX      MODC        MODCZ       MODZ        MOV
MOVBYTS     MUL         MULPIX      MULS        MUXC        MUXNC
MUXNIBS     MUXNITS     MUXNZ       MUXQ        MUXZ        NEG
NEGC        NEGNC       NEGNZ       NEGZ        NIXINT1     NIXINT2
NIXINT3     NOP         NOT         ONES        OR          OUTC
OUTH        OUTL        OUTNC       OUTNOT      OUTNZ       OUTRND
OUTZ        POLLATN     POLLCT1     POLLCT2     POLLCT3     POLLFBW
POLLINT     POLLPAT     POLLQMT     POLLSE1     POLLSE2     POLLSE3
POLLSE4     POLLXFI     POLLXMT     POLLXRL     POLLXRO     POP
POPA        POPB        PUSH        PUSHA       PUSHB       QDIV
QEXP        QFRAC       QLOG        QMUL        QROTATE     QSQRT
QVECTOR     RCL         RCR         RCZL        RCZR        RDBYTE
RDFAST      RDLONG      RDLUT       RDPIN       RDWORD      REP
RESI0       RESI1       RESI2       RESI3       RET         RETA
RETB        RETI0       RETI1       RETI2       RETI3       REV
RFBYTE      RFLONG      RFVAR       RFVARS      RFWORD      RGBEXP
RGBSQZ      ROL         ROLBYTE     ROLNIB      ROLWORD     ROR
RQPIN       SAL         SAR         SCA         SCAS        SETBYTE
SETCFRQ     SETCI       SETCMOD     SETCQ       SETCY       SETD
SETDACS     SETINT1     SETINT2     SETINT3     SETLUTS     SETNIB
SETPAT      SETPIV      SETPIX      SETQ        SETQ2       SETR
SETS        SETSCP      SETSE1      SETSE2      SETSE3      SETSE4
SETWORD     SETXFRQ     SEUSSF      SEUSSR      SHL         SHR
SIGNX       SKIP        SKIPF       SPLITB      SPLITW      STALLI
SUB         SUBR        SUBS        SUBSX       SUBX        SUMC
SUMNC       SUMNZ       SUMZ        TEST        TESTB       TESTBN
TESTN       TESTP       TESTPN      TJF         TJNF        TJNS
TJNZ        TJS         TJV         TJZ         TRGINT1     TRGINT2
TRGINT3     WAITATN     WAITCT1     WAITCT2     WAITCT3     WAITFBW
WAITINT     WAITPAT     WAITSE1     WAITSE2     WAITSE3     WAITSE4
WAITX       WAITXFI     WAITXMT     WAITXRL     WAITXRO     WFBYTE
WFLONG      WFWORD      WMLONG      WRBYTE      WRC         WRFAST
WRLONG      WRLUT       WRNC        WRNZ        WRPIN       WRWORD
WRZ         WXPIN       WYPIN       XCONT       XINIT       XOR
XORO32      XSTOP       XZERO       ZEROX
```



## Assembly Directives (14 words)

Directives control the assembly process and code organization:

- **ALIGNL** - Align to next long boundary (4-byte alignment)
- **ALIGNW** - Align to next word boundary (2-byte alignment)
- **BYTE** - Reserve/initialize byte-sized data
- **BYTEFIT** - Verify code fits in specified byte count
- **DEBUG** - Insert debug statements (Spin2 feature)
- **DITTO** - Repeat previous instruction encoding
- **FIT** - Verify code fits in COG memory
- **LONG** - Reserve/initialize long-sized data (32 bits)
- **ORG** - Set assembly origin (COG address)
- **ORGF** - Set assembly origin with fill
- **ORGH** - Set assembly origin (Hub address)
- **RES** - Reserve uninitialized registers/memory
- **WORD** - Reserve/initialize word-sized data (16 bits)
- **WORDFIT** - Verify code fits in specified word count



## Predefined Constants (11 words)

Built-in constants that can be used in assembly expressions:

### Basic Constants (5)

- **FALSE** - Boolean false value (`$00000000`, decimal 0)
- **NEGX** - Most negative signed 32-bit value (`$80000000`, decimal -2147483648)
- **PI** - Fixed-point pi value for CORDIC operations
- **POSX** - Most positive signed 32-bit value (`$7FFFFFFF`, decimal 2147483647)
- **TRUE** - Boolean true value (`$FFFFFFFF`, decimal -1)

### Execution Mode Constants (6)

Used with the COGINIT instruction to specify execution mode:

- **COGEXEC** - Execute from COG RAM (base mode, `%0_0_0000`)
- **COGEXEC_NEW** - Auto-select available COG, execute from COG RAM
- **COGEXEC_NEW_PAIR** - Auto-select COG pair, execute from COG RAM
- **HUBEXEC** - Execute from Hub RAM (base mode, `%0_1_0000`)
- **HUBEXEC_NEW** - Auto-select available COG, execute from Hub RAM
- **HUBEXEC_NEW_PAIR** - Auto-select COG pair, execute from Hub RAM

**Note:** The `_NEW` and `_NEW_PAIR` variants are bit patterns that modify the base `COGEXEC` and `HUBEXEC` constants for use with COGINIT's automatic COG selection feature.



## Special Register Names (16 words)

Special-purpose registers mapped to COG RAM addresses `$1F0-$1FF`:

### Dual-Purpose Registers ($1F0-$1F7)

Can be used as general RAM or special registers depending on enabled features:

- **IJMP3** - Interrupt 3 jump address ($1F0, 496)
- **IRET3** - Interrupt 3 return address ($1F1, 497)
- **IJMP2** - Interrupt 2 jump address ($1F2, 498)
- **IRET2** - Interrupt 2 return address ($1F3, 499)
- **IJMP1** - Interrupt 1 jump address ($1F4, 500)
- **IRET1** - Interrupt 1 return address ($1F5, 501)
- **PA** - Multi-purpose register A ($1F6, 502)
- **PB** - Multi-purpose register B ($1F7, 503)

### Fixed Special Registers ($1F8-$1FF)

Always provide special functions when accessed:

- **PTRA** - Pointer A to Hub RAM ($1F8, 504)
- **PTRB** - Pointer B to Hub RAM ($1F9, 505)
- **DIRA** - Direction register for pins 0-31 ($1FA, 506)
- **DIRB** - Direction register for pins 32-63 ($1FB, 507)
- **OUTA** - Output register for pins 0-31 ($1FC, 508)
- **OUTB** - Output register for pins 32-63 ($1FD, 509)
- **INA** - Input register for pins 0-31 ($1FE, 510)
- **INB** - Input register for pins 32-63 ($1FF, 511)



## Condition Keywords (41 words)

Conditional execution prefixes (IF_xxx) that can be applied to any instruction. These test the C (Carry) and Z (Zero) flags:

### Primary Condition Codes (16)

These are the canonical condition names:

- **IF_ALWAYS** - Always execute (default, can be omitted)
- **IF_NEVER** - Never execute (effectively a NOP)
- **IF_C** - Execute if C=1
- **IF_NC** - Execute if C=0
- **IF_Z** - Execute if Z=1
- **IF_NZ** - Execute if Z=0
- **IF_C_AND_Z** - Execute if C=1 AND Z=1
- **IF_C_AND_NZ** - Execute if C=1 AND Z=0
- **IF_NC_AND_Z** - Execute if C=0 AND Z=1
- **IF_NC_AND_NZ** - Execute if C=0 AND Z=0
- **IF_C_OR_Z** - Execute if C=1 OR Z=1
- **IF_C_OR_NZ** - Execute if C=1 OR Z=0
- **IF_NC_OR_Z** - Execute if C=0 OR Z=1
- **IF_NC_OR_NZ** - Execute if C=0 OR Z=0
- **IF_C_EQ_Z** - Execute if C equals Z
- **IF_C_NE_Z** - Execute if C not equal to Z

### Comparison Aliases (15)

Convenient aliases for post-comparison conditional execution:

**Unsigned comparison aliases:**
- **IF_A** - Above (same as IF_NC_AND_NZ)
- **IF_AE** - Above or equal (same as IF_NC)
- **IF_B** - Below (same as IF_C)
- **IF_BE** - Below or equal (same as IF_C_OR_Z or IF_NC_OR_Z)
- **IF_E** - Equal (same as IF_Z)
- **IF_NE** - Not equal (same as IF_NZ)

**Signed comparison aliases:**
- **IF_GE** - Greater or equal (same as IF_NC)
- **IF_GT** - Greater than (same as IF_NC_AND_NZ)
- **IF_LE** - Less or equal (same as IF_NC_OR_Z)
- **IF_LT** - Less than (same as IF_C)

**Other aliases:**
- **IF_DIFF** - Different (same as IF_C_NE_Z)
- **IF_SAME** - Same (same as IF_C_EQ_Z)
- **IF_NZ_AND_C** - Not zero and carry (same as IF_C_AND_NZ)
- **IF_NZ_AND_NC** - Not zero and no carry (same as IF_NC_AND_NZ)
- **IF_Z_AND_C** - Zero and carry (same as IF_C_AND_Z)

### Special Return Condition (1)

- **_RET_** - Always execute AND return (combines execution with return)

### Symmetric Alternatives (9)

Additional aliases that express the same conditions in reverse order:

- **IF_Z_AND_NC** - Same as IF_NC_AND_Z
- **IF_Z_OR_C** - Same as IF_C_OR_Z
- **IF_Z_OR_NC** - Same as IF_NC_OR_Z
- **IF_NZ_OR_C** - Same as IF_C_OR_NZ
- **IF_NZ_OR_NC** - Same as IF_NC_OR_NZ

**Note:** Many conditions have multiple valid names (aliases). For example, `IF_C`, `IF_B`, and `IF_LT` all represent the same condition code but provide semantic clarity depending on context.



## Effect Keywords (9 words)

Effect suffixes control flag updates after instruction execution:

### Basic Effect Modifiers (3)

- **WC** - Write result to Carry flag
- **WZ** - Write result to Zero flag
- **WCZ** - Write result to both Carry and Zero flags

### Logical Effect Modifiers (6)

Combine instruction result with existing flag using logic operation:

- **ANDC** - AND result with C flag
- **ANDZ** - AND result with Z flag
- **ORC** - OR result with C flag
- **ORZ** - OR result with Z flag
- **XORC** - XOR result with C flag
- **XORZ** - XOR result with Z flag

**Usage:** Effect keywords appear after the instruction's operands:

```pasm
ADD   x, y  WC      ' Update C flag with carry
CMP   a, b  WCZ     ' Update both C and Z flags
TEST  val, mask  ANDZ   ' AND test result with Z flag
```



## Avoiding Reserved Words

When naming labels, variables, and symbols in your PASM2 code:

1. **Check this reference** before choosing identifiers
2. **Use descriptive names** that clearly differ from reserved words
3. **Add prefixes/suffixes** to avoid conflicts (e.g., `my_add`, `loop_counter`)
4. **Case sensitivity:** PASM2 is case-insensitive - `MOV`, `mov`, and `Mov` are all reserved

### Common Naming Strategies

- Add application-specific prefixes: `uart_receive`, `led_toggle`
- Add type suffixes: `count_value`, `delay_ms`
- Use underscores: `_start`, `main_loop`, `temp_reg`
- Combine words: `blink_rate`, `max_count`

### Example Conflicts to Avoid

```pasm
' WRONG - uses reserved words as labels
add:    mov   x, #1      ' Error: 'add' is instruction
or:     jmp   #loop      ' Error: 'or' is instruction
byte:   long  $0         ' Error: 'byte' is directive

' CORRECT - uses valid label names
add_routine:  mov   x, #1
choice_or:    jmp   #loop
byte_data:    long  $0
```



## Summary

PASM2 reserves **449 identifiers** across six categories:

| Category | Count | Purpose |
|----------|-------|---------|
| Instructions | 358 | All instruction mnemonics |
| Directives | 14 | Assembly-time directives |
| Constants | 11 | Predefined constant values |
| Special Registers | 16 | Hardware-mapped registers |
| Conditions | 41 | Conditional execution prefixes |
| Effects | 9 | Flag modification suffixes |
| **Total** | **449** | |

**Cross-Reference:** See Part II for complete documentation of instructions, directives, constants, and special registers. See Chapter 3 (Conditional Execution) for detailed explanation of condition codes and effect modifiers.

# Appendix F: Opcode Bit Patterns Reference

## Instruction Word Format

The P2 uses a fixed 32-bit instruction word with five distinct fields that encode all instruction information:

```{=latex}
\InstructionEncoding{Generic}{EEEE}{OOOOOOO}{CZI}{DDDDDDDDD}{SSSSSSSSS}
```

This compact encoding allows:
- 16 execution conditions
- 128 primary opcodes
- 512 register addresses (COG and LUT)
- Immediate mode selection
- Flag effect control

## Field Definitions

### Condition Field (EEEE) - Bits 31:28

The condition field determines whether an instruction executes based on the current state of the C and Z flags:

| EEEE | Mnemonic | Execute When | Description |
|------|----------|--------------|-------------|
| 0000 | IF_ALWAYS | Always | Unconditional execution (default) |
| 0001 | IF_NC_AND_NZ | C=0 AND Z=0 | Above (unsigned) |
| 0010 | IF_NC_AND_Z | C=0 AND Z=1 | Not carry and zero |
| 0011 | IF_NC | C=0 | Not carry (also IF_AE, IF_GE) |
| 0100 | IF_C_AND_NZ | C=1 AND Z=0 | Carry and not zero |
| 0101 | IF_NZ | Z=0 | Not zero (also IF_NE) |
| 0110 | IF_C_NE_Z | C≠Z | Carry not equal zero |
| 0111 | IF_NC_OR_NZ | C=0 OR Z=0 | Not (carry and zero) |
| 1000 | IF_C_AND_Z | C=1 AND Z=1 | Carry and zero |
| 1001 | IF_C_EQ_Z | C=Z | Carry equals zero |
| 1010 | IF_Z | Z=1 | Zero (also IF_E) |
| 1011 | IF_NC_OR_Z | C=0 OR Z=1 | Not carry or zero |
| 1100 | IF_C | C=1 | Carry (also IF_B, IF_LT) |
| 1101 | IF_C_OR_NZ | C=1 OR Z=0 | Carry or not zero |
| 1110 | IF_C_OR_Z | C=1 OR Z=1 | Carry or zero (also IF_BE, IF_LE) |
| 1111 | IF_NEVER | Never | Never executes (used for padding) |

When a condition is false, the instruction is skipped with no effect on registers or flags.

### CZI Field - Bits 23:21

The CZI field controls flag updates and addressing mode:

| Bit | Name | Meaning |
|-----|------|---------|
| 23 | C | Write C flag if set (WC effect) |
| 22 | Z | Write Z flag if set (WZ effect) |
| 21 | I | Source is immediate if set (#) |

**Examples:**
- `CZI = 000`: No flag writes, S is register address
- `CZI = 001`: No flag writes, S is immediate value
- `CZI = 100`: Write C only, S is register address
- `CZI = 101`: Write C only, S is immediate value
- `CZI = 110`: Write C and Z, S is register address
- `CZI = 111`: Write C and Z, S is immediate value

### Destination Field (D) - Bits 18:9

9-bit field specifying the destination register address:

| Range | Region |
|-------|--------|
| $000-$1EF | COG RAM (496 registers) |
| $1F0-$1FF | Special registers (16 registers) |
| $200-$3FF | LUT RAM (512 longs) |

The D field always references a register, never an immediate value.

### Source Field (S) - Bits 8:0

9-bit field specifying either:
- **Register address** (when I=0): Same address space as D field
- **Immediate value** (when I=1): Unsigned 0-511, or extended by AUGS

When used as immediate, negative values or values >511 require AUGS prefix.

### Opcode Field (OOOOOOO) - Bits 27:21

7-bit field encoding the instruction operation. See Opcode Organization section below.

## Opcode Field Organization

The 7-bit opcode space (128 possible opcodes) is organized by instruction category:

### Basic Operations (0000000-0001111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 0000000 | ROR | Rotate/shift |
| 0000001 | ROL | Rotate/shift |
| 0000010 | SHR | Rotate/shift |
| 0000011 | SHL | Rotate/shift |
| 0000100 | RCR | Rotate/shift |
| 0000101 | RCL | Rotate/shift |
| 0000110 | SAR | Rotate/shift |
| 0000111 | SAL | Rotate/shift |
| 0001000 | ADD | Arithmetic |
| 0001001 | ADDX | Arithmetic |
| 0001010 | ADDS | Arithmetic |
| 0001011 | ADDSX | Arithmetic |
| 0001100 | SUB | Arithmetic |
| 0001101 | SUBX | Arithmetic |
| 0001110 | SUBS | Arithmetic |
| 0001111 | SUBSX | Arithmetic |

### Comparison and Logic (0010000-0011111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 0010000 | CMP | Comparison |
| 0010001 | CMPX | Comparison |
| 0010010 | CMPS | Comparison |
| 0010011 | CMPSX | Comparison |
| 0010100 | CMPR | Comparison |
| 0010101 | CMPM | Comparison |
| 0010110 | SUBR | Arithmetic |
| 0010111 | CMPSUB | Comparison |
| 0011000 | FGE | Min/max |
| 0011001 | FLE | Min/max |
| 0011010 | FGES | Min/max |
| 0011011 | FLES | Min/max |
| 0011100 | SUMC | Summation |
| 0011101 | SUMNC | Summation |
| 0011110 | SUMZ | Summation |
| 0011111 | SUMNZ | Summation |

### Bit Operations (0100000-0101111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 0100000 | TESTB | Bit test |
| 0100001 | TESTBN | Bit test |
| 0100010-0100011 | Reserved | - |
| 0100100 | BITL | Bit write |
| 0100101 | BITH | Bit write |
| 0100110 | BITC | Bit write |
| 0100111 | BITNC | Bit write |
| 0101000 | BITZ | Bit write |
| 0101001 | BITNZ | Bit write |
| 0101010 | BITRND | Bit write |
| 0101011 | BITNOT | Bit write |
| 0101100 | AND | Logic |
| 0101101 | ANDN | Logic |
| 0101110 | OR | Logic |
| 0101111 | XOR | Logic |

### Move and Multiply (0110000-0111111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 0110000 | MUXC | Multiplex |
| 0110001 | MUXNC | Multiplex |
| 0110010 | MUXZ | Multiplex |
| 0110011 | MUXNZ | Multiplex |
| 0110100 | MOV | Data movement |
| 0110101 | NOT | Logic |
| 0110110 | ABS | Arithmetic |
| 0110111 | NEG | Arithmetic |
| 0111000 | NEGC | Arithmetic |
| 0111001 | NEGNC | Arithmetic |
| 0111010 | NEGZ | Arithmetic |
| 0111011 | NEGNZ | Arithmetic |
| 0111100 | INCMOD | Modulo |
| 0111101 | DECMOD | Modulo |
| 0111110 | ZEROX | Bit field |
| 0111111 | SIGNX | Bit field |

### Extended Math (1000000-1001111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1000000 | ENCOD | Encoding |
| 1000001 | ONES | Bit counting |
| 1000010 | TEST | Testing |
| 1000011 | TESTN | Testing |
| 1000100 | SETNIB | Nibble/byte |
| 1000101 | GETNIB | Nibble/byte |
| 1000110 | ROLNIB | Nibble/byte |
| 1000111 | SETBYTE | Nibble/byte |
| 1001000 | GETBYTE | Nibble/byte |
| 1001001 | ROLBYTE | Nibble/byte |
| 1001010 | SETWORD | Word operations |
| 1001011 | GETWORD | Word operations |
| 1001100 | ROLWORD | Word operations |
| 1001101 | ALTSN | Indirection |
| 1001110 | ALTGN | Indirection |
| 1001111 | ALTSB | Indirection |

### Memory and Multiply (1010000-1011111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1010000 | ALTGB | Indirection |
| 1010001 | ALTSW | Indirection |
| 1010010 | ALTGW | Indirection |
| 1010011 | ALTR | Indirection |
| 1010100 | ALTD | Indirection |
| 1010101 | ALTS | Indirection |
| 1010110 | ALTB | Indirection |
| 1010111 | ALTI | Indirection |
| 1011000 | SETR | Register control |
| 1011001 | SETD | Register control |
| 1011010 | SETS | Register control |
| 1011011 | DECOD | Decoding |
| 1011100 | BMASK | Bit mask |
| 1011101 | CRCBIT | CRC |
| 1011110 | CRCNIB | CRC |
| 1011111 | MUXNITS | Multiplex |

### Multiply Operations (1100000-1100111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1100000 | MUXNIBS | Multiplex |
| 1100001 | MUXQ | Multiplex |
| 1100010 | MOVBYTS | Data movement |
| 1100011 | MUL | Multiply (U×U) |
| 1100100 | MULS | Multiply (S×S) |
| 1100101 | SCA | Multiply (U×U, scaled) |
| 1100110 | SCAS | Multiply (S×S, scaled) |
| 1100111 | ADDPIX | Pixel operations |

### Control Flow (1101000-1101111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1101000 | MULPIX | Pixel operations |
| 1101001 | BLNPIX | Pixel operations |
| 1101010 | MIXPIX | Pixel operations |
| 1101011 | ADDCT1 | Event control |
| 1101100 | ADDCT2 | Event control |
| 1101101 | ADDCT3 | Event control |
| 1101110 | WMLONG | Hub write |
| 1101111 | RQPIN | Smart Pins |

### Hub and Special (1110000-1111111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1110000 | RDPIN | Smart Pins |
| 1110001 | RDLUT | LUT read |
| 1110010 | RDBYTE | Hub read |
| 1110011 | RDWORD | Hub read |
| 1110100 | RDLONG | Hub read |
| 1110101 | CALLD | Call/return |
| 1110110-1110111 | Reserved | - |
| 1111000 | CALLPA | Call with parameter |
| 1111001 | CALLPB | Call with parameter |
| 1111010 | DJZ | Loop control |
| 1111011 | DJNZ | Loop control |
| 1111100 | DJF | Loop control |
| 1111101 | DJNF | Loop control |
| 1111110 | IJZ | Loop control |
| 1111111 | IJNZ | Loop control |

*Note: This is a representative subset. Complete opcode tables appear in Appendix A.*

## Special Encoding Forms

### AUGS/AUGD (Immediate Extension)

When immediate values exceed 9 bits, AUGS and AUGD instructions extend the next instruction's operands:

| Instruction | Bit Pattern | Extended Field |
|-------------|-------------|----------------|
| AUGS | `1111_000x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx` | S becomes 32 bits |
| AUGD | `1111_100x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx` | D becomes 32 bits |

**Extension mechanism:**

- Bits 31:9 come from the AUG instruction (x bits above)
- Bits 8:0 come from the following instruction's S or D field
- Combined value used for that instruction only

**Example:**

```pasm
AUGS    #$1234      ' Bits 31:9 = $1234
MOV     result, #$56 ' S = $1234_056 = $2468AC
```

### NOP Encoding

NOP is encoded as all zeros: `0000_0000_000_000000000_000000000`

This decodes as `IF_ALWAYS ROR $000, $000` - a useless rotate with no effect.

### Hub Instruction Extensions

Some hub instructions use extended encoding:

**WRLONG D, #\S (WC, WZ, WCZ):**
- Uses special OOOOOOO values to indicate hub write variants
- Additional mode bits in S field select FIFO vs direct addressing

**RDXXXX/WRXXXX with PTRx:**
- Uses PTRA/PTRB selection bit
- Auto-increment/decrement encoding
- Index register selection

See Appendix A for complete hub instruction encoding details.

## Encoding Examples

### Example 1: ADD D, #5

```
ADD     result, #5      ' Add immediate 5 to result

Encoding breakdown:
  Condition: 0000 (IF_ALWAYS - unconditional)
  Opcode: 0001000 (ADD operation)
  CZI: 001 (no WC, no WZ, immediate mode)
  D: [9-bit register address of 'result']
  S: 000000101 (immediate value 5)

32-bit pattern:
  0000_0001000_001_DDDDDDDDD_000000101
  ││││ │││││││ │││ │││││││││ │││││││││
  ││││ │││││││ │││ └────┬───┘ └───┬───┘
  ││││ │││││││ │││      │         └─ S = 5
  ││││ │││││││ │││      └─ D = result address
  ││││ │││││││ └┴┴─ I=1, Z=0, C=0
  ││││ └─────┴─ ADD opcode
  └──┴─ IF_ALWAYS
```

### Example 2: IF_Z MOV D, S WC

```
  IF_Z    MOV     dest, source    WC

Encoding breakdown:
  Condition: 1010 (IF_Z - execute only if Z=1)
  Opcode: 0110100 (MOV operation)
  CZI: 100 (WC=yes, WZ=no, register mode)
  D: [9-bit register address of 'dest']
  S: [9-bit register address of 'source']

32-bit pattern:
  1010_0110100_100_DDDDDDDDD_SSSSSSSSS
  ││││ │││││││ │││ │││││││││ │││││││││
  ││││ │││││││ │││ └────┬───┘ └───┬───┘
  ││││ │││││││ │││      │         └─ S = source address
  ││││ │││││││ │││      └─ D = dest address
  ││││ │││││││ └┴┴─ I=0, Z=0, C=1 (WC)
  ││││ └─────┴─ MOV opcode
  └──┴─ IF_Z
```

### Example 3: DJNZ loop, #label WC

```
DJNZ    counter, #target    WC

Encoding breakdown:
  Condition: 0000 (IF_ALWAYS)
  Opcode: 1111011 (DJNZ operation)
  CZI: 101 (WC=yes, WZ=no, immediate mode)
  D: [9-bit register address of 'counter']
  S: [9-bit relative branch offset]

Notes:
  - S field contains signed relative offset
  - Offset is from next instruction PC
  - WC sets C flag based on counter=0 after decrement
  - D register decremented before branch decision

32-bit pattern:
  0000_1111011_101_DDDDDDDDD_SSSSSSSSS
```

### Example 4: CALLD return_reg, #subroutine WC, WZ

```
CALLD   return_addr, #subroutine    WC, WZ

Encoding breakdown:
  Condition: 0000 (IF_ALWAYS)
  Opcode: 1110101 (CALLD operation)
  CZI: 111 (WC=yes, WZ=yes, immediate mode)
  D: [9-bit register address for return address]
  S: [9-bit absolute branch target]

Effect:
  - D ← PC+1 (return address)
  - PC ← S (jump to subroutine)
  - Flags updated based on operation
```

### Example 5: Extended Immediate with AUGS

```
MOV     result, ##$12345678

Assembler generates two instructions:

1) AUGS #$12345678 >> 9:
   1111_000_[23-bit value = $91A2B]
   Provides bits 31:9 = $91A2B

2) MOV result, #$12345678 & $1FF:
   0000_0110100_001_[result]_078
   Uses bits 8:0 = $078

Combined: result ← $91A2B_078 = $12345678
```

## Decoding Process

To decode a 32-bit instruction word:

1. **Extract condition field** (bits 31:28)
   - Check against C and Z flags
   - Skip instruction if condition false

2. **Extract opcode** (bits 27:21)
   - Lookup instruction mnemonic
   - Determine operation category

3. **Extract CZI field** (bits 23:21)
   - Determine immediate vs register mode
   - Identify which flags will be updated

4. **Extract D field** (bits 18:9)
   - Decode destination register address
   - May be modified by prior AUGD

5. **Extract S field** (bits 8:0)
   - If I=1: immediate value (possibly extended by AUGS)
   - If I=0: source register address

6. **Execute instruction**
   - Perform opcode operation
   - Write result to D register
   - Update flags per CZI setting

## Special Register Encoding

The special register range ($1F0-$1FF) uses specific D/S field values:

| Address | Register | Purpose |
|---------|----------|---------|
| $1F0 | IJMP3 | Interrupt jump 3 |
| $1F1 | IRET3 | Interrupt return 3 |
| $1F2 | IJMP2 | Interrupt jump 2 |
| $1F3 | IRET2 | Interrupt return 2 |
| $1F4 | IJMP1 | Interrupt jump 1 |
| $1F5 | IRET1 | Interrupt return 1 |
| $1F6 | PA | Pin A control |
| $1F7 | PB | Pin B control |
| $1F8 | PTRA | Hub pointer A |
| $1F9 | PTRB | Hub pointer B |
| $1FA | DIRA | Pin direction A |
| $1FB | DIRB | Pin direction B |
| $1FC | OUTA | Pin output A |
| $1FD | OUTB | Pin output B |
| $1FE | INA | Pin input A |
| $1FF | INB | Pin input B |

Reading these addresses accesses hardware registers. Writing to some (like INA/INB) has no effect.

## Bit Field Summary

Quick reference for manual instruction encoding:

| Field | Bits | Width | Purpose |
|-------|------|-------|---------|
| Condition (EEEE) | 31:28 | 4 | Execution condition |
| Opcode (OOOOOOO) | 27:21 | 7 | Instruction operation |
| C flag write | 23 | 1 | Update C if set |
| Z flag write | 22 | 1 | Update Z if set |
| Immediate mode | 21 | 1 | S is immediate if set |
| Destination (D) | 18:9 | 9 | Register address |
| Source (S) | 8:0 | 9 | Register or immediate |

**Total:** 32 bits (4 + 7 + 3 + 9 + 9)

## Notes

- **Instruction alignment:** All instructions are 32-bit aligned in COG/LUT memory
- **Execution time:** Most instructions execute in 2 clock cycles
- **Hub instructions:** RDLONG/WRLONG may take additional cycles for hub access
- **SKIPF pattern:** Uses special encoding for multi-instruction skip patterns
- **Reserved opcodes:** Some opcode values are reserved for future use

For complete instruction encoding details, see **Appendix A: Instruction Set Reference**.

For instruction timing and pipeline behavior, see **Chapter 4: Instruction Execution**.

For condition code usage patterns, see **Chapter 6: Control Flow**.

