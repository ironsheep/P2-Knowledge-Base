# P2 Board Pin Mapping Knowledge Base

## Executive Summary
This document provides the complete pin mapping chain from P2 add-on board devices through their header connections to the final P2 port assignments. When a developer specifies their board combination, this knowledge enables automatic code generation with correct pin assignments.

## Standard 2x6 Header Interface

### Physical Layout
All P2 Eval Board accessory modules use a standardized 2x6 (12-pin) header:

```
    Pin 1   Pin 2
    Pin 3   Pin 4
    Pin 5   Pin 6
    Pin 7   Pin 8
    Pin 9   Pin 10
    Pin 11  Pin 12
```

### Standard Pin Functions
- **Pins 1-8**: Data/Signal pins (connected to P2 I/O ports)
- **Pin 9**: 3.3V power supply
- **Pin 10**: Ground
- **Pin 11**: 5V power supply (when available)
- **Pin 12**: Ground

## Main Board Header Mappings

### P2 Eval Board Rev C (#64000)
**Total Headers**: 8 sets of 2x6 edge headers at board perimeter
**Pin Coverage**: Complete P0-P63 access

### Header A (Top Edge, Left)
- **P2 Port Range**: P0-P7
- **Pin Mapping**:
  - Header Pin 1 → P0
  - Header Pin 2 → P1
  - Header Pin 3 → P2
  - Header Pin 4 → P3
  - Header Pin 5 → P4
  - Header Pin 6 → P5
  - Header Pin 7 → P6
  - Header Pin 8 → P7
  - Header Pins 9-12 → Power/Ground

### Header B (Top Edge, Right)
- **P2 Port Range**: P8-P15
- **Pin Mapping**:
  - Header Pin 1 → P8
  - Header Pin 2 → P9
  - Header Pin 3 → P10
  - Header Pin 4 → P11
  - Header Pin 5 → P12
  - Header Pin 6 → P13
  - Header Pin 7 → P14
  - Header Pin 8 → P15
  - Header Pins 9-12 → Power/Ground

### Header C (Right Edge, Top)
- **P2 Port Range**: P16-P23
- **Pin Mapping**:
  - Header Pin 1 → P16
  - Header Pin 2 → P17
  - Header Pin 3 → P18
  - Header Pin 4 → P19
  - Header Pin 5 → P20
  - Header Pin 6 → P21
  - Header Pin 7 → P22
  - Header Pin 8 → P23
  - Header Pins 9-12 → Power/Ground

### Header D (Right Edge, Bottom)
- **P2 Port Range**: P24-P31
- **Pin Mapping**:
  - Header Pin 1 → P24
  - Header Pin 2 → P25
  - Header Pin 3 → P26
  - Header Pin 4 → P27
  - Header Pin 5 → P28
  - Header Pin 6 → P29
  - Header Pin 7 → P30
  - Header Pin 8 → P31
  - Header Pins 9-12 → Power/Ground

### Header E (Bottom Edge, Right)
- **P2 Port Range**: P32-P39
- **Pin Mapping**:
  - Header Pin 1 → P32
  - Header Pin 2 → P33
  - Header Pin 3 → P34
  - Header Pin 4 → P35
  - Header Pin 5 → P36
  - Header Pin 6 → P37
  - Header Pin 7 → P38
  - Header Pin 8 → P39
  - Header Pins 9-12 → Power/Ground

### Header F (Bottom Edge, Left)
- **P2 Port Range**: P40-P47
- **Pin Mapping**:
  - Header Pin 1 → P40
  - Header Pin 2 → P41
  - Header Pin 3 → P42
  - Header Pin 4 → P43
  - Header Pin 5 → P44
  - Header Pin 6 → P45
  - Header Pin 7 → P46
  - Header Pin 8 → P47
  - Header Pins 9-12 → Power/Ground

### Header G (Left Edge, Bottom)
- **P2 Port Range**: P48-P55
- **Pin Mapping**:
  - Header Pin 1 → P48
  - Header Pin 2 → P49
  - Header Pin 3 → P50
  - Header Pin 4 → P51
  - Header Pin 5 → P52
  - Header Pin 6 → P53
  - Header Pin 7 → P54
  - Header Pin 8 → P55
  - Header Pins 9-12 → Power/Ground

### Header H (Left Edge, Top)
- **P2 Port Range**: P56-P63
- **Pin Mapping**:
  - Header Pin 1 → P56 (Buffered LED)
  - Header Pin 2 → P57 (Buffered LED)
  - Header Pin 3 → P58 (Flash SPI DO/MISO)
  - Header Pin 4 → P59 (Flash SPI DI/MOSI)
  - Header Pin 5 → P60 (Flash SPI CLK)
  - Header Pin 6 → P61 (Flash SPI CS)
  - Header Pin 7 → P62 (Serial TXD to PC)
  - Header Pin 8 → P63 (Serial RXD from PC)
  - Header Pins 9-12 → Power/Ground

### P2 Edge Mini Breakout (#64019)
**Total Headers**: 6 sets of 2x6 headers
**Pin Coverage**: P0-P31, P56-P63 (40 pins at headers, P32-P55 require jumpers)

### Available Headers (Direct Access)
- **P0-P7 Header**: Maps to P0-P7 (includes 5V)
- **P8-P15 Header**: Maps to P8-P15 (includes 5V)
- **P16-P23 Header**: Maps to P16-P23 (includes 5V)
- **P24-P31 Header**: Maps to P24-P31 (NO 5V)
- **P48-P55 Header**: Maps to P48-P55 (includes 5V)
- **P56-P63 Header**: Maps to P56-P63 (NO 5V, includes RES pin)

### P2 Edge Standard Breakout (#64029)
**Total Headers**: 8 sets of 2x6 headers
**Pin Coverage**: Complete P0-P63 access

#### Header Mappings
- **P0-P7 Header**: Maps to P0-P7 (includes 5V)
- **P8-P15 Header**: Maps to P8-P15 (includes 5V)
- **P16-P23 Header**: Maps to P16-P23 (includes 5V)
- **P24-P31 Header**: Maps to P24-P31 (NO 5V)
- **P32-P39 Header**: Maps to P32-P39 (includes 5V)
- **P40-P47 Header**: Maps to P40-P47 (includes 5V)
- **P48-P55 Header**: Maps to P48-P55 (includes 5V)
- **P56-P63 Header**: Maps to P56-P63 (NO 5V, includes RES pin)

### P2 Edge Module Breadboard / JonnyMac Board (#64020)
**Total Headers**: 8 sets of 2x6 headers
**Pin Coverage**: Complete P0-P63 access
**Additional Features**: Large integrated breadboard, 8 servo/sensor ports
**Note**: Known as the "JonnyMac board" after designer Jon McPhalen

#### Header Mappings (same as Standard Breakout)
- **P0-P7 Header**: Maps to P0-P7 (includes 5V)
- **P8-P15 Header**: Maps to P8-P15 (includes 5V)
- **P16-P23 Header**: Maps to P16-P23 (includes 5V)
- **P24-P31 Header**: Maps to P24-P31 (NO 5V)
- **P32-P39 Header**: Maps to P32-P39 (includes 5V)
- **P40-P47 Header**: Maps to P40-P47 (includes 5V)
- **P48-P55 Header**: Maps to P48-P55 (includes 5V)
- **P56-P63 Header**: Maps to P56-P63 (NO 5V, includes RES pin)

### Pins Requiring Bottom-Side Access (Mini Breakout Only)
- **P32-P39**: No header on Mini Breakout, requires jumper wires
- **P40-P47**: No header on Mini Breakout, requires jumper wires

## Add-on Board Device Mappings

### #64006A - LED Array Board
**Devices**: 8 individual LEDs with 330Ω current limiting resistors
**Device-to-Header Mapping**:
- LED 0 → Header Pin 1
- LED 1 → Header Pin 2
- LED 2 → Header Pin 3
- LED 3 → Header Pin 4
- LED 4 → Header Pin 5
- LED 5 → Header Pin 6
- LED 6 → Header Pin 7
- LED 7 → Header Pin 8

### #64006B - Switch Array Board
**Devices**: 8 momentary push switches with 10kΩ pull-ups
**Device-to-Header Mapping**:
- Switch 0 → Header Pin 1
- Switch 1 → Header Pin 2
- Switch 2 → Header Pin 3
- Switch 3 → Header Pin 4
- Switch 4 → Header Pin 5
- Switch 5 → Header Pin 6
- Switch 6 → Header Pin 7
- Switch 7 → Header Pin 8

### #64006C - Potentiometer Board
**Devices**: 8 × 10kΩ linear potentiometers
**Device-to-Header Mapping**:
- Pot 0 (wiper) → Header Pin 1
- Pot 1 (wiper) → Header Pin 2
- Pot 2 (wiper) → Header Pin 3
- Pot 3 (wiper) → Header Pin 4
- Pot 4 (wiper) → Header Pin 5
- Pot 5 (wiper) → Header Pin 6
- Pot 6 (wiper) → Header Pin 7
- Pot 7 (wiper) → Header Pin 8

### #64006D - Servo Header Board
**Devices**: 8 standard 3-pin servo connectors
**Device-to-Header Mapping**:
- Servo 0 (signal) → Header Pin 1
- Servo 1 (signal) → Header Pin 2
- Servo 2 (signal) → Header Pin 3
- Servo 3 (signal) → Header Pin 4
- Servo 4 (signal) → Header Pin 5
- Servo 5 (signal) → Header Pin 6
- Servo 6 (signal) → Header Pin 7
- Servo 7 (signal) → Header Pin 8
**Note**: Each servo connector also has +5V and GND connections

### #64006E - Sensor Board
**Devices**: Temperature, light, and sound sensors
**Device-to-Header Mapping** (typical configuration):
- Temperature sensor output → Header Pin 1
- Light sensor output → Header Pin 2
- Sound sensor output → Header Pin 3
- Reserved → Header Pins 4-8

### #64006G - Digital I/O Board
**Devices**: 4 LEDs and 4 switches
**Device-to-Header Mapping**:
- LED 0 / Switch 0 → Header Pin 1
- LED 1 / Switch 1 → Header Pin 2
- LED 2 / Switch 2 → Header Pin 3
- LED 3 / Switch 3 → Header Pin 4
- Reserved → Header Pins 5-8

### #64006H - Analog I/O Board
**Devices**: 4 potentiometers and 4 analog sensors
**Device-to-Header Mapping**:
- Potentiometer 0 → Header Pin 1
- Potentiometer 1 → Header Pin 2
- Potentiometer 2 → Header Pin 3
- Potentiometer 3 → Header Pin 4
- Analog sensor 0 → Header Pin 5
- Analog sensor 1 → Header Pin 6
- Analog sensor 2 → Header Pin 7
- Analog sensor 3 → Header Pin 8

## Board Comparison Summary

| Board | Total Headers | Pin Access | Size | Special Features |
|-------|--------------|------------|------|------------------|
| P2 Eval Rev C (#64000) | 8 | P0-P63 (64 pins) | 3.55 × 3.55 in | LEDs, switches, full featured |
| Edge Mini (#64019) | 6 | P0-P31, P56-P63 (40 pins) | 3.15 × 1.4 in | Compact, prototyping areas |
| Edge Standard (#64029) | 8 | P0-P63 (64 pins) | 4.0 × 1.4 in | All pins at headers |
| JonnyMac/Edge Breadboard (#64020) | 8 | P0-P63 (64 pins) | 3.5 × 8 in | Large breadboard, servo ports |

## Complete Mapping Examples

### Example 1: LED Array on P2 Eval Board Header A
**Setup**: #64006A LED Array Board plugged into Header A of P2 Eval Board
**Complete Mapping**:
- LED 0 → Header Pin 1 → P0
- LED 1 → Header Pin 2 → P1
- LED 2 → Header Pin 3 → P2
- LED 3 → Header Pin 4 → P3
- LED 4 → Header Pin 5 → P4
- LED 5 → Header Pin 6 → P5
- LED 6 → Header Pin 7 → P6
- LED 7 → Header Pin 8 → P7

**Generated Code**:
```spin2
CON
  LED_BASE = 0  ' LEDs start at P0
  LED_COUNT = 8

PUB flash_leds() | i
  repeat i from LED_BASE to LED_BASE + LED_COUNT - 1
    PINHIGH(i)
    WAITMS(100)
    PINLOW(i)
```

### Example 2: Servo Board on P2 Eval Board Header E
**Setup**: #64006D Servo Header Board plugged into Header E of P2 Eval Board
**Complete Mapping**:
- Servo 0 → Header Pin 1 → P32
- Servo 1 → Header Pin 2 → P33
- Servo 2 → Header Pin 3 → P34
- Servo 3 → Header Pin 4 → P35
- Servo 4 → Header Pin 5 → P36
- Servo 5 → Header Pin 6 → P37
- Servo 6 → Header Pin 7 → P38
- Servo 7 → Header Pin 8 → P39

**Generated Code**:
```spin2
CON
  SERVO_BASE = 32  ' Servos start at P32
  SERVO_COUNT = 8

PUB init_servos() | i
  repeat i from SERVO_BASE to SERVO_BASE + SERVO_COUNT - 1
    PINSTART(i, P_PWM_TRIANGLE | P_OE, 20_000, 1500)  ' 50Hz, 1.5ms pulse
```

### Example 3: Mixed Setup on Edge Mini Breakout
**Setup**: 
- LED Array on P0-P7 header
- Potentiometer Board on P8-P15 header

**Complete Mapping**:
- LEDs 0-7 → P0-P7
- Pots 0-7 → P8-P15

**Generated Code**:
```spin2
CON
  LED_BASE = 0
  POT_BASE = 8
  
PUB read_pot_set_led() | pot_val
  PINSTART(POT_BASE, P_ADC_1X | P_ADC, 0, 0)  ' Configure ADC
  pot_val := PINREAD(POT_BASE) >> 24          ' Get 8-bit value
  PINWRITE(LED_BASE, pot_val)                 ' Set LED brightness via PWM
```

## Code Generation Rules

### Pin Assignment Constants
When generating code for a specific board combination:

1. **Identify main board** (Eval Board, Edge Mini, etc.)
2. **Identify header location** (A-H for Eval, specific ranges for Edge)
3. **Identify add-on board** type
4. **Generate constants** for base pin and device count

### Smart Pin Configuration
Based on add-on board type, automatically configure Smart Pins:

- **LED boards**: PWM mode for brightness control
- **Switch boards**: Edge detection with debouncing
- **Potentiometer boards**: ADC mode, 0-3.3V range
- **Servo boards**: PWM mode, 50Hz, 1-2ms pulses
- **Sensor boards**: ADC mode with appropriate scaling

### Example Code Generation Function
```python
def generate_pin_constants(main_board, header_location, addon_board):
    # Map header location to P2 port range
    port_ranges = {
        'eval_A': (0, 7),
        'eval_B': (8, 15),
        'eval_C': (16, 23),
        'eval_D': (24, 31),
        'eval_E': (32, 39),
        'eval_F': (40, 47),
        'eval_G': (48, 55),
        'eval_H': (56, 63),
        'edge_mini_1': (0, 7),
        'edge_mini_2': (8, 15),
        # ... etc
    }
    
    base_pin = port_ranges[f"{main_board}_{header_location}"][0]
    
    # Generate Spin2 constants
    return f"""
CON
  {addon_board.upper()}_BASE = {base_pin}
  {addon_board.upper()}_COUNT = 8
"""
```

## Hardware Abstraction Benefits

This mapping knowledge enables:

1. **Automatic pin assignment** - No manual lookup required
2. **Board-agnostic code** - Same code works on different header locations
3. **Error prevention** - Validates legal board combinations
4. **Smart Pin automation** - Configures appropriate modes per device type
5. **Documentation generation** - Creates pinout diagrams for user reference

## Future Extensions

### Additional Main Boards
- P2 Edge Module Breadboard mappings
- JonnyMac board (if different from Eval)
- Custom carrier boards

### Additional Add-on Boards
- HyperRAM modules
- Audio I/O boards
- Video output boards
- Custom sensor arrays

### Enhanced Mappings
- Power consumption per configuration
- Signal integrity considerations
- Maximum frequency per pin/board combination
- Thermal considerations for high-current configurations

---

**Document Status**: Initial mapping knowledge captured
**Trust Level**: HIGH - Based on official Parallax documentation
**Next Steps**: Validate with hardware testing, expand board coverage