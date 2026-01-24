# Clock Configuration Usage Guide

## Overview

The Propeller 2 clock system supports multiple clock sources with optional PLL multiplication. The compiler automatically calculates the clock mode register value based on constants defined in your CON block.

Clock sources:
- **RCFAST** - Internal RC oscillator (~20 MHz, default)
- **RCSLOW** - Internal slow RC oscillator (~20 kHz)
- **Crystal** - External crystal oscillator (1-60 MHz typical)
- **External input** - External clock signal
- **PLL** - Phase-locked loop for frequency multiplication

## Basic Usage

### Simple Fixed Frequency (Most Common)

```spin2
CON
  _clkfreq = 200_000_000     ' 200 MHz using PLL with 20 MHz crystal

PUB main()
  ' System runs at 200 MHz
  waitms(1000)               ' 1 second delay
```

The compiler assumes a 20 MHz crystal and calculates PLL settings automatically.

### Using a Different Crystal

```spin2
CON
  _xtlfreq = 25_000_000      ' 25 MHz crystal
  _clkfreq = 250_000_000     ' 250 MHz output via PLL

PUB main()
  ' System runs at 250 MHz
```

### No PLL (Crystal Direct)

```spin2
CON
  _xtlfreq = 20_000_000      ' Run at crystal frequency, no PLL

PUB main()
  ' System runs at exactly 20 MHz
```

## Clock Configuration Constants

Define these in your top-level object's CON block:

| Constant | Description | Range |
|----------|-------------|-------|
| `_clkfreq` | Desired system frequency | 3.333 MHz - 500 MHz |
| `_xtlfreq` | External crystal frequency | 1 - 60 MHz typical |
| `_xinfreq` | External clock input frequency | 250 kHz - 500 MHz |
| `_rcfast` | Use internal RC fast oscillator | ~20 MHz |
| `_rcslow` | Use internal RC slow oscillator | ~20 kHz |
| `_errfreq` | Allowable PLL frequency error | Default: 1,000,000 Hz |

### Configuration Rules

1. Only ONE clock configuration per program
2. `_clkfreq` alone assumes 20 MHz crystal input
3. `_xtlfreq` or `_xinfreq` alone runs at that frequency (no PLL)
4. Combining `_clkfreq` with `_xtlfreq` or `_xinfreq` enables PLL
5. `_rcfast` and `_rcslow` ignore other settings

## Runtime Clock Variables

The system maintains clock information at fixed HUB addresses:

| Variable | Address | Description |
|----------|---------|-------------|
| `CLKMODE` | $00040 | Current clock mode register value |
| `CLKFREQ` | $00044 | Current clock frequency in Hz |

```spin2
PUB show_clock()
  debug("Clock frequency: ", udec(clkfreq), " Hz")
  debug("Clock mode: ", uhex(clkmode))
```

## Clock Mode Configurations

### RCFAST - Internal RC Oscillator

```spin2
CON
  _rcfast = TRUE             ' Use ~20 MHz internal oscillator

PUB main()
  ' Runs at approximately 20 MHz
  ' No external crystal required
  ' Frequency varies with temperature
```

Use when:
- Crystal accuracy not required
- Minimal external components desired
- Power consumption is critical

### RCSLOW - Slow RC Oscillator

```spin2
CON
  _rcslow = TRUE             ' Use ~20 kHz internal oscillator

PUB main()
  ' Runs at approximately 20 kHz
  ' Extremely low power
```

Use when:
- Ultra-low power operation needed
- Timing accuracy not critical
- Real-time clock or sleep modes

### Crystal with PLL

```spin2
CON
  _xtlfreq = 20_000_000      ' 20 MHz crystal
  _clkfreq = 200_000_000     ' 200 MHz via PLL
```

The compiler calculates PLL dividers and multipliers to achieve the target frequency. Crystal frequencies ≥16 MHz use 15pF loading; frequencies <16 MHz use 30pF loading.

### External Input with PLL

```spin2
CON
  _xinfreq = 10_000_000      ' 10 MHz external clock input
  _clkfreq = 160_000_000     ' 160 MHz via PLL
```

Use external input when:
- Multiple chips share a clock source
- Precise frequency from external oscillator
- Synchronization with external system required

## PLL Operation

The PLL (Phase-Locked Loop) multiplies the input frequency to achieve higher system clocks.

### PLL Constraints

- Input frequency: 250 kHz to 500 MHz
- Output frequency: 3.333 MHz to 500 MHz
- VCO range: 99 MHz to 201 MHz (or up to requested + error)
- Feedback frequency (FPFD): ≥ 250 kHz

### Error Budget

```spin2
CON
  _xtlfreq = 12_000_000      ' 12 MHz crystal
  _clkfreq = 200_000_000     ' Target 200 MHz
  _errfreq = 500_000         ' Allow 0.5 MHz error (tighter than default)
```

The compiler iterates through PLL configurations to find the closest match within the error budget. Default error allowance is 1 MHz.

### PLL Mode Register Format

The compiler generates the clock mode register with these fields:

```
Bit 24:     PLL enable (1 = on)
Bits 23-18: Input divider - 1 (DIVD)
Bits 17-8:  Multiplier - 1 (MULT)
Bits 7-4:   Post divider - 1 (PPPP)
Bits 3-2:   Crystal capacitance
Bits 1-0:   Clock source
```

## Dynamic Clock Changes

Use HUBSET to change clock configuration at runtime.

### HUBSET Instruction

```spin2
DAT
              org     0
change_clock
              hubset  new_mode       ' Set new clock mode
              ' ... clock is now changed
```

### Safe Clock Switching Pattern

When switching to PLL, the process requires:
1. Set up PLL configuration (but don't switch to it yet)
2. Wait for PLL to lock
3. Switch clock source to PLL

```spin2
CON
  _clkfreq = 200_000_000

PUB switch_to_pll() | mode
  ' Step 1: Configure PLL but stay on RCFAST
  mode := clkmode & !%11         ' Clear source bits
  hubset(mode)                   ' Configure PLL

  ' Step 2: Wait for PLL to lock
  waitms(10)                     ' PLL settling time

  ' Step 3: Switch to PLL
  mode |= %11                    ' Set PLL source
  hubset(mode)
```

## Common Configurations

### 200 MHz with 20 MHz Crystal

```spin2
CON
  _clkfreq = 200_000_000
```

This is the most common configuration. The compiler assumes a 20 MHz crystal and calculates PLL settings for 10x multiplication.

### 297 MHz for HDTV Output

```spin2
CON
  _clkfreq = 297_000_000         ' HDTV 1080p pixel clock
```

### 160 MHz with 16 MHz Crystal

```spin2
CON
  _xtlfreq = 16_000_000
  _clkfreq = 160_000_000
```

### Battery-Powered Low Speed

```spin2
CON
  _rcfast = TRUE                 ' ~20 MHz, no crystal needed
```

Or for ultra-low power:

```spin2
CON
  _rcslow = TRUE                 ' ~20 kHz
```

### Debug-Enabled Default

When DEBUG statements are present and no clock is specified, the compiler defaults to 20 MHz crystal operation to ensure debug output works correctly.

## Patterns

### Checking Clock Frequency

```spin2
PUB verify_clock() : ok
  ok := (clkfreq >= 180_000_000) AND (clkfreq <= 220_000_000)
  if NOT ok
    debug("Warning: Clock outside expected range")
```

### Frequency-Dependent Timing

```spin2
PUB delay_microseconds(us) | ticks
  ticks := clkfreq / 1_000_000 * us
  waitx(ticks)

PUB calculate_baud_divisor(baud) : divisor
  divisor := clkfreq / baud
```

### Clock-Independent Timing

```spin2
PUB wait_ms(ms)
  waitms(ms)                     ' Automatically uses CLKFREQ

PUB wait_us(us)
  waitus(us)                     ' Automatically uses CLKFREQ
```

### Conditional Compilation by Clock

```spin2
CON
  _clkfreq = 200_000_000

  #if _clkfreq >= 200_000_000
  FAST_MODE = TRUE
  #else
  FAST_MODE = FALSE
  #endif
```

## Anti-Patterns

### Conflicting Clock Definitions

```spin2
' WRONG: Multiple clock sources specified
CON
  _rcfast = TRUE
  _clkfreq = 200_000_000         ' Error: conflicting settings
```

### Missing Crystal Frequency for Non-20MHz Crystal

```spin2
' WRONG: Assumes 20 MHz crystal but you have 25 MHz
CON
  _clkfreq = 200_000_000         ' Will miscalculate if crystal isn't 20 MHz!

' CORRECT: Specify your actual crystal
CON
  _xtlfreq = 25_000_000
  _clkfreq = 200_000_000
```

### Unreachable PLL Frequency

```spin2
' WRONG: May not be achievable with given crystal
CON
  _xtlfreq = 12_000_000
  _clkfreq = 333_333_333         ' Odd frequency, tight tolerance
  _errfreq = 1                   ' Unrealistic error budget

' BETTER: Use achievable frequency or relax error
CON
  _xtlfreq = 12_000_000
  _clkfreq = 336_000_000         ' 28x multiplier, achievable
  _errfreq = 1_000_000           ' Default error budget
```

### Hardcoded Timing Values

```spin2
' WRONG: Assumes specific clock frequency
PUB delay_1ms()
  waitx(200_000)                 ' Only correct at 200 MHz!

' CORRECT: Use CLKFREQ or built-in waits
PUB delay_1ms()
  waitms(1)                      ' Works at any clock frequency

PUB delay_1ms_manual()
  waitx(clkfreq / 1000)          ' Calculates based on actual frequency
```

### Clock Change Without PLL Lock Time

```spin2
' WRONG: Switching too fast
PUB bad_clock_switch()
  hubset(pll_mode)
  ' Immediately using clock - PLL may not be locked!

' CORRECT: Wait for PLL lock
PUB good_clock_switch()
  hubset(pll_setup_mode)         ' Configure but don't switch
  waitms(10)                     ' Wait for PLL to lock
  hubset(pll_active_mode)        ' Now switch to PLL
```

### Using CLKFREQ Before Initialization

```spin2
' WRONG: In a child object loaded before clock is set
OBJ
  uart : "serial"                ' May initialize before clock is configured

' BETTER: Initialize peripherals after clock is stable
PUB main()
  ' Clock is configured by this point
  uart.start(TX_PIN, RX_PIN, BAUD)
```

## Summary Tables

### Clock Source Selection

| Configuration | Clock Source | Typical Frequency |
|---------------|--------------|-------------------|
| `_rcfast = TRUE` | Internal RC fast | ~20 MHz |
| `_rcslow = TRUE` | Internal RC slow | ~20 kHz |
| `_xtlfreq` only | Crystal direct | Crystal frequency |
| `_xinfreq` only | External direct | Input frequency |
| `_clkfreq` only | PLL with 20 MHz crystal | 3.3-500 MHz |
| `_clkfreq + _xtlfreq` | PLL with crystal | 3.3-500 MHz |
| `_clkfreq + _xinfreq` | PLL with external | 3.3-500 MHz |

### Clock Mode Register Bits

| Bits | Value | Meaning |
|------|-------|---------|
| [1:0] | 00 | RCFAST source |
| [1:0] | 01 | RCSLOW source |
| [1:0] | 10 | XI source |
| [1:0] | 11 | PLL source |
| [3:2] | 00 | No capacitors |
| [3:2] | 01 | 15pF capacitors |
| [3:2] | 11 | 30pF capacitors |
| [24] | 1 | PLL enable |

### Frequency Limits

| Parameter | Minimum | Maximum |
|-----------|---------|---------|
| `_clkfreq` | 3,333,333 Hz | 500,000,000 Hz |
| `_xinfreq` | 250,000 Hz | 500,000,000 Hz |
| PLL VCO | 99,000,000 Hz | 201,000,000 Hz |
| PLL FPFD | 250,000 Hz | - |

## Related Documentation

- [Timing-Operations-Usage-Guide.md](Timing-Operations-Usage-Guide.md) - Using CLKFREQ for timing
- [Spin2-Object-Patterns-Guide.md](Spin2-Object-Patterns-Guide.md) - Top-level application clock setup
