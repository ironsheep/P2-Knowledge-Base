# Smart Startup System - Work Type Detection & Document Guidance

**Purpose**: Authoritative session start guide - detect work focus and route to correct guidance documents.
**Last Updated**: 2025-12-06
**Status**: ACTIVE - Primary session start reference

## How It Works

1. Run `mcp__todo-mcp__context_resume` to see current state
2. Match context patterns below to determine work type
3. Read the listed Quick Guide to get into frame of mind
4. Use filter tag with Todo MCP for focused task list

---

## Work Type Detection & Routing

### 1. Document Ingestion
**Context Patterns**: `*extraction*`, `*ingestion*`, `*source*`, `*edge*`, `*silicon*`

**Quick Guide**: `/engineering/ingestion/work-modes/document-ingestion-focused.md`
**Filter Tag**: `document_ingestion`

**Additional Resources**:
- `/engineering/ingestion/work-modes/image-extraction-focused.md` - Image extraction sub-process
- `/engineering/ingestion/methodology/enhanced-source-code-ingestion-methodology.md` - Full methodology

---

### 2. YAML Knowledge Base
**Context Patterns**: `*yaml*`, `*crossref*`, `*index*`, `*dod*`, `*validation*`

**Quick Guide**: `/engineering/procedures/yaml-workflow-quick-guide.md`
**Filter Tag**: `yaml_knowledge_base`

**Additional Resources**:
- CLAUDE.md → DOD v3.0 Procedure section - Complete workflow
- `/engineering/tools/validate-crossref-keys.py` - Cross-reference validation
- `/engineering/tools/generate-p2kb-index.py` - Index regeneration

---

### 3. PDF Document Production
**Context Patterns**: `*pdf*`, `*template*`, `*desilva*`, `*smart_pins*`, `*manual*`

**READ FIRST**: `/engineering/document-production/PDF-PRODUCTION-ARCHITECTURE.md`
- Three-folder rule (manuals → workspace → outbound)
- Where edits happen (content in manuals/, templates in workspace/)
- Two operational modes (interactive testing vs production)

**Then read document-specific Quick Guide**:
- DeSilva Manual: `/engineering/document-production/work-modes/desilva-visual-refinement.md`
- Smart Pins: `/engineering/document-production/work-modes/smart-pins-visual-refinement.md`
- PASM2 Manual: `/engineering/document-production/work-modes/desilva-visual-refinement.md`
- General PDF: `/engineering/pdf-forge/work-modes/production-pdf-generation.md`
- Interactive Testing: `/engineering/pdf-forge/work-modes/automated-pdf-testing.md`

**Filter Tags**: `desilva_visual`, `smart_pins_visual`, `pdf_production`, `pasm2_manual`

**Rules & References**:
- `/engineering/pdf-forge/PDF-CLAUDE-RULES.md` - Critical rules (edit locations, file naming)
- `/workspace/[doc]/README.md` - Document-specific workspace instructions

---

### 4. Engineering Tooling
**Context Patterns**: `*tool*`, `*script*`, `*compiler*`, `*pnut*`

**Quick Guide**: Standard development practices (no specific guide needed)
**Filter Tag**: `engineering_tooling`

**Additional Resources**:
- `/engineering/tools/compiler/pnut_ts-usage-guide.md` - P2 compiler usage
- `/engineering/tools/compiler/claude-p2-development-environment.md` - Development environment

---

### 5. Operational Infrastructure
**Context Patterns**: `*sprint*`, `*process*`, `*methodology*`, `*workflow*`, `*documentation*`

**Quick Guide**: `/engineering/operations/project-guidance/work-mode-lifecycle.md`
**Filter Tag**: `operational`

**Additional Resources**:
- `/engineering/operations/project-guidance/sprint-lifecycle-methodology.md` - Complete sprint process
- `/engineering/operations/project-guidance/human-ai-collaboration-process.md` - Feedback cycles
- `/engineering/operations/PROCESS-GUIDANCE-ARCHITECTURE.md` - Map of all guidance docs

---

## Document-Specific Context Detection

### PASM2 Assembly Manual Work
**Context Patterns**: `*pasm2*`, `*assembly*`, `*instruction*`
**Quick Guide**: `/engineering/document-production/work-modes/desilva-visual-refinement.md`
**Creation Guide**: `/engineering/document-production/manuals/p2-pasm-desilva-style/creation-guide.md`

### Smart Pins Reference Work
**Context Patterns**: `smart_pins*`, `*pins*`, `*reference*`
**Quick Guide**: `/engineering/document-production/work-modes/smart-pins-visual-refinement.md`

---

## Session Startup Protocol

```bash
# 1. ALWAYS FIRST - Restore context
mcp__todo-mcp__context_resume

# 2. Analyze context patterns → Determine work type (use sections above)

# 3. Read Quick Guide for identified work type
# Example: Read(engineering/document-production/work-modes/desilva-visual-refinement.md)

# 4. Use filter tag for focused task list
mcp__todo-mcp__todo_next tags:["desilva_visual"]

# 5. Begin work with proper context loaded
```

---

## Success Metrics

**Before Smart Startup**:
- 10+ minutes orienting to work context
- Reading multiple long documents to find relevant sections
- Mistakes from incomplete context understanding

**After Smart Startup**:
- 2-3 minutes with targeted document routing
- Read only the Quick Guide for current work type
- Faster, more confident work execution

---

## Master Document Path Reference

### Core Operational:
- `/CLAUDE.md` - AI operational guide (quality rules, sacred rules)
- `/engineering/operations/PROCESS-GUIDANCE-ARCHITECTURE.md` - Map of all guidance docs
- `/engineering/operations/README.md` - Operational dashboard

### PDF Generation:
- `/engineering/pdf-forge/PDF-CLAUDE-RULES.md` - Claude-specific rules
- `/engineering/document-production/methodology/pdf-generation-format-guide.md` - Format standards
- `/engineering/pdf-forge/guides/pdf-forge-system/layered-template-architecture.md` - Template system
- `/engineering/document-production/shared-assets/templates/pdf-templates-master/` - Master templates

### Content Ingestion:
- `/engineering/ingestion/methodology/enhanced-source-code-ingestion-methodology.md` - Ingestion process
- `/engineering/ingestion/methodology/source-code-extraction-methodology.md` - Code extraction

### Process & Methodology:
- `/engineering/operations/project-guidance/human-ai-collaboration-process.md` - Feedback cycles
- `/engineering/operations/project-guidance/task-generation-process.md` - Task workflow
- `/engineering/operations/project-guidance/methodology/TECHNICAL-CLIMBING-METHODOLOGY.md` - Project principles

### Lessons Learned:
- `/engineering/operations/lessons-learned/INDEX.md` - Rule → incident mapping

---

## Relationship to Other Documents

- **CLAUDE.md**: Contains core quality rules that apply to ALL work types. This document routes to work-type-specific guidance.
- **PROCESS-GUIDANCE-ARCHITECTURE.md**: Comprehensive map of all guidance documents. This document provides quick routing.
- **Quick Guides**: Entry points for each work type. This document tells you which one to read.

---

*This is the authoritative session start reference. Run context_resume, match patterns, read the right Quick Guide.*
