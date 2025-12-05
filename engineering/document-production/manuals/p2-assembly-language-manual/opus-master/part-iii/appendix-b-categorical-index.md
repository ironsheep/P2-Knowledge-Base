# Appendix B: Categorical Instruction Index

This appendix organizes P2 instructions by functional category, helping you find instructions based on what you want to accomplish rather than by alphabetical order. Each instruction name links to its detailed reference in Part II.

For a quick overview of each category with compact instruction lists, see [Instruction Categories](#instruction-categories) in Part II.


## Arithmetic Operations {#arithmetic-operations-ref}

Arithmetic instructions perform mathematical and logical operations on register values. This includes addition, subtraction, multiplication, comparisons, bitwise operations (AND, OR, XOR), bit manipulation, shifts, rotates, and data movement. This is the largest instruction category.

| Instruction | Description |
|-------------|-------------|
| [ABS](#abs) | Get absolute value of D into D |
| [ADD](#add) | Add S into D |
| [ADDS](#adds) | Add S into D, signed |
| [ADDSX](#addsx) | Add (S + C) into D, signed and extended |
| [ADDX](#addx) | Add (S + C) into D, extended |
| [AND](#and) | AND S into D |
| [ANDN](#andn) | AND !S into D |
| [BITC](#bitc) | Bits D[S[9:5]+S[4:0]:S[4:0]] = C |
| [BITH](#bith) | Bits D[S[9:5]+S[4:0]:S[4:0]] = 1 |
| [BITL](#bitl) | Bits D[S[9:5]+S[4:0]:S[4:0]] = 0 |
| [BITNC](#bitnc) | Bits D[S[9:5]+S[4:0]:S[4:0]] = !C |
| [BITNOT](#bitnot) | Toggle bits D[S[9:5]+S[4:0]:S[4:0]] |
| [BITNZ](#bitnz) | Bits D[S[9:5]+S[4:0]:S[4:0]] = !Z |
| [BITRND](#bitrnd) | Bits D[S[9:5]+S[4:0]:S[4:0]] = RNDs |
| [BITZ](#bitz) | Bits D[S[9:5]+S[4:0]:S[4:0]] = Z |
| [BMASK](#bmask) | Get LSB-justified bit mask of size (D[4:0] + 1) into D |
| [CMP](#cmp) | Compare D to S |
| [CMPM](#cmpm) | Compare D to S, get MSB of difference into C |
| [CMPR](#cmpr) | Compare S to D (reverse) |
| [CMPS](#cmps) | Compare D to S, signed |
| [CMPSUB](#cmpsub) | Compare and subtract S from D if D >= S |
| [CMPSX](#cmpsx) | Compare D to (S + C), signed and extended |
| [CMPX](#cmpx) | Compare D to (S + C), extended |
| [CRCBIT](#crcbit) | Iterate CRC value in D using C and polynomial in S |
| [CRCNIB](#crcnib) | Iterate CRC value in D using Q[31:28] and polynomial in S |
| [DECMOD](#decmod) | Decrement with modulus |
| [DECOD](#decod) | Decode D[4:0] into D |
| [ENCOD](#encod) | Get bit position of top-most '1' in D into D |
| [FGE](#fge) | Force D >= S |
| [FGES](#fges) | Force D >= S, signed |
| [FLE](#fle) | Force D <= S |
| [FLES](#fles) | Force D <= S, signed |
| [GETBYTE](#getbyte) | Get byte established by prior ALTGB instruction into D |
| [GETNIB](#getnib) | Get nibble established by prior ALTGN instruction into D |
| [GETWORD](#getword) | Get word established by prior ALTGW instruction into D |
| [INCMOD](#incmod) | Increment with modulus |
| [LOC](#loc) | Get {12'b0, address[19:0]} into PA/PB/PTRA/PTRB (per W) |
| [MERGEB](#mergeb) | Merge bits of bytes in D |
| [MERGEW](#mergew) | Merge bits of words in D |
| [MODC](#modc) | Modify C according to cccc |
| [MODCZ](#modcz) | Modify C and Z according to cccc and zzzz |
| [MODZ](#modz) | Modify Z according to zzzz |
| [MOV](#mov) | Move S into D |
| [MOVBYTS](#movbyts) | Move bytes within D, per S |
| [MUL](#mul) | D = unsigned (D[15:0] * S[15:0]) |
| [MULS](#muls) | D = signed (D[15:0] * S[15:0]) |
| [MUXC](#muxc) | Mux C into each D bit that is '1' in S |
| [MUXNC](#muxnc) | Mux !C into each D bit that is '1' in S |
| [MUXNIBS](#muxnibs) | For each non-zero nibble in S, copy that nibble into the corresponding D nibble |
| [MUXNITS](#muxnits) | For each non-zero bit pair in S, copy that bit pair into the corresponding D bits |
| [MUXNZ](#muxnz) | Mux !Z into each D bit that is '1' in S |
| [MUXQ](#muxq) | Used after SETQ |
| [MUXZ](#muxz) | Mux Z into each D bit that is '1' in S |
| [NEG](#neg) | Negate D |
| [NEGC](#negc) | Negate D by C |
| [NEGNC](#negnc) | Negate D by !C |
| [NEGNZ](#negnz) | Negate D by !Z |
| [NEGZ](#negz) | Negate D by Z |
| [NOT](#not) | Get !D into D |
| [ONES](#ones) | Get number of '1's in D into D |
| [OR](#or) | OR S into D |
| [RCL](#rcl) | Rotate carry left |
| [RCR](#rcr) | Rotate carry right |
| [RCZL](#rczl) | Rotate C,Z left through D |
| [RCZR](#rczr) | Rotate C,Z right through D |
| [REV](#rev) | Reverse D bits |
| [RGBEXP](#rgbexp) | Expand 5:6:5 RGB value in D[15:0] into 8:8:8 value in D[31:8] |
| [RGBSQZ](#rgbsqz) | Squeeze 8:8:8 RGB value in D[31:8] into 5:6:5 value in D[15:0] |
| [ROL](#rol) | Rotate left |
| [ROLBYTE](#rolbyte) | Rotate-left byte established by prior ALTGB instruction into D |
| [ROLNIB](#rolnib) | Rotate-left nibble established by prior ALTGN instruction into D |
| [ROLWORD](#rolword) | Rotate-left word established by prior ALTGW instruction into D |
| [ROR](#ror) | Rotate right |
| [SAL](#sal) | Shift arithmetic left |
| [SAR](#sar) | Shift arithmetic right |
| [SCA](#sca) | Next instruction's S value = unsigned (D[15:0] * S[15:0]) >> 16 |
| [SCAS](#scas) | Next instruction's S value = signed (D[15:0] * S[15:0]) >> 14 |
| [SETBYTE](#setbyte) | Set S[7:0] into byte established by prior ALTSB instruction |
| [SETD](#setd) | Set D field of D to S[8:0] |
| [SETNIB](#setnib) | Set S[3:0] into nibble established by prior ALTSN instruction |
| [SETR](#setr) | Set R field of D to S[8:0] |
| [SETS](#sets) | Set S field of D to S[8:0] |
| [SETWORD](#setword) | Set S[15:0] into word established by prior ALTSW instruction |
| [SEUSSF](#seussf) | Relocate and periodically invert bits within D |
| [SEUSSR](#seussr) | Relocate and periodically invert bits within D |
| [SHL](#shl) | Shift left |
| [SHR](#shr) | Shift right |
| [SIGNX](#signx) | Sign-extend D from bit S[4:0] |
| [SPLITB](#splitb) | Split every 4th bit of D into bytes |
| [SPLITW](#splitw) | Split odd/even bits of D into words |
| [SUB](#sub) | Subtract S from D |
| [SUBR](#subr) | Subtract D from S (reverse) |
| [SUBS](#subs) | Subtract S from D, signed |
| [SUBSX](#subsx) | Subtract (S + C) from D, signed and extended |
| [SUBX](#subx) | Subtract (S + C) from D, extended |
| [SUMC](#sumc) | Sum +/-S into D by C |
| [SUMNC](#sumnc) | Sum +/-S into D by !C |
| [SUMNZ](#sumnz) | Sum +/-S into D by !Z |
| [SUMZ](#sumz) | Sum +/-S into D by Z |
| [TEST](#test) | Test D |
| [TESTB](#testb) | Test bit S[4:0] of D, XOR into C/Z |
| [TESTBN](#testbn) | Test bit S[4:0] of !D, XOR into C/Z |
| [TESTN](#testn) | Test D with !S |
| [WRC](#wrc) | Write 0 or 1 to D, according to C |
| [WRNC](#wrnc) | Write 0 or 1 to D, according to !C |
| [WRNZ](#wrnz) | Write 0 or 1 to D, according to !Z |
| [WRZ](#wrz) | Write 0 or 1 to D, according to Z |
| [XOR](#xor) | XOR S into D |
| [XORO32](#xoro32) | Iterate D with xoroshiro32+ PRNG algorithm |
| [ZEROX](#zerox) | Zero-extend D above bit S[4:0] |


## Branching and Flow Control {#branching-and-flow-control-ref}

Branch instructions control program flow by modifying the program counter. This category includes conditional and unconditional jumps, subroutine calls using stack or pointer registers, returns from subroutines and interrupts, and instruction skipping/repeating mechanisms.

### Jump Instructions

| Instruction | Description |
|-------------|-------------|
| [JMP](#jmp) | Jump to A |
| [JMPREL](#jmprel) | Jump ahead/back by D instructions |

### Call Instructions

| Instruction | Description |
|-------------|-------------|
| [CALL](#call) | Call to A by pushing {C, Z, 10'b0, PC[19:0]} onto stack |
| [CALLA](#calla) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRA++ |
| [CALLB](#callb) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRB++ |
| [CALLD](#calld) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to PA/PB/PTRA/PTRB (per W) |
| [CALLPA](#callpa) | Call to S by pushing return onto stack, copy D to PA |
| [CALLPB](#callpb) | Call to S by pushing return onto stack, copy D to PB |

### Return Instructions

| Instruction | Description |
|-------------|-------------|
| [RET](#ret) | Return by popping stack |
| [RETA](#reta) | Return by reading hub long at --PTRA |
| [RETB](#retb) | Return by reading hub long at --PTRB |
| [RETI0](#reti0) | Return from INT0 |
| [RETI1](#reti1) | Return from INT1 |
| [RETI2](#reti2) | Return from INT2 |
| [RETI3](#reti3) | Return from INT3 |
| [RESI0](#resi0) | Resume from INT0 |
| [RESI1](#resi1) | Resume from INT1 |
| [RESI2](#resi2) | Resume from INT2 |
| [RESI3](#resi3) | Resume from INT3 |

### Test and Branch Instructions

| Instruction | Description |
|-------------|-------------|
| [TJF](#tjf) | Test D and jump to S if D is full ($FFFF_FFFF) |
| [TJNF](#tjnf) | Test D and jump to S if D is not full |
| [TJNS](#tjns) | Test D and jump to S if D is not signed (D[31] = 0) |
| [TJNZ](#tjnz) | Test D and jump to S if D is not zero |
| [TJS](#tjs) | Test D and jump to S if D is signed (D[31] = 1) |
| [TJV](#tjv) | Test D and jump to S if D overflowed |
| [TJZ](#tjz) | Test D and jump to S if D is zero |
| [DJF](#djf) | Decrement D and jump to S if result is $FFFF_FFFF |
| [DJNF](#djnf) | Decrement D and jump to S if result is not $FFFF_FFFF |
| [DJNZ](#djnz) | Decrement D and jump to S if result is not zero |
| [DJZ](#djz) | Decrement D and jump to S if result is zero |
| [IJNZ](#ijnz) | Increment D and jump to S if result is not zero |
| [IJZ](#ijz) | Increment D and jump to S if result is zero |

### Skip and Repeat Instructions

| Instruction | Description |
|-------------|-------------|
| [SKIP](#skip) | Skip instructions per D |
| [SKIPF](#skipf) | Skip cog/LUT instructions fast per D |
| [EXECF](#execf) | Jump to D[9:0] in cog/LUT and set SKIPF pattern to D[31:10] |
| [REP](#rep) | Execute next D[8:0] instructions S times |


## Hub Memory Access {#hub-memory-access-ref}

Hub memory instructions transfer data between cog registers and the shared 512KB hub RAM. This includes byte, word, and long access with various addressing modes, pointer-based operations using PTRA/PTRB, and high-speed FIFO streaming for bulk data transfers.

### Hub RAM Read

| Instruction | Description |
|-------------|-------------|
| [POPA](#popa) | Read long from hub address --PTRA into D |
| [POPB](#popb) | Read long from hub address --PTRB into D |
| [RDBYTE](#rdbyte) | Read zero-extended byte from hub address into D |
| [RDLONG](#rdlong) | Read long from hub address into D |
| [RDWORD](#rdword) | Read zero-extended word from hub address into D |

### Hub RAM Write

| Instruction | Description |
|-------------|-------------|
| [PUSHA](#pusha) | Write long in D to hub address PTRA++ |
| [PUSHB](#pushb) | Write long in D to hub address PTRB++ |
| [WMLONG](#wmlong) | Write only non-$00 bytes in D to hub address |
| [WRBYTE](#wrbyte) | Write byte in D[7:0] to hub address |
| [WRLONG](#wrlong) | Write long in D to hub address |
| [WRWORD](#wrword) | Write word in D[15:0] to hub address |

### Hub FIFO

| Instruction | Description |
|-------------|-------------|
| [GETPTR](#getptr) | Get current FIFO hub pointer into D |
| [RDFAST](#rdfast) | Begin new fast hub read via FIFO |
| [WRFAST](#wrfast) | Begin new fast hub write via FIFO |
| [FBLOCK](#fblock) | Set next block for when block wraps |
| [RFBYTE](#rfbyte) | Read byte from FIFO (after RDFAST) |
| [RFLONG](#rflong) | Read long from FIFO (after RDFAST) |
| [RFVAR](#rfvar) | Read variable-length value from FIFO |
| [RFVARS](#rfvars) | Read signed variable-length value from FIFO |
| [RFWORD](#rfword) | Read word from FIFO (after RDFAST) |
| [WFBYTE](#wfbyte) | Write byte to FIFO (after WRFAST) |
| [WFLONG](#wflong) | Write long to FIFO (after WRFAST) |
| [WFWORD](#wfword) | Write word to FIFO (after WRFAST) |


## Lookup Table {#lookup-table-ref}

Lookup table (LUT) instructions access the 512-long LUT memory private to each cog. The LUT provides fast table lookups, additional register storage, and can be shared between adjacent cog pairs for inter-cog communication.

| Instruction | Description |
|-------------|-------------|
| [RDLUT](#rdlut) | Read data from LUT address into D |
| [SETLUTS](#setluts) | Enable/disable LUT sharing with adjacent cog |
| [WRLUT](#wrlut) | Write D to LUT address |


## Pin I/O and Smart Pins {#pin-io-and-smart-pins-ref}

Pin instructions control the P2's 64 I/O pins. Basic pin operations set direction (input/output) and output level (high/low). Smart pin instructions configure and communicate with the autonomous smart pin state machines that can perform complex I/O functions independent of cog processing.

### Direction Control

| Instruction | Description |
|-------------|-------------|
| [DIRC](#dirc) | DIR bits of pins = C |
| [DIRH](#dirh) | DIR bits of pins = 1 (output) |
| [DIRL](#dirl) | DIR bits of pins = 0 (input) |
| [DIRNC](#dirnc) | DIR bits of pins = !C |
| [DIRNOT](#dirnot) | Toggle DIR bits of pins |
| [DIRNZ](#dirnz) | DIR bits of pins = !Z |
| [DIRRND](#dirrnd) | DIR bits of pins = random |
| [DIRZ](#dirz) | DIR bits of pins = Z |

### Output Control

| Instruction | Description |
|-------------|-------------|
| [OUTC](#outc) | OUT bits of pins = C |
| [OUTH](#outh) | OUT bits of pins = 1 (high) |
| [OUTL](#outl) | OUT bits of pins = 0 (low) |
| [OUTNC](#outnc) | OUT bits of pins = !C |
| [OUTNOT](#outnot) | Toggle OUT bits of pins |
| [OUTNZ](#outnz) | OUT bits of pins = !Z |
| [OUTRND](#outrnd) | OUT bits of pins = random |
| [OUTZ](#outz) | OUT bits of pins = Z |

### Drive Control (Direction + Output)

| Instruction | Description |
|-------------|-------------|
| [DRVC](#drvc) | Set pins to output, level = C |
| [DRVH](#drvh) | Set pins to output high |
| [DRVL](#drvl) | Set pins to output low |
| [DRVNC](#drvnc) | Set pins to output, level = !C |
| [DRVNOT](#drvnot) | Set pins to output, toggle level |
| [DRVNZ](#drvnz) | Set pins to output, level = !Z |
| [DRVRND](#drvrnd) | Set pins to output, random level |
| [DRVZ](#drvz) | Set pins to output, level = Z |

### Float Control (Input with Preset)

| Instruction | Description |
|-------------|-------------|
| [FLTC](#fltc) | Set pins to input, preset output = C |
| [FLTH](#flth) | Set pins to input, preset output high |
| [FLTL](#fltl) | Set pins to input, preset output low |
| [FLTNC](#fltnc) | Set pins to input, preset output = !C |
| [FLTNOT](#fltnot) | Set pins to input, toggle preset output |
| [FLTNZ](#fltnz) | Set pins to input, preset output = !Z |
| [FLTRND](#fltrnd) | Set pins to input, random preset output |
| [FLTZ](#fltz) | Set pins to input, preset output = Z |

### Pin Testing

| Instruction | Description |
|-------------|-------------|
| [TESTP](#testp) | Test IN bit of pin, XOR into C/Z |
| [TESTPN](#testpn) | Test !IN bit of pin, XOR into C/Z |

### Smart Pin Control

| Instruction | Description |
|-------------|-------------|
| [AKPIN](#akpin) | Acknowledge smart pin (clear flag) |
| [RDPIN](#rdpin) | Read smart pin result, acknowledge |
| [RQPIN](#rqpin) | Read smart pin result, don't acknowledge |
| [WRPIN](#wrpin) | Set mode of smart pin |
| [WXPIN](#wxpin) | Set X parameter of smart pin |
| [WYPIN](#wypin) | Set Y parameter of smart pin |
| [SETDACS](#setdacs) | Set all four DAC channels |
| [GETSCP](#getscp) | Get four-channel oscilloscope samples |
| [SETSCP](#setscp) | Set oscilloscope enable and input pin base |


## Events and Timing {#events-and-timing-ref}

Event instructions monitor and respond to system events including counter/timer triggers, smart pin signals, FIFO status, streamer conditions, and inter-cog attention signals. They provide configuration, polling, waiting, and conditional branching mechanisms for synchronization.

### Event Configuration

| Instruction | Description |
|-------------|-------------|
| [ADDCT1](#addct1) | Set CT1 event to trigger on CT = D + S |
| [ADDCT2](#addct2) | Set CT2 event to trigger on CT = D + S |
| [ADDCT3](#addct3) | Set CT3 event to trigger on CT = D + S |
| [SETPAT](#setpat) | Set pin pattern for PAT event |
| [SETSE1](#setse1) | Set SE1 event configuration |
| [SETSE2](#setse2) | Set SE2 event configuration |
| [SETSE3](#setse3) | Set SE3 event configuration |
| [SETSE4](#setse4) | Set SE4 event configuration |

### Event Polling

| Instruction | Description |
|-------------|-------------|
| [POLLATN](#pollatn) | Get ATN event flag into C/Z, then clear |
| [POLLCT1](#pollct1) | Get CT1 event flag into C/Z, then clear |
| [POLLCT2](#pollct2) | Get CT2 event flag into C/Z, then clear |
| [POLLCT3](#pollct3) | Get CT3 event flag into C/Z, then clear |
| [POLLFBW](#pollfbw) | Get FBW event flag into C/Z, then clear |
| [POLLINT](#pollint) | Get INT event flag into C/Z, then clear |
| [POLLPAT](#pollpat) | Get PAT event flag into C/Z, then clear |
| [POLLQMT](#pollqmt) | Get QMT event flag into C/Z, then clear |
| [POLLSE1](#pollse1) | Get SE1 event flag into C/Z, then clear |
| [POLLSE2](#pollse2) | Get SE2 event flag into C/Z, then clear |
| [POLLSE3](#pollse3) | Get SE3 event flag into C/Z, then clear |
| [POLLSE4](#pollse4) | Get SE4 event flag into C/Z, then clear |
| [POLLXFI](#pollxfi) | Get XFI event flag into C/Z, then clear |
| [POLLXMT](#pollxmt) | Get XMT event flag into C/Z, then clear |
| [POLLXRL](#pollxrl) | Get XRL event flag into C/Z, then clear |
| [POLLXRO](#pollxro) | Get XRO event flag into C/Z, then clear |

### Event Waiting

| Instruction | Description |
|-------------|-------------|
| [WAITATN](#waitatn) | Wait for ATN event flag, then clear |
| [WAITCT1](#waitct1) | Wait for CT1 event flag, then clear |
| [WAITCT2](#waitct2) | Wait for CT2 event flag, then clear |
| [WAITCT3](#waitct3) | Wait for CT3 event flag, then clear |
| [WAITFBW](#waitfbw) | Wait for FBW event flag, then clear |
| [WAITINT](#waitint) | Wait for INT event flag, then clear |
| [WAITPAT](#waitpat) | Wait for PAT event flag, then clear |
| [WAITSE1](#waitse1) | Wait for SE1 event flag, then clear |
| [WAITSE2](#waitse2) | Wait for SE2 event flag, then clear |
| [WAITSE3](#waitse3) | Wait for SE3 event flag, then clear |
| [WAITSE4](#waitse4) | Wait for SE4 event flag, then clear |
| [WAITXFI](#waitxfi) | Wait for XFI event flag, then clear |
| [WAITXMT](#waitxmt) | Wait for XMT event flag, then clear |
| [WAITXRL](#waitxrl) | Wait for XRL event flag, then clear |
| [WAITXRO](#waitxro) | Wait for XRO event flag, then clear |

### Event Branching

| Instruction | Description |
|-------------|-------------|
| [JATN](#jatn) | Jump to S if ATN event flag is set |
| [JCT1](#jct1) | Jump to S if CT1 event flag is set |
| [JCT2](#jct2) | Jump to S if CT2 event flag is set |
| [JCT3](#jct3) | Jump to S if CT3 event flag is set |
| [JFBW](#jfbw) | Jump to S if FBW event flag is set |
| [JINT](#jint) | Jump to S if INT event flag is set |
| [JNATN](#jnatn) | Jump to S if ATN event flag is clear |
| [JNCT1](#jnct1) | Jump to S if CT1 event flag is clear |
| [JNCT2](#jnct2) | Jump to S if CT2 event flag is clear |
| [JNCT3](#jnct3) | Jump to S if CT3 event flag is clear |
| [JNFBW](#jnfbw) | Jump to S if FBW event flag is clear |
| [JNINT](#jnint) | Jump to S if INT event flag is clear |
| [JNPAT](#jnpat) | Jump to S if PAT event flag is clear |
| [JNQMT](#jnqmt) | Jump to S if QMT event flag is clear |
| [JNSE1](#jnse1) | Jump to S if SE1 event flag is clear |
| [JNSE2](#jnse2) | Jump to S if SE2 event flag is clear |
| [JNSE3](#jnse3) | Jump to S if SE3 event flag is clear |
| [JNSE4](#jnse4) | Jump to S if SE4 event flag is clear |
| [JNXFI](#jnxfi) | Jump to S if XFI event flag is clear |
| [JNXMT](#jnxmt) | Jump to S if XMT event flag is clear |
| [JNXRL](#jnxrl) | Jump to S if XRL event flag is clear |
| [JNXRO](#jnxro) | Jump to S if XRO event flag is clear |
| [JPAT](#jpat) | Jump to S if PAT event flag is set |
| [JQMT](#jqmt) | Jump to S if QMT event flag is set |
| [JSE1](#jse1) | Jump to S if SE1 event flag is set |
| [JSE2](#jse2) | Jump to S if SE2 event flag is set |
| [JSE3](#jse3) | Jump to S if SE3 event flag is set |
| [JSE4](#jse4) | Jump to S if SE4 event flag is set |
| [JXFI](#jxfi) | Jump to S if XFI event flag is set |
| [JXMT](#jxmt) | Jump to S if XMT event flag is set |
| [JXRL](#jxrl) | Jump to S if XRL event flag is set |
| [JXRO](#jxro) | Jump to S if XRO event flag is set |

### Inter-COG Attention

| Instruction | Description |
|-------------|-------------|
| [COGATN](#cogatn) | Strobe attention of cogs whose bits are high in D[15:0] |


## Interrupts {#interrupts-ref}

Interrupt instructions control the cog's three-level interrupt system (INT1, INT2, INT3) plus the debug interrupt (INT0). This includes enabling/disabling interrupts, configuring interrupt sources, triggering software interrupts, and managing breakpoints for debugging.

| Instruction | Description |
|-------------|-------------|
| [ALLOWI](#allowi) | Allow interrupts (default) |
| [BRK](#brk) | If in debug ISR, set next break condition to D |
| [COGBRK](#cogbrk) | If in debug ISR, trigger breakpoint in cog D[3:0] |
| [GETBRK](#getbrk) | Get breakpoint/cog status into D |
| [NIXINT1](#nixint1) | Cancel INT1 |
| [NIXINT2](#nixint2) | Cancel INT2 |
| [NIXINT3](#nixint3) | Cancel INT3 |
| [SETINT1](#setint1) | Set INT1 source to D[3:0] |
| [SETINT2](#setint2) | Set INT2 source to D[3:0] |
| [SETINT3](#setint3) | Set INT3 source to D[3:0] |
| [STALLI](#stalli) | Stall interrupts |
| [TRGINT1](#trgint1) | Trigger INT1, regardless of STALLI mode |
| [TRGINT2](#trgint2) | Trigger INT2, regardless of STALLI mode |
| [TRGINT3](#trgint3) | Trigger INT3, regardless of STALLI mode |


## COG Control and Locks {#cog-control-and-locks-ref}

COG control instructions manage cog operations including starting and stopping cogs, querying cog identity, and configuring hub-level system settings. Lock instructions provide mutex-style synchronization primitives for safe inter-cog resource sharing.

### COG Control

| Instruction | Description |
|-------------|-------------|
| [COGID](#cogid) | Get cog ID (0 to 15) into D |
| [COGINIT](#coginit) | Start cog selected by D |
| [COGSTOP](#cogstop) | Stop cog D[3:0] |
| [HUBSET](#hubset) | Set hub configuration to D |

### Locks

| Instruction | Description |
|-------------|-------------|
| [LOCKNEW](#locknew) | Request a lock from the pool |
| [LOCKREL](#lockrel) | Release lock D[3:0] |
| [LOCKRET](#lockret) | Return lock D[3:0] for reallocation |
| [LOCKTRY](#locktry) | Try to get lock D[3:0] |


## CORDIC Coprocessor {#cordic-coprocessor-ref}

CORDIC (Coordinate Rotation Digital Computer) instructions provide hardware-accelerated mathematical operations. The dedicated coprocessor performs multiplication, division, square root, trigonometric functions, logarithms, and coordinate transformations with high precision.

| Instruction | Description |
|-------------|-------------|
| [GETQX](#getqx) | Retrieve CORDIC result X into D |
| [GETQY](#getqy) | Retrieve CORDIC result Y into D |
| [QDIV](#qdiv) | Begin CORDIC unsigned division |
| [QEXP](#qexp) | Begin CORDIC logarithm-to-number conversion |
| [QFRAC](#qfrac) | Begin CORDIC fractional division |
| [QLOG](#qlog) | Begin CORDIC number-to-logarithm conversion |
| [QMUL](#qmul) | Begin CORDIC unsigned multiplication |
| [QROTATE](#qrotate) | Begin CORDIC rotation of point by angle |
| [QSQRT](#qsqrt) | Begin CORDIC square root |
| [QVECTOR](#qvector) | Begin CORDIC vectoring of point |


## Streamer {#streamer-ref}

Streamer instructions control the cog's dedicated DMA engine that autonomously transfers data between hub memory, LUT, and I/O pins. The streamer is essential for high-bandwidth applications like video output, audio streaming, and bulk data movement.

| Instruction | Description |
|-------------|-------------|
| [GETXACC](#getxacc) | Get Goertzel X and Y accumulators, clear them |
| [SETXFRQ](#setxfrq) | Set streamer NCO frequency to D |
| [XCONT](#xcont) | Buffer new streamer command, continue phase |
| [XINIT](#xinit) | Issue streamer command immediately, zero phase |
| [XSTOP](#xstop) | Stop streamer immediately |
| [XZERO](#xzero) | Buffer new streamer command, zero phase |


## Color Space and Pixel Operations {#color-space-and-pixel-operations-ref}

Color space and pixel instructions provide hardware-accelerated graphics processing. The colorspace converter transforms between color representations (RGB, YUV). The pixel mixer performs alpha blending, color addition, and format conversions for video and graphics applications.

### Color Space Converter

| Instruction | Description |
|-------------|-------------|
| [SETCFRQ](#setcfrq) | Set colorspace converter CFRQ parameter |
| [SETCI](#setci) | Set colorspace converter CI parameter |
| [SETCMOD](#setcmod) | Set colorspace converter CMOD parameter |
| [SETCQ](#setcq) | Set colorspace converter CQ parameter |
| [SETCY](#setcy) | Set colorspace converter CY parameter |

### Pixel Mixer

| Instruction | Description |
|-------------|-------------|
| [ADDPIX](#addpix) | Add bytes of S into bytes of D with saturation |
| [BLNPIX](#blnpix) | Alpha-blend bytes of S into bytes of D |
| [MIXPIX](#mixpix) | Mix bytes of S into bytes of D |
| [MULPIX](#mulpix) | Multiply bytes of S into bytes of D |
| [SETPIV](#setpiv) | Set BLNPIX/MIXPIX blend factor |
| [SETPIX](#setpix) | Set MIXPIX mode |


## Instruction Modification {#instruction-modification-ref}

Instruction modification instructions (also known as register indirection) dynamically alter subsequent instructions by changing their source, destination, or bit index fields before execution. They enable register arrays, computed addressing, and self-modifying code patterns essential for efficient data structure access.

| Instruction | Description |
|-------------|-------------|
| [ALTB](#altb) | Alter D field of next instruction to D[13:5] |
| [ALTD](#altd) | Alter D field of next instruction to D[8:0] |
| [ALTGB](#altgb) | Alter subsequent GETBYTE/ROLBYTE instruction |
| [ALTGN](#altgn) | Alter subsequent GETNIB/ROLNIB instruction |
| [ALTGW](#altgw) | Alter subsequent GETWORD/ROLWORD instruction |
| [ALTI](#alti) | Execute D in place of next instruction |
| [ALTR](#altr) | Alter result register address of next instruction |
| [ALTS](#alts) | Alter S field of next instruction to D[8:0] |
| [ALTSB](#altsb) | Alter subsequent SETBYTE instruction |
| [ALTSN](#altsn) | Alter subsequent SETNIB instruction |
| [ALTSW](#altsw) | Alter subsequent SETWORD instruction |


## Miscellaneous {#miscellaneous-ref}

Miscellaneous instructions provide utility functions including immediate value extension (AUGS/AUGD), stack operations, random number generation, system timer access, and delay insertion.

| Instruction | Description |
|-------------|-------------|
| [AUGD](#augd) | Extend next instruction's D immediate to 32 bits |
| [AUGS](#augs) | Extend next instruction's S immediate to 32 bits |
| [GETCT](#getct) | Get CT[31:0] or CT[63:32] if WC into D |
| [GETRND](#getrnd) | Get random number into D and/or C/Z |
| [NOP](#nop) | No operation |
| [POP](#pop) | Pop stack into D |
| [PUSH](#push) | Push D onto stack |
| [SETQ](#setq) | Set Q register to D |
| [SETQ2](#setq2) | Set Q register to D (for LUT transfers) |
| [WAITX](#waitx) | Wait 2 + D clocks |

