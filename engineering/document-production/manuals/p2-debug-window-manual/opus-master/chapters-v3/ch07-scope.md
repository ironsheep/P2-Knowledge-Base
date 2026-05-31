# Chapter 7: The SCOPE Window — Time-Domain Oscilloscope

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
> plots, Lissajous figures, XY trajectories — use the SCOPE_XY window in Chapter 8.
> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work here too and are covered for
> all windows together in Chapter 12. Packed data formats, which let you move
> samples faster over the debug link, are covered in Chapter 13.

## Creating the window and declaring its channels

You create and configure a SCOPE window in a single `DEBUG` statement. The first
token after the backtick is the window type (`SCOPE`); the second is a name you
choose and address the window by afterward. Configuration keywords and channel
declarations follow on the same line:

```spin2
PUB main() | ang
  debug(`SCOPE Sig SIZE 400 200 'Wave' AUTO)   ' create, one auto-ranging channel
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
| `SIZE` | `width height` | `512 256` | Display size in pixels; each is **32–2048** |
| `SAMPLES` | `count` | `512` | Horizontal resolution — sets displayed at once; **16–2048** |
| `RATE` | `divisor` | `1` | Display-update divisor (see "Considerations"); **1–2048** |
| `DOTSIZE` | `pixels` | `0` | Dot diameter; **0–32** (`0` = no dots) |
| `LINESIZE` | `pixels` | `3` | Line thickness; **0–32** (`0` = no lines) |
| `TEXTSIZE` | `points` | `9` | Label font size; **6–200** |
| `COLOR` | `back grid` | black / gray | Background color, then grid color (`$RRGGBB` each) |
| `HIDEXY` | — | off | Hides the mouse-coordinate readout |
| Packing keyword | — | `LONGS_1BIT` | Sets the data-packing format (see Chapter 13) |

If you set both `DOTSIZE` and `LINESIZE` to `0`, the window forces a dot size of 1
so traces remain visible.

### Channels are declared as elements, not keywords

You do not declare channels with a `CHANNELS` or `LABELS` keyword. Each channel is
introduced by a **quoted label** in the creation stream, optionally followed by
numeric arguments that configure that one channel:

```
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

```
TRIGGER channel {AUTO | arm fire} {offset}
```

| Argument | Meaning |
|----------|---------|
| `channel` | Which channel to watch: `-1` disables the trigger (free-run), `0`–`7` selects a channel |
| `AUTO` | Auto-trigger — the window computes the arm and fire levels from the signal's range |
| `arm fire` | Manual arm and fire levels (use these *instead of* `AUTO`) |
| `offset` | Where the trigger point sits in the display, `0`..`SAMPLES-1` (default: `SAMPLES/2`) |

```spin2
debug(`Capture TRIGGER 0 -500 500 256)   ' channel 0, arm -500, fire 500, centered
debug(`Capture TRIGGER 0 AUTO)            ' channel 0, levels chosen automatically
debug(`Capture TRIGGER -1)                ' disable: back to free-running
```

### Direction is set by the levels, not a keyword

There is no `RISING` or `FALLING` keyword. The direction follows from how `fire`
compares to `arm`:

- **`fire` ≥ `arm` → rising-edge trigger.** The window arms when the signal falls to
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
debug(`Capture HOLDOFF 512)   ' ignore new triggers for 512 samples after one fires
```

The holdoff count ranges from **2 to 2048**. It defaults to `SAMPLES` — one full
screen — so by default the window will not re-trigger until it has shown the
captured frame.

## Clearing and saving

Two more runtime commands round out the set:

- `` `CLEAR `` — clears the display and resets the sample buffer, so the next samples
  start a fresh trace from the right edge.
- `` `SAVE `` — saves the current display image to a `.bmp` file on the host. An
  optional filename may follow; without one, the host names the file.

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
  ' Three stacked channels: fixed -1000..1000 range, 100px tall, offset by 'base'
  debug(`SCOPE Waves SIZE 512 300 SAMPLES 256 LINESIZE 2 ...
    'Sine'  -1000 1000 100   0 0 $00FF00 ...
    'Tri'   -1000 1000 100 100 0 $FF0000 ...
    'Noise' -1000 1000 100 200 0 $00AAFF)

  ang := 0
  tri := -1000
  dir := 40

  repeat
    sine  := qsin(1000, ang, 256)          ' CORDIC sine, amplitude 1000, 256 steps/cycle
    tri   += dir                           ' ramp up/down for a triangle
    if tri >= 1000 or tri <= -1000
      dir := -dir
    noise := (GETRND() // 2001) - 1000     ' random in -1000..1000

    debug(`Waves `(sine) `(tri) `(noise))  ' one set: three values, in channel order

    ang += 4
    waitms(5)                              ' your loop sets the time scale
```

To turn the same display into a **triggered capture**, declare one channel and add a
trigger. The window then waits for the signal to rise through 0 (armed below −500,
fired at or above 500 — `fire` ≥ `arm`, so rising) and freezes a 512-sample frame
with the trigger point centered:

```spin2
CON
  _clkfreq = 200_000_000

PUB main() | ang, sig
  debug(`SCOPE Capture SIZE 512 256 SAMPLES 512 'Signal' -1000 1000)
  debug(`Capture TRIGGER 0 -500 500 256)   ' rising edge, trigger centered in the frame
  debug(`Capture HOLDOFF 512)              ' one frame of holdoff before re-arming

  ang := 0
  repeat
    sig := qsin(1000, ang, 256)
    debug(`Capture `(sig))
    ang += 3
    waitms(2)
```

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
  packing keywords (Chapter 13) move more samples per `DEBUG` packet over the link.

## Try it

Start from the three-channel example. First switch the `Sine` channel from its fixed
`-1000 1000` range to `AUTO` and watch the trace rescale on its own as you change the
amplitude argument to `qsin`. Then add a trigger on the sine channel
(`debug(`Waves TRIGGER 0 -500 500 256)`) and observe the waveform stand still instead
of scrolling. Finally, vary the trigger `offset` between `0`, `SAMPLES/2`, and
`SAMPLES-1` to move the trigger point from the right edge to the center to the left
edge, and see the pre-trigger region grow.
