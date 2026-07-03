# Appendix B: P_ Constants Quick Reference

This appendix provides a complete reference for all P_ constants used in smart pin configuration.


## How to Use P_ Constants

Constants are combined using the OR operator to build a complete WRPIN configuration:

```spin2
mode := P_ASYNC_TX | P_OE | P_INVERT_OUT
WRPIN(pin, mode)
```

**Structure of a P_ constant value:**

```{=latex}
\DiagPConstFields
```


## Smart Pin Modes (pick one)

| Constant | Value | Mode | Description | Chapter |
|----------|-------|------|-------------|---------|
| P_NORMAL | %00000 | Default | Normal mode (not smart pin) | 3 |
| P_REPOSITORY | %00001 | Non-DAC | Long repository | 18 |
| P_DAC_NOISE | %00001 | DAC | DAC noise output | 10 |
| P_DAC_DITHER_RND | %00010 | DAC | 16-bit random dither DAC | 10 |
| P_DAC_DITHER_PWM | %00011 | DAC | 16-bit PWM dither DAC | 10 |
| P_PULSE | %00100 | - | Pulse/cycle output | 7 |
| P_TRANSITION | %00101 | - | Transition output | 7 |
| P_NCO_FREQ | %00110 | - | NCO frequency output | 8 |
| P_NCO_DUTY | %00111 | - | NCO duty output | 8 |
| P_PWM_TRIANGLE | %01000 | - | PWM triangle | 9 |
| P_PWM_SAWTOOTH | %01001 | - | PWM sawtooth | 9 |
| P_PWM_SMPS | %01010 | - | PWM SMPS I/O | 9 |
| P_QUADRATURE | %01011 | - | Quadrature encoder | 14 |
| P_REG_UP | %01100 | - | Inc on A-rise when B-high | 14 |
| P_REG_UP_DOWN | %01101 | - | Inc/dec gated counter | 14 |
| P_COUNT_RISES | %01110 | - | Count A-rises | 14 |
| P_COUNT_HIGHS | %01111 | - | Count A-highs | 14 |
| P_STATE_TICKS | %10000 | - | Time A-low and A-high | 13 |
| P_HIGH_TICKS | %10001 | - | Time A-high states | 13 |
| P_EVENTS_TICKS | %10010 | - | Time X events / timeout | 13 |
| P_PERIODS_TICKS | %10011 | - | Measure X periods | 15 |
| P_PERIODS_HIGHS | %10100 | - | Sum highs in X periods | 15 |
| P_COUNTER_TICKS | %10101 | - | Time in X-clock window | 15 |
| P_COUNTER_HIGHS | %10110 | - | Highs in X-clock window | 15 |
| P_COUNTER_PERIODS | %10111 | - | Count periods in X clocks | 15 |
| P_ADC | %11000 | - | ADC internal clock | 16 |
| P_ADC_EXT | %11001 | - | ADC external clock | 16 |
| P_ADC_SCOPE | %11010 | - | ADC scope with trigger | 16 |
| P_USB_PAIR | %11011 | - | USB differential pair | 19 |
| P_SYNC_TX | %11100 | - | Synchronous serial TX | 11 |
| P_SYNC_RX | %11101 | - | Synchronous serial RX | 17 |
| P_ASYNC_TX | %11110 | - | Asynchronous serial TX | 11 |
| P_ASYNC_RX | %11111 | - | Asynchronous serial RX | 17 |


## A Input Selection (pick one)

| Constant | Bits [31:28] | Description |
|----------|--------------|-------------|
| P_TRUE_A | %0000 | True A input (default) |
| P_INVERT_A | %1000 | Invert A input |
| P_LOCAL_A | %0000 | Select local pin for A (default) |
| P_PLUS1_A | %0001 | Select pin+1 for A |
| P_PLUS2_A | %0010 | Select pin+2 for A |
| P_PLUS3_A | %0011 | Select pin+3 for A |
| P_OUTBIT_A | %0100 | Select OUT bit for A |
| P_MINUS3_A | %0101 | Select pin-3 for A |
| P_MINUS2_A | %0110 | Select pin-2 for A |
| P_MINUS1_A | %0111 | Select pin-1 for A |


## B Input Selection (pick one)

| Constant | Bits [27:24] | Description |
|----------|--------------|-------------|
| P_TRUE_B | %0000 | True B input (default) |
| P_INVERT_B | %1000 | Invert B input |
| P_LOCAL_B | %0000 | Select local pin for B (default) |
| P_PLUS1_B | %0001 | Select pin+1 for B |
| P_PLUS2_B | %0010 | Select pin+2 for B |
| P_PLUS3_B | %0011 | Select pin+3 for B |
| P_OUTBIT_B | %0100 | Select OUT bit for B |
| P_MINUS3_B | %0101 | Select pin-3 for B |
| P_MINUS2_B | %0110 | Select pin-2 for B |
| P_MINUS1_B | %0111 | Select pin-1 for B |


## A/B Input Logic (pick one)

| Constant | Bits [23:21] | Description |
|----------|--------------|-------------|
| P_PASS_AB | %000 | Pass A, B unchanged (default) |
| P_AND_AB | %001 | A AND B, B |
| P_OR_AB | %010 | A OR B, B |
| P_XOR_AB | %011 | A XOR B, B |
| P_FILT0_AB | %100 | FILT0 settings for A, B |
| P_FILT1_AB | %101 | FILT1 settings for A, B |
| P_FILT2_AB | %110 | FILT2 settings for A, B |
| P_FILT3_AB | %111 | FILT3 settings for A, B |


## Input Conditioning Modes (pick one)

### Logic/Schmitt/Comparator Modes

| Constant | Description | Chapter |
|----------|-------------|---------|
| P_LOGIC_A | Logic level A to IN, output OUT (default) | 12 |
| P_LOGIC_A_FB | Logic level A to IN, output feedback | 12 |
| P_LOGIC_B_FB | Logic level B to IN, output feedback | 12 |
| P_SCHMITT_A | Schmitt trigger A to IN, output OUT | 12 |
| P_SCHMITT_A_FB | Schmitt trigger A to IN, output feedback | 12 |
| P_SCHMITT_B_FB | Schmitt trigger B to IN, output feedback | 12 |
| P_COMPARE_AB | A > B to IN, output OUT | 12 |
| P_COMPARE_AB_FB | A > B to IN, output feedback | 12 |

### Level Comparison Modes

| Constant | Description | Chapter |
|----------|-------------|---------|
| P_LEVEL_A | A > Level to IN, output OUT | 12 |
| P_LEVEL_A_FBN | A > Level to IN, negative feedback | 12 |
| P_LEVEL_B_FBP | B > Level to IN, positive feedback | 12 |
| P_LEVEL_B_FBN | B > Level to IN, negative feedback | 12 |


## ADC Input Modes (pick one)

| Constant | Gain | Input Range | Description |
|----------|------|-------------|-------------|
| P_ADC_GIO | - | - | Ground-referenced input |
| P_ADC_VIO | - | - | VIO-referenced input |
| P_ADC_FLOAT | - | - | Floating input |
| P_ADC_1X | 1x | 0-3.3V | Unity gain |
| P_ADC_3X | 3.16x | 0-1.04V | 3.16x gain |
| P_ADC_10X | 10x | 0-330mV | 10x gain |
| P_ADC_30X | 31.6x | 0-104mV | 31.6x gain |
| P_ADC_100X | 100x | 0-33mV | 100x gain |


## DAC Output Modes (pick one)

| Constant | Resistance | Voltage | Description |
|----------|------------|---------|-------------|
| P_DAC_990R_3V | 990 Ω | 3.3V peak | Standard DAC |
| P_DAC_600R_2V | 600 Ω | 2.0V peak | Lower impedance |
| P_DAC_124R_3V | 124 Ω | 3.3V peak | Low impedance |
| P_DAC_75R_2V | 75 Ω | 2.0V peak | Lowest impedance |


## Sync/Async I/O (pick one)

| Constant | Description |
|----------|-------------|
| P_ASYNC_IO | Asynchronous I/O (default) |
| P_SYNC_IO | Synchronous I/O |


## IN/OUT Polarity (pick one each)

### IN Polarity

| Constant | Description |
|----------|-------------|
| P_TRUE_IN | True IN bit (default) |
| P_INVERT_IN | Invert IN bit |

### Output Polarity

| Constant | Description |
|----------|-------------|
| P_TRUE_OUTPUT | True output (default) |
| P_TRUE_OUT | Alias for P_TRUE_OUTPUT |
| P_INVERT_OUTPUT | Inverted output |
| P_INVERT_OUT | Alias for P_INVERT_OUTPUT |


## Drive Strength - High (pick one)

| Constant | Drive | Description |
|----------|-------|-------------|
| P_HIGH_FAST | 30mA | Fast drive high (default) |
| P_HIGH_1K5 | 1.5k Ω | Resistive pull-up |
| P_HIGH_15K | 15k Ω | Weak pull-up |
| P_HIGH_150K | 150k Ω | Very weak pull-up |
| P_HIGH_1MA | 1mA | Current source |
| P_HIGH_100UA | 100uA | Weak current source |
| P_HIGH_10UA | 10uA | Very weak current source |
| P_HIGH_FLOAT | - | Float high (tri-state) |


## Drive Strength - Low (pick one)

| Constant | Drive | Description |
|----------|-------|-------------|
| P_LOW_FAST | 30mA | Fast drive low (default) |
| P_LOW_1K5 | 1.5k Ω | Resistive pull-down |
| P_LOW_15K | 15k Ω | Weak pull-down |
| P_LOW_150K | 150k Ω | Very weak pull-down |
| P_LOW_1MA | 1mA | Current sink |
| P_LOW_100UA | 100uA | Weak current sink |
| P_LOW_10UA | 10uA | Very weak current sink |
| P_LOW_FLOAT | - | Float low (tri-state) |


## TT Bits / DIR-OUT Control (pick one)

| Constant | TT Value | Description |
|----------|----------|-------------|
| P_TT_00 | %00 | Default TT setting |
| P_TT_01 | %01 | TT = 01 |
| P_TT_10 | %10 | TT = 10 |
| P_TT_11 | %11 | TT = 11 |
| P_OE | %01 | Enable output in smart pin mode |
| P_CHANNEL | %01 | Enable DAC channel (non-smart pin) |
| P_BITDAC | %10 | Enable BITDAC (non-smart pin) |


## Common Combinations

### UART Transmit
```spin2
P_ASYNC_TX | P_OE                              ' Basic UART TX
P_ASYNC_TX | P_OE | P_INVERT_OUT               ' RS-232 TX (inverted)
```

### UART Receive
```spin2
P_ASYNC_RX                                     ' Basic UART RX
P_ASYNC_RX | P_INVERT_IN                       ' RS-232 RX (inverted)
```

### SPI Master TX
```spin2
P_SYNC_TX | P_OE                               ' SPI data out
```

### SPI Slave RX
```spin2
P_SYNC_RX | P_PLUS1_B                  ' SPI data in, clock from next pin
```

### PWM Output
```spin2
P_PWM_SAWTOOTH | P_OE                          ' Standard PWM
P_PWM_TRIANGLE | P_OE                          ' Triangle PWM
```

### DAC Output
```spin2
P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE        ' 16-bit dithered DAC
P_DAC_990R_3V | P_OE                           ' Basic 8-bit DAC
```

### ADC Input
```spin2
P_ADC_GIO | P_ADC                              ' Ground-referenced ADC
P_ADC_10X | P_ADC                              ' 10x gain ADC
```

### Button Input with Pull-up
```spin2
P_SCHMITT_A | P_HIGH_15K                  ' Schmitt trigger + 15k pull-up
```

### Open-Drain Output
```spin2
P_HIGH_FLOAT | P_LOW_FAST                    ' Open-drain (for I2C, etc.)
```


*For mode-specific usage, see the relevant chapter. For task-based lookup, see Appendix A.*
