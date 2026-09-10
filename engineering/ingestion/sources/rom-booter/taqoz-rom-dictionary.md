# TAQOZ ROM Dictionary — all 432 words in the P2 boot ROM

**Extracted:** 2026-09-10 · **Machine-readable:** `romdict-data.json`

**Source:** `rom_booter_v33_01j.lst` — the **silicon** build (`ver = "G"`, *Prop2 Silicon v2*;
source v141, 2018-05-27). The dictionary is `romdict` at `$FF466`, ending `$FFFA6` (`END`).

> 🔴 **Not `ROM_Booter.lst`** — that sibling is the FPGA build (`ver = "A"`). See **F-421**.

ROM TAQOZ is **v33h** (`taqoz_name`, `$FD054`). That is what makes any *TAQOZ Reloaded 2.8*
glossary a **superset** claim until it is checked against this list.

## How this was read, and how it checks itself

Each entry is a directive pair the listing describes as `CNT,NAME,ATR,addr16`:

```
ff466     50554403         byte 3,         "DUP"
ff46a     0073             word DUP
```

`byte N` is the name length, `+im` marks an **IMMEDIATE** word, the following `word` is the code
target. Names may embed byte escapes — `byte 3+im, "[",$22,"]"` is the word `["]`, and
`byte 2+im, $2E,$22` is `."` — so a name is rebuilt from all the directive's operands rather
than from its first quoted literal.

**The check:** the listing declares each name's length independently of the name itself.
All **432 of 432** rebuilt names match their declared count, so this parse is verified
by the source rather than asserted. An independent grep of assembled entries returns the same
432. Entries that are commented out carry no address and are excluded automatically.

- **432 words in ROM** · **50 immediate**
- **17 words commented OUT** — in the source, *not* in the ROM (listed at the end)
- One genuine duplicate: **`SDRDS`** at `$FFF03` and `$FFF53`, both targeting `e724`

## A caution about the groupings below

The headings are **the listing's own comment banners**, applied to every word beneath them
until the next banner. They are not a taxonomy we devised, and two of them should be read
loosely: the first 14 words appear *before* any banner, and the listing stops emitting banners
after `CONDITIONAL COMPILATION`, so the 80 words under that heading simply follow it — most
are SPI, terminal and system words that plainly are not conditional-compilation words. The
word, address, target and immediate flag are exact; **the heading is only where it sits.**

### (before the listing's first banner)  (14)

| word | addr | imm | target |
|---|---|:--:|---|
| `DUP` | `$FF466` |  | `DUP` |
| `OVER` | `$FF46C` |  | `OVER` |
| `SWAP` | `$FF473` |  | `SWAP` |
| `ROT` | `$FF47A` |  | `ROT` |
| `-ROT` | `$FF480` |  | `ROT2` |
| `DROP` | `$FF487` |  | `DROP` |
| `3RD` | `$FF48E` |  | `THIRD` |
| `4TH` | `$FF494` |  | `FOURTH` |
| `2DROP` | `$FF49A` |  | `DROP2` |
| `3DROP` | `$FF4A2` |  | `DROP3` |
| `NIP` | `$FF4AA` |  | `NIP` |
| `2SWAP` | `$FF4B0` |  | `DSWAP` |
| `2DUP` | `$FF4B8` |  | `DUP2` |
| `?DUP` | `$FF4BF` |  | `QDUP` |

### BITWISE LOGIC  (4)

| word | addr | imm | target |
|---|---|:--:|---|
| `AND` | `$FF4C6` |  | `_AND` |
| `ANDN` | `$FF4CC` |  | `_ANDN` |
| `OR` | `$FF4D3` |  | `_OR` |
| `XOR` | `$FF4D8` |  | `_XOR` |

### SHIFT  (22)

| word | addr | imm | target |
|---|---|:--:|---|
| `ROL` | `$FF4DE` |  | `_ROL` |
| `ROR` | `$FF4E4` |  | `_ROR` |
| `>>` | `$FF4EA` |  | `_SHR` |
| `<<` | `$FF4EF` |  | `_SHL` |
| `SAR` | `$FF4F4` |  | `_SAR` |
| `2/` | `$FF4FA` |  | `_SHR1` |
| `2*` | `$FF4FF` |  | `_SHL1` |
| `4/` | `$FF504` |  | `_SHR2` |
| `4*` | `$FF509` |  | `_SHL2` |
| `8<<` | `$FF50E` |  | `_SHL8` |
| `16>>` | `$FF514` |  | `_SHR16` |
| `8>>` | `$FF51B` |  | `_SHR8` |
| `9<<` | `$FF521` |  | `_SHL9` |
| `9>>` | `$FF527` |  | `_SHR9` |
| `REV` | `$FF52D` |  | `_REV` |
| `\|<` | `$FF533` |  | `MASK` |
| `>\|` | `$FF538` |  | `ENCODE` |
| `>N` | `$FF53D` |  | `BITS4` |
| `>B` | `$FF542` |  | `BITS8` |
| `>9` | `$FF547` |  | `BITS9` |
| `BITS` | `$FF54C` |  | `BITS` |
| `NOT` | `$FF553` |  | `_NOT` |

### COMPARISON  (27)

| word | addr | imm | target |
|---|---|:--:|---|
| `=` | `$FF559` |  | `_EQ` |
| `<>` | `$FF55D` |  | `_NEQ` |
| `0=` | `$FF562` |  | `_ZEQ` |
| `0<>` | `$FF567` |  | `_ZNE` |
| `0<` | `$FF56D` |  | `_ZLT` |
| `<` | `$FF572` |  | `LT` |
| `U<` | `$FF576` |  | `_ULT` |
| `>` | `$FF57B` |  | `GT` |
| `U>` | `$FF57F` |  | `UGT` |
| `<=` | `$FF584` |  | `LTEQ` |
| `=>` | `$FF589` |  | `EQGT` |
| `WITHIN` | `$FF58E` |  | `WITHIN` |
| `DUPC@` | `$FF597` |  | `DUPCFT` |
| `C@` | `$FF59F` |  | `CFETCH` |
| `W@` | `$FF5A4` |  | `WFETCH` |
| `@` | `$FF5A9` |  | `FETCH` |
| `C+!` | `$FF5AD` |  | `CPLUSST` |
| `C!` | `$FF5B3` |  | `CSTORE` |
| `C@++` | `$FF5B8` |  | `CFETCHINC` |
| `W+!` | `$FF5BF` |  | `WPLUSST` |
| `W!` | `$FF5C5` |  | `WSTORE` |
| `+!` | `$FF5CA` |  | `PLUSST` |
| `!` | `$FF5CF` |  | `STORE` |
| `BIT!` | `$FF5D3` |  | `BITST` |
| `SET` | `$FF5DA` |  | `SET` |
| `CLR` | `$FF5E0` |  | `CLR` |
| `SET?` | `$FF5E6` |  | `BITQ` |

### MATHS  (47)

| word | addr | imm | target |
|---|---|:--:|---|
| `1+` | `$FF5ED` |  | `INC` |
| `1-` | `$FF5F2` |  | `DEC` |
| `2+` | `$FF5F7` |  | `INC2` |
| `2-` | `$FF5FC` |  | `DEC2` |
| `4+` | `$FF601` |  | `INC4` |
| `+` | `$FF606` |  | `PLUS` |
| `-` | `$FF60A` |  | `MINUS` |
| `UM*` | `$FF60E` |  | `UMMUL` |
| `*` | `$FF614` |  | `MULTIPLY` |
| `W*` | `$FF618` |  | `MUL16` |
| `/` | `$FF61D` |  | `DIVIDE` |
| `U/` | `$FF621` |  | `UDIVIDE` |
| `U//` | `$FF626` |  | `UDIVMOD` |
| `//` | `$FF62C` |  | `UMOD` |
| `*/` | `$FF631` |  | `MULDIV` |
| `UM//` | `$FF636` |  | `UMDIVMOD64` |
| `C++` | `$FF63D` |  | `CINC` |
| `C--` | `$FF643` |  | `CDEC` |
| `W++` | `$FF649` |  | `WINC` |
| `W--` | `$FF64F` |  | `WDEC` |
| `++` | `$FF655` |  | `LINC` |
| `--` | `$FF65A` |  | `LDEC` |
| `RND` | `$FF65F` |  | `_RND` |
| `GETRND` | `$FF665` |  | `_GETRND` |
| `SQRT` | `$FF66E` |  | `_SQRT` |
| `SETDACS` | `$FF675` |  | `_SETDACS` |
| `~` | `$FF67F` |  | `CLRL` |
| `~~` | `$FF683` |  | `SETL` |
| `W~` | `$FF688` |  | `CLRW` |
| `W~~` | `$FF68D` |  | `SETW` |
| `C~` | `$FF693` |  | `CLRC` |
| `C~~` | `$FF698` |  | `SETC` |
| `L>S` | `$FF69E` |  | `L2S` |
| `>W` | `$FF6A4` |  | `TOW` |
| `L>W` | `$FF6A9` |  | `L2W` |
| `W>B` | `$FF6AF` |  | `W2B` |
| `W>L` | `$FF6B5` |  | `W2L` |
| `B>W` | `$FF6BB` |  | `B2W` |
| `B>L` | `$FF6C1` |  | `B2L` |
| `MINS` | `$FF6C7` |  | `_MINS` |
| `MAXS` | `$FF6CE` |  | `_MAXS` |
| `MIN` | `$FF6D5` |  | `_MIN` |
| `MAX` | `$FF6DB` |  | `_MAX` |
| `ABS` | `$FF6E1` |  | `_ABS` |
| `-NEGATE` | `$FF6E7` |  | `MNEGATE` |
| `?NEGATE` | `$FF6F1` |  | `QNEGATE` |
| `NEGATE` | `$FF6FB` |  | `NEGATE` |

### CONSTANTS  (5)

| word | addr | imm | target |
|---|---|:--:|---|
| `ON` | `$FF704` |  | `MINUS1` |
| `TRUE` | `$FF709` |  | `MINUS1` |
| `-1` | `$FF710` |  | `MINUS1` |
| `FALSE` | `$FF715` |  | `_0` |
| `OFF` | `$FF71D` |  | `_0` |

### STRUCTURES  (15)

| word | addr | imm | target |
|---|---|:--:|---|
| `GOTO` | `$FF723` | **im** | `GOTO` |
| `IF` | `$FF72A` | **im** | `_IF_` |
| `ELSE` | `$FF72F` | **im** | `_ELSE_` |
| `THEN` | `$FF736` | **im** | `_THEN_` |
| `BEGIN` | `$FF73D` | **im** | `_BEGIN_` |
| `UNTIL` | `$FF745` | **im** | `_UNTIL_` |
| `AGAIN` | `$FF74D` | **im** | `_AGAIN_` |
| `WHILE` | `$FF755` | **im** | `_IF_` |
| `REPEAT` | `$FF75D` | **im** | `_REPEAT_` |
| `SWITCH` | `$FF766` |  | `_SWITCH` |
| `CASE@` | `$FF76F` |  | `SWFETCH` |
| `CASE=` | `$FF777` |  | `ISEQ` |
| `CASE>` | `$FF77F` |  | `ISWITHIN` |
| `BREAK` | `$FF787` | **im** | `ISEND` |
| `CASE` | `$FF78F` | **im** | `_CASE` |

### LOOPS  (22)

| word | addr | imm | target |
|---|---|:--:|---|
| `ADO` | `$FF796` |  | `ADO` |
| `DO` | `$FF79C` |  | `DO` |
| `LOOP` | `$FF7A1` |  | `LOOP` |
| `+LOOP` | `$FF7A8` |  | `PLOOP` |
| `FOR` | `$FF7B0` |  | `FOR` |
| `NEXT` | `$FF7B6` |  | `forNEXT` |
| `?NEXT` | `$FF7BD` |  | `QNEXT` |
| `I` | `$FF7C5` |  | `IX` |
| `J` | `$FF7C9` |  | `J` |
| `LEAVE` | `$FF7CD` |  | `LEAVE` |
| `IC@` | `$FF7D5` |  | `ICFETCH` |
| `I+` | `$FF7DB` |  | `IPLUS` |
| `BOUNDS` | `$FF7E0` |  | `BOUNDS` |
| `H` | `$FF7E9` |  | `H` |
| `L` | `$FF7ED` |  | `L` |
| `T` | `$FF7F1` |  | `_T` |
| `F` | `$FF7F5` |  | `F` |
| `R` | `$FF7F9` |  | `R` |
| `HIGH` | `$FF7FD` |  | `HIGH` |
| `LOW` | `$FF804` |  | `LOW` |
| `FLOAT` | `$FF80A` |  | `_FLOAT` |
| `PIN@` | `$FF812` |  | `PINTEST` |

### SMARTPIN INSTRUCTIONS  (15)

| word | addr | imm | target |
|---|---|:--:|---|
| `WRPIN` | `$FF819` |  | `_WRPIN` |
| `WXPIN` | `$FF821` |  | `_WXPIN` |
| `WYPIN` | `$FF829` |  | `_WYPIN` |
| `RDPIN` | `$FF831` |  | `_RDPIN` |
| `RQPIN` | `$FF839` |  | `_RQPIN` |
| `AKPIN` | `$FF841` |  | `_AKPIN` |
| `WAITPIN` | `$FF849` |  | `WAITPIN` |
| `WRACK` | `$FF853` |  | `WRACK` |
| `PIN` | `$FF85B` |  | `_PIN` |
| `@PIN` | `$FF861` |  | `_ATPIN` |
| `ns` | `$FF868` |  | `ns` |
| `PW` | `$FF86D` |  | `PW` |
| `PULSE` | `$FF872` |  | `PULSE` |
| `PULSES` | `$FF87A` |  | `PULSES` |
| `HILO` | `$FF883` |  | `HILO` |

### SMARTPIN NCO/PWM  (9)

| word | addr | imm | target |
|---|---|:--:|---|
| `DUTY` | `$FF88A` |  | `DUTY` |
| `NCO` | `$FF891` |  | `NCO` |
| `HZ` | `$FF897` |  | `HZ` |
| `KHZ` | `$FF89C` |  | `KHZ` |
| `MHZ` | `$FF8A2` |  | `MHZ` |
| `MUTE` | `$FF8A8` |  | `MUTE` |
| `BLINK` | `$FF8AF` |  | `BLINK` |
| `PWM` | `$FF8B7` |  | `PWM` |
| `SAW` | `$FF8BD` |  | `SAW` |

### SMARTPIN ASYNCH  (48)

| word | addr | imm | target |
|---|---|:--:|---|
| `BIT` | `$FF8C3` |  | `BIT` |
| `BAUD` | `$FF8C9` |  | `BAUDST` |
| `TXD` | `$FF8D0` |  | `TXD` |
| `RXD` | `$FF8D6` |  | `RXD` |
| `TXDAT` | `$FF8DC` |  | `_TXDAT` |
| `WAITX` | `$FF8E4` |  | `DELTA` |
| `WAITCNT` | `$FF8EC` |  | `WAITCNTS` |
| `REBOOT` | `$FF8F6` |  | `REBOOT` |
| `RESET` | `$FF8FF` |  | `RESET` |
| `0EXIT` | `$FF907` |  | `ZEXIT` |
| `EXIT` | `$FF90F` |  | `EXIT` |
| `NOP` | `$FF916` |  | `_NOP` |
| `CALL` | `$FF91C` |  | `ACALL` |
| `JUMP` | `$FF923` |  | `AJMP` |
| `>R` | `$FF92A` |  | `PUSHR` |
| `R>` | `$FF92F` |  | `RPOP` |
| `>L` | `$FF934` |  | `PUSHL` |
| `L>` | `$FF939` |  | `LPOP` |
| `!SP` | `$FF93E` |  | `INITSP` |
| `DEPTH` | `$FF944` |  | `_DEPTH` |
| `COG@` | `$FF94C` |  | `COGFETCH` |
| `COG!` | `$FF953` |  | `COGSTORE` |
| `LUT@` | `$FF95A` |  | `LUTFETCH` |
| `LUT!` | `$FF961` |  | `LUTSTORE` |
| `COGID` | `$FF968` |  | `_COGID` |
| `COGINIT` | `$FF970` |  | `_COGINIT` |
| `COGSTOP` | `$FF97A` |  | `_COGSTOP` |
| `NEWCOG` | `$FF984` |  | `NEWCOG` |
| `COGATN` | `$FF98D` |  | `_COGATN` |
| `POLLATN` | `$FF996` |  | `_POLLATN` |
| `SETEDG` | `$FF9A0` |  | `_SETEDG` |
| `POLLEDG` | `$FF9A9` |  | `_POLLEDG` |
| `KEY` | `$FF9B3` |  | `KEY` |
| `WKEY` | `$FF9B9` |  | `WKEY` |
| `KEY!` | `$FF9C0` |  | `PUTKEY` |
| `CON` | `$FF9C7` |  | `_CON` |
| `NONE` | `$FF9CD` |  | `NONE` |
| `COM` | `$FF9D4` |  | `_COM` |
| `CONKEY` | `$FF9DA` |  | `CONKEY` |
| `CONEMIT` | `$FF9E3` |  | `CONEMIT` |
| `SEROUT` | `$FF9ED` |  | `SEROUT` |
| `EMIT` | `$FF9F6` |  | `EMIT` |
| `EMITS` | `$FF9FD` |  | `EMITS` |
| `CRLF` | `$FFA05` |  | `CRLF` |
| `CR` | `$FFA0C` |  | `CR` |
| `CLS` | `$FFA11` |  | `CLS` |
| `SPACE` | `$FFA17` |  | `SPACE` |
| `SPACES` | `$FFA1F` |  | `SPACES` |

### DUMP MEMORY  (16)

| word | addr | imm | target |
|---|---|:--:|---|
| `RAM` | `$FFA28` |  | `RAM` |
| `DUMP:` | `$FFA2E` |  | `SETDMP` |
| `DUMP` | `$FFA36` |  | `DUMP` |
| `DUMPW` | `$FFA3D` |  | `DUMPW` |
| `DUMPL` | `$FFA45` |  | `DUMPL` |
| `DUMPA` | `$FFA4D` |  | `DUMPA` |
| `DUMPAW` | `$FFA55` |  | `DUMPAW` |
| `QD` | `$FFA5E` |  | `QD` |
| `QW` | `$FFA63` |  | `QW` |
| `DEBUG` | `$FFA68` |  | `DEBUG` |
| `lsio` | `$FFA70` |  | `lsio` |
| `COG` | `$FFA77` |  | `_COG` |
| `LUT` | `$FFA7D` |  | `_LUT` |
| `KB` | `$FFA83` |  | `KB` |
| `MB` | `$FFA88` |  | `MB` |
| `M` | `$FFA8D` |  | `M` |

### PRINTING  (29)

| word | addr | imm | target |
|---|---|:--:|---|
| `.` | `$FFA91` |  | `PRT` |
| `PRINT` | `$FFA95` |  | `PRT` |
| `.AS` | `$FFA9D` |  | `PRTAS` |
| `.AS"` | `$FFAA3` | **im** | `PRTASR` |
| `.DECL` | `$FFAAA` |  | `PRTDECL` |
| `.DEC4` | `$FFAB2` |  | `PRTDEC4` |
| `HOLD` | `$FFABA` |  | `HOLD` |
| `#>` | `$FFAC1` |  | `RHASH` |
| `<#` | `$FFAC6` |  | `LHASH` |
| `#` | `$FFACB` |  | `HASH` |
| `#S` | `$FFACF` |  | `HASHS` |
| `<D>` | `$FFAD4` |  | `DNUM` |
| `U.` | `$FFADA` |  | `UPRT` |
| `.DEC` | `$FFADF` |  | `PRTDEC` |
| `.BIN` | `$FFAE6` |  | `PRTBIN` |
| `.H` | `$FFAED` |  | `PRTHEX` |
| `.B` | `$FFAF2` |  | `PRTB` |
| `.BYTE` | `$FFAF7` |  | `PRTBYTE` |
| `.W` | `$FFAFF` |  | `PRTW` |
| `.WORD` | `$FFB04` |  | `PRTWORD` |
| `.L` | `$FFB0C` |  | `PRTL` |
| `.LONG` | `$FFB11` |  | `PRTLONG` |
| `.ADDR` | `$FFB19` |  | `PRTADR` |
| `PRINT$` | `$FFB21` |  | `PRINTSTR` |
| `LEN$` | `$FFB2A` |  | `STRLEN` |
| `"` | `$FFB31` | **im** | `_STRING_` |
| `."` | `$FFB35` | **im** | `_PSTR_` |
| `CTYPE` | `$FFB3A` |  | `CTYPE` |
| `?EXIT` | `$FFB42` |  | `IFEXIT` |

### MEMORY BLOCKS  (5)

| word | addr | imm | target |
|---|---|:--:|---|
| `DATA?` | `$FFB4A` |  | `DATAQ` |
| `ERASE` | `$FFB52` |  | `ERASE` |
| `FILL` | `$FFB5A` |  | `CFILL` |
| `CMOVE` | `$FFB61` |  | `CMOVE` |
| `<CMOVE` | `$FFB69` |  | `RCMOVE` |

### TIMING  (3)

| word | addr | imm | target |
|---|---|:--:|---|
| `s` | `$FFB72` |  | `secs` |
| `ms` | `$FFB76` |  | `ms` |
| `us` | `$FFB7B` |  | `us` |

### LAP TIMING  (5)

| word | addr | imm | target |
|---|---|:--:|---|
| `CNT@` | `$FFB80` |  | `_GETCNT` |
| `LAP` | `$FFB87` |  | `LAP` |
| `LAP@` | `$FFB8D` |  | `LAPFETCH` |
| `.LAP` | `$FFB94` |  | `PRTLAP` |
| `.ms` | `$FFB9B` |  | `PRTMS` |

### RADIX  (4)

| word | addr | imm | target |
|---|---|:--:|---|
| `HEX` | `$FFBA1` |  | `HEX` |
| `DEC` | `$FFBA7` |  | `DECIMAL` |
| `BIN` | `$FFBAD` |  | `BIN` |
| `.S` | `$FFBB3` |  | `PRTSTK` |

### DICTIONARY  (9)

| word | addr | imm | target |
|---|---|:--:|---|
| `WORDS` | `$FFBB8` |  | `WORDS` |
| `@WORDS` | `$FFBC0` |  | `ATNAMES` |
| `GET$` | `$FFBC9` |  | `_GETWORD` |
| `SEARCH` | `$FFBD0` |  | `SEARCH` |
| `$>#` | `$FFBD9` |  | `NUMBER` |
| `@DATA` | `$FFBDF` |  | `ATDAT` |
| `HERE` | `$FFBE7` |  | `ATHERE` |
| `@HERE` | `$FFBEE` |  | `rg+here` |
| `@CODES` | `$FFBF6` |  | `rg+codes` |

### VARIABLES  (17)

| word | addr | imm | target |
|---|---|:--:|---|
| `uemit` | `$FFBFF` |  | `rg+uemit` |
| `ukey` | `$FFC07` |  | `rg+ukey` |
| `char` | `$FFC0E` |  | `w+lastkey` |
| `delim` | `$FFC15` |  | `rg+delim` |
| `names` | `$FFC1D` |  | `rg+names` |
| `TASK` | `$FFC25` |  | `TASK` |
| `REG` | `$FFC2C` |  | `ATREG` |
| `@WORD` | `$FFC32` |  | `rg+wordbuf` |
| `SPIN` | `$FFC3A` |  | `SPINNER` |
| `\|` | `$FFC41` | **im** | `CCOMP` |
| `\|\|` | `$FFC45` | **im** | `WCOMP` |
| `,` | `$FFC4A` | **im** | `LCOMP` |
| `[W]` | `$FFC4E` | **im** | `COMPW` |
| `["]` | `$FFC54` | **im** | `COMPSTR` |
| `NULL$` | `$FFC5A` |  | `NULLSTR` |
| `$!` | `$FFC62` |  | `STRST` |
| `$=` | `$FFC67` |  | `STREQ` |

### DEFINITIONS  (28)

| word | addr | imm | target |
|---|---|:--:|---|
| `ASM` | `$FFC6C` |  | `_ASM` |
| `FORGET` | `$FFC72` | **im** | `FORGET` |
| `CREATE$` | `$FFC7B` | **im** | `CREATEWORD` |
| `CREATE` | `$FFC85` | **im** | `CREATE` |
| `VAR` | `$FFC8E` | **im** | `_VAR` |
| `pub` | `$FFC94` | **im** | `PUBDEF` |
| `pri` | `$FFC9A` | **im** | `PRIDEF` |
| `pre` | `$FFCA0` | **im** | `PREDEF` |
| `:` | `$FFCA6` | **im** | `NEWDEF` |
| `;` | `$FFCAA` | **im** | `ENDDEF` |
| `[` | `$FFCAE` | **im** | `UNDEF` |
| `]` | `$FFCB2` | **im** | `REDEF` |
| `'` | `$FFCB6` | **im** | `ATICK` |
| `:=` | `$FFCBA` | **im** | `_CONST` |
| `==!` | `$FFCBF` |  | `CONST` |
| `ALIGN` | `$FFCC5` |  | `_ALIGN` |
| `DATCON` | `$FFCCD` | **im** | `_DATCON` |
| `ALLOT` | `$FFCD6` |  | `ALLOT` |
| `org` | `$FFCDE` |  | `DATORG` |
| `bytes` | `$FFCE4` | **im** | `dbytes` |
| `words` | `$FFCEC` | **im** | `dwords` |
| `longs` | `$FFCF4` | **im** | `dlongs` |
| `byte` | `$FFCFC` | **im** | `dbyte` |
| `word` | `$FFD03` | **im** | `dword` |
| `long` | `$FFD0A` | **im** | `dlong` |
| `res` | `$FFD11` |  | `dres` |
| `[C]` | `$FFD17` | **im** | `COMPILES` |
| `GRAB` | `$FFD1D` | **im** | `GRAB` |

### FIELDS  (3)

| word | addr | imm | target |
|---|---|:--:|---|
| `NFA'` | `$FFD24` | **im** | `_NFATICK` |
| `CPA` | `$FFD2B` |  | `NFACPA` |
| `CFA` | `$FFD31` |  | `NFACFA` |

### COMMENTS  (5)

| word | addr | imm | target |
|---|---|:--:|---|
| `\` | `$FFD37` | **im** | `COMMENT` |
| `---` | `$FFD3B` | **im** | `COMMENT` |
| `(` | `$FFD41` | **im** | `PAREN` |
| `{` | `$FFD45` | **im** | `BRACE` |
| `}` | `$FFD49` | **im** | `_NOP` |

### CONDITIONAL COMPILATION  (80)

| word | addr | imm | target |
|---|---|:--:|---|
| `IFNDEF` | `$FFD4D` | **im** | `IFNDEF` |
| `IFDEF` | `$FFD56` | **im** | `IFDEF` |
| `TAQOZ` | `$FFD5E` |  | `_TAQOZ` |
| `TERM` | `$FFD66` |  | `TERMINAL` |
| `AUTO` | `$FFD6D` | **im** | `AUTORUN` |
| `SPIRD` | `$FFD74` |  | `SPIRD` |
| `SPIRDL` | `$FFD7C` |  | `SPIRDL` |
| `SPIWB` | `$FFD85` |  | `SPIWR8` |
| `SPICE` | `$FFD8D` |  | `SPICE` |
| `SPIWC` | `$FFD95` |  | `SPIWRC` |
| `SPIWW` | `$FFD9D` |  | `SPIWR16` |
| `SPIWM` | `$FFDA5` |  | `SPIWM` |
| `SPIWL` | `$FFDAD` |  | `SPIWRL` |
| `SPIPINS` | `$FFDB5` |  | `SPIPINS` |
| `SPIRX` | `$FFDBF` |  | `SPIRX` |
| `SPITXE` | `$FFDC7` |  | `SPITXE` |
| `SPITX` | `$FFDD0` |  | `SPITX` |
| `WAIT` | `$FFDD8` |  | `WAIT` |
| `CLKDIV` | `$FFDDF` |  | `CLKDIV` |
| `RCSLOW` | `$FFDE8` |  | `RCSLOW` |
| `HUBSET` | `$FFDF1` |  | `_HUBSET` |
| `WP` | `$FFDFA` |  | `WP` |
| `WE` | `$FFDFF` |  | `WE` |
| `CLKHZ` | `$FFE04` |  | `CLKHZ` |
| `ERROR` | `$FFE0C` |  | `ERROR` |
| `SFPINS` | `$FFE14` |  | `SFPINS` |
| `SF?` | `$FFE1D` |  | `SFSTAT` |
| `SFWE` | `$FFE23` |  | `SFWE` |
| `SFINS` | `$FFE2A` |  | `SFINS` |
| `SFWD` | `$FFE32` |  | `SFWD` |
| `SFSID` | `$FFE39` |  | `SFSID` |
| `SFJID` | `$FFE41` |  | `SFJID` |
| `SFER4` | `$FFE49` |  | `SFER4` |
| `SFER32` | `$FFE51` |  | `SFER32` |
| `SFER64` | `$FFE5A` |  | `SFER64` |
| `SFERASE` | `$FFE63` |  | `SFERALL` |
| `SFWRPG` | `$FFE6D` |  | `SFWRPAGE` |
| `BACKUP` | `$FFE76` |  | `BACKUP` |
| `RESTORE` | `$FFE7F` |  | `RESTORE` |
| `SFRDS` | `$FFE89` |  | `SFRDS` |
| `SFWRS` | `$FFE91` |  | `SFWRS` |
| `SFC@` | `$FFE99` |  | `SFCFETCH` |
| `SFW@` | `$FFEA0` |  | `SFWFETCH` |
| `SF@` | `$FFEA7` |  | `SFFETCH` |
| `SF` | `$FFEAD` |  | `SF` |
| `.SF` | `$FFEB2` |  | `PRTSF` |
| `SDBUF` | `$FFEB8` |  | `SDBUF` |
| `sdpins` | `$FFEC0` |  | `_sdpins` |
| `MOUNT` | `$FFEC9` |  | `MOUNT` |
| `DIR` | `$FFED1` |  | `PRTDIR` |
| `!SD` | `$FFED7` |  | `INITSD` |
| `!SX` | `$FFEDD` |  | `INITSX` |
| `SD?` | `$FFEE3` |  | `SDQ` |
| `CMD` | `$FFEE9` |  | `CMD` |
| `ACMD` | `$FFEEF` |  | `ACMD` |
| `cid` | `$FFEF6` |  | `w+cid` |
| `SDWR` | `$FFEFC` |  | `SDWR` |
| `SDRDS` | `$FFF03` |  | `SDRDS` |
| `SDWRS` | `$FFF0B` |  | `SDWRS` |
| `FLUSH` | `$FFF13` |  | `FLUSH` |
| `FOPEN` | `$FFF1B` |  | `FOPEN` |
| `FLOAD` | `$FFF23` |  | `FLOAD` |
| `FGET` | `$FFF2B` |  | `FGET` |
| `FREAD` | `$FFF32` |  | `FREAD` |
| `FWRITE` | `$FFF3A` |  | `FWRITE` |
| `SECTOR` | `$FFF43` |  | `SECTOR` |
| `SDRD` | `$FFF4C` |  | `SDRD` |
| `SDRDS` | `$FFF53` |  | `SDRDS` |
| `SDADR` | `$FFF5B` |  | `SDADR` |
| `SD@` | `$FFF63` |  | `SDFETCH` |
| `SD!` | `$FFF69` |  | `SDSTORE` |
| `SDC@` | `$FFF6F` |  | `SDCFETCH` |
| `SDC!` | `$FFF76` |  | `SDCSTORE` |
| `SDW@` | `$FFF7D` |  | `SDWFETCH` |
| `SD` | `$FFF84` |  | `SD` |
| `@FAT` | `$FFF89` |  | `ATFAT` |
| `@BOOT` | `$FFF90` |  | `ATBOOT` |
| `@ROOT` | `$FFF98` |  | `ATROOT` |
| `fat` | `$FFFA0` |  | `w+fat32` |
| `END` | `$FFFA6` |  | `_END` |

## Commented out — in the source, NOT in the ROM

The assembler emitted no address for these, so they are absent from the ROM. A capability
claim naming any of them against the P2 boot ROM is wrong:

```
  .DEC2  .VER  :=  >CHAR  CL>SECT  CLKMHZ  DISCARD  IDLE  LOOKIN  LOOKUP  RDFAT  SHRINP  SHROUT  SKIPNZ  ZEROX  csd  keypoll
```

## What this does NOT establish

- **No semantics.** Names, addresses, targets and the immediate flag — not what each word does.
  That is the code at the target address, which this pass did not read.
- **No stack effects.** The listing carries `( n lo hi -- flg )` comments for some kernel words;
  they are not harvested here, and a stack effect must never be inferred from a name.
- **No ROM-vs-Reloaded diff.** This is the ROM side of that comparison, at v33h. The Reloaded
  glossary is still needed for the other side.
