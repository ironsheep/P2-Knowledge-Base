# Production Process Rules for PDF Generation

## 🚨 CRITICAL: Local Pandoc Cannot Be Used

**WARNING: Do NOT use local Pandoc for PDF work!**

- Local machine has ancient Pandoc 1.19 (no Lua filter support)
- PDF Forge has modern Pandoc 2.17 (required for our workflow)
- **ALL PDF generation must happen on PDF Forge**

**Best Practice:**
- Prepare files locally (markdown, templates, filters)
- Deploy to PDF Forge for all testing and production
- See `PDF-FORGE-INTERNAL-DETAILS.md` for technical details

## Directory Structure and Purpose

### Workspace-to-Outbound Mapping
**Parallel folder structure for easy navigation:**
- `/workspace/<canonical-name>/` → `/outbound/<canonical-name>/`

e.g. `/workspace/p2-pasm-desilva-style/` → `/outbound/p2-pasm-desilva-style/`. The set of
canonical names lives in `PUBLICATION-ROSTER.md`, not here.

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

## 🚨 CRITICAL RULE: ONLY CHANGED FILES GO IN OUTBOUND 🚨

**PDF Forge PERSISTS templates, filters, and styles - don't resend what hasn't changed!**

**ALWAYS include:**
- ✅ `request.json` - Required every time
- ✅ `[Document-Name].md` - The content to process
- ✅ `assets/` folder - If images are referenced

**ONLY include if YOU modified during THIS session:**
- ⚠️ `*.latex` files - Template you edited
- ⚠️ `*.sty` files - Style packages you changed
- ⚠️ `*.lua` files - Filters you created or fixed

**NEVER include:**
- ❌ Templates that haven't changed
- ❌ Filters that haven't changed
- ❌ Style files that haven't changed
- ❌ Intermediate work files
- ❌ Backup files
- ❌ Test versions

**Why "Only Changed Files" Matters:**
- PDF Forge has persistent storage for templates and filters
- Files sent once stay installed until replaced
- Sending unchanged files wastes time and causes confusion
- Keep workspace as source of truth for all files

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
1. Copy ONLY changed files (see rules above)
2. Use production names (no suffixes)
3. Verify request.json format includes request-requirements.json args
4. Ready for deployment to PDF Forge

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