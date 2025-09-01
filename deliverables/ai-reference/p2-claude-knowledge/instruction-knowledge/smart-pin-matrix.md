# Smart Pin Configuration Matrix

**Purpose**: Documents Smart Pin mode compatibility and configuration dependencies.

## Configuration Sequence Dependencies

### WRPIN → WXPIN → WYPIN → DIRH Pattern
```pasm2
WRPIN   mode, pin       ' Set Smart Pin mode
WXPIN   param_x, pin    ' Configure X parameter  
WYPIN   param_y, pin    ' Configure Y parameter
DIRH    pin             ' Enable Smart Pin
```

**Critical Dependencies**:
- WRPIN must precede WXPIN/WYPIN for valid configuration
- DIRH enables Smart Pin - configuration must be complete before this
- Some modes require specific WXPIN/WYPIN parameter relationships

### Mode-Specific Configuration Requirements

**PWM Modes**:
```pasm2
WRPIN   ##P_PWM_TRIANGLE, pin
WXPIN   period, pin         ' X = period cycles
WYPIN   duty, pin           ' Y = duty (0 to period)
```

**ADC Modes**:
```pasm2
WRPIN   ##P_ADC, pin
WXPIN   sample_time, pin    ' X = sampling duration
WYPIN   #0, pin             ' Y = start conversion
```

**UART Modes**:
```pasm2
WRPIN   ##P_ASYNC_TX, pin
WXPIN   bit_period, pin     ' X = bit timing
WYPIN   data_byte, pin      ' Y = data to transmit
```

## Mode Compatibility Matrix

### Mutual Exclusions
- **Output vs Input**: Most Smart Pin modes are either output OR input, not both
- **Digital vs Analog**: ADC modes incompatible with digital output modes
- **Clock vs Data**: Clock generation modes typically incompatible with data modes

### Pin Pairing Requirements
- **Differential modes**: Some modes require adjacent pin pairs (even/odd)
- **Quadrature modes**: Encoder modes may require specific pin relationships
- **Synchronous modes**: Some modes coordinate between multiple pins

## Research Gaps - DEMO CRITICAL

### High Priority (Demo Impact)
1. **PWM mode parameter relationships** (4 hours)
   - WXPIN/WYPIN interdependencies for each PWM variant
   - Triangle vs sawtooth vs square wave configuration differences
   - Frequency and duty cycle calculation formulas

2. **ADC mode timing requirements** (3 hours)
   - Sample time parameter calculation for different ADC resolutions
   - Conversion timing vs system clock relationships
   - Multi-channel ADC coordination patterns

3. **UART parameter calculation** (2 hours)
   - Bit period calculation for standard baud rates
   - Clock frequency dependencies for timing accuracy
   - Error rates at different clock speeds

### Medium Priority (Development Important)
4. **Smart Pin mode enumeration** (6 hours)
   - Complete catalog of all Smart Pin modes with P_ constants
   - Mode-specific parameter documentation
   - Hardware capability matrix per mode

5. **Pin pairing rules** (4 hours)
   - Which modes require specific pin relationships
   - Differential pair requirements and limitations
   - Multi-pin coordination patterns

### Low Priority (Documentation Complete)
6. **Advanced configuration patterns** (8 hours)
   - Complex Smart Pin sequences for specialized applications
   - Mode switching procedures and requirements
   - Performance optimization techniques

**Total Research Required**: 27 hours
**Demo Critical Subset**: 9 hours (33% of total)

## Integration Notes

**Cross-References**:
- State Setup Matrix: WRPIN as setup instruction
- Instruction Sequence Matrix: Smart Pin configuration ordering
- COG Lifecycle Matrix: Smart Pin initialization timing

**Documentation Sources Needed**:
- Official Smart Pin documentation
- P_ constant definitions and explanations  
- Hardware reference for timing requirements
- Community examples of complex Smart Pin usage