# Chapter 1: The P2 Execution Model

<!-- Chapter establishing the foundational mental model for the P2 architecture -->

The Propeller 2 microcontroller implements a unique multi-processor architecture that differs fundamentally from conventional microcontrollers. Understanding this architecture is essential for effective PASM2 programming.


## 1.1 The Eight-COG Architecture

```{=latex}
\EightCogSimpleDiagram
```

::: {.figurecaption #fig:eight-cog-overview}
Figure 1.1: Eight-COG Architecture Overview
:::

The P2 contains eight identical processors called COGs (Cog Processors). Each COG:

- Executes instructions independently and simultaneously
- Has its own dedicated 512-long register file
- Operates at full clock speed with deterministic timing
- Shares access to a common Hub memory

### 1.1.1 COG Independence

Unlike conventional microcontrollers that use time-slicing or task switching, the P2 implements true parallel execution. Each COG runs at full clock speed simultaneously with all other COGs. There is no scheduler, no context switching overhead, and no need for traditional interrupts to handle multiple tasks.

This architecture provides deterministic timing. The same code executing on a COG takes exactly the same number of clock cycles every time it runs. This predictability makes the P2 ideal for real-time applications such as video generation, motor control, and protocol implementation where precise timing is essential.

Each COG operates independently. One COG can execute a tight control loop while another manages communications and a third handles user interface tasks. All eight COGs run simultaneously without interfering with each other's timing.

### 1.1.2 COG Identification

Each COG has a unique identifier from 0 to 7. A COG can determine its own identifier using the `COGID` instruction, which writes the COG number to the destination register. This capability allows the same code to run on multiple COGs while behaving differently based on COG identity.

COGs can communicate with each other through shared Hub memory, hardware locks, and attention signals. The `COGATN` instruction allows one COG to signal other COGs through hardware attention flags, providing fast inter-COG notification without polling shared memory locations.

### 1.1.3 Starting and Stopping COGs

The `COGINIT` instruction starts a new COG or restarts an existing one. COGINIT specifies which COG to start (0-7), where the code resides in Hub memory, and optionally passes a parameter to the new COG. The parameter value appears in the new COG's PTRB register, providing a simple mechanism for initialization data.

The `COGSTOP` instruction halts a running COG. A COG can stop itself or another COG by specifying the target COG number. Stopped COGs consume no power and can be restarted later with different code.


## 1.2 COG Memory

```{=latex}
\CogMemoryMapDiagram
```

::: {.figurecaption #fig:cog-memory-map}
Figure 1.2: COG Memory Map
:::

Each COG has 512 longs (2048 bytes) of dedicated RAM addressed from $000 to $1FF. This memory is private to each COG and provides single-cycle read and write access. Unlike Hub memory, COG memory stores 32-bit longs only and uses long-addressing rather than byte-addressing.

### 1.2.1 General Purpose Registers ($000-$1EF)

The first 496 longs ($000-$1EF) serve as general-purpose registers available for code and data storage. In PASM2, these locations function as registers rather than traditional memory. Instructions specify source and destination operands by register address, and the assembler translates symbolic names to these addresses.

Programs can use this space flexibly. A small program might dedicate most of the space to data storage and lookup tables. A larger program uses more space for code and less for data. The programmer controls this allocation through the assembler's ORG directive and RES directive for reserving data space.

Registers $1D8-$1DF have predefined symbols PR0-PR7 for Spin2 interoperability. For standalone PASM2 programs, these are ordinary general-purpose registers. See Part II: Special Registers for details on Spin2/PASM2 communication.

### 1.2.2 Special Purpose Registers ($1F0-$1FF)

The final 16 registers have dedicated hardware functions. Registers $1F0-$1F7 (IJMP3/IRET3, IJMP2/IRET2, IJMP1/IRET1, PA, PB) serve dual purposes: they function as interrupt vectors and call/return storage when those features are enabled, or as general-purpose RAM otherwise. Registers $1F8-$1FF (PTRA, PTRB, DIRA, DIRB, OUTA, OUTB, INA, INB) are fixed special registers that always provide their hardware I/O and pointer functions.

For complete documentation of each register, see Part II: Special Registers and Appendix C: Special Registers Quick Reference.

### 1.2.3 Register Addressing

PASM2 instructions use 9-bit fields to specify source (S) and destination (D) register addresses. Nine bits provide 512 possible values, addressing the complete COG RAM space from $000 to $1FF. The instruction encoding dedicates specific bit positions to these address fields, and the assembler automatically encodes symbolic register names into the appropriate bit patterns.


## 1.3 LUT Memory

```{=latex}
\LutMemoryMapDiagram
```

::: {.figurecaption #fig:lut-memory-map}
Figure 1.3: LUT Memory Map
:::

Each COG has a dedicated 512-long Lookup Table (LUT) providing additional fast memory separate from the main COG RAM space. The LUT serves as auxiliary storage for lookup tables, waveform data, additional code space, or working memory.

### 1.3.1 LUT Characteristics

LUT memory occupies a separate address space from COG RAM, addressed at $200-$3FF relative to COG addressing. Programs access LUT through dedicated RDLUT and WRLUT instructions. RDLUT takes 3 clock cycles and WRLUT takes 2 cycles—both faster than Hub access but slower than direct COG register operations. This separation doubles the available fast memory per COG from 512 longs to 1024 longs total.

LUT RAM can also execute code at the same speed as COG RAM (2 clocks per instruction), making it valuable "overflow" code space when programs exceed COG RAM capacity. When the program counter is in the range $200-$3FF, the COG fetches instructions from LUT memory with the same deterministic timing as COG execution.

The LUT integrates with the P2's streamer and cordic subsystems. The streamer can directly output LUT contents to pins for waveform generation, and cordic operations can store results in LUT memory. This integration makes the LUT particularly valuable for signal generation and digital signal processing applications. A common application is paletted VGA display, where the LUT stores a 256-color palette and the streamer translates 8-bit pixel values to RGB output in real-time.

### 1.3.2 LUT Instructions

`RDLUT` reads a value from LUT memory to a COG register. `WRLUT` writes a value from a COG register to LUT memory. These instructions work similarly to regular COG memory operations but target the separate LUT address space.

Programs often load the LUT with data from Hub memory at initialization using `SETQ` for burst transfers, then access the LUT repeatedly during time-critical operations. This pattern keeps frequently-accessed data in fast LUT memory while larger datasets remain in Hub memory.

### 1.3.3 LUT Sharing Between COGs

```{=latex}
\EightCogEggbeaterDiagram
```

::: {.figurecaption #fig:eight-cog-lut-sharing}
Figure 1.4: Eight-COG Architecture with LUT Write Sharing
:::

The `SETLUTS` instruction activates write-sharing of LUT memory between adjacent COG pairs. When a COG executes `SETLUTS #1`, the paired COG's `WRLUT` writes are copied into this COG's LUT via the LUT's second port. This is one-directional; for two-way mirroring both COGs of the pair must execute `SETLUTS #1`. Adjacent pairs are COGs 0-1, 2-3, 4-5, and 6-7. Each COG retains its own 512-long LUT; SETLUTS activates cross-COG write access rather than expanding LUT size. This feature supports producer-consumer patterns where one COG generates data that another COG consumes, eliminating the need to transfer data through Hub memory.


## 1.4 Hub Memory

```{=latex}
\HubMemoryLayoutDiagram
```

::: {.figurecaption #fig:hub-memory-map}
Figure 1.5: Hub Memory Layout: Spin2+PASM vs PASM-Only Programs
:::

The Hub provides 512KB of shared RAM accessible by all COGs. Unlike COG memory, Hub memory is byte-addressable and stores programs, data, and resources shared among COGs.

### 1.4.1 Hub Address Space

Hub memory spans addresses $00000 through $7FFFF, providing 524,288 bytes of storage. All eight COGs can read and write any location in this space. Hub memory stores bytes, words (16-bit), and longs (32-bit) with appropriate address alignment.

Programs use Hub memory to share data between COGs, store large lookup tables, hold program code for Hub execution mode, and buffer data for I/O operations. Each COG accesses Hub memory through dedicated Hub instructions that handle shared access timing.

Hub memory organization is application-defined. Programs allocate space according to their requirements—there is no fixed layout imposed by hardware. Different applications use different organizations: some reserve specific regions for communication buffers, others dedicate areas to code overlays, and boot loaders may use particular addresses for compatibility.

⚠️ **Pitfall:** Hub addresses below $400 overlap with the region from which COGs load initial code during COGINIT. Writing to this area while COGs are being started can cause unpredictable behavior. Programs that dynamically start COGs should avoid using low hub addresses for shared data storage.

### 1.4.2 Hub Access Timing

Hub RAM is divided into eight "slices"—one per COG. Each slice holds every eighth long in the composite Hub RAM address space. On every clock cycle, each COG can access the "next" RAM slice in sequence. This arrangement supports continuous bidirectional streaming of 32 bits per clock for sequential addresses.

When a COG accesses a specific Hub address, it must wait up to 7 clocks to reach the initial RAM slice of interest. Once aligned, subsequent sequential locations can be accessed on every clock thereafter for continuous reading or writing of 32-bit longs. This slice architecture differs fundamentally from P1's rotating hub window and provides substantially higher sustained bandwidth.

The hardware FIFO smooths out data flow for non-sequential or variable-rate access. The FIFO can be configured for hub-RAM-read or hub-RAM-write operation, allowing sequential transfers in any combination of bytes, words, or longs at rates up to one long per clock. The FIFO maintains proper hub slice alignment without programmer intervention.

Hub read instructions (RDBYTE/RDWORD/RDLONG) take 9-16 clocks in COG/LUT execution mode (9-26 in Hub execution mode). Hub write instructions (WRBYTE/WRWORD/WRLONG) take 3-10 clocks in COG/LUT mode (3-20 in Hub execution mode). All ranges are egg-beater hub-window dependent. Hub control instructions (HUBSET, COGINIT, LOCK*, CORDIC) have different timing of 2-9 clocks.

Despite the variable initial wait, hub timing remains deterministic. The maximum wait is always seven clocks, and once aligned, sequential access proceeds at one long per clock. Programs requiring precise timing use COG execution mode for critical sections and Hub memory for data storage and inter-COG communication.

### 1.4.3 Hub Instructions

PASM2 provides six primary instructions for Hub memory access. `RDBYTE` reads a byte, `RDWORD` reads a word, and `RDLONG` reads a long from Hub memory to a COG register. `WRBYTE`, `WRWORD`, and `WRLONG` write the corresponding data sizes from a COG register to Hub memory.

The `SETQ` instruction enhances Hub access efficiency by configuring burst transfers to COG RAM. SETQ followed by a Hub read instruction loads multiple consecutive values in a single operation, amortizing the Hub window wait time across many transfers. Similarly, `SETQ2` configures burst transfers to LUT RAM—use SETQ2 before RDLONG/WRLONG to transfer blocks directly between Hub and LUT memory.

For high-bandwidth streaming, `RDFAST` and `WRFAST` configure the hardware FIFO for continuous Hub transfers. The FIFO prefetches data in the background, hiding Hub access latency from the program. `FBLOCK` provides dynamic control over FIFO buffer boundaries for seamless ping-pong buffering. These streaming instructions are documented in detail in Chapter 4.

Other hub-related instructions include lock instructions (`LOCKNEW`, `LOCKRET`, `LOCKTRY`, `LOCKREL`) for inter-COG synchronization, `HUBSET` for clock and system configuration, and `SETLUTS` for LUT sharing configuration between adjacent COGs.

The CORDIC coprocessor also interacts with Hub memory. CORDIC operations can read operands from and write results to Hub addresses, enabling efficient processing of large datasets stored in Hub RAM.


## 1.5 The Execution Pipeline

The P2 implements a five-stage pipelined execution architecture. When the pipeline is full, each instruction effectively takes as little as two clock cycles to execute, providing high throughput while maintaining predictable timing.

Most instructions complete in two clock cycles once the pipeline fills. The first instruction through the pipeline takes five clocks to reach completion. Once the pipeline is full, subsequent instructions complete at a rate of one per two clocks, giving an effective throughput of one instruction every two clocks in steady-state execution.

Hub memory instructions add variable delays waiting for Hub access windows. The hub access rotation means a Hub instruction might execute immediately or wait up to seven clocks for its COG's access slot. This variability affects only Hub memory operations; pure COG operations maintain consistent two-clock timing.

When executing from Hub RAM (Hub execution mode), the COG uses its FIFO hardware to prefetch instructions rather than rotating hub access. The FIFO queues instructions ahead of execution, providing smoother instruction flow. However, this dedicates the FIFO to instruction fetch, making it unavailable for RDFAST/WRFAST streaming operations during Hub execution.

Branch instructions incur additional overhead when taken. A conditional branch that is not taken completes in two clocks like other instructions. A taken branch causes the pipeline to be flushed, so the first instruction following the branch takes at least five clock cycles as the pipeline refills from the branch target address.

The P2 handles data dependencies internally through forwarding logic. An instruction that depends on the result of the immediately preceding instruction receives the correct value without requiring explicit programmer intervention or NOP insertion. This hardware forwarding removes a major class of pipeline hazards present in simpler architectures (see Chapter 4 for timing detail).

Register indirection instructions (ALTS, ALTD, ALTR, ALTB, ALTI) perform dynamic instruction modification within the pipeline. These instructions substitute computed addresses or values into the next instruction's source, destination, or result fields without modifying the actual program code in memory. The next instruction following any ALT instruction is shielded from interrupts, guaranteeing atomic execution of the ALT+target instruction pair. This pipeline-level modification supports powerful indirect addressing patterns while maintaining deterministic timing.


## 1.6 Execution Modes

The P2 supports three execution modes based on the program counter address, each offering different trade-offs between speed and capacity. Programs can use any mode exclusively or mix all three modes within a single application.

| Mode | PC Range | Characteristics |
|------|----------|----------------|
| COG Execution | $00000-$001FF | Fastest, 2 clocks/instruction, 512 longs |
| LUT Execution | $00200-$003FF | Fast, 2 clocks/instruction, 512 longs overflow |
| Hub Execution | $00400-$7FFFF | Largest capacity, variable timing, uses FIFO |

### 1.6.1 COG Execution Mode

COG execution mode runs code from COG RAM (PC in range $000-$1FF). Instructions execute in the consistent two-clock pipeline with no additional delays. This mode provides the fastest possible execution and deterministic timing, making it ideal for time-critical code such as communication protocols, motor control loops, and signal generation.

COG execution mode limits programs to the available COG RAM space. After accounting for special registers and data storage, typically 200-400 longs remain for code. Programs that fit in this space achieve maximum performance. Larger programs can overflow into LUT execution or use Hub execution mode.

### 1.6.2 LUT Execution Mode

LUT execution mode runs code from LUT RAM (PC in range $200-$3FF). Instructions execute at the same speed as COG execution—two clocks per instruction with deterministic timing. LUT execution effectively doubles the available fast code space from 512 to 1024 longs per COG.

LUT execution is ideal for overflow code that doesn't fit in COG RAM but requires deterministic timing. The COG fetches instructions from LUT memory with no additional delays beyond the standard pipeline. There are no special considerations when branching between COG and LUT addresses.

Time-critical inner loops often execute in COG or LUT mode even when the main program runs from Hub memory. The program loads critical code sections to COG/LUT RAM, executes the loop, then returns to Hub-based code. This hybrid approach combines the performance of local execution with the capacity of Hub storage.

### 1.6.3 Hub Execution Mode

Hub execution mode runs code directly from Hub RAM without loading it to COG memory first. The COG fetches instructions from Hub memory using the FIFO hardware to prefetch and queue instructions for continuous execution. This is distinct from the hub rotation used for random-access data transfers. The FIFO provides smoother instruction flow but adds variable delay compared to COG mode.

Hub execution mode provides access to the full 512KB Hub address space, enabling programs far larger than COG memory could hold. In practice, Hub-executed code typically resides at addresses $400 and above—the `ORGH` directive defaults to $400, reserving low addresses for COG initialization data. The mode suits applications where code size exceeds available COG RAM and deterministic timing is less critical. User interface code, data processing algorithms, and high-level control logic typically run well in Hub execution mode.

`COGINIT` determines execution mode when starting a COG. The initialization parameter specifies either COG execution (code loaded from Hub to COG RAM, then executed) or Hub execution (code executed directly from Hub RAM). The `ORGH` assembler directive marks code intended for Hub execution, while `ORG` marks code for COG execution.

⚠️ **Pitfall:** While executing from Hub RAM, the FIFO hardware is dedicated to instruction prefetch and cannot be used for other purposes. The following instructions are unavailable during Hub execution: RDFAST, WRFAST, FBLOCK, RFBYTE, RFWORD, RFLONG, RFVAR, RFVARS, WFBYTE, WFWORD, WFLONG, and the streamer FIFO instructions XINIT, XZERO, and XCONT when the streamer mode engages the FIFO. Code requiring these instructions must execute from COG RAM.

### 1.6.4 Switching Between Modes

Programs switch between execution modes using `CALL` or `JMP` instructions. A COG executing from COG RAM can call or jump to Hub addresses, and Hub-executing code can call or jump to COG addresses. The program counter determines current mode: addresses $000-$3FF indicate COG/LUT execution, while higher addresses indicate Hub execution.

The hardware handles mode transitions transparently. The programmer specifies the target address, and the COG switches to the appropriate execution mode based on the address range. This seamless transition supports hybrid programs that place performance-critical code in COG RAM while maintaining larger program logic in Hub RAM.


```{=latex}
\begin{keyconcepts}
\item The P2 has 8 independent COGs executing in true parallel
\item Each COG has 512 longs of private RAM plus 512 longs of private LUT
\item Hub memory (512KB) is shared among all COGs with deterministic access timing
\item Special registers at \$1F0-\$1FF provide hardware I/O functions
\item COGs can execute from COG RAM (fast), LUT RAM (fast), or Hub RAM (larger capacity)—three distinct execution modes
\item Hub execution uses FIFO for instruction prefetch; FIFO instructions unavailable in Hub mode
\item The pipeline provides two-clock execution for most instructions
\item No interrupts are required due to true parallel execution; however, complete interrupt mechanisms are provided
\end{keyconcepts}
```


<!-- End of Chapter 1 -->

