# ADD Instruction - Example with Full Lineage

## ADD - Add Two Unsigned Values

[PRIMARY SOURCE: P2 Instructions v35 Spreadsheet, Row 34]
[SECONDARY SOURCE: PASM2 Manual Draft 221117, Page 22 (category listing)]
[CONFIDENCE: Verified - Multiple authoritative sources agree]

### Syntax
```pasm2
ADD     D,{#}S   {WC/WZ/WCZ}
```

### Encoding
[SOURCE: P2 Instructions v35, Row 34, Column 4]
```
EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS
```
- EEEE: Condition code (4 bits)
- 0001000: Opcode (7 bits)
- C: Write C flag (1 bit)
- Z: Write Z flag (1 bit)  
- I: Immediate flag (1 bit, 0=register, 1=immediate)
- D: Destination register (9 bits)
- S: Source value/register (9 bits)

### Timing
[SOURCE: P2 Instructions v35, Row 34, Columns 8-11]
- **Cog/LUT Execution**: 2 cycles (8 or 16 cogs)
- **Hub Execution**: 2 cycles (same for both cog configurations)
- **Pipeline**: Normal, no special shielding

### Operation
[SOURCE: P2 Instructions v35, Row 34, Column 6]
```
D = D + S
```
Adds the source value S to the destination register D, storing result in D.

### Flags
[SOURCE: P2 Instructions v35, Row 34, Column 6]
- **C Flag**: Set to carry bit from addition (bit 32 of result)
- **Z Flag**: Set if result equals zero (standard behavior)

### Parameters
[SOURCE: PASM2 Manual Draft, General Conventions]
- **D**: Destination register (0-511/$000-$1FF)
- **S**: Source - can be register (0-511) or 9-bit immediate value (0-511) when # prefix used
- **WC**: Optional - write carry flag
- **WZ**: Optional - write zero flag
- **WCZ**: Optional - write both flags

### Examples

[GENERATED - NEEDS HARDWARE VALIDATION]
```pasm2
; Example 1: Simple addition with immediate
    ADD     count, #1          ; Increment count by 1
    
; Example 2: Add two registers
    ADD     total, value       ; Add value to total
    
; Example 3: Addition with carry flag
    ADD     sum, addend  WC    ; Add and save carry for multi-precision
    
; Example 4: Multi-precision addition (32+32=64 bit)
    ADD     low_result, low_val  WC    ; Add low longs, save carry
    ADDX    high_result, high_val      ; Add high longs with carry
```

[SOURCE: Community Forum - Needs Verification]
```pasm2
; Example 5: Conditional execution based on carry
    ADD     value, limit  WC   ; Add and check for overflow
    IF_C    JMP #overflow     ; Branch if carry set (overflow occurred)
```

### Related Instructions
[SOURCE: P2 Instructions v35, Rows 35-37]
- **ADDX**: Add with carry extended (Row 35)
- **ADDS**: Add signed values (Row 36)  
- **ADDSX**: Add signed with carry extended (Row 37)
- **SUB**: Subtract (opposite operation)

### Notes and Warnings
[DERIVED from instruction format]
- Immediate values limited to 9 bits (0-511)
- For larger immediates, use AUGMENT prefix instruction
- Result wraps at 32 bits in single-precision operations

### Validation Status
- Encoding: ✅ Verified (Spreadsheet)
- Timing: ✅ Verified (Spreadsheet)
- Operation: ✅ Verified (Spreadsheet)
- Examples 1-4: ⚠️ Generated - Need hardware test
- Example 5: ⚠️ Community - Needs verification

### Traceability Matrix

| Information | Source | Row/Page | Status |
|------------|--------|----------|---------|
| Instruction name | P2 Instructions v35 | Row 34 | Verified |
| Encoding | P2 Instructions v35 | Row 34, Col 4 | Verified |
| Operation formula | P2 Instructions v35 | Row 34, Col 6 | Verified |
| Clock cycles | P2 Instructions v35 | Row 34, Cols 8-11 | Verified |
| Flag behavior | P2 Instructions v35 | Row 34, Col 6 | Verified |
| Multi-precision example | Generated | - | Needs validation |
| Conditional execution | Community | Forum post | Needs verification |