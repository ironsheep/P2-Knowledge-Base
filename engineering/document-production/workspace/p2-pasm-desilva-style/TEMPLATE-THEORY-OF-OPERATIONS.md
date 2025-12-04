# Template Theory of Operations
## P2 PASM DeSilva Style (Discovering P2 Assembly)

**Document:** P2-PASM-deSilva-Style.md
**Template Prefix:** `p2kb-desilva-*`
**Status:** Fully self-contained, properly namespaced

---

## Template Stack Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    p2kb-desilva.latex                                   │
│                    (Main Document Template)                             │
│  - Document class: book (12pt, letter paper, oneside)                  │
│  - Loads all .sty layers in order                                      │
│  - Contains \begin{document}...\end{document}                          │
│  - Inserts $body$ (Pandoc content)                                     │
│  - Calls \printindex at end                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 1: p2kb-desilva-foundation.sty                 │
│                    (Core Infrastructure - 301 lines)                    │
│                                                                         │
│  PANDOC COMPATIBILITY:                                                  │
│  - \tightlist, \passthrough, \subtitle, \institute                     │
│  - All *Tok syntax highlighting commands                               │
│  - Highlighting/Shaded environments                                    │
│                                                                         │
│  FONT CONFIGURATION (XeLaTeX):                                          │
│  - Latin Modern Roman/Sans/Mono via fontspec                           │
│                                                                         │
│  CORE PACKAGES:                                                         │
│  - graphicx, longtable, booktabs, array, multirow                      │
│  - xcolor, hyperref, fancyhdr, titlesec, tocloft                       │
│  - tcolorbox with skins,breakable                                      │
│  - listings, fancyvrb (code blocks)                                    │
│  - enumitem (list control)                                             │
│                                                                         │
│  HEADING SPACING:                                                       │
│  - Chapter: -40pt before, 10pt after (compact)                         │
│  - Section: 12pt before, 2pt after                                     │
│  - Subsection: 10pt before, 3pt after                                  │
│                                                                         │
│  PAGE LAYOUT:                                                           │
│  - Geometry: 0.75in top, 0.5in bottom, 1in left/right                  │
│  - Parskip: 10pt (standard)                                            │
│  - Linespread: 1.3 (standard)                                          │
│                                                                         │
│  TOC CONFIGURATION:                                                     │
│  - tocdepth=1 (Chapters and Sections)                                  │
│  - secnumdepth=-1 (no auto-numbering)                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 2: p2kb-desilva-content.sty                    │
│                    (Content Styling - 470+ lines)                       │
│                                                                         │
│  5-COLOR CODE BLOCK SYSTEM:                                             │
│  ┌──────────────────┬─────────────────────┬──────────────────────────┐ │
│  │ Block Type       │ Environment         │ Color Theme              │ │
│  ├──────────────────┼─────────────────────┼──────────────────────────┤ │
│  │ Spin2 code       │ DeSilvaSpin2Block   │ Green (desilva-spin2-*)  │ │
│  │ PASM2 code       │ DeSilvaPASM2Block   │ Yellow (desilva-pasm2-*) │ │
│  │ CORDIC code      │ DeSilvaCORDICBlock  │ Purple (desilva-cordic-*)│ │
│  │ Multi-COG code   │ DeSilvaMultiCOGBlock│ Blue (desilva-multicog-*)│ │
│  │ Antipattern      │ DeSilvaAntipatternBlock│Red (desilva-antipattern)│ │
│  └──────────────────┴─────────────────────┴──────────────────────────┘ │
│                                                                         │
│  PEDAGOGICAL ENVIRONMENTS (DeSilva* prefix):                            │
│  - DeSilvaMedicineCabinet (teal): Simpler alternatives                 │
│  - DeSilvaYourTurn (green): Hands-on exercises                         │
│  - DeSilvaSidetrack (purple): Interesting diversions                   │
│  - DeSilvaInterlude (orange): Stories and history                      │
│  - DeSilvaChapterEnd (blue): Chapter summaries                         │
│                                                                         │
│  LOWERCASE ds* VARIANTS (for Lua filter compatibility):                 │
│  - dsmedicinecabinet, dsyourturn, dssidetrack                          │
│  - dsuff ("Uff!" - complexity acknowledgment)                          │
│  - dswell ("Well..." - correcting assumptions)                         │
│  - dshavefun ("Have Fun!" - encouragement)                             │
│                                                                         │
│  ADDITIONAL ENVIRONMENTS:                                               │
│  - commongotas: Red - debugging help                                   │
│  - realworldexample: Brown - practical applications                    │
│  - performancenote: Violet - optimization tips                         │
│                                                                         │
│  LANGUAGE DEFINITIONS:                                                  │
│  - spin2: Spin2 keywords for listings                                  │
│  - pasm2: PASM2 keywords for listings                                  │
│  - cordic: PASM2 extended with CORDIC instructions                     │
│  - multicog: PASM2 extended with multi-COG instructions                │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 3: p2kb-desilva-diagrams.sty                   │
│                    (TikZ Diagrams)                                      │
│                                                                         │
│  ARCHITECTURAL DIAGRAMS:                                                │
│  - COG memory layout diagrams                                          │
│  - Hub memory organization                                             │
│  - Register maps                                                       │
│                                                                         │
│  (Shared with PASM2 Reference Manual where applicable)                 │
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
│ 1. p2kb-desilva-pagination.lua                                          │
│    - Handles page breaks between Chapters                              │
│    - Detects Chapter, Appendix, Preface, etc. headers                  │
│    - First chapter after TOC: no page break                            │
│    - All subsequent chapters: \clearpage before                        │
│    - Chapter-based (not Part-based like Smart Pins)                    │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. p2kb-desilva-div-blocks.lua                                          │
│    - Converts div-syntax code blocks to LaTeX environments             │
│    - ::: spin2 → DeSilvaSpin2Block                                     │
│    - ::: pasm2 → DeSilvaPASM2Block                                     │
│    - ::: cordic → DeSilvaCORDICBlock                                   │
│    - ::: multicog → DeSilvaMultiCOGBlock                               │
│    - ::: antipattern → DeSilvaAntipatternBlock                         │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. p2kb-desilva-semantic-blocks.lua                                     │
│    - Converts pedagogical divs to LaTeX environments                   │
│    - ::: medicine → DeSilvaMedicineCabinet                             │
│    - ::: yourturn → DeSilvaYourTurn                                    │
│    - ::: sidetrack → DeSilvaSidetrack (with title extraction)          │
│    - Handles sidetrack titles from first header                        │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. p2kb-desilva-semantic.lua                                            │
│    - Additional semantic div mappings                                  │
│    - DeSilva elements: medicine-cabinet, your-turn, sidetrack          │
│    - Uff, well, have-fun elements                                      │
│    - Also supports Smart Pins gb* elements for compatibility           │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. p2kb-desilva-code-coloring.lua                                       │
│    - Handles code block coloring with integrated mnemonic uppercasing  │
│    - 5-color DeSilva pedagogical system                                │
│    - Complete PASM2 mnemonic list (200+ instructions)                  │
│    - Uppercases mnemonics in code blocks                               │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 6. p2kb-desilva-mnemonic-bold.lua (OPTIONAL - may be integrated)        │
│    - Standalone mnemonic bolding filter                                │
│    - Conservative context detection in prose                           │
│    - May be redundant with code-coloring.lua integration               │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
LaTeX Output → PDF
```

---

## Data Flow: Pedagogical Element

```
┌─────────────────────────────────────────────────────────────────────────┐
│ MARKDOWN SOURCE                                                         │
│                                                                         │
│ # Chapter 5: The COG                                                    │
│                                                                         │
│ ::: sidetrack                                                           │
│ ### Why Eight COGs?                                                     │
│ The P2's eight COGs aren't arbitrary - they match...                    │
│ :::                                                                     │
│                                                                         │
│ ::: pasm2                                                               │
│ ```pasm2                                                                │
│ mov     pa, #0          ' Initialize counter                            │
│ add     pa, #1          ' Increment                                     │
│ ```                                                                     │
│ :::                                                                     │
│                                                                         │
│ ::: medicine                                                            │
│ If this is overwhelming, try the Spin2 approach first.                  │
│ :::                                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Pandoc + Lua Filters
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LATEX OUTPUT                                                            │
│                                                                         │
│ \chapter{Chapter 5: The COG}                                            │
│                                                                         │
│ \begin{DeSilvaSidetrack}                                                │
│ \subsection*{Why Eight COGs?}                                           │
│ The P2's eight COGs aren't arbitrary - they match...                    │
│ \end{DeSilvaSidetrack}                                                  │
│                                                                         │
│ \begin{DeSilvaPASM2Block}                                               │
│ \begin{Highlighting}                                                    │
│ MOV     pa, \#0          ' Initialize counter                           │
│ ADD     pa, \#1          ' Increment                                    │
│ \end{Highlighting}                                                      │
│ \end{DeSilvaPASM2Block}                                                 │
│                                                                         │
│ \begin{DeSilvaMedicineCabinet}                                          │
│ If this is overwhelming, try the Spin2 approach first.                  │
│ \end{DeSilvaMedicineCabinet}                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ XeLaTeX + Template Stack
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PDF OUTPUT                                                              │
│                                                                         │
│ - Chapter starts new page (except first after TOC)                     │
│ - Sidetrack: purple box with "Sidetrack" title                         │
│ - PASM2 code: yellow/cream box with thick left border                  │
│ - Mnemonics MOV, ADD uppercased                                        │
│ - Medicine Cabinet: teal box with "The Medicine Cabinet" title         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Pandoc Arguments Required

```json
{
  "pandoc_args": [
    "--top-level-division=chapter",
    "--pdf-engine=xelatex"
  ]
}
```

| Argument | Purpose |
|----------|---------|
| `--top-level-division=chapter` | Maps # → \chapter, ## → \section. Tutorial uses chapters. |
| `--pdf-engine=xelatex` | Required for fontspec and Unicode support |

**Note:** Uses `chapter` not `part` - this is a flat chapter-based tutorial, not a multi-part reference.

---

## Customization Points

### To Add a New Pedagogical Environment

1. **In `p2kb-desilva-content.sty`:** Define the environment
   ```latex
   \newtcolorbox{DeSilvaNewElement}{
     title=New Element,
     fonttitle=\bfseries\color{white},
     colbacktitle=cyan!70!black,
     colback=cyan!5,
     colframe=cyan!70!black,
     ...
   }

   % Also add lowercase variant for Lua filter
   \newtcolorbox{dsnewelement}{
     ...
   }
   ```

2. **In `p2kb-desilva-semantic.lua`:** Add mapping
   ```lua
   local divMappings = {
       ...
       ["new-element"] = "dsnewelement",
   }
   ```

3. **In markdown:** Use the div
   ```markdown
   ::: new-element
   Content here
   :::
   ```

### To Modify Code Block Colors

Edit color definitions in `p2kb-desilva-content.sty`:
```latex
\definecolor{desilva-pasm2-bg}{HTML}{FFFEF5}
\definecolor{desilva-pasm2-border}{HTML}{D4B896}
```

---

## Conversion Status

### Naming Convention Compliance

| File | Status | Notes |
|------|--------|-------|
| `p2kb-desilva.latex` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-foundation.sty` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-content.sty` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-diagrams.sty` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-pagination.lua` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-div-blocks.lua` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-semantic-blocks.lua` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-semantic.lua` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-code-coloring.lua` | ✅ Compliant | Proper prefix |
| `p2kb-desilva-mnemonic-bold.lua` | ✅ Compliant | Proper prefix |

### Self-Containment Status

✅ **Fully self-contained.** All template files are:
- Located in workspace `templates/` and `filters/` directories
- Properly prefixed with `p2kb-desilva-`
- No dependencies on shared files outside workspace

### Potential Redundancy

| Issue | Action When Active |
|-------|-------------------|
| `p2kb-desilva-code-coloring.lua` has integrated mnemonic uppercasing | Verify if `p2kb-desilva-mnemonic-bold.lua` is still needed |
| `p2kb-desilva-div-blocks.lua` vs `p2kb-desilva-semantic-blocks.lua` | May have overlapping responsibilities - review and consolidate |

---

## Unique Features (vs Other Manuals)

1. **DeSilva Pedagogical Philosophy** - Medicine Cabinet, Your Turn, Sidetrack
2. **5-Color Code System** - Spin2/PASM2/CORDIC/MultiCOG/Antipattern
3. **Chapter-Based Structure** - Flat chapters, no Parts
4. **Encouraging Voice** - "Uff!", "Well...", "Have Fun!" environments
5. **Title Extraction** - Sidetrack titles extracted from first header

---

## Differences from Smart Pins Tutorial

| Feature | DeSilva | Smart Pins |
|---------|---------|------------|
| **Top-level division** | chapter | part |
| **Code colors** | 5-color DeSilva | 3-color + config |
| **Pedagogical focus** | Encouraging, human | Technical reference |
| **Special environments** | Medicine Cabinet, Uff!, etc. | Decision trees, mode reference |
| **Frontmatter handling** | Simple pagination | Complex filter chain |
| **Primary audience** | Beginners learning PASM2 | Smart Pins users |

---

## Differences from Assembly Language Manual

| Feature | DeSilva | Assembly Manual |
|---------|---------|-----------------|
| **Purpose** | Learning tutorial | Reference lookup |
| **Spacing** | Standard (10pt parskip) | Tighter (8pt parskip) |
| **Environments** | Pedagogical (Your Turn, etc.) | Reference (At a Glance, etc.) |
| **Encoding tables** | None | tabularray-based system |
| **Mnemonic handling** | Code-integrated | Grammar-aware |
| **Font size** | 12pt | 11pt |

---

*Created: 2025-12-03*
*Document: P2 PASM DeSilva Style (Discovering P2 Assembly)*
*Template Version: 1.0*
