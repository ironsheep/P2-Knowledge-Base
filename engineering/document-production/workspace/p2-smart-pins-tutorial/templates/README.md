# P2 Smart Pins Tutorial - Template Documentation

## Template Prefix
**Prefix:** `p2kb-sp-*`
**Purpose:** Smart Pins tutorial and reference documentation

## Template Hierarchy

This document uses a **4-layer template stack** with clear separation of concerns:

### Layer 1: Foundation (Core Infrastructure)
**File:** `p2kb-sp-foundation.sty`
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
**Depends On:** p2kb-sp-foundation.sty

### Layer 3: Numbering System
**File:** `p2kb-sp-numbering.sty`
**Purpose:** Custom numbering and cross-referencing for Smart Pins
**Provides:**
- Mode numbering system
- Pin reference formatting
- Example numbering
**Depends On:** p2kb-sp-foundation.sty, p2kb-sp-styles.sty

### Layer 4: TikZ Diagrams
**File:** `p2kb-sp-diagrams.sty`
**Purpose:** Vector timing diagrams and block diagrams replacing PNG assets
**Provides:**
- 18 TikZ diagram commands (timing diagrams, block diagrams, waveforms)
- Consistent styling matching original PNG visual style
- See `SMARTPINS-DIAGRAMS-REFERENCE.md` for complete diagram mapping
**Depends On:** p2kb-sp-foundation.sty (TikZ packages)

### Main Template
**File:** `p2kb-sp-template.latex`
**Purpose:** Master Pandoc template that orchestrates all layers
**Includes:** All 4 layers in correct order

## Cover Page

The cover page is embedded directly in the markdown file as raw LaTeX (De Silva style).
This approach:
- Uses the standard P2KB banner image (`assets/book-artwork.png`)
- Includes title, subtitle, date, and version
- Features a "Tutorial Guide" box explaining code block colors
- Generates table of contents
- Sets page style to fancy after cover

## Loading Order (Critical!)

The template loads layers in this exact order:
```latex
1. \usepackage{p2kb-sp-foundation}   % Core infrastructure first
2. \usepackage{p2kb-sp-styles}       % Content styling second
3. \usepackage{p2kb-sp-numbering}    % Numbering third
4. \usepackage{p2kb-sp-diagrams}     % TikZ diagrams fourth
```

**Why Order Matters:** Each layer builds on previous layers. Foundation provides basics, content adds styling, numbering adds structure, diagrams add visuals.

## Request.json Configuration

Reference the template in request.json as:
```json
{
  "documents": [{
    "input": "P2-Smart-Pins-Green-Book-Tutorial.md",
    "output": "P2-Smart-Pins-Green-Book-Tutorial.pdf",
    "template": "p2kb-sp-template"
  }]
}
```

**Note:** Template name has NO `.latex` extension in request.json!

## Special Features

### Code Block System (3 types)
- **Spin2:** High-level programming examples (green)
- **PASM2:** Assembly language examples (yellow)
- **Antipattern:** What NOT to do (red)

### Visual Hierarchy
- 11pt body text
- Digital-first margins
- Consistent with De Silva manual styling

## Archive

The `archive/` subdirectory contains unused style files kept for reference:
- `p2kb-sp-tech-review.sty` - Previous tech-review branding (replaced by markdown cover)

## Deployment Process

1. **Edit:** Modify templates in this folder as needed
2. **Test:** Generate PDF via PDF Forge to verify changes
3. **Iterate:** Refine based on visual output
4. **Commit:** Version control changes when stable

Templates deploy to PDF Forge when copied to outbound directory alongside markdown and request.json.
