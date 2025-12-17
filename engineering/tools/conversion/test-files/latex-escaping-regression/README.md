# LaTeX Escaping Regression Testing Framework

## Purpose
Track and validate LaTeX special character escaping for P2 Assembly Manual generation.

## Current Script Version
- **Script**: `latex-escape-all.sh` + `latex_escape_processor.py`
- **Last Modified**: 2025-12-17 (v7 - Pandoc superscript syntax protection added)
- **Performance Target**: < 30 seconds for full document processing
- **Current Status**: Working correctly - protects code blocks, fenced divs, image paths, trailing backslashes, grid tables, hypertarget commands, PASM2 absolute address syntax, Pandoc superscript syntax; escapes P2 literals

## Test Coverage

### ✅ Currently Handled
1. **Pandoc Superscript Syntax Protection** (NEW in v7)
   - `^text^` patterns (Pandoc superscript syntax) are NOT escaped
   - Pandoc converts `^text^` to `\textsuperscript{text}` in LaTeX
   - Without protection, `^` becomes `\^{}` which Pandoc outputs as literal `^{}`
   - Bare `^{}` in LaTeX causes "Missing $ inserted" error (invalid outside math mode)
   - Standalone carets (like `2^9`) are still escaped correctly
   - Test Case: `test-cases.md` → "Pandoc Superscript Syntax Test"

2. **Hypertarget Command Protection** (v6)
   - `\hypertarget{anchor}{}` commands are NOT escaped
   - Used for Pandoc cross-reference anchors in combined instruction groups
   - Test Case: `test-cases.md` → "Hypertarget Anchor Commands Test"

2. **PASM2 Absolute Address Protection** (NEW in v6)
   - `#\Label` and `\Label` syntax for absolute addresses NOT escaped
   - P2 uses backslash prefix for absolute vs relative addressing
   - Produces proper `\#\\Label` output for LaTeX
   - Test Case: Added to production but deferred test case

3. **Grid Table Protection** (v5)
   - Grid tables (using `+---+` borders) are NOT escaped at all
   - Escaping `%` → `\%` adds a character, breaking column alignment
   - Broken alignment causes Pandoc to misparse the entire table structure
   - Pipe tables (using `|---|`) ARE still escaped (no alignment issues)
   - Test Case: `test-cases.md` → "Grid Table Alignment Test"

2. **Trailing Backslash Preservation** (v4)
   - Trailing `\` at end of line is Pandoc hard line break syntax
   - Preserved as-is (NOT escaped to `\textbackslash{}`)
   - Used for multi-line operand lists in instruction documentation
   - Test Case: `test-cases.md` → "Trailing Backslash Test"

3. **Pandoc Fenced Divs** (v3)
   - `::: pasm2` / `::: spin2` / `::: cordic` / `::: multicog` / `::: antipattern` - Code NOT escaped
   - Content between `:::` and closing `:::` is preserved exactly
   - Text outside fenced divs is still escaped normally

4. **Markdown Image Paths** (v2)
   - `![alt](path/with_underscores.png)` - NOT escaped
   - `[link](file.ext)` - NOT escaped if contains extension
   - Preserves spaces and underscores in paths

5. **Basic LaTeX Special Characters**
   - `#` → `\#` (except in markdown headers)
   - `$` → `\$`
   - `%` → `\%`
   - `&` → `\&`
   - `_` → `\_`
   - `^` → `\^{}`
   - `{` → `\{`
   - `}` → `\}`

6. **Protected Contexts**
   - Code blocks (```pasm2, ```spin2, etc.) - NO escaping
   - Fenced divs (::: pasm2, ::: spin2, etc.) - NO escaping (v3)
   - Grid tables (`+---+` style) - NO escaping (v5)
   - Standard LaTeX environments (equation, align, etc.) - NO escaping
   - Template environments (sidetrack, interlude, etc.) - content IS escaped

7. **LaTeX Commands Preserved**
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

### ✅ Fixed Issues (v2)
1. **Image Path Protection**
   - Previously: Underscores in image paths were escaped
   - Now: Image paths are protected from all escaping
   - Test Case: `test-image-paths-fixed.md`

2. **P2 Literals Still Protected**
   - Text with `#immediate`, `$hex`, `%binary` properly escaped
   - Image paths remain clean for Pandoc
   - Test Case: `test-p2-literals-escaped.md`

## Regression Test Files

### Basic Tests
- `test-image-paths.md` - Various image path patterns (v2: now protected)
- `test-p2-literals.md` - P2 special characters in text (v2: still escaped)
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

### 2025-12-17: Version 7 Released
- **Pandoc Superscript Syntax Protection**: `^text^` patterns are preserved for Pandoc processing
- **Root Cause**: Encoding tables in PASM2 manual use `D^1^` notation for footnote references
- **Bug Chain**:
  1. Markdown has `D^1^` (Pandoc superscript syntax)
  2. Escape script converted `^` to `\^{}` producing `D\^{}1\^{}`
  3. Pandoc interpreted `\^` as escaped caret (literal character)
  4. Pandoc output `D^{}1^{}` to LaTeX
  5. Bare `^` in LaTeX (outside math mode) caused "Missing $ inserted" error
- **Solution**: Protect `^text^` patterns before caret escaping, restore unchanged after
- **Pattern**: `\^([^^\s]+)\^` matches paired carets with non-whitespace content
- **Standalone carets** (like `2^9`) are still escaped correctly as `2\^{}9`
- **Test Added**: "Pandoc Superscript Syntax Test" section in test-cases.md

### 2025-12-13: Version 6 Released
- **Hypertarget Command Protection**: `\hypertarget{anchor}{}` commands are preserved
- **Root Cause**: Combined instruction groups (RESI0/1/2/3, SETINT1/2/3, etc.) use hypertargets for cross-reference anchors
- **Impact**: Without protection, `\hypertarget{resi1}{}` becomes `\textbackslash\{\}hypertarget\{resi1\}\{\}` appearing literally in PDF
- **Solution**: Added regex pattern to protected LaTeX command list: `r'\\hypertarget\{([^}]*)\}\{([^}]*)\}'`
- **PASM2 Absolute Address Protection**: `#\Label` and `\Label` syntax preserved
- **Root Cause**: P2 assembly uses backslash prefix for absolute addressing vs relative
- **Impact**: `CALLB #\Addr` was rendering as `CALLB \#\{\}Addr` in PDF
- **Solution**: Pre-protect patterns before escaping, restore with proper double-backslash for LaTeX
- **Test Added**: "Hypertarget Anchor Commands Test" section in test-cases.md

### 2025-12-05: Version 5 Released
- **Grid Table Protection**: Grid tables (using `+---+` border syntax) are completely protected from escaping
- **Root Cause**: Escaping `%` → `\%` in grid tables adds characters that break column alignment
- **Impact**: Broken alignment causes Pandoc to fail to recognize the grid table structure, resulting in complete parse failure (PDF errors like "Misplaced \noalign")
- **Solution**: Detect grid table lines and skip ALL escaping inside grid tables
- **Pipe Tables**: Still escaped normally (pipe tables are more forgiving of alignment)
- **Test Added**: "Grid Table Alignment Test (Bug Fix - Grid Tables with %)" section in test-cases.md
- **Real-World Fix**: PASM2 manual Appendix E instruction encoding tables with binary patterns like `%AAAAA111F`

### 2025-12-05: Version 4 Released
- **Trailing Backslash Preservation**: Single trailing `\` at end of line preserved for Pandoc hard line breaks
- **Use Case**: Instruction operand lists with multiple lines (e.g., `**TESTP** *{#}Dest* WC/WZ\`)
- **Bug Fixed**: Trailing backslash was incorrectly escaped to `\textbackslash{}` breaking multi-line layouts
- **Impact**: PASM2 manual instruction documentation uses trailing backslashes for operand formatting
- **Test Added**: "Trailing Backslash Test (Pandoc Hard Line Breaks)" section in test-cases.md

### 2025-12-05: Version 3 Released
- **Fenced Div Protection**: Added protection for `::: type` Pandoc fenced divs
- **Code Types Protected**: pasm2, spin2, cordic, multicog, antipattern, pasm, spin
- **Bug Fixed**: Issue #324 - underscores/hash/dollar in fenced div code blocks were incorrectly escaped
- **Impact**: PASM2 manual, DeSilva manual, Smart Pins tutorial all use fenced divs extensively

### 2025-08-27: Version 2 Released
- **Image Path Protection**: Added protection for markdown image/link syntax
- **Script Enhancement**: Images and links with file extensions are not escaped
- **Maintained**: P2 literals in text still properly escaped
- **Performance**: Still < 1 second for test files

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