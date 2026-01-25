# Appendix A: Intent Index

This appendix provides task-oriented navigation. Find what you want to accomplish, then follow the reference to the appropriate chapter and mode.

---

## Generate Signals

### I want to generate a clock signal
**Chapter 7: Transition and Pulse Output**
- Specifically: P_TRANSITION (%00101) for continuous clock
- Also consider: P_NCO_FREQ for frequency synthesis

### I want to generate a fixed frequency
**Chapter 8: NCO Frequency**
- Specifically: P_NCO_FREQ (%00110)
- Also consider: P_TRANSITION for square waves

### I want to generate PWM for motor control
**Chapter 9: PWM Output**
- Specifically: P_PWM_SAWTOOTH (%01001) for standard PWM
- Also consider: P_PWM_SMPS for switch-mode power

### I want to generate PWM for LED dimming
**Chapter 9: PWM Output**
- Specifically: P_PWM_TRIANGLE (%01000) for smooth dimming
- Also consider: P_NCO_DUTY for duty cycle control

### I want to generate audio tones
**Chapter 8: NCO Frequency**
- Specifically: P_NCO_FREQ (%00110) for tone generation
- Also consider: DAC modes for higher quality audio

### I want to generate arbitrary waveforms
**Chapter 10: DAC Output**
- Specifically: P_DAC_DITHER_RND or P_DAC_DITHER_PWM for 16-bit resolution
- Also consider: Using NCO with lookup tables

### I want to output analog voltage
**Chapter 10: DAC Output**
- Specifically: P_DAC_990R_3V for basic 8-bit DAC
- Specifically: P_DAC_DITHER_RND for 16-bit resolution
- Also consider: Resistor values for impedance matching

### I want to transmit serial data (UART)
**Chapter 11: Serial Transmit**
- Specifically: P_ASYNC_TX (%11110) for UART
- Also consider: P_INVERT_OUT for RS-232 polarity

### I want to transmit serial data (SPI)
**Chapter 11: Serial Transmit**
- Specifically: P_SYNC_TX (%11100) for SPI master
- Also consider: Clock polarity and phase settings

### I want to generate pulses with precise timing
**Chapter 7: Transition and Pulse Output**
- Specifically: P_PULSE (%00100) for single or counted pulses
- Also consider: NCO modes for continuous waveforms

---

## Measure Signals

### I want to measure pulse width
**Chapter 13: Timing Measurement**
- Specifically: P_HIGH_TICKS (%10001) for high-pulse duration
- Specifically: P_STATE_TICKS (%10000) for both high and low

### I want to measure signal frequency
**Chapter 15: Period and Frequency Measurement**
- Specifically: P_COUNTER_PERIODS (%10111) with 1-second gate
- Also consider: P_PERIODS_TICKS for period-based measurement

### I want to measure signal period
**Chapter 15: Period and Frequency Measurement**
- Specifically: P_PERIODS_TICKS (%10011) over multiple periods
- Also consider: P_COUNTER_TICKS for time-window measurement

### I want to measure duty cycle
**Chapter 15: Period and Frequency Measurement**
- Specifically: Use P_PERIODS_TICKS and P_PERIODS_HIGHS together
- Also consider: P_COUNTER_TICKS with P_COUNTER_HIGHS

### I want to measure time between events
**Chapter 13: Timing Measurement**
- Specifically: P_EVENTS_TICKS (%10010) for event timing
- Also consider: Timeout detection capability

### I want to count events
**Chapter 14: Counting**
- Specifically: P_COUNT_RISES for rising edges
- Specifically: P_COUNT_HIGHS for high states
- Also consider: P_QUADRATURE for bidirectional counting

### I want to measure analog voltage (ADC)
**Chapter 16: ADC (Analog Input)**
- Specifically: P_ADC (%11000) with SINC2 filtering
- Also consider: Gain options (P_ADC_1X through P_ADC_100X)

### I want to receive serial data (UART)
**Chapter 17: Serial Receive**
- Specifically: P_ASYNC_RX (%11111) for UART
- Also consider: P_INVERT_IN for RS-232 polarity

### I want to receive serial data (SPI)
**Chapter 17: Serial Receive**
- Specifically: P_SYNC_RX (%11101) for SPI slave
- Also consider: Clock routing with P_PLUS1_B

---

## Control Outputs

### I want to turn a pin on or off
**Chapter 6: Digital Output**
- Specifically: PINHIGH/PINLOW or PINNOT
- Also consider: PINWRITE for value-based control

### I want to control LED brightness
**Chapter 9: PWM Output**
- Specifically: P_PWM_TRIANGLE for smooth fading
- Also consider: P_NCO_DUTY for simple duty control

### I want to control motor speed
**Chapter 9: PWM Output**
- Specifically: P_PWM_SAWTOOTH for standard DC motor PWM
- Also consider: P_PWM_SMPS for H-bridge applications

### I want to control servo position
**Chapter 7: Transition and Pulse Output**
- Specifically: P_PULSE for 1-2ms pulse generation
- Also consider: PWM modes with 50Hz frequency

### I want to output precise analog levels
**Chapter 10: DAC Output**
- Specifically: P_DAC_DITHER_PWM for best dynamic range
- Also consider: External DAC for higher resolution

---

## Read Inputs

### I want to read a button or switch
**Chapter 12: Digital Input**
- Specifically: PINREAD with pull-up (P_HIGH_15K)
- Also consider: Schmitt trigger (P_SCHMITT_A) for noisy signals

### I want to read a digital sensor
**Chapter 12: Digital Input**
- Specifically: TESTP for fast flag-based reading
- Also consider: Input conditioning options

### I want to read a rotary encoder
**Chapter 14: Counting**
- Specifically: P_QUADRATURE (%01011) for quadrature decoding
- Also consider: Velocity measurement from position changes

### I want to read an analog sensor
**Chapter 16: ADC (Analog Input)**
- Specifically: P_ADC with appropriate gain setting
- Also consider: Averaging for noise reduction

### I want to read multiple pins at once
**Chapter 12: Digital Input**
- Specifically: INA/INB register access
- Also consider: PINREAD with ADDPINS for pin groups

---

## Communicate

### I want to use UART/RS-232
**Chapter 11: Serial Transmit** and **Chapter 17: Serial Receive**
- Specifically: P_ASYNC_TX and P_ASYNC_RX
- Also consider: P_INVERT_IN/P_INVERT_OUT for RS-232 levels

### I want to be an SPI master
**Chapter 11: Serial Transmit** and **Chapter 17: Serial Receive**
- Specifically: P_SYNC_TX for data out, separate clock pin
- Also consider: NCO mode for clock generation

### I want to be an SPI slave
**Chapter 17: Serial Receive**
- Specifically: P_SYNC_RX (%11101) with clock routing
- Also consider: Data justification (left-justified)

### I want to implement I2C
Multiple modes required:
- Clock stretching with input monitoring
- Open-drain output configuration
- Consider using existing I2C library

### I want to use USB
**Chapter 19: USB Host/Device**
- Specifically: P_USB_PAIR (%11011) on even/odd pin pair
- Also consider: Using existing USB library (recommended)

---

## Coordinate and Synchronize

### I want to synchronize multiple pin outputs
**Chapter 7: Transition and Pulse Output**
- Specifically: SETSE1/WAITSE1 for event synchronization
- Also consider: Common X register base for timing

### I want to share data between COGs
**Chapter 18: Repository and Inter-COG Data Sharing**
- Specifically: P_REPOSITORY (non-DAC mode of %00001-%00011)
- Also consider: RQPIN for non-blocking reads

### I want precise timing control
**Chapter 5: Pin Timing**
- Specifically: Understanding 3-clock output/input latency
- Also consider: TESTP for 2-clock input path

### I want to generate synchronized waveforms
**Chapter 8: NCO Frequency**
- Specifically: Multiple NCO pins with related frequencies
- Also consider: Common base period for phase alignment

---

## Quick Mode Lookup

| Mode | Constant | Primary Use |
|------|----------|-------------|
| %00001 | P_REPOSITORY / P_DAC_NOISE | Inter-COG data / Noise |
| %00010 | P_DAC_DITHER_RND | 16-bit DAC (random dither) |
| %00011 | P_DAC_DITHER_PWM | 16-bit DAC (PWM dither) |
| %00100 | P_PULSE | Pulse generation |
| %00101 | P_TRANSITION | Clock/transition output |
| %00110 | P_NCO_FREQ | Frequency synthesis |
| %00111 | P_NCO_DUTY | Duty cycle control |
| %01000 | P_PWM_TRIANGLE | Triangle PWM |
| %01001 | P_PWM_SAWTOOTH | Sawtooth PWM |
| %01010 | P_PWM_SMPS | SMPS PWM |
| %01011 | P_QUADRATURE | Quadrature encoder |
| %01100-%01111 | P_COUNT_* | Counting modes |
| %10000 | P_STATE_TICKS | Measure both states |
| %10001 | P_HIGH_TICKS | Measure high time |
| %10010 | P_EVENTS_TICKS | Event timing/timeout |
| %10011 | P_PERIODS_TICKS | Measure X periods |
| %10100 | P_PERIODS_HIGHS | Sum highs in X periods |
| %10101 | P_COUNTER_TICKS | Time in X-clock window |
| %10110 | P_COUNTER_HIGHS | Highs in X-clock window |
| %10111 | P_COUNTER_PERIODS | Count periods in X clocks |
| %11000 | P_ADC | Internal clock ADC |
| %11001 | P_ADC_EXT | External clock ADC |
| %11010 | P_ADC_SCOPE | Triggered scope ADC |
| %11011 | P_USB_PAIR | USB differential pair |
| %11100 | P_SYNC_TX | Synchronous serial TX |
| %11101 | P_SYNC_RX | Synchronous serial RX |
| %11110 | P_ASYNC_TX | Asynchronous serial TX |
| %11111 | P_ASYNC_RX | Asynchronous serial RX |

---

*For detailed mode descriptions, see the relevant chapter. For P_ constant values, see Appendix B.*
