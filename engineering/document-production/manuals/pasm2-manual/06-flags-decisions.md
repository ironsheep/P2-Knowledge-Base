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