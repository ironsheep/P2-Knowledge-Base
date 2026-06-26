# Appendix A: Intent Index

This appendix provides task-oriented navigation. Find what you want to accomplish, then follow the reference to the appropriate chapter and mode.

## Generate Signals

*Producing output — clocks, frequencies, PWM, analog, and serial.*

| I want to… | Go to | Primary mode | Also consider |
|------------|-------|--------------|---------------|
| Generate a clock signal | [Ch 7](#chapter-7-pulse-and-transition-generation) | `P_TRANSITION` (%00101) | `P_NCO_FREQ` |
| Generate a fixed frequency | [Ch 8](#chapter-8-frequency-generation-nco) | `P_NCO_FREQ` (%00110) | `P_TRANSITION` |
| Generate PWM (motor control) | [Ch 9](#chapter-9-pwm-output) | `P_PWM_SAWTOOTH` (%01001) | `P_PWM_SMPS` |
| Generate PWM (LED dimming) | [Ch 9](#chapter-9-pwm-output) | `P_PWM_TRIANGLE` (%01000) | `P_NCO_DUTY` |
| Generate audio tones | [Ch 8](#chapter-8-frequency-generation-nco) | `P_NCO_FREQ` (%00110) | DAC modes |
| Generate arbitrary waveforms | [Ch 10](#chapter-10-dac-output) | `P_DAC_DITHER_RND` / `P_DAC_DITHER_PWM` | NCO + lookup table |
| Output analog voltage | [Ch 10](#chapter-10-dac-output) | `P_DAC_990R_3V` (8-bit) | `P_DAC_DITHER_RND` (16-bit) |
| Transmit serial — UART | [Ch 11](#chapter-11-serial-transmission) | `P_ASYNC_TX` (%11110) | `P_INVERT_OUT` (RS-232) |
| Transmit serial — SPI | [Ch 11](#chapter-11-serial-transmission) | `P_SYNC_TX` (%11100) | clock polarity/phase |
| Generate precise pulses | [Ch 7](#chapter-7-pulse-and-transition-generation) | `P_PULSE` (%00100) | NCO modes |

## Measure Signals

*Reading signal characteristics — width, frequency, period, counts, analog.*

| I want to… | Go to | Primary mode | Also consider |
|---|---|---|---|
| Measure pulse width | [Ch 13](#chapter-13-timing-measurement) | `P_HIGH_TICKS` (%10001) | `P_STATE_TICKS` (%10000) for both states |
| Measure signal frequency | [Ch 15](#chapter-15-period-and-frequency-measurement) | `P_COUNTER_PERIODS` (%10111), 1-s gate | `P_PERIODS_TICKS` |
| Measure signal period | [Ch 15](#chapter-15-period-and-frequency-measurement) | `P_PERIODS_TICKS` (%10011) | `P_COUNTER_TICKS` |
| Measure duty cycle | [Ch 15](#chapter-15-period-and-frequency-measurement) | `P_PERIODS_TICKS` + `P_PERIODS_HIGHS` | `P_COUNTER_TICKS` + `P_COUNTER_HIGHS` |
| Measure time between events | [Ch 13](#chapter-13-timing-measurement) | `P_EVENTS_TICKS` (%10010) | timeout detection |
| Count events | [Ch 14](#chapter-14-counting-modes) | `P_COUNT_RISES` / `P_COUNT_HIGHS` | `P_QUADRATURE` (bidirectional) |
| Measure analog voltage (ADC) | [Ch 16](#chapter-16-adc-analog-input) | `P_ADC` (%11000), SINC2 | gain `P_ADC_1X`…`P_ADC_100X` |
| Receive serial — UART | [Ch 17](#chapter-17-serial-receive) | `P_ASYNC_RX` (%11111) | `P_INVERT_IN` (RS-232) |
| Receive serial — SPI | [Ch 17](#chapter-17-serial-receive) | `P_SYNC_RX` (%11101) | clock routing `P_PLUS1_B` |

## Control Outputs

*Driving actuators and indicators.*

| I want to… | Go to | Primary mode | Also consider |
|---|---|---|---|
| Turn a pin on or off | [Ch 6](#chapter-6-digital-output) | `PINHIGH` / `PINLOW` / `PINNOT` | `PINWRITE` (value-based) |
| Control LED brightness | [Ch 9](#chapter-9-pwm-output) | `P_PWM_TRIANGLE` | `P_NCO_DUTY` |
| Control motor speed | [Ch 9](#chapter-9-pwm-output) | `P_PWM_SAWTOOTH` | `P_PWM_SMPS` (H-bridge) |
| Control servo position | [Ch 7](#chapter-7-pulse-and-transition-generation) | `P_PULSE` (1–2 ms) | PWM at 50 Hz |
| Output precise analog levels | [Ch 10](#chapter-10-dac-output) | `P_DAC_DITHER_PWM` | external DAC |

## Read Inputs

*Sensing the outside world.*

| I want to… | Go to | Primary mode | Also consider |
|---|---|---|---|
| Read a button or switch | [Ch 12](#chapter-12-digital-input) | `PINREAD` + pull-up (`P_HIGH_15K`) | `P_SCHMITT_A` for noisy signals |
| Read a digital sensor | [Ch 12](#chapter-12-digital-input) | `TESTP` (fast flag read) | input conditioning options |
| Read a rotary encoder | [Ch 14](#chapter-14-counting-modes) | `P_QUADRATURE` (%01011) | velocity from position deltas |
| Read an analog sensor | [Ch 16](#chapter-16-adc-analog-input) | `P_ADC` + gain | averaging for noise |
| Read multiple pins at once | [Ch 12](#chapter-12-digital-input) | `INA` / `INB` registers | `PINREAD` with `ADDPINS` |

## Communicate

*Talking to other devices — UART, SPI, I²C, USB.*

| I want to… | Go to | Primary mode | Also consider |
|---|---|---|---|
| UART / RS-232 | [Ch 11](#chapter-11-serial-transmission) & [Ch 17](#chapter-17-serial-receive) | `P_ASYNC_TX` + `P_ASYNC_RX` | `P_INVERT_IN` / `P_INVERT_OUT` |
| Be an SPI master | [Ch 11](#chapter-11-serial-transmission) & [Ch 17](#chapter-17-serial-receive) | `P_SYNC_TX` + separate clock pin | NCO for clock generation |
| Be an SPI slave | [Ch 17](#chapter-17-serial-receive) | `P_SYNC_RX` (%11101) + clock routing | left-justified data |
| Implement I²C | [Ch 6](#chapter-6-digital-output) | open-drain + clock stretching | existing I²C library |
| Use USB | [Ch 19](#chapter-19-usb-hostdevice) | `P_USB_PAIR` (%11011), even/odd pair | existing USB library (recommended) |

## Coordinate and Synchronize

*Timing, events, and inter-cog coordination.*

| I want to… | Go to | Primary mode | Also consider |
|---|---|---|---|
| Synchronize multiple pin outputs | [Ch 7](#chapter-7-pulse-and-transition-generation) | `SETSE1` / `WAITSE1` events | shared X base period |
| Share data between Cogs | [Ch 18](#chapter-18-repository-and-inter-cog-data-sharing) | `P_REPOSITORY` (%00001, non-DAC) | `RQPIN` for non-blocking reads |
| Precise timing control | [Ch 1](#chapter-1-direct-io---the-foundation) | 3-clock output/input latency (§1.2) | `TESTP` for 2-clock input path |
| Generate synchronized waveforms | [Ch 8](#chapter-8-frequency-generation-nco) | multiple NCO pins, related freqs | common base period for phase |

## Quick Mode Lookup

| Mode | Constant | Primary Use |
|------|----------|-------------|
| %00001 | P_REPOSITORY / P_DAC_NOISE | Inter-Cog data / Noise |
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


*For detailed mode descriptions, see the relevant chapter. For P_ constant values, see Appendix B.*
