# FIELD Operator Usage Guide for Spin2/PASM2

This document describes the `FIELD` operator in Spin2/PASM2, which provides access to packed bit-fields stored in memory. The FIELD operator enables efficient manipulation of data structures where multiple values are packed into bytes, words, or longs.

## Language Version

The `FIELD` operator is part of the base Spin2 language and does not require a special language version directive. It works with any supported Spin2 version.

If your code uses other language extensions (such as `STRUCT`), you may still need a version directive like `{Spin2_v45}` for those features, but `FIELD` itself is always available.

## Overview

The `FIELD` operator allows you to:
- Access arbitrary bit-width fields within memory
- Create arrays of packed bit-fields (1-bit flags, 2-bit states, 12-bit IDs, etc.)
- Read and write individual fields without manual bit manipulation
- Efficiently store data when values don't require full byte/word/long storage

## Field Pointers

A **field pointer** is a special value that encodes:
1. The base address of the memory containing the fields
2. The bit range (width and position) of each field element

### Creating Field Pointers with `^@`

The `^@` (up-at) operator creates a field pointer from a variable with a bitfield specifier:

```spin2
fieldPointer := ^@variable.[highBit..lowBit]
```

This creates a pointer to an array of fields, where each field has the width `(highBit - lowBit + 1)` bits.

### Examples

```spin2
DAT
  ' Storage for different field sizes
  flagStorage   BYTE    0[100]        ' 100 bytes = 800 bits for 1-bit flags
  stateStorage  BYTE    0[50]         ' 50 bytes = 200 2-bit states
  idStorage     WORD    0[150]        ' 150 words for 12-bit IDs (12 bits each)

VAR
  LONG  flagField                     ' Field pointer to 1-bit flags
  LONG  stateField                    ' Field pointer to 2-bit states
  LONG  idField                       ' Field pointer to 12-bit IDs

PUB Initialize()
  ' Create field pointers
  flagField  := ^@flagStorage.[0]           ' 1-bit fields (bit 0 only)
  stateField := ^@stateStorage.[1..0]       ' 2-bit fields (bits 1..0)
  idField    := ^@idStorage.[11..0]         ' 12-bit fields (bits 11..0)
```

---

## Using the FIELD Operator

### Basic Syntax

```spin2
value := FIELD[fieldPointer][index]         ' Read field at index
FIELD[fieldPointer][index] := value         ' Write field at index
```

### Reading Fields

```spin2
PUB GetFlag(index) : flagValue
  flagValue := FIELD[flagField][index]      ' Returns 0 or 1

PUB GetState(index) : stateValue
  stateValue := FIELD[stateField][index]    ' Returns 0, 1, 2, or 3

PUB GetID(index) : idValue
  idValue := FIELD[idField][index]          ' Returns 0 to 4095
```

### Writing Fields

```spin2
PUB SetFlag(index, value)
  FIELD[flagField][index] := value          ' value: 0 or 1

PUB SetState(index, value)
  FIELD[stateField][index] := value         ' value: 0 to 3

PUB SetID(index, value)
  FIELD[idField][index] := value            ' value: 0 to 4095
```

### Modify-and-Assign Operations

Field elements support standard modify-and-assign operators:

```spin2
FIELD[fieldPointer][index]++                ' Increment
FIELD[fieldPointer][index]--                ' Decrement
FIELD[fieldPointer][index] += value         ' Add
FIELD[fieldPointer][index] -= value         ' Subtract
FIELD[fieldPointer][index] &= value         ' AND
FIELD[fieldPointer][index] |= value         ' OR
FIELD[fieldPointer][index] ^= value         ' XOR
FIELD[fieldPointer][index]~                 ' Clear (set to 0)
FIELD[fieldPointer][index]~~                ' Set all bits to 1
```

### Example: Toggle a Flag

```spin2
PUB ToggleFlag(index)
  FIELD[flagField][index] ^= 1              ' XOR with 1 to toggle

PUB ClearFlag(index)
  FIELD[flagField][index]~                  ' Clear to 0

PUB SetFlagTrue(index)
  FIELD[flagField][index]~~                 ' Set all bits (1 for 1-bit field)
```

---

## Field Pointer Details

### Bitfield Specification

The bitfield specifier `.[highBit..lowBit]` determines the field width:

| Specifier | Field Width | Values Per Byte | Values Per Word | Max Value |
|-----------|-------------|-----------------|-----------------|-----------|
| `.[0]`    | 1 bit       | 8               | 16              | 1         |
| `.[1..0]` | 2 bits      | 4               | 8               | 3         |
| `.[2..0]` | 3 bits      | 2 (partial)     | 5 (partial)     | 7         |
| `.[3..0]` | 4 bits      | 2               | 4               | 15        |
| `.[7..0]` | 8 bits      | 1               | 2               | 255       |
| `.[11..0]`| 12 bits     | -               | 1 (partial)     | 4095      |
| `.[15..0]`| 16 bits     | -               | 1               | 65535     |

### Storage Calculation

To calculate storage requirements:

```
bytes_needed = (count * field_width_bits + 7) / 8
```

For example:
- 100 1-bit flags: `(100 * 1 + 7) / 8 = 13 bytes`
- 50 2-bit states: `(50 * 2 + 7) / 8 = 13 bytes`
- 200 12-bit IDs: `(200 * 12 + 7) / 8 = 300 bytes`

### Word vs Byte Storage

For fields wider than 8 bits, use WORD or LONG storage:

```spin2
DAT
  ' 12-bit fields work better with WORD storage
  idStorage     WORD    0[(COUNT * 12 + 15) / 16]   ' Round to full WORDs
```

---

## Practical Example: Flash File System

This example is adapted from the flash file system implementation, demonstrating real-world FIELD usage:

```spin2
CON
  BLOCKS = 256                              ' Number of blocks in flash

  ' Calculate storage sizes
  ID_TO_BLOCKS_SZ = (BLOCKS * 12 + 15) / 16 ' 12-bit fields in WORDs
  FLAGS_SIZE      = (BLOCKS * 1 + 7) / 8    ' 1-bit fields in BYTEs
  STATES_SIZE     = (BLOCKS * 2 + 7) / 8    ' 2-bit fields in BYTEs

  ' Block states (2-bit values)
  B_FREE = %00                              ' Block is free
  B_TEMP = %01                              ' Block is temporary
  B_HEAD = %10                              ' Block is file head
  B_BODY = %11                              ' Block is file body

DAT
  ' Storage arrays
  IDToBlocks    WORD    0[ID_TO_BLOCKS_SZ]  ' ID-to-block mapping (12-bit)
  IDValids      BYTE    0[FLAGS_SIZE]       ' ID validity flags (1-bit)
  BlockStates   BYTE    0[STATES_SIZE]      ' Block states (2-bit)

  ' Field pointers (initialized at runtime)
  IDToBlock     LONG    0                   ' Pointer to 12-bit fields
  IDValid       LONG    0                   ' Pointer to 1-bit fields
  BlockState    LONG    0                   ' Pointer to 2-bit fields

PUB Initialize()
  ' Initialize field pointers
  IDToBlock  := ^@IDToBlocks.[11..0]        ' 12-bit ID-to-block mapping
  IDValid    := ^@IDValids.[0]              ' 1-bit validity flags
  BlockState := ^@BlockStates.[1..0]        ' 2-bit block states

PUB AllocateBlock() : blockID | blockAddress
  ' Find a free block
  repeat blockAddress from 0 to BLOCKS - 1
    if FIELD[BlockState][blockAddress] == B_FREE
      ' Found free block - mark as temporary
      FIELD[BlockState][blockAddress] := B_TEMP
      return blockAddress
  return -1                                 ' No free blocks

PUB SetBlockAsHead(blockID, blockAddress)
  ' Mark block as file head
  FIELD[IDToBlock][blockID] := blockAddress ' Set ID-to-block mapping
  FIELD[IDValid][blockID]~~                 ' Set ID as valid
  FIELD[BlockState][blockAddress] := B_HEAD ' Set block state

PUB FreeBlock(blockID) | blockAddress
  ' Free a block
  if FIELD[IDValid][blockID]                ' Check if ID is valid
    blockAddress := FIELD[IDToBlock][blockID]
    FIELD[BlockState][blockAddress] := B_FREE
    FIELD[IDValid][blockID]~                ' Clear validity flag

PUB IsBlockFree(blockAddress) : isFree
  isFree := FIELD[BlockState][blockAddress] == B_FREE

PUB GetBlockAddress(blockID) : blockAddress
  if FIELD[IDValid][blockID]
    blockAddress := FIELD[IDToBlock][blockID]
  else
    blockAddress := -1                      ' Invalid ID
```

---

## Using FIELD with Register Bitfields

The `^@` operator can also create field pointers from register bitfields:

```spin2
PUB GetRegisterField() : value | fieldPtr
  fieldPtr := ^@DIRA.[23..21]               ' 3-bit field from DIRA bits 23-21
  value := FIELD[fieldPtr]                  ' Read the field
```

### Reading Variable Bitfields

```spin2
VAR
  LONG myValue

PUB Example() | bits3Field
  myValue := $12345678
  bits3Field := ^@myValue.[23..21]          ' Create pointer to bits 23-21
  pinh(FIELD[bits3Field])                   ' Access the 3-bit field
```

---

## Field Operator vs. Direct Bitfield Access

### When to Use FIELD

- **Arrays of packed values**: When you need many small values (flags, states, IDs)
- **Memory efficiency**: When saving memory is important
- **Dynamic indexing**: When the field index is computed at runtime

### When to Use Direct Bitfield Access

- **Single values**: For one-off bitfield operations
- **Known positions**: When the bit positions are constants

```spin2
' Direct bitfield access (for single values)
value := myLong.[7..0]                      ' Read bits 7-0 directly

' FIELD access (for arrays of packed values)
value := FIELD[fieldPtr][index]             ' Read from packed array
```

---

## Performance Considerations

1. **Field pointer creation**: Creating a field pointer with `^@` computes the encoding once; store and reuse it.

2. **Access overhead**: FIELD access has some overhead compared to direct array access, but saves significant memory for small values.

3. **Alignment**: Fields are not aligned; they pack contiguously across byte/word boundaries.

4. **Read-modify-write**: Writing a field involves reading the containing byte/word, modifying the bits, and writing back.

---

## Summary

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Create pointer | `ptr := ^@var.[h..l]` | Create field pointer to bitfield |
| Read field | `v := FIELD[ptr][i]` | Read field at index i |
| Write field | `FIELD[ptr][i] := v` | Write value to field at index i |
| Increment | `FIELD[ptr][i]++` | Increment field |
| Clear | `FIELD[ptr][i]~` | Set field to zero |
| Set bits | `FIELD[ptr][i]~~` | Set all field bits to 1 |
| Modify | `FIELD[ptr][i] op= v` | Modify-and-assign |

---

## Common Patterns

### Boolean Flag Array

```spin2
DAT
  flags     BYTE    0[(COUNT + 7) / 8]
  flagPtr   LONG    0

PUB InitFlags()
  flagPtr := ^@flags.[0]

PUB SetFlag(n)
  FIELD[flagPtr][n]~~

PUB ClearFlag(n)
  FIELD[flagPtr][n]~

PUB TestFlag(n) : isSet
  isSet := FIELD[flagPtr][n]
```

### State Machine States

```spin2
CON
  STATE_IDLE    = 0
  STATE_RUNNING = 1
  STATE_PAUSED  = 2
  STATE_ERROR   = 3

DAT
  states    BYTE    0[(COUNT * 2 + 7) / 8]
  statePtr  LONG    0

PUB InitStates()
  statePtr := ^@states.[1..0]

PUB SetState(n, state)
  FIELD[statePtr][n] := state

PUB GetState(n) : state
  state := FIELD[statePtr][n]
```

---

*This document describes FIELD operator usage in Spin2/PASM2 as implemented in the PNut-TS compiler.*
