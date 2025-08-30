# PDF Generation Format Guide

**Created**: 2025-08-20  
**Purpose**: Define consistent file formats for PDF Forge pipeline  
**Critical**: Use these exact formats to ensure successful PDF generation

## 🎯 Document-Specific Creation Guides

**IMPORTANT**: This guide covers UNIVERSAL patterns for all PDF generation. Each document has its own creation guide with specific requirements:

- **Smart Pins Reference**: `/documentation/manuals/smart-pins-reference/creation-guide.md`
- **PASM2 deSilva Manual**: `/documentation/manuals/p2-pasm-desilva-style/creation-guide.md`  
- **[Other documents]**: `/documentation/manuals/[document-name]/creation-guide.md`

**ALWAYS check the document's creation guide for:**
- Specific .sty file requirements
- Exact template references
- Document-specific request.json structure
- Pandoc arguments and Lua filter usage
- Asset management requirements
- Architecture phase status

**Rule**: Universal patterns here + Document specifics in creation guide = Complete deployment knowledge

## 🏭 PRODUCTION FILENAME DISCIPLINE (2025-08-25)

**CRITICAL RULE**: Use production filenames from day 1 - practice production process every iteration.

### Filename Consistency Rules:
- ✅ **Base name consistency**: `Document-Name.md` → `Document-Name.pdf`
- ✅ **Same files improved iteratively**: Each iteration replaces previous version
- ✅ **Production naming always**: When we release, files already have official names
- ❌ **NO version suffixes**: No -test, -v1, -draft, -auto-indent in filenames
- ❌ **NO random renaming**: Never change established filenames mid-process

### Why This Matters:
- **Prevents confusion**: User knows exactly which file is current
- **Production practice**: Every iteration practices the release process
- **Clean releases**: Final files are already named correctly
- **No mistakes**: Eliminates "which file is the real one?" problems

### Example - Smart Pins Reference:
```
Markdown: P2-Smart-Pins-Complete-Reference.md
PDF Output: P2-Smart-Pins-Complete-Reference.pdf
Request.json: "output": "P2-Smart-Pins-Complete-Reference.pdf"
```

**Every iteration replaces the same filenames - no proliferation of test files.**

## 🎯 NEW: Request Requirements Pattern (2025-08-25)

**MANDATORY for all new documents**: Each document workspace must include `request-requirements.json` when special Pandoc arguments are needed.

### request-requirements.json Format
```json
{
  "required_pandoc_args": ["--top-level-division=part"],
  "reason": "Document uses Part/Chapter structure",
  "discovered": "2025-08-25",
  "issue": "Without this, page breaks fail"
}
```

### Deployment Process
1. **Check workspace** for `request-requirements.json` or `request-source-of-truth.json`
2. **If present**: Use as basis for creating request.json
3. **Deploy** complete request.json to outbound

### Process Rules
- **New requests**: Always check workspace for requirements/source-of-truth file
- **Request changes needed**: Update source-of-truth file, regenerate request.json
- **Never lose requirements**: They're versioned with the document in workspace

## 📁 Workspace Organization for PDF Generation

### 🆕 Documents with Images Pattern (Established 2025-08-24)

For documents containing images, use this structure:

```
/exports/pdf-generation/
├── workspace/                    # Master files for iteration
│   └── [document-name]/          # Document workspace
│       ├── Document.md           # Master markdown
│       ├── template.latex        # Master template
│       └── request-requirements.json  # **NEW: Special Pandoc args**
│
└── outbound/                     # Deployment folders
    └── [Document-Name]/          # Ready for PDF Forge
        ├── Document.md           # LaTeX-escaped markdown
        ├── template.latex        # LaTeX template (if modified)
        ├── request.json          # Generation config
        └── assets/               # Images folder (if document has images)
            └── *.png            # All referenced images
```

**Key Rules for Images**:
1. **Always use `assets/` subfolder** for images
2. **Use relative paths** in markdown: `![Caption](assets/image.png)`
3. **Copy entire folder** to PDF Forge including assets
4. **NO SPACES in image filenames** - Use hyphens: `P2-SmartPins-page01.png` ✅, not `P2 SmartPins page01.png` ❌
5. **URL encoding issues** - Spaces become %20 and break image loading

### Critical Directory Structure

```
/exports/pdf-generation/
├── workspace/                    # CLAUDE'S ITERATION WORKSPACE
│   ├── desilva-manual/          # Masters for De Silva manual
│   ├── reference-manual/        # Masters for PASM2 reference
│   └── WORKSPACE-PROCESS.md    # This process documentation
│
└── outbound/                     # TEMPORARY DELIVERY FOLDERS
    ├── P2-PASM-deSilva-Style/   # Empty until delivery
    └── PASM2-Reference/         # Empty until delivery
```

### Why This Structure?

**workspace/** = Where Claude iterates on documents
- Master markdown files live here
- Master templates live here
- Split into manageable chunks (<50KB each for speed)
- Edit, test, refine repeatedly
- Version controlled, persistent storage

**outbound/** = Temporary transfer point to PDF Forge
- Files appear here only when ready for PDF generation
- User moves files to PDF Forge
- Files disappear after user grabs them
- Directory returns to empty state
- NOT for permanent storage

### The Iteration Process

1. **Edit Phase** (in workspace/)
   - Modify master markdown files
   - Update LaTeX template as needed
   - Keep files under 50KB for fast editing

2. **Delivery Phase** (to outbound/)
   ```bash
   # Run escaping script
   /tools/latex-escape-all.sh workspace/Part1.md outbound/Part1.md
   
   # Copy template if changed
   cp workspace/template.latex outbound/
   
   # Create request.json
   ```

3. **User Grabs Files**
   - Files disappear from outbound/
   - User generates PDF on Forge
   - User provides visual feedback

4. **Refinement Phase** (back to workspace/)
   - Apply feedback to masters
   - Iterate until visually perfect

### Key Rules

- **Never work directly in outbound/** - It's temporary storage only
- **No "-escaped" suffix** - All markdown for PDF is escaped by definition
- **Empty outbound = success** - Files disappeared means user grabbed them
- **Split large files** - Keep under 50KB for editing speed
- **Combine only at end** - Final assembly happens after all parts are perfect

## 🔧 PDF Forge Installation Requirements

### ✅ Current Installation Status (2025-08-20)

**PDF Forge now has complete LaTeX installation**:
```bash
# Complete TeXLive installation command used:
sudo apt-get install texlive-full
```

### What texlive-full Provides
| Component | Included | Benefits |
|-----------|----------|----------|
| **ALL LaTeX packages** | Complete distribution | No missing dependencies |
| **XeLaTeX engine** | Modern font handling | Unicode support, Charter fonts |
| **tcolorbox with ALL libraries** | skins, breakable, etc. | Advanced colored boxes with dashed borders |
| **Font packages** | Charter, Palatino, etc. | Professional typography |
| **Graphics packages** | TikZ, PGF complete | Complex diagrams and borders |
| **Math packages** | amsmath, amsfonts, etc. | Mathematical typesetting |

### Package Verification (All Available)
```bash
# All these should return file paths:
kpsewhich tcolorbox.sty         # ✅ Advanced colored boxes
kpsewhich tikz.sty              # ✅ Graphics and borders
kpsewhich charter.sty           # ✅ Charter font
kpsewhich soul.sty              # ✅ Text highlighting
xelatex --version               # ✅ XeLaTeX engine
```

### Advanced Features Now Supported
- **Dashed/dotted borders**: `borderline={1pt}{0pt}{gray!50, dashed}`
- **Enhanced tcolorbox**: All skin libraries available
- **Professional fonts**: Charter, Palatino, Latin Modern
- **Graphics**: TikZ for complex diagrams
- **Math**: Complete mathematical typesetting
- **Unicode**: Full international character support

### Why texlive-full vs Individual Packages
| Approach | Size | Reliability | Features |
|----------|------|-------------|----------|
| **Individual packages** | ~1GB | Dependency issues possible | Limited |
| **texlive-full** | ~4GB | 100% reliable | Complete |

## 🚨 CRITICAL: Template Management Process

### LaTeX Template Workflow
**ALWAYS follow this exact process for template changes:**

1. **Check Master Template**: `/exports/pdf-generation/outbound/pasm2-manual-v1/p2kb-pasm-desilva.latex`
2. **Make Changes in Master**: Edit the master template only
3. **Copy to Production**: `cp master-template production-directory/`
4. **NEVER check production directory first** - the master is the source of truth

### PDF Generation File Flow
**CRITICAL UNDERSTANDING**: Files get MOVED during PDF generation, not copied.

```
MY Working Directory → User copies to → PDF Forge
                                    ↓
                              Files MOVED (not copied)
                                    ↓
                              Gone from output directory
```

**Process Rules**:
- **I must keep my own copies** in working directories
- **NEVER expect files in output directory** after user runs PDF
- **Check MY working directories**, not output directory
- User copies FROM my output directory TO PDF Forge
- During generation, files get moved out of output directory

### LaTeX Primitive Conflicts
**Fixed LaTeX primitive conflicts in template**:
- `\immediate` → `\immediatevalue` (LaTeX primitive)
- `\label` → `\codelabel` (LaTeX primitive) 
- `\value` → `\codevalue` (LaTeX primitive)
- `\address` → `\memaddress` (LaTeX primitive)

**Why This Matters**: LaTeX has many built-in commands. Custom `\newcommand` definitions cannot override these primitives without causing compilation errors.

## 🔥 CRITICAL WORKFLOW RULE: NO CONTEXT FOR PROCESS CHANGES

### Process Documentation Protocol
**ALWAYS follow this exact rule:**

❌ **NEVER store process changes in context keys**  
✅ **ALWAYS update process documents immediately**  

**Why This Matters**:
- **VERSION CONTROL LOSS**: Context keys exist outside Git repository
- **Knowledge Disappears**: When we commit document improvements, context knowledge is lost forever
- **Process Evolution Lost**: Valuable debugging and process discoveries not captured in version history
- **Team Knowledge Loss**: Other team members can't see process improvements made via context
- **Reproducibility Failure**: Future sessions can't benefit from undocumented process knowledge

**Implementation Rule**:
```
Discover process improvement → Update document NOW → Delete any context keys
```

**Examples of What Goes to Documents NOT Context**:
- Template management workflows
- File generation processes  
- Error resolution procedures
- Critical operational knowledge
- Debugging discoveries
- Tool usage patterns

**Decision**: Chose reliability over size for professional document generation.

## 📁 File Format Requirements

### For PDF Forge System

| Component | File Extension | Format | Location |
|-----------|---------------|--------|----------|
| **Main Document** | `.md` | Markdown | `document.md` or specific name |
| **Request Config** | `.json` | JSON | `request.json` |
| **Template** | Referenced by name | N/A | Specified in request.json |
| **Style/Template** | `.latex` | LaTeX | On PDF Forge server (not in package) |

### ❌ Common Mistakes to Avoid

1. **DON'T** provide `.tex` files - PDF Forge expects `.md`
2. **DON'T** include `.latex` template files - Reference them by name
3. **DON'T** mix LaTeX and Markdown syntax in the `.md` file
4. **DON'T** use raw LaTeX commands in Markdown

### ✅ Correct File Structure

```
/exports/pdf-generation/outbound/pasm2-manual-v1/
├── P2-PASM-deSilva-Style.md    # Main content in Markdown
├── request.json                 # Configuration file
├── compile-order.txt            # (optional) for multi-file
└── README.md                    # Instructions
```

## 🎆 NEW Formatting Features Available

With these packages installed, we can now use:

### Visual Content Markers
- **🚧 Violet boxes**: Missing content flags
- **🔍 Orange boxes**: Technical review needed
- **🎨 Blue boxes**: Diagram placeholders
- **Gray + dotted border**: Optional sidetracks
- **Gray no border**: Interlude sections
- **Yellow background**: Inline code highlighting
- **Green tinted**: Chapter celebrations

### Typography Improvements
- **Charter/Palatino fonts**: Professional appearance
- **Better line spacing**: Reduced eye strain
- **Proper code fonts**: Consolas/Source Code Pro
- **Smart kerning**: Better character spacing

### Layout Features
- **3-column index**: Maximum density
- **Keep-together blocks**: Code examples don't split
- **Auto-numbered diagrams**: Consistent references
- **Smart page breaks**: Chapters/appendices start fresh

### These Features Work In:
- P2-PASM-deSilva-Style (tutorial format)
- Future manuals using p2kb- templates
- Any document needing pedagogical formatting
- Technical documentation with visual hierarchy

## 📝 Markdown Format for PDF Forge

### Special Blocks (Use Triple Colons)

```markdown
::: sidetrack
Content with gray background and dotted border
:::

::: interlude
Content with gray background, no border
:::

::: missing
🚧 **CONTENT MISSING**
What needs to be added
:::

::: review
🔍 **NEEDS REVIEW**
What needs verification
:::

::: diagram
🎨 **DIAGRAM NEEDED**
Description of diagram
:::

::: yourturn
Exercise content
:::

::: chapterend
✨ Celebration message
:::
```

### Code Blocks

```markdown
```pasm2
' P2 Assembly code here
mov x, #42
```　
```

### Typography

- **Bold**: `**text**`
- *Italic*: `*text*`
- `Inline code`: `` `code` ``
- Headers: Use # for chapters, ## for sections

## 🎯 NAMING CONVENTIONS

### Document Naming Rules

**Pattern**: `P2-[TYPE]-[STYLE].md`

**Examples**:
- `P2-PASM-deSilva-Style.md` - Our manual in deSilva style
- `P2-PASM-Reference.md` - Technical reference (different doc)
- `P2-Spin2-Tutorial.md` - Spin2 tutorial

**PDF Output**: Same base name with `.pdf`
- `P2-PASM-deSilva-Style.pdf`

### Template Naming on PDF Forge

**Pattern**: `p2kb-[purpose]`

**Our Templates**:
- `p2kb-pasm-desilva` - deSilva-style manual template
- `p2kb-technical-ref` - Technical reference template
- `p2kb-tutorial` - General tutorial template
- `p2kb-smart-pins` - Smart Pins reference template

**MANDATORY RULES**:
1. **All P2 Knowledge Base templates MUST start with `p2kb-`**
2. **Template file**: `p2kb-[purpose].latex` (with extension when saved)
3. **Template reference in request.json**: `"template": "p2kb-[purpose]"` (NO .latex extension)
4. **Never use version numbers** in template names (no -v1, -v2, -fixed, etc.)

## 📋 Request.json Format - ALWAYS USE THIS EXACT STRUCTURE

### 📌 Release Status Headers - CRITICAL REQUIREMENT

**MANDATORY**: The `header-right` field MUST reflect the current release status:

| Release Phase | Header-Right Value | Purpose |
|--------------|-------------------|----------|
| **Technical Review** | `"TECHNICAL REVIEW"` | P2 assembly accuracy validation |
| **Editorial Review** | `"EDITORIAL REVIEW"` | Grammar, clarity, flow |
| **Community Preview** | `"COMMUNITY PREVIEW"` | User feedback gathering |
| **Release Candidate** | `"RC-[number]"` | Final testing before release |
| **Final Release** | (omit header-right) | Production version |

**Example for Technical Review Phase**:
```json
"metadata": {
  "header-left": "Discovering P2 Assembly",
  "header-center": "",
  "header-right": "TECHNICAL REVIEW",  // Release status here!
  "footer-left": "deSilva"
}
```

**Why This Matters**:
- Readers immediately know document status
- Prevents confusion about completeness
- Tracks document through review pipeline
- Maintains professional appearance

### ⚠️ CRITICAL: This is the ONLY format that works - memorize it!

```json
{
  "documents": [     // REQUIRED: Must be array, even for single document
    {
      "input": "P2-PASM-deSilva-Style.md",      // Input markdown file
      "output": "P2-PASM-deSilva-Style.pdf",     // Output PDF name
      "template": "p2kb-pasm-desilva",          // Template name (no .latex)
      "lua_filters": ["filter-name1", "filter-name2"],  // OPTIONAL: Lua filters to apply
      "variables": {
        "title": "Discovering P2 Assembly",
        "subtitle": "Build, Experiment, and Master the Propeller 2",
        "author": "P2 Community",
        "footer": "In the Spirit of deSilva's P1 Tutorial"
      }
    }
  ],
  "options": {
    "cleanup": true,
    "archive": false,   // Usually false for testing
    "optimize": false   // Usually false for testing
  }
}
```

### 🔧 Lua Filters Field (Optional)

**When to use `lua_filters`:**
- Add this field when you need Lua filter processing
- Filters are applied in the order specified
- Filter names should NOT include path or .lua extension
- PDF Forge looks for filters in its filters/ directory

**Example with Lua filters:**
```json
{
  "documents": [{
    "input": "P2-Smart-Pins-Complete-Reference.md",
    "output": "P2-Smart-Pins-Complete-Reference.pdf",
    "template": "p2kb-smart-pins",
    "lua_filters": [
      "smart-pins-block-coloring",   // Adds color to code blocks
      "part-chapter-pagebreaks"      // Manages page breaks
    ],
    "variables": {
      "title": "P2 Smart Pins Complete Reference",
      "subtitle": "Specifications and Implementation for All 32 Modes",
      "author": "P2 Community",
      "footer": "Version 1.0 - Technical Review Draft"
    }
  }]
}
```

### 🔴 COMMON MISTAKES THAT WASTE TIME:

#### Mistake 1: Missing documents array wrapper
```json
// ❌ WRONG - Missing documents array:
{
  "input_file": "...",
  "output_file": "..."
}

// ✅ CORRECT - Always wrapped in documents array:
{
  "documents": [{
    "input": "...",
    "output": "..."
  }]
}
```

#### Mistake 2: Using "metadata" instead of "variables"
```json
// ❌ WRONG - Using metadata:
{
  "documents": [{
    "metadata": {
      "title": "..."
    }
  }]
}

// ✅ CORRECT - Use variables:
{
  "documents": [{
    "variables": {
      "title": "..."
    }
  }]
}
```

#### Mistake 3: Including .latex extension in template reference
```json
// ❌ WRONG - Has .latex extension:
"template": "p2kb-smart-pins.latex"

// ✅ CORRECT - No extension:
"template": "p2kb-smart-pins"
```

## 📷 Asset (Image) Management Workflow

### 🔴 CRITICAL: Asset Folder Requirements

**MANDATORY for documents with images:**

1. **Folder Structure**:
   ```
   Document-Folder/
   ├── Document.md           # References: assets/image.png
   ├── assets/               # MUST be named exactly "assets"
   │   └── *.png            # NO SPACES in filenames!
   ├── template.latex
   └── request.json
   ```

2. **Image Filename Rules**:
   - ✅ **CORRECT**: `P2-SmartPins-page01.png` (hyphens)
   - ❌ **WRONG**: `P2 SmartPins page01.png` (spaces)
   - **Why**: Spaces become %20 in URLs, breaking image loading

3. **Markdown References**:
   ```markdown
   ![Caption](assets/image-name.png)
   ```
   - Always use relative path `assets/`
   - Never use absolute paths
   - Never use `../` or complex paths

4. **Deployment Process**:
   ```bash
   # Copy ENTIRE folder to PDF Forge
   cp -r Document-Folder/ [PDF-FORGE]/inbox/
   
   # Assets folder MUST be in inbox alongside markdown:
   inbox/
   ├── Document.md
   ├── request.json
   └── assets/        # Images here
       └── *.png
   ```

5. **Common Failures**:
   - **"Could not fetch resource"** → Check for spaces in filenames
   - **Images missing** → Verify assets/ folder was copied
   - **Wrong path** → Ensure using `assets/` not `./assets/` or `/assets/`

### Asset Workflow Checklist:
- [ ] Create `assets/` subfolder (exact name)
- [ ] Place all images in assets folder
- [ ] NO SPACES in image filenames (use hyphens)
- [ ] Reference as `assets/filename.png` in markdown
- [ ] Copy entire folder structure to PDF Forge
- [ ] Verify assets/ is at same level as markdown

## 🎨 Template Management Process

### 🔴 CRITICAL: Master-Copy Workflow

**ALWAYS follow this sequence when updating templates:**

1. **Update Master First**: `/documentation/pdf-templates-master/[template-name].latex`
2. **Copy to Document Folder**: `cp master-template target-folder/`
3. **Deploy to PDF Forge**: User handles PDF Forge template upload

**Why This Matters:**
- Ensures all improvements are preserved in master
- Prevents losing fixes when regenerating documents
- Maintains version control and change tracking
- Creates reliable source of truth for templates

**Example Process:**
```bash
# 1. Fix master template
vim /documentation/pdf-templates-master/p2kb-pasm-desilva.latex

# 2. Copy to document folder
cp /documentation/pdf-templates-master/p2kb-pasm-desilva.latex \
   /exports/pdf-generation/outbound/P2-PASM-deSilva-Style/

# 3. User deploys to PDF Forge
# (User handles this step)
```

**⚠️ Template Change Checklist:**
- [ ] Master template updated with fix
- [ ] Fix tested and verified
- [ ] Template copied to document folder
- [ ] Document generation verified
- [ ] Master template committed to git

### Template Naming Policy

**CRITICAL RULE**: Templates NEVER have version suffixes

✅ **CORRECT**:
- `p2kb-pasm-desilva.latex`
- `p2kb-technical-ref.latex`
- `p2kb-tutorial.latex`

❌ **WRONG**:
- `p2kb-pasm-desilva-v2.latex`
- `p2kb-pasm-desilva-fixed.latex`
- `p2kb-pasm-desilva-draft.latex`
- `p2kb-pasm-desilva-old.latex`

**Update Process**:
1. Always use the same template name
2. Overwrite existing template with updates
3. Delete any versioned variants
4. Keep templates folder clean

**Benefits**:
- request.json never needs template name updates
- No confusion about which version to use
- Clean template directory
- Simple deployment

### Available Templates on PDF Forge

| Template Name | Purpose | Features |
|--------------|---------|----------|
| `p2kb-pasm-desilva` | PASM2 Manual (deSilva style) | Colored boxes, custom fonts, pedagogical |
| `p2kb-technical-ref` | Technical Reference | Formal, minimal styling |
| `p2kb-tutorial` | Tutorial Style | Friendly, lots of visuals |

### How Templates Work

1. **Template lives on PDF Forge server** as `.latex` file
2. **You reference it by name** in request.json
3. **Variables in request.json** fill template placeholders
4. **Markdown content** gets converted and inserted

## 🔧 PRODUCTION WORKFLOW - MANDATORY PROCESS

### 🎯 Scratchpad Directory Protocol

**CRITICAL**: We now operate under strict production etiquette. All development work MUST use the Scratchpad directory.

#### Scratchpad Usage Rules:
1. **Location**: `/Scratchpad/` (root of P2-Knowledge-Base repository)
2. **Purpose**: ALL development, testing, debugging, and experimentation
3. **Cleanup**: When problem is solved, DELETE ALL FILES from Scratchpad
4. **Git Status**: Added to `.gitignore` - never versioned
5. **Production**: Only final, clean files in production directories

#### Production Directory Rules:
✅ **ONLY production files**:
- Document: `[DocName].md` (processed, escaped, final)
- Request: `request.json` (clean configuration)
- Template: `[template-name].latex` (if changed)
- README: `README.md` (instructions)

❌ **NEVER in production**:
- Test files (use Scratchpad)
- Backup files (automatic cleanup)
- Version suffixes (-v1, -FIXED, -escaped)
- Development artifacts

#### Workflow Protocol:
1. **Problem arises** → Work in `/Scratchpad/`
2. **Solution found** → Apply to production files
3. **Success confirmed** → DELETE everything in `/Scratchpad/`
4. **Production ready** → Only clean files remain

#### LaTeX Escaping Production Process:
1. Source document → `/Scratchpad/` for processing
2. Apply escaping script: `latex-escape-all.sh`
3. Test thoroughly in `/Scratchpad/`
4. Deploy final result with production name
5. Clean `/Scratchpad/` completely

**This process ensures every iteration improves production discipline.**

### 🧪 REGRESSION TESTING PROTOCOL

**CRITICAL**: Every time we discover a case our script doesn't handle, we add it to the test suite.

#### Regression Test Files:
- **Test Cases**: `/tools/latex-escaping-test-cases.md` (input patterns)
- **Gold Standard**: `/tools/latex-escaping-test-cases-GOLD-STANDARD.md` (expected output)
- **Test Script**: `/tools/latex-escape-all.sh` (must handle all cases)

#### When Script Fails in Production:
1. **Identify Pattern** - Find exact text that caused failure
2. **Add to Test Suite** - Update test-cases.md with new pattern
3. **Update Gold Standard** - Add correctly escaped version
4. **Test Script** - Run script against updated test suite
5. **Fix Script** - Update script if needed until tests pass
6. **Validate** - Ensure script output matches gold standard exactly
7. **Deploy** - Apply to production when all tests pass

#### Test Validation Command:
```bash
# Script must produce output identical to gold standard
diff latex-escaping-test-cases-GOLD-STANDARD.md script-output.md
# No output = perfect match = script ready for production
```

**This ensures our script gets more robust with every failure we encounter.**

## 🚫 What NOT to Include

### Don't Send These Files:
- `.tex` files (PDF Forge doesn't process these)
- `.latex` style files (already on server)
- `.sty` LaTeX packages (server has them)
- Raw LaTeX documents (use Markdown)

### Don't Use This Syntax in Markdown:
- `\newtcolorbox{}` - LaTeX commands
- `\begin{document}` - LaTeX structure
- `\usepackage{}` - LaTeX packages
- `$` math mode - Use code blocks instead

## ✅ Validation Checklist

### 🔴 CRITICAL: Pre-Deployment Validation

**Before sending ANY files to PDF Forge, verify EVERY item:**

#### File Structure Requirements:
- [ ] Main document follows naming: `P2-[TYPE]-[STYLE].md`
- [ ] `request.json` exists and has required `"variables"` field
- [ ] No `.tex` files in package
- [ ] No `.lua` files UNLESS architecture phase includes Lua filters
- [ ] Assets folder named exactly `assets/` (not `images/` or other)
- [ ] NO SPACES in any filenames (use hyphens: `file-name.png`)

#### Request.json Structure:
- [ ] `"documents"` array wrapper (even for single document)
- [ ] Required `"variables"` field with title, subtitle, author, footer
- [ ] Template reference as `p2kb-[purpose]` (NO .latex extension)
- [ ] Options section with cleanup, archive, optimize settings
- [ ] NO `"pandoc_args"` with Lua filters UNLESS explicitly planned

#### Template Files (.sty validation):
- [ ] **ALL .sty files MUST start with `p2kb-`** (no exceptions)
- [ ] Template `.latex` file references correct `p2kb-` style files
- [ ] NO old naming: `iron-sheep-*`, `tutorial-manual`, `reference-manual`
- [ ] Foundation layer: `p2kb-foundation.sty`
- [ ] Content layer: `p2kb-[document-type]-content.sty`
- [ ] Presentation layer: `p2kb-[brand-status].sty`

#### Content Format:
- [ ] Special blocks use `::: blockname` format
- [ ] Code blocks use triple backticks
- [ ] LaTeX escaping applied if needed
- [ ] Image references use relative paths: `assets/image.png`

#### Architecture Phase Check:
- [ ] **Layered Template Phase**: NO Lua filters, focus on core stack
- [ ] **Enhancement Phase**: Lua filters allowed after core validation
- [ ] Current phase documented in deployment folder

### 🚨 COMMON FAILURE PATTERNS:

#### "Missing required field 'input'":
- **Cause**: Missing `"variables"` field in request.json
- **Fix**: Add variables section with title, subtitle, author, footer

#### "Package not found" errors:
- **Cause**: Non-p2kb .sty files or wrong template references
- **Fix**: Verify all .sty files start with `p2kb-`, update template references

#### "Could not fetch resource" for images:
- **Cause**: Spaces in image filenames or wrong asset folder name
- **Fix**: Rename files with hyphens, ensure `assets/` folder name

### 📝 Emergency Recovery Checklist:
If deployment fails:
1. **Check workspace/** for source files
2. **Verify file naming** against p2kb- standards
3. **Validate request.json** structure
4. **Confirm architecture phase** (Lua filters y/n)
5. **Re-run validation checklist** completely

## 🔄 Conversion Rules

If you have LaTeX content, convert it:

| LaTeX | Markdown |
|-------|----------|
| `\textbf{text}` | `**text**` |
| `\textit{text}` | `*text*` |
| `\texttt{code}` | `` `code` `` |
| `\section{Title}` | `## Title` |
| `\begin{lstlisting}` | `` ```pasm2 `` |
| `\begin{tcolorbox}` | `::: sidetrack` |

## 📚 File Naming Conventions Summary

### Documents (Markdown)
- **Lead with P2**: `P2-PASM-deSilva-Style.md`
- **Type clear**: PASM, Spin2, SmartPin, etc.
- **Style indicator**: deSilva-Style, Reference, Tutorial
- **Use hyphens**: Not underscores or spaces

### Templates (on PDF Forge)
- **Always prefix**: `p2kb-` for our templates
- **Purpose clear**: `p2kb-pasm-desilva`
- **Lowercase**: Template names are lowercase

### PDF Output
- **Match input**: `P2-PASM-deSilva-Style.pdf`
- **Version in metadata**: Not in filename (use request.json)

## 🚫 LaTeX Debugging Solutions

### Common "Missing $ inserted" Errors

**Problem**: Most common PDF generation failure
**Root Cause**: Pandoc math delimiter parsing issues

#### 🔴 CRITICAL Math Expression Rules
# LaTeX Character Escaping Rules for P2 Assembly

**Added**: 2025-08-21 after binary search debugging success  
**Source**: Perplexity comprehensive escaping guide  
**Success**: Fixed "Missing $ inserted" errors in P2 Assembly manual

## Essential LaTeX Escaping for P2 Assembly Code

**CRITICAL**: Assembly code contains many LaTeX special characters that MUST be escaped:

### Assembly Immediate Values - Escape `#` Characters
```
WRONG: mov value, ##1000000
RIGHT: mov value, \#\#1000000

WRONG: qsqrt value, #0  
RIGHT: qsqrt value, \#0
```

### Dollar Signs in Text - Escape `$`
```
WRONG: full circle = $1_0000_0000
RIGHT: full circle = \$1\_0000\_0000
```

### Underscores in Math/Text - Escape `_`
```
WRONG: $1_0000_0000
RIGHT: $1\_0000\_0000
```

### Carets for Exponents - Use `\^{}`
```
WRONG: e\^2 = 7.389
RIGHT: e\^{}2 = 7.389
```

## Complete LaTeX Special Character Reference

| Character | Escape As | Usage |
|-----------|-----------|-------|
| `#` | `\#` | Assembly immediate values |
| `$` | `\$` | Hex values, math mode delimiter |
| `%` | `\%` | Comments (rare in our content) |
| `&` | `\&` | Alignment (rare in our content) |
| `~` | `\textasciitilde{}` | Approximation symbol |
| `_` | `\_` | Underscores in identifiers |
| `^` | `\^{}` | Exponents, XOR operations |
| `\` | `\textbackslash{}` | Backslashes |
| `{` | `\{` | Literal braces |
| `}` | `\}` | Literal braces |

## Binary Search Debugging Success Story

**Problem**: Lines 3095-3188 causing "Missing $ inserted" error  
**Solution Process**:
1. Isolated 94 problematic lines through binary search
2. Applied systematic character escaping:
   - `$1_0000_0000` → `\$1\_0000\_0000`
   - `##1000000` → `\#\#1000000`
   - `e\^2` → `e\^{}2`
3. **Result**: PDF generation successful!

## Integration into Content Generation

**MANDATORY STEP**: When generating P2 assembly content:
1. Write content normally first
2. Apply systematic character escaping before PDF generation
3. Test problematic sections in isolation
4. Use binary search if issues persist

## 🔧 Automated LaTeX Escaping Script

### Production Script Location
**Script**: `/tools/latex-escape-all.sh`  
**Processor**: `/tools/latex_escape_processor.py`  
**Usage**: Final step before PDF generation

### How to Use
```bash
# From any directory:
cd /path/to/your/document/
/tools/latex-escape-all.sh input.md output-escaped.md

# Script automatically:
# - Creates backup of input file
# - Runs Python processor for intelligent escaping
# - Verifies output for remaining unescaped characters
# - Reports summary of escaping performed
```

### What the Script Does
- **Escapes** LaTeX special characters (#, $, %, &, _, ^, etc.)
- **Preserves** markdown headers (# Chapter stays as # Chapter)
- **Skips** code blocks (```pasm2 content untouched)
- **Handles** environments intelligently:
  - Template environments (sidetrack, interlude): content IS escaped
  - Standard LaTeX (equation, align): content NOT escaped

### Regression Testing
**Test Suite**: `/tools/latex-escaping-regression/`
```bash
# Run regression tests:
cd /tools/latex-escaping-regression/
./test-runner.sh

# If tests fail:
# 1. STOP - Don't proceed with PDF generation
# 2. Fix the issue in latex_escape_processor.py
# 3. Update test cases if needed
# 4. Verify tests pass
# 5. Resume PDF generation
```

### Emergency Protocol
If PDF generation fails with "Missing $ inserted" or similar:
1. **Check if escaping was run** - Most failures are from forgetting this step
2. **Isolate problem** - Use binary search on content
3. **Add to test cases** - New patterns go in `input/test-cases.md`
4. **Fix script** - Update processor to handle new pattern
5. **Update golden** - New expected output in `golden/test-cases-GOLDEN.md`

**Tools Available**:
- Automated escaping script with regression tests
- Content bisection for error isolation
- Test file generation (`test-XXXX-YYYY.md`)
- Incremental testing approach

## Green Book Visual Standards

### Overview
The Green Book (Tutorial) uses distinct visual treatment optimized for extended reading and learning.

### Implementation Files
- **Specifications**: `/exports/pdf-generation/workspace/smart-pins-manual/green-book-visual-specifications.md`
- **Lua Filter**: `green-book-semantic-blocks.lua`
- **Style Package**: `p2kb-smart-pins-content.sty` (extended for Green Book)

### Visual Features
1. **Semantic Markers** (7 types)
   - Full borders with title bars
   - Distinct border styles for accessibility
   - Pastel color palette for comfort

2. **Typography**
   - 10.5pt body text (5% larger than reference)
   - 1.25x line spacing
   - Digital-first margins (0.75" with 1" binding)

3. **Code Blocks**
   - Maintained pastel backgrounds
   - Left border only (distinct from semantic markers)
   - Three types: Configuration, Spin2, PASM2

### Filter Pipeline for Green Book
```json
"pandoc_args": [
    "--lua-filter=filters/smart-pins-colored-blocks.lua",
    "--lua-filter=filters/green-book-semantic-blocks.lua",
    "--lua-filter=filters/part-chapter-pagebreaks.lua"
]
```

**Order Critical**: Colored blocks → Semantic blocks → Page breaks

## Template Compatibility

This escaping works with:
- `p2kb-pasm-desilva.latex` template
- Pandoc → XeLaTeX → PDF pipeline
- tcolorbox colored environments
- Markdown code blocks (```pasm2)

**CRITICAL SUCCESS FACTOR**: Assembly code readability in PDF must match source fidelity while ensuring LaTeX compilation success.