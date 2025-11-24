# Automated Testing with Lua Filters - v2.3 Workflow

## Overview

The PDF Forge daemon v2.3 now supports full Lua filter automation with enhanced path resolution and working directory management.

## Confirmed Working Features ✅

### Lua Filter Support
- **Temporary testing**: `.lua` files used from `/workspace/shared/filters/` for testing only
- **Path resolution**: Filter names automatically resolved to `filters/name.lua` paths
- **Filter copying**: Lua filters copied to temporary `/tmp/` working directory for Pandoc execution
- **Debug support**: Lua filters can output debug comments to .tex files
- **No permanent installation**: Filters are NOT automatically deployed to production

### Validation Workflow
- **Filter validation**: Local filter paths checked before processing
- **Working directory setup**: Filters copied to Pandoc working directory
- **Resource path configuration**: `--resource-path` includes filters directory

## Test Request Format (🔴 UPDATED 2025-08-29)

**✅ CORRECT FORMAT - Use `lua_filters` array:**
```json
{
  "template": "p2kb-smart-pins.latex", 
  "tests": [
    {
      "name": "test-name",
      "document": "test-document.md",
      "lua_filters": ["smart-pins-block-coloring", "part-chapter-pagebreaks"]
    }
  ]
}
```

**❌ INCORRECT FORMAT (documentation was wrong):**
```json
{
  "tests": [
    {
      "pandoc_args": ["--lua-filter=filter-name"]  // This format causes "file not found" errors
    }
  ]
}
```

**Key Points:**
- Use `lua_filters` array property, NOT `pandoc_args`
- Provide filter names only (no path, no .lua extension)
- Daemon builds full path: `/workspace/shared/filters/[name].lua`
- Multiple filters supported in single array
- Verified working: 2025-08-29 with smart-pins-block-coloring filter

## Directory Structure

### Master Workspace (Your Working Area)
```
pdf-forge-workspace/
├── scripts/
│   └── watch-shared-workspace.js    # v2.3 daemon script (MASTER)
├── templates/
│   ├── *.lua                        # Lua filters (temporary testing only)
│   └── *.latex                      # Templates (temporary testing only)
├── test-requests/                   # Test requests directory
├── test-documents/                  # Test documents directory
└── test-results/                    # Results with .tex files

⚠️ IMPORTANT: This workspace is for TESTING ONLY - not production deployment!
```

### Shared Directory (Container Communication)
```
pdf-forge-workspace/                 # Maps to /workspace/shared/ on Forge
├── test-requests/                   # Container watches here
├── test-documents/                  # Container reads documents here
├── test-results/                    # Container writes results here
└── filters/                         # Container filter validation

⚠️ CRITICAL: pdf-forge-workspace/ itself IS the shared workspace!
NEVER create pdf-forge-workspace/shared/ - that creates nested confusion!
```

## Verified Lua Filter Example

The `part-chapter-pagebreaks.lua` filter successfully implements conditional page breaks:

```lua
-- Verified working: Parts get \clearpage before them
-- First chapters after parts flow on same page
-- Subsequent chapters get new pages
local after_part = false

function Header(elem)
  if elem.level == 1 then
    after_part = true
    local pagebreak = pandoc.RawInline('latex', '\\clearpage')
    return {pagebreak, elem}
  elseif elem.level == 2 then
    if after_part then
      after_part = false
      return elem  -- No pagebreak for first chapter after part
    else
      local pagebreak = pandoc.RawInline('latex', '\\clearpage') 
      return {pagebreak, elem}  -- Pagebreak for subsequent chapters
    end
  end
  return elem
end
```

## Debug Capabilities

Lua filters can output debug comments that appear in generated .tex files:

```lua
-- Add debug comments to track filter execution
local debug_comment = pandoc.RawInline('latex', '% LUA FILTER: Processing header level ' .. elem.level .. ' - ' .. pandoc.utils.stringify(elem.content))
```

## Test Results Structure

Successful tests generate:
```json
{
  "status": "✅ PASS",
  "tex_path": "test-name-timestamp.tex",
  "tex_available": true,
  "pdf_path": "output-pdfs/test-name-timestamp.pdf",
  "pdf_size_bytes": 30912
}
```

## Daemon Log Indicators

Successful Lua filter processing shows:
```
🔧 Filter: filter-name → filters/filter-name.lua
📝 Pandoc args: --lua-filter=filters/filter-name.lua
✅ Filter validated: filter-name.lua exists in /workspace/shared/filters/
🔧 Copying N Lua filters: filter1.lua, filter2.lua
📄 .tex file available: test-name-timestamp.tex
```

## Known Issues & Solutions

### Directory Structure Confusion (RESOLVED)
The confusion arose from creating `pdf-forge-workspace/shared/` locally, which maps to `/workspace/shared/shared/` on the Forge.
**Solution**: Remember that `pdf-forge-workspace/` directly maps to `/workspace/shared/` - no nested `shared/` directory needed!

### Filter Path Resolution  
The v2.3 enhancements ensure proper filter path resolution, but verify the daemon is processing from the correct directory structure.

## Usage Workflow

1. **Place Lua filters** in `filters/` directory (daemon also checks `templates/`)
2. **Create test request** with `lua_filters: ["filter-name"]` array  
3. **Create test document** in `test-documents/` directory
4. **Monitor daemon logs** for processing confirmation
5. **Check .tex file** for filter debug output and LaTeX commands
6. **Verify PDF generation** for visual confirmation

**Working Example (2025-08-29):**
```json
{
  "request_id": "lua-filters-array-test",
  "template": "p2kb-smart-pins.latex",
  "tests": [
    {
      "name": "correct-lua-filters-format",
      "document": "smart-pins-minimal-test.md",
      "lua_filters": ["smart-pins-block-coloring"]
    }
  ]
}
// Result: ✅ PASS - PDF generated with colored code blocks

## Version Notes

- **v2.3**: Fixed Lua filter path resolution and working directory setup
- **Tested**: 2025-08-27 with `part-chapter-pagebreaks.lua` filter
- **Result**: ✅ Perfect conditional page break functionality confirmed