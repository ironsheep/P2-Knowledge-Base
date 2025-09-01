# Formatting Specifications for "Discovering P2 Assembly"

**Title**: Discovering P2 Assembly  
**Subtitle**: *Build, Experiment, and Master the Propeller 2*  
**Footer**: P2 Assembly in the Spirit of deSilva's Legendary P1 Tutorial  
**Created**: 2025-08-20  
**Purpose**: Define precise visual formatting for PDF generation  
**Status**: Specifications defined, LaTeX implementation pending

## 📐 Visual Design System

### Typography Analysis & Recommendations

#### Current Issues
- deSilva original: Typewriter font (too retro, hard to read long-form)
- Current draft: Modern fonts but headings are distracting
- Cognitive interference from font contrast

#### Recommended Font Stack

**For Optimal Readability & Low Cognitive Load:**

1. **Body Text**: 
   - **Primary**: Charter (excellent readability, gentle serif)
   - **Alternative**: Palatino (warmer, still professional)
   - **Fallback**: Georgia (web-safe, good screen reading)
   - **Size**: 11pt (optimal for technical content)
   - **Line spacing**: 1.3 (reduces eye strain)

2. **Headings**:
   - **Font**: Same as body (Charter/Palatino) - reduces cognitive switching
   - **Weight**: Bold for chapters, semibold for sections
   - **Size**: Moderate scaling (16pt, 14pt, 12pt, 11pt)
   - **Key**: Avoid sans-serif headings with serif body (causes friction)

3. **Code**:
   - **Font**: Consolas or Source Code Pro (modern, readable)
   - **Alternative**: JetBrains Mono (excellent ligatures)
   - **Size**: 95% of body text (slight reduction maintains hierarchy)
   - **Avoid**: Courier (too typewriter-like)

#### Why This Works
- **Unified font family** reduces cognitive switching
- **Gentle serifs** guide eye flow without distraction
- **Moderate contrast** maintains hierarchy without jarring transitions
- **Consistent spacing** creates predictable rhythm

#### LaTeX Implementation
```latex
% Install if needed:
% apt-get install texlive-fonts-extra
% or use XeLaTeX for system fonts

\usepackage{charter}  % or
\usepackage{palatino} % or
\usepackage{XCharter} % enhanced Charter for XeLaTeX

% For code
\usepackage{sourcecodepro}
% or with fontspec (XeLaTeX):
\setmonofont{Consolas}[Scale=0.95]
```

### Color Palette
- **Code blocks**: Light gray background (#F5F5F5)
- **Inline code**: Light yellow background (#FFFACD) - full line width
- **Sidetracks**: Light gray background (#F5F5F5) with dotted border
- **TBD sections**: Light violet background (#E6E6FA)
- **Links**: Blue (#0000FF) with underline
- **Body text**: Black on white
- **Diagrams**: White background, no borders

## 📝 Paragraph Styles

### 1. Code Blocks
```latex
% Requirements:
- Background: Light gray (#F5F5F5)
- Font: Monospace (Courier or similar)
- Padding: 10pt all sides
- Border: None (solid gray background)
```

### 2. Inline Code
```latex
% Requirements:
- Font: Slightly bolder monospace
- Background: Light yellow (#FFFACD)
- Background width: FULL LINE WIDTH (not just text width)
- Padding: 2pt vertical, extends to margins horizontally
```
**Pedagogical Benefit**: Full-width highlighting creates stronger visual breaks, reducing cognitive load when scanning for code examples.

### 3. Sidetrack Sections
```latex
% Requirements:
- Background: Light gray (#F5F5F5)
- Border: Dotted outline (1pt, dark gray)
- Heading: Bold, part of the gray box
- Padding: 10pt all sides
- Format: "Sidetrack: [Topic Name]" in bold
```
**Pedagogical Benefit**: Dotted borders signal "optional depth" - readers can skip without losing main thread.

### 3a. Interlude Sections
```latex
% Requirements:
- Background: Light gray (#F5F5F5)
- Border: NONE (just background, no outline)
- Heading: Bold, part of the gray box
- Padding: 10pt all sides
- Format: "Interlude [Number]: [Topic]" in bold
```
**Pedagogical Benefit**: Gray background without border creates a "pause" feeling - a mental break between intense sections.
**Difference from Sidetrack**: No border = integrated flow, not optional

### 4. TBD/Missing Information - CRITICAL VISIBILITY

**GOAL**: These colored sections must be IMPOSSIBLE to miss. As content is completed, all colored backgrounds disappear.

```latex
% HIGHLY VISIBLE missing content box
\newtcolorbox{missingcontent}{
  colback=violet!20,          % Bright violet background  
  colframe=violet!70,          % Dark violet border
  boxrule=2pt,                 % Thick border
  title={🚧 CONTENT MISSING - COMING SOON},
  fonttitle=\bfseries\large
}

% Usage:
\begin{missingcontent}
CORDIC operation examples - all 34 functions needed
\end{missingcontent}
```

#### Three Types of Content Flags:

1. **🚧 MISSING CONTENT** (Violet #E6E6FA)
   - Examples not written yet
   - Explanations coming soon
   - Placeholder sections

2. **🔍 NEEDS REVIEW** (Orange #FFE4B5)
   - Technical accuracy not verified
   - Hardware testing required
   - Expert review pending

3. **🎨 DIAGRAM NEEDED** (Blue #E0F2FF)
   - Visual aid placeholder
   - Timing diagram required
   - Illustration to be created

**Progress Tracking**: Document is READY when ALL colored backgrounds are gone!
**Pedagogical Benefit**: Clear "coming soon" flags prevent reader frustration.

### 5. Links
```latex
% Requirements:
- Color: Blue (#0000FF)
- Style: Underlined
- Format: Full URL displayed (not abbreviated)
- Example: https://github.com/example/repo (blue, underlined)
```

## 📊 Diagram Formatting

### Numbering Convention
```
Diagram 1 shows the COG architecture...
[DIAGRAM HERE]

The egg beater model (Diagram 2) revolutionizes...
[DIAGRAM HERE]
```

### Requirements
- **Numbering**: "Diagram N" above the diagram
- **Reference style**: "Diagram N" (underlined when referenced)
- **Positioning**: Free-floating on white background
- **Borders**: None
- **Captions**: None (reference is above, inline with text)
- **Color**: Supports both color and B&W

### Asset Requirements for Diagrams
When requesting diagram assets:
- Specify: "No borders, white background"
- Format: PNG or PDF vector
- Resolution: 300 DPI minimum for raster
- Color mode: RGB (will convert to grayscale if needed)

## 🎯 Pedagogical Analysis

### Visual Hierarchy Benefits

1. **Reduced Cognitive Load**
   - Color coding creates instant recognition
   - No need to parse formatting to understand content type
   - Visual patterns become automatic with repetition

2. **Scanability Enhancement**
   - Yellow highlights make code examples "pop" for quick reference
   - Gray boxes clearly delineate optional content
   - Violet TBDs prevent frustration from incomplete sections

3. **Learning Path Clarity**
   - Main content (white) forms primary path
   - Sidetracks (gray + dotted) are clearly optional
   - Code (yellow) stands out for hands-on learners

### Recommended Enhancements

While staying true to deSilva's style, consider:

1. **Formal Figure Captions** (Optional Enhancement)
   - **Current**: "Diagram N" inline above
   - **Alternative**: Centered, bold caption below
   - **Benefit**: Better for academic reference
   - **Decision**: Keep deSilva style for consistency, but number consistently

2. **Code Line Numbers** (Future Enhancement)
   - Add line numbers to code blocks >5 lines
   - Helps with error discussions and tutorials
   - Can reference specific lines in explanations

## 🔧 LaTeX Package Requirements

### Required Packages for PDF Forge
```latex
% Color support
\usepackage{xcolor}
\usepackage{colortbl}

% Background colors for paragraphs
\usepackage{mdframed}  % or tcolorbox for more control
\usepackage{soul}      % For inline highlighting

% Code formatting
\usepackage{listings}
\usepackage{fancyvrb}

% Box drawing (for sidetracks and interludes)
\usepackage{tcolorbox}

% Sidetrack with dotted border
\newtcolorbox{sidetrack}{
  colback=gray!10,
  colframe=gray!50,
  boxrule=1pt,
  arc=0pt,
  boxsep=10pt,
  left=10pt,right=10pt,top=10pt,bottom=10pt,
  borderline={1pt}{0pt}{gray, dotted}
}

% Interlude with no border
\newtcolorbox{interlude}{
  colback=gray!10,
  colframe=gray!10,  % Same as background
  boxrule=0pt,       % No border
  arc=0pt,
  boxsep=10pt,
  left=10pt,right=10pt,top=10pt,bottom=10pt
}
```

### Installation Requirements
```bash
# For Debian/Ubuntu (PDF Forge machine):
apt-get install texlive-latex-extra  # mdframed, tcolorbox
apt-get install texlive-xetex        # Better color support

# These are TeX packages, not npm/pip
# They come with texlive distributions
```

## 📋 Implementation Checklist

### For Each Chapter
- [ ] Chapters start on new pages (`\newpage` or `\chapter`)
- [ ] Code blocks use gray background
- [ ] Inline code uses yellow background (full width)
- [ ] Sidetracks have dotted borders
- [ ] TBD sections use violet background
- [ ] Diagrams are numbered consistently
- [ ] Links show full URL in blue

### For Template Creation
- [ ] Define `\inlinecode{}` command for yellow background
- [ ] Define `\sidetrack{}` environment (dotted border)
- [ ] Define `\interlude{}` environment (no border)
- [ ] Define `\todoblock{}` for TBD sections
- [ ] Configure listings package for code blocks
- [ ] Set up diagram numbering counter

## 🎨 Visual Consistency Rules

1. **Never mix background colors** (no yellow inside gray)
2. **Exception**: Inline code in sidetracks keeps yellow background
3. **Maintain padding** consistency (10pt for blocks, 2pt for inline)
4. **Use semantic commands** not direct formatting

## 📚 Style Decision Record

### Decisions Made
1. **Full-width yellow for inline code** - Better visual separation than text-width only
2. **Keep deSilva diagram numbering** - Inline references maintain flow
3. **Dotted borders for sidetracks** - Clear "optional" signal
4. **Violet for TBDs** - Visible but not alarming

### Open Questions
1. Better title for manual - TBD with user
2. Exact gray/yellow/violet RGB values - may need adjustment for print

### Font Decision Record

**Decision**: Use unified font family approach
- Single serif family for both body and headings
- Reduces cognitive load from font switching
- Creates cohesive, professional appearance
- Maintains deSilva's approachability without typewriter aesthetic

**Rejected Options**:
- Mixed serif/sans-serif: Too much cognitive switching
- Pure sans-serif: Harder to read in long-form technical content
- Typewriter fonts: Too retro, reduces readability
- Heavily stylized headings: Distracting from content

## 7. Chapter Transitions

### The Problem
Three horizontal lines (---) create a jarring visual break that feels inconsistent with document flow.

### The Solution: Gentle Celebration

#### Recommended Approach - Subtle Celebration Box:
```latex
% Chapter ending celebration
\newtcolorbox{chapterending}{
  colback=green!5,      % Very subtle green tint (5% opacity)
  colframe=green!5,     % No visible border
  boxrule=0pt,
  width=0.8\textwidth,
  center,
  fontupper=\itshape
}

% Usage:
\begin{chapterending}
  You've got this! Time to celebrate what you've learned.
  
  Ready for the next adventure? → Chapter 2 awaits!
\end{chapterending}
```

#### Alternative Approaches:

1. **Subtle Fade Line**:
   ```latex
   \tikz\draw[gray!30, line width=0.5pt] (0,0) -- (\textwidth,0);
   ```
   - Single thin line, not three
   - Very light gray (30% opacity)
   - Gentle visual pause

2. **Typography Only**:
   ```latex
   \vspace{1em}
   {\centering\itshape\color{gray}
   You've mastered these concepts! \\[0.5em]
   Continue to Chapter 2 →\par}
   \vspace{2em}
   ```
   - No visual elements
   - Italics + gray text
   - Extra spacing for breathing room

3. **Tiny Centered Icon**:
   ```latex
   \begin{center}
   \textcolor{gray!50}{✓}  % or small P2 logo
   \end{center}
   ```
   - Minimal visual element
   - Celebrates completion
   - No harsh lines

### What to Avoid:
- ❌ **Multiple horizontal lines** - Too jarring, breaks flow
- ❌ **Heavy borders/boxes** - Creates visual walls
- ❌ **Sudden style changes** - Causes cognitive friction
- ❌ **Stark black elements** - Too harsh for transitions

### Pedagogical Rationale:
Chapter transitions should feel like:
- A gentle pause for reflection
- A moment of celebration
- A natural breath before continuing
- NOT a hard stop or barrier

The visual treatment should maintain document rhythm while providing closure.

### Implementation Note:
Test with actual readers to ensure the chosen approach:
- Feels natural and unobtrusive
- Provides clear chapter separation
- Maintains emotional engagement
- Doesn't create "speed bumps" in reading flow

---

*This specification ensures visual clarity enhances learning rather than distracting from it.*