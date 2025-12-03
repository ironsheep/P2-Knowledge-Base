# Workspace - P2 Single-Step Debugger Manual

**Purpose:** PDF production workspace for the P2 Single-Step Debugger Manual.

**Status:** Planned - Not Started
**Content Source:** TBD

---

## Quick Reference

| Resource | Location |
|----------|----------|
| **Escape Script** | `../../../tools/conversion/latex-escape-all.sh` |
| **Outbound Folder** | `../../outbound/p2-single-step-debugger-manual/` (when created) |
| **Related Document** | Debug Window Manual (coordinate to avoid overlap) |

---

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Critical File Naming Convention

**The master document name is sacred and never changes:**

| Purpose | Filename |
|---------|----------|
| **Master Document** | `P2-Single-Step-Debugger-Manual.md` |
| **Output PDF** | `P2-Single-Step-Debugger-Manual.pdf` |

**Rules:**
- Always use the exact document name - no suffixes like `-escaped`, `-v2`, `-final`
- The workspace copy is unescaped (source of truth)
- The outbound copy is escaped (ready for Forge)
- Both use the identical filename: `P2-Single-Step-Debugger-Manual.md`
- Never rename files - always replace in place

---

## Directory Structure

```
workspace/p2-single-step-debugger-manual/     ← YOU ARE HERE (unescaped source)
├── README.md                                  # This file
├── P2-Single-Step-Debugger-Manual.md          # Master document (when created)
├── templates/
│   ├── README.md                              # Template documentation
│   ├── p2kb-debugger.latex                    # Main LaTeX template (TBD)
│   ├── p2kb-debugger-foundation.sty           # Foundation layer (TBD)
│   └── p2kb-debugger-content.sty              # Content styling (TBD)
├── filters/
│   └── *.lua                                  # Lua filters if needed
├── request.json                               # PDF Forge configuration (TBD)
└── request-requirements.json                  # Mandatory pandoc arguments (TBD)

outbound/p2-single-step-debugger-manual/       ← FLAT structure for PDF Forge
├── P2-Single-Step-Debugger-Manual.md          # ESCAPED copy (same name!)
├── p2kb-debugger.latex                        # Template (FLAT - no subfolder!)
├── p2kb-debugger-foundation.sty               # Style files at root level
├── p2kb-debugger-content.sty
├── *.lua                                      # Filters at root level
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

### Step-by-Step Process (When Ready)

#### 1. Edit in Workspace
All edits happen in the workspace folder. Files here are **unescaped** - this is your source of truth.

#### 2. Stage ONLY Changed Files to Outbound

**CRITICAL: Only stage files that CHANGED!**

```bash
# From the workspace folder:
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/p2-single-step-debugger-manual

# Run escape script for markdown (content usually changes each iteration)
../../../tools/conversion/latex-escape-all.sh \
    P2-Single-Step-Debugger-Manual.md \
    ../../outbound/p2-single-step-debugger-manual/P2-Single-Step-Debugger-Manual.md

# Copy ONLY templates that CHANGED (not all of them!)
cp templates/p2kb-debugger-content.sty ../../outbound/p2-single-step-debugger-manual/

# Copy ONLY filters that CHANGED
cp filters/*.lua ../../outbound/p2-single-step-debugger-manual/

# Copy request.json ONLY if it changed
cp request.json ../../outbound/p2-single-step-debugger-manual/
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
outbound/p2-single-step-debugger-manual/P2-Single-Step-Debugger-Manual.tex
```
This intermediate LaTeX file is useful for:
- Correlating error line numbers to actual content
- Understanding how Pandoc transformed the markdown
- Debugging rendering issues when user provides visual feedback

### Important Notes

- **Outbound is FLAT** - No subfolders! All `.sty` and `.latex` files go at root level
- **Same filename everywhere** - `P2-Single-Step-Debugger-Manual.md` in workspace AND outbound
- **Workspace is unescaped** - Never run escape script in place; always output to outbound
- **Outbound files disappear** - This is normal; user moves them to Forge
- **Iterative process** - Expect multiple rounds of feedback and fixes

---

## Document Identity

**Document Title:** P2 Single-Step Debugger Manual (TBD)
**Status:** Planned - Not Started
**Priority:** TBD based on P2 community needs

---

## Template Recommendations

**Template Not Yet Selected.** When ready, consider:

| Starting Point | Use Case |
|----------------|----------|
| `p2kb-debugwin-*` | Visual/discovery approach (like Debug Window) |
| `p2kb-desilva-*` | Tutorial/pedagogical approach |
| `p2kb-sp-*` | Quick reference approach |

**Next Steps When Development Begins:**
1. Determine document style (tutorial vs. reference vs. visual discovery)
2. Survey existing templates in Template Catalog
3. Copy closest match to this workspace
4. Rename with `p2kb-debugger-*` prefix
5. Customize for debugger content

---

## PDF Forge Configuration (Template)

When ready, the `request.json` file will look like:

```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "P2-Single-Step-Debugger-Manual.md",
      "output": "P2-Single-Step-Debugger-Manual.pdf",
      "template": "p2kb-debugger",
      "pandoc_args": [
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2"
      ],
      "metadata": {
        "title": "P2 Single-Step Debugger Manual",
        "subtitle": "TBD",
        "author": "Iron Sheep Productions, LLC"
      }
    }
  ]
}
```

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| **Debug Window Manual** | Coordinate to avoid overlap and ensure complementary coverage |

---

*Created: 2025-09-10*
*Updated: 2025-12-03 - Restructured to match gold standard format*
*Status: Planned - Placeholder for future single-step debugger documentation*
