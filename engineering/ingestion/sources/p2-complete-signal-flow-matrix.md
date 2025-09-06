# P2 Complete Signal Flow Matrix
*End-to-end signal path from device to P2 core*

## Signal Flow Architecture

```
[Physical Device] → [Add-on Board Circuit] → [Header Pin] → 
[Main Board Header] → [P2 Pin] → [Smart Pin] → [Cog]
```

## Complete Signal Path Tables

### LED Signal Paths (64025 Board)

| LED # | Circuit Element | Header Pin | Board Location | P2 Port | Smart Pin Mode | Cog Access |
|-------|----------------|------------|----------------|---------|----------------|------------|
| LED0 | 330Ω→LED→GND | Pin 1 | Rev C: P0 | P0 | P_NORMAL | OUTH[0] |
| | | | Edge: P32 | P32 | P_NORMAL | OUTH[32] |
| LED1 | 330Ω→LED→GND | Pin 2 | Rev C: P1 | P1 | P_NORMAL | OUTH[1] |
| | | | Edge: P33 | P33 | P_NORMAL | OUTH[33] |
| LED2 | 330Ω→LED→GND | Pin 3 | Rev C: P2 | P2 | P_NORMAL | OUTH[2] |
| | | | Edge: P34 | P34 | P_NORMAL | OUTH[34] |
| LED3 | 330Ω→LED→GND | Pin 4 | Rev C: P3 | P3 | P_NORMAL | OUTH[3] |
| | | | Edge: P35 | P35 | P_NORMAL | OUTH[35] |
| LED4 | 330Ω→LED→GND | Pin 5 | Rev C: P4 | P4 | P_NORMAL | OUTH[4] |
| | | | Edge: P36 | P36 | P_NORMAL | OUTH[36] |
| LED5 | 330Ω→LED→GND | Pin 6 | Rev C: P5 | P5 | P_NORMAL | OUTH[5] |
| | | | Edge: P37 | P37 | P_NORMAL | OUTH[37] |
| LED6 | 330Ω→LED→GND | Pin 7 | Rev C: P6 | P6 | P_NORMAL | OUTH[6] |
| | | | Edge: P38 | P38 | P_NORMAL | OUTH[38] |
| LED7 | 330Ω→LED→GND | Pin 8 | Rev C: P7 | P7 | P_NORMAL | OUTH[7] |
| | | | Edge: P39 | P39 | P_NORMAL | OUTH[39] |

**Signal Characteristics:**
- Output Type: Digital push-pull
- Drive Current: 20mA nominal, 50mA absolute max
- Logic Levels: 0V (OFF), 3.3V (ON)
- Rise/Fall Time: <2ns at 50Ω load

### Switch Signal Paths (64027 Board)

| Switch # | Circuit Element | Header Pin | Board Location | P2 Port | Smart Pin Mode | Cog Access |
|----------|----------------|------------|----------------|---------|----------------|------------|
| SW0 | Switch→GND | Pin 1 | Rev C: P0 | P0 | P_HIGH_15K | INA[0] |
| | 10kΩ Pull-up | | Edge: P32 | P32 | P_HIGH_15K | INA[32] |
| SW1 | Switch→GND | Pin 2 | Rev C: P1 | P1 | P_HIGH_15K | INA[1] |
| | 10kΩ Pull-up | | Edge: P33 | P33 | P_HIGH_15K | INA[33] |
| SW2 | Switch→GND | Pin 3 | Rev C: P2 | P2 | P_HIGH_15K | INA[2] |
| | 10kΩ Pull-up | | Edge: P34 | P34 | P_HIGH_15K | INA[34] |
| SW3 | Switch→GND | Pin 4 | Rev C: P3 | P3 | P_HIGH_15K | INA[3] |
| | 10kΩ Pull-up | | Edge: P35 | P35 | P_HIGH_15K | INA[35] |
| SW4 | Switch→GND | Pin 5 | Rev C: P4 | P4 | P_HIGH_15K | INA[4] |
| | 10kΩ Pull-up | | Edge: P36 | P36 | P_HIGH_15K | INA[36] |
| SW5 | Switch→GND | Pin 6 | Rev C: P5 | P5 | P_HIGH_15K | INA[5] |
| | 10kΩ Pull-up | | Edge: P37 | P37 | P_HIGH_15K | INA[37] |
| SW6 | Switch→GND | Pin 7 | Rev C: P6 | P6 | P_HIGH_15K | INA[6] |
| | 10kΩ Pull-up | | Edge: P38 | P38 | P_HIGH_15K | INA[38] |
| SW7 | Switch→GND | Pin 8 | Rev C: P7 | P7 | P_HIGH_15K | INA[7] |
| | 10kΩ Pull-up | | Edge: P39 | P39 | P_HIGH_15K | INA[39] |

**Signal Characteristics:**
- Input Type: Digital with internal pull-up
- Logic Levels: 0V (pressed), 3.3V (released)
- Debounce Required: 10-50ms typical
- Current Draw: 220µA through pull-up when pressed

### 7-Segment Display Signal Paths (64026 Board)

| Signal | Function | Circuit | Header Pin | P2 Port (Rev C) | P2 Port (Edge) | Drive Required |
|--------|----------|---------|------------|-----------------|----------------|----------------|
| A | Segment A | LED+Resistor | Pin 1 | P0 | P32 | 20mA |
| B | Segment B | LED+Resistor | Pin 2 | P1 | P33 | 20mA |
| C | Segment C | LED+Resistor | Pin 3 | P2 | P34 | 20mA |
| D | Segment D | LED+Resistor | Pin 4 | P3 | P35 | 20mA |
| E | Segment E | LED+Resistor | Pin 5 | P4 | P36 | 20mA |
| F | Segment F | LED+Resistor | Pin 6 | P5 | P37 | 20mA |
| G | Segment G | LED+Resistor | Pin 7 | P6 | P38 | 20mA |
| DP | Decimal Point | LED+Resistor | Pin 8 | P7 | P39 | 20mA |
| DIG0 | Digit 0 Enable | Transistor | Pin 9 | P8 | P40 | 5mA (base) |
| DIG1 | Digit 1 Enable | Transistor | Pin 10 | P9 | P41 | 5mA (base) |
| DIG2 | Digit 2 Enable | Transistor | Pin 11 | P10 | P42 | 5mA (base) |
| DIG3 | Digit 3 Enable | Transistor | Pin 12 | P11 | P43 | 5mA (base) |
| DIG4 | Digit 4 Enable | Extra 1 | P12 | P44 | 5mA (base) |
| DIG5 | Digit 5 Enable | Extra 2 | P13 | P45 | 5mA (base) |

**Multiplexing Requirements:**
- Refresh Rate: >60Hz to avoid flicker
- Duty Cycle: 1/6 for 6 digits (16.7%)
- Peak Current: 8 segments × 20mA = 160mA per digit
- Average Current: 160mA / 6 = 27mA continuous

### Analog Signal Paths (40004 Goertzel Board)

| Signal | Source | Processing | Header | P2 Port (Rev C) | P2 Port (Edge) | Smart Pin Mode |
|--------|--------|------------|--------|-----------------|----------------|----------------|
| Audio In | Microphone | Pre-amp→Filter | Pin 3 | P2 | P34 | P_ADC_1X |
| Tone Out | DAC | Buffer Amp | Pin 4 | P3 | P35 | P_DAC_124R_3V |
| AGC Feedback | Envelope | Comparator | Pin 5 | P4 | P36 | P_ADC_GIO |
| Reference | Voltage Ref | Buffer | Pin 6 | P5 | P37 | P_ADC_VIO |
| Filter Control | Digital | RC Filter | Pin 7 | P6 | P38 | P_PWM_SAWTOOTH |
| Gain Control | Digital | VCA | Pin 8 | P7 | P39 | P_DAC_990R_3V |

**Analog Specifications:**
- ADC Resolution: 8-14 bits (configurable)
- ADC Sample Rate: Up to 1MSPS
- DAC Resolution: 8 bits (PWM), 16 bits (dithered)
- Input Impedance: >10kΩ
- Output Impedance: <100Ω

## Smart Pin Configuration Details

### Digital Output Modes (LEDs, 7-Segment)
```spin2
' Basic digital output - no Smart Pin needed
DIRH(pin)               ' Set as output
OUTH(pin) := state     ' Set high/low

' PWM for brightness control
WRPIN(pin, P_PWM_SAWTOOTH)
WXPIN(pin, $100_0000 | brightness)  ' 8-bit PWM
DIRH(pin)
```

### Digital Input Modes (Switches, Buttons)
```spin2
' Input with pull-up
WRPIN(pin, P_HIGH_15K)   ' 15kΩ pull-up
state := INH(pin)        ' Read state

' Input with schmitt trigger
WRPIN(pin, P_SCHMITT_A)  ' Schmitt trigger input
state := INH(pin)        ' Clean transitions
```

### Analog Modes (Goertzel, Audio)
```spin2
' ADC configuration
WRPIN(pin, P_ADC | P_ADC_1X)  ' Unity gain ADC
WXPIN(pin, 13)                 ' 14-bit conversions
DIRH(pin)                      ' Start ADC
value := RDPIN(pin) SAR 18    ' Read and scale

' DAC configuration  
WRPIN(pin, P_DAC_124R_3V)     ' 124Ω, 3.3V DAC
DIRH(pin)                      ' Enable DAC
WYPIN(pin, value)              ' Set output level
```

## Cog-to-Cog Signal Routing

### Hub RAM Signal Path
```
Cog0 → Hub RAM → Cog1
      ↓        ↑
   Cog Write  Cog Read
   4-16 clocks latency
```

### Lock-Based Synchronization
```spin2
VAR
  long signal_data
  byte lock_id

PUB cog0_writer()
  repeat while LOCKTRY(lock_id)  ' Wait for lock
  signal_data := new_value       ' Update signal
  LOCKREL(lock_id)               ' Release lock

PUB cog1_reader()  
  repeat while LOCKTRY(lock_id)  ' Wait for lock
  local_copy := signal_data      ' Read signal
  LOCKREL(lock_id)               ' Release lock
```

### Event-Based Signaling
```spin2
' Cog 0: Signal producer
COGATN(1 << target_cog)  ' Signal target cog

' Cog 1: Signal consumer
POLLATN()                ' Check for attention
if POLLATN()
  ' Process signal
```

## Power Domain Mapping

### VIO Group Distribution

| VIO Group | P2 Pins | Board Headers | Current Limit | Typical Load |
|-----------|---------|---------------|---------------|--------------|
| VIO_0 | P0-P7 | Rev C: Pins 1-8 | 150mA | LEDs/Switches |
| VIO_1 | P8-P15 | Rev C: Pins 9-12+ | 150mA | 7-Seg digits |
| VIO_2 | P16-P23 | Rev C: Extra | 150mA | User defined |
| VIO_3 | P24-P31 | Rev C: Extra | 150mA | User defined |
| VIO_4 | P32-P39 | Edge: Pins 1-8 | 150mA | LEDs/Switches |
| VIO_5 | P40-P47 | Edge: Pins 9-12+ | 150mA | 7-Seg/Combo |
| VIO_6 | P48-P55 | Edge: Extra | 150mA | User defined |
| VIO_7 | P56-P63 | Edge: Special | 150mA | Serial/Boot |

### Power Budget Calculation
```spin2
CON
  ' Current per element (mA)
  LED_CURRENT = 20
  SEGMENT_CURRENT = 20  
  PULLUP_CURRENT = 0.22  ' 220µA
  ANALOG_CURRENT = 10
  
PUB calculate_vio_load(board_type, addon_type) : total_ma
  case addon_type
    ADDON_64025_LED:
      total_ma := LED_CURRENT * 8
    ADDON_64026_7SEG:
      total_ma := SEGMENT_CURRENT * 8  ' Per digit when active
    ADDON_64027_SWITCH:
      total_ma := PULLUP_CURRENT * 8
    ADDON_64029_COMBO:
      total_ma := (LED_CURRENT * 4) + (PULLUP_CURRENT * 8)
    ADDON_40004_GOERTZEL:
      total_ma := ANALOG_CURRENT * 2
      
  if total_ma > 150
    debug("WARNING: Exceeds VIO group limit!")
```

## Signal Integrity Considerations

### Digital Signal Quality
```
Signal Path Analysis:
P2 Output → PCB Trace → Header → Add-on PCB → Device

Typical Trace Impedance: 50-75Ω
Maximum Frequency: 250MHz (P2 clock)
Rise Time: <2ns
Recommended: Keep traces <3 inches for >50MHz signals
```

### Analog Signal Quality  
```
Noise Sources:
- Digital switching noise: -60dB typical
- Power supply noise: -70dB with proper bypassing
- Thermal noise floor: -110dBm

Mitigation:
- Separate analog/digital grounds
- Star ground at single point
- 0.1µF bypass caps at each VIO pin
- Ferrite beads on analog supplies
```

## Timing Specifications

### Digital I/O Timing

| Parameter | Min | Typical | Max | Unit |
|-----------|-----|---------|-----|------|
| Output Valid | - | 2 | 4 | ns |
| Input Setup | 1.5 | - | - | ns |
| Input Hold | 0.5 | - | - | ns |
| Propagation | - | 3 | 5 | ns |

### Smart Pin Timing

| Mode | Latency | Resolution | Max Rate |
|------|---------|------------|----------|
| Digital I/O | 2 clocks | 1 clock | FCLK/2 |
| PWM | 4 clocks | 1 clock | FCLK/2^16 |
| ADC | 16 clocks | 8-14 bits | 1 MSPS |
| DAC | 3 clocks | 8-16 bits | FCLK/2 |

## Complete Code Generation Framework

### Universal Board/Addon Detector
```spin2
CON
  ' Board type detection (based on known pins)
  BOARD_UNKNOWN = 0
  BOARD_REVC = 1
  BOARD_EDGE_MINI = 2
  BOARD_EDGE_STD = 3
  BOARD_JONNYMAC = 4
  
  ' Addon type detection
  ADDON_UNKNOWN = 0
  ADDON_64025_LED = 1
  ADDON_64026_7SEG = 2
  ADDON_64027_SWITCH = 3
  ADDON_64028_BUTTON = 4
  ADDON_64029_COMBO = 5
  ADDON_40003_PROTO = 6
  ADDON_40004_GOERTZEL = 7
  ADDON_40007_DIGITAL = 8

PUB detect_configuration() : board, addon | test_val
  ' Detect board type by testing known pins
  
  ' Check for Edge boards (P56-57 typically serial)
  FLTL(56 ADDPINS 1)
  WRPIN(56, P_HIGH_15K)
  waitms(1)
  test_val := INA[56]
  
  if test_val == 1  ' Pull-up worked
    board := BOARD_EDGE_MINI  ' Or STD/JONNYMAC
  else
    board := BOARD_REVC
    
  ' Detect addon by impedance signature
  addon := detect_addon_signature()
  
PRI detect_addon_signature() : addon_type | z_test
  ' Measure impedance characteristics
  
  ' Float all test pins
  FLTL(base_pin ADDPINS 11)
  waitms(10)
  
  ' Check natural state
  z_test := INA[base_pin ADDPINS 7]
  
  case z_test
    $FF:  ' All high = external pull-ups
      return ADDON_64027_SWITCH
    $00:  ' All low = LEDs or no connection
      return detect_led_vs_none()
    other:
      return ADDON_UNKNOWN
      
PRI detect_led_vs_none() : addon_type
  ' Try to detect LED forward voltage
  WRPIN(base_pin, P_HIGH_1K5)  ' Weak pull-up
  DIRH(base_pin)
  waitms(1)
  
  if INA[base_pin] == 0  ' Current flowing
    return ADDON_64025_LED
  else
    return ADDON_UNKNOWN
```

This completes the comprehensive signal flow matrix showing the complete path from physical devices through all stages to the P2 processor core!