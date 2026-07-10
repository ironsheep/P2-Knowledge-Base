# Chapter 16: ADC (Analog Input) {#ch16}

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

| Constant | P[9:7] | Role / Behavior |
|----------|----------|-------------|
| P_ADC_GIO | %000 | Internal **ground reference** — a calibration source, not a signal input |
| P_ADC_VIO | %001 | Internal **supply reference** — a calibration source, not a signal input |
| P_ADC_FLOAT | %010 | Floating input — self-biases to ~mid-supply (good for AC / capacitive coupling) |
| P_ADC_1X | %011 | Pin, unity gain — full-scale spans the supply rail (≈0V to 3.3V at 3.3V VIO) |
| P_ADC_3X | %100 | Pin, 3.16x gain (window below) |
| P_ADC_10X | %101 | Pin, 10x gain (window below) |
| P_ADC_30X | %110 | Pin, 31.6x gain (window below) |
| P_ADC_100X | %111 | Pin, 100x gain (window below) |

> **Gain modes measure *around* the ADC's mid-supply bias point (~VIO/2) — not up from ground.** A higher gain narrows the measurable window *symmetrically about mid-supply*; it does not rescale a 0 V-referenced range. A ground-referenced small signal (a 0-100 mV sensor sitting near 0 V) cannot be read directly by a gain mode — bias it to mid-supply first, or use the ratiometric reference method in §16.3.

The per-gain input windows below were **measured on a real P2** (one sample; the on-chip DAC driven through a pin-to-pin loopback into the ADC). Every gain centers on ~VIO/2, and the windows narrow ~3.16x per gain step. Treat them as **representative** — the exact endpoints vary part-to-part and with VIO and temperature, so calibrate for absolute work.

| Mode | Gain | Input window (measured, VIO ~3.3 V) |
|------|------|-------------------------------------|
| P_ADC_1X | 1x | 0-3.3 V (full rail) |
| P_ADC_3X | 3.16x | ~0.9-2.4 V |
| P_ADC_10X | 10x | ~1.4-1.9 V |
| P_ADC_30X | 31.6x | ~1.57-1.71 V |
| P_ADC_100X | 100x | ~1.61-1.66 V |

### Choosing an Input Mode

**P_ADC_1X (unity-gain pin read):**

- The general-purpose mode for reading a voltage on a pin
- Full-scale spans the supply rail (≈0V to 3.3V at 3.3V VIO)
- Best for pots and sensors that swing across the rail

**P_ADC_GIO / P_ADC_VIO (calibration references):**

- Not signal inputs — they read the chip's own internal ground and supply references
- Used to calibrate a pin reading against known endpoints (ratiometric method, §16.3)

**P_ADC_3X through P_ADC_100X (gain modes):**

- Increase sensitivity to small signals *centered on the ADC's mid-supply bias point*
- Higher gain = a narrower measurable window about mid-supply (not a smaller 0-referenced range)
- A ground-referenced small signal must be biased to mid-supply first (or read ratiometrically, §16.3)

**Example: Gain Selection**
```spin2
' Gain modes measure about mid-supply (~VIO/2), not up from 0V.
' A ground-referenced 0-100mV sensor must be biased to mid-supply first,
' or read ratiometrically (Section 16.3).
WRPIN(pin, P_ADC_30X | P_ADC)   ' 31.6x sensitivity about mid-supply
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

| X[3:0] | Sample Period | SINC2 Sample | SINC2 Filter | SINC3 Filter† | Bitstream |
|--------|---------------|--------------|--------------|---------------|-----------|
| %0001 | 2 clocks | 2 bits | - | - | 2 new bits |
| %0011 | 8 clocks | 4 bits | 4 bits | - | 8 new bits |
| %0101 | 32 clocks | 6 bits | 6 bits | 10 bits | 32 new bits |
| %0111 | 128 clocks | 8 bits | 8 bits | 14 bits | overflow |
| %1001 | 512 clocks | 10 bits | 10 bits | 18 bits | overflow |
| %1011 | 2048 clocks | 12 bits | 12 bits | overflow | overflow |
| %1101 | 8192 clocks | 14 bits | 14 bits | overflow | overflow |

*The bit figures above are **nominal resolution** — the width the decimation math produces — **not ENOB.** ENOB (Effective Number of Bits) is the *measured* effective resolution after noise and distortion; on the P2 it is lower than these nominal figures and must be characterized on your own hardware (see §16.8 Accuracy Considerations).*

† **SINC3 Filter:** the higher SINC3 figures assume an idealized doubling over simple bit-summing that the P2's ADC does not actually deliver — treat them as optimistic upper bounds, not attainable resolution.

> **Beyond 14 bits — the instrumentation ceiling.** The table stops at 14 bits because that is the single-conversion SINC2 limit. Reaching further is possible by running SINC2 *filtering* mode fast and **summing many per-period differentials** over a long integration window (optionally with input gain ahead of it): each doubling of the accumulated sample count buys roughly another half-bit, and long integrations push into **16–17-bit / microvolt territory**. This is a *mechanism*, not a guaranteed specification — and these are *nominal* resolutions, the bit-width the accumulation produces. The *effective* number of bits (ENOB) actually measured is lower still, because it accounts for noise and distortion; it depends on the board, the source impedance, the VIO supply, and temperature (see §16.8 Accuracy Considerations, and the ratiometric method later in this section). Any specific ENOB figure is a bench result for a *particular* rig, never a datasheet value.

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
  WRPIN(ADC_PIN, P_ADC_1X | P_ADC)
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
  WRPIN(ADC_PIN, P_ADC_1X | P_ADC)
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

SINC3 provides better dynamic response than SINC2, roughly doubling the nominal bit-count over simple bit-summing for fast-changing signals (at DC it is only marginally better than SINC2). Limited to 512 samples per period due to 27-bit accumulator.

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

> **Two things the post-processing must get right.**
>
> - **Warm-up.** The difference math depends on a valid prior accumulator state, so the filter is only accurate **from the second period for SINC2, and from the third period for SINC3.** Discard the first reading (SINC2) or the first two (SINC3) after starting.
> - **Normalization.** To right-justify the differenced result, apply a final right-shift sized to the sample count: `LOG2(samples) - 1` bits for SINC2, `LOG2(samples)` bits for SINC3 (e.g. 128 samples → 6 for SINC2). The shift tracks the sample period, so it changes whenever X changes.

> **Startup warm-up and source-switch flush are two different discards.** The warm-up above is a *one-time* settling of the differencing filter when the smart pin first starts. A **separate** discard applies every time the input source **changes** (for example GIO → VIO → pin in the instrumentation method below): switching the ADC's reference contaminates the **first 3 samples** — two for the SINC filter to decimate the step through, plus one for the analog front end to settle — so the **4th sample after a source switch is the first clean one.** A steady single-source reading pays only the startup warm-up, once; a method that rotates among sources pays the 3-sample flush on every switch.

### Bitstream Capture Mode (%11)

Captures raw ADC bitstream for custom processing algorithms.

```spin2
PUB bitstream_init()
  WRPIN(ADC_PIN, P_ADC_1X | P_ADC)
  WXPIN(ADC_PIN, %11_0101)                    ' Bitstream, 32 bits
  PINH(ADC_PIN)

PUB read_bitstream() : bits
  REPEAT UNTIL PINREAD(ADC_PIN)
  bits := RDPIN(ADC_PIN)                      ' 32 bits, LSB = oldest
```

### Ratiometric Absolute-Voltage Instrumentation

The gain and filter modes above turn the pin reading into a *number*, but that number is relative to the ADC's own internal references — which themselves drift with supply and temperature. To recover an **absolute** voltage in microvolts, measure the pin against the chip's two internal references and scale ratiometrically. This is the foundation of single-pin instrumentation measurement on the P2; the complete, runnable builds live in the P2AN001 application note, so the sketch here stays minimal.

**Read all three sources.** The ADC input can be switched among the internal ground reference (`P_ADC_GIO`), the internal supply reference (`P_ADC_VIO`), and the external pin. Absolute voltage needs **all three** — the shortcut of reading only `P_ADC_FLOAT` and the pin is far noisier, because the float point only *approximately* sits mid-supply. Read each reference from the same pin in turn, then place the pin between them:

```formula
uV = (pin − GIO) / (VIO − GIO) × 3,300,000
```

```spin2
PUB read_microvolts() : uv | gio, vio, pin
  ' Read each reference from the same pin, in turn.
  gio := read_source(P_ADC_GIO)                ' internal ground reference
  vio := read_source(P_ADC_VIO)                ' internal supply reference
  pin := read_source(P_ADC_1X)                 ' the external pin
  ' Ratiometric: where does the pin sit between GIO and VIO?
  ' muldiv64 keeps the (pin - gio) x 3_300_000 product at 64 bits.
  uv := muldiv64(pin - gio, 3_300_000, vio - gio)

PRI read_source(input_mode) : sample | acc, last
  WRPIN(ADC_PIN, input_mode | P_ADC)
  WXPIN(ADC_PIN, %01_0111)                     ' SINC2 filtering, 128 clocks
  PINH(ADC_PIN)
  ' Switching the source contaminates the first 3 samples; the 4th is
  ' the first clean one (see the source-switch flush note above).
  last := RDPIN(ADC_PIN)
  REPEAT 4
    REPEAT UNTIL PINREAD(ADC_PIN)
    acc    := RDPIN(ADC_PIN)
    sample := acc - last
    last   := acc
```

**The references are local to the pin's power group.** The P2 powers its I/O pins in **isolated groups of four** — pins 0–3, 4–7, 8–11, …, 60–63 — and each group shares a single VIO/GIO supply pair (P2 datasheet, pin descriptions). When a pin's ADC selects `P_ADC_GIO` or `P_ADC_VIO`, it measures *its own group's* ground and supply rails. This is what makes the single-pin ratiometric reading absolute: pin, GIO, and VIO are all referenced to the same local domain, so the supply and temperature drift common to all three divides out. It also carries a layout rule for multi-pin work (§16.6): pins tied together for one measurement should sit **within a single group**, so they share one reference domain — straddling a group boundary mixes supply domains and degrades the result.

**Handle the out-of-band cases.** Both edges of the formula are legitimate readings, not errors:

- **Below ground** (`pin < GIO`): `pin - GIO` is negative, so `uv` is negative — the signal sits below the ground reference (below 0 V).
- **Over-range** (`pin > VIO`): `pin - GIO` exceeds `VIO - GIO`, so `uv` exceeds 3,300,000 µV — the signal is above the supply reference. Clamp or flag these as the application requires.

How close the absolute number lands depends on the front-end limits in §16.8 — most importantly the matched-resistor absolute-error floor, which no amount of averaging removes.


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

Use WYPIN to override the power-of-2 period from X[3:0] with an arbitrary value in **Y[13:0]**:

> The WYPIN override only applies when **X[5:4] > %00** — i.e. in SINC2 Filtering, SINC3 Filtering, or Bitstream modes. In **SINC2 Sampling (X[5:4] = %00)** the period is fixed by X[3:0] and WYPIN has no effect, so a non-power-of-2 rate there requires one of the filtering modes instead.


```spin2
WRPIN(ADC_PIN, P_ADC_EXT | P_PLUS1_B)
WXPIN(ADC_PIN, %10_0111)                      ' SINC3 base
WYPIN(ADC_PIN, 320)                          ' Override: 320 clock period
PINH(ADC_PIN)
```

### Accumulator Limits

| Filter | Max Period | Why |
|--------|------------|-----|
| SINC2 | 11,585 clocks | 27-bit accumulator: 2^(27/2)^ |
| SINC3 | 512 clocks | 27-bit accumulator: 2^(27/3)^ |


## 16.5 Mode %11010: P_ADC_SCOPE (Triggered Capture)

### Purpose

Oscilloscope-style triggered acquisition for capturing signal events. Supports four simultaneous ADC channels with hysteretic triggering.

### Four-Channel Architecture

The scope mode captures from four consecutive pins simultaneously. Pin numbers must be multiples of 4 (0, 4, 8, ..., 60).

```layout
Pin group starting at 52:
  Pin 52: Channel 0
  Pin 53: Channel 1
  Pin 54: Channel 2
  Pin 55: Channel 3
  (each channel has its own independent hysteretic trigger)
```

### Configuration

```spin2
CON
  SCOPE_BASE = 52                             ' Must be multiple of 4

PUB scope_init(trigger_config)
  ' Configure 4 consecutive pins for scope mode
  WRPIN(SCOPE_BASE, P_ADC_1X | P_ADC_SCOPE)
  WXPIN(SCOPE_BASE, trigger_config)
  PINH(SCOPE_BASE)
```

### X Register: Trigger Configuration

```layout
X[15:10]: B (trigger) value, 6-bit MSB-justified (0-252, step 4)
X[7:2]:   A (arm) value, 6-bit MSB-justified (0-252, step 4)
X[1:0]:   Filter: %00 = 68-tap Tukey, %01 = 45-tap Tukey, %1x = 28-tap Hann
```

The hysteretic trigger works as follows:

1. Signal must cross arm level to arm the trigger
2. Signal must then cross trigger level to fire
3. Data capture begins after trigger fires

### Reading Scope Data

```pasm2
              ' Enable the SCOPE data pipe (D[6]=1) and point it at the
              ' 4-pin block (D[5:2] = base pin) before reading it:
              setscp    #%0100_0000 | SCOPE_BASE
              getscp    combined           ' Read all 4 channels (32-bit)
              ' combined = [ch3][ch2][ch1][ch0], 8 bits each

              ' Or read individual pins:
              rdpin     ch0, #SCOPE_BASE
              rdpin     ch1, #SCOPE_BASE+1
              rdpin     ch2, #SCOPE_BASE+2
              rdpin     ch3, #SCOPE_BASE+3
```


## 16.6 Multi-Channel ADC

> **Power-domain layout.** The P2 powers its pins in isolated groups of four (§16.3) — pins 0–3, 4–7, …, 60–63, each group on its own VIO/GIO pair. This shapes multi-channel layout two ways: each pin's `P_ADC_GIO`/`P_ADC_VIO` references *its own* group, so an independent channel is self-consistent wherever it sits; but any pins tied to a *shared* node (as in a constant-impedance multi-pin instrument) must sit within one group to share a reference domain. The example below spans pins 40–47 — two full groups (40–43, 44–47) — which is fine because the channels are independent.

### Configuring Multiple Pins

Configure each pin individually:

```spin2
CON
  ADC_BASE = 40
  NUM_CHANNELS = 8

PUB multi_adc_init() | ch
  REPEAT ch FROM 0 TO NUM_CHANNELS-1
    WRPIN(ADC_BASE + ch, P_ADC_1X | P_ADC)
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
  WRPIN(POT_PIN, P_ADC_1X | P_ADC)
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

```{.spin2 caption="ch16-adc-audio-capture.spin2"}
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
  WRPIN(AUDIO_PIN, P_ADC_FLOAT | P_ADC)
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

> **Feeding a microphone: no bias network needed.** This example uses `P_ADC_FLOAT`, the floating pin input that **self-biases to roughly mid-supply**, so an AC source such as an electret microphone couples straight in through a single series capacitor — no external bias-divider resistors. That self-bias point is only *approximately* VIO/2, so for absolute-voltage work use the ratiometric three-reference method in §16.3; for audio (AC, where only the changes matter) the approximate midpoint is exactly what audio needs.

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

  ' Discard the first reading (SINC2 is valid from the 2nd period)
  REPEAT UNTIL PINREAD(SENSOR_PIN)
  ack := RDPIN(SENSOR_PIN)                 ' discard warm-up sample

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

Gain modes raise sensitivity *around the ADC's mid-supply bias point* (~VIO/2), so
the small signal must sit near mid-supply — not at ground. A raw thermocouple (tens
of millivolts referenced to ground) needs a bias network to lift it to mid-supply,
or the ratiometric reference method (§16.3); it cannot be read directly by a gain
mode. This example configures a gain mode for a signal already biased to mid-supply
and reads the filtered result. Converting that reading to volts needs the per-gain
input window, which is being characterized on hardware (see §16.2).

```spin2
CON
  _clkfreq = 200_000_000
  SIGNAL_PIN = 46                 ' small signal, biased to mid-supply

PUB read_small_signal() : sample
  WRPIN(SIGNAL_PIN, P_ADC_100X | P_ADC)       ' 100x about mid-supply
  WXPIN(SIGNAL_PIN, %00_1001)                 ' SINC2 sampling, 10-bit
  PINH(SIGNAL_PIN)

  WAITMS(1)                                   ' let filter stabilize

  sample := RDPIN(SIGNAL_PIN)                 ' filtered result
```

### Example 5: PASM2 ADC with Event Detection

```pasm2
CON
  _clkfreq = 200_000_000
  ADC_PIN = 46

DAT           org

              ' Initialize ADC
              dirl      #ADC_PIN
              wrpin     ##P_ADC_1X | P_ADC, #ADC_PIN
              wxpin     #%00_0111, #ADC_PIN   ' 8-bit SINC2
              dirh      #ADC_PIN

              ' Set up event detection for IN flag
              setse1    #%001<<6 + ADC_PIN    ' Event on IN rising edge

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

### Hardware Limits

Some bounds come from the analog front end itself and **cannot be averaged away** — know them before promising absolute accuracy:

- **High input impedance.** The 1× range presents a high input impedance, so a low-impedance source loads it lightly. A high-impedance source — or a large external series resistor — forms a divider with it that shifts the reading. Buffer high-Z sources, or account for the divider.
- **Absolute-error floor.** A single pin's absolute error is small — a few millivolts (≤ ~9 mV measured on real P2 silicon; representative, not a guaranteed spec). The larger concern is **pin-to-pin spread**: the GIO, VIO, and pin paths use three *separate* matched on-chip resistors that do not match perfectly, so different pins can read a bit apart in absolute terms. This is a design limit, not noise — more averaging will not remove it. Where absolute accuracy matters, self-calibrate by driving the pin to each rail and measuring the result, or characterize the per-pin offset once.
- **Supply and temperature sensitivity.** The internal references track the VIO supply, so a noisy switch-mode VIO degrades precision — feed VIO from a clean LDO for instrumentation work. GIO and VIO also drift with temperature (VIO is the more stable of the two), giving each chip a per-pin fingerprint; periodic re-referencing handles the slow drift.
- **Power-of-2 sample period.** In SINC2 sampling mode the period must be a power of two (`2^X[3:0]`) and cannot be freely dithered (§16.3, Resolution and Sample Rate).

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
| P_ADC_GIO | Internal ground reference (calibration) |
| P_ADC_VIO | Internal supply reference (calibration) |
| P_ADC_FLOAT | Floating input (self-biases to ~mid-supply) |
| P_ADC_1X | Pin, unity gain — 0-3.3 V (full rail) |
| P_ADC_3X | Pin, 3.16x gain — window ~0.9-2.4 V (measured, about mid-supply) |
| P_ADC_10X | Pin, 10x gain — window ~1.4-1.9 V |
| P_ADC_30X | Pin, 31.6x gain — window ~1.57-1.71 V |
| P_ADC_100X | Pin, 100x gain — window ~1.61-1.66 V |

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
