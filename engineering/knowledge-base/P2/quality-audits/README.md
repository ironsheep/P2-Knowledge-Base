# Quality Audits

## Overview
Tracks extraction coverage, completeness scores, and quality metrics for all repository entries.

## Audit Files

### Instruction Audits
- `pasm2-instructions-audit.yaml` - Coverage and scores for PASM2
- `spin2-constructs-audit.yaml` - Coverage and scores for Spin2

### Component Audits  
- `architecture-audit.yaml` - Architecture component coverage
- `hardware-audit.yaml` - Hardware documentation completeness
- `smart-pins-audit.yaml` - Smart pin mode documentation status

### Source Coverage
- `csv-extraction-audit.yaml` - P2 Instruction Set CSV coverage
- `datasheet-extraction-audit.yaml` - Datasheet mining status
- `silicon-doc-extraction-audit.yaml` - Silicon Doc narrative coverage
- `forum-extraction-audit.yaml` - Forum clarification integration

## Completeness Scoring (0-8 scale)

### Score Components
1. **Basic Definition** (CSV/specification present)
2. **Timing Data** (Cycle counts, conditions)
3. **Rich Narrative** (Detailed explanation)
4. **Authoritative Clarification** (Chip's input)
5. **Code Examples** (Working samples)
6. **Cross-References** (Related items linked)
7. **Usage Patterns** (Common idioms)
8. **Meta-Knowledge** (Tips, gotchas, optimizations)

### Quality Thresholds
- **Score 0-3**: Incomplete, not usable
- **Score 4-5**: Basic documentation, limited use
- **Score 6-7**: Production-ready documentation
- **Score 8**: Comprehensive, ideal documentation

## Audit Schema
```yaml
entry_id: instruction-or-component-id
completeness_score: 6
layers_present:
  csv: true
  datasheet: true
  silicon_doc: true
  forum: false
  examples: true
  cross_refs: true
extraction_date: "2025-01-06"
last_verified: "2025-01-06"
known_gaps:
  - "Missing CORDIC interaction timing"
  - "No forum clarifications found"
improvement_priority: medium
```