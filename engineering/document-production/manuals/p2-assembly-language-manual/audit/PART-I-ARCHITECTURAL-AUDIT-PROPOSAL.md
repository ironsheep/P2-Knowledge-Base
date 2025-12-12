# PART I ARCHITECTURAL AUDIT PROPOSAL

**Created:** 2025-12-12
**Triggered by:** `_RET_` critical error discovery
**Purpose:** Audit non-instruction documentation that was missed in the 357-instruction audit

---

## Why This Audit Is Needed

The comprehensive multi-agent audit focused on **Part II: Instruction Reference** - validating each of the 357 PASM2 instructions. However, **Part I: Architecture and Concepts** was not systematically audited.

The `_RET_` error was in Chapter 2 (Instruction Format), not in the instruction reference. It's a **condition prefix**, not an instruction. Our instruction-centric approach missed it entirely.

### Root Cause Analysis

| Audit Scope | Coverage | Result |
|-------------|----------|--------|
| Part II: Instructions A-Z | 100% audited | 99.9% accurate |
| Part I: Architecture | NOT audited | **Unknown accuracy** |
| Part III: Appendices | Partial | Some issues found |

---

## Scope: Items to Audit

### 1. CONDITION PREFIXES (Chapter 2)
**Status:** `_RET_` was CRITICALLY WRONG
**Risk:** HIGH for remaining conditions

| Code | Primary Form | Aliases to Verify |
|------|-------------|-------------------|
| 0000 | _RET_ | ✅ FIXED |
| 0001 | IF_NC_AND_NZ | IF_00, IF_A, IF_GT, IF_NZ_AND_NC |
| 0010 | IF_NC_AND_Z | IF_01, IF_Z_AND_NC |
| 0011 | IF_NC | IF_0X, IF_AE, IF_GE |
| 0100 | IF_C_AND_NZ | IF_10, IF_NZ_AND_C |
| 0101 | IF_NZ | IF_NE, IF_X0 |
| 0110 | IF_C_NE_Z | IF_Z_NE_C, IF_DIFF |
| 0111 | IF_NC_OR_NZ | IF_NZ_OR_NC, IF_NOT_11 |
| 1000 | IF_C_AND_Z | IF_11, IF_Z_AND_C |
| 1001 | IF_C_EQ_Z | IF_Z_EQ_C, IF_SAME |
| 1010 | IF_Z | IF_E, IF_X1 |
| 1011 | IF_NC_OR_Z | IF_Z_OR_NC, IF_NOT_10 |
| 1100 | IF_C | IF_1X, IF_B, IF_LT |
| 1101 | IF_C_OR_NZ | IF_NZ_OR_C, IF_NOT_01 |
| 1110 | IF_C_OR_Z | IF_Z_OR_C, IF_BE, IF_LE, IF_NOT_00 |
| 1111 | (always) | Default when no prefix |

**Validation needed:**
- Are all aliases documented?
- Is "signed vs unsigned" comparison semantics correct? (IF_LT vs IF_B, IF_GE vs IF_AE)
- Are truth tables accurate?

### 2. WC/WZ/WCZ EFFECTS (Chapter 2)
**Risk:** MEDIUM

Questions to validate:
- Do we correctly describe when WC/WZ are allowed?
- Do we correctly describe what each flag means for each instruction class?
- Are there special cases (like `_RET_` not restoring flags)?

### 3. ADDRESS MODES (Chapter 3)
**Risk:** MEDIUM

PTRx pointer modes to validate:
| Syntax | Behavior |
|--------|----------|
| PTRA | Use pointer, no modification |
| PTRA++ | Use pointer, post-increment |
| ++PTRA | Pre-increment, then use pointer |
| PTRA-- | Use pointer, post-decrement |
| --PTRA | Pre-decrement, then use pointer |
| PTRA[index] | Indexed addressing |
| PTRA[index]++ | Indexed with post-increment |

Are increment amounts correctly documented for each instruction (byte/word/long)?

### 4. AUGS/AUGD (Chapter 2)
**Risk:** MEDIUM

Questions:
- Is the automatic insertion behavior correctly described?
- Is the 32-bit immediate assembly correct?
- Are there timing implications documented?

### 5. REP BLOCK BEHAVIOR (Chapter 5)
**Risk:** MEDIUM

Questions:
- Is the instruction count limitation correct?
- Are nested REP restrictions documented?
- Is the timing calculation correct?
- What instructions are forbidden inside REP?

### 6. SKIP/SKIPF MECHANISM (Part II + Chapter 5)
**Risk:** LOW-MEDIUM

Questions:
- Is the bit pattern interpretation correct?
- Is the "cancellation" behavior documented?
- Are SKIP vs SKIPF differences clear?

### 7. MODCZ MNEMONICS (Appendix G)
**Risk:** LOW

| Mnemonic | Value | Usage |
|----------|-------|-------|
| _CLR | 0000 | Clear (same as _RET_) |
| _SET | 1111 | Set (always) |
| _NC | xxxx | Not carry |
| _NZ | xxxx | Not zero |
| _C | xxxx | Carry |
| _Z | xxxx | Zero |

Are all MODCZ operand mnemonics documented?

### 8. SPECIAL REGISTERS (Chapter 4)
**Risk:** LOW

| Register | Aliases | Special Behavior |
|----------|---------|------------------|
| PA | $1F8 | Used by LOC, CALLD, CALLPA |
| PB | $1F9 | Used by LOC, CALLD, CALLPB |
| PTRA | $1FA | Auto-increment pointer |
| PTRB | $1FB | Auto-increment pointer |
| DIRA | $1FC | Port A direction |
| DIRB | $1FD | Port B direction |
| OUTA | $1FE | Port A output |
| OUTB | $1FF | Port B output |

---

## Audit Methodology

### Phase 1: Cross-Reference Build
1. Extract all relevant sections from authoritative sources:
   - Silicon Documentation (p2-documentation.txt)
   - Parallax PASM2 Manual (pasm2-manual-narrative.txt)
   - P2 Instructions CSV v35
   - PNut-TS condition codes JSON

2. Build comparison matrix for each item

### Phase 2: Verification
For each item in scope:
1. Compare our manual text against all sources
2. Flag any discrepancies
3. Determine authoritative answer
4. Document required fix

### Phase 3: Fix Application
Apply fixes to:
- `opus-master/part-i/chapter-02-instruction-format.md`
- `opus-master/part-i/chapter-03-address-modes.md`
- `opus-master/part-i/chapter-04-memory-organization.md`
- `opus-master/part-i/chapter-05-hardware.md`
- `opus-master/part-iii/appendix-g-reserved-words.md`

---

## Estimated Effort

| Item | Estimated Time |
|------|---------------|
| Condition Prefixes (15 codes + aliases) | 1-2 hours |
| WC/WZ/WCZ Effects | 30 min |
| Address Modes (PTRx) | 1 hour |
| AUGS/AUGD | 30 min |
| REP Block | 30 min |
| SKIP/SKIPF | 30 min |
| MODCZ | 15 min |
| Special Registers | 30 min |
| **Total** | **5-6 hours** |

---

## Priority Recommendation

**HIGH**: Condition Prefixes - same category as _RET_, highest risk
**MEDIUM**: Address Modes, REP, WC/WZ/WCZ - commonly used, moderate complexity
**LOW**: MODCZ, Special Registers - rarely misunderstood

---

## Decision Needed

Should we proceed with this Part I Architectural Audit?

Options:
1. **Full audit** - Validate all items listed above
2. **High-priority only** - Focus on condition prefixes + address modes
3. **Defer** - Add to backlog for future session

---

*Proposal created in response to discovering `_RET_` critical error was missed by instruction-centric audit approach.*
