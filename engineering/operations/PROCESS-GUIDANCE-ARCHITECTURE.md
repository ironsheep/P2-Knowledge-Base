# Process Guidance Architecture

**Purpose**: Central map of all process guidance documents - what exists, why, and when to use each.

**Last Updated**: 2025-12-06

---

## The Two-Tier Guidance System

| Tier | Purpose | Token Cost | When Used |
|------|---------|------------|-----------|
| **Quick Guides (Work Modes)** | Get into frame of mind, key steps, directory structure | Low (~200-400 lines) | Session start, mode entry |
| **Full Methodology Docs** | Complete process, all phases, quality gates, examples | High (~500-1000+ lines) | During execution, when questions arise |

**Design Principle**: Quick guides load at session start (minimal context). Full methodology docs are read on-demand during actual work.

---

## Work Types & Their Guidance

### 1. Document Ingestion

**Description**: Extract and normalize source material from trusted sources (Parallax docs, Chip's posts, datasheets) into knowledge base.

| Tier | Document | Location | Lines | Purpose |
|------|----------|----------|-------|---------|
| Quick | document-ingestion-focused.md | `engineering/ingestion/work-modes/` | 631 | Frame of mind, task generation, phase overview |
| Quick | image-extraction-focused.md | `engineering/ingestion/work-modes/` | 698 | Image extraction sub-process |
| Quick | central-repository-build.md | `engineering/ingestion/work-modes/` | 165 | Central repo build mode |
| Quick | download-on-demand-api.md | `engineering/ingestion/work-modes/` | 251 | Download API mode |
| Full | source-ingestion-methodology.md | `engineering/ingestion/methodology/` | 314 | Complete ingestion theory |
| Full | enhanced-source-code-ingestion-methodology.md | `engineering/ingestion/methodology/` | 324 | Code extraction details |
| Full | source-code-extraction-methodology.md | `engineering/ingestion/methodology/` | 701 | Source code extraction |
| Full | image-extraction-methodology.md | `engineering/ingestion/methodology/` | 347 | Image extraction complete process |
| Full | focused-extraction-methodology.md | `engineering/ingestion/methodology/` | 64 | Targeted extraction approach |

**Entry Point**: `engineering/ingestion/work-modes/document-ingestion-focused.md`
**Filter Tag**: `document_ingestion`

---

### 2. YAML Knowledge Base

**Description**: Create and maintain structured YAML files for AI consumption. Includes cross-reference validation, index generation, and DOD compliance.

| Tier | Document | Location | Lines | Purpose |
|------|----------|----------|-------|---------|
| Quick | yaml-workflow-quick-guide.md | `engineering/procedures/` | 103 | Complete DOD v3.0 workflow |
| Tool | validate-crossref-keys.py | `engineering/tools/` | — | Cross-reference validation |
| Tool | generate-p2kb-index.py | `engineering/tools/` | — | Index regeneration |
| Tool | validate-dod-release.py | `engineering/tools/` | — | Pre-release validation |

**Entry Point**: `engineering/procedures/yaml-workflow-quick-guide.md`
**Filter Tag**: `yaml_knowledge_base`

---

### 3. PDF Document Production

**Description**: Create human-readable documentation (manuals, tutorials, guides) via PDF Forge system.

| Tier | Document | Location | Lines | Purpose |
|------|----------|----------|-------|---------|
| **Arch** | **PDF-PRODUCTION-ARCHITECTURE.md** | `engineering/document-production/` | ~200 | **READ FIRST** - Central architecture, 3-folder rule, new doc checklist |
| Quick | desilva-visual-refinement.md | `engineering/document-production/work-modes/` | 225 | DeSilva manual iteration |
| Quick | smart-pins-visual-refinement.md | `engineering/document-production/work-modes/` | 79 | Smart Pins manual iteration |
| Quick | production-pdf-generation.md | `engineering/pdf-forge/work-modes/` | 220 | Production PDF workflow |
| Quick | automated-pdf-testing.md | `engineering/pdf-forge/work-modes/` | 449 | Interactive testing (Claude-driven) |
| Full | pdf-generation-format-guide.md | `engineering/document-production/methodology/` | 1044 | Format standards |
| Full | document-generation-process.md | `engineering/document-production/methodology/` | 672 | Complete checklist |
| Ref | PDF-CLAUDE-RULES.md | `engineering/pdf-forge/` | 90 | Claude rules (edit locations, naming) |
| Ref | PRODUCTION-REQUEST-FORMAT.md | `engineering/pdf-forge/` | — | Request.json format |

**Entry Point**: `engineering/document-production/PDF-PRODUCTION-ARCHITECTURE.md` → then document-specific Quick Guide

**Filter Tags**: `desilva_visual`, `smart_pins_visual`, `pdf_production`, `pasm2_manual`

---

### 4. Engineering Tooling

**Description**: Scripts, validators, and automation tools supporting the knowledge base.

| Tier | Document | Location | Lines | Purpose |
|------|----------|----------|-------|---------|
| Quick | *Light process - no guide needed* | — | — | Standard development practices |
| Ref | pnut_ts-usage-guide.md | `engineering/tools/compiler/` | ~200 | P2 compiler usage |
| Ref | claude-p2-development-environment.md | `engineering/tools/compiler/` | ~150 | Development environment |

**Entry Point**: Individual tool documentation
**Filter Tag**: `engineering_tooling`

---

### 5. Operational Infrastructure

**Description**: Sprint methodology, project management, standards, and meta-processes.

| Tier | Document | Location | Lines | Purpose |
|------|----------|----------|-------|---------|
| Quick | work-mode-lifecycle.md | `engineering/operations/project-guidance/` | 326 | Work mode transitions |
| Quick | STARTUP-BY-WORK-TYPE.md | `engineering/operations/claude-guidance/` | 167 | Session start detection (authoritative) |
| Full | sprint-lifecycle-methodology.md | `engineering/operations/project-guidance/` | 209 | Complete sprint process |
| Full | sprint-planning-methodology.md | `engineering/operations/project-guidance/` | 197 | Planning phase |
| Full | sprint-execution-methodology.md | `engineering/operations/project-guidance/` | 264 | Execution phase |
| Full | sprint-execution-process.md | `engineering/operations/project-guidance/` | 378 | Execution details |
| Full | task-generation-process.md | `engineering/operations/project-guidance/` | 442 | Task generation |
| Full | human-ai-collaboration-process.md | `engineering/operations/project-guidance/` | 192 | Feedback cycles |
| Full | claude-human-optimization-guide.md | `engineering/operations/claude-guidance/` | 231 | Session management |
| Full | claude-model-selection-strategy.md | `engineering/pipelines/` | 214 | Model switching |

**Entry Point**: `engineering/operations/project-guidance/work-mode-lifecycle.md`
**Filter Tag**: `operational`

---

## Lessons Learned System

**Purpose**: Preserve "why" knowledge from past incidents for on-demand retrieval.

| Document | Location | Incident | Rule Created |
|----------|----------|----------|--------------|
| INDEX.md | `engineering/operations/lessons-learned/` | — | Rule→incident mapping |
| file-operations-regression-lesson.md | `engineering/operations/lessons-learned/` | Lost 3300 lines | Non-destructive file ops |
| pdf-generation-changelog.md | `engineering/operations/lessons-learned/` | Template evolution | PDF process rules |

**When to Read**: When near a rule boundary or questioning why a rule exists.

**Entry Point**: `engineering/operations/lessons-learned/INDEX.md`

---

## Quick Guide vs Full Methodology: Decision Tree

```
Starting work on a task?
│
├─ First time in this work mode today?
│  └─ YES → Read Quick Guide (frame of mind, directory structure)
│
├─ Hit a question about process steps?
│  └─ YES → Read Full Methodology (complete details)
│
├─ Questioning why a rule exists?
│  └─ YES → Read Lessons Learned (incident context)
│
└─ Familiar with work mode, just executing?
   └─ YES → No reading needed, use filter tags for task focus
```

---

## CLAUDE.md Integration

**CLAUDE.md should contain**:
1. Pointer to this document for work type routing
2. Core quality rules (apply to ALL work types)
3. Quick reference for session start protocol
4. Sacred rules with "why" pointers to lessons-learned

**CLAUDE.md should NOT contain**:
1. Full procedures (point to methodology docs instead)
2. Detailed explanations of why rules exist (point to lessons-learned)
3. Work-type-specific guidance (point to quick guides)

---

## Identified Gaps

### Critical Gaps - FILLED

| Gap | Status | Document Created |
|-----|--------|------------------|
| YAML workflow quick guide | **FILLED** | `engineering/procedures/yaml-workflow-quick-guide.md` |
| PDF rules quick guide | **FILLED** | `engineering/pdf-forge/PDF-CLAUDE-RULES.md` |
| Lessons-learned index | **FILLED** | `engineering/operations/lessons-learned/INDEX.md` |

### Remaining Gaps

| Gap | Priority | Action Required | Impact |
|-----|----------|-----------------|--------|
| Environment protocols doc | Medium | Extract container/host-native rules from CLAUDE.md | Currently ~100 lines in CLAUDE.md |

### Observations from Inventory

**Ingestion work modes are heavy** (631-698 lines each):
- `document-ingestion-focused.md` is 631 lines - more like a full methodology than a quick guide
- `image-extraction-focused.md` is 698 lines - same issue
- These may need splitting into quick guide + full methodology

**PDF work modes are appropriately sized** (79-449 lines):
- Most are under 250 lines - good quick guide size
- `automated-pdf-testing.md` at 449 lines is borderline

**Operational guides are well-structured**:
- Clear quick vs full separation
- Reasonable sizes

### CLAUDE.md Refactor Status (2025-12-06)

**Completed**: CLAUDE.md reduced from 1,026 → 252 lines (75% reduction)

| Content | Status | Location |
|---------|--------|----------|
| YAML DOD Procedure | ✅ Externalized | `engineering/procedures/yaml-workflow-quick-guide.md` |
| PDF Generation Rules | ✅ Externalized | `engineering/pdf-forge/PDF-CLAUDE-RULES.md` |
| Environment Protocols | ✅ Summarized | CLAUDE.md lines 144-159 (compact version) |
| Model Switching | ✅ Pointer only | Points to `claude-model-selection-strategy.md` |
| Session Management | ✅ Pointer only | Points to `claude-human-optimization-guide.md` |
| Todo MCP | ✅ Quick ref only | CLAUDE.md lines 163-180, full docs in `.todo-mcp/mastery/` |

**CLAUDE.md now contains**: Essential guardrails, sacred rules with incident context, pointers to detailed guides

---

## Maintenance

**When to update this document**:
- New work mode guide created
- Methodology document added or moved
- Lessons learned documented
- CLAUDE.md refactored

**Owner**: Updated during operational work sessions

---

*This document is the "map of the map" - the central reference for understanding the process guidance ecosystem.*
