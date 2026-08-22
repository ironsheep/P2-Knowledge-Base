# Appendix G: Streamer Mode Constants

PASM2 provides predefined constants for configuring the P2's streamer, a DMA-like engine that transfers data between hub RAM, LUT RAM, pins, and DAC outputs. These constants replace complex bit patterns with readable symbolic names.

## Streamer Overview

The streamer operates in conjunction with the FIFO and can:

- Transfer data from hub RAM to pins/DACs (playback)
- Transfer data from pins/ADCs to hub RAM (capture)
- Perform real-time data transformations (color conversion, bit manipulation)
- Generate video signals with automatic timing

Streamer commands are issued via XINIT, XCONT, and related instructions.



## Command Word Structure

Streamer commands are 32-bit values composed of mode selection and control fields:

```
Bits 31-28: Mode selector; bits 27-16: control/config fields
Bits 15-0:  Transfer count (NCO rollovers); NCO rate is set by SETXFRQ
```

The values shown below are the base constants that get combined with control flags using OR operations.

Two fields inside that control range apply to every mode and appear in none of the constants:

- **`D[22:20]` selects the pin group**, in 8-pin increments, for transfers of up to 32 pins; the selection wraps around. Every constant in this appendix leaves those bits zero, so every example below works on the group starting at pin 0. Streaming anywhere else means OR-ing the group number in.
- **`D[23]` is the pin-output or hub-write enable**, depending on the mode's direction. `X_PINS_ON` and `X_WRITE_ON` are its two names — see "Pin Output and Hub Write Control" below.



## Reading a Mode Constant Name

Every constant in this appendix encodes its own configuration. Read the name and you know what the mode does; the tables below say the same thing in words, and the `Value` column gives the bits.

```
X_[source][size]_[pins]P_[dacs]DAC[bits]_[dest]
```

| Component | Meaning |
|-----------|---------|
| X_ | Streamer constant prefix |
| IMM | Immediate data (the long supplied to XINIT) |
| RF | Read from FIFO — hub RAM out to pins/DACs |
| WF | Write to FIFO — pins/ADCs in to hub RAM |
| BYTE/WORD/LONG | Hub data unit size |
| 32X1 … 1X32 | Data width — how each transfer unit is split (see below) |
| _nP | Number of **pins** driven or sampled |
| _kDACb | **k DAC channels, b bits each** |
| LUT | Data passes through the LUT |

**`_kDACb` is the field that gets misread.** The first number is the channel *count*; the second is the *bit width per channel*. They are not two counts. So:

| Name | Pins | DAC channels | Bits per channel |
|------|:----:|:------------:|:----------------:|
| X_RFBYTE_8P_1DAC8 | 8 | 1 | 8 |
| X_RFBYTE_8P_2DAC4 | 8 | 2 | 4 |
| X_RFBYTE_8P_4DAC2 | 8 | 4 | 2 |

All three read a byte and drive eight pins. They differ only in how that byte is divided among DAC channels — one 8-bit channel, two 4-bit channels, or four 2-bit channels. The pin count comes from `_nP` alone. Where a name carries no `_nP` — the X_IMM_ family — the pin count is fixed by the mode and is stated in the table.

### Data Width

The 32X1-style field says how each transfer unit is split:

| Width | Meaning |
|------|---------|
| 32X1 | 32 single-bit values per transfer |
| 16X2 | 16 2-bit values per transfer |
| 8X4 | 8 4-bit (nibble) values per transfer |
| 4X8 | 4 8-bit (byte) values per transfer |
| 2X16 | 2 16-bit (word) values per transfer |
| 1X32 | 1 32-bit (long) value per transfer |



## Immediate to LUT to Pins/DACs

These modes stream immediate data through the LUT to output pins or DAC channels. **The width figure is the LUT index size, not the pin data.** Each n-bit field taken from the long indexes the LUT, and the LUT entry it selects is what reaches the pins — so a 1-bit field still drives the full pin group, it just chooses between two LUT entries. All four modes output to a 32-pin group.

| Constant | Value | Description |
|----------|-------|-------------|
| X_IMM_32X1_LUT | %0000_0000_0000_0000 << 16 | 32 one-bit LUT lookups per long |
| X_IMM_16X2_LUT | %0001_0000_0000_0000 << 16 | 16 two-bit LUT lookups per long |
| X_IMM_8X4_LUT | %0010_0000_0000_0000 << 16 | 8 four-bit LUT lookups per long |
| X_IMM_4X8_LUT | %0011_0000_0000_0000 << 16 | 4 eight-bit LUT lookups per long |



## Immediate to Pins/DACs (Direct)

These modes stream immediate data directly to pins and DAC channels.

| Constant | Value | Description |
|----------|-------|-------------|
| X_IMM_32X1_1DAC1 | %0100_0000_0000_0000 << 16 | 32×1 immediate: 1 pin + 1 DAC channel at 1 bit |
| X_IMM_16X2_2DAC1 | %0101_0000_0000_0000 << 16 | 16×2 immediate: 2 pins + 2 DAC channels at 1 bit |
| X_IMM_16X2_1DAC2 | %0101_0000_0000_0010 << 16 | 16×2 immediate: 2 pins + 1 DAC channel at 2 bits |
| X_IMM_8X4_4DAC1 | %0110_0000_0000_0000 << 16 | 8×4 immediate: 4 pins + 4 DAC channels at 1 bit |
| X_IMM_8X4_2DAC2 | %0110_0000_0000_0010 << 16 | 8×4 immediate: 4 pins + 2 DAC channels at 2 bits |
| X_IMM_8X4_1DAC4 | %0110_0000_0000_0100 << 16 | 8×4 immediate: 4 pins + 1 DAC channel at 4 bits |
| X_IMM_4X8_4DAC2 | %0110_0000_0000_0110 << 16 | 4×8 immediate: 8 pins + 4 DAC channels at 2 bits |
| X_IMM_4X8_2DAC4 | %0110_0000_0000_0111 << 16 | 4×8 immediate: 8 pins + 2 DAC channels at 4 bits |
| X_IMM_4X8_1DAC8 | %0110_0000_0000_1110 << 16 | 4×8 immediate: 8 pins + 1 DAC channel at 8 bits |
| X_IMM_2X16_4DAC4 | %0110_0000_0000_1111 << 16 | 2×16 immediate: 16 pins + 4 DAC channels at 4 bits |
| X_IMM_2X16_2DAC8 | %0111_0000_0000_0000 << 16 | 2×16 immediate: 16 pins + 2 DAC channels at 8 bits |
| X_IMM_1X32_4DAC8 | %0111_0000_0000_0001 << 16 | 1×32 immediate: 32 pins + 4 DAC channels at 8 bits |



## RDFAST to LUT to Pins/DACs

These modes read data from hub RAM via the RDFAST FIFO, index the LUT with it, and output to pins/DACs. The index-width rule is the same as above: the figure below is how many lookups each long yields, not how many pins are driven. All four output to a 32-pin group.

| Constant | Value | Description |
|----------|-------|-------------|
| X_RFLONG_32X1_LUT | %0111_0000_0000_0010 << 16 | Read long: 32 one-bit LUT lookups |
| X_RFLONG_16X2_LUT | %0111_0000_0000_0100 << 16 | Read long: 16 two-bit LUT lookups |
| X_RFLONG_8X4_LUT | %0111_0000_0000_0110 << 16 | Read long: 8 four-bit LUT lookups |
| X_RFLONG_4X8_LUT | %0111_0000_0000_1000 << 16 | Read long: 4 eight-bit LUT lookups |



## RDFAST Byte Operations

These modes read bytes from hub RAM and output to pins/DACs with various configurations.

| Constant | Value | Description |
|----------|-------|-------------|
| X_RFBYTE_1P_1DAC1 | %1000_0000_0000_0000 << 16 | Read byte: 1 pin + 1 DAC channel at 1 bit |
| X_RFBYTE_2P_2DAC1 | %1001_0000_0000_0000 << 16 | Read byte: 2 pins + 2 DAC channels at 1 bit |
| X_RFBYTE_2P_1DAC2 | %1001_0000_0000_0010 << 16 | Read byte: 2 pins + 1 DAC channel at 2 bits |
| X_RFBYTE_4P_4DAC1 | %1010_0000_0000_0000 << 16 | Read byte: 4 pins + 4 DAC channels at 1 bit |
| X_RFBYTE_4P_2DAC2 | %1010_0000_0000_0010 << 16 | Read byte: 4 pins + 2 DAC channels at 2 bits |
| X_RFBYTE_4P_1DAC4 | %1010_0000_0000_0100 << 16 | Read byte: 4 pins + 1 DAC channel at 4 bits |
| X_RFBYTE_8P_4DAC2 | %1010_0000_0000_0110 << 16 | Read byte: 8 pins + 4 DAC channels at 2 bits |
| X_RFBYTE_8P_2DAC4 | %1010_0000_0000_0111 << 16 | Read byte: 8 pins + 2 DAC channels at 4 bits |
| X_RFBYTE_8P_1DAC8 | %1010_0000_0000_1110 << 16 | Read byte: 8 pins + 1 DAC channel at 8 bits |



## RDFAST Word/Long Operations

These modes read words or longs from hub RAM for higher bandwidth applications.

| Constant | Value | Description |
|----------|-------|-------------|
| X_RFWORD_16P_4DAC4 | %1010_0000_0000_1111 << 16 | Read word: 16 pins + 4 DAC channels at 4 bits |
| X_RFWORD_16P_2DAC8 | %1011_0000_0000_0000 << 16 | Read word: 16 pins + 2 DAC channels at 8 bits |
| X_RFLONG_32P_4DAC8 | %1011_0000_0000_0001 << 16 | Read long: 32 pins + 4 DAC channels at 8 bits |



## Video and Color Modes

These modes perform color space conversion for video generation. All five expand the hub data into the same 32-bit output word, `%rrrrrrrr_gggggggg_bbbbbbbb_00000000` — so all five carry **24 bits of color** across a 32-pin group, and place the same red, green and blue bytes on DAC channels X3, X2 and X1, with X0 receiving zero. They differ only in how the hub data is expanded into those three bytes.

**LUMA8 and RGBI8 look alike and take their color from opposite places.** Both spend 8 bits per pixel, and both give one color at varying brightness. LUMA8 takes the color from the streamer command's S operand and spends all 8 pixel bits on luminance — one color at 256 levels. RGBI8 takes the color from the pixel itself, spending its top 3 bits on the color select and the remaining 5 on intensity — 8 colors at 32 levels each. Neither carries separate red, green and blue fields.

| Constant | Value | Description |
|----------|-------|-------------|
| X_RFBYTE_LUMA8 | %1011_0000_0000_0010 << 16 | Read byte as luminance; the color is selected by S[2:0] |
| X_RFBYTE_RGBI8 | %1011_0000_0000_0011 << 16 | Read byte as color + intensity: P[7:5] selects the color, P[4:0] is the intensity |
| X_RFBYTE_RGB8 | %1011_0000_0000_0100 << 16 | Read byte as RGB 3:3:2 (256 colors) |
| X_RFWORD_RGB16 | %1011_0000_0000_0101 << 16 | Read word as RGB 5:6:5 (65,536 colors) |
| X_RFLONG_RGB24 | %1011_0000_0000_0110 << 16 | Read long as RGB 8:8:8 (16.7M colors) |



## WRFAST Operations (Capture)

These modes capture data from pins/ADCs and write to hub RAM via WRFAST FIFO.

| Constant | Value | Description |
|----------|-------|-------------|
| X_1P_1DAC1_WFBYTE | %1100_0000_0000_0000 << 16 | Capture 1 pin → 1 DAC channel at 1 bit, byte to hub |
| X_2P_2DAC1_WFBYTE | %1101_0000_0000_0000 << 16 | Capture 2 pins → 2 DAC channels at 1 bit, byte to hub |
| X_2P_1DAC2_WFBYTE | %1101_0000_0000_0010 << 16 | Capture 2 pins → 1 DAC channel at 2 bits, byte to hub |
| X_4P_4DAC1_WFBYTE | %1110_0000_0000_0000 << 16 | Capture 4 pins → 4 DAC channels at 1 bit, byte to hub |
| X_4P_2DAC2_WFBYTE | %1110_0000_0000_0010 << 16 | Capture 4 pins → 2 DAC channels at 2 bits, byte to hub |
| X_4P_1DAC4_WFBYTE | %1110_0000_0000_0100 << 16 | Capture 4 pins → 1 DAC channel at 4 bits, byte to hub |
| X_8P_4DAC2_WFBYTE | %1110_0000_0000_0110 << 16 | Capture 8 pins → 4 DAC channels at 2 bits, byte to hub |
| X_8P_2DAC4_WFBYTE | %1110_0000_0000_0111 << 16 | Capture 8 pins → 2 DAC channels at 4 bits, byte to hub |
| X_8P_1DAC8_WFBYTE | %1110_0000_0000_1110 << 16 | Capture 8 pins → 1 DAC channel at 8 bits, byte to hub |
| X_16P_4DAC4_WFWORD | %1110_0000_0000_1111 << 16 | Capture 16 pins → 4 DAC channels at 4 bits, word to hub |
| X_16P_2DAC8_WFWORD | %1111_0000_0000_0000 << 16 | Capture 16 pins → 2 DAC channels at 8 bits, word to hub |
| X_32P_4DAC8_WFLONG | %1111_0000_0000_0001 << 16 | Capture 32 pins → 4 DAC channels at 8 bits, long to hub |



## ADC Sampling Modes

These modes capture ADC samples and optionally write to hub RAM. These
constant names are the longest in the appendix, so the shared `<< 16` shift is
stated here once rather than repeated in every row: each constant equals the
mode field below shifted left 16 bits.

**Two setup steps come before any of these constants will do anything.** The streamer reads the four 8-bit SCOPE channels, and neither the block they come from nor the pins' analog mode is part of the mode word:

- `SETSCP` selects the block of four pins that feeds the four SCOPE channels.
- Each pin in that block used as an ADC8 input must be put into "ADC sample" or "ADC scope" smart pin mode, and enabled.

Which channel of that block is captured comes from the `S` operand, not from `D`: `S[1:0]` selects the channel for the 1-ADC8 modes, `S[1]` picks the upper or lower pair for the 2-ADC8 modes, and the 4-ADC8 mode captures all four. For the modes that also capture pin data, `D[22:20]` selects the 32-pin group whose lower 8 or 16 pins are recorded.

| Constant | Value | Description |
|----------|-------|-------------|
| X_1ADC8_0P_1DAC8_WFBYTE | %1111_0000_0000_0010 | 1 ADC to 8-bit, 0 pins, 1 DAC, write byte |
| X_1ADC8_8P_2DAC8_WFWORD | %1111_0000_0000_0011 | 1 ADC to 8-bit, 8 pins, 2 DACs, write word |
| X_2ADC8_0P_2DAC8_WFWORD | %1111_0000_0000_0100 | 2 ADCs to 8-bit, 0 pins, 2 DACs, write word |
| X_2ADC8_16P_4DAC8_WFLONG | %1111_0000_0000_0101 | 2 ADCs to 8-bit, 16 pins, 4 DACs, write long |
| X_4ADC8_0P_4DAC8_WFLONG | %1111_0000_0000_0110 | 4 ADCs to 8-bit, 0 pins, 4 DACs, write long |



## DDS and Goertzel Modes

These modes perform digital signal processing operations — direct digital synthesis on up to four DAC channels, Goertzel analysis on up to four ADC bit streams, or both at once.

The four-pin input block is selected by `D[22:19]`, a 4-bit block number whose base pin is that number times four. Both constants below leave the field zero, which selects pins 0–3; reaching any other block means OR-ing the block number into those bits yourself. One to four pins in the block should be configured for ADC mode **with no smart pin mode selected**, so their IN signals are raw delta-sigma bit streams.

That is the opposite of what the ADC sampling modes above require, and the two are easy to confuse: those need `SETSCP` plus an ADC smart pin mode, while these need the block number in the mode word and no smart pin mode at all.

| Constant | Value | Description |
|----------|-------|-------------|
| X_DDS_GOERTZEL_SINC1 | %1111_0000_0000_0111 << 16 | DDS/Goertzel with SINC1 filter |
| X_DDS_GOERTZEL_SINC2 | %1111_0000_1000_0111 << 16 | DDS/Goertzel with SINC2 filter |



## Control Flags

These flags modify streamer behavior and are combined with mode constants using OR.

### DAC Channel Selection

The DAC selection constants control which of the four DAC channels (3, 2, 1, 0) are active and how they're configured. In the naming convention, 0 = streamer data channel X0, 1 = data channel X1 (likewise 2 = X2, 3 = X3), X = no override (the SETDACS value for that DAC passes through), and the N suffix = one's-complement (inverted) output.

| Constant | Value | Description |
|----------|-------|-------------|
| X_DACS_OFF | (default - no bits set) | No streamer DAC output (SETDACS values pass through on all channels) |
| X_DACS_0_0_0_0 | %0000_0001_0000_0000 << 16 | X0 on all four DAC channels (mono) |
| X_DACS_X_X_0_0 | %0000_0010_0000_0000 << 16 | X0 on DAC channels 1 and 0; channels 3,2 not overridden |
| X_DACS_0_0_X_X | %0000_0011_0000_0000 << 16 | X0 on DAC channels 3 and 2; channels 1,0 not overridden |
| X_DACS_X_X_X_0 | %0000_0100_0000_0000 << 16 | X0 on DAC channel 0 only |
| X_DACS_X_X_0_X | %0000_0101_0000_0000 << 16 | X0 on DAC channel 1 only |
| X_DACS_X_0_X_X | %0000_0110_0000_0000 << 16 | X0 on DAC channel 2 only |
| X_DACS_0_X_X_X | %0000_0111_0000_0000 << 16 | X0 on DAC channel 3 only |
| X_DACS_0N0_0N0 | %0000_1000_0000_0000 << 16 | X0 differential pairs on all four channels: ch3 !X0, ch2 X0, ch1 !X0, ch0 X0 |
| X_DACS_X_X_0N0 | %0000_1001_0000_0000 << 16 | X0 differential pair on DAC channels 1 and 0: ch1 !X0, ch0 X0 |
| X_DACS_0N0_X_X | %0000_1010_0000_0000 << 16 | X0 differential pair on DAC channels 3 and 2: ch3 !X0, ch2 X0 |
| X_DACS_1_0_1_0 | %0000_1011_0000_0000 << 16 | X1,X0 pairs on all four channels: ch3 X1, ch2 X0, ch1 X1, ch0 X0 |
| X_DACS_X_X_1_0 | %0000_1100_0000_0000 << 16 | X1,X0 on DAC channels 1 and 0: ch1 X1, ch0 X0 |
| X_DACS_1_0_X_X | %0000_1101_0000_0000 << 16 | X1,X0 on DAC channels 3 and 2: ch3 X1, ch2 X0 |
| X_DACS_1N1_0N0 | %0000_1110_0000_0000 << 16 | X1,X0 differential pairs on all four channels: ch3 !X1, ch2 X1, ch1 !X0, ch0 X0 |
| X_DACS_3_2_1_0 | %0000_1111_0000_0000 << 16 | X3,X2,X1,X0 — one streamer word per channel (standard 4-channel) |

### Pin Output and Hub Write Control

`X_PINS_ON` and `X_WRITE_ON` are **the same bit** — D[23] — under two names, and their values below are identical for that reason. Which one it is depends on the direction of the mode it is combined with: in an output mode (hub to pins/DACs) D[23] enables the streamer's pin output; in a capture mode (pins/ADCs to hub) it enables the hub write. Use the name that matches the mode. OR-ing both sets one bit, not two.

| Constant | Value | Description |
|----------|-------|-------------|
| X_PINS_OFF | (default - no bits set) | Streamer makes no contribution to pin output |
| X_PINS_ON | %0000_0000_1000_0000 << 16 | Streamer drives the pin group's output state (output modes) |
| X_WRITE_OFF | (default - no bits set) | Captured data is not written to hub RAM |
| X_WRITE_ON | %0000_0000_1000_0000 << 16 | Captured data is written to hub RAM (capture modes) |

::: hardware
**`X_PINS_ON` is not the pin's output enable.** It enables the streamer's contribution to the pin's output *state* — the same signal `OUT` supplies. `DIR` is still what lets the pin drive at all, so a streamer command aimed at a pin whose DIR is low runs to completion and changes nothing: the count decrements, the command finishes, and the pin never moves. On the bench that reads as a pin holding whatever charge it had, which looks like noise rather than like a missing step. `DIRH` the pins before streaming to them. Measured on P2 silicon: the same command scored 4 of 8 toggles with DIR low, and 8 of 8 after `DIRH`.
:::

### Alternate Bit Order

| Constant | Value | Description |
|----------|-------|-------------|
| X_ALT_OFF | (default - no bits set) | Normal bit order |
| X_ALT_ON | %0000_0000_0000_0001 << 16 | Alternate bit order for 1/2/4 bit modes |



## Usage Examples

A working streamer command carries three things the mode constant does not, and each has its own home:

- **The data rate** belongs to `SETXFRQ` — a per-clock NCO increment, not a frequency in hertz, where the cog-start default `$8000_0000` produces one streamer event every two clocks. (A `SETQ` immediately before the streamer instruction sets it too.) `XINIT`'s second operand is **not** the rate.
- **The duration** belongs to `D[15:0]`, the number of NCO rollovers the command runs for. The constants below occupy only `D[31:16]`, so a mode ORed with nothing else leaves the count at zero — and a count of zero stops the streamer immediately. OR the count in.
- **The pins** must be able to drive. `X_PINS_ON` enables the streamer's contribution to a pin's output *state*; `DIRH` is still what enables the pin's output.

`XINIT`'s `S` operand supplies mode-specific data — a LUT base, an ADC channel select — or is ignored. Each example says which.

### Video Pixel Streaming

```pasm2
' Stream RGB24 video to pin group 0; color lands on the upper
' 24 pins, the low 8 receive zero
        setxfrq ##NCO_RATE             ' Pixel rate lives here
        rdfast  #0, video_buffer       ' Set up FIFO from video buffer
        dirh    ##0 addpins 31         ' Pins must be enabled to drive
        mov     mode, ##X_RFLONG_RGB24 | X_PINS_ON
        or      mode, ##PIXEL_COUNT    ' D[15:0]: rollovers to run for
        xinit   mode, #0               ' S unused by this mode
```

### Audio DAC Output

The mode constant routes streamer data to a DAC channel; it does not put that channel on a pin. That takes `WRPIN` with a DAC pin mode and this cog's ID, plus `DIRH` — and the pin's own low two bits pick which of the four channels it listens to.

```pasm2
' Stream 8-bit audio samples to DAC channel 0.
' DAC_PIN's low two bits are %00, so it listens to DAC0.
        cogid   cogn                   ' This cog, 0..7
        setnib  dacmode, cogn, #2      ' COGID into M[3:0]
        wrpin   dacmode, #DAC_PIN      ' DAC mode, fed by a cog channel
        dirh    #DAC_PIN               ' The pin now drives

        setxfrq ##NCO_RATE             ' Sample rate lives here
        rdfast  #0, audio_buffer
        mov     mode, ##X_RFBYTE_1P_1DAC1 | X_DACS_X_X_X_0
        or      mode, ##SAMPLE_COUNT   ' D[15:0]: rollovers to run for
        xinit   mode, #0               ' S unused by this mode

dacmode long    P_DAC_124R_3V | P_CHANNEL
```

A one-channel mode wants one-channel routing. `X_DACS_X_X_X_0` puts X0 on DAC0 and leaves the rest to their `SETDACS` values; `X_DACS_3_2_1_0` would route four channels a one-channel mode never fills.

### ADC Capture to Memory

These modes read the four 8-bit SCOPE channels, so the SCOPE pipe must be pointed at a pin block first and the pin itself must be in an ADC smart pin mode.

```pasm2
' Capture SCOPE channel 0 to hub RAM.
' ADC_PIN = 16, so its four-pin block is block 4 (pins 16-19).
        wrpin   ##P_ADC_1X, #ADC_PIN   ' Pin samples in ADC mode
        dirh    #ADC_PIN
        setscp  #%101_0000             ' D[6] on, D[5:2] = block 4
        setxfrq ##NCO_RATE             ' Sample rate lives here
        wrfast  #0, capture_buffer     ' Set up FIFO for writing
        mov     mode, ##X_1ADC8_0P_1DAC8_WFBYTE | X_WRITE_ON
        or      mode, ##SAMPLE_COUNT   ' D[15:0]: rollovers to run for
        xinit   mode, #0               ' S[1:0] selects the channel
```

### LUT-Based Color Mapping

The LUT needs no enabling instruction — the palette simply has to be in lookup RAM before the command runs. For the RDFAST LUT modes the base address comes from `S[3:0]`: those four bits are `%bbbb` in a base of `%bbbb00000`.

```pasm2
' Map nibbles through a LUT palette onto pin group 0
        setxfrq ##NCO_RATE
        rdfast  #0, sprite_data
        dirh    ##0 addpins 31         ' Pins must be enabled to drive
        mov     mode, ##X_RFLONG_8X4_LUT | X_PINS_ON
        or      mode, ##NIBBLE_COUNT   ' D[15:0]: rollovers to run for
        xinit   mode, #0               ' S[3:0] = 0: LUT base $000
```



## Combining Constants

Streamer mode and control flags are combined using OR:

```pasm2
' Full-featured video mode: pins and all four DAC channels
        setxfrq ##NCO_RATE
        mov     mode, ##X_RFLONG_RGB24 | X_PINS_ON | X_DACS_3_2_1_0
        or      mode, ##PIXEL_COUNT    ' D[15:0]: rollovers to run for
        xinit   mode, #0
```



## Related Documentation

**Chapter 5.3 (streamer)** provides the architectural overview of the streamer subsystem, including its relationship with the FIFO, capabilities, and programming model. Refer to that section for conceptual understanding before using these mode constants.

## Related Instructions

- [XINIT](#xinit) — Initialize streamer with mode and NCO rate
- [XCONT](#xcont) — Continue streamer with new parameters
- [XSTOP](#xstop) — Stop streamer operation
- [XZERO](#xzero) — Zero streamer and stop
- [RDFAST](#rdfast) — Set up hub-to-FIFO reading
- [WRFAST](#wrfast) — Set up FIFO-to-hub writing
- [SETLUTS](#setluts) — Configure LUT for streamer use


