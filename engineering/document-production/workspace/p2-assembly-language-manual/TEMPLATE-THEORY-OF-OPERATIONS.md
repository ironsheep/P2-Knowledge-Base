# Template Theory of Operations
## P2 Assembly Language (PASM2) Reference Manual

**Document:** P2-Assembly-Language-Manual.md
**Template Prefix:** `p2kb-pasm2-*`
**Status:** Fully self-contained, properly namespaced

---

## Template Stack Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    p2kb-pasm2-reference.latex                           │
│                    (Main Document Template)                             │
│  - Document class: book (11pt, letter paper, oneside)                  │
│  - Loads all .sty layers in order                                      │
│  - Sets document metadata (title, author, date)                        │
│  - Configures two-column index                                         │
│  - Contains \begin{document}...\end{document}                          │
│  - Inserts $body$ (Pandoc content)                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 1: p2kb-pasm2-foundation.sty                   │
│                    (Core Infrastructure - 278 lines)                    │
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
│  - graphicx, longtable, booktabs, array, tabularx (tables/images)      │
│  - tabularray with booktabs library (modern encoding tables)           │
│  - xcolor with table option                                            │
│  - fancyhdr, titlesec, tocloft (styling)                               │
│  - tcolorbox with skins,breakable                                      │
│  - hyperref, bookmark (PDF links)                                      │
│  - listings, fancyvrb (code blocks)                                    │
│  - enumitem (list control)                                             │
│  - environ (for capturing environment body in encoding tables)         │
│                                                                         │
│  HEADING SPACING (tighter than tutorials):                              │
│  - Chapter: -30pt before, 15pt after                                   │
│  - Section: 14pt before, 4pt after                                     │
│  - Subsection: 10pt before, 3pt after                                  │
│                                                                         │
│  PAGE LAYOUT:                                                           │
│  - Geometry: 0.75in top/bottom, 1in left/right                         │
│  - Parskip: 8pt (tighter than tutorials)                               │
│  - Linespread: 1.2 (tighter than tutorials)                            │
│                                                                         │
│  TOC CONFIGURATION:                                                     │
│  - tocdepth=1 (Chapters and Sections only)                             │
│  - secnumdepth=-1 (no auto-numbering)                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 2: p2kb-pasm2-content.sty                      │
│                    (Reference Manual Environments - 665 lines)          │
│                                                                         │
│  COLOR PALETTE:                                                         │
│  ┌─────────────────┬─────────────────┬───────────────────────────────┐ │
│  │ Purpose         │ Background      │ Border                        │ │
│  ├─────────────────┼─────────────────┼───────────────────────────────┤ │
│  │ Entry header    │ pasm2-entry-bg  │ pasm2-entry-border (#DEE2E6)  │ │
│  │ At a Glance     │ pasm2-glance-bg │ pasm2-glance-border (#1976D2) │ │
│  │ Warning         │ pasm2-warning-bg│ pasm2-warning-border (#FF9800)│ │
│  │ Note            │ pasm2-note-bg   │ pasm2-note-border (#2196F3)   │ │
│  │ Tip             │ pasm2-tip-bg    │ pasm2-tip-border (#4CAF50)    │ │
│  │ Hardware        │ pasm2-hardware-bg│pasm2-hardware-border (#9C27B0)│ │
│  │ Code            │ pasm2-code-bg   │ pasm2-code-border (#BDBDBD)   │ │
│  └─────────────────┴─────────────────┴───────────────────────────────┘ │
│                                                                         │
│  REFERENCE MANUAL ENVIRONMENTS:                                         │
│  - ataglance: Summary box at top of each entry                         │
│  - instructionentry: Optional container for visual separation          │
│  - warningbox, notebox, tipbox, hardwarebox: Callouts                  │
│  - keyconcepts: Chapter summary with bullet list                       │
│  - syntaxbox: Instruction syntax display                               │
│                                                                         │
│  ENCODING TABLE SYSTEM (tabularray-based):                              │
│  - encodingtable environment: 9-column instruction encoding            │
│  - \simpleencoding command: Single-row encoding                        │
│  - \encodingrow, \encodingrowcont: Multi-row tables                    │
│  - \inlineencoding, \encodingsnippet: Inline examples                  │
│  - Columns: EEEE, Opcode, CZI, D, S, C, Z, Result, Clks                │
│                                                                         │
│  5-COLOR DESILVA CODE BLOCKS:                                           │
│  - DeSilvaPASM2Block (yellow/cream)                                    │
│  - DeSilvaSpin2Block (green)                                           │
│  - DeSilvaCORDICBlock (purple)                                         │
│  - DeSilvaMultiCOGBlock (blue)                                         │
│  - DeSilvaAntipatternBlock (red)                                       │
│                                                                         │
│  PART/CHAPTER STYLING:                                                  │
│  - \partdivider command: Part without page break after                 │
│  - Part styling: centered, large, no auto page break after             │
│                                                                         │
│  CROSS-REFERENCE HELPERS:                                               │
│  - \instrref{name}: Hyperlink to instruction                           │
│  - \chapref{label}: Chapter reference                                  │
│  - \appref{label}: Appendix reference                                  │
│                                                                         │
│  INDEX COMMANDS:                                                        │
│  - \indexinstruction, \indexdirective, \indexconstant, \indexregister  │
│                                                                         │
│  TABLE COLUMN TYPES:                                                    │
│  - E, O, C, T: Encoding table columns                                  │
│  - N, W: 30%/70% split for description tables                          │
│  - R, M, L: Reference tables                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Layer 3: p2kb-pasm2-diagrams.sty                     │
│                    (TikZ Diagrams - ~800+ lines)                        │
│                                                                         │
│  COLOR DEFINITIONS:                                                     │
│  - Memory regions: mem-cog, mem-hub, mem-lut, mem-special              │
│  - Encoding fields: encoding-cond, encoding-op, encoding-flag, etc.    │
│  - Bit reordering: bit-byte0/1/2/3                                     │
│  - Timing: timing-active, timing-wait, timing-hub                      │
│                                                                         │
│  ARCHITECTURAL DIAGRAMS:                                                │
│  - \CogAnatomyDiagram: COG memory layout ($000-$1FF, LUT, etc.)        │
│  - \HubOverviewDiagram: 512KB Hub RAM organization                     │
│  - \EightCogDiagram: 8-COG system overview                             │
│  - \CogHubRelationDiagram: Per-COG vs shared memory                    │
│                                                                         │
│  INSTRUCTION ENCODING DIAGRAMS:                                         │
│  - \InstructionEncodingDiagram: 32-bit instruction format              │
│  - \ConditionFieldDiagram: EEEE condition encoding                     │
│  - \AddressingModeDiagram: D/S field addressing                        │
│                                                                         │
│  TIMING DIAGRAMS:                                                       │
│  - \HubAccessTimingDiagram: Egg-beater hub access pattern              │
│  - \InstructionTimingDiagram: 2-cycle base with hub extension          │
│  - \PipelineDiagram: Instruction pipeline                              │
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
│ 1. p2kb-pasm2-pagination.lua                                            │
│    - Handles page breaks between Chapters                              │
│    - Part headings use \partdivider (no page break after)              │
│    - First chapter stays on same page as Part                          │
│    - Tracks just_emitted_part flag                                     │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. p2kb-pasm2-entry-format.lua                                          │
│    - Converts Markdown --- to tight LaTeX horizontal rules             │
│    - Uses negative vspace to counter paragraph spacing                 │
│    - Processes multiple instruction syntax forms                       │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. p2kb-pasm2-tables.lua                                                │
│    - Makes content tables full width                                   │
│    - Content-aware column width selection                              │
│    - EXCLUDES 9-column encoding tables (handled by template)           │
│    - Short columns get minimal width, descriptions get maximum         │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. p2kb-pasm2-code-coloring.lua                                         │
│    - Converts div-wrapped code blocks to colored environments          │
│    - 5-color DeSilva pedagogical system:                               │
│      ::: spin2 → DeSilvaSpin2Block (green)                             │
│      ::: pasm2 → DeSilvaPASM2Block (yellow)                            │
│      ::: cordic → DeSilvaCORDICBlock (purple)                          │
│      ::: multicog → DeSilvaMultiCOGBlock (blue)                        │
│      ::: antipattern → DeSilvaAntipatternBlock (red)                   │
│    - Integrated mnemonic uppercasing                                   │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. p2kb-pasm2-mnemonic-bold.lua                                         │
│    - Grammar-aware PASM2 mnemonic detection                            │
│    - Code blocks: UPPERCASE all mnemonics                              │
│    - Inline code: UPPERCASE all mnemonics                              │
│    - Prose: BOLD+UPPERCASE with false positive filtering               │
│    - Avoids "and", "or", "not" in normal English context               │
└─────────────────────────────────────────────────────────────────────────┘
     │
     ▼
LaTeX Output → PDF
```

---

## Data Flow: Instruction Entry

```
┌─────────────────────────────────────────────────────────────────────────┐
│ MARKDOWN SOURCE (Instruction Entry)                                     │
│                                                                         │
│ ### ABS                                                                 │
│                                                                         │
│ ::: ataglance                                                           │
│ Get absolute value of S into D                                          │
│ :::                                                                     │
│                                                                         │
│ **Syntax:** `ABS D,S{#} {WC,WZ}`                                        │
│                                                                         │
│ ---                                                                     │
│                                                                         │
│ **Description:** The `ABS` instruction computes...                      │
│                                                                         │
│ ::: pasm2                                                               │
│ ```pasm2                                                                │
│ abs     result, value  wc                                               │
│ ```                                                                     │
│ :::                                                                     │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Pandoc + Lua Filters
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LATEX OUTPUT                                                            │
│                                                                         │
│ \subsection{ABS}                                                        │
│                                                                         │
│ \begin{ataglance}                                                       │
│ Get absolute value of S into D                                          │
│ \end{ataglance}                                                         │
│                                                                         │
│ \textbf{Syntax:} \texttt{ABS D,S\{\#\} \{WC,WZ\}}                       │
│                                                                         │
│ \vspace{-\parskip}\vspace{-2pt}\noindent\rule{\linewidth}{0.4pt}...    │
│                                                                         │
│ \textbf{Description:} The \textbf{ABS} instruction computes...         │
│                                                                         │
│ \begin{DeSilvaPASM2Block}                                               │
│ \begin{Highlighting}                                                    │
│ ABS     result, value  WC                                               │
│ \end{Highlighting}                                                      │
│ \end{DeSilvaPASM2Block}                                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ XeLaTeX + Template Stack
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PDF OUTPUT                                                              │
│                                                                         │
│ - ABS as subsection heading                                            │
│ - Blue "At a Glance" box with summary                                  │
│ - Tight horizontal rule separating syntax from description             │
│ - Mnemonic "ABS" bold in prose                                         │
│ - Yellow code block with "ABS" uppercased                              │
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
| `--top-level-division=chapter` | Maps # → \chapter, ## → \section. Reference manual uses chapters, not parts. |
| `--pdf-engine=xelatex` | Required for fontspec and Unicode support |

**Note:** Unlike Smart Pins (which uses `--top-level-division=part`), this manual uses chapter-based division.

---

## Customization Points

### To Add a New Callout Type

1. **In `p2kb-pasm2-content.sty`:** Define colors and tcolorbox
   ```latex
   \definecolor{pasm2-newtype-bg}{HTML}{...}
   \definecolor{pasm2-newtype-border}{HTML}{...}

   \newtcolorbox{newtypebox}{
     colback=pasm2-newtype-bg,
     colframe=pasm2-newtype-border,
     ...
   }
   ```

2. **In markdown:** Use the environment
   ```markdown
   ::: newtypebox
   Content here
   :::
   ```

### To Modify Encoding Table Format

Edit `p2kb-pasm2-content.sty` in the `encodingtable` environment definition. The table uses tabularray with expand key for proper macro expansion.

### To Add a New TikZ Diagram

1. **In `p2kb-pasm2-diagrams.sty`:** Add new command
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

---

## Conversion Status

### Naming Convention Compliance

| File | Status | Notes |
|------|--------|-------|
| `p2kb-pasm2-reference.latex` | ✅ Compliant | Proper prefix |
| `p2kb-pasm2-foundation.sty` | ✅ Compliant | Proper prefix |
| `p2kb-pasm2-content.sty` | ✅ Compliant | Proper prefix |
| `p2kb-pasm2-diagrams.sty` | ✅ Compliant | Proper prefix |
| `p2kb-pasm2-pagination.lua` | ✅ Compliant | Proper prefix |
| `p2kb-pasm2-entry-format.lua` | ✅ Compliant | Proper prefix |
| `p2kb-pasm2-tables.lua` | ✅ Compliant | Proper prefix |
| `p2kb-pasm2-code-coloring.lua` | ✅ Compliant | Proper prefix |
| `p2kb-pasm2-mnemonic-bold.lua` | ✅ Compliant | Proper prefix |

### Self-Containment Status

✅ **Fully self-contained.** All template files are:
- Located in workspace `templates/` and `filters/` directories
- Properly prefixed with `p2kb-pasm2-`
- No dependencies on shared files outside workspace

---

## Unique Features (vs Other Manuals)

1. **Encoding Table System** - tabularray-based 9-column instruction encoding
2. **At a Glance Boxes** - Summary at top of each instruction entry
3. **5-Color Code System** - PASM2/Spin2/CORDIC/MultiCOG/Antipattern
4. **Grammar-Aware Mnemonic Detection** - Avoids "and", "or", "not" false positives
5. **Tight Horizontal Rules** - Entry section separators with negative vspace
6. **Chapter-Based Structure** - Uses `--top-level-division=chapter` not `part`
7. **Index Commands** - Type-specific index entries (instruction, directive, etc.)

---

## Differences from Smart Pins Tutorial

| Feature | Assembly Manual | Smart Pins |
|---------|-----------------|------------|
| **Top-level division** | chapter | part |
| **Code colors** | 5-color DeSilva | 3-color + config |
| **Primary purpose** | Reference lookup | Learning tutorial |
| **Spacing** | Tighter (8pt parskip) | Standard (10pt parskip) |
| **Special tables** | Encoding tables | Decision trees |
| **Mnemonic handling** | Grammar-aware bold | N/A |
| **Index system** | Type-specific commands | Standard |

---

*Created: 2025-12-03*
*Document: P2 Assembly Language Reference Manual*
*Template Version: 1.0*
