# Inline PASM Usage Guide for Spin2/PASM2

This document describes how to use inline PASM (Propeller Assembly) code within PUB and PRI methods in the Spin2 language for the Parallax Propeller 2 (P2) microcontroller as implemented in the PNut-TS compiler.

## Overview

Inline PASM allows you to embed assembly code directly within Spin2 methods. This provides:

- **Maximum Speed**: PASM code executes much faster than Spin2 bytecode
- **Hardware Access**: Direct register and pin manipulation
- **Precise Timing**: Cycle-accurate control when needed
- **Local Integration**: Seamless access to method's local variables

| Block Type | Start | End | Execution Location |
|------------|-------|-----|--------------------|
| COG Inline | `ORG` | `END` | COG RAM (fastest) |
| Hub Inline | `ORGH` | `END` | Hub RAM (fast) |

---

## Basic Syntax

### COG Mode Inline (ORG...END)

```spin2
PUB Method() | local1, local2
  ' Spin2 code before inline

  ORG                           ' Begin inline PASM (COG execution)
                instruction1
                instruction2
  END                           ' End inline PASM

  ' Spin2 code after inline
```

### Hub Mode Inline (ORGH...END)

```spin2
PUB Method()
  ' Spin2 code before inline

  ORGH                          ' Begin inline PASM (Hub execution)
                instruction1
                instruction2
  END                           ' End inline PASM

  ' Spin2 code after inline
```

---

## ORG vs ORGH for Inline

| Aspect | ORG (COG Mode) | ORGH (Hub Mode) |
|--------|----------------|-----------------|
| Execution location | COG RAM | Hub RAM |
| Speed | Fastest | Fast |
| Address space limit | $120 (288 longs) | $1F8 (504 longs) |
| Code size | Limited | Larger |
| Use case | Timing-critical | Larger routines |

### ORG with Optional Parameters

```spin2
PUB Method()
  ORG                           ' Start at address 0, default limit $120
  ' ... code ...
  END

  ORG 0, $100                   ' Start at 0, custom limit $100
  ' ... code ...
  END
```

---

## Local Variable Access

Inline PASM can access local variables from the enclosing method, but with restrictions:

### Requirements for Local Variable Access

1. **Must be LONG type** - BYTE and WORD locals cannot be accessed directly
2. **Within first 16 longs** - Only the first 16 LONG variables are accessible
3. **Automatic mapping** - Variables are mapped to COG addresses starting at $1E0

```spin2
PUB Write(i2cbyte) : ackbit | scl, sda, tix, bits
  ' All locals are LONGs and within first 16 - accessible from inline!

  longmove(@scl, @sclpin, 3)    ' Initialize locals before inline

  ORG
                shl       i2cbyte, #24          ' Access method parameter
                mov       bits, #8              ' Access local variable
.loop           shl       i2cbyte, #1       wc  ' Shift and set carry
                drvc      sda                   ' Use local as pin number
                waitx     tix                   ' Use local as timing value
                djnz      bits, #.loop          ' Loop using local counter
  END

  ' ackbit return value is available after END
```

### Local Variable Mapping

Local LONG variables are mapped to COG registers:

| Local Position | COG Address |
|----------------|-------------|
| 1st LONG | $1E0 |
| 2nd LONG | $1E1 |
| 3rd LONG | $1E2 |
| ... | ... |
| 16th LONG | $1EF |

### Invalid Local Variable Access

```spin2
PUB BadExample() | byte myByte, word myWord, longVar

  ORG
                mov     longVar, #0           ' OK - LONG variable
                mov     myByte, #0            ' ERROR: Local variable must be LONG
                mov     myWord, #0            ' ERROR: Local variable must be LONG
  END
```

---

## Labels in Inline PASM

### Local Labels (Supported)

Local labels starting with `.` are fully supported and commonly used:

```spin2
PUB I2CWrite(i2cbyte) : ackbit | scl, sda, tix, bits

  ORG
                shl       i2cbyte, #24

.wr_byte        mov       bits, #8              ' Local label
.wb0            shl       i2cbyte, #1       wc  ' Another local label
                drvc      sda
                waitx     tix
                drvh      scl
                waitx     tix
                waitx     tix
                drvl      scl
                waitx     tix
                djnz      bits, #.wb0           ' Branch to local label

.get_ack        drvh      sda                   ' Another local label
                waitx     tix
                drvh      scl
                waitx     tix
                testp     sda                wc
                muxc      ackbit, #1
                waitx     tix
                drvl      scl
  END
```

### Global Labels (Not Recommended)

Global labels (without `.` prefix) in inline code are added to a separate inline symbol table and reset after the inline block ends. While syntactically allowed, local labels are preferred for clarity.

### Label References

Use `#` prefix to reference labels as immediate values:

```spin2
  ORG
.loop           nop
                djnz      count, #.loop         ' Branch to label
                jmp       #.done                ' Jump to label
.done           nop
  END
```

---

## Allowed Features

### All PASM Instructions

All standard PASM2 instructions work in inline mode:

```spin2
PUB Example() | pin, value, count

  ORG
                ' I/O instructions
                drvh      pin                   ' Drive pin high
                drvl      pin                   ' Drive pin low
                drvc      pin                   ' Drive pin to C flag
                drvnot    pin                   ' Toggle pin
                testp     pin               wc  ' Test pin state

                ' ALU instructions
                mov       value, #100
                add       value, #1
                sub       value, #1
                shl       value, #8
                shr       value, #8

                ' Control flow
                djnz      count, #.loop         ' Decrement and jump if not zero
                jmp       #.done                ' Unconditional jump
                ret                             ' Return (implicit at END)

                ' Timing
                waitx     #100                  ' Wait for clock cycles

                ' Memory access
                rdlong    value, ##hubAddr      ' Read from hub
                wrlong    value, ##hubAddr      ' Write to hub
  END
```

### Conditional Execution

All condition codes work:

```spin2
  ORG
                testp     pin               wc  ' Set C flag
    if_c        jmp       #.high                ' Jump if pin high
    if_nc       jmp       #.low                 ' Jump if pin low

                cmp       value, #10        wz  ' Set Z flag
    if_z        mov       result, #1            ' If equal
    if_nz       mov       result, #0            ' If not equal

    if_c_and_z  nop                             ' If C and Z
    if_c_or_z   nop                             ' If C or Z
  END
```

### REP Instruction

The REP (repeat) instruction works in inline:

```spin2
  ORG
                rep       #8, #9                ' Repeat next 8 instructions, 9 times
                 testp    sda               wc
    if_c         jmp      #.done
                 drvl     scl
                 waitx    tix
                 waitx    tix
                 drvh     scl
                 waitx    tix
                 waitx    tix
.done
  END
```

### Current Address ($)

The `$` symbol represents the current COG address:

```spin2
  ORG
                jmp       #$                    ' Infinite loop (jump to self)
                testp     pin               wc
    if_nc       jmp       #$-2                  ' Jump back 2 instructions
  END
```

### Flag Effects (WC, WZ, WCZ)

All flag modifiers work:

```spin2
  ORG
                testp     pin               wc  ' Set C to pin state
                add       value, #1         wz  ' Set Z if result is zero
                shl       value, #1        wcz  ' Set both C and Z
  END
```

### Data Declarations

BYTE, WORD, LONG data can be included:

```spin2
PUB Example()
  ORG 0, 3
                byte      1, 2, 3, 4            ' Inline data
  END
```

---

## Restrictions

### Directives NOT Allowed Inside Inline

| Directive | Error Message |
|-----------|---------------|
| `ORG` | `ORG not allowed within inline assembly code` |
| `ORGH` | `ORGH not allowed within inline assembly code` |
| `ALIGNW` | `ALIGNW/ALIGNL not allowed within inline assembly code` |
| `ALIGNL` | `ALIGNW/ALIGNL not allowed within inline assembly code` |

```spin2
PUB BadExample()
  ORG
                nop
                ORG     $100              ' ERROR: ORG not allowed
                ALIGNL                    ' ERROR: ALIGNW/ALIGNL not allowed
  END
```

### Address Limits

| Mode | Maximum Address |
|------|-----------------|
| ORG (COG) | $120 (288 longs) |
| ORGH (Hub) | $1F8 (504 longs) |

Exceeding these limits produces:
- `Inline cog address exceeds $120 limit`
- `ORGH inline block exceeds $FFFF longs`

### Empty Blocks Not Allowed

```spin2
PUB BadExample()
  ORG
  END                                     ' ERROR: ORG/ORGH inline block is empty
```

### Local Variable Constraints

- Only LONG variables accessible
- Maximum 16 LONGs
- Error: `Local variable must be LONG and within first 16 longs`

---

## How Inline PASM Works

When the Spin2 interpreter encounters inline PASM:

1. **Load Locals**: First 16 local LONG variables are loaded from hub into COG buffer at $1E0
2. **Execute Code**: PASM code executes from COG or Hub RAM
3. **Implicit RET**: The `END` directive inserts an implicit `RET` instruction
4. **Restore Locals**: Local variables are written back to hub memory
5. **Resume Spin2**: Execution continues with Spin2 bytecode after END

---

## Complete Examples

### I2C Start Sequence

```spin2
PUB start() | scl, sda, tix

  longmove(@scl, @sclpin, 3)              ' Copy pins & timing to locals

  ORG
                drvh      sda              ' SDA high
                drvh      scl              ' SCL high
                waitx     tix              ' Delay

                drvl      sda              ' SDA low (start condition)
                waitx     tix              ' Delay
                drvl      scl              ' SCL low
                waitx     tix              ' Delay
  END
```

### Pin Toggle with Count

```spin2
PUB togglePin(pin, count)

  ORG
.loop           drvnot    pin              ' Toggle pin
                waitx     #1000            ' Small delay
                djnz      count, #.loop    ' Repeat count times
  END
```

### Reading from Hub Memory

```spin2
PUB readBlock(p_buffer, count) | value

  ORG
.loop           rdbyte    value, p_buffer  ' Read byte from hub
                add       p_buffer, #1     ' Increment pointer
                ' ... process value ...
                djnz      count, #.loop    ' Loop for all bytes
  END
```

### SPI Byte Transfer

```spin2
PRI flash_send(p_buffer, count) | tx_byte, bits

  ORG
.byte           rdbyte    tx_byte, p_buffer
                add       p_buffer, #1
                shl       tx_byte, #24+1  wc  ' MSB-justify, get D7 into C

                rep       @.done, #8          ' Repeat 8 times
                drvc      #SF_MOSI            ' Output data bit
                drvnot    #SF_SCLK            ' Toggle clock
                waitx     #2                  ' Delay
                drvnot    #SF_SCLK            ' Toggle clock
                shl       tx_byte, #1     wc  ' Next bit
.done
                djnz      count, #.byte       ' Loop for all bytes

                drvl      #SF_MOSI            ' MOSI low when done
  END
```

### Clock Stretch Handling

```spin2
PUB write(i2cbyte) : ackbit | scl, sda, tix, bits

  ORG
                shl       i2cbyte, #24

.wr_byte        mov       bits, #8
.wb0            shl       i2cbyte, #1     wc
                drvc      sda
                waitx     tix
                drvh      scl
                testp     scl             wc  ' Check for clock stretch
    if_nc       jmp       #$-2                ' Wait if clock held low
                waitx     tix
                waitx     tix
                drvl      scl
                waitx     tix
                djnz      bits, #.wb0

.get_ack        drvh      sda
                waitx     tix
                drvh      scl
                testp     scl             wc  ' Check for clock stretch
    if_nc       jmp       #$-2
                waitx     tix
                testp     sda             wc  ' Sample ack bit
                muxc      ackbit, #1
                waitx     tix
                drvl      scl
                waitx     tix
  END
```

---

## Summary

### Quick Reference

```spin2
PUB Method() | local1, local2, local3

  ' Copy data to locals before inline if needed
  longmove(@local1, @sourceData, 3)

  ORG                           ' Begin COG-mode inline
                mov     local1, #100    ' Access local variable
.loop           drvnot  #pin            ' Toggle pin
                djnz    local1, #.loop  ' Branch to local label
  END                           ' End inline (implicit RET)

  ' Or use ORGH for larger code:
  ORGH
                ' Hub-mode inline code
  END
```

### Feature Summary

| Feature | Supported | Notes |
|---------|-----------|-------|
| Local labels (`.name`) | Yes | Recommended |
| Global labels | Yes | Reset after block |
| LONG local variables | Yes | First 16 only |
| BYTE/WORD locals | No | Error |
| All PASM instructions | Yes | |
| Conditional execution | Yes | All conditions |
| REP instruction | Yes | |
| Data declarations | Yes | BYTE/WORD/LONG |
| `$` current address | Yes | |
| ORG inside inline | No | Error |
| ORGH inside inline | No | Error |
| ALIGNW/ALIGNL | No | Error |

---

## Best Practices

1. **Keep inline blocks short** - For complex PASM, use DAT blocks and COGINIT
   ```spin2
   ' Good: Simple, focused inline
   ORG
           drvnot  pin
   END

   ' Better for complex code: Use DAT block
   COGINIT(NEWCOG, @complex_routine, 0)
   ```

2. **Copy data to locals first** - Use `longmove()` to prepare local variables
   ```spin2
   longmove(@scl, @sclpin, 3)  ' Copy instance vars to locals
   ORG
           waitx   tix         ' Now accessible in inline
   END
   ```

3. **Use local labels** - Prefix with `.` for clarity
   ```spin2
   ORG
   .loop   nop
           djnz    count, #.loop
   END
   ```

4. **Declare enough LONGs** - Ensure locals are LONG and within limit
   ```spin2
   PUB Method() | a, b, c, d    ' All are LONGs, all accessible
   ```

5. **Document timing** - Comment cycle-critical code
   ```spin2
   ORG
           waitx   tix         ' 1/4 bit period
           drvh    scl         ' Clock high
           waitx   tix         ' Hold time
   END
   ```

---

*This document describes inline PASM usage in Spin2 methods as implemented in the PNut-TS compiler.*
