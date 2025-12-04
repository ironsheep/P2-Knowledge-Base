# Predefined Constants

PASM2 provides a set of predefined constants that the assembler substitutes at compile time. These constants do not generate code themselves but provide standardized values for common operations including boolean logic, numeric bounds, mathematical calculations, and execution mode control.

## Boolean Constants

::: constheader
### TRUE {#true}
Logical True Constant
Category: [Boolean Constants](instruction-categories.md#boolean-constants)
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
```pasm
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
Category: [Boolean Constants](instruction-categories.md#boolean-constants)
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
```pasm
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
Category: [Numeric Limit Constants](instruction-categories.md#numeric-limit-constants)
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
```pasm
' Checking for negative underflow
                cmps    value, NEGX     wc      ' Check if below min negative
        if_c    jmp     #underflow              ' Jump if underflow

' Using NEGX as lower limit
                mov     limit, NEGX             ' Set limit to max negative
                maxs    value, limit            ' Clamp to not go below NEGX
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
Category: [Numeric Limit Constants](instruction-categories.md#numeric-limit-constants)
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
```pasm
' Checking for positive overflow
                cmp     value, POSX     wc      ' Check if exceeds max positive
        if_nc   jmp     #overflow               ' Jump if overflow

' Using POSX as upper limit
                mov     limit, POSX             ' Set limit to max positive
                mins    value, limit            ' Clamp to not exceed POSX
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
Category: [Mathematical Constants](instruction-categories.md#mathematical-constants)
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
```pasm
' Using PI with CORDIC rotation
        mov     angle, PI           ' Load PI constant
        shr     angle, #1           ' Divide by 2 for PI/2 (90 degrees)
        qrotate angle, radius       ' Rotate by PI/2 radians

' Converting radians to degrees using PI
        mov     x, PI               ' Start with PI
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
Category: [Execution Mode Constants](instruction-categories.md#execution-mode-constants)
:::

Execution mode constant for loading code from hub RAM to cog RAM.

#### Value
| Representation | Value |
|----------------|-------|
| Binary | %0_0_0000 |
| Hexadecimal | $00 |

#### Description
COGEXEC specifies cog execution mode for the COGINIT instruction. When used, COGINIT loads 496 longs from hub RAM into cog RAM registers $000-$1F7 and begins execution at cog address $000. This mode provides maximum execution speed since all instructions execute from fast cog RAM.

#### Usage
```pasm
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
- Loads cog RAM registers $000-$1F7 (496 longs) from hub RAM
- Begins execution at cog register address $000
- Must specify target cog ID (0-7)
- Fastest execution mode due to cog RAM access speeds
- Code size limited to 496 longs (2KB minus register space)

#### Related Constants
- [HUBEXEC](#hubexec) — Hub execution mode constant
- [COGEXEC_NEW](#cogexec_new) — Auto-select available cog variant
- [COGEXEC_NEW_PAIR](#cogexec_new_pair) — Auto-select adjacent cog pair variant



::: constheader
### HUBEXEC {#hubexec}
Hub Execution Mode
Category: [Execution Mode Constants](instruction-categories.md#execution-mode-constants)
:::

Execution mode constant for executing code directly from hub RAM.

#### Value
| Representation | Value |
|----------------|-------|
| Binary | %0_1_0000 |
| Hexadecimal | $10 |

#### Description
HUBEXEC specifies hub execution mode for the COGINIT instruction. When used, COGINIT starts the target cog executing instructions directly from hub RAM without loading code to cog RAM. This mode removes code size restrictions at the cost of slower instruction fetch times.

#### Usage
```pasm
' Start specific cog with hub execution
        COGINIT #HUBEXEC+1, #$400   ' Cog 1 from Hub RAM $400

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
- Hub execution allows unlimited code size (not limited to 496 longs)
- Slower than cog execution due to hub RAM access timing and FIFO overhead
- Instruction fetching occurs through FIFO/streamer mechanism
- Must specify target cog ID (0-7)
- Each cog maintains its own program counter for hub execution

#### Related Constants
- [COGEXEC](#cogexec) — Cog execution mode constant
- [HUBEXEC_NEW](#hubexec_new) — Auto-select available cog variant
- [HUBEXEC_NEW_PAIR](#hubexec_new_pair) — Auto-select adjacent cog pair variant



## Execution Mode Variants

The execution mode constants include additional variants for automatic cog selection:

::: constheader
### COGEXEC_NEW {#cogexec_new}
Auto-Select Cog For Cog Execution
Category: [Execution Mode Constants](instruction-categories.md#execution-mode-constants)
:::

Automatically selects the next available cog for COGEXEC mode. Eliminates the need to manually specify cog ID when any available cog will suffice.

::: constheader
### COGEXEC_NEW_PAIR {#cogexec_new_pair}
Auto-Select Cog Pair For Cog Execution
Category: [Execution Mode Constants](instruction-categories.md#execution-mode-constants)
:::

Automatically selects an adjacent pair of available cogs for COGEXEC mode. Used when paired cog operations require two adjacent cogs.

::: constheader
### HUBEXEC_NEW {#hubexec_new}
Auto-Select Cog For Hub Execution
Category: [Execution Mode Constants](instruction-categories.md#execution-mode-constants)
:::

Automatically selects the next available cog for HUBEXEC mode. Eliminates the need to manually specify cog ID when any available cog will suffice.

::: constheader
### HUBEXEC_NEW_PAIR {#hubexec_new_pair}
Auto-Select Cog Pair For Hub Execution
Category: [Execution Mode Constants](instruction-categories.md#execution-mode-constants)
:::

Automatically selects an adjacent pair of available cogs for HUBEXEC mode. Used when paired cog operations require two adjacent cogs.

These variants simplify cog management by allowing the system to automatically assign available cogs rather than requiring explicit cog ID specification.



## Hardware Configuration Constants

The P2 provides extensive predefined constants for configuring its sophisticated hardware subsystems. These constants are documented in dedicated reference sections:

### SmartPin Constants

The P2's 64 Smart Pins each function as independent hardware peripherals. Over 50 predefined constants configure input selection, filtering, output control, and the 32 operating modes including DAC, ADC, PWM, serial communication, and counters.

**See:** [SmartPin Configuration Constants](smartpin-constants.md)

### Streamer Constants

The Streamer is the P2's DMA-like engine for high-bandwidth data transfer between hub RAM, LUT, pins, and DAC outputs. Over 80 predefined constants configure data sources, destinations, formats, color modes, and control flags.

**See:** [Streamer Configuration Constants](streamer-constants.md)



## Constants Summary

| Category | Count | Purpose |
|----------|-------|---------|
| Boolean | 2 | TRUE, FALSE for logical operations |
| Numeric Limits | 2 | NEGX, POSX for bounds checking |
| Mathematical | 1 | PI for CORDIC and floating-point |
| Execution Mode | 6 | COGEXEC, HUBEXEC and variants |
| SmartPin | 59 | Pin configuration and modes |
| Streamer | 85 | Data streaming and video |
| **Total** | **155** | Core predefined constants |

*Note: Clock configuration constants (RCFAST, RCSLOW, XI, PLL, XDIV*, XMUL*, etc.) add over 1,000 additional symbols for system clock setup.*
