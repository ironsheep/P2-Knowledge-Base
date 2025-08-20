# Conditional Execution Matrix

**Purpose**: Documents P2 conditional execution patterns and flag-based control flow.

## Conditional Execution Modifiers

### Standard Condition Codes
```pasm2
IF_C    MOV dest, source    ' Execute if C flag set
IF_NC   MOV dest, source    ' Execute if C flag clear
IF_Z    MOV dest, source    ' Execute if Z flag set  
IF_NZ   MOV dest, source    ' Execute if Z flag clear
```

### Combined Condition Codes
```pasm2
IF_C_AND_Z      MOV dest, source    ' Execute if both C and Z set
IF_C_AND_NZ     MOV dest, source    ' Execute if C set and Z clear
IF_NC_AND_Z     MOV dest, source    ' Execute if C clear and Z set
IF_NC_AND_NZ    MOV dest, source    ' Execute if both C and Z clear
```

### Specialized Condition Codes
```pasm2
IF_A    MOV dest, source    ' Execute if above (unsigned >)
IF_AE   MOV dest, source    ' Execute if above/equal (unsigned >=)
IF_B    MOV dest, source    ' Execute if below (unsigned <)
IF_BE   MOV dest, source    ' Execute if below/equal (unsigned <=)
```

## Flag Setting Patterns

### Explicit Flag Control
```pasm2
' Set flags explicitly
CMP     value1, value2 WZ, WC    ' Compare and set Z, C flags
TEST    value, mask WZ           ' Test bits and set Z flag
MOV     dest, source WZ          ' Move and set Z flag based on result
```

### Implicit Flag Setting
```pasm2
' Instructions that automatically affect flags
ADD     dest, source             ' Affects C flag on overflow
SUB     dest, source             ' Affects C and Z flags
SHL     dest, source             ' C flag gets shifted-out bit
```

### Flag Preservation
```pasm2
' Instructions that don't affect flags
MOV     dest, source             ' No flags affected (without WZ)
NOP                              ' No flags affected
JMP     #label                   ' No flags affected
```

## Complex Conditional Patterns

### Branching Chains
```pasm2
CMP     value, #100 WZ, WC
IF_A    JMP #greater_than_100
IF_Z    JMP #equals_100  
        ' Fall through for less than 100
```

### Conditional Flag Modification
```pasm2
' Conditional flag setting based on existing flags
IF_C    MODC   result, test_value    ' Modify C flag conditionally
IF_NZ   MODZ   result, test_value    ' Modify Z flag conditionally
```

### Multi-Instruction Conditional Blocks
```pasm2
CMP     condition, threshold WZ
IF_NZ   MOV     temp, value1
IF_NZ   ADD     temp, value2  
IF_NZ   MOV     result, temp
```

## Research Gaps - DEMO CRITICAL

### High Priority (Demo Impact)
1. **Complete condition code enumeration** (2 hours)
   - All available IF_* condition codes
   - Condition code combinations and their meanings
   - Signed vs unsigned comparison condition codes

2. **Flag interaction patterns** (3 hours)
   - Which instructions affect which flags automatically
   - How WZ and WC modifiers change flag behavior
   - Flag preservation rules across instruction sequences

3. **Conditional execution performance** (2 hours)
   - Performance cost of conditional vs unconditional execution
   - Branch prediction behavior (if any)
   - Optimization patterns for conditional code

### Medium Priority (Development Important)
4. **Complex conditional logic** (4 hours)
   - Multi-condition evaluation techniques
   - Conditional flag setting patterns
   - Nested conditional execution strategies

5. **Comparison instruction variants** (3 hours)
   - CMP vs CMPS vs other comparison instructions
   - Signed vs unsigned comparison semantics
   - Efficient comparison patterns for different data types

### Low Priority (Documentation Complete)
6. **Advanced conditional patterns** (5 hours)
   - State machine implementation using conditional execution
   - Complex branching optimization techniques
   - Conditional execution in loops and algorithms

**Total Research Required**: 19 hours
**Demo Critical Subset**: 7 hours (37% of total)

## Integration Notes

**Cross-References**:
- Flag Setting Reality Matrix: Relationship between flag setting and conditional execution
- Event System Matrix: Event-based conditional execution
- Instruction Sequence Matrix: Conditional execution timing and dependencies

**Documentation Sources Needed**:
- Complete P2 condition code reference
- Flag behavior documentation for all instructions
- Performance characteristics of conditional execution
- Assembly optimization guides for conditional code