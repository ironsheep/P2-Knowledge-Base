# Multi-Lua Filter Usage Guide

**Purpose**: Document how to use multiple Lua filters in PDF generation for both manual and automated testing

**Created**: 2025-08-28

## Overview

The PDF Forge system supports multiple Lua filters for both manual PDF generation and automated testing. This guide documents the proper syntax and patterns that work in both contexts.

## Request Format Comparison

### Manual PDF Generation (request.json)
```json
{
  "documents": [{
    "input": "document.md",
    "output": "document.pdf",
    "template": "p2kb-smart-pins",
    "variables": {
      "title": "Document Title",
      "author": "Author Name"
    },
    "pandoc_args": [
      "--top-level-division=part",
      "--wrap=preserve",
      "--lua-filter=filters/part-chapter-pagebreaks.lua",
      "--lua-filter=filters/smart-pins-block-coloring.lua"
    ]
  }],
  "options": {
    "cleanup": true,
    "archive": false,
    "optimize": false
  }
}
```

### Automated Testing (test-request.json)
```json
{
  "id": "test-multiple-filters",
  "document": {
    "path": "test-document.md",
    "template": "p2kb-smart-pins"
  },
  "pandoc_args": [
    "--lua-filter=filters/part-chapter-pagebreaks.lua",
    "--lua-filter=filters/smart-pins-block-coloring.lua"
  ]
}
```

## Key Differences

| Aspect | Manual Generation | Automated Testing |
|--------|------------------|-------------------|
| **File location** | `inbox/request.json` | `shared/test-*.json` |
| **Document spec** | `documents` array | Single `document` object |
| **Path prefix** | Relative to `inbox/` | Relative to `shared/` |
| **Variables** | `variables` object | Not typically used |
| **Options** | `options` object | Not used |
| **ID field** | Not required | Required (`id` field) |

## Critical Pattern: Multiple Lua Filters

### The Pattern That Works
Both systems accept multiple Lua filters in the `pandoc_args` array:

```json
"pandoc_args": [
  "--lua-filter=filters/filter1.lua",
  "--lua-filter=filters/filter2.lua",
  "--lua-filter=filters/filter3.lua"
]
```

### Filter Execution Order
Filters are executed in the order specified:
1. First filter processes the document
2. Output from first filter feeds into second filter
3. And so on...

### Common P2KB Filter Stack
For Smart Pins documents, the typical filter stack is:

```json
"pandoc_args": [
  "--top-level-division=part",
  "--wrap=preserve",
  "--lua-filter=filters/part-chapter-pagebreaks.lua",
  "--lua-filter=filters/smart-pins-block-coloring.lua"
]
```

**Purpose of each:**
- `--top-level-division=part` - Makes # headers create Parts instead of Chapters
- `--wrap=preserve` - Preserves line breaks in markdown
- `part-chapter-pagebreaks.lua` - Handles page break logic (Parts on new page, first chapter flows)
- `smart-pins-block-coloring.lua` - Maps code block classes to colored environments

## Filter Implementation Examples

### Page Break Filter (part-chapter-pagebreaks.lua)
Handles document structure:
- Parts always start new pages
- First chapter after a part stays on same page
- Subsequent chapters start new pages

### Color Mapping Filter (smart-pins-block-coloring.lua)
Maps markdown classes to LaTeX environments:
- `{.configuration}` → `ConfigBlock` (blue)
- `{.spin2}` → `Spin2Block` (green)
- `{.pasm2}` → `PASM2Block` (yellow)
- `{.antipattern}` → `AntipatternBlock` (red)

## Testing Workflow

### 1. Create Test Document
Place in `shared/` folder:
```markdown
# Test Document

## Configuration Test
```{.configuration}
WRPIN: Test config
```

## Spin2 Test
```spin2
PUB test()
  return
```
```

### 2. Create Test Request
Place in `shared/` folder:
```json
{
  "id": "test-filters",
  "document": {
    "path": "test-document.md",
    "template": "p2kb-smart-pins"
  },
  "pandoc_args": [
    "--lua-filter=filters/part-chapter-pagebreaks.lua",
    "--lua-filter=filters/smart-pins-block-coloring.lua"
  ]
}
```

### 3. Run Test
The watch script will automatically:
1. Detect the test request
2. Process with specified filters
3. Generate results in `test-results/`
4. Archive the request

## Troubleshooting

### Filters Not Applied
**Check:**
- Filter files exist in `filters/` directory
- Path is correct: `filters/filename.lua`
- No typos in filter names

### Wrong Order
**Remember:** Filters execute sequentially, order matters!

### Template Not Found
**Ensure:**
- Template exists in `templates/` directory
- Template name matches exactly (case-sensitive)
- Include `.latex` extension in manual generation only

## Migration Notes

### For De Silva Manual
The De Silva manual can use the same pattern:
```json
"pandoc_args": [
  "--top-level-division=part",
  "--wrap=preserve",
  "--lua-filter=filters/part-chapter-pagebreaks.lua",
  "--lua-filter=filters/desilva-div-to-environment.lua"
]
```

### Creating New Filters
When creating new Lua filters:
1. Place in `pdf-forge-workspace/filters/`
2. Test with automated system first
3. Deploy to PDF Forge when verified
4. Document the filter's purpose here

## Success Verification

A successful multi-filter test will show:
1. PDF generated with correct formatting
2. `.tex` file shows transformed environments
3. No pandoc errors in logs
4. Visual elements (colors, page breaks) appear correctly

## References
- PDF Forge scripts: `/pdf-forge-scripts/`
- Filter examples: `/pdf-forge-workspace/filters/`
- Template definitions: `/pdf-forge-workspace/templates/`