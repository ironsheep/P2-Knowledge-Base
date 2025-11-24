# PASM2 Reference Manual - Workspace Guide

## Quick Reference
**Canonical Name:** `pasm2-reference-manual`
**Document Title:** PASM2 Reference Manual (TBD)
**Outbound Deployment:** `/engineering/document-production/outbound/pasm2-reference-manual/` (when ready)
**Status:** PLANNED - Early Stage

## Document Purpose

Comprehensive reference manual for PASM2 assembly language instruction set and programming model. Formal specifications and quick lookup optimized.

## Related Folders

### This Workspace
- **Templates:** `templates/` folder - See [templates/README.md](templates/README.md)
- **Production:** `production/` subfolder (staging area)
- **Status:** Minimal content

### Deployment Location
- **Outbound:** `/engineering/document-production/outbound/pasm2-reference-manual/` (to be created)

## Template Recommendations

**Document Type:** Formal Reference Manual

**Content Characteristics:**
- Instruction set documentation (all PASM2 instructions)
- Formal specifications and timing
- Flag behavior and side effects
- Register definitions
- Address modes
- Optimized for quick lookup

**Suggested Starting Points:**
- `p2kb-sp-*` templates - If technical reference approach desired
- `p2kb-desilva-*` templates - If approachable reference approach desired
- Custom minimal reference template - If formal spec style needed

**Key Decisions Needed:**
1. Formal vs. approachable tone?
2. Comprehensive vs. quick reference?
3. Coordinate with PASM deSilva Manual to avoid duplication

## Content Sources Available

### YAML Instruction Files
**Location:** `/engineering/knowledge-base/P2/language/pasm2/`
- Complete instruction set documentation
- Accurate timing and flag information
- Hardware operation details
- Recently updated with DEBUG and Smart Pin reset requirements

### Existing Content
- PASM deSilva Manual content (pedagogical - avoid duplication)
- Pattern extractions (code examples and idioms)

## Layout Considerations

### Reference Manual Needs
- Instruction tables (systematic organization)
- Flag status indicators (quick visual reference)
- Timing diagrams (cycle-accurate specifications)
- Cross-reference system (find related instructions)
- Comprehensive index (fast lookup)

## Workflow (When Ready)

### 1. Define Scope
Determine what distinguishes this from PASM deSilva Manual:
- Formal specifications vs. tutorial approach
- Complete instruction set vs. pedagogical selection
- Quick lookup vs. learning progression

### 2. Extract from YAML
Use YAML instruction files as authoritative source:
```bash
# YAML files contain formal specifications
/engineering/knowledge-base/P2/language/pasm2/*.yaml
```

### 3. Select Template
Choose template that matches reference manual style

### 4. Generate Content
Systematic extraction and formatting of instruction set

## Key Process Documents

### Universal Methodology
- **Format Guide:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`
- **Template Catalog:** `/engineering/document-production/TEMPLATE-CATALOG.md`

### Content Sources
- **YAML Instructions:** `/engineering/knowledge-base/P2/language/pasm2/`
- **PASM Manual:** Coordinate with `/workspace/p2-pasm-desilva-style/`

## Current Status

**Status:** Planned - Early Stage
**Priority:** Medium - Needed for complete P2 documentation suite

**Strategic Question:** How does this complement (not duplicate) PASM deSilva Manual?
- DeSilva: Tutorial, pedagogical, learning-focused
- This Manual: Reference, specifications, lookup-focused


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

This workspace will house the formal PASM2 reference manual. Template infrastructure is ready (foundation files available). Content strategy needs definition to avoid duplicating PASM deSilva Manual while providing value as formal reference.

Consider generating systematically from YAML sources for accuracy and completeness.
