# Spin2 Reference Manual - Workspace Guide

## Quick Reference
**Canonical Name:** `spin2-reference-manual`
**Document Title:** Spin2 Reference Manual (TBD)
**Outbound Deployment:** `/engineering/document-production/outbound/spin2-reference-manual/` (when ready)
**Status:** PLANNED - Early Stage

## Document Purpose

Comprehensive reference manual for Spin2 high-level language, covering syntax, semantics, built-in functions, object-oriented features, and inline PASM2 integration.

## Related Folders

### This Workspace
- **Templates:** `templates/` folder - See [templates/README.md](templates/README.md)
- **Production:** `production/` subfolder (staging area)
- **Status:** Minimal content

### Deployment Location
- **Outbound:** `/engineering/document-production/outbound/spin2-reference-manual/` (to be created)

## Template Recommendations

**Document Type:** Language Reference Manual

**Content Characteristics:**
- Language syntax and semantics
- Built-in functions and operators
- Object-oriented features (objects, methods, properties)
- Inline PASM2 integration
- Standard library documentation
- Code examples (Spin2 and mixed Spin2/PASM2)

**Suggested Starting Points:**
- `p2kb-sp-*` templates - If technical reference approach desired
- `p2kb-desilva-*` templates - If approachable reference approach desired
- Coordinate with PASM2 Reference for consistency if both are formal

**Key Decisions Needed:**
1. Formal language specification vs. practical reference?
2. Target audience: beginners vs. experienced programmers?
3. Cross-referencing strategy with PASM2 manual

## Content Sources Available

### YAML Language Files (If Available)
**Location:** `/engineering/knowledge-base/P2/language/spin2/` (check availability)

### Existing Content
- Spin2 extractions from previous work
- Pattern examples showing Spin2/PASM2 integration
- Object-oriented usage patterns

## Layout Considerations

### Language Reference Needs
- Syntax diagrams or clear syntax descriptions
- Function reference tables (organized by category)
- Code examples for every language feature
- Cross-references between related concepts
- Index optimized for language lookup
- Inline PASM2 integration examples

### Unique Spin2 Features
- Object-oriented programming (OOP) in Spin2
- COG/LUT memory management
- Smart Pin integration from Spin2
- DEBUG() statement usage
- Seamless PASM2 inline assembly

## Workflow (When Ready)

### 1. Define Scope
Determine reference manual approach:
- Language specification formality level
- Integration with PASM2 manual
- Standard library coverage depth
- Example code density

### 2. Gather Content
Extract and organize:
- Language syntax rules
- Built-in function documentation
- OOP feature descriptions
- PASM2 integration patterns

### 3. Select Template
Choose template matching reference style (coordinate with PASM2 Reference if both formal)

### 4. Generate Content
Systematic documentation of language features

## Key Process Documents

### Universal Methodology
- **Format Guide:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`
- **Template Catalog:** `/engineering/document-production/TEMPLATE-CATALOG.md`

### Content Coordination
- **PASM2 Reference:** `/workspace/pasm2-reference-manual/` - Coordinate inline assembly coverage
- **PASM DeSilva:** `/workspace/p2-pasm-desilva-style/` - Coordinate Spin2/PASM2 examples

## Current Status

**Status:** Planned - Early Stage
**Priority:** Medium-High - Important for complete P2 documentation suite

**Strategic Questions:**
- How formal should language specification be?
- How to handle Spin2/PASM2 boundary?
- Coordinate visual style with PASM2 Reference?


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

This workspace will house the Spin2 language reference manual. Template infrastructure is ready (foundation files available). Content strategy needs definition.

**Key Differentiator:** Spin2 is the high-level language, PASM2 is the assembly language. This manual should emphasize:
- Language-level abstractions
- Object-oriented features unique to Spin2
- How to effectively use inline PASM2
- When to use Spin2 vs. drop to PASM2

Consider generating systematically from language specification sources for accuracy.
