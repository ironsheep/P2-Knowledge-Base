# Instruction Sequence Matrix

**Purpose**: Documents critical instruction ordering dependencies and timing relationships in P2 assembly.

## Critical Sequence Dependencies

### Setup → Execute Patterns
```pasm2
' SETQ must immediately precede target instruction
SETQ    #7                  ' Setup for 8-long transfer
RDLONG  buffer, hub_addr    ' MUST be next instruction

' Smart Pin configuration sequence
WRPIN   mode, pin           ' 1. Set mode first
WXPIN   param_x, pin        ' 2. Configure X parameter
WYPIN   param_y, pin        ' 3. Configure Y parameter  
DIRH    pin                 ' 4. Enable pin last
```

### Memory Synchronization Sequences
```pasm2
' Hub memory write synchronization
WRLONG  data, hub_addr      ' Write to hub
HUBWAIT                     ' Wait for hub operation complete
RDLONG  verify, hub_addr    ' Safe to read back

' LUT coordination sequence
WRLUT   data, lut_addr      ' Write to LUT
' No explicit wait needed for LUT operations
RDLUT   verify, lut_addr    ' Immediate read is safe
```

### Flag-Dependent Sequences
```pasm2
' Flag setting followed by conditional execution
CMP     value1, value2 WZ, WC    ' Set comparison flags
IF_A    JMP #greater_label       ' Use flags immediately
' Flags remain valid until next flag-setting instruction
```

## Timing-Critical Sequences

### Clock Cycle Dependencies
```pasm2
' Instructions with multi-cycle timing
RDLONG  data, hub_addr      ' Hub access: variable timing
NOP                         ' May need delay for data valid
MOV     result, data        ' Safe to use data
```

### Pipeline Considerations
```pasm2
' Branch instruction timing
CMP     condition, threshold WZ
IF_Z    JMP #label          ' Branch may have delay slot?
        NOP                 ' Potential delay slot instruction
label   MOV     result, value   ' Branch target
```

### Interrupt-Safe Sequences
```pasm2
' Atomic operation simulation
SETI    #$FF                ' Disable interrupts (if available)
        ' Critical section
        MOV     shared_data, new_value
CLRI                        ' Re-enable interrupts (if available)
```

## Hardware Interface Sequences

### Smart Pin Operation Chains
```pasm2
' PWM configuration and start
WRPIN   ##P_PWM_TRIANGLE, pin   ' Configure PWM mode
WXPIN   period, pin             ' Set period
WYPIN   duty, pin               ' Set duty cycle
DIRH    pin                     ' Start PWM output
' PWM now running automatically
```

### ADC Sampling Sequences
```pasm2
' ADC setup and read
WRPIN   ##P_ADC, pin           ' Configure ADC mode
WXPIN   sample_time, pin       ' Set sampling duration
WYPIN   #0, pin                ' Start conversion
DIRH    pin                    ' Enable ADC
.wait   RDPIN   result, pin    ' Read result
        TEST    result, #$80000000 WZ  ' Check valid bit
IF_Z    JMP     #.wait         ' Wait until conversion complete
```

### Serial Communication Sequences
```pasm2
' UART transmit sequence
WRPIN   ##P_ASYNC_TX, pin      ' Configure TX mode
WXPIN   bit_period, pin        ' Set baud timing
DIRH    pin                    ' Enable transmitter
.send   WYPIN   byte_data, pin ' Send byte
.wait   RDPIN   status, pin    ' Check transmit status
        TEST    status, #$100 WZ   ' Test busy flag
IF_NZ   JMP     #.wait         ' Wait until not busy
```

## Research Gaps - DEMO CRITICAL

### High Priority (Demo Impact)
1. **Setup instruction timing requirements** (3 hours)
   - Exact timing between SETQ and following instruction
   - Setup instruction persistence (how long setup remains valid)
   - Interruption effects on setup sequences

2. **Hub operation timing and synchronization** (4 hours)
   - When HUBWAIT is required vs optional
   - Hub operation completion detection
   - Hub timing vs COG timing coordination

3. **Smart Pin sequence timing** (2 hours)
   - Required delays between configuration steps
   - When configuration takes effect
   - Safe timing for immediate operation after setup

### Medium Priority (Development Important)
4. **Flag persistence and invalidation** (3 hours)
   - How long flags remain valid after setting
   - Which instructions invalidate which flags
   - Safe flag usage patterns in complex sequences

5. **Branch and jump timing** (4 hours)
   - Branch delay slots and pipeline effects
   - Jump target timing and execution
   - Conditional branch performance characteristics

### Low Priority (Documentation Complete)
6. **Advanced sequence optimization** (6 hours)
   - Instruction reordering for performance
   - Parallel execution opportunities
   - Complex multi-step hardware operation coordination

**Total Research Required**: 22 hours
**Demo Critical Subset**: 9 hours (41% of total)

## Integration Notes

**Cross-References**:
- State Setup Matrix: Setup→Execute sequence patterns
- Smart Pin Matrix: Smart Pin configuration sequences
- FIFO/Queue Matrix: FIFO operation sequences
- Conditional Execution Matrix: Flag-dependent sequence patterns

**Documentation Sources Needed**:
- P2 instruction timing documentation
- Pipeline architecture details
- Hub timing and synchronization requirements
- Smart Pin timing specifications