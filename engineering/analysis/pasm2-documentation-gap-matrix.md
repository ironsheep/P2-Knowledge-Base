# PASM2 Instruction Documentation Gap Matrix

*Generated: 2025-09-09*  
*Total Instructions: 357*  
*Comprehensive: 175 (49%)*  
*Minimal: 179 (50%)*  
*Enhanced: 3 (1%)*  

## Executive Summary

This matrix identifies specific documentation gaps in PASM2 instruction YAML files. Half of our instructions have minimal documentation, missing critical information that AI systems need to generate correct code.

## Documentation Quality Levels

### Comprehensive Documentation Includes:
- ✅ Full description with context and purpose
- ✅ Clear category classification
- ✅ Parameters section with detailed explanations
- ✅ Related instructions listed
- ✅ Flags affected with clear formulas
- ✅ Examples (in enhanced docs)
- ✅ Usage notes and patterns

### Minimal Documentation Missing:
- ❌ Detailed descriptions (often cryptic/terse)
- ❌ Parameters section entirely
- ❌ Related instructions
- ❌ Clear flag formulas (often cryptic)
- ❌ Examples of usage
- ❌ Context about when/why to use
- ❌ Common patterns

## Gap Analysis by Instruction Category

### 1. Smart Pin Instructions (Critical Priority)
**Status: 100% Minimal Documentation**

| Instruction | Current Description | Missing Elements |
|------------|-------------------|------------------|
| WRPIN | "Set mode of smart pins..." | - Parameter details<br>- Mode values/meanings<br>- Pin range explanation<br>- Examples for each mode |
| WXPIN | "Set 'X' of smart pins..." | - What 'X' parameter controls<br>- Mode-dependent meanings<br>- Timing configurations<br>- Examples |
| WYPIN | "Set 'Y' of smart pins..." | ✅ ENHANCED (we fixed this) |
| RDPIN | "C = modal result" | - What results mean per mode<br>- How to interpret data<br>- Timing considerations |
| RQPIN | Missing | - Complete documentation needed |
| AKPIN | Missing | - Complete documentation needed |

**Why Critical**: Smart pins are P2's unique feature. Without proper documentation, AI cannot leverage P2's hardware acceleration capabilities.

### 2. Pin Control Instructions (High Priority)
**Status: ~90% Minimal Documentation**

| Instruction | Current State | Missing Elements |
|------------|--------------|------------------|
| DRVH | "Z = OUT bit" | - Pin range handling<br>- ADDPINS operator usage<br>- Multi-pin patterns |
| DRVL | ✅ Comprehensive | Complete |
| DIRH/DIRL | Minimal | - Direction control details<br>- Relationship to DRVx |
| FLTL/FLTH | Minimal | - Float vs drive explanation<br>- Use cases |
| OUTH/OUTL | Minimal | - OUT register interaction<br>- Difference from DRVx |

**Why High Priority**: Basic I/O is fundamental to all P2 programs.

### 3. CORDIC Instructions (High Priority)
**Status: 100% Minimal Documentation**

| Instruction | Current State | Missing Elements |
|------------|--------------|------------------|
| QMUL | "Begin CORDIC unsigned multiplication" | - Timing (54-55 cycles)<br>- Result retrieval pattern<br>- 64-bit result handling |
| QDIV | "Begin CORDIC unsigned division" | - SETQ usage for 64-bit<br>- Remainder handling<br>- Timing details |
| QSQRT | Brief | - Input range<br>- Result format<br>- Precision |
| QROTATE | Brief | - Angle format<br>- Coordinate system<br>- Result retrieval |
| QLOG/QEXP | Brief | - Number format<br>- Range limitations<br>- Accuracy |

**Why High Priority**: CORDIC provides hardware acceleration for complex math.

### 4. Streamer Instructions (High Priority)
**Status: Mixed Documentation**

| Instruction | Current State | Missing Elements |
|------------|--------------|------------------|
| XINIT | ✅ Enhanced | Complete (we fixed this) |
| XSTOP | Minimal | - When to use<br>- State after stop |
| XCONT | Minimal | - Phase preservation<br>- Use cases |
| SETXFRQ | Minimal | - Frequency calculation<br>- NCO operation |
| WAITXFI | ✅ Enhanced | Complete |

### 5. Block Transfer Instructions (Medium Priority)
**Status: Mostly Minimal**

| Instruction | Current State | Missing Elements |
|------------|--------------|------------------|
| SETQ | "Set Q to D" | - Block transfer setup<br>- Count calculation<br>- Examples |
| SETQ2 | ✅ Enhanced | Complete (we fixed this) |
| RDFAST | Minimal | - FIFO operation<br>- Alignment requirements |
| WRFAST | Minimal | - Write FIFO setup<br>- Flushing behavior |

### 6. Basic ALU Instructions (Low Priority)
**Status: Mostly Comprehensive**

Most basic math/logic instructions (ADD, SUB, AND, OR, XOR, etc.) have comprehensive documentation. However, some gaps remain:

| Instruction | Missing Elements |
|------------|------------------|
| NOT | No parameters section, brief description |
| RET | Cryptic flag formula "K[31]", no context |
| BITH | Missing description details |

## Specific Information Gaps

### 1. Missing Parameter Sections (179 instructions)
**Pattern**: Minimal docs lack parameter explanations entirely

**What's Needed**:
- Purpose of D (destination) operand
- Purpose of S (source) operand  
- Literal vs register usage
- Special encoding meanings

### 2. Cryptic Flag Formulas (120+ instructions)
**Examples**:
- "C = K[31]" - What is K?
- "C = modal result" - What modes?
- "Z = OUT bit" - Which bit?

**What's Needed**:
- Clear explanation of formula variables
- Context for when flags are meaningful
- Examples showing flag usage

### 3. Missing Related Instructions (170+ instructions)
**Impact**: AI doesn't know instruction relationships

**What's Needed**:
- Alternative instructions
- Complementary operations
- Instruction families

### 4. No Usage Examples (350+ instructions)
**Impact**: AI must guess at proper usage

**What's Needed**:
- Basic usage example
- Common patterns
- Real-world context

## Prioritized Improvement Plan

### Phase 1: Critical (Can Infer/Propose)
**These we can propose improvements for:**

1. **Smart Pin Instructions** (6 instructions)
   - We have code examples from flash_loader, motor_control
   - Can extract patterns and create documentation
   - Need validation of mode tables

2. **Pin Control Instructions** (15 instructions)
   - Simple enough to infer from context
   - Have good examples in codebase
   - Can propose complete documentation

3. **Block Transfer Setup** (4 instructions)
   - Have good examples from debugger
   - Can document patterns
   - Need validation of edge cases

### Phase 2: High Priority (Need Expert Input)
**These need external validation:**

1. **CORDIC Instructions** (8 instructions)
   - Need exact cycle counts
   - Need precision specifications
   - Need range limitations

2. **Interrupt Instructions** (12 instructions)
   - Need exact behavior details
   - Priority and masking rules
   - Edge cases

3. **Event Instructions** (16 instructions)  
   - Event types and encoding
   - Timing relationships
   - Configuration patterns

### Phase 3: Medium Priority (Can Mostly Infer)
**These we can improve with confidence:**

1. **Basic ALU Variants** (30 instructions)
   - Signed/unsigned variants
   - Carry variants
   - Can infer from base instruction

2. **Conditional Execution** (20 instructions)
   - Pattern is consistent
   - Can document systematically

## Proposed Approach

### For Instructions We Can Improve:
1. Generate proposed documentation based on:
   - Code analysis patterns
   - Instruction family similarities
   - Silicon documentation references
   - Existing comprehensive examples

2. Create standardized template with:
   - Description (clear, not cryptic)
   - Parameters (all operands explained)
   - Flags (formulas explained)
   - Examples (from real code)
   - Related (instruction family)

3. Mark as "proposed_documentation" for review

### For Instructions Needing Expert Input:
1. Create specific questions:
   - "What are the CORDIC cycle counts?"
   - "What is the K register in RET?"
   - "What are the smart pin mode encodings?"

2. Provide context:
   - What we've inferred
   - Where we're uncertain
   - What would help most

## Sample Documentation Template

```yaml
instruction: WRPIN
syntax: WRPIN   {#}D,{#}S
encoding: EEEE 1100000 0LI DDDDDDDDD SSSSSSSSS
timing:
  cycles: 2
  type: fixed
group: Smart Pins
description: |
  Configure smart pin mode and operating parameters. WRPIN sets the 
  operating mode for one or more smart pins, enabling hardware-accelerated
  I/O operations without CPU intervention.
category: Smart Pin Configuration
parameters:
  - name: D
    description: |
      32-bit mode configuration value:
      - Bits [31:24]: Pin-to-pin coupling configuration
      - Bits [23:16]: High-level mode selection
      - Bits [15:8]: Low-level mode selection  
      - Bits [7:0]: Digital filtering configuration
  - name: S
    description: |
      Pin selection (can use ADDPINS for ranges):
      - Bits [5:0]: Base pin number (0-63)
      - Bits [10:6]: Additional pins (0-31)
      - ADDPINS operator: Creates multi-pin value
flags_affected: none
examples:
  - name: SPI Clock Generation
    code: |
      wrpin   ##P_TRANSITION_OUTPUT | P_OE, #SPI_CLK
      wxpin   #1, #SPI_CLK      ' Sysclk/2
      dirh    #SPI_CLK          ' Enable
  - name: ADC Configuration  
    code: |
      wrpin   ##P_ADC_1X, #ADC_PIN
      wxpin   #%10_0111, #ADC_PIN  ' 128 samples
related:
  - WXPIN: Set X parameter
  - WYPIN: Set Y parameter  
  - RDPIN: Read result
  - DIRH: Enable smart pin
documentation_source: proposed_from_code_analysis
documentation_level: comprehensive
needs_validation: true
```

## Conclusion

**Key Findings**:
- 50% of instructions have minimal documentation
- Smart pins, CORDIC, and pin control are critical gaps
- Most gaps follow patterns we can address systematically
- ~100 instructions we can propose improvements for
- ~80 instructions need expert validation

**Recommendation**:
1. Let me generate proposed documentation for the ~100 instructions we can infer
2. Create targeted questions for expert review on the ~80 we cannot
3. Implement phased improvement starting with smart pins and pin control
4. Use standardized template for consistency

This approach maximizes our autonomous improvement capability while clearly identifying where we need expert assistance.