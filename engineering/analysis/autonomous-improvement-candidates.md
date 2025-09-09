# PASM2 Instructions - Autonomous Improvement Candidates

*Generated: 2025-09-09*

## Overview

These are the PASM2 instructions where we can confidently propose documentation improvements based on:
- Code patterns from production analysis (flash_loader, debugger, motor control, etc.)
- Instruction family similarities
- Clear operational patterns
- Existing comprehensive documentation of related instructions

## Category 1: Pin Control Instructions (15 instructions)
**Confidence: HIGH** - Simple patterns, good examples available

### Can Improve Now:
1. **DRVH** - Drive pin high (have examples from all analyzed code)
2. **DIRH** - Set pin direction high (pattern clear from DRVL)
3. **DIRL** - Set pin direction low (pattern clear from DIRH)
4. **FLTL** - Float pin low (reset smart pin pattern seen)
5. **FLTH** - Float pin high (complementary to FLTL)
6. **OUTL** - Set OUT register low (pattern clear)
7. **OUTH** - Set OUT register high (pattern clear)
8. **DIRC/DRVNC/OUTNC** - Conditional versions (pattern consistent)
9. **DIRNOT/DRVNOT/OUTNOT** - Toggle versions (pattern consistent)
10. **DIRNZ/DRVNZ/OUTNZ** - Zero conditional versions

### Proposed Template Pattern:
```yaml
instruction: DRVH
description: |
  Drive one or more pins high (output 1). Sets both the direction 
  register (DIR) and output register (OUT) for the specified pins.
  Can operate on single pins or pin groups using ADDPINS.
parameters:
  - name: D
    description: |
      Pin specification:
      - Single pin: 0-63
      - Pin group: Use ADDPINS operator
      - Example: 32 ADDPINS 3 = pins 32-35
examples:
  - name: Single Pin
    code: drvh    #LED_PIN
  - name: Pin Group  
    code: drvh    #BASE_PIN ADDPINS 7   ' 8 pins
```

## Category 2: Smart Pin Instructions (5 instructions)
**Confidence: HIGH** - Extensive examples from flash_loader and motor control

### Can Improve Now:
1. **WRPIN** - Configure smart pin mode (many examples)
2. **WXPIN** - Set X parameter (timing/config examples)
3. **RDPIN** - Read pin result (clear patterns)
4. **RQPIN** - Read pin status (can infer from usage)
5. **AKPIN** - Acknowledge pin (pattern from WYPIN)

### Evidence Base:
- Flash loader: Complete SPI implementation
- Motor control: ADC and PWM patterns
- HUB75 driver: Parallel output patterns

## Category 3: Basic ALU Variants (25 instructions)
**Confidence: HIGH** - Can infer from base instructions

### Can Improve Now:
1. **ADDS/ADDX/ADDSX** - Signed/carry variants of ADD
2. **SUBS/SUBX/SUBSX** - Signed/carry variants of SUB
3. **CMPS/CMPX/CMPSX** - Signed/carry variants of CMP
4. **NEGC/NEGNC/NEGZ/NEGNZ** - Conditional NEG variants
5. **SUMC/SUMNC/SUMZ/SUMNZ** - Conditional sum variants
6. **BITC/BITNC/BITZ/BITNZ** - Conditional bit operations
7. **MUXC/MUXNC/MUXZ/MUXNZ** - Conditional mux operations
8. **MODC/MODZ/MODCZ** - Flag modification instructions

### Pattern Example:
```yaml
instruction: ADDS
description: |
  Add signed values. Identical to ADD but treats operands as 
  signed integers for flag calculations. The addition itself
  is the same, only flag interpretation differs.
flags_affected:
  C: Signed overflow (V flag equivalent)
  Z: Result is zero
related:
  - ADD: Unsigned addition
  - ADDSX: Signed addition with C
```

## Category 4: Shift/Rotate Instructions (8 instructions)
**Confidence: HIGH** - Patterns are consistent

### Can Improve Now:
1. **SAL** - Shift arithmetic left (same as SHL)
2. **SAR** - Shift arithmetic right (sign-extending)
3. **RCL** - Rotate through carry left
4. **RCR** - Rotate through carry right
5. **ZEROX** - Zero-extend value
6. **SIGNX** - Sign-extend value
7. **REV** - Reverse bits
8. **MOVBYTS** - Move bytes (have examples)

## Category 5: Memory Operations (10 instructions)
**Confidence: MEDIUM-HIGH** - Clear patterns from usage

### Can Improve Now:
1. **RDBYTE/RDWORD** - Pattern from RDLONG
2. **WRBYTE/WRWORD** - Pattern from WRLONG
3. **WMLONG** - Masked write (have examples)
4. **RDLUT/WRLUT** - LUT access (debugger examples)
5. **GETBYTE/SETBYTE** - Byte manipulation
6. **GETWORD/SETWORD** - Word manipulation
7. **GETNIB/SETNIB** - Nibble manipulation

## Category 6: Branch Instructions (15 instructions)
**Confidence: HIGH** - Patterns are consistent

### Can Improve Now:
1. **CALL/CALLA/CALLB** - Call variants (clear patterns)
2. **RETA/RETB** - Return variants
3. **JMP** - Already comprehensive but can add examples
4. **JMPREL** - Relative jump
5. **TJZ/TJNZ/TJF/TJNF** - Test and jump variants
6. **DJZ/DJNZ/DJF/DJNF** - Decrement and jump variants
7. **IJZ/IJNZ** - Increment and jump variants

## Category 7: Stack Operations (6 instructions)
**Confidence: HIGH** - Debugger shows complete patterns

### Can Improve Now:
1. **PUSH/POP** - Basic stack ops
2. **PUSHA/POPA** - Stack A operations
3. **PUSHB/POPB** - Stack B operations

### Example from Debugger:
```yaml
instruction: PUSH
description: |
  Push value onto 8-level hardware stack. The hardware stack
  is independent of hub RAM and provides fast subroutine
  return address storage.
examples:
  - name: Save Return Address
    code: |
      push    return_addr
      call    #subroutine
      pop     return_addr
```

## Category 8: COG Control (8 instructions)
**Confidence: MEDIUM-HIGH** - Good examples available

### Can Improve Now:
1. **COGINIT** - Start COG (many examples)
2. **COGSTOP** - Stop COG (pattern clear)
3. **COGID** - Get COG ID (simple)
4. **COGATN** - Signal attention (debugger examples)
5. **POLLATN** - Poll attention
6. **WAITATN** - Wait for attention
7. **COGBRK** - Break COG (debugger)
8. **GETBRK** - Get break status

## Category 9: Lock Instructions (4 instructions)
**Confidence: HIGH** - Debugger shows all patterns

### Can Improve Now:
1. **LOCKTRY** - Try to acquire lock
2. **LOCKREL** - Release lock
3. **LOCKNEW** - Allocate new lock
4. **LOCKRET** - Return lock to pool

### Complete Pattern from Debugger:
```yaml
instruction: LOCKTRY
description: |
  Attempt to acquire a hardware lock (non-blocking). Returns
  immediately with C flag indicating success. Used for mutual
  exclusion between COGs.
parameters:
  - name: D
    description: Lock number (0-15), result stored here if LOCKNEW
  - name: S
    description: Lock number for immediate form
flags_affected:
  C: 1 if lock acquired, 0 if busy
examples:
  - name: Critical Section
    code: |
      .retry  locktry #RESOURCE_LOCK wc
      if_nc   jmp     #.retry
              ' Critical section
              lockrel #RESOURCE_LOCK
```

## Category 10: Simple Instructions (10 instructions)
**Confidence: HIGH** - Operations are straightforward

### Can Improve Now:
1. **NOP** - Already comprehensive
2. **NOT** - Bitwise NOT (needs parameters section)
3. **TEST/TESTN** - Test bits (have good docs)
4. **SKIP/SKIPF** - Skip instructions (have examples)
5. **GETCT** - Get counter (simple)
6. **WAITX** - Wait cycles (enhanced already)
7. **HUBSET** - Set hub config (have examples)
8. **CLKSET** - Set clock (depreciated but documentable)

## Summary

### Total Instructions We Can Improve: ~100

**By Confidence Level:**
- HIGH Confidence: 75 instructions
- MEDIUM-HIGH Confidence: 25 instructions

**By Priority:**
- Critical (Smart Pins, Pin Control): 20 instructions
- High (Basic ALU, Branches): 40 instructions
- Medium (Memory, COG Control): 25 instructions
- Low (Simple operations): 15 instructions

### Proposed Next Steps:

1. **Generate documentation for HIGH confidence instructions first**
   - Use consistent template
   - Include real code examples
   - Mark as "proposed_documentation"

2. **Create validation checklist for each**
   - Flag formulas to verify
   - Timing to confirm
   - Edge cases to validate

3. **Group by families for consistency**
   - All conditional variants together
   - All pin operations together
   - All memory operations together

This systematic approach will improve documentation for ~30% of all PASM2 instructions without requiring external expertise, focusing on the most commonly used operations first.