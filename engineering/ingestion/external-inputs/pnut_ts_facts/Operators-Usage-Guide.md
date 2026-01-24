# Operators Usage Guide

## Overview

Spin2 provides a comprehensive set of operators for arithmetic, comparison, logical operations, bitwise manipulation, and specialized tasks. This guide documents all operators, their precedence, and correct usage patterns.

Operators fall into these categories:
- **Arithmetic** - Mathematical operations (+, -, *, /, //)
- **Comparison** - Value comparisons (==, <>, <, >, <=, >=, <=>)
- **Logical** - Boolean logic (AND, OR, XOR, NOT)
- **Bitwise** - Bit manipulation (&, |, ^, !, >>, <<)
- **Assignment** - Value assignment (:=) and compound forms (+=, -=)
- **Special** - Swap, random, sign extend, address operators

## Basic Usage

### Arithmetic Operations

```spin2
PUB calculate() | a, b, result
  a := 100
  b := 7

  result := a + b      ' Addition: 107
  result := a - b      ' Subtraction: 93
  result := a * b      ' Multiplication: 700
  result := a / b      ' Signed division: 14
  result := a // b     ' Remainder (modulo): 2
```

### Comparison Operations

```spin2
PUB check_bounds(value) : in_range
  if value >= 0 AND value <= 255
    in_range := TRUE
  else
    in_range := FALSE
```

### Bitwise Operations

```spin2
PUB set_flags() | flags
  flags := %0000_0001           ' Start with bit 0 set
  flags |= %0000_0100           ' Set bit 2: flags = %0000_0101
  flags &= !%0000_0001          ' Clear bit 0: flags = %0000_0100
  flags ^= %0000_1100           ' Toggle bits 2,3: flags = %0000_1000
```

## Operator Precedence

Spin2 has 15 precedence levels. Lower numbers bind tighter (evaluate first).

| Level | Operators | Category |
|-------|-----------|----------|
| 0 | `!` `-` `ABS` `ENCOD` `DECOD` `BMASK` `ONES` `SQRT` `QLOG` `QEXP` `NOT` | Unary |
| 1 | `>>` `<<` `SAR` `ROR` `ROL` `REV` `ZEROX` `SIGNX` | Shift/Rotate |
| 2 | `&` | Bitwise AND |
| 3 | `^` | Bitwise XOR |
| 4 | `\|` | Bitwise OR |
| 5 | `*` `/` `+/` `//` `+//` `SCA` `SCAS` `FRAC` | Multiply/Divide |
| 6 | `+` `-` | Add/Subtract |
| 7 | `#>` `<#` | Limit Min/Max |
| 8 | `ADDBITS` `ADDPINS` | Bit/Pin Fields |
| 9 | `<` `+<` `<=` `+<=` `==` `<>` `>=` `+>=` `>` `+>` `<=>` | Comparison |
| 10 | `!!` `NOT` | Logical NOT |
| 11 | `&&` `AND` | Logical AND |
| 12 | `^^` `XOR` | Logical XOR |
| 13 | `\|\|` `OR` | Logical OR |
| 14 | `? :` | Ternary |

### Precedence Example

```spin2
PUB precedence_demo() | result
  ' Without parentheses - multiplication binds tighter than addition
  result := 2 + 3 * 4           ' Result: 14 (not 20)

  ' Parentheses override precedence
  result := (2 + 3) * 4         ' Result: 20

  ' Comparison binds looser than arithmetic
  if value * 2 > threshold      ' Evaluates as: (value * 2) > threshold
    process()
```

## Arithmetic Operators

### Signed vs Unsigned Division

```spin2
PUB division_types() | signed_val, result
  signed_val := -100

  ' Signed division (default)
  result := signed_val / 7      ' Result: -14 (rounds toward zero)

  ' Unsigned division - treats operands as positive 32-bit values
  result := signed_val +/ 7     ' Result: 613566751 (interprets -100 as large positive)
```

The `+/` and `+//` operators treat both operands as unsigned 32-bit integers. Use them when working with addresses, pixel values, or other inherently positive quantities.

### Modulo (Remainder)

```spin2
PUB wrap_value(value, max) : wrapped
  ' Keep value within 0 to max-1 range
  wrapped := value // max

PUB is_even(n) : result
  result := (n // 2) == 0
```

### Scaling Operators

```spin2
PUB scale_sensor(raw_value) : scaled
  ' SCA: Unsigned scale (raw * multiplier) >> 32
  ' Useful for fixed-point math without overflow
  scaled := raw_value SCA $4000_0000   ' Multiply by 0.25

  ' SCAS: Signed scale
  scaled := raw_value SCAS $4000_0000
```

### FRAC - Fractional Division

```spin2
PUB high_precision_divide(a, b) : quotient, remainder
  ' FRAC gives high 32 bits of (a << 32) / b
  ' Useful for fixed-point arithmetic
  quotient := a / b
  remainder := a FRAC b
```

## Comparison Operators

### Standard Comparisons

| Operator | Meaning | Returns |
|----------|---------|---------|
| `==` | Equal | TRUE (-1) or FALSE (0) |
| `<>` | Not equal | TRUE (-1) or FALSE (0) |
| `<` | Less than (signed) | TRUE (-1) or FALSE (0) |
| `>` | Greater than (signed) | TRUE (-1) or FALSE (0) |
| `<=` | Less than or equal (signed) | TRUE (-1) or FALSE (0) |
| `>=` | Greater than or equal (signed) | TRUE (-1) or FALSE (0) |

### Unsigned Comparisons

```spin2
PUB compare_addresses(addr1, addr2) : result
  ' Addresses should be compared unsigned
  if addr1 +< addr2              ' Unsigned less than
    result := -1
  elseif addr1 +> addr2          ' Unsigned greater than
    result := 1
  else
    result := 0
```

Use `+<`, `+<=`, `+>`, `+>=` when comparing:
- Memory addresses
- Unsigned counters
- Values where the sign bit represents data, not sign

### Three-Way Comparison

```spin2
PUB compare(a, b) : relation
  ' <=> returns: -1 if a < b, 0 if a == b, +1 if a > b
  relation := a <=> b

  case relation
    -1: handle_less()
    0:  handle_equal()
    1:  handle_greater()
```

## Logical Operators

Logical operators treat any non-zero value as TRUE and return TRUE (-1) or FALSE (0).

```spin2
PUB logic_demo(a, b, c) : result
  ' AND - both must be true
  if a > 0 AND b > 0
    result := TRUE

  ' OR - either can be true
  if a > 0 OR b > 0
    result := TRUE

  ' XOR - exactly one must be true
  if a > 0 XOR b > 0
    result := TRUE

  ' NOT - inverts truth value
  if NOT a
    result := TRUE
```

### Symbol vs Keyword Forms

Both forms are equivalent:
- `&&` and `AND`
- `||` and `OR`
- `^^` and `XOR`
- `!!` and `NOT`

```spin2
' These are identical
if a && b
if a AND b

' These are identical
if a || b
if a OR b
```

## Bitwise Operators

### Basic Bitwise Operations

```spin2
PUB bitwise_demo() | a, b, result
  a := %1100_1010
  b := %1010_1010

  result := a & b       ' AND: %1000_1010
  result := a | b       ' OR:  %1110_1010
  result := a ^ b       ' XOR: %0110_0000
  result := !a          ' NOT: %0011_0101 (inverts all 32 bits)
```

### Shift and Rotate

```spin2
PUB shift_demo() | value, result
  value := %1100_0011

  ' Logical shifts - zeros fill vacated bits
  result := value >> 2        ' Right shift: %0011_0000
  result := value << 2        ' Left shift:  %0000_1100 (lower bits shown)

  ' Arithmetic right shift - sign bit fills
  value := $8000_0000         ' Negative number
  result := value SAR 4       ' Result: $F800_0000 (sign extended)

  ' Rotate - bits wrap around
  value := %1100_0011
  result := value ROR 2       ' Rotate right
  result := value ROL 2       ' Rotate left
```

### REV - Bit Reversal

```spin2
PUB reverse_bits(value, count) : reversed
  ' REV reverses the bottom 'count' bits, zeros the rest
  reversed := value REV count

  ' Example: reverse bottom 8 bits
  ' %1010_0011 REV 8 = %1100_0101
```

### ZEROX and SIGNX - Extension

```spin2
PUB extend_demo() | byte_val, result
  byte_val := $FF            ' 8-bit value with high bit set

  ' ZEROX - zero extend (treat as unsigned)
  result := byte_val ZEROX 7  ' Result: $0000_00FF

  ' SIGNX - sign extend (treat as signed)
  result := byte_val SIGNX 7  ' Result: $FFFF_FFFF (-1)
```

### ENCOD and DECOD

```spin2
PUB encode_decode_demo() | value, bit_pos
  ' ENCOD - find highest set bit position (0-31), returns 0 if input is 0
  value := %0000_1000
  bit_pos := ENCOD value      ' Result: 3

  ' DECOD - create value with single bit set at position
  value := DECOD 5            ' Result: %0010_0000 (32)

  ' Common pattern: create bit mask
  value := DECOD pin_number   ' Single bit for pin
```

### BMASK - Bit Mask Creation

```spin2
PUB mask_demo() | mask
  ' BMASK creates a mask with N+1 lowest bits set
  mask := BMASK 7             ' Result: %1111_1111 ($FF)
  mask := BMASK 3             ' Result: %0000_1111 ($0F)

  ' Useful for extracting bit fields
  value := (data >> 4) & BMASK 3   ' Extract 4 bits starting at bit 4
```

### ONES - Population Count

```spin2
PUB count_bits(value) : count
  ' ONES counts the number of 1 bits
  count := ONES value

  ' Example: ONES %1010_1010 = 4
```

## Limit Operators

### #> and <# - Clamp Values

```spin2
PUB clamp_demo(value) : clamped
  ' #> - limit minimum (force greater than or equal)
  clamped := value #> 0       ' If value < 0, returns 0

  ' <# - limit maximum (force less than or equal)
  clamped := value <# 255     ' If value > 255, returns 255

  ' Chain for both limits
  clamped := value #> 0 <# 255   ' Clamp to 0-255 range

PUB set_pwm(duty)
  ' Ensure duty cycle is valid
  duty := duty #> 0 <# 100
  apply_pwm(duty)
```

## Assignment Operators

### Basic Assignment

```spin2
PUB assign_demo() | a, b
  a := 10                     ' Simple assignment
  a, b := 10, 20              ' Multiple assignment
```

### Compound Assignment

All binary operators support compound assignment:

```spin2
PUB compound_demo() | value
  value := 10

  ' Arithmetic
  value += 5                  ' value := value + 5
  value -= 3                  ' value := value - 3
  value *= 2                  ' value := value * 2
  value /= 4                  ' value := value / 4
  value //= 3                 ' value := value // 3

  ' Bitwise
  value &= $FF                ' value := value & $FF
  value |= $100               ' value := value | $100
  value ^= $FF                ' value := value ^ $FF

  ' Shift
  value >>= 2                 ' value := value >> 2
  value <<= 1                 ' value := value << 1
  value SAR= 1                ' value := value SAR 1
  value ROR= 8                ' value := value ROR 8
  value ROL= 8                ' value := value ROL 8
```

### Swap Operator

```spin2
PUB swap_demo() | a, b
  a := 10
  b := 20

  a :=: b                     ' Swap values: a=20, b=10

  ' Useful for sorting
  if array[i] > array[j]
    array[i] :=: array[j]
```

## Special Operators

### ?? - Random Number

```spin2
PUB random_demo() | value
  ' ?? generates random number using hardware XORO32
  value := ??                 ' Get random 32-bit value

  ' Can also apply to variable (modifies and returns)
  value := 0
  value := ??value            ' Seed and get random

  ' Common pattern: random in range
  value := ?? // 100          ' Random 0-99
```

### ~ and ~~ - Sign Extend

```spin2
PUB sign_extend_demo() | byte_val, word_val
  byte_val := $FF
  word_val := $FFFF

  ' ~ sign extends from bit 7 (byte to long)
  byte_val := ~byte_val       ' Result: $FFFF_FFFF (-1)

  ' ~~ sign extends from bit 15 (word to long)
  word_val := ~~word_val      ' Result: $FFFF_FFFF (-1)

  ' Also used to clear variables
  byte_val~                   ' Sets byte_val to 0 and sign extends (result: 0)
```

### @ - Address Of

```spin2
VAR
  long buffer[100]

PUB address_demo() | ptr
  ptr := @buffer              ' Get hub address of buffer

  ' Pass buffer address to method
  fill_buffer(@buffer, 100)

PRI fill_buffer(addr, count) | i
  repeat i from 0 to count - 1
    long[addr][i] := 0
```

### @@ - Object Address Resolution

```spin2
DAT
  strings   word  @str1, @str2, @str3
  str1      byte  "First", 0
  str2      byte  "Second", 0
  str3      byte  "Third", 0

PUB get_string(index) : addr
  ' @ gives relative offset in DAT
  ' @@ resolves to actual hub address
  addr := @@strings[index]

  ' Now addr points to actual string in hub memory
  print_string(addr)
```

### ^@ - Object Base Plus Offset

```spin2
PUB base_offset_demo() | base, offset, addr
  ' ^@ adds offset to object base address
  ' Useful in child objects accessing parent data
  addr := ^@offset
```

### .. - Range Operator

Used in CASE statements and LOOKUP/LOOKDOWN:

```spin2
PUB range_demo(value) : category
  case value
    0..9:       category := DIGIT
    "A".."Z":   category := UPPER
    "a".."z":   category := LOWER
    OTHER:      category := OTHER_CHAR

PUB in_range(value, low, high) : result
  ' Using LOOKDOWN with range
  result := lookdown(value : low..high) > 0
```

### Bit Field Access with ..

```spin2
PUB bitfield_demo() | value, field
  value := $ABCD_1234

  ' Extract bits 15..8 (second byte)
  field := value.[15..8]      ' Result: $12

  ' Extract bits 7..0 (low byte)
  field := value.[7..0]       ' Result: $34

  ' Set a bit field
  value.[15..8] := $FF        ' value = $ABCD_FF34
```

### ? : - Ternary Operator

```spin2
PUB ternary_demo(condition) : result
  ' condition ? true_value : false_value
  result := condition ? 100 : 0

  ' Equivalent to:
  ' if condition
  '   result := 100
  ' else
  '   result := 0

  ' Can be chained (right-associative)
  result := a > b ? 1 : a < b ? -1 : 0
```

### ++ and -- - Increment/Decrement

```spin2
PUB inc_dec_demo() | value, result
  value := 10

  ' Pre-increment: increment first, then use
  result := ++value           ' value=11, result=11

  ' Post-increment: use first, then increment
  result := value++           ' result=11, value=12

  ' Same for decrement
  result := --value           ' value=11, result=11
  result := value--           ' result=11, value=10
```

## Floating-Point Operators

Spin2 supports IEEE-754 single-precision floats with dedicated operators (marked with `.` suffix):

```spin2
PUB float_demo() | f1, f2, result
  f1 := 3.14159
  f2 := 2.0

  ' Float arithmetic
  result := f1 +. f2          ' Float add
  result := f1 -. f2          ' Float subtract
  result := f1 *. f2          ' Float multiply
  result := f1 /. f2          ' Float divide

  ' Float comparisons
  if f1 >. f2
    process()

  ' Float functions
  result := FABS f1           ' Float absolute value
  result := FSQRT f1          ' Float square root
```

Note: The P2 has no hardware FPU. Float operations are performed by the Spin2 interpreter and are significantly slower than integer operations.

## Patterns

### Safe Division

```spin2
PUB safe_divide(a, b) : result
  ' Avoid division by zero
  if b == 0
    result := 0               ' Or return error value
  else
    result := a / b

  ' Alternative using ternary
  result := b ? a / b : 0
```

### Bit Manipulation Patterns

```spin2
PUB bit_patterns() | flags
  ' Set bit N
  flags |= DECOD N

  ' Clear bit N
  flags &= !DECOD N

  ' Toggle bit N
  flags ^= DECOD N

  ' Test bit N
  if flags & DECOD N
    bit_is_set()

  ' Extract N bits starting at position P
  field := (value >> P) & BMASK (N-1)
```

### Value Clamping

```spin2
PUB clamp(value, min_val, max_val) : clamped
  clamped := value #> min_val <# max_val

PUB wrap(value, max_val) : wrapped
  ' Keep value in 0 to max_val-1 range
  wrapped := value // max_val
  if wrapped < 0
    wrapped += max_val        ' Handle negative values
```

### Power of Two Operations

```spin2
PUB is_power_of_two(n) : result
  ' A power of 2 has exactly one bit set
  result := n > 0 AND ONES n == 1

PUB next_power_of_two(n) : result
  ' Round up to next power of 2
  result := DECOD ENCOD (n - 1)
```

## Anti-Patterns

### Precedence Mistakes

```spin2
' WRONG: Assumes left-to-right evaluation
if flags & MASK == EXPECTED     ' Compares MASK to EXPECTED first!

' CORRECT: Use parentheses
if (flags & MASK) == EXPECTED

' WRONG: Shift vs multiply precedence confusion
result := value << 2 + 1        ' Adds 1 then shifts!

' CORRECT: Parentheses make intent clear
result := (value << 2) + 1      ' Shift then add
result := value << (2 + 1)      ' Add then shift
```

### Signed vs Unsigned Confusion

```spin2
' WRONG: Using signed comparison for addresses
if addr1 < addr2                ' Fails if addresses cross $8000_0000

' CORRECT: Use unsigned comparison
if addr1 +< addr2

' WRONG: Using signed division for positive-only values
pixels := total_pixels / width  ' May give wrong result if total_pixels > $7FFF_FFFF

' CORRECT: Use unsigned division
pixels := total_pixels +/ width
```

### Integer Division Truncation

```spin2
' WRONG: Expecting floating-point result
average := (a + b) / 2          ' Integer division truncates

' CORRECT: Scale first for better precision
average := (a + b + 1) / 2      ' Round to nearest

' Or use explicit float if precision needed
average := (FLOAT(a) +. FLOAT(b)) /. 2.0
```

### Modifying Loop Variables

```spin2
' WRONG: Using compound assignment in REPEAT FROM loop
repeat i from 0 to 9
  i += 2                        ' Undefined behavior

' CORRECT: Use REPEAT WHILE for complex iteration
i := 0
repeat while i < 10
  ' ... work ...
  i += 2
```

### Bitwise vs Logical Confusion

```spin2
' WRONG: Using bitwise AND for logical test
if a & b                        ' True if ANY bits overlap

' CORRECT: Use logical AND for boolean conditions
if a AND b                      ' True if both non-zero

' WRONG: Using logical operators for bit manipulation
flags := a AND b                ' Returns -1 or 0, not bit intersection

' CORRECT: Use bitwise operators for bit manipulation
flags := a & b                  ' Actual bit intersection
```

## Summary Tables

### Arithmetic Operators

| Operator | Name | Example | Notes |
|----------|------|---------|-------|
| `+` | Add | `a + b` | |
| `-` | Subtract | `a - b` | |
| `*` | Multiply | `a * b` | |
| `/` | Divide (signed) | `a / b` | Rounds toward zero |
| `+/` | Divide (unsigned) | `a +/ b` | Treats operands as unsigned |
| `//` | Remainder | `a // b` | Modulo operation |
| `+//` | Remainder (unsigned) | `a +// b` | |
| `SCA` | Scale (unsigned) | `a SCA b` | (a * b) >> 32 |
| `SCAS` | Scale (signed) | `a SCAS b` | |
| `FRAC` | Fractional | `a FRAC b` | High bits of (a << 32) / b |

### Comparison Operators

| Operator | Meaning | Signed | Unsigned |
|----------|---------|--------|----------|
| `==` | Equal | Yes | - |
| `<>` | Not equal | Yes | - |
| `<` | Less than | Yes | `+<` |
| `<=` | Less or equal | Yes | `+<=` |
| `>` | Greater than | Yes | `+>` |
| `>=` | Greater or equal | Yes | `+>=` |
| `<=>` | Three-way compare | Yes | - |

### Bitwise Operators

| Operator | Name | Example |
|----------|------|---------|
| `&` | AND | `a & b` |
| `\|` | OR | `a \| b` |
| `^` | XOR | `a ^ b` |
| `!` | NOT | `!a` |
| `>>` | Shift right | `a >> n` |
| `<<` | Shift left | `a << n` |
| `SAR` | Arithmetic shift right | `a SAR n` |
| `ROR` | Rotate right | `a ROR n` |
| `ROL` | Rotate left | `a ROL n` |
| `REV` | Reverse bits | `a REV n` |
| `ZEROX` | Zero extend | `a ZEROX n` |
| `SIGNX` | Sign extend | `a SIGNX n` |

### Unary Operators

| Operator | Name | Example |
|----------|------|---------|
| `-` | Negate | `-a` |
| `!` | Bitwise NOT | `!a` |
| `!!` / `NOT` | Logical NOT | `NOT a` |
| `ABS` | Absolute value | `ABS a` |
| `ENCOD` | Encode (find MSB) | `ENCOD a` |
| `DECOD` | Decode (1 << n) | `DECOD n` |
| `BMASK` | Bit mask | `BMASK n` |
| `ONES` | Count ones | `ONES a` |
| `SQRT` | Square root | `SQRT a` |
| `QLOG` | Quaternary log | `QLOG a` |
| `QEXP` | Quaternary exp | `QEXP a` |

### Special Operators

| Operator | Name | Example | Notes |
|----------|------|---------|-------|
| `:=` | Assign | `a := b` | |
| `:=:` | Swap | `a :=: b` | Exchange values |
| `??` | Random | `??` or `??a` | XORO32 random |
| `~` | Sign extend byte | `a~` | From bit 7 |
| `~~` | Sign extend word | `a~~` | From bit 15 |
| `@` | Address of | `@var` | Hub address |
| `@@` | Object address | `@@ptr` | Resolve DAT pointer |
| `^@` | Base plus | `^@offset` | Object base + offset |
| `..` | Range | `0..9` | In CASE/LOOKUP |
| `? :` | Ternary | `a ? b : c` | Conditional |
| `++` | Increment | `++a` or `a++` | Pre/post |
| `--` | Decrement | `--a` or `a--` | Pre/post |

## Related Documentation

- [Control-Flow-Usage-Guide.md](Control-Flow-Usage-Guide.md) - IF, CASE, REPEAT with operator conditions
- [Floating-Point-Usage-Guide.md](Floating-Point-Usage-Guide.md) - Float operator details
- [Lookup-Table-Usage-Guide.md](Lookup-Table-Usage-Guide.md) - Range operator in LOOKUP/LOOKDOWN
