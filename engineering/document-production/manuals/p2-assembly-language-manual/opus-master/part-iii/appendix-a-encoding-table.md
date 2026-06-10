# Appendix A: Instruction Encoding Master Table

This appendix provides the complete encoding reference for all PASM2 instructions in alphabetical order.

## Reading This Table

| Column | Description |
|--------|-------------|
| Instruction | Mnemonic name |
| Opcode | 7-bit binary pattern (bits 21-27 of instruction word) (bits 28-31 are the EEEE condition-code field; see Appendix B) |
| CZI | Available effects (C=WC, Z=WZ, I=immediate) |
| Cycles | Execution time in clock cycles |
| C Effect | What C flag indicates after instruction execution |
| Z Effect | What Z flag indicates after instruction execution |

**Flag Effect Notation:**

- `---` indicates the flag is not affected by the instruction
- `Result = 0` means the flag is set if the result equals zero
- Specific conditions are described where applicable



## Instruction Encodings

| Instruction | Opcode | CZI | Cycles | C Effect | Z Effect |
|-------------|--------|-----|--------|----------|----------|
| ABS | `0110010` | CZI | 2 | S[31] | Result = 0 |
| ADD | `0001000` | CZI | 2 | carry of (D + S) | Result = 0 |
| ADDCT1 | `1010011` | — | 2 | — | — |
| ADDCT2 | `1010011` | — | 2 | — | — |
| ADDCT3 | `1010011` | — | 2 | — | — |
| ADDPIX | `1010010` | — | 7 | — | — |
| ADDS | `0001010` | CZI | 2 | sign of (D + S) | Result = 0 |
| ADDSX | `0001011` | CZI | 2 | sign of (D+S+C) | Z AND (Result = 0) |
| ADDX | `0001001` | CZI | 2 | carry of (D + S + C) | Z AND (result == 0) |
| AKPIN | `1100000` | — | 2 | — | — |
| ALLOWI | `1101011` | — | 2 | — | — |
| ALTB | `1001100` | — | 2 | — | — |
| ALTD | `1001100` | — | 2 | — | — |
| ALTGB | `1001011` | — | 2 | — | — |
| ALTGN | `1001010` | — | 2 | — | — |
| ALTGW | `1001011` | — | 2 | — | — |
| ALTI | `1001101` | — | 2 | — | — |
| ALTR | `1001100` | — | 2 | — | — |
| ALTS | `1001100` | — | 2 | — | — |
| ALTSB | `1001011` | — | 2 | — | — |
| ALTSN | `1001010` | — | 2 | — | — |
| ALTSW | `1001011` | — | 2 | — | — |
| AND | `0101000` | CZI | 2 | parity of result | Result = 0 |
| ANDN | `0101001` | CZI | 2 | parity of result | Result = 0 |
| ASMCLK | `---` | — | — | — | — |
| AUGD | `1111100` | — | 2 | — | — |
| AUGS | `1111000` | — | 2 | — | — |
| BITC | `0100010` | CZI | 2 | — | original D[S[4:0]] |
| BITH | `0100001` | CZI | 2 | — | original D[S[4:0]] |
| BITL | `0100000` | CZI | 2 | — | original D[S[4:0]] |
| BITNC | `0100011` | CZI | 2 | — | original D[S[4:0]] |
| BITNOT | `0100111` | CZI | 2 | — | original D[S[4:0]] |
| BITNZ | `0100101` | CZI | 2 | — | original D[S[4:0]] |
| BITRND | `0100110` | CZI | 2 | Original D base bit | Original D base bit |
| BITZ | `0100100` | CZI | 2 | — | original D[S[4:0]] |
| BLNPIX | `1010010` | — | 7 | — | — |
| BMASK | `1001110` | — | 2 | — | — |
| BRK | `1101011` | — | 2 | — | — |
| CALL | `1101101` | — | 4 / 13-20 | — | — |
| CALLA | `1101011` | CZ | 5...12 * | D[31] | D[30] |
| CALLB | `1101011` | CZ | 5...12 * | D[31] | D[30] |
| CALLD | `1011001` | CZI | 4 / 13-20 | — | — |
| CALLPA | `1011010` | — | 4 / 13–20 | — | — |
| CALLPB | `1011010` | — | 4 / 13–20 | — | — |
| CMP | `0010000` | CZI | 2 | Unsigned (D < S) | D=S |
| CMPM | `0010101` | CZI | 2 | Result[31] | D=S |
| CMPR | `0010100` | CZI | 2 | borrow of (S - D) | (D == S) |
| CMPS | `0010010` | CZI | 2 | Signed (D < S) | D=S |
| CMPSUB | `0010111` | CZI | 2 | Unsigned(D => S) | Result = 0 |
| CMPSX | `0010011` | CZI | 2 | correct sign of (D - (S + C)) | Z AND (D == S + C) |
| CMPX | `0010001` | CZI | 2 | borrow of (D - (S + C)) | Z AND (D == S + C) |
| COGATN | `1101011` | — | 2 | — | — |
| COGBRK | `1101011` | — | 2 | — | — |
| COGID | `1101011` | C | 2–9, +2 if result | Cog Running | — |
| COGINIT | `1100111` | C | 2–9, +2 if result | No cog available | — |
| COGSTOP | `1101011` | — | 2–9 | — | — |
| CRCBIT | `1001110` | — | 2 | — | — |
| CRCNIB | `1001110` | — | 2 | — | — |
| DEBUG | `---` | — | — | — | — |
| DECMOD | `0111001` | CZI | 2 | Modulus triggered | Result = 0 |
| DECOD | `1001110` | — | 2 | — | — |
| DIRC | `1101011` | CZ | 2 | — | DIR bit |
| DIRH | `1101011` | CZ | 2 | — | DIR bit |
| DIRL | `1101011` | CZ | 2 | — | DIR bit |
| DIRNC | `1101011` | CZ | 2 | — | DIR bit |
| DIRNOT | `1101011` | CZ | 2 | — | DIR bit |
| DIRNZ | `1101011` | CZ | 2 | — | DIR bit |
| DIRRND | `1101011` | CZ | 2 | Original DIRx base bit | Original DIRx base bit |
| DIRZ | `1101011` | CZ | 2 | — | DIR bit |
| DJF | `1011011` | — | 2 or 4 | — | — |
| DJNF | `1011011` | — | 2 or 4 | — | — |
| DJNZ | `1011011` | — | 2 or 4 | — | — |
| DJZ | `1011011` | — | 2 or 4 | — | — |
| DRVC | `1101011` | CZ | 2 | — | OUT bit |
| DRVH | `1101011` | CZ | 2 | — | OUT bit |
| DRVL | `1101011` | CZ | 2 | — | OUT bit |
| DRVNC | `1101011` | CZ | 2 | — | OUT bit |
| DRVNOT | `1101011` | CZ | 2 | — | OUT bit |
| DRVNZ | `1101011` | CZ | 2 | — | OUT bit |
| DRVRND | `1101011` | CZ | 2 | Original OUTx base bit | Original OUTx base bit |
| DRVZ | `1101011` | CZ | 2 | — | OUT bit |
| ENCOD | `0111100` | CZI | 2 | S != 0 | Result = 0 |
| EXECF | `1101011` | — | 4 | — | — |
| FBLOCK | `1100100` | — | 2 | — | — |
| FGE | `0011000` | CZI | 2 | limit enforced | Result = 0 |
| FGES | `0011010` | CZI | 2 | limit enforced | Result = 0 |
| FLE | `0011001` | CZI | 2 | limit enforced | Result = 0 |
| FLES | `0011011` | CZI | 2 | limit enforced | Result = 0 |
| FLTC | `1101011` | CZ | 2 | — | OUT bit |
| FLTH | `1101011` | CZ | 2 | — | OUT bit |
| FLTL | `1101011` | CZ | 2 | — | OUT bit |
| FLTNC | `1101011` | CZ | 2 | — | OUT bit |
| FLTNOT | `1101011` | CZ | 2 | — | OUT bit |
| FLTNZ | `1101011` | CZ | 2 | — | OUT bit |
| FLTRND | `1101011` | CZ | 2 | Original OUTx base bit | Original OUTx base bit |
| FLTZ | `1101011` | CZ | 2 | — | OUT bit |
| GETBRK | `1101011` | CZ | 2 | — | — |
| GETBYTE | `1000111` | — | 2 | — | — |
| GETCT | `1101011` | C | 2 | same | — |
| GETNIB | `1000010` | — | 2 | — | — |
| GETPTR | `1101011` | — | 2 | — | — |
| GETQX | `1101011` | CZ | 2...58 | X[31] | Result = 0 |
| GETQY | `1101011` | CZ | 2...58 | Y[31] | Result = 0 |
| GETRND | `1101011` | CZ | 2 | RND[31] | RND[30], unique per cog |
| GETSCP | `1101011` | — | 2 | — | — |
| GETWORD | `1001001` | — | 2 | — | — |
| GETXACC | `1101011` | — | 2 | — | — |
| HUBSET | `1101011` | — | 2...9 | — | — |
| IJNZ | `1011100` | — | 2 or 4 | — | — |
| IJZ | `1011100` | — | 2 or 4 | — | — |
| INCMOD | `0111000` | CZI | 2 | 1, else D = D + 1 and C = 0 | Result = 0 |
| JATN | `1011110` | — | 2 or 4 | — | — |
| JCT1 | `1011110` | — | 2 or 4 | — | — |
| JCT2 | `1011110` | — | 2 or 4 | — | — |
| JCT3 | `1011110` | — | 2 or 4 | — | — |
| JFBW | `1011110` | — | 2 or 4 | — | — |
| JINT | `1011110` | — | 2 or 4 | — | — |
| JMP | `1101011` | CZ | 4 | D[31] | D[30] |
| JMPREL | `1101011` | — | 4 | — | — |
| JNATN | `1011110` | — | 2 or 4 | — | — |
| JNCT1 | `1011110` | — | 2 or 4 | — | — |
| JNCT2 | `1011110` | — | 2 or 4 | — | — |
| JNCT3 | `1011110` | — | 2 or 4 | — | — |
| JNFBW | `1011110` | — | 2 or 4 | — | — |
| JNINT | `1011110` | — | 2 or 4 | — | — |
| JNPAT | `1011110` | — | 2 or 4 | — | — |
| JNQMT | `1011110` | — | 2 or 4 | — | — |
| JNSE1 | `1011110` | — | 2 or 4 | — | — |
| JNSE2 | `1011110` | — | 2 or 4 | — | — |
| JNSE3 | `1011110` | — | 2 or 4 | — | — |
| JNSE4 | `1011110` | — | 2 or 4 | — | — |
| JNXFI | `1011110` | — | 2 or 4 | — | — |
| JNXMT | `1011110` | — | 2 or 4 | — | — |
| JNXRL | `1011110` | — | 2 or 4 | — | — |
| JNXRO | `1011110` | — | 2 or 4 | — | — |
| JPAT | `1011110` | — | 2 or 4 | — | — |
| JQMT | `1011110` | — | 2 or 4 | — | — |
| JSE1 | `1011110` | — | 2 or 4 | — | — |
| JSE2 | `1011110` | — | 2 or 4 | — | — |
| JSE3 | `1011110` | — | 2 or 4 | — | — |
| JSE4 | `1011110` | — | 2 or 4 | — | — |
| JXFI | `1011110` | — | 2 or 4 | — | — |
| JXMT | `1011110` | — | 2 or 4 | — | — |
| JXRL | `1011110` | — | 2 or 4 | — | — |
| JXRO | `1011110` | — | 2 or 4 | — | — |
| LOC | `1110100` | — | 2 | — | — |
| LOCKNEW | `1101011` | C | 4...11 | 1 if no LOCK available | — |
| LOCKREL | `1101011` | C | 2...9, +2 if result | — | — |
| LOCKRET | `1101011` | — | 2...9 | — | — |
| LOCKTRY | `1101011` | C | 2...9, +2 if result | 1 if got LOCK | — |
| MERGEB | `1101011` | — | 2 | — | — |
| MERGEW | `1101011` | — | 2 | — | — |
| MIXPIX | `1010010` | — | 7 | — | — |
| MODC | `1101011` | — | 2 | cccc[{C,Z}] | — |
| MODCZ | `1101011` | — | 2 | cccc[{C,Z}] | zzzz[{C,Z}] |
| MODZ | `1101011` | — | 2 | — | zzzz[{C,Z}] |
| MOV | `0110000` | CZI | 2 | S[31] | Result = 0 |
| MOVBYTS | `1001111` | — | 2 | — | — |
| MUL | `1010000` | I | 2 | — | (D = 0) OR (S = 0) |
| MULPIX | `1010010` | — | 7 | — | — |
| MULS | `1010000` | I | 2 | — | (D = 0) OR (S = 0) |
| MUXC | `0101100` | CZI | 2 | parity of result | Result = 0 |
| MUXNC | `0101101` | CZI | 2 | parity of result | Result = 0 |
| MUXNIBS | `1001111` | — | 2 | — | — |
| MUXNITS | `1001111` | — | 2 | — | — |
| MUXNZ | `0101111` | CZI | 2 | parity of result | Result = 0 |
| MUXQ | `1001111` | — | 2 | — | — |
| MUXZ | `0101110` | CZI | 2 | parity of result | Result = 0 |
| NEG | `0110011` | CZI | 2 | Sign of result | Result = 0 |
| NEGC | `0110100` | CZI | 2 | Sign of result | Result = 0 |
| NEGNC | `0110101` | CZI | 2 | Sign of result | Result = 0 |
| NEGNZ | `0110111` | CZI | 2 | Sign of result | Result = 0 |
| NEGZ | `0110110` | CZI | 2 | Sign of result | Result = 0 |
| NIXINT1 | `1101011` | — | 2 | — | — |
| NIXINT2 | `1101011` | — | 2 | — | — |
| NIXINT3 | `1101011` | — | 2 | — | — |
| NOP | `0000000` | — | 2 | — | — |
| NOT | `0110001` | CZI | 2 | !S[31] | Result = 0 |
| ONES | `0111101` | CZI | 2 | Result is odd | Result = 0 |
| OR | `0101010` | CZI | 2 | Parity of Result | Result = 0 |
| OUTC | `1101011` | CZ | 2 | — | OUT bit |
| OUTH | `1101011` | CZ | 2 | — | OUT bit |
| OUTL | `1101011` | CZ | 2 | — | OUT bit |
| OUTNC | `1101011` | CZ | 2 | — | OUT bit |
| OUTNOT | `1101011` | CZ | 2 | — | OUT bit |
| OUTNZ | `1101011` | CZ | 2 | — | OUT bit |
| OUTRND | `1101011` | CZ | 2 | Original OUTx base bit | Original OUTx base bit |
| OUTZ | `1101011` | CZ | 2 | — | OUT bit |
| POLLATN | `1101011` | — | 2 | ATN Event | ATN Event |
| POLLCT1 | `1101011` | — | 2 | CT1 Event | CT1 Event |
| POLLCT2 | `1101011` | — | 2 | CT2 Event | CT2 Event |
| POLLCT3 | `1101011` | — | 2 | CT3 Event | CT3 Event |
| POLLFBW | `1101011` | — | 2 | FBW Event | FBW Event |
| POLLINT | `1101011` | — | 2 | INT Event | INT Event |
| POLLPAT | `1101011` | — | 2 | PAT Event | PAT Event |
| POLLQMT | `1101011` | — | 2 | QMT Event | QMT Event |
| POLLSE1 | `1101011` | — | 2 | SE1 Event | SE1 Event |
| POLLSE2 | `1101011` | — | 2 | SE2 Event | SE2 Event |
| POLLSE3 | `1101011` | — | 2 | SE3 Event | SE3 Event |
| POLLSE4 | `1101011` | — | 2 | SE4 Event | SE4 Event |
| POLLXFI | `1101011` | — | 2 | XFI Event | XFI Event |
| POLLXMT | `1101011` | — | 2 | XMT Event | XMT Event |
| POLLXRL | `1101011` | — | 2 | XRL Event | XRLEvent |
| POLLXRO | `1101011` | — | 2 | XRO Event | XRO Event |
| POP | `1101011` | CZ | 2 | K[31] | Result = 0 |
| POPA | `1011000` | CZ | 9...16 * | MSB of long | Result = 0 |
| POPB | `1011000` | CZ | 9...16 * | MSB of long | Result = 0 |
| PUSH | `1101011` | — | 2 | — | — |
| PUSHA | `1100011` | — | 3...10* | — | — |
| PUSHB | `1100011` | — | 3...10* | — | — |
| QDIV | `1101000` | — | 2...9 | — | — |
| QEXP | `1101011` | — | 2...9 | — | — |
| QFRAC | `1101001` | — | 2...9 | — | — |
| QLOG | `1101011` | — | 2...9 | — | — |
| QMUL | `1101000` | — | 2...9 | — | — |
| QROTATE | `1101010` | — | 2...9 | — | — |
| QSQRT | `1101001` | — | 2...9 | — | — |
| QVECTOR | `1101010` | — | 2...9 | — | — |
| RCL | `0000101` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 |
| RCR | `0000100` | CZI | 2 | Last bit out1 | Result = 0 |
| RCZL | `1101011` | CZ | 2 | D[31] | D[30] |
| RCZR | `1101011` | CZ | 2 | D[1] | D[0] |
| RDBYTE | `1010110` | CZI | 9...16 | MSB of byte | Result = 0 |
| RDFAST | `1100011` | — | 2 or WRFAST finish + 10...17 | — | — |
| RDLONG | `1011000` | CZI | 9...16 * | MSB of long | — |
| RDLUT | `1010101` | CZI | 3 | MSB of data | Result = 0 |
| RDPIN | `1010100` | C | 2 | modal result | — |
| RDWORD | `1010111` | CZI | 9...16 * | MSB of word | Result = 0 |
| REP | `1100110` | — | 2 | — | — |
| RESI0 | `1011001` | — | 4 | — | — |
| RESI1 | `1011001` | — | 4 | — | — |
| RESI2 | `1011001` | — | 4 | — | — |
| RESI3 | `1011001` | — | 4 | — | — |
| RET | `1101011` | — | 4 | K[31] | K[30] |
| RETA | `1101011` | — | 11...18 * | L[31] | L[30] |
| RETB | `1101011` | — | 11...18 * | L[31] | L[30] |
| RETI0 | `1011001` | — | 4 | — | — |
| RETI1 | `1011001` | — | 4 | — | — |
| RETI2 | `1011001` | — | 4 | — | — |
| RETI3 | `1011001` | — | 4 | — | — |
| REV | `1101011` | — | 2 | — | — |
| RFBYTE | `1101011` | CZ | 2 | MSB of byte | Result = 0 |
| RFLONG | `1101011` | CZ | 2 | MSB of long | Result = 0 |
| RFVAR | `1101011` | CZ | 2 | 0 | Result = 0 |
| RFVARS | `1101011` | CZ | 2 | MSB of value | Result = 0 |
| RFWORD | `1101011` | CZ | 2 | MSB of word | Result = 0 |
| RGBEXP | `1101011` | — | 2 | — | — |
| RGBSQZ | `1101011` | — | 2 | — | — |
| ROL | `0000001` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 |
| ROLBYTE | `1001000` | — | 2 | — | — |
| ROLNIB | `1000100` | — | 2 | — | — |
| ROLWORD | `1001010` | — | 2 | — | — |
| ROR | `0000000` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[0] | Result = 0 |
| RQPIN | `1010100` | C | 2 | modal result | — |
| SAL | `0000111` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 |
| SAR | `0000110` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[0] | Result = 0 |
| SCA | `1010001` | I | 2 | — | Product = 0 |
| SCAS | `1010001` | I | 2 | — | Result = 0 |
| SETBYTE | `1000110` | — | 2 | — | — |
| SETCFRQ | `1101011` | — | 2 | — | — |
| SETCI | `1101011` | — | 2 | — | — |
| SETCMOD | `1101011` | — | 2 | — | — |
| SETCQ | `1101011` | — | 2 | — | — |
| SETCY | `1101011` | — | 2 | — | — |
| SETD | `1001101` | — | 2 | — | — |
| SETDACS | `1101011` | — | 2 | — | — |
| SETINT1 | `1101011` | — | 2 | — | — |
| SETINT2 | `1101011` | — | 2 | — | — |
| SETINT3 | `1101011` | — | 2 | — | — |
| SETLUTS | `1101011` | — | 2 | — | — |
| SETNIB | `1000000` | — | 2 | — | — |
| SETPAT | `1011111` | — | 2 | — | — |
| SETPIV | `1101011` | — | 2 | — | — |
| SETPIX | `1101011` | — | 2 | — | — |
| SETQ | `1101011` | — | 2 | — | — |
| SETQ2 | `1101011` | — | 2 | — | — |
| SETR | `1001101` | — | 2 | — | — |
| SETS | `1001101` | — | 2 | — | — |
| SETSCP | `1101011` | — | 2 | — | — |
| SETSE1 | `1101011` | — | 2 | — | — |
| SETSE2 | `1101011` | — | 2 | — | — |
| SETSE3 | `1101011` | — | 2 | — | — |
| SETSE4 | `1101011` | — | 2 | — | — |
| SETWORD | `1001001` | — | 2 | — | — |
| SETXFRQ | `1101011` | — | 2 | — | — |
| SEUSSF | `1101011` | — | 2 | — | — |
| SEUSSR | `1101011` | — | 2 | — | — |
| SHL | `0000011` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[31] | Result = 0 |
| SHR | `0000010` | CZI | 2 | last bit shifted out if S[4:0] > 0, else D[0] | Result = 0 |
| SIGNX | `0111011` | CZI | 2 | MSB of result | Result = 0 |
| SKIP | `1101011` | — | 2 | — | — |
| SKIPF | `1101011` | — | 2 | — | — |
| SPLITB | `1101011` | — | 2 | — | — |
| SPLITW | `1101011` | — | 2 | — | — |
| STALLI | `1101011` | — | 2 | — | — |
| SUB | `0001100` | CZI | 2 | borrow of (D - S) | Result = 0 |
| SUBR | `0010110` | CZI | 2 | borrow of (S - D) | Result = 0 |
| SUBS | `0001110` | CZI | 2 | sign of (D - S) | Result = 0 |
| SUBSX | `0001111` | CZI | 2 | sign of D-(S+C) | Z AND (Result = 0) |
| SUBX | `0001101` | CZI | 2 | borrow of (D - (S + C)) | Z AND (result == 0) |
| SUMC | `0011100` | CZI | 2 | 1 then D = D - S, else D = D + S. C = correct sign of (D +/- S) | Result = 0 |
| SUMNC | `0011101` | CZI | 2 | 0 then D = D - S, else D = D + S. C = correct sign of (D +/- S) | Result = 0 |
| SUMNZ | `0011111` | CZI | 2 | correct sign of (D +/- S) | 0 then D = D - S, else D = D + S |
| SUMZ | `0011110` | CZI | 2 | correct sign of (D +/- S) | 1 then D = D - S, else D = D + S |
| TEST | `0111110` | CZ | 2 | Parity of (D & S) | (D & S) = 0 |
| TESTB | `0100000` | CZI | 2 | D[S[4:0]] | D[S[4:0]] |
| TESTBN | `0100001` | CZI | 2 | !D[S[4:0]] | !D[S[4:0]] |
| TESTN | `0111111` | CZI | 2 | Parity of (D & !S) | (D & !S) = 0 |
| TESTP | `1101011` | CZ | 2 | IN[D[5:0]] | IN[D[5:0]] |
| TESTPN | `1101011` | CZ | 2 | !IN[D[5:0]] | !IN[D[5:0]] |
| TJF | `1011101` | — | 2 or 4 | — | — |
| TJNF | `1011101` | — | 2 or 4 / 2 or 13-20 | — | — |
| TJNS | `1011101` | — | 2 or 4 | — | — |
| TJNZ | `1011100` | — | 2 or 4 | — | — |
| TJS | `1011101` | — | 2 or 4 / 2 or 13-20 | — | — |
| TJV | `1011110` | — | 2 or 4 / 2 or 13–20 | — | — |
| TJZ | `1011100` | — | 2 or 4 | — | — |
| TRGINT1 | `1101011` | — | 2 | — | — |
| TRGINT2 | `1101011` | — | 2 | — | — |
| TRGINT3 | `1101011` | — | 2 | — | — |
| WAITATN | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITCT1 | `1101011` | — | 2+ | timeout | timeout |
| WAITCT2 | `1101011` | — | 2+ | timeout | timeout |
| WAITCT3 | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITFBW | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITINT | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITPAT | `1101011` | — | 2+ | timeout | timeout |
| WAITSE1 | `1101011` | — | 2+ | timeout | timeout |
| WAITSE2 | `1101011` | — | 2+ | timeout | timeout |
| WAITSE3 | `1101011` | — | 2+ | timeout | timeout |
| WAITSE4 | `1101011` | — | 2+ | timeout | timeout |
| WAITX | `1101011` | CZ | 2 + D | 0 | 0 |
| WAITXFI | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITXMT | `1101011` | — | 2+ | timeout | timeout |
| WAITXRL | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WAITXRO | `1101011` | — | 2+ | Timeout Abort | Timeout Abort |
| WFBYTE | `1101011` | — | 2 | — | — |
| WFLONG | `1101011` | — | 2 | — | — |
| WFWORD | `1101011` | — | 2 | — | — |
| WMLONG | `1010011` | — | 3...10 * | — | — |
| WRBYTE | `1100010` | — | 3...10 | — | — |
| WRC | `1101011` | — | 2 | — | — |
| WRFAST | `1100100` | — | 2 or WRFAST finish + 3 | — | — |
| WRLONG | `1100011` | — | 3...10* | — | — |
| WRLUT | `1100001` | — | 2 | — | — |
| WRNC | `1101011` | — | 2 | — | — |
| WRNZ | `1101011` | — | 2 | — | — |
| WRPIN | `1100000` | — | 2 | — | — |
| WRWORD | `1100010` | — | 3...10* | — | — |
| WRZ | `1101011` | — | 2 | — | — |
| WXPIN | `1100000` | — | 2 | — | — |
| WYPIN | `1100001` | — | 2 | — | — |
| XCONT | `1100110` | — | 2+ | — | — |
| XINIT | `1100101` | — | 2 | — | — |
| XOR | `0101011` | CZI | 2 | Parity of Result | Result = 0 |
| XORO32 | `1101011` | — | 2 | — | — |
| XSTOP | `1100101` | — | 2 | — | — |
| XZERO | `1100101` | — | 2+ | — | — |
| ZEROX | `0111010` | CZI | 2 | MSB of result | Result = 0 |

**Total Instructions:** 359 (357 with a fixed encoding + 2 without: ASMCLK and DEBUG)



**Notes:**

- This table shows the primary encoding for each instruction
- Instructions with multiple encoding forms show only the most common variant
- Multi-cycle instructions show ranges (e.g., `2...9`) where timing depends on:
  - Hub synchronization (variable wait for hub access)
  - Operation parameters (CORDIC solver iterations, streamer operations)
  - Memory location (cog vs. LUT vs. hub execution)
- The `*` symbol indicates hub memory access with variable timing
- See Part II (Instruction Reference) for complete encoding details and all variants
- ASMCLK is a pseudo-instruction (macro) and DEBUG is a debug directive; neither has a single fixed hardware encoding (ASMCLK expands to HUBSET/WAITX, DEBUG emits a debug call under -d)

