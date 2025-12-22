# Instructions: H

This section contains all PASM2 instructions beginning with the letter H.



::: instrheader
## HUBSET {#hubset}
Set Hub Configuration

[COG Control and Locks](#cog-control-and-locks) - Configures hub clock system, crystal, and PLL settings.
:::

**HUBSET**  *{#}D*

---

**Result:** Hub configuration is updated according to the value in D, controlling clock source, crystal settings, and PLL configuration.

- D is a register or 9-bit literal (or 32-bit augmented literal) containing the configuration value for the hub system.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000000000 | --- | --- | --- | 2...9 |


**Related:** [COGINIT](#coginit), [COGID](#cogid)

**Explanation:**

HUBSET configures the P2's clock system and hub parameters. The 32-bit value in D specifies clock source selection, crystal oscillator settings, and PLL configuration to control the system clock frequency.

The D value contains multiple fields that control different aspects of the clock system:

**Clock Source Selection (D[3:2]):**
- `%00` - RCFAST internal oscillator (~20-25 MHz, boot default)
- `%01` - RCSLOW internal oscillator (~20 kHz, low power mode)
- `%10` - Crystal or external clock on XI pin
- `%11` - PLL output

**Crystal Configuration (D[1:0]):**
- `%00` - XI/XO pins disabled (Hi-Z)
- `%01` - XI/XO with 1MΩ feedback, no capacitors
- `%10` - XI/XO with 1MΩ feedback, 15pF capacitors
- `%11` - XI/XO with 1MΩ feedback, 30pF capacitors

**PLL Configuration:**
- D[27:24] - Input divider (PPPP field, divides XI input by 1-64)
- D[23:14] - VCO multiplier (10-bit field, multiplies by 1-1024)
- D[7:4] - Post divider (DDDD field, divides VCO by 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30)
- D[9] - PLL power enable
- D[8] - Crystal oscillator enable

**System Reset:**
- D[31] - Write 1 to reset the entire chip

The clock switching is glitch-free, and the system automatically falls back to RCFAST if the selected clock source fails. Proper timing must be observed when switching clock sources to allow for oscillator stabilization.

Example: Enable a 20 MHz crystal with 15pF capacitors:

::: pasm2
        hubset  ##%00_10              ' Enable crystal with 15pF caps
        waitx   ##20_000_000/100      ' Wait 10ms for stabilization
        hubset  ##%10_10              ' Switch to crystal clock
:::

Example: Configure PLL to generate 160 MHz from a 20 MHz crystal:

::: pasm2
        hubset  ##%00_10                        ' Enable crystal
        waitx   ##20_000_000/100                ' Wait 10ms
        hubset  ##%10_10                        ' Switch to crystal
        hubset  ##%0001_0000_0000_00001010_10  ' PLL: /1 * 16 / 2
        waitx   ##20_000_000/10000              ' Wait 100µs for PLL lock
        hubset  ##%0001_0000_0000_00001010_11  ' Switch to PLL output
:::

In this PLL example, the VCO runs at 20 MHz * 16 = 320 MHz, then the post divider divides by 2 to produce 160 MHz system clock.

HUBSET takes 2-9 clock cycles to execute depending on Hub window alignment. Switching to a new clock source may take additional time for oscillator stabilization and PLL lock. Always allow appropriate wait periods when changing clock sources.



