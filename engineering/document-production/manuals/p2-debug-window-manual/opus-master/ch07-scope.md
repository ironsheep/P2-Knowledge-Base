# Chapter 7: The SCOPE Window — Time-Domain Oscilloscope {#ch-7}

The SCOPE window plots values against time, the way a bench oscilloscope does.
You send it a stream of samples; it scrolls them across the display, newest at the
right, oldest at the left. Where the TERM window shows you *what* a value is, the
SCOPE window shows you *how it changes* — the shape of a waveform, the settling of
a signal, the moment an event crosses a threshold.

One SCOPE window holds up to **eight channels**, each with its own label, color,
vertical range, and position. Behind the display is a circular buffer of **2048
sample sets** per window — a set being one sample from every active channel. You
declare the window once, naming its channels in the same statement, and then feed
it bare numeric values for the rest of the run.

> SCOPE plots one value against time. For one value against *another* value — phase
> plots, Lissajous figures, XY trajectories — use the SCOPE_XY window in [Chapter 8](#ch-8).
> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work here too and are covered for
> all windows together in [Chapter 12](#ch-12). Packed data formats, which let you move
> samples faster over the debug link, are covered in [Chapter 13](#ch-13).

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.80\linewidth]{inbox/assets/fig-07-scope.png}
\caption{The SCOPE window displaying a time-domain sine waveform.}
\end{figure}
```

## Creating the window and declaring its channels

You create and configure a SCOPE window in a single `DEBUG` statement. The first
token after the backtick is the window type (`SCOPE`); the second is a name you
choose and address the window by afterward. Configuration keywords and channel
declarations follow on the same line:

```spin2
PUB main() | ang
  ' create, one auto-ranging channel
  debug(`SCOPE Sig SIZE 400 200 'Wave' AUTO)
  ang := 0
  repeat
    debug(`Sig `(qsin(1000, ang, 256)))         ' feed it by name
    ang += 4
    waitms(5)
```

The configuration keywords you can place on the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | `Scope` | The window's title-bar text |
| `POS` | `left top` | cascaded | Screen position of the window, in pixels |
| `SIZE` | `width height` | `256 256` | Display size in pixels; each is **32–2048** |
| `SAMPLES` | `count` | `256` | Horizontal resolution — sets displayed at once; **16–2048** |
| `RATE` | `divisor` | `1` | Display-update divisor (see "Considerations"); **1–2048** |
| `DOTSIZE` | `pixels` | `0` | Dot diameter; **0–32** (`0` = no dots) |
| `LINESIZE` | `pixels` | `3` | Line thickness; **0–32** (`0` = no lines) |
| `TEXTSIZE` | `points` | `10` | Label font size; **6–200** |
| `COLOR` | `back grid` | black / gray | Background color, then grid color (`$RRGGBB` each) |
| `HIDEXY` | — | off | Hides the mouse-coordinate readout |
| Packing keyword | — | `LONGS_1BIT` | Sets the data-packing format (see [Chapter 13](#ch-13)) |

If you set both `DOTSIZE` and `LINESIZE` to `0`, the window forces a dot size of 1
so traces remain visible.

### Channels are declared as elements, not keywords

You do not declare channels with a `CHANNELS` or `LABELS` keyword. Each channel is
introduced by a **quoted label** in the creation stream, optionally followed by
numeric arguments that configure that one channel:

```debug-config
'label' {AUTO | lo hi} {tall} {base} {grid} {color}
```

The window reads the label, then reads the optional numeric arguments **in order**:

| Argument | Meaning | If omitted |
|----------|---------|------------|
| `AUTO` | Auto-range this channel (mutually exclusive with `lo hi`) | manual range used |
| `lo hi` | Manual range: value at the bottom and top of the trace area | full 32-bit range |
| `tall` | Vertical span of the trace, in pixels | full window height |
| `base` | Vertical offset of the trace, in pixels | `0` |
| `grid` | Grid spacing (accepted but not rendered by SCOPE) | `0` |
| `color` | Trace color, `$RRGGBB` | next from the default palette |

The first label after `SCOPE` becomes channel 0, the next becomes channel 1, and so
on, up to eight. So this declares three channels:

```spin2
debug(`SCOPE Waves SIZE 512 300 SAMPLES 256 ...
  'Sine'  -1000 1000 100   0 0 $00FF00 ...
  'Tri'   -1000 1000 100 100 0 $FF0000 ...
  'Noise' -1000 1000 100 200 0 $00AAFF)
```

Each channel here has a fixed range of −1000 to 1000, is 100 pixels tall, and is
offset vertically by `base` (0, 100, 200) so the three traces stack instead of
overlapping. The `grid` argument is `0`, and the last value is the trace color.

> The arguments are positional. To set `color`, you must supply the arguments before
> it. If you want auto-ranging *and* a specific color, give `AUTO` followed by the
> `tall`, `base`, and `grid` values, then the color — for example
> `'Wave' AUTO 100 0 0 $00FF00`.

### AUTO versus a manual range

A channel declared `AUTO` rescales itself on every redraw: the window scans the
channel's samples currently in the buffer, finds their minimum and maximum, and maps
that span to the trace height. This tracks an unknown signal without your having to
know its amplitude in advance, at the cost of a display whose scale shifts as the
signal changes.

A channel declared with `lo hi` keeps a fixed scale: `lo` sits at the bottom of the
trace area and `hi` at the top, regardless of what the samples do. Use a manual
range when you know the signal's bounds and want a stable display you can read
against. If `lo` is greater than `hi`, the display is simply inverted — high values
at the bottom.

## Sending samples

Once the window exists, you feed it by name. Send **one bare numeric value per
active channel**, in channel order, using the `` `() `` value form:

```spin2
debug(`Waves `(sine) `(tri) `(noise))   ' three channels: one set
```

Each complete set of values — one per channel — advances the time base by one
column. The window stores the set in its circular buffer and scrolls the display.
With a single channel you send a single value:

```spin2
debug(`Sig `(value))
```

The sample timing is entirely yours: the window plots a set whenever one arrives, so
the spacing of your `DEBUG` calls in the loop is what determines the time scale. A
`waitms` or `waitx` in the loop sets how fast samples are produced.

> Send sample values with the `` `() `` form, which transmits the *value*. This is
> the same distinction as in the TERM chapter: `` `udec_(x) `` would send the visible
> *digits* of `x`, which is not what a sample stream wants.

## Triggering

By default a SCOPE window free-runs: it redraws continuously as samples arrive. A
**trigger** instead holds the display until the signal does something specific —
crosses a level in a particular direction — so a repeating waveform appears
stationary and a one-shot event is captured at a known position.

You configure the trigger at runtime with the `TRIGGER` command:

```debug-update
TRIGGER channel {AUTO | arm fire} {offset}
```

| Argument | Meaning |
|----------|---------|
| `channel` | Which channel to watch: `-1` disables the trigger (free-run), `0`–`7` selects a channel |
| `AUTO` | Auto-trigger — the window computes the arm and fire levels from the signal's range |
| `arm fire` | Manual arm and fire levels (use these *instead of* `AUTO`) |
| `offset` | Where the trigger point sits in the display, `0`..`SAMPLES-1` (default: `SAMPLES/2`) |

```spin2
' channel 0, arm -500, fire 500, centered
debug(`Capture TRIGGER 0 -500 500 256)
debug(`Capture TRIGGER 0 AUTO)  ' channel 0, levels chosen automatically
debug(`Capture TRIGGER -1)                ' disable: back to free-running
```

### Direction is set by the levels, not a keyword

There is no `RISING` or `FALLING` keyword. The direction follows from how `fire`
compares to `arm`:

- **`fire` >= `arm` → rising-edge trigger.** The window arms when the signal falls to
  or below `arm`, then fires when it rises to or above `fire`.
- **`fire` < `arm` → falling-edge trigger.** The window arms when the signal rises to
  or above `arm`, then fires when it falls to or below `fire`.

The two-level scheme (arm one place, fire at another) gives the trigger hysteresis,
so noise around a single threshold does not produce repeated false triggers. To
trigger on a rising signal at 500, set `arm` below it and `fire` at 500
(`TRIGGER 0 -500 500`); to trigger on a falling signal at 500, put `arm` above
`fire` (`TRIGGER 0 700 500`).

With `AUTO`, the window scans the trigger channel's range and sets
`arm = low + range/3` and `fire = low + range/2` — a rising-edge trigger near the
middle of the signal.

### Trigger position with offset

The `offset` argument places the trigger point within the displayed window, measured
in samples from `0` to `SAMPLES-1`:

- `0` puts the trigger at the **right** edge — you see only what happens after the event.
- `SAMPLES-1` puts it at the **left** edge — you see the lead-up *to* the event (pre-trigger).
- `SAMPLES/2` (the default) centers it, showing equal time before and after.

The trigger is evaluated only once the buffer holds a full `SAMPLES` worth of data,
so the pre-trigger region is always populated.

### HOLDOFF

After a trigger fires, `HOLDOFF` suppresses re-triggering for a number of samples,
which steadies the display of a busy or bursty signal:

```spin2
' ignore new triggers for 512 samples after one fires
debug(`Capture HOLDOFF 512)
```

The holdoff count ranges from **2 to 2048**. It defaults to `SAMPLES` — one full
screen — so by default the window will not re-trigger until it has shown the
captured frame.

## Clearing and saving

Three more runtime commands round out the set:

- `` `CLEAR `` — clears the display and resets the sample buffer, so the next samples
  start a fresh trace from the right edge.
- `` `SAVE `` — saves the current display image to a `.bmp` file on the host. An
  optional filename may follow; without one, the host names the file.
- `` `CLOSE `` — closes this window and frees its resources.

```spin2
debug(`Sig SAVE)    ' write the current trace to a bitmap on the PC
debug(`Sig CLEAR)   ' wipe the buffer and start over
```

## A complete worked example

This program needs no wiring. It generates three software waveforms and plots them
on three stacked SCOPE channels: a CORDIC sine (`QSIN`), a counter-driven triangle,
and random noise from `GETRND`. It compiles with `pnut_ts` and runs on a bare P2
board with `pnut_term_ts` open.

```spin2
CON
  _clkfreq = 200_000_000

PUB main() | ang, sine, tri, dir, noise
  ' Three stacked channels: fixed -1000..1000 range,
  ' 100px tall, offset by 'base'
  debug(`SCOPE Waves SIZE 512 300 SAMPLES 256 LINESIZE 2 ...
    'Sine'  -1000 1000 100   0 0 $00FF00 ...
    'Tri'   -1000 1000 100 100 0 $FF0000 ...
    'Noise' -1000 1000 100 200 0 $00AAFF)

  ang := 0
  tri := -1000
  dir := 40

  repeat
    ' CORDIC sine, amplitude 1000, 256 steps/cycle
    sine  := qsin(1000, ang, 256)
    tri   += dir                           ' ramp up/down for a triangle
    if tri >= 1000 or tri <= -1000
      dir := -dir
    noise := (GETRND() // 2001) - 1000     ' random in -1000..1000

    ' one set: three values, in channel order
    debug(`Waves `(sine) `(tri) `(noise))

    ang += 4
    waitms(5)                              ' your loop sets the time scale
```

## Acquisition: catching a fast event over a slow link

[Chapter 1](#ch-1) named the debt plainly: every sample you send crosses the
2 Mbaud debug link, so a *continuous* full-rate stream of a fast signal will not
fit. The SCOPE window is still the right tool for fast signals — you just stop
streaming them live and use the two techniques every bench oscilloscope uses
instead. Both are fully synthetic here; neither needs hardware.

### Capture and dump — full fidelity, one window per trigger

The **capture-and-dump** strategy ([Chapter 1](#ch-1)) decouples the measurement
from the link. A tight loop — in PASM when you need full speed — fills a
**circular buffer at the P2's own sample rate**, overwriting oldest with newest,
while it tests a trigger condition on every pass: a level crossing, a bus
pattern, an out-of-range fault. When the trigger fires, you **freeze the buffer
and dump it once** over the link — the pre-trigger samples already captured plus a
post-trigger tail. The fidelity of what you caught is set by **how fast your loop
runs and how deep your buffer is, not by the link**, which only carries the one
readout. You see one frame per trigger and are blind between events; that is the
price of full detail, and it is exactly the oscilloscope's *arm → acquire →
trigger → freeze → read out* model.

The SCOPE window models this directly: a `TRIGGER` holds the display on the event
and freezes the frame. Recasting the free-running display as a **one-shot
capture** is one line of setup. Here the window waits for the signal to rise past
500 (armed below at −500, fired at or above 500 — `fire` >= `arm`, so rising) and
freezes a 512-sample frame with the trigger point centered:

```spin2
CON
  _clkfreq = 200_000_000

PUB main() | ang, sig
  ' SCOPE takes its channel declaration as a feed to the window name
  debug(`SCOPE Capture SIZE 512 256 SAMPLES 512)
  debug(`Capture 'Signal' -1000 1000)
  ' rising edge, trigger centered in the frame
  debug(`Capture TRIGGER 0 -500 500 256)
  debug(`Capture HOLDOFF 512)  ' one frame of holdoff before re-arming

  ang := 0
  repeat
    sig := qsin(1000, ang, 256)
    debug(`Capture `(sig))
    ang += 3
    waitms(2)
```

The trigger and the buffer belong to the acquisition, not to the link. In a real
high-rate capture you would move that arm-and-test loop into PASM so it runs at
full speed, and only the frozen frame would ever cross the wire.

#### Worked example: catch a rare glitch

This is the capture-and-dump pattern end to end, fully synthetic. A clean,
low-amplitude signal — it stands in for any quiet line you are watching —
occasionally throws a single out-of-range spike. A `TRIGGER` set well above the
clean signal's range arms on the quiet signal and fires the moment a spike
crosses it, freezing a 512-sample frame with the glitch centered, its lead-up to
the left and its aftermath to the right:

```spin2
CON
  _clkfreq = 200_000_000

PUB main() | ang, n, sig
  debug(`SCOPE Glitch SIZE 512 256 SAMPLES 512)
  debug(`Glitch 'Signal' -1000 1000)
  ' arm on the quiet signal, fire on the spike (fire >= arm -> rising)
  debug(`Glitch TRIGGER 0 200 800 256)   ' centered: see before and after
  debug(`Glitch HOLDOFF 512)

  ang := 0
  n   := 0
  repeat
    sig := qsin(300, ang, 256)           ' clean signal, well inside range
    if n // 233 == 0                     ' a rare, occasional fault
      sig := 950                         ' one out-of-range sample
    debug(`Glitch `(sig))
    ang += 5
    n   += 1
    waitms(1)
```

The display free-runs on the quiet signal until a spike crosses 800; then it
locks, showing the glitch at the center of the frame with the clean signal before
and after it. `HOLDOFF` keeps it from re-arming until you have had a full frame to
read the captured event.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.80\linewidth]{inbox/assets/fig-07-scope-glitch.png}
\caption{A rare out-of-range glitch frozen by a SCOPE trigger, shown with its lead-up and aftermath.}
\end{figure}
```

### Decimate — a live trend, at the cost of detail

When you want a *continuous* view of a slowly-evolving signal rather than a frozen
event, **decimate** ([Chapter 1](#ch-1)): send only one sample in every N. The
window updates forever; you have traded resolution for a live trend. The naive
form — take every Nth sample — carries a trap any instrument engineer will warn
you about: a narrow spike that lands between the kept samples simply disappears,
and a periodic signal can alias into a slower phantom.

```spin2
' naive: keep 1 in 8 -- a one-cycle spike between samples is lost
if n // 8 == 0
  debug(`Trend `(sig))
```

The honest fix is **min/max (peak) decimation**: over each group of N samples keep
both the smallest and the largest, and send both. A one-cycle spike now survives,
because it lands as the group's min or max even though you never sent that exact
sample:

```spin2
' peak decimation: keep the extremes of each group of 8
lo := lo <# sig                          ' running min (<# = limit max)
hi := hi #> sig                          ' running max (#> = limit min)
if n // 8 == 7
  debug(`Trend `(lo) `(hi))              ' two traces preserve the spike
  lo := POSX                             ' reset for the next group
  hi := NEGX
```

Decimation is always-on but lossy; capture-and-dump is perfect but episodic.
**Choose by whether you are watching a *trend* or hunting an *event*.**

### Where you'd use this

In computer science and computer engineering, the SCOPE window is the everyday
tool for **DSP work** — inspecting a waveform, the response of a filter, the
settling of a control loop — and for **power and control electronics**, where the
shape of a signal in time is the measurement.

**On an embedded project**, you reach for it to watch an ADC capture, a PWM edge
or duty cycle, supply ripple or inrush at power-on (a triggered one-shot),
contact bounce on a switch, or an intermittent fault line — the glitch-capture
pattern above.

**Bandwidth fit:** low-rate live signals stream comfortably; a fast transient is
caught as a triggered one-shot; a *continuous* high-rate analog stream does not
fit, and is the case the acquisition strategies above exist to handle.

**Extension (real hardware):** replace the synthetic `qsin`/spike source with a
real sampled input — read an ADC or a smart pin in the loop — and the same
channel, trigger, and capture code shows the live signal.

## Considerations

- **`RATE` is a display-update divisor, not a sample rate in Hz.** With `RATE 1`
  (the default) the window redraws on every sample set. With `RATE 16` it accepts and
  buffers every set but redraws only on every sixteenth — which lowers the host's
  drawing load for fast streams. It does not change how often *you* send samples.
- **You set the time scale, not the window.** The horizontal axis is one column per
  sample set. How fast time appears to move is set by the spacing of your `DEBUG`
  calls — the `waitms`/`waitx` in your loop — not by any window parameter.
- **`AUTO` adapts; a manual range stays put.** Auto-ranging follows an unknown signal
  but shifts scale as the signal changes; a fixed `lo hi` gives a stable, readable
  display when you know the bounds. For a steady trace, prefer a manual range.
- **Stack channels with `base`, scale them with `tall`.** Give each channel a height
  (`tall`) smaller than the window and a stepped `base` offset to lay multiple traces
  out without overlap, as the worked example does.
- **`SAMPLES` sets horizontal resolution and trigger depth.** It is also the default
  holdoff and the default trigger offset, so raising `SAMPLES` widens the captured
  frame and the pre-trigger window together.
- **For high sample rates, pack the data.** Bare per-channel values are simplest; the
  packing keywords ([Chapter 13](#ch-13)) move more samples per `DEBUG` packet over the link.

## Try it

Start from the three-channel example. First switch the `Sine` channel from its fixed
`-1000 1000` range to `AUTO` and watch the trace rescale on its own as you change the
amplitude argument to `qsin`. Then add a trigger on the sine channel
(`debug(`Waves TRIGGER 0 -500 500 256)`) and observe the waveform stand still instead
of scrolling. Finally, vary the trigger `offset` between `0`, `SAMPLES/2`, and
`SAMPLES-1` to move the trigger point from the right edge to the center to the left
edge, and see the pre-trigger region grow.
