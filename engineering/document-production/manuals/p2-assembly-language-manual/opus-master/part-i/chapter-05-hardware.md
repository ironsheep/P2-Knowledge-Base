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
