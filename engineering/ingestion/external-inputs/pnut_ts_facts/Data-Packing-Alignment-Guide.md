# Data Packing and Alignment Guide for Spin2/PASM2

This document describes how data is packed and aligned in memory when declaring variables in VAR blocks, DAT blocks, and local variables in PUB/PRI methods for the Parallax Propeller 2 (P2) microcontroller as implemented in the PNut-TS compiler.

## Overview

**Key Finding: There is NO automatic alignment based on data size in Spin2/PASM2.**

Unlike many other languages (C, C++, Rust, etc.) where variables are automatically aligned to their natural boundaries, Spin2/PASM2 packs data **sequentially without gaps** unless you explicitly request alignment using the `ALIGNW` or `ALIGNL` directives.

| Declaration Context | Auto-Alignment | Manual Alignment Available |
|---------------------|----------------|---------------------------|
| VAR block | **No** | Yes (ALIGNW, ALIGNL) |
| DAT block (data) | **No** | Yes (ALIGNW, ALIGNL) |
| DAT block (instructions) | **Yes** (COG mode only) | Yes (ALIGNW, ALIGNL) |
| Local variables | **No** | Yes (ALIGNW, ALIGNL) |

---

## Sequential Packing Behavior

### VAR Block Packing

Variables in VAR blocks are packed sequentially at byte boundaries:

```spin2
VAR
  BYTE  v1        ' Offset 0x04 (starts at 4, after object pointer)
  BYTE  v2        ' Offset 0x05 (immediately after v1)
  WORD  w1        ' Offset 0x06 (NOT aligned to word boundary!)
  LONG  l1        ' Offset 0x08 (NOT aligned to long boundary!)
```

**Memory Layout:**
```
Offset: 0x00  0x01  0x02  0x03  0x04  0x05  0x06  0x07  0x08  0x09  0x0A  0x0B
        [--- object pointer ---]  v1    v2   [--w1--] [------l1------]
```

Notice that `w1` is at offset 0x06 (not word-aligned) and `l1` is at offset 0x08 (happens to be long-aligned only by coincidence).

### DAT Block Packing

Data in DAT blocks is also packed sequentially:

```spin2
DAT
myByte    BYTE    $AA           ' Offset 0x00
myWord    WORD    $BBCC         ' Offset 0x01 (NOT word-aligned!)
myLong    LONG    $DDEEFF00     ' Offset 0x03 (NOT long-aligned!)
```

**Memory Layout:**
```
Offset: 0x00  0x01  0x02  0x03  0x04  0x05  0x06
        $AA   $CC   $BB   $00   $FF   $EE   $DD
              [--myWord--] [------myLong------]
```

### Local Variable Packing

Local variables in PUB/PRI methods follow the same sequential packing:

```spin2
PUB Example() | BYTE b1, BYTE b2, WORD w1, LONG l1
  ' b1 at stack offset 0
  ' b2 at stack offset 1
  ' w1 at stack offset 2 (NOT word-aligned!)
  ' l1 at stack offset 4 (happens to be long-aligned by coincidence)
```

---

## The ALIGNW and ALIGNL Directives

To force alignment, use `ALIGNW` (word alignment) or `ALIGNL` (long alignment).

### Syntax

```spin2
VAR
  ALIGNW              ' Align next variable to word (2-byte) boundary
  ALIGNL              ' Align next variable to long (4-byte) boundary

DAT
  ALIGNW              ' Align next data to word boundary
  ALIGNL              ' Align next data to long boundary

PUB Method() | ALIGNW WORD x, ALIGNL LONG y
  ' ALIGNW before x ensures word alignment
  ' ALIGNL before y ensures long alignment
```

### How Alignment Works

The compiler pads with zero bytes until the current offset satisfies the alignment requirement:

- **ALIGNW**: Pads until offset is even (offset & 0x01 == 0)
- **ALIGNL**: Pads until offset is divisible by 4 (offset & 0x03 == 0)

```spin2
VAR
  BYTE  v1        ' Offset 0x04
  ALIGNW          ' Pads 1 byte (0x05 -> 0x06)
  BYTE  v2        ' Offset 0x06 (now word-aligned)
  ALIGNL          ' Pads 1 byte (0x07 -> 0x08)
  BYTE  v3        ' Offset 0x08 (now long-aligned)
```

**Memory Layout with Alignment:**
```
Offset: 0x04  0x05  0x06  0x07  0x08
        v1    [pad] v2    [pad] v3
```

---

## VAR Block Details

### Starting Offset

VAR blocks start at offset **0x04** (4 bytes), reserving the first long for the object pointer.

### End Alignment

After all variables are declared, the compiler automatically aligns to the next long boundary. This ensures that each object instance starts on a long boundary.

```spin2
VAR
  BYTE  b1        ' Offset 0x04
  BYTE  b2        ' Offset 0x05
  ' Compiler pads 2 bytes to reach 0x08
  ' Total VAR size: 8 bytes (padded from 2)
```

### Examples

**Without Explicit Alignment:**
```spin2
VAR
  BYTE  status          ' 0x04
  WORD  sensorValue     ' 0x05 (misaligned!)
  LONG  timestamp       ' 0x07 (misaligned!)
  BYTE  flags           ' 0x0B
  ' Total: 8 bytes + 4 bytes end-padding = 12 bytes
```

**With Explicit Alignment:**
```spin2
VAR
  BYTE  status          ' 0x04
  ALIGNW
  WORD  sensorValue     ' 0x06 (properly word-aligned)
  ALIGNL
  LONG  timestamp       ' 0x08 (properly long-aligned)
  BYTE  flags           ' 0x0C
  ' Total: 9 bytes + 3 bytes end-padding = 12 bytes
```

---

## DAT Block Details

### Data Declarations (BYTE, WORD, LONG)

Data declarations are packed sequentially without automatic alignment:

```spin2
DAT
header      BYTE    $AA, $BB, $CC       ' 3 bytes at offset 0
value       WORD    $1234               ' Misaligned at offset 3!
result      LONG    $DEADBEEF           ' Misaligned at offset 5!
```

### PASM Instructions (Special Case)

**Important Exception:** In COG/LUT mode, PASM instructions ARE automatically aligned to 4-byte (long) boundaries.

```spin2
DAT
            ORG     0                   ' COG mode
dataByte    BYTE    $FF                 ' Offset 0x00 (1 byte)
            ' Compiler auto-pads 3 bytes for instruction alignment
entry       MOV     PA, #1              ' Offset 0x04 (long-aligned)
```

This automatic alignment occurs via the `advanceToNextCogLong()` function before each instruction.

### ORGH Mode (Hub Memory)

In ORGH mode (hub memory), there is NO automatic instruction alignment:

```spin2
DAT
            ORGH                        ' Hub mode
dataByte    BYTE    $FF                 ' Offset 0x00
            ' NO automatic padding
moreData    LONG    $12345678           ' Offset 0x01 (misaligned!)
```

### Using ALIGNW and ALIGNL in DAT

```spin2
DAT
header      BYTE    $AA, $BB, $CC       ' 3 bytes
            ALIGNW                      ' Pad to word boundary
wordData    WORD    $1234               ' Now word-aligned
            ALIGNL                      ' Pad to long boundary
longData    LONG    $DEADBEEF           ' Now long-aligned
```

---

## Local Variable Details

### Declaration Syntax

Local variables support ALIGNW and ALIGNL inline:

```spin2
PUB Method() | BYTE b1, ALIGNW WORD w1, ALIGNL LONG l1
  ' b1 at offset 0
  ' padding added, w1 at next even offset
  ' padding added, l1 at next 4-byte aligned offset
```

### Stack Allocation

Local variables are allocated on the stack in declaration order:

```spin2
PUB Example() | BYTE a, BYTE b, WORD c, LONG d
  ' Stack layout (no alignment):
  '   a at offset 0
  '   b at offset 1
  '   c at offset 2 (misaligned word)
  '   d at offset 4 (happens to be aligned)

PUB ExampleAligned() | BYTE a, ALIGNW BYTE b, ALIGNL WORD c, LONG d
  ' Stack layout (with alignment):
  '   a at offset 0
  '   [pad 1 byte]
  '   b at offset 2 (word-aligned)
  '   [pad 2 bytes]
  '   c at offset 4 (long-aligned word)
  '   d at offset 6 (misaligned! ALIGNL only affected c)
```

### Multiple Alignment Directives

```spin2
PRI ProcessData() | BYTE status, ALIGNW WORD values[10], ALIGNL LONG result
  ' status at offset 0
  ' [1 byte padding]
  ' values at offset 2 (word-aligned)
  ' values uses 20 bytes (10 words)
  ' [2 bytes padding to long-align]
  ' result at offset 24 (long-aligned)
```

---

## Why Alignment Matters

### Performance

On the P2, misaligned memory accesses may require additional clock cycles:

- **RDLONG/WRLONG** at non-long-aligned addresses: Additional cycles
- **RDWORD/WRWORD** at non-word-aligned addresses: Additional cycles
- **RDBYTE/WRBYTE**: Always efficient (no alignment needed)

### Correctness with Hardware

Some hardware interfaces require aligned data:

```spin2
DAT
            ALIGNL
dmaBuffer   LONG    0[64]               ' DMA requires long-aligned buffer
```

### Atomic Operations

Spin2's atomic operations (LOCKTRY, LOCKREL) work on long values. Using them on misaligned data produces undefined behavior.

---

## Common Patterns

### 1. Structure-like VAR Layout

```spin2
VAR
  ' Header fields - tightly packed bytes
  BYTE  type
  BYTE  flags
  BYTE  reserved1
  BYTE  reserved2
  ' Now at offset 0x08, naturally long-aligned

  ' Main data - explicitly aligned
  ALIGNL
  LONG  timestamp
  LONG  sequence
  WORD  length
  ALIGNL
  LONG  checksum
```

### 2. Performance-Critical DAT Tables

```spin2
DAT
            ALIGNL
sinTable    LONG    0[256]              ' Long-aligned for fast RDLONG

            ALIGNW
pixelData   WORD    0[320]              ' Word-aligned for RDWORD
```

### 3. Mixed Local Variables

```spin2
PUB FastProcess() | ALIGNL LONG buffer[16], BYTE status, WORD count
  ' buffer long-aligned for performance
  ' status and count packed after buffer
```

### 4. Interpreter Data Tables

From the Spin2 interpreter source:
```spin2
DAT
        ORG
        ...byte tables...

        ALIGNW                          ' Word-align for vectors
vectors WORD    vector0, vector1, ...

        ALIGNL                          ' Long-align for interpreter
interp  ...instructions...
```

---

## Calculating Offsets

### VAR Block Formula

```
Offset(N) = 4 + sum of all previous variable sizes + alignment padding
```

Where:
- `4` = initial offset for object pointer
- Alignment padding is added by ALIGNW/ALIGNL directives

### Example Calculation

```spin2
VAR
  BYTE  a           ' Size: 1, Offset: 4
  BYTE  b           ' Size: 1, Offset: 5
  ALIGNW            ' Padding: 1 byte
  WORD  c           ' Size: 2, Offset: 6
  ALIGNL            ' Padding: 0 bytes (already at 8)
  LONG  d           ' Size: 4, Offset: 8
  BYTE  e           ' Size: 1, Offset: 12
  ' End padding: 3 bytes to reach offset 16
```

---

## Comparison with C/C++

| Aspect | Spin2/PASM2 | C/C++ |
|--------|-------------|-------|
| Default alignment | None (packed) | Natural alignment |
| Struct padding | None | Automatic |
| Array alignment | None | Element-aligned |
| End padding | VAR: to long boundary | Struct: to largest member |
| Manual control | ALIGNW, ALIGNL | `__attribute__((aligned))` |

### C Equivalent of Spin2 Behavior

To achieve Spin2-like packing in C:
```c
#pragma pack(push, 1)
struct packed_data {
    uint8_t  byte1;
    uint16_t word1;   // Misaligned at offset 1
    uint32_t long1;   // Misaligned at offset 3
};
#pragma pack(pop)
```

---

## Summary

### Key Points

1. **No automatic alignment** - BYTE, WORD, LONG data is packed sequentially
2. **Use ALIGNW/ALIGNL** - For explicit word/long alignment when needed
3. **VAR blocks end-aligned** - Compiler pads to long boundary at end
4. **PASM instructions auto-aligned** - Only in COG/LUT mode, not ORGH
5. **Performance impact** - Misaligned accesses may be slower
6. **Available everywhere** - ALIGNW/ALIGNL work in VAR, DAT, and local variables

### Quick Reference

| Directive | Effect | Pads Until |
|-----------|--------|------------|
| `ALIGNW` | Word-align next item | offset & 0x01 == 0 |
| `ALIGNL` | Long-align next item | offset & 0x03 == 0 |

### Best Practices

1. **Use alignment for performance-critical data** - Especially LONG arrays
2. **Consider memory layout** - Group same-sized variables together
3. **Document alignment requirements** - Comment when alignment matters
4. **Test on hardware** - Verify performance assumptions

---

*This document describes data packing and alignment in Spin2/PASM2 as implemented in the PNut-TS compiler.*
