# PDF Formatting Decisions - Technical Reasoning

## Document Purpose
This document captures architectural decisions about PDF formatting approaches, explaining WHY certain choices were made for future maintainers and document creators.

## Key Decision: Baked-in Formatting vs. Semantic Tagging

### The Decision
For pedagogical documents, we use **baked-in formatting** (literally writing **MOV** in markdown) rather than semantic tagging (\pasm{mov} with stylesheet processing).

### Technical Reasoning

#### Why NOT Semantic Tagging
1. **LaTeX Verbatim Limitation**: Code blocks use verbatim/lstlisting environments where LaTeX commands are treated as literal text. `\pasm{mov}` would appear in the output instead of being processed.

2. **Toolchain Complexity**: Adding semantic processing requires:
   - Custom Pandoc filters (Lua/Python)
   - Complex listings package configuration
   - Additional escaping rules
   - More failure points

3. **Case Transformation Challenges**: Getting listings package to do case-insensitive matching with uppercase output is non-trivial and fragile.

#### Why Baked-in Formatting Works

1. **Pedagogical Clarity**: In teaching documents, formatting IS meaning. **UPPERCASE + BOLD** isn't just style—it's teaching "these are COMMANDS with POWER."

2. **What You See Is What You Get**: No surprises between markdown and PDF. The author sees exactly what students will see.

3. **Zero Toolchain Risk**: No custom filters, no LaTeX magic, no escaping issues. Pandoc and LaTeX just pass it through.

4. **Philosophical Alignment**: For documents where the presentation IS the pedagogy, baking in the format is actually more honest than pretending it's separable.

### The Hybrid Approach

We maintain TWO versions:
```
source/part1.md          → lowercase, clean for editing
generated/part1-PASM.md  → **UPPERCASE**, for PDF generation
```

Benefits:
- Clean source for version control
- Formatted version for production
- Can regenerate anytime
- Best of both worlds

### When to Use Each Approach

#### Use Baked-in Formatting When:
- Document is pedagogical (teaching through formatting)
- Formatting conveys semantic meaning
- Consistency is absolutely critical
- Document is final/published (not draft)

#### Use Semantic Tagging When:
- Document is reference material
- Multiple output formats needed
- Style might change frequently
- Content is more important than presentation

## Key Decision: Code Block Coloring Consistency

### The Decision
Code blocks are ALWAYS yellow (`FFFACD`), even inside colored boxes (gray sidetracks, green chapter ends, etc.).

### Reasoning

1. **Visual Consistency**: Readers learn "yellow = code" and this NEVER changes, reducing cognitive load.

2. **Hierarchical Clarity**: Code is primary content that happens to be inside a box, not subordinate to the box.

3. **deSilva Precedent**: Original P1 manual maintained code coloring inside other environments.

4. **Implementation Simplicity**: Don't override code block styling in box environments.

### Technical Implementation
```latex
% Code blocks maintain their color everywhere
\lstset{
  backgroundcolor=\color{inlineyellow},  % ALWAYS this color
  % ... other settings
}

% Box environments don't override code coloring
\newtcolorbox{sidetrack}{
  colback=codegray,
  % No code color override
}
```

## Key Decision: Instruction Mnemonic Formatting

### The Rule
ALL PASM2 instruction mnemonics are **UPPERCASE + BOLD** everywhere:
- In prose text
- In code blocks  
- In boxes
- In tables
- NO EXCEPTIONS

### Why This Extreme Consistency?

1. **Cognitive Load Reduction**: Any inconsistency makes readers ask "why?" instead of learning "what."

2. **Visual Scanning**: Bold uppercase instructions jump out immediately, improving code readability.

3. **Language Properties**: PASM2 is case-insensitive, so we can optimize for pedagogy rather than syntax.

4. **Teaching Through Form**: The formatting teaches "these are COMMANDS" not just text.

### Implementation Note
Since PASM2 accepts both cases, we choose the case that best serves learning. This is a pedagogical choice, not a technical requirement.

## Document Maintenance Strategy

### Source Control
```
/sources/               → Original lowercase markdown
/generated/            → Processed **UPPERCASE** markdown  
/exports/              → Final PDFs
```

### Processing Pipeline
1. Edit in `/sources/` (clean, lowercase)
2. Run formatting script → `/generated/`
3. Run Pandoc + LaTeX → `/exports/`

### Why This Pipeline?
- Clean diffs in git (source files unchanged)
- Regeneratable output (script is deterministic)
- Clear separation of concerns
- Easy to update formatting rules

## Lessons Learned

### What Worked
1. **Testing early**: Discovering LaTeX verbatim limitations early saved time
2. **Documenting decisions**: This document prevents re-litigating choices
3. **Hybrid approach**: Keeping both clean and formatted versions

### What To Avoid
1. **Over-engineering**: Semantic tagging sounds clean but adds complexity
2. **Assuming LaTeX magic**: Code blocks are special environments with limitations
3. **Inconsistent formatting**: Even minor inconsistencies distract from learning

## Future Considerations

### If Moving to HTML/Web
- Would need different approach (CSS can handle semantic tagging)
- Consider markdown-it plugins for instruction highlighting
- Keep source lowercase for flexibility

### If Creating Reference Docs
- Semantic tagging becomes more valuable
- Style changes more likely
- Consider listings package approach

### For Other Languages
- Case-sensitive languages: Must preserve original case
- Different formatting approach needed
- Consider syntax highlighting instead

---

*This document is part of the P2KB documentation pipeline standards.*