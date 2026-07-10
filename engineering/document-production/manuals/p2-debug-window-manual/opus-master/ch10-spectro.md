# Chapter 10: The SPECTRO Window — Spectrogram Waterfall {#ch-10}

The SPECTRO window shows how a signal's frequency content changes over time. It
runs an FFT on a sliding window of samples, turns each transform into one line of
colored pixels — one pixel per frequency bin, color set by that bin's magnitude —
and scrolls the line stack so the newest spectrum appears at the edge and older
spectra drift away. The result is a *waterfall*: frequency along one axis, time
along the other, intensity carried by color.

This is the difference between SPECTRO and the FFT window of [Chapter 9](#ch-9). The FFT
window draws one spectrum at a time as a magnitude-versus-frequency graph and
redraws it on every update; you see *now*, and nothing else. SPECTRO keeps a
history. A tone that slides up in pitch traces a diagonal streak; a steady harmonic
draws a straight line; a transient flashes as a short band. SPECTRO is **single
channel** — it analyzes one stream of samples, unlike the FFT window's up-to-eight
overlaid channels.

You create one SPECTRO window per `` DEBUG(`SPECTRO ...) `` declaration, name it, and
feed it samples by that name. This chapter covers creating the window, feeding it,
choosing scroll direction and update rate, mapping magnitude to color, and the
runtime commands.

> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work in the SPECTRO window, but
> they share one mechanism across every window type and are covered together in
> [Chapter 12](#ch-12). This chapter is about the display.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.65\linewidth]{inbox/assets/fig-10-spectro.png}
\caption{The SPECTRO window as a motor run-up: rising vibration frequency draws a diagonal streak down the waterfall.}
\end{figure}
```

## Creating a SPECTRO window

You create and configure the window in a single `DEBUG` statement. The first token
after the backtick is the window type (`SPECTRO`); the second is a name you choose.
You feed it afterward by that name:

```spin2
debug(`SPECTRO Wfall SAMPLES 512 DEPTH 256 RANGE $40000 LUMA8X)
debug(`Wfall `(sample))      ' feed it one sample by name
```

The configuration keywords for the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | `SPECTRO` | The window's title-bar text |
| `POS` | `left top` | auto | Screen position of the window, in pixels |
| `SAMPLES` | `count` | `512` | FFT size; a power of two, **4–2048** |
| `DEPTH` | `pixels` | `256` | Time-history depth (the scrolling dimension), **1–2048** |
| `RANGE` | `value` | `$7FFFFFFF` | Magnitude ceiling — the bin magnitude that maps to full color, **1–$7FFFFFFF** |
| `RATE` | `samples` | `SAMPLES`/8 | Samples taken in between display updates, **1–2048** |
| `TRACE` | `mode` | `15` | Scroll direction and scroll-enable (see "Scroll direction") |
| `MAG` | `shift` | `0` | Magnitude pre-scale; multiplies FFT output by 2^shift, **0–11** |
| `DOTSIZE` | `x [y]` | `1` | Pixel scaling; one value sets both axes, two set them separately, **1–16** |
| *color mode* | — | `LUMA8X` | One color-mode keyword (see "Color mapping") |
| `LOGSCALE` | — | linear | Logarithmic magnitude scaling instead of linear |
| `HIDEXY` | — | off | Hides the coordinate readout |

`SAMPLES` is the first decision. It sets the FFT size, and the FFT produces
`SAMPLES`/2 frequency bins spanning DC up to the Nyquist frequency (half your
effective sample rate). A `SAMPLES 512` window analyzes 512 points into 256 bins;
`SAMPLES 2048` gives 1024 bins. `SAMPLES` is rounded to a power of two — values that
are not powers of two are reduced to the next lower power, and the range is clamped
to 4–2048.

`SAMPLES` and `DEPTH` set the two axes. The frequency axis is `SAMPLES`/2 bins long.
The time axis is `DEPTH` pixels long — that is how many past spectra stay on screen
before scrolling off. Which axis is horizontal and which is vertical depends on
`TRACE`, covered below.

> **`SAMPLES` is the FFT size, not a keyword named `FFT_SIZE`.** There is no
> `FFT_SIZE`, no `OVERLAP`, and no windowing option — the analysis window is a fixed
> Hanning window, identical to the FFT window's. You control the transform through
> `SAMPLES`, `RANGE`, `MAG`, and `LOGSCALE`.

## Feeding samples

After the window exists, send signed sample values by its name. Each value is one
time-domain sample. Send the *value* with `` `() `` — not a display formatter, which
would print visible digits rather than deliver a number:

```spin2
debug(`Wfall `(sample))
```

Internally the window stores samples in a circular buffer. It does nothing visible
until it has collected a full `SAMPLES` window; from then on it runs an FFT over the
most recent `SAMPLES` samples whenever the rate counter says it is time, and plots
the result as one line. You keep feeding samples; the window decides when to
transform and draw.

You can send several samples in one `DEBUG` call by listing them, and you can pack
multiple samples per long for higher throughput. SPECTRO uses the same 12-mode
packing scheme as the other sampling windows: a packing keyword on the feed selects
how many samples each long carries; an optional `SIGNED` keyword sign-extends them.

```spin2
debug(`SPECTRO Pk SAMPLES 512 RANGE $4000 LONGS_8BIT SIGNED LUMA8X)
' four signed bytes -> four samples ($C0 = -64)
debug(`Pk `($7F | $40 << 8 | $C0 << 16 | $10 << 24))
```

The packing keywords are `LONGS_1BIT`, `LONGS_2BIT`, `LONGS_4BIT`, `LONGS_8BIT`,
`LONGS_16BIT`, and `WORDS_1BIT`/`2BIT`/`4BIT`/`8BIT` and
`BYTES_1BIT`/`2BIT`/`4BIT`. Every mode delivers unsigned (zero-extended) values by
default; append the optional `SIGNED` keyword to sign-extend them. `LONGS_8BIT`
carries four 8-bit samples per long, a 4× bandwidth gain over sending one sample
per long.

## Scroll direction — TRACE

`TRACE` does two jobs in one value, **0–15**:

- **Bits 0–2** select one of eight trace directions.
- **Bit 3** enables scrolling. With bit 3 clear (`TRACE` 0–7) the window *wraps* —
  new lines overwrite from the opposite edge with no scrolling. With bit 3 set
  (`TRACE` 8–15) the bitmap *scrolls* one line per update, the classic waterfall.

The direction bits also decide which axis is frequency and which is time. Directions
0–3 lay frequency along the horizontal axis and scroll the time history vertically;
directions 4–7 put time on the horizontal axis and frequency vertical. The window
swaps its width and height accordingly when it sizes itself.

The default is `TRACE 15` — direction 7 with scrolling on. For a downward-scrolling
waterfall with frequency across the top, use `TRACE 8`:

```spin2
debug(`SPECTRO Wfall SAMPLES 512 DEPTH 256 TRACE 8 RANGE $40000 LUMA8X)
```

For a vertical waterfall scrolling sideways — frequency up the side, time advancing
horizontally — use a direction in the 4–7 group with bit 3 set, for example
`TRACE 12`:

```spin2
debug(`SPECTRO Vert SAMPLES 256 DEPTH 400 TRACE 12 RANGE $20000 HSV16X LOGSCALE)
```

> **Set scrolling on (`TRACE` 8–15) for a waterfall.** Values 0–7 wrap in place,
> which overwrites old history rather than scrolling it away. The scrolling forms
> are what give SPECTRO its waterfall behavior.

## Update rate — RATE

`RATE` is the number of samples the window collects between display updates. It does
not change the FFT size; it controls how often a new line is drawn, and therefore
how fast the waterfall scrolls. Smaller `RATE` means more updates per second and
faster scrolling at higher CPU cost; larger `RATE` means slower scrolling.

The default is `SAMPLES`/8 — for a 512-point FFT, an update every 64 samples. The
effective scroll rate in lines per second is your sample feed rate divided by
`RATE`. Set `RATE` to control how much real time each line of the display
represents.

```spin2
debug(`SPECTRO Slow SAMPLES 2048 DEPTH 200 RATE 512 TRACE 8 RANGE $80000 LUMA8X)
```

`RATE` accepts **1–2048**.

## Color mapping

SPECTRO turns each bin's magnitude into a color. First the magnitude is scaled:
`RANGE` is the magnitude that maps to full intensity, so it sets the display's
sensitivity. A single value — `RANGE $40000` — is the ceiling; magnitudes at or
above it saturate, magnitudes below scale proportionally to 0–255. There is no
floor, no second value. Lower `RANGE` to make weak signals brighter; raise it when
strong signals wash out.

```spin2
debug(`SPECTRO Sens SAMPLES 512 RANGE $8000 MAG 4 LOGSCALE LUMA8X)
```

Two more controls shape the magnitude before color:

- **`MAG shift`** multiplies the FFT output by 2^shift (a 0–11 bit pre-shift),
  raising low-level signals before scaling.
- **`LOGSCALE`** applies logarithmic magnitude scaling instead of linear, which
  compresses a wide dynamic range so faint detail stays visible alongside strong
  peaks.

The scaled 0–255 value then drives a color-mode keyword. The modes SPECTRO accepts
on its creation line are the luminance and 16-bit HSV families:

| Keyword | Encoding | What it does |
|---------|----------|--------------|
| `LUMA8` | 8-bit luminance | Black-to-color ramp; magnitude sets brightness |
| `LUMA8W` | 8-bit luminance | White-to-color ramp (inverted) |
| `LUMA8X` | 8-bit luminance | Extended-range luminance — the default |
| `HSV16` | 16-bit HSV | Hue/saturation/value; magnitude in value |
| `HSV16W` | 16-bit HSV | White variant |
| `HSV16X` | 16-bit HSV | Extended range |

`LUMA8X` is the default if you name no mode. The luminance modes render a brightness
ramp — the natural "heat map" look for a single magnitude. The HSV16 modes encode
phase as well: the FFT's per-bin phase angle is folded into the hue while magnitude
drives the value, so an HSV16 waterfall shows both how strong each frequency is and
its phase relationship. Choose a luminance mode when magnitude is all you need;
choose an HSV16 mode when phase matters.

> The theory-of-operations lists additional color-encoding constants (HSV8, RGBI8,
> RGB8/16/24, and LUT modes) shared across the display infrastructure, but SPECTRO's
> own configuration parser accepts only the LUMA8 and HSV16 families above. Those are
> the modes to use here.

## Runtime commands — CLEAR, SAVE, and CLOSE

Three keyword commands work at runtime, sent by the window's name:

- `` `CLEAR `` — clears the display, resets the sample buffer (so the window waits
  for a fresh full window before drawing again), and resets the trace position to
  its starting edge.
- `` `SAVE `` — saves the current window image to a file on the host.
- `` `CLOSE `` — closes this window and frees its resources.

```spin2
debug(`Wfall CLEAR)
debug(`Wfall SAVE)
```

Use `` `CLEAR `` to start a new capture cleanly — after it, the next `SAMPLES`
samples refill the buffer before anything new is drawn.

## A complete software-only example: a motor run-up

This program needs no wiring. It synthesizes a signal that stands in for the
**vibration of a motor as it runs up to speed**. A spinning motor vibrates most
strongly at its shaft-rotation frequency; as it accelerates from rest to full
speed, that tone climbs. We make exactly that with the CORDIC: a sine tone whose
frequency rises block by block. Fed to a downward-scrolling SPECTRO, the rising
vibration draws a **diagonal streak** down the waterfall — the run-up captured as
a picture.

```{.spin2 caption="ch10-spectro-runup.spin2"}
CON
  _clkfreq = 200_000_000

PUB main() | i, phase, ainc, sample
  ' One scrolling spectrogram, 512-point FFT, 256 lines of history.
  debug(`SPECTRO RunUp SAMPLES 512 DEPTH 256 RANGE $40000 RATE 512 TRACE 8 LUMA8X)

  phase := 0
  ainc  := 8_000_000           ' shaft frequency at rest (a low tone)

  repeat
    ' Feed one 512-sample FFT window at the current speed, then accelerate.
    repeat i from 1 to 512
      sample := sine(2000, phase)
      phase += ainc            ' advance the synthesized vibration tone
      debug(`RunUp `(sample))
    ainc += 5_000_000  ' motor speeds up -> higher tone -> diagonal streak
    if ainc > 400_000_000
      debug(`RunUp CLEAR)      ' reached top speed: clear and run up again
      ainc := 8_000_000

PRI sine(amp, angle) : y
  ' amp * sin(angle), via the CORDIC.
  ' angle $0000_0000..$FFFF_FFFF spans one full circle.
  org
    qrotate amp, angle         ' X = amp, Y = 0 (no SETQ)
    getqy   y                  ' Y result = amp * sin(angle)
  end
```

`sine()` uses **QROTATE** to rotate the point (amp, 0) by `angle`; **GETQY** returns
the Y component, which is `amp x sin(angle)`. Stepping `phase` by `ainc` each sample
produces a tone whose frequency is set by `ainc` — the stand-in for shaft speed;
raising `ainc` after every 512-sample block accelerates the motor, and the
waterfall records the climb as a diagonal. The Hanning window is applied inside the
FFT automatically; you supply only the samples.

Hold `ainc` constant and the motor runs at a steady speed — the same frequency
every block draws a straight vertical streak (with `TRACE 8`). A structural
resonance the machine passes through on its way up shows as a bright spot where the
climbing tone crosses that fixed frequency — exactly the resonance-crossing a
machine-health engineer watches for during run-up and coast-down.

### Where you'd use this

In computer science and computer engineering, SPECTRO is the tool for **spectral
monitoring over time** — watching how a signal's frequency content evolves — in
narrowband RF and communications and in acoustics and speech analysis.

**On an embedded project**, its natural home is **machine-health monitoring**:
trending a motor or bearing's vibration spectrum so you can see a fault band grow,
watching resonance crossings during run-up and coast-down (as here), or following a
narrowband or voice signal over time.

**Bandwidth fit:** vibration and acoustic monitoring live at sub-10 kHz and play
out over seconds to minutes — low sample rate, long duration — which is exactly
what the link and the waterfall want. A full-rate RF or music spectrum does not fit
and is out.

**Extension (real hardware):** replace the synthetic `sine()` with real samples
from an accelerometer or microphone — read an ADC or I²S input in the feed loop —
and the waterfall shows live machine vibration.

## Considerations

- **Single channel.** SPECTRO analyzes one sample stream. To compare several signals
  in the frequency domain at one instant, the FFT window ([Chapter 9](#ch-9)) overlays up to
  eight channels; SPECTRO trades that for time history on one channel.
- **The window is a fixed Hanning window.** You cannot select a different window
  function or set overlap. Spectral leakage is what Hanning gives you — the same as
  the FFT window.
- **`SAMPLES` trades frequency resolution against time resolution.** Large `SAMPLES`
  (e.g. 2048) gives fine frequency detail but each line averages more time; small
  `SAMPLES` (e.g. 128) reacts fast in time but resolves frequency coarsely. Pick to
  match whether you care more about *which* frequency or *when*.
- **`RATE` sets scroll speed, `DEPTH` sets how much history is visible.** They are
  independent: `RATE` is samples-per-line, `DEPTH` is lines-on-screen. Together they
  determine the real-time span shown.
- **Tune visibility with `RANGE`, then `MAG`/`LOGSCALE`.** Start by setting `RANGE`
  near your expected peak magnitude. If weak detail is still too dark, add `MAG` to
  pre-amplify or `LOGSCALE` to compress the dynamic range.
- **Pack for throughput.** A high sample feed rate over the DEBUG link benefits from
  `LONGS_8BIT` or similar; packing multiplies how many samples each long carries.

## Try it

Start from the run-up example. Then:

1. **Switch axes.** Change `TRACE 8` to `TRACE 12` and watch the waterfall scroll
   sideways with frequency up the side.
2. **Add a second source.** Sum a second `sine()` at a fixed frequency into each
   sample so a steady horizontal line — a second machine running at constant speed —
   sits alongside the moving diagonal; toggle it on and off per block to see it
   appear and vanish:

   ```spin2
   sample := sine(1500, p1)
   p1 += 200_000
   if t & 1
     sample += sine(1500, p2)   ' second tone toggles per block
     p2 += 600_000
   ```

3. **Reveal weak detail.** Lower `RANGE`, then add `LOGSCALE`, and compare how much
   more of the spectrum becomes visible.

You will have used `SAMPLES`, `RANGE`, `TRACE`, `RATE`, a color mode, and `CLEAR`
together — and built a working spectrogram with no hardware beyond the P2 board.
