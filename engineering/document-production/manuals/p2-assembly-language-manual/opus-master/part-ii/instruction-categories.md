# Instruction Categories {#instruction-categories}

This chapter defines the instruction categories used throughout Part II. Each category groups instructions by their primary function. Click any category name in the instruction entries to return here for an overview, or click any instruction mnemonic to jump to its detailed reference.

---

## Arithmetic Operations {#arithmetic-operations}

Arithmetic instructions perform mathematical and logical operations on register values. This includes addition, subtraction, multiplication, comparisons, bitwise operations (AND, OR, XOR), bit manipulation, shifts, rotates, and data movement. This is the largest instruction category.

[ABS](#abs), [ADD](#add), [ADDS](#adds), [ADDSX](#addsx), [ADDX](#addx), [AND](#and), [ANDN](#andn), [BITC](#bitc), [BITH](#bith), [BITL](#bitl), [BITNC](#bitnc), [BITNOT](#bitnot), [BITNZ](#bitnz), [BITRND](#bitrnd), [BITZ](#bitz), [BMASK](#bmask), [CMP](#cmp), [CMPM](#cmpm), [CMPR](#cmpr), [CMPS](#cmps), [CMPSUB](#cmpsub), [CMPSX](#cmpsx), [CMPX](#cmpx), [CRCBIT](#crcbit), [CRCNIB](#crcnib), [DECMOD](#decmod), [DECOD](#decod), [ENCOD](#encod), [FGE](#fge), [FGES](#fges), [FLE](#fle), [FLES](#fles), [GETBYTE](#getbyte), [GETNIB](#getnib), [GETWORD](#getword), [INCMOD](#incmod), [LOC](#loc), [MERGEB](#mergeb), [MERGEW](#mergew), [MODC](#modc), [MODCZ](#modcz), [MODZ](#modz), [MOV](#mov), [MOVBYTS](#movbyts), [MUL](#mul), [MULS](#muls), [MUXC](#muxc), [MUXNC](#muxnc), [MUXNIBS](#muxnibs), [MUXNITS](#muxnits), [MUXNZ](#muxnz), [MUXQ](#muxq), [MUXZ](#muxz), [NEG](#neg), [NEGC](#negc), [NEGNC](#negnc), [NEGNZ](#negnz), [NEGZ](#negz), [NOT](#not), [ONES](#ones), [OR](#or), [RCL](#rcl), [RCR](#rcr), [RCZL](#rczl), [RCZR](#rczr), [REV](#rev), [RGBEXP](#rgbexp), [RGBSQZ](#rgbsqz), [ROL](#rol), [ROLBYTE](#rolbyte), [ROLNIB](#rolnib), [ROLWORD](#rolword), [ROR](#ror), [SAL](#sal), [SAR](#sar), [SCA](#sca), [SCAS](#scas), [SETBYTE](#setbyte), [SETD](#setd), [SETNIB](#setnib), [SETR](#setr), [SETS](#sets), [SETWORD](#setword), [SEUSSF](#seussf), [SEUSSR](#seussr), [SHL](#shl), [SHR](#shr), [SIGNX](#signx), [SPLITB](#splitb), [SPLITW](#splitw), [SUB](#sub), [SUBR](#subr), [SUBS](#subs), [SUBSX](#subsx), [SUBX](#subx), [SUMC](#sumc), [SUMNC](#sumnc), [SUMNZ](#sumnz), [SUMZ](#sumz), [TEST](#test), [TESTB](#testb), [TESTBN](#testbn), [TESTN](#testn), [WRC](#wrc), [WRNC](#wrnc), [WRNZ](#wrnz), [WRZ](#wrz), [XOR](#xor), [XORO32](#xoro32), [ZEROX](#zerox)

---

## Branching and Flow Control {#branching-and-flow-control}

Branch instructions control program flow by modifying the program counter. This category includes conditional and unconditional jumps, subroutine calls using stack or pointer registers, returns from subroutines and interrupts, and instruction skipping/repeating mechanisms.

[CALL](#call), [CALLA](#calla), [CALLB](#callb), [CALLD](#calld), [CALLPA](#callpa), [CALLPB](#callpb), [DJF](#djf), [DJNF](#djnf), [DJNZ](#djnz), [DJZ](#djz), [EXECF](#execf), [IJNZ](#ijnz), [IJZ](#ijz), [JMP](#jmp), [JMPREL](#jmprel), [REP](#rep), [RESI0](#resi0), [RESI1](#resi1), [RESI2](#resi2), [RESI3](#resi3), [RET](#ret), [RETA](#reta), [RETB](#retb), [RETI0](#reti0), [RETI1](#reti1), [RETI2](#reti2), [RETI3](#reti3), [SKIP](#skip), [SKIPF](#skipf), [TJF](#tjf), [TJNF](#tjnf), [TJNS](#tjns), [TJNZ](#tjnz), [TJS](#tjs), [TJV](#tjv), [TJZ](#tjz)

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

[AKPIN](#akpin), [DIRC](#dirc), [DIRH](#dirh), [DIRL](#dirl), [DIRNC](#dirnc), [DIRNOT](#dirnot), [DIRNZ](#dirnz), [DIRRND](#dirrnd), [DIRZ](#dirz), [DRVC](#drvc), [DRVH](#drvh), [DRVL](#drvl), [DRVNC](#drvnc), [DRVNOT](#drvnot), [DRVNZ](#drvnz), [DRVRND](#drvrnd), [DRVZ](#drvz), [FLTC](#fltc), [FLTH](#flth), [FLTL](#fltl), [FLTNC](#fltnc), [FLTNOT](#fltnot), [FLTNZ](#fltnz), [FLTRND](#fltrnd), [FLTZ](#fltz), [GETSCP](#getscp), [OUTC](#outc), [OUTH](#outh), [OUTL](#outl), [OUTNC](#outnc), [OUTNOT](#outnot), [OUTNZ](#outnz), [OUTRND](#outrnd), [OUTZ](#outz), [RDPIN](#rdpin), [RQPIN](#rqpin), [SETDACS](#setdacs), [SETSCP](#setscp), [TESTP](#testp), [TESTPN](#testpn), [WRPIN](#wrpin), [WXPIN](#wxpin), [WYPIN](#wypin)

---

## Events and Timing {#events-and-timing}

Event instructions monitor and respond to system events including counter/timer triggers, smart pin signals, FIFO status, streamer conditions, and inter-cog attention signals. They provide configuration, polling, waiting, and conditional branching mechanisms for synchronization.

[ADDCT1](#addct1), [ADDCT2](#addct2), [ADDCT3](#addct3), [COGATN](#cogatn), [JATN](#jatn), [JCT1](#jct1), [JCT2](#jct2), [JCT3](#jct3), [JFBW](#jfbw), [JINT](#jint), [JNATN](#jnatn), [JNCT1](#jnct1), [JNCT2](#jnct2), [JNCT3](#jnct3), [JNFBW](#jnfbw), [JNINT](#jnint), [JNPAT](#jnpat), [JNQMT](#jnqmt), [JNSE1](#jnse1), [JNSE2](#jnse2), [JNSE3](#jnse3), [JNSE4](#jnse4), [JNXFI](#jnxfi), [JNXMT](#jnxmt), [JNXRL](#jnxrl), [JNXRO](#jnxro), [JPAT](#jpat), [JQMT](#jqmt), [JSE1](#jse1), [JSE2](#jse2), [JSE3](#jse3), [JSE4](#jse4), [JXFI](#jxfi), [JXMT](#jxmt), [JXRL](#jxrl), [JXRO](#jxro), [POLLATN](#pollatn), [POLLCT1](#pollct1), [POLLCT2](#pollct2), [POLLCT3](#pollct3), [POLLFBW](#pollfbw), [POLLINT](#pollint), [POLLPAT](#pollpat), [POLLQMT](#pollqmt), [POLLSE1](#pollse1), [POLLSE2](#pollse2), [POLLSE3](#pollse3), [POLLSE4](#pollse4), [POLLXFI](#pollxfi), [POLLXMT](#pollxmt), [POLLXRL](#pollxrl), [POLLXRO](#pollxro), [SETPAT](#setpat), [SETSE1](#setse1), [SETSE2](#setse2), [SETSE3](#setse3), [SETSE4](#setse4), [WAITATN](#waitatn), [WAITCT1](#waitct1), [WAITCT2](#waitct2), [WAITCT3](#waitct3), [WAITFBW](#waitfbw), [WAITINT](#waitint), [WAITPAT](#waitpat), [WAITSE1](#waitse1), [WAITSE2](#waitse2), [WAITSE3](#waitse3), [WAITSE4](#waitse4), [WAITXFI](#waitxfi), [WAITXMT](#waitxmt), [WAITXRL](#waitxrl), [WAITXRO](#waitxro)

---

## Interrupts {#interrupts}

Interrupt instructions control the cog's three-level interrupt system (INT1, INT2, INT3) plus the debug interrupt (INT0). This includes enabling/disabling interrupts, configuring interrupt sources, triggering software interrupts, and managing breakpoints for debugging.

[ALLOWI](#allowi), [BRK](#brk), [COGBRK](#cogbrk), [GETBRK](#getbrk), [NIXINT1](#nixint1), [NIXINT2](#nixint2), [NIXINT3](#nixint3), [SETINT1](#setint1), [SETINT2](#setint2), [SETINT3](#setint3), [STALLI](#stalli), [TRGINT1](#trgint1), [TRGINT2](#trgint2), [TRGINT3](#trgint3)

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

## Register Indirection {#register-indirection}

Register indirection instructions modify subsequent instructions by dynamically altering their source, destination, or bit index fields. They enable register arrays, computed addressing, and self-modifying code patterns essential for efficient data structure access.

[ALTB](#altb), [ALTD](#altd), [ALTGB](#altgb), [ALTGN](#altgn), [ALTGW](#altgw), [ALTI](#alti), [ALTR](#altr), [ALTS](#alts), [ALTSB](#altsb), [ALTSN](#altsn), [ALTSW](#altsw)

---

## Miscellaneous {#miscellaneous}

Miscellaneous instructions provide utility functions including immediate value extension (AUGS/AUGD), stack operations, random number generation, system timer access, and delay insertion.

[AUGD](#augd), [AUGS](#augs), [GETCT](#getct), [GETRND](#getrnd), [NOP](#nop), [POP](#pop), [PUSH](#push), [SETQ](#setq), [SETQ2](#setq2), [WAITX](#waitx)
