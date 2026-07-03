# Chapter 18: Repository — Inter-Cog Data Sharing {#ch18}

This chapter covers the repository modes (%00001-%00011) that serve dual purposes: inter-cog data sharing via the long repository function, and high-resolution DAC output with dithering. These modes provide hardware-arbitrated data transfer without lock contention.


## 18.1 Repository Concept

### Dual-Purpose Modes

Modes %00001-%00011 behave differently based on pin configuration:

| Condition | Function |
|-----------|----------|
| NOT DAC_MODE | 32-bit long repository |
| DAC_MODE (P[12:10]=%101) | DAC with dithering |

### Repository Function

When not configured for DAC output, these modes create a shared data register:

- **WXPIN** writes a 32-bit long to the repository
- **RDPIN/RQPIN** reads the stored long
- **IN flag** indicates when new data has been written

This enables lock-free data sharing between cogs through dedicated pin hardware.

### Mode Variants

| Mode | Constant | Repository | DAC Function |
|------|----------|------------|--------------|
| %00001 | P_REPOSITORY | Yes | Noise output |
| %00010 | P_DAC_DITHER_RND | Yes | PRNG-dithered 16-bit |
| %00011 | P_DAC_DITHER_PWM | Yes | PWM-dithered 16-bit |


## 18.2 Long Repository (Non-DAC Mode)

### Purpose

The repository provides a hardware-arbitrated communication channel between cogs. Unlike hub RAM which may require locks for atomic access, the repository guarantees atomic 32-bit reads and writes.

### Operation

```{=latex}
\DiagRepository
```

### Configuration

```spin2
CON
  REPO_PIN = 48

PUB setup_repository()
  WRPIN(REPO_PIN, P_REPOSITORY)                 ' Mode %00001
  PINH(REPO_PIN)                                ' Enable

PUB write_value(value)
  WXPIN(REPO_PIN, value)                        ' Store 32-bit value

PUB read_value() : value
  value := RQPIN(REPO_PIN)                     ' Read without clearing IN
```

### PASM2 Repository Access

```pasm2
DAT           org

              ' Configure repository
              dirl      #REPO_PIN
              wrpin     ##P_REPOSITORY, #REPO_PIN
              dirh      #REPO_PIN

              ' Write value
              wxpin     ##$DEADBEEF, #REPO_PIN  ' Store value

              ' Read value
              rqpin     data, #REPO_PIN         ' Get stored value

data          res       1
```

### Multi-Cog Sharing

**Writer cog:**
```spin2
PUB sensor_cog() | reading
  setup_repository()

  REPEAT
    reading := read_sensor()
    WXPIN(REPO_PIN, reading)                    ' Share with other Cogs
    WAITMS(10)
```

**Reader cogs:**
```spin2
PUB display_cog()
  REPEAT
    IF PINREAD(REPO_PIN)                        ' New data available?
      display_value(RQPIN(REPO_PIN))
    WAITMS(100)

PUB logger_cog()
  REPEAT
    log_value(RQPIN(REPO_PIN))                  ' Read current value
    WAITMS(1000)
```


## 18.3 Mode %00001: DAC Noise

### Purpose

When configured for DAC output, mode %00001 generates pseudo-random noise on the 8-bit DAC. Each pin produces a unique random pattern.

`P_REPOSITORY` and `P_DAC_NOISE` name the same %00001 mode — the DAC_MODE bits (P[12:10]=%101) decide whether the pin acts as a long repository or a noise DAC.

### Configuration

```spin2
CON
  NOISE_PIN = 20

PUB setup_noise_dac()
  ' P[12:10] = %101 enables DAC output
  WRPIN(NOISE_PIN, P_DAC_NOISE | P_DAC_124R_3V | P_OE)
  WXPIN(NOISE_PIN, 0)                           ' No sample period
  PINH(NOISE_PIN)
```

### X Register: Sample Period

| X[15:0] | Behavior |
|---------|----------|
| 0 | 65,536 clocks (longest sample period) |
| N | IN raised every N clocks |

**Note:** The DAC outputs noise continuously regardless of sample period. The sample period only affects when IN is raised.

### Voltage Range

The noise spans the full scale of the selected DAC range. See Chapter 10 §10.2 for the resistor-DAC voltage options.

### Example: White Noise Generator

```spin2
CON
  _clkfreq = 200_000_000
  AUDIO_PIN = 20

PUB white_noise()
  ' Configure for 3.3V peak noise output
  WRPIN(AUDIO_PIN, P_DAC_NOISE | P_DAC_124R_3V | P_OE)
  WXPIN(AUDIO_PIN, 0)                           ' Max period (low power)
  PINH(AUDIO_PIN)

  ' Noise runs continuously - just wait
  REPEAT
    WAITMS(1000)
```


## 18.4 Mode %00010: DAC PRNG Dither

### Purpose

Provides 16-bit DAC resolution using pseudo-random dithering of the 8-bit DAC. The dithering randomly toggles between adjacent DAC levels to achieve higher effective resolution when averaged over time.

### Operation

- Y[15:0] sets the desired 16-bit output value
- Hardware randomly dithers between adjacent 8-bit levels
- Averaging over time yields 16-bit effective resolution

> **The "16-bit" figure is nominal — a temporal-averaging ceiling, not sample-by-sample accuracy** (the hardware DAC is 8-bit). See Chapter 10 §10.4 for the full dithering-resolution treatment.

### Configuration

```spin2
CON
  DAC_PIN = 20

PUB setup_dither_dac() | mode
  mode := P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE
  WRPIN(DAC_PIN, mode)
  WXPIN(DAC_PIN, 1)                             ' Update immediately
  PINH(DAC_PIN)

PUB set_voltage(value_16bit)
  WYPIN(DAC_PIN, value_16bit)                   ' 16-bit value
```

### X Register: Sample Period

| X[15:0] | Behavior |
|---------|----------|
| 1 | Update immediately (IN stays high) |
| N | Y captured every N clocks, IN raised |

For audio waveforms, set sample period to match sample rate:
```spin2
sample_period := _clkfreq / sample_rate
WXPIN(DAC_PIN, sample_period)
```

### Voltage Calculation

```formula
voltage = (Y[15:0] / 65536) × DAC_max_voltage
```

For P_DAC_124R_3V:
```formula
voltage = (Y[15:0] / 65536) × 3.3V
```

### Example: 16-bit Audio DAC

```spin2
CON
  _clkfreq = 200_000_000
  DAC_PIN = 20
  SAMPLE_RATE = 44100

PUB audio_dac() | sample_period
  sample_period := _clkfreq / SAMPLE_RATE       ' ~4535 clocks

  ' Configure 16-bit dithered DAC
  WRPIN(DAC_PIN, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE)
  WXPIN(DAC_PIN, sample_period)
  PINH(DAC_PIN)

  ' Output audio samples
  REPEAT
    REPEAT UNTIL PINREAD(DAC_PIN)               ' Wait for sample period
    WYPIN(DAC_PIN, get_next_sample())

PRI get_next_sample() : sample
  ' Application-specific: return next 16-bit audio sample
  sample := $8000
```

### ADC Readback

When OUT is high, the pin's ADC is enabled and RDPIN returns the 16-bit ADC accumulation (useful for measuring DAC loading). See Chapter 10 §10.6 for the ADC-feedback pattern.


## 18.5 Mode %00011: DAC PWM Dither

### Purpose

Provides 16-bit DAC resolution using PWM dithering. PWM dithering is more deterministic than PRNG dithering and provides better dynamic range, but introduces a fixed-frequency component.

### Operation

- Y[15:0] sets the desired 16-bit output value
- Hardware PWM-dithers between adjacent 8-bit levels
- Sample period must be multiple of 256 for proper operation

### Key Difference from PRNG Dither

| Aspect | PRNG Dither (%00010) | PWM Dither (%00011) |
|--------|---------------------|---------------------|
| Transition pattern | Random | Deterministic |
| Transitions per 256 clocks | Up to one per clock | At most two |
| Noise floor | Higher | Lower |
| Spurious tones | None | One at Fclock/256 |
| Dynamic range | Good | Better (-48dB spur) |

The "at most two transitions per 256 clocks" is what gives PWM dither its lower noise floor and lower switching activity: where the PRNG mode can flip the DAC on any clock, the PWM mode confines all of a period's switching to two edges.

### Configuration

```spin2
CON
  DAC_PIN = 20

PUB setup_pwm_dither_dac() | mode, period
  mode := P_DAC_DITHER_PWM | P_DAC_124R_3V | P_OE

  ' Period MUST be multiple of 256
  period := 256 * 16                            ' 4096 clocks

  WRPIN(DAC_PIN, mode)
  WXPIN(DAC_PIN, period)
  PINH(DAC_PIN)
```

### Sample Period Constraint

**X[15:0] must have X[7:0] = 0** (multiple of 256):

| Period | Valid? | Notes |
|--------|--------|-------|
| 256 | Yes | Minimum (fast update) |
| 512 | Yes | |
| 4096 | Yes | 256 × 16 |
| 1000 | No | X[7:0] ≠ 0 |

### Example: High-Quality Audio

```spin2
CON
  _clkfreq = 200_000_000
  DAC_PIN = 20
  SAMPLE_RATE = 48000

PUB hq_audio_dac() | period, samples_per_period
  ' Calculate period as multiple of 256
  ' At 48 kHz: period = 200_000_000 / 48000 = 4166.67
  ' Nearest 256 multiple: 4096 = 256 × 16
  period := 4096

  WRPIN(DAC_PIN, P_DAC_DITHER_PWM | P_DAC_124R_3V | P_OE)
  WXPIN(DAC_PIN, period)
  PINH(DAC_PIN)

  ' Actual sample rate: 200 MHz / 4096 = 48,828 Hz
  ' Close enough for most applications

  REPEAT
    REPEAT UNTIL PINREAD(DAC_PIN)
    WYPIN(DAC_PIN, get_next_sample())

PRI get_next_sample() : sample
  ' Application-specific: return next 16-bit audio sample
  sample := $8000
```


## 18.6 Comparison with Other Inter-Cog Mechanisms

### Hub RAM

| Aspect | Hub RAM | Repository |
|--------|---------|------------|
| Capacity | 512 KB | 32 bits per pin |
| Access | May need LOCK | Atomic |
| Speed | 8-15 clocks/access | 1 instruction |
| Flexibility | High | Limited |
| Best for | Large data | Flags, status |

### LOCK Bits

| Aspect | LOCK Bits | Repository |
|--------|-----------|------------|
| Capacity | 16 locks total | 32 bits per pin |
| Function | Mutex only | Data + flag |
| Complexity | TRY/REL pattern | Read/Write |
| Best for | Critical sections | Data sharing |

### Repository Advantages

1. **No contention**: Hardware arbitration, no lock waits
2. **Atomic updates**: Guaranteed 32-bit coherence
3. **Flag included**: IN indicates new data
4. **Non-blocking reads**: RQPIN doesn't clear IN

### When to Use Repository

- Sharing single sensor reading across multiple cogs
- Status flags and state indicators
- Real-time data where latest value is sufficient
- Simple producer-consumer patterns


## 18.7 Application Examples

### Example 1: Shared Sensor Reading

```{.spin2 caption="ch18-repository-multicog.spin2"}
CON
  _clkfreq = 200_000_000
  REPO_PIN = 48
  TEMP_SENSOR = 20

VAR
  long sensor_stack[64]

PUB main()
  ' Start sensor reading Cog
  COGSPIN(NEWCOG, sensor_cog(), @sensor_stack)

  ' This Cog reads the shared value
  setup_repository_reader()

  REPEAT
    display_temperature(RQPIN(REPO_PIN))
    WAITMS(500)

PRI setup_repository_reader()
  ' Just need to read - writer sets up the pin
  ' Repository is already configured by sensor_cog

PRI sensor_cog() | temp
  ' Configure repository
  WRPIN(REPO_PIN, P_REPOSITORY)
  PINH(REPO_PIN)

  REPEAT
    temp := read_temperature_sensor()
    WXPIN(REPO_PIN, temp)                       ' Share reading
    WAITMS(100)

PRI display_temperature(t)
  ' Application-specific: render temperature value t

PRI read_temperature_sensor() : t
  ' Application-specific: return current temperature reading
  t := 25
```

### Example 2: Multi-Cog Status Flags

```spin2
CON
  STATUS_PIN = 48
  FLAG_RUNNING = $0001
  FLAG_ERROR = $0002
  FLAG_COMPLETE = $0004

PUB set_flag(flag)
  WXPIN(STATUS_PIN, RQPIN(STATUS_PIN) | flag)

PUB clear_flag(flag)
  WXPIN(STATUS_PIN, RQPIN(STATUS_PIN) & !flag)

PUB test_flag(flag) : set
  set := (RQPIN(STATUS_PIN) & flag) <> 0
```

> **Caution — set/clear-flag is a read-modify-write, not an atomic update.** `WXPIN(STATUS_PIN, RQPIN(STATUS_PIN) | flag)` reads, modifies, then writes back. The 32-bit *store* is atomic (§18.6), but the read-modify-write spanning those three steps is not: if two cogs each set a different flag at the same time, one update can be lost. This pattern is safe only when a **single cog owns all writes** to the repository. For multiple writers, guard the update with a lock or give each writer its own repository pin.

### Example 3: Stereo Audio with Dithered DAC

```spin2
CON
  _clkfreq = 200_000_000
  LEFT_PIN = 20
  RIGHT_PIN = 21
  SAMPLE_RATE = 44100

PUB stereo_audio() | period
  period := _clkfreq / SAMPLE_RATE

  ' Configure both channels for PRNG dithering
  WRPIN(LEFT_PIN, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE)
  WRPIN(RIGHT_PIN, P_DAC_DITHER_RND | P_DAC_124R_3V | P_OE)
  WXPIN(LEFT_PIN, period)
  WXPIN(RIGHT_PIN, period)
  PINH(LEFT_PIN)
  PINH(RIGHT_PIN)

  REPEAT
    REPEAT UNTIL PINREAD(LEFT_PIN)              ' Wait for sample time
    WYPIN(LEFT_PIN, get_left_sample())
    WYPIN(RIGHT_PIN, get_right_sample())

PRI get_left_sample() : sample
  ' Application-specific: return next 16-bit left-channel sample
  sample := $8000

PRI get_right_sample() : sample
  ' Application-specific: return next 16-bit right-channel sample
  sample := $8000
```

### Example 4: Function Generator with PWM DAC

```spin2
CON
  _clkfreq = 200_000_000
  DAC_PIN = 20

VAR
  word sine_table[256]

PUB function_generator(frequency) | period, phase, increment
  ' Build sine table (0-65535 range)
  build_sine_table()

  ' Calculate DDS parameters
  ' phase accumulator increments per sample
  period := 4096                                ' PWM dither requirement
  increment := (frequency * 256 * 65536) / (_clkfreq / period)

  WRPIN(DAC_PIN, P_DAC_DITHER_PWM | P_DAC_124R_3V | P_OE)
  WXPIN(DAC_PIN, period)
  PINH(DAC_PIN)

  phase := 0
  REPEAT
    REPEAT UNTIL PINREAD(DAC_PIN)
    WYPIN(DAC_PIN, sine_table[phase >> 8])      ' Output current phase
    phase += increment                          ' Advance phase

PRI build_sine_table() | i
  ' Fill sine_table[0..255] with sine values 0..65535
  REPEAT i FROM 0 TO 255
    sine_table[i] := $8000 + QSIN(32767, i << 24, 0)
```


## 18.8 Quick Reference

### Mode Constants

| Constant | Mode | Function (Non-DAC) | Function (DAC) |
|----------|------|-------------------|----------------|
| P_REPOSITORY | %00001 | 32-bit repository | Noise output |
| P_DAC_DITHER_RND | %00010 | 32-bit repository | PRNG-dithered 16-bit |
| P_DAC_DITHER_PWM | %00011 | 32-bit repository | PWM-dithered 16-bit |

### DAC Mode Enable

Add to WRPIN value: `P_DAC_xxxR_yV | P_OE`

- P[12:10] = %101 for DAC output
- `P_OE` sets the output-enable flag (drives the pin)

### Register Usage

**Repository Mode:**

| Register | Write | Read |
|----------|-------|------|
| X via WXPIN | Store value | - |
| Y | Not used | - |
| Z via RQPIN (or RDPIN to acknowledge) | - | Retrieve value |

**DAC Dither Modes:**

| Register | Function |
|----------|----------|
| X[15:0] | Sample period (PWM must be ×256) |
| Y[15:0] | 16-bit DAC value |
| Z | ADC readback (if OUT=1) |

### Key Points

- **Repository**: WXPIN writes, RQPIN reads without clearing IN
- **DAC Noise**: Random 8-bit values every clock
- **PRNG Dither**: Random toggle between adjacent levels
- **PWM Dither**: Deterministic dither, period must be ×256
- **All modes**: IN raised when sample period completes


*This chapter covered repository and dithered DAC modes. For USB host/device, see Chapter 19. For a complete mode reference, see Appendix F.*
