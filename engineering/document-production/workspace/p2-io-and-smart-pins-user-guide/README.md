# Workspace - P2 I/O & Smart Pins User Guide

**Purpose:** PDF production workspace for the P2 I/O & Smart Pins User Guide.

**Status:** Initialized - Awaiting content development

---

## Quick Reference

| Resource | Location |
|----------|----------|
| **Content (Opus Master)** | `../../manuals/p2-io-and-smart-pins-user-guide/opus-master/` |
| **Creation Guide** | `../../manuals/p2-io-and-smart-pins-user-guide/creation-guide.md` |
| **Voice Guide** | `../../manuals/p2-io-and-smart-pins-user-guide/voice-guide.md` |
| **Escape Script** | `../../../tools/conversion/latex-escape-all.sh` |
| **Outbound Folder** | `../../outbound/p2-io-and-smart-pins-user-guide/` |

---

## Before You Begin

**Read the PDF generation lessons learned:** `/engineering/operations/lessons-learned/pdf-generation-changelog.md`

This changelog documents critical issues discovered during document production that will save significant debugging time.

---

## Critical File Naming Convention

**The master document name is sacred and never changes:**

| Purpose | Filename |
|---------|----------|
| **Master Document** | `P2-IO-and-Smart-Pins-User-Guide.md` |
| **Output PDF** | `P2-IO-and-Smart-Pins-User-Guide.pdf` |

**Rules:**
- Always use the exact document name - no suffixes like `-escaped`, `-v2`, `-final`
- The manuals copy is the canonical source (edit here)
- The workspace copy is unescaped (production prep, copied from manuals)
- The outbound copy is escaped (ready for Forge)
- All three use the identical filename
- Never rename files - always replace in place

---

## Directory Structure

```
manuals/p2-io-and-smart-pins-user-guide/opus-master/  <- CANONICAL SOURCE (edit here)
|-- P2-IO-and-Smart-Pins-User-Guide.md                # Master document

workspace/p2-io-and-smart-pins-user-guide/            <- YOU ARE HERE (production prep)
|-- README.md                                         # This file
|-- P2-IO-and-Smart-Pins-User-Guide.md                # Working copy (UNESCAPED)
|-- templates/
|   +-- (template files)
|-- filters/
|   +-- (Lua filter files)
|-- assets/
|   +-- (PNG images)
|-- request.json                                      # PDF Forge configuration

outbound/p2-io-and-smart-pins-user-guide/             <- FLAT structure for PDF Forge
|-- P2-IO-and-Smart-Pins-User-Guide.md                # ESCAPED copy
|-- (template files - FLAT)
|-- (filter files - FLAT)
|-- request.json
+-- assets/                                           # ALL images go here
    +-- *.png
```

---

## Document Scope

This guide covers the complete P2 pin I/O system:

**Part I: Fundamentals**
- Direct I/O (DIR/OUT/IN, pin instructions)
- Enhanced Direct I/O (P_ constants without Smart Pin modes)
- Smart Pin Architecture and Configuration

**Part II: Output Modes** (simple → complex)
- Digital, Pulse, NCO, PWM, DAC, Serial TX

**Part III: Input Modes** (simple → complex)
- Digital, Timing, Counting, Quadrature, Period/Freq, ADC, Serial RX

**Part IV: Special Modes**
- Repository, USB

**Part V: Appendices**
- Intent Index, P_ Constants, Formulas, Comparisons, Troubleshooting

---

## PDF Forge Workflow

### Three-Stage Document Pipeline

```
MANUALS (canonical source)     WORKSPACE (production prep)     OUTBOUND (staging)
        |                              |                              |
   Edit content here           Copy/assemble here              Escaped files here
        |                              |                              |
        +---- copy or assemble ------->|                              |
                                       +---- latex-escape-all.sh ---->|
                                       + copy CHANGED templates/filters
```

### PDF Forge Persistence

**PDF Forge is a PERSISTENT system.** It retains ALL files from the last deployment indefinitely.

**Critical Rules:**
- Only send files that CHANGED in this session
- Forge keeps the last version of every file
- Empty outbound after deployment is NORMAL
- DO NOT re-copy unchanged files

### Step-by-Step Process

1. **Edit in Manuals** - All content edits in `manuals/.../opus-master/`
2. **Copy to Workspace** - Copy edited master to workspace
3. **Escape to Outbound** - Run latex-escape-all.sh, stage CHANGED files only
4. **User Deploys** - User MOVES files from outbound to PDF Forge
5. **Feedback Loop** - Fix based on errors/visual feedback, repeat

---

## Important Notes

- **Outbound is FLAT** - All `.sty`, `.latex`, `.lua`, `.json` at root level
- **One exception: `assets/`** - Only subfolder; ALL images go here
- **Same filename everywhere** - Consistent naming across all locations
- **Workspace is unescaped** - Never run escape script in place
- **Outbound empties after deployment** - This is NORMAL

---

## Source Materials

| Source | Location | Purpose |
|--------|----------|---------|
| Smart Pins catalog | `/engineering/ingestion/smart-pins-catalog/ingestionSources/` | Mode documentation |
| P_ constants | `/engineering/ingestion/sources/spin2-v51/smartpin-symbols.txt` | Constant values |
| Silicon doc extracts | `*/silicon-doc-extract.md` | Hardware behavior |
| Titus extracts | `*/john-titus-extract.md` | Detailed mode docs |

---

*Created: 2026-01-24*
*Renamed: 2026-01-24 (from p2-smart-pins-user-guide)*
*Status: Initialized*
