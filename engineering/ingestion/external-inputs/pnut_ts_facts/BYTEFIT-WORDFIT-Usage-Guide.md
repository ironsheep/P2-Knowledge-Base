# BYTEFIT and WORDFIT Usage Guide for Spin2/PASM2

This document describes the `BYTEFIT` and `WORDFIT` directives in the Spin2 and PASM2 languages for the Parallax Propeller 2 (P2) microcontroller as implemented in the PNut-TS compiler.

## Overview

`BYTEFIT` and `WORDFIT` are data declaration directives used in DAT blocks that work similarly to `BYTE` and `WORD`, but with **compile-time range validation**. They ensure that the values you declare actually fit within the specified size, catching potential overflow errors during compilation rather than at runtime.

| Directive | Storage Size | Valid Range (Unsigned) | Valid Range (Signed) |
|-----------|-------------|------------------------|----------------------|
| `BYTEFIT` | 8 bits (1 byte) | 0 to $FF (255) | -$80 to $7F (-128 to 127) |
| `WORDFIT` | 16 bits (2 bytes) | 0 to $FFFF (65535) | -$8000 to $7FFF (-32768 to 32767) |

---

## Syntax

```spin2
DAT
  [label]  BYTEFIT  value1 [, value2, ...]
  [label]  WORDFIT  value1 [, value2, ...]
```

### Key Points

- **No parentheses required** - These are data declaration directives, not function calls
- Work identically to `BYTE` and `WORD` in terms of storage
- Add compile-time validation to ensure values fit within size constraints
- Can only be used in DAT blocks

---

## Basic Examples

### BYTEFIT

```spin2
DAT
  ' Valid BYTEFIT values
  byteData    BYTEFIT   -$80              ' Minimum signed value: -128
              BYTEFIT   $FF               ' Maximum unsigned value: 255
              BYTEFIT   0, 100, 200, 255  ' Multiple values
              BYTEFIT   -128, -1, 0, 127  ' Signed values

  ' The following would cause compile errors:
  ' BYTEFIT   256                         ' Too large for byte
  ' BYTEFIT   -129                        ' Too negative for signed byte
  ' BYTEFIT   $100                        ' Exceeds $FF
```

### WORDFIT

```spin2
DAT
  ' Valid WORDFIT values
  wordData    WORDFIT   -$8000            ' Minimum signed value: -32768
              WORDFIT   $FFFF             ' Maximum unsigned value: 65535
              WORDFIT   1000, 30000       ' Multiple values
              WORDFIT   -32768, 0, 32767  ' Signed values

  ' The following would cause compile errors:
  ' WORDFIT   65536                       ' Too large for word
  ' WORDFIT   -32769                      ' Too negative for signed word
  ' WORDFIT   $10000                      ' Exceeds $FFFF
```

---

## Value Range Details

### BYTEFIT Range

| Representation | Minimum | Maximum |
|----------------|---------|---------|
| Hexadecimal | -$80 | $FF |
| Decimal (signed) | -128 | 127 |
| Decimal (unsigned) | 0 | 255 |
| Binary | %0000_0000 | %1111_1111 |

The combined range allows both:
- Signed byte values: -128 to +127
- Unsigned byte values: 0 to 255

This gives an effective range of **-$80 to $FF** (-128 to 255).

### WORDFIT Range

| Representation | Minimum | Maximum |
|----------------|---------|---------|
| Hexadecimal | -$8000 | $FFFF |
| Decimal (signed) | -32768 | 32767 |
| Decimal (unsigned) | 0 | 65535 |
| Binary | %0000_0000_0000_0000 | %1111_1111_1111_1111 |

The combined range allows both:
- Signed word values: -32768 to +32767
- Unsigned word values: 0 to 65535

This gives an effective range of **-$8000 to $FFFF** (-32768 to 65535).

---

## Advanced Syntax

### Multiple Values

```spin2
DAT
  ' Multiple values on one line
  byteTable   BYTEFIT   0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250

  ' Continued on next line (no label needed)
              BYTEFIT   10, 20, 30, 40, 50

  wordTable   WORDFIT   1000, 2000, 3000, 4000, 5000
```

### Multipliers (Repetition)

Use `[count]` to repeat a value multiple times:

```spin2
DAT
  ' Fill 100 bytes with value 0, with range checking
  zeros       BYTEFIT   0[100]

  ' Fill 50 words with value $ABCD, with range checking
  pattern     WORDFIT   $ABCD[50]

  ' Multiple values with different repeat counts
  mixed       BYTEFIT   0[10], 255[5], 128[3]
```

### Size Overrides

You can use inline size overrides just like with BYTE/WORD/LONG:

```spin2
DAT
  ' Start with BYTEFIT, but include some word-sized data
  data        BYTEFIT   10, 20, 30
              WORD      $1234            ' Override to word size
              BYTEFIT   40, 50           ' Back to BYTEFIT
```

### Expressions

BYTEFIT and WORDFIT accept constant expressions:

```spin2
CON
  BASE_VALUE = 100
  MULTIPLIER = 2

DAT
  ' Expressions are evaluated at compile time
  computed    BYTEFIT   BASE_VALUE * MULTIPLIER    ' 200, fits in byte
              BYTEFIT   BASE_VALUE + 50            ' 150, fits in byte

  ' Would fail if expression exceeds range:
  ' BYTEFIT   BASE_VALUE * 3                       ' 300, too large!
```

---

## Comparison with BYTE and WORD

### BYTE vs BYTEFIT

| Feature | BYTE | BYTEFIT |
|---------|------|---------|
| Storage size | 8 bits | 8 bits |
| Range checking | No | Yes |
| Truncation | Silent | Compile error |
| Expression handling | Stores low 8 bits | Validates full value |

```spin2
DAT
  ' BYTE silently truncates
  truncated   BYTE      $1234            ' Stores $34 (low byte only)

  ' BYTEFIT prevents truncation
  ' checked   BYTEFIT   $1234            ' ERROR: value too large!
```

### WORD vs WORDFIT

| Feature | WORD | WORDFIT |
|---------|------|---------|
| Storage size | 16 bits | 16 bits |
| Range checking | No | Yes |
| Truncation | Silent | Compile error |
| Expression handling | Stores low 16 bits | Validates full value |

```spin2
DAT
  ' WORD silently truncates
  truncated   WORD      $12345678        ' Stores $5678 (low word only)

  ' WORDFIT prevents truncation
  ' checked   WORDFIT   $12345678        ' ERROR: value too large!
```

---

## Common Use Cases

### 1. Lookup Tables with Validation

```spin2
DAT
' Ensure all values in a gamma correction table fit in a byte
gammaTable  BYTEFIT   0, 1, 2, 3, 4, 5, 7, 9, 12, 15, 18, 22, 27, 32, 38, 44
            BYTEFIT   51, 58, 67, 76, 86, 96, 108, 120, 134, 148, 163, 180
            BYTEFIT   197, 216, 235, 255

' ADC calibration values - must fit in 16 bits
adcOffsets  WORDFIT   -1024, -512, 0, 512, 1024
adcGains    WORDFIT   32768, 33000, 32500, 32768
```

### 2. Protocol Data Structures

```spin2
DAT
' Packet header - command IDs must be valid byte values
cmdTable    BYTEFIT   $01              ' CMD_START
            BYTEFIT   $02              ' CMD_STOP
            BYTEFIT   $03              ' CMD_RESET
            BYTEFIT   $FF              ' CMD_INVALID (max byte value)

' Status codes - fit in word
statusCodes WORDFIT   $0000            ' STATUS_OK
            WORDFIT   $0001            ' STATUS_BUSY
            WORDFIT   $FFFF            ' STATUS_ERROR
```

### 3. Configuration Data with Safety

```spin2
CON
  ' These constants must be safe for byte storage
  PWM_MIN    = 0
  PWM_MAX    = 255
  PWM_CENTER = 128

DAT
' Using BYTEFIT ensures these values are actually valid bytes
pwmDefaults BYTEFIT   PWM_MIN, PWM_CENTER, PWM_MAX

' If someone changes PWM_MAX to 300, compilation will fail
' rather than silently storing 44 (300 & $FF)
```

### 4. Sensor Calibration Data

```spin2
CON
  TEMP_OFFSET = -40    ' Temperature sensor offset (-40 to +215 range)

DAT
' Temperature thresholds in sensor units (must fit in byte with offset)
tempLow     BYTEFIT   TEMP_OFFSET + 0    ' -40 degrees
tempHigh    BYTEFIT   TEMP_OFFSET + 125  ' +85 degrees (85 fits in byte)

' ADC reference voltages in millivolts (0-65535 range)
vrefTable   WORDFIT   0, 1000, 2048, 3300, 5000
```

### 5. Calculated Jump Tables

```spin2
CON
  FUNC_COUNT = 8
  ENTRY_SIZE = 4

DAT
' Offsets must fit in bytes (validating they're < 256)
funcOffsets BYTEFIT   0 * ENTRY_SIZE
            BYTEFIT   1 * ENTRY_SIZE
            BYTEFIT   2 * ENTRY_SIZE
            BYTEFIT   3 * ENTRY_SIZE
            BYTEFIT   4 * ENTRY_SIZE
            BYTEFIT   5 * ENTRY_SIZE
            BYTEFIT   6 * ENTRY_SIZE
            BYTEFIT   7 * ENTRY_SIZE
' If ENTRY_SIZE were 64, the last entries would fail (7*64=448 > 255)
```

---

## Error Messages

When values exceed the allowed range, the compiler produces these errors:

| Directive | Error Message |
|-----------|--------------|
| `BYTEFIT` | `BYTEFIT values must range from -$80 to $FF` |
| `WORDFIT` | `WORDFIT values must range from -$8000 to $FFFF` |

### Examples of Errors

```spin2
DAT
  ' These all produce compile-time errors:

  ' Error: BYTEFIT values must range from -$80 to $FF
  bad1      BYTEFIT   256                ' 256 > 255
  bad2      BYTEFIT   -129               ' -129 < -128
  bad3      BYTEFIT   $100               ' $100 > $FF

  ' Error: WORDFIT values must range from -$8000 to $FFFF
  bad4      WORDFIT   65536              ' 65536 > 65535
  bad5      WORDFIT   -32769             ' -32769 < -32768
  bad6      WORDFIT   $10000             ' $10000 > $FFFF
```

---

## When to Use BYTEFIT/WORDFIT

### Use When:

1. **Data integrity is critical** - Sensor calibration, protocol headers
2. **Constants might change** - Values derived from CON block constants
3. **Calculations are involved** - Computed offsets or scaling factors
4. **Documentation is important** - Makes intent clear that values must fit
5. **Debugging data issues** - Catch truncation bugs at compile time

### Use Regular BYTE/WORD When:

1. **Truncation is intentional** - Extracting low bytes/words from larger values
2. **Legacy code compatibility** - Matching existing data layouts
3. **Performance critical paths** - Though the difference is only at compile time

---

## Summary

| Aspect | BYTEFIT | WORDFIT |
|--------|---------|---------|
| Location | DAT block only | DAT block only |
| Storage | 8 bits (1 byte) | 16 bits (2 bytes) |
| Min value | -$80 (-128) | -$8000 (-32768) |
| Max value | $FF (255) | $FFFF (65535) |
| Syntax | `BYTEFIT value [, ...]` | `WORDFIT value [, ...]` |
| Multiplier | `BYTEFIT value[count]` | `WORDFIT value[count]` |
| Parentheses | Not required | Not required |
| Validation | At compile time | At compile time |

---

## Best Practices

1. **Prefer BYTEFIT/WORDFIT for critical data** - Catch errors early.

2. **Use for derived values** - When values come from calculations or constants.
   ```spin2
   CON
     SCALE = 10
   DAT
     scaled  BYTEFIT  BASE * SCALE   ' Validates result fits
   ```

3. **Document your constraints** - BYTEFIT/WORDFIT serve as documentation.
   ```spin2
   DAT
   ' Command codes must be single bytes
   commands    BYTEFIT  CMD_READ, CMD_WRITE, CMD_RESET
   ```

4. **Use for lookup tables** - Ensure all table entries fit the expected size.

5. **Consider future changes** - If constants might be modified, use FIT variants.

---

*This document describes BYTEFIT and WORDFIT usage in Spin2/PASM2 as implemented in the PNut-TS compiler.*
