# P2 Board-Addon Compatibility Matrix
*Complete cross-reference for automatic code generation*

## Matrix Overview

This matrix provides the complete mapping from any board+addon combination to:
1. Physical pin connections
2. P2 port assignments  
3. Smart Pin configurations
4. Generated initialization code
5. Power consumption estimates

## Compatibility Matrix

### Quick Reference Grid

| Add-on Board | Rev C | Edge Mini | Edge Standard | Edge Breadboard |
|-------------|-------|-----------|---------------|-----------------|
| 64025 LEDs | ✅ P0-P7 | ✅ P32-P39 | ✅ P32-P39 | ✅ P32-P39 |
| 64026 7-Segment | ✅ P0-P13 | ✅ P32-P45 | ✅ P32-P45 | ✅ P32-P45 |
| 64027 Switches | ✅ P0-P7 | ✅ P32-P39 | ✅ P32-P39 | ✅ P32-P39 |
| 64028 Buttons | ✅ P0-P7 | ✅ P32-P39 | ✅ P32-P39 | ✅ P32-P39 |
| 64029 Switches+LEDs | ✅ P0-P11 | ✅ P32-P43 | ✅ P32-P43 | ✅ P32-P43 |
| 40003 Protoboard | ✅ All 12 | ✅ All 12 | ✅ All 12 | ✅ All 12 |
| 40004 Goertzel | ✅ P2-P11 | ✅ P34-P43 | ✅ P34-P43 | ✅ P34-P43 |
| 40007 Digital I/O | ✅ P0-P11 | ✅ P32-P43 | ✅ P32-P43 | ✅ P32-P43 |
| 64032 HUB75 Adapter | ✅ P0-P13* | ✅ P16-P29** | ✅ P32-P45 | ✅ P32-P45 |

*Default configuration uses P16-P31 on Rev C board
**Recommended configuration for Rev C (default in driver)

## Detailed Configurations

### Rev C Board (#64006-ES) with Add-ons

#### With 64025 LED Board
```spin2
CON
  ' Physical: Header pins 1-8 → P2 ports P0-P7
  LED_BASE = 0
  LED_COUNT = 8
  
PUB led_init()
  PINL(LED_BASE ADDPINS (LED_COUNT-1))  ' All LEDs off
  DIRL(LED_BASE ADDPINS (LED_COUNT-1))  ' Set as outputs

PUB led_pattern(pattern)
  OUTH(LED_BASE ADDPINS 7) := pattern   ' Write 8-bit pattern
```
**Power**: 8 LEDs × 20mA = 160mA max @ 3.3V

#### With 64026 7-Segment Display Board
```spin2
CON
  ' Physical: Header pins 1-12 + extras → P2 ports P0-P13
  SEG_BASE = 0      ' Segments start at P0
  DIGIT_BASE = 8    ' Digit selects start at P8
  DIGITS = 6        ' 6 digits
  
PUB display_init()
  PINL(SEG_BASE ADDPINS 13)   ' All outputs low
  DIRL(SEG_BASE ADDPINS 13)   ' Set as outputs
  
PUB display_digit(digit, segments) | mask
  PINL(DIGIT_BASE ADDPINS (DIGITS-1))     ' All digits off
  OUTH(SEG_BASE ADDPINS 7) := segments    ' Set segment pattern
  PINHIGH(DIGIT_BASE + digit)             ' Enable selected digit
```
**Power**: 8 segments × 20mA + digit driver = 180mA per active digit

#### With 64027 Switches Board
```spin2
CON
  ' Physical: Header pins 1-8 → P2 ports P0-P7
  SW_BASE = 0
  SW_COUNT = 8
  
PUB switches_init()
  WRPIN(SW_BASE ADDPINS (SW_COUNT-1), P_HIGH_15K)  ' Enable pull-ups
  
PUB read_switches() : state
  state := INA[SW_BASE ADDPINS (SW_COUNT-1)] ^ $FF  ' Read and invert
```
**Power**: 8 × 220µA pull-up current = 1.76mA

#### With 64028 Buttons Board
```spin2
CON
  ' Physical: Header pins 1-8 → P2 ports P0-P7
  BTN_BASE = 0
  BTN_COUNT = 8
  
PUB buttons_init()
  WRPIN(BTN_BASE ADDPINS (BTN_COUNT-1), P_HIGH_15K)  ' Enable pull-ups
  
PUB wait_button() : button | mask
  repeat
    mask := INA[BTN_BASE ADDPINS (BTN_COUNT-1)] ^ $FF
    if mask
      button := ENCOD(mask)  ' Get highest priority button
      repeat while INA[BTN_BASE + button] == 0  ' Wait for release
      return button
```
**Power**: 8 × 220µA pull-up = 1.76mA

#### With 64029 Switches and LEDs Board
```spin2
CON
  ' Physical: Header pins 1-12 → P2 ports P0-P11
  SW_BASE = 0      ' Switches on P0-P7
  LED_BASE = 8     ' LEDs on P8-P11
  SW_COUNT = 8
  LED_COUNT = 4
  
PUB combo_init()
  ' Configure switches with pull-ups
  WRPIN(SW_BASE ADDPINS (SW_COUNT-1), P_HIGH_15K)
  ' Configure LEDs as outputs
  PINL(LED_BASE ADDPINS (LED_COUNT-1))
  DIRL(LED_BASE ADDPINS (LED_COUNT-1))
  
PUB mirror_switches_to_leds() | state
  repeat
    state := INA[SW_BASE ADDPINS 3] ^ $F  ' Read SW0-SW3, invert
    OUTH[LED_BASE ADDPINS 3] := state     ' Mirror to LEDs
```
**Power**: 8 switches (1.76mA) + 4 LEDs (80mA max) = 81.76mA

### Edge Mini Breakout Board (#64019) with Add-ons

#### With 64025 LED Board
```spin2
CON
  ' Physical: Header pins 1-8 → P2 ports P32-P39
  LED_BASE = 32
  LED_COUNT = 8
  
PUB led_init()
  PINL(LED_BASE ADDPINS (LED_COUNT-1))  ' All LEDs off
  DIRL(LED_BASE ADDPINS (LED_COUNT-1))  ' Set as outputs

PUB led_chase(delay_ms)
  repeat
    repeat led from 0 to 7
      PINHIGH(LED_BASE + led)
      waitms(delay_ms)
      PINLOW(LED_BASE + led)
```
**Power**: Same as Rev C (160mA max)

#### With 64026 7-Segment Display Board  
```spin2
CON
  ' Physical: Header pins 1-12 + extras → P2 ports P32-P45
  SEG_BASE = 32     ' Segments at P32-P39
  DIGIT_BASE = 40   ' Digits at P40-P45
  DIGITS = 6
  
  ' 7-segment patterns (active high, DP-G-F-E-D-C-B-A)
  DIGIT_0 = %00111111
  DIGIT_1 = %00000110
  DIGIT_2 = %01011011
  DIGIT_3 = %01001111
  DIGIT_4 = %01100110
  DIGIT_5 = %01101101
  DIGIT_6 = %01111101
  DIGIT_7 = %00000111
  DIGIT_8 = %01111111
  DIGIT_9 = %01101111
  
PUB display_number(value) | digit, digits[6], i
  ' Convert number to digits
  repeat i from 0 to 5
    digits[i] := value // 10
    value /= 10
    
  ' Multiplex display
  repeat 100  ' Show for ~100ms
    repeat digit from 0 to 5
      display_digit(digit, lookup(digits[digit]: DIGIT_0..DIGIT_9))
      waitus(2777)  ' ~6 digits @ 60Hz refresh
```
**Power**: 180mA per active digit (multiplex reduces average)

#### With 40004 Goertzel Board
```spin2
CON
  ' Physical: Headers use P34-P43 (skipping first 2 pins)
  GOERTZEL_BASE = 34
  FREQ_620Hz = 620
  FREQ_1209Hz = 1209
  FREQ_1336Hz = 1336
  FREQ_1477Hz = 1477
  FREQ_1633Hz = 1633
  
PUB goertzel_init()
  ' Configure for analog input on P34
  WRPIN(GOERTZEL_BASE, P_ADC_1X | P_ADC)
  WXPIN(GOERTZEL_BASE, 13)  ' 14-bit conversions
  DIRH(GOERTZEL_BASE)
  
PUB detect_dtmf_tone() : tone | samples[256], magnitude
  ' Collect ADC samples
  repeat 256
    samples[i++] := RDPIN(GOERTZEL_BASE) SAR 16
    waitus(125)  ' 8kHz sampling
    
  ' Run Goertzel algorithm for each DTMF frequency
  magnitude := goertzel_magnitude(@samples, 256, FREQ_1209Hz, 8000)
  if magnitude > THRESHOLD
    tone := "1"  ' Column 2 frequency detected
```
**Power**: Op-amp circuits ~10mA

### Edge Standard Board (#64029-ES) with Add-ons

The Edge Standard Board uses identical header mappings to Edge Mini Breakout, so all code examples above work by using the same pin definitions (P32-P43 range).

Key differences:
- More robust power delivery (can handle higher current loads)
- Better ground plane for analog operations
- All 64 P2 pins accessible (vs 40 on Mini without jumpers)

### Edge Breadboard / JonnyMac Board (#64020) with Add-ons

#### Special Considerations for JonnyMac Board
```spin2
CON
  ' JonnyMac has same header mapping but additional features
  ' Headers: P32-P43 same as other Edge boards
  ' Built-in: P56-P57 often used for serial
  ' Special: May have onboard LED on P56 or P57
  
  ADDON_BASE = 32     ' Add-on boards start here
  SERIAL_TX = 57      ' Common serial pin
  SERIAL_RX = 56      ' Common serial pin
  ONBOARD_LED = 57    ' If present
  
PUB jonny_mac_init()
  ' Initialize serial (if not using add-on pins)
  if SERIAL_TX >= 56
    serial.start(SERIAL_RX, SERIAL_TX, 0, 115200)
    
  ' Check for onboard LED
  if ONBOARD_LED >= 56
    PINH(ONBOARD_LED)
    DIRH(ONBOARD_LED)
```

## Power Budget Calculations

### Maximum Power per Board Combination

| Board | Add-on | Peak Current | Sustained | Notes |
|-------|--------|--------------|-----------|-------|
| Rev C | 64025 LEDs | 160mA | 80mA | Typical 50% duty |
| Rev C | 64026 7-Seg | 180mA | 30mA | Multiplexed |
| Rev C | 64029 Combo | 82mA | 42mA | 4 LEDs + switches |
| Edge Mini | 64025 LEDs | 160mA | 80mA | Check VIO group |
| Edge Mini | 40004 Goertzel | 15mA | 10mA | Analog circuits |
| All | 40003 Proto | Variable | Variable | User-defined |

### VIO Group Constraints
- Each VIO group limited to 150mA sustained
- P0-P31: VIO group 0 (Rev C headers)
- P32-P63: VIO group 1 (Edge board headers)
- Plan LED patterns to avoid exceeding limits

## Code Generation Patterns

### Universal Initialization Template
```spin2
OBJ
  system : "p2_system"
  
VAR
  long board_type
  long addon_type
  
PUB init(board, addon)
  board_type := board
  addon_type := addon
  
  case board_type
    BOARD_REVC:
      base_pin := 0
    BOARD_EDGE_MINI, BOARD_EDGE_STD, BOARD_JONNYMAC:
      base_pin := 32
      
  case addon_type
    ADDON_64025_LED:
      init_leds(base_pin)
    ADDON_64026_7SEG:
      init_7segment(base_pin)
    ADDON_64027_SWITCH:
      init_switches(base_pin)
    ADDON_64028_BUTTON:
      init_buttons(base_pin)
    ADDON_64029_COMBO:
      init_combo(base_pin)
```

### Auto-Detection Pattern
```spin2
PUB detect_addon() : addon_type | test_pins
  ' Try to detect add-on board by testing pin characteristics
  
  ' Check for pull-ups (indicates switches/buttons)
  FLTL(base_pin ADDPINS 7)  ' Float pins
  waitus(10)
  test_pins := INH[base_pin ADDPINS 7]
  
  if test_pins == $FF  ' All high = pull-ups present
    return ADDON_SWITCHES_OR_BUTTONS
    
  ' Check for LED drive capability
  DIRL(base_pin ADDPINS 7)
  OUTL(base_pin ADDPINS 7)
  waitus(1)
  
  ' Real detection would need external feedback
  ' This is simplified for demonstration
  return ADDON_UNKNOWN
```

## Hardware Testing Checklist

### Pre-Connection Verification
- [ ] Verify P2 board powered off
- [ ] Check add-on board orientation (pin 1 alignment)
- [ ] Inspect headers for bent pins
- [ ] Verify voltage jumper settings (3.3V for all add-ons)

### Connection Testing Protocol
1. **Power-off connection**: Always connect with power off
2. **Visual inspection**: Check alignment before power
3. **Power-on sequence**: 
   - Apply power to P2 board
   - Run detection code
   - Verify expected pins respond
4. **Functional test**: Run board-specific test code
5. **Power budget check**: Monitor current consumption

### Board-Specific Tests

#### LED Board Test
```spin2
PUB test_led_board() | i
  led_init()
  
  ' Test each LED individually
  repeat i from 0 to 7
    PINHIGH(LED_BASE + i)
    waitms(100)
    PINLOW(LED_BASE + i)
    
  ' Test all on (check current)
  OUTH[LED_BASE ADDPINS 7] := $FF
  waitms(500)
  
  ' Test patterns
  repeat 10
    OUTH[LED_BASE ADDPINS 7] := GETRND()
    waitms(200)
```

#### Switch/Button Board Test
```spin2
PUB test_switch_board() | state, last_state
  switches_init()
  
  last_state := 0
  repeat
    state := read_switches()
    if state <> last_state
      debug("Switch state: ", BIN8(state))
      last_state := state
    waitms(50)
```

#### 7-Segment Display Test  
```spin2
PUB test_7segment_board() | digit
  display_init()
  
  ' Test each digit position
  repeat digit from 0 to 5
    display_digit(digit, DIGIT_8)  ' All segments on
    waitms(500)
    
  ' Count on all digits
  repeat value from 0 to 999999
    display_number(value)
    waitms(10)
```

## Troubleshooting Guide

### Common Issues and Solutions

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| No LED response | Wrong base pin | Check board_type in code |
| Dim LEDs | Current limit | Check VIO group loading |
| Switch always reads 0 | No pull-ups | Enable P_HIGH_15K mode |
| Switch always reads 1 | Pin not input | Remove DIRH for that pin |
| 7-seg ghosting | Slow multiplex | Increase refresh rate |
| Partial digit display | Power issue | Check total current draw |
| Erratic behavior | Poor connection | Reseat header connection |

### Debug Utilities
```spin2
PUB diagnose_connection(base, count)
  debug("Testing pins P", DEC(base), " to P", DEC(base+count-1))
  
  ' Test as outputs (safe current)
  repeat pin from base to base+count-1
    WRPIN(pin, P_HIGH_1K5)  ' Weak drive
    DIRH(pin)
    OUTH(pin)
    waitms(100)
    reading := INH(pin)
    debug("  P", DEC(pin), " output test: ", reading ? "PASS" : "FAIL")
    DIRL(pin)
    
  ' Test as inputs with pull-ups
  repeat pin from base to base+count-1  
    WRPIN(pin, P_HIGH_15K)
    waitms(1)
    reading := INH(pin)
    debug("  P", DEC(pin), " pull-up test: ", reading ? "PASS" : "FAIL")
```

### P2 Eval Board with HUB75 Adapter (64032)

#### Default Configuration (P16-P31)
```spin2
CON
  ' Iron Sheep Productions HUB75 Adapter
  ' Default configuration for P2 Eval Board
  HUB75_BASE = 16  ' P16-P31 (recommended)
  
OBJ
  display : "isp_hub75_matrix"
  
PUB start_hub75_64x32()
  ' Initialize 64x32 panel with ISP driver
  display.start(HUB75_BASE, 64, 32)
  display.setBrightness(100)  ' 40% brightness
  
  ' Demo pattern
  display.clear($0000)
  display.drawBox(0, 0, 63, 31, $F800)  ' Red border
  display.drawText(8, 12, string("P2+HUB75"), $07E0)  ' Green text
  display.update()
```
**Power**: Adapter: 35mA @ 35MHz, Panel: 3-4A @ 5V external

## Code Generation Examples

### Complete Application: Simon Says Game
Using Edge Mini + 64029 (Switches and LEDs) Board:

```spin2
CON
  _CLKFREQ = 200_000_000
  
  ' Edge Mini with 64029 board
  SW_BASE = 32      ' P32-P39: 8 switches
  LED_BASE = 40     ' P40-P43: 4 LEDs
  
  MAX_SEQUENCE = 100
  
VAR
  byte sequence[MAX_SEQUENCE]
  long score
  
PUB main() | level
  combo_init()
  
  debug("Simon Says - Press SW0 to start")
  wait_for_switch(0)
  
  repeat
    level := play_game()
    debug("Game Over! Score: ", DEC(level))
    show_score_on_leds(level)
    waitms(3000)
    
PUB play_game() : level | i
  level := 1
  
  repeat
    ' Generate and show sequence
    if level > MAX_SEQUENCE
      return level-1
      
    sequence[level-1] := GETRND() & 3  ' Random LED 0-3
    
    ' Show sequence
    repeat i from 0 to level-1
      flash_led(sequence[i])
      waitms(500)
      
    ' Get player input
    repeat i from 0 to level-1
      button := wait_for_switch_timeout(5000)
      if button <> sequence[i]
        return level-1  ' Wrong button
      flash_led(button)
      
    level++
    waitms(1000)
    
PUB flash_led(num)
  PINHIGH(LED_BASE + num)
  waitms(300)
  PINLOW(LED_BASE + num)
  
PUB wait_for_switch_timeout(ms) : switch | timeout
  timeout := GETMS() + ms
  
  repeat while GETMS() < timeout
    repeat switch from 0 to 3
      if INA[SW_BASE + switch] == 0  ' Active low
        repeat while INA[SW_BASE + switch] == 0  ' Debounce
        return switch
        
  return -1  ' Timeout
```

This completes the comprehensive board-addon matrix with full code generation capabilities!