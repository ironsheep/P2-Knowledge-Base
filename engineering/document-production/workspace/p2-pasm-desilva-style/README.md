# Workspace - P2 PASM DeSilva Style

**Purpose:** PDF production workspace for "Discovering P2 Assembly" - a pedagogical PASM2 tutorial.

**Status:** Active - Content Development Phase
**Content Source:** `../../manuals/p2-pasm-desilva-style/opus-master/`

---

## Quick Reference

| Resource | Location |
|----------|----------|
| **Content (Opus Master)** | `../../manuals/p2-pasm-desilva-style/opus-master/` |
| **Creation Guide** | `../../manuals/p2-pasm-desilva-style/creation-guide.md` |
| **Style Guide** | `../../manuals/p2-pasm-desilva-style/desilva-style-guide.md` |
| **Escape Script** | `../../../tools/conversion/latex-escape-all.sh` |
| **Outbound Folder** | `../../outbound/p2-pasm-desilva-style/` |

---

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Critical File Naming Convention

**The master document name is sacred and never changes:**

| Purpose | Filename |
|---------|----------|
| **Master Document** | `P2-PASM-deSilva-Style.md` |
| **Output PDF** | `P2-PASM-deSilva-Style.pdf` |

**Rules:**
- Always use the exact document name - no suffixes like `-escaped`, `-v2`, `-final`
- The workspace copy is unescaped (source of truth)
- The outbound copy is escaped (ready for Forge)
- Both use the identical filename: `P2-PASM-deSilva-Style.md`
- Never rename files - always replace in place

---

## Directory Structure

```
workspace/p2-pasm-desilva-style/     ← YOU ARE HERE (unescaped source)
├── README.md                         # This file
├── P2-PASM-deSilva-Style.md          # Master document (UNESCAPED)
├── templates/
│   ├── README.md                     # Template documentation
│   ├── p2kb-desilva.latex            # Main LaTeX template
│   ├── p2kb-desilva-foundation.sty   # DeSilva-specific foundation
│   └── p2kb-desilva-content.sty      # 5-color code + pedagogical environments
├── filters/
│   └── *.lua                         # Lua filters if needed
├── request.json                      # PDF Forge configuration
├── request-requirements.json         # Mandatory pandoc arguments
└── VERSION-TRACKING.md               # Document version history

outbound/p2-pasm-desilva-style/       ← FLAT structure for PDF Forge
├── P2-PASM-deSilva-Style.md          # ESCAPED copy (same name!)
├── p2kb-desilva.latex                # Template (FLAT - no subfolder!)
├── p2kb-desilva-foundation.sty       # Style files at root level
├── p2kb-desilva-content.sty
├── *.lua                             # Filters at root level
└── request.json
```

---

## PDF Forge Workflow

### CRITICAL UNDERSTANDING: PDF Forge Persistence

**PDF Forge is a PERSISTENT system.** It retains ALL files from the last deployment indefinitely. This has major implications:

1. **Files sent to Forge DISAPPEAR from outbound** - The user MOVES (not copies) files to the Forge
2. **Forge keeps the last version of every file** - If you sent `p2kb-desilva-content.sty` last week, Forge still has it
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
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/p2-pasm-desilva-style

# Run escape script for markdown (content usually changes each iteration)
../../../tools/conversion/latex-escape-all.sh \
    P2-PASM-deSilva-Style.md \
    ../../outbound/p2-pasm-desilva-style/P2-PASM-deSilva-Style.md

# Copy ONLY templates that CHANGED (not all of them!)
# Example: If only p2kb-desilva-content.sty changed:
cp templates/p2kb-desilva-content.sty ../../outbound/p2-pasm-desilva-style/

# Copy ONLY filters that CHANGED
cp filters/*.lua ../../outbound/p2-pasm-desilva-style/

# Copy request.json ONLY if it changed
cp request.json ../../outbound/p2-pasm-desilva-style/
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
outbound/p2-pasm-desilva-style/P2-PASM-deSilva-Style.tex
```
This intermediate LaTeX file is useful for:
- Correlating error line numbers to actual content
- Understanding how Pandoc transformed the markdown
- Debugging rendering issues when user provides visual feedback

### Important Notes

- **Outbound is FLAT** - No subfolders! All `.sty` and `.latex` files go at root level
- **Same filename everywhere** - `P2-PASM-deSilva-Style.md` in workspace AND outbound
- **Workspace is unescaped** - Never run escape script in place; always output to outbound
- **Outbound files disappear** - This is normal; user moves them to Forge
- **Iterative process** - Expect multiple rounds of feedback and fixes

---

## Document Identity

**Document Title:** Discovering P2 Assembly
**Subtitle:** Build, Experiment, and Master the Propeller 2
**Status:** In Production - Content Development Phase

## Document Purpose

Creating a pedagogical PASM2 manual that captures deSilva's teaching philosophy: approachable, hands-on, and genuinely enjoyable assembly language learning.

**Teaching Philosophy:** "Learn by doing, celebrate progress, have fun!"

## Template Stack

**Prefix:** `p2kb-desilva-*`

| File | Purpose |
|------|---------|
| `p2kb-desilva.latex` | Main document template |
| `p2kb-desilva-foundation.sty` | DeSilva-specific foundation |
| `p2kb-desilva-content.sty` | 5-color code + pedagogical environments |

**Full Details:** See [templates/README.md](templates/README.md)

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

### 5-Color Code Block System
- 🟢 **Green** = Spin2 (High-level language)
- 🟡 **Yellow** = PASM2 (Assembly language)
- 🟣 **Purple** = CORDIC (Math operations)
- 🔵 **Blue** = Multi-COG (Parallel processing)
- 🔴 **Red** = Antipattern (What NOT to do)

**Purpose:** Helps learners distinguish contexts at a glance

### Pedagogical Environments
- **Sidetracks:** Optional deeper dives (gray with dashed borders)
- **Interludes:** Conceptual bridges between topics (gray, no border)
- **Your Turn:** Hands-on exercises (light blue boxes)
- **Chapter Celebrations:** Learning milestones (green tinted)
- **Medicine Cabinet:** Quick reference tips

## Content Sources & Production Method

### Primary Sources
1. **YAML Instruction Files** - `/engineering/knowledge-base/P2/language/pasm2/` - Technical accuracy
2. **Opus Master** - `/engineering/document-production/manuals/p2-pasm-desilva-style/opus-master/` - Pedagogical structure (Chapters 1-6)
3. **Pattern Extractions** - Recent pattern extraction work - Code examples and idioms
4. **Smart Pins & I/O Documentation** - For Chapter 8 basic I/O only (reference advanced features to separate manual)

### Modular Manual Strategy
- **This Manual:** Core PASM2 assembly programming with basic I/O (250-300 pages)
- **Smart Pins Manual:** Comprehensive Smart Pin modes (separate document)
- **I/O Manual:** Advanced I/O techniques (separate document - future)
- **DEBUG Manual:** Debug system reference (separate or integrated - TBD)

**Rationale:** Cognitive load management - Core PASM2 alone is substantial enough for one focused manual.


## DeSilva Teaching Approach

### Voice Characteristics
- **Encouraging:** Celebrates progress, builds confidence
- **Approachable:** Friendly tone, no intimidation
- **Hands-On:** Every concept has working code examples
- **Progressive:** Simple to complex, building on success

### Visual Pedagogy
The 5-color code system creates:
- **Context Awareness:** Instantly recognize Spin2 vs PASM2 vs CORDIC
- **Pattern Recognition:** Consistent color coding reveals patterns
- **Mistake Avoidance:** Red antipatterns highlight what not to do
- **Confidence Building:** Color progression shows learning advancement

## PDF Forge Configuration

The `request.json` file configures PDF Forge:

```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "P2-PASM-deSilva-Style.md",
      "output": "P2-PASM-deSilva-Style.pdf",
      "template": "p2kb-desilva",
      "pandoc_args": [
        "--top-level-division=part",
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2"
      ],
      "metadata": {
        "title": "Discovering P2 Assembly",
        "subtitle": "Build, Experiment, and Master the Propeller 2",
        "author": "Iron Sheep Productions, LLC"
      }
    }
  ]
}
```

Required arguments are documented in `request-requirements.json`.

---

## Code Validation

All code examples MUST be validated before inclusion:
```bash
# Validate PASM2/Spin2 code
pnut_ts filename.spin2
```

**Compiler Location:** `/engineering/tools/compiler/pnut_ts`
**Usage Guide:** `/engineering/tools/compiler/pnut_ts-usage-guide.md`

---

*Created: 2025-09-10*
*Updated: 2025-12-03 - Restructured to match gold standard format*
