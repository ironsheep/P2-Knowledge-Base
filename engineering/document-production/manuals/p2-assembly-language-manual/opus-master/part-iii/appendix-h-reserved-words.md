# Appendix H: Reserved Words Reference

This appendix lists all reserved words recognized by the Propeller 2 compiler. These identifiers cannot be used as user-defined labels, symbols, or variable names. Attempting to use a reserved word as a label will result in an assembly error.

**Important:** Since Spin2 and PASM2 share a single compiler, **all reserved words from both languages apply** regardless of whether you are writing pure PASM2 or mixed Spin2/PASM2 code.

**Total Reserved Words: 1,042+** (456 PASM2 + 586 Spin2; P_*/X_* hardware constants add ~194 more — see Grand Total below)

## Quick Reference Index

Use this alphabetical index to quickly check if a name is reserved. For detailed descriptions and usage context, see the categorized sections that follow.

**Note:** P_* constants (Smart Pin, ~116 words) are listed in Appendix E. X_* constants (Streamer, ~78 words) are listed in Appendix F. Both prefixes are reserved.

### A
```
ABS         ABORT       ADDBITS     ADD         ADDCT1      ADDCT2
ADDCT3      ADDPIX      ADDPINS     ADDS        ADDSX       ADDX
AKPIN       ALIGNL      ALIGNW      ALLOWI      ALT         ALTB
ALTD        ALTGB       ALTGN       ALTGW       ALTI        ALTR
ALTS        ALTSB       ALTSN       ALTSW       AND         ANDC
ANDN        ANDZ        ARCHIVE     ASMCLK      AUGD        AUGS
```

### B
```
BACKCOLOR   BITMAP      BITC        BITH        BITL        BITNC
BITNOT      BITNZ       BITRND      BITZ        BLACK       BLNPIX
BLUE        BMASK       BOX         BRK         BYTE        BYTEFILL
BYTEFIT     BYTEMOVE    BYTES_1BIT  BYTES_2BIT  BYTES_4BIT
```

### C
```
CALL        CALLA       CALLB       CALLD       CALLPA      CALLPB
CARTESIAN   CASE        CASE_FAST   CHANNEL     CIRCLE      CLEAR
CLKFREQ     CLKMODE     CLKSET      CLOSE       CMP         CMPM
CMPR        CMPS        CMPSUB      CMPSX       CMPX        COGBRK
COGCHK      COGEXEC     COGEXEC_NEW COGEXEC_NEW_PAIR        COGATN
COGID       COGINIT     COGSPIN     COGSTOP     COLOR       CON
CRCBIT      CRCNIB      CYAN
```

### D
```
DAT         DEBUG       DEBUG_BAUD  DEBUG_COGS  DEBUG_COGINIT           DEBUG_DELAY
DEBUG_DISABLE           DEBUG_DISPLAY_LEFT      DEBUG_DISPLAY_TOP       DEBUG_HEIGHT
DEBUG_LEFT  DEBUG_LOG_SIZE          DEBUG_MAIN  DEBUG_MASK  DEBUG_PIN   DEBUG_PIN_RX
DEBUG_PIN_TX            DEBUG_TIMESTAMP         DEBUG_TOP   DEBUG_WIDTH DEBUG_WINDOWS_OFF
DECMOD      DECOD       DEPTH       DIRA        DIRB        DIRC
DIRH        DIRL        DIRNC       DIRNOT      DIRNZ
DIRRND      DIRZ        DITTO       DJF         DJNF        DJNZ
DJZ         DLY         DOT         DOTSIZE     DRVC        DRVH
DRVL        DRVNC       DRVNOT      DRVNZ       DRVRND      DRVZ
```

### E
```
ELSE        ELSEIF      ELSEIFNOT   ENCOD       END         EVENT_ATN
EVENT_CT1   EVENT_CT2   EVENT_CT3   EVENT_FBW   EVENT_INT   EVENT_PAT
EVENT_QMT   EVENT_SE1   EVENT_SE2   EVENT_SE3   EVENT_SE4   EVENT_XFI
EVENT_XMT   EVENT_XRL   EVENT_XRO   EXECF
```

### F
```
FABS        FALSE       FBLOCK      FDEC        FDEC_       FDEC_ARRAY
FDEC_ARRAY_ FDEC_REG_ARRAY          FDEC_REG_ARRAY_         FFT
FGE         FGES        FILE        FIT         FLE         FLES
FLOAT       FLTC        FLTH        FLTL        FLTNC       FLTNOT
FLTNZ       FLTRND      FLTZ        FRAC        FROM        FSQRT
FVAR        FVARS
```

### G
```
GETBRK      GETBYTE     GETCRC      GETCT       GETMS       GETNIB
GETPTR      GETQX       GETQY       GETREGS     GETRND      GETSCP
GETSEC      GETWORD     GETXACC     GREEN       GREY
```

### H
```
HIDEXY      HOLDOFF     HSV8        HSV8W       HSV8X       HSV16
HSV16W      HSV16X      HUBEXEC     HUBEXEC_NEW HUBEXEC_NEW_PAIR
HUBSET
```

### I
```
IF          IF_00       IF_0000     IF_0001     IF_0010     IF_0011
IF_01       IF_0100     IF_0101     IF_0110     IF_0111     IF_0X
IF_10       IF_1000     IF_1001     IF_1010     IF_1011     IF_11
IF_1100     IF_1101     IF_1110     IF_1111     IF_1X       IF_A
IF_AE       IF_ALWAYS   IF_B        IF_BE       IF_C        IF_C_AND_NZ
IF_C_AND_Z  IF_C_EQ_Z   IF_C_NE_Z   IF_C_OR_NZ  IF_C_OR_Z   IF_DIFF
IF_E        IF_GE       IF_GT       IF_LE       IF_LT       IF_NC
IF_NC_AND_NZ            IF_NC_AND_Z IF_NC_OR_NZ IF_NC_OR_Z  IF_NE
IF_NOT_00   IF_NOT_01   IF_NOT_10   IF_NOT_11   IF_NZ
IF_NZ_AND_C IF_NZ_AND_NC            IF_NZ_OR_C  IF_NZ_OR_NC IF_SAME
IF_X0       IF_X1       IF_Z        IF_Z_AND_C  IF_Z_AND_NC IF_Z_EQ_C
IF_Z_NE_C   IF_Z_OR_C   IF_Z_OR_NC  IFNOT       IJMP1       IJMP2
IJMP3       IJNZ        IJZ         INA         INB         INCMOD
INT_OFF     IRET1       IRET2       IRET3
```

### J
```
JATN        JCT1        JCT2        JCT3        JFBW        JINT
JMP         JMPREL      JNATN       JNCT1       JNCT2       JNCT3
JNFBW       JNINT       JNPAT       JNQMT       JNSE1       JNSE2
JNSE3       JNSE4       JNXFI       JNXMT       JNXRL       JNXRO
JPAT        JQMT        JSE1        JSE2        JSE3        JSE4
JXFI        JXMT        JXRL        JXRO
```

### L
```
LINE        LINESIZE    LOC         LOCKCHK     LOCKNEW     LOCKREL
LOCKRET     LOCKTRY     LOGIC       LONG        LONGFILL    LONGMOVE
LONGS_16BIT LONGS_1BIT  LONGS_2BIT  LONGS_4BIT  LONGS_8BIT
LOOKDOWN    LOOKDOWNZ   LOOKUP      LOOKUPZ     LSTR        LSTR_
LUMA8       LUMA8W      LUMA8X      LUT1        LUT2        LUT4
LUT8        LUTCOLORS
```

### M
```
MAG         MAGENTA     MERGEB      MERGEW      MIDI        MIXPIX
MODC        MODCZ       MODZ        MOV         MOVBYTS     MUL
MULDIV64    MULPIX      MULS        MUXC        MUXNC       MUXNIBS
MUXNITS     MUXNZ       MUXQ        MUXZ
```

### N
```
NAN         NEG         NEGC        NEGNC       NEGNZ       NEGX
NEGZ        NEWCOG      NEXT        NIXINT1     NIXINT2     NIXINT3
NOP         NOT
```

### O
```
OBJ         OBOX        ONES        OPACITY     OR          ORANGE
ORC         ORG         ORGF        ORGH        ORIGIN      ORZ
OTHER       OUTA        OUTB        OUTC        OUTH        OUTL
OUTNC       OUTNOT      OUTNZ       OUTRND      OUTZ        OVAL
```

### P
```
PA          PB          PC_KEY      PC_MOUSE    PI          PINCLEAR
PINF        PINFLOAT    PINH        PINHIGH     PINL        PINLOW
PINR        PINREAD     PINSTART    PINT        PINTOGGLE   PINW
PINWRITE    PLOT        POLAR       POLLATN     POLLCT      POLLCT1
POLLCT2     POLLCT3     POLLFBW     POLLINT     POLLPAT     POLLQMT
POLLSE1     POLLSE2     POLLSE3     POLLSE4     POLLXFI     POLLXMT
POLLXRL     POLLXRO     POLXY       POP         POPA        POPB
POS         POSX        PR0         PR1         PR2         PR3
PR4         PR5         PR6         PR7         PRECISE     PRECOMPILE
PRI         PTRA        PTRB        PUB         PUSH        PUSHA
PUSHB
```

### Q
```
QCOS        QDIV        QEXP        QFRAC       QLOG        QMUL
QROTATE     QSIN        QSQRT       QUIT        QVECTOR
```

### R
```
RANGE       RCL         RCR         RCZL        RCZR        RDBYTE
RDFAST      RDLONG      RDLUT       RDPIN       RDWORD      RECV
RED         REG         REGEXEC     REGLOAD     REP         REPEAT
RES         RESI0       RESI1       RESI2       RESI3       RET
RETA        RETB        RETI0       RETI1       RETI2       RETI3
RETURN      REV         RFBYTE      RFLONG      RFVAR       RFVARS
RFWORD      RGB8        RGB16       RGB24       RGBEXP      RGBI8
RGBI8W      RGBI8X      RGBSQZ      ROL         ROLBYTE     ROLNIB
ROLWORD     ROR         ROTXY       ROUND       RQPIN
```

### S
```
SAL         SAMPLES     SAR         SAVE        SBIN        SBIN_
SBIN_BYTE   SBIN_BYTE_  SBIN_BYTE_ARRAY         SBIN_BYTE_ARRAY_
SBIN_LONG   SBIN_LONG_  SBIN_LONG_ARRAY         SBIN_LONG_ARRAY_
SBIN_REG_ARRAY          SBIN_REG_ARRAY_         SBIN_WORD   SBIN_WORD_
SBIN_WORD_ARRAY         SBIN_WORD_ARRAY_        SCA         SCAS
SCOPE       SCOPE_XY    SCROLL      SDEC        SDEC_       SDEC_BYTE
SDEC_BYTE_  SDEC_BYTE_ARRAY         SDEC_BYTE_ARRAY_        SDEC_LONG
SDEC_LONG_  SDEC_LONG_ARRAY         SDEC_LONG_ARRAY_        SDEC_REG_ARRAY
SDEC_REG_ARRAY_         SDEC_WORD   SDEC_WORD_  SDEC_WORD_ARRAY
SDEC_WORD_ARRAY_        SEND        SET         SETBYTE     SETCFRQ
SETCI       SETCMOD     SETCQ       SETCY       SETD        SETDACS
SETINT1     SETINT2     SETINT3     SETLUTS     SETNIB      SETPAT
SETPIV      SETPIX      SETQ        SETQ2       SETR        SETREGS
SETS        SETSCP      SETSE1      SETSE2      SETSE3      SETSE4
SETWORD     SETXFRQ     SEUSSF      SEUSSR      SHEX        SHEX_
SHEX_BYTE   SHEX_BYTE_  SHEX_BYTE_ARRAY         SHEX_BYTE_ARRAY_
SHEX_LONG   SHEX_LONG_  SHEX_LONG_ARRAY         SHEX_LONG_ARRAY_
SHEX_REG_ARRAY          SHEX_REG_ARRAY_         SHEX_WORD   SHEX_WORD_
SHEX_WORD_ARRAY         SHEX_WORD_ARRAY_        SHL         SHR
SIGNED      SIGNX       SIZE        SKIP        SKIPF       SPACING
SPECTRO     SPLITB      SPLITW      SPRITE      SPRITEDEF   SQRT
STALLI      STEP        STRCOMP     STRCOPY     STRING      STRSIZE
STRUCT      SUB         SUBR        SUBS        SUBSX       SUBX
SUMC        SUMNC       SUMNZ       SUMZ
```

### T
```
TERM        TEST        TESTB       TESTBN      TESTN       TESTP
TESTPN      TEXT        TEXTANGLE   TEXTSIZE    TEXTSTYLE   TITLE
TJF         TJNF        TJNS        TJNZ        TJS         TJV
TJZ         TO          TRACE       TRGINT1     TRGINT2     TRGINT3
TRIGGER     TRUE        TRUNC
```

### U
```
UBIN        UBIN_       UBIN_BYTE   UBIN_BYTE_  UBIN_BYTE_ARRAY
UBIN_BYTE_ARRAY_        UBIN_LONG   UBIN_LONG_  UBIN_LONG_ARRAY
UBIN_LONG_ARRAY_        UBIN_REG_ARRAY          UBIN_REG_ARRAY_
UBIN_WORD   UBIN_WORD_  UBIN_WORD_ARRAY         UBIN_WORD_ARRAY_
UDEC        UDEC_       UDEC_BYTE   UDEC_BYTE_  UDEC_BYTE_ARRAY
UDEC_BYTE_ARRAY_        UDEC_LONG   UDEC_LONG_  UDEC_LONG_ARRAY
UDEC_LONG_ARRAY_        UDEC_REG_ARRAY          UDEC_REG_ARRAY_
UDEC_WORD   UDEC_WORD_  UDEC_WORD_ARRAY         UDEC_WORD_ARRAY_
UHEX        UHEX_       UHEX_BYTE   UHEX_BYTE_  UHEX_BYTE_ARRAY
UHEX_BYTE_ARRAY_        UHEX_LONG   UHEX_LONG_  UHEX_LONG_ARRAY
UHEX_LONG_ARRAY_        UHEX_REG_ARRAY          UHEX_REG_ARRAY_
UHEX_WORD   UHEX_WORD_  UHEX_WORD_ARRAY         UHEX_WORD_ARRAY_
UNTIL       UPDATE
```

### V-W
```
VAR         VARBASE     WAITATN     WAITCT      WAITCT1     WAITCT2
WAITCT3     WAITFBW     WAITINT     WAITMS      WAITPAT     WAITSE1
WAITSE2     WAITSE3     WAITSE4     WAITUS      WAITX       WAITXFI
WAITXMT     WAITXRL     WAITXRO     WC          WCZ         WFBYTE
WFLONG      WFWORD      WHITE       WHILE       WINDOW      WITH
WMLONG      WORD        WORDFILL    WORDFIT     WORDMOVE    WORDS_1BIT
WORDS_2BIT  WORDS_4BIT  WORDS_8BIT  WRBYTE      WRC         WRFAST
WRLONG      WRLUT       WRNC        WRNZ        WRPIN       WRWORD
WRZ         WXPIN       WYPIN       WZ
```

### X-Z
```
XCONT       XINIT       XOR         XORC        XORO32      XORZ
XSTOP       XYPOL       XZERO       YELLOW      ZEROX       ZSTR
ZSTR_
```

### Underscore-Prefixed Conditions
```
_C          _CLR        _C_AND_NZ   _C_AND_Z    _C_EQ_Z     _C_NE_Z
_C_OR_NZ    _C_OR_Z     _E          _GE         _GT         _LE
_LT         _NC         _NC_AND_NZ  _NC_AND_Z   _NC_OR_NZ   _NC_OR_Z
_NE         _NZ         _NZ_AND_C   _NZ_AND_NC  _NZ_OR_C    _NZ_OR_NC
_RET_       _SET        _Z          _Z_AND_C    _Z_AND_NC   _Z_EQ_C
_Z_NE_C     _Z_OR_C     _Z_OR_NC
```

---

## Categories

Reserved words fall into six main categories:

1. **Instruction Mnemonics** (358 words) - All instruction names
2. **Assembly Directives** (21 words) - Block identifiers and assembly-time directives
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



## Assembly Directives (21 words)

Directives control the assembly process and code organization:

### Block/Section Identifiers (7)

These keywords define the major sections of a Spin2/PASM2 source file:

- **CON** - Constants block (define named constants)
- **DAT** - Data block (contains PASM2 code and data)
- **FILE** - Include binary file in DAT section
- **OBJ** - Objects block (instantiate child objects)
- **PRI** - Private method block
- **PUB** - Public method block
- **VAR** - Variables block (instance variables)

### Assembly-Time Directives (14)

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

- **IF_ALWAYS** - Always execute (EEEE=1111; this is the encoding used when no condition is specified)
- **_RET_** - Execute instruction, then return if no branch (EEEE=0000; note: P1's IF_NEVER does NOT exist in P2)
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

Convenient aliases for post-comparison conditional execution. Two equivalent terminology styles are available—both encode to identical condition codes:

**Magnitude terminology aliases:**

- **IF_A** - Above (same as IF_NC_AND_NZ)
- **IF_AE** - Above or equal (same as IF_NC)
- **IF_B** - Below (same as IF_C)
- **IF_BE** - Below or equal (same as IF_C_OR_Z)
- **IF_E** - Equal (same as IF_Z)
- **IF_NE** - Not equal (same as IF_NZ)

**Arithmetic terminology aliases:**

- **IF_GE** - Greater or equal (same as IF_NC)
- **IF_GT** - Greater than (same as IF_NC_AND_NZ)
- **IF_LE** - Less or equal (same as IF_C_OR_Z)
- **IF_LT** - Less than (same as IF_C)

**Other aliases:**

- **IF_DIFF** - Different (same as IF_C_NE_Z)
- **IF_SAME** - Same (same as IF_C_EQ_Z)
- **IF_NZ_AND_C** - Not zero and carry (same as IF_C_AND_NZ)
- **IF_NZ_AND_NC** - Not zero and no carry (same as IF_NC_AND_NZ)
- **IF_Z_AND_C** - Zero and carry (same as IF_C_AND_Z)

### Special Return Condition (1)

- **_RET_** - Always execute instruction, then return if no branch (no flag restore)

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

```pasm2
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

::: antipattern

```pasm2
' WRONG - uses reserved words as labels
add         mov   x, #1      ' Error: 'add' is instruction
or          jmp   #loop      ' Error: 'or' is instruction
byte        long  $0         ' Error: 'byte' is directive
```

:::

```pasm2
' CORRECT - uses valid label names
add_routine     mov   x, #1
choice_or       jmp   #loop
byte_data       long  $0
```



## Summary

The Propeller 2 compiler reserves **1,042+ identifiers** across PASM2 and Spin2:

**PASM2-Specific Reserved Words (456):**

| Category | Count | Purpose |
|----------|-------|---------|
| Instructions | 358 | All instruction mnemonics |
| Directives | 21 | Block identifiers and assembly-time directives |
| Constants | 11 | Predefined constant values |
| Special Registers | 16 | Hardware-mapped registers |
| Conditions | 41 | Conditional execution prefixes |
| Effects | 9 | Flag modification suffixes |
| **PASM2 Subtotal** | **456** | |

**Spin2-Specific Reserved Words (586):**

| Category | Count | Purpose |
|----------|-------|---------|
| Language Keywords | 20 | Core Spin2 constructs |
| DEBUG Parameters | 120 | Debug output formatting |
| Graphics/Color | 34 | Color names and display |
| String/Data Methods | 22 | Memory/string manipulation |
| Math/Conversion | 11 | Math functions |
| Event Constants | 16 | Event source identifiers |
| Pin Methods | 14 | High-level pin control |
| Condition Shortcuts | 32 | Underscore-prefixed conditions |
| IF_ Variants | 28 | Extended condition patterns |
| Shared Registers | 8 | PR0-PR7 communication |
| System/I/O | 27 | System control methods |
| Graphics Drawing | 32 | Graphics primitives |
| Text/Display | 12 | Text rendering |
| Lookup/Misc | 20 | Table lookup and other |
| **Spin2 Subtotal** | **586** | |

**Hardware Constants (194+):**

| Category | Count | Purpose |
|----------|-------|---------|
| Smart Pin (P_*) | ~116 | Pin configuration |
| Streamer (X_*) | ~78 | Streamer modes |
| **Constants Subtotal** | **~194** | |

**Grand Total: 1,236+ reserved identifiers**

**Cross-References:**

- **Part II** — Complete documentation of instructions, directives, constants, and special registers
- **Chapter 3** — Detailed explanation of condition codes and effect modifiers
- **Appendix E** — Smart Pin mode constants (P_* symbols, approximately 116 constants)
- **Appendix F** — Streamer mode constants (X_* symbols, approximately 78 constants)

**Note on P_* and X_* Constants:** The Smart Pin configuration constants (P_*) and Streamer mode constants (X_*) are predefined symbols that function as reserved words when programming the P2's Smart Pins and Streamer hardware. These are documented in their own appendices due to their specialized nature and extensive count. While not included in the 456-word count above, they are effectively reserved and cannot be used as user-defined symbols.


## Spin2 Reserved Words

Since the Propeller 2 uses a single compiler for both Spin2 and PASM2, **all Spin2 reserved words are also reserved in PASM2**. You cannot use any of these identifiers as labels, symbols, or variable names in your assembly code, even when writing pure PASM2.

**Total Spin2-Only Reserved Words: 586**

The following sections list Spin2 reserved words organized by category.



### Language Keywords (20 words)

Core Spin2 language constructs (block names CON, DAT, VAR, PUB, PRI, OBJ are listed under PASM2 Assembly Directives):

```
ABORT       CASE        CASE_FAST   ELSE        ELSEIF      ELSEIFNOT
END         FROM        IF          IFNOT       NEXT        OTHER
QUIT        REPEAT      RETURN      STRUCT      TO          UNTIL
WHILE       WITH
```

**Note:** STRUCT requires Spin2 v45 or later; WITH is the REPEAT positive-count loop-counter binding (`REPEAT <count> WITH <var>`).



### DEBUG Command Parameters (120 words)

Debug output formatting commands and their variants:

**Configuration Symbols:**
```
DEBUG_BAUD           DEBUG_COGS           DEBUG_COGINIT        DEBUG_DELAY
DEBUG_DISABLE        DEBUG_DISPLAY_LEFT   DEBUG_DISPLAY_TOP    DEBUG_HEIGHT
DEBUG_LEFT           DEBUG_LOG_SIZE       DEBUG_MAIN           DEBUG_MASK
DEBUG_PIN            DEBUG_PIN_RX         DEBUG_PIN_TX         DEBUG_TIMESTAMP
DEBUG_TOP            DEBUG_WIDTH          DEBUG_WINDOWS_OFF
```

**Signed decimal (SDEC) variants:**
```
SDEC        SDEC_       SDEC_BYTE        SDEC_BYTE_       SDEC_BYTE_ARRAY
SDEC_BYTE_ARRAY_      SDEC_LONG        SDEC_LONG_       SDEC_LONG_ARRAY
SDEC_LONG_ARRAY_      SDEC_REG_ARRAY   SDEC_REG_ARRAY_  SDEC_WORD
SDEC_WORD_            SDEC_WORD_ARRAY  SDEC_WORD_ARRAY_
```

**Unsigned decimal (UDEC) variants:**
```
UDEC        UDEC_       UDEC_BYTE        UDEC_BYTE_       UDEC_BYTE_ARRAY
UDEC_BYTE_ARRAY_      UDEC_LONG        UDEC_LONG_       UDEC_LONG_ARRAY
UDEC_LONG_ARRAY_      UDEC_REG_ARRAY   UDEC_REG_ARRAY_  UDEC_WORD
UDEC_WORD_            UDEC_WORD_ARRAY  UDEC_WORD_ARRAY_
```

**Signed hex (SHEX) variants:**
```
SHEX        SHEX_       SHEX_BYTE        SHEX_BYTE_       SHEX_BYTE_ARRAY
SHEX_BYTE_ARRAY_      SHEX_LONG        SHEX_LONG_       SHEX_LONG_ARRAY
SHEX_LONG_ARRAY_      SHEX_REG_ARRAY   SHEX_REG_ARRAY_  SHEX_WORD
SHEX_WORD_            SHEX_WORD_ARRAY  SHEX_WORD_ARRAY_
```

**Unsigned hex (UHEX) variants:**
```
UHEX        UHEX_       UHEX_BYTE        UHEX_BYTE_       UHEX_BYTE_ARRAY
UHEX_BYTE_ARRAY_      UHEX_LONG        UHEX_LONG_       UHEX_LONG_ARRAY
UHEX_LONG_ARRAY_      UHEX_REG_ARRAY   UHEX_REG_ARRAY_  UHEX_WORD
UHEX_WORD_            UHEX_WORD_ARRAY  UHEX_WORD_ARRAY_
```

**Signed binary (SBIN) variants:**
```
SBIN        SBIN_       SBIN_BYTE        SBIN_BYTE_       SBIN_BYTE_ARRAY
SBIN_BYTE_ARRAY_      SBIN_LONG        SBIN_LONG_       SBIN_LONG_ARRAY
SBIN_LONG_ARRAY_      SBIN_REG_ARRAY   SBIN_REG_ARRAY_  SBIN_WORD
SBIN_WORD_            SBIN_WORD_ARRAY  SBIN_WORD_ARRAY_
```

**Unsigned binary (UBIN) variants:**
```
UBIN        UBIN_       UBIN_BYTE        UBIN_BYTE_       UBIN_BYTE_ARRAY
UBIN_BYTE_ARRAY_      UBIN_LONG        UBIN_LONG_       UBIN_LONG_ARRAY
UBIN_LONG_ARRAY_      UBIN_REG_ARRAY   UBIN_REG_ARRAY_  UBIN_WORD
UBIN_WORD_            UBIN_WORD_ARRAY  UBIN_WORD_ARRAY_
```

**Floating-point decimal (FDEC) variants:**
```
FDEC        FDEC_       FDEC_ARRAY       FDEC_ARRAY_      FDEC_REG_ARRAY
FDEC_REG_ARRAY_
```



### Graphics and Color Constants (34 words)

Color names and graphics-related constants:

```
BACKCOLOR   BLACK       BLUE        COLOR       CYAN        DEPTH
GREEN       GREY        MAGENTA     OPACITY     ORANGE      RED
WHITE       YELLOW
```

**HSV color conversion:**
```
HSV8        HSV8W       HSV8X       HSV16       HSV16W      HSV16X
```

**RGB color formats:**
```
RGB8        RGB16       RGB24       RGBI8       RGBI8W      RGBI8X
```

**Luminance and LUT:**
```
LUMA8       LUMA8W      LUMA8X      LUT1        LUT2        LUT4
LUT8        LUTCOLORS
```



### String and Data Methods (22 words)

Memory and string manipulation:

```
BYTEFILL    BYTEMOVE    LONGFILL    LONGMOVE    STRCOMP     STRCOPY
STRING      STRSIZE     WORDFILL    WORDMOVE
```

**Bit-packing constants:**
```
BYTES_1BIT  BYTES_2BIT  BYTES_4BIT
WORDS_1BIT  WORDS_2BIT  WORDS_4BIT  WORDS_8BIT
LONGS_1BIT  LONGS_2BIT  LONGS_4BIT  LONGS_8BIT  LONGS_16BIT
```



### Math and Conversion Methods (11 words)

Mathematical functions available in Spin2:

```
FABS        FLOAT       FRAC        FSQRT       MULDIV64    NAN
QCOS        QSIN        ROUND       SQRT        TRUNC
```



### Event Constants (16 words)

Event source identifiers for WAITSE and POLLSE:

```
EVENT_ATN   EVENT_CT1   EVENT_CT2   EVENT_CT3   EVENT_FBW   EVENT_INT
EVENT_PAT   EVENT_QMT   EVENT_SE1   EVENT_SE2   EVENT_SE3   EVENT_SE4
EVENT_XFI   EVENT_XMT   EVENT_XRL   EVENT_XRO
```



### Pin Methods (14 words)

High-level pin manipulation methods:

```
PINCLEAR    PINF        PINFLOAT    PINH        PINHIGH     PINL
PINLOW      PINR        PINREAD     PINSTART    PINT        PINTOGGLE
PINW        PINWRITE
```



### Condition Code Shortcuts (32 words)

Spin2 uses underscore-prefixed condition codes as shortcuts:

```
_C          _CLR        _E          _GE         _GT         _LE
_LT         _NC         _NE         _NZ         _SET        _Z
```

**Compound conditions:**
```
_C_AND_NZ   _C_AND_Z    _C_EQ_Z     _C_NE_Z     _C_OR_NZ    _C_OR_Z
_NC_AND_NZ  _NC_AND_Z   _NC_OR_NZ   _NC_OR_Z    _NZ_AND_C   _NZ_AND_NC
_NZ_OR_C    _NZ_OR_NC   _Z_AND_C    _Z_AND_NC   _Z_EQ_C     _Z_NE_C
_Z_OR_C     _Z_OR_NC
```

**MODCZ Operand Values:**

These mnemonics are used with the MODCZ instruction to modify C and Z flags. Each mnemonic represents a 4-bit value that selects the flag modification logic:

| Value | Binary | Mnemonic | Description |
|-------|--------|----------|-------------|
| 0 | 0000 | _CLR | Always clear (result = 0) |
| 1 | 0001 | _NC_AND_NZ | C=0 AND Z=0 |
| 2 | 0010 | _NC_AND_Z | C=0 AND Z=1 |
| 3 | 0011 | _NC | Copy inverse of C (not C) |
| 4 | 0100 | _C_AND_NZ | C=1 AND Z=0 |
| 5 | 0101 | _NZ | Copy inverse of Z (not Z) |
| 6 | 0110 | _C_NE_Z | C XOR Z (C not equal to Z) |
| 7 | 0111 | _NC_OR_NZ | C=0 OR Z=0 (NAND) |
| 8 | 1000 | _C_AND_Z | C=1 AND Z=1 (AND) |
| 9 | 1001 | _C_EQ_Z | NOT(C XOR Z) (C equals Z) |
| 10 | 1010 | _Z | Copy Z |
| 11 | 1011 | _NC_OR_Z | C=0 OR Z=1 |
| 12 | 1100 | _C | Copy C |
| 13 | 1101 | _C_OR_NZ | C=1 OR Z=0 |
| 14 | 1110 | _C_OR_Z | C=1 OR Z=1 (OR) |
| 15 | 1111 | _SET | Always set (result = 1) |

**Common MODCZ Usage:**
```pasm2
        MODCZ   _CLR, _SET      ' Clear C, set Z
        MODCZ   _SET, _CLR      ' Set C, clear Z
        MODCZ   _C, _Z          ' C and Z unchanged (copy to themselves)
        MODCZ   _Z, _C          ' Swap C and Z values
        MODCZ   _NC, _NZ        ' Invert both flags
```

**Cross-Reference:** See Part II MODCZ instruction for complete behavior description.



### Additional IF_ Condition Variants (28 words)

Extended condition code patterns for bit-testing:

```
IF          IF_00       IF_0000     IF_0001     IF_0010     IF_0011
IF_01       IF_0100     IF_0101     IF_0110     IF_0111     IF_0X
IF_10       IF_1000     IF_1001     IF_1010     IF_1011     IF_11
IF_1100     IF_1101     IF_1110     IF_1111     IF_1X       IF_NOT_00
IF_NOT_01   IF_NOT_10   IF_NOT_11   IF_X0       IF_X1       IF_Z_EQ_C
IF_Z_NE_C   IFNOT
```



### Shared Registers (8 words)

PASM2 to Spin2 communication registers:

```
PR0         PR1         PR2         PR3         PR4         PR5
PR6         PR7
```



### System and I/O Methods (27 words)

System control and I/O operations (FILE is listed under PASM2 Assembly Directives):

```
CLKFREQ     CLKMODE     CLKSET      CLOSE       COGCHK      COGSPIN
GETCRC      GETMS       GETREGS     GETSEC      INT_OFF     LOCKCHK
NEWCOG      RECV        REG         REGEXEC     REGLOAD     SEND
SETREGS     UPDATE      VARBASE     WAITCT      WAITMS      WAITUS
WINDOW
```



### Graphics Drawing Methods (32 words)

Graphics primitives and display control:

```
BITMAP      BOX         CARTESIAN   CIRCLE      CLEAR       DOT
DOTSIZE     FFT         HIDEXY      HOLDOFF     LINE        LINESIZE
LOGIC       OBOX        ORIGIN      OVAL        PC_KEY      PC_MOUSE
PLOT        POLAR       POLLCT      POLXY       POS         RANGE
ROTXY       SAMPLES     SAVE        SCOPE       SCOPE_XY    SCROLL
SPECTRO     XYPOL
```



### Text and Display (12 words)

Text rendering parameters:

```
SPACING     SPRITE      SPRITEDEF   TERM        TEXT        TEXTANGLE
TEXTSIZE    TEXTSTYLE   TITLE       TRACE       TRIGGER     ZSTR
ZSTR_
```



### Lookup and Miscellaneous (20 words)

Table lookup and other Spin2 features:

```
ADDBITS     ADDPINS     ALT         ARCHIVE     CHANNEL     DLY
FVAR        FVARS       LOOKDOWN    LOOKDOWNZ   LOOKUP      LOOKUPZ
LSTR        LSTR_       MAG         MIDI        PRECISE     PRECOMPILE
SET         SIGNED      SIZE        SQRT        STEP
```



### Smart Pin Constants (P_*)

The complete list of Smart Pin configuration constants (116 constants) is documented in **Appendix E: Smart Pin Constants**. These include:

- Pin mode constants (P_ASYNC_TX, P_ASYNC_RX, P_SYNC_TX, etc.)
- DAC configuration (P_DAC_*, P_BITDAC)
- ADC configuration (P_ADC_*)
- Filter and logic modes (P_FILT*, P_LOGIC_*, P_COMPARE_*)
- Output drive strength (P_HIGH_*, P_LOW_*)
- Many more specialized pin configurations

All P_* constants are reserved words and cannot be used as user-defined symbols.



### Streamer Constants (X_*)

The complete list of Streamer mode constants (78 constants) is documented in **Appendix F: Streamer Constants**. These include:

- Immediate mode constants (X_IMM_*)
- RF byte/word/long modes (X_RFBYTE_*, X_RFWORD_*, X_RFLONG_*)
- DAC output configurations (X_*DAC*)
- Control flags (X_PINS_ON, X_PINS_OFF, X_WRITE_ON, X_WRITE_OFF, etc.)

All X_* constants are reserved words and cannot be used as user-defined symbols.


