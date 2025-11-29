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

---

## Directory Structure

```
p2-assembly-language-manual/
├── README.md                           # This file
├── P2-Assembly-Language-Manual.md      # Assembled master document
├── templates/
│   ├── README.md                       # Template stack documentation
│   ├── p2kb-pasm2-reference.latex      # Main LaTeX template
│   └── p2kb-pasm2-diagrams.sty         # TikZ diagram macro definitions
├── filters/
│   └── (Lua filters if needed)
├── assets/
│   └── (External images if needed)
├── request.json                        # PDF Forge configuration
├── request-requirements.json           # Mandatory pandoc arguments
└── VERSION-TRACKING.md                 # Document version history
```

---

## Workflow

### 1. Content Creation (Opus Master)
All markdown content is created in the Opus Master folder.

### 2. Assembly
Combine Opus Master files into single document:
```bash
# From opus-master directory:
cat front-matter.md \
    part-i/chapter-*.md \
    part-ii/instructions-*.md \
    part-ii/directives.md \
    part-ii/constants.md \
    part-ii/special-registers.md \
    part-iii/appendix-*.md \
    > ../../workspace/p2-assembly-language-manual/P2-Assembly-Language-Manual.md
```

### 3. PDF Generation
Deploy to PDF Forge:
1. Copy assembled markdown to PDF Forge
2. Copy templates/ contents to PDF Forge
3. Copy request.json to PDF Forge
4. Run PDF generation

---

## Template Stack

The LaTeX template system consists of:

| File | Purpose |
|------|---------|
| `p2kb-pasm2-reference.latex` | Main template with document structure, colors, environments |
| `p2kb-pasm2-diagrams.sty` | TikZ macro definitions for encoding diagrams, memory maps, bit fields |

See `templates/README.md` for detailed template documentation.

---

## PDF Forge Configuration

The `request.json` file configures PDF Forge:

```json
{
  "input_file": "P2-Assembly-Language-Manual.md",
  "output_file": "P2-Assembly-Language-Manual.pdf",
  "template": "p2kb-pasm2-reference.latex",
  "pandoc_args": [
    "--pdf-engine=xelatex",
    "--toc",
    "--toc-depth=3"
  ]
}
```

Required arguments are documented in `request-requirements.json`.

---

*Created: 2025-11-28*
*Sprint: PASM2 Manual Generation*
