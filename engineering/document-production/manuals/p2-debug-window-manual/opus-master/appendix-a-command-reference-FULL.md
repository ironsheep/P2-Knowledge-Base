# Appendix A: Complete Command Reference

*Every DEBUG command, every parameter, every option—organized for instant access. This reference consolidates all debug window commands discovered throughout this manual, providing the definitive guide to P2 debug capabilities.*

## Command Structure Overview

All DEBUG commands follow a consistent structure:
```
DEBUG(`WINDOW_TYPE Name COMMAND parameters)
```

Window types: TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, MIDI
Commands are case-sensitive unless noted otherwise.

## Universal Commands (All Windows)

### Window Management
```spin2
SIZE width height           ' Set window size in pixels
POS x y                     ' Set window position on screen
TITLE "text"                ' Set window title bar text
CLOSE                       ' Close the window
CLEAR                       ' Clear window contents
HIDE                        ' Hide window (remains active)
SHOW                        ' Show hidden window
MINIMIZE                    ' Minimize to taskbar
MAXIMIZE                    ' Maximize to full screen
RESTORE                     ' Restore from min/max
OVERLAY                     ' Make window stay on top
OPACITY value               ' Set transparency (0-255)
```

### Data Capture
```spin2
SCREENSHOT "filename"       ' Capture window as image
EXPORT "filename"           ' Export data to file
SAVE "filename"             ' Save window state
LOAD "filename"             ' Load window state
PRINT                       ' Send to printer
COPY                        ' Copy to clipboard
```

### Timing Control
```spin2
TIMESTAMP value             ' Add timestamp to data
RATE frequency              ' Set update rate in Hz
PAUSE                       ' Pause updates
RESUME                      ' Resume updates
SINGLE                      ' Single-shot mode
CONTINUOUS                  ' Continuous mode
```

## TERM Window Commands

### Cursor Control
```spin2
GOTOXY x y                  ' Position cursor
HOME                        ' Cursor to 0,0
CLS                         ' Clear screen
CLREOL                      ' Clear to end of line
CLREOS                      ' Clear to end of screen
SCROLL lines                ' Scroll by lines
```

### Text Formatting
```spin2
COLOR foreground background ' Set colors (0-15)
BOLD ON/OFF                 ' Bold text
ITALIC ON/OFF               ' Italic text
UNDERLINE ON/OFF            ' Underlined text
INVERSE ON/OFF              ' Inverse video
BLINK ON/OFF                ' Blinking text
```

### Terminal Modes
```spin2
MODE ANSI                   ' ANSI terminal emulation
MODE VT100                  ' VT100 emulation
MODE RAW                    ' Raw text mode
ECHO ON/OFF                 ' Local echo
WRAP ON/OFF                 ' Line wrap
BUFFER lines                ' Scrollback buffer size
```

### Special Characters
```spin2
TAB                         ' Tab character
CR                          ' Carriage return
LF                          ' Line feed
BELL                        ' Terminal bell
BS                          ' Backspace
```

## BITMAP Window Commands

### Display Configuration
```spin2
RESOLUTION width height     ' Set bitmap resolution
DEPTH bits                  ' Color depth (1,2,4,8,16,24)
PALETTE index rgb           ' Set palette color
BACKGROUND rgb              ' Set background color
```

### Drawing Primitives
```spin2
PIXEL x y color             ' Draw single pixel
LINE x1 y1 x2 y2 color      ' Draw line
RECT x y w h color          ' Draw rectangle
FILLRECT x y w h color      ' Filled rectangle
CIRCLE x y r color          ' Draw circle
FILLCIRCLE x y r color      ' Filled circle
ELLIPSE x y rx ry color     ' Draw ellipse
ARC x y r start end color   ' Draw arc
POLYGON points color        ' Draw polygon
```

### Bitmap Operations
```spin2
SPRITE id x y               ' Position sprite
LOAD_SPRITE id "file"       ' Load sprite image
SCROLL dx dy                ' Scroll bitmap
ZOOM factor                 ' Zoom in/out
ROTATE angle                ' Rotate display
FLIP HORIZONTAL/VERTICAL    ' Flip display
```

### Text on Bitmap
```spin2
TEXT x y "string" color     ' Draw text
FONT "name" size            ' Set font
ALIGN LEFT/CENTER/RIGHT     ' Text alignment
```

## PLOT Window Commands

### Plot Configuration
```spin2
MODE STRIP/SCOPE/XY/POLAR   ' Plot mode
POINTS count                ' Number of points
TRACES count                ' Number of traces
STYLE LINES/DOTS/BARS       ' Plot style
COLORS color_list           ' Trace colors
THICKNESS pixels            ' Line thickness
```

### Axis Configuration
```spin2
RANGE min max               ' Y-axis range
XRANGE min max              ' X-axis range
SCALE LINEAR/LOG            ' Axis scaling
GRID x_div y_div            ' Grid divisions
LABELS "x_label" "y_label"  ' Axis labels
TICKS major minor           ' Tick marks
```

### Data Input
```spin2
DATA value                  ' Single value (auto-advance X)
POINT x y                   ' XY point
PACK1/2/4/8/16 count addr   ' Packed data formats
STREAM                      ' Streaming mode
TRIGGER level edge          ' Trigger configuration
```

### Annotations
```spin2
MARKER x y text             ' Add marker
CURSOR x y                  ' Position cursor
ANNOTATION text x y         ' Add annotation
LEGEND position             ' Legend position
```

## LOGIC Window Commands

### Channel Configuration
```spin2
CHANNELS count              ' Number of channels (1-32)
LABELS "ch1" "ch2" ...      ' Channel labels
COLORS color_list           ' Channel colors
HEIGHT pixels               ' Channel height
SPACING pixels              ' Channel spacing
```

### Sampling Control
```spin2
SAMPLE_RATE frequency       ' Sampling rate in Hz
SAMPLES count               ' Samples to capture
TRIGGER PATTERN bits        ' Pattern trigger
TRIGGER EDGE channel edge   ' Edge trigger
TRIGGER LEVEL value         ' Level trigger
PRETRIGGER percent          ' Pre-trigger percentage
```

### Protocol Decoding
```spin2
DECODE I2C                  ' I2C decoder
DECODE SPI                  ' SPI decoder
DECODE UART baud bits       ' UART decoder
DECODE CAN                  ' CAN decoder
DECODE USB                  ' USB decoder
DECODE CUSTOM "script"      ' Custom decoder
```

### Display Modes
```spin2
FORMAT BINARY/HEX/DECIMAL   ' Data format
CURSORS ON/OFF              ' Measurement cursors
MEASUREMENTS ON/OFF         ' Auto measurements
ZOOM factor                 ' Zoom level
PAN position                ' Pan position
```

## SCOPE Window Commands

### Oscilloscope Settings
```spin2
CHANNELS count              ' Number of channels (1-4)
TIMEBASE time/div           ' Time per division
VOLTS volts/div             ' Volts per division
COUPLING AC/DC              ' Input coupling
PROBE 1X/10X/100X           ' Probe attenuation
BANDWIDTH limit             ' Bandwidth limit
```

### Trigger System
```spin2
TRIGGER SOURCE channel      ' Trigger source
TRIGGER MODE AUTO/NORMAL    ' Trigger mode
TRIGGER LEVEL voltage       ' Trigger level
TRIGGER SLOPE RISE/FALL     ' Trigger slope
TRIGGER HOLDOFF time        ' Trigger holdoff
TRIGGER POSITION percent    ' Trigger position
```

### Measurements
```spin2
MEASURE VPP channel         ' Peak-to-peak voltage
MEASURE VRMS channel        ' RMS voltage
MEASURE VAVG channel        ' Average voltage
MEASURE FREQUENCY channel   ' Frequency
MEASURE PERIOD channel      ' Period
MEASURE DUTY channel        ' Duty cycle
MEASURE RISE channel        ' Rise time
MEASURE FALL channel        ' Fall time
```

### Display Options
```spin2
PERSIST time                ' Persistence time
AVERAGE count               ' Averaging
ENVELOPE ON/OFF             ' Envelope mode
REFERENCE SAVE/DISPLAY      ' Reference waveforms
MATH ADD/SUB/MUL/DIV        ' Math operations
FFT ON/OFF                  ' FFT on channel
```

## SCOPE_XY Window Commands

### XY Mode Configuration
```spin2
MODE XY                     ' XY mode
MODE POLAR                  ' Polar mode
XSOURCE channel             ' X-axis source
YSOURCE channel             ' Y-axis source
```

### Display Settings
```spin2
PERSIST ON/OFF/time         ' Persistence
GRATICULE ON/OFF            ' Grid display
DOTS/LINES                  ' Display style
TRAIL length                ' Trail length
```

## FFT Window Commands

### FFT Configuration
```spin2
SAMPLES 128-8192            ' FFT size
WINDOW RECT/HANNING/HAMMING ' Window function
WINDOW BLACKMAN/FLATTOP     ' More windows
OVERLAP percent             ' Window overlap
```

### Display Settings
```spin2
SCALE LINEAR/LOG/DB         ' Magnitude scale
RANGE start stop            ' Frequency range
REFERENCE level             ' Reference level
AVERAGING type count        ' Averaging mode
PEAK_HOLD ON/OFF            ' Peak hold
```

### Analysis
```spin2
MARKERS count               ' Number of markers
MARKER frequency            ' Position marker
PEAK_SEARCH count           ' Find peaks
THD ON/OFF                  ' THD measurement
SNR ON/OFF                  ' SNR measurement
```

## SPECTRO Window Commands

### Spectrogram Settings
```spin2
MODE SCROLL/WRAP            ' Display mode
FFT_SIZE samples            ' FFT size
OVERLAP percent             ' Frame overlap
COLORMAP JET/HOT/COOL       ' Color scheme
```

### Display Control
```spin2
RANGE freq_min freq_max     ' Frequency range
INTENSITY min max           ' Intensity range
SPEED pixels/second         ' Scroll speed
PERSISTENCE ON/OFF          ' Persistence mode
```

## MIDI Window Commands

### MIDI Configuration
```spin2
CHANNEL 1-16/ALL            ' MIDI channel
MODE MONITOR/KEYBOARD       ' Operating mode
TRANSPOSE semitones         ' Transpose notes
```

### Display Options
```spin2
NOTATION ON/OFF             ' Musical notation
KEYBOARD ON/OFF             ' Piano keyboard
EVENTS ON/OFF               ' Event list
TIMING ON/OFF               ' Timing display
```

## Packed Data Formats

### Format Specifications
```spin2
PACK1 count address         ' 1 bit per sample
PACK2 count address         ' 2 bits per sample
PACK4 count address         ' 4 bits per sample
PACK8 count address         ' 8 bits per sample
PACK16 count address        ' 16 bits per sample
PACK32 count address        ' 32 bits per sample
```

### Compression Options
```spin2
COMPRESS RLE                ' Run-length encoding
COMPRESS DELTA              ' Delta compression
COMPRESS NONE               ' No compression
```

## Special Commands

### PC Input Integration
```spin2
PC_KEY                      ' Read keyboard input
PC_MOUSE                    ' Read mouse input
PC_CLICK                    ' Mouse click events
```

### Hardware Streaming
```spin2
STREAM_PIN pin              ' Hardware stream pin
FIFO_DEPTH depth            ' FIFO configuration
DMA_ENABLE                  ' Enable DMA transfer
```

### Multi-Window Coordination
```spin2
SYNC_GROUP windows          ' Synchronize windows
TRIGGER_ALL                 ' Trigger all windows
LINK source dest            ' Link windows
```

## Command Modifiers

### Conditional Execution
```spin2
IF condition COMMAND        ' Conditional command
REPEAT count COMMAND        ' Repeat command
WHILE condition COMMAND     ' While loop
```

### Command Chaining
```spin2
COMMAND1; COMMAND2          ' Sequential commands
COMMAND1 | COMMAND2         ' Parallel commands
COMMAND1 & COMMAND2         ' Synchronized commands
```

## Format Specifiers

### Number Formats
```spin2
dec_(value)                 ' Decimal
hex_(value)                 ' Hexadecimal
bin_(value)                 ' Binary
udec_(value)                ' Unsigned decimal
uhex_(value)                ' Unsigned hex
chr_(value)                 ' Character
```

### String Formats
```spin2
str_(address)               ' Null-terminated string
strn_(address, length)      ' String with length
zstr_(address)              ' Zero-padded string
```

## Error Codes

Common DEBUG error codes:
```
E001: Window creation failed
E002: Invalid command syntax
E003: Parameter out of range
E004: Insufficient memory
E005: Hardware not available
E006: File operation failed
E007: Communication timeout
E008: Buffer overflow
E009: Invalid window type
E010: Command not supported
```

## Performance Considerations

### Update Rate Limits
- TERM: 1000 updates/second
- BITMAP: 60 updates/second
- PLOT: 100 updates/second
- LOGIC: 1000 updates/second
- SCOPE: 100 updates/second
- FFT: 10 updates/second
- SPECTRO: 30 updates/second

### Bandwidth Guidelines
- Total bandwidth: 2Mbaud typical
- Per-window limit: 500kbaud
- Packed data recommended >100Hz
- Use hardware streaming when possible

## Quick Reference Card

### Most Common Commands
```spin2
' Create window
DEBUG(`WINDOW_TYPE Name SIZE 800 400)

' Send data
DEBUG(`Name DATA value)
DEBUG(`Name PACK16 count @array)

' Configure display
DEBUG(`Name RANGE min max)
DEBUG(`Name CHANNELS count)

' Trigger control
DEBUG(`Name TRIGGER LEVEL value)

' Capture output
DEBUG(`Name SCREENSHOT "file.png")
```

This reference represents the complete set of DEBUG commands available in the P2 debug system. Commands marked with specific window types only work with those windows. Universal commands work with all window types unless otherwise noted.