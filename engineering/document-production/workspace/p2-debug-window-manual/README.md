# Workspace - P2 Debug Window Manual

**Purpose:** PDF production workspace for the P2 Debug Window Manual.

**Status:** Active - Visual Refinement Phase
**Content Source:** `../../manuals/p2-debug-window-manual/`

---

## Quick Reference

| Resource | Location |
|----------|----------|
| **Creation Guide** | `../../manuals/p2-debug-window-manual/creation-guide.md` |
| **Escape Script** | `../../../tools/conversion/latex-escape-all.sh` |
| **Outbound Folder** | `../../outbound/p2-debug-window-manual/` |

---

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Critical File Naming Convention

**The master document name is sacred and never changes:**

| Purpose | Filename |
|---------|----------|
| **Master Document** | `P2-Debug-Window-Manual.md` |
| **Output PDF** | `P2-Debug-Window-Manual.pdf` |

**Rules:**
- Always use the exact document name - no suffixes like `-escaped`, `-v2`, `-final`
- The workspace copy is unescaped (source of truth)
- The outbound copy is escaped (ready for Forge)
- Both use the identical filename: `P2-Debug-Window-Manual.md`
- Never rename files - always replace in place

---

## Directory Structure

```
workspace/p2-debug-window-manual/     ← YOU ARE HERE (unescaped source)
├── README.md                          # This file
├── P2-Debug-Window-Manual.md          # Master document (UNESCAPED)
├── templates/
│   ├── README.md                      # Template documentation
│   ├── p2kb-debugwin.latex            # Main LaTeX template
│   ├── p2kb-debugwin-foundation.sty   # Debug window-specific foundation
│   └── p2kb-debugwin-content.sty      # Visual discovery elements
├── filters/
│   └── *.lua                          # Lua filters if needed
├── assets/
│   └── *.png                          # Screenshots (NO SPACES in filenames)
├── request.json                       # PDF Forge configuration
└── fix-*.py                           # Content processing scripts

outbound/p2-debug-window-manual/       ← FLAT structure for PDF Forge
├── P2-Debug-Window-Manual.md          # ESCAPED copy (same name!)
├── p2kb-debugwin.latex                # Template (FLAT - no subfolder!)
├── p2kb-debugwin-foundation.sty       # Style files at root level
├── p2kb-debugwin-content.sty
├── *.lua                              # Filters at root level
├── *.png                              # Screenshots at root level
└── request.json
```

---

## PDF Forge Workflow

### CRITICAL UNDERSTANDING: PDF Forge Persistence

**PDF Forge is a PERSISTENT system.** It retains ALL files from the last deployment indefinitely. This has major implications:

1. **Files sent to Forge DISAPPEAR from outbound** - The user MOVES (not copies) files to the Forge
2. **Forge keeps the last version of every file** - If you sent `p2kb-debugwin-content.sty` last week, Forge still has it
3. **Only send files that CHANGED** - Sending unchanged files is pointless; Forge already has them
4. **Renaming requires sending the new file** - If you rename `foo.sty` to `bar.sty`, you must send `bar.sty`

**Why outbound is often empty:** After user deploys to Forge, ALL files are moved out. This is NORMAL. It does NOT mean the Forge lost them.

### Overview

```
WORKSPACE (unescaped)          OUTBOUND (staging)              PDF FORGE (persistent)
        │                              │                               │
   Edit files here            Stage ONLY changes here         Retains ALL files
        │                              │                               │
        └── latex-escape-all.sh ──────►│                               │
              + copy CHANGED files     │                               │
                                       └──── User MOVES files ────────►│
                                             (files DISAPPEAR          │
                                              from outbound)           │
                                                                       │
        ◄─────────────────── User provides feedback ───────────────────┘
        │
   Fix issues, repeat (only send what changed)
```

### Step-by-Step Process

#### 1. Edit in Workspace
All edits happen in the workspace folder. Files here are **unescaped** - this is your source of truth.

#### 2. Stage ONLY Changed Files to Outbound

**CRITICAL: Only stage files that CHANGED!**

```bash
# From the workspace folder:
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/p2-debug-window-manual

# Run escape script for markdown (content usually changes each iteration)
../../../tools/conversion/latex-escape-all.sh \
    P2-Debug-Window-Manual.md \
    ../../outbound/p2-debug-window-manual/P2-Debug-Window-Manual.md

# Copy ONLY templates that CHANGED (not all of them!)
cp templates/p2kb-debugwin-content.sty ../../outbound/p2-debug-window-manual/

# Copy ONLY filters that CHANGED
cp filters/*.lua ../../outbound/p2-debug-window-manual/

# Copy ONLY new or changed screenshots (FLAT - no subfolder!)
cp assets/new-screenshot.png ../../outbound/p2-debug-window-manual/

# Copy request.json ONLY if it changed
cp request.json ../../outbound/p2-debug-window-manual/
```

**Decision guide for each file type:**

| File Type | When to Stage |
|-----------|---------------|
| `.md` (markdown) | Usually every iteration (content changes) |
| `.latex` (template) | Only if template structure changed |
| `.sty` (style) | Only if styling/environments changed |
| `.lua` (filter) | Only if filter logic changed |
| `.png` (screenshots) | Only if new images added or replaced |
| `request.json` | Only if pandoc args or metadata changed |

#### 3. User Deploys to PDF Forge
The user **MOVES** (not copies) files from outbound to PDF Forge. **After deployment, outbound will be EMPTY.** This is NORMAL.

#### 4. Feedback Loop
- If PDF Forge reports errors → Fix in workspace → Stage ONLY the fixed files → Repeat
- If PDF generates successfully → User provides visual feedback → Fix → Repeat
- Each iteration, only stage files you actually modified

#### 5. Debugging with Generated .tex File
After each PDF Forge run, the user will drop the generated `.tex` file into the outbound directory:
```
outbound/p2-debug-window-manual/P2-Debug-Window-Manual.tex
```
This intermediate LaTeX file is useful for:
- Correlating error line numbers to actual content
- Understanding how Pandoc transformed the markdown
- Debugging rendering issues when user provides visual feedback

### Important Notes

- **Outbound is FLAT** - No subfolders! All files go at root level (including screenshots!)
- **Same filename everywhere** - `P2-Debug-Window-Manual.md` in workspace AND outbound
- **Workspace is unescaped** - Never run escape script in place; always output to outbound
- **Outbound files disappear** - This is normal; user moves them to Forge
- **Iterative process** - Expect multiple rounds of feedback and fixes

---

## Document Identity

**Document Title:** P2 Debug Window Manual
**Subtitle:** Visual Discovery Through Systematic Exploration
**Philosophy:** "Show, don't just tell" - Every feature proven with screenshots

---

## Template Stack

**Prefix:** `p2kb-debugwin-*`

| File | Purpose |
|------|---------|
| `p2kb-debugwin.latex` | Main template + list of figures |
| `p2kb-debugwin-foundation.sty` | Debug window-specific foundation |
| `p2kb-debugwin-content.sty` | Visual discovery elements |

**Full Details:** See [templates/README.md](templates/README.md)

## Window Types Covered

1. **Terminal** - Text output and logging
2. **Bitmap** - Graphics and image display
3. **Plot** - Data visualization and charting
4. **Scope** - Waveform display
5. **Logic** - Digital signal analysis
6. **FFT** - Frequency analysis
7. **Spectro** - Spectrogram visualization
8. **Scope_XY** - X-Y plotting
9. **Mixed** - Combination windows

## Visual Discovery Philosophy

### Teaching Approach
- **Visual First:** Every feature shown with screenshot
- **Systematic Exploration:** Methodical coverage of all capabilities
- **Hands-On Discovery:** "Try this experiment" prompts throughout
- **Performance Metrics:** Real measurements, not just specs

### Content Structure
- **Discovery Boxes:** Experiment prompts and exploration suggestions
- **Screenshots:** Visual proof of every feature (requires assets/)
- **Comparison Tables:** Quick reference between window types
- **Code Examples:** Complete DEBUG() statement examples

## Content Processing Scripts

Scripts for preprocessing content before PDF generation:

| Script | Purpose |
|--------|---------|
| `convert-debug-window-images.py` | Image conversion/preparation |
| `fix-unicode-characters.py` | Unicode character normalization |
| `fix-document-structure.py` | Document structure corrections |

## Screenshot Requirements

- **Location:** `assets/` folder in workspace
- **Format:** PNG preferred for clarity
- **Naming:** NO SPACES (use hyphens: `Terminal-Window-Example.png`)
- **Outbound:** Copy screenshots FLAT to outbound root (no subfolder!)
- **List of Figures:** Template automatically generates from image references

---

## PDF Forge Configuration

The `request.json` file configures PDF Forge:

```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "P2-Debug-Window-Manual.md",
      "output": "P2-Debug-Window-Manual.pdf",
      "template": "p2kb-debugwin",
      "pandoc_args": [
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2"
      ],
      "metadata": {
        "title": "P2 Debug Window Manual",
        "subtitle": "Visual Discovery Through Systematic Exploration",
        "author": "Iron Sheep Productions, LLC"
      }
    }
  ]
}
```

---

## Document Statistics

| Metric | Value |
|--------|-------|
| **Total Chapters** | 14 |
| **Appendices** | 5 (Command Reference, Examples, Performance) |
| **Window Types** | 9 (Full coverage) |
| **Code Examples** | 200+ |
| **Learning Style** | Discovery-driven exploration |

---

*Created: 2025-09-10*
*Updated: 2025-12-03 - Restructured to match gold standard format*
