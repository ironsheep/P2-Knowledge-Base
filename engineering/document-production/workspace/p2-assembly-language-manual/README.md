# Workspace - P2 Assembly Language Manual

**Purpose:** PDF production workspace for the P2 Assembly Language (PASM2) Reference Manual.

**Status:** Active
**Content Source:** `../../manuals/p2-assembly-language-manual/opus-master/`

---

## Quick Reference

| Resource | Location |
|----------|----------|
| **Content (Opus Master)** | `../../manuals/p2-assembly-language-manual/opus-master/` |
| **Creation Guide** | `../../manuals/p2-assembly-language-manual/creation-guide.md` |
| **Style Guide** | `../../manuals/p2-assembly-language-manual/style-guide.md` |
| **Voice Guide** | `../../manuals/p2-assembly-language-manual/voice-guide.md` |
| **Sprint Plan** | `../../manuals/p2-assembly-language-manual/sprint/PASM2-MANUAL-GENERATION-SPRINT.md` |
| **Escape Script** | `../../../tools/conversion/latex-escape-all.sh` |
| **Outbound Folder** | `../../outbound/p2-assembly-language-manual/` |

---

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production (font configuration, Pandoc quirks, pagination problems) that will save significant debugging time.

---

## Critical File Naming Convention

**The master document name is sacred and never changes:**

| Purpose | Filename |
|---------|----------|
| **Master Document** | `P2-Assembly-Language-Manual.md` |
| **Output PDF** | `P2-Assembly-Language-Manual.pdf` |

**Rules:**
- Always use the exact document name - no suffixes like `-escaped`, `-v2`, `-final`
- The workspace copy is unescaped (source of truth)
- The outbound copy is escaped (ready for Forge)
- Both use the identical filename: `P2-Assembly-Language-Manual.md`
- Never rename files - always replace in place

---

## Directory Structure

```
workspace/p2-assembly-language-manual/     ← YOU ARE HERE (unescaped source)
├── README.md                              # This file
├── P2-Assembly-Language-Manual.md         # Master document (UNESCAPED)
├── templates/
│   ├── README.md                          # Template documentation
│   ├── p2kb-pasm2-reference.latex         # Main LaTeX template
│   ├── p2kb-pasm2-foundation.sty          # Pandoc compatibility layer
│   ├── p2kb-pasm2-content.sty             # Reference manual environments
│   └── p2kb-pasm2-diagrams.sty            # TikZ diagram macros (24 diagrams)
├── filters/
│   └── (Lua filters if needed)
├── assets/
│   └── (External images if needed)
├── request.json                           # PDF Forge configuration
├── request-requirements.json              # Mandatory pandoc arguments
└── VERSION-TRACKING.md                    # Document version history

outbound/p2-assembly-language-manual/      ← FLAT structure for PDF Forge
├── P2-Assembly-Language-Manual.md         # ESCAPED copy (same name!)
├── p2kb-pasm2-reference.latex             # Template (FLAT - no subfolder!)
├── p2kb-pasm2-foundation.sty              # Style files at root level
├── p2kb-pasm2-content.sty
├── p2kb-pasm2-diagrams.sty
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
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/p2-assembly-language-manual

# Run escape script (creates backup automatically)
../../../tools/conversion/latex-escape-all.sh \
    P2-Assembly-Language-Manual.md \
    ../../outbound/p2-assembly-language-manual/P2-Assembly-Language-Manual.md

# Copy ONLY CHANGED templates FLAT (no subfolder!) to outbound
# Example: If only p2kb-pasm2-content.sty changed:
cp templates/p2kb-pasm2-content.sty ../../outbound/p2-assembly-language-manual/

# Copy ONLY CHANGED filters to outbound
# Example: If a new filter was added:
cp filters/p2kb-pasm2-tables.lua ../../outbound/p2-assembly-language-manual/

# Copy request.json ONLY if it changed
cp request.json ../../outbound/p2-assembly-language-manual/
```

**What to copy each iteration:**
- `P2-Assembly-Language-Manual.md` - Always (content changes)
- Template files (`.latex`, `.sty`) - Only if modified
- Lua filters (`.lua`) - Only if modified or added
- `request.json` - Only if configuration changed

#### 3. User Deploys to PDF Forge
The user hand-copies files from `outbound/p2-assembly-language-manual/` to PDF Forge.
**Files will disappear from outbound** after being moved to the Forge.

#### 4. Feedback Loop
- If PDF Forge reports errors → User relays error messages → Fix in workspace → Re-escape → Repeat
- If PDF generates successfully → User provides visual feedback → Fix in workspace → Re-escape → Repeat
- Continue until PDF is correct

#### 5. Debugging with Generated .tex File
After each PDF Forge run, the user will drop the generated `.tex` file into the outbound directory:
```
outbound/p2-assembly-language-manual/P2-Assembly-Language-Manual.tex
```
This intermediate LaTeX file is useful for:
- Correlating error line numbers to actual content
- Understanding how Pandoc transformed the markdown
- Debugging rendering issues when user provides visual feedback
- Finding the exact LaTeX that produced problematic output

### Important Notes

- **Outbound is FLAT** - No subfolders! All `.sty` and `.latex` files go at root level
- **Same filename everywhere** - `P2-Assembly-Language-Manual.md` in workspace AND outbound
- **Workspace is unescaped** - Never run escape script in place; always output to outbound
- **Outbound files disappear** - This is normal; user moves them to Forge
- **Iterative process** - Expect multiple rounds of feedback and fixes

---

## Content Assembly

### CRITICAL: Always Use the Assembly Script

**NEVER use raw `cat` commands to assemble the manual.**

**ALWAYS use the assembly script:**

```bash
# From the workspace folder:
cd /workspaces/P2-Knowledge-Base/engineering/document-production/workspace/p2-assembly-language-manual

# Run the assembly script
./assemble-manual.sh
```

**Why?** The assembly script does much more than concatenate files:
- Verifies ALL required source files exist before starting
- Adds proper Part I/II/III section markers with correct pagination control
- Ensures proper spacing between assembled sections
- Provides detailed logging of what's being assembled
- Reports statistics (line counts, file counts) for verification

**What the script produces that `cat` doesn't:**
- Part I marker: `# Part I: Architectural Foundation`
- Part II marker: `# Part II: Instruction Set Reference`
- Part III marker: `# Part III: Reference Tables`
- Proper blank lines between sections for clean LaTeX output

### Assembly Output

After running the script, you'll see:
```
========================================
PASM2 Manual Assembly Script
========================================

Verifying source files...
  All source files verified!

Assembling manual...
  Adding: Front Matter
  Adding: Part I marker
  Adding: Chapter 1: Execution Model
  ...
  Adding: Part III marker
  Adding: Appendix A: Encoding Table
  ...

========================================
Assembly Complete!
========================================

Output file: P2-Assembly-Language-Manual.md
Total lines: ~19,500
Source files included: 38
```

### Historical Note

Early development used raw `cat` commands, but this approach:
- Missed Part markers (breaking TOC navigation)
- Didn't verify source files existed
- Provided no feedback during assembly
- Made it easy to accidentally skip files

The assembly script was created to prevent these issues.

---

## Template Stack

| File | Purpose | Lines |
|------|---------|-------|
| `p2kb-pasm2-reference.latex` | Main document template | ~70 |
| `p2kb-pasm2-foundation.sty` | Pandoc compatibility, fonts, headers | ~270 |
| `p2kb-pasm2-content.sty` | Reference manual environments, callouts | ~320 |
| `p2kb-pasm2-diagrams.sty` | TikZ diagram macros (24 diagrams) | ~1600 |

See `templates/README.md` for detailed template and diagram documentation.

---

## PDF Forge Configuration

The `request.json` file configures PDF Forge:

```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "P2-Assembly-Language-Manual.md",
      "output": "P2-Assembly-Language-Manual.pdf",
      "template": "p2kb-pasm2-reference",
      "pandoc_args": [
        "--top-level-division=chapter",
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2"
      ],
      "metadata": {
        "title": "P2 Assembly Language Reference Manual",
        "subtitle": "Complete PASM2 Instruction Set Documentation",
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

## Release Process

When a PDF is ready for distribution:

### 1. Update Version in Source Files

**Changelog** (in opus-master):
```
../../manuals/p2-assembly-language-manual/opus-master/CHANGELOG.md
```
- Add new version section at top (e.g., `## v1.1.0 (2025-12-12)`)
- Document all changes since last release

**request.json** (in workspace):
- Update `metadata.version` field to match (e.g., `"Version 1.1.0"`)

### 2. Promote to Deliverables

After PDF Forge generates the final PDF:

```bash
# Deliverables folder (at repository root)
DOCS="/workspaces/P2-Knowledge-Base/deliverables/documents/DOCs"

# Copy PDF (user provides from PDF Forge output)
cp <path-to-generated-pdf> "$DOCS/P2-Assembly-Language-Manual.pdf"

# Copy changelog
cp ../../manuals/p2-assembly-language-manual/opus-master/CHANGELOG.md \
   "$DOCS/p2-assembly-language-manual-changelog.md"
```

### 3. Deliverables Structure

```
deliverables/documents/DOCs/
├── P2-Assembly-Language-Manual.pdf           # Latest PDF
└── p2-assembly-language-manual-changelog.md  # Cumulative changelog
```

**Naming Convention:**
- Filenames are **versionless** - always the same name
- Version numbers live **inside** the documents (PDF title page, changelog headers)
- Git provides version history - checkout any tag to get that release
- Changelog is cumulative - newest version at top

### 4. Tag the Release

```bash
git add .
git commit -m "Release p2-assembly-language-manual v1.1.0"
git tag -a p2-assembly-language-manual-v1.1.0 -m "P2 Assembly Language Manual v1.1.0"
```

---

*Created: 2025-11-28*
*Updated: 2025-12-01 - Added PDF Forge workflow, file naming conventions*
*Updated: 2025-12-12 - Added Release Process section*
*Sprint: PASM2 Manual Generation*
