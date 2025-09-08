# Smart Pins Visual Refinement Guide

**Purpose**: Iterate Smart Pins visual presentation through feedback loops

## Session Start
```bash
mcp__todo-mcp__todo_next tags:["smart_pins_visual"]
```

## Directory Structure & Purpose
**Understanding the three key directories:**
- **`manuals/`**: Opus-created master documents (reference only, NEVER edit)
  - Original documents with references like `v6-assets/`
  - Gold masters that serve as source material
- **`workspace/`**: Production working copies (ALL EDITING HAPPENS HERE)
  - Clean versions prepared from masters
  - Already has processed paths (e.g., `assets/` not `v6-assets/`)
  - Maintain as clean, unescaped markdown
  - This is your primary editing environment
- **`outbound/`**: Deployment staging for PDF Forge
  - LaTeX-escaped versions only
  - Temporary staging area
  - NEVER edit these directly

## Source of Truth Locations
**Edit these in workspace, never in manuals or outbound:**
- **Markdown**: `workspace/p2-smart-pins-tutorial/P2-Smart-Pins-Green-Book-Tutorial.md`
- **Templates**: `workspace/p2-smart-pins-tutorial/p2kb-*.sty`
  - **TODO**: Templates scattered across multiple locations - needs consolidation
  - Currently: workspace, pdf-forge/interactive-testing/templates, etc.
- **Lua Filters**: `workspace/p2-smart-pins-tutorial/filters/*.lua`

## Workflow
1. Edit source files in workspace (maintain clean, unescaped state)
2. Run: `/engineering/tools/conversion/latex-escape-all.sh workspace/input.md outbound/output.md`
3. Copy ONLY modified files to outbound:
   - Style files (.sty) - copy directly
   - Lua filters (.lua) - copy directly to outbound (no filters/ subdirectory)
   - Templates (.latex) - only if changed
   - request.json - only if updated
4. User deploys from outbound to PDF Forge

## Exchange Directory Protocol
**Outbound = Two-way exchange point**
- User places files here for Claude to examine/use
- Claude retrieves them, then removes after copying to workspace
- Claude places deployment files here for user to take to PDF Forge
- Keeps outbound clean and purpose-clear

## Required Reading
- `engineering/pdf-forge/work-modes/production-pdf-generation.md` - Production PDFs
- `engineering/pdf-forge/work-modes/automated-pdf-testing.md` - Interactive testing
- `workspace/p2-smart-pins-tutorial/request-requirements.json` - Mandatory args

## Production Request
Always check `request-requirements.json` first. Example:
```json
{
  "format_type": "document_generation",
  "documents": [{
    "input": "P2-Smart-Pins-Green-Book-Tutorial.md",
    "output": "P2-Smart-Pins-Green-Book-Tutorial.pdf",
    "template": "p2kb-smart-pins",
    "pandoc_args": ["--top-level-division=part"],
    "lua_filters": ["non-floating-images", "smart-pins-colored-blocks"]
  }]
}
```

## Critical Rules
- NO file renaming (-fixed, -v2, -working, etc)
- Edit files in place
- Spaces in image filenames ARE allowed (Pandoc handles them)
- Arrays in request.json for ALL fields (even single items)

## Quick Reference
- **Code blocks**: Must use div syntax (`::: type`)
- **Antipatterns**: Split into separate `::: antipattern` and `::: spin2` blocks
- **Conversion script**: `/engineering/tools/convert-to-div-syntax.py`