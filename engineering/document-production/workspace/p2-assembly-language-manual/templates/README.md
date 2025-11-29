# Templates - P2 Assembly Language Manual

**Purpose:** LaTeX template stack for PDF generation via PDF Forge.

---

## Template Files

| File | Purpose | Status |
|------|---------|--------|
| `p2kb-pasm2-reference.latex` | Main document template | **Complete** |
| `p2kb-pasm2-diagrams.sty` | TikZ macro definitions | **Complete** |

---

## Template Architecture

### p2kb-pasm2-reference.latex

The main template defines:

- **Document class and geometry** - Page size, margins
- **Color palette** - All colors from style-guide Section 9
- **Typography** - Fonts, heading styles
- **Custom environments** - At-a-glance boxes, note callouts, code blocks
- **Encoding table styling** - Column widths, header formatting
- **Package imports** - TikZ, colortbl, booktabs, etc.

#### Encoding Table Macros

| Macro | Purpose |
|-------|---------|
| `\begin{encodingtable}...\end{encodingtable}` | Full encoding table environment |
| `\encodingrow{9 args}` | Table row with bottom border |
| `\encodingrowcont{9 args}` | Table row without border (for multi-row) |
| `\simpleencoding{9 args}` | Quick single-row encoding table |

**Arguments (9 total):** COND, INSTR, FX, DEST, SRC, Write, CFlag, ZFlag, Clocks

### p2kb-pasm2-diagrams.sty

TikZ macro definitions for:

| Macro | Purpose |
|-------|---------|
| `\InstructionEncoding{}` | 32-bit instruction encoding diagram |
| `\MemoryMap{}` | Vertical memory layout diagrams |
| `\MemoryRegion{}` | Inline memory reference (compact) |
| `\BitReorder{}` | Before/after bit manipulation diagrams |
| `\RegisterMap{}` | Special register bit field layouts |

---

## Usage in Markdown

Invoke TikZ macros using LaTeX passthrough:

```markdown
```{=latex}
\InstructionEncoding{ADD}{EEEE}{0001000}{CZI}{DDDDDDDDD}{SSSSSSSSS}
```
```

---

## Color Palette Reference

Defined in template, matching style-guide Section 9.1:

**Primary Palette:**
- `p2kb-dark` (#2C3E50) - Headers, emphasis
- `p2kb-medium` (#7F8C8D) - Secondary text
- `p2kb-light` (#ECF0F1) - Backgrounds
- `p2kb-accent` (#3498DB) - Links, highlights

**Encoding Diagram Colors:**
- `encoding-cond` (#E8E8E8) - Condition field
- `encoding-op` (#D0D0D0) - Opcode field
- `encoding-flag` (#E8E0E0) - Flag field
- `encoding-dest` (#E0E8E0) - Destination field
- `encoding-src` (#E0E0E8) - Source field

**Note Colors:**
- `pitfall-bg` (#FFF3E0) - Warning backgrounds
- `tip-bg` (#E3F2FD) - Tip backgrounds
- `hardware-bg` (#F5F5F5) - Hardware note backgrounds

---

## PDF Forge Deployment

When deploying to PDF Forge:

1. Copy `p2kb-pasm2-reference.latex` to PDF Forge templates
2. Copy `p2kb-pasm2-diagrams.sty` to PDF Forge templates
3. Ensure both files are in same directory as input markdown
4. PDF Forge will use these for rendering

---

*Created: 2025-11-28*
*Sprint: PASM2 Manual Generation Phase 0*
