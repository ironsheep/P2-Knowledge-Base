# [Document Name] - Workspace Guide

**Template Version:** 1.0
**Instructions:** Replace all [BRACKETED] placeholders with document-specific information. Delete instruction sections when complete.

---

## Quick Reference
**Canonical Name:** `[document-folder-name]`
**Document Title:** [Full Document Title]
**Subtitle:** [Document Subtitle]
**Creation Guide:** `/engineering/document-production/manuals/[document-name]/creation-guide.md` [if exists]
**Outbound Deployment:** `/engineering/document-production/outbound/[document-name]/`
**Status:** [In Production | Planned | Technical Review | etc.]

## Document Purpose

[1-2 paragraph description of what this document is and why it exists. Include target audience and key differentiators from other documents.]

**[Optional: Teaching Philosophy/Approach]:** ["Quote or brief statement of document's philosophical approach"]

## Related Folders

### This Workspace
- **Master Markdown:** `[Primary-Document-Name].md` (main working document)
- **Templates:** `templates/` folder - See [templates/README.md](templates/README.md)
- **[Optional: Lua Filters]:** `filters/` folder - Pandoc processing filters
- **[Optional: Images/Assets]:** `assets/` folder ([N] images/screenshots)
- **[Optional: Special Requirements]:** `request-requirements.json` (special pandoc args if needed)
- **Request Config:** `request.json` (PDF generation configuration)
- **[Optional: Other Files]:**
  - `[file-name].md` - [Description]
  - `[script-name].py` - [Description]

### Creation and Style Guides
**[Delete this section if no creation guides exist yet]**
- **Creation Guide:** `/engineering/document-production/manuals/[document-name]/creation-guide.md`
- **[Optional: Style Guide]:** `/engineering/document-production/manuals/[document-name]/style-guide.md`
- **[Optional: Content Guide]:** `/engineering/document-production/manuals/[document-name]/content-guide.md`

### Deployment Location
- **Outbound:** `/engineering/document-production/outbound/[document-name]/`
- **Process:** Files copied here after LaTeX escaping, ready for PDF Forge

## Template Stack

**Prefix:** `p2kb-[identifier]-*`

```
[Document template hierarchy - copy from templates/README.md]

Example for 4-layer stack:
Layer 1: p2kb-[id]-foundation.sty (core infrastructure)
    ↓
Layer 2: p2kb-[id]-content.sty (content styling)
    ↓
Layer 3: p2kb-[id]-numbering.sty (numbering system)
    ↓
Layer 4: p2kb-[id]-presentation.sty (presentation branding)
    ↓
Main: p2kb-[id]-template.latex (orchestrates all layers)

Example for 2-layer stack:
Layer 1: p2kb-[id]-foundation.sty (foundation)
    ↓
Layer 2: p2kb-[id]-content.sty (content styling)
    ↓
Main: p2kb-[id].latex (main template)
```

**Full Details:** See [templates/README.md](templates/README.md)

## Special Requirements

**[Delete this entire section if no special requirements exist]**

### Pandoc Arguments (If Applicable)
[If document requires special pandoc arguments:]
```json
{
  "required_pandoc_args": ["--top-level-division=part"]
}
```

**Why:** [Explanation of why this argument is needed]
**Documented In:** `request-requirements.json` in this workspace

### Lua Filter Pipeline (If Applicable)
[If document uses Lua filters, list them in order:]
Filters must be applied in this exact order:
1. `[filter-name-1].lua` - [Description]
2. `[filter-name-2].lua` - [Description]
3. `[filter-name-3].lua` - [Description]

**Order Critical:** Each filter depends on previous filter's output

### Assets Folder (If Applicable)
- **Location:** `assets/` subfolder in this workspace
- **Contents:** [N] [PNG/image type] images ([description])
- **Naming:** NO SPACES in filenames (use hyphens: `Image-Name-01.png`)
- **References:** Use relative paths in markdown: `![Caption](assets/image.png)`

## Content Sources & Production Method

**[Optional section - include if document has specific content sources]**

### Primary Sources
1. **[Source Name]** - `[location]` - [Description/purpose]
2. **[Source Name]** - `[location]` - [Description/purpose]

### [Optional: Document Strategy]
[If document follows specific strategy like modular approach, coordinated references, etc.]

## Workflow Quick Start

### 1. Edit Content
Edit `[Primary-Document-Name].md` in this workspace

### 2. [Optional: Additional Processing Steps]
**[Include if document needs special processing before LaTeX escaping]**
```bash
# Example: Process screenshots, run conversion scripts, etc.
[command]
```

### 3. Prepare for PDF Generation
```bash
# From workspace directory:
/workspaces/P2-Knowledge-Base/engineering/tools/latex-escape-all.sh \
    [Source-Document].md \
    /workspaces/P2-Knowledge-Base/engineering/document-production/outbound/[document-name]/[Output-Document].md
```

### 4. Copy Supporting Files
```bash
# Copy templates if changed
cp templates/*.{latex,sty} ../outbound/[document-name]/

# [Optional: Copy Lua filters if changed]
cp -r filters ../outbound/[document-name]/

# [Optional: Copy assets folder]
cp -r assets ../outbound/[document-name]/

# Ensure request.json is present
cp request.json ../outbound/[document-name]/
```

### 5. User Deploys to PDF Forge
User manually moves files from outbound to PDF Forge system

## Key Process Documents

### Universal Methodology
- **Format Guide:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`
- **Template Catalog:** `/engineering/document-production/TEMPLATE-CATALOG.md`

### Document-Specific
**[Delete section if no document-specific guides exist yet]**
- **Creation Guide:** `/engineering/document-production/manuals/[document-name]/creation-guide.md` [if exists]
- **[Optional: Specific guides in workspace]:** `[guide-name].md` (in this workspace)

## [Optional: Visual Features / Special Content Elements]

**[Include this section if document has distinctive visual features worth highlighting]**

### [Feature Category 1]
[Description of visual/content features]

### [Feature Category 2]
[Description]

## Current Status

**Phase:** [Technical Review | Content Development | Planning | etc.]
**[Optional: Completion]:** [Description of current progress]
**Next Steps:**
- [Step 1]
- [Step 2]
- [Step 3]

## [Optional: Document-Specific Tools/Scripts]

**[Include if workspace has custom processing scripts]**

### Available Tools
- `[script-name].py` - [Description]
- `[script-name].sh` - [Description]

**Purpose:** [Why these scripts exist]

## Notes

[Any additional context, strategic considerations, coordination with other documents, or important reminders specific to this document]

**[Optional: Document Strategy/Philosophy]:** [Any unique approaches or considerations]

---

## Template Usage Instructions

**When creating a new workspace README:**

1. **Copy this template** to new workspace:
   ```bash
   cp /engineering/document-production/methodology/workspace-README-template.md \
      /engineering/document-production/workspace/[new-doc]/README.md
   ```

2. **Replace all [BRACKETED] placeholders** with document-specific information

3. **Delete optional sections** that don't apply to your document:
   - Lua Filters (if no filters)
   - Assets Folder (if no images)
   - Special Requirements (if none)
   - Content Sources (if standard)
   - Visual Features (if standard)
   - Document-Specific Tools (if none)

4. **Delete this instruction section** when complete

5. **Customize as needed** - This template provides structure, not constraints

**Core sections to always include:**
- Quick Reference
- Document Purpose
- Related Folders
- Template Stack (link to templates/README.md)
- Workflow Quick Start
- Key Process Documents
- Current Status
- Notes
