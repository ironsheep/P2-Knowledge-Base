# Document Production Technical Debt

*Consolidated debt tracking for PDF generation, templates, and visual assets*

## Overview

This document tracks technical debt in the document production pipeline, including LaTeX templates, visual assets, PDF generation issues, and presentation layer problems.

## Template System Debt

### LaTeX Template Issues

#### Template Synchronization
- **Problem**: Multiple template versions across directories
- **Locations**: 
  - `/pdf-forge-workspace/templates/` (17 templates)
  - `/pipelines/templates/` (4 templates)  
  - `/exports/pdf-generation/workspace/manual-templates/` (23 templates)
  - Document-specific folders (scattered copies)
- **Impact**: HIGH - Changes don't propagate, confusion about authoritative version
- **Solution**: Single `/documentation/pdf-templates-master/` source

#### Naming Conventions
```
Current Issues:
  p2kb-foundation.sty vs p2kb-foundation-simple.sty
  p2kb-smart-pins.latex vs p2kb-smart-pins-simple.latex
  p2kb-smart-pins-pagebreak-test.latex (test file in production)
  
Needed:
  - Clear naming: p2kb-[document]-[layer].ext
  - No test files in production directories
  - Version control through git, not filenames
```

#### Layered Architecture Inconsistencies
```yaml
Foundation Layer Issues:
  - Some templates bypass foundation
  - Foundation features duplicated in content layer
  - Presentation layer mixed into content

Content Layer Issues:
  - Smart Pins content layer includes presentation
  - De Silva content layer has embedded colors
  - PASM2 content missing semantic structure

Presentation Layer Issues:
  - Tech review layer not used consistently
  - Iron Sheep branding incomplete
  - Color schemes vary between documents
```

### Lua Filter Coordination

#### Filter Duplication
```
Duplicate Filters Found:
  - div-to-environment.lua (3 versions)
  - smart-pins-auto-indent.lua (2 versions)
  - part-chapter-pagebreaks.lua (2 versions)

Issues:
  - Different behavior between versions
  - No clear versioning strategy
  - Manual copying between directories
```

#### Filter Dependencies
- Filters assume specific div syntax
- Order of filter application matters
- No documentation of filter requirements
- Filters break with pandoc updates

## Visual Assets Debt

### Missing Visual Elements

#### Timing Diagrams (Critical)
```
Smart Pins Timing Diagrams: 21 diagrams
  Location: Not extracted from PDF
  Status: Text descriptions only
  Impact: Cannot understand timing relationships
  
CORDIC Pipeline Diagrams: 8 diagrams
  Location: Never created
  Status: Text descriptions exist
  Impact: Pipeline scheduling unclear
  
State Machine Diagrams: 12 diagrams
  Location: In silicon docs, not extracted
  Status: Partial text descriptions
  Impact: Mode transitions unclear
```

#### Architecture Diagrams
- Hub/Cog interconnect (missing)
- Smart Pin internal structure (partial)
- Streamer data flow (missing)
- Event system connections (missing)

#### Instructional Diagrams  
- Bit field layouts (text only)
- Flag effects visualization (missing)
- Instruction encoding (tables only)
- Register organization (text only)

### Image Asset Management

#### Current Issues
```yaml
Storage Chaos:
  - Images in 15+ different directories
  - No naming convention
  - Mix of PNG, JPG, PDF formats
  - No source files for diagrams

Quality Issues:
  - Screenshots at wrong resolution
  - Diagrams not vector format
  - Inconsistent visual style
  - No dark mode versions

Workflow Issues:
  - No automated image optimization
  - Manual copying to documents
  - No version tracking for images
  - Lost source files for editing
```

#### Missing Standardization
- No image style guide
- No color palette definition
- No diagram templates
- No icon library

## PDF Generation Pipeline Debt

### PDF Forge System Issues

#### Environment Mismatches
```
Local vs PDF Forge:
  - Different pandoc versions
  - Missing LaTeX packages locally
  - Can't test templates locally
  - Debugging requires deployment
```

#### Request.json Complexity
```json
Issues with current approach:
  - Pandoc args duplicated everywhere
  - No validation of request files
  - Manual template path updates
  - No way to batch generate
```

### Build Process Debt

#### Manual Steps
1. Copy templates to document directory
2. Update request.json paths
3. Deploy to PDF Forge
4. Wait for generation
5. Download result
6. Check for issues
7. Repeat if needed

**Automation Needed**: Single command build and deploy

#### Quality Checks Missing
- No automated PDF validation
- No template syntax checking
- No image resolution verification
- No cross-reference validation

## Creation Guide Compliance Debt

### Visual Formatting Requirements
```
De Silva Manual Issues:
  - Sidetrack boxes: Specified dashed, got solid borders
  - Code blocks: Missing syntax highlighting
  - Info boxes: Wrong color scheme
  
Smart Pins Tutorial Issues:
  - Challenge boxes: Missing icons
  - Pin diagrams: Text instead of visual
  - Timing sections: No visual separation
```

### Structural Requirements
- Part/Chapter breaks not working correctly
- TOC depth inconsistent
- Index generation broken
- Page headers showing wrong content

## Metrics

| Category | Issues | Resolved | Remaining |
|----------|--------|----------|-----------|
| Template Sync | 45 | 12 | 33 |
| Visual Assets | 67 | 8 | 59 |
| PDF Pipeline | 23 | 5 | 18 |
| Creation Guides | 31 | 7 | 24 |
| Lua Filters | 12 | 2 | 10 |

## Priority Remediation

### 🔴 Critical (Blocks document generation)
1. Fix template synchronization chaos
2. Establish single source of truth
3. Fix part/chapter page breaks
4. Resolve Lua filter duplication

### 🟡 Major (Degrades quality)
1. Extract missing timing diagrams
2. Standardize visual asset management
3. Create image style guide
4. Fix creation guide compliance

### 🟢 Minor (Efficiency improvement)
1. Automate PDF pipeline
2. Create validation tests
3. Build template library
4. Document filter requirements

## Action Plan

### Immediate (This week)
1. Consolidate templates to single master location
2. Document current filter dependencies
3. Fix critical page break issues

### Short-term (Next sprint)
1. Extract Smart Pins timing diagrams manually
2. Create visual asset style guide
3. Build automated validation

### Long-term
1. Full PDF pipeline automation
2. Visual asset generation system
3. Template component library
4. Automated compliance checking

## Notes

- Template debt is blocking new document creation
- Visual debt severely impacts document quality
- PDF pipeline inefficiency slows iteration
- Creation guide violations reduce trust
- Focus on consolidation before enhancement

---
*Last Updated: 2025-08-31*
*Consolidated from: technical-debt/TEMPLATE-COORDINATION-DEBT.md, technical-debt/VISUAL-ASSETS-DEBT.md*