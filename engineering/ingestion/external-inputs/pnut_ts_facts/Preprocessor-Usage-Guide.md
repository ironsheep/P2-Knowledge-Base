# Preprocessor Usage Guide

## Overview

The Spin2 preprocessor provides conditional compilation, symbol definition, file inclusion, and diagnostic directives. These directives are processed before compilation begins, allowing code to be configured for different build configurations, platforms, or hardware variants.

Preprocessor directives:
- **Symbol Definition** - `#define`, `#undef`
- **Conditional Compilation** - `#ifdef`, `#ifndef`, `#else`, `#elseifdef`, `#elseifndef`, `#endif`
- **File Inclusion** - `#include`
- **Diagnostics** - `#error`, `#warn`
- **Pragma** - `#pragma exportdef`

All directives begin with `#` at the start of a line (leading whitespace is allowed). Directive names are case-insensitive.

**Important**: The `#` character is also used for constant enumeration in CON sections (e.g., `#0, VALUE1, VALUE2`). This is not a preprocessor directive - it's Spin2 syntax for assigning sequential values to constants.

## Basic Usage

### Defining Symbols

```spin2
' Define a symbol (exists/doesn't exist)
#define DEBUG_MODE

' Define a symbol with a value
#define BUFFER_SIZE 256

' Symbol names are case-insensitive (stored as uppercase internally)
#define MySymbol           ' Same as MYSYMBOL
```

### Conditional Compilation

```spin2
#define USE_SERIAL

CON
#ifdef USE_SERIAL
  TX_PIN = 30
  RX_PIN = 31
  BAUD_RATE = 115200
#endif

PUB main()
#ifdef USE_SERIAL
  serial.start(TX_PIN, RX_PIN, BAUD_RATE)
  serial.str(string("Debug output enabled", 13, 10))
#endif
  ' Main program continues...
```

### Conditional with Else

```spin2
#define CLOCK_200MHZ

CON
#ifdef CLOCK_300MHZ
  CLK_FREQ = 300_000_000
#else
  CLK_FREQ = 200_000_000
#endif

  _clkfreq = CLK_FREQ
```

## Symbol Definition Directives

### #define

Creates a preprocessor symbol. The symbol can optionally have a value.

```spin2
' Symbol without value - used for existence checks
#define FEATURE_ENABLED

' Symbol with numeric value
#define MAX_ITEMS 100

' Symbol with expression value
#define TIMEOUT_MS 5000
```

Symbols defined with `#define` can be:
- Checked for existence with `#ifdef` and `#ifndef`
- Removed with `#undef`
- Overridden by command-line `-D` option

### #undef

Removes a previously defined symbol.

```spin2
#define CLOCK_200MHZ
#define CLOCK_300MHZ

' Override the 200MHz setting when 300MHz is defined
#ifdef CLOCK_300MHZ
#undef CLOCK_200MHZ
#endif
```

Use `#undef` to:
- Remove a default setting when an override is specified
- Ensure mutual exclusivity between configuration options
- Clean up temporary symbols after use

## Conditional Compilation Directives

### #ifdef / #endif

Includes code only if the symbol is defined.

```spin2
#define VERBOSE_LOGGING

PUB process_data(buffer, length) | i
#ifdef VERBOSE_LOGGING
  debug("Processing ", udec(length), " bytes")
#endif

  repeat i from 0 to length - 1
    ' Process buffer[i]...

#ifdef VERBOSE_LOGGING
  debug("Processing complete")
#endif
```

### #ifndef / #endif

Includes code only if the symbol is NOT defined.

```spin2
' Provide default if not specified elsewhere
#ifndef STACK_SIZE
#define STACK_SIZE 256
#endif

VAR
  long stack[STACK_SIZE]
```

### #else

Provides an alternative branch when the condition is false.

```spin2
#ifdef USE_I2C
  i2c.setup(SDA_PIN, SCL_PIN)
#else
  spi.setup(CLK_PIN, MOSI_PIN, MISO_PIN, CS_PIN)
#endif
```

### #elseifdef / #elseifndef

Tests additional conditions after an initial `#ifdef` or `#ifndef`.

```spin2
#define CLOCK_200MHZ

CON
#ifdef CLOCK_300MHZ
  CLK_FREQ = 300_000_000
  CLK_MODE = %1_0000_01_00
#elseifdef CLOCK_250MHZ
  CLK_FREQ = 250_000_000
  CLK_MODE = %1_0000_01_00
#elseifdef CLOCK_200MHZ
  CLK_FREQ = 200_000_000
  CLK_MODE = %1_0000_01_00
#else
  CLK_FREQ = 160_000_000
  CLK_MODE = %1_0000_01_00
#endif
```

### Nested Conditionals

Conditionals can be nested to any depth.

```spin2
#define USE_PSRAM16
#define USE_PSRAM_SLOW

#ifdef USE_PSRAM16
  MA_CHAR_ASHIFT = 1
  MA_CHAR_CYCLES = 4

  #ifdef USE_PSRAM_SLOW
    MA_CLKDIV = 3
    MA_CYMUL = 1
  #else
    MA_CLKDIV = 2
    MA_CYMUL = 2
  #endif

#elseifdef USE_PSRAM8
  MA_CHAR_ASHIFT = 2
  MA_CHAR_CYCLES = 8
#endif
```

## File Inclusion

### #include

Inserts the contents of another file at the directive location.

```spin2
PUB main()

#include "driver_methods"

CON
  ' Constants continue after included content...
```

The included file (`driver_methods.spin2` or `driver_methods`):

```spin2
' -- Included content --

PUB driver_init()
  ' Initialization code...

PUB driver_read() : value
  ' Read operation...

' -- End of included content --
```

**Include file rules:**
- Filename is enclosed in double quotes
- The `.spin2` extension is optional (added automatically if missing)
- Only `.spin2` files can be included
- The file is searched in:
  1. Directories specified by `-I` command-line option
  2. The directory containing the source file

**Include with subdirectory:**

```spin2
#include "inc/utility_methods"
```

## Diagnostic Directives

### #error

Generates a compile-time error with a custom message.

```spin2
#ifndef USE_PSRAM16
#ifndef USE_PSRAM8
#ifndef USE_PSRAM4
#error "Must define exactly one of USE_PSRAM16, USE_PSRAM8, or USE_PSRAM4"
#endif
#endif
#endif
```

Use `#error` to:
- Enforce required configuration
- Detect incompatible option combinations
- Provide clear guidance when configuration is incomplete

### #warn

Generates a compile-time warning without stopping compilation.

```spin2
#ifdef USE_DEPRECATED_API
#warn "USE_DEPRECATED_API is deprecated, migrate to new API"
#endif
```

Use `#warn` to:
- Flag deprecated configurations
- Alert about non-optimal settings
- Provide informational messages during compilation

## Command-Line Options

### -D (Define Symbol)

Defines a preprocessor symbol from the command line, as if `#define` appeared at the start of the file.

```bash
# Define a single symbol
pnut-ts -D DEBUG_MODE source.spin2

# Define multiple symbols
pnut-ts -D DEBUG_MODE -D CLOCK_300MHZ source.spin2
```

Command-line defines:
- Take effect before any source code is processed
- Override `#define` directives in source code
- Are visible in all files (including `#include` files)

### -U (Undefine Symbol)

Prevents a symbol from being defined, even if `#define` appears in source code.

```bash
# Prevent DEBUG_MODE from being defined
pnut-ts -U DEBUG_MODE source.spin2
```

Use `-U` to:
- Override default settings in source files
- Create release builds without modifying source
- Test configurations without editing code

### -I (Include Directory)

Adds directories to the search path for `#include` files.

```bash
# Add single include directory
pnut-ts -I /path/to/includes source.spin2

# Add multiple include directories
pnut-ts -I ./common -I ./drivers source.spin2
```

Include directories are searched in order:
1. Directories from `-I` options (in order specified)
2. Directory containing the source file

## Pragma Directive

### #pragma exportdef

Exports a symbol definition to child objects and subsequent compilations.

```spin2
#pragma exportdef HARDWARE_REV 2

' Child objects will have HARDWARE_REV defined
OBJ
  sensor : "sensor_driver"
```

The exported symbol acts like a `-D` option for child objects. This allows a top-level object to configure symbols that propagate to all dependencies.

**Interaction with command line:**
- `-U` on command line prevents `#pragma exportdef` from taking effect
- `-D` on command line takes precedence over `#pragma exportdef`

## Patterns

### Debug vs Release Builds

```spin2
' Source file with debug code
#define DEBUG_BUILD

PUB process(data) | result
#ifdef DEBUG_BUILD
  debug("Input: ", uhex(data))
#endif

  result := transform(data)

#ifdef DEBUG_BUILD
  debug("Output: ", uhex(result))
#endif
  return result
```

Build commands:
```bash
# Debug build (uses #define in source)
pnut-ts source.spin2

# Release build (removes debug code)
pnut-ts -U DEBUG_BUILD source.spin2
```

### Hardware Configuration Selection

```spin2
' Default to P2 Edge board
#ifndef BOARD_TYPE
#define BOARD_P2EDGE
#endif

CON
#ifdef BOARD_P2EDGE
  LED_PIN = 56
  BUTTON_PIN = 57
#elseifdef BOARD_P2EVAL
  LED_PIN = 0
  BUTTON_PIN = 1
#elseifdef BOARD_CUSTOM
  LED_PIN = 16
  BUTTON_PIN = 17
#else
#error "Unknown BOARD_TYPE - define BOARD_P2EDGE, BOARD_P2EVAL, or BOARD_CUSTOM"
#endif
```

### Feature Flags

```spin2
#define FEATURE_LOGGING
#define FEATURE_NETWORKING
' #define FEATURE_BLUETOOTH  ' Disabled

OBJ
#ifdef FEATURE_LOGGING
  log : "logger"
#endif
#ifdef FEATURE_NETWORKING
  net : "network_driver"
#endif
#ifdef FEATURE_BLUETOOTH
  bt : "bluetooth_driver"
#endif
```

### Memory Configuration Variants

```spin2
#define USE_PSRAM16

CON
#ifdef USE_PSRAM16
  MEM_SHIFT = 1
  MEM_CYCLES = 4
  PAGE_SIZE = 512
#elseifdef USE_PSRAM8
  MEM_SHIFT = 2
  MEM_CYCLES = 8
  PAGE_SIZE = 256
#elseifdef USE_PSRAM4
  MEM_SHIFT = 3
  MEM_CYCLES = 16
  PAGE_SIZE = 128
#else
#error "Must define USE_PSRAM16, USE_PSRAM8, or USE_PSRAM4"
#endif
```

### Shared Include Files

Create common definitions in a shared file:

**config.spin2:**
```spin2
' Common configuration
#define SYSTEM_VERSION 1

#ifndef CLOCK_SPEED
#define CLOCK_200MHZ
#endif

#ifdef CLOCK_300MHZ
  CLK_FREQ = 300_000_000
#elseifdef CLOCK_200MHZ
  CLK_FREQ = 200_000_000
#endif
```

**main.spin2:**
```spin2
CON
#include "config"

  _clkfreq = CLK_FREQ

PUB main()
  ' Uses CLK_FREQ from config
```

### Mutual Exclusivity

Ensure only one option from a set is active:

```spin2
#define USE_UART

' Clear conflicting options
#ifdef USE_UART
#undef USE_USB
#undef USE_BLUETOOTH
#endif

#ifdef USE_USB
#undef USE_UART
#undef USE_BLUETOOTH
#endif

' Verify exactly one is set
#ifndef USE_UART
#ifndef USE_USB
#ifndef USE_BLUETOOTH
#error "Must define USE_UART, USE_USB, or USE_BLUETOOTH"
#endif
#endif
#endif
```

## Anti-Patterns

### Deeply Nested Conditionals

```spin2
' WRONG: Hard to read and maintain
#ifdef FEATURE_A
  #ifdef OPTION_1
    #ifdef VARIANT_X
      #ifdef DEBUG
        VALUE = 1
      #else
        VALUE = 2
      #endif
    #else
      VALUE = 3
    #endif
  #else
    VALUE = 4
  #endif
#else
  VALUE = 5
#endif

' CORRECT: Flatten with compound conditions or separate files
#ifdef FEATURE_A
#define HAS_FEATURE_A
#endif
#ifdef OPTION_1
#define HAS_OPTION_1
#endif

' Use simpler structure
#ifdef HAS_FEATURE_A
  #ifdef HAS_OPTION_1
    VALUE = 1
  #else
    VALUE = 4
  #endif
#else
  VALUE = 5
#endif
```

### Unbalanced Conditionals

```spin2
' WRONG: Missing #endif
#ifdef DEBUG_MODE
  debug_init()

PUB main()      ' Error: #endif never found
  process()

' CORRECT: Properly balanced
#ifdef DEBUG_MODE
  debug_init()
#endif

PUB main()
  process()
```

### Contradictory Conditions

```spin2
' WRONG: Conditions can never be true
#ifdef USE_MODE_A
#ifdef USE_MODE_B        ' If USE_MODE_A is true, this is confusing
  ' This code suggests both modes active simultaneously
#endif
#endif

' CORRECT: Make mutual exclusivity explicit
#ifdef USE_MODE_A
#undef USE_MODE_B        ' Explicitly clear the other mode
  ' Mode A code
#elseifdef USE_MODE_B
  ' Mode B code
#endif
```

### Overusing Preprocessor for Logic

```spin2
' WRONG: Using preprocessor where runtime logic is better
#ifdef SENSOR_TYPE_1
PUB read_sensor() : value
  value := sensor1_read()
#elseifdef SENSOR_TYPE_2
PUB read_sensor() : value
  value := sensor2_read()
#endif

' CORRECT: Use runtime polymorphism for flexibility
VAR
  long sensor_type

PUB init(type)
  sensor_type := type

PUB read_sensor() : value
  case sensor_type
    SENSOR_TYPE_1: value := sensor1_read()
    SENSOR_TYPE_2: value := sensor2_read()
```

### Missing Default Case

```spin2
' WRONG: No fallback if none match
#ifdef OPTION_A
  VALUE = 1
#elseifdef OPTION_B
  VALUE = 2
#endif
' VALUE undefined if neither defined!

' CORRECT: Always provide default or error
#ifdef OPTION_A
  VALUE = 1
#elseifdef OPTION_B
  VALUE = 2
#else
  VALUE = 0              ' Default value
  ' Or use: #error "Must define OPTION_A or OPTION_B"
#endif
```

### Including Code Multiple Times

```spin2
' WRONG: No include guard
' utils.spin2
PUB helper_func()
  ' ...

' main.spin2
#include "utils"
#include "other"         ' If other.spin2 also includes utils.spin2,
                          ' helper_func is defined twice

' CORRECT: Use include guards
' utils.spin2
#ifndef UTILS_INCLUDED
#define UTILS_INCLUDED

PUB helper_func()
  ' ...

#endif
```

## Preprocessor Output

When using the `-E` flag (if available) or examining preprocessed output, directives are converted to comments:

**Source:**
```spin2
#define DEBUG_MODE

#ifdef DEBUG_MODE
  DEBUG_FLAG = TRUE
#else
  DEBUG_FLAG = FALSE
#endif
```

**After preprocessing:**
```spin2
' #define DEBUG_MODE

' #ifdef DEBUG_MODE
  DEBUG_FLAG = TRUE
' #else
' #endif
```

The commented-out directives preserve line numbers for error reporting while showing which code paths were selected.

## Summary Tables

### Preprocessor Directives

| Directive | Purpose | Example |
|-----------|---------|---------|
| `#define` | Define symbol | `#define DEBUG_MODE` |
| `#define` | Define with value | `#define SIZE 100` |
| `#undef` | Remove symbol | `#undef DEBUG_MODE` |
| `#ifdef` | If defined | `#ifdef DEBUG_MODE` |
| `#ifndef` | If not defined | `#ifndef RELEASE` |
| `#else` | Else clause | `#else` |
| `#elseifdef` | Else if defined | `#elseifdef OTHER` |
| `#elseifndef` | Else if not defined | `#elseifndef OTHER` |
| `#endif` | End conditional | `#endif` |
| `#include` | Include file | `#include "utils"` |
| `#error` | Emit error | `#error "msg"` |
| `#warn` | Emit warning | `#warn "msg"` |
| `#pragma` | Compiler directive | `#pragma exportdef SYM` |

### Command-Line Options

| Option | Purpose | Example |
|--------|---------|---------|
| `-D` | Define symbol | `-D DEBUG_MODE` |
| `-U` | Undefine symbol | `-U DEBUG_MODE` |
| `-I` | Add include path | `-I ./includes` |

### Conditional Compilation Logic

| Source Directive | `-D SYMBOL` | Result |
|------------------|-------------|--------|
| `#ifdef SYMBOL` | Yes | Code included |
| `#ifdef SYMBOL` | No | Code excluded |
| `#ifndef SYMBOL` | Yes | Code excluded |
| `#ifndef SYMBOL` | No | Code included |

## Related Documentation

- [Control-Flow-Usage-Guide.md](Control-Flow-Usage-Guide.md) - Runtime conditionals (IF, CASE)
- [Spin2-Object-Patterns-Guide.md](Spin2-Object-Patterns-Guide.md) - Configurable object patterns
