# Directory Nesting Audit
## Date: 2025-09-01

### Problem Discovered
During PHASE 40 audit, found improper nesting: `engineering/ingestion/sources/sources/`

## Current Structure Analysis

### At `engineering/ingestion/sources/` level:

**Individual Ingestion Projects** (19 directories):
- desilva-p1-tutorial/
- edge-32mb-module/ (contains: assets/, audit.md, PDF)
- edge-breakout-board/
- edge-mini-breakout/
- edge-module-breadboard/
- edge-standard-module/
- p2-eval-add-on-boards/
- p2-eval-board/
- p2-instructions-csv/
- p2-wx-adapter/
- parallax-wx-wifi/
- pasm2-manual/
- propplug-rev-e/
- rom-booter/
- silicon-doc/
- smart-pins/
- spin2-v51/
- universal-motor-driver/
- **sources/** ← THE PROBLEM (nested directory)

### At `engineering/ingestion/sources/sources/` level:

**Core Ingestion Infrastructure**:
- analysis/ (20+ analysis documents)
- extractions/ (main extraction documents)
- extractions-v1-archived/ (obsolete V1)
- format-analysis/ (format studies)
- originals/ (source PDFs, CSVs)
- p1-master/ (P1 references)
- pasm2-manual-development/ (development work)
- pasm2-master/ (PASM2 master docs)
- visual-assets/ (extracted images)
- working/ (temporary work)
- EXTRACTION-INDEX.md
- EXTRACTION-INDEX-V2.md
- V1-TO-V2-MIGRATION-AUDIT.md
- V2-MIGRATION-COMPLETE.md
- README.md

## The Problem:

We have TWO different organizational patterns mixed:
1. **Project-based** (edge-32mb-module/, smart-pins/, etc.) - Each with their own audit and assets
2. **Function-based** (extractions/, originals/, analysis/) - Core infrastructure

The function-based directories got nested inside a 'sources' subdirectory when they should be at the same level as the project directories.

## Proposed Solution:

### Target Structure:
```
engineering/ingestion/sources/
├── [PROJECT DIRECTORIES - Stay in place]
│   ├── edge-32mb-module/
│   ├── edge-mini-breakout/
│   ├── smart-pins/
│   └── ... (all 19 project dirs)
├── [CORE INFRASTRUCTURE - Move up from sources/sources/]
│   ├── analysis/
│   ├── extractions/
│   ├── originals/
│   ├── visual-assets/
│   ├── format-analysis/
│   ├── pasm2-master/
│   └── working/
└── [ROOT FILES - Move up from sources/sources/]
    ├── EXTRACTION-INDEX.md
    ├── V2-MIGRATION-COMPLETE.md
    └── README.md
```

## Move Plan:

### Phase 1: Move Core Infrastructure (10 items)
```bash
git mv engineering/ingestion/sources/sources/analysis engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/extractions engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/originals engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/visual-assets engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/format-analysis engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/p1-master engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/pasm2-manual-development engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/pasm2-master engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/extractions-v1-archived engineering/ingestion/sources/
git mv engineering/ingestion/sources/sources/working engineering/ingestion/sources/
```

### Phase 2: Move Root Files (5 items)
```bash
git mv engineering/ingestion/sources/sources/*.md engineering/ingestion/sources/
```

### Phase 3: Remove Empty Nested Directory
```bash
rmdir engineering/ingestion/sources/sources
```

### Phase 4: Update References
- Search for paths containing "sources/sources/"
- Update to single "sources/"
- Document in reference-fixes.log

## Verification Checklist:
- [ ] All project directories remain in place
- [ ] Core infrastructure moved up one level
- [ ] No nested sources/sources/ remains
- [ ] All references updated
- [ ] Mapping.csv updated with moves