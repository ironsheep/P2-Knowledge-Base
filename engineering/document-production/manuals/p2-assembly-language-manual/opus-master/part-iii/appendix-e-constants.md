# Appendix E: Predefined Constants

PASM2 provides a set of predefined constants that the assembler substitutes at compile time. These constants do not generate code themselves but provide standardized values for common operations including boolean logic, numeric bounds, mathematical calculations, and execution mode control.

## Boolean Constants

::: constheader
### TRUE {#true}
Logical True Constant

All bits set ($FFFFFFFF / -1).
:::

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
```pasm2
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



::: constheader
### FALSE {#false}
Logical False Constant

All bits cleared ($00000000 / 0).
:::

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
```pasm2
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

::: constheader
### NEGX {#negx}
Maximum Negative Integer

Most negative 32-bit signed value ($80000000).
:::

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
```pasm2
' Checking for negative underflow
                cmps    value, ##NEGX   wc      ' Check if below min neg
        if_c    jmp     #underflow              ' Jump if underflow

' Using NEGX as lower limit
                mov     limit, ##NEGX           ' Set limit to max negative
                fges    value, limit            ' Clamp to not go below NEGX
```

#### Notes
- Represents -2³¹ in decimal notation
- Bit 31 set, bits 30-0 clear
- Used for saturation arithmetic and bounds checking
- Special case: `abs(NEGX) = NEGX` due to two's complement representation (no positive equivalent exists)

#### Related Constants
- [POSX](#posx) — Maximum positive integer constant



::: constheader
### POSX {#posx}
Maximum Positive Integer

Most positive 32-bit signed value ($7FFFFFFF).
:::

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
```pasm2
' Checking for positive overflow
                cmp     value, ##POSX   wc      ' Check if exceeds max
        if_nc   jmp     #overflow               ' Jump if overflow

' Using POSX as upper limit
                mov     limit, ##POSX           ' Set limit to max positive
                fles    value, limit            ' Clamp to not exceed POSX
```

#### Notes
- Represents 2³¹ - 1 in decimal notation
- Bit 31 clear, bits 30-0 set
- Used for saturation arithmetic and bounds checking
- One less than 2³¹ due to zero occupying one value in the range

#### Related Constants
- [NEGX](#negx) — Maximum negative integer constant



## Mathematical Constants

::: constheader
### PI {#pi}
Mathematical Pi Constant

IEEE 754 single-precision π ($40490FDB).
:::

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
```pasm2
' Using PI with CORDIC rotation
        mov     angle, ##PI         ' Load PI constant
        shr     angle, #1           ' Divide by 2 for PI/2 (90 degrees)
        qrotate angle, radius       ' Rotate by PI/2 radians

' Converting radians to degrees using PI
        mov     x, ##PI             ' Start with PI
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

::: constheader
### COGEXEC {#cogexec}
Cog Execution Mode

Load code from hub to cog RAM and execute.
:::

Execution mode constant for loading code from hub RAM to cog RAM.

#### Value
| Representation | Value |
|----------------|-------|
| Binary | %0_0_0000 |
| Hexadecimal | $00 |

#### Description
COGEXEC specifies cog execution mode for the COGINIT instruction. When used, COGINIT loads 504 longs from hub RAM into cog RAM registers $000-$1F7 and begins execution at cog address $000. This mode provides maximum execution speed since all instructions execute from fast cog RAM.

#### Usage
```pasm2
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
- Loads cog RAM registers $000-$1F7 (504 longs) from hub RAM
- Begins execution at cog register address $000
- Must specify target cog ID (0-7)
- Fastest execution mode due to cog RAM access speeds
- Code size limited to 504 longs (2KB minus the 8 special-purpose registers at $1F8-$1FF)

#### Related Constants
- [HUBEXEC](#hubexec) — hub execution mode constant
- [COGEXEC_NEW](#cogexec_new) — Auto-select available cog variant
- [COGEXEC_NEW_PAIR](#cogexec_new_pair) — Auto-select adjacent cog pair variant



::: constheader
### HUBEXEC {#hubexec}
Hub Execution Mode

Execute code directly from hub RAM.
:::

Execution mode constant for executing code directly from hub RAM.

#### Value
| Representation | Value |
|----------------|-------|
| Binary | %1_0_0000 |
| Hexadecimal | $20 |

#### Description
HUBEXEC specifies hub execution mode for the COGINIT instruction. When used, COGINIT starts the target cog executing instructions directly from hub RAM without loading code to cog RAM. This mode removes code size restrictions at the cost of slower instruction fetch times.

#### Usage
```pasm2
' Start specific cog with hub execution
        COGINIT #HUBEXEC+1, ##$400   ' Cog 1 from Hub RAM $400

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
- Hub execution allows unlimited code size (not limited to 504 longs)
- Slower than cog execution due to hub RAM access timing and FIFO overhead
- Instruction fetching occurs through FIFO/streamer mechanism
- Must specify target cog ID (0-7)
- Each cog maintains its own program counter for hub execution

#### Related Constants
- [COGEXEC](#cogexec) — cog execution mode constant
- [HUBEXEC_NEW](#hubexec_new) — Auto-select available cog variant
- [HUBEXEC_NEW_PAIR](#hubexec_new_pair) — Auto-select adjacent cog pair variant



## Execution Mode Variants

The execution mode constants include additional variants for automatic cog selection. These variants combine the base execution mode (COGEXEC or HUBEXEC) with automatic resource selection flags, eliminating the need to manually specify cog IDs.

::: constheader
### COGEXEC_NEW {#cogexec_new}
Auto-Select Cog For Cog Execution

Auto-selects available cog for COGEXEC mode.
:::

Execution mode constant for automatically selecting an available cog with cog RAM execution.

#### Encoding
Combines COGEXEC base mode with the N (new cog) flag set. The assembler resolves this to the appropriate bit pattern for COGINIT's Dest operand.

#### Description
COGEXEC_NEW instructs COGINIT to find the next available (stopped) cog, load 504 longs from hub RAM into that cog's RAM, and begin execution at cog address $000. This mode provides maximum execution speed since all instructions execute from fast cog RAM.

#### Usage
```pasm2
' Start any available cog with code load
                coginit #COGEXEC_NEW, ##@cog_code  wc
        if_c    jmp     #no_cog_available
```

#### Notes
- Use WC to detect if no cog was available (C=1 on failure)
- With WC and register Dest, the launched cog's ID is returned
- Equivalent to COGEXEC with N=1 in the %E_N_xVVV encoding

#### Related Constants
- [COGEXEC](#cogexec) — Base cog execution mode (specific cog)
- [COGEXEC_NEW_PAIR](#cogexec_new_pair) — Auto-select adjacent cog pair variant


::: constheader
### COGEXEC_NEW_PAIR {#cogexec_new_pair}
Auto-Select Cog Pair For Cog Execution

Auto-selects adjacent cog pair for COGEXEC mode.
:::

Execution mode constant for automatically selecting an adjacent pair of available cogs with cog RAM execution.

#### Encoding
Combines COGEXEC base mode with both the N (new cog) and pair selection flags set.

#### Description
COGEXEC_NEW_PAIR instructs COGINIT to find an adjacent pair of available cogs (0-1, 2-3, 4-5, or 6-7), load code into the first cog, and start execution. Adjacent cog pairs can share their LUT memory via SETLUTS, enabling efficient inter-cog communication and data sharing.

#### Usage
```pasm2
' Start a cog pair for LUT sharing
                coginit #COGEXEC_NEW_PAIR, ##@pair_code  wc
        if_c    jmp     #no_pair_available
```

#### Notes
- Requires two adjacent, stopped cogs to succeed
- The returned cog ID is the lower of the pair (0, 2, 4, or 6)
- Adjacent pairs can share LUT memory for fast inter-cog communication
- Use SETLUTS to configure LUT sharing after both cogs are running

#### Related Constants
- [COGEXEC](#cogexec) — Base cog execution mode
- [COGEXEC_NEW](#cogexec_new) — Single cog auto-select variant


::: constheader
### HUBEXEC_NEW {#hubexec_new}
Auto-Select Cog For Hub Execution

Auto-selects available cog for HUBEXEC mode.
:::

Execution mode constant for automatically selecting an available cog with hub RAM execution.

#### Encoding
Combines HUBEXEC base mode with the N (new cog) flag set.

#### Description
HUBEXEC_NEW instructs COGINIT to find the next available (stopped) cog and start it executing instructions directly from hub RAM without loading code to cog RAM. This mode removes the 504-long code size limitation at the cost of slower instruction fetch times due to hub access latency.

#### Usage
```pasm2
' Start any available cog in hub execution mode
                coginit #HUBEXEC_NEW, ##@hub_code  wc
        if_c    jmp     #no_cog_available
```

#### Notes
- Hub execution allows unlimited code size
- Instruction fetching uses the FIFO/streamer mechanism
- Slower than cog execution due to hub RAM access timing
- Use WC to detect failure and retrieve the launched cog's ID

#### Related Constants
- [HUBEXEC](#hubexec) — Base hub execution mode (specific cog)
- [HUBEXEC_NEW_PAIR](#hubexec_new_pair) — Auto-select adjacent cog pair variant


::: constheader
### HUBEXEC_NEW_PAIR {#hubexec_new_pair}
Auto-Select Cog Pair For Hub Execution

Auto-selects adjacent cog pair for HUBEXEC mode.
:::

Execution mode constant for automatically selecting an adjacent pair of available cogs with hub RAM execution.

#### Encoding
Combines HUBEXEC base mode with both the N (new cog) and pair selection flags set.

#### Description
HUBEXEC_NEW_PAIR instructs COGINIT to find an adjacent pair of available cogs and start them executing from hub RAM. This combines the unlimited code size of hub execution with the LUT sharing capability of cog pairs.

#### Usage
```pasm2
' Start a cog pair for hub execution with LUT sharing
                coginit #HUBEXEC_NEW_PAIR, ##@hub_pair_code  wc
        if_c    jmp     #no_pair_available
```

#### Notes
- Combines unlimited hub code size with LUT sharing capability
- Requires two adjacent, stopped cogs to succeed
- The returned cog ID is the lower of the pair
- Use SETLUTS to configure LUT sharing after both cogs are running

#### Related Constants
- [HUBEXEC](#hubexec) — Base hub execution mode
- [HUBEXEC_NEW](#hubexec_new) — Single cog auto-select variant


These variants simplify cog management by allowing the system to automatically assign available cogs rather than requiring explicit cog ID specification. Always use WC with COGINIT when using these variants to detect allocation failures.



## Debug Configuration Constants

The P2's debug system operates at three distinct levels, each controlled by CON constants defined in the program. Code instrumentation constants control whether DEBUG statements compile into the program. Output infrastructure constants configure the debug serial communication system. Breakpoint constants configure automatic breaks for single-step debugging.

### Code Instrumentation Constants

These constants control compile-time behavior. When debug statements are disabled, the assembler generates no code for them—zero runtime overhead.

::: constheader
### DEBUG_DISABLE {#debug-disable}
Disable All Debug Statements

Prevents all DEBUG statements from compiling (0 = enabled, non-zero = disabled).
:::

Compile-time constant that globally disables all DEBUG statements.

#### Value

| Value | Effect |
|-------|--------|
| 0 or undefined | DEBUG statements compile normally |
| Non-zero | All DEBUG statements are omitted from compilation |

#### Description

DEBUG_DISABLE provides a master switch for debug output. When defined as any non-zero value, the assembler skips all DEBUG statements entirely—no code is generated, no runtime overhead exists. This enables maintaining debug instrumentation in source code while producing release binaries with zero debug footprint.

#### Usage

```spin2
CON
  DEBUG_DISABLE = 1       ' Set to 1 for release, 0 for development

DAT
        org
entry   debug("This generates no code when DEBUG_DISABLE = 1")
        ' ... program code ...
```

#### Notes

- Must be defined as an integer constant in a CON block
- Affects both standard `debug()` and selective `debug[N]()` statements
- The check occurs at compile time; disabled statements produce zero bytes
- Works identically in Spin2 PUB/PRI blocks and PASM2 DAT blocks

#### Related Constants

- [DEBUG_MASK](#debug-mask) — Selective channel control



::: constheader
### DEBUG_MASK {#debug-mask}
Selective Debug Channel Mask

32-bit mask controlling which debug[N]() channels compile (bit N = channel N).
:::

Compile-time constant enabling selective debug channel compilation.

#### Value

| Bit | Channel | Binary Mask |
|-----|---------|-------------|
| 0 | debug[0] | %00000000_00000000_00000000_00000001 |
| 1 | debug[1] | %00000000_00000000_00000000_00000010 |
| 2 | debug[2] | %00000000_00000000_00000000_00000100 |
| ... | ... | ... |
| 31 | debug[31] | %10000000_00000000_00000000_00000000 |

#### Description

DEBUG_MASK provides fine-grained control over debug output by channel. Each bit in the 32-bit mask corresponds to a debug channel numbered 0 through 31. The `debug[N]()` statement compiles only if bit N is set in DEBUG_MASK. Standard `debug()` statements without a channel number are unaffected by DEBUG_MASK.

This mechanism enables categorizing debug output by subsystem, verbosity level, or development phase. Changing a single constant recompiles only the desired debug channels.

#### Usage

```spin2
CON
  ' Channel assignments
  DBG_INIT   = 0              ' Initialization messages
  DBG_MOTOR  = 1              ' Motor control
  DBG_SENSOR = 2              ' Sensor readings
  DBG_ERROR  = 3              ' Error conditions

  ' Enable only initialization and errors
  DEBUG_MASK = (1 << DBG_INIT) | (1 << DBG_ERROR)

DAT
        org
entry   debug[DBG_INIT]("Starting")     ' COMPILED - bit 0 set
        debug[DBG_MOTOR]("Motor on")    ' NOT compiled - bit 1 clear
        debug[DBG_SENSOR]("Reading")    ' NOT compiled - bit 2 clear
        debug[DBG_ERROR]("Fault!")      ' COMPILED - bit 3 set
```

#### Notes

- Must be defined as an integer constant for `debug[N]()` to compile
- If DEBUG_MASK is undefined, using `debug[N]()` causes a compile error
- A mask of 0 disables all numbered channels; standard `debug()` still works
- A mask of $FFFF_FFFF (-1) enables all 32 channels
- Channel numbers outside 0-31 cause a compile error

#### Related Constants

- [DEBUG_DISABLE](#debug-disable) — Global debug disable
- [DEBUG_COGS](#debug-cogs) — Runtime cog filtering



### Output Infrastructure Constants

These constants configure the debug output system that handles all DEBUG statement output. They are patched into the debugger binary and affect serial communication parameters and output formatting.

::: constheader
### DEBUG_COGS {#debug-cogs}
Debug-Enabled Cog Mask

8-bit mask specifying which cogs can produce debug output (bit N = Cog N).
:::

Runtime constant controlling which cogs can trigger debug output.

#### Value

| Bit | Cog | Binary Mask |
|-----|-----|-------------|
| 0 | Cog 0 | %00000001 |
| 1 | Cog 1 | %00000010 |
| 2 | Cog 2 | %00000100 |
| 3 | Cog 3 | %00001000 |
| 4 | Cog 4 | %00010000 |
| 5 | Cog 5 | %00100000 |
| 6 | Cog 6 | %01000000 |
| 7 | Cog 7 | %10000000 |

#### Description

DEBUG_COGS controls runtime debug capability per cog. If a cog's bit is clear, DEBUG statements executing on that cog produce no output—the debug interrupt is ignored. This operates independently from DEBUG_MASK: DEBUG_MASK controls compile-time code generation, while DEBUG_COGS controls runtime output permission.

For a DEBUG statement to produce output, both conditions must be met: the statement must compile (DEBUG_MASK allows it or it's a standard `debug()`), and the executing cog must have its bit set in DEBUG_COGS.

#### Usage

```spin2
CON
  DEBUG_COGS = %00000011      ' Only Cogs 0 and 1 produce output

DAT
        org
entry   debug("From Cog 0")           ' Output appears
        cogspin(NEWCOG, worker, @stack)

worker  debug("From worker")          ' Output only if on Cog 0 or 1
```

#### Notes

- Default behavior (undefined): all cogs can produce debug output
- Must be defined as an integer constant
- Reduces debug overhead in multi-cog applications
- Useful for isolating debug output from specific cogs during development

#### Related Constants

- [DEBUG_MASK](#debug-mask) — Compile-time channel filtering



::: constheader
### DEBUG_DELAY {#debug-delay}
Debug Startup Delay

Milliseconds to wait before debug system begins operation.
:::

Startup delay before any debug output occurs.

#### Value

| Type | Range |
|------|-------|
| Integer | 0 to practical limit (milliseconds) |

#### Description

DEBUG_DELAY specifies a delay in milliseconds before the debug system begins operation. This delay occurs before the application launches, providing time for serial terminals to connect. The delay is calculated as `(CLKFREQ / 1000) * DEBUG_DELAY` and executed during debugger initialization.

#### Usage

```spin2
CON
  DEBUG_DELAY = 2000          ' Wait 2 seconds for terminal connection

DAT
        org
entry   debug("This appears after 2 seconds")
```

#### Notes

- Must be defined as an integer constant
- Value is in milliseconds
- The delay occurs before any application code executes
- Useful when the host serial terminal needs connection time

#### Related Constants

- [DEBUG_BAUD](#debug-baud) — Communication baud rate



::: constheader
### DEBUG_TIMESTAMP {#debug-timestamp}
Enable Debug Timestamps

Adds timing information to all debug output.
:::

Enables timestamps in debug messages.

#### Value

| Definition | Effect |
|------------|--------|
| Defined (any value) | Timestamps enabled |
| Undefined | No timestamps |

#### Description

DEBUG_TIMESTAMP enables timing information in all debug output. When defined, each debug message includes a timestamp relative to program start. This aids timing analysis and performance profiling by showing when events occur.

#### Usage

```spin2
CON
  DEBUG_TIMESTAMP = TRUE

DAT
        org
entry   debug("Started")              ' Output includes timestamp
        waitms(100)
        debug("After delay")          ' Timestamp shows ~100ms elapsed
```

#### Notes

- The value is irrelevant; defining the symbol enables timestamps
- Timestamps appear on all debug output, not selectively
- Useful for profiling and timing-sensitive debugging

#### Related Constants

- [DEBUG_DELAY](#debug-delay) — Startup delay



::: constheader
### DEBUG_PIN_TX {#debug-pin-tx}
Debug Transmit Pin

P2 pin number for debug serial transmit.
:::

Configures the debug serial transmit pin.

#### Value

| Type | Default | Range |
|------|---------|-------|
| Integer | 62 | 0-63 |

#### Description

DEBUG_PIN_TX specifies which P2 pin transmits debug serial data to the host. The default pin 62 matches standard development board configurations where pins 62-63 connect to the USB-serial interface.

#### Usage

```spin2
CON
  DEBUG_PIN_TX = 62           ' Use default transmit pin
```

#### Notes

- Must be defined as an integer constant
- DEBUG_PIN is an alias for DEBUG_PIN_TX
- Default matches Parallax development board pinout

#### Related Constants

- [DEBUG_PIN_RX](#debug-pin-rx) — Receive pin
- [DEBUG_BAUD](#debug-baud) — Baud rate



::: constheader
### DEBUG_PIN_RX {#debug-pin-rx}
Debug Receive Pin

P2 pin number for debug serial receive.
:::

Configures the debug serial receive pin.

#### Value

| Type | Default | Range |
|------|---------|-------|
| Integer | 63 | 0-63 |

#### Description

DEBUG_PIN_RX specifies which P2 pin receives debug serial data from the host. The default pin 63 matches standard development board configurations.

#### Usage

```spin2
CON
  DEBUG_PIN_RX = 63           ' Use default receive pin
```

#### Notes

- Must be defined as an integer constant
- Used for bidirectional debug communication with host
- Default matches Parallax development board pinout

#### Related Constants

- [DEBUG_PIN_TX](#debug-pin-tx) — Transmit pin
- [DEBUG_BAUD](#debug-baud) — Baud rate



::: constheader
### DEBUG_BAUD {#debug-baud}
Debug Baud Rate

Serial communication speed for debug output.
:::

Configures the debug serial baud rate.

#### Value

| Type | Default | Typical Values |
|------|---------|----------------|
| Integer | DOWNLOAD_BAUD | 115200, 230400, 921600, 2000000 |

#### Description

DEBUG_BAUD sets the serial communication speed for all debug output. Higher baud rates reduce debug overhead but require host terminal support. The default uses the same baud rate as the download connection.

#### Usage

```spin2
CON
  DEBUG_BAUD = 2_000_000      ' 2 Mbaud for fast debug output
```

#### Notes

- Must be defined as an integer constant
- Higher rates reduce per-statement timing impact
- Host terminal must support the configured rate
- 2 Mbaud is common for development; lower rates for compatibility

#### Related Constants

- [DEBUG_PIN_TX](#debug-pin-tx) — Transmit pin
- [DEBUG_PIN_RX](#debug-pin-rx) — Receive pin



### Breakpoint Configuration Constants

These constants configure automatic breakpoints for single-step debugging. They instruct the debugger to halt execution at specific points, enabling interactive debugging.

::: constheader
### DEBUG_MAIN {#debug-main}
Break at Program Start

Triggers a breakpoint when the main program begins.
:::

Configures the debugger to break at program entry.

#### Value

| Definition | Effect |
|------------|--------|
| Defined (any value) | Break at main entry |
| Undefined | No automatic break |

#### Description

DEBUG_MAIN instructs the debugger to trigger a breakpoint at the start of the main program. Execution halts before any user code runs, allowing single-stepping from the first instruction. This is essential for debugging initialization issues or understanding program flow from the beginning.

#### Usage

```spin2
CON
  DEBUG_MAIN                  ' Break at program start

PUB main()
  ' Debugger breaks here before any code executes
  initialize()
```

#### Notes

- The value is irrelevant; defining the symbol enables the break
- Takes precedence over DEBUG_COGINIT if both are defined
- Enables single-stepping from program entry
- Used for debugging startup and initialization code

#### Related Constants

- [DEBUG_COGINIT](#debug-coginit) — Break on cog initialization



::: constheader
### DEBUG_COGINIT {#debug-coginit}
Break on Cog Initialization

Triggers a breakpoint when any cog is initialized.
:::

Configures the debugger to break on cog startup.

#### Value

| Definition | Effect |
|------------|--------|
| Defined (any value) | Break on each COGINIT/COGSPIN |
| Undefined | No automatic break |

#### Description

DEBUG_COGINIT instructs the debugger to trigger a breakpoint whenever a COGINIT or COGSPIN instruction executes. This enables debugging multi-cog applications by providing an opportunity to examine state before each new cog begins execution.

#### Usage

```spin2
CON
  DEBUG_COGINIT               ' Break on every cog initialization

PUB main()
  cogspin(NEWCOG, worker(), @stack)   ' Debugger breaks here
```

#### Notes

- The value is irrelevant; defining the symbol enables the break
- DEBUG_MAIN takes precedence if both are defined
- Useful for debugging cog startup and inter-cog coordination
- Each COGINIT or COGSPIN triggers a separate break

#### Related Constants

- [DEBUG_MAIN](#debug-main) — Break at program start
- [DEBUG_COGS](#debug-cogs) — Runtime cog filtering



## Hardware Configuration Constants

The P2 provides extensive predefined constants for configuring its hardware subsystems. These constants are documented in dedicated reference sections:

### SmartPin Constants

The P2's 64 smart pins each function as independent hardware peripherals. Over 50 predefined constants configure input selection, filtering, output control, and the 32 operating modes including DAC, ADC, PWM, serial communication, and counters.

**See:** [SmartPin Configuration Constants](smartpin-constants.md)

### Streamer Constants

The streamer is the P2's DMA-like engine for high-bandwidth data transfer between hub RAM, LUT, pins, and DAC outputs. Over 80 predefined constants configure data sources, destinations, formats, color modes, and control flags.

**See:** [Streamer Configuration Constants](streamer-constants.md)



## Constants Summary

| Category | Count | Purpose |
|----------|-------|---------|
| Boolean | 2 | TRUE, FALSE for logical operations |
| Numeric Limits | 2 | NEGX, POSX for bounds checking |
| Mathematical | 1 | PI for CORDIC and floating-point |
| Execution Mode | 6 | COGEXEC, HUBEXEC and variants |
| Debug Configuration | 10 | DEBUG_DISABLE, DEBUG_MASK, infrastructure |
| SmartPin | 59 | Pin configuration and modes |
| Streamer | 85 | Data streaming and video |
| **Total** | **165** | Core predefined constants |

*Note: Clock configuration constants (RCFAST, RCSLOW, XI, PLL, XDIV*, XMUL*, etc.) add over 1,000 additional symbols for system clock setup.*

