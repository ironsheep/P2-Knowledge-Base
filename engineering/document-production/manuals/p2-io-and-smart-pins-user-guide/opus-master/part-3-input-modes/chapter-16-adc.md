# Chapter 16: ADC (Analog Input)

This chapter covers the P2's analog-to-digital conversion capabilities using smart pin modes P_ADC (%11000), P_ADC_EXT (%11001), and P_ADC_SCOPE (%11010). Topics include internal/external clocking, SINC filtering, gain settings, and triggered acquisition.


## 16.1 ADC Architecture

### Overview

The P2 includes a sigma-delta ADC on every I/O pin. Unlike traditional SAR or flash ADCs, sigma-delta ADCs oversample a single bit and use digital filtering to achieve multi-bit resolution. The smart pin modes provide hardware filtering with optional software post-processing.

```{=latex}
\DiagAdcChain
```

### ADC Modes

| Mode | Constant | Description |
|------|----------|-------------|
| %11000 | P_ADC | Internal clock ADC with filtering |
| %11001 | P_ADC_EXT | External clock ADC for delta-sigma integration |
| %11010 | P_ADC_SCOPE | Triggered oscilloscope-style capture |

### Pin Configuration

ADC operation requires specific pin mode bits. Set P[12:10] = %100 in the WRPIN value:

```{=latex}
\DiagAdcEnableField
```


## 16.2 ADC Input Modes

### Input Configuration Options

| Constant | P[16:14] | Description | Input Range |
|----------|----------|-------------|-------------|
| P_ADC_GIO | %000 | Ground-referenced | 0V to 3.3V |
| P_ADC_VIO | %001 | VIO-referenced | VIO-relative |
| P_ADC_FLOAT | %010 | Floating input | Self-biased |
| P_ADC_1X | %011 | 1x gain | 0V to 3.3V |
| P_ADC_3X | %100 | 3.16x gain | 0V to ~1.04V |
| P_ADC_10X | %101 | 10x gain | 0V to 330mV |
| P_ADC_30X | %110 | 31.6x gain | 0V to ~104mV |
| P_ADC_100X | %111 | 100x gain | 0V to 33mV |

### Choosing an Input Mode

**P_ADC_GIO (Ground-referenced):**

- Most common mode for general-purpose ADC
- Full 0V to 3.3V range
- Best for sensors and potentiometers

**P_ADC_1X through P_ADC_100X (Gain modes):**

- Amplify small signals before conversion
- Reduce noise by using more of the ADC range
- Higher gain = smaller input range

**Example: Gain Selection**
```spin2
' For a 0-100mV sensor, use 30x gain
' 100mV × 31.6 = 3.16V (uses most of ADC range)
WRPIN(pin, P_ADC_30X | P_ADC)
```


## 16.3 Mode %11000: P_ADC (Internal Clock)

### Operation

Samples the analog input at the system clock rate and applies SINC filtering to produce multi-bit samples. The filter type and sample period determine resolution and update rate.

### X Register Configuration

```layout
X[5:4]: Filter mode
X[3:0]: Sample period = 2^(X[3:0]) clocks
```

**Filter Modes:**

| X[5:4] | Mode | Description |
|--------|------|-------------|
| %00 | SINC2 Sampling | Complete conversion in hardware |
| %01 | SINC2 Filtering | Requires software difference computation |
| %10 | SINC3 Filtering | Requires software multi-stage difference |
| %11 | Bitstream Capture | Raw bits (LSB = oldest) |

### Resolution and Sample Rate

| X[3:0] | Sample Period | SINC2 Sample | SINC2 Filter | SINC3 Filter | Bitstream |
|--------|---------------|--------------|--------------|--------------|-----------|
| %0001 | 2 clocks | 2 bits | - | - | 2 new bits |
| %0011 | 8 clocks | 4 bits | 4 ENOB | - | 8 new bits |
| %0101 | 32 clocks | 6 bits | 6 ENOB | 10 ENOB | 32 new bits |
| %0111 | 128 clocks | 8 bits | 8 ENOB | 14 ENOB | overflow |
| %1001 | 512 clocks | 10 bits | 10 ENOB | 18 ENOB | overflow |
| %1011 | 2048 clocks | 12 bits | 12 ENOB | overflow | overflow |
| %1101 | 8192 clocks | 14 bits | 14 ENOB | overflow | overflow |

*ENOB = Effective Number of Bits*

### Sample Rate Calculation

```formula
sample_rate = sysclk / 2^(X[3:0])
```

At 200 MHz with X[3:0] = %0111 (128 clocks):
```formula
sample_rate = 200_000_000 / 128 = 1,562,500 samples/sec
```

### SINC2 Sampling Mode (%00)

**Advantages:**

- Complete conversion in hardware
- Just read RDPIN for latest sample
- Power-of-2 sample periods only

**Configuration:**
```spin2
CON
  _clkfreq = 200_000_000
  ADC_PIN = 46

PUB adc_init()
  ' Configure ADC with 8-bit SINC2 sampling
  WRPIN(ADC_PIN, P_ADC_GIO | P_ADC)
  WXPIN(ADC_PIN, %00_0111)                   ' SINC2 sampling, 128 clocks
  PINH(ADC_PIN)                               ' Enable smart pin

PUB read_adc() : value
  value := RDPIN(ADC_PIN)                     ' Get latest sample
```

### SINC2 Filtering Mode (%01)

Requires software post-processing to compute the difference between consecutive accumulator readings.

**Configuration:**
```spin2
PUB sinc2_init()
  WRPIN(ADC_PIN, P_ADC_GIO | P_ADC)
  WXPIN(ADC_PIN, %01_0111)                  ' SINC2 filtering, 128 clocks
  PINH(ADC_PIN)

PUB sinc2_read() : sample | acc
  REPEAT UNTIL PINREAD(ADC_PIN)               ' Wait for new sample
  acc := RDPIN(ADC_PIN)                       ' Get accumulator
  sample := acc - last_acc                    ' Compute difference
  last_acc := acc                             ' Save for next time
```

**PASM2 Implementation:**
```pasm2
              rdpin     x, #ADC_PIN           ' Get SINC2 accumulator
              shl       x, #5                 ' Prescale 27-bit to 32-bit
              sub       x, diff               ' Compute sample
              add       diff, x               ' Update diff value
              ' x now contains the sample
```

### SINC3 Filtering Mode (%10)

SINC3 provides better dynamic response than SINC2, doubling the effective bits for fast-changing signals. Limited to 512 samples per period due to 27-bit accumulator.

**Post-processing:**
```pasm2
              rdpin     x, #ADC_PIN           ' Get SINC3 accumulator
              shl       x, #5                 ' Prescale to 32-bit
              sub       x, diff1              ' First difference
              add       diff1, x
              sub       x, diff2              ' Second difference
              add       diff2, x
              sub       x, diff3              ' Third difference
              add       diff3, x
              ' x now contains the sample
```

### Bitstream Capture Mode (%11)

Captures raw ADC bitstream for custom processing algorithms.

```spin2
PUB bitstream_init()
  WRPIN(ADC_PIN, P_ADC_GIO | P_ADC)
  WXPIN(ADC_PIN, %11_0101)                    ' Bitstream, 32 bits
  PINH(ADC_PIN)

PUB read_bitstream() : bits
  REPEAT UNTIL PINREAD(ADC_PIN)
  bits := RDPIN(ADC_PIN)                      ' 32 bits, LSB = oldest
```


## 16.4 Mode %11001: P_ADC_EXT (External Clock)

### Purpose

For interfacing with external delta-sigma ADC chips. Samples A-input data on B-input rising edges, allowing the P2 to apply SINC filtering to external ADC bitstreams.

### Configuration

```spin2
CON
  DATA_PIN = 20                               ' A-input: ADC data
  CLOCK_PIN = 21                              ' B-input: ADC clock

PUB external_adc_init()
  ' External ADC with SINC2 sampling
  WRPIN(DATA_PIN, P_ADC_EXT | P_PLUS1_B)      ' Use next pin as clock
  WXPIN(DATA_PIN, %00_0111)                   ' SINC2, 8-bit
  PINH(DATA_PIN)
```

### Custom Sample Periods

Use WYPIN to override the power-of-2 period from X[3:0]:

```spin2
WRPIN(ADC_PIN, P_ADC_EXT | P_PLUS1_B)
WXPIN(ADC_PIN, %10_0111)                      ' SINC3 base
WYPIN(ADC_PIN, 320)                          ' Override: 320 clock period
PINH(ADC_PIN)
```

### Accumulator Limits

| Filter | Max Period | Why |
|--------|------------|-----|
| SINC2 | 11,585 clocks | 27-bit accumulator: 2^(27/2) |
| SINC3 | 512 clocks | 27-bit accumulator: 2^(27/3) |


## 16.5 Mode %11010: P_ADC_SCOPE (Triggered Capture)

### Purpose

Oscilloscope-style triggered acquisition for capturing signal events. Supports four simultaneous ADC channels with hysteretic triggering.

### Four-Channel Architecture

The scope mode captures from four consecutive pins simultaneously. Pin numbers must be multiples of 4 (0, 4, 8, 12, ..., 52).

```
Pin group starting at 52:
  Pin 52: Channel 0 (and trigger source)
  Pin 53: Channel 1
  Pin 54: Channel 2
  Pin 55: Channel 3
```

### Configuration

```spin2
CON
  SCOPE_BASE = 52                             ' Must be multiple of 4

PUB scope_init(trigger_config)
  ' Configure 4 consecutive pins for scope mode
  WRPIN(SCOPE_BASE, P_ADC_GIO | P_ADC_SCOPE)
  WXPIN(SCOPE_BASE, trigger_config)
  PINH(SCOPE_BASE)
```

### X Register: Trigger Configuration

```layout
X[15:8]: Trigger level (0-252, multiples of 4)
X[7:0]: Arm level (0-252, multiples of 4)
```

The hysteretic trigger works as follows:

1. Signal must cross arm level to arm the trigger
2. Signal must then cross trigger level to fire
3. Data capture begins after trigger fires

### Reading Scope Data

```pasm2
              getscp    combined           ' Read all 4 channels (32-bit)
              ' combined = [ch3][ch2][ch1][ch0], 8 bits each

              ' Or read individual pins:
              rdpin     ch0, #SCOPE_BASE
              rdpin     ch1, #SCOPE_BASE+1
              rdpin     ch2, #SCOPE_BASE+2
              rdpin     ch3, #SCOPE_BASE+3
```


## 16.6 Multi-Channel ADC

### Configuring Multiple Pins

Configure each pin individually:

```spin2
CON
  ADC_BASE = 40
  NUM_CHANNELS = 8

PUB multi_adc_init() | ch
  REPEAT ch FROM 0 TO NUM_CHANNELS-1
    WRPIN(ADC_BASE + ch, P_ADC_GIO | P_ADC)
    WXPIN(ADC_BASE + ch, %00_0111)            ' 8-bit SINC2
    PINH(ADC_BASE + ch)

PUB read_all_channels(ptr) | ch
  REPEAT ch FROM 0 TO NUM_CHANNELS-1
    LONG[ptr][ch] := RDPIN(ADC_BASE + ch)
```

### Simultaneous Configuration

Configure multiple pins with a single WRPIN using pin group encoding:

```pasm2
              ' Configure pins 16-23 simultaneously
              ' Pin group: bits [10:6] = additional pins (7)
              ' Base pin: bits [5:0] = starting pin (16)
              mov       pinaddr, #%00111_010000   ' 8 pins starting at 16
              wrpin     adc_mode, pinaddr
              wxpin     #%00_0111, pinaddr
              dirh      pinaddr
```


## 16.7 Practical Examples

### Example 1: Simple Potentiometer Reading

```spin2
CON
  _clkfreq = 200_000_000
  POT_PIN = 46
  LED_BASE = 56

PUB main() | adc_value, led_bits, i
  ' Initialize ADC - 8-bit, ~1.5 MHz sample rate
  WRPIN(POT_PIN, P_ADC_GIO | P_ADC)
  WXPIN(POT_PIN, %00_0111)
  PINH(POT_PIN)

  ' Initialize LED outputs
  REPEAT i FROM 0 TO 7
    PINLOW(LED_BASE + i)

  REPEAT
    adc_value := RDPIN(POT_PIN)

    ' Display value on 8 LEDs
    REPEAT i FROM 0 TO 7
      IF adc_value.[i]
        PINHIGH(LED_BASE + i)
      ELSE
        PINLOW(LED_BASE + i)

    WAITMS(50)
```

### Example 2: Audio Sampling

```spin2
CON
  _clkfreq = 200_000_000
  AUDIO_PIN = 46
  SAMPLE_RATE = 44100
  BUFFER_SIZE = 1024

VAR
  long audio_buffer[BUFFER_SIZE]
  long buffer_index

PUB main() | sample_period
  ' Calculate sample period for 44.1 kHz
  sample_period := _clkfreq / SAMPLE_RATE     ' ~4535 clocks

  ' Configure ADC with SINC2 sampling
  ' Use period override for exact rate
  WRPIN(AUDIO_PIN, P_ADC_GIO | P_ADC)
  WXPIN(AUDIO_PIN, %01_1100)                  ' SINC2 filter, base period
  WYPIN(AUDIO_PIN, sample_period)             ' Override period
  PINH(AUDIO_PIN)

  REPEAT
    capture_buffer()
    process_audio()

PRI capture_buffer() | i, last_acc, acc
  last_acc := RDPIN(AUDIO_PIN)

  REPEAT i FROM 0 TO BUFFER_SIZE-1
    REPEAT UNTIL PINREAD(AUDIO_PIN)
    acc := RDPIN(AUDIO_PIN)
    audio_buffer[i] := acc - last_acc         ' SINC2 difference
    last_acc := acc

PRI process_audio()
  ' Application-specific audio processing of audio_buffer[]
```

### Example 3: High-Resolution DC Measurement

```spin2
CON
  _clkfreq = 200_000_000
  SENSOR_PIN = 46

PUB measure_voltage() : millivolts | sample, last_acc, acc, ack
  ' 14-bit resolution with SINC2 (8192 clocks)
  WRPIN(SENSOR_PIN, P_ADC_1X | P_ADC)
  WXPIN(SENSOR_PIN, %01_1101)                 ' SINC2 filter, 14-bit
  PINH(SENSOR_PIN)

  ' Wait for filter to stabilize (2 periods)
  REPEAT 2
    REPEAT UNTIL PINREAD(SENSOR_PIN)
    ack := RDPIN(SENSOR_PIN)               ' Discard stabilization sample

  ' Get actual measurement
  REPEAT UNTIL PINREAD(SENSOR_PIN)
  last_acc := RDPIN(SENSOR_PIN)
  REPEAT UNTIL PINREAD(SENSOR_PIN)
  acc := RDPIN(SENSOR_PIN)

  sample := (acc - last_acc) & $3FFF          ' 14-bit value

  ' Convert to millivolts (0-3300mV for 0-16383)
  millivolts := (sample * 3300) / 16383
```

### Example 4: Small Signal with Gain

```spin2
CON
  _clkfreq = 200_000_000
  THERMOCOUPLE_PIN = 46                 ' Range ~0-50mV depending on type

PUB read_thermocouple() : microvolts | sample
  ' Use 100x gain: 33mV max input → full ADC range
  WRPIN(THERMOCOUPLE_PIN, P_ADC_100X | P_ADC)
  WXPIN(THERMOCOUPLE_PIN, %00_1001)           ' SINC2 sampling, 10-bit
  PINH(THERMOCOUPLE_PIN)

  WAITMS(1)                                   ' Let filter stabilize

  sample := RDPIN(THERMOCOUPLE_PIN)

  ' Convert: 0-1023 → 0-33000 µV (0-33mV at 100x gain)
  microvolts := (sample * 33000) / 1023
```

### Example 5: PASM2 ADC with Event Detection

```pasm2
CON
  _clkfreq = 200_000_000
  ADC_PIN = 46

DAT           org

              ' Initialize ADC
              dirl      #ADC_PIN
              wrpin     ##P_ADC_GIO | P_ADC, #ADC_PIN
              wxpin     #%00_0111, #ADC_PIN   ' 8-bit SINC2
              dirh      #ADC_PIN

              ' Set up event detection for IN flag
              setse1    #%001<<6 + ADC_PIN    ' Event on IN high

.loop
              waitse1                         ' Wait for sample ready
              rdpin     sample, #ADC_PIN      ' Read sample

              ' Process sample...
              cmp       sample, threshold wc   ' Compare to threshold
        if_c  call      #below_threshold
        if_nc call      #above_threshold

              jmp       #.loop

sample        res       1
threshold     long      128                   ' Mid-scale threshold
```


## 16.8 Accuracy Considerations

### Noise Sources

| Source | Effect | Mitigation |
|--------|--------|------------|
| Supply noise | Adds to conversion | Clean power supply, decoupling |
| Digital crosstalk | Couples into analog | Separate analog from digital |
| Input impedance | Source loading | Low-impedance source |
| Temperature | Offset drift | Periodic calibration |

### Improving Accuracy

**Averaging:**
```spin2
PUB averaged_reading(num_samples) : average | sum, i
  sum := 0
  REPEAT num_samples
    REPEAT UNTIL PINREAD(ADC_PIN)
    sum += RDPIN(ADC_PIN)
  average := sum / num_samples
```

**Oversampling for Extra Bits:**
Each 4x oversampling adds approximately 1 bit of resolution.

**Calibration:**
```spin2
VAR
  long adc_offset                             ' Zero offset
  long adc_scale                              ' Gain factor

PUB calibrate()
  ' Connect input to ground
  adc_offset := read_averaged(100)

  ' Connect input to known voltage (e.g., 2.5V)
  ' Expected value for 8-bit: (2.5/3.3) × 255 = 193
  adc_scale := (193 * 256) / (read_averaged(100) - adc_offset)

PUB calibrated_read() : value
  value := RDPIN(ADC_PIN)
  value := ((value - adc_offset) * adc_scale) >> 8
```

### Resolution vs Speed Trade-off

| Resolution | Sample Period | Sample Rate at 200 MHz |
|------------|---------------|------------------------|
| 8 bits | 128 clocks | 1.56 MHz |
| 10 bits | 512 clocks | 390 kHz |
| 12 bits | 2048 clocks | 97.6 kHz |
| 14 bits | 8192 clocks | 24.4 kHz |


## 16.9 Quick Reference

### Mode Constants

| Constant | Mode | Description |
|----------|------|-------------|
| P_ADC | %11000 | Internal clock ADC |
| P_ADC_EXT | %11001 | External clock ADC |
| P_ADC_SCOPE | %11010 | Triggered scope capture |

### Input Mode Constants

| Constant | Function |
|----------|----------|
| P_ADC_GIO | Ground-referenced input |
| P_ADC_VIO | VIO-referenced input |
| P_ADC_FLOAT | Floating input |
| P_ADC_1X | 1x gain (0-3.3V) |
| P_ADC_3X | 3.16x gain (0-1.04V) |
| P_ADC_10X | 10x gain (0-330mV) |
| P_ADC_30X | 31.6x gain (0-104mV) |
| P_ADC_100X | 100x gain (0-33mV) |

### Filter Mode Summary

| X[5:4] | Mode | Post-Processing |
|--------|------|-----------------|
| %00 | SINC2 Sampling | None (hardware complete) |
| %01 | SINC2 Filtering | Software difference |
| %10 | SINC3 Filtering | Software triple difference |
| %11 | Bitstream | Custom processing |

### Sample Rate Formula

```formula
sample_rate = sysclk / 2^(X[3:0])
```

Or with WYPIN override:
```formula
sample_rate = sysclk / WYPIN_value
```

### Voltage Conversion

For P_ADC_1X (0-3.3V range):
```formula
voltage_mv = (sample × 3300) / full_scale
```

Where full_scale depends on resolution (255 for 8-bit, 16383 for 14-bit).


*This chapter covered analog-to-digital conversion. For serial reception, see Chapter 17. For USB, see Chapter 19.*
