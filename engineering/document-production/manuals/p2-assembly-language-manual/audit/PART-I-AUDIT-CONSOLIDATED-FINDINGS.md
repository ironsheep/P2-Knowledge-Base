# Part I Architectural Audit - Consolidated Findings

**Audit Date:** 2025-12-12
**Triggered By:** `_RET_` critical error discovery
**Approach:** Multi-agent parallel audit treating every finding as a CLASS ISSUE
**Status:** COMPLETE

---

## Sources Consulted

| Source | Location | Used For |
|--------|----------|----------|
| P2 Instructions CSV v35 | `engineering/ingestion/sources/p2-instructions-csv/` | Condition codes, encodings |
| Silicon Documentation v35 | `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` | PTR modes, REP, SKIP, XBYTE |
| PASM2 Manual (Parallax) | `engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt` | Flags, AUGS/AUGD, syntax |
| PNut-TS JSON | `engineering/ingestion/sources/pnut-ts-pasm-ref/PASM2-Condition-Codes.json` | Condition code validation |
| Known Bugs | `engineering/ingestion/sources/silicon-doc/KNOWN-BUGS-CRITICAL.md` | Hardware bugs |

---

## Executive Summary

### Issue Counts

| Severity | Count | Examples |
|----------|-------|----------|
| **CRITICAL** | 11 | IF_NC/IF_C wrong semantics, SCALE errors, missing MODCZ table |
| **MAJOR** | 11 | Missing aliases, missing PTR docs, timing info |
| **MINOR** | 7 | Enhanced examples, cross-references |
| **Missing Items** | 36+ | Condition aliases, instruction PTR modes |

### Root Cause

The original 357-instruction audit was **instruction-centric** and did not audit:
- Part I architectural concepts (Chapter 2-5)
- Condition prefixes (not instructions)
- Address mode documentation
- Hardware mechanisms (REP, SKIP/SKIPF)

---

## Detailed Findings By Category

### 1. Condition Prefixes (Chapter 2)

**Audit Report:** `condition-prefix-audit-findings.md`

#### Critical Errors (2)

| Code | Condition | Our Manual Says | Should Say |
|------|-----------|-----------------|------------|
| 0011 | IF_NC | "unsigned less than" | "greater than or equal" (signed GE, unsigned AE) |
| 1100 | IF_C | "unsigned greater than or equal" | "less than" (signed LT, unsigned B) |

#### Missing Aliases (36 total)

| Code | Primary | Missing Aliases |
|------|---------|-----------------|
| 0001 | IF_NC_AND_NZ | IF_NZ_AND_NC, IF_GT, IF_A, IF_00 |
| 0010 | IF_NC_AND_Z | IF_Z_AND_NC, IF_01 |
| 0011 | IF_NC | IF_GE, IF_AE, IF_0X |
| 0100 | IF_C_AND_NZ | IF_NZ_AND_C, IF_10 |
| 0101 | IF_NZ | IF_NE, IF_X0 |
| 0110 | IF_C_NE_Z | IF_Z_NE_C, IF_DIFF |
| 0111 | IF_NC_OR_NZ | IF_NZ_OR_NC, IF_NOT_11 |
| 1000 | IF_C_AND_Z | IF_Z_AND_C, IF_11 |
| 1001 | IF_C_EQ_Z | IF_Z_EQ_C, IF_SAME |
| 1010 | IF_Z | IF_E, IF_X1 |
| 1011 | IF_NC_OR_Z | IF_Z_OR_NC, IF_NOT_10 |
| 1100 | IF_C | IF_LT, IF_B, IF_1X |
| 1101 | IF_C_OR_NZ | IF_NZ_OR_C, IF_NOT_01 |
| 1110 | IF_C_OR_Z | IF_Z_OR_C, IF_LE, IF_BE, IF_NOT_00 |

#### Additional Issue: IF_NEVER

`IF_NEVER` is documented in our manual but **DOES NOT EXIST** in P2.
- In P1: EEEE=0000 meant "if_never" (never execute)
- In P2: EEEE=0000 became `_RET_` (execute, then return)

**Files containing IF_NEVER that need correction:**
- `chapter-03-flags.md` (line 159)
- `appendix-g-reserved-words.md` (lines 98, 450)

---

### 2. Address Modes (PTRx Pointers)

**Audit Report:** `address-modes-audit-findings.md`

#### Critical Errors (4)

1. **PTRA/PTRB SCALE Documentation WRONG**
   - Our manual says: "Post-increment by 4 bytes (one long)"
   - Correct: SCALE = 1 for byte, 2 for word, 4 for long (instruction-dependent)
   - Location: `special-registers.md` lines 258-264, 288-294

2. **Missing PTR Mode Documentation**
   - 8 hub instructions lack ALL PTR addressing mode documentation
   - Affected: RDBYTE, RDWORD, RDLONG, WRBYTE, WRWORD, WRLONG, WMLONG

3. **Missing Address Modes Chapter**
   - Part I has NO dedicated chapter on address modes
   - Industry-standard assembly manuals all have this

4. **Missing SETQ Block Transfer PTR Behavior**
   - Index override behavior not documented
   - Pre vs post-increment with block transfers not explained

#### Undocumented Hardware Bug

**ALTD/AUGS/PTR Bug:**
```pasm
SETQ    #16-1           ' Ready to load 16 longs
ALTD    start_reg       ' ALTD CANCELS block-size PTRx deltas!
RDLONG  0,ptra++        ' PTRA only incremented by 4, NOT 64!
```

**Workaround:** Do not place ALTx, AUGS, or AUGD between SETQ/SETQ2 and block transfer instructions when using PTRx expressions.

---

### 3. Flags and Augmentation (WC/WZ/WCZ, AUGS/AUGD)

**Audit Report:** `flags-and-augmentation-audit-findings.md`

**Status:** Mostly correct with gaps

#### Missing Information

| Item | Status | Fix Needed |
|------|--------|------------|
| CZI field encoding | ✅ CORRECT | None |
| WC/WZ/WCZ behavior | ✅ CORRECT | None |
| AUGS/AUGD encoding | ✅ CORRECT | None |
| **AUGS/AUGD timing** | ❌ MISSING | Add "+2 cycles" overhead |
| **Special flag effects** | ❌ MISSING | Add ANDC/ANDZ/ORC/ORZ/XORC/XORZ |
| **Extended Z flag behavior** | ❌ MISSING | Add "Z = Z AND (result==0)" for ADDX etc. |
| **9-bit immediate signedness** | ⚠️ UNCLEAR | Clarify always unsigned (0-511) |

---

### 4. Hardware Mechanisms (REP, SKIP/SKIPF, MODCZ, Registers)

**Audit Report:** `hardware-mechanisms-audit-findings.md`

#### REP Block Behavior

| Item | Status | Severity |
|------|--------|----------|
| Branch cancellation | ❌ NOT DOCUMENTED | **CRITICAL** |
| Hub vs cog overhead | ❌ NOT DOCUMENTED | **CRITICAL** |
| Instruction count (0-511) | ✅ CORRECT | — |
| Nesting depth (3 levels) | ✅ CORRECT | — |

**Critical Missing Warning:**
> "Any branch within the repeating instruction block will cancel REP activity."

#### SKIP/SKIPF Mechanism

| Item | Status | Severity |
|------|--------|----------|
| Pattern interpretation | ⚠️ INCOMPLETE | **CRITICAL** |
| SKIPF cog/LUT-only | ❌ NOT DOCUMENTED | **CRITICAL** |
| Hub SKIPF fallback | ❌ NOT DOCUMENTED | **CRITICAL** |
| REP compatibility | ❌ NOT DOCUMENTED | MAJOR |

**Critical Missing Warning:**
> "SKIPF can ONLY leap over instructions in cog/LUT memory. In hub, it reverts to SKIP behavior."

#### MODCZ Mnemonics

| Item | Status | Severity |
|------|--------|----------|
| Complete mnemonic table | ❌ MISSING | **CRITICAL** |
| Mnemonic listing | ✅ EXISTS | — |
| MODCZ mechanism | ✅ CORRECT | — |

**Required Table (16 mnemonics with 4-bit values):**
- _CLR (0000), _SET (1111), _C (1100), _Z (1010), _NC (0011), _NZ (0101)
- All compound forms: _C_AND_Z, _C_OR_Z, _NC_AND_NZ, etc.

#### Special Registers

| Item | Status | Severity |
|------|--------|----------|
| Addresses $1F0-$1FF | ✅ CORRECT | — |
| INA/INB debug usage | ⚠️ UNCLEAR | MODERATE |
| $1FF XBYTE behavior | ⚠️ PARTIAL | MODERATE |

---

## Fix Priority Matrix

### Priority 1: CRITICAL (Immediate)

1. Fix IF_NC description ("less than" → "greater than or equal")
2. Fix IF_C description ("greater than or equal" → "less than")
3. Remove IF_NEVER from documentation (doesn't exist in P2)
4. Fix PTRA/PTRB SCALE documentation (instruction-dependent, not always 4)
5. Add REP branch cancellation warning
6. Add SKIPF cog/LUT-only restriction
7. Add complete MODCZ mnemonic table
8. Document ALTD/AUGS/PTR hardware bug

### Priority 2: MAJOR (High)

9. Add all 36 missing condition aliases
10. Add PTR mode documentation to 8 hub instructions
11. Add signed vs unsigned comparison explanation
12. Add AUGS/AUGD timing (+2 cycles)
13. Add REP hub memory hidden jump note
14. Add SKIP pattern interpretation clarification
15. Add extended instruction Z flag behavior (Z AND)

### Priority 3: MODERATE (Medium)

16. Create Address Modes chapter for Part I
17. Add SETQ block transfer PTR behavior
18. Add special flag effects (ANDC/ANDZ/ORC/ORZ/XORC/XORZ)
19. Enhance INA/INB debug interrupt documentation
20. Add INB to XBYTE cross-reference
21. Add SKIP/SKIPF REP compatibility notes

---

## Files Requiring Modification

### Part I: Architecture

| File | Changes Needed |
|------|----------------|
| `chapter-02-instruction-format.md` | Condition codes, AUGS timing |
| `chapter-03-flags.md` | Remove IF_NEVER, add flag effects |
| NEW: `chapter-0X-address-modes.md` | Create comprehensive address modes chapter |

### Part II: Instruction Reference

| File | Changes Needed |
|------|----------------|
| `special-registers.md` | Fix PTRA/PTRB SCALE, add debug info |
| `instructions-r.md` | Add PTR modes to RDBYTE/RDWORD/RDLONG, REP branch warning |
| `instructions-w.md` | Add PTR modes to WRBYTE/WRWORD/WRLONG/WMLONG |
| `instructions-s.md` | SKIP pattern clarification, SKIPF hub restriction |

### Part III: Appendices

| File | Changes Needed |
|------|----------------|
| `appendix-g-reserved-words.md` | Remove IF_NEVER, add MODCZ table |

---

## Verification Completed

All findings cross-referenced against:
- ✅ P2 Instructions CSV v35 (line numbers cited)
- ✅ Silicon Documentation v35 (line numbers cited)
- ✅ PASM2 Manual narrative (line numbers cited)
- ✅ PNut-TS condition codes JSON
- ✅ Known Bugs documentation

---

## Audit Completion Statement

This audit examined ALL non-instruction architectural documentation in Part I of the P2 Assembly Language Manual. The audit methodology treated each finding as a CLASS ISSUE, checking all members of each class for similar problems.

**Confidence Level:** HIGH - All findings verified against multiple authoritative sources.

**Next Step:** Apply fixes according to priority matrix.

---

*Audit completed 2025-12-12 by Claude Opus 4.5 with 4 parallel specialized agents.*
