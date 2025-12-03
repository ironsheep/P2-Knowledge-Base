# Workspace - AI Privacy Guide

**Purpose:** PDF production workspace for the AI Privacy Guide for P2 Developers.

**Status:** Deferred - Not P2-related content
**Content Source:** This workspace (standalone documents)

---

## Quick Reference

| Resource | Location |
|----------|----------|
| **Escape Script** | `../../../tools/conversion/latex-escape-all.sh` |
| **Outbound Folder** | `../../outbound/ai-privacy-guide/` |

---

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Critical File Naming Convention

**The master document name is sacred and never changes:**

| Purpose | Filename |
|---------|----------|
| **Master Document** | `ai-privacy-guide.md` |
| **Output PDF** | `ai-privacy-guide.pdf` |

**Rules:**
- Always use the exact document name - no suffixes like `-escaped`, `-v2`, `-final`
- The workspace copy is unescaped (source of truth)
- The outbound copy is escaped (ready for Forge)
- Both use the identical filename: `ai-privacy-guide.md`
- Never rename files - always replace in place

---

## Directory Structure

```
workspace/ai-privacy-guide/     ← YOU ARE HERE (unescaped source)
├── README.md                    # This file
├── ai-privacy-guide.md          # Master document (UNESCAPED)
├── ai-implementation-strategy.md
├── claude-code-privacy-guide-for-p2-developers.md
├── templates/
│   ├── README.md                # Template documentation
│   └── p2kb-presentation.latex  # Presentation-style template
├── filters/
│   └── *.lua                    # Lua filters if needed
└── request.json                 # PDF Forge configuration

outbound/ai-privacy-guide/       ← FLAT structure for PDF Forge
├── ai-privacy-guide.md          # ESCAPED copy (same name!)
├── p2kb-presentation.latex      # Template (FLAT - no subfolder!)
├── *.lua                        # Filters at root level
└── request.json
```

---

## PDF Forge Workflow

### CRITICAL UNDERSTANDING: PDF Forge Persistence

**PDF Forge is a PERSISTENT system.** It retains ALL files from the last deployment indefinitely. This has major implications:

1. **Files sent to Forge DISAPPEAR from outbound** - The user MOVES (not copies) files to the Forge
2. **Forge keeps the last version of every file** - Templates persist between deployments
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

### Step-by-Step Process (If Work Resumes)

#### 1. Edit in Workspace
All edits happen in the workspace folder. Files here are **unescaped** - this is your source of truth.

#### 2. Stage ONLY Changed Files to Outbound

**CRITICAL: Only stage files that CHANGED!**

```bash
# From the workspace folder:
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/ai-privacy-guide

# Run escape script for markdown (content usually changes each iteration)
../../../tools/conversion/latex-escape-all.sh \
    ai-privacy-guide.md \
    ../../outbound/ai-privacy-guide/ai-privacy-guide.md

# Copy ONLY templates that CHANGED (not all of them!)
cp templates/p2kb-presentation.latex ../../outbound/ai-privacy-guide/

# Copy request.json ONLY if it changed
cp request.json ../../outbound/ai-privacy-guide/
```

**Decision guide for each file type:**

| File Type | When to Stage |
|-----------|---------------|
| `.md` (markdown) | Usually every iteration (content changes) |
| `.latex` (template) | Only if template structure changed |
| `.sty` (style) | Only if styling/environments changed |
| `.lua` (filter) | Only if filter logic changed |
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
outbound/ai-privacy-guide/ai-privacy-guide.tex
```
This intermediate LaTeX file is useful for:
- Correlating error line numbers to actual content
- Understanding how Pandoc transformed the markdown
- Debugging rendering issues when user provides visual feedback

### Important Notes

- **Outbound is FLAT** - No subfolders! All `.sty` and `.latex` files go at root level
- **Same filename everywhere** - `ai-privacy-guide.md` in workspace AND outbound
- **Workspace is unescaped** - Never run escape script in place; always output to outbound
- **Outbound files disappear** - This is normal; user moves them to Forge
- **Iterative process** - Expect multiple rounds of feedback and fixes

---

## Document Identity

**Document Title:** AI Privacy Guide for P2 Developers
**Subtitle:** Claude Code Privacy Guidelines
**Status:** Deferred - Not P2-related content
**Priority:** Low - Focus on P2 technical documentation first

---

## Template Stack

**Prefix:** `p2kb-presentation-*`

| File | Purpose |
|------|---------|
| `p2kb-presentation.latex` | Presentation-style template |

**Full Details:** See [templates/README.md](templates/README.md)

---

## PDF Forge Configuration (Template)

When work resumes, the `request.json` file will look like:

```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "ai-privacy-guide.md",
      "output": "ai-privacy-guide.pdf",
      "template": "p2kb-presentation",
      "pandoc_args": [
        "--pdf-engine=xelatex",
        "--toc"
      ],
      "metadata": {
        "title": "AI Privacy Guide for P2 Developers",
        "subtitle": "Claude Code Privacy Guidelines",
        "author": "Iron Sheep Productions, LLC"
      }
    }
  ]
}
```

---

## Notes

This workspace contains AI/privacy content that's not directly related to P2 microcontroller documentation. Work on this document is deferred while P2 technical documentation takes priority.

If work resumes on this document, template can be enhanced based on presentation needs.

---

*Created: 2025-09-10*
*Updated: 2025-12-03 - Restructured to match gold standard format*
*Status: Deferred - Not P2-related content*
