|    | 0             | 1                                    | 2               | 3                  | 4           | 5        |
|---:|:--------------|:-------------------------------------|:----------------|:-------------------|:------------|:---------|
|  0 | Instruction   | -INSTR-  ZCRI  -CON-                 | Z Result        | C Result           | Result      | Clocks   |
|    |               | -DEST-                               |                 |                    |             |          |
|    |               | -SRC-                                |                 |                    |             |          |
|  1 | ABS      D, S | 101010 001i 1111 ddddddddd sssssssss | Result = 0      | S[31]              | Written     | 4        |
|  2 | ABSNEG   D, S | 101011 001i 1111 ddddddddd sssssssss | Result = 0      | S[31]              | Written     | 4        |
|  3 | ADD      D, S | 100000 001i 1111 ddddddddd sssssssss | D + S = 0       | Unsigned Carry     | Written     | 4        |
|  4 | ADDABS        | 100010 001i 1111 ddddddddd sssssssss | D + |S| = 0     | Unsigned Carry 3   | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
|  5 | ADDS          | 110100 001i 1111 ddddddddd sssssssss | D + S = 0       | Signed Overflow    | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
|  6 | ADDSX         | 110110 001i 1111 ddddddddd sssssssss | Z & (D+S+C = 0) | Signed Overflow    | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
|  7 | ADDX          | 110010 001i 1111 ddddddddd sssssssss | Z & (D+S+C = 0) | Unsigned Carry     | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
|  8 | AND      D, S | 011000 001i 1111 ddddddddd sssssssss | Result = 0      | Parity of Result   | Written     | 4        |
|  9 | ANDN          | 011001 001i 1111 ddddddddd sssssssss | Result = 0      | Parity of Result   | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 10 | CALL          | 010111 0011 1111 ????????? sssssssss | Result = 0      | ---                | Written     | 4        |
|    | #S            |                                      |                 |                    |             |          |
| 11 | CLKSET   D    | 000011 0001 1111 ddddddddd ------000 | ---             | ---                | Not Written | 8..23 1  |
| 12 | CMP      D, S | 100001 000i 1111 ddddddddd sssssssss | D = S           | Unsigned (D < S)   | Not Written | 4        |
| 13 | CMPS          | 110000 000i 1111 ddddddddd sssssssss | D = S           | Signed (D < S)     | Not Written | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 14 | CMPSUB        | 111000 001i 1111 ddddddddd sssssssss | D = S           | Unsigned (D => S)  | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 15 | CMPSX         | 110001 000i 1111 ddddddddd sssssssss | Z & (D = S+C)   | Signed (D < S+C)   | Not Written | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 16 | CMPX          | 110011 000i 1111 ddddddddd sssssssss | Z & (D = S+C)   | Unsigned (D < S+C) | Not Written | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 17 | COGID         | 000011 0011 1111 ddddddddd ------001 | ID = 0          | 0                  | Written     | 8..23 1  |
|    | D             |                                      |                 |                    |             |          |
| 18 | COGINIT  D    | 000011 0001 1111 ddddddddd ------010 | ID = 0          | No Cog Free        | Not Written | 8..23 1  |
| 19 | COGSTOP  D    | 000011 0001 1111 ddddddddd ------011 | Stopped ID = 0  | No Cog Free        | Not Written | 8..23 1  |
| 20 | DJNZ          | 111001 001i 1111 ddddddddd sssssssss | Result = 0      | Unsigned Borrow    | Written     | 4 or 8 2 |
|    | D, S          |                                      |                 |                    |             |          |
| 21 | HUBOP         | 000011 000i 1111 ddddddddd sssssssss | Result = 0      | ---                | Not Written | 8..23 1  |
|    | D, S          |                                      |                 |                    |             |          |
| 22 | JMP      S    | 010111 000i 1111 --------- sssssssss | Result = 0      | ---                | Not Written | 4        |
| 23 | JMPRET   D, S | 010111 001i 1111 ddddddddd sssssssss | Result = 0      | ---                | Written     | 4        |
| 24 | LOCKCLR  D    | 000011 0001 1111 ddddddddd ------111 | ID = 0          | Prior Lock State   | Not Written | 8..23 1  |
| 25 | LOCKNEW  D    | 000011 0011 1111 ddddddddd ------100 | ID = 0          | No Lock Free       | Written     | 8..23 1  |
| 26 | LOCKRET  D    | 000011 0001 1111 ddddddddd ------101 | ID = 0          | No Lock Free       | Not Written | 8..23 1  |
| 27 | LOCKSET  D    | 000011 0001 1111 ddddddddd ------110 | ID = 0          | Prior Lock State   | Not Written | 8..23 1  |
| 28 | MAX      D, S | 010011 001i 1111 ddddddddd sssssssss | S = 0           | Unsigned (D < S)   | Written     | 4        |
| 29 | MAXS     D, S | 010001 001i 1111 ddddddddd sssssssss | S = 0           | Signed (D < S)     | Written     | 4        |
| 30 | MIN      D, S | 010010 001i 1111 ddddddddd sssssssss | S = 0           | Unsigned (D < S)   | Written     | 4        |
| 31 | MINS     D, S | 010000 001i 1111 ddddddddd sssssssss | S = 0           | Signed (D < S)     | Written     | 4        |
| 32 | MOV      D, S | 101000 001i 1111 ddddddddd sssssssss | Result = 0      | S[31]              | Written     | 4        |
| 33 | MOVD          | 010101 001i 1111 ddddddddd sssssssss | Result = 0      | ---                | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 34 | MOVI          | 010110 001i 1111 ddddddddd sssssssss | Result = 0      | ---                | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 35 | MOVS          | 010100 001i 1111 ddddddddd sssssssss | Result = 0      | ---                | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 36 | MUXC          | 011100 001i 1111 ddddddddd sssssssss | Result = 0      | Parity of Result   | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 37 | MUXNC         | 011101 001i 1111 ddddddddd sssssssss | Result = 0      | Parity of Result   | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 38 | MUXNZ         | 011111 001i 1111 ddddddddd sssssssss | Result = 0      | Parity of Result   | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 39 | MUXZ          | 011110 001i 1111 ddddddddd sssssssss | Result = 0      | Parity of Result   | Written     | 4        |
|    | D, S          |                                      |                 |                    |             |          |
| 40 | NEG      D, S | 101001 001i 1111 ddddddddd sssssssss | Result = 0      | S[31]              | Written     | 4        |