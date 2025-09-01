# Pin Selection Guide for P2 Examples

**Created**: 2025-08-20  
**Purpose**: Ensure examples use appropriate pins that avoid conflicts and confusion  
**Critical**: Examples shape understanding - choose pins wisely

## 🚫 Pins to AVOID in Examples

### High Pins (56-63) - Board-Specific Functions
```
P56-P63: Often reserved for:
- On-board LEDs (P2 Eval: 56-63)
- Boot functions
- Serial communication
- Special hardware features
```
**Why avoid**: Conflict with board features, confusing for beginners

### Very Low Pins (0-3) - Potential Confusion
```
P0-P1: Could be confused with:
- Boolean values (0/1)
- Array indices
- Loop counters
```
**Why avoid**: Cognitive interference with other programming concepts

### Special Function Pins
```
P28-P31: Often used for:
- I2C communication
- Serial boot
- Programming interface
```
**Why avoid**: May interfere with development tools

## ✅ RECOMMENDED Pins for Examples

### Primary Teaching Pins
```pasm2
' Best choices for examples:
LED_PIN         = 16    ' Clearly a pin number
BUTTON_PIN      = 17    ' Adjacent for paired examples
SENSOR_PIN      = 24    ' Another clear pin
OUTPUT_PIN      = 32    ' Power of 2, memorable

' Good alternatives:
DATA_PIN        = 8     ' Simple, clear
CLOCK_PIN       = 9     ' Good for serial examples
ENABLE_PIN      = 12    ' Round number
```

### Why These Work
1. **Clearly pin numbers** - No confusion with other values
2. **Middle range** - Away from special functions
3. **Memorable** - Round numbers or powers of 2
4. **Safe** - Unlikely to conflict with board features

## 📚 Pedagogical Pin Progression

### Chapter 1: First Examples
```pasm2
' Start with a clear, safe pin
        drvh    #16             ' LED on pin 16
        waitx   ##25_000_000    
        drvl    #16             ' LED off
```
**Note in text**: "We're using pin 16 for our LED. You can connect an LED with a resistor to this pin, or change the number to match your board's LED pin (often 56-63)."

### Chapter 2: Multiple Pins
```pasm2
' Use sequential pins for clarity
LED_A   = 16
LED_B   = 17
LED_C   = 18
```

### Chapter 8: Smart Pins
```pasm2
' Use descriptive middle-range pins
TX_PIN  = 24    ' UART transmit
RX_PIN  = 25    ' UART receive
PWM_PIN = 32    ' PWM output
ADC_PIN = 33    ' Analog input
```

## 🔄 Migration from Board LEDs

### Teaching Strategy
When readers need to use board LEDs, show the transition:

```pasm2
' Generic example (works with external LED):
MY_LED  = 16            ' Connect LED to pin 16

' For P2 Eval board built-in LED:
' MY_LED = 56          ' Uncomment for P2 Eval board

' For P2 Edge with LED on different pin:
' MY_LED = 38          ' Uncomment for P2 Edge
```

## 📝 Example Update Checklist

### Current Usage Review
- [x] Chapter 1: Uses pin 56 (board LED) - **NEEDS UPDATE**
- [ ] Chapter 2: Check all examples
- [ ] Chapter 8: Smart Pins examples
- [ ] All other chapters

### Recommended Changes
1. **Chapter 1**: Change from pin 56 to pin 16
   - Add note about board LEDs
   - Explain pin choice
   
2. **Throughout**: Use consistent pin numbering
   - LED examples: 16-19
   - Serial examples: 24-25
   - PWM examples: 32-33

## 🎯 Pin Selection Rules

### Rule 1: Clarity Over Convenience
Better to require an external LED than confuse with board-specific pins

### Rule 2: Consistency Builds Memory
Use same pins across related examples

### Rule 3: Document Alternatives
Always mention how to adapt for specific boards

### Rule 4: Middle Range is Safe Range
Pins 8-47 are generally safe across all P2 boards

## 📋 Standard Pin Assignments for Manual

```pasm2
' Standard pins for all examples (unless specifically noted):
LED_BASE        = 16    ' LEDs on 16-19
BUTTON_BASE     = 20    ' Buttons on 20-23
SERIAL_BASE     = 24    ' Serial on 24-27
PWM_BASE        = 32    ' PWM on 32-35
SENSOR_BASE     = 40    ' Sensors on 40-43

' Reserve for special examples:
' 56-63: Board-specific (document when used)
' 0-7:   Avoid unless necessary
' 48-55: Available for expansion
```

## 🔍 Quick Reference (Updated 2025-08-20)

**Universal Safe (ALL boards)**: 0-37  
**Standard boards only**: 38-55  
**LED pins (buffered)**: 56-57 (standard), 38-39 (RAM board)  
**NEVER USE**: 58-63 (SPI flash & programming)  

### Board-Specific Reality:
- **Standard P2 boards**: Can use 0-55 + LEDs with care (56-57)
- **#P2-EC32MB (RAM)**: Can use 0-37 + LEDs with care (38-39)
- **All boards**: 58-63 reserved for boot/programming

---

*"Good examples teach concepts, not board quirks"*