# WMLONG vs WMLONG_ Naming Convention Resolution

## Investigation Results

### Current State
- **YAML Knowledge Base**: Has `WMLONG` instruction
- **PNUT_TS Compiler**: Has `WMLONG_` instruction (with underscore)
- **Conflict**: Different naming conventions between sources

### Technical Analysis

#### WMLONG (in YAML)
- **Syntax**: `WMLONG D,{#}S/P`
- **Encoding**: `EEEE 1010011 11I DDDDDDDDD SSSSSSSSS`
- **Description**: "Write only non-$00 bytes in D[31:0] to hub address"
- **Source**: Original P2 documentation

#### WMLONG_ (in Compiler)
- **Syntax**: `WMLONG_ D,S/#/PTRx`
- **Encoding**: Opcode 335, rawValue 31055
- **Description**: "WMLONG_ instruction"
- **Source**: PNUT_TS compiler analysis

### Key Differences
1. **Name Format**: WMLONG vs WMLONG_ (underscore suffix)
2. **Operand Syntax**: `{#}S/P` vs `S/#/PTRx` (formatting difference)
3. **Encoding**: Different bit patterns suggest these may be different instructions

### Hypothesis
These appear to be **two different instructions** rather than naming variations:

1. **WMLONG**: Original P2 instruction for selective byte writing
2. **WMLONG_**: Compiler-specific variant or alternate addressing mode

### Research Needed
To resolve definitively, need to check:
1. **P2 Silicon Documentation**: Official instruction list
2. **PNUT_TS Source Code**: Instruction definitions and comments
3. **P2 Datasheet**: Complete instruction encoding tables

## Recommended Resolution

### Short-Term (Current State)
- **Keep both instructions** as separate entities
- **Document the difference** clearly in both YAML files
- **Cross-reference** each instruction to the other

### Long-Term (Verification Required)
- **Research official P2 documentation** to determine canonical names
- **Check PNUT_TS source comments** for instruction intent
- **Verify with P2 community** if these are indeed separate instructions

## Implementation Actions

### Immediate Steps
1. **Update WMLONG.yaml** with compiler cross-reference
2. **Update WMLONG_.yaml** with YAML cross-reference  
3. **Document naming discrepancy** in both files
4. **Flag for future research** in documentation tracking

### YAML File Updates
- Add `alternate_names` field to both instructions
- Include cross-references in `related_instructions`
- Document the naming discrepancy with source attribution

## Conclusion

**Decision**: Treat as separate instructions until proven otherwise.

**Rationale**: 
- Different opcodes suggest different functionality
- Both sources are authoritative in their domains
- Safer to maintain both than to merge incorrectly

**Next Steps**: Research official P2 documentation to resolve definitively.