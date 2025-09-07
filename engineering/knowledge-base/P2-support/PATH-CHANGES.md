# Path Changes During Migration
*Track all moves for script updates*

## Directory Moves

| FROM | TO | Scripts Affected |
|------|-----|-----------------|
| P2/extractors/ | P2-support/extractors/ | All extractor scripts |
| P2/validators/ | P2-support/validators/ | All validator scripts |
| P2/filters/ | P2-support/filters/ | Filter scripts |
| P2/production/_sources/ | P2-support/sources/ | ALL scripts that read source files |
| P2/production/instructions/ | P2/instructions/ | Scripts reading production files |
| P2/production/language/ | P2/language/ | Scripts reading language files |
| P2/production/hardware/ | P2/hardware/ | Scripts reading hardware files |
| P2/production/architecture/ | P2/architecture/ | Scripts reading architecture files |
| P2/quality-audits/ | P2-support/quality-reports/ | Quality check scripts |
| P2/update-tracking/ | P2-support/tracking/ | Tracking scripts |

## Critical Path Updates Needed

### In Extractor Scripts:
```python
# OLD:
pasm2_dir = Path("P2/production/_sources/instructions/pasm2")
# NEW:
pasm2_dir = Path("../sources/instructions/pasm2")  # Relative from P2-support/extractors/
```

### In Validator Scripts:
```python
# OLD:
production_dir = Path("P2/production/instructions/pasm2")
# NEW:
production_dir = Path("../P2/instructions/pasm2")  # Relative from P2-support/validators/
```

### In Converter Scripts:
```python
# OLD:
source_dir = Path("P2/production/_sources/")
# NEW:
source_dir = Path("P2-support/sources/")
```

## Files Being Moved (tracking for updates)

### Extractors (9 files):
- [x] layer1-csv-extractor.py
- [x] layer2-datasheet-extractor.py
- [x] layer3-silicon-doc-extractor.py
- [x] layer4-chip-extractor.py
- [x] narrative-csv-extractor.py
- [x] timing-simple-extractor.py
- [x] timing-complete-extractor.py
- [x] timing-group-fixer.py
- [x] add-timing-to-layer2.py

### Validators (5 files):
- [ ] quality-check-10percent.py
- [ ] verify-timing-coverage.py
- [ ] validate-against-csv.py
- [ ] independent-count-check.py
- [ ] final-validation.py

### Other Scripts in P2/:
- [ ] identify-conditionals.py
- [ ] investigate-missing-timing.py
- [ ] All .py files in root

## Update Status
- [ ] Scripts moved
- [ ] Paths updated in scripts
- [ ] Scripts tested with new paths
- [ ] Documentation updated