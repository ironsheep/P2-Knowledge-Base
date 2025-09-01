# Smart Pins Visual Presentation Refinement Guide

**Single Purpose**: Iterate Smart Pins document visual presentation through human feedback loops

## 🚨 SESSION START INTEGRATION

### Work Mode Identification
**Trigger Phrases**: "Smart Pins visual", "Smart Pins refinement", "Smart Pins PDF work"
**Confirmation**: "This covers PDF visual refinement, list formatting, and iterative testing with PDF Forge"

### Todo MCP Integration  
**CRITICAL - Always use this filter:**
```bash
mcp__todo-mcp__todo_next tags:["smart_pins_visual"]
```

**Why This Matters:**
- ✅ **Filters 50+ tasks down to 5-10 relevant tasks**
- ✅ **Prevents skipping required tasks** (like mini-TOC removal before PDF generation)
- ✅ **Ensures proper task sequence** defined in Todo MCP
- ✅ **No more guessing what to work on** - MCP tells you exactly

### SESSION START CHECKLIST (DO THIS FIRST!)

#### 1. Verify Source of Truth Locations
```bash
# Check markdown source has language markers
grep -c '{.configuration}\|```spin2\|```pasm2' \
  /engineering/document-production/workspace/p2-smart-pins-tutorial/P2-Smart-Pins-Complete-Reference-WORKING.md
# Should show ~119 matches

# Check template has color environments  
grep -c 'ConfigBlock\|Spin2Block\|PASM2Block' \
  /exports/pdf-generation/workspace/manual-templates/p2kb-smart-pins-content.sty
# Should show 5+ matches
```

#### 2. Required Reading
**Always read these documents when starting Smart Pins visual work:**
1. **THIS FILE FIRST** - Smart Pins specific protocols and source of truth
2. `/exports/pdf-generation/REQUEST-JSON-FORMAT-CRITICAL.md` - **CRITICAL**: "Always use arrays" rule
3. `/documentation/pipelines/pdf-generation-format-guide.md` - PDF production workflow
4. `/documentation/pdf-forge-system/layered-template-architecture.md` - Template system

**🔴 CRITICAL**: Before creating any request.json, read REQUEST-JSON-FORMAT-CRITICAL.md!
- **Golden Rule**: Arrays for everything, even single items
- `"documents": []` - NEVER singular, NEVER string  
- `"lua_filters": []` - NEVER pandoc_args, NEVER string



## 🔴 CRITICAL: SOURCE OF TRUTH LOCATIONS

### Markdown Source of Truth
**ALWAYS EDIT HERE**: `/engineering/document-production/workspace/p2-smart-pins-tutorial/P2-Smart-Pins-Complete-Reference-WORKING.md`
- This file has all language markers: `{.configuration}`, ````spin2`, ````pasm2`
- ALL markdown changes happen here FIRST
- Never edit the escaped version in outbound

### Template Source of Truth  
**ALWAYS EDIT HERE**: `/exports/pdf-generation/workspace/manual-templates/`
- `p2kb-foundation.sty` - Foundation layer
- `p2kb-smart-pins-content.sty` - Smart Pins content with color environments
- `p2kb-tech-review.sty` - Tech review presentation
- ALL template changes happen here FIRST

### Deployment Workflow (EXACT SEQUENCE)
1. **Edit markdown**: `workspace/p2-smart-pins-tutorial/P2-Smart-Pins-Complete-Reference-WORKING.md`
2. **Edit templates**: `workspace/manual-templates/*.sty` (IF NEEDED)
3. **Edit scripts**: Fix scripts as needed (generate-pdf.js, watch-shared-workspace.js)
4. **Escape markdown**: ALWAYS run `./tools/latex-escape-all.sh WORKING.md → outbound/p2-smart-pins-tutorial/P2-Smart-Pins-Tutorial.md`
5. **Deploy ONLY MODIFIED FILES to outbound**: 
   - **⚠️ CRITICAL: ONLY COPY WHAT YOU MODIFIED - NEVER COPY EVERYTHING**
   - If you edited templates: `cp [specific-modified.sty] → outbound/p2-smart-pins-tutorial/`
   - If you fixed scripts: `cp [specific-fixed.js] → outbound/P2-Smart-Pins-Reference/scripts-from-forge/`
   - If you modified filters: `cp [specific-filter.lua] → outbound/P2-Smart-Pins-Reference/`
   - **DEFAULT FOR TESTING**: Usually just escaped markdown + request.json
6. **User deploys**: Takes ONLY the files you placed in outbound to PDF Forge

### ⛔️ NEVER Use Outbound as Reference Source ⛔️
**CRITICAL**: Outbound is OUTPUT only, NEVER a reference!
- ❌ `/exports/pdf-generation/outbound/` - Deployment staging ONLY
- ❌ Escaped markdown files - Always edit WORKING.md then re-escape
- ❌ Templates in outbound - Always edit in workspace/manual-templates first

**Information Hierarchy (USE THIS ORDER):**
1. ✅ **Source of Truth FIRST**: `workspace/` directories
2. ✅ **Documentation SECOND**: When source doesn't have info
3. ❌ **NEVER outbound**: It's where we PUT files, not GET information

### Outbound Directory = Deployment Staging
**CRITICAL**: The outbound directory is WHERE YOU DROP FILES FOR USER TO DEPLOY:
- LaTeX templates (.sty files) → User moves to PDF Forge templates/
- Lua filters (.lua files) → User moves to PDF Forge filters/
- Fixed scripts (.js files) → User replaces on PDF Forge scripts/
- Request files (request.json) → User uses for PDF generation

**User handles the right deployment based on file type**



## Visual Refinement Workflow

1. **Human provides feedback** (numbering, page breaks, etc.)
2. **Claude edits** in workspace (markdown/templates)
3. **Escape & deploy**: `latex-escape-all.sh` → outbound
4. **Human tests** on PDF Forge → repeat

## Quick Reference
- **Numbering fix**: `secnumdepth` in template
- **Page breaks**: `\ifafterpart` logic
- **Unnumbered**: `{.unnumbered}` in markdown
- **Images**: `assets/filename.png` (NO SPACES)
- **Smart Pins Visual Lua filters** (in order): `smart-pins-colored-blocks.lua`, `part-chapter-pagebreaks.lua`

## 🚨 CRITICAL RULES

### NO FILE RENAMING - EVER
- **NEVER** create `-fixed`, `-v2`, `-working` versions
- **ALWAYS** edit existing files in place
- **WHY**: Breaks template references, confuses deployment

### Template Layers
- `p2kb-foundation.sty` - Base Pandoc fixes
- `p2kb-smart-pins-content.sty` - Color environments (ConfigBlock, Spin2Block, PASM2Block)
- `p2kb-tech-review.sty` - Visual presentation

## Code Block Markers (Already in Document)
- `{.configuration}` → Blue boxes (config constants)
- ````spin2` → Green boxes (Spin2 code)
- ````pasm2` → Yellow boxes (PASM2 assembly)

---

**This guide covers ONLY Smart Pins visual refinement. Other documents get their own focused guides.**