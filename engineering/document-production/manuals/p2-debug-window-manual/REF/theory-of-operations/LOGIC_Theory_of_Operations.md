# LOGIC Display Window - Theory of Operations

**Current as of**: PNut v51a for Propeller 2

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Display Type and Constants](#3-display-type-and-constants)
4. [Data Structures](#4-data-structures)
5. [Configuration and Initialization](#5-configuration-and-initialization)
6. [Data Packing System](#6-data-packing-system)
7. [Channel Configuration](#7-channel-configuration)
8. [Sample Processing](#8-sample-processing)
9. [Trigger System](#9-trigger-system)
10. [Rendering Pipeline](#10-rendering-pipeline)
11. [Timing and Rate Control](#11-timing-and-rate-control)
12. [User Commands](#12-user-commands)
13. [Performance Characteristics](#13-performance-characteristics)
14. [Comparison with Other Display Types](#14-comparison-with-other-display-types)
15. [Usage Examples](#15-usage-examples)
16. [Implementation Details](#16-implementation-details)
17. [Element Array Protocol Specification](#17-element-array-protocol-specification)
18. [Buffer Management and Timing](#18-buffer-management-and-timing)
19. [Bitmap System and Double-Buffering](#19-bitmap-system-and-double-buffering)
20. [Shared Infrastructure](#20-shared-infrastructure)
21. [Initialization Lifecycle](#21-initialization-lifecycle)
22. [Summary](#22-summary)

---

## 1. Introduction

The **LOGIC** display window is a digital logic analyzer for the Propeller 2 (P2) microcontroller debug environment. It provides real-time visualization of digital signals with features similar to traditional logic analyzer hardware:

- **Up to 32 digital channels** with individual labeling and coloring
- **Multi-bit range visualization** (display multi-bit values as analog waveforms)
- **Flexible data packing** (12 packing modes from 1-bit to 32-bit)
- **Edge-sensitive triggering** with configurable mask and match
- **Holdoff control** to avoid trigger spam
- **Circular sample buffer** (2048 samples)
- **Rate limiting** for display update control
- **Anti-aliased waveform rendering**

The LOGIC window is ideal for debugging digital circuits, communication protocols, state machines, and timing-critical code.

**File Location**: `DebugDisplayUnit.pas`

**Key Methods**:
- `LOGIC_Configure` (lines 926-1032): Initialization and channel setup
- `LOGIC_Update` (lines 1034-1106): Sample ingestion and trigger processing
- `LOGIC_Draw` (lines 1108-1144): Waveform rendering

---

## 2. Architecture Overview

### 2.1 System Context

The LOGIC window operates as part of the P2 debug display system:

```
┌─────────────────────────────────────────────────────────────┐
│                    Propeller 2 Hardware                     │
│              (Digital Signal Sampling)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Serial Transmission
                         │ (Packed Sample Data)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      SerialUnit.pas                          │
│            (Background Thread, 16MB RX Buffer)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Element Array Parsing
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       DebugUnit.pas                          │
│                  (Display Management Layer)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ UpdateDisplay Trigger
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   DebugDisplayUnit.pas                       │
│                     LOGIC_Update Method                      │
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│  │ Data Packing │   │   Trigger    │   │   Circular   │   │
│  │   UnPack()   │──>│  Detection   │──>│Sample Buffer │   │
│  └──────────────┘   └──────────────┘   └──────────────┘   │
│                                              │               │
│                                              │ RateCycle     │
│                                              ▼               │
│                     ┌──────────────────────────────┐        │
│                     │     LOGIC_Draw Method        │        │
│                     │  (Waveform Rendering)        │        │
│                     └──────────────────────────────┘        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Double-Buffered Display
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Windows VCL Canvas                         │
│              (Waveform Visualization)                        │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

**Configuration Flow** (Window Creation):
```
Serial Command → Parse Channels → LOGIC_Configure → Set Metrics → Create Window
```

**Sample Flow** (Data Acquisition):
```
P2 Sample → Pack Data → Serial TX → UnPack → Circular Buffer → Trigger Check → LOGIC_Draw
```

**Trigger Flow** (Event Detection):
```
Sample → Apply Mask → Compare with Match → Arming Logic → Holdoff → Trigger Event → Redraw
```

---

## 3. Display Type and Constants

### 3.1 Display Type Identifier

```pascal
dis_logic = 0;
```

The LOGIC display is the first display type (index 0) in the debug display system.

**Source Location**: Line 22 in DebugDisplayUnit.pas

### 3.2 Buffer Constants

```pascal
DataSetsExp      = 11;
DataSets         = 1 shl DataSetsExp;    // 2048

LogicChannels    = 32;                    // Maximum channels
LogicSets        = DataSets;              // 2048 samples
LogicPtrMask     = LogicSets - 1;         // 2047 (for circular buffer)
```

**Purpose**:
- `DataSets`: Number of sample slots in circular buffer (2048)
- `LogicChannels`: Maximum number of displayable channels (32)
- `LogicSets`: Alias for DataSets, specific to LOGIC display
- `LogicPtrMask`: Bit mask for circular buffer wraparound (2047 = 0x7FF)

**Memory Calculation**:
```
LogicSampleBuff: 2048 samples × 4 bytes = 8 KB
```

**Source Locations**: Lines 154-162 in DebugDisplayUnit.pas

### 3.3 Default Values

```pascal
// From LOGIC_Configure (lines 933-939)
vSamples     := 32;          // Default horizontal resolution (samples)
vSpacing     := 8;           // Default spacing between samples (pixels)
vRate        := 1;           // Default rate divisor (1 = every sample)
vLogicIndex  := 0;           // Channel counter
vDotSize     := 0;           // Default dot size (0 = no dots)
vLineSize    := 3;           // Default line thickness (pixels)
vTextSize    := FontSize;    // Default label font size
```

**Default Display Dimensions**:
```
Width  = vSamples × vSpacing = 32 × 8 = 256 pixels
Height = vLogicIndex × ChrHeight (depends on channel count)
```

---

## 4. Data Structures

### 4.1 Sample Buffer

```pascal
LogicSampleBuff: array[0..LogicSets - 1] of integer;
```

**Characteristics**:
- **Size**: 2048 samples (LogicSets = 2048)
- **Element Type**: 32-bit integer (can hold 32 channels of 1-bit data)
- **Access Pattern**: Circular buffer with wraparound
- **Pointer**: `SamplePtr` (global variable)

**Circular Buffer Management**:
```pascal
// Write sample
LogicSampleBuff[SamplePtr] := sample;
SamplePtr := (SamplePtr + 1) and LogicPtrMask;

// Read sample (k samples back from current)
sample := LogicSampleBuff[(SamplePtr - k - 1) and LogicPtrMask];
```

**Fill Level**:
```pascal
SamplePop: integer;          // Number of valid samples (0..vSamples)
```

### 4.2 Channel Configuration Arrays

```pascal
vLogicLabel : array[0..LogicChannels - 1] of string;     // Channel labels
vLogicColor : array[0..LogicChannels - 1] of integer;    // Channel colors (RGB24)
vLogicBits  : array[0..LogicChannels - 1] of byte;       // Bits per channel (1 or >1 for range)
```

**Purpose**:
- **vLogicLabel**: Text labels displayed to the left of each channel
- **vLogicColor**: Waveform colors (RGB24 format: $00RRGGBB)
- **vLogicBits**: Bit width of each channel
  - `1`: Single-bit digital signal (binary waveform)
  - `>1`: Multi-bit range (analog-style waveform)

**Channel Indexing**:
- Channels are indexed 0 to 31
- `vLogicIndex`: Total number of active channels

**Example**:
```pascal
// Channel 0: Single-bit clock signal
vLogicLabel[0] := 'CLK';
vLogicColor[0] := $00FF00;      // Lime green
vLogicBits[0]  := 1;            // 1-bit signal

// Channel 1: 8-bit range value
vLogicLabel[1] := 'DATA';
vLogicColor[1] := $FF0000;      // Red
vLogicBits[1]  := 8;            // 8-bit range
```

### 4.3 Trigger State Variables

```pascal
vTriggerMask    : integer;       // Bit mask for trigger channels
vTriggerMatch   : integer;       // Expected value for trigger
vTriggerOffset  : integer;       // Sample offset for trigger position (0..vSamples-1)
vHoldOff        : integer;       // Holdoff count to prevent re-triggering
vHoldOffCount   : integer;       // Current holdoff counter
vArmed          : boolean;       // Trigger armed state
vTriggered      : boolean;       // Trigger event occurred
```

**Trigger Logic**:
1. **vTriggerMask**: Defines which channels participate in trigger
   - Bit N set = channel N is part of trigger condition
   - Example: `$00000003` = channels 0 and 1

2. **vTriggerMatch**: Expected value on masked channels
   - Example: `$00000001` = channel 0 high, channel 1 low

3. **vTriggerOffset**: Position of trigger in display
   - `0`: Trigger at left edge
   - `vSamples/2`: Trigger at center (default)
   - `vSamples-1`: Trigger at right edge

4. **vHoldOff**: Minimum samples between triggers
   - Prevents continuous re-triggering on high-frequency signals

5. **vArmed/vTriggered**: State machine flags

### 4.4 Packing State Variables

```pascal
vPackAlt        : boolean;       // Alternate bit ordering
vPackSignx      : boolean;       // Sign extension enabled
vPackMask       : integer;       // Bit mask for extraction
vPackShift      : integer;       // Bits per sample
vPackCount      : integer;       // Samples per packed value
```

**Purpose**: Control unpacking of samples from serial data stream.

**Packing Modes** (see Section 6 for details):
- LONGS_1BIT: 32 samples of 1 bit each
- LONGS_2BIT: 16 samples of 2 bits each
- ... through ...
- BYTES_4BIT: 2 samples of 4 bits each

### 4.5 Display State Variables

```pascal
vSamples        : integer;       // Horizontal resolution (samples displayed)
vSpacing        : integer;       // Pixel spacing between samples
vRate           : integer;       // Rate divisor (1 = every sample triggers draw)
vRateCount      : integer;       // Current rate counter
vDotSize        : integer;       // Dot diameter (pixels, 0 = no dots)
vLineSize       : integer;       // Line thickness (pixels)
vTextSize       : integer;       // Label font size
vLogicIndex     : integer;       // Number of active channels
```

---

## 5. Configuration and Initialization

### 5.1 LOGIC_Configure Method

```pascal
procedure TDebugDisplayForm.LOGIC_Configure;
var
  i, v, color: integer;
  s: string;
  isRange: boolean;
begin
  // Set unique defaults
  vSamples := 32;
  vSpacing := 8;
  vRate := 1;
  vLogicIndex := 0;
  vDotSize := 0;
  vLineSize := 3;
  vTextSize := FontSize;

  // Process any parameters
  while not NextEnd do
  begin
    if NextNum then Break;   // number not allowed
    if NextKey then
    case val of
      key_title:       KeyTitle;
      key_pos:         KeyPos;
      key_samples:     KeyValWithin(vSamples, 4, LogicSets - 1);
      key_spacing:     KeyValWithin(vSpacing, 2-1, 32);
      key_rate:        KeyValWithin(vRate, 1, LogicSets);
      key_dotsize:     KeyValWithin(vDotSize, 0, 32);
      key_linesize:    KeyValWithin(vLineSize, 1, 32);
      key_textsize:    KeyTextSize;
      key_color:       if KeyColor(vBackColor) then KeyColor(vGridColor);
      key_hidexy:      vHideXY := True;
      key_longs_1bit..key_bytes_4bit:  KeyPack;
    end
    else
    if NextStr then
    begin
      // Channel configuration (see Section 7)
    end;
  end;

  // If no labels specified, do 32 channels
  if vLogicIndex = 0 then
  begin
    for i := 0 to LogicChannels - 1 do
    begin
      vLogicLabel[i] := IntToStr(i);
      vLogicColor[i] := DefaultScopeColors[0];
      vLogicBits[i] := 1;
    end;
    vLogicIndex := LogicChannels;
  end
  else MaxLimit(vLogicIndex, LogicChannels);

  // Reset trigger data
  vTriggerMask := 0;
  vTriggerMatch := 1;
  vTriggerOffset := vSamples div 2;
  vHoldOff := vSamples;

  // Set channel metrics
  v := 0;
  for i := 0 to vLogicIndex - 1 do MinLimit(v, Length(vLogicLabel[i]) + 2);

  // Set form metrics
  SetTextMetrics;
  vWidth := vSamples * vSpacing;
  vHeight := vLogicIndex * ChrHeight;
  SetSize(v * ChrWidth, ChrHeight, ChrHeight, ChrHeight);
end;
```

**Source Location**: Lines 926-1032

### 5.2 Configuration Parameters

| Parameter | Command | Default | Range | Purpose |
|-----------|---------|---------|-------|---------|
| Title | `TITLE 'string'` | "Logic" | - | Window title |
| Position | `POS x y` | Cascaded | Screen coords | Window position |
| Samples | `SAMPLES count` | 32 | 4-2047 | Horizontal resolution |
| Spacing | `SPACING pixels` | 8 | 1-32 | Pixel spacing between samples |
| Rate | `RATE divisor` | 1 | 1-2048 | Display update rate divisor |
| Dot Size | `DOTSIZE pixels` | 0 | 0-32 | Dot diameter (0 = no dots) |
| Line Size | `LINESIZE pixels` | 3 | 1-32 | Line thickness |
| Text Size | `TEXTSIZE size` | 9 | 6-200 | Label font size |
| Colors | `COLOR back grid` | Black/Gray | RGB24 | Background and grid colors |
| Hide XY | `HIDEXY` | Show | - | Hide mouse coordinates |
| Packing | `LONGS_1BIT` etc. | LONGS_1BIT | 12 modes | Data packing format |

### 5.3 Display Metrics Calculation

**Width Calculation**:
```pascal
vWidth := vSamples * vSpacing;
```

Example: 32 samples × 8 pixels = 256 pixels

**Height Calculation**:
```pascal
vHeight := vLogicIndex * ChrHeight;
```

Example: 8 channels × 18 pixels = 144 pixels

**Left Margin** (for labels):
```pascal
// Maximum label length among all channels
maxLabelLen := 0;
for i := 0 to vLogicIndex - 1 do
  maxLabelLen := max(maxLabelLen, Length(vLogicLabel[i]) + 2);

vMarginLeft := maxLabelLen * ChrWidth;
```

**Window Size**:
```pascal
SetSize(leftMargin, topMargin, rightMargin, bottomMargin);
// Expands client area to accommodate canvas + margins
```

### 5.4 Default Channel Configuration

If no channels are explicitly configured:

```pascal
for i := 0 to LogicChannels - 1 do
begin
  vLogicLabel[i] := IntToStr(i);            // Labels: "0", "1", "2", ...
  vLogicColor[i] := DefaultScopeColors[0];  // All channels lime green
  vLogicBits[i] := 1;                       // All single-bit channels
end;
vLogicIndex := LogicChannels;               // Enable all 32 channels
```

### 5.5 Trigger Initialization

```pascal
vTriggerMask := 0;              // Trigger disabled (no mask)
vTriggerMatch := 1;             // Match value (ignored when mask = 0)
vTriggerOffset := vSamples div 2;   // Trigger at center
vHoldOff := vSamples;           // Holdoff = full buffer width
```

**Trigger Disabled**: When `vTriggerMask = 0`, every sample (after rate limiting) triggers a display update.

---

## 6. Data Packing System

The LOGIC window supports 12 data packing modes to efficiently transmit sample data over the serial link.

### 6.1 Packing Mode Constants

```pascal
key_longs_1bit  = 29;    // LONGS_1BIT
key_longs_2bit  = 30;    // LONGS_2BIT
key_longs_4bit  = 31;    // LONGS_4BIT
key_longs_8bit  = 32;    // LONGS_8BIT
key_longs_16bit = 33;    // LONGS_16BIT
key_words_1bit  = 34;    // WORDS_1BIT
key_words_2bit  = 35;    // WORDS_2BIT
key_words_4bit  = 36;    // WORDS_4BIT
key_words_8bit  = 37;    // WORDS_8BIT
key_bytes_1bit  = 38;    // BYTES_1BIT
key_bytes_2bit  = 39;    // BYTES_2BIT
key_bytes_4bit  = 40;    // BYTES_4BIT
```

**Source Locations**: Lines 63-74 in DebugDisplayUnit.pas

### 6.2 PackDef Table

```pascal
PackDef: array [key_longs_1bit..key_bytes_4bit] of integer = (
  0 shl 16 +  1 shl 8 + 32,   // LONGS_1BIT:  signx=0, shift=1,  count=32
  0 shl 16 +  2 shl 8 + 16,   // LONGS_2BIT:  signx=0, shift=2,  count=16
  0 shl 16 +  4 shl 8 + 8,    // LONGS_4BIT:  signx=0, shift=4,  count=8
  0 shl 16 +  8 shl 8 + 4,    // LONGS_8BIT:  signx=0, shift=8,  count=4
  0 shl 16 + 16 shl 8 + 2,    // LONGS_16BIT: signx=0, shift=16, count=2
  0 shl 16 +  1 shl 8 + 16,   // WORDS_1BIT:  signx=0, shift=1,  count=16
  0 shl 16 +  2 shl 8 + 8,    // WORDS_2BIT:  signx=0, shift=2,  count=8
  0 shl 16 +  4 shl 8 + 4,    // WORDS_4BIT:  signx=0, shift=4,  count=4
  0 shl 16 +  8 shl 8 + 2,    // WORDS_8BIT:  signx=0, shift=8,  count=2
  0 shl 16 +  1 shl 8 + 8,    // BYTES_1BIT:  signx=0, shift=1,  count=8
  0 shl 16 +  2 shl 8 + 4,    // BYTES_2BIT:  signx=0, shift=2,  count=4
  0 shl 16 +  4 shl 8 + 2);   // BYTES_4BIT:  signx=0, shift=4,  count=2
```

**Encoding Format**: `signx shl 16 + shift shl 8 + count`

**Source Location**: Lines 140-152 in DebugDisplayUnit.pas

### 6.3 Packing Parameters

| Mode | Shift (Bits) | Count (Samples) | Mask | Description |
|------|--------------|-----------------|------|-------------|
| **LONGS_1BIT** | 1 | 32 | $00000001 | 32 × 1-bit samples per long |
| **LONGS_2BIT** | 2 | 16 | $00000003 | 16 × 2-bit samples per long |
| **LONGS_4BIT** | 4 | 8 | $0000000F | 8 × 4-bit samples per long |
| **LONGS_8BIT** | 8 | 4 | $000000FF | 4 × 8-bit samples per long |
| **LONGS_16BIT** | 16 | 2 | $0000FFFF | 2 × 16-bit samples per long |
| **WORDS_1BIT** | 1 | 16 | $00000001 | 16 × 1-bit samples per word (lower 16 bits) |
| **WORDS_2BIT** | 2 | 8 | $00000003 | 8 × 2-bit samples per word |
| **WORDS_4BIT** | 4 | 4 | $0000000F | 4 × 4-bit samples per word |
| **WORDS_8BIT** | 8 | 2 | $000000FF | 2 × 8-bit samples per word |
| **BYTES_1BIT** | 1 | 8 | $00000001 | 8 × 1-bit samples per byte (lower 8 bits) |
| **BYTES_2BIT** | 2 | 4 | $00000003 | 4 × 2-bit samples per byte |
| **BYTES_4BIT** | 4 | 2 | $0000000F | 2 × 4-bit samples per byte |

### 6.4 SetPack Method

```pascal
procedure TDebugDisplayForm.SetPack(val: integer; alt, signx: boolean);
var
  i: integer;
begin
  vPackAlt := alt;
  vPackSignx := signx;
  if val = 0 then i := 32 shl 8 + 1 else i := PackDef[val];
  if val = 0 then vPackMask := $FFFFFFFF else vPackMask := 1 shl (i shr 8 and $FF) - 1;
  vPackShift := i shr 8 and $FF;
  vPackCount := i and $FF;
end;
```

**Source Location**: Lines 4138-4148

**Processing**:
1. Extract packing definition from PackDef table
2. Calculate bit mask: `(1 << shift) - 1`
3. Store shift amount (bits per sample)
4. Store count (samples per packed value)

**Special Case** (`val = 0`):
- Unpacked mode: 1 sample per long, all 32 bits
- Mask: $FFFFFFFF
- Shift: 32
- Count: 1

### 6.5 NewPack Function

```pascal
function TDebugDisplayForm.NewPack: integer;
begin
  Result := val;
  if vPackAlt and (vPackShift <= 1) then Result := Result shr 1 and $55555555 or Result shl 1 and $AAAAAAAA;
  if vPackAlt and (vPackShift <= 2) then Result := Result shr 2 and $33333333 or Result shl 2 and $CCCCCCCC;
  if vPackAlt and (vPackShift <= 4) then Result := Result shr 4 and $0F0F0F0F or Result shl 4 and $F0F0F0F0;
end;
```

**Source Location**: Lines 4150-4156

**Purpose**: Read packed value from element stream and optionally apply alternate bit ordering.

**Alternate Bit Ordering** (vPackAlt = true):
- Swaps adjacent bits: bits 0↔1, 2↔3, 4↔5, etc.
- Swaps adjacent 2-bit groups: bits 1:0↔3:2, 5:4↔7:6, etc.
- Swaps adjacent 4-bit nibbles: bits 3:0↔7:4, 11:8↔15:12, etc.

**Example** (LONGS_1BIT with ALT):
```
Original: bit31 bit30 ... bit1 bit0
After:    bit30 bit31 ... bit0 bit1
```

### 6.6 UnPack Function

```pascal
function TDebugDisplayForm.UnPack(var v: integer): integer;
begin
  Result := v and vPackMask;
  v := v shr vPackShift;
  if vPackSignx and (Result shr (vPackShift - 1) and 1 = 1) then
    Result := Result or ($FFFFFFFF xor vPackMask);
end;
```

**Source Location**: Lines 4158-4163

**Processing**:
1. Extract sample: `Result = v & mask`
2. Shift packed value for next sample: `v = v >> shift`
3. If sign extension enabled and MSB set: sign-extend to 32 bits

**Sign Extension** (vPackSignx = true):
```
Example (4-bit signed):
  Value: $F (binary: 1111)
  MSB = 1 (bit 3)
  Sign extend: $FFFFFFFF (treat as -1)

  Value: $7 (binary: 0111)
  MSB = 0 (bit 3)
  No extension: $00000007 (treat as +7)
```

### 6.7 Packing Usage Example

**Configuration**:
```
LOGIC LONGS_1BIT 'CLK' 'DATA' 'RDY' 'ACK'
```

**P2 Code** (Spin2):
```spin2
' Sample 4 channels (bits 0-3 of OUTA)
sample := OUTA & $F

' Send to PC
DEBUG("`logic sample)
```

**Serial Transmission**:
- Each long contains 32 samples of the 4-bit value
- Sample 0 in bits 0-3, sample 1 in bits 4-7, etc.

**PC Reception**:
```pascal
v := NewPack;               // Read packed long from stream
for i := 1 to 32 do         // vPackCount = 32 for LONGS_1BIT
begin
  sample := UnPack(v);      // Extract 1-bit sample
  LogicSampleBuff[SamplePtr] := sample;
  SamplePtr := (SamplePtr + 1) and LogicPtrMask;
end;
```

---

## 7. Channel Configuration

The LOGIC window supports two channel modes: **single-bit** channels and **multi-bit range** channels.

### 7.1 Channel Configuration Syntax

**String Element Format**:
```
'label' {count} {RANGE} {color}
```

**Parameters**:
- `label`: Channel name (displayed on left side)
- `count`: Number of channels (default: 1)
- `RANGE`: Keyword for multi-bit range mode
- `color`: Waveform color (RGB24, default: cycle through DefaultScopeColors)

### 7.2 Single-Bit Channels

**Single Channel**:
```
'CLK'
```

Creates one channel:
- Label: "CLK"
- Bits: 1
- Color: DefaultScopeColors[0] (lime green)

**Multiple Single-Bit Channels**:
```
'DATA' 8
```

Creates 8 channels:
- Labels: "DATA 0", "DATA 1", ..., "DATA 7"
- Bits: 1 each
- Color: All same color

**Configuration Code** (lines 975-1005):
```pascal
if NextStr then
begin
  s := PChar(val);
  if vLogicIndex < LogicChannels then
  begin
    vLogicLabel[vLogicIndex] := s;
    if not KeyValWithin(v, 1, LogicChannels) then v := 1;
    MaxLimit(v, LogicChannels - vLogicIndex);
    isRange := KeyIs(key_range);
    if not KeyColor(color) then color := DefaultScopeColors[vLogicIndex mod 8];

    for i := 0 to v - 1 do
    begin
      vLogicColor[vLogicIndex + i] := color;
      if isRange then
      begin
        // Range mode (see below)
      end
      else
      begin
        vLogicBits[vLogicIndex + i] := 1;
        if v > 1 then
          if i = 0 then vLogicLabel[vLogicIndex] := s + ' 0'
          else vLogicLabel[vLogicIndex + i] := IntToStr(i);
      end;
    end;
    Inc(vLogicIndex, v);
  end;
end;
```

### 7.3 Multi-Bit Range Channels

**Range Syntax**:
```
'VALUE' 8 RANGE
```

Creates a **single multi-bit channel**:
- Label: "VALUE"
- Bits: 8
- Rendered as analog-style waveform (value mapped to vertical position)

**Configuration Code** (range mode, lines 985-994):
```pascal
if isRange then
begin
  vLogicBits[vLogicIndex + i] := v;
  if i = 1 then
  begin
    vLogicLabel[vLogicIndex + 1] := IntToStr(v);
    vLogicColor[vLogicIndex + 1] := vLogicColor[vLogicIndex + 1] shr 2 and $3F3F3F;
  end;
  if i > 1 then vLogicLabel[vLogicIndex + i] := '';
end
```

**Special Processing**:
- First channel (i=0): Full label, full color
- Second channel (i=1): Label = bit count (e.g., "8"), dimmed color
- Remaining channels (i>1): Empty label

**Vertical Allocation**:
- Range channels occupy multiple vertical rows equal to bit count
- Example: 8-bit range uses 8 × ChrHeight vertical space

### 7.4 Channel Color Cycling

**Default Colors**:
```pascal
DefaultScopeColors: array[0..7] of integer = (
  clLime,      // $00FF00 - Lime green
  clRed,       // $FF0000 - Red
  clCyan,      // $00FFFF - Cyan
  clYellow,    // $FFFF00 - Yellow
  clMagenta,   // $FF00FF - Magenta
  clBlue,      // $7F7FFF - Blue
  clOrange,    // $FFA500 - Orange
  clOlive      // $808000 - Olive
);
```

**Source Location**: Line 241

**Color Assignment**:
```pascal
color := DefaultScopeColors[vLogicIndex mod 8];
```

Channels cycle through the 8 default colors.

### 7.5 Configuration Examples

**Example 1: Simple 8-Channel Logic**:
```
LOGIC 'CLK' 'DATA' 'ADDR' 'CS' 'WR' 'RD' 'INT' 'RST'
```

Result:
- 8 single-bit channels
- Labels: CLK, DATA, ADDR, CS, WR, RD, INT, RST
- Colors: cycle through DefaultScopeColors

**Example 2: 8-Bit Data Bus**:
```
LOGIC 'D' 8
```

Result:
- 8 single-bit channels
- Labels: D 0, D 1, D 2, ..., D 7
- All same color

**Example 3: 8-Bit Range Value**:
```
LOGIC 'ADC' 8 RANGE
```

Result:
- 1 multi-bit channel (8 bits)
- Label: ADC (with "8" on second row)
- Rendered as analog waveform (0-255 mapped to vertical height)

**Example 4: Mixed Configuration**:
```
LOGIC 'CLK' 'COUNTER' 8 RANGE $FF0000 'BUSY'
```

Result:
- Channel 0: CLK (single-bit, lime)
- Channels 1-8: COUNTER (8-bit range, red)
- Channel 9: BUSY (single-bit, yellow)

---

## 8. Sample Processing

### 8.1 LOGIC_Update Method

```pascal
procedure TDebugDisplayForm.LOGIC_Update;
var
  i, t, v: integer;
begin
  while not NextEnd do
  begin
    if NextStr then Break;   // string not allowed
    if NextKey then
    case val of
      key_trigger:  // Process trigger command (see Section 9)
      key_holdoff:  // Process holdoff command
      key_clear:    // Clear display and buffer
      key_save:     // Save bitmap to file
      key_pc_key:   // Send keyboard state
      key_pc_mouse: // Send mouse position
    end
    else
    while NextNum do
    begin
      // Get channel sample(s)
      v := NewPack;
      for i := 1 to vPackCount do
      begin
        // Enter sample into buffer
        LogicSampleBuff[SamplePtr] := UnPack(v);
        SamplePtr := (SamplePtr + 1) and LogicPtrMask;
        if SamplePop < vSamples then Inc(SamplePop);

        // Trigger processing (see Section 9)
      end;
    end;
  end;
end;
```

**Source Location**: Lines 1034-1106

### 8.2 Sample Ingestion Flow

**Step 1: Read Packed Value**
```pascal
v := NewPack;
```

Reads next numeric element from stream and applies alternate bit ordering if enabled.

**Step 2: Unpack Samples**
```pascal
for i := 1 to vPackCount do
begin
  sample := UnPack(v);
  // ...
end;
```

Extracts `vPackCount` samples from the packed value.

**Step 3: Store in Circular Buffer**
```pascal
LogicSampleBuff[SamplePtr] := UnPack(v);
SamplePtr := (SamplePtr + 1) and LogicPtrMask;
if SamplePop < vSamples then Inc(SamplePop);
```

- Store sample at current pointer position
- Advance pointer with wraparound (AND with LogicPtrMask)
- Increment fill level until buffer is full

**Buffer Fill States**:
- `SamplePop = 0`: Empty buffer
- `0 < SamplePop < vSamples`: Partially filled
- `SamplePop = vSamples`: Full buffer (ready for trigger check)

### 8.3 Sample to Channel Mapping

**Bit Extraction**:
```pascal
// From LOGIC_Draw (line 1136)
v := (LogicSampleBuff[(SamplePtr - k - 1) and LogicPtrMask] shr j) and mask;
```

**Variables**:
- `k`: Sample index (0 = most recent, SamplePop-1 = oldest)
- `j`: Channel start bit (0 for channel 0, increments by vLogicBits[])
- `mask`: Bit mask = `(1 << vLogicBits[j]) - 1`

**Example** (4 channels: 1-bit CLK, 8-bit DATA, 1-bit CS, 1-bit WR):

```
Sample value: $00000ABC (binary: ...1010 10111100)

Channel 0 (CLK):  bit 0    = (sample >> 0) & 0x1  = 0
Channel 1 (DATA): bits 1-8 = (sample >> 1) & 0xFF = $5E (10111100 >> 1 = 01011110)
Channel 2 (CS):   bit 9    = (sample >> 9) & 0x1  = 1
Channel 3 (WR):   bit 10   = (sample >> 10) & 0x1 = 0
```

### 8.4 Command Processing

**CLEAR Command**:
```pascal
key_clear:
begin
  vTriggered := False;    // Reset trigger indicator
  ClearBitmap;            // Fill canvas with background color
  BitmapToCanvas(0);      // Update display
  SamplePop := 0;         // Reset fill level
  vRateCount := 0;        // Reset rate counter
end;
```

**Purpose**: Reset display and buffer state.

**SAVE Command**:
```pascal
key_save:
  KeySave;
```

Saves current display to BMP file (see PLOT documentation for KeySave details).

**PC_KEY / PC_MOUSE Commands**:
```pascal
key_pc_key:   SendKeyPress;
key_pc_mouse: SendMousePos;
```

Sends user input feedback to P2 (see PLOT documentation for details).

---

## 9. Trigger System

The LOGIC window implements an edge-sensitive trigger system similar to hardware logic analyzers.

### 9.1 Trigger Configuration

**TRIGGER Command Syntax**:
```
TRIGGER mask match {offset}
```

**Parameters**:
- `mask`: Bit mask for trigger channels (32-bit)
- `match`: Expected value on masked channels (32-bit)
- `offset`: Trigger position in display (0..vSamples-1) (default: vSamples/2)

**Configuration Code** (lines 1043-1049):
```pascal
key_trigger:
begin
  vArmed := False;
  if not KeyVal(vTriggerMask) then Continue;
  if not KeyVal(vTriggerMatch) then Continue;
  KeyValWithin(vTriggerOffset, 0, vSamples - 1);
end;
```

**Example**:
```
TRIGGER $3 $1 16
```

- Mask: $3 (bits 0-1)
- Match: $1 (bit 0 high, bit 1 low)
- Offset: 16 (trigger appears 16 samples from left edge)

### 9.2 Trigger Detection Algorithm

**Code** (lines 1078-1099):
```pascal
// Trigger enabled?
vTriggered := False;
if vTriggerMask <> 0 then
begin
  if SamplePop <> vSamples then Continue;    // Wait for full buffer

  t := LogicSampleBuff[(SamplePtr - vTriggerOffset) and LogicPtrMask];

  if vArmed then
  begin
    // Armed: check for match
    if ((t xor vTriggerMatch) and vTriggerMask) = 0 then
    begin
      vTriggered := True;
      vArmed := False;
    end;
  end
  else
  begin
    // Not armed: check for non-match (to detect edge)
    if ((t xor vTriggerMatch) and vTriggerMask) <> 0 then
      vArmed := True;
  end;

  if vHoldOffCount > 0 then Dec(vHoldOffCount);
  if not vTriggered or (vHoldOffCount > 0) then Continue;
  vHoldOffCount := vHoldOff;

  if RateCycle then LOGIC_Draw;
end
```

**State Machine**:

```
┌─────────────┐
│   DISARMED  │ <──────────────┐
└──────┬──────┘                │
       │                       │
       │ Sample ≠ Match        │ Trigger Match
       ▼                       │
┌─────────────┐                │
│    ARMED    │ ───────────────┘
└─────────────┘
```

**Step-by-Step**:

1. **Wait for Full Buffer**: Skip processing until SamplePop = vSamples
2. **Read Sample at Trigger Position**: `t = LogicSampleBuff[(SamplePtr - vTriggerOffset) and LogicPtrMask]`
3. **Check Arming State**:
   - **If ARMED**: Check if sample matches trigger condition
     - Match: Set vTriggered = True, disarm
     - No match: Stay armed
   - **If DISARMED**: Check if sample doesn't match
     - No match: Arm trigger
     - Match: Stay disarmed
4. **Holdoff Check**: If in holdoff period, suppress trigger
5. **Display Update**: If triggered and holdoff expired, call LOGIC_Draw

**Trigger Condition**:
```pascal
((sample XOR match) AND mask) = 0
```

This is true when all masked bits match the expected values.

**Example**:
```
Mask:   $00000003  (binary: ...0011) - check bits 0-1
Match:  $00000001  (binary: ...0001) - expect bit 0=1, bit 1=0

Sample: $00000001  (binary: ...0001)
  XOR:  00000000
  AND:  00000000  = 0  → MATCH

Sample: $00000003  (binary: ...0011)
  XOR:  00000002
  AND:  00000002  ≠ 0  → NO MATCH
```

### 9.3 Edge Detection (Arming)

The trigger requires an **edge** (transition) to the match condition, not just the condition being true.

**Sequence**:
1. Sample doesn't match → ARM
2. Sample matches → TRIGGER
3. Disarm

This prevents continuous re-triggering on a static signal.

**Example** (trigger on rising edge of CLK):
```
Mask:  $1 (bit 0 = CLK)
Match: $1 (CLK high)

Samples:  0 0 0 0 1 1 1 0 0 1 1 0 0
Armed:    - - - A A - - - A A - - -
Trigger:  - - - - T - - - - T - - -
              ↑ ↑               ↑
              │ └─ Trigger      └─ Trigger
              └─ Arm
```

### 9.4 Holdoff System

**HOLDOFF Command**:
```
HOLDOFF count
```

**Purpose**: Prevent re-triggering for `count` samples after a trigger event.

**Configuration** (lines 1050-1051):
```pascal
key_holdoff:
  if KeyValWithin(vHoldOff, 2, LogicSets) then vHoldOffCount := 0;
```

**Processing** (lines 1096-1098):
```pascal
if vHoldOffCount > 0 then Dec(vHoldOffCount);
if not vTriggered or (vHoldOffCount > 0) then Continue;
vHoldOffCount := vHoldOff;
```

**Behavior**:
1. After trigger event: `vHoldOffCount = vHoldOff`
2. Each sample: Decrement vHoldOffCount
3. Suppress triggers while vHoldOffCount > 0

**Use Case**: Prevent triggering on noise or high-frequency signals.

**Example**:
```
HOLDOFF 64
```

After a trigger, ignore the next 64 samples before allowing another trigger.

### 9.5 Trigger Offset

**Purpose**: Control where the trigger event appears in the display.

**Values**:
- `0`: Trigger at left edge (show what happens after trigger)
- `vSamples/2`: Trigger at center (show before and after) - **default**
- `vSamples-1`: Trigger at right edge (show what led up to trigger)

**Sample Selection** (line 1083):
```pascal
t := LogicSampleBuff[(SamplePtr - vTriggerOffset) and LogicPtrMask];
```

**Visualization** (vSamples = 32, vTriggerOffset = 16):

```
Buffer (newest → oldest):
[31][30][29]...[17][16][15]...[1][0]
                     ↑
                  Trigger point
                  (SamplePtr - 16)

Display:
[0][1]...[15][16][17]...[30][31]
             ↑
          Trigger at center
```

### 9.6 Trigger Disabled Mode

When `vTriggerMask = 0`:
```pascal
// Trigger not enabled (lines 1101-1102)
else if RateCycle then LOGIC_Draw;
```

Every sample (after rate limiting) triggers a display update.

This is **free-running mode** - continuous display updates.

---

## 10. Rendering Pipeline

### 10.1 LOGIC_Draw Method

```pascal
procedure TDebugDisplayForm.LOGIC_Draw;
var
  j, k, x, top, bot, color, colordim: integer;
  mask, v, y: int64;
  first, last: boolean;
begin
  ClearBitmap;
  j := 0;
  while j < vLogicIndex do
  begin
    // Set waveform attributes
    color := vLogicColor[j];
    colordim := color shr 2 and $3F3F3F;
    bot := (vMarginTop + vHeight - ChrHeight * j                       - ChrHeight *  3 shr 4) shl 8;
    top := (vMarginTop + vHeight - ChrHeight * (j + vLogicBits[j] - 1) - ChrHeight * 13 shr 4) shl 8;
    mask := Int64(1) shl vLogicBits[j] - 1;

    // If range waveform, draw top and bottom boundary lines
    if vLogicBits[j] > 1 then
    begin
      SmoothLine((vMarginLeft + 1) shl 8, top, (vMarginLeft + vWidth - 1) shl 8, top, $80, colordim, 255);
      SmoothLine((vMarginLeft + 1) shl 8, bot, (vMarginLeft + vWidth - 1) shl 8, bot, $80, colordim, 255);
    end;

    // Plot waveform
    for k := SamplePop - 1 downto 0 do
    begin
      first := k = SamplePop - 1;
      last := k = 0;
      x := (vMarginLeft + vWidth - (k + 1) * vSpacing) shl 8;
      v := (LogicSampleBuff[(SamplePtr - k - 1) and LogicPtrMask] shr j) and mask;
      y := v * (top - bot) div mask + bot;
      DrawLineDot(x + Ord(first) shl 8, y, color, first);
      DrawLineDot(x + (vSpacing - Ord(last)) shl 8, y, color, false);
    end;

    Inc(j, vLogicBits[j]);
  end;
  BitmapToCanvas(0);
end;
```

**Source Location**: Lines 1108-1144

### 10.2 Coordinate System

**Vertical (Y) Coordinates**:
```pascal
bot := (vMarginTop + vHeight - ChrHeight * j                       - ChrHeight *  3 shr 4) shl 8;
top := (vMarginTop + vHeight - ChrHeight * (j + vLogicBits[j] - 1) - ChrHeight * 13 shr 4) shl 8;
```

**Fixed-Point Format**: Coordinates are left-shifted by 8 bits (8.8 fixed-point) for sub-pixel precision.

**Channel Positioning**:
- Channels are stacked bottom-to-top
- Channel 0 at bottom, channel N at top
- Each channel occupies `vLogicBits[j] × ChrHeight` vertical space

**Insets**:
- `ChrHeight * 3 / 16`: Bottom inset
- `ChrHeight * 13 / 16`: Top inset

**Example** (3 channels, ChrHeight = 16):
```
Channel 2: top = 32, bot = 48
Channel 1: top = 16, bot = 32
Channel 0: top = 0,  bot = 16
```

**Horizontal (X) Coordinates**:
```pascal
x := (vMarginLeft + vWidth - (k + 1) * vSpacing) shl 8;
```

**Right-to-Left Plotting**:
- Most recent sample (k=0) at right edge
- Oldest sample (k=SamplePop-1) at left edge
- Spacing between samples: vSpacing pixels

### 10.3 Value to Y-Position Mapping

**For Single-Bit Channels** (vLogicBits[j] = 1):
```pascal
mask := Int64(1) shl vLogicBits[j] - 1;  // mask = 1
v := (sample >> j) & mask;                // v = 0 or 1
y := v * (top - bot) / mask + bot;        // y = bot (low) or top (high)
```

- `v = 0`: `y = bot` (bottom of channel area)
- `v = 1`: `y = top` (top of channel area)

**For Range Channels** (vLogicBits[j] > 1):
```pascal
mask := Int64(1) shl vLogicBits[j] - 1;  // mask = 2^n - 1 (e.g., 255 for 8-bit)
v := (sample >> j) & mask;                // v = 0..mask
y := v * (top - bot) / mask + bot;        // Linear interpolation
```

**Example** (8-bit range, top = 0, bot = 256):
```
v = 0:   y = 0 * 256 / 255 + 256 = 256 (bottom)
v = 128: y = 128 * 256 / 255 + 256 = 384 (middle)
v = 255: y = 255 * 256 / 255 + 256 = 512 (top)
```

### 10.4 Range Channel Boundary Lines

**Code** (lines 1125-1129):
```pascal
if vLogicBits[j] > 1 then
begin
  SmoothLine((vMarginLeft + 1) shl 8, top, (vMarginLeft + vWidth - 1) shl 8, top, $80, colordim, 255);
  SmoothLine((vMarginLeft + 1) shl 8, bot, (vMarginLeft + vWidth - 1) shl 8, bot, $80, colordim, 255);
end;
```

**Purpose**: Draw horizontal lines at top and bottom of range channel.

**Color**: Dimmed channel color (`color >> 2 & $3F3F3F`)

**Line Thickness**: $80 (fixed-point) = 128/256 = 0.5 pixels

### 10.5 DrawLineDot Method

```pascal
procedure TDebugDisplayForm.DrawLineDot(x, y, color: integer; first: boolean);
begin
  if (vLineSize > 0) and not first then
    SmoothLine(vPixelX, vPixelY, x, y, vLineSize shl 6, color, $FF);
  if (vDotSize > 0) then
    SmoothDot(x, y, vDotSize shl 7, color, $FF);
  vPixelX := x;
  vPixelY := y;
end;
```

**Source Location**: Lines 3415-3423

**Processing**:
1. **Draw Line** (if vLineSize > 0 and not first point):
   - Connect previous point (vPixelX, vPixelY) to current point (x, y)
   - Line thickness: `vLineSize << 6` (convert to fixed-point with scaling)
2. **Draw Dot** (if vDotSize > 0):
   - Render circular dot at current point
   - Dot diameter: `vDotSize << 7` (convert to fixed-point with scaling)
3. **Update State**: Store current point as previous for next iteration

**Line/Dot Modes**:
- `vDotSize = 0, vLineSize > 0`: Connected lines only
- `vDotSize > 0, vLineSize = 0`: Dots only (no connections)
- Both > 0: Lines with dots at sample points
- Both = 0: No rendering (error condition, caught in SCOPE_Configure)

### 10.6 Waveform Rendering Loop

**Code** (lines 1131-1140):
```pascal
for k := SamplePop - 1 downto 0 do
begin
  first := k = SamplePop - 1;
  last := k = 0;
  x := (vMarginLeft + vWidth - (k + 1) * vSpacing) shl 8;
  v := (LogicSampleBuff[(SamplePtr - k - 1) and LogicPtrMask] shr j) and mask;
  y := v * (top - bot) div mask + bot;
  DrawLineDot(x + Ord(first) shl 8, y, color, first);
  DrawLineDot(x + (vSpacing - Ord(last)) shl 8, y, color, false);
end;
```

**Processing**:

1. **Loop Through Samples**: From oldest (k = SamplePop-1) to newest (k = 0)

2. **Calculate X Position**:
   ```pascal
   x := (vMarginLeft + vWidth - (k + 1) * vSpacing) shl 8;
   ```

3. **Extract Sample Value**:
   ```pascal
   v := (LogicSampleBuff[(SamplePtr - k - 1) and LogicPtrMask] shr j) and mask;
   ```
   - Read sample from circular buffer
   - Shift right by channel bit offset (j)
   - Mask to extract channel bits

4. **Map Value to Y Position**:
   ```pascal
   y := v * (top - bot) div mask + bot;
   ```

5. **Draw Two Points Per Sample**:
   - **Left point**: `DrawLineDot(x + Ord(first) << 8, y, color, first)`
     - If first sample: x offset by 256 (1 pixel)
     - Otherwise: x offset by 0
   - **Right point**: `DrawLineDot(x + (vSpacing - Ord(last)) << 8, y, color, false)`
     - If last sample: x offset by (vSpacing - 1) pixels
     - Otherwise: x offset by vSpacing pixels

**Two-Point Rendering**:

Purpose: Create horizontal segments for single-bit waveforms and vertical transitions.

```
Example (vSpacing = 8):

Sample 0:  ────────  (value = 1, top)
Sample 1:  ────────  (value = 1, top)
Sample 2:        │   (transition)
               ───   (value = 0, bot)

Points:
  Sample 0 left:  x=0, y=top
  Sample 0 right: x=7, y=top
  Sample 1 left:  x=8, y=top
  Sample 1 right: x=15, y=top
  Sample 2 left:  x=16, y=bot
  Sample 2 right: x=23, y=bot

Lines drawn:
  (0,top) → (7,top)      // Sample 0 horizontal
  (7,top) → (8,top)      // Connection to sample 1
  (8,top) → (15,top)     // Sample 1 horizontal
  (15,top) → (16,bot)    // Vertical transition
  (16,bot) → (23,bot)    // Sample 2 horizontal
```

### 10.7 Display Update

**Code** (line 1143):
```pascal
BitmapToCanvas(0);
```

**Purpose**: Copy render target (Bitmap[0]) to display buffer (Bitmap[1]) and update canvas.

**Double-Buffering**:
- Prevents flicker during rendering
- All drawing happens on Bitmap[0]
- Only completed frames are copied to Bitmap[1] for display

---

## 11. Timing and Rate Control

### 11.1 Rate Limiting

**Purpose**: Control display update frequency independently of sample rate.

**Rate Parameter**:
```
RATE divisor
```

**Range**: 1 to 2048

**Behavior**:
```pascal
vRateCount := 0;              // Reset counter
vRate := divisor;             // Set divisor

// In RateCycle function:
Inc(vRateCount);
if vRateCount = vRate then
begin
  vRateCount := 0;
  Result := True;             // Trigger display update
end
else Result := False;
```

**Effect**:
- `RATE 1`: Update display every sample (no limiting)
- `RATE 10`: Update display every 10th sample
- `RATE 100`: Update display every 100th sample

**Use Cases**:
- Reduce CPU usage for high-speed sampling
- Slow down display updates for visual clarity
- Match display rate to screen refresh rate

### 11.2 RateCycle Function

```pascal
function TDebugDisplayForm.RateCycle: boolean;
begin
  Inc(vRateCount);
  if vRateCount = vRate then
  begin
    vRateCount := 0;
    Result := True;
  end
  else Result := False;
end;
```

**Source Location**: Lines 3071-3080

**Usage**:
```pascal
if RateCycle then LOGIC_Draw;
```

Called for each sample or trigger event to determine if display should update.

### 11.3 Sample Buffer Timing

**Buffer Fill**:
```pascal
if SamplePop < vSamples then Inc(SamplePop);
```

- Buffer fills linearly: 0 → 1 → 2 → ... → vSamples
- Once full, stays at vSamples (circular buffer overwrites oldest)

**First Display Update**:
- Trigger mode: Waits for buffer to fill AND trigger condition
- Free-running mode: Updates as soon as RateCycle returns true

**Continuous Operation**:
- After first update, buffer is always full (SamplePop = vSamples)
- New samples overwrite oldest samples
- Display updates on trigger or rate cycle

---

## 12. User Commands

### 12.1 Configuration Commands

| Command | Parameters | Purpose |
|---------|------------|---------|
| `TITLE` | 'string' | Set window title |
| `POS` | x y | Set window position |
| `SAMPLES` | count | Set horizontal resolution (4-2047) |
| `SPACING` | pixels | Set pixel spacing between samples (1-32) |
| `RATE` | divisor | Set display update rate (1-2048) |
| `DOTSIZE` | pixels | Set dot diameter (0-32, 0=no dots) |
| `LINESIZE` | pixels | Set line thickness (1-32) |
| `TEXTSIZE` | size | Set label font size (6-200) |
| `COLOR` | back grid | Set background and grid colors |
| `HIDEXY` | - | Hide mouse coordinates |
| `LONGS_1BIT` | - | Set packing mode (see Section 6) |
| ... other packing modes ... | - | |

### 12.2 Runtime Commands

| Command | Parameters | Purpose |
|---------|------------|---------|
| `TRIGGER` | mask match {offset} | Configure trigger system |
| `HOLDOFF` | count | Set holdoff count (2-2048) |
| `CLEAR` | - | Clear display and reset buffer |
| `SAVE` | {filename} | Save display to BMP file |
| `PC_KEY` | - | Request keyboard state |
| `PC_MOUSE` | - | Request mouse position/color |

### 12.3 Sample Data Format

**Numeric Elements**:

Samples are sent as numeric elements in the element stream:

```
ele_num: sample_value
ele_num: sample_value
...
ele_end
```

**Packing**:

Samples are packed according to the configured packing mode. See Section 6 for packing details.

---

## 13. Performance Characteristics

### 13.1 Memory Usage

**Sample Buffer**:
```
LogicSampleBuff: 2048 samples × 4 bytes = 8 KB
```

**Channel Configuration**:
```
vLogicLabel: 32 strings × ~20 bytes avg = ~640 bytes
vLogicColor: 32 × 4 bytes = 128 bytes
vLogicBits:  32 × 1 byte = 32 bytes
Total: ~800 bytes
```

**Display Bitmaps**:
```
Typical size: 256×256 pixels × 4 bytes (RGBA) = 256 KB
Bitmap[0] + Bitmap[1] = 512 KB
```

**Total**: ~520 KB (typical configuration)

### 13.2 Rendering Performance

**Factors Affecting Performance**:

1. **Number of Channels**: More channels = more DrawLineDot calls
2. **Sample Count**: More samples = longer loop
3. **Line/Dot Rendering**: Anti-aliased rendering is expensive
4. **Rate Limiting**: Higher rate = more frequent updates

**Rendering Cost** (per LOGIC_Draw call):
```
Channels × Samples × 2 DrawLineDot calls
```

**Example** (8 channels, 256 samples):
```
8 × 256 × 2 = 4096 DrawLineDot calls
```

**Optimization**:
- Use RATE limiting to reduce update frequency
- Reduce vSamples for fewer samples per frame
- Increase vSpacing to fit more samples in less width
- Use vLineSize=0 and vDotSize=0 for fastest rendering (error condition, not recommended)

### 13.3 Serial Bandwidth

**Unpacked Transmission**:
```
1 sample per long = 4 bytes per sample
256 samples = 1024 bytes
```

**Packed Transmission** (LONGS_1BIT):
```
32 samples per long = 0.125 bytes per sample
256 samples = 32 bytes
```

**Bandwidth Savings**:
```
Unpacked: 1024 bytes
Packed (LONGS_1BIT): 32 bytes
Reduction: 32× (97% savings)
```

**Recommendation**: Always use appropriate packing mode for data width.

---

## 14. Comparison with Other Display Types

### 14.1 LOGIC vs. SCOPE

**LOGIC Advantages**:
- Digital signal visualization (binary waveforms)
- Up to 32 channels
- Multi-bit range mode
- Edge-sensitive triggering
- Designed for discrete signals

**SCOPE Advantages**:
- Analog signal visualization (continuous waveforms)
- Auto-ranging (automatic Y-scale)
- Vertical offset and grid control
- Level-sensitive triggering
- Designed for continuous signals

**Use Cases**:
- **LOGIC**: Digital I/O, communication protocols, state machines
- **SCOPE**: ADC values, sensor readings, analog signals

### 14.2 LOGIC vs. BITMAP

**LOGIC Advantages**:
- Automatic waveform rendering
- Channel labeling and organization
- Trigger system
- Fixed horizontal time base

**BITMAP Advantages**:
- Pixel-perfect control
- Multiple color modes
- Trace patterns (waterfall, etc.)
- Arbitrary pixel positioning

**Use Cases**:
- **LOGIC**: Time-domain signal analysis
- **BITMAP**: Raster graphics, color-mapped data, custom visualizations

### 14.3 Common Features

All display types share:
- Serial communication protocol
- Element array parsing
- Data packing system (same 12 modes)
- Double-buffered rendering
- User input feedback (PC_KEY, PC_MOUSE)
- SAVE command for bitmap export

---

## 15. Usage Examples

### 15.1 Basic Logic Analyzer

**Configuration**:
```
LOGIC SAMPLES 64 SPACING 4 'CLK' 'DATA' 'CS' 'WR'
```

**P2 Code** (Spin2):
```spin2
debug(`logic `{OUTA & $F})

' Or in a loop:
repeat
  value := OUTA & $F
  debug(`logic `value)
```

**Result**:
- 4 channels: CLK, DATA, CS, WR
- 64 samples displayed
- 4 pixels between samples
- Free-running (no trigger)

### 15.2 Triggered Capture

**Configuration**:
```
LOGIC SAMPLES 128 'CS' 'CLK' 'MOSI' 'MISO' TRIGGER $1 $1 64
```

**Trigger**:
- Mask: $1 (bit 0 = CS)
- Match: $1 (CS high)
- Offset: 64 (trigger at center)

**Behavior**:
- Display updates when CS goes high
- Shows 64 samples before and after CS edge
- Ideal for capturing SPI transactions

### 15.3 Multi-Bit Range

**Configuration**:
```
LOGIC SAMPLES 256 'ADC' 8 RANGE $FF0000
```

**P2 Code**:
```spin2
repeat
  value := adc_read()      ' Read 8-bit ADC
  debug(`logic `value)
```

**Result**:
- Single 8-bit range channel
- Value 0-255 mapped to vertical position
- Red waveform ($FF0000)
- Appears as analog-style waveform

### 15.4 Mixed Configuration

**Configuration**:
```
LOGIC SAMPLES 128 SPACING 2
      'CLK'
      'ADDR' 8 $FFFF00
      'DATA' 8 RANGE $00FF00
      'CS' 'WR' 'RD'
```

**Channels**:
- 0: CLK (single-bit, lime)
- 1-8: ADDR (8 single-bit channels, yellow)
- 9: DATA (8-bit range, green)
- 10: CS (single-bit, cyan)
- 11: WR (single-bit, yellow)
- 12: RD (single-bit, magenta)

**Total**: 13 channels

### 15.5 High-Speed Capture with Rate Limiting

**Configuration**:
```
LOGIC SAMPLES 512 RATE 100 'D0' 'D1' 'D2' 'D3'
```

**P2 Code** (high-speed loop):
```spin2
repeat
  value := OUTA & $F
  debug(`logic `value)
  waitx(1)               ' Minimal delay
```

**Behavior**:
- Samples arriving at MHz rate
- Display updates every 100th sample
- Reduces CPU load on PC
- Still captures all samples (buffer is 2048 deep)

### 15.6 Packed Data Transmission

**Configuration**:
```
LOGIC LONGS_1BIT SAMPLES 256 'D' 4
```

**P2 Code**:
```spin2
' Pack 32 4-bit samples into one long
samples := 0
repeat 32
  value := OUTA & $F
  samples := (samples << 4) | value
  waitx(1000)

' Send packed long
debug(`logic `samples)
```

**Efficiency**:
- 32 samples per transmission
- 128 bytes → 4 bytes (32× reduction)

---

## 16. Implementation Details

### 16.1 Element Array Protocol

**Sample Transmission**:
```
ele_num: packed_value_1
ele_num: packed_value_2
...
ele_end
```

**Unpacking Loop** (lines 1068-1104):
```pascal
while NextNum do
begin
  v := NewPack;
  for i := 1 to vPackCount do
  begin
    LogicSampleBuff[SamplePtr] := UnPack(v);
    SamplePtr := (SamplePtr + 1) and LogicPtrMask;
    // ... trigger processing ...
  end;
end;
```

### 16.2 Circular Buffer Mathematics

**Write Index**:
```pascal
SamplePtr := (SamplePtr + 1) and LogicPtrMask;
```

Equivalent to:
```pascal
SamplePtr := (SamplePtr + 1) % LogicSets;
```

But faster using bitwise AND (LogicPtrMask = 2047 = $7FF).

**Read Index** (k samples back):
```pascal
index := (SamplePtr - k - 1) and LogicPtrMask;
```

Handles wraparound correctly:
```
SamplePtr = 10, k = 15:
  index = (10 - 15 - 1) & 2047 = (-6) & 2047 = 2042
```

### 16.3 Fixed-Point Coordinate System

**8.8 Fixed-Point**:
```
Integer part: bits 31-8 (24 bits)
Fractional part: bits 7-0 (8 bits)

Example:
  256 (decimal) = $00000100 (fixed) = 1.0 pixels
  384 (decimal) = $00000180 (fixed) = 1.5 pixels
  512 (decimal) = $00000200 (fixed) = 2.0 pixels
```

**Conversion**:
```pascal
// Integer to fixed-point
fixed := integer shl 8;

// Fixed-point to integer (truncate)
integer := fixed shr 8;

// Fixed-point to integer (round)
integer := (fixed + 128) shr 8;
```

### 16.4 Color Dimming

**Dimmed Color Calculation** (line 1120):
```pascal
colordim := color shr 2 and $3F3F3F;
```

**Effect**: Divide each RGB component by 4.

**Example**:
```
Original: $FF0000 (red = 255, green = 0, blue = 0)
  >> 2:   $3F0000
  & $3F3F3F: $3F0000 (red = 63, green = 0, blue = 0)

Result: 25% intensity
```

### 16.5 Anti-Aliased Line/Dot Rendering

**SmoothLine**:
- Bresenham-style algorithm with sub-pixel accuracy
- Perpendicular distance calculation
- Gamma-corrected alpha blending

**SmoothDot**:
- Distance from center calculation
- Circular coverage based on radius
- Gamma-corrected alpha blending

**Performance Impact**:
- Higher quality than simple pixel drawing
- ~10-100× slower than non-anti-aliased rendering
- Acceptable for typical channel/sample counts

---

## 17. Element Array Protocol Specification

### 17.1 Protocol Overview

The LOGIC display receives configuration and sample data through an **element array protocol** that uses parallel arrays of types and values. This protocol enables flexible data transmission while maintaining ASCII compatibility.

**Element Storage** (GlobalUnit.pas:126-127):
```pascal
DebugDisplayType:  array[0..DebugDisplayLimit - 1] of integer;
DebugDisplayValue: array[0..DebugDisplayLimit - 1] of integer;
```

**Capacity**: 1100 elements per message (DebugDisplayLimit = 1100)

### 17.2 Element Types

**Type Constants** (DebugDisplayUnit.pas:15-20):
```pascal
ele_end = 0;   // End of element array
ele_key = 3;   // Configuration keyword/command
ele_num = 4;   // Numeric data value
ele_str = 5;   // String data (pointer to PChar)
```

**Type Encoding**:
- Each element has a type (stored in DebugDisplayType array)
- Each element has a value (stored in DebugDisplayValue array)
- Arrays are traversed in parallel using parser functions

### 17.3 Parser Functions

**NextKey** - Check for and consume keyword element:
```pascal
function NextKey: boolean;
begin
  Result := (ElementPtr < ElementEnd) and (DebugDisplayType[ElementPtr] = ele_key);
  if Result then
  begin
    val := DebugDisplayValue[ElementPtr];
    Inc(ElementPtr);
  end;
end;
```

**NextNum** - Check for and consume numeric element:
```pascal
function NextNum: boolean;
begin
  Result := (ElementPtr < ElementEnd) and (DebugDisplayType[ElementPtr] = ele_num);
  if Result then
  begin
    val := DebugDisplayValue[ElementPtr];
    Inc(ElementPtr);
  end;
end;
```

**NextStr** - Check for and consume string element:
```pascal
function NextStr: boolean;
begin
  Result := (ElementPtr < ElementEnd) and (DebugDisplayType[ElementPtr] = ele_str);
  if Result then
  begin
    val := DebugDisplayValue[ElementPtr];  // Pointer to PChar
    Inc(ElementPtr);
  end;
end;
```

**NextEnd** - Check if end reached:
```pascal
function NextEnd: boolean;
begin
  Result := (ElementPtr >= ElementEnd) or (DebugDisplayType[ElementPtr] = ele_end);
end;
```

**Source Location**: Lines 4101-4131 in DebugDisplayUnit.pas

### 17.4 LOGIC Configuration Message Example

**Basic Configuration**:
```
Element Array:
[0] type=ele_key   value=key_samples     → SAMPLES
[1] type=ele_num   value=256             → horizontal resolution
[2] type=ele_key   value=key_spacing     → SPACING
[3] type=ele_num   value=2               → vertical pixel spacing
[4] type=ele_key   value=key_longs_1bit  → LONGS_1BIT
[5] type=ele_str   value=<ptr>           → 'CLK'
[6] type=ele_num   value=$FF0000         → red color
[7] type=ele_str   value=<ptr>           → 'DATA'
[8] type=ele_num   value=$00FF00         → green color
[9] type=ele_end   value=0               → end marker
```

**Parsing Flow**:
```pascal
LOGIC_Configure:
  NextKey → key_samples → NextNum → 256 → vSamples := 256
  NextKey → key_spacing → NextNum → 2 → vSpacing := 2
  NextKey → key_longs_1bit → SetPack(key_longs_1bit)
  NextStr → 'CLK' → vLabel[0] := 'CLK'
  NextNum → $FF0000 → vColor[0] := $FF0000
  NextStr → 'DATA' → vLabel[1] := 'DATA'
  NextNum → $00FF00 → vColor[1] := $00FF00
  NextEnd → done, vIndex := 2 (2 channels)
```

### 17.5 LOGIC Sample Data Message Example

**Binary Channels** (4 channels, LONGS_1BIT packing):
```
Element Array:
[0] type=ele_num   value=$00000001       → packed: 32 samples for ch0
[1] type=ele_num   value=$FFFFFFFF       → packed: 32 samples for ch1
[2] type=ele_num   value=$AAAA5555       → packed: 32 samples for ch2
[3] type=ele_num   value=$F0F0F0F0       → packed: 32 samples for ch3
[4] type=ele_end   value=0
```

**Unpacking**:
```pascal
LOGIC_Update:
  NextNum → $00000001
    vPackCount = 32 (LONGS_1BIT mode)
    for i := 1 to 32 do
      UnPack → bit value → Store in SampleBuff[SamplePtr * 32 + 0]
  NextNum → $FFFFFFFF
    for i := 1 to 32 do
      UnPack → bit value → Store in SampleBuff[SamplePtr * 32 + 1]
  NextNum → $AAAA5555
    for i := 1 to 32 do
      UnPack → bit value → Store in SampleBuff[SamplePtr * 32 + 2]
  NextNum → $F0F0F0F0
    for i := 1 to 32 do
      UnPack → bit value → Store in SampleBuff[SamplePtr * 32 + 3]
  → Complete sample set received, advance SamplePtr
```

### 17.6 RANGE Mode Configuration Example

**Multi-Bit Value Display**:
```
Element Array:
[0] type=ele_key   value=key_range       → RANGE
[1] type=ele_num   value=0               → start channel
[2] type=ele_num   value=7               → end channel (8 bits)
[3] type=ele_num   value=0               → minimum value
[4] type=ele_num   value=255             → maximum value
[5] type=ele_str   value=<ptr>           → 'Counter'
[6] type=ele_num   value=$FFFF00         → cyan color
[7] type=ele_end   value=0
```

**Effect**: Channels 0-7 displayed as analog-style waveform showing counter value from 0-255.

### 17.7 Trigger Configuration Example

**Edge Trigger on Rising Edge**:
```
Element Array:
[0] type=ele_key   value=key_trigger     → TRIGGER
[1] type=ele_num   value=$FFFFFFFF       → mask (all channels)
[2] type=ele_num   value=$00000001       → match (channel 0 = 1)
[3] type=ele_num   value=512             → position (50% pre-trigger)
[4] type=ele_num   value=10              → holdoff (prevent re-trigger)
[5] type=ele_end   value=0
```

**Trigger Logic**:
```
samples_xor = (current_sample XOR previous_sample) AND mask
trigger = ((samples_xor AND current_sample) AND match) != 0
```

### 17.8 Runtime Command Examples

**CLEAR Command**:
```
Element Array:
[0] type=ele_key   value=key_clear
[1] type=ele_end   value=0
```

**SAVE Command**:
```
Element Array:
[0] type=ele_key   value=key_save
[1] type=ele_str   value=<ptr>           → 'logic_capture.bmp'
[2] type=ele_end   value=0
```

---

## 18. Buffer Management and Timing

### 18.1 Circular Buffer Model

LOGIC uses a **circular buffer** to store the most recent samples for display:

**Sample Buffer**:
```pascal
SampleBuff: array[0..SampleSets * SampleSetSize - 1] of integer;
```

**Dimensions**:
```
SampleSets = 2048              // Number of sample sets
SampleSetSize = 32             // Channels per set
Total size = 2048 × 32 = 65,536 samples = 262,144 bytes
```

**Buffer Organization**:
```
Set 0:  [Ch0][Ch1][Ch2]...[Ch31]  (32 channel values)
Set 1:  [Ch0][Ch1][Ch2]...[Ch31]
...
Set 2047: [Ch0][Ch1][Ch2]...[Ch31]
```

### 18.2 Write Operations

**Sample Set Storage** (LOGIC_Update, lines 1259-1268):
```pascal
// Store complete sample set
Move(samp, SampleBuff[SamplePtr * SampleSetSize], SampleSetSize shl 2);

// Advance write pointer with wraparound
SamplePtr := (SamplePtr + 1) and SamplePtrMask;

// Track valid sample count
if SamplePop < SampleSets then Inc(SamplePop);
```

**Write Process**:
1. Unpack data from element array into `samp` temporary buffer
2. Copy complete sample set (32 channels) to circular buffer at SamplePtr
3. Advance SamplePtr with wraparound: `(SamplePtr + 1) and 2047`
4. Increment SamplePop until buffer is full (2048 samples)

### 18.3 Read Operations

**Display Rendering** (LOGIC_Plot):
```pascal
// Calculate starting index
start_idx := ((SamplePtr - vSamples) and SamplePtrMask) * SampleSetSize;

// Read samples for display
for sample := 0 to vSamples - 1 do
begin
  idx := ((SamplePtr - vSamples + sample) and SamplePtrMask) * SampleSetSize;
  for channel := 0 to vIndex - 1 do
    value := SampleBuff[idx + channel];
  // Render value
end;
```

**Index Calculation**:
```
idx = ((SamplePtr - vSamples + sample_offset) and 2047) × 32 + channel
```

**Components**:
- `SamplePtr`: Current write position (next slot to write)
- `vSamples`: Number of samples to display (horizontal resolution)
- `sample_offset`: Position within display window (0 to vSamples-1)
- `and 2047`: Circular wraparound
- `× 32`: Convert set index to element index
- `+ channel`: Offset to specific channel (0-31)

### 18.4 Trigger Detection Timing

**Trigger Check** (LOGIC_Update, lines 1270-1284):
```pascal
if vTrigger then
begin
  // Check for edge trigger
  samples_xor := (samp_current xor samp_previous) and vTriggerMask;
  trigger_detected := ((samples_xor and samp_current) and vTriggerMatch) <> 0;

  if trigger_detected then
  begin
    if HoldoffCount = 0 then
    begin
      // Trigger fired
      TriggerPos := SamplePtr;
      HoldoffCount := vTriggerHoldoff;
    end;
  end
  else
    if HoldoffCount > 0 then Dec(HoldoffCount);
end;
```

**Trigger Timing**:
- Edge detection performed on every sample set
- Trigger position recorded as SamplePtr value
- Holdoff counter prevents immediate re-triggering
- Display updated when trigger fires or rate cycle occurs

### 18.5 Rate Control

**RateCycle Function**:
```pascal
function RateCycle: boolean;
begin
  Inc(vRateCount);
  if vRateCount >= vRate then
  begin
    vRateCount := 0;
    Result := True;
  end
  else
    Result := False;
end;
```

**Purpose**: Throttle display updates to configured rate.

**Configuration**: `RATE divisor` (default = 1)

**Timing**:
- Samples always buffered (continuous acquisition)
- Display only redrawn on trigger event or rate cycle
- Between updates: Samples accumulate in circular buffer

### 18.6 Pre/Post Trigger Buffering

**Trigger Position** (`vTriggerPos`):
```
vTriggerPos = 0:     All pre-trigger (trigger at right edge)
vTriggerPos = 512:   50% pre/post (trigger at center, for vSamples=1024)
vTriggerPos = 1024:  All post-trigger (trigger at left edge)
```

**Display Window Calculation**:
```pascal
// Starting sample relative to trigger
start_sample := TriggerPos - vTriggerPos;

// Ending sample
end_sample := start_sample + vSamples;
```

**Buffer Access**:
- Pre-trigger samples: Already in buffer before trigger
- Post-trigger samples: Collected after trigger detected
- Circular buffer ensures pre-trigger data always available

### 18.7 Memory Access Patterns

**Write Pattern**:
```
Sample Data → UnPack → Temporary samp[] → Copy to SampleBuff[SamplePtr * 32]
                                           (32 sequential writes)
```

**Read Pattern** (display rendering):
```
For each sample in display window:
  Calculate index: ((SamplePtr - offset) and 2047) * 32
  For each channel: Read SampleBuff[index + channel]
  Sequential access for 32 channels
```

**Cache Efficiency**:
- Write: Sequential 32-channel write (good locality)
- Read: Sequential access with stride of vSamples (moderate locality)
- Sample buffer size (256 KB) typically fits in L2 cache

---

## 19. Bitmap System and Double-Buffering

### 19.1 Bitmap Architecture

LOGIC uses the same double-buffered bitmap system as other display types.

**Bitmap Array** (DebugDisplayUnit.pas):
```pascal
Bitmap: array[0..1] of TBitmap;
```

**Bitmap Roles**:
- **Bitmap[0]**: Render target (all drawing operations)
- **Bitmap[1]**: Display buffer (copied to Canvas)

**Configuration**:
```pascal
Bitmap[0].PixelFormat := pf32bit;     // 32-bit RGBA
Bitmap[1].PixelFormat := pf32bit;
Bitmap[0].SetSize(vBitmapWidth, vBitmapHeight);
Bitmap[1].SetSize(vBitmapHeight, vBitmapHeight);
```

### 19.2 Memory Layout

**Pixel Format**: 32-bit RGBA (4 bytes per pixel)

**Memory Organization**:
```
Bitmap[0]:
  Row 0: [B0][G0][R0][A0][B1][G1][R1][A1]...[Bn][Gn][Rn][An]
  Row 1: [B0][G0][R0][A0][B1][G1][R1][A1]...[Bn][Gn][Rn][An]
  ...
  Row N: [B0][G0][R0][A0][B1][G1][R1][A1]...[Bn][Gn][Rn][An]
```

**Byte Order**: BGRA (Windows convention)

**Memory Size** (typical 512×512 display):
```
512 × 512 × 4 bytes × 2 bitmaps = 2,097,152 bytes = 2 MB
```

### 19.3 BitmapToCanvas Transfer

**Implementation** (DebugDisplayUnit.pas:3514-3522):
```pascal
procedure BitmapToCanvas(i: integer);
begin
  // Swap bitmaps
  BitmapPtr := BitmapPtr xor 1;

  // Copy render target to display buffer
  Bitmap[BitmapPtr xor 1].Canvas.Draw(0, 0, Bitmap[BitmapPtr]);

  // Trigger Windows paint event
  Invalidate;
end;
```

**Double-Buffer Swap**:
```
Before:
  Bitmap[0] = render target (being drawn to)
  Bitmap[1] = display buffer (visible)
  BitmapPtr = 0

After BitmapToCanvas:
  BitmapPtr = 1
  Bitmap[1] = new render target (will be drawn to next)
  Bitmap[0] = new display buffer (visible)
```

**Purpose**: Eliminate flicker by separating render and display operations.

**Timing**: Called on trigger event or rate cycle.

### 19.4 Waveform Rendering

**Binary Channel Rendering** (single-bit):
```pascal
for x := 0 to vSamples - 1 do
begin
  // Get sample value
  value := SampleBuff[index + channel];

  // Calculate Y position
  if value = 0 then
    y := channel_y + vSpacing
  else
    y := channel_y;

  // Draw line or dot
  if vLineStyle then
    SmoothLine(x_prev, y_prev, x, y, vDotSize, color, 255)
  else
    SmoothDot(x, y, vDotSize, color, 255);

  x_prev := x;
  y_prev := y;
end;
```

**Range Channel Rendering** (multi-bit analog-style):
```pascal
for x := 0 to vSamples - 1 do
begin
  // Get multi-bit value (combine channels)
  value := 0;
  for bit := range_start to range_end do
    if SampleBuff[index + bit] <> 0 then
      value := value or (1 shl (bit - range_start));

  // Scale to display range
  y := range_y_min + (value - range_min) * scale;

  // Draw line
  SmoothLine(x_prev, y_prev, x, y, vDotSize, color, 255);

  x_prev := x;
  y_prev := y;
end;
```

**Rendering Parameters**:
- `x, y`: Position in 8.8 fixed-point (256 = 1 pixel)
- `vDotSize`: Dot/line thickness in 6.6 fixed-point (64 = 1 pixel)
- `color`: RGB24 color value
- `opacity`: Always 255 (fully opaque) for LOGIC

### 19.5 Anti-Aliased Line/Dot Rendering

**SmoothLine** - Anti-aliased line:
```pascal
SmoothLine(x1, y1, x2, y2, thickness, color, opacity);
```

**SmoothDot** - Circular dot with anti-aliasing:
```pascal
SmoothDot(x, y, radius, color, opacity);
```

**Rendering Algorithm** (simplified):
```pascal
procedure SmoothLine(x1, y1, x2, y2, thickness, color, opacity);
begin
  // Bresenham line algorithm with anti-aliasing
  for each pixel along line do
  begin
    // Calculate distance from pixel center to line
    distance := perpendicular_distance(pixel, line);

    // Calculate coverage based on distance and thickness
    if distance < thickness / 2 - 128 then
      coverage := 1.0                    // Fully inside
    else if distance > thickness / 2 + 128 then
      coverage := 0.0                    // Fully outside
    else
      coverage := smooth_falloff(distance, thickness);  // Anti-aliased edge

    // Blend with existing pixel
    alpha := Round(opacity * coverage);
    if alpha > 0 then
      BlendPixel(px, py, color, alpha);
  end;
end;
```

**Anti-Aliasing**: Sub-pixel accuracy for smooth edges.

**Alpha Blending**: Combines waveform color with existing bitmap content.

### 19.6 Rendering Pipeline

**Full Render Cycle**:
```
1. Check trigger or rate cycle
2. Clear bitmap (ClearBitmap)
3. Draw grid lines (optional)
4. For each channel:
   a. Binary channel → Draw digital waveform
   b. Range channel → Draw analog-style waveform
5. Draw channel labels
6. Draw trigger marker (if triggered)
7. BitmapToCanvas (display update)
```

**Trigger Marker Rendering**:
```pascal
if vTrigger and (TriggerPos >= 0) then
begin
  // Draw vertical line at trigger position
  x := trigger_x_position;
  SmoothLine(x, 0, x, vBitmapHeight, vDotSize, vTriggerColor, 255);
end;
```

### 19.7 Performance Optimization

**Rendering Cost Factors**:
- Number of channels (vIndex)
- Number of samples displayed (vSamples)
- Line thickness (vDotSize)
- Anti-aliasing overhead

**Typical Performance** (32 channels, 512 samples, thickness=4):
```
Rendering time: ~10-50ms per frame
Frame rate: 20-100 Hz
```

**Optimization Strategies**:
1. Reduce vSamples (horizontal resolution)
2. Reduce vSpacing (vertical spacing)
3. Use smaller vDotSize (line thickness)
4. Apply rate limiting (reduce update frequency)
5. Disable unused channels

---

## 20. Shared Infrastructure

### 20.1 Color System

**TranslateColor Function** (shared with all displays):
```pascal
function TranslateColor(c: integer): integer;
begin
  if c < 0 then
    Result := DefaultScopeColors[(-c - 1) mod 8]
  else
    Result := SwapRGB(c);  // Convert RGB to BGR for Windows
end;
```

**Default Colors** (8 colors):
```pascal
DefaultScopeColors: array[0..7] of integer = (
  $00FFFF,  // Yellow
  $FF00FF,  // Magenta
  $FFFF00,  // Cyan
  $0000FF,  // Red
  $00FF00,  // Green
  $FF0000,  // Blue
  $00FFAA,  // Orange
  $FF00AA   // Purple
);
```

**LOGIC Color Usage**:
- Background color: vBackColor (default black)
- Grid color: vGridColor (default gray)
- Channel colors: vColor[0..31] (per-channel)
- Trigger marker color: Bright yellow

### 20.2 Data Packing System

LOGIC shares the same 12 packing modes as other display types:

**Packing Modes** (DebugDisplayUnit.pas:29-40):
```pascal
key_longs_1bit   = $10;   // 32 values per long (1 bit each)
key_longs_2bit   = $11;   // 16 values per long (2 bits each)
key_longs_4bit   = $12;   // 8 values per long (4 bits each)
key_longs_8bit   = $13;   // 4 values per long (8 bits each)
key_longs_16bit  = $14;   // 2 values per long (16 bits each)
key_words_1bit   = $15;   // 16 values per word (1 bit each)
key_words_2bit   = $16;   // 8 values per word (2 bits each)
key_words_4bit   = $17;   // 4 values per word (4 bits each)
key_words_8bit   = $18;   // 2 values per word (8 bits each)
key_bytes_1bit   = $19;   // 8 values per byte (1 bit each)
key_bytes_2bit   = $1A;   // 4 values per byte (2 bits each)
key_bytes_4bit   = $1B;   // 2 values per byte (4 bits each)
```

**LOGIC Typical Usage**: LONGS_1BIT (32 samples per long)

**UnPack Function** (lines 4152-4163):
```pascal
function UnPack(var v: integer): integer;
begin
  // Extract bits
  Result := v and vPackMask;

  // Sign-extend if MSB set (for SIGNED mode)
  if (Result shr (vPackSize - 1)) <> 0 then
    Result := Result or (not vPackMask);

  // Advance to next value
  Inc(vPackIndex);
  if vPackIndex < vPackCount then
    v := v shr vPackSize
  else
    vPackIndex := 0;
end;
```

### 20.3 Fixed-Point Arithmetic

LOGIC uses **8.8 fixed-point** format (8 integer bits, 8 fractional bits).

**Conversion**:
```
Integer to fixed-point: x << 8 (multiply by 256)
Fixed-point to integer: x >> 8 (divide by 256)
```

**Example**:
```
x = 10.5 pixels → fixed-point = 10.5 × 256 = 2688
x = 2688 (fixed-point) → pixels = 2688 / 256 = 10.5
```

**Purpose**: Sub-pixel positioning for anti-aliased rendering.

**LOGIC Coordinate Calculation**:
```pascal
x := sample_index * pixel_width * 256;  // Convert to 8.8 fixed-point
y := channel_y_position * 256;
```

### 20.4 Text Rendering

**Channel Labels**:
```pascal
procedure DrawChannelLabel(channel: integer; label: string);
begin
  // Set font
  Bitmap[0].Canvas.Font.Name := vFont;
  Bitmap[0].Canvas.Font.Size := vTextSize;
  Bitmap[0].Canvas.Font.Color := vColor[channel];

  // Draw label text
  y := channel * vSpacing * vHeight / vIndex;
  Bitmap[0].Canvas.TextOut(5, y, label);
end;
```

**Text Rendering**:
- Uses Windows GDI (not custom anti-aliasing)
- Font: Monospaced (typically 'Consolas' or 'Courier New')
- Size: Configurable via TEXTSIZE command
- Color: Matches channel color

### 20.5 File Operations

**Save to BMP** (shared SaveBitmap function):
```pascal
procedure SaveBitmap(filename: string);
begin
  if filename = '' then
    filename := Format('logic_%d.bmp', [SaveCounter]);
  Bitmap[BitmapPtr xor 1].SaveToFile(filename);
  Inc(SaveCounter);
end;
```

**LOGIC Command**: `SAVE {filename}`

**Behavior**: Saves current display buffer to BMP file.

---

## 21. Initialization Lifecycle

### 21.1 Window Creation Sequence

**Trigger**: Host software calls `CreateDebugDisplay(display_type, element_array)`.

**LOGIC Creation** (display_type = dis_logic = 4):

```pascal
// 1. Form instantiation
DebugDisplayForm := TDebugDisplayForm.Create(Application);
DebugDisplayForm.DisplayType := dis_logic;

// 2. Initialize element parser
ElementPtr := 0;
ElementEnd := element_count;

// 3. Set defaults
vWidth := 512;
vHeight := 512;
vSamples := 256;           // Horizontal resolution
vSpacing := 2;             // Vertical spacing
vRate := 1;                // Rate divisor
vDotSize := 4;             // Line thickness
vTextSize := 9;            // Label font size
vBackColor := $000000;     // Black
vGridColor := $202020;     // Dark gray
vLineStyle := True;        // Lines (not dots)
vTrigger := False;         // Trigger disabled
vIndex := 0;               // No channels configured yet

// 4. Call LOGIC_Configure
LOGIC_Configure;

// 5. Create bitmaps
Bitmap[0] := TBitmap.Create;
Bitmap[1] := TBitmap.Create;
Bitmap[0].PixelFormat := pf32bit;
Bitmap[1].PixelFormat := pf32bit;
Bitmap[0].SetSize(vBitmapWidth, vBitmapHeight);
Bitmap[1].SetSize(vBitmapWidth, vBitmapHeight);

// 6. Initialize sample buffer
SamplePtr := 0;
SamplePop := 0;
FillChar(SampleBuff, SizeOf(SampleBuff), 0);

// 7. Set form size and position
ClientWidth := vWidth + margins;
ClientHeight := vHeight + margins;
SetFormPosition;  // From POS command or cascade

// 8. Set packing mode
SetPack(key_longs_1bit);  // Default

// 9. Clear display
ClearBitmap;
BitmapToCanvas(0);

// 10. Show window
Show;
```

**Source Locations**:
- LOGIC_Configure: Lines 1096-1168
- Form creation: DebugUnit.pas (display manager)

### 21.2 Configuration Parameter Processing

**Parameter Parsing Loop** (lines 1102-1160):
```pascal
while not NextEnd do
begin
  if NextKey then
  case val of
    key_title:       KeyTitle;                    // Window title
    key_pos:         KeyPos;                      // Window position
    key_size:        KeySize;                     // Display dimensions
    key_samples:     KeyValWithin(vSamples, 4, 2047);
    key_spacing:     KeyValWithin(vSpacing, 1, 32);
    key_rate:        KeyValWithin(vRate, 1, 2048);
    key_dotsize:     KeyValWithin(vDotSize, 2, 20);
    key_textsize:    KeyTextSize;
    key_color:       if KeyColor(vBackColor) then KeyColor(vGridColor);
    key_trigger:     KeyTrigger;                  // Configure trigger
    key_line:        vLineStyle := True;          // Line mode
    key_dot:         vLineStyle := False;         // Dot mode
    key_longs_1bit..key_bytes_4bit:  KeyPack;    // Set packing mode
  end
  else if NextStr then                            // Channel label
  begin
    if vIndex <> Channels then Inc(vIndex);
    vLabel[vIndex - 1] := PChar(val);
    KeyColor(vColor[vIndex - 1]);                // Optional color follows
    KeyRange;                                     // Optional RANGE follows
  end;
end;
```

**Default Overrides**:
- SIZE not specified → vWidth = 512, vHeight = 512
- SAMPLES not specified → vSamples = 256
- SPACING not specified → vSpacing = 2
- RATE not specified → vRate = 1
- DOTSIZE not specified → vDotSize = 4
- Packing not specified → LONGS_1BIT
- Trigger not specified → Disabled

**Validation**:
- SAMPLES clamped to 4-2047
- SPACING clamped to 1-32 pixels
- RATE clamped to 1-2048
- DOTSIZE clamped to 2-20 pixels

### 21.3 Trigger Initialization

**KeyTrigger Processing**:
```pascal
procedure KeyTrigger;
begin
  vTrigger := True;
  if NextNum then vTriggerMask := val else vTriggerMask := $FFFFFFFF;
  if NextNum then vTriggerMatch := val else vTriggerMatch := $00000001;
  if NextNum then vTriggerPos := Within(val, 0, SampleSets) else vTriggerPos := SampleSets div 2;
  if NextNum then vTriggerHoldoff := Within(val, 0, 1000) else vTriggerHoldoff := 0;
end;
```

**Trigger Configuration Examples**:
```
TRIGGER                    → mask=$FFFFFFFF, match=$1, pos=1024, holdoff=0
TRIGGER $FF $01            → mask=$FF, match=$1 (channel 0 rising edge)
TRIGGER $FF $01 512 10     → 50% pre-trigger, 10-sample holdoff
```

### 21.4 Range Mode Initialization

**KeyRange Processing**:
```pascal
procedure KeyRange;
begin
  if not NextKey then Exit;  // No RANGE keyword
  if val <> key_range then Exit;

  // Configure range for previous channel
  if NextNum then range_start := Within(val, 0, 31) else Exit;
  if NextNum then range_end := Within(val, range_start, 31) else range_end := range_start;
  if NextNum then range_min := val else range_min := 0;
  if NextNum then range_max := val else range_max := (1 shl (range_end - range_start + 1)) - 1;

  // Mark channel as range mode
  vRange[vIndex - 1] := True;
  vRangeStart[vIndex - 1] := range_start;
  vRangeEnd[vIndex - 1] := range_end;
  vRangeMin[vIndex - 1] := range_min;
  vRangeMax[vIndex - 1] := range_max;
end;
```

**Range Configuration Examples**:
```
'Counter' $FFFF00 RANGE 0 7 0 255        → 8-bit counter (channels 0-7)
'ADC' $00FFFF RANGE 0 15 -32768 32767    → 16-bit signed ADC
```

### 21.5 Sample Buffer Initialization

**Buffer Allocation** (static):
```pascal
SampleBuff: array[0..SampleSets * SampleSetSize - 1] of integer;
```

**Initialization**:
```pascal
SamplePtr := 0;     // Write position
SamplePop := 0;     // Valid sample count
TriggerPos := -1;   // No trigger yet
HoldoffCount := 0;  // No holdoff active

// Clear buffer
FillChar(SampleBuff, SizeOf(SampleBuff), 0);
```

**Buffer State**:
- Empty buffer (all zeros)
- Write pointer at position 0
- No trigger detected
- Ready to receive first sample set

### 21.6 Initial Display State

**After Initialization**:
```
Window: Created and visible
Display: Black (cleared), no waveforms
Buffer: Empty (SamplePop = 0)
Trigger: Disabled or armed (depending on configuration)
Packing: LONGS_1BIT or configured mode
Channels: vIndex channels configured with labels/colors
```

**Ready for Data**: Window now waits for LOGIC_Update calls with sample data.

### 21.7 Runtime State Transitions

**State Diagram**:
```
[Created] → LOGIC_Configure → [Configured]
                                    ↓
                       LOGIC_Update (first samples)
                                    ↓
                            [Acquiring]
                                ↓    ↑
                          Sample data arrives
                                ↓    ↑
                          UnPack and buffer
                                ↓    ↑
                          Check trigger (if enabled)
                                ↓
                          Trigger detected or rate cycle
                                ↓
                          LOGIC_Plot (render waveforms)
                                ↓
                          BitmapToCanvas (display)
                                ↓
                        [Displaying] → Continue acquiring

CLEAR command → Reset buffer, SamplePtr=0, SamplePop=0
Close window → Cleanup → [Destroyed]
```

### 21.8 Cleanup and Destruction

**Window Close**:
```pascal
// 1. Stop processing updates
FormClosing := True;

// 2. Free bitmaps
Bitmap[0].Free;
Bitmap[1].Free;

// 3. Free form
Form.Free;

// Note: Sample buffer is static global, not freed
```

**Buffer Cleanup**: SampleBuff is a static global array, not freed per-window.

---

## 22. Summary

The **LOGIC** display window is a comprehensive digital logic analyzer for the Propeller 2 debug environment. It combines the visualization capabilities of hardware logic analyzers with the flexibility of software-based signal processing.

### 22.1 Key Capabilities

**Signal Visualization**:
- Up to 32 digital channels
- Single-bit binary waveforms
- Multi-bit range waveforms (analog-style)
- Anti-aliased rendering with configurable line/dot styles

**Data Acquisition**:
- 2048-sample circular buffer
- 12 packing modes (1-bit to 32-bit)
- Support for SIGNED and ALT modifiers
- Efficient serial transmission

**Trigger System**:
- Edge-sensitive triggering
- Configurable mask and match
- Adjustable trigger position (pre/post trigger)
- Holdoff to prevent re-triggering
- Free-running mode when trigger disabled

**Display Control**:
- Configurable horizontal resolution (4-2047 samples)
- Adjustable spacing (1-32 pixels)
- Rate limiting (1-2048 divisor)
- Channel labeling and coloring

**User Interaction**:
- Keyboard input feedback
- Mouse position/color feedback
- Bitmap export (SAVE command)
- Clear and reset commands

### 22.2 Performance Profile

**Strengths**:
- Efficient for digital signal visualization
- Low memory usage (8 KB sample buffer + ~520 KB display)
- Flexible data packing (32× bandwidth reduction)
- Edge-sensitive trigger reduces false triggers

**Limitations**:
- Limited to 32 channels
- Fixed 2048-sample buffer depth
- No real-time filtering or signal processing
- Rendering cost increases with channel count and sample count

**Optimization**:
- Use appropriate packing mode for data width
- Apply rate limiting for high-speed sampling
- Use trigger system to capture specific events
- Limit vSamples to reduce rendering load

### 22.3 Common Use Cases

**Digital Protocol Analysis**:
- SPI, I2C, UART communication
- Parallel bus monitoring
- Handshake signal analysis

**State Machine Debugging**:
- State transitions
- Control signal timing
- Flag synchronization

**Timing Analysis**:
- Clock relationship verification
- Setup/hold time validation
- Pulse width measurement

**Multi-Bit Values**:
- Counter values (RANGE mode)
- ADC samples (RANGE mode)
- Parallel data buses

### 22.4 Integration with P2 Workflow

The LOGIC window seamlessly integrates into the P2 debug ecosystem:

1. **P2 Sampling**: Sample digital signals at full speed
2. **Packing**: Pack multiple samples per transmission
3. **Serial TX**: Transmit packed data at 2 Mbaud
4. **PC Reception**: UnPack and buffer samples
5. **Trigger Detection**: Detect trigger conditions
6. **Display Update**: Render waveforms on trigger or rate cycle
7. **User Feedback**: Send mouse/keyboard state back to P2

This bidirectional communication enables interactive debugging and signal capture controlled from the P2 code.

### 22.5 Design Philosophy

The LOGIC window embodies a "hardware logic analyzer in software" design philosophy:

- **Familiarity**: Similar to traditional logic analyzer UX
- **Flexibility**: Software-based trigger and display control
- **Efficiency**: Optimized for serial bandwidth and rendering performance
- **Integration**: Shares infrastructure with other display types
- **Simplicity**: Straightforward configuration and operation

This balance makes LOGIC ideal for both quick signal visualization and detailed timing analysis.

---

**End of LOGIC Theory of Operations**
