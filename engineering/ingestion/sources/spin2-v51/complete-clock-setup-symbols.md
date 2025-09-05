# Complete Clock Setup Symbols Reference - ALL MODES

## Critical Understanding
Clock setup determines P2 performance, power consumption, and peripheral operation. These symbols configure the complex clock system without dealing with raw bit patterns.

---

## COMPLETE Clock Source Symbols

### Primary Clock Sources
```spin2
RCFAST             ' Internal RC oscillator ~20-24 MHz (default at boot)
RCSLOW             ' Internal RC oscillator ~20 KHz (low power)
XI                 ' External crystal/oscillator input
XO                 ' External crystal output (with XI forms crystal circuit)
PLL                ' Phase-locked loop output
```

---

## COMPLETE Crystal Oscillator Symbols

### Crystal Frequency Divider (Pre-PLL)
```spin2
XDIV1              ' Crystal divide by 1
XDIV2              ' Crystal divide by 2
XDIV4              ' Crystal divide by 4
XDIV8              ' Crystal divide by 8
XDIV16             ' Crystal divide by 16
XDIV32             ' Crystal divide by 32
XDIV64             ' Crystal divide by 64
```

### Crystal Drive Strength Selection
```spin2
XSEL0              ' Lowest power drive (<10 MHz crystals)
XSEL1              ' Low power drive (10-20 MHz crystals)
XSEL2              ' Medium power drive (15-30 MHz crystals)
XSEL3              ' High power drive (25-60 MHz crystals)
```

### Crystal Capacitance Settings
```spin2
' Automatic based on frequency:
' If _xtlfreq >= 16_000_000: 15pF per pin
' If _xtlfreq < 16_000_000:  30pF per pin
```

---

## COMPLETE PLL Multiplier Symbols

### VCO Multiplier Settings (Partial List - Full Range)
```spin2
XMUL1              ' VCO multiply by 1
XMUL2              ' VCO multiply by 2
XMUL3              ' VCO multiply by 3
XMUL4              ' VCO multiply by 4
XMUL5              ' VCO multiply by 5
XMUL6              ' VCO multiply by 6
XMUL7              ' VCO multiply by 7
XMUL8              ' VCO multiply by 8
XMUL9              ' VCO multiply by 9
XMUL10             ' VCO multiply by 10
XMUL11             ' VCO multiply by 11
XMUL12             ' VCO multiply by 12
XMUL13             ' VCO multiply by 13
XMUL14             ' VCO multiply by 14
XMUL15             ' VCO multiply by 15
XMUL16             ' VCO multiply by 16
XMUL20             ' VCO multiply by 20
XMUL24             ' VCO multiply by 24
XMUL25             ' VCO multiply by 25
XMUL30             ' VCO multiply by 30
XMUL32             ' VCO multiply by 32
XMUL40             ' VCO multiply by 40
XMUL48             ' VCO multiply by 48
XMUL50             ' VCO multiply by 50
XMUL60             ' VCO multiply by 60
XMUL64             ' VCO multiply by 64
XMUL80             ' VCO multiply by 80
XMUL96             ' VCO multiply by 96
XMUL100            ' VCO multiply by 100
XMUL128            ' VCO multiply by 128
XMUL200            ' VCO multiply by 200
XMUL256            ' VCO multiply by 256
XMUL512            ' VCO multiply by 512
XMUL1024           ' VCO multiply by 1024 (maximum)
' ... continues for ALL values 1-1024
```

---

## COMPLETE PLL Configuration Symbols

### PLL Post-Divider Settings
```spin2
XPPPP              ' PLL post-divider value (1-64)
' Encoded as: (divider - 1) in bits [4:0]
' Examples:
'   %00000 = divide by 1
'   %00001 = divide by 2
'   %11111 = divide by 32
'   %111111 = divide by 64
```

### Crystal Pre-Divider (for PLL)
```spin2
XDIVP              ' Crystal pre-divider for PLL (1-64)
' Reduces crystal frequency before PLL
' Helps achieve PFD frequency requirements
```

### PLL Multiplier (Fine Control)
```spin2
XMULP              ' PLL multiplier value (1-1024)
' Actual VCO frequency = (XI / XDIVP) * XMULP
```

### PLL Filter Settings
```spin2
XPLLN              ' PLL loop filter value (0-15)
' Controls PLL bandwidth and stability
' Higher values = narrower bandwidth
' %0000 = widest bandwidth
' %1111 = narrowest bandwidth
```

---

## Clock Configuration Constants

### Configuration Declaration Patterns
```spin2
CON
  ' Method 1: Specify target frequency, auto-calculate PLL
  _clkfreq = 200_000_000      ' Desired frequency
  _errfreq = 1_000_000        ' Acceptable error (optional, default 1MHz)
  
  ' Method 2: Specify crystal and target frequencies  
  _xtlfreq = 20_000_000       ' Crystal frequency
  _clkfreq = 200_000_000      ' Desired frequency
  _errfreq = 100_000          ' Acceptable error
  
  ' Method 3: External clock input
  _xinfreq = 10_000_000       ' External clock frequency
  _clkfreq = 200_000_000      ' Desired frequency
  
  ' Method 4: Use crystal directly (no PLL)
  _xtlfreq = 20_000_000       ' Crystal frequency only
  
  ' Method 5: Use internal oscillators
  _rcfast                     ' Use RCFAST (~20-24 MHz)
  _rcslow                     ' Use RCSLOW (~20 KHz)
```

---

## Compiler-Generated Symbols

### Automatic Clock Symbols
```spin2
clkmode_           ' Compiled clock mode value (compiler-generated)
clkfreq_           ' Compiled clock frequency (compiler-generated)
```

### Runtime Clock Variables (Hub RAM)
```spin2
clkmode            ' Current clock mode at LONG[$40]
clkfreq            ' Current clock frequency at LONG[$44]
```

---

## Clock Mode Bit Structure

### HUBSET Clock Mode Format
```
%PPPP_CC_SS
Where:
  PPPP = PLL settings
  CC = Clock source select:
    %00 = RCFAST
    %01 = RCSLOW  
    %10 = Crystal/External
    %11 = PLL
  SS = Crystal/External settings
```

### Detailed Bit Fields
```
%0000_00EE_DDDDDD_MMMMMMMMMM_PPPP_CC_SS
  E = Enable crystal/external (2 bits)
  D = Crystal divider (6 bits)
  M = PLL multiplier (10 bits)
  P = PLL post-divider (4 bits)
  C = Clock source (2 bits)
  S = Settings (2 bits)
```

---

## Clock Setup Examples

### Example 1: 200 MHz from 20 MHz Crystal
```spin2
CON
  _clkfreq = 200_000_000
  _xtlfreq = 20_000_000
  
' Compiler calculates: 20MHz/1 * 10 / 1 = 200MHz
' Uses: XDIV1, XMUL10, post-div 1
```

### Example 2: 297 MHz from 20 MHz Crystal
```spin2
CON  
  _xtlfreq = 20_000_000
  _clkfreq = 297_000_000
  _errfreq = 500_000
  
' Compiler finds closest: 20MHz/2 * 30 / 1 = 300MHz
' Within error tolerance
```

### Example 3: External 10 MHz Input
```spin2
CON
  _xinfreq = 10_000_000
  _clkfreq = 180_000_000
  
' 10MHz * 18 / 1 = 180MHz
```

### Example 4: Low Power Mode
```spin2
CON
  _rcslow            ' ~20 KHz operation
  
' Ultra-low power, slow operation
```

---

## Runtime Clock Changes

### Safe Clock Change Procedure
```spin2
PUB change_clock(new_mode, new_freq)
  ' Method 1: Using CLKSET (safest)
  CLKSET(new_mode, new_freq)
  
  ' Method 2: Manual (PASM or advanced use)
  HUBSET(new_mode & !%11)    ' Start crystal/PLL, stay in RCFAST
  WAITX(20_000_000/100)       ' Wait 10ms for stability
  HUBSET(new_mode)            ' Switch to new clock
```

### PASM Clock Setup
```pasm
' For PASM-only programs
ASMCLK                      ' Sets clock per CON declarations
' Or manual:
HUBSET  ##clkmode_ & !%11   ' Start external, stay RCFAST
WAITX   ##20_000_000/100    ' Wait 10ms
HUBSET  ##clkmode_          ' Switch to external
```

---

## Critical Clock Rules

### VCO (Voltage Controlled Oscillator) Limits
```spin2
' VCO frequency = (Crystal / XDIVP) * XMULP
' MUST be between 100 MHz and 350 MHz
' Example: 20MHz * 10 = 200 MHz VCO (valid)
```

### PFD (Phase Frequency Detector) Limits  
```spin2
' PFD frequency = Crystal / XDIVP
' MUST be between 250 KHz and 28.3 MHz
' Example: 20MHz / 1 = 20 MHz PFD (valid)
```

### Crystal Drive Selection Rules
```spin2
' Match XSEL to crystal frequency:
XSEL0  ' Use for crystals < 10 MHz
XSEL1  ' Use for crystals 10-20 MHz
XSEL2  ' Use for crystals 15-30 MHz
XSEL3  ' Use for crystals 25-60 MHz
```

### Clock Glitch Prevention
```spin2
' ALWAYS update frequency first when increasing speed:
WRLONG new_freq, #$44       ' Update frequency
HUBSET new_mode             ' Then change mode

' ALWAYS update mode first when decreasing speed:
HUBSET new_mode             ' Change mode
WRLONG new_freq, #$44       ' Then update frequency
```

---

## Special Clock Modes

### DEBUG Mode Clock
```spin2
' When DEBUG is enabled and no clock specified:
' Automatically uses 20 MHz crystal mode
' Ensures DEBUG communication works
```

### Boot Clock
```spin2
' P2 always boots in RCFAST mode (~20-24 MHz)
' Your code must switch to desired clock
```

### Clock Failure Recovery
```spin2
' If PLL fails to lock or crystal stops:
' P2 automatically falls back to RCFAST
' Check clkmode to detect this condition
```

---

## Why Clock Symbols Matter

### Without Symbols:
```spin2
HUBSET ##%0000_0001_100111_0001100100_0001_10_11  ' What does this do?
```

### With Symbols:
```spin2
CON
  _xtlfreq = 20_000_000
  _clkfreq = 200_000_000
  ' Clear, self-documenting intention
```

The clock system is the foundation of P2 operation. These symbols make it accessible and maintainable, preventing timing errors and ensuring reliable operation across the full performance range from 20 KHz to 350+ MHz.