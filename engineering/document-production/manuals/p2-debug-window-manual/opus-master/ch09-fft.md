# Chapter 9: The FFT Window — Frequency Spectrum

The FFT window shows you the *frequency content* of a signal. Where SCOPE plots
a value against time — the waveform itself — FFT takes a block of samples,
transforms it, and plots magnitude against frequency. A steady tone that looks
like a sine wave on SCOPE shows up on FFT as a single tall spike at that tone's
frequency. Mix three tones together and you see three spikes; add noise and you
see a low carpet under them.

The window runs a Cooley-Tukey FFT on the samples you feed it and displays the
resulting **magnitude spectrum** — one point per frequency bin, drawn as a line,
dot, or filled-bar trace. It supports up to **8 channels**, each transformed and
drawn independently.

You create one FFT window per `` DEBUG(`FFT ...) `` declaration, name it, and feed
it samples by that name. This chapter covers creating the window, setting the FFT
size, feeding samples across one or more channels, the two amplitude controls
(magnitude shift and log scale), reading the spectrum, and the runtime commands.

> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work in the FFT window, but they
> share one mechanism across every window type, so they are covered together in
> Chapter 12. This chapter is about the spectrum display.

![The FFT window showing two tones as spectral peaks.](inbox/assets/fig-09-fft.png){width=80%}

## What the FFT window does with your samples

You send a continuous stream of time-domain samples. The window stores them in a
circular buffer and, once it has collected a full block of `N` samples, it:

1. Multiplies the block by a **Hanning window** to reduce spectral leakage.
2. Runs the FFT.
3. Computes the magnitude of each of the `N/2` frequency bins.
4. Draws the bins you asked for across the plot area.

The Hanning window is **applied internally on every transform** and is not
configurable — there is no keyword to change it, and no choice of Hamming,
Blackman, Flattop, or rectangular windowing. Every spectrum you see has been
Hanning-windowed.

The transform produces `N/2` bins because a real-valued input signal has a
spectrum that is symmetric about the Nyquist frequency; only the lower half
carries unique information. Bin 0 is the DC (zero-frequency) component and bin
`N/2 - 1` is the highest frequency the transform resolves.

## Creating an FFT window

You create and configure the window in a single `DEBUG` statement. The first
token after the backtick is the window type (`FFT`); the second is a name you
choose. You feed it afterward by that name:

```spin2
PUB main() | s
  debug(`FFT Spectrum SIZE 512 256 SAMPLES 1024)   ' create the window
  repeat
    repeat 1024
      s := qsin(20000, getct(), $1_0000)           ' a sample
      debug(`Spectrum `(s))                         ' feed it by name
```

The configuration keywords you can add to the creation line:

| Keyword | Arguments | Default | What it sets |
|---------|-----------|---------|--------------|
| `TITLE` | `'text'` | `FFT` | The window's title-bar text |
| `POS` | `left top` | auto | Screen position of the window, in pixels |
| `SIZE` | `width height` | — | Plot area in pixels; each is **32–2048** |
| `SAMPLES` | `N {first last}` | `512` | FFT size, and an optional displayed bin range |
| `RATE` | `count` | one per buffer | Redraw every `count` samples (**1–2048**) |
| `DOTSIZE` | `radius` | `0` | Dot radius in pixels (**0–32**) |
| `LINESIZE` | `width` | `3` | Line width (**−32–32**; negative draws filled bars) |
| `TEXTSIZE` | `points` | `10` | Label font size |
| `COLOR` | `back grid` | black/grey | Background color, then grid/frame color (`$RRGGBB`) |
| `LOGSCALE` | — | off | Logarithmic (log2-based) amplitude scaling |
| `HIDEXY` | — | off | Hides the coordinate readout |
| packing | — | off | Sample packing format (see "Packing samples") |

`SAMPLES` is the one that defines the transform. The other essential is `SIZE`,
which sets the pixel dimensions of the plot area.

### Setting the FFT size with SAMPLES

`SAMPLES N` sets the FFT size. `N` must be a **power of 2 between 4 and 2048**;
the value you give is clamped to that range and rounded down to the nearest power
of 2, so `SAMPLES 1000` becomes 512 and `SAMPLES 1024` stays 1024. The default,
if you omit `SAMPLES` entirely, is 512.

The window displays bins `0` through `N/2 - 1` by default — the full spectrum.
You can restrict the display to a contiguous **range of bins** by adding two more
numbers:

```spin2
debug(`FFT Zoom SIZE 512 256 SAMPLES 1024 100 400)
```

This still runs a 1024-point transform but draws only bins 100 through 400,
stretched across the full plot width — a zoom into one frequency region. The
first bin must be in `0 ... N/2 - 2` and the last in `first+1 ... N/2 - 1`.

## Feeding samples and declaring channels

Once the window exists, every bare number you send by its name is a **sample**.
Samples are signed integers; the window collects them into its buffer and
transforms a block at a time.

You declare a channel by sending a **string** — the channel's label — optionally
followed by per-channel settings. The first string declares channel 0, the second
declares channel 1, and so on, up to 8 channels. After a channel is declared, the
samples you send are distributed across the declared channels in order: with two
channels declared, samples alternate channel 0, channel 1, channel 0, channel 1.

A channel declaration takes these arguments, in order, all optional after the
label:

| Position | Meaning | Range |
|----------|---------|-------|
| label | Channel name (string) | — |
| `MAG` shift | Magnitude bit-shift | **0–11** |
| high | Full-scale value for the Y axis | `1 ... $7FFF_FFFF` |
| tall | Channel height in pixels | — |
| base | Baseline offset from the bottom, in pixels | — |
| grid | Grid flags: bit 0 = baseline line, bit 1 = top line | — |
| color | Trace color (`$RRGGBB`) | — |

A single green channel, full height, with a baseline grid line:

```spin2
debug(`Spectrum 'Signal' 0 $7FFF_FFFF 256 0 1 $00FF00)
```

Read that as: label `Signal`, magnitude shift 0, full scale `$7FFF_FFFF`, 256
pixels tall, baseline at the bottom (`base` 0), grid flag 1 (baseline line),
color green.

To stack two channels in one window — say a left and right pair, one in the lower
half and one in the upper half — declare both, then interleave their samples:

```spin2
PUB main() | a, b
  debug(`FFT Dual SIZE 512 256 SAMPLES 512)
  debug(`Dual 'Left'  0 $7FFF_FFFF 128 0   1 $00FF00 'Right' 0 $7FFF_FFFF 128 128 1 $FF7F00)
  repeat
    repeat 512
      a := qsin(20000, getct(), $1_0000)
      b := qsin(10000, getct(), $1_0000)
      debug(`Dual `(a) `(b))               ' one sample per channel
```

`Left` sits in the bottom 128 pixels (base 0), `Right` in the top 128 (base 128).
Each channel is transformed independently and drawn in its own color. Channels are
drawn back-to-front, so the first-declared channel ends up on top where they
overlap.

## Amplitude: magnitude shift and log scale

The FFT output is in arbitrary units — not decibels, and not an absolute scale.
You have two independent controls over how tall the spectrum is drawn.

**`MAG` (per channel, 0–11)** is a bit-shift applied to the transform output: a
`MAG` of `n` multiplies the magnitude by 2ⁿ. Use it to bring up a weak signal
(`MAG 3` multiplies by 8) or to pull down one that saturates the top of the plot
(`MAG 0`). It is set in the channel declaration, in the `MAG` shift position
shown above.

**`LOGSCALE`** is a bare flag on the creation line. It applies a **log2-based**
compression to the amplitude before drawing, expanding small values and
compressing large ones so a wide dynamic range fits in one window. When
`LOGSCALE` is active, the window also draws power-of-2 markers (1, 2, 4, 8, …)
along the amplitude axis.

`LOGSCALE` is **not a decibel mode**. There is no dB scale, no dB markers, and no
keyword that produces one — the markers are powers of 2, and the underlying math
is log2 of the magnitude.

```spin2
debug(`FFT Spectrum SIZE 512 256 SAMPLES 512 LOGSCALE)
debug(`Spectrum 'Signal' 3 $7FFF_FFFF 256 0 1 $00FF00)   ' MAG 3
```

## Reading the spectrum: bins and frequency

The horizontal axis is **frequency bin number**, left to right, from `FFTfirst`
to `FFTlast`. The vertical axis is magnitude. The window itself does **not**
label the axis in Hz — it knows nothing about your sample rate. Converting a bin
to a frequency is a calculation you do yourself.

If you feed the window samples at a known rate, each bin corresponds to a fixed
frequency:

```
frequency of bin k  =  k x (sample_rate / N)
```

So with a 1024-point transform fed at 10 kHz, the bins are spaced
`10000 / 1024 ~ 9.77 Hz` apart, and bin 100 sits at about 977 Hz. The highest
bin, `N/2 - 1`, sits just below the Nyquist frequency `sample_rate / 2`; signal
content above Nyquist aliases down into the displayed range. Choosing the bin
range with `SAMPLES N first last` lets you zoom into the band you care about, but
the bin-to-Hz arithmetic — and any Hz labeling you want — is yours to add in your
own program or notes.

## Clearing and saving

Two runtime commands work in the feed stream:

- `` `CLEAR `` — erases the display and resets the sample buffer, so the next
  spectrum is built from fresh samples rather than blending with what was already
  collected.
- `` `SAVE 'name' `` — saves the current window image to `name.bmp` on the host.

```spin2
debug(`Spectrum CLEAR)
debug(`Spectrum SAVE 'spectrum')        ' writes spectrum.bmp
```

## Packing samples

For low-resolution data you can reduce the serial traffic by packing several
samples into each transmitted value. Add one packing keyword to the creation
line; the window then unpacks each value it receives into multiple samples. The
formats name the container size and the bits per sample:

`LONGS_1BIT`, `LONGS_2BIT`, `LONGS_4BIT`, `LONGS_8BIT`, `LONGS_16BIT`,
`WORDS_1BIT`, `WORDS_2BIT`, `WORDS_4BIT`, `WORDS_8BIT`,
`BYTES_1BIT`, `BYTES_2BIT`, `BYTES_4BIT`.

For example, `LONGS_8BIT` unpacks each long you send into four 8-bit samples.
Packing is most useful for the LOGIC and SCOPE windows where samples are
naturally narrow; for full-range FFT input it is rarely needed.

## A complete example: a multi-tone spectrum, no hardware

This program needs nothing but a P2 board and the host. It synthesizes a signal
in software — three sine tones summed, plus a little noise — and feeds it to the
FFT window so you can see the three tones as three spikes and the noise as a low
floor beneath them.

The tones come from the CORDIC `qsin` operator. Each tone has its own phase
accumulator; adding a fixed increment to a phase each sample sets that tone's
frequency, and the size of the increment relative to a full `$1_0000_0000` turn
fixes which bin the spike lands in.

```spin2
CON
  _clkfreq = 180_000_000

  N        = 1024                      ' FFT size (power of 2, 4..2048)

PUB main() | p1, p2, p3, s

  ' Create a 512x256 FFT window, 1024-point transform, log amplitude.
  debug(`FFT Spectrum SIZE 512 256 SAMPLES 1024 LOGSCALE)

  ' One channel: label, MAG=0, full scale, 256 tall, baseline 0,
  ' baseline grid line, drawn green.
  debug(`Spectrum 'Signal' 0 $7FFF_FFFF 256 0 1 $00FF00)

  p1 := 0                              ' phase accumulators
  p2 := 0
  p3 := 0
  repeat
    repeat N                           ' one full FFT buffer per pass
      s :=  qsin(20000, p1, $1_0000)   ' tone 1
      s += qsin(12000, p2, $1_0000)   ' tone 2
      s += qsin( 6000, p3, $1_0000)   ' tone 3
      s += (getrnd() & $FFF) - $800    ' +/- noise
      debug(`Spectrum `(s))            ' feed one sample

      p1 += $0080_0000                 ' lowest tone
      p2 += $0140_0000                 ' middle tone
      p3 += $0300_0000                 ' highest tone
    waitms(20)
```

`qsin(length, angle, twopi)` returns a CORDIC sine: `length` is the amplitude,
`angle` is the current phase, and `twopi` is the value that represents one full
turn — here `$1_0000`, so the phase wraps every 65,536 counts. Summing three of
them, scaling the noise down with a mask, and feeding the result one sample at a
time produces a spectrum with three clear peaks at the three increment-determined
bins.

The bin each tone lands in is set by its phase increment: a larger increment
advances the phase faster, which is a higher frequency, which is a higher bin.
Change an increment and watch the corresponding spike slide along the axis.

> **Extension (real hardware).** To analyze a real signal instead of a synthetic
> one, read an ADC-configured smart pin in the sample loop and feed its value in
> place of the `qsin` sum. Everything else — the window, the channel, the
> redraw — stays the same.

## Considerations

- **The window is fixed; there is no choice of window function.** Every transform
  is Hanning-windowed internally. Do not look for a `WINDOW` keyword or alternate
  window types — there are none.
- **Amplitude is arbitrary units, not dB.** `LOGSCALE` is a log2 compression with
  power-of-2 markers, and `MAG` is a power-of-2 gain. Neither produces decibels.
- **The frequency axis is yours to compute.** The window plots bins, not Hertz.
  Bin `k` is at `k x sample_rate / N`; if you want Hz labels, you add them.
- **One FFT per channel per redraw.** Each channel runs its own transform, so
  spectra for several channels cost proportionally more work per frame; use
  `RATE` to redraw less often when feeding many channels or large `N`.
- **Collect a full block before the first spectrum appears.** The window waits
  until it has `N` samples before drawing, so there is a brief fill delay at
  startup and after `` `CLEAR ``.
- **Pick `N` for the resolution you need.** Larger `N` gives finer bin spacing
  (better frequency resolution) at the cost of a longer block to fill and more
  work per transform. The maximum is **2048**.

## When to use FFT

- **FFT** — you care about *which frequencies* are present: tones, harmonics,
  resonances, noise floor.
- **SCOPE** (Chapter 8) — you care about the *waveform over time*: shape, timing,
  transients.
- **SPECTRO** (Chapter 10) — you care about *how the spectrum changes over time*:
  a scrolling waterfall built from the same FFT, one column per transform.

FFT and SPECTRO share the same transform and the same `SAMPLES`/`MAG`/range
configuration; FFT shows the current spectrum as a graph, SPECTRO shows a history
of spectra as a color-coded waterfall.

## Try it

Start with the multi-tone example above. Then:

1. Change one phase increment and watch its spike move; double an increment and
   confirm the spike lands roughly twice as far along the axis.
2. Add `SAMPLES 1024 0 200` to zoom into the low end where your tones sit, and
   see them spread across the full width.
3. Declare a second channel with a different color and baseline, feed it a single
   pure tone, and compare the clean spike against the noisy three-tone trace.
4. Toggle `LOGSCALE` off and on to see the noise floor rise into view under log
   scaling, then raise `MAG` on the channel to lift weak content further.

You will have used creation config, the `SAMPLES` size and bin range, a channel
declaration with color and grid, and both amplitude controls together — a
complete software-only spectrum analyzer in a few dozen lines.
