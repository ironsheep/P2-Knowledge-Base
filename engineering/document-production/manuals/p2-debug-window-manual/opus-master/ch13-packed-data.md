# Chapter 13: Packed Data — Compact High-Rate Transfers {#ch-13}

Every element you send to a window travels over the `DEBUG()` serial link. That
link is finite. The P2 transmits debug output on pin P62 in 8-N-1 format at the
rate set by the `DEBUG_BAUD` symbol, which defaults to `DOWNLOAD_BAUD` — **2 Mbaud**.
`pnut_term_ts` runs at 2 Mbaud, so keep the link there: set `DEBUG_BAUD`
explicitly only if you have changed `DOWNLOAD_BAUD` or your clock requires it, and
do not drop the DEBUG link to a slow rate such as 115200 — debugging needs the
bandwidth. (If you drive the windows from the Spin Tools IDE, confirm it runs at
2 Mbaud.) When your data is *small* — single bits from a logic capture, 8-bit
samples from a scope trace — sending one value per element wastes the link: a
1-bit sample carried as a full long spends 32 bits of wire to convey one bit of
information.

Packed-data modes fix that. You pack many small values into a byte, word, or long
on the P2 side, send the container as a single element, and the host **unpacks** it
back into the individual values. A single `DEBUG` element can then carry as many
as 32 samples instead of one. The instrument windows — LOGIC, SCOPE, SCOPE_XY,
FFT, SPECTRO, and BITMAP — all read the same packed formats, so the same technique
raises the effective sample rate of every one of them.

This chapter documents the complete set of packed-data modes, how to feed them, and
how to choose one for your data.

## Why packing helps

The `DEBUG()` link carries every element you send one after another over the serial
connection, so the rate at which you can feed a window is bounded by that link. A
high-rate capture — a logic-analyzer trace, a fast scope sweep — generates samples
faster than one-element-per-sample transmission can keep up with.

Packing trades a little P2-side work for a large reduction in element count. If you
have 32 one-bit logic samples, you can shift them into a single long and send that
long as one element. The host unpacks it into 32 separate samples. One element of
link traffic now carries what would otherwise have been 32 — a 32× reduction in the
number of elements crossing the link for that data.

The savings scale with how much smaller your data is than its container. The denser
the packing, the fewer elements you send for the same number of samples.

## The packed-data modes

A packed-data mode is named by a **container** (the unit you send — `LONGS_`,
`WORDS_`, or `BYTES_`) and a **bit width** (how many bits each unpacked value
occupies inside that container). The host divides the container by the bit width to
get the count of values it unpacks from each element.

There are **12 modes**. The maximum compression is **32×**, with `LONGS_1BIT`.

| Mode | Container bits | Bits per value | Values per element | Compression |
|------|---------------|----------------|--------------------|-------------|
| `LONGS_1BIT`  | 32 | 1  | 32 | 32× |
| `LONGS_2BIT`  | 32 | 2  | 16 | 16× |
| `LONGS_4BIT`  | 32 | 4  | 8  | 8×  |
| `LONGS_8BIT`  | 32 | 8  | 4  | 4×  |
| `LONGS_16BIT` | 32 | 16 | 2  | 2×  |
| `WORDS_1BIT`  | 16 | 1  | 16 | 16× |
| `WORDS_2BIT`  | 16 | 2  | 8  | 8×  |
| `WORDS_4BIT`  | 16 | 4  | 4  | 4×  |
| `WORDS_8BIT`  | 16 | 8  | 2  | 2×  |
| `BYTES_1BIT`  | 8  | 1  | 8  | 8×  |
| `BYTES_2BIT`  | 8  | 2  | 4  | 4×  |
| `BYTES_4BIT`  | 8  | 4  | 2  | 2×  |

Each value is extracted **starting from the LSB** of the element. For
`LONGS_1BIT`, bit 0 is the first unpacked value, bit 1 the second, and so on up to
bit 31. For `LONGS_8BIT`, the low byte is the first value, the next byte the
second, and so on. The unpacked ranges are:

| Bits per value | Unpacked range | Range if `SIGNED` |
|----------------|----------------|-------------------|
| 1  | 0..1      | -1..0            |
| 2  | 0..3      | -2..1            |
| 4  | 0..15     | -8..7            |
| 8  | 0..255    | -128..127        |
| 16 | 0..65,535 | -32,768..32,767  |

### The ALT and SIGNED modifiers

A mode keyword may be followed by either or both of two optional keywords:

- **`SIGNED`** — the host sign-extends each unpacked value. Without it, values are
  unsigned (the left column above); with it, they take the right column's signed
  range. Use it when your packed fields represent signed quantities.
- **`ALT`** — **within each byte sent**, the host reorders the sub-units (the bits,
  double-bits, or nibbles set by the mode's field width) **end-to-end** — a per-byte
  reversal of sub-unit order, applied independently to each byte of the element. This
  helps when your source data has its sub-field order swapped from what the display
  expects — most often bitmap data composed in a standard pixel format.

```spin2
' two signed 16-bit values per long
debug(`SCOPE Sig SIZE 256 128 LONGS_16BIT SIGNED)
debug(`Sig 'val')
```

## How to send packed data

Packing is set on the window's creation line — you add the mode keyword to the same
`DEBUG` statement that declares the window. From then on, every element you feed
that window is treated as a packed container and unpacked according to the mode.
You do the packing on the P2 side; the host does the unpacking.

This example feeds a single-channel LOGIC window with `LONGS_1BIT`. Each long carries
32 one-bit samples; the host unpacks them LSB-first and applies them to the channel
in turn, so one long becomes 32 successive samples of `D0`. The data is generated in
software with the random-number generator, so it runs on a bare board with no wiring:

```{.spin2 caption="ch13-packed-logic-stream.spin2"}
CON _clkfreq = 200_000_000

VAR long buff[8]                              ' 8 longs x 32 samples = 256 = one full window

PUB main() | i, j, packed
  debug(`LOGIC Stream SAMPLES 256 'D0' LONGS_1BIT)
  repeat
    repeat j from 0 to 7                       ' build one window of packed samples
      packed := 0
      repeat i from 0 to 31
        ' pack 32 one-bit samples into a long
        packed := (packed << 1) | (getrnd() & 1)
      buff[j] := packed
    ' feed the whole window in one message; the host unpacks each long into
    ' 32 samples LSB-first (packed data is streamed as an array, not one long
    ' per DEBUG call)
    debug(`Stream `uhex_long_array_(@buff, 8))
    waitms(50)
```

The packing loop builds the long bit by bit. You can build it any way you like —
from a streamer capture in hub RAM, from CORDIC results, from a shift register —
as long as the bits you want unpacked first land in the low end of the element.

Stream the packed longs as an **array** — one full window's worth per message,
using `` `uhex_long_array_(@buff, count) `` — rather than one long per `DEBUG`
call. Packed data is delivered as a batch the host unpacks in one pass; a full
window per frame is the pattern the Spin2 documentation uses for packed capture.

Packing is not tied to one channel — it is a **fixed bit budget** you choose how to
spend. Every `LONGS_` mode delivers the same 32 bits per element: `LONGS_1BIT` as
32 one-bit values, `LONGS_2BIT` as 16 two-bit values, `LONGS_4BIT` as 8 four-bit
values. You spend that budget on **time** — one channel, the most samples per long,
as above — or across **channels**, several signals carried at once. Declaring two
channels and packing with `LONGS_2BIT` sends a *pair* of one-bit logic channels
(`D0` in bit 0, `D1` in bit 1), sixteen sample-pairs to a long — the same 32-bit
budget split two ways instead of one:

```{.spin2 caption="ch13-packed-logic-multi.spin2"}
CON _clkfreq = 200_000_000

VAR long buff[16]                            ' 16 longs x 16 sample-pairs = 256 = one full window

PUB main() | i, j, packed
  debug(`LOGIC Pair SAMPLES 256 'D0' 'D1' LONGS_2BIT)
  repeat
    repeat j from 0 to 15                      ' build one window of packed sample-pairs
      packed := 0
      repeat i from 0 to 15
        ' pack 16 two-bit samples into a long: bit 0 -> D0, bit 1 -> D1
        packed := (packed << 2) | (getrnd() & %11)
      buff[j] := packed
    ' feed the whole window in one message; the host unpacks each long into
    ' 16 two-bit samples (one bit per channel), streamed as an array -- not one
    ' long per DEBUG call
    debug(`Pair `uhex_long_array_(@buff, 16))
    waitms(50)
```

Same packing mechanism, same array feed — only the channel count and the mode's
bit width changed. That is the whole point: high-density capture serves a single
channel and many channels equally.

A scope works the same way. Here four 8-bit samples ride in each long under
`LONGS_8BIT`, packed low byte first:

```{.spin2 caption="ch13-packed-scope.spin2"}
CON _clkfreq = 200_000_000

VAR long buff[128]                           ' 128 longs x 4 values = 512 = 256 sample-sets (A,B)

PUB main() | i, ch
  debug(`SCOPE Sig SIZE 256 128 LONGS_8BIT)   ' create with config only
  debug(`Sig 'A' 0 255 'B' 0 255)             ' channel-defs (each needs a range) as a separate feed
  ch := 0
  repeat
    repeat i from 0 to 127
      ' four 8-bit values per long, low byte first
      buff[i] := (ch++ & $FF) | ((ch++ & $FF) << 8) | ((ch++ & $FF) << 16) | ((ch++ & $FF) << 24)
    ' feed the whole window in one message; the host unpacks each long into
    ' four 8-bit values (packed data is streamed as an array, not one long
    ' per DEBUG call)
    debug(`Sig `uhex_long_array_(@buff, 128))
    waitms(20)
```

A BITMAP window unpacks the same formats into pixels. With a `LUT2` (two-bit) color
mode you would pack with `LONGS_2BIT`; with a one-bit source you can drive a
two-color image using `LUT1` with `LONGS_1BIT`, sending one long per 32-pixel
row segment:

```{.spin2 caption="ch13-packed-bitmap-frame.spin2"}
CON _clkfreq = 200_000_000

PUB main() | row, x, packed, bit
  debug(`BITMAP Frame SIZE 32 16 DOTSIZE 8 LUT1 LONGS_1BIT)   ' 1-bit pixels -> LUT1 (2-color)
  debug(`Frame LUTCOLORS $000000 $00FFFF)                     ' index 0 = background, 1 = cyan
  repeat
    repeat row from 0 to 15
      packed := 0
      repeat x from 0 to 31
        bit := (((x + row) & 3) == 0) & 1  ' a diagonal stripe pattern
        packed := packed | (bit << x)
      debug(`Frame `(packed))  ' one long = 32 pixels of one row
    waitms(200)
```

## Choosing a format

Match the bit width to the size of your values, then pick the container that holds
the most of them.

1. **Match the bit width to your data.** One-bit logic channels → a `_1BIT` mode.
   Values that fit in a nibble (0–15, or −8..7 signed) → a `_4BIT` mode. Byte-sized
   samples → an `_8BIT` mode. Don't pad small values into a wider field; that
   throws away the compression.
2. **Pick the widest container you can fill.** For a given bit width, `LONGS_`
   packs the most values per element, then `WORDS_`, then `BYTES_`. Use `LONGS_`
   unless your data naturally arrives as words or bytes and repacking into longs
   would cost more than it saves.
3. **Add `SIGNED` if the values are signed**, and `ALT` only if your sub-byte field
   order is swapped relative to the display.

So a single-bit logic capture at the highest rate uses `LONGS_1BIT` (32×). A scope
sampling a signed 16-bit ADC-style value uses `LONGS_16BIT SIGNED` (2×). A
four-level (2-bit) bitmap uses `LONGS_2BIT` (16×).

### Where you'd use this

Packing is not a window; it is the **headroom mechanism** the rest of the manual
leans on. You reach for it the moment a window cannot keep up with the data — when
a fast sample stream would saturate the 2 Mbaud link ([Chapter 1](#ch-1)).

The concrete case is a **high-rate burst** you have captured in a tight PASM loop —
a triggered scope frame, a logic-analyzer capture, a block destined for the FFT —
and now have to move over the slow link. Sending one long per sample wastes three
or more bytes on values only a few bits wide; packing them (up to 32 samples per
long) is what lets the dump fit. This is the readout half of the **capture-and-dump**
strategy ([Chapter 7](#ch-7)): capture fast, pack tight, dump once.

**Bandwidth fit:** packing multiplies how much *fits*, not how fast the link runs —
it buys headroom, not an order of magnitude. When even packed data outruns the
link, capture a finite burst and dump it rather than trying to stream live.

## Considerations

- **Maximum compression is 32×.** `LONGS_1BIT` is the densest mode. There is no
  format denser than one bit per value, and no run-length, delta, or general
  compression scheme — packing is fixed-width bit-field extraction, nothing more.
- **You pack; the host unpacks.** The mode keyword only tells the host how to take
  the element apart. Building the packed container correctly — right bit width, LSB
  first — is your code's responsibility.
- **LSB-first ordering is fixed.** The first unpacked value always comes from the
  low end of the element. Shift your first sample into the low bits. Use `ALT` only
  to reverse the order of the sub-units (bits, 2-bit pairs, or nibbles by mode width)
  end-to-end within each byte of the element — a per-byte sub-unit reversal, not a
  whole-element reversal.
- **Packing is per window, set at creation.** All elements fed to that window are
  unpacked the same way for its lifetime; there is no per-element mode switch.
- **Send whole multiples of the values-per-element count.** A `LONGS_1BIT` LOGIC
  feed advances 32 samples per element; size your buffers and `SAMPLES` count in
  multiples of the values-per-element so sets land on element boundaries.
- **The link is still the limit.** Packing reduces *element count*, not the link's
  raw rate. It is the lever you reach for when a window can't keep up — but the
  ceiling is still the 2 Mbaud debug link.

The windows that read packed data are LOGIC ([Chapter 6](#ch-6)), SCOPE ([Chapter 7](#ch-7)),
SCOPE_XY ([Chapter 8](#ch-8)), FFT ([Chapter 9](#ch-9)), SPECTRO ([Chapter 10](#ch-10)), and BITMAP
([Chapter 4](#ch-4)). Each chapter shows the mode keyword in its creation-line table; this
chapter is the shared reference for what those keywords mean.

## Try it

You have now seen the same two-bit element spent two ways — as one channel at maximum
time-resolution (`LONGS_1BIT`), and as two 1-bit channels (`LONGS_2BIT`). Spend it a
third way: keep `LONGS_2BIT`, but declare a **single** channel with a `0 3` range, so
each two-bit sample is one *value* (0..3) instead of two channel bits — now the same
mode draws a stepped 0..3 waveform on one channel. Then declare the window with
`SIGNED` and watch the same bit patterns reinterpret as −2..1. Finally, switch the
container from `LONGS_` to `WORDS_` and `BYTES_` for the same bit width and observe how
the values-per-element count — and therefore the number of elements you send per
screen — changes with the container size.
