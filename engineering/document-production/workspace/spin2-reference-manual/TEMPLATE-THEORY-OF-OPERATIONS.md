# Spin2 Reference Manual - Template Theory of Operations

**Document:** Spin2-Reference-Manual.md (TBD)
**Template Prefix:** `p2kb-spin2-ref-*` (to be established)
**Version:** 0.1 (Placeholder)
**Last Updated:** 2025-12-03
**Status:** PLANNED - Early Stage (No content or custom templates yet)

## Overview

This workspace is in **early planning stage**. No custom templates or document content have been created yet. Only the shared `p2kb-foundation.sty` is present.

## Current Template Stack Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      NOT YET CREATED                         │
│        (p2kb-spin2-ref.latex will go here)                   │
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
├── p2kb-spin2-ref.latex           # Master Pandoc template
├── p2kb-spin2-ref-foundation.sty  # Document-specific foundation
└── p2kb-spin2-ref-content.sty     # Content layer (syntax, examples)
```

### Lua Filters Potentially Needed

```
filters/
├── p2kb-spin2-ref-div-blocks.lua  # Code block styling
├── p2kb-spin2-ref-semantic.lua    # Semantic environments
└── p2kb-spin2-ref-syntax.lua      # Syntax diagram processing (TBD)
```

### Configuration Files Needed

```
request.json                       # PDF Forge configuration
request-requirements.json          # Mandatory pandoc arguments
```

## Design Decisions Pending

### 1. Reference Style
- **Option A:** Formal language specification (technical, precise)
- **Option B:** Practical reference guide (approachable, examples-first)
- **Recommendation:** Likely Option B to match other P2KB manuals

### 2. Template Starting Point
| Template Source | Pros | Cons |
|-----------------|------|------|
| `p2kb-sp-*` | Proven, technical | Tutorial-focused |
| `p2kb-desilva-*` | Approachable, pedagogical | May need adaptation |
| `p2kb-pasm2-*` | Reference-focused | Assembly-centric |
| New template | Clean slate | More work |

**Recommended:** Start from `p2kb-pasm2-*` templates (Assembly Language Reference Manual) since both are language reference manuals and should share visual style.

### 3. Coordination with PASM2 Manual
Both manuals document P2 programming languages. Consider:
- Shared color palette for code blocks
- Consistent cross-referencing style
- Similar section organization for familiar navigation
- Distinct visual identity (Spin2 = high-level, PASM2 = low-level)

### 4. Code Block System
Likely need **3-4 color system**:

| Block Type | Suggested Color | Purpose |
|------------|-----------------|---------|
| Spin2 | Green | Primary language examples |
| PASM2 | Cream/Yellow | Inline assembly examples |
| Mixed | Gradient/Split | Spin2 with inline PASM2 |
| Output | Gray | Program output |

### 5. Top-Level Division
| Option | Use Case |
|--------|----------|
| `--top-level-division=part` | If organizing by language area (Types, Operators, Control Flow, Objects, etc.) |
| `--top-level-division=chapter` | If simpler flat organization |

**Recommendation:** Use `part` for major language divisions, similar to PASM2 Reference Manual.

## Content Characteristics (When Developed)

### Core Sections Expected
1. **Language Basics** - Types, variables, operators
2. **Control Structures** - If, case, repeat
3. **Methods** - PUB, PRI, parameters, returns
4. **Objects** - OBJ, instantiation, method calls
5. **Data Handling** - DAT blocks, arrays, strings
6. **Inline PASM2** - ORG blocks, register access
7. **Built-in Functions** - Math, string, I/O functions
8. **Standard Library** - Common objects and patterns

### Special Features Needed
- **Syntax Diagrams** - Railroad diagrams for grammar
- **Type System Documentation** - BYTE, WORD, LONG semantics
- **Object Model Explanation** - How Spin2 objects work
- **Inline Assembly Guide** - When/how to use PASM2 in Spin2

## Naming Convention Compliance

### When Templates Are Created

All files should follow: `p2kb-{docprefix}-{purpose}.{ext}`

| File | Pattern Compliance |
|------|-------------------|
| `p2kb-spin2-ref.latex` | ✅ Will be correct |
| `p2kb-spin2-ref-foundation.sty` | ✅ Will be correct |
| `p2kb-spin2-ref-content.sty` | ✅ Will be correct |
| `p2kb-spin2-ref-div-blocks.lua` | ✅ Will be correct |

**Note:** Using `spin2-ref` prefix (not just `spin2`) to distinguish from any Spin2 tutorial documents that might be created later.

## Related Documents

| Document | Relationship |
|----------|--------------|
| **PASM2 Assembly Language Reference** | Coordinate visual style, cross-reference inline assembly |
| **PASM2 DeSilva Style Manual** | Example patterns, pedagogical approach |
| **Smart Pins Tutorial** | May share Spin2 code block styling |

## Next Steps to Begin Development

1. **Confirm reference style** - Ask user: formal specification or practical guide?
2. **Copy template base** - Start from `p2kb-pasm2-*` templates
3. **Rename with prefix** - `p2kb-spin2-ref-*`
4. **Adapt color palette** - Spin2-appropriate colors
5. **Create content outline** - Define chapter/section structure
6. **Build incrementally** - Start with one section, iterate

## When Working on This Document

### Before Starting Development:
1. Confirm user wants to prioritize this document
2. Review PASM2 Reference Manual for consistency patterns
3. Check `/engineering/knowledge-base/P2/language/spin2/` for YAML sources
4. Decide on reference style with user input

### Initial Development Steps:
1. Copy template files from chosen source
2. Rename with `p2kb-spin2-ref-*` prefix
3. Create initial content outline
4. Update request.json with correct configuration
5. Generate test PDF with minimal content
6. Iterate on template styling

---

*This is a placeholder Theory of Operations. It will be fully developed when the Spin2 Reference Manual enters active development.*
