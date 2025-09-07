# P2 Knowledge Base Architecture
*Version 1.2.0 - Clean Separation Structure*

## Overview
The P2 Knowledge Base provides comprehensive technical documentation for the Propeller 2 microcontroller, organized for optimal AI and human consumption.

## Directory Structure

```
P2/                           # The Knowledge Base
├── instructions/             # CPU Instructions (357 files)
│   └── pasm2/               # PASM2 assembly instructions
├── language/                # Programming Languages
│   └── spin2/               # Spin2 high-level language
│       ├── methods/         # Built-in methods (73 files)
│       ├── operators/       # Language operators (46 files)
│       ├── symbols/         # Built-in symbols
│       └── integration/     # PASM2 integration docs
├── hardware/                # Hardware Specifications
│   ├── smart-pins/          # Smart Pin documentation
│   │   └── modes/          # Smart Pin modes (64 files)
│   └── system-registers/    # System register specs
├── architecture/            # Core Architecture (8 components)
│   ├── cog.yaml            # COG processor details
│   ├── hub.yaml            # Hub memory system
│   ├── cordic.yaml         # CORDIC solver
│   └── ...                 # Other components
├── components/              # Detailed Component Docs
│   ├── cordic/             # CORDIC implementation
│   └── smart-pins/         # Smart Pin details
├── documentation/           # User Documentation
│   ├── clarifications/     # Chip Gracey clarifications
│   └── meta-knowledge/     # Cross-cutting concepts
└── examples/               # Code Examples
    └── instruction-examples/
```

## Design Principles

### 1. Single Source of Truth
Each P2 element has exactly ONE authoritative file containing all essential information.

### 2. Clean YAML Format
```yaml
instruction: ADD
syntax: ADD D,{#}S {WC/WZ/WCZ}
encoding: EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS
description: |
  Add S into D
timing:
  cycles: 2
  type: fixed
```

### 3. Separation of Concerns
- **P2/**: Contains ONLY knowledge files
- **P2-support/**: Contains ALL maintenance tools (separate directory)

### 4. Optimized for AI
- Structured data format
- Consistent naming conventions
- Complete timing and encoding information
- Clear semantic relationships

## File Counts

| Category | Files | Description |
|----------|-------|-------------|
| PASM2 Instructions | 357 | Complete CPU instruction set |
| Spin2 Methods | 73 | Built-in language methods |
| Spin2 Operators | 46 | Language operators |
| Hardware Specs | 11 | Board and module specifications |
| Architecture | 8 | Core P2 components |
| Smart Pin Modes | 64 | All Smart Pin configurations |
| **Total** | **559+** | Complete P2 knowledge |

## Quality Guarantees

### Coverage
- ✅ 100% of real CPU instructions documented
- ✅ 100% timing information for all instructions
- ✅ Complete encoding for all instructions
- ✅ All Smart Pin modes documented

### Validation
- Cross-referenced against P2 Silicon v35 documentation
- Validated against official CSV instruction set
- Chip Gracey clarifications incorporated
- No conditional/pseudo instructions (cleaned)

## Maintenance

### Supporting Infrastructure
The P2-support/ directory (parallel to P2/) contains:
- Extraction scripts
- Validation tools
- Source files (multi-layer originals)
- Quality reports
- Update tracking

### Update Process
1. Sources updated in P2-support/sources/
2. Converters regenerate production files
3. Validators ensure quality
4. Changes committed to P2/

## Usage

### For AI/Code Generation
```python
# Direct file access
instruction = load("P2/instructions/pasm2/add.yaml")
# Use instruction.syntax, instruction.timing, etc.
```

### For Documentation
- Start with P2/README.md
- Browse by category (instructions/, language/, etc.)
- Check documentation/ for guides

### For Maintenance
- Use tools in P2-support/
- Run health audit: `python3 P2-support/scripts/health-audit.py`
- Validate quality: `python3 P2-support/validators/final-validation.py`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-09-06 | Initial extraction (440 files) |
| 1.0.1 | 2025-09-07 | Removed 83 conditionals |
| 1.1.0 | 2025-09-07 | Production/source separation |
| 1.2.0 | 2025-09-07 | P2/P2-support clean separation |

## Key Benefits

1. **Clarity**: Immediate understanding of what's knowledge vs tools
2. **Usability**: Clean structure for AI consumption
3. **Maintainability**: Clear separation of concerns
4. **Quality**: Validated, complete coverage
5. **Efficiency**: 50% smaller than source files

---

*For maintenance documentation, see P2-support/README.md*