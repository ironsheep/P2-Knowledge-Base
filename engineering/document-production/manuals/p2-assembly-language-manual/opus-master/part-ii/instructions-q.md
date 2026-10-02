# Instructions: Q

This section contains all PASM2 instructions beginning with the letter Q. The Q instructions are part of the CORDIC coprocessor family.

**A CORDIC command and the GETQX/GETQY that collects its result must not be split by an interrupt.** Every instruction on this page queues an operation whose result arrives 55 clocks later, so the issue and the collection are separate instructions with a gap between them. In PASM2 with interrupts enabled, fence that gap with a REP block, which blocks interrupts for its duration — including debug interrupts that ordinary masking cannot hold off. See [REP](#rep) for the pattern. Spin2 needs no such fence; the interpreter already protects its own CORDIC use.



::: instrheader
## QDIV {#qdiv}
Queue Divide

[CORDIC Coprocessor](#cordic-coprocessor) - Divides 64-bit by 32-bit, producing quotient and remainder.
:::

**QDIV**  *{#}Dest, {#}Src*

**Operation:** CORDIC: `{SETQ-value or 0, D} / S` → GETQX = quotient, GETQY = remainder

**Result:** Divides a 64-bit numerator by a 32-bit denominator, producing a 32-bit quotient (GETQX) and remainder (GETQY) 55 clocks later.

- Dest is a register or literal containing the lower 32 bits of the 64-bit numerator.
- Src is a register or literal containing the 32-bit denominator (divisor).
- Use SETQ before QDIV to specify the upper 32 bits of the numerator (defaults to 0 if not used).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101000 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QFRAC](#qfrac), [QMUL](#qmul)

**Explanation:**

QDIV performs high-precision unsigned division using the P2's 54-stage pipelined CORDIC solver. It divides a 64-bit numerator by a 32-bit denominator, producing both a 32-bit quotient and 32-bit remainder.

The 64-bit numerator is formed by concatenating the SETQ value (or 0 if SETQ not used) as the upper 32 bits with the Dest operand as the lower 32 bits: {SETQ, Dest}. The denominator is specified in the Src operand. Supply the upper 32 bits of the numerator with SETQ before QDIV, then after 55 clocks read the quotient with GETQX and the remainder with GETQY.

```pasm2
        QDIV    ##1000000, #3  ' {0, 1000000} / 3
        GETQX   quotient       ' 333333 (GETQX waits for the result)
        GETQY   remainder      ' 1
```

Division by zero does not trap or stall, and takes the same time as any other divide. GETQX returns the bitwise NOT of the numerator's upper long (the SETQ value, or 0 without SETQ, giving $FFFF_FFFF) and GETQY returns the numerator's lower long, Dest. For example, `SETQ #1` then `QDIV D, #0` gives GETQX = $FFFF_FFFE. Each cog can issue one CORDIC instruction per hub window (every 8 clocks).



::: instrheader
## QEXP {#qexp}
Queue Exponential

[CORDIC Coprocessor](#cordic-coprocessor) - Converts logarithm to integer (antilog/exponential).
:::

**QEXP**  *{#}Dest*

**Operation:** CORDIC: `2^D` (D as {5'whole, 27'frac}) → GETQX = number

**Result:** Converts a 5:27-bit logarithm format into a 32-bit unsigned integer, retrieved via GETQX 55 clocks later.

- Dest is a register or literal containing the 5:27-bit logarithm (5-bit exponent in bits [31:27], 27-bit fraction in bits [26:0]).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000001111 | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [QLOG](#qlog), [QMUL](#qmul)

**Explanation:**

QEXP performs logarithm to integer conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 5:27-bit logarithm format into a 32-bit unsigned integer, effectively computing the exponential (antilog) of the input.

The instruction takes the logarithm value in the Dest operand, which must be in P2's 5:27 format where bits [31:27] contain the 5-bit whole exponent and bits [26:0] contain the 27-bit fractional exponent. After 55 clocks, the integer result can be retrieved using GETQX.

QEXP converts a logarithm in the format QLOG produces back to an integer.

```pasm2
        QEXP    log_value      ' Begin exponential conversion
        GETQX   integer_result ' Get 32-bit integer (waits for it)
```



::: instrheader
## QFRAC {#qfrac}
Queue Fractional Divide

[CORDIC Coprocessor](#cordic-coprocessor) - Divides 64-bit by 32-bit with reversed operand arrangement.
:::

**QFRAC**  *{#}Dest, {#}Src*

**Operation:** CORDIC: `{D, SETQ-value or 0} / S` → GETQX = quotient, GETQY = remainder

**Result:** Divides a 64-bit numerator by a 32-bit denominator, producing a 32-bit quotient (GETQX) and remainder (GETQY) 55 clocks later.

- Dest is a register or literal containing the upper 32 bits of the 64-bit numerator.
- Src is a register or literal containing the 32-bit denominator (divisor).
- Use SETQ before QFRAC to specify the lower 32 bits of the numerator (defaults to 0 if not used).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101001 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QDIV](#qdiv), [QMUL](#qmul)

**Explanation:**

QFRAC performs fractional division using the P2's 54-stage pipelined CORDIC solver. It divides a 64-bit numerator by a 32-bit denominator, but differs from QDIV in the operand arrangement: Dest forms the upper 32 bits while SETQ (or 0) forms the lower 32 bits.

The 64-bit numerator is formed as {Dest, SETQ}. The quotient is 32 bits, so it fits only while Dest < Src: QFRAC returns a fraction of 2^32 (a ratio below 1). For a quotient of 1 or more, use QDIV.

```pasm2
        QFRAC   #1, #3         ' {1, 0} / 3 = 2^32 / 3
        GETQX   fraction       ' $5555_5555, 0.3333... of 2^32
        GETQY   remainder      ' 1
```

A SETQ value supplies the lower 32 bits of the numerator:

```pasm2
        SETQ    ##$8000_0000   ' lower 32 bits of the numerator: 0.5
        QFRAC   #1, #4         ' {1, $8000_0000} / 4 = 1.5 / 4
        GETQX   fraction       ' $6000_0000, 0.375 of 2^32
        GETQY   remainder      ' 0
```

Division by zero does not trap or stall, and takes the same time as any other divide. GETQX returns the bitwise NOT of Dest and GETQY returns the SETQ value (or 0 without SETQ). For example, `QFRAC #1, #0` gives GETQX = $FFFF_FFFE.



::: instrheader
## QLOG {#qlog}
Queue Logarithm

[CORDIC Coprocessor](#cordic-coprocessor) - Converts 32-bit integer to logarithm format.
:::

**QLOG**  *{#}Dest*

**Operation:** CORDIC: `log2(D)` → GETQX = {5'whole, 27'frac}

**Result:** Converts a 32-bit unsigned integer into a 5:27-bit logarithm format, retrieved via GETQX 55 clocks later.

- Dest is a register or literal containing the 32-bit unsigned integer input.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000001110 | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [QEXP](#qexp)

**Explanation:**

QLOG performs integer to logarithm conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 32-bit unsigned integer into a 5:27-bit logarithm format, where the result contains a 5-bit whole exponent in bits [31:27] and a 27-bit fractional exponent in bits [26:0].

The instruction takes the unsigned integer value in the Dest operand. After 55 clocks, the logarithm result can be retrieved using GETQX.

```pasm2
        QLOG    ##1000         ' Begin log conversion
        GETQX   log_result     ' Get 5:27 logarithm (waits for it)
```



::: instrheader
## QMUL {#qmul}
Queue Multiply

[CORDIC Coprocessor](#cordic-coprocessor) - Multiplies two 32-bit values, producing 64-bit result.
:::

**QMUL**  *{#}Dest, {#}Src*

**Operation:** CORDIC: `D * S` (unsigned) → GETQX = low product, GETQY = high product

**Result:** Multiplies two 32-bit unsigned values, producing a 64-bit result with lower 32 bits via GETQX and upper 32 bits via GETQY, 55 clocks later.

- Dest is a register or literal containing the first 32-bit multiplicand.
- Src is a register or literal containing the second 32-bit multiplicand.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101000 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [QDIV](#qdiv), [QFRAC](#qfrac)

**Explanation:**

QMUL performs high-precision unsigned multiplication using the P2's 54-stage pipelined CORDIC solver. It multiplies two 32-bit unsigned integers (Dest × Src) and produces a full 64-bit product, avoiding the precision loss that would occur with standard 32-bit multiplication. When both operands fit in 16 bits, the 2-clock MUL or MULS is faster; QMUL's 64-bit product is retrieved with GETQX for the low long and GETQY for the high long.

After 55 clocks, the 64-bit result can be retrieved using GETQX for the lower 32 bits and GETQY for the upper 32 bits.

```pasm2
        QMUL    ##1000000, ##2000000
        GETQX   lower_32       ' Get lower 32 bits (waits for it)
        GETQY   upper_32       ' Get upper 32 bits
```

Each cog can issue one CORDIC instruction per hub window (every 8 clocks), allowing efficient pipelining.



::: instrheader
## QROTATE {#qrotate}
Queue Rotate

[CORDIC Coprocessor](#cordic-coprocessor) - Rotates coordinate pair around origin by specified angle.
:::

**QROTATE**  *{#}Dest, {#}Src*

**Operation:** CORDIC: rotate point (D, SETQ-value or 0) by angle S → GETQX = X, GETQY = Y

**Result:** Rotates a coordinate pair around the origin, producing new X (GETQX) and Y (GETQY) coordinates 55 clocks later.

- Dest is a register or literal containing the X coordinate (32-bit signed).
- Src is a register or literal containing the rotation angle in P2 angle units ($00000000 = 0°, $40000000 = 90°, $80000000 = 180°, $C0000000 = 270°).
- Use SETQ before QROTATE to specify the Y coordinate (defaults to 0 if not used).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101010 | 0LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [SETQ](#setq), [QVECTOR](#qvector)

**Explanation:**

QROTATE performs point rotation using the P2's 54-stage pipelined CORDIC solver. It rotates a 32-bit signed (X, Y) coordinate pair around the origin (0, 0) by a specified angle, producing new 32-bit signed (X, Y) results.

The instruction takes the X coordinate from Dest and the Y coordinate from the SETQ value (or 0 if SETQ was not used). The rotation angle is specified in Src using P2's standard angle units.

This instruction can also be used for polar to cartesian conversion by setting X (Dest) to the length, Y (SETQ) to 0, and the angle (Src) to the desired angle.

```pasm2
        SETQ    #200           ' Set Y coordinate
        QROTATE #100, ##$20000000 ' X=100, angle=45 degrees
        GETQX   new_x          ' Get rotated X (waits for it)
        GETQY   new_y          ' Get rotated Y
```



::: instrheader
## QSQRT {#qsqrt}
Queue Square Root

[CORDIC Coprocessor](#cordic-coprocessor) - Calculates square root of a 64-bit value.
:::

**QSQRT**  *{#}Dest, {#}Src*

**Operation:** CORDIC: `sqrt({S, D})` → GETQX = root

**Result:** Calculates the square root of a 64-bit value, producing a 32-bit result via GETQX 55 clocks later.

- Dest is a register or literal containing the lower 32 bits of the 64-bit input value.
- Src is a register or literal containing the upper 32 bits of the 64-bit input value.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101001 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [QMUL](#qmul)

**Explanation:**

QSQRT performs square root calculation using the P2's 54-stage pipelined CORDIC solver. It calculates the square root of a 64-bit unsigned value and produces a 32-bit result.

The 64-bit input is formed by concatenating the Src operand as the upper 32 bits with the Dest operand as the lower 32 bits, creating the value {Src, Dest}. After 55 clocks, the 32-bit square root result can be retrieved using GETQX.

The result is the largest integer whose square does not exceed the input value.

```pasm2
        QSQRT   ##1000000, #0  ' sqrt(1000000) = 1000
        GETQX   sqrt_result    ' Get 1000 (waits for it)
```

For 32-bit square roots, use Src=0.



::: instrheader
## QVECTOR {#qvector}
Queue Vector

[CORDIC Coprocessor](#cordic-coprocessor) - Converts cartesian coordinates to polar form.
:::

**QVECTOR**  *{#}Dest, {#}Src*

**Operation:** CORDIC: vector of point (D, S) → GETQX = length, GETQY = angle

**Result:** Converts cartesian coordinates to polar form, producing length (GETQX) and angle (GETQY) 55 clocks later.

- Dest is a register or literal containing the X coordinate (32-bit signed).
- Src is a register or literal containing the Y coordinate (32-bit signed).


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101010 | 1LI | DDDDDDDDD | SSSSSSSSS | --- | --- | --- | 2...9 |


**Related:** [GETQX](#getqx), [GETQY](#getqy), [QROTATE](#qrotate)

**Explanation:**

QVECTOR performs cartesian to polar coordinate conversion using the P2's 54-stage pipelined CORDIC solver. It converts a 32-bit signed (X, Y) cartesian coordinate pair into a 32-bit (length, angle) polar coordinate pair.

The instruction takes the X coordinate in Dest and Y coordinate in Src, both as 32-bit signed values. After 55 clocks, the results can be retrieved using GETQX for the length and GETQY for the angle.

The angle result uses P2's standard angle units where $00000000 = 0°, $40000000 = 90°, $80000000 = 180°, and $C0000000 = 270°.

QROTATE with Y = 0 converts polar to cartesian coordinates.

```pasm2
        QVECTOR #100, #200     ' Begin conversion
        GETQX   length         ' Get polar length (waits for it)
        GETQY   angle          ' Get polar angle
```


