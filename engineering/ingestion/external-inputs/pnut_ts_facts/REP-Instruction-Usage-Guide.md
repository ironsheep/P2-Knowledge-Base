# REP Instruction Usage Guide

## Overview

The `REP` (Repeat) instruction is a PASM2 directive that repeats a block of instructions a specified number of times without requiring explicit branch instructions. The loop executes with no branch instruction overhead per iteration.

## Syntax

The REP instruction supports two syntax forms:

```pasm2
REP  @label, S/#      ' Block size determined by label distance
REP  D/#, S/#         ' Explicit instruction count
```

Where:
- **D** - Destination: instruction count (0-511)
- **S** - Source: repetition count (register or immediate)
- **@label** - Forward label marking the end of the block

## Instruction Encoding

```
Format: EEEE_OOOOOOOO_DI_SI_DDDDDDDDD_SSSSSSSSS

Bits 31:28 (E)  - Execution condition (IF_ALWAYS, IF_C, etc.)
Bits 27:20      - Base opcode: 11001101
Bit  19    (DI) - D-immediate flag: set when D is #immediate or @label
Bit  18    (SI) - S-immediate flag: set when S is #immediate
Bits 17:9  (D)  - Instruction count (0-511 in 9-bit field)
Bits 8:0   (S)  - Repetition count (0-511 in 9-bit field, or register address)
```

**Note:** REP does not support WC/WZ/WCZ effects (allowedEffects = 0b00). Bits 20:19, which serve as effect flags for other instructions, function as addressing mode flags for REP.

## @label Form Details

When using the `@label` form, the compiler:
1. Sets bit 19 (DI bit) to indicate label-based addressing
2. Calculates instruction count from label distance
3. Validates alignment (must be long-aligned)
4. Validates range (0-511 instructions)

The instruction count calculation differs by execution mode:

**COG Mode (ORG):**
```
byteOffset = (labelAddress << 2) - cogOrg
instructionCount = (byteOffset >> 2) - 1
```

**HUB Mode (ORGH):**
```
byteOffset = labelAddress - hubOrg
instructionCount = (byteOffset >> 2) - 1
```

In both cases, the final `instructionCount` must be 0-511 (9-bit field).

## Constraints

### Block Size (D field) - Instruction Count
The D field specifies how many instructions to repeat:

| Form | Compiler Behavior | Compiler Limit |
|------|-------------------|----------------|
| `@label` | Calculates distance, validates range | 0-511 (error if exceeded) |
| `#count` | Validates via `tryValueCon()` | 0-511 (error: "Constant must be from 0 to 511") |
| `##count` | Emits AUGD prefix, stores lower 9 bits in D field | 0 to 2^32-1 |
| `register` | Stores register address in D field | Register address 0-511; register value 0 to 2^32-1 |

**Memory Configuration Limits:**

| Memory Mode | Address Range | Memory Size | @label Max (compiler-enforced) |
|-------------|---------------|-------------|-------------------------------|
| COGRAM only | $000-$1FF | 512 longs (2KB) | min(511, available longs from current address to $1FF) |
| COGRAM + LUTRAM | $000-$3FF | 1024 longs (4KB) | min(511, available longs from current address to $3FF) |
| LUTRAM only | $200-$3FF | 512 longs (2KB) | min(511, available longs from current address to $3FF) |
| HUBRAM | $00000-$7FFFF | 512KB (131,072 longs) | 511 instructions (9-bit field limit) |

For `@label` form, the compiler enforces that the calculated instruction count fits in the 9-bit D field (0-511). The available memory determines the upper bound of where the end label can be placed.

**End Label (@label) Position Constraints:**

The compiler validates that the `@label` end point satisfies both constraints:
1. The calculated instruction count must be 0-511 (9-bit D field)
2. The label must be within the valid address range for the execution mode

| Memory | Address Range | Memory Size | Constraints |
|--------|---------------|-------------|-------------|
| COGRAM only | $000-$1FF | 512 longs (2KB) | Label must be at or before $1FF AND within 511 instructions |
| COGRAM + LUTRAM | $000-$3FF | 1024 longs (4KB) | Label must be at or before $3FF AND within 511 instructions |
| LUTRAM only | $200-$3FF | 512 longs (2KB) | Label must be at or before $3FF AND within 511 instructions |
| HUBRAM | $00000-$7FFFF | 512KB | Label must be within 511 instructions of REP |

**COG Execution Mode (ORG) - COGRAM Only:**
- End label must be within COGRAM ($000-$1FF)
- If REP is at $000, max end label is $1FF (511 instructions)
- If REP is at $100, max end label is $1FF (only 255 instructions due to cog boundary)
- The constraint is: `min(511 instructions, $1FF - current_address)`

**COG + LUT Execution Mode (ORG with SETQ+EXECF or similar):**
- Code can span COGRAM ($000-$1FF) and LUTRAM ($200-$3FF)
- End label must be within combined space ($000-$3FF)
- If REP is at $000, max end label is $1FF (511 instructions - encoding limit reached first)
- If REP is at $100, max end label is $2FF (511 instructions - encoding limit)
- If REP is at $200 (in LUT), max end label is $3FF (only 511 instructions available anyway)
- The constraint is: `min(511 instructions, $3FF - current_address)`

**LUT Execution Mode (code in LUTRAM only):**
- End label must be within LUTRAM ($200-$3FF)
- If REP is at $200, max end label is $3FF (511 instructions, but only 512 longs available)
- The constraint is: `min(511 instructions, $3FF - current_address)`

**HUB Execution Mode (ORGH):**
- End label can be anywhere in HUBRAM
- Distance from REP to end label is always limited to 511 instructions (9-bit encoding)
- Memory size is not the constraint; the encoding is

**Examples:**
```pasm2
' COG mode near boundary
                org     $1F0              ' Near end of cog
                rep     @.end, #10        ' ERROR if .end would be past $1FF
                add     sum, #1
                ...                       ' Only ~15 instructions available
.end                                      ' Must be at or before $1FF

' COG+LUT mode - REP can span into LUT
                org     $1F0              ' Near end of cog
                rep     @.end, #32        ' OK - .end can be in LUT ($200+)
                add     sum, #1
                ...                       ' Block continues into LUTRAM
.end                                      ' Can be up to $3FF (if within 511 instructions)
```

### Repetition Count (S field) - Iteration Count
The S field specifies how many times to repeat the block:

| Form | Compiler Behavior | Compiler Limit |
|------|-------------------|----------------|
| `#count` | Validates via `tryValueCon()` | 0-511 (error: "Constant must be from 0 to 511") |
| `##count` | Emits AUGS prefix, stores lower 9 bits in S field | 0 to 2^32-1 |
| `register` | Stores register address in S field | Register address 0-511; register value 0 to 2^32-1 |

The repetition count is independent of memory configuration - it specifies the number of loop iterations.

**Examples:**
```pasm2
                rep     @.end, #511       ' 511 iterations (max for single # immediate)
                rep     @.end, ##1000     ' 1000 iterations (AUGS prefix emitted)
                rep     @.end, counter    ' Iterations determined by register value at runtime
```

### Alignment
- Block end must be long-aligned (byte offset & 0b11 == 0)
- In COG mode, this is inherently satisfied since COG addresses are long-aligned
- In HUB mode, the compiler validates that the end label is at a 4-byte boundary

### Effects Not Allowed
- REP cannot use WC, WZ, or WCZ effects
- Allowed effects value: 0b00

### Nesting Restrictions

**CRITICAL: REP instructions cannot be nested.**

The P2 hardware uses a single internal counter for REP execution. Starting a new REP while one is active will overwrite the existing repeat state. The compiler does not enforce this restriction - it is a hardware limitation.

**Invalid (will not work as expected):**
```pasm2
' DO NOT DO THIS - nesting is not supported
                rep     @.outer_end, #10      ' Outer loop
                rep     @.inner_end, #5       ' OVERWRITES outer REP!
                add     sum, #1
.inner_end
                add     counter, #1
.outer_end
```

For nested loops, use branch-based loops for the outer loop:
```pasm2
' Alternative using branch for outer loop
                mov     outer_count, #10
.outer_loop     rep     @.inner_end, #5       ' Inner REP is fine
                add     sum, #1
.inner_end
                add     counter, #1
                djnz    outer_count, #.outer_loop   ' Branch for outer
```

## Usage Examples

### Basic Repetition with Label

```pasm2
' Repeat 3 instructions, 5 times
                rep     @.end, #5
                add     sum, #1
                sub     counter, #1
                nop
.end
```

### Basic Repetition with Explicit Count

```pasm2
' Repeat 8 instructions, 9 times
                rep     #8, #9
                testp   sda                   wc
    if_c        jmp     #.done
                drvl    scl
                waitx   tix
                waitx   tix
                drvh    scl
                waitx   tix
                waitx   tix
.done
```

### Repetition with Register Count

```pasm2
' Count from register
                mov     counter, #8
                rep     @.end, counter
                add     sum, #2
.end
```

### Interrupt Stalling Behavior

REP stalls interrupt handling until all repeated instructions complete. This behavior is used internally by the Spin2 interpreter to protect CORDIC operations.

**Spin2 vs PASM2 CORDIC Operations:**

| Context | CORDIC Protection | User Action Required |
|---------|-------------------|---------------------|
| Spin2 operators (SQRT, QLOG, QEXP, SCA, SCAS, FRAC, etc.) | Built into interpreter | None - interpreter uses REP internally |
| PASM2 instructions (QMUL, QDIV, QSQRT, QROTATE, etc.) | User's responsibility | Only if interrupts are enabled |

**Spin2 Interpreter Implementation:**

The Spin2 interpreter (`src/ext/Spin2_interpreter.spin2`) uses REP to protect its internal CORDIC operations:

```pasm2
' From Spin2 interpreter - protects CORDIC until ret/_ret_
op_quna         rep     #99, #1
                qsqrt   x, #0
                qlog    x
                qexp    x
                ...
        _ret_   mov     result, x
```

This pattern uses a large instruction count (99) with repetition count of 1, creating an interrupt-free zone that terminates at the first `ret`, `_ret_`, or branch instruction.

**PASM2 User Code:**

When writing PASM2 code that uses CORDIC instructions directly (QMUL, QDIV, QFRAC, QSQRT, QROTATE, QLOG, QEXP) with interrupts enabled, the user may need to implement similar protection:

```pasm2
' PASM2 user code - only needed if interrupts are enabled
                rep     @.done, #1
                qmul    y, x              ' CORDIC multiply
                getqx   x                 ' Get result
                getqy   y                 ' Get overflow
.done
```

### Array Operations

```pasm2
' Fill array with incrementing values
                mov     counter, #0
                loc     ptra, #\hub_array
                rep     @.arr_end, #8
                add     counter, #1
                wrlong  counter, ptra++
.arr_end
```

### Bit-Bang I2C Pattern

```pasm2
' Output 8 bits, MSB first
.wr_byte        rep     #8, #8
                shl     data, #1          wc
                drvc    sda
                drvh    scl
                waitx   delay
                drvl    scl
                waitx   delay
                nop
                nop
```

### Zero Count Behavior

When the repetition count (S) is 0, the block executes 0 times (skipped entirely):

```pasm2
                mov     counter, #0
                rep     @.end, counter    ' Block will not execute
                add     sum, #100         ' Skipped
.end
```

## Conditional Execution

REP can be conditionally executed:

```pasm2
                testp   pin               wc
    if_c        rep     @.end, #5         ' Only repeat if C set
                add     sum, #1
.end
```

Instructions within the REP block can also be conditional:

```pasm2
                rep     @.end, #4
                add     sum, #1
                test    sum, #1           wz
    if_z        add     result, #1        ' Conditional within block
.end
```

## Error Messages

The compiler generates these errors for REP:

| Error | Cause | Solution |
|-------|-------|----------|
| `REP block end is out of alignment` | Label address not long-aligned in hub mode | Ensure label is at a long boundary |
| `REP block end is out of range` | Block exceeds 511 instructions | Reduce block size or restructure code |

## Inline PASM Usage

REP works within inline PASM blocks:

```spin2
PUB ReadByte() : value
  ORG
                rep     #8, #9
                testp   sda               wc
    if_c        jmp     #.done
                drvl    scl
                waitx   tix
                waitx   tix
                drvh    scl
                waitx   tix
                waitx   tix
.done
  END
```

## Behavioral Characteristics

1. **Loop overhead**: REP executes with no branch instruction per iteration
2. **Interrupt handling**: Interrupts are stalled during REP block execution
3. **Nesting**: REP uses a single hardware counter; nested REP overwrites the outer REP state
4. **Atomic execution**: The entire REP block executes without interruption

## Comparison with Branch Loops

| Aspect | REP | DJNZ Loop |
|--------|-----|-----------|
| Branch overhead | None | 1 instruction per iteration |
| Nesting | Single level (hardware counter) | Multiple levels supported |
| Interrupts | Stalled during block | Handled between instructions |
| Max iterations (`#`) | 511 | Register-limited |
| Max iterations (`##`/register) | 2^32-1 | Register-limited |
| Max block size (`@label`/`#`) | 511 instructions | No limit |
| Max block size (`##`/register) | 2^32-1 | No limit |

## Implementation Notes

### Compiler Source References

The REP instruction is implemented in:
- `src/classes/parseUtils.ts:1416` - Opcode definition
- `src/classes/spinResolver.ts:2044-2078` - Operand handling
- `src/classes/types.ts:331` - operand_rep value type

### Opcode Details

```typescript
// From parseUtils.ts
ac_rep: opcode=0b110011010, allowedEffects=0b00, operandType=operand_rep
```

## See Also

- [PASM2-Authoring-Guide.md](PASM2-Authoring-Guide.md) - General PASM2 guidance
- [Inline-PASM-Usage-Guide.md](Inline-PASM-Usage-Guide.md) - Using REP in inline PASM
