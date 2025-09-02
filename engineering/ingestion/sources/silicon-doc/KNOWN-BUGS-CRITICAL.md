# P2 Silicon KNOWN BUGS - CRITICAL DOCUMENTATION

**SOURCE**: Silicon Doc p2-documentation.txt, Lines 197-227
**STATUS**: Active bugs in current silicon (Rev C)
**CRITICALITY**: HIGH - These affect code generation and instruction sequencing

## Bug #1: SETQ/SETQ2 Block Operations with PTRx Cancelled by ALTx/AUGS/AUGD

### Description
Intervening ALTx/AUGS/AUGD instructions between SETQ/SETQ2 and RDLONG/WRLONG/WMLONG-PTRx instructions will cancel the special-case block-size PTRx deltas.

### Impact
- The expected number of longs will still transfer correctly
- BUT: PTRx will only be modified according to normal PTRx expression behavior
- NOT: The expected block-size delta (number of longs * 4)

### Example of Bug
```pasm
SETQ    #16-1           'ready to load 16 longs
ALTD    start_reg       'alter start register (ALTD cancels block-size PTRx deltas)  
RDLONG  0,ptra++        'ptra will only be incremented by 4 (1 long), not 16*4 as anticipated!!!
```

### Workaround
Do not place ALTx, AUGS, or AUGD instructions between SETQ/SETQ2 and block transfer instructions when using PTRx expressions.

### Affected Instructions
- SETQ/SETQ2 followed by:
  - RDLONG with PTRx expressions
  - WRLONG with PTRx expressions
  - WMLONG with PTRx expressions

---

## Bug #2: AUGS Value Used by Intervening ALTx Instructions

### Description
Intervening ALTx instructions with an immediate #S operand, between AUGS and the AUGS' intended target instruction, will use the AUGS value but not cancel it.

### Impact
- The intervening ALTx instruction will unexpectedly use the AUGS value (if it has an immediate #S operand)
- The intended AUGS target instruction will still use and cancel the AUGS value as expected
- This causes the AUGS value to be applied to BOTH instructions instead of just the intended target

### Example of Bug
```pasm
AUGS    #$FFFFF123      'This AUGS is intended for the ADD instruction.
ALTD    index,#base     'Look out! AUGS will affect #base, too. Use a register, instead.
ADD     0-0,#$123       '#$123 will be augmented by the AUGS and cancel the AUGS.
```

### Workaround
To avoid problems in these circumstances, use a register for the S operand of the ALTx instruction, and not an immediate #S operand.

### Correct Code
```pasm
        MOV     base_reg, #base     'Put base in a register
AUGS    #$FFFFF123                  'This AUGS is for the ADD instruction only
ALTD    index, base_reg             'Using register avoids AUGS application
ADD     0-0, #$123                  'AUGS correctly applies only here
```

---

## Impact on Code Generation

### For AI Code Generation
1. **NEVER** place ALTx/AUGS/AUGD between SETQ and block transfers with PTRx
2. **ALWAYS** use register operands (not immediates) for ALTx instructions that appear after AUGS
3. **VALIDATE** instruction sequences to ensure these patterns don't occur

### For Compiler/Assembler Writers  
1. Add warnings for these instruction sequences
2. Consider automatic instruction reordering to avoid these patterns
3. Document these restrictions clearly in error messages

### For Manual Assembly Programmers
1. Be extremely careful with instruction ordering
2. Test PTRx values after block operations to verify correct updates
3. Use registers instead of immediates for ALTx S operands when near AUGS

---

## Verification Test Cases

### Test 1: SETQ Block Transfer Bug
```pasm
' Setup
        MOV     ptra, ##$1000
        MOV     x, ptra         'Save original

' Bug case - PTRx only increments by 4
        SETQ    #4-1            'Transfer 4 longs
        ALTD    dest            'This breaks PTRx update!
        RDLONG  0, ptra++       
        
        SUB     ptra, x         'Should be 16, will be 4!

' Correct case - PTRx increments by 16  
        MOV     ptra, ##$1000
        SETQ    #4-1            'Transfer 4 longs
        RDLONG  dest, ptra++    'No intervening instruction
        
        SUB     ptra, x         'Will correctly be 16
```

### Test 2: AUGS Interference Bug
```pasm
' Bug case - AUGS affects both instructions
        AUGS    #$12340000
        ALTD    index, #$100    '#$100 becomes #$12340100!
        MOV     dest, #$5678    '#$5678 becomes #$12345678
        
' Correct case - AUGS affects only intended instruction
        MOV     base, #$100     'Use register
        AUGS    #$12340000
        ALTD    index, base     'base register not affected
        MOV     dest, #$5678    '#$5678 becomes #$12345678
```

---

## Historical Context
- These bugs exist in Rev C silicon (current production as of 2020-06-01)
- 7,000 Rev C chips were received from ON Semi
- Rev C fixed the adjacent-pin ADC crosstalk problem from prior revisions
- These instruction sequencing bugs remain in Rev C

## Cross-Reference
- Affects: PTRA/PTRB operations with SETQ block transfers
- Affects: AUGS/AUGD immediate value extension
- Affects: ALTx instruction behavior
- Related to: Instruction pipelining and execution order