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

**UPDATED**: Templates are now stored in each document's workspace `templates/` subdirectory for isolation and simplicity.

```
/engineering/document-production/workspace/
├── p2-smart-pins-manual/              ← Smart Pins document workspace
│   ├── templates/                     ← Smart Pins templates (isolated)
│   │   ├── p2kb-foundation.sty       ← Foundation layer (copy)
│   │   ├── p2kb-smartpins-content.sty ← Smart Pins content layer
│   │   └── p2kb-smartpins.latex      ← Smart Pins main template
│   └── filters/                       ← Smart Pins Lua filters
│       └── p2kb-smartpins-*.lua
├── p2-pasm-desilva-style/             ← DeSilva manual workspace
│   ├── templates/                     ← DeSilva templates (isolated)
│   │   ├── p2kb-foundation.sty       ← Foundation layer (copy)
│   │   ├── p2kb-desilva-content.sty  ← 5-color blocks + pedagogical envs
│   │   ├── p2kb-desilva-foundation.sty ← DeSilva foundation extensions
│   │   └── p2kb-desilva.latex        ← DeSilva main template
│   └── filters/                       ← DeSilva Lua filters
│       └── p2kb-desilva-*.lua
├── p2-debug-window-manual/            ← Debug Window manual workspace
│   ├── templates/                     ← Debug Window templates (isolated)
│   │   ├── p2kb-foundation.sty       ← Foundation layer (copy)
│   │   ├── p2kb-debugwin-content.sty ← Debug-specific environments
│   │   ├── p2kb-debugwin-foundation.sty ← Debug Window foundation extensions
│   │   └── p2kb-debugwin.latex       ← Debug Window main template
│   └── filters/                       ← Debug Window Lua filters
│       └── p2kb-debugwin-*.lua
```

**Benefits of workspace-local templates:**
- ✅ Complete isolation between documents
- ✅ No risk of cross-document interference
- ✅ Self-contained workspaces for easier deployment
- ✅ Clear ownership of each template set

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

### **Phase 1: Foundation Setup** (COMPLETED)
Templates are now stored in each workspace's `templates/` subdirectory.

1. **Foundation copies in each workspace**:
   ```bash
   # Each workspace has its own copy of foundation
   workspace/p2-pasm-desilva-style/templates/p2kb-foundation.sty
   workspace/p2-debug-window-manual/templates/p2kb-foundation.sty
   workspace/p2-smart-pins-manual/templates/p2kb-foundation.sty
   ```

2. **No central shared directory** - isolation preferred for production stability

### **Phase 2: Document-Specific Development** (COMPLETED)

**For DeSilva Manual** (✅ DONE):
1. **Content Layer**: `workspace/p2-pasm-desilva-style/templates/p2kb-desilva-content.sty`
2. **Foundation Extensions**: `workspace/p2-pasm-desilva-style/templates/p2kb-desilva-foundation.sty`
3. **Main Template**: `workspace/p2-pasm-desilva-style/templates/p2kb-desilva.latex`
4. **Lua Filters**: `workspace/p2-pasm-desilva-style/filters/p2kb-desilva-*.lua`

**For Debug Window Manual** (✅ DONE):
1. **Content Layer**: `workspace/p2-debug-window-manual/templates/p2kb-debugwin-content.sty`
2. **Foundation Extensions**: `workspace/p2-debug-window-manual/templates/p2kb-debugwin-foundation.sty`
3. **Main Template**: `workspace/p2-debug-window-manual/templates/p2kb-debugwin.latex`
4. **Lua Filters**: `workspace/p2-debug-window-manual/filters/p2kb-debugwin-*.lua`

**For Smart Pins Manual** (✅ DONE):
1. **Templates**: `workspace/p2-smart-pins-manual/templates/`
2. **Filters**: `workspace/p2-smart-pins-manual/filters/`

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
Each document template follows this pattern (all paths relative to workspace/[document]/):

```latex
% Document-specific template: templates/p2kb-[document].latex

% 1. Foundation layer (local copy)
\usepackage{p2kb-foundation}

% 2. Document-specific foundation extensions (if needed)
\usepackage{p2kb-[document]-foundation}

% 3. Content layer (document-specific)
\usepackage{p2kb-[document]-content}

% 4. Document configuration
\title{Document-Specific Title}
\author{Document-Specific Author}

% 5. Document-specific customizations
\renewcommand{\chapterformat}{...}  % If needed
```

### **Lua Filter Assembly Pattern**
Each document uses this filter chain (filters in workspace/[document]/filters/):

```json
{
  "lua_filters": [
    "p2kb-[document]-code-coloring",
    "p2kb-[document]-semantic",
    "p2kb-[document]-pagination"
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