# SCOPE Display Window - Theory of Operations

**Current as of**: PNut v51a for Propeller 2

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Display Type and Constants](#3-display-type-and-constants)
4. [Data Structures](#4-data-structures)
5. [Configuration and Initialization](#5-configuration-and-initialization)
6. [Channel Configuration](#6-channel-configuration)
7. [Auto-Ranging System](#7-auto-ranging-system)
8. [Sample Processing](#8-sample-processing)
9. [Trigger System](#9-trigger-system)
10. [Rendering Pipeline](#10-rendering-pipeline)
11. [Scaling and Positioning](#11-scaling-and-positioning)
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

The **SCOPE** display window is a multi-channel oscilloscope for the Propeller 2 (P2) microcontroller debug environment. It provides real-time visualization of analog signals with features similar to traditional oscilloscope hardware:

- **Up to 8 analog channels** with independent configuration
- **Automatic range detection** (auto-ranging) for each channel
- **Manual scaling control** (low, high, tall, base, grid)
- **Level-based triggering** with rising/falling edge detection
- **Holdoff control** to stabilize display
- **Circular sample buffer** (2048 samples per channel)
- **Rate limiting** for display update control
- **Anti-aliased trace rendering**
- **Flexible data packing** (12 packing modes)

The SCOPE window is ideal for monitoring sensor values, ADC readings, analog signals, and any continuous time-domain data.

**File Location**: `DebugDisplayUnit.pas`

**Key Methods**:
- `SCOPE_Configure` (lines 1151-1207): Initialization and channel setup
- `SCOPE_Update` (lines 1209-1337): Sample ingestion and trigger processing
- `SCOPE_Draw` (lines 1339-1364): Waveform rendering
- `SCOPE_Range` (lines 1366-1379): Auto-ranging calculation

---

## 2. Architecture Overview

### 2.1 System Context

The SCOPE window operates as part of the P2 debug display system:

```
┌─────────────────────────────────────────────────────────────┐
│                    Propeller 2 Hardware                     │
│              (Analog Signal Sampling)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Serial Transmission
                         │ (Packed Sample Sets)
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
│                     SCOPE_Update Method                      │
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│  │ Data Packing │   │ Auto-Ranging │   │   Trigger    │   │
│  │   UnPack()   │──>│ SCOPE_Range()│──>│  Detection   │   │
│  └──────────────┘   └──────────────┘   └──────────────┘   │
│                                              │               │
│                                              │ RateCycle     │
│                                              ▼               │
│                     ┌──────────────────────────────┐        │
│                     │     SCOPE_Draw Method        │        │
│                     │   (Multi-Trace Rendering)    │        │
│                     └──────────────────────────────┘        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Double-Buffered Display
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Windows VCL Canvas                         │
│              (Oscilloscope Visualization)                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

**Configuration Flow** (Window Creation):
```
Serial Command → Parse Channels → SCOPE_Configure → Set Metrics → Create Window
```

**Sample Flow** (Data Acquisition):
```
P2 Samples → Pack Data → Serial TX → UnPack → Sample Set Assembly → Circular Buffer → Trigger Check → SCOPE_Draw
```

**Auto-Ranging Flow** (Dynamic Scaling):
```
Sample Buffer → SCOPE_Range Scan → Find Min/Max → Update vLow/vHigh → Apply Scale Factor
```

---

## 3. Display Type and Constants

### 3.1 Display Type Identifier

```pascal
dis_scope = 1;
```

The SCOPE display is the second display type (index 1) in the debug display system.

**Source Location**: Line 23 in DebugDisplayUnit.pas

### 3.2 Buffer Constants

```pascal
Channels         = 8;                    // Maximum channels
Y_SetSize        = Channels;             // 8 samples per set (one per channel)
Y_Sets           = DataSets;             // 2048 sample sets
Y_PtrMask        = Y_Sets - 1;           // 2047 (for circular buffer)
```

**Purpose**:
- `Channels`: Maximum number of simultaneous analog channels (8)
- `Y_SetSize`: Samples per complete set (one sample from each channel)
- `Y_Sets`: Number of sample sets in circular buffer (2048)
- `Y_PtrMask`: Bit mask for circular buffer wraparound (2047 = 0x7FF)

**Memory Calculation**:
```
Y_SampleBuff: 2048 sets × 8 samples × 4 bytes = 65,536 bytes = 64 KB
```

**Source Locations**: Lines 167-169 in DebugDisplayUnit.pas

### 3.3 Size Constraints

```pascal
scope_wmin    = 32;                      // Minimum width in pixels
scope_wmax    = SmoothFillMax;           // Maximum width (2048)
scope_hmin    = 32;                      // Minimum height in pixels
scope_hmax    = SmoothFillMax;           // Maximum height (2048)
```

**Source Locations**: Lines 210-213 in DebugDisplayUnit.pas

### 3.4 Default Values

```pascal
// From SCOPE_Configure (lines 1156-1159)
vRate        := 1;               // Default rate divisor (1 = every sample)
vDotSize     := 0;               // Default dot size (0 = no dots)
vLineSize    := 3;               // Default line thickness (pixels)
vTextSize    := FontSize;        // Default label font size (9)
```

---

## 4. Data Structures

### 4.1 Sample Buffer

```pascal
Y_SampleBuff: array[0..Y_Sets * Y_SetSize - 1] of integer;
```

**Characteristics**:
- **Size**: 2048 sets × 8 channels = 16,384 samples total
- **Element Type**: 32-bit signed integer
- **Access Pattern**: Circular buffer with wraparound
- **Organization**: Interleaved by sample set
  - `Y_SampleBuff[set * 8 + channel]` = sample for given set and channel

**Buffer Layout**:
```
Set 0:  [Ch0][Ch1][Ch2][Ch3][Ch4][Ch5][Ch6][Ch7]
Set 1:  [Ch0][Ch1][Ch2][Ch3][Ch4][Ch5][Ch6][Ch7]
...
Set 2047: [Ch0][Ch1][Ch2][Ch3][Ch4][Ch5][Ch6][Ch7]
```

**Circular Buffer Management**:
```pascal
// Write sample set
Move(samp, Y_SampleBuff[SamplePtr * Y_SetSize], Y_SetSize shl 2);
SamplePtr := (SamplePtr + 1) and Y_PtrMask;

// Read sample (k sets back, channel j)
v := Y_SampleBuff[((SamplePtr - k - 1) and Y_PtrMask) * Y_SetSize + j];
```

**Source Location**: Line 361

### 4.2 Channel Configuration Arrays

```pascal
vAuto        : array[0..Channels - 1] of boolean;     // Auto-ranging enable per channel
vLow         : array[0..Channels - 1] of integer;     // Low value (bottom of range)
vHigh        : array[0..Channels - 1] of integer;     // High value (top of range)
vTall        : array[0..Channels - 1] of integer;     // Vertical height in pixels
vBase        : array[0..Channels - 1] of integer;     // Vertical offset in pixels
vGrid        : array[0..Channels - 1] of integer;     // Grid spacing (not rendered in SCOPE)
vLabel       : array[0..Channels - 1] of string;      // Channel labels
vColor       : array[0..Channels - 1] of integer;     // Trace colors (RGB24)
```

**Purpose**:

**vAuto**: Auto-ranging mode per channel
- `True`: Automatically calculate vLow/vHigh from sample buffer
- `False`: Use manually specified vLow/vHigh values

**vLow/vHigh**: Value range for vertical scaling
- `vLow`: Corresponds to bottom of trace area
- `vHigh`: Corresponds to top of trace area
- Range: -$80000000 to $7FFFFFFF (full 32-bit signed)

**vTall**: Vertical height in pixels
- Determines vertical span of trace
- Default: vHeight (full display height)
- Allows partial-height traces for multi-channel overlay

**vBase**: Vertical offset in pixels
- Positive: Shift trace up
- Negative: Shift trace down
- Default: 0 (no offset)
- Useful for overlaying multiple channels

**vGrid**: Grid spacing (reserved, not rendered)
- Intended for grid line rendering
- Not currently implemented in SCOPE_Draw

**Default Initialization** (lines 1189-1197):
```pascal
for i := 0 to Channels - 1 do
begin
  vAuto[i] := False;
  vLow[i]  := -$80000000;
  vHigh[i] := $7FFFFFFF;
  vTall[i] := vHeight;
  vBase[i] := 0;
  vGrid[i] := 0;
end;
```

**Source Locations**: Lines 304-310

### 4.3 Trigger State Variables

```pascal
vTriggerChannel : integer;       // Channel to trigger on (-1 = disabled, 0-7 = channel)
vTriggerAuto    : boolean;       // Auto-trigger mode
vTriggerArm     : integer;       // Arm level (must cross before trigger)
vTriggerFire    : integer;       // Fire level (trigger occurs here)
vTriggerOffset  : integer;       // Sample offset for trigger position (0..vSamples-1)
vHoldOff        : integer;       // Holdoff count to prevent re-triggering
vHoldOffCount   : integer;       // Current holdoff counter
vArmed          : boolean;       // Trigger armed state
vTriggered      : boolean;       // Trigger event occurred
```

**Trigger Logic**:

**vTriggerChannel**: Selects which channel to monitor
- `-1`: Trigger disabled (free-running mode)
- `0-7`: Channel index to trigger on

**vTriggerAuto**: Auto-calculate trigger levels
- `True`: Calculate arm/fire levels from sample buffer range
  - Arm level = low + (high - low) / 3 (lower third)
  - Fire level = low + (high - low) / 2 (middle)
- `False`: Use manually specified arm/fire levels

**vTriggerArm/vTriggerFire**: Threshold levels
- **Rising edge**: `TriggerFire >= TriggerArm`
  - Arm when signal drops below TriggerArm
  - Fire when signal rises above TriggerFire
- **Falling edge**: `TriggerFire < TriggerArm`
  - Arm when signal rises above TriggerArm
  - Fire when signal falls below TriggerFire

**vTriggerOffset**: Pre/post-trigger position
- `0`: Trigger at left edge (show what happens after trigger)
- `vSamples/2`: Trigger at center (default)
- `vSamples-1`: Trigger at right edge (show what led up to trigger)

**Default Initialization** (lines 1198-1203):
```pascal
vTriggerChannel := -1;
vTriggerAuto := False;
vTriggerArm := -1;
vTriggerFire := 0;
vTriggerOffset := vSamples div 2;
vHoldOff := vSamples;
```

### 4.4 Display State Variables

```pascal
vSamples        : integer;       // Horizontal resolution (sets displayed)
vWidth          : integer;       // Display width in pixels
vHeight         : integer;       // Display height in pixels
vRate           : integer;       // Rate divisor (1 = every sample triggers draw)
vRateCount      : integer;       // Current rate counter
vDotSize        : integer;       // Dot diameter (pixels, 0 = no dots)
vLineSize       : integer;       // Line thickness (pixels, 0 = no lines)
vTextSize       : integer;       // Label font size
vIndex          : integer;       // Number of active channels
```

---

## 5. Configuration and Initialization

### 5.1 SCOPE_Configure Method

```pascal
procedure TDebugDisplayForm.SCOPE_Configure;
var
  i: integer;
begin
  // Set unique defaults
  vRate := 1;
  vDotSize := 0;
  vLineSize := 3;
  vTextSize := FontSize;

  // Process any parameters
  while NextKey do
  case val of
    key_title:       KeyTitle;
    key_pos:         KeyPos;
    key_size:        KeySize(vWidth, vHeight, scope_wmin, scope_wmax, scope_hmin, scope_hmax);
    key_samples:     KeyValWithin(vSamples, 16, Y_Sets);
    key_rate:        KeyValWithin(vRate, 1, Y_Sets);
    key_dotsize:     KeyValWithin(vDotSize, 0, 32);
    key_linesize:    KeyValWithin(vLineSize, 0, 32);
    key_textsize:    KeyTextSize;
    key_color:       if KeyColor(vBackColor) then KeyColor(vGridColor);
    key_hidexy:      vHideXY := True;
    key_longs_1bit..key_bytes_4bit:  KeyPack;
  end;

  // Set defaults
  if (vDotSize = 0) and (vLineSize = 0) then vDotSize := 1;
  for i := 0 to Channels - 1 do
  begin
    vAuto[i] := False;
    vLow[i]  := -$80000000;
    vHigh[i] := $7FFFFFFF;
    vTall[i] := vHeight;
    vBase[i] := 0;
    vGrid[i] := 0;
  end;
  vTriggerChannel := -1;
  vTriggerAuto := False;
  vTriggerArm := -1;
  vTriggerFire := 0;
  vTriggerOffset := vSamples div 2;
  vHoldOff := vSamples;

  // Set form metrics
  SetTextMetrics;
  SetSize(ChrWidth, ChrHeight * 2, ChrWidth, ChrWidth);
end;
```

**Source Location**: Lines 1151-1207

### 5.2 Configuration Parameters

| Parameter | Command | Default | Range | Purpose |
|-----------|---------|---------|-------|---------|
| Title | `TITLE 'string'` | "Scope" | - | Window title |
| Position | `POS x y` | Cascaded | Screen coords | Window position |
| Size | `SIZE width height` | 512 × 256 | 32-2048 | Display dimensions |
| Samples | `SAMPLES count` | 512 | 16-2048 | Horizontal resolution |
| Rate | `RATE divisor` | 1 | 1-2048 | Display update rate divisor |
| Dot Size | `DOTSIZE pixels` | 0 | 0-32 | Dot diameter (0 = no dots) |
| Line Size | `LINESIZE pixels` | 3 | 0-32 | Line thickness (0 = no lines) |
| Text Size | `TEXTSIZE size` | 9 | 6-200 | Label font size |
| Colors | `COLOR back grid` | Black/Gray | RGB24 | Background and grid colors |
| Hide XY | `HIDEXY` | Show | - | Hide mouse coordinates |
| Packing | `LONGS_1BIT` etc. | LONGS_1BIT | 12 modes | Data packing format |

### 5.3 Rendering Mode Validation

```pascal
// Set defaults (line 1188)
if (vDotSize = 0) and (vLineSize = 0) then vDotSize := 1;
```

**Purpose**: Ensure at least one rendering mode is active.
- If both dot and line sizes are 0, default to dot size of 1
- Prevents invisible traces

---

## 6. Channel Configuration

### 6.1 Channel Configuration Syntax

**String Element Format**:
```
'label' {AUTO | low high} {tall} {base} {grid} {color}
```

**Parameters**:
- `label`: Channel name
- `AUTO`: Enable auto-ranging (exclusive with low/high)
- `low high`: Manual range (min/max values)
- `tall`: Vertical height in pixels (default: vHeight)
- `base`: Vertical offset in pixels (default: 0)
- `grid`: Grid spacing (default: 0, not rendered)
- `color`: Trace color (RGB24, default: cycle through DefaultScopeColors)

### 6.2 Auto-Ranging Mode

**Syntax**:
```
'SENSOR' AUTO
```

**Configuration Code** (lines 1217-1232):
```pascal
if NextStr then
begin
  if vIndex <> Channels then Inc(vIndex);
  vLabel[vIndex - 1] := PChar(val);
  if KeyIs(key_auto) then
    vAuto[vIndex - 1] := True
  else
  begin
    if not KeyVal( vLow[vIndex - 1]) then Continue;
    if not KeyVal(vHigh[vIndex - 1]) then Continue;
  end;
  if not KeyVal(vTall[vIndex - 1]) then Continue;
  if not KeyVal(vBase[vIndex - 1]) then Continue;
  if not KeyVal(vGrid[vIndex - 1]) then Continue;
  KeyColor(vColor[vIndex - 1]);
end
```

**Behavior**:
- `vAuto[channel] = True`
- vLow/vHigh automatically calculated by SCOPE_Range on each draw
- Trace scale adapts to signal range

### 6.3 Manual Ranging Mode

**Syntax**:
```
'ADC' -128 127 256 0 0 $FF0000
```

**Parameters**:
- Label: "ADC"
- Low: -128 (bottom of display)
- High: 127 (top of display)
- Tall: 256 pixels (vertical span)
- Base: 0 (no vertical offset)
- Grid: 0 (no grid)
- Color: Red ($FF0000)

**Behavior**:
- `vAuto[channel] = False`
- vLow/vHigh remain fixed
- Trace scale is constant

### 6.4 Overlay Configuration

**Multiple Channels with Offsets**:
```
'CH1' AUTO 128 0   $00FF00
'CH2' AUTO 128 128 $FF0000
```

**Result**:
- CH1: Green, full height (128px), bottom half of display
- CH2: Red, full height (128px), top half of display
- Overlaid on same time base

### 6.5 Configuration Examples

**Example 1: Single Auto-Ranging Channel**:
```
SCOPE 'TEMPERATURE' AUTO
```

Result:
- 1 channel
- Automatic range detection
- Lime green (DefaultScopeColors[0])

**Example 2: Fixed Range ADC**:
```
SCOPE 'ADC' 0 1023 256
```

Result:
- 1 channel
- Fixed 0-1023 range
- 256 pixels tall
- Lime green

**Example 3: Multi-Channel with Colors**:
```
SCOPE SIZE 512 384
      'X' AUTO 128 0   0 $FF0000
      'Y' AUTO 128 128 0 $00FF00
      'Z' AUTO 128 256 0 $0000FF
```

Result:
- 3 channels (X, Y, Z)
- Auto-ranging
- 128 pixels each
- Stacked vertically (base offsets: 0, 128, 256)
- Red, green, blue

---

## 7. Auto-Ranging System

### 7.1 SCOPE_Range Method

```pascal
procedure TDebugDisplayForm.SCOPE_Range(channel: integer; var low, high: integer);
var
  k: integer;
  v: int64;
begin
  low := $7FFFFFFF;
  high := -$80000000;
  for k := SamplePop - 1 downto 0 do
  begin
    v := Y_SampleBuff[((SamplePtr - k - 1) and Y_PtrMask) * Y_SetSize + channel];
    if v < low then low := v;
    if v > high then high := v;
  end;
end;
```

**Source Location**: Lines 1366-1379

**Processing**:
1. Initialize low/high to extreme values
2. Scan all samples in buffer for given channel
3. Track minimum (low) and maximum (high)
4. Return range via var parameters

**Complexity**: O(n) where n = SamplePop (number of samples)

### 7.2 Auto-Ranging Application

**Code** (SCOPE_Draw, line 1346):
```pascal
for j := vIndex - 1 downto 0 do if vAuto[j] then SCOPE_Range(j, vLow[j], vHigh[j]);
```

**Processing**:
- Called once per SCOPE_Draw invocation
- Only processes channels with `vAuto[j] = True`
- Updates vLow/vHigh for those channels
- Scaling recalculated based on new range

### 7.3 Auto-Trigger Range Calculation

**Code** (SCOPE_Update, lines 1289-1294):
```pascal
if vTriggerAuto then
begin
  SCOPE_Range(vTriggerChannel, low, high);
  vTriggerArm := (high - low) div 3 + low;
  vTriggerFire := (high - low) div 2 + low;
end;
```

**Formula**:
```
range = high - low
vTriggerArm  = low + range / 3    (lower third)
vTriggerFire = low + range / 2    (midpoint)
```

**Example**:
```
Signal range: 100 to 700
  range = 600
  arm  = 100 + 200 = 300
  fire = 100 + 300 = 400

Trigger on rising edge crossing 400 (after falling below 300)
```

### 7.4 Range Stability

**Potential Issue**: Range can change rapidly if signal varies.

**Mitigation Strategies**:
1. Use manual ranging for stable display
2. Use trigger holdoff to prevent excessive updates
3. Use rate limiting to slow down updates

**Trade-offs**:
- Auto-ranging: Adapts to signal, but may be unstable
- Manual ranging: Stable display, but requires known signal range

---

## 8. Sample Processing

### 8.1 SCOPE_Update Method Overview

```pascal
procedure TDebugDisplayForm.SCOPE_Update;
var
  ch, i, t, v, low, high: integer;
  samp: array[0..Y_SetSize - 1] of integer;
begin
  ch := 0;
  while not NextEnd do
  begin
    // String element: channel configuration (see Section 6)
    if NextStr then ...
    // Key element: trigger/control commands
    else if NextKey then ...
    // Numeric elements: sample data
    else while NextNum do ...
  end;
end;
```

**Source Location**: Lines 1209-1337

### 8.2 Sample Set Assembly

**Processing Loop** (lines 1268-1335):
```pascal
while NextNum do
begin
  // Get channel sample(s)
  v := NewPack;
  for i := 1 to vPackCount do
  begin
    // Enter sample into local buffer
    samp[ch] := UnPack(v);
    Inc(ch);
    if ch = vIndex then
    begin
      // Complete sample set received
      ch := 0;
      Move(samp, Y_SampleBuff[SamplePtr * Y_SetSize], Y_SetSize shl 2);
      SamplePtr := (SamplePtr + 1) and Y_PtrMask;
      if SamplePop < vSamples then Inc(SamplePop);
      // Trigger processing...
    end;
  end;
end;
```

**Sample Set Assembly**:
1. Read packed value: `v = NewPack()`
2. Unpack samples: `samp[ch] = UnPack(v)`
3. Increment channel counter
4. When all channels received (`ch = vIndex`):
   - Copy complete set to circular buffer
   - Advance write pointer
   - Increment fill level (until full)
   - Process trigger
   - Reset channel counter for next set

**Example** (4 channels, LONGS_1BIT):
```
Packed value 1:  32 samples of channel 0
Packed value 2:  32 samples of channel 1
Packed value 3:  32 samples of channel 2
Packed value 4:  32 samples of channel 3

Each iteration through outer loop:
  - Processes 32 sample sets
  - Stores 32 × 4 = 128 samples total
```

### 8.3 Buffer Management

**Write Operation** (line 1281):
```pascal
Move(samp, Y_SampleBuff[SamplePtr * Y_SetSize], Y_SetSize shl 2);
```

**Breakdown**:
- `samp`: Local array with one sample per channel
- `Y_SampleBuff[SamplePtr * Y_SetSize]`: Destination in circular buffer
- `Y_SetSize shl 2`: Byte count (8 channels × 4 bytes = 32 bytes)

**Pointer Advancement** (line 1282):
```pascal
SamplePtr := (SamplePtr + 1) and Y_PtrMask;
```

**Fill Level** (line 1283):
```pascal
if SamplePop < vSamples then Inc(SamplePop);
```

- Increments until buffer is full
- Once full, stays at vSamples (circular buffer overwrites oldest)

---

## 9. Trigger System

The SCOPE window implements a **level-based** trigger system (as opposed to LOGIC's edge-based trigger).

### 9.1 Trigger Configuration

**TRIGGER Command Syntax**:
```
TRIGGER channel {AUTO | arm fire} {offset}
```

**Parameters**:
- `channel`: Channel to trigger on (-1 = disabled, 0-7 = channel index)
- `AUTO`: Auto-calculate arm/fire levels
- `arm fire`: Manual arm/fire threshold levels
- `offset`: Trigger position in display (0..vSamples-1)

**Configuration Code** (lines 1236-1249):
```pascal
key_trigger:
begin
  vArmed := False;
  if not KeyValWithin(vTriggerChannel, -1, 7) then Continue;
  if KeyIs(key_auto) then
    vTriggerAuto := True
  else
  begin
    vTriggerAuto := False;
    if not KeyVal(vTriggerArm) then Continue;
    if not KeyVal(vTriggerFire) then Continue;
  end;
  KeyValWithin(vTriggerOffset, 0, vSamples - 1);
end;
```

**Examples**:
```
TRIGGER 0 AUTO             // Auto-trigger on channel 0
TRIGGER 1 500 600 256      // Trigger on channel 1, arm=500, fire=600, offset=256
TRIGGER -1                 // Disable trigger (free-running)
```

### 9.2 Trigger Detection Algorithm

**Rising Edge Trigger** (`TriggerFire >= TriggerArm`):

```pascal
if vArmed then
begin
  if t >= vTriggerFire then
  begin
    vTriggered := True;
    vArmed := False;
  end;
end
else
begin
  if t <= vTriggerArm then vArmed := True;
end;
```

**Sequence**:
1. Signal below arm level → ARM
2. Signal rises above fire level → TRIGGER
3. Disarm

**Falling Edge Trigger** (`TriggerFire < TriggerArm`):

```pascal
if vArmed then
begin
  if t <= vTriggerFire then
  begin
    vTriggered := True;
    vArmed := False;
  end;
end
else
begin
  if t >= vTriggerArm then vArmed := True;
end;
```

**Sequence**:
1. Signal above arm level → ARM
2. Signal falls below fire level → TRIGGER
3. Disarm

**Source Location**: Lines 1295-1325

### 9.3 Trigger State Machine

```
Rising Edge (Fire > Arm):

    Signal
      │
Arm   ├─────┐      Armed
      │     │
      │     ▼
Fire  │   ──┼──    Triggered
      │
      │
     ─┴─────


Falling Edge (Fire < Arm):

    Signal
      │
Fire  │   ──┼──    Triggered
      │     │
      │     ▼
Arm   ├─────┘      Armed
      │
      │
     ─┴─────
```

### 9.4 Trigger Comparison Code

**Full Implementation** (lines 1286-1325):
```pascal
if vTriggerChannel >= 0 then
begin
  if SamplePop <> vSamples then Continue;      // Wait for full buffer

  // Auto-calculate trigger levels if enabled
  if vTriggerAuto then
  begin
    SCOPE_Range(vTriggerChannel, low, high);
    vTriggerArm := (high - low) div 3 + low;
    vTriggerFire := (high - low) div 2 + low;
  end;

  // Read sample at trigger position
  t := Y_SampleBuff[((SamplePtr - vTriggerOffset - 1) and Y_PtrMask) * Y_SetSize + vTriggerChannel];

  // Check arming and firing
  if vArmed then
  begin
    if vTriggerFire >= vTriggerArm then
    begin
      if t >= vTriggerFire then
      begin
        vTriggered := True;
        vArmed := False;
      end;
    end
    else
    begin
      if t <= vTriggerFire then
      begin
        vTriggered := True;
        vArmed := False;
      end;
    end;
  end
  else
  begin
    if vTriggerFire >= vTriggerArm then
    begin
      if t <= vTriggerArm then vArmed := True;
    end
    else
    begin
      if t >= vTriggerArm then vArmed := True;
    end;
  end;

  // Holdoff processing
  if vHoldOffCount > 0 then Dec(vHoldOffCount);
  if not vTriggered or (vHoldOffCount > 0) then Continue;
  vHoldOffCount := vHoldOff;

  // Update display
  if RateCycle then SCOPE_Draw;
end
```

### 9.5 Holdoff System

**Same as LOGIC window**:
```pascal
key_holdoff:
  if KeyValWithin(vHoldOff, 2, Y_Sets) then vHoldOffCount := 0;
```

**Behavior**: Prevent re-triggering for `vHoldOff` samples after trigger event.

### 9.6 Trigger Disabled Mode

**Condition**: `vTriggerChannel = -1`

**Code** (lines 1331-1332):
```pascal
else if RateCycle then SCOPE_Draw;
```

**Behavior**: Free-running mode - display updates on every rate cycle.

---

## 10. Rendering Pipeline

### 10.1 SCOPE_Draw Method

```pascal
procedure TDebugDisplayForm.SCOPE_Draw;
var
  j, k, x, y, color, offset: integer;
  v: int64;
  fScale: Extended;
begin
  // Autoscale enabled channels
  for j := vIndex - 1 downto 0 do if vAuto[j] then SCOPE_Range(j, vLow[j], vHigh[j]);

  // Draw scope
  ClearBitmap;
  for j := vIndex - 1 downto 0 do
  begin
    if vHigh[j] = vLow[j] then fscale := 0
    else fScale := (vTall[j] - 1) / (Abs(Int64(vHigh[j]) - Int64(vLow[j]))) * $100;
    if vHigh[j] > vLow[j] then offset := vLow[j] else offset := vHigh[j];
    color := vColor[j];
    for k := SamplePop - 1 downto 0 do
    begin
      v := Y_SampleBuff[((SamplePtr - k - 1) and Y_PtrMask) * Y_SetSize + j];
      x := (vMarginLeft + vWidth - 1) shl 8 - Round(k / vSamples * vWidth * $100);
      y := (vMarginTop + vHeight - 1 - vBase[j]) shl 8 - Round((v - offset) * fScale);
      DrawLineDot(x, y, color, k = SamplePop - 1)
    end;
  end;
  BitmapToCanvas(0);
end;
```

**Source Location**: Lines 1339-1364

### 10.2 Rendering Steps

**Step 1: Auto-Range Update** (line 1346):
```pascal
for j := vIndex - 1 downto 0 do if vAuto[j] then SCOPE_Range(j, vLow[j], vHigh[j]);
```

Update vLow/vHigh for auto-ranging channels.

**Step 2: Clear Canvas** (line 1348):
```pascal
ClearBitmap;
```

Fill with background color.

**Step 3: Per-Channel Loop** (lines 1349-1362):

For each channel:
1. Calculate scale factor
2. Set color
3. Plot all samples
4. Connect with lines/dots

**Step 4: Display Update** (line 1363):
```pascal
BitmapToCanvas(0);
```

Copy render target to display buffer.

### 10.3 Scale Factor Calculation

**Code** (lines 1351-1353):
```pascal
if vHigh[j] = vLow[j] then fscale := 0
else fScale := (vTall[j] - 1) / (Abs(Int64(vHigh[j]) - Int64(vLow[j]))) * $100;
if vHigh[j] > vLow[j] then offset := vLow[j] else offset := vHigh[j];
```

**Scale Factor Formula**:
```
fScale = (tall - 1) / |high - low| × 256
```

**Converts**:
- Value units → pixel units (fixed-point)

**Offset**:
- If `high > low`: offset = low (normal case)
- If `high < low`: offset = high (inverted range)

**Example**:
```
vLow = 0, vHigh = 1023, vTall = 256

fScale = (256 - 1) / |1023 - 0| × 256
       = 255 / 1023 × 256
       = 63.87

Value 512: y_offset = 512 × 63.87 = 32,702 (fixed-point) ≈ 128 pixels
```

### 10.4 Coordinate Calculation

**Horizontal (Time)** (line 1358):
```pascal
x := (vMarginLeft + vWidth - 1) shl 8 - Round(k / vSamples * vWidth * $100);
```

**Formula**:
```
x = (left + width - 1) × 256 - (k / samples) × width × 256
```

**Effect**:
- Right-to-left plotting
- k = 0 (newest): right edge
- k = SamplePop-1 (oldest): left edge

**Vertical (Value)** (line 1359):
```pascal
y := (vMarginTop + vHeight - 1 - vBase[j]) shl 8 - Round((v - offset) * fScale);
```

**Formula**:
```
y = (top + height - 1 - base) × 256 - (value - offset) × scale
```

**Effect**:
- Bottom-to-top plotting
- Low values at bottom
- High values at top
- vBase offsets entire trace vertically

### 10.5 Point Rendering

**Code** (line 1360):
```pascal
DrawLineDot(x, y, color, k = SamplePop - 1)
```

**Same as LOGIC**: Connects points with lines (if vLineSize > 0) and/or draws dots (if vDotSize > 0).

---

## 11. Scaling and Positioning

### 11.1 Vertical Scaling Examples

**Example 1: Full-Scale ADC (0-1023)**:
```
vLow = 0
vHigh = 1023
vTall = 256
vBase = 0

fScale = 255 / 1023 × 256 = 63.87

Value 0:    y = (top + 255) × 256 - (0 - 0) × 63.87 = bottom
Value 512:  y = (top + 255) × 256 - 512 × 63.87 = middle
Value 1023: y = (top + 255) × 256 - 1023 × 63.87 = top
```

**Example 2: Signed Temperature (-40 to +85 °C)**:
```
vLow = -40
vHigh = 85
vTall = 256
vBase = 0

range = |85 - (-40)| = 125
fScale = 255 / 125 × 256 = 522.24

Value -40:  y = bottom
Value 0:    y = (top + 255) × 256 - (0 - (-40)) × 522.24 = middle-low
Value +85:  y = top
```

### 11.2 Overlay with Base Offsets

**Example: 3 Channels Stacked**:
```
CH1: vTall = 100, vBase = 0
CH2: vTall = 100, vBase = 100
CH3: vTall = 100, vBase = 200
```

**Result**:
- CH1: Bottom 100 pixels
- CH2: Middle 100 pixels
- CH3: Top 100 pixels

**Y Calculation**:
```
CH1: y = (top + height - 1 - 0) × 256 - ...
CH2: y = (top + height - 1 - 100) × 256 - ...
CH3: y = (top + height - 1 - 200) × 256 - ...
```

### 11.3 Inverted Range

**Configuration**:
```
vLow = 100
vHigh = -100
```

**Effect**:
- High values at bottom
- Low values at top
- Inverted display

**Code** (line 1353):
```pascal
if vHigh[j] > vLow[j] then offset := vLow[j] else offset := vHigh[j];
```

Handles inverted ranges correctly.

---

## 12. User Commands

### 12.1 Configuration Commands

| Command | Parameters | Purpose |
|---------|------------|---------|
| `TITLE` | 'string' | Set window title |
| `POS` | x y | Set window position |
| `SIZE` | width height | Set display dimensions (32-2048) |
| `SAMPLES` | count | Set horizontal resolution (16-2048) |
| `RATE` | divisor | Set display update rate (1-2048) |
| `DOTSIZE` | pixels | Set dot diameter (0-32, 0=no dots) |
| `LINESIZE` | pixels | Set line thickness (0-32, 0=no lines) |
| `TEXTSIZE` | size | Set label font size (6-200) |
| `COLOR` | back grid | Set background and grid colors |
| `HIDEXY` | - | Hide mouse coordinates |
| Packing modes | - | Set data packing format (12 modes) |

### 12.2 Runtime Commands

| Command | Parameters | Purpose |
|---------|------------|---------|
| `TRIGGER` | channel {AUTO\|arm fire} {offset} | Configure trigger |
| `HOLDOFF` | count | Set holdoff count (2-2048) |
| `CLEAR` | - | Clear display and reset buffer |
| `SAVE` | {filename} | Save display to BMP file |
| `PC_KEY` | - | Request keyboard state |
| `PC_MOUSE` | - | Request mouse position/color |

### 12.3 Channel Configuration Format

**String Element**:
```
'label' {AUTO | low high} {tall} {base} {grid} {color}
```

---

## 13. Performance Characteristics

### 13.1 Memory Usage

**Sample Buffer**:
```
Y_SampleBuff: 2048 sets × 8 channels × 4 bytes = 64 KB
```

**Channel Configuration**:
```
Arrays (vAuto, vLow, vHigh, etc.): ~8 × 8 × 4 bytes = 256 bytes
Labels: 8 × ~20 bytes = 160 bytes
Total: ~400 bytes
```

**Display Bitmaps**:
```
Typical: 512×256 × 4 bytes × 2 = 1 MB
```

**Total**: ~1.1 MB (typical)

### 13.2 Rendering Performance

**Auto-Ranging Cost**:
```
SCOPE_Range: O(n) where n = SamplePop
Called once per auto-ranging channel per draw
```

**Rendering Cost**:
```
Channels × Samples × DrawLineDot
Example: 4 channels × 512 samples = 2048 calls
```

### 13.3 Optimization Strategies

1. **Disable Auto-Ranging**: Use manual ranges for stable, faster rendering
2. **Rate Limiting**: Reduce update frequency with RATE parameter
3. **Reduce Samples**: Lower vSamples for fewer plot points
4. **Single Channel**: Monitor one signal at a time

---

## 14. Comparison with Other Display Types

### 14.1 SCOPE vs. LOGIC

**SCOPE Advantages**:
- Analog/continuous value visualization
- Auto-ranging for unknown signals
- Per-channel vertical scaling (vTall, vBase)
- Level-based triggering

**LOGIC Advantages**:
- More channels (32 vs. 8)
- Optimized for digital signals
- Edge-based triggering
- Multi-bit range mode

**Use Cases**:
- **SCOPE**: ADC values, temperatures, analog sensors
- **LOGIC**: Digital I/O, communication protocols

### 14.2 SCOPE vs. SCOPE_XY

**SCOPE Advantages**:
- Time-domain display
- Multiple independent channels
- Triggering support

**SCOPE_XY Advantages**:
- XY/polar plotting
- Phase relationship visualization
- Lissajous figures

**Use Cases**:
- **SCOPE**: Signal vs. time
- **SCOPE_XY**: Signal vs. signal (phase, trajectory)

---

## 15. Usage Examples

### 15.1 Basic Single-Channel Scope

**Configuration**:
```
SCOPE 'ADC' AUTO
```

**P2 Code**:
```spin2
repeat
  value := adc_read()
  debug(`scope `value)
```

**Result**: Auto-ranging oscilloscope display of ADC values.

### 15.2 Multi-Channel with Fixed Ranges

**Configuration**:
```
SCOPE SIZE 512 256 SAMPLES 256
      'X' -100 100 128 0 0 $FF0000
      'Y' -100 100 128 128 0 $00FF00
```

**P2 Code**:
```spin2
repeat
  x := accelerometer_x()
  y := accelerometer_y()
  debug(`scope `x `y)
```

**Result**: Two channels (X/Y) with fixed ±100 range, stacked display.

### 15.3 Triggered Capture

**Configuration**:
```
SCOPE SAMPLES 512 'SIGNAL' 0 1023 TRIGGER 0 500 600 256
```

**P2 Code**:
```spin2
repeat
  value := read_signal()
  debug(`scope `value)
```

**Result**: Display updates when signal rises from <500 to >600, showing 256 samples before and after.

### 15.4 High-Speed with Rate Limiting

**Configuration**:
```
SCOPE SAMPLES 1024 RATE 100 'DATA' AUTO
```

**P2 Code**:
```spin2
repeat
  value := fast_sample()
  debug(`scope `value)
  waitx(10)
```

**Result**: Fast sampling, display updates every 100th sample (reduces PC CPU load).

---

## 16. Implementation Details

### 16.1 Data Packing

**Same as LOGIC**: 12 packing modes from LONGS_1BIT to BYTES_4BIT.

**Example** (4 channels, LONGS_8BIT):
```
Each long contains 4 samples (one per channel, 8 bits each)
Efficient for byte-range data (0-255)
```

### 16.2 Fixed-Point Arithmetic

**8.8 Format**: All coordinates use 8.8 fixed-point (left-shifted by 8).

**Example**:
```
x = 100 pixels → x_fixed = 100 << 8 = 25600
```

### 16.3 Sample Set Transmission Protocol

**Element Stream**:
```
ele_num: packed_value_1 (contains samples for all channels)
ele_num: packed_value_2
...
ele_end
```

**Unpacking**: Assembles complete sample sets before storing in buffer.

---

## 17. Element Array Protocol Specification

### 17.1 Protocol Overview

The SCOPE display receives configuration and sample data through an **element array protocol** that uses parallel arrays of types and values.

**Element Storage** (GlobalUnit.pas:126-127):
```pascal
DebugDisplayType:  array[0..DebugDisplayLimit - 1] of integer;
DebugDisplayValue: array[0..DebugDisplayLimit - 1] of integer;
```

**Capacity**: 1100 elements per message

### 17.2 SCOPE Configuration Message Example

```
Element Array:
[0] type=ele_key   value=key_samples     → SAMPLES
[1] type=ele_num   value=512             → horizontal resolution
[2] type=ele_key   value=key_longs_16bit → LONGS_16BIT
[3] type=ele_str   value=<ptr>           → 'Signal1'
[4] type=ele_num   value=$FF0000         → red color
[5] type=ele_str   value=<ptr>           → 'Signal2'
[6] type=ele_num   value=$00FF00         → green color
[7] type=ele_end   value=0
```

### 17.3 SCOPE Sample Data Message Example

```
Element Array:
[0] type=ele_num   value=$00640032       → packed: ch0=100, ch0=50
[1] type=ele_num   value=$FF9CFF38       → packed: ch1=-100, ch1=-200
[2] type=ele_end   value=0
```

---

## 18. Buffer Management and Timing

### 18.1 Circular Buffer Per Channel

SCOPE uses **independent circular buffers** for each channel:

```pascal
SampleBuff: array[0..Channels - 1, 0..SampleSets - 1] of integer;
```

**Dimensions**:
```
Channels = 8                  // Maximum channels
SampleSets = 2048            // Samples per channel
Total size = 8 × 2048 × 4 bytes = 65,536 bytes
```

### 18.2 Write Operations

```pascal
// Store sample for channel
SampleBuff[channel][SamplePtr[channel]] := value;
SamplePtr[channel] := (SamplePtr[channel] + 1) and SamplePtrMask;
if SamplePop[channel] < SampleSets then Inc(SamplePop[channel]);
```

### 18.3 Auto-Ranging Updates

```pascal
// Track min/max for auto-ranging
if value < vMin[channel] then vMin[channel] := value;
if value > vMax[channel] then vMax[channel] := value;

// Periodically recalculate range
if AutoRangeCycle then
begin
  range := vMax[channel] - vMin[channel];
  vScale[channel] := vHeight / range;
end;
```

### 18.4 Trigger Detection

```pascal
if vTrigger and (channel = vTriggerChannel) then
begin
  // Check level crossing
  if (prev_value < vTriggerLevel) and (value >= vTriggerLevel) then
  begin
    // Rising edge trigger
    TriggerPos := SamplePtr[channel];
  end;
end;
```

---

## 19. Bitmap System and Double-Buffering

### 19.1 Bitmap Architecture

```pascal
Bitmap: array[0..1] of TBitmap;  // Double-buffered
```

**Memory Size** (512×512 display):
```
512 × 512 × 4 bytes × 2 bitmaps = 2 MB
```

### 19.2 Trace Rendering

```pascal
for x := 0 to vSamples - 1 do
begin
  // Get sample value
  idx := ((SamplePtr[ch] - vSamples + x) and SamplePtrMask);
  value := SampleBuff[ch][idx];

  // Scale to display
  y := vBase + Round((value - vCenter[ch]) * vScale[ch]);

  // Draw line
  if vLineStyle then
    SmoothLine(x_prev, y_prev, x, y, vDotSize, color, 255)
  else
    SmoothDot(x, y, vDotSize, color, 255);
end;
```

### 19.3 Vertical Scaling

**vTall Parameter**: Scales channel height
```pascal
channel_height := vHeight / vIndex / vTall;
```

**vBase Parameter**: Offsets channel vertically
```pascal
y_offset := vBase * vHeight / 100;
```

---

## 20. Shared Infrastructure

### 20.1 Color System

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

### 20.2 Data Packing System

SCOPE typically uses:
- **LONGS_16BIT**: 2 samples per long (16-bit signed)
- **LONGS_8BIT**: 4 samples per long (8-bit signed)

```pascal
function UnPack(var v: integer): integer;
begin
  Result := v and vPackMask;
  if (Result shr (vPackSize - 1)) <> 0 then
    Result := Result or (not vPackMask);  // Sign-extend
  Inc(vPackIndex);
  if vPackIndex < vPackCount then
    v := v shr vPackSize
  else
    vPackIndex := 0;
end;
```

### 20.3 Fixed-Point Arithmetic

**8.8 fixed-point** for sub-pixel rendering:
```pascal
x := sample_index * pixel_width * 256;
y := channel_y_position * 256;
```

---

## 21. Initialization Lifecycle

### 21.1 Window Creation Sequence

```pascal
// 1. Form instantiation
DebugDisplayForm := TDebugDisplayForm.Create(Application);
DebugDisplayForm.DisplayType := dis_scope;

// 2. Set defaults
vWidth := 512;
vHeight := 512;
vSamples := 256;
vTall := 1;
vBase := 0;
vDotSize := 4;
vLineStyle := True;
vTrigger := False;

// 3. Call SCOPE_Configure
SCOPE_Configure;

// 4. Create bitmaps
Bitmap[0].SetSize(vBitmapWidth, vBitmapHeight);
Bitmap[1].SetSize(vBitmapWidth, vBitmapHeight);

// 5. Initialize buffers
for ch := 0 to Channels - 1 do
begin
  SamplePtr[ch] := 0;
  SamplePop[ch] := 0;
  vAuto[ch] := True;  // Auto-ranging enabled
end;

// 6. Show window
Show;
```

### 21.2 Configuration Parameter Processing

```pascal
while not NextEnd do
begin
  if NextKey then
  case val of
    key_samples:     KeyValWithin(vSamples, 4, 2047);
    key_tall:        KeyValWithin(vTall, 1, 8);
    key_base:        KeyValWithin(vBase, -100, 100);
    key_dotsize:     KeyValWithin(vDotSize, 2, 20);
    key_trigger:     KeyTrigger;
    key_line:        vLineStyle := True;
    key_dot:         vLineStyle := False;
    key_longs_1bit..key_bytes_4bit:  KeyPack;
  end
  else if NextStr then  // Channel label
  begin
    if vIndex <> Channels then Inc(vIndex);
    vLabel[vIndex - 1] := PChar(val);
    KeyColor(vColor[vIndex - 1]);
    KeyRange;  // Optional RANGE for manual scaling
  end;
end;
```

### 21.3 Auto-Ranging Initialization

```pascal
for ch := 0 to vIndex - 1 do
begin
  if vAuto[ch] then
  begin
    vMin[ch] := MaxInt;
    vMax[ch] := MinInt;
    vCenter[ch] := 0;
    vScale[ch] := 1.0;
  end;
end;
```

### 21.4 Trigger Initialization

```pascal
procedure KeyTrigger;
begin
  vTrigger := True;
  if NextNum then vTriggerChannel := Within(val, 0, vIndex - 1);
  if NextNum then vTriggerLevel := val;
  if NextNum then vTriggerPos := Within(val, 0, SampleSets);
  if NextNum then vTriggerHoldoff := Within(val, 0, 1000);
  vTriggerRising := True;  // Default: rising edge
end;
```

### 21.5 Cleanup and Destruction

```pascal
// Window Close
FormClosing := True;
Bitmap[0].Free;
Bitmap[1].Free;
Form.Free;
```

---

## 22. Summary

The **SCOPE** display window is a comprehensive multi-channel oscilloscope for the Propeller 2 debug environment, providing real-time analog signal visualization with automatic and manual scaling, level-based triggering, and flexible display control.

**Key Capabilities**:
- Up to 8 analog channels with independent configuration
- Auto-ranging or manual range specification per channel
- Level-based triggering with rising/falling edge detection
- Vertical scaling (vTall) and offset (vBase) for channel overlay
- 2048-sample circular buffer per channel
- Rate limiting and holdoff for display control
- Anti-aliased trace rendering with lines and/or dots

**Performance Profile**:
- 64 KB sample buffer
- Auto-ranging: O(n) per channel per draw
- Rendering: O(channels × samples)
- Efficient for 4-8 channels at 256-512 samples

**Common Use Cases**:
- ADC monitoring and visualization
- Sensor data logging (temperature, pressure, etc.)
- Signal waveform analysis
- Multi-channel comparison
- Triggered event capture

The SCOPE window integrates seamlessly with the P2 debug ecosystem, providing oscilloscope-grade visualization for analog signal debugging and analysis.

---

**End of SCOPE Theory of Operations**
