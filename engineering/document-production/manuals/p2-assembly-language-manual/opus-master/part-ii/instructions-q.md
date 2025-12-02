# Instructions: Q

This section contains all PASM2 instructions beginning with the letter Q. The Q instructions are part of the CORDIC coprocessor family.



## QDIV {#qdiv}

Queue divide
[CORDIC Solver](#cordic-solver) - Perform 64÷32 unsigned division with 32-bit quotient and remainder.

**QDIV**  *{#}Dest, {#}Src*

---

**Result:** Divides a 64-bit numerator by a 32-bit denominator, producing a 32-bit quotient (GETQX) and remainder (GETQY) 55 clocks later.

- Dest is a register or literal containing the lower 32 bits of the 64-bit numerator.
- Src is a register or literal containing the 32-bit denominator (divisor).
- Use SETQ before QDIV to specify the upper 32 bits of the numerator (defaults to 0 if not used).

```{=latex}
\simpleencoding{EEEE}{1101000}{1LI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{---}{2...9}
```

**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QFRAC](#qfrac), [QMUL](#qmul)

**Explanation:**

QDIV performs high-precision unsigned division using the P2's 54-stage pipelined CORDIC solver. It divides a 64-bit numerator by a 32-bit denominator, producing both a 32-bit quotient and 32-bit remainder.

The 64-bit numerator is formed by concatenating the SETQ value (or 0 if SETQ not used) as the upper 32 bits with the Dest operand as the lower 32 bits: {SETQ, Dest}. The denominator is specified in the Src operand. After 55 clocks, the quotient can be retrieved using GETQX and the remainder using GETQY.

::: pasm2
        QDIV    #1000000, #3   ' {0, 1000000} / 3
        ' Wait 55 clocks...
        GETQX   quotient       ' Get 333333
        GETQY   remainder      ' Get 1
:::

Division by zero produces undefined results. Each cog can issue one CORDIC instruction per hub window (every 8 clocks).



## QEXP {#qexp}

Queue exponential
[CORDIC Solver](#cordic-solver) - Convert 5:27-bit logarithm to 32-bit unsigned integer.

**QEXP**  *{#}Dest*

---

**Result:** Converts a 5:27-bit logarithm format into a 32-bit unsigned integer, retrieved via GETQX 55 clocks later.

- Dest is a register or literal containing the 5:27-bit logarithm (5-bit exponent in bits [31:27], 27-bit fraction in bits [26:0]).

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000001111}{---}{---}{---}{2...9}
```

**Related:** [GETQX](#getqx), [QLOG](#qlog), [QMUL](#qmul)

**Explanation:**

QEXP performs logarithm to integer conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 5:27-bit logarithm format into a 32-bit unsigned integer, effectively computing the exponential (antilog) of the input.

The instruction takes the logarithm value in the Dest operand, which must be in P2's 5:27 format where bits [31:27] contain the 5-bit whole exponent and bits [26:0] contain the 27-bit fractional exponent. After 55 clocks, the integer result can be retrieved using GETQX.

QEXP is the complement of QLOG and is commonly used together with QLOG to perform power calculations.

::: pasm2
        QEXP    log_value      ' Begin exponential conversion
        ' Wait 55 clocks...
        GETQX   integer_result ' Get 32-bit integer
:::



## QFRAC {#qfrac}

Queue fractional divide
[CORDIC Solver](#cordic-solver) - Perform 64÷32 unsigned fractional division.

**QFRAC**  *{#}Dest, {#}Src*

---

**Result:** Divides a 64-bit numerator by a 32-bit denominator, producing a 32-bit quotient (GETQX) and remainder (GETQY) 55 clocks later.

- Dest is a register or literal containing the upper 32 bits of the 64-bit numerator.
- Src is a register or literal containing the 32-bit denominator (divisor).
- Use SETQ before QFRAC to specify the lower 32 bits of the numerator (defaults to 0 if not used).

```{=latex}
\simpleencoding{EEEE}{1101001}{0LI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{---}{2...9}
```

**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QDIV](#qdiv), [QMUL](#qmul)

**Explanation:**

QFRAC performs fractional division using the P2's 54-stage pipelined CORDIC solver. It divides a 64-bit numerator by a 32-bit denominator, but differs from QDIV in the operand arrangement: Dest forms the upper 32 bits while SETQ (or 0) forms the lower 32 bits.

The 64-bit numerator is formed as {Dest, SETQ}. This arrangement makes QFRAC particularly suitable for fractional arithmetic where the integer part is in Dest and the fractional part is in SETQ.

::: pasm2
        SETQ    #$C0000000     ' 0.75 in 32-bit fraction format
        QFRAC   #5, #2         ' {5, 0.75} / 2 = 2.875
        ' Wait 55 clocks...
        GETQX   quotient       ' Get integer quotient
        GETQY   remainder      ' Get fractional remainder
:::



## QLOG {#qlog}

Queue logarithm
[CORDIC Solver](#cordic-solver) - Convert 32-bit unsigned integer to 5:27-bit logarithm.

**QLOG**  *{#}Dest*

---

**Result:** Converts a 32-bit unsigned integer into a 5:27-bit logarithm format, retrieved via GETQX 55 clocks later.

- Dest is a register or literal containing the 32-bit unsigned integer input.

```{=latex}
\simpleencoding{EEEE}{1101011}{00L}{DDDDDDDDD}{000001110}{---}{---}{---}{2...9}
```

**Related:** [GETQX](#getqx), [QEXP](#qexp)

**Explanation:**

QLOG performs integer to logarithm conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 32-bit unsigned integer into a 5:27-bit logarithm format, where the result contains a 5-bit whole exponent in bits [31:27] and a 27-bit fractional exponent in bits [26:0].

The instruction takes the unsigned integer value in the Dest operand. After 55 clocks, the logarithm result can be retrieved using GETQX.

::: pasm2
        QLOG    #1000          ' Begin log conversion
        ' Wait 55 clocks...
        GETQX   log_result     ' Get 5:27 logarithm
:::



## QMUL {#qmul}

Queue multiply
[CORDIC Solver](#cordic-solver) - Perform 32×32 unsigned multiplication producing 64-bit result.

**QMUL**  *{#}Dest, {#}Src*

---

**Result:** Multiplies two 32-bit unsigned values, producing a 64-bit result with lower 32 bits via GETQX and upper 32 bits via GETQY, 55 clocks later.

- Dest is a register or literal containing the first 32-bit multiplicand.
- Src is a register or literal containing the second 32-bit multiplicand.

```{=latex}
\simpleencoding{EEEE}{1101000}{0LI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{---}{2...9}
```

**Related:** [GETQX](#getqx), [GETQY](#getqy), [QDIV](#qdiv), [QFRAC](#qfrac)

**Explanation:**

QMUL performs high-precision unsigned multiplication using the P2's 54-stage pipelined CORDIC solver. It multiplies two 32-bit unsigned integers (Dest × Src) and produces a full 64-bit product, avoiding the precision loss that would occur with standard 32-bit multiplication.

After 55 clocks, the 64-bit result can be retrieved using GETQX for the lower 32 bits and GETQY for the upper 32 bits.

::: pasm2
        QMUL    #1000000, #2000000
        ' Wait 55 clocks...
        GETQX   lower_32       ' Get lower 32 bits
        GETQY   upper_32       ' Get upper 32 bits
:::

Each cog can issue one CORDIC instruction per hub window (every 8 clocks), allowing efficient pipelining.



## QROTATE {#qrotate}

Queue rotate
[CORDIC Solver](#cordic-solver) - Rotate a 32-bit signed (X, Y) point around origin by specified angle.

**QROTATE**  *{#}Dest, {#}Src*

---

**Result:** Rotates a coordinate pair around the origin, producing new X (GETQX) and Y (GETQY) coordinates 55 clocks later.

- Dest is a register or literal containing the X coordinate (32-bit signed).
- Src is a register or literal containing the rotation angle in P2 angle units ($00000000 = 0°, $40000000 = 90°, $80000000 = 180°, $C0000000 = 270°).
- Use SETQ before QROTATE to specify the Y coordinate (defaults to 0 if not used).

```{=latex}
\simpleencoding{EEEE}{1101010}{0LI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{---}{2...9}
```

**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QVECTOR](#qvector)

**Explanation:**

QROTATE performs point rotation using the P2's 54-stage pipelined CORDIC solver. It rotates a 32-bit signed (X, Y) coordinate pair around the origin (0, 0) by a specified angle, producing new 32-bit signed (X, Y) results.

The instruction takes the X coordinate from Dest and the Y coordinate from the SETQ value (or 0 if SETQ was not used). The rotation angle is specified in Src using P2's standard angle units.

This instruction can also be used for polar to cartesian conversion by setting X (Dest) to the length, Y (SETQ) to 0, and the angle (Src) to the desired angle.

::: pasm2
        SETQ    #200           ' Set Y coordinate
        QROTATE #100, #$20000000  ' X=100, angle=45 degrees
        ' Wait 55 clocks...
        GETQX   new_x          ' Get rotated X
        GETQY   new_y          ' Get rotated Y
:::



## QSQRT {#qsqrt}

Queue square root
[CORDIC Solver](#cordic-solver) - Calculate square root of 64-bit unsigned number.

**QSQRT**  *{#}Dest, {#}Src*

---

**Result:** Calculates the square root of a 64-bit value, producing a 32-bit result via GETQX 55 clocks later.

- Dest is a register or literal containing the lower 32 bits of the 64-bit input value.
- Src is a register or literal containing the upper 32 bits of the 64-bit input value.

```{=latex}
\simpleencoding{EEEE}{1101001}{1LI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{---}{2...9}
```

**Related:** [GETQX](#getqx), [QMUL](#qmul)

**Explanation:**

QSQRT performs square root calculation using the P2's 54-stage pipelined CORDIC solver. It calculates the square root of a 64-bit unsigned value and produces a 32-bit result.

The 64-bit input is formed by concatenating the Src operand as the upper 32 bits with the Dest operand as the lower 32 bits, creating the value {Src, Dest}. After 55 clocks, the 32-bit square root result can be retrieved using GETQX.

The result is the largest integer whose square does not exceed the input value.

::: pasm2
        QSQRT   #1000000, #0   ' sqrt(1000000) = 1000
        ' Wait 55 clocks...
        GETQX   sqrt_result    ' Get 1000
:::

For 32-bit square roots, use Src=0.



## QVECTOR {#qvector}

Queue vector
[CORDIC Solver](#cordic-solver) - Convert cartesian coordinates (X, Y) to polar coordinates (length, angle).

**QVECTOR**  *{#}Dest, {#}Src*

---

**Result:** Converts cartesian coordinates to polar form, producing length (GETQX) and angle (GETQY) 55 clocks later.

- Dest is a register or literal containing the X coordinate (32-bit signed).
- Src is a register or literal containing the Y coordinate (32-bit signed).

```{=latex}
\simpleencoding{EEEE}{1101010}{1LI}{DDDDDDDDD}{SSSSSSSSS}{---}{---}{---}{2...9}
```

**Related:** [GETQX](#getqx), [GETQY](#getqy), [QROTATE](#qrotate)

**Explanation:**

QVECTOR performs cartesian to polar coordinate conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 32-bit signed (X, Y) cartesian coordinate pair into a 32-bit (length, angle) polar coordinate pair.

The instruction takes the X coordinate in Dest and Y coordinate in Src, both as 32-bit signed values. After 55 clocks, the results can be retrieved using GETQX for the length and GETQY for the angle.

The angle result uses P2's standard angle units where $00000000 = 0°, $40000000 = 90°, $80000000 = 180°, and $C0000000 = 270°.

QVECTOR is the inverse operation of QROTATE.

::: pasm2
        QVECTOR #100, #200     ' Begin conversion
        ' Wait 55 clocks...
        GETQX   length         ' Get polar length
        GETQY   angle          ' Get polar angle
:::

