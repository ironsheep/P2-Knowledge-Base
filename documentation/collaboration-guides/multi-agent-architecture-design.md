# Multi-Agent Architecture for Complex Document Production

**Context**: Discussion on 2025-08-25 about breaking complex document production tasks into manageable agent workflows to solve Claude's context depth limitations.

## Problem Statement

**Current Issue**: Complex document production exceeds single-agent context management:
- Multiple file trees (documentation, workspace, outbound)
- Complex state tracking (processed, escaped, deployed files)  
- Intricate workflows with precise dependencies
- Session boundary trauma losing critical context
- Constant regressions and re-learning overhead

**Root Cause**: Projects like Smart Pins PDF generation require orchestrating:
- Template architecture (foundation, content, presentation layers)
- Content processing (TOC removal, image paths, escaping)
- Deployment workflows (workspace → outbound → PDF generation)
- Cross-session state continuity

## Proposed Architecture

### Agent Types

**1. Agent-Template**
- **Scope**: Pure LaTeX/template work
- **Responsibilities**: 
  - Template syntax errors, styling, package conflicts
  - Template testing with sample content
  - Template deployment to outbound
- **Boundaries**: No markdown content changes
- **Example Tasks**: Fix `shobtabs` typo, update numbering logic, resolve package conflicts

**2. Agent-Markdown**  
- **Scope**: Pure content work
- **Responsibilities**:
  - Image path fixes, manual TOC removal, content structure
  - Template compatibility adjustments
  - **LaTeX escaping as final step** (natural workflow end)
- **Boundaries**: No template modifications
- **Example Tasks**: Fix asset paths, remove manual TOC, escape for PDF generation

**3. Agent-Coupled**
- **Scope**: Coordinated template + markdown changes
- **Responsibilities**:
  - Changes that must work together across both template and content
  - Full workflow testing (template + content + escaping)
- **Boundaries**: Both template and markdown modifications allowed
- **Example Tasks**: Numbering system changes, new content environments, page break logic

### Context Management Approaches

**Option A: Role-Based System Prompts**
- Predefined specialist contexts for each agent type
- Template agents know LaTeX, not content
- Content agents know P2 concepts, not LaTeX internals

**Option B: Context Injection**  
- Opus builds task-specific context packages
- Dynamic context based on current task needs
- Includes current file locations and specific objectives

**Option C: Hybrid (Likely Best)**
- Base roles (predefined domain expertise)
- Task context (dynamic from Opus)
- File locations (current project state)

### Decision Logic

**Opus Analyzes Request:**
```
"Fix section numbering" → Template + Markdown coupling → Agent-Coupled
"Fix image paths" → Content only → Agent-Markdown  
"Fix LaTeX syntax error" → Template only → Agent-Template
```

## Key Architecture Questions (Unresolved)

### Q1: Agent Context Initialization
**Question**: How does invoked agent receive initial context?
- Predefined roles + task description?
- Dynamic context injection from Opus?
- File location awareness?

**Considerations**: TodoMCP v7 provides independent context silos per agent

### Q2: Task Boundary Detection
**Question**: How does Opus determine agent type needed?
- Analysis of request scope?
- Predefined task patterns?
- Dynamic coupling detection?

### Q3: Success Criteria Definition
**Question**: How does agent know when task is complete?
- Predefined success patterns per agent type?
- Dynamic criteria from Opus?
- Self-validation capabilities?

## Complexity Analysis

### Document Creation vs Ingestion

**Ingestion Tasks (Lower Complexity)**:
- Linear workflows (extract → process → catalog)
- Clear input/output boundaries
- Self-contained operations
- Minimal cross-file dependencies

**Document Production Tasks (Higher Complexity)**:
- Multi-stage workflows (workspace → outbound → PDF)
- Complex state management across sessions
- Intricate file interdependencies
- Template-content coupling requirements
- Visual feedback loops requiring iteration

**Conclusion**: Document creation requires multi-agent architecture due to workflow complexity and state management needs.

## Implementation Readiness

**TodoMCP v7 Features**:
- Independent context silos per agent
- Agent-specific todo lists and context management
- Strong environment for agent deployment

**Next Steps**:
1. Define concrete agent role specifications
2. Create task classification decision tree for Opus
3. Develop agent success criteria frameworks
4. Test with Smart Pins PDF generation workflow

## Use Cases for Testing

**Smart Pins PDF Generation**:
- Template numbering fixes (Agent-Template or Agent-Coupled?)
- Image path corrections (Agent-Markdown)
- Escaping script issues (Agent-Markdown final step)
- Integration testing (Agent-Coupled)

**Future Applications**:
- PASM2 manual production
- Multi-part document workflows
- Template development and testing

---

*This document captures architectural thinking for future implementation. Actual agent deployment will require TodoMCP v7 and concrete role definitions.*