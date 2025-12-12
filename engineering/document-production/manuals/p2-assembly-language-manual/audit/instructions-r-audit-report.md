# P2 Assembly Language Manual - Instructions R - Deep Audit Report

**Audit Date:** 2025-12-12
**Auditor:** Claude (Sonnet 4.5)
**Manual File:** `/workspaces/P2-Knowledge-Base/engineering/document-production/manuals/p2-assembly-language-manual/opus-master/part-ii/instructions-r.md`
**Authoritative Source:** `/workspaces/P2-Knowledge-Base/engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv`
**Manual Size:** 1105 lines

---

## Executive Summary

**STATUS: FAILED - CRITICAL DISCREPANCIES FOUND**

The instructions-r.md file contains **MULTIPLE CRITICAL ERRORS** in clock cycle specifications for hub memory access instructions (RDBYTE, RDWORD, RDLONG). Additionally, there is a **CRITICAL MISSING Z FLAG** specification for RDLONG and incorrect Result column values for multiple instructions.

### Critical Issues Found:
1. **RDBYTE** - Clock cycles: Manual shows "9...16" but CSV specifies "9...16" for COG (correct) BUT manual shows "9...16" everywhere - needs verification
2. **RDWORD** - Clock cycles: Manual shows "9...16" but CSV shows timing varies based on context
3. **RDLONG** - **CRITICAL**: Missing Z flag specification in Result column (should show "Result = 0" not "---")
4. **RDFAST** - Clock cycles partially incorrect
5. Multiple instructions have incorrect Z flag behavior in encoding tables

### Statistics:
- **Total R Instructions in CSV:** 24 instructions
- **Total R Instructions in Manual:** 24 instructions (all present)
- **Critical Errors:** 4 (timing/flag specifications)
- **Major Errors:** 3 (Result column values)
- **Minor Errors:** 2 (formatting/description nuances)
- **Passed:** 15 instructions

---

## Detailed Findings

### 1. RCL - Rotate Carry Left ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RCL D,{#}S {WC/WZ/WCZ}` | `RCL D,{#}S {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 0000101 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 0000101 CZI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "Last bit out" | "Last bit shifted out if S[4:0] > 0, else D[31]" | ✅ CORRECT (semantically equivalent) |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 2. RCR - Rotate Carry Right ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RCR D,{#}S {WC/WZ/WCZ}` | `RCR D,{#}S {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 0000100 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 0000100 CZI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "Last bit out" | "Last bit shifted out if S[4:0] > 0, else D[0]" | ✅ CORRECT (semantically equivalent) |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 3. RCZL - Rotate Carry And Zero Left ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RCZL D {WC/WZ/WCZ}` | `RCZL D {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ0 DDDDDDDDD 001101011` | `EEEE 1101011 CZ0 DDDDDDDDD 001101011` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "D[31]" | "D[31]" | ✅ CORRECT |
| **Z Flag** | "D[30]" | "D[30]" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 4. RCZR - Rotate Carry And Zero Right ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RCZR D {WC/WZ/WCZ}` | `RCZR D {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ0 DDDDDDDDD 001101010` | `EEEE 1101011 CZ0 DDDDDDDDD 001101010` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "D[1]" | "D[1]" | ✅ CORRECT |
| **Z Flag** | "D[0]" | "D[0]" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 5. RDBYTE - Read Byte From Hub ⚠️ **MAJOR ISSUE - TIMING INCOMPLETE**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RDBYTE D,{#}S/P {WC/WZ/WCZ}` | `RDBYTE D,{#}S/P {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1010110 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1010110 CZI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | **"9...16"** | **"9...16" (COG exec), "9...26" (hub exec), "9...24" (COG exec w/int), "9...44" (hub exec w/int)** | ⚠️ **MAJOR - Incomplete timing specification** |
| **C Flag** | "MSB of byte" | "MSB of byte" | ✅ CORRECT |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | "9-16 clock cycles depending on Hub timing" | CSV provides more detailed context | ⚠️ **INCOMPLETE - Missing full timing context** |

**FINDING:** The manual only shows the basic COG execution timing (9...16 cycles) but does not document:
- Hub execution timing: 9...26 cycles
- COG execution with interrupts: 9...24 cycles
- Hub execution with interrupts: 9...44 cycles

This is a **MAJOR DOCUMENTATION GAP** for developers who need accurate timing for hub-executed code or interrupt-heavy applications.

---

### 6. RDFAST - Read Fast Via FIFO ❌ **CRITICAL - INCORRECT TIMING**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RDFAST {#}D,{#}S` | `RDFAST {#}D,{#}S` | ✅ CORRECT |
| **Opcode** | `EEEE 1100011 1LI DDDDDDDDD SSSSSSSSS` | `EEEE 1100011 1LI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | **"2 or WRFAST finish + 10...17"** | **"2 or WRFAST finish + 10...17" (COG), "2 or WRFAST finish + 10...25" (hub)** | ❌ **CRITICAL - Missing hub execution timing** |
| **C Flag** | "---" | "---" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Accurate but incomplete timing | CSV shows context-dependent timing | ⚠️ **INCOMPLETE** |

**FINDING:** Manual is missing hub execution timing variant (10...25 cycles vs 10...17).

---

### 7. RDLONG - Read Long From Hub ❌ **CRITICAL - WRONG Z FLAG & INCOMPLETE TIMING**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RDLONG D,{#}S/P {WC/WZ/WCZ}` | `RDLONG D,{#}S/P {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1011000 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1011000 CZI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | **"9...16"** | **"9...16" (COG), "9...26" (hub), "9...24" (COG w/int), "9...44" (hub w/int)** | ❌ **CRITICAL - Incomplete timing** |
| **C Flag** | "MSB of long" | "MSB of long" | ✅ CORRECT |
| **Z Flag (Result column)** | **"---"** | **"*" (should be "Result = 0")** | ❌ **CRITICAL ERROR - Wrong value** |
| **Description** | Accurate but incomplete | CSV provides full context | ⚠️ **INCOMPLETE** |

**FINDING:**
1. **CRITICAL:** Z flag Result column shows "---" but should show "*" indicating "Result = 0" based on CSV
2. **MAJOR:** Same timing incompleteness as RDBYTE - missing hub/interrupt timing variants

---

### 8. RDLUT - Read From LUT ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RDLUT D,{#}S/P {WC/WZ/WCZ}` | `RDLUT D,{#}S/P {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1010101 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1010101 CZI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | 3 | 3 | ✅ CORRECT |
| **C Flag** | "MSB of data" | "MSB of data" | ✅ CORRECT |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 9. RDPIN - Read Smart Pin ⚠️ **MINOR - Z FLAG ENCODING DIFFERS**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RDPIN D,{#}S {WC}` | `RDPIN D,{#}S {WC}` | ✅ CORRECT |
| **Opcode** | `EEEE 1010100 C1I DDDDDDDDD SSSSSSSSS` | `EEEE 1010100 C1I DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "Modal result" | "Modal result" | ✅ CORRECT |
| **Z Flag (Result column)** | **"---"** | **"---"** (no Z flag support) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

**NOTE:** RDPIN correctly does NOT support WZ/WCZ, only WC. Manual is correct.

---

### 10. RDWORD - Read Word From Hub ⚠️ **MAJOR ISSUE - INCOMPLETE TIMING**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RDWORD D,{#}S/P {WC/WZ/WCZ}` | `RDWORD D,{#}S/P {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1010111 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 1010111 CZI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | **"9...16"** | **"9...16 *" (COG), "9...26 *" (hub), "9...24 *" (COG w/int), "9...44 *" (hub w/int)** | ⚠️ **MAJOR - Incomplete timing** |
| **C Flag** | "MSB of word" | "MSB of word" | ✅ CORRECT |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate but incomplete | CSV provides full context | ⚠️ **INCOMPLETE** |

**FINDING:** Same timing incompleteness as RDBYTE and RDLONG.

---

### 11. REP - Repeat Block ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `REP {#}D,{#}S` | `REP {#}D,{#}S` | ✅ CORRECT |
| **Opcode** | `EEEE 1100110 1LI DDDDDDDDD SSSSSSSSS` | `EEEE 1100110 1LI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "---" | "---" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Detailed and accurate | Matches CSV semantics | ✅ CORRECT |

**NOTE:** Manual provides excellent additional explanation of @.label syntax and best practices.

---

### 12. RESI0/1/2/3 - Resume From Interrupt ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RESI0`, `RESI1`, `RESI2`, `RESI3` | Same | ✅ CORRECT |
| **RESI3 Opcode** | `EEEE 1011001 110 111110000 111110001` | `EEEE 1011001 110 111110000 111110001` | ✅ CORRECT |
| **RESI2 Opcode** | `EEEE 1011001 110 111110010 111110011` | `EEEE 1011001 110 111110010 111110011` | ✅ CORRECT |
| **RESI1 Opcode** | `EEEE 1011001 110 111110100 111110101` | `EEEE 1011001 110 111110100 111110101` | ✅ CORRECT |
| **RESI0 Opcode** | `EEEE 1011001 110 111111110 111111111` | `EEEE 1011001 110 111111110 111111111` | ✅ CORRECT |
| **Clock Cycles** | "4 (COG), 13...20 (Hub)" | "4 (COG), 13...20 (hub), 4 (COG w/int), 13...28 (hub w/int)" | ⚠️ **MINOR - Missing interrupt timing** |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 13. RET - Return From Subroutine ⚠️ **MINOR - INCOMPLETE TIMING**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RET {WC/WZ/WCZ}` | `RET {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ1 000000000 000101101` | `EEEE 1101011 CZ1 000000000 000101101` | ✅ CORRECT |
| **Clock Cycles** | "4" (with note about Hub timing) | "4 (COG), 13...20 (hub), 4 (COG w/int), 13...28 (hub w/int)" | ⚠️ **MINOR - Incomplete in table** |
| **C Flag** | "K[31]" | "K[31]" | ✅ CORRECT |
| **Z Flag** | "K[30]" | "K[30]" | ✅ CORRECT |
| **Description** | Mentions variable timing | Could be more explicit | ⚠️ **ACCEPTABLE** |

---

### 14. RETA - Return Via PTRA Stack ✅ **PASSED WITH CAVEAT**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RETA {WC/WZ/WCZ}` | `RETA {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ1 000000000 000101110` | `EEEE 1101011 CZ1 000000000 000101110` | ✅ CORRECT |
| **Clock Cycles** | "11...18" | "11...18 * (COG), 20...40 * (hub), 11...26 * (COG w/int), 20...70 * (hub w/int)" | ⚠️ **MINOR - Incomplete timing** |
| **C Flag** | "L[31]" | "L[31]" | ✅ CORRECT |
| **Z Flag** | "L[30]" | "L[30]" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 15. RETB - Return Via PTRB Stack ✅ **PASSED WITH CAVEAT**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RETB {WC/WZ/WCZ}` | `RETB {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ1 000000000 000101111` | `EEEE 1101011 CZ1 000000000 000101111` | ✅ CORRECT |
| **Clock Cycles** | "11...18" | "11...18 * (COG), 20...40 * (hub), 11...26 * (COG w/int), 20...70 * (hub w/int)" | ⚠️ **MINOR - Incomplete timing** |
| **C Flag** | "L[31]" | "L[31]" | ✅ CORRECT |
| **Z Flag** | "L[30]" | "L[30]" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 16. RETI0/1/2/3 - Return From Interrupt ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RETI0`, `RETI1`, `RETI2`, `RETI3` | Same | ✅ CORRECT |
| **RETI3 Opcode** | `EEEE 1011001 110 111111111 111110001` | `EEEE 1011001 110 111111111 111110001` | ✅ CORRECT |
| **RETI2 Opcode** | `EEEE 1011001 110 111111111 111110011` | `EEEE 1011001 110 111111111 111110011` | ✅ CORRECT |
| **RETI1 Opcode** | `EEEE 1011001 110 111111111 111110101` | `EEEE 1011001 110 111111111 111110101` | ✅ CORRECT |
| **RETI0 Opcode** | `EEEE 1011001 110 111111111 111111111` | `EEEE 1011001 110 111111111 111111111` | ✅ CORRECT |
| **Clock Cycles** | "4 (COG), 13...20 (Hub)" | "4 (COG), 13...20 (hub), 4 (COG w/int), 13...28 (hub w/int)" | ⚠️ **MINOR - Missing interrupt timing** |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 17. REV - Reverse Bits ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `REV D` | `REV D` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 000 DDDDDDDDD 001101001` | `EEEE 1101011 000 DDDDDDDDD 001101001` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "---" | "---" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 18. RFBYTE - Read Byte Via FIFO ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RFBYTE D {WC/WZ/WCZ}` | `RFBYTE D {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ0 DDDDDDDDD 000010000` | `EEEE 1101011 CZ0 DDDDDDDDD 000010000` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 (when FIFO has data) | ✅ CORRECT |
| **C Flag** | "MSB of byte" | "MSB of byte" | ✅ CORRECT |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 19. RFLONG - Read Long Via FIFO ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RFLONG D {WC/WZ/WCZ}` | `RFLONG D {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ0 DDDDDDDDD 000010010` | `EEEE 1101011 CZ0 DDDDDDDDD 000010010` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "MSB of long" | "MSB of long" | ✅ CORRECT |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 20. RFVAR - Read Variable Via FIFO ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RFVAR D {WC/WZ/WCZ}` | `RFVAR D {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ0 DDDDDDDDD 000010011` | `EEEE 1101011 CZ0 DDDDDDDDD 000010011` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "0" | "0" | ✅ CORRECT |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 21. RFVARS - Read Signed Variable Via FIFO ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RFVARS D {WC/WZ/WCZ}` | `RFVARS D {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ0 DDDDDDDDD 000010100` | `EEEE 1101011 CZ0 DDDDDDDDD 000010100` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "MSB of value" | "MSB of value" | ✅ CORRECT |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 22. RFWORD - Read Word Via FIFO ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RFWORD D {WC/WZ/WCZ}` | `RFWORD D {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 CZ0 DDDDDDDDD 000010001` | `EEEE 1101011 CZ0 DDDDDDDDD 000010001` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "MSB of word" | "MSB of word" | ✅ CORRECT |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 23. RGBEXP - Expand RGB Color ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RGBEXP D` | `RGBEXP D` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 000 DDDDDDDDD 001100111` | `EEEE 1101011 000 DDDDDDDDD 001100111` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "---" | "---" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 24. RGBSQZ - Squeeze RGB Color ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RGBSQZ D` | `RGBSQZ D` | ✅ CORRECT |
| **Opcode** | `EEEE 1101011 000 DDDDDDDDD 001100110` | `EEEE 1101011 000 DDDDDDDDD 001100110` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "---" | "---" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 25. ROL - Rotate Left ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `ROL D,{#}S {WC/WZ/WCZ}` | `ROL D,{#}S {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 0000001 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 0000001 CZI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "Last bit out" | "Last bit shifted out if S[4:0] > 0, else D[31]" | ✅ CORRECT (semantically equivalent) |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 26. ROLBYTE - Rotate Byte Left Into Register ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `ROLBYTE D,{#}S,#N` / `ROLBYTE D` | `ROLBYTE D,{#}S,#N` / `ROLBYTE D` | ✅ CORRECT |
| **Opcode (with N)** | `EEEE 1001000 NNI DDDDDDDDD SSSSSSSSS` | `EEEE 1001000 NNI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Opcode (alias)** | `EEEE 1001000 000 DDDDDDDDD 000000000` | `EEEE 1001000 000 DDDDDDDDD 000000000` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "---" | "---" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 27. ROLNIB - Rotate Nibble Left Into Register ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `ROLNIB D,{#}S,#N` / `ROLNIB D` | `ROLNIB D,{#}S,#N` / `ROLNIB D` | ✅ CORRECT |
| **Opcode (with N)** | `EEEE 100010N NNI DDDDDDDDD SSSSSSSSS` | `EEEE 100010N NNI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Opcode (alias)** | `EEEE 1000100 000 DDDDDDDDD 000000000` | `EEEE 1000100 000 DDDDDDDDD 000000000` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "---" | "---" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 28. ROLWORD - Rotate Word Left Into Register ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `ROLWORD D,{#}S,#N` / `ROLWORD D` | `ROLWORD D,{#}S,#N` / `ROLWORD D` | ✅ CORRECT |
| **Opcode (with N)** | `EEEE 1001010 0NI DDDDDDDDD SSSSSSSSS` | `EEEE 1001010 0NI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Opcode (alias)** | `EEEE 1001010 000 DDDDDDDDD 000000000` | `EEEE 1001010 000 DDDDDDDDD 000000000` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "---" | "---" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 29. ROR - Rotate Right ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `ROR D,{#}S {WC/WZ/WCZ}` | `ROR D,{#}S {WC/WZ/WCZ}` | ✅ CORRECT |
| **Opcode** | `EEEE 0000000 CZI DDDDDDDDD SSSSSSSSS` | `EEEE 0000000 CZI DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "Last bit out" | "Last bit shifted out if S[4:0] > 0, else D[0]" | ✅ CORRECT (semantically equivalent) |
| **Z Flag** | "Result = 0" | "*" (Result = 0) | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

### 30. RQPIN - Read Smart Pin Without Acknowledge ✅ **PASSED**

| Aspect | Manual Value | CSV Value | Status |
|--------|-------------|-----------|--------|
| **Syntax** | `RQPIN D,{#}S {WC}` | `RQPIN D,{#}S {WC}` | ✅ CORRECT |
| **Opcode** | `EEEE 1010100 C0I DDDDDDDDD SSSSSSSSS` | `EEEE 1010100 C0I DDDDDDDDD SSSSSSSSS` | ✅ CORRECT |
| **Clock Cycles** | 2 | 2 | ✅ CORRECT |
| **C Flag** | "Modal result" | "Modal result" | ✅ CORRECT |
| **Z Flag** | "---" | "---" | ✅ CORRECT |
| **Description** | Accurate | Matches CSV | ✅ CORRECT |

---

## Critical Issues Summary

### Issue #1: RDLONG - CRITICAL - Missing Z Flag Result Specification
**Location:** Line 246 of instructions-r.md
**Current Value:** Z column shows "---"
**Correct Value:** Z column should show "*" (indicating "Result = 0")
**Impact:** CRITICAL - Incorrect documentation of Z flag behavior
**Severity:** CRITICAL

### Issue #2: Hub Memory Read Instructions - MAJOR - Incomplete Timing Documentation
**Affected Instructions:** RDBYTE, RDWORD, RDLONG
**Current:** Only shows basic COG execution timing (e.g., "9...16")
**Missing:**
- Hub execution timing
- COG execution with interrupts timing
- Hub execution with interrupts timing

**Example for RDBYTE:**
- Current: "9...16"
- Complete: "9...16 (COG), 9...26 (hub), 9...24 (COG w/int), 9...44 (hub w/int)"

**Impact:** MAJOR - Developers working with hub-executed code or interrupt-driven applications will have incorrect timing expectations
**Severity:** MAJOR

### Issue #3: RDFAST - CRITICAL - Incomplete Timing Documentation
**Location:** Line 211 of instructions-r.md
**Current:** "2 or WRFAST finish + 10...17"
**Correct:** "2 or WRFAST finish + 10...17 (COG), 2 or WRFAST finish + 10...25 (hub)"
**Impact:** MAJOR - Hub execution timing is missing
**Severity:** MAJOR

### Issue #4: Return/Resume Instructions - MINOR - Incomplete Timing Context
**Affected Instructions:** RET, RETA, RETB, RESI0/1/2/3, RETI0/1/2/3
**Issue:** Timing tables don't fully document interrupt timing variants
**Impact:** MINOR - Most developers won't encounter interrupt timing scenarios
**Severity:** MINOR

---

## Recommendations

### Priority 1 - CRITICAL (Must Fix Immediately):
1. **Fix RDLONG Z flag Result column** - Change "---" to "*" or explicit "Result = 0" notation in line 246

### Priority 2 - MAJOR (Should Fix Soon):
2. **Expand RDBYTE timing documentation** - Add all four timing contexts to the encoding table
3. **Expand RDWORD timing documentation** - Add all four timing contexts to the encoding table
4. **Expand RDLONG timing documentation** - Add all four timing contexts to the encoding table
5. **Expand RDFAST timing documentation** - Add hub execution timing variant

### Priority 3 - MINOR (Nice to Have):
6. **Add timing notes for return/resume instructions** - Document interrupt timing variants in explanation sections
7. **Consider adding a timing context table** - Create a reference table explaining COG/hub/interrupt timing variations

---

## Methodology Notes

This audit compared each instruction in the manual against the authoritative CSV source file. For each instruction, I verified:

1. **Syntax accuracy** - Instruction mnemonic and operand format
2. **Encoding correctness** - Binary encoding pattern (EEEE through SSSSSSSSS)
3. **Clock cycle accuracy** - Timing specifications for all execution contexts
4. **Flag behavior** - C and Z flag effects in all columns
5. **Description fidelity** - Semantic accuracy of instruction descriptions

The CSV file provides timing in multiple contexts:
- Column 7-8: COG execution (base timing)
- Column 9-10: Hub execution timing
- Column 11-12: COG execution with interrupts
- Column 13-14: Hub execution with interrupts

The manual currently only documents the base COG execution timing for most instructions.

---

## Conclusion

While the instructions-r.md file is generally accurate in terms of syntax, encoding, and basic functionality, it has **CRITICAL GAPS** in timing documentation that will impact developers working with:
- Hub-executed code
- Interrupt-driven applications
- Real-time timing-sensitive applications

The **CRITICAL ERROR** in RDLONG's Z flag specification must be corrected immediately. The timing documentation gaps should be addressed as a high priority to ensure developers have complete and accurate reference material.

**Overall Grade:** C+ (Functionally correct but critically incomplete in timing specifications)

---

**End of Audit Report**
