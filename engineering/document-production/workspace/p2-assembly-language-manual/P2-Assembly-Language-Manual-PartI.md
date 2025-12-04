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

### 2.8.2 Visual Anchors: Color Bars

Each entry in Part II has a colored bar on the left edge of its header block. These color bars serve as visual anchors, making it easy to locate entry boundaries when scanning through pages.

The colors indicate entry type:

| Color | Entry Type | Description |
|-------|------------|-------------|
| **Red** | Instruction | PASM2 machine instructions (the majority of entries) |
| **Amber** | Directive | Assembler directives like ORG, BYTE, LONG |
| **Violet** | Constant | Pre-defined constants like smart pin mode values |

The color bar spans the three-line identity block at the top of each entry:

1. **Mnemonic** --- The instruction, directive, or constant name
2. **Expansion** --- What the mnemonic stands for (e.g., "Add Signed, Extended")
3. **Category** --- The functional category with a brief description

When flipping through Part II, these color bars help you quickly identify entry boundaries and distinguish between instructions, directives, and constants.

### 2.8.3 Example: Understanding ADD

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

### 2.8.4 Using Categories for Discovery

Instructions are grouped by category in Appendix B. When looking for "an instruction that does X," consult the categorical index:

- **Math Instructions:** ADD, SUB, MUL, etc.
- **Logic Instructions:** AND, OR, XOR, etc.
- **Branch/Jump Instructions:** JMP, CALL, DJNZ, etc.
- **Hub Memory Instructions:** RDLONG, WRLONG, etc.

### 2.8.5 Using Related Instructions

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

Each COG has access to a shared FIFO buffer that can operate in either read mode or write mode (not both simultaneously). The FIFO contains (cogs+11) stages—with all 8 COGs active, this provides 19 stages of buffering. When in read mode, the FIFO loads continuously whenever fewer than (cogs+7) stages are filled, after which up to 5 more longs may stream in, potentially filling all stages. These metrics ensure the FIFO never underflows under any reading scenario.

**Setting Up the Read FIFO:**

RDFAST configures the FIFO for reading from hub memory. The D operand provides a block count (number of 64-byte blocks before wrapping), and the S operand provides the starting hub address:

```pasm
        rdfast  #0, ptr                 ' Start continuous read FIFO
loop
        rflong  data                    ' Read from FIFO (fast, no hub wait)
        ' ... process data ...
        jmp     #loop                   ' Continue reading
```

The RFLONG, RFWORD, and RFBYTE instructions read from the FIFO without waiting for hub windows—if data is available in the FIFO buffer, the read completes immediately. The FIFO refills automatically in the background using whatever hub windows become available.

**Wait Mode vs. No-Wait Mode:**

RDFAST and WRFAST each have two modes controlled by bit 31 of the D operand:

| D[31] | Behavior |
|-------|----------|
| 0 | Wait for any previous WRFAST to finish, then reconfigure FIFO. For RDFAST, also wait until FIFO begins receiving data. Ready to use immediately after instruction completes. |
| 1 | No-wait mode—takes only 2 clocks. Code must allow sufficient time before accessing FIFO data. |

The no-wait mode is useful when you need to reconfigure the FIFO quickly and can guarantee enough cycles will pass before the first FIFO access.

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

**Important:** If a COG has been writing to hub via WRFAST and wants to immediately COGSTOP itself, execute `WAITX #20` first to allow time for any lingering FIFO data to be written to hub memory.

**Circular Buffer Mode:**

The FIFO supports circular buffer operation for continuous streaming. When configured with a non-zero block count, the FIFO wraps back to the starting address after transferring the specified number of 64-byte blocks:

```pasm
        rdfast  #16, audio_buffer       ' Read 16 blocks (1KB), then wrap
```

For wrapping mode, the hub start address must be long-aligned (address ends in %00) since there won't be an extra cycle to read/write a partial long at block boundaries. Use 0 for block count when you don't want wrapping—the FIFO will sequence through the entire 1MB hub map before wrapping.

**Dynamic Buffer Management with FBLOCK:**

The FBLOCK instruction provides dynamic control over the FIFO's wrap behavior. It sets a new start address and block count that take effect when the current blocks are fully read or written:

```pasm
        rdfast  #16, buffer_a           ' Start reading from buffer A
        ' ... reading proceeds ...
        fblock  #16, buffer_b           ' Queue buffer B for when A completes
        ' ... FIFO seamlessly transitions to buffer B on wrap
```

FBLOCK can be executed after RDFAST, WRFAST, or a FIFO block wrap event. Coordinating FBLOCK with streamer activity enables dynamic, seamless streaming between hub RAM and pins/DACs—essential for continuous audio/video output where buffer switches must be glitch-free.

**Variable-Length Data: RFVAR and RFVARS:**

For bytecode interpreters and compact data formats, RFVAR and RFVARS read 1-4 bytes of variable-length encoded data from the FIFO. The encoding uses the MSB of each byte to indicate whether more bytes follow:

| First Byte | Additional Bytes | RFVAR Returns | RFVARS Returns |
|------------|------------------|---------------|----------------|
| %0xxxxxxx | none | 7-bit value, zero-extended | 7-bit value, sign-extended |
| %1xxxxxxx | 1 more (%0xxxxxxx) | 14-bit value, zero-extended | 14-bit value, sign-extended |
| %1xxxxxxx | 2 more | 21-bit value, zero-extended | 21-bit value, sign-extended |
| %1xxxxxxx | 3 more | 28-bit value, zero-extended | 28-bit value, sign-extended |

This encoding provides memory-efficient storage for bytecode constants and offset addresses—small values use 1 byte, larger values expand as needed. RFVAR returns unsigned (zero-extended) values; RFVARS returns signed (sign-extended) values.

**FIFO Events:**

The FIFO generates events that programs can monitor for buffer management:

- **EVENT_FBW** (FIFO Block Wrap) signals when the FIFO wraps around in circular buffer mode. Programs use this event to know when to refill the next section of a circular buffer or to synchronize with buffer boundaries.

Programs can wait for this event using WAITSE or poll it using POLLSE after configuring a selectable event source. This enables efficient ping-pong buffering where one COG fills buffers while another consumes them.

**Hub Execution Restriction:**

The FIFO cannot be used while the COG is executing from hub RAM. During hub execution mode, the FIFO hardware is dedicated to spooling instructions, so these instructions cannot be used:

- RDFAST / WRFAST / FBLOCK
- RFBYTE / RFWORD / RFLONG / RFVAR / RFVARS
- WFBYTE / WFWORD / WFLONG
- XINIT / XZERO / XCONT (when streamer mode engages the FIFO)

To use FIFO operations, ensure your code executes from COG or LUT RAM.

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

The CORDIC is a fully pipelined, shared resource accessed through hub rotation—the same arbitration mechanism used for hub RAM. Each COG receives a CORDIC access slot every 8 clock cycles. With a 54-stage pipeline and 8-clock access intervals, a single COG can have 6-7 operations in flight simultaneously (54 ÷ 8 ≈ 6.75). This deep pipelining enables sustained high throughput when processing multiple values.

### 5.1.4 The Pipeline Phases

Effective CORDIC usage follows a three-phase pattern: fill, steady-state, and drain.

**Fill Phase:** Submit multiple operations before expecting any results. During this phase, you queue operations without retrieving results, filling the pipeline:

```pasm
        ' Fill phase - queue first 6 operations
        qmul    a0, b0                      ' Operation 0 enters pipeline
        qmul    a1, b1                      ' Operation 1 (8 clocks later)
        qmul    a2, b2                      ' Operation 2
        qmul    a3, b3                      ' Operation 3
        qmul    a4, b4                      ' Operation 4
        qmul    a5, b5                      ' Operation 5
        ' Pipeline now filling, first result not ready yet
```

**Steady-State Phase:** Once the pipeline fills, retrieve one result and submit one new operation each access slot. This phase achieves maximum throughput—one result per 8 clocks:

```pasm
        ' Steady state - retrieve previous, submit next
.loop   getqx   result_lo                   ' Get result from ~54 clocks ago
        getqy   result_hi
        qmul    a_next, b_next              ' Submit next operation
        ' ... process result, prepare next operands ...
        djnz    count, #.loop
```

**Drain Phase:** After submitting the final operation, continue retrieving remaining results without submitting new operations:

```pasm
        ' Drain phase - retrieve final results
        getqx   result_lo                   ' Get remaining results
        getqy   result_hi
        ' ... repeat for each operation still in pipeline ...
```

### 5.1.5 Result Retrieval Timing

The GETQX and GETQY instructions retrieve results in submission order. If a result is not yet ready when GETQX or GETQY executes, the COG stalls until the result becomes available. This automatic stalling simplifies programming—you need not count cycles precisely—but can impact performance if you retrieve too early.

For non-blocking result checking, use POLLQMT to test whether the CORDIC pipeline is empty:

```pasm
        pollqmt             wc              ' C=1 if pipeline empty, C=0 if results pending
        if_nc getqx result                  ' Only retrieve if results available
```

The CORDIC generates Event 15 when GETQX or GETQY executes with no results available. This event can trigger an interrupt or be polled, useful for detecting programming errors where retrieval occurs before any operations were queued.

### 5.1.6 Practical Pipelining Example

This example processes an array of coordinate pairs, rotating each by a fixed angle. The pipeline keeps multiple rotations in flight:

```pasm
' Rotate 16 coordinate pairs by angle
' Input: point_array (pairs of X,Y longs), angle
' Output: rotated coordinates written back to array
rotate_points
        mov     count, #16
        mov     ptra, ##point_array         ' Read pointer
        mov     ptrb, ##point_array         ' Write pointer (same array)

        ' Fill phase - start first 6 rotations
        call    #queue_rotation             ' Queue op 0
        call    #queue_rotation             ' Queue op 1
        call    #queue_rotation             ' Queue op 2
        call    #queue_rotation             ' Queue op 3
        call    #queue_rotation             ' Queue op 4
        call    #queue_rotation             ' Queue op 5
        sub     count, #6

        ' Steady state - retrieve one, queue one
.loop   getqx   rotated_x                   ' Get previous result
        getqy   rotated_y
        wrlong  rotated_x, ptrb++           ' Store result
        wrlong  rotated_y, ptrb++
        call    #queue_rotation             ' Queue next
        djnz    count, #.loop

        ' Drain phase - retrieve final 6 results
        rep     @.drain_end, #6
        getqx   rotated_x
        getqy   rotated_y
        wrlong  rotated_x, ptrb++
        wrlong  rotated_y, ptrb++
.drain_end
        ret

' Helper: queue one rotation from point array
queue_rotation
        rdlong  x, ptra++
        rdlong  y, ptra++
        setq    y                           ' Y coordinate to Q register
        qrotate x, angle                    ' Start rotation
        ret
```

This pattern achieves one rotation result every ~20 instructions (the loop body), rather than waiting 54 clocks per rotation. For 16 points, the pipelined version completes in roughly 320 clocks versus 864 clocks for sequential processing—nearly 3× faster.

### 5.1.7 CORDIC Instructions Reference

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


## 5.6 XBYTE Bytecode Engine

The P2 includes a hardware bytecode execution engine called XBYTE that accelerates interpreted languages and virtual machines. Traditional software interpreters spend 20-40 clock cycles dispatching each bytecode—reading the bytecode, looking up a handler address, and jumping to the handler. XBYTE reduces this overhead to just 6 clock cycles through dedicated hardware that automates the fetch-lookup-dispatch cycle. This acceleration makes the P2 practical for running bytecode interpreters at speeds approaching native code performance.

### 5.6.1 XBYTE Operation

XBYTE operates by reading bytecodes from the hub FIFO and using each bytecode as an index into a lookup table stored in LUT RAM. Each LUT entry contains a routine address and optional skip pattern. The hardware automatically fetches the bytecode, retrieves the corresponding LUT entry, and dispatches to the routine using EXECF—all in 6 clock cycles plus the routine's own execution time.

XBYTE is like a phantom instruction that executes on a hardware stack return (RET/\_RET\_) to address $1FF. Such a return does not pop the stack, so each additional RET/\_RET\_ causes another bytecode to be fetched and executed. This creates a continuous interpretation loop with minimal overhead.

The execution cycle proceeds through eight clock phases:

| Clock | Phase | Activity | Description |
|-------|-------|----------|-------------|
| 1 | go | RFBYTE bytecode, SKIPF #0 | Fetch bytecode from FIFO, cancel any prior skip pattern |
| 2 | get | MOV PA,bytecode, RDLUT | Write bytecode to PA ($1F6), start LUT read |
| 3 | go | RDLUT (data → D) | Complete LUT read, get routine address and skip pattern |
| 4 | get | EXECF D (begin) | Start EXECF dispatch |
| 5 | go | MOV PB,(GETPTR), MODCZ, EXECF D (branch) | Write FIFO pointer to PB ($1F7), optionally set C/Z, branch |
| 6 | get | flush pipeline | Pipeline flush for branch |
| 7 | go | reload pipeline | Pipeline reload |
| 8 | get | first instruction | First instruction of bytecode routine executes |

When a bytecode routine completes and returns, XBYTE automatically fetches the next bytecode and repeats the cycle. The bytecode stream flows continuously from hub memory through the FIFO, enabling sustained interpretation without explicit fetching in the bytecode routines themselves. The bytecode routine could be as short as a single 2-clock instruction with a \_RET\_ prefix, making the total XBYTE loop take only 8 clocks.

### 5.6.2 LUT Table Format

The bytecode translation table in LUT memory consists of long values that EXECF uses for dispatch. Each 32-bit LUT entry contains two fields:

- **Bits [9:0]**: Jump address in COG/LUT RAM ($000-$3FF)
- **Bits [31:10]**: SKIPF pattern (22 bits) applied after the jump

When XBYTE dispatches to a bytecode routine, EXECF simultaneously jumps to the routine address and applies the skip pattern. This allows compact bytecode routines where common instruction sequences are shared and skip patterns select which instructions execute.

### 5.6.3 Configuration Options

XBYTE supports multiple configuration modes that trade bytecode count against LUT space requirements. The SETQ/SETQ2 D value controls the mode:

| Bits | SETQ D Pattern | LUT Base | Index Calculation | Bytecodes |
|------|----------------|----------|-------------------|-----------|
| 8 | %A0000000F | %A00000000 | I = bytecode[7:0] | 256 |
| 7 | %AAxx0010F | %AA0000000 | I = bytecode[6:0] | 128 |
| 7 | %AAxx0011F | %AA0000000 | I = bytecode[7:1] | 128 |
| 6 | %AAAx1010F | %AAA000000 | I = bytecode[5:0] | 64 |
| 6 | %AAAx1011F | %AAA000000 | I = bytecode[7:2] | 64 |
| 5 | %AAAAx100F | %AAAA00000 | I = bytecode[4:0] | 32 |
| 5 | %AAAAx101F | %AAAA00000 | I = bytecode[7:3] | 32 |
| 4 | %AAAAA110F | %AAAAA0000 | I = bytecode[3:0] | 16 |
| 4 | %AAAAA111F | %AAAAA0000 | I = bytecode[7:4] | 16 |

The A bits specify the LUT base address where the dispatch table begins. The full 256-bytecode mode uses the entire LUT for dispatch tables. Smaller modes leave LUT space available for other purposes—data tables, waveforms, or additional code.

A compressed mode (%ABBBB00xF where BBBB > 0) provides efficient handling of bytecode families:

- If bytecode[7:4] < BBBB: Use full bytecode as index (individual handlers)
- If bytecode[7:4] >= BBBB: Use bytecode[7:4] - BBBB as index (shared handlers)

This allows 16 primary bytecodes with full dispatch plus up to 240 extended bytecodes using shared handlers, balancing bytecode variety against LUT consumption. When bytecodes share a handler, the full bytecode value in PA differentiates behavior within the routine.

### 5.6.4 Flag Control

The F bit (bit 0) of the SETQ/SETQ2 D value controls whether XBYTE writes the bytecode's index bits to the C and Z flags:

| F Bit | Behavior |
|-------|----------|
| 0 | Do not affect flags on XBYTE dispatch |
| 1 | Write bytecode index bit 1 to C, bit 0 to Z |

This flag option allows bytecode routines to receive up to 4 states encoded in the flag bits, enabling compact opcode families. For example, four related bytecodes can share a single routine that uses conditional execution based on C and Z to differentiate behavior—useful for cases where a SKIPF pattern alone would be insufficient.

### 5.6.5 Starting XBYTE

XBYTE mode begins through a specific instruction sequence. First, push $1FF onto the hardware stack, then execute \_RET\_ SETQ to configure the mode and trigger XBYTE:

```pasm
                                        ' Setup before starting XBYTE:
        setq2   #256-1                  ' Load 256 longs into LUT
        rdlong  $100, #bytetable        ' Bytecode table at LUT $100

        rdfast  #0, #bytecodes          ' Init FIFO at bytecode stream

        push    #$1FF                   ' Push $1FF for XBYTE returns
_RET_   setq    #$100                   ' Start XBYTE: LUT base=$100, 256 bytecodes
```

The \_RET\_ SETQ instruction both configures XBYTE mode and returns to $1FF, which triggers the first bytecode fetch. Each bytecode routine ends with RET or \_RET\_, returning to $1FF to fetch the next bytecode.

To alter the XBYTE mode for all subsequent bytecodes, execute another \_RET\_ SETQ instruction within a bytecode routine. To alter the mode for the next bytecode only, use \_RET\_ SETQ2 instead—the original mode automatically restores after one bytecode. This is useful for engaging singular bytecodes from alternate sets without having to restore the original mode afterward.

### 5.6.6 Bytecode Routine Requirements

Bytecode routines must follow these constraints:

- **Location**: Must reside in COG RAM ($000-$1FF) or LUT RAM ($200-$3FF)
- **Exit**: Must end with RET or \_RET\_ to return control to XBYTE
- **Stack**: Hardware stack must not overflow (8 levels maximum)

The PA register ($1F6) contains the current bytecode value, available as an immediate operand within routines. The PB register ($1F7) contains the FIFO read pointer, enabling routines to track their position in the bytecode stream or read inline parameters following the bytecode using RFBYTE, RFWORD, or RFLONG.

For maximum performance, use the \_RET\_ prefix on the final instruction:

```pasm
toggle_pin0
_RET_   drvnot  #0                      ' Toggle pin 0, return to XBYTE (2 clocks)
```

This executes in just 2 clocks, making the complete XBYTE cycle only 8 clocks total.

### 5.6.7 XBYTE Applications

XBYTE enables efficient implementation of virtual machines and interpreters. Java bytecode interpreters, Forth threaded code systems, BASIC interpreters, and custom scripting languages all benefit from the reduced dispatch overhead. At 160 MHz, XBYTE can dispatch over 26 million bytecodes per second (considering only dispatch overhead), making interpreted languages practical for real-time applications.

| Dispatch Method | Overhead | Relative Speed |
|-----------------|----------|----------------|
| Software dispatch | 20-40 clocks | 1× (baseline) |
| XBYTE dispatch | 6 clocks | 3-7× faster |

XBYTE is particularly effective for:

- **Virtual machines**: Java, Python, or custom bytecode interpreters
- **Threaded interpreters**: Forth direct/indirect threaded code
- **Command processors**: Parsing and executing token streams
- **Compression**: Executing compressed instruction sequences
- **Protocol handling**: Processing token-based communication protocols


## 5.7 Boot Process

When the P2 powers on or receives a hardware reset, it begins a deterministic boot sequence that loads and executes user code. Understanding this sequence is essential for embedded applications—it explains why programs must configure the clock, how the chip finds your code, and what state the hardware is in when your program starts executing.

### 5.7.1 Initial Chip State

At reset, the P2 initializes to a known state before any user code executes:

| Resource | Initial State |
|----------|---------------|
| Clock source | RCFAST (~20-25 MHz internal RC oscillator) |
| All COGs | Stopped (except COG 0) |
| Hub RAM | Undefined contents |
| I/O pins | High-impedance (floating) |
| 64-bit counter | Cleared to zero |
| PRNG | Seeded with thermal noise |

The internal RC oscillator (RCFAST) provides the initial clock. This oscillator is guaranteed to run at least 20 MHz under all conditions, ensuring reliable serial communication during boot. The exact frequency varies with temperature and manufacturing, typically 20-25 MHz. Programs requiring precise timing must configure an external crystal or the PLL after boot.

The boot ROM seeds the Xoroshiro128** pseudo-random number generator with true random data. The ROM reads thermal noise from pin 63 (configured in ADC calibration mode) fifty times, using each 31-bit sample to seed the PRNG through HUBSET. This establishes high-quality randomness available immediately when user code starts—there is no need to seed the PRNG again, though programs may do so if desired.

### 5.7.2 Boot Source Selection

The P2 determines its boot source by sensing external pull-up resistors on pins P59-P61. This hardware detection occurs automatically and requires no software configuration.

| P61 | P60 | P59 | Boot Behavior |
|-----|-----|-----|---------------|
| none | none | none | Serial only (60s window) |
| pull-up | none | none | SPI flash, then serial (60s) on failure |
| pull-up | pull-up | none | SPI flash only (fast boot), shutdown on failure |
| none | pull-up | none | SD card, then serial (60s) on failure |
| none | pull-up | pull-down | SD card only, shutdown on failure |
| pull-up | ignored | ignored | Serial override (60s window) |

The pull-up detection uses internal sensing—no software reads these pins. The boot ROM checks pin states immediately after reset and branches to the appropriate loader. Development boards typically include jumpers or switches to select boot mode; production designs hard-wire the appropriate resistor configuration.

### 5.7.3 Boot Pin Assignments

The boot process uses pins P58-P63 for communication with external boot sources:

**Serial Boot (P62-P63):**

| Pin | Function | Direction |
|-----|----------|-----------|
| P63 | Serial RX | Input |
| P62 | Serial TX | Output |

**SPI Flash Boot (P58-P61):**

| Pin | Function | Direction |
|-----|----------|-----------|
| P61 | Chip Select (active low) | Output |
| P60 | Clock | Output |
| P59 | Data Out (MOSI) | Output |
| P58 | Data In (MISO) | Input |

**SD Card Boot (P58-P61):**

| Pin | Function | Direction |
|-----|----------|-----------|
| P61 | Chip Select (directly active low) | Output |
| P60 | Clock | Output |
| P59 | Data Out (MOSI) | Output |
| P58 | Data In (MISO) | Input |

After boot completes, these pins return to general-purpose I/O. Programs can reconfigure them for any purpose once execution begins.

### 5.7.4 The Boot Sequence

After reset, COG 0 loads and executes the boot ROM program (ROM_Booter.spin2). The boot sequence proceeds as follows:

**Step 1: Check for SPI Flash**

If an external pull-up is detected on P61, the booter attempts SPI flash boot:

1. Load the first 1024 bytes (256 longs) from SPI flash into hub RAM at $00000
2. Compute the 32-bit sum of these 256 longs
3. If the sum equals "Prop" ($706F7250), the data is valid:
   - Copy the 256 longs from hub to COG 0 registers $000-$0FF
   - If P60 also has a pull-up: execute immediately (`JMP #$000`)
   - Otherwise: wait for serial commands (100ms timeout), then execute

**Step 2: Serial Loader Window**

If SPI boot is not configured or fails checksum validation, the booter enters serial loader mode:

1. Wait for serial commands on P63 (RX pin)
2. Auto-detect baud rate from incoming data (9600 to 2,000,000 baud)
3. Accept commands for up to 60 seconds
4. If a valid program loads: execute via `COGINIT #0,#0`
5. If timeout expires with no valid program: switch to RCSLOW (~20 kHz) and halt COG 0

**Step 3: Program Execution**

Once valid code is loaded, the booter launches it:

- For SPI/SD boot: `JMP #$000` executes code now in COG 0's registers
- For serial boot: `COGINIT #0,#0` relaunches COG 0 from hub address $00000

In both cases, user code begins executing with the clock still in RCFAST mode. The program must configure the desired clock source if different timing is required.

### 5.7.5 Serial Loading Protocol

The serial loader provides a text-based protocol for loading code during development. The protocol auto-detects baud rate by measuring bit timing from received characters, supporting rates from 9,600 to 2,000,000 baud.

**Auto-Baud Detection:**

The loader calibrates timing from ">" characters ($3E) in the data stream. Send "> " (greater-than followed by space) before the first command and periodically throughout data to maintain accurate baud detection against the drifting internal RC oscillator.

**Commands:**

| Command | Purpose |
|---------|---------|
| `Prop_Chk` | Verify communication, returns chip version |
| `Prop_Clk` | Configure clock source before loading |
| `Prop_Hex` | Load program data in hexadecimal format |
| `Prop_Txt` | Load program data in Base64 format |

Each command includes mask fields for selecting specific chips when multiple P2s share a serial bus. For single-chip loading, use zero masks: `Prop_Chk 0 0 0 0`.

**Data Validation:**

Loaded programs must include a validation header. The loader computes a 32-bit sum of all loaded longs; if the sum equals "Prop" ($706F7250), the data is considered valid and execution proceeds. Compilers and loaders automatically generate this checksum.

### 5.7.6 Clock Configuration After Boot

User code starts executing with the RCFAST clock source—an internal RC oscillator running approximately 20-25 MHz. For applications requiring precise timing, configure an external crystal or the PLL early in your program:

```pasm
' Configure 20 MHz crystal with PLL for 160 MHz operation
                hubset  ##%0000_0001_0000_0000_0000_0000_00_10    ' Enable crystal, 15pF caps
                waitx   ##20_000_000/100                          ' Wait 10ms for crystal
                hubset  ##%0000_0001_0000_0000_0000_0000_10_10    ' Switch to crystal
                hubset  ##%0000_0001_0000_1000_0000_0010_00_10    ' PLL: /1 * 8 / 1 = 160MHz
                waitx   ##20_000_000/10000                        ' Wait 100µs for PLL lock
                hubset  ##%0000_0001_0000_1000_0000_0010_00_11    ' Switch to PLL output
```

The ASMCLK directive provides a convenient shorthand when using standard crystal configurations. It generates the appropriate HUBSET sequence based on the _clkfreq and _clkmode constants defined in your program.

**Why Clock Setup Is Required:**

The boot ROM cannot know what clock source your hardware provides. Some boards use 20 MHz crystals, others use 25 MHz, and some applications run directly from the internal oscillator. By starting in RCFAST mode, the P2 boots reliably on any hardware. Your program then configures the actual clock source appropriate for your design.

### 5.7.7 Rebooting from Software

The HUBSET instruction can trigger a hardware reset, returning the chip to the boot sequence:

```pasm
                hubset  ##$1000_0000                ' Generate reset pulse, reboot chip
```

This performs a full hardware reset—all COGs stop, all I/O returns to high-impedance, the clock reverts to RCFAST, and the boot ROM executes from the beginning. Use this for implementing watchdog recovery, firmware updates, or returning to the boot loader.


## 5.8 DEBUG Output

The DEBUG statement provides built-in debugging output without requiring external serial drivers or dedicated COGs. When your program includes DEBUG statements, the compiler generates code that transmits formatted data over the serial connection to the development host. The host's debug window displays values, text, and even graphical visualizations—oscilloscope traces, plots, and logic analyzer views. This integrated debugging capability accelerates development by providing visibility into program behavior without consuming pins or writing serial communication code.

### 5.8.1 DEBUG Fundamentals

DEBUG is a compile-time directive that generates serial output code. The compiler translates each DEBUG statement into instructions that format and transmit data at runtime. When DEBUG is disabled (via compiler option), these statements generate no code, allowing debug instrumentation to remain in source code without affecting production builds.

The basic DEBUG syntax accepts text strings and formatted values:

```pasm
                debug("Hello from P2")                  ' Simple text message
                debug("Count: ", udec(counter))         ' Text with decimal value
                debug("Address: ", uhex(ptr))           ' Hexadecimal display
                debug("Flags: ", ubin(status))          ' Binary display
```

DEBUG output appears in the development environment's debug window—a terminal-style display that shows messages as they arrive. The serial connection typically runs at 2 Mbaud, providing high-throughput debugging without significant timing impact.

### 5.8.2 Value Formatters

DEBUG provides formatters for displaying values in different numeric bases and formats. Each formatter follows a consistent naming pattern: the base prefix (U for unsigned, S for signed) followed by the radix (DEC, HEX, BIN).

| Formatter | Output Format | Example Output |
|-----------|---------------|----------------|
| UDEC | Unsigned decimal | `counter = 42` |
| SDEC | Signed decimal | `temperature = -25` |
| UHEX | Hexadecimal with $ | `address = $0400` |
| SHEX | Signed hexadecimal | `offset = -$20` |
| UBIN | Binary with % | `flags = %10110` |
| SBIN | Signed binary | `mask = -%0101` |
| FDEC | Floating point | `voltage = 3.14159` |

**The Underscore Convention:** Each formatter has a variant with an underscore suffix that outputs only the value, omitting the variable name:

```pasm
                debug(udec(count))                      ' Output: count = 42
                debug(udec_(count))                     ' Output: 42
                debug("Items: ", udec_(count))          ' Output: Items: 42
```

The underscore variants enable clean custom formatting. Without the underscore, formatters automatically include the variable name—useful for quick inspection but awkward when building custom output strings.

### 5.8.3 Sized Formatters

Each formatter supports size suffixes that control the display width and value interpretation:

| Suffix | Bit Width | Unsigned Range | Signed Range |
|--------|-----------|----------------|--------------|
| _BYTE | 8 bits | 0–255 | -128 to 127 |
| _WORD | 16 bits | 0–65535 | -32768 to 32767 |
| _LONG | 32 bits | 0–4294967295 | Full 32-bit |

Sized formatters ensure consistent output width and proper sign extension:

```pasm
                debug(uhex_byte(value))                 ' 2 hex digits: $xx
                debug(uhex_word(value))                 ' 4 hex digits: $xxxx
                debug(uhex_long(value))                 ' 8 hex digits: $xxxxxxxx
                debug(ubin_byte(flags))                 ' 8 binary digits
```

### 5.8.4 Array Formatters

DEBUG can display multiple consecutive values using array formatters. These combine a base formatter with an array type suffix:

```pasm
                debug(uhex_byte_array(@buffer, 16))     ' 16 bytes in hex
                debug(udec_word_array(@samples, 8))     ' 8 words in decimal
                debug(uhex_long_array(@data, 4))        ' 4 longs in hex
                debug(udec_reg_array(@regs, 10))        ' 10 COG registers
```

Array formatters display values separated by commas, providing quick inspection of memory regions and data buffers. The `@` operator provides the address; the second parameter specifies the count.

### 5.8.5 Special Formatters

Beyond numeric values, DEBUG supports several special-purpose formatters:

**String Display:**

```pasm
                debug(zstr(@message))                   ' Zero-terminated string
                debug(lstr(@text, length))              ' Length-specified string
```

**Boolean and Flag Display:**

```pasm
                debug(bool(enabled))                    ' Displays TRUE or FALSE
                debug(c_z)                              ' Shows C and Z flag values
```

**Conditional Output:**

```pasm
                debug(if(error_flag), "Error detected") ' Only outputs if condition true
                debug(ifnot(ready), "Not ready")        ' Only outputs if condition false
```

### 5.8.6 Visual Debug Displays

Beyond text output, DEBUG supports graphical display windows that visualize data in real time. These displays open automatically when the corresponding DEBUG statement executes.

**SCOPE — Oscilloscope Display:**

The SCOPE display provides multi-channel waveform visualization, similar to a digital oscilloscope:

```pasm
.loop           rdlong  adc_value, adc_ptr
                debug(`scope MySignal, adc_value)
                waitms  #1
                jmp     #.loop
```

SCOPE supports up to 8 channels, auto-scaling, triggering modes, and time base adjustment. Each DEBUG call adds one sample point; the display scrolls as new data arrives.

**PLOT — Data Plotting:**

The PLOT display creates line graphs, scatter plots, and trend charts:

```pasm
.loop           call    #read_temperature
                debug(`plot Temperature, temp_value)
                waitms  #1000
                jmp     #.loop
```

PLOT provides rolling or accumulating display modes, multiple data series, and statistical overlays including moving averages and min/max envelopes.

**TERM — Terminal Display:**

The TERM display provides a dedicated text terminal window, separate from the default debug output:

```pasm
                debug(`term Status, "System initialized", 13)
                debug(`term Status, "Temperature: ", sdec_(temp), "°C", 13)
```

TERM supports control characters (13 for newline, 9 for tab, 12 for clear screen) and provides a scrolling text buffer.

**LOGIC — Logic Analyzer:**

The LOGIC display shows digital signal timing as a logic analyzer view:

```pasm
.loop           rdbyte  port_state, port_addr
                debug(`logic PortA, port_state)
                waitx   ##100
                jmp     #.loop
```

LOGIC displays multiple digital channels with timing relationships, useful for debugging communication protocols and state machines.

**BITMAP — Pixel Display:**

The BITMAP display renders pixel data as an image:

```pasm
                debug(`bitmap Display, 320, 240, @framebuffer)
```

BITMAP creates a window showing raw pixel data, useful for graphics and video debugging.

### 5.8.7 Practical DEBUG Patterns

**Watching Values in Loops:**

```pasm
.loop           rdlong  sensor, sensor_addr
                debug(sdec(sensor))                     ' Shows each reading
                call    #process_data
                djnz    count, #.loop
```

**Conditional Debug Output:**

```pasm
                cmp     error_code, #0          wz
        if_nz   debug("Error: ", udec_(error_code), " at ", uhex_(location))
```

**Timing Measurement:**

```pasm
                getct   start_time
                call    #function_under_test
                getct   end_time
                sub     end_time, start_time
                debug("Execution time: ", udec_(end_time), " clocks")
```

**Multi-Value Inspection:**

```pasm
                debug("X:", sdec_(x), " Y:", sdec_(y), " Z:", sdec_(z))
```

**Memory Dump:**

```pasm
                debug("Buffer contents:", 13)
                debug(uhex_byte_array_(@buffer, 32))
```

### 5.8.8 DEBUG Performance Considerations

DEBUG statements execute at runtime, consuming clock cycles for formatting and serial transmission. While typically negligible for occasional debug output, intensive debugging can affect timing-critical code.

**Timing Impact:**

- Each DEBUG statement requires cycles for formatting and transmission
- Serial transmission at 2 Mbaud limits throughput
- Visual displays (SCOPE, PLOT) add host-side processing

**Mitigation Strategies:**

- Use conditional DEBUG to output only when conditions warrant
- Remove or disable DEBUG in timing-critical inner loops
- Use the compiler's debug-disable option for production builds
- Aggregate multiple values into single DEBUG statements

**Production Builds:**

The compiler provides options to disable DEBUG entirely. When disabled, DEBUG statements compile to nothing—no code generated, no runtime impact. This allows debug instrumentation to remain in source code, ready for future debugging sessions, without affecting production performance.

### 5.8.9 DEBUG and Multi-COG Programs

When multiple COGs execute DEBUG statements, output interleaves in the debug window. Each COG's output appears as it transmits, which can create confusing mixed output when COGs debug simultaneously.

**Strategies for Multi-COG Debugging:**

- Prefix messages with COG identification: `debug("COG", udec_(cog_id), ": message")`
- Use separate TERM windows for each COG: `debug(`term COG0, ...)`, `debug(`term COG1, ...)`
- Add brief delays between DEBUG calls in different COGs
- Debug one COG at a time during initial development

The debug interrupt (a hidden fourth interrupt level) coordinates DEBUG access across COGs, ensuring atomic message transmission, but message ordering depends on execution timing.


```{=latex}
\begin{keyconcepts}
\item The CORDIC coprocessor provides 54-cycle hardware math (multiply, divide, sqrt, trig)
\item Smart Pins are 64 programmable I/O peripherals with local state machines
\item The Streamer enables DMA-like high-speed data movement
\item Events provide non-interrupt notification; interrupts are available when needed
\item 16 hardware locks enable safe inter-COG synchronization
\item XBYTE provides 6-cycle bytecode dispatch for interpreters and virtual machines
\item The P2 boots from RCFAST (\textasciitilde20 MHz) and detects boot source via pin pull-ups
\item Serial, SPI flash, and SD card boot modes support different deployment scenarios
\item User code must configure the desired clock source after boot
\item DEBUG provides built-in serial output with formatters and visual displays
\item Visual DEBUG displays include oscilloscope, plot, logic analyzer, and bitmap views
\item DEBUG can be disabled for production builds with zero runtime overhead
\item The 8-COG architecture often eliminates the need for interrupts
\item Each subsystem is controlled through dedicated PASM2 instructions
\end{keyconcepts}
```


<!-- End of Chapter 5 -->
