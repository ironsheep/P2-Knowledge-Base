# Spin2 v51 Grammar Reference

**Document Type**: Grammar and Syntax Reference  
**Created**: 2025-09-03  
**Sources**: v51 documentation + syntax highlighter developer insights  
**Purpose**: Complete grammar reference for code generation and validation

---

## 🎯 Language Fundamentals

### Data Types & Sizes
- **LONG**: 32-bit (4 bytes) - Primary unit
- **WORD**: 16-bit (2 bytes) 
- **BYTE**: 8-bit (1 byte)
- **All constants**: Always resolve to 32-bit values
- **Floating-point**: IEEE-754 32-bit when "." or "e" present

### Identifier Rules
- **Maximum length**: 32 characters
- **Case-insensitive**: `MyVar` = `myvar` = `MYVAR`
- **Valid characters**: Letters, digits, underscore (must start with letter or underscore)
- **Reserved words**: Cannot be used as identifiers

### Program Structure
- **Compilation root**: Topmost .spin2 file
- **Program entry**: First PUB method in topmost file
- **Object tree**: Follows OBJ references recursively
- **Block order**: Flexible, but at least one PUB required for Spin2 programs

---

## 📦 CON Block - Constants and Structures

### Syntax Grammar
```ebnf
con_block     ::= "CON" con_statement*
con_statement ::= constant_def | enumeration | struct_def | alignment

constant_def  ::= identifier "=" expression ["," identifier "=" expression]*
enumeration   ::= identifier ["," identifier]*
enum_control  ::= "#" [expression] ["[" expression "]"]
struct_def    ::= "STRUCT" identifier "(" member_list ")"
```

### Detailed Rules
```spin2
CON
  ' Direct assignments (always 32-bit result)
  MAX_SIZE = 100                           ' Decimal constant
  MASK = $FF00_FF00                       ' Hex with underscores
  BITS = %1010_1010                       ' Binary
  PI = 3.14159                            ' Float (IEEE-754)
  
  ' Expressions and operators
  DOUBLE = MAX_SIZE * 2                    ' Math expressions
  CONVERTED = FLOAT(42)                    ' Float conversion
  TRUNCATED = TRUNC(3.14)                  ' Truncate to integer
  
  ' Enumerations
  #0[1]                                    ' Start at 0, step by 1
  FIRST, SECOND, THIRD                    ' 0, 1, 2
  #10[5]                                   ' Start at 10, step by 5
  TENTH, FIFTEENTH, TWENTIETH              ' 10, 15, 20
  
  ' Structures (v44+)
  STRUCT point(LONG x, LONG y)
  STRUCT line(point start, point end)
  STRUCT data(BYTE flags[4], WORD count, LONG value)
```

### Key Insights
- **Multi-pass compiler**: Forward references work
- **Child object access**: Parent can reference child CON values AND structure definitions
- **Enumeration**: Base and step can be changed mid-sequence, step CAN be negative
- **Override mechanism**: Parameters in OBJ can override child CON values
- **CON scope**: ALL constants are public - no privacy control
- **Structure definitions**: ONLY allowed in CON blocks
- **ADDPINS operator**: Creates pin ranges (e.g., `base ADDPINS 7`)
- **ROUND() function**: Float-to-integer conversion in constants

---

## 🔗 OBJ Block - Object Instantiation

### Syntax Grammar
```ebnf
obj_block     ::= "OBJ" obj_statement*
obj_statement ::= [conditional] object_decl

object_decl   ::= identifier ["[" expression "]"] ":" string_literal ["|" param_list]
param_list    ::= param_assign ["," param_assign]*
param_assign  ::= identifier "=" expression
conditional   ::= "#ifdef" identifier | "#ifndef" identifier | "#endif"
```

### Detailed Rules
```spin2
OBJ
  ' Basic instantiation
  serial : "serial_driver"
  
  ' With parameter overrides (up to 16)
  display : "lcd_driver" | WIDTH = 320, HEIGHT = 240
  
  ' Object arrays (all share same parameters)
  sensors[8] : "sensor" | PIN_BASE = 0
  
  ' Conditional compilation (v48+)
  #ifdef DEBUG_MODE
    debug : "debug_terminal"
  #endif
```

### Key Insights
- **Array parameters**: All elements share the same parameter values
- **Uniqueness**: name + parameters = unique instance in memory
- **Deduplication**: Same object without overrides = single copy in memory
- **File search**: Current directory only (PNut), richer in other tools
- **Structure visibility**: Parent can see child's STRUCT definitions
- **Depth limit**: None, but total memory limit applies
- **Circular dependencies**: Detection uncertain, may not be significant

### Usage Patterns
```spin2
' Null method pattern for libraries
PUB null()  ' Empty - prevents library being run as main

' Accessing child members
serial.start(115200)              ' Call child method
value := sensor.THRESHOLD         ' Access child constant
type := sensor.structname         ' Access child structure definition
```

---

## 💾 VAR Block - Instance Variables

### Syntax Grammar
```ebnf
var_block     ::= "VAR" var_statement*
var_statement ::= type_decl var_list | alignment | mixed_decl

type_decl     ::= "BYTE" | "WORD" | "LONG" | struct_name | pointer_type
pointer_type  ::= "^BYTE" | "^WORD" | "^LONG" | "^" struct_name
var_list      ::= variable ["," variable]*
variable      ::= identifier ["[" expression "]"]
alignment     ::= "ALIGNW" | "ALIGNL"
mixed_decl    ::= type_decl var_list ["," type_decl var_list]*  ' v46+
```

### Detailed Rules
```spin2
VAR
  ' Basic declarations
  BYTE flag                                ' Single byte
  WORD count, total                       ' Multiple words
  LONG buffer[256]                        ' Array of longs
  
  ' Structure instances
  point position                          ' Structure variable
  line paths[10]                          ' Array of structures
  
  ' Pointers
  ^BYTE string_ptr                        ' Pointer to byte
  ^WORD data_ptrs[5]                      ' Array of pointers
  ^point location_ptr                     ' Pointer to structure
  
  ' Alignment
  BYTE a, b                               ' Bytes
  ALIGNW                                  ' Align to word boundary
  WORD c                                  ' Word aligned
  ALIGNL                                  ' Align to long boundary
  LONG d[100]                             ' Long aligned buffer
  
  ' Mixed types on one line (v46+)
  BYTE x, y, WORD p, q, LONG m, n, ^BYTE ptr
```

### Key Insights
- **Instance variables**: Each object instance gets unique VAR space
- **Initialization**: All zeroed on method entry (v37+)
- **Memory layout**: Compiler may optimize (long→word→byte) but not guaranteed
- **Arrays allowed**: Of any type including structures and pointers
- **Alignment**: Affects variables to the right on same line
- **Critical distinction**: VAR = instance, DAT = shared across all instances

### Pointer Mechanics (Complete)
```spin2
' Basic pointer operations
ptrvar              ' Access pointed-to variable (like regular variable)
ptrvar[++]          ' Access then post-increment pointer by type size
ptrvar[--]          ' Access then post-decrement pointer by type size
[++]ptrvar          ' Pre-increment pointer then access
[--]ptrvar          ' Pre-decrement pointer then access
[ptrvar]            ' Access the pointer itself (not what it points to)

' Critical: ++ and -- step by TYPE size automatically
' ^BYTE: steps by 1 byte
' ^WORD: steps by 2 bytes  
' ^LONG: steps by 4 bytes
' ^struct: steps by sizeof(struct) bytes

' Pointer assignment
[ptrvar] := @variable    ' Point to a variable
[ptrvar]++              ' Increment pointer by type size
[ptrvar]--              ' Decrement pointer by type size
```

---

## 🌍 PUB/PRI Blocks - Methods

### Syntax Grammar
```ebnf
method_block  ::= ("PUB" | "PRI") method_def method_body

method_def    ::= identifier "(" [param_list] ")" [":" result_list] ["|" local_list]
param_list    ::= parameter ["," parameter]* ' up to 127 parameters
result_list   ::= result ["," result]*       ' up to 15 results
local_list    ::= local ["," local]*         ' up to 64KB total

parameter     ::= [type_override] identifier
result        ::= [type_override] identifier  
local         ::= [type_override] identifier ["[" expression "]"]
type_override ::= "BYTE" | "WORD" | "LONG" | struct_name | pointer_type

method_body   ::= spin2_statement* | inline_pasm
inline_pasm   ::= ("ORG" pasm_code "END") | ("ORGH" pasm_code "END")
```

### Detailed Rules
```spin2
' Basic methods
PUB main()                              ' No params, no return
PRI helper(x)                           ' One parameter
PUB calculate(a, b) : result           ' Two params, one return
PRI process() | temp1, temp2           ' Local variables

' Complex signatures
PUB complex(p1, p2, p3) : r1, r2, r3 | local1, local2[10]
  ' Up to 127 parameters
  ' Up to 15 return values
  ' Up to 64KB of locals

' With type overrides
PUB data_handler(BYTE val, ^WORD ptr) : ^LONG result | point p
  ' BYTE parameter (promoted to long on stack)
  ' Pointer parameter
  ' Pointer return
  ' Structure local

' Inline assembly
PUB fast_operation() | x, y
  x := 10
  ORG                   ' Switch to cog assembly
    mov x, #5          ' First 16 locals available as registers
    add y, x           
  END                   ' Return to Spin2
  return y

PUB hub_operation() | a, b
  ORGH                  ' Hub assembly (v51+)
    ' Assembly executes from hub, not loaded to cog
  END
```

### Key Insights
- **Visibility**: PUB = public (parent accessible), PRI = private (internal only)
- **Entry point**: First PUB in topmost file = program start
- **Null pattern**: Empty PUB prevents library being run as main
- **Efficiency**: First 16 longs (params+results+locals) map to cog registers
- **Register access**: $1E0..$1EF contain first 16 longs for PASM access
- **Limits**: 127 params, 15 results, 64KB locals
- **Stack layout**: Parameters → Results → Locals (in declaration order)
- **Zero initialization**: Results and locals automatically zeroed on entry
- **Type overrides**: Apply only to the variable being declared
- **ORG vs ORGH**: ORG loads to cog RAM, ORGH executes from hub

---

## 📊 DAT Block - Data and PASM Code

### Syntax Grammar
```ebnf
dat_block     ::= "DAT" dat_statement*
dat_statement ::= [label] (data_def | pasm_inst | directive | file_inc)

label         ::= identifier | "." identifier | ":" identifier
data_def      ::= data_type data_list
data_type     ::= "BYTE" | "WORD" | "LONG" | "BYTEFIT" | "WORDFIT"
data_list     ::= data_item ["," data_item]*
data_item     ::= expression ["[" count "]"] | string_literal

directive     ::= "ORG" [address] | "ORGH" [address] | "ORGF" address | 
                  "FIT" address | "RES" count | "ALIGNW" | "ALIGNL"
file_inc      ::= "FILE" string_literal
```

### Detailed Rules
```spin2
DAT
  ' ORG directive modes
  ORG                     ' Cog mode, address 0 (no label allowed before)
  ORG  $100              ' Cog mode, specific address
  ORGH                    ' Hub mode, default $400 (no label before)
  ORGH $1000             ' Hub mode, specific address
  ORGF $040              ' Fill with zeros to address (no label before)
  FIT  $1F0              ' Verify fits in cog space
  
  ' Data declarations
  message    BYTE  "Hello, World", 0     ' String with terminator
  table      WORD  $1234[100]           ' Array, all initialized
  values     LONG  10, 20, 30, 40       ' Multiple values
  
  ' Safety checking
  small      BYTEFIT  $FF               ' Error if > 255
  medium     WORDFIT  $FFFF             ' Error if > 65535
  
  ' Labels and addressing
  global_label                           ' Global scope
  .local_label                           ' Local scope (dot prefix)
  :local_also                           ' Local scope (colon prefix)
  
  data       LONG  value                ' Value at label
  pointer    LONG  @data                ' Address of data
  absolute   LONG  @@data               ' Absolute address
  
  ' Alignment
  ALIGNW                                ' Align to word
  buffer     WORD  0[100]
  ALIGNL                                ' Align to long  
  longs      LONG  0[50]
  
  ' Reserved space
  RES        10                         ' Reserve 10 longs, no init
  
  ' File inclusion
  FILE       "image.bin"                ' Include binary file
  FILE       "font.dat"                 ' Common for resources
  
  ' PASM code
  ORG        0
  entry      mov   x, y                 ' Assembly instructions
             add   a, b
             jmp   #entry
  FIT        $1F0                       ' Must fit in cog
  
  ' Pointer arrays pattern
  strings    LONG  @msg1, @msg2, @msg3  ' For iteration
  msg1       BYTE  "First", 0
  msg2       BYTE  "Second", 0
  msg3       BYTE  "Third", 0
```

### ORG Variant Behaviors

#### ORG - Cog Addressing Mode
- Sets origin for cog RAM (512 longs, $000-$1FF)
- No symbol allowed before ORG directive
- Used for PASM code that loads into cog
- Limited space, use FIT to verify

#### ORGH - Hub Addressing Mode  
- Sets origin for hub RAM (512KB total)
- Default $400 if no address specified
- No symbol allowed before ORGH directive
- For hub-executed code or data
- Much larger space available

#### ORGF - Fill to Address
- Fills from current position to target with zeros
- No symbol allowed before ORGF directive
- Only valid in cog/LUT mode (not hub)
- Creates gaps for fixed-address code/data

### Key Insights
- **Shared memory**: DAT is "class variables" - all instances share
- **Mixed content**: Data, PASM code, binary files all together
- **Context-sensitive**: ORG/ORGH/FIT behave differently in PUB/PRI vs DAT
- **String convention**: Zero-terminated is dominant pattern
- **Pointer arrays**: Common pattern for iterating variable-length data
- **Label scoping**: Global by default, local with . or : prefix
- **No initialization**: RES reserves space without values
- **Address forms**: name (value), @name (relative), @@name (absolute)
- **Binary inclusion**: FILE directive includes entire file at compile time
- **Address resolution differs by program type**:
  - Spin2+PASM: Addresses are object-relative
  - PASM-only: Addresses are absolute

---

## 🔄 Context-Sensitive Keywords

### ORG/ORGH/END in Different Contexts

#### In PUB/PRI Methods (Inline Assembly)
```spin2
PUB method() | x, y
  ORG                    ' Must have END
    mov x, y
  END                    ' Required
  
  ORGH                   ' Must have END  
    ' hub assembly
  END                    ' Required
```

#### In DAT Blocks (Assembly/Data)
```spin2
DAT
  ORG  0                ' No END needed
    mov x, y            ' Continues until next directive
  
  ORGH $400            ' No END needed
    long values[100]   ' Continues until next directive
```

---

## ⚠️ Special Rules and Gotchas

### Order Dependencies
- First PUB in topmost file = entry point
- CON is default block if none specified
- Multi-pass compiler handles forward references (mostly)

### Memory Model
- VAR = instance variables (unique per object)
- DAT = class variables (shared across instances)
- First 16 method locals = cog registers (fast)
- Remaining locals = hub RAM (slower)

### Addressing Restrictions
- No labels before ORG, ORGH, ORGF directives
- @ = object-relative address
- @@ = absolute address fixup at runtime

### Size Limits
- Identifiers: 32 characters
- Parameters: 127 maximum
- Results: 15 maximum  
- Local variables: 64KB total
- Structure size: 64KB maximum
- Object parameters: 16 maximum
- Different child objects: 32 maximum per parent
- Object array size: 255 maximum instances
- Total child objects: 1024 maximum per parent

---

## 📝 Grammar Evolution Notes

### Verified Through Documentation Review
- ✅ Enumeration step CAN be negative (example: `#-1[-1]`)
- Memory layout: Compiler does NOT optimize - declaration order matters
- ADDPINS operator for pin ranges (special operator)
- ROUND() function for float-to-int in constants

### Program Type Distinction
| Block | Spin2+PASM Programs | PASM-only Programs |
|-------|--------------------|-----------------|
| **CON** | Permitted | Permitted |
| **OBJ** | Permitted | **Not Allowed** |
| **VAR** | Permitted | **Not Allowed** |
| **PUB** | **Required** | **Not Allowed** |
| **PRI** | Permitted | **Not Allowed** |
| **DAT** | Permitted | **Required** |

- **Spin2+PASM**: Requires at least one PUB, bytecode interpreter loaded
- **PASM-only**: No PUB/PRI/OBJ/VAR allowed, pure assembly, no interpreter overhead

### Still To Verify
- Are circular object dependencies detected?
- Complete operator precedence table (15 levels)
- All valid operators in constant expressions

### Version-Specific Features
- v37: Object parameterization
- v44: Structures (revised in v45)
- v46: Mixed VAR declarations, DEBUG gating
- v47: Cooperative multitasking (TASK*)
- v48: Preprocessor (#ifdef, etc.)
- v51: ORGH in PUB/PRI methods

---

*This grammar reference combines official documentation with syntax highlighter implementation insights.*