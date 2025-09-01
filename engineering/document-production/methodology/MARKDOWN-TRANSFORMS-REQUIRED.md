# Markdown Transforms Required for PDF Generation

**Created**: 2025-08-29
**Purpose**: Document all transforms needed before sending markdown to PDF Forge

## 1. LaTeX Character Escaping
**Tool**: `tools/latex-escape-all.sh`
**Status**: ✅ Implemented (needs refinement)
**Transforms**:
- Escape `$`, `%`, `&`, `_`, `^`, `#` characters
- Preserve code blocks and language markers
- Protect markdown image syntax

## 2. Image Path Normalization 
**Status**: ❌ NOT IMPLEMENTED - Manual fix required
**Problem**: Images use complex relative paths from source locations
**Example**:
```markdown
# WRONG - Current state
![Caption](../../../sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/P2 SmartPins-220809_page52_img02.png)

# CORRECT - Should be
![Caption](assets/P2-SmartPins-220809-page52-img02.png)
```

**Required Transform**:
1. Extract just the filename from complex path
2. Replace spaces with hyphens in filename
3. Point to local `assets/` directory
4. URL-encode if needed (spaces → %20)

**Pattern**:
```bash
# Find: ../../../sources/.*/assets/.*/([^/]+\.png)
# Replace: assets/$1
# Then: Replace spaces in filename with hyphens
```

## 3. Code Block Language Preservation
**Status**: ✅ Working
**Requirement**: Preserve `{.configuration}`, `{.antipattern}`, `spin2`, `pasm2` markers

## 4. List Formatting
**Status**: ✅ Working with Pandoc
**Note**: Pandoc handles list conversion automatically

## 5. Table Alignment
**Status**: ⚠️ Needs verification
**Note**: Complex tables may need manual review

## Transform Pipeline Order

```
1. Fix image paths (normalize to assets/)
   ↓
2. Run LaTeX escape script
   ↓
3. Copy to outbound with assets
   ↓
4. Deploy to PDF Forge
```

## Implementation Priority

1. **URGENT**: Image path transform (blocking PDF generation)
2. **HIGH**: LaTeX escape refinements (some characters still unescaped)
3. **MEDIUM**: Table formatting verification
4. **LOW**: Additional safety checks

## Testing Checklist

- [ ] All images resolve to `assets/` directory
- [ ] No spaces in image filenames
- [ ] LaTeX special characters escaped
- [ ] Code block markers preserved
- [ ] Lists render correctly
- [ ] Tables maintain alignment

---

**Note**: Each transform should be idempotent - running it multiple times should not change an already-transformed document.