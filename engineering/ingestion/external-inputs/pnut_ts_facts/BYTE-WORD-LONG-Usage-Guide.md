# BYTE, WORD, and LONG Usage Guide for Spin2/PASM2

This document describes all the ways `BYTE`, `WORD`, and `LONG` can be used in the Spin2 and PASM2 languages for the Parallax Propeller 2 (P2) microcontroller.

## Overview

`BYTE`, `WORD`, and `LONG` are fundamental data type specifiers in Spin2/PASM2 that serve multiple purposes:

| Type   | Size    | Value Range (Unsigned) | Value Range (Signed) |
|--------|---------|------------------------|----------------------|
| `BYTE` | 8 bits  | 0 to 255               | -128 to 127          |
| `WORD` | 16 bits | 0 to 65,535            | -32,768 to 32,767    |
| `LONG` | 32 bits | 0 to 4,294,967,295     | -2,147,483,648 to 2,147,483,647 |

These keywords are used in seven distinct contexts:

1. **Variable Declarations** (VAR block)
2. **Local Variable Declarations** (PUB/PRI methods)
3. **Parameter Declarations** (PUB/PRI methods)
4. **Return Type Declarations** (PUB/PRI methods)
5. **Data Declarations** (DAT block)
6. **Memory Access Operators** (Spin2 expressions)
7. **Built-in Functions** (BYTEFILL, WORDMOVE, etc.)

---

## 1. Variable Declarations (VAR Block)

In a `VAR` block, `BYTE`, `WORD`, and `LONG` declare instance variables (hub memory allocated per object instance).

### Syntax

```spin2
VAR
  BYTE varName              ' Single byte variable
  BYTE varName[count]       ' Array of bytes
  WORD varName              ' Single word variable
  WORD varName[count]       ' Array of words
  LONG varName              ' Single long variable
  LONG varName[count]       ' Array of longs
```

### Notes

- Variables without an explicit type default to `LONG`
- Multiple variables of the same type can be declared on one line
- Variables are automatically aligned to their natural boundaries within the object

### Examples

```spin2
VAR
  BYTE status               ' 1 byte
  BYTE buffer[256]          ' 256-byte array
  WORD sensorValue          ' 2 bytes
  WORD readings[10]         ' 20-byte array (10 words)
  LONG counter              ' 4 bytes
  LONG timestamps[100]      ' 400-byte array
  myVar                     ' Defaults to LONG (4 bytes)
```

### Alignment Directives

Use `ALIGNW` and `ALIGNL` to force alignment:

```spin2
VAR
  BYTE v1
  ALIGNW                    ' Align next variable to word boundary
  BYTE v2
  ALIGNL                    ' Align next variable to long boundary
  BYTE v3
```

---

## 2. Pointer Variable Declarations

Spin2 supports typed pointers using the `^` (caret) prefix with size types.

### Syntax

```spin2
VAR
  ^BYTE pBytePtr            ' Pointer to byte data
  ^WORD pWordPtr            ' Pointer to word data
  ^LONG pLongPtr            ' Pointer to long data
```

### Notes

- All pointers are 32-bit values (LONG-sized)
- The type specifies the size of data the pointer references
- Pointer arithmetic increments/decrements by the type size

### Examples

```spin2
VAR
  ^BYTE pBuffer             ' Pointer to byte data
  ^WORD pTable              ' Pointer to word data
  ^LONG pValues             ' Pointer to long data

PUB Example() | ^BYTE ptr
  ptr := @buffer            ' Get address of buffer
  ptr++                     ' Increment by 1 byte
```

---

## 3. Local Variable Declarations (PUB/PRI Methods)

Local variables are declared after the `|` separator in method signatures.

### Syntax

```spin2
PUB methodName() | BYTE localByte, WORD localWord, LONG localLong
PRI methodName() | varName  ' Without type, defaults to LONG
```

### Examples

```spin2
PUB ProcessData() | BYTE temp, WORD index, LONG result
  temp := 0
  index := 100
  result := index * temp

PRI Calculate() | x, y, z  ' All default to LONG
  x := 1
  y := 2
  z := x + y
```

---

## 4. Parameter Declarations (PUB/PRI Methods)

Method parameters can be typed using `BYTE`, `WORD`, or `LONG`.

### Syntax

```spin2
PUB methodName(BYTE param1, WORD param2, LONG param3)
PUB methodName(param)       ' Without type, defaults to LONG
```

### Pointer Parameters

```spin2
PUB methodName(^BYTE pData, ^WORD pTable, ^LONG pValues)
```

### Examples

```spin2
PUB SetValue(BYTE channel, WORD value)
  ' channel is 8-bit, value is 16-bit

PUB ProcessBuffer(^BYTE pBuffer, LONG length)
  ' pBuffer points to byte data, length is 32-bit
```

---

## 5. Return Type Declarations (PUB/PRI Methods)

Methods can specify typed return values after the `:` separator.

### Syntax

```spin2
PUB methodName() : BYTE result
PUB methodName() : WORD result
PUB methodName() : LONG result
PUB methodName() : ^BYTE pResult   ' Return a byte pointer
```

### Multiple Return Values

```spin2
PUB methodName() : BYTE status, WORD value, LONG timestamp
```

### Examples

```spin2
PUB GetStatus() : BYTE status
  status := readHardware()

PUB GetPointer() : ^BYTE pData
  pData := @buffer

PUB GetValues() : WORD lowVal, WORD highVal
  lowVal := readLow()
  highVal := readHigh()
```

---

## 6. Data Declarations (DAT Block)

In `DAT` blocks, `BYTE`, `WORD`, and `LONG` specify the size of initialized data.

### Syntax

```spin2
DAT
  label   BYTE  value1, value2, ...       ' 8-bit values
  label   WORD  value1, value2, ...       ' 16-bit values
  label   LONG  value1, value2, ...       ' 32-bit values
```

### Notes

- Data is stored in hub memory
- Multiple values can follow a single type specifier
- Values can include expressions, constants, and addresses

### Examples

```spin2
DAT
  ' Byte data
  myBytes       BYTE    $00, $FF, 128, "Hello", 0

  ' Word data
  myWords       WORD    1000, 2000, 3000

  ' Long data
  myLongs       LONG    1_000_000, -500, $DEADBEEF

  ' Mixed data with in-line type overrides
  mixedData     LONG    $12345678
                WORD    $ABCD
                BYTE    $EF
```

### BYTEFIT and WORDFIT

Use `BYTEFIT` and `WORDFIT` to specify data that must fit within the smaller size:

```spin2
DAT
  smallVals     BYTEFIT   100, 200, 255    ' Values must fit in a byte
  medVals       WORDFIT   1000, 30000      ' Values must fit in a word
```

### Arrays and Repetition

Use `[count]` to repeat values:

```spin2
DAT
  zeros         BYTE    0[100]            ' 100 zero bytes
  pattern       WORD    $AAAA[50]         ' 50 copies of $AAAA
  longs         LONG    0[25]             ' 25 zero longs
```

---

## 7. Memory Access Operators (Spin2 Expressions)

`BYTE`, `WORD`, and `LONG` can be used as memory access operators to read or write specific memory locations.

### 7.1 Direct Memory Access

Access memory at an address using `TYPE[address]`:

```spin2
value := BYTE[address]          ' Read byte from address
value := WORD[address]          ' Read word from address
value := LONG[address]          ' Read long from address

BYTE[address] := value          ' Write byte to address
WORD[address] := value          ' Write word to address
LONG[address] := value          ' Write long to address
```

### 7.2 Indexed Memory Access

Access memory with base address and index using `TYPE[base][index]`:

```spin2
value := BYTE[@buffer][index]   ' Read byte at buffer + index
value := WORD[@array][index]    ' Read word at array + (index * 2)
value := LONG[@table][index]    ' Read long at table + (index * 4)
```

### 7.3 Variable Type Override

Override a variable's native type using `.BYTE`, `.WORD`, or `.LONG`:

```spin2
VAR
  LONG myLong

PUB Example()
  myLong.BYTE[0] := $12         ' Write to byte 0 of myLong
  myLong.BYTE[1] := $34         ' Write to byte 1 of myLong
  myLong.WORD[0] := $5678       ' Write to low word of myLong
```

### 7.4 Bitfield Access

Combine with bitfield notation for bit-level access:

```spin2
value := LONG[address].[7..0]   ' Read bits 7-0 of long at address
LONG[address].[31..24] := $FF   ' Write to bits 31-24
```

### Examples

```spin2
PUB WritePacket(^BYTE pBuffer, LONG length) | i
  ' Write header
  LONG[@pBuffer][0] := $AA55AA55   ' Magic number
  LONG[@pBuffer][1] := length      ' Length field

  ' Write data bytes
  repeat i from 0 to length-1
    BYTE[@pBuffer + 8][i] := getData(i)

PUB ReadSensor() : WORD result | addr
  addr := $4000_0000              ' Memory-mapped sensor
  result := WORD[addr]            ' Read 16-bit value

PUB ExtractFields(LONG packedValue) : BYTE field1, WORD field2
  field1 := packedValue.BYTE[0]   ' Extract low byte
  field2 := packedValue.WORD[1]   ' Extract high word
```

---

## 8. Built-in Functions

Spin2 provides size-specific functions for memory operations:

### Fill Functions

```spin2
BYTEFILL(address, value, count)  ' Fill 'count' bytes with 'value'
WORDFILL(address, value, count)  ' Fill 'count' words with 'value'
LONGFILL(address, value, count)  ' Fill 'count' longs with 'value'
```

### Move Functions

```spin2
BYTEMOVE(dest, source, count)    ' Copy 'count' bytes
WORDMOVE(dest, source, count)    ' Copy 'count' words
LONGMOVE(dest, source, count)    ' Copy 'count' longs
```

### Swap Functions

```spin2
BYTESWAP(addr1, addr2, count)    ' Swap 'count' bytes
WORDSWAP(addr1, addr2, count)    ' Swap 'count' words
LONGSWAP(addr1, addr2, count)    ' Swap 'count' longs
```

### Compare Functions

```spin2
BYTECOMP(addr1, addr2, count)    ' Compare 'count' bytes, returns 0/-1
WORDCOMP(addr1, addr2, count)    ' Compare 'count' words, returns 0/-1
LONGCOMP(addr1, addr2, count)    ' Compare 'count' longs, returns 0/-1
```

### Examples

```spin2
PUB InitBuffer(^BYTE pBuffer, LONG size)
  BYTEFILL(pBuffer, 0, size)      ' Zero the buffer

PUB CopyTable(^LONG pDest, ^LONG pSrc, LONG count)
  LONGMOVE(pDest, pSrc, count)    ' Copy longs efficiently

PUB CompareBuffers(^BYTE p1, ^BYTE p2, LONG size) : LONG match
  match := BYTECOMP(p1, p2, size) ' Returns -1 if equal, 0 if different
```

---

## 9. BYTE(), WORD(), LONG() as Data Constructors

These can be used in expressions to construct inline data:

### Syntax

```spin2
BYTE(val1, val2, ...)            ' Create byte sequence
WORD(val1, val2, ...)            ' Create word sequence
LONG(val1, val2, ...)            ' Create long sequence
```

### Mixed Types

```spin2
BYTE(val1, WORD val2, LONG val3) ' Mix sizes in one sequence
```

### Notes

- Total data cannot exceed 255 bytes
- Useful for creating inline constant data in expressions

### Examples

```spin2
PUB SendCommand(BYTE cmd)
  sendBuffer(BYTE(cmd, $00, $FF, WORD $1234, LONG counter))
```

---

## 10. PASM2 Usage

In PASM2 assembly code, `BYTE`, `WORD`, and `LONG` are used for data declarations and memory access instructions.

### Data Declarations

```pasm2
DAT
        ORG

entry   MOV     dest, source
        JMP     #entry

myByte        BYTE    $FF
myWord        WORD    $1234
myLong        LONG    $12345678
timeValue     LONG    CLK_FREQ / 1000   ' Computed constant
```

### Memory Instructions

PASM2 has specific instructions for sized memory access:

```pasm2
' Read from hub memory
RDBYTE  dest, address           ' Read byte from hub[address]
RDWORD  dest, address           ' Read word from hub[address]
RDLONG  dest, address           ' Read long from hub[address]

' Write to hub memory
WRBYTE  source, address         ' Write byte to hub[address]
WRWORD  source, address         ' Write word to hub[address]
WRLONG  source, address         ' Write long to hub[address]
```

### Examples

```pasm2
DAT
        ORG

        ' Read a byte from hub memory
        MOV     addr, ##bufferAddr
        RDBYTE  value, addr

        ' Write a long to hub memory
        MOV     addr, ##resultAddr
        WRLONG  result, addr

        ' Pointer with auto-increment
        RDLONG  data, ptra++    ' Read long, increment PTRA by 4

addr          RES     1
value         RES     1
data          RES     1
result        RES     1
```

---

## 11. Summary Table

| Context | BYTE | WORD | LONG | Notes |
|---------|------|------|------|-------|
| VAR declaration | `BYTE x` | `WORD x` | `LONG x` | Instance variables |
| VAR array | `BYTE x[n]` | `WORD x[n]` | `LONG x[n]` | Arrays |
| VAR pointer | `^BYTE p` | `^WORD p` | `^LONG p` | Typed pointers |
| Local variable | `\| BYTE x` | `\| WORD x` | `\| LONG x` | Stack variables |
| Parameter | `(BYTE x)` | `(WORD x)` | `(LONG x)` | Method params |
| Return value | `: BYTE x` | `: WORD x` | `: LONG x` | Return types |
| DAT data | `BYTE val` | `WORD val` | `LONG val` | Initialized data |
| Memory access | `BYTE[addr]` | `WORD[addr]` | `LONG[addr]` | Hub memory I/O |
| Type override | `.BYTE[n]` | `.WORD[n]` | `.LONG[n]` | Access sub-elements |
| Fill function | `BYTEFILL()` | `WORDFILL()` | `LONGFILL()` | Memory fill |
| Move function | `BYTEMOVE()` | `WORDMOVE()` | `LONGMOVE()` | Memory copy |
| Swap function | `BYTESWAP()` | `WORDSWAP()` | `LONGSWAP()` | Memory swap |
| Compare function | `BYTECOMP()` | `WORDCOMP()` | `LONGCOMP()` | Memory compare |
| Data constructor | `BYTE(...)` | `WORD(...)` | `LONG(...)` | Inline data |
| PASM2 read | `RDBYTE` | `RDWORD` | `RDLONG` | Hub read |
| PASM2 write | `WRBYTE` | `WRWORD` | `WRLONG` | Hub write |

---

## 12. Best Practices

1. **Choose Appropriate Sizes**: Use `BYTE` for small values, flags, and characters; `WORD` for medium-range values; `LONG` for large values and addresses.

2. **Memory Efficiency**: Use smaller types when possible to conserve hub memory, especially in arrays.

3. **Alignment Awareness**: Be aware that misaligned accesses may require extra cycles on the P2.

4. **Pointer Safety**: When using typed pointers, ensure the pointer arithmetic matches the data organization.

5. **Type Consistency**: Maintain consistent types when passing data between methods to avoid truncation or sign-extension issues.

6. **Use Built-in Functions**: Prefer `BYTEMOVE`/`WORDMOVE`/`LONGMOVE` over manual loops for better performance.

---

*This document describes BYTE, WORD, and LONG usage in Spin2/PASM2 as implemented in the PNut-TS compiler.*
