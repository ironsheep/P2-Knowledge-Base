# Spin2 Built-In Symbols and Tables - Complete Reference

## Overview
These built-in symbols are **essential** for Spin2 coders to access P2's extended capabilities. They provide symbolic names for complex bit patterns needed to configure SmartPins, Streamers, Events, Interrupts, and Clock settings.

---

## 1. Built-In Symbols for SmartPin Configuration

### SmartPin Mode Structure (32-bit configuration)
```
Bits [31..0] = %AAAA_BBBB_FFF_PPPPPPPPPPPP_TT_MMMMM_0
```
- AAAA = A input selector
- BBBB = B input selector  
- FFF = Filter settings
- P = Pin mode parameters
- TT = Timing mode
- M = Mode selection
- 0 = Reserved (must be 0)

### A Input Configuration

#### A Input Polarity
| Symbol | Description |
|--------|-------------|
| P_TRUE_A | True A input (default) |
| P_INVERT_A | Invert A input |

#### A Input Selection
| Symbol | Description |
|--------|-------------|
| P_LOCAL_A | Select local pin (default) |
| P_PLUS1_A | Select pin+1 |
| P_PLUS2_A | Select pin+2 |
| P_PLUS3_A | Select pin+3 |
| P_OUTBIT_A | Select OUT bit |
| P_MINUS3_A | Select pin-3 |
| P_MINUS2_A | Select pin-2 |
| P_MINUS1_A | Select pin-1 |

### B Input Configuration

#### B Input Polarity
| Symbol | Description |
|--------|-------------|
| P_TRUE_B | True B input (default) |
| P_INVERT_B | Invert B input |

#### B Input Selection
| Symbol | Description |
|--------|-------------|
| P_LOCAL_B | Select local pin (default) |
| P_PLUS1_B | Select pin+1 |
| P_PLUS2_B | Select pin+2 |
| P_PLUS3_B | Select pin+3 |
| P_OUTBIT_B | Select OUT bit |
| P_MINUS3_B | Select pin-3 |
| P_MINUS2_B | Select pin-2 |
| P_MINUS1_B | Select pin-1 |

### Filter Settings
| Symbol | Description |
|--------|-------------|
| P_PASS | No filtering |
| P_FILT0_AB | Filter A and B with 2-clock filter |
| P_FILT1_AB | Filter A and B with 3-clock filter |
| P_FILT2_AB | Filter A and B with 5-clock filter |
| P_FILT3_AB | Filter A and B with 8-clock filter |

### Output Enable Control
| Symbol | Description |
|--------|-------------|
| P_OE | Output enable ON |
| P_FLOAT | Output enable OFF (float) |

### SmartPin Modes (Primary)

#### Digital I/O Modes
| Symbol | Mode | Description |
|--------|------|-------------|
| P_NORMAL | %00000 | Normal I/O (not smart) |
| P_REPOSITORY | %00001 | Long repository |
| P_DAC_990R_3V | %00010 | DAC 990Ω, 3.3V range |
| P_DAC_600R_2V | %00011 | DAC 600Ω, 2.0V range |
| P_DAC_124R_3V | %00100 | DAC 124Ω, 3.3V range |
| P_DAC_75R_2V | %00101 | DAC 75Ω, 2.0V range |
| P_COMPARATOR | %00110 | Comparator mode |
| P_COMPARATOR_FB | %00111 | Comparator with feedback |

#### Measurement Modes
| Symbol | Mode | Description |
|--------|------|-------------|
| P_ADC | %01000 | ADC sample/filter/scope |
| P_ADC_EXT | %01001 | ADC ext trigger |
| P_ADC_SCOPE | %01010 | ADC scope with trigger |
| P_USB_PAIR | %01011 | USB pin pair |

#### Synchronous Serial
| Symbol | Mode | Description |
|--------|------|-------------|
| P_SYNC_RX | %01100 | Sync serial receive |
| P_SYNC_TX | %01101 | Sync serial transmit |
| P_ASYNC_RX | %01110 | Async serial receive |
| P_ASYNC_TX | %01111 | Async serial transmit |

#### Pulse/Edge Modes
| Symbol | Mode | Description |
|--------|------|-------------|
| P_PULSE | %10000 | Pulse output |
| P_TRANSITION | %10001 | Transition output |
| P_NCO_FREQ | %10010 | NCO frequency |
| P_NCO_DUTY | %10011 | NCO duty |
| P_PWM_TRIANGLE | %10100 | PWM triangle |
| P_PWM_SAWTOOTH | %10101 | PWM sawtooth |
| P_PWM_SMPS | %10110 | PWM SMPS |

#### Counter Modes
| Symbol | Mode | Description |
|--------|------|-------------|
| P_QUADRATURE | %10111 | Quadrature decoder |
| P_REG_UP | %11000 | Inc on A-rise & B-high |
| P_REG_UP_DOWN | %11001 | Inc on A-rise, dec on A-fall |
| P_COUNT_RISES | %11010 | Count A-rises |
| P_COUNT_HIGHS | %11011 | Count A-highs |

---

## 2. Built-In Symbols for Streamer Modes

### Streamer Command Structure
```
XCONT D/#, S/#
D = Command + Mode Configuration
S = NCO frequency (32-bit phase increment)
```

### Basic Streamer Commands
| Symbol | Value | Description |
|--------|-------|-------------|
| X_IMM_32X1_LUT | %0000 << 28 | 32x1 from LUT immediate |
| X_IMM_16X2_LUT | %0001 << 28 | 16x2 from LUT immediate |
| X_IMM_8X4_LUT | %0010 << 28 | 8x4 from LUT immediate |
| X_IMM_4X8_LUT | %0011 << 28 | 4x8 from LUT immediate |

### Pin Output Modes
| Symbol | Description |
|--------|-------------|
| X_PINS_OFF | Disable pin outputs |
| X_PINS_ON | Enable pin outputs |
| X_DACS_OFF | Disable DAC outputs |
| X_DACS_ON | Enable DAC outputs (3 channels) |

### DDS/Goertzel Modes
| Symbol | Description |
|--------|-------------|
| X_DDS_GOERTZEL_SINC1 | DDS/Goertzel with SINC1 filter |
| X_DDS_GOERTZEL_SINC2 | DDS/Goertzel with SINC2 filter |

### Data Source Selection
| Symbol | Description |
|--------|-------------|
| X_RFBYTE_LUMA8 | Read bytes, output as 8-bit luma |
| X_RFBYTE_RGB8 | Read bytes, output as RGB 2:2:2 |
| X_RFWORD_RGB16 | Read words, output as RGB 5:6:5 |
| X_RFLONG_RGB24 | Read longs, output as RGB 8:8:8 |

---

## 3. Built-In Symbols for Events and Interrupt Sources

### Event Symbols
| Symbol | Value | Description |
|--------|-------|-------------|
| EVENT_INT | %0000 | Interrupt edge/level |
| EVENT_CT1 | %0001 | CT = CT1 (timing) |
| EVENT_CT2 | %0010 | CT = CT2 |
| EVENT_CT3 | %0011 | CT = CT3 |
| EVENT_SE1 | %0100 | SELINDA execution |
| EVENT_SE2 | %0101 | SELINDA execution |
| EVENT_SE3 | %0110 | SELINDA execution |
| EVENT_SE4 | %0111 | SELINDA execution |
| EVENT_PAT | %1000 | Pin pattern match |
| EVENT_FBW | %1001 | FIFO block wrap |
| EVENT_XMT | %1010 | Streamer empty |
| EVENT_XFI | %1011 | Streamer finished |
| EVENT_XRO | %1100 | Streamer NCO rollover |
| EVENT_XRL | %1101 | Streamer pattern match |
| EVENT_ATN | %1110 | Attention from other cog |
| EVENT_QMT | %1111 | CORDIC/PIX done |

### Interrupt Configuration
```spin2
SETINT1 #event_source
SETINT2 #event_source  
SETINT3 #event_source
```

---

## 4. Built-In Symbols for COG/TASK Control

### COGINIT Usage
| Symbol | Value | Description |
|--------|-------|-------------|
| COGEXEC | %0 << 5 | Start in COG exec mode |
| HUBEXEC | %1 << 5 | Start in HUB exec mode |
| COGEXEC_NEW | %10000 | Start in new COG, COG exec |
| HUBEXEC_NEW | %10001 | Start in new COG, HUB exec |
| COGEXEC_NEW_PAIR | %10010 | Start in new COG pair, COG exec |
| HUBEXEC_NEW_PAIR | %10011 | Start in new COG pair, HUB exec |

### COGSPIN Usage
| Symbol | Description |
|--------|-------------|
| NEWCOG | -1 | Start in any available COG |
| COGID | Current COG number |

### Task Control
| Symbol | Description |
|--------|-------------|
| TASKSPIN | Start task in current COG |
| TASKSTOP | Stop specified task |
| TASKHALT | Halt task execution |
| TASKRESUME | Resume halted task |
| TASKNEXT | Switch to next task |
| TASKWAIT | Wait for task event |

---

## 5. Built-In Numeric Symbols

### Mathematical Constants
| Symbol | Value | Description |
|--------|-------|-------------|
| PI | 3.14159265 | Pi constant |
| E | 2.71828183 | Euler's number |

### System Constants
| Symbol | Value | Description |
|--------|-------|-------------|
| POSX | $7FFFFFFF | Maximum positive |
| NEGX | $80000000 | Maximum negative |
| TRUE | -1 ($FFFFFFFF) | Boolean true |
| FALSE | 0 | Boolean false |

### Memory Sizes
| Symbol | Value | Description |
|--------|-------|-------------|
| COGMEM | 512 | COG memory longs |
| LUTMEM | 512 | LUT memory longs |
| HUBMEM | 524288 | HUB memory bytes |

---

## 6. Clock Setup (CRITICAL)

### Clock Mode Structure
```
CLKMODE = %PPPP_CC_SS
```
- PPPP = PLL divider (1-64)
- CC = Clock source
- SS = Crystal divider

### Clock Source Selection
| Symbol | Value | Description |
|--------|-------|-------------|
| RCFAST | %00 | Internal RC fast (~20MHz) |
| RCSLOW | %01 | Internal RC slow (~20KHz) |
| XTAL | %10 | Crystal/external |
| PLL | %11 | PLL output |

### Crystal Settings
| Symbol | Range | Description |
|--------|-------|-------------|
| XDIV1 | %00 | XI divide by 1 |
| XDIV2 | %01 | XI divide by 2 |
| XDIV4 | %10 | XI divide by 4 |
| XMUL1 | %00 | VCO multiply by 1 |
| XMUL2 | %01 | VCO multiply by 2 |
| XMUL4 | %10 | VCO multiply by 4 |
| XMUL8 | %11 | VCO multiply by 8 |

### Crystal Drive
| Symbol | Description |
|--------|-------------|
| XSEL0 | Low power (< 10MHz) |
| XSEL1 | Medium power (10-20MHz) |
| XSEL2 | High power (15-30MHz) |
| XSEL3 | Maximum power (25-60MHz) |

### PLL Settings
| Symbol | Range | Description |
|--------|-------|-------------|
| XPPPP | 1..64 | PLL post-divider |
| XDIVP | 1..64 | Crystal pre-divider |
| XMULP | 1..1024 | PLL multiplier |
| XPLLN | 0..15 | PLL bandwidth |

### Clock Configuration Example
```spin2
CON
  _clkfreq = 200_000_000  ' Target frequency
  _xtlfreq = 20_000_000   ' Crystal frequency
  _clkmode = XTAL + PLL   ' Use crystal with PLL
```

### Critical Clock Rules
1. **VCO range**: 100-350 MHz
2. **PFD range**: 250 KHz - 28.3 MHz
3. **Crystal ranges**: Match XSEL to crystal frequency
4. **Update P63**: When changing frequency at runtime

---

## Why These Tables Matter

### For SmartPins
- Each pin can be an independent peripheral
- 64 concurrent state machines
- No CPU intervention needed
- Symbols make configuration readable

### For Streamer
- High-speed data movement
- Video generation
- Pattern matching
- DMA-like functionality

### For Events/Interrupts
- 16 event sources per COG
- 3 interrupt levels
- Hardware event detection
- Precise timing control

### For Clock Setup
- System performance
- Power consumption
- Timing accuracy
- Peripheral operation

---

## Usage Examples

### SmartPin PWM Configuration
```spin2
PINSTART(56, P_OE | P_PWM_TRIANGLE, 10000, 5000)
' Pin 56, output enabled, triangle PWM, period=10000, duty=5000
```

### Streamer for Video
```spin2
XCONT(X_RFLONG_RGB24 | X_PINS_ON, ##25_000_000)
' Stream RGB24 data to pins at 25MHz pixel rate
```

### Event Setup
```spin2
SETSE1(EVENT_PAT | pin_mask)
WAITSE1  ' Wait for pin pattern
```

### Clock Change
```spin2
HUBSET(new_clkmode)
WAITX(20_000_000 / 100)  ' Wait 10ms for PLL lock
```

These built-in symbols are the key to unlocking P2's hardware capabilities without dealing with raw bit patterns!