# Smart Pins Tutorial - Lua Filter & Stylesheet Decisions
**Date**: 2025-09-04 (Updated: 2025-09-04 Evening)  
**Document**: P2 Smart Pins Green Book Tutorial

## 🎯 CRITICAL INSIGHT: Division of Responsibility (2025-09-04 Evening)

### The Processing Pipeline
1. **Markdown** → Pandoc reads it
2. **Lua filters** → Process document structure (in request.json order)
3. **Pandoc conversion** → Converts to LaTeX based on Lua filter output
4. **LaTeX template** → Wraps the converted content
5. **LaTeX styles** → Applied when LaTeX compiles (`p2kb-foundation.sty`)
6. **PDF** → Final output

### Key Understanding: Lua Filters Run FIRST
- Lua filters CANNOT override what styles will do
- Lua filters CAN change structure (header levels)
- Lua filters CAN inject raw LaTeX
- But styles have final say on how commands behave

### The p2kb-foundation.sty Page Break Behavior
With `--top-level-division=part`:
- Level 1 (`#`) → `\part{}` → style adds `\clearpage`
- Level 2 (`##`) → `\chapter{}` → style adds `\clearpage`
- Level 3 (`###`) → `\section{}` → style adds `\clearpage` UNLESS after chapter
- Level 4 (`####`) → `\subsection{}` → no automatic page break

### Our Strategy: Work WITH the Style Sheet
**Philosophy**: Lua filters arrange the structure, style sheet handles presentation

**Division of Labor**:
1. **Lua Filters**: Control WHAT becomes a chapter/section/subsection
2. **Style Sheet**: Controls HOW chapters/sections behave (page breaks, formatting)
3. **No Fighting**: Never try to override style behavior with Lua

### Practical Implementation
**In frontmatter (before Part I)**:
- Headers that SHOULD page break → Keep as `\chapter` (level 2)
- Headers that SHOULDN'T → Demote to `\section` or lower
- Add LaTeX formatting to preserve visual weight when demoting

Example:
```lua
-- Copyright shouldn't page break but should look like a chapter
header.level = 3  -- Becomes \section (no auto page break)
return {
  pandoc.RawBlock('latex', '{\\Large\\bfseries}'),  -- Look like chapter
  header,
  pandoc.RawBlock('latex', '}')
}
```

## 🎯 NEW NAMING CONVENTION (2025-09-04)

### Pattern: `p2kb-[document]-[function].[ext]`
- **p2kb** = P2 Knowledge Base (project prefix)
- **sp** = Smart Pins (document identifier)
- **function** = descriptive name of what it does

### Benefits:
- No collisions between documents on PDF Forge
- Clear purpose from filename
- Consistent across all asset types
- Easy to identify which document uses which assets

## 🔄 SEPARATION OF CONCERNS (2025-09-04)

**Previous Problem**: One filter doing too much (coloring + pagination)
**Solution**: Separate into single-purpose filters

### New Filter Architecture:

#### 1. `p2kb-sp-code-coloring.lua` (NEW)
**Purpose**: ONLY handles code block coloring
**Replaces**: Code coloring portion of smart-pins-div-blocks.lua
**Features**:
- Spin2 blocks (green) - `::: spin2` div syntax
- PASM2 blocks (yellow) - `::: pasm2` div syntax
- Antipattern blocks (red) - `::: antipattern` div syntax
- NO pagination logic

#### 2. `p2kb-sp-pagination.lua` (NEW)
**Purpose**: ONLY handles page breaks between sections
**Replaces**: Pagination portion of smart-pins-div-blocks.lua
**Features**:
- Page breaks after Parts
- Page breaks after Chapters
- Page breaks after Appendices
- Handles Index and Quick Reference sections
- Uses correct `RawBlock` for `\clearpage`

#### 3. `p2kb-sp-semantic.lua` 
**Purpose**: Convert semantic divs to LaTeX environments
**Formerly**: green-book-semantic-blocks.lua
**Handles 7 markers**: needs-diagram, tip, etc.

#### 4. `p2kb-sp-images.lua` (CURRENTLY DISABLED)
**Purpose**: Prevent image floating
**Formerly**: non-floating-images.lua
**Status**: Needs fix for spaces in filenames

## Legacy Filters (Being Replaced)

### ~~1. ❌ `smart-pins-div-blocks.lua`~~ → SPLIT INTO TWO
**Being replaced by**: 
- `p2kb-sp-code-coloring.lua` (coloring only)
- `p2kb-sp-pagination.lua` (pagination only)
**Reason**: Violated single responsibility principle

### OLD: Filters to Use (Pre-Separation)

### 1. ✅ `smart-pins-div-blocks.lua`
**Purpose**: Handles div-based colored code blocks AND page breaks  
**Features**:
- Spin2 blocks (green) - `::: spin2` div syntax
- PASM2 blocks (yellow) - `::: pasm2` div syntax  
- Antipattern blocks (red) - `::: antipattern` div syntax
- Decision tree flowchart boxes (start-box, decision-*, option groups)
- **Page breaks between Parts/Chapters/Appendices** (built-in)

**Why chosen**: 
- Document uses div syntax (`::: spin2`) not backtick syntax
- Handles both code coloring AND page breaks correctly
- Uses correct `RawBlock` for `\clearpage` commands
- Handles Appendix and Index sections (not just Chapters)
- Production-tested with div syntax

### 2. ✅ `green-book-semantic-blocks.lua`
**Purpose**: Convert semantic divs to LaTeX tcolorbox environments  
**Handles 7 semantic markers**:
- `needs-diagram` → `gbneedsdiagram`
- `preliminary-content` → `gbpreliminarycontent`
- `needs-verification` → `gbneedsverification`
- `needs-examples` → `gbneedsexamples`
- `needs-technical-review` → `gbneedstechreview`
- `needs-code-review` → `gbneedscodereview`
- `tip` → `gbtipbox`

**Why chosen**: Provides visual feedback for document completeness tracking

## Filters to OMIT

### 1. ❌ `part-chapter-pagebreaks.lua`
**Reason for omission**: 
- Duplicates functionality already in `smart-pins-div-blocks.lua`
- Uses incorrect `RawInline` instead of `RawBlock` for `\clearpage`
- Having two filters handle the same headers could cause conflicts
- Less comprehensive than the page break logic in smart-pins-div-blocks

### 2. ❌ `non-floating-images.lua` (TEMPORARILY)
**Reason for temporary omission**:
- Currently breaks PDF generation with spaces in filenames
- Error: "File ended while scanning use of \Gin@ii"
- Production system handles images correctly without this filter
- Will re-enable once spaces-in-filenames issue is resolved

**When re-enabled**: This filter prevents LaTeX from moving images away from their narrative context, keeping them exactly where placed in the document flow.

## Other Filters Considered

### `div-to-env.lua` / `desilva-div-to-environment.lua`
**Status**: Not needed  
**Reason**: Handles De Silva pedagogical elements (sidetrack, interlude, yourturn) which aren't used in Smart Pins Tutorial. The Smart Pins tutorial uses different semantic markers handled by `green-book-semantic-blocks.lua`.

## Filters Still on PDF Forge (2025-09-04)

### Available on Forge (May be useful):
- `smart-pins-auto-indent.lua` - Auto-indentation for code blocks
- `smart-pins-block-coloring.lua` - Earlier version of colored blocks
- `smart-pins-code-styling.lua` - Code formatting styles
- `smart-pins-colored-blocks.lua` - Previous main coloring filter (superseded by p2kb-sp-code-coloring)
- `smart-pins-index-formatting.lua` - Index-specific formatting
- `smart-pins-pagebreaks.lua` - Previous pagination (superseded by p2kb-sp-pagination)
- `smart-pins-pasm-formatting.lua` - PASM-specific formatting (11KB - comprehensive!)
- `smart-pins-vertical-spacing.lua` - Vertical space adjustments

### Potentially Useful Filters (NOW IN WORKSPACE):

#### 1. **`smart-pins-pasm-formatting.lua`** (11KB)
**Purpose**: Makes PASM instructions uppercase and bold
**Features**:
- Comprehensive P2 instruction list (200+ instructions)
- Handles labels, conditionals, instructions
- Proper P2 syntax understanding (no trailing colons on labels)
- Could fix PASM formatting issues
**Consider renaming to**: `p2kb-sp-pasm-formatter.lua`

#### 2. **`smart-pins-auto-indent.lua`** 
**Purpose**: Varies code block indentation by header level
**Features**:
- Level 1 headers: Shaded environment
- Level 2 headers: CodeLevel2 environment  
- Level 3+ headers: CodeLevel3 environment
**Note**: Might conflict with our coloring system

#### 3. **`smart-pins-index-formatting.lua`**
**Purpose**: Index-specific formatting
**Status**: Need to examine

#### 4. **`smart-pins-code-styling.lua`**
**Purpose**: General code styling
**Status**: Need to examine

### Legacy/Superseded Filters
- `smart-pins-block-coloring.lua` - Superseded by `smart-pins-colored-blocks.lua`
- `smart-pins-config-blue-v2.lua` - Early iteration, functionality now in main filter
- `smart-pins-four-color-final.lua` - Testing version, production version is `smart-pins-colored-blocks.lua`
- `smart-pins-pagebreaks.lua` - Earlier version, functionality now integrated
- `smart-pins-pasm-formatting.lua` - PASM formatting now handled in main filter
- `smart-pins-vertical-spacing.lua` - Not needed with current template

## Current Filter Responsibilities (After Style Sheet Coordination)

### 1. p2kb-sp-fix-hypertarget.lua (Runs FIRST)
**Purpose**: Remove identifiers from Part headers only
**Why**: Prevents `[Part I:]Part I:` duplication issue
**Note**: May not be needed if Part parameter issue is fixed

### 2. p2kb-sp-fix-title-as-part.lua (Runs SECOND)
**Purpose**: Prevent document title from becoming `\part{}`
**Action**: Demotes first level 1 header to level 3 with formatting
**Why**: Title shouldn't be a Part division

### 3. p2kb-sp-frontmatter.lua (Runs THIRD)
**Purpose**: Handle everything until Part I
**Actions**:
- Demote Copyright/Version History to level 3 + formatting
- Keep Preface as level 2 (gets page break from style)
- Demote Preface subsections to level 4 + formatting
- Suppress metadata headers and horizontal rules
- Insert `\mainmatter` at Part I
**Philosophy**: Structure manipulation only, NO `\clearpage` commands

### 4. p2kb-sp-structure.lua (Runs FOURTH)
**Purpose**: Track document flow after Part I
**Actions**:
- Track when we just saw a Part
- Let style handle all page breaks
**Philosophy**: Minimal intervention, work with style sheet

## Production Configuration

### ✅ CURRENT FILTERS FOR PAGE BREAK FIXES (2025-09-04 - Updated)
**request.json filters array**:
```json
"lua_filters": [
  "p2kb-sp-frontmatter",
  "p2kb-sp-structure",
  "p2kb-sp-fix-hypertarget"
]
```

### What Each Filter Does:
1. **p2kb-sp-frontmatter** - Comprehensive page break and metadata handling:
   - Suppresses metadata headers (Version, Created date) that cause square brackets
   - Adds page breaks for Parts, Preface, Executive Summary, Quick Start
   - Manages Roman to Arabic numeral transition
   - Handles \frontmatter and \mainmatter commands

2. **p2kb-sp-structure** - Document structure processing

3. **p2kb-sp-fix-hypertarget** - Fixes hyperlink targets (already on PDF Forge)

### Migration Status
- ✅ `p2kb-sp-pagination.lua` - Created from Header function of smart-pins-div-blocks
- ✅ `p2kb-sp-code-coloring.lua` - Created from Div function of smart-pins-div-blocks
- ✅ `p2kb-sp-semantic.lua` - Renamed from green-book-semantic-blocks.lua
- ⏸️ `p2kb-sp-images.lua` - Renamed from non-floating-images.lua (disabled until spaces fix)

### OLD CONFIGURATION (Pre-separation)
**Deprecated - Do not use**:
```json
"lua_filters": [
  "smart-pins-div-blocks",
  "green-book-semantic-blocks"
]
```

**Note**: When `non-floating-images` is fixed, add it as the third filter.

## Page Break Filter Analysis

### Should we switch to `part-chapter-pagebreaks.lua`?
**Decision: NO - Keep using `smart-pins-div-blocks.lua`**

**Reasons to stay with smart-pins-div-blocks:**
1. **One filter does both jobs** - Handles code coloring AND page breaks
2. **Correct implementation** - Uses `RawBlock` (correct) not `RawInline` (incorrect)
3. **Broader coverage** - Handles Appendix, Index, Quick Reference (not just Chapters)
4. **Already working** - Tested and functioning in production

**Problems with part-chapter-pagebreaks:**
1. Uses `RawInline` for block-level commands (technically wrong)
2. Only handles "Chapter" headers, not "Appendix" or other sections
3. Would require loading two filters instead of one
4. Has excessive debug output that clutters the LaTeX

## Technical Notes

1. **Filter order matters**: Colored blocks should run before semantic blocks
2. **All filters use `gb` prefix** to avoid pandoc namespace conflicts  
3. **Page breaks are handled** by smart-pins-colored-blocks (no separate filter needed)
4. **Images work in production** without our custom filter (pandoc handles them)

## Naming Convention (Established 2025-09-04)

Document-specific files use abbreviated prefixes:
- `p2kb-sp-*` : Smart Pins Tutorial files (filters, templates, styles)
- `p2kb-pasm-*` : PASM Manual files  
- `p2kb-spin-*` : Spin2 Manual files (future)

Shared/foundation files use descriptive names:
- `p2kb-foundation.sty` : Base styles (shared across all documents)
- `p2kb-tech-review.sty` : Review formatting (shared)
- `p2kb-tutorial-content.sty` : Tutorial helpers (shared)
- `p2kb-reference-content.sty` : Reference styles (shared)

This keeps file names short while preventing collisions on PDF Forge.

## Files Needing Updates from PDF Forge (2025-09-04)

**Newer versions on Forge that need copying:**
- `p2kb-foundation.sty` (Sep 4 00:10 version)
- `p2kb-tech-review.sty` (Sep 4 00:11 version)

**File to rename on Forge:**
- `p2kb-smart-pins-numbering.sty` → `p2kb-sp-numbering.sty` (for consistency)