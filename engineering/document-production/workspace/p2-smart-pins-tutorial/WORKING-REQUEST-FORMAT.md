# Working Request.json Format for Smart Pins Tutorial

**Last Successful Build**: 2025-01-10
**Document**: P2-Smart-Pins-Green-Book-Tutorial.md (v7)

## ✅ CONFIRMED WORKING REQUEST.JSON

```json
{
  "format_type": "document_generation",
  "documents": [{
    "input": "P2-Smart-Pins-Green-Book-Tutorial.md",
    "output": "P2-Smart-Pins-Green-Book-Tutorial.pdf",
    "template": "p2kb-sp-template",
    "pandoc_args": [
      "--top-level-division=part",
      "--pdf-engine=xelatex",
      "--toc",
      "--toc-depth=3"
    ],
    "lua_filters": [
      "p2kb-sp-fix-hypertarget",
      "p2kb-sp-fix-title-as-part",
      "p2kb-sp-frontmatter",
      "p2kb-sp-structure",
      "p2kb-sp-index-toc",
      "p2kb-sp-code-coloring",
      "p2kb-sp-semantic"
    ],
    "metadata": {
      "title": "P2 Smart Pins \\& I/O Complete Tutorial",
      "subtitle": "Master Every Aspect of P2 Input/Output Through Progressive Learning",
      "version": "Version 7.0 - Green Book Edition"
    }
  }]
}
```

## Critical Elements That Made It Work

### 1. Pandoc Arguments (ALL REQUIRED)
- `--top-level-division=part` - Essential for Part/Chapter structure
- `--pdf-engine=xelatex` - Required for font/special character handling
- `--toc` - Generate table of contents
- `--toc-depth=3` - Include up to subsections in TOC

### 2. Lua Filter Pipeline (ORDER MATTERS!)
1. **p2kb-sp-fix-hypertarget** - Must run first to fix hyperlink targets
2. **p2kb-sp-fix-title-as-part** - Prevents title becoming \part{}
3. **p2kb-sp-frontmatter** - Handles copyright, version history, preface
4. **p2kb-sp-structure** - Document structure after Part I
5. **p2kb-sp-index-toc** - Index and TOC formatting
6. **p2kb-sp-code-coloring** - Colors div-syntax blocks (NOT smart-pins-div-blocks!)
7. **p2kb-sp-semantic** - Handles semantic divs (needs-diagram, tip, etc.)

### 3. Metadata Section
- **Double backslash for ampersand**: `\\&` not just `\&`
- **Version string**: Update to match current version

## Document Preparation Requirements

### 1. Markdown Must Use Div Syntax
All code blocks MUST use:
```markdown
::: spin2
```
code here
```
:::
```

NOT the old backtick syntax:
```markdown
```spin2
code here
```
```

### 2. Run Conversion Script
```bash
python3 /engineering/tools/convert-to-div-syntax.py input.md output.md
```

### 3. Post-Conversion Cleanup
- Remove extra blank lines in antipattern blocks
- Ensure blank lines before opening div blocks

### 4. LaTeX Escape
```bash
/engineering/tools/conversion/latex-escape-all.sh \
  workspace/p2-smart-pins-tutorial/P2-Smart-Pins-Green-Book-Tutorial.md \
  outbound/p2-smart-pins-tutorial/P2-Smart-Pins-Green-Book-Tutorial.md
```

## Deployment Checklist

### Files to Deploy to `/outbound/p2-smart-pins-tutorial/`:
1. ✅ `P2-Smart-Pins-Green-Book-Tutorial.md` (LaTeX-escaped)
2. ✅ `request.json` (using format above)

### Files NOT to Deploy (already on PDF Forge):
- ❌ Style files (.sty) - Unless modified
- ❌ Lua filters (.lua) - Unless modified
- ❌ LaTeX template (.latex) - Unless modified

## Common Mistakes to Avoid

1. **Wrong filter name**: Use `p2kb-sp-code-coloring` NOT `smart-pins-div-blocks`
2. **Missing pandoc args**: All four args are required
3. **Wrong escape sequence**: Use `\\&` in metadata, not `\&`
4. **Including unchanged files**: Only deploy what you modified

## Source of Truth
- **Working copy**: `/workspace/p2-smart-pins-tutorial/request.json`
- **This guide**: `/workspace/p2-smart-pins-tutorial/WORKING-REQUEST-FORMAT.md`
- Always copy from workspace request.json, not from memory!