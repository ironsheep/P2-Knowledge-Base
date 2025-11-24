# P2 Smart Pins Tutorial - Template Documentation

## Template Prefix
**Prefix:** `p2kb-sp-*`
**Purpose:** Smart Pins tutorial and reference documentation

## Template Hierarchy

This document uses a **4-layer template stack** with clear separation of concerns:

### Layer 1: Foundation (Core Infrastructure)
**File:** `p2kb-foundation.sty`
**Purpose:** Pandoc compatibility, core LaTeX packages, basic document structure
**Provides:**
- Pandoc integration packages
- Basic typography and page layout
- Core color definitions
- Standard document infrastructure

### Layer 2: Content Styling
**File:** `p2kb-sp-styles.sty`
**Purpose:** Smart Pins-specific content elements and visual treatments
**Provides:**
- Code block styling (3 types: Configuration, Spin2, PASM2)
- Semantic marker boxes (7 types with distinct borders)
- Smart Pin mode formatting
- Technical content visual hierarchy
**Depends On:** p2kb-foundation.sty

### Layer 3: Numbering System
**File:** `p2kb-sp-numbering.sty`
**Purpose:** Custom numbering and cross-referencing for Smart Pins
**Provides:**
- Mode numbering system
- Pin reference formatting
- Example numbering
**Depends On:** p2kb-foundation.sty, p2kb-sp-styles.sty

### Layer 4: Presentation Branding
**File:** `p2kb-tech-review.sty`
**Purpose:** Technical review phase branding and title pages
**Provides:**
- Technical review title page
- Review status headers
- Copyright page
- Draft watermarks (if applicable)
**Depends On:** p2kb-foundation.sty

### Main Template
**File:** `p2kb-sp-template.latex`
**Purpose:** Master Pandoc template that orchestrates all layers
**Includes:** All 4 layers in correct order
**Variables:** title, subtitle, version, date, acknowledgments

## Loading Order (Critical!)

The template loads layers in this exact order:
```latex
1. \usepackage{p2kb-foundation}      % Core infrastructure first
2. \usepackage{p2kb-sp-styles}       % Content styling second
3. \usepackage{p2kb-sp-numbering}    % Numbering third
4. \usepackage{p2kb-tech-review}     % Branding last
```

**Why Order Matters:** Each layer builds on previous layers. Foundation provides basics, content adds styling, numbering adds structure, branding adds presentation.

## Request.json Configuration

Reference the template in request.json as:
```json
{
  "documents": [{
    "template": "p2kb-sp-template",
    "variables": {
      "title": "P2 Smart Pins Complete Tutorial",
      "subtitle": "Master Every Smart Pin Mode",
      "version": "Version 1.0 - Technical Review",
      "date": "2025"
    }
  }]
}
```

**Note:** Template name has NO `.latex` extension in request.json!

## Special Features

### Semantic Markers (7 types)
- Full borders with title bars
- Distinct border styles for accessibility
- Pastel color palette for extended reading

### Code Block System (3 types)
- **Configuration:** Pin setup and mode selection
- **Spin2:** High-level programming examples
- **PASM2:** Assembly language examples

### Visual Hierarchy
- 10.5pt body text (optimized for digital reading)
- 1.25x line spacing for comfort
- Digital-first margins (0.75" with 1" binding)

## Template Evolution

This template is **document-specific** and evolves with the Smart Pins documentation:
- Modifications stay within this workspace
- No shared template dependencies
- Template and content co-evolve
- Improvements preserved in this location only

## Deployment Process

1. **Edit:** Modify templates in this folder as needed
2. **Test:** Generate PDF via PDF Forge to verify changes
3. **Iterate:** Refine based on visual output
4. **Commit:** Version control changes when stable

Templates deploy to PDF Forge when copied to outbound directory alongside markdown and request.json.
