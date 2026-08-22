# Example purposes

The one header field `sync-manual-examples.py` will not derive. Everything else
in an example's header (the manual, the version, where it appears, the dates)
is read from the repository at sync time. This is the sentence a person writes.

Keep it to one line, and say what the example *shows*, not what it *is*.

- `ch01-getting-started-term.spin2`: The first window - one directive creates it, and the next line already prints into it
- `ch02-term-pin-config.spin2`: A TERM window standing in for a serial console while pin configuration is worked out
- `ch02-term-print-value.spin2`: Printing a live value rather than a message, so the window becomes a readout
- `ch02-term-signals.spin2`: Several named signals sharing one window, each keeping its own line
- `ch03-term-dashboard.spin2`: Colour used to separate fields, turning a text window into a status panel
- `ch04-bitmap-heatmap.spin2`: A BITMAP window as a heat map, where the pixel value IS the measurement
- `ch05-plot-field.spin2`: PLOT as a drawing surface, with the origin at bottom-left and Y running up
- `ch05-plot-gauge.spin2`: A dial drawn from primitives - polar placement doing the work an image would otherwise do
- `ch05-plot-pid.spin2`: A control loop watched as it settles, setpoint and response on one pair of axes
- `ch05-plot-wave-scatter.spin2`: The same data as a trace and as a scatter, showing what each view hides
- `ch06-logic-declare.spin2`: Declaring named channels up front, so the LOGIC window labels its own rows
- `ch06-logic-spi-bus.spin2`: A real SPI transaction captured on three channels, read as a bus rather than as pins
- `ch07-scope-glitch.spin2`: A short glitch caught because the sample window was sized for it
- `ch07-scope-three-channel.spin2`: Three traces at once, with line size chosen so they stay distinguishable
- `ch07-scope-triggered.spin2`: A trigger holding the trace still, instead of chasing a free-running signal
- `ch08-scope-xy-lissajous.spin2`: Two signals plotted against each other, where the figure itself reports the phase
- `ch09-fft-spectrum.spin2`: A time-domain buffer shown as frequency, with a log scale so small peaks survive
- `ch10-spectro-runup.spin2`: A motor run-up as a spectrogram - frequency against time, with the change as the subject
- `ch11-midi-scale-chord.spin2`: A scale and a chord on the MIDI keyboard, showing notes sounding together
- `ch11-midi-velocity.spin2`: Velocity carried as colour, so a dynamic passage is legible at a glance
- `ch12-keyboard-adjust.spin2`: Arrow keys read back from the window, making a display into an input
- `ch12-mouse-pointer.spin2`: Mouse position and buttons reported live, with the window as the pointing device
- `ch13-packed-bitmap-frame.spin2`: A whole 1-bit frame pushed as packed longs through a LUT palette
- `ch13-packed-logic-multi.spin2`: Two channels packed 2 bits at a time, fed as the full-window array the format requires
- `ch13-packed-logic-stream.spin2`: A continuous 1-bit stream packed into longs, one full window per message
- `ch13-packed-scope.spin2`: Packed 8-bit samples into a SCOPE window, config and data sent separately
- `ch14-multiwindow.spin2`: Two independent windows open at once, each with its own position and configuration
- `ch14-pasm-inline.spin2`: A debug window fed from an inline-PASM org/end block inside a Spin2 method
- `ch14-pasm-scope.spin2`: A SCOPE window fed from a PASM cog launched with coginit, not from Spin2
- `ch14-pasm-terminal.spin2`: The same from a PASM cog into TERM, showing debug works below Spin2
- `ch14-scope-trace.spin2`: A scan traced into a positioned SCOPE window while other windows stay put
- `ch15-control-panel.spin2`: PLOT built into a control panel, where the window both shows state and takes input
- `ch15-dashboard.spin2`: A titled status window collecting the values worth watching in one place
- `ch15-panel-plot.spin2`: A compact plot panel with the axes hidden, sized to sit alongside other windows
