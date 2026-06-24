# Chapter 6: Address Modes

<!-- Chapter covering all operand addressing modes in PASM2 -->

PASM2 provides several addressing modes that determine how instruction operands are specified and how memory is accessed. Understanding these modes is essential for writing efficient code that accesses registers, immediate values, and hub memory correctly.

This chapter covers all addressing modes from simple register access through the pointer expressions used for hub memory operations. Each mode has specific use cases, encoding requirements, and performance characteristics.


## 6.1 Direct Register Addressing

The most basic addressing mode specifies cog registers directly by address. Both source and destination operands can use direct register addressing.

### 6.1.1 Register as Destination

The destination field (D) in every instruction specifies a 9-bit cog register address ($000-$1FF). The instruction reads from and/or writes to this register:

```pasm2
        add     result, value           ' result is destination register
        mov     counter, #0             ' counter is destination register
        test    flags, #MASK    wz      ' flags is destination (read here)
```

The assembler translates symbolic register names to their addresses. Programmers define registers using labels or the RES directive:

```pasm2
result          res     1               ' Reserve one long here
counter         res     1
flags           res     1
```

### 6.1.2 Register as Source

When the I bit (bit 18) is clear, the source field (S) specifies a register address. The instruction reads the value from that register:

```pasm2
        add     x, y                    ' y is source register (I=0)
        mov     dest, source            ' source is register (I=0)
        cmp     a, b            wc      ' b is source register (I=0)
```

Direct register addressing provides single-cycle access to cog RAM. Both operands are read simultaneously during instruction execution, making register-to-register operations the fastest possible.

### 6.1.3 Special Register Addresses

Addresses $1F0-$1FF access special-purpose registers with hardware functions:

| Address | Register | Purpose |
|:--------|:---------|:--------|
| $1F0-$1F7 | IJMP3/IRET3 through PA/PB | Interrupt and scratch registers |
| $1F8 | PTRA | Pointer A for Hub addressing |
| $1F9 | PTRB | Pointer B for Hub addressing |
| $1FA-$1FB | DIRA/DIRB | Pin direction control |
| $1FC-$1FD | OUTA/OUTB | Pin output control |
| $1FE-$1FF | INA/INB | Pin input (read-only) |

These registers function like ordinary registers for most purposes but have additional hardware significance.


## 6.2 Immediate Addressing

Immediate addressing embeds a constant value directly in the instruction rather than reading from a register.

### 6.2.1 The # Prefix (9-bit Immediate)

The `#` prefix before an operand indicates an immediate value:

```pasm2
        add     x, #100                 ' Add immediate value 100
        mov     counter, #0             ' Load zero
        cmp     value, #255     wc      ' Compare against 255
```

When `#` is used:

- The assembler sets the I bit (bit 18) to 1
- The 9-bit S field contains the immediate value
- Valid range: 0 to 511 ($000 to $1FF)

### 6.2.2 Immediate Range and Signedness

For data instructions the 9-bit immediate field is always zero-extended and treated as unsigned (0-511). Sign-extension of the 9-bit immediate applies only to relative-branch instructions, where the immediate is a signed offset in the range -256..+255:

```pasm2
        mov     x, #$1FF                ' x = 511 (9-bit, zero-extended)
        add     x, #1                   ' Add 1
        sub     x, #10                  ' Subtract 10
```

For relative branches, the same 9-bit immediate is interpreted as a signed offset:

```pasm2
        jmp     #$-1                    ' Relative branch back 1 (signed)
```

Values outside the 0-511 range require augmentation (see Section 6.3).

### 6.2.3 Current Address ($)

The `$` symbol represents the current assembly address:

```pasm2
loop    add     counter, #1
        djnz    count, #$-1             ' Jump back one instruction (to ADD)
        jmp     #$                      ' Infinite loop (jump to self)
```

When used with `#`, it becomes an immediate value representing the address. This is useful for relative branches and self-referencing code.


## 6.3 Augmented Immediate Addressing

When values exceed 9 bits, PASM2 uses augmentation to provide full 32-bit immediates.

### 6.3.1 The ## Prefix (32-bit Immediate)

The `##` prefix indicates a full 32-bit immediate value:

```pasm2
        mov     dest, ##$12345678       ' Load full 32-bit value
        add     counter, ##1000000      ' Add one million
        mov     ptr, ##hub_buffer       ' Load 20-bit Hub address
```

### 6.3.2 How Augmentation Works

The assembler implements `##` by inserting an AUGS or AUGD instruction before the target instruction:

```pasm2
' What the programmer writes:
        mov     dest, ##$12345678

' What the assembler generates:
        augs    #$12345678              ' Provides upper 23 bits [31:9]
        mov     dest, #$078             ' Provides lower 9 bits: $078
                                        ' Combined result: $12345678
```

The AUG instruction provides bits 31-9, which combine with the 9-bit field from the next instruction to form the complete 32-bit value.

### 6.3.3 AUGS vs. AUGD

Two augmentation instructions exist:

- **AUGS** augments the Source field of the following instruction
- **AUGD** augments the Destination field of the following instruction

Both operands can be augmented simultaneously:

```pasm2
' What the programmer writes:
        wrlong  ##value, ##address      ' Both operands augmented

' What the assembler generates:
        augd    #value_upper            ' Augment D field
        augs    #address_upper          ' Augment S field
        wrlong  #value_lower, #address_lower
```

### 6.3.4 Augmentation Timing

Each AUG instruction adds **+2 clock cycles** to execution:

| Augmentation | Additional Cycles |
|:-------------|:------------------|
| `##Src` only | +2 cycles (AUGS) |
| `##Dest` only | +2 cycles (AUGD) |
| `##Dest, ##Src` | +4 cycles (AUGD + AUGS) |

```pasm2
        mov     x, #100                 ' 2 cycles
        mov     x, ##100000             ' 4 cycles (2 + 2 for AUGS)
        wrlong  ##data, ##addr          ' 6+ cycles (2+2+2: AUGD+AUGS+instr)
```

**Performance Note:** In time-critical code, large constants should be loaded into registers once and reused, rather than using `##` repeatedly inside loops.

### 6.3.5 Augmentation is One-Shot

The augmented value applies only to the immediately following instruction. If any instruction intervenes (including a conditional instruction that doesn't execute), the augmentation is consumed:

```pasm2
        augs    #$12345678
        nop                             ' This consumes the AUGS!
        mov     x, #$078                ' Gets only $078, NOT $12345678

        augs    #$12345678
        if_z    mov     x, #$078        ' Even if Z=0, MOV skipped,
                                        '  AUGS is still consumed
```

The assembler handles this automatically when `##` notation is used. Manual AUGS/AUGD usage requires careful attention to instruction sequencing.


## 6.4 Pointer Register Addressing (PTRA/PTRB)

The P2 provides two dedicated pointer registers—PTRA ($1F8) and PTRB ($1F9)—that enable hub memory addressing with automatic increment, decrement, and indexing.

### 6.4.1 Basic Pointer Access

The simplest pointer usage reads or writes hub memory at the address in PTRA or PTRB:

```pasm2
        mov     ptra, ##hub_buffer      ' Set PTRA to Hub address
        rdbyte  x, ptra                 ' Read byte from Hub at PTRA
        wrlong  y, ptrb                 ' Write long to Hub at PTRB
```

### 6.4.2 The SCALE Factor

**Critical Concept:** Pointer operations are scaled by the instruction's data size:

| Instruction | SCALE | Description |
|:------------|:------|:------------|
| RDBYTE, WRBYTE | 1 | Byte operations |
| RDWORD, WRWORD | 2 | Word (16-bit) operations |
| RDLONG, WRLONG, WMLONG | 4 | Long (32-bit) operations |

All pointer increments, decrements, and index offsets are multiplied by SCALE. This means:

- `RDBYTE x, PTRA++` increments PTRA by **1 byte**
- `RDWORD x, PTRA++` increments PTRA by **2 bytes**
- `RDLONG x, PTRA++` increments PTRA by **4 bytes**

This automatic scaling makes sequential memory access natural—each operation advances to the next element regardless of element size.

### 6.4.3 Post-Increment and Post-Decrement

Post-modify modes use the current pointer value for the memory access, then update the pointer afterward:

```pasm2
        rdbyte  x, ptra++               ' Read byte at PTRA, then PTRA += 1
        rdword  y, ptrb++               ' Read word at PTRB, then PTRB += 2
        rdlong  z, ptra--               ' Read long at PTRA, then PTRA -= 4
        wrbyte  x, ptrb--               ' Write byte at PTRB, then PTRB -= 1
```

**Execution sequence for `RDLONG x, PTRA++`:**
1. Read long from hub address in PTRA
2. Store value in register x
3. Add 4 (SCALE for long) to PTRA

Post-modify is ideal for sequential forward or backward traversal:

```pasm2
' Read 10 bytes sequentially
        mov     ptra, ##source
        rep     @.end, #10
        rdbyte  x, ptra++               ' Read byte, advance pointer
        ' ... process x ...
.end

' Write longs in reverse order
        mov     ptrb, ##buffer_end
        rep     @.done, #count
        wrlong  value, ptrb--           ' Write long, move backward
.done
```

### 6.4.4 Pre-Increment and Pre-Decrement

Pre-modify modes update the pointer first, then use the new value for memory access:

```pasm2
        rdbyte  x, ++ptra               ' PTRA += 1, then read byte there
        rdword  y, ++ptrb               ' PTRB += 2, then read word there
        rdlong  z, --ptra               ' PTRA -= 4, then read long there
        wrbyte  x, --ptrb               ' PTRB -= 1, then write byte
```

**Execution sequence for `RDLONG x, ++PTRA`:**
1. Add 4 (SCALE for long) to PTRA
2. Read long from hub address in updated PTRA
3. Store value in register x

Pre-modify is useful for stack operations and accessing elements relative to a base:

```pasm2
' Push onto stack (stack grows upward)
        wrlong  value, ptra++           ' Post: write here, then advance

' Pop from stack
        rdlong  value, --ptra           ' Pre: back up first, then read

' Skip first element, read second
        mov     ptra, ##array
        rdlong  x, ++ptra               ' Skip element 0, read element 1
```

### 6.4.5 Indexed Pointer Access (Non-Updating)

Indexed mode accesses memory at an offset from the pointer without modifying the pointer:

```pasm2
        rdlong  x, ptra[0]              ' Read at PTRA + 0*4 = PTRA
        rdlong  y, ptra[5]              ' Read at PTRA + 5*4 = +20 bytes
        rdbyte  z, ptrb[-3]             ' Read at PTRB - 3 bytes
        wrword  w, ptra[10]             ' Write at PTRA + 20 bytes
```

The index is multiplied by SCALE:

| Expression | Instruction | Effective Address |
|:-----------|:------------|:------------------|
| `PTRA[5]` | RDBYTE | PTRA + 5 bytes |
| `PTRA[5]` | RDWORD | PTRA + 10 bytes |
| `PTRA[5]` | RDLONG | PTRA + 20 bytes |

**Index Range (non-updating):** -32 to +31 (6-bit signed)

Indexed mode is ideal for accessing structure fields or array elements:

```pasm2
' Access structure fields
        mov     ptra, ##my_struct
        rdlong  id, ptra[0]             ' First field (offset 0)
        rdlong  flags, ptra[1]          ' Second field (offset 4)
        rdlong  data, ptra[2]           ' Third field (offset 8)

' Access array element
        mov     ptra, ##long_array
        rdlong  x, ptra[index]          ' Read array[index]
```

### 6.4.6 Indexed Pointer with Update (Compound Forms)

Compound forms combine indexing with pointer update:

```pasm2
        rdlong  x, ptra++[5]            ' Read at PTRA, then PTRA += 20
        rdlong  y, ptra--[3]            ' Read at PTRA, then PTRA -= 12
        rdlong  z, ++ptra[5]            ' PTRA += 5*4, then read at new PTRA
        rdlong  w, --ptra[3]            ' PTRA -= 3*4, then read at new PTRA
```

**Index Range (updating):** -16 to +16 (positive 1-16 for `++`/`++[]`, negative -16 to -1 for `--`/`--[]`; value 16 encoded as 0)

These forms enable strided access patterns:

```pasm2
' Read every 4th long (stride of 16 bytes)
        mov     ptra, ##data
        rep     @.end, #count
        rdlong  x, ptra++[4]            ' Read, advance by 4 longs
        ' ... process x ...
.end

' Read structure array (12-byte structures as 3 longs)
        mov     ptra, ##struct_array
.loop   rdlong  field1, ptra++[3]       ' Read field1, skip to next struct
        ' ... (to read all fields, use indexed without update
        '      for field2, field3)
```

### 6.4.7 Complete PTRx Expression Summary

| Expression | Memory Address | Pointer Update |
|:-----------|:---------------|:---------------|
| `PTRA` | PTRA | None |
| `PTRA[index]` | PTRA + index*SCALE | None |
| `PTRA++` | PTRA | PTRA += 1*SCALE |
| `PTRA--` | PTRA | PTRA -= 1*SCALE |
| `++PTRA` | PTRA + 1*SCALE | PTRA += 1*SCALE |
| `--PTRA` | PTRA - 1*SCALE | PTRA -= 1*SCALE |
| `PTRA++[index]` | PTRA | PTRA += index*SCALE |
| `PTRA--[index]` | PTRA | PTRA -= index*SCALE |
| `++PTRA[index]` | PTRA + index*SCALE | PTRA += index*SCALE |
| `--PTRA[index]` | PTRA - index*SCALE | PTRA -= index*SCALE |

All expressions work identically with PTRB.

### 6.4.8 Extended Index with AUGS

For index values beyond the 5-bit or 6-bit limits, use `##` to invoke AUGS:

```pasm2
        rdlong  x, ptra[##1000]         ' Index 1000 = 1000-byte offset
                                        ' (AUGS index is unscaled)
        rdbyte  y, ++ptrb[##$12345]     ' 20-bit index with update
```

With AUGS, the index becomes a 20-bit value, and the index is **not scaled**—it represents the actual byte offset:

```pasm2
' Without AUGS: index is scaled
        rdlong  x, ptra[10]             ' Offset = 10 * 4 = 40 bytes

' With AUGS: index is NOT scaled (direct byte offset)
        rdlong  x, ptra[##40]           ' Offset = 40 bytes (same result)
```


## 6.5 Block Transfers with SETQ and Pointers

The SETQ instruction enables efficient multi-long transfers between hub memory and cog/LUT RAM.

### 6.5.1 Basic Block Transfer

```pasm2
        setq    #15                     ' Transfer 16 longs (count - 1)
        rdlong  first_reg, ptra         ' Read 16 consecutive longs
```

SETQ specifies the count minus one. The transfer moves `count+1` longs at one long per clock cycle.

### 6.5.2 Block Transfer with Pointer Update

When using PTRx with SETQ block transfers, the pointer updates by the **total transfer size**:

```pasm2
' Post-increment: read from current PTRA, then advance by transfer size
        setq    #15                     ' 16 longs
        rdlong  buffer, ptra++          ' Read 16 longs, PTRA += 64

' Post-decrement: read from current PTRA, then move back
        setq    #15
        rdlong  buffer, ptra--          ' Read 16 longs, PTRA -= 64 bytes

' Pre-increment: advance first, then read
        setq    #15
        rdlong  buffer, ++ptra          ' PTRA += 64, then read 16 longs

' Pre-decrement: move back first, then read
        setq    #15
        rdlong  buffer, --ptra          ' PTRA -= 64, then read 16 longs
```

**Critical:** With SETQ block transfers, the index field is **overridden** by the block count. An arbitrary index cannot be specified:

```pasm2
' This does NOT work as expected:
        setq    #15
        rdlong  buffer, ptra++[5]       ' Index [5] IGNORED! Uses count
```

### 6.5.3 SETQ2 for LUT Transfers

SETQ2 works like SETQ but transfers to/from LUT RAM instead of cog RAM:

```pasm2
        setq2   #31                     ' Transfer 32 longs
        rdlong  lut_addr, ptra++        ' Read 32 longs into LUT
```

### 6.5.4 Hardware Bug: ALTx/AUGS Between SETQ and Transfer

::: {.warningbox}
**SILICON BUG:** Do not place ALTx, AUGS, or AUGD instructions between SETQ/SETQ2 and the block transfer instruction when using PTRx expressions.
:::

```pasm2
' BUGGY CODE - PTRx update is wrong!
        setq    #15                     ' Ready to transfer 16 longs
        altd    dest_reg                ' ALTD cancels block PTRx delta!
        rdlong  0, ptra++               ' PTRA += 4 (1 long), NOT 64!

' CORRECT CODE - No intervening instruction
        setq    #15
        rdlong  dest_reg, ptra++        ' PTRA correctly increments by 64
```

**Impact:** The data transfer completes correctly (16 longs are read), but PTRA only increments by the normal single-operation amount (4 bytes) instead of the block amount (64 bytes).

**Workaround:** Never place ALTx, AUGS, or AUGD between SETQ/SETQ2 and the subsequent RDLONG/WRLONG/WMLONG when using PTRx expressions.


## 6.6 ALTx Modified Addressing

The ALT instructions modify how the following instruction interprets its operands, enabling computed addresses and self-modifying code patterns.

**Hub-Exec Compatibility:** All ALTx instructions (ALTI, ALTS, ALTD, ALTR, ALTB, ALTSN, ALTSB, ALTSW, ALTGN, ALTGB, ALTGW) operate identically in cog-exec and hub-exec modes. The ALTx mechanism acts on the next pipelined instruction regardless of its source (cog/LUT memory or the hub-prefetch FIFO), enabling dynamic register-substitution patterns in hub-resident code blocks.

### 6.6.1 ALTD (Alter Destination)

ALTD modifies the destination field of the next instruction:

```pasm2
        altd    index, #base            ' Next D = base + index
        mov     0-0, value              ' Actually writes to base[index]
```

The assembler uses `0-0` as a placeholder for the modified destination.

### 6.6.2 ALTS (Alter Source)

ALTS modifies the source field of the next instruction:

```pasm2
        alts    index, #table           ' Next S = table + index
        mov     result, 0-0             ' Actually reads from table[index]
```

### 6.6.3 ALTI (Alter Both)

ALTI can modify both destination and source fields, plus the instruction opcode:

```pasm2
        alti    index, #template        ' Modify D, S, and opcode
        add     0-0, 0-0                ' Both operands modified
```

### 6.6.4 ALTx with AUGS Interaction

::: {.warningbox}
**SILICON BUG:** When an ALTx instruction with an immediate operand follows AUGS, the AUGS value affects both the ALTx and its intended target.
:::

```pasm2
' BUGGY CODE - AUGS affects both instructions
        augs    #$12340000
        altd    index, #$100            ' #$100 becomes #$12340100! (bug)
        mov     0-0, #$078              ' #$078 becomes #$12340078

' CORRECT CODE - Use register for ALTx operand
        mov     base, #$100             ' Put base in register
        augs    #$12340000
        altd    index, base             ' Register not affected by AUGS
        mov     0-0, #$078              ' Only this augments to #$12340078
```

**Workaround:** When using ALTx near AUGS, use a register for the ALTx S operand instead of an immediate.


## 6.7 Hub Address Expressions

Hub memory instructions accept several address expression forms:

### 6.7.1 Register Address

A register containing a hub address:

```pasm2
        mov     addr, ##$1000
        rdlong  x, addr                 ' Read from Hub address in register
```

### 6.7.2 Immediate Address

An 8-bit immediate hub address (limited range):

```pasm2
        rdlong  x, #$80                 ' Read from Hub address $80
```

### 6.7.3 Augmented Immediate Address

A 20-bit hub address using AUGS:

```pasm2
        rdlong  x, ##$12345             ' Read from Hub address $12345
```

### 6.7.4 Pointer Expressions

Any of the PTRx forms described in Section 6.4:

```pasm2
        rdlong  x, ptra                 ' Basic pointer
        rdlong  x, ptra++               ' With update
        rdlong  x, ptra[5]              ' With index
```


## 6.8 Address Mode Selection Guide

| Need | Recommended Mode |
|:-----|:-----------------|
| Local variable access | Direct register |
| Small constants (0-511) | 9-bit immediate (#) |
| Large constants, Hub addresses | Augmented immediate (##) |
| Sequential Hub access | PTRx with ++/-- |
| Random Hub access | PTRx with index |
| Structure field access | PTRx with fixed index |
| Block transfers | SETQ + PTRx |
| Computed register access | ALTx instructions |

### 6.8.1 Performance Considerations

**Fastest:** Direct register addressing (2 cycles)

**Fast:** 9-bit immediate (2 cycles)

**Moderate:** Augmented immediate (+2 cycles per AUG instruction)

**Variable:** Hub operations (9-16 clocks in cog/LUT mode, 9-26 clocks in HUB mode)

> **Timing Note:** Hub operations require ~9 base clocks plus 0-7 clocks waiting for the hub window (with 8 cogs). In HUB execution mode, the FIFO is busy fetching instructions, adding contention that extends the maximum to 26 clocks.

For time-critical inner loops:
- Frequently-used values should reside in cog registers
- Large constants should be pre-loaded before entering the loop
- Sequential hub access benefits from PTRx with ++/--
- Bulk data movement is most efficient with block transfers (SETQ)


```{=latex}
\begin{keyconcepts}
\item Direct register addressing uses 9-bit fields to access cog RAM at addresses \$000-\$1FF
\item The \# prefix creates 9-bit immediates (0-511); \#\# creates 32-bit immediates via AUGS/AUGD
\item Each AUG instruction adds +2 clock cycles; augmentation is consumed by the next instruction
\item PTRA and PTRB support post-modify (PTRx++), pre-modify (++PTRx), and indexed (PTRx[n]) forms
\item The SCALE factor (1/2/4) depends on instruction: byte=1, word=2, long=4
\item Non-updating index range: -32 to +31; updating index range: -16 to +16
\item SETQ block transfers override the index field; pointer updates by total transfer size
\item SILICON BUG: ALTx/AUGS between SETQ and PTRx transfer breaks pointer update
\item SILICON BUG: AUGS affects immediate operands in intervening ALTx instructions
\end{keyconcepts}
```


<!-- End of Chapter 6 -->
