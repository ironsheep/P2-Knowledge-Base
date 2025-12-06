# Chapter 2: The Instruction Format

Every PASM2 instruction is encoded in a 32-bit word with a consistent structure. Understanding this format enables reading the encoding tables in Part II and manually encoding or decoding instructions when needed.


## 2.1 The 32-Bit Instruction Word

Every PASM2 instruction occupies exactly one 32-bit long with this structure:

```{=latex}
\InstructionEncoding{Generic}{EEEE}{OOOOOOO}{CZI}{DDDDDDDDD}{SSSSSSSSS}
```

### 2.1.1 Field Summary

| Field | Bits | Width | Purpose |
|:----------|:------|:------|:-----------------------------------------------|
| EEEE | 31-28 | 4 | Condition code for conditional execution |
| OOOOOOO | 27-21 | 7 | Opcode identifying the instruction |
| CZI | 20-18 | 3 | Flag effects and immediate mode |
| DDDDDDDDD | 17-9 | 9 | Destination register address |
| SSSSSSSSS | 8-0 | 9 | Source operand (register or immediate) |

### 2.1.2 The CZI Field

The three bits at positions 20-18 control flag behavior and operand mode:

| Bit | Position | Purpose |
|:----|:---------|:-------------------------------------------------|
| C | 20 | C flag write enable (1 = update C flag) |
| Z | 19 | Z flag write enable (1 = update Z flag) |
| I | 18 | Immediate mode (1 = S is immediate value) |

When WC is specified in source code, the assembler sets bit 20 to 1. When WZ is specified, bit 19 is set. When # prefixes the source operand, bit 18 is set.


## 2.2 Condition Codes (EEEE Field)

The condition field enables conditional execution of any instruction. The instruction executes only if the specified condition is true based on the current C and Z flags.

### 2.2.1 Condition Code Table

| EEEE | Mnemonic | Condition | Description |
|:-----|:-------------|:-------------|:------------------------------------------|
| 0000 | _RET_ | (special) | Return from subroutine |
| 0001 | IF_NC_AND_NZ | C=0 AND Z=0 | Neither carry nor zero |
| 0010 | IF_NC_AND_Z | C=0 AND Z=1 | No carry and zero |
| 0011 | IF_NC | C=0 | No carry (unsigned less than) |
| 0100 | IF_C_AND_NZ | C=1 AND Z=0 | Carry and not zero |
| 0101 | IF_NZ | Z=0 | Not zero |
| 0110 | IF_C_NE_Z | C≠Z | Carry not equal to zero |
| 0111 | IF_NC_OR_NZ | C=0 OR Z=0 | No carry or not zero |
| 1000 | IF_C_AND_Z | C=1 AND Z=1 | Carry and zero |
| 1001 | IF_C_EQ_Z | C=Z | Carry equals zero |
| 1010 | IF_Z | Z=1 | Zero |
| 1011 | IF_NC_OR_Z | C=0 OR Z=1 | No carry or zero |
| 1100 | IF_C | C=1 | Carry (unsigned greater than or equal) |
| 1101 | IF_C_OR_NZ | C=1 OR Z=0 | Carry or not zero |
| 1110 | IF_C_OR_Z | C=1 OR Z=1 | Carry or zero |
| 1111 | (always) | Always | Unconditional execution |

### 2.2.2 The _RET_ Condition

The condition code 0000 (_RET_) has special behavior. When an instruction has EEEE=0000, it functions as a return from subroutine:

- The instruction field is ignored
- PC is loaded from the return address stored in PA (for CALL) or from the stack

This encoding allows any instruction mnemonic to become a conditional return when prefixed with _RET_:

```pasm
_ret_   add     x, y                    ' Return, ADD is not executed
```

The _RET_ prefix is primarily used with CALLA, CALLB, and related call instructions that use the condition field for return control.

### 2.2.3 Conditional Execution Patterns

Conditional execution eliminates branches, providing deterministic timing:

```pasm
' Instead of branching:
                cmp     a, b            wc wz
        if_z    jmp     #equal_handler          ' 4 cycles if taken
                mov     result, #0

' Use conditional execution:
                cmp     a, b            wc wz
        if_z    mov     result, #1              ' Always 2 cycles
        if_nz   mov     result, #0              ' Always 2 cycles
```

Common patterns:

**Minimum/Maximum:**
```pasm
                cmp     a, b            wc      ' Compare unsigned
        if_c    mov     min, a                  ' min = a if a < b
        if_nc   mov     min, b                  ' min = b if a >= b
```

**Conditional Assignment:**
```pasm
                test    flags, #MASK    wz      ' Test bit
        if_nz   mov     mode, #1                ' Set if bit present
```

**Multi-way Selection:**
```pasm
                cmp     selector, #0    wz
        if_z    mov     result, value0
                cmp     selector, #1    wz
        if_z    mov     result, value1
                cmp     selector, #2    wz
        if_z    mov     result, value2
```


## 2.3 Reading Encoding Tables

Each instruction entry in Part II includes an encoding table with nine columns. The table shows the instruction's binary encoding on the left and its effects on the right.

### 2.3.1 Encoding Columns (Left Five)

The left five columns show the 32-bit instruction encoding:

| Column | Content | Description |
|:-------|:-------------|:---------------------------------------------------------------|
| COND | EEEE | Condition field (4 bits, always EEEE for conditional instructions) |
| INSTR | 7 bits | The instruction's unique opcode (positions 27-21) |
| FX | CZI variant | Flag modification and immediate bits (positions 20-18) |
| DEST | DDDDDDDDD | Destination field pattern (positions 17-9) |
| SRC | SSSSSSSSS | Source field pattern (positions 8-0) |

### 2.3.2 Result Columns (Right Four)

The right four columns describe instruction effects:

| Column | Content | Description |
|:-------|:---------------|:----------------------------------------------------|
| Write | What's written | Which register(s) receive output (D, PC, etc.) |
| C Flag | C behavior | How C flag is affected, or "---" for no change |
| Z Flag | Z behavior | How Z flag is affected, or "---" for no change |
| Clocks | Cycle count | Execution time in clock cycles |

### 2.3.3 The FX Field Variations

The FX column shows which flag and immediate options are available:

| FX Pattern | Meaning |
|:-----------|:----------------------------------------------------------------------------|
| CZI | C modifiable (WC), Z modifiable (WZ), Immediate allowed (#) |
| 0ZI | C not modifiable, Z modifiable, Immediate allowed |
| C0I | C modifiable, Z not modifiable, Immediate allowed |
| 00I | Neither flag modifiable, Immediate allowed |
| CZ0 | Flags modifiable, Immediate not allowed (register only) |
| NNI | NN bits encode sub-function (e.g., byte number), Immediate allowed |
| LLI | LL bits encode sub-function, Immediate allowed |

When FX shows fixed bits (like `000` or `01I`), those bits have fixed values and the corresponding options are not available.

### 2.3.4 Special Values in Columns

**Write column:**

| Value | Meaning |
|-------|---------|
| `D` | Destination register is written |
| `D and PC` | Both destination and program counter written (for jumps/calls) |
| `PC` | Only PC written |
| `---` | Nothing written (compare, test instructions) |
| `LUT` | LUT memory written |
| `Hub` | Hub memory written |

**Flag columns:**

| Value | Meaning |
|-------|---------|
| `---` | Flag is not changed |
| Descriptive text | Describes condition that sets/clears the flag |

**Clocks column:**

| Value | Meaning |
|-------|---------|
| `2` | Always 2 clock cycles |
| `2+` | Minimum 2 cycles, may be more |
| `2 or 4` | 2 if condition false/not taken, 4 if true/taken |
| `2 / 8-23` | COG mode cycles / Hub mode cycles |
| `9..35` | Variable range depending on operands |


## 2.4 Understanding Multiple Encoding Rows

Some instruction entries show multiple rows in the encoding table. Each row represents a unique machine code encoding.

### 2.4.1 Instruction Families

When related instructions share an entry (e.g., DIRZ/DIRNZ), each instruction gets its own row:

**DIRZ / DIRNZ**


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001000100 | D | --- | Orig bit | 2 |
| EEEE | 1101011 | CZ0 | DDDDDDDDD | 001000101 | D | --- | Orig bit | 2 |


The first row is DIRZ (S = 001000100), the second is DIRNZ (S = 001000101). Both share the same opcode but differ in the SRC field.

### 2.4.2 Multiple Syntax Forms

When one instruction has multiple syntax forms with different encodings:

**GETBYTE**

Syntax 1: `GETBYTE  Dest, {#}Src, #Num`

Syntax 2: `GETBYTE  Dest`


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1000111 | NNI | DDDDDDDDD | SSSSSSSSS | --- | --- | D | 2 |
| EEEE | 1000111 | 000 | DDDDDDDDD | 000000000 | --- | --- | D | 2 |


The first row shows the standard form with Src and Num operands (NN encodes the byte number 0-3). The second row shows the ALTGB-compatible form where Dest is both read and written.

### 2.4.3 Key Principle

Each unique machine code encoding = one table row. If two mnemonics produce different bit patterns, they appear as separate rows. If one mnemonic has multiple valid encodings (different syntax forms), each encoding appears as a row.


## 2.5 Destination and Source Fields

### 2.5.1 The Destination Field (D)

The 9-bit D field (bits 17-9) addresses a COG register from $000 to $1FF:

- **Read and written:** Most ALU instructions read D, compute, and write result back to D
- **Read only:** Compare instructions (CMP, CMPS, TEST) read D but do not modify it
- **Write only:** Some move instructions write D without reading its previous value

The D field can also specify:

- Hub addresses (for ALTD-modified instructions)
- LUT addresses (for LUT instructions)
- Pin numbers (for certain I/O instructions)

### 2.5.2 The Source Field (S)

The 9-bit S field (bits 8-0) has two modes controlled by the I bit:

**Register mode (I = 0):**

- S is a COG register address ($000-$1FF)
- The value in that register is used as the operand

**Immediate mode (I = 1):**

- S is a 9-bit unsigned value (0-511)
- This value is used directly as the operand

```pasm
        add     result, counter         ' S = register address (I=0)
        add     result, #100            ' S = immediate 100 (I=1)
```

### 2.5.3 When S is Fixed

Some encodings show fixed S values instead of SSSSSSSSS. These instructions use the S field to encode which specific operation to perform:

```{=latex}
\encodingsnippetannotated{EEEE}{1101011}{CZI}{DDDDDDDDD}{001000100}{Fixed value selects DIRZ}
```

The fixed value distinguishes this instruction from others sharing the same opcode. The programmer does not specify this value; it is implicit in the instruction mnemonic.


## 2.6 Immediate Operands

### 2.6.1 The # Prefix (9-bit Immediate)

The `#` prefix before an operand indicates an immediate value:

```pasm
        add     result, #100            ' Add immediate 100
        add     result, value           ' Add contents of register 'value'
        mov     x, #$1FF                ' Load maximum 9-bit value (511)
```

When `#` is used:

- The assembler sets the I bit (bit 18) to 1
- The S field contains the 9-bit value

### 2.6.2 Immediate Range

9-bit immediates can represent:

- Unsigned: 0 to 511 ($000 to $1FF)
- Signed (when interpreted): -256 to +255

Values outside this range require augmentation (see Section 2.7).

### 2.6.3 The $ Prefix for Current Address

The `$` symbol represents the current assembly address:

```pasm
loop    add     counter, #1
        djnz    count, #$-1             ' Jump back one instruction
```

When used with `#`, it becomes an immediate representing the address.


## 2.7 Augmented Immediates

### 2.7.1 The ## Prefix (32-bit Immediate)

The `##` prefix indicates a full 32-bit immediate value:

```pasm
        mov     dest, ##$12345678       ' Load full 32-bit value
        add     counter, ##1000000      ' Add 1 million
        mov     ptr, ##hub_data         ' Load 20-bit Hub address
```

### 2.7.2 AUGS and AUGD Instructions

The assembler implements 32-bit immediates by inserting AUG instructions:

- **AUGS** - Augments the Source field for the following instruction
- **AUGD** - Augments the Destination field for the following instruction

The AUG instruction provides the upper 23 bits, which combine with the lower 9 bits from the next instruction:

```pasm
' What the programmer writes:
        mov     dest, ##$12345678

' What the assembler generates:
        augs    #$12345                 ' Upper 23 bits: $12345
        mov     dest, #$678             ' Lower 9 bits: $678
                                        ' Combined: $12345678
```

### 2.7.3 Augmentation Behavior

The AUG instruction must immediately precede the instruction it augments:

1. The AUG executes, storing the 23-bit value internally
2. The next instruction combines this with its 9-bit field
3. The combined 32-bit value is used for that instruction only
4. The augmentation is consumed (one-shot)

If any instruction intervenes (including a conditional NOP), the augmentation is lost.

### 2.7.4 When Augmentation is Required

Augmentation is needed when:

- Values exceed 9 bits (> 511 for unsigned)
- Hub addresses are used (20-bit address space)
- 32-bit constants are needed
- Pin masks exceed 9 bits

```pasm
        wrlong  value, ##$1000          ' Hub address $1000 (> 511)
        mov     mask, ##$FFFF0000       ' 32-bit mask
        waitx   ##1000000               ' Delay > 511 cycles
```


## 2.8 How to Use This Manual

### 2.8.1 Looking Up an Instruction

1. **Find the instruction** alphabetically in Part II
2. **Read the syntax** to understand valid operand forms
3. **Check the Result** line for what the instruction produces
4. **Review Parameters** for operand requirements and constraints
5. **Use the Encoding table** when you need machine code details
6. **Read Related** instructions for alternatives and family members
7. **Study Explanation** for complete behavioral description

### 2.8.2 Visual Anchors: Color Bars

Each entry in Part II has a colored bar on the left edge of its header block. These color bars serve as visual anchors, making it easy to locate entry boundaries when scanning through pages.

The colors indicate entry type:

| Color | Entry Type | Description |
|:----------|:-----------|:--------------------------------------------------------|
| **Red** | Instruction | PASM2 machine instructions (the majority of entries) |
| **Amber** | Directive | Assembler directives like ORG, BYTE, LONG |
| **Violet** | Constant | Pre-defined constants like smart pin mode values |

The color bar spans the three-line identity block at the top of each entry:

1. **Mnemonic** --- The instruction, directive, or constant name
2. **Expansion** --- What the mnemonic stands for (e.g., "Add Signed, Extended")
3. **Category** --- The functional category with a brief description

When flipping through Part II, these color bars help you quickly identify entry boundaries and distinguish between instructions, directives, and constants.

### 2.8.3 Example: Understanding ADD

Consider the ADD instruction entry:

::: {.notebox}
**ADD** --- Math Instruction --- Add two unsigned values.

`ADD  Dest, {#}Src  {WC|WZ|WCZ}`

**Result:** Sum of unsigned Src and unsigned Dest is stored in Dest.

- Dest is a register containing the value to add Src to, and is where the result is written.
- Src is a register, 9-bit literal, or 32-bit augmented literal whose value is added into Dest.
- WC, WZ, or WCZ are optional effects to update flags.
:::


| EEEE | Opcode | CZI | D | S | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 0001000 | CZI | DDDDDDDDD | SSSSSSSSS | D | carry of (D + S) | Result = 0 | 2 |


From this entry:

- **Category:** Math Instruction - this is arithmetic
- **Syntax:** `{#}Src` means Src can be register or immediate; `{WC|WZ|WCZ}` means flag effects are optional
- **Result:** The sum goes into Dest (Dest is modified)
- **Encoding:** Opcode is 0001000 (7 bits); FX is CZI meaning all options available; takes 2 cycles
- **C Flag:** Set if addition overflows (unsigned carry)
- **Z Flag:** Set if result is zero

### 2.8.4 Using Categories for Discovery

Instructions are grouped by category in Appendix B. When looking for "an instruction that does X," consult the categorical index:

- **Math Instructions:** ADD, SUB, MUL, etc.
- **Logic Instructions:** AND, OR, XOR, etc.
- **Branch/Jump Instructions:** JMP, CALL, DJNZ, etc.
- **Hub Memory Instructions:** RDLONG, WRLONG, etc.

**Tip:** In the PDF version, the category name in each entry's header block is a clickable link that jumps directly to that category's listing in Appendix B.

### 2.8.5 Navigating with Links

The PDF version of this manual includes extensive cross-reference links to help you navigate efficiently. Links appear in blue text and are clickable:

**In the entry header block:**

- The **Category name** links to Appendix B's categorical listing

**In the Related line:**

> **Related:** ADDX, ADDS, ADDSX, SUB

Each instruction name in the Related section is a clickable link that jumps directly to that instruction's entry. This makes it easy to explore instruction families:

- ADDX: ADD with carry-in (for multi-precision)
- ADDS: Signed addition
- ADDSX: Signed addition with carry-in
- SUB: The opposite operation

**Navigation tip:** Use your PDF reader's "back" function (often Alt+Left Arrow or Cmd+[) to return to where you were after following a link.


## 2.9 Constant Expressions and Operators

PASM2 allows constant expressions anywhere a numeric value is expected. These expressions are evaluated at assembly time—the resulting value is encoded into the instruction, not computed at runtime. This enables readable, self-documenting code using symbolic calculations.

### 2.9.1 Where Constant Expressions Apply

Constant expressions can appear in:

- **Immediate operands:** `MOV x, #(BUFFER_SIZE - 1)`
- **EQU definitions:** `MAX_COUNT EQU 1000 * 60`
- **Data declarations:** `LONG $FF << 24 | $80 << 16`
- **ORG/ORGH directives:** `ORG $100 + HEADER_SIZE`
- **Repeat counts:** `REP @loop_end, #(TABLE_SIZE / 4)`

### 2.9.2 Operator Reference

Operators are listed from highest to lowest precedence within each category.

**Unary Operators** (highest precedence)

| Operator | Description | Example |
|----------|-------------|---------|
| `!` | Bitwise NOT (invert all bits) | `!$FF` → `$FFFFFF00` |
| `+` | Positive (no effect, explicit sign) | `+5` → `5` |
| `-` | Negate (two's complement) | `-1` → `$FFFFFFFF` |

**Bitwise Operators**

| Operator | Description | Example |
|----------|-------------|---------|
| `>>` | Shift right | `$80 >> 4` → `$08` |
| `<<` | Shift left | `1 << 8` → `$100` |
| `&` | Bitwise AND | `$FF & $0F` → `$0F` |
| `\|` | Bitwise OR | `$F0 \| $0F` → `$FF` |
| `^` | Bitwise XOR | `$FF ^ $0F` → `$F0` |

**Arithmetic Operators**

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `100 + 50` → `150` |
| `-` | Subtraction | `100 - 50` → `50` |
| `*` | Multiplication (lower 32 bits, signed) | `1000 * 1000` → `1000000` |
| `/` | Division quotient (signed) | `-100 / 3` → `-33` |
| `+/` | Division quotient (unsigned) | `$FFFFFFFF +/ 2` → `$7FFFFFFF` |
| `//` | Division remainder/modulo (signed) | `-100 // 3` → `-1` |
| `+//` | Division remainder (unsigned) | `$FFFFFFFF +// 16` → `15` |

**Limit Operators**

| Operator | Description | Example |
|----------|-------------|---------|
| `#>` | Limit minimum (signed) | `x #> 0` — ensures x ≥ 0 |
| `<#` | Limit maximum (signed) | `x <# 255` — ensures x ≤ 255 |

**Comparison Operators**

Comparison operators return -1 (true, all bits set) or 0 (false).

| Operator | Description | Signed/Unsigned |
|----------|-------------|-----------------|
| `<` | Less than | Signed |
| `+<` | Less than | Unsigned |
| `>` | Greater than | Signed |
| `+>` | Greater than | Unsigned |
| `<=` | Less than or equal | Signed |
| `+<=` | Less than or equal | Unsigned |
| `>=` | Greater than or equal | Signed |
| `+>=` | Greater than or equal | Unsigned |
| `==` | Equal | (n/a) |
| `<>` | Not equal | (n/a) |

**Boolean Operators**

| Operator | Description | Example |
|----------|-------------|---------|
| `!!` | Boolean NOT (0→-1, non-zero→0) | `!!5` → `0` |
| `&&` | Boolean AND | `(a > 0) && (b > 0)` |
| `\|\|` | Boolean OR | `(a == 0) \|\| (b == 0)` |
| `^^` | Boolean XOR | `(a > 0) ^^ (b > 0)` |
| `<=>` | Three-way compare (returns -1, 0, or 1) | `5 <=> 3` → `1` |

**Ternary Operator** (lowest precedence)

| Operator | Description | Example |
|----------|-------------|---------|
| `? :` | Conditional selection | `(x > 0) ? x : -x` — absolute value |

### 2.9.3 Signed vs. Unsigned Comparisons

The `+` prefix on comparison operators indicates unsigned comparison. This matters when comparing values that may have the high bit set:

```pasm
' Signed comparison: $80000000 is negative (-2147483648)
        IF  $80000000 < 0       ' True: negative < 0

' Unsigned comparison: $80000000 is positive (2147483648)
        IF  $80000000 +< 0      ' False: 2147483648 is not < 0
```

Use signed comparisons (`<`, `>`, etc.) for values representing signed quantities. Use unsigned comparisons (`+<`, `+>`, etc.) for addresses, bit patterns, or values that should never be negative.

### 2.9.4 Practical Examples

**Bit field construction:**
```pasm
PIN_MODE    EQU  %01 << 5 | %11 << 3 | %1 << 0   ' Combine fields
MASK_BITS   EQU  (1 << NUM_BITS) - 1              ' Create bit mask
```

**Buffer calculations:**
```pasm
BUFFER_END  EQU  BUFFER_START + BUFFER_SIZE - 1
WRAP_MASK   EQU  BUFFER_SIZE - 1                  ' For power-of-2 buffers
```

**Conditional assembly values:**
```pasm
DELAY_MS    EQU  (CLKFREQ / 1000) #> 1            ' At least 1 tick
TIMEOUT     EQU  (MAX_WAIT < 1000) ? MAX_WAIT : 1000  ' Clamp to 1000
```


## 2.10 Labels and Symbol Scoping

PASM2 supports two scoping levels for labels within DAT blocks: global labels and local labels. This scoping mechanism enables reuse of common label names (such as `loop`, `done`, `exit`) without naming collisions across different routines.

### 2.10.1 Global Labels

Global labels are defined by placing an identifier at the start of a line without any prefix character.

**Syntax:**
```pasm
labelname       instruction     operands        ' comment
```

Global labels have these characteristics:

- Visible throughout the entire DAT block
- Can be referenced from Spin2 code using `@labelname`
- Defining a new global label resets the local label scope
- Must begin with a letter (A-Z, a-z) or underscore (_)
- May contain letters, digits (0-9), and underscores
- Maximum length: 30 characters

**Example:**
```pasm
DAT             org

' Global labels - visible everywhere in DAT block
init_routine    mov     x, #0                   ' Routine entry point
                add     x, #1
                ret

data_table      long    $DEAD_BEEF              ' Data with global label
                long    $CAFE_BABE

math_helper     abs     x                       ' Another routine
                ret
```

### 2.10.2 Local Labels

Local labels are defined by prefixing an identifier with either a dot (`.`) or colon (`:`). Both prefix characters are functionally equivalent.

**Syntax:**
```pasm
.labelname      instruction     operands        ' comment
:labelname      instruction     operands        ' comment
```

Local labels have these characteristics:

- Visible only within the scope of the preceding global label
- Scope ends when the next global label is defined
- The same local name can be reused under different global labels
- Internally mangled by the compiler (e.g., `loop'0001`) for uniqueness
- Must begin with a letter or underscore after the prefix

**Example:**
```pasm
DAT             org

send_byte       rdbyte  x, ptr                  ' Global: send_byte
                call    #.wait                  ' Reference local .wait
.loop           testp   tx_pin          wc      ' Local: .loop (scope: send_byte)
        if_nc   jmp     #.loop
                wypin   x, tx_pin
.wait           testp   tx_pin          wc      ' Local: .wait (scope: send_byte)
        if_c    jmp     #.wait
                ret

recv_byte       testp   rx_pin          wc      ' Global: recv_byte
                                                '  (new scope begins)
        if_nc   jmp     #.wait                  ' This .wait is different from above
.wait           testp   rx_pin          wc      ' Local: .wait (scope: recv_byte)
        if_nc   jmp     #.wait
                rdpin   x, rx_pin
.loop           shr     x, #24                  ' Local: .loop (scope: recv_byte)
                ret
```

The example demonstrates how `.loop` and `.wait` can be reused in both `send_byte` and `recv_byte` without collision. Each global label creates a new local scope.

### 2.10.3 Label Reference Operators

PASM2 provides several operators for referencing labels in different contexts:

| Operator | Meaning | Context |
|----------|---------|---------|
| `#label` | Immediate value (COG address) | PASM instructions |
| `#.local` | Immediate reference to local label | PASM instructions |
| `#\label` | Absolute COG-relative address | Forces 9-bit COG address |
| `@label` | Hub address of label | Spin2 or PASM |
| `@@label` | Object-relative address | Spin2 or PASM |
| `$` | Current COG address | PASM (ORG mode) |
| `$$` | Current Hub address | PASM (ORGH mode) |

**Example:**
```pasm
DAT             org

routine         jmp     #.skip                  ' Jump to local label
                long    0
.skip           mov     x, #routine             ' Load address of global
                call    #\.helper               ' Absolute call to local
                ret

.helper         nop
                ret

' In ORGH (Hub) mode:
                orgh
hub_data        byte    "Hello", 0
hub_routine     long    @routine                ' Hub address of COG routine
```

### 2.10.4 Scope Boundary Rules

Three events create scope boundaries:

1. **Global label definition** — Starts a new local scope
2. **Storage directives** (BYTE, WORD, LONG, RES with a label) — Also start a new local scope
3. **End of DAT block** — Terminates all label scopes

**Example:**
```pasm
DAT             org

func_a          mov     x, #1                   ' Global: func_a, scope #1 begins
.loop           djnz    x, #.loop               ' Local .loop in scope #1

data_block      long    0, 0, 0, 0              ' Global: data_block,
                                                '  scope #2 begins

func_b          mov     y, #2                   ' Global: func_b,
                                                '  scope #3 begins
.loop           djnz    y, #.loop               ' Local .loop in scope #3
                                                '  (different)
.done           ret                             ' Local .done in scope #3
```

### 2.10.5 Best Practices

**Use descriptive global names** for routine entry points: `send_packet`, `init_uart`, `calc_crc`

**Use short local names** for flow control: `.loop`, `.done`, `.retry`, `.skip`, `.exit`

**Prefer dot notation** (`.label`) over colon notation (`:label`) for consistency with modern convention

**Keep local labels near their references** to improve readability

**Limit symbol names to 30 characters** for compatibility with the PNut compiler


```{=latex}
\begin{keyconcepts}
\item Every instruction is exactly 32 bits: 4-bit condition, 7-bit opcode, 3-bit flags, 9-bit D, 9-bit S
\item The EEEE condition field enables conditional execution based on C and Z flags
\item The I bit (position 18) determines whether S is a register address (0) or immediate value (1)
\item 9-bit immediates range 0-511; larger values require \#\# augmentation
\item AUGS/AUGD extend immediates to full 32 bits by inserting an extra instruction before the target
\item Encoding tables show both the bit pattern (left 5 columns) and the effects (right 4 columns)
\item Multiple table rows indicate instruction families or syntax variants with different encodings
\item The \_RET\_ condition (EEEE=0000) transforms any instruction into a subroutine return
\item Global labels are visible throughout a DAT block; local labels (.name or :name) are scoped to the preceding global label
\end{keyconcepts}
```


<!-- End of Chapter 2 -->

