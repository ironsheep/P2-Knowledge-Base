# P2 Smart Pins Tutorial - Workspace Guide

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Quick Reference
**Canonical Name:** `p2-smart-pins-tutorial`
**Document Title:** P2 Smart Pins Complete Tutorial
**Subtitle:** Master Every Smart Pin Mode Through Progressive Learning
**Creation Guide:** `/engineering/document-production/manuals/p2-smart-pins-tutorial/creation-guide.md`
**Outbound Deployment:** `/engineering/document-production/outbound/p2-smart-pins-tutorial/`
**Status:** In Production - Technical Review Phase

## Document Identity

**Type:** Enhanced Tutorial Guide (Titus Remastered - "Green Book")
**Target Audience:** Anyone learning Smart Pins or implementing advanced features
**Size:** ~450 pages (comprehensive learning resource)
**Philosophy:** "Understand deeply, implement confidently"

## Related Folders

### This Workspace
- **Master Markdown:** `P2-Smart-Pins-Green-Book-Tutorial.md` (main working document)
- **Templates:** `templates/` folder - See [templates/README.md](templates/README.md)
- **Lua Filters:** `filters/` folder - Pandoc processing filters
- **Images/Screenshots:** `assets/` folder (21+ images)
- **Special Requirements:** `request-requirements.json` (--top-level-division=part)
- **Request Config:** `request.json` (PDF generation configuration)

### Creation and Style Guides
- **Creation Guide:** `/engineering/document-production/manuals/p2-smart-pins-tutorial/creation-guide.md`
- **Content Guide:** `/engineering/document-production/manuals/p2-smart-pins-tutorial/content-guide.md`
- **Presentation Style:** `/engineering/document-production/manuals/p2-smart-pins-tutorial/presentation-style-guide.md`
- **Style Guide:** `/engineering/document-production/manuals/p2-smart-pins-tutorial/style-guide.md`

### Deployment Location
- **Outbound:** `/engineering/document-production/outbound/p2-smart-pins-tutorial/`
- **Process:** Files copied here after LaTeX escaping, ready for PDF Forge

## Template Stack

**Prefix:** `p2kb-sp-*`

```
Layer 1: p2kb-foundation.sty (core infrastructure)
    ↓
Layer 2: p2kb-sp-styles.sty (Smart Pins content styling)
    ↓
Layer 3: p2kb-sp-numbering.sty (numbering system)
    ↓
Layer 4: p2kb-tech-review.sty (presentation branding)
    ↓
Main: p2kb-sp-template.latex (orchestrates all layers)
```

**Full Details:** See [templates/README.md](templates/README.md)

## Special Requirements

### Pandoc Arguments (CRITICAL!)
This document REQUIRES special pandoc arguments:
```json
{
  "required_pandoc_args": ["--top-level-division=part"]
}
```

**Why:** Document uses Part/Chapter structure. Without this argument, page breaks fail.
**Documented In:** `request-requirements.json` in this workspace

### Lua Filter Pipeline
Filters must be applied in this exact order:
1. `smart-pins-colored-blocks.lua` - Code block coloring
2. `green-book-semantic-blocks.lua` - Semantic marker conversion
3. `part-chapter-pagebreaks.lua` - Page break management

**Order Critical:** Each filter depends on previous filter's output

### Assets Folder
- **Location:** `assets/` subfolder in this workspace
- **Contents:** 21+ PNG images (Smart Pins diagrams and examples)
- **Naming:** NO SPACES in filenames (use hyphens: `Smart-Pins-Mode-01.png`)
- **References:** Use relative paths in markdown: `![Caption](assets/image.png)`

## Workflow Quick Start

### 1. Edit Content
Edit `P2-Smart-Pins-Green-Book-Tutorial.md` in this workspace

### 2. Prepare for PDF Generation
```bash
# From workspace directory:
/workspaces/P2-Knowledge-Base/engineering/tools/latex-escape-all.sh \
    P2-Smart-Pins-Green-Book-Tutorial.md \
    /workspaces/P2-Knowledge-Base/engineering/document-production/outbound/p2-smart-pins-tutorial/P2-Smart-Pins-Green-Book-Tutorial.md
```

### 3. Copy Supporting Files
```bash
# Copy templates if changed
cp templates/*.{latex,sty} ../outbound/p2-smart-pins-tutorial/

# Copy Lua filters if changed
cp -r filters ../outbound/p2-smart-pins-tutorial/

# Copy assets folder
cp -r assets ../outbound/p2-smart-pins-tutorial/

# Ensure request.json is present
cp request.json ../outbound/p2-smart-pins-tutorial/
```

### 4. User Deploys to PDF Forge
User manually moves files from outbound to PDF Forge system

## Key Process Documents

### Universal Methodology
- **Format Guide:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`

### Document-Specific
- **Creation Guide:** `/engineering/document-production/manuals/p2-smart-pins-tutorial/creation-guide.md` (voice, philosophy, content sources)
- **Green Book Processing:** `green-book-processing-guide.md` (in this workspace)
- **Markdown Changes:** `green-book-markdown-changes-guide.md` (in this workspace)

## Visual Features

### Semantic Markers (7 types)
- Full borders with title bars
- Distinct border styles (solid, dashed, dotted) for accessibility
- Pastel color palette optimized for extended reading

### Code Block System (3 types)
- **Configuration:** Pin setup and mode selection (light blue)
- **Spin2:** High-level programming examples (light green)
- **PASM2:** Assembly language examples (light yellow)

### Typography
- 10.5pt body text (5% larger than reference manual)
- 1.25x line spacing for comfortable reading
- Digital-first margins (0.75" with 1" binding)

## Current Status

**Phase:** Technical Review
**Completion:** Content complete, visual refinement ongoing
**Next Steps:**
- Iterate on visual presentation based on PDF output
- Refine semantic marker styling
- Complete code example validation
- Prepare for technical review submission

## PDF Forge Integration

### Testing (Template Development & Visual Refinement)
**Guide:** `/engineering/pdf-forge/work-modes/automated-pdf-testing.md`
- Rapid iteration for template fixes and visual refinement (30-60 sec cycles)
- Test multiple scenarios in one request
- Temporary testing - does NOT install templates permanently

### Production (Final Deliverable Generation)
**Guide:** `/engineering/pdf-forge/work-modes/production-pdf-generation.md`
- Create deliverable PDFs for distribution
- **CRITICAL:** Only copy CHANGED files to outbound (request.json + .md always, templates/filters only if modified)
- Templates and filters persist on PDF Forge - don't resend unchanged files

**Complete Rules:** `/engineering/pdf-forge/PRODUCTION-PROCESS-RULES.md` (🚨 "only changed files" details)

## Notes

This workspace maintains the "Green Book" (tutorial) variant of Smart Pins documentation. The companion "Blue Book" (quick reference) is a separate document.

**Two-Book Strategy:**
- Green Book (this): ~450 pages, comprehensive tutorial
- Blue Book (separate): ~230 pages, quick reference
