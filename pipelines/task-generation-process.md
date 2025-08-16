# Task Generation Process for P2 Knowledge Base

## Purpose
Convert sprint plans into executable tasks that drive implementation. These tasks provide complete context for independent execution.

## Core Principles
1. **Each task must be single-purpose** - If it does multiple things, split it
2. **Each task must be information-rich** - No questions during implementation

## The Process

### Phase 1: Review Sprint Planning
- Understand what deliverables were decided
- Note extraction sources and audit requirements  
- Consider document generation sequences
- Check reusable patterns (extractions, audits)

### Phase 2: Create Task List
- Convert each plan item to an actionable task
- Write paragraph-length descriptions with full context
- Include all source documents and extraction paths
- Identify dependencies between tasks
- Add standard completion tasks (git, documentation)

### Phase 3: Iterate with Stephen
- Present proposed task list
- Check for missing work
- Validate single-purpose focus
- Continue until no questions remain

### Phase 4: Optimize Sequence
**Key Goal: Minimize rework**
- Extract before audit
- Audit before generation
- Complete sources before synthesis
- Respect knowledge dependencies

### Phase 5: Persist to Todo-MCP
- Create all tasks in Todo-MCP with estimates
- Verify dependencies are captured
- Clear TodoWrite completely
- Ready for execution with time tracking

## Standard Sprint Completion Tasks
Always include at sprint end:
- Update PROJECT-MASTER.md
- Update README.md coverage metrics
- Document methodology improvements
- Create sprint summary document
- Prepare comprehensive git commit
- Archive completed todo-mcp tasks

## Task Description Requirements

### Each Task MUST Include:
**Paragraph-length rich description** containing:
- What exactly needs to be done
- Which documents to extract/create (with paths)
- Source documents to reference (PDF pages, sections)
- Extraction methodology to follow
- Audit criteria to apply
- Output format requirements
- Quality checks needed
- Cross-references to validate

### P2 Project Task Pattern
```
"Extract Terminal Window content from SPIN2 v51

Create focused extraction at sources/extractions/spin2-terminal-windows.md 
from sources/originals/spin2-text.txt. Extract ALL content related to 
DEBUG displays including SCOPE, PLOT, LOGIC, FFT, and terminal output. 
Include configuration constants (DEBUG_WINDOWS_OFF, DEBUG_BAUD, etc.) 
from around line 7400. Capture display commands from sections starting 
at line 6423. Include examples from throughout document. Follow focused 
extraction methodology in pipelines/focused-extraction-methodology.md. 
Note any screenshots referenced for later capture. Mark sections that 
need enrichment with practical examples. Cross-reference with existing 
spin2-v51-complete-extraction-audit.md to ensure nothing missed."
```

**This is the standard** - Rich, complete, no questions needed.

## P2-Specific Task Types

### Extraction Tasks
- Source document identification
- Content boundaries defined
- Output location specified
- Audit requirements noted

### Audit Tasks
- Completeness checks
- Consistency validation
- Gap identification
- Trust level assignment

### Generation Tasks
- Source extractions referenced
- Target audience identified
- Voice/style specified
- Examples included

### Documentation Tasks
- Coverage metrics update
- Pipeline queue maintenance
- Methodology capture
- Sprint summaries

## Clear Handoffs

### From Planning
- Deliverables defined
- Sources identified
- Methodologies chosen
- Quality gates set

### To Implementation
- Complete task list created
- All paths and sources included
- Dependencies mapped
- Ready for independent execution

### During Implementation
- MCP tasks tracked with start/pause/complete
- TodoWrite used for current task decomposition only
- Context backup preserves TodoWrite state
- Time automatically accumulated in Todo-MCP

## Quality Checks
Before finalizing:
- [ ] All planned deliverables covered
- [ ] Each task single-purpose
- [ ] Each task has rich paragraph description
- [ ] All source paths and references included
- [ ] No implementation questions remain
- [ ] Extraction → Audit → Generation sequence
- [ ] Standard completion tasks included
- [ ] Stephen approved

## Anti-Patterns
- **Multi-purpose tasks** - "Extract and audit" should be two tasks
- **Thin descriptions** - "Process SPIN2 doc" vs detailed extraction
- **Missing sources** - Always include page numbers, line numbers
- **Vague outputs** - Specify exact paths and formats
- **Missing methodology** - Reference which process to follow
- **No validation** - Always include quality checks
- **Skipping documentation** - Part of "done"

## Example Commands (When Applicable)

### For Git Operations
```bash
git add -A
git commit -m "Complete Terminal Window extraction and audit"
git tag v1.0.0-terminal-extraction
```

### For Todo-MCP
```bash
# Create sprint tasks
mcp todo create "Extract Terminal Window content" --estimate 60
mcp todo create "Audit Terminal Window extraction" --estimate 30

# Execute with time tracking
mcp todo start 1       # CRITICAL - starts time tracking
mcp todo pause 1       # If switching tasks
mcp todo start 1       # Resume work
mcp todo complete 1    # Captures actual time

# Sprint completion
mcp todo archive       # Preserves time metrics
```

### For Validation
```bash
# Test JSON schema
python validate_schema.py ai-reference/schemas/pasm2-schema.json

# Check markdown rendering
grip sources/extractions/terminal-windows.md
```