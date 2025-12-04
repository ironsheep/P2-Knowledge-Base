# P2 Single-Step Debugger Manual - Template Theory of Operations

**Document:** P2-Single-Step-Debugger-Manual.md (TBD)
**Template Prefix:** `p2kb-debugger-*` (to be established)
**Version:** 0.1 (Placeholder)
**Last Updated:** 2025-12-03
**Status:** PLANNED - Not Started (No content or custom templates yet)

## Overview

This workspace is in **early planning stage**. No custom templates or document content have been created yet. Only the shared `p2kb-foundation.sty` is present.

## Current Template Stack Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      NOT YET CREATED                         │
│          (p2kb-debugger.latex will go here)                  │
├─────────────────────────────────────────────────────────────┤
│                   p2kb-foundation.sty                        │
│                  (Shared Foundation Only)                    │
│            Available for future development                  │
└─────────────────────────────────────────────────────────────┘
```

## Files Currently Present

| File | Status | Purpose |
|------|--------|---------|
| `README.md` | ✅ Complete | Workspace documentation with gold standard format |
| `templates/README.md` | ✅ Complete | Template planning documentation |
| `templates/p2kb-foundation.sty` | ✅ Present | Shared foundation (reference only) |

## Files to Create When Development Begins

### Template Files Needed

```
templates/
├── p2kb-debugger.latex           # Master Pandoc template
├── p2kb-debugger-foundation.sty  # Document-specific foundation
└── p2kb-debugger-content.sty     # Content layer (debugging UI, workflows)
```

### Lua Filters Potentially Needed

```
filters/
├── p2kb-debugger-div-blocks.lua  # Code block styling
├── p2kb-debugger-semantic.lua    # Semantic environments
└── p2kb-debugger-screenshots.lua # Screenshot processing (TBD)
```

### Configuration Files Needed

```
request.json                      # PDF Forge configuration
request-requirements.json         # Mandatory pandoc arguments
```

## Design Decisions Pending

### 1. Document Style
| Option | Description | Best For |
|--------|-------------|----------|
| **Tutorial** | Step-by-step learning | New debugger users |
| **Reference** | Feature lookup | Experienced users |
| **Visual Discovery** | Screenshot-driven | Complex UI documentation |

**Recommendation:** Visual Discovery approach (like Debug Window Manual) since the debugger has significant UI elements.

### 2. Template Starting Point
| Template Source | Pros | Cons |
|-----------------|------|------|
| `p2kb-debugwin-*` | Visual/discovery style, screenshot support | May have debug window-specific elements |
| `p2kb-desilva-*` | Tutorial style, pedagogical | Less visual focus |
| `p2kb-sp-*` | Technical reference | Tutorial-focused |

**Recommended:** Start from `p2kb-debugwin-*` templates since both are debugger-related tools and share similar documentation needs (screenshots, UI descriptions, workflow documentation).

### 3. Relationship with Debug Window Manual
Both documents are debugging-related. Consider:

| Consideration | Recommendation |
|---------------|----------------|
| Visual style | Share color palette and screenshot styling |
| Code blocks | May share same 5-color system |
| Cross-references | Link between documents where relevant |
| Content overlap | Clearly delineate scope - Debug Window = data visualization, Single-Step = execution control |

### 4. Code Block System
Likely inherit from Debug Window Manual:

| Block Type | Purpose |
|------------|---------|
| Spin2 | Program code being debugged |
| PASM2 | Assembly code being debugged |
| Debug Commands | Debugger commands/interactions |
| Output | Debugger output display |

### 5. Top-Level Division
| Option | Use Case |
|--------|----------|
| `--top-level-division=part` | If organizing by major debugger areas |
| `--top-level-division=chapter` | If simpler organization |

**Recommendation:** Use `part` only if document is large enough to warrant it; otherwise `chapter` for simpler navigation.

## Content Characteristics (When Developed)

### Core Sections Expected
1. **Introduction** - What is single-step debugging on P2
2. **Setup** - How to enable/configure the debugger
3. **Basic Operations** - Step, continue, break, examine
4. **Breakpoints** - Setting, conditional, watchpoints
5. **Variable Inspection** - Viewing COG/HUB/registers
6. **Call Stack** - Understanding execution flow
7. **Advanced Features** - Multi-cog debugging, specialized modes
8. **Troubleshooting** - Common issues and solutions

### Special Features Needed
- **UI Screenshots** - Every debugger pane documented
- **Keyboard Shortcuts** - Reference tables
- **Workflow Diagrams** - Debug session flows
- **Code Examples** - Debugging real P2 programs

## Naming Convention Compliance

### When Templates Are Created

All files should follow: `p2kb-{docprefix}-{purpose}.{ext}`

| File | Pattern Compliance |
|------|-------------------|
| `p2kb-debugger.latex` | ✅ Will be correct |
| `p2kb-debugger-foundation.sty` | ✅ Will be correct |
| `p2kb-debugger-content.sty` | ✅ Will be correct |
| `p2kb-debugger-div-blocks.lua` | ✅ Will be correct |

**Note:** Using `debugger` prefix (not `debug` or `ssdebug`) to be distinct but clear.

## Related Documents

| Document | Relationship |
|----------|--------------|
| **Debug Window Manual** | Coordinate to avoid overlap; link where relevant; share visual style |

## Scope Delineation with Debug Window Manual

| Topic | Debug Window Manual | Single-Step Debugger Manual |
|-------|--------------------|-----------------------------|
| DEBUG() statements | ✅ Primary focus | Reference only |
| 9 window types | ✅ Complete coverage | Reference for data display |
| Execution control | Reference only | ✅ Primary focus |
| Breakpoints | N/A | ✅ Primary focus |
| Step operations | N/A | ✅ Primary focus |
| Variable inspection | Data visualization | ✅ Examine/watch |
| Multi-cog debugging | N/A | ✅ Primary focus |

## Next Steps to Begin Development

1. **Confirm priority** - Check with user if this document should be developed
2. **Define scope clearly** - What does single-step debugger cover vs. Debug Window?
3. **Copy template base** - Start from `p2kb-debugwin-*` templates
4. **Rename with prefix** - `p2kb-debugger-*`
5. **Adapt content layer** - Remove debug window specifics, add debugger-specific environments
6. **Create content outline** - Define chapter/section structure
7. **Build incrementally** - Start with basic operations section

## When Working on This Document

### Before Starting Development:
1. Confirm user wants to prioritize this document
2. Review Debug Window Manual to understand scope boundaries
3. Identify available source material for single-step debugger
4. Decide on document style with user input

### Initial Development Steps:
1. Copy template files from Debug Window Manual
2. Rename with `p2kb-debugger-*` prefix
3. Modify content.sty to remove debug window-specific environments
4. Add debugger-specific environments (breakpoint boxes, step illustrations, etc.)
5. Create initial content outline
6. Update request.json with correct configuration
7. Generate test PDF with minimal content
8. Iterate on template styling

---

*This is a placeholder Theory of Operations. It will be fully developed when the P2 Single-Step Debugger Manual enters active development.*
