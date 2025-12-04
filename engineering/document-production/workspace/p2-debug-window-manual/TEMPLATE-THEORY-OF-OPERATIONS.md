# P2 Debug Window Manual - Template Theory of Operations

**Document:** P2-Debug-Window-Manual.md
**Template Prefix:** `p2kb-debugwin-*`
**Version:** 1.0
**Last Updated:** 2025-12-03

## Overview

The P2 Debug Window Manual uses a **2-layer self-contained template stack** with 3 Lua filters, designed for visual discovery documentation covering the P2 DEBUG() system and its 9 window types. The architecture emphasizes screenshot-heavy content and discovery-driven learning.

## Template Stack Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    p2kb-debugwin.latex                       │
│                  (Master Pandoc Template)                    │
│         Title page, List of Figures, Document Stats          │
├─────────────────────────────────────────────────────────────┤
│                p2kb-debugwin-foundation.sty                  │
│              (Debug Window Foundation Layer)                 │
│    Pandoc compat, image scaling, page layout, pagination     │
├─────────────────────────────────────────────────────────────┤
│                 p2kb-debugwin-content.sty                    │
│              (5-Color Code + Semantic Elements)              │
│    Code blocks, discovery boxes, screenshot containers       │
└─────────────────────────────────────────────────────────────┘
```

### Loading Order (Critical)
```latex
1. p2kb-debugwin-foundation.sty  % Document infrastructure first
2. p2kb-debugwin-content.sty     % Visual discovery layer second
```

## Style Sheet Details

### Layer 1: p2kb-debugwin-foundation.sty (379 lines)

**Purpose:** Debug Window-specific document infrastructure

**Key Features:**
- **Pandoc Compatibility:** Complete set of `\providecommand` for Pandoc integration
- **Image Scaling:** Default 85% width with auto-height preservation
- **Non-Floating Figures:** Forces `[H]` placement for screenshots
- **Page Layout:** A4, 11pt, single-sided (digital-first)
- **Conditional Pagination:** Part→Chapter→Section hierarchy with intelligent breaks
- **Header Configuration:** Clean chapter titles, no "Chapter X:" prefix
- **TOC Depth:** 2 levels (tocdepth=2)
- **Section Numbering:** Disabled (secnumdepth=-1) - headings contain own numbers

**Special Logic:**
- Part II sections get page breaks (debug window modes as chapters)
- First chapter in each part stays on same page as part heading
- Subsequent chapters get their own pages

### Layer 2: p2kb-debugwin-content.sty (530 lines)

**Purpose:** 5-color code block system plus visual discovery elements

**5-Color Code Block System:**

| Block Type | Color | Purpose | LaTeX Environment |
|------------|-------|---------|-------------------|
| Spin2 | Green (#F8FCF8) | Main program structure | `DebugWinSpin2Block` |
| PASM2 | Cream (#FFFEF5) | Assembly language | `DebugWinPASM2Block` |
| DEBUG | Blue (#F5F9FC) | DEBUG() statements | `DebugWinDebugBlock` |
| Terminal | Gray (#F8F8F8) | Terminal output | `DebugWinTerminalBlock` |
| Window | Purple (#F8F5FF) | Window commands | `DebugWinWindowBlock` |

**Window-Specific Blocks (all use purple theme):**
- `DebugWinBitmapBlock`, `DebugWinScopeBlock`, `DebugWinLogicBlock`
- `DebugWinPlotBlock`, `DebugWinFFTBlock`, `DebugWinSpectroBlock`
- `DebugWinScopeXYBlock`

**Visual Discovery Elements:**

| Element | Purpose | Border Color |
|---------|---------|--------------|
| Discovery | Major findings | Orange |
| Experiment | Hands-on learning | Green |
| Performance | Optimization tips | Red |
| Tip | Pro tips | Blue |
| Screenshot | Annotated images | Gray |
| NeedsScreenshot | Placeholder | Amber dashed |
| Comparison | Performance comparison | Purple |
| MultiChannel | Multi-window coordination | Teal |
| Gallery | Window type showcase | Brown |
| CommandRef | Command reference | Violet |

**Lowercase Aliases (for Lua filter compatibility):**
- `dwdiscovery`, `dwexperiment`, `dwperformance`, `dwtip`, `dwscreenshot`, `dwneedsscreenshot`

**Language Definitions:**
- `spin2` language with P2-specific keywords
- `pasm2` language with assembly mnemonics
- `debug` language with DEBUG() commands and window types

### Master Template: p2kb-debugwin.latex (117 lines)

**Purpose:** Pandoc template with custom title page

**Features:**
- Custom title page with Technical Review Focus Areas
- Document Statistics section (chapters, appendices, window types, examples)
- Copyright page with acknowledgments
- `\tableofcontents` + `\listoffigures` (for screenshot navigation)
- Loads both style layers in correct order

## Lua Filter Pipeline

### Processing Order (as specified in request.json):
```
1. p2kb-debugwin-div-blocks.lua    → Code block styling
2. p2kb-debugwin-semantic.lua      → Discovery/learning boxes
```

### Filter 1: p2kb-debugwin-div-blocks.lua (134 lines)

**Purpose:** Convert div-syntax code blocks to 5-color LaTeX environments

**Div Classes Processed:**

| Markdown Div | LaTeX Environment |
|--------------|-------------------|
| `.spin2` | `DebugWinSpin2Block` |
| `.pasm2` | `DebugWinPASM2Block` |
| `.debug` | `DebugWinDebugBlock` |
| `.terminal` | `DebugWinTerminalBlock` |
| `.bitmap` | `DebugWinBitmapBlock` |
| `.scope` | `DebugWinScopeBlock` |
| `.logic` | `DebugWinLogicBlock` |
| `.plot` | `DebugWinPlotBlock` |
| `.fft` | `DebugWinFFTBlock` |
| `.spectro` | `DebugWinSpectroBlock` |
| `.scope_xy` / `.scopexy` | `DebugWinScopeXYBlock` |
| `.window` | `DebugWinWindowBlock` |

**CodeBlock Fallback:** Also handles legacy language-tagged code blocks by wrapping them in appropriate div classes.

### Filter 2: p2kb-debugwin-semantic.lua (94 lines)

**Purpose:** Convert semantic div blocks to discovery/learning environments

**Div Classes Processed:**

| Markdown Div | LaTeX Environment |
|--------------|-------------------|
| `.discovery` | `dwdiscovery` |
| `.experiment` | `dwexperiment` |
| `.performance` | `dwperformance` |
| `.tip` | `dwtip` |
| `.screenshot` | `dwscreenshot` |
| `.needs-screenshot` | `dwneedsscreenshot` |
| `.performance-comparison` / `.comparison` | `DebugWinComparison` |
| `.multichannel` / `.multiwindow` | `DebugWinMultiChannel` |
| `.gallery` | `DebugWinGallery` |
| `.commandref` / `.reference` | `DebugWinCommandRef` |

### Filter 3: p2kb-debugwin-non-floating-images.lua (34 lines)

**Purpose:** Force non-floating image placement with captions

**Behavior:**
- Wraps all images in `figure[H]` environment
- Default width: 85% of textwidth
- Respects width attribute if specified
- Extracts caption from title attribute

**Note:** This filter is listed in workspace but NOT in request.json - may need to be added for screenshot-heavy documents.

## Additional Files in Workspace

### Shared Foundation (Reference Only)
**File:** `p2kb-foundation.sty` (379 lines)
**Status:** Present but NOT actively loaded - Debug Window uses its own foundation

### Utility Scripts
- `convert-images-to-placeholders.py` - Replace images with placeholders
- `convert-debug-window-images.py` - Process debug window screenshots
- `fix-unicode-characters.py` - Unicode cleanup
- `fix-document-structure.py` - Document structure fixes

### Documentation
- `template-development-plan.md` - Template evolution notes
- `debug-window-markdown-changes-guide.md` - Markdown conversion guide
- `templates/README.md` - Template hierarchy documentation

## Naming Convention Compliance

### ✅ Compliant Files
| File | Pattern | Status |
|------|---------|--------|
| `p2kb-debugwin.latex` | `p2kb-{docprefix}.latex` | ✅ Correct |
| `p2kb-debugwin-foundation.sty` | `p2kb-{docprefix}-{purpose}.sty` | ✅ Correct |
| `p2kb-debugwin-content.sty` | `p2kb-{docprefix}-{purpose}.sty` | ✅ Correct |
| `p2kb-debugwin-div-blocks.lua` | `p2kb-{docprefix}-{purpose}.lua` | ✅ Correct |
| `p2kb-debugwin-semantic.lua` | `p2kb-{docprefix}-{purpose}.lua` | ✅ Correct |
| `p2kb-debugwin-non-floating-images.lua` | `p2kb-{docprefix}-{purpose}.lua` | ✅ Correct |

### ⚠️ Mixed Status Files
| File | Issue |
|------|-------|
| `p2kb-foundation.sty` | Shared/generic file - appropriate name but not document-specific |
| `p2kb-non-floating-images.lua` | Shared filter variant - should use document prefix if used |

## Pandoc Arguments (from request.json)

```json
"pandoc_args": [
  "--top-level-division=part",
  "--pdf-engine=xelatex",
  "--toc",
  "--toc-depth=3",
  "--number-sections",
  "--highlight-style=tango"
]
```

**Key Settings:**
- `--top-level-division=part`: `#` → Part, `##` → Chapter, `###` → Section
- `--pdf-engine=xelatex`: Required for tcolorbox and advanced typography
- `--toc-depth=3`: Show down to subsections in TOC
- `--number-sections`: Auto-numbering (overridden by template secnumdepth=-1)
- `--highlight-style=tango`: Syntax highlighting theme

## Self-Containment Status

### ✅ Fully Self-Contained
- All template files use `p2kb-debugwin-*` prefix
- Foundation layer is document-specific (not shared)
- Content layer designed for visual discovery style
- Lua filters are document-specific

### 📋 Conversion Notes
- This workspace was created self-contained from the start
- Based on DeSilva template patterns but adapted for screenshot-heavy content
- No dependencies on shared template files

## Document-Specific Features

### Visual Discovery Philosophy
1. **Show, don't just tell:** Every feature has screenshot proof
2. **Discover through exploration:** Hands-on experimentation encouraged
3. **Systematic coverage:** All 9 window types documented
4. **Visual verification:** Screenshots confirm every capability

### 9 Window Types Covered
1. Terminal (text output)
2. Bitmap (graphics)
3. Plot (data visualization)
4. Scope (waveform display)
5. Logic (digital signals)
6. FFT (frequency analysis)
7. Spectro (spectrogram)
8. Scope_XY (X-Y plotting)
9. Mixed (combination windows)

### Screenshot Management
- All screenshots in `assets/` folder
- Reference as: `![Caption](assets/screenshot-name.png)`
- NO SPACES in filenames (use hyphens)
- PNG format preferred
- List of Figures auto-generated for navigation

## When Working on This Document

### Before Editing:
1. Review this Theory of Operations
2. Check templates/README.md for visual discovery philosophy
3. Understand 5-color code block system
4. Review semantic element options (discovery, experiment, tip, etc.)

### Code Block Usage:
```markdown
::: spin2
' Spin2 high-level code (green)
PUB Main()
  DEBUG("Hello World")
:::

::: debug
DEBUG BITMAP 'MySine' SIZE 256 LUT8X TRACE 10 `MySine` RANGE 0 255
:::

::: terminal
Terminal output (gray, monospace)
:::
```

### Discovery Element Usage:
```markdown
::: discovery
Major finding about DEBUG() behavior discovered through experimentation.
:::

::: experiment
Try running this code and observe the window position changes.
:::

::: tip
Pro tip: Use TRACE to connect multiple windows.
:::
```

### Deployment:
1. Edit markdown and templates as needed
2. Run LaTeX escape script: `../../../tools/conversion/latex-escape-all.sh`
3. Copy to outbound: markdown, templates/, filters/, assets/, request.json
4. PDF Forge generates PDF with `\listoffigures` for screenshot navigation

## Maintenance Notes

- Template co-evolves with visual content
- Discovery-driven style should be preserved
- Screenshot quality is paramount
- Performance metrics should be real measurements
- Needs-screenshot placeholders track missing visuals
