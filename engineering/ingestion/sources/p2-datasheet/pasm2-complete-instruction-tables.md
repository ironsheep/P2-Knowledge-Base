# PASM2 Complete Instruction Tables from P2 Datasheet

This document contains all PASM2 instruction tables extracted from the Propeller 2 datasheet, organized by functional groups.

## Table Structure
Each instruction group table has:
- **Group Header**: Category name (e.g., "Math and Logic Instructions")
- **Column 1**: Instruction mnemonic and operands
- **Column 2**: Description of operation
- **Column 3**: Clock cycles and memory info

### Clock Timing Notation
- Single number (e.g., "2"): Fixed clock cycles
- "Cog & LUT / Hub" format: Different timing for different memory regions
- Ranges (e.g., "13...20"): Variable timing based on hub window alignment
- "2 or 4": Conditional timing based on branch taken/not taken
- "2+": Base clocks plus additional based on wait condition

---

## Math and Logic Instructions

All Math and Logic instructions execute in 2 clock cycles.

| Instruction | Description |
|------------|-------------|
| **ABS D {WC/WZ/WCZ}** | Get absolute value of D into D. D = ABS(D). C = D[31]. * |
| **ABS D,{#}S {WC/WZ/WCZ}** | Get absolute value of S into D. D = ABS(S). C = S[31]. * |
| **ADD D,{#}S {WC/WZ/WCZ}** | Add S into D. D = D + S. C = carry of (D + S). * |
| **ADDS D,{#}S {WC/WZ/WCZ}** | Add S into D, signed. D = D + S. C = correct sign of (D + S). * |
| **ADDSX D,{#}S {WC/WZ/WCZ}** | Add (S + C) into D, signed and extended. D = D + S + C. C = correct sign of (D + S + C). Z = Z AND (result == 0). |
| **ADDX D,{#}S {WC/WZ/WCZ}** | Add (S + C) into D, extended. D = D + S + C. C = carry of (D + S + C). Z = Z AND (result == 0). |
| **AND D,{#}S {WC/WZ/WCZ}** | AND S into D. D = D & S. C = parity of result. * |
| **ANDN D,{#}S {WC/WZ/WCZ}** | AND !S into D. D = D & !S. C = parity of result. * |
| **BITC D,{#}S {WCZ}** | Bits D[S[9:5]+S[4:0]:S[4:0]] = C. Other bits unaffected. Prior SETQ overrides S[9:5]. C,Z = original D[S[4:0]]. |
| **BITH D,{#}S {WCZ}** | Bits D[S[9:5]+S[4:0]:S[4:0]] = 1. Other bits unaffected. Prior SETQ overrides S[9:5]. C,Z = original D[S[4:0]]. |
| **BITL D,{#}S {WCZ}** | Bits D[S[9:5]+S[4:0]:S[4:0]] = 0. Other bits unaffected. Prior SETQ overrides S[9:5]. C,Z = original D[S[4:0]]. |
| **BITNC D,{#}S {WCZ}** | Bits D[S[9:5]+S[4:0]:S[4:0]] = !C. Other bits unaffected. Prior SETQ overrides S[9:5]. C,Z = original D[S[4:0]]. |
| **BITNOT D,{#}S {WCZ}** | Toggle bits D[S[9:5]+S[4:0]:S[4:0]]. Other bits unaffected. Prior SETQ overrides S[9:5]. C,Z = original D[S[4:0]]. |
| **BITNZ D,{#}S {WCZ}** | Bits D[S[9:5]+S[4:0]:S[4:0]] = !Z. Other bits unaffected. Prior SETQ overrides S[9:5]. C,Z = original D[S[4:0]]. |
| **BITRND D,{#}S {WCZ}** | Bits D[S[9:5]+S[4:0]:S[4:0]] = RNDs. Other bits unaffected. Prior SETQ overrides S[9:5]. C,Z = original D[S[4:0]]. |
| **BITZ D,{#}S {WCZ}** | Bits D[S[9:5]+S[4:0]:S[4:0]] = Z. Other bits unaffected. Prior SETQ overrides S[9:5]. C,Z = original D[S[4:0]]. |
| **BMASK D** | Get LSB-justified bit mask of size (D[4:0] + 1) into D. D = ($0000_0002 << D[4:0]) - 1. |
| **BMASK D,{#}S** | Get LSB-justified bit mask of size (S[4:0] + 1) into D. D = ($0000_0002 << S[4:0]) - 1. |
| **CMP D,{#}S {WC/WZ/WCZ}** | Compare D to S. C = borrow of (D - S). Z = (D == S). |
| **CMPM D,{#}S {WC/WZ/WCZ}** | Compare D to S, get MSB of difference into C. C = MSB of (D - S). Z = (D == S). |
| **CMPR D,{#}S {WC/WZ/WCZ}** | Compare S to D (reverse). C = borrow of (S - D). Z = (D == S). |
| **CMPS D,{#}S {WC/WZ/WCZ}** | Compare D to S, signed. C = correct sign of (D - S). Z = (D == S). |
| **CMPSUB D,{#}S {WC/WZ/WCZ}** | Compare and subtract S from D if D >= S. If D => S then D = D - S and C = 1, else D same and C = 0. * |
| **CMPSX D,{#}S {WC/WZ/WCZ}** | Compare D to (S + C), signed and extended. C = correct sign of (D - (S + C)). Z = Z AND (D == S + C). |
| **CMPX D,{#}S {WC/WZ/WCZ}** | Compare D to (S + C), extended. C = borrow of (D - (S + C)). Z = Z AND (D == S + C). |
| **CRCBIT D,{#}S** | Iterate CRC value in D using C and polynomial in S. If (C XOR D[0]) then D = (D >> 1) XOR S, else D = (D >> 1). |
| **CRCNIB D,{#}S** | Iterate CRC value in D using Q[31:28] and polynomial in S. Like CRCBIT x 4. Q = Q << 4. |
| **DECMOD D,{#}S {WC/WZ/WCZ}** | Decrement with modulus. If D = 0 then D = S and C = 1, else D = D - 1 and C = 0. * |
| **DECOD D** | Decode D[4:0] into D. D = 1 << D[4:0]. |
| **DECOD D,{#}S** | Decode S[4:0] into D. D = 1 << S[4:0]. |
| **ENCOD D {WC/WZ/WCZ}** | Get bit position of top-most '1' in D into D. D = position of top '1' in S (0..31). C = (S != 0). * |
| **ENCOD D,{#}S {WC/WZ/WCZ}** | Get bit position of top-most '1' in S into D. D = position of top '1' in S (0..31). C = (S != 0). * |
| **FGE D,{#}S {WC/WZ/WCZ}** | Force D >= S. If D < S then D = S and C = 1, else D same and C = 0. * |
| **FGES D,{#}S {WC/WZ/WCZ}** | Force D >= S, signed. If D < S then D = S and C = 1, else D same and C = 0. * |
| **FLE D,{#}S {WC/WZ/WCZ}** | Force D <= S. If D > S then D = S and C = 1, else D same and C = 0. * |
| **FLES D,{#}S {WC/WZ/WCZ}** | Force D <= S, signed. If D > S then D = S and C = 1, else D same and C = 0. * |
| **GETBYTE D** | Get byte established by prior ALTGB instruction into D. |
| **GETBYTE D,{#}S,#N** | Get byte N of S into D. D = {24'b0, S.BYTE[N]). |
| **GETNIB D** | Get nibble established by prior ALTGN instruction into D. |
| **GETNIB D,{#}S,#N** | Get nibble N of S into D. D = {28'b0, S.NIBBLE[N]). |
| **GETWORD D** | Get word established by prior ALTGW instruction into D. |
| **GETWORD D,{#}S,#N** | Get word N of S into D. D = {16'b0, S.WORD[N]). |
| **INCMOD D,{#}S {WC/WZ/WCZ}** | Increment with modulus. If D = S then D = 0 and C = 1, else D = D + 1 and C = 0. * |
| **LOC PA/PB/PTRA/PTRB,#{\}A** | Get {12'b0, address[19:0]} into PA/PB/PTRA/PTRB (per W). If R = 1, address = PC + A, else address = A. "\\" forces R = 0. |
| **MERGEB D** | Merge bits of bytes in D. D = {D[31], D[23], D[15], D[7], ...D[24], D[16], D[8], D[0]}. |
| **MERGEW D** | Merge bits of words in D. D = {D[31], D[15], D[30], D[14], ...D[17], D[1], D[16], D[0]}. |
| **MODC c {WC}** | Modify C according to cccc. C = cccc[{C,Z}]. |
| **MODCZ c,z {WC/WZ/WCZ}** | Modify C and Z according to cccc and zzzz. C = cccc[{C,Z}], Z = zzzz[{C,Z}]. |
| **MODZ z {WZ}** | Modify Z according to zzzz. Z = zzzz[{C,Z}]. |
| **MOV D,{#}S {WC/WZ/WCZ}** | Move S into D. D = S. C = S[31]. * |
| **MOVBYTS D,{#}S** | Move bytes within D, per S. D = {D.BYTE[S[7:6]], D.BYTE[S[5:4]], D.BYTE[S[3:2]], D.BYTE[S[1:0]]}. |
| **MUL D,{#}S {WZ}** | D = unsigned (D[15:0] * S[15:0]). Z = (S == 0) \| (D == 0). |
| **MULS D,{#}S {WZ}** | D = signed (D[15:0] * S[15:0]). Z = (S == 0) \| (D == 0). |
| **MUXC D,{#}S {WC/WZ/WCZ}** | Mux C into each D bit that is '1' in S. D = (!S & D ) \| (S & {32{ C}}). C = parity of result. * |
| **MUXNC D,{#}S {WC/WZ/WCZ}** | Mux !C into each D bit that is '1' in S. D = (!S & D ) \| (S & {32{!C}}). C = parity of result. * |
| **MUXNIBS D,{#}S** | For each non-zero nibble in S, copy that nibble into the corresponding D nibble. |
| **MUXNITS D,{#}S** | For each non-zero bit pair in S, copy that bit pair into the corresponding D bits. |
| **MUXNZ D,{#}S {WC/WZ/WCZ}** | Mux !Z into each D bit that is '1' in S. D = (!S & D ) \| (S & {32{!Z}}). C = parity of result. * |
| **MUXQ D,{#}S** | Used after SETQ. For each '1' bit in Q, copy the corresponding bit in S into D. D = (D & !Q) \| (S & Q). |
| **MUXZ D,{#}S {WC/WZ/WCZ}** | Mux Z into each D bit that is '1' in S. D = (!S & D ) \| (S & {32{ Z}}). C = parity of result. * |
| **NEG D {WC/WZ/WCZ}** | Negate D. D = -D. C = MSB of result. * |
| **NEG D,{#}S {WC/WZ/WCZ}** | Negate S into D. D = -S. C = MSB of result. * |
| **NEGC D {WC/WZ/WCZ}** | Negate D by C. If C = 1 then D = -D, else D = D. C = MSB of result. * |
| **NEGC D,{#}S {WC/WZ/WCZ}** | Negate S by C into D. If C = 1 then D = -S, else D = S. C = MSB of result. * |
| **NEGNC D {WC/WZ/WCZ}** | Negate D by !C. If C = 0 then D = -D, else D = D. C = MSB of result. * |
| **NEGNC D,{#}S {WC/WZ/WCZ}** | Negate S by !C into D. If C = 0 then D = -S, else D = S. C = MSB of result. * |
| **NEGNZ D {WC/WZ/WCZ}** | Negate D by !Z. If Z = 0 then D = -D, else D = D. C = MSB of result. * |
| **NEGNZ D,{#}S {WC/WZ/WCZ}** | Negate S by !Z into D. If Z = 0 then D = -S, else D = S. C = MSB of result. * |
| **NEGZ D {WC/WZ/WCZ}** | Negate D by Z. If Z = 1 then D = -D, else D = D. C = MSB of result. * |
| **NEGZ D,{#}S {WC/WZ/WCZ}** | Negate S by Z into D. If Z = 1 then D = -S, else D = S. C = MSB of result. * |
| **NOT D {WC/WZ/WCZ}** | Get !D into D. D = !D. C = !D[31]. * |
| **NOT D,{#}S {WC/WZ/WCZ}** | Get !S into D. D = !S. C = !S[31]. * |
| **ONES D {WC/WZ/WCZ}** | Get number of '1's in D into D. D = number of '1's in S (0..32). C = LSB of result. * |
| **ONES D,{#}S {WC/WZ/WCZ}** | Get number of '1's in S into D. D = number of '1's in S (0..32). C = LSB of result. * |
| **OR D,{#}S {WC/WZ/WCZ}** | OR S into D. D = D \| S. C = parity of result. * |
| **RCL D,{#}S {WC/WZ/WCZ}** | Rotate carry left. D = [63:32] of ({D[31:0], {32{C}}} << S[4:0]). C = last bit shifted out. * |
| **RCR D,{#}S {WC/WZ/WCZ}** | Rotate carry right. D = [31:0] of ({{32{C}}, D[31:0]} >> S[4:0]). C = last bit shifted out. * |
| **RCZL D {WC/WZ/WCZ}** | Rotate C,Z left through D. D = {D[29:0], C, Z}. C = D[31], Z = D[30]. |
| **RCZR D {WC/WZ/WCZ}** | Rotate C,Z right through D. D = {C, Z, D[31:2]}. C = D[1], Z = D[0]. |
| **REV D** | Reverse D bits. D = D[0:31]. |
| **RGBEXP D** | Expand 5:6:5 RGB value in D[15:0] into 8:8:8 value in D[31:8]. |
| **RGBSQZ D** | Squeeze 8:8:8 RGB value in D[31:8] into 5:6:5 value in D[15:0]. |
| **ROL D,{#}S {WC/WZ/WCZ}** | Rotate left. D = [63:32] of ({D[31:0], D[31:0]} << S[4:0]). C = last bit shifted out. * |
| **ROLBYTE D** | Rotate-left byte established by prior ALTGB instruction into D. |
| **ROLBYTE D,{#}S,#N** | Rotate-left byte N of S into D. D = {D[23:0], S.BYTE[N]). |
| **ROLNIB D** | Rotate-left nibble established by prior ALTGN instruction into D. |
| **ROLNIB D,{#}S,#N** | Rotate-left nibble N of S into D. D = {D[27:0], S.NIBBLE[N]). |
| **ROLWORD D** | Rotate-left word established by prior ALTGW instruction into D. |
| **ROLWORD D,{#}S,#N** | Rotate-left word N of S into D. D = {D[15:0], S.WORD[N]). |
| **ROR D,{#}S {WC/WZ/WCZ}** | Rotate right. D = [31:0] of ({D[31:0], D[31:0]} >> S[4:0]). C = last bit shifted out. * |
| **SAL D,{#}S {WC/WZ/WCZ}** | Shift arithmetic left. D = [63:32] of ({D[31:0], {32{D[0]}}} << S[4:0]). C = last bit shifted out. * |
| **SAR D,{#}S {WC/WZ/WCZ}** | Shift arithmetic right. D = [31:0] of ({{32{D[31]}}, D[31:0]} >> S[4:0]). C = last bit shifted out. * |
| **SCA D,{#}S {WZ}** | Next instruction's S value = unsigned (D[15:0] * S[15:0]) >> 16. * |
| **SCAS D,{#}S {WZ}** | Next instruction's S value = signed (D[15:0] * S[15:0]) >> 14. In this scheme, $4000 = 1.0 and $C000 = -1.0. * |
| **SETBYTE {#}S** | Set S[7:0] into byte established by prior ALTSB instruction. |
| **SETBYTE D,{#}S,#N** | Set S[7:0] into byte N in D, keeping rest of D same. |
| **SETD D,{#}S** | Set D field of D to S[8:0]. D = {D[31:18], S[8:0], D[8:0]}. |
| **SETNIB {#}S** | Set S[3:0] into nibble established by prior ALTSN instruction. |
| **SETNIB D,{#}S,#N** | Set S[3:0] into nibble N in D, keeping rest of D same. |
| **SETR D,{#}S** | Set R field of D to S[8:0]. D = {D[31:28], S[8:0], D[18:0]}. |
| **SETS D,{#}S** | Set S field of D to S[8:0]. D = {D[31:9], S[8:0]}. |
| **SETWORD {#}S** | Set S[15:0] into word established by prior ALTSW instruction. |
| **SETWORD D,{#}S,#N** | Set S[15:0] into word N in D, keeping rest of D same. |
| **SEUSSF D** | Relocate and periodically invert bits within D. Returns to original value on 32nd iteration. Forward pattern. |
| **SEUSSR D** | Relocate and periodically invert bits within D. Returns to original value on 32nd iteration. Reverse pattern. |
| **SHL D,{#}S {WC/WZ/WCZ}** | Shift left. D = [63:32] of ({D[31:0], 32'b0} << S[4:0]). C = last bit shifted out. * |
| **SHR D,{#}S {WC/WZ/WCZ}** | Shift right. D = [31:0] of ({32'b0, D[31:0]} >> S[4:0]). C = last bit shifted out. * |
| **SIGNX D,{#}S {WC/WZ/WCZ}** | Sign-extend D from bit S[4:0]. C = MSB of result. * |
| **SPLITB D** | Split every 4th bit of D into bytes. D = {D[31], D[27], D[23], D[19], ...D[12], D[8], D[4], D[0]}. |
| **SPLITW D** | Split odd/even bits of D into words. D = {D[31], D[29], D[27], D[25], ...D[6], D[4], D[2], D[0]}. |
| **SUB D,{#}S {WC/WZ/WCZ}** | Subtract S from D. D = D - S. C = borrow of (D - S). * |
| **SUBR D,{#}S {WC/WZ/WCZ}** | Subtract D from S (reverse). D = S - D. C = borrow of (S - D). * |
| **SUBS D,{#}S {WC/WZ/WCZ}** | Subtract S from D, signed. D = D - S. C = correct sign of (D - S). * |
| **SUBSX D,{#}S {WC/WZ/WCZ}** | Subtract (S + C) from D, signed and extended. D = D - (S + C). C = correct sign. Z = Z AND (result == 0). |
| **SUBX D,{#}S {WC/WZ/WCZ}** | Subtract (S + C) from D, extended. D = D - (S + C). C = borrow. Z = Z AND (result == 0). |
| **SUMC D,{#}S {WC/WZ/WCZ}** | Sum +/-S into D by C. If C = 1 then D = D - S, else D = D + S. C = correct sign. * |
| **SUMNC D,{#}S {WC/WZ/WCZ}** | Sum +/-S into D by !C. If C = 0 then D = D - S, else D = D + S. C = correct sign. * |
| **SUMNZ D,{#}S {WC/WZ/WCZ}** | Sum +/-S into D by !Z. If Z = 0 then D = D - S, else D = D + S. C = correct sign. * |
| **SUMZ D,{#}S {WC/WZ/WCZ}** | Sum +/-S into D by Z. If Z = 1 then D = D - S, else D = D + S. C = correct sign. * |
| **TEST D {WC/WZ/WCZ}** | Test D. C = parity of D. Z = (D == 0). |
| **TEST D,{#}S {WC/WZ/WCZ}** | Test D with S. C = parity of (D & S). Z = ((D & S) == 0). |
| **TESTB D,{#}S WC/WZ** | Test bit S[4:0] of D, write to C/Z. C/Z = D[S[4:0]]. |
| **TESTB D,{#}S ORC/ORZ** | Test bit S[4:0] of D, OR into C/Z. C/Z = C/Z OR D[S[4:0]]. |
| **TESTB D,{#}S ANDC/ANDZ** | Test bit S[4:0] of D, AND into C/Z. C/Z = C/Z AND D[S[4:0]]. |
| **TESTB D,{#}S XORC/XORZ** | Test bit S[4:0] of D, XOR into C/Z. C/Z = C/Z XOR D[S[4:0]]. |
| **TESTBN D,{#}S WC/WZ** | Test bit S[4:0] of !D, write to C/Z. C/Z = !D[S[4:0]]. |
| **TESTBN D,{#}S ORC/ORZ** | Test bit S[4:0] of !D, OR into C/Z. C/Z = C/Z OR !D[S[4:0]]. |
| **TESTBN D,{#}S ANDC/ANDZ** | Test bit S[4:0] of !D, AND into C/Z. C/Z = C/Z AND !D[S[4:0]]. |
| **TESTBN D,{#}S XORC/XORZ** | Test bit S[4:0] of !D, XOR into C/Z. C/Z = C/Z XOR !D[S[4:0]]. |
| **TESTN D,{#}S {WC/WZ/WCZ}** | Test D with !S. C = parity of (D & !S). Z = ((D & !S) == 0). |
| **WRC D** | Write 0 or 1 to D, according to C. D = {31'b0, C). |
| **WRNC D** | Write 0 or 1 to D, according to !C. D = {31'b0, !C). |
| **WRNZ D** | Write 0 or 1 to D, according to !Z. D = {31'b0, !Z). |
| **WRZ D** | Write 0 or 1 to D, according to Z. D = {31'b0, Z). |
| **XOR D,{#}S {WC/WZ/WCZ}** | XOR S into D. D = D ^ S. C = parity of result. * |
| **XORO32 D** | Iterate D with xoroshiro32+ PRNG algorithm and put PRNG result into next instruction's S. |
| **ZEROX D,{#}S {WC/WZ/WCZ}** | Zero-extend D above bit S[4:0]. C = MSB of result. * |

*Note: Asterisk (*) indicates instructions that affect Z flag based on result being zero.

---

## Pin & Smart Pin Instructions

All Pin & Smart Pin instructions execute in 2 clock cycles.

| Instruction | Description |
|------------|-------------|
| **DIRC {#}D {WCZ}** | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = C. Wraps within DIRA/DIRB. Prior SETQ overrides D[10:6]. C,Z = DIR bit. |
| **DIRH {#}D {WCZ}** | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = 1. Wraps within DIRA/DIRB. Prior SETQ overrides D[10:6]. C,Z = DIR bit. |
| **DIRL {#}D {WCZ}** | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = 0. Wraps within DIRA/DIRB. Prior SETQ overrides D[10:6]. C,Z = DIR bit. |
| **DIRNC {#}D {WCZ}** | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = !C. Wraps within DIRA/DIRB. Prior SETQ overrides D[10:6]. C,Z = DIR bit. |
| **DIRNOT {#}D {WCZ}** | Toggle DIR bits of pins D[10:6]+D[5:0]..D[5:0]. Wraps within DIRA/DIRB. Prior SETQ overrides D[10:6]. C,Z = DIR bit. |
| **DIRNZ {#}D {WCZ}** | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = !Z. Wraps within DIRA/DIRB. Prior SETQ overrides D[10:6]. C,Z = DIR bit. |
| **DIRRND {#}D {WCZ}** | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs. Wraps within DIRA/DIRB. Prior SETQ overrides D[10:6]. C,Z = DIR bit. |
| **DIRZ {#}D {WCZ}** | DIR bits of pins D[10:6]+D[5:0]..D[5:0] = Z. Wraps within DIRA/DIRB. Prior SETQ overrides D[10:6]. C,Z = DIR bit. |
| **DRVC {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C. DIR bits = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **DRVH {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1. DIR bits = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **DRVL {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0. DIR bits = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **DRVNC {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C. DIR bits = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **DRVNOT {#}D {WCZ}** | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0]. DIR bits = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **DRVNZ {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z. DIR bits = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **DRVRND {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs. DIR bits = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **DRVZ {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z. DIR bits = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **FLTC {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C. DIR bits = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **FLTH {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1. DIR bits = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **FLTL {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0. DIR bits = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **FLTNC {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C. DIR bits = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **FLTNOT {#}D {WCZ}** | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0]. DIR bits = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **FLTNZ {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z. DIR bits = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **FLTRND {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs. DIR bits = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **FLTZ {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z. DIR bits = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **OUTC {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = C. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **OUTH {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 1. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **OUTL {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = 0. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **OUTNC {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !C. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **OUTNOT {#}D {WCZ}** | Toggle OUT bits of pins D[10:6]+D[5:0]..D[5:0]. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **OUTNZ {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = !Z. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **OUTRND {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = RNDs. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **OUTZ {#}D {WCZ}** | OUT bits of pins D[10:6]+D[5:0]..D[5:0] = Z. Wraps within OUTA/OUTB. Prior SETQ overrides D[10:6]. C,Z = OUT bit. |
| **TESTP {#}D WC/WZ** | Test IN bit of pin D[5:0], write to C/Z. C/Z = IN[D[5:0]]. |
| **TESTP {#}D ORC/ORZ** | Test IN bit of pin D[5:0], OR into C/Z. C/Z = C/Z OR IN[D[5:0]]. |
| **TESTP {#}D ANDC/ANDZ** | Test IN bit of pin D[5:0], AND into C/Z. C/Z = C/Z AND IN[D[5:0]]. |
| **TESTP {#}D XORC/XORZ** | Test IN bit of pin D[5:0], XOR into C/Z. C/Z = C/Z XOR IN[D[5:0]]. |
| **TESTPN {#}D WC/WZ** | Test !IN bit of pin D[5:0], write to C/Z. C/Z = !IN[D[5:0]]. |
| **TESTPN {#}D ORC/ORZ** | Test !IN bit of pin D[5:0], OR into C/Z. C/Z = C/Z OR !IN[D[5:0]]. |
| **TESTPN {#}D ANDC/ANDZ** | Test !IN bit of pin D[5:0], AND into C/Z. C/Z = C/Z AND !IN[D[5:0]]. |
| **TESTPN {#}D XORC/XORZ** | Test !IN bit of pin D[5:0], XOR into C/Z. C/Z = C/Z XOR !IN[D[5:0]]. |
| **AKPIN {#}S** | Acknowledge smart pins S[10:6]+S[5:0]..S[5:0]. Wraps within A/B pins. Prior SETQ overrides S[10:6]. |
| **GETSCP D** | Get four-channel oscilloscope samples into D. D = {ch3[7:0],ch2[7:0],ch1[7:0],ch0[7:0]}. |
| **RDPIN D,{#}S {WC}** | Read smart pin S[5:0] result "Z" into D, acknowledge smart pin. C = modal result. |
| **RQPIN D,{#}S {WC}** | Read smart pin S[5:0] result "Z" into D, don't acknowledge smart pin ("Q" in RQPIN means "quiet"). C = modal result. |
| **SETDACS {#}D** | DAC3 = D[31:24], DAC2 = D[23:16], DAC1 = D[15:8], DAC0 = D[7:0]. |
| **SETSCP {#}D** | Set four-channel oscilloscope enable to D[6] and set input pin base to D[5:2]. |
| **WRPIN {#}D,{#}S** | Set mode of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins. Wraps within A/B pins. Prior SETQ overrides S[10:6]. |
| **WXPIN {#}D,{#}S** | Set "X" of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins. Wraps within A/B pins. Prior SETQ overrides S[10:6]. |
| **WYPIN {#}D,{#}S** | Set "Y" of smart pins S[10:6]+S[5:0]..S[5:0] to D, acknowledge smart pins. Wraps within A/B pins. Prior SETQ overrides S[10:6]. |

---

## Branch Instructions

| Instruction | Description | Clocks (Cog&LUT / Hub) |
|------------|-------------|------------------------|
| **CALL #{\\}A** | Call to A by pushing {C, Z, 10'b0, PC[19:0]} onto stack. If R = 1 then PC += A, else PC = A. "\\" forces R = 0. | 4 / 13...20 |
| **CALL D {WC/WZ/WCZ}** | Call to D by pushing {C, Z, 10'b0, PC[19:0]} onto stack. C = D[31], Z = D[30], PC = D[19:0]. | 4 / 13...20 |
| **CALLA #{\\}A** | Call to A by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRA++. If R = 1 then PC += A, else PC = A. "\\" forces R = 0. | 5...12 / 14...32 |
| **CALLA D {WC/WZ/WCZ}** | Call to D by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRA++. C = D[31], Z = D[30], PC = D[19:0]. | 5...12 / 14...32 |
| **CALLB #{\\}A** | Call to A by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRB++. If R = 1 then PC += A, else PC = A. "\\" forces R = 0. | 5...12 / 14...32 |
| **CALLB D {WC/WZ/WCZ}** | Call to D by writing {C, Z, 10'b0, PC[19:0]} to hub long at PTRB++. C = D[31], Z = D[30], PC = D[19:0]. | 5...12 / 14...32 |
| **CALLD D,{#}S {WC/WZ/WCZ}** | Call to S** by writing {C, Z, 10'b0, PC[19:0]} to D. C = S[31], Z = S[30]. | 4 / 4 |
| **CALLD PA/PB/PTRA/PTRB,#{\\}A** | Call to A by writing {C, Z, 10'b0, PC[19:0]} to PA/PB/PTRA/PTRB (per W). If R = 1 then PC += A, else PC = A. "\\" forces R = 0. | 4 / 4 |
| **CALLPA {#}D,{#}S** | Call to S** by pushing {C, Z, 10'b0, PC[19:0]} onto stack, copy D to PA. | 4 / 13...20 |
| **CALLPB {#}D,{#}S** | Call to S** by pushing {C, Z, 10'b0, PC[19:0]} onto stack, copy D to PB. | 4 / 13...20 |
| **DJF D,{#}S** | Decrement D and jump to S** if result is $FFFF_FFFF. | 2 or 4 / 2 or 13...20 |
| **DJNF D,{#}S** | Decrement D and jump to S** if result is not $FFFF_FFFF. | 2 or 4 / 2 or 13...20 |
| **DJNZ D,{#}S** | Decrement D and jump to S** if result is not zero. | 2 or 4 / 2 or 13...20 |
| **DJZ D,{#}S** | Decrement D and jump to S** if result is zero. | 2 or 4 / 2 or 13...20 |
| **EXECF {#}D** | Jump to D[9:0] in cog/LUT and set SKIPF pattern to D[31:10]. PC = {10'b0, D[9:0]}. | 4 / ILLEGAL |
| **IJNZ D,{#}S** | Increment D and jump to S** if result is not zero. | 2 or 4 / 2 or 13...20 |
| **IJZ D,{#}S** | Increment D and jump to S** if result is zero. | 2 or 4 / 2 or 13...20 |
| **JMP #{\\}A** | Jump to A. If R = 1 then PC += A, else PC = A. "\\" forces R = 0. | 4 / 13...20 |
| **JMP D {WC/WZ/WCZ}** | Jump to D. C = D[31], Z = D[30], PC = D[19:0]. | 4 / 13...20 |
| **JMPREL {#}D** | Jump ahead/back by D instructions. For cogex, PC += D[19:0]. For hubex, PC += D[17:0] << 2. | 4 / 13...20 |
| **REP {#}D,{#}S** | Execute next D[8:0] instructions S times. If S = 0, repeat instructions infinitely. If D[8:0] = 0, nothing repeats. | 2 / 2 |
| **RESI0** | Resume from INT0. (CALLD $1FE,$1FF WCZ) | 4 / 13...20 |
| **RESI1** | Resume from INT1. (CALLD $1F4,$1F5 WCZ) | 4 / 13...20 |
| **RESI2** | Resume from INT2. (CALLD $1F2,$1F3 WCZ) | 4 / 13...20 |
| **RESI3** | Resume from INT3. (CALLD $1F0,$1F1 WCZ) | 4 / 13...20 |
| **RET {WC/WZ/WCZ}** | Return by popping stack (K). C = K[31], Z = K[30], PC = K[19:0]. | 4 / 13...20 |
| **RETA {WC/WZ/WCZ}** | Return by reading hub long (L) at --PTRA. C = L[31], Z = L[30], PC = L[19:0]. | 11...18 / 20...40 |
| **RETB {WC/WZ/WCZ}** | Return by reading hub long (L) at --PTRB. C = L[31], Z = L[30], PC = L[19:0]. | 11...18 / 20...40 |
| **RETI0** | Return from INT0. (CALLD $1FF,$1FF WCZ) | 4 / 13...20 |
| **RETI1** | Return from INT1. (CALLD $1FF,$1F5 WCZ) | 4 / 13...20 |
| **RETI2** | Return from INT2. (CALLD $1FF,$1F3 WCZ) | 4 / 13...20 |
| **RETI3** | Return from INT3. (CALLD $1FF,$1F1 WCZ) | 4 / 13...20 |
| **SKIP {#}D** | Skip instructions per D. Subsequent instructions 0..31 get cancelled for each '1' bit in D[0]..D[31]. | 2 / 2 |
| **SKIPF {#}D** | Skip cog/LUT instructions fast per D. Like SKIP, but instead of cancelling instructions, the PC leaps over them. | 2 / ILLEGAL |
| **TJF D,{#}S** | Test D and jump to S** if D is full (D = $FFFF_FFFF). | 2 or 4 / 2 or 13...20 |
| **TJNF D,{#}S** | Test D and jump to S** if D is not full (D != $FFFF_FFFF). | 2 or 4 / 2 or 13...20 |
| **TJNS D,{#}S** | Test D and jump to S** if D is not signed (D[31] = 0). | 2 or 4 / 2 or 13...20 |
| **TJNZ D,{#}S** | Test D and jump to S** if D is not zero. | 2 or 4 / 2 or 13...20 |
| **TJS D,{#}S** | Test D and jump to S** if D is signed (D[31] = 1). | 2 or 4 / 2 or 13...20 |
| **TJV D,{#}S** | Test D and jump to S** if D overflowed (D[31] != C, C = 'correct sign' from last addition/subtraction). | 2 or 4 / 2 or 13...20 |
| **TJZ D,{#}S** | Test D and jump to S** if D is zero. | 2 or 4 / 2 or 13...20 |

**Note**: S** indicates 20-bit address for hub execution or 9-bit address for cog/LUT execution.

---

## Hub Control, FIFO, & RAM Instructions

### Hub Control

| Instruction | Description | Clocks (Cog&LUT / Hub) |
|------------|-------------|------------------------|
| **COGID {#}D {WC}** | If D is register and no WC, get cog ID (0 to 15) into D. If WC, check status of cog D[3:0], C = 1 if on. | 2...9, +2 if result / same |
| **COGINIT {#}D,{#}S {WC}** | Start cog selected by D. S[19:0] sets hub startup address and PTRB of cog. Prior SETQ sets PTRA of cog. | 2...9, +2 if result / same |
| **COGSTOP {#}D** | Stop cog D[3:0]. | 2...9 / same |
| **LOCKNEW D {WC}** | Request a LOCK. D will be written with the LOCK number (0 to 15). C = 1 if no LOCK available. | 4...11 / same |
| **LOCKREL {#}D {WC}** | Release LOCK D[3:0]. If D is a register and WC, get current/last cog id of LOCK owner into D and LOCK status into C. | 2...9, +2 if result / same |
| **LOCKRET {#}D** | Return LOCK D[3:0] for reallocation. | 2...9 / same |
| **LOCKTRY {#}D {WC}** | Try to get LOCK D[3:0]. C = 1 if got LOCK. LOCKREL releases LOCK. LOCK is also released if owner cog stops or restarts. | 2...9, +2 if result / same |
| **HUBSET {#}D** | Set hub configuration to D. | 2...9 / same |

### Hub FIFO

| Instruction | Description | Clocks (Cog&LUT / Hub) |
|------------|-------------|------------------------|
| **GETPTR D** | Get current FIFO hub pointer into D. | 2 / FIFO IN USE |
| **FBLOCK {#}D,{#}S** | Set next block for when block wraps. D[13:0] = block size in 64-byte units (0 = max), S[19:0] = block start address. | 2 / FIFO IN USE |
| **RDFAST {#}D,{#}S** | Begin new fast hub read via FIFO. D[31] = no wait, D[13:0] = block size in 64-byte units (0 = max), S[19:0] = block start address. | 2 or WRFAST finish + 10...17 / FIFO IN USE |
| **WRFAST {#}D,{#}S** | Begin new fast hub write via FIFO. D[31] = no wait, D[13:0] = block size in 64-byte units (0 = max), S[19:0] = block start address. | 2 or WRFAST finish + 3 / FIFO IN USE |
| **RFBYTE D {WC/WZ/WCZ}** | Used after RDFAST. Read zero-extended byte from FIFO into D. C = MSB of byte. * | 2 / FIFO IN USE |
| **RFLONG D {WC/WZ/WCZ}** | Used after RDFAST. Read long from FIFO into D. C = MSB of long. * | 2 / FIFO IN USE |
| **RFVAR D {WC/WZ/WCZ}** | Used after RDFAST. Read zero-extended 1..4-byte value from FIFO into D. C = 0. * | 2 / FIFO IN USE |
| **RFVARS D {WC/WZ/WCZ}** | Used after RDFAST. Read sign-extended 1..4-byte value from FIFO into D. C = MSB of value. * | 2 / FIFO IN USE |
| **RFWORD D {WC/WZ/WCZ}** | Used after RDFAST. Read zero-extended word from FIFO into D. C = MSB of word. * | 2 / FIFO IN USE |
| **WFBYTE {#}D** | Used after WRFAST. Write byte in D[7:0] into FIFO. | 2 / FIFO IN USE |
| **WFLONG {#}D** | Used after WRFAST. Write long in D[31:0] into FIFO. | 2 / FIFO IN USE |
| **WFWORD {#}D** | Used after WRFAST. Write word in D[15:0] into FIFO. | 2 / FIFO IN USE |

### Hub RAM

| Instruction | Description | Clocks (Cog&LUT / Hub) |
|------------|-------------|------------------------|
| **POPA D {WC/WZ/WCZ}** | Read long from hub address --PTRA into D. C = MSB of long. * | 9...16 / 9...26 |
| **POPB D {WC/WZ/WCZ}** | Read long from hub address --PTRB into D. C = MSB of long. * | 9...16 / 9...26 |
| **RDBYTE D,{#}S/P {WC/WZ/WCZ}** | Read zero-extended byte from hub address {#}S/PTRx into D. C = MSB of byte. * | 9...16 / 9...26 |
| **RDLONG D,{#}S/P {WC/WZ/WCZ}** | Read long from hub address {#}S/PTRx into D. C = MSB of long. * Prior SETQ/SETQ2 invokes cog/LUT block transfer. | 9...16 / 9...26 |
| **RDWORD D,{#}S/P {WC/WZ/WCZ}** | Read zero-extended word from hub address {#}S/PTRx into D. C = MSB of word. * | 9...16 / 9...26 |
| **PUSHA {#}D** | Write long in D[31:0] to hub address PTRA++. | 3...10 / 3...20 |
| **PUSHB {#}D** | Write long in D[31:0] to hub address PTRB++. | 3...10 / 3...20 |
| **WMLONG D,{#}S/P** | Write only non-$00 bytes in D[31:0] to hub address {#}S/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer. | 3...10 / 3...20 |
| **WRBYTE {#}D,{#}S/P** | Write byte in D[7:0] to hub address {#}S/PTRx. | 3...10 / 3...20 |
| **WRLONG {#}D,{#}S/P** | Write long in D[31:0] to hub address {#}S/PTRx. Prior SETQ/SETQ2 invokes cog/LUT block transfer. | 3...10 / 3...20 |
| **WRWORD {#}D,{#}S/P** | Write word in D[15:0] to hub address {#}S/PTRx. | 3...10 / 3...20 |

**Note**: Additional +1 clock if instruction crosses hub long boundary.

---

## Event Instructions

| Instruction | Description | Clocks |
|------------|-------------|--------|
| **ADDCT1 D,{#}S** | Set CT1 event to trigger on CT = D + S. Adds S into D. | 2 |
| **ADDCT2 D,{#}S** | Set CT2 event to trigger on CT = D + S. Adds S into D. | 2 |
| **ADDCT3 D,{#}S** | Set CT3 event to trigger on CT = D + S. Adds S into D. | 2 |
| **COGATN {#}D** | Strobe "attention" of all cogs whose corresponding bits are high in D[15:0]. | 2 |
| **JATN {#}S** | Jump to S** if ATN event flag is set. | 2 or 4 / 2 or 13...20 |
| **JCT1 {#}S** | Jump to S** if CT1 event flag is set. | 2 or 4 / 2 or 13...20 |
| **JCT2 {#}S** | Jump to S** if CT2 event flag is set. | 2 or 4 / 2 or 13...20 |
| **JCT3 {#}S** | Jump to S** if CT3 event flag is set. | 2 or 4 / 2 or 13...20 |
| **JFBW {#}S** | Jump to S** if FBW event flag is set. | 2 or 4 / 2 or 13...20 |
| **JINT {#}S** | Jump to S** if INT event flag is set. | 2 or 4 / 2 or 13...20 |
| **JNATN {#}S** | Jump to S** if ATN event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNCT1 {#}S** | Jump to S** if CT1 event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNCT2 {#}S** | Jump to S** if CT2 event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNCT3 {#}S** | Jump to S** if CT3 event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNFBW {#}S** | Jump to S** if FBW event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNINT {#}S** | Jump to S** if INT event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNPAT {#}S** | Jump to S** if PAT event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNQMT {#}S** | Jump to S** if QMT event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNSE1 {#}S** | Jump to S** if SE1 event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNSE2 {#}S** | Jump to S** if SE2 event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNSE3 {#}S** | Jump to S** if SE3 event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNSE4 {#}S** | Jump to S** if SE4 event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNXFI {#}S** | Jump to S** if XFI event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNXMT {#}S** | Jump to S** if XMT event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNXRL {#}S** | Jump to S** if XRL event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JNXRO {#}S** | Jump to S** if XRO event flag is clear. | 2 or 4 / 2 or 13...20 |
| **JPAT {#}S** | Jump to S** if PAT event flag is set. | 2 or 4 / 2 or 13...20 |
| **JQMT {#}S** | Jump to S** if QMT event flag is set. | 2 or 4 / 2 or 13...20 |
| **JSE1 {#}S** | Jump to S** if SE1 event flag is set. | 2 or 4 / 2 or 13...20 |
| **JSE2 {#}S** | Jump to S** if SE2 event flag is set. | 2 or 4 / 2 or 13...20 |
| **JSE3 {#}S** | Jump to S** if SE3 event flag is set. | 2 or 4 / 2 or 13...20 |
| **JSE4 {#}S** | Jump to S** if SE4 event flag is set. | 2 or 4 / 2 or 13...20 |
| **JXFI {#}S** | Jump to S** if XFI event flag is set. | 2 or 4 / 2 or 13...20 |
| **JXMT {#}S** | Jump to S** if XMT event flag is set. | 2 or 4 / 2 or 13...20 |
| **JXRL {#}S** | Jump to S** if XRL event flag is set. | 2 or 4 / 2 or 13...20 |
| **JXRO {#}S** | Jump to S** if XRO event flag is set. | 2 or 4 / 2 or 13...20 |
| **POLLATN {WC/WZ/WCZ}** | Get ATN event flag into C/Z, then clear it. | 2 |
| **POLLCT1 {WC/WZ/WCZ}** | Get CT1 event flag into C/Z, then clear it. | 2 |
| **POLLCT2 {WC/WZ/WCZ}** | Get CT2 event flag into C/Z, then clear it. | 2 |
| **POLLCT3 {WC/WZ/WCZ}** | Get CT3 event flag into C/Z, then clear it. | 2 |
| **POLLFBW {WC/WZ/WCZ}** | Get FBW event flag into C/Z, then clear it. | 2 |
| **POLLINT {WC/WZ/WCZ}** | Get INT event flag into C/Z, then clear it. | 2 |
| **POLLPAT {WC/WZ/WCZ}** | Get PAT event flag into C/Z, then clear it. | 2 |
| **POLLQMT {WC/WZ/WCZ}** | Get QMT event flag into C/Z, then clear it. | 2 |
| **POLLSE1 {WC/WZ/WCZ}** | Get SE1 event flag into C/Z, then clear it. | 2 |
| **POLLSE2 {WC/WZ/WCZ}** | Get SE2 event flag into C/Z, then clear it. | 2 |
| **POLLSE3 {WC/WZ/WCZ}** | Get SE3 event flag into C/Z, then clear it. | 2 |
| **POLLSE4 {WC/WZ/WCZ}** | Get SE4 event flag into C/Z, then clear it. | 2 |
| **POLLXFI {WC/WZ/WCZ}** | Get XFI event flag into C/Z, then clear it. | 2 |
| **POLLXMT {WC/WZ/WCZ}** | Get XMT event flag into C/Z, then clear it. | 2 |
| **POLLXRL {WC/WZ/WCZ}** | Get XRL event flag into C/Z, then clear it. | 2 |
| **POLLXRO {WC/WZ/WCZ}** | Get XRO event flag into C/Z, then clear it. | 2 |
| **SETPAT {#}D,{#}S** | Set pin pattern for PAT event. C selects INA/INB, Z selects =/!=, D provides mask value, S provides match value. | 2 |
| **SETSE1 {#}D** | Set SE1 event configuration to D[8:0]. | 2 |
| **SETSE2 {#}D** | Set SE2 event configuration to D[8:0]. | 2 |
| **SETSE3 {#}D** | Set SE3 event configuration to D[8:0]. | 2 |
| **SETSE4 {#}D** | Set SE4 event configuration to D[8:0]. | 2 |
| **WAITATN {WC/WZ/WCZ}** | Wait for ATN event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITCT1 {WC/WZ/WCZ}** | Wait for CT1 event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITCT2 {WC/WZ/WCZ}** | Wait for CT2 event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITCT3 {WC/WZ/WCZ}** | Wait for CT3 event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITFBW {WC/WZ/WCZ}** | Wait for FBW event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITINT {WC/WZ/WCZ}** | Wait for INT event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITPAT {WC/WZ/WCZ}** | Wait for PAT event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITSE1 {WC/WZ/WCZ}** | Wait for SE1 event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITSE2 {WC/WZ/WCZ}** | Wait for SE2 event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITSE3 {WC/WZ/WCZ}** | Wait for SE3 event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITSE4 {WC/WZ/WCZ}** | Wait for SE4 event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITXFI {WC/WZ/WCZ}** | Wait for XFI event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITXMT {WC/WZ/WCZ}** | Wait for XMT event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITXRL {WC/WZ/WCZ}** | Wait for XRL event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |
| **WAITXRO {WC/WZ/WCZ}** | Wait for XRO event flag, then clear it. Prior SETQ sets optional CT timeout value. C/Z = timeout. | 2+ |

---

## Interrupt Instructions

All Interrupt instructions execute in 2 clock cycles.

| Instruction | Description |
|------------|-------------|
| **ALLOWI** | Allow interrupts (default). |
| **BRK {#}D** | If in debug ISR, set next break condition to D. Else, set BRK code to D[7:0] and unconditionally trigger BRK interrupt, if enabled. |
| **COGBRK {#}D** | If in debug ISR, trigger asynchronous breakpoint in cog D[3:0]. Cog D[3:0] must have asynchronous breakpoint enabled. |
| **GETBRK D WC/WZ/WCZ** | Get breakpoint/cog status into D according to WC/WZ/WCZ. See documentation for details. |
| **NIXINT1** | Cancel INT1. |
| **NIXINT2** | Cancel INT2. |
| **NIXINT3** | Cancel INT3. |
| **SETINT1 {#}D** | Set INT1 source to D[3:0]. |
| **SETINT2 {#}D** | Set INT2 source to D[3:0]. |
| **SETINT3 {#}D** | Set INT3 source to D[3:0]. |
| **STALLI** | Stall Interrupts. |
| **TRGINT1** | Trigger INT1, regardless of STALLI mode. |
| **TRGINT2** | Trigger INT2, regardless of STALLI mode. |
| **TRGINT3** | Trigger INT3, regardless of STALLI mode. |

---

## Register Indirection Instructions

All Register Indirection instructions execute in 2 clock cycles.

| Instruction | Description |
|------------|-------------|
| **ALTB D,{#}S** | Alter D field of next instruction to D[13:5]. |
| **ALTB D,{#}S** | Alter D field of next instruction to (D[13:5] + S) & $1FF. D += sign-extended S[17:9]. |
| **ALTD D** | Alter D field of next instruction to D[8:0]. |
| **ALTD D,{#}S** | Alter D field of next instruction to (D + S) & $1FF. D += sign-extended S[17:9]. |
| **ALTGB D** | Alter subsequent GETBYTE/ROLBYTE instruction. Next S field = D[10:2], N field = D[1:0]. |
| **ALTGB D,{#}S** | Alter subsequent GETBYTE/ROLBYTE instruction. Next S field = (D[10:2] + S) & $1FF, N field = D[1:0]. D += sign-extended S[17:9]. |
| **ALTGN D** | Alter subsequent GETNIB/ROLNIB instruction. Next S field = D[11:3], N field = D[2:0]. |
| **ALTGN D,{#}S** | Alter subsequent GETNIB/ROLNIB instruction. Next S field = (D[11:3] + S) & $1FF, N field = D[2:0]. D += sign-extended S[17:9]. |
| **ALTGW D** | Alter subsequent GETWORD/ROLWORD instruction. Next S field = D[9:1], N field = D[0]. |
| **ALTGW D,{#}S** | Alter subsequent GETWORD/ROLWORD instruction. Next S field = ((D[9:1] + S) & $1FF), N field = D[0]. D += sign-extended S[17:9]. |
| **ALTI D** | Execute D in place of next instruction. D stays same. |
| **ALTI D,{#}S** | Substitute next instruction's I/R/D/S fields with fields from D, per S. Modify D per S. |
| **ALTR D** | Alter result register address (normally D field) of next instruction to D[8:0]. |
| **ALTR D,{#}S** | Alter result register address (normally D field) of next instruction to (D + S) & $1FF. D += sign-extended S[17:9]. |
| **ALTS D** | Alter S field of next instruction to D[8:0]. |
| **ALTS D,{#}S** | Alter S field of next instruction to (D + S) & $1FF. D += sign-extended S[17:9]. |
| **ALTSB D** | Alter subsequent SETBYTE instruction. Next D field = D[10:2], N field = D[1:0]. |
| **ALTSB D,{#}S** | Alter subsequent SETBYTE instruction. Next D field = (D[10:2] + S) & $1FF, N field = D[1:0]. D += sign-extended S[17:9]. |
| **ALTSN D** | Alter subsequent SETNIB instruction. Next D field = D[11:3], N field = D[2:0]. |
| **ALTSN D,{#}S** | Alter subsequent SETNIB instruction. Next D field = (D[11:3] + S) & $1FF, N field = D[2:0]. D += sign-extended S[17:9]. |
| **ALTSW D** | Alter subsequent SETWORD instruction. Next D field = D[9:1], N field = D[0]. |
| **ALTSW D,{#}S** | Alter subsequent SETWORD instruction. Next D field = (D[9:1] + S) & $1FF, N field = D[0]. D += sign-extended S[17:9]. |

---

## CORDIC Solver Instructions

| Instruction | Description | Clocks |
|------------|-------------|--------|
| **GETQX D {WC/WZ/WCZ}** | Retrieve CORDIC result X into D. Waits, in case result not ready. C = X[31]. | 2...58 |
| **GETQY D {WC/WZ/WCZ}** | Retrieve CORDIC result Y into D. Waits, in case result not ready. C = Y[31]. | 2...58 |
| **QDIV {#}D,{#}S** | Begin CORDIC unsigned division of {SETQ value or 32'b0, D} / S. GETQX/GETQY retrieves quotient/remainder. | 2...9 |
| **QEXP {#}D** | Begin CORDIC logarithm-to-number conversion of D. GETQX retrieves number. | 2...9 |
| **QFRAC {#}D,{#}S** | Begin CORDIC unsigned division of {D, SETQ value or 32'b0} / S. GETQX/GETQY retrieves quotient/remainder. | 2...9 |
| **QLOG {#}D** | Begin CORDIC number-to-logarithm conversion of D. GETQX retrieves log {5'whole_exponent, 27'fractional_exponent}. | 2...9 |
| **QMUL {#}D,{#}S** | Begin CORDIC unsigned multiplication of D * S. GETQX/GETQY retrieves lower/upper product. | 2...9 |
| **QROTATE {#}D,{#}S** | Begin CORDIC rotation of point (D, SETQ value or 32'b0) by angle S. GETQX/GETQY retrieves X/Y. | 2...9 |
| **QSQRT {#}D,{#}S** | Begin CORDIC square root of {S, D}. GETQX retrieves root. | 2...9 |
| **QVECTOR {#}D,{#}S** | Begin CORDIC vectoring of point (D, S). GETQX/GETQY retrieves length/angle. | 2...9 |

**Note**: Z = (result == 0) for GETQX/GETQY instructions.

---

## Color Space Converter and Pixel Mixer Instructions

### Color Space Converter

All Color Space Converter instructions execute in 2 clock cycles.

| Instruction | Description |
|------------|-------------|
| **SETCFRQ {#}D** | Set the colorspace converter "CFRQ" parameter to D[31:0]. |
| **SETCI {#}D** | Set the colorspace converter "CI" parameter to D[31:0]. |
| **SETCMOD {#}D** | Set the colorspace converter "CMOD" parameter to D[8:0]. |
| **SETCQ {#}D** | Set the colorspace converter "CQ" parameter to D[31:0]. |
| **SETCY {#}D** | Set the colorspace converter "CY" parameter to D[31:0]. |

### Pixel Mixer

| Instruction | Description | Clocks |
|------------|-------------|--------|
| **ADDPIX D,{#}S** | Add bytes of S into bytes of D, with $FF saturation. | 7 |
| **BLNPIX D,{#}S** | Alpha-blend bytes of S into bytes of D, using SETPIV value. | 7 |
| **MIXPIX D,{#}S** | Mix bytes of S into bytes of D, using SETPIX and SETPIV values. | 7 |
| **MULPIX D,{#}S** | Multiply bytes of S into bytes of D, where $FF = 1.0 and $00 = 0.0. | 7 |
| **SETPIV {#}D** | Set BLNPIX/MIXPIX blend factor to D[7:0]. | 2 |
| **SETPIX {#}D** | Set MIXPIX mode to D[5:0]. | 2 |

---

## Lookup Table, Streamer, and Misc Instructions

### Lookup Table

| Instruction | Description | Clocks (Cog&LUT / Hub) |
|------------|-------------|------------------------|
| **RDLUT D,{#}S/P {WC/WZ/WCZ}** | Read data from LUT address {#}S/PTRx into D. C = MSB of data. * | 3 |
| **SETLUTS {#}D** | If D[0] = 1 then enable LUT sharing, where LUT writes within the adjacent odd/even companion cog are copied to this cog's LUT. | 2 |
| **WRLUT {#}D,{#}S/P** | Write D to LUT address {#}S/PTRx. | 2 |

### Streamer

| Instruction | Description | Clocks |
|------------|-------------|--------|
| **GETXACC D** | Get the streamer's Goertzel X accumulator into D and the Y accumulator into the next instruction's S, clear accumulators. | 2 |
| **SETXFRQ {#}D** | Set streamer NCO frequency to D. | 2 |
| **XCONT {#}D,{#}S** | Buffer new streamer command to be issued on final NCO rollover of current command, continuing phase. | 2+ |
| **XINIT {#}D,{#}S** | Issue streamer command immediately, zeroing phase. | 2 |
| **XSTOP** | Stop streamer immediately. | 2 |
| **XZERO {#}D,{#}S** | Buffer new streamer command to be issued on final NCO rollover of current command, zeroing phase. | 2+ |

### Miscellaneous

| Instruction | Description | Clocks |
|------------|-------------|--------|
| **AUGD #n** | Queue #n to be used as upper 23 bits for next #D occurrence, so that the next 9-bit #D will be augmented to 32 bits. | 2 |
| **AUGS #n** | Queue #n to be used as upper 23 bits for next #S occurrence, so that the next 9-bit #S will be augmented to 32 bits. | 2 |
| **GETCT D {WC}** | Get CT[31:0] or CT[63:32] if WC into D. GETCT WC + GETCT gets full CT. CT=0 on reset, CT++ on every clock. C = same. | 2 |
| **GETRND WC/WZ/WCZ** | Get RND into C/Z. C = RND[31], Z = RND[30], unique per cog. | 2 |
| **GETRND D {WC/WZ/WCZ}** | Get RND into D/C/Z. RND is the PRNG that updates on every clock. D = RND[31:0], C = RND[31], Z = RND[30], unique per cog. | 2 |
| **NOP** | No operation. | 2 |
| **POP D {WC/WZ/WCZ}** | Pop stack (K). D = K. C = K[31]. * | 2 |
| **PUSH {#}D** | Push D onto stack. | 2 |
| **SETQ {#}D** | Set Q to D. Use before RDLONG/WRLONG/WMLONG to set block transfer. Also used before MUXQ/COGINIT/QDIV/QFRAC/QROTATE/WAITxxx. | 2 |
| **SETQ2 {#}D** | Set Q to D. Use before RDLONG/WRLONG/WMLONG to set LUT block transfer. | 2 |
| **WAITX {#}D {WC/WZ/WCZ}** | Wait 2 + D clocks if no WC/WZ/WCZ. If WC/WZ/WCZ, wait 2 + (D & RND) clocks. C/Z = 0. | 2+D |

---

## Summary Statistics

- **Total instruction groups**: 10
- **Total instructions documented**: ~450
- **Most common execution time**: 2 clock cycles
- **Variable timing instructions**: Primarily hub access and branch instructions
- **Hub window alignment**: Causes 13...20 or similar clock ranges