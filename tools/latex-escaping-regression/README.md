# LaTeX Escaping Regression Testing Framework

## Purpose
Track and validate LaTeX special character escaping for P2 Assembly Manual generation.

## Current Script Version
- **Script**: `latex-escape-all.sh` + `latex_escape_processor.py`
- **Last Modified**: 2025-08-27
- **Performance Target**: < 30 seconds for full document processing
- **Current Status**: Working with known deferrals

## Test Coverage

### ✅ Currently Handled
1. **Basic LaTeX Special Characters**
   - `#` → `\#` (except in markdown headers)
   - `$` → `\$`
   - `%` → `\%`
   - `&` → `\&`
   - `_` → `\_`
   - `^` → `\^{}`
   - `{` → `\{`
   - `}` → `\}`

2. **Protected Contexts**
   - Code blocks (```pasm2, ```spin2, etc.) - NO escaping
   - Standard LaTeX environments (equation, align, etc.) - NO escaping
   - Template environments (sidetrack, interlude, etc.) - content IS escaped

3. **LaTeX Commands Preserved**
   - `\textbf{}`, `\textit{}`, `\emph{}`, etc.
   - `\section{}`, `\subsection{}`, etc. (content inside {} IS escaped)
   - Spacing commands (`\vspace{}`, `\quad`, etc.)
   - Reference commands (`\ref{}`, `\label{}`, etc.)

### ⏸️ Deferred Until First PDF
1. **P2 Numeric Literals with Underscores**
   - Pattern: `25_000_000` (numeric separators)
   - Pattern: `$FF_AA_BB` (hex with underscores)
   - Decision: Wait to see if problematic in PDF output
   - Rationale: Underscores are valid except as first character

2. **Bit Indexing Patterns**
   - Pattern: `bits[15:0]`
   - Decision: Wait to see if problematic
   - Rationale: May not need escaping in practice

### 🔍 Known Issues to Monitor
1. **URL-Encoded Image Paths**
   - Symptom: `%20` in paths gets escaped to `\%20`
   - Impact: Unknown - need to test with actual PDF generation
   - Test Case: `test-url-encoded.md`

2. **Image Paths with Spaces**
   - Current: Spaces preserved, underscores escaped
   - Question: Does Pandoc URL-encode these automatically?
   - Test Case: `test-image-paths.md`

## Regression Test Files

### Basic Tests
- `test-image-paths.md` - Various image path patterns
- `test-url-encoded.md` - Pre-encoded URL paths
- `latex-escaping-test-cases-GOLD-STANDARD.md` - Comprehensive test suite

### Performance Benchmark
- Target: < 30 seconds for full Smart Pins document (~400 pages)
- Current: 0 seconds for small test files
- Script includes automatic timing and warnings

## Testing Workflow

1. **Before Making Changes**
   ```bash
   # Run regression tests
   bash ./tools/latex-escape-all.sh tools/latex-escaping-test-cases-GOLD-STANDARD.md /tmp/test-output.md
   
   # Check timing (displayed automatically)
   # Check verification counts (displayed automatically)
   ```

2. **After Making Changes**
   ```bash
   # Same test, compare results
   diff /tmp/test-output.md tools/latex-escaping-test-cases-SCRIPT-OUTPUT-V9.md
   ```

3. **Production Validation**
   ```bash
   # Time the real document
   time bash ./tools/latex-escape-all.sh [large-document].md [output].md
   # Should complete in < 30 seconds
   ```

## Decision Log

### 2025-08-27: Deferred Decisions
- **Underscores in numerics**: Wait for PDF to show problems
- **Bit indexing**: Wait for PDF to show problems  
- **Rationale**: "Defer until we see them, then hit a class of them"
- **Performance**: Added timing to script, 30-second warning threshold

### Future Enhancements (When Needed)
1. Add P2-specific numeric pattern handling
2. Add bit indexing pattern preservation  
3. Consider inline test mode (decided against for now)
4. Optimize for large documents if > 30 seconds

## Maintenance Notes

- Script uses Python for complex regex operations
- Bash wrapper provides timing and verification
- Backup created automatically with timestamp
- Performance monitoring built-in (warns if > 30 seconds)