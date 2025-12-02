# Workspace - P2 Smart Pins Tutorial (Green Book)

**Purpose:** PDF production workspace for the P2 Smart Pins Complete Tutorial.

**Status:** Active - Sprint audit complete, ready for PDF generation
**Content Source:** `../../manuals/p2-smart-pins-tutorial/opus-master-green-book/`

---

## Quick Reference

| Resource | Location |
|----------|----------|
| **Content (Opus Master)** | `../../manuals/p2-smart-pins-tutorial/opus-master-green-book/` |
| **Creation Guide** | `../../manuals/p2-smart-pins-tutorial/creation-guide.md` |
| **Style Guide** | `../../manuals/p2-smart-pins-tutorial/style-guide.md` |
| **Content Guide** | `../../manuals/p2-smart-pins-tutorial/content-guide.md` |
| **Presentation Style** | `../../manuals/p2-smart-pins-tutorial/presentation-style-guide.md` |
| **Escape Script** | `../../../tools/latex-escape-all.sh` |
| **Outbound Folder** | `../../outbound/p2-smart-pins-tutorial/` |

---

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Critical File Naming Convention

**The master document name is sacred and never changes:**

| Purpose | Filename |
|---------|----------|
| **Master Document** | `P2-Smart-Pins-Green-Book-Tutorial.md` |
| **Output PDF** | `P2-Smart-Pins-Green-Book-Tutorial.pdf` |

**Rules:**
- Always use the exact document name - no suffixes like `-escaped`, `-v2`, `-final`
- The workspace copy is unescaped (source of truth)
- The outbound copy is escaped (ready for Forge)
- Both use the identical filename: `P2-Smart-Pins-Green-Book-Tutorial.md`
- Never rename files - always replace in place

---

## Directory Structure

```
workspace/p2-smart-pins-tutorial/     ← YOU ARE HERE (unescaped source)
├── README.md                         # This file
├── P2-Smart-Pins-Green-Book-Tutorial.md  # Master document (UNESCAPED)
├── templates/
│   ├── README.md                     # Template documentation
│   ├── p2kb-sp-template.latex        # Main LaTeX template
│   ├── p2kb-foundation.sty           # Core infrastructure (shared)
│   ├── p2kb-sp-styles.sty            # Smart Pins content styling
│   ├── p2kb-sp-numbering.sty         # Numbering system
│   ├── p2kb-tech-review.sty          # Presentation branding
│   └── p2kb-smartpins-diagrams.sty   # TikZ diagram macros (18 diagrams)
├── filters/
│   ├── smart-pins-colored-blocks.lua # Code block coloring
│   ├── green-book-semantic-blocks.lua# Semantic marker conversion
│   └── part-chapter-pagebreaks.lua   # Page break management
├── assets/
│   └── (PNG images for diagrams)
├── request.json                      # PDF Forge configuration
├── request-requirements.json         # Mandatory pandoc arguments
├── green-book-processing-guide.md    # Processing documentation
└── green-book-markdown-changes-guide.md  # Markdown transform rules

outbound/p2-smart-pins-tutorial/      ← FLAT structure for PDF Forge
├── P2-Smart-Pins-Green-Book-Tutorial.md  # ESCAPED copy (same name!)
├── p2kb-sp-template.latex            # Template (FLAT - no subfolder!)
├── p2kb-foundation.sty               # Style files at root level
├── p2kb-sp-styles.sty
├── p2kb-sp-numbering.sty
├── p2kb-tech-review.sty
├── p2kb-smartpins-diagrams.sty
├── smart-pins-colored-blocks.lua     # Lua filters at root level
├── green-book-semantic-blocks.lua
├── part-chapter-pagebreaks.lua
└── request.json
```

---

## PDF Forge Workflow

### Overview

```
WORKSPACE (unescaped)          OUTBOUND (escaped, flat)         PDF FORGE
        │                              │                            │
   Edit files here            Escape & flatten here          Generate PDF here
        │                              │                            │
        └──── latex-escape-all.sh ────►│                            │
              + copy templates flat    │                            │
                                       └──── User hand-copies ─────►│
                                             (files disappear)      │
                                                                    │
        ◄─────────────────── User provides feedback ────────────────┘
        │
   Fix issues, repeat
```

### Step-by-Step Process

#### 1. Edit in Workspace
All edits happen in the workspace folder. Files here are **unescaped** - this is your source of truth.

#### 2. Escape and Stage to Outbound

**IMPORTANT: Only copy files that have changed!** PDF Forge is persistent and retains the last version of each file. Sending unchanged files is nonsensical - the Forge already has them. Only stage files that were actually modified in this iteration.

```bash
# From the workspace folder:
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/p2-smart-pins-tutorial

# Run escape script (creates backup automatically)
../../../tools/latex-escape-all.sh \
    P2-Smart-Pins-Green-Book-Tutorial.md \
    ../../outbound/p2-smart-pins-tutorial/P2-Smart-Pins-Green-Book-Tutorial.md

# Copy ONLY CHANGED templates FLAT (no subfolder!) to outbound
# Example: If only p2kb-sp-styles.sty changed:
cp templates/p2kb-sp-styles.sty ../../outbound/p2-smart-pins-tutorial/

# Copy ONLY CHANGED filters to outbound
# Example: If green-book-semantic-blocks.lua was modified:
cp filters/green-book-semantic-blocks.lua ../../outbound/p2-smart-pins-tutorial/

# Copy request.json ONLY if it changed
cp request.json ../../outbound/p2-smart-pins-tutorial/
```

**What to copy each iteration:**
- `P2-Smart-Pins-Green-Book-Tutorial.md` - Always (content changes)
- Template files (`.latex`, `.sty`) - Only if modified
- Lua filters (`.lua`) - Only if modified or added
- `request.json` - Only if configuration changed

#### 3. User Deploys to PDF Forge
The user hand-copies files from `outbound/p2-smart-pins-tutorial/` to PDF Forge.
**Files will disappear from outbound** after being moved to the Forge.

#### 4. Feedback Loop
- If PDF Forge reports errors → User relays error messages → Fix in workspace → Re-escape → Repeat
- If PDF generates successfully → User provides visual feedback → Fix in workspace → Re-escape → Repeat
- Continue until PDF is correct

#### 5. Debugging with Generated .tex File
After each PDF Forge run, the user will drop the generated `.tex` file into the outbound directory:
```
outbound/p2-smart-pins-tutorial/P2-Smart-Pins-Green-Book-Tutorial.tex
```
This intermediate LaTeX file is useful for:
- Correlating error line numbers to actual content
- Understanding how Pandoc transformed the markdown
- Debugging rendering issues when user provides visual feedback
- Finding the exact LaTeX that produced problematic output

### Important Notes

- **Outbound is FLAT** - No subfolders! All `.sty`, `.latex`, and `.lua` files go at root level
- **Same filename everywhere** - `P2-Smart-Pins-Green-Book-Tutorial.md` in workspace AND outbound
- **Workspace is unescaped** - Never run escape script in place; always output to outbound
- **Outbound files disappear** - This is normal; user moves them to Forge
- **Iterative process** - Expect multiple rounds of feedback and fixes

---

## Document Identity

**Type:** Enhanced Tutorial Guide (Titus Remastered - "Green Book")
**Target Audience:** Anyone learning Smart Pins or implementing advanced features
**Size:** ~450 pages (comprehensive learning resource)
**Philosophy:** "Understand deeply, implement confidently"

---

## Template Stack

**Prefix:** `p2kb-sp-*`

```
Layer 1: p2kb-foundation.sty (core infrastructure)
    ↓
Layer 2: p2kb-sp-styles.sty (Smart Pins content styling)
    ↓
Layer 3: p2kb-sp-numbering.sty (numbering system)
    ↓
Layer 4: p2kb-tech-review.sty (presentation branding)
    ↓
Main: p2kb-sp-template.latex (orchestrates all layers)
```

**Full Details:** See [templates/README.md](templates/README.md)

---

## Special Requirements

### Pandoc Arguments (CRITICAL!)
This document REQUIRES special pandoc arguments:
```json
{
  "required_pandoc_args": ["--top-level-division=part"]
}
```

**Why:** Document uses Part/Chapter structure. Without this argument, page breaks fail.
**Documented In:** `request-requirements.json` in this workspace

### Lua Filter Pipeline
Filters must be applied in this exact order:
1. `smart-pins-colored-blocks.lua` - Code block coloring
2. `green-book-semantic-blocks.lua` - Semantic marker conversion
3. `part-chapter-pagebreaks.lua` - Page break management

**Order Critical:** Each filter depends on previous filter's output

### Assets Folder
- **Location:** `assets/` subfolder in this workspace
- **Contents:** PNG images (Smart Pins diagrams and oscilloscope captures)
- **Naming:** NO SPACES in filenames (use hyphens: `smart-pins-master-trimmed.png`)
- **References:** Use relative paths in markdown: `![Caption](assets/image.png)`
- **TikZ Replacement:** Most PNG images have been replaced with TikZ diagrams

---

## Visual Features

### Semantic Markers (7 types)
- Full borders with title bars
- Distinct border styles (solid, dashed, dotted) for accessibility
- Pastel color palette optimized for extended reading

### Code Block System (3 types)
- **Spin2:** High-level programming examples (light green)
- **PASM2:** Assembly language examples (light yellow)
- **Antipattern:** Common mistakes with correct alternatives (light red)

### Typography
- 10.5pt body text (5% larger than reference manual)
- 1.25x line spacing for comfortable reading
- Digital-first margins (0.75" with 1" binding)

---

## Two-Book Strategy

This workspace maintains the "Green Book" (tutorial) variant of Smart Pins documentation:

| Book | Pages | Purpose |
|------|-------|---------|
| **Green Book** (this) | ~450 | Comprehensive tutorial |
| **Blue Book** (separate) | ~230 | Quick reference |

---

## PDF Forge Configuration

The `request.json` file configures PDF Forge:

```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "P2-Smart-Pins-Green-Book-Tutorial.md",
      "output": "P2-Smart-Pins-Green-Book-Tutorial.pdf",
      "template": "p2kb-sp-template",
      "pandoc_args": [
        "--top-level-division=part",
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=3",
        "--lua-filter=smart-pins-colored-blocks.lua",
        "--lua-filter=green-book-semantic-blocks.lua",
        "--lua-filter=part-chapter-pagebreaks.lua"
      ],
      "metadata": {
        "title": "P2 Smart Pins Complete Tutorial",
        "subtitle": "Master Every Smart Pin Mode Through Progressive Learning",
        "author": "Iron Sheep Productions, LLC",
        "version": "Version 1.0 - Technical Review",
        "date": "December 2025"
      }
    }
  ]
}
```

Required arguments are documented in `request-requirements.json`.

---

## Related Processing Documents

### In This Workspace
- **Green Book Processing Guide:** `green-book-processing-guide.md`
- **Markdown Changes Guide:** `green-book-markdown-changes-guide.md`

### Universal Methodology
- **Format Guide:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`

---

*Created: 2025-09-10*
*Updated: 2025-12-02 - Sprint audit complete, PDF Forge workflow documented*
*Sprint: Smart Pins Tutorial Audit*
