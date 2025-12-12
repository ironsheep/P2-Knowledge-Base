# Instruction Categories {#instruction-categories}

This chapter defines the instruction categories used throughout Part II. Each category groups instructions by their primary function. Click any category name in the instruction entries to return here for an overview, or click any instruction mnemonic to jump to its detailed reference.

---

## Arithmetic Operations {#arithmetic-operations}

Arithmetic instructions perform mathematical and logical operations on register values. This includes addition, subtraction, multiplication, comparisons, bitwise operations (AND, OR, XOR), bit manipulation, shifts, rotates, and data movement. This is the largest instruction category.

**Data Movement:** [MOV](#mov), [LOC](#loc)

**Addition/Subtraction:** [ADD](#add), [ADDS](#adds), [ADDSX](#addsx), [ADDX](#addx), [SUB](#sub), [SUBR](#subr), [SUBS](#subs), [SUBSX](#subsx), [SUBX](#subx)

**Negation/Absolute:** [ABS](#abs), [NEG](#neg), [NEGC](#negc), [NEGNC](#negc), [NEGNZ](#negc), [NEGZ](#negc)

**Multiplication:** [MUL](#mul), [MULS](#muls), [SCA](#sca), [SCAS](#scas)

**Comparisons:** [CMP](#cmp), [CMPM](#cmpm), [CMPR](#cmpr), [CMPS](#cmps), [CMPSUB](#cmpsub), [CMPSX](#cmpsx), [CMPX](#cmpx), [TEST](#test), [TESTN](#testn)

**Min/Max:** [FGE](#fge), [FGES](#fges), [FLE](#fle), [FLES](#fles)

**Modular Arithmetic:** [INCMOD](#incmod), [DECMOD](#decmod)

**Bitwise Logic:** [AND](#and), [ANDN](#andn), [OR](#or), [XOR](#xor), [NOT](#not), [XORO32](#xoro32)

**Bit Field Operations:** [BITC](#bitc), [BITH](#bith), [BITL](#bitl), [BITNC](#bitc), [BITNOT](#bitnot), [BITNZ](#bitc), [BITRND](#bitrnd), [BITZ](#bitc), [TESTB](#testb), [TESTBN](#testbn)

**Bit Utilities:** [BMASK](#bmask), [DECOD](#decod), [ENCOD](#encod), [ONES](#ones), [REV](#rev), [SIGNX](#signx), [ZEROX](#zerox)

**Shifts:** [SHL](#shl), [SHR](#shr), [SAL](#sal), [SAR](#sar)

**Rotates:** [ROL](#rol), [ROR](#ror), [RCL](#rcl), [RCR](#rcr), [RCZL](#rczl), [RCZR](#rczr)

**Byte/Word/Nibble Access:** [GETBYTE](#getbyte), [GETNIB](#getnib), [GETWORD](#getword), [SETBYTE](#setbyte), [SETNIB](#setnib), [SETWORD](#setword), [ROLBYTE](#rolbyte), [ROLNIB](#rolnib), [ROLWORD](#rolword)

**Byte/Word Packing:** [MOVBYTS](#movbyts), [SPLITB](#splitb), [SPLITW](#splitw), [MERGEB](#mergeb), [MERGEW](#mergew)

**Mux Operations:** [MUXC](#muxc), [MUXNC](#muxc), [MUXNZ](#muxc), [MUXZ](#muxc), [MUXQ](#muxq), [MUXNIBS](#muxnibs), [MUXNITS](#muxnits)

**Conditional Sum:** [SUMC](#sumc), [SUMNC](#sumc), [SUMNZ](#sumc), [SUMZ](#sumc)

**Flag Operations:** [WRC](#wrc), [WRNC](#wrc), [WRNZ](#wrc), [WRZ](#wrc), [MODC](#modc), [MODZ](#modz), [MODCZ](#modcz)

**Instruction Field Modification:** [SETD](#setd), [SETS](#sets), [SETR](#setr)

**CRC:** [CRCBIT](#crcbit), [CRCNIB](#crcnib)

**Graphics:** [RGBEXP](#rgbexp), [RGBSQZ](#rgbsqz)

**Shuffling:** [SEUSSF](#seussf), [SEUSSR](#seussr)

---

## Branching and Flow Control {#branching-and-flow-control}

Branch instructions control program flow by modifying the program counter. This category includes conditional and unconditional jumps, subroutine calls using stack or pointer registers, returns from subroutines and interrupts, and instruction skipping/repeating mechanisms.

[CALL](#call), [CALLA](#calla), [CALLB](#callb), [CALLD](#calld), [CALLPA](#callpa), [CALLPB](#callpb), [DJF](#djf), [DJNF](#djnf), [DJNZ](#djz), [DJZ](#djz), [EXECF](#execf), [IJNZ](#ijz), [IJZ](#ijz), [JMP](#jmp), [JMPREL](#jmprel), [REP](#rep), [RESI0](#resi0), [RESI1](#resi0), [RESI2](#resi0), [RESI3](#resi0), [RET](#ret), [RETA](#reta), [RETB](#retb), [RETI0](#reti0), [RETI1](#reti0), [RETI2](#reti0), [RETI3](#reti0), [SKIP](#skip), [SKIPF](#skipf), [TJF](#tjf), [TJNF](#tjf), [TJNS](#tjs), [TJNZ](#tjz), [TJS](#tjs), [TJV](#tjv), [TJZ](#tjz)

---

## Hub Memory Access {#hub-memory-access}

Hub memory instructions transfer data between cog registers and the shared 512KB hub RAM. This includes byte, word, and long access with various addressing modes, pointer-based operations using PTRA/PTRB, and high-speed FIFO streaming for bulk data transfers.

[FBLOCK](#fblock), [GETPTR](#getptr), [POPA](#popa), [POPB](#popb), [PUSHA](#pusha), [PUSHB](#pushb), [RDBYTE](#rdbyte), [RDFAST](#rdfast), [RDLONG](#rdlong), [RDWORD](#rdword), [RFBYTE](#rfbyte), [RFLONG](#rflong), [RFVAR](#rfvar), [RFVARS](#rfvars), [RFWORD](#rfword), [WFBYTE](#wfbyte), [WFLONG](#wflong), [WFWORD](#wfword), [WMLONG](#wmlong), [WRBYTE](#wrbyte), [WRFAST](#wrfast), [WRLONG](#wrlong), [WRWORD](#wrword)

---

## Lookup Table {#lookup-table}

Lookup table (LUT) instructions access the 512-long LUT memory private to each cog. The LUT provides fast table lookups, additional register storage, and can be shared between adjacent cog pairs for inter-cog communication.

[RDLUT](#rdlut), [SETLUTS](#setluts), [WRLUT](#wrlut)

---

## Pin I/O and Smart Pins {#pin-io-and-smart-pins}

Pin instructions control the P2's 64 I/O pins. Basic pin operations set direction (input/output) and output level (high/low). Smart pin instructions configure and communicate with the autonomous smart pin state machines that can perform complex I/O functions independent of cog processing.

**Direction Control:** [DIRC](#dirc), [DIRH](#dirh), [DIRL](#dirl), [DIRNC](#dirc), [DIRNOT](#dirnot), [DIRNZ](#dirz), [DIRRND](#dirrnd), [DIRZ](#dirz)

**Output Control:** [OUTC](#outc), [OUTH](#outh), [OUTL](#outl), [OUTNC](#outc), [OUTNOT](#outnot), [OUTNZ](#outc), [OUTRND](#outrnd), [OUTZ](#outc)

**Drive (Direction + Output):** [DRVC](#drvc), [DRVH](#drvh), [DRVL](#drvl), [DRVNC](#drvc), [DRVNOT](#drvnot), [DRVNZ](#drvz), [DRVRND](#drvrnd), [DRVZ](#drvz)

**Float (Input with Preset):** [FLTC](#fltc), [FLTH](#flth), [FLTL](#fltl), [FLTNC](#fltc), [FLTNOT](#fltnot), [FLTNZ](#fltc), [FLTRND](#fltrnd), [FLTZ](#fltc)

**Pin Testing:** [TESTP](#testp), [TESTPN](#testp)

**Smart Pin Control:** [AKPIN](#akpin), [RDPIN](#rdpin), [RQPIN](#rqpin), [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin)

**Oscilloscope/DAC:** [GETSCP](#getscp), [SETSCP](#setscp), [SETDACS](#setdacs)

---

## Events and Timing {#events-and-timing}

Event instructions monitor and respond to system events including counter/timer triggers, smart pin signals, FIFO status, streamer conditions, and inter-cog attention signals. They provide configuration, polling, waiting, and conditional branching mechanisms for synchronization.

**Configuration:** [ADDCT1](#addct1), [ADDCT2](#addct1), [ADDCT3](#addct1), [SETPAT](#setpat), [SETSE1](#setse1), [SETSE2](#setse1), [SETSE3](#setse1), [SETSE4](#setse1)

**Inter-COG:** [COGATN](#cogatn)

**Polling:** [POLLATN](#pollatn), [POLLCT1](#pollct1), [POLLCT2](#pollct1), [POLLCT3](#pollct1), [POLLFBW](#pollfbw), [POLLINT](#pollint), [POLLPAT](#pollpat), [POLLQMT](#pollqmt), [POLLSE1](#pollse1), [POLLSE2](#pollse1), [POLLSE3](#pollse1), [POLLSE4](#pollse1), [POLLXFI](#pollxfi), [POLLXMT](#pollxmt), [POLLXRL](#pollxrl), [POLLXRO](#pollxro)

**Waiting:** [WAITATN](#waitatn), [WAITCT1](#waitct1), [WAITCT2](#waitct1), [WAITCT3](#waitct1), [WAITFBW](#waitfbw), [WAITINT](#waitint), [WAITPAT](#waitpat), [WAITSE1](#waitse1), [WAITSE2](#waitse1), [WAITSE3](#waitse1), [WAITSE4](#waitse1), [WAITXFI](#waitxfi), [WAITXMT](#waitxmt), [WAITXRL](#waitxrl), [WAITXRO](#waitxro)

**Branch on Event Set:** [JATN](#jatn), [JCT1](#jct1), [JCT2](#jct1), [JCT3](#jct1), [JFBW](#jfbw), [JINT](#jint), [JPAT](#jpat), [JQMT](#jqmt), [JSE1](#jse1), [JSE2](#jse1), [JSE3](#jse1), [JSE4](#jse1), [JXFI](#jxfi), [JXMT](#jxmt), [JXRL](#jxrl), [JXRO](#jxro)

**Branch on Event Clear:** [JNATN](#jatn), [JNCT1](#jct1), [JNCT2](#jct1), [JNCT3](#jct1), [JNFBW](#jfbw), [JNINT](#jint), [JNPAT](#jpat), [JNQMT](#jqmt), [JNSE1](#jse1), [JNSE2](#jse1), [JNSE3](#jse1), [JNSE4](#jse1), [JNXFI](#jxfi), [JNXMT](#jxmt), [JNXRL](#jxrl), [JNXRO](#jxro)

---

## Interrupts {#interrupts}

Interrupt instructions control the cog's three-level interrupt system (INT1, INT2, INT3) plus the debug interrupt (INT0). This includes enabling/disabling interrupts, configuring interrupt sources, triggering software interrupts, and managing breakpoints for debugging.

[ALLOWI](#allowi), [BRK](#brk), [COGBRK](#cogbrk), [GETBRK](#getbrk), [NIXINT1](#nixint1), [NIXINT2](#nixint1), [NIXINT3](#nixint1), [SETINT1](#setint1), [SETINT2](#setint1), [SETINT3](#setint1), [STALLI](#stalli), [TRGINT1](#trgint1), [TRGINT2](#trgint1), [TRGINT3](#trgint1)

---

## COG Control and Locks {#cog-control-and-locks}

COG control instructions manage cog operations including starting and stopping cogs, querying cog identity, and configuring hub-level system settings. Lock instructions provide mutex-style synchronization primitives for safe inter-cog resource sharing.

[COGID](#cogid), [COGINIT](#coginit), [COGSTOP](#cogstop), [HUBSET](#hubset), [LOCKNEW](#locknew), [LOCKREL](#lockrel), [LOCKRET](#lockret), [LOCKTRY](#locktry)

---

## CORDIC Coprocessor {#cordic-coprocessor}

CORDIC (Coordinate Rotation Digital Computer) instructions provide hardware-accelerated mathematical operations. The dedicated coprocessor performs multiplication, division, square root, trigonometric functions, logarithms, and coordinate transformations with high precision.

[GETQX](#getqx), [GETQY](#getqy), [QDIV](#qdiv), [QEXP](#qexp), [QFRAC](#qfrac), [QLOG](#qlog), [QMUL](#qmul), [QROTATE](#qrotate), [QSQRT](#qsqrt), [QVECTOR](#qvector)

---

## Streamer {#streamer}

Streamer instructions control the cog's dedicated DMA engine that autonomously transfers data between hub memory, LUT, and I/O pins. The streamer is essential for high-bandwidth applications like video output, audio streaming, and bulk data movement.

[GETXACC](#getxacc), [SETXFRQ](#setxfrq), [XCONT](#xcont), [XINIT](#xinit), [XSTOP](#xstop), [XZERO](#xzero)

---

## Color Space and Pixel Operations {#color-space-and-pixel-operations}

Color space and pixel instructions provide hardware-accelerated graphics processing. The colorspace converter transforms between color representations (RGB, YUV). The pixel mixer performs alpha blending, color addition, and format conversions for video and graphics applications.

[ADDPIX](#addpix), [BLNPIX](#blnpix), [MIXPIX](#mixpix), [MULPIX](#mulpix), [SETCFRQ](#setcfrq), [SETCI](#setci), [SETCMOD](#setcmod), [SETCQ](#setcq), [SETCY](#setcy), [SETPIV](#setpiv), [SETPIX](#setpix)

---

## Instruction Modification {#instruction-modification}

Instruction modification instructions (also known as register indirection) dynamically alter subsequent instructions by changing their source, destination, or bit index fields before execution. They enable register arrays, computed addressing, and self-modifying code patterns essential for efficient data structure access.

[ALTB](#altb), [ALTD](#altd), [ALTGB](#altgb), [ALTGN](#altgn), [ALTGW](#altgw), [ALTI](#alti), [ALTR](#altr), [ALTS](#alts), [ALTSB](#altsb), [ALTSN](#altsn), [ALTSW](#altsw)

---

## Miscellaneous {#miscellaneous}

Miscellaneous instructions provide utility functions including immediate value extension (AUGS/AUGD), stack operations, random number generation, system timer access, and delay insertion.

[AUGD](#augd), [AUGS](#augs), [GETCT](#getct), [GETRND](#getrnd), [NOP](#nop), [POP](#pop), [PUSH](#push), [SETQ](#setq), [SETQ2](#setq2), [WAITX](#waitx)

