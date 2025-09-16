# DeSilva Visual Refinement Guide

**Purpose**: Iterate DeSilva manual visual presentation through feedback loops

## Session Start
```bash
mcp__todo-mcp__todo_next tags:["desilva_visual"]
```

## Directory Structure & Purpose
**Understanding the three parallel directories - ALL have the same document structure:**

### Parallel Structure Design
```
manuals/p2-pasm-desilva-style/     # Master documents (reference only)
workspace/p2-pasm-desilva-style/   # Working copies (edit here)
outbound/p2-pasm-desilva-style/    # Deployment staging (LaTeX-escaped)
```

**Each directory serves a different purpose:**

- **`manuals/`**: Opus-created master documents (reference only, NEVER edit)
  - Original documents like `p2-pasm-desilva-style/opus-master/COMBINED-COMPLETE-MASTER.md`
  - Gold masters that serve as source material
  - Same document folder structure as workspace and outbound

- **`workspace/`**: Production working copies (ALL EDITING HAPPENS HERE)
  - Clean versions prepared from masters: `workspace/p2-pasm-desilva-style/P2-PASM-deSilva-Working-Copy.md`
  - Template files, filters, and configuration
  - Maintain as clean, unescaped markdown
  - This is your primary editing environment
  - **Same document folder structure** as manuals and outbound

- **`outbound/`**: Deployment staging for PDF Forge
  - LaTeX-escaped versions only
  - **Same document folder structure** as workspace: `outbound/p2-pasm-desilva-style/`
  - Temporary staging area
  - NEVER edit these directly
  - Files automatically removed when deployed to PDF Forge

## Source of Truth Locations
**Edit these in workspace, never in manuals or outbound:**
- **Markdown**: `workspace/p2-pasm-desilva-style/P2-PASM-deSilva-Working-Copy.md`
- **Main Template**: `workspace/p2-pasm-desilva-style/p2kb-desilva.latex`
- **Lua Filters**: `workspace/p2-pasm-desilva-style/filters/p2kb-desilva-*.lua`
  - `p2kb-desilva-code-coloring.lua` - 5-color code block system
  - `p2kb-desilva-semantic.lua` - DeSilva pedagogical elements
  - `p2kb-desilva-pagination.lua` - Smart page breaks

## Template Architecture
**DeSilva uses layered template system:**
- **Foundation**: `templates/shared/p2kb-foundation.sty` (shared components)
- **Content**: `templates/desilva/p2kb-desilva-content.sty` (5-color system + pedagogical environments)
- **Main**: `workspace/p2-pasm-desilva-style/p2kb-desilva.latex` (loads foundation + content)

## 5-Color Code Block System
**DeSilva pedagogical color coding:**
1. **Spin2** (Green) - `::: spin2`
2. **PASM2** (Yellow/Cream) - `::: pasm2`
3. **CORDIC** (Purple) - `::: cordic`
4. **Multi-COG** (Blue) - `::: multicog`
5. **Antipattern** (Red) - `::: antipattern`

## DeSilva Pedagogical Elements
**Human-centered teaching elements:**
- `::: medicine-cabinet` - Solutions for common problems
- `::: your-turn` - Hands-on exercises
- `::: sidetrack` - Interesting but optional topics
- `::: uff` - We just got through something complex
- `::: well` - Correcting common assumptions
- `::: have-fun` - Encouragement and celebration

## Workflow

### Development Phase (Edit in Workspace)
1. Edit source files in workspace (maintain clean, unescaped state)
2. Test template components locally if possible
3. Update filter chain or template files as needed

### PDF Generation Request Phase

#### Step 1: Prepare Files for Outbound
```bash
# Escape markdown for LaTeX using the proven Smart Pins escaping script
# Note: Output goes to the PARALLEL outbound document directory
./engineering/tools/conversion/latex-escape-all.sh \
  engineering/document-production/workspace/p2-pasm-desilva-style/P2-PASM-deSilva-Working-Copy.md \
  engineering/document-production/outbound/p2-pasm-desilva-style/P2-PASM-deSilva-Working-Copy.md
```

#### Step 2: Copy Required Files to Outbound
**CRITICAL**: Copy files to the parallel outbound document directory:
```bash
# Copy escaped markdown (from Step 1)
# ✅ Already done above

# Copy template files to parallel outbound directory
cp engineering/document-production/workspace/p2-pasm-desilva-style/p2kb-desilva.latex \
   engineering/document-production/outbound/p2-pasm-desilva-style/

cp engineering/document-production/templates/desilva/p2kb-desilva-foundation.sty \
   engineering/document-production/outbound/p2-pasm-desilva-style/

cp engineering/document-production/templates/desilva/p2kb-desilva-content.sty \
   engineering/document-production/outbound/p2-pasm-desilva-style/

# Copy Lua filters (flat structure - no filters/ subdirectory!)
cp engineering/document-production/workspace/p2-pasm-desilva-style/filters/p2kb-desilva-code-coloring.lua \
   engineering/document-production/outbound/p2-pasm-desilva-style/

cp engineering/document-production/workspace/p2-pasm-desilva-style/filters/p2kb-desilva-semantic.lua \
   engineering/document-production/outbound/p2-pasm-desilva-style/

cp engineering/document-production/workspace/p2-pasm-desilva-style/filters/p2kb-desilva-pagination.lua \
   engineering/document-production/outbound/p2-pasm-desilva-style/

# Copy request configuration
cp engineering/document-production/workspace/p2-pasm-desilva-style/request.json \
   engineering/document-production/outbound/p2-pasm-desilva-style/
```

#### Step 3: Verify Outbound Structure
**Your outbound/p2-pasm-desilva-style/ should look exactly like this:**
```
engineering/document-production/outbound/p2-pasm-desilva-style/
├── P2-PASM-deSilva-Working-Copy.md          # LaTeX-escaped markdown
├── p2kb-desilva.latex                       # Main template
├── p2kb-desilva-foundation.sty              # DeSilva foundation
├── p2kb-desilva-content.sty                 # DeSilva content layer
├── p2kb-desilva-code-coloring.lua          # Filter 1 (NO filters/ subdir!)
├── p2kb-desilva-semantic.lua               # Filter 2
├── p2kb-desilva-pagination.lua             # Filter 3
└── request.json                             # PDF generation request
```

**Key Points:**
- **Parallel structure**: outbound mirrors workspace document organization
- **Flat file layout**: All files at same level in document directory
- **No subdirectories**: Lua filters and templates all in root of document folder

#### Step 4: User Deploys to PDF Forge
**User copies everything from outbound/ to PDF Forge system and runs generation**

#### Step 5: Clean Up Outbound
**After successful PDF generation, remove files from outbound to keep it clean**

## Exchange Directory Protocol
**Outbound = Two-way exchange point**
- User places files here for Claude to examine/use
- Claude retrieves them, then removes after copying to workspace
- Claude places deployment files here for user to take to PDF Forge
- Keeps outbound clean and purpose-clear

### ⚠️ Critical Outbound Rules
1. **NO subdirectories** - Lua filters go directly in outbound/, not outbound/filters/
2. **LaTeX-escaped markdown only** - Never put unescaped markdown in outbound
3. **Clean after deployment** - Remove files after successful PDF generation
4. **Exact file structure** - PDF Forge expects specific layout (see Step 3 above)

## Required Reading
- `engineering/pdf-forge/work-modes/production-pdf-generation.md` - Production PDFs
- `engineering/pdf-forge/work-modes/automated-pdf-testing.md` - Interactive testing
- `workspace/p2-pasm-desilva-style/request-requirements.json` - Mandatory args
- `templates/desilva/README.md` - Complete template documentation

## Production Request Format
Always check `request-requirements.json` first. Example:
```json
{
  "format_type": "document_generation",
  "documents": [{
    "input": "P2-PASM-deSilva-Working-Copy.md",
    "output": "P2-PASM-deSilva-Working-Copy.pdf",
    "template": "p2kb-desilva",
    "pandoc_args": ["--top-level-division=part", "--pdf-engine=xelatex", "--toc", "--toc-depth=3"],
    "lua_filters": ["p2kb-desilva-code-coloring", "p2kb-desilva-semantic", "p2kb-desilva-pagination"],
    "metadata": {
      "title": "P2 Assembly Programming in the Style of deSilva",
      "subtitle": "A Human-Centered Approach to Parallel Processing",
      "version": "Version 1.0 - deSilva Style Edition",
      "date": "September 2025"
    }
  }]
}
```

## Critical Rules
- NO file renaming (-fixed, -v2, -working, etc)
- Edit files in place
- Spaces in image filenames ARE allowed (Pandoc handles them)
- Arrays in request.json for ALL fields (even single items)
- Template names without .latex extension in request.json

## DeSilva-Specific Guidelines
- **Human voice**: Maintain deSilva's conversational, encouraging tone
- **Progressive complexity**: Simple concepts first, build gradually
- **Pedagogical flow**: Use "Medicine Cabinet" for troubleshooting, "Your Turn" for practice
- **5-color clarity**: Different code types get different colors for visual learning
- **Accessibility**: All code blocks have thick left borders for distinction

## Filter Chain Order (IMPORTANT)
1. **p2kb-desilva-code-coloring** - Convert div-wrapped code blocks first
2. **p2kb-desilva-semantic** - Convert pedagogical elements second
3. **p2kb-desilva-pagination** - Add smart page breaks last

## Quick Reference
- **Code blocks**: Must use div syntax (`::: type`)
- **Antipatterns**: Split into separate `::: antipattern` and correct approach blocks
- **Conversion script**: `/engineering/tools/convert-to-div-syntax.py`
- **Template test**: Use working copy markdown for validation
- **Filter source**: Adapted from proven Smart Pins workspace filters

## Template Status
✅ **COMPLETE**: DeSilva template stack ready for production
- Foundation layer updated with Smart Pins improvements
- 5-color code system implemented and tested
- Pedagogical environments defined
- Filter chain proven working (adapted from Smart Pins)
- Request format validated against PDF Forge requirements

## Development History
- **Base**: Adapted from Smart Pins proven working template system
- **Enhancement**: Extended 3-color to 5-color pedagogical system
- **Features**: Added DeSilva human-centered teaching elements
- **Validation**: All components copied from production Smart Pins filters