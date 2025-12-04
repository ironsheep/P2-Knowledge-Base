# Template Theory of Operations
## P2 Smart Pins Tutorial (Green Book)

**Document:** P2-Smart-Pins-Green-Book-Tutorial.md
**Template Prefix:** `p2kb-sp-*`
**Status:** Fully self-contained, properly namespaced

---

## Template Stack Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    p2kb-sp-template.latex                               │
│                    (Main Document Template)                             │
│  - Document class: book (11pt, A4, oneside)                            │
│  - Loads all .sty layers in order                                      │
│  - Contains \begin{document}...\end{document}                          │
│  - Inserts $body$ (Pandoc content)                                     │
│  - Calls \printindex at end                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 1: p2kb-sp-foundation.sty                      │
│                    (Core Infrastructure - 406 lines)                    │
│                                                                         │
│  PANDOC COMPATIBILITY:                                                  │
│  - \tightlist, \passthrough, \subtitle, \institute                     │
│  - \pandocbounded (image scaling)                                      │
│  - All *Tok syntax highlighting commands                               │
│  - Highlighting/Shaded environments                                    │
│                                                                         │
│  CORE PACKAGES:                                                         │
│  - inputenc, fontenc, lmodern, microtype (typography)                  │
│  - graphicx, longtable, booktabs, array (tables/images)                │
│  - xcolor, fancyhdr, titlesec, tocloft (styling)                       │
│  - tcolorbox with skins,breakable (colored boxes)                      │
│  - hyperref, bookmark (PDF links)                                      │
│  - listings, fancyvrb (code blocks)                                    │
│  - makeidx (index generation)                                          │
│                                                                         │
│  PAGINATION CONTROL:                                                    │
│  - Part always starts new page, first chapter same page                │
│  - Chapters get page breaks except first in part                       │
│  - Sections in Part II get page breaks (mode reference)                │
│  - Tracks: \iffirstchapterinpart, \iffirstsectioninchapter             │
│                                                                         │
│  IMAGE SCALING:                                                         │
│  - Default 85% linewidth, 80% textheight                               │
│  - Forces all figures to [H] placement (no floating)                   │
│                                                                         │
│  HEADING CONTROL (titlesec):                                            │
│  - Part: Page break, no vertical space                                 │
│  - Chapter: No auto page break (we control), 12pt after                │
│  - Section: 18pt before, 8pt after                                     │
│  - Subsection: 12pt before, 6pt after                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 2: p2kb-sp-styles.sty                          │
│                    (Content Styling - 849 lines)                        │
│                                                                         │
│  3-COLOR CODE BLOCK SYSTEM:                                             │
│  ┌──────────────────┬──────────────────┬────────────────────────────┐  │
│  │ Block Type       │ Environment      │ Color Theme                │  │
│  ├──────────────────┼──────────────────┼────────────────────────────┤  │
│  │ Spin2 code       │ Spin2Block       │ Green (smartpins-spin2-*)  │  │
│  │ PASM2 code       │ PASM2Block       │ Yellow (smartpins-pasm2-*) │  │
│  │ Antipattern      │ AntipatternBlock │ Red (smartpins-antipattern)│  │
│  │ Config (blue)    │ ConfigBlock      │ Blue (smartpins-config-*)  │  │
│  └──────────────────┴──────────────────┴────────────────────────────┘  │
│                                                                         │
│  SEMANTIC MARKER ENVIRONMENTS (gb* prefix):                             │
│  - gbdiagram: Amber dashed - "Diagram Needed"                          │
│  - gbpreliminary: Gray dotted - "Preliminary Content"                  │
│  - gbverify: Blue dashed - "Needs Verification"                        │
│  - gbexamples: Green solid - "Examples Needed"                         │
│  - gbtechreview: Rose dashed - "Technical Review Needed"               │
│  - gbcodereview: Orange dotted - "Code Review Needed"                  │
│  - gbtip: Mint rounded - "Tip"                                         │
│                                                                         │
│  TUTORIAL ENVIRONMENTS:                                                 │
│  - exercise: Blue - hands-on exercises                                 │
│  - keytakeaway: Green - key learning points                            │
│  - commonmistakes: Red - what NOT to do                                │
│  - trythis/trythisplus/trythischallenge: Progressive difficulty        │
│  - checkpoint: Purple - learning progress markers                      │
│  - gbseealso/quickref: Cross-references                                │
│  - remember: Violet - memory aids                                      │
│                                                                         │
│  DECISION TREE BOXES (Appendix A):                                      │
│  - startbox, decisioncategory, questionbox, modeanswer, optiongroup    │
│                                                                         │
│  SPIN2/PASM2 LANGUAGE DEFINITIONS:                                      │
│  - lstdefinelanguage{spin2} with P2 keywords                           │
│  - lstdefinelanguage{pasm2} with P2 instructions                       │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 3: p2kb-sp-numbering.sty                       │
│                    (Numbering System - 80 lines)                        │
│                                                                         │
│  PART NUMBERING:                                                        │
│  - Uses Arabic numerals: "Part 1", "Part 2" (not Roman)                │
│  - Actually removes part/chapter/section auto-numbers                   │
│  - Markdown already contains the numbers in heading text               │
│                                                                         │
│  CHAPTER FORMAT:                                                        │
│  - Left-aligned via \raggedright                                       │
│  - No automatic numbering prefix                                       │
│  - 12pt vertical space after                                           │
│                                                                         │
│  TOC ADJUSTMENTS:                                                       │
│  - "Chapter " prefix in TOC entries                                    │
│  - 5em number width                                                    │
│                                                                         │
│  IMPORTANT: This layer works WITH foundation pagination                │
│  - Does NOT override \part or \chapter page break logic                │
│  - Only handles numbering format                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 4: p2kb-sp-diagrams.sty                        │
│                    (TikZ Diagrams - ~1600 lines)                        │
│                                                                         │
│  HELPER MACROS:                                                         │
│  - \spClock: Draw clock waveform                                       │
│  - \spSignalLow/\spSignalHigh: Digital signal segments                 │
│  - \spRisingEdge/\spFallingEdge: Transition edges                      │
│                                                                         │
│  DIAGRAM COMMANDS (18 total):                                           │
│  1. \DRVHTimingDiagram - Drive high timing                             │
│  2. \TESTBINATimingDiagram - Test binary A timing                      │
│  3. \TESTPTimingDiagram - Test P timing                                │
│  4. \DACPWMPeriodDiagram - DAC/PWM period                              │
│  5. \PulseWidthMeasurementDiagram - Pulse width measurement            │
│  6. \NCOFrequencyDiagram - NCO frequency                               │
│  7. \NCODutyTimingDiagram - NCO duty timing                            │
│  8. \NCODutyBlockDiagram - NCO duty block                              │
│  9. \TrianglePWMDiagram - Triangle wave PWM                            │
│  10. \SawtoothPWMDiagram - Sawtooth wave PWM                           │
│  11. \QuadEncoderDiagram - Quadrature encoder                          │
│  12. \ComparatorDiagram - Comparator operation                         │
│  13. \PeriodMeasurementDiagram - Period measurement                    │
│  14. \ContinuousPeriodDiagram - Continuous period                      │
│  15. \TimeoutWatchdogDiagram - Timeout/watchdog                        │
│  (+ more)                                                               │
│                                                                         │
│  TIKZ STYLES:                                                           │
│  - sp-signal, sp-clock: Waveform lines                                 │
│  - sp-block, sp-arrow, sp-biarrow: Block diagrams                      │
│  - sp-annotation, sp-label, sp-bitlabel: Text formatting               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Lua Filter Pipeline

**Order is CRITICAL.** Filters must run in this sequence:

```
Markdown Input
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. p2kb-sp-fix-hypertarget.lua                                          │
│    - Removes problematic identifiers from Part headers                 │
│    - Prevents [Part I:]Part I: bracket duplication                     │
│    - Clears ALL attributes on Part headers                             │
│    - Leaves other headers for TOC linking                              │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. p2kb-sp-fix-title-as-part.lua                                        │
│    - First H1 that isn't "Part X" = document title, not \part{}        │
│    - Prevents title from becoming Part 0                               │
│    - Escapes LaTeX special characters in title                         │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. p2kb-sp-frontmatter.lua                                              │
│    - Handles EVERYTHING before Part I                                  │
│    - Demotes headers to work WITH stylesheet page breaks               │
│    - Suppresses metadata headers (Version, Created)                    │
│    - Preface subsections demoted to level 5 (exclude from TOC)         │
│    - STOPS processing at Part I                                        │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. p2kb-sp-structure.lua                                                │
│    - Handles document structure AFTER Part I                           │
│    - Tracks Part transitions for first-chapter handling                │
│    - Lets stylesheet handle ALL page breaks                            │
│    - Takes over FROM frontmatter filter                                │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. p2kb-sp-index-toc.lua                                                │
│    - Prevents index letter sections (A, B, C...) from TOC              │
│    - Converts single uppercase letter headings to \section*{}          │
│    - Keeps them in document but excludes from TOC                      │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 6. p2kb-sp-code-coloring.lua                                            │
│    - Converts div-wrapped code blocks to colored environments          │
│    - ::: spin2 → Spin2Block (green)                                    │
│    - ::: pasm2 → PASM2Block (yellow)                                   │
│    - ::: antipattern → AntipatternBlock (red)                          │
│    - Also handles decision tree flowchart boxes                        │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 7. p2kb-sp-semantic.lua                                                 │
│    - Converts semantic divs to LaTeX tcolorbox environments            │
│    - ::: needs-diagram → gbdiagram                                     │
│    - ::: tip → gbtip                                                   │
│    - (See full mapping in styles.sty section)                          │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
LaTeX Output → PDF
```

---

## Data Flow: Markdown to PDF

```
┌─────────────────────────────────────────────────────────────────────────┐
│ MARKDOWN SOURCE                                                         │
│                                                                         │
│ # Part I: Foundations                                                   │
│                                                                         │
│ ## Chapter 1: Introduction                                              │
│                                                                         │
│ ::: tip                                                                 │
│ Smart Pins are powerful!                                                │
│ :::                                                                     │
│                                                                         │
│ ::: pasm2                                                               │
│ ```pasm2                                                                │
│ wrpin  mode, #PIN                                                       │
│ ```                                                                     │
│ :::                                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Pandoc + Lua Filters
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LATEX OUTPUT                                                            │
│                                                                         │
│ \part{Part I: Foundations}                                              │
│                                                                         │
│ \chapter{Chapter 1: Introduction}                                       │
│                                                                         │
│ \begin{gbtip}                                                           │
│ Smart Pins are powerful!                                                │
│ \end{gbtip}                                                             │
│                                                                         │
│ \begin{PASM2Block}                                                      │
│ \begin{Highlighting}                                                    │
│ wrpin  mode, \#PIN                                                      │
│ \end{Highlighting}                                                      │
│ \end{PASM2Block}                                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ XeLaTeX + Template Stack
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PDF OUTPUT                                                              │
│                                                                         │
│ - Part starts new page with "Part I: Foundations"                      │
│ - Chapter follows on same page (no break after part)                   │
│ - gbtip renders as mint green box with "Tip" title                     │
│ - PASM2Block renders as yellow-bordered code box                       │
│ - All hyperlinks, TOC entries, index entries work                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Pandoc Arguments Required

```json
{
  "pandoc_args": [
    "--top-level-division=part",
    "--pdf-engine=xelatex"
  ]
}
```

| Argument | Purpose |
|----------|---------|
| `--top-level-division=part` | **CRITICAL.** Maps # → \part, ## → \chapter, ### → \section. Without this, pagination breaks. |
| `--pdf-engine=xelatex` | Required for Unicode support and modern font handling |

---

## Customization Points

### To Add a New Semantic Environment

1. **In `p2kb-sp-styles.sty`:** Add new tcolorbox definition
   ```latex
   \newtcolorbox{gbNEWENV}{
     colback=...,
     colframe=...,
     title={New Environment},
     ...
   }
   ```

2. **In `p2kb-sp-semantic.lua`:** Add mapping
   ```lua
   local divMappings = {
       ...
       ["new-env"] = "gbNEWENV",
   }
   ```

### To Add a New TikZ Diagram

1. **In `p2kb-sp-diagrams.sty`:** Add new command
   ```latex
   \newcommand{\NewDiagram}{%
     \begin{tikzpicture}
       ...
     \end{tikzpicture}
   }
   ```

2. **In markdown:** Use raw LaTeX
   ```markdown
   ```{=latex}
   \NewDiagram
   ```
   ```

### To Modify Code Block Colors

Edit color definitions in `p2kb-sp-styles.sty`:
```latex
\definecolor{smartpins-pasm2-bg}{HTML}{FFFEF5}
\definecolor{smartpins-pasm2-border}{HTML}{D4B896}
```

---

## Conversion Status

### Naming Convention Compliance

| File | Status | Notes |
|------|--------|-------|
| `p2kb-sp-template.latex` | ✅ Compliant | Proper prefix |
| `p2kb-sp-foundation.sty` | ✅ Compliant | Proper prefix |
| `p2kb-sp-styles.sty` | ✅ Compliant | Proper prefix |
| `p2kb-sp-numbering.sty` | ✅ Compliant | Proper prefix |
| `p2kb-sp-diagrams.sty` | ✅ Compliant | Proper prefix |
| `p2kb-sp-fix-hypertarget.lua` | ✅ Compliant | Proper prefix |
| `p2kb-sp-fix-title-as-part.lua` | ✅ Compliant | Proper prefix |
| `p2kb-sp-frontmatter.lua` | ✅ Compliant | Proper prefix |
| `p2kb-sp-structure.lua` | ✅ Compliant | Proper prefix |
| `p2kb-sp-index-toc.lua` | ✅ Compliant | Proper prefix |
| `p2kb-sp-code-coloring.lua` | ✅ Compliant | Proper prefix |
| `p2kb-sp-semantic.lua` | ✅ Compliant | Proper prefix |

### Self-Containment Status

✅ **Fully self-contained.** All template files are:
- Located in workspace `templates/` and `filters/` directories
- Properly prefixed with `p2kb-sp-`
- No dependencies on shared files outside workspace

### Internal File Naming Issues

| File | Issue | Action When Active |
|------|-------|-------------------|
| `p2kb-sp-styles.sty` | Header says `p2kb-smart-pins-content` | Update header comment |
| `p2kb-sp-numbering.sty` | Header says `smart-pins-numbering-fix` | Update header comment |

These are cosmetic - the actual filenames are correct.

---

## Unique Features (vs Other Manuals)

1. **7-Filter Pipeline** - Most complex Lua filter chain
2. **4-Layer Template Stack** - Including dedicated diagrams layer
3. **18 TikZ Diagrams** - Embedded timing/block diagrams
4. **3-Color Code System** - Spin2/PASM2/Antipattern distinction
5. **Tutorial Environments** - Exercise/Checkpoint/TryThis progression
6. **Part II Mode Reference** - Special pagination (sections get page breaks)

---

*Created: 2025-12-03*
*Document: P2 Smart Pins Tutorial (Green Book)*
*Template Version: 2.0*
