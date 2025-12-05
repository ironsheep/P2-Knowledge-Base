# Appendix G: Reserved Words Reference

This appendix lists all reserved words in PASM2. These identifiers cannot be used as user-defined labels, symbols, or variable names. Attempting to use a reserved word as a label will result in an assembly error.

**Total Reserved Words: 449**

## Categories

Reserved words fall into six main categories:

1. **Instruction Mnemonics** (358 words) - All instruction names
2. **Assembly Directives** (14 words) - Assembly-time directives
3. **Predefined Constants** (11 words) - Built-in constant values
4. **Special Register Names** (16 words) - Special-purpose registers
5. **Condition Keywords** (41 words) - Conditional execution prefixes
6. **Effect Keywords** (9 words) - Flag modification suffixes



## Instruction Mnemonics (358 words)

All PASM2 instruction names are reserved. These appear in alphabetical order for quick reference:

```
ABS         ADD         ADDCT1      ADDCT2      ADDCT3      ADDPIX
ADDS        ADDSX       ADDX        AKPIN       ALLOWI      ALTB
ALTD        ALTGB       ALTGN       ALTGW       ALTI        ALTR
ALTS        ALTSB       ALTSN       ALTSW       AND         ANDN
ASMCLK      AUGD        AUGS        BITC        BITH        BITL
BITNC       BITNOT      BITNZ       BITRND      BITZ        BLNPIX
BMASK       BRK         CALL        CALLA       CALLB       CALLD
CALLPA      CALLPB      CMP         CMPM        CMPR        CMPS
CMPSUB      CMPSX       CMPX        COGATN      COGBRK      COGID
COGINIT     COGSTOP     CRCBIT      CRCNIB      DECMOD      DECOD
DIRC        DIRH        DIRL        DIRNC       DIRNOT      DIRNZ
DIRRND      DIRZ        DJF         DJNF        DJNZ        DJZ
DRVC        DRVH        DRVL        DRVNC       DRVNOT      DRVNZ
DRVRND      DRVZ        ENCOD       EXECF       FBLOCK      FGE
FGES        FLE         FLES        FLTC        FLTH        FLTL
FLTNC       FLTNOT      FLTNZ       FLTRND      FLTZ        GETBRK
GETBYTE     GETCT       GETNIB      GETPTR      GETQX       GETQY
GETRND      GETSCP      GETWORD     GETXACC     HUBSET      IJNZ
IJZ         INCMOD      JATN        JCT1        JCT2        JCT3
JFBW        JINT        JMP         JMPREL      JNATN       JNCT1
JNCT2       JNCT3       JNFBW       JNINT       JNPAT       JNQMT
JNSE1       JNSE2       JNSE3       JNSE4       JNXFI       JNXMT
JNXRL       JNXRO       JPAT        JQMT        JSE1        JSE2
JSE3        JSE4        JXFI        JXMT        JXRL        JXRO
LOC         LOCKNEW     LOCKREL     LOCKRET     LOCKTRY     MERGEB
MERGEW      MIXPIX      MODC        MODCZ       MODZ        MOV
MOVBYTS     MUL         MULPIX      MULS        MUXC        MUXNC
MUXNIBS     MUXNITS     MUXNZ       MUXQ        MUXZ        NEG
NEGC        NEGNC       NEGNZ       NEGZ        NIXINT1     NIXINT2
NIXINT3     NOP         NOT         ONES        OR          OUTC
OUTH        OUTL        OUTNC       OUTNOT      OUTNZ       OUTRND
OUTZ        POLLATN     POLLCT1     POLLCT2     POLLCT3     POLLFBW
POLLINT     POLLPAT     POLLQMT     POLLSE1     POLLSE2     POLLSE3
POLLSE4     POLLXFI     POLLXMT     POLLXRL     POLLXRO     POP
POPA        POPB        PUSH        PUSHA       PUSHB       QDIV
QEXP        QFRAC       QLOG        QMUL        QROTATE     QSQRT
QVECTOR     RCL         RCR         RCZL        RCZR        RDBYTE
RDFAST      RDLONG      RDLUT       RDPIN       RDWORD      REP
RESI0       RESI1       RESI2       RESI3       RET         RETA
RETB        RETI0       RETI1       RETI2       RETI3       REV
RFBYTE      RFLONG      RFVAR       RFVARS      RFWORD      RGBEXP
RGBSQZ      ROL         ROLBYTE     ROLNIB      ROLWORD     ROR
RQPIN       SAL         SAR         SCA         SCAS        SETBYTE
SETCFRQ     SETCI       SETCMOD     SETCQ       SETCY       SETD
SETDACS     SETINT1     SETINT2     SETINT3     SETLUTS     SETNIB
SETPAT      SETPIV      SETPIX      SETQ        SETQ2       SETR
SETS        SETSCP      SETSE1      SETSE2      SETSE3      SETSE4
SETWORD     SETXFRQ     SEUSSF      SEUSSR      SHL         SHR
SIGNX       SKIP        SKIPF       SPLITB      SPLITW      STALLI
SUB         SUBR        SUBS        SUBSX       SUBX        SUMC
SUMNC       SUMNZ       SUMZ        TEST        TESTB       TESTBN
TESTN       TESTP       TESTPN      TJF         TJNF        TJNS
TJNZ        TJS         TJV         TJZ         TRGINT1     TRGINT2
TRGINT3     WAITATN     WAITCT1     WAITCT2     WAITCT3     WAITFBW
WAITINT     WAITPAT     WAITSE1     WAITSE2     WAITSE3     WAITSE4
WAITX       WAITXFI     WAITXMT     WAITXRL     WAITXRO     WFBYTE
WFLONG      WFWORD      WMLONG      WRBYTE      WRC         WRFAST
WRLONG      WRLUT       WRNC        WRNZ        WRPIN       WRWORD
WRZ         WXPIN       WYPIN       XCONT       XINIT       XOR
XORO32      XSTOP       XZERO       ZEROX
```



## Assembly Directives (14 words)

Directives control the assembly process and code organization:

- **ALIGNL** - Align to next long boundary (4-byte alignment)
- **ALIGNW** - Align to next word boundary (2-byte alignment)
- **BYTE** - Reserve/initialize byte-sized data
- **BYTEFIT** - Verify code fits in specified byte count
- **DEBUG** - Insert debug statements (Spin2 feature)
- **DITTO** - Repeat previous instruction encoding
- **FIT** - Verify code fits in COG memory
- **LONG** - Reserve/initialize long-sized data (32 bits)
- **ORG** - Set assembly origin (COG address)
- **ORGF** - Set assembly origin with fill
- **ORGH** - Set assembly origin (Hub address)
- **RES** - Reserve uninitialized registers/memory
- **WORD** - Reserve/initialize word-sized data (16 bits)
- **WORDFIT** - Verify code fits in specified word count



## Predefined Constants (11 words)

Built-in constants that can be used in assembly expressions:

### Basic Constants (5)

- **FALSE** - Boolean false value (`$00000000`, decimal 0)
- **NEGX** - Most negative signed 32-bit value (`$80000000`, decimal -2147483648)
- **PI** - Fixed-point pi value for CORDIC operations
- **POSX** - Most positive signed 32-bit value (`$7FFFFFFF`, decimal 2147483647)
- **TRUE** - Boolean true value (`$FFFFFFFF`, decimal -1)

### Execution Mode Constants (6)

Used with the COGINIT instruction to specify execution mode:

- **COGEXEC** - Execute from COG RAM (base mode, `%0_0_0000`)
- **COGEXEC_NEW** - Auto-select available COG, execute from COG RAM
- **COGEXEC_NEW_PAIR** - Auto-select COG pair, execute from COG RAM
- **HUBEXEC** - Execute from Hub RAM (base mode, `%0_1_0000`)
- **HUBEXEC_NEW** - Auto-select available COG, execute from Hub RAM
- **HUBEXEC_NEW_PAIR** - Auto-select COG pair, execute from Hub RAM

**Note:** The `_NEW` and `_NEW_PAIR` variants are bit patterns that modify the base `COGEXEC` and `HUBEXEC` constants for use with COGINIT's automatic COG selection feature.



## Special Register Names (16 words)

Special-purpose registers mapped to COG RAM addresses `$1F0-$1FF`:

### Dual-Purpose Registers ($1F0-$1F7)

Can be used as general RAM or special registers depending on enabled features:

- **IJMP3** - Interrupt 3 jump address ($1F0, 496)
- **IRET3** - Interrupt 3 return address ($1F1, 497)
- **IJMP2** - Interrupt 2 jump address ($1F2, 498)
- **IRET2** - Interrupt 2 return address ($1F3, 499)
- **IJMP1** - Interrupt 1 jump address ($1F4, 500)
- **IRET1** - Interrupt 1 return address ($1F5, 501)
- **PA** - Multi-purpose register A ($1F6, 502)
- **PB** - Multi-purpose register B ($1F7, 503)

### Fixed Special Registers ($1F8-$1FF)

Always provide special functions when accessed:

- **PTRA** - Pointer A to Hub RAM ($1F8, 504)
- **PTRB** - Pointer B to Hub RAM ($1F9, 505)
- **DIRA** - Direction register for pins 0-31 ($1FA, 506)
- **DIRB** - Direction register for pins 32-63 ($1FB, 507)
- **OUTA** - Output register for pins 0-31 ($1FC, 508)
- **OUTB** - Output register for pins 32-63 ($1FD, 509)
- **INA** - Input register for pins 0-31 ($1FE, 510)
- **INB** - Input register for pins 32-63 ($1FF, 511)



## Condition Keywords (41 words)

Conditional execution prefixes (IF_xxx) that can be applied to any instruction. These test the C (Carry) and Z (Zero) flags:

### Primary Condition Codes (16)

These are the canonical condition names:

- **IF_ALWAYS** - Always execute (default, can be omitted)
- **IF_NEVER** - Never execute (effectively a NOP)
- **IF_C** - Execute if C=1
- **IF_NC** - Execute if C=0
- **IF_Z** - Execute if Z=1
- **IF_NZ** - Execute if Z=0
- **IF_C_AND_Z** - Execute if C=1 AND Z=1
- **IF_C_AND_NZ** - Execute if C=1 AND Z=0
- **IF_NC_AND_Z** - Execute if C=0 AND Z=1
- **IF_NC_AND_NZ** - Execute if C=0 AND Z=0
- **IF_C_OR_Z** - Execute if C=1 OR Z=1
- **IF_C_OR_NZ** - Execute if C=1 OR Z=0
- **IF_NC_OR_Z** - Execute if C=0 OR Z=1
- **IF_NC_OR_NZ** - Execute if C=0 OR Z=0
- **IF_C_EQ_Z** - Execute if C equals Z
- **IF_C_NE_Z** - Execute if C not equal to Z

### Comparison Aliases (15)

Convenient aliases for post-comparison conditional execution:

**Unsigned comparison aliases:**
- **IF_A** - Above (same as IF_NC_AND_NZ)
- **IF_AE** - Above or equal (same as IF_NC)
- **IF_B** - Below (same as IF_C)
- **IF_BE** - Below or equal (same as IF_C_OR_Z or IF_NC_OR_Z)
- **IF_E** - Equal (same as IF_Z)
- **IF_NE** - Not equal (same as IF_NZ)

**Signed comparison aliases:**
- **IF_GE** - Greater or equal (same as IF_NC)
- **IF_GT** - Greater than (same as IF_NC_AND_NZ)
- **IF_LE** - Less or equal (same as IF_NC_OR_Z)
- **IF_LT** - Less than (same as IF_C)

**Other aliases:**
- **IF_DIFF** - Different (same as IF_C_NE_Z)
- **IF_SAME** - Same (same as IF_C_EQ_Z)
- **IF_NZ_AND_C** - Not zero and carry (same as IF_C_AND_NZ)
- **IF_NZ_AND_NC** - Not zero and no carry (same as IF_NC_AND_NZ)
- **IF_Z_AND_C** - Zero and carry (same as IF_C_AND_Z)

### Special Return Condition (1)

- **_RET_** - Always execute AND return (combines execution with return)

### Symmetric Alternatives (9)

Additional aliases that express the same conditions in reverse order:

- **IF_Z_AND_NC** - Same as IF_NC_AND_Z
- **IF_Z_OR_C** - Same as IF_C_OR_Z
- **IF_Z_OR_NC** - Same as IF_NC_OR_Z
- **IF_NZ_OR_C** - Same as IF_C_OR_NZ
- **IF_NZ_OR_NC** - Same as IF_NC_OR_NZ

**Note:** Many conditions have multiple valid names (aliases). For example, `IF_C`, `IF_B`, and `IF_LT` all represent the same condition code but provide semantic clarity depending on context.



## Effect Keywords (9 words)

Effect suffixes control flag updates after instruction execution:

### Basic Effect Modifiers (3)

- **WC** - Write result to Carry flag
- **WZ** - Write result to Zero flag
- **WCZ** - Write result to both Carry and Zero flags

### Logical Effect Modifiers (6)

Combine instruction result with existing flag using logic operation:

- **ANDC** - AND result with C flag
- **ANDZ** - AND result with Z flag
- **ORC** - OR result with C flag
- **ORZ** - OR result with Z flag
- **XORC** - XOR result with C flag
- **XORZ** - XOR result with Z flag

**Usage:** Effect keywords appear after the instruction's operands:

```pasm
ADD   x, y  WC      ' Update C flag with carry
CMP   a, b  WCZ     ' Update both C and Z flags
TEST  val, mask  ANDZ   ' AND test result with Z flag
```



## Avoiding Reserved Words

When naming labels, variables, and symbols in your PASM2 code:

1. **Check this reference** before choosing identifiers
2. **Use descriptive names** that clearly differ from reserved words
3. **Add prefixes/suffixes** to avoid conflicts (e.g., `my_add`, `loop_counter`)
4. **Case sensitivity:** PASM2 is case-insensitive - `MOV`, `mov`, and `Mov` are all reserved

### Common Naming Strategies

- Add application-specific prefixes: `uart_receive`, `led_toggle`
- Add type suffixes: `count_value`, `delay_ms`
- Use underscores: `_start`, `main_loop`, `temp_reg`
- Combine words: `blink_rate`, `max_count`

### Example Conflicts to Avoid

```pasm
' WRONG - uses reserved words as labels
add:    mov   x, #1      ' Error: 'add' is instruction
or:     jmp   #loop      ' Error: 'or' is instruction
byte:   long  $0         ' Error: 'byte' is directive

' CORRECT - uses valid label names
add_routine:  mov   x, #1
choice_or:    jmp   #loop
byte_data:    long  $0
```



## Summary

PASM2 reserves **449 identifiers** across six categories:

| Category | Count | Purpose |
|----------|-------|---------|
| Instructions | 358 | All instruction mnemonics |
| Directives | 14 | Assembly-time directives |
| Constants | 11 | Predefined constant values |
| Special Registers | 16 | Hardware-mapped registers |
| Conditions | 41 | Conditional execution prefixes |
| Effects | 9 | Flag modification suffixes |
| **Total** | **449** | |

**Cross-References:**

- **Part II** — Complete documentation of instructions, directives, constants, and special registers
- **Chapter 3** — Detailed explanation of condition codes and effect modifiers
- **Appendix E** — Smart Pin mode constants (P_* symbols, approximately 116 constants)
- **Appendix F** — Streamer mode constants (X_* symbols, approximately 78 constants)

**Note on P_* and X_* Constants:** The Smart Pin configuration constants (P_*) and Streamer mode constants (X_*) are predefined symbols that function as reserved words when programming the P2's Smart Pins and Streamer hardware. These are documented in their own appendices due to their specialized nature and extensive count. While not included in the 449-word count above, they are effectively reserved and cannot be used as user-defined symbols.

**Note on Spin2 Reserved Words:** This appendix covers PASM2-specific reserved words. The Spin2 language includes additional reserved words for its high-level constructs (CASE, CON, DAT, IF, PUB, VAR, etc.), DEBUG command parameters (UBIN, UDEC, UHEX variants), and graphics constants (BLACK, WHITE, YELLOW, etc.). When writing inline PASM2 within Spin2 code, both sets of reserved words apply. Pure PASM2 files need only consider the words listed in this appendix plus the P_* and X_* constants.
