# Chapter 6: The LOGIC Window — Digital Waveforms {#ch-6}

The LOGIC window is a digital-waveform visualizer. You send it sample values; it
renders the individual bits of those samples as stacked logic traces, the way a
hardware logic analyzer draws its channels. Each channel is one bit (or, in range
mode, a small field of bits) of every sample, plotted left to right across a fixed
time base.

The window shows raw logic levels and nothing more. It has **no protocol
decoding** — there is no `DECODE` keyword and no built-in I2C, SPI, UART, CAN, or
USB interpreter. If you want a byte value or a decoded transaction, your own
Spin2/PASM2 code computes it; the LOGIC window only displays the lines. This is the
single most important thing to keep in mind about the window, and this chapter
returns to it in the worked example and the considerations.

You create one LOGIC window per `` DEBUG(`LOGIC ...) `` declaration, naming it and
declaring its channels in that one statement, then feed it sample values by name.

> Keyboard and mouse input (`PC_KEY`, `PC_MOUSE`) work in the LOGIC window, but they
> share one mechanism across every window type and are covered in [Chapter 12](#ch-12). Packed
> data formats are shared across the instrument windows and are detailed in
> [Chapter 13](#ch-13); this chapter shows how LOGIC uses them.

```{=latex}
\begin{figure}[H]
\centering
\screenshotfig[width=0.95\linewidth]{inbox/assets/fig-06-logic.png}
\caption{The LOGIC window showing eight channels of a binary ripple counter.}
\end{figure}
```

## Creating a LOGIC window and declaring channels

You create the window, set its display options, and declare its channels in a single
`DEBUG` statement. The first token after the backtick is the window type (`LOGIC`);
the second is a name you choose. Channels are declared as **string and value
elements inside the same statement** — a quoted label, optionally followed by a
count, the `RANGE` keyword, and a color. There are no `CHANNELS`, `LABELS`, or
`COLORS` keywords; the labels, counts, and colors *are* the channel declaration.

```spin2
PUB main() | sample
  ' create + declare 4 channels
  debug(`LOGIC Bus SAMPLES 64 'CLK' $00FF00 'DATA' $FFFF00 'CS' 'WR')
  debug(`Bus `(sample))  ' feed it by name
```

That line creates a window named `Bus` with four single-bit channels: `CLK`
(green), `DATA` (yellow), and `CS` and `WR` (default cycling colors). Channel 0 is
the first declared label, channel 1 the second, and so on.

The configuration keywords you can add to the creation line:

| Keyword | Arguments | Default | Range | What it sets |
|---------|-----------|---------|-------|--------------|
| `TITLE` | `'text'` | `Logic` | — | The window's title-bar text |
| `POS` | `left top` | cascaded | screen px | Window position, in pixels |
| `SAMPLES` | `count` | `32` | 4–2047 | Horizontal resolution — samples shown across the width |
| `SPACING` | `pixels` | `8` | 1–32 | Horizontal pixels between samples |
| `RATE` | `divisor` | `1` | 1–2048 | Redraw once per `divisor` samples |
| `DOTSIZE` | `pixels` | `0` | 0–32 | Dot diameter at each sample (`0` = no dots) |
| `LINESIZE` | `pixels` | `3` | 1–32 | Waveform line thickness |
| `TEXTSIZE` | `points` | `10` | 6–200 | Channel-label font size |
| `COLOR` | `back grid` | black / gray | `$RRGGBB` | Background and grid colors |
| `HIDEXY` | — | shown | — | Hides the mouse-coordinate readout |
| `LONGS_1BIT` … `BYTES_4BIT` | — | unpacked | 12 modes | Sets the data-packing mode (see "Packed sample data") |

`SAMPLES` and `SPACING` together set the window width: width in pixels is
`SAMPLES x SPACING`. The default `SAMPLES 32 SPACING 8` gives a 256-pixel-wide
trace. Increasing `SAMPLES` shows more history; increasing `SPACING` stretches each
sample wider.

> The window holds **up to 32 channels** and a single shared **2048-sample**
> circular buffer. The buffer is shared across all channels — every sample you send
> is one 32-bit value whose bits are distributed to the channels — not 2048 samples
> per channel. `SAMPLES` controls how many of those buffered samples are drawn, up to
> 2047.

### Channel declaration syntax

Each channel element follows this form, with the optional parts in any of the
combinations shown below:

```debug-config
'label' {count} {RANGE} {color}
```

- **`'label'`** — the channel name, drawn to the left of its trace.
- **`count`** — a number declaring multiple channels at once.
- **`RANGE`** — makes the channel a multi-bit value drawn as an analog-style
  waveform instead of a single high/low line.
- **`color`** — an `$RRGGBB` waveform color. Omit it and channels cycle through eight
  built-in colors (lime, red, cyan, yellow, magenta, blue, orange, olive).

**One single-bit channel:**

```spin2
debug(`LOGIC L 'CLK')              ' one channel, bit 0, default lime
```

**Several single-bit channels from one label** — a count after the label expands to
that many consecutive single-bit channels, labeled `D 0`, `1`, `2`, …:

```spin2
debug(`LOGIC L 'D' 8)  ' 8 single-bit channels: D 0 .. D 7, bits 0..7
```

**A multi-bit range channel** — `RANGE` after a count makes a single channel that
many bits wide, drawn as a waveform whose height tracks the value:

```spin2
' one 8-bit channel, value 0..255 -> height
debug(`LOGIC L 'ADC' 8 RANGE $FF0000)
```

**A mix** — declare them in the order you want them stacked (channel 0 at the
bottom):

```spin2
debug(`LOGIC L 'CLK' 'COUNT' 8 RANGE $FF0000 'BUSY')
'                   bit0   bits 1..8 (8-bit range, red)  bit 9
```

If you declare no channels at all, the window defaults to all 32 channels, each a
single bit, labeled `0`–`31`.

## Sending sample data

Once the window exists, you feed it sample values by name. Each value you send is one
**sample** — a 32-bit number whose bits are distributed across the declared channels:
channel 0 takes the low bit (or low field, for a range channel), the next channel
takes the bits above it, and so on. You send the *value* with `` `() ``:

```spin2
debug(`Bus `(sample))              ' one sample; its bits feed the channels
```

For the four-channel `Bus` above (`CLK DATA CS WR`, all single-bit), a sample value
of `%1011` lights channel 0 (`CLK`) high, channel 1 (`DATA`) low, channel 2 (`CS`)
high, channel 3 (`WR`) high. You build that value in your own code — from a counter,
from `GETRND`, from port reads, or from a software-simulated signal — and the window
draws whatever bits you send.

A range channel reads a *field* of bits rather than one bit. An 8-bit `RANGE`
channel declared at the bottom of the stack reads bits 0–7 of each sample and maps
that 0–255 value to the channel's vertical height, producing a stepped analog-style
trace.

You can send several samples in one statement; each numeric element is one sample:

```spin2
debug(`Bus `(s0) `(s1) `(s2) `(s3))   ' four samples in one DEBUG call
```

### Packed sample data

Sending one 32-bit long per sample is the simplest form, but it spends four serial
bytes on every sample. When a sample needs only a few bits, a **packing mode** lets
you carry many samples in one transmitted value. You set the mode as a keyword on the
creation line; the window then unpacks each value you send into multiple samples.

| Mode | Bits per sample | Samples per value |
|------|-----------------|-------------------|
| `LONGS_1BIT` | 1 | 32 |
| `LONGS_2BIT` | 2 | 16 |
| `LONGS_4BIT` | 4 | 8 |
| `LONGS_8BIT` | 8 | 4 |
| `LONGS_16BIT` | 16 | 2 |
| `WORDS_1BIT` | 1 | 16 |
| `WORDS_2BIT` | 2 | 8 |
| `WORDS_4BIT` | 4 | 4 |
| `WORDS_8BIT` | 8 | 2 |
| `BYTES_1BIT` | 1 | 8 |
| `BYTES_2BIT` | 2 | 4 |
| `BYTES_4BIT` | 4 | 2 |

With `LONGS_4BIT`, for example, each long you send is unpacked into eight samples of
four bits each — sample 0 in bits 0–3, sample 1 in bits 4–7, and so on:

```spin2
PUB main() | packed, j
  debug(`LOGIC Packed SAMPLES 256 LONGS_4BIT 'CLK' 'MOSI' 'MISO' 'CS')
  repeat
    packed := 0
    repeat j from 0 to 7                 ' build 8 four-bit samples
      packed |= (getrnd() & $F) << (j << 2)
    debug(`Packed `(packed))             ' one value -> eight samples
```

Packing trades serial bandwidth for the work of assembling the value in your code.
The packing system is shared across the instrument windows and described in full in
[Chapter 13](#ch-13). The names are `LONGS_`, `WORDS_`, and `BYTES_` followed by the bit width
(`_1BIT`, `_2BIT`, `_4BIT`, `_8BIT`, `_16BIT`); there are no `PACK1`-style shortcuts
and no run-length or compression modes.

## Triggering

By default the window is **free-running**: every sample (after rate limiting)
redraws the trace. To stabilize the display on a repeating event, set a trigger. The
trigger watches a chosen set of channels for a specific bit pattern and aligns the
display to the moment that pattern is matched.

```debug-update
TRIGGER mask match {offset}
```

- **`mask`** — which channels participate, one bit per channel. `$1` watches channel
  0; `$3` watches channels 0 and 1; `0` disables the trigger (free-running).
- **`match`** — the bit values expected on the masked channels.
- **`offset`** — where the trigger event sits in the display, `0` to `SAMPLES-1`.
  `0` is the left edge (show what follows the event), `SAMPLES-1` is the right edge
  (show what led up to it), and the default is the center (`SAMPLES/2`).

The match test is `((sample XOR match) AND mask) = 0` — true when every masked bit
equals its expected value. The trigger is **edge-sensitive**: it first has to see a
sample that does *not* match (which arms it), then fires on the next sample that
*does* match. This prevents a steady, already-matching signal from re-triggering on
every sample.

```spin2
' fire when channel 0 (CLK) goes high, event at sample 32
debug(`Bus TRIGGER $1 $1 32)
' fire when ch0=1 and ch1=0, event 16 samples from left
debug(`Bus TRIGGER $3 $1 16)
debug(`Bus TRIGGER 0 0)            ' disable trigger (free-running)
```

You issue `TRIGGER` as a runtime command after the window exists; it is not a
creation-line keyword. The trigger only evaluates once the displayed window of
samples (the `SAMPLES` count) has filled.

### Holdoff

After a trigger fires, `HOLDOFF` suppresses further triggers for a number of samples,
so a busy or noisy signal does not re-trigger immediately:

```debug-update
HOLDOFF count
```

`count` ranges from 2 to 2048. After each trigger the window ignores trigger matches
for `count` samples, then re-arms.

```spin2
' after a trigger, skip 128 samples before re-arming
debug(`Bus HOLDOFF 128)
```

## Clearing and saving

Three runtime commands manage the display:

- `` `CLEAR `` — clears the trace, empties the sample buffer (`SamplePop` returns to
  zero), resets the trigger indicator, and resets the rate counter. The window starts
  collecting fresh samples from empty.
- `` `SAVE `` — saves the current window image to a `.bmp` file on the host.
- `` `CLOSE `` — closes this window and frees its resources.

```spin2
debug(`Bus CLEAR)                  ' empty the buffer and blank the trace
debug(`Bus SAVE)  ' write the current image to a bitmap file
```

## A complete software-only example

This program simulates an SPI master in Spin2 — no wiring, no probe — and shows its
three lines (`CS`, `CLK`, `MOSI`) on the LOGIC window. Each call to `emit` packs the
three logical levels into one sample (channel 0 = `CS`, channel 1 = `CLK`, channel 2
= `MOSI`) and sends it. The trigger aligns the display to the falling edge of `CS`,
the start of each frame.

The decoding — knowing that this *is* SPI, that data is sampled on the rising clock
edge, that the byte is `$A5` — lives entirely in this Spin2 code. The window shows
only the three waveforms; it does not know they are SPI.

```{.spin2 caption="ch06-logic-spi-bus.spin2"}
CON
  _clkfreq = 100_000_000

PUB main() | tx_byte, i, cs, clk, mosi
  debug(`LOGIC SPIbus TITLE 'Software SPI' SAMPLES 200 SPACING 3 ...
         'CS' $00FFFF 'CLK' $00FF00 'MOSI' $FFFF00)
  ' align display to CS going low (frame start)
  debug(`SPIbus TRIGGER $1 $0 32)

  tx_byte := $A5
  repeat
    ' idle: CS high, CLK low
    cs := 1
    clk := 0
    mosi := 0
    emit(cs, clk, mosi)
    emit(cs, clk, mosi)

    ' start frame: assert CS low
    cs := 0
    emit(cs, clk, mosi)

    ' clock out 8 bits, MSB first
    ' (mode 0: data set on low, sampled on rising edge)
    repeat i from 7 to 0
      mosi := (tx_byte >> i) & 1
      clk := 0
      emit(cs, clk, mosi)                    ' present data with clock low
      clk := 1
      emit(cs, clk, mosi)                    ' rising edge

    ' end frame: release CS
    clk := 0
    cs := 1
    emit(cs, clk, mosi)

    tx_byte := (tx_byte + 1) & $FF           ' next byte

PRI emit(cs, clk, mosi) | s
  ' pack 3 lines into bits 0,1,2 of one sample
  s := cs | (clk << 1) | (mosi << 2)
  debug(`SPIbus `(s))
```

Run it and the window shows `CS` framing each byte, eight clock pulses per frame, and
`MOSI` carrying the bit pattern of `$A5`, `$A6`, `$A7`, … Because the trigger is set
on `CS` low, every frame redraws in the same horizontal position and the display
holds steady. To watch a multi-bit value instead, declare a `RANGE` channel and send
the byte value directly:

```spin2
debug(`LOGIC Counter SAMPLES 256 'BYTE' 8 RANGE $00FF00)
repeat
  ' 8-bit ramp drawn as an analog-style trace
  debug(`Counter `(value++ & $FF))
```

## Acquisition: software-paced sampling and transition capture

The LOGIC window sits comfortably inside the link budget ([Chapter 1](#ch-1)),
because digital debugging rarely needs a continuous full-rate stream. Two
logic-specific habits keep it that way.

**Software-paced — one sample per event.** You do not have to sample a bus on
every system-clock tick. The SPI example above sends one sample each time a line
*changes* — idle, CS low, each clock edge — not one per clock cycle. Driving the
window from your protocol's own events, rather than a free-running sample clock,
is what keeps a bring-up trace small enough to stream live: a few hundred samples
frame an entire transaction.

**Transition + timestamp capture.** When you do need to record a fast bus, store
*transitions*, not samples. Each time a watched line changes, capture the new
line state together with a timestamp (from `GETCT` or a free-running counter) and
keep only those pairs. An idle bus then costs nothing while idle and a single
entry per edge when it moves — far less than one sample per clock. The pairs pack
tightly ([Chapter 13](#ch-13)), and you reconstruct the timing from the
timestamps on the host. This is how a logic analyzer records minutes of a sparse
bus without a giant buffer.

The mechanics underneath a fast capture — a circular buffer filled in a tight PASM
loop, an arm/trigger/freeze cycle, dumping one frozen frame over the slow link —
are shared with SCOPE; the acquisition section of [Chapter 7](#ch-7) develops them
once. LOGIC's trigger (above) arms and fires on a bit pattern the same way.

### Where you'd use this

In computer science and computer engineering, the LOGIC window is the tool for
**protocol engineering** — bringing up and verifying a serial bus — and for
**debugging concurrent systems**, where what matters is the *timing relationship*
between several digital signals.

**On an embedded project**, you reach for it during bit-banged-driver bring-up
(does the clock idle in the right state, is data sampled on the correct edge —
CPOL/CPHA), to check chip-select and bus-arbitration timing, to watch inter-cog
signalling and lock hand-offs, and to confirm setup-and-hold against a datasheet's
timing diagram.

**Bandwidth fit:** software-paced traces and buffered bursts stream comfortably;
continuously monitoring a *fast* live bus does not fit, and is the case the
capture strategies above exist to handle.

**Extension (real hardware):** replace the simulated lines with real pin reads —
sample the actual port bits into each sample value — and the same channels,
trigger, and decode-in-code approach shows a live bus.

## Considerations

- **The window shows waveforms; you decode in code.** LOGIC renders logic levels. Any
  interpretation — framing, byte values, protocol state — is computed by your Spin2
  or PASM2 code before you send the sample. There is no decoder keyword. Treat the
  window as the lines on a logic analyzer's screen, not as a protocol analyzer.
- **One sample is one 32-bit value, distributed across channels.** Build the value so
  each channel's bit (or field) lands at the right offset: channel 0 at bit 0, the
  next channel at the bits above it. A range channel consumes a contiguous field.
- **The buffer is 2048 samples, shared, circular.** `SAMPLES` chooses how many are
  drawn (4–2047) — and only that many are ever marked valid, so the trigger
  evaluates and displays within the `SAMPLES` window, not the full 2048-deep buffer.
- **Trigger fires on an edge, not a level.** It must first see a non-matching sample,
  then a matching one. A signal already sitting at the match value will not trigger
  until it leaves and returns. Use `HOLDOFF` to keep a busy signal from
  re-triggering.
- **Pack when bandwidth matters.** One long per sample is simplest; the `LONGS_`/
  `WORDS_`/`BYTES_` packing modes carry many narrow samples per transmitted value at
  the cost of assembling that value in your code ([Chapter 13](#ch-13)).
- **`RATE` thins redraws, not samples.** A high `RATE` divisor reduces how often the
  trace repaints, lowering host load, while every sample still enters the buffer.
- **LOGIC vs. SCOPE.** Use LOGIC for discrete digital lines and bit patterns; use
  SCOPE ([Chapter 7](#ch-7)) for a continuously varying analog value over time. A `RANGE`
  channel bridges the two when you want a small multi-bit value shown as a stepped
  waveform alongside digital lines.

> See also: [Chapter 7](#ch-7) (SCOPE) for analog time-domain traces, [Chapter 12](#ch-12) for `PC_KEY`
> and `PC_MOUSE` input, and [Chapter 13](#ch-13) for the shared packed-data formats.

## Try it

Start with the SPI example above. Then: add a fourth channel `MISO` and have the
simulated peripheral drive a reply byte back on it (compute the bits in code — the
window still only shows the lines). Next, switch `CS`/`CLK`/`MOSI`/`MISO` to a
packed feed using `LONGS_4BIT`, building each long from eight four-bit samples, and
confirm the same waveforms appear with a quarter of the serial traffic. Finally,
add an 8-bit `RANGE` channel that shows the byte value your code has assembled, so
you can watch the decoded byte rise and fall beside the raw lines — proof that the
decoding is yours and the display is just the waveforms.
