# P2 Knowledge Base

Central repository of Propeller 2 technical knowledge extracted from authoritative sources.

## Overview

This knowledge base contains structured YAML representations of P2 technical documentation, organized in a layered data model for progressive enhancement and AI consumption.

## Structure

```
P2/
├── instructions/pasm2/     # 440 PASM2 instruction definitions
├── language/spin2/         # 119 Spin2 language elements
├── hardware/               # 11 hardware specifications
├── architecture/           # 8 architecture components
├── extractors/             # Extraction scripts
├── manifest.yaml           # Complete content index
└── baseline-quality-report-v1.0.md
```

## Content Statistics

| Category | Count | Coverage |
|----------|-------|----------|
| PASM2 Instructions | 440 | 100% base encoding |
| Layer 1 (CSV) | 440 | 100% complete |
| Layer 2 (Timing) | 61 | 13.9% (available data) |
| Layer 3 (Narratives) | 405 | 92.0% complete |
| Layer 4 (Clarifications) | 12 | 2.7% (critical instructions) |
| Spin2 Methods | 73 | Complete |
| Spin2 Operators | 46 | Complete |
| Hardware Specs | 11 | Major boards/modules |
| Architecture | 8 | Core components |

## Layered Data Model

### PASM2 Instructions
Each instruction file contains up to 4 layers of data:

1. **Layer 1 - CSV Base**: Encoding, syntax, group (100% coverage)
2. **Layer 2 - Datasheet**: Timing information where available
3. **Layer 3 - Narrative**: Functional descriptions (92% coverage)
4. **Layer 4 - Clarifications**: Expert insights from Chip Gracey

### Example Structure
```yaml
name: ADD
layer1_csv:
  mnemonic: ADD
  syntax: ADD D,{#}S {WC/WZ/WCZ}
  encoding: EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS
layer2_datasheet:
  timing_cog: 2
layer3_narrative:
  description: "Add S into D"
```

## Quality Metrics

- **Total Files**: 578 YAML files
- **Quality Score**: 94.7% (validation pass rate)
- **Completeness**: All core P2 elements documented
- **Format**: Consistent YAML structure

## Usage

This knowledge base is designed for:
- AI training and code generation
- Documentation generation tools
- IDE code completion
- Instruction reference systems
- Hardware compatibility checking

## Sources

| Source | Type | Authority |
|--------|------|-----------|
| P2 Instructions CSV v35 | Spreadsheet | Official |
| P2 Datasheet | Document | Official |
| Silicon Doc v35 | Manual | Official |
| Spin2 Doc v51 | Manual | Official |
| Chip Gracey Clarifications | Expert | Designer |

## Version

**Current Version**: 1.0.0  
**Release Date**: 2025-09-07  
**Tag**: v1.0.0

## Future Improvements (v2.0)

- Extended timing coverage
- More instruction examples
- Cross-reference system
- Smart Pin mode details
- Additional expert clarifications

## License

Part of the P2-Language-Study project. See main repository for license details.

---

*P2 Knowledge Base - Enabling AI-powered Propeller 2 development*