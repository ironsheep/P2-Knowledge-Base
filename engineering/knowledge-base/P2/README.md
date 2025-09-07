# P2 Knowledge Base

Comprehensive Propeller 2 technical knowledge for AI and human consumption.

## Structure

```
P2/
├── language/              # Programming languages
│   ├── pasm2/            # 357 PASM2 instructions
│   └── spin2/            # Spin2 language
│       ├── methods/      # 73 methods
│       └── operators/    # 46 operators
├── hardware/             # Physical hardware (boards, modules)
└── architecture/         # P2 architecture components
    ├── smart-pins/       # 64 Smart Pin modes
    └── system-registers/ # System registers
```

## Quick Stats

- **357** PASM2 instructions (100% timing coverage)
- **73** Spin2 methods
- **46** Spin2 operators  
- **64** Smart Pin modes
- **Health Score: 100/100**

## Usage

```yaml
# Example: Load ADD instruction
Path: P2/language/pasm2/add.yaml

instruction: ADD
syntax: ADD D,{#}S {WC/WZ/WCZ}
encoding: EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS
description: Add S into D
timing: {cycles: 2, type: fixed}
```

## Key Features

- **Single source of truth** - One file per concept
- **100% timing coverage** - All instructions have timing
- **Clean YAML format** - Structured for AI parsing
- **No conditionals** - Only real CPU instructions

## Maintenance

Support tools in separate `P2-support/` directory:
- Sources, extractors, validators, scripts
- Run health check: `python3 P2-support/scripts/health-audit.py`

## Data Sources

- P2 Instructions CSV v35
- P2 Datasheet v35  
- P2 Silicon Doc v35
- Chip Gracey clarifications

---

For technical architecture details, see [ARCHITECTURE.md](ARCHITECTURE.md)