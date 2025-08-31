# Production Process Rules for PDF Generation

## Directory Structure and Purpose

### `/workspace/desilva-manual/` - DEVELOPMENT AREA
**This is where ALL work happens:**
- Source files (unprocessed markdown)
- Work-in-progress files
- Test outputs with descriptive names
- Templates being edited
- Tracking documents

**Naming convention for iterations:**
- `P2-PASM-deSilva-Style-Part1.md` - Source
- `P2-PASM-deSilva-Style-Part1-FORMATTED.md` - After instruction formatting
- `P2-PASM-deSilva-Style-Part1-ESCAPED.md` - After LaTeX escaping
- `P2-PASM-deSilva-Style-Part1-PASS2.md` - Second visual pass
- `P2-PASM-deSilva-Style-Part1-FINAL.md` - Ready for production

### `/outbound/[document-name]/` - PRODUCTION STAGING
**ONLY final, deployment-ready files go here:**
- One markdown file (properly named, no suffixes)
- One LaTeX template 
- One request.json
- NO intermediate files
- NO backups
- NO test versions

**Strict naming rules:**
- Markdown: `[DocumentBaseName].md` (NO -FINAL, -COMPLETE, etc.)
- Template: `[template-name].latex`
- Request: `request.json` (always this exact name)

## Production Pipeline

### Phase 1: Development (workspace)
1. Edit source markdown
2. Run formatting scripts
3. Run escaping scripts
4. Test and iterate
5. Keep ALL versions with descriptive suffixes

### Phase 2: Validation (workspace)
1. Final visual review
2. Technical validation
3. Creation guide compliance check
4. Style guide compliance check

### Phase 3: Staging (outbound)
**ONLY when ready for PDF Forge:**
1. Copy ONLY the final files
2. Use production names (no suffixes)
3. Verify request.json format
4. User moves to PDF Forge

## Process Tracking Requirements

### For Each Document Part:
```
workspace/desilva-manual/
├── tracking/
│   ├── part1-iterations.md     # Track each pass
│   ├── part2-iterations.md     # Track each pass
│   └── issues-resolved.md      # What was fixed
├── P2-PASM-deSilva-Style-Part1.md           # Source
├── P2-PASM-deSilva-Style-Part1-PASS1.md     # First pass
├── P2-PASM-deSilva-Style-Part1-PASS2.md     # Second pass
├── P2-PASM-deSilva-Style-Part1-FINAL.md     # Production ready
└── visual-fixes-tracking.md                  # Issue tracking
```

### Version Naming Convention:
- **PASS1, PASS2, PASS3**: Visual/content iterations
- **FORMATTED**: After instruction formatting
- **ESCAPED**: After LaTeX escaping
- **REVIEWED**: After technical review
- **FINAL**: Ready for production

## Critical Rules

### 1. NEVER Work Directly in Outbound
- Outbound is for deployment only
- All work happens in workspace
- Only copy final files to outbound

### 2. Clear Naming Discipline
- Source files: Keep original names
- Work files: Add descriptive suffixes
- Production files: Clean names only

### 3. Track Everything
- Document what changed in each pass
- Keep iteration history
- Record issues and resolutions

### 4. Production Checklist
Before copying to outbound:
- [ ] All visual issues resolved
- [ ] Instructions properly formatted
- [ ] LaTeX escaping complete
- [ ] Template validated
- [ ] request.json correct format
- [ ] No test/temp files included

## Example Workflow

```bash
# In workspace - iterate freely
vim P2-PASM-deSilva-Style-Part1.md
./format-instructions.py ... -Part1-FORMATTED.md
./latex-escape-all.sh ... -Part1-ESCAPED.md
# Review PDF, find issues
vim P2-PASM-deSilva-Style-Part1-PASS2.md
# More iterations...

# When FINAL:
cp P2-PASM-deSilva-Style-Part1-FINAL.md \
   ../../outbound/P2-PASM-deSilva-Style/P2-PASM-deSilva-Style-Part1.md
cp template.latex ../../outbound/P2-PASM-deSilva-Style/
cp request-FINAL.json ../../outbound/P2-PASM-deSilva-Style/request.json
```

## The Golden Rule
**Workspace = Messy creativity allowed**
**Outbound = Production discipline required**

Never confuse the two!