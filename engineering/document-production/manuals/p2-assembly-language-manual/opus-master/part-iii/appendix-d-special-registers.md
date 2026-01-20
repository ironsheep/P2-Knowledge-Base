# Appendix D: Special Registers Quick Reference

## Register Summary

| Address | Hex | Register | Access | Purpose |
|---------|-----|----------|--------|---------|
| 496 | $1F0 | IJMP3 | R/W | Interrupt 3 jump address |
| 497 | $1F1 | IRET3 | R/W | Interrupt 3 return address |
| 498 | $1F2 | IJMP2 | R/W | Interrupt 2 jump address |
| 499 | $1F3 | IRET2 | R/W | Interrupt 2 return address |
| 500 | $1F4 | IJMP1 | R/W | Interrupt 1 jump address |
| 501 | $1F5 | IRET1 | R/W | Interrupt 1 return address |
| 502 | $1F6 | PA | R/W | Multi-purpose register A |
| 503 | $1F7 | PB | R/W | Multi-purpose register B |
| 504 | $1F8 | PTRA | R/W | Hub pointer A |
| 505 | $1F9 | PTRB | R/W | Hub pointer B |
| 506 | $1FA | DIRA | R/W | Pin direction 0-31 |
| 507 | $1FB | DIRB | R/W | Pin direction 32-63 |
| 508 | $1FC | OUTA | R/W | Pin output 0-31 |
| 509 | $1FD | OUTB | R/W | Pin output 32-63 |
| 510 | $1FE | INA | R/O | Pin input 0-31 |
| 511 | $1FF | INB | R/O | Pin input 32-63 |

## Dual-Purpose Register Functions

| Register | Primary | Alternate Functions |
|----------|---------|---------------------|
| PA ($1F6) | General | CALLD return, CALLPA param, LOC address |
| PB ($1F7) | General | CALLD return, CALLPB param, LOC address |
| INA ($1FE) | Pin input | Debug interrupt call address |
| INB ($1FF) | Pin input | Debug interrupt return address |

## Memory Map

```{=latex}
\SpecialRegistersMapDiagram
```

::: {.figurecaption #fig:special-registers-map}
Special Registers Memory Map ($1F0–$1FF)
:::

*For complete documentation, see Part II: Special Registers.*

