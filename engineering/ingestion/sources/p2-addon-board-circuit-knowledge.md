# P2 Add-on Board Circuit and Signal Knowledge

## Overview
This document details the circuit design and signal characteristics of each P2 Eval Board add-on module. Understanding these circuits enables proper code generation with correct signal polarity, drive strength, and Smart Pin configurations.

## Circuit Descriptions by Board

### #64006A - LED Array Board

**Circuit Configuration**:
```
P2 Pin → 330Ω Resistor → LED Anode → LED Cathode → Ground
```

**Signal Characteristics**:
- **Drive Type**: Active HIGH (pin HIGH = LED ON)
- **Current Limiting**: 330Ω series resistor
- **Current Draw**: ~10mA per LED @ 3.3V
- **Voltage Drop**: ~2.0V (red LED) + 1.3V (resistor) = 3.3V total
- **Max Current**: 10mA typical, 20mA absolute max
- **Power Source**: From P2 pin directly

**Code Implications**:
```spin2
' LED ON: Drive pin HIGH
PINHIGH(led_pin)

' LED OFF: Drive pin LOW  
PINLOW(led_pin)

' PWM Brightness: Configure Smart Pin
PINSTART(led_pin, P_PWM_TRIANGLE | P_OE, 255, 128)  ' 50% brightness
```

### #64006B - Switch Array Board

**Circuit Configuration**:
```
3.3V → 10kΩ Pull-up → P2 Pin → Switch → Ground
                            ↓
                    Debounce Capacitor
```

**Signal Characteristics**:
- **Logic**: Active LOW (pressed = LOW, released = HIGH)
- **Pull-up Resistor**: 10kΩ to 3.3V
- **Debounce Capacitor**: External capacitor provided
- **Current when Pressed**: 3.3V / 10kΩ = 0.33mA
- **Input Voltage**: 3.3V (HIGH) when open, 0V (LOW) when pressed
- **Switch Type**: Momentary, normally open

**Code Implications**:
```spin2
' Read switch state (inverted logic)
IF NOT PINREAD(switch_pin)  ' Switch pressed
  ' Handle press
  
' Configure Smart Pin for edge detection with debouncing
PINSTART(switch_pin, P_MINUS_A | P_MINUS_B, 20_000, 0)  ' 20ms debounce
```

### #64006C - Potentiometer Board  

**Circuit Configuration**:
```
3.3V → Pot Top Terminal
        ↓
     Wiper → P2 Pin (ADC input)
        ↓
GND → Pot Bottom Terminal
```

**Signal Characteristics**:
- **Resistance**: 10kΩ linear taper
- **Output Voltage Range**: 0V to 3.3V
- **Wiper Current**: Minimal (high impedance ADC input)
- **Linearity**: Linear response across rotation
- **Power Dissipation**: (3.3V)² / 10kΩ = 1.1mW
- **ADC Resolution**: 8-bit internal (0-255 counts)

**Code Implications**:
```spin2
' Configure ADC Smart Pin
PINSTART(pot_pin, P_ADC_1X | P_ADC, 0, 0)

' Read 8-bit value (0-255)
pot_value := PINREAD(pot_pin) >> 24

' Scale to percentage (0-100)
percentage := pot_value * 100 / 255
```

### #64006D - Servo Header Board

**Circuit Configuration**:
```
Each 3-pin Servo Connector:
Pin 1: P2 Signal Pin → Servo Control Wire (White/Yellow)
Pin 2: 5V Power → Servo Power Wire (Red)
Pin 3: Ground → Servo Ground Wire (Black/Brown)
```

**Signal Characteristics**:
- **Signal Level**: 3.3V from P2 (most servos accept this)
- **PWM Frequency**: 50Hz (20ms period)
- **Pulse Width Range**: 1.0ms to 2.0ms (1.5ms = center)
- **Power Supply**: 5V direct from header (not from P2)
- **Current per Servo**: Up to 500mA peak
- **Signal Current**: <1mA (high impedance input)

**Code Implications**:
```spin2
' Configure Smart Pin for servo PWM (50Hz, 1.5ms pulse)
CLK_FREQ := 200_000_000  ' 200MHz system clock
PERIOD := CLK_FREQ / 50  ' 20ms period
PULSE := CLK_FREQ / 1000 * 1.5  ' 1.5ms pulse

PINSTART(servo_pin, P_PWM_TRIANGLE | P_OE, PERIOD, PULSE)

' Set servo position (1000-2000 microseconds)
WYPIN(servo_pin, CLK_FREQ / 1000 * microseconds)
```

### #64006E - Sensor Board

**Temperature Sensor Circuit**:
```
Temp Sensor IC → Analog Out (10mV/°C) → P2 Pin
```

**Light Sensor Circuit**:
```
3.3V → Photoresistor → P2 Pin → 10kΩ → Ground
                (Voltage Divider)
```

**Sound Sensor Circuit**:
```
Microphone → Op-Amp → AC Coupling Cap → P2 Pin
              ↑
          Bias Circuit
```

**Signal Characteristics**:

**Temperature**:
- Output: 10mV per °C
- Range: 0°C to 100°C = 0V to 1.0V
- Response Time: <1 second
- Supply: 3.3V

**Light**:
- Dark Resistance: ~1MΩ
- Bright Resistance: ~1kΩ  
- Voltage Range: ~0.03V (dark) to ~3.0V (bright)
- Response Time: <100ms

**Sound**:
- Frequency Response: 20Hz - 20kHz
- Output: AC coupled, 1.65V bias
- Amplitude: ±1.65V around bias
- Response Time: <1ms

**Code Implications**:
```spin2
' Temperature reading
PINSTART(temp_pin, P_ADC_1X | P_ADC, 0, 0)
temp_raw := PINREAD(temp_pin) >> 24
temp_celsius := temp_raw * 330 / 255  ' Scale to 0-100°C range

' Light reading  
PINSTART(light_pin, P_ADC_1X | P_ADC, 0, 0)
light_level := PINREAD(light_pin) >> 24  ' 0=dark, 255=bright

' Sound reading (needs continuous sampling)
PINSTART(sound_pin, P_ADC_1X | P_ADC, 0, 0)
REPEAT
  sound_sample := PINREAD(sound_pin) >> 24
  ' Process audio sample
```

### #64006F - Prototyping Board

**Circuit Configuration**:
- Breadboard with power rails connected to header
- All signal pins brought to breadboard tie points
- No built-in components

**Available Signals**:
- 8 I/O pins from header (pins 1-8)
- 3.3V power (pin 9)
- Ground (pins 10, 12)
- 5V power if available (pin 11)

### #64006G - Digital I/O Board

**LED Circuit** (pins 1-4):
```
P2 Pin → 330Ω → LED → Ground
```

**Switch Circuit** (same pins 1-4):
```
3.3V → 10kΩ → P2 Pin → Switch → Ground
```

**Signal Characteristics**:
- **Bi-directional**: Can read switch while LED is on
- **LED Drive**: Active HIGH
- **Switch Read**: Active LOW  
- **Isolation**: LED and switch circuits independent
- **Current**: LED ~10mA, switch ~0.33mA when pressed

**Code Implications**:
```spin2
' Set LED while reading switch
PINWRITE(pin, led_state)  ' Set LED
PINFLOAT(pin)            ' Briefly float to read
switch := NOT PINREAD(pin)  ' Read switch (inverted)
PINWRITE(pin, led_state)  ' Restore LED state
```

### #64006H - Analog I/O Board

**Potentiometer Circuit** (pins 1-4):
```
3.3V → 10kΩ Linear Pot → Wiper → P2 Pin
                          ↓
                         Ground
```

**Analog Sensor Circuit** (pins 5-8):
```
Sensor Element → RC Filter → Buffer → P2 Pin
```

**Signal Characteristics**:

**Potentiometers**:
- Same as #64006C board
- 10kΩ linear, 0-3.3V output

**Analog Sensors**:
- Variable resistance/capacitance elements
- RC filtered for noise reduction
- Output range: 0-3.3V
- Calibration trimpots available

**Code Implications**:
```spin2
' Read all 8 analog inputs
REPEAT i FROM 0 TO 7
  PINSTART(base_pin + i, P_ADC_1X | P_ADC, 0, 0)
  analog[i] := PINREAD(base_pin + i) >> 24
```

## Power and Ground Distribution

### Power Requirements by Board Type

| Board | 3.3V Current | 5V Current | Ground Connections |
|-------|--------------|------------|-------------------|
| LED Array | 80mA max (8×10mA) | None | Pin 10, 12 |
| Switch Array | 3mA max | None | Pin 10, 12 |
| Potentiometer | 11mW total | None | Pin 10, 12 |
| Servo Header | Signal only | 4A max (8×500mA) | Pin 10, 12 |
| Sensor Board | 50mA typical | None | Pin 10, 12 |
| Digital I/O | 40mA (4 LEDs) | None | Pin 10, 12 |
| Analog I/O | 20mA typical | None | Pin 10, 12 |

### Critical Design Rules

1. **Current Limits**: 
   - P2 pin source/sink: 8mA standard, 20mA high drive
   - Total VIO group: 100mA (8 pins share VIO regulator)
   - 5V supply: Limited by main board capability

2. **Voltage Levels**:
   - All signals are 3.3V logic
   - 5V is power only, not for logic
   - No 5V tolerance on signal pins

3. **Signal Integrity**:
   - Keep analog and digital signals separated
   - Use appropriate Smart Pin modes
   - Consider ground return paths

## Smart Pin Configuration Summary

### By Function Type

**Digital Output (LEDs)**:
- Mode: `P_PWM_TRIANGLE | P_OE` for PWM brightness
- Mode: `P_HIGH | P_OE` for simple on/off

**Digital Input (Switches)**:
- Mode: `P_MINUS_A | P_MINUS_B` for debounced edge detection
- Pull-ups already on board (10kΩ)

**Analog Input (Pots/Sensors)**:
- Mode: `P_ADC_1X | P_ADC` for single-ended ADC
- 8-bit resolution standard

**PWM Output (Servos)**:
- Mode: `P_PWM_TRIANGLE | P_OE`
- 50Hz frequency, 1-2ms pulses

## Code Generation Patterns

### Universal Initialization
```spin2
PUB init_addon_board(board_type, base_pin) | i
  CASE board_type
    LED_BOARD:
      REPEAT i FROM 0 TO 7
        PINLOW(base_pin + i)  ' Start with LEDs off
    
    SWITCH_BOARD:
      REPEAT i FROM 0 TO 7
        PINFLOAT(base_pin + i)  ' High-Z for input
    
    POT_BOARD:
      REPEAT i FROM 0 TO 7
        PINSTART(base_pin + i, P_ADC_1X | P_ADC, 0, 0)
    
    SERVO_BOARD:
      REPEAT i FROM 0 TO 7
        init_servo(base_pin + i)
```

### Reading Pattern
```spin2
PUB read_addon_board(board_type, base_pin, @buffer) | i
  CASE board_type
    SWITCH_BOARD:
      REPEAT i FROM 0 TO 7
        buffer[i] := NOT PINREAD(base_pin + i)  ' Invert for active-low
    
    POT_BOARD, ANALOG_BOARD:
      REPEAT i FROM 0 TO 7
        buffer[i] := PINREAD(base_pin + i) >> 24  ' Get 8-bit value
```

### Writing Pattern
```spin2
PUB write_addon_board(board_type, base_pin, @buffer) | i
  CASE board_type
    LED_BOARD:
      REPEAT i FROM 0 TO 7
        PINWRITE(base_pin + i, buffer[i])
    
    SERVO_BOARD:
      REPEAT i FROM 0 TO 7
        set_servo_position(base_pin + i, buffer[i])
```

## 9. 64032 P2 Eval HUB75 Adapter Board (Iron Sheep Productions)

### Overview
- **Purpose**: Drive HUB75 RGB LED matrix panels from P2
- **Manufacturer**: Iron Sheep Productions, LLC (Stephen Moraco)
- **Connectivity**: Dual 2×6 pass-through headers + HUB75 IDC connector
- **Level Shifting**: 3.3V to 5V via dual 74HCT244 ICs
- **Status**: Retiring from Parallax store (limited stock)

### Signal Configuration
```
HUB75 Signal Mapping (Base Pin + Offset):
Control Signals:
- CLK:     io+0  (Pixel clock)
- OE#:     io+1  (Output Enable, active low)
- LAT:     io+2  (Latch Enable)

Address Lines:
- A:       io+3  (Row select bit 0)
- B:       io+4  (Row select bit 1)
- C:       io+5  (Row select bit 2)
- D:       io+6  (Row select bit 3, for 32+ rows)
- E:       io+7  (Row select bit 4, for 64+ rows)

Color Data:
- R1:      io+8  (Red, upper half)
- G1:      io+9  (Green, upper half)
- B1:      io+10 (Blue, upper half)
- R2:      io+11 (Red, lower half)
- G2:      io+12 (Green, lower half)
- B2:      io+13 (Blue, lower half)
```

### Circuit Details
- **Level Shifters**: 2× 74HCT244 octal buffers
  - Input: TTL compatible (2.0V VIH accepts 3.3V logic)
  - Output: 5V CMOS (4.4V VOH minimum)
  - Drive: ±6mA per output
  - Propagation delay: 13-18ns
  - Maximum frequency: 35-40MHz reliable

### Power Requirements
- **Adapter Board**: 
  - Quiescent: 20µA typical
  - Operating @ 25MHz: 25mA
  - Operating @ 35MHz: 35mA
  - Maximum: 50mA @ 40MHz
  
- **LED Panel Power** (External 5V PSU Required):
  - 32×32: 2-3A typical, 8A peak
  - 64×32: 3-4A typical, 12A peak
  - 64×64: 4-6A typical, 20A peak

### Smart Pin Configuration
```spin2
CON
  ' Default base pin group (configurable)
  HUB75_BASE = 16  ' P16-P31
  ' Alternative: 0 (P0-P15), 32 (P32-P47), 48 (P48-P63)
  
PUB init_hub75() | base
  base := HUB75_BASE
  
  ' Set all 14 pins as outputs
  DIRH(base ADDPINS 13)
  
  ' Initialize control signals
  OUTL(base + 0)   ' CLK low
  OUTH(base + 1)   ' OE# high (disabled)
  OUTL(base + 2)   ' LAT low
  
  ' Optional: PWM brightness control on OE#
  WRPIN(base + 1, P_PWM_SAWTOOTH)
  WXPIN(base + 1, brightness << 16 | $FF)
  
  ' Optional: NCO clock generation
  WRPIN(base + 0, P_NCO_FREQ)
  WXPIN(base + 0, clock_freq)
  
  ' Optional: Streamer for fast parallel output
  ' Color data pins are consecutive for streamer use
```

### Code Generation Pattern
```spin2
OBJ
  display : "isp_hub75_matrix"  ' From P2 OBEX
  
PUB example_hub75_display() | base
  base := HUB75_BASE
  
  ' Initialize display driver (64x32 panel)
  display.start(base, 64, 32)
  display.setBrightness(128)  ' 0-255
  
  ' Draw content
  display.clear($0000)  ' Black background
  display.drawText(0, 0, string("Hello P2!"), $F800)  ' Red text
  display.drawLine(0, 16, 63, 16, $07E0)  ' Green line
  display.update()  ' Send to panel
  
PUB manual_panel_control() | base, row, col
  base := HUB75_BASE
  
  ' Drive panel manually (1:16 scan for 32-row panel)
  REPEAT row FROM 0 TO 15
    ' Set row address
    OUTH[base+3..base+6] := row
    
    ' Clock out one row of pixels
    REPEAT col FROM 0 TO 63
      ' Set RGB data for upper and lower halves
      OUTH[base+8..base+10] := get_rgb1(row, col)
      OUTH[base+11..base+13] := get_rgb2(row+16, col)
      
      ' Clock pulse
      OUTH(base + 0)  ' CLK high
      OUTL(base + 0)  ' CLK low
      
    ' Latch the row data
    OUTL(base + 1)  ' OE# low (blank display)
    OUTH(base + 2)  ' LAT high
    OUTL(base + 2)  ' LAT low
    OUTH(base + 1)  ' OE# high (enable display)
    
    ' Optional: PWM dimming via OE# duty cycle
    WAITUS(100)  ' Adjust for brightness
```

### Supported Panel Configurations
| Panel Size | Pixels | Scan | Address Lines | Refresh @ P2 200MHz |
|------------|--------|------|---------------|---------------------|
| 16×32 | 512 | 1:8 | A,B,C | 480 Hz |
| 32×32 | 1024 | 1:16 | A,B,C,D | 240 Hz |
| 64×32 | 2048 | 1:16 | A,B,C,D | 120 Hz |
| 64×64 | 4096 | 1:32 | A,B,C,D,E | 60 Hz |
| 128×64 | 8192 | 1:32 | A,B,C,D,E | 30 Hz |

### Panel Types and Pixel Pitch
- **Pixel Pitch**: P1.25, P2, P3, P4, P5, P6, P7, P8, P10
- **Indoor**: P1.25-P4 (high resolution, lower brightness)
- **Outdoor**: P5-P10 (weather resistant, high brightness)
- **Standard**: HUB75 and HUB75E (E = 5 address lines)

### GitHub Resources
- **Driver**: https://github.com/ironsheep/P2-HUB75-LED-Matrix-Driver
- **Documentation**: Comprehensive API and examples
- **P2 OBEX**: ISP HUB75 Driver object available

---

**Document Status**: Complete circuit and signal knowledge for all P2 add-on boards
**Trust Level**: HIGH - Based on official specifications and datasheets
**Last Updated**: Added 64032 HUB75 Adapter Board specifications