# Smart Startup System - Work Type Detection & Document Guidance

**Purpose**: Automatically detect current work focus and provide targeted reading lists with explicit paths
**Created**: 2025-08-25
**Status**: ACTIVE - Integrated with session start protocol

## 🎯 How It Works

During session startup, check context keys to determine current work focus, then read the appropriate document set for maximum efficiency.

## 🔍 Work Type Detection Patterns

### PDF Generation & Template Development
**Context Key Patterns**: `*pdf*`, `*template*`, `*layered*`, `*smart_pins_step*`, `*desilva_manual*`

**READ LIST**:
- `/documentation/pipelines/pdf-generation-format-guide.md` - Universal patterns
- `/documentation/pdf-forge-system/layered-template-architecture.md` - Current architecture
- Document-specific creation guide (auto-detect from context)

### Document Review & Iteration Cycles  
**Context Key Patterns**: `*review*`, `*feedback*`, `*iteration*`, `*validation*`, `*step*_complete`

**READ LIST**:
- `/documentation/pipelines/pdf-generation-format-guide.md` - Deployment standards
- `/documentation/pdf-forge-system/layered-template-architecture.md` - Template system
- Document-specific creation guide (for quality gates)
- `/pipelines/human-ai-collaboration-process.md` - Feedback interpretation
- `/TECHNICAL-CLIMBING-METHODOLOGY.md` - Iteration principles

### Content Ingestion & Source Studies
**Context Key Patterns**: `*extraction*`, `*ingestion*`, `*source*`, `*edge*`, `*silicon*`

**READ LIST**:
- `/pipelines/enhanced-source-code-ingestion-methodology.md` - Process methodology
- `/sources/INGESTED-SOURCES-CATALOG.md` - What we have
- `/pipelines/source-code-extraction-methodology.md` - Code extraction
- `/documentation/project-process/task-generation-process.md` - Task workflow

### Template/Style Sheet Development
**Context Key Patterns**: `*sty*`, `*latex*`, `*template*`, `*foundation*`, `*content*`, `*presentation*`

**READ LIST**:
- `/documentation/pdf-forge-system/layered-template-architecture.md` - Architecture principles
- `/documentation/pipelines/pdf-generation-format-guide.md` - Format standards
- `/pipelines/formatting-reference/` - Visual design guides
- Document-specific creation guide (target requirements)

### System Maintenance & Process Improvement
**Context Key Patterns**: `*process*`, `*methodology*`, `*workflow*`, `*documentation*`

**READ LIST**:
- `/TECHNICAL-CLIMBING-METHODOLOGY.md` - Core principles
- `/engineering/operations/README.md` - Current goals (was PROJECT-MASTER.md)
- `/pipelines/task-generation-process.md` - Process framework
- Active sprint documentation

## 🎯 Document-Specific Context Detection

### Smart Pins Reference Work
**Context Patterns**: `smart_pins*`, `*pins*`, `*reference*`
**Additional Reading**:
- `/documentation/manuals/smart-pins-reference/creation-guide.md` - Specific requirements
- `/sources/extractions/smart-pins-complete-extraction-audit/` - Source material

### PASM2 deSilva Manual Work  
**Context Patterns**: `desilva*`, `*pasm*`, `*tutorial*`
**Additional Reading**:
- `/documentation/manuals/p2-pasm-desilva-style/creation-guide.md` - Tutorial requirements
- `/sources/extractions/desilva-p1-tutorial/` - Reference material

## 📋 Session Startup Integration

### Enhanced Session Start Protocol:

```bash
# 1. Standard context resume
mcp__todo-mcp__context_resume

# 2. Smart work type detection
# Check recent context keys for patterns → determine work type

# 3. Auto-suggest reading list
# "Context shows Smart Pins review work → Recommend reading:"
# → List specific documents with full paths

# 4. Optional: Auto-read critical documents
# For highly focused work, automatically read 1-2 key documents
```

### Implementation in CLAUDE.md:
```markdown
### 3. 🔴 MANDATORY: Smart Document Reading
# Context analysis determines work type:
# - PDF_GENERATION_SMART_PINS → Read pdf-generation + smart-pins creation guide  
# - REVIEW_ITERATION_CYCLE → Read pdf-generation + collaboration-process + creation guide
# - CONTENT_INGESTION → Read extraction methodologies + source catalog
# - TEMPLATE_DEVELOPMENT → Read layered-architecture + format-guide
# - SYSTEM_MAINTENANCE → Read technical-climbing + project-master
```

## 🏆 Success Metrics

**Before Smart Startup**: 
- 10+ minutes orienting to work context
- Reading 3-5 long documents to find relevant sections
- Mistakes from incomplete context understanding

**After Smart Startup**:
- 2-3 minutes with targeted document list
- Reading 2-3 specific documents with full context
- Faster, more confident work execution

## 🔄 Continuous Improvement

### Feedback Loop:
1. **Track context patterns** that don't match current detection rules
2. **Add new work types** as project evolves  
3. **Refine reading lists** based on what's actually helpful
4. **Update paths** when documentation moves

### Pattern Evolution:
- New document types → New context patterns + reading lists
- New methodologies → Update relevant reading lists
- Process improvements → Reflect in startup guidance

## 📚 Master Document Path Reference

### Core Operational Guides:
- `/CLAUDE.md` - AI operational guide
- `/TECHNICAL-CLIMBING-METHODOLOGY.md` - Project principles  
- `/engineering/operations/README.md` - Goals and current state

### PDF Generation & Templates:
- `/documentation/pipelines/pdf-generation-format-guide.md` - Universal patterns
- `/documentation/pdf-forge-system/layered-template-architecture.md` - Template system
- `/documentation/pdf-templates-master/` - Master template files

### Content Creation & Ingestion:
- `/pipelines/enhanced-source-code-ingestion-methodology.md` - Ingestion process
- `/sources/INGESTED-SOURCES-CATALOG.md` - Available sources
- `/pipelines/source-code-extraction-methodology.md` - Code extraction

### Process & Methodology:
- `/pipelines/human-ai-collaboration-process.md` - Feedback cycles
- `/documentation/project-process/task-generation-process.md` - Task workflow
- `/pipelines/task-generation-process.md` - Process framework

### Document-Specific Guides:
- `/documentation/manuals/smart-pins-reference/creation-guide.md` - Smart Pins requirements
- `/documentation/manuals/p2-pasm-desilva-style/creation-guide.md` - deSilva tutorial requirements

---

**Integration Status**: Ready for CLAUDE.md session protocol integration
**Next Steps**: Test with actual context key patterns, refine detection rules