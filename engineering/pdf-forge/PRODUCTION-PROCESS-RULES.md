# Production Process Rules for PDF Generation

## 🚨 CRITICAL: Pandoc Version Distinction

**WARNING: Local machine has ancient Pandoc 1.19 - DO NOT USE FOR TESTING!**

### Environment Differences:
- **Local Machine**: Pandoc 1.19.2.1 (pre-2016, NO Lua filter support)
  - Found at: `/Users/stephen/anaconda3/bin/pandoc`
  - **NEVER use this for PDF work** - it's misleading and incompatible
  - Cannot test Lua filters locally
  - Cannot generate proper PDFs locally
  
- **PDF Forge**: Pandoc 2.17.1.1 (modern version with full Lua filter support)
  - This is where ALL actual PDF generation happens
  - Supports all our Lua filters
  - Has proper LaTeX integration
  - This is the ONLY Pandoc that matters for our workflow

### Key Implications:
1. **Cannot test Lua filters locally** - they will fail with "unrecognized option"
2. **All PDF testing must go through PDF Forge** - no local shortcuts
3. **Local Pandoc output is NOT representative** - different version = different behavior
4. **Filter errors only show up on PDF Forge** - that's where they actually run

### Best Practice:
- Prepare files locally (markdown, templates, filters)
- Deploy to PDF Forge for ALL testing and production
- Never trust local Pandoc output or errors
- When debugging, remember: filters run on PDF Forge, not locally

## Directory Structure and Purpose

### Workspace-to-Outbound Mapping
**Parallel folder structure for easy navigation:**
- `/workspace/p2-smart-pins-tutorial/` → `/outbound/p2-smart-pins-tutorial/`
- `/workspace/p2-pasm-desilva-style/` → `/outbound/p2-pasm-desilva-style/`
- `/workspace/pasm2-reference-manual/` → `/outbound/pasm2-reference-manual/`

**The folders have identical names** - just swap "workspace" for "outbound" in the path.

### `/workspace/desilva-manual/` - DEVELOPMENT AREA
**This is where ALL work happens:**
- Source files (unprocessed markdown)
- Work-in-progress files
- Test outputs with descriptive names
- Templates being edited
- Tracking documents
- **request-requirements.json** - Special pandoc arguments needed for this document

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
- Modified .sty, .lua, or .latex files (when changed)
- NO intermediate files
- NO backups
- NO test versions

**CRITICAL: Template and Support File Persistence**
- PDF Forge remembers the last copy of all .latex, .sty, and .lua files
- These files persist across PDF generation sessions
- Only copy modified files to outbound when you change them
- The Knowledge Base repository is the source of truth for these files
- User deploys modified files from outbound to PDF Forge to update production environment

**🎯 IMPORTANT: Files Disappear from Outbound - This is NORMAL!**
- User drags files from outbound to PDF Forge
- **Files disappearing = successful deployment** (don't panic!)
- Empty outbound folder means files are now on the Forge
- Assets folder may remain as backup (intentional)
- Workspace always contains the masters - you can re-copy if needed
- During production iterations, keep copies in workspace to re-deploy quickly

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
4. Copy ONLY modified template files:
   - If you changed p2kb-smart-pins.latex → copy it
   - If you changed p2kb-smart-pins-content.sty → copy it
   - If you changed green-book-semantic-blocks.lua → copy it
   - If files weren't changed → DON'T copy (Forge has them)
5. User moves files from outbound to PDF Forge

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

## Request Requirements Snippet Pattern

### Purpose of request-requirements.json
Each document workspace may contain a `request-requirements.json` file that specifies:
- Critical pandoc arguments needed for proper rendering
- The reason why these arguments are required
- When the requirement was discovered
- The issue that occurs without these arguments

### Example request-requirements.json:
```json
{
  "required_pandoc_args": ["--top-level-division=part"],
  "reason": "Smart Pins uses Part/Chapter structure",
  "discovered": "2025-08-25",
  "issue": "Without this, parts don't get page breaks"
}
```

### Using the Snippet
When creating the production request.json:
1. Check if workspace has request-requirements.json
2. Add the `required_pandoc_args` to the document's `pandoc_args` array
3. Include standard arguments like `--toc`, `--number-sections` as needed

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