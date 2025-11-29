# Q Instructions — CORDIC Coprocessor Operations

The P2 Propeller includes a dedicated CORDIC (COordinate Rotation DIgital Computer) coprocessor that performs high-precision mathematical operations. The Q* instruction family queues operations to this 54-stage pipelined coprocessor, enabling sophisticated calculations while the cog continues executing other instructions.

## CORDIC Operation Model

All Q* instructions follow a queue-based operation model:

1. **Queue Operation**: Q* instructions (QMUL, QDIV, etc.) start a computation but do not wait for the result
2. **54-Cycle Latency**: All CORDIC operations take 54 clock cycles to complete
3. **Result Retrieval**: Use GETQX and GETQY to retrieve results 55 clocks after issuing the Q* instruction
4. **Pipelining**: Multiple operations can be queued while waiting for results (one per hub window, every 8 clocks)
5. **Extended Operands**: Some operations use SETQ to provide additional 32-bit input data

This pipelined architecture enables high-throughput mathematical processing by overlapping computation with other work.

---

## QDIV — CORDIC Solver

Perform 64÷32 unsigned division with 32-bit quotient and remainder.

### Syntax
```pasm
        QDIV    {#}D,{#}S
```

### Result
Divides a 64-bit numerator by a 32-bit denominator, producing both a 32-bit quotient (retrieved via GETQX) and a 32-bit remainder (retrieved via GETQY) 55 clocks later.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Lower 32 bits of 64-bit numerator |
| S | 32-bit denominator (divisor) |
| SETQ | Upper 32 bits of 64-bit numerator (optional, defaults to 0 if not used) |

### Encoding
\simpleencoding{EEEE | 1101000 1LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2...9}

### Related Instructions
- [GETQX](#getqx) — Retrieve quotient result
- [GETQY](#getqy) — Retrieve remainder result
- [SETQ](#setq) — Set upper 32 bits of numerator
- [QFRAC](#qfrac) — Fractional division with reversed operand order
- [QMUL](#qmul) — CORDIC multiplication

### Explanation
The QDIV instruction performs high-precision unsigned division using the P2's 54-stage pipelined CORDIC solver. It divides a 64-bit numerator by a 32-bit denominator, producing both a 32-bit quotient and 32-bit remainder.

The 64-bit numerator is formed by concatenating the SETQ value (or 32'b0 if SETQ not used) as the upper 32 bits with the D operand as the lower 32 bits: {SETQ, D}. The denominator is specified in the S operand. After 55 clocks, the quotient can be retrieved using GETQX and the remainder using GETQY.

The optional SETQ instruction allows for true 64-bit division when high precision is required, while omitting SETQ effectively performs 32-bit division (equivalent to {0, D} / S). This instruction is essential for precise arithmetic operations where full 64-bit precision is needed in the dividend, such as fixed-point mathematics, scaling operations, and algorithms requiring exact division results without precision loss.

**Simple 32-bit division example (1000000 ÷ 3 = 333333 remainder 1):**
```pasm
        QDIV    #1000000, #3   ' No SETQ, so {0, 1000000} / 3
        ' Wait 55 clocks...
        GETQX   quotient       ' Get 333333
        GETQY   remainder      ' Get 1
```

**Full 64-bit division example:**
```pasm
        SETQ    #$12345678     ' Set upper 32 bits
        QDIV    #$9ABCDEF0, #1000  ' {SETQ, D} / S
        ' ... other work for 55 clocks ...
        GETQX   big_quotient
        GETQY   big_remainder
```

Division by zero produces undefined results. Each cog can issue one CORDIC instruction per hub window (every 8 clocks), allowing pipelined mathematical operations.

---

## QEXP — CORDIC Solver

Convert 5:27-bit logarithm to 32-bit unsigned integer.

### Syntax
```pasm
        QEXP    {#}D
```

### Result
Converts a 5:27-bit logarithm format into a 32-bit unsigned integer (exponential result), retrieved via GETQX 55 clocks later.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | 5:27-bit logarithm (5-bit whole exponent in bits [31:27], 27-bit fractional exponent in bits [26:0]) |

### Encoding
\simpleencoding{EEEE | 1101011 00L | DDDDDDDDD | 000001111 | — | — | — | 2...9}

### Related Instructions
- [GETQX](#getqx) — Retrieve exponential result
- [QLOG](#qlog) — Convert integer to logarithm
- [QMUL](#qmul) — CORDIC multiplication for logarithmic scaling

### Explanation
The QEXP instruction performs logarithm to integer conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 5:27-bit logarithm format into a 32-bit unsigned integer, effectively computing the exponential (antilog) of the input.

The instruction takes the logarithm value in the D operand, which must be in P2's 5:27 format where bits [31:27] contain the 5-bit whole exponent and bits [26:0] contain the 27-bit fractional exponent. After 55 clocks, the integer result can be retrieved using the GETQX instruction.

This instruction is the complement of QLOG and is commonly used together with QLOG to perform power calculations, exponential functions, and other mathematical operations requiring logarithmic scaling. The high precision of the 5:27 format allows for accurate exponential calculations across a wide range of input values, making it suitable for signal processing, mathematical modeling, and scientific computations.

**Basic logarithm to integer conversion:**
```pasm
        QEXP    log_value      ' Begin exponential conversion
        ' Wait 55 clocks...
        GETQX   integer_result ' Get 32-bit integer
```

**Power calculation using log/exp (result = base^exponent):**
```pasm
        QLOG    base          ' Convert base to log
        ' ... wait 55 clocks ...
        GETQX   log_base
        QMUL    log_base, exponent  ' Multiply log by exponent
        ' ... wait 55 clocks ...
        GETQX   log_result
        QEXP    log_result    ' Convert back to integer
        ' ... wait 55 clocks ...
        GETQX   power_result
```

The input must be in 5:27 logarithmic format as produced by QLOG. QEXP is the complementary operation to QLOG, enabling sophisticated power and exponential calculations.

---

## QFRAC — CORDIC Solver

Perform 64÷32 unsigned fractional division with D as upper 32 bits.

### Syntax
```pasm
        QFRAC   {#}D,{#}S
```

### Result
Divides a 64-bit numerator by a 32-bit denominator, producing both a 32-bit quotient (retrieved via GETQX) and a 32-bit remainder (retrieved via GETQY) 55 clocks later.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Upper 32 bits of 64-bit numerator (integer portion) |
| S | 32-bit denominator (divisor) |
| SETQ | Lower 32 bits of 64-bit numerator (fractional portion, optional, defaults to 0 if not used) |

### Encoding
\simpleencoding{EEEE | 1101001 0LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2...9}

### Related Instructions
- [GETQX](#getqx) — Retrieve quotient result
- [GETQY](#getqy) — Retrieve remainder result
- [SETQ](#setq) — Set lower 32 bits of numerator
- [QDIV](#qdiv) — Standard division with reversed operand order
- [QMUL](#qmul) — CORDIC multiplication

### Explanation
The QFRAC instruction performs fractional division using the P2's 54-stage pipelined CORDIC solver. It divides a 64-bit numerator by a 32-bit denominator, but differs from QDIV in the operand arrangement: D forms the upper 32 bits while SETQ (or 32'b0) forms the lower 32 bits.

The 64-bit numerator is formed by concatenating the D operand as the upper 32 bits with the SETQ value (or 32'b0 if SETQ not used) as the lower 32 bits: {D, SETQ}. This arrangement makes QFRAC particularly suitable for fractional arithmetic where the integer part is in D and the fractional part is in SETQ.

After 55 clocks, the quotient can be retrieved using GETQX and the remainder using GETQY. This instruction is essential for fixed-point mathematics, fractional scaling operations, and algorithms where the dividend's integer portion needs to be preserved in the primary operand.

The key difference from QDIV is the bit arrangement: QFRAC uses {D, SETQ} while QDIV uses {SETQ, D}, making QFRAC more natural for fractional operations where D represents the whole number portion.

**Fractional number division (5.75 ÷ 2):**
```pasm
        SETQ    #$C0000000     ' 0.75 in 32-bit fraction format
        QFRAC   #5, #2         ' {5, 0.75} / 2 = 2.875
        ' Wait 55 clocks...
        GETQX   quotient       ' Get integer quotient
        GETQY   remainder      ' Get fractional remainder
```

**Simple fractional scaling without SETQ (D.0 format):**
```pasm
        QFRAC   #1000, #3      ' {1000, 0} / 3 = 333 remainder 1
        ' ... other work for 55 clocks ...
        GETQX   scaled_result
        GETQY   leftover
```

Use SETQ before QFRAC to specify the fractional part. Without SETQ, the lower 32 bits default to 0. Division by zero produces undefined results.

---

## QLOG — CORDIC Solver

Convert 32-bit unsigned integer to 5:27-bit logarithm format.

### Syntax
```pasm
        QLOG    {#}D
```

### Result
Converts a 32-bit unsigned integer into a 5:27-bit logarithm format (retrieved via GETQX) 55 clocks later.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | 32-bit unsigned integer input |

### Encoding
\simpleencoding{EEEE | 1101011 00L | DDDDDDDDD | 000001110 | — | — | — | 2...9}

### Related Instructions
- [GETQX](#getqx) — Retrieve logarithm result
- [QEXP](#qexp) — Convert logarithm back to integer

### Explanation
The QLOG instruction performs integer to logarithm conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 32-bit unsigned integer into a 5:27-bit logarithm format, where the result contains a 5-bit whole exponent in bits [31:27] and a 27-bit fractional exponent in bits [26:0].

The instruction takes the unsigned integer value in the D operand. After 55 clocks, the logarithm result can be retrieved using the GETQX instruction.

The logarithm result uses P2's fixed-point 5:27 format, which provides high precision for mathematical calculations. This format allows representing a wide range of logarithmic values while maintaining fractional precision.

Common applications include signal processing algorithms, mathematical computations requiring logarithmic scaling, and implementations of exponential/power functions when combined with QEXP.

**Basic logarithm calculation:**
```pasm
        QLOG    #1000          ' Begin log conversion
        ' Wait 55 clocks...
        GETQX   log_result     ' Get 5:27 logarithm
```

**Extracting logarithm components:**
```pasm
        QLOG    number
        ' ... wait 55 clocks ...
        GETQX   log_result
        SHR     log_result, #27 WZ  ' Extract 5-bit exponent
        MOV     exponent, log_result
        AND     mantissa, ##$07FFFFFF  ' Extract 27-bit mantissa
```

The result format is {5'whole_exponent, 27'fractional_exponent}. Use with QEXP for exponential operations.

---

## QMUL — CORDIC Solver

Perform 32×32 unsigned multiplication producing 64-bit result.

### Syntax
```pasm
        QMUL    {#}D,{#}S
```

### Result
Multiplies two 32-bit unsigned values, producing a 64-bit result with the lower 32 bits retrieved via GETQX and upper 32 bits retrieved via GETQY, 55 clocks later.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | First multiplicand (32-bit unsigned) |
| S | Second multiplicand (32-bit unsigned) |

### Encoding
\simpleencoding{EEEE | 1101000 0LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2...9}

### Related Instructions
- [GETQX](#getqx) — Retrieve lower 32 bits of product
- [GETQY](#getqy) — Retrieve upper 32 bits of product
- [QDIV](#qdiv) — CORDIC division
- [QFRAC](#qfrac) — CORDIC fractional division

### Explanation
The QMUL instruction performs high-precision unsigned multiplication using the P2's 54-stage pipelined CORDIC solver. It multiplies two 32-bit unsigned integers (D × S) and produces a full 64-bit product, avoiding the precision loss that would occur with standard 32-bit multiplication.

The instruction takes the first multiplicand in the D operand and the second multiplicand in the S operand, both as 32-bit unsigned values. After 55 clocks, the 64-bit result can be retrieved using GETQX for the lower 32 bits and GETQY for the upper 32 bits.

This full-precision multiplication is essential for applications requiring accurate large number arithmetic, such as DSP operations, cryptographic calculations, fixed-point mathematics, and multiply-accumulate operations where intermediate precision is critical.

The pipelined nature allows for continuous multiply-accumulate operations by issuing new QMUL instructions every 8 clocks (hub window) while retrieving results from previous operations, enabling high-throughput mathematical processing.

**Basic large number multiplication (1000000 × 2000000):**
```pasm
        QMUL    #1000000, #2000000
        ' Wait 55 clocks...
        GETQX   lower_32       ' Get lower 32 bits
        GETQY   upper_32       ' Get upper 32 bits
```

**Multiply-accumulate pattern:**
```pasm
        MOV     acc_low, #0
        MOV     acc_high, #0
        QMUL    a1, b1          ' First multiplication
        ' ... 55 clocks of other work ...
        GETQX   prod_low
        GETQY   prod_high
        ADD     acc_low, prod_low
        ADDX    acc_high, prod_high  ' Add with carry
```

**Pipelined multiplication for throughput:**
```pasm
        QMUL    a1, b1          ' Start first multiply
        ' ... 8 clocks later ...
        QMUL    a2, b2          ' Start second multiply
        ' ... 47 clocks later ...
        GETQX   result1_low     ' Get first result
        GETQY   result1_high
        ' ... 8 clocks later ...
        GETQX   result2_low     ' Get second result
        GETQY   result2_high
```

Each cog can issue one CORDIC instruction per hub window (every 8 clocks), allowing efficient pipelining of multiple operations.

---

## QROTATE — CORDIC Solver

Rotate a 32-bit signed (X, Y) point around origin (0, 0) by a specified angle.

### Syntax
```pasm
        QROTATE {#}D,{#}S
```

### Result
Rotates a coordinate pair around the origin, producing new X and Y coordinates retrieved via GETQX (X) and GETQY (Y) 55 clocks later.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | X coordinate (32-bit signed) |
| S | Rotation angle in P2 angle units (32-bit unsigned: $00000000 = 0°, $40000000 = 90°, $80000000 = 180°, $C0000000 = 270°) |
| SETQ | Y coordinate (32-bit signed, optional - defaults to 0 if not used) |

### Encoding
\simpleencoding{EEEE | 1101010 0LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2...9}

### Related Instructions
- [GETQX](#getqx) — Retrieve rotated X coordinate
- [GETQY](#getqy) — Retrieve rotated Y coordinate
- [SETQ](#setq) — Set Y coordinate
- [QVECTOR](#qvector) — Cartesian to polar conversion (inverse operation)

### Explanation
The QROTATE instruction performs point rotation using the P2's 54-stage pipelined CORDIC solver. It rotates a 32-bit signed (X, Y) coordinate pair around the origin (0, 0) by a specified angle, producing new 32-bit signed (X, Y) results.

The instruction takes the X coordinate from the D operand and the Y coordinate from the SETQ value (or 32'b0 if SETQ was not used). The rotation angle is specified in the S operand using P2's standard angle units where $00000000 = 0°, $40000000 = 90°, $80000000 = 180°, and $C0000000 = 270°.

After 55 clocks, the rotated coordinates can be retrieved using GETQX for the new X coordinate and GETQY for the new Y coordinate.

This instruction can also be used for polar to cartesian conversion by setting the X coordinate (D) to the length, Y coordinate (SETQ) to 0, and the angle (S) to the desired angle.

Common applications include graphics transformations, signal processing rotations, and coordinate system conversions.

**Rotate point (100, 200) by 45 degrees:**
```pasm
        SETQ    #200           ' Set Y coordinate
        QROTATE #100, #$20000000  ' X=100, angle=45°
        ' Wait 55 clocks...
        GETQX   new_x          ' Get rotated X
        GETQY   new_y          ' Get rotated Y
```

**Polar to cartesian conversion (length=500, angle=30°):**
```pasm
        SETQ    #0             ' Y coordinate = 0
        QROTATE #500, #$15555555  ' X=length, angle=30°
        ' ... other work for 55 clocks ...
        GETQX   cart_x         ' Get cartesian X
        GETQY   cart_y         ' Get cartesian Y
```

Use SETQ before QROTATE to specify the Y coordinate. If SETQ is not used, Y defaults to 0, making this useful for polar to cartesian conversions.

---

## QSQRT — CORDIC Solver

Calculate square root of 64-bit unsigned number formed from {S, D}.

### Syntax
```pasm
        QSQRT   {#}D,{#}S
```

### Result
Calculates the square root of a 64-bit value, producing a 32-bit result retrieved via GETQX 55 clocks later.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | Lower 32 bits of 64-bit input value |
| S | Upper 32 bits of 64-bit input value |

### Encoding
\simpleencoding{EEEE | 1101001 1LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2...9}

### Related Instructions
- [GETQX](#getqx) — Retrieve square root result
- [QMUL](#qmul) — CORDIC multiplication for squaring operations
- [ADD](#add) — Addition for sum of squares calculations
- [ADDX](#addx) — Addition with carry

### Explanation
The QSQRT instruction performs square root calculation using the P2's 54-stage pipelined CORDIC solver. It calculates the square root of a 64-bit unsigned value and produces a 32-bit result.

The 64-bit input is formed by concatenating the S operand as the upper 32 bits with the D operand as the lower 32 bits, creating the value {S, D}. Note that the operand order is reversed from the typical convention: QSQRT takes D first, S second, but forms {S, D}. After 55 clocks, the 32-bit square root result can be retrieved using the GETQX instruction.

This instruction is essential for mathematical calculations requiring precise square root operations on large values, such as distance calculations, RMS computations, geometric algorithms, and signal processing applications where maintaining precision across the full 64-bit range is important.

The result is the largest integer whose square does not exceed the input value. For perfect squares, the result is exact; for non-perfect squares, the result is the floor of the true square root. Mathematically, the result R satisfies: R² ≤ input < (R+1)².

**Basic square root of 32-bit number:**
```pasm
        QSQRT   #1000000, #0   ' sqrt{0, 1000000} = sqrt(1000000) ≈ 1000
        ' Wait 55 clocks...
        GETQX   sqrt_result    ' Get 1000
```

**Square root of 64-bit number:**
```pasm
        ' Example: sqrt({0x12345678, 0x9ABCDEF0})
        QSQRT   #$9ABCDEF0, #$12345678
        ' ... other work for 55 clocks ...
        GETQX   big_sqrt
```

**Distance calculation (sqrt(x² + y²)):**
```pasm
        QMUL    coord_x, coord_x    ' x²
        ' ... wait 55 clocks ...
        GETQX   x_squared_low
        GETQY   x_squared_high
        QMUL    coord_y, coord_y    ' y²
        ' ... wait 55 clocks ...
        GETQX   y_squared_low
        GETQY   y_squared_high
        ADD     sum_low, x_squared_low, y_squared_low    ' x² + y² (low)
        ADDX    sum_high, x_squared_high, y_squared_high ' x² + y² (high)
        QSQRT   sum_low, sum_high   ' sqrt(x² + y²)
        ' ... wait 55 clocks ...
        GETQX   distance
```

For 32-bit square roots, use S=0. The result is floor(sqrt(input)).

---

## QVECTOR — CORDIC Solver

Convert cartesian coordinates (X, Y) to polar coordinates (length, angle).

### Syntax
```pasm
        QVECTOR {#}D,{#}S
```

### Result
Converts cartesian coordinates to polar form, producing length (retrieved via GETQX) and angle (retrieved via GETQY) 55 clocks later.

### Parameters
| Parameter | Description |
|-----------|-------------|
| D | X coordinate (32-bit signed) |
| S | Y coordinate (32-bit signed) |

### Encoding
\simpleencoding{EEEE | 1101010 1LI | DDDDDDDDD | SSSSSSSSS | — | — | — | 2...9}

### Related Instructions
- [GETQX](#getqx) — Retrieve length/magnitude result
- [GETQY](#getqy) — Retrieve angle result
- [QROTATE](#qrotate) — Polar to cartesian conversion (inverse operation)
- [SETQ](#setq) — Used in complementary QROTATE operation

### Explanation
The QVECTOR instruction performs cartesian to polar coordinate conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 32-bit signed (X, Y) cartesian coordinate pair into a 32-bit (length, angle) polar coordinate pair.

The instruction takes the X coordinate in the D operand and Y coordinate in the S operand, both as 32-bit signed values. After 55 clocks, the results can be retrieved using GETQX for the length and GETQY for the angle.

The angle result uses P2's standard angle units where $00000000 = 0°, $40000000 = 90°, $80000000 = 180°, and $C0000000 = 270°.

This operation is commonly used in signal processing, graphics, and mathematical calculations requiring coordinate system conversions. It is the inverse operation of QROTATE, which converts polar coordinates back to cartesian form.

**Basic cartesian to polar conversion:**
```pasm
        QVECTOR #100, #200     ' Begin conversion
        ' Wait 55 clocks...
        GETQX   length         ' Get polar length
        GETQY   angle          ' Get polar angle
```

**Converting variable coordinates:**
```pasm
        QVECTOR x_coord, y_coord
        ' ... other work for 55 clocks ...
        GETQX   magnitude
        GETQY   phase_angle
```

Each cog can issue one CORDIC instruction per hub window (every 8 clocks), allowing efficient pipelining with other Q* operations.
