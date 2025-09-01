# Lua Filter Loop Issue - Green Book Generation

**Date**: 2025-08-31  
**Issue**: PDF Forge took too long generating .tex file  
**Likely Cause**: `smart-pins-div-blocks.lua` using `pandoc.walk_block` recursion

## Problem Analysis

The original `smart-pins-div-blocks.lua` uses `pandoc.walk_block` to find CodeBlock elements inside Div elements. This can cause issues if:
1. The document has deeply nested div structures
2. The filter accidentally processes its own output
3. There are circular references in the AST

## Solution

Created `smart-pins-div-blocks-safe.lua` which:
- Only looks at immediate children (no recursion)
- Processes each div only once
- Returns early if no code block found
- Simpler, more predictable execution

## Files for Next Outbound Creation

When recreating the outbound directory for P2-Smart-Pins-Green-Book:

### Use SAFE version of filter:
```bash
cp smart-pins-div-blocks-safe.lua smart-pins-div-blocks.lua
```

### Required files:
1. **Markdown**: `P2-Smart-Pins-Green-Book-Tutorial.md` (escaped)
2. **Template**: `p2kb-smart-pins.latex`
3. **Lua Filters** (in order):
   - `smart-pins-div-blocks.lua` (use the SAFE version!)
   - `non-floating-images.lua` 
   - `green-book-semantic-blocks.lua`
   - `part-chapter-pagebreaks.lua` (if not already on forge)
4. **Style Files** (only modified ones):
   - `p2kb-foundation.sty`
   - `p2kb-smart-pins-content.sty`
   - `p2kb-smart-pins-numbering.sty`
   - `p2kb-tech-review.sty`
5. **Assets**: `assets/` directory with images
6. **Request**: `request.json` with documents array

## Request.json Content
```json
{
  "template": "p2kb-smart-pins.latex",
  "documents": [
    {
      "input": "P2-Smart-Pins-Green-Book-Tutorial.md",
      "output": "P2-Smart-Pins-Green-Book-Tutorial.pdf"
    }
  ],
  "lua_filters": [
    "smart-pins-div-blocks",
    "non-floating-images",
    "green-book-semantic-blocks",
    "part-chapter-pagebreaks"
  ],
  "metadata": {
    "title": "P2 Smart Pins Complete Tutorial",
    "subtitle": "Green Book - Visual Learning Guide",
    "version": "Version 2.0 - Enhanced with Images",
    "date": "August 2025",
    "generated": "2025-08-31"
  }
}
```

## Testing Strategy

If forge is still processing:
1. Let it timeout or cancel if possible
2. Use the SAFE version for next attempt
3. Consider removing `green-book-semantic-blocks.lua` temporarily to test
4. Test with smaller document subset first

## Alternative Minimal Filter Set

If issues persist, try with only essential filters:
```json
"lua_filters": [
  "smart-pins-div-blocks",  // SAFE version
  "non-floating-images"
]
```

Then add back one at a time to identify problematic filter.