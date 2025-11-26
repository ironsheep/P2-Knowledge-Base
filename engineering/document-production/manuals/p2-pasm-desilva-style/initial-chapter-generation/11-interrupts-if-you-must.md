# Chapter 11: Interrupts (If You Must)

*With great power comes great responsibility*

## The Hook: Yes, P2 Has Interrupts

```pasm2
        setint1 #INT_PINRISE, #BUTTON_PIN  ' Setup interrupt
        ' Your code runs normally...
        ' Until button is pressed!
        
int1_handler
        ' Interrupt code here
        reti1                               ' Return from interrupt
```

## The Interrupt Controversy

P2 has interrupts. Should you use them? Usually NO.

Why? Because you have 8 COGs! Instead of interrupting important work, dedicate a COG to monitoring.

## When to Use Them

Rarely. But sometimes useful for:
- Ultra-low latency response
- Power-saving scenarios
- Legacy code ports

## When NOT to Use Them

Most of the time! Use a dedicated COG instead:
- Cleaner code
- Deterministic timing
- No priority inversion
- Easier debugging

---

*Continue to [Chapter 12: Optimization Mastery](12-optimization-mastery.md) →*