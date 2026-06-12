# Appendix D: Mode Comparison Charts

This appendix provides comparison matrices to help select the appropriate Smart Pin mode for your application.

## Output Mode Comparison

### All Output Modes at a Glance

| Mode | Constant | Freq Range | Resolution | Duty Control | Continuous | Complexity | Primary Use |
|------|----------|------------|------------|--------------|------------|------------|-------------|
| Digital | - | DC only | 1-bit | N/A | Yes | Low | On/off control |
| Pulse | P_PULSE | DC to MHz | 16-bit timing | Fixed per pulse | One-shot | Low | Single pulses, triggers |
| Transition | P_TRANSITION | DC to 100 MHz | 16-bit period | 50% fixed | Counted | Low | Clock generation |
| NCO Freq | P_NCO_FREQ | 0.05 Hz to 100 MHz | 32-bit | 50% fixed | Yes | Low | Frequency synthesis |
| NCO Duty | P_NCO_DUTY | 0.05 Hz to 100 MHz | 32-bit | Variable | Yes | Medium | Variable duty waves |
| PWM Triangle | P_PWM_TRIANGLE | 1 Hz to 390 kHz | 16-bit | Full range | Yes | Low | Motor, LED dimming |
| PWM Sawtooth | P_PWM_SAWTOOTH | 1 Hz to 780 kHz | 16-bit | Full range | Yes | Low | Motor, audio |
| PWM SMPS | P_PWM_SMPS | Variable | 16-bit | Feedback | Autonomous | High | Power supply |
| DAC 8-bit | P_DAC_xxx | DC | 8-bit | N/A | Yes | Low | Voltage reference |
| DAC 16-bit | P_DAC_DITHER_* | DC to audio | 16-bit | N/A | Yes | Medium | Audio, precision |
| Sync TX | P_SYNC_TX | Clock rate | 1-32 bits | N/A | Clocked | Medium | SPI master |
| Async TX | P_ASYNC_TX | 300 to 1M+ baud | 1-32 bits | N/A | Per-byte | Low | UART |

## Input Mode Comparison

### All Input Modes at a Glance

| Mode | Constant | Measurement | Resolution | Speed | Autonomous | Complexity | Primary Use |
|------|----------|-------------|------------|-------|------------|------------|-------------|
| Digital | - | Logic state | 1-bit | Instant | No | Low | Button, sensor |
| State Ticks | P_STATE_TICKS | High/low time | 1 clock | Every edge | Yes | Low | PWM analysis |
| High Ticks | P_HIGH_TICKS | Pulse width | 1 clock | Per pulse | Yes | Low | Servo, pulse |
| Events Ticks | P_EVENTS_TICKS | N events / timeout | 1 clock | Configurable | Yes | Medium | Frequency, watchdog |
| Quadrature | P_QUADRATURE | Position/velocity | 4x encoder | Every edge | Yes | Low | Encoder |
| Count Highs | P_COUNT_HIGHS | Gated edges | 32-bit | Configurable | Yes | Low | Freq counter |
| Count Up/Down | P_REG_UP_DOWN | Up/down by B direction | 32-bit | Configurable | Yes | Low | Step/direction |
| Count Edges | P_COUNT_RISES | Edge/rise count | 32-bit | Configurable | Yes | Low | Event counter |
| High Clocks | P_HIGH_TICKS | High time sum | 32-bit | Configurable | Yes | Low | Duty cycle |
| Periods Ticks | P_PERIODS_TICKS | N period time | 1 clock | N periods | Yes | Medium | Precision freq |
| Periods Highs | P_PERIODS_HIGHS | N period high | 1 clock | N periods | Yes | Medium | Duty cycle |
| Counter Ticks | P_COUNTER_TICKS | Time in window | 1 clock | Time window | Yes | Medium | Freq measurement |
| Counter Periods | P_COUNTER_PERIODS | Periods in window | 1 period | Time window | Yes | Low | Freq counter |
| ADC | P_ADC | Voltage | 8-14 bits | kHz to MHz | Yes | Medium | Analog sensor |
| ADC Scope | P_ADC_SCOPE | 4-ch capture | 8 bits | Triggered | Triggered | High | Oscilloscope |
| Sync RX | P_SYNC_RX | Serial data | 1-32 bits | Clock rate | Yes | Medium | SPI slave |
| Async RX | P_ASYNC_RX | Serial data | 1-32 bits | Baud rate | Yes | Low | UART |

## Frequency Generation Comparison

### When to Use Each Mode

| Application | Best Mode | Why |
|-------------|-----------|-----|
| Fixed frequency clock | P_TRANSITION or P_NCO_FREQ | Clean 50% duty, precise frequency |
| Variable frequency | P_NCO_FREQ | 32-bit resolution, instant updates |
| Audio tone | P_NCO_FREQ | Sub-Hz resolution for musical notes |
| Motor PWM | P_PWM_SAWTOOTH | Fast switching, full duty range |
| LED dimming | P_PWM_TRIANGLE | Smooth transitions, no flicker |
| Servo control | P_PULSE | Precise 1-2ms pulses at 50 Hz |
| Analog waveform | P_DAC_DITHER_PWM | True analog output, 16-bit |
| SMPS control | P_PWM_SMPS | Built-in voltage/current feedback |

### Frequency Range by Mode

| Mode | Minimum | Maximum | Resolution |
|------|---------|---------|------------|
| P_NCO_FREQ | 0.05 Hz | 100 MHz | 0.05 Hz (32-bit) |
| P_TRANSITION | DC | 100 MHz | 1 clock |
| P_PWM_TRIANGLE | ~1 Hz | 390 kHz | 1/frame |
| P_PWM_SAWTOOTH | ~1 Hz | 780 kHz | 1/frame |
| P_PULSE | Single | MHz | 1 clock |

### Duty Cycle Capability

| Mode | Duty Range | Control Method |
|------|------------|----------------|
| P_NCO_FREQ | 50% fixed | None |
| P_NCO_DUTY | 0-100% | Y value |
| P_PWM_TRIANGLE | 0-100% | Y / frame |
| P_PWM_SAWTOOTH | 0-100% | Y / frame |
| P_TRANSITION | 50% fixed | None |
| P_PULSE | Pulse width | Explicit clocks |

## Counting Mode Comparison

### Choosing the Right Counter

| Scenario | Best Mode | Configuration |
|----------|-----------|---------------|
| Simple event count | P_COUNT_RISES | X=0, Y=0 |
| Gated frequency counter | P_COUNT_HIGHS | X=gate_period |
| Step/direction motor | P_COUNT_RISES | X=0 |
| Up/down buttons | P_COUNT_RISES | X=0, Y=1 |
| Rotary encoder | P_QUADRATURE | X=0 (position) |
| Encoder velocity | P_QUADRATURE | X=period |
| PWM duty integration | P_HIGH_TICKS | X=period |
| Differential timing | P_HIGH_TICKS | X=period, Y=1 |

### Counter Features Matrix

| Mode | A-Input | B-Input | Direction | Gating | Signed |
|------|---------|---------|-----------|--------|--------|
| P_COUNT_RISES | Count | Down (Y=1) | Y[0] | No | Yes |
| P_COUNT_HIGHS | Count | Gate | No | Yes | No |
| P_COUNT_RISES | Count | Direction | B level | No | Yes |
| P_HIGH_TICKS | Time | Time (Y=1) | Y[0] | Level | Yes |
| P_QUADRATURE | Phase A | Phase B | Automatic | No | Yes |

## Period/Frequency Measurement Comparison

### Mode Selection Guide

| Need | Best Mode | Why |
|------|-----------|-----|
| Simple frequency count | P_COUNTER_PERIODS | Direct Hz reading with 1s gate |
| Precise period | P_PERIODS_TICKS | Clock-accurate over N periods |
| Unknown frequency | P_COUNTER_PERIODS | Time-windowed, consistent rate |
| Duty cycle | P_PERIODS_HIGHS + P_PERIODS_TICKS | Both measurements needed |
| RPM measurement | P_COUNTER_PERIODS | 100ms-1s gate time |
| Oscillator calibration | P_PERIODS_TICKS | Many periods for ppm accuracy |

### Measurement Resolution

| Mode | What's Measured | Resolution | Precision Improves With |
|------|-----------------|------------|------------------------|
| P_PERIODS_TICKS | Time for X periods | ±1 clock | More periods |
| P_PERIODS_HIGHS | High time for X periods | ±1 clock | More periods |
| P_COUNTER_TICKS | Period time in window | ±1 clock | Longer window |
| P_COUNTER_HIGHS | High time in window | ±1 clock | Longer window |
| P_COUNTER_PERIODS | Periods in window | ±1 period | Longer window |

## Serial Mode Comparison

### Transmit Modes

| Aspect | P_ASYNC_TX (UART) | P_SYNC_TX (SPI) |
|--------|-------------------|-----------------|
| Clock | Implicit (baud) | Explicit (B-input) |
| Framing | Start/stop bits | None |
| Pins | 1 (TX) | 2 (Data + Clock) |
| Bits per frame | 1-32 + start/stop | 1-32 |
| Update rate | Baud / (bits + 2) | Clock / bits |
| Double buffered | Yes | Yes |
| Best for | Point-to-point | Bus, shift registers |

### Receive Modes

| Aspect | P_ASYNC_RX (UART) | P_SYNC_RX (SPI) |
|--------|-------------------|-----------------|
| Clock | Implicit (baud) | External (B-input) |
| Framing | Auto-detects start | None |
| Pins | 1 (RX) | 1 (Data), clock from adjacent |
| Bits per frame | 1-32 | 1-32 |
| Clock routing | N/A | P_PLUS1_B etc. required |
| Data justification | Left (MSB at Z[31]) | Left (MSB at Z[31]) |
| Best for | RS-232, debug | SPI slave, shift in |

### Serial Speed Comparison

| Protocol | Max Speed | Typical Use |
|----------|-----------|-------------|
| UART 115200 | 115 kbps | Debug, GPS |
| UART 1 Mbps | 1 Mbps | Fast serial |
| SPI 1 MHz | 1 Mbps | Sensors |
| SPI 10 MHz | 10 Mbps | Flash, display |
| SPI 25 MHz | 25 Mbps | High-speed ADC |

## ADC Mode Comparison

### ADC Modes

| Mode | Clock | Triggering | Channels | Best For |
|------|-------|------------|----------|----------|
| P_ADC | Internal | Continuous | 1 | General sensors |
| P_ADC_EXT | External | B-input edge | 1 | External ADC chips |
| P_ADC_SCOPE | Internal | Hysteretic | 4 | Signal capture |

### Filter Modes (X[5:4])

| X[5:4] | Mode | Post-Processing | Resolution | Speed |
|--------|------|-----------------|------------|-------|
| %00 | SINC2 Sampling | None | 8-14 bits | Fast |
| %01 | SINC2 Filtering | Software diff | 8-14 ENOB | Medium |
| %10 | SINC3 Filtering | Software 3x diff | 10-18 ENOB | Slow |
| %11 | Bitstream | Custom | 1 bit/clock | Fastest |

### Gain Selection Guide

| Signal Level | Best Gain | Input Range | Use Case |
|--------------|-----------|-------------|----------|
| 0-3.3V | P_ADC_1X | Full | Pot, sensor |
| 0-1V | P_ADC_3X | 0-1.04V | Low-voltage sensor |
| 0-300mV | P_ADC_10X | 0-330mV | Thermocouple |
| 0-100mV | P_ADC_30X | 0-104mV | Strain gauge |
| 0-30mV | P_ADC_100X | 0-33mV | Microphone |

## DAC Mode Comparison

### Resistor Options

| Mode | Resistance | Voltage | Current | Best For |
|------|------------|---------|---------|----------|
| P_DAC_990R_3V | 990 ohm | 0-3.3V | ~3 mA | Op-amp input |
| P_DAC_600R_2V | 600 ohm | 0-2.0V | ~3 mA | Medium load |
| P_DAC_124R_3V | 124 ohm | 0-3.3V | ~27 mA | LED, speaker |
| P_DAC_75R_2V | 75 ohm | 0-2.0V | ~27 mA | Coax cable |

### Dithering Comparison

| Aspect | P_DAC_DITHER_RND | P_DAC_DITHER_PWM |
|--------|------------------|------------------|
| Pattern | Random | Deterministic |
| Transitions | Many | Max 2 per 256 clk |
| Spectrum | White noise floor | Fclock/256 at -48dB |
| Dynamic range | Good | Better |
| Sample period | Any >= 1 | Multiple of 256 |
| Best for | Control signals | Audio |

## Quick Selection Trees

### "I need to generate a signal"

```{=latex}
\DiagSelectOutput
```

### "I need to measure a signal"

```{=latex}
\DiagSelectInput
```


*For P_ constant values, see Appendix B. For formulas, see Appendix C. For troubleshooting, see Appendix E.*
