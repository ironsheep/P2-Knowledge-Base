# Mode %00010 - DAC 124Ω, 3.3V Output

## Specifications

**Function**: 16-bit digital-to-analog converter with 124Ω output impedance, 3.3V range.

**Operating Parameters**:
- Resolution: 16 bits
- Output range: 0V to 3.3V (VIO)
- Output impedance: 124Ω ±5%
- Update rate: Up to sysclock/2
- Settling time: <1µs to 0.1%
- Power consumption: 3mA typical at 1MHz update

**Mode Register Configuration**:
```
Bits 31..6: Must be zero
Bits 5..0:  %00010
```

## Configuration

**WRPIN - Mode Setup**:
Sets Smart Pin to DAC mode with 124Ω impedance.
```
Value: ##P_DAC_124R_3V | P_OE
Bits:  %0000_0000_000_10100_00_00000_0_000_00010
```

**WXPIN - Update Period**:
Sets automatic update period in system clocks. 
- 0 = Manual update only (via WYPIN)
- N = Update every N clocks

**WYPIN - Output Value**:
16-bit value determines output voltage.
- $0000 = 0V
- $8000 = 1.65V  
- $FFFF = 3.3V

**Z Register (RDPIN/RQPIN)**:
Returns current DAC value.

## Implementation

### Spin2 Example
```spin2
CON
  DAC_PIN = 20
  DAC_MODE = P_DAC_124R_3V | P_OE

PUB setup_dac() : result
  ' Configure pin 20 as 124Ω DAC
  pinstart(DAC_PIN, DAC_MODE, 0, 0)
  
PUB set_voltage(millivolts) | dacval
  ' Set output voltage (0-3300 millivolts)
  dacval := (millivolts * $FFFF) / 3300
  wypin(DAC_PIN, dacval)
  
PUB generate_sine() | angle
  ' Generate 1kHz sine wave
  repeat
    repeat angle from 0 to 359
      wypin(DAC_PIN, $8000 + (^^$8000 ** sin(angle)))
      waitus(1000/360)  ' 1kHz
```

### PASM2 Example
```pasm2
DAT
        org     0
        
dac_init
        mov     pa, ##P_DAC_124R_3V | P_OE
        wrpin   pa, #20             ' Configure pin 20 as DAC
        dirh    #20                 ' Enable DAC output
        
set_half_scale
        mov     pa, ##$8000         ' Mid-scale value
        wypin   pa, #20             ' Output 1.65V
        
generate_ramp
.loop   add     dacval, #$100       ' Increment DAC
        wypin   dacval, #20         ' Update output
        waitx   ##1000              ' Wait ~10µs @ 100MHz
        jmp     #.loop              ' Repeat forever
        
dacval  long    0
```

## Applications

**Audio Output**:
The 124Ω impedance is suitable for driving line-level audio (600Ω typical load). 
For 8Ω speakers, use external amplification.

**Control Voltages**:
Generate precise analog control signals for external circuits.
Update rate supports control loops up to 1MHz.

**Waveform Generation**:
Create arbitrary waveforms up to sysclock/2N frequency where N is samples per cycle.
32 samples/cycle allows signals up to 1.5MHz at 100MHz sysclock.

**Performance Considerations**:
- Output drives 10mA maximum
- Capacitive loads >100pF may cause instability
- Use filtering for frequencies above 1MHz
- Adjacent pin crosstalk: -40dB typical

**Known Limitations**:
- No differential output mode
- Cannot drive 50Ω loads directly
- Limited to VIO rail (typically 3.3V)
- No internal calibration