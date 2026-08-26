# P2 Hardware Validation Checklist
*Comprehensive testing procedures for board-addon combinations*

## Pre-Connection Validation

### Visual Inspection Checklist
- [ ] **Board Inspection**
  - [ ] No visible damage to PCB
  - [ ] All components properly soldered
  - [ ] No solder bridges between pins
  - [ ] Headers firmly attached
  - [ ] No bent pins in headers
  - [ ] Voltage jumpers in correct position (3.3V)
  
- [ ] **Add-on Board Inspection**
  - [ ] Components facing correct direction
  - [ ] Pin 1 marker clearly visible
  - [ ] No missing components
  - [ ] LEDs/displays not damaged
  - [ ] Switches/buttons move freely

### Electrical Pre-Check
```spin2
PUB pre_connection_test() | pin
  ' Test for shorts before connecting addon
  repeat pin from 0 to 11
    FLTL(TEST_BASE + pin)  ' Float pin
    WRPIN(TEST_BASE + pin, P_HIGH_15K)  ' Weak pull-up
    waitms(1)
    if INA[TEST_BASE + pin] == 0
      debug("WARNING: Pin ", SDEC(TEST_BASE + pin), " may be shorted!")
      return FALSE
  return TRUE
```

## Connection Protocol

### Safe Connection Sequence
1. **Power OFF State**
   - [ ] P2 board powered down
   - [ ] Add-on board not connected
   - [ ] Power supply disconnected
   
2. **Alignment Check**
   - [ ] Pin 1 on add-on aligns with Pin 1 on header
   - [ ] Board orientation matches documentation
   - [ ] All pins will seat properly
   
3. **Physical Connection**
   - [ ] Gently align pins with header
   - [ ] Press straight down (no angle)
   - [ ] Verify full seating (no gap)
   - [ ] Check adjacent components not touching

4. **Pre-Power Verification**
   - [ ] Visual check of connection
   - [ ] No pins bent under board
   - [ ] Board sits level
   - [ ] Nothing touching that shouldn't

## Power-On Testing

### Initial Power Test
```spin2
CON
  POWER_TEST_DELAY = 100  ' ms between tests
  
PUB power_on_sequence() | voltage
  debug("Starting power-on sequence...")
  
  ' Step 1: Apply power with current monitoring
  enable_power_with_limit(100)  ' 100mA limit initially
  waitms(POWER_TEST_DELAY)
  
  ' Step 2: Check for overcurrent
  if check_overcurrent()
    debug("FAULT: Overcurrent detected!")
    disable_power()
    return FALSE
    
  ' Step 3: Verify voltage levels
  voltage := measure_vio_voltage()
  if voltage < 3.0 OR voltage > 3.6
    debug("FAULT: VIO out of range: ", FDEC(voltage), "V")
    disable_power()
    return FALSE
    
  ' Step 4: Increase current limit
  enable_power_with_limit(500)  ' Normal operation
  debug("Power-on successful")
  return TRUE
```

### Current Consumption Verification
- [ ] Measure baseline current (no add-on)
- [ ] Connect add-on and measure idle current
- [ ] Compare to expected values from power matrix
- [ ] Check for unusual heating

## Functional Testing by Add-on Type

> **Removed 2026-08-26 (F-341, task «#323»).** Content describing Parallax part numbers **#64025 "LED Board"**, **#64026 "7-Segment Display"** and **#64027 "Switches Board"** was deleted from this section. Those three part numbers appear in no captured Parallax document; Stephen confirmed on 2026-08-26 that they are invented. The real boards nearest to what they claimed are the **#64006C LED Matrix** (an 8x7 Charlieplexed grid on 8 pins, not eight discrete LEDs) and the **#64006A Control** add-on (four buttons and four LEDs, not eight switches); there is no 7-segment board in the #64006 series. The removed pin maps, currents and test procedures described none of those, so they were deleted rather than relabelled -- relabelling would have attached fabricated numbers to real boards.


### 64028 Buttons Board Validation

#### Test 1: Debounce Test
```spin2
PUB test_button_debounce() | button, bounces
  debug("Testing button debounce...")
  
  repeat button from 0 to 7
    bounces := count_bounces(BTN_BASE + button)
    debug("Button ", SDEC(button), ": ", SDEC(bounces), " bounces")
    
PRI count_bounces(pin) : count | state, last, samples
  debug("Press and release button ", SDEC(pin - BTN_BASE))
  
  ' Wait for press
  repeat while INA[pin] == 1
  
  ' Count transitions during press/release
  last := 0
  samples := 0
  
  repeat while samples < 1000  ' Sample for 100ms
    state := INA[pin]
    if state <> last
      count++
      last := state
    waitus(100)
    samples++
```

### 64029 Combo Board Validation

#### Test 1: Switch-LED Interaction
```spin2
PUB test_combo_interaction()
  debug("Testing switch-LED interaction...")
  
  ' Mirror switches to LEDs
  repeat 100
    OUTH[LED_BASE ADDPINS 3] := INA[SW_BASE ADDPINS 3] ^ $F
    waitms(50)
    
  debug("Test complete - check all switches controlled LEDs")
```

### 40004 Goertzel Board Validation

#### Test 1: Analog Input Test
```spin2
PUB test_analog_input() | samples[256], i, avg
  debug("Testing analog input...")
  
  ' Configure ADC
  WRPIN(ANALOG_PIN, P_ADC | P_ADC_1X)
  WXPIN(ANALOG_PIN, 13)  ' 14-bit
  DIRH(ANALOG_PIN)
  
  ' Collect samples
  repeat i from 0 to 255
    samples[i] := RDPIN(ANALOG_PIN) SAR 18
    waitus(125)  ' 8kHz
    
  ' Calculate statistics
  avg := 0
  repeat i from 0 to 255
    avg += samples[i]
  avg /= 256
  
  debug("Average ADC value: ", SDEC(avg))
  debug("Should be near 8192 for mid-scale")
```

## Communication Testing

### I2C Communication Test
```spin2
PUB test_i2c_bus() | device_count
  debug("Scanning I2C bus...")
  
  device_count := 0
  
  repeat addr from $08 to $77
    if i2c_ping(addr)
      debug("Device found at $", HEX(addr))
      device_count++
      
  debug("Found ", SDEC(device_count), " I2C devices")
```

### SPI Communication Test
```spin2
PUB test_spi_loopback() | sent, received
  debug("Testing SPI loopback...")
  
  ' Configure SPI pins (MOSI to MISO externally)
  setup_spi_pins()
  
  repeat sent from 0 to 255
    received := spi_transfer(sent)
    if received <> sent
      debug("ERROR: Sent $", HEX(sent), " got $", HEX(received))
      return FALSE
      
  debug("SPI loopback test PASSED")
  return TRUE
```

## Performance Testing

### Maximum Toggle Rate Test
```spin2
PUB test_max_toggle_rate() | pin, toggles
  debug("Testing maximum toggle rate...")
  
  pin := TEST_BASE
  DIRL(pin)
  
  toggles := 0
  repeat 1_000_000
    OUTH(pin)
    OUTL(pin)
    toggles += 2
    
  debug("Achieved ", SDEC(toggles/2), " Hz toggle rate")
```

### Streamer Performance Test
```spin2
PUB test_streamer_output() | buffer[64]
  debug("Testing streamer performance...")
  
  ' Fill buffer with test pattern
  repeat i from 0 to 63
    buffer[i] := $AA55AA55
    
  ' Configure streamer
  SETXFRQ($4000_0000)  ' Half clock rate
  SETSTREAMER(X_RFLONG_32, @buffer, TEST_BASE)
  
  waitms(10)  ' Let it run
  
  debug("Streamer test complete - check with scope")
```

## Stress Testing

### Thermal Stress Test
```spin2
PUB thermal_stress_test() | temp_start, temp_end
  debug("Running thermal stress test...")
  
  temp_start := read_temperature()
  
  ' Run high-current load for 5 minutes
  OUTH(LED_BASE ADDPINS 7) := $FF  ' All LEDs on
  
  repeat 300  ' 5 minutes
    debug("Time: ", SDEC(_/60), ":", SDEC(_ // 60))
    waitms(1000)
    
  temp_end := read_temperature()
  
  OUTL(LED_BASE ADDPINS 7)  ' LEDs off
  
  debug("Temperature rise: ", SDEC(temp_end - temp_start), "°C")
```

### Continuous Operation Test
```spin2
PUB endurance_test() | hours, errors
  debug("Starting 24-hour endurance test...")
  
  errors := 0
  
  repeat hours from 1 to 24
    ' Run all tests
    if !test_all_functions()
      errors++
      
    debug("Hour ", SDEC(hours), ": ", SDEC(errors), " errors")
    waitms(3_600_000)  ' 1 hour
    
  debug("Endurance test complete: ", SDEC(errors), " total errors")
```

## Troubleshooting Procedures

### No Response from Add-on
1. [ ] Check power (measure VIO at header)
2. [ ] Verify pin mapping matches code
3. [ ] Test continuity from header to component
4. [ ] Check for solder bridges
5. [ ] Try different P2 pins
6. [ ] Test add-on on different P2 board

### Intermittent Operation
1. [ ] Check header connection (reseat)
2. [ ] Measure supply voltage under load
3. [ ] Look for thermal issues
4. [ ] Add bypass capacitors
5. [ ] Reduce clock speed
6. [ ] Check for ground loops

### Excessive Current Draw
1. [ ] Disconnect add-on immediately
2. [ ] Check for shorts with multimeter
3. [ ] Verify component orientation
4. [ ] Test each section individually
5. [ ] Check for damaged components
6. [ ] Verify current limiting resistors

## Test Result Documentation

### Test Report Template
```
Date: ___________
Tester: ___________
Board: P2 _________ Rev ___
Add-on: _________ SKU _____

Visual Inspection: [ ] PASS [ ] FAIL
Connection Test: [ ] PASS [ ] FAIL
Power-On Test: [ ] PASS [ ] FAIL
Functional Test: [ ] PASS [ ] FAIL
Communication Test: [ ] PASS [ ] FAIL
Performance Test: [ ] PASS [ ] FAIL
Stress Test: [ ] PASS [ ] FAIL

Notes:
_________________________
_________________________
_________________________

Signature: _______________
```

## Automated Test Suite

### Complete Validation Script
```spin2
PUB run_complete_validation() : pass_count, fail_count | test_num
  debug("Starting automated validation suite...")
  
  test_list := @[
    @pre_connection_test,
    @power_on_sequence,
    @test_individual_leds,
    @test_led_patterns,
    @test_segments,
    @test_digit_multiplex,
    @test_switch_pullups,
    @test_switch_interactive,
    @test_button_debounce,
    @test_combo_interaction,
    @test_analog_input,
    @test_i2c_bus,
    @test_spi_loopback,
    @test_max_toggle_rate,
    @test_streamer_output
  ]
  
  repeat test_num from 0 to 14
    debug("Running test ", SDEC(test_num + 1), " of 15...")
    
    if call_test(test_list[test_num])
      pass_count++
      debug("  PASSED")
    else
      fail_count++
      debug("  FAILED")
      
  debug("Validation complete: ", SDEC(pass_count), " passed, ", SDEC(fail_count), " failed")
  
  return pass_count == 15  ' TRUE if all passed
```

## Safety Protocols

### Emergency Procedures
1. **Smoke/Smell**: Immediately disconnect power
2. **Overcurrent**: Power down, check for shorts
3. **Overheating**: Allow cooldown, check ventilation
4. **No Response**: Safe mode recovery procedure
5. **Damaged Board**: Document and quarantine

### Required Equipment
- [ ] Digital multimeter
- [ ] Current meter (or current sensing)
- [ ] Oscilloscope (optional but recommended)
- [ ] Anti-static wrist strap
- [ ] Good lighting and magnification
- [ ] Appropriate power supply with current limiting
- [ ] Test leads and probes
- [ ] Documentation and schematics

This comprehensive validation checklist ensures thorough testing of all P2 board-addon combinations for reliable operation.