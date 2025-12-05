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

#### Parameter Registers ($1D8-$1DF)

Within the general-purpose range, registers $1D8-$1DF have predefined names PR0-PR7 for Spin2/PASM2 interoperability:

| Address | Register | Purpose |
|:--------|:---------|:------------------------------------------------|
| $1D8 | PR0 | Parameter/result register 0 |
| $1D9 | PR1 | Parameter/result register 1 |
| $1DA | PR2 | Parameter/result register 2 |
| $1DB | PR3 | Parameter/result register 3 |
| $1DC | PR4 | Parameter/result register 4 |
| $1DD | PR5 | Parameter/result register 5 |
| $1DE | PR6 | Parameter/result register 6 |
| $1DF | PR7 | Parameter/result register 7 |

These registers provide a communication mechanism between Spin2 and PASM2 code running in the same COG. Spin2 methods can read and write PR0-PR7, and inline PASM2 code can access the same values. For standalone PASM2 programs or code launched into a separate COG, these are simply general-purpose registers with convenient predefined names.

### 1.2.2 Special Purpose Registers ($1F0-$1FF)

```{=latex}
\SpecialRegistersMapDiagram
```

The final 16 registers ($1F0-$1FF) have special hardware functions:

| Address | Register | Purpose |
|:--------|:---------|:------------------------------------------------|
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
