# Assembler Directives

Assembler directives control the assembly process itself. Unlike instructions that generate executable code, directives guide the assembler in organizing memory, reserving space, and verifying code constraints. Directives execute at assembly time, not runtime.

The P2 assembler provides 15 directives organized into seven functional categories: origin control, memory definition, size verification, alignment, code replication, space management, and inline assembly control.



## Origin Control Directives

Origin directives set the memory address where subsequent code or data will be assembled. The P2 distinguishes between COG RAM (0-$1FF), LUT RAM ($200-$3FF), and Hub RAM addresses.

### The $ Symbol (Current Origin)

Within DAT blocks, the `$` symbol represents the current origin address:

- **In COG mode** (after ORG): `$` returns the current COG address in longs (0-$3FF)
- **In Hub mode** (after ORGH): `$` returns the current Hub address in bytes

```pasm2
DAT
        ORG     0
        ' $ = 0 (COG address 0)
        NOP
        ' $ = 1 (COG address 1)

        ORGH    $400
        ' $ = $400 (Hub address $400)
        BYTE    0
        ' $ = $401 (Hub address $401)
```

### COG/LUT Memory Regions

| Address Range | Memory | Notes |
|---------------|--------|-------|
| $000 - $1EF | COG RAM | General purpose registers |
| $1F0 - $1FF | COG RAM | Special purpose registers (PTRA, DIRA, etc.) |
| $200 - $3FF | LUT RAM | Lookup table / additional code space |

::: dirheader
### ORG {#org}
Set Origin

Sets assembly origin to a specific COG/LUT RAM address.
:::

Set the assembly origin to a specific COG or LUT RAM address. All subsequent instructions assemble starting from this address.

#### Syntax
```pasm2
        ORG                     ' Reset to COG address 0, limit $1F8
        ORG     address         ' Set COG address, auto-calculate limit
        ORG     address, limit  ' Set COG address and limit
```

#### Parameters
| Parameter | Range | Description |
|-----------|-------|-------------|
| address | 0 to $400 | Starting COG/LUT address (in longs) |
| limit | 0 to $400 | Maximum address for FIT checking (optional) |

#### Auto-Limit Behavior

1. **Without parameters** (`ORG`):
   - Sets COG address to 0
   - Sets limit to $1F8 (standard COG RAM limit, before special registers)

2. **With address only** (`ORG address`):
   - Sets COG address to specified value
   - Auto-calculates limit:
     - If address < $200: limit = $200 (COG RAM boundary)
     - If address >= $200: limit = $400 (LUT RAM boundary)

3. **With address and limit** (`ORG address, limit`):
   - Sets COG address and limit to specified values

#### Usage
Use ORG to position code or data at specific COG/LUT RAM addresses. This is essential for creating interrupt vectors, placing time-critical code at optimal locations, organizing cog memory layout, or positioning code in LUT RAM.

#### Example
```pasm2
        ORG     0               ' Start at COG address 0
entry   jmp     #main           ' First instruction at address 0

        ORG     $100            ' Start at COG address $100
table   long    1, 2, 3         ' Data table at specific address

        ORG     $200            ' Start in LUT RAM
lut_code
        MOV     PA, #0          ' LUT address $200
        RET                     ' LUT address $201
        FIT     $400            ' Verify fits in LUT
```

#### Restrictions

| Restriction | Error Message |
|-------------|--------------|
| Inside inline assembly | `ORG not allowed within inline assembly code` |
| Inside DITTO block | `ORG not allowed within a DITTO block` |
| Address > $400 | `Cog address exceeds $400 limit` |
| Cannot precede with symbol | `This directive cannot be preceded by a symbol` |

#### Notes
- ORG affects COG/LUT RAM addresses (range 0-$3FF)
- For Hub RAM addresses, use ORGH
- To fill gaps between addresses with zeros, use ORGF
- ORG sets the address counter without generating any bytes
- DAT blocks start in Hub mode by default; use ORG to switch to COG mode

⚠️ **Pitfall:** Forgetting that ORG without parameters defaults to limit $1F8 (not $200) can cause unexpected FIT errors when code approaches the special register area.

#### Related Directives
- [ORGH](#orgh) — Set hub RAM origin
- [ORGF](#orgf) — Set origin with zero-fill
- [FIT](#fit) — Verify code fits within address limit



::: dirheader
### ORGF {#orgf}
Set Origin With Fill

Advances to specified address, filling with zeros.
:::

Set origin with fill—advance to specified address, filling intervening space with zeros. Unlike ORG which only sets the address counter, ORGF fills the gap between the current address and the target address with zero bytes.

#### Syntax
```pasm2
        ORGF    address
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| address | Target address to advance to (cog 0-$1FF or hub address) |

#### Usage
Use ORGF for contiguous binary output with guaranteed zero-filled gaps. ORGF ensures data structures start at exact addresses while maintaining a complete memory image. Essential for interrupt vector tables, memory-mapped structures, and fixed-layout binary formats.

#### Example
```pasm2
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

#### Restrictions

| Restriction | Error Message |
|-------------|--------------|
| In ORGH mode | `ORGF is not allowed in ORGH mode` |
| Target < current | `Origin already exceeds target` |
| Target > limit | `Cog address exceeds limit` |
| Cannot precede with symbol | `This directive cannot be preceded by a symbol` |

#### Notes
- ORGF fills the gap with zero bytes/longs to reach the target address
- ORGF is only valid in COG mode (after ORG), not in Hub mode
- Generates assembly error if target address is less than current address
- ORG only changes the address counter without filling
- Useful for creating fixed-layout binary structures
- Essential for interrupt vector tables and memory-mapped structures

⚠️ **Pitfall:** ORGF only works in COG mode. Attempting to use ORGF after ORGH produces an error. For hub address gaps, use explicit BYTE or LONG declarations with zero values.

#### Related Directives
- [ORG](#org) — Set origin without fill
- [ORGH](#orgh) — Set Hub RAM origin
- [FIT](#fit) — Verify code fits
- [RES](#res) — Reserve space without initialization



::: dirheader
### ORGH {#orgh}
Set Hub Origin

Sets assembly origin to a Hub RAM address.
:::

Set the assembly origin to a Hub RAM address. All subsequent code and data assemble for hub execution starting at the specified address.

#### Syntax
```pasm2
        ORGH                    ' Reset to current hub position (or $400)
        ORGH    address         ' Set hub address
        ORGH    address, limit  ' Set hub address and limit
```

#### Parameters
| Parameter | Range | Description |
|-----------|-------|-------------|
| address | $400 to $100000 | Starting hub address (in bytes) |
| limit | address to $100000 | Maximum address for FIT checking (optional) |

#### Behavior by Context

1. **Without parameters** (`ORGH`):
   - In Spin2 objects: Sets hub address to $400 (after interpreter)
   - In PASM-only objects: Sets hub address to current object position
   - Sets limit to $100000 (1MB)

2. **With address only** (`ORGH address`):
   - Sets hub address to specified value
   - In PASM-only mode: Pads with zeros to reach the address
   - Sets limit to $100000

3. **With address and limit** (`ORGH address, limit`):
   - Sets hub address and limit to specified values

#### Address Constraints

| Context | Minimum | Maximum |
|---------|---------|---------|
| Spin2 objects | $400 | $100000 |
| PASM-only objects | 0 | $100000 |

The $400 minimum for Spin2 objects reserves space for the Spin2 interpreter.

#### Usage
Use ORGH when switching from cog-exec code to hub-exec code, or when defining data that resides in Hub RAM. DAT blocks start in Hub mode by default. Use ORGH to explicitly set hub addresses or to switch back to Hub mode after using ORG.

#### Example
```pasm2
        ORGH    $400            ' Start at hub address $400
        ' Hub-exec code here

        ORGH                    ' Default: start at hub $400

        ORGH    $1000           ' Start at hub address $1000
hubData LONG    $DEADBEEF       ' Hub address $1000
        LONG    $CAFEBABE       ' Hub address $1004

        ORGH    $400, $800      ' Hub from $400 to $800 limit
        BYTE    0[1024]         ' 1KB of data
        FIT     $800            ' Verify fits within limit
```

#### Mode Switching

A DAT block can switch between COG and Hub modes multiple times:

```pasm2
DAT
        ORGH                    ' Hub mode: bytecode tables
dispatch_table
        WORD    @routine1
        WORD    @routine2
        ALIGNL

        ORG     $100            ' COG mode: register code
routine1
        MOV     PA, #1
        RET

        ORGH                    ' Back to hub mode
hub_data
        LONG    $12345678
```

#### Restrictions

| Restriction | Error Message |
|-------------|--------------|
| Inside inline assembly | `ORGH not allowed within inline assembly code` |
| Inside DITTO block | `ORGH not allowed within a DITTO block` |
| Address < $400 (Spin2) | `Hub address below $400 limit` |
| Address > $100000 | `Hub address exceeds $100000 ceiling` |
| Address decrease (PASM) | `Hub address cannot decrease` |
| Limit < address | `Hub address exceeds limit` |
| Cannot precede with symbol | `This directive cannot be preceded by a symbol` |

#### Notes
- ORGH sets Hub RAM addresses for hub-exec code and hub data
- Default address is $400 if not specified (in Spin2 objects)
- Hub-exec code executes directly from Hub RAM without loading into COG
- After ORGH, use ORG to switch to COG RAM addresses
- DAT blocks start in Hub mode by default

💡 **Tip:** Use `@label` to get the hub address of any label, regardless of whether that label is in COG or Hub mode.

#### Related Directives
- [ORG](#org) — Set COG RAM origin
- [ORGF](#orgf) — Set origin with fill
- [FIT](#fit) — Verify code fits within limit



## Memory Definition Directives

Memory definition directives allocate and initialize data in memory. Each directive specifies the size of data elements (byte, word, or long) and their initial values.

::: dirheader
### BYTE {#byte}
Declare Byte Data

Stores 8-bit values at the current address.
:::

Declare byte data in memory. Stores 8-bit values at the current address.

#### Syntax
```pasm2
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
```pasm2
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
```pasm2
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
```pasm2
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
```pasm2
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
```pasm2
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
```pasm2
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
| `|` | Pipe |

The compiler searches for the file in the following order:
1. **Current directory** — The directory containing the source file
2. **Library directory** — The compiler's built-in library location
3. **Include directories** — Directories specified via compiler options†

† *Include directory support varies by compiler. PNut_ts supports `-I` options; other P2 compilers may have different or no include directory mechanisms.*

#### Usage
Use FILE to embed binary resources directly into your program—font data, lookup tables, images, audio samples, or any pre-computed binary content. The file is read at assembly time and its raw bytes are inserted at the current address. A label preceding FILE becomes a byte pointer to the start of the included data.

FILE is only allowed in DAT blocks, not in inline PASM code within PUB or PRI methods.

#### Example
```pasm2
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
```pasm2
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
- [ORGH](#orgh) — Set hub origin (FILE data resides in hub RAM)



### Inline Type Mixing {#inline-type-mixing}

BYTE, WORD, and LONG declarations can be mixed within a single data block to create packed data structures. Each type specifier affects only the values that follow it until the next type specifier or end of line.

#### Example: Protocol Packet Header
```pasm2
DAT
' Packet header: 1-byte type, 2-byte length, 4-byte timestamp
packet_hdr
        byte    $01             ' Packet type (1 byte)
        word    $0100           ' Length field (2 bytes)
        long    0               ' Timestamp placeholder (4 bytes)
```

#### Example: Mixed Data Block
```pasm2
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
```pasm2
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
Use BYTEFIT instead of BYTE for compile-time verification that values fit in 8 bits. BYTEFIT catches overflow errors during assembly rather than silently truncating values. Particularly valuable when values derive from calculations or constants subject to change.

#### Example
```pasm2
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
```pasm2
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
Use WORDFIT instead of WORD for compile-time verification that values fit in 16 bits. WORDFIT catches overflow errors during assembly rather than silently truncating values. Particularly valuable when values derive from calculations or constants subject to change.

#### Example
```pasm2
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
```pasm2
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

```pasm2
DAT
    T1      byte    $11
    T2      word    $BBAA
            long    $44332211
```

This data is emitted into the Hub memory image as shown below. The actual starting address depends on preceding code and data; the relative layout remains constant. The L#, W#, and B# labels denote contiguous long, word, and byte boundaries. Note that P2 is little-endian, so the word $BBAA stores as bytes $AA, $BB and the long $44332211 stores as bytes $11, $22, $33, $44 in memory order.

```{=latex}
\AlignLBeforeDiagram
```

::: {.figurecaption #fig:alignl-before}
Figure D.1: Memory Layout Before ALIGNL
:::

Notice how each data element packs immediately after the previous one without any automatic padding or alignment. The word at T2 starts at byte offset 1 (misaligned), and the long starts at byte offset 3 (also misaligned). If the code that is meant to access Table T2 expects it to align with a long boundary (i.e. for convenient long-sized access or pointer alignment), the ALIGNL directive achieves this, as follows.

```pasm2
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

::: {.figurecaption #fig:alignl-after}
Figure D.2: Memory Layout After ALIGNL
:::

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
```pasm2
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

```pasm2
DAT
    T1      byte    $11
    T2      byte    $AA, $BB
            long    $44332211
```

This data is emitted into the Hub memory image as shown below. The actual starting address depends on preceding code and data; the relative layout remains constant. The L#, W#, and B# labels denote contiguous long, word, and byte boundaries. Note that P2 is little-endian, so the long $44332211 stores as bytes $11, $22, $33, $44 in memory order.

```{=latex}
\AlignWBeforeDiagram
```

::: {.figurecaption #fig:alignw-before}
Figure D.3: Memory Layout Before ALIGNW
:::

Notice how each data element, regardless of size, is packed right next to the data before it. If the code that is meant to access Table T2 expects it to align with a word boundary (i.e. for convenient word-sized access), the ALIGNW directive achieves this, as follows.

```pasm2
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

::: {.figurecaption #fig:alignw-after}
Figure D.4: Memory Layout After ALIGNW
:::

In this case, the ALIGNW directive causes one zero ($00) byte to emit after Table T1 to pad and align the start of Table T2 to the boundary of W1. This allows T2 to be accessed as a word-aligned address. Note that the long after T2 packs sequentially at offset 4—it happens to be long-aligned here only because T2 is exactly 2 bytes; this is coincidental, not automatic.

#### Notes
- Inserts 0-1 bytes of padding as needed to reach next 2-byte boundary
- Important for 16-bit data access efficiency
- No effect if already on a word boundary

#### Related Directives
- [ALIGNL](#alignl) — Align to long boundary
- [WORD](#word) — Declare word data
- [ORG](#org) — Set origin address



## Code Replication Directive

The code replication directive generates multiple copies of instruction or data blocks at compile time. Unlike runtime repetition (REP instruction), code replication expands during assembly, producing distinct instruction copies with optional iteration-based variation.

::: dirheader
### DITTO {#ditto}
Replicate Code/Data Block

Repeats a block of code or data with iteration index access.
:::

Replicate a block of instructions or data a specified number of times at compile time. The special `$$` symbol provides access to the current iteration index within the block.

#### Syntax
```pasm2
DAT
        DITTO   count           ' Start block, repeat count times
        ' ... code or data ...
        DITTO   END             ' End block
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| count | Number of iterations (0 or more); zero skips the block entirely |
| `$$` | Special symbol evaluating to current iteration index (0 to count-1) |

#### Usage
Use DITTO to generate repetitive code or data patterns without manual duplication. The `$$` symbol allows each iteration to produce different values based on the iteration index. This is particularly useful for pin initialization sequences, lookup table generation, and multi-channel configurations. DITTO was introduced in PNut version 50.

#### Example
```pasm2
CON
  NumChannels = 8
  BasePin = 16

DAT
        ORG     0

' Initialize 8 consecutive pins using DITTO
        DITTO   NumChannels
        DRVH    #BasePin + $$   ' Drive pins 16, 17, 18, ... 23 high
        DITTO   END

' Generate indexed data table
        DITTO   4
        LONG    $$ * 100        ' Produces: 0, 100, 200, 300
        DITTO   END

' Multi-instruction block per iteration
        DITTO   NumChannels
        WRPIN   ##PinMode, #BasePin + $$
        WXPIN   ##PinX, #BasePin + $$
        DRVL    #BasePin + $$
        DITTO   END
```

#### Zero Count Behavior

When count is 0, the entire block is skipped with no output generated:

```pasm2
CON
  MotorCount = 0                ' No motors in this build

DAT
        DITTO   MotorCount      ' Block skipped entirely
        ' ... motor init code ...
        DITTO   END
```

#### Restrictions

| Restriction | Error Message |
|-------------|--------------|
| ORG inside DITTO | `ORG not allowed within a DITTO block` |
| ORGH inside DITTO | `ORGH not allowed within a DITTO block` |
| `$$` outside DITTO | `"$$" (DITTO index) is only allowed within a DITTO block` |
| Negative count | `DITTO count must be a positive integer or zero` |
| Missing END | `Expected DITTO END` |

#### Notes
- Introduced in PNut version 50
- Works in COG, LUT, and ORGH (hub) modes
- `$$` can be used in any expression: `$$ * 2`, `1 << $$`, `BasePin + $$`
- Replication occurs at compile time—no runtime overhead
- Use constants for count to enable configuration: `DITTO NumChannels`
- Each iteration generates its own instructions/data with `$$` evaluated fresh

#### Related Directives
- REP instruction — Hardware-assisted runtime instruction repeat
- [ORG](#org) — Set origin address (not allowed inside DITTO)
- [ORGH](#orgh) — Set hub origin (not allowed inside DITTO)



## Space Management Directives

Space management directives control memory allocation and verify size constraints. FIT verifies that code fits within specified address limits, while RES reserves COG/LUT RAM space without initialization.

::: dirheader
### FIT {#fit}
Verify Code Fits

Generates error if current address exceeds limit.
:::

Verify at compile time that the current address has not exceeded a specified limit. FIT is a safety check that produces an error if code or data is too large.

#### Syntax
```pasm2
        FIT     limit           ' Verify current address <= limit
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| limit | Maximum address (in longs for COG mode, bytes for Hub mode) |

#### Behavior by Mode

**In COG Mode (after ORG):**
- `limit` is a long address (0 to $400)
- Error: `Cog address exceeds FIT limit`

**In Hub Mode (after ORGH):**
- `limit` is a byte address
- Error: `Hub address exceeds FIT limit`

#### Common Limit Values

| Limit | Meaning |
|-------|---------|
| `$1F0` | User COG RAM (before special registers) |
| `$1F8` | COG RAM (with some special registers) |
| `$200` | Full COG RAM |
| `$400` | COG + LUT RAM |
| `496` | Decimal equivalent of $1F0 |

#### Usage
Use FIT to verify that code does not exceed available space. This is essential for COG code, which must fit within 512 longs (addresses 0-$1FF). FIT generates an assembly error if the current address exceeds the specified limit, catching size overflow during assembly rather than at runtime.

FIT does nothing if the limit is not exceeded—it is purely a compile-time check.

#### Example: Standard COG Program
```pasm2
DAT
        ORG     0

entry   ASMCLK                  ' Set clock
        ' ... main code ...
        JMP     #entry

vars    RES     10

        FIT     $1F0            ' Ensure user area only
```

#### Example: Split COG/LUT Program
```pasm2
DAT
        ORG     0

        ' COG code
        MOV     PA, #1
        CALL    #lut_routine
        JMP     #$

        FIT     $200            ' Must fit in COG before LUT

        ORG     $200            ' LUT code

lut_routine
        MOV     PB, #2
        RET

        FIT     $400            ' Must fit in LUT
```

#### Example: Hub Data Table
```pasm2
DAT
        ORGH    $400

sinTable
        LONG    0[256]          ' Sine lookup table

        FIT     $800            ' Table must not exceed $800
```

#### Example: Calculated Limits
```pasm2
CON
  OVERLAY_END = $300

DAT
        ORG     0
        ' ... overlay code ...
        FIT     OVERLAY_END     ' Must fit before overlay area
```

#### Restrictions

| Restriction | Error |
|-------------|-------|
| Cannot have a preceding label | `This directive cannot be preceded by a symbol` |
| Address exceeds COG limit | `Cog address exceeds FIT limit` |
| Address exceeds Hub limit | `Hub address exceeds FIT limit` |

#### Notes
- FIT generates an assembly error if the limit is exceeded
- Essential for COG code size verification
- Special registers occupy COG addresses $1F0-$1FF
- Use FIT $1F0 to ensure code does not overwrite special registers
- FIT works in both COG mode and Hub mode

💡 **Tip:** Always add FIT after COG code to catch overflow early. It costs nothing at runtime and prevents hard-to-debug overwrites of special registers or adjacent code.

#### Related Directives
- [ORG](#org) — Set origin address
- [RES](#res) — Reserve space
- [ORGF](#orgf) — Fill to address



::: dirheader
### RES {#res}
Reserve Space

Allocates COG/LUT RAM without initialization.
:::

Reserve space in COG or LUT RAM without initializing. Allocates memory space but generates no object code.

#### Syntax
```pasm2
[label] RES     count           ' Reserve 'count' longs
[label] RES     0               ' Create label here, no space reserved
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| label | Symbol name for the reserved space (optional but typical) |
| count | Number of longs to reserve (can be 0) |

#### Key Characteristics

1. **COG Mode Only** - RES only works after ORG, not in ORGH mode
2. **No Object Code** - RES advances the COG address counter but produces no bytes in the object file
3. **Uninitialized** - Reserved space contains whatever was previously in COG RAM
4. **Long-Aligned** - RES advances to the next long boundary before reserving

#### Usage
Use RES to allocate variables and buffers in COG RAM without initializing them. This advances the address counter by the specified number of longs without generating any bytes in the binary. RES is only valid in COG/LUT RAM—Hub RAM variables must use LONG with initial values or be allocated at runtime.

#### Example
```pasm2
DAT
        ORG     0

entry   MOV     temp, #100
        ADD     temp, value
        RET

temp    RES     1               ' Reserve 1 long for temporary variable
value   RES     1               ' Reserve 1 long for value storage
buffer  RES     16              ' Reserve 16 longs for buffer
```

#### Zero-Count Label (Alias Technique)

RES with a count of 0 creates a label at the current address without reserving any space. This technique creates aliases—multiple names for the same register:

```pasm2
DAT
        ORG     0

' Create aliases - both point to same register
ma      RES     0               ' ma is alias for x (RES 0 = no space)
x       RES     1               ' x occupies 1 long

' Both ma and x refer to the same COG address
```

💡 **Tip:** Use RES 0 aliases to give meaningful names for overlapping register uses—for example, `float_a` and `int_x` can be aliases when the same register serves different purposes at different times.

#### RES vs LONG for Data

| Aspect | `RES count` | `LONG 0[count]` |
|--------|-------------|-----------------|
| Initializes memory | No | Yes (to 0) |
| Generates object code | No | Yes |
| Valid in ORGH mode | No | Yes |
| Use case | COG working registers | Initialized data |

#### Working with Spin2 Structures

When reserving space for Spin2-declared structures, use the SIZEOF() operator to calculate the correct size in longs:

```pasm2
' Reserve space for a Spin2 structure (structure defined in CON block)
mystruct        RES     SIZEOF(point) / 4       ' Reserve longs for point structure
```

The SIZEOF() operator returns the structure size in bytes, so divide by 4 to convert to longs for RES. For complete documentation of Spin2 structures and the SIZEOF() operator, refer to the Spin2 Reference Manual.

#### Restrictions

| Restriction | Error Message |
|-------------|--------------|
| Used in ORGH mode | `RES is not allowed in ORGH mode` |
| Exceeds limit | `Cog address exceeds limit` |

#### Notes
- RES only reserves space in COG/LUT RAM (not Hub RAM)
- No Hub memory is allocated or affected
- Useful for variables and buffers that will be initialized at runtime
- Advances address counter by count longs without generating binary data
- Use LONG to declare initialized data in Hub RAM
- SIZEOF() enables correct sizing when working with Spin2 structures

⚠️ **Pitfall:** RES cannot be used in Hub mode (after ORGH). For hub-resident uninitialized buffers, use `LONG 0[count]` which does generate object code.

#### Related Directives
- [LONG](#long) — Declare initialized long data
- [ORG](#org) — Set origin address
- [FIT](#fit) — Verify space fits within limit



## Inline Assembly Directives

Inline assembly allows PASM2 code to be embedded directly within Spin2 PUB and PRI methods. The END directive marks the boundary where inline assembly ends and Spin2 code resumes.

::: dirheader
### END {#end}
End Inline Assembly

Terminates an inline assembly block within a Spin2 method.
:::

Terminate an inline assembly block and return to Spin2 execution. The compiler automatically inserts a RET instruction at the END location.

#### Syntax
```pasm2
PUB/PRI MethodName() | locals
  ' Spin2 code

  ORG                           ' Begin inline PASM (COG execution)
  ' ... PASM instructions ...
  END                           ' End inline PASM, implicit RET

  ' Spin2 code continues
```

#### Parameters

END takes no parameters. It must appear alone on its line.

#### Usage

Use END to mark the conclusion of an inline assembly block that began with ORG or ORGH within a PUB or PRI method. Inline assembly enables time-critical operations to execute at full PASM speed within Spin2 methods.

**ORG vs ORGH for Inline Assembly:**

| Directive | Execution Location | Speed | Address Space |
|-----------|-------------------|-------|---------------|
| ORG | COG RAM | Fastest | $000-$11F (limited) |
| ORGH | Hub RAM | Fast | Larger |

#### Example: Pin Toggle

```spin2
PUB FastToggle(pin) | mask

  mask := 1 << pin              ' Spin2 code

  ORG                           ' Begin inline PASM (COG execution)
                DRVNOT  mask    ' Toggle the pin
  END                           ' End inline PASM, implicit RET

  ' Execution returns here
```

#### Example: I2C Start Sequence

```spin2
PUB start() | scl, sda, tix

  longmove(@scl, @sclpin, 3)    ' Copy pins & timing to locals

  ORG
                DRVH    sda     ' SDA high
                DRVH    scl     ' SCL high
                WAITX   tix     ' Delay

                DRVL    sda     ' SDA low (start condition)
                WAITX   tix     ' Delay
                DRVL    scl     ' SCL low
                WAITX   tix     ' Delay
  END
```

#### Example: Local Variable Access

Inline PASM accesses local variables by name:

```spin2
PUB Example() | value, result

  value := 100

  ORG
                MOV     result, value    ' Read local variable
                ADD     result, #50      ' Modify
  END

  ' result now contains 150
```

#### Restrictions

| Restriction | Error Message |
|-------------|--------------|
| Missing END after ORG/ORGH in method | `Expected END` |
| ORG inside inline (nested) | `ORG not allowed within inline assembly code` |
| ORGH inside inline (nested) | `ORGH not allowed within inline assembly code` |
| ALIGNW/ALIGNL inside inline | `ALIGNW/ALIGNL not allowed within inline assembly code` |

#### END vs RET

| Aspect | END | RET instruction |
|--------|-----|-----------------|
| Purpose | End inline block | Return from PASM subroutine |
| Automatic RET | Compiler adds RET | Manual |
| Returns to | Spin2 code | PASM caller |
| Context | Inline assembly only | Any PASM code |

#### Notes
- END is only valid within inline assembly blocks (after ORG or ORGH in PUB/PRI methods)
- The compiler automatically inserts a RET instruction at the END location
- Inline assembly is limited in scope—complex PASM routines belong in DAT blocks
- Local variables declared in the method are accessible by name within inline PASM
- END does not apply to DAT blocks—DAT assembly has no explicit terminator

#### Variable vs Code Limits in Inline PASM

The Spin2 interpreter handles inline PASM in two separate copy operations:

1. The first 16 long variables (method parameters, result, and locals) are copied to cog registers `$1E0..$1EF`. **The 16-long limit applies to variables only — not to the PASM code itself.**
2. The PASM code is copied separately into cog registers starting at the ORG address (default `$000`).

With no multitasking in use, the inline code area is `$000..$11F` — 288 longs of code space, which is far more than the variable limit suggests.

#### Multitasking and Inline Code Space Overlap

When a cog uses Spin2 multitasking, the interpreter maintains a taskptr table in cog registers `$100..$11F`. The taskptr for task 31 occupies `$11F`, task 30 occupies `$11E`, and so on, filling downward. **This range is the upper portion of the inline-PASM code area** (`$000..$11F`) — multitasking and large inline-PASM blocks compete for the same space.

Programs using fewer than 32 software tasks leave the *lower* portion of `$100..$11F` free for inline code. Programs using all 32 tasks consume the full table. Plan inline-PASM size accordingly, or place large inline blocks in `ORGH` (hub-exec mode) to avoid this conflict entirely.

⚠️ **Pitfall:** Programs using both inline PASM and multitasking can silently lose code space without compile-time warning. If an inline block compiles but behaves unexpectedly with multitasking enabled, suspect taskptr-table overlap and move the block to `ORGH`.

💡 **Tip:** Keep inline assembly short and focused. For complex PASM routines, define them in a DAT block and launch with COGINIT or CALL from hub-exec code.

#### Related Directives
- [ORG](#org) — Set COG/LUT origin (begins inline block in methods)
- [ORGH](#orgh) — Set hub origin (begins hub-exec inline block)



## Summary

The P2 assembler's 15 directives provide complete control over memory layout and assembly constraints:

**Origin Control**: ORG, ORGH, ORGF set assembly addresses
**Memory Definition**: BYTE, WORD, LONG allocate and initialize data; FILE includes binary files
**Size Verification**: BYTEFIT, WORDFIT declare data with compile-time range validation
**Alignment**: ALIGNL, ALIGNW optimize memory access
**Code Replication**: DITTO generates multiple copies of instruction/data blocks at compile time
**Space Management**: RES, FIT control allocation and verify constraints
**Inline Assembly**: END terminates inline PASM blocks within Spin2 methods

These directives execute at assembly time, shaping the binary output without affecting runtime execution. Understanding and using directives effectively is essential for efficient P2 assembly programming.

