# P2 Eval HUB75 Adapter Board - Complete Pin Mapping
*SKU 64032 - Iron Sheep Productions, LLC*

## Official P2 Pin Assignments

The HUB75 Adapter Board uses a base pin + offset system. The default configuration uses **P16-P31** as the base pin group.

### Pin Mapping Table (Base = P16)

| HUB75 Signal | Offset | P2 Pin (P16 base) | P2 Pin (P0 base) | P2 Pin (P32 base) | Function |
|--------------|--------|-------------------|------------------|-------------------|----------|
| CLK | io+0 | P16 | P0 | P32 | Clock signal |
| OE# | io+1 | P17 | P1 | P33 | Output Enable (active low) |
| LAT | io+2 | P18 | P2 | P34 | Latch Enable |
| A | io+3 | P19 | P3 | P35 | Row Address bit 0 |
| B | io+4 | P20 | P4 | P36 | Row Address bit 1 |
| C | io+5 | P21 | P5 | P37 | Row Address bit 2 |
| D | io+6 | P22 | P6 | P38 | Row Address bit 3 |
| E | io+7 | P23 | P7 | P39 | Row Address bit 4 |
| R1 | io+8 | P24 | P8 | P40 | Red data - upper half |
| G1 | io+9 | P25 | P9 | P41 | Green data - upper half |
| B1 | io+10 | P26 | P10 | P42 | Blue data - upper half |
| R2 | io+11 | P27 | P11 | P43 | Red data - lower half |
| G2 | io+12 | P28 | P12 | P44 | Green data - lower half |
| B2 | io+13 | P29 | P13 | P45 | Blue data - lower half |
| - | io+14 | P30 | P14 | P46 | (unused) |
| - | io+15 | P31 | P15 | P47 | (unused) |

### Connector Organization

#### Upper Connector (J1 on P2 Eval Board)
- **Pins 1-6**: P16-P21 (CLK, OE#, LAT, A, B, C)
- **Pins 7-12**: P22-P27 (D, E, R1, G1, B1, R2)

#### Lower Connector (J2 on P2 Eval Board)
- **Pins 1-6**: P28-P33 (G2, B2, unused, unused, unused, unused)
- **Pins 7-12**: Not used for HUB75 signals

## Configuration Constants

### Spin2 Configuration Example

```spin2
CON
  ' Base pin selection (choose one)
  DISP0_ADAPTER_BASE_PIN = hwEnum.PINS_P0_P15    ' Use P0-P15
  DISP0_ADAPTER_BASE_PIN = hwEnum.PINS_P16_P31   ' Use P16-P31 (DEFAULT)
  DISP0_ADAPTER_BASE_PIN = hwEnum.PINS_P32_P47   ' Use P32-P47
  DISP0_ADAPTER_BASE_PIN = hwEnum.PINS_P48_P63   ' Use P48-P63
  
  ' Pin offsets from base (DO NOT CHANGE)
  PIN_CLK = 0      ' Base + 0
  PIN_OE = 1       ' Base + 1  
  PIN_LAT = 2      ' Base + 2
  PIN_ADDR_A = 3   ' Base + 3
  PIN_ADDR_B = 4   ' Base + 4
  PIN_ADDR_C = 5   ' Base + 5
  PIN_ADDR_D = 6   ' Base + 6
  PIN_ADDR_E = 7   ' Base + 7
  PIN_R1 = 8       ' Base + 8
  PIN_G1 = 9       ' Base + 9
  PIN_B1 = 10      ' Base + 10
  PIN_R2 = 11      ' Base + 11
  PIN_G2 = 12      ' Base + 12
  PIN_B2 = 13      ' Base + 13
```

### Address Line Configuration

```spin2
CON
  ' Select based on your panel type
  DISP0_ADDR_LINES = hwEnum.ADDR_ABC    ' 8 scan lines (16-row panels)
  DISP0_ADDR_LINES = hwEnum.ADDR_ABCD   ' 16 scan lines (32-row panels)
  DISP0_ADDR_LINES = hwEnum.ADDR_ABCDE  ' 32 scan lines (64-row panels)
```

## Signal Grouping Rationale

The pin assignment is optimized for P2 features:

### Control Group (P16-P23 / io+0 to io+7)
- **CLK, OE#, LAT**: Primary timing signals (io+0 to io+2)
- **A-E**: Address lines in sequence (io+3 to io+7)
- Benefit: Can be manipulated as single 8-bit value

### Data Group (P24-P29 / io+8 to io+13)
- **R1, G1, B1**: Upper half RGB (io+8 to io+10)
- **R2, G2, B2**: Lower half RGB (io+11 to io+13)
- Benefit: 6-bit parallel data perfect for P2 streamer

### Why This Layout?

1. **Streamer Optimization**: The 6 color bits (R1,G1,B1,R2,G2,B2) are consecutive, allowing efficient use of P2's streamer for parallel output

2. **Single Operation Updates**: Address lines (A-E) are consecutive, allowing single operation to set row address

3. **Smart Pin Compatible**: Each signal can use Smart Pin modes:
   - CLK: Can use Smart Pin NCO for precise timing
   - OE#: Can use Smart Pin PWM for brightness control
   - Data pins: Can use repository mode for buffering

4. **16-Pin Alignment**: Uses exactly 14 of 16 pins in a standard dual-header configuration, leaving 2 spares

## Hardware Interface Details

### Level Shifters
- All signals use 3.3V to 5V level shifting
- Maximum frequency: 70 MHz (limited by level shifter ICs)
- Bi-directional capability not required (all outputs)

### Power Distribution
- 5V power passed through from P2 board to HUB75 connector
- Level shifters powered from P2 board 5V
- Separate high-current 5V supply required for LED panels

## Usage Examples

### Basic Pin Setup
```spin2
PUB setup_pins() | base
  base := DISP0_ADAPTER_BASE_PIN
  
  ' Set all HUB75 pins as outputs
  DIRH(base ADDPINS 13)
  
  ' Initialize control signals
  OUTL(base + PIN_CLK)    ' Clock low
  OUTL(base + PIN_LAT)    ' Latch low  
  OUTH(base + PIN_OE)     ' Output disabled (active low)
```

### Writing Pixel Data
```spin2
PUB write_pixels(r1, g1, b1, r2, g2, b2) | base
  base := DISP0_ADAPTER_BASE_PIN
  
  ' Set color data
  OUTH(base + PIN_R1) := r1
  OUTH(base + PIN_G1) := g1
  OUTH(base + PIN_B1) := b1
  OUTH(base + PIN_R2) := r2
  OUTH(base + PIN_G2) := g2
  OUTH(base + PIN_B2) := b2
  
  ' Clock the data
  OUTH(base + PIN_CLK)
  OUTL(base + PIN_CLK)
```

### Setting Row Address
```spin2
PUB select_row(row) | base
  base := DISP0_ADAPTER_BASE_PIN
  
  ' Set address lines (5 bits for full range)
  OUTH[base+PIN_ADDR_A..base+PIN_ADDR_E] := row
```

## Alternative Base Pin Options

### P0-P15 Base (Edge Boards with P0 Access)
- Advantage: Leaves P32+ free for other peripherals
- Disadvantage: May conflict with boot/programming pins

### P32-P47 Base (Edge Module Standard)
- Advantage: Standard Edge Module header location
- Disadvantage: May limit other Edge Module accessories

### P48-P63 Base (Custom Applications)
- Advantage: Keeps lower pins free
- Disadvantage: P56-P63 often used for boot/serial

## Verification Test

```spin2
PUB verify_connections() | base, errors
  base := DISP0_ADAPTER_BASE_PIN
  errors := 0
  
  debug("HUB75 Adapter Pin Verification")
  debug("Base Pin: P", DEC(base))
  
  ' Test each pin can be toggled
  repeat offset from 0 to 13
    DIRL(base + offset)
    OUTH(base + offset)
    if INH(base + offset) <> 1
      debug("ERROR: Pin P", DEC(base + offset), " not responding")
      errors++
    OUTL(base + offset)
    
  if errors == 0
    debug("All pins verified successfully!")
  else
    debug(DEC(errors), " pins failed verification")
    
  return errors == 0
```

This complete pin mapping documentation provides all the technical details needed for using the P2 Eval HUB75 Adapter Board with any P2 development system.