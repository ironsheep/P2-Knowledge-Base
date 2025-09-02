# Mini-Guide: Central Repository Build

## Purpose
Build unified P2 knowledge repository from current 76% coverage for demo in 1 week.

## Context Required
- Read: `/engineering/planning/UNIFIED-SHAPE-ANALYSIS.md` (unified approach)
- Read: `/engineering/planning/RICHNESS-PRINCIPLE.md` (richness strategy)
- Read: `/engineering/planning/SNAPSHOT-AND-DEMO-STRATEGY.md` (timeline)

## Data Flow
```
[SOURCES] → [PROCESSING] → [OUTPUT]
/engineering/ingestion/    aggregate_knowledge.py    /central-repository/
```

## Source Locations (INPUT)
```bash
# Primary instruction sources
/engineering/ingestion/sources/p2-instructions-csv/
  └── P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv
  
# Authority sources  
/engineering/ingestion/sources/chip-gracey-clarifications/
  ├── chip-instruction-clarifications-2025-09-02.md
  └── chip-gracey-programming-patterns-2025-09-02.md

# Technical details
/engineering/ingestion/sources/silicon-doc/
  ├── KNOWN-BUGS-CRITICAL.md
  ├── COG-RAM-REGISTER-MAP.md
  └── INSTRUCTION-TIMING-AND-ENCODING.md

# Smart Pins
/engineering/ingestion/sources/smart-pins/
  └── [Titus documentation]

# Processed data
/engineering/ingestion/central-analysis/
  ├── P2-COMPLETE-INSTRUCTION-MATRIX.json
  └── SMART-PINS-SOURCE-COMPARISON.md
```

## Output Location (TARGET)
```bash
/central-repository/                    # NEW - we create this
├── instructions/                       # 491 instruction files
│   ├── ADD.yaml
│   ├── ADDX.yaml
│   └── ...
├── smart-pins/                        # 32 mode files
│   ├── async-serial-tx.yaml
│   ├── async-serial-rx.yaml
│   └── ...
├── architecture/                      # Core P2 structure
│   ├── cogs.yaml
│   ├── memory.yaml
│   └── pipeline.yaml
└── manifest.yaml                      # Index of all entities
```

## Immediate Actions

### Step 1: Snapshot Current Knowledge
```python
# Read from ingestion sources
sources = {
    'csv': '/engineering/ingestion/sources/p2-instructions-csv/*.csv',
    'chip': '/engineering/ingestion/sources/chip-gracey-clarifications/*.md',
    'silicon': '/engineering/ingestion/sources/silicon-doc/*.md',
    'analysis': '/engineering/ingestion/central-analysis/*.json'
}
```

### Step 2: Create Repository Structure
```bash
# Create output directory structure
mkdir -p /central-repository/instructions
mkdir -p /central-repository/smart-pins
mkdir -p /central-repository/architecture
```
```
/central-repository/
├── instructions/      # 491 instructions (95% complete)
│   ├── ADD.yaml
│   └── ...
├── smart-pins/       # 32 modes (95% complete)
│   ├── uart.yaml
│   └── ...
├── architecture/     # Basic P2 structure
│   └── core.yaml
└── manifest.yaml     # Index and metadata
```

### Step 3: Define Minimal Schema
```yaml
# Minimal viable richness for demo
entity:
  id: "ADD"
  syntax: "ADD D,{#}S {WC/WZ/WCZ}"
  encoding: "EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS"
  description: "Adds S into D, result in D"
  timing: {cog: 2, hub: 2}
  flags: {C: "carry out", Z: "zero result"}
  examples: ["ADD sum, value", "ADD ptr, #4"]
  confidence: 0.95
  sources: ["CSV:10", "Silicon:45", "Chip:2025-09-02"]
```

### Step 4: Build Aggregator Script
```python
# aggregate_knowledge.py
def build_repository():
    repo = {}
    # 1. Load instruction matrix (95% complete)
    # 2. Add smart pins (95% complete)  
    # 3. Add architecture basics
    # 4. Calculate confidence scores
    # 5. Output as YAML/JSON
    return repo
```

## Success Criteria
- [ ] All 491 instructions captured
- [ ] All 32 smart pin modes included
- [ ] Basic architecture documented
- [ ] Confidence scores calculated
- [ ] Single query can answer "How does ADD work?"
- [ ] Ready for API layer in 2-3 days

## Time Budget
- Snapshot: 2 hours
- Schema design: 1 hour
- Aggregator script: 3 hours
- Initial population: 2 hours
- Validation: 2 hours
- **Total: 10 hours over 2-3 days**

## Key Decisions Already Made
1. **Unified shape** - One format serves all
2. **YAML/JSON** - Machine/human readable
3. **Snapshot at 76%** - Good enough for demo
4. **Incremental updates** - Post-demo improvement

## Files to Create
```bash
# Scripts location
/engineering/tools/repository-build/
├── aggregate_knowledge.py     # Reads from /engineering/ingestion/
├── validate_repository.py     # Validates /central-repository/
└── query_repository.py        # Tests /central-repository/

# Output location
/central-repository/           # Final knowledge base
└── [generated structure]      # Created by scripts
```

## Remember
- Demo in 1 week - speed over perfection
- 76% coverage is plenty for impressive demo
- Focus on instructions + smart pins first
- Rich enough for all consumers
- Updates are cheap post-demo

## Next Guide
After this: `download-on-demand-api.md`