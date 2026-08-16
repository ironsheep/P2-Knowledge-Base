# Engineering & Deliverables Structure Guide

> Complete map of the P2 Knowledge Base repository structure
> Last Updated: 2025-09-28

## 🎯 Repository Overview

The repository is organized into two main trees:
- **`deliverables/`** - User-facing documentation (what people consume)
- **`engineering/`** - Internal systems and processes (how we create)

---

## 📦 DELIVERABLES TREE
*User-facing documentation organized by audience*

### `/deliverables/ai-reference/`
**Purpose**: AI/LLM-optimized documentation for code generation
- `README.md` - Entry point for AI systems
- `p2-claude-knowledge/` - Claude-specific knowledge structures
- `schemas/` - JSON schemas for P2 architecture, PASM2, Spin2
- `versions/` - Versioned JSON reference files
  - `v0.1.0/` - Current release (65% PASM2 coverage)
- `v1.0/` - Next major release preparation
- `pasm2-knowledge-synthesis.md` - Instruction set synthesis

### `/deliverables/developer-docs/`
**Purpose**: Quick-start guides for human developers
- `START-HERE.md` - Primary entry point for developers

### `/deliverables/learning-paths/`
**Purpose**: Structured tutorials and migration guides
- `01-fundamentals/` - Getting started with P2
- `p1-to-p2-migration-framework.md` - For P1 developers

---

## 🛠️ ENGINEERING TREE
*Internal systems for creating and maintaining documentation*

## 📚 The Three-Folder Document Pattern

Every document in production follows this consistent pattern with canonical naming:

### 1. **`manuals/[canonical-name]/`** - The Blueprint
- `creation-guide.md` - Contains `canonical_name:` field and creation instructions
- `assets/` - Static images and resources that don't change
- Style guides and formatting specifications
- NO working markdown files (those go in workspace)

### 2. **`workspace/[canonical-name]/`** - Active Development
- Working markdown files being edited
- Backups and iterations during development
- Work in progress until ready for production

### 3. **`outbound/[canonical-name]/`** - Ready for PDF
- Final escaped markdown ready for PDF generation
- LaTeX templates and request.json configured
- Deploy to PDF Forge from here (the "shipping dock")

**Canonical Names** ensure consistency across all three folders. Each document has ONE canonical name used everywhere.

### Current Canonical Names

**Not listed here.** `engineering/document-production/PUBLICATION-ROSTER.md` is the single
authority: every document appears there exactly once, under its lifecycle status
(Done / In progress / Upcoming / Abandoned) and with its Type. This file used to keep a
second copy, which is how it came to advertise a retired document as current.

---

### `/engineering/document-production/`
**Purpose**: Creating user-facing documentation

#### **Work Modes** (`work-modes/`)
*Quick reference guides for specific tasks*
- `desilva-manual-mode.md` - Working on deSilva-style manual
- `smart-pins-visual-refinement.md` - Smart Pins visual formatting
- `latex-escape-script-management.md` - LaTeX escaping workflow
- `pdf-generation-template-debugging.md` - Template debugging

#### **Methodology** (`methodology/`)
*Detailed process documentation*
- `document-generation-process.md` - Complete generation checklist
- `pdf-generation-methodology.md` - PDF creation process
- `pdf-generation-format-guide.md` - Formatting standards
- `p2kb-document-production-process.md` - Production pipeline

#### **Workspace** (`workspace/`)
*Active document development*
- `desilva-manual/` - P2-for-P1 guide development
- `smart-pins-manual/` - Smart Pins documentation
- `pasm2-user-manual/` - PASM2 reference manual
- `p2-debug-window-system-manual/` - Debug system docs

#### **Outbound** (`outbound/`)
*Documents ready for PDF generation*
- `P2-PASM-deSilva-Style/` - deSilva manual for PDF Forge
- `P2-Smart-Pins-Green-Book/` - Smart Pins tutorial
- `P2-Smart-Pins-Reference/` - Smart Pins reference

#### **Shared Assets** (`shared-assets/`)
- `templates/` - LaTeX templates (.latex, .sty files)
- `filters/` - Lua filters for pandoc

---

### `/engineering/ingestion/`
**Purpose**: Processing source documents into knowledge base

#### **Work Modes** (`work-modes/`)
*Quick reference for ingestion tasks*
- `document-ingestion-focused.md` - Ingesting new documents
- `image-extraction-focused.md` - Extracting images

#### **Methodology** (`methodology/`)
*Detailed ingestion processes*
- `source-ingestion-methodology.md` - Master ingestion process
- `image-extraction-methodology.md` - Image extraction process
- `source-code-extraction-methodology.md` - Code extraction
- `enhanced-source-code-ingestion-methodology.md` - Advanced extraction
- `focused-extraction-methodology.md` - Targeted extraction
- `pasm2-instruction-clarification-methodology.md` - Instruction docs

#### **Sources** (`sources/`)
*Ingested source documents*
- Each source has its own folder with:
  - `original/` - Source PDFs/documents
  - `assets/` - Extracted images and code
  - `*.md` - Extraction audit files

#### **Pipeline** (`pipeline/`)
*Ingestion pipeline documentation*

#### **External Inputs** (`external-inputs/`)
*Documents from external sources (Google Docs, etc.)*

---

### `/engineering/pdf-forge/`
**Purpose**: PDF generation system interface

#### **Work Modes** (`work-modes/`)
- `automated-pdf-testing.md` - Automated testing workflow

#### **Key Directories**
- `inbound/` - Files going TO PDF Forge
- `production/` - Active PDF generation projects
- `reference/` - Reference files FROM PDF Forge
- `scripts/` - Automation scripts
- `testing/` - Test configurations
- `forge-state/` - PDF Forge system state

#### **Key Documents**
- `PRODUCTION-REQUEST-FORMAT.md` - Production request.json format
- `TESTING-REQUEST-FORMAT.md` - Testing request format
- `TEMPLATE-VERIFICATION-CHECKLIST.md` - Template QA

---

### `/engineering/operations/`
**Purpose**: Project management and governance

#### **Directories**
- `migration/` - Repository reorganization tracking
  - `mapping.csv` - All 269 file moves documented
- `project-guidance/` - Project standards and decisions
- `claude-guidance/` - AI collaboration guidelines
- `standards/` - Documentation standards

---

### `/engineering/history/`
**Purpose**: Project history and completed work
- `sprints/` - Completed sprint documentation
- `releases/` - Release history
- `sessions/` - Work session logs

---

### `/engineering/pipelines/`
**Purpose**: Pipeline templates and processes
- `pdf-formatting-decisions.md` - Formatting choices

---

### `/engineering/tools/`
**Purpose**: Scripts and utilities
- `compiler/` - P2 compiler tools (pnut_ts)
- `latex-escape-all.sh` - LaTeX character escaping

---

### `/engineering/testing/`
**Purpose**: Test infrastructure and results

---

### `/engineering/planning/`
**Purpose**: Future work planning

---

### `/engineering/standards/`
**Purpose**: Documentation and code standards

---

### `/engineering/workspace/`
**Purpose**: General working area for development

---

### `/engineering/knowledge-base/`
**Purpose**: Core knowledge structures and matrices

---

## 📋 MANIFEST SYSTEM STRUCTURE
*How knowledge is organized and referenced*

### Manifest Tree Structure
```
manifests/
├── propeller-knowledge-root.yaml    # Universal entry point
└── P2/                              # P2-specific manifests
    ├── p2-root.yaml                 # P2 entry with registry
    ├── architecture-manifest.yaml   # Hardware architecture
    ├── hardware-manifest.yaml       # Boards and modules  
    ├── patterns-manifest.yaml       # Code patterns
    ├── smart-pins-manifest.yaml     # Smart Pin modes
    ├── language/                    # Language manifests
    │   ├── language-manifest.yaml   # Language hub
    │   ├── pasm2-manifest.yaml      # 376 PASM2 instructions
    │   ├── spin2-manifest.yaml      # Spin2 methods
    │   └── fundamentals-manifest.yaml
    └── community/                   # Community resources
        ├── community-manifest.yaml  
        └── obex-manifest.yaml       # 113 OBEX objects
```

### Knowledge Base Tree Structure
```
engineering/knowledge-base/P2/
├── architecture/                    # Hardware subsystems
│   ├── cog.yaml                    # COG processor details
│   ├── lookup_ram.yaml             # LUT RAM
│   ├── smart_pins.yaml             # Smart Pin overview
│   └── ...
├── language/
│   ├── pasm2/                      # 376 instruction files
│   │   ├── abs.yaml               # ABS instruction
│   │   ├── add.yaml               # ADD instruction
│   │   └── ...
│   ├── spin2/                      # Spin2 method files
│   │   ├── methods/
│   │   ├── operators/
│   │   └── ...
│   └── fundamentals/               # Cross-language concepts
├── hardware/                        # Board specifications
│   ├── boards/
│   └── modules/
├── community/
│   └── obex/
│       └── objects/                # 113 OBEX objects
└── patterns/                        # Implementation patterns
```

### Manifest Path Standard (4-Key System)

**All manifests use ONLY these four keys for paths:**

1. **`manifest_base:`** - Full path for manifest references
   - Example: `/manifests/P2/language`
   
2. **`content_base:`** - Full path for content references  
   - Example: `/engineering/knowledge-base/P2/language/pasm2`
   
3. **`manifest:`** - Reference to another manifest
   - Resolution: `{manifest_base}/{manifest}`
   - Example: `"spin2-manifest.yaml"`
   
4. **`content:`** - Reference to knowledge content
   - Resolution: `{content_base}/{content}`
   - Example: `"abs.yaml"`

**Example Manifest:**
```yaml
# Define bases once at top
manifest_base: "/manifests/P2/language"
content_base: "/engineering/knowledge-base/P2/language/pasm2"

# Clean references
items:
  - manifest: "spin2-manifest.yaml"  # → /manifests/P2/language/spin2-manifest.yaml
  - content: "abs.yaml"              # → /engineering/knowledge-base/P2/language/pasm2/abs.yaml
```

**Path Resolution is Simple:**
- Just concatenate: `base + "/" + reference`
- No context accumulation needed
- External Claude instances get full paths

---

## 📍 Quick Navigation Tips

### Finding Process Documentation:
1. **Quick guides**: Look in `*/work-modes/` directories
2. **Detailed processes**: Look in `*/methodology/` directories
3. **PDF generation**: Start at `/engineering/pdf-forge/`
4. **Ingestion**: Start at `/engineering/ingestion/`

### Common Workflows:
- **Ingesting a new document**: `/engineering/ingestion/work-modes/document-ingestion-focused.md`
- **Creating a PDF**: `/engineering/pdf-forge/PRODUCTION-REQUEST-FORMAT.md`
- **Working on deSilva manual**: `/engineering/document-production/work-modes/desilva-manual-mode.md`
- **Extracting images**: `/engineering/ingestion/work-modes/image-extraction-focused.md`

### Key Status Documents:
- **Engineering overview**: `/engineering/README.md`
- **Ingestion status**: `/engineering/ingestion/README.md`
- **Document production**: `/engineering/document-production/README.md`

---

*This document is your map. When in doubt, start here to find what you need.*