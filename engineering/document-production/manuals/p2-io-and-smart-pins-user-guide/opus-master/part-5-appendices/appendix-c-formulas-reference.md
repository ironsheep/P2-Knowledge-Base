# Appendix C: Formulas Reference

This appendix collects all mathematical formulas from the P2 I/O & Smart Pins User Guide in a single quick-reference location.


## NCO Frequency Generation

### Output Frequency from Y Value

**Formula:**
```formula
frequency = (Y × sysclk) / (X[15:0] × 2^32)
```

For X[15:0] = 1 (maximum update rate):
```formula
frequency = (Y × sysclk) / 2^32
```

**Variables:**

- `frequency`: Output frequency in Hz
- `Y`: NCO frequency control word (32-bit)
- `sysclk`: System clock frequency in Hz
- `X[15:0]`: Base period (1 for maximum resolution)

**Worked Example (1 kHz at 200 MHz):**
```formula
frequency = 1000 Hz
sysclk = 200,000,000 Hz
Y = (1000 × 4,294,967,296) / 200,000,000
Y = 21,475
```

**Note:** Frequency resolution is sysclk / 2^32 (~0.047 Hz at 200 MHz).


### Y Value from Desired Frequency

**Formula:**
```formula
Y = (frequency × 2^32) / sysclk
```

In Spin2:
```spin2
y_value := frequency FRAC _clkfreq
```

**Worked Example (10 kHz at 200 MHz):**
```formula
Y = (10,000 × 4,294,967,296) / 200,000,000
Y = 214,748
```


## PWM Output

### PWM Frequency (Triangle Mode)

**Formula:**
```formula
PWM_frequency = sysclk / (2 × X[31:16] × X[15:0])
```

**Variables:**

- `X[31:16]`: Frame period (counter range)
- `X[15:0]`: Base period (clocks per counter update)

**Worked Example (1 kHz PWM at 200 MHz):**
```formula
PWM_frequency = 200,000,000 / (2 × 100,000 × 1) = 1000 Hz
```


### PWM Frequency (Sawtooth Mode)

**Formula:**
```formula
PWM_frequency = sysclk / (X[31:16] × X[15:0])
```

**Worked Example (20 kHz PWM at 200 MHz):**
```formula
X[31:16] = 200,000,000 / 20,000 = 10,000
PWM_frequency = 200,000,000 / (10,000 × 1) = 20,000 Hz
```


### PWM Duty Cycle

**Formula:**
```formula
duty_percent = (Y[15:0] / X[31:16]) × 100%
```

**Worked Example (50% duty with frame=10,000):**
```formula
Y = 10,000 × 50 / 100 = 5,000
duty_percent = (5,000 / 10,000) × 100% = 50%
```


### PWM Resolution (Bits)

**Formula:**
```formula
resolution_bits = log2(X[31:16])
```

| Frame Period | Resolution |
|--------------|------------|
| 256 | 8 bits |
| 1024 | 10 bits |
| 4096 | 12 bits |
| 65535 | 16 bits |


## Serial Communication (UART)

### Baud Rate Timing

**Formula (Basic):**
```formula
X[31:16] = sysclk / baud_rate
```

**Formula (With Fractional Precision):**
```formula
X = ((sysclk × 65536 / baud_rate) & $FFFFFC00) | data_bits
```

**Variables:**

- `X[31:16]`: Integer bit period in clocks
- `X[15:10]`: Fractional adjustment (1/64 clock)
- `X[4:0]`: Number of data bits (1-32)
- `baud_rate`: Desired baud rate in bits/second

**Worked Example (115200 baud at 200 MHz):**
```formula
X[31:16] = 200,000,000 / 115,200 = 1736 clocks/bit
bit_period = 1736 × 65536 = 113,770,496
X = ($06C8_0000 | 8) = $06C8_0008  (8 data bits)
```


### Baud Rate Error

**Formula:**
```formula
actual_baud = sysclk / round(sysclk / target_baud)
error_percent = abs(actual_baud - target_baud) / target_baud × 100%
```

**Note:** UART typically tolerates ±2-3% baud rate error.


## ADC (Analog Input)

### ADC Sample Rate

**Formula:**
```formula
sample_rate = sysclk / 2^(X[3:0])
```

**Variables:**

- `X[3:0]`: Sample period exponent (1-15)

**Worked Example (8-bit SINC2 at 200 MHz):**
```formula
X[3:0] = 7  (128 clocks)
sample_rate = 200,000,000 / 128 = 1,562,500 Hz
```

| X[3:0] | Period | Sample Rate at 200 MHz |
|--------|--------|------------------------|
| %0111 | 128 clocks | 1.56 MHz |
| %1001 | 512 clocks | 390 kHz |
| %1011 | 2048 clocks | 97.6 kHz |
| %1101 | 8192 clocks | 24.4 kHz |


### ADC Voltage Conversion

**Formula:**
```formula
voltage_mv = (sample × 3300) / full_scale
```

**Variables:**

- `sample`: Raw ADC reading
- `full_scale`: Maximum ADC value (depends on resolution)
- For 8-bit: full_scale = 255
- For 14-bit: full_scale = 16383

**Worked Example (8-bit ADC reading 128):**
```formula
voltage_mv = (128 × 3300) / 255 = 1655 mV
```


### ADC with Gain

**Effective Input Range:**
```formula
input_max = 3300mV / gain_factor
```

| Gain Mode | Gain Factor | Input Range |
|-----------|-------------|-------------|
| P_ADC_1X | 1 | 0-3.3V |
| P_ADC_3X | 3.16 | 0-1.04V |
| P_ADC_10X | 10 | 0-330mV |
| P_ADC_30X | 31.6 | 0-104mV |
| P_ADC_100X | 100 | 0-33mV |


## DAC (Analog Output)

### 8-bit DAC Voltage

**Formula:**
```formula
voltage = (DAC_value / 256) × V_full_scale
```

**Worked Example (DAC value 128, 3.3V range):**
```formula
voltage = (128 / 256) × 3.3V = 1.65V
```


### 16-bit DAC Voltage

**Formula:**
```formula
voltage = (DAC_value / 65536) × V_full_scale
```

**Resolution:**

- 3.3V range: 3.3V / 65536 = 50.4 µV/LSB
- 2.0V range: 2.0V / 65536 = 30.5 µV/LSB

**Worked Example (DAC value 32768, 3.3V range):**
```formula
voltage = (32768 / 65536) × 3.3V = 1.65V
```


### Voltage to DAC Value

**8-bit:**
```spin2
dac8 := (millivolts * 256) / 3300
```

**16-bit:**
```spin2
dac16 := (millivolts * 65536) / 3300
```


## Timing Measurement

### Frequency from Period

**Formula:**
```formula
frequency = sysclk / period_clocks
```

**Worked Example (period of 200,000 clocks at 200 MHz):**
```formula
frequency = 200,000,000 / 200,000 = 1000 Hz
```


### Period in Microseconds

**Formula:**
```formula
period_us = clocks / (sysclk / 1,000,000)
```

**Worked Example (1000 clocks at 200 MHz):**
```formula
period_us = 1000 / (200,000,000 / 1,000,000) = 1000 / 200 = 5 µs
```


### Duty Cycle

**Formula:**
```formula
duty_percent = (high_clocks × 100) / (high_clocks + low_clocks)
```

**Worked Example (high=3000, low=7000 clocks):**
```formula
duty_percent = (3000 × 100) / (3000 + 7000) = 30%
```


## Period/Frequency Measurement

### Frequency from Period Ticks

**Formula (P_PERIODS_TICKS):**
```formula
frequency = (num_periods × sysclk) / rdpin_value
```

**Variables:**

- `num_periods`: X register value (periods measured)
- `rdpin_value`: Total clocks for all periods

**Worked Example (100 periods, 2,000,000 clocks at 200 MHz):**
```formula
frequency = (100 × 200,000,000) / 2,000,000 = 10,000 Hz
```


### Frequency from Period Count

**Formula (P_COUNTER_PERIODS with 1-second window):**
```formula
frequency = rdpin_value  (direct Hz reading)
```

**General Formula:**
```formula
frequency = (rdpin_value × sysclk) / window_clocks
```


### Duty Cycle from Period Modes

**Using P_PERIODS_TICKS and P_PERIODS_HIGHS:**
```formula
duty_percent = (high_time × 100) / total_time
```

Where:

- `high_time` = RDPIN from P_PERIODS_HIGHS
- `total_time` = RDPIN from P_PERIODS_TICKS


## Quadrature Encoder

### Position to Degrees

**Formula:**
```formula
degrees = (position × 360) / counts_per_revolution
```

**Variables:**

- `position`: Quadrature count from RDPIN
- `counts_per_revolution`: 4 × encoder lines per revolution

**Worked Example (1000 line encoder, position 1000):**
```formula
counts_per_revolution = 4 × 1000 = 4000
degrees = (1000 × 360) / 4000 = 90°
```


### Velocity (Steps per Period)

**Formula:**
```formula
rpm = (steps_per_period × 60 × (1000 / period_ms)) / counts_per_revolution
```

**Worked Example (500 steps in 100ms, 4000 counts/rev):**
```formula
rpm = (500 × 60 × 10) / 4000 = 75 RPM
```


## Common sysclk Values

### Pre-Calculated Values at 200 MHz

| Frequency | NCO Y Value | PWM Frame (Sawtooth) |
|-----------|-------------|---------------------|
| 100 Hz | 2,147 | 2,000,000 |
| 1 kHz | 21,475 | 200,000 |
| 10 kHz | 214,748 | 20,000 |
| 100 kHz | 2,147,484 | 2,000 |
| 1 MHz | 21,474,836 | 200 |

### Common Baud Rates at 200 MHz

| Baud Rate | X[31:16] | Error |
|-----------|----------|-------|
| 9600 | 20833 | 0.00% |
| 19200 | 10417 | 0.00% |
| 38400 | 5208 | 0.01% |
| 57600 | 3472 | 0.01% |
| 115200 | 1736 | 0.01% |
| 230400 | 868 | 0.01% |
| 460800 | 434 | 0.01% |
| 921600 | 217 | 0.01% |
| 1000000 | 200 | 0.00% |

### ADC Resolution vs Speed at 200 MHz

| Resolution | X[3:0] | Sample Rate |
|------------|--------|-------------|
| 8 bits | %0111 | 1.56 MHz |
| 10 bits | %1001 | 390 kHz |
| 12 bits | %1011 | 97.6 kHz |
| 14 bits | %1101 | 24.4 kHz |


### Pre-Calculated Values at 250 MHz

| Frequency | NCO Y Value | PWM Frame (Sawtooth) |
|-----------|-------------|---------------------|
| 100 Hz | 1,718 | 2,500,000 |
| 1 kHz | 17,180 | 250,000 |
| 10 kHz | 171,799 | 25,000 |
| 100 kHz | 1,717,987 | 2,500 |
| 1 MHz | 17,179,869 | 250 |

### Common Baud Rates at 250 MHz

| Baud Rate | X[31:16] | Error |
|-----------|----------|-------|
| 9600 | 26042 | 0.00% |
| 19200 | 13021 | 0.00% |
| 38400 | 6510 | 0.01% |
| 57600 | 4340 | 0.01% |
| 115200 | 2170 | 0.01% |
| 230400 | 1085 | 0.01% |
| 460800 | 543 | 0.09% |
| 921600 | 271 | 0.10% |
| 1000000 | 250 | 0.00% |


### Pre-Calculated Values at 300 MHz

| Frequency | NCO Y Value | PWM Frame (Sawtooth) |
|-----------|-------------|---------------------|
| 100 Hz | 1,432 | 3,000,000 |
| 1 kHz | 14,317 | 300,000 |
| 10 kHz | 143,165 | 30,000 |
| 100 kHz | 1,431,656 | 3,000 |
| 1 MHz | 14,316,558 | 300 |

### Common Baud Rates at 300 MHz

| Baud Rate | X[31:16] | Error |
|-----------|----------|-------|
| 9600 | 31250 | 0.00% |
| 19200 | 15625 | 0.00% |
| 38400 | 7813 | 0.01% |
| 57600 | 5208 | 0.01% |
| 115200 | 2604 | 0.01% |
| 230400 | 1302 | 0.01% |
| 460800 | 651 | 0.01% |
| 921600 | 326 | 0.15% |
| 1000000 | 300 | 0.00% |

### Pre-Calculated Values at 350 MHz

| Frequency | NCO Y Value | PWM Frame (Sawtooth) |
|-----------|-------------|---------------------|
| 100 Hz | 1,227 | 3,500,000 |
| 1 kHz | 12,271 | 350,000 |
| 10 kHz | 122,713 | 35,000 |
| 100 kHz | 1,227,134 | 3,500 |
| 1 MHz | 12,271,335 | 350 |

### Common Baud Rates at 350 MHz

| Baud Rate | X[31:16] | Error |
|-----------|----------|-------|
| 9600 | 36458 | 0.00% |
| 19200 | 18229 | 0.00% |
| 38400 | 9115 | 0.00% |
| 57600 | 6076 | 0.01% |
| 115200 | 3038 | 0.01% |
| 230400 | 1519 | 0.01% |
| 460800 | 760 | 0.06% |
| 921600 | 380 | 0.06% |
| 1000000 | 350 | 0.00% |


## Accuracy Notes

### NCO Frequency

- Resolution: sysclk / 2^32
- At 200 MHz: ~0.047 Hz resolution
- Maximum frequency: sysclk / 2 (Nyquist limit)

### PWM

- Resolution determined by frame period
- Maximum useful resolution: 16 bits (frame = 65535)
- Duty cycle error: 1/frame × 100%

### UART Baud

- Error should be <3% for reliable communication
- Fractional timing (X[15:10]) provides <0.01% error
- Both transmitter and receiver errors accumulate

### ADC

- SINC2 sampling provides power-of-2 sample periods only
- SINC3 limited to 512 clocks maximum period
- Oversampling 4× provides ~1 additional bit resolution

### DAC

- 8-bit native resolution (256 levels)
- 16-bit dithered resolution requires low-pass filtering
- Output accuracy depends on power supply and loading


*This appendix provides formula reference. For P_ constants, see Appendix B. For application examples, see Appendix D.*
