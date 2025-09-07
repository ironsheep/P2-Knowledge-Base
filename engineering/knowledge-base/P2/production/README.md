# P2 Knowledge Base - Production Files

## Overview
This directory contains the **production-ready** P2 knowledge base files. These are clean, simplified versions optimized for AI and human consumption.

## Quick Stats
- **357 PASM2 instructions** - Complete CPU instruction set
- **73 Spin2 methods** - High-level language methods
- **46 Spin2 operators** - Language operators
- **11 Hardware specifications** - Board and module specs
- **8 Architecture components** - Core P2 architecture

## Directory Structure

```
production/
├── instructions/
│   └── pasm2/          # 357 CPU instructions
├── language/
│   └── spin2/
│       ├── methods/    # 73 Spin2 methods
│       └── operators/  # 46 Spin2 operators
├── hardware/           # 11 hardware specs
├── architecture/       # 8 core components
└── _sources/           # Original multi-layer files (for debugging)
```

## File Format

### PASM2 Instruction Example (`add.yaml`):
```yaml
instruction: ADD
syntax: ADD D,{#}S {WC/WZ/WCZ}
encoding: EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS
description: |
  Add S into D
timing:
  cycles: 2
  type: fixed
group: Math and Logic
flags_affected:
  C: carry of (D + S)
```

### Key Benefits
- **Single source of truth** - One description per instruction
- **Clean format** - Just essential fields
- **50% smaller** than source files
- **No confusion** - No multiple layers to choose from
- **AI-optimized** - Structured for easy parsing

## Usage

### For AI/Code Generation
Use production files directly:
```
/production/instructions/pasm2/add.yaml
/production/language/spin2/methods/debug.yaml
```

### For Debugging/Validation
Check source files in `_sources/`:
```
/production/_sources/instructions/pasm2/pasm2_add.yaml
```

## Data Sources
- **P2 Instructions CSV v35** - Instruction encodings and syntax
- **P2 Datasheet v35** - Timing and technical details
- **P2 Silicon Doc v35** - Architecture and features
- **Spin2 Language Doc v35** - Language specification

## Quality Metrics
- **100% timing coverage** for all CPU instructions
- **100% encoding coverage** for all instructions
- **Validated against** official Parallax documentation
- **Cross-checked** with multiple sources

## Notes
- Condition codes (IF_*, C_*, etc.) were intentionally excluded - they're not real instructions
- Source files preserved in `_sources/` maintain full extraction lineage
- Production files are regenerated from sources - don't edit directly