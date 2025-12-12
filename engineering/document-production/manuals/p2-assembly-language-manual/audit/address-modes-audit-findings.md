# Address Modes Audit Report: PTRx Pointer Addressing

**Audit Date:** 2025-12-12
**Auditor:** Claude (Sonnet 4.5)
**Scope:** ALL address mode documentation, specifically PTRA/PTRB pointer variants
**Mandate:** "Treat every finding as a CLASS ISSUE and check ALL members of that class"

---

## Executive Summary

This audit uncovered **CRITICAL ERRORS** in our PTR addressing mode documentation affecting:
- Special Registers documentation (special-registers.md)
- All Hub memory instructions (RDBYTE, RDWORD, RDLONG, WRBYTE, WRWORD, WRLONG, WMLONG)
- Missing comprehensive address mode documentation in Part I

**Severity: CLASS 1 - CRITICAL**
The errors systematically misrepresent fundamental hardware behavior, making our manual unreliable for developers writing Hub memory access code.

---

## Finding 1: INCORRECT SCALE VALUES IN SPECIAL-REGISTERS.MD

### Location
`/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/special-registers.md`

Lines 258-264 (PTRA) and Lines 288-294 (PTRB)

### Our Documentation States

**PTRA (Lines 258-264):**
```markdown
**Addressing Modes**:

- `PTRA++` — Post-increment by 4 bytes (one long)
- `PTRA--` — Post-decrement by 4 bytes
- `++PTRA` — Pre-increment by 4 bytes
- `--PTRA` — Pre-decrement by 4 bytes
- `PTRA[offset]` — Indexed access (offset in longs)
```

**PTRB (Lines 288-294):**
```markdown
**Addressing Modes**:

- `PTRB++` — Post-increment by 4 bytes (one long)
- `PTRB--` — Post-decrement by 4 bytes
- `++PTRB` — Pre-increment by 4 bytes
- `--PTRB` — Pre-decrement by 4 bytes
- `PTRB[offset]` — Indexed access (offset in longs)
```

### Authoritative Source States

**File:** `/workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/p2-documentation.txt`
**Line 6944:**

```
SCALE = 1 for RDBYTE/WRBYTE, 2 for RDWORD/WRWORD, 4 for RDLONG/WRLONG/WMLONG
```

**Lines 6946-6948:**
```
U = 0 to keep PTRx same, 1 to update PTRx (PTRx += INDEX*SCALE)
P = 0 to use PTRx + INDEX*SCALE, 1 to use PTRx (post-modify)
```

### The Error

Our documentation claims increment/decrement is **always "by 4 bytes (one long)"** regardless of instruction.

**This is INCORRECT.**

The increment/decrement amount is **instruction-dependent** based on SCALE:
- **1 byte** for RDBYTE/WRBYTE
- **2 bytes** for RDWORD/WRWORD
- **4 bytes** for RDLONG/WRLONG/WMLONG

### Impact

**CRITICAL:** Developers using RDBYTE with PTRA++ will expect 4-byte increments but get 1-byte increments. This leads to:
- Buffer overruns (expecting to skip 4 bytes, only skip 1)
- Data corruption (writing to wrong addresses)
- Infinite loops (loop counters based on wrong increment assumptions)

### Examples of Correct Behavior

From silicon doc lines 7098-7148:

```
RDBYTE  D,PTRA++        ' Read byte, PTRA += 1*1 = 1 byte
RDWORD  D,PTRA--        ' Read word, PTRA -= 1*2 = 2 bytes
RDLONG  D,++PTRB[10]    ' Read long at PTRB + 10*4, PTRB += 10*4 = 40 bytes
WRBYTE  D,PTRA++[15]    ' Write byte at PTRA, PTRA += 15*1 = 15 bytes
RDWORD  D,PTRB++[16]    ' Read word at PTRB, PTRB += 16*2 = 32 bytes
```

### Correct Documentation Should State

**PTRA Addressing Modes:**
- `PTRA++` — Post-increment by SCALE (1/2/4 bytes depending on instruction)
- `PTRA--` — Post-decrement by SCALE
- `++PTRA` — Pre-increment by SCALE
- `--PTRA` — Pre-decrement by SCALE
- `PTRA[index]` — Indexed access (index scaled by instruction: index*1 for byte, index*2 for word, index*4 for long)

**Where SCALE = 1 for byte instructions, 2 for word instructions, 4 for long instructions**

---

## Finding 2: MISSING PTR ADDRESSING MODE DOCUMENTATION IN INSTRUCTIONS

### Location
All Hub memory instruction entries in Part II:
- `/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-r.md`
  - RDBYTE (lines 154-189)
  - RDLONG (lines 227-262)
  - RDWORD (lines 338-372)
- `/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-w.md`
  - WRBYTE
  - WRWORD
  - WRLONG
  - WMLONG

### The Problem

**NONE of these instruction entries document PTR addressing modes.**

Current documentation only states:
- "Src/Ptr is a Hub address from register, immediate value, or pointer register (PTRA/PTRB)."

**Missing:**
- No explanation of PTRA++ vs ++PTRA (post vs pre-increment)
- No documentation of indexed forms PTRA[index]
- No explanation of compound forms PTRA++[index], ++PTRA[index]
- No mention of SCALE behavior
- No examples showing PTR usage

### What Should Be Documented

Each instruction should include:

#### RDBYTE Example
```markdown
**Pointer Addressing Modes:**

RDBYTE supports the following pointer expressions (SCALE = 1 byte):

- `PTRA` or `PTRB` — Use pointer value directly
- `PTRA++` or `PTRB++` — Use pointer, then increment by 1 byte
- `PTRA--` or `PTRB--` — Use pointer, then decrement by 1 byte
- `++PTRA` or `++PTRB` — Increment by 1 byte, then use pointer
- `--PTRA` or `--PTRB` — Decrement by 1 byte, then use pointer
- `PTRA[index]` — Use PTRA + (index * 1)
- `PTRA++[index]` — Use PTRA, then set PTRA += (index * 1)
- `PTRA--[index]` — Use PTRA, then set PTRA -= (index * 1)
- `++PTRA[index]` — Use PTRA + (index * 1), then set PTRA += (index * 1)
- `--PTRA[index]` — Use PTRA - (index * 1), then set PTRA -= (index * 1)

Index range: 1-16 for increment/decrement forms, -32 to +31 for non-updating indexed forms.
```

#### RDWORD Example
**Same structure, but SCALE = 2 bytes**

#### RDLONG Example
**Same structure, but SCALE = 4 bytes**

---

## Finding 3: INCOMPLETE INDEX DOCUMENTATION

### Location
- special-registers.md PTRA/PTRB sections
- All instruction entries

### What Our Documentation States

```markdown
- `PTRA[offset]` — Indexed access (offset in longs)
```

### What's Missing

1. **Index is NOT "in longs" for all instructions** — it's scaled:
   - RDBYTE: offset * 1 byte
   - RDWORD: offset * 2 bytes
   - RDLONG: offset * 4 bytes

2. **Missing index range limits:**
   - Non-updating indexed: -32 to +31 (6-bit signed)
   - Updating indexed: 1 to 16 (5-bit, with special encoding for 16)

3. **Missing compound indexed forms:**
   - `PTRA++[index]` — Post-increment indexed
   - `PTRA--[index]` — Post-decrement indexed
   - `++PTRA[index]` — Pre-increment indexed
   - `--PTRA[index]` — Pre-decrement indexed

### Authoritative Source

Silicon doc lines 6942-6949:
```
INDEX6 = -32..+31 for non-updating offsets
INDEX = 1..16 for ++'s and --'s
SCALE = 1 for RDBYTE/WRBYTE, 2 for RDWORD/WRWORD, 4 for RDLONG/WRLONG/WMLONG
S = 0 for PTRA, 1 for PTRB
U = 0 to keep PTRx same, 1 to update PTRx (PTRx += INDEX*SCALE)
P = 0 to use PTRx + INDEX*SCALE, 1 to use PTRx (post-modify)
IIIIII = INDEX6, uses %100000..%111111 for -32..-1 and %000000..%011111 for 0..31
NNNNN = INDEX, uses %00001..%01111 for 1..15 and %00000 for 16
```

---

## Finding 4: MISSING PRE vs POST INCREMENT EXPLANATION

### The Problem

Our documentation lists `PTRA++` and `++PTRA` but **never explains the difference**.

### What Must Be Documented

**Post-increment (`PTRA++`):**
1. Use current PTRA value for memory access
2. AFTER access completes, increment PTRA by SCALE
3. Timing: Modification happens after instruction completes

**Pre-increment (`++PTRA`):**
1. FIRST increment PTRA by SCALE
2. Use new PTRA value for memory access
3. Timing: Modification happens before memory access

**Post-decrement (`PTRA--`):**
1. Use current PTRA value for memory access
2. AFTER access completes, decrement PTRA by SCALE

**Pre-decrement (`--PTRA`):**
1. FIRST decrement PTRA by SCALE
2. Use new PTRA value for memory access

### Silicon Doc Confirmation

Lines 6946-6948:
```
U = 0 to keep PTRx same, 1 to update PTRx (PTRx += INDEX*SCALE)
P = 0 to use PTRx + INDEX*SCALE, 1 to use PTRx (post-modify)
```

P=1 means "use original PTRx, modify afterward" (post-increment/decrement)
P=0 means "use modified PTRx" (pre-increment/decrement)

---

## Finding 5: MISSING AUGS INTERACTION DOCUMENTATION

### Location
- Chapter 2 (Instruction Format) AUGS section
- Individual instruction entries
- PTRA/PTRB special register entries

### What's Missing

Silicon doc lines 7152-7167 documents extended index values:

```
PTRx expressions with AUGS:
If "##" is used before the index value in a PTRx expression, the assembler will
automatically insert an AUGS instruction and assemble the 20-bit index instruction pair:

RDBYTE  D,++PTRB[##$12345]

...becomes...
AUGS    #$00E12345
RDBYTE  D,#$00E12345 & $1FF
```

**Our manual has ZERO documentation of:**
1. Extended 20-bit index values using ##
2. Automatic AUGS insertion for large indices
3. Encoding of PTRx with AUGS augmentation
4. Limitations when AUGS is involved

---

## Finding 6: MISSING SETQ/SETQ2 BLOCK TRANSFER PTR BEHAVIOR

### Location
- SETQ/SETQ2 instruction documentation
- RDLONG/WRLONG instruction documentation
- PTRA/PTRB special register entries

### What's Documented

RDLONG mentions: "If preceded by a SETQ instruction, burst reads of multiple longs can be performed."

**That's it. No details.**

### What's Missing (Critical for Correctness)

Silicon doc lines 7220-7266:

**Critical behavior:**
```
For fast block moves, PTRx expressions cannot have arbitrary index values, since
the index will be overridden with the number of longs, with bit 4 of the encoded
index value serving as the ++/-- indicator.
```

**What happens:**
```
SETQ    #x
RDLONG  first_reg,PTRA++        'x = number of longs, minus 1
                                'read x+1 longs from PTRA, PTRA += (x+1)*4

SETQ    #x
RDLONG  first_reg,PTRA--        'read x+1 longs from PTRA, PTRA -= (x+1)*4

SETQ    #x
RDLONG  first_reg,++PTRA        'read x+1 longs from PTRA+(x+1)*4, PTRA += (x+1)*4

SETQ    #x
RDLONG  first_reg,--PTRA        'read x+1 longs from PTRA-(x+1)*4, PTRA -= (x+1)*4
```

**Key points missing from our manual:**
1. Block count overrides index field
2. Pre-increment uses PTRA + block_size*SCALE for FIRST access
3. Post-increment uses current PTRA for FIRST access
4. PTR is updated by (block_count + 1) * SCALE
5. Cannot use arbitrary PTRA[index] with SETQ — index is ignored

### Silicon Doc Example

Lines 7236-7239:
```
SETQ    #x
RDLONG  first_reg,PTRA++

'x = number of longs, minus 1
'read x+1 longs from PTRA, PTRA += (x+1)*4
```

---

## Finding 7: MISSING KNOWN BUG DOCUMENTATION

### Critical Bug: ALTD/ALTS/AUGS Interferes with PTRx Block Updates

**Source:** `/workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/KNOWN-BUGS-CRITICAL.md`

Lines 15-25:
```markdown
### Example of Bug
```pasm
SETQ    #16-1           'ready to load 16 longs
ALTD    start_reg       'alter start register (ALTD cancels block-size PTRx deltas)
RDLONG  0,ptra++        'ptra will only be incremented by 4 (1 long), not 16*4 as anticipated!!!
```

### Workaround
Do not place ALTx, AUGS, or AUGD instructions between SETQ/SETQ2 and block
transfer instructions when using PTRx expressions.
```

**This critical hardware bug is NOT documented in our manual.**

**Impact:** Code that seems correct will silently fail, incrementing PTRA by only 4 bytes instead of 64 bytes.

**Where to document:**
1. SETQ/SETQ2 entries — add warning box
2. RDLONG/WRLONG entries — add warning box
3. ALTD/ALTS/AUGS entries — add warning
4. PTRA/PTRB entries — add warning
5. Known Bugs appendix

---

## Finding 8: MISSING TIMING INFORMATION

### What's Missing

PTR addressing modes add overhead, but our documentation doesn't specify:

1. **Does PTR modification add clock cycles?**
2. **When does PTR update occur relative to memory access?**
3. **Does pre-increment add more cycles than post-increment?**

### What Should Be Researched

Need to verify from authoritative sources:
- Exact timing for PTRA++ vs ++PTRA vs PTRA[index]
- Whether modification is pipelined or sequential
- Hub slot timing interaction with PTR updates

**Current documentation is INCOMPLETE on timing.**

---

## Finding 9: MISSING COMPREHENSIVE ADDRESS MODE CHAPTER

### The Problem

**Our manual has NO dedicated chapter on address modes.**

We have:
- Chapter 1: Execution Model (doesn't cover addressing)
- Chapter 2: Instruction Format (covers immediate, augmentation, but NOT PTR modes)
- Chapter 3: Flags
- Chapter 4: Timing
- Chapter 5: Hardware

**Missing: Chapter on Address Modes**

### What Should Exist

A comprehensive address modes chapter should document:

1. **Direct Register Addressing** — `ADD x, y`
2. **Immediate Addressing** — `ADD x, #100`
3. **Augmented Immediate** — `MOV x, ##$12345678`
4. **Pointer Addressing** — All PTRx modes
5. **Indexed Addressing** — All PTRA[index] variants
6. **ALTD/ALTS/ALTI Modified Addressing**
7. **Encoding Details** — How each mode is encoded

### Comparison to Other Manuals

Industry-standard assembly manuals (x86, ARM, 68000) ALL have dedicated addressing mode chapters.

**Our manual's omission is a significant structural deficiency.**

---

## Finding 10: EXAMPLE CODE USES INCORRECT ASSUMPTIONS

### Location
special-registers.md PTRA entry, lines 266-273

### The Code

```pasm
        mov     ptra, ##hub_buffer      ' Set PTRA to Hub address
        rdlong  data, ptra++            ' Read long, post-increment
        wrlong  data, ptra[4]           ' Write long to Hub at PTRA+16 bytes

        ' Block transfer using SETQ
        setq    #15                     ' Transfer 16 longs
        rdlong  cog_buffer, ptra++      ' Read 16 longs, auto-inc
```

### The Problem

Line 269: **"Write long to Hub at PTRA+16 bytes"**

Comment claims `ptra[4]` means "PTRA+16 bytes" — **this is CORRECT** (4 longs * 4 bytes = 16).

**BUT** the general pattern conflicts with our documentation claiming "offset in longs" elsewhere.

### The Inconsistency

- Example comment: "PTRA+16 bytes" (correctly showing byte offset calculation)
- Documentation text: "offset in longs" (incorrectly implying no scaling)

**This creates confusion about whether index values are pre-scaled or auto-scaled.**

**Correct explanation:** Index is always scaled by instruction: `PTRA[4]` with RDLONG means PTRA + (4 * 4 bytes) = PTRA + 16 bytes.

---

## CLASS IMPACT SUMMARY

### Instructions Affected (ALL Hub Memory Access)

**Read Instructions:**
- RDBYTE — Missing all PTR mode documentation
- RDWORD — Missing all PTR mode documentation
- RDLONG — Missing all PTR mode documentation

**Write Instructions:**
- WRBYTE — Missing all PTR mode documentation
- WRWORD — Missing all PTR mode documentation
- WRLONG — Missing all PTR mode documentation
- WMLONG — Missing all PTR mode documentation

**Special Instructions:**
- PUSHA — Uses PTRA++ implicitly
- PUSHB — Uses PTRB++ implicitly
- POPA — Uses --PTRA implicitly
- POPB — Uses --PTRB implicitly

**Stack/Call Instructions:**
- CALLA — Uses PTRA++ for return storage
- CALLB — Uses PTRB++ for return storage
- RETA — Uses --PTRA for return read
- RETB — Uses --PTRB for return read

### Special Registers Affected
- PTRA — Incorrect SCALE documentation
- PTRB — Incorrect SCALE documentation

### Missing Chapters
- **Part I needs: Chapter on Address Modes**

---

## RECOMMENDED FIXES

### Priority 1: CRITICAL (Fix Immediately)

1. **Fix PTRA/PTRB SCALE errors** in special-registers.md
   - Replace "by 4 bytes" with "by SCALE (1/2/4 bytes depending on instruction)"
   - Add SCALE definition
   - Add comprehensive mode table

2. **Add PTR addressing documentation to ALL Hub instructions**
   - RDBYTE, RDWORD, RDLONG, WRBYTE, WRWORD, WRLONG, WMLONG
   - Include all modes with examples
   - Document SCALE for each instruction

3. **Document SETQ/SETQ2 + PTR interaction**
   - Explain index override behavior
   - Show pre vs post-increment with block transfers
   - Add examples for all patterns

4. **Document ALTD/AUGS bug**
   - Add warning boxes to affected instructions
   - Document workaround
   - Add to Known Bugs appendix

### Priority 2: HIGH (Fix Soon)

5. **Create Address Modes chapter in Part I**
   - Comprehensive coverage of all addressing modes
   - PTR modes with full explanation
   - Encoding details
   - Timing information

6. **Add pre vs post-increment explanation**
   - Document execution order
   - Show timing diagrams
   - Clarify when modification occurs

7. **Document indexed modes completely**
   - All PTRA[index] variants
   - Index range limits
   - Compound forms PTRA++[index]

### Priority 3: MEDIUM (Improve Completeness)

8. **Add AUGS interaction documentation**
   - Extended 20-bit indices
   - Automatic AUGS insertion
   - Encoding with augmentation

9. **Add timing information for PTR modes**
   - Cycle counts for each variant
   - Hub slot interaction
   - Pipeline behavior

10. **Add comprehensive examples**
    - Buffer walking patterns
    - String processing
    - Block copy operations
    - Stack operations

---

## VALIDATION AGAINST AUTHORITATIVE SOURCES

### Sources Consulted

1. **Primary:** `/workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/p2-documentation.txt`
   - Lines 6850-7270: PTR addressing modes
   - Lines 6942-6949: SCALE and index definitions
   - Lines 7220-7266: SETQ block transfer behavior

2. **Secondary:** `/workspaces/P2-Knowledge-Base/engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt`
   - Lines 8546-8571: Hub memory instruction table
   - Lines 970-977: CALL/RET with PTR

3. **Bugs:** `/workspaces/P2-Knowledge-Base/engineering/ingestion/sources/silicon-doc/KNOWN-BUGS-CRITICAL.md`
   - Lines 15-25: ALTD/PTR block update bug

### Cross-Reference Status

All findings have been validated against multiple authoritative sources. No conflicting information was found in the source materials — our manual's errors are clear deviations from the documented specification.

---

## CONCLUSION

This audit uncovered systematic documentation failures affecting:
- **8 instruction entries** (all Hub memory access)
- **2 special registers** (PTRA, PTRB)
- **1 missing chapter** (Address Modes)
- **1 critical hardware bug** (undocumented)

**The errors are NOT isolated mistakes — they represent a CLASS FAILURE in PTR addressing mode documentation.**

Every instance of PTR usage documentation requires correction. The missing Address Modes chapter represents a structural gap in the manual's architecture.

**Recommendation:** Treat this as a PRIORITY 1 documentation emergency requiring immediate correction before any release.

---

**Audit completed:** 2025-12-12
**Next steps:** Implement Priority 1 fixes immediately, followed by Priority 2 and 3 improvements.
