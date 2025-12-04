# Appendix F: Streamer Mode Constants

PASM2 provides predefined constants for configuring the P2's Streamer—a powerful DMA-like engine that transfers data between hub RAM, LUT RAM, pins, and DAC outputs. These constants replace complex bit patterns with readable symbolic names.

## Streamer Overview

The Streamer operates in conjunction with the FIFO and can:
- Transfer data from hub RAM to pins/DACs (playback)
- Transfer data from pins/ADCs to hub RAM (capture)
- Perform real-time data transformations (color conversion, bit manipulation)
- Generate video signals with automatic timing

Streamer commands are issued via XINIT, XCONT, and related instructions.



## Command Word Structure

Streamer commands are 32-bit values composed of mode selection and control fields:

```
Bits 31-16: Mode and sub-mode selection
Bits 15-0:  Additional parameters (NCO rate typically passed separately)
```

The values shown below are the base constants that get combined with control flags using OR operations.



## Immediate to LUT to Pins/DACs

These modes stream immediate data through the LUT to output pins or DAC channels.

| Constant | Value | Description |
|----------|-------|-------------|
| X_IMM_32X1_LUT | %0000_0000_0000_0000 << 16 | 32×1: 32 bits to LUT, 1 bit per pin |
| X_IMM_16X2_LUT | %0001_0000_0000_0000 << 16 | 16×2: 16 bits to LUT, 2 bits per pin |
| X_IMM_8X4_LUT | %0010_0000_0000_0000 << 16 | 8×4: 8 bits to LUT, 4 bits per pin |
| X_IMM_4X8_LUT | %0011_0000_0000_0000 << 16 | 4×8: 4 bits to LUT, 8 bits per pin |



## Immediate to Pins/DACs (Direct)

These modes stream immediate data directly to pins and DAC channels.

| Constant | Value | Description |
|----------|-------|-------------|
| X_IMM_32X1_1DAC1 | %0100_0000_0000_0000 << 16 | 32×1 immediate, 1 pin, 1 DAC channel |
| X_IMM_16X2_2DAC1 | %0101_0000_0000_0000 << 16 | 16×2 immediate, 2 pins, 1 DAC channel |
| X_IMM_16X2_1DAC2 | %0101_0000_0000_0010 << 16 | 16×2 immediate, 1 pin, 2 DAC channels |
| X_IMM_8X4_4DAC1 | %0110_0000_0000_0000 << 16 | 8×4 immediate, 4 pins, 1 DAC channel |
| X_IMM_8X4_2DAC2 | %0110_0000_0000_0010 << 16 | 8×4 immediate, 2 pins, 2 DAC channels |
| X_IMM_8X4_1DAC4 | %0110_0000_0000_0100 << 16 | 8×4 immediate, 1 pin, 4 DAC channels |
| X_IMM_4X8_4DAC2 | %0110_0000_0000_0110 << 16 | 4×8 immediate, 4 pins, 2 DAC channels |
| X_IMM_4X8_2DAC4 | %0110_0000_0000_0111 << 16 | 4×8 immediate, 2 pins, 4 DAC channels |
| X_IMM_4X8_1DAC8 | %0110_0000_0000_1110 << 16 | 4×8 immediate, 1 pin, 8 DAC channels |
| X_IMM_2X16_4DAC4 | %0110_0000_0000_1111 << 16 | 2×16 immediate, 4 pins, 4 DAC channels |
| X_IMM_2X16_2DAC8 | %0111_0000_0000_0000 << 16 | 2×16 immediate, 2 pins, 8 DAC channels |
| X_IMM_1X32_4DAC8 | %0111_0000_0000_0001 << 16 | 1×32 immediate, 4 pins, 8 DAC channels |



## RDFAST to LUT to Pins/DACs

These modes read data from hub RAM via RDFAST FIFO, process through LUT, and output to pins/DACs.

| Constant | Value | Description |
|----------|-------|-------------|
| X_RFLONG_32X1_LUT | %0111_0000_0000_0010 << 16 | Read long, 32×1 to LUT to pins |
| X_RFLONG_16X2_LUT | %0111_0000_0000_0100 << 16 | Read long, 16×2 to LUT to pins |
| X_RFLONG_8X4_LUT | %0111_0000_0000_0110 << 16 | Read long, 8×4 to LUT to pins |
| X_RFLONG_4X8_LUT | %0111_0000_0000_1000 << 16 | Read long, 4×8 to LUT to pins |



## RDFAST Byte Operations

These modes read bytes from hub RAM and output to pins/DACs with various configurations.

| Constant | Value | Description |
|----------|-------|-------------|
| X_RFBYTE_1P_1DAC1 | %1000_0000_0000_0000 << 16 | Read byte, 1 pin, 1 DAC channel |
| X_RFBYTE_2P_2DAC1 | %1001_0000_0000_0000 << 16 | Read byte, 2 pins, 1 DAC channel |
| X_RFBYTE_2P_1DAC2 | %1001_0000_0000_0010 << 16 | Read byte, 1 pin, 2 DAC channels |
| X_RFBYTE_4P_4DAC1 | %1010_0000_0000_0000 << 16 | Read byte, 4 pins, 1 DAC channel |
| X_RFBYTE_4P_2DAC2 | %1010_0000_0000_0010 << 16 | Read byte, 2 pins, 2 DAC channels |
| X_RFBYTE_4P_1DAC4 | %1010_0000_0000_0100 << 16 | Read byte, 1 pin, 4 DAC channels |
| X_RFBYTE_8P_4DAC2 | %1010_0000_0000_0110 << 16 | Read byte, 4 pins, 2 DAC channels |
| X_RFBYTE_8P_2DAC4 | %1010_0000_0000_0111 << 16 | Read byte, 2 pins, 4 DAC channels |
| X_RFBYTE_8P_1DAC8 | %1010_0000_0000_1110 << 16 | Read byte, 1 pin, 8 DAC channels |



## RDFAST Word/Long Operations

These modes read words or longs from hub RAM for higher bandwidth applications.

| Constant | Value | Description |
|----------|-------|-------------|
| X_RFWORD_16P_4DAC4 | %1010_0000_0000_1111 << 16 | Read word, 16 pins, 4 DAC channels |
| X_RFWORD_16P_2DAC8 | %1011_0000_0000_0000 << 16 | Read word, 16 pins, 8 DAC channels |
| X_RFLONG_32P_4DAC8 | %1011_0000_0000_0001 << 16 | Read long, 32 pins, 8 DAC channels |



## Video and Color Modes

These modes perform color space conversion for video generation.

| Constant | Value | Description |
|----------|-------|-------------|
| X_RFBYTE_LUMA8 | %1011_0000_0000_0010 << 16 | Read byte as 8-bit luminance (grayscale) |
| X_RFBYTE_RGBI8 | %1011_0000_0000_0011 << 16 | Read byte as RGBI 2:2:2:2 (16 colors + intensity) |
| X_RFBYTE_RGB8 | %1011_0000_0000_0100 << 16 | Read byte as RGB 3:3:2 (256 colors) |
| X_RFWORD_RGB16 | %1011_0000_0000_0101 << 16 | Read word as RGB 5:6:5 (65536 colors) |
| X_RFLONG_RGB24 | %1011_0000_0000_0110 << 16 | Read long as RGB 8:8:8 (16M colors) |



## WRFAST Operations (Capture)

These modes capture data from pins/ADCs and write to hub RAM via WRFAST FIFO.

| Constant | Value | Description |
|----------|-------|-------------|
| X_1P_1DAC1_WFBYTE | %1100_0000_0000_0000 << 16 | 1 pin, 1 DAC to byte, write to hub |
| X_2P_2DAC1_WFBYTE | %1101_0000_0000_0000 << 16 | 2 pins, 1 DAC to byte, write to hub |
| X_2P_1DAC2_WFBYTE | %1101_0000_0000_0010 << 16 | 1 pin, 2 DACs to byte, write to hub |
| X_4P_4DAC1_WFBYTE | %1110_0000_0000_0000 << 16 | 4 pins, 1 DAC to byte, write to hub |
| X_4P_2DAC2_WFBYTE | %1110_0000_0000_0010 << 16 | 2 pins, 2 DACs to byte, write to hub |
| X_4P_1DAC4_WFBYTE | %1110_0000_0000_0100 << 16 | 1 pin, 4 DACs to byte, write to hub |
| X_8P_4DAC2_WFBYTE | %1110_0000_0000_0110 << 16 | 4 pins, 2 DACs to byte, write to hub |
| X_8P_2DAC4_WFBYTE | %1110_0000_0000_0111 << 16 | 2 pins, 4 DACs to byte, write to hub |
| X_8P_1DAC8_WFBYTE | %1110_0000_0000_1110 << 16 | 1 pin, 8 DACs to byte, write to hub |
| X_16P_4DAC4_WFWORD | %1110_0000_0000_1111 << 16 | 16 pins, 4 DACs to word, write to hub |
| X_16P_2DAC8_WFWORD | %1111_0000_0000_0000 << 16 | 16 pins, 8 DACs to word, write to hub |
| X_32P_4DAC8_WFLONG | %1111_0000_0000_0001 << 16 | 32 pins, 8 DACs to long, write to hub |



## ADC Sampling Modes

These modes capture ADC samples and optionally write to hub RAM.

| Constant | Value | Description |
|----------|-------|-------------|
| X_1ADC8_0P_1DAC8_WFBYTE | %1111_0000_0000_0010 << 16 | 1 ADC to 8-bit, 0 pins, 1 DAC, write byte |
| X_1ADC8_8P_2DAC8_WFWORD | %1111_0000_0000_0011 << 16 | 1 ADC to 8-bit, 8 pins, 2 DACs, write word |
| X_2ADC8_0P_2DAC8_WFWORD | %1111_0000_0000_0100 << 16 | 2 ADCs to 8-bit, 0 pins, 2 DACs, write word |
| X_2ADC8_16P_4DAC8_WFLONG | %1111_0000_0000_0101 << 16 | 2 ADCs to 8-bit, 16 pins, 4 DACs, write long |
| X_4ADC8_0P_4DAC8_WFLONG | %1111_0000_0000_0110 << 16 | 4 ADCs to 8-bit, 0 pins, 4 DACs, write long |



## DDS and Goertzel Modes

These modes perform digital signal processing operations.

| Constant | Value | Description |
|----------|-------|-------------|
| X_DDS_GOERTZEL_SINC1 | %1111_0000_0000_0111 << 16 | DDS/Goertzel with SINC1 filter |
| X_DDS_GOERTZEL_SINC2 | %1111_0000_1000_0111 << 16 | DDS/Goertzel with SINC2 filter |



## Control Flags

These flags modify Streamer behavior and are combined with mode constants using OR.

### DAC Channel Selection

The DAC selection constants control which of the four DAC channels (3, 2, 1, 0) are active and how they're configured. The naming convention uses X for disabled channels, 0/1 for channel values, and N suffix for inverted output.

| Constant | Value | Description |
|----------|-------|-------------|
| X_DACS_OFF | (default - no bits set) | Disable all DAC outputs |
| X_DACS_0_0_0_0 | %0000_0000_0000_0000 << 16 | All 4 DAC channels output 0 |
| X_DACS_X_X_0_0 | %0000_0001_0000_0000 << 16 | DAC channels 3,2 disabled; 1,0 output 0 |
| X_DACS_0_0_X_X | %0000_0010_0000_0000 << 16 | DAC channels 3,2 output 0; 1,0 disabled |
| X_DACS_X_X_X_0 | %0000_0011_0000_0000 << 16 | Only DAC channel 0 enabled |
| X_DACS_X_X_0_X | %0000_0100_0000_0000 << 16 | Only DAC channel 1 enabled |
| X_DACS_X_0_X_X | %0000_0101_0000_0000 << 16 | Only DAC channel 2 enabled |
| X_DACS_0_X_X_X | %0000_0110_0000_0000 << 16 | Only DAC channel 3 enabled |
| X_DACS_0N0_0N0 | %0000_0111_0000_0000 << 16 | Channels 3,1 normal; channels 2,0 inverted |
| X_DACS_X_X_0N0 | %0000_1000_0000_0000 << 16 | Channels 1,0 enabled; channel 0 inverted |
| X_DACS_0N0_X_X | %0000_1001_0000_0000 << 16 | Channels 3,2 enabled; channel 2 inverted |
| X_DACS_1_0_1_0 | %0000_1010_0000_0000 << 16 | Alternating 1,0 pattern across all channels |
| X_DACS_X_X_1_0 | %0000_1011_0000_0000 << 16 | Channels 1,0 with 1,0 pattern |
| X_DACS_1_0_X_X | %0000_1100_0000_0000 << 16 | Channels 3,2 with 1,0 pattern |
| X_DACS_1N1_0N0 | %0000_1101_0000_0000 << 16 | All channels; odd channels inverted |
| X_DACS_3_2_1_0 | %0000_1110_0000_0000 << 16 | Use all 4 DAC channels (standard) |

### Pin Output Control

| Constant | Value | Description |
|----------|-------|-------------|
| X_PINS_OFF | (default - no bits set) | Disable pin outputs |
| X_PINS_ON | %0000_0000_1000_0000 << 16 | Enable pin outputs |

### Write Control

| Constant | Value | Description |
|----------|-------|-------------|
| X_WRITE_OFF | (default - no bits set) | Disable hub RAM writes |
| X_WRITE_ON | %0000_0000_1000_0000 << 16 | Enable hub RAM writes |

### Alternate Bit Order

| Constant | Value | Description |
|----------|-------|-------------|
| X_ALT_OFF | (default - no bits set) | Normal bit order |
| X_ALT_ON | %0000_0000_0000_0001 << 16 | Alternate bit order for 1/2/4 bit modes |



## Usage Examples

### Video Pixel Streaming

```pasm
' Stream RGB24 video data to VGA pins
        rdfast  #0, video_buffer       ' Set up FIFO from video buffer
        mov     mode, ##X_RFLONG_RGB24 | X_PINS_ON
        xinit   mode, ##25_000_000     ' 25 MHz pixel clock
```

### Audio DAC Output

```pasm
' Stream 8-bit audio samples to DAC
        rdfast  #0, audio_buffer
        mov     mode, ##X_RFBYTE_1P_1DAC1 | X_DACS_3_2_1_0
        xinit   mode, ##44100          ' 44.1 kHz sample rate
```

### ADC Capture to Memory

```pasm
' Capture ADC samples to hub RAM
        wrfast  #0, capture_buffer     ' Set up FIFO for writing
        mov     mode, ##X_1ADC8_0P_1DAC8_WFBYTE | X_WRITE_ON
        xinit   mode, ##100_000        ' 100 kHz sample rate
```

### LUT-Based Color Mapping

```pasm
' Stream bytes through LUT for palette lookup
        rdfast  #0, sprite_data
        mov     mode, ##X_RFLONG_8X4_LUT | X_PINS_ON
        setluts #0                      ' Use LUT for color palette
        xinit   mode, nco_value
```



## Mode Naming Convention

Streamer constant names follow a consistent pattern:

```
X_[source][size]_[pins]P_[dacs]DAC[bits]_[dest]
```

| Component | Meaning |
|-----------|---------|
| X_ | Streamer constant prefix |
| RF | Read from FIFO (hub RAM) |
| WF | Write to FIFO (hub RAM) |
| IMM | Immediate data |
| BYTE/WORD/LONG | Data unit size |
| _nP | Number of pins used |
| _nDACn | Number of DAC channels, bits per channel |
| LUT | Data passes through LUT |



## Combining Constants

Streamer mode and control flags are combined using OR:

```pasm
' Full-featured video mode
        mov     mode, ##X_RFLONG_RGB24 | X_PINS_ON | X_DACS_3_2_1_0
        xinit   mode, nco_rate
```



## Data Width Modes

The Streamer supports various data packing/unpacking modes:

| Mode | Meaning |
|------|---------|
| 32x1 | 32 single-bit values per transfer |
| 16x2 | 16 2-bit values per transfer |
| 8x4 | 8 4-bit (nibble) values per transfer |
| 4x8 | 4 8-bit (byte) values per transfer |
| 2x16 | 2 16-bit (word) values per transfer |
| 1x32 | 1 32-bit (long) value per transfer |



## Related Instructions

- [XINIT](#xinit) — Initialize Streamer with mode and NCO rate
- [XCONT](#xcont) — Continue Streamer with new parameters
- [XSTOP](#xstop) — Stop Streamer operation
- [XZERO](#xzero) — Zero Streamer and stop
- [RDFAST](#rdfast) — Set up hub-to-FIFO reading
- [WRFAST](#wrfast) — Set up FIFO-to-hub writing
- [SETLUTS](#setluts) — Configure LUT for Streamer use

