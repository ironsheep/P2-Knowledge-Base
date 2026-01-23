# Addressing Operators Usage Guide for Spin2/PASM2

This document provides comprehensive coverage of the address-of operators (`@`, `@@`, `^@`) in Spin2/PASM2, including how they work with variables, structures, arrays, and different memory spaces.

## Overview

The Propeller 2 provides three address-related operators for obtaining addresses of data and code:

| Operator | Name | Purpose | Result Type |
|----------|------|---------|-------------|
| `@` | Address-of | Get compile-time/object-relative address | Object-relative address |
| `@@` | Hub Address-of | Add program base to get runtime hub address | Absolute hub address |
| `^@` | Field Pointer | Get field pointer for bitfield access | Field pointer |

These operators work together with the P2's memory architecture to provide flexible addressing capabilities for both Spin2 high-level code and PASM2 assembly.

---

## P2 Memory Architecture

Understanding the P2 memory model is essential for proper use of addressing operators.

### Memory Spaces

| Memory | Address Range | Size | Access |
|--------|--------------|------|--------|
| **COG RAM** | $000-$1FF (long addresses) | 512 longs (2KB) | Direct register access |
| **LUT RAM** | $200-$3FF (long addresses) | 512 longs (2KB) | RDLUT/WRLUT instructions |
| **HUB RAM** | $00000-$7FFFF (byte addresses) | 512KB | RDLONG/WRLONG, etc. |

### Address Encoding

The compiler encodes addresses differently depending on their memory space:

- **COG addresses**: Stored as long addresses (0-$1FF range)
- **HUB addresses**: Stored as byte addresses, often with upper bits indicating hub mode
- **Object-relative addresses**: Lower 20 bits contain the offset from object base

---

## The `@` Operator (Address-Of)

The `@` operator returns the address of a symbol. The exact meaning depends on context.

### Basic Usage with Variables

```spin2
VAR
  BYTE  myByte
  WORD  myWord
  LONG  myLong
  BYTE  buffer[256]

PUB Example() | ptr
  ptr := @myByte            ' Address of myByte in VAR space
  ptr := @myWord            ' Address of myWord
  ptr := @myLong            ' Address of myLong
  ptr := @buffer            ' Address of buffer[0]
  ptr := @buffer[10]        ' Address of buffer[10]
```

### Usage with DAT Section Labels

In DAT sections, `@` returns the object-relative address of a label:

```spin2
DAT
myData      LONG    0, 1, 2, 3
myString    BYTE    "Hello", 0

PUB Example() | addr
  addr := @myData           ' Object-relative address of myData
  addr := @myString         ' Object-relative address of myString
```

### Usage with Array Indexing

The `@` operator can be combined with array indices to get addresses of specific elements:

```spin2
VAR
  LONG values[100]
  BYTE data[256]

PUB Example() | ptr
  ptr := @values[0]         ' Address of first element
  ptr := @values[50]        ' Address of element at index 50
  ptr := @data[n]           ' Address of element at runtime index n
```

**Address Calculation**: For indexed access, the compiler calculates:
```
address = base_address + (index << wordSize)
```
Where `wordSize` is 0 for BYTE, 1 for WORD, 2 for LONG.

### Usage with Strings

The `@` operator can get addresses of inline strings:

```spin2
PUB Example() | pStr
  pStr := @"Hello, World!"  ' Address of inline string constant
```

With escape sequences:
```spin2
PUB Example() | pStr
  pStr := @\"Line1\nLine2"  ' String with escape processing
```

### Usage with Methods (Method Pointers)

Get the address of a method for indirect calls:

```spin2
PUB Main() | methodPtr
  methodPtr := @ProcessData
  methodPtr()               ' Indirect method call

PUB ProcessData()
  ' ... processing code ...
```

### Usage with Object Methods

Get method pointers from child objects:

```spin2
OBJ
  child : "childObject"

PUB Example() | methodPtr
  methodPtr := @child.SomeMethod    ' Method pointer in child object
  methodPtr := @child[0].SomeMethod ' Method pointer in indexed object array
```

### Restrictions on `@`

The `@` operator has specific restrictions:

1. **Cannot be used with COG registers**: Use `^@` instead
   ```spin2
   ' WRONG: @DIRA, @INA, @OUTA
   ' Compiler error: "@ is not allowed, use ^@ to get field pointer"
   ```

2. **Cannot be used with bitfields**: Use `^@` instead
   ```spin2
   ' WRONG: @myVar.[3..0]
   ' Compiler error: "@ is not allowed for bitfields, use ^@ to get field pointer"
   ```

---

## The `@@` Operator (Hub Address-Of)

The `@@` operator adds the program base address to a value, converting an object-relative address to an absolute hub address.

### Basic Usage

```spin2
DAT
dataTable   LONG    100, 200, 300, 400

PUB Example() | hubAddr
  hubAddr := @@dataTable    ' Absolute hub address of dataTable
```

### Understanding `@` vs `@@`

The key distinction:
- `@` returns an **object-relative** address (offset from object base)
- `@@` returns an **absolute hub** address (actual memory location)

```spin2
DAT
myData      LONG    $12345678

PUB Example() | relAddr, absAddr
  relAddr := @myData        ' Object-relative offset
  absAddr := @@myData       ' Absolute hub address

  ' These are equivalent:
  absAddr := @@myData
  absAddr := @myData + PBASE ' PBASE is the program base address
```

### Lookup Tables with `@@`

A common pattern is storing `@` addresses in tables, then using `@@` to resolve them:

```spin2
DAT
' Table of string addresses (object-relative)
stringTable WORD    @str0, @str1, @str2, @str3, @str4

str0        BYTE    "Zero", 0
str1        BYTE    "One", 0
str2        BYTE    "Two", 0
str3        BYTE    "Three", 0
str4        BYTE    "Four", 0

PUB GetString(index) : pStr
  ' Resolve object-relative address to hub address
  pStr := @@WORD[@stringTable][index]
```

### Complex `@@` Expressions

The `@@` operator can be combined with type specifiers and indexing:

```spin2
DAT
pointerTable    LONG    @buffer1, @buffer2, @buffer3

PUB GetBuffer(index) : pBuffer
  pBuffer := @@LONG[@pointerTable][index]
```

This pattern:
1. `@pointerTable` - get address of the table
2. `LONG[...][index]` - read the LONG at that index
3. `@@` - add program base to convert to hub address

### When to Use `@@`

Use `@@` when:
- Initializing pointers from DAT section addresses
- Resolving addresses stored in lookup tables
- Converting object-relative addresses for runtime use

```spin2
DAT
dataBlock   BYTE    0[256]

VAR
  LONG pData

PUB Init()
  pData := @@dataBlock      ' Store hub address in VAR

PUB Process()
  BYTE[pData][0] := $FF     ' Use hub address for access
```

---

## The `^@` Operator (Field Pointer)

The `^@` operator creates a field pointer for accessing bitfields within variables.

### Basic Usage

```spin2
VAR
  LONG storage

PUB Example() | fieldPtr, value
  ' Create field pointer for 4-bit field at bits [3..0]
  fieldPtr := ^@storage.[3..0]

  ' Access through FIELD operator
  FIELD[fieldPtr][0] := 5   ' Write to first 4-bit slot
  value := FIELD[fieldPtr][0] ' Read from first 4-bit slot
```

### Field Width Specification

The bit range notation specifies field width:

| Notation | Width | Range |
|----------|-------|-------|
| `.[0]` or `.[0..0]` | 1 bit | 0-1 |
| `.[1..0]` | 2 bits | 0-3 |
| `.[3..0]` | 4 bits | 0-15 |
| `.[7..0]` | 8 bits | 0-255 |
| `.[11..0]` | 12 bits | 0-4095 |
| `.[15..0]` | 16 bits | 0-65535 |
| `.[31..0]` | 32 bits | Full LONG |

### Field Pointer Examples

```spin2
VAR
  LONG flagStorage          ' 32 single-bit flags
  LONG nibbleStorage        ' 8 four-bit values

PUB Example() | flagPtr, nibPtr, i
  ' 1-bit fields (32 flags in one LONG)
  flagPtr := ^@flagStorage.[0]
  repeat i from 0 to 31
    FIELD[flagPtr][i] := i & 1    ' Alternating 0/1

  ' 4-bit fields (8 nibbles in one LONG)
  nibPtr := ^@nibbleStorage.[3..0]
  repeat i from 0 to 7
    FIELD[nibPtr][i] := i         ' Store 0-7
```

### When to Use `^@` vs `@`

| Situation | Use |
|-----------|-----|
| Get address of a variable | `@` |
| Get address of a COG register | `^@` |
| Get field pointer for bitfield access | `^@` |
| Get address of array element | `@` |
| Get address of structure member | `@` |

---

## Addressing with Structures

Structures (STRUCT) provide organized data layouts with member addressing support.

### Structure Address

Get the address of an entire structure:

```spin2
CON
  STRUCT point(x, y)

VAR
  point myPoint

PUB Example() | ptr
  ptr := @myPoint           ' Address of the structure

  ' Access through pointer
  LONG[ptr][0] := 100       ' x member (first LONG)
  LONG[ptr][1] := 200       ' y member (second LONG)
```

### Structure Member Address

Get the address of a specific member within a structure:

```spin2
CON
  STRUCT point(x, y)
  STRUCT line(point a, point b)

VAR
  line myLine

PUB Example() | ptr
  ptr := @myLine.a          ' Address of point 'a' within line
  ptr := @myLine.a.x        ' Address of x within point a
  ptr := @myLine.b.y        ' Address of y within point b
```

### Nested Structure Addressing

For deeply nested structures:

```spin2
CON
  STRUCT point(x, y)
  STRUCT rect(point topLeft, point bottomRight)

VAR
  rect myRect

PUB Example() | ptr
  ' Multi-level member addressing
  ptr := @myRect.topLeft.x
  LONG[ptr] := 10

  ptr := @myRect.bottomRight
  ptr.x := 100              ' Using struct pointer syntax
  ptr.y := 200
```

### Structure Array Element Addressing

```spin2
CON
  STRUCT point(x, y)
  NUM_POINTS = 10

VAR
  point points[NUM_POINTS]

PUB Example() | ptr, i
  ' Address of specific array element
  ptr := @points[0]         ' First point
  ptr := @points[5]         ' Sixth point
  ptr := @points[i]         ' Point at runtime index

  ' Iterate with address arithmetic
  ptr := @points[0]
  repeat NUM_POINTS
    ptr.x := 0
    ptr.y := 0
    ptr += 8                ' Advance by structure size (2 LONGs = 8 bytes)
```

---

## Addressing in PASM2 Context

Address operators behave differently in PASM2 inline assembly vs Spin2 code.

### DAT Section Addressing

In DAT sections, addresses are relative to the DAT origin:

```spin2
DAT
        ORG     0                       ' COG origin

entry   MOV     addr, #@myData          ' Immediate object-relative address
        RDLONG  value, addr             ' Read from hub

myData  LONG    0

addr    RES     1
value   RES     1
```

### ORG vs ORGH Impact

The origin directive affects how addresses are interpreted:

```spin2
DAT
        ORG     0                       ' COG mode: addresses 0-$1FF
cogCode
        MOV     PA, #@hubData           ' Get hub address
        JMP     #cogCode                ' COG-relative jump

        ORGH    $400                    ' HUB mode: addresses >= $400
hubCode
        RDLONG  temp, ##@hubData        ' Hub addressing

hubData LONG    $12345678
```

### Compile-Time vs Runtime Addresses

In PASM2 inline assembly:

```spin2
PUB DoSomething() | result
  ORG
    MOV     PA, #@myVar               ' Compile-time address constant
    RDLONG  result, PA                ' Runtime hub read
  END

DAT
myVar   LONG    42
```

---

## Address Arithmetic

Once you have an address, you can perform arithmetic on it.

### Basic Pointer Arithmetic

```spin2
VAR
  BYTE buffer[256]

PUB Example() | ptr
  ptr := @buffer

  ' Move to specific offset
  ptr += 10                 ' Now points to buffer[10]
  ptr -= 5                  ' Now points to buffer[5]
```

### Calculating Sizes with Address Subtraction

```spin2
DAT
startData   BYTE    0[100]
endData

PUB GetSize() : size
  size := @endData - @startData   ' Returns 100
```

### Type-Aware Indexing

When using type specifiers, indexing is scaled appropriately:

```spin2
VAR
  LONG values[10]

PUB Example() | ptr, val
  ptr := @values

  val := LONG[ptr][0]       ' values[0]
  val := LONG[ptr][5]       ' values[5] (ptr + 5*4 = ptr + 20)

  ' Equivalent manual calculation:
  val := LONG[ptr + 20]     ' Same as LONG[ptr][5]
```

---

## Built-in Methods Using Addresses

Many built-in methods accept addresses as parameters.

### Memory Copy Operations

```spin2
VAR
  BYTE src[100]
  BYTE dst[100]
  LONG lsrc[25]
  LONG ldst[25]

PUB Example()
  BYTEMOVE(@dst, @src, 100)   ' Copy 100 bytes
  WORDMOVE(@dst, @src, 50)    ' Copy 50 words (100 bytes)
  LONGMOVE(@ldst, @lsrc, 25)  ' Copy 25 longs
```

### Memory Comparison

```spin2
PUB Compare() | result
  result := BYTECOMP(@buf1, @buf2, 100)   ' Compare 100 bytes
  result := WORDCOMP(@buf1, @buf2, 50)    ' Compare 50 words
  result := LONGCOMP(@buf1, @buf2, 25)    ' Compare 25 longs
```

### Memory Swap

```spin2
PUB SwapBuffers()
  BYTESWAP(@buf1, @buf2, 100)   ' Swap 100 bytes
  WORDSWAP(@buf1, @buf2, 50)    ' Swap 50 words
  LONGSWAP(@buf1, @buf2, 25)    ' Swap 25 longs
```

### Register Operations

```spin2
VAR
  LONG hubBuffer[16]

PUB CogTransfer()
  SETREGS(@hubBuffer, $1E0, 4)       ' Hub to COG: copy 4 longs to $1E0
  GETREGS(@hubBuffer[8], $1E0, 4)    ' COG to Hub: copy 4 longs from $1E0
```

---

## Common Patterns and Idioms

### String Table Lookup

```spin2
DAT
strings     WORD    @s0, @s1, @s2, @s3
s0          BYTE    "Option A", 0
s1          BYTE    "Option B", 0
s2          BYTE    "Option C", 0
s3          BYTE    "Option D", 0

PUB GetOptionName(index) : pStr
  pStr := @@WORD[@strings][index]
```

### Buffer Initialization from DAT

```spin2
DAT
defaults    LONG    100, 200, 300, 400

VAR
  LONG settings[4]

PUB Init()
  LONGMOVE(@settings, @@defaults, 4)
```

### Pointer-Based State Machine

```spin2
DAT
stateHandlers   LONG    @State0, @State1, @State2

VAR
  LONG currentHandler

PUB Init()
  currentHandler := @@stateHandlers[0]

PUB Run()
  currentHandler()          ' Call current state handler
```

---

## Gotchas and Pitfalls

### 1. Forgetting `@@` for DAT Addresses

**Wrong:**
```spin2
DAT
myData  LONG    0

PUB Example()
  LONG[@myData] := 100      ' Object-relative, may not work as expected
```

**Right:**
```spin2
PUB Example()
  LONG[@@myData] := 100     ' Absolute hub address
```

### 2. Using `@` with Registers

**Wrong:**
```spin2
PUB Example() | ptr
  ptr := @DIRA              ' ERROR: @ not allowed with registers
```

**Right:**
```spin2
PUB Example() | fieldPtr
  fieldPtr := ^@DIRA.[15..0] ' Use ^@ for register/field access
```

### 3. Confusing Byte vs Long Addresses

COG addresses are in **longs**, HUB addresses are in **bytes**:

```spin2
DAT
        ORG     0
        MOV     reg, #$10         ' COG address $10 = long address

        ORGH    $400
        RDLONG  val, ##$1000      ' HUB address $1000 = byte address
```

### 4. Address Alignment

For optimal performance, ensure proper alignment:

```spin2
DAT
        ALIGNL                    ' Align to long boundary
myLongs LONG    0, 0, 0, 0

        ALIGNW                    ' Align to word boundary
myWords WORD    0, 0, 0, 0
```

### 5. Object-Relative vs Absolute in Tables

When building address tables in DAT sections, use `@` (object-relative) and resolve with `@@` at runtime:

```spin2
DAT
' CORRECT: Store object-relative, resolve at runtime
addrTable   LONG    @data1, @data2, @data3

PUB GetAddr(i) : addr
  addr := @@LONG[@addrTable][i]   ' Resolve to hub address
```

---

## Summary Tables

### Operator Quick Reference

| Operator | Syntax | Returns | Use Case |
|----------|--------|---------|----------|
| `@` | `@symbol` | Object-relative address | Get address of variable/label |
| `@` | `@array[i]` | Address of element | Get address of array element |
| `@` | `@struct.member` | Member address | Get address of structure member |
| `@` | `@method` | Method pointer | Get address of method |
| `@` | `@"string"` | String address | Get address of inline string |
| `@@` | `@@symbol` | Absolute hub address | Convert to runtime address |
| `@@` | `@@table[i]` | Resolved pointer | Lookup and resolve from table |
| `^@` | `^@var.[bits]` | Field pointer | Create bitfield accessor |

### Address Types by Symbol Location

| Symbol Location | `@` Returns | `@@` Returns |
|-----------------|-------------|--------------|
| VAR variable | VAR-base offset | Runtime hub address |
| DAT label | Object-relative offset | Absolute hub address |
| Local variable | Stack-frame offset | Runtime stack address |
| Method | Method index | Callable address |
| String literal | String data offset | String hub address |

## Related Documentation

- **Pointer-Usage-Guide.md** - Comprehensive pointer operations with `^BYTE`, `^WORD`, `^LONG`
- **STRUCT-Usage-Guide.md** - Structure definition and member access
- **FIELD-Operator-Usage-Guide.md** - Bitfield access with FIELD[]
- **BYTE-WORD-LONG-Usage-Guide.md** - Memory access operators
- **ORG-Directives-Usage-Guide.md** - Origin directives for PASM2

---

*This document describes addressing operators as implemented in the PNut-TS compiler for Spin2/PASM2.*
