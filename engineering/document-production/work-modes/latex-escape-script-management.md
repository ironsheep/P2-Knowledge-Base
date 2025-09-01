# LaTeX Escape Script Management Guide

**Single Purpose**: Maintain rigorous control over the LaTeX escape script using regression testing

## Script Locations

**Production Script**: `/tools/latex-escape-all.sh`
**Regression Tests**: `/tools/latex-escaping-regression/`
```
tools/latex-escaping-regression/
├── README.md                    # Test suite documentation
├── latex-escape-all.sh         # Copy of production script
├── latex_escape_processor.py   # Copy of processor
├── input/                       # Test input files
├── golden/                      # Expected outputs
└── test-runner.sh              # Regression test runner
```

## Critical Testing Protocol

### Before ANY Script Changes
```bash
# 1. ALWAYS test current state first
cd tools/latex-escaping-regression/
./test-runner.sh

# 2. Only proceed if all tests pass
# 3. If tests fail - STOP and fix first
```

### Making Script Changes
```bash
# 1. Add new test case for the issue
echo "problematic content" >> input/test-cases.md

# 2. Define expected output
vim golden/test-cases-GOLDEN.md

# 3. Verify test fails (as expected)
./test-runner.sh

# 4. Fix the script
vim latex_escape_processor.py

# 5. Copy to production when tests pass
cp latex_escape_processor.py ../../tools/
cp latex-escape-all.sh ../../tools/

# 6. Final verification
./test-runner.sh
```

## Emergency Protocol

**When Script Breaks in Production:**

1. **IMMEDIATE STOP** - Don't work around it
2. **ISOLATE** - Create minimal case that reproduces issue  
3. **CLASS ANALYSIS** - Is this one bug or class of bugs?
4. **ADD TO TESTS** - Add failing case + related cases
5. **FIX COMPREHENSIVELY** - Handle entire class of problems
6. **VERIFY** - All tests pass before resuming

## The Class Problem Principle

**Every bug represents a class of bugs.**

Found one LaTeX command escaping wrong?
→ Check ALL LaTeX commands in same category
→ Test sectioning, formatting, math, references
→ Fix the entire class at once

## Current Test Coverage

**Core Test Cases**:
- Basic special characters (_, #, %, ^, &)
- LaTeX environments (preserved completely)
- Template environments (content escaped)
- Markdown headers (escaped when needed)
- Code blocks (preserved completely)

**Golden Standard**: `/tools/latex-escaping-regression/golden/`
- Contains expected output for every test case
- NEVER edit golden files casually
- Only update when behavior intentionally changes

## Integration with Document Work

**Before Using Script in Production**:
```bash
cd /tools/latex-escaping-regression/
./test-runner.sh
# Must show "✅ All tests passed!" before proceeding
```

**Script Usage**:
```bash
# Standard document processing
./tools/latex-escape-all.sh \
  "/exports/pdf-generation/workspace/smart-pins-manual/WORKING.md" \
  "/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/Document.md"
```

## Maintenance Checklist

- [ ] Production script matches regression copy
- [ ] All regression tests pass
- [ ] Golden standards are current  
- [ ] New edge cases added when discovered
- [ ] Emergency fixes follow Class Problem Principle

---

**This script is CRITICAL infrastructure. Never bypass the testing protocol.**