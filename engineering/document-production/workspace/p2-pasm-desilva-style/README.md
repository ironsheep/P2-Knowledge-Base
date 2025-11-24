# P2 PASM DeSilva Style - Workspace Guide

## Quick Reference
**Canonical Name:** `p2-pasm-desilva-style`
**Document Title:** Discovering P2 Assembly
**Subtitle:** Build, Experiment, and Master the Propeller 2
**Creation Guide:** `/engineering/document-production/manuals/p2-pasm-desilva-style/creation-guide.md`
**Outbound Deployment:** `/engineering/document-production/outbound/p2-pasm-desilva-style/`
**Status:** In Production - Content Development Phase

## Document Purpose

Creating a pedagogical PASM2 manual that captures deSilva's teaching philosophy: approachable, hands-on, and genuinely enjoyable assembly language learning.

**Teaching Philosophy:** "Learn by doing, celebrate progress, have fun!"

## Related Folders

### This Workspace
- **Master Markdown:** `P2-PASM-deSilva-Working-Copy.md` (main working document)
- **Templates:** `templates/` folder - See [templates/README.md](templates/README.md)
- **Lua Filters:** `filters/` folder - Pandoc processing filters
- **Special Requirements:** `request-requirements.json` (--top-level-division=part)
- **Request Config:** `request.json` (PDF generation configuration)
- **Version Tracking:** `VERSION-TRACKING.md` (document version history)
- **Template Testing:** `TEMPLATE-STACK-TEST-SUMMARY.md` (template validation notes)

### Creation and Style Guides
- **Creation Guide:** `/engineering/document-production/manuals/p2-pasm-desilva-style/creation-guide.md`
- **DeSilva Style:** `/engineering/document-production/manuals/p2-pasm-desilva-style/desilva-style-guide.md`

### Deployment Location
- **Outbound:** `/engineering/document-production/outbound/p2-pasm-desilva-style/`
- **Process:** Files copied here after LaTeX escaping, ready for PDF Forge

## Template Stack

**Prefix:** `p2kb-desilva-*`

```
Layer 1: p2kb-desilva-foundation.sty (deSilva-specific foundation)
    ↓
Layer 2: p2kb-desilva-content.sty (5-color code + pedagogical environments)
    ↓
Main: p2kb-desilva.latex (orchestrates both layers + custom title page)
```

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

## Workflow Quick Start

### 1. Edit Content
Edit `P2-PASM-deSilva-Working-Copy.md` in this workspace

### 2. Prepare for PDF Generation
```bash
# From workspace directory:
/workspaces/P2-Knowledge-Base/engineering/tools/latex-escape-all.sh \
    P2-PASM-deSilva-Working-Copy.md \
    /workspaces/P2-Knowledge-Base/engineering/document-production/outbound/p2-pasm-desilva-style/P2-PASM-deSilva-Style.md
```

### 3. Copy Supporting Files
```bash
# Copy templates if changed
cp templates/*.{latex,sty} ../outbound/p2-pasm-desilva-style/

# Copy Lua filters if changed
cp -r filters ../outbound/p2-pasm-desilva-style/

# Ensure request.json is present
cp request.json ../outbound/p2-pasm-desilva-style/
```

### 4. User Deploys to PDF Forge
User manually moves files from outbound to PDF Forge system

## Key Process Documents

### Universal Methodology
- **Format Guide:** `/engineering/document-production/methodology/pdf-generation-format-guide.md`
- **Workflow Guide:** `/engineering/document-production/methodology/pdf-generation-workflow-guide.md`

### Document-Specific
- **Creation Guide:** `/engineering/document-production/manuals/p2-pasm-desilva-style/creation-guide.md` (comprehensive document philosophy and content strategy)
- **DeSilva Style Guide:** `/engineering/document-production/manuals/p2-pasm-desilva-style/desilva-style-guide.md`
- **Markdown Changes:** `desilva-markdown-changes-guide.md` (in this workspace)

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

## Current Status

**Phase:** Content Development
**Progress:**
- Chapters 1-6 complete from Opus master (strong foundation)
- Chapter 7 (CORDIC) enhancement in progress
- Chapter 8 (Basic I/O) rewrite planned
- Chapters 9-16 development ongoing

**Next Steps:**
- Enhance remaining chapters using YAML sources
- Add Medicine Cabinet sections
- Expand "Your Turn" exercises
- Validate all code examples with pnut_ts compiler
- Prepare for Technical Review

## Code Validation

All code examples MUST be validated before inclusion:
```bash
# Validate PASM2/Spin2 code
/workspaces/P2-Knowledge-Base/engineering/tools/compiler/pnut_ts filename.spin2
```

**Compiler Location:** `/engineering/tools/compiler/pnut_ts`
**Usage Guide:** `/engineering/tools/compiler/pnut_ts-usage-guide.md`

## PDF Forge Integration

### Testing (Template Development & Visual Refinement)
**Guide:** `/engineering/pdf-forge/work-modes/automated-pdf-testing.md`
- Rapid iteration for template fixes and visual refinement (30-60 sec cycles)
- Test multiple scenarios in one request
- Temporary testing - does NOT install templates permanently

### Production (Final Deliverable Generation)
**Guide:** `/engineering/pdf-forge/work-modes/production-pdf-generation.md`
- Create deliverable PDFs for distribution
- **CRITICAL:** Only copy CHANGED files to outbound (request.json + .md always, templates/filters only if modified)
- Templates and filters persist on PDF Forge - don't resend unchanged files

**Complete Rules:** `/engineering/pdf-forge/PRODUCTION-PROCESS-RULES.md` (🚨 "only changed files" details)

## Notes

This workspace follows the **Technical Climbing Methodology** - each regeneration incorporates new trusted P2 sources while preserving proven pedagogical patterns.

**Protection Points:** Successful pedagogy from Opus, working code examples, deSilva voice
**Climbing Higher:** Enhanced with YAML accuracy, pattern examples, improved structure
