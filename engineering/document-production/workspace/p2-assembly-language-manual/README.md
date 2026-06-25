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

**Rendering-stack note (migrated 2026-06-10 onto the shared platform stack).** This
manual no longer carries a bespoke `p2kb-pasm2-foundation/-content.sty` fork. It now
loads the **shared platform** `.sty`/`.lua` from `../../platform/`, plus a thin
per-manual fork (`p2kb-pasm2-local.sty`, `p2kb-pasm2-diagrams.sty`, and the
`p2kb-pasm2-entry-*` filters). The shared platform files are staged to outbound by
`prepare-manual` only when their content changes.

```
workspace/p2-assembly-language-manual/     ← YOU ARE HERE (unescaped source)
├── README.md                              # This file
├── P2-Assembly-Language-Manual.md         # Master document (UNESCAPED, assembled)
├── templates/                             # Per-manual fork files only
│   ├── README.md                          # Template documentation
│   ├── p2kb-pasm2-reference.latex         # Main LaTeX template (loads platform + local + diagrams)
│   ├── p2kb-pasm2-local.sty               # PASM2 reference apparatus (loaded AFTER platform)
│   └── p2kb-pasm2-diagrams.sty            # TikZ diagram macros
├── filters/                               # Per-manual fork Lua filters
│   ├── p2kb-pasm2-entry-format.lua        # ACTIVE (in request.json)
│   └── p2kb-pasm2-entry-headers.lua       # ACTIVE (in request.json)
│   (other p2kb-pasm2-*.lua here are pre-migration leftovers — request.json
│    uses the platform versions; safe to remove as a separate cleanup)
├── assets/
│   └── (External images if needed)
├── request.json                           # PDF Forge configuration
└── request-requirements.json              # Mandatory pandoc arguments

../../platform/                            ← SHARED rendering stack (consumed by many manuals)
├── templates/p2kb-platform-foundation.sty # Geometry, fonts, headers, glyph fallbacks
├── templates/p2kb-platform-content.sty    # Code-box family, callouts, part mechanism
└── filters/p2kb-platform-{figures,tables,mnemonic-bold,code-coloring,pagination}.lua

outbound/p2-assembly-language-manual/      ← FLAT structure for PDF Forge (stage ONLY changed files)
├── P2-Assembly-Language-Manual.md         # ESCAPED copy (same name!) — always staged
├── p2kb-pasm2-reference.latex             # Per-manual fork files (FLAT — no subfolders!)
├── p2kb-pasm2-local.sty                   #   staged only when changed
├── p2kb-pasm2-diagrams.sty
├── p2kb-pasm2-entry-format.lua
├── p2kb-pasm2-entry-headers.lua
├── p2kb-platform-foundation.sty           # Shared platform files (from ../../platform/),
├── p2kb-platform-content.sty              #   staged only when their content hash changes
├── p2kb-platform-{figures,tables,mnemonic-bold,code-coloring,pagination}.lua
└── request.json                           # staged on version bump or a document switch
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

# Copy ONLY CHANGED per-manual fork templates FLAT (no subfolder!) to outbound
# Example: If only p2kb-pasm2-local.sty changed:
cp templates/p2kb-pasm2-local.sty ../../outbound/p2-assembly-language-manual/

# Copy ONLY CHANGED per-manual fork filters to outbound
# Example: If p2kb-pasm2-entry-format.lua changed:
cp filters/p2kb-pasm2-entry-format.lua ../../outbound/p2-assembly-language-manual/

# Copy ONLY CHANGED shared platform files (from ../../platform/), e.g. a glyph fix:
cp ../../platform/templates/p2kb-platform-foundation.sty ../../outbound/p2-assembly-language-manual/

# Copy request.json ONLY if it changed (version bump) or on a document switch
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
Total lines: ~21,900
Source files included: 42
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

The reference template loads, in order: the two shared **platform** `.sty` first, then
the two per-manual **fork** `.sty` (so the fork's reference apparatus and overrides win).

| File | Stack | Purpose |
|------|-------|---------|
| `p2kb-pasm2-reference.latex` | fork | Main document template (loads the stack below) |
| `p2kb-platform-foundation.sty` | shared | Geometry, fonts, headers, penalties, glyph fallbacks |
| `p2kb-platform-content.sty` | shared | Code-box family, callouts, continuation markers, part mechanism |
| `p2kb-pasm2-local.sty` | fork | PASM2 reference apparatus (loaded AFTER platform) |
| `p2kb-pasm2-diagrams.sty` | fork | TikZ diagram macros |

Shared platform files live in `../../platform/templates/`; fork files live in this
workspace's `templates/`. See `templates/README.md` for detailed diagram documentation.

---

## PASM2 Code Block Guidelines

Code boxes use a monospace Verbatim environment and **do not wrap** — an over-long code
line is an authorship defect, not a template concern. **No overflow is acceptable.**

| Constraint | Value | Notes |
|------------|-------|-------|
| **Max code columns (K)** | 76 characters | Calibrated for the platform code box; the hard gate |

The authoritative budget is the `**Max code columns (K): 76**` line in
`../../manuals/p2-assembly-language-manual/creation-guide.md`. `prepare-manual` enforces it
before staging via `engineering/tools/validation/audit-code-line-length.py` (exit 1 = stop).

**Comment length tips:**
- Instruction + operands typically use 30-40 characters
- Leaves ~36-46 characters for comments within K=76
- For longer explanations, move the comment to full line(s) above, or split it with a
  continuation comment aligned to the inline `'` column — never a typeset wrap

**Example well-formatted line (76 chars):**
```
.loop           testp   tx_pin          wc      ' Local: .loop, send
```

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
      "lua_filters": [
        "p2kb-platform-figures",
        "p2kb-platform-tables",
        "p2kb-platform-mnemonic-bold",
        "p2kb-platform-code-coloring",
        "p2kb-pasm2-entry-format",
        "p2kb-pasm2-entry-headers",
        "p2kb-platform-pagination"
      ],
      "metadata": {
        "title": "P2 Assembly Language Reference Manual",
        "subtitle": "Complete PASM2 Instruction Set Documentation",
        "author": "Iron Sheep Productions, LLC",
        "version": "v3.1.0",
        "date": "June 2026"
      }
    }
  ]
}
```

The `lua_filters` run in order — the shared `p2kb-platform-*` filters plus the two
per-manual `p2kb-pasm2-entry-*` filters that format instruction entries.

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
- Update `metadata.version` field to match (e.g., `"v3.1.0"`) and `metadata.date`
- Also update the cover-page version/date in `opus-master/front-matter.md` (the visible
  cover renders from the markdown, not from `request.json` metadata)

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
*Updated: 2026-06-25 - Refreshed rendering-stack docs for the 2026-06-10 platform migration (platform .sty/.lua + thin pasm2 fork); corrected code budget to K=76*
*Sprint: PASM2 Manual Generation*
