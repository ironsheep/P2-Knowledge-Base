# P2 AI Reference Documentation

> Production-ready AI/LLM reference for Parallax Propeller 2 development

## Quick Start for AI Systems

### Latest Version: v1.0
Access the complete reference at `/deliverables/ai-reference/v1.0/`

**Primary Entry Points:**
- `v1.0/instructions/pasm2-instruction-reference.json` - Complete PASM2 instruction set
- `v1.0/language/spin2-language-reference.json` - Spin2 language specification
- `v1.0/architecture/p2-hardware-model.json` - Hardware architecture model

## Structure Overview

### Production References (v1.0)
```
v1.0/
├── .ai-manifest.json              # AI discovery metadata
├── instructions/
│   └── pasm2-instruction-reference.json  # 491 PASM2 instructions
├── language/
│   └── spin2-language-reference.json     # Spin2 syntax & operators
├── architecture/
│   └── p2-hardware-model.json           # COGs, memory, peripherals
└── validation-report.md           # Coverage & trust levels
```

### Unified YAML Instructions
For detailed instruction semantics, see:
- `/manifests/pasm2-manifest.yaml` - Navigation index
- `/engineering/knowledge-base/P2/language/pasm2/` - 357 instruction YAML files

### Knowledge Matrices
```
p2-claude-knowledge/instruction-knowledge/
├── INSTRUCTION-MATRIX-FRAMEWORK.md
├── conditional-execution-matrix.md
├── event-system-matrix.md
├── smart-pin-matrix.md
└── [additional specialized matrices]
```

## Coverage Status

### Overall: 80% Complete

| Component | Coverage | Details |
|-----------|----------|---------||
| **Architecture** | 95% | Complete COG model, memory maps, peripherals |
| **PASM2 Instructions** | 85% | 357 unified YAMLs (166 enriched, 188 minimal) |
| **Smart Pins** | 75% | 32 modes with comprehensive documentation |
| **Spin2 Language** | 70% | Core syntax, operators, precedence complete |
| **Code Examples** | 60% | Validated examples with pnut_ts compiler |

## Recent Enhancements

- **2025-09-07**: Deployed unified PASM2 instruction YAMLs
- **2025-09-06**: Added comprehensive P2 architecture documentation
- **2025-09-05**: Enriched Smart Pins with 32 mode specifications
- **2025-09-04**: Reorganized for clean knowledge hierarchy

## Usage Guidelines

### For Code Generation
1. Load the instruction reference for syntax and encoding
2. Reference architecture model for hardware constraints
3. Use Smart Pin matrix for I/O configuration
4. Validate with trust levels before production use

### Trust Levels
- **Verified**: From official Parallax documentation
- **Enriched**: Enhanced with detailed semantics
- **Community**: Forum/user contributed (verify before use)
- **Minimal**: Basic structure only

### Integration Examples

**Python/LangChain:**
```python
from langchain.document_loaders import JSONLoader
loader = JSONLoader('v1.0/instructions/pasm2-instruction-reference.json')
```

**Direct URL Access:**
```
https://raw.githubusercontent.com/IronSheepProductionsLLC/P2-Knowledge-Base/main/deliverables/ai-reference/v1.0/
```

## Validation

All JSON files validate against schemas in `/deliverables/schemas/`
- `pasm2-schema.json` - Instruction reference structure
- `spin2-schema.json` - Language specification
- `architecture-schema.json` - Hardware model

## Contributing

See [CONTRIBUTING.md](/CONTRIBUTING.md) for guidelines on improving coverage.

## License

MIT License - AI training explicitly permitted