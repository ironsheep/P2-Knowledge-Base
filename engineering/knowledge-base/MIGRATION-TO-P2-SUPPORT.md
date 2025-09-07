# Migration Plan: P2 + P2-support Structure
*Date: 2025-09-07*

## Goal
Separate P2 knowledge from maintenance tools for clarity and usability.

## New Structure
```
engineering/knowledge-base/
├── P2/                    # Pure knowledge base
└── P2-support/           # Maintenance and tools
```

## Migration Steps

### Phase 1: Create P2-support Structure
```bash
mkdir -p P2-support/extractors
mkdir -p P2-support/validators
mkdir -p P2-support/converters
mkdir -p P2-support/filters
mkdir -p P2-support/sources/instructions/pasm2
mkdir -p P2-support/sources/language/spin2
mkdir -p P2-support/sources/hardware
mkdir -p P2-support/sources/architecture
mkdir -p P2-support/scripts
mkdir -p P2-support/tracking
mkdir -p P2-support/quality-reports
```

### Phase 2: Move Maintenance Materials
```bash
# Move tools
git mv P2/extractors/* P2-support/extractors/
git mv P2/validators/* P2-support/validators/
git mv P2/filters/* P2-support/filters/

# Move sources
git mv P2/production/_sources/* P2-support/sources/

# Move tracking/quality
git mv P2/quality-audits/* P2-support/quality-reports/
git mv P2/update-tracking/* P2-support/tracking/
git mv P2/version-control/* P2-support/tracking/

# Move scripts
git mv P2/*.py P2-support/scripts/
```

### Phase 3: Move Production to Root
```bash
# Move production files to P2 root
git mv P2/production/instructions P2/
git mv P2/production/language P2/
git mv P2/production/hardware P2/
git mv P2/production/architecture P2/
git mv P2/production/README.md P2/

# Remove empty production directory
rmdir P2/production/_sources
rmdir P2/production
```

### Phase 4: Clean Up Empty Directories
```bash
rmdir P2/extractors
rmdir P2/validators
rmdir P2/filters
rmdir P2/quality-audits
rmdir P2/update-tracking
rmdir P2/version-control
rmdir P2/instructions/pasm2
rmdir P2/instructions/spin2
rmdir P2/instructions/cross-references
rmdir P2/instructions
rmdir P2/language/spin2
rmdir P2/language
rmdir P2/.git-hooks
```

### Phase 5: Update Documentation
- Create P2/ARCHITECTURE.md
- Create P2/HEALTH-AUDIT.md
- Update P2/README.md
- Create P2-support/README.md

### Phase 6: Update Script Paths
All scripts need path updates:
- FROM: `P2/production/_sources/`
- TO: `P2-support/sources/`

## Files to Move

### To P2-support/extractors/
- layer1-csv-extractor.py
- layer2-datasheet-extractor.py
- layer3-silicon-doc-extractor.py
- layer4-chip-extractor.py
- narrative-csv-extractor.py
- timing-simple-extractor.py
- timing-complete-extractor.py
- timing-group-fixer.py
- add-timing-to-layer2.py

### To P2-support/validators/
- quality-check-10percent.py
- verify-timing-coverage.py
- validate-against-csv.py
- independent-count-check.py
- final-validation.py

### To P2-support/scripts/
- identify-conditionals.py
- investigate-missing-timing.py
- All other .py files

### To P2-support/tracking/
- REORGANIZATION-TRACKER.md
- timing-investigation-report.md
- All version control docs

## Success Criteria
- P2/ contains ONLY knowledge files
- P2-support/ contains ALL maintenance materials
- No broken script paths
- Clear documentation
- Health audit system in place