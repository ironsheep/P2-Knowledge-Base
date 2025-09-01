# Smart Pins PDF Generation Architecture

## Document Processing Pipeline & Component Responsibilities

*Last Updated: 2025-08-29*  
*Document: P2 Smart Pins Complete Reference v1.0*

---

## 🎯 Executive Summary

The Smart Pins PDF generation uses a **layered template architecture** with **Lua preprocessing** to create a sophisticated technical manual. Multiple components work in concert, each with specific responsibilities. This document explains what each file does and how they interact.

## 📊 Processing Flow

```
1. Markdown Source (P2-Smart-Pins-Complete-Reference.md)
   ↓
2. LaTeX Escaping (latex-escape-all.sh → latex_escape_processor.py)
   ↓
3. Pandoc Processing with Lua Filters
   - smart-pins-pagebreaks.lua (page break control)
   - smart-pins-block-coloring.lua (code block styling)
   ↓
4. LaTeX Template Application (p2kb-smart-pins.latex)
   - Loads style packages in order
   - Applies overrides
   ↓
5. PDF Generation
```

---

## 🏗️ Component Architecture

### Layer 1: Foundation (`p2kb-foundation.sty`)
**Purpose**: Core LaTeX setup shared by all P2KB documents  
**Responsibilities**:
- Pandoc compatibility commands
- Basic packages (fonts, geometry, hyperref)
- Image scaling defaults
- Table formatting
- Basic code block environment (`Shaded`)
- TOC formatting
- ❌ ~~Page break logic~~ (disabled by template override)

**Key Features**:
- Sets `tocdepth=2` (overridden to 3 in main template)
- Defines `\tightlist` for Pandoc
- Configures 1-inch margins
- Sets up `fancyhdr` basics

---

### Layer 2: Content Styling (`p2kb-smart-pins-content.sty`)
**Purpose**: Smart Pins-specific visual styling  
**Responsibilities**:
- 4-color code block system (Configuration/Spin2/PASM2/Antipattern)
- Color definitions (recently muted for less dominance)
- Special environments (tryityourself, pinconfig, techspec)
- Code syntax highlighting for Spin2/PASM2
- Multi-level code block indentation

**Color Palette** (muted pastels):
```latex
Configuration (blue):    #F5F9FC background, #7FA8C9 border
Spin2 (green):          #F8FCF8 background, #85B985 border  
PASM2 (yellow/cream):   #FFFEF5 background, #D4B896 border
Antipattern (red/pink): #FFF5F5 background, #C08080 border
```

---

### Layer 3: Numbering System (`p2kb-smart-pins-numbering.sty`)
**Purpose**: Hybrid numbering for different document parts  
**Responsibilities**:
- Part numbering (Arabic instead of Roman)
- Conditional section numbering
- Parts I, III, IV: Numbered sections (1.1, 1.2)
- Part II (Mode Reference): Unnumbered sections
- Tracks current part for numbering decisions

**Note**: Some functionality overlaps with Lua filters - could be consolidated.

---

### Layer 4: Branding (`p2kb-tech-review.sty`)
**Purpose**: Headers, footers, and review branding  
**Responsibilities**:
- Page headers with chapter names (`\leftmark`)
- "Iron Sheep Productions" attribution
- "TECHNICAL REVIEW DRAFT" footer
- Red warning color definitions

**Headers/Footers**:
- Left header: Chapter name (via `\leftmark`)
- Right header: "Iron Sheep Productions"
- Left footer: "TECHNICAL REVIEW DRAFT" (red)
- Center footer: Page number

---

### Main Template (`p2kb-smart-pins.latex`)
**Purpose**: Document assembly and override control  
**Responsibilities**:
- Loads all style packages in correct order
- **OVERRIDES** foundation's page break behavior
- Sets TOC depth to 3 (overrides foundation's 2)
- Clears header marks after TOC
- Defines title and copyright pages

**Critical Overrides**:
```latex
% Neutralizes automatic page breaks
\renewcommand{\chapter}[1]{%
  % NO \clearpage - Lua handles it
  \originalchapter{#1}%
  \markboth{#1}{}%  % Sets header
}
```

---

## 🔧 Lua Filter Architecture

### Page Break Controller (`smart-pins-pagebreaks.lua`)
**Purpose**: Single source of truth for ALL page breaks  
**Responsibilities**:
- Parts: Always new page
- First chapter after part: Same page
- Other chapters: New page
- Executive Summary: New page
- Quick Start: New page
- Each Mode section: New page
- Appendices: New page
- Index: New page

**Why Lua Instead of LaTeX**:
- Sees document structure before LaTeX
- Can identify sections by heading text
- Easier to debug with comment injection
- No conflicting macro interactions

### Code Block Styler (`smart-pins-block-coloring.lua`)
**Purpose**: Apply color coding to code blocks based on language  
**Responsibilities**:
- Maps languages to color environments
- `{.configuration}` → blue box
- `spin2` → green box
- `pasm2` → yellow box
- `{.antipattern}` → red box

---

## 🎮 Request Configuration (`request.json`)

**Controls**:
- Input/output filenames
- Template selection
- Document variables (title, version, etc.)
- Lua filter pipeline order
- Pandoc arguments

**Critical Settings**:
```json
"pandoc_args": [
  "--top-level-division=part",  // Makes # = Part, ## = Chapter
  "--wrap=preserve",            // Maintains line wrapping
  "--lua-filter=filters/smart-pins-pagebreaks.lua",
  "--lua-filter=filters/smart-pins-block-coloring.lua"
]
```

---

## 🚨 Common Pitfalls & Solutions

### Problem: Page breaks not working as expected
**Cause**: Conflicting page break logic between LaTeX and Lua  
**Solution**: We disabled LaTeX page breaks; Lua filter is sole authority

### Problem: Headers showing "Contents" on all pages
**Cause**: TOC sets `\leftmark` and nothing clears it  
**Solution**: Added `\markboth{}{}` after TOC in main template

### Problem: Colors too dominant/bright
**Cause**: Original pastels too saturated  
**Solution**: Muted all colors in `p2kb-smart-pins-content.sty`

### Problem: TOC missing subsections
**Cause**: Default `tocdepth=2`  
**Solution**: Override to `tocdepth=3` in main template

---

## 🔄 Modification Guide

### To Change Page Break Behavior:
Edit `smart-pins-pagebreaks.lua` - it's the single source of truth

### To Adjust Colors:
Edit color definitions in `p2kb-smart-pins-content.sty`

### To Change Headers/Footers:
Edit `p2kb-tech-review.sty`

### To Add New Code Block Types:
1. Add color definition in `p2kb-smart-pins-content.sty`
2. Add mapping in `smart-pins-block-coloring.lua`

### To Change TOC Depth:
Edit `\setcounter{tocdepth}` in `p2kb-smart-pins.latex`

---

## 📁 File Locations

**Templates**: `/pdf-forge-workspace/templates/`
- Main: `p2kb-smart-pins.latex`
- Styles: `p2kb-*.sty`

**Lua Filters**: `/pdf-forge-workspace/filters/`
- `smart-pins-pagebreaks.lua`
- `smart-pins-block-coloring.lua`

**Output**: `/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/`
- All files needed for PDF Forge deployment

---

## 🎯 Design Philosophy

1. **Layered Architecture**: Each layer has specific responsibilities
2. **Lua for Structure**: Document structure decisions in Lua
3. **LaTeX for Style**: Visual styling in LaTeX packages
4. **Override Locally**: Main template overrides general behaviors
5. **Single Source of Truth**: One system owns each decision (e.g., Lua owns page breaks)

---

## 📝 Maintenance Notes

- **Testing**: Changes to Lua filters show as comments in .tex output
- **Color Accessibility**: Current palette designed for print, not screen
- **Performance**: Lua filters add ~2-3 seconds to processing time
- **Compatibility**: Requires pandoc 2.14+ for full Lua filter support

---

*This architecture supports sophisticated document requirements while maintaining maintainability. The layered approach allows changes at appropriate levels without affecting other components.*