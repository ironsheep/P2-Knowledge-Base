# Chapter 5: Special Hardware Overview

The P2 includes specialized hardware subsystems that extend beyond basic instruction execution. Understanding these subsystems enables advanced applications: the CORDIC coprocessor accelerates mathematical operations, Smart Pins provide programmable I/O peripherals, the Streamer enables high-speed data movement, events support responsive programming, hardware locks coordinate multi-COG applications, and debug hardware assists development. This chapter provides an overview of each subsystem; detailed instruction usage is covered in Part II, and complete subsystem documentation is available in specialized manuals.


## 5.1 CORDIC Coprocessor

The CORDIC (Coordinate Rotation Digital Computer) coprocessor provides hardware-accelerated mathematical operations. While the P2's instruction set includes basic arithmetic, the CORDIC handles operations that would otherwise require hundreds of instructions: 32×32-bit multiplication producing 64-bit results, division with quotient and remainder, square root extraction, trigonometric computations, and logarithmic functions. The CORDIC operates as a queue-based coprocessor—your code initiates an operation, performs other useful work for 54 clock cycles while the CORDIC computes, then retrieves the results.

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
| Logarithm | [QLOG](#qlog) | Natural log approximation in X |
| Exponential | [QEXP](#qexp) | e^x approximation in X |

Each operation produces one or two 32-bit results, retrieved through [GETQX](#getqx) and [GETQY](#getqy) instructions. The multiply operation (QMUL) is particularly valuable for fixed-point arithmetic, providing the full 64-bit product that would otherwise require complex multi-instruction sequences.

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

**Queue Operations:** [QMUL](#qmul), [QDIV](#qdiv), [QFRAC](#qfrac), [QSQRT](#qsqrt), [QROTATE](#qrotate), [QVECTOR](#qvector), [QLOG](#qlog), [QEXP](#qexp)

**Result Retrieval:** [GETQX](#getqx), [GETQY](#getqy)

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

+-------------+-------------------------------------+-----------------------------------+
| Category    | Example Modes                       | Typical Applications              |
+=============+=====================================+===================================+
| Digital I/O | Repository mode, registered input,  | Debounced buttons, event          |
|             | long pulse accumulator              | counting, pulse measurement       |
+-------------+-------------------------------------+-----------------------------------+
| Serial      | UART transmit/receive, synchronous  | Communication with peripherals    |
|             | serial, SPI                         | and other systems                 |
+-------------+-------------------------------------+-----------------------------------+
| PWM         | PWM/duty mode, triangle/sawtooth    | Motor control, LED dimming,       |
|             | mode, incremental mode              | audio generation                  |
+-------------+-------------------------------------+-----------------------------------+
| Analog      | DAC output, ADC sampling,           | Sensor interfacing, analog        |
|             | comparator                          | signal generation                 |
+-------------+-------------------------------------+-----------------------------------+
| Timing      | Period measurement, pulse width     | Frequency measurement, event      |
|             | measurement, timeout                | timing, watchdog                  |
+-------------+-------------------------------------+-----------------------------------+
| Quadrature  | Quadrature encoder input            | Rotary encoder reading, motor     |
|             |                                     | position feedback                 |
+-------------+-------------------------------------+-----------------------------------+

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

Polling enables responsive event handling within loops. Code can check multiple events in sequence, responding to whichever occurred, without blocking on any single event:

```pasm
                pollse1         wc              ' Test event 1, set C if occurred
        if_c    jmp     #handler                ' Branch to handler only if event fired
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

XBYTE is like a phantom instruction that executes on a hardware stack return (RET/_RET_) to address $1FF. Such a return does not pop the stack, so each additional RET/_RET_ causes another bytecode to be fetched and executed. This creates a continuous interpretation loop with minimal overhead.

The execution cycle proceeds through eight clock phases:

+-------+-------+------------------------------------------+------------------------------+
| Clock | Phase | Activity                                 | Description                  |
+=======+=======+==========================================+==============================+
| 1     | go    | RFBYTE bytecode, SKIPF #0                | Fetch bytecode from FIFO,    |
|       |       |                                          | cancel any prior skip        |
|       |       |                                          | pattern                      |
+-------+-------+------------------------------------------+------------------------------+
| 2     | get   | MOV PA,bytecode, RDLUT                   | Write bytecode to PA         |
|       |       |                                          | ($1F6), start LUT read       |
+-------+-------+------------------------------------------+------------------------------+
| 3     | go    | RDLUT (data → D)                         | Complete LUT read, get       |
|       |       |                                          | routine address and skip     |
|       |       |                                          | pattern                      |
+-------+-------+------------------------------------------+------------------------------+
| 4     | get   | EXECF D (begin)                          | Start EXECF dispatch         |
+-------+-------+------------------------------------------+------------------------------+
| 5     | go    | MOV PB,(GETPTR), MODCZ, EXECF D (branch) | Write FIFO pointer to PB     |
|       |       |                                          | ($1F7), optionally set C/Z,  |
|       |       |                                          | branch                       |
+-------+-------+------------------------------------------+------------------------------+
| 6     | get   | flush pipeline                           | Pipeline flush for branch    |
+-------+-------+------------------------------------------+------------------------------+
| 7     | go    | reload pipeline                          | Pipeline reload              |
+-------+-------+------------------------------------------+------------------------------+
| 8     | get   | first instruction                        | First instruction of         |
|       |       |                                          | bytecode routine executes    |
+-------+-------+------------------------------------------+------------------------------+

When a bytecode routine completes and returns, XBYTE automatically fetches the next bytecode and repeats the cycle. The bytecode stream flows continuously from hub memory through the FIFO, enabling sustained interpretation without explicit fetching in the bytecode routines themselves. The bytecode routine could be as short as a single 2-clock instruction with a _RET_ prefix, making the total XBYTE loop take only 8 clocks.

### 5.6.2 LUT Table Format

The bytecode translation table in LUT memory consists of long values that EXECF uses for dispatch. Each 32-bit LUT entry contains two fields:

- **Bits [9:0]**: Jump address in COG/LUT RAM ($000-$3FF)
- **Bits [31:10]**: SKIPF pattern (22 bits) applied after the jump

When XBYTE dispatches to a bytecode routine, EXECF simultaneously jumps to the routine address and applies the skip pattern. This allows compact bytecode routines where common instruction sequences are shared and skip patterns select which instructions execute.

### 5.6.3 Configuration Options

XBYTE supports multiple configuration modes that trade bytecode count against LUT space requirements. The SETQ/SETQ2 D value controls the mode:

+------+----------------+-------------+-------------------+-----------+
| Bits | SETQ D Pattern | LUT Base    | Index Calculation | Bytecodes |
+======+================+=============+===================+===========+
| 8    | %A0000000F     | %A00000000  | I = bytecode[7:0] | 256       |
+------+----------------+-------------+-------------------+-----------+
| 7    | %AAxx0010F     | %AA0000000  | I = bytecode[6:0] | 128       |
+------+----------------+-------------+-------------------+-----------+
| 7    | %AAxx0011F     | %AA0000000  | I = bytecode[7:1] | 128       |
+------+----------------+-------------+-------------------+-----------+
| 6    | %AAAx1010F     | %AAA000000  | I = bytecode[5:0] | 64        |
+------+----------------+-------------+-------------------+-----------+
| 6    | %AAAx1011F     | %AAA000000  | I = bytecode[7:2] | 64        |
+------+----------------+-------------+-------------------+-----------+
| 5    | %AAAAx100F     | %AAAA00000  | I = bytecode[4:0] | 32        |
+------+----------------+-------------+-------------------+-----------+
| 5    | %AAAAx101F     | %AAAA00000  | I = bytecode[7:3] | 32        |
+------+----------------+-------------+-------------------+-----------+
| 4    | %AAAAA110F     | %AAAAA0000  | I = bytecode[3:0] | 16        |
+------+----------------+-------------+-------------------+-----------+
| 4    | %AAAAA111F     | %AAAAA0000  | I = bytecode[7:4] | 16        |
+------+----------------+-------------+-------------------+-----------+

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

XBYTE mode begins through a specific instruction sequence. First, push $1FF onto the hardware stack, then execute _RET_ SETQ to configure the mode and trigger XBYTE:

```pasm
                                        ' Setup before starting XBYTE:
        setq2   #256-1                  ' Load 256 longs into LUT
        rdlong  $100, #bytetable        ' Bytecode table at LUT $100

        rdfast  #0, #bytecodes          ' Init FIFO at bytecode stream

        push    #$1FF                   ' Push $1FF for XBYTE returns
_RET_   setq    #$100                   ' Start XBYTE: LUT base=$100, 256 bytecodes
```

The _RET_ SETQ instruction both configures XBYTE mode and returns to $1FF, which triggers the first bytecode fetch. Each bytecode routine ends with RET or _RET_, returning to $1FF to fetch the next bytecode.

To alter the XBYTE mode for all subsequent bytecodes, execute another _RET_ SETQ instruction within a bytecode routine. To alter the mode for the next bytecode only, use _RET_ SETQ2 instead—the original mode automatically restores after one bytecode. This is useful for engaging singular bytecodes from alternate sets without having to restore the original mode afterward.

### 5.6.6 Bytecode Routine Requirements

Bytecode routines must follow these constraints:

- **Location**: Must reside in COG RAM ($000-$1FF) or LUT RAM ($200-$3FF)
- **Exit**: Must end with RET or _RET_ to return control to XBYTE
- **Stack**: Hardware stack must not overflow (8 levels maximum)

The PA register ($1F6) contains the current bytecode value, available as an immediate operand within routines. The PB register ($1F7) contains the FIFO read pointer, enabling routines to track their position in the bytecode stream or read inline parameters following the bytecode using RFBYTE, RFWORD, or RFLONG.

For maximum performance, use the _RET_ prefix on the final instruction:

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

Beyond text output, DEBUG supports graphical display windows that visualize data in real time. Visual displays use a two-phase pattern: one statement **creates** the display window, and subsequent statements **update** it with new data.

**Window Creation vs. Update:**

The first DEBUG statement with a display name creates and configures the window. Inside loops, you update the existing window using the backtick-name syntax:

```pasm
                debug(`scope MySignal)              ' CREATE window (before loop)

.loop           rdlong  adc_value, adc_ptr
                debug(`MySignal adc_value)          ' UPDATE window (in loop)
                waitms  #1
                jmp     #.loop
```

The creation statement (with the display type keyword) establishes the window. Update statements (using just the backtick and name) send data points to the existing window. This separation is critical—creating windows inside loops would be extremely slow and waste resources.

**SCOPE — Oscilloscope Display:**

The SCOPE display provides multi-channel waveform visualization, similar to a digital oscilloscope:

```pasm
                debug(`scope MySignal)              ' Create scope window

.loop           rdlong  adc_value, adc_ptr
                debug(`MySignal adc_value)          ' Send sample to scope
                waitms  #1
                jmp     #.loop
```

SCOPE supports up to 8 channels, auto-scaling, triggering modes, and time base adjustment. Each update call adds one sample point; the display scrolls as new data arrives.

**PLOT — Data Plotting:**

The PLOT display creates line graphs, scatter plots, and trend charts:

```pasm
                debug(`plot Temperature)            ' Create plot window

.loop           call    #read_temperature
                debug(`Temperature temp_value)      ' Send data point to plot
                waitms  #1000
                jmp     #.loop
```

PLOT provides rolling or accumulating display modes, multiple data series, and statistical overlays including moving averages and min/max envelopes.

**TERM — Terminal Display:**

The TERM display provides a dedicated text terminal window, separate from the default debug output:

```pasm
                debug(`term Status)                           ' Create terminal window
                debug(`Status "System initialized", 13)       ' Send text to terminal
                debug(`Status "Temperature: ", sdec_(temp), "°C", 13)
```

TERM supports control characters (13 for newline, 9 for tab, 12 for clear screen) and provides a scrolling text buffer.

**LOGIC — Logic Analyzer:**

The LOGIC display shows digital signal timing as a logic analyzer view:

```pasm
                debug(`logic PortA)                 ' Create logic analyzer window

.loop           rdbyte  port_state, port_addr
                debug(`PortA port_state)            ' Send sample to analyzer
                waitx   ##100
                jmp     #.loop
```

LOGIC displays multiple digital channels with timing relationships, useful for debugging communication protocols and state machines.

**BITMAP — Pixel Display:**

The BITMAP display renders pixel data as an image:

```pasm
                debug(`bitmap Display, 320, 240)              ' Create bitmap window
                debug(`Display @framebuffer)                  ' Send pixel data
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

**CRITICAL WARNING:** Never place DEBUG statements inside performance-critical loops. DEBUG is a serial transmission mechanism—each statement can take thousands of clock cycles to format and transmit data. A tight loop with DEBUG inside will run orders of magnitude slower than the same loop without DEBUG. This isn't a subtle performance concern; it will fundamentally change your code's timing behavior.

**What DEBUG Actually Costs:**

- Each DEBUG statement requires cycles for formatting and transmission
- Serial transmission at 2 Mbaud limits throughput to roughly 200,000 characters per second
- A single `debug(udec(value))` statement may consume 100+ microseconds
- Visual display updates (SCOPE, PLOT) add host-side processing overhead
- In a loop running at 1 MHz, adding DEBUG drops effective frequency to kilohertz range

**Safe DEBUG Patterns:**

```pasm
                ' WRONG - DEBUG inside tight loop destroys timing
.bad_loop       rdlong  value, ptr
                debug(udec_(value))                 ' This kills performance!
                djnz    count, #.bad_loop

                ' RIGHT - DEBUG outside performant loop
.fast_loop      rdlong  value, ptr
                call    #process_value
                djnz    count, #.fast_loop
                debug("Final value: ", udec_(value))  ' Debug after loop completes

                ' RIGHT - Conditional debug for occasional sampling
.sample_loop    rdlong  value, ptr
                incmod  sample_cnt, #999    wz
        if_z    debug(udec_(value))                 ' Only every 1000th iteration
                djnz    count, #.sample_loop
```

**Mitigation Strategies:**

- Debug before or after performance-critical loops, never inside
- Use conditional DEBUG with counters to sample infrequently
- Remove DEBUG from timing-critical code paths entirely during development
- Use the compiler's debug-disable option for production builds
- For real-time monitoring, use hardware methods (pin toggles, scope probes)

**Production Builds:**

The compiler provides options to disable DEBUG entirely. When disabled, DEBUG statements compile to nothing—no code generated, no runtime impact. This allows debug instrumentation to remain in source code, ready for future debugging sessions, without affecting production performance.

### 5.8.9 DEBUG and Multi-COG Programs

When multiple COGs execute DEBUG statements, output interleaves in the debug window. Each COG's output appears as it transmits, which can create confusing mixed output when COGs debug simultaneously.

**Automatic COG Identification:**

For standard DEBUG output (not routed to a visual display window), the debug system automatically prefixes each message with the COG number (Cog0: through Cog7:). You do not need to manually add COG identification—it's built into the debug protocol:

```pasm
                debug("Starting motor control")     ' Output: Cog2: Starting motor control
                debug(udec(speed))                  ' Output: Cog2: speed = 1500
```

This automatic prefixing applies only to text output. Visual displays (SCOPE, PLOT, TERM, etc.) do not receive the COG prefix because they're typically dedicated to specific COGs or purposes.

**Strategies for Multi-COG Debugging:**

- Rely on automatic COG prefixes for text debug output—no manual prefix needed
- Use separate TERM windows for each COG: `debug(`term COG0, ...)`, `debug(`term COG1, ...)`
- Add brief delays between DEBUG calls in different COGs if message interleaving is problematic
- Debug one COG at a time during initial development for clearest output

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


# Part II: Instruction Set Reference

