# Filter Updates Required

**Document:** P2 Assembly Language Manual
**Purpose:** Track Lua filter and template changes needed for PDF generation
**Status:** ✅ IMPLEMENTED (2026-01-20)

---

## 1. Figure Numbering System

**Requirement:** Implement chapter-based figure numbering (Figure X.Y format)

**Source:** Rayman review feedback (C1) - "figures should have numbers so they can be referred to"

### Markdown Format Added

Figure captions are marked in the opus-master using Pandoc fenced divs:

```markdown
```{=latex}
\DiagramMacroName
```

::: {.figurecaption #fig:descriptive-id}
Caption Text Here
:::
```

### Figures Added (10 total)

| Location | ID | Caption |
|----------|-----|---------|
| Chapter 1 | `#fig:eight-cog-overview` | Eight-COG Architecture Overview |
| Chapter 1 | `#fig:cog-memory-map` | COG Memory Map |
| Chapter 1 | `#fig:lut-memory-map` | LUT Memory Map |
| Chapter 1 | `#fig:hub-memory-map` | Hub Memory Organization |
| Chapter 4 | `#fig:egg-beater` | Hub Access Rotation ("Egg Beater") |
| Appendix D | `#fig:special-registers-map` | Special Registers Memory Map ($1F0–$1FF) |
| Directives | `#fig:alignl-before` | Memory Layout Before ALIGNL |
| Directives | `#fig:alignl-after` | Memory Layout After ALIGNL |
| Directives | `#fig:alignw-before` | Memory Layout Before ALIGNW |
| Directives | `#fig:alignw-after` | Memory Layout After ALIGNW |

### Implementation ✅ COMPLETE

#### A. Lua Filter: `p2kb-pasm2-figures.lua` ✅

**Created:** `filters/p2kb-pasm2-figures.lua`

The filter:
1. Detects RawBlock (latex) followed by `.figurecaption` Div
2. Wraps them in `\begin{figure}[H]...\end{figure}`
3. Extracts caption text and label ID from the Div

**Added to:** `request.json` lua_filters array (first position)

#### B. LaTeX Preamble Addition ✅

**Added to:** `templates/p2kb-pasm2-foundation.sty` (after line 75)

```latex
% ==================== FIGURE NUMBERING ====================
% Chapter-based figure numbering: Figure 1.1, 1.2, 2.1, etc.
% Implements Rayman review item C1
\counterwithin{figure}{chapter}
```

#### C. Cross-Reference Support

Prose can now reference figures using:

```markdown
As shown in Figure \ref{fig:eight-cog-overview}, the P2 contains...
```

Or with pandoc-crossref (if enabled):

```markdown
As shown in @fig:eight-cog-overview, the P2 contains...
```

### Numbering Scheme

| Document Section | Figure Number Format |
|------------------|---------------------|
| Part I chapters | Figure 1.1, 1.2, 2.1, 4.1, etc. |
| Part II (Directives) | TBD - may use "Figure D.1" or sequential |
| Part III (Appendices) | TBD - may use "Figure D.1" for Appendix D |

**Decision needed:** How to number figures in non-chapter sections (Part II, Part III). Options:
- Continue sequential from Part I (Figure 6.1, 6.2...)
- Use section letters (Figure D.1 for Directives, Figure AD.1 for Appendix D)
- Simple sequential throughout document (Figure 1, 2, 3...)

---

## Files to Deploy to Outbound

The following files were modified/created and need to be copied to outbound for PDF Forge:

| File | Type | Action |
|------|------|--------|
| `filters/p2kb-pasm2-figures.lua` | New filter | Copy to outbound (flat) |
| `templates/p2kb-pasm2-foundation.sty` | Modified | Copy to outbound (flat) |
| `request.json` | Modified | Copy to outbound |

**Note:** The markdown content with `.figurecaption` divs is in the opus-master files. When the manual is assembled and escaped, those divs will be included automatically.

---

## Future Filter Updates

*(Add additional filter requirements here as they arise)*

---

*Created: 2026-01-20*
*Last Updated: 2026-01-20*
