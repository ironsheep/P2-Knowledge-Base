# P2 Instructions Repository

## Overview
Contains structured YAML definitions for all P2 instructions, organized by language context.

## Directory Structure
- `pasm2/` - PASM2 assembly instructions (~500 files)
- `spin2/` - Spin2 language constructs and operators
- `cross-references/` - Instructions that span both contexts

## File Naming Convention
Each instruction gets its own YAML file named:
- Pattern: `[mnemonic]-instruction.yaml`
- Examples: 
  - `add-instruction.yaml`
  - `mov-instruction.yaml`
  - `wrpin-instruction.yaml`

## YAML Schema
Each instruction file contains:
```yaml
id: unique-instruction-id
mnemonic: ADD
category: math
syntax: ADD D,{#}S
encoding: "EEEE 1000000 CZI DDDDDDDDD SSSSSSSSS"
timing:
  cycles: 2
  conditions: "2-9 cycles depending on hub alignment"
description: "Adds source to destination..."
examples:
  - code: "ADD x,#1"
    explanation: "Increment x by 1"
related:
  - SUB
  - ADDS
  - ADDX
source_layers:
  csv: true
  datasheet: true
  silicon_doc: true
  forum_clarification: false
completeness_score: 6
last_updated: "2025-01-06"
```

## Cross-References
Instructions used in both PASM2 and Spin2 contexts have:
- Primary definition in most common context
- Symlink or reference file in other context
- Clear notation of dual usage

## Quality Requirements
- Minimum score 4 (CSV + datasheet) for inclusion
- Target score 6+ for production use
- Score 8 indicates fully documented instruction