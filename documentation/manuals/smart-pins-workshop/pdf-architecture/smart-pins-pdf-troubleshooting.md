# Smart Pins PDF Troubleshooting Guide

## Common Problems & Solutions

*Last Updated: 2025-08-29*  
*Purpose: Operational guide for debugging PDF generation issues*

---

## 🚨 Common Issues

### Page Breaks Not Working
**Symptoms**: Chapters/parts not breaking where expected  
**Cause**: Conflicting page break logic between LaTeX and Lua  
**Solution**: 
- Ensure titlesec is NOT loaded
- Verify `part-chapter-pagebreaks.lua` is in lua_filters array
- Check filter is actually on PDF Forge

### Colors Missing from Code Blocks
**Symptoms**: All code blocks gray instead of colored  
**Cause**: Lua filter not running or being overridden  
**Solution**:
- Verify `smart-pins-colored-blocks.lua` in request.json
- Check filter order (pagebreaks first, then coloring)
- Ensure all 4 environments exist in `p2kb-smart-pins-content.sty`

### Headers Showing "Contents" Everywhere
**Symptoms**: Every page header says "Contents"  
**Cause**: TOC sets `\leftmark` and nothing clears it  
**Solution**: Add `\markboth{}{}` after TOC in main template

### LaTeX Error: Environment Undefined
**Symptoms**: `Environment AntipatternBlock undefined`  
**Cause**: Incomplete or regressed .sty file  
**Solution**: 
- Verify complete 415-line version of `p2kb-smart-pins-content.sty`
- Check all 4 environments defined: ConfigBlock, Spin2Block, PASM2Block, AntipatternBlock

### Request.json Validation Failure
**Symptoms**: `Missing required field: documents`  
**Cause**: Wrong structure for lua_filters  
**Solution**: Use per-document array, not top-level pandoc_args

---

## 🔧 LaTeX Escaping Pipeline

### Process Overview
```bash
# Run BEFORE sending to PDF Forge
./tools/latex-escape-all.sh input.md output.md
```

### What Gets Escaped
- Underscores outside code blocks: `_` → `\_`
- Dollar signs: `$` → `\$`
- Percent signs: `%` → `\%`
- Ampersands: `&` → `\&`
- Hash symbols: `#` → `\#` (context-dependent)

### Double-Escaping Prevention
**WARNING**: Never escape an already-escaped file!
- Check for existing backslashes before escaping
- Keep track of which files have been processed
- Use different filenames for escaped versions

---

## 🏭 Testing vs Production Workflows

### Testing Workflow (PDF Forge Workspace)
```
/pdf-forge-workspace/
├── templates/       # Live testing
├── filters/         # Experimental filters
└── test-docs/       # Test documents
```
- Used for iterative development
- May contain experimental code
- NOT source of truth

### Production Workflow
```
1. Edit in: /exports/pdf-generation/workspace/manual-templates/
2. Copy to: /exports/pdf-generation/outbound/P2-Smart-Pins-Reference/
3. Deploy to: PDF Forge system
4. Generate PDF on Forge
```

### Critical Rules
- ❌ NEVER use pandoc locally (even though it exists)
- ❌ NEVER edit in outbound directory
- ❌ NEVER use pdf-forge-workspace as reference
- ✅ ALWAYS edit master templates
- ✅ ALWAYS escape before sending to Forge

---

## 🐛 Known Issues & Workarounds

### Spurious .tex File Generation
**Issue**: Sometimes a .tex file appears in outbound  
**Impact**: Can interfere with PDF generation  
**Workaround**: Delete any .tex files before deployment

### Old request.json Conflicts
**Issue**: Previous request.json can cause wrong settings  
**Impact**: Filters may not run or wrong template used  
**Workaround**: Always clear and recreate request.json

### Filter Order Matters
**Issue**: Filters can interfere with each other  
**Impact**: Later filters may override earlier ones  
**Workaround**: Test filter combinations, order matters

### File Regression Risk
**Issue**: Incomplete files can overwrite complete ones  
**Impact**: Lost functionality (e.g., missing environments)  
**Best Practice**: 
- Check file sizes before replacing
- Keep backups of working versions
- Use MultiEdit for changes, not Write

---

## 🔍 Debugging Techniques

### Check Filter Execution
Lua filters can inject comments:
```lua
local debug_comment = pandoc.RawInline('latex', 
  '% LUA FILTER: Processing header level ' .. elem.level)
```
Look for these in the generated .tex file

### Verify Template Loading
Check PDF Forge logs for:
- Which template was loaded
- Which .sty files were found
- Any missing package errors

### Test Incrementally
1. Test with minimal markdown
2. Add one feature at a time
3. Identify exactly what breaks it

---

## 📋 Pre-Deployment Checklist

- [ ] Markdown is escaped with `latex-escape-all.sh`
- [ ] All .sty files copied to outbound
- [ ] Lua filters exist on PDF Forge
- [ ] request.json has correct structure
- [ ] No .tex files in outbound
- [ ] Previous request.json cleared
- [ ] File sizes look reasonable

---

## 🆘 Emergency Recovery

### If Colors Disappear
1. Check `p2kb-smart-pins-content.sty` has all 4 environments
2. Verify filter in request.json
3. Check filter exists on Forge

### If Pagination Breaks
1. Verify no titlesec in foundation
2. Check `part-chapter-pagebreaks.lua` on Forge
3. Verify filter in lua_filters array

### If Build Fails Completely
1. Check for LaTeX escaping issues
2. Verify all environments defined
3. Look for undefined commands
4. Check template references

---

*For architecture overview, see `smart-pins-pdf-architecture.md`*  
*For component status, see `smart-pins-component-status.md`*