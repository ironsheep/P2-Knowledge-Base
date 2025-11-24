# P2 PASM DeSilva Style - Template Documentation

## Template Prefix
**Prefix:** `p2kb-desilva-*`
**Purpose:** Pedagogical P2 Assembly programming manual in deSilva tutorial style

## Template Hierarchy

This document uses a **2-layer template stack** optimized for pedagogical content:

### Layer 1: Foundation (DeSilva-Specific)
**File:** `p2kb-desilva-foundation.sty`
**Purpose:** Pandoc compatibility, basic document setup, deSilva-specific infrastructure
**Provides:**
- Pandoc integration packages
- 12pt font on letter paper (tutorial-friendly)
- Two-sided layout for printed manuals
- Basic pagination and structure
- deSilva color palette definitions

### Layer 2: Content & Pedagogy
**File:** `p2kb-desilva-content.sty`
**Purpose:** 5-color code system and pedagogical environments
**Provides:**
- **5-Color Code Block System:**
  - 🟢 Green = Spin2 (High-level language)
  - 🟡 Yellow = PASM2 (Assembly language)
  - 🟣 Purple = CORDIC (Math operations)
  - 🔵 Blue = Multi-COG (Parallel processing)
  - 🔴 Red = Antipattern (What NOT to do)
- **Pedagogical Environments:**
  - Sidetrack boxes (optional learning detours)
  - Interlude sections (conceptual bridges)
  - "Your Turn" exercises
  - Chapter celebration boxes
  - Medicine cabinet (quick reference tips)
- **Visual Teaching Elements:**
  - Code examples with clear labeling
  - Progressive difficulty markers
  - Success celebration moments
**Depends On:** p2kb-desilva-foundation.sty

### Additional Shared Foundation
**File:** `p2kb-foundation.sty`
**Purpose:** Generic P2KB foundation (may be used by content layer)
**Status:** Available for reference, may not be actively used

### Main Template
**File:** `p2kb-desilva.latex`
**Purpose:** Master Pandoc template with custom deSilva title page
**Includes:** Both foundation and content layers
**Variables:** title, subtitle, date, version

## Loading Order (Critical!)

The template loads layers in this exact order:
```latex
1. \usepackage{p2kb-desilva-foundation}  % deSilva-specific foundation first
2. \usepackage{p2kb-desilva-content}     % Pedagogical content second
```

**Why This Order:** Foundation establishes document structure and colors, content layer builds pedagogical elements on that foundation.

## Request.json Configuration

Reference the template in request.json as:
```json
{
  "documents": [{
    "template": "p2kb-desilva",
    "variables": {
      "title": "Discovering P2 Assembly",
      "subtitle": "Build, Experiment, and Master the Propeller 2",
      "date": "2025",
      "version": "Version 1.0 - Technical Review"
    }
  }]
}
```

**Note:** Template name has NO `.latex` extension in request.json!

## DeSilva Tutorial Philosophy

### Teaching Approach
- **Learn by doing:** Hands-on code examples throughout
- **Celebrate progress:** Chapter-end celebrations acknowledge learning
- **Have fun:** Approachable tone, encouraging voice
- **Build confidence:** Progressive complexity with clear scaffolding

### Visual Pedagogy
The 5-color code system helps learners:
- **Distinguish contexts** at a glance (Spin2 vs PASM2 vs CORDIC)
- **Track progression** from high-level to low-level
- **Recognize patterns** through consistent color coding
- **Avoid mistakes** through red antipattern highlighting

### Pedagogical Environments
- **Sidetracks:** Optional deeper dives (gray with dashed borders)
- **Interludes:** Conceptual bridges between topics (gray no border)
- **Your Turn:** Hands-on exercises (light blue boxes)
- **Chapter Celebrations:** Learning milestones (green tinted)
- **Medicine Cabinet:** Quick reference tips

## Template Evolution

This template is **document-specific** and evolves with the deSilva manual:
- Modifications stay within this workspace
- No shared template dependencies
- Template and pedagogical content co-evolve
- deSilva teaching style preserved and enhanced

## Deployment Process

1. **Edit:** Modify templates in this folder as needed
2. **Test:** Generate PDF via PDF Forge to verify pedagogical effectiveness
3. **Iterate:** Refine based on visual output and teaching clarity
4. **Commit:** Version control changes when stable

Templates deploy to PDF Forge when copied to outbound directory alongside markdown and request.json.
