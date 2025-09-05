# Complete Spin2 Operators Reference

## Operator Overview
Spin2 has 52 operators organized in 16 precedence levels, with additional floating-point variants.

---

## Operator Precedence Table (Complete)

### Priority Order (1 = highest, executes first)

| Priority | Operators | Type | Description | Block Usage |
|----------|-----------|------|-------------|-------------|
| **1** | `++` `--` `??` | Var-modify | Pre/post increment/decrement/random | All blocks |
| **2** | `!` `NOT` `-` `ABS` `\|\|` `^^` `ENCOD` `DECOD` `ONES` `SQRT` `QLOG` `QEXP` | Unary | Logic/math/encode operations | All blocks |
| **3** | `>>` `<<` `SAR` `ROR` `ROL` `REV` `ZEROX` `SIGNX` | Shift/Rotate | Bit manipulation | All blocks |
| **4** | `&` | Binary AND | Bitwise AND | All blocks |
| **5** | `^` | Binary XOR | Bitwise exclusive OR | All blocks |
| **6** | `\|` | Binary OR | Bitwise OR | All blocks |
| **7** | `*` `*.` | Multiply | Integer/float multiply | All blocks |
| **8** | `/` `/.` `//` `+/` | Divide | Divide/float/modulo/unsigned | All blocks |
| **9** | `+` `+.` | Add | Integer/float addition | All blocks |
| **10** | `-` `-.` | Subtract | Integer/float subtraction | All blocks |
| **11** | `#>` `<#` | Limit | Max/min limiting | All blocks |
| **12** | `<` `+<` `>` `+>` `<=` `+<=` `>=` `+>=` `<=>` `+<=>` | Comparison | Signed/unsigned compare | All blocks |
| **13** | `==` `<>` `===` `<>>` | Equality | Equal/not equal (logical/bitwise) | All blocks |
| **14** | `&&` `AND` `!&&` | Logical AND | Boolean AND/NAND | All blocks |
| **15** | `\|\|` `OR` `XOR` `!\|\|` | Logical OR | Boolean OR/XOR/NOR | All blocks |
| **16** | `? :` | Ternary | Conditional selection | PUB/PRI only |
| **Lowest** | `:=` `+=` `-=` `*=` `/=` `//=` `+/=` `#>=` `<#=` `&=` `\|=` `^=` `>>=` `<<=` `SAR=` `ROR=` `ROL=` `REV=` `ZEROX=` `SIGNX=` `AND=` `OR=` `XOR=` | Assignment | Store operations | PUB/PRI only |

---

## Operator Categories and Usage

### 1. Variable Modification Operators

#### Pre/Post Increment/Decrement
```spin2
++variable    ' Pre-increment: increment THEN use
variable++    ' Post-increment: use THEN increment
--variable    ' Pre-decrement: decrement THEN use
variable--    ' Post-decrement: use THEN decrement
```

#### Random Fill
```spin2
??variable    ' Fill with random value (pre)
variable??    ' Fill with random value (post)
```

**Block Usage**: All blocks (CON, PUB, PRI, DAT inline)

### 2. Unary Operators

#### Logical/Bitwise
```spin2
!expression   ' Logical NOT (0 becomes -1, non-zero becomes 0)
NOT expression ' Bitwise NOT (invert all bits)
```

#### Mathematical
```spin2
-expression   ' Negate
ABS(value)    ' Absolute value
SQRT(value)   ' Square root
```

#### Bit Operations
```spin2
||expression  ' Encode: convert to 0-32 bit position
^^expression  ' Decode: convert bit position to mask
ENCOD(value)  ' Find highest bit set (0-31)
DECOD(value)  ' Create mask from bit position
ONES(value)   ' Count number of 1 bits
```

#### CORDIC Functions
```spin2
QLOG(value)   ' Logarithm via CORDIC
QEXP(value)   ' Exponential via CORDIC
```

**Block Usage**: All blocks

### 3. Shift and Rotate Operators

```spin2
value >> count     ' Shift right (zero fill)
value << count     ' Shift left
value SAR count    ' Shift arithmetic right (sign extend)
value ROR count    ' Rotate right
value ROL count    ' Rotate left
value REV count    ' Reverse bits
value ZEROX count  ' Zero-extend from bit position
value SIGNX count  ' Sign-extend from bit position
```

**Block Usage**: All blocks

### 4. Bitwise Binary Operators

```spin2
a & b    ' Bitwise AND
a ^ b    ' Bitwise XOR
a | b    ' Bitwise OR
```

**Block Usage**: All blocks

### 5. Arithmetic Operators

#### Integer Operations
```spin2
a * b     ' Multiply
a / b     ' Divide (signed)
a // b    ' Modulo (remainder)
a +/ b    ' Unsigned divide
a + b     ' Add
a - b     ' Subtract
```

#### Floating-Point Operations
```spin2
a *. b    ' Float multiply
a /. b    ' Float divide
a +. b    ' Float add
a -. b    ' Float subtract
```

**Block Usage**: All blocks

### 6. Limit Operators

```spin2
a #> b    ' Maximum (limit minimum to b)
a <# b    ' Minimum (limit maximum to b)
```

Example:
```spin2
value := value #> 0 <# 100   ' Clamp value to 0..100 range
```

**Block Usage**: All blocks

### 7. Comparison Operators

#### Signed Comparisons
```spin2
a < b     ' Less than
a > b     ' Greater than
a <= b    ' Less than or equal
a >= b    ' Greater than or equal
a <=> b   ' Signed comparison (-1, 0, or 1)
```

#### Unsigned Comparisons (prefix with +)
```spin2
a +< b    ' Unsigned less than
a +> b    ' Unsigned greater than
a +<= b   ' Unsigned less than or equal
a +>= b   ' Unsigned greater than or equal
a +<=> b  ' Unsigned comparison (-1, 0, or 1)
```

**Block Usage**: All blocks

### 8. Equality Operators

```spin2
a == b    ' Equal (logical: returns -1 or 0)
a <> b    ' Not equal (logical: returns -1 or 0)
a === b   ' Bitwise equal (returns all bits of comparison)
a <>> b   ' Bitwise not equal (returns all bits of comparison)
```

**Block Usage**: All blocks

### 9. Logical Boolean Operators

```spin2
a && b    ' Logical AND
a AND b   ' Same as &&
a !&& b   ' Logical NAND

a || b    ' Logical OR
a OR b    ' Same as ||
a !|| b   ' Logical NOR

a XOR b   ' Logical XOR
```

**Block Usage**: All blocks

### 10. Ternary Conditional Operator

```spin2
condition ? true_value : false_value
```

Example:
```spin2
result := x > 0 ? x : -x    ' Absolute value using ternary
```

**⚠️ Block Usage**: PUB/PRI methods ONLY (not in CON or DAT)

### 11. Assignment Operators

#### Basic Assignment
```spin2
variable := expression    ' Assign (write-focused)
```

#### Compound Assignment
```spin2
variable += value     ' Add and assign
variable -= value     ' Subtract and assign
variable *= value     ' Multiply and assign
variable /= value     ' Divide and assign
variable //= value    ' Modulo and assign
variable +/= value    ' Unsigned divide and assign
variable #>= value    ' Max limit and assign
variable <#= value    ' Min limit and assign
variable &= value     ' AND and assign
variable |= value     ' OR and assign
variable ^= value     ' XOR and assign
variable >>= count    ' Shift right and assign
variable <<= count    ' Shift left and assign
variable SAR= count   ' Arithmetic shift right and assign
variable ROR= count   ' Rotate right and assign
variable ROL= count   ' Rotate left and assign
variable REV= count   ' Reverse bits and assign
variable ZEROX= pos   ' Zero-extend and assign
variable SIGNX= pos   ' Sign-extend and assign
variable AND= value   ' Logical AND and assign
variable OR= value    ' Logical OR and assign
variable XOR= value   ' Logical XOR and assign
```

**⚠️ Block Usage**: PUB/PRI methods ONLY (not in CON or DAT)

---

## Special Operator Behaviors

### Field Extraction Operators
```spin2
BYTE[address][index]    ' Access byte at address+index
WORD[address][index]    ' Access word at address+(index*2)
LONG[address][index]    ' Access long at address+(index*4)
REG[address][index]     ' Access cog register
```

**Block Usage**: PUB/PRI methods, DAT with some restrictions

### Address and Object Operators
```spin2
@variable           ' Get address of variable
@@variable          ' Get absolute hub address
@object.method      ' Get method pointer
\method()           ' Trap ABORT from method
```

**Block Usage**: 
- `@` - All blocks
- `@@` - PUB/PRI only
- `\` - PUB/PRI only

### Pin Field Operators
```spin2
pin ADDPINS count   ' Create pin field (base + additional pins)
pin1 ADDBITS pin2   ' OR pin masks together
```

Example:
```spin2
PINWRITE(56 ADDPINS 7, $FF)   ' Write to pins 56-63
```

**Block Usage**: PUB/PRI methods

---

## Block-Specific Limitations

### CON Block Restrictions
In CON blocks, only compile-time constant expressions allowed:
- ✅ All arithmetic operators
- ✅ All bitwise operators
- ✅ All shift/rotate operators
- ❌ NO assignment operators
- ❌ NO ternary operator
- ❌ NO runtime functions
- ❌ NO variable references

### DAT Block Restrictions
In DAT blocks, limited to data declarations:
- ✅ Constant expressions
- ✅ Address references with @
- ❌ NO assignment operators
- ❌ NO ternary operator
- ❌ NO method calls

### PUB/PRI Full Access
In PUB/PRI methods, ALL operators available:
- ✅ All operators
- ✅ Assignment operators
- ✅ Ternary operator
- ✅ Method calls
- ✅ Runtime expressions

---

## Operator Associativity

Most operators are **left-to-right associative**:
```spin2
a + b + c    ' Evaluates as (a + b) + c
a * b * c    ' Evaluates as (a * b) * c
```

Assignment operators are **right-to-left associative**:
```spin2
a := b := c := 0    ' Evaluates as a := (b := (c := 0))
```

---

## Special Notes

### The `:=` Philosophy
The `:=` operator emphasizes "write" over "equals":
- Reads as "gets" or "becomes"
- Distinguishes assignment from comparison
- Prevents `if (a = b)` mistakes (must use `==`)

### Floating-Point Operators
Float operators use dot suffix:
- `+.` `-.` `*.` `/.` for float operations
- Automatically handle IEEE-754 32-bit floats
- Can mix with integer operations (auto-conversion)

### Unsigned Operations
Prefix with `+` for unsigned:
- `+<` `+>` `+<=` `+>=` for unsigned comparison
- `+/` for unsigned division
- Important for values > $7FFFFFFF

### Precedence Override
Use parentheses to override precedence:
```spin2
result := a + b * c      ' b*c first, then add a
result := (a + b) * c    ' a+b first, then multiply by c
```

---

## Common Patterns

### Clamping Values
```spin2
value := value #> MIN_VAL <# MAX_VAL   ' Clamp to range
```

### Bit Manipulation
```spin2
mask := |< bit_position     ' Create single-bit mask
bits := value & $FF         ' Extract low byte
value |= mask               ' Set bits
value &= !mask              ' Clear bits
value ^= mask               ' Toggle bits
```

### Conditional Assignment
```spin2
result := flag ? true_val : false_val   ' Choose based on flag
direction := delta <=> 0                ' Get sign (-1, 0, 1)
```

---

This comprehensive operator reference covers all 52+ Spin2 operators, their precedence, usage contexts, and block-specific limitations.