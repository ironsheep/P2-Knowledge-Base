# Semantic Types Manifest
## P2 Smart Pins Green Book Tutorial

Generated: 2025-08-30

## Used Semantic Types

### Content Gap Markers

1. **`needs-diagram`** - Used 1 time
   - Purpose: Indicates where visual diagrams are needed
   - Example: Smart Pin internal block diagram
   - Suggested styling: Light yellow background with diagram icon

2. **`needs-code-review`** - Used 1 time
   - Purpose: Marks code that needs verification
   - Example: Sine wave generation accuracy
   - Suggested styling: Light orange background with checkmark icon

3. **`needs-technical-review`** - Used 2 times
   - Purpose: Technical specifications needing validation
   - Example: ADC calibration temperature effects, electrical specs
   - Suggested styling: Light red background with warning icon

4. **`preliminary-content`** - Used 3 times
   - Purpose: Content that's incomplete pending more information
   - Example: USB mode, SMPS mode, Scope mode
   - Suggested styling: Light gray background with "beta" badge

5. **`needs-examples`** - Used 1 time
   - Purpose: Sections that would benefit from more examples
   - Example: Community projects section
   - Suggested styling: Light green background with code icon

6. **`needs-verification`** - Used 1 time
   - Purpose: Information that needs fact-checking
   - Example: P_ constant list
   - Suggested styling: Light blue background with question mark icon

### Instructional Elements

7. **`tip`** - Used 1 time
   - Purpose: Helpful tips and best practices
   - Example: Repository mode for COG synchronization
   - Suggested styling: Green border with lightbulb icon

## Semantic Type Categories

### Gap Markers (6 types)
- Technical gaps that need filling
- Visual styling should indicate severity/type
- Colors: Yellow (visual), Orange (code), Red (technical), Gray (preliminary), Green (examples), Blue (verification)

### Instructional (1 type)
- Teaching aids and helpful hints
- Visual styling should be encouraging
- Color: Green for positive reinforcement

## Implementation Notes

### For LaTeX/PDF Generation

Each semantic type should map to a LaTeX environment:

```latex
% Example environment definitions
\newenvironment{needsdiagram}{%
  \begin{tcolorbox}[colback=yellow!10,colframe=yellow!50,title=Diagram Needed]
}{%
  \end{tcolorbox}
}

\newenvironment{preliminarycontent}{%
  \begin{tcolorbox}[colback=gray!10,colframe=gray!50,title=Preliminary Content]
}{%
  \end{tcolorbox}
}
```

### For Lua Filter Processing

The Lua filter should convert markdown divs to LaTeX environments:

```lua
function Div(el)
  if el.classes[1] == "needs-diagram" then
    return {
      pandoc.RawBlock('latex', '\\begin{needsdiagram}'),
      el,
      pandoc.RawBlock('latex', '\\end{needsdiagram}')
    }
  end
  -- Continue for other types...
end
```

## Statistics

- **Total semantic markers used**: 10 instances
- **Unique semantic types**: 7 types
- **Most common**: `preliminary-content` (3 uses)
- **Categories**: 2 (Gap Markers, Instructional)

## Recommendations

1. **Visual Hierarchy**: Use color intensity to indicate severity
   - Light tints for informational
   - Medium saturation for important
   - Strong colors for critical

2. **Icon System**: Use consistent icons
   - 📊 for diagrams
   - ✓ for review needed
   - ⚠️ for technical review
   - 🔬 for preliminary
   - 💡 for tips
   - ❓ for verification

3. **Production vs Development**: 
   - In development: Show all markers prominently
   - In production: Consider hiding or styling more subtly

## Future Semantic Types to Consider

Based on content patterns, these semantic types might be useful:

- `hardware-note`: For hardware-specific considerations
- `performance-tip`: For optimization advice
- `common-mistake`: For typical errors and solutions
- `advanced-technique`: For expert-level content
- `cross-reference`: For linking related content

## Validation Checklist

- [ ] All semantic divs have closing markers
- [ ] No nested semantic divs
- [ ] Semantic types are used consistently
- [ ] All types listed here are defined in templates
- [ ] Lua filter handles all types

---

This manifest provides complete documentation of semantic types used in the P2 Smart Pins Green Book Tutorial for proper styling and processing.