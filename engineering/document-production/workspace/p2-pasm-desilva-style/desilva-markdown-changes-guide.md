# DeSilva Manual Markdown Changes Guide

**Purpose**: Document all changes needed to transform DeSilva Manual master documents into production-ready document that works with our LaTeX template system

**Document**: P2-PASM-DeSilva-Manual-Combined.md
**Last Updated**: 2025-09-16

## 🔴 CRITICAL: DIV-ONLY APPROACH

**DECISION**: All code blocks MUST use div syntax (`::: type`) for consistency and future maintainability.
- NO language tags (````spin2`, ````pasm2`)
- NO mixed approaches
- ALL code blocks wrapped in semantic divs
- Lua filters will ONLY process div syntax

## Overview
This guide documents the REQUIRED markdown transformations to convert the DeSilva Manual master documents to our standardized div-based syntax. All code blocks must be converted to div environments for proper LaTeX processing.

## Current State Analysis

### Source Document Assessment
**Master Documents**: 
- COMPLETE-OPUS-MASTER.md (Chapters 1-6 + appendices)
- CHAPTERS-7-16-ENHANCED.md (Chapters 7-16)
- COMBINED-COMPLETE-MASTER.md (Combined production master)

**Working File**: P2-PASM-DeSilva-Manual-working.md (to be created)

### Code Block Inventory
**Validated 183 code examples** across both master documents:
- COMPLETE-OPUS-MASTER.md: 77 examples (100% pass rate)
- CHAPTERS-7-16-ENHANCED.md: 106 examples (100% pass rate)
- Current format: `pasm2` and `spin2` language-tagged blocks → MUST convert to `::: pasm2` and `::: spin2`
- Mixed antipattern blocks: Several instances → MUST split and wrap
- Complete programs vs code fragments: Both types present

### DeSilva-Specific Elements Status
**Pedagogical Elements** requiring div conversion:
- Medicine Cabinet sections → `::: medicine`
- Your Turn exercises → `::: yourturn`
- Sidetrack boxes → `::: sidetrack`
- Chapter ending celebrations → `::: chapterend`
- Common Gotchas → `::: gotchas`
- Interlude sections → `::: interlude`

## Known Issues and Solutions

### LaTeX Image Float Problem ✅ **IMPLEMENT SAME AS SMART PINS**
**Issue**: LaTeX moves images to "optimize" page layout, causing them to appear at page tops instead of where referenced in narrative.

**Solution**: Use `non-floating-images.lua` filter (same as Smart Pins manual)

**Design Decision - 85% Width**:
- Images default to 85% of text width for visual breathing room
- Maintains consistency with Smart Pins manual styling
- Creates professional appearance with clear text/image hierarchy

**Implementation**: Add to pandoc args:
```json
"lua_filters": [
  "desilva-div-blocks",
  "non-floating-images",
  "desilva-semantic-blocks"
]
```

## Required Transformations

### 1. Automated Code Block Conversion 🚀 **USE EXISTING SCRIPT**

**Automated Tool**: `/engineering/tools/convert-to-div-syntax.py`
```bash
python3 /engineering/tools/convert-to-div-syntax.py COMBINED-COMPLETE-MASTER.md P2-PASM-DeSilva-Manual-working.md
```

**What the script handles**:
- ✅ Converts all `pasm2` and `spin2` blocks to div syntax
- ✅ Automatically adds blank lines where needed (prevents colons showing in PDF)
- ✅ Splits antipattern blocks (WRONG/RIGHT patterns)
- ✅ Provides statistics on conversions and blank lines added

**Post-script cleanup required**:

1. **DeSilva-specific patterns**: Look for teaching moments with comments:
   - `' This won't work` followed by problematic code
   - `' Better approach` followed by improved code
   - `' The old way` followed by traditional code
   - `' The P2 way` followed by modern code
   - `' Method 1:` and `' Method 2:` comparisons

2. **Ensure blank lines before opening div blocks**: All opening div blocks (`::: type`) MUST have a blank line before them.

### 2. DeSilva Pedagogical Element Conversion 🎓 **MANUAL CONVERSION REQUIRED**

**Purpose**: Convert DeSilva's special sections to semantic divs for proper styling

**Medicine Cabinet Sections**:
```markdown
<!-- BEFORE -->
## The Medicine Cabinet

Feeling overwhelmed? Here's your prescription:

**Minimum viable blinker** - Just 3 instructions:
```pasm2
loop    drvnot  #56         ' Toggle pin 56
        waitx   ##25_000_000 ' Wait
        jmp     #loop       ' Repeat
```

<!-- AFTER -->
::: medicine
Feeling overwhelmed? Here's your prescription:

**Minimum viable blinker** - Just 3 instructions:

::: pasm2
```
loop    drvnot  #56         ' Toggle pin 56
        waitx   ##25_000_000 ' Wait
        jmp     #loop       ' Repeat
```
:::
:::
```

**Your Turn Exercises**:
```markdown
<!-- BEFORE -->
### Experiment 1: Different Patterns
Make the LED blink in a pattern: short-short-long (like SOS):

```pasm2
        org     0
        
        mov     short, ##10_000_000    ' 0.1 second
        mov     long_d, ##30_000_000   ' 0.3 seconds
        
pattern drvh    #56                    ' Short pulse 1
        waitx   short
        drvl    #56
        waitx   short
        jmp     #pattern
```

<!-- AFTER -->
::: yourturn
**Experiment 1: Different Patterns**

Make the LED blink in a pattern: short-short-long (like SOS):

::: pasm2
```
        org     0
        
        mov     short, ##10_000_000    ' 0.1 second
        mov     long_d, ##30_000_000   ' 0.3 seconds
        
pattern drvh    #56                    ' Short pulse 1
        waitx   short
        drvl    #56
        waitx   short
        jmp     #pattern
```
:::

Goal: Create SOS pattern with timing
Hint: Short = 0.1s, Long = 0.3s
Success Check: Clear SOS pattern visible
:::
```

**Sidetrack Boxes**:
```markdown
<!-- BEFORE -->
### Sidetrack: Why Start at Address 0?

You might wonder why COG code always starts at address 0...

<!-- AFTER -->
::: sidetrack
**Why Start at Address 0?**

You might wonder why COG code always starts at address 0...
:::
```

**Chapter Endings**:
```markdown
<!-- BEFORE -->
## What We've Learned

Let's celebrate what you've accomplished:
- ✅ Written your first PASM2 program
- ✅ Controlled hardware (LED) directly
- ✅ Used immediate values (# and ##)

---

**Have Fun!** And remember, every expert was once a beginner...

<!-- AFTER -->
::: chapterend
**What We've Learned**

Let's celebrate what you've accomplished:
- ✅ Written your first PASM2 program
- ✅ Controlled hardware (LED) directly
- ✅ Used immediate values (# and ##)

**Have Fun!** And remember, every expert was once a beginner...
:::
```

### 3. CORDIC Code Block Special Handling 🔄 **PASM2 WITH CORDIC FLAG**

**Purpose**: CORDIC examples need special highlighting as unique P2 feature

**Standard PASM2 blocks** → `::: pasm2`
**CORDIC-specific blocks** → `::: cordic` (for special highlighting)

```markdown
<!-- CORDIC examples get special treatment -->
::: cordic
```
' Calculate sine and cosine simultaneously
        qrotate angle, ##$7FFF_FFFF  ' Max radius for unit circle
        getqx   cosine              ' cos(angle) in 2.30 fixed point
        getqy   sine                ' sin(angle) in 2.30 fixed point
```
:::
```

**Detection Pattern**: Look for these CORDIC instructions:
- `qrotate`, `qvector`, `qdiv`, `qfrac`, `qmul`, `qsqrt`, `qlog`, `qexp`
- `getqx`, `getqy` (CORDIC result retrieval)

### 4. Multi-COG Example Blocks 🔄 **MULTI-COG SYNTAX**

**Purpose**: Multi-COG examples need special formatting to show parallel execution

```markdown
<!-- BEFORE -->
```spin2
PUB main() | i
    repeat i from 0 to 3
        coginit(COGEXEC_NEW, @cog_code, 56 + i)
    repeat

DAT
        org     0
cog_code
        rdlong  pin_num, ptra
        
loop    drvnot  pin_num
        waitx   ##10_000_000
        jmp     #loop
```

<!-- AFTER -->
::: multicog
```
PUB main() | i
    repeat i from 0 to 3
        coginit(COGEXEC_NEW, @cog_code, 56 + i)
    repeat

DAT
        org     0
cog_code
        rdlong  pin_num, ptra
        
loop    drvnot  pin_num
        waitx   ##10_000_000
        jmp     #loop
```
:::
```

## 4-Color Code Block System (DeSilva Pedagogical Decision)

### Color Mappings (AFTER div conversion)

**🟢 GREEN - Spin2 Blocks** (high-level coordination)
- Markdown: `::: spin2`
- LaTeX Environment: `Spin2Block`
- Purpose: High-level program structure, COG launching

**🟡 YELLOW - PASM2 Blocks** (core assembly)
- Markdown: `::: pasm2`
- LaTeX Environment: `PASM2Block`
- Purpose: Core assembly language examples

**🔵 BLUE - CORDIC Blocks** (unique P2 feature)
- Markdown: `::: cordic`
- LaTeX Environment: `CORDICBlock`
- Purpose: Highlight P2's unique mathematical capabilities

**🟣 PURPLE - Multi-COG Blocks** (parallel processing)
- Markdown: `::: multicog`
- LaTeX Environment: `MultiCOGBlock`
- Purpose: Demonstrate parallel processing concepts

**🔴 RED - Antipattern Blocks** (what not to do)
- Markdown: `::: antipattern`
- LaTeX Environment: `AntipatternBlock`
- Purpose: Show incorrect approaches for teaching

### Pedagogical Rationale - DeSilva Learning Progression

**4-Color System Benefits**:
- **Spin2 (Green)**: Safe, familiar high-level starting point
- **PASM2 (Yellow)**: Core skill development
- **CORDIC (Blue)**: P2's unique mathematical power
- **Multi-COG (Purple)**: Advanced parallel processing
- **Antipattern (Red)**: Clear "don't do this" warnings

**Learning Progression**:
1. Start with Spin2 (green) for basic concepts
2. Transition to PASM2 (yellow) for real programming
3. Explore CORDIC (blue) for P2 advantages
4. Master Multi-COG (purple) for true parallel processing
5. Avoid antipatterns (red) throughout

## Semantic Environment Mappings

### DeSilva-Specific Environments

**🟡 medicine** (Medicine Cabinet sections)
- Markdown: `::: medicine`
- Purpose: Simplified alternatives when overwhelmed
- LaTeX Environment: `MedicineCabinet`

**🔵 yourturn** (Your Turn exercises)
- Markdown: `::: yourturn`
- Purpose: Hands-on experiments and practice
- LaTeX Environment: `YourTurn`

**⚪ sidetrack** (Sidetrack boxes)
- Markdown: `::: sidetrack`
- Purpose: Deep dives without breaking main flow
- LaTeX Environment: `Sidetrack`

**🟢 chapterend** (Chapter celebrations)
- Markdown: `::: chapterend`
- Purpose: Celebrate learning achievements
- LaTeX Environment: `ChapterEnd`

**🟠 gotchas** (Common Gotchas)
- Markdown: `::: gotchas`
- Purpose: Prevent common mistakes
- LaTeX Environment: `CommonGotchas`

**🟣 interlude** (Interlude sections)
- Markdown: `::: interlude`
- Purpose: Historical context and perspective
- LaTeX Environment: `Interlude`

## CRITICAL FILE NAMING RULES

### NO SUFFIXES - EVER
**NEVER create files with suffixes like:**
- ❌ `desilva-div-blocks-v2.lua`
- ❌ `p2kb-desilva-content-fixed.sty`
- ❌ `P2-PASM-DeSilva-Manual-FINAL.md`

**ALWAYS use production names:**
- ✅ `desilva-div-blocks.lua`
- ✅ `p2kb-desilva-content.sty`
- ✅ `P2-PASM-DeSilva-Manual.md`

**WHY**: Suffixes break references, create confusion, and violate our production workflow.

## Processing Philosophy

**Goal**: Preserve DeSilva's pedagogical voice + rich visual presentation = engaging manual

**DeSilva Voice Preservation**:
- Conversational tone maintained in all environments
- "Have Fun!" celebration moments preserved
- Progressive difficulty maintained through color coding
- Medicine Cabinet philosophy preserved

**Preference Order**:
1. **Lua Filter Solution** - Can we detect and handle automatically?
2. **Stylesheet Solution** - Can we handle with better LaTeX rules?
3. **Markdown Change** - Only if processing pipeline cannot handle

## File Locations

- **Combined Master**: `/engineering/document-production/manuals/p2-pasm-desilva-style/opus-master/COMBINED-COMPLETE-MASTER.md`
- **Working Copy**: `/engineering/document-production/workspace/p2-pasm-desilva-style/P2-PASM-DeSilva-Manual-working.md`
- **Escaped Copy**: `/engineering/document-production/workspace/p2-pasm-desilva-style/P2-PASM-DeSilva-Manual-escaped.md`
- **Deployment**: `/engineering/pdf-forge/production/p2-pasm-desilva-manual/`

## Template Requirements

The following templates must work with DeSilva Manual:
- `p2kb-foundation.sty` - Base layer (shared with Smart Pins)
- `p2kb-desilva-content.sty` - Content styles with 5-color blocks + semantic environments
- `p2kb-tech-review.sty` - Presentation layer (shared)
- `desilva-div-blocks.lua` - 5-color code block processing
- `desilva-semantic-blocks.lua` - DeSilva semantic div processing
- `non-floating-images.lua` - Image placement (shared with Smart Pins)

## Systematic Transformation Guide: Combined Master → LaTeX-Ready

### 📋 EXECUTIVE SUMMARY: DESILVA-SPECIFIC TRANSFORMATIONS

**The DeSilva Manual needs code block conversion + pedagogical element wrapping for optimal LaTeX processing.**

### Deployment Workflow

**Step 1: Create Working Copy** 🔄
```bash
# Start with combined master
cp ../manuals/p2-pasm-desilva-style/opus-master/COMBINED-COMPLETE-MASTER.md \
   P2-PASM-DeSilva-Manual-working.md
```

**Step 2: Apply Code Block Conversion** 🚀
```bash
# Use existing script for code blocks
python3 ../../tools/convert-to-div-syntax.py \
  P2-PASM-DeSilva-Manual-working.md \
  P2-PASM-DeSilva-Manual-div-converted.md
```

**Step 3: Manual Pedagogical Element Conversion** 🎓
- Convert Medicine Cabinet sections → `::: medicine`
- Convert Your Turn exercises → `::: yourturn`
- Convert Sidetrack boxes → `::: sidetrack`
- Convert Chapter endings → `::: chapterend`
- Convert Common Gotchas → `::: gotchas`
- Convert Interlude sections → `::: interlude`
- Identify CORDIC blocks → `::: cordic`
- Identify Multi-COG blocks → `::: multicog`

**Step 4: Verification** ✅
```bash
# Should return 0 - no language tags remain
grep -c '^```[sp]' P2-PASM-DeSilva-Manual-working.md

# Should show div blocks
grep -c '^:::' P2-PASM-DeSilva-Manual-working.md

# Should show DeSilva elements
grep -c '::: medicine\|::: yourturn\|::: sidetrack' P2-PASM-DeSilva-Manual-working.md
```

**Step 5: LaTeX Escaping**
```bash
../../tools/latex-escape-all.sh \
  P2-PASM-DeSilva-Manual-working.md \
  P2-PASM-DeSilva-Manual-escaped.md
```

**Step 6: Deploy with DeSilva Filters**
- Template: `p2kb-desilva.latex`
- Lua Filters:
  - `desilva-div-blocks.lua` - 5-color code block processing
  - `desilva-semantic-blocks.lua` - DeSilva pedagogical elements
  - `non-floating-images.lua` - Image placement control

### Quality Assurance Checklist

**Code Block Verification** ✅
- [ ] All `spin2` blocks → green rendering
- [ ] All `pasm2` blocks → yellow rendering  
- [ ] CORDIC blocks → blue rendering
- [ ] Multi-COG blocks → purple rendering
- [ ] Antipattern blocks → red rendering
- [ ] All opening div blocks have blank lines before them
- [ ] NO language-tagged blocks remain

**DeSilva Element Verification** ✅
- [ ] Medicine Cabinet sections → proper styling
- [ ] Your Turn exercises → proper styling with clear goals/hints
- [ ] Sidetrack boxes → proper styling with letters (A, B, C...)
- [ ] Chapter endings → celebration styling
- [ ] Common Gotchas → warning styling
- [ ] Interlude sections → historical context styling

**LaTeX Template Compatibility** ✅
- [ ] Headers follow proper hierarchy for pagebreaks
- [ ] Images use standard markdown syntax (85% width)
- [ ] No manual LaTeX commands in content
- [ ] Proper pandoc div syntax throughout
- [ ] DeSilva voice preserved in all environments

### Post-Processing Verification

**After PDF Generation:**
1. **Visual Check**: All 183 code blocks properly colored with 5-color system
2. **Pedagogical Check**: All DeSilva elements (Medicine, Your Turn, etc.) properly styled
3. **Layout Check**: Headers, pagebreaks, and flow maintain DeSilva progression
4. **Voice Check**: Conversational tone preserved in all environments

### Success Metrics

🎯 **Target**: Complete conversion to div-wrapped format with DeSilva pedagogical elements

**Success Criteria**:
- ✅ 0 language-tagged blocks remaining
- ✅ 100% div-wrapped code blocks with 5-color system
- ✅ All DeSilva pedagogical elements properly wrapped
- ✅ Lua filters handle ONLY div syntax
- ✅ DeSilva voice and progression preserved
- ✅ Consistent styling with Smart Pins manual base

### Summary of Required Changes

1. **Convert 183 code blocks** from language-tagged to div-wrapped with 5-color system
2. **Wrap DeSilva pedagogical elements** in semantic divs
3. **Preserve DeSilva voice** throughout all transformations
4. **Create specialized Lua filters** for DeSilva-specific environments
5. **Maintain compatibility** with Smart Pins base template system

### Why This Matters for DeSilva Manual

- **Pedagogical Integrity**: DeSilva's teaching approach preserved through proper styling
- **Visual Consistency**: 5-color system supports learning progression
- **Production Quality**: Professional output worthy of DeSilva's legacy
- **Template Sharing**: Base components shared with Smart Pins for efficiency
- **Future-proof**: Semantic divs enable easy style updates