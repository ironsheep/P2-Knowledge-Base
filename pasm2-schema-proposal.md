# PASM2 Instruction Schema Standardization Plan

## Core Schema (Required Fields)

```yaml
# Required fields for ALL PASM2 instruction files
instruction: "ADD"                    # Instruction name (uppercase)
category: "arithmetic"                # Native P2 category (lowercase, no descriptions)
oneliner: "Add two unsigned values"   # Brief description for manifest
description: |                        # Full description
  ADD sums the two unsigned values...
syntax: "ADD D,{#}S {WC/WZ/WCZ}"     # Instruction syntax
encoding: "EEEE 1000000 CZI DDDDDDDDD SSSSSSSSS"  # Binary encoding
```

## Optional Standard Fields

```yaml
# Fields that appear frequently and should be standardized when present
flags_affected:                       # Z, C, or both
  z: "Set if result is zero"
  c: "Set on unsigned overflow"

operands:                             # Operand descriptions
  d: "Destination register"
  s: "Source value or register"

timing: "2 clock cycles"             # Execution time

examples:                             # Code examples
  - code: "ADD x, #1"
    description: "Increment x by 1"

see_also:                             # Related instructions (not 'related')
  - "ADDS"
  - "ADDX"
  - "SUB"
```

## Fields to Remove/Consolidate

```yaml
# Remove these duplicate/malformed fields:
group: "..."          # Remove - duplicate of category
category_full: "..."  # Remove - embedded descriptions
long_description: ""  # Consolidate into 'description'
detailed_description: # Consolidate into 'description'
related: []          # Rename to 'see_also'
```

## Implementation Plan

### Phase 1: Clean Category Fields (360 files)
1. Extract oneliner from malformed category/group fields
2. Clean category to just the type (arithmetic, logic, etc.)
3. Remove duplicate group field

### Phase 2: Standardize Optional Fields
1. Rename 'related' to 'see_also'
2. Consolidate description fields
3. Standardize operand descriptions

### Phase 3: Build Complete Manifest
1. Create entries for all 377 PASM2 files
2. Use oneliner as desc: in manifest
3. Organize by native P2 categories

## Categories to Use (from P2 native organization)

- arithmetic (38 instructions)
- logic (41 instructions)  
- bit_manipulation (23 instructions)
- memory_hub (22 instructions)
- memory_cog (10 instructions)
- control_flow (27 instructions)
- pin_control (32 instructions)
- timing_events (35 instructions)
- cordic (7 instructions)
- streamer (6 instructions)
- colorspace (7 instructions)
- interrupts (14 instructions)
- cog_control (11 instructions)
- stack_ops (6 instructions)
- special_ops (35 instructions)
- misc_ops (47 instructions)
- directives (9 items)
- constants (5 items)
- special_registers (1 item)

## Validation Rules

1. **instruction** field must match filename (minus .yaml)
2. **category** must be from approved list above
3. **oneliner** must be < 80 chars for manifest display
4. **description** must exist (can be minimal initially)
5. **syntax** must be present for instructions (not directives/constants)

## Benefits of This Schema

1. **Clean separation**: Category for organization, oneliner for discovery
2. **AI-friendly**: Short descriptions in manifest, full details on demand
3. **Maintainable**: Single source of truth for each field
4. **Extensible**: Optional fields can be added as needed
5. **Native alignment**: Uses P2's actual instruction categories