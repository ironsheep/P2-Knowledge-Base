# Appendix A: Instruction Set Reference

## Quick Reference Format

Each instruction entry includes:
- Syntax
- Operation
- Flags affected
- Timing
- Example

## Memory Access Instructions

### RDBYTE - Read Byte from Hub
```
Syntax:  RDBYTE D, S/# {WZ/WC}
Operation: D = byte at hub[S]
Flags:    Z = (D == 0), C = D[7]
Timing:   2-9 clocks
Example:  RDBYTE value, hubaddr wz
```

### RDWORD - Read Word from Hub
```
Syntax:  RDWORD D, S/# {WZ/WC}
Operation: D = word at hub[S]
Flags:    Z = (D == 0), C = D[15]
Timing:   2-9 clocks
```

### RDLONG - Read Long from Hub
```
Syntax:  RDLONG D, S/# {WZ/WC}
Operation: D = long at hub[S]
Flags:    Z = (D == 0), C = D[31]
Timing:   2-9 clocks
```

[Continue with all instruction categories...]

---

*For complete instruction details, see the P2 Silicon Documentation*