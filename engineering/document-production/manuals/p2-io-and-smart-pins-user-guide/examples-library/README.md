# P2 I/O & Smart Pins User Guide — Examples Library

These are the complete, runnable Spin2 programs that appear in the *P2 I/O & Smart
Pins User Guide*, one flagship worked example per I/O-mode chapter, named by the
chapter it appears in.

- **Exactly as printed.** Each file is the program shown in the guide, verbatim — the
  same code carried by the printed caption (e.g. `ch09-pwm-led-fade.spin2`) under the
  block.
- **One per mode.** This is a curated set, not a dump of every code block. The guide's
  many teaching snippets — the per-mode configuration sequences, bit-field layouts,
  and one- or two-line fragments — are *not* here; only the flagship program that
  shows each I/O mode end to end.
- **Keeps running.** Each program stays alive — either the cog loops (a `repeat`), or
  the program configures an autonomous smart pin and returns, leaving the pin
  generating, measuring, or converting on its own.
- **Compiles clean.** Every file compiles with `pnut-ts` (the two with `debug()`
  output compile clean with `pnut-ts -d`).

Open one in your P2 toolchain, compile, and run it on a P2.

## Index

| File | Chapter | What it shows |
|------|---------|---------------|
| `ch01-button-led.spin2` | 1 — Direct I/O | Read a button and mirror it to an LED with `PINREAD`/`PINHIGH`/`PINLOW` |
| `ch06-current-drive-blink.spin2` | 6 — Digital Output | Blink an LED using a configured constant-current drive for steady brightness |
| `ch07-step-motor-pulses.spin2` | 7 — Pulse and Transition | Generate a counted burst of step pulses in `P_PULSE` mode |
| `ch08-three-phase-nco.spin2` | 8 — Frequency Generation (NCO) | Three NCO pins at one frequency with 0°/120°/240° phase offsets |
| `ch09-pwm-led-fade.spin2` | 9 — PWM Output | Fade an LED up and down with sawtooth PWM (`P_PWM_SAWTOOTH`) |
| `ch10-audio-dac.spin2` | 10 — DAC Output | Dithered audio DAC driven by a CORDIC sine generator |
| `ch11-spi-master.spin2` | 11 — Serial Transmission | Synchronous-serial (SPI) master: clocked transmit + register write |
| `ch12-button-schmitt-led.spin2` | 12 — Digital Input | Debounced button input via a Schmitt-trigger pin |
| `ch13-ultrasonic-distance.spin2` | 13 — Timing Measurement | Measure an echo pulse width to read ultrasonic distance |
| `ch14-tachometer-rpm.spin2` | 14 — Counting Modes | Count rising edges over a fixed window to compute RPM |
| `ch15-oscillator-calibration.spin2` | 15 — Period and Frequency | Measure a reference period to calibrate an oscillator in ppm |
| `ch16-adc-audio-capture.spin2` | 16 — ADC (Analog Input) | Capture an audio buffer with the SINC2 ADC and a precise sample period |
| `ch17-uart-command-loop.spin2` | 17 — Serial Receive | Asynchronous-serial (UART) receive driving a line-editing command loop |
| `ch18-repository-multicog.spin2` | 18 — Repository | Share a sensor reading between cogs through a pin repository |
| `ch19-usb-device-config.spin2` | 19 — USB Host/Device | Configure a USB device-mode pin pair (`P_USB_PAIR`) |
