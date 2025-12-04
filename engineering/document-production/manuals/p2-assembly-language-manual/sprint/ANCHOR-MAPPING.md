# Anchor Mapping Reference

**Sprint:** Instruction Block Retrofit
**Created:** 2025-12-04

---

## Anchor Types

The P2 Assembly Language Manual uses three types of anchors:

### 1. Instruction Name Anchors
Defined in instruction entry headers using `{#anchor}` syntax.
- Example: `## ABS {#abs}`
- Total: ~280 unique instruction anchors

### 2. Category Group Anchors
Defined in `instruction-categories.md` for the 17 instruction categories.
- Example: `## Math and Logic {#math-and-logic}`
- Display text uses proper English (spaces, title case)
- Anchor uses lowercase with hyphens

### 3. Special Register Anchors
Defined in `special-registers.md` for hardware registers using explicit `{#anchor}` syntax.
- Example: `### PA {#pa}` → anchor is `#pa`
- Table anchor: `#special-registers-map` → links to the memory map table
- All 16 memory-mapped registers have explicit anchors: `#ijmp1`, `#ijmp2`, `#ijmp3`, `#iret1`, `#iret2`, `#iret3`, `#pa`, `#pb`, `#ptra`, `#ptrb`, `#dira`, `#dirb`, `#outa`, `#outb`, `#ina`, `#inb`

---

## Category Anchors (17 Total)

All categories use proper English display text with hyphenated anchors:

| Display Text | Anchor |
|--------------|--------|
| Branch | `#branch` |
| CORDIC Solver | `#cordic-solver` |
| Color Space Converter | `#color-space-converter` |
| Event | `#event` |
| Hub Control | `#hub-control` |
| Hub FIFO | `#hub-fifo` |
| Hub RAM | `#hub-ram` |
| Interrupt | `#interrupt` |
| Lookup Table | `#lookup-table` |
| Math and Logic | `#math-and-logic` |
| Miscellaneous | `#miscellaneous` |
| Pin | `#pin` |
| Pixel Mixer | `#pixel-mixer` |
| Register Indirection | `#register-indirection` |
| Smart Pin | `#smart-pin` |
| Streamer | `#streamer-category` |
| System Control | `#system-control` |

---

## Multi-Instruction Blocks

Some entries document multiple related instructions in a single block. Only the primary instruction gets an anchor; secondary instructions should link to that primary anchor.

### Confirmed Multi-Instruction Blocks

| Block Title | Primary Anchor | Secondary Instructions |
|-------------|----------------|----------------------|
| ADDCT1 / ADDCT2 / ADDCT3 | `#addct1` | ADDCT2, ADDCT3 |
| DIRC / DIRNC | `#dirc` | DIRNC |
| DIRZ / DIRNZ | `#dirz` | DIRNZ |
| DRVC / DRVNC | `#drvc` | DRVNC |
| DRVZ / DRVNZ | `#drvz` | DRVNZ |
| JCT1 / JCT2 / JCT3 | `#jct1` | JCT2, JCT3 |
| POLLCT1 / POLLCT2 / POLLCT3 | `#pollct1` | POLLCT2, POLLCT3 |
| POLLSE1 / POLLSE2 / POLLSE3 / POLLSE4 | `#pollse1` | POLLSE2, POLLSE3, POLLSE4 |
| WAITCT1 / WAITCT2 / WAITCT3 | `#waitct1` | WAITCT2, WAITCT3 |
| WAITSE1 / WAITSE2 / WAITSE3 / WAITSE4 | `#waitse1` | WAITSE2, WAITSE3, WAITSE4 |

---

## Broken Anchor References (To Fix)

These references point to anchors that don't exist and must be corrected:

| Broken Reference | Correct Anchor | Reason |
|------------------|----------------|--------|
| `#addct2` | `#addct1` | Secondary in multi-block |
| `#addct3` | `#addct1` | Secondary in multi-block |
| `#dirnc` | `#dirc` | Secondary in multi-block |
| `#dirnz` | `#dirz` | Secondary in multi-block |
| `#drvnc` | `#drvc` | Secondary in multi-block |
| `#drvnz` | `#drvz` | Secondary in multi-block |
| `#jct2` | `#jct1` | Secondary in multi-block |
| `#jct3` | `#jct1` | Secondary in multi-block |
| `#pollatt` | `#pollatn` | Typo (ATT vs ATN) |
| `#pollct2` | `#pollct1` | Secondary in multi-block |
| `#pollct3` | `#pollct1` | Secondary in multi-block |

### References to Non-Instruction Anchors (Researched Fixes)

Based on contextual analysis of where each broken reference appears:

| Broken Reference | Location | Correct Fix | Reason |
|------------------|----------|-------------|--------|
| `#subpix` | ADDPIX Related, BLNPIX Related | **REMOVE** | No SUBPIX instruction exists. PIX family is: ADDPIX, BLNPIX, MIXPIX, MULPIX, SETPIX. SUBPIX was likely placeholder or confusion. |
| `#setbrk` | GETBRK Related | **REMOVE** | No SETBRK instruction exists. BRK family is: BRK, GETBRK, COGBRK. The breakpoint is set via BRK instruction, not SETBRK. |
| `#clkset` | ASMCLK Related, HUBSET Related | **REMOVE** | CLKSET is a Spin2 method, not PASM2 instruction. ASMCLK and HUBSET handle clock configuration in PASM2. |
| `#ijmp` | JMPREL Related | `[IJMP1](special-registers.md#ijmp1)` | IJMP is not an instruction - it's a special register. IJMP1/2/3 are interrupt jump address registers at $1F0-$1F5. Link to special registers. |
| `#waitcnt` | NOP Related | `[WAITCT1](instructions-w.md#waitct1)` | WAITCNT was P1 instruction. P2 uses WAITCT1/WAITCT2/WAITCT3 for counter-based waits. |
| `#pa` | (various CALL instructions) | `[PA](special-registers.md#pa)` | PA is a special register at $1F6, not an instruction. Cross-file link to special-registers.md. |
| `#pb` | (various CALL instructions) | `[PB](special-registers.md#pb)` | PB is a special register at $1F7, not an instruction. Cross-file link to special-registers.md. |
| `#ptra` | (various memory instructions) | `[PTRA](special-registers.md#ptra)` | PTRA is a special register at $1F8, not an instruction. Cross-file link to special-registers.md. |
| `#ptrb` | (various memory instructions) | `[PTRB](special-registers.md#ptrb)` | PTRB is a special register at $1F9, not an instruction. Cross-file link to special-registers.md. |

### Fix Actions Summary

| Action | Count | References |
|--------|-------|------------|
| **REMOVE** | 3 | #subpix, #setbrk, #clkset |
| **Link to special-registers.md** | 5 | #ijmp→#ijmp1, #pa, #pb, #ptra, #ptrb |
| **Fix typo** | 1 | #waitcnt→#waitct1 |
| **Fix multi-block** | 11 | #addct2/3, #dirnc, #dirnz, #drvnc, #drvnz, #jct2/3, #pollatt, #pollct2/3 |

---

## Audit Summary

- **Category anchors**: ✅ All 17 correctly formatted
- **Instruction anchors**: ~280 defined with explicit `{#anchor}` syntax
- **Special register anchors**: ✅ 16 explicit anchors added to special-registers.md
- **Broken references**: 20 identified, all fixes determined
- **Category display text**: ✅ All use proper English

---

*Generated: 2025-12-04*
*Updated: 2025-12-04 - Completed broken anchor research*
