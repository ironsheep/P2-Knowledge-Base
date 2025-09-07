# Unified Field Strategy for PASM2 Instructions

## Goal
ONE authoritative field for each type of information - no duplicates, no choices.

## Field Hierarchy (Most to Least Detailed)

### 1. DESCRIPTION (Single Unified Field)
**Current Problem:**
- `description`: "Add S into D" (terse)
- `operation_result`: "Sum of unsigned Src and unsigned Dest is stored in Dest" (better)
- `detailed_explanation`: "ADD sums the two unsigned values..." (most complete)

**Solution - Single `description` Field:**
```yaml
description: |
  ADD sums the two unsigned values of Dest and Src together and stores 
  the result into the Dest register. D = D + S.
```
- Merge the detailed explanation with the formula
- Remove `operation_result` and `detailed_explanation` fields
- One place to look, no confusion

### 2. SYNTAX (Single Field)
**Current Problem:**
- `syntax`: "ADD     D,{#}S   {WC/WZ/WCZ}" (compact)
- `syntax_full`: "ADD Dest, {#}Src {WC|WZ|WCZ}" (readable)

**Solution - Enhanced Single `syntax` Field:**
```yaml
syntax: "ADD D,{#}S {WC/WZ/WCZ}"
syntax_pattern: "ADD Dest,{#}Src {WC/WZ/WCZ}"  # Only if different
```
- Keep compact form as primary
- Only add pattern if parameter names differ from D/S

### 3. CATEGORY (Single Field)
**Current Problem:**
- `group`: "Math and Logic"
- `category_detailed`: "Math Instruction - Add two unsigned values"

**Solution - Single `category` Field:**
```yaml
category: "Math and Logic"
subcategory: "Add two unsigned values"  # Optional detail
```

### 4. FLAGS (Unified Structure)
**Current Problem:**
- `flags_affected.C`: "carry of (D + S)" (formula)
- `flags_affected.C_description`: "set if 32-bit overflow" (explanation)

**Solution - Structured Flag Documentation:**
```yaml
flags_affected:
  C: 
    formula: "carry of (D + S)"
    condition: "Set if 32-bit unsigned overflow occurs"
  Z:
    formula: "(D == S)"  
    condition: "Set if result equals zero"
```

## Merge Rules

### Rule 1: Prefer Detailed Over Terse
When merging `description`:
1. Start with `detailed_explanation` if it exists
2. Add the formula from original `description` (e.g., "D = D + S")
3. Combine into single coherent description

### Rule 2: Preserve Technical Precision
Never lose:
- Encoding patterns
- Clock cycles
- Flag formulas
- Timing type (fixed/variable)

### Rule 3: Single Location Per Info Type
Each piece of information appears ONCE:
- Instruction behavior → `description`
- How to write it → `syntax`
- What category → `category`
- Parameter details → `parameters`
- Related instructions → `related`
- Flag behavior → `flags_affected` (structured)

## Implementation Plan

### Phase 1: Update Merge Script
Modify `safe-merge-manual-yaml.py` to:
1. Combine descriptions into single field
2. Structure flag documentation
3. Eliminate duplicate fields
4. Create unified output

### Phase 2: Validation Rules
Add checks to ensure:
- No `detailed_explanation` field remains
- No `operation_result` field remains  
- No `category_detailed` field remains
- All descriptions are complete sentences

### Phase 3: Final Structure
```yaml
instruction: ADD
syntax: "ADD D,{#}S {WC/WZ/WCZ}"
encoding: "EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS"
description: |
  ADD sums the two unsigned values of Dest and Src together and stores 
  the result into the Dest register. D = D + S. This instruction is 
  used for unsigned addition and sets the C flag on overflow.
category: "Math and Logic"
subcategory: "Unsigned addition"
parameters:
  - "D (Dest): Register to add to and store result"
  - "S (Src): Register or immediate value to add"
  - "WC: Update C flag with carry"
  - "WZ: Update Z flag if result is zero"
timing:
  cycles: 2
  type: fixed
flags_affected:
  C: 
    formula: "carry of (D + S)"
    condition: "Set if unsigned overflow (result > $FFFFFFFF)"
  Z:
    formula: "(result == 0)"
    condition: "Set if result equals zero"
related: [ADDX, ADDS, ADDSX, SUB]
```

## Benefits
1. **No Ambiguity**: One field per information type
2. **AI-Friendly**: Clear structure, no choice paralysis
3. **Human-Readable**: Complete descriptions with formulas
4. **Maintainable**: Clear what goes where
5. **Searchable**: Consistent field names across all instructions

## Migration Path
1. Test with 10 instructions
2. Validate no information lost
3. Apply to all 357 instructions
4. Archive old structure
5. Update any tools that consume YAMLs