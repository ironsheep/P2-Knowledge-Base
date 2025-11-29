# Appendix F: Opcode Bit Patterns Reference

## Instruction Word Format

The P2 uses a fixed 32-bit instruction word with five distinct fields that encode all instruction information:

```
 31  30  29  28  27  26  25  24  23  22  21  20  19  18  17  16  15  14  13  12  11  10   9   8   7   6   5   4   3   2   1   0
├───┴───┴───┴───┼───┴───┴───┴───┴───┴───┴───┼───┴───┴───┼───┴───┴───┴───┴───┴───┴───┴───┴───┼───┴───┴───┴───┴───┴───┴───┴───┴───┤
│    EEEE       │       OOOOOOO             │    CZI    │         DDDDDDDDD                 │         SSSSSSSSS                 │
│  Condition    │       Opcode              │  Effects  │         Destination               │         Source                    │
│   (4 bits)    │       (7 bits)            │  (3 bits) │         (9 bits)                  │         (9 bits)                  │
└───────────────┴───────────────────────────┴───────────┴───────────────────────────────────┴───────────────────────────────────┘
```

This compact encoding allows:
- 16 execution conditions
- 128 primary opcodes
- 512 register addresses (COG and LUT)
- Immediate mode selection
- Flag effect control

## Field Definitions

### Condition Field (EEEE) - Bits 31:28

The condition field determines whether an instruction executes based on the current state of the C and Z flags:

| EEEE | Mnemonic | Execute When | Description |
|------|----------|--------------|-------------|
| 0000 | IF_ALWAYS | Always | Unconditional execution (default) |
| 0001 | IF_NC_AND_NZ | C=0 AND Z=0 | Above (unsigned) |
| 0010 | IF_NC_AND_Z | C=0 AND Z=1 | Not carry and zero |
| 0011 | IF_NC | C=0 | Not carry (also IF_AE, IF_GE) |
| 0100 | IF_C_AND_NZ | C=1 AND Z=0 | Carry and not zero |
| 0101 | IF_NZ | Z=0 | Not zero (also IF_NE) |
| 0110 | IF_C_NE_Z | C≠Z | Carry not equal zero |
| 0111 | IF_NC_OR_NZ | C=0 OR Z=0 | Not (carry and zero) |
| 1000 | IF_C_AND_Z | C=1 AND Z=1 | Carry and zero |
| 1001 | IF_C_EQ_Z | C=Z | Carry equals zero |
| 1010 | IF_Z | Z=1 | Zero (also IF_E) |
| 1011 | IF_NC_OR_Z | C=0 OR Z=1 | Not carry or zero |
| 1100 | IF_C | C=1 | Carry (also IF_B, IF_LT) |
| 1101 | IF_C_OR_NZ | C=1 OR Z=0 | Carry or not zero |
| 1110 | IF_C_OR_Z | C=1 OR Z=1 | Carry or zero (also IF_BE, IF_LE) |
| 1111 | IF_NEVER | Never | Never executes (used for padding) |

When a condition is false, the instruction is skipped with no effect on registers or flags.

### CZI Field - Bits 23:21

The CZI field controls flag updates and addressing mode:

| Bit | Name | Meaning |
|-----|------|---------|
| 23 | C | Write C flag if set (WC effect) |
| 22 | Z | Write Z flag if set (WZ effect) |
| 21 | I | Source is immediate if set (#) |

**Examples:**
- `CZI = 000`: No flag writes, S is register address
- `CZI = 001`: No flag writes, S is immediate value
- `CZI = 100`: Write C only, S is register address
- `CZI = 101`: Write C only, S is immediate value
- `CZI = 110`: Write C and Z, S is register address
- `CZI = 111`: Write C and Z, S is immediate value

### Destination Field (D) - Bits 18:9

9-bit field specifying the destination register address:

| Range | Region |
|-------|--------|
| $000-$1EF | COG RAM (496 registers) |
| $1F0-$1FF | Special registers (16 registers) |
| $200-$3FF | LUT RAM (512 longs) |

The D field always references a register, never an immediate value.

### Source Field (S) - Bits 8:0

9-bit field specifying either:
- **Register address** (when I=0): Same address space as D field
- **Immediate value** (when I=1): Unsigned 0-511, or extended by AUGS

When used as immediate, negative values or values >511 require AUGS prefix.

### Opcode Field (OOOOOOO) - Bits 27:21

7-bit field encoding the instruction operation. See Opcode Organization section below.

## Opcode Field Organization

The 7-bit opcode space (128 possible opcodes) is organized by instruction category:

### Basic Operations (0000000-0001111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 0000000 | ROR | Rotate/shift |
| 0000001 | ROL | Rotate/shift |
| 0000010 | SHR | Rotate/shift |
| 0000011 | SHL | Rotate/shift |
| 0000100 | RCR | Rotate/shift |
| 0000101 | RCL | Rotate/shift |
| 0000110 | SAR | Rotate/shift |
| 0000111 | SAL | Rotate/shift |
| 0001000 | ADD | Arithmetic |
| 0001001 | ADDX | Arithmetic |
| 0001010 | ADDS | Arithmetic |
| 0001011 | ADDSX | Arithmetic |
| 0001100 | SUB | Arithmetic |
| 0001101 | SUBX | Arithmetic |
| 0001110 | SUBS | Arithmetic |
| 0001111 | SUBSX | Arithmetic |

### Comparison and Logic (0010000-0011111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 0010000 | CMP | Comparison |
| 0010001 | CMPX | Comparison |
| 0010010 | CMPS | Comparison |
| 0010011 | CMPSX | Comparison |
| 0010100 | CMPR | Comparison |
| 0010101 | CMPM | Comparison |
| 0010110 | SUBR | Arithmetic |
| 0010111 | CMPSUB | Comparison |
| 0011000 | FGE | Min/max |
| 0011001 | FLE | Min/max |
| 0011010 | FGES | Min/max |
| 0011011 | FLES | Min/max |
| 0011100 | SUMC | Summation |
| 0011101 | SUMNC | Summation |
| 0011110 | SUMZ | Summation |
| 0011111 | SUMNZ | Summation |

### Bit Operations (0100000-0101111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 0100000 | TESTB | Bit test |
| 0100001 | TESTBN | Bit test |
| 0100010-0100011 | Reserved | - |
| 0100100 | BITL | Bit write |
| 0100101 | BITH | Bit write |
| 0100110 | BITC | Bit write |
| 0100111 | BITNC | Bit write |
| 0101000 | BITZ | Bit write |
| 0101001 | BITNZ | Bit write |
| 0101010 | BITRND | Bit write |
| 0101011 | BITNOT | Bit write |
| 0101100 | AND | Logic |
| 0101101 | ANDN | Logic |
| 0101110 | OR | Logic |
| 0101111 | XOR | Logic |

### Move and Multiply (0110000-0111111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 0110000 | MUXC | Multiplex |
| 0110001 | MUXNC | Multiplex |
| 0110010 | MUXZ | Multiplex |
| 0110011 | MUXNZ | Multiplex |
| 0110100 | MOV | Data movement |
| 0110101 | NOT | Logic |
| 0110110 | ABS | Arithmetic |
| 0110111 | NEG | Arithmetic |
| 0111000 | NEGC | Arithmetic |
| 0111001 | NEGNC | Arithmetic |
| 0111010 | NEGZ | Arithmetic |
| 0111011 | NEGNZ | Arithmetic |
| 0111100 | INCMOD | Modulo |
| 0111101 | DECMOD | Modulo |
| 0111110 | ZEROX | Bit field |
| 0111111 | SIGNX | Bit field |

### Extended Math (1000000-1001111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1000000 | ENCOD | Encoding |
| 1000001 | ONES | Bit counting |
| 1000010 | TEST | Testing |
| 1000011 | TESTN | Testing |
| 1000100 | SETNIB | Nibble/byte |
| 1000101 | GETNIB | Nibble/byte |
| 1000110 | ROLNIB | Nibble/byte |
| 1000111 | SETBYTE | Nibble/byte |
| 1001000 | GETBYTE | Nibble/byte |
| 1001001 | ROLBYTE | Nibble/byte |
| 1001010 | SETWORD | Word operations |
| 1001011 | GETWORD | Word operations |
| 1001100 | ROLWORD | Word operations |
| 1001101 | ALTSN | Indirection |
| 1001110 | ALTGN | Indirection |
| 1001111 | ALTSB | Indirection |

### Memory and Multiply (1010000-1011111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1010000 | ALTGB | Indirection |
| 1010001 | ALTSW | Indirection |
| 1010010 | ALTGW | Indirection |
| 1010011 | ALTR | Indirection |
| 1010100 | ALTD | Indirection |
| 1010101 | ALTS | Indirection |
| 1010110 | ALTB | Indirection |
| 1010111 | ALTI | Indirection |
| 1011000 | SETR | Register control |
| 1011001 | SETD | Register control |
| 1011010 | SETS | Register control |
| 1011011 | DECOD | Decoding |
| 1011100 | BMASK | Bit mask |
| 1011101 | CRCBIT | CRC |
| 1011110 | CRCNIB | CRC |
| 1011111 | MUXNITS | Multiplex |

### Multiply Operations (1100000-1100111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1100000 | MUXNIBS | Multiplex |
| 1100001 | MUXQ | Multiplex |
| 1100010 | MOVBYTS | Data movement |
| 1100011 | MUL | Multiply (U×U) |
| 1100100 | MULS | Multiply (S×S) |
| 1100101 | SCA | Multiply (U×U, scaled) |
| 1100110 | SCAS | Multiply (S×S, scaled) |
| 1100111 | ADDPIX | Pixel operations |

### Control Flow (1101000-1101111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1101000 | MULPIX | Pixel operations |
| 1101001 | BLNPIX | Pixel operations |
| 1101010 | MIXPIX | Pixel operations |
| 1101011 | ADDCT1 | Event control |
| 1101100 | ADDCT2 | Event control |
| 1101101 | ADDCT3 | Event control |
| 1101110 | WMLONG | Hub write |
| 1101111 | RQPIN | Smart Pins |

### Hub and Special (1110000-1111111)

| Opcode | Instruction | Category |
|--------|-------------|----------|
| 1110000 | RDPIN | Smart Pins |
| 1110001 | RDLUT | LUT read |
| 1110010 | RDBYTE | Hub read |
| 1110011 | RDWORD | Hub read |
| 1110100 | RDLONG | Hub read |
| 1110101 | CALLD | Call/return |
| 1110110-1110111 | Reserved | - |
| 1111000 | CALLPA | Call with parameter |
| 1111001 | CALLPB | Call with parameter |
| 1111010 | DJZ | Loop control |
| 1111011 | DJNZ | Loop control |
| 1111100 | DJF | Loop control |
| 1111101 | DJNF | Loop control |
| 1111110 | IJZ | Loop control |
| 1111111 | IJNZ | Loop control |

*Note: This is a representative subset. Complete opcode tables appear in Appendix A.*

## Special Encoding Forms

### AUGS/AUGD (Immediate Extension)

When immediate values exceed 9 bits, AUGS and AUGD instructions extend the next instruction's operands:

**AUGS Format:**
```
1111_000x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx

Effect: Next instruction's S field becomes 23 bits:
  Bits 31:9 from AUGS (x bits)
  Bits 8:0 from instruction S field
```

**AUGD Format:**
```
1111_100x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx

Effect: Next instruction's D field becomes 23 bits:
  Bits 31:9 from AUGD (x bits)
  Bits 8:0 from instruction D field
```

**Example:**
```
AUGS    #$1234      ' Bits 31:9 = $1234
MOV     result, #$56 ' S = $1234_056 = $2468AC
```

### NOP Encoding

NOP is encoded as all zeros, which decodes as:
```
0000_0000_000_000000000_000000000
= IF_ALWAYS ROR $000, $000
```

This performs a useless rotate with no effect.

### Hub Instruction Extensions

Some hub instructions use extended encoding:

**WRLONG D, #\S (WC, WZ, WCZ):**
- Uses special OOOOOOO values to indicate hub write variants
- Additional mode bits in S field select FIFO vs direct addressing

**RDXXXX/WRXXXX with PTRx:**
- Uses PTRA/PTRB selection bit
- Auto-increment/decrement encoding
- Index register selection

See Appendix A for complete hub instruction encoding details.

## Encoding Examples

### Example 1: ADD D, #5

```
ADD     result, #5      ' Add immediate 5 to result

Encoding breakdown:
  Condition: 0000 (IF_ALWAYS - unconditional)
  Opcode: 0001000 (ADD operation)
  CZI: 001 (no WC, no WZ, immediate mode)
  D: [9-bit register address of 'result']
  S: 000000101 (immediate value 5)

32-bit pattern:
  0000_0001000_001_DDDDDDDDD_000000101
  ││││ │││││││ │││ ││││││││││ │││││││││
  ││││ │││││││ │││ └────┬────┘ └───┬───┘
  ││││ │││││││ │││      │          └─ S = 5
  ││││ │││││││ │││      └─ D = result address
  ││││ │││││││ └┴┴─ I=1, Z=0, C=0
  ││││ └─────┴─ ADD opcode
  └──┴─ IF_ALWAYS
```

### Example 2: IF_Z MOV D, S WC

```
  IF_Z    MOV     dest, source    WC

Encoding breakdown:
  Condition: 1010 (IF_Z - execute only if Z=1)
  Opcode: 0110100 (MOV operation)
  CZI: 100 (WC=yes, WZ=no, register mode)
  D: [9-bit register address of 'dest']
  S: [9-bit register address of 'source']

32-bit pattern:
  1010_0110100_100_DDDDDDDDD_SSSSSSSSS
  ││││ │││││││ │││ ││││││││││ │││││││││
  ││││ │││││││ │││ └────┬────┘ └───┬───┘
  ││││ │││││││ │││      │          └─ S = source address
  ││││ │││││││ │││      └─ D = dest address
  ││││ │││││││ └┴┴─ I=0, Z=0, C=1 (WC)
  ││││ └─────┴─ MOV opcode
  └──┴─ IF_Z
```

### Example 3: DJNZ loop, #label WC

```
DJNZ    counter, #target    WC

Encoding breakdown:
  Condition: 0000 (IF_ALWAYS)
  Opcode: 1111011 (DJNZ operation)
  CZI: 101 (WC=yes, WZ=no, immediate mode)
  D: [9-bit register address of 'counter']
  S: [9-bit relative branch offset]

Notes:
  - S field contains signed relative offset
  - Offset is from next instruction PC
  - WC sets C flag based on counter=0 after decrement
  - D register decremented before branch decision

32-bit pattern:
  0000_1111011_101_DDDDDDDDD_SSSSSSSSS
```

### Example 4: CALLD return_reg, #subroutine WC, WZ

```
CALLD   return_addr, #subroutine    WC, WZ

Encoding breakdown:
  Condition: 0000 (IF_ALWAYS)
  Opcode: 1110101 (CALLD operation)
  CZI: 111 (WC=yes, WZ=yes, immediate mode)
  D: [9-bit register address for return address]
  S: [9-bit absolute branch target]

Effect:
  - D ← PC+1 (return address)
  - PC ← S (jump to subroutine)
  - Flags updated based on operation
```

### Example 5: Extended Immediate with AUGS

```
MOV     result, ##$12345678

Assembler generates two instructions:

1) AUGS #$12345678 >> 9:
   1111_000_[23-bit value = $91A2B]
   Provides bits 31:9 = $91A2B

2) MOV result, #$12345678 & $1FF:
   0000_0110100_001_[result]_078
   Uses bits 8:0 = $078

Combined: result ← $91A2B_078 = $12345678
```

## Decoding Process

To decode a 32-bit instruction word:

1. **Extract condition field** (bits 31:28)
   - Check against C and Z flags
   - Skip instruction if condition false

2. **Extract opcode** (bits 27:21)
   - Lookup instruction mnemonic
   - Determine operation category

3. **Extract CZI field** (bits 23:21)
   - Determine immediate vs register mode
   - Identify which flags will be updated

4. **Extract D field** (bits 18:9)
   - Decode destination register address
   - May be modified by prior AUGD

5. **Extract S field** (bits 8:0)
   - If I=1: immediate value (possibly extended by AUGS)
   - If I=0: source register address

6. **Execute instruction**
   - Perform opcode operation
   - Write result to D register
   - Update flags per CZI setting

## Special Register Encoding

The special register range ($1F0-$1FF) uses specific D/S field values:

| Address | Register | Purpose |
|---------|----------|---------|
| $1F0 | IJMP3 | Interrupt jump 3 |
| $1F1 | IRET3 | Interrupt return 3 |
| $1F2 | IJMP2 | Interrupt jump 2 |
| $1F3 | IRET2 | Interrupt return 2 |
| $1F4 | IJMP1 | Interrupt jump 1 |
| $1F5 | IRET1 | Interrupt return 1 |
| $1F6 | PA | Pin A control |
| $1F7 | PB | Pin B control |
| $1F8 | PTRA | Hub pointer A |
| $1F9 | PTRB | Hub pointer B |
| $1FA | DIRA | Pin direction A |
| $1FB | DIRB | Pin direction B |
| $1FC | OUTA | Pin output A |
| $1FD | OUTB | Pin output B |
| $1FE | INA | Pin input A |
| $1FF | INB | Pin input B |

Reading these addresses accesses hardware registers. Writing to some (like INA/INB) has no effect.

## Bit Field Summary

Quick reference for manual instruction encoding:

| Field | Bits | Width | Purpose |
|-------|------|-------|---------|
| Condition (EEEE) | 31:28 | 4 | Execution condition |
| Opcode (OOOOOOO) | 27:21 | 7 | Instruction operation |
| C flag write | 23 | 1 | Update C if set |
| Z flag write | 22 | 1 | Update Z if set |
| Immediate mode | 21 | 1 | S is immediate if set |
| Destination (D) | 18:9 | 9 | Register address |
| Source (S) | 8:0 | 9 | Register or immediate |

**Total:** 32 bits (4 + 7 + 3 + 9 + 9)

## Notes

- **Instruction alignment:** All instructions are 32-bit aligned in COG/LUT memory
- **Execution time:** Most instructions execute in 2 clock cycles
- **Hub instructions:** RDLONG/WRLONG may take additional cycles for hub access
- **SKIPF pattern:** Uses special encoding for multi-instruction skip patterns
- **Reserved opcodes:** Some opcode values are reserved for future use

For complete instruction encoding details, see **Appendix A: Instruction Set Reference**.

For instruction timing and pipeline behavior, see **Chapter 4: Instruction Execution**.

For condition code usage patterns, see **Chapter 6: Control Flow**.
