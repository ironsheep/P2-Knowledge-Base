# Green Book Visual Design Specifications
## For Sonnet Implementation

Generated: 2025-08-30
Purpose: Exact specifications for implementing Green Book visual design in LaTeX/Lua

---

## 1. Typography Settings

### Base Font Configuration
```latex
\setmainfont{Linux Libertine O}  % Or similar serif font
\setsansfont{Calibri}            % For headers
\setmonofont{Consolas}           % For code

% Font sizes
\renewcommand{\normalsize}{\fontsize{10.5pt}{13.125pt}\selectfont}  % Body text
\renewcommand{\small}{\fontsize{9pt}{11pt}\selectfont}              % Code blocks
\renewcommand{\large}{\fontsize{12pt}{14pt}\selectfont}             % Section heads
```

### Line Spacing
```latex
\linespread{1.25}  % 1.25x line spacing for readability
```

---

## 2. Page Layout

### Geometry Settings
```latex
\usepackage[
    paperwidth=8.5in,
    paperheight=11in,
    top=0.75in,
    bottom=0.75in,
    outer=0.75in,
    inner=1in,        % Extra 0.25" for binding
    headheight=15pt,
    headsep=10pt,
    footskip=25pt
]{geometry}
```

---

## 3. Code Block Colors

### Existing Code Block Styles (Keep As-Is)
```latex
% Configuration blocks - Light blue with navy left border
\newtcolorbox{ConfigBlock}{
    colback=blue!3!white,      % #E8F4F8 equivalent
    colframe=blue!50!black,    % Navy border
    boxrule=0pt,
    leftrule=3pt,
    arc=0pt,
    outer arc=0pt
}

% Spin2 blocks - Light green with forest left border  
\newtcolorbox{Spin2Block}{
    colback=green!3!white,     % #F0F8F0 equivalent
    colframe=green!50!black,   % Forest border
    boxrule=0pt,
    leftrule=3pt,
    arc=0pt,
    outer arc=0pt
}

% PASM2 blocks - Light cream with golden left border
\newtcolorbox{PASM2Block}{
    colback=yellow!3!white,    % #FFFEF5 equivalent
    colframe=yellow!50!black,  % Golden border
    boxrule=0pt,
    leftrule=3pt,
    arc=0pt,
    outer arc=0pt
}
```

---

## 4. Semantic Marker Environments

### Design Pattern for All Semantic Markers
Each marker has:
- Full border (not just left edge)
- Title bar with darker color
- Body with light background
- Distinct border style for accessibility

### Implementation for Each Marker

```latex
% needs-diagram - Amber with dashed border
\newtcolorbox{gbdiagram}{  % ACTUAL NAME: gbdiagram (renamed to avoid conflicts)
    colback=yellow!5!white,        % #FFF8E1 - cream background
    colframe=orange!70!yellow,     % #FFB300 - amber border
    coltitle=white,
    fonttitle=\bfseries,
    title={Diagram Needed},
    boxrule=1.5pt,
    arc=2pt,
    outer arc=2pt,
    borderline={1.5pt}{0pt}{orange!70!yellow, dashed}
}

% preliminary-content - Gray with dotted border
\newtcolorbox{gbpreliminary}{  % ACTUAL NAME: gbpreliminary (renamed to avoid conflicts)
    colback=gray!5!white,          % #F5F5F5 - light gray
    colframe=gray!60!black,        % #757575 - dark gray
    coltitle=white,
    fonttitle=\bfseries,
    title={Preliminary Content},
    boxrule=1.5pt,
    arc=2pt,
    outer arc=2pt,
    borderline={1.5pt}{0pt}{gray!60!black, dotted}
}

% needs-verification - Pale blue with dashed border
\newtcolorbox{gbverify}{  % ACTUAL NAME: gbverify (renamed to avoid conflicts)
    colback=cyan!5!white,          % #E3F7FF - pale blue
    colframe=cyan!50!blue,         % #4FC3F7 - sky blue
    coltitle=white,
    fonttitle=\bfseries,
    title={Needs Verification},
    boxrule=1.5pt,
    arc=2pt,
    outer arc=2pt,
    borderline={1.5pt}{0pt}{cyan!50!blue, dashed}
}

% needs-examples - Pale green with solid border
\newtcolorbox{gbexamples}{  % ACTUAL NAME: gbexamples (renamed to avoid conflicts)
    colback=green!5!white,         % #F1F8E9 - pale green
    colframe=green!60!black,       % #8BC34A - leaf green
    coltitle=white,
    fonttitle=\bfseries,
    title={Examples Needed},
    boxrule=1pt,
    arc=2pt,
    outer arc=2pt
}

% needs-technical-review - Pale rose with dashed border
\newtcolorbox{gbtechreview}{  % ACTUAL NAME: gbtechreview (renamed to avoid conflicts)
    colback=red!5!white,           % #FFE8E8 - pale rose
    colframe=red!40!white,         % #EF9A9A - rose
    coltitle=white,
    fonttitle=\bfseries,
    title={Technical Review Needed},
    boxrule=1.5pt,
    arc=2pt,
    outer arc=2pt,
    borderline={1.5pt}{0pt}{red!40!white, dashed}
}

% needs-code-review - Pale orange with dotted border
\newtcolorbox{gbcodereview}{  % ACTUAL NAME: gbcodereview (renamed to avoid conflicts)
    colback=orange!5!white,        % #FFF3E0 - pale orange
    colframe=orange!60!yellow,     % #FFB74D - orange
    coltitle=white,
    fonttitle=\bfseries,
    title={Code Review Needed},
    boxrule=1.5pt,
    arc=2pt,
    outer arc=2pt,
    borderline={1.5pt}{0pt}{orange!60!yellow, dotted}
}

% tip - Mint green with solid rounded border
\newtcolorbox{gbtip}{  % ACTUAL NAME: gbtip (renamed to avoid conflicts)
    colback=green!5!white,         % #E8F5E9 - mint
    colframe=green!50!black,       % #66BB6A - green
    coltitle=white,
    fonttitle=\bfseries,
    title={Tip},
    boxrule=1.5pt,
    arc=4pt,                       % More rounded
    outer arc=4pt
}
```

---

## 5. Lua Filter Mappings

The Lua filter must convert markdown divs to these LaTeX environments:

```lua
-- Mapping table (ACTUAL IMPLEMENTATION)
local divMappings = {
    ["needs-diagram"] = "gbdiagram",         -- Renamed to avoid conflicts
    ["preliminary-content"] = "gbpreliminary", -- Renamed to avoid conflicts
    ["needs-verification"] = "gbverify",       -- Renamed to avoid conflicts
    ["needs-examples"] = "gbexamples",        -- Renamed to avoid conflicts
    ["needs-technical-review"] = "gbtechreview", -- Renamed to avoid conflicts
    ["needs-code-review"] = "gbcodereview",    -- Renamed to avoid conflicts
    ["tip"] = "gbtip"                        -- Renamed to avoid conflicts
}

function Div(el)
    local divClass = el.classes[1]
    local envName = divMappings[divClass]
    
    if envName then
        return {
            pandoc.RawBlock('latex', '\\begin{' .. envName .. '}'),
            el,
            pandoc.RawBlock('latex', '\\end{' .. envName .. '}')
        }
    end
    return el
end
```

---

## 6. Color Palette Summary

### Hex Values for Reference
| Element | Background | Border/Title | Hex Background | Hex Border |
|---------|------------|--------------|----------------|------------|
| needs-diagram | Cream | Amber | #FFF8E1 | #FFB300 |
| preliminary-content | Light Gray | Dark Gray | #F5F5F5 | #757575 |
| needs-verification | Pale Blue | Sky Blue | #E3F7FF | #4FC3F7 |
| needs-examples | Pale Green | Leaf Green | #F1F8E9 | #8BC34A |
| needs-technical-review | Pale Rose | Rose | #FFE8E8 | #EF9A9A |
| needs-code-review | Pale Orange | Orange | #FFF3E0 | #FFB74D |
| tip | Mint | Green | #E8F5E9 | #66BB6A |

### LaTeX Color Approximations
- All backgrounds: 5% tint (color!5!white)
- Title bars: 40-70% saturation depending on color
- White text on all title bars for contrast

---

## 7. Implementation Checklist for Sonnet

### Phase 1: Lua Filter
- [ ] Create `green-book-semantic-blocks.lua`
- [ ] Implement all 7 div type conversions
- [ ] Test with sample markdown containing all types
- [ ] Verify proper nesting and escaping

### Phase 2: LaTeX Styles
- [ ] Add all environments to `p2kb-smart-pins-content.sty`
- [ ] Test each environment compiles without errors
- [ ] Verify colors match specifications
- [ ] Check border styles render correctly (dashed, dotted, solid)

### Phase 3: Integration
- [ ] Update request.json to include new Lua filter
- [ ] Verify filter order: colored-blocks → semantic-blocks → pagebreaks
- [ ] Test complete pipeline with v2 document
- [ ] Check PDF output for visual consistency

### Phase 4: Validation
- [ ] All 36 semantic markers render correctly
- [ ] Colors are distinct but not harsh
- [ ] Border styles provide accessibility differentiation
- [ ] Title bars display properly with white text
- [ ] No LaTeX compilation errors

---

## 8. Testing Snippets

### Markdown Test File
```markdown
::: needs-diagram
Timing diagram showing clock relationships
:::

::: preliminary-content
This feature is under development
:::

::: tip
Use Smart Pins for hardware timing
:::
```

### Expected LaTeX Output
```latex
\begin{gbdiagram}
Timing diagram showing clock relationships
\end{gbdiagram}

\begin{gbpreliminary}
This feature is under development
\end{gbpreliminary}

\begin{gbtip}
Use Smart Pins for hardware timing
\end{gbtip}
```

---

## Notes for Sonnet

1. **Order matters**: Lua filters must run in correct sequence
2. **Escaping**: The LaTeX escape script runs BEFORE Lua filters
3. **Compatibility**: These styles must coexist with existing code block styles
4. **Page breaks**: Avoid breaking semantic boxes across pages if possible
5. **Accessibility**: Border styles (dashed/dotted/solid) are intentional for visual impairment

This document provides everything needed to implement the Green Book visual design. Follow the checklist systematically and test each component before integration.