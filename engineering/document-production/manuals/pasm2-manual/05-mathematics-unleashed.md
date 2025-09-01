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