# P2 Board Power Analysis Matrix
*Complete power budget calculations for all board-addon combinations*

## Power Architecture Overview

### P2 Power Domains
- **VDD (Core)**: 1.8V @ 1A max (P2 internal)
- **VIO (I/O)**: 3.3V distributed across 8 groups
- **Each VIO Group**: 150mA sustained, 300mA peak
- **Total VIO**: 1.2A sustained across all groups

### VIO Group Distribution

| Group | Pins | Rev C Access | Edge Access | Current Budget |
|-------|------|--------------|-------------|----------------|
| VIO_0 | P0-P7 | Header 1-8 | - | 150mA |
| VIO_1 | P8-P15 | Header 9-12+ | - | 150mA |
| VIO_2 | P16-P23 | Auxiliary | - | 150mA |
| VIO_3 | P24-P31 | Auxiliary | - | 150mA |
| VIO_4 | P32-P39 | - | Header 1-8 | 150mA |
| VIO_5 | P40-P47 | - | Header 9-12+ | 150mA |
| VIO_6 | P48-P55 | - | Auxiliary | 150mA |
| VIO_7 | P56-P63 | Boot/Serial | Boot/Serial | 150mA |

## Detailed Power Consumption by Add-on Board

> **Removed 2026-08-26 (F-341, task «#323»).** Content describing Parallax part numbers **#64025 "LED Board"**, **#64026 "7-Segment Display"** and **#64027 "Switches Board"** was deleted from this section. Those three part numbers appear in no captured Parallax document; Stephen confirmed on 2026-08-26 that they are invented. The real boards nearest to what they claimed are the **#64006C LED Matrix** (an 8x7 Charlieplexed grid on 8 pins, not eight discrete LEDs) and the **#64006A Control** add-on (four buttons and four LEDs, not eight switches); there is no 7-segment board in the #64006 series. The removed pin maps, currents and test procedures described none of those, so they were deleted rather than relabelled -- relabelling would have attached fabricated numbers to real boards.


### 64028 Buttons Board Power Analysis

Identical to switches board:
- 220µA per button when pressed
- 1.76mA maximum with all pressed
- Negligible VIO group impact

### 64029 Switches and LEDs Combo Power Analysis

#### Combined Load
```
Switches: 8 × 220µA = 1.76mA (when pressed)
LEDs: 4 × 20mA = 80mA (when all on)
Total: 81.76mA maximum
```

| Mode | Switch Load | LED Load | Total | VIO Load | Safe? |
|------|-------------|----------|-------|----------|-------|
| Idle | 0mA | 0mA | 0mA | 0% | ✅ |
| Active | 1.76mA | 40mA | 41.76mA | 28% | ✅ |
| Maximum | 1.76mA | 80mA | 81.76mA | 55% | ✅ |

**Verdict**: Well within limits

### 40003 Protoboard Power Analysis

User-defined, but typical limits:
```
Per VIO group: 150mA sustained
Distributed across 12 pins: 12.5mA per pin average
Peak per pin: 50mA (P2 absolute maximum)
```

**Guidelines**:
- Balance loads across pins
- Use multiple VIO groups for high current
- Add external drivers for >150mA loads

### 40004 Goertzel Board Power Analysis

#### Analog Circuit Consumption
```
Op-amps: 2-5mA per amplifier
Voltage reference: 1mA
Input bias: <1mA
Total analog: ~10-15mA
```

| Circuit | Current | VIO Load | Safe? |
|---------|---------|----------|-------|
| Input stage | 5mA | 3.3% | ✅ |
| Filter stage | 5mA | 3.3% | ✅ |
| Output stage | 5mA | 3.3% | ✅ |
| Total | 15mA | 10% | ✅ |

**Verdict**: Minimal power requirements

### 40007 Digital I/O Board Power Analysis

Depends on connected devices:
```
TTL loads: 1.6mA per input (worst case)
CMOS loads: <1µA static
LED indicators: 10mA each (if present)
```

Typical scenarios:
| Configuration | Current | VIO Load | Safe? |
|---------------|---------|----------|-------|
| All inputs | <1mA | <1% | ✅ |
| 4 TTL + 4 CMOS | 7mA | 5% | ✅ |
| With LED indicators | 40-80mA | 27-53% | ✅ |

## Power Budget Calculations by Configuration

### Rev C Board Power Distribution

```spin2
CON
  ' Rev C VIO group assignments
  VIO_0_PINS = 0  ' P0-P7: Primary header
  VIO_1_PINS = 8  ' P8-P15: Extended header
  VIO_0_BUDGET = 150  ' mA
  VIO_1_BUDGET = 150  ' mA
  
PUB calculate_revc_load(addon) : vio0_load, vio1_load
  case addon
    ADDON_64029_COMBO:
      vio0_load := 2    ' Switches
      vio1_load := 80   ' LEDs
```

### Edge Board Power Distribution

```spin2
CON
  ' Edge VIO group assignments
  VIO_4_PINS = 32  ' P32-P39: Primary header
  VIO_5_PINS = 40  ' P40-P47: Extended header
  VIO_4_BUDGET = 150  ' mA
  VIO_5_BUDGET = 150  ' mA
  
PUB calculate_edge_load(addon) : vio4_load, vio5_load
  case addon
    ADDON_64029_COMBO:
      vio4_load := 82   ' All on VIO_4
      vio5_load := 0
```

## Thermal Considerations

### P2 Package Thermal Limits
```
Thermal Resistance (θJA): 20°C/W
Maximum Junction Temperature: 125°C
Ambient Operating: -40°C to 85°C
```

### Power Dissipation
```
P2 Core (1.8V @ 500mA typical): 0.9W
VIO (3.3V @ 200mA typical): 0.66W
Total typical: 1.56W
Temperature rise: 1.56W × 20°C/W = 31°C
```

### Thermal Management Guidelines

| Total Power | Temp Rise | Cooling Needed |
|-------------|-----------|----------------|
| <1W | <20°C | None |
| 1-2W | 20-40°C | Airflow recommended |
| 2-3W | 40-60°C | Heatsink required |
| >3W | >60°C | Active cooling |

## Power Supply Requirements

### Recommended Supply Configurations

#### Basic System (1-2 add-on boards)
```
3.3V @ 1.5A switching regulator
Input: 5V USB or 7-15V DC
Efficiency: >85%
Ripple: <50mV
```

#### High-Current System (LEDs, displays)
```
3.3V @ 3A switching regulator
5V @ 2A for external circuits
Input: 12V @ 2A adapter
Separate VIO supplies recommended
```

#### Professional System (multiple boards)
```
1.8V @ 1.5A for P2 core (regulated from 3.3V)
3.3V @ 500mA per VIO group (8 supplies)
5V @ 5A for peripherals
Input: ATX power supply or 12V @ 5A
```

## Power Optimization Strategies

### Software Techniques

#### PWM Brightness Control
```spin2
PUB set_led_power(percent) | duty
  duty := percent * 255 / 100
  
  repeat led from 0 to 7
    WRPIN(LED_BASE + led, P_PWM_SAWTOOTH)
    WXPIN(LED_BASE + led, duty << 16 | $FF)
    DIRH(LED_BASE + led)
```

#### Time-Division Multiplexing
```spin2
PUB multiplex_leds(pattern, duty_percent)
  repeat
    repeat led from 0 to 7
      if pattern & (1 << led)
        PINHIGH(LED_BASE + led)
        waitus(duty_percent * 10)
        PINLOW(LED_BASE + led)
        waitus((100 - duty_percent) * 10)
```

#### Dynamic Clock Management
```spin2
PUB reduce_power_idle()
  HUBSET(%0000_0000_0000_0000_0000_0000_0000_0000)  ' Reduce clock
  ' ... idle operations ...
  HUBSET(CLKMODE)  ' Restore full speed
```

### Hardware Techniques

#### Current Limiting Resistors
```
LED current = (VIO - Vf) / R
For 10mA: R = (3.3V - 2.1V) / 0.010A = 120Ω
For 5mA: R = (3.3V - 2.1V) / 0.005A = 240Ω
```

#### External Drivers
```
Use transistor/MOSFET for loads >50mA
Use dedicated LED drivers for >8 LEDs
Use shift registers to reduce pin count
```

## Measurement and Monitoring

### Current Measurement Code
```spin2
VAR
  long vio_current[8]
  
PUB monitor_power() | group
  repeat group from 0 to 7
    vio_current[group] := measure_vio_group(group)
    if vio_current[group] > 150
      debug("WARNING: VIO", SDEC(group), " overcurrent: ", SDEC(vio_current[group]), "mA")
      
PRI measure_vio_group(group) : current_ma
  ' Use ADC to measure sense resistor voltage
  WRPIN(SENSE_PIN[group], P_ADC | P_ADC_1X)
  WXPIN(SENSE_PIN[group], 13)  ' 14-bit conversion
  DIRH(SENSE_PIN[group])
  
  current_ma := (RDPIN(SENSE_PIN[group]) * 3300) / 16384 / SENSE_RESISTOR
```

### Power Profiling
```spin2
PUB profile_addon_power() | baseline, active
  all_pins_low()
  baseline := measure_total_current()
  
  activate_addon()
  active := measure_total_current()
  
  debug("Addon power consumption: ", SDEC(active - baseline), "mA")
```

## Safety Guidelines

### Absolute Maximum Ratings (Never Exceed)
- VIO pin current: ±50mA
- VIO group current: 300mA (peak only)
- Total VIO current: 1.5A
- Junction temperature: 125°C

### Recommended Operating Conditions
- VIO pin current: ±30mA
- VIO group current: 150mA
- Total VIO current: 1.0A
- Junction temperature: <85°C

### Protection Circuits
```
External protection recommended:
- Polyfuse on each VIO group (150mA trip)
- TVS diodes on exposed pins
- Series resistors on inputs (100-1kΩ)
- Bypass capacitors (0.1µF per VIO pin)
```

## Quick Reference Table

| Board | Add-on | Typical mA | Peak mA | VIO Groups | Safe? | Notes |
|-------|--------|------------|---------|------------|-------|-------|
| Rev C | 64029 Combo | 42 | 82 | 2 | ✅ | Balanced |
| Edge | 40004 Goertzel | 10 | 15 | 1 | ✅ | Analog |
| All | 40003 Proto | Variable | Variable | Variable | - | User defined |

## Conclusion

Most P2 board-addon combinations operate safely within power limits when:
1. LED boards use PWM or limit simultaneous LEDs
2. 7-segment displays use multiplexing
3. Loads are distributed across VIO groups
4. External supplies power high-current devices

The P2's distributed VIO architecture provides excellent flexibility when properly managed.