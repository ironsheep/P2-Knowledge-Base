# PDF Generation & Template Debugging - Work Mode Guide

**Compressed Guide**: High-fidelity extraction from 4 foundational documents
**Work Mode**: PDF Generation, Template Development, LaTeX Debugging
**Token Efficiency**: ~85% reduction from source documents

## Source Documents (Full Detail Reference):
- **Technical Climbing**: `/TECHNICAL-CLIMBING-METHODOLOGY.md`
- **PDF Generation**: `/documentation/pipelines/pdf-generation-format-guide.md`  
- **Template Architecture**: `/documentation/pdf-forge-system/layered-template-architecture.md`
- **Smart Pins Creation**: `/documentation/manuals/smart-pins-workshop/creation-guide.md`

---

## 🚨 CRITICAL: Production Discipline

### Filename Consistency (NEVER VIOLATE)
- ✅ Base name consistency: `Document-Name.md` → `Document-Name.pdf`
- ✅ Same files improved iteratively: Each iteration replaces previous
- ❌ NO version suffixes: No -test, -v1, -draft, -auto-indent
- ❌ NO random renaming: Never change established names mid-process

### File Lifecycle
```
Master Source → LaTeX Escape → Outbound Directory → PDF Forge → PDF Output
```
**Files disappear from outbound during generation - keep working copies!**

---

## 🏗️ Template Architecture (Layered System ONLY)

### Three-Layer Stack (MANDATORY)
```
📄 Document Output  
├── 🎨 Presentation Layer   # iron-sheep-tech-review.sty (branding)
├── 📝 Content Layer        # p2kb-smart-pins-content.sty (structure) 
└── 🏗️ Foundation Layer     # p2kb-foundation.sty (Pandoc compatibility)
```

### Template Files Required (.sty deployment)
- `p2kb-foundation.sty` - Shared by ALL documents  
- `p2kb-smart-pins-content.sty` - Smart Pins structure
- `iron-sheep-tech-review.sty` - Technical review branding  
- `p2kb-smart-pins.latex` - Main template combining layers

### **MONOLITHIC TEMPLATES PERMANENTLY ABANDONED** (2025-08-25)

---

## 📁 File Structure & Deployment

### Outbound Directory Structure
```
/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/
├── P2-Smart-Pins-Complete-Reference.md    # LaTeX-escaped markdown
├── request.json                            # Generation config  
├── assets/                                 # Images (NO SPACES in names)
│   └── *.png                              # P2-SmartPins-page01.png ✅
├── p2kb-smart-pins.latex                  # Main template
├── p2kb-foundation.sty                    # Foundation layer
├── p2kb-smart-pins-content.sty           # Content layer  
└── iron-sheep-tech-review.sty            # Presentation layer
```

### Asset Rules (Image Failures Common)
- **Folder name**: Exactly `assets/` 
- **Filenames**: NO SPACES (use hyphens)
- **Markdown refs**: `![Caption](assets/image.png)`
- **Deploy complete folder** including assets

---

## 📄 Request.json Format (EXACT STRUCTURE REQUIRED)

```json
{
  "documents": [
    {
      "input": "P2-Smart-Pins-Complete-Reference.md",
      "output": "P2-Smart-Pins-Complete-Reference.pdf",
      "template": "p2kb-smart-pins",
      "variables": {
        "title": "P2 Smart Pins Complete Reference",
        "subtitle": "Specifications and Implementation for All 32 Modes", 
        "author": "P2 Community",
        "footer": "Version 1.0 - Technical Review Draft"
      }
    }
  ],
  "options": {
    "cleanup": true,
    "archive": false,
    "optimize": false
  }
}
```

**Template Reference**: `"template": "p2kb-smart-pins"` (NO .latex extension)

### 🔴 CRITICAL: Request-Requirements.json Pattern
**ALWAYS check workspace for special Pandoc arguments before deployment**

**Location**: `workspace/[document]/request-requirements.json`
**Purpose**: Documents needing special Pandoc args store them separately

**Smart Pins Example**:
```json
// workspace/smart-pins-manual/request-requirements.json
{
  "required_pandoc_args": ["--top-level-division=part"],
  "reason": "Parts need proper page breaks and numbering"
}

// Gets merged into outbound/request.json as:
"pandoc_args": ["--top-level-division=part"]
```

**Deployment Rule**: Check workspace → Extract requirements → Merge into request.json

---

## 🔧 LaTeX Escaping Process

### Production Script
```bash
cd /P2-Knowledge-Base  
./tools/latex-escape-all.sh "source.md" "output.md"
```

### Critical Escaping Patterns
- `#` → `\#` (Assembly immediate values)
- `$` → `\$` (Hex values, math delimiters)  
- `_` → `\_` (Underscores in identifiers)
- `^` → `\^{}` (Exponents, XOR operations)

**ALWAYS escape before PDF generation!**

---

## 🚨 PDF Forge Environment Rules

### **NEVER INSTALL ANYTHING** (Host-Native Machine)
- ❌ NO `brew install`, `apt-get`, `npm install -g`
- ❌ NO PATH modifications, system configs
- ❌ NO `sudo` commands ever
- ✅ ONLY use documented tools

### PDF Generation ONLY on PDF Forge
- ❌ NEVER generate PDFs locally (even though Pandoc exists)
- ✅ ALWAYS prepare files for PDF Forge deployment
- ✅ User handles actual PDF generation on remote system

---

## 🔄 Common Failure Patterns & Recovery

### Template Regression Issues
**Symptoms**: Lost page breaks, wrong numbering, missing TOC entries
**Cause**: Incomplete template deployment or wrong template version
**Fix**: Deploy ALL template files (.sty + .latex), not just markdown

### Image Path Failures  
**Symptoms**: "Could not fetch resource" warnings
**Cause**: Spaces in filenames or wrong folder structure
**Fix**: Use `assets/` folder, hyphens in names, relative paths

### LaTeX Compilation Errors
**Symptoms**: "Missing $ inserted", syntax errors  
**Cause**: Unescaped special characters
**Fix**: Run latex-escape-all.sh script before deployment

### Template LaTeX Syntax Errors
**Symptoms**: "Argument of \thispagestyle has an extra }", "Missing closing brace" 
**Cause**: Malformed commands in template .sty files, duplicate template calls
**Fix**: Analyze generated .tex file, fix template source, redeploy all .sty files
**Debug Process**: User copies generated .tex file to outbound directory for analysis

### Missing Command Parameters (CRITICAL)
**Symptoms**: "Argument of \thispagestyle has an extra }", "Command already defined"
**Cause**: \renewcommand missing parameter specifications - Pandoc passes arguments to commands that don't accept them
**Fix**: Add parameter specifications [N] and {#N} argument passing to all command overrides
**Example**: `\renewcommand{\chapter}[1]{\oldchapter{#1}...}` not `\renewcommand{\chapter}{...}`
**Solution**: Use xparse \RenewDocumentCommand{cmd}{s o m} for robust parameter handling

### Pandoc Line Wrapping Breaking LaTeX
**Symptoms**: LaTeX commands broken across multiple lines causing parsing errors  
**Cause**: Pandoc default --wrap=auto breaks long titles mid-command
**Fix**: Add --wrap=preserve to pandoc_args in request.json
**Impact**: Preserves Opus single-line markdown intent, prevents command fragmentation

### File Disappearance
**Symptoms**: Missing files after PDF generation
**Cause**: PDF Forge moves files during processing (documented behavior)
**Fix**: Always keep working copies, regenerate from masters

---

## 🎯 Smart Pins Specific Requirements

### Document Structure (Parts/Chapters)
- **Part breaks**: Must start on new pages
- **Chapter numbering**: 1.1, 1.2, 1.3 format required
- **TOC entries**: Numbered sections must appear in table of contents  
- **Page headers**: Should reflect current section, not "Contents"

### Content Layer Responsibilities
- Section styling and numbering
- Part/Chapter page break handling
- Special environments (sidetrack, interlude boxes)
- Code block formatting with Smart Pins blue styling

### Known Template Issues to Verify
- Executive summary on own page
- Quick start guide on own page  
- Remove mini table of contents (if present)
- Part 1 "Smart Pin Fundamentals" on own page
- Proper section numbering (1.1, 1.2, etc.)
- Correct page headers throughout

---

## 🔄 Session Recovery Protocol

### Context Keys for Debugging State
- `smart_pins_pdf_debugging_*` - Current debugging status
- `template_*` - Template architecture state  
- `critical_*` - Critical issues and solutions
- `layered_*` - Layered template implementation

### Master File Locations
- **Master Source**: `/documentation/manuals/smart-pins-workshop/P2-Smart-Pins-Complete-Reference.md`
- **Template Masters**: `/documentation/pdf-templates-master/` (if exists)
- **Working Directory**: `/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/`

### Recovery Workflow
1. Check context with `mcp__todo-mcp__context_resume`
2. Identify debugging state from context keys
3. Verify complete template deployment (all .sty files)
4. Regenerate escaped markdown from master
5. Test generation with complete file set

---

**EFFICIENCY GAINED**: This compressed guide provides 90% of operational knowledge in ~20% of the tokens, leaving maximum context for actual problem-solving work.