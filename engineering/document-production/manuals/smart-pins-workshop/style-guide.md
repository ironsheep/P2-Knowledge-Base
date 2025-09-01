# Smart Pins Documentation Style Guide

## Document Variants

### Blue Book (Reference Manual)
**Purpose**: Quick reference for experienced developers
**Characteristics**:
- Minimal narrative
- Dense information presentation
- Bold, high-contrast colors for scanning
- Emphasis on specifications and formulas
- One example per mode

### Green Book (Tutorial Guide)
**Purpose**: Progressive learning for all skill levels
**Characteristics**:
- Rich narrative and explanations
- Comfortable reading typography
- Soft, pastel colors for extended reading
- Multiple examples with progression
- Exercises and troubleshooting

## Visual Design Philosophy

### Color Strategy Comparison

| Element | Blue Book (Reference) | Green Book (Tutorial) |
|---------|----------------------|----------------------|
| **Philosophy** | High contrast for scanning | Comfort for extended reading |
| **Code Blocks** | Bold colors with strong borders | Pastel backgrounds with subtle borders |
| **Emphasis** | Vibrant highlights | Soft accents |
| **Semantic Markers** | N/A (complete content) | Title bars with distinct borders |

### Typography Decisions

**Blue Book**:
- 10pt body text (information density)
- 1.2x line spacing (compact)
- Narrow margins (maximize content)

**Green Book**:
- 10.5pt body text (5% larger for comfort)
- 1.25x line spacing (breathing room)
- Digital-first margins (0.75" standard, 1" binding)

### Semantic Markers (Green Book Only)

Seven distinct visual treatments for content gaps:

1. **needs-diagram** - Amber title bar, dashed border
2. **preliminary-content** - Gray title bar, dotted border
3. **needs-verification** - Sky blue title bar, dashed border
4. **needs-examples** - Leaf green title bar, solid border
5. **needs-technical-review** - Rose title bar, dashed border
6. **needs-code-review** - Orange title bar, dotted border
7. **tip** - Green title bar, solid rounded border

**Design Principles**:
- Full borders (vs left-only for code blocks)
- Title bars for clear identification
- Border styles aid accessibility (solid/dashed/dotted)
- Text labels over icons (clarity over decoration)

## Rationale for Design Choices

### Why Pastel Colors for Green Book?
- **Reduced eye strain** during extended reading sessions
- **Better for learning** - less distraction from content
- **Accessibility** - easier for color-sensitive readers
- **Print-friendly** - uses less ink, better reproduction

### Why Different Border Styles?
- **Visual accessibility** - pattern differentiation for colorblind readers
- **Semantic grouping** - dashed = needs work, solid = informational
- **Visual hierarchy** - full borders for gaps, left borders for code
- **Professional appearance** - consistent but not monotonous

### Why Title Bars for Semantic Markers?
- **Clear identification** without reading content
- **Scannable** - quickly find all gaps of a type
- **Professional** - like technical documentation standards
- **Accessible** - text is screen-reader friendly

## Implementation References

### Key Files
- **Visual Specifications**: `/exports/pdf-generation/workspace/smart-pins-manual/green-book-visual-specifications.md`
- **Creation Guide**: `/documentation/manuals/smart-pins-workshop/creation-guide.md`
- **Pipeline Guide**: `/documentation/pipelines/pdf-generation-format-guide.md`

### Template Stack
```
p2kb-foundation.sty          # Base Pandoc fixes
    ↓
p2kb-smart-pins-content.sty  # Colors and environments
    ↓
p2kb-tech-review.sty         # Presentation layer
```

### Lua Filter Pipeline
```
smart-pins-colored-blocks.lua    # Code block coloring
    ↓
green-book-semantic-blocks.lua   # Semantic marker conversion
    ↓
part-chapter-pagebreaks.lua      # Structure formatting
```

## Version History

- **2025-08-30**: Initial style guide created
- **Design Session**: Interactive planning with user (Opus 4.1)
- **Implementation**: Specifications for Sonnet 4

## Future Considerations

### Potential Enhancements
- Chapter thumb indices for printed version
- Progress indicators at chapter starts
- QR codes linking to online resources
- Interactive PDF features for digital version

### Maintenance Notes
- Colors calibrated for both screen and print
- Tested with colorblind simulation tools
- Compatible with PDF/A archival standards
- Supports high-contrast mode overrides

---

This style guide documents the visual design decisions made for the P2 Smart Pins documentation suite, ensuring consistency across both reference and tutorial materials.