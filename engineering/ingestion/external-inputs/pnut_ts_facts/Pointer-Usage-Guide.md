# Pointer Usage Guide for Spin2/PASM2

This document describes pointers in Spin2/PASM2, including typed pointers (`^BYTE`, `^WORD`, `^LONG`), structure pointers (`^structName`), and all the operations that can be performed with them.

## Language Version Requirement

**Typed pointers are a language extension that requires Spin2 version 45 or later.**

To use typed pointers (`^BYTE`, `^WORD`, `^LONG`) or structure pointers (`^structName`) in your code, you must include the language version directive at the very beginning of your source file:

```spin2
{Spin2_v45}
VAR
  ^BYTE  pByteData
  ^WORD  pWordData
  ^LONG  pLongData
  ' ... rest of your code
```

The directive `{Spin2_v45}` (or a later version like `{Spin2_v51}`) must appear before any other code. Without this directive, the compiler will not recognize the `^` pointer type syntax.

**Note**: Basic pointer operations using `@` (address-of) and `BYTE[]`/`WORD[]`/`LONG[]` memory access are part of the base Spin2 language and do not require a version directive.

## Overview

Pointers in Spin2 are 32-bit values that hold memory addresses. They enable:
- Direct memory access at arbitrary addresses
- Efficient array traversal without index calculations
- Pass-by-reference for method parameters
- Dynamic data structure manipulation

Spin2 supports four types of pointers:

| Pointer Type | Syntax | Points To | Increment Size |
|--------------|--------|-----------|----------------|
| Byte pointer | `^BYTE` | 8-bit data | 1 byte |
| Word pointer | `^WORD` | 16-bit data | 2 bytes |
| Long pointer | `^LONG` | 32-bit data | 4 bytes |
| Struct pointer | `^structName` | Structure data | Structure size |

---

## Declaring Pointers

### VAR Block Declarations

```spin2
VAR
  ^BYTE  pByteData          ' Pointer to byte data
  ^WORD  pWordData          ' Pointer to word data
  ^LONG  pLongData          ' Pointer to long data
  ^myStruct pStructData     ' Pointer to structure data
```

### Local Variable Declarations

Declare pointer locals after `|` in method signatures:

```spin2
PUB Process() | ^BYTE ptr, ^LONG dataPtr, ^point pPoint
  ' ptr, dataPtr, and pPoint are local pointers
```

### Parameter Declarations

Pointers can be method parameters:

```spin2
PUB ProcessBuffer(^BYTE pBuffer, LONG length)
  ' pBuffer points to byte data

PUB ModifyValue(^LONG pValue)
  ' pValue points to a long

PUB UpdatePoint(^point pPt)
  ' pPt points to a point structure
```

### Return Value Declarations

Methods can return pointers:

```spin2
PUB GetBuffer() : ^BYTE result
  result := @myBuffer

PUB FindItem() : ^LONG pItem
  ' Search and return pointer to found item

PUB GetOrigin() : ^point pOrigin
  pOrigin := @origin
```

### Pointer Arrays

**Note**: Pointers themselves cannot be arrays:

```spin2
VAR
  ^BYTE pArray              ' OK: single pointer
  ^BYTE pArrays[10]         ' ERROR: Pointers cannot be arrays
```

However, pointers can point to arrays of data.

---

## Getting Addresses: The `@` Operator

The `@` operator returns the address of a variable, array element, or structure member.

### Basic Address-Of

```spin2
VAR
  BYTE  myByte
  WORD  myWord
  LONG  myLong
  BYTE  buffer[256]

PUB Example() | ^BYTE pB, ^WORD pW, ^LONG pL
  pB := @myByte             ' Address of myByte
  pW := @myWord             ' Address of myWord
  pL := @myLong             ' Address of myLong
  pB := @buffer             ' Address of buffer[0]
```

### Array Element Addresses

```spin2
VAR
  LONG values[100]

PUB Example() | ^LONG ptr
  ptr := @values            ' Address of values[0]
  ptr := @values[0]         ' Same as above
  ptr := @values[50]        ' Address of values[50]
```

### Structure Member Addresses

```spin2
CON
  STRUCT point(x, y)
  STRUCT line(point a, point b)

VAR
  line myLine

PUB Example() | ^LONG pX, ^point pA
  pX := @myLine.a.x         ' Address of the x member
  pA := @myLine.a           ' Address of point a
```

### Method Pointers

Get the address of a method for indirect calls:

```spin2
PUB Example() | methodPtr
  methodPtr := @ProcessData ' Address of ProcessData method
  methodPtr()               ' Call through pointer
```

### String Addresses

```spin2
PUB Example() | ^BYTE pStr
  pStr := @"Hello, World!"  ' Address of inline string
  pStr := string("Test")    ' Address of string constant
```

---

## Dereferencing Pointers

### Reading Through Pointers

Access the data a pointer points to:

```spin2
VAR
  ^BYTE pByte
  ^WORD pWord
  ^LONG pLong

PUB Example() | value
  ' Read value at pointer location
  value := BYTE[pByte]      ' Read byte at pByte
  value := WORD[pWord]      ' Read word at pWord
  value := LONG[pLong]      ' Read long at pLong
```

### Writing Through Pointers

```spin2
PUB Example()
  BYTE[pByte] := $FF        ' Write byte at pByte
  WORD[pWord] := $1234      ' Write word at pWord
  LONG[pLong] := $DEADBEEF  ' Write long at pLong
```

### Indexed Access Through Pointers

Access elements at offsets from the pointer:

```spin2
PUB Example() | ^BYTE pData, i
  ' Access elements at index offsets
  value := BYTE[pData][0]   ' Same as BYTE[pData]
  value := BYTE[pData][5]   ' Element 5 bytes from pData

  ' Loop through array
  repeat i from 0 to 99
    BYTE[pData][i] := 0     ' Clear 100 bytes
```

### Structure Pointer Access

For structure pointers, use dot notation directly:

```spin2
CON
  STRUCT point(x, y)

VAR
  ^point pPt

PUB Example()
  ' Access structure members through pointer
  pPt.x := 100              ' Write to x member
  pPt.y := 200              ' Write to y member
  value := pPt.x            ' Read x member
```

### Bracket Dereference Notation

Use `[ptr]` to access the value a pointer points to (especially for structures):

```spin2
VAR
  ^point ptr
  point storage

PUB Example() | point temp
  ptr := @storage

  temp := [ptr]             ' Read entire structure
  [ptr] := temp             ' Write entire structure
```

---

## Pointer Arithmetic

### Increment and Decrement

Pointers support `++` and `--` operations that advance by the appropriate size:

| Pointer Type | `ptr++` / `ptr--` Advances By |
|--------------|-------------------------------|
| `^BYTE`      | 1 byte |
| `^WORD`      | 2 bytes |
| `^LONG`      | 4 bytes |
| `^struct`    | Structure size (bytes) |

### Basic Increment/Decrement

```spin2
VAR
  ^BYTE pByte
  ^LONG pLong

PUB Example()
  pByte++                   ' Advance by 1 byte
  pByte--                   ' Go back 1 byte

  pLong++                   ' Advance by 4 bytes
  pLong--                   ' Go back 4 bytes
```

### Pre-Increment/Decrement

Increment/decrement before using the pointer:

```spin2
PUB Example() | value
  value := ++pLong          ' Increment first, then read value
  value := --pByte          ' Decrement first, then read value
```

### Post-Increment/Decrement

Use the pointer, then increment/decrement:

```spin2
PUB Example() | value
  value := pLong++          ' Read value, then increment
  value := pByte--          ' Read value, then decrement
```

---

## Advanced Pointer Operations

### Bracket Pre/Post Increment Notation

Spin2 provides bracket notation for pointer operations:

```spin2
' Post-increment: use current, then advance
ptr[++]                     ' Return current address, then advance ptr
ptr[--]                     ' Return current address, then go back

' Pre-increment: advance first, then use
[++]ptr                     ' Advance ptr first, then return new address
[--]ptr                     ' Go back first, then return new address
```

### Structure Pointer with Increment

```spin2
CON
  STRUCT point(x, y)

VAR
  point points[10]
  ^point ptr

PUB Example() | value
  ptr := @points[0]

  ' Post-increment: access current, then advance
  value := ptr[++].x        ' Read x from current point, advance ptr

  ' Pre-increment: advance, then access
  value := [++]ptr.x        ' Advance ptr, then read x

  ' Combined with member operations
  value := ptr[++].x--      ' Read x (post-dec), then advance ptr
  value := --[++]ptr.x      ' Advance ptr, then pre-dec and read x
```

### Modify-and-Assign Through Pointers

```spin2
PUB Example()
  ' Arithmetic assignments through dereference
  LONG[ptr] += 10           ' Add 10 to value at ptr
  BYTE[ptr] -= 5            ' Subtract 5 from value at ptr
  WORD[ptr] *= 2            ' Multiply by 2

  ' Bitwise operations
  BYTE[ptr] |= $80          ' Set high bit
  BYTE[ptr] &= $0F          ' Mask to low nibble
  LONG[ptr] ^= $FF          ' XOR with $FF

  ' Using bracket notation with pointers
  [ptr] += 100              ' Add to value at ptr (for struct pointers)
```

### Pointer Value Modification

Modify the pointer while dereferencing:

```spin2
PUB Example()
  [ptr]++                   ' Increment value at ptr
  [ptr]--                   ' Decrement value at ptr
  [ptr]~                    ' Clear value at ptr (set to 0)
  [ptr]~~                   ' Set all bits at ptr
```

---

## Common Pointer Patterns

### Array Traversal

```spin2
VAR
  BYTE buffer[256]

PUB ClearBuffer() | ^BYTE ptr, i
  ptr := @buffer
  repeat 256
    BYTE[ptr++] := 0        ' Clear and advance

' Or equivalently:
PUB ClearBuffer2() | ^BYTE ptr
  ptr := @buffer
  repeat 256
    [ptr]~
    ptr++
```

### Linked List Traversal

```spin2
CON
  STRUCT node(^node next, data)

VAR
  ^node head

PUB TraverseList() | ^node current
  current := head
  repeat while current <> 0
    ProcessNode(current)
    current := current.next
```

### Buffer Processing

```spin2
PUB ProcessPacket(^BYTE pData, LONG length) | ^BYTE ptr, i
  ptr := pData
  repeat length
    ProcessByte(BYTE[ptr++])

PUB FillBuffer(^LONG pBuffer, LONG count, LONG value)
  repeat count
    LONG[pBuffer++] := value
```

### String Operations

```spin2
PUB StringLength(^BYTE pStr) : length
  length := 0
  repeat while BYTE[pStr++] <> 0
    length++

PUB CopyString(^BYTE pDest, ^BYTE pSrc)
  repeat while BYTE[pSrc] <> 0
    BYTE[pDest++] := BYTE[pSrc++]
  BYTE[pDest] := 0          ' Null terminator
```

### Structure Array Processing

```spin2
CON
  STRUCT point(x, y)

VAR
  point points[100]

PUB ScalePoints(scale) | ^point ptr, i
  ptr := @points
  repeat 100
    ptr.x *= scale
    ptr.y *= scale
    ptr++

PUB SumPoints() : totalX, totalY | ^point ptr
  ptr := @points
  totalX := 0
  totalY := 0
  repeat 100
    totalX += ptr[++].x     ' Read x, then advance
    totalY += ptr.y         ' Note: ptr already advanced
```

---

## Pointer Safety and Best Practices

### Initialize Before Use

Always initialize pointers before dereferencing:

```spin2
PUB Example() | ^BYTE ptr
  ptr := @buffer            ' Initialize first!
  BYTE[ptr] := value        ' Now safe to use
```

### Bounds Checking

Pointers don't have automatic bounds checking:

```spin2
PUB SafeCopy(^BYTE pDest, ^BYTE pSrc, LONG maxLen) | i
  repeat i from 0 to maxLen - 1
    if BYTE[pSrc] == 0
      quit
    BYTE[pDest++] := BYTE[pSrc++]
  BYTE[pDest] := 0
```

### Null Pointer Checks

Check for null (0) before dereferencing:

```spin2
PUB ProcessIfValid(^LONG ptr)
  if ptr <> 0
    LONG[ptr] := ProcessValue(LONG[ptr])
```

### Alignment Considerations

- `^BYTE` pointers can point anywhere
- `^WORD` pointers work best at even addresses
- `^LONG` pointers work best at 4-byte aligned addresses

The P2 handles misaligned access, but aligned access is more efficient.

### Pointer Type Consistency

Use the correct pointer type for the data:

```spin2
VAR
  LONG values[10]

PUB Example() | ^LONG pL, ^BYTE pB
  pL := @values             ' Correct: ^LONG for LONG array

  ' Accessing as different sizes (advanced usage):
  pB := @values             ' Points to first byte of values[0]
  BYTE[pB] := $12           ' Modifies low byte of values[0]
```

---

## Summary Table

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Declare byte ptr | `^BYTE ptr` | Pointer to byte data |
| Declare word ptr | `^WORD ptr` | Pointer to word data |
| Declare long ptr | `^LONG ptr` | Pointer to long data |
| Declare struct ptr | `^structName ptr` | Pointer to structure |
| Get address | `ptr := @var` | Assign address of variable |
| Read through ptr | `v := BYTE[ptr]` | Read byte at address |
| Write through ptr | `BYTE[ptr] := v` | Write byte at address |
| Indexed read | `v := LONG[ptr][i]` | Read at offset i |
| Struct member | `ptr.member` | Access structure member |
| Dereference struct | `[ptr]` | Access entire structure |
| Post-increment | `ptr++` | Use ptr, then advance |
| Pre-increment | `++ptr` | Advance, then use ptr |
| Post-increment (bracket) | `ptr[++]` | Access current, advance |
| Pre-increment (bracket) | `[++]ptr` | Advance, then access |
| Value increment | `[ptr]++` | Increment value at ptr |
| Modify-assign | `LONG[ptr] += v` | Add v to value at ptr |

---

## Comparison with BYTE[]/WORD[]/LONG[] Memory Access

Pointers and direct memory access are related but serve different purposes:

| Direct Access | Pointer Equivalent | Use Case |
|---------------|-------------------|----------|
| `BYTE[addr]` | `BYTE[ptr]` where `ptr := addr` | One-time access |
| `BYTE[addr][i]` | `BYTE[ptr][i]` or `ptr++` | Indexed access |
| `BYTE[@var]` | `ptr := @var; BYTE[ptr]` | Variable address |

**Use direct access** for:
- One-time or infrequent access
- Known addresses
- Simple indexed access

**Use pointers** for:
- Repeated access to same location
- Sequential traversal
- Pass-by-reference parameters
- Dynamic data structures

---

*This document describes pointer usage in Spin2/PASM2 as implemented in the PNut-TS compiler.*
