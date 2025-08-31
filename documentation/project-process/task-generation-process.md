# Task Generation Process

**Version**: 1.0
**Created**: 2025-08-20
**Status**: Living Document

---

## Overview

Task generation transforms detailed sprint plans into executable, atomic work units. Each task must be completely self-contained, requiring zero external context for successful execution. This exhaustive approach ensures quality and prepares for future multi-agent workflows.

---

## Core Principles

### 1. Exhaustive Self-Containment
**Every task must include ALL context needed for execution**

Each task should be writable as if for an agent who has:
- Never seen the codebase
- No knowledge of the project
- No access to other tasks
- Only the task description to work from

**Example Task Format**:
```
Review the PASM2 instruction narratives in `/sources/extractions/pasm2-manual-docx-extraction.md`, 
identify gaps in completeness against the 400+ instruction set, and update the master instruction 
table at `/sources/pasm2-master/instruction-table.md` with findings. For each instruction, verify 
presence of: meta group classification, clocking information, flag modification capabilities, 
and operational description. Mark missing aspects as 'MISSING: [aspect]'. Cross-reference with 
questions logged in `/sources/extractions/qa-spreadsheet-extraction.md` lines 45-89. 
Deliverable: Updated instruction table with gap annotations and source citations.
```

### 2. Atomic Work Units
**No task should reference or depend on another task's description**

- Each task = complete beginning-to-end workflow
- No "continue from previous task" references
- No shared state between tasks
- Complete even if it's the only task executed

### 3. Model Purity
**Each task uses exactly ONE model**

- Never mix Opus and Sonnet in single task
- If work needs both models, create two tasks
- Explicitly state model requirement if non-default
- Group tasks by model to minimize switches

### 4. Prevention Over Correction
**Dependencies are recovery mechanisms, not design tools**

MCP's dependency and sequencing features are for:
- Late-discovered issues
- Planning oversights
- Unexpected complications

NOT for:
- Primary task organization
- Known relationships
- Planned workflows

Build tasks that need no dependencies through careful ordering.

---

## Task Generation Workflow

### Step 1: Review Sprint Plan

Extract from plan:
- All sprint items and deliverables
- Advisory guidance on ordering
- Model recommendations
- File locations and paths
- Success criteria

### Step 2: Decompose Items into Tasks

For each sprint item:
1. **Identify atomic work units**
   - What's the smallest complete piece?
   - Can this run independently?
   - Is the deliverable clear?

2. **Enrich with full context**
   - Source file paths (complete)
   - Destination locations (exact)
   - Validation criteria (specific)
   - Format requirements (detailed)
   - Cross-references (with line numbers if applicable)

3. **Assign model requirement**
   - Default: Current model (usually Sonnet)
   - Specify if Opus needed
   - Never mix models

### Step 3: Order for Zero Rework

**Ordering Considerations**:
1. **Foundation first** - Build what others need
2. **Extraction before analysis** - Get data, then process
3. **Creation before validation** - Make it, then check it
4. **Independent before dependent** - Parallel-capable first

**Model Batching**:
- Group all Sonnet tasks together
- Group all Opus tasks together
- Minimize model switches
- Consider human availability for switches

### Step 4: Write Paragraph Tasks

**Required Elements per Task**:
- **Context**: What situation are we in?
- **Sources**: What files/data to read? (full paths)
- **Actions**: What specific work to do?
- **Validation**: How to verify correctness?
- **Deliverables**: What to create/update? (full paths)
- **Success Criteria**: What defines completion?

**Quality Checklist**:
- [ ] Could an agent with no context succeed?
- [ ] Are all file paths complete and exact?
- [ ] Is the deliverable unambiguous?
- [ ] Is validation criteria included?
- [ ] Is it truly atomic?

### Step 5: Stage and Review

**Option A: TodoWrite Staging**
```javascript
// Stage in TodoWrite for easy reordering
TodoWrite: [
  {content: "Task 1 full description...", status: "pending"},
  {content: "Task 2 full description...", status: "pending"},
  // Reorder here before sending to MCP
]
```

**Option B: Direct MCP Creation**
```bash
# Create directly in MCP with priorities
mcp__todo-mcp__todo_create content:"[full task]" priority:"high"
# Use bulk operations to reorder if needed
```

### Step 6: Add Estimates

**CRITICAL: Every task needs an estimate in minutes**
- Don't overthink accuracy - make your best guess
- Enables time tracking and sprint metrics
- Required by MCP todo system
- Helps gauge sprint size (<24 hours total recommended)

### Step 7: Model Tagging for Opportunistic Execution

**Tag each task with required model**:
```
#sonnet - Default model tasks
#opus - Creative/synthesis tasks
#either - Model-agnostic tasks
```

**Enables**:
- Opportunistic execution when model switches
- Filtering by current model availability
- Minimal switch requests to human

### Step 8: Final Organization

**Apply MCP Priorities**:
- `critical` - Blocks everything
- `high` - Sprint core objectives
- `medium` - Important but not blocking
- `low` - Nice to have
- `backlog` - Future consideration

**Tag Strategy** (Advisory from plan):
- By sprint item (AD-007, AD-001, etc.)
- By model (opus-required, sonnet-batch)
- By type (extraction, analysis, documentation)

**Sequence Within Priority** (if needed):
- Use for discovered ordering needs
- Not for primary organization
- Document why sequencing was needed

### Step 9: CRITICAL - Rework Analysis Pass

**Purpose**: Prevent tasks from requiring rework due to execution order conflicts

**Process**:
1. **Trace execution flow**: "If I do these tasks in this exact order, what happens?"
2. **Identify conflicts**: Look for tasks where later discoveries might invalidate earlier work
3. **Check methodology dependencies**: Does one task establish approaches that another should use?
4. **Fix ordering issues**:
   - **Preferred**: Adjust task priorities to get natural ordering
   - **Fallback**: Use sequencing within same priority
   - **Last resort**: Add dependencies across priorities

**Common Conflict Patterns**:
- **Audit before execution**: Methodology audits should precede work using that methodology
- **Standards before application**: Establishing approaches before using them
- **Foundation before building**: Base knowledge before derived knowledge
- **Discovery before utilization**: Finding information before applying it

**Example from Sprint 005**:
- **Problem**: Code extraction (#930) before methodology audit (#935)
- **Risk**: Audit might reveal better extraction approaches, causing rework
- **Solution**: Moved audit to same priority, natural ordering resolved conflict

**Remember**: This analysis often reveals that tasks are mis-prioritized, not just mis-ordered

---

## Task Examples by Type

### Extraction Task
```
Extract all code examples from the Spin2 v51 audit document at 
`/sources/extractions/spin2-v51-complete-extraction-audit.md`. For each example found between 
lines 1250-8900, capture: (1) the complete code block, (2) the section heading it appears under, 
(3) any descriptive text within 5 lines before/after, (4) the line number reference. Organize 
into folders at `/sources/extractions/spin2-v51-complete-extraction-audit/code-examples/` 
using pattern `[section-name]/example-[number].spin2`. Create metadata file for each with 
source location and description. Deliverable: Organized code examples with metadata files.
```

### Analysis Task (Opus)
```
[Model: Opus 4.1] Analyze the teaching voice in the DeSilva P1 Assembly Tutorial text at 
`/sources/extractions/desilva-p1-tutorial/extracted-text.md`. Identify: (1) characteristic 
phrases and terminology, (2) explanation patterns and progression, (3) use of examples vs 
theory ratio, (4) assumed reader knowledge level, (5) encouragement/motivation techniques. 
Compare against modern pedagogical best practices. Document findings in 
`/sources/extractions/desilva-p1-tutorial/voice-analysis.md` with sections for each aspect. 
Include specific quotes demonstrating each characteristic. Deliverable: Comprehensive voice 
analysis document suitable for replication.
```

### Creation Task
```
Create the PASM2 master instruction table at `/sources/pasm2-master/instruction-table.md`. 
Initialize with all 400+ instructions from the comprehensive list at 
`/sources/extractions/csv-pasm2-instructions-v2.md`. For each instruction, create columns for: 
Instruction Name, Opcode, Meta Group, Clock Cycles, Flag Effects (C/Z/both/none), Category, 
Description, Missing Info. Pre-populate known values from CSV extraction. Mark all unknown 
fields as "MISSING: [field]". Format as markdown table with consistent column widths. 
Include header explaining purpose and update methodology. Deliverable: Initial master 
instruction table with gap tracking.
```

---

## Future-Proofing for v0.7+ Multi-Agent Work

### Why This Matters Now

Our exhaustive task approach prepares for Todo MCP v0.7's multi-agent capabilities:

1. **Agent-Ready Tasks**
   - Zero shared context requirement
   - Complete execution parameters
   - Clear success criteria
   - No human interpretation needed

2. **Parallel Execution**
   - Truly atomic tasks can run simultaneously
   - No hidden dependencies
   - Clear deliverable boundaries
   - Merge-friendly outputs

3. **Sub-Agent Delegation**
   - Tasks become agent directives
   - Self-contained work packages
   - Model requirements pre-specified
   - Validation included

### Preparing Today for Tomorrow

**Current Benefit**: Better single-agent execution
**Future Benefit**: Drop-in multi-agent scaling

When v0.7 arrives, our tasks will already be:
- Distributable across agents
- Parallelizable by design
- Integration-tested through practice
- Quality-assured through exhaustive detail

### The Vision

```
Main Agent (Orchestrator)
├── Extraction Agent (Sonnet) - Handles all extraction tasks in parallel
├── Analysis Agent (Opus) - Processes all creative work
├── Validation Agent (Sonnet) - Runs all quality checks
└── Integration Agent (Sonnet) - Merges deliverables
```

Our task generation discipline today enables this tomorrow.

---

## Common Patterns and Anti-Patterns

### ✅ Good Patterns

**Complete Context**:
```
"Using the instruction list at `/path/to/list.md` (lines 50-450) and the 
completion matrix at `/path/to/matrix.md`, identify..."
```

**Clear Deliverable**:
```
"Deliverable: Updated `/sources/pasm2-master/instruction-table.md` with 
all gaps marked as 'MISSING: [aspect]' and source citations added."
```

**Validation Included**:
```
"Verify completeness by checking that all 400+ instructions from the 
master list appear in the table with at least partial data."
```

### ❌ Anti-Patterns

**Vague References**:
```
"Continue from the previous extraction task..."
"Using the data we found earlier..."
"Update the relevant files..."
```

**Mixed Models**:
```
"Extract the data (Sonnet) then analyze the voice patterns (Opus)..."
```

**Hidden Dependencies**:
```
"After the matrix is ready..." (makes assumption)
"Once we have the extraction..." (creates dependency)
```

---

## Integration with Other Processes

### From Sprint Planning
- Receives detailed plan with items
- Uses advisory guidance
- Inherits model strategy
- Applies suggested organization

### To Sprint Execution
- Provides ordered task list
- Specifies model requirements
- Enables checkpoint/commit workflow
- Defines success criteria

### With MCP Todo
- Creates persistent task records
- Enables progress tracking
- Supports priority management
- Allows dynamic reordering

---

## Metrics for Success

### Task Generation Quality
- Zero tasks need clarification during execution
- No rework due to ordering issues
- Model switches minimized
- All deliverables clearly defined

### Execution Efficiency
- Tasks executable without questions
- Parallel work possible where designed
- Dependencies only for true surprises
- Smooth progression through sprint

---

## Quick Reference Checklist

Before finalizing tasks, verify:

- [ ] Every task has complete file paths
- [ ] No task references another task
- [ ] Each task uses single model
- [ ] Ordering prevents rework
- [ ] Model switches minimized
- [ ] Deliverables are unambiguous
- [ ] Validation criteria included
- [ ] Could an agent execute this alone?
- [ ] Priority levels assigned (critical/high/medium/low/backlog)
- [ ] Advisory tags applied where helpful
- [ ] **CRITICAL: Rework analysis completed**
- [ ] Execution order conflicts identified and resolved
- [ ] Task priorities adjusted if needed for optimal ordering

---

## Task Generation Gate

**Before execution can begin**:

### Final Quality Checks
1. **Rework Analysis Complete**: Systematic review for execution order conflicts
2. **Model Strategy Optimal**: Minimize switches, batch work appropriately
3. **Dependencies Justified**: Any dependencies are truly necessary, not planning failures
4. **Estimates Reasonable**: Total time within sprint guidelines (<24 hours)

### Iteration with Human
1. Present complete task list with priorities and estimates
2. Human reviews for:
   - Correct prioritization  
   - Reasonable estimates
   - Proper ordering (no rework conflicts)
   - Model assignments
3. Iterate until:
   - Both parties have no questions
   - Both agree it's the right set of tasks
   - Priorities are correct
   - Order minimizes rework
   - Rework analysis confirms no conflicts

**The final gate**: "We both like this task list and neither of us has questions"

### Sprint Size Check
- Total estimates should be <24 hours of Claude execution time
- If larger, consider splitting into multiple sprints
- Remember: Machine stability enables long unattended runs

---

*This is a living document. Each sprint's task generation experience should contribute improvements.*