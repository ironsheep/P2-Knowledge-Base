# DITTO Directive Usage Guide for Spin2/PASM2

This document describes the `DITTO` directive in the Spin2 and PASM2 languages for the Parallax Propeller 2 (P2) microcontroller as implemented in the PNut-TS compiler. This feature was introduced in PNut version 50.

## Overview

The `DITTO` directive provides a powerful code/data replication mechanism for DAT blocks. It allows you to repeat a block of instructions or data a specified number of times, with access to the current iteration index via the special `$$` symbol.

**Key Features:**
- Repeats a block of code/data N times at compile time
- The `$$` symbol provides the current iteration index (0 to N-1)
- Zero replication count produces no output (block is skipped)
- Works in both COG/LUT mode and ORGH (hub) mode

---

## Syntax

```spin2
DAT
        DITTO   count       ' Start DITTO block, repeat 'count' times
        ' ... code or data to repeat ...
        DITTO   END         ' End DITTO block
```

### Components

| Component | Description |
|-----------|-------------|
| `DITTO count` | Starts a DITTO block; `count` is the number of iterations (0 or more) |
| `$$` | Special symbol that evaluates to current iteration index (0 to count-1) |
| `DITTO END` | Marks the end of the DITTO block |

---

## Basic Examples

### Simple Data Replication

```spin2
DAT
        DITTO   4                   ' Repeat 4 times
        LONG    $77777777 + $$      ' Each long gets different value
        DITTO   END

' Produces:
'   LONG  $77777777   (when $$ = 0)
'   LONG  $77777778   (when $$ = 1)
'   LONG  $77777779   (when $$ = 2)
'   LONG  $7777777A   (when $$ = 3)
```

### Instruction Replication

```spin2
DAT
        ORG     0

        DITTO   8                   ' Repeat for 8 pins
        DRVH    #BasePin + $$       ' Drive high: pin BasePin+0, +1, +2, ... +7
        DITTO   END
```

Equivalent to writing:
```spin2
        DRVH    #BasePin + 0
        DRVH    #BasePin + 1
        DRVH    #BasePin + 2
        DRVH    #BasePin + 3
        DRVH    #BasePin + 4
        DRVH    #BasePin + 5
        DRVH    #BasePin + 6
        DRVH    #BasePin + 7
```

---

## The $$ Symbol

The `$$` symbol is a special compile-time constant that evaluates to the current DITTO iteration index.

### Properties

| Property | Value |
|----------|-------|
| First iteration | 0 |
| Last iteration | count - 1 |
| Outside DITTO block | Error: `"$$" (DITTO index) is only allowed within a DITTO block, inside a DAT block` |

### Using $$ in Expressions

`$$` can be used in any expression where a constant is valid:

```spin2
DAT
        DITTO   4
        LONG    $$ * 100            ' 0, 100, 200, 300
        DITTO   END

        DITTO   4
        LONG    1 << $$             ' 1, 2, 4, 8 (bit patterns)
        DITTO   END

CON
  BasePin = 16
  PinStep = 2

DAT
        DITTO   4
        DRVH    #BasePin + $$ * PinStep    ' Pins 16, 18, 20, 22
        DITTO   END
```

---

## Zero Count Behavior

When the DITTO count is 0, the block produces **no output** at all:

```spin2
DAT
        DITTO   0                   ' Count is zero
        LONG    $22222222 + $$      ' This line is never emitted
        DITTO   END
        ' No output generated - block is completely skipped
```

This is useful for conditional code generation with CON constants:

```spin2
CON
  MotorCount = 0                    ' No motors in this build

DAT
        DITTO   MotorCount          ' If MotorCount = 0, nothing generated
        ' ... motor initialization code ...
        DITTO   END
```

---

## Multi-Line DITTO Blocks

DITTO blocks can contain multiple lines of code or data:

```spin2
CON
  MotorCount = 4
  BasePin = 8

DAT
        ORG     0

        DITTO   MotorCount
        ' Each iteration generates 4 instructions
        WYPIN   speed + $$, #BasePin + $$ * 2 + 0     ' Set step pin speed
        RDPIN   position + $$, #BasePin + $$ * 2 + 1  ' Read direction totalizer
        TESTB   speed + $$, #31                   WC  ' Test direction bit
        DRVC    #BasePin + $$ * 2 + 1                 ' Update direction pin
        DITTO   END

speed       RES     MotorCount
position    RES     MotorCount
```

---

## Restrictions

### Not Allowed Within DITTO Blocks

The following directives cannot appear inside a DITTO block:

| Directive | Error Message |
|-----------|--------------|
| `ORG` | `ORG not allowed within a DITTO block` |
| `ORGH` | `ORGH not allowed within a DITTO block` |

```spin2
DAT
        DITTO   4
        ORG     0           ' ERROR: ORG not allowed within a DITTO block
        DITTO   END
```

### Block Must Be Properly Terminated

A DITTO block must end with `DITTO END`:

```spin2
DAT
        DITTO   4
        LONG    $$
        ' Missing DITTO END - will cause: Expected DITTO END
```

### Count Must Be Non-Negative

```spin2
DAT
        DITTO   -1          ' ERROR: DITTO count must be a positive integer or zero
        LONG    $$
        DITTO   END
```

### $$ Only Valid Inside DITTO

```spin2
DAT
        LONG    $$          ' ERROR: "$$" (DITTO index) is only allowed within a DITTO block
```

---

## Use Cases

### 1. Pin Initialization Tables

```spin2
CON
  NumChannels = 8
  BasePin = 0

DAT
        ORG     0

init_pins
        DITTO   NumChannels
        WRPIN   ##PinMode, #BasePin + $$
        WXPIN   ##PinX, #BasePin + $$
        DRVL    #BasePin + $$
        DITTO   END
        RET
```

### 2. Indexed Data Structures

```spin2
CON
  TableSize = 16

DAT
        ORGH

lookupTable
        DITTO   TableSize
        LONG    $$ * $$ * 10        ' Quadratic sequence: 0, 10, 40, 90, ...
        DITTO   END
```

### 3. Motor/Servo Control Arrays

From the PNut test file - real-world stepper motor driver:

```spin2
CON
  MotorCount = 4
  BasePin = 8

DAT
        ORG     0

' Update step/direction pins for each motor
        DITTO   MotorCount
        WYPIN   :MotorStats + sizeof(MotorStat)/4 * $$ + :ncov - :tail, #BasePin + $$ * 2 + 0
        RDPIN   :MotorStats + sizeof(MotorStat)/4 * $$ + :totl - :tail, #BasePin + $$ * 2 + 1
        TESTB   :MotorStats + sizeof(MotorStat)/4 * $$ + :ncov - :tail, #31    WC
        DRVC    #BasePin + $$ * 2 + 1
        DITTO   END
```

### 4. Lookup Table Generation

```spin2
CON
  SinTableSize = 256

DAT
        ORGH    $400

sinTable
        DITTO   SinTableSize
        ' Generate sine table: sin(2*PI*$$/256) scaled to 0-65535
        WORD    32768 + round(32767.0 * sin(float($$) * 2.0 * PI / 256.0))
        DITTO   END
```

### 5. Channel Configuration

```spin2
CON
  NumADC = 4
  ADCBase = $100

DAT
adcConfig
        DITTO   NumADC
        LONG    ADCBase + $$ * $10  ' ADC channel addresses
        DITTO   END

adcGain
        DITTO   NumADC
        LONG    $8000 + $$ * $100   ' Per-channel gain values
        DITTO   END
```

---

## Comparison with Manual Replication

### Without DITTO

```spin2
DAT
        ' Manual replication - error-prone and verbose
        DRVH    #16
        DRVH    #17
        DRVH    #18
        DRVH    #19
        DRVH    #20
        DRVH    #21
        DRVH    #22
        DRVH    #23
```

### With DITTO

```spin2
DAT
        ' Clean, maintainable, parameterized
        DITTO   8
        DRVH    #16 + $$
        DITTO   END
```

### Benefits of DITTO

1. **Maintainability** - Change count in one place
2. **Readability** - Intent is clear
3. **Parameterization** - Use constants for count
4. **Flexibility** - Expressions with `$$` enable complex patterns
5. **Zero-cost** - Replication happens at compile time

---

## Error Messages

| Error | Cause |
|-------|-------|
| `DITTO count must be a positive integer or zero` | Negative count value |
| `Expected END` | `DITTO END` not properly formatted |
| `Expected DITTO END` | Block not terminated or nested incorrectly |
| `ORG not allowed within a DITTO block` | ORG directive inside DITTO |
| `ORGH not allowed within a DITTO block` | ORGH directive inside DITTO |
| `"$$" (DITTO index) is only allowed within a DITTO block, inside a DAT block` | Using `$$` outside DITTO |

---

## Version Information

- **Introduced:** PNut v50
- **Compiler Support:** PNut-TS fully supports DITTO as of the v50-compatible release

---

## Summary

| Aspect | Details |
|--------|---------|
| Location | DAT blocks only |
| Syntax | `DITTO count` ... `DITTO END` |
| Index access | `$$` (0 to count-1) |
| Count range | 0 to any positive integer |
| Zero count | Block is skipped entirely |
| Restrictions | No ORG/ORGH inside block |
| Mode support | COG, LUT, and ORGH modes |

---

## Best Practices

1. **Use constants for counts** - Makes code configurable
   ```spin2
   CON
     ChannelCount = 8
   DAT
     DITTO   ChannelCount
   ```

2. **Comment the purpose** - Explain what the DITTO block generates
   ```spin2
   DITTO   8                       ' Initialize 8 PWM channels
   ```

3. **Keep blocks focused** - One logical operation per DITTO block

4. **Verify with listing** - Use `-l` option to review generated code

5. **Consider zero case** - Ensure your code handles `count = 0` correctly

---

*This document describes DITTO directive usage in Spin2/PASM2 as implemented in the PNut-TS compiler.*
