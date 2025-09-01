# Test Document for Semantic Blocks

This document tests all 7 semantic marker types.

## Diagram Needs

::: needs-diagram
Timing diagram showing clock relationships between cog and hub memory access cycles.
:::

## Preliminary Content

::: preliminary-content
This feature documentation is under development. The API may change.
:::

## Verification Needed

::: needs-verification
The frequency calculation formula needs hardware verification on actual P2 chips.
:::

## Examples Required

::: needs-examples
Code examples needed for ADC mode configuration with different sampling rates.
:::

## Technical Review

::: needs-technical-review
Smart Pin transition mode behavior requires review by hardware engineering team.
:::

## Code Review

::: needs-code-review
This PASM2 routine needs optimization review for cycle count and register usage.

```pasm2
        rdpin   temp, #PIN_ADC
        shr     temp, #16
        mov     result, temp
```
:::

## Tips

::: tip
Use Smart Pins for hardware timing whenever possible - they're more accurate than software delays.
:::

## Regular Content

This is normal paragraph text that should remain unchanged.