# Smart Pins PDF Generation Configuration

**Purpose**: Quick reference for generating PDF from Smart Pins markdown
**Last Updated**: 2025-08-28

## request.json Template

```json
{
  "documents": [{
    "input": "P2-Smart-Pins-Complete-Reference.md",
    "output": "P2-Smart-Pins-Complete-Reference.pdf",
    "template": "p2kb-smart-pins",
    "lua_filters": [
      "part-chapter-pagebreaks",
      "smart-pins-block-coloring"
    ],
    "metadata": {
      "title": "P2 Smart Pins Complete Reference",
      "subtitle": "Specifications and Implementation for All 32 Modes",
      "version": "Version 1.0 - Technical Review Draft",
      "date": "August 2025"
    }
  }]
}
```

## Template Stack

### Main Template
- **File**: `p2kb-smart-pins.latex`
- **Purpose**: Document class setup, includes style layers

### Style Layers (in order)
1. **p2kb-foundation.sty** - Base layer (fonts, colors, basic environments)
2. **p2kb-smart-pins-content.sty** - Content styling (code blocks, boxes, AntipatternBlock)
3. **p2kb-tech-review.sty** - Presentation layer (final formatting)

## Lua Filters (ORDER CRITICAL!)

### 1. part-chapter-pagebreaks.lua
- **Purpose**: Controls Part/Chapter page breaks
- **Logic**: Parts start new pages, first chapter after part flows, subsequent chapters new page
- **Must run FIRST** to establish document structure

### 2. smart-pins-block-coloring.lua  
- **Purpose**: Maps code block classes to colored environments
- **Handles**:
  - `{.configuration}` → Blue ConfigBlock
  - `spin2` → Green Spin2Block
  - `pasm2` → Yellow PASM2Block (uses Verbatim, not lstlisting)
  - `{.antipattern}` → Red AntipatternBlock
  - Default → Gray standard code block
- **Must run SECOND** after pagination established

## Required Pandoc Arguments
```
--top-level-division=part    # Parts are highest level (not chapters)
--wrap=preserve              # Preserve line wrapping from markdown
```

## Pre-Generation Checklist

- [ ] Markdown escaped with `tools/latex-escape-all.sh`
- [ ] All templates present in pdf-forge-workspace/templates/
- [ ] Both Lua filters present in pdf-forge-workspace/filters/
- [ ] Mini TOCs removed from markdown
- [ ] Code blocks properly tagged (configuration/spin2/pasm2/antipattern)

## Common Issues & Solutions

### White background on yellow PASM2 blocks
**Cause**: Using lstlisting with backgroundcolor  
**Fix**: Use Verbatim like other blocks (fixed in current filter)

### Too many page breaks
**Cause**: Wrong filter or Header function too aggressive  
**Fix**: Use only part-chapter-pagebreaks.lua for pagination

### Missing AntipatternBlock environment
**Cause**: p2kb-smart-pins-content.sty not loaded  
**Fix**: Ensure all three .sty files are present

## Files Location

### Working Files
- **Markdown**: `exports/pdf-generation/workspace/smart-pins-manual/P2-Smart-Pins-Complete-Reference-WORKING.md`
- **Opus Master**: `exports/pdf-generation/workspace/smart-pins-manual/opus-master/COMPLETE-OPUS-MASTER.md`

### Deployment
- **Outbound**: `exports/pdf-generation/outbound/P2-Smart-Pins-Reference/`
- **Copy escaped markdown and request.json here for PDF Forge**

## Related Documentation
- **Creation Guide**: `documentation/manuals/smart-pins-workshop/creation-guide.md`
- **Markdown Changes**: `exports/pdf-generation/workspace/smart-pins-manual/markdown-changes-guide.md`