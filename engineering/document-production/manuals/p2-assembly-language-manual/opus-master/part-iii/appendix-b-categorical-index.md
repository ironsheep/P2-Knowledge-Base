# Appendix B: Categorical Instruction Index

This appendix organizes P2 instructions by functional category, helping you find instructions based on what you want to accomplish rather than by alphabetical order.

Each instruction name links to its detailed reference in Part II.


## Arithmetic Operations

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
| [GETBYTE](#getbyte) | Get byte established by prior ALTGB instruction into D. |
| [GETNIB](#getnib) | Get nibble established by prior ALTGN instruction into D. |
| [GETWORD](#getword) | Get word established by prior ALTGW instruction into D. |
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
| [MUXNIBS](#muxnibs) | For each non-zero nibble in S, copy that nibble into the corresponding D nibble, else leave that D nibble the same. |
| [MUXNITS](#muxnits) | For each non-zero bit pair in S, copy that bit pair into the corresponding D bits, else leave that D bit pair the same. |
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
| [ROLBYTE](#rolbyte) | Rotate-left byte established by prior ALTGB instruction into D. |
| [ROLNIB](#rolnib) | Rotate-left nibble established by prior ALTGN instruction into D. |
| [ROLWORD](#rolword) | Rotate-left word established by prior ALTGW instruction into D. |
| [ROR](#ror) | Rotate right |
| [SAL](#sal) | Shift arithmetic left |
| [SAR](#sar) | Shift arithmetic right |
| [SCA](#sca) | Next instruction's S value = unsigned (D[15:0] * S[15:0]) >> 16 |
| [SCAS](#scas) | Next instruction's S value = signed (D[15:0] * S[15:0]) >> 14 |
| [SETBYTE](#setbyte) | Set S[7:0] into byte established by prior ALTSB instruction. |
| [SETD](#setd) | Set D field of D to S[8:0] |
| [SETNIB](#setnib) | Set S[3:0] into nibble established by prior ALTSN instruction. |
| [SETR](#setr) | Set R field of D to S[8:0] |
| [SETS](#sets) | Set S field of D to S[8:0] |
| [SETWORD](#setword) | Set S[15:0] into word established by prior ALTSW instruction. |
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
| [XORO32](#xoro32) | Iterate D with xoroshiro32+ PRNG algorithm and put PRNG result into next instruction's S. |
| [ZEROX](#zerox) | Zero-extend D above bit S[4:0] |


## Branching and Flow Control


### Branch A - Jump

| Instruction | Description |
|-------------|-------------|
| [JMP](#jmp) | Jump to A |


### Branch A - Call

| Instruction | Description |
|-------------|-------------|
| [CALL](#call) | Call to A by pushing {C, Z, 10'b0, PC[19:0]} onto stack |
| [CALLA](#calla) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRA++ |
| [CALLB](#callb) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRB++ |
| [CALLD](#calld) | Call to A by writing {C, Z, 10'b0, PC[19:0]} to PA/PB/PTRA/PTRB (per W) |


### Branch D - Jump

| Instruction | Description |
|-------------|-------------|
| [JMPREL](#jmprel) | Jump ahead/back by D instructions |


### Branch D - Jump+Skip

| Instruction | Description |
|-------------|-------------|
| [SKIPF](#skipf) | Skip cog/LUT instructions fast per D |


### Branch D - Call+Skip

| Instruction | Description |
|-------------|-------------|
| [EXECF](#execf) | Jump to D[9:0] in cog/LUT and set SKIPF pattern to D[31:10] |


### Branch D - Skip

| Instruction | Description |
|-------------|-------------|
| [SKIP](#skip) | Skip instructions per D |


### Branch S - Call

| Instruction | Description |
|-------------|-------------|
| [CALLPA](#callpa) | Call to S** by pushing {C, Z, 10'b0, PC[19:0]} onto stack, copy D to PA. |
| [CALLPB](#callpb) | Call to S** by pushing {C, Z, 10'b0, PC[19:0]} onto stack, copy D to PB. |


### Branch S - Test

| Instruction | Description |
|-------------|-------------|
| [TJF](#tjf) | Test D and jump to S** if D is full (D = $FFFF_FFFF). |
| [TJNF](#tjnf) | Test D and jump to S** if D is not full (D != $FFFF_FFFF). |
| [TJNS](#tjns) | Test D and jump to S** if D is not signed (D[31] = 0). |
| [TJNZ](#tjnz) | Test D and jump to S** if D is not zero. |
| [TJS](#tjs) | Test D and jump to S** if D is signed (D[31] = 1). |
| [TJV](#tjv) | Test D and jump to S** if D overflowed (D[31] != C, C = 'correct sign' from last addition/subtraction). |
| [TJZ](#tjz) | Test D and jump to S** if D is zero. |


### Branch S - Mod & Test

| Instruction | Description |
|-------------|-------------|
| [DJF](#djf) | Decrement D and jump to S** if result is $FFFF_FFFF. |
| [DJNF](#djnf) | Decrement D and jump to S** if result is not $FFFF_FFFF. |
| [DJNZ](#djnz) | Decrement D and jump to S** if result is not zero. |
| [DJZ](#djz) | Decrement D and jump to S** if result is zero. |
| [IJNZ](#ijnz) | Increment D and jump to S** if result is not zero. |
| [IJZ](#ijz) | Increment D and jump to S** if result is zero. |


### Branch Return

| Instruction | Description |
|-------------|-------------|
| [RET](#ret) | Return by popping stack (K) |
| [RETA](#reta) | Return by reading hub long (L) at --PTRA |
| [RETB](#retb) | Return by reading hub long (L) at --PTRB |


### Branch S - Return

| Instruction | Description |
|-------------|-------------|
| [RETI0](#reti0) | Return from INT0 |
| [RETI1](#reti1) | Return from INT1 |
| [RETI2](#reti2) | Return from INT2 |
| [RETI3](#reti3) | Return from INT3 |


### Branch S - Resume

| Instruction | Description |
|-------------|-------------|
| [RESI0](#resi0) | Resume from INT0 |
| [RESI1](#resi1) | Resume from INT1 |
| [RESI2](#resi2) | Resume from INT2 |
| [RESI3](#resi3) | Resume from INT3 |


### Branch Repeat

| Instruction | Description |
|-------------|-------------|
| [REP](#rep) | Execute next D[8:0] instructions S times |


## Hub Memory Access


### Hub RAM - Read

| Instruction | Description |
|-------------|-------------|
| [POPA](#popa) | Read long from hub address --PTRA into D |
| [POPB](#popb) | Read long from hub address --PTRB into D |
| [RDBYTE](#rdbyte) | Read zero-extended byte from hub address {#}S/PTRx into D |
| [RDLONG](#rdlong) | Read long from hub address {#}S/PTRx into D |
| [RDWORD](#rdword) | Read zero-extended word from hub address {#}S/PTRx into D |


### Hub RAM - Write

| Instruction | Description |
|-------------|-------------|
| [PUSHA](#pusha) | Write long in D[31:0] to hub address PTRA++. |
| [PUSHB](#pushb) | Write long in D[31:0] to hub address PTRB++. |
| [WMLONG](#wmlong) | Write only non-$00 bytes in D[31:0] to hub address {#}S/PTRx |
| [WRBYTE](#wrbyte) | Write byte in D[7:0] to hub address {#}S/PTRx. |
| [WRLONG](#wrlong) | Write long in D[31:0] to hub address {#}S/PTRx |
| [WRWORD](#wrword) | Write word in D[15:0] to hub address {#}S/PTRx. |


### Hub FIFO

| Instruction | Description |
|-------------|-------------|
| [GETPTR](#getptr) | Get current FIFO hub pointer into D. |


### Hub FIFO - New Read

| Instruction | Description |
|-------------|-------------|
| [RDFAST](#rdfast) | Begin new fast hub read via FIFO |


### Hub FIFO - New Write

| Instruction | Description |
|-------------|-------------|
| [WRFAST](#wrfast) | Begin new fast hub write via FIFO |


### Hub FIFO - New Block

| Instruction | Description |
|-------------|-------------|
| [FBLOCK](#fblock) | Set next block for when block wraps |


### Hub FIFO - Read

| Instruction | Description |
|-------------|-------------|
| [RFBYTE](#rfbyte) | Used after RDFAST |
| [RFLONG](#rflong) | Used after RDFAST |
| [RFVAR](#rfvar) | Used after RDFAST |
| [RFVARS](#rfvars) | Used after RDFAST |
| [RFWORD](#rfword) | Used after RDFAST |


### Hub FIFO - Write

| Instruction | Description |
|-------------|-------------|
| [WFBYTE](#wfbyte) | Used after WRFAST |
| [WFLONG](#wflong) | Used after WRFAST |
| [WFWORD](#wfword) | Used after WRFAST |


## Lookup Table

| Instruction | Description |
|-------------|-------------|
| [RDLUT](#rdlut) | Read data from LUT address {#}S/PTRx into D |
| [SETLUTS](#setluts) | If D[0] = 1 then enable LUT sharing, where LUT writes within the adjacent odd/even companion cog are copied to this cog's LUT. |
| [WRLUT](#wrlut) | Write D to LUT address {#}S/PTRx. |


## Pin I/O and Smart Pins


### Pins

| Instruction | Description |
|-------------|-------------|
| [DIRC](#dirc) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = C |
| [DIRH](#dirh) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = 1 |
| [DIRL](#dirl) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = 0 |
| [DIRNC](#dirnc) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = !C |
| [DIRNOT](#dirnot) | Toggle DIR bits of pins D[10:6]+D[5:0]..D[5:0] |
| [DIRNZ](#dirnz) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = !Z |
| [DIRRND](#dirrnd) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs |
| [DIRZ](#dirz) | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = Z |
| [DRVC](#drvc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C |
| [DRVH](#drvh) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1 |
| [DRVL](#drvl) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0 |
| [DRVNC](#drvnc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C |
| [DRVNOT](#drvnot) | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0] |
| [DRVNZ](#drvnz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z |
| [DRVRND](#drvrnd) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs |
| [DRVZ](#drvz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z |
| [FLTC](#fltc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C |
| [FLTH](#flth) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1 |
| [FLTL](#fltl) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0 |
| [FLTNC](#fltnc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C |
| [FLTNOT](#fltnot) | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0] |
| [FLTNZ](#fltnz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z |
| [FLTRND](#fltrnd) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs |
| [FLTZ](#fltz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z |
| [OUTC](#outc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C |
| [OUTH](#outh) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1 |
| [OUTL](#outl) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0 |
| [OUTNC](#outnc) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C |
| [OUTNOT](#outnot) | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0] |
| [OUTNZ](#outnz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z |
| [OUTRND](#outrnd) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs |
| [OUTZ](#outz) | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z |
| [TESTP](#testp) | Test IN bit of pin D[5:0], XOR into C/Z |
| [TESTPN](#testpn) | Test !IN bit of pin D[5:0], XOR into C/Z |


### Smart Pins

| Instruction | Description |
|-------------|-------------|
| [AKPIN](#akpin) | Acknowledge smart pins S[10:6]+S[5:0]..S[5:0] |
| [GETSCP](#getscp) | Get four-channel oscilloscope samples into D |
| [RDPIN](#rdpin) | Read smart pin S[5:0] result "Z" into D, acknowledge smart pin |
| [RQPIN](#rqpin) | Read smart pin S[5:0] result "Z" into D, don't acknowledge smart pin ("Q" in RQPIN means "quiet") |
| [SETDACS](#setdacs) | DAC3 = D[31:24], DAC2 = D[23:16], DAC1 = D[15:8], DAC0 = D[7:0]. |
| [SETSCP](#setscp) | Set four-channel oscilloscope enable to D[6] and set input pin base to D[5:2]. |
| [WRPIN](#wrpin) | Set mode of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins |
| [WXPIN](#wxpin) | Set "X" of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins |
| [WYPIN](#wypin) | Set "Y" of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins |


## Events and Timing


### Events - Configuration

| Instruction | Description |
|-------------|-------------|
| [ADDCT1](#addct1) | Set CT1 event to trigger on CT = D + S |
| [ADDCT2](#addct2) | Set CT2 event to trigger on CT = D + S |
| [ADDCT3](#addct3) | Set CT3 event to trigger on CT = D + S |
| [SETPAT](#setpat) | Set pin pattern for PAT event |
| [SETSE1](#setse1) | Set SE1 event configuration to D[8:0]. |
| [SETSE2](#setse2) | Set SE2 event configuration to D[8:0]. |
| [SETSE3](#setse3) | Set SE3 event configuration to D[8:0]. |
| [SETSE4](#setse4) | Set SE4 event configuration to D[8:0]. |


### Events - Poll

| Instruction | Description |
|-------------|-------------|
| [POLLATN](#pollatn) | Get ATN event flag into C/Z, then clear it. |
| [POLLCT1](#pollct1) | Get CT1 event flag into C/Z, then clear it. |
| [POLLCT2](#pollct2) | Get CT2 event flag into C/Z, then clear it. |
| [POLLCT3](#pollct3) | Get CT3 event flag into C/Z, then clear it. |
| [POLLFBW](#pollfbw) | Get FBW event flag into C/Z, then clear it. |
| [POLLINT](#pollint) | Get INT event flag into C/Z, then clear it. |
| [POLLPAT](#pollpat) | Get PAT event flag into C/Z, then clear it. |
| [POLLQMT](#pollqmt) | Get QMT event flag into C/Z, then clear it. |
| [POLLSE1](#pollse1) | Get SE1 event flag into C/Z, then clear it. |
| [POLLSE2](#pollse2) | Get SE2 event flag into C/Z, then clear it. |
| [POLLSE3](#pollse3) | Get SE3 event flag into C/Z, then clear it. |
| [POLLSE4](#pollse4) | Get SE4 event flag into C/Z, then clear it. |
| [POLLXFI](#pollxfi) | Get XFI event flag into C/Z, then clear it. |
| [POLLXMT](#pollxmt) | Get XMT event flag into C/Z, then clear it. |
| [POLLXRL](#pollxrl) | Get XRL event flag into C/Z, then clear it. |
| [POLLXRO](#pollxro) | Get XRO event flag into C/Z, then clear it. |


### Events - Wait

| Instruction | Description |
|-------------|-------------|
| [WAITATN](#waitatn) | Wait for ATN event flag, then clear it |
| [WAITCT1](#waitct1) | Wait for CT1 event flag, then clear it |
| [WAITCT2](#waitct2) | Wait for CT2 event flag, then clear it |
| [WAITCT3](#waitct3) | Wait for CT3 event flag, then clear it |
| [WAITFBW](#waitfbw) | Wait for FBW event flag, then clear it |
| [WAITINT](#waitint) | Wait for INT event flag, then clear it |
| [WAITPAT](#waitpat) | Wait for PAT event flag, then clear it |
| [WAITSE1](#waitse1) | Wait for SE1 event flag, then clear it |
| [WAITSE2](#waitse2) | Wait for SE2 event flag, then clear it |
| [WAITSE3](#waitse3) | Wait for SE3 event flag, then clear it |
| [WAITSE4](#waitse4) | Wait for SE4 event flag, then clear it |
| [WAITXFI](#waitxfi) | Wait for XFI event flag, then clear it |
| [WAITXMT](#waitxmt) | Wait for XMT event flag, then clear it |
| [WAITXRL](#waitxrl) | Wait for XRL event flag, then clear it |
| [WAITXRO](#waitxro) | Wait for XRO event flag, then clear it |


### Events - Branch

| Instruction | Description |
|-------------|-------------|
| [JATN](#jatn) | Jump to S** if ATN event flag is set. |
| [JCT1](#jct1) | Jump to S** if CT1 event flag is set. |
| [JCT2](#jct2) | Jump to S** if CT2 event flag is set. |
| [JCT3](#jct3) | Jump to S** if CT3 event flag is set. |
| [JFBW](#jfbw) | Jump to S** if FBW event flag is set. |
| [JINT](#jint) | Jump to S** if INT event flag is set. |
| [JNATN](#jnatn) | Jump to S** if ATN event flag is clear. |
| [JNCT1](#jnct1) | Jump to S** if CT1 event flag is clear. |
| [JNCT2](#jnct2) | Jump to S** if CT2 event flag is clear. |
| [JNCT3](#jnct3) | Jump to S** if CT3 event flag is clear. |
| [JNFBW](#jnfbw) | Jump to S** if FBW event flag is clear. |
| [JNINT](#jnint) | Jump to S** if INT event flag is clear. |
| [JNPAT](#jnpat) | Jump to S** if PAT event flag is clear. |
| [JNQMT](#jnqmt) | Jump to S** if QMT event flag is clear. |
| [JNSE1](#jnse1) | Jump to S** if SE1 event flag is clear. |
| [JNSE2](#jnse2) | Jump to S** if SE2 event flag is clear. |
| [JNSE3](#jnse3) | Jump to S** if SE3 event flag is clear. |
| [JNSE4](#jnse4) | Jump to S** if SE4 event flag is clear. |
| [JNXFI](#jnxfi) | Jump to S** if XFI event flag is clear. |
| [JNXMT](#jnxmt) | Jump to S** if XMT event flag is clear. |
| [JNXRL](#jnxrl) | Jump to S** if XRL event flag is clear. |
| [JNXRO](#jnxro) | Jump to S** if XRO event flag is clear. |
| [JPAT](#jpat) | Jump to S** if PAT event flag is set. |
| [JQMT](#jqmt) | Jump to S** if QMT event flag is set. |
| [JSE1](#jse1) | Jump to S** if SE1 event flag is set. |
| [JSE2](#jse2) | Jump to S** if SE2 event flag is set. |
| [JSE3](#jse3) | Jump to S** if SE3 event flag is set. |
| [JSE4](#jse4) | Jump to S** if SE4 event flag is set. |
| [JXFI](#jxfi) | Jump to S** if XFI event flag is set. |
| [JXMT](#jxmt) | Jump to S** if XMT event flag is set. |
| [JXRL](#jxrl) | Jump to S** if XRL event flag is set. |
| [JXRO](#jxro) | Jump to S** if XRO event flag is set. |


### Events - Attention

| Instruction | Description |
|-------------|-------------|
| [COGATN](#cogatn) | Strobe "attention" of all cogs whose corresponging bits are high in D[15:0]. |


## Interrupts

| Instruction | Description |
|-------------|-------------|
| [ALLOWI](#allowi) | Allow interrupts (default). |
| [BRK](#brk) | If in debug ISR, set next break condition to D |
| [COGBRK](#cogbrk) | If in debug ISR, trigger asynchronous breakpoint in cog D[3:0] |
| [GETBRK](#getbrk) | Get breakpoint/cog status into D according to WC/WZ/WCZ |
| [NIXINT1](#nixint1) | Cancel INT1. |
| [NIXINT2](#nixint2) | Cancel INT2. |
| [NIXINT3](#nixint3) | Cancel INT3. |
| [SETINT1](#setint1) | Set INT1 source to D[3:0]. |
| [SETINT2](#setint2) | Set INT2 source to D[3:0]. |
| [SETINT3](#setint3) | Set INT3 source to D[3:0]. |
| [STALLI](#stalli) | Stall Interrupts. |
| [TRGINT1](#trgint1) | Trigger INT1, regardless of STALLI mode. |
| [TRGINT2](#trgint2) | Trigger INT2, regardless of STALLI mode. |
| [TRGINT3](#trgint3) | Trigger INT3, regardless of STALLI mode. |


## COG Control and Locks


### Hub Control - Cogs

| Instruction | Description |
|-------------|-------------|
| [COGID](#cogid) | If D is register and no WC, get cog ID (0 to 15) into D |
| [COGINIT](#coginit) | Start cog selected by D |
| [COGSTOP](#cogstop) | Stop cog D[3:0]. |


### Hub Control - Locks

| Instruction | Description |
|-------------|-------------|
| [LOCKNEW](#locknew) | Request a LOCK |
| [LOCKREL](#lockrel) | Release LOCK D[3:0] |
| [LOCKRET](#lockret) | Return LOCK D[3:0] for reallocation. |
| [LOCKTRY](#locktry) | Try to get LOCK D[3:0] |


### Hub Control - Multi

| Instruction | Description |
|-------------|-------------|
| [HUBSET](#hubset) | Set hub configuration to D. |


## CORDIC Coprocessor

| Instruction | Description |
|-------------|-------------|
| [GETQX](#getqx) | Retrieve CORDIC result X into D |
| [GETQY](#getqy) | Retrieve CORDIC result Y into D |
| [QDIV](#qdiv) | Begin CORDIC unsigned division of {SETQ value or 32'b0, D} / S |
| [QEXP](#qexp) | Begin CORDIC logarithm-to-number conversion of D |
| [QFRAC](#qfrac) | Begin CORDIC unsigned division of {D, SETQ value or 32'b0} / S |
| [QLOG](#qlog) | Begin CORDIC number-to-logarithm conversion of D |
| [QMUL](#qmul) | Begin CORDIC unsigned multiplication of D * S |
| [QROTATE](#qrotate) | Begin CORDIC rotation of point (D, SETQ value or 32'b0) by angle S |
| [QSQRT](#qsqrt) | Begin CORDIC square root of {S, D} |
| [QVECTOR](#qvector) | Begin CORDIC vectoring of point (D, S) |


## Streamer

| Instruction | Description |
|-------------|-------------|
| [GETXACC](#getxacc) | Get the streamer's Goertzel X accumulator into D and the Y accumulator into the next instruction's S, clear accumulators. |
| [SETXFRQ](#setxfrq) | Set streamer NCO frequency to D. |
| [XCONT](#xcont) | Buffer new streamer command to be issued on final NCO rollover of current command, continuing phase. |
| [XINIT](#xinit) | Issue streamer command immediately, zeroing phase. |
| [XSTOP](#xstop) | Stop streamer immediately. |
| [XZERO](#xzero) | Buffer new streamer command to be issued on final NCO rollover of current command, zeroing phase. |


## Color Space and Pixel Operations


### Color Space Converter

| Instruction | Description |
|-------------|-------------|
| [SETCFRQ](#setcfrq) | Set the colorspace converter "CFRQ" parameter to D[31:0]. |
| [SETCI](#setci) | Set the colorspace converter "CI" parameter to D[31:0]. |
| [SETCMOD](#setcmod) | Set the colorspace converter "CMOD" parameter to D[8:0]. |
| [SETCQ](#setcq) | Set the colorspace converter "CQ" parameter to D[31:0]. |
| [SETCY](#setcy) | Set the colorspace converter "CY" parameter to D[31:0]. |


### Pixel Mixer

| Instruction | Description |
|-------------|-------------|
| [ADDPIX](#addpix) | Add bytes of S into bytes of D, with $FF saturation. |
| [BLNPIX](#blnpix) | Alpha-blend bytes of S into bytes of D, using SETPIV value. |
| [MIXPIX](#mixpix) | Mix bytes of S into bytes of D, using SETPIX and SETPIV values. |
| [MULPIX](#mulpix) | Multiply bytes of S into bytes of D, where $FF = 1.0 and $00 = 0.0. |
| [SETPIV](#setpiv) | Set BLNPIX/MIXPIX blend factor to D[7:0]. |
| [SETPIX](#setpix) | Set MIXPIX mode to D[5:0]. |


## Register Indirection

| Instruction | Description |
|-------------|-------------|
| [ALTB](#altb) | Alter D field of next instruction to D[13:5]. |
| [ALTD](#altd) | Alter D field of next instruction to D[8:0]. |
| [ALTGB](#altgb) | Alter subsequent GETBYTE/ROLBYTE instruction |
| [ALTGN](#altgn) | Alter subsequent GETNIB/ROLNIB instruction |
| [ALTGW](#altgw) | Alter subsequent GETWORD/ROLWORD instruction |
| [ALTI](#alti) | Execute D in place of next instruction |
| [ALTR](#altr) | Alter result register address (normally D field) of next instruction to D[8:0]. |
| [ALTS](#alts) | Alter S field of next instruction to D[8:0]. |
| [ALTSB](#altsb) | Alter subsequent SETBYTE instruction |
| [ALTSN](#altsn) | Alter subsequent SETNIB instruction |
| [ALTSW](#altsw) | Alter subsequent SETWORD instruction |


## Miscellaneous

| Instruction | Description |
|-------------|-------------|
| [AUGD](#augd) | Queue |
| [AUGS](#augs) | Queue |
| [GETCT](#getct) | Get CT[31:0] or CT[63:32] if WC into D |
| [GETRND](#getrnd) | Get RND into C/Z |
| [NOP](#nop) | No operation. |
| [POP](#pop) | Pop stack (K) |
| [PUSH](#push) | Push D onto stack. |
| [SETQ](#setq) | Set Q to D |
| [SETQ2](#setq2) | Set Q to D |
| [WAITX](#waitx) | Wait 2 + D clocks if no WC/WZ/WCZ |

