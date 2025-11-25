# P2 Debug Window Manual - Workspace Guide

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Quick Reference
**Canonical Name:** `p2-debug-window-manual`
**Document Title:** P2 Debug Window Manual
**Subtitle:** Visual Discovery Through Systematic Exploration
**Creation Guide:** `/engineering/document-production/manuals/p2-debug-window-manual/creation-guide.md`
**Outbound Deployment:** `/engineering/document-production/outbound/p2-debug-window-manual/`
**Status:** In Production - Visual Refinement Phase

## Document Purpose

Comprehensive manual for P2's DEBUG() system covering all 9 window types through discovery-driven exploration with visual verification.

**Philosophy:** "Show, don't just tell" - Every feature proven with screenshots

## Related Folders

### This Workspace
- **Master Markdown:** `P2-Debug-Window-Manual.md` (main working document)
- **Templates:** `templates/` folder - See [templates/README.md](templates/README.md)
- **Lua Filters:** `filters/` folder - Pandoc processing filters
- **Request Config:** `request.json` (PDF generation configuration)
- **Development Notes:**
  - `debug-window-markdown-changes-guide.md` - Change tracking
  - `template-development-plan.md` - Template evolution notes
  - `fix-*.py` - Content processing scripts

### Creation Guide
- **Creation Guide:** `/engineering/document-production/manuals/p2-debug-window-manual/creation-guide.md`

### Deployment Location
- **Outbound:** `/engineering/document-production/outbound/p2-debug-window-manual/`
- **Process:** Files copied here after LaTeX escaping, ready for PDF Forge

## Template Stack

**Prefix:** `p2kb-debugwin-*`

```
Layer 1: p2kb-debugwin-foundation.sty (debug window-specific foundation)
    ↓
Layer 2: p2kb-debugwin-content.sty (5-color code + visual discovery elements)
    ↓
Main: p2kb-debugwin.latex (custom title page + list of figures)
```

**Full Details:** See [templates/README.md](templates/README.md)

## Window Types Covered

1. **Terminal** - Text output and logging
2. **Bitmap** - Graphics and image display
3. **Plot** - Data visualization and charting
4. **Scope** - Waveform display
5. **Logic** - Digital signal analysis
6. **FFT** - Frequency analysis
7. **Spectro** - Spectrogram visualization
8. **Scope_XY** - X-Y plotting
9. **Mixed** - Combination windows

## Visual Discovery Philosophy

### Teaching Approach
- **Visual First:** Every feature shown with screenshot
- **Systematic Exploration:** Methodical coverage of all capabilities
- **Hands-On Discovery:** "Try this experiment" prompts throughout
- **Performance Metrics:** Real measurements, not just specs

### Content Structure
- **Discovery Boxes:** Experiment prompts and exploration suggestions
- **Screenshots:** Visual proof of every feature (requires assets/)
- **Comparison Tables:** Quick reference between window types
- **Code Examples:** Complete DEBUG() statement examples

## Workflow Quick Start

### 1. Edit Content
Edit `P2-Debug-Window-Manual.md` in this workspace

### 2. Process Screenshots (If Updated)
```bash
# Convert/prepare screenshots if needed
python3 convert-debug-window-images.py
```

### 3. Fix Unicode/Structure (If Needed)
```bash
# Fix unicode characters
python3 fix-unicode-characters.py P2-Debug-Window-Manual.md

# Fix document structure
python3 fix-document-structure.py P2-Debug-Window-Manual.md
```

### 4. Prepare for PDF Generation
```bash
# From workspace directory:
/workspaces/P2-Knowledge-Base/engineering/tools/latex-escape-all.sh \
    P2-Debug-Window-Manual.md \
    /workspaces/P2-Knowledge-Base/engineering/document-production/outbound/p2-debug-window-manual/P2-Debug-Window-Manual.md
```

### 5. Copy Supporting Files
```bash
# Copy templates if changed
cp templates/*.{latex,sty} ../outbound/p2-debug-window-manual/

# Copy Lua filters if changed (if applicable)
cp -r filters ../outbound/p2-debug-window-manual/

# Copy screenshots/assets if present
cp -r assets ../outbound/p2-debug-window-manual/

# Ensure request.json is present
cp request.json ../outbound/p2-debug-window-manual/
```

### 6. User Deploys to PDF Forge
User manually moves files from outbound to PDF Forge system

## Key Process Documents

### Universal Methodology
- **Format Guide:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`

### Document-Specific
- **Creation Guide:** `/engineering/document-production/manuals/p2-debug-window-manual/creation-guide.md`
- **Markdown Changes:** `debug-window-markdown-changes-guide.md` (in this workspace)
- **Template Development:** `template-development-plan.md` (in this workspace)

## Visual Elements

### 5-Color Code System (Adapted)
Similar to deSilva approach but optimized for debug contexts:
- DEBUG statement highlighting
- Window type differentiation
- Discovery vs. reference code marking

### Screenshot Requirements
- **Location:** `assets/` folder (to be created if not present)
- **Format:** PNG preferred for clarity
- **Naming:** NO SPACES (use hyphens: `Terminal-Window-Example.png`)
- **References:** Use markdown: `![Caption](assets/screenshot.png)`

### List of Figures
Template automatically generates "List of Figures" from all image references for easy navigation to specific screenshots.

## Content Processing Scripts

### Available Tools
- `convert-debug-window-images.py` - Image conversion/preparation
- `fix-unicode-characters.py` - Unicode character normalization
- `fix-document-structure.py` - Document structure corrections

**Purpose:** These scripts handle content transformation specific to debug window documentation.

## Current Status

**Phase:** Visual Refinement
**Progress:**
- Complete content with 14 chapters + 5 appendices
- All 9 window types documented
- 200+ code examples included
- Screenshot integration in progress

**Next Steps:**
- Complete screenshot collection for all features
- Verify all DEBUG() examples work on P2 hardware
- Refine visual layout based on PDF output
- Prepare for Technical Review

## Document Statistics

- **Total Chapters:** 14 (Complete Manual)
- **Appendices:** 5 (Command Reference, Examples, Performance)
- **Window Types:** 9 (Full coverage)
- **Code Examples:** 200+ (DEBUG statements and programs)
- **Learning Style:** Discovery-driven exploration

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

This manual documents discoveries made through systematic exploration of P2's debug window system. Every capability shown has been (or will be) verified with actual hardware and includes visual proof via screenshots.
