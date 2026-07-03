# Appendix E: Troubleshooting

This appendix provides problem/solution guidance for common smart pin issues organized by symptom.

## Pin Not Responding

### Symptom
Pin appears completely inactive. No output changes, no IN flag, no measurements.

### Likely Causes

1. **DIR not set** - Smart pin not enabled
2. **WRPIN not executed** - Mode not configured
3. **Wrong pin number** - Configuration applied to different pin
4. **Pin used by another cog** - Conflicting configurations

### Diagnostic Steps

1. Read pin state:
```spin2
DEBUG("DIR: ", UDEC_(PINREAD(pin) >> 31))
DEBUG("OUT: ", UDEC_((INA >> pin) & 1))
```

2. Verify mode was written:
```spin2
' Reset and reconfigure
PINL(pin)
WRPIN(pin, your_mode)
PINH(pin)
DEBUG("Mode applied")
```

### Solutions

**Enable the pin:**
```spin2
' After WRPIN, MUST set DIR
WRPIN(pin, P_NCO_FREQ | P_OE)
PINH(pin)                                ' THIS IS REQUIRED
```

**For output modes, also set output:**
```spin2
PINLOW(pin)                              ' Sets DIR=1, starts smart pin
' or
PINH(pin)                                ' Alternative
```

**Check for typos in pin number:**
```spin2
CON
  MY_PIN = 20                            ' Define constant

PUB setup(mode)
  ' Use constant, not magic numbers
  WRPIN(MY_PIN, mode)                    ' Correct
  PINH(MY_PIN)
```

## No Output Visible

### Symptom
Smart pin configured for output, but oscilloscope shows no signal or wrong level.

### Likely Causes

1. **P_OE not set** - Output enable missing
2. **Wrong drive strength** - Signal too weak
3. **Output routing mismatch** - Signal going elsewhere
4. **Hardware issue** - Shorted pin, wrong connection

### Diagnostic Steps

1. Check mode includes P_OE:
```spin2
mode := P_NCO_FREQ | P_OE                ' P_OE is REQUIRED for output
```

2. Test with maximum drive:
```spin2
mode := P_NCO_FREQ | P_OE | P_HIGH_FAST | P_LOW_FAST
```

3. Verify basic output works:
```spin2
' Test pin with simple on/off
PINHIGH(pin)
WAITMS(1000)
PINLOW(pin)
WAITMS(1000)
```

### Solutions

**Add P_OE to mode:**
```spin2
' WRONG - no output
WRPIN(pin, P_PWM_SAWTOOTH)

' CORRECT - output enabled
WRPIN(pin, P_PWM_SAWTOOTH | P_OE)
```

**Check inverted output:**
```spin2
' If signal appears inverted
mode := P_NCO_FREQ | P_OE | P_INVERT_OUTPUT
```

**For weak signals, increase drive:**
```spin2
' Default is P_HIGH_FAST | P_LOW_FAST
' For high-impedance loads, this should work
' For capacitive loads, ensure adequate drive
```

## Wrong Frequency or Timing

### Symptom
Output frequency or timing does not match expected value.

### Likely Causes

1. **sysclk assumption wrong** - Using wrong clock frequency
2. **Formula error** - Incorrect calculation
3. **Integer overflow** - Calculation exceeds 32 bits
4. **X register not set** - Default value being used

### Diagnostic Steps

1. Verify sysclk:
```spin2
DEBUG("sysclk: ", UDEC_(_clkfreq))
```

2. Check calculated values:
```spin2
y_val := frequency FRAC _clkfreq
DEBUG("Y value: ", UHEX_(y_val))
```

3. Verify X register was written:
```spin2
WXPIN(pin, x_value)
DEBUG("X written: ", UHEX_(x_value))
```

### Solutions

**Use correct sysclk:**
```spin2
CON
  _clkfreq = 200_000_000               ' Verify this matches actual clock

PUB calc_frequency(hz) : y_val
  y_val := hz FRAC _clkfreq
```

**Use the FRAC operator for NCO Y calculation:**
```spin2
  ' CORRECT - FRAC = (frequency * 2^32) / _clkfreq (32-bit)
' without manual 33-bit constant arithmetic.
y_val := frequency FRAC _clkfreq
```

Use `FRAC`, not a hand-rolled `frequency * $1_0000_0000 / _clkfreq` (the
`$1_0000_0000` literal exceeds the 32-bit constant range). See Chapter 8 for
how `FRAC` derives the NCO Y value.

**For NCO, remember X[15:0] affects frequency:**
```formula
' With X[15:0] = 1 (default)
frequency = Y * sysclk / 2^32

' With X[15:0] = 10
frequency = Y * sysclk / (10 * 2^32)
```

## Noisy or Unstable Signal

### Symptom
Input measurements fluctuate, outputs have jitter, counts are erratic.

### Likely Causes

1. **No input conditioning** - Raw input picking up noise
2. **Poor grounding** - Ground loops or high impedance
3. **Inadequate filtering** - High-frequency noise passing through
4. **Edge detection on slow signals** - Multiple triggers per transition

### Diagnostic Steps

1. Check input waveform on oscilloscope
2. Verify ground connections
3. Test with Schmitt trigger enabled

### Solutions

**Add Schmitt trigger:**
```spin2
' WRONG - raw input
mode := P_COUNT_RISES

' CORRECT - Schmitt trigger for clean edges
mode := P_COUNT_RISES | P_SCHMITT_A
```

**Add input filtering:**
```spin2
' For noisy signals, add filter
mode := P_HIGH_TICKS | P_SCHMITT_A | P_FILT1_AB
```

**Use higher sample count for averaging:**
```spin2
' Measure over more periods to average noise
WXPIN(pin, 1000)                         ' 1000 periods instead of 10
```

**For ADC, increase sample period:**
```spin2
' More samples = more filtering
WXPIN(adc_pin, %00_1001)                 ' 512 clocks instead of 128
```

## Serial Not Working

### Symptom
UART or SPI communication fails. No data received or garbled data.

### Likely Causes

1. **Baud rate mismatch** - TX and RX at different speeds
2. **Wrong polarity** - Signal inverted (RS-232 vs TTL)
3. **Bit count mismatch** - Wrong number of data bits
4. **Missing clock routing** - For sync modes

### Diagnostic Steps

1. Verify baud calculation:
```spin2
bit_period := _clkfreq / BAUD
DEBUG("Bit period: ", UDEC_(bit_period))
```

2. Check with loopback:
```spin2
' Connect TX to RX and verify echo
```

3. Use oscilloscope to measure actual baud rate

### Solutions

**Match TX and RX configuration:**
```spin2
' TRANSMIT
tx_x := (_clkfreq / BAUD) << 16 | 7      ' 8 data bits
WRPIN(TX_PIN, P_ASYNC_TX | P_OE)
WXPIN(TX_PIN, tx_x)

' RECEIVE - must match exactly
rx_x := (_clkfreq / BAUD) << 16 | 7      ' Same baud and bits
WRPIN(RX_PIN, P_ASYNC_RX)
WXPIN(RX_PIN, rx_x)
```

**For RS-232, add inversion:**
```spin2
' RS-232 uses inverted logic
WRPIN(TX_PIN, P_ASYNC_TX | P_OE | P_INVERT_OUTPUT)
WRPIN(RX_PIN, P_ASYNC_RX | P_INVERT_IN)
```

**For P_SYNC_TX/RX, add clock routing:**
```spin2
' WRONG - no clock source specified
mode := P_SYNC_TX | P_OE

' CORRECT - clock from adjacent pin
mode := P_SYNC_TX | P_OE | P_PLUS1_B     ' Clock from pin+1
```

## ADC Readings Wrong

### Symptom
ADC returns unexpected values, zero, or maximum.

### Likely Causes

1. **Wrong gain setting** - Signal outside input range
2. **Missing reference** - Floating input
3. **Wrong filter mode** - Post-processing not applied
4. **Sample period too short** - Not enough resolution

### Diagnostic Steps

1. Read raw ADC value:
```spin2
raw := RDPIN(adc_pin)
DEBUG("Raw ADC: ", UHEX_(raw))
```

2. Verify input is within range

3. Check for saturation (stuck at 0 or max)

### Solutions

**Match gain to signal level:**
```spin2
' For 0-3.3V signal
mode := P_ADC_1X | P_ADC

' For 0-100mV signal
mode := P_ADC_30X | P_ADC
```

**Use ground reference for single-ended:**
```spin2
mode := P_ADC_GIO | P_ADC                ' Ground-referenced input
```

**For SINC2 filtering, compute difference:**
```spin2
' SINC2 filter mode requires difference
REPEAT UNTIL PINREAD(adc_pin)
acc := RDPIN(adc_pin)
sample := acc - last_acc                 ' THIS IS REQUIRED
last_acc := acc
```

**Increase sample period for more bits:**
```spin2
' 8-bit resolution
WXPIN(adc_pin, %00_0111)                 ' 128 clocks

' 12-bit resolution
WXPIN(adc_pin, %00_1011)                 ' 2048 clocks
```

## Encoder Counts Incorrect

### Symptom
Quadrature encoder reports wrong position or skips counts.

### Likely Causes

1. **A/B wiring swapped** - Direction reversed
2. **Noise causing false edges** - Missing conditioning
3. **B-input not routed** - Using wrong pin
4. **Speed too fast** - Missing transitions

### Diagnostic Steps

1. Verify count direction:
```spin2
' Rotate slowly, check count increases/decreases correctly
pos := RDPIN(enc_pin)
DEBUG("Position: ", SDEC_(pos))
```

2. Check for noise by holding still:
```spin2
' Stationary encoder should give stable count
```

### Solutions

**Route B-input correctly:**
```spin2
' Encoder A on pin 20, B on pin 21
mode := P_QUADRATURE | P_PLUS1_B         ' B from pin+1
WRPIN(20, mode)
```

**Add Schmitt trigger for noisy signals:**
```spin2
mode := P_QUADRATURE | P_PLUS1_B | P_SCHMITT_A
```

**If direction reversed, swap wiring or invert:**
```spin2
mode := P_QUADRATURE | P_PLUS1_B | P_INVERT_A
```

**For high-speed encoders, verify no missed edges:**
```spin2
' Maximum encoder speed depends on edge separation
' At 200 MHz, minimum detectable pulse is ~5ns
' For 1000 line encoder at 10,000 RPM:
' edges/sec = 1000 * 4 * 10000/60 = 666,667
' Period = 1.5 µs - well within capability
```

## Mode Stops Working

### Symptom
Smart pin works initially then stops. No more IN flags or output changes.

### Likely Causes

1. **IN flag not acknowledged** - Accumulator overflow
2. **Measurement complete, not restarted** - One-shot mode
3. **Counter overflow** - 32-bit limit reached

### Diagnostic Steps

1. Check if IN flag is being cleared:
```spin2
' RDPIN clears IN, RQPIN does not
value := RDPIN(pin)                      ' Clears IN
' vs
value := RQPIN(pin)                      ' Does NOT clear IN
```

2. Verify mode auto-restarts

### Solutions

**Read with RDPIN to acknowledge:**
```spin2
REPEAT
  REPEAT UNTIL PINREAD(pin)              ' Wait for IN
  value := RDPIN(pin)                    ' READ AND CLEAR - restarts
```

**For continuous measurement, verify X value:**
```spin2
' X=0 means continuous, no IN flag
WXPIN(pin, 0)                            ' Continuous - read anytime

' X>0 means periodic, IN raised each period
WXPIN(pin, period)                      ' Periodic - must read to restart
```

**Pulse DIR to reset if stuck:**
```spin2
PINL(pin)                                ' Disable
PINH(pin)                                ' Re-enable from fresh state
```

## Interference Between Pins

### Symptom
Configuring one pin affects behavior of another.

### Likely Causes

1. **Input routing overlap** - Same signal feeding multiple pins
2. **Shared resources** - Adjacent pin interactions
3. **Ground bounce** - High-current switching affecting nearby signals

### Diagnostic Steps

1. Test pins in isolation
2. Check for input routing to adjacent pins
3. Monitor with oscilloscope for crosstalk

### Solutions

**Verify no accidental routing:**
```spin2
' Check A or B is not routed from affected pin
' P_PLUS1_A, P_MINUS1_A, etc. share inputs

' If pin 20 has issues when pin 21 is used:
' Check if pin 21 mode includes P_MINUS1_A
```

**Isolate pin configurations:**
```spin2
' Configure pins one at a time, test each
WRPIN(pin1, mode1)
PINH(pin1)
' Test pin1 works

WRPIN(pin2, mode2)
PINH(pin2)
' Test pin2 works AND pin1 still works
```

**For high-current outputs, add slew limiting:**
```spin2
' Reduce switching speed to minimize ground bounce
' Use slower drive if timing permits
```

## Debugging Techniques

### Using RDPIN to Inspect State

```spin2
' Read Z register contents
z_value := RDPIN(pin)
DEBUG("Z: ", UHEX_(z_value))

' Read without clearing IN
z_value := RQPIN(pin)
DEBUG("Z (no clear): ", UHEX_(z_value))

' Check IN flag
in_flag := PINREAD(pin)
DEBUG("IN: ", UDEC_(in_flag))
```

### Incremental Configuration Testing

```spin2
' Step 1: Verify pin can output
PINHIGH(pin)
WAITMS(100)
PINLOW(pin)
' Confirm on scope

' Step 2: Add smart pin mode
PINL(pin)
WRPIN(pin, P_NCO_FREQ | P_OE)
WXPIN(pin, 1)
WYPIN(pin, 21475)                        ' 1 kHz
PINH(pin)
' Check for 1 kHz

' Step 3: Add full configuration
' ...continue adding complexity
```

### Logic Analyzer Protocol Decoding

For serial protocols:

1. Capture raw waveform
2. Verify timing matches expected baud/clock
3. Decode data and compare to expected
4. Check for framing errors

### Oscilloscope Measurements

**For PWM:**

- Measure frequency
- Measure duty cycle
- Check for glitches at transitions

**For ADC:**

- Measure input voltage
- Verify within expected range
- Check for noise on input

**For Serial:**

- Measure bit period
- Verify logic levels
- Check start/stop bits (async)

### Common Debug Patterns

**Blink test:**
```spin2
' Simplest test - does the pin toggle?
REPEAT
  PINTOGGLE(pin)
  WAITMS(500)
```

**Counter verification:**
```spin2
' Verify counter is incrementing
REPEAT 10
  DEBUG("Count: ", UDEC_(RDPIN(pin)))
  WAITMS(100)
```

**Mode echo test:**
```spin2
' Loopback test for serial
WRPIN(TX_PIN, P_ASYNC_TX | P_OE)
WRPIN(RX_PIN, P_ASYNC_RX)
' Wire TX_PIN to RX_PIN
WYPIN(TX_PIN, $55)
WAITMS(1)
received := RDPIN(RX_PIN)
DEBUG("Sent: $55, Received: ", UHEX_(received))
```

## Quick Diagnostic Checklist

### Output Not Working

- [ ] WRPIN executed with correct mode?
- [ ] Mode includes P_OE?
- [ ] DIRH or PINLOW called?
- [ ] X and Y registers set correctly?
- [ ] Pin number correct?

### Input Not Working

- [ ] WRPIN executed?
- [ ] DIRH called?
- [ ] Waiting for IN flag when required?
- [ ] Using RDPIN (not RQPIN) to restart?
- [ ] Input conditioning appropriate?

### Serial Not Working

- [ ] Baud rate calculation correct?
- [ ] TX and RX configured identically?
- [ ] Polarity matches (P_INVERT_*)?
- [ ] Bit count matches?
- [ ] For sync, clock routing added?

### ADC Not Working

- [ ] Input mode (P_ADC_GIO, etc.) appropriate?
- [ ] Gain matches input level?
- [ ] Filter mode understood?
- [ ] Sample period set?
- [ ] For SINC2/3, difference computed?


*For mode details, see relevant chapter. For P_ constants, see Appendix B. For formulas, see Appendix C.*
