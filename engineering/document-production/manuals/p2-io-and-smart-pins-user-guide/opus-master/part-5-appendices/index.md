# Index

Alphabetical index of terms, constants, and concepts in this guide.

---

## A

- **A-input** - Smart pin primary input, Ch. 3, 5
- **A-input routing** - P_PLUS1_A, P_MINUS1_A, etc., Ch. 3, App. B
- **Accumulator, phase** - NCO Z register, Ch. 8
- **ADC** - see Analog-to-Digital Conversion
- **ADC external clock** - P_ADC_EXT (%11001), Ch. 16
- **ADC gain** - P_ADC_1X through P_ADC_100X, Ch. 16
- **ADC internal clock** - P_ADC (%11000), Ch. 16
- **ADC scope** - P_ADC_SCOPE (%11010), Ch. 16
- **AKPIN** - Acknowledge pin (PASM2), Ch. 4
- **Analog input** - see ADC, Ch. 16
- **Analog output** - see DAC, Ch. 10
- **Asynchronous serial** - UART modes, Ch. 11, 17
- **Audio** - NCO tones Ch. 8, DAC waveforms Ch. 10, 18

## B

- **B-input** - Smart pin secondary input, Ch. 3, 5
- **B-input routing** - P_PLUS1_B, P_MINUS1_B, etc., Ch. 3, App. B
- **Base period** - X[15:0] in PWM and other modes, Ch. 9
- **Baud rate** - Serial timing calculation, Ch. 11, App. C
- **Baud rate error** - Calculation and tolerance, Ch. 11, App. E
- **Bit period** - Serial bit timing, Ch. 11, 17
- **BITDAC** - Single-bit DAC mode, Ch. 10
- **Bitstream** - Raw ADC output (X[5:4]=%11), Ch. 16
- **Buffer, double** - Serial TX modes, Ch. 11

## C

- **C flag** - State indicator in timing modes, Ch. 13
- **Clock generation** - P_TRANSITION, P_NCO_FREQ, Ch. 7, 8
- **Clock routing** - B-input for sync serial, Ch. 11, 17
- **COG** - Processor core, inter-COG sharing Ch. 18
- **Comparator input** - P_COMPARE_AB, Ch. 12
- **Continuous mode** - X=0 for counting, Ch. 14
- **Counter modes** - %01100-%01111, Ch. 14
- **Counting** - Event and period counting, Ch. 14
- **CPOL/CPHA** - SPI clock polarity/phase, Ch. 11

## D

- **DAC** - see Digital-to-Analog Conversion
- **DAC dithering** - 16-bit resolution modes, Ch. 10, 18
- **DAC noise** - P_DAC_NOISE (%00001), Ch. 18
- **DAC resistor modes** - P_DAC_990R_3V, etc., Ch. 10
- **Data bits** - Serial frame size, Ch. 11, 17
- **DIR** - Pin direction control, Ch. 3, 6
- **DIRH** - Set pin as output (PASM2), Ch. 4, 6
- **DIRL** - Set pin as input (PASM2), Ch. 4, 6
- **Dithering** - DAC resolution enhancement, Ch. 18
- **Drive strength** - P_HIGH_FAST, P_LOW_FAST, etc., Ch. 6, App. B
- **DRVH** - Drive pin high (PASM2), Ch. 4, 6
- **DRVL** - Drive pin low (PASM2), Ch. 4, 6
- **Duty cycle** - PWM ratio, Ch. 9; measurement Ch. 13, 15

## E

- **Edge counting** - P_COUNT_RISES, P_COUNT_RISES, Ch. 14
- **Encoder** - see Quadrature encoder
- **ENOB** - Effective number of bits (ADC), Ch. 16
- **Event timing** - P_EVENTS_TICKS, Ch. 13

## F

- **Filtering, input** - P_FILT0_AB through P_FILT3_AB, Ch. 12
- **Float** - see PINFLOAT
- **Fractional baud** - X[15:10] precision, Ch. 11
- **Frame period** - X[31:16] in PWM, Ch. 9
- **Frequency counter** - P_COUNTER_PERIODS, Ch. 15
- **Frequency generation** - NCO modes, Ch. 8
- **Frequency measurement** - Period modes, Ch. 15
- **Full Speed USB** - 12 Mbps, Ch. 19

## G

- **Gain, ADC** - P_ADC_1X through P_ADC_100X, Ch. 16
- **Gate time** - Frequency counter window, Ch. 15
- **Gated counting** - P_REG_UP, Ch. 14

## H

- **High-state counting** - P_COUNT_HIGHS, Ch. 14
- **High-state timing** - P_HIGH_TICKS, Ch. 13
- **Hub RAM** - vs. Repository, Ch. 18

## I

- **I2C** - Implementation notes, App. A
- **IN flag** - Smart pin status, Ch. 3, 4
- **INA/INB** - Input registers, Ch. 12
- **Input conditioning** - Schmitt, filter, compare, Ch. 12
- **Input routing** - A/B input selection, Ch. 3
- **Inter-COG** - Data sharing via Repository, Ch. 18
- **Inversion** - P_INVERT_A, P_INVERT_B, P_INVERT_OUTPUT, App. B

## L

- **Latency** - Pin I/O timing, Ch. 5
- **LED dimming** - PWM application, Ch. 9
- **Level comparison** - P_LEVEL_A modes, Ch. 12
- **LOCK bits** - vs. Repository, Ch. 18
- **Logic input** - P_LOGIC_A, Ch. 12
- **Low Speed USB** - 1.5 Mbps, Ch. 19
- **LSB first** - Serial bit order, Ch. 11, 17

## M

- **Mode number** - Smart pin mode (%XXXXX), Ch. 3, App. F
- **Motor control** - PWM application, Ch. 9
- **MSB first** - Bit reversal for SPI, Ch. 11

## N

- **NCO** - Numerically Controlled Oscillator, Ch. 8
- **NCO duty** - P_NCO_DUTY (%00111), Ch. 8
- **NCO frequency** - P_NCO_FREQ (%00110), Ch. 8
- **Noise, DAC** - P_DAC_NOISE, Ch. 18

## O

- **Open-drain** - P_HIGH_FLOAT configuration, Ch. 6
- **OUT** - Pin output state, Ch. 3, 6
- **OUTA/OUTB** - Output registers, Ch. 6
- **Output enable** - P_OE (TT bits), Ch. 3, App. B

## P

- **P_ADC** - ADC internal clock (%11000), Ch. 16, App. F
- **P_ADC_100X** - 100x gain ADC, Ch. 16
- **P_ADC_10X** - 10x gain ADC, Ch. 16
- **P_ADC_1X** - Unity gain ADC, Ch. 16
- **P_ADC_30X** - 31.6x gain ADC, Ch. 16
- **P_ADC_3X** - 3.16x gain ADC, Ch. 16
- **P_ADC_EXT** - ADC external clock (%11001), Ch. 16, App. F
- **P_ADC_FLOAT** - Floating ADC input, Ch. 16
- **P_ADC_GIO** - Ground-referenced ADC, Ch. 16
- **P_ADC_SCOPE** - Triggered scope (%11010), Ch. 16, App. F
- **P_ADC_VIO** - VIO-referenced ADC, Ch. 16
- **P_ASYNC_RX** - Async serial receive (%11111), Ch. 17, App. F
- **P_ASYNC_TX** - Async serial transmit (%11110), Ch. 11, App. F
- **P_BITDAC** - Bit DAC enable, Ch. 10
- **P_CHANNEL** - DAC channel enable, Ch. 10
- **P_COMPARE_AB** - A>B comparator, Ch. 12
- **P_COUNT_HIGHS** - Count high states (%01111), Ch. 14, App. F
- **P_COUNT_RISES** - Count rising edges (%01110), Ch. 14, App. F
- **P_COUNTER_HIGHS** - High time in window (%10110), Ch. 15, App. F
- **P_COUNTER_PERIODS** - Period count in window (%10111), Ch. 15, App. F
- **P_COUNTER_TICKS** - Period time in window (%10101), Ch. 15, App. F
- **P_DAC_124R_3V** - 124 ohm, 3.3V DAC, Ch. 10
- **P_DAC_600R_2V** - 600 ohm, 2.0V DAC, Ch. 10
- **P_DAC_75R_2V** - 75 ohm, 2.0V DAC, Ch. 10
- **P_DAC_990R_3V** - 990 ohm, 3.3V DAC, Ch. 10
- **P_DAC_DITHER_PWM** - PWM dithered DAC (%00011), Ch. 18, App. F
- **P_DAC_DITHER_RND** - PRNG dithered DAC (%00010), Ch. 18, App. F
- **P_DAC_NOISE** - DAC noise output (%00001), Ch. 18, App. F
- **P_EVENTS_TICKS** - Event timing (%10010), Ch. 13, App. F
- **P_FILT0_AB** through **P_FILT3_AB** - Input filtering, Ch. 12
- **P_HIGH_FAST** - Fast high drive, Ch. 6
- **P_HIGH_FLOAT** - Float high (open-drain), Ch. 6
- **P_HIGH_TICKS** - Measure high time (%10001), Ch. 13, App. F
- **P_INVERT_A** - Invert A-input, App. B
- **P_INVERT_B** - Invert B-input, App. B
- **P_INVERT_IN** - Invert IN bit, App. B
- **P_INVERT_OUTPUT** - Invert output, App. B
- **P_LEVEL_A** - Level comparison modes, Ch. 12
- **P_LOCAL_A** - Select local pin for A, App. B
- **P_LOCAL_B** - Select local pin for B, App. B
- **P_LOGIC_A** - Logic level input, Ch. 12
- **P_LOW_FAST** - Fast low drive, Ch. 6
- **P_LOW_FLOAT** - Float low (high-Z), Ch. 6
- **P_MINUS1_A** through **P_MINUS3_A** - A-input from pin-N, App. B
- **P_MINUS1_B** through **P_MINUS3_B** - B-input from pin-N, App. B
- **P_NCO_DUTY** - NCO variable duty (%00111), Ch. 8, App. F
- **P_NCO_FREQ** - NCO 50% duty (%00110), Ch. 8, App. F
- **P_NORMAL** - Normal I/O mode (%00000), Ch. 6, App. F
- **P_OE** - Output enable (TT=%01), Ch. 3, App. B
- **P_OUTBIT_A** - OUT bit to A-input, App. B
- **P_OUTBIT_B** - OUT bit to B-input, App. B
- **P_PERIODS_HIGHS** - High time for periods (%10100), Ch. 15, App. F
- **P_PERIODS_TICKS** - Time for periods (%10011), Ch. 15, App. F
- **P_PLUS1_A** through **P_PLUS3_A** - A-input from pin+N, App. B
- **P_PLUS1_B** through **P_PLUS3_B** - B-input from pin+N, App. B
- **P_PULSE** - Pulse output (%00100), Ch. 7, App. F
- **P_PWM_SAWTOOTH** - Sawtooth PWM (%01001), Ch. 9, App. F
- **P_PWM_SMPS** - SMPS PWM (%01010), Ch. 9, App. F
- **P_PWM_TRIANGLE** - Triangle PWM (%01000), Ch. 9, App. F
- **P_QUADRATURE** - Quadrature encoder (%01011), Ch. 14, App. F
- **P_REG_UP** - Gated increment (%01100), Ch. 14, App. F
- **P_REG_UP_DOWN** - Up/down counter (%01101), Ch. 14, App. F
- **P_REPOSITORY** - Inter-COG data (%00001), Ch. 18, App. F
- **P_SCHMITT_A** - Schmitt trigger A, Ch. 12
- **P_STATE_TICKS** - Time both states (%10000), Ch. 13, App. F
- **P_SYNC_IO** - Synchronous I/O, App. B
- **P_SYNC_RX** - Sync serial receive (%11101), Ch. 17, App. F
- **P_SYNC_TX** - Sync serial transmit (%11100), Ch. 11, App. F
- **P_TRANSITION** - Transition output (%00101), Ch. 7, App. F
- **P_TRUE_A** - Non-inverted A, App. B
- **P_TRUE_B** - Non-inverted B, App. B
- **P_TT_00** through **P_TT_11** - TT bit values, App. B
- **P_USB_PAIR** - USB differential (%11011), Ch. 19, App. F
- **Parity** - Software implementation, Ch. 11
- **Period measurement** - Modes %10011-%10111, Ch. 15
- **Periodic mode** - X>0 for counting, Ch. 14
- **Phase accumulator** - NCO Z register, Ch. 8
- **Phase synchronization** - NCO X[31:16], Ch. 8
- **PINFLOAT** - Float pin (Spin2), Ch. 4, 6
- **PINHIGH** - Drive pin high (Spin2), Ch. 4, 6
- **PINLOW** - Drive pin low (Spin2), Ch. 4, 6
- **PINNOT** - Toggle pin (Spin2), Ch. 4, 6
- **PINREAD** - Read IN flag (Spin2), Ch. 4
- **PINSTART** - Configure and start (Spin2), Ch. 4
- **PINWRITE** - Write pin value (Spin2), Ch. 4, 6
- **PRNG dithering** - Random DAC dither, Ch. 18
- **Pull-up/pull-down** - P_HIGH_15K, P_LOW_15K, etc., Ch. 6
- **Pulse measurement** - P_HIGH_TICKS, Ch. 13
- **Pulse output** - P_PULSE mode, Ch. 7
- **PWM** - Pulse Width Modulation, Ch. 9
- **PWM dithering** - Deterministic DAC dither, Ch. 18

## Q

- **Quadrature encoder** - P_QUADRATURE (%01011), Ch. 14
- **Quantization error** - Measurement accuracy, Ch. 13

## R

- **RDPIN** - Read Z, clear IN (PASM2), Ch. 4
- **Repository** - P_REPOSITORY (%00001), Ch. 18
- **Resolution** - ADC bits Ch. 16, PWM bits Ch. 9
- **RPM measurement** - Period counting, Ch. 15
- **RQPIN** - Read Z, keep IN (PASM2), Ch. 4
- **RS-232** - Inverted serial, Ch. 11, 17

## S

- **Sample period** - ADC X register, Ch. 16
- **Sample rate** - ADC calculation, Ch. 16, App. C
- **Sawtooth PWM** - P_PWM_SAWTOOTH, Ch. 9
- **Schmitt trigger** - P_SCHMITT_A, Ch. 12
- **Servo control** - Pulse output, Ch. 7, 9
- **SINC2 filter** - ADC filter mode, Ch. 16
- **SINC3 filter** - ADC filter mode, Ch. 16
- **Smart pin** - Hardware-autonomous I/O, Ch. 1, 3
- **SMPS** - Switch-mode power supply, Ch. 9
- **SPI** - Synchronous serial, Ch. 11, 17
- **Square wave** - NCO 50% duty, Ch. 8
- **Start bit** - Async serial framing, Ch. 11, 17
- **State timing** - P_STATE_TICKS, Ch. 13
- **Stop bit** - Async serial framing, Ch. 11, 17
- **Synchronous serial** - SPI modes, Ch. 11, 17
- **sysclk** - System clock frequency, Ch. 2

## T

- **TESTP** - Test IN flag (PASM2), Ch. 4
- **Three-phase** - NCO phase synchronization, Ch. 8
- **Timeout detection** - P_EVENTS_TICKS, Ch. 13
- **Timing measurement** - Modes %10000-%10010, Ch. 13
- **Transition output** - P_TRANSITION, Ch. 7
- **Triangle PWM** - P_PWM_TRIANGLE, Ch. 9
- **Trigger, hysteretic** - ADC scope, Ch. 16
- **TT bits** - DIR/OUT control, Ch. 3, App. B

## U

- **UART** - Async serial, Ch. 11, 17
- **Up/down counter** - P_REG_UP_DOWN, Ch. 14
- **USB** - P_USB_PAIR (%11011), Ch. 19

## V

- **Velocity measurement** - Quadrature periodic mode, Ch. 14
- **Voltage, DAC** - Output calculation, Ch. 10, App. C

## W

- **Watchdog** - Timeout detection, Ch. 13
- **WRPIN** - Write mode (PASM2), Ch. 4
- **WXPIN** - Write X (PASM2), Ch. 4
- **WYPIN** - Write Y (PASM2), Ch. 4

## X

- **X register** - Smart pin configuration, Ch. 3, 4

## Y

- **Y register** - Smart pin parameter, Ch. 3, 4

## Z

- **Z register** - Smart pin accumulator/result, Ch. 3, 4

---

## Appendix Cross-Reference

| Appendix | Title | Content |
|----------|-------|---------|
| A | Intent Index | Task-based navigation |
| B | P_ Constants | Complete constant reference |
| C | Formulas | Mathematical formulas |
| D | Mode Comparison | Selection charts |
| E | Troubleshooting | Problem/solution guide |
| F | Mode Reference | Quick reference per mode |

---

*Page numbers refer to chapter numbers in this digital document.*
