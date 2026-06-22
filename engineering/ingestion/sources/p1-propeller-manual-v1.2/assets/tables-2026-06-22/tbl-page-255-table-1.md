|    | 0             | 1                                    | 2                                                       | 3                 | 4           | 5        |
|---:|:--------------|:-------------------------------------|:--------------------------------------------------------|:------------------|:------------|:---------|
|  0 | Instruction   | -INSTR-  ZCRI  -CON-                 | Z Result                                                | C Result          | Result      | Clocks   |
|    |               | -DEST-                               |                                                         |                   |             |          |
|    |               | -SRC-                                |                                                         |                   |             |          |
|  1 | NEGC     D, S | 101100 001i 1111 ddddddddd sssssssss | Result = 0                                              | S[31]             | Written     | 4        |
|  2 | NEGNC    D, S | 101101 001i 1111 ddddddddd sssssssss | Result = 0                                              | S[31]             | Written     | 4        |
|  3 | NEGNZ    D, S | 101111 001i 1111 ddddddddd sssssssss | Result = 0                                              | S[31]             | Written     | 4        |
|  4 | NEGZ     D, S | 101110 001i 1111 ddddddddd sssssssss | Result = 0                                              | S[31]             | Written     | 4        |
|  5 | NOP           | ------ ---- 0000 --------- --------- | ---                                                     | ---               | ---         | 4        |
|  6 | OR       D, S | 011010 001i 1111 ddddddddd sssssssss | Result = 0                                              | Parity of Result  | Written     | 4        |
|  7 | RCL      D, S | 001101 001i 1111 ddddddddd sssssssss | Result = 0                                              | D[31]             | Written     | 4        |
|  8 | RCR      D, S | 001100 001i 1111 ddddddddd sssssssss | Result = 0                                              | D[0]              | Written     | 4        |
|  9 | RDBYTE   D, S | 000000 001i 1111 ddddddddd sssssssss | Result = 0                                              | ---               | Written     | 8..23 1  |
| 10 | RDLONG   D, S | 000010 001i 1111 ddddddddd sssssssss | Result = 0                                              | ---               | Written     | 8..23 1  |
| 11 | RDWORD   D, S | 000001 001i 1111 ddddddddd sssssssss | Result = 0                                              | ---               | Written     | 8..23 1  |
| 12 | RET           | 010111 0001 1111 --------- --------- | Result = 0                                              | ---               | Not Written | 4        |
| 13 | REV      D, S | 001111 001i 1111 ddddddddd sssssssss | Result = 0                                              | D[0]              | Written     | 4        |
| 14 | ROL      D, S | 001001 001i 1111 ddddddddd sssssssss | Result = 0                                              | D[31]             | Written     | 4        |
| 15 | ROR      D, S | 001000 001i 1111 ddddddddd sssssssss | Result = 0                                              | D[0]              | Written     | 4        |
| 16 | SAR      D, S | 001110 001i 1111 ddddddddd sssssssss | Result = 0                                              | D[0]              | Written     | 4        |
| 17 | SHL      D, S | 001011 001i 1111 ddddddddd sssssssss | Result = 0                                              | D[31]             | Written     | 4        |
| 18 | SHR      D, S | 001010 001i 1111 ddddddddd sssssssss | Result = 0                                              | D[0]              | Written     | 4        |
| 19 | SUB      D, S | 100001 001i 1111 ddddddddd sssssssss | D - S = 0                                               | Unsigned Borrow   | Written     | 4        |
| 20 | SUBABS        | 100011 001i 1111 ddddddddd sssssssss | D - |S| = 0                                             | Unsigned Borrow 4 | Written     | 4        |
|    | D, S          |                                      |                                                         |                   |             |          |
| 21 | SUBS          | 110101 001i 1111 ddddddddd sssssssss | D - S = 0                                               | Signed Overflow   | Written     | 4        |
|    | D, S          |                                      |                                                         |                   |             |          |
| 22 | SUBSX         |                                      | 110111 001i 1111 ddddddddd sssssssss  Z & (D-(S+C) = 0) | Signed Overflow   | Written     | 4        |
|    | D, S          |                                      |                                                         |                   |             |          |
| 23 | SUBX          |                                      | 110011 001i 1111 ddddddddd sssssssss  Z & (D-(S+C) = 0) | Unsigned Borrow   | Written     | 4        |
|    | D, S          |                                      |                                                         |                   |             |          |
| 24 | SUMC          | 100100 001i 1111 ddddddddd sssssssss | D ± S = 0                                               | Signed Overflow   | Written     | 4        |
|    | D, S          |                                      |                                                         |                   |             |          |
| 25 | SUMNC         | 100101 001i 1111 ddddddddd sssssssss | D ± S = 0                                               | Signed Overflow   | Written     | 4        |
|    | D, S          |                                      |                                                         |                   |             |          |
| 26 | SUMNZ         | 100111 001i 1111 ddddddddd sssssssss | D ± S = 0                                               | Signed Overflow   | Written     | 4        |
|    | D, S          |                                      |                                                         |                   |             |          |
| 27 | SUMZ     D, S | 100110 001i 1111 ddddddddd sssssssss | D ± S = 0                                               | Signed Overflow   | Written     | 4        |
| 28 | TEST     D, S | 011000 000i 1111 ddddddddd sssssssss | D = 0                                                   | Parity of Result  | Not Written | 4        |
| 29 | TESTN    D, S | 011001 000i 1111 ddddddddd sssssssss | D = 0                                                   | Parity of Result  | Not Written | 4        |
| 30 | TJNZ     D, S | 111010 000i 1111 ddddddddd sssssssss | D = 0                                                   | 0                 | Not Written | 4 or 8 2 |
| 31 | TJZ      D, S | 111011 000i 1111 ddddddddd sssssssss | D = 0                                                   | 0                 | Not Written | 4 or 8 2 |
| 32 | WAITCNT  D, S | 111110 001i 1111 ddddddddd sssssssss | Result = 0                                              | Unsigned Carry    | Written     | 6+       |
| 33 | WAITPEQ  D, S | 111100 000i 1111 ddddddddd sssssssss | Result = 0                                              | ---               | Not Written | 6+       |
| 34 | WAITPNE  D, S | 111101 000i 1111 ddddddddd sssssssss | Result = 0                                              | ---               | Not Written | 6+       |
| 35 | WAITVID  D, S | 111111 000i 1111 ddddddddd sssssssss | Result = 0                                              | ---               | Not Written | 4+ 5     |
| 36 | WRBYTE   D, S | 000000 000i 1111 ddddddddd sssssssss | ---                                                     | ---               | Not Written | 8..23 1  |
| 37 | WRLONG   D, S | 000010 000i 1111 ddddddddd sssssssss | ---                                                     | ---               | Not Written | 8..23 1  |
| 38 | WRWORD   D, S | 000001 000i 1111 ddddddddd sssssssss | ---                                                     | ---               | Not Written | 8..23 1  |
| 39 | XOR  D,       | 011011 001i 1111 ddddddddd sssssssss | Result = 0                                              | Parity of Result  | Written     | 4        |
|    | S             |                                      |                                                         |                   |             |          |