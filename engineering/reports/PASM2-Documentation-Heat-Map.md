# PASM2 Documentation Quality Heat Maps

**Analysis Date**: 2025-09-19
**Separate tracking for instructions and directives**

## Key Features

- ✅ **Separate heat maps** for instructions vs directives
- ✅ **Complete directive coverage** - all assembly directives included
- ✅ **Proper categorization** - directives not mixed with instructions
- ✅ **Accurate scoring** - different criteria for different categories

## Legend

| Score | Color | Quality | Description |
|-------|-------|---------|-------------|
| 80-100 | 🟩 | Excellent | Full documentation with examples, all fields present |
| 60-79 | 🟦 | Good | Good documentation, may lack examples or some details |
| 40-59 | 🟨 | Fair | Basic documentation, missing important details |
| 20-39 | 🟧 | Poor | Minimal documentation, many gaps |
| 0-19 | 🟥 | Minimal | Little to no documentation |

## 1. PASM2 CPU Instructions Heat Map

CPU instructions that execute on the P2 processor.

### CPU Instructions (Worst to Best)

**Total: 358 items**

| Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 | Col 7 | Col 8 | Col 9 | Col 10 | Col 11 | Col 12 |
||".join(["-------"] * cols) + "|
| 🟧 PUSHA | 🟧 PUSHB | 🟨 POPB | 🟨 POPA | 🟨 NIXINT1 | 🟨 NIXINT3 | 🟨 NIXINT2 | 🟨 CRCNIB | 🟨 CRCBIT | 🟨 SETCY | 🟨 XSTOP | 🟨 SETDACS |
| 🟨 WRLUT | 🟨 RGBEXP | 🟨 TRGINT1 | 🟨 MULPIX | 🟨 SETINT3 | 🟨 SETPIX | 🟨 SETCFRQ | 🟨 SETSE1 | 🟨 WRC | 🟨 WRBYTE | 🟨 WRZ | 🟨 SETINT2 |
| 🟨 WMLONG | 🟨 SETINT1 | 🟨 SETPIV | 🟨 SETSE2 | 🟨 SETCQ | 🟨 SETSE3 | 🟨 SETCI | 🟨 SETCMOD | 🟨 SETSE4 | 🟨 TRGINT2 | 🟨 SETXFRQ | 🟨 RGBSQZ |
| 🟨 LOC | 🟨 BLNPIX | 🟨 TRGINT3 | 🟨 MIXPIX | 🟨 RQPIN | 🟨 SETQ | 🟨 TJNZ | 🟨 GETCT | 🟨 JINT | 🟨 JNXRO | 🟨 TJF | 🟨 SKIP |
| 🟨 TJS | 🟨 REP | 🟨 JPAT | 🟨 JNINT | 🟨 WFBYTE | 🟨 WRLONG | 🟨 JXRO | 🟨 WRWORD | 🟨 WRFAST | 🟨 JNPAT | 🟨 WFWORD | 🟨 HUBSET |
| 🟨 WFLONG | 🟨 LOCKRET | 🟨 MERGEW | 🟨 GETPTR | 🟨 MERGEB | 🟨 MOVBYTS | 🟨 SETPAT | 🟨 XCONT | 🟨 NOP | 🟨 WXPIN | 🟨 JNATN | 🟨 JMPREL |
| 🟨 TESTB | 🟨 TJZ | 🟨 XZERO | 🟨 SETSCP | 🟨 FBLOCK | 🟨 JXFI | 🟨 RET | 🟨 GETXACC | 🟨 SETLUTS | 🟨 SEUSSR | 🟨 GETSCP | 🟨 XORO32 |
| 🟨 GETRND | 🟨 SEUSSF | 🟨 SKIPF | 🟨 SPLITW | 🟨 SPLITB | 🟨 JNXFI | 🟨 JMP | 🟨 ASMCLK | 🟨 SUMZ | 🟨 RDBYTE | 🟨 SUMC | 🟨 RFVAR |
| 🟨 EXECF | 🟨 RFVARS | 🟨 WRNZ | 🟨 RDPIN | 🟨 WRNC | 🟨 RETB | 🟨 MUXC | 🟨 RFWORD | 🟨 RFLONG | 🟨 MUXNC | 🟨 RETA | 🟨 GETQX |
| 🟨 RFBYTE | 🟨 GETQY | 🟨 RDLUT | 🟨 LOCKNEW | 🟨 DEBUG | 🟨 JATN | 🟦 XINIT | 🟦 RESI1 | 🟦 RETI3 | 🟦 RETI2 | 🟦 RESI0 | 🟦 RETI1 |
| 🟦 RESI3 | 🟦 TJNS | 🟦 RESI2 | 🟦 RETI0 | 🟦 RDWORD | 🟦 WMLONG_ | 🟦 RDLONG | 🟦 BITNC | 🟦 AND | 🟦 BITL | 🟦 BITNZ | 🟦 OUTH |
| 🟦 FLTNZ | 🟦 FLTZ | 🟦 ANDN | 🟦 JXMT | 🟦 BITC | 🟦 TJNF | 🟦 BITZ | 🟦 BITH | 🟦 JNXMT | 🟦 OUTL | 🟦 POLLXRO | 🟦 COGBRK |
| 🟦 POLLQMT | 🟦 SCA | 🟦 CALLPB | 🟦 COGATN | 🟦 COGSTOP | 🟦 STALLI | 🟦 POLLSE4 | 🟦 ADDCT1 | 🟦 POLLSE3 | 🟦 POLLINT | 🟦 POLLSE2 | 🟦 ALLOWI |
| 🟦 SCAS | 🟦 POLLPAT | 🟦 ADDCT3 | 🟦 POLLATN | 🟦 POLLSE1 | 🟦 AKPIN | 🟦 JFBW | 🟦 ADDCT2 | 🟦 JXRL | 🟦 CALLPA | 🟦 POLLXFI | 🟦 JNFBW |
| 🟦 POLLXMT | 🟦 SETNIB | 🟦 JNXRL | 🟦 POLLXRL | 🟦 POLLFBW | 🟦 ALTSN | 🟦 SETD | 🟦 OUTZ | 🟦 FLTRND | 🟦 JNQMT | 🟦 RCZL | 🟦 CMP |
| 🟦 SUBS | 🟦 NEGNZ | 🟦 CMPX | 🟦 NEGNC | 🟦 ALTSB | 🟦 CMPSX | 🟦 NOT | 🟦 OUTC | 🟦 CALLD | 🟦 CMPM | 🟦 ROLWORD | 🟦 OR |
| 🟦 ENCOD | 🟦 ROR | 🟦 SUMNZ | 🟦 WAITATN | 🟦 OUTNC | 🟦 FGES | 🟦 ZEROX | 🟦 FGE | 🟦 SAL | 🟦 DIRC | 🟦 TESTPN | 🟦 ADDX |
| 🟦 SUBR | 🟦 IJNZ | 🟦 DIRZ | 🟦 SUMNC | 🟦 COGID | 🟦 OUTNZ | 🟦 ROLBYTE | 🟦 WAITXMT | 🟦 TEST | 🟦 SUB | 🟦 DJF | 🟦 CALLB |
| 🟦 DRVNOT | 🟦 WAITXFI | 🟦 ADDS | 🟦 DJNF | 🟦 DIRH | 🟦 JQMT | 🟦 CMPR | 🟦 WAITFBW | 🟦 DECOD | 🟦 DRVL | 🟦 CALL | 🟦 ROL |
| 🟦 WAITXRL | 🟦 MUXNITS | 🟦 SAR | 🟦 REV | 🟦 ROLNIB | 🟦 SUBSX | 🟦 DIRNZ | 🟦 IJZ | 🟦 ALTD | 🟦 FLTNC | 🟦 DIRNOT | 🟦 CMPS |
| 🟦 SUBX | 🟦 BITRND | 🟦 RCZR | 🟦 MOV | 🟦 OUTNOT | 🟦 XOR | 🟦 FLTL | 🟦 ABS | 🟦 DIRNC | 🟦 DRVNZ | 🟦 NEGC | 🟦 TESTN |
| 🟦 MUXNZ | 🟦 TJV | 🟦 NEG | 🟦 ALTR | 🟦 NEGZ | 🟦 MULS | 🟦 DRVNC | 🟦 FLTC | 🟦 MUXZ | 🟦 FLTNOT | 🟦 SETWORD | 🟦 ADD |
| 🟦 GETNIB | 🟦 FLE | 🟦 SIGNX | 🟦 DRVZ | 🟦 ALTGW | 🟦 RCL | 🟦 WAITXRO | 🟦 BMASK | 🟦 ALTGN | 🟦 DRVC | 🟦 CALLA | 🟦 ADDSX |
| 🟦 TESTBN | 🟦 SHL | 🟦 SETBYTE | 🟦 SETS | 🟦 MODC | 🟦 DRVH | 🟦 ADDPIX | 🟦 ONES | 🟦 MUL | 🟦 SHR | 🟦 DIRL | 🟦 DECMOD |
| 🟦 DRVRND | 🟦 MODZ | 🟦 WAITPAT | 🟦 RCR | 🟦 GETBYTE | 🟦 CMPSUB | 🟦 FLTH | 🟦 DJNZ | 🟦 OUTRND | 🟦 BITNOT | 🟦 FLES | 🟦 DIRRND |
| 🟦 MUXNIBS | 🟦 WAITINT | 🟦 GETWORD | 🟦 MODCZ | 🟦 DJZ | 🟦 SETR | 🟩 ALTSW | 🟩 WAITX | 🟩 ALTB | 🟩 TESTP | 🟩 JSE3 | 🟩 JSE2 |
| 🟩 JNCT1 | 🟩 JNSE3 | 🟩 JCT1 | 🟩 JSE4 | 🟩 JNSE2 | 🟩 JNSE1 | 🟩 JCT2 | 🟩 JCT3 | 🟩 JNCT2 | 🟩 JSE1 | 🟩 GETBRK | 🟩 COGINIT |
| 🟩 POLLCT1 | 🟩 SETQ2 | 🟩 RDFAST | 🟩 QVECTOR | 🟩 LOCKREL | 🟩 QLOG | 🟩 WYPIN | 🟩 QEXP | 🟩 POLLCT2 | 🟩 QMUL | 🟩 POLLCT3 | 🟩 AUGD |
| 🟩 QFRAC | 🟩 BRK | 🟩 ALTGB | 🟩 ALTS | 🟩 QDIV | 🟩 QROTATE | 🟩 WRPIN | 🟩 INCMOD | 🟩 MUXQ | 🟩 LOCKTRY | 🟩 QSQRT | 🟩 AUGS |
| 🟩 JNSE4 | 🟩 JNCT3 | 🟩 ALTI | 🟩 WAITSE1 | 🟩 WAITCT3 | 🟩 WAITCT2 | 🟩 WAITCT1 | 🟩 WAITSE4 | 🟩 WAITSE2 | 🟩 WAITSE3 |  |  |

**Distribution:**
- Excellent (80-100): 52
- Good (60-79): 192
- Fair (40-59): 112
- Poor (20-39): 2

## 2. Assembly Directives Heat Map

Assembler directives for data declaration and memory organization.

### Assembly Directives (Worst to Best)

**Total: 12 items**

| Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 | Col 7 | Col 8 | Col 9 | Col 10 | Col 11 | Col 12 |
||".join(["-------"] * cols) + "|
| 🟧 FIT | 🟧 ORGH | 🟧 DITTO | 🟧 ORGF | 🟧 RES | 🟧 ORG | 🟨 BYTE | 🟨 WORD | 🟨 LONG | 🟨 FILE | 🟩 ALIGNL | 🟩 ALIGNW |

**Distribution:**
- Excellent (80-100): 2
- Fair (40-59): 4
- Poor (20-39): 6

## 3. Instruction Groups Analysis

| Group | Avg Score | Quality | Count | Sample Instructions |
|-------|-----------|---------|-------|---------------------|
| Color Space Converter | 🟨 45 | fair | 5 | SETCY, SETCFRQ, SETCQ... |
| Pixel Mixer | 🟨 45 | fair | 5 | MULPIX, SETPIX, SETPIV... |
| Hub RAM - Write | 🟨 46 | fair | 7 | PUSHA, WMLONG_, WRLONG... |
| Interrupts | 🟨 48 | fair | 10 | GETBRK, TRGINT1, SETINT3... |
| Flow Control Instruction - Tes | 🟨 50 | fair | 1 | TJNZ |
| Streamer | 🟨 50 | fair | 6 | XSTOP, XINIT, XCONT... |
| Branch D - Skip | 🟨 50 | fair | 1 | SKIP |
| Lookup Table | 🟨 50 | fair | 3 | WRLUT, RDLUT, SETLUTS |
| Branch Repeat | 🟨 50 | fair | 1 | REP |
| Hub FIFO - Write | 🟨 50 | fair | 3 | WFBYTE, WFWORD, WFLONG |
| Hub FIFO - New Write | 🟨 50 | fair | 1 | WRFAST |
| Hub Control - Multi | 🟨 50 | fair | 1 | HUBSET |
| Hub FIFO | 🟨 50 | fair | 1 | GETPTR |
| Miscellaneous Instruction - No | 🟨 50 | fair | 1 | NOP |
| Branch D - Jump | 🟨 50 | fair | 1 | JMPREL |
| Hub FIFO - New Block | 🟨 50 | fair | 1 | FBLOCK |
| Branch D - Jump+Skip | 🟨 50 | fair | 1 | SKIPF |
| Branch A - Jump | 🟨 50 | fair | 1 | JMP |
| Math and Logic | 🟨 52 | fair | 23 | CRCBIT, SUMZ, NOT... |
| Hub RAM - Read | 🟨 53 | fair | 5 | RDBYTE, RDWORD, RDLONG... |

## 4. Overall Statistics

### CPU Instructions
- Total: 358
- Excellent: 52
- Good: 192
- Fair: 112
- Poor: 2
- Minimal: 0

### Assembly Directives
- Total: 12
- With documentation: 12
- Missing: 0

## 5. Recommendations

### Priority 1: Fix 2 Poor Instructions
- PUSHA (score: 35)
- PUSHB (score: 35)

### Priority 2: Complete Directive Documentation
- Improve FIT (score: 33)
- Improve ORGH (score: 33)
- Improve DITTO (score: 33)
- Improve ORGF (score: 33)
- Improve RES (score: 33)

---
*Generated by PASM2 documentation analysis tool*
*Separate tracking for instructions and directives*