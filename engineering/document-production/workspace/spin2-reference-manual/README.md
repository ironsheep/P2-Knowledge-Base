# Workspace - Spin2 Reference Manual

**Purpose:** PDF production workspace for the Spin2 Language Reference Manual.

**Status:** Planned - Early Stage
**Content Source:** TBD (YAML language files when available)

---

## Quick Reference

| Resource | Location |
|----------|----------|
| **YAML Sources (if available)** | `/engineering/knowledge-base/P2/language/spin2/` |
| **Escape Script** | `../../../tools/conversion/latex-escape-all.sh` |
| **Outbound Folder** | `../../outbound/spin2-reference-manual/` |

---

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Critical File Naming Convention

**The master document name is sacred and never changes:**

| Purpose | Filename |
|---------|----------|
| **Master Document** | `Spin2-Reference-Manual.md` |
| **Output PDF** | `Spin2-Reference-Manual.pdf` |

**Rules:**
- Always use the exact document name - no suffixes like `-escaped`, `-v2`, `-final`
- The workspace copy is unescaped (source of truth)
- The outbound copy is escaped (ready for Forge)
- Both use the identical filename: `Spin2-Reference-Manual.md`
- Never rename files - always replace in place

---

## Directory Structure

```
workspace/spin2-reference-manual/     ← YOU ARE HERE (unescaped source)
├── README.md                          # This file
├── Spin2-Reference-Manual.md          # Master document (UNESCAPED) - when created
├── templates/
│   ├── README.md                      # Template documentation
│   ├── p2kb-spin2-reference.latex     # Main LaTeX template (TBD)
│   ├── p2kb-spin2-foundation.sty      # Foundation layer (TBD)
│   └── p2kb-spin2-content.sty         # Content styling (TBD)
├── filters/
│   └── *.lua                          # Lua filters if needed
├── request.json                       # PDF Forge configuration (TBD)
└── request-requirements.json          # Mandatory pandoc arguments (TBD)

outbound/spin2-reference-manual/       ← FLAT structure for PDF Forge
├── Spin2-Reference-Manual.md          # ESCAPED copy (same name!)
├── p2kb-spin2-reference.latex         # Template (FLAT - no subfolder!)
├── p2kb-spin2-foundation.sty          # Style files at root level
├── p2kb-spin2-content.sty
├── *.lua                              # Filters at root level
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
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/spin2-reference-manual

# Run escape script for markdown (content usually changes each iteration)
../../../tools/conversion/latex-escape-all.sh \
    Spin2-Reference-Manual.md \
    ../../outbound/spin2-reference-manual/Spin2-Reference-Manual.md

# Copy ONLY templates that CHANGED (not all of them!)
cp templates/p2kb-spin2-content.sty ../../outbound/spin2-reference-manual/

# Copy ONLY filters that CHANGED
cp filters/*.lua ../../outbound/spin2-reference-manual/

# Copy request.json ONLY if it changed
cp request.json ../../outbound/spin2-reference-manual/
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
outbound/spin2-reference-manual/Spin2-Reference-Manual.tex
```
This intermediate LaTeX file is useful for:
- Correlating error line numbers to actual content
- Understanding how Pandoc transformed the markdown
- Debugging rendering issues when user provides visual feedback

### Important Notes

- **Outbound is FLAT** - No subfolders! All `.sty` and `.latex` files go at root level
- **Same filename everywhere** - `Spin2-Reference-Manual.md` in workspace AND outbound
- **Workspace is unescaped** - Never run escape script in place; always output to outbound
- **Outbound files disappear** - This is normal; user moves them to Forge
- **Iterative process** - Expect multiple rounds of feedback and fixes

---

## Document Identity

**Document Title:** Spin2 Reference Manual (TBD)
**Document Type:** Language Reference Manual
**Target Audience:** Spin2 programmers (beginners to advanced)

---

## Template Recommendations

**Template Not Yet Selected.** When ready, consider:

| Starting Point | Use Case |
|----------------|----------|
| `p2kb-sp-*` templates | Technical reference approach |
| `p2kb-desilva-*` templates | Approachable reference approach |
| Coordinate with PASM2 Reference | If both manuals should share visual style |

**Key Decisions Needed:**
1. Formal language specification vs. practical reference?
2. Target audience: beginners vs. experienced programmers?
3. Cross-referencing strategy with PASM2 manual?

---

## Content Characteristics

When development begins, the manual should cover:

- Language syntax and semantics
- Built-in functions and operators
- Object-oriented features (objects, methods, properties)
- Inline PASM2 integration
- Standard library documentation
- Code examples (Spin2 and mixed Spin2/PASM2)

**Key Differentiator:** Spin2 is the high-level language, PASM2 is the assembly language. This manual should emphasize:
- Language-level abstractions
- Object-oriented features unique to Spin2
- How to effectively use inline PASM2
- When to use Spin2 vs. drop to PASM2

---

## PDF Forge Configuration (Template)

When ready, the `request.json` file will look like:

```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "Spin2-Reference-Manual.md",
      "output": "Spin2-Reference-Manual.pdf",
      "template": "p2kb-spin2-reference",
      "pandoc_args": [
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2"
      ],
      "metadata": {
        "title": "Spin2 Reference Manual",
        "subtitle": "Complete Spin2 Language Documentation",
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
| **PASM2 Reference** | Coordinate inline assembly coverage |
| **PASM DeSilva** | Coordinate Spin2/PASM2 examples |

---

*Created: 2025-09-10*
*Updated: 2025-12-03 - Restructured to match gold standard format*
*Status: Planned - Template infrastructure ready, content development not begun*
