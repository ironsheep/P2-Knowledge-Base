# Spin2 Coding Reference for Smart Pins Documentation

## Purpose
This is the authoritative reference for writing correct Spin2 code examples in P2 documentation, especially Smart Pins tutorials. Based on comprehensive study of Spin2 v51 documentation.

## Critical Documents to Read (in priority order)

### 1. For Spin2 Language Rules
**PRIMARY**: `/engineering/ingestion/sources/spin2-v51/spin2-grammar-reference.md`
- Complete syntax and structure rules
- Block types (CON, OBJ, VAR, PUB, PRI, DAT)
- Indentation requirements (critical!)
- Method signatures and return values

### 2. For SmartPin Programming
**PRIMARY**: `/engineering/ingestion/sources/spin2-v51/complete-builtin-symbols.md`
- ALL 59 SmartPin configuration symbols
- Correct symbol names and usage
- Shows how to compose readable configurations

**REFERENCE**: `/engineering/ingestion/sources/spin2-v51/spin2-builtin-symbols-tables.md`
- Quick lookup tables for all symbols
- SmartPin modes table (all 32 modes)

### 3. For Inline PASM
**REFERENCE**: `/engineering/ingestion/sources/spin2-v51/spin2-pasm-integration-deep-dive.md`
- How to embed PASM in Spin2 methods
- Automatic variable synchronization rules
- ORG/END requirements

## Key Rules for Smart Pins Code Examples

### 1. Basic Spin2 Structure Requirements
```spin2
CON
  ' Constants must be defined in CON block
  _clkfreq = 200_000_000    ' Clock frequency
  
  PIN_LED = 56              ' Pin assignments
  
PUB main()
  ' Every Spin2 program needs at least one PUB method
  ' First PUB is the entry point
  
PRI helper()
  ' Private methods use PRI
```

### 2. SmartPin Configuration - ALWAYS Use Symbols
```spin2
' ❌ WRONG - Never use raw bit patterns:
PINSTART(56, %0001_0000_000_0000000000000_00_10100_0, 10000, 5000)

' ✅ CORRECT - Always use symbolic constants:
PINSTART(56, P_OE | P_PWM_TRIANGLE, 10000, 5000)
```

### 3. Complete SmartPin Setup Pattern
```spin2
PUB setup_smartpin(pin, mode, x_val, y_val)
  PINCLEAR(pin)                    ' Always clear first
  WRPIN(pin, mode)                  ' Set mode using symbols
  WXPIN(pin, x_val)                ' Configure X parameter
  WYPIN(pin, y_val)                ' Configure Y parameter  
  PINLOW(pin)                       ' Set initial state
  DIRH(pin)                         ' Enable SmartPin
```

### 4. Symbol Composition Examples
```spin2
' PWM with specific input configuration
mode := P_OE | P_PWM_TRIANGLE | P_MINUS1_B

' Async serial with inverted input
mode := P_ASYNC_TX | P_INVERT_A

' ADC with filtering
mode := P_ADC_SCOPE | P_FILT2_AB
```

### 5. Common SmartPin Patterns
```spin2
' PWM Output
PINSTART(pin, P_OE | P_PWM_TRIANGLE, period, duty)

' Servo Control  
PINSTART(pin, P_OE | P_PULSE, pulse_period, pulse_width)

' Quadrature Decoder
PINSTART(pin, P_QUADRATURE, 0, 0)
position := RDPIN(pin)

' Frequency Counter
PINSTART(pin, P_COUNT_RISES, sample_period, 0)
count := RDPIN(pin)
```

### 6. Indentation is SEMANTIC (Critical!)
```spin2
' Indentation determines block scope - NOT decorative!
PUB method() : result | local
  if condition              ' 2 spaces
    action1()              ' 4 spaces (inside if)
    action2()              ' 4 spaces (inside if)
  other_action()           ' 2 spaces (after if)
```

### 7. Method Signatures
```spin2
' With return value
PUB method_name() : return_value
  return_value := 42

' With parameters and locals
PUB method_name(param1, param2) : result | local1, local2
  local1 := param1 + param2
  result := local1 * 2

' Multiple return values
PUB get_xy() : x, y
  x := 100
  y := 200
```

## Common Mistakes to Avoid

1. **Raw bit patterns** - Always use symbol names
2. **Wrong indentation** - It changes program meaning!
3. **Missing PINCLEAR()** - Always clear before setup
4. **Forgetting P_OE** - Output enable needed for output modes
5. **Wrong symbol names** - Check exact names in reference
6. **No CON block** - Constants belong in CON, not in methods

## Symbol Categories Quick Reference

### SmartPin Input Selection
- `P_LOCAL_A/B` - Local pin
- `P_PLUS1_A/B` through `P_PLUS3_A/B` - Neighboring pins
- `P_MINUS1_A/B` through `P_MINUS3_A/B` - Other neighbors
- `P_TRUE_A/B` or `P_INVERT_A/B` - Polarity

### SmartPin Modes (use exact names!)
- `P_PWM_TRIANGLE` - Triangle wave PWM
- `P_PWM_SAWTOOTH` - Sawtooth PWM
- `P_PULSE` - Pulse/cycle output
- `P_TRANSITION` - Transition output
- `P_NCO_FREQ` - NCO frequency mode
- `P_NCO_DUTY` - NCO duty mode
- `P_QUADRATURE` - Quadrature decoder
- `P_ASYNC_TX` - Async serial transmit
- `P_ASYNC_RX` - Async serial receive
[etc. - see complete list in builtin-symbols.md]

### Output Control
- `P_OE` - Output enable (REQUIRED for outputs)
- `P_FLOAT` - High-impedance output

## Testing Your Code Examples

Before including in documentation:
1. Verify all symbol names exist in `complete-builtin-symbols.md`
2. Check indentation carefully (use spaces, not tabs)
3. Ensure every program has a PUB method
4. Test with pnut_ts compiler if possible

## Additional Resources

- **Conceptual Understanding**: `/engineering/ingestion/sources/spin2-v51/spin2-conceptual-framework.md`
- **Language Comparisons**: `/engineering/ingestion/sources/spin2-v51/spin2-comparative-analysis.md`
- **Method Pointers**: `/engineering/ingestion/sources/spin2-v51/spin2-method-pointers-send-recv.md`

---

**INSTRUCTION FOR OPUS**: Read this document first, then refer to the detailed documents listed above as needed. Focus on using symbolic constants for ALL SmartPin configurations to ensure readable, maintainable code examples.