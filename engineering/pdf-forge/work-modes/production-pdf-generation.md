# Production PDF Generation Work Mode Guide

**Purpose**: Generate final deliverable PDFs for distribution and publication  
**Script**: `generate-pdf.js` on PDF Forge  
**Format**: `document_generation`  
**Counterpart**: See `automated-pdf-testing.md` for rapid iteration/debugging

## 🎯 When to Use This Mode vs Testing Mode

**Use Production Mode (THIS GUIDE) when:**
- ✅ Visual refinement is complete
- ✅ All issues resolved through testing
- ✅ Ready to create final deliverable
- ✅ Need specific output filename (Manual-v1.pdf)
- ✅ Creating release documents for distribution

**Use Testing Mode (`automated-pdf-testing.md`) when:**
- 🔧 Debugging template issues
- 🔧 Testing Lua filters
- 🔧 Rapid visual iteration
- 🔧 Comparing before/after changes
- 🔧 Need quick feedback cycles

## System Architecture Comparison

| Aspect | Testing Mode | Production Mode |
|--------|-------------|----------------|
| **Script** | watch-shared-workspace.js | generate-pdf.js |
| **Location** | /interactive-testing/ | /outbound/[document]/ |
| **Request format** | tests array | documents array |
| **Purpose** | Debug & iterate | Final generation |
| **Output** | Timestamped test files | Named deliverables |
| **Typical time** | 30-60 seconds | 2-10 minutes |

## 🔴 MANDATORY PROCESS - APPLIES TO ALL DOCUMENTS

### Step 1: Check for Document-Specific Requirements

**ALWAYS run this command first:**
```bash
# Replace [document-name] with actual document folder name
cat /engineering/document-production/workspace/[document-name]/request-requirements.json
```

**Common document folders:**
- `p2-smart-pins-tutorial` - Smart Pins Green Book
- `pasm2-desilva-tutorial` - De Silva Tutorial  
- `pasm2-reference-manual` - PASM2 Reference Manual
- `p2-spin2-manual` - Spin2 Language Manual

**If file exists**, it contains MANDATORY pandoc arguments like:
```json
{
  "required_pandoc_args": ["--top-level-division=part"],
  "reason": "Document uses Part/Chapter structure",
  "discovered": "2025-08-25",
  "issue": "Without this, parts don't get page breaks"
}
```

### Step 2: Create Production Request

**Template for request.json:**
```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "document-name.md",
      "output": "Document-Name.pdf",
      "template": "template-name",
      "pandoc_args": [...],    // Include from request-requirements.json!
      "lua_filters": [...],     // Document-specific filters
      "metadata": {            // Optional variables
        "version": "1.0",
        "date": "September 2025"
      }
    }
  ]
}
```

**CRITICAL Rules:**
- ✅ `"format_type": "document_generation"` - REQUIRED
- ✅ `"documents"` array - NOT "tests"
- ✅ Template name WITHOUT .latex extension
- ✅ Include ALL pandoc_args from request-requirements.json
- ✅ Lua filters as array of filter names (no path/extension)

### Step 3: Prepare Outbound Directory

**Standard structure (flat - all files at root level):**
```
/engineering/document-production/outbound/[document-name]/
├── request.json                    # ALWAYS: Production request
├── Document-Name.md                 # ALWAYS: Document content
├── assets/                          # ALWAYS: Images subdirectory (if referenced)
│   └── *.png, *.jpg                #         Images stay in assets/
├── my-template.latex               # ONLY IF CHANGED: Template file
├── my-styles.sty                   # ONLY IF CHANGED: Style file
└── my-filter.lua                   # ONLY IF CHANGED: Lua filter

⚠️ IMPORTANT: .latex, .sty, and .lua files go at ROOT level, NOT in subdirectories!
```

## 🚨 CRITICAL: ONLY CHANGED FILES GO IN OUTBOUND 🚨

**PDF Forge has a PERSISTENT file system - templates and filters stay installed!**

**What to Copy from Workspace to Outbound:**

### **ALWAYS copy these files:**
- ✅ `request.json` - Required every time
- ✅ `[Document-Name].md` - The content (escaped if needed)
- ✅ `assets/` - Referenced images

### **ONLY copy if YOU modified during THIS session:**
- ⚠️ `*.latex` files - Templates you edited
- ⚠️ `*.sty` files - Style packages you changed
- ⚠️ `*.lua` filters - Filters you created or fixed

### **NEVER copy if unchanged:**
- ❌ Templates already on PDF Forge
- ❌ Filters that weren't modified
- ❌ Style files that are the same
- ❌ Foundation files shared across documents

**Why This Matters:** PDF Forge remembers installed files. Copying unchanged files wastes time and causes confusion about what actually changed.

**Example for Smart Pins:**
```bash
# From workspace to outbound
cp P2-Smart-Pins-Green-Book-Tutorial-divs.md ../../../outbound/p2-smart-pins-tutorial/
cp -r assets/ ../../../outbound/p2-smart-pins-tutorial/
cp request.json ../../../outbound/p2-smart-pins-tutorial/

# Only if modified:
cp filters/non-floating-images.lua ../../../outbound/p2-smart-pins-tutorial/  # If fixed
cp templates/p2kb-smart-pins.latex ../../../outbound/p2-smart-pins-tutorial/ # If changed
```

**Checklist:**
- [ ] request.json created with requirements from Step 1
- [ ] Markdown file escaped with latex-escape-all.sh (if needed)
- [ ] Assets folder with all referenced images
- [ ] Modified templates/styles/filters included
- [ ] Unchanged files NOT included (avoid clutter)

### Step 4: Deploy to PDF Forge

**User deploys the outbound folder to PDF Forge for generation**

## Common Document Requirements

### Smart Pins Tutorial
```json
"pandoc_args": ["--top-level-division=part"],
"lua_filters": ["non-floating-images", "smart-pins-colored-blocks"]
```

### De Silva Tutorial  
```json
"pandoc_args": ["--top-level-division=part"],
"lua_filters": ["part-chapter-pagebreaks", "desilva-div-to-environment"]
```

### PASM2 Reference Manual
```json
"pandoc_args": [],  // Check request-requirements.json
"lua_filters": []   // Document-specific
```

## Troubleshooting

### Missing pandoc_args symptoms:
- Parts don't start on new pages
- Chapter numbering incorrect
- Section hierarchy broken

### Missing lua_filters symptoms:
- Images floating to wrong pages
- Code blocks not colored
- Special environments not rendering

### Always verify:
1. request-requirements.json checked
2. All required args included
3. Filter names match exactly
4. Template name correct (no .latex)

## Why request-requirements.json Exists

Different documents have different structural needs:
- **Part/Chapter documents**: Need `--top-level-division=part`
- **Article-style documents**: May need different division settings
- **Custom structures**: May need special pandoc flags

The `request-requirements.json` file ensures these critical settings aren't forgotten during production generation.

## Typical Workflow: Testing → Production

1. **Start with Testing Mode** (`automated-pdf-testing.md`)
   - Debug templates and filters
   - Iterate on visual refinements
   - Validate fixes work correctly

2. **Transition to Production Mode** (this guide)
   - Verify request-requirements.json
   - Create production request
   - Generate final deliverable

3. **Deploy Result**
   - Review generated PDF
   - Confirm quality standards met
   - Distribute to stakeholders

---

**This is the standard process for ALL production PDF generation, regardless of document type.**

**See also**: `automated-pdf-testing.md` for the testing workflow that typically precedes production generation.