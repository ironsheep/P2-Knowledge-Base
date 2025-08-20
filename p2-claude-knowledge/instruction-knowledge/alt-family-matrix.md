# ALT Family Instruction Modification Matrix

**Purpose**: Documents ALT family instructions that modify subsequent instruction behavior in P2 assembly.

## ALT Instruction Categories

### Address Modification Instructions
```pasm2
ALTR    reg, #offset        ' Modify R field (destination) of next instruction
ALTS    reg, #offset        ' Modify S field (source) of next instruction  
ALTD    reg, #offset        ' Modify D field (destination) of next instruction
ALTI    reg, #offset        ' Modify immediate field of next instruction
```

### Combined Modification Instructions
```pasm2
ALTRS   reg1, reg2          ' Modify both R and S fields
ALTDS   reg1, reg2          ' Modify both D and S fields
ALTRDS  reg1, reg2, reg3    ' Modify R, D, and S fields (if exists)
```

### Specialized ALT Instructions
```pasm2
ALTB    reg, #bit_position  ' Modify bit field of next instruction
ALTN    reg, #count         ' Modify count/repeat field of next instruction
```

## Modification Patterns

### Dynamic Register Selection
```pasm2
' Dynamically select source register
MOV     source_select, array_index
ALTS    source_select, #array_base
MOV     result, 0-0         ' 0-0 gets replaced with actual register

' Dynamically select destination register  
MOV     dest_select, output_index
ALTD    dest_select, #output_base
MOV     0-0, computed_value ' 0-0 gets replaced with actual register
```

### Array Access Patterns
```pasm2
' Array element access using ALT
array_read:
        MOV     temp, index
        SHL     temp, #2        ' Convert to long offset
        ALTS    temp, #array_start
        MOV     result, 0-0     ' Read array[index]
        
array_write:
        MOV     temp, index  
        SHL     temp, #2        ' Convert to long offset
        ALTD    temp, #array_start
        MOV     0-0, new_value  ' Write array[index]
```

### Indirect Addressing Simulation
```pasm2
' Simulate indirect addressing
indirect_read:
        RDLONG  actual_addr, pointer_reg
        SUB     actual_addr, #$1F0      ' Convert to COG register
        ALTS    actual_addr, #0
        MOV     result, 0-0             ' Read from *pointer_reg
        
indirect_write:
        RDLONG  actual_addr, pointer_reg
        SUB     actual_addr, #$1F0      ' Convert to COG register  
        ALTD    actual_addr, #0
        MOV     0-0, new_value          ' Write to *pointer_reg
```

## ALT Instruction Constraints

### Single Instruction Effect
```pasm2
' ALT only affects the IMMEDIATELY following instruction
ALTS    source_reg, #offset
MOV     result, 0-0         ' ✅ Modified by ALTS
MOV     other, 0-0          ' ❌ NOT modified - uses literal 0
```

### Instruction Type Limitations
```pasm2
' Not all instructions can be modified by ALT
ALTS    source_reg, #offset  
ADD     result, 0-0         ' ✅ ALT can modify ADD operands
JMP     #0-0                ' ❌ ALT cannot modify jump targets
NOP                         ' ❌ ALT has no effect on NOP
```

### Register Range Constraints
```pasm2
' ALT modifications must result in valid register numbers
ALTS    #$1FF, #0           ' ✅ Valid COG register range
ALTS    #$400, #0           ' ❌ Beyond COG register space
ALTD    base_reg, index     ' Must ensure base_reg + index is valid
```

## Advanced ALT Patterns

### Loop Optimization with ALT
```pasm2
' Optimized array processing loop
array_process:
        MOV     index, #0
        MOV     count, #array_size
        
.loop   ALTS    index, #array_base     ' Select source element
        ALTD    index, #result_base    ' Select dest element
        MOV     0-0, 0-0               ' Copy with processing
        
        ADD     index, #1
        DJNZ    count, #.loop
```

### Table-Driven Operations
```pasm2
' Table-driven instruction modification
lookup_operation:
        RDLONG  operation_code, ##@operation_table
        ALTI    operation_code, #0      ' Modify immediate field
        ADD     result, #0-0            ' Operation code inserted here
```

### State Machine Implementation
```pasm2
' State machine using ALT for dynamic dispatch
state_machine:
        ALTS    current_state, #state_table_base
        MOV     next_state, 0-0         ' Load next state
        
        ALTS    current_state, #handler_table_base  
        JMP     0-0                     ' Jump to state handler
```

## Research Gaps - DEMO CRITICAL

### High Priority (Demo Impact)
1. **Complete ALT instruction enumeration** (3 hours)
   - All ALT family instructions and their specific functions
   - Field modification capabilities for each ALT variant
   - Syntax and encoding for ALT instructions

2. **ALT modification limitations** (2 hours)
   - Which instruction types can/cannot be modified by ALT
   - Register range constraints and validation
   - Error conditions and undefined behavior

3. **Performance characteristics** (2 hours)
   - Performance cost of ALT instructions vs direct addressing
   - ALT instruction timing and pipeline effects
   - Optimization strategies for ALT-heavy code

### Medium Priority (Development Important)
4. **Complex ALT patterns** (4 hours)
   - Multi-field modification techniques
   - ALT coordination with other P2 features
   - Error handling for invalid ALT modifications

5. **Debugging ALT-modified code** (3 hours)
   - How debuggers handle ALT-modified instructions
   - Visualization of dynamic instruction modification
   - Debugging strategies for ALT-based algorithms

### Low Priority (Documentation Complete)
6. **Advanced ALT applications** (5 hours)
   - Compiler optimization using ALT instructions
   - Dynamic code generation techniques
   - ALT-based interpreter implementations

**Total Research Required**: 19 hours
**Demo Critical Subset**: 7 hours (37% of total)

## Integration Notes

**Cross-References**:
- Instruction Sequence Matrix: ALT instruction timing and ordering
- Conditional Execution Matrix: ALT with conditional execution
- COG Lifecycle Matrix: ALT usage in dynamic COG programming

**Documentation Sources Needed**:
- Complete ALT family instruction reference
- P2 instruction encoding documentation for ALT modifications
- Performance characteristics of dynamic instruction modification
- Examples of ALT usage in optimized P2 algorithms