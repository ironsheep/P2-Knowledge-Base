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
workspace/p2-smart-pins-tutorial/     <- YOU ARE HERE (unescaped source)
|-- README.md                         # This file
|-- P2-Smart-Pins-Green-Book-Tutorial.md  # Master document (UNESCAPED)
|-- templates/
|   |-- README.md                     # Template documentation
|   |-- p2kb-sp-template.latex        # Main LaTeX template
|   |-- p2kb-sp-foundation.sty        # Core infrastructure (SP-specific)
|   |-- p2kb-sp-styles.sty            # Smart Pins content styling
|   |-- p2kb-sp-numbering.sty         # Numbering system
|   +-- p2kb-sp-diagrams.sty          # TikZ diagram macros (18 diagrams)
|-- filters/
|   |-- p2kb-sp-fix-hypertarget.lua   # Hypertarget fixes
|   |-- p2kb-sp-fix-title-as-part.lua # Title-to-part conversion
|   |-- p2kb-sp-frontmatter.lua       # Front matter handling
|   |-- p2kb-sp-structure.lua         # Document structure
|   |-- p2kb-sp-index-toc.lua         # Index and TOC
|   |-- p2kb-sp-code-coloring.lua     # Code block coloring
|   +-- p2kb-sp-semantic.lua          # Semantic marker conversion
|-- assets/
|   +-- (PNG images for diagrams)
|-- request.json                      # PDF Forge configuration
|-- request-requirements.json         # Mandatory pandoc arguments
|-- green-book-processing-guide.md    # Processing documentation
+-- green-book-markdown-changes-guide.md  # Markdown transform rules

outbound/p2-smart-pins-tutorial/      <- FLAT structure for PDF Forge
|-- P2-Smart-Pins-Green-Book-Tutorial.md  # ESCAPED copy (same name!)
|-- p2kb-sp-template.latex            # Template (FLAT - root level)
|-- p2kb-sp-foundation.sty            # Style files (FLAT - root level)
|-- p2kb-sp-styles.sty
|-- p2kb-sp-numbering.sty
|-- p2kb-sp-diagrams.sty
|-- p2kb-sp-fix-hypertarget.lua       # Lua filters (FLAT - root level)
|-- p2kb-sp-fix-title-as-part.lua
|-- p2kb-sp-frontmatter.lua
|-- p2kb-sp-structure.lua
|-- p2kb-sp-index-toc.lua
|-- p2kb-sp-code-coloring.lua
|-- p2kb-sp-semantic.lua
|-- request.json                      # Config (FLAT - root level)
+-- assets/                           # ALL images go here (only subfolder!)
    |-- book-artwork.png              # Cover image
    +-- *.png                         # All other images
```

---

## PDF Forge Workflow

### CRITICAL UNDERSTANDING: PDF Forge Persistence

**PDF Forge is a PERSISTENT system.** It retains ALL files from the last deployment indefinitely. This has major implications:

1. **Files sent to Forge DISAPPEAR from outbound** - The user MOVES (not copies) files to the Forge
2. **Forge keeps the last version of every file** - If you sent `p2kb-sp-styles.sty` last week, Forge still has it
3. **Only send files that CHANGED or were RENAMED** - Sending unchanged files is pointless; Forge already has them
4. **Renaming requires sending the new file** - If you rename `foo.sty` to `bar.sty`, you must send `bar.sty`

**Why outbound is often empty:** After user deploys to Forge, ALL files are moved out. This is NORMAL. It does NOT mean the Forge lost them - the Forge is persistent. An empty outbound just means nothing new needs to be sent.

### Overview

```
WORKSPACE (unescaped)          OUTBOUND (staging)              PDF FORGE (persistent)
        |                              |                               |
   Edit files here            Stage ONLY changes here         Retains ALL files
        |                              |                               |
        +---- latex-escape-all.sh ---->|                               |
              + copy CHANGED files     |                               |
                                       +---- User MOVES files -------->|
                                             (files DISAPPEAR          |
                                              from outbound)           |
                                                                       |
        <------------------- User provides feedback -------------------+
        |
   Fix issues, repeat (only send what changed)
```

### Step-by-Step Process

#### 1. Edit in Workspace
All edits happen in the workspace folder. Files here are **unescaped** - this is your source of truth.

#### 2. Stage ONLY Changed Files to Outbound

**CRITICAL: Only stage files that CHANGED!**

PDF Forge already has every file from the last deployment. Ask yourself:
- Did this file's CONTENT change? -> Stage it
- Did this file get RENAMED? -> Stage the new name
- Is this file UNCHANGED? -> DO NOT stage it (Forge has it)

```bash
# From the workspace folder:
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/p2-smart-pins-tutorial

# Run escape script for markdown (content usually changes each iteration)
../../../tools/latex-escape-all.sh \
    P2-Smart-Pins-Green-Book-Tutorial.md \
    ../../outbound/p2-smart-pins-tutorial/P2-Smart-Pins-Green-Book-Tutorial.md

# Copy ONLY templates that CHANGED (not all of them!)
# Example: If only p2kb-sp-styles.sty changed:
cp templates/p2kb-sp-styles.sty ../../outbound/p2-smart-pins-tutorial/

# Copy ONLY filters that CHANGED
# Example: If p2kb-sp-semantic.lua was modified:
cp filters/p2kb-sp-semantic.lua ../../outbound/p2-smart-pins-tutorial/

# Copy request.json ONLY if it changed
cp request.json ../../outbound/p2-smart-pins-tutorial/
```

**Decision guide for each file type:**

| File Type | When to Stage |
|-----------|---------------|
| `.md` (markdown) | Usually every iteration (content changes) |
| `.latex` (template) | Only if template structure changed |
| `.sty` (style) | Only if styling/environments changed |
| `.lua` (filter) | Only if filter logic changed |
| `request.json` | Only if pandoc args or metadata changed |
| `.png` (assets) | Only if new images added or images replaced |

#### 3. User Deploys to PDF Forge

The user **MOVES** (not copies) files from `outbound/p2-smart-pins-tutorial/` to PDF Forge.

**After deployment, outbound will be EMPTY or nearly empty.** This is NORMAL and EXPECTED:
- Files were MOVED, not copied
- Forge now has them persistently
- Empty outbound = nothing new to send
- DO NOT panic and re-copy everything

#### 4. Feedback Loop

- If PDF Forge reports errors -> User relays error messages -> Fix in workspace -> Stage ONLY the fixed files -> Repeat
- If PDF generates successfully -> User provides visual feedback -> Fix in workspace -> Stage ONLY the fixed files -> Repeat
- Continue until PDF is correct

**Each iteration, only stage files you actually modified.** The Forge already has everything else.

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

#### 6. Interactive Testing for Component Isolation

For debugging specific components (like individual TikZ diagrams), use PDF Forge's interactive testing system:

```
/engineering/pdf-forge/interactive-testing/
├── templates/          # Drop template files here
├── test-documents/     # Create minimal test .md files
├── test-requests/      # JSON requests (timestamped: test-$(date +%s).json)
└── test-results/       # Results appear here automatically
```

**Usage:**
1. Copy templates to `interactive-testing/templates/`
2. Create minimal test documents in `test-documents/` (e.g., one diagram per file)
3. Create timestamped request: `test-requests/test-$(date +%s).json`
4. Forge processes automatically; results appear in `test-results/`

**Example:** To test all 18 TikZ diagrams individually, create 18 test files each containing just one `\DiagramName` macro. This isolates which specific diagram is failing.

**Full documentation:** `/engineering/pdf-forge/interactive-testing/README.md`

---

### Important Notes

- **Outbound is FLAT** - All `.sty`, `.latex`, `.lua`, and `.json` files go at root level
- **One exception: `assets/`** - This is the ONLY subfolder; ALL images go here (cover image and body images alike)
- **Same filename everywhere** - `P2-Smart-Pins-Green-Book-Tutorial.md` in workspace AND outbound
- **Workspace is unescaped** - Never run escape script in place; always output to outbound
- **Outbound empties after deployment** - This is NORMAL; Forge has the files persistently
- **Iterative process** - Expect multiple rounds of feedback and fixes; only send what changed

---

## Document Identity

**Type:** Enhanced Tutorial Guide (Titus Remastered - "Green Book")
**Target Audience:** Anyone learning Smart Pins or implementing advanced features
**Size:** ~450 pages (comprehensive learning resource)
**Philosophy:** "Understand deeply, implement confidently"

---

## Template Stack

**Prefix:** `p2kb-sp-*` (all files use this prefix for isolation)

```
Layer 1: p2kb-sp-foundation.sty (core infrastructure)
    |
Layer 2: p2kb-sp-styles.sty (Smart Pins content styling)
    |
Layer 3: p2kb-sp-numbering.sty (numbering system)
    |
Layer 4: p2kb-sp-diagrams.sty (TikZ timing/block diagrams)
    |
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
1. `p2kb-sp-fix-hypertarget.lua` - Hypertarget fixes
2. `p2kb-sp-fix-title-as-part.lua` - Title-to-part conversion
3. `p2kb-sp-frontmatter.lua` - Front matter handling
4. `p2kb-sp-structure.lua` - Document structure
5. `p2kb-sp-index-toc.lua` - Index and TOC
6. `p2kb-sp-code-coloring.lua` - Code block coloring
7. `p2kb-sp-semantic.lua` - Semantic marker conversion

**Order Critical:** Each filter depends on previous filter's output

### Assets

**All images go in one place: `outbound/p2-smart-pins-tutorial/assets/`**

This is the ONLY subfolder in outbound. Every PNG file goes here - cover image, body images, everything.

**IMPORTANT: `inbox/assets/` path in markdown:**

The markdown source (specifically the raw LaTeX cover page block) references `inbox/assets/book-artwork.png`. This path is for PDF Forge's internal resolution - you do NOT create an `inbox/` folder in outbound. The actual file goes in `assets/`:

| Markdown Path | Actual Outbound Location |
|---------------|--------------------------|
| `inbox/assets/book-artwork.png` | `assets/book-artwork.png` |
| `assets/smart-pins-master-trimmed.png` | `assets/smart-pins-master-trimmed.png` |

PDF Forge handles the path mapping internally. When staging files:
```bash
# ALL images go to the same assets/ folder
cp workspace/.../assets/*.png outbound/.../assets/
```

**Rules:**
- NO SPACES in filenames (use hyphens: `smart-pins-master-trimmed.png`)
- Do NOT create `inbox/` folder in outbound - it doesn't exist there
- TikZ diagrams are replacing most PNG images (fewer assets needed over time)

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
        "--pdf-engine=xelatex"
      ],
      "lua_filters": [
        "p2kb-sp-fix-hypertarget",
        "p2kb-sp-fix-title-as-part",
        "p2kb-sp-frontmatter",
        "p2kb-sp-structure",
        "p2kb-sp-index-toc",
        "p2kb-sp-code-coloring",
        "p2kb-sp-semantic"
      ]
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
*Updated: 2025-12-03 - Added interactive testing section for component isolation debugging*
*Sprint: Smart Pins Tutorial Audit*
