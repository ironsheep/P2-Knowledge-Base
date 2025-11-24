# P2 Debug Window Manual - Template Documentation

## Template Prefix
**Prefix:** `p2kb-debugwin-*`
**Purpose:** Visual discovery manual for P2 DEBUG() system and 9 window types

## Template Hierarchy

This document uses a **2-layer template stack** optimized for visual/discovery content:

### Layer 1: Foundation (Debug Window-Specific)
**File:** `p2kb-debugwin-foundation.sty`
**Purpose:** Debug Window specific document infrastructure
**Provides:**
- Pandoc integration packages
- 11pt font on A4 paper (screen-reading optimized)
- Single-sided layout (digital-first)
- Screenshot and figure support
- Basic pagination and structure
- Debug window color palette

### Layer 2: Content & Visual Discovery
**File:** `p2kb-debugwin-content.sty`
**Purpose:** 5-color code system plus visual discovery elements
**Provides:**
- **5-Color Code Block System:**
  - Similar to deSilva approach but adapted for debug contexts
  - DEBUG statement highlighting
  - Window type differentiation
  - Discovery vs. reference code marking
- **Visual Elements:**
  - Screenshot placement and captioning
  - Discovery/experiment boxes
  - Window type comparison tables
  - Performance metric displays
- **Learning Style:**
  - Discovery-driven exploration
  - Visual verification emphasis
  - Hands-on experimentation encouragement
**Depends On:** p2kb-debugwin-foundation.sty

### Additional Shared Foundation
**File:** `p2kb-foundation.sty`
**Purpose:** Generic P2KB foundation (available for reference)
**Status:** Available but may not be actively used

### Main Template
**File:** `p2kb-debugwin.latex`
**Purpose:** Master Pandoc template with custom debug window title page
**Includes:** Both foundation and content layers
**Features:**
- Custom title page with review focus areas
- Document statistics section
- List of figures (for screenshots)
- Table of contents

## Loading Order (Critical!)

The template loads layers in this exact order:
```latex
1. \usepackage{p2kb-debugwin-foundation}  % Debug Window foundation first
2. \usepackage{p2kb-debugwin-content}     % Visual discovery content second
```

**Why This Order:** Foundation establishes document structure for visual content, content layer adds discovery-oriented elements.

## Request.json Configuration

Reference the template in request.json as:
```json
{
  "documents": [{
    "template": "p2kb-debugwin",
    "variables": {
      "title": "P2 Debug Window Manual",
      "subtitle": "Visual Discovery Through Systematic Exploration",
      "version": "Version 1.0 - Technical Review",
      "date": "September 2025"
    }
  }]
}
```

**Note:** Template name has NO `.latex` extension in request.json!

## Visual Discovery Philosophy

### Teaching Approach
- **Show, don't just tell:** Every feature has screenshot proof
- **Discover through exploration:** Encourage hands-on experimentation
- **Systematic coverage:** All 9 window types documented with examples
- **Visual verification:** Screenshots confirm every capability

### Window Types Covered
1. Terminal (text output)
2. Bitmap (graphics)
3. Plot (data visualization)
4. Scope (waveform display)
5. Logic (digital signals)
6. FFT (frequency analysis)
7. Spectro (spectrogram)
8. Scope_XY (X-Y plotting)
9. Mixed (combination windows)

### Visual Elements
- **Discovery Boxes:** "Try this experiment" prompts
- **Screenshots:** Visual proof of every feature
- **Comparison Tables:** Quick reference between window types
- **Performance Metrics:** Real measurements, not just specs

## Template Evolution

This template is **document-specific** and evolves with the Debug Window manual:
- Modifications stay within this workspace
- No shared template dependencies
- Template and visual content co-evolve
- Discovery-driven style preserved

## Deployment Process

1. **Edit:** Modify templates in this folder as needed
2. **Test:** Generate PDF via PDF Forge to verify visual layout
3. **Verify:** Check screenshot quality and placement
4. **Iterate:** Refine based on visual output
5. **Commit:** Version control changes when stable

Templates deploy to PDF Forge when copied to outbound directory alongside markdown, request.json, and assets/ folder (containing screenshots).

## Special Considerations

### Screenshots
- All screenshots must be in `assets/` folder at workspace root
- Reference in markdown as: `![Caption](assets/screenshot-name.png)`
- NO SPACES in screenshot filenames (use hyphens)
- PNG format preferred for clarity

### List of Figures
This template automatically generates a "List of Figures" from all `![...]()` image references, making it easy to navigate to specific screenshots.
