# P2 Opcode Matrix - p2docs.github.io

**Source**: https://p2docs.github.io/p2_opmatrix.html  
**Import Date**: 2025-08-15  
**Verification Status**: 🟡 NEEDS VERIFICATION - Community source, requires validation against official P2 specifications  
**Purpose**: Instruction encoding reference for ADA emulation projects

## ⚠️ Verification Requirements

Critical verification needed for:
- Opcode bit patterns and encoding accuracy
- Special sub-opcode mappings
- Instruction grouping correctness

## Opcode Matrix Structure

**Format**: 8x8 grid representing instruction encodings
- **First 3 bits** (xxxx000 to xxxx111): Least significant bits
- **Next 3 bits** (0000xxx to 1111xxx): Most significant bits

### Instruction Categories by Encoding

#### Arithmetic Operations
- ADD, SUB, CMP groupings
- Mathematical operations clustering

#### Bit Manipulation
- AND, OR, XOR operations
- Logical instruction patterns

#### Shifts and Rotates  
- SHL, SHR, ROL, ROR encodings
- Bit movement operations

#### Memory Operations
- RDLONG, WRLONG patterns
- Hub RAM access instructions

#### Branch and Control
- JMP, CALL encodings
- Control flow instructions

### Special Sub-Opcode Section

**1101011 Opcode Group**: Extended instruction encoding
- Additional bit field subdivisions
- Complex instruction variations
- Extended operation modes

## ADA Emulation Critical Usage

**Essential for:**
- **CPU Emulation**: Accurate instruction decoding
- **Performance**: Fast opcode lookup tables
- **Compatibility**: Precise bit-level instruction matching
- **Debugging**: Instruction disassembly and analysis

## Encoding Analysis Requirements

1. **Bit Pattern Validation**: Cross-check all encoding patterns
2. **Sub-Opcode Verification**: Validate 1101011 extension mappings
3. **Instruction Completeness**: Ensure all 491 P2 instructions covered
4. **Encoding Conflicts**: Check for any ambiguous patterns

## Integration Notes

- Matrix provides fast lookup for emulation engines
- Essential for disassemblers and debuggers
- Critical for code generation validation
- Required for instruction timing analysis

## Next Steps
- Verify against official P2 instruction manual
- Cross-reference with existing PASM2 instruction database
- Extract any missing instruction variants