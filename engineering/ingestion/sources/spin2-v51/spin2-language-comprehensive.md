# Spin2 Language - Comprehensive Reference

## Critical: Whitespace and Indentation Rules

### The Golden Rule
**Left-edge whitespace (indentation) determines code structure in Spin2**

Key principles:
1. **Consistency matters, not tabs vs spaces** - Can use either, but be consistent
2. **Relative indentation defines scope** - Code at same indent level is in same scope
3. **Indented lines belong to the construct above** - Like Python
4. **Multiple indentation levels under one construct can be misinterpreted** - Keep it simple

### Indentation Examples
```spin2
IF cog                           ' Condition at base level
  COGSTOP(cog-1)                ' Indented = controlled by IF
  PINCLEAR(av_base_pin ADDPINS 4)  ' Same indent = also controlled by IF

REPEAT count                     ' Loop construct
  doSomething()                  ' Indented = inside loop
  doMore()                       ' Same indent = also inside loop
done()                           ' Back to base = outside loop
```

### Warning About Multiple Levels
```spin2
' AVOID THIS - Can be misinterpreted:
IF condition
  doFirst()
    doNested()      ' Double indentation under IF - problematic!
    
' PREFER THIS - Clear structure:
IF condition
  doFirst()
  doSecond()        ' Single level of indentation
```

## Comments

### Comment Types

| Type | Syntax | Description | Documentation? |
|------|--------|-------------|----------------|
| Single-line | `'` | Rest of line ignored | No |
| Doc single-line | `''` | Rest of line ignored | Yes |
| Block | `{ }` | Everything within braces ignored | No |
| Doc block | `{{ }}` | Everything within double braces ignored | Yes |
| Line continuation | `...` | Rest of line ignored, parsing continues on next line | No |

### Examples
```spin2
a := 0  ' Simple comment
b := 1  '' Documentation comment (goes to doc file)

x := 4, {inline comment} y := 5

{ Multi-line
  block comment }

{{ Documentation
   block comment }}

z := 100 ...  comment here
  * x    ...  more comment
  - w         ' Continues as single expression
```

## Constants

### Numeric Formats

| Format | Prefix | Example | Description |
|--------|--------|---------|-------------|
| Decimal | none | `123`, `3_000_000` | Base 10, underscores allowed |
| Hexadecimal | `$` | `$FF`, `$DEAD_BEEF` | Base 16 |
| Binary | `%` | `%1010`, `%1111_0000` | Base 2 |
| Quaternary | `%%` | `%%0123`, `%%33_22_11_00` | Base 4 |
| Float | decimal point or `e` | `1.0`, `1e9`, `-1.23e-7` | IEEE-754 32-bit |

### Character/String Constants

| Format | Syntax | Example | Result |
|--------|--------|---------|--------|
| Character | `"c"` | `"A"` | `$41` (8-bit ASCII) |
| String | `"str"` | `"Hello"` | `$48, $65, $6C, $6C, $6F` |
| Packed | `%"str"` | `%"ABCD"` | `$44_43_42_41` (little-endian, max 4 chars) |

## Variables

### Variable Types and Scope

| Type | Location | Scope | Notes |
|------|----------|-------|-------|
| VAR | Hub RAM | Instance | Each object instance has its own |
| DAT | Hub RAM | Shared | All instances share same data |
| Local | Hub RAM | Method | PUB/PRI parameters, returns, locals |
| Registers | Cog RAM | Cog | PR0-PR7, IJMP1-3, IRET1-3, etc. |

### Permanent Variables

| Variable | Address | Description | Spin2 | PASM |
|----------|---------|-------------|-------|------|
| CLKMODE | $00040 | Clock mode settings | Yes | Yes |
| CLKFREQ | $00044 | System frequency | Yes | Yes |
| VARBASE | +0 | Base of VAR space | Maybe | No |
| PR0-PR7 | $1D8-$1DF | Parameter registers | Yes | Yes |
| PTRA/PTRB | $1F8-$1F9 | Pointer registers | No | Yes |
| INA/INB | $1FE-$1FF | Input pin states | Yes | Yes |
| OUTA/OUTB | $1FC-$1FD | Output pin states | Yes | Yes |
| DIRA/DIRB | $1FA-$1FB | Pin directions | Yes | Yes |

## Data Types and Sizes

### Size Prefixes

| Prefix | Size | Range | Memory Step |
|--------|------|-------|-------------|
| BYTE | 8 bits | 0-255 (unsigned) | 1 |
| WORD | 16 bits | 0-65535 (unsigned) | 2 |
| LONG | 32 bits | Full 32-bit range | 4 |

### Variable Declaration Examples
```spin2
VAR
  BYTE  myByte                  ' Single byte
  WORD  myWords[10]             ' Array of 10 words
  LONG  buffer[256]             ' Array of 256 longs
  
  BYTE  name[32]                ' String buffer
  WORD  samples[1000]           ' Data samples
  LONG  stackSpace[64]          ' Stack for cog
```

## Operators (Overview)

### Operator Categories

1. **Var-Prefix Operators** (`++var`, `--var`, `??var`)
2. **Var-Postfix Operators** (`var++`, `var--`, `var??`)
3. **Unary Operators** (`-`, `!`, `NOT`, `ABS`, `||`, etc.)
4. **Binary Operators** (`+`, `-`, `*`, `/`, `<<`, `>>`, etc.)
5. **Ternary Operator** (`condition ? true_val : false_val`)
6. **Assignment Operators** (`:=`, `+=`, `-=`, etc.)
7. **Floating-Point Operators** (`+.`, `-.`, `*.`, `/.`)

### Operator Precedence (Priority)

Higher priority operators evaluate first:

1. **Priority 1**: Pre/post increment/decrement (`++`, `--`, `??`)
2. **Priority 2**: Unary operators (`-`, `!`, `||`, etc.)
3. **Priority 3-15**: Binary operators (multiplication before addition, etc.)
4. **Priority 16**: Ternary operator (`? :`)
5. **Lowest**: Assignment operators (`:=`, `+=`, etc.)

## Method Calls and Parameters

### Method Definition
```spin2
PUB methodName(param1, param2, param3) : returnValue | local1, local2
  ' Method body
  returnValue := calculation
  
PRI privateMethod() | temp
  ' Private method body
```

### Special Method Parameters

- **First 16 local variables** map to cog registers $1E0-$1EF for speed
- Parameters are passed by value
- Arrays/strings passed by reference (address)
- Maximum 127 parameters
- Maximum 15 return values

## Flow Control

### Core Constructs

All use **indentation** to determine scope:

1. **IF/IFNOT/ELSEIF/ELSEIFNOT/ELSE** - Conditional execution
2. **CASE/CASE_FAST** - Multi-way branching
3. **REPEAT** - Looping with multiple forms

### IF Constructs
```spin2
IF condition
  ' Execute if condition is non-zero
  doSomething()
ELSEIF otherCondition
  ' Execute if first was zero, this is non-zero
  doOtherThing()
ELSE
  ' Execute if all conditions were zero
  doDefault()

IFNOT condition  ' Execute if condition IS zero
  handleZeroCase()
```

### CASE Constructs
```spin2
CASE value
  1: handleOne()
  2, 3: handleTwoOrThree()
  4..10: handleRange()
  OTHER: handleDefault()

CASE_FAST value   ' Optimized for speed, limited range
  0: handle0()
  1: handle1()
```

### REPEAT Constructs
```spin2
REPEAT               ' Infinite loop
  doForever()
  
REPEAT count         ' Fixed iterations
  doNTimes()
  
REPEAT WHILE condition   ' While condition true
  keepGoing()
  
REPEAT UNTIL condition   ' Until condition true
  keepTrying()
  
REPEAT variable FROM start TO end  ' Count up/down
  processIndex(variable)
  
REPEAT variable FROM start TO end STEP 2  ' With step
  processEveryOther(variable)
```

## Special Keywords in Loops

- **NEXT** - Skip to next iteration
- **QUIT** - Exit loop entirely
- **RETURN** - Exit entire method
- **ABORT** - Exit with optional value

## Memory Access

### Direct Memory Access
```spin2
BYTE[address] := value          ' Write byte
value := WORD[address]          ' Read word  
LONG[address] += 10             ' Modify long

' Array style
BYTE[base][index] := value      ' Indexed access
```

### Special Memory Operations
```spin2
BYTEFILL(address, value, count)  ' Fill memory with byte
WORDMOVE(dest, source, count)    ' Copy words
LONGMOVE(dest, source, count)    ' Copy longs
```

## Key Language Insights

1. **Indentation is semantic** - Not just style, it determines program structure
2. **Everything is 32-bit** internally - BYTE/WORD are storage optimizations
3. **Pointer arithmetic is type-aware** - Increments by type size
4. **Methods are not reentrant** by default - Single execution context
5. **First 16 locals are fast** - Mapped to cog registers
6. **Symbols can exceed 32 chars** in practice (compiler accepts, docs say 32)
7. **Underscores allowed** in symbol names (including prefix)

## Common Patterns

### Pin Operations
```spin2
PINH(pin)                       ' Set pin high
PINL(pin)                       ' Set pin low
PINT(pin)                       ' Toggle pin
PINR(pin)                       ' Read pin state
```

### Cog Management
```spin2
cogid := COGINIT(COGEXEC_NEW, @code, @params)
COGSTOP(cogid)
```

### Timing
```spin2
WAITMS(milliseconds)
WAITUS(microseconds)
start := GETCT()
elapsed := GETCT() - start
```

## Method Pointers

### Creating Method Pointers
```spin2
VAR
  LONG methodPtr
  
PUB main()
  methodPtr := @someMethod      ' Get pointer to method
  methodPtr := @object.method   ' Pointer to object's method
  
  ' Call through pointer
  result := methodPtr(params)   ' Indirect call
```

### Key Points
- Method pointers are LONG values
- Use `@` without parentheses to get pointer
- Call with parentheses like normal method

## ABORT Mechanism

### Trap and Handle
```spin2
PUB caller()
  result := \calledMethod()    ' Backslash traps ABORT
  ' If ABORT occurs, result contains abort value
  ' If no ABORT, result is 0
  
PUB calledMethod()
  if error
    ABORT errorCode            ' Instantly return to caller with \
```

### ABORT Rules
1. `\` before method call traps any ABORT
2. ABORT with value returns that value to trapper
3. Untrapped ABORT stops the cog
4. Can return from any call depth instantly

## String Handling

### String Methods
```spin2
STRSIZE(addr)                  ' Count bytes in zero-terminated string
STRCOMP(addrA, addrB)          ' Compare strings, -1 if match, 0 if not
STRCOPY(dest, source, max)     ' Copy string with max length

@"Hello"                       ' Get address of string literal
STRING("Text", 13)            ' Create string with values
LSTRING("Text")                ' Length-headed string
```

## Critical Implementation Details

### Whitespace Rules Summary
1. **Indentation depth matters** - Defines block membership
2. **Tabs vs spaces doesn't matter** - Just be consistent
3. **Same indent = same scope** - All at same level are siblings
4. **Increased indent = child scope** - Belongs to construct above
5. **Decreased indent = exit scope** - Back to parent level

### Method Execution Context
1. **Not reentrant by default** - Each method has single context
2. **First 16 locals in cog registers** - Fast access via $1E0-$1EF
3. **Stack-based parameter passing** - Hub RAM based
4. **127 parameter limit** - Compiler enforced
5. **15 return value limit** - Multiple returns supported

### Memory Architecture
1. **Hub RAM** - Shared between all cogs, where Spin2 executes
2. **Cog RAM** - Private to each cog, 512 longs
3. **LUT RAM** - 512 longs, dual-port, **shared between adjacent cog pairs** (0-1, 2-3, 4-5, 6-7)
4. **Special registers** - INA/INB, OUTA/OUTB, DIRA/DIRB at top of cog RAM

#### LUT RAM Sharing (Critical for Inter-Cog Communication)
- **Cog pairs share LUT**: Cogs 0-1, 2-3, 4-5, 6-7
- **Enables fast communication** between paired cogs without hub RAM
- **Very useful for parallel processing** - paired cogs can work on larger shared datasets
- **No hub RAM bottleneck** - Direct cog-to-cog data sharing
- **Example use case**: One cog produces data, paired cog consumes it via shared LUT

## Operator Precedence Complete Table

### Priority Order (1 = highest)

| Pri | Operators | Type | Description |
|-----|-----------|------|-------------|
| 1 | `++` `--` `??` (pre/post) | Var-modify | Inc/dec/random |
| 2 | `!` `NOT` `-` `ABS` `\|\|` `^^` | Unary | Logic/math/encode |
| 3 | `>>` `<<` `SAR` `ROR` `ROL` `REV` | Shift/rotate | Bit manipulation |
| 4 | `&` | Binary AND | Bitwise |
| 5 | `^` | Binary XOR | Bitwise |
| 6 | `\|` | Binary OR | Bitwise |
| 7 | `*` `*.` | Multiply | Integer/float |
| 8 | `/` `/.` `//` `+/` | Divide | Various forms |
| 9 | `+` `+.` | Add | Integer/float |
| 10 | `-` `-.` | Subtract | Integer/float |
| 11 | `#>` `<#` | Limit max/min | Bounds |
| 12 | `<` `>` `<=` `>=` | Comparison | Relations |
| 13 | `==` `<>` | Equality | Compare |
| 14 | `&&` `AND` | Logical AND | Boolean |
| 15 | `\|\|` `OR` `XOR` | Logical OR/XOR | Boolean |
| 16 | `? :` | Ternary | Conditional |
| Low | `:=` `+=` `-=` etc. | Assignment | Store |

## Built-In Method Categories

### Hub Control
- `COGINIT` / `COGSTOP` - Cog management
- `COGSPIN` - Start Spin2 method in cog
- `COGATN` - Cog attention signaling
- `POLLATN` / `WAITATN` - Attention handling

### Pin Control  
- `PINH` / `PINL` / `PINT` - Basic pin control
- `PINW` / `PINR` - Pin write/read
- `PINFLOAT` / `PINMODE` - Pin configuration
- `WRPIN` / `WXPIN` / `WYPIN` - Smart pin control

### Timing
- `GETCT` - Get system counter
- `WAITMS` / `WAITUS` - Delay milliseconds/microseconds
- `WAITX` - Wait clock cycles
- `POLLCT` / `WAITCT` - Counter polling/waiting

### Math
- `MULDIV64` - 64-bit intermediate multiply/divide
- `ROTXY` / `POLXY` - Coordinate rotation
- `XYPOL` - Cartesian to polar
- `QSIN` / `QCOS` - CORDIC trig functions
- `QLOG` / `QEXP` - CORDIC log/exp

### Memory
- `BYTEMOVE` / `WORDMOVE` / `LONGMOVE` - Block copy
- `BYTEFILL` / `WORDFILL` / `LONGFILL` - Block fill
- `LOOKUP` / `LOOKUPZ` - Table lookup
- `LOOKDOWN` / `LOOKDOWNZ` - Reverse lookup

## Flow Control Details

### CASE_FAST Limitations
- Values must be in 0..255 range
- Optimized jump table implementation
- No OTHER clause allowed
- All cases must be explicit

### REPEAT FROM..TO Direction
```spin2
REPEAT i FROM 0 TO 10    ' Counts UP: 0,1,2...10
REPEAT i FROM 10 TO 0    ' Counts DOWN: 10,9,8...0
' Direction auto-detected based on start vs end
```

### REPEAT WITH Multiple Variables
```spin2
REPEAT 10 WITH i  ' i gets 1..10
  ' Use i here
  
REPEAT WHILE flag WITH counter  ' counter increments each loop
  ' Automatic loop counter
```

## Lessons Learned from Testing

1. **Symbol length limit is soft** - Compiler accepts >32 chars despite docs
2. **Underscores work everywhere** - `_private` symbols compile fine
3. **Error m280 is non-blocking** - "Expected end of line" but still compiles
4. **Symbols aren't truncated** - 35-char symbols with same 32-char prefix remain distinct
5. **Highlighter follows spec** - Correctly warns at >32 chars per documentation
