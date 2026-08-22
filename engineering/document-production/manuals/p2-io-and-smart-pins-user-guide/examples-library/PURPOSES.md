# Example purposes

The one header field `sync-manual-examples.py` will not derive. Everything else
in an example's header (the manual, the version, where it appears, the dates)
is read from the repository at sync time. This is the sentence a person writes.

Keep it to one line, and say what the example *shows*, not what it *is*.

- `ch01-button-led.spin2`: A pin read and a pin driven, with no smart pin involved - the baseline everything later is measured against
- `ch06-current-drive-blink.spin2`: The same blink, but choosing the drive strength the pin uses to get there
- `ch07-step-motor-pulses.spin2`: Transition mode issuing a precise pulse train, with the period and the low time set independently
- `ch08-three-phase-nco.spin2`: Three NCO pins sharing one frequency and differing only in phase - the offset lives in X, not in code
- `ch09-pwm-led-fade.spin2`: Sawtooth PWM at a flicker-free rate, and what to do when the period will not fit the counter
- `ch10-audio-dac.spin2`: A DAC pin fed at an audio sample rate, driven by the smart pin rather than by the cog
- `ch11-spi-master.spin2`: A synchronous serial master built from smart pins, clock and data kept in step by hardware
- `ch12-button-schmitt-led.spin2`: A noisy mechanical input made clean in the pin itself, with Schmitt thresholds instead of software debounce
- `ch13-ultrasonic-distance.spin2`: Pulse-width measurement turning an echo into a distance, timed by the pin and not by a loop
- `ch14-tachometer-rpm.spin2`: Counting edges over a fixed window to get RPM, where the window is what sets the resolution
- `ch15-oscillator-calibration.spin2`: Measuring a reference against the system clock to find the error in parts per million
- `ch16-adc-audio-capture.spin2`: A pin sampling as an ADC into a buffer, at the same rate the DAC example plays back
- `ch17-uart-command-loop.spin2`: Asynchronous serial receive as a smart pin, so the cog reads characters instead of bit-banging them
- `ch18-repository-multicog.spin2`: A pin used as shared storage between cogs - no hub variable, no lock
- `ch19-usb-device-config.spin2`: The pin pair and clock a USB device configuration requires before any transfer happens
