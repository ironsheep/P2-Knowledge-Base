# Cross-Reference Validation Report

**Document**: P2 Assembly Language (PASM2) Manual
**Generated**: 2025-11-29 02:16:25
**Status**: ⚠️ **1077 broken references found (54.7% failure rate)**

---

## Executive Summary

The assembled PASM2 Manual contains **1968 internal cross-references**, of which:

- ✅ **891 (45.3%) are VALID** - Link to existing anchors
- ❌ **1077 (54.7%) are BROKEN** - Link to non-existent anchors
- ⚠️ **0 warnings** - No near-miss typos detected

**Anchor Inventory**:
- 184 explicit anchors (headings with `{#id}` syntax)
- 744 implicit anchors (auto-generated from regular headings)
- **748 total unique anchors** available

---

## Problem Categories

### 1. 📚 Instruction Category Links (185 broken references)

**Problem**: References point to categorical instruction index pages that don't exist.

The manual uses links like `[Math Instruction](#math-instructions)` to categorize instructions, but there are no corresponding anchor targets.

**Most Common Missing Categories**:

| Category Anchor | References | Example Text |
|----------------|------------|--------------|
| `#event-instructions` | 39 | "Event Instruction" |
| `#math-instructions` | 31 | "Math Instruction" |
| `#io-pin-instructions` | 28 | "I/O Pin Instruction" |
| `#math-and-logic-instructions` | 22 | "Math and Logic Instruction" |
| `#branch-jump-instructions` | 15 | "Branch/Jump Instruction" |
| `#register-indirection-instructions` | 11 | "Register Indirection Instruction" |
| `#cog-control-instructions` | 8 | "COG Control Instruction" |
| `#misc-instructions` | 5 | "Misc Instruction" |
| `#pixel-mixer-instructions` | 4 | "Pixel Mixer Instruction" |
| `#logic-instructions` | 4 | "Logic Instruction" |

**Complete List of Missing Category Anchors**:
- `#branch-jump-instructions` (15 refs)
- `#cog-control-instructions` (8 refs)
- `#cordic-instructions` (2 refs)
- `#debug-instructions` (3 refs)
- `#event-instructions` (39 refs)
- `#flag-instructions` (3 refs)
- `#hub-fifo-instructions` (1 ref)
- `#hub-memory-instructions` (2 refs)
- `#interrupt-instructions` (2 refs)
- `#io-pin-instructions` (28 refs)
- `#logic-instructions` (4 refs)
- `#math-and-logic-instructions` (22 refs)
- `#math-instructions` (31 refs)
- `#misc-instructions` (5 refs)
- `#pixel-mixer-instructions` (4 refs)
- `#register-indirection-instructions` (11 refs)
- `#skip--skip-instructions` (1 ref)
- `#smart-pin-instructions` (2 refs)
- `#streamer-instructions` (1 ref)
- `#system-control-instructions` (1 ref)

**Recommended Fix**:
Either (a) create categorical index pages with these anchors, or (b) remove the category links from instruction descriptions.

---

### 2. 🔗 Missing Instruction References (926 broken references)

**Problem**: Instructions reference other instructions that aren't defined with explicit anchors.

The manual has 184 instruction anchors defined, but references 261 additional instruction names that don't have corresponding anchors.

**Top Missing Instructions** (by reference count):

| Instruction | References | Likely Location |
|------------|------------|-----------------|
| `#xcont` | 16 | X Instructions section |
| `#xinit` | 16 | X Instructions section |
| `#rdfast` | 11 | R Instructions section |
| `#qmul` | 11 | Q Instructions (CORDIC) |
| `#testb` | 11 | T Instructions section |
| `#testbn` | 11 | T Instructions section |
| `#setq` | 10 | S Instructions section |
| `#wrfast` | 9 | W Instructions section |
| `#rfbyte` | 9 | R Instructions section |
| `#waitxfi` | 9 | W Instructions section |
| `#pollct1` | 8 | P Instructions section |
| `#ret` | 8 | R Instructions section |
| `#tjz` | 8 | T Instructions section |
| `#tjnz` | 8 | T Instructions section |
| `#waitct1` | 7 | W Instructions section |
| `#pollct2` | 7 | P Instructions section |
| `#waitct2` | 7 | W Instructions section |
| `#pollct3` | 7 | P Instructions section |
| `#waitct3` | 7 | W Instructions section |
| `#wxpin` | 7 | W Instructions section |

**Additional Missing Instructions** (261 total unique):
241 more missing instruction anchors not shown above.

**Sample of Other Missing Instructions**:
- Event timing: `#jct1`, `#jct2`, `#jct3`, `#jnct1`, `#jnct2`, `#jnct3`
- I/O operations: `#dirnc`, `#dirnz`, `#drvnc`, `#drvnz`
- Subroutine control: `#reta`, `#retb`
- Math operations: `#sub`, `#subs`, `#subsx`, `#subx`, `#subpix`
- Smart pins: `#wrpin`, `#wypin`, `#rdpin`
- Data access: `#setbyte`, `#setnib`, `#setword`, `#rolbyte`, `#rolnib`, `#rolword`
- CORDIC: `#qdiv`, `#qexp`, `#qfrac`, `#qlog`, `#qrotate`, `#qsqrt`, `#qvector`
- Streamer: `#setxfrq`, `#xstop`, `#xzero`
- Pixel mixer: `#setpiv`, `#setpix`
- Skip operations: `#skip`, `#skipf`
- Stack operations: `#pop`, `#push`
- Interrupts: `#setint1`, `#setint2`, `#setint3`, `#trgint1`, `#trgint2`, `#trgint3`, `#stalli`
- CORDIC config: `#setcfrq`, `#setci`, `#setcmod`, `#setcq`, `#setcy`
- Register alteration: `#setd`, `#sets`, `#setr`
- Debug: `#setbrk`, `#getbrk`
- Bit testing: `#test`, `#testn`
- Logic: `#xor`
- Data movement: `#zerox`
- Encoding: `#rev`
- Timing: `#getct`, `#setq2`, `#waitx`

**Recommended Fix**:
Add explicit `{#anchor}` syntax to all instruction headings in Part II. Pattern should be:
```markdown
## INSTRUCTION {#instruction}
```

---

### 3. 🎛️ Special Register References (14 broken references)

**Problem**: Special registers referenced in instruction descriptions don't have anchor targets.

| Register | References | Description |
|----------|------------|-------------|
| `#pa` | 3 | Parameter A register |
| `#pb` | 3 | Parameter B register |
| `#ptra` | 4 | Pointer A register |
| `#ptrb` | 4 | Pointer B register |

**Recommended Fix**:
Add explicit anchors to special register definitions in the "Special Registers" section.

---

## Validation Statistics by Category

| Category | Checked | Valid | Broken | Success Rate |
|----------|---------|-------|--------|--------------|
| **Instruction** | 1784 | 891 | 893 | 49.9% |
| **Other** | 184 | 0 | 184 | 0.0% |
| **TOTAL** | 1968 | 891 | 1077 | 45.3% |

---

## Detailed Broken Reference List

### Sample of Broken References (First 50)

| Line | Reference Text | Target Anchor | Issue |
|------|---------------|---------------|-------|
| 165 | INSTRUCTION | `#instruction` | Anchor not found |
| 2314 | Math Instruction | `#math-instructions` | Anchor not found |
| 2351 | Math Instruction | `#math-instructions` | Anchor not found |
| 2367 | SUB | `#sub` | Anchor not found |
| 2391 | Event Instruction | `#event-instructions` | Anchor not found |
| 2406 | POLLCT1 | `#pollct1` | Anchor not found |
| 2406 | WAITCT1 | `#waitct1` | Anchor not found |
| 2419 | Event Instruction | `#event-instructions` | Anchor not found |
| 2434 | POLLCT2 | `#pollct2` | Anchor not found |
| 2434 | WAITCT2 | `#waitct2` | Anchor not found |
| 2447 | Event Instruction | `#event-instructions` | Anchor not found |
| 2462 | POLLCT3 | `#pollct3` | Anchor not found |
| 2462 | WAITCT3 | `#waitct3` | Anchor not found |
| 2475 | Pixel Mixer Instruction | `#pixel-mixer-instructions` | Anchor not found |
| 2490 | SUBPIX | `#subpix` | Anchor not found |
| 2505 | Math Instruction | `#math-instructions` | Anchor not found |
| 2521 | SUBS | `#subs` | Anchor not found |
| 2540 | Math Instruction | `#math-instructions` | Anchor not found |
| 2556 | SUBSX | `#subsx` | Anchor not found |
| 2573 | Math Instruction | `#math-instructions` | Anchor not found |
| 2589 | SUBX | `#subx` | Anchor not found |
| 2606 | Smart Pin Instruction | `#smart-pin-instructions` | Anchor not found |
| 2620 | WRPIN | `#wrpin` | Anchor not found |
| 2620 | WXPIN | `#wxpin` | Anchor not found |
| 2620 | WYPIN | `#wypin` | Anchor not found |
| 2620 | RDPIN | `#rdpin` | Anchor not found |
| 2639 | Interrupt Instruction | `#interrupt-instructions` | Anchor not found |
| 2651 | STALLI | `#stalli` | Anchor not found |
| 2664 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 2708 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 2746 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 2767 | ROLBYTE | `#rolbyte` | Anchor not found |
| 2788 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 2809 | ROLNIB | `#rolnib` | Anchor not found |
| 2830 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 2851 | ROLWORD | `#rolword` | Anchor not found |
| 2872 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 2891 | SETD | `#setd` | Anchor not found |
| 2891 | SETS | `#sets` | Anchor not found |
| 2891 | SETR | `#setr` | Anchor not found |
| 2910 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 2950 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 2988 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 3009 | SETBYTE | `#setbyte` | Anchor not found |
| 3028 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 3049 | SETNIB | `#setnib` | Anchor not found |
| 3070 | Register Indirection Instruction | `#register-indirection-instructions` | Anchor not found |
| 3091 | SETWORD | `#setword` | Anchor not found |
| 3112 | Logic Instruction | `#logic-instructions` | Anchor not found |
| 3128 | XOR | `#xor` | Anchor not found |

**Note**: Full list of 1077 broken references available in raw validation data.

---

## Current Anchor Inventory

**Successfully Defined Instruction Anchors** (184 total):

First 50 defined instructions:
- abs, add, addct1, addct2, addct3, addpix, adds, addsx, addx
- akpin, allowi, altb, altd, altgb, altgn, altgw, alti, altr, alts
- altsb, altsn, altsw, and, andn, asmclk, augd, augs
- bitc, bith, bitl, bitnc, bitnot, bitnz, bitrnd, bitz, blnpix, bmask, brk
- call, calla, callb, calld, callpa, callpb, cmp, cmpm, cmpr, cmps, cmpsub, cmpsx, cmpx
- cogatn, cogbrk, cogid

... and 134 more instructions properly defined with anchors.

---

## Recommendations

### 🔴 Critical Priority (Blocks Usability)

1. **Add Missing Instruction Anchors** (926 broken refs)
   - Scan Part II and add `{#instructionname}` to all instruction headings
   - Focus first on most-referenced: xcont, xinit, rdfast, qmul, testb, testbn, setq
   - Pattern: `## INSTRUCTIONNAME {#instructionname}`

2. **Resolve Category Link Strategy** (185 broken refs)
   - **Option A**: Create categorical index pages (e.g., "Math Instructions" landing page)
   - **Option B**: Remove category links from instruction descriptions
   - **Option C**: Link to Appendix B categorical index instead

### 🟡 Medium Priority (Improves Navigation)

3. **Add Special Register Anchors** (14 broken refs)
   - Add anchors to PA, PB, PTRA, PTRB definitions in Special Registers section

### ✅ Best Practices Going Forward

- Use explicit `{#anchor-id}` syntax for all cross-reference targets
- Keep anchor names lowercase and hyphen-separated
- Validate anchors exist before creating references to them
- Run this validation script before each release

---

## Validation Methodology

This report was generated by automated analysis that:

1. **Extracted all anchor definitions** from headings with `{#id}` syntax (184 explicit)
2. **Generated implicit anchors** from regular headings (744 auto-generated by markdown)
3. **Extracted all cross-references** in `[text](#anchor)` format (1968 total)
4. **Validated each reference** against available anchors
5. **Categorized failures** by pattern analysis

**Tools Used**:
- Python 3 regex pattern matching
- Markdown anchor auto-generation simulation
- Fuzzy string matching for typo detection (SequenceMatcher)

---

## Appendix: Validation Script

The validation can be re-run anytime using:

```bash
python3 /tmp/validate-cross-references.py
```

Script features:
- Detects explicit `{#anchor}` definitions
- Simulates markdown implicit anchor generation
- Fuzzy matching for near-miss typos
- Categorized reporting
- Actionable recommendations
