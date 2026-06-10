# Chapter 5: Special Hardware Overview

The P2 includes specialized hardware subsystems that extend beyond basic instruction execution. Understanding these subsystems enables advanced applications: the CORDIC coprocessor accelerates mathematical operations, Smart Pins provide programmable I/O peripherals, the Streamer enables high-speed data movement, events support responsive programming, hardware locks coordinate multi-COG applications, and debug hardware assists development. This chapter provides an overview of each subsystem; detailed instruction usage is covered in Part II, and complete subsystem documentation is available in specialized manuals.


## 5.1 CORDIC Coprocessor {#cordic-overview}

The CORDIC (Coordinate Rotation Digital Computer) coprocessor provides hardware-accelerated mathematical operations. While the P2's instruction set includes basic arithmetic, the CORDIC handles operations that would otherwise require hundreds of instructions: 32×32-bit multiplication producing 64-bit results, division with quotient and remainder, square root extraction, trigonometric computations, and logarithmic functions. The CORDIC operates as a queue-based coprocessor—your code initiates an operation, performs other useful work for 55 clock cycles while the CORDIC computes, then retrieves the results.

### 5.1.1 CORDIC Capabilities

The CORDIC provides eight categories of operations, each accessed through dedicated queue instructions:

| Operation | Instruction | Output |
|-----------|-------------|--------|
| Multiply | [QMUL](#qmul) | 64-bit product (low 32 bits in X, high 32 bits in Y) |
| Divide | [QDIV](#qdiv) | Quotient in X, remainder in Y |
| Fractional divide | [QFRAC](#qfrac) | Fractional quotient in X, remainder in Y |
| Square root | [QSQRT](#qsqrt) | Integer square root in X |
| Rotate | [QROTATE](#qrotate) | Rotated X coordinate, rotated Y coordinate |
| Vector | [QVECTOR](#qvector) | Magnitude in X, angle in Y (Cartesian to polar) |
| Logarithm | [QLOG](#qlog) | Base-2 logarithm (5:27 fixed-point) in X |
| Exponential | [QEXP](#qexp) | e^x approximation in X |

Each operation produces one or two 32-bit results, retrieved through [GETQX](#getqx) and [GETQY](#getqy) instructions. The multiply operation (QMUL) is particularly valuable for fixed-point arithmetic, providing the full 64-bit product that would otherwise require complex multi-instruction sequences.

### 5.1.2 CORDIC Operation Flow

CORDIC operations follow a three-step pattern: queue the operation, wait for computation, retrieve results. The critical timing constraint is the 55-clock computation period—attempting to retrieve results before this period completes produces undefined values.

```pasm2
        qmul    multiplicand, multiplier    ' Start 32x32 multiply
        ' ... 55 clocks of other useful work ...
        getqx   product_lo                  ' Get low 32 bits
        getqy   product_hi                  ' Get high 32 bits
```

The 55-clock computation period is fixed for all CORDIC operations. Efficient code interleaves CORDIC computations with other processing, ensuring the CPU remains productive while the coprocessor works. The CORDIC operates independently once queued, allowing the COG to execute unrelated instructions during the computation period.

### 5.1.3 CORDIC Pipelining

The CORDIC is a fully pipelined, shared resource accessed through hub rotation—the same arbitration mechanism used for hub RAM. Each COG receives a CORDIC access slot every 8 clocks. The pipeline is 54 stages deep; results are available 55 clocks after queuing (1 clock to enter the pipeline, 54 clocks to process). With 8-clock access intervals, a single COG can have 6-7 operations in flight simultaneously (54 ÷ 8 ≈ 6.75). This deep pipelining enables sustained high throughput when processing multiple values.

### 5.1.4 The Pipeline Phases

Effective CORDIC usage follows a three-phase pattern: fill, steady-state, and drain.

**Fill Phase:** Submit multiple operations before expecting any results. During this phase, you queue operations without retrieving results, filling the pipeline:

```pasm2
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

```pasm2
        ' Steady state - retrieve previous, submit next
.loop   getqx   result_lo                   ' Get result from ~55 clocks ago
        getqy   result_hi
        qmul    a_next, b_next              ' Submit next operation
        ' ... process result, prepare next operands ...
        djnz    count, #.loop
```

**Drain Phase:** After submitting the final operation, continue retrieving remaining results without submitting new operations:

```pasm2
        ' Drain phase - retrieve final results
        getqx   result_lo                   ' Get remaining results
        getqy   result_hi
        ' ... repeat for each operation still in pipeline ...
```

### 5.1.5 Result Retrieval Timing

The GETQX and GETQY instructions retrieve results in submission order. If a result is not yet ready when GETQX or GETQY executes, the COG stalls until the result becomes available. This automatic stalling simplifies programming—you need not count cycles precisely—but can impact performance if you retrieve too early.

For non-blocking result checking, use POLLQMT to test whether the CORDIC pipeline is empty:

```pasm2
        pollqmt             wc              ' C=1 if pipeline empty,
                                            '  C=0 if results pending
        if_nc   getqx   result              ' Retrieve if available
```

The CORDIC generates Event 15 when GETQX or GETQY executes with no results available. This event can trigger an interrupt or be polled, useful for detecting programming errors where retrieval occurs before any operations were queued.

### 5.1.6 Practical Pipelining Example

This example processes an array of coordinate pairs, rotating each by a fixed angle. The pipeline keeps multiple rotations in flight:

```pasm2
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

This pattern achieves one rotation result every ~20 instructions (the loop body), rather than waiting 55 clocks per rotation. For 16 points, the pipelined version completes in roughly 320 clocks versus 864 clocks for sequential processing—nearly 3× faster.

### 5.1.7 CORDIC Instructions Reference

**Queue Operations:** [QMUL](#qmul), [QDIV](#qdiv), [QFRAC](#qfrac), [QSQRT](#qsqrt), [QROTATE](#qrotate), [QVECTOR](#qvector), [QLOG](#qlog), [QEXP](#qexp)

**Result Retrieval:** [GETQX](#getqx), [GETQY](#getqy)

Full instruction details, including operand formats and result interpretations, appear in Part II under each instruction's entry.

### 5.1.8 Protecting Critical CORDIC Sequences

**Note:** This section applies only to PASM2 code with interrupts enabled. Spin2 operators that use CORDIC (such as `*`, `/`, `SQRT`, `QSIN`, `QCOS`, etc.) are already protected by the Spin2 interpreter—no additional protection is needed when using Spin2.

The 55-clock delay between queuing a CORDIC operation and retrieving its result creates a timing window. In PASM2 applications using interrupts, an interrupt that fires during this window could delay result retrieval or queue additional operations that interfere with the expected sequence. For timing-critical applications, this can cause incorrect results or undefined behavior.

The P2 provides a simple protection mechanism using REP with a single iteration:

```pasm2
' Protect CORDIC operation from interrupts
        rep     @.protect, #1         ' Execute block atomically
        qmul    multiplicand, multiplier
        ' ... other CORDIC work (up to 55 clocks) ...
        getqx   result_lo
        getqy   result_hi
.protect
```

This idiom works because REP stalls interrupt handling until all repeated instructions complete—even with just one iteration. The entire sequence from QMUL through GETQY executes without interruption.

**When to use interrupt protection:**

- **DSP inner loops:** Where CORDIC operations must maintain precise timing relationships
- **Fixed-point arithmetic chains:** Where one CORDIC result feeds immediately into another calculation
- **Real-time control:** Where interrupt latency could cause result retrieval timing errors

**When protection is unnecessary:**

- **Spin2 code:** The Spin2 interpreter already protects CORDIC operations internally
- **PASM2 without interrupts:** When no interrupts are enabled (SETINT not used)
- **Background calculations:** Where the 55-clock window has explicit NOP padding or other work
- **Pipelined processing:** Where the fill-steady-drain pattern naturally handles timing

For longer critical sequences, use a large REP block count with one iteration:

```pasm2
' Extended interrupt-free zone
        rep     #99, #1               ' 99 instructions, 1 iteration
        qsqrt   value, #0             ' CORDIC operations
        qlog    value
        qexp    value
        ' ... up to 99 total instructions ...
        getqx   result
_ret_   mov     output, result        ' REP exits at _ret_
```

The large instruction count (99) creates an interrupt-free zone that terminates at the first `ret`, `_ret_`, or branch instruction encountered.


## 5.2 Smart Pins

The P2 provides 64 Smart Pins, one per I/O pin, each containing a complete programmable peripheral. Smart Pins eliminate the need for external support chips in many applications—a single Smart Pin can implement a UART transmitter and receiver, generate PWM signals, measure pulse widths, read quadrature encoders, or convert analog signals. Each Smart Pin contains local state machines, DAC and ADC hardware, timing circuits, and configuration registers, all controlled through PASM2 instructions. The Smart Pin architecture offloads I/O processing from the COG, allowing precise timing and continuous operation without software intervention.

### 5.2.1 Smart Pin Architecture

Each Smart Pin integrates multiple hardware components that work together to implement various I/O functions:

- **Configurable I/O circuitry:** Programmable pull-up/down resistors, output drivers, and high-impedance (floating) modes
- **Mode selection logic:** 32 distinct operating modes covering digital, analog, serial, and timing applications
- **Local state machine:** Autonomous operation once configured, generating events when data is ready
- **DAC hardware:** 8-bit digital-to-analog converter for analog output and sigma-delta modulation
- **ADC hardware:** Analog-to-digital conversion using sigma-delta and comparator techniques
- **Timing hardware:** Counters and comparators for precise edge detection and pulse generation

The Smart Pin's autonomous operation is particularly significant. Once configured, a Smart Pin operates independently of the COG—a UART Smart Pin transmits and receives bytes, a PWM Smart Pin generates continuous waveforms, an encoder Smart Pin tracks position changes, all without ongoing CPU attention. The COG interacts with Smart Pins only when new data arrives or new output is needed.

### 5.2.2 Smart Pin Modes

Smart Pins support 32 distinct modes organized into functional categories. Each mode transforms the pin into a specialized peripheral:

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

- **WRPIN** - Write pin mode (selects one of 32 operating modes)
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

Direction and output control manage the physical pin state. The P2 provides four instruction families (DIR, OUT, FLT, DRV), each with eight suffix variants (L, H, C, NC, Z, NZ, NOT, RND):

- **DIR** family - Set pin direction (input vs. output)
- **OUT** family - Set output value (when pin is output)
- **FLT** family - Float pin to high-impedance (tri-state)
- **DRV** family - Drive pin (opposite of float)

Each family includes suffix variants: `L` (DIR/OUT bit := 0), `H` (:= 1), `C` (:= C flag), `NC` (:= !C flag), `Z` (:= Z flag), `NZ` (:= !Z flag), `NOT` (toggle the bit), `RND` (:= a random bit). This provides fine-grained control: `DIRL` forces the pin to input (DIR=0), while `DIRZ` sets the pin's direction to the current Z flag value (Z=1 → output, Z=0 → input).

### 5.2.4 Smart Pin Documentation

Smart Pin modes vary significantly in configuration and operation. The mode value, X parameter, and Y parameter have different meanings for each mode—UART mode parameters differ completely from PWM mode parameters. Complete Smart Pin mode documentation, including configuration values, timing diagrams, and usage examples, appears in the **P2 Smart Pins Tutorial** (`p2-smart-pins-tutorial`). That manual provides essential reference material for Smart Pin programming.


## 5.3 Streamer {#streamer-overview}

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

Mode selection appears in the XINIT instruction's mode parameter, along with configuration bits controlling data width, pin selection, and transfer direction. Each mode interprets Hub memory data differently—LUT mode uses data as lookup indices, NCO mode uses data as frequency control words, RF mode uses data as modulation patterns.

### 5.3.4 Streamer Configuration

Streamer commands are built by combining mode constants using OR operations. The constants follow a naming convention that encodes the data flow:

- **X_IMM_** - Immediate data modes (data passed directly)
- **X_RFBYTE/RFWORD/RFLONG_** - Read from FIFO (hub RAM) with specified data width
- **X_..._WFBYTE/WFWORD/WFLONG** - Write to FIFO (hub RAM) for capture operations
- **X_DACS_** - DAC channel selection and configuration
- **X_PINS_ON/OFF** - Enable/disable pin outputs
- **X_WRITE_ON/OFF** - Enable/disable hub RAM writes

The naming pattern `X_[source][size]_[pins]P_[dacs]DAC[bits]` describes the complete data path. For example, `X_RFBYTE_RGB8` reads bytes from hub RAM and interprets them as RGB 3:3:2 color values.

**Complete X_* constant documentation, including all 78 mode constants with values and descriptions, appears in Appendix F (Streamer Mode Constants).** That appendix provides the detailed reference needed to configure the Streamer for specific applications, including usage examples for video streaming, audio DAC output, and ADC capture.


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
| FBW | FIFO block wrap | Set up next FIFO block at circular-buffer boundary (via FBLOCK) |
| XMT | Streamer ready for new command | Command-buffer-empty (streamer-empty) notification |
| XFI | Streamer finished (no pending command) | Wait for streamer completion / streamer idle |
| XRO | Streamer rollover | Circular buffer management |
| XRL | Streamer read LUT $1FF | LUT-wrap timing event |
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

- **SETINT1, SETINT2, SETINT3** - Select the interrupt event source (4-bit code in Dest[3:0]). The handler address is set separately by writing the IJMP1/2/3 registers ($1F4/$1F2/$1F0).
- **STALLI** - Stall (disable) interrupt processing
- **ALLOWI** - Allow (enable) interrupt processing (default on COG start)

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

Polling enables responsive event handling within loops. Code can check multiple events in sequence, responding to whichever occurred, without blocking on any single event:

```pasm2
                pollse1         wc          ' Test event 1, C if occurred
        if_c    jmp     #handler                ' Branch to handler only if
                                                '  event fired
```

This pattern branches to handler code only when the event occurred.

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

```pasm2
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

```pasm2
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

```pasm2
                locktry display_lock    wc      ' Acquire display
        if_nc   jmp     #retry
                ' ... draw graphics, write text ...
                lockrel display_lock            ' Release for other COGs
```

**Producer/Consumer Synchronization:**

Lock status serves as a signaling mechanism. A producer holds a lock while data is invalid; releasing the lock signals data ready. A consumer waits via LOCKTRY, acquiring the lock when data becomes valid.

The 16-lock limit rarely constrains applications—complex systems typically need fewer than 16 distinct critical sections. Applications requiring more synchronization points often combine locks with other mechanisms (event flags, shared memory flags) for fine-grained coordination.


## 5.6 XBYTE Bytecode Engine

XBYTE is a hardware bytecode dispatch mechanism. When a RET or _RET_ instruction returns to address $1FF, the hardware automatically fetches a bytecode from the FIFO, looks up a dispatch entry in LUT RAM, and branches to the handler routine. Total dispatch overhead is 6 clock cycles.

### 5.6.1 Dispatch Cycle

XBYTE executes as a phantom instruction triggered by returning to $1FF. The return does not pop the hardware stack, so repeated RET/_RET_ instructions fetch successive bytecodes.

| Clock | Phase | Activity |
|-------|-------|----------|
| 1 | go | RFBYTE bytecode, SKIPF #0 |
| 2 | get | MOV PA,bytecode, RDLUT |
| 3 | go | RDLUT complete |
| 4 | get | EXECF begin |
| 5 | go | MOV PB,(GETPTR), MODCZ, branch |
| 6-7 | | Pipeline flush/reload |
| 8 | get | First instruction of handler |

A handler ending with `_RET_` adds 2 clocks, making the minimum cycle 8 clocks total.

### 5.6.2 LUT Entry Format

Each 32-bit LUT entry contains:

| Bits | Content |
|------|---------|
| [9:0] | Handler address in COG/LUT RAM |
| [31:10] | SKIPF pattern (22 bits) |

EXECF simultaneously branches and applies the skip pattern.

### 5.6.3 Configuration Summary

XBYTE is configured via `_RET_ SETQ {#}D` with $1FF on the stack:

| Mode | LUT Entries | Index Source |
|------|-------------|--------------|
| Full 8-bit | 256 | bytecode[7:0] |
| 7-bit | 128 | bytecode[6:0] or [7:1] |
| 6-bit | 64 | bytecode[5:0] or [7:2] |
| 5-bit | 32 | bytecode[4:0] or [7:3] |
| 4-bit | 16 | bytecode[3:0] or [7:4] |

Smaller modes conserve LUT space. A compressed mode allows mixing individual and shared handlers.

### 5.6.4 Handler Requirements

- **Location:** COG RAM ($000-$1FF) or LUT RAM ($200-$3FF)
- **Exit:** Must end with RET or _RET_
- **Registers:** PA contains bytecode value; PB contains FIFO pointer

**See:** SETQ, SETQ2 for configuration; EXECF, SKIPF for dispatch mechanism; RFBYTE, RDFAST for FIFO operations; GETBRK for debugging state


## 5.7 Boot Process

When the P2 powers on or receives a hardware reset, it begins a deterministic boot sequence that loads and executes user code. Understanding this sequence is essential for embedded applications—it explains why programs must configure the clock, how the chip finds your code, and what state the hardware is in when your program starts executing.

### 5.7.1 Initial Chip State

At reset, the P2 initializes to a known state before any user code executes:

| Resource | Initial State |
|----------|---------------|
| Clock source | RCFAST (~20-30 MHz (typically ~24 MHz) internal RC oscillator) |
| All COGs | Stopped (except COG 0) |
| Hub RAM | Undefined contents |
| I/O pins | High-impedance (floating) |
| 64-bit counter | Cleared to zero |
| PRNG | Seeded with thermal noise |

The internal RC oscillator (RCFAST) provides the initial clock. This oscillator is guaranteed to run at least 20 MHz under all conditions, ensuring reliable serial communication during boot. The exact frequency varies with temperature and manufacturing, typically ~24 MHz. Programs requiring precise timing must configure an external crystal or the PLL after boot.

The boot ROM seeds the Xoroshiro128** pseudo-random number generator with true random data. The ROM reads thermal noise from pin 63 (configured in ADC calibration mode) fifty times, using each 31-bit sample to seed the PRNG through HUBSET. This establishes high-quality randomness available immediately when user code starts—there is no need to seed the PRNG again, though programs may do so if desired.

### 5.7.2 Boot Source Selection

The P2 determines its boot source by sensing external pull-up resistors on pins P59-P61. This hardware detection occurs automatically and requires no software configuration.

| P61 | P60 | P59 | Boot Behavior |
|-----|-----|-----|---------------|
| none | none | none | Serial only (60s window) |
| pull-up | none | none | Serial 100 ms window, then SPI flash; serial 60s on flash failure |
| pull-up | any | pull-down | SPI flash only (fast boot), no serial; shutdown on failure |
| none | pull-up | none | SD card, then serial (60s) on failure |
| none | pull-up | pull-down | SD card only, shutdown on failure |
| any | any | pull-up | Serial only (60s window); no flash or SD boot |

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

After boot completes, ROM control of these pins ends and user code takes over. However, the boot source hardware typically remains physically connected:

- **SPI Flash (P58-P61):** The flash chip remains attached. User programs commonly continue using these pins to access flash storage for code snippets, lookup tables, audio files, or data logging.
- **SD Card (P58-P61):** The SD card socket remains attached. User programs commonly continue using these pins for file system access.
- **Serial (P62-P63):** On development boards, these pins typically remain connected to the USB-serial interface for debugging and host communication.

The pins are available for user code to configure and use—but practical usage depends on what external hardware is connected to them.

### 5.7.4 The Boot Sequence

After reset, COG 0 loads and executes the boot ROM program (ROM_Booter.spin2). The boot sequence proceeds as follows:

**Step 1: Check for SPI Flash**

If an external pull-up is detected on P61, the booter attempts SPI flash boot:

1. Load the first 1024 bytes (256 longs) from SPI flash into hub RAM at $00000
2. Compute the 32-bit sum of these 256 longs
3. If the sum equals "Prop" ($706F7250), the data is valid:
   - Copy the 256 longs from hub to COG 0 registers $000-$0FF
   - If P59 is pulled down: execute immediately (`JMP #$000`)
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

User code starts executing with the RCFAST clock source—an internal RC oscillator running approximately 20-30 MHz (typically ~24 MHz). For applications requiring precise timing, configure an external crystal or the PLL early in your program:

```pasm2
' Configure 20 MHz crystal with PLL for 160 MHz operation
                ' Enable crystal oscillator with 15pF caps
                hubset  ##%0000_0001_0000_0000_0000_0000_00_10
                ' Wait 10ms for crystal stabilization
                waitx   ##20_000_000/100
                ' Switch to crystal clock source
                hubset  ##%0000_0001_0000_0000_0000_0000_10_10
                ' Configure PLL: /1 * 8 / 1 = 160MHz
                hubset  ##%0000_0001_0000_1000_0000_0010_00_10
                ' Wait 100µs for PLL lock
                waitx   ##20_000_000/10000
                ' Switch to PLL output
                hubset  ##%0000_0001_0000_1000_0000_0010_00_11
```

The ASMCLK directive provides a convenient shorthand when using standard crystal configurations. It generates the appropriate HUBSET sequence based on the _clkfreq and _clkmode constants defined in your program.

**Why Clock Setup Is Required:**

The boot ROM cannot know what clock source your hardware provides. Some boards use 20 MHz crystals, others use 25 MHz, and some applications run directly from the internal oscillator. By starting in RCFAST mode, the P2 boots reliably on any hardware. Your program then configures the actual clock source appropriate for your design.

### 5.7.7 Rebooting from Software

The HUBSET instruction can trigger a hardware reset, returning the chip to the boot sequence:

```pasm2
                hubset  ##$1000_0000                ' Generate reset pulse,
                                                    '  reboot chip
```

This performs a full hardware reset—all COGs stop, all I/O returns to high-impedance, the clock reverts to RCFAST, and the boot ROM executes from the beginning. Use this for implementing watchdog recovery, firmware updates, or returning to the boot loader.


## 5.8 DEBUG Output

DEBUG is a compile-time directive that generates serial output code. When enabled, DEBUG statements transmit formatted data over the serial connection to the development host, where the debug window displays values, text, and graphical visualizations.

### 5.8.1 Basic Usage

DEBUG statements output text strings and formatted values:

```pasm2
                debug("Starting motor control")     ' Text message
                debug("Speed: ", udec(speed))       ' Decimal value
                debug("Status: ", uhex_(status))    ' Hex without name
```

The serial connection typically runs at 2 Mbaud. When DEBUG is disabled via compiler option, statements generate no code.

### 5.8.2 Value Formatters

DEBUG provides formatters for numeric display. Each has unsigned (U prefix) and signed (S prefix) variants:

| Base | Formatters | Output Example |
|------|------------|----------------|
| Decimal | UDEC, SDEC | `counter = 42` |
| Hexadecimal | UHEX, SHEX | `addr = $0400` |
| Binary | UBIN, SBIN | `flags = %10110` |

Underscore suffix (UDEC_, UHEX_, etc.) outputs only the value, omitting the variable name.

Size suffixes (_BYTE, _WORD, _LONG) control display width. Array variants (_BYTE_ARRAY, etc.) display multiple consecutive values.

### 5.8.3 Visual Debug Displays

DEBUG supports graphical display windows including:
- **SCOPE** — Oscilloscope waveform display
- **PLOT** — Data plotting and charts
- **LOGIC** — Logic analyzer view
- **TERM** — Dedicated terminal window
- **BITMAP** — Pixel display

Visual displays use a two-phase pattern: creation statement (with display type) establishes the window, update statements (backtick + name) send data points.

### 5.8.4 Multi-COG Programs

When multiple COGs execute DEBUG statements, the system automatically prefixes each message with the COG number (Cog0: through Cog7:). This applies to text output only; visual displays are typically dedicated to specific COGs.

### 5.8.5 Performance Considerations

⚠️ **Pitfall:** DEBUG transmits data serially—each statement can consume hundreds of microseconds. Never place DEBUG inside performance-critical loops. Use DEBUG before or after loops, or sample infrequently with conditional statements.

For production builds, disable DEBUG via compiler option. Statements compile to nothing—zero runtime impact.

**See:** DEBUG instruction in Part II for complete syntax; P2 Debug Window Manual for visual display configuration, advanced formatters, and professional debugging techniques.


### 5.8.6 Debug Configuration

The debug system operates at three distinct levels, each controlled by CON constants:

- **Code Instrumentation (Compile-Time):** DEBUG_DISABLE and DEBUG_MASK control whether debug statements generate code
- **Output Infrastructure (Runtime):** DEBUG_COGS, DEBUG_BAUD, and related constants configure the debug serial system
- **Breakpoint Configuration:** DEBUG_MAIN and DEBUG_COGINIT configure automatic breaks for single-step debugging

**Selective Debug with debug[N]():**

The `debug[N]()` form categorizes debug statements into channels (0-31) that compile selectively based on DEBUG_MASK:

```pasm2
CON
  DBG_INIT  = 0
  DBG_ERROR = 3
  DEBUG_MASK = (1 << DBG_INIT) | (1 << DBG_ERROR)

DAT
        org
entry   debug[DBG_INIT]("Starting")   ' COMPILED - bit 0 set
        debug[1]("Motor status")       ' NOT compiled - bit 1 clear
        debug[DBG_ERROR]("Fault!")     ' COMPILED - bit 3 set
```

Disabled channels produce zero code—no runtime overhead exists. Standard `debug()` statements without channel numbers are unaffected by DEBUG_MASK and compile whenever debug is enabled.

**Compile-Time vs Runtime Filtering:**

DEBUG_MASK and DEBUG_COGS operate at different levels:

| Constant | Level | Controls |
|----------|-------|----------|
| DEBUG_MASK | Compile-time | Whether `debug[N]()` generates code |
| DEBUG_COGS | Runtime | Whether a COG can produce debug output |

For a debug statement to produce output, both conditions must be met: the statement must compile (DEBUG_MASK permits it), and the executing COG must have its bit set in DEBUG_COGS.

**See:** Appendix E (Debug Configuration Constants) for complete constant documentation including DEBUG_DELAY, DEBUG_TIMESTAMP, DEBUG_BAUD, and breakpoint configuration.


```{=latex}
\begin{keyconcepts}
\item The CORDIC coprocessor provides 55-clock hardware math (multiply, divide, sqrt, trig)
\item Smart Pins are 64 programmable I/O peripherals with local state machines
\item The Streamer enables DMA-like high-speed data movement
\item Events provide non-interrupt notification; interrupts are available when needed
\item 16 hardware locks enable safe inter-COG synchronization
\item XBYTE provides 6-cycle bytecode dispatch for interpreters and VMs
\item The P2 boots from RCFAST (\textasciitilde20 MHz) and detects boot source via pin pull-ups
\item User code must configure the desired clock source after boot
\item DEBUG provides serial output with formatters; can be disabled for production
\item The 8-COG architecture often removes the need for interrupts (see Chapter 4: each COG runs deterministically; dedicate a COG to a task instead of interrupting one)
\item Each subsystem is controlled through dedicated PASM2 instructions
\end{keyconcepts}
```


<!-- End of Chapter 5 -->
