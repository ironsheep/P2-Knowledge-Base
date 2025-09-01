# State Setup Matrix

## Matrix Definition

**Purpose**: Document Setup→Execute instruction pairs where one instruction prepares processor state for optimal execution of subsequent instructions.

**Scope**: Instructions that modify internal P2 state to enable enhanced operation of following instructions, particularly for block operations, memory access patterns, and hardware control sequences.

**Critical For**: 
- Block data operations (SETQ family)
- Hardware initialization sequences (WRPIN family)  
- Performance optimization through state preparation
- Generating compilable vs. non-functional P2 code

---

## Instruction Categories

### 🔧 **SETQ Family - Block Operation Setup**

#### **SETQ - Set Q for Block Operations**
**Function**: Prepares Q register for block read/write operations

**Setup→Execute Patterns**:
```pasm2
SETQ    #count-1        ' Setup: Prepare for block operation
RDLONG  dest, source    ' Execute: Read 'count' longs starting at source
```

**Compatible Execute Instructions**:
- ✅ **RDLONG** - Block read from hub memory
- ✅ **WRLONG** - Block write to hub memory  
- ✅ **RDWORD** - Block read words
- ✅ **WRWORD** - Block write words
- ✅ **RDBYTE** - Block read bytes
- ✅ **WRBYTE** - Block write bytes

**Incompatible Instructions**:
- ❌ **ADD/SUB/MOV** - Arithmetic/logic operations (no block support)
- ❌ **JMP/CALL** - Control flow (no block support)
- ❌ **Smart Pin operations** - Use different setup pattern

#### **SETQ2 - Set Q for Advanced Block Operations**
**Function**: Prepares Q register for block operations with stride/addressing modes

**Setup→Execute Patterns**:
```pasm2
SETQ2   #mode           ' Setup: Advanced block operation mode
RDLONG  dest, source    ' Execute: Read with advanced addressing
```

**Status**: ⚠️ **NEEDS RESEARCH** - Specific compatible instructions and modes need documentation

### 🔌 **Smart Pin Setup Family**

#### **WRPIN - Configure Smart Pin Mode**
**Function**: Sets Smart Pin configuration register

**Setup→Execute Patterns**:
```pasm2
WRPIN   mode, pin       ' Setup: Configure pin mode
WXPIN   x_value, pin    ' Execute: Set X parameter  
WYPIN   y_value, pin    ' Execute: Set Y parameter
DIRH    pin             ' Execute: Enable pin
```

**Sequential Requirements**:
1. **WRPIN** (mode configuration) - MUST be first
2. **WXPIN** (X parameter) - Optional, depends on mode
3. **WYPIN** (Y parameter) - Optional, depends on mode  
4. **DIRH/DIRL** (enable/disable) - Activates configuration

**Status**: ⚠️ **NEEDS RESEARCH** - Mode-specific parameter requirements need documentation

### 🎯 **ALT Family - Dynamic Instruction Modification**

#### **ALTR/ALTD/ALTS - Modify Following Instruction**
**Function**: Dynamically modify register fields in the next instruction

**Setup→Execute Patterns**:
```pasm2
ALTR    new_result      ' Setup: Modify result field of next instruction
ADD     old_dest, src   ' Execute: Modified to use new_result as destination
```

**Status**: ⚠️ **NEEDS RESEARCH** - Complete field modification patterns need documentation

---

## Known Relationships

### ✅ **Documented Patterns**

#### **SETQ→Memory Operations**
- **SETQ + RDLONG**: Block read from hub memory (verified)
- **SETQ + WRLONG**: Block write to hub memory (verified)
- **Block Size**: Q register contains count-1 (0 = 1 item, 15 = 16 items)

#### **Basic Smart Pin Sequence**
- **WRPIN→DIRH**: Minimal pin activation (verified)
- **Pin State**: Must configure before enabling

### ⚠️ **Partially Documented**

#### **WXPIN/WYPIN Requirements**
- **Mode Dependency**: Some modes require X/Y parameters, others don't
- **Parameter Order**: WXPIN before WYPIN (needs verification)
- **Parameter Timing**: Can parameters be set after DIRH? (needs research)

#### **SETQ2 Advanced Modes**
- **Stride Operations**: How stride affects compatible instructions
- **Address Modes**: Which addressing patterns are supported
- **Performance Impact**: Cycle count differences vs. basic SETQ

---

## Research Gaps

### 🔍 **Critical Unknowns**

#### **SETQ/SETQ2 Compatibility Matrix**
- **Complete Instruction List**: Which instructions support SETQ setup?
- **Parameter Limits**: Maximum block sizes for different operations
- **Error Conditions**: What happens with invalid SETQ→instruction combinations?

#### **Smart Pin Mode Matrix**  
- **Mode→Parameter Mapping**: Which modes require WXPIN/WYPIN?
- **Configuration Timing**: Can parameters be changed after pin activation?
- **Error Recovery**: How to handle Smart Pin configuration errors?

#### **ALT Family Coverage**
- **Field Modification Scope**: Which instruction fields can be modified?
- **Modification Timing**: Can ALT instructions be chained?
- **Interaction with Other Setup**: How ALT interacts with SETQ/Smart Pin setup?

### 🎯 **Research Priorities**

#### **High Priority** (Demo Blocking)
1. **SETQ Compatibility List** - Essential for block operations
2. **Basic Smart Pin Sequences** - Required for hardware control
3. **Common Setup Patterns** - Most frequently used combinations

#### **Medium Priority** (Complete Understanding)
1. **SETQ2 Advanced Features** - Performance optimization
2. **ALT Family Complete Coverage** - Dynamic programming capabilities
3. **Error Condition Handling** - Robust programming patterns

#### **Low Priority** (Optimization)
1. **Performance Characteristics** - Cycle count differences
2. **Advanced Smart Pin Modes** - Specialized hardware features
3. **Multi-Setup Interactions** - Complex state preparation sequences

---

## Integration Points

### 🔗 **Cross-Matrix Dependencies**

#### **SETQ/SETQ2 Compatibility Matrix**
This matrix provides the execute instructions; SETQ matrix provides the setup patterns.

#### **Smart Pin Matrix**  
State Setup provides configuration sequence; Smart Pin Matrix provides mode details.

#### **Flag Setting Reality Matrix**
Setup instructions may affect flags that influence subsequent execution.

### 🎯 **Code Generation Rules**

#### **SETQ Usage**
```pasm2
' ✅ CORRECT: Setup before compatible instruction
SETQ    #7              ' Prepare for 8-long block operation
RDLONG  buffer, source  ' Read 8 longs

' ❌ INCORRECT: Setup before incompatible instruction  
SETQ    #7              ' Setup lost/ignored
ADD     dest, source    ' No block support - SETQ wasted
```

#### **Smart Pin Configuration**
```pasm2
' ✅ CORRECT: Configure before enable
WRPIN   ##P_ASYNC_TX, pin    ' Configure UART transmit mode
WXPIN   ##baud_value, pin    ' Set baud rate
DIRH    pin                  ' Enable pin

' ❌ INCORRECT: Enable before configure
DIRH    pin                  ' Enable with undefined configuration
WRPIN   ##P_ASYNC_TX, pin    ' Configuration may be ignored
```

---

## Validation Status

### ✅ **Verified Relationships**
- **SETQ→RDLONG/WRLONG**: Confirmed block operation behavior
- **WRPIN→DIRH**: Confirmed basic Smart Pin activation

### ⚠️ **Needs Verification**
- **SETQ→RDBYTE/WRBYTE**: Block operation behavior with bytes
- **WXPIN/WYPIN Timing**: Parameter setting order and requirements
- **SETQ2 Modes**: Advanced block operation capabilities

### ❌ **Unknown/Untested**
- **ALT Family**: Complete field modification capabilities
- **Error Conditions**: Invalid setup→execute combinations
- **Performance Impact**: Cycle count differences between patterns

---

## Matrix Status

**Completion**: 25% - Basic patterns identified, major gaps remain
**Research Priority**: Critical - Blocks AI code generation capability
**Next Steps**: 
1. Complete SETQ compatibility research
2. Document Smart Pin mode requirements  
3. Analyze ALT family modification patterns

**Integration Ready**: No - Requires completion of research gaps before reliable use