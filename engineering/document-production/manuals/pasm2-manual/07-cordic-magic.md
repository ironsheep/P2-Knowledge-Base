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