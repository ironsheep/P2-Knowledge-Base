# Smart Pins Green Book Processing Workflow

**Document**: P2-Smart-Pins-Green-Book-Tutorial
**Last Updated**: 2025-09-01
**Current Version**: V5 (balanced language coverage)

## Complete Processing Pipeline

### Starting Point: Master Document
- **Location**: `/engineering/document-production/manuals/p2-smart-pins-tutorial/opus-master-green-book/`
- **Current Master**: `P2-Smart-Pins-Green-Book-Tutorial-v5.md`
- **Format**: Markdown with language-tagged code blocks (`\`\`\`spin2` and `\`\`\`pasm2`)

### Step 1: Convert to Div Syntax
**Tool**: `/engineering/tools/convert-to-div-syntax.py`
```bash
python3 /engineering/tools/convert-to-div-syntax.py \
  P2-Smart-Pins-Green-Book-Tutorial-v5.md \
  P2-Smart-Pins-Green-Book-Tutorial-v5-converted.md
```

**What it does**:
- Converts `\`\`\`spin2` → `::: spin2`
- Converts `\`\`\`pasm2` → `::: pasm2`
- **CRITICAL**: Adds blank lines where needed (prevents colons in PDF)
- Splits antipattern blocks (WRONG/RIGHT examples)
- Uses 3-colon syntax consistently

**Expected output**:
- ~114 code blocks converted (87 Spin2, 27 PASM2)
- ~30+ blank lines added automatically
- 0 language-tagged blocks remaining

### Step 2: LaTeX Character Escaping
**Tool**: `/tools/latex-escape-all.sh` (or similar)
```bash
./tools/latex-escape-all.sh \
  P2-Smart-Pins-Green-Book-Tutorial-v5-converted.md \
  P2-Smart-Pins-Green-Book-Tutorial-v5-escaped.md
```

**What it escapes**:
- Underscores in code (except in code blocks)
- Special LaTeX characters
- Preserves div syntax and code blocks

### Step 3: Prepare for PDF Forge
**Location**: `/engineering/pdf-forge/production/P2-Smart-Pins-Green-Book/`

1. **Copy escaped markdown**:
   ```bash
   cp P2-Smart-Pins-Green-Book-Tutorial-v5-escaped.md \
      /engineering/pdf-forge/production/P2-Smart-Pins-Green-Book/
   ```

2. **Ensure LaTeX template is present**:
   - Template: `p2kb-smart-pins.latex`
   - Style files: `p2kb-foundation.sty`, `p2kb-smart-pins-content.sty`

3. **Configure request.json**:
   ```json
   {
     "document_name": "P2-Smart-Pins-Green-Book-Tutorial",
     "template": "p2kb-smart-pins.latex",
     "lua_filters": [
       "smart-pins-div-blocks",
       "green-book-semantic-blocks",
       "non-floating-images",
       "part-chapter-pagebreaks"
     ]
   }
   ```

### Step 4: Deploy to PDF Forge
**User Action Required**: Copy to PDF Forge system for generation

## Critical Requirements

### Code Block Formatting Rules
1. **MUST use div syntax** (`::: type`) not language tags
2. **MUST have blank lines** before div openers when preceded by text
3. **MUST use 3 colons** consistently (not 4)

### Why Each Step Matters
- **Div conversion**: Enables Lua filters to apply colored environments
- **Blank lines**: Prevents literal colons appearing in PDF output
- **LaTeX escaping**: Prevents compilation errors from special characters
- **Lua filters**: Apply visual styling (green/yellow/red blocks)

## Visual Output Expectations

### Code Block Colors (via Lua filters)
- **Green**: Spin2 blocks (working code)
- **Yellow**: PASM2 blocks (assembly code)
- **Red**: Antipattern blocks (incorrect examples)

### Semantic Environments
- `needs-diagram` → Gray box with icon
- `tip` → Blue tip box
- `needs-examples` → Orange placeholder
- Others as defined in `green-book-semantic-blocks.lua`

## Version History

### V5 (Current - 2025-09-01)
- 87 Spin2 blocks, 27 PASM2 blocks (3.22:1 ratio)
- Added 15 PASM2 examples from Titus files
- Fixed all spacing issues
- Ready for production

### V4 (2025-09-01)
- Assembled from V3 + Chapter 0 + Index
- 87 Spin2 blocks, 12 PASM2 blocks (7.25:1 ratio)
- Foundation for V5 enhancements

## Troubleshooting

### If colons appear in PDF
- Check blank lines before div openers
- Re-run conversion script
- Verify with: `grep -B1 "^:::" file.md`

### If code blocks aren't colored
- Verify div syntax is used (not language tags)
- Check Lua filter is included in request.json
- Ensure filter name matches exactly

### If LaTeX compilation fails
- Check for unescaped underscores
- Look for special characters outside code blocks
- Verify all div blocks are properly closed

## Quick Commands

### Full pipeline (workspace):
```bash
cd /engineering/document-production/workspace/p2-smart-pins-tutorial/

# 1. Convert to div syntax
python3 /engineering/tools/convert-to-div-syntax.py \
  P2-Smart-Pins-Green-Book-Tutorial-v5.md \
  P2-Smart-Pins-Green-Book-Tutorial-v5-converted.md

# 2. Escape LaTeX characters
./tools/latex-escape-all.sh \
  P2-Smart-Pins-Green-Book-Tutorial-v5-converted.md \
  P2-Smart-Pins-Green-Book-Tutorial-v5-escaped.md

# 3. Copy to production
cp P2-Smart-Pins-Green-Book-Tutorial-v5-escaped.md \
   /engineering/pdf-forge/production/P2-Smart-Pins-Green-Book/

# 4. User deploys to PDF Forge
```

## Notes

- This workflow is specific to the Smart Pins Green Book
- Other documents may have different requirements
- Always work from protected master versions
- Test with small sections first if making changes