# P2 Debug Window Visual Refinement Guide

**Purpose**: Iterate P2 Debug Window Manual visual presentation through feedback loops

## Session Start
```bash
mcp__todo-mcp__todo_next tags:["p2_debug_visual"]
```

## Directory Structure & Purpose
**Understanding the three key directories:**
- **`manuals/p2-debug-window-manual/opus-master/`**: Opus-created master documents (reference only, NEVER edit)
  - Original documents with comprehensive debug content
  - Gold master serving as source material
  - Contains validated code examples and complete documentation
- **`workspace/p2-debug-window-manual/`**: Production working copies (ALL EDITING HAPPENS HERE)
  - Clean versions prepared from masters
  - Maintain as clean, unescaped markdown
  - This is your primary editing environment
  - Copy from opus-master when starting fresh
- **`pdf-forge/production/p2-debug-window-manual/`**: Deployment staging for PDF Forge
  - LaTeX-escaped versions only
  - Temporary staging area
  - NEVER edit these directly

## Source of Truth Locations
**Edit these in workspace, never in opus-master or pdf-forge:**
- **Main Document**: `workspace/p2-debug-window-manual/P2-Debug-Window-Manual.md`
- **Templates**: `workspace/p2-debug-window-manual/p2kb-debug-window.latex`
  - De Silva style template adapted for debug window content
  - Contains specific environments for debug window types
- **Style Files**: `workspace/p2-debug-window-manual/p2kb-*.sty`
  - `p2kb-foundation.sty` - Base styles
  - `p2kb-debug-window.sty` - Debug-specific styles (if created)
- **Lua Filters**: `workspace/p2-debug-window-manual/filters/*.lua`
  - Debug-specific filters for window types
  - Terminal, bitmap, plot, scope formatting

## Workflow
1. Copy from opus-master to workspace if starting fresh:
   ```bash
   cp opus-master/COMPLETE-OPUS-MASTER.md workspace/p2-debug-window-manual/P2-Debug-Window-Manual.md
   ```
2. Edit source files in workspace (maintain clean, unescaped state)
3. Run LaTeX escape: 
   ```bash
   /engineering/tools/conversion/latex-escape-all.sh \
     workspace/p2-debug-window-manual/P2-Debug-Window-Manual.md \
     pdf-forge/production/p2-debug-window-manual/P2-Debug-Window-Manual.md
   ```
4. Copy ONLY modified files to pdf-forge/production:
   - Style files (.sty) - copy directly
   - Lua filters (.lua) - copy directly (no filters/ subdirectory)
   - Templates (.latex) - only if changed
   - request.json - only if updated
5. User deploys from pdf-forge to PDF Forge system

## Exchange Directory Protocol
**pdf-forge/production = Two-way exchange point**
- User places files here for Claude to examine/use
- Claude retrieves them, then removes after copying to workspace
- Claude places deployment files here for user to take to PDF Forge
- Keeps production directory clean and purpose-clear

## Required Reading
- `engineering/pdf-forge/work-modes/production-pdf-generation.md` - Production PDFs
- `engineering/pdf-forge/work-modes/automated-pdf-testing.md` - Interactive testing
- `opus-master/COMPLETE-OPUS-MASTER.md` - Master reference document
- `opus-master/screenshot-checklist.md` - 56 required screenshots

## Production Request Template
Create `request.json` in pdf-forge/production/p2-debug-window-manual/:
```json
{
  "format_type": "document_generation",
  "documents": [{
    "input": "P2-Debug-Window-Manual.md",
    "output": "P2-Debug-Window-Manual.pdf",
    "template": "p2kb-debug-window",
    "pandoc_args": [
      "--top-level-division=part",
      "--toc",
      "--toc-depth=3"
    ],
    "lua_filters": [
      "non-floating-images",
      "debug-window-blocks"
    ]
  }]
}
```

## Debug Window Specific Considerations
- **Window Types**: 9 distinct types (TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, MIDI)
- **Code Examples**: 75 validated examples must compile with pnut_ts
- **Screenshots**: 56 placeholders need actual screenshots
- **Hover Coordinates**: Unique feature requiring special formatting
- **Multi-Window**: Complex layouts need careful visual design

## Visual Elements Requiring Attention
1. **Terminal Window Formatting**
   - Monospace font for output
   - Color coding for different message types
   - Cursor position indicators

2. **Bitmap/Graphics Windows**
   - Coordinate system diagrams
   - Color palette references
   - Sprite/layer composition visuals

3. **Instrument Windows**
   - Scope/Logic analyzer displays
   - FFT/Spectrogram representations
   - Measurement annotations

4. **Code Blocks**
   - Spin2 syntax highlighting
   - PASM2 instruction formatting
   - Debug command highlighting

## Critical Rules
- NO file renaming (-fixed, -v2, -working, etc)
- Edit files in place in workspace
- Maintain clean markdown (no LaTeX escapes) in workspace
- Arrays in request.json for ALL fields (even single items)
- Validate all code examples before PDF generation
- Follow De Silva visual style guidelines

## Quick Reference Commands
- **Validate code**: `pnut_ts example.spin2`
- **Extract examples**: `python3 opus-master/code-validation/extract_and_validate.py`
- **LaTeX escape**: `/engineering/tools/conversion/latex-escape-all.sh input.md output.md`
- **Convert code blocks**: `/engineering/tools/convert-to-div-syntax.py input.md output.md`

## Todo MCP Tags
- `p2_debug_visual` - Visual refinement tasks
- `p2_debug_screenshots` - Screenshot capture/integration
- `p2_debug_validation` - Code validation tasks
- `p2_debug_production` - PDF production tasks

## Next Steps Checklist
- [ ] Set up workspace directory with clean copy from opus-master
- [ ] Create/adapt p2kb-debug-window.latex template
- [ ] Create/adapt p2kb-debug-window.sty styles
- [ ] Create debug-window-blocks.lua filter
- [ ] Generate first test PDF
- [ ] Iterate based on visual feedback
- [ ] Add actual screenshots (56 required)
- [ ] Final production PDF generation