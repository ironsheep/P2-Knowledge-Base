# _RET_ CONDITION - CRITICAL ERROR ANALYSIS

**Date:** 2025-12-12
**Severity:** CRITICAL - Fundamental behavioral error
**Reported by:** Reader feedback
**Analyzed by:** Claude Opus 4.5 (ultrathink audit)

---

## Executive Summary

Our manual contains **fundamentally incorrect information** about the `_RET_` condition prefix. The error is not minor - it describes the exact opposite of actual behavior.

| Aspect | Our Manual (WRONG) | Correct Behavior |
|--------|-------------------|------------------|
| Instruction execution | "instruction field is ignored" | **Instruction IS executed** |
| Code example comment | "Return, ADD is not executed" | ADD **IS** executed, then return |
| Flag restoration | Not mentioned | No C/Z restoration (unlike RET WCZ) |
| Branch handling | Not mentioned | No return if instruction branches |

---

## Source Authority Cross-Reference

### 1. P2 Instructions CSV v35 (AUTHORITATIVE)
```
_RET_         <inst>  <ops>,Instruction Prefix,0000 ------- --- --------- ---------
Execute <inst> always and return if no branch. If <inst> is not branching
then return by popping stack[19:0] into PC.
```
**Key points:**
- "Execute <inst> always" - instruction IS executed
- "return if no branch" - only returns if instruction didn't branch
- "popping stack[19:0] into PC" - only restores PC, not flags

### 2. Parallax PASM2 Manual (AUTHORITATIVE)
```
_RET_    %0000    always; execute instruction then return if no branch; no context restore
```
**Key points:**
- "execute instruction" - instruction IS executed
- "then return if no branch" - returns after instruction, unless it branched
- "no context restore" - does NOT restore C/Z flags from stack

### 3. Silicon Documentation (AUTHORITATIVE)
Used extensively in XBYTE examples:
```pasm
        PUSH    #$1FF                   ' Push $1FF onto hardware stack
_RET_   SETQ    #$100                   ' Start XBYTE: SETQ executes, then returns to $1FF
```
**Key proof:** If SETQ was ignored, XBYTE would not be configured. The entire XBYTE mechanism depends on `_RET_ SETQ` actually executing SETQ.

Also confirms:
```
"The bytecode routine could be as short as a single 2-clock instruction with
a _RET_ prefix, making the total XBYTE loop take only 8 clocks."
```
This proves the instruction executes (2 clocks) + return overhead (6 clocks) = 8 total.

---

## Detailed Error Analysis

### ERROR #1: "instruction field is ignored" (chapter-02-instruction-format.md:66)

**Our Manual Says:**
```markdown
- The instruction field is ignored
- PC is loaded from the return address stored in PA (for CALL) or from the stack
```

**Correct Behavior:**
The instruction IS executed. Only PC[19:0] is restored from the stack (not flags, not PA).

### ERROR #2: Code Example (chapter-02-instruction-format.md:72-73)

**Our Manual Shows:**
```pasm
_ret_   add     x, y                    ' Return, ADD is not executed
```

**Correct Code Should Be:**
```pasm
_ret_   add     x, y                    ' ADD executes, then return (no flag restore)
```

### ERROR #3: Missing "if no branch" Behavior

When `_RET_` prefixes a **branching** instruction (JMP, CALL, etc.):
- The branch instruction executes normally
- **No return occurs** because the instruction changed PC

Example:
```pasm
_ret_   jmp     #somewhere              ' JMP executes - NO return happens!
```

This is NOT documented in our manual.

### ERROR #4: Missing "no context restore" Explanation

**RET instruction (full):**
- `RET WCZ` restores C and Z flags from stack K[31:30]
- Restores PC from stack K[19:0]

**_RET_ prefix:**
- Does NOT restore C or Z flags
- Only restores PC from stack[19:0]

This distinction is critical for code that depends on flag state after return.

### ERROR #5: Incorrect PA Reference

**Our Manual Says:**
```
PC is loaded from the return address stored in PA (for CALL)
```

**This is Wrong:**
- Regular CALL/RET use the hardware stack, not PA
- PA is only involved with CALLD when explicitly specified
- _RET_ always pops from hardware stack

### ERROR #6: Missing Timing Information

**CSV Shows:**
```
Timing: +2,+11...18 (COG/Hub)
```

Meaning _RET_ **adds** to the base instruction timing:
- COG: instruction cycles + 2 cycles for return
- Hub: instruction cycles + 11-18 cycles for return

---

## Correct _RET_ Behavior Summary

1. **Always Execute**: The prefixed instruction always executes (EEEE=0000 means "always" for _RET_)

2. **Conditional Return**: After execution:
   - IF instruction did NOT branch → pop stack[19:0] into PC (return)
   - IF instruction DID branch → no return (branch took precedence)

3. **No Context Restore**: Unlike `RET WCZ`, `_RET_` does NOT restore C/Z flags from stack

4. **Timing**: Adds 2 clocks (COG) or 11-18 clocks (Hub) to instruction timing

5. **Use Cases**:
   - XBYTE bytecode interpreter: `_RET_ SETQ` configures XBYTE AND returns
   - Single-instruction subroutines: `_RET_ drvnot #0` toggles pin AND returns
   - Compact code: Execute one more instruction before returning

---

## Required Fixes

### Fix Location: `opus-master/part-i/chapter-02-instruction-format.md`

**Current (lines 64-75):**
```markdown
### 2.2.2 The _RET_ Condition

The condition code 0000 (_RET_) has special behavior. When an instruction has EEEE=0000,
it functions as a return from subroutine:

- The instruction field is ignored
- PC is loaded from the return address stored in PA (for CALL) or from the stack

This encoding allows any instruction mnemonic to become a conditional return when prefixed with _RET_:

```pasm
_ret_   add     x, y                    ' Return, ADD is not executed
```

The _RET_ prefix is primarily used with CALLA, CALLB, and related call instructions
that use the condition field for return control.
```

**Corrected Version:**
```markdown
### 2.2.2 The _RET_ Condition

The condition code 0000 (_RET_) has special behavior. Unlike other condition codes,
_RET_ means "always execute the instruction, then return if the instruction did not branch."

When an instruction has EEEE=0000:

1. The instruction **always executes** (condition code 0000 means "always" for _RET_)
2. **If the instruction does not branch**: PC is loaded from stack[19:0], returning to the caller
3. **If the instruction branches** (JMP, CALL, etc.): No return occurs; the branch takes precedence
4. **No context restore**: Unlike `RET WCZ`, the _RET_ prefix does NOT restore C or Z flags

This is different from the RET instruction, which optionally restores C and Z flags with WC/WZ/WCZ.

```pasm
_ret_   add     x, y                    ' ADD executes, then return (flags unchanged)
_ret_   jmp     #label                  ' JMP executes - NO return (branch took precedence)
_ret_   drvnot  #0                      ' Toggle pin 0, then return
```

The _RET_ prefix adds 2 clock cycles (COG/LUT execution) or 11-18 cycles (Hub execution)
to the base instruction timing.

**Common Uses:**
- **XBYTE bytecode interpreter**: `_RET_ SETQ #$100` configures XBYTE mode and returns to $1FF
- **Single-instruction subroutines**: Execute one operation and return in minimal cycles
- **Compact returns**: Combine final operation with return

```pasm
' XBYTE startup - SETQ executes to configure mode, then returns to $1FF
        push    #$1FF
_ret_   setq    #$100                   ' SETQ executes, configures XBYTE, then returns

' Efficient single-instruction subroutine
toggle_pin
_ret_   drvnot  #0                      ' Toggle pin 0 (2 clocks) + return (2 clocks) = 4 clocks
```
```

---

## Impact Assessment

| Area | Impact |
|------|--------|
| **Educational** | HIGH - Readers learn incorrect behavior |
| **Code Examples** | HIGH - Examples would fail if attempted |
| **XBYTE Understanding** | CRITICAL - Cannot understand bytecode execution |
| **Debugging** | HIGH - Wrong mental model leads to confusion |

---

## Verification Test

To verify correct behavior, assemble and test:

```pasm
DAT     org

        ' Test 1: _RET_ ADD should execute ADD
test1   mov     result, #0
        call    #add_and_return
        ' result should be 10, not 0

        ' Test 2: _RET_ JMP should NOT return
test2   call    #jmp_test
        ' Should NOT reach here if _RET_ JMP works correctly

        cogstop #0

add_and_return
_ret_   add     result, #10             ' ADD executes, result=10, then return

jmp_test
_ret_   jmp     #infinite               ' JMP executes, NO return
        ret                             ' Never reached

infinite
        jmp     #infinite

result  long    0
```

---

## Action Items

1. **IMMEDIATE**: Fix chapter-02-instruction-format.md with corrected _RET_ documentation
2. **VERIFY**: Check all other _RET_ references in manual for consistency
3. **ADD**: Consider adding _RET_ to instruction reference in Part II
4. **TEST**: Verify examples compile and behave correctly

---

**Analysis Complete**
**Recommendation:** IMMEDIATE FIX REQUIRED - This is a fundamental behavioral error
