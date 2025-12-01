# PASM2 Reference Manual - Template Documentation

## Template Prefix
**Prefix:** `p2kb-pasm2-*`
**Purpose:** Complete PASM2 Assembly Language Reference Manual
**Status:** Production ready

## Template Stack

```
p2kb-pasm2-reference.latex     (Main template)
    |
    +-- p2kb-pasm2-foundation.sty   (Pandoc compatibility, core setup)
    |
    +-- p2kb-pasm2-content.sty      (Reference manual environments)
    |
    +-- p2kb-pasm2-diagrams.sty     (TikZ diagram macros - 24 diagrams)
```

## File Inventory

| File | Purpose | Lines |
|------|---------|-------|
| `p2kb-pasm2-reference.latex` | Main document template | ~70 |
| `p2kb-pasm2-foundation.sty` | Pandoc compat, fonts, headers | ~230 |
| `p2kb-pasm2-content.sty` | Reference environments, colors | ~280 |
| `p2kb-pasm2-diagrams.sty` | TikZ diagrams | ~900+ |
| `p2kb-foundation.sty` | Shared foundation (if needed) | ~200 |

## Diagram Macros Available

### Part I: Architectural (from DeSilva + new)
- `\CogAnatomyDiagram` - COG memory layout
- `\HubMemoryDiagram` - Hub 512KB layout
- `\EggBeaterDiagram` - P1 vs P2 hub access timing
- `\InstructionAnatomyDiagram` - PASM2 instruction format
- `\InstructionExampleDiagram` - Concrete instruction example
- `\EightCogOverviewDiagram` - 8 COGs connected to Hub
- `\CogMemoryMapDiagram` - COG $000-$1FF layout
- `\LutMemoryMapDiagram` - LUT $200-$3FF layout
- `\CogHubRelationshipDiagram` - Memory hierarchy
- `\SpecialRegistersMapDiagram` - $1F0-$1FF detail

### Part I: Timing
- `\HubWindowTimingDiagram` - Egg beater rotation timing
- `\InstructionTimingDiagram` - 2-cycle base with hub extension
- `\BranchTimingDiagram` - Branch taken vs not taken

### Part I: Flags & Hardware
- `\FlagFlowDiagram` - WC/WZ flag modification
- `\CordicOperationDiagram` - CORDIC pipeline
- `\InterruptPriorityDiagram` - INT1/2/3 priority levels

### Part II: Instruction Encoding
- `\InstructionEncoding{NAME}{EEEE}{OPCODE}{CZI}{DEST}{SRC}` - Universal encoding diagram

### Part II: Bit Reordering
- `\SplitBDiagram` - SPLITB operation
- `\RevDiagram` - REV bit reversal
- `\MovbytsDiagram{pattern}` - MOVBYTS shuffle
- `\RolByteDiagram` - ROLBYTE rotation
- `\SetByteDiagram` - SETBYTE insertion
- `\BitValueBar{value}` - 32-bit value display

### Part II: Directives
- `\AlignWDiagram` - ALIGNW word alignment
- `\AlignLDiagram` - ALIGNL long alignment
- `\MemoryMap{title}{content}` - Generic memory map

### Part II: Register Fields
- `\CoginitDestFieldDiagram` - COGINIT dest field
- `\DirRegisterFieldDiagram` - DIRA/DIRB layout
- `\RegisterBitField{name}{width}{content}` - Generic bit field

## Content Environments

### Callout Boxes
```latex
\begin{warningbox}
Warning content here
\end{warningbox}

\begin{notebox}
Note content here
\end{notebox}

\begin{tipbox}
Tip content here
\end{tipbox}

\begin{hardwarebox}
Hardware-specific note here
\end{hardwarebox}
```

### At a Glance
```latex
\begin{ataglance}
Quick summary of instruction
\end{ataglance}
```

### Syntax Display
```latex
\begin{syntaxbox}
\texttt{ADD D, S/\#n}
\end{syntaxbox}
```

## Usage in Markdown

### Embedding Diagrams
```markdown
```{=latex}
\EggBeaterDiagram
```
```

### Instruction Encoding
```markdown
```{=latex}
\InstructionEncoding{ADD}{EEEE}{0001000}{CZI}{DDDDDDDDD}{SSSSSSSSS}
```
```

## PDF Generation

### Prerequisites on PDF Forge
- XeLaTeX with Latin Modern fonts
- TikZ with libraries: shapes.geometric, arrows.meta, positioning, calc, decorations.pathreplacing, patterns, fit
- tcolorbox with skins, breakable
- All template files in same directory

### Command
```bash
pandoc P2-Assembly-Language-Manual.md \
  --template=p2kb-pasm2-reference.latex \
  --pdf-engine=xelatex \
  --top-level-division=chapter \
  --toc \
  --toc-depth=2 \
  -o P2-Assembly-Language-Manual.pdf
```

## Color Palette

### Entry Structure
- `pasm2-entry-header` (#2C3E50) - Dark blue-gray headers
- `pasm2-entry-bg` (#F8F9FA) - Light gray background
- `pasm2-glance-bg` (#E3F2FD) - Light blue for At a Glance

### Callouts
- `pasm2-warning-*` - Orange theme
- `pasm2-note-*` - Blue theme
- `pasm2-tip-*` - Green theme
- `pasm2-hardware-*` - Purple theme

### Diagram Colors
- `mem-cog` (#E0F0E0) - COG memory (light green)
- `mem-hub` (#E0E0F0) - Hub memory (light blue)
- `mem-lut` (#F0E0E0) - LUT memory (light red)
- `mem-special` (#F0F0E0) - Special registers (light yellow)
- `encoding-*` - Instruction field colors

---

*Created: 2025-12-01*
*Template Version: 1.0*
