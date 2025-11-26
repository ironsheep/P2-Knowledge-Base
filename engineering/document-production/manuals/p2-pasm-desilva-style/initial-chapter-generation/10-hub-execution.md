# Chapter 10: Hub Execution

*Breaking free from 512 instructions*

## The Hook: Unlimited Code Size

```pasm2
        orgh    $400            ' Code in hub memory
        org     0               ' But executes like COG code!
        
hub_code
        ' Your code can be megabytes!
        ' No more 512 instruction limit!
```

## COG vs Hub Execution

**COG Execution**:
- Fast (2 clocks per instruction)
- Limited to 512 instructions
- Deterministic timing

**Hub Execution**:
- Slower (2-9 clocks per instruction)
- Unlimited size
- Perfect for large programs

## Mixed Mode Programming

```pasm2
        call    #hub_function   ' Call hub code from COG
        jmp     #cog_code      ' Jump back to COG
        ' Mix and match as needed!
```

---

*Continue to [Chapter 11: Interrupts (If You Must)](11-interrupts-if-you-must.md) →*