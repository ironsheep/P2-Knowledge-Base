# P2 Repository Validators

## Overview
Comprehensive validation system for ensuring data integrity, consistency, and quality across the P2 Knowledge Base repository.

## Validation Components

### 1. Repository Validator (`repository-validator.py`)
Main validation framework that performs comprehensive checks:
- **Schema Validation**: Ensures all entries conform to defined schemas
- **Cross-Reference Checking**: Validates all instruction relationships
- **Circular Reference Detection**: Identifies dependency cycles
- **Encoding Validation**: Verifies 32-bit instruction encodings
- **Timing Validation**: Checks cycle count formats and ranges
- **Coverage Analysis**: Identifies systematic gaps in documentation
- **Consistency Checking**: Ensures bidirectional references and category compatibility

### 2. Validation Dashboard (`validation-dashboard.html`)
Interactive web dashboard showing:
- Real-time validation status
- Error and warning counts
- Field coverage percentages
- Reference graph visualization
- Recent issues list
- Auto-refresh capability

## Usage

### Running Full Validation
```bash
cd /engineering/knowledge-base/P2
python3 validators/repository-validator.py
```

This will:
1. Load all YAML entries from the repository
2. Run all validation checks
3. Generate a report in `validation-reports/validation-report.md`
4. Save JSON results in `validation-reports/validation-report.json`

### Viewing the Dashboard
Open `validators/validation-dashboard.html` in a web browser to view the interactive dashboard.

## Validation Checks

### Schema Compliance
- Required fields presence
- Field type validation
- Pattern matching (mnemonics, encodings)
- Enum value validation

### Cross-Reference Integrity
- Instruction references exist
- See-also links are valid
- Bidirectional relationships maintained
- No orphaned entries

### Encoding Format
- 32-bit length verification
- Valid bit patterns (0, 1, E, C, Z, I, D, S)
- Consistent formatting

### Timing Specifications
- Valid cycle counts (integer or range)
- Range format validation (e.g., "2-9")
- Condition string presence

### Circular References
- Dependency cycle detection
- Graph traversal validation
- Reference chain analysis

## Error Types

### Critical Errors (Must Fix)
- `missing_required_field`: Required field not present
- `field_validation_failed`: Field value doesn't match specification
- `broken_reference`: Referenced instruction doesn't exist
- `invalid_encoding_length`: Encoding not 32 bits
- `invalid_timing_format`: Malformed timing specification

### Warnings (Should Fix)
- `unverified_reference`: Reference to concept (not instruction)
- `missing_bidirectional_reference`: One-way reference detected
- `circular_reference`: Dependency cycle found
- `orphaned_entry`: No incoming/outgoing references

### Info (Consider)
- `cross_category_reference`: Reference across unrelated categories
- `low_completeness_score`: Entry below quality threshold

## Quality Gates

### Validation Levels
1. **Development** (Score ≥ 3)
   - Basic structure valid
   - Minimal documentation

2. **Testing** (Score ≥ 4)
   - Schema compliant
   - No critical errors

3. **Production** (Score ≥ 6)
   - All validations pass
   - Examples present
   - Cross-references valid

4. **Publication** (Score ≥ 7)
   - Comprehensive documentation
   - All references verified
   - No warnings

## Continuous Validation

### Pre-Commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python3 validators/repository-validator.py
if [ $? -ne 0 ]; then
    echo "Validation failed. Please fix errors before committing."
    exit 1
fi
```

### CI/CD Integration
```yaml
# .github/workflows/validate.yml
name: Validate Repository
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: python3 validators/repository-validator.py
      - uses: actions/upload-artifact@v2
        with:
          name: validation-report
          path: validation-reports/
```

## Customization

### Adding New Validation Rules
Edit `repository-validator.py` and add methods:
```python
def _validate_custom_rule(self) -> Dict[str, Any]:
    results = {}
    # Custom validation logic
    return results
```

### Modifying Error Severity
Update error classification in the validator:
```python
# Change from error to warning
self.warnings.append({...})  # Instead of self.errors.append({...})
```

### Dashboard Configuration
Edit `validation-dashboard.html` to:
- Change refresh interval
- Add new metric cards
- Customize styling
- Add chart visualizations

## Troubleshooting

### Common Issues

1. **"Schema file not found"**
   - Ensure `instruction-schema.yaml` exists in repository root
   - Check file permissions

2. **"NetworkX not installed"**
   - Install dependency: `pip install networkx`
   - Required for circular reference detection

3. **"YAML parse error"**
   - Check for syntax errors in YAML files
   - Validate indentation and special characters

4. **"Dashboard not updating"**
   - Check browser console for errors
   - Ensure JSON results file exists
   - Verify CORS settings if loading from file://

## Best Practices

### Regular Validation
- Run validation before commits
- Schedule daily full validation
- Monitor dashboard for trends

### Issue Resolution
1. Fix errors first (blocking issues)
2. Address warnings next (quality issues)
3. Review info items (improvements)

### Maintaining Quality
- Keep average completeness score > 6
- Maintain < 5% broken references
- Ensure 100% schema compliance
- Target 0 circular references

## Metrics and KPIs

### Repository Health Score
```
Health = (Schema% × 0.3) + (RefIntegrity% × 0.3) + 
         (AvgCompleteness/8 × 0.2) + (1 - ErrorRate × 0.2)
```

### Target Metrics
- Schema Compliance: 100%
- Reference Integrity: > 95%
- Average Completeness: > 6.0
- Error Rate: < 1%
- Warning Rate: < 5%

## Future Enhancements

### Planned Features
- Real-time validation API
- Automated fix suggestions
- Historical trend analysis
- Performance benchmarking
- Integration with extraction pipeline

### Proposed Validations
- Semantic consistency checking
- Example code compilation
- Dead link detection
- Duplicate content identification
- Style guide compliance