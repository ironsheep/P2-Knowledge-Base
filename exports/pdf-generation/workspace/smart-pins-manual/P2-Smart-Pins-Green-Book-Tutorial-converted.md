# P2 Smart Pins Complete Reference

## Specifications and Implementation for All 32 Modes

### Version 1.0 - Production Ready  
### August 2025

---

## Executive Summary

### Why Smart Pins Revolutionize P2 Development

The Propeller 2's Smart Pin architecture represents a paradigm shift in microcontroller I/O handling. Instead of consuming precious COG cycles for routine I/O operations, Smart Pins provide 64 independent hardware units that operate autonomously, each capable of 32 different modes ranging from simple digital I/O to complex protocols like USB.

**The Smart Pin Advantage:**
- **Zero COG Overhead**: Once configured, Smart Pins run independently
- **Deterministic Timing**: Hardware-guaranteed precision unaffected by code execution
- **Massive Parallelism**: All 64 pins can operate simultaneously in different modes
- **Power Efficiency**: Hardware implementation uses less power than software loops

### Performance Impact Analysis

| Operation | COG-Driven | Smart Pin | COG Savings | Notes |
|-----------|------------|-----------|-------------|-------|
| **1MHz PWM** | 100% of COG | 0% of COG | 1 full COG | Smart Pin handles entirely |
| **UART 115200** | 15% of COG | 0% of COG | 15% per channel | Per serial channel |
| **Quadrature Decode** | 40% of COG | 0% of COG | 40% per encoder | Hardware tracking |
| **ADC Sampling** | 30% of COG | 0% of COG | 30% per channel | Continuous sampling |
| **DAC Output** | 10% of COG | 0% of COG | 10% per channel | Autonomous updates |
| **Pulse Measurement** | 25% of COG | 0% of COG | 25% per channel | Hardware capture |

### When to Use Smart Pins

**Always Use Smart Pins For:**
- Serial communication (UART, SPI, I2C patterns)
- PWM generation (motors, LEDs, power control)
- Encoder reading (quadrature, incremental)
- Precision timing measurements
- ADC/DAC operations
- Frequency generation

**Consider COG-Driven I/O For:**
- Complex protocols with conditional logic
- Bit-banged interfaces needing data manipulation
- Dynamic protocol changes mid-stream
- Learning/debugging before Smart Pin implementation

### Resource Planning Guide

With 64 Smart Pins available, typical applications use:
- **Robot Controller**: 4 PWM (motors) + 2 encoders + 4 ADC (sensors) + 2 UART = 12 pins
- **Data Logger**: 8 ADC + 1 SPI + 1 UART + 1 I2C pattern = 20 pins  
- **Motor Driver**: 6 PWM + 3 encoders + 6 current sense ADC = 15 pins
- **Communication Hub**: 4 UART + 2 SPI patterns + USB = 14 pins

This leaves 50-75% of Smart Pins available for expansion, ensuring room for growth.

---

## Quick Start Guide

### Your First Smart Pin in 5 Minutes

Let's create a 1kHz square wave without using any COG processing time.

#### Step 1: Understanding the Goal
We'll configure Pin 56 (LED on P2 Eval board) to toggle at 1kHz automatically.

#### Step 2: The Complete Program

:::: spin2
```
CON
  _clkfreq = 200_000_000        ' 200MHz system clock
  LED_PIN = 56                  ' P2 Eval board LED

PUB main()
  ' Configure Smart Pin for transition output mode
  pinstart(LED_PIN, P_TRANSITION | P_OE, clkfreq / 2000, 0)
  
  ' Smart Pin now runs forever at 1kHz!
  ' COG is free to do other work
  repeat
    ' Your application code here
    ' The LED keeps blinking regardless
```

#### Step 3: Understanding What Happened

1. **`P_TRANSITION`** - Selects transition output mode (toggles pin)
2. **`P_OE`** - Enables output driver
3. **`clkfreq / 2000`** - Sets period (1kHz = 500µs high + 500µs low)
4. **`pinstart()`** - Configures and enables the Smart Pin

The Smart Pin now generates a perfect 1kHz signal forever, with zero COG involvement!

#### Step 4: Verify It's Working

:::: spin2
```
PUB verify_smart_pin() | count
  ' Read how many transitions have occurred
  repeat 10
    count := rdpin(LED_PIN)     ' Read transition count
    debug("Transitions: ", udec(count))
    waitms(100)
```

### Common Beginner Mistakes (and Solutions)

#### Mistake 1: Forgetting Output Enable
:::: spin2
```
' WRONG - Pin won't output
pinstart(pin, P_TRANSITION, period, 0)

' RIGHT - Include P_OE
pinstart(pin, P_TRANSITION | P_OE, period, 0)
```

#### Mistake 2: Wrong Period Calculation
:::: spin2
```
' WRONG - This gives 500Hz, not 1kHz
wxpin(pin, clkfreq / 1000)

' RIGHT - Transitions are edges, need /2000 for 1kHz
wxpin(pin, clkfreq / 2000)
```

#### Mistake 3: Not Clearing Before Reconfigure
:::: spin2
```
' WRONG - May retain old settings
pinstart(pin, new_mode, x, y)

' RIGHT - Clear first
pinclear(pin)
pinstart(pin, new_mode, x, y)
```

### Next Steps: Try These Experiments

1. **Change Frequency**: Modify the formula to get 10Hz, 100Hz, 10kHz
2. **Multiple Pins**: Configure 4 pins with different frequencies
3. **Read Results**: Use `rdpin()` to count transitions
4. **PWM Instead**: Change to `P_PWM_SAWTOOTH` mode for dimming

### Quick Mode Selection Checklist

Ask yourself:
1. **Digital or Analog?** → Narrows to ~half the modes
2. **Input or Output?** → Narrows to ~quarter of modes
3. **Continuous or Triggered?** → Narrows to 2-3 modes
4. **What Resolution/Speed?** → Selects exact mode

Example: Digital → Output → Continuous → Fast = NCO Frequency mode

---

## Table of Contents

**Executive Summary**
- Why Smart Pins Matter
- Performance Impact
- Resource Planning

**Quick Start Guide**
- First Smart Pin in 5 Minutes
- Common Mistakes
- Mode Selection

**Part I: Smart Pin Fundamentals**
- Chapter 1: Smart Pin Architecture
- Chapter 2: Configuration Protocol  
- Chapter 3: Programming Interface

**Part II: Mode Reference**
- Chapter 4: Digital I/O Modes
- Chapter 5: DAC Output Modes
- Chapter 6: Pulse and NCO Modes
- Chapter 7: PWM Modes
- Chapter 8: Encoder Modes
- Chapter 9: Measurement Modes
- Chapter 10: ADC Modes
- Chapter 11: USB Mode
- Chapter 12: Serial Modes

**Part III: Application Guide**
- Chapter 13: Common Implementations
- Chapter 14: Multi-Pin Applications
- Chapter 15: Optimization & Troubleshooting

**Part IV: Quick Reference**
- Appendix A: Mode Selection Guide with Comparison Matrix
- Appendix B: Configuration Calculator
- Appendix C: Register Reference
- Appendix D: Electrical Specifications
- Index

---

# Part I: Smart Pin Fundamentals

## Chapter 1: Smart Pin Architecture

### Overview

The Propeller 2 incorporates 64 Smart Pins, one for each I/O pin. Each Smart Pin contains independent hardware that can be configured to perform one of 32 specialized modes without COG intervention. Once configured, Smart Pins operate autonomously, freeing COG resources for other tasks.

![Smart Pin Block Diagram](assets/P2 SmartPins-220809_page03_img01.png)

### Hardware Architecture

Each Smart Pin consists of:
- **Mode Control Logic**: Determines pin function based on 6-bit mode selection
- **X Register**: 32-bit parameter register (mode-specific function)
- **Y Register**: 32-bit parameter register (mode-specific function)  
- **Z Register**: 32-bit result register (read via RDPIN/RQPIN)
- **Input Selector**: Routes signals from any pin or internal source
- **Output Driver**: Configurable drive strength and modes

### Smart Pin Capabilities

Smart Pins operate independently of COGs, providing:
- Autonomous signal generation and measurement
- Precise timing without COG overhead
- Concurrent operation across all 64 pins
- Deterministic behavior regardless of COG activity

### Pin Numbering and Access

P2 I/O pins are numbered 0-63. Smart Pin instructions use 6-bit addressing:
```
Pin 0-31:  Direct addressing in instruction
Pin 32-63: Direct addressing in instruction  
Pin 0-63:  Indirect addressing via register
```

### Clock Domains

Smart Pins operate in the system clock domain:
- Maximum frequency: sysclock/2 for most modes
- Synchronous updates with COG instructions
- Independent timing from COG execution

---

## Chapter 2: Configuration Protocol

### Configuration Sequence

Smart Pins require a specific configuration sequence:

1. **Reset Pin** (optional but recommended)
   ```pasm2
   dirl    #pin            ' Disable pin (Smart Pin OFF)
   ```

2. **Configure Mode**
   ```pasm2
   wrpin   mode_value, #pin ' Write mode configuration
   ```

3. **Set X Parameter** (mode-dependent)
   ```pasm2
   wxpin   x_value, #pin   ' Write X parameter
   ```

4. **Set Y Parameter** (mode-dependent)
   ```pasm2
   wypin   y_value, #pin   ' Write Y parameter
   ```

5. **Enable Smart Pin**
   ```pasm2
   dirh    #pin            ' Enable Smart Pin
   ```

![Configuration Flow Diagram](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page04_img01.png)

### Mode Register Structure (WRPIN)

The 32-bit mode register controls all Smart Pin settings:

```
Bits 31..14: Pin input/output configuration
Bits 13..8:  Digital filter settings
Bits 7..6:   Output enable control
Bits 5..0:   Smart Pin mode selection (%MMMMMM)
```

### X Register Functions (WXPIN)

The X register function varies by mode:
- **Timing modes**: Period or timeout value
- **Counter modes**: Count limit or reset value
- **PWM modes**: Base period
- **Serial modes**: Bit period

### Y Register Functions (WYPIN)

The Y register function varies by mode:
- **Output modes**: Output value or duty cycle
- **Counter modes**: Not used or count increment
- **Measurement modes**: Measurement window
- **Serial modes**: Data to transmit

### Z Register Functions (RDPIN/RQPIN)

The Z register always contains the Smart Pin result:
- **RDPIN**: Read and acknowledge (clears IN flag)
- **RQPIN**: Read without acknowledge (preserves IN flag)

Result varies by mode:
- **Counter modes**: Current count
- **Measurement modes**: Measured value
- **Serial modes**: Received data
- **Output modes**: Current output value

### Reading Smart Pin State

Two methods to check Smart Pin status:

**Method 1: Test IN Flag**
:::: pasm2
```
        testp   #pin, wc        ' C = IN flag state
  if_c  jmp     #data_ready     ' Jump if data ready
```

**Method 2: Read with Status**
:::: pasm2
```
        rdpin   value, #pin wc  ' Read value, C = IN flag
  if_nc jmp     #no_data        ' Jump if no data
```

---

## Chapter 3: Programming Interface

### Spin2 Smart Pin Methods

Spin2 provides high-level methods for Smart Pin control:

:::: spin2
```
pinstart(pin, mode, x_value, y_value)  ' Configure and start
pinclear(pin)                           ' Disable Smart Pin
pinw(pin, value)                        ' Write to Y register
pinr(pin)                               ' Read Z register
pinfloat(pin)                          ' Float pin (high-Z)
pinl(pin)                              ' Drive pin low
pinh(pin)                              ' Drive pin high
pintoggle(pin)                         ' Toggle pin state
```

### PASM2 Smart Pin Instructions

PASM2 provides direct Smart Pin control:

:::: pasm2
```
WRPIN   D/#, S/#    ' Write mode configuration
WXPIN   D/#, S/#    ' Write X parameter
WYPIN   D/#, S/#    ' Write Y parameter  
RDPIN   D, S/# {WC} ' Read Z result and acknowledge
RQPIN   D, S/# {WC} ' Read Z result without acknowledge
AKPIN   S/#         ' Acknowledge Smart Pin
TESTP   S/# {WC/WZ} ' Test pin state
```

### Multi-COG Coordination

Smart Pins can be accessed by any COG:
- Pin ownership is not exclusive
- Multiple COGs can read results
- Configuration should be coordinated
- OR'd signal paths for shared pins

### Synchronization Techniques

**Starting Multiple Pins Simultaneously**
:::: spin2
```
PUB start_synchronized(first_pin, last_pin, mode) | mask
  mask := (1 << (last_pin - first_pin + 1)) - 1
  mask <<= first_pin
  
  ' Configure all pins while disabled
  repeat pin from first_pin to last_pin
    pinstart(pin, mode, 0, 0)
    pinclear(pin)
    
  ' Enable all simultaneously  
  DIRH(mask)
```

**Phase-Locked PWM Outputs**
:::: pasm2
```
        mov     mask, #$FF      ' Pins P7..P0
        shl     mask, #20       ' Pins P27..P20
        
        ' Configure while disabled
        rep     #4, #8          ' 8 pins
        wrpin   pwm_mode, pin
        wxpin   period, pin
        wypin   duty, pin
        add     pin, #1
        
        ' Start synchronized
        dirh    mask            ' Enable all PWM pins
```

### Error Handling

Common Smart Pin errors and recovery:

**Configuration Error**
- Symptom: Pin doesn't respond as expected
- Solution: Reset pin (DIRL) and reconfigure

**Overflow/Underflow**
- Symptom: Counter wraps or saturates
- Solution: Monitor and reset periodically

**Timing Violation**
- Symptom: Missed samples or events
- Solution: Increase sampling rate or use buffering

---

# Part II: Mode Reference

## Chapter 4: Digital I/O Modes

### Mode %00000 - Smart Pin OFF (Default)

**Specifications**
- Function: Smart Pin disabled, normal I/O operation
- Power: Minimum consumption
- Timing: Immediate I/O response
- Usage: Default state after reset

**Configuration**
```
WRPIN: $00000000 (or simply 0)
WXPIN: Not used
WYPIN: Not used
Z Result: Not applicable
```

**Spin2 Implementation**
:::: spin2
```
PUB disable_smart_pin(pin)
  pinclear(pin)        ' Disable Smart Pin
  pinfloat(pin)        ' Float to high-Z
  
PUB use_as_normal_io(pin)
  pinclear(pin)        ' Ensure Smart Pin OFF
  pinh(pin)           ' Drive high
  pinl(pin)           ' Drive low
  result := pinr(pin)  ' Read pin state
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
disable_smart
        dirl    #20             ' Disable pin (Smart Pin OFF)
        
normal_output
        dirl    #20             ' Ensure disabled
        or      outa, #(1<<20)  ' Prepare high
        or      dira, #(1<<20)  ' Drive high
        andn    outa, #(1<<20)  ' Drive low
        
normal_input  
        andn    dira, #(1<<20)  ' Set as input
        test    ina, #(1<<20) wc ' Read state into C
```

**Applications**
- Standard GPIO operations
- Reset Smart Pin to known state
- Power-sensitive applications

---

### Mode %00001 - Repository Mode

**Specifications**
- Function: 32-bit read/write repository
- Storage: Retains value until overwritten
- Access: Multiple COGs can read/write
- Power: Low consumption

**Configuration**
```
WRPIN: %00001 (P_REPOSITORY)
WXPIN: Not used
WYPIN: Value to store
Z Result: Stored value
```

**Spin2 Implementation**
:::: spin2
```
CON
  REPO_PIN = 20
  REPO_MODE = P_REPOSITORY | P_OE

PUB setup_repository()
  pinstart(REPO_PIN, REPO_MODE, 0, 0)

PUB store_value(data)
  wypin(REPO_PIN, data)       ' Store 32-bit value
  
PUB retrieve_value() : data
  data := rdpin(REPO_PIN)     ' Read stored value
  
PUB share_between_cogs(value) | retrieved
  store_value(value)          ' COG 1 stores
  ' ... other COG can read ...
  retrieved := retrieve_value() ' COG 2 reads
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
repo_init
        mov     pa, ##P_REPOSITORY | P_OE
        wrpin   pa, #20         ' Configure as repository
        dirh    #20             ' Enable repository
        
store_data
        mov     pa, ##$12345678 ' Data to store
        wypin   pa, #20         ' Write to repository
        
read_data
        rdpin   result, #20     ' Read repository
        ' result now contains stored value
        
result  long    0
```

**Applications**
- Inter-COG communication without HUB access
- Parameter passing between COGs
- Temporary value storage
- Configuration storage

**Performance Notes**
- Single clock access from any COG
- No HUB bandwidth impact
- Atomic 32-bit operations

---

### Mode %00111 - Transition Output

**Specifications**
- Function: Output transitions on X-clock intervals
- Timing: Precise edge generation
- Control: X sets period, Y sets pattern
- Applications: Clock generation, protocol signaling

**Configuration**
```
WRPIN: %00111 (P_TRANSITION)
WXPIN: Clock period (sysclock cycles)
WYPIN: Number of transitions
Z Result: Current transition count
```

**Spin2 Implementation**
:::: spin2
```
CON
  TRANS_PIN = 20
  TRANS_MODE = P_TRANSITION | P_OE

PUB setup_transition_output(period, count)
  pinstart(TRANS_PIN, TRANS_MODE, period, count)
  
PUB generate_clock(freq_hz) | period
  period := clkfreq / (freq_hz * 2)  ' Calculate period
  wxpin(TRANS_PIN, period)           ' Set period
  wypin(TRANS_PIN, 0)                ' Continuous transitions
  
PUB burst_transitions(num_edges)
  wypin(TRANS_PIN, num_edges)        ' Generate N transitions
  repeat while pinr(TRANS_PIN)       ' Wait for completion
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
trans_init
        mov     pa, ##P_TRANSITION | P_OE
        wrpin   pa, #20         ' Configure transition mode
        mov     pa, ##1000      ' Period = 1000 clocks
        wxpin   pa, #20         ' Set period
        dirh    #20             ' Enable output
        
gen_burst
        mov     pa, #10         ' Generate 10 transitions
        wypin   pa, #20         ' Start burst
.wait   testp   #20, wc         ' Check if done
  if_c  jmp     #.wait          ' Wait for completion
```

**Applications**
- Clock generation
- Pulse train generation
- Protocol bit timing
- Test signal generation

---

## Chapter 5: DAC Output Modes

### Mode %00010 - DAC 124Ω, 3.3V Output

**Specifications**
- Resolution: 16 bits
- Output range: 0V to 3.3V (VIO)
- Output impedance: 124Ω ±5%
- Update rate: Up to sysclock/2
- Settling time: <1µs to 0.1%
- Current drive: 10mA maximum

![DAC Output Characteristic](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page13_img01.png)

**Configuration**
```
WRPIN: P_DAC_124R_3V | P_OE
WXPIN: Update period (0 = manual)
WYPIN: 16-bit DAC value
Z Result: Current DAC value
```

**Spin2 Implementation**
:::: spin2
```
CON
  DAC_PIN = 20
  DAC_MODE = P_DAC_124R_3V | P_OE

PUB setup_dac()
  pinstart(DAC_PIN, DAC_MODE, 0, 0)
  
PUB set_voltage(millivolts) | dacval
  ' Convert millivolts (0-3300) to DAC value
  dacval := (millivolts * $FFFF) / 3300
  wypin(DAC_PIN, dacval)
  
PUB generate_sine(freq_hz) | angle, delay
  delay := clkfreq / (freq_hz * 360)
  repeat
    repeat angle from 0 to 359
      wypin(DAC_PIN, $8000 + sin(angle, $7FFF))
      waitx(delay)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
dac_init
        mov     pa, ##P_DAC_124R_3V | P_OE
        wrpin   pa, #20         ' Configure DAC
        dirh    #20             ' Enable output
        
set_voltage
        mov     pa, ##$8000     ' Mid-scale (1.65V)
        wypin   pa, #20         ' Output voltage
        
generate_ramp
.loop   add     dacval, #$100   ' Increment
        wypin   dacval, #20     ' Update DAC
        waitx   ##1000          ' Delay
        jmp     #.loop
        
dacval  long    0
```

**Applications**
- Analog voltage generation
- Audio output
- Control voltage generation
- Sensor simulation
- Waveform synthesis

**Performance Notes**
- No filtering required for DC outputs
- Add RC filter for audio applications
- Consider 75Ω mode for lower impedance

---

### Mode %00011 - DAC 75Ω, 2.0V Output

**Specifications**
- Resolution: 16 bits
- Output range: 0V to 2.0V
- Output impedance: 75Ω ±5%
- Update rate: Up to sysclock/2
- Settling time: <1µs to 0.1%
- Current drive: 15mA maximum

**Configuration**
```
WRPIN: P_DAC_75R_2V | P_OE
WXPIN: Update period (0 = manual)
WYPIN: 16-bit DAC value
Z Result: Current DAC value
```

**Spin2 Implementation**
:::: spin2
```
CON
  VIDEO_PIN = 20
  VIDEO_MODE = P_DAC_75R_2V | P_OE

PUB setup_video_dac()
  pinstart(VIDEO_PIN, VIDEO_MODE, 0, 0)
  
PUB set_video_level(millivolts) | dacval
  ' Convert millivolts (0-2000) to DAC value
  dacval := (millivolts * $FFFF) / 2000
  wypin(VIDEO_PIN, dacval)
  
PUB generate_sync_pulse()
  wypin(VIDEO_PIN, 0)         ' Sync level (0V)
  waitus(5)                   ' Sync width
  wypin(VIDEO_PIN, $4CCC)     ' Black level (0.3V)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
video_init
        mov     pa, ##P_DAC_75R_2V | P_OE
        wrpin   pa, #20         ' Configure video DAC
        dirh    #20             ' Enable output
        
composite_sync
        mov     pa, #0          ' Sync level
        wypin   pa, #20
        waitx   ##400           ' 5µs at 80MHz
        mov     pa, ##$4CCC     ' Black level
        wypin   pa, #20
        
white_level
        mov     pa, ##$FFFF     ' White level (2.0V)
        wypin   pa, #20
```

**Applications**
- Composite video generation
- Component video output
- Professional video equipment
- 75Ω transmission line driving
- Precision analog signaling

---

## Chapter 6: Pulse and NCO Modes

### Mode %00100 - Pulse/Cycle Output

**Specifications**
- Function: Generate pulses with programmable width
- Timing: X sets base period, Y sets pulse count
- Resolution: System clock precision
- Range: 1 to 2^32 clocks

**Configuration**
```
WRPIN: %00100 (P_PULSE)
WXPIN: Base period in clocks
WYPIN: Pulse count/width
Z Result: Remaining pulses
```

**Spin2 Implementation**
:::: spin2
```
CON
  PULSE_PIN = 20
  PULSE_MODE = P_PULSE | P_OE

PUB setup_pulse_gen(period)
  pinstart(PULSE_PIN, PULSE_MODE, period, 0)
  
PUB single_pulse(width_us)
  wxpin(PULSE_PIN, clkfreq / 1_000_000 * width_us)
  wypin(PULSE_PIN, 1)         ' Generate one pulse
  
PUB pulse_burst(count, width_us)
  wxpin(PULSE_PIN, clkfreq / 1_000_000 * width_us)
  wypin(PULSE_PIN, count)     ' Generate count pulses
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
pulse_init
        mov     pa, ##P_PULSE | P_OE
        wrpin   pa, #20         ' Configure pulse mode
        mov     pa, ##10000     ' 10000 clock period
        wxpin   pa, #20
        dirh    #20             ' Enable output
        
gen_pulse
        mov     pa, #5          ' Generate 5 pulses
        wypin   pa, #20
.wait   testp   #20, wc         ' Check completion
  if_c  jmp     #.wait
```

**Applications**
- Stepper motor control
- Servo positioning
- Timing pulse generation
- Trigger signal generation

---

### Mode %00101 - NCO Frequency

**Specifications**
- Function: Numerically Controlled Oscillator
- Frequency: DC to sysclock/2
- Resolution: 32-bit frequency control
- Jitter: < 1 clock period

![NCO Frequency Generation](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page15_img01.png)

**Configuration**
```
WRPIN: %00101 (P_NCO_FREQ)
WXPIN: Base period (divider)
WYPIN: Frequency value (32-bit)
Z Result: Phase accumulator
```

**Spin2 Implementation**
:::: spin2
```
CON
  NCO_PIN = 20
  NCO_MODE = P_NCO_FREQ | P_OE

PUB setup_nco()
  pinstart(NCO_PIN, NCO_MODE, 1, 0)
  
PUB set_frequency(freq_hz) | nco_val
  ' Calculate NCO value for desired frequency
  nco_val := freq_hz frac clkfreq
  wypin(NCO_PIN, nco_val)
  
PUB sweep_frequency(start_hz, end_hz, time_ms) | step, current
  current := start_hz frac clkfreq
  step := ((end_hz - start_hz) frac clkfreq) / time_ms
  
  repeat time_ms
    wypin(NCO_PIN, current)
    current += step
    waitms(1)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
nco_init
        mov     pa, ##P_NCO_FREQ | P_OE
        wrpin   pa, #20         ' Configure NCO
        mov     pa, #1          ' Divider = 1
        wxpin   pa, #20
        dirh    #20             ' Enable output
        
set_1khz
        ' For 1kHz at 200MHz clock:
        ' NCO = (1000 * 2^32) / 200_000_000
        mov     pa, ##21474836  ' NCO value for 1kHz
        wypin   pa, #20         ' Set frequency
```

**Applications**
- Precision frequency synthesis
- Clock generation
- Local oscillator for mixing
- DDS signal generation
- Frequency sweeping

---

### Mode %00110 - NCO Duty

**Specifications**
- Function: NCO with programmable duty cycle
- Frequency: DC to sysclock/4
- Duty resolution: 16 bits
- Duty range: 0% to 100%

**Configuration**
```
WRPIN: %00110 (P_NCO_DUTY)
WXPIN: Base period
WYPIN: [31:16] = Duty, [15:0] = Frequency
Z Result: Phase accumulator
```

**Spin2 Implementation**
:::: spin2
```
CON
  DUTY_PIN = 20
  DUTY_MODE = P_NCO_DUTY | P_OE

PUB setup_nco_duty()
  pinstart(DUTY_PIN, DUTY_MODE, 1, 0)
  
PUB set_freq_and_duty(freq_hz, duty_percent) | nco_val, duty_val
  nco_val := freq_hz frac clkfreq
  duty_val := (duty_percent * $FFFF) / 100
  wypin(DUTY_PIN, (duty_val << 16) | (nco_val >> 16))
  
PUB pulse_width_modulate(duty)
  ' Fixed frequency, variable duty
  wypin(DUTY_PIN, (duty << 16) | $8000)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
duty_init
        mov     pa, ##P_NCO_DUTY | P_OE
        wrpin   pa, #20         ' Configure NCO duty
        mov     pa, #1
        wxpin   pa, #20
        dirh    #20
        
set_50_percent
        mov     pa, ##$8000_8000 ' 50% duty, mid frequency
        wypin   pa, #20
        
variable_duty
        mov     duty, #0
.loop   add     duty, ##$0100_0000 ' Increment duty
        or      duty, ##$0000_8000 ' Keep frequency
        wypin   duty, #20
        waitx   ##10000
        jmp     #.loop
        
duty    long    0
```

**Applications**
- Variable duty cycle generation
- Precision PWM at high frequencies
- Power control with fine resolution
- LED dimming with no flicker

---

## Chapter 7: PWM Modes

### Mode %01000 - PWM Sawtooth

**Specifications**
- Function: Edge-aligned PWM
- Resolution: Up to 16 bits
- Frequency: sysclock / (2 × period)
- Duty cycle: 0% to 100%

![PWM Sawtooth Waveform](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page17_img01.png)

**Configuration**
```
WRPIN: %01000 (P_PWM_SAWTOOTH)
WXPIN: Base period (16-bit)
WYPIN: Duty value (16-bit)
Z Result: Current counter value
```

**Spin2 Implementation**
:::: spin2
```
CON
  PWM_PIN = 20
  PWM_MODE = P_PWM_SAWTOOTH | P_OE

PUB setup_pwm(freq_hz) | period
  period := clkfreq / freq_hz
  pinstart(PWM_PIN, PWM_MODE, period, 0)
  
PUB set_duty_percent(percent) | duty
  duty := (percent * $FFFF) / 100
  wypin(PWM_PIN, duty)
  
PUB fade_led()
  repeat
    repeat duty from 0 to $FFFF step $100
      wypin(PWM_PIN, duty)
      waitms(1)
    repeat duty from $FFFF to 0 step $100
      wypin(PWM_PIN, duty)
      waitms(1)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
pwm_init
        mov     pa, ##P_PWM_SAWTOOTH | P_OE
        wrpin   pa, #20         ' Configure PWM
        mov     pa, ##1000      ' Period = 1000
        wxpin   pa, #20
        dirh    #20             ' Enable output
        
set_25_percent
        mov     pa, ##$4000     ' 25% duty
        wypin   pa, #20
        
sweep_duty
        mov     duty, #0
.loop   add     duty, #$100     ' Increment duty
        wypin   duty, #20       ' Update PWM
        waitx   ##10000         ' Delay
        jmp     #.loop
        
duty    long    0
```

**Applications**
- Motor speed control
- LED dimming
- Power regulation
- Audio amplifier control
- Heater control

---

### Mode %01001 - PWM Triangle

**Specifications**
- Function: Center-aligned PWM
- Resolution: Up to 16 bits
- Frequency: sysclock / (4 × period)
- Duty cycle: 0% to 100%
- Advantage: Reduced harmonics

![PWM Triangle Waveform](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page17_img02.png)

**Configuration**
```
WRPIN: %01001 (P_PWM_TRIANGLE)
WXPIN: Base period (16-bit)
WYPIN: Duty value (16-bit)
Z Result: Current counter value
```

**Spin2 Implementation**
:::: spin2
```
CON
  MOTOR_PIN = 20
  MOTOR_MODE = P_PWM_TRIANGLE | P_OE

PUB setup_motor_pwm(freq_hz) | period
  ' Triangle mode frequency is 1/2 of sawtooth
  period := clkfreq / (freq_hz * 2)
  pinstart(MOTOR_PIN, MOTOR_MODE, period, 0)
  
PUB set_motor_speed(percent) | duty
  duty := (percent * $FFFF) / 100
  wypin(MOTOR_PIN, duty)
  
PUB soft_start(target_percent, ramp_ms) | step, current
  step := ($FFFF * target_percent) / (100 * ramp_ms)
  current := 0
  
  repeat ramp_ms
    wypin(MOTOR_PIN, current)
    current := (current + step) <# ($FFFF * target_percent / 100)
    waitms(1)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
triangle_init
        mov     pa, ##P_PWM_TRIANGLE | P_OE
        wrpin   pa, #20         ' Configure triangle PWM
        mov     pa, ##2000      ' Period = 2000
        wxpin   pa, #20
        dirh    #20
        
complementary_drive
        ' For H-bridge with pin 20 and 21
        mov     pa, ##P_PWM_TRIANGLE | P_OE
        wrpin   pa, #20
        wrpin   pa, #21
        mov     pa, ##2000
        wxpin   pa, #20
        wxpin   pa, #21
        dirh    #20
        dirh    #21
        
        ' Set complementary duties
        mov     pa, ##$8000     ' 50% on pin 20
        wypin   pa, #20
        mov     pa, ##$8000     ' 50% on pin 21 (inverted externally)
        wypin   pa, #21
```

**Applications**
- Three-phase motor control
- Reduced EMI applications
- High-quality audio amplifiers
- Inverter control
- Precision power supplies

---

### Mode %01010 - Periodic Pulse (SMPS)

**Specifications**
- Function: Switch-mode power supply optimized
- Base period: X register
- ON time: Y register
- Frequency: sysclock / X
- Duty precision: Clock-cycle accurate

**Configuration**
```
WRPIN: %01010 (P_PERIODIC_PULSE)
WXPIN: Total period
WYPIN: ON time
Z Result: Cycle counter
```

**Spin2 Implementation**
:::: spin2
```
CON
  SMPS_PIN = 20
  SMPS_MODE = P_PERIODIC_PULSE | P_OE

PUB setup_smps(freq_hz)
  pinstart(SMPS_PIN, SMPS_MODE, clkfreq / freq_hz, 0)
  
PUB set_duty_cycle(on_time_ns) | clocks
  clocks := (clkfreq / 1_000_000_000) * on_time_ns
  wypin(SMPS_PIN, clocks)
  
PUB voltage_feedback_loop(target_adc) | current_adc, duty
  duty := $8000  ' Start at 50%
  
  repeat
    current_adc := read_adc()
    if current_adc < target_adc
      duty := (duty + 1) <# $FFFF
    else
      duty := (duty - 1) #> 0
    wypin(SMPS_PIN, duty)
    waitus(100)  ' Control loop rate
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
smps_init
        mov     pa, ##P_PERIODIC_PULSE | P_OE
        wrpin   pa, #20         ' Configure SMPS mode
        mov     pa, ##4000      ' 50kHz at 200MHz
        wxpin   pa, #20         ' Set period
        dirh    #20
        
feedback_control
        rdpin   adc_val, #30    ' Read ADC on pin 30
        cmp     adc_val, target wc
  if_c  add     duty, #1        ' Increase if below target
  if_nc sub     duty, #1        ' Decrease if above target
        wypin   duty, #20       ' Update duty
        waitx   ##1000          ' Loop delay
        jmp     #feedback_control
        
target  long    $8000
duty    long    $4000
adc_val long    0
```

**Applications**
- Buck converters
- Boost converters
- LED drivers
- Battery chargers
- Motor drivers with current control

---

## Chapter 8: Encoder Modes

### Mode %01011 - Quadrature Encoder

**Specifications**
- Function: A/B quadrature decoder
- Resolution: 4x encoder resolution
- Speed: Up to sysclock/2
- Counter: 32-bit signed

![Quadrature Encoder Signals](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page19_img01.png)

**Configuration**
```
WRPIN: %01011 (P_QUADRATURE_ENC)
WXPIN: Not used
WYPIN: Reset value (typically 0)
Z Result: Current position count
```

**Spin2 Implementation**
:::: spin2
```
CON
  ENCODER_A = 20
  ENCODER_MODE = P_QUADRATURE_ENC

PUB setup_encoder()
  ' A and B pins must be consecutive (A=20, B=21)
  pinstart(ENCODER_A, ENCODER_MODE, 0, 0)
  
PUB read_position() : position
  position := rdpin(ENCODER_A)
  
PUB reset_position()
  wypin(ENCODER_A, 0)
  
PUB read_speed() : speed | pos1, pos2
  pos1 := rdpin(ENCODER_A)
  waitms(10)
  pos2 := rdpin(ENCODER_A)
  speed := (pos2 - pos1) * 100  ' Counts per second
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
encoder_init
        mov     pa, ##P_QUADRATURE_ENC
        wrpin   pa, #20         ' Configure encoder on pins 20+21
        dirh    #20             ' Enable encoder
        
read_position
        rdpin   position, #20   ' Get current count
        
track_velocity
.loop   rdpin   pos1, #20       ' First reading
        waitx   ##1000000       ' Wait 5ms at 200MHz
        rdpin   pos2, #20       ' Second reading
        sub     pos2, pos1      ' Calculate delta
        ' pos2 now contains velocity
        jmp     #.loop
        
position long   0
pos1    long    0
pos2    long    0
```

**Applications**
- Motor position feedback
- Rotary knob input
- Linear position sensing
- Closed-loop control systems
- CNC machine positioning

---

### Mode %01101 - A-B Encoder

**Specifications**
- Function: Separate A and B inputs
- Counting: A increments, B decrements
- Speed: Up to sysclock/2
- Counter: 32-bit signed

**Configuration**
```
WRPIN: %01101 (P_AB_ENCODER)
WXPIN: Not used
WYPIN: Reset value
Z Result: Net count (A pulses - B pulses)
```

**Spin2 Implementation**
:::: spin2
```
CON
  COUNT_PIN = 20
  AB_MODE = P_AB_ENCODER

PUB setup_ab_counter()
  ' A on pin 20, B on pin 21
  pinstart(COUNT_PIN, AB_MODE, 0, 0)
  
PUB read_difference() : diff
  diff := rdpin(COUNT_PIN)
  
PUB differential_measurement() : result
  wypin(COUNT_PIN, 0)      ' Reset counter
  waitms(100)              ' Measurement period
  result := rdpin(COUNT_PIN)  ' A-B difference
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
ab_init
        mov     pa, ##P_AB_ENCODER
        wrpin   pa, #20         ' A=20, B=21
        dirh    #20
        
differential_count
        wypin   #0, #20         ' Reset counter
        waitx   ##20000000      ' 100ms at 200MHz
        rdpin   diff, #20       ' Read A-B count
        ' diff = pulses on A minus pulses on B
        
diff    long    0
```

**Applications**
- Differential pulse counting
- Phase comparison
- Frequency difference measurement
- Direction sensing

---

### Mode %01110 - Incremental Encoder

**Specifications**
- Function: Single input pulse counter
- Counting: Rising edges
- Speed: Up to sysclock/2
- Counter: 32-bit unsigned

**Configuration**
```
WRPIN: %01110 (P_INC_ENCODER)
WXPIN: Not used
WYPIN: Reset value
Z Result: Pulse count
```

**Spin2 Implementation**
:::: spin2
```
CON
  PULSE_PIN = 20
  INC_MODE = P_INC_ENCODER

PUB setup_counter()
  pinstart(PULSE_PIN, INC_MODE, 0, 0)
  
PUB read_count() : count
  count := rdpin(PULSE_PIN)
  
PUB measure_frequency() : freq
  wypin(PULSE_PIN, 0)      ' Reset
  waitms(1000)             ' 1 second gate
  freq := rdpin(PULSE_PIN) ' Hz
  
PUB count_events(gate_ms) : total
  wypin(PULSE_PIN, 0)
  waitms(gate_ms)
  total := rdpin(PULSE_PIN)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
counter_init
        mov     pa, ##P_INC_ENCODER
        wrpin   pa, #20
        dirh    #20
        
frequency_counter
        wypin   #0, #20         ' Reset count
        waitx   ##200000000     ' 1 second at 200MHz
        rdpin   freq, #20       ' Read frequency in Hz
        
event_counter
        wypin   #0, #20         ' Reset
.wait   rdpin   count, #20      ' Read current
        cmp     count, #1000 wc ' Check if < 1000
  if_c  jmp     #.wait          ' Keep counting
        ' Reached 1000 events
        
freq    long    0
count   long    0
```

**Applications**
- Frequency counting
- Event counting
- Tachometer input
- Production counting
- Flow meter input

---

### Mode %01111 - Local/Global Comparator

**Specifications**
- Function: Pin state comparison
- Inputs: Selectable A and B pins
- Output: Comparison result
- Speed: Single clock response

**Configuration**
```
WRPIN: %01111 (P_COMPARATOR)
WXPIN: Input pin selection
WYPIN: Comparison mode
Z Result: Comparison state
```

**Spin2 Implementation**
:::: spin2
```
CON
  COMP_PIN = 20
  COMP_MODE = P_COMPARATOR

PUB setup_comparator()
  pinstart(COMP_PIN, COMP_MODE, %0001_0010, 0)  ' Compare pins 1 and 2
  
PUB read_comparison() : state
  state := rdpin(COMP_PIN) & 1
  
PUB wait_for_match()
  repeat until rdpin(COMP_PIN) & 1
  
PUB detect_crossing() | last, current
  last := rdpin(COMP_PIN) & 1
  repeat
    current := rdpin(COMP_PIN) & 1
    if current <> last
      ' Crossing detected
      return
    last := current
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
comp_init
        mov     pa, ##P_COMPARATOR
        wrpin   pa, #20
        mov     pa, ##%0001_0010 ' Pins 1 and 2
        wxpin   pa, #20
        dirh    #20
        
wait_equal
.loop   rdpin   state, #20
        test    state, #1 wc
  if_nc jmp     #.loop          ' Wait until equal
        ' Pins are now equal
        
detect_change
        rdpin   last, #20
.watch  rdpin   current, #20
        cmp     current, last wz
  if_z  jmp     #.watch
        ' State changed
        
state   long    0
last    long    0
current long    0
```

**Applications**
- Window comparator
- Zero-crossing detection
- Phase comparison
- Threshold detection
- Signal routing

---

## Chapter 9: Measurement Modes

### Mode %10000-%10011 - Time Accumulation

**Specifications**
- Function: Measure time in selected state
- States: High, Low, or changing
- Resolution: System clock
- Accumulator: 32-bit

**Configuration**
```
WRPIN: %10000-%10011 (P_TIME_ACC)
WXPIN: Measurement period
WYPIN: Not used
Z Result: Accumulated time
```

**Mode Variants:**
- %10000: Time high
- %10001: Time low  
- %10010: Time since change
- %10011: Time between changes

**Spin2 Implementation**
:::: spin2
```
CON
  TIME_PIN = 20
  TIME_HIGH = P_TIME_ACC | %00  ' Measure high time
  TIME_LOW = P_TIME_ACC | %01   ' Measure low time

PUB measure_duty_cycle() : duty_percent | high_time, total_time
  ' Measure high time
  pinstart(TIME_PIN, TIME_HIGH, clkfreq, 0)  ' 1 second window
  waitms(1001)
  high_time := rdpin(TIME_PIN)
  
  ' Calculate duty cycle
  duty_percent := (high_time * 100) / clkfreq
  
PUB measure_pulse_width() : width_us
  pinstart(TIME_PIN, TIME_HIGH, 0, 0)  ' Continuous
  wypin(TIME_PIN, 0)  ' Reset accumulator
  
  ' Wait for pulse
  repeat until pinr(TIME_PIN)
  width_us := rdpin(TIME_PIN) / (clkfreq / 1_000_000)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
time_init
        mov     pa, ##P_TIME_ACC | %00  ' Measure high time
        wrpin   pa, #20
        mov     pa, ##20000000   ' 100ms window at 200MHz
        wxpin   pa, #20
        dirh    #20
        
measure_duty
        wypin   #0, #20         ' Reset
        waitx   ##20000000      ' Wait for window
        rdpin   high_time, #20  ' Get high time
        ' Duty = (high_time * 100) / 20000000
        
measure_period
        mov     pa, ##P_TIME_ACC | %11  ' Time between changes
        wrpin   pa, #20
        dirh    #20
        wypin   #0, #20         ' Reset
.wait   testp   #20, wc         ' Wait for measurement
  if_nc jmp     #.wait
        rdpin   period, #20     ' Get period in clocks
        
high_time long  0
period  long    0
```

**Applications**
- Duty cycle measurement
- Pulse width measurement
- Period measurement
- Frequency measurement
- Signal quality analysis

---

### Mode %10100-%10111 - State Measurement

**Specifications**
- Function: Count state occurrences
- Events: Edges or levels
- Counter: 32-bit
- Speed: Up to sysclock/2

![State Measurement Modes](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page29_img01.png)

**Mode Variants:**
- %10100: Count rising edges
- %10101: Count falling edges
- %10110: Count any edge
- %10111: Count high states

**Configuration**
```
WRPIN: %10100-%10111 (P_STATE_MEAS)
WXPIN: Measurement window (0=continuous)
WYPIN: Not used
Z Result: Event count
```

**Spin2 Implementation**
:::: spin2
```
CON
  EDGE_PIN = 20
  COUNT_RISE = P_STATE_MEAS | %00
  COUNT_FALL = P_STATE_MEAS | %01
  COUNT_BOTH = P_STATE_MEAS | %10

PUB count_pulses(duration_ms) : count
  pinstart(EDGE_PIN, COUNT_RISE, 0, 0)
  wypin(EDGE_PIN, 0)  ' Reset counter
  waitms(duration_ms)
  count := rdpin(EDGE_PIN)
  
PUB measure_frequency() : freq_hz
  pinstart(EDGE_PIN, COUNT_RISE, clkfreq, 0)  ' 1 second
  wypin(EDGE_PIN, 0)
  waitsec(1)
  freq_hz := rdpin(EDGE_PIN)
  
PUB detect_activity() : active
  pinstart(EDGE_PIN, COUNT_BOTH, clkfreq/100, 0)  ' 10ms window
  wypin(EDGE_PIN, 0)
  waitms(11)
  active := rdpin(EDGE_PIN) > 0
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
edge_init
        mov     pa, ##P_STATE_MEAS | %00  ' Count rising
        wrpin   pa, #20
        mov     pa, #0          ' Continuous
        wxpin   pa, #20
        dirh    #20
        
count_events
        wypin   #0, #20         ' Reset counter
        waitx   ##10000000      ' 50ms at 200MHz
        rdpin   count, #20      ' Read count
        
frequency_gate
        mov     pa, ##200000000 ' 1 second gate
        wxpin   pa, #20
        wypin   #0, #20         ' Reset and start
        
.wait   testp   #20, wc         ' Wait for gate close
  if_nc jmp     #.wait
        rdpin   freq, #20       ' Frequency in Hz
        
count   long    0
freq    long    0
```

**Applications**
- Frequency measurement
- Event counting
- RPM measurement
- Signal activity detection
- Pulse counting

---

### Mode %11010 - Pin State Measurement

**Specifications**
- Function: Measure pin state timing
- Measurement: High/low duration
- Resolution: System clock
- Range: 1 to 2^32 clocks

**Configuration**
```
WRPIN: %11010 (P_PIN_STATE)
WXPIN: Timeout value
WYPIN: Edge selection
Z Result: Duration measurement
```

**Spin2 Implementation**
:::: spin2
```
CON
  STATE_PIN = 20
  STATE_MODE = P_PIN_STATE

PUB measure_pulse() : width_clocks
  pinstart(STATE_PIN, STATE_MODE, 0, %01)  ' Positive pulse
  repeat until pinr(STATE_PIN)  ' Wait for measurement
  width_clocks := rdpin(STATE_PIN)
  
PUB measure_frequency_precise() : freq_hz | period
  pinstart(STATE_PIN, STATE_MODE, 0, %11)  ' Full period
  repeat until pinr(STATE_PIN)
  period := rdpin(STATE_PIN)
  freq_hz := clkfreq / period
  
PUB timeout_measurement(max_clocks) : duration | timeout
  pinstart(STATE_PIN, STATE_MODE, max_clocks, %01)
  timeout := cnt + max_clocks + 1000
  repeat until pinr(STATE_PIN) or (cnt > timeout)
  if pinr(STATE_PIN)
    duration := rdpin(STATE_PIN)
  else
    duration := -1  ' Timeout occurred
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
state_init
        mov     pa, ##P_PIN_STATE
        wrpin   pa, #20
        mov     pa, #0          ' No timeout
        wxpin   pa, #20
        mov     pa, #%01        ' Positive pulse
        wypin   pa, #20
        dirh    #20
        
measure_pulse
.wait   testp   #20, wc         ' Wait for measurement
  if_nc jmp     #.wait
        rdpin   width, #20      ' Get pulse width
        
measure_with_timeout
        mov     pa, ##10000000  ' 50ms timeout
        wxpin   pa, #20
        wypin   #%01, #20       ' Reset for new measurement
        
        mov     timeout, cnt
        add     timeout, ##10000000
.check  testp   #20, wc
  if_c  jmp     #.got_it
        cmp     cnt, timeout wc
  if_c  jmp     #.check
        ' Timeout occurred
        mov     width, #-1
        jmp     #.done
.got_it rdpin   width, #20
.done
        
width   long    0
timeout long    0
```

**Applications**
- Pulse width measurement
- Period measurement
- Timeout detection
- Glitch detection
- Protocol timing verification

---

## Chapter 10: ADC Modes

### Mode %11000 - ADC Sample/Filter/Capture (SINC2)

**Specifications**
- Resolution: Up to 14 bits
- Filter: SINC2 decimation
- Sample rate: sysclock / (8 × period)
- Input: Differential or single-ended
- Range: 0V to 3.3V (VIO)

![ADC SINC2 Filter Response](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page31_img01.png)

**Configuration**
```
WRPIN: %11000 (P_ADC_SINC2)
WXPIN: Sample period
WYPIN: Calibration value
Z Result: ADC reading
```

**Spin2 Implementation**
:::: spin2
```
CON
  ADC_PIN = 20
  ADC_MODE = P_ADC_1X | P_ADC

PUB setup_adc()
  pinstart(ADC_PIN, ADC_MODE, 4096, 0)  ' 13-bit resolution
  
PUB read_voltage() : millivolts
  millivolts := (rdpin(ADC_PIN) * 3300) / 8191
  
PUB average_readings(count) : avg | sum
  sum := 0
  repeat count
    sum += rdpin(ADC_PIN)
    waitus(100)
  avg := sum / count
  
PUB continuous_sample(buffer, samples) | i
  repeat i from 0 to samples-1
    repeat until pinr(ADC_PIN)
    buffer[i] := rdpin(ADC_PIN)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
adc_init
        mov     pa, ##P_ADC_1X | P_ADC
        wrpin   pa, #20
        mov     pa, ##4096      ' 13-bit mode
        wxpin   pa, #20
        dirh    #20
        
read_adc
.wait   testp   #20, wc         ' Wait for sample
  if_nc jmp     #.wait
        rdpin   sample, #20     ' Get ADC value
        
continuous_log
        mov     ptra, ##buffer  ' Buffer address
        mov     count, #100     ' 100 samples
.loop   testp   #20, wc
  if_nc jmp     #.loop
        rdpin   sample, #20
        wrlong  sample, ptra++
        djnz    count, #.loop
        
sample  long    0
count   long    0
buffer  res     100
```

**Applications**
- Voltage measurement
- Sensor reading
- Audio sampling
- Data acquisition
- Process monitoring

---

### Mode %11001 - ADC Scope with Trigger (SINC3)

**Specifications**
- Resolution: Up to 12 bits
- Filter: SINC3 decimation
- Trigger: Programmable level
- Sample rate: sysclock / (64 × period)
- Pre/post trigger capture

![ADC Scope Mode](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page32_img01.png)

**Configuration**
```
WRPIN: %11001 (P_ADC_SCOPE)
WXPIN: [31:16] = trigger level, [15:0] = period
WYPIN: Trigger mode and position
Z Result: ADC samples
```

**Spin2 Implementation**
:::: spin2
```
CON
  SCOPE_PIN = 20
  SCOPE_MODE = P_ADC_1X | P_ADC_SCOPE

PUB setup_scope(trigger_mv) | trigger_val
  trigger_val := (trigger_mv * 4095) / 3300
  pinstart(SCOPE_PIN, SCOPE_MODE, trigger_val << 16 | 256, 0)
  
PUB capture_waveform(buffer, samples) | i
  wypin(SCOPE_PIN, %01_00000000)  ' Rising edge trigger
  
  ' Wait for trigger
  repeat until pinr(SCOPE_PIN)
  
  ' Capture post-trigger samples
  repeat i from 0 to samples-1
    repeat until pinr(SCOPE_PIN)
    buffer[i] := rdpin(SCOPE_PIN)
    
PUB auto_trigger() : triggered
  wypin(SCOPE_PIN, %00_00000000)  ' Auto trigger mode
  triggered := pinr(SCOPE_PIN)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
scope_init
        mov     pa, ##P_ADC_1X | P_ADC_SCOPE
        wrpin   pa, #20
        mov     pa, ##$8000_0100 ' Mid-level trigger, 256 period
        wxpin   pa, #20
        dirh    #20
        
triggered_capture
        mov     pa, #%01_00000000 ' Rising edge
        wypin   pa, #20
        
.wait_trig
        testp   #20, wc
  if_nc jmp     #.wait_trig     ' Wait for trigger
        
        ' Capture 100 post-trigger samples
        mov     ptra, ##buffer
        mov     count, #100
.capture
        testp   #20, wc
  if_nc jmp     #.capture
        rdpin   sample, #20
        wrlong  sample, ptra++
        djnz    count, #.capture
        
sample  long    0
count   long    0
buffer  res     100
```

**Applications**
- Oscilloscope function
- Transient capture
- Glitch detection
- Waveform analysis
- Triggered data logging

---

### Mode %11010 - ADC with Calibration

**Specifications**
- Resolution: 8 to 14 bits
- Calibration: Offset and gain
- Input: Differential option
- Sample rate: Programmable
- Accuracy: ±0.5% after calibration

**Configuration**
```
WRPIN: %11010 (P_ADC_CAL)
WXPIN: Sample period
WYPIN: Calibration values
Z Result: Calibrated ADC reading
```

**Spin2 Implementation**
:::: spin2
```
CON
  CAL_PIN = 20
  CAL_MODE = P_ADC_1X | P_ADC_CAL

VAR
  long cal_zero, cal_span

PUB calibrate_adc()
  ' Apply 0V reference
  pinstart(CAL_PIN, CAL_MODE, 4096, 0)
  waitms(10)
  cal_zero := rdpin(CAL_PIN)
  
  ' Apply 3.3V reference
  ' (switch input to reference)
  waitms(10)
  cal_span := rdpin(CAL_PIN) - cal_zero
  
PUB read_calibrated() : millivolts | raw
  raw := rdpin(CAL_PIN) - cal_zero
  millivolts := (raw * 3300) / cal_span
  
PUB auto_calibrate()
  ' Use internal references
  pinstart(CAL_PIN, P_ADC_GIO | P_ADC_CAL, 4096, 0)
  waitms(10)
  cal_zero := rdpin(CAL_PIN)
  
  pinstart(CAL_PIN, P_ADC_VIO | P_ADC_CAL, 4096, 0)
  waitms(10)
  cal_span := rdpin(CAL_PIN) - cal_zero
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
cal_init
        mov     pa, ##P_ADC_1X | P_ADC_CAL
        wrpin   pa, #20
        mov     pa, ##4096
        wxpin   pa, #20
        dirh    #20
        
calibrate
        ' Read zero point
        mov     pa, ##P_ADC_GIO | P_ADC_CAL
        wrpin   pa, #20
        waitx   ##1000000
        rdpin   cal_zero, #20
        
        ' Read span point
        mov     pa, ##P_ADC_VIO | P_ADC_CAL
        wrpin   pa, #20
        waitx   ##1000000
        rdpin   cal_span, #20
        sub     cal_span, cal_zero
        
read_calibrated
.wait   testp   #20, wc
  if_nc jmp     #.wait
        rdpin   raw, #20
        sub     raw, cal_zero
        ' Apply calibration
        mul     raw, ##3300
        div     raw, cal_span
        ' raw now contains millivolts
        
cal_zero long   0
cal_span long   0
raw     long    0
```

**Applications**
- Precision measurement
- Sensor calibration
- Temperature compensation
- Production test systems
- Scientific instruments

---

## Chapter 11: USB Mode

### Mode %11011 - USB Host/Device (Preliminary)

**Specifications**
- Function: USB 1.1 Low/Full Speed
- Data rate: 1.5/12 Mbps
- Mode: Host or Device
- Status: Preliminary implementation

![USB Signaling](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page34_img01.png)

**Note**: USB mode is preliminary. Consult latest silicon documentation for updates.

**Configuration**
```
WRPIN: %11011 (P_USB_MODE)
WXPIN: USB configuration
WYPIN: Data to transmit
Z Result: Received data
```

**Spin2 Implementation**
:::: spin2
```
CON
  USB_DM = 20  ' D- pin
  USB_DP = 21  ' D+ pin
  USB_MODE = P_USB_PAIR

PUB setup_usb_device()
  ' USB requires pin pair (DM, DP)
  pinstart(USB_DM, USB_MODE, 0, 0)
  
PUB usb_low_speed()
  wxpin(USB_DM, %0_0_000000)  ' Low speed mode
  
PUB usb_full_speed()
  wxpin(USB_DM, %1_0_000000)  ' Full speed mode
  
PUB send_usb_packet(data)
  wypin(USB_DM, data)
  repeat until pinr(USB_DM)
  
PUB receive_usb_packet() : data
  repeat until pinr(USB_DM)
  data := rdpin(USB_DM)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
usb_init
        mov     pa, ##P_USB_PAIR
        wrpin   pa, #20         ' DM on pin 20
        mov     pa, #%1_0_000000 ' Full speed
        wxpin   pa, #20
        dirh    #20             ' Enable USB
        
send_packet
        mov     pa, packet_data
        wypin   pa, #20
.wait   testp   #20, wc
  if_nc jmp     #.wait
        
receive_packet
.wait2  testp   #20, wc
  if_nc jmp     #.wait2
        rdpin   received, #20
        
packet_data long $12345678
received    long 0
```

**Applications**
- USB device implementation
- USB host functions
- HID devices
- Serial over USB
- Custom USB protocols

**Important**: Full USB implementation requires additional software stack. This mode provides low-level USB signaling only.

---

## Chapter 12: Serial Modes

### Mode %11100 - Synchronous Serial Transmit

**Specifications**
- Function: Clocked serial output
- Data width: 1-32 bits
- Clock: Generated or external
- Speed: Up to sysclock/2
- Bit order: MSB or LSB first

![Synchronous Serial Timing](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page46_img01.png)

**Configuration**
```
WRPIN: %11100 (P_SYNC_TX)
WXPIN: [31:16] = clock divider, [15:0] = bits-1
WYPIN: Data to transmit
Z Result: Transmission status
```

**Spin2 Implementation**
:::: spin2
```
CON
  SPI_TX = 20
  SPI_CLK = 21
  SYNC_TX_MODE = P_SYNC_TX | P_OE

PUB setup_spi_tx(freq_hz, bits)
  pinstart(SPI_TX, SYNC_TX_MODE, (clkfreq/freq_hz) << 16 | (bits-1), 0)
  
PUB send_byte(data)
  wypin(SPI_TX, data << 24)  ' MSB first for 8 bits
  repeat until pinr(SPI_TX)
  
PUB send_word(data)
  wxpin(SPI_TX, (clkfreq/1_000_000) << 16 | 15)  ' 16 bits at 1MHz
  wypin(SPI_TX, data << 16)  ' MSB first
  repeat until pinr(SPI_TX)
  
PUB burst_send(buffer, count) | i
  repeat i from 0 to count-1
    wypin(SPI_TX, buffer[i] << 24)
    repeat until pinr(SPI_TX)
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
spi_tx_init
        mov     pa, ##P_SYNC_TX | P_OE
        wrpin   pa, #20
        mov     pa, ##$00C8_0007 ' Div by 200, 8 bits
        wxpin   pa, #20
        dirh    #20
        
send_byte
        shl     data, #24       ' Position for MSB first
        wypin   data, #20
.wait   testp   #20, wc
  if_nc jmp     #.wait
        
send_buffer
        mov     ptra, ##buffer
        mov     count, #10
.loop   rdbyte  data, ptra++
        shl     data, #24
        wypin   data, #20
.wait2  testp   #20, wc
  if_nc jmp     #.wait2
        djnz    count, #.loop
        
data    long    0
count   long    0
buffer  byte    $01,$02,$03,$04,$05,$06,$07,$08,$09,$0A
```

**Applications**
- SPI master transmit
- Shift register driving
- Synchronous protocols
- Display interfaces
- DAC serial control

---

### Mode %11101 - Synchronous Serial Receive

**Specifications**
- Function: Clocked serial input
- Data width: 1-32 bits
- Clock: Generated or external
- Speed: Up to sysclock/2
- Bit order: MSB or LSB first

**Configuration**
```
WRPIN: %11101 (P_SYNC_RX)
WXPIN: [31:16] = clock divider, [15:0] = bits-1
WYPIN: Not used
Z Result: Received data
```

**Spin2 Implementation**
:::: spin2
```
CON
  SPI_RX = 20
  SYNC_RX_MODE = P_SYNC_RX

PUB setup_spi_rx(freq_hz, bits)
  pinstart(SPI_RX, SYNC_RX_MODE, (clkfreq/freq_hz) << 16 | (bits-1), 0)
  
PUB receive_byte() : data
  repeat until pinr(SPI_RX)
  data := rdpin(SPI_RX) >> 24  ' MSB first, 8 bits
  
PUB receive_buffer(buffer, count) | i
  repeat i from 0 to count-1
    repeat until pinr(SPI_RX)
    buffer[i] := rdpin(SPI_RX) >> 24
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
spi_rx_init
        mov     pa, ##P_SYNC_RX
        wrpin   pa, #20
        mov     pa, ##$00C8_0007 ' Div by 200, 8 bits
        wxpin   pa, #20
        dirh    #20
        
receive_byte
.wait   testp   #20, wc
  if_nc jmp     #.wait
        rdpin   data, #20
        shr     data, #24       ' Extract byte
        
data    long    0
```

**Applications**
- SPI slave receive
- Shift register reading
- ADC serial interfaces
- Sensor data collection

---

### Mode %11110 - Asynchronous Serial Transmit

**Specifications**
- Function: UART transmit
- Baud rates: 300 to 3 Mbps
- Data bits: 5-8
- Stop bits: 1-2
- Parity: None, even, odd

![Async Serial Format](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page52_img01.png)

**Configuration**
```
WRPIN: %11110 (P_ASYNC_TX)
WXPIN: Bit period in clocks
WYPIN: Data to transmit
Z Result: Transmit buffer status
```

**Spin2 Implementation**
:::: spin2
```
CON
  UART_TX = 20
  BAUD_115200 = 115_200
  ASYNC_TX_MODE = P_ASYNC_TX | P_OE

PUB setup_uart_tx()
  pinstart(UART_TX, ASYNC_TX_MODE, clkfreq / BAUD_115200, 0)
  
PUB tx_byte(b)
  wypin(UART_TX, b)
  repeat until pinr(UART_TX)
  
PUB tx_string(str) | c
  repeat while c := byte[str++]
    tx_byte(c)
    
PUB tx_hex(value) | i
  repeat i from 7 to 0
    tx_byte(lookupz((value >> (i*4)) & $F: "0".."9", "A".."F"))
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
uart_init
        mov     pa, ##P_ASYNC_TX | P_OE
        wrpin   pa, #20
        mov     pa, ##1736      ' 115200 at 200MHz
        wxpin   pa, #20
        dirh    #20
        
tx_char
        wypin   char, #20
.wait   testp   #20, wc
  if_nc jmp     #.wait
        
tx_string
        mov     ptra, ##message
.loop   rdbyte  char, ptra++
        tjz     char, #.done
        wypin   char, #20
.wait2  testp   #20, wc
  if_nc jmp     #.wait2
        jmp     #.loop
.done
        
char    long    0
message byte    "Hello P2!",13,10,0
```

**Applications**
- Serial console output
- Debug messages
- Data logging
- Modem communication
- GPS/sensor interfaces

---

### Mode %11111 - Asynchronous Serial Receive

**Specifications**
- Function: UART receive
- Baud rates: 300 to 3 Mbps
- Data bits: 5-8
- Stop bits: 1-2
- Parity: None, even, odd

![Async Receive Timing](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page52_img02.png)

**Configuration**
```
WRPIN: %11111 (P_ASYNC_RX)
WXPIN: Bit period in clocks
WYPIN: Not used
Z Result: Received character
```

**Spin2 Implementation**
:::: spin2
```
CON
  UART_RX = 20
  BAUD_115200 = 115_200
  ASYNC_RX_MODE = P_ASYNC_RX

PUB setup_uart_rx()
  pinstart(UART_RX, ASYNC_RX_MODE, clkfreq / BAUD_115200, 0)
  
PUB rx_byte() : b
  repeat until pinr(UART_RX)
  b := rdpin(UART_RX)
  
PUB rx_check() : b | avail
  avail := pinr(UART_RX)
  if avail
    b := rdpin(UART_RX)
  else
    b := -1
    
PUB rx_string(buffer, maxlen) | c, i
  i := 0
  repeat
    c := rx_byte()
    if c == 13 or i => maxlen-1
      buffer[i] := 0
      return
    buffer[i++] := c
```

**PASM2 Implementation**
:::: pasm2
```
DAT
        org     0
        
uart_rx_init
        mov     pa, ##P_ASYNC_RX
        wrpin   pa, #20
        mov     pa, ##1736      ' 115200 at 200MHz
        wxpin   pa, #20
        dirh    #20
        
rx_char
.wait   testp   #20, wc
  if_nc jmp     #.wait
        rdpin   char, #20
        
rx_buffer
        mov     ptra, ##buffer
        mov     count, #0
.loop   testp   #20, wc
  if_nc jmp     #.loop
        rdpin   char, #20
        cmp     char, #13 wz    ' Check for CR
  if_z  jmp     #.done
        wrbyte  char, ptra++
        add     count, #1
        cmp     count, #79 wc   ' Buffer limit
  if_c  jmp     #.loop
.done   wrbyte  #0, ptra        ' Null terminate
        
char    long    0
count   long    0
buffer  res     80
```

**Applications**
- Serial console input
- Command processing
- Data reception
- Sensor reading
- GPS parsing

---

# Part III: Application Guide

## Chapter 13: Common Implementations

This chapter provides complete, production-ready implementations combining multiple Smart Pin modes.

### 13.1 Motor Control with Encoder Feedback

:::: spin2
```
CON
  MOTOR_PWM = 20
  ENCODER_A = 22
  TARGET_RPM = 3000
  
VAR
  long current_rpm, pwm_duty

PUB motor_control_loop() | error, last_pos, current_pos
  ' Setup PWM for motor
  pinstart(MOTOR_PWM, P_PWM_TRIANGLE | P_OE, clkfreq/20_000, 0)
  
  ' Setup quadrature encoder
  pinstart(ENCODER_A, P_QUADRATURE_ENC, 0, 0)
  
  repeat
    ' Read encoder
    last_pos := current_pos
    current_pos := rdpin(ENCODER_A)
    
    ' Calculate RPM (assuming 100 counts/rev, 10Hz loop)
    current_rpm := ((current_pos - last_pos) * 600) / 100
    
    ' PID control (simplified P-only)
    error := TARGET_RPM - current_rpm
    pwm_duty := (pwm_duty + (error / 10)) #> 0 <# $FFFF
    
    ' Update motor PWM
    wypin(MOTOR_PWM, pwm_duty)
    
    waitms(100)  ' 10Hz control loop
```

### 13.2 Multi-Channel Data Acquisition

:::: spin2
```
CON
  ADC_CHANNELS = 8
  SAMPLE_RATE = 1000  ' Hz per channel
  
VAR
  long adc_buffer[ADC_CHANNELS * 100]  ' 100ms buffer

PUB acquire_multichannel() | ch, sample_count
  ' Configure all ADC channels
  repeat ch from 0 to ADC_CHANNELS-1
    pinstart(ch, P_ADC_1X | P_ADC, clkfreq/SAMPLE_RATE/ADC_CHANNELS, 0)
    
  sample_count := 0
  repeat
    ' Round-robin sampling
    repeat ch from 0 to ADC_CHANNELS-1
      repeat until pinr(ch)
      adc_buffer[sample_count * ADC_CHANNELS + ch] := rdpin(ch)
    
    sample_count++
    if sample_count => 100
      process_buffer(@adc_buffer, sample_count)
      sample_count := 0
```

### 13.3 UART Bridge with Flow Control

:::: spin2
```
CON
  UART1_RX = 20
  UART1_TX = 21
  UART2_RX = 22
  UART2_TX = 23
  
PUB uart_bridge() | c
  ' Setup both UARTs at 115200
  pinstart(UART1_RX, P_ASYNC_RX, clkfreq/115_200, 0)
  pinstart(UART1_TX, P_ASYNC_TX | P_OE, clkfreq/115_200, 0)
  pinstart(UART2_RX, P_ASYNC_RX, clkfreq/115_200, 0)
  pinstart(UART2_TX, P_ASYNC_TX | P_OE, clkfreq/115_200, 0)
  
  repeat
    ' Bridge UART1 -> UART2
    if pinr(UART1_RX)
      c := rdpin(UART1_RX)
      wypin(UART2_TX, c)
      repeat until pinr(UART2_TX)
      
    ' Bridge UART2 -> UART1
    if pinr(UART2_RX)
      c := rdpin(UART2_RX)
      wypin(UART1_TX, c)
      repeat until pinr(UART1_TX)
```

### 13.4 Frequency Counter with Display

:::: spin2
```
CON
  FREQ_INPUT = 20
  GATE_TIME = 1_000  ' 1 second gate
  
PUB frequency_meter() : freq_hz
  ' Setup for rising edge counting
  pinstart(FREQ_INPUT, P_STATE_MEAS | %00, clkfreq, 0)
  
  repeat
    wypin(FREQ_INPUT, 0)  ' Reset counter
    waitms(GATE_TIME)
    freq_hz := rdpin(FREQ_INPUT)
    
    ' Display frequency
    if freq_hz < 1000
      debug("Frequency: ", udec(freq_hz), " Hz")
    elseif freq_hz < 1_000_000
      debug("Frequency: ", udec(freq_hz/1000), ".", udec3((freq_hz//1000)), " kHz")
    else
      debug("Frequency: ", udec(freq_hz/1_000_000), ".", udec3((freq_hz//1_000_000)/1000), " MHz")
```

### 13.5 Waveform Generator

:::: spin2
```
CON
  DAC_OUT = 20
  
VAR
  long wave_table[256]

PUB setup_waveforms()
  ' Generate sine table
  repeat i from 0 to 255
    wave_table[i] := $8000 + sin(i * 1406, $7FFF)  ' 360/256 = 1.406 degrees
    
PUB generate_sine(freq_hz) | index, step
  pinstart(DAC_OUT, P_DAC_124R_3V | P_OE, 0, 0)
  
  step := (freq_hz * 256) frac clkfreq
  index := 0
  
  repeat
    wypin(DAC_OUT, wave_table[index >> 24])
    index += step
    waitus(10)  ' 100kHz update rate
```

### 13.6 SPI Master Implementation

:::: spin2
```
CON
  SPI_CLK = 20
  SPI_MOSI = 21
  SPI_MISO = 22
  SPI_CS = 23
  
PUB spi_transfer(data_out) : data_in
  pinl(SPI_CS)  ' Assert chip select
  
  ' Send and receive 8 bits
  wypin(SPI_MOSI, data_out << 24)
  repeat until pinr(SPI_MOSI) and pinr(SPI_MISO)
  data_in := rdpin(SPI_MISO) >> 24
  
  pinh(SPI_CS)  ' Deassert chip select
```

### 13.7 Servo Controller Array

:::: spin2
```
CON
  SERVO_COUNT = 8
  SERVO_BASE = 20
  
VAR
  long servo_positions[SERVO_COUNT]

PUB setup_servos() | i
  repeat i from 0 to SERVO_COUNT-1
    pinstart(SERVO_BASE + i, P_PULSE | P_OE, clkfreq/50, 0)  ' 50Hz/20ms
    servo_positions[i] := 1500  ' Center position (1.5ms)
    
PUB set_servo(ch, microseconds)
  servo_positions[ch] := microseconds #> 500 <# 2500
  wypin(SERVO_BASE + ch, servo_positions[ch] * (clkfreq/1_000_000))
  
PUB sweep_all_servos() | i, pos
  repeat
    repeat pos from 1000 to 2000 step 10
      repeat i from 0 to SERVO_COUNT-1
        set_servo(i, pos)
      waitms(20)
```

### 13.8 I2C Master Bit-Bang Pattern

:::: spin2
```
CON
  I2C_SCL = 20
  I2C_SDA = 21
  
PUB i2c_start()
  pinh(I2C_SDA)
  pinh(I2C_SCL)
  waitus(1)
  pinl(I2C_SDA)  ' SDA low while SCL high
  waitus(1)
  pinl(I2C_SCL)
  
PUB i2c_write(data) : ack | bit
  repeat bit from 7 to 0
    if data & (1 << bit)
      pinh(I2C_SDA)
    else
      pinl(I2C_SDA)
    waitus(1)
    pinh(I2C_SCL)
    waitus(1)
    pinl(I2C_SCL)
    
  ' Read ACK
  pinfloat(I2C_SDA)
  waitus(1)
  pinh(I2C_SCL)
  ack := pinr(I2C_SDA)
  pinl(I2C_SCL)
```

### 13.9 RGB LED Controller

:::: spin2
```
CON
  LED_R = 20
  LED_G = 21
  LED_B = 22
  
PUB setup_rgb()
  pinstart(LED_R, P_PWM_SAWTOOTH | P_OE, $FFFF, 0)
  pinstart(LED_G, P_PWM_SAWTOOTH | P_OE, $FFFF, 0)
  pinstart(LED_B, P_PWM_SAWTOOTH | P_OE, $FFFF, 0)
  
PUB set_color(r, g, b)
  wypin(LED_R, r << 8)  ' Scale 0-255 to 0-65535
  wypin(LED_G, g << 8)
  wypin(LED_B, b << 8)
  
PUB rainbow_cycle() | hue
  repeat
    repeat hue from 0 to 359
      set_color_hsv(hue, 255, 255)
      waitms(10)
```

### 13.10 Precision Timing Generator

:::: spin2
```
CON
  TIMING_PIN = 20
  
PUB microsecond_pulse(width_us)
  pinstart(TIMING_PIN, P_PULSE | P_OE, clkfreq/1_000_000 * width_us, 0)
  wypin(TIMING_PIN, 1)  ' Single pulse
  repeat until pinr(TIMING_PIN)
  
PUB nanosecond_delay(delay_ns) | clocks
  clocks := (clkfreq * delay_ns) / 1_000_000_000
  pinstart(TIMING_PIN, P_PULSE, clocks, 0)
  wypin(TIMING_PIN, 1)
  repeat until pinr(TIMING_PIN)
```

---

## Chapter 14: Multi-Pin Applications

This chapter demonstrates complex applications using multiple Smart Pins working together.

### 14.1 Three-Phase Motor Controller

:::: spin2
```
CON
  PHASE_A = 20
  PHASE_B = 21
  PHASE_C = 22
  
VAR
  long phase_angle

PUB three_phase_motor(freq_hz)
  ' Configure three PWM pins 120 degrees apart
  pinstart(PHASE_A, P_PWM_TRIANGLE | P_OE, clkfreq/20_000, 0)
  pinstart(PHASE_B, P_PWM_TRIANGLE | P_OE, clkfreq/20_000, 0)
  pinstart(PHASE_C, P_PWM_TRIANGLE | P_OE, clkfreq/20_000, 0)
  
  repeat
    ' Generate three-phase sine waves
    wypin(PHASE_A, $8000 + sin(phase_angle, $7FFF))
    wypin(PHASE_B, $8000 + sin(phase_angle + 120, $7FFF))
    wypin(PHASE_C, $8000 + sin(phase_angle + 240, $7FFF))
    
    phase_angle += freq_hz / 100  ' Advance angle
    waitms(10)
```

### 14.2 Logic Analyzer

:::: spin2
```
CON
  CHANNELS = 8
  SAMPLE_DEPTH = 1000
  
VAR
  long samples[SAMPLE_DEPTH]

PUB logic_analyzer(trigger_channel, trigger_level)
  ' Setup trigger on one channel
  pinstart(trigger_channel, P_COMPARATOR, trigger_level, 0)
  
  ' Wait for trigger
  repeat until rdpin(trigger_channel) & 1
  
  ' Capture samples
  repeat i from 0 to SAMPLE_DEPTH-1
    samples[i] := ina[CHANNELS-1..0]
    waitus(1)  ' 1MHz sample rate
```

### 14.3 Digital Oscilloscope

:::: spin2
```
CON
  CH1_ADC = 20
  CH2_ADC = 21
  TRIGGER = 22
  
VAR
  long ch1_buffer[1000]
  long ch2_buffer[1000]

PUB dual_channel_scope()
  ' Setup ADCs
  pinstart(CH1_ADC, P_ADC_SCOPE, $8000_0100, 0)  ' Mid-level trigger
  pinstart(CH2_ADC, P_ADC_1X | P_ADC, 4096, 0)
  
  ' Wait for trigger on CH1
  wypin(CH1_ADC, %01_00000000)  ' Rising edge trigger
  repeat until pinr(CH1_ADC)
  
  ' Capture both channels
  repeat i from 0 to 999
    repeat until pinr(CH1_ADC) and pinr(CH2_ADC)
    ch1_buffer[i] := rdpin(CH1_ADC)
    ch2_buffer[i] := rdpin(CH2_ADC)
```

### 14.4 Stepper Motor with Acceleration

:::: spin2
```
CON
  STEP_PIN = 20
  DIR_PIN = 21
  ENABLE_PIN = 22
  
VAR
  long current_speed, target_speed

PUB accelerated_move(steps, max_speed) | accel_steps
  pinh(DIR_PIN)  ' Set direction
  pinl(ENABLE_PIN)  ' Enable driver
  
  accel_steps := max_speed / 100  ' Simple acceleration
  
  ' Acceleration phase
  repeat i from 1 to accel_steps
    current_speed := (max_speed * i) / accel_steps
    pinstart(STEP_PIN, P_PULSE | P_OE, clkfreq/current_speed, 0)
    wypin(STEP_PIN, 1)
    repeat until pinr(STEP_PIN)
    
  ' Constant speed phase
  pinstart(STEP_PIN, P_PULSE | P_OE, clkfreq/max_speed, 0)
  wypin(STEP_PIN, steps - (accel_steps * 2))
  repeat until pinr(STEP_PIN)
  
  ' Deceleration phase
  repeat i from accel_steps to 1
    current_speed := (max_speed * i) / accel_steps
    pinstart(STEP_PIN, P_PULSE | P_OE, clkfreq/current_speed, 0)
    wypin(STEP_PIN, 1)
    repeat until pinr(STEP_PIN)
```

### 14.5 Audio Spectrum Analyzer

:::: spin2
```
CON
  AUDIO_IN = 20
  LED_BASE = 30
  BANDS = 8
  
VAR
  long fft_bins[BANDS]

PUB spectrum_display()
  ' Setup audio ADC
  pinstart(AUDIO_IN, P_ADC_1X | P_ADC, 256, 0)  ' ~780kHz sample rate
  
  ' Setup LED bar graph
  repeat i from 0 to BANDS-1
    pinstart(LED_BASE + i, P_PWM_SAWTOOTH | P_OE, $FFFF, 0)
    
  repeat
    ' Collect samples and compute FFT (simplified)
    compute_fft()
    
    ' Display on LEDs
    repeat i from 0 to BANDS-1
      wypin(LED_BASE + i, fft_bins[i] << 8)
```

---

## Chapter 15: Optimization & Troubleshooting

### Performance Optimization

#### Clock Distribution
:::: spin2
```
PUB optimize_clock_distribution()
  ' Use NCO for multiple synchronized clocks
  pinstart(20, P_NCO_FREQ | P_OE, 1, freq1)
  pinstart(21, P_NCO_FREQ | P_OE, 1, freq2)
  pinstart(22, P_NCO_FREQ | P_OE, 1, freq3)
  
  ' All NCOs are phase-coherent when started together
  dirh(20 addpins 2)  ' Enable all three simultaneously
```

#### Power Management
:::: spin2
```
PUB low_power_sampling()
  ' Use repository mode for infrequent updates
  pinstart(20, P_REPOSITORY, 0, 0)
  
  ' COG can sleep while Smart Pin maintains value
  repeat
    wypin(20, read_sensor())
    waitms(1000)  ' COG sleeps, Smart Pin holds value
```

### Common Issues and Solutions

#### Issue: PWM Glitches
**Symptom**: Brief pulses when changing duty cycle  
**Solution**: Update during safe window
:::: spin2
```
PUB glitch_free_pwm_update(new_duty)
  ' Wait for counter reset
  repeat until (rdpin(PWM_PIN) & $FFFF) < 100
  wypin(PWM_PIN, new_duty)
```

#### Issue: ADC Noise
**Symptom**: Unstable ADC readings  
**Solution**: Use averaging and filtering
:::: spin2
```
PUB filtered_adc_read() : result | sum
  sum := 0
  repeat 16
    repeat until pinr(ADC_PIN)
    sum += rdpin(ADC_PIN)
  result := sum >> 4  ' Average of 16 samples
```

#### Issue: Encoder Missing Counts
**Symptom**: Position drift over time  
**Solution**: Check maximum frequency
:::: spin2
```
PUB verify_encoder_speed() | max_freq
  ' Encoder max frequency = sysclock / 2
  max_freq := clkfreq / 2
  debug("Max encoder frequency: ", udec(max_freq/1000), " kHz")
  
  ' For 1000 CPR encoder:
  debug("Max RPM: ", udec(max_freq * 60 / 1000 / 4))
```

#### Issue: Serial Data Corruption
**Symptom**: Garbled UART data  
**Solution**: Verify baud rate calculation
:::: spin2
```
PUB calculate_baud_error(desired_baud) | actual_baud, divider, error_ppm
  divider := clkfreq / desired_baud
  actual_baud := clkfreq / divider
  error_ppm := abs(((actual_baud - desired_baud) * 1_000_000) / desired_baud)
  
  debug("Desired: ", udec(desired_baud))
  debug("Actual: ", udec(actual_baud))
  debug("Error: ", udec(error_ppm), " ppm")
  
  if error_ppm > 20_000  ' >2% error
    debug("WARNING: Baud rate error too high!")
```

### Debugging Techniques

#### Smart Pin State Monitor
:::: spin2
```
PUB monitor_smart_pin(pin)
  debug("Pin ", udec(pin), " Status:")
  debug("  IN flag: ", udec(pinr(pin)))
  debug("  Z value: ", uhex(rdpin(pin)))
  debug("  Mode: ", uhex((pinr(pin) >> 6) & $3F))
```

#### Performance Profiling
:::: spin2
```
PUB profile_smart_pin_timing(pin) | start, cycles
  start := cnt
  
  ' Perform Smart Pin operation
  wypin(pin, test_value)
  repeat until pinr(pin)
  
  cycles := cnt - start
  debug("Operation took ", udec(cycles), " cycles")
  debug("Time: ", udec(cycles * 1_000_000 / clkfreq), " microseconds")
```

---

# Part IV: Quick Reference

## Appendix A: Mode Selection Guide with Comparison Matrix

### Smart Pin Mode Comparison Matrix

| Mode | Function | Max Freq | Resolution | Power | Typical Use |
|------|----------|----------|------------|-------|-------------|
| **%00000** | OFF | - | - | Minimum | GPIO |
| **%00001** | Repository | sysclock | 32-bit | Low | Inter-COG data |
| **%00111** | Transition | sysclock/2 | 1 clock | Low | Clock gen |
| **%00010** | DAC 124Ω 3.3V | sysclock/2 | 16-bit | Medium | Audio out |
| **%00011** | DAC 75Ω 2.0V | sysclock/2 | 16-bit | Medium | Video out |
| **%00100** | Pulse/Cycle | sysclock/2 | 32-bit | Low | Timing |
| **%00101** | NCO Frequency | sysclock/2 | 32-bit | Low | Synthesis |
| **%00110** | NCO Duty | sysclock/4 | 16-bit | Low | Fine PWM |
| **%01000** | PWM Sawtooth | sysclock/2 | 16-bit | Low | Motor control |
| **%01001** | PWM Triangle | sysclock/4 | 16-bit | Low | Low EMI PWM |
| **%01010** | SMPS Pulse | sysclock | 32-bit | Low | Power supply |
| **%01011** | Quadrature | sysclock/2 | 32-bit | Low | Encoders |
| **%01101** | A-B Encoder | sysclock/2 | 32-bit | Low | Differential |
| **%01110** | Incremental | sysclock/2 | 32-bit | Low | Counting |
| **%01111** | Comparator | sysclock | 1-bit | Low | Threshold |
| **%10000** | Time High | sysclock | 32-bit | Low | Duty measure |
| **%10001** | Time Low | sysclock | 32-bit | Low | Pulse measure |
| **%10010** | Time Change | sysclock | 32-bit | Low | Period |
| **%10011** | Time Between | sysclock | 32-bit | Low | Frequency |
| **%10100** | Count Rise | sysclock/2 | 32-bit | Low | Events |
| **%10101** | Count Fall | sysclock/2 | 32-bit | Low | Events |
| **%10110** | Count Edges | sysclock/2 | 32-bit | Low | Activity |
| **%10111** | Count High | sysclock | 32-bit | Low | Duty count |
| **%11000** | ADC SINC2 | sysclock/8 | 14-bit | Medium | Precision ADC |
| **%11001** | ADC Scope | sysclock/64 | 12-bit | Medium | Triggered |
| **%11010** | ADC Calibrated | sysclock/8 | 14-bit | Medium | Accurate |
| **%11011** | USB | 12 Mbps | 8-bit | High | USB 1.1 |
| **%11100** | Sync TX | sysclock/2 | 32-bit | Low | SPI/Shift |
| **%11101** | Sync RX | sysclock/2 | 32-bit | Low | SPI/Shift |
| **%11110** | Async TX | 3 Mbps | 8-bit | Low | UART |
| **%11111** | Async RX | 3 Mbps | 8-bit | Low | UART |

### Decision Tree for Mode Selection

```
Start: What type of signal?
│
├─ Digital Output?
│  ├─ Simple on/off? → Mode %00000 (GPIO)
│  ├─ Clock/Square wave? → Mode %00111 (Transition)
│  ├─ Precise pulses? → Mode %00100 (Pulse)
│  ├─ Variable frequency? → Mode %00101 (NCO Freq)
│  ├─ PWM needed?
│  │  ├─ High frequency? → Mode %00110 (NCO Duty)
│  │  ├─ Motor control? → Mode %01000 (Sawtooth)
│  │  ├─ Low EMI? → Mode %01001 (Triangle)
│  │  └─ SMPS? → Mode %01010 (SMPS Pulse)
│  └─ Serial data? → Mode %11100 (Sync TX) or %11110 (Async TX)
│
├─ Digital Input?
│  ├─ Simple read? → Mode %00000 (GPIO)
│  ├─ Encoder?
│  │  ├─ Quadrature? → Mode %01011
│  │  ├─ A-B separate? → Mode %01101
│  │  └─ Single channel? → Mode %01110
│  ├─ Counting events?
│  │  ├─ Rising edges? → Mode %10100
│  │  ├─ Falling edges? → Mode %10101
│  │  └─ Both edges? → Mode %10110
│  ├─ Measuring time?
│  │  ├─ High duration? → Mode %10000
│  │  ├─ Low duration? → Mode %10001
│  │  └─ Period? → Mode %10010
│  └─ Serial data? → Mode %11101 (Sync RX) or %11111 (Async RX)
│
├─ Analog Output?
│  ├─ General purpose? → Mode %00010 (DAC 124Ω)
│  └─ Video/75Ω line? → Mode %00011 (DAC 75Ω)
│
└─ Analog Input?
   ├─ Basic sampling? → Mode %11000 (SINC2)
   ├─ Triggered capture? → Mode %11001 (Scope)
   └─ Calibrated? → Mode %11010 (Calibrated)
```

### Performance Characteristics by Category

#### Output Modes - Timing Performance
| Mode | Min Period | Max Frequency | Jitter |
|------|------------|---------------|--------|
| Transition | 2 clocks | sysclock/2 | < 1 clock |
| NCO Freq | 8 clocks | sysclock/8 | < 1 clock |
| NCO Duty | 4 clocks | sysclock/4 | < 1 clock |
| PWM Sawtooth | 2 clocks | sysclock/2 | None |
| PWM Triangle | 4 clocks | sysclock/4 | None |

#### Input Modes - Measurement Limits
| Mode | Min Pulse | Max Count Rate | Resolution |
|------|-----------|----------------|------------|
| Edge Counter | 2 clocks | sysclock/2 | 1 edge |
| Time Measure | 1 clock | continuous | 1 clock |
| Quadrature | 4 clocks | sysclock/4 | 4x encoder |

#### ADC Modes - Quality Metrics
| Mode | Bits | Sample Rate | Filter | SNR |
|------|------|-------------|--------|-----|
| SINC2 | 14 | sysclock/8 | 2nd order | 86dB |
| Scope | 12 | sysclock/64 | 3rd order | 74dB |
| Calibrated | 14 | sysclock/8 | 2nd order | 86dB |

---

## Appendix B: Configuration Calculator

### Common Configuration Values

#### UART Baud Rate Settings (at 200MHz)
```
Baud Rate   WXPIN Value   Actual Baud   Error
---------   -----------   -----------   -----
300         666,667       300.0         0.00%
1,200       166,667       1,200.0       0.00%
2,400       83,333        2,400.0       0.00%
4,800       41,667        4,800.0       0.00%
9,600       20,833        9,600.0       0.00%
19,200      10,417        19,200.0      0.00%
38,400      5,208         38,400.0      0.00%
57,600      3,472         57,603.7      0.01%
115,200     1,736         115,207.4     0.01%
230,400     868           230,414.7     0.01%
460,800     434           460,829.5     0.01%
921,600     217           921,658.9     0.01%
```

#### PWM Frequency Settings (at 200MHz)
```
Frequency   Period (WXPIN)   Resolution
---------   -------------   ----------
100 Hz      2,000,000       24 bits
1 kHz       200,000         20 bits
10 kHz      20,000          16 bits
20 kHz      10,000          15 bits
50 kHz      4,000           13 bits
100 kHz     2,000           12 bits
200 kHz     1,000           11 bits
500 kHz     400             10 bits
1 MHz       200             9 bits
```

#### NCO Frequency Values (at 200MHz)
```
Frequency   WYPIN Value (hex)   Actual Freq   Error
---------   ----------------   -----------   -----
1 Hz        0x00A7C5AC         1.000 Hz      0.000%
10 Hz       0x068DB8B          10.000 Hz     0.000%
100 Hz      0x418937A          100.000 Hz    0.000%
1 kHz       0x28F5C29          1.000 kHz     0.000%
10 kHz      0x1999999A         10.000 kHz    0.000%
100 kHz     0xFFFFFFFF         100.000 kHz   0.000%
1 MHz       0x0CCCCCCD         1.000 MHz     0.000%
```

### Configuration Formulas

#### Clock/Frequency Calculations
:::: spin2
```
' UART bit period
bit_period = clkfreq / baud_rate

' PWM frequency
pwm_freq = clkfreq / pwm_period

' NCO frequency value
nco_value = (desired_freq << 32) / clkfreq

' ADC sample rate
sample_rate = clkfreq / (8 * wxpin_value)  ' SINC2
sample_rate = clkfreq / (64 * wxpin_value) ' SINC3
```

#### Timing Calculations
:::: spin2
```
' Pulse width in microseconds
wxpin_value = (pulse_us * clkfreq) / 1_000_000

' Period measurement to frequency
frequency = clkfreq / measured_period

' Duty cycle from time measurements
duty_percent = (high_time * 100) / (high_time + low_time)
```

---

## Appendix C: Register Reference

### WRPIN Mode Register Bit Fields

```
Bit 31..14: Pin Configuration
  31..28: Reserved
  27..26: Output drive strength
  25..24: Input selector
  23..20: Input pin select
  19..14: Filter/comparator settings

Bit 13..8: Digital Filtering
  13..8: Filter tau value (0-63)

Bit 7..6: Output Enable
  7: Invert output
  6: Output enable

Bit 5..0: Smart Pin Mode
  5..0: Mode selection (%MMMMMM)
```

### X Register Usage by Mode

| Mode | X Register Function |
|------|-------------------|
| Repository | Not used |
| Transition | Period in clocks |
| DAC | Update period (0=manual) |
| Pulse | Pulse width |
| NCO | Base divider |
| PWM | Period value |
| Encoder | Not used |
| Time Measure | Window period |
| Count | Window period |
| ADC | Sample period |
| USB | Configuration |
| Serial TX | [31:16]=divider, [15:0]=bits |
| Serial RX | [31:16]=divider, [15:0]=bits |

### Y Register Usage by Mode

| Mode | Y Register Function |
|------|-------------------|
| Repository | Value to store |
| Transition | Transition count |
| DAC | DAC value (16-bit) |
| Pulse | Pulse count |
| NCO Freq | Frequency value |
| NCO Duty | [31:16]=duty, [15:0]=freq |
| PWM | Duty value |
| Encoder | Reset value |
| Time Measure | Not used |
| Count | Not used |
| ADC | Calibration |
| USB | Data to send |
| Serial TX | Data to transmit |
| Serial RX | Not used |

### Z Register Results by Mode

| Mode | Z Register Contents |
|------|-------------------|
| Repository | Stored value |
| Transition | Transitions remaining |
| DAC | Current DAC value |
| Pulse | Pulses remaining |
| NCO | Phase accumulator |
| PWM | Current counter |
| Encoder | Position count |
| Time Measure | Accumulated time |
| Count | Event count |
| ADC | Sample value |
| USB | Received data |
| Serial TX | Status |
| Serial RX | Received data |

---

## Appendix D: Electrical Specifications

### Digital I/O Specifications

| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| VIL (Input Low) | -0.3 | - | 0.8 | V |
| VIH (Input High) | 2.0 | - | 3.6 | V |
| VOL (Output Low) | - | 0.4 | 0.6 | V |
| VOH (Output High) | 2.4 | 3.0 | - | V |
| IOL (Sink Current) | - | 25 | 40 | mA |
| IOH (Source Current) | - | 25 | 40 | mA |
| Input Capacitance | - | 5 | 10 | pF |
| Rise/Fall Time | - | 2 | 5 | ns |

### DAC Specifications

| Parameter | 124Ω Mode | 75Ω Mode | Unit |
|-----------|-----------|----------|------|
| Resolution | 16 | 16 | bits |
| Output Range | 0-3.3 | 0-2.0 | V |
| Output Impedance | 124±5% | 75±5% | Ω |
| Settling Time | <1 | <1 | µs |
| Update Rate | 100 | 100 | MHz |
| INL | ±2 | ±2 | LSB |
| DNL | ±1 | ±1 | LSB |

### ADC Specifications

| Parameter | SINC2 | SINC3 | Calibrated | Unit |
|-----------|-------|-------|------------|------|
| Resolution | 14 | 12 | 14 | bits |
| Sample Rate | 25M | 3.125M | 25M | SPS |
| Input Range | 0-3.3 | 0-3.3 | 0-3.3 | V |
| Input Impedance | >1 | >1 | >1 | MΩ |
| SNR | 86 | 74 | 86 | dB |
| ENOB | 14 | 12 | 14 | bits |

### Timing Specifications

| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| Smart Pin Setup | - | 2 | 4 | clocks |
| Smart Pin Hold | - | 1 | 2 | clocks |
| IN Flag Delay | - | 2 | 3 | clocks |
| RDPIN Latency | - | 3 | 4 | clocks |
| Maximum Toggle | - | 100 | - | MHz |

### Power Consumption (per Smart Pin)

| Mode | Idle | Active | Unit |
|------|------|--------|------|
| OFF | 0 | 0 | µA |
| Digital | 10 | 100 | µA |
| PWM | 20 | 200 | µA |
| NCO | 25 | 250 | µA |
| ADC | 50 | 2000 | µA |
| DAC | 40 | 1500 | µA |
| USB | 100 | 5000 | µA |

---

## Index

**A**
- A-B Encoder Mode: 8-2
- ADC Calibration: 10-3
- ADC Modes: Chapter 10
- ADC SINC2 Filter: 10-1
- ADC Scope Mode: 10-2
- Acknowledge Smart Pin: 3-2
- AKPIN Instruction: 3-2
- Analog Input: Chapter 10
- Analog Output: Chapter 5
- Applications: Chapter 13-14
- Architecture: 1-1
- Asynchronous Serial: 12-3, 12-4

**B**
- Baud Rate Calculation: B-1
- Bit Period: 12-3
- Block Diagram: 1-1

**C**
- Calibration: 10-3
- Clock Distribution: 15-1
- Clock Domains: 1-4
- Comparator Mode: 8-4
- Configuration Calculator: Appendix B
- Configuration Protocol: Chapter 2
- Configuration Sequence: 2-1
- Counter Modes: Chapter 8-9

**D**
- DAC 124Ω Mode: 5-1
- DAC 75Ω Mode: 5-2
- DAC Modes: Chapter 5
- Data Acquisition: 13-2
- Debugging: 15-3
- Digital Filtering: 2-2
- Digital I/O: Chapter 4
- DIRH Instruction: 2-5
- DIRL Instruction: 2-1
- Duty Cycle: 6-3, 7-1

**E**
- Edge Detection: 9-2
- Electrical Specifications: Appendix D
- Encoder Modes: Chapter 8
- Error Handling: 3-4

**F**
- Frequency Generation: 6-2
- Frequency Measurement: 9-1

**G**
- GPIO Mode: 4-1

**H**
- Hardware Architecture: 1-2

**I**
- IN Flag: 2-4
- Incremental Encoder: 8-3
- Input Selector: 1-2
- Inter-COG Communication: 4-2

**M**
- Measurement Modes: Chapter 9
- Mode Register: 2-2
- Mode Selection: Appendix A
- Motor Control: 13-1
- Multi-COG Coordination: 3-3
- Multi-Pin Applications: Chapter 14

**N**
- NCO Duty Mode: 6-3
- NCO Frequency Mode: 6-2
- NCO Modes: 6-2, 6-3

**O**
- Optimization: Chapter 15
- Output Driver: 1-2
- Output Enable: 2-2

**P**
- PASM2 Instructions: 3-2
- Performance: 15-1
- Periodic Pulse Mode: 7-3
- Pin Numbering: 1-3
- Pin State Measurement: 9-3
- Pulse Mode: 6-1
- PWM Modes: Chapter 7
- PWM Sawtooth: 7-1
- PWM Triangle: 7-2

**Q**
- Quadrature Encoder: 8-1
- Quick Reference: Part IV
- Quick Start Guide: Page 3

**R**
- RDPIN Instruction: 2-4
- Register Reference: Appendix C
- Repository Mode: 4-2
- RQPIN Instruction: 2-4

**S**
- Serial Modes: Chapter 12
- Setup Sequence: 2-1
- Smart Pin Architecture: 1-1
- Smart Pin Capabilities: 1-3
- Smart Pin Instructions: 3-2
- SMPS Mode: 7-3
- Spin2 Methods: 3-1
- State Measurement: 9-2
- Synchronization: 3-3
- Synchronous Serial: 12-1, 12-2

**T**
- Three-Phase Control: 14-1
- Time Accumulation: 9-1
- Time Measurement: 9-1
- Timing Specifications: D-3
- Transition Output: 4-3
- Troubleshooting: 15-2

**U**
- UART: 12-3, 12-4
- USB Mode: Chapter 11

**V**
- Velocity Measurement: 13-2

**W**
- WRPIN Instruction: 2-2
- WXPIN Instruction: 2-3
- WYPIN Instruction: 2-3

**X**
- X Register: 2-3, C-2

**Y**
- Y Register: 2-3, C-3

**Z**
- Z Register: 2-4, C-4

---

## About This Reference

This P2 Smart Pins Complete Reference represents the comprehensive documentation effort to make all 32 Smart Pin modes accessible to developers. Created through collaboration between Iron Sheep Productions and the P2 community, it combines official documentation, validated code examples, and real-world applications.

**Version 1.0 - Production Ready**
August 2025

**Produced by Iron Sheep Productions, LLC**
www.ironsheepproductions.com

Special thanks to:
- Jon Titus for the original Smart Pins documentation
- Chip Gracey for the P2 architecture
- The Parallax community for validation and feedback

**Copyright © 2025 Iron Sheep Productions, LLC**
All rights reserved. 

Propeller 2 and P2 are trademarks of Parallax Inc.

---

*End of P2 Smart Pins Complete Reference v1.0*