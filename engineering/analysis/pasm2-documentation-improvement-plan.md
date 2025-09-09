# PASM2 Documentation Improvement Plan

*Created: 2025-09-09*  
*Status: Ready for execution*

## Executive Summary

Analysis of 357 PASM2 instruction YAML files reveals that 50% have minimal documentation, lacking critical information for AI code generation. We've identified ~100 instructions we can improve autonomously and ~80 requiring expert validation.

## Current State

### Documentation Coverage
- **Total Instructions**: 357
- **Comprehensive**: 175 (49%)
- **Minimal**: 179 (50%)  
- **Enhanced**: 3 (1%)

### Key Gaps Identified
1. **Missing Parameter Sections**: 179 instructions
2. **Cryptic Flag Formulas**: 120+ instructions
3. **No Related Instructions**: 170+ instructions
4. **No Usage Examples**: 350+ instructions

### Critical Priority Areas
- **Smart Pin Instructions**: 100% minimal (WRPIN, WXPIN, RDPIN, etc.)
- **CORDIC Instructions**: 100% minimal (QMUL, QDIV, QSQRT, etc.)
- **Pin Control**: 90% minimal (DRVH, DIRH, FLTL, etc.)

## Proposed Improvement Phases

### Phase I: Autonomous Documentation Generation
**Timeline**: Ready to start immediately  
**Scope**: ~100 instructions we can improve based on code analysis

#### Instructions to Document:
1. **Pin Control** (15 instructions) - HIGH confidence
   - DRVH, DIRH, DIRL, FLTL, FLTH, OUTL, OUTH
   - Conditional variants (DIRC, DRVNC, etc.)
   
2. **Smart Pins** (5 instructions) - HIGH confidence
   - WRPIN, WXPIN, RDPIN, RQPIN, AKPIN
   - Based on flash_loader and motor control patterns
   
3. **ALU Variants** (25 instructions) - HIGH confidence
   - ADDS/ADDX/ADDSX, SUBS/SUBX/SUBSX
   - NEGC/NEGNC/NEGZ/NEGNZ
   - Conditional bit operations
   
4. **Memory Operations** (10 instructions) - MEDIUM-HIGH confidence
   - RDBYTE/RDWORD, WRBYTE/WRWORD
   - RDLUT/WRLUT, GETBYTE/SETBYTE
   
5. **Branch Instructions** (15 instructions) - HIGH confidence
   - CALL variants, RET variants
   - Test-and-jump patterns
   
6. **COG Control** (8 instructions) - MEDIUM-HIGH confidence
   - COGINIT, COGSTOP, COGATN, etc.
   
7. **Lock Instructions** (4 instructions) - HIGH confidence
   - LOCKTRY, LOCKREL, LOCKNEW, LOCKRET

#### Deliverables:
- Proposed YAML documentation for each instruction
- Consistent template format
- Real code examples from production analysis
- Marked as "proposed_documentation" for review

### Phase II: Review and Ratification
**Timeline**: After Phase I completion  
**Scope**: Expert review of proposed documentation

#### Process:
1. Review proposed documentation for accuracy
2. Validate flag formulas and timing
3. Confirm examples are idiomatic
4. Ratify or request modifications
5. Merge approved documentation

#### Success Criteria:
- Technical accuracy verified
- Examples tested with compiler
- Consistent formatting confirmed
- No ambiguous descriptions

### Phase III: Expert Input Collection
**Timeline**: Concurrent with Phase II  
**Scope**: ~80 instructions requiring expert knowledge

#### Instructions Needing Expert Input:

1. **CORDIC Operations** (8 instructions)
   - Exact cycle counts (currently showing "54-55 cycles")
   - Precision specifications
   - Range limitations
   - Number formats
   
2. **Interrupt System** (12 instructions)
   - Priority levels and masking
   - Edge cases and timing
   - State preservation details
   
3. **Event System** (16 instructions)
   - Event type encodings
   - Configuration patterns
   - Timing relationships
   
4. **Streamer Details** (8 instructions)
   - SETXFRQ frequency calculations
   - NCO operation details
   - Phase accumulator behavior
   
5. **Special Registers** (Various)
   - "K" register in RET instruction
   - Modal results in smart pins
   - Hidden state machines

#### Required Information:
- Cycle-accurate timing tables
- Complete mode encoding tables
- Precision and range specifications
- Internal state machine details
- Edge case behaviors

## Implementation Resources

### Documentation Template
```yaml
instruction: INSTRUCTION_NAME
syntax: INSTRUCTION D,{#}S {WC/WZ/WCZ}
encoding: [binary encoding]
timing:
  cycles: N
  type: fixed/variable
group: Category
description: |
  Clear, comprehensive description of what the instruction does,
  when to use it, and why it's useful.
category: Specific category
parameters:
  - name: D
    description: Detailed explanation of destination operand
  - name: S
    description: Detailed explanation of source operand
flags_affected:
  C:
    formula: Clear explanation of C flag calculation
  Z:
    formula: Clear explanation of Z flag calculation
examples:
  - name: Example Name
    description: When/why to use this pattern
    code: |
      instruction operands   ' Comment
    source: Source file or pattern
related:
  - RELATED1: How it relates
  - RELATED2: How it relates
notes:
  - Important usage notes
  - Common pitfalls
  - Performance considerations
documentation_source: proposed_from_code_analysis / expert_validated
documentation_level: comprehensive
needs_validation: true/false
```

### Supporting Analysis Documents
1. **`pasm2-documentation-gap-matrix.md`** - Complete gap analysis
2. **`autonomous-improvement-candidates.md`** - Instructions we can fix
3. **Code analysis documents** - Source patterns and examples

## Success Metrics

### Phase I Success:
- 100 instructions documented
- Consistent template applied
- Real examples included
- Ready for review

### Phase II Success:
- 80%+ approval rate on first review
- All critical instructions validated
- Documentation tested with compiler

### Phase III Success:
- Expert input obtained for all unknowns
- Complete mode tables documented
- Timing specifications confirmed
- Edge cases documented

## Risk Mitigation

### Risks:
1. **Incorrect inference** - Mitigated by "proposed" marking and review
2. **Missing edge cases** - Mitigated by expert validation
3. **Inconsistent format** - Mitigated by strict template

### Contingencies:
- If inference confidence drops, mark for expert review
- If patterns conflict, document both for validation
- If examples don't compile, mark as pseudo-code

## Next Actions

1. **Approval to proceed** with Phase I
2. **Identify expert reviewers** for Phase II
3. **Prepare questions list** for Phase III
4. **Set timeline** for execution

## Notes

- This plan leverages extensive code analysis already completed
- Focuses on most-used instructions first
- Maintains clear separation between confident improvements and unknowns
- Designed for incremental progress with validation checkpoints

---

*This plan is ready for execution when resources are available. The analysis and templates are complete, awaiting only the go-ahead to begin Phase I documentation generation.*