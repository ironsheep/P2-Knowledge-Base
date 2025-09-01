# Chapter 5: Mathematics Unleashed

*Hardware multiply and divide - finally!*

## The Hook: 64-Bit Multiply in 2 Clocks

```pasm2
        mul     x, y              ' 32x32->64 bit multiply
        getmulh high              ' Get high 32 bits
        ' Done! 64-bit result in 2 instructions!
```

Remember doing this with shifts and adds? Those days are over!

## The Multiplication Revolution

```pasm2
' Unsigned multiply
        mul     result, value     ' result = low 32 bits
        
' Signed multiply  
        muls    result, value     ' Signed version
        
' Scale and multiply
        scl     result, ##$8000   ' Scale by 0.5 (32.32 fixed point)
```

## Division Without Tears

```pasm2
' Start division
        qdiv    dividend, divisor ' Start the operation
        
' Get results (takes 30 clocks)
        getqx   quotient         ' Get quotient
        getqy   remainder        ' Get remainder
        
' Fractional division
        qfrac   numerator, denominator
        getqx   fraction         ' 32-bit fraction
```

## 64-Bit Operations

```pasm2
' 64-bit add
        add     low1, low2 wc
        addx    high1, high2
        
' 64-bit multiply  
        mul     x, y
        getmulh high
        ' Result in high:x
```

## Real-World Example: Fixed-Point Math

```pasm2
' 16.16 fixed point multiply
fixed_mul
        muls    a, b             ' Multiply
        getmulh high            ' Get high part
        shl     a, #16          ' Shift low part
        shr     high, #16       ' Shift high part
        or      a, high         ' Combine
        ' Result in 16.16 format!
```

---

*Continue to [Chapter 6: Flags and Decisions](06-flags-decisions.md) →*

---

# Chapter 6: Flags and Decisions

*Making choices at machine speed*

## The Hook: Any Instruction Can Be Conditional

```pasm2
        cmp     x, y wcz         ' Compare x and y
if_a    mov     result, x        ' If x > y, result = x
if_be   mov     result, y        ' If x <= y, result = y
        ' Max function in 3 instructions!
```

## The C and Z Flags

```pasm2
' Z Flag - Zero detection
        sub     x, y wz          ' Z=1 if x equals y
if_z    jmp     #equal          ' Jump if equal

' C Flag - Carry/Borrow
        add     x, y wc          ' C=1 if overflow
if_c    jmp     #overflow       ' Handle overflow
```

## Complex Conditions

```pasm2
' Combining flags
        cmp     x, y wcz
if_a    jmp     #greater        ' x > y (unsigned)
if_b    jmp     #less           ' x < y (unsigned)
if_z    jmp     #equal          ' x == y

' Signed comparisons
        cmps    x, y wcz        ' Signed compare
if_gt   jmp     #greater        ' x > y (signed)
if_lt   jmp     #less           ' x < y (signed)
```

## Skip Patterns - Conditional Blocks

```pasm2
        skipf   pattern          ' Set skip pattern
        add     x, #1           ' Maybe executed
        sub     y, #1           ' Maybe executed
        mov     z, #0           ' Maybe executed
        ' Pattern determines what runs!
```

---

*Continue to [Chapter 7: CORDIC Magic](07-cordic-magic.md) →*

---

# Chapter 7: CORDIC Magic

*Trigonometry at the speed of logic*

## The Hook: Hardware Sine in 55 Clocks

```pasm2
        qrotate angle, ##$7FFF_FFFF  ' Start rotation
        getqx   cosine               ' Get cosine (55 clocks later)
        getqy   sine                 ' Get sine
        ' Hardware trigonometry!
```

No lookup tables. No approximations. Pure mathematical precision.

## What Is CORDIC?

CORDIC (COordinate Rotation DIgital Computer) is a method for calculating trigonometric functions using only shifts and adds. P2 has it in hardware!

```pasm2
' Rotate a point
        setq    y                ' Set Y coordinate
        qrotate x, angle        ' Rotate X,Y by angle
        getqx   new_x           ' Get rotated X
        getqy   new_y           ' Get rotated Y
```

## Practical Applications

```pasm2
' Calculate distance (Pythagorean theorem)
        setq    y
        qvector x, #0           ' Start vector calculation
        getqx   distance        ' sqrt(x² + y²)
        getqy   angle          ' atan2(y, x)
        
' Generate sine wave
        qrotate angle, ##AMPLITUDE
        getqy   sample         ' Sine wave sample
        add     angle, ##FREQUENCY
```

## The Pipeline Concept

CORDIC operations take 55 clocks, but they're pipelined:

```pasm2
' Start multiple operations
        qrotate angle1, radius
        add     angle1, #1
        qrotate angle1, radius  ' Starts immediately!
        ' Both complete in ~56 clocks total
```

---

*Continue to [Chapter 8: Smart Pins Symphony](08-smart-pins-symphony.md) →*

---

# Chapter 8: Smart Pins Symphony
