# P2 DEBUG Displays - Complete Command Catalog

## Overview
The P2 DEBUG system supports graphical display windows for real-time data visualization. Each display type has two distinct command forms:
1. **Display Creation Command** - Creates a window with a user-defined instance name
2. **Display Update Commands** - Updates the specific named window instance

## Critical Concept: Instance Names

**CREATION**: Uses display type + creates instance name
```spin2
DEBUG(`LOGIC MyLogicAnalyzer ...)     ' Creates instance "MyLogicAnalyzer"
DEBUG(`SCOPE OscilloscopeA ...)       ' Creates instance "OscilloscopeA"
```

**UPDATES**: Uses the instance name only (NOT the display type)
```spin2
DEBUG(`MyLogicAnalyzer `(data))       ' Updates "MyLogicAnalyzer" instance
DEBUG(`OscilloscopeA `(value))        ' Updates "OscilloscopeA" instance
```

The backtick (`) syntax provides cleaner output without "CogN" prefix.

## Critical Concept: Update Command Flexibility

**Update commands are compositional** - developers combine parameters, keywords, and values as needed:

```spin2
' Simple single value
DEBUG(`MyScope `(value))

' Multiple values
DEBUG(`MyScope `(ch1) `(ch2) `(ch3))

' Keywords with parameters
DEBUG(`MyScope TRIGGER `(level) HOLDOFF `(count) `(value))

' Mixed operations
DEBUG(`MyTerm GOTOXY `(x) `(y) COLOR `(fg) `(bg) 'Text' `(value))

' Complex aggregations
DEBUG(`MyLogic LONGS_8BIT `(@buffer) `(32) TRIGGER `(pattern))
```

The actual syntax depends on what the developer wants to visualize and how they want to control the display. The following sections show common patterns, but these can be combined in many ways.

## Complete Display Types Catalog

### 1. LOGIC Display - Logic Analyzer

#### Creation Command
```spin2
DEBUG(`LOGIC name [configuration] 'channel_name' bits ['channel2' bits2...])
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'SPI Monitor' |
| POS | Window position | POS 100 200 |
| SIZE | Display dimensions | SIZE 800 400 |
| SAMPLES | Number of samples | SAMPLES 256 |
| RATE | Sample rate divider | RATE 4 |
| COLOR | Trace colors | COLOR GREEN |
| TRIGGER | Trigger configuration | TRIGGER $FF |
| HOLDOFF | Trigger holdoff | HOLDOFF 100 |
| RANGES | Value ranges | RANGES 0 255 |
| LABELS | Show labels | LABELS ON |
| LINESIZE | Line thickness | LINESIZE 2 |
| TEXTSIZE | Text size | TEXTSIZE 12 |
| BACKCOLOR | Background color | BACKCOLOR BLACK |
| GRIDCOLOR | Grid color | GRIDCOLOR GRAY |

#### Channel Definition
- `'channel_name' bits` - Define channel with name and bit count
- Bits can be 1-32 for each channel
- Maximum 32 channels total

#### Update Commands - Common Patterns

**Note**: These are common patterns, but developers often combine these in various ways depending on their needs.

**Value Updates:**
```spin2
DEBUG(`instance_name `(value))                       ' Single value
DEBUG(`instance_name `(value1) `(value2) ...)       ' Multiple channels
DEBUG(`instance_name KEYWORD `(param) `(value))     ' Keyword + value
```

**Packed Data Formats:**
```spin2
DEBUG(`instance_name PACK_FORMAT `(@buffer) `(count))
DEBUG(`instance_name PACK_FORMAT `(@buffer) `(count) TRIGGER `(pattern))
```

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name from creation | Any valid name |
| value | integer | Channel data value | 0 to 2^bits-1 |
| @buffer | address | Hub memory address | Valid hub address |
| count | integer | Number of packed units | 1 to buffer size |
| PACK_FORMAT | keyword | Data packing format | See table below |

#### Packing Formats Table

| Format | Description | Samples per Unit |
|--------|-------------|------------------|
| BYTES_2BIT | 2-bit samples in bytes | 4 samples/byte |
| BYTES_4BIT | 4-bit samples in bytes | 2 samples/byte |
| WORDS_2BIT | 2-bit samples in words | 8 samples/word |
| WORDS_4BIT | 4-bit samples in words | 4 samples/word |
| WORDS_8BIT | 8-bit samples in words | 2 samples/word |
| LONGS_2BIT | 2-bit samples in longs | 16 samples/long |
| LONGS_4BIT | 4-bit samples in longs | 8 samples/long |
| LONGS_8BIT | 8-bit samples in longs | 4 samples/long |
| LONGS_16BIT | 16-bit samples in longs | 2 samples/long |

#### Example
```spin2
' CREATION: Define a logic analyzer instance named "SPI_Monitor"
DEBUG(`LOGIC SPI_Monitor TITLE 'SPI Bus' SAMPLES 512 'CLK' 1 'MOSI' 1 'MISO' 1 'CS' 1)

' UPDATE: Send data to the "SPI_Monitor" instance
pins := INA[3..0]
DEBUG(`SPI_Monitor `(pins))              ' Note: just instance name, no "LOGIC"
```

---

### 2. SCOPE Display - Oscilloscope

#### Creation Command
```spin2
DEBUG(`SCOPE name [configuration] 'channel_name' range height offset flags [more channels...])
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'Waveform' |
| POS | Window position | POS 0 0 |
| SIZE | Display size | SIZE 640 480 |
| SAMPLES | Samples per screen | SAMPLES 256 |
| TRIGGER | Trigger level | TRIGGER 128 |
| HOLDOFF | Trigger holdoff | HOLDOFF 50 |
| COLOR | Trace color | COLOR YELLOW |
| BACKCOLOR | Background | BACKCOLOR BLACK |
| GRIDCOLOR | Grid color | GRIDCOLOR GRAY |
| TEXTSIZE | Text size | TEXTSIZE 10 |
| LINESIZE | Line width | LINESIZE 1 |
| DOT | Dot mode | DOT |
| LINE | Line mode | LINE |
| SOLID | Solid fill | SOLID |

#### Channel Parameters
- `'name'` - Channel label
- `range` - Two values: min max (e.g., 0 255)
- `height` - Display height in pixels
- `offset` - Vertical offset in pixels
- `flags` - %TLBR (Top/Legend/Bottom/Right) grid lines

#### Update Commands - Common Patterns

**Flexible Composition Examples:**
```spin2
' Simple values
DEBUG(`instance_name `(value))
DEBUG(`instance_name `(ch1) `(ch2) ... `(ch8))

' With control keywords
DEBUG(`instance_name TRIGGER `(level) `(value))
DEBUG(`instance_name HOLDOFF `(samples) TRIGGER `(level) `(value))

' Buffer updates with options
DEBUG(`instance_name `(@buffer))
DEBUG(`instance_name `(@buffer) SAMPLES `(count))
DEBUG(`instance_name `(@buffer) SAMPLES `(count) TRIGGER `(level))
```

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name from creation | Any valid name |
| value/ch1..ch8 | number | Sample values | Integer or float |
| @buffer | address | Hub address of sample array | Valid hub address |
| count | integer | Number of samples | 1 to SAMPLES max |
| level | number | Trigger threshold | Within channel range |
| samples | integer | Holdoff count | 0 to 65535 |

#### Update Keywords Table

| Keyword | Purpose | Parameters | Usage |
|---------|---------|------------|-------|
| SAMPLES | Specify sample count | count | Buffer updates |
| TRIGGER | Set trigger level | level | Before data |
| HOLDOFF | Set trigger holdoff | samples | Before data |

#### Example
```spin2
' CREATION: Define an oscilloscope instance named "WaveMonitor"
DEBUG(`SCOPE WaveMonitor TITLE 'Signals' SAMPLES 256 'CH1' 0 255 100 10 %1111 'CH2' -128 127 100 130 %1111)

' UPDATE: Send samples to "WaveMonitor" instance
DEBUG(`WaveMonitor `(adc1) `(adc2))     ' Note: just instance name, no "SCOPE"
```

---

### 3. SCOPE_XY Display - XY Oscilloscope

#### Creation Command
```spin2
DEBUG(`SCOPE_XY name [configuration] 'x_channel' 'y_channel' ['z_channel'...])
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'XY Plot' |
| POS | Window position | POS 200 100 |
| SIZE | Display size | SIZE 400 400 |
| RANGE | Value range | RANGE 1000 |
| SAMPLES | Persistence | SAMPLES 512 |
| POLAR | Polar divisions | POLAR 360 |
| LOGSCALE | Log scaling | LOGSCALE |
| COLOR | Trace color | COLOR CYAN |
| DOTSIZE | Dot size | DOTSIZE 2 |
| LINESIZE | Line width | LINESIZE 1 |

#### Update Commands - Common Patterns

**Flexible Composition Examples:**
```spin2
' Point plotting variations
DEBUG(`instance_name `(x) `(y))
DEBUG(`instance_name `(x) `(y) `(z))
DEBUG(`instance_name `(x) `(y) `(z) `(w))

' Buffer updates
DEBUG(`instance_name `(@xy_buffer) POINTS `(count))
DEBUG(`instance_name `(@xyz_buffer) POINTS3D `(count))

' Control commands (can be combined with data)
DEBUG(`instance_name CLEAR)
DEBUG(`instance_name CLEAR `(x) `(y))  ' Clear then plot
DEBUG(`instance_name RESET `(@buffer) POINTS `(count))  ' Reset then buffer
```

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name | Any valid name |
| x, y, z, w | number | Coordinate values | Integer or float |
| @xy_buffer | address | Interleaved XY pairs | Valid hub address |
| @xyz_buffer | address | Interleaved XYZ triplets | Valid hub address |
| count | integer | Number of points | 1 to buffer size |

#### Update Commands Table

| Command | Purpose | Parameters | Effect |
|---------|---------|------------|--------|
| POINTS | XY buffer update | @buffer, count | Plot XY pairs |
| POINTS3D | XYZ buffer update | @buffer, count | Plot XYZ triplets |
| CLEAR | Clear display | None | Erase persistence |
| RESET | Reset origin | None | Return to center |

#### Example
```spin2
' CREATION: Define XY scope instance named "Lissajous"
DEBUG(`SCOPE_XY Lissajous TITLE 'Phase' RANGE 100 SAMPLES 256 'X' 'Y')

' UPDATE: Send XY coordinates to "Lissajous" instance
angle := angle + 1
x := QSIN(angle, 100)
y := QCOS(angle, 100)
DEBUG(`Lissajous `(x) `(y))              ' Note: just instance name, no "SCOPE_XY"
```

---

### 4. FFT Display - Spectrum Analyzer

#### Creation Command
```spin2
DEBUG(`FFT name [configuration] 'channel_name')
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'Spectrum' |
| POS | Window position | POS 0 300 |
| SIZE | Display size | SIZE 640 200 |
| SAMPLES | FFT size | SAMPLES 1024 |
| RATE | Sample rate | RATE 48000 |
| LOGSCALE | Log frequency | LOGSCALE |
| MAGNITUDE | Mag display | MAGNITUDE |
| PHASE | Phase display | PHASE |
| WINDOW | Window function | WINDOW HAMMING |
| COLOR | Trace color | COLOR GREEN |
| RANGE | dB range | RANGE 0 120 |

#### Window Functions
- RECTANGULAR, HAMMING, HANNING, BLACKMAN, BARTLETT

#### Update Commands - Common Patterns

**Flexible Composition Examples:**
```spin2
' Time-domain samples
DEBUG(`instance_name `(sample))
DEBUG(`instance_name `(@buffer))
DEBUG(`instance_name `(@buffer) SAMPLES `(count))

' Frequency-domain data
DEBUG(`instance_name SPECTRUM `(@freq_buffer) BINS `(count))
DEBUG(`instance_name MAG `(@mag_buffer) PHASE `(@phase_buffer) BINS `(count))

' Control operations
DEBUG(`instance_name CLEAR)
DEBUG(`instance_name AVERAGE `(n) `(sample))
DEBUG(`instance_name PEAK_HOLD SPECTRUM `(@freq_buffer) BINS `(count))
```

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name | Any valid name |
| sample | number | Time-domain sample | Integer or float |
| @buffer | address | Time-domain samples | Valid hub address |
| @freq_buffer | address | Frequency bin data | Valid hub address |
| @mag_buffer | address | Magnitude array | Valid hub address |
| @phase_buffer | address | Phase array | Valid hub address |
| count | integer | Sample/bin count | 1 to FFT size |
| n | integer | Averaging count | 1 to 256 |

#### Update Commands Table

| Command | Purpose | Parameters | Effect |
|---------|---------|------------|--------|
| SAMPLES | Specify sample count | count | Time-domain buffer |
| SPECTRUM | Pre-computed FFT | @buffer, count | Frequency bins |
| MAG | Magnitude data | @buffer | Magnitude array |
| PHASE | Phase data | @buffer | Phase array |
| BINS | Bin count | count | Number of bins |
| CLEAR | Clear display | None | Erase data |
| AVERAGE | Set averaging | n | Average n frames |
| PEAK_HOLD | Enable peaks | None | Hold peak values |
| PEAK_RESET | Reset peaks | None | Clear peak hold |

#### Example
```spin2
' CREATION: Define FFT analyzer instance named "AudioSpectrum"
DEBUG(`FFT AudioSpectrum TITLE 'Audio FFT' SAMPLES 1024 LOGSCALE WINDOW HAMMING 'Audio')

' UPDATE: Feed ADC samples to "AudioSpectrum" instance
sample := GETADC(pin)
DEBUG(`AudioSpectrum `(sample))          ' Note: just instance name, no "FFT"
```

---

### 5. SPECTRO Display - Spectrogram/Waterfall

#### Creation Command
```spin2
DEBUG(`SPECTRO name [configuration])
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'Waterfall' |
| POS | Window position | POS 100 100 |
| SIZE | Display size | SIZE 512 256 |
| SAMPLES | FFT size | SAMPLES 512 |
| RATE | Sample rate | RATE 44100 |
| LOGSCALE | Log frequency | LOGSCALE |
| RANGE | Intensity range | RANGE 0 100 |
| COLORMAP | Color palette | COLORMAP JET |

#### Color Maps
- GRAY, JET, HOT, COOL, SPRING, SUMMER, AUTUMN, WINTER

#### Update Commands - Common Patterns

**Flexible Composition Examples:**
```spin2
' Time-domain input
DEBUG(`instance_name `(sample))
DEBUG(`instance_name `(@buffer))
DEBUG(`instance_name `(@buffer) SAMPLES `(count))

' Frequency line input
DEBUG(`instance_name LINE `(@freq_line) BINS `(count))
DEBUG(`instance_name LINE `(@freq_line) BINS `(count) SCROLL)

' Display control
DEBUG(`instance_name CLEAR)
DEBUG(`instance_name PAUSE)
DEBUG(`instance_name GAIN `(factor) `(sample))
```

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name | Any valid name |
| sample | number | Time-domain sample | Integer or float |
| @buffer | address | Time-domain buffer | Valid hub address |
| @freq_line | address | Frequency bin array | Valid hub address |
| count | integer | Sample/bin count | 1 to buffer size |
| factor | float | Gain multiplier | 0.1 to 10.0 |

#### Update Commands Table

| Command | Purpose | Parameters | Effect |
|---------|---------|------------|--------|
| SAMPLES | Sample count | count | Buffer size |
| LINE | Frequency line | @buffer, count | One spectral line |
| BINS | Bin count | count | Frequency bins |
| SCROLL | Scroll left | None | Shift display |
| CLEAR | Clear display | None | Erase all |
| PAUSE | Pause scroll | None | Stop scrolling |
| RESUME | Resume scroll | None | Start scrolling |
| GAIN | Set gain | factor | Intensity scale |

#### Example
```spin2
' CREATION: Define spectrogram instance named "VoiceAnalyzer"
DEBUG(`SPECTRO VoiceAnalyzer TITLE 'Voice Print' SIZE 640 480 SAMPLES 512 COLORMAP JET)

' UPDATE: Stream audio samples to "VoiceAnalyzer" instance
REPEAT
  sample := GETADC(mic_pin)
  DEBUG(`VoiceAnalyzer `(sample))        ' Note: just instance name, no "SPECTRO"
```

---

### 6. PLOT Display - XY Data Plotter

#### Creation Command
```spin2
DEBUG(`PLOT name [configuration] 'series_name' [more series...])
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'Data Plot' |
| POS | Window position | POS 50 50 |
| SIZE | Display size | SIZE 800 600 |
| RANGE | Y-axis range | RANGE -100 100 |
| XRANGE | X-axis range | XRANGE 0 1000 |
| SAMPLES | Points shown | SAMPLES 1000 |
| COLOR | Series color | COLOR RED |
| STYLE | Plot style | STYLE LINES |
| DOTSIZE | Point size | DOTSIZE 3 |
| LINESIZE | Line width | LINESIZE 2 |
| GRID | Show grid | GRID ON |

#### Plot Styles
- DOTS, LINES, LINESPOINTS, IMPULSES, STEPS, BOXES, HISTOGRAM

#### Update Commands - Common Patterns

**Flexible Composition Examples:**
```spin2
' Point plotting
DEBUG(`instance_name `(x) `(y))
DEBUG(`instance_name `(x) `(y1) `(y2) ... `(y8))
DEBUG(`instance_name SERIES `(n) `(x) `(y))

' Buffer updates
DEBUG(`instance_name `(@xy_buffer) POINTS `(count))
DEBUG(`instance_name SERIES `(n) `(@buffer) POINTS `(count))

' Display control
DEBUG(`instance_name CLEAR)
DEBUG(`instance_name AUTO XRANGE `(min) `(max))
DEBUG(`instance_name MARKER `(x) `(y) `(type) LABEL `(x) `(y) 'text')
```

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name | Any valid name |
| x, y | number | Coordinate values | Integer or float |
| n | integer | Series number | 1 to 8 |
| @xy_buffer | address | XY pairs array | Valid hub address |
| count | integer | Number of points | 1 to buffer size |
| min, max | number | Range limits | Any numeric value |
| type | integer | Marker type | 0=dot, 1=cross, 2=square, 3=diamond |
| color | integer | RGB color | $000000 to $FFFFFF |

#### Update Commands Table

| Command | Purpose | Parameters | Effect |
|---------|---------|------------|--------|
| SERIES | Select series | n | Target series 1-8 |
| POINTS | Buffer update | count | Plot XY pairs |
| CLEAR | Clear data | [SERIES n] | Clear all or one |
| AUTO | Auto-scale | None | Scale both axes |
| AUTOX | Auto-scale X | None | Scale X only |
| AUTOY | Auto-scale Y | None | Scale Y only |
| XRANGE | Set X range | min, max | X axis limits |
| YRANGE | Set Y range | min, max | Y axis limits |
| MARKER | Add marker | x, y, type | Place marker |
| LABEL | Add text | x, y, 'text' | Place label |
| VLINE | Vertical line | x, color | Draw vertical |
| HLINE | Horizontal line | y, color | Draw horizontal |

#### Example
```spin2
' CREATION: Define plot instance named "TempMonitor"
DEBUG(`PLOT TempMonitor TITLE 'Temperature' RANGE 0 100 SAMPLES 3600 STYLE LINES 'Sensor1' 'Sensor2')

' UPDATE: Add data points to "TempMonitor" instance
x := GETCT() / clkfreq
y1 := ReadTemp(0)
y2 := ReadTemp(1)
DEBUG(`TempMonitor `(x) `(y1) `(x) `(y2))  ' Note: just instance name, no "PLOT"
```

---

### 7. TERM Display - Terminal Window

#### Creation Command
```spin2
DEBUG(`TERM name [configuration])
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'Console' |
| POS | Window position | POS 0 0 |
| SIZE | Character dimensions | SIZE 80 25 |
| TEXTSIZE | Font size | TEXTSIZE 14 |
| COLOR | Text color | COLOR WHITE |
| BACKCOLOR | Background | BACKCOLOR BLACK |
| CURSOR | Cursor style | CURSOR BLOCK |
| ECHO | Local echo | ECHO ON |
| WRAP | Line wrap | WRAP ON |

#### Update Commands - Common Patterns

**Flexible Composition Examples:**
```spin2
' Text output
```spin2
DEBUG(`instance_name 'text string')                      ' String literal
DEBUG(`instance_name `(char))                            ' Single character
DEBUG(`instance_name `(@string))                         ' String from hub
DEBUG(`instance_name ZSTR `(@string))                    ' Zero-terminated string
DEBUG(`instance_name LSTR `(@string) `(length))         ' Length-specified string
```

' Cursor control
```spin2
DEBUG(`instance_name CLS)                                ' Clear screen (char 0)
DEBUG(`instance_name HOME)                               ' Home cursor (char 1)
DEBUG(`instance_name GOTOXY `(x) `(y))                  ' Position cursor (2,x,y)
DEBUG(`instance_name CURSORLEFT)                        ' Move left (char 8)
DEBUG(`instance_name TAB)                                ' Tab (char 9)
DEBUG(`instance_name LF)                                 ' Line feed (char 10)
DEBUG(`instance_name CURSORHOME)                        ' Start of line (char 11)
DEBUG(`instance_name CLS)                                ' Clear screen (char 12)
DEBUG(`instance_name CR)                                 ' Carriage return (char 13)
DEBUG(`instance_name GOTOX `(x))                        ' Set X position (14,x)
DEBUG(`instance_name GOTOY `(y))                        ' Set Y position (15,y)
```

' Color control
```spin2
DEBUG(`instance_name COLOR `(fg) `(bg))                 ' Set foreground/background
DEBUG(`instance_name FGCOLOR `(color))                  ' Foreground only
DEBUG(`instance_name BGCOLOR `(color))                  ' Background only
```

' Special characters
```spin2
DEBUG(`instance_name `(0))                              ' Clear screen
DEBUG(`instance_name `(1))                              ' Cursor home
DEBUG(`instance_name `(2) `(x) `(y))                    ' Position cursor
DEBUG(`instance_name `(8))                              ' Backspace
DEBUG(`instance_name `(9))                              ' Tab
DEBUG(`instance_name `(10))                             ' Line feed
DEBUG(`instance_name `(13))                             ' Carriage return
```

' PC input
```spin2
DEBUG(`instance_name PC_KEY `(key))                     ' Send PC keystroke
DEBUG(`instance_name PC_MOUSE `(x) `(y) `(buttons))    ' Send mouse state
```

```

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name | Any valid name |
| char | integer | ASCII character | 0 to 255 |
| @string | address | String address | Valid hub address |
| length | integer | String length | 1 to buffer size |
| x | integer | Column position | 0 to width-1 |
| y | integer | Row position | 0 to height-1 |
| fg, bg | integer | Foreground/background | 0-255 or RGB |
| color | integer | Color value | 0-255 or RGB |
| key | integer | Keyboard scan code | 0 to 255 |
| buttons | integer | Mouse buttons | Bit flags |

#### Update Commands Table

| Command | Purpose | Parameters | Effect |
|---------|---------|------------|--------|
| CLS | Clear screen | None | Clear display |
| HOME | Home cursor | None | Position 0,0 |
| GOTOXY | Position cursor | x, y | Move to x,y |
| GOTOX | Set X position | x | Move to column |
| GOTOY | Set Y position | y | Move to row |
| TAB | Tab character | None | Advance tab |
| CR | Carriage return | None | Start of line |
| LF | Line feed | None | Next line |
| COLOR | Set colors | fg, bg | Text colors |
| FGCOLOR | Foreground only | color | Text color |
| BGCOLOR | Background only | color | Back color |
| ZSTR | Zero-term string | @string | Output string |
| LSTR | Length string | @string, length | Output n chars |
| PC_KEY | PC keyboard | key | Send keystroke |
| PC_MOUSE | PC mouse | x, y, buttons | Send mouse |

#### ANSI Escape Codes
```spin2
DEBUG(`instance_name 27 '[' '3' '1' 'm')          ' Red text
DEBUG(`instance_name 27 '[' '2' 'J')              ' Clear screen
DEBUG(`instance_name 27 '[' '1' '0' ';' '5' 'H')  ' Goto row 10, col 5
```

#### Example
```spin2
' CREATION: Define terminal instance named "SerialConsole"
DEBUG(`TERM SerialConsole TITLE 'Serial Terminal' SIZE 80 30 COLOR WHITE BACKCOLOR BLACK)

' UPDATE: Output colored text to "SerialConsole" instance
DEBUG(`SerialConsole 27 '[31m' 'Error: ' 27 '[0m' 'File not found' 13 10)
                     ' Note: just instance name, no "TERM"
```

---

### 8. BITMAP Display - Graphics Display

#### Creation Command
```spin2
DEBUG(`BITMAP name [configuration])
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'Graphics' |
| POS | Window position | POS 100 100 |
| SIZE | Pixel dimensions | SIZE 320 240 |
| FORMAT | Pixel format | LUMA8 |
| ZOOM | Zoom factor | ZOOM 2 |
| PALETTE | Color palette | PALETTE @colors |
| TRANSPARENT | Transparent color | TRANSPARENT $FF00FF |

#### Pixel Formats
| Format | Description | Bits/Pixel |
|--------|-------------|------------|
| LUMA1 | 1-bit monochrome | 1 |
| LUMA2 | 2-bit grayscale | 2 |
| LUMA4 | 4-bit grayscale | 4 |
| LUMA8 | 8-bit grayscale | 8 |
| RGB1 | 1-bit per channel | 3 |
| RGB2 | 2-bit per channel | 6 |
| RGB4 | 4-bit per channel | 12 |
| RGB8 | 8-bit per channel | 24 |
| RGBI8 | 8-bit indexed color | 8 |
| RGB16 | 16-bit RGB (5-6-5) | 16 |
| RGB24 | 24-bit true color | 24 |

#### Update Commands - Common Patterns

**Flexible Composition Examples:**
```spin2
' Frame buffer updates
DEBUG(`instance_name `(@buffer))
DEBUG(`instance_name `(@buffer) RECT `(x) `(y) `(w) `(h))
DEBUG(`instance_name `(@buffer) OFFSET `(offset) LENGTH `(bytes))

' Drawing operations
DEBUG(`instance_name PIXEL `(x) `(y) `(color))
DEBUG(`instance_name LINE `(x1) `(y1) `(x2) `(y2) `(color))
DEBUG(`instance_name FILLBOX `(x) `(y) `(w) `(h) `(color) TEXT `(x) `(y) 'label' `(color))

' Display control
DEBUG(`instance_name CLEAR `(color))
DEBUG(`instance_name ZOOM `(factor) SCROLL `(dx) `(dy))
DEBUG(`instance_name FONT `(id) TEXTSIZE `(size) TEXT `(x) `(y) 'string' `(color))
```

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name | Any valid name |
| @buffer | address | Pixel data | Valid hub address |
| @sprite | address | Sprite data | Valid hub address |
| @string | address | Text string | Valid hub address |
| x, y | integer | Pixel coordinates | 0 to width/height |
| x1, y1, x2, y2 | integer | Line endpoints | 0 to width/height |
| sx, sy, dx, dy | integer | Source/dest coords | 0 to width/height |
| w, h | integer | Width, height | 1 to display size |
| r | integer | Circle radius | 1 to max radius |
| rx, ry | integer | Ellipse radii | 1 to max radius |
| color | integer | Pixel color | Format dependent |
| offset | integer | Buffer offset | 0 to buffer size |
| bytes | integer | Byte count | 1 to buffer size |
| size | integer | Text size | 1 to 8 |
| font_id | integer | Font selection | 0 to 15 |
| factor | integer | Zoom factor | 1 to 8 |

#### Update Commands Table

| Command | Purpose | Parameters | Effect |
|---------|---------|------------|--------|
| RECT | Define region | x, y, w, h | Partial update |
| OFFSET | Buffer offset | offset | Start position |
| LENGTH | Byte count | bytes | Data length |
| PIXEL | Draw pixel | x, y, color | Single pixel |
| LINE | Draw line | x1, y1, x2, y2, color | Line segment |
| BOX | Rectangle outline | x, y, w, h, color | Draw box |
| FILLBOX | Filled rectangle | x, y, w, h, color | Solid box |
| CIRCLE | Circle outline | x, y, r, color | Draw circle |
| FILLCIRCLE | Filled circle | x, y, r, color | Solid circle |
| ELLIPSE | Ellipse outline | x, y, rx, ry, color | Draw ellipse |
| TEXT | Draw text | x, y, 'string', color | Place text |
| TEXTSIZE | Set text size | size | Scale text |
| FONT | Select font | font_id | Change font |
| SPRITE | Draw sprite | x, y, @sprite, w, h | Bitmap image |
| TRANSPARENT | Transparency | color | Transparent color |
| COPY | Copy region | sx, sy, dx, dy, w, h | Region copy |
| CLEAR | Clear display | [color] | Erase all |
| INVERT | Invert pixels | None | Toggle pixels |
| SCROLL | Scroll display | dx, dy | Shift pixels |
| ZOOM | Set zoom | factor | Scale display |

#### Example
```spin2
' CREATION: Define bitmap instance named "VideoDisplay"
DEBUG(`BITMAP VideoDisplay TITLE 'Video' SIZE 320 240 RGBI8)

' UPDATE: Send frame buffer to "VideoDisplay" instance
REPEAT
  UpdateFrameBuffer(@buffer)
  DEBUG(`VideoDisplay `(@buffer))        ' Note: just instance name, no "BITMAP"
```

---

### 9. MIDI Display - Musical Keyboard Monitor

#### Creation Command
```spin2
DEBUG(`MIDI name [configuration])
```

#### Configuration Parameters
| Parameter | Description | Example |
|-----------|-------------|---------|
| TITLE | Window title | TITLE 'MIDI Monitor' |
| POS | Window position | POS 200 400 |
| SIZE | Octaves displayed | SIZE 3 |
| RANGE | Note range | RANGE 36 84 |
| CHANNEL | MIDI channel | CHANNEL 0 |
| COLOR | Key colors | COLOR WHITE BLACK |
| VELOCITY | Show velocity | VELOCITY ON |

#### MIDI Note Range
- 0-127 standard MIDI notes
- Middle C = 60
- SIZE sets how many octaves to display (1-10)
- RANGE sets starting and ending notes

#### Update Commands - Common Patterns

**Note Events:**
```spin2
DEBUG(`instance_name NOTE_ON `(channel) `(note) `(velocity))  ' Note on event
DEBUG(`instance_name NOTE_OFF `(channel) `(note) `(velocity)) ' Note off event
DEBUG(`instance_name $9C `(note) `(velocity))                 ' Note ON, channel C (hex)
DEBUG(`instance_name $8C `(note) `(velocity))                 ' Note OFF, channel C
```

**MIDI Messages (Status Byte Format):**
```spin2
' Note Messages (8n/9n where n=channel 0-F)
DEBUG(`MIDI name `($80 + channel) `(note) `(velocity))    ' Note OFF
DEBUG(`MIDI name `($90 + channel) `(note) `(velocity))    ' Note ON

' Pressure Messages (An/Dn)
DEBUG(`MIDI name `($A0 + channel) `(note) `(pressure))    ' Polyphonic aftertouch
DEBUG(`MIDI name `($D0 + channel) `(pressure))            ' Channel pressure

' Control Messages (Bn/Cn)
DEBUG(`MIDI name `($B0 + channel) `(controller) `(value)) ' Control change
DEBUG(`MIDI name `($C0 + channel) `(program))             ' Program change

' Pitch Bend (En)
DEBUG(`MIDI name `($E0 + channel) `(lsb) `(msb))         ' Pitch bend
```

**System Messages:**
```spin2
DEBUG(`MIDI name SYSEX `(@data) `(length))               ' System exclusive
DEBUG(`MIDI name `($F8))                                 ' Timing clock
DEBUG(`MIDI name `($FA))                                 ' Start
DEBUG(`MIDI name `($FB))                                 ' Continue
DEBUG(`MIDI name `($FC))                                 ' Stop
DEBUG(`MIDI name `($FF))                                 ' System reset
```

**Batch Updates:**
```spin2
DEBUG(`MIDI name CHORD `(root) `(type) `(velocity))      ' Chord preset
DEBUG(`MIDI name SCALE `(root) `(mode) `(velocity))      ' Scale run
DEBUG(`MIDI name `(@midi_buffer) EVENTS `(count))        ' Buffer of MIDI events
```

**Display Control:**
```spin2
DEBUG(`MIDI name CLEAR)                                  ' Clear all notes
DEBUG(`MIDI name PANIC)                                  ' All notes off
DEBUG(`MIDI name CHANNEL `(n))                           ' Set display channel
DEBUG(`MIDI name TRANSPOSE `(semitones))                 ' Transpose display
```

**Parameter Specifications:**
- `name` - Instance name of the display
- `channel` - MIDI channel (0-15)
- `note` - MIDI note number (0-127, 60=middle C)
- `velocity` - Note velocity (0-127)
- `pressure` - Aftertouch pressure (0-127)
- `controller` - Controller number (0-127)
- `value` - Controller value (0-127)
- `program` - Program number (0-127)
- `lsb, msb` - Pitch bend values (0-127)
- `@data` - Hub address of sysex data
- `@midi_buffer` - Hub address of MIDI event array
- `length/count` - Number of bytes/events
- `root` - Root note for chord/scale
- `type/mode` - Chord type or scale mode
- `semitones` - Transposition amount

#### Update Parameters Table

| Parameter | Type | Description | Valid Values |
|-----------|------|-------------|-------------|
| instance_name | identifier | User-defined name | Any valid name |
| channel | integer | MIDI channel | 0 to 15 |
| note | integer | MIDI note number | 0 to 127 (60=middle C) |
| velocity | integer | Note velocity | 0 to 127 |
| pressure | integer | Aftertouch pressure | 0 to 127 |
| controller | integer | Controller number | 0 to 127 |
| value | integer | Controller value | 0 to 127 |
| program | integer | Program number | 0 to 127 |
| lsb, msb | integer | Pitch bend values | 0 to 127 |
| @data | address | Sysex data address | Valid hub address |
| @midi_buffer | address | MIDI event array | Valid hub address |
| length/count | integer | Number of bytes/events | 1 to buffer size |
| root | integer | Root note for chord/scale | 0 to 127 |
| type | integer | Chord type | Chord type constant |
| mode | integer | Scale mode | Scale mode constant |
| semitones | integer | Transposition amount | -127 to +127 |
| n | integer | Display channel number | 0 to 15 |

#### Update Commands Table

| Command | Purpose | Parameters | Effect |
|---------|---------|------------|--------|
| NOTE_ON | Note on event | channel, note, velocity | Press key |
| NOTE_OFF | Note off event | channel, note, velocity | Release key |
| CHORD | Chord preset | root, type, velocity | Play chord |
| SCALE | Scale run | root, mode, velocity | Play scale |
| EVENTS | Buffer playback | @buffer, count | Multiple events |
| SYSEX | System exclusive | @data, length | Send sysex |
| CLEAR | Clear all notes | None | All notes off |
| PANIC | MIDI panic | None | Force all off |
| CHANNEL | Set channel | n | Display channel |
| TRANSPOSE | Transpose notes | semitones | Shift pitch |

#### Example
```spin2
' Create 5-octave keyboard display
DEBUG(`MIDI Keyboard TITLE 'MIDI Input' SIZE 5 RANGE 36 96 VELOCITY ON)

' Play middle C
DEBUG(`MIDI Keyboard $90 `(60) `(100))        ' Note ON
WAITMS(500)
DEBUG(`MIDI Keyboard $80 `(60) `(0))          ' Note OFF

' Play chord
DEBUG(`MIDI Keyboard $90 `(60) `(100))        ' C
DEBUG(`MIDI Keyboard $90 `(64) `(100))        ' E
DEBUG(`MIDI Keyboard $90 `(67) `(100))        ' G
```

---

## Common Display Operations

### Display Control Commands

These commands work with most display types:

```spin2
DEBUG(`DisplayType name CLEAR)                 ' Clear display
DEBUG(`DisplayType name FREEZE)                ' Pause updates
DEBUG(`DisplayType name UNFREEZE)              ' Resume updates
DEBUG(`DisplayType name SAVE 'filename')       ' Save to file
DEBUG(`DisplayType name PRINT)                 ' Print display
```

### PC Input Integration

Read keyboard and mouse input from the PC host:

```spin2
' Get keyboard input
key := PC_KEY()

' Get mouse position and buttons
x, y, buttons := PC_MOUSE()

' Send keyboard input to terminal
DEBUG(`TERM Console PC_KEY `(key))
```

### Multi-Display Coordination

Multiple displays can receive the same data:

```spin2
' Create scope and FFT displays
DEBUG(`SCOPE Wave TITLE 'Time Domain' SAMPLES 256 'Signal' 0 255 100 10 %1111)
DEBUG(`FFT Spectrum TITLE 'Frequency Domain' SAMPLES 256 'Signal')

' Feed same data to both
REPEAT
  sample := GETADC(pin)
  DEBUG(`SCOPE Wave `(sample))
  DEBUG(`FFT Spectrum `(sample))
```

---

## Display Update Patterns

### Pattern 1: Single Value Updates
```spin2
' Most efficient for real-time data
REPEAT
  value := GetSensor()
  DEBUG(`SCOPE Monitor `(value))
  WAITMS(1)
```

### Pattern 2: Multi-Channel Updates
```spin2
' Update all channels together
REPEAT
  ch1 := GetChannel(0)
  ch2 := GetChannel(1)
  ch3 := GetChannel(2)
  DEBUG(`SCOPE Multi `(ch1) `(ch2) `(ch3))
```

### Pattern 3: Buffer Updates
```spin2
' Efficient for batch data
REPEAT
  CollectSamples(@buffer, 256)
  DEBUG(`SCOPE Batch `(@buffer) SAMPLES 256)
```

### Pattern 4: Conditional Updates
```spin2
' Update only when data changes
last_value := -1
REPEAT
  value := GetSensor()
  IF value <> last_value
    DEBUG(`SCOPE Monitor `(value))
    last_value := value
```

### Pattern 5: Triggered Updates
```spin2
' Update on specific conditions
REPEAT
  value := GetSensor()
  IF value > threshold
    DEBUG(`SCOPE Trigger `(value))
```

---

## Performance Considerations

1. **Update Rate**: DEBUG displays can handle ~10,000 updates/second at 2 Mbaud
2. **Buffer Size**: Larger SAMPLES values use more memory but provide smoother displays
3. **Multiple Displays**: Each display window uses system resources - limit to necessary displays
4. **Data Format**: Packed formats (BYTES_2BIT, etc.) are more efficient for logic analyzer data
5. **USB Latency**: Set USB Serial Port Latency Timer to 1ms in Windows Device Manager

---

## Color Reference

### Named Colors
- BLACK, WHITE
- RED, GREEN, BLUE
- CYAN, MAGENTA, YELLOW
- ORANGE, GRAY

### Brightness Modifiers
Add 0-15 after color name:
- `RED0` - Darkest red
- `RED8` - Medium red (default)
- `RED15` - Brightest red

### RGB Values
24-bit RGB: `$RRGGBB`
- `$FF0000` - Pure red
- `$00FF00` - Pure green
- `$0000FF` - Pure blue
- `$FFFFFF` - White
- `$808080` - Gray

---

## Display Creation Best Practices

1. **Name displays meaningfully**: Use descriptive instance names
2. **Set appropriate SAMPLES**: Balance between detail and performance
3. **Configure before first update**: All parameters in creation command
4. **Use consistent color schemes**: Helps identify related data
5. **Position windows logically**: Group related displays together
6. **Add titles**: Makes multi-window debugging clearer
7. **Set ranges appropriately**: Prevents auto-scaling jumps
8. **Use backtick syntax**: Cleaner output without "CogN" prefix

---

## Debugging Workflow Integration

### Complete Debugging System
```spin2
CON
  DEBUG_BAUD = 2_000_000
  DEBUG_DELAY = 100          ' 100ms startup delay

PUB main() | value
  ' Create multiple coordinated displays
  DEBUG(`TERM Console TITLE 'Status' SIZE 80 10)
  DEBUG(`SCOPE Signals TITLE 'Waveforms' SAMPLES 256 'ADC' 0 4095 100 10 %1111)
  DEBUG(`FFT Spectrum TITLE 'Frequency' SAMPLES 512 LOGSCALE 'Input')
  DEBUG(`LOGIC Digital TITLE 'Digital I/O' SAMPLES 128 'P0..P7' 8)
  
  ' Main monitoring loop
  REPEAT
    ' Read analog
    value := GETADC(adc_pin)
    
    ' Update displays
    DEBUG(`SCOPE Signals `(value))
    DEBUG(`FFT Spectrum `(value))
    DEBUG(`LOGIC Digital `(INA[7..0]))
    
    ' Status message
    IF value > 3000
      DEBUG(`TERM Console 'WARNING: High value detected!' 13 10)
    
    WAITMS(1)
```

This completes the comprehensive catalog of P2 DEBUG display commands!