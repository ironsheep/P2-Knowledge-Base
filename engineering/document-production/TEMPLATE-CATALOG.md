# P2 Knowledge Base - Template Catalog

**Purpose:** Quick reference for all document templates across the P2KB project
**Last Updated:** 2025-11-23
**Template Organization:** Each workspace has its own `templates/` folder with document-specific templates

## 🎯 Quick Template Selection Guide

### By Document Type

| Need | Template | Location | Best For |
|------|----------|----------|----------|
| **Tutorial/Learning** | `p2kb-desilva-*` | `p2-pasm-desilva-style/templates/` | Pedagogical manuals with progressive learning |
| **Tutorial (Enhanced)** | `p2kb-sp-*` | `p2-smart-pins-tutorial/templates/` | Comprehensive tutorials with rich visual elements |
| **Visual Discovery** | `p2kb-debugwin-*` | `p2-debug-window-manual/templates/` | Discovery-driven docs with screenshot integration |
| **Presentation** | `p2kb-presentation-*` | `ai-privacy-guide/templates/` | Simple presentation-style documents |
| **Reference Manual** | Start from `p2kb-sp-*` | Smart Pins templates | Formal reference documentation |

### By Template Stack Complexity

| Layers | Template | Purpose |
|--------|----------|---------|
| **4-Layer** | `p2kb-sp-*` | Maximum flexibility: foundation + content + numbering + presentation |
| **2-Layer** | `p2kb-desilva-*`, `p2kb-debugwin-*` | Streamlined: foundation + content |
| **1-Layer** | `p2kb-presentation-*` | Minimal: self-contained template |

## 📚 Available Templates

### 1. Smart Pins Tutorial Templates
**Location:** `workspace/p2-smart-pins-tutorial/templates/`
**Prefix:** `p2kb-sp-*`
**Status:** ✅ Production-Ready

**Template Hierarchy:**
```
Layer 1: p2kb-foundation.sty (core infrastructure)
Layer 2: p2kb-sp-styles.sty (Smart Pins content styling)
Layer 3: p2kb-sp-numbering.sty (numbering system)
Layer 4: p2kb-tech-review.sty (presentation branding)
Main:    p2kb-sp-template.latex
```

**Features:**
- 4-layer stack for maximum modularity
- 3 code block types (Configuration, Spin2, PASM2)
- 7 semantic marker boxes with distinct borders
- Pastel color palette for extended reading
- 10.5pt body text, 1.25x line spacing
- Technical review title pages

**Best For:**
- Tutorial-style learning documents
- Documents with progressive examples
- Reference manuals with rich formatting
- Technical review phase documents

**Special Requirements:**
- Requires `--top-level-division=part` pandoc arg
- Lua filter pipeline support
- Assets folder for images

---

### 2. PASM2 DeSilva Style Templates
**Location:** `workspace/p2-pasm-desilva-style/templates/`
**Prefix:** `p2kb-desilva-*`
**Status:** ✅ Production-Ready

**Template Hierarchy:**
```
Layer 1: p2kb-desilva-foundation.sty (deSilva-specific foundation)
Layer 2: p2kb-desilva-content.sty (5-color code + pedagogy)
Main:    p2kb-desilva.latex (custom title page)
```

**Features:**
- 5-color code block system (Spin2, PASM2, CORDIC, Multi-COG, Antipattern)
- Pedagogical environments (Sidetracks, Interludes, Your Turn, Celebrations)
- Medicine Cabinet quick reference tips
- 12pt font on letter paper (tutorial-friendly)
- Two-sided layout for printed manuals
- Encouraging, approachable voice

**Best For:**
- Pedagogical assembly language manuals
- Tutorial-style programming guides
- Learn-by-doing documents
- Progressive difficulty content

**Special Requirements:**
- Requires `--top-level-division=part` pandoc arg
- Built for deSilva teaching philosophy

---

### 3. Debug Window Manual Templates
**Location:** `workspace/p2-debug-window-manual/templates/`
**Prefix:** `p2kb-debugwin-*`
**Status:** ✅ Production-Ready

**Template Hierarchy:**
```
Layer 1: p2kb-debugwin-foundation.sty (debug window foundation)
Layer 2: p2kb-debugwin-content.sty (5-color + visual discovery)
Main:    p2kb-debugwin.latex (custom title + list of figures)
```

**Features:**
- 5-color code system adapted for debug contexts
- Discovery/experiment boxes
- Screenshot integration (automatic List of Figures)
- Window type comparison tables
- Performance metric displays
- 11pt font on A4 (screen-optimized)
- Single-sided digital-first layout

**Best For:**
- Visual discovery documents
- Screenshot-heavy manuals
- Systematic feature exploration docs
- Hands-on experimentation guides

**Special Requirements:**
- Assets folder for screenshots required
- List of Figures automatically generated

---

### 4. Presentation Templates
**Location:** `workspace/ai-privacy-guide/templates/`
**Prefix:** `p2kb-presentation-*`
**Status:** 🔶 Minimal/Experimental

**Template Hierarchy:**
```
Main: p2kb-presentation.latex (self-contained)
```

**Features:**
- Clean, modern layout
- Presentation-optimized formatting
- Minimal dependencies
- Simple structure

**Best For:**
- Non-technical presentation documents
- Quick one-off documents
- Simple layout needs

**Note:** This is a minimal template. Can be enhanced based on needs.

---

## 🚧 Templates In Development

### 5. PASM2 Reference Manual Templates
**Location:** `workspace/pasm2-reference-manual/templates/`
**Prefix:** `p2kb-pasm-ref-*` (to be established)
**Status:** 🔴 Planned

**Recommended Starting Point:**
- Copy from `p2kb-sp-*` if technical reference style desired
- Copy from `p2kb-desilva-*` if approachable reference style desired

**Content Focus:**
- Formal instruction set specifications
- Quick lookup optimization
- Comprehensive instruction tables

---

### 6. Spin2 Reference Manual Templates
**Location:** `workspace/spin2-reference-manual/templates/`
**Prefix:** `p2kb-spin2-ref-*` (to be established)
**Status:** 🔴 Planned

**Recommended Starting Point:**
- Copy from `p2kb-sp-*` or `p2kb-desilva-*`
- Coordinate style with PASM2 Reference if both are formal

**Content Focus:**
- Language syntax and semantics
- Built-in function reference
- Object-oriented features
- Inline PASM2 integration

---

### 7. Single-Step Debugger Templates
**Location:** `workspace/p2-single-step-debugger-manual/templates/`
**Prefix:** `p2kb-debugger-*` (to be established)
**Status:** 🔴 Planned

**Recommended Starting Point:**
- `p2kb-debugwin-*` if visual/discovery approach
- `p2kb-desilva-*` if tutorial approach
- `p2kb-sp-*` if reference approach

**Content Focus:** TBD based on document approach

---

## 🔧 Template Usage Workflow

### For New Documents

1. **Review this catalog** - Find closest template match
2. **Copy template folder:**
   ```bash
   cp -r workspace/[source-doc]/templates/* workspace/[new-doc]/templates/
   ```
3. **Rename files** with new prefix:
   ```bash
   # Example: p2kb-sp-* → p2kb-mynew-*
   cd workspace/[new-doc]/templates/
   for f in p2kb-sp-*; do mv "$f" "${f/p2kb-sp-/p2kb-mynew-}"; done
   ```
4. **Update template/README.md** - Document new template hierarchy
5. **Update workspace/README.md** - Point to new templates
6. **Evolve independently** - No shared dependencies!

### For Existing Documents

Each workspace `templates/` folder contains:
- Template files (`.latex`, `.sty`)
- `README.md` documenting hierarchy and usage

**See workspace-specific `templates/README.md` for detailed implementation.**

---

## 📋 Template Naming Convention

**Pattern:** `p2kb-[document-identifier]-[layer].[ext]`

### Examples:
- `p2kb-sp-foundation.sty` - Smart Pins foundation layer
- `p2kb-desilva-content.sty` - DeSilva content layer
- `p2kb-debugwin.latex` - Debug Window main template

### Naming Rules:
- ✅ Always start with `p2kb-` prefix
- ✅ Use document-specific identifier (sp, desilva, debugwin)
- ✅ Indicate layer if multi-layer (foundation, content, presentation)
- ✅ Use `.latex` for main templates, `.sty` for packages
- ❌ No version numbers (v1, v2, etc.)
- ❌ No status suffixes (draft, fixed, old)

---

## 🎨 Common Template Features

### All Templates Provide:
- Pandoc integration (variables, metadata)
- LaTeX character escaping compatibility
- PDF generation via PDF Forge
- request.json configuration support

### Common Visual Elements:
- **Code Blocks:** Language-specific styling
- **Colored Boxes:** Semantic content markers
- **Typography:** Professional fonts (Charter, Palatino)
- **Page Layout:** Optimized for digital or print

### Common Layers (When Present):
- **Foundation:** Pandoc compatibility, basic document structure, colors
- **Content:** Document-specific styling, colored boxes, code blocks
- **Presentation:** Branding, title pages, headers/footers

---

## 🔍 Quick Selection Decision Tree

```
Need a template?
├─ Tutorial/Learning?
│  ├─ With rich pedagogy? → p2kb-desilva-*
│  └─ With visual elements? → p2kb-sp-*
├─ Visual/Discovery?
│  └─ Screenshots/exploration? → p2kb-debugwin-*
├─ Reference Manual?
│  └─ Start from p2kb-sp-* (adapt as needed)
└─ Simple/Presentation?
   └─ p2kb-presentation-*
```

---

## 📝 Template Evolution Philosophy

**Every template is document-specific:**
- Templates live in workspace `templates/` folders
- No shared template dependencies
- Templates evolve with their documents
- Improvements stay within workspace
- Copy and adapt for new documents

**Benefits:**
- No shared modification friction
- Each document controls its own visual identity
- Templates improve through document iteration
- Clear ownership and evolution path

---

## 🔗 Related Documentation

- **Universal PDF Process:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`
- **Document Pipeline:** `/engineering/document-production/README.md`

---

**Status Legend:**
- ✅ Production-Ready - Proven templates used in active documents
- 🔶 Minimal/Experimental - Basic template, can be enhanced
- 🔴 Planned - Not yet created, use production templates as starting point
