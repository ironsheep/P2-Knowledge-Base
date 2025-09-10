# Visual Fixes Tracking - De Silva Manual Part 1

## Pass 1 Issues and Resolutions ✅

### TEMPLATE-ONLY FIXES
1. ✅ **Inline code with yellow background** - Fixed: bold only, no background
2. ✅ **Code blocks gray instead of yellow** - Fixed: yellow background applied
3. ✅ **Duplicate titles in special boxes** - Fixed: removed title parameters
4. ✅ **Separator line floating below chapter-end box** - Fixed: positioned inside
5. ✅ **Page headers showing "contents"** - Fixed: proper chapter structure

### MARKDOWN-ONLY FIXES
1. ✅ **LaTeX artifacts in output** - Fixed: removed `\part{Foundation}`
2. ✅ **Chapter numbering issues** - Fixed: proper chapter syntax

## Pass 2 Issues and Resolutions (COLLECTING)

### IDENTIFIED ISSUES
1. **Title page warning box** - Correctly shows only 3 incompleteness flags ✅
2. **Duplicate Table of Contents** - Manual TOC plus auto-generated TOC ✅
3. **Chapter numbering in TOC** - Shows 0.4, 0.5, 0.6, 0.7 instead of 1, 2, 3, 4 ✅
4. ✅ **Code blocks yellow background** - Working correctly now!
5. **Instruction mnemonics not emphasized** - `org`, `mov`, `drvh` etc should be bold/highlighted
6. **Escaped # and _ in code** - `\#16` should be `#16`, `25\_000\_000` should be `25_000_000`
7. **Your Turn box color too similar to code** - Current color (FFF8DC) too close to code yellow (FFFACD)
8. **GREEN BOX ISSUES (Chapter-end):**
   - Separator line is closer but NOT BETWEEN the two text sections
   - Instructions are bold+italic but should be bold+uppercase+NO italic
   - Should show as `DRVH`/`DRVL` not `drvh`/`drvl`
9. **"Meet the Cogs" section issues:**
   - Wrong specs: "25 MIPS at 50MHz" is P1, not P2 (should be ~100 MIPS at 200MHz)
   - Wrong formatting: Using code block for informational content
   - Should be sidetrack box (gray with dotted border) like "Why 512 Longs?"

### FIXES APPLIED
1. ✅ **Removed manual TOC** - Deleted entire "Table of Contents" section from markdown
2. ✅ **Chapter numbering** - Root cause: content before first chapter was creating sections

## Content Formatting Patterns

### Sidetrack Box Usage (Gray with dotted border)
**Purpose**: Technical asides, specifications, architecture explanations
**Visual**: Gray background with dashed border
**Examples**:
- "Why 512 Longs?" - explaining architecture decisions ✓
- "Cog Resources at a Glance" - should use this format too!
- Any technical detail that supplements but doesn't interrupt flow

### Correct Cog Resources Content:
```
\begin{sidetrack}
\textbf{Cog Resources at a Glance}

• 512 longs (2KB) of private RAM
• ~100 MIPS at 200MHz (1 instruction per 2 clocks)
• Direct access to all 64 I/O pins  
• Private access to CORDIC engine
• Guaranteed hub access every 8 clocks
• Hardware multiply/divide
\end{sidetrack}
```

## Green Chapter-End Box Issues

### Current Problems:
1. **Separator line positioning** - It's inside the box but not properly BETWEEN the two text sections
2. **Instruction formatting** - Currently: bold + italic (wrong!)
   - Should be: **UPPERCASE + BOLD + NO ITALIC**
   - Example: `DRVH`, `DRVL`, `WAITX`, `JMP` (not `drvh`, `drvl`)

### Decision on PASM Instructions:
**AGREED FORMAT**: 
- **UPPERCASE** - Yes, for visual distinction and tradition
- **BOLD** - Yes, for emphasis
- **NO BACKGROUND** - Correct
- **NEVER ITALIC** - Correct, italic is for comments/emphasis, not instructions

This applies to:
- Instructions in prose text
- Instructions in green boxes
- Instructions referenced anywhere outside code blocks

(In actual code blocks, keep them lowercase as people write them)

## Color Analysis

### Current Color Scheme
- **Code blocks**: `FFFACD` (Light Goldenrod Yellow)
- **Your Turn boxes**: `FFF8DC` (Cornsilk - very pale yellow/beige)
- **Problem**: Only ~5% difference in color values, visually indistinguishable

### Suggested Alternative Colors for Your Turn
Options to consider:
1. **Light Blue** (`E6F3FF`) - Clear distinction, suggests "practice/exercise"
2. **Light Green** (`E8F5E8`) - "Go/action" color, distinct from yellow
3. **Light Purple** (`F0E6FF`) - Different hue entirely, stands out
4. **Pale Cyan** (`E0FFFF`) - Cool tone vs warm yellow
5. **Light Pink** (`FFE0E6`) - Energetic, attention-getting

**Recommendation**: Light blue or light green for pedagogical clarity

## Escaping Script Issues

### Problem Analysis
The latex-escape-all.sh script is escaping:
- `#` → `\#` (but `#16` is P2 immediate value syntax!)
- `_` → `\_` (but `25_000_000` is P2 number format!)

These should NOT be escaped when they appear in:
1. Code blocks (```pasm2 ... ```)
2. Inline code backticks (`#16`)

### Examples of Over-Escaping
- `drvh #16` becoming `drvh \#16`
- `waitx ##25_000_000` becoming `waitx \#\#25\_000\_000`
- `#%01_000001` becoming `\#\%01\_000001`

## Pedagogical Decisions

### Instruction Mnemonic Presentation - REVISED
**FINAL DECISION**: 
- **In prose/boxes**: UPPERCASE + BOLD (e.g., `MOV`, `ADD`, `JMP`)
- **In code blocks**: lowercase as written (e.g., `mov`, `add`, `jmp`)
- **Never italic**: Instructions are never italicized
- **No background**: Clean, professional look

## Template Fix Needed for Green Box

The chapterend environment needs adjustment:
1. The separator line must be positioned to actually separate the two text parts
2. The `fontupper=\itshape` is making everything italic - need to fix
3. Need to handle instruction formatting specially

Current template (lines 148-163):
```latex
\newtcolorbox{chapterend}{
  colback=chaptergreen,
  colframe=chaptergreen,
  boxrule=0pt,
  width=0.8\textwidth,
  center,
  fontupper=\itshape,  % THIS IS THE PROBLEM - makes everything italic!
  left=20pt,right=20pt,top=15pt,bottom=15pt,
  before skip=20pt,
  after skip=20pt,
  overlay={\draw[gray!40, line width=0.5pt] 
    ([xshift=30pt]frame.west |- frame.center) -- 
    ([xshift=-30pt]frame.east |- frame.center);}
}
```

## Pass 3 Checklist (COMPLETED)
- [x] Fix escaping script to not escape # and _ in code - DONE (made context-aware)
- [x] Change Your Turn box color to be distinct from code yellow - DONE (E6F3FF light blue)
- [x] Fix green box separator line position - DONE (positioned inside box)
- [x] Fix green box italic issue (remove fontupper=\itshape) - DONE (removed italic)
- [x] Make instructions UPPERCASE + BOLD in prose - DONE (updated WAITX, DRVH, DRVL, JMP)
- [x] Fix "Meet the Cogs" section - wrong specs and wrong format - DONE (sidetrack box, ~100 MIPS)
- [ ] Verify chapter numbering is 1, 2, 3, 4 in TOC - Need user to generate PDF
- [ ] Confirm only one TOC appears - Need user to generate PDF
- [ ] Check page headers show proper chapter names - Need user to generate PDF
- [ ] Verify all previous fixes still work - Need user to generate PDF

## Implementation Summary

### Scripts Modified:
- `/tools/latex_escape_processor.py` - Made context-aware for inline code and code blocks

### Templates Modified:
- `/exports/pdf-generation/workspace/desilva-manual/p2kb-pasm-desilva.latex`
  - Lines 38: yourturncolor changed to E6F3FF
  - Lines 101-109: missing environment title removed
  - Lines 112-120: review environment title removed
  - Lines 123-131: diagram environment title removed
  - Line 152: Removed italic formatting from chapterend

### Content Modified:
- `/exports/pdf-generation/workspace/desilva-manual/P2-PASM-deSilva-Style-FULL-Part1.md`
  - Lines 229-241: Meet the Cogs changed to sidetrack box with correct P2 specs
  - Line 91: WAITX instruction reference uppercased
  - Line 194: All instruction references in chapter end uppercased