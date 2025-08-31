# Chapter 12: Optimization Mastery

*Making it faster, smaller, better*

## The Hook: 2x Speed with One Change

```pasm2
' Before: 8 clocks
        rdlong  x, hubaddr
        add     x, #1
        wrlong  x, hubaddr
        
' After: 4 clocks  
        rdlong  x, ptra++
        add     x, #1
        wrlong  x, --ptra
        ' PTRA magic saves cycles!
```

## Pipeline Optimization

Understanding the pipeline:
- Most instructions: 2 clocks
- Hub access: 2-9 clocks
- CORDIC: 55 clocks
- Multiply: 2 clocks

## Instruction Pairing

```pasm2
' These can overlap
        mul     x, y           ' Starts multiply
        add     a, b           ' Executes while multiply runs
        getmulh result         ' Gets multiply result
```

## Memory Access Patterns

```pasm2
' Block transfers are FAST
        setq    #16-1
        rdlong  buffer, hubaddr ' 16 longs in one go!
```

---

*Continue to [Chapter 13: Video Generation](13-video-generation.md) →*