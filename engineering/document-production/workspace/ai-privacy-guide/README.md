# AI Privacy Guide - Workspace Guide

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Quick Reference
**Canonical Name:** `ai-privacy-guide`
**Document Title:** AI Privacy Guide for P2 Developers
**Subtitle:** Claude Code Privacy Guidelines
**Outbound Deployment:** `/engineering/document-production/outbound/ai-privacy-guide/`
**Status:** DEFERRED (Not P2-related content)

## Document Purpose

Privacy guidelines for using Claude Code with P2 development work. Currently deferred as it's not directly related to P2 technical documentation.

## Related Folders

### This Workspace
- **Documents:**
  - `ai-privacy-guide.md`
  - `ai-implementation-strategy.md`
  - `claude-code-privacy-guide-for-p2-developers.md`
- **Templates:** `templates/` folder - See [templates/README.md](templates/README.md)
- **Request Config:** `request.json` (PDF generation configuration)

### Deployment Location
- **Outbound:** `/engineering/document-production/outbound/ai-privacy-guide/`

## Template Stack

**Prefix:** `p2kb-presentation-*`

```
Main: p2kb-presentation.latex (presentation-style template)
```

**Full Details:** See [templates/README.md](templates/README.md)

## Workflow Quick Start

### 1. Edit Content
Edit markdown files in this workspace

### 2. Prepare for PDF Generation (If Needed)
```bash
/workspaces/P2-Knowledge-Base/engineering/tools/latex-escape-all.sh \
    ai-privacy-guide.md \
    ../outbound/ai-privacy-guide/ai-privacy-guide.md
```

### 3. Copy Supporting Files
```bash
cp templates/*.latex ../outbound/ai-privacy-guide/
cp request.json ../outbound/ai-privacy-guide/
```

## Current Status

**Status:** Deferred - Not P2-related content
**Priority:** Low - Focus on P2 technical documentation first

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

This workspace contains AI/privacy content that's not directly related to P2 microcontroller documentation. Work on this document is deferred while P2 technical documentation takes priority.

If work resumes on this document, template can be enhanced based on presentation needs.
