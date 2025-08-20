# Flag Setting Reality Matrix

## Matrix Definition

**Purpose**: Document the reality of flag modification behavior across P2 instructions - which instructions actually modify flags vs. which instructions accept WC/WZ syntax.

**Scope**: Analysis of C (Carry) and Z (Zero) flag behavior across all P2 instructions, identifying discrepancies between syntax acceptance and actual flag modification.

**Critical For**:
- Accurate flag-based conditional programming
- Understanding instruction side effects
- Generating correct flag-dependent code sequences
- Avoiding silent flag modification bugs

---

## Flag Modification Categories

### 🎯 **Explicit Flag Control Instructions**

#### **Direct Flag Modification** (Chip Clarifications 2025-08-18)
✅ **MODC** - Modify C flag based on operand test
- **Syntax**: `MODC D, S`
- **Behavior**: Tests operand and explicitly sets/clears C flag
- **Use Case**: Precise flag preparation for conditional execution

✅ **MODZ** - Modify Z flag based on operand test  
- **Syntax**: `MODZ D, S`
- **Behavior**: Tests operand and explicitly sets/clears Z flag
- **Use Case**: Zero-condition setup for conditional logic

✅ **MODCZ** - Modify both C and Z flags based on operand tests
- **Syntax**: `MODCZ D, S`  
- **Behavior**: Tests operands and sets/clears both flags
- **Use Case**: Dual-condition preparation for complex conditionals

### 🔢 **Arithmetic with Flag Control**

#### **Controlled Arithmetic Operations** (Chip Clarifications 2025-08-18)
✅ **SUMC** - Sum with carry, modify C flag
- **Syntax**: `SUMC D, S`
- **Behavior**: Addition with carry input, updates C flag
- **Use Case**: Extended precision arithmetic chains

✅ **SUMNC** - Sum with no carry, modify C flag
- **Syntax**: `SUMNC D, S`  
- **Behavior**: Addition ignoring carry input, updates C flag
- **Use Case**: Selective carry arithmetic operations

✅ **SUMZ** - Sum with zero handling, modify Z flag
- **Syntax**: `SUMZ D, S`
- **Behavior**: Addition with zero-specific behavior, updates Z flag
- **Use Case**: Zero-detection arithmetic

✅ **SUMNZ** - Sum with no zero, modify Z flag
- **Syntax**: `SUMNZ D, S`
- **Behavior**: Addition with non-zero behavior, updates Z flag  
- **Use Case**: Non-zero accumulation operations

---

## Research Categories

### ⚠️ **Syntax vs. Reality Analysis Needed**

#### **WC/WZ Syntax Acceptance**
**Research Question**: Which instructions accept WC (Write Carry) and WZ (Write Zero) syntax in their assembly format?

**Example Patterns to Investigate**:
```pasm2
ADD     dest, source WC WZ    ' Does ADD accept WC/WZ syntax?
MOV     dest, source WC       ' Does MOV accept WC syntax?
JMP     label WC              ' Does JMP accept WC syntax?
```

#### **Actual Flag Modification**
**Research Question**: Of instructions that accept WC/WZ syntax, which actually modify the flags vs. which ignore the syntax?

**Categories to Document**:
- **Syntax + Modification**: Instructions that accept WC/WZ AND modify flags
- **Syntax Only**: Instructions that accept WC/WZ but DON'T modify flags  
- **No Syntax**: Instructions that reject WC/WZ syntax entirely
- **Silent Modification**: Instructions that modify flags WITHOUT WC/WZ syntax

### 🔍 **Instruction Family Analysis**

#### **Arithmetic Instructions**
**Status**: ⚠️ **NEEDS RESEARCH**
- **ADD, SUB, MUL, DIV families**: WC/WZ behavior analysis
- **Extended operations**: ADDX, SUBX flag interaction
- **Comparison operations**: CMP, CMPS flag setting patterns

#### **Logic Instructions**  
**Status**: ⚠️ **NEEDS RESEARCH**
- **AND, OR, XOR, NOT families**: Flag modification patterns
- **Bit operations**: TESTB, BITL, BITH flag behavior
- **Shift/Rotate**: ROR, ROL, SHR, SHL flag effects

#### **Memory Operations**
**Status**: ⚠️ **NEEDS RESEARCH** 
- **Hub operations**: RDLONG, WRLONG flag interaction
- **Register operations**: MOV, MOVF flag behavior
- **Block operations**: SETQ interaction with flags

#### **Control Flow Instructions**
**Status**: ⚠️ **NEEDS RESEARCH**
- **Branch instructions**: JMP, CALL flag preservation
- **Conditional branches**: IF_ family flag testing
- **Loop instructions**: DJNZ, TJZ flag modification

---

## Known Flag Behaviors

### ✅ **Documented (Chip Clarifications 2025-08-18)**

#### **Explicit Flag Control Family**
**MODC/MODZ/MODCZ Pattern**:
- **MODC D, S**: Tests operand value → sets/clears C flag accordingly
- **MODZ D, S**: Tests operand value → sets/clears Z flag accordingly  
- **MODCZ D, S**: Tests operand values → sets/clears both C and Z flags
- **Key Insight**: Microcode-level flag control - precise conditional setup
- **Syntax**: No WC/WZ modifiers needed - flag modification is the primary function

#### **Arithmetic with Controlled Flag Updates**
**SUM* Family Flag Behavior**:
- **SUMC D, S**: Addition with carry input → updates C flag based on overflow
- **SUMNC D, S**: Addition ignoring carry input → updates C flag based on result
- **SUMZ D, S**: Addition with zero-aware behavior → updates Z flag based on result
- **SUMNZ D, S**: Addition with non-zero behavior → updates Z flag based on result
- **Key Insight**: Specialized arithmetic with explicit flag control outcomes
- **Syntax**: No WC/WZ modifiers documented - flag updates are inherent to operation

#### **Flag Modification Characteristics**
**Pattern Analysis from Chip Documentation**:
- **Deliberate Design**: These instructions exist specifically for flag manipulation
- **No Accidental Flags**: Flag changes are the intended behavior, not side effects
- **Microcode Exposure**: Provides assembly-level access to processor microcode patterns
- **Conditional Preparation**: Designed to setup flags for subsequent conditional execution

### ⚠️ **Partially Known**

#### **Traditional Arithmetic** 
- **Assumption**: ADD, SUB likely modify flags as side effect
- **Uncertainty**: Exact conditions for C/Z flag setting
- **Need**: Verification of flag-setting rules

#### **Logic Operations**
- **Assumption**: AND, OR, XOR likely affect Z flag
- **Uncertainty**: C flag behavior in logic operations  
- **Need**: Complete flag-setting specification

---

## Research Priorities

### 🎯 **Critical for Demo**

#### **Basic Arithmetic Flags**
- **ADD/SUB**: Flag modification patterns
- **CMP**: Flag setting for conditional execution
- **MOV**: Flag preservation or modification

#### **Conditional Execution Impact**
- **Flag Testing**: How IF_ family reads C/Z flags
- **Flag Preservation**: Which instructions preserve vs. modify flags
- **Chain Programming**: Flag-dependent instruction sequences

### 📊 **Systematic Analysis Needed**

#### **Complete Instruction Survey**
1. **Syntax Analysis**: Which instructions accept WC/WZ?
2. **Behavior Testing**: Which actually modify flags?
3. **Condition Documentation**: Under what conditions are flags set?
4. **Exception Identification**: Instructions with unexpected flag behavior

#### **Pattern Documentation**
- **Flag Setting Rules**: Consistent patterns across instruction families
- **Silent Modifications**: Instructions that change flags without WC/WZ
- **Preservation Patterns**: Instructions guaranteed not to modify flags

---

## Integration Points

### 🔗 **Cross-Matrix Dependencies**

#### **Conditional Execution Matrix**
Flag Setting Reality provides the flag state; Conditional Execution shows how flags are tested.

#### **State Setup Matrix**
Setup instructions may modify flags that affect subsequent instruction execution.

#### **Instruction Sequence Matrix**
Flag-setting instructions influence the behavior of following conditional instructions.

### 🎯 **Code Generation Rules**

#### **Flag-Dependent Sequences**
```pasm2
' ✅ CORRECT: Understanding flag modification
CMP     value1, value2 WC WZ  ' Sets C and Z flags based on comparison
IF_E    MOV result, #0        ' Executes if Z flag set (equal)
IF_B    MOV result, #1        ' Executes if C flag set (below)

' ❌ INCORRECT: Assuming flag preservation
CMP     value1, value2 WC WZ  ' Sets flags
ADD     temp, #1              ' May modify flags (needs research)
IF_E    MOV result, #0        ' May test wrong flag state
```

---

## Validation Requirements

### 🧪 **Testing Methodology**
1. **Syntax Testing**: Compile instructions with WC/WZ to verify syntax acceptance
2. **Runtime Testing**: Execute instructions and monitor actual flag changes  
3. **Pattern Analysis**: Identify consistent flag-setting rules
4. **Exception Documentation**: Catalog unexpected behaviors

### 📊 **Verification Status**
- **Explicit Flag Control**: ✅ Verified (7 instructions from Chip)
- **Basic Arithmetic**: ❌ Needs systematic testing
- **Logic Operations**: ❌ Needs systematic testing  
- **Memory Operations**: ❌ Needs systematic testing
- **Control Flow**: ❌ Needs systematic testing

---

## Matrix Status

**Completion**: 25% - Explicit flag control instructions fully documented from authoritative source  
**Research Priority**: High - Essential for conditional programming accuracy
**Blocking Impact**: Limits reliable conditional code generation

**Next Steps**:
1. Systematic survey of WC/WZ syntax acceptance
2. Runtime testing of actual flag modification behavior
3. Documentation of flag-setting rules and exceptions

**Integration Ready**: Partial - Explicit flag control ready, arithmetic/logic needs research