# Example purposes — P2AN003

One line per shipped example. `sync-manual-examples.py` reads these into the
generated header's `Purpose....` field; it will not invent one. ASCII only —
the header is `.spin2` source, and the authoring guide's rule is absolute.

- `dac-sample-playback.spin2` — Play a stored sample buffer at any pitch with a phase accumulator, paced by the DAC's IN event
- `dac-waveform-synthesis.spin2` — Compute a sine, sawtooth or triangle from a DDS phase and drive it out a single DAC pin
- `dac-dithering.spin2` — Walk the full 16-bit code range to compare PRNG and PWM dither on a filtered scope
- `dac-adc-passthrough.spin2` — Read a pin's ADC every sample period and re-emit the value on a DAC pin
- `dac-mixing-panning.spin2` — Sum three DDS voices and pan them to a stereo pair of DAC pins
