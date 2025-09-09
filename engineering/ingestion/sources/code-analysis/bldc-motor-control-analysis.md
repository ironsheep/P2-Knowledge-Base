# BLDC Motor Control Analysis
*Source: P2-BLDC-Motor-Control project*  
*Files: Multiple (demo files, motor driver, configuration)*  
*Purpose: Professional BLDC motor control using P2 motor control add-on board*

## Executive Summary
This is a sophisticated BLDC (Brushless DC) motor control system demonstrating:
- Real-time motor commutation using Hall sensors
- Smart Pin PWM generation with dead-time management
- ADC-based current sensing and calibration
- Multi-motor coordination capability
- Configuration-driven architecture for different motors and voltages
- Closed-loop control with fault detection

## Architecture Overview

### System Layers
1. **Configuration Layer** (`isp_bldc_motor_userconfig.spin2`)
   - Motor type selection (6.5" wheel, 4000 RPM motor)
   - Pin group assignment (16-pin blocks)
   - Voltage configuration (6V to 25.9V)
   - Board revision detection (Rev A/B auto-detect)

2. **API Layer** (Spin2 methods)
   - High-level control: `driveAtPower()`, `stopAfterTime()`
   - State monitoring: `isReady()`, `isStopped()`
   - Parameter configuration: `setMaxSpeed()`

3. **Real-Time Control Layer** (PASM2)
   - PWM generation with dead-time
   - Hall sensor reading and commutation
   - Current sensing via ADC
   - Closed-loop position/speed control

## Key Patterns Discovered

### 1. Smart Pin PWM with Dead-Time Management
**Discovery**: Sophisticated PWM generation preventing shoot-through

```spin2
' PWM pin configuration
wrpin   pwmn, pin_pwm_u_l    ' Low side inverted
wrpin   pwmt, pin_pwm_u_h    ' High side not inverted
wxpin   fram, drive_pins     ' Set PWM frame width

' Dead-time insertion
add     drive_u_, dead_gap_  ' Low side off earlier
wypin   drive_u_, pin_pwm_u_l
sub     drive_u_, dead_gap_  ' High side on later  
wypin   drive_u_, pin_pwm_u_h
```

**Pattern**: Hardware PWM with software-controlled dead-time prevents MOSFETs from conducting simultaneously.

### 2. ADC Calibration Sequence
**Discovery**: Three-stage ADC calibration for accurate current sensing

```spin2
' Stage 1: GIO calibration
wrpin   adc_modes+0, adc_pins  ' GIO calibration mode
dirh    adc_pins
call    #.wait4adc
rdpin   gio_levels+0, pin_adc_u_i

' Stage 2: VIO calibration  
wrpin   adc_modes+1, adc_pins  ' VIO calibration mode
call    #.wait4adc
rdpin   vio_levels+0, pin_adc_u_i

' Stage 3: Calculate scaling
sub     vio_levels+0, gio_levels+0  ' Get range
qdiv    numerator, vio_levels+0      ' Calculate scale factor
```

**Pattern**: Calibrates ADC against ground and VIO for accurate measurements.

### 3. Hall Sensor Commutation
**Discovery**: Table-driven commutation with direction support

```spin2
' Read Hall sensors
testp   pin_hall_w           wc
rcl     hall_, #1
testp   pin_hall_v           wc  
rcl     hall_, #1
testp   pin_hall_u           wc
rcl     hall_, #1

' Lookup delta from table
altgb   hall_, #deltas       ' Index into delta table
getbyte tmpY
signx   tmpY, #7             ' Sign extend
add     pos_, tmpY           ' Update position
```

**Pattern**: Hall sensors provide 6-step commutation with position tracking.

### 4. Center-Aligned PWM
**Discovery**: Reduces torque ripple in motor control

```spin2
' Find min and max drive levels
mov     tmpX, drive_u_       ' Find smallest
cmps    tmpX, drive_v_       wc
if_nc   mov     tmpX, drive_v_

' Center the PWM
add     tmpX, tmpY           ' Sum min+max
sar     tmpX, #1             ' Divide by 2
sub     drive_u_, tmpX       ' Center all phases
sub     drive_v_, tmpX
sub     drive_w_, tmpX
```

**Pattern**: Centers PWM around midpoint to minimize ripple.

### 5. State Machine Architecture
**Discovery**: Sophisticated state management for motor control

```spin2
' Motor states
#10, DCS_Unknown, DCS_STOPPED, DCS_SPIN_UP, DCS_AT_SPEED
     DCS_SPIN_DN, DCS_HOLDING, DCS_FAULTED, DCS_ESTOP

' State transitions
cmp     drv_state_, #DCS_STOPPED    wz
if_z    mov     drv_state_, #DCS_SPIN_UP   ' Start ramping
```

**Pattern**: Clean state machine handles all motor operating modes.

### 6. Fault Detection
**Discovery**: Multiple fault detection mechanisms

```spin2
' Angle error fault detection
abs     tmpY, err_           ' Get absolute error
cmp     tmpY, #125       wc  ' Check if < 176 degrees
if_nc   call    #.driveoff      ' Fault: disable PWM
if_nc   mov     drv_state_, #DCS_FAULTED
```

**Pattern**: Detects impossible Hall sensor states and excessive position error.

### 7. Multi-COG Architecture
**Discovery**: Separate COGs for control and sensing

```spin2
' Start motor control COG
motorCog := wheel.start(basePin, voltage, detectMode)

' Start sensing COG
senseCog := wheel.startSenseCog()
```

**Pattern**: Distributes real-time tasks across multiple COGs.

### 8. Configuration Validation
**Discovery**: Comprehensive parameter validation

```spin2
basePin := wheel.validBasePinForChoice(user.ONLY_MOTOR_BASE)
voltage := wheel.validVoltageForChoice(user.DRIVE_VOLTAGE)
motor := wheel.validMotorForChoice(user.MOTOR_TYPE)

if basePin <> wheel.INVALID_PIN_BASE and voltage <> wheel.INVALID_VOLTAGE
    ' Safe to start motor
```

**Pattern**: Validates all configuration before enabling motor.

## Advanced Instruction Usage

### Real-Time Control Instructions
1. **TESTP** - Read Hall sensors without affecting pins
2. **RCL** - Rotate carry left for bit packing
3. **ALTGB** - Indexed byte table lookup
4. **POLLATN** - Non-blocking COG synchronization
5. **JNCT1** - Event-based loop timing
6. **WXPIN/WYPIN** - Smart Pin PWM control
7. **RDPIN** - Read ADC values
8. **CMPM** - Compare and get direction
9. **FLES/FGES** - Floating-point limits
10. **QDIV/GETQX** - Hardware division

### Smart Pin Modes Used
- PWM mode for motor phases (6 pins)
- ADC mode for current sensing (4 pins)
- Digital input for Hall sensors (3 pins)

## Performance Optimizations

### 1. Event-Driven Timing
```spin2
.loop   jnct1   #.ctlMotor   ' Wait for timer event
        jmp     #.drvMotor   ' Service motor drive
```

### 2. Block Parameter Updates
```spin2
setq    #DRVR_PARAMS_LONGS_COUNT-1
rdlong  params_ptr_+1, params_ptr_
```

### 3. Pipelined ADC Reading
- ADC runs continuously
- Synchronized with PWM period
- No polling overhead

## Motor Control Idioms for YAML

### 1. PWM Dead-Time Idiom
```yaml
idiom: "pwm_deadtime_control"
pattern: |
  add     drive, dead_gap   ' Delay low side off
  wypin   drive, pin_low
  sub     drive, dead_gap   ' Advance high side on
  wypin   drive, pin_high
```

### 2. Hall Sensor Reading Idiom
```yaml
idiom: "hall_sensor_read"
pattern: |
  testp   pin_hall_a    wc
  rcl     hall, #1
  testp   pin_hall_b    wc
  rcl     hall, #1
  testp   pin_hall_c    wc
  rcl     hall, #1
```

### 3. ADC Calibration Idiom
```yaml
idiom: "adc_calibration"
pattern: |
  wrpin   gio_mode, pins
  rdpin   gio_level, pin
  wrpin   vio_mode, pins
  rdpin   vio_level, pin
  sub     vio_level, gio_level
```

## System Integration Insights

### Board Hardware Integration
- Uses P2 motor control add-on board
- 16-pin interface per motor
- Supports dual motor configurations
- Auto-detects board revision

### Power Management
- Configurable for 6V to 25.9V operation
- Supports various battery configurations (2S-7S LiPo)
- PWM duty cycle limits based on voltage

### Safety Features
- Dead-time prevents shoot-through
- Fault detection stops motor on errors
- Emergency stop capability
- Configurable stop modes (float/brake)

## Key Takeaways for Knowledge Base

### 1. Professional Motor Control
- Complete BLDC commutation
- Closed-loop control
- Multiple safety mechanisms
- Production-ready code

### 2. Smart Pin Utilization
- PWM generation offloaded to hardware
- ADC runs autonomously
- Minimal CPU overhead for I/O

### 3. Real-Time Performance
- Deterministic control loops
- Event-driven architecture
- Multi-COG coordination

### 4. Configuration Architecture
- User-friendly configuration file
- Runtime validation
- Multiple motor/voltage support

## Recommendations for YAML Updates

### Instructions to Enhance
1. **TESTP** - Add Hall sensor reading example
2. **WXPIN/WYPIN** - Add PWM control examples
3. **RDPIN** - Add ADC reading patterns
4. **ALTGB** - Add table lookup example
5. **JNCT1** - Add event timing pattern

### New Patterns to Document
1. BLDC motor commutation
2. PWM dead-time management
3. ADC calibration sequences
4. Hall sensor processing
5. Multi-COG motor control

### Smart Pin Modes to Enhance
- PWM mode - Add motor control example
- ADC mode - Add current sensing example
- Smart Pin synchronization patterns

## Conclusion
This BLDC motor control system demonstrates professional-grade embedded control on the P2:
- Sophisticated real-time control algorithms
- Efficient use of P2's unique hardware features
- Robust fault detection and safety mechanisms
- Clean architecture with clear separation of concerns

The patterns discovered here are invaluable for understanding:
- Real-time control systems on P2
- Smart Pin usage for motor control
- Multi-COG coordination patterns
- Production-quality embedded software architecture