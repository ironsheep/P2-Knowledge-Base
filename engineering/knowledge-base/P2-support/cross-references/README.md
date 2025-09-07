# Cross-Reference Definitions

## Overview
Handles instructions and features that span multiple contexts (PASM2/Spin2) or have complex relationships.

## Types of Cross-References

### Dual-Context Instructions
Instructions available in both PASM2 and Spin2:
- Primary definition in most-used context
- Reference file pointing to primary
- Context-specific usage notes

### Instruction Families
Related instructions grouped by function:
- `math-operations.yaml` - All math instructions
- `branch-operations.yaml` - All branching instructions
- `memory-operations.yaml` - All memory access

### Shared Concepts
Concepts that apply across multiple areas:
- `timing-rules.yaml` - Universal timing principles
- `flag-operations.yaml` - C and Z flag usage
- `addressing-modes.yaml` - Common addressing patterns

## Reference Schema
```yaml
reference_id: "dual-context-mov"
type: "dual-context"
primary_definition: "instructions/pasm2/mov-instruction.yaml"
secondary_contexts:
  - context: "spin2"
    usage_notes: "Available as inline PASM2"
    syntax_differences: "Uses different operand format"
related_instructions:
  - "instructions/pasm2/movbyts-instruction.yaml"
  - "instructions/pasm2/movs-instruction.yaml"
```

## Relationship Types
- `implements` - Higher-level construct uses instruction
- `related` - Similar function or usage
- `opposite` - Inverse operation
- `prerequisite` - Must understand first
- `see-also` - Additional relevant information