# Appendix B: Condition Code Reference

This appendix is the **canonical reference** for all P2 condition codes. The EEEE field (bits 31-28) of every instruction specifies one of sixteen conditions that control whether the instruction executes based on the current C and Z flag states.

Every instruction can be made conditional by prefixing it with one of these condition mnemonics. When the condition is false, the instruction does not execute but still consumes its normal execution time (2 clock cycles for most instructions).


## B.1 Complete Condition Code Table

| EEEE | Primary Mnemonic | Condition | All Aliases |
|:-----|:-----------------|:----------|:------------|
| 0000 | _RET_ | Always + return | — |
| 0001 | IF_NC_AND_NZ | C=0 AND Z=0 | IF_NZ_AND_NC, IF_GT, IF_A, IF_00 |
| 0010 | IF_NC_AND_Z | C=0 AND Z=1 | IF_Z_AND_NC, IF_01 |
| 0011 | IF_NC | C=0 | IF_GE, IF_AE, IF_0X |
| 0100 | IF_C_AND_NZ | C=1 AND Z=0 | IF_NZ_AND_C, IF_10 |
| 0101 | IF_NZ | Z=0 | IF_NE, IF_X0 |
| 0110 | IF_C_NE_Z | C!=Z | IF_Z_NE_C, IF_DIFF |
| 0111 | IF_NC_OR_NZ | C=0 OR Z=0 | IF_NZ_OR_NC, IF_NOT_11 |
| 1000 | IF_C_AND_Z | C=1 AND Z=1 | IF_Z_AND_C, IF_11 |
| 1001 | IF_C_EQ_Z | C=Z | IF_Z_EQ_C, IF_SAME |
| 1010 | IF_Z | Z=1 | IF_E, IF_X1 |
| 1011 | IF_NC_OR_Z | C=0 OR Z=1 | IF_Z_OR_NC, IF_NOT_10 |
| 1100 | IF_C | C=1 | IF_LT, IF_B, IF_1X |
| 1101 | IF_C_OR_NZ | C=1 OR Z=0 | IF_NZ_OR_C, IF_NOT_01 |
| 1110 | IF_C_OR_Z | C=1 OR Z=1 | IF_Z_OR_C, IF_LE, IF_BE, IF_NOT_00 |
| 1111 | IF_ALWAYS | Always | — |


## B.2 Alias Categories

The P2 provides multiple aliases for the same condition codes, enabling programmers to express intent clearly in different contexts.

### B.2.1 Comparison Aliases

After a comparison instruction (CMP or CMPS), condition aliases express relational comparisons. Two equivalent terminology styles are available—choose whichever reads best for your code:

| Relationship | Magnitude Style | Arithmetic Style | Primary | Flag State |
|:-------------|:----------------|:-----------------|:--------|:-----------|
| Greater than | IF_A (Above) | IF_GT (Greater Than) | IF_NC_AND_NZ | C=0, Z=0 |
| Greater or equal | IF_AE (Above or Equal) | IF_GE (Greater or Equal) | IF_NC | C=0 |
| Less than | IF_B (Below) | IF_LT (Less Than) | IF_C | C=1 |
| Less or equal | IF_BE (Below or Equal) | IF_LE (Less or Equal) | IF_C_OR_Z | C=1 OR Z=1 |
| Equal | IF_E | IF_E | IF_Z | Z=1 |
| Not equal | IF_NE | IF_NE | IF_NZ | Z=0 |

**Magnitude terminology** (A = Above, B = Below) reads naturally with unsigned values like addresses, counts, and sizes.

**Arithmetic terminology** (GT = Greater Than, LT = Less Than) reads naturally with signed values like temperatures, positions, and deltas.

Both styles encode to the same condition codes—the choice is purely stylistic. Use whichever terminology makes your code's intent clearer.

### B.2.2 Flag State Aliases

Express exact C/Z bit patterns directly:

| Alias | C | Z | Primary |
|:------|:--|:--|:--------|
| IF_00 | 0 | 0 | IF_NC_AND_NZ |
| IF_01 | 0 | 1 | IF_NC_AND_Z |
| IF_10 | 1 | 0 | IF_C_AND_NZ |
| IF_11 | 1 | 1 | IF_C_AND_Z |
| IF_0X | 0 | * | IF_NC |
| IF_1X | 1 | * | IF_C |
| IF_X0 | * | 0 | IF_NZ |
| IF_X1 | * | 1 | IF_Z |

The asterisk (*) indicates "don't care"—the condition is true regardless of that flag's value.

### B.2.3 Logical Aliases

Express logical relationships between flag states:

| Alias | Meaning | Primary |
|:------|:--------|:--------|
| IF_SAME | C equals Z | IF_C_EQ_Z |
| IF_DIFF | C differs from Z | IF_C_NE_Z |
| IF_NOT_00 | Not both clear | IF_C_OR_Z |
| IF_NOT_01 | Not (C=0, Z=1) | IF_C_OR_NZ |
| IF_NOT_10 | Not (C=1, Z=0) | IF_NC_OR_Z |
| IF_NOT_11 | Not both set | IF_NC_OR_NZ |

### B.2.4 Commutative Forms

These pairs are identical—the operand order in the name is interchangeable:

| Form 1 | Form 2 |
|:-------|:-------|
| IF_NC_AND_NZ | IF_NZ_AND_NC |
| IF_NC_AND_Z | IF_Z_AND_NC |
| IF_C_AND_NZ | IF_NZ_AND_C |
| IF_C_AND_Z | IF_Z_AND_C |
| IF_NC_OR_NZ | IF_NZ_OR_NC |
| IF_NC_OR_Z | IF_Z_OR_NC |
| IF_C_OR_NZ | IF_NZ_OR_C |
| IF_C_OR_Z | IF_Z_OR_C |
| IF_C_EQ_Z | IF_Z_EQ_C |
| IF_C_NE_Z | IF_Z_NE_C |


## B.3 The _RET_ Condition (EEEE=0000)

The condition code 0000 (`_RET_`) has special behavior that differs from all other conditions. Unlike other condition codes which control whether the instruction executes, `_RET_` means: **"Always execute the instruction, then return if the instruction did not branch."**

### B.3.1 Behavior

When an instruction has EEEE=0000:

1. **The instruction always executes** (condition 0000 means "always" for `_RET_`)
2. **If the instruction does not branch**: Return by popping stack[19:0] into PC
3. **If the instruction branches** (JMP, CALL, etc.): No return occurs—the branch takes precedence
4. **No context restore**: Unlike `RET WCZ`, the `_RET_` prefix does NOT restore C or Z flags from the stack

This is fundamentally different from the RET instruction, which optionally restores C and Z flags when WC/WZ/WCZ effects are specified.

### B.3.2 Basic Usage

::: pasm2
        _ret_   add     x, y            ' ADD then return (flags unchanged)
        _ret_   drvnot  #0              ' Toggle pin 0, then return
        _ret_   mov     result, temp    ' Copy to result, then return
:::

### B.3.3 Branch Behavior

When `_RET_` prefixes a branching instruction, the branch executes normally but no return occurs because the instruction itself changed PC:

::: pasm2
        _ret_   jmp     #somewhere      ' JMP executes, NO return
        _ret_   call    #subroutine     ' CALL executes, NO return
        _ret_   djnz    counter, #loop  ' Branch: no return; zero: return
:::

For DJNZ and similar conditional branches: if the branch is taken, no return occurs; if the branch is not taken (counter reaches zero), the return executes.

### B.3.4 XBYTE Bytecode Interpreter

The `_RET_` prefix with SETQ and SETQ2 is essential for the XBYTE bytecode execution mechanism. When the top of the hardware stack holds $1FF, these combinations configure XBYTE mode:

::: pasm2
' Start XBYTE: SETQ configures mode, returns to $1FF
        push    #$1FF                   ' Push $1FF for XBYTE returns
        _ret_   setq    #$100           ' LUT base $100, then return

' Change XBYTE mode permanently
        _ret_   setq    #$200           ' New LUT base for all bytecodes

' Change XBYTE mode for next bytecode only
        _ret_   setq2   #$300           ' Temporary LUT base for one bytecode
:::

### B.3.5 SKIP/SKIPF with _RET_

Both SKIP and SKIPF can be combined with `_RET_` to branch before a skip pattern begins:

::: pasm2
        push    #routine                ' Push target address
        _ret_   skipf   pattern         ' SKIPF then branch with skip active
:::

### B.3.6 Timing

The `_RET_` prefix adds overhead to the base instruction timing:

| Execution Mode | Additional Cycles |
|:---------------|:------------------|
| COG/LUT | +2 cycles |
| Hub | +11 to +18 cycles |

### B.3.7 Single-Instruction Subroutines

The `_RET_` prefix enables efficient single-instruction subroutines:

::: pasm2
toggle_pin0                             ' Subroutine: toggle pin 0
        _ret_   drvnot  #0              ' 2 + 2 return = 4 cycles

read_input                              ' Subroutine: read input
        _ret_   mov     result, ina     ' MOV, then return
:::

This is significantly faster than a separate instruction followed by RET (which would take at least 4 additional cycles).


## B.4 Conditional Execution Timing

When a conditional instruction's condition is false, the instruction does not execute but still consumes 2 clock cycles. This provides deterministic timing—critical for real-time operations:

::: pasm2
                cmp     a, b            wc wz   ' 2 cycles - always
        if_z    mov     result, #1              ' 2 cycles - whether Z=1 or not
        if_nz   mov     result, #0              ' 2 cycles - whether Z=0 or not
                                                ' Total: always 6 cycles
:::

This timing predictability enables branchless programming where instruction timing remains constant regardless of data values.
