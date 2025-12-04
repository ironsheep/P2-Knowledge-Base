# Assembler Directives

Assembler directives control the assembly process itself. Unlike instructions that generate executable code, directives guide the assembler in organizing memory, reserving space, and verifying code constraints. Directives execute at assembly time, not runtime.

The P2 assembler provides 13 directives organized into five functional categories: origin control, memory definition, size verification, alignment, and space management.



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
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 8-bit value or string literal |

#### Usage
Use BYTE to define individual bytes, byte arrays, or strings. Each value occupies exactly 1 byte. Strings are stored as individual bytes in sequence. BYTE provides no automatic alignment—data appears at the current address.

#### Example
```pasm
text    byte    "Hello P2", 0   ' String with null terminator
data    byte    $FF, $00, $55   ' Hex values
nums    byte    1, 2, 3, 4, 5   ' Decimal values
```

#### Notes
- Each value occupies exactly 1 byte
- Strings are stored as individual bytes without alignment
- No automatic alignment—use ALIGNW or ALIGNL if needed
- Values outside 0-255 range will be truncated to 8 bits

#### Related Directives
- [WORD](#word) — Declare 16-bit word data
- [LONG](#long) — Declare 32-bit long data
- [BYTEFIT](#bytefit) — Verify value fits in byte range
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
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 32-bit value, expression, or address reference |

#### Usage
Use LONG to define 32-bit integers, addresses, or any data requiring full 32-bit precision. Each value occupies 4 bytes. In hub RAM, LONG data is automatically long-aligned for optimal access efficiency.

#### Example
```pasm
counter long    0               ' Single long
table   long    $1234_5678      ' Hex value with underscores for readability
ptrs    long    @start, @end    ' Address pointers
```

#### Notes
- Each value occupies 4 bytes
- Automatically long-aligned in hub RAM
- Supports full 32-bit range (0 to $FFFFFFFF)
- Standard size for P2 registers and instructions

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
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| value | 16-bit value or expression |

#### Usage
Use WORD to define 16-bit integers or data elements. Each value occupies 2 bytes. In hub RAM, WORD data is automatically word-aligned for efficient 16-bit access.

#### Example
```pasm
counts  word    1000, 2000, 3000    ' Decimal values
addr    word    @buffer             ' Address reference (lower 16 bits)
```

#### Notes
- Each value occupies 2 bytes
- Automatically word-aligned in hub RAM
- Range: 0 to 65535 (unsigned)
- Values outside this range will be truncated to 16 bits

#### Related Directives
- [BYTE](#byte) — Declare 8-bit byte data
- [LONG](#long) — Declare 32-bit long data
- [WORDFIT](#wordfit) — Verify value fits in word range
- [ALIGNW](#alignw) — Force word alignment



## Size Verification Directives

Size verification directives provide compile-time checking that values fit within specified bit ranges. These directives generate assembly errors when constraints are violated, catching overflow errors before runtime.

::: dirheader
### BYTEFIT {#bytefit}
Constrain To Byte Range

Generates error if expression exceeds byte range.
:::

Constrain expression to fit within byte range (0-255). Generates assembly error if expression value exceeds byte range.

#### Syntax
```pasm
        BYTEFIT(expression)
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| expression | Constant expression that must evaluate to 0-255 |

#### Usage
Use BYTEFIT to ensure compile-time verification that values fit in 8 bits. This catches overflow errors during assembly, preventing runtime data corruption. The expression must be resolvable at compile time.

#### Example
```pasm
        byte    BYTEFIT(100)        ' OK: 100 fits in a byte

CON
    SMALL_VAL = BYTEFIT(200)        ' OK: 200 fits in byte range

DAT
        byte    BYTEFIT(256)        ' ERROR: 256 exceeds byte range
```

#### Notes
- Compile-time constraint only—no runtime overhead
- Useful for catching overflow errors during assembly
- Expression must be resolvable at compile time (no runtime values)
- Generates error if value is negative or exceeds 255
- Returns the expression value if constraint is satisfied

#### Related Directives
- [WORDFIT](#wordfit) — Constrain to word range (0-65535)
- [BYTE](#byte) — Declare byte data



::: dirheader
### WORDFIT {#wordfit}
Constrain To Word Range

Generates error if expression exceeds word range.
:::

Constrain expression to fit within word range (0-65535). Generates assembly error if expression value exceeds word range.

#### Syntax
```pasm
        WORDFIT(expression)
```

#### Parameters
| Parameter | Description |
|-----------|-------------|
| expression | Constant expression that must evaluate to 0-65535 |

#### Usage
Use WORDFIT to ensure compile-time verification that values fit in 16 bits. This catches overflow errors during assembly before they cause runtime problems. The expression must be resolvable at compile time.

#### Example
```pasm
        word    WORDFIT(1000)       ' OK: 1000 fits in a word

CON
    MED_VAL = WORDFIT(50000)        ' OK: 50000 fits in word range

DAT
        word    WORDFIT(70000)      ' ERROR: 70000 exceeds word range
```

#### Notes
- Compile-time constraint only—no runtime overhead
- Useful for catching overflow errors during assembly
- Expression must be resolvable at compile time (no runtime values)
- Generates error if value is negative or exceeds 65535
- Returns the expression value if constraint is satisfied

#### Related Directives
- [BYTEFIT](#bytefit) — Constrain to byte range (0-255)
- [WORD](#word) — Declare word data



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
        ALIGNL
```

#### Usage
Use ALIGNL before data declarations or code sections that require long alignment for efficient access or hardware requirements. The P2 requires long alignment for certain operations and achieves optimal performance when accessing long-aligned data in hub RAM.

#### Example
```pasm
        ALIGNL                  ' Align to next long boundary
mydata  long    0               ' This starts on a long-aligned address
```

#### Notes
- Inserts 0-3 bytes of padding as needed to reach next 4-byte boundary
- P2 requires long alignment for certain operations
- Critical for hub memory access efficiency
- No effect if already on a long boundary

#### Related Directives
- [ALIGNW](#alignw) — Align to word boundary
- [LONG](#long) — Declare long data (auto-aligned in hub)
- [ORG](#org) — Set origin address



::: dirheader
### ALIGNW {#alignw}
Align To Word Boundary

Inserts padding bytes for 2-byte alignment.
:::

Align to word boundary (2-byte alignment). Inserts zero bytes as needed to align the next data or instruction to a word boundary.

#### Syntax
```pasm
        ALIGNW
```

#### Usage
Use ALIGNW before data declarations that require word alignment for efficient 16-bit access. Proper word alignment improves performance when accessing word-sized data in hub RAM.

#### Example
```pasm
        ALIGNW                  ' Align to next word boundary
myword  word    0               ' This starts on a word-aligned address
```

#### Notes
- Inserts 0-1 bytes of padding as needed to reach next 2-byte boundary
- Important for 16-bit data access efficiency
- No effect if already on a word boundary

#### Related Directives
- [ALIGNL](#alignl) — Align to long boundary
- [WORD](#word) — Declare word data (auto-aligned in hub)
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

#### Notes
- RES only reserves space in cog RAM (not hub RAM)
- No hub memory is allocated or affected
- Useful for variables and buffers that will be initialized at runtime
- Advances address counter by count longs without generating binary data
- Use LONG to reserve initialized space in hub RAM

#### Related Directives
- [LONG](#long) — Declare initialized long data
- [ORG](#org) — Set origin address
- [FIT](#fit) — Verify space fits within limit



## Summary

The P2 assembler's 13 directives provide complete control over memory layout and assembly constraints:

**Origin Control**: ORG, ORGH, ORGF set assembly addresses
**Memory Definition**: BYTE, WORD, LONG allocate and initialize data
**Size Verification**: BYTEFIT, WORDFIT catch overflow at compile time
**Alignment**: ALIGNL, ALIGNW optimize memory access
**Space Management**: RES, FIT, DITTO control allocation and verify constraints

These directives execute at assembly time, shaping the binary output without affecting runtime execution. Understanding and using directives effectively is essential for efficient P2 assembly programming.
