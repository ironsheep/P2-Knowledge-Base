# Green Book Markdown Changes Guide

**Purpose**: Document all changes needed to transform Green Book Tutorial into production-ready document that works with our LaTeX template system

**Document**: P2-Smart-Pins-Green-Book-Tutorial.md
**Last Updated**: 2025-08-31

## 🔴 CRITICAL: DIV-ONLY APPROACH

**DECISION**: All code blocks MUST use div syntax (`::: type`) for consistency and future maintainability.
- NO language tags (````spin2`, ````pasm2`)
- NO mixed approaches
- ALL code blocks wrapped in semantic divs
- Lua filters will ONLY process div syntax

## Overview
This guide documents the REQUIRED markdown transformations to convert the Green Book to our standardized div-based syntax. All code blocks must be converted to div environments for proper LaTeX processing.

## Current State Analysis

### Source Document Assessment
**Document**: P2-Smart-Pins-Green-Book-Tutorial (opus-master/COMPLETE-OPUS-MASTER.md)
**Working File**: P2-Smart-Pins-Green-Book-Tutorial-working.md

### Code Block Inventory
**Found 88 code blocks** currently using language tags:
- `spin2` blocks: 58 instances → MUST convert to `::: spin2`
- `pasm2` blocks: 30 instances → MUST convert to `::: pasm2`
- Mixed antipattern blocks: Several instances → MUST split and wrap
- Configuration blocks with WRPIN: → Keep as `::: spin2` (pedagogical decision)

### Semantic Div Status
**Found 26 semantic divs** already using correct syntax:
- `needs-diagram`: 18 instances ✅
- `needs-technical-review`: 1 instance ✅
- `needs-examples`: 2 instances ✅
- `needs-verification`: 2 instances ✅
- `needs-code-review`: 1 instance ✅
- `tip`: 2 instances ✅
- `preliminary-content`: 2 instances ✅

## Known Issues and Solutions

### LaTeX Image Float Problem ✅ **IMPLEMENTED**
**Issue**: LaTeX moves images to "optimize" page layout, causing them to appear at page tops instead of where referenced in narrative. This can split code blocks and break the tutorial flow.

**Solution**: Use `non-floating-images.lua` filter to convert all images to non-floating, centered images that stay exactly where placed.

**Design Decision - 85% Width**:
- Images default to 85% of text width for visual breathing room
- Prevents images from dominating the narrative
- Creates professional appearance with clear text/image hierarchy
- Easily adjustable in the Lua filter if needed
- Individual images can override with explicit width attributes

**Implementation Status**: ✅ **COMPLETED** (2025-09-02)
- Filter copied to workspace/filters/non-floating-images.lua
- Images already in correct format (simple markdown syntax)
- Default 85% width pre-planned and confirmed

**Implementation**: Add to pandoc args:
```json
"lua_filters": [
  "smart-pins-div-blocks",
  "non-floating-images",  // Keeps images in place
  "part-chapter-pagebreaks"
]
```

## Required Transformations

### 1. Automated Code Block Conversion 🚀 **USE SCRIPT**

**Automated Tool**: `/engineering/tools/convert-to-div-syntax.py`
```bash
python3 /engineering/tools/convert-to-div-syntax.py input.md output.md
```

**What the script handles**:
- ✅ Converts all `spin2` and `pasm2` blocks to div syntax
- ✅ Automatically adds blank lines where needed (prevents colons showing in PDF)
- ✅ Splits antipattern blocks (WRONG/RIGHT patterns)
- ✅ Provides statistics on conversions and blank lines added

**Critical blank line handling**: The script detects when text immediately precedes a code block and inserts a blank line before the div opener. This prevents the colons from appearing in the final PDF (a problem found in Master V3).

### 1.1 Antipattern Code Block Splitting (handled by script) ⚠️ **CRITICAL**

**Location**: Throughout the tutorial, teaching moments (3-4 occurrences expected)
**Pattern**: Single code blocks containing both failing and working code
**Detection**: Spin2 uses single tick marks for comments. Look for ALL these patterns:
- `' WRONG - [explanation]` followed by incorrect code
- `' RIGHT - [explanation]` followed by correct code
- `' This won't work` followed by incorrect code
- `' This works` followed by correct code
- `' This blinks at [wrong rate]` followed by incorrect code
- `' This blinks at [correct rate] correctly` followed by correct code
- `' First configuration` followed by initial code
- `' Trying to change` followed by problematic code
- `' Correct way` followed by working code

**CRITICAL**: Search for sections titled **Mistake 1:**, **Mistake 2:**, **Mistake 3:** as these contain the antipattern blocks

**Known Antipattern Blocks (typically 3 occurrences):**
1. **Mistake 1: Forgetting Output Enable**
   - Pattern: "This won't work" / "This works"
2. **Mistake 2: Wrong Timing Calculation**
   - Pattern: "This blinks at 0.5Hz" / "This blinks at 1Hz correctly"
3. **Mistake 3: Not Clearing Before Reconfiguring**
   - Pattern: "First configuration" / "Trying to change" / "Correct way"

**Required Action**: Split each mixed code block into separate blocks:
- Code with `' WRONG` comments → `::: antipattern` div environment (red)
- Code with `' RIGHT` comments → `::: spin2` div environment (green)

**Example Transformation**:
```markdown
<!-- BEFORE (current v3) -->
```spin2
' WRONG - Pin won't output
wrpin(P_TRANSITION, LED_PIN)

' RIGHT - Include P_OE
wrpin(P_TRANSITION | P_OE, LED_PIN)
```

<!-- AFTER (required) -->
::: antipattern
```
' WRONG - Pin won't output
wrpin(P_TRANSITION, LED_PIN)
```
:::

::: spin2
```
' RIGHT - Include P_OE
wrpin(P_TRANSITION | P_OE, LED_PIN)
```
:::
```

**Note**: Spin2 uses single tick marks (') for comments, not double slashes (//)

### 2. Missing Image Placeholder Replacement 🖼️ **NEW REQUIREMENT**

**Purpose**: Replace missing images with informative placeholder blocks so PDF generation doesn't fail

**Process**:
1. Check each image reference against assets/ folder
2. If image doesn't exist, replace with placeholder div block
3. Preserve the description for future reference

**Transformation**:
```markdown
<!-- BEFORE (missing image) -->
![UART Frame Structure](assets/uart-frame-structure.png)

<!-- AFTER (placeholder block) -->
::: needs-diagram
Image showing "UART Frame Structure" is missing and should be added.
Expected file: assets/uart-frame-structure.png
:::
```

**Missing Images to Replace**:
- `smps-timing-diagram.png` → "SMPS Timing Diagram"
- `ab-encoder-timing.png` → "A-B Encoder Timing"
- `comparator-operation.png` → "Comparator Operation"
- `uart-frame-structure.png` → "UART Frame Structure"
- `adc-operation-diagram.png` → "ADC Operation Diagram"

### 3. Code Block Environment Conversion 🔄 **REQUIRED**

**MANDATORY**: ALL code blocks must use div-wrapped format. NO exceptions.

**Language-Tagged Blocks (OLD - FORBIDDEN)**:
```markdown
```spin2
code here
```
```

**Div-Wrapped Blocks (NEW - REQUIRED)**:
```markdown
::: spin2
```
code here
```
:::
```

**Required Conversions**:
- ALL `spin2` blocks → `::: spin2` (including those with WRPIN:)
- ALL `pasm2` blocks → `::: pasm2`
- Split antipattern blocks → `::: antipattern` and `::: spin2`
- NO blocks remain with language tags

## 3-Color Code Block System (Pedagogical Decision)

### Color Mappings (AFTER div conversion)

**🟢 GREEN - Spin2 Blocks** (all Spin2 including config)
- Markdown: `::: spin2`
- LaTeX Environment: `Spin2Block`
- Lua Detection: Div with class "spin2"
- **Includes**: Regular code AND configuration (WRPIN:/WXPIN:/WYPIN:)

**🟡 YELLOW - PASM2 Blocks** (30 instances)
- Markdown: `::: pasm2`
- LaTeX Environment: `PASM2Block`
- Lua Detection: Div with class "pasm2"

**🔴 RED - Antipattern Blocks** (created from split blocks)
- Markdown: `::: antipattern`
- LaTeX Environment: `AntipatternBlock`
- Lua Detection: Div with class "antipattern"

### Pedagogical Rationale - A Conscious Decision

**We considered creating a separate `::: configuration` div for WRPIN: blocks** but decided AGAINST it:

**Why we considered it:**
- Would provide visual distinction between setup and action code
- Could help pattern recognition for initialization
- Matches the reference manual's 4-color system

**Why we rejected it:**
- **Tutorial flow** - Configuration IS part of the learning sequence
- **Reduces complexity** - 3 colors (green/yellow/red) is cleaner than 4
- **Natural learning** - Students should see config as normal code, not special
- **Self-documenting** - WRPIN:/WXPIN:/WYPIN: patterns are obvious without color
- **IDE reality** - Their editor won't color these differently

**Decision**: Configuration blocks remain `::: spin2` (green) for pedagogical clarity.

### Verification Checklist
- [ ] NO language-tagged blocks remain (no ````spin2`, ````pasm2`)
- [ ] ALL code blocks use div syntax (`::: type`)
- [ ] Antipattern blocks properly split
- [ ] Configuration blocks remain as `::: spin2` (not separate)

## Semantic Environment Mappings

### Current Implementation Status
✅ **All 26 semantic divs properly formatted**

### Lua Filter Requirements

**CRITICAL**: Use `smart-pins-div-blocks.lua` instead of `smart-pins-colored-blocks.lua`
- The new filter processes Div elements (::: syntax)
- The old filter processes CodeBlock elements (``` syntax)
- Both filters should NOT be used together

### Environment Mappings (green-book-semantic-blocks.lua)

**🔵 gbdiagram** (18 instances)
- Markdown: `::: needs-diagram`
- Purpose: Placeholder for missing technical diagrams
- Status: 8 instances will be replaced with actual images in deployment

**🟡 gbtip** (2 instances)
- Markdown: `::: tip`
- Purpose: Helpful tips and insights

**🟠 gbexamples** (2 instances)
- Markdown: `::: needs-examples`
- Purpose: Placeholder for additional code examples

**🟣 gbverify** (2 instances)
- Markdown: `::: needs-verification`
- Purpose: Content requiring technical verification

**🔴 gbtechreview** (1 instance)
- Markdown: `::: needs-technical-review`
- Purpose: Complex content needing expert review

**🟢 gbcodereview** (1 instance)
- Markdown: `::: needs-code-review`
- Purpose: Code examples needing verification

**⚪ gbpreliminary** (2 instances)
- Markdown: `::: preliminary-content`
- Purpose: Draft content not yet finalized

## CRITICAL FILE NAMING RULES

### NO SUFFIXES - EVER
**NEVER create files with suffixes like:**
- ❌ `green-book-semantic-blocks-v2.lua`
- ❌ `p2kb-smart-pins-content-fixed.sty`
- ❌ `P2-Smart-Pins-Green-Book-Tutorial-FINAL.md`

**ALWAYS use production names:**
- ✅ `green-book-semantic-blocks.lua`
- ✅ `p2kb-smart-pins-content.sty`
- ✅ `P2-Smart-Pins-Green-Book-Tutorial.md`

**WHY**: Suffixes break references, create confusion, and violate our production workflow.

## Processing Philosophy

**Goal**: Minimal markdown changes + maximum stylesheet/Lua intelligence = rich output

**Preference Order**:
1. **Lua Filter Solution** - Can we detect and handle automatically?
2. **Stylesheet Solution** - Can we handle with better LaTeX rules?
3. **Markdown Change** - Only if processing pipeline cannot handle

## File Locations

- **Green Book v0**: `/documentation/manuals/smart-pins-workshop/opus-master-green-book/P2-Smart-Pins-Green-Book-Tutorial-v0.md`
- **Green Book v2**: `/documentation/manuals/smart-pins-workshop/opus-master-green-book/P2-Smart-Pins-Green-Book-Tutorial-v2.md`
- **Working Copy**: `/exports/pdf-generation/workspace/smart-pins-manual/P2-Smart-Pins-Green-Book-Tutorial-working.md`
- **Escaped Copy**: `/exports/pdf-generation/workspace/smart-pins-manual/P2-Smart-Pins-Green-Book-Tutorial-escaped.md`
- **Deployment**: `/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/`

## Template Requirements

The following templates must work with Green Book:
- `p2kb-foundation.sty` - Base layer
- `p2kb-smart-pins-content.sty` - Content styles with 4-color blocks + semantic environments
- `p2kb-tech-review.sty` - Presentation layer
- `smart-pins-colored-blocks.lua` - 4-color code block processing
- `green-book-semantic-blocks.lua` - Semantic div processing
- `part-chapter-pagebreaks.lua` - Page break handling

## Systematic Transformation Guide: v3 → LaTeX-Ready

### 📋 EXECUTIVE SUMMARY: TARGETED TRANSFORMATIONS REQUIRED

**The Green Book v3 needs specific antipattern splitting and code block environment conversion for optimal LaTeX processing.**

### Deployment Workflow

**Step 1: Apply ALL Transformations** 🔄
```bash
# Start with master document
cp opus-master/COMPLETE-OPUS-MASTER.md \
   P2-Smart-Pins-Green-Book-Tutorial-working.md

# Apply transformations (manual or scripted):
# - Convert all language-tagged to div-wrapped
# - Split antipattern blocks
# - Identify and wrap configuration blocks
```

**Step 2: Verify Transformations** ✅
```bash
# Should return 0 - no language tags remain
grep -c '^```[sp]' P2-Smart-Pins-Green-Book-Tutorial-working.md

# Should show div blocks
grep -c '^:::' P2-Smart-Pins-Green-Book-Tutorial-working.md
```

**Step 3: LaTeX Escaping**
```bash
./tools/latex-escape-all.sh \
  P2-Smart-Pins-Green-Book-Tutorial-working.md \
  P2-Smart-Pins-Green-Book-Tutorial-escaped.md
```

**Step 4: Deploy with Updated Filters**
- Template: `p2kb-smart-pins.latex`
- Lua Filters:
  - `smart-pins-div-blocks.lua` - NEW filter for div-wrapped code blocks (replaces smart-pins-colored-blocks.lua)
  - `green-book-semantic-blocks.lua` - Semantic div processing
  - `part-chapter-pagebreaks.lua` - Page break handling
- **IMPORTANT**: Do NOT use smart-pins-colored-blocks.lua with div-wrapped content

### Quality Assurance Checklist

**Code Block Verification** ✅
- [ ] All `spin2` blocks → green rendering (including config)
- [ ] 30 `pasm2` blocks → yellow rendering
- [ ] Split antipattern blocks → red rendering
- [ ] NO separate configuration blocks (pedagogical choice)

**Semantic Div Verification** ✅
- [ ] 18 `needs-diagram` → gbdiagram environments
- [ ] 2 `tip` → gbtip environments
- [ ] 2 `needs-examples` → gbexamples environments
- [ ] 2 `needs-verification` → gbverify environments
- [ ] 1 `needs-technical-review` → gbtechreview environment
- [ ] 1 `needs-code-review` → gbcodereview environment
- [ ] 2 `preliminary-content` → gbpreliminary environments

**LaTeX Template Compatibility** ✅
- [ ] Headers follow proper hierarchy for pagebreaks
- [ ] Images use standard markdown syntax
- [ ] No manual LaTeX commands in content
- [ ] Proper pandoc div syntax throughout

### Post-Processing Verification

**After PDF Generation:**
1. **Visual Check**: All 87 code blocks properly colored
2. **Semantic Check**: All 26 semantic divs properly styled
3. **Layout Check**: Headers, pagebreaks, and flow correct
4. **Image Check**: All referenced images display correctly

### Backup Strategy

**Before any changes** (even though none needed):
```bash
# Create timestamped backup
cp "P2-Smart-Pins-Green-Book-Tutorial-v3.md" \
   "P2-Smart-Pins-Green-Book-Tutorial-v3-backup-$(date +%Y%m%d_%H%M%S).md"
```

### Success Metrics

🎯 **Target**: Complete conversion to div-wrapped format

**Success Criteria**:
- ✅ 0 language-tagged blocks remaining
- ✅ 100% div-wrapped code blocks
- ✅ All antipattern blocks properly split
- ✅ Lua filters handle ONLY div syntax
- ✅ Clean, consistent markdown format

### Summary of Required Changes

1. **Convert 88 code blocks** from language-tagged to div-wrapped
2. **Split mixed antipattern blocks** into separate div blocks
3. **Keep configuration blocks as spin2** (pedagogical decision - not separate)
4. **Update Lua filter** to process Div elements instead of CodeBlock elements
5. **NO language tags remain** - complete migration to div syntax

### Why This Matters

- **Consistency**: Single format for all code blocks
- **Maintainability**: Easier to update and extend
- **Semantic clarity**: Div names clearly indicate content type
- **Future-proof**: Aligns with Pandoc's semantic div approach
