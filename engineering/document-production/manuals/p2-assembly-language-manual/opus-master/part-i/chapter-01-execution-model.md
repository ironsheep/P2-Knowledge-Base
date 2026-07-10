# Chapter 1: The P2 Execution Model

The Propeller 2 microcontroller implements a unique multi-processor architecture that differs fundamentally from conventional microcontrollers. Understanding this architecture is essential for effective PASM2 programming.


## 1.1 The Eight-Cog Architecture

```{=latex}
\EightCogSimpleDiagram
```

::: {.figurecaption #fig:eight-cog-overview}
Figure 1.1: Eight-Cog Architecture Overview
:::

The P2 contains eight identical processors called cogs (Cog Processors). Each cog:

- Executes instructions independently and simultaneously
- Has its own dedicated 512-long register file
- Operates at full clock speed with deterministic timing
- Shares access to a common hub memory

### 1.1.1 Cog Independence

Unlike conventional microcontrollers that use time-slicing or task switching, the P2 implements true parallel execution: there is no scheduler, no context-switching overhead, and no need for interrupts to share the processor among tasks.

This architecture provides deterministic timing. The same code executing on a cog takes exactly the same number of clock cycles every time it runs. This predictability supports real-time work where instruction timing must be exact.

One cog can run a tight control loop while another manages communications and a third handles the user interface, with no cog affecting another's timing.

Cogs are independent in execution and timing, but they share one hub; random hub access costs up to seven clocks to align (§1.4.2), so time-critical inner loops keep their working set in cog or LUT RAM.

### 1.1.2 Cog Identification

Each cog has a unique identifier from 0 to 7. A cog can determine its own identifier using the `COGID` instruction, which writes the cog number to the destination register. This capability allows the same code to run on multiple cogs while behaving differently based on cog identity.

Cogs can communicate with each other through shared hub memory, hardware locks, and attention signals. The `COGATN` instruction allows one cog to signal other cogs through hardware attention flags, providing fast inter-cog notification without polling shared memory locations.

### 1.1.3 Starting and Stopping Cogs

The `COGINIT` instruction starts a new cog or restarts an existing one. COGINIT specifies which cog to start (0-7), where the code resides in hub memory, and optionally passes a parameter to the new cog. The start address is written to the new cog's PTRB register; the optional parameter—supplied via a `SETQ` executed immediately before COGINIT—is written to the new cog's PTRA register, providing a simple mechanism for initialization data.

The `COGSTOP` instruction halts a running cog. A cog can stop itself or another cog by specifying the target cog number. Stopped cogs consume no power and can be restarted later with different code.


## 1.2 Cog Memory

```{=latex}
\CogMemoryMapDiagram
```

::: {.figurecaption #fig:cog-memory-map}
Figure 1.2: Cog Memory Map
:::

Each cog has 512 longs (2048 bytes) of dedicated RAM addressed from $000 to $1FF. This memory is private to each cog and provides single-cycle read and write access. Unlike hub memory, cog memory stores 32-bit longs only and uses long-addressing rather than byte-addressing.

### 1.2.1 General Purpose Registers ($000-$1EF)

The first 496 longs ($000-$1EF) serve as general-purpose registers available for code and data storage. In PASM2, these locations function as registers rather than traditional memory. Instructions specify source and destination operands by register address, and the assembler translates symbolic names to these addresses.

Programs can use this space flexibly. A small program might dedicate most of the space to data storage and lookup tables. A larger program uses more space for code and less for data. The programmer controls this allocation through the assembler's ORG directive and RES directive for reserving data space.

Registers $1D8-$1DF have predefined symbols PR0-PR7 for Spin2 interoperability. For standalone PASM2 programs, these are ordinary general-purpose registers. See Part II: Special Registers for details on Spin2/PASM2 communication.

### 1.2.2 Special Purpose Registers ($1F0-$1FF)

The final 16 registers have dedicated hardware functions. Registers $1F0-$1F7 (IJMP3/IRET3, IJMP2/IRET2, IJMP1/IRET1, PA, PB) serve dual purposes: they function as interrupt vectors and call/return storage when those features are enabled, or as general-purpose RAM otherwise. Registers $1F8-$1FF (PTRA, PTRB, DIRA, DIRB, OUTA, OUTB, INA, INB) are fixed special registers that always provide their hardware I/O and pointer functions.

For complete documentation of each register, see Part II: Special Registers and Appendix D: Special Registers Quick Reference.

### 1.2.3 Register Addressing

PASM2 instructions use 9-bit fields to specify source (S) and destination (D) register addresses. Nine bits provide 512 possible values, addressing the complete cog RAM space from $000 to $1FF. The instruction encoding dedicates specific bit positions to these address fields, and the assembler automatically encodes symbolic register names into the appropriate bit patterns.


## 1.3 LUT Memory

```{=latex}
\LutMemoryMapDiagram
```

::: {.figurecaption #fig:lut-memory-map}
Figure 1.3: LUT Memory Map
:::

Each cog has a dedicated 512-long Lookup Table (LUT) providing additional fast memory separate from the main cog RAM space. The LUT serves as auxiliary storage for lookup tables, waveform data, additional code space, or working memory. Because cog RAM doubles as the register file, it is a cog's most constrained resource; the LUT gives each cog a second 512-long fast space for data tables and overflow code, so plan the split between them early in a design.

### 1.3.1 LUT Characteristics

LUT memory occupies a separate address space from cog RAM, addressed at $200-$3FF relative to cog addressing. Programs access LUT through dedicated RDLUT and WRLUT instructions. RDLUT takes 3 clock cycles and WRLUT takes 2 cycles—both faster than hub access. WRLUT matches the speed of a direct cog-register operation (2 clocks), while RDLUT is one clock slower. This separation doubles the available fast memory per cog from 512 longs to 1024 longs total.

LUT RAM can also execute code at the same speed as cog RAM (2 clocks per instruction), making it valuable "overflow" code space when programs exceed cog RAM capacity. When the program counter is in the range $200-$3FF, the cog fetches instructions from LUT memory with the same deterministic timing as cog execution.

The LUT integrates with the P2's streamer and CORDIC subsystems. The streamer can output LUT contents to pins for waveform generation, and CORDIC operations can store results in LUT memory. For example, in paletted VGA display the LUT holds a 256-color palette and the streamer translates 8-bit pixel values to RGB output in real time.

### 1.3.2 LUT Instructions

`RDLUT` reads a value from LUT memory to a cog register. `WRLUT` writes a value from a cog register to LUT memory. These instructions work similarly to regular cog memory operations but target the separate LUT address space.

**Pitfall:** A literal LUT address reaches only the lower half—`RDLUT d, #0` through `RDLUT d, #255`. `RDLUT d, #256` and above do not assemble (the compiler reports `Constant must be from 0 to 255`). To reach any of the 512 LUT longs, use a register holding the address, or a `PTRA`/`PTRB` pointer with an optional index: `RDLUT d, addr` or `RDLUT d, PTRB[4]`. The 9-bit address field's top bit selects the pointer form, so a plain literal spans only 8 bits; pointers carry the full range.

Programs often load the LUT with data from hub memory at initialization using `SETQ` for burst transfers, then access the LUT repeatedly during time-critical operations. This pattern keeps frequently-accessed data in fast LUT memory while larger datasets remain in hub memory.

### 1.3.3 LUT Sharing Between Cogs

```{=latex}
\EightCogEggbeaterDiagram
```

::: {.figurecaption #fig:eight-cog-lut-sharing}
Figure 1.4: Eight-Cog Architecture with LUT Write Sharing
:::

The `SETLUTS` instruction activates write-sharing of LUT memory between adjacent cog pairs. When a cog executes `SETLUTS #1`, the paired cog's `WRLUT` writes are copied into this cog's LUT via the LUT's second port. This is one-directional; for two-way mirroring both cogs of the pair must execute `SETLUTS #1`. Adjacent pairs are cogs 0-1, 2-3, 4-5, and 6-7. Each cog retains its own 512-long LUT; SETLUTS activates cross-cog write access rather than expanding LUT size. This supports producer-consumer patterns: one cog writes data the paired cog reads directly, without a hub round-trip.


## 1.4 Hub Memory

```{=latex}
\HubMemoryLayoutDiagram
```

::: {.figurecaption #fig:hub-memory-map}
Figure 1.5: Hub Memory Layout: Spin2+PASM vs PASM-Only Programs
:::

The hub provides 512KB of shared RAM accessible by all cogs. Unlike cog memory, hub memory is byte-addressable and stores programs, data, and resources shared among cogs.

### 1.4.1 Hub Address Space

Hub memory spans addresses $00000 through $7FFFF, providing 524,288 bytes of storage. All eight cogs can read and write any location in this space. Hub memory stores bytes, words (16-bit), and longs (32-bit) with appropriate address alignment.

Programs use hub memory to share data between cogs, store large lookup tables, hold program code for hub execution mode, and buffer data for I/O operations. Each cog accesses hub memory through dedicated hub instructions that handle shared access timing.

Hub memory organization is application-defined. Programs allocate space according to their requirements—there is no fixed layout imposed by hardware. Different applications use different organizations: some reserve specific regions for communication buffers, others dedicate areas to code overlays, and boot loaders may use particular addresses for compatibility.

**Pitfall:** Hub addresses below $400 overlap with the region from which cogs load initial code during COGINIT. Writing to this area while cogs are being started can cause unpredictable behavior. Programs that dynamically start cogs should avoid using low hub addresses for shared data storage.

### 1.4.2 Hub Access Timing

Hub RAM is divided into eight "slices"—one per cog. Each slice holds every eighth long in the composite hub RAM address space. On every clock cycle, each cog can access the "next" RAM slice in sequence. This arrangement supports continuous bidirectional streaming of 32 bits per clock for sequential addresses.

When a cog accesses a specific hub address, it must wait up to 7 clocks to reach the initial RAM slice of interest. Once aligned, subsequent sequential locations can be accessed on every clock thereafter for continuous reading or writing of 32-bit longs. This slice architecture differs fundamentally from P1's rotating hub window and provides substantially higher sustained bandwidth.

The hardware FIFO smooths out data flow for non-sequential or variable-rate access. The FIFO can be configured for hub-RAM-read or hub-RAM-write operation, allowing sequential transfers in any combination of bytes, words, or longs at rates up to one long per clock. The FIFO maintains proper hub slice alignment without programmer intervention.

Hub read instructions (RDBYTE/RDWORD/RDLONG) take 9-16 clocks in cog/LUT execution mode (9-26 in hub execution mode). Hub write instructions (WRBYTE/WRWORD/WRLONG) take 3-10 clocks in cog/LUT mode (3-20 in hub execution mode). All ranges are egg-beater hub-window dependent. Hub control instructions (HUBSET, COGINIT, LOCK*, CORDIC) have different timing of 2-9 clocks (LOCKNEW takes 4-11).

Despite the variable initial wait, hub timing remains deterministic. The maximum wait is always seven clocks, and once aligned, sequential access proceeds at one long per clock. Programs requiring precise timing use cog execution mode for critical sections and hub memory for data storage and inter-cog communication.

### 1.4.3 Hub Instructions

PASM2 provides six primary instructions for hub memory access. `RDBYTE` reads a byte, `RDWORD` reads a word, and `RDLONG` reads a long from hub memory to a cog register. `WRBYTE`, `WRWORD`, and `WRLONG` write the corresponding data sizes from a cog register to hub memory.

The `SETQ` instruction enhances hub access efficiency by configuring burst transfers to cog RAM. SETQ followed by a hub read instruction loads multiple consecutive values in a single operation, amortizing the hub window wait time across many transfers. Similarly, `SETQ2` configures burst transfers to LUT RAM—use SETQ2 before RDLONG/WRLONG to transfer blocks directly between hub and LUT memory.

For high-bandwidth streaming, `RDFAST` and `WRFAST` configure the hardware FIFO for continuous hub transfers. The FIFO prefetches data in the background, hiding hub access latency from the program. `FBLOCK` provides dynamic control over FIFO buffer boundaries for ping-pong buffering. These streaming instructions are documented in detail in Chapter 4.

Other hub-related instructions include lock instructions (`LOCKNEW`, `LOCKRET`, `LOCKTRY`, `LOCKREL`) for inter-cog synchronization, `HUBSET` for clock and system configuration, and `SETLUTS` for LUT sharing configuration between adjacent cogs.

The CORDIC coprocessor also interacts with hub memory. CORDIC operations can read operands from and write results to hub addresses, enabling efficient processing of large datasets stored in hub RAM.

### 1.4.4 Moving Hub Data: the Cog and the Streamer

The hub instructions above are *cog-driven*: the cog issues each RDLONG or WRLONG and waits for its hub window, so the transfer occupies—blocks—the cog while it runs. A SETQ burst (§1.4.3) is the fast cog-driven path, moving one long per clock after the initial window. Wrapping a transfer loop in a `REP` block (Chapter 4) makes it interrupt-atomic: REP shields its repeated instructions from interrupts—including debug interrupts that ordinary masking cannot hold off—so the whole block runs uninterrupted, at the cost of added interrupt latency for its duration.

Alongside this cog-driven path, each cog has its own **streamer**: a small engine that moves data between hub memory and the pins, DACs, or ADC inputs on its own, at a rate the program sets, without the cog's further involvement. If you have used DMA before, the streamer is a close cousin of a DMA channel—with the additions that it paces transfers to an exact rate and can reshape data as it moves; if you have not, it is simply hardware that moves a stream of data while the cog does other work. The streamer shares the cog's FIFO with hub execution and the RDFAST/WRFAST instructions, so only one of those uses is active at a time. The streamer is covered in Chapter 4 and, in depth, in the *P2 Streamer Programming Guide*.


## 1.5 The Execution Pipeline

The P2 implements a five-stage pipelined execution architecture. When the pipeline is full, each instruction effectively takes as little as two clock cycles to execute, providing high throughput while maintaining predictable timing.

Most instructions complete in two clock cycles once the pipeline fills. The first instruction through the pipeline takes five clocks to reach completion. Once the pipeline is full, subsequent instructions complete at a rate of one per two clocks, giving an effective throughput of one instruction every two clocks in steady-state execution.

Hub memory instructions add variable delays waiting for hub access windows. The hub access rotation means a hub instruction might execute immediately or wait up to seven clocks for its cog's access slot. This variability affects only hub memory operations; pure cog operations maintain consistent two-clock timing.

When executing from hub RAM (hub execution mode), the cog uses its FIFO hardware to prefetch instructions rather than rotating hub access. The FIFO queues instructions ahead of execution, providing smoother instruction flow. However, this dedicates the FIFO to instruction fetch, making it unavailable for RDFAST/WRFAST streaming operations during hub execution.

Branch instructions incur additional overhead when taken. A conditional branch that is not taken completes in two clocks like other instructions. A taken branch causes the pipeline to be flushed, so the first instruction following the branch takes at least five clock cycles as the pipeline refills from the branch target address.

The P2 handles data dependencies internally through forwarding logic. An instruction that depends on the result of the immediately preceding instruction receives the correct value without requiring explicit programmer intervention or NOP insertion. This hardware forwarding removes a major class of pipeline hazards present in simpler architectures (see Chapter 4 for timing detail).

Register indirection instructions (ALTS, ALTD, ALTR, ALTB, ALTI) perform dynamic instruction modification within the pipeline. These instructions substitute computed addresses or values into the next instruction's source, destination, or result fields without modifying the actual program code in memory. The next instruction following any ALT instruction is shielded from interrupts, guaranteeing atomic execution of the ALT+target instruction pair. This pipeline-level modification supports indirect addressing patterns while maintaining deterministic timing.


## 1.6 Execution Modes

The P2 names three execution modes by the program counter's address range. The first two—cog execution and LUT execution—are mechanically identical: both run from the cog's own RAM at a fixed two clocks per instruction with no FIFO involved, and the program counter rolls from cog RAM straight into LUT RAM (from $1FF to $200) with no branch and no penalty. Treat them as one contiguous 1024-long fast execution space. The real divide is the third mode—hub execution—where the cog fetches instructions through the FIFO and timing becomes variable. Most programs combine the fast cog/LUT space with hub execution—time-critical code in cog/LUT, bulk code in hub—moving between them by branching (§1.6.3).

| Mode | PC Range | Characteristics |
|------|----------|----------------|
| Cog Execution | $00000-$001FF | Fast: 2 clocks/instruction, 512 longs |
| LUT Execution | $00200-$003FF | Fast: 2 clocks/instruction, continuous with cog RAM |
| Hub Execution | $00400-$7FFFF | Largest capacity, variable timing, uses FIFO |

Cog and LUT execution differ only in which half of the fast space holds the code; they carry no speed or behavioral distinction, and branching freely between them costs nothing. What changes performance is crossing into hub execution: a branch to a hub address takes at least 13 clocks while the FIFO refills and the pipeline reloads. The `REP` instruction sidesteps even ordinary branch overhead—it repeats a block of cog or LUT instructions with no per-iteration branch at all (Chapter 4).

### 1.6.1 Cog and LUT Execution

Cog execution runs code from cog RAM (PC in $000-$1FF) in the consistent two-clock pipeline with no added delay—the fastest, most deterministic execution the P2 offers, and the home a cog boots into. After special registers and data storage, typically 200-400 of the 512 longs remain for code.

When a program outgrows that space, the LUT is its seamless extension. LUT execution runs code from LUT RAM (PC in $200-$3FF) at the identical two clocks per instruction, doubling the fast code space to 1024 longs per cog. The program counter rolls from $1FF straight into $200, and branching between cog and LUT addresses carries no special consideration—the two are one contiguous fast space. The hardware reflects this: a cog's boot-mode status records only whether it started in hub execution or in cog/LUT execution, with no separate state for the LUT. Use LUT execution for overflow code that must keep deterministic timing.

Time-critical inner loops often run in cog or LUT even when the main program lives in hub memory: the program loads the critical section into cog/LUT RAM, runs the loop at full speed, then returns to hub-based code—combining local-execution performance with hub capacity.

### 1.6.2 Hub Execution Mode

Hub execution mode runs code directly from hub RAM without loading it to cog memory first. The cog fetches instructions from hub memory using the FIFO hardware to prefetch and queue instructions for continuous execution. This is distinct from the hub rotation used for random-access data transfers. The FIFO provides smoother instruction flow but adds variable delay compared to cog mode.

Hub execution mode provides access to the full 512KB hub address space, enabling programs far larger than cog memory could hold. In practice, hub-executed code typically resides at addresses $400 and above—the `ORGH` directive defaults to $400, reserving low addresses for cog initialization data. The mode suits applications where code size exceeds available cog RAM and deterministic timing is less critical. User interface code, data processing algorithms, and high-level control logic typically run well in hub execution mode.

`COGINIT` determines execution mode when starting a cog. The initialization parameter specifies either cog execution (code loaded from hub to cog RAM, then executed) or hub execution (code executed directly from hub RAM). The `ORGH` assembler directive marks code intended for hub execution, while `ORG` marks code for cog execution.

**Pitfall:** While executing from hub RAM, the FIFO hardware is dedicated to instruction prefetch and cannot be used for other purposes. The following instructions are unavailable during hub execution: RDFAST, WRFAST, FBLOCK, RFBYTE, RFWORD, RFLONG, RFVAR, RFVARS, WFBYTE, WFWORD, WFLONG, and the streamer FIFO instructions XINIT, XZERO, and XCONT when the streamer mode engages the FIFO. Code requiring these instructions must execute from cog RAM.

### 1.6.3 Switching Between Modes

Programs switch between execution modes using `CALL` or `JMP` instructions. A cog executing from cog RAM can call or jump to hub addresses, and hub-executing code can call or jump to cog addresses. The program counter determines current mode: addresses $000-$3FF indicate cog/LUT execution, while higher addresses indicate hub execution.

The hardware handles mode transitions transparently. The programmer specifies the target address, and the cog switches to the appropriate execution mode based on the address range. This lets hybrid programs place performance-critical code in cog RAM while keeping larger program logic in hub RAM.


```{=latex}
\begin{keyconcepts}
\item The P2 has 8 independent cogs executing in true parallel
\item Each cog has 512 longs of private RAM plus 512 longs of private LUT
\item Hub memory (512KB) is shared among all cogs with deterministic access timing
\item Special registers at \$1F0-\$1FF provide hardware I/O functions
\item Cog RAM and LUT RAM form one contiguous fast execution space (2 clocks/instruction); hub RAM adds capacity at variable, FIFO-paced timing
\item Hub execution uses FIFO for instruction prefetch; FIFO instructions unavailable in Hub mode
\item The pipeline provides two-clock execution for most instructions
\item No interrupts are required due to true parallel execution; however, complete interrupt mechanisms are provided
\end{keyconcepts}
```

