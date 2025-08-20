# Dual System Mastery Strategy: TodoWrite + Todo MCP v0.6.8.1

## The Iron Rule (Learned from P2KB Violation)

> **TodoWrite NEVER tracks multiple Todo MCP task IDs**  
> **TodoWrite is ONLY a scratch pad for the CURRENT single MCP task**

## Critical Concept: Position ID Universe

**Position IDs exist in a temporary universe defined by your current list view:**
- `position_id:1` = first task in your CURRENT todo_list output
- Run a filtered list or sort differently = NEW position universe
- Position IDs are ephemeral and view-specific

**Task IDs are permanent anchors:**
- `task_id:"#42"` = always refers to the same task
- Survives filtering, sorting, session changes
- Safe for automation and scripts

**Choose based on your context:**
- **Interactive work** (you see the list): `position_id` is convenient
- **Automation/scripts**: `task_id` is safer
- **Uncertain universe**: Use `task_id` or verify with todo_list first
- **Both accepted**: All functions that take position_id also accept task_id

This flexibility lets you work naturally - quick position references when you're looking at the list, permanent IDs when you need reliability.

## Operational Safety Foundations

### Empirically Validated Type Requirements
**Based on actual testing (2025-08-19), these are the verified parameter requirements:**
```bash
# NUMBER types (will fail if passed as string)
estimate_minutes: 60        # ✅ Correct
estimate_minutes: "60"      # ❌ Will fail

# STRING types with flexibility
priority: "high"            # ✅ Case-insensitive (HIGH, High, high all work)
status: "in_progress"       # ⚠️ Must be exact lowercase (IN_PROGRESS fails)

# BOOLEAN types  
force: true                 # ✅ Boolean value
include_context: false      # ✅ Boolean value

# ID formats
task_id: #890              # ✅ In parameter (no quotes)
position_id: 1             # ✅ Plain number
```

### Safe Testing Sandbox Pattern
**When you need to test potentially destructive operations or verify behavior:**

```bash
# Step 1: Create safety backup (without context to preserve working memory)
mcp__todo-mcp__project_dump include_context:false
# Note the filename returned (e.g., project_dump_20250819_120758.json)

# Step 2: Run your tests freely
# - Test parameter variations
# - Try destructive operations  
# - Verify error behaviors
# - Experiment with edge cases

# Step 3: Restore to clean state
mcp__todo-mcp__project_restore file:"project_dump_20250819_120758.json" mode:"replace" include_context:false
```

**Benefits of this pattern:**
- **Zero risk**: Real work is protected
- **Clean testing**: Isolated from production tasks
- **Context preservation**: Working memory remains intact
- **Repeatability**: Can run multiple test scenarios
- **Learning tool**: Safe exploration of system boundaries

### Defensive Operation Protocol
```bash
# Before risky operations:
1. Get current state: mcp__todo-mcp__todo_list
2. Verify target exists with expected status
3. Consider using dump/restore pattern for safety

# After operations:
1. Refresh state to confirm success
2. If unexpected result, restore from backup
```

## System Architecture

### Todo MCP (Persistent Layer)
- **Purpose**: Project features, session-spanning work, permanent tracking
- **Persistence**: Survives crashes, compaction, session changes
- **Identity**: Permanent task IDs «#N» for automation and reference
- **Lifecycle**: Multi-session, can span days/weeks
- **Backup**: Full project dumps with context preservation

### TodoWrite (Tactical Layer)  
- **Purpose**: Implementation steps, test fixes, current task breakdown
- **Persistence**: Temporary, cleared on MCP task completion
- **Identity**: Sequential steps for human cognitive scanning
- **Lifecycle**: Single session, supports one MCP task only
- **Backup**: Context preservation when switching tasks

## The Standard Workflow

### 1. Strategic Planning (MCP)
```bash
# Create persistent task for main work
mcp__todo-mcp__todo_create content:"Implement authentication system" estimate_minutes:240 priority:"high"

# Start the MCP task (using position from current list universe)  
mcp__todo-mcp__todo_start position_id:1
```

### 2. Tactical Breakdown (TodoWrite)
```bash
# Break down current MCP task into implementation steps
TodoWrite: [
  "Research authentication patterns",
  "Design API endpoints", 
  "Implement core auth logic",
  "Add comprehensive tests",
  "Integration with existing system"
]
```

### 3. Context Bridge (Critical for Recovery)
```bash
# ALWAYS save TodoWrite state to context for crash recovery
mcp__todo-mcp__context_set key:"task_#N_steps" value:'["✓Research patterns","Design API","Implement core","Add tests","Integration"]'
```

**Why full snapshot works:**
- TodoWrite is transient and can be lost entirely (crashes, compaction)
- It only tracks ONE MCP task's subtasks, keeping it naturally small (5-10 items typical)
- Task decomposition happens at MCP level, preventing oversized TodoWrite lists
- Full fidelity backup ensures perfect recovery without information loss
- The dual-system architecture solves the size problem by design

This pattern achieves **brevity without losing fidelity** - the list is brief because it's scoped to one task, not because we artificially compressed it.

### 4. Work Execution
- Work through TodoWrite steps sequentially
- Update TodoWrite status (✓ for completed steps)
- Update context bridge after each major step
- Promote discoveries to new MCP tasks if needed

### 5. Task Completion
```bash
# Complete MCP task
mcp__todo-mcp__todo_complete position_id:1  # or task_id:"#N"

# Clear TodoWrite (clean slate for next task)
TodoWrite: []

# Clean up task-specific context
mcp__todo-mcp__context_delete pattern:"task_#N_*"
```

## Advanced Patterns

### Task Switching Protocol
```bash
# Pause current work
mcp__todo-mcp__context_set key:"task_#42_steps" value:'["✓Step1","→Step2","Step3"]'
mcp__todo-mcp__todo_pause position_id:1 reason:"Blocked on review"
TodoWrite: []

# Resume later
mcp__todo-mcp__todo_resume position_id:1
steps = mcp__todo-mcp__context_get key:"task_#42_steps"
TodoWrite: [from context steps]
```

### Discovery Promotion Pattern
```bash
# Work in TodoWrite (disposable, fast exploration)
TodoWrite: ["Research echo behavior", "Test with PST", "Document findings"]

# Promote important discoveries to permanent MCP tasks
mcp__todo-mcp__todo_create content:"[CRITICAL] Echo filtering mechanism needs refactoring" estimate_minutes:90

# Clean TodoWrite when MCP task created
TodoWrite: []
```

### Sprint Integration
```bash
# MCP tasks define sprint scope
mcp__todo-mcp__todo_create content:"Feature A implementation #sprint-v2.1" estimate_minutes:180
mcp__todo-mcp__todo_create content:"Feature B testing #sprint-v2.1" estimate_minutes:120

# TodoWrite provides daily execution breakdown
TodoWrite: ["Implement Feature A API", "Unit tests", "Integration tests"]
```

## Context Management Strategy

### Persistent Context (Keep)
- `lesson_*` - Learning from mistakes and successes
- `workaround_*` - Solutions to known tool limitations
- `recovery_*` - Emergency procedures and backup info
- `friction_*` - Tool improvement opportunities

### Temporary Context (Delete)
- `temp_*` - Scratch calculations and temporary state  
- `current_*` - Active work status (delete when work complete)
- `session_*` - Session-specific state (delete at session end)
- `task_#N_*` - Task-specific tracking (delete when task complete)

### Context Hygiene Rules
1. **Copy TodoWrite to context** after every significant change
2. **Delete task context** immediately after task completion
3. **Regular cleanup** of temporary keys (age-based)
4. **Pattern-based deletion** for efficiency
5. **Context stats monitoring** to prevent bloat

## Quality Patterns

### The TodoWrite Discipline Violation (Never Repeat)
**WRONG**: Creating TodoWrite "project tracker" with multiple MCP task IDs
```bash
# ❌ NEVER DO THIS
TodoWrite: [
  "Task #523: Implement feature",
  "Task #524: Add tests", 
  "Task #525: Documentation"
]
```

**CORRECT**: One MCP task at a time
```bash
# ✅ ALWAYS DO THIS  
Current MCP Task: #523
TodoWrite: [
  "Research implementation patterns",
  "Design feature architecture", 
  "Implement core functionality",
  "Add comprehensive tests"
]
```

### Process Consistency Rule
**Autonomy changes WHO makes decisions, not HOW work gets done.**

Whether user is present or absent:
- Same TodoWrite discipline (single task only)
- Same context preservation patterns  
- Same quality standards
- Same recovery procedures

## Recovery Excellence

### Primary Recovery (2-Minute Protocol)
```bash
# Step 1: Quick state check (30s)
mcp__todo-mcp__context_resume

# Step 2: Full context if needed (30s) 
mcp__todo-mcp__context_get_all

# Step 3: Verify task state (30s)
mcp__todo-mcp__todo_list

# Step 4: Rebuild TodoWrite from context (30s)
# Reconstruct current task steps from context_get
```

### Context Resume Enhancement (v0.6.8.1)
- **10-minute recent window**: Shows context keys modified in last 10 minutes
- **Automatic grouping**: Context organized by prefix patterns
- **Age indicators**: Clear visibility into stale vs fresh context
- **Task integration**: Active and paused tasks with elapsed time

### Success Metrics
- **Data preservation**: 100% (MCP tasks + critical context)
- **Recovery time**: <2 minutes average
- **Work continuity**: Resume at exact interruption point
- **Quality consistency**: No degradation during recovery

## Anti-Patterns to Avoid

### Critical Violations
1. **Multiple MCP task IDs in TodoWrite** → Quality degradation
2. **Not copying TodoWrite to context** → Lost progress on crash
3. **Not cleaning task context after completion** → Context bloat
4. **Using TodoWrite for long-term tracking** → Wrong tool for purpose

### Medium Issues  
1. **Forgetting to start MCP tasks** → No time tracking
2. **Not promoting important discoveries** → Lost insights
3. **Manual context cleanup only** → Unsustainable maintenance
4. **Trusting empty states without verification** → Missing data

## Meta-Learning: Why This Works

### Cognitive Benefits
- **TodoWrite**: Immediate visibility into current work breakdown
- **MCP**: Persistent memory across sessions and interruptions  
- **Context**: Communication channel between past and future work

### Technical Benefits
- **Crash resilience**: Multiple recovery mechanisms
- **Context hygiene**: Systematic cleanup prevents memory issues
- **Quality consistency**: Same standards under all conditions
- **Discovery preservation**: Important insights become permanent tasks

### Process Benefits
- **Clear boundaries**: Each system has specific purpose
- **Scalable patterns**: Works for simple tasks and complex projects
- **Recovery confidence**: Systematic procedures build trust
- **Continuous improvement**: Friction documentation drives tool evolution

## Summary

The dual system strategy provides both **tactical visibility** (TodoWrite) and **strategic persistence** (Todo MCP) while maintaining **crash resilience** and **quality consistency**. 

**Key Success Formula**: One MCP task + TodoWrite breakdown + Context bridge + Clean completion = Reliable, recoverable, high-quality workflows.