# Assembler Directives

Assembler directives control the assembly process itself. Unlike instructions that generate executable code, directives guide the assembler in organizing memory, reserving space, and verifying code constraints. Directives execute at assembly time, not runtime.

The P2 assembler provides 14 directives organized into five functional categories: origin control, memory definition, size verification, alignment, and space management.



## Origin Control Directives

Origin directives set the memory address where subsequent code or data will be assembled. The P2 distinguishes between cog RAM (0-$1FF) and hub RAM addresses.

::: dirheader
### ORG {#org}
Set Origin

Sets assembly origin to a specific cog RAM address.
:::

Set the assembly origin to a specific cog RAM address. All subsequent instructions assemble starting from this address.

#### Syntax
```pasm
        ORG     address
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Cog RAM address (0-$1FF, range 0-511 decimal) |

#### Usage
Use ORG to position code or data at specific cog RAM addresses. This is essential for creating interrupt vectors, placing time-critical code at optimal locations, or organizing cog memory layout.

#### Example
```pasm
        ORG     0               ' Start at cog RAM address 0
entry   jmp     #main           ' First instruction at address 0

        ORG     $100            ' Start at cog address $100
table   long    1, 2, 3         ' Data table at specific address
```

#### Notes
- ORG affects cog RAM addresses only (range 0-$1FF)
- For hub RAM addresses, use ORGH
- To fill gaps between addresses with zeros, use ORGF
- ORG simply sets the address counter without generating any bytes

#### Related Directives
- [ORGH](#orgh) — Set hub RAM origin
- [ORGF](#orgf) — Set origin with zero-fill
- [FIT](#fit) — Verify code fits within address limit



::: dirheader
### ORGF {#orgf}
Set Origin With Fill

Advances to specified address, filling with zeros.
:::

Set origin with fill—advance to specified address, filling intervening space with zeros. Unlike ORG which simply sets the address counter, ORGF fills the gap between the current address and the target address with zero bytes.

#### Syntax
```pasm
        ORGF    address
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Target address to advance to (cog 0-$1FF or hub address) |

#### Usage
Use ORGF when you need contiguous binary output with guaranteed zero-filled gaps. This ensures data structures start at exact addresses while maintaining a complete memory image. Essential for interrupt vector tables, memory-mapped structures, and fixed-layout binary formats.

#### Example
```pasm
DAT
        ORG     0
entry   jmp     #main
        ' ... some code ...

        ORGF    $100            ' Fill with zeros up to address $100
table   long    1, 2, 3         ' Table starts exactly at $100

        ' Create fixed-size code block
        ORG     0
block_start
        ' ... code ...
        ORGF    block_start + 64   ' Ensure block is exactly 64 longs
block_end
```

#### Notes
- ORGF fills the gap with zero bytes/longs to reach the target address
- Generates assembly error if target address is less than current address
- ORG only changes the address counter without filling
- Useful for creating fixed-layout binary structures
- Essential for interrupt vector tables and memory-mapped structures

#### Related Directives
- [ORG](#org) — Set origin without fill
- [ORGH](#orgh) — Set hub RAM origin
- [FIT](#fit) — Verify code fits
- [RES](#res) — Reserve space without initialization



::: dirheader
### ORGH {#orgh}
Set Hub Origin

Sets assembly origin to a hub RAM address.
:::

Set the assembly origin to a hub RAM address. All subsequent code and data assemble for hub execution starting at the specified address.

#### Syntax
```pasm
        ORGH    [address]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Hub RAM address (optional, defaults to $400) |

#### Usage
Use ORGH when switching from cog-exec code to hub-exec code, or when defining data that resides in hub RAM. If no address is specified, ORGH defaults to $400, the standard starting location for hub-exec code.

#### Example
```pasm
        ORGH    $400            ' Start at hub address $400
        ' Hub-exec code here

        ORGH                    ' Default: start at hub $400
```

#### Notes
- ORGH sets hub RAM addresses for hub-exec code and hub data
- Default address is $400 if not specified
- Hub-exec code executes directly from hub RAM without loading into cog
- After ORGH, use ORG to switch back to cog RAM addresses

#### Related Directives
- [ORG](#org) — Set cog RAM origin
- [ORGF](#orgf) — Set origin with fill
- HUBEXEC constant — Hub execution mode flag



## Memory Definition Directives

Memory definition directives allocate and initialize data in memory. Each directive specifies the size of data elements (byte, word, or long) and their initial values.

::: dirheader
### BYTE {#byte}
Declare Byte Data

Stores 8-bit values at the current address.
:::

Declare byte data in memory. Stores 8-bit values at the current address.

#### Syntax
```pasm
[label] BYTE    value[, value...]
[label] BYTE    value[count]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 8-bit value or string literal |
| count | Repetition count (creates *count* copies of *value*) |

#### Usage
Use BYTE to define individual bytes, byte arrays, or strings. Each value occupies exactly 1 byte. Strings are stored as individual bytes in sequence. BYTE provides no automatic alignment—data appears at the current address.

The repetition syntax `value[count]` creates multiple copies of the same value, useful for initializing buffers or padding.

#### Example
```pasm
text    byte    "Hello P2", 0   ' String with null terminator
data    byte    $FF, $00, $55   ' Hex values
nums    byte    1, 2, 3, 4, 5   ' Decimal values
zeros   byte    0[256]          ' 256 zero bytes (buffer initialization)
pattern byte    $AA[16], $55[16] ' Alternating pattern: 16 $AA, then 16 $55
```

#### Notes
- Each value occupies exactly 1 byte
- Strings are stored as individual bytes without alignment
- No automatic alignment—use ALIGNW or ALIGNL if needed
- Values outside 0-255 range will be truncated to 8 bits
- The `[count]` syntax repeats the preceding value, useful for buffer initialization

#### Related Directives
- [WORD](#word) — Declare 16-bit word data
- [LONG](#long) — Declare 32-bit long data
- [BYTEFIT](#bytefit) — Declare byte data with range validation
- [RES](#res) — Reserve uninitialized space



::: dirheader
### LONG {#long}
Declare Long Data

Stores 32-bit values at the current address.
:::

Declare long data in memory. Stores 32-bit values at the current address.

#### Syntax
```pasm
[label] LONG    value[, value...]
[label] LONG    value[count]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 32-bit value, expression, or address reference |
| count | Repetition count (creates *count* copies of *value*) |

#### Usage
Use LONG to define 32-bit integers, addresses, or any data requiring full 32-bit precision. Each value occupies 4 bytes. No automatic alignment—data packs sequentially; use ALIGNL before LONG if alignment is needed for optimal access efficiency.

The repetition syntax `value[count]` creates multiple copies of the same value, useful for initializing register buffers or lookup tables.

#### Example
```pasm
counter long    0               ' Single long
table   long    $1234_5678      ' Hex value with underscores for readability
ptrs    long    @start, @end    ' Address pointers
buffer  long    0[32]           ' 32 zero longs (128 bytes)
clkfreq long    160_000_000[8]  ' Initialize 8 entries with clock frequency
```

#### Notes
- Each value occupies 4 bytes
- No automatic alignment—data packs sequentially; use ALIGNL if alignment needed
- Supports full 32-bit range (0 to $FFFFFFFF)
- Standard size for P2 registers and instructions
- The `[count]` syntax repeats the preceding value

#### Related Directives
- [BYTE](#byte) — Declare 8-bit byte data
- [WORD](#word) — Declare 16-bit word data
- [ALIGNL](#alignl) — Force long alignment
- [RES](#res) — Reserve uninitialized longs



::: dirheader
### WORD {#word}
Declare Word Data

Stores 16-bit values at the current address.
:::

Declare word data in memory. Stores 16-bit values at the current address.

#### Syntax
```pasm
[label] WORD    value[, value...]
[label] WORD    value[count]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 16-bit value or expression |
| count | Repetition count (creates *count* copies of *value*) |

#### Usage
Use WORD to define 16-bit integers or data elements. Each value occupies 2 bytes. Data packs sequentially without automatic alignment—use ALIGNW if word alignment is needed for efficient access.

The repetition syntax `value[count]` creates multiple copies of the same value, useful for initializing tables or buffers.

#### Example
```pasm
counts  word    1000, 2000, 3000    ' Decimal values
addr    word    @buffer             ' Address reference (lower 16 bits)
zeros   word    0[64]               ' 64 zero words (128 bytes)
sine    word    $8000[256]          ' Initialize sine table with midpoint values
```

#### Notes
- Each value occupies 2 bytes
- No automatic alignment—data packs sequentially; use ALIGNW if alignment needed
- Range: 0 to 65535 (unsigned)
- Values outside this range will be truncated to 16 bits
- The `[count]` syntax repeats the preceding value

#### Related Directives
- [BYTE](#byte) — Declare 8-bit byte data
- [LONG](#long) — Declare 32-bit long data
- [WORDFIT](#wordfit) — Declare word data with range validation
- [ALIGNW](#alignw) — Force word alignment



::: dirheader
### FILE {#file}
Include Binary File

Includes raw binary file data at the current address.
:::

Include the contents of a binary file at the current assembly address. The raw bytes from the specified file are inserted directly into the assembled output.

#### Syntax
```pasm
[label] FILE    "filename"
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| filename | Filename enclosed in double quotes (no path separators allowed) |

#### Filename Requirements

The filename must not contain path separator characters. The following characters are invalid in filenames:

| Character | Description |
|-----------|-------------|
| `/` | Forward slash |
| `:` | Colon |
| `*` | Asterisk |
| `?` | Question mark |
| `"` | Double quote |
| `<` | Less than |
| `>` | Greater than |
| `\|` | Pipe |

The compiler searches for the file in the following order:
1. **Current directory** — The directory containing the source file
2. **Library directory** — The compiler's built-in library location
3. **Include directories** — Directories specified via compiler options†

† *Include directory support varies by compiler. PNut_ts supports `-I` options; other P2 compilers may have different or no include directory mechanisms.*

#### Usage
Use FILE to embed binary resources directly into your program—font data, lookup tables, images, audio samples, or any pre-computed binary content. The file is read at assembly time and its raw bytes are inserted at the current address. A label preceding FILE becomes a byte pointer to the start of the included data.

FILE is only allowed in DAT blocks, not in inline PASM code within PUB or PRI methods.

#### Example
```pasm
DAT
' Include a font file for VGA text display
font_data   file    "8x8_font.bin"      ' 2KB font bitmap
font_end                                 ' Label marks end for size calculation

' Include pre-computed sine table
sine_table  file    "sine_256.dat"      ' 256-entry sine lookup

' Include raw image data
splash      file    "logo.raw"          ' Splash screen bitmap

' Calculate included file size at assembly time
            long    @font_end - @font_data  ' Store font size in bytes
```

#### Example: Text File Inclusion
```pasm
DAT
' Include text file for display
text_data   file    "message.txt"
text_end

PUB ShowText() | ptr, len
    ptr := @text_data
    len := @text_end - @text_data
    ' Process text bytes...
```

#### Notes
- FILE reads the file at assembly time—the file must exist during compilation
- File contents are included as raw bytes without modification
- A label before FILE provides a byte-addressable pointer to the data
- Place a label after the FILE directive to calculate the included file's size
- FILE is only allowed in DAT blocks (not in inline PASM code)
- Maximum filename length: 253 characters
- Filename matching is case-insensitive
- Common uses: fonts, lookup tables, images, audio samples, pre-computed data

#### Related Directives
- [BYTE](#byte) — Declare individual byte data
- [LONG](#long) — Declare long data
- [ORGH](#orgh) — Set hub origin (FILE data typically resides in hub RAM)



### Inline Type Mixing {#inline-type-mixing}

BYTE, WORD, and LONG declarations can be mixed within a single data block to create packed data structures. Each type specifier affects only the values that follow it until the next type specifier or end of line.

#### Example: Protocol Packet Header
```pasm
DAT
' Packet header: 1-byte type, 2-byte length, 4-byte timestamp
packet_hdr
        byte    $01             ' Packet type (1 byte)
        word    $0100           ' Length field (2 bytes)
        long    0               ' Timestamp placeholder (4 bytes)
```

#### Example: Mixed Data Block
```pasm
DAT
' Sensor configuration block with mixed sizes
sensor_cfg
        byte    $42             ' Sensor ID
        byte    $03             ' Channel count
        word    1000            ' Sample rate (Hz)
        long    @callback       ' Callback address
        byte    "SENS", 0       ' Name string with terminator
```

#### Notes
- Data elements pack contiguously regardless of size
- No automatic padding is inserted between different-sized elements
- Use ALIGNW or ALIGNL when subsequent access requires alignment
- This technique is useful for protocol buffers, hardware register layouts, and memory-mapped structures

For Spin2-declared structures (STRUCT) accessed from PASM2, refer to the Spin2 Reference Manual for structure memory layout and the SIZEOF() operator.



## Size Verification Directives

Size verification directives provide compile-time checking that values fit within specified bit ranges. These directives generate assembly errors when constraints are violated, catching overflow errors before runtime.

::: dirheader
### BYTEFIT {#bytefit}
Declare Byte Data With Range Validation

Stores byte values with compile-time range checking.
:::

Declare byte data with compile-time range validation. Works identically to BYTE for storage, but generates an assembly error if any value exceeds the valid byte range. This catches potential truncation errors during compilation.

#### Syntax
```pasm
[label] BYTEFIT  value [, value...]
[label] BYTEFIT  value[count]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | Constant value or expression that must fit in byte range |
| count | Repetition count (creates *count* copies of *value*) |

#### Valid Range

| Representation | Minimum | Maximum |
|----------------|---------|---------|
| Hexadecimal | -$80 | $FF |
| Decimal (signed) | -128 | 127 |
| Decimal (unsigned) | 0 | 255 |

The combined range allows both signed (-128 to +127) and unsigned (0 to 255) byte values.

#### Usage
Use BYTEFIT instead of BYTE when you need compile-time verification that values fit in 8 bits. This catches overflow errors during assembly rather than silently truncating values. BYTEFIT is particularly useful when values come from calculations or constants that might change.

#### Example
```pasm
DAT
' Valid BYTEFIT values
byteData    BYTEFIT   -$80              ' Minimum signed value: -128
            BYTEFIT   $FF               ' Maximum unsigned value: 255
            BYTEFIT   0, 100, 200, 255  ' Multiple values
            BYTEFIT   -128, -1, 0, 127  ' Signed values
            BYTEFIT   0[100]            ' 100 bytes of value 0

' Lookup table with validation
gammaTable  BYTEFIT   0, 1, 2, 3, 4, 5, 7, 9, 12, 15
            BYTEFIT   18, 22, 27, 32, 38, 44, 51, 58

' The following would cause compile errors:
'           BYTEFIT   256               ' ERROR: 256 > 255
'           BYTEFIT   -129              ' ERROR: -129 < -128
```

#### Error Message
When values exceed the valid range, the compiler produces:
```
BYTEFIT values must range from -$80 to $FF
```

#### Notes
- Compile-time validation only—no runtime overhead
- Storage is identical to BYTE (8 bits per value)
- Unlike BYTE, does not silently truncate out-of-range values
- Useful for lookup tables, configuration data, and calculated offsets
- Can only be used in DAT blocks

#### Related Directives
- [WORDFIT](#wordfit) — Declare word data with range validation
- [BYTE](#byte) — Declare byte data (no range checking)



::: dirheader
### WORDFIT {#wordfit}
Declare Word Data With Range Validation

Stores word values with compile-time range checking.
:::

Declare word data with compile-time range validation. Works identically to WORD for storage, but generates an assembly error if any value exceeds the valid word range. This catches potential truncation errors during compilation.

#### Syntax
```pasm
[label] WORDFIT  value [, value...]
[label] WORDFIT  value[count]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | Constant value or expression that must fit in word range |
| count | Repetition count (creates *count* copies of *value*) |

#### Valid Range

| Representation | Minimum | Maximum |
|----------------|---------|---------|
| Hexadecimal | -$8000 | $FFFF |
| Decimal (signed) | -32768 | 32767 |
| Decimal (unsigned) | 0 | 65535 |

The combined range allows both signed (-32768 to +32767) and unsigned (0 to 65535) word values.

#### Usage
Use WORDFIT instead of WORD when you need compile-time verification that values fit in 16 bits. This catches overflow errors during assembly rather than silently truncating values. WORDFIT is particularly useful when values come from calculations or constants that might change.

#### Example
```pasm
DAT
' Valid WORDFIT values
wordData    WORDFIT   -$8000            ' Minimum signed value: -32768
            WORDFIT   $FFFF             ' Maximum unsigned value: 65535
            WORDFIT   1000, 30000       ' Multiple values
            WORDFIT   -32768, 0, 32767  ' Signed values
            WORDFIT   $ABCD[50]         ' 50 words of value $ABCD

' ADC calibration values
adcOffsets  WORDFIT   -1024, -512, 0, 512, 1024
adcGains    WORDFIT   32768, 33000, 32500, 32768

' The following would cause compile errors:
'           WORDFIT   65536             ' ERROR: 65536 > 65535
'           WORDFIT   -32769            ' ERROR: -32769 < -32768
```

#### Error Message
When values exceed the valid range, the compiler produces:
```
WORDFIT values must range from -$8000 to $FFFF
```

#### Notes
- Compile-time validation only—no runtime overhead
- Storage is identical to WORD (16 bits per value)
- Unlike WORD, does not silently truncate out-of-range values
- Useful for lookup tables, calibration data, and calculated offsets
- Can only be used in DAT blocks

#### Related Directives
- [BYTEFIT](#bytefit) — Declare byte data with range validation
- [WORD](#word) — Declare word data (no range checking)



## Alignment Directives

Alignment directives insert padding bytes to align the next data or instruction to specified boundaries. Proper alignment improves memory access efficiency and is required for certain P2 operations.

::: dirheader
### ALIGNL {#alignl}
Align To Long Boundary

Inserts padding bytes for 4-byte alignment.
:::

Align to long boundary (4-byte alignment). Inserts zero bytes as needed to align the next data or instruction to a long boundary.

#### Syntax
```pasm
DAT
  code_and_data_statements
  ALIGNL
  data_statements
```

**Result:** The next data element is long-aligned in Hub RAM by emitting up to three bytes (each $00) prior.

- *code_and_data_statements* are leading program code and/or data.
- *data_statements* begin long-aligned in Hub RAM.

#### Explanation

ALIGNL aligns the next data element to the beginning of the next long of Hub RAM. ALIGNL is important to use when code requires certain data to begin on a long boundary (for access convenience and speed).

ALIGNL is only allowed in DAT blocks, not in in-line PASM.

#### Example

The following creates a data table of a byte ($11), a word ($BBAA), and a long ($44332211) meant for access from Hub RAM.

```pasm
DAT
    T1      byte    $11
    T2      word    $BBAA
            long    $44332211
```

This data may be emitted into the Hub memory image like below; the actual data start and alignment will vary depending on the code and data that precede it. The L#, W#, and B# labels denote contiguous long, word, and byte boundaries. Note that P2 is little-endian, so the word $BBAA stores as bytes $AA, $BB and the long $44332211 stores as bytes $11, $22, $33, $44 in memory order.

```{=latex}
\AlignLBeforeDiagram
```

Notice how each data element packs immediately after the previous one without any automatic padding or alignment. The word at T2 starts at byte offset 1 (misaligned), and the long starts at byte offset 3 (also misaligned). If the code that is meant to access Table T2 expects it to align with a long boundary (i.e. for convenient long-sized access or pointer alignment), the ALIGNL directive achieves this, as follows.

```pasm
DAT
    T1      byte    $11

            ALIGNL
    T2      word    $BBAA
            long    $44332211
```

In comparison, this data will be emitted as follows:

```{=latex}
\AlignLAfterDiagram
```

In this case, the ALIGNL directive causes three zero ($00) bytes to emit after Table T1 to pad and align the start of Table T2 to the boundary of L1. After T2, the word and long pack sequentially—the long at offset 6 is still misaligned. To long-align the long as well, another ALIGNL would be needed before it.

#### Notes
- Inserts 0-3 bytes of padding as needed to reach next 4-byte boundary
- P2 requires long alignment for certain operations
- Critical for hub memory access efficiency
- No effect if already on a long boundary

#### Related Directives
- [ALIGNW](#alignw) — Align to word boundary
- [LONG](#long) — Declare long data
- [ORG](#org) — Set origin address



::: dirheader
### ALIGNW {#alignw}
Align To Word Boundary

Inserts padding bytes for 2-byte alignment.
:::

Align to word boundary (2-byte alignment). Inserts zero bytes as needed to align the next data or instruction to a word boundary.

#### Syntax
```pasm
DAT
  code_and_data_statements
  ALIGNW
  data_statements
```

**Result:** The next data element is word-aligned in Hub RAM by emitting zero or one byte ($00) prior.

- *code_and_data_statements* are leading program code and/or data.
- *data_statements* begin word-aligned in Hub RAM.

#### Explanation

ALIGNW aligns the next data element to the beginning of the next word of Hub RAM. ALIGNW is important to use when code requires certain data to begin on a word boundary (for access convenience and speed).

ALIGNW is only allowed in DAT blocks, not in in-line PASM.

#### Example

The following creates a data table of a byte ($11), two bytes ($AA, $BB), and a long ($44332211) meant for access from Hub RAM.

```pasm
DAT
    T1      byte    $11
    T2      byte    $AA, $BB
            long    $44332211
```

This data may be emitted into the Hub memory image like below; the actual data start and alignment will vary depending on the code and data that precede it. The L#, W#, and B# labels denote contiguous long, word, and byte boundaries. Note that P2 is little-endian, so the long $44332211 stores as bytes $11, $22, $33, $44 in memory order.

```{=latex}
\AlignWBeforeDiagram
```

Notice how each data element, regardless of size, is packed right next to the data before it. If the code that is meant to access Table T2 expects it to align with a word boundary (i.e. for convenient word-sized access), the ALIGNW directive achieves this, as follows.

```pasm
DAT
    T1      byte    $11

            ALIGNW
    T2      byte    $AA, $BB
            long    $44332211
```

In comparison, this data will be emitted as follows:

```{=latex}
\AlignWAfterDiagram
```

In this case, the ALIGNW directive causes one zero ($00) byte to emit after Table T1 to pad and align the start of Table T2 to the boundary of W1. This allows T2 to be accessed as a word-aligned address. Note that the long after T2 packs sequentially at offset 4—it happens to be long-aligned here only because T2 is exactly 2 bytes; this is coincidental, not automatic.

#### Notes
- Inserts 0-1 bytes of padding as needed to reach next 2-byte boundary
- Important for 16-bit data access efficiency
- No effect if already on a word boundary

#### Related Directives
- [ALIGNL](#alignl) — Align to long boundary
- [WORD](#word) — Declare word data
- [ORG](#org) — Set origin address



## Space Management Directives

Space management directives control memory allocation and verify size constraints. These directives either reserve space without initialization or verify that code fits within specified limits.

::: dirheader
### DITTO {#ditto}
Repeat Previous Instruction

Inserts a copy of the preceding instruction.
:::

Repeat the previous instruction. Inserts a copy of the immediately preceding instruction at the current location.

#### Syntax
```pasm
        DITTO
```

#### Usage
Use DITTO to create repeated instruction sequences without copy-paste. Useful for loop unrolling, repeated initialization sequences, and creating multiple instances of the same operation. DITTO was introduced in Spin2/PASM2 version 50 and later.

#### Example
```pasm
        nop                     ' First NOP
        ditto                   ' Second NOP (repeat of previous)
        ditto                   ' Third NOP (repeat of previous)

        wrlong  data, ptra++    ' Write and increment pointer
        ditto                   ' Repeat the wrlong with ptra++
        ditto                   ' And again
        ditto                   ' Four total writes

' Initialize 8 consecutive registers to zero
        mov     reg+0, #0
        ditto                   ' reg+1
        ditto                   ' reg+2
        ditto                   ' reg+3
        ditto                   ' reg+4
        ditto                   ' reg+5
        ditto                   ' reg+6
        ditto                   ' reg+7
```

#### Notes
- Introduced in Spin2/PASM2 version 50 and later
- DITTO copies the exact previous instruction including all operands and effects
- Useful for loop unrolling and repeated initialization sequences
- Must follow a valid instruction—cannot be first in a DAT block
- The repeated instruction appears in listing output for clarity
- Each DITTO generates a full instruction word (same size as original)

#### Related Directives
- REP instruction — Hardware-assisted instruction repeat
- [ORG](#org) — Set origin address



::: dirheader
### FIT {#fit}
Verify Code Fits

Generates error if current address exceeds limit.
:::

Verify that code fits within specified address limit. Generates assembly error if current address exceeds specified limit.

#### Syntax
```pasm
        FIT     [address]
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Maximum allowed address (optional, defaults to $200 for cog RAM limit) |

#### Usage
Use FIT to verify that code doesn't exceed available space. This is essential for cog code, which must fit within 512 longs (addresses 0-$1FF). FIT generates an assembly error if the current address exceeds the specified limit, catching size overflow during assembly rather than at runtime.

#### Example
```pasm
' Cog code
        ORG     0
        ' ... code ...
        FIT     $1F0            ' Ensure fits before special regs

        FIT                     ' Default: ensure fits in cog RAM (< $200)
```

#### Notes
- FIT without parameter checks for cog RAM limit ($200 / 512 longs)
- Generates assembly error if limit exceeded
- Essential for cog code size verification
- Special registers occupy cog addresses $1F0-$1FF
- Use FIT $1F0 to ensure code doesn't overwrite special registers

#### Related Directives
- [ORG](#org) — Set origin address
- [RES](#res) — Reserve space
- [ORGF](#orgf) — Fill to address



::: dirheader
### RES {#res}
Reserve Space

Allocates cog RAM without initialization.
:::

Reserve space in cog RAM without initializing. Allocates memory space but doesn't generate any data.

#### Syntax
```pasm
[label] RES     count
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| count | Number of longs to reserve |

#### Usage
Use RES to allocate variables and buffers in cog RAM without initializing them. This advances the address counter by the specified number of longs without generating any bytes in the binary. RES is only valid in cog RAM—hub RAM variables must use LONG with initial values or be allocated at runtime.

#### Example
```pasm
buffer  res     16              ' Reserve 16 longs
temp    res     1               ' Reserve 1 long for temporary storage
```

#### Working with Spin2 Structures

When reserving space for Spin2-declared structures, use the SIZEOF() operator to calculate the correct size in longs:

```pasm
' Reserve space for a Spin2 structure (structure defined in CON block)
mystruct        res     SIZEOF(point) / 4       ' Reserve longs for point structure
```

The SIZEOF() operator returns the structure size in bytes, so divide by 4 to convert to longs for RES. For complete documentation of Spin2 structures and the SIZEOF() operator, refer to the Spin2 Reference Manual.

#### Notes
- RES only reserves space in cog RAM (not hub RAM)
- No hub memory is allocated or affected
- Useful for variables and buffers that will be initialized at runtime
- Advances address counter by count longs without generating binary data
- Use LONG to reserve initialized space in hub RAM
- SIZEOF() enables correct sizing when working with Spin2 structures

#### Related Directives
- [LONG](#long) — Declare initialized long data
- [ORG](#org) — Set origin address
- [FIT](#fit) — Verify space fits within limit



## Summary

The P2 assembler's 14 directives provide complete control over memory layout and assembly constraints:

**Origin Control**: ORG, ORGH, ORGF set assembly addresses
**Memory Definition**: BYTE, WORD, LONG allocate and initialize data; FILE includes binary files
**Size Verification**: BYTEFIT, WORDFIT declare data with compile-time range validation
**Alignment**: ALIGNL, ALIGNW optimize memory access
**Space Management**: RES, FIT, DITTO control allocation and verify constraints

These directives execute at assembly time, shaping the binary output without affecting runtime execution. Understanding and using directives effectively is essential for efficient P2 assembly programming.

