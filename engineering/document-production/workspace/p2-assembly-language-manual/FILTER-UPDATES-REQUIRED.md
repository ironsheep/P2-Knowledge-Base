# Filter Updates Required

**Document:** P2 Assembly Language Manual
**Purpose:** Track Lua filter and template changes needed for PDF generation
**Status:** Pending implementation

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

### Implementation Required

#### A. Lua Filter: `p2kb-pasm2-figures.lua`

Create a filter that:

1. **Detects pattern:** Raw LaTeX block followed by `.figurecaption` div
2. **Wraps in figure environment:**
   ```latex
   \begin{figure}[htbp]
   \centering
   <raw LaTeX content>
   \caption{<div content>}
   \label{<div id>}
   \end{figure}
   ```
3. **Handles the div:** Converts content to `\caption{}` and ID to `\label{}`

#### B. LaTeX Preamble Addition

Add to template or `.sty` file:

```latex
% Enable chapter-based figure numbering
\counterwithin{figure}{chapter}
```

This makes figures number as 1.1, 1.2, 2.1, etc., resetting at each chapter.

#### C. Cross-Reference Support

Once implemented, prose can reference figures using:

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

## Future Filter Updates

*(Add additional filter requirements here as they arise)*

---

*Created: 2026-01-20*
*Last Updated: 2026-01-20*
