# Appendix D: Predefined Constants Quick Reference

## Boolean Constants

| Constant | Hex Value | Decimal | Description |
|----------|-----------|---------|-------------|
| TRUE | $FFFFFFFF | -1 | All bits set (boolean true) |
| FALSE | $00000000 | 0 | All bits clear (boolean false) |

## Numeric Limit Constants

| Constant | Hex Value | Decimal | Description |
|----------|-----------|---------|-------------|
| NEGX | $80000000 | -2,147,483,648 | Most negative signed 32-bit |
| POSX | $7FFFFFFF | +2,147,483,647 | Most positive signed 32-bit |

## Mathematical Constants

| Constant | Hex Value | Approximate | Description |
|----------|-----------|-------------|-------------|
| PI | $40490FDB | 3.14159265 | IEEE 754 single-precision π |

## Execution Mode Constants

| Constant | Pattern | Description |
|----------|---------|-------------|
| COGEXEC | %0_0_0000 | Execute from COG RAM after loading |
| HUBEXEC | %0_1_0000 | Execute directly from Hub RAM |
| COGEXEC_NEW | %1_0_0000 | Auto-select COG, execute from COG |
| COGEXEC_NEW_PAIR | %1_0_0001 | Auto-select COG pair, execute from COG |
| HUBEXEC_NEW | %1_1_0000 | Auto-select COG, execute from Hub |
| HUBEXEC_NEW_PAIR | %1_1_0001 | Auto-select COG pair, execute from Hub |

## COGINIT Usage Example

```pasm
        ' Start COG 2 executing from COG RAM
        COGINIT #COGEXEC, ptra, #2

        ' Start any available COG executing from Hub
        COGINIT #HUBEXEC_NEW, ##@hub_code wc
        IF_C    jmp     #no_cogs_available
```

*For complete documentation, see Part II: Constants.*
