# P2 Knowledge Base Reorganization Tracker
*Generated: 2025-09-07*

## Overview
This document tracks all file movements for the P2 knowledge base reorganization.
Goal: Create production/source separation and clean directory structure.

## Key Changes
1. Create production versions from multi-layer source files
2. Move source files to `_sources/` subdirectory  
3. Fix misplaced directories (move into P2/)
4. Move tools/scripts out of knowledge-base
5. Clean extraction artifacts

## File Movement Plan

### Phase 1: Create Production Structure
```bash
# Create new directories
engineering/knowledge-base/P2/production/
engineering/knowledge-base/P2/production/instructions/
engineering/knowledge-base/P2/production/instructions/pasm2/
engineering/knowledge-base/P2/production/language/
engineering/knowledge-base/P2/production/language/spin2/
engineering/knowledge-base/P2/production/language/spin2/methods/
engineering/knowledge-base/P2/production/language/spin2/operators/
engineering/knowledge-base/P2/production/hardware/
engineering/knowledge-base/P2/production/architecture/
engineering/knowledge-base/P2/production/_sources/
```

### Phase 2: Move Current P2 Files to Sources
```
FROM: engineering/knowledge-base/P2/instructions/pasm2/*.yaml (357 files)
TO:   engineering/knowledge-base/P2/production/_sources/instructions/pasm2/

FROM: engineering/knowledge-base/P2/language/spin2/*.yaml (126 files)
TO:   engineering/knowledge-base/P2/production/_sources/language/spin2/

FROM: engineering/knowledge-base/P2/hardware/*.yaml
TO:   engineering/knowledge-base/P2/production/_sources/hardware/

FROM: engineering/knowledge-base/P2/architecture/*.yaml
TO:   engineering/knowledge-base/P2/production/_sources/architecture/
```

### Phase 3: Move Misplaced Directories into P2
```
FROM: engineering/knowledge-base/instructions/
TO:   [DELETE - duplicate of P2/instructions]

FROM: engineering/knowledge-base/clarifications/
TO:   engineering/knowledge-base/P2/documentation/clarifications/

FROM: engineering/knowledge-base/code-examples/
TO:   engineering/knowledge-base/P2/examples/

FROM: engineering/knowledge-base/p2-hardware/
TO:   [MERGE INTO] engineering/knowledge-base/P2/hardware/

FROM: engineering/knowledge-base/smart-pins/
TO:   engineering/knowledge-base/P2/hardware/smart-pins/

FROM: engineering/knowledge-base/spin2/
TO:   [MERGE INTO] engineering/knowledge-base/P2/language/spin2/

FROM: engineering/knowledge-base/system-registers/
TO:   engineering/knowledge-base/P2/hardware/system-registers/

FROM: engineering/knowledge-base/pasm2-instructions/
TO:   [DELETE - extraction artifacts]

FROM: engineering/knowledge-base/meta-knowledge/
TO:   engineering/knowledge-base/P2/documentation/meta-knowledge/
```

### Phase 4: Move Tools Out of Knowledge Base
```
FROM: engineering/knowledge-base/P2/extractors/
TO:   engineering/tools/p2-extractors/

FROM: engineering/knowledge-base/P2/validators/
TO:   engineering/tools/p2-validators/

FROM: engineering/knowledge-base/P2/filters/
TO:   engineering/tools/p2-filters/
```

### Phase 5: Clean Up Scripts
```
DELETE: engineering/knowledge-base/P2/*.py (move useful ones to tools/)
DELETE: engineering/knowledge-base/P2/instructions/pasm2/*.sh
```

## Scripts That Need Path Updates

### Extractors (11 files)
- `layer1-csv-extractor.py`
- `layer2-datasheet-extractor.py`
- `layer3-silicon-doc-extractor.py`
- `layer4-chip-extractor.py`
- `timing-simple-extractor.py`
- `timing-complete-extractor.py`
- `timing-group-fixer.py`
- `add-timing-to-layer2.py`
- `spin2-method-extractor.py`
- `spin2-operator-extractor.py`
- `narrative-csv-extractor.py`

### Validators/Checkers (6 files)
- `quality-check-10percent.py`
- `verify-timing-coverage.py`
- `validate-against-csv.py`
- `independent-count-check.py`
- `identify-conditionals.py`
- `investigate-missing-timing.py`

### Path References to Update
All scripts referencing:
- `/engineering/knowledge-base/P2/instructions/pasm2/`
  → `/engineering/knowledge-base/P2/production/_sources/instructions/pasm2/`
  
- `/engineering/knowledge-base/P2/language/spin2/`
  → `/engineering/knowledge-base/P2/production/_sources/language/spin2/`

## Production File Generation

### Source → Production Conversion
For each source file with multiple layers, create simplified production version:

**Source file structure** (pasm2_add.yaml):
- metadata (version, dates, sources)
- layer1_csv (encoding, syntax, description)
- layer2_datasheet (timing)
- layer3_narrative (description)
- layer4_clarifications (if any)

**Production file structure** (add.yaml):
- instruction: ADD
- syntax: ADD D,{#}S {WC/WZ/WCZ}
- encoding: EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS
- description: (best from all layers)
- timing: {cycles: 2, type: fixed}
- group: Math and Logic
- flags_affected: {C: carry, Z: zero}

## Tracking Status

### ✅ Completed
- [x] Created tracking document
- [x] Mapped all file movements
- [x] Identified scripts needing updates
- [x] Execute git moves
- [x] Create production converter script
- [x] Generate production files (357 PASM2)
- [x] Clean artifacts
- [x] Commit reorganization

### 🔄 In Progress
- [ ] Update script paths (next task)

### ⏳ Pending
- [ ] Generate production files for Spin2/Hardware/Architecture
- [ ] Update documentation
- [ ] Final validation

## Notes
- Using `git mv` to preserve history
- Keep _sources for debugging/validation
- Production files are ~50% smaller
- Single source of truth per instruction