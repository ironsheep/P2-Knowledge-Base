# P2KB Template Development Plan

**Purpose**: Document the layered template architecture strategy for multiple P2 documents
**Created**: September 16, 2025
**Strategy**: Layered Isolation with Shared Foundation

## 🏗️ Architecture Overview

### Three-Layer Strategy
1. **Foundation Layer**: Shared base components across all P2 documents
2. **Content Layer**: Document-specific styling and environments
3. **Template Layer**: Document assembly and configuration

### Benefits
- ✅ **Rapid Development**: Isolated document development without interference
- ✅ **Production Safety**: Changes to one document don't affect others
- ✅ **Code Reuse**: Shared foundation provides consistency
- ✅ **Future Flexibility**: Can optimize/merge later without blocking current work

## 📁 Directory Structure

```
/engineering/document-production/templates/
├── README.md                           ← This plan document
├── shared/                             ← Foundation layer (ALL documents)
│   ├── p2kb-foundation.sty            ← Base typography, layout, fonts
│   ├── p2kb-common-environments.sty   ← Shared environments (equations, tables)
│   └── lua-utilities/
│       ├── p2kb-non-floating-images.lua    ← Image placement (85% width)
│       ├── p2kb-common-div-helpers.lua     ← Div detection utilities
│       └── p2kb-latex-escape-helpers.lua   ← String processing utilities
├── smart-pins/                        ← Smart Pins document family
│   ├── p2kb-smartpins-content.sty     ← 3-color blocks + semantic envs
│   ├── p2kb-smartpins.latex           ← Smart Pins main template
│   ├── p2kb-smartpins-div-blocks.lua       ← spin2/pasm2/antipattern processing
│   ├── p2kb-smartpins-semantic-blocks.lua  ← needs-diagram, tip, etc.
│   └── README-smartpins.md            ← Smart Pins specific documentation
├── desilva/                           ← DeSilva manual family
│   ├── p2kb-desilva-content.sty       ← 5-color blocks + pedagogical envs
│   ├── p2kb-desilva.latex             ← DeSilva main template
│   ├── p2kb-desilva-div-blocks.lua          ← 5-color code block processing
│   ├── p2kb-desilva-semantic-blocks.lua     ← medicine, yourturn, sidetrack, etc.
│   └── README-desilva.md              ← DeSilva specific documentation
├── debug-window/                      ← Debug Window manual family
│   ├── p2kb-debugwin-content.sty      ← Debug-specific environments
│   ├── p2kb-debugwin.latex            ← Debug Window main template
│   └── README-debugwin.md             ← Debug Window documentation
└── future-documents/                  ← Template for new document families
    └── TEMPLATE-README.md              ← How to add new document types
```

## 🏷️ Namespace Strategy

### **Document-Prefixed Namespacing**
**Decision**: Use document prefixes to avoid LaTeX environment/command conflicts

### **Naming Convention**
```
Pattern: p2kb-[document-type]-[component-type]-[specific-name]

Examples:
- p2kb-desilva-div-blocks.lua
- p2kb-smartpins-div-blocks.lua  
- p2kb-desilva-content.sty
- p2kb-smartpins-content.sty
```

### **CRITICAL: P2KB Prefix for Lua Filters**
**Issue**: PDF Forge is a shared environment with multiple configuration sources
**Solution**: ALL P2KB Lua filters MUST use `p2kb-` prefix to prevent namespace collisions

```
❌ Old (collision risk):    desilva-div-blocks.lua
✅ New (namespace safe):   p2kb-desilva-div-blocks.lua

❌ Old (collision risk):    non-floating-images.lua  
✅ New (namespace safe):   p2kb-non-floating-images.lua
```

**Migration Strategy**: 
- New documents: Use p2kb- prefix from start
- Existing documents: Migrate during next update cycle
- No exceptions: ALL Lua filters get p2kb- prefix

### **LaTeX Environment Namespaces**

**Shared Foundation** (no prefix - global scope):
```latex
% Shared across all documents
\newenvironment{P2CodeGeneric}{...}{...}
\newcommand{\P2InlineCode}[1]{...}
\newenvironment{P2Table}{...}{...}
```

**Document-Specific** (prefixed - isolated scope):
```latex
% DeSilva Manual
\newenvironment{DeSilvaSpin2Block}{...}{...}
\newenvironment{DeSilvaPASM2Block}{...}{...}
\newenvironment{DeSilvaCORDICBlock}{...}{...}
\newenvironment{DeSilvaMultiCOGBlock}{...}{...}
\newenvironment{DeSilvaMedicineCabinet}{...}{...}
\newenvironment{DeSilvaYourTurn}{...}{...}
\newenvironment{DeSilvaSidetrack}{...}{...}

% Smart Pins Manual
\newenvironment{SmartPinsSpin2Block}{...}{...}
\newenvironment{SmartPinsPASM2Block}{...}{...}
\newenvironment{SmartPinsAntipatternBlock}{...}{...}
\newenvironment{SmartPinsNeedsDiagram}{...}{...}
\newenvironment{SmartPinsTip}{...}{...}
```

### **Benefits of Prefixed Namespacing**
- ✅ **Zero Conflicts**: Documents can't interfere with each other
- ✅ **Clear Ownership**: Easy to see which document an environment belongs to
- ✅ **Parallel Development**: Teams can work on different documents simultaneously
- ✅ **Debugging**: Clear error messages show which document has issues
- ✅ **Future Merging**: Can always create aliases later if needed

## 🚀 Development Workflow

### **Phase 1: Foundation Setup** (One-time)
1. **Extract Working Foundation**:
   ```bash
   # Copy proven Smart Pins foundation as base
   cp smart-pins-current/p2kb-foundation.sty templates/shared/
   cp smart-pins-current/non-floating-images.lua templates/shared/lua-utilities/p2kb-non-floating-images.lua
   ```

2. **Clean Foundation** (remove document-specific elements):
   - Keep: Typography, page layout, basic environments
   - Remove: Smart Pins specific environments and colors

### **Phase 2: Document-Specific Development** (Parallel)

**For DeSilva Manual**:
1. **Create Content Layer**:
   ```bash
   # New file: templates/desilva/p2kb-desilva-content.sty
   # Contains: 5-color code blocks + DeSilva pedagogical environments
   ```

2. **Create Lua Filters**:
   ```bash
   # New file: templates/desilva/p2kb-desilva-div-blocks.lua
   # Converts: ::: spin2|pasm2|cordic|multicog|antipattern → LaTeX environments
   
   # New file: templates/desilva/p2kb-desilva-semantic-blocks.lua  
   # Converts: ::: medicine|yourturn|sidetrack|chapterend → LaTeX environments
   ```

3. **Create Main Template**:
   ```bash
   # New file: templates/desilva/p2kb-desilva.latex
   # Includes: shared/p2kb-foundation.sty + desilva/p2kb-desilva-content.sty
   ```

**For Smart Pins Manual** (migrate existing):
1. **Extract to Content Layer**:
   ```bash
   # New file: templates/smart-pins/p2kb-smartpins-content.sty
   # Move Smart Pins specific environments from current template
   ```

2. **Update Existing Filters**:
   ```bash
   # Rename: smart-pins-div-blocks.lua → templates/smart-pins/p2kb-smartpins-div-blocks.lua
   # Update: Environment names to use SmartPins prefix
   # Add: p2kb- prefix for PDF Forge namespace safety
   ```

### **Phase 3: Testing & Refinement**
1. **Test Each Document Independently**:
   - DeSilva manual with new template stack
   - Smart Pins manual with migrated template stack
   - Verify no cross-document interference

2. **Iterative Refinement**:
   - Adjust document-specific styling without affecting others
   - Add new features to one document without breaking others

## 🎯 Implementation Priorities

### **High Priority** (Block deployment)
1. ✅ DeSilva content layer (`p2kb-desilva-content.sty`)
2. ✅ DeSilva Lua filters (div processing)
3. ✅ DeSilva main template assembly

### **Medium Priority** (Improve workflow)
1. 🔄 Smart Pins migration to new structure
2. 🔄 Foundation layer cleanup and optimization
3. 🔄 Lua utility extraction

### **Low Priority** (Future optimization)
1. 📋 Cross-document pattern analysis
2. 📋 Common environment extraction
3. 📋 Template consolidation opportunities

## 🔧 Template Assembly Pattern

### **Standard Assembly Pattern**
Each document template follows this pattern:

```latex
% Document-specific template: p2kb-[document].latex

% 1. Foundation layer (shared)
\usepackage{shared/p2kb-foundation}

% 2. Content layer (document-specific)
\usepackage{[document]/p2kb-[document]-content}

% 3. Document configuration
\title{Document-Specific Title}
\author{Document-Specific Author}

% 4. Document-specific customizations
\renewcommand{\chapterformat}{...}  % If needed
```

### **Lua Filter Assembly Pattern**
Each document uses this filter chain:

```json
{
  "lua_filters": [
    "shared/lua-utilities/p2kb-non-floating-images",
    "[document]/p2kb-[document]-div-blocks", 
    "[document]/p2kb-[document]-semantic-blocks"
  ]
}
```

## 🧪 Testing Strategy

### **Unit Testing** (Individual components)
- Test each `.sty` file compiles without errors
- Test each Lua filter processes sample divs correctly
- Test template assembly includes all required components

### **Integration Testing** (Full document)
- Generate PDF from each document type
- Verify all environments render correctly
- Check for LaTeX conflicts or naming collisions

### **Regression Testing** (Cross-document safety)
- Ensure changes to one document don't affect others
- Verify shared foundation changes work for all documents
- Test parallel development scenarios

## 🔄 Migration Path

### **Smart Pins Migration** (Low risk)
1. **Copy current working template** to new structure
2. **Extract shared elements** to foundation layer
3. **Rename environments** with SmartPins prefix
4. **Test thoroughly** before switching production

### **DeSilva Creation** (New development)
1. **Start with foundation** + new content layer
2. **Develop iteratively** without affecting Smart Pins
3. **Test frequently** with sample content
4. **Deploy when ready** independently

## 📋 Success Metrics

### **Development Velocity**
- ✅ Documents can be developed in parallel
- ✅ Changes to one document don't block others
- ✅ New document types can be added easily

### **Production Quality**
- ✅ Each document produces professional PDFs
- ✅ Consistent base typography across documents
- ✅ Document-specific pedagogical elements work correctly

### **Maintainability**
- ✅ Clear separation of concerns
- ✅ Documented namespace strategy
- ✅ Easy to add new documents or features

## 🚨 Risk Mitigation

### **Namespace Conflicts**
- **Risk**: LaTeX environment name collisions
- **Mitigation**: Strict prefixing convention enforced

### **Foundation Changes**
- **Risk**: Shared foundation changes break existing documents
- **Mitigation**: Thorough testing before foundation updates

### **Development Complexity**
- **Risk**: Too many files to manage
- **Mitigation**: Clear documentation and README files in each directory

---

**Next Steps**: Begin Phase 1 with foundation extraction and DeSilva content layer development.