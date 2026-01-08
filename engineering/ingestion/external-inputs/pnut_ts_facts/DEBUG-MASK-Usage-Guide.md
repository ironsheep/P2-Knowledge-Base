# Debug Configuration and Selective Debug Usage Guide for Spin2/PASM2

This document describes the debug configuration constants and the selective `debug[N]()` form in the Spin2 and PASM2 languages for the Parallax Propeller 2 (P2) microcontroller.

## Language Version Requirement

**The selective debug feature (`debug[N]()` with `DEBUG_MASK`) requires Spin2 version 46 or later.**

To use selective debug channels in your code, you must include the language version directive at the very beginning of your source file:

```spin2
{Spin2_v46}
CON
  DEBUG_MASK = %0101          ' Enable channels 0 and 2

PUB go()
  debug[0]("Channel 0 message")
  debug[2]("Channel 2 message")
```

The directive `{Spin2_v46}` (or a later version like `{Spin2_v51}`) must appear before any other code.

**Note**: Basic debug statements (`debug()` without channel numbers) and most debug configuration constants (`DEBUG_DISABLE`, `DEBUG_COGS`, etc.) are part of the base Spin2 language and do not require a version directive.

## Overview

The P2's debug system operates at three distinct levels:

1. **Code Instrumentation (Compile-Time)**: Controls whether `debug()` statements generate code at all
2. **Debug Output Infrastructure**: Configures the debug system that handles all `debug()` output
3. **Automatic Breakpoint Configuration**: Configures breakpoints for single-step debugging

Understanding this distinction is critical: code instrumentation constants affect what code is compiled, while debug output infrastructure constants configure the runtime debug system that handles all debug messages.

---

# Part 1: Code Instrumentation (Compile-Time)

These constants control whether `debug()` statements are compiled into your program. They are evaluated during compilation and determine if debug code is generated.

**Key Point:** When debug statements are disabled via these constants, they produce **zero code** - no runtime overhead whatsoever.

| Symbol | Purpose |
|--------|---------|
| `DEBUG_DISABLE` | Globally disable ALL debug statements at compile time |
| `DEBUG_MASK` | 32-bit mask to selectively enable/disable `debug[N]()` channels |
| `debug[N](...)` | Channel-specific debug statement (compiled only if bit N is set in DEBUG_MASK) |

---

## DEBUG_DISABLE

### Purpose

`DEBUG_DISABLE` is a CON constant that, when defined as a non-zero value, completely disables all debug statements in the program. The debug code is not compiled at all, resulting in smaller binary size and no runtime overhead.

### Syntax

```spin2
CON
  DEBUG_DISABLE = 1       ' Disable all debug (non-zero = disabled)
  ' or
  DEBUG_DISABLE = 0       ' Enable debug (zero = enabled)
```

### How It Works

1. If `DEBUG_DISABLE` is not defined, debug statements are compiled normally (when -d flag is used)
2. If `DEBUG_DISABLE = 0`, debug statements are compiled normally
3. If `DEBUG_DISABLE` is any non-zero value, ALL debug statements are skipped during compilation

### Examples

#### Disabling Debug for Release Build

```spin2
CON
  DEBUG_DISABLE = 1       ' Set to 1 for release, 0 for development

PUB main()
  debug("This will NOT appear in the binary")  ' Skipped when DEBUG_DISABLE = 1
  ' ... rest of program
```

#### Using Expressions

```spin2
CON
  RELEASE_BUILD = 1
  DEBUG_DISABLE = RELEASE_BUILD   ' Disable debug for release builds

  ' Or use computed values
  DEBUG_OBJECT_MASK = $FFFF
  DEBUG_OBJECT_BIT  = $0100
  DEBUG_DISABLE = (DEBUG_OBJECT_MASK & DEBUG_OBJECT_BIT)  ' Computed at compile time
```

### Notes

- `DEBUG_DISABLE` must be defined as an integer constant (not a float or string)
- The check is performed at compile time, so disabled debug statements add zero overhead
- Works in both Spin2 and PASM2 code

---

## DEBUG_MASK

### Purpose

`DEBUG_MASK` is a 32-bit CON constant that provides fine-grained control over which debug statements are compiled. Each bit in the mask corresponds to a debug "channel" numbered 0 through 31.

### Syntax

```spin2
CON
  DEBUG_MASK = %00000000_00000000_00000000_00001111  ' Enable channels 0-3
  ' or
  DEBUG_MASK = $0000_000F    ' Same as above, hex notation
  ' or
  DEBUG_MASK = 15            ' Same as above, decimal
```

### Bit Mapping

| Bit | Channel | Binary Mask |
|-----|---------|-------------|
| 0   | debug[0] | `%00000000_00000000_00000000_00000001` |
| 1   | debug[1] | `%00000000_00000000_00000000_00000010` |
| 2   | debug[2] | `%00000000_00000000_00000000_00000100` |
| 3   | debug[3] | `%00000000_00000000_00000000_00001000` |
| ... | ... | ... |
| 31  | debug[31] | `%10000000_00000000_00000000_00000000` |

### Examples

```spin2
CON
  DEBUG_MASK = %0101          ' Enable channels 0 and 2 only

PUB main()
  debug[0]("Channel 0")       ' COMPILED - bit 0 is set
  debug[1]("Channel 1")       ' NOT compiled - bit 1 is clear
  debug[2]("Channel 2")       ' COMPILED - bit 2 is set
  debug[3]("Channel 3")       ' NOT compiled - bit 3 is clear
```

### Notes

- `DEBUG_MASK` must be defined as an integer constant
- If `DEBUG_MASK` is not defined, using `debug[N]()` causes a compile error
- A mask of 0 disables all numbered debug channels (but regular `debug()` still works)
- A mask of `$FFFF_FFFF` (-1) enables all 32 channels

---

## debug[N](...) - Selective Debug Statements

### Purpose

The `debug[N](...)` form allows you to categorize debug statements into channels (0-31) that can be individually enabled or disabled via the `DEBUG_MASK` constant.

### Syntax

```spin2
debug[channel]("message", values...)
```

Where:
- `channel` is an integer constant from 0 to 31
- The parentheses contain standard debug() content (strings, format specifiers, values)

### Requirements

For `debug[N]()` to compile:
1. Debug must be enabled (via -d compiler flag)
2. `DEBUG_DISABLE` must not be set, or must equal 0
3. `DEBUG_MASK` must be defined
4. Bit N of `DEBUG_MASK` must be set (1)

### Compile-Time Behavior

| Condition | Result |
|-----------|--------|
| Bit N is set (1) in DEBUG_MASK | Debug statement is compiled |
| Bit N is clear (0) in DEBUG_MASK | Debug statement is skipped entirely |
| DEBUG_MASK not defined | Compile error |
| Channel < 0 or > 31 | Compile error |

### Examples

#### Basic Channel Usage

```spin2
CON
  DEBUG_MASK = %0101          ' Enable channels 0 and 2

VAR
  BYTE a
  WORD b
  LONG c

PUB go()
  debug[0]("Bit0", c, z)      ' Enabled - bit 0 is set
  debug[1]("Bit1", c, z)      ' Disabled - bit 1 is clear
  debug[2]("Bit2", c, z)      ' Enabled - bit 2 is set
  debug[3]("Bit3", c, z)      ' Disabled - bit 3 is clear
```

**Result:** Only "Bit0" and "Bit2" debug statements are compiled. The binary contains no code for "Bit1" or "Bit3".

#### Organizing Debug by Category

```spin2
CON
  ' Debug channel assignments
  DBG_INIT   = 0              ' Initialization messages
  DBG_COMM   = 1              ' Communication debugging
  DBG_SENSOR = 2              ' Sensor readings
  DBG_MOTOR  = 3              ' Motor control
  DBG_ERROR  = 4              ' Error conditions

  ' Enable only what you need
  DEBUG_MASK = (1 << DBG_INIT) | (1 << DBG_ERROR)  ' Enable init and errors only

PUB main() | temp
  debug[DBG_INIT]("System starting...")           ' COMPILED
  debug[DBG_COMM]("Comm check")                   ' NOT compiled
  debug[DBG_SENSOR]("Reading sensor")             ' NOT compiled
  debug[DBG_MOTOR]("Motor at ", UDEC(speed))      ' NOT compiled
  debug[DBG_ERROR]("Error: ", UHEX(errorCode))    ' COMPILED
```

#### Using with Standard debug()

Regular `debug()` statements (without channel numbers) are not affected by `DEBUG_MASK`:

```spin2
CON
  DEBUG_MASK = 0              ' All numbered channels disabled

PUB main()
  debug("This ALWAYS compiles when -d is used")   ' Standard debug() works
  debug[0]("This does NOT compile")               ' Channel 0 is disabled
```

---

## PASM2 Usage (Code Instrumentation)

The `debug[N]()` form works identically in PASM2 assembly code:

```spin2
CON
  DEBUG_MASK = %0011          ' Enable channels 0 and 1

DAT
        ORG

entry   debug[0]("PASM Entry")        ' COMPILED
        debug[1]("Loop start")         ' COMPILED
        debug[2]("Not shown")          ' NOT compiled

loop    NOP
        debug[0]("In loop")            ' COMPILED
        JMP     #loop
```

---

## Code Instrumentation Examples

### 1. Development vs Production

```spin2
CON
  ' Set to 1 for production builds
  PRODUCTION = 0

  DEBUG_DISABLE = PRODUCTION

  ' Even if debug is enabled, only show critical info in production tests
  DEBUG_MASK = PRODUCTION ? %00001 : %11111  ' Only channel 0 in production
```

### 2. Module-Specific Debugging

```spin2
CON
  ' Each module gets its own bit
  DBG_UI      = 0
  DBG_NETWORK = 1
  DBG_STORAGE = 2
  DBG_AUDIO   = 3

  ' Enable only the module you're currently debugging
  DEBUG_MASK = 1 << DBG_NETWORK   ' Only network debugging active
```

### 3. Verbosity Levels

```spin2
CON
  DBG_ERROR   = 0     ' Always enabled
  DBG_WARNING = 1
  DBG_INFO    = 2
  DBG_DEBUG   = 3
  DBG_TRACE   = 4

  ' Set verbosity level
  VERBOSITY = 2       ' Show errors, warnings, and info

  ' Create mask for all levels up to VERBOSITY
  DEBUG_MASK = (1 << (VERBOSITY + 1)) - 1   ' %00000111 for VERBOSITY=2
```

---

# Part 2: Debug Output Infrastructure

These constants configure the **debug output system** that handles ALL `debug()` statement output. They are patched into the debugger binary and affect how debug messages are transmitted and formatted.

**Key Point:** These constants affect all debug output, not just single-step debugging. The debugger binary handles both `debug()` statement output and breakpoint-based debugging.

| Symbol | Purpose |
|--------|---------|
| `DEBUG_COGS` | 8-bit mask specifying which cogs have debug capability enabled |
| `DEBUG_DELAY` | Startup delay (ms) before debug system begins operation |
| `DEBUG_TIMESTAMP` | Enable timestamps in all debug output |
| `DEBUG_PIN` / `DEBUG_PIN_TX` | Transmit pin for debug serial communication |
| `DEBUG_PIN_RX` | Receive pin for debug serial communication |
| `DEBUG_BAUD` | Baud rate for debug serial communication |

---

## DEBUG_COGS

### Purpose

`DEBUG_COGS` is an 8-bit CON constant that specifies which cogs have debug capability enabled. Each bit corresponds to a cog (bit 0 = cog 0, bit 1 = cog 1, etc.).

**Important:** This controls whether a cog can trigger debug interrupts at runtime. If a cog's bit is clear, `debug()` statements running on that cog will NOT produce output, even if the code was compiled.

### Syntax

```spin2
CON
  DEBUG_COGS = %11111111      ' Debug all 8 cogs (default behavior)
  DEBUG_COGS = %00000001      ' Debug only cog 0
  DEBUG_COGS = %00000011      ' Debug cogs 0 and 1
```

### Bit Mapping

| Bit | Cog |
|-----|-----|
| 0   | Cog 0 |
| 1   | Cog 1 |
| 2   | Cog 2 |
| 3   | Cog 3 |
| 4   | Cog 4 |
| 5   | Cog 5 |
| 6   | Cog 6 |
| 7   | Cog 7 |

### Interaction with DEBUG_MASK

`DEBUG_COGS` and `DEBUG_MASK` operate at different levels and are independent:

| Constant | Level | Controls |
|----------|-------|----------|
| `DEBUG_MASK` | Compile-time | Whether `debug[N]()` generates code |
| `DEBUG_COGS` | Runtime | Whether a cog can produce debug output |

For a `debug[N]()` statement to produce output:
1. Bit N must be set in `DEBUG_MASK` (compile-time: code is generated)
2. The cog's bit must be set in `DEBUG_COGS` (runtime: cog can trigger debug interrupts)

```spin2
CON
  DEBUG_MASK = %1111          ' Compile debug[0..3]
  DEBUG_COGS = %00000011      ' Only cogs 0 and 1 can output

PUB main()
  debug[0]("From cog 0")      ' Works - cog 0 is enabled
  cogspin(NEWCOG, worker(), @stack)

PRI worker()
  ' This runs on cog 1, 2, 3, etc.
  debug[0]("From worker")     ' Only works if running on cog 0 or 1
```

### Examples

```spin2
CON
  DEBUG_COGS = %00001111      ' Debug cogs 0-3 only

PUB main()
  cogspin(NEWCOG, workerTask(), @stack1)  ' Cog may or may not produce debug output
  ' ...
```

### Notes

- Patched into debugger binary at offset `0xE8` (used with `HUBSET` instruction)
- By default, all cogs are debugged if `DEBUG_COGS` is not defined
- Useful for reducing debug overhead in multi-cog applications
- Must be defined as an integer constant

---

## DEBUG_DELAY

### Purpose

`DEBUG_DELAY` specifies a delay in milliseconds before the debug system begins operation. This delay occurs BEFORE the application is launched, giving time for serial terminals to connect.

**Key Point:** This affects ALL debug output, not just single-step debugging. The delay happens during debugger setup, before any application code runs.

### Syntax

```spin2
CON
  DEBUG_DELAY = 1000          ' Wait 1 second (1000ms) before debug starts
  DEBUG_DELAY = 5000          ' Wait 5 seconds before debug starts
```

### How It Works

The delay is calculated as: `(CLKFREQ / 1000) * DEBUG_DELAY`

This value is patched into the debugger's delay register. During debugger initialization, the debugger executes `waitx _delay_` before launching the application.

### Examples

```spin2
CON
  _clkfreq = 200_000_000
  DEBUG_DELAY = 2000          ' 2 second delay before ANY debug output

PUB main()
  debug("This appears after 2 seconds")
```

### Notes

- Patched into debugger binary at offset `0xE0` (`_delay_`)
- Value is in milliseconds
- Must be defined as an integer constant
- Useful for giving time for serial terminals to connect
- Very large delays may be clamped to the maximum 32-bit value

---

## DEBUG_TIMESTAMP

### Purpose

`DEBUG_TIMESTAMP` enables timestamps in ALL debug output. When enabled, each debug message includes timing information relative to program start.

**Key Point:** This affects all `debug()` output, not just single-step debugging. It's controlled by the MSB of the RX pin configuration.

### Syntax

```spin2
CON
  DEBUG_TIMESTAMP = 1         ' Enable timestamps (any value works)
```

### How It Works

When `DEBUG_TIMESTAMP` is defined, the MSB of the RX pin register is set, which signals the debugger to include timestamp information with every debug message.

### Examples

```spin2
CON
  DEBUG_TIMESTAMP = TRUE

PUB main()
  debug("Started")            ' Output includes timestamp
  waitms(100)
  debug("After 100ms")        ' Timestamp shows ~100ms elapsed
```

### Notes

- Sets bit 7 of the byte at offset `0x147` (MSB of `_rxpin_` register)
- The value doesn't matter; defining the symbol is sufficient
- Timestamps are useful for profiling and timing analysis
- Affects ALL debug() output, not just breakpoints

---

## DEBUG_PIN, DEBUG_PIN_TX, DEBUG_PIN_RX

### Purpose

These constants configure which P2 pins the debug system uses for serial communication with the host. This affects ALL debug output.

### Syntax

```spin2
CON
  DEBUG_PIN = 62              ' TX pin (alias for DEBUG_PIN_TX)
  DEBUG_PIN_TX = 62           ' Transmit pin
  DEBUG_PIN_RX = 63           ' Receive pin
```

### Notes

- `DEBUG_PIN` and `DEBUG_PIN_TX` are equivalent; both set the transmit pin
- Patched into debugger binary at offsets `0x140` (`_txpin_`) and `0x144` (`_rxpin_`)
- Default: TX = 62, RX = 63
- Must be defined as integer constants

---

## DEBUG_BAUD

### Purpose

`DEBUG_BAUD` sets the baud rate for ALL debug serial communication.

### Syntax

```spin2
CON
  DEBUG_BAUD = 2_000_000      ' 2 Mbaud
```

### Notes

- Patched into debugger binary at offset `0x148` (`_baud_`)
- Default: Same as `DOWNLOAD_BAUD`
- Must be defined as an integer constant

---

# Part 3: Automatic Breakpoint Configuration

These constants configure **automatic breakpoints** for single-step debugging. They tell the debugger to break execution at specific points, allowing you to step through code.

**Key Point:** These are specifically for interactive single-step debugging, unlike the debug output infrastructure which affects all `debug()` output.

| Symbol | Purpose |
|--------|---------|
| `DEBUG_MAIN` | Trigger breakpoint at program start |
| `DEBUG_COGINIT` | Trigger breakpoint when any cog is initialized |

---

## DEBUG_MAIN

### Purpose

`DEBUG_MAIN` configures the debugger to trigger a breakpoint at the start of the main program. This allows you to begin single-stepping immediately when the program starts.

### Syntax

```spin2
CON
  DEBUG_MAIN = 1              ' Any value, or just define the symbol
```

### How It Works

When `DEBUG_MAIN` is defined, the debugger's break condition register is set to `0x001`, causing it to break at the very beginning of the main cog's execution.

### Examples

```spin2
CON
  DEBUG_MAIN = TRUE           ' Break at program start

PUB main()
  ' Debugger breaks here, before any code executes
  initialize()
  processData()
```

### Notes

- Patched into debugger binary at offset `0x11C` (`_brkcond_`) with value `0x001`
- The value doesn't matter; defining the symbol is sufficient
- Takes precedence over `DEBUG_COGINIT` if both are defined

---

## DEBUG_COGINIT

### Purpose

`DEBUG_COGINIT` configures the debugger to trigger a breakpoint whenever any cog is initialized. This is useful for debugging cog startup issues or stepping through the initialization of multiple cogs.

### Syntax

```spin2
CON
  DEBUG_COGINIT = 1           ' Any non-zero value, or just define the symbol
```

### How It Works

When `DEBUG_COGINIT` is defined, the debugger's break condition register is set to `0x110`, causing it to break whenever a `COGINIT` or `COGSPIN` instruction is executed.

### Examples

```spin2
CON
  DEBUG_COGINIT = TRUE        ' Break on every cog initialization

PUB main()
  cogspin(NEWCOG, task1(), @stack1)   ' Debugger breaks here
  cogspin(NEWCOG, task2(), @stack2)   ' Debugger breaks here too
```

### Notes

- Patched into debugger binary at offset `0x11C` (`_brkcond_`) with value `0x110`
- The value of `DEBUG_COGINIT` doesn't matter; just defining it enables the feature
- `DEBUG_COGINIT` and `DEBUG_MAIN` are mutually exclusive; if both are defined, `DEBUG_MAIN` takes precedence

---

# Part 4: Host Application Configuration

These constants are intended for configuring the debug display on the host computer. They are read by the compiler but may not be fully utilized in PNut-TS.

**Note:** These values are stored during compilation but their actual usage depends on the host-side debug application (e.g., PNut on Windows).

| Symbol | Purpose | Default |
|--------|---------|---------|
| `DEBUG_LEFT` | Left position of debug window | -1 (auto) |
| `DEBUG_TOP` | Top position of debug window | -1 (auto) |
| `DEBUG_WIDTH` | Width of debug window | -1 (auto) |
| `DEBUG_HEIGHT` | Height of debug window | -1 (auto) |
| `DEBUG_DISPLAY_LEFT` | Left position of debug display area | 0 |
| `DEBUG_DISPLAY_TOP` | Top position of debug display area | 0 |
| `DEBUG_LOG_SIZE` | Size of debug log buffer | 0 |
| `DEBUG_WINDOWS_OFF` | Disable debug windows (non-zero = off) | 0 (enabled) |

### Example

```spin2
CON
  ' Position debug window on host
  DEBUG_LEFT = 100
  DEBUG_TOP = 50
  DEBUG_WIDTH = 800
  DEBUG_HEIGHT = 600

  ' Disable graphical windows if using terminal only
  DEBUG_WINDOWS_OFF = TRUE
```

---

# Error Messages

| Error | Cause |
|-------|-------|
| `DEBUG mask bit-number must be 0..31` | Channel number outside valid range |
| `DEBUG_MASK symbol must be defined for DEBUG[0..31] usage` | Using `debug[N]()` without defining `DEBUG_MASK` |
| `DEBUG_DISABLE can only be defined as an integer constant` | Non-integer value for DEBUG_DISABLE |
| `DEBUG_MASK can only be defined as an integer constant` | Non-integer value for DEBUG_MASK |
| `DEBUG_COGS can only be defined as an integer constant` | Non-integer value for DEBUG_COGS |
| `DEBUG_DELAY can only be defined as an integer constant` | Non-integer value for DEBUG_DELAY |
| `DEBUG_PIN can only be defined as an integer constant` | Non-integer value for DEBUG_PIN |
| `DEBUG_PIN_TX can only be defined as an integer constant` | Non-integer value for DEBUG_PIN_TX |
| `DEBUG_PIN_RX can only be defined as an integer constant` | Non-integer value for DEBUG_PIN_RX |
| `DEBUG_BAUD can only be defined as an integer constant` | Non-integer value for DEBUG_BAUD |

---

# Summary Tables

## Code Instrumentation (Compile-Time)

| Symbol | Type | Purpose | Default |
|--------|------|---------|---------|
| `DEBUG_DISABLE` | CON integer | Disable ALL debug statements at compile time | Not defined (debug enabled) |
| `DEBUG_MASK` | CON integer (32-bit) | Bitmask for which `debug[N]()` channels compile | Not defined (must define for debug[N]) |

| Statement | Purpose | Behavior |
|-----------|---------|----------|
| `debug()` | Standard debug output | Compiled when -d flag used and DEBUG_DISABLE is 0 or undefined |
| `debug[N]()` | Channel-specific debug (0-31) | Compiled only if bit N is set in DEBUG_MASK |

## Debug Output Infrastructure

| Symbol | Type | Debugger Offset | Purpose | Default |
|--------|------|-----------------|---------|---------|
| `DEBUG_COGS` | CON integer (8-bit) | `0xE8` | Which cogs can produce debug output | All cogs ($FF) |
| `DEBUG_DELAY` | CON integer | `0xE0` | Startup delay before debug system starts (ms) | 0 |
| `DEBUG_TIMESTAMP` | CON (any value) | `0x147` bit 7 | Enable timestamps in all debug output | Not defined |
| `DEBUG_PIN_TX` | CON integer | `0x140` | Transmit pin | 62 |
| `DEBUG_PIN_RX` | CON integer | `0x144` | Receive pin | 63 |
| `DEBUG_BAUD` | CON integer | `0x148` | Communication baud rate | DOWNLOAD_BAUD |

## Automatic Breakpoint Configuration

| Symbol | Type | Debugger Offset | Purpose | Default |
|--------|------|-----------------|---------|---------|
| `DEBUG_COGINIT` | CON (any value) | `0x11C` = 0x110 | Break on cog initialization | Not defined |
| `DEBUG_MAIN` | CON (any value) | `0x11C` = 0x001 | Break at program start | Not defined |

## Host Application Configuration

| Symbol | Type | Purpose | Default |
|--------|------|---------|---------|
| `DEBUG_LEFT` | CON integer | Window left position | -1 (auto) |
| `DEBUG_TOP` | CON integer | Window top position | -1 (auto) |
| `DEBUG_WIDTH` | CON integer | Window width | -1 (auto) |
| `DEBUG_HEIGHT` | CON integer | Window height | -1 (auto) |
| `DEBUG_DISPLAY_LEFT` | CON integer | Display area left | 0 |
| `DEBUG_DISPLAY_TOP` | CON integer | Display area top | 0 |
| `DEBUG_LOG_SIZE` | CON integer | Log buffer size | 0 |
| `DEBUG_WINDOWS_OFF` | CON integer | Disable windows (non-zero) | 0 (enabled) |

---

# Best Practices

## Code Instrumentation

1. **Define channel constants**: Use named constants for channel numbers to make code self-documenting

2. **Group related functionality**: Assign channels to functional areas (sensors, motors, communication, etc.)

3. **Use DEBUG_DISABLE for releases**: Set `DEBUG_DISABLE = 1` for production builds to ensure zero debug overhead

4. **Keep DEBUG_MASK near the top**: Define it prominently in your CON block so it's easy to find and modify

5. **Document channel assignments**: Comment what each channel is used for

6. **Use expressions for flexibility**: Calculate DEBUG_MASK using expressions like `(1 << DBG_X) | (1 << DBG_Y)`

7. **Regular debug() for always-on**: Use standard `debug()` for messages that should always appear when debugging is enabled

## Debug Output Infrastructure

8. **Use DEBUG_COGS in multi-cog applications**: Limit debug output to specific cogs to reduce overhead and focus debugging

9. **Add DEBUG_DELAY when needed**: Use DEBUG_DELAY to give time for serial terminals to connect before any debug output begins

10. **Enable DEBUG_TIMESTAMP for timing analysis**: When debugging timing-sensitive code, enable timestamps to see when events occur

## Automatic Breakpoints

11. **Use DEBUG_MAIN for startup debugging**: When troubleshooting initialization issues, use DEBUG_MAIN to break at program start for single-stepping

12. **Use DEBUG_COGINIT for multi-cog debugging**: When debugging cog startup, use DEBUG_COGINIT to break when each cog initializes

---

# Complete Configuration Example

```spin2
{
  Complete Debug Configuration Example
  Demonstrates all debug configuration options
}

CON
  _clkfreq = 200_000_000

  ' ========================================
  ' PART 1: CODE INSTRUMENTATION
  ' Controls what debug code is compiled
  ' ========================================

  DEBUG_DISABLE = 0           ' Set to 1 for release builds (removes ALL debug code)

  ' Channel definitions for selective debug
  DBG_MAIN   = 0
  DBG_INIT   = 1
  DBG_COMM   = 2
  DBG_SENSOR = 3
  DBG_ERROR  = 4

  ' Enable specific channels (only these debug[N]() statements will compile)
  DEBUG_MASK = (1 << DBG_MAIN) | (1 << DBG_INIT) | (1 << DBG_ERROR)

  ' ========================================
  ' PART 2: DEBUG OUTPUT INFRASTRUCTURE
  ' Configures how debug output is transmitted
  ' ========================================

  ' Which cogs can produce debug output
  DEBUG_COGS = %00000011      ' Only cogs 0 and 1

  ' Startup delay before any debug output
  DEBUG_DELAY = 500           ' 500ms delay for terminal connection

  ' Show timestamps on all debug messages
  DEBUG_TIMESTAMP = TRUE

  ' Communication settings
  DEBUG_PIN_TX = 62
  DEBUG_PIN_RX = 63
  DEBUG_BAUD = 2_000_000

  ' ========================================
  ' PART 3: AUTOMATIC BREAKPOINT CONFIGURATION
  ' For single-step debugging
  ' ========================================

  ' Uncomment ONE of these if needed for single-step debugging:
  ' DEBUG_MAIN = TRUE         ' Break at program start
  ' DEBUG_COGINIT = TRUE      ' Break on cog init

  ' ========================================
  ' PART 4: HOST APPLICATION CONFIGURATION
  ' For debug display on host computer
  ' ========================================

  DEBUG_LEFT = 100
  DEBUG_TOP = 100
  DEBUG_WIDTH = 1024
  DEBUG_HEIGHT = 768

PUB main()
  debug[DBG_MAIN]("Program started")      ' Compiled (bit 0 set in DEBUG_MASK)
  debug[DBG_INIT]("Initializing...")      ' Compiled (bit 1 set in DEBUG_MASK)
  debug[DBG_COMM]("Comm check")           ' NOT compiled (bit 2 not set)
  debug[DBG_ERROR]("Error test")          ' Compiled (bit 4 set in DEBUG_MASK)
  debug("Always shows")                    ' Standard debug() always compiles
```

---

# Interaction Between DEBUG_MASK and DEBUG_COGS

These two constants operate at completely different levels:

| Constant | Level | When Applied | Effect |
|----------|-------|--------------|--------|
| `DEBUG_MASK` | Compile-time | During compilation | Controls whether `debug[N]()` generates any code |
| `DEBUG_COGS` | Runtime | When debug ISR triggers | Controls whether a cog can produce debug output |

**For a `debug[N]()` statement to produce output, BOTH conditions must be met:**

1. **Compile-time**: Bit N must be set in `DEBUG_MASK` (otherwise no code is generated)
2. **Runtime**: The cog executing the code must have its bit set in `DEBUG_COGS` (otherwise the debug interrupt is ignored)

### Example

```spin2
CON
  DEBUG_MASK = %0011          ' Compile debug[0] and debug[1]
  DEBUG_COGS = %00000101      ' Only cogs 0 and 2 can output

PUB main()                    ' Runs on cog 0
  debug[0]("Cog 0 channel 0") ' OUTPUT: compiled AND cog 0 enabled
  debug[1]("Cog 0 channel 1") ' OUTPUT: compiled AND cog 0 enabled
  debug[2]("Cog 0 channel 2") ' NO CODE: not compiled (bit 2 not in DEBUG_MASK)

  cogspin(NEWCOG, worker(), @stack)  ' Starts on cog 1

PRI worker()                  ' Runs on cog 1
  debug[0]("Cog 1 channel 0") ' NO OUTPUT: compiled but cog 1 not in DEBUG_COGS
  debug[1]("Cog 1 channel 1") ' NO OUTPUT: compiled but cog 1 not in DEBUG_COGS
```

---

*This document describes debug configuration and selective debug usage in Spin2/PASM2 as implemented in the PNut-TS compiler.*
