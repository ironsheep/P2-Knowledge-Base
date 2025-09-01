# Smart Pins Markdown Changes Guide

**Purpose**: Document all changes applied to Opus Master to create production-ready working copy

**Last Updated**: 2025-08-28

## Overview
This guide documents all markdown changes required to transform the Opus Master into a production-ready document that works with our LaTeX template system. Each change includes:
- What to change
- Why it's needed  
- How to apply it
- Verification steps

## Change Log

### 1. Add Color Block Decorations
**What**: Add language markers to code blocks for color-coding
**Why**: Triggers our 4-color system (blue/green/yellow/gray)
**How**: 
- Configuration sections: Add `{.configuration}` after opening ```
- Spin2 code: Use ````spin2`
- PASM2 code: Use ````pasm2`
- Default code: Leave unmarked for gray

**Pattern**: Most chapters have three sections:
1. Configuration constants (CON blocks) → `{.configuration}`
2. Spin2 implementation → ````spin2`
3. PASM2 implementation → ````pasm2`

**Implementation**:
```bash
# For configuration blocks after **Configuration** headers:
awk '/^\*\*Configuration\*\*$/ {print; getline; if ($0 == "```") print "```{.configuration}"; else print; next} {print}'
```

**Verification**: 
```bash
grep -c '{.configuration}' P2-Smart-Pins-Complete-Reference-WORKING.md
# Should show 26 matches
```

### 2. Change Hex Notation
**What**: Replace `0x` with `$` for hex values
**Why**: P2/Spin community convention
**How**: 
```bash
sed -i.bak 's/0x/$&/g; s/\$0x/$/g' WORKING.md
```
**Example**: `0x1F` → `$1F`

### 3. Add Hardware Diagram
**What**: Insert Smart Pins hardware diagram in Chapter 1
**Why**: Visual reference for pin architecture
**Location**: Replace existing diagram reference after "Overview" section
**Content**: 
- Image: `![Smart Pin Block Diagram](assets/smart-pins-master-trimmed.png)`
- Add Figure 1.1 caption and comprehensive narrative
- Source: `/exports/pdf-generation/workspace/smart-pins-manual/diagram-update.md`

### 4. Remove Mini-TOCs
**What**: Remove mini table of contents sections
**Why**: Clutters document, not needed with main TOC
**Status**: Already clean - no mini-TOCs found in Opus Master

### 5. Fix List Formatting
**What**: Convert certain code blocks to proper bullet lists
**Why**: Better readability, proper semantic markup
**Specific Fix Applied**:
```markdown
# Changed from:
```
Pin 0-31:  Direct addressing in instruction
```
# To:
- **Pin 0-31**: Direct addressing in instruction
```

### 6. Convert Code Blocks to Tables (Appendix B)
**What**: Convert code-formatted tables to proper markdown tables
**Why**: Better formatting, proper alignment
**Location**: Appendix B - Configuration Calculator
**Tables Converted**:
1. UART Baud Rate Settings (12 rows)
2. PWM Frequency Settings (9 rows)
3. NCO Frequency Values (7 rows)

**Format**:
```markdown
| Frequency | WYPIN Value (hex) | Actual Freq | Error |
|-----------|-------------------|-------------|-------|
| 1 Hz      | `$00A7C5AC`       | 1.000 Hz    | 0.000% |
```

### 7. Apply Monospace to Mode Headers
**What**: Add monospace formatting to mode values in headers
**Why**: Consistent appearance in TOC
**How**: 
```bash
sed -i 's/^### Mode %\([0-9]*\)/### Mode `%\1`/g' WORKING.md
```
**Result**: `### Mode %00010` → `### Mode `%00010``

### 8. Special Formatting for Anti-Patterns
**What**: Mark anti-pattern examples with `{.antipattern}`
**Why**: These show what NOT to do - need visual distinction (red boxes)
**Location**: Common Beginner Mistakes section
**How**: 
- Separate WRONG and RIGHT examples into different code blocks
- Mark WRONG examples with `{.antipattern}`
- Keep RIGHT examples as normal `spin2` blocks

**Applied to**:
1. Mistake 1: Forgetting Output Enable
2. Mistake 2: Wrong Period Calculation
3. Mistake 3: Not Clearing Before Reconfigure

## CRITICAL FILE NAMING RULES

### NO SUFFIXES - EVER
**NEVER create files with suffixes like:**
- ❌ `smart-pins-block-coloring-v2.lua`
- ❌ `p2kb-foundation-fixed.sty`
- ❌ `P2-Smart-Pins-Complete-Reference-FINAL.md`

**ALWAYS use production names:**
- ✅ `smart-pins-block-coloring.lua`
- ✅ `p2kb-foundation.sty`
- ✅ `P2-Smart-Pins-Complete-Reference.md`

**WHY**: Suffixes break references, create confusion, and violate our production workflow.

## Notes for Future Recovery

### File Locations
- **Opus Master**: `/exports/pdf-generation/workspace/smart-pins-manual/opus-master/COMPLETE-OPUS-MASTER.md`
- **Working Copy**: `/exports/pdf-generation/workspace/smart-pins-manual/P2-Smart-Pins-Complete-Reference-WORKING.md`
- **Deployment**: `/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/`

### Complete Recovery Workflow
1. Copy Opus Master to Working Copy
2. Apply all changes in this guide systematically
3. Run LaTeX escape script: `./tools/latex-escape-all.sh WORKING.md escaped.md`
4. Copy escaped markdown to outbound
5. Copy templates from workspace/manual-templates/ to outbound
6. User deploys to PDF Forge and generates PDF
7. Review PDF and iterate with additional changes

### Template Requirements
The following templates must be present on PDF Forge:
- `p2kb-foundation.sty` - Base layer
- `p2kb-smart-pins-content.sty` - Content styles with color blocks
- `p2kb-tech-review.sty` - Presentation layer
- `smart-pins-block-coloring.lua` - Lua filter for color transformations

### Update History
- 2025-08-28: Initial guide created from recovery effort
- 2025-08-28: Applied all changes to fresh copy from Opus Master

## Changes Applied Today (2025-08-28)

### ✅ Successfully Applied:
1. **Configuration block decorations** - Added `{.configuration}` to 26 configuration blocks
2. **Hex notation** - Changed 7 instances from `0x` to `$`
3. **Hardware diagram** - Inserted new diagram and narrative in Chapter 1
4. **List formatting** - Fixed pin addressing list (converted from code block)
5. **Tables in appendices** - Converted 3 code blocks to proper markdown tables in Appendix B
6. **Monospace mode headers** - Added backticks to mode values in headers (26 mode headers)
7. **Anti-pattern formatting** - Added `{.antipattern}` marker to 3 "WRONG" examples

### 📝 Implementation Notes:
- Mini-TOCs were already clean (none found to remove)
- Used sed/awk for bulk changes where possible
- Separated WRONG/RIGHT examples in mistakes section for clarity
- All changes preserve document structure and content