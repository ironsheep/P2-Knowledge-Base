# P2 DEBUG System - Comprehensive Guide

## Three Types of Debugging in Spin2/PASM

### 1. DEBUG Statements (Serial Output)
### 2. Single-Step PASM Debugger
### 3. DEBUG Displays (Graphical Windows)

---

## Type 1: DEBUG Statements - Formatted Serial Output

### Overview
- Serial output on P62 at 2 Mbaud (configurable)
- Works in both Spin2 and PASM code
- Up to 255 DEBUG() statements per application
- Always prefixed with "CogN  " and ends with CR+LF

### Basic Syntax

#### Spin2 DEBUG
```spin2
DEBUG("Hello from Spin2")
DEBUG(UDEC(x))                    ' Outputs: "x = 123"
DEBUG(UHEX(value))                ' Outputs: "value = $ABC"
DEBUG(SDEC(a, b, c))              ' Multiple values
DEBUG(UDEC_(x))                   ' Just value, no label: "123"
```

#### PASM DEBUG
```pasm
DEBUG("Hello from PASM")
DEBUG(UDEC(register))             ' Register value
DEBUG(UHEX(#123))                 ' Immediate value
DEBUG(UDEC(PA, PB))               ' Multiple registers
```

### Output Formatters

| Command | Description | Example Output |
|---------|-------------|----------------|
| UDEC | Unsigned decimal | "x = 123" |
| SDEC | Signed decimal | "x = -456" |
| UHEX | Unsigned hex | "x = $1ABC" |
| SHEX | Signed hex | "x = -$234" |
| UBIN | Unsigned binary | "x = %1010" |
| SBIN | Signed binary | "x = -%0101" |
| FDEC | Floating point | "x = 3.14159" |
| STR/ZSTR | String output | "Hello World" |

### Size Modifiers
- _BYTE - 8-bit display
- _WORD - 16-bit display  
- _LONG - 32-bit display (default)

Example: `UHEX_BYTE(x)` displays as 8-bit hex

### Array/Memory Display
```spin2
' Hub memory arrays
DEBUG(UHEX_BYTE_ARRAY(@buffer, 16))  ' Show 16 bytes
DEBUG(UDEC_LONG_ARRAY(@data, count)) ' Show longs

' PASM register arrays
DEBUG(UHEX_REG_ARRAY(first_reg, 8))  ' Show 8 registers
```

### Conditional Output
```spin2
DEBUG(IF(condition), "This only outputs if true")
DEBUG(IFNOT(flag), "This outputs if flag is false")
DEBUG("Always", IF(x > 10), ", x is big")  ' Partial gating
```

### Timing Control
```spin2
DEBUG("Status", DLY(1000))  ' Delay 1 second after output
```

### Configuration Symbols

| Symbol | Purpose | Default |
|--------|---------|----------|
| DEBUG_BAUD | Serial baud rate | 2_000_000 |
| DEBUG_PIN | Output pin | 62 |
| DEBUG_TIMESTAMP | Add timestamps | not defined |
| DEBUG_COGS | Limit which cogs debug | all cogs |
| DEBUG_DELAY | Startup delay | 0 ms |

---

## Type 2: Single-Step PASM Debugger

### Invocation Methods

1. **Manual Invocation**
   ```spin2
   DEBUG        ' No parentheses - enters debugger
   ```
   
2. **Automatic on COGINIT**
   ```spin2
   CON
     DEBUG_COGINIT = 1  ' Every cog enters debugger on start
   ```
   
3. **Main-Only Mode**
   ```spin2
   CON
     DEBUG_MAIN = 1     ' Ready to single-step, ignores DEBUG commands
   ```

### Debugger Features

#### Display Areas
1. **Register Display** - Shows cog registers with highlighting for changes
2. **Code Window** - Shows PASM code with current instruction highlighted
3. **Memory Window** - Hub/cog/LUT memory viewing
4. **Stack Display** - Hardware stack contents
5. **Status Line** - C/Z flags, PC, interrupt states

#### Control Commands

| Key | Action |
|-----|--------|
| Space | Single step |
| Enter | Run to breakpoint |
| G | Go (run freely) |
| Q | Quit debugger |
| M | Switch memory view (Hub/Cog/LUT) |
| R | Reset cog |
| I | Step into call |
| O | Step over call |
| U | Run until return |

#### Memory Navigation
- Arrow keys: Move cursor
- Page Up/Down: Scroll memory
- Home/End: Jump to start/end
- Type address to jump directly

#### Breakpoints
- Click on instruction to toggle breakpoint
- Conditional breakpoints on register values
- Break on memory access

### Multi-Cog Debugging
- Each cog gets its own debugger window
- Windows are independent
- Can debug multiple cogs simultaneously
- Cogs can debug each other non-invasively

### Performance Note
**CRITICAL**: Set USB Serial Port Latency Timer to 1ms (not default 16ms) in Windows Device Manager for good performance!

---

## Type 3: DEBUG Displays (Graphical Windows)

### Overview
- Up to 32 simultaneous graphical displays
- Animated, real-time data visualization
- Each display is a separate window
- Data continuously fed for animation

### Display Types Available (9 Total)

#### 1. LOGIC Display - Logic Analyzer
```spin2
DEBUG(`LOGIC MyLogic TITLE 'Pin States' SAMPLES 256 'P0' 1 'P1' 1 'P2' 1)
DEBUG(`LOGIC MyLogic `(pins))  ' Update with data
```

**Features**:
- Multiple channels (up to 32)
- Adjustable sample depth
- Trigger conditions
- Zoom and pan
- Measure timing

#### 2. SCOPE Display - Oscilloscope
```spin2
DEBUG(`SCOPE MyScope TITLE 'Waveform' SAMPLES 512 TRIGGER 128)
DEBUG(`SCOPE MyScope `(value))  ' Feed samples
```

**Features**:
- 1-8 channels
- Adjustable time base
- Trigger on level with hysteresis
- Measurements (frequency, amplitude)

#### 3. SCOPE_XY Display - XY Oscilloscope
```spin2
DEBUG(`SCOPE_XY MyXY RANGE 500 POLAR 360 'X' 'Y' 'Z')
DEBUG(`SCOPE_XY MyXY `(x) `(y) `(z))  ' Plot XY points
```

**Features**:
- 1-8 channels for multi-dimensional plotting
- Persistence control (0-512 samples)
- Polar mode for circular displays
- Log scale mode
- Perfect for Lissajous patterns
- Phase relationship visualization

#### 4. FFT Display - Spectrum Analyzer
```spin2
DEBUG(`FFT MyFFT TITLE 'Spectrum' SAMPLES 1024 LOGSCALE)
DEBUG(`FFT MyFFT `(sample))  ' Feed time-domain data
```

**Features**:
- Real-time FFT
- Linear/log scale
- Peak detection
- Frequency measurement

#### 5. SPECTRO Display - Spectrogram
```spin2
DEBUG(`SPECTRO MySpectro TITLE 'Waterfall' SIZE 512 256)
DEBUG(`SPECTRO MySpectro `(sample))
```

**Features**:
- Waterfall display
- Color-coded intensity
- Time-frequency visualization

#### 6. PLOT Display - XY Plotter
```spin2
DEBUG(`PLOT MyPlot TITLE 'Data Plot' SIZE 640 480 RANGE -100 100)
DEBUG(`PLOT MyPlot `(x) `(y))  ' Plot point
```

**Features**:
- Scatter plots
- Line plots
- Multiple series
- Auto-scaling

#### 7. TERM Display - Terminal Window
```spin2
DEBUG(`TERM MyTerm TITLE 'Terminal' SIZE 80 25)
DEBUG(`TERM MyTerm 'Hello World' 13)  ' Output text
```

**Features**:
- Text display
- ANSI color codes
- Scrolling
- Keyboard input via PC_KEY()

#### 8. BITMAP Display - Graphical Display
```spin2
DEBUG(`BITMAP MyBitmap TITLE 'Graphics' SIZE 320 240 RGBI8)
DEBUG(`BITMAP MyBitmap `(@buffer))  ' Display image
```

**Features**:
- Multiple color formats
- Real-time updates
- Scaling
- Image processing visualization

#### 9. MIDI Display - MIDI Keyboard Monitor
```spin2
DEBUG(`MIDI MyMidi SIZE 3 RANGE 36 84)  ' 3 octaves, C2 to C6
DEBUG(`MIDI MyMidi $90 `(note) `(velocity))  ' Note on
DEBUG(`MIDI MyMidi $80 `(note) `(0))         ' Note off
```

**Features**:
- Visual keyboard display
- Note on/off status
- Velocity visualization
- MIDI channel selection (0-15)
- Adjustable keyboard range (0-127)
- Size control (1-50 octaves)

### Display Configuration

#### Common Keywords

| Keyword | Purpose | Example |
|---------|---------|----------|
| TITLE | Window title | TITLE 'My Display' |
| POS | Screen position | POS 100 50 |
| SIZE | Display size | SIZE 640 480 |
| SAMPLES | Buffer size | SAMPLES 1024 |
| RANGE | Value range | RANGE -100 100 |
| COLOR | Trace color | COLOR $FF0000 |
| TRIGGER | Trigger level | TRIGGER 128 |

### Display Syntax Options

#### Backtick Syntax (Cleaner)
```spin2
DEBUG(`SCOPE MyScope `(value))     ' Clean, no "CogN" prefix
```

#### Regular Syntax (Verbose)
```spin2
DEBUG("`SCOPE MyScope ", SDEC_(value))  ' Includes "CogN" prefix
```

### Update Patterns

#### Continuous Updates
```spin2
REPEAT
  sample := GetADC()
  DEBUG(`SCOPE MyScope `(sample))
  WAITMS(1)
```

#### Batch Updates
```spin2
REPEAT i FROM 0 TO 255
  buffer[i] := GetSample()
DEBUG(`SCOPE MyScope `(@buffer) SAMPLES 256)
```

### PC Input Integration

```spin2
' Read PC keyboard/mouse in displays
key := PC_KEY()         ' Get keyboard state
mx, my := PC_MOUSE()   ' Get mouse position

DEBUG(`TERM MyTerm PC_KEY `(key))  ' Show key pressed
```

---

## Advanced Debug Features

### Timestamp Support
```spin2
CON
  DEBUG_TIMESTAMP = 1   ' Add timestamps to all output
```
Output: `[00001234] Cog0  x = 123`

### Cog Filtering
```spin2
CON
  DEBUG_COGS = %00001111  ' Only debug cogs 0-3
```

### Output Redirection
```spin2
CON
  DEBUG_PIN = 30         ' Use different pin
  DEBUG_BAUD = 115200    ' Different baud rate
```

### Lock Usage
LOCK[15] is reserved for DEBUG system coordination between cogs.

### Clock Frequency Tracking
P63 holds clock frequency in long-repository mode for debug system.

---

## Usage Examples

### Example 1: Basic Value Monitoring
```spin2
PUB main() | value
  REPEAT
    value := GetSensor()
    DEBUG(UDEC(value), DLY(100))  ' Output every 100ms
```

### Example 2: Logic Analyzer for SPI
```spin2
PUB spi_monitor()
  DEBUG(`LOGIC SPI TITLE 'SPI Bus' 'CLK' 1 'MOSI' 1 'MISO' 1 'CS' 1)
  REPEAT
    pins := INA[3..0]
    DEBUG(`LOGIC SPI `(pins))
```

### Example 3: Real-Time Waveform
```spin2
PUB waveform() | t, value
  DEBUG(`SCOPE Wave TITLE 'Sine Wave' SAMPLES 256 RANGE -100 100)
  REPEAT t FROM 0 TO 359
    value := QSIN(t * $100_0000, 100)
    DEBUG(`SCOPE Wave `(value))
    WAITMS(10)
```

### Example 4: Multi-Cog Debugging
```spin2
CON
  DEBUG_COGINIT = 1  ' Auto-debug each cog

PUB main()
  COGSPIN(NEWCOG, worker(), @stack1)
  COGSPIN(NEWCOG, worker(), @stack2)
  
PRI worker()
  DEBUG  ' Enter debugger manually
  ' Each cog gets its own debugger window
```

---

## Key Insights

1. **Three Distinct Systems** working together:
   - Text output (DEBUG statements)
   - Interactive debugging (PASM debugger)
   - Visual displays (DEBUG Displays)

2. **No External Hardware Needed**:
   - Logic analyzer built-in
   - Oscilloscope built-in
   - Spectrum analyzer built-in

3. **Real-Time Performance**:
   - 2 Mbaud serial
   - ~10,000 messages/second capability
   - Hardware-assisted via BRK instruction

4. **Multi-Cog Aware**:
   - Each cog can debug independently
   - Shared coordination via LOCK[15]
   - Non-invasive cog monitoring

5. **Integrated with IDE**:
   - Ctrl+F10 to run with debug
   - Windows open automatically
   - Data flows directly to displays

This is a complete debugging ecosystem unmatched in any other microcontroller!