# P2 DEBUG Window Manual — Examples Library

These are the complete, runnable Spin2 programs that appear in the *P2 DEBUG
Window Manual*, one file per worked example, named by the chapter it appears in.

- **Exactly as printed.** Each file is the program shown in the manual, verbatim.
- **No capture facilities.** Unlike the figure-generators used to produce the
  manual's screenshots, these contain no `` `SAVE ``/`` `SAVE WINDOW ``/`` `CLOSE ``
  or `DEBUG_END_SESSION` commands.
- **Windows stay open.** Every program keeps running after the demo finishes —
  a Spin2 `repeat` loop (or, in the PASM examples, a `jmp` back into the cog
  loop) — so the program does not exit and close its DEBUG window(s).
- **Compiles clean.** Every file compiles with `pnut-ts -d` (the `-d` flag
  compiles the `debug()` directive contents as well).

Open one in your P2 toolchain, compile, and run on a P2 with the DEBUG terminal
attached — no external wiring is required.

## Index

| File | Window | Example |
|------|--------|---------|
| `ch01-getting-started-term.spin2` | TERM | Minimal first program — print to a TERM window |
| `ch02-term-print-value.spin2` | TERM | Your first window — print a value |
| `ch02-term-pin-config.spin2` | TERM | Optional DEBUG symbols / configuration |
| `ch02-term-signals.spin2` | TERM | Two software signal sources |
| `ch03-term-dashboard.spin2` | TERM | Positioned signal-monitor dashboard |
| `ch04-bitmap-heatmap.spin2` | BITMAP | 32×24 thermopile heatmap with a drifting warm spot |
| `ch05-plot-field.spin2` | PLOT | Animated sprite field |
| `ch05-plot-gauge.spin2` | PLOT | Analog gauge instrument |
| `ch05-plot-wave-scatter.spin2` | PLOT | Drawing-primitive tour — sine polyline + scatter |
| `ch05-plot-pid.spin2` | PLOT | PI control-loop strip chart |
| `ch06-logic-spi-bus.spin2` | LOGIC | Software SPI bus on a LOGIC window |
| `ch07-scope-three-channel.spin2` | SCOPE | Three-channel scope |
| `ch07-scope-triggered.spin2` | SCOPE | One-shot triggered capture |
| `ch07-scope-glitch.spin2` | SCOPE | Catch a rare glitch (trigger + holdoff) |
| `ch08-scope-xy-lissajous.spin2` | SCOPE_XY | Lissajous figure |
| `ch09-fft-spectrum.spin2` | FFT | Multi-tone spectrum |
| `ch10-spectro-runup.spin2` | SPECTRO | Motor run-up spectrogram (rising diagonal streak) |
| `ch11-midi-scale-chord.spin2` | MIDI | Play a scale and a chord |
| `ch11-midi-velocity.spin2` | MIDI | Velocity fill |
| `ch12-keyboard-adjust.spin2` | TERM (PC_KEY) | Adjust a value with the arrow keys |
| `ch12-mouse-pointer.spin2` | TERM (PC_MOUSE) | Read mouse pointer state |
| `ch13-packed-bitmap-frame.spin2` | BITMAP | Packed frame — `LONGS_1BIT` |
| `ch13-packed-logic-multi.spin2` | LOGIC | Packed 2-channel stream — `LONGS_2BIT` |
| `ch13-packed-logic-stream.spin2` | LOGIC | Packed stream — single channel `LONGS_1BIT` |
| `ch13-packed-scope.spin2` | SCOPE | Packed samples — `LONGS_8BIT` |
| `ch14-multiwindow.spin2` | SCOPE + TERM | Feed two windows in one loop |
| `ch14-pasm-inline.spin2` | TERM | Inline PASM (`ORG`/`END`) feeding a window |
| `ch14-pasm-scope.spin2` | SCOPE | PASM cog driving a SCOPE via `coginit` |
| `ch14-pasm-terminal.spin2` | TERM | PASM cog driving a TERM |
| `ch14-scope-trace.spin2` | SCOPE + TERM | "Try it" — peak-tracking trace |
| `ch15-control-panel.spin2` | PLOT | Interactive control panel |
| `ch15-dashboard.spin2` | TERM | Dashboard (technique 1) |
| `ch15-panel-plot.spin2` | PLOT | Sprite-sheet panel plot (technique 3) |
