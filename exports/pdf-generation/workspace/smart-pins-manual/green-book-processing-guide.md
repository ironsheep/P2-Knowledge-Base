# Green Book Post-Processing Guide

**Purpose**: Document verification and processing steps for the Green Book Tutorial before PDF generation  
**Document**: P2-Smart-Pins-Green-Book-Tutorial.md  
**Generated**: 2025-08-30 by Opus 4.1  
**Last Updated**: 2025-08-30

## Overview
The Green Book Tutorial was generated with many conventions already in place, so this guide is simpler than the original Blue Book processing guide. Focus is on verification and minor adjustments rather than major transformations.

## Pre-Processing Checklist

### 1. Verify Semantic Div Types (Already Present)
**Count**: 7 types of gap markers already embedded
**Verification**:
```bash
grep -c '^::: needs-' P2-Smart-Pins-Green-Book-Tutorial.md
# Should show multiple instances across document
```

**Types Present**:
- `::: needs-diagram` → Visual diagrams needed
- `::: needs-code-review` → Code samples need review  
- `::: needs-technical-review` → Technical accuracy verification
- `::: preliminary-content` → Content is draft/beta
- `::: needs-examples` → More examples needed
- `::: needs-verification` → Hardware verification needed
- `::: tip` → Helpful tips and notes

### 2. Add Code Block Language Tags
**Required**: ~200+ code blocks need language markers
**Why**: Triggers our 4-color system in PDF output

**Pattern Recognition**:
- After "**Configuration**" headers → Add `{.configuration}`
- Spin2 code examples → Add ````spin2`
- PASM2 code examples → Add ````pasm2`
- Mixed/general code → Leave unmarked (gray default)

**Semi-Automated Application**:
```bash
# For configuration blocks after Configuration headers:
awk '/^\*\*Configuration\*\*$/ {print; getline; if ($0 == "```") print "```{.configuration}"; else print; next} {print}' input.md > output.md
```

**Manual Review Required**: 
- Each mode section typically has 3 code blocks (config, spin2, pasm2)
- Exercise code blocks should use appropriate language
- Verify context to choose correct language tag

**Verification**:
```bash
grep -E '```(spin2|pasm2|{.configuration})' Green-Book.md | wc -l
# Should be close to 200+
```

### 3. Verify Image Paths
**Pattern**: All images should reference `assets/` directory
**Check**:
```bash
grep -o '!\[.*\](.*\.png)' Green-Book.md | grep -v '^!\[.*\](assets/'
# Should return nothing (all paths start with assets/)
```

**Document Missing Images**:
Create `missing-images.md` listing any referenced but non-existent images for later resolution.

### 4. Check Hex Notation Convention
**Standard**: P2 uses `$` prefix for hex values
**Verify**: 
```bash
grep -o '0x[0-9A-Fa-f]\+' Green-Book.md
# If found, convert to $ notation
```

**Convert if needed**:
```bash
sed -i.bak 's/0x\([0-9A-Fa-f]\+\)/$\1/g' Green-Book.md
```

### 5. Tutorial-Specific Elements
**Verify Present**:
- Exercise blocks (should have clear markers)
- Key Takeaways sections
- Common Mistakes warnings
- Progressive difficulty indicators

**No changes needed** - these are already properly structured for Lua filter processing

## Processing Workflow

### Phase 1: Preparation
1. **Copy** Opus Master to workspace (preserve original)
2. **Apply** code block language tags (semi-automated + manual)
3. **Verify** image paths and document missing
4. **Check** hex notation (convert if needed)
5. **Run** LaTeX escape script:
```bash
./tools/latex-escape-all.sh \
  P2-Smart-Pins-Green-Book-Tutorial.md \
  P2-Smart-Pins-Green-Book-Tutorial-escaped.md
```

### Phase 2: Lua Filter Setup
Ensure `green-book-semantic-blocks.lua` handles:
- All 7 semantic div types
- Tutorial-specific elements (exercises, takeaways)

### Phase 3: Template Configuration
Verify `p2kb-smart-pins-content.sty` includes:
- Environments for all semantic types
- Tutorial-specific box styles
- Appropriate color scheme for extended reading

## Validation Steps

### Before PDF Generation
1. **Line count** should remain ~2800 lines (minor growth OK)
2. **All code blocks** have language tags
3. **All images** use assets/ paths
4. **Semantic divs** are unchanged (Lua filter will process)
5. **LaTeX escaping** completed successfully

### Quick Checks
```bash
# Verify language tags added
echo "Configuration blocks: $(grep -c '{.configuration}' escaped.md)"
echo "Spin2 blocks: $(grep -c '```spin2' escaped.md)"  
echo "PASM2 blocks: $(grep -c '```pasm2' escaped.md)"

# Verify semantic divs preserved
echo "Semantic markers: $(grep -c '^:::' escaped.md)"

# Check file growth is reasonable
echo "Original: $(wc -l < original.md) lines"
echo "Processed: $(wc -l < escaped.md) lines"
```

## Notes
- The Green Book was generated with most conventions in place
- Focus on verification rather than transformation
- Manual review of code blocks is critical for correct language tagging
- Preserve all semantic div markers for Lua filter processing

---
**Remember**: Always work on a copy, never modify the Opus Master directly!