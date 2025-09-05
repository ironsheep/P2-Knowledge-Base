# Complete Streamer Symbols Reference - ALL MODES

## Understanding Streamer Symbols
The Streamer moves data at high speed between hub memory and pins/DACs without CPU intervention. These symbols configure complex 32-bit patterns into readable operations.

---

## COMPLETE Streamer Mode Symbols

### Immediate to LUT to Pins/DACs
```spin2
X_IMM_32X1_LUT         ' %0000 << 28 - 32x1 immediate to LUT to pins
X_IMM_16X2_LUT         ' %0001 << 28 - 16x2 immediate to LUT to pins  
X_IMM_8X4_LUT          ' %0010 << 28 - 8x4 immediate to LUT to pins
X_IMM_4X8_LUT          ' %0011 << 28 - 4x8 immediate to LUT to pins
```

### Immediate to Pins/DACs (Complete Set)
```spin2
X_IMM_32X1_1DAC1       ' %0100 << 28 - 32x1 immediate, 1 pin, 1 DAC channel
X_IMM_16X2_2DAC1       ' %0101 << 28 - 16x2 immediate, 2 pins, 1 DAC channel
X_IMM_16X2_1DAC2       ' %0101 << 28 - 16x2 immediate, 1 pin, 2 DAC channels
X_IMM_8X4_4DAC1        ' %0110 << 28 - 8x4 immediate, 4 pins, 1 DAC channel
X_IMM_8X4_2DAC2        ' %0110 << 28 - 8x4 immediate, 2 pins, 2 DAC channels
X_IMM_8X4_1DAC4        ' %0110 << 28 - 8x4 immediate, 1 pin, 4 DAC channels
X_IMM_4X8_4DAC2        ' %0110 << 28 - 4x8 immediate, 4 pins, 2 DAC channels
X_IMM_4X8_2DAC4        ' %0110 << 28 - 4x8 immediate, 2 pins, 4 DAC channels
X_IMM_4X8_1DAC8        ' %0110 << 28 - 4x8 immediate, 1 pin, 8 DAC channels
X_IMM_2X16_4DAC4       ' %0110 << 28 - 2x16 immediate, 4 pins, 4 DAC channels
X_IMM_2X16_2DAC8       ' %0111 << 28 - 2x16 immediate, 2 pins, 8 DAC channels
X_IMM_1X32_4DAC8       ' %0111 << 28 - 1x32 immediate, 4 pins, 8 DAC channels
```

### RDFAST to LUT to Pins/DACs
```spin2
X_RFLONG_32X1_LUT      ' %0111 << 28 - Read long, 32x1 to LUT to pins
X_RFLONG_16X2_LUT      ' %0111 << 28 - Read long, 16x2 to LUT to pins
X_RFLONG_8X4_LUT       ' %0111 << 28 - Read long, 8x4 to LUT to pins
X_RFLONG_4X8_LUT       ' %0111 << 28 - Read long, 4x8 to LUT to pins
```

### RDFAST Byte Operations (Complete Set)
```spin2
X_RFBYTE_1P_1DAC1      ' %1000 << 28 - Read byte, 1 pin, 1 DAC channel
X_RFBYTE_2P_2DAC1      ' %1001 << 28 - Read byte, 2 pins, 1 DAC channel
X_RFBYTE_2P_1DAC2      ' %1001 << 28 - Read byte, 1 pin, 2 DAC channels
X_RFBYTE_4P_4DAC1      ' %1010 << 28 - Read byte, 4 pins, 1 DAC channel
X_RFBYTE_4P_2DAC2      ' %1010 << 28 - Read byte, 2 pins, 2 DAC channels
X_RFBYTE_4P_1DAC4      ' %1010 << 28 - Read byte, 1 pin, 4 DAC channels
X_RFBYTE_8P_4DAC2      ' %1010 << 28 - Read byte, 4 pins, 2 DAC channels
X_RFBYTE_8P_2DAC4      ' %1010 << 28 - Read byte, 2 pins, 4 DAC channels
X_RFBYTE_8P_1DAC8      ' %1010 << 28 - Read byte, 1 pin, 8 DAC channels
```

### RDFAST Word/Long Operations
```spin2
X_RFWORD_16P_4DAC4     ' %1010 << 28 - Read word, 16 pins, 4 DAC channels
X_RFWORD_16P_2DAC8     ' %1011 << 28 - Read word, 16 pins, 8 DAC channels
X_RFLONG_32P_4DAC8     ' %1011 << 28 - Read long, 32 pins, 8 DAC channels
```

### Video/Color Modes (RGB Operations)
```spin2
X_RFBYTE_LUMA8         ' %1011 << 28 - Read byte as 8-bit luminance
X_RFBYTE_RGBI8         ' %1011 << 28 - Read byte as RGBI 2:2:2:2
X_RFBYTE_RGB8          ' %1011 << 28 - Read byte as RGB 3:3:2
X_RFWORD_RGB16         ' %1011 << 28 - Read word as RGB 5:6:5
X_RFLONG_RGB24         ' %1011 << 28 - Read long as RGB 8:8:8
```

### WRFAST Operations (Complete Set)
```spin2
X_1P_1DAC1_WFBYTE      ' %1100 << 28 - Write byte, 1 pin to 1 DAC channel
X_2P_2DAC1_WFBYTE      ' %1101 << 28 - Write byte, 2 pins to 1 DAC channel
X_2P_1DAC2_WFBYTE      ' %1101 << 28 - Write byte, 1 pin to 2 DAC channels
X_4P_4DAC1_WFBYTE      ' %1110 << 28 - Write byte, 4 pins to 1 DAC channel
X_4P_2DAC2_WFBYTE      ' %1110 << 28 - Write byte, 2 pins to 2 DAC channels
X_4P_1DAC4_WFBYTE      ' %1110 << 28 - Write byte, 1 pin to 4 DAC channels
X_8P_4DAC2_WFBYTE      ' %1110 << 28 - Write byte, 4 pins to 2 DAC channels
X_8P_2DAC4_WFBYTE      ' %1110 << 28 - Write byte, 2 pins to 4 DAC channels
X_8P_1DAC8_WFBYTE      ' %1110 << 28 - Write byte, 1 pin to 8 DAC channels
X_16P_4DAC4_WFWORD     ' %1110 << 28 - Write word, 16 pins to 4 DAC channels
X_16P_2DAC8_WFWORD     ' %1111 << 28 - Write word, 16 pins to 8 DAC channels
X_32P_4DAC8_WFLONG     ' %1111 << 28 - Write long, 32 pins to 8 DAC channels
```

### ADC Sampling Modes
```spin2
X_1ADC8_0P_1DAC8_WFBYTE  ' %1111 << 28 - 1 ADC to 8-bit, 0 pins, 1 DAC channel
X_1ADC8_8P_2DAC8_WFWORD  ' %1111 << 28 - 1 ADC to 8-bit, 8 pins, 2 DAC channels
X_2ADC8_0P_2DAC8_WFWORD  ' %1111 << 28 - 2 ADCs to 8-bit, 0 pins, 2 DAC channels
X_2ADC8_16P_4DAC8_WFLONG ' %1111 << 28 - 2 ADCs to 8-bit, 16 pins, 4 DAC channels
X_4ADC8_0P_4DAC8_WFLONG  ' %1111 << 28 - 4 ADCs to 8-bit, 0 pins, 4 DAC channels
```

### DDS/Goertzel Modes
```spin2
X_DDS_GOERTZEL_SINC1   ' %1111 << 28 - DDS/Goertzel with SINC1 filter
X_DDS_GOERTZEL_SINC2   ' %1111 << 28 - DDS/Goertzel with SINC2 filter
```

---

## COMPLETE Streamer Control Flags

### Pin Output Control
```spin2
X_PINS_OFF             ' Disable pin outputs (default)
X_PINS_ON              ' Enable pin outputs
```

### DAC Channel Selection (ALL Combinations)
```spin2
X_DACS_OFF             ' Disable all DAC outputs (default)
X_DACS_0_0_0_0         ' All 4 DAC channels to 0
X_DACS_X_X_0_0         ' DAC channels 3,2 off, 1,0 to 0
X_DACS_0_0_X_X         ' DAC channels 3,2 to 0, 1,0 off
X_DACS_X_X_X_0         ' DAC channel 0 only (3,2,1 off)
X_DACS_X_X_0_X         ' DAC channel 1 only
X_DACS_X_0_X_X         ' DAC channel 2 only
X_DACS_0_X_X_X         ' DAC channel 3 only
X_DACS_0N0_0N0         ' Channels 3,1 normal, 2,0 inverted
X_DACS_X_X_0N0         ' Channels 1,0 with 0 inverted
X_DACS_0N0_X_X         ' Channels 3,2 with 2 inverted
X_DACS_1_0_1_0         ' Alternating 1,0 pattern
X_DACS_X_X_1_0         ' Channels 1,0 = 1,0 pattern
X_DACS_1_0_X_X         ' Channels 3,2 = 1,0 pattern
X_DACS_1N1_0N0         ' All with odd inverted
X_DACS_3_2_1_0         ' Use all 4 channels (3,2,1,0)
```

### Write Control
```spin2
X_WRITE_OFF            ' Disable write operations (default)
X_WRITE_ON             ' Enable write operations
```

### Alternate Bit Order
```spin2
X_ALT_OFF              ' Normal bit order (default)
X_ALT_ON               ' Alternate bit order for 1/2/4 bit modes
```

---

## Streamer Command Structure

### Basic Usage
```spin2
XCONT D/#, S/#
' D = Command (mode symbol) | Control flags
' S = NCO frequency (32-bit phase increment)
```

### Example Configurations
```spin2
' Stream RGB video to pins
XCONT X_RFLONG_RGB24 | X_PINS_ON, ##25_000_000

' Stream data to all 4 DAC channels
XCONT X_RFBYTE_8P_1DAC8 | X_DACS_3_2_1_0, ##1_000_000

' High-speed pattern generation via LUT
XCONT X_IMM_32X1_LUT | X_PINS_ON, ##100_000_000

' ADC sampling to hub memory
XCONT X_4ADC8_0P_4DAC8_WFLONG | X_WRITE_ON, ##500_000
```

---

## Mode Categories Summary

### Data Width Modes
- **32x1**: 32 single-bit values
- **16x2**: 16 2-bit values
- **8x4**: 8 4-bit values
- **4x8**: 4 8-bit values
- **2x16**: 2 16-bit values
- **1x32**: 1 32-bit value

### Source/Destination
- **IMM**: Immediate data from instruction
- **RF**: RDFAST from hub memory
- **WF**: WRFAST to hub memory
- **LUT**: Through lookup table
- **ADC**: From ADC pins

### Pin/DAC Combinations
- **xP**: Number of pins (1P, 2P, 4P, 8P, 16P, 32P)
- **xDACy**: DAC channels (1DAC1, 2DAC2, 4DAC4, etc.)

---

## Why These Symbols Matter

Without these symbols, configuring the streamer requires manipulating raw 32-bit patterns like `%1111_0000_0000_0110 << 16`. The symbols make complex streaming operations readable and maintainable.

### The Power of Composition
```spin2
' Instead of: %1011_0000_1000_0101 << 16
' Use: X_RFWORD_RGB16 | X_PINS_ON | X_DACS_3_2_1_0
```

This transforms incomprehensible bit patterns into self-documenting code that clearly shows:
- Reading words from hub
- Interpreting as RGB 5:6:5
- Outputting to pins
- Using all 4 DAC channels

The Streamer is one of P2's most powerful features, and these symbols make it accessible.