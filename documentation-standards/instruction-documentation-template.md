# PASM2 Instruction Documentation Template

## Documentation Lineage Requirements

Every instruction MUST include source citations in the following format:

```
INSTRUCTION_NAME    Brief description from official sources

[PRIMARY SOURCE: P2 Instructions v35 spreadsheet, Row XXX]
[SECONDARY SOURCE: P2 Silicon Doc, Page XXX, Section Y.Y]
[MANUAL SOURCE: PASM2 Manual Draft 221117, Page XX]
[CONFIDENCE: Verified/Partial/Inferred]

Syntax: INSTRUCTION dest, {#}source {WC/WZ/WCZ}

Encoding: [FROM SPREADSHEET]
EEEE OOOOOO FXI DDDDDDDDD SSSSSSSSS

Timing: [FROM SPREADSHEET]
- Cycles: X
- Pipeline: Normal/Special
- Hub Impact: None/Stalls/Variable

Flags: [FROM SPREADSHEET]
- C: Updated/Unchanged/Special behavior
- Z: Updated/Unchanged/Special behavior

Parameters:
- dest: [FROM SILICON DOC/MANUAL]
- source: [FROM SILICON DOC/MANUAL]

Operation: [FROM SILICON DOC]
Detailed description of what the instruction does internally

Examples:
[GENERATED - NEEDS VALIDATION]
; Example 1: Basic usage
    INSTRUCTION result, #value    ; Comment

[VERIFIED - FROM FORUM POST BY CHIP GRACEY, 2020-XX-XX]
; Example 2: Real-world pattern
    INSTRUCTION reg1, reg2 WC     ; Comment

Notes & Warnings:
[SOURCE: Silicon Doc Known Issues, Page XX]
- Any special cases or gotchas

Related Instructions:
- LIST of related instructions with cross-references
```

## Traceability Matrix Example

| Claim | Primary Source | Secondary Source | Confidence |
|-------|---------------|------------------|------------|
| ADD takes 2 cycles | Spreadsheet Row 15 | Silicon Doc p.234 | Verified |
| ADD affects C flag for overflow | Spreadsheet Row 15 | Manual p.32 | Verified |
| ADD can use immediate values | Spreadsheet Row 15 | - | Verified |
| Example showing multi-precision add | - | - | Generated - Needs Validation |

## Source Priority Order

1. **P2 Instruction Spreadsheet v35** - Authoritative for encoding, timing, flags
2. **P2 Silicon Documentation** - Authoritative for operation details
3. **PASM2 Manual Draft** - Authoritative for syntax and usage patterns
4. **Forum posts by Chip Gracey** - Authoritative clarifications
5. **Community examples** - Must be marked as "Community Contributed"
6. **Generated examples** - Must be marked as "Needs Hardware Validation"

## Validation Requirements

Before marking any information as "Verified":
1. Must appear in at least one primary source
2. Must not contradict any other primary source
3. If sources conflict, mark as "NEEDS CLARIFICATION" with details

## Example Citation Formats

Good:
```
[SOURCE: P2 Instructions v35, Row 234, Column "Cycles": "2"]
The ADD instruction executes in 2 clock cycles.
```

Bad:
```
The ADD instruction is fast. [No source]
```

## Confidence Levels

- **Verified**: Directly stated in primary documentation
- **Derived**: Logically follows from primary documentation
- **Inferred**: Reasonable assumption based on similar instructions
- **Generated**: Created example, needs hardware testing
- **Unknown**: Information not found in available sources