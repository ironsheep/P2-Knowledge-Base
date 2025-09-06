# P2 Eval HUB75 Adapter Board (64032) - Preliminary Knowledge
*Iron Sheep Productions, LLC*

## Board Overview
**SKU**: 64032
**Manufacturer**: Iron Sheep Productions, LLC  
**Purpose**: Connect HUB75 LED matrix panels to P2 Eval board
**Status**: Production board lacking official datasheet

## Known Specifications (To Be Confirmed)

### HUB75 Interface Standard
Standard 16-pin IDC connector for LED matrix panels:
1. R1 - Red data, upper half
2. G1 - Green data, upper half  
3. B1 - Blue data, upper half
4. GND
5. R2 - Red data, lower half
6. G2 - Green data, lower half
7. B2 - Blue data, lower half
8. GND
9. A - Row select bit 0
10. B - Row select bit 1
11. C - Row select bit 2
12. D - Row select bit 3
13. CLK - Clock signal
14. LAT - Latch signal
15. OE - Output Enable (active low)
16. GND

### Additional Signals (if 32+ row panels supported)
- E - Row select bit 4 (for 32+ row panels)

## P2 Pin Mapping (Preliminary)

Typical efficient mapping for P2:
```spin2
CON
  ' HUB75 Data pins (6 bits parallel)
  HUB75_R1 = 0   ' Red upper
  HUB75_G1 = 1   ' Green upper
  HUB75_B1 = 2   ' Blue upper
  HUB75_R2 = 3   ' Red lower
  HUB75_G2 = 4   ' Green lower
  HUB75_B2 = 5   ' Blue lower
  
  ' HUB75 Control pins
  HUB75_CLK = 6  ' Clock
  HUB75_LAT = 7  ' Latch
  HUB75_OE = 8   ' Output Enable
  
  ' Row select pins
  HUB75_A = 9    ' Row bit 0
  HUB75_B = 10   ' Row bit 1
  HUB75_C = 11   ' Row bit 2
  HUB75_D = 12   ' Row bit 3
  HUB75_E = 13   ' Row bit 4 (if present)
```

## Power Considerations

### LED Panel Power
- Panels require 5V power (not from P2)
- Current depends on panel size and brightness
- Typical 32x64 panel: 2-4A peak @ 5V
- Must use external 5V supply

### Logic Level Translation
- HUB75 expects 5V logic
- P2 outputs 3.3V logic
- May include level shifters (TBD)
- Or rely on 3.3V meeting VIH threshold

## Supported Panel Configurations

### Common Panel Sizes
- 16x32 (512 LEDs)
- 32x32 (1024 LEDs)  
- 32x64 (2048 LEDs)
- 64x64 (4096 LEDs)

### Daisy-Chaining
- Multiple panels in series
- Data flows through panels
- Single clock/control for chain
- Power distributed per panel

## Driver Architecture

### Refresh Strategy
```spin2
PUB drive_panel() | row
  repeat
    repeat row from 0 to 15  ' For 32-row panel (scan 1/16)
      ' Set row address
      OUTH[HUB75_A..HUB75_D] := row
      
      ' Clock out 64 pixels (for 64-wide panel)
      repeat 64
        OUTH[HUB75_R1..HUB75_B2] := get_next_pixels()
        PINHIGH(HUB75_CLK)
        PINLOW(HUB75_CLK)
        
      ' Latch data
      PINLOW(HUB75_OE)   ' Blank display
      PINHIGH(HUB75_LAT) ' Latch new data
      PINLOW(HUB75_LAT)
      PINHIGH(HUB75_OE)  ' Enable display
```

### Smart Pin Utilization
- Clock generation via Smart Pin PWM
- Streamer for parallel data output
- Multiple COGs for higher refresh rates

## Required Information for Datasheet

### Physical Specifications
- [ ] Board dimensions
- [ ] Mounting hole locations
- [ ] Connector types and positions
- [ ] Weight

### Electrical Specifications  
- [ ] Exact P2 pin assignments
- [ ] Level shifter specifications (if present)
- [ ] Current consumption
- [ ] Maximum clock frequency
- [ ] Signal timing requirements

### Compatibility
- [ ] Compatible P2 boards (Eval, Edge, etc.)
- [ ] Compatible HUB75 panel list
- [ ] Maximum panels supported
- [ ] Refresh rate capabilities

### Software Support
- [ ] Example driver code
- [ ] Panel configuration utilities
- [ ] Brightness/color correction
- [ ] Multi-panel synchronization

## Code Examples Needed

### Basic Panel Test
```spin2
PUB test_panel()
  ' Initialize pins
  DIRL(HUB75_R1..HUB75_E)
  
  ' Simple test pattern
  repeat
    ' Fill red
    fill_color($FF, $00, $00)
    waitms(1000)
    
    ' Fill green  
    fill_color($00, $FF, $00)
    waitms(1000)
    
    ' Fill blue
    fill_color($00, $00, $FF)
    waitms(1000)
```

### PWM Brightness Control
```spin2
PUB set_brightness(level) | pwm_duty
  pwm_duty := level * 256 / 100  ' Convert percentage
  
  ' Use Smart Pin for OE PWM
  WRPIN(HUB75_OE, P_PWM_SAWTOOTH)
  WXPIN(HUB75_OE, $100_0000 | pwm_duty)
  DIRH(HUB75_OE)
```

### Streamer-Based Fast Output
```spin2
PUB stream_row(row_buffer)
  ' Setup streamer for 6-bit parallel output
  SETXFRQ($8000_0000)  ' Max rate
  SETSTREAMER(X_RFBYTE_RGB, row_buffer, HUB75_R1)
  
  ' Stream automatically outputs RGB data
```

## Action Items for Complete Datasheet

1. **Measure and document physical specifications**
2. **Map exact P2 pin connections**
3. **Test and specify electrical characteristics**
4. **Create comprehensive example code library**
5. **Generate timing diagrams**
6. **Write user guide section**
7. **Create troubleshooting guide**
8. **Format in Parallax datasheet style**

## Related Documentation Needs

- Application note: Multi-panel video walls
- Application note: Scrolling text displays  
- Reference: HUB75 protocol specification
- Example: Weather station display
- Example: Spectrum analyzer visualization