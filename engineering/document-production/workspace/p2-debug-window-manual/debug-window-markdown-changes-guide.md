# Debug Window Manual Markdown Changes Guide

**Purpose**: Document all changes needed to transform Debug Window Manual opus-master into production-ready document
**Document**: P2-Debug-Window-Manual.md
**Last Updated**: 2025-09-16

## 🔴 CRITICAL: DIV-ONLY APPROACH (Same as DeSilva)

**DECISION**: All code blocks MUST use div syntax (`::: type`) for consistency and future maintainability.
- NO language tags (````spin2`, ````pasm2`, ````debug`)
- NO mixed approaches
- ALL code blocks wrapped in semantic divs
- Lua filters will ONLY process div syntax

## Overview
This guide documents the REQUIRED markdown transformations to convert the Debug Window Manual opus-master to our standardized div-based syntax. The Debug Window manual has unique requirements for showing DEBUG() statements, terminal output, and various window types.

## Current State Analysis

### Source Document Assessment
**Master Documents in opus-master/**: 
- `COMPLETE-OPUS-MASTER.md` - Full manual with all chapters and appendices
- Individual chapter files (chapter-01 through chapter-14)
- Appendix files (appendix-a through appendix-e)

**Working File**: `P2-Debug-Window-Manual.md` (to be created in workspace)

### Code Block Inventory
**Estimated code examples across manual**:
- DEBUG() statement examples: ~150+ blocks
- Spin2 program structure: ~50+ blocks  
- PASM2 debug integration: ~30+ blocks
- Terminal output examples: ~100+ blocks
- Window configuration commands: ~200+ blocks

**Current formats requiring conversion**:
- Language-tagged blocks: ````spin2`, ````pasm2`
- DEBUG statement blocks: Need special `::: debug` wrapper
- Terminal output: Need `::: terminal` wrapper
- Mixed code/output blocks: Need splitting

### Debug Window-Specific Elements
**Visual Debug Elements** requiring special handling:
- Terminal window output → `::: terminal`
- Bitmap window commands → `::: bitmap`
- Scope window commands → `::: scope`
- Logic window commands → `::: logic`
- Plot window commands → `::: plot`
- FFT window commands → `::: fft`
- Spectro window commands → `::: spectro`
- Scope_XY commands → `::: scope_xy`
- Screenshot callouts → `::: screenshot`

**Discovery & Learning Elements**:
- Discovery moments → `::: discovery`
- Experiments → `::: experiment`
- Performance tips → `::: performance`
- Pro tips → `::: tip`

## Required Transformations

### 1. Automated Code Block Conversion 🚀 **USE EXISTING SCRIPT**

**Automated Tool**: `/engineering/tools/convert-to-div-syntax.py`
```bash
# First, copy opus-master to workspace
cp ../manuals/p2-debug-window-manual/opus-master/COMPLETE-OPUS-MASTER.md \
   P2-Debug-Window-Manual.md

# Then convert code blocks
python3 ../../tools/convert-to-div-syntax.py \
  P2-Debug-Window-Manual.md \
  P2-Debug-Window-Manual-converted.md
```

**What the script handles**:
- ✅ Converts all `spin2` and `pasm2` blocks to div syntax
- ✅ Automatically adds blank lines where needed
- ✅ Provides statistics on conversions

**Post-script cleanup required**:
1. Convert DEBUG() statement blocks to `::: debug`
2. Convert terminal output blocks to `::: terminal`
3. Add window-specific wrappers (bitmap, scope, logic, etc.)
4. Add semantic elements (discovery, experiment, etc.)

### 2. DEBUG Statement Block Conversion 🔵 **MANUAL REQUIRED**

**Purpose**: DEBUG() statements need special highlighting to distinguish from regular code

```markdown
<!-- BEFORE -->
```spin2
PUB main()
  DEBUG("Hello, World!")
  DEBUG(`SCOPE MyScope SIZE 800 400`)
```

<!-- AFTER -->
::: debug
```
DEBUG("Hello, World!")
DEBUG(`SCOPE MyScope SIZE 800 400`)
```
:::
```

**Detection Pattern**: Look for lines starting with `DEBUG(` or `DEBUG``

### 3. Terminal Output Block Conversion ⚪ **MANUAL REQUIRED**

**Purpose**: Show what appears in terminal window, distinct from code

```markdown
<!-- BEFORE -->
```
Value: 1234
Temperature: 72.5°F
Status: Running
```

<!-- AFTER -->
::: terminal
```
Value: 1234
Temperature: 72.5°F
Status: Running
```
:::
```

### 4. Window-Specific Command Blocks 🟣 **CATEGORIZATION REQUIRED**

**Purpose**: Different window types need visual distinction

**Bitmap Window Commands**:
```markdown
::: bitmap
```
DEBUG(`BITMAP MyBitmap SIZE 256 256 COLOR $FF_00_00`)
DEBUG(`MyBitmap PIXEL 128 128`)
```
:::
```

**Scope Window Commands**:
```markdown
::: scope
```
DEBUG(`SCOPE MyScope SIZE 800 400 RANGE -5000 5000`)
DEBUG(`MyScope TRIGGER RISING 2500`)
```
:::
```

**Logic Window Commands**:
```markdown
::: logic
```
DEBUG(`LOGIC MyLogic SIZE 800 200 SAMPLES 1024`)
DEBUG(`MyLogic TRIGGER %10101010`)
```
:::
```

### 5. Discovery & Experiment Boxes 🎯 **PEDAGOGICAL ELEMENTS**

**Discovery Boxes** (Major findings):
```markdown
<!-- BEFORE -->
The sprite-based layer approach delivers 20× performance improvement...

<!-- AFTER -->
::: discovery
**Discovery**: The sprite-based layer approach delivers 20× performance improvement through layer composition. A single CROP command can update complex displays instantly.
:::
```

**Experiment Boxes** (Try it yourself):
```markdown
<!-- BEFORE -->
Try modifying the update rate from 10Hz to 60Hz...

<!-- AFTER -->
::: experiment
**Experiment**: Modify the update rate from 10Hz to 60Hz

**Code to modify**:
::: debug
```
DEBUG(`SCOPE MyScope UPDATE 60`)
```
:::

**Expected Result**: Smoother waveform updates with minimal CPU impact.
:::
```

## 5-Color Code Block System (Debug Window Focus)

### Color Mappings

**🟢 GREEN - Spin2 Blocks** (program structure)
- Markdown: `::: spin2`
- Purpose: Main program, object structure

**🟡 YELLOW - PASM2 Blocks** (assembly debug)
- Markdown: `::: pasm2`
- Purpose: Low-level debugging, assembly integration

**🔵 BLUE - DEBUG Blocks** (debug statements)
- Markdown: `::: debug`
- Purpose: DEBUG() statement syntax and examples

**⚪ GRAY - Terminal Blocks** (output display)
- Markdown: `::: terminal`
- Purpose: What appears in terminal window

**🟣 PURPLE - Window Command Blocks** (visual debug)
- Markdown: `::: bitmap`, `::: scope`, `::: logic`, etc.
- Purpose: Window-specific configuration and commands

## Semantic Environment Mappings

### Debug Window-Specific Environments

**🔍 discovery** (Major discoveries)
- Markdown: `::: discovery`
- Purpose: Highlight breakthrough findings
- LaTeX Environment: `DebugWinDiscovery`

**🧪 experiment** (Hands-on learning)
- Markdown: `::: experiment`
- Purpose: Interactive exercises
- LaTeX Environment: `DebugWinExperiment`

**⚡ performance** (Performance tips)
- Markdown: `::: performance`
- Purpose: Optimization guidance
- LaTeX Environment: `DebugWinPerformance`

**💡 tip** (Pro tips)
- Markdown: `::: tip`
- Purpose: Advanced techniques
- LaTeX Environment: `DebugWinTip`

**📸 screenshot** (Visual proof)
- Markdown: `::: screenshot`
- Purpose: Annotated screenshots
- LaTeX Environment: `DebugWinScreenshot`

## Screenshot Integration

### Standard Screenshot Format
```markdown
::: screenshot
![Window Type showing Feature](images/debug-window-type-feature.png)
**Figure X.Y**: Caption describing what the screenshot demonstrates.
:::
```

### Screenshot Naming Convention
- Pattern: `debug-[window]-[feature]-[number].png`
- Examples:
  - `debug-terminal-hello-world-01.png`
  - `debug-scope-trigger-02.png`
  - `debug-logic-i2c-decode-03.png`
  - `debug-bitmap-sprite-04.png`

## Processing Workflow

### Step 1: Create Working Copy 📁
```bash
# Copy opus-master to workspace
cp ../manuals/p2-debug-window-manual/opus-master/COMPLETE-OPUS-MASTER.md \
   P2-Debug-Window-Manual.md
```

### Step 2: Apply Automated Conversion 🤖
```bash
# Convert basic code blocks
python3 ../../tools/convert-to-div-syntax.py \
  P2-Debug-Window-Manual.md \
  P2-Debug-Window-Manual-converted.md
  
# Move converted back
mv P2-Debug-Window-Manual-converted.md P2-Debug-Window-Manual.md
```

### Step 3: Manual Categorization 🏷️
1. Identify and wrap DEBUG() statements → `::: debug`
2. Identify and wrap terminal output → `::: terminal`
3. Categorize window commands → `::: bitmap`, `::: scope`, etc.
4. Add discovery boxes for major findings
5. Add experiment boxes for hands-on sections
6. Add performance tips where appropriate
7. Wrap screenshot references

### Step 4: Verification ✅
```bash
# No language tags should remain
grep -c '^```[sp]' P2-Debug-Window-Manual.md  # Should be 0

# Check div blocks exist
grep -c '^:::' P2-Debug-Window-Manual.md  # Should be high

# Check debug-specific elements
grep -c '::: debug\|::: terminal\|::: discovery' P2-Debug-Window-Manual.md
```

### Step 5: LaTeX Escaping 📝
```bash
# Escape for LaTeX processing
../../tools/latex-escape-all.sh \
  P2-Debug-Window-Manual.md \
  ../outbound/p2-debug-window-manual/P2-Debug-Window-Manual.md
```

### Step 6: Template and Filter Setup 🔧
Copy required files to outbound:
```bash
# Template files
cp p2kb-debugwin.latex ../outbound/p2-debug-window-manual/
cp p2kb-debugwin-content.sty ../outbound/p2-debug-window-manual/

# Lua filters (flat structure - no subdirectory!)
cp filters/p2kb-debugwin-div-blocks.lua ../outbound/p2-debug-window-manual/
cp filters/p2kb-debugwin-semantic.lua ../outbound/p2-debug-window-manual/

# Shared filter
cp ../../templates/shared/lua-utilities/p2kb-non-floating-images.lua \
   ../outbound/p2-debug-window-manual/

# Request configuration
cp request.json ../outbound/p2-debug-window-manual/
```

## Quality Assurance Checklist

### Code Block Verification ✅
- [ ] All `spin2` blocks → `::: spin2` (green)
- [ ] All `pasm2` blocks → `::: pasm2` (yellow)
- [ ] All DEBUG() statements → `::: debug` (blue)
- [ ] All terminal output → `::: terminal` (gray)
- [ ] Window commands properly categorized
- [ ] NO language-tagged blocks remain

### Semantic Element Verification ✅
- [ ] Discovery boxes highlight major findings
- [ ] Experiment boxes have clear instructions
- [ ] Performance tips properly marked
- [ ] Pro tips distinguished from regular content
- [ ] Screenshots properly wrapped and captioned

### Visual Verification ✅
- [ ] All screenshots exist in images/
- [ ] Screenshots display at 85% width
- [ ] Code colors distinct and meaningful
- [ ] Page breaks logical between topics

## Special Considerations for Debug Window Manual

### Multi-Window Coordination Examples
When showing coordinated debug displays:
```markdown
::: multichannel
**Channel 1 - Scope Window**:
::: scope
```
DEBUG(`SCOPE Ch1 SIZE 400 300`)
```
:::

**Channel 2 - Logic Window**:
::: logic
```
DEBUG(`LOGIC Ch2 SIZE 400 300`)
```
:::

**Result**: Synchronized display of analog and digital signals
:::
```

### Performance Comparison Blocks
When comparing approaches:
```markdown
::: performance-comparison
**Traditional Approach** (10% CPU):
::: spin2
```
repeat
  value := read_sensor()
  if value > threshold
    DEBUG("Over: ", udec(value))
```
:::

**Optimized Approach** (0.1% CPU):
::: debug
```
DEBUG(`SCOPE Monitor TRIGGER RISING 2500 'sensor_value')
```
:::

**Improvement**: 100× reduction in CPU overhead
:::
```

## File Locations

- **Opus Master**: `/manuals/p2-debug-window-manual/opus-master/COMPLETE-OPUS-MASTER.md`
- **Working Copy**: `/workspace/p2-debug-window-manual/P2-Debug-Window-Manual.md`
- **Outbound**: `/outbound/p2-debug-window-manual/P2-Debug-Window-Manual.md`
- **Images**: `/workspace/p2-debug-window-manual/images/`

## Template Requirements

The following templates must work with Debug Window Manual:
- `p2kb-foundation.sty` - Base layer (shared)
- `p2kb-debugwin-content.sty` - Debug Window styles (5-color + semantic)
- `p2kb-debugwin.latex` - Main template
- `p2kb-debugwin-div-blocks.lua` - Code block processing
- `p2kb-debugwin-semantic.lua` - Semantic element processing
- `p2kb-non-floating-images.lua` - Image placement (shared)

## Post-Processing Transformations Required

### Character Encoding Fixes

**Problem**: Special characters cause LaTeX compilation errors or display incorrectly.

#### Complete Unicode Character Fixes

**Script Available**: `fix-unicode-characters.py` handles all replacements automatically

##### Multiplication Sign Fix
- **Issue**: × (Unicode multiplication sign) appears as "Œ" in PDF
- **Fix**: Replace all × with ASCII x
- **Pattern**: `20×` → `20x`, `16×16` → `16x16`
- **Count**: 38 occurrences

##### Em Dash Fix
- **Issue**: — (em dash) may not render correctly in LaTeX
- **Fix**: Replace with -- (double hyphen)
- **Pattern**: `difference—it's` → `difference--it's`
- **Count**: 20 occurrences

##### Comparison Operators Fix
- **Issue**: ≤ and ≥ cause LaTeX errors
- **Fix**: Replace with <= and >=
- **Count**: 3 occurrences of ≤

##### Arrow Fix
- **Issue**: → (Unicode arrow) may not render
- **Fix**: Replace with ->
- **Count**: 6 occurrences

##### Checkmark Removal from Lists
- **Issue**: ✓ and ✗ at start of list items
- **Fix**: Remove from beginning of list items
- **Pattern**: `✓ **Fixed positioning**` → `**Fixed positioning**`
- **Count**: 25 list items with ✓

#### Greek Letter and Degree Symbol Fixes
- **Issue**: θ (theta) and ° (degree) cause LaTeX compilation errors in inline code
- **Fix in inline code blocks**: 
  - Replace `<r>,<θ>°` with `<r>,<theta>deg`
  - Replace standalone θ with `theta`
  - Replace standalone ° with `deg` (except in temperature readings)
- **Note**: Only required in inline code (backticks), not in regular text

### List Formatting Fixes

**Problem**: Numbered lists immediately after headings appear inline with heading text.

#### "Your Mission:" Section Fix
- **Issue**: Lists starting with "1. Your Mission:" appear inline
- **Fix**: Add blank line after heading before numbered list
- **Example**:
```markdown
<!-- BEFORE -->
### Discovery #1: Real-Time Without the Overhead
1. Your Mission: Monitor a temperature sensor

<!-- AFTER -->
### Discovery #1: Real-Time Without the Overhead

1. Your Mission: Monitor a temperature sensor
```
- **Pattern**: Search for all headings followed immediately by numbered lists

### LaTeX Style File Adjustments

#### Code Block Padding Fix (p2kb-debugwin-content.sty)
- **Issue**: Excessive 30pt left padding pushes code too far right
- **Fix**: Reduce to 10pt in all tcolorbox environments
- **Lines to modify**: All `left=30pt` → `left=10pt`
- **Affects**: spin2block, pasm2block, debugblock, terminalblock, etc.

#### Gray Background Removal (p2kb-debugwin-foundation.sty)
- **Issue**: Gray background overlays colored code blocks
- **Fix**: Comment out `backgroundcolor=\color{gray!10}` in lstset
- **Line**: Around line 172 in foundation style
- **Result**: Colored backgrounds show properly without gray overlay

## Success Metrics

🎯 **Target**: Complete conversion to div-wrapped format with debug-specific semantics

**Success Criteria**:
- ✅ 0 language-tagged blocks remaining
- ✅ 100% div-wrapped code blocks with proper categorization
- ✅ All DEBUG() statements in blue blocks
- ✅ All terminal output in gray blocks
- ✅ All discovery/experiment boxes properly styled
- ✅ All screenshots integrated at 85% width
- ✅ Professional appearance matching Smart Pins/DeSilva quality
- ✅ All special characters properly escaped (×→x, θ→theta, °→deg)
- ✅ All lists properly formatted with blank lines after headings
- ✅ Code blocks properly indented (10pt left padding)
- ✅ No gray background overlay on colored code blocks

## Why This Matters for Debug Window Manual

- **Visual Learning**: Different colors for different debug contexts
- **Practical Focus**: Experiments and discoveries drive learning
- **Screenshot Integration**: Visual proof of every capability
- **Performance Awareness**: Clear metrics and comparisons
- **Production Ready**: Templates enable professional documentation

---

**Status**: Guide complete, ready for Debug Window Manual transformation