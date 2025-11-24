# P2 Single-Step Debugger Manual - Workspace Guide

## Quick Reference
**Canonical Name:** `p2-single-step-debugger-manual`
**Document Title:** P2 Single-Step Debugger Manual (TBD)
**Outbound Deployment:** `/engineering/document-production/outbound/p2-single-step-debugger-manual/` (when created)
**Status:** PLANNED - Not Started

## Document Purpose

Documentation for P2's single-step debugger functionality. Early planning stage - no content yet.

## Related Folders

### This Workspace
- **Templates:** `templates/` folder - See [templates/README.md](templates/README.md)
- **Status:** No content files yet

### Deployment Location
- **Outbound:** `/engineering/document-production/outbound/p2-single-step-debugger-manual/` (to be created)

## Template Recommendations

**Next Steps:**
1. Determine document style:
   - Tutorial/pedagogical (like deSilva)?
   - Visual discovery (like Debug Window)?
   - Quick reference (like Smart Pins Blue Book)?
2. Survey existing templates in Template Catalog
3. Copy closest match to this workspace
4. Rename with `p2kb-debugger-*` prefix
5. Customize for debugger content

**Suggested Starting Points:**
- `p2kb-debugwin-*` - If visual/discovery approach desired
- `p2kb-desilva-*` - If tutorial/pedagogical approach desired
- `p2kb-sp-*` - If reference manual approach desired

## Workflow (When Ready)

### 1. Create Content
Create main markdown document in this workspace

### 2. Select/Customize Template
Choose and customize template from existing documents

### 3. Follow Standard Process
Use standard PDF generation workflow once content exists

## Key Process Documents

### Universal Methodology
- **Format Guide:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`
- **Template Catalog:** `/engineering/document-production/TEMPLATE-CATALOG.md`

## Current Status

**Status:** Planned - Not Started
**Priority:** TBD based on P2 community needs


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

This workspace is a placeholder for future single-step debugger documentation. Template infrastructure is ready (foundation files available), but content development has not begun.

Coordinate with Debug Window manual to avoid overlap and ensure complementary coverage.
