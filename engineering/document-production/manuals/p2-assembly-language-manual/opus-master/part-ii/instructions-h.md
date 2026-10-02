# Instructions: H

This section contains all PASM2 instructions beginning with the letter H.



::: instrheader
## HUBSET {#hubset}
Set Hub Configuration

[Cog Control and Locks](#cog-control-and-locks) - Configures hub clock system, crystal, and PLL settings.
:::

**HUBSET**  *{#}D*

**Result:** Hub configuration is updated according to the value in D, selected by D[31:28]: clock source, crystal settings, and PLL configuration, a hard reset, write-protect and debug enables, the filter, or the PRNG seed.

- D is a register or 9-bit literal (or 32-bit augmented literal) containing the configuration value for the hub system.


| EEEE | Opcode | CZI | Dest | Src | C | Z | Result | Clks |
|:----:|:------:|:---:|:-:|:-:|:-:|:-:|:-------|:----:|
| EEEE | 1101011 | 00L | DDDDDDDDD | 000000000 | --- | --- | --- | 2...9 |


**Related:** [COGINIT](#coginit), [COGID](#cogid)

**Explanation:**

HUBSET configures the P2's global hub circuits. The single D operand both selects the circuit to configure, by its upper bits D[31:28], and supplies the configuration data:

| D[31:28] | D format | Effect |
|:--------:|:---------|:-------|
| %0000 | `%0000_xxxE_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS` | Set clock generator mode |
| %0001 | `%0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx` | Hard reset, reboots the chip |
| %0010 | `%0010_xxxx_xxxx_xxLW_DDDD_DDDD_DDDD_DDDD` | Set write-protect and debug enables |
| %0100 | `%0100_xxxx_xxxx_xxxx_xxxx_xxxR_RLLT_TTTT` | Set filter R to length L and tap T |
| %1xxx | `%1DDD_DDDD_DDDD_DDDD_DDDD_DDDD_DDDD_DDDD` | Seed the Xoroshiro128** PRNG with D |

The rest of this entry describes the clock generator mode, which controls clock source selection, crystal oscillator settings, and PLL configuration.

**Clock Source Selection (D[1:0]):**
- `%00` - RCFAST internal oscillator (~20-25 MHz, boot default)
- `%01` - RCSLOW internal oscillator (~20 kHz, low power mode)
- `%10` - Crystal or external clock on XI pin
- `%11` - PLL output

**Crystal Configuration (D[3:2]):**
- `%00` - XI/XO pins disabled (Hi-Z)
- `%01` - XI/XO with 1MΩ feedback, no capacitors
- `%10` - XI/XO with 1MΩ feedback, 15pF capacitors
- `%11` - XI/XO with 1MΩ feedback, 30pF capacitors

**PLL Configuration:**
- D[23:18] - Input divider (DDDDDD field, divides XI input by 1-64; stored as divider-1)
- D[17:8] - VCO multiplier (MMMMMMMMMM, 10-bit; multiplies by 1-1024; stored as multiplier-1)
- D[7:4] - Post divider (PPPP field): VCO/2, VCO/4, ..., VCO/30 for PPPP=0..14, and VCO/1 for PPPP=15 (the fast-overclock mode)
- D[24] - PLL power enable (E)
  - Note: the XI oscillator is enabled by the crystal-config field CC != %00, not by a dedicated bit.

**Hard Reset and PRNG Seed (other D[31:28] values):**
- D[31:28] = %0001 - hard reset, which reboots the chip: `HUBSET ##$1000_0000`
- D[31] == 1 - seed the Xoroshiro128** PRNG: `{1'b1, D[30:0]}` is written into 32 bits of its 128-bit state

**Switching Clock Sources:**

The clock selector controlled by the SS bits has a deglitching circuit: it waits for a positive edge on the old clock source before disengaging, then for a positive edge on the new clock source before switching over to it. Select RCFAST (%00) or RCSLOW (%01) while waiting for the crystal and/or PLL to settle, then switch over. Allow 5 ms for a crystal to stabilize before switching to XI, and 10 ms for crystal and PLL to stabilize before switching to the PLL. The PLL's VCO should be kept within 100 MHz to 200 MHz.

**Warning:** Incorrectly switching away from the PLL setting (SS = %11 and CC != %00) with PPPP = %1111 can cause a clock glitch that hangs the chip until a reset occurs. To switch away safely, first switch to an internal RC oscillator (SS = %00 or %01) while keeping PPPP = %1111 and the same CC.

Example: Enable a 20 MHz crystal with 15pF capacitors:

```pasm2
        hubset  ##%10_00              ' Enable 15pF crystal, stay RCFAST
        waitx   ##20_000_000/100      ' Wait 10ms for stabilization
        hubset  ##%10_10              ' Switch to crystal clock
```

Example: Configure the PLL to generate 80 MHz from a 20 MHz crystal:

```pasm2
        ' PLL on, XI /1, VCO x8, post divider /2, 15pF crystal;
        ' stay in RCFAST while the crystal and PLL stabilize:
        hubset  ##%1_000000_0000000111_0000_10_00
        waitx   ##20_000_000/100  ' Wait ~10ms for crystal+PLL
        ' Switch to PLL output:
        hubset  ##%1_000000_0000000111_0000_10_11
```

In this PLL example, the VCO runs at 20 MHz / 1 * 8 = 160 MHz, within the 100 MHz to 200 MHz range, then the post divider divides by 2 to produce an 80 MHz system clock.

HUBSET takes 2-9 clock cycles to execute depending on hub window alignment. Switching to a new clock source may take additional time for oscillator stabilization and PLL lock. Always allow appropriate wait periods when changing clock sources.



