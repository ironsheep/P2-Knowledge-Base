# P2 Knowledge Base Repository Structure
## Living Document - Version 1.0

## Overview
This document serves as the comprehensive map of the P2 Knowledge Base central repository, documenting structure, schemas, naming conventions, and operational procedures.

## Directory Hierarchy

```
/engineering/knowledge-base/P2/
├── README.md                          # Repository overview and quick start
├── repository-structure.md            # This document - living map
│
├── instructions/                      # All P2 instructions
│   ├── README.md                      # Instructions overview
│   ├── pasm2/                         # PASM2 assembly instructions
│   │   ├── README.md                  # PASM2 specific documentation
│   │   └── *.yaml                     # One file per instruction (~500 files)
│   ├── spin2/                         # Spin2 language constructs
│   │   ├── README.md                  # Spin2 specific documentation
│   │   └── *.yaml                     # Operators, methods, keywords
│   └── cross-references/              # Dual-context and relationships
│       ├── README.md                  # Cross-reference documentation
│       └── *.yaml                     # Reference definitions
│
├── architecture/                      # P2 architectural components
│   ├── README.md                      # Architecture overview
│   └── *.yaml                         # System components (cogs, hub, etc.)
│
├── hardware/                          # Physical hardware specifications
│   ├── README.md                      # Hardware overview
│   └── *.yaml                         # Chips, boards, modules
│
├── components/                        # P2 subsystems
│   ├── README.md                      # Components overview
│   ├── smart-pins/                    # Smart pin subsystem
│   │   ├── README.md                  # Smart pins documentation
│   │   └── mode-*.yaml                # One file per mode (30+ files)
│   ├── cordic/                        # CORDIC solver
│   │   ├── README.md                  # CORDIC documentation
│   │   └── *.yaml                     # CORDIC operations
│   └── *.yaml                         # Other components
│
├── examples/                          # Code examples
│   ├── README.md                      # Examples overview
│   └── [category]/                    # Organized by type/feature
│       └── *.spin2|*.pasm2            # Example code files
│
├── quality-audits/                    # Coverage and quality tracking
│   ├── README.md                      # Audit documentation
│   └── *.yaml                         # Audit files by category
│
└── update-tracking/                   # Version and change tracking
    ├── README.md                      # Update tracking documentation
    └── *.yaml                         # Change logs and version data
```

## Naming Conventions

### Files
- **Format**: lowercase, hyphens for spaces, descriptive names
- **Extensions**: `.yaml` for data, `.md` for documentation
- **Examples**:
  - Instructions: `add-instruction.yaml`, `wrpin-instruction.yaml`
  - Components: `smart-pin-mode-07-pwm.yaml`
  - Hardware: `p2-eval-board.yaml`

### Directories
- **Format**: lowercase, hyphens for spaces
- **Structure**: Logical grouping by function
- **Examples**: `smart-pins/`, `cross-references/`, `quality-audits/`

### YAML IDs
- **Format**: lowercase, hyphens, unique within category
- **Pattern**: `[category]-[specific]-[type]`
- **Examples**: `pasm2-add-instruction`, `smart-pin-mode-07`

## Core YAML Schemas

### Instruction Schema
```yaml
# Required fields
id: string                    # Unique identifier
mnemonic: string              # Instruction mnemonic (ADD, MOV, etc.)
category: string              # Functional category
syntax: string                # Syntax pattern
encoding: string              # Binary encoding format

# Timing information
timing:
  cycles: number|string       # Cycle count or range
  conditions: string          # Conditions affecting timing
  
# Documentation
description: string           # Detailed description
usage_notes: string           # Programming notes
examples:                     # Code examples
  - code: string
    explanation: string

# Relationships
related: [string]            # Related instruction IDs
see_also: [string]           # Additional references
affects_flags:               # Flag effects
  c: boolean|string
  z: boolean|string

# Source tracking
source_layers:
  csv: boolean               # From P2 Instruction Set CSV
  datasheet: boolean         # From P2 Datasheet
  silicon_doc: boolean       # From Silicon Doc
  forum_clarification: boolean # From Chip's forum posts
  
# Quality metrics
completeness_score: number   # 0-8 scale
extraction_date: date        # When extracted
last_updated: date           # Last modification
last_verified: date          # Last verification
```

### Component Schema
```yaml
id: string                    # Unique identifier
name: string                  # Component name
type: string                  # Component type
category: string              # Functional category

# Specifications
specifications:
  [key]: value               # Component-specific specs
  
# Configuration
configuration:
  registers: [object]        # Configuration registers
  modes: [object]            # Operational modes
  
# Documentation
description: string          # Detailed description
programming_model: string    # How to program it
timing: object              # Timing characteristics
examples: [object]          # Usage examples

# Relationships
related_instructions: [string] # Instructions that control this
related_components: [string]   # Related components
  
# Quality metrics
completeness_score: number
last_updated: date
```

### Hardware Schema
```yaml
id: string                   # Unique identifier
name: string                 # Product name
type: string                 # Hardware type (chip, board, module)
manufacturer: string         # Manufacturer name
part_number: string          # Part number

# Specifications
specifications:
  dimensions: object         # Physical dimensions
  power: object              # Power requirements
  connectors: [object]       # Connector details
  features: [string]         # Feature list
  
# Compatibility
compatibility:
  boards: [string]           # Compatible boards
  modules: [string]          # Compatible modules
  software: [string]         # Software support
  
# Documentation
description: string
pinout: object              # Pin assignments
schematic_ref: string       # Schematic reference
revision_history: [object]  # Hardware revisions

# Quality metrics
documentation_level: string  # complete|partial|minimal
last_updated: date
```

## Cross-Reference Handling

### Types of Cross-References
1. **Dual-Context**: Instructions/features in both PASM2 and Spin2
2. **Related**: Functionally related items
3. **Dependencies**: Items that depend on each other
4. **See-Also**: Additional relevant information

### Implementation Strategy
```yaml
# For dual-context items:
# 1. Primary definition in main usage context
# 2. Reference file in secondary context:
reference_id: string
type: "dual-context"
primary_definition: "path/to/primary.yaml"
secondary_contexts:
  - context: string
    usage_notes: string
    syntax_differences: string
```

## Quality Assurance

### Completeness Scoring (0-8 Scale)
- **0-1**: Minimal - ID and name only
- **2-3**: Basic - Includes syntax and encoding
- **4-5**: Functional - Has timing and description
- **6-7**: Production - Examples and cross-references
- **8**: Comprehensive - All layers present

### Data Layers
1. **Layer 1**: P2 Instruction Set CSV (base definitions)
2. **Layer 2**: P2 Datasheet (timing, specifications)
3. **Layer 3**: Silicon Doc (rich narratives)
4. **Layer 4**: Forum clarifications (authoritative updates)

### Validation Rules
- All required fields must be present
- IDs must be unique within category
- Cross-references must resolve
- Examples must compile (when applicable)
- Completeness score must match actual content

## Update Procedures

### Adding New Entries
1. Create YAML file following naming convention
2. Populate required fields from primary source
3. Add available optional fields
4. Calculate completeness score
5. Create/update cross-references
6. Update relevant audit files
7. Commit with descriptive message

### Updating Existing Entries
1. Identify trigger (new source, correction, etc.)
2. Load existing entry
3. Apply updates preserving history
4. Recalculate completeness score
5. Update cross-references if needed
6. Log change in update-tracking
7. Commit with update rationale

### Conflict Resolution
Priority order for conflicting information:
1. P2 Datasheet (official specification)
2. Silicon Doc (authoritative narrative)  
3. Chip's forum posts (creator clarification)
4. Community consensus (validated information)

## Usage Patterns

### For Document Generation
```python
# Load all instructions with score >= 6
instructions = load_yaml("instructions/pasm2/*.yaml")
filtered = [i for i in instructions if i.completeness_score >= 6]
generate_documentation(filtered)
```

### For AI Training
```python
# Get comprehensive instruction data
data = aggregate_layers([
    "instructions/pasm2/*.yaml",
    "examples/*.yaml",
    "cross-references/*.yaml"
])
prepare_training_data(data)
```

### For Quality Analysis
```python
# Generate coverage report
audits = load_yaml("quality-audits/*.yaml")
report = generate_coverage_report(audits)
identify_gaps(report)
```

## Version Control Integration

### Commit Message Format
```
[CATEGORY] Brief description

- Added: New entries or fields
- Updated: Modified entries
- Fixed: Corrections
- Removed: Deleted entries

Sources: [Document names and versions]
Score changes: [ID: old->new]
```

### Branch Strategy
- `main`: Stable, validated content
- `extraction/*`: Active extraction work
- `update/*`: Source update integration
- `fix/*`: Corrections and improvements

## API Access Patterns

### Query Examples
- Get single instruction: `/api/instruction/pasm2/add`
- Get by category: `/api/instructions?category=math`
- Get by score: `/api/instructions?min_score=6`
- Get updates since: `/api/updates?since=2025-01-01`

## Maintenance Tasks

### Daily
- Check for source document updates
- Process pending extractions
- Validate cross-references

### Weekly
- Generate quality reports
- Review and resolve conflicts
- Update completeness scores

### Monthly
- Full repository validation
- Archive completed updates
- Generate coverage statistics

## Future Enhancements

### Planned Features
- Automated extraction pipeline
- Real-time validation system
- API rate limiting and caching
- Visual dependency graphs
- Interactive documentation browser

### Schema Evolution
- Version field in all schemas
- Migration scripts for updates
- Backward compatibility for 2 versions
- Deprecation warnings in API

## Contact and Contributing

### Reporting Issues
- File issues in quality-audits/
- Include entry ID and description
- Provide source references

### Contributing Updates
- Follow extraction methodology
- Maintain audit trail
- Include source attribution
- Update completeness scores

---

This document is the authoritative reference for repository structure and operations. Update this document whenever structural changes are made.