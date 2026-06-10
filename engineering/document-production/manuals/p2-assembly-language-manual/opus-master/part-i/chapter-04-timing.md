# Chapter 4: Timing and Determinism

<!-- Chapter covering clock cycles, hub windows, and deterministic timing -->

The P2 provides deterministic instruction timing, enabling precise real-time control. Understanding timing characteristics is essential for time-critical applications and optimizing code performance.


## 4.1 Clock Sources and Configuration

Before examining instruction timing, understanding clock configuration is essential—the system clock frequency determines all timing calculations. The P2 supports multiple clock sources, from simple internal oscillators to PLL-multiplied crystals running at 320 MHz.

### 4.1.1 Available Clock Sources

The P2 provides four clock source options, each suited to different application requirements:

**RCFAST** is the internal fast RC oscillator, running at 20 MHz or higher (nominally ~24 MHz, characterized 20-30 MHz across process, voltage, and temperature). This is the default clock source at power-on and reset. RCFAST requires no external components and provides immediate operation, though its frequency varies with temperature and process. Use RCFAST for applications where precise timing is not critical or as a bootstrap clock while configuring a more accurate source.

**RCSLOW** is the internal slow RC oscillator, running at approximately 20 kHz. This ultra-low-power clock serves sleep modes and real-time clock applications. RCSLOW frequency varies significantly with temperature (±50%), making it unsuitable for precision timing but ideal for power-sensitive applications.

**Crystal oscillator** mode connects an external crystal (typically 10-20 MHz) between the XI and XO pins. The P2 includes internal feedback resistors and programmable loading capacitors, simplifying crystal circuit design. Crystal sources provide the stability needed for precise timing, communication protocols, and frequency synthesis.

**External clock** mode accepts an external clock signal on the XI pin, supporting frequencies up to the device's rated system-clock maximum (180 MHz typical, 320 MHz extended per the spec sheet). Note that 350 MHz is the PLL overclock ceiling (VCO/1 mode, see §4.1.2), not the direct external-input range. This mode allows the P2 to synchronize with external timing sources or use specialized oscillators.

### 4.1.2 PLL Multiplication

The Phase-Locked Loop (PLL) multiplies a reference clock to achieve higher frequencies. The PLL takes the crystal or external clock as input and produces an output frequency according to three parameters:

- **Input divider** (1-64): Divides the reference frequency before the VCO
- **VCO multiplier** (1-1024): Multiplies to produce the VCO frequency
- **Post divider** (1, or 2-30 even): Divides the VCO output. Values 2, 4, 6...30 divide the VCO; value 1 passes VCO frequency directly (no division).

The output frequency follows the equation: f_out = (f_ref / input_div) × multiplier / post_div

For example, a 20 MHz crystal with input divider 1, multiplier 16, and post divider 2 produces: (20 MHz / 1) × 16 / 2 = 160 MHz.

The VCO operates optimally between 100-200 MHz for stability. For overclocking, the PLL can be pushed to 350 MHz using VCO/1 mode (%PPPP = 15), though stability becomes application-dependent.

### 4.1.3 The HUBSET Instruction

**Note for Spin2 Programs:** Spin2 programs typically configure the clock using CON constants (`_clkfreq`, `_xtlfreq`, `_xinfreq`). The compiler automatically generates the appropriate HUBSET calls at program initialization. Direct HUBSET use is primarily for:
- Pure PASM2 programs without Spin2
- Dynamic clock changes at runtime
- Advanced clock configurations not supported by CON constants

Clock configuration uses the HUBSET instruction with a 32-bit configuration value:

```pasm2
        hubset  ##config_value          ' Configure clock system
```

The configuration value contains fields for clock source selection, crystal configuration, and PLL parameters. The full PLL-mode layout is `%0000_xxxE_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS`:

| Bits | Field | Purpose |
|------|-------|---------|
| 1:0 | SS | Source select (RCFAST/RCSLOW/crystal/PLL) |
| 3:2 | CC | Crystal configuration (XI/XO loading and feedback) |
| 7:4 | PPPP | Post divider (value → VCO/2..30; 15 = VCO/1) |
| 17:8 | MMMMMMMMMM | VCO multiplier (1..1024 = stored value + 1) |
| 23:18 | DDDDDD | XI input divider (1..64 = stored value + 1) |
| 24 | E | PLL enable |
| 27:25, 31:28 | - | Reserved (0) |

### 4.1.4 Clock Switching Sequence

Switching clock sources requires a careful sequence to ensure glitch-free transitions:

1. **Enable the new source**: Configure crystal oscillator or PLL, but keep the current clock source active
2. **Wait for stabilization**: Crystal oscillators need approximately 10 ms to stabilize; PLL lock requires approximately 10 µs
3. **Switch sources**: Change the SS field to select the new clock source
4. **Optionally disable the old source**: Turn off unused oscillators to save power

```pasm2
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
| CORDIC operations | 2...9 (start), 55 (wait) |

Register operations like ADD, SUB, AND, and OR complete in 2 cycles whether they operate on registers or immediate values. This uniformity means that choosing between a register operand and an immediate operand has no performance impact—the decision is purely about code clarity and register pressure.

Branch instructions take 2 cycles when the branch is not taken and 4 cycles when taken. This predictable variation allows precise timing of both paths through conditional code. Programmers can eliminate this variation entirely by using conditional execution instead of branches.

Hub memory access instructions have variable timing because they must wait for the COG's hub access window. The base instruction time is 2 cycles, but the wait for hub access adds 0 to 7 additional cycles depending on when the instruction executes relative to the hub rotation pattern.

CORDIC operations use a two-phase execution model. The instruction that starts a CORDIC operation (like QMUL for multiplication) completes in 2 clocks when the COG's hub slot is current, and up to 9 clocks (2 base + up to 7 slot-wait, on an 8-COG P2) when it must wait for its hub slot. The result is not available until 55 clocks after the operation starts. Programs can perform other work during this 55-clock computation period and retrieve the result later with GETQX or GETQY.

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

The "2+" notation indicates a base time of 2 cycles plus additional variable time, where the "+" represents an instruction-specific variable delay. Hub data-access instructions are instead documented with an explicit range—RDLONG, for example, is listed as "9...16" (cog mode), the variation being the hub-window slot-wait.

Branch instructions show "2 or 4" to reflect their dual timing behavior. When the branch condition is false, the processor continues to the next instruction in 2 cycles. When the condition is true, the processor loads a new program counter and takes 4 cycles total.

The "2 / 8-23" notation distinguishes between COG execution mode and hub execution mode. In COG mode (when executing from COG RAM), the instruction takes the first number. In hub execution mode (when executing from hub RAM), the instruction takes longer because the processor must fetch each instruction through the hub access mechanism. The range "8-23" reflects the variability of hub access timing.

Variable range notation like "9..35" indicates that execution time depends on the instruction's parameters or the processor state. For example, REP (repeat) shows variable timing because the total time depends on how many iterations the repeat block executes.


## 4.3 Hub Access Timing

### 4.3.1 Hub Access Rotation

```{=latex}
\EggBeaterDiagram
```

::: {.figurecaption #fig:egg-beater}
Figure 4.1: Hub Access Rotation ("Egg Beater")
:::

Hub memory access uses round-robin arbitration that gives each COG fair access to the shared hub RAM. This rotating pattern is commonly called the "egg beater" due to its visual similarity to rotating blades, with each COG's access window spinning through the sequence in turn.

The hub controller divides time into eight-cycle periods. Within each period, every COG gets exactly one cycle to access hub memory. The access windows rotate continuously through COGs 0, 1, 2, 3, 4, 5, 6, 7, then back to COG 0, repeating this pattern indefinitely. This rotation never stops and never changes—it runs continuously from the moment the chip powers on.

When a COG executes an instruction that accesses hub memory (RDLONG, WRLONG, RDWORD, WRWORD, RDBYTE, or WRBYTE), the instruction waits until that COG's window arrives, performs the memory access during the window, then completes. The wait time depends on when the instruction executes relative to the rotation pattern.

This deterministic rotation means hub access timing is predictable. While the wait time varies from 0 to 7 cycles, the variation follows a fixed pattern. A program that knows its phase relationship to the hub rotation can achieve minimum wait times by scheduling hub access to align with its windows.

### 4.3.2 Hub Access Latency

When a COG executes a hub instruction, the actual wait time depends on timing relative to the hub rotation. Three scenarios illustrate the range of possibilities:

**Best case:** The instruction executes just as the COG's hub window arrives, with zero slot-wait. A standalone RDLONG in COG mode then completes in 9 clocks total. The 0-cycle figure is only the slot-wait *component*; the 9-clock floor reflects the hub-access pipeline (FIFO arbitration plus read latency), which a simple "2 base + 1 access" model omits.

**Worst case:** The instruction executes just after the COG's hub window has passed. The instruction must wait for the rotation to complete—seven more COGs take their turns before this COG's window comes around again. This adds 7 cycles of slot-wait, for 16 clocks total (a standalone RDLONG in COG mode). In hub-execution mode the same access ranges 9...26 clocks.

**Average case:** On average, an instruction that executes at a random time relative to the hub rotation waits 3.5 cycles of slot-wait for its hub window, landing mid-range in the 9...16 span. This average assumes no deliberate scheduling to align with windows.

The hub access latency directly impacts program performance when hub memory access is frequent. Programs that minimize hub access (by keeping frequently-accessed data in COG registers or COG RAM) avoid this latency. Programs that must access hub memory frequently achieve better performance by organizing hub access into bursts, which amortize the window wait time across multiple memory transfers.

### 4.3.3 Hub Burst Transfers

SETQ enables burst transfers that read or write multiple consecutive longs in a single hub access sequence. This feature dramatically improves hub memory throughput by eliminating the window wait time for all but the first transfer.

The SETQ instruction takes one parameter specifying how many additional longs to transfer. The hub access instruction that follows SETQ performs a burst of that many consecutive transfers:

```pasm2
        setq    #15                     ' Transfer 16 longs total
        rdlong  buffer, ptr             ' Burst read from Hub
```

This code reads 16 consecutive longs from hub memory starting at address `ptr` and stores them in COG RAM starting at address `buffer`. The first long experiences the normal hub access (9...16 clocks, including its slot-wait), but each subsequent long transfers in just one additional cycle. The whole burst completes in roughly 2 (SETQ) + 9...16 (first RDLONG) + 15 (subsequent longs) ≈ 26-33 cycles—far faster than 16 separate RDLONG instructions, each of which costs 9...16 clocks for a total on the order of 144-256 clocks (nominally ~10-12 each).

Burst transfers work because once a COG has started transferring data during its hub window, it can continue occupying subsequent windows in the rotation. The hub controller grants consecutive windows to a COG performing a burst, allowing continuous transfers without interruption.

SETQ affects only the next hub instruction. If that instruction is not a hub access instruction, SETQ has no effect (some non-hub instructions use SETQ for other purposes). After the hub instruction completes, SETQ must be reissued to enable another burst.

### 4.3.4 FIFO Operations

The P2 includes a hardware FIFO (First In, First Out) buffer that provides the highest-bandwidth method for sequential hub data transfer. Unlike individual hub access instructions that wait for hub windows, the FIFO continuously moves data between hub memory and the COG in the background. The hardware prefetches data before the COG needs it (for reads) or buffers data until hub windows become available (for writes), hiding hub access latency from the program.

**FIFO Architecture:**

Each COG has access to a shared FIFO buffer that can operate in either read mode or write mode (not both simultaneously). The FIFO contains (cogs+11) stages—with all 8 COGs active, this provides 19 stages of buffering. When in read mode, the FIFO loads continuously whenever fewer than (cogs+7) stages are filled, after which up to 5 more longs may stream in, potentially filling all stages. These metrics ensure the FIFO never underflows under any reading scenario.

**Setting Up the Read FIFO:**

RDFAST configures the FIFO for reading from hub memory. The D operand provides a block count (number of 64-byte blocks before wrapping), and the S operand provides the starting hub address:

```pasm2
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

```pasm2
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

```pasm2
        rdfast  #16, audio_buffer       ' Read 16 blocks (1KB), then wrap
```

For wrapping mode, the hub start address must be long-aligned (address ends in %00) since there won't be an extra cycle to read/write a partial long at block boundaries. Use 0 for block count when you don't want wrapping—the FIFO will sequence through the entire 1MB hub map before wrapping.

**Dynamic Buffer Management with FBLOCK:**

The FBLOCK instruction provides dynamic control over the FIFO's wrap behavior. It sets a new start address and block count that take effect when the current blocks are fully read or written:

```pasm2
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
| Hub access wait | 0-7 cycles | Loop alignment, careful scheduling |
| Branches | 2 vs 4 cycles | Conditional execution instead |
| CORDIC wait | Up to 55 clocks | Interleave other work |
| WAITX | Variable | Intentional delays |

**Hub access wait** varies from 0 to 7 cycles depending on when a hub instruction executes relative to the hub rotation. This variation is deterministic—if a program executes a hub instruction at the same point in the rotation cycle, the wait time is identical. Programs can eliminate this variation by scheduling hub access to occur at aligned points in loops, ensuring the loop body is a multiple of 8 cycles so hub access always occurs at the same phase of the rotation.

**Branch timing** varies because taken branches require 4 cycles while not-taken branches require only 2 cycles. This variation is completely predictable—the same branch decision always takes the same time. Programs can eliminate this variation by using conditional execution instead of branches, trading the variable 2-or-4-cycle branch for a fixed 2-cycle conditional instruction.

**CORDIC wait** varies because different CORDIC operations take different amounts of time to compute. Multiplication, division, square root, and trigonometric functions each have specific completion times. The variation is deterministic—the same operation always takes the same time. Programs hide CORDIC latency by issuing the operation early and performing other work during the computation period.

**WAITX** provides intentional variable delay. This is the only case where variation is desired rather than avoided—WAITX exists specifically to introduce precise, controlled timing delays for applications like bit-banging protocols or pulse generation.

### 4.4.3 Eliminating Branches

Conditional execution provides an alternative to branching that eliminates timing variation. Instead of using a compare instruction followed by a conditional jump, code can use a compare instruction followed by conditionally-executed instructions.

The branching approach introduces timing variation:

```pasm2
' With branch (2 or 4 cycles):
        cmp     a, b            wz
        if_z    jmp     #equal_case
        ' Not-equal path continues here
```

When `a` equals `b`, this code takes 2 (CMP) + 4 (JMP taken) = 6 cycles. When `a` differs from `b`, the code takes 2 (CMP) + 2 (JMP not taken) = 4 cycles. The 2-cycle variation complicates timing analysis.

The conditional execution approach provides constant timing:

```pasm2
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

```pasm2
        waitx   ##100                   ' Wait exactly 100 cycles
```

The instruction accepts a value specifying the delay duration. Execution resumes exactly after that many cycles have elapsed. This precision makes WAITX essential for timing-critical operations like bit-banging communication protocols, generating precise pulse widths, or synchronizing with external events.

WAITX delays are relative to when the instruction executes. If a program needs to generate a pulse every 1,000 cycles, using WAITX alone accumulates timing drift because the WAITX instruction itself consumes time, and the instructions between WAITX calls add additional cycles. For precise periodic timing without drift, the counter-based wait instructions provide better alternatives.

### 4.5.2 Counter-Based Waiting

The P2 provides a global cycle counter that increments every clock cycle. COGs can read this counter with GETCT and wait for specific counter values using the WAITCT family of instructions. This mechanism enables drift-free periodic timing.

Each COG has three independent counter match registers (CT1, CT2, CT3). Programs load target counter values into these registers using ADDCT1, ADDCT2, or ADDCT3, then wait for the counter to reach those values using WAITCT1, WAITCT2, or WAITCT3:

```pasm2
        getct   time                    ' Read current time
        addct1  time, ##1000            ' Set CT1 = time + 1000
        ' ... do work ...
        waitct1                         ' Wait until counter reaches CT1
```

This pattern ensures that the wait completes exactly 1,000 cycles after the GETCT instruction, regardless of how long the intervening work takes. If the work completes in 800 cycles, WAITCT1 waits 200 more cycles. If the work takes 1,200 cycles, WAITCT1 returns immediately (the deadline has already passed).

For periodic operations, adding a fixed delta to the counter match register each iteration eliminates drift:

```pasm2
        getct   time                    ' Initialize time base
loop
        addct1  time, ##1000            ' Next deadline = previous + 1000
        ' ... generate pulse or process data ...
        waitct1                         ' Wait for next period
        jmp     #loop
```

Each iteration runs exactly 1,000 cycles from the previous iteration, maintaining perfect periodicity regardless of small variations in the work performed each cycle.

### 4.5.3 Pin-Based Synchronization

Several instructions synchronize with pin state changes, enabling precise timing relative to external events:

**WAITATN** waits for any pin to make a low-to-high transition (attention flag). Smart Pins can be configured to set their ATN flags on specific conditions, making WAITATN useful for waiting on external events with minimal COG overhead.

**WAITSE1, WAITSE2, WAITSE3, WAITSE4** wait for selectable events SE1-SE4. Each is configured via the corresponding SETSE1-SETSE4 instruction to fire on a chosen source—a pin edge or level, a LUT-address access, or a hub-lock event. A selected event can also be polled (POLLSE1-4), branched on (JSE/JNSE), or used as an interrupt source. (Streamer-driven activity such as a FIFO block-wrap is observed by routing it through one of these selectable event sources, not by a streamer-specific wait.)

**WAITPAT** waits for a pin pattern match. Programs configure a pattern and mask, then WAITPAT suspends execution until the pin states match the specified pattern. This enables synchronization with parallel interfaces or detection of specific pin combinations.

**POLLATN, POLLCT1, POLLCT2, POLLCT3** provide polling-based alternatives to waiting. Instead of blocking until a condition occurs, these instructions check whether an event has occurred and set flags accordingly. This allows code to perform useful work while watching for events, rather than waiting idly.


## 4.6 Timing-Critical Patterns

### 4.6.1 Cycle-Exact Loops

Many real-time applications require loops that execute with precise, predictable timing. The P2's deterministic instruction timing makes cycle-exact loops practical and reliable.

Consider a loop that reads data from hub memory, processes it, and repeats:

```pasm2
loop
        rdlong  data, ptr               ' 9...16 cycles (hub-window dependent)
        add     ptr, #4                 ' 2 cycles
        djnz    count, #loop            ' 4 cycles (taken)
```

This loop body must account for hub access timing variation. If the loop starts aligned with the COG's hub window, RDLONG incurs 0 slot-wait (9 cycles) and the loop takes 9 + 2 + 4 = 15 cycles. If the loop starts just after the hub window, RDLONG incurs 7 cycles of slot-wait (16 cycles) and the loop takes 16 + 2 + 4 = 22 cycles.

For truly cycle-exact timing, loops must either eliminate hub access or align hub access with the hub rotation. One approach uses COG RAM for all data, avoiding hub access entirely:

```pasm2
loop
        add     data, #1                ' 2 cycles
        djnz    count, #loop            ' 4 cycles (taken)
        ' Exactly 6 cycles per iteration
```

Another approach aligns the loop body to an 8-cycle boundary and ensures hub access occurs at the same phase each iteration:

```pasm2
loop
        rdlong  data, ptr               ' 9...16 cycles (same slot-wait each time)
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

```pasm2
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

CORDIC operations take 55 clocks to compute results, but the instruction that starts a CORDIC operation completes in just 2...9 clocks (2 when the COG's hub slot is current, up to 9 when it must wait for its hub slot). This creates an opportunity for pipelining: start a CORDIC operation, perform other work during the 55-clock computation period, then retrieve the result.

A simple example shows the pattern:

```pasm2
        qmul    a, b                    ' Start multiply
        ' ... 55 clocks of other work ...
        getqx   result                  ' Get result (low 32 bits)
```

For maximum efficiency, interleave multiple CORDIC operations with other work:

```pasm2
        qmul    a1, b1                  ' Start first multiply
        ' ... some work ...
        qmul    a2, b2                  ' Start second multiply
        ' ... more work ...
        getqx   result1                 ' Get first result
        ' ... more work ...
        getqx   result2                 ' Get second result
```

GETQX returns in 2 clocks if the CORDIC result is already available (or the CORDIC is empty); otherwise it automatically stalls the COG until the result is ready—it never returns a partial result (worst case approaching the 55-clock latency). To test readiness without stalling, poll the CORDIC-empty (QMT) event rather than calling GETQX blindly. If GETQX executes later than the result, the result remains available—CORDIC results persist until the next CORDIC operation starts.

Multiple CORDIC operations can be in flight simultaneously, with results retrieved in order. Starting a new CORDIC operation does not invalidate results from previous operations until their results have been read.

### 4.6.4 Deterministic I/O

Bit-banging—directly controlling I/O pins with software timing—requires cycle-accurate execution. The P2's deterministic timing makes bit-banging practical for protocols like WS2812 LED control, custom serial formats, or precise pulse generation.

A WS2812 LED protocol example demonstrates the precision required:

```pasm2
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

The P2 provides a global 64-bit cycle counter (Rev B/C silicon) that increments every clock cycle. This counter runs continuously from power-on. COGs read the counter using the GETCT instruction, which returns the lower 32 bits by default. The lower 32 bits wrap around after reaching their maximum value.

Measuring code execution time involves reading the counter before and after the code section of interest:

```pasm2
        getct   start_time              ' Read cycle counter
        ' ... code to measure ...
        getct   end_time                ' Read cycle counter again
        sub     end_time, start_time    ' Elapsed cycles
```

The difference between the two readings gives the exact number of cycles elapsed. This measurement includes the cycles consumed by GETCT itself (2 cycles each), so precise measurements should account for this overhead.

For short code sequences, the measurement overhead matters. Measuring a 10-cycle sequence with two GETCT instructions reports 14 cycles (2 + 10 + 2). For longer sequences, the 4-cycle overhead becomes negligible.

The cycle counter is global across all COGs—all COGs read the same counter value. This enables synchronization and coordination between COGs. One COG can mark a time value and pass it to another COG via hub memory, allowing the second COG to measure time relative to events in the first COG.

### 4.7.2 Counter Wrap-Around

The lower 32 bits of the cycle counter wrap around every 2³² cycles. At 320 MHz, this occurs every 13.4 seconds. Code that measures elapsed time using the lower 32 bits must handle wrap-around correctly.

Subtraction using unsigned arithmetic naturally handles wrap-around. When end_time is less than start_time (because wrap-around occurred), the subtraction `end_time - start_time` produces the correct elapsed time due to modular arithmetic:

```pasm2
        mov     start_time, ##$FFFF_FFF0  ' Near wrap-around
        mov     end_time,   ##$0000_0010  ' After wrap-around
        sub     end_time, start_time      ' Result: $20 (32 cycles)
```

This automatic wrap-around handling works for elapsed times up to 2³¹ cycles (half the counter range). For longer measurements, code must count wrap-around events explicitly or use multiple counter values.

### 4.7.3 Profiling Techniques

GETCT enables detailed performance profiling of assembly code. By measuring execution time for different code paths, programmers can identify performance bottlenecks and verify that optimizations achieve expected speedups.

A common profiling pattern measures loop iteration time:

```pasm2
        mov     iterations, ##1000
        getct   start_time
loop
        ' ... code to profile ...
        djnz    iterations, #loop
        getct   end_time
        mov     elapsed, end_time
        sub     elapsed, start_time
```

The total elapsed time divided by the iteration count gives the average time per iteration. For more detailed profiling, place multiple GETCT measurements within the loop to identify which parts of the loop consume the most time:

```pasm2
loop
        getct   time1
        ' ... section A ...
        getct   time2
        ' ... section B ...
        getct   time3
        mov     timeA, time2
        sub     timeA, time1              ' Section A timing
        mov     timeB, time3
        sub     timeB, time2              ' Section B timing
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

Hub execution mode—often called "HUBEXEC mode"—executes instructions from hub RAM. This allows programs to exceed the 512-long COG RAM size limit, supporting much larger code bases at the cost of a branch-refill penalty (sequential throughput is unchanged).

In hub execution mode, sequential straight-line code executes at 2 cycles per instruction—identical throughput to COG mode. The (cogs+11) = 19-stage prefetch FIFO streams instructions ahead of execution, hiding hub latency so there is no per-instruction hub-window wait. The only hubexec penalty occurs at branches: a taken branch forces a FIFO refill, costing a minimum of 13 clocks (one more if the target is not long-aligned), versus 4 clocks for a COG-mode branch.

Hub execution mode begins when a COG starts via COGINIT with a hub RAM address ($400 or higher). The program counter points to hub RAM locations, and the processor fetches instructions through the FIFO prefetch mechanism. Code can utilize the full 512 KB of hub RAM.

Despite the branch-refill penalty, hub mode remains useful for several scenarios:

**Large programs:** When code exceeds 512 longs, hub mode is the only option short of implementing code overlays.

**Non-critical code:** Initialization routines, background tasks, and other code without tight timing requirements run acceptably in hub mode.

**Mixed execution:** Programs can start in hub mode and copy time-critical sections to COG RAM for execution at full speed. COGINIT can switch a running COG between hub and COG mode dynamically.

### 4.8.3 Timing Comparison

The following table shows typical execution times for common operations in both execution modes:

| Operation | COG Mode | Hub Mode |
|-----------|----------|----------|
| Simple ALU | 2 cycles | 2 cycles |
| Branch taken | 4 cycles | min 13 cycles (+1 if target not long-aligned) |
| Hub access | 2 + hub wait | 2 + hub wait |
| CORDIC start | 2...9 clocks | 2...9 clocks |

Simple ALU operations (ADD, SUB, AND, OR, etc.) take 2 cycles in both modes. In sequential straight-line code the FIFO prefetches instructions ahead of execution, so hubexec instruction fetch adds no per-instruction hub-window wait—throughput matches COG mode.

Branch instructions take 4 cycles in COG mode when taken. In hub mode, a taken branch forces the prefetch FIFO to refill from the new address, costing a minimum of 13 clocks (one more if the target is not long-aligned). This branch-refill penalty—not per-instruction fetch—is where hubexec loses time relative to COG mode.

Hub access instructions show essentially the same data-access timing in both modes because the data access (as opposed to instruction fetch) uses the hub window mechanism regardless of where the instruction itself came from. A RDLONG takes 9...16 clocks in COG mode (9...26 in hub-execution mode), the variation being the hub-window slot-wait.

CORDIC operations start in 2...9 clocks in both modes (the slot-wait component reflects waiting for the COG's hub slot, not instruction fetch; the 55-clock computation time is the same in both modes). The CORDIC-issue instruction is sequential and streamed by the FIFO, so it incurs no extra hubexec fetch penalty.

Because branch-heavy code pays the FIFO-refill penalty on every taken branch, COG mode remains strongly preferred for timing-critical, tightly-looped code. Programs typically keep inner loops, interrupt handlers, and time-sensitive operations in COG RAM while using hub mode for larger, less-critical code sections.


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

