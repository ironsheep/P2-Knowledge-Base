# P2 Debug Window Manual Template Development Plan

**Purpose**: Document the layered template architecture strategy for P2 Debug Window Manual
**Created**: September 16, 2025
**Strategy**: Leverage shared foundation with Debug Window-specific specializations

## 🏗️ Architecture Overview

### Three-Layer Strategy (Same as DeSilva)
1. **Foundation Layer**: Shared base components across all P2 documents
2. **Content Layer**: Debug Window-specific styling and environments
3. **Template Layer**: Debug Window assembly and configuration

### Benefits
- ✅ **Rapid Development**: Build on proven Smart Pins/DeSilva foundation
- ✅ **Debug-Specific Features**: Custom environments for debug windows
- ✅ **Visual Consistency**: Screenshots and code examples properly integrated
- ✅ **Future Flexibility**: Can add new debug window types as discovered

## 📁 Directory Structure for Debug Window

**UPDATED**: Templates are now stored in the workspace's `templates/` subdirectory for isolation.

```
/engineering/document-production/workspace/p2-debug-window-manual/
├── templates/                          ← Debug Window templates (isolated)
│   ├── p2kb-foundation.sty            ← Base typography, layout, fonts (local copy)
│   ├── p2kb-debugwin-foundation.sty   ← Debug Window foundation extensions
│   ├── p2kb-debugwin-content.sty      ← Debug-specific environments
│   ├── p2kb-debugwin.latex            ← Debug Window main template
│   └── README.md                       ← Debug Window template documentation
├── filters/                            ← Debug Window Lua filters
│   ├── p2kb-debugwin-div-blocks.lua   ← Debug window code processing
│   └── p2kb-debugwin-semantic.lua     ← Debug semantic elements
├── P2-Debug-Window-Manual.md          ← Working copy markdown
└── images/                             ← Screenshots and diagrams
```

## 🏷️ Namespace Strategy for Debug Window

### **Naming Convention**
```
Pattern: p2kb-debugwin-[component-type]-[specific-name]

Examples:
- p2kb-debugwin-div-blocks.lua
- p2kb-debugwin-semantic.lua
- p2kb-debugwin-content.sty
- p2kb-debugwin.latex
```

### **LaTeX Environment Namespaces**

**Debug Window-Specific** (prefixed - isolated scope):
```latex
% Debug Window Manual Code Blocks
\newenvironment{DebugWinSpin2Block}{...}{...}
\newenvironment{DebugWinPASM2Block}{...}{...}
\newenvironment{DebugWinDebugBlock}{...}{...}     % DEBUG() statements
\newenvironment{DebugWinTerminalBlock}{...}{...}  % Terminal output
\newenvironment{DebugWinBitmapBlock}{...}{...}    % Bitmap commands

% Debug Window Semantic Elements
\newenvironment{DebugWinDiscovery}{...}{...}      % Discovery moments
\newenvironment{DebugWinExperiment}{...}{...}     % Try-it-yourself
\newenvironment{DebugWinTip}{...}{...}            % Pro tips
\newenvironment{DebugWinPerformance}{...}{...}    % Performance notes
\newenvironment{DebugWinScreenshot}{...}{...}     % Screenshot callouts
```

## 🎨 Debug Window Color System

### 5-Color Code Block System (Debug Window Focused)

**🟢 GREEN - Spin2 Blocks** (program structure)
- Markdown: `::: spin2`
- LaTeX Environment: `DebugWinSpin2Block`
- Purpose: Program structure, debug setup

**🟡 YELLOW - PASM2 Blocks** (low-level debug)
- Markdown: `::: pasm2`
- LaTeX Environment: `DebugWinPASM2Block`
- Purpose: PASM-level debugging examples

**🔵 BLUE - DEBUG Blocks** (debug statements)
- Markdown: `::: debug`
- LaTeX Environment: `DebugWinDebugBlock`
- Purpose: DEBUG() statement examples with syntax highlighting

**⚪ GRAY - Terminal Blocks** (output examples)
- Markdown: `::: terminal`
- LaTeX Environment: `DebugWinTerminalBlock`
- Purpose: Show terminal window output

**🟣 PURPLE - Bitmap/Graphics Blocks** (visual debug)
- Markdown: `::: bitmap`
- LaTeX Environment: `DebugWinBitmapBlock`
- Purpose: Bitmap, plot, scope commands

## 🚀 Development Workflow for Debug Window

### **Phase 1: Foundation Setup** (COMPLETED)
```bash
# Foundation is now in workspace/p2-debug-window-manual/templates/
# Each workspace has its own isolated copy
templates/p2kb-foundation.sty
templates/p2kb-debugwin-foundation.sty
```

### **Phase 2: Debug Window-Specific Development** (COMPLETED)

1. **Content Layer** (✅ DONE):
```bash
# Location: workspace/p2-debug-window-manual/templates/p2kb-debugwin-content.sty
# Contains: 5-color debug blocks + debug semantic environments
```

2. **Lua Filters** (✅ DONE):
```bash
# Location: workspace/p2-debug-window-manual/filters/p2kb-debugwin-div-blocks.lua
# Converts: ::: spin2|pasm2|debug|terminal|bitmap → LaTeX environments

# Location: workspace/p2-debug-window-manual/filters/p2kb-debugwin-semantic.lua
# Converts: ::: discovery|experiment|tip|performance → LaTeX environments
```

3. **Main Template** (✅ DONE):
```bash
# Location: workspace/p2-debug-window-manual/templates/p2kb-debugwin.latex
# Includes: p2kb-foundation.sty + p2kb-debugwin-foundation.sty + p2kb-debugwin-content.sty
```

### **Phase 3: Testing & Refinement**
1. **Test with Chapter 1** (Beyond Basic DEBUG)
2. **Verify screenshot integration** (85% width working)
3. **Check code block colors** (5-color system)
4. **Validate semantic elements** (discoveries, experiments)

## 🎯 Implementation Priorities for Debug Window

### **High Priority** (Block deployment)
1. 🔄 Debug Window content layer (`p2kb-debugwin-content.sty`)
2. 🔄 Debug Window Lua filters (div processing)
3. 🔄 Debug Window main template assembly
4. 🔄 Screenshot integration testing

### **Medium Priority** (Enhance presentation)
1. 📋 Window-specific styling (terminal, bitmap, plot, etc.)
2. 📋 Performance comparison boxes
3. 📋 Discovery callout formatting

### **Low Priority** (Future enhancements)
1. 📋 Interactive element markers
2. 📋 Video reference placeholders
3. 📋 Cross-reference automation

## 🔧 Template Assembly Pattern for Debug Window

```latex
% Debug Window template: templates/p2kb-debugwin.latex

% 1. Foundation layer (local copy)
\usepackage{p2kb-foundation}

% 2. Foundation extensions (debug-specific)
\usepackage{p2kb-debugwin-foundation}

% 3. Content layer (debug-specific)
\usepackage{p2kb-debugwin-content}

% 4. Document configuration
\title{P2 Debug Window Manual}
\subtitle{Visual Discovery Through Systematic Exploration}
\author{Propeller 2 Development Team}

% 5. Debug Window-specific customizations
\renewcommand{\chapterformat}{...}  % If needed for part structure
```

## 📋 Debug Window Semantic Elements

### Discovery Boxes (Major findings)
```markdown
::: discovery
**Discovery**: The sprite-based layer approach delivers 20× performance improvement through layer composition.
:::
```

### Experiment Sections (Try it yourself)
```markdown
::: experiment
**Experiment**: Modify the update rate from 10Hz to 60Hz and observe the difference in responsiveness.

Code to modify:
` ` `spin2
DEBUG(`SCOPE MyScope SAMPLES 1024 RATE 1000000`)
` ` `

Expected Result: Smoother waveform updates with minimal CPU impact.
:::
```

### Performance Notes (Optimization tips)
```markdown
::: performance
**Performance Tip**: Use packed data format for 16× reduction in bandwidth requirements.
:::
```

### Screenshot Callouts (Visual proof)
```markdown
::: screenshot
![Logic Analyzer showing I2C protocol](images/logic-i2c-decoded.png)
**Figure 3.2**: LOGIC window automatically decoding I2C protocol with address and data visible.
:::
```

## 🧪 Testing Strategy for Debug Window

### **Chapter-by-Chapter Testing**
- Start with Chapter 1 (vision/overview)
- Test each window type chapter individually
- Verify all code examples compile
- Check screenshot placement and sizing

### **Integration Testing**
- Full manual PDF generation
- Cross-references working
- Table of contents accurate
- Appendices properly formatted

## 📊 Debug Window-Specific Requirements

### Screenshot Management
- **Format**: PNG preferred for clarity
- **Width**: 85% of text width (via non-floating-images.lua)
- **Naming**: `debug-[window-type]-[feature].png`
- **Location**: `images/` subdirectory

### Code Example Categories
1. **Basic DEBUG()** - Simple text output
2. **Window Creation** - BITMAP, SCOPE, LOGIC, etc.
3. **Configuration** - SIZE, RANGE, TRIGGER, etc.
4. **Data Streaming** - SAMPLES, continuous updates
5. **Multi-Window** - Coordinated debug displays

### Performance Metrics to Document
- Update rates (Hz)
- Bandwidth usage (bytes/sec)
- CPU overhead (%)
- Memory footprint (bytes)

## 🚨 Risk Mitigation for Debug Window

### **Screenshot Quality**
- **Risk**: Low-quality or missing screenshots
- **Mitigation**: Create screenshot checklist, validate all images

### **Code Example Accuracy**
- **Risk**: Non-working debug examples
- **Mitigation**: Test all examples on P2 hardware

### **Window Type Coverage**
- **Risk**: Missing or incomplete window type documentation
- **Mitigation**: Systematic exploration of all 9 window types

## 📋 Success Metrics for Debug Window Manual

### **Content Quality**
- ✅ All 9 window types documented with examples
- ✅ Every feature claim backed by screenshot
- ✅ Code examples tested and working
- ✅ Performance metrics validated

### **Visual Presentation**
- ✅ Consistent 5-color code system
- ✅ Screenshots at 85% width
- ✅ Clear discovery/experiment boxes
- ✅ Professional layout matching other manuals

### **Learning Effectiveness**
- ✅ Progressive complexity from basic to advanced
- ✅ Hands-on experiments in each chapter
- ✅ Clear performance comparisons
- ✅ Practical production examples

## 🔄 Migration from Opus Master

### **Source Files**
- **Master**: `manuals/p2-debug-window-manual/opus-master/COMPLETE-OPUS-MASTER.md`
- **Working**: `workspace/p2-debug-window-manual/P2-Debug-Window-Manual.md`

### **Conversion Steps**
1. Copy master to workspace
2. Apply div syntax conversion for code blocks
3. Add debug semantic elements (discovery, experiment, etc.)
4. Verify all screenshots referenced exist
5. Test with subset before full generation

## 📝 File Naming Standards (NO SUFFIXES)

**NEVER create**:
- ❌ `p2kb-debugwin-content-v2.sty`
- ❌ `P2-Debug-Window-Manual-FINAL.md`
- ❌ `p2kb-debugwin-div-blocks-fixed.lua`

**ALWAYS use**:
- ✅ `p2kb-debugwin-content.sty`
- ✅ `P2-Debug-Window-Manual.md`
- ✅ `p2kb-debugwin-div-blocks.lua`

## 🎯 Next Steps

1. **Create workspace working copy** from opus-master
2. **Develop p2kb-debugwin-content.sty** with 5-color system
3. **Create Lua filters** for debug div processing
4. **Test with Chapter 1** for proof of concept
5. **Iterate based on visual results**

---

**Status**: Ready to begin Debug Window template development based on proven Smart Pins/DeSilva patterns.