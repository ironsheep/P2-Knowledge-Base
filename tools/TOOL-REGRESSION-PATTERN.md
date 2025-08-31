# Tool Regression Testing Pattern

## Overview
This document defines our standard pattern for creating and maintaining regression-tested tools in the P2 Knowledge Base project. Every tool that transforms data should follow this pattern to ensure reliability and maintainability.

## Directory Structure Pattern

```
tools/
├── TOOL-REGRESSION-PATTERN.md         # This document
├── [tool-name]/                       # Production tool directory
│   ├── [tool-name].sh                 # Main script
│   ├── [tool-name]_processor.*        # Processing engine (if separate)
│   └── README.md                       # Tool documentation
│
└── [tool-name]-regression/            # Regression test directory
    ├── README.md                       # Test suite documentation
    ├── [tool-name].sh                  # Copy of production script
    ├── [tool-name]_processor.*         # Copy of processing engine
    ├── input/                          # Test input files
    │   ├── test-cases.md               # Primary test input
    │   └── edge-cases.md               # Edge case inputs
    ├── golden/                         # Golden output files
    │   ├── test-cases-GOLDEN.md       # Expected output
    │   └── edge-cases-GOLDEN.md       # Expected edge case output
    └── test-runner.sh                  # Regression test runner
```

## Core Principles

### 1. Separation of Concerns
- **Production code** lives in `tools/[tool-name]/`
- **Test assets** live in `tools/[tool-name]-regression/`
- Never mix production and test files

### 2. Golden Standard Pattern
- **INPUT**: What goes into the tool
- **GOLDEN**: What should come out
- **ACTUAL**: What the tool produces (not versioned)
- Test passes when ACTUAL matches GOLDEN exactly

### 3. Regression Test Workflow

```bash
# Standard test execution:
cd tools/[tool-name]-regression/
./test-runner.sh

# When test fails:
# 1. STOP all other work
# 2. Fix the issue
# 3. Re-run tests
# 4. Only proceed when tests pass
```

## Creating a New Regression-Tested Tool

### Step 1: Create Tool Directory
```bash
mkdir tools/my-tool
mkdir tools/my-tool-regression
mkdir tools/my-tool-regression/input
mkdir tools/my-tool-regression/golden
```

### Step 2: Create Test Runner
Use this template for `test-runner.sh`:

```bash
#!/bin/bash
# Regression test runner for [tool-name]

TOOL_NAME="[tool-name]"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running regression tests for $TOOL_NAME..."

# Test each input/golden pair
for input_file in input/*.md; do
    base=$(basename "$input_file" .md)
    
    # Run the tool
    ./${TOOL_NAME}.sh "input/$base.md" "output/$base.md"
    
    # Compare with golden
    if diff -q "output/$base.md" "golden/$base-GOLDEN.md" > /dev/null; then
        echo "✅ PASS: $base"
    else
        echo "❌ FAIL: $base"
        echo "Differences:"
        diff "output/$base.md" "golden/$base-GOLDEN.md"
        exit 1
    fi
done

echo "✅ All tests passed!"
```

### Step 3: Document the Tool
Create README.md in regression directory with:
- Purpose of the tool
- How to run tests
- How to add new test cases
- Emergency procedures when tests fail

## When Tools Fail - Emergency Protocol

### Generic Fix Process
1. **IMMEDIATE STOP** - Don't try to work around it
2. **ISOLATE** - Create minimal test case that reproduces issue
3. **CLASS ANALYSIS** - Is this one bug or a class of bugs?
4. **ADD TO TESTS** - Add failing case AND related cases to input/
5. **UPDATE GOLDEN** - Define expected output for all cases
6. **VERIFY FAILURE** - Run tests, confirm they fail
7. **FIX COMPREHENSIVELY** - Update tool to handle entire class
8. **VERIFY SUCCESS** - Run tests, confirm they pass
9. **RESUME** - Only after all tests pass

### The Class Problem Principle
**CRITICAL**: Every bug is a symptom of a class of bugs.

When you find a problem:
- ❌ DON'T just fix that one instance
- ✅ DO identify the entire class of similar problems
- ✅ DO fix all of them at once

**Generic Examples**:
- Found one special character breaking? → Check ALL special characters
- Found one edge case number? → Test negative, zero, max values
- Found one file type failing? → Test all supported file types
- Found one escape sequence broken? → Review entire escape handling

This prevents future breaks and reduces maintenance cycles.

### Tool-Specific Regression Patterns

**For PDF/LaTeX tools**: See `/pipelines/pdf-generation-workflow-v2.md` section on "Regression Testing Critical Scripts"
- Includes Class Problem Principle for LaTeX escaping
- Specific examples of LaTeX command classes
- PDF generation emergency procedures

**For other tools**: Follow the generic pattern above, adapting as needed for tool specifics

### Adding Test Cases
```bash
# 1. Add problematic pattern to input file
echo "problematic pattern" >> input/test-cases.md

# 2. Run tool to see current behavior
./[tool-name].sh input/test-cases.md output/test-cases.md

# 3. Manually create correct output
vim golden/test-cases-GOLDEN.md  # Edit to correct output

# 4. Fix tool if needed
vim [tool-name]_processor.py

# 5. Verify fix
./test-runner.sh
```

## Integration Points

### PDF Pipeline Integration
- Tools are called at specific pipeline stages
- Each tool must pass regression before pipeline runs
- Pipeline documentation references tool regression status

### Version Control
```gitignore
# Never version control test outputs
tools/*/output/
tools/*-regression/output/

# Do version control golden standards
!tools/*-regression/golden/
```

## Current Regression-Tested Tools

| Tool | Purpose | Test Coverage | Last Updated |
|------|---------|---------------|--------------|
| latex-escape-all | Escape LaTeX special characters | Full | 2025-08-21 |
| (future tools listed here) | | | |

## Pattern Compliance Checklist

When creating or updating a tool:
- [ ] Tool has dedicated directory
- [ ] Regression tests in separate directory
- [ ] Input files in `input/`
- [ ] Golden files in `golden/`
- [ ] Test runner script exists
- [ ] README documents test process
- [ ] Emergency protocol documented
- [ ] Integration points identified
- [ ] Added to tools inventory above

## Future Considerations

As we add more tools:
1. Consider shared test utilities
2. May need tool dependency management
3. Could benefit from test result dashboard
4. Might want automated test runs on changes

---
*This pattern ensures every tool we create is reliable, testable, and maintainable.*