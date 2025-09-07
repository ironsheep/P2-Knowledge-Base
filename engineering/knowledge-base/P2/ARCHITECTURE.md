# P2 Knowledge Base Architecture

## Directory Structure

```
P2/                           # Knowledge Base
├── language/                 # Programming Languages
│   ├── pasm2/               # PASM2 assembly (357 instructions)
│   └── spin2/               # Spin2 high-level language
│       ├── methods/         # 73 built-in methods
│       └── operators/       # 46 operators
├── hardware/                # Physical hardware specs
└── architecture/            # P2 architecture components
    ├── *.yaml              # Core components (COG, HUB, CORDIC)
    ├── smart-pins/         # 64 Smart Pin modes
    └── system-registers/   # System registers

P2-support/                  # Maintenance (separate directory)
├── sources/                # Multi-layer source files
├── extractors/             # Extraction scripts
├── validators/             # Validation tools
└── scripts/               # Utility scripts
```

## Design Principles

1. **Clean Separation**: Knowledge (P2/) vs Tools (P2-support/)
2. **Single Source of Truth**: One file per concept
3. **Logical Organization**: Instructions are part of their language
4. **No Maintenance Files**: Scripts/tools in P2-support only

## YAML Schema

### PASM2 Instruction
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

## Quality Guarantees

- ✅ 357 real CPU instructions (no conditionals)
- ✅ 100% timing coverage
- ✅ 100% encoding coverage
- ✅ Health score: 100/100

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-09-06 | Initial extraction |
| 1.1 | 2025-09-07 | Removed conditionals |
| 1.2 | 2025-09-07 | P2/P2-support separation |
| 1.3 | 2025-09-07 | Instructions → language/pasm2 |
| 2.0 | 2025-09-07 | Clean architecture, 100% timing |