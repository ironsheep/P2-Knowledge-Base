# Dual System Mastery Strategy: TodoWrite + Todo MCP

## The Iron Rule

> **TodoWrite tracks ONLY the current single MCP task**  
> **Never multiple MCP task IDs in TodoWrite**

## System Architecture

**Todo MCP**: Persistent project features, survives everything, permanent IDs «#N»  
**TodoWrite**: Tactical scratch pad for current task only, cleared on completion

## Standard Workflow

### 1. Create MCP Task
```bash
mcp__todo-mcp__todo_create content:"Implement auth system" estimate_minutes:240 priority:"high"
mcp__todo-mcp__todo_start position_id:1
```

### 2. Break Down in TodoWrite
```bash
TodoWrite: [
  "Research patterns",
  "Design API", 
  "Implement logic",
  "Add tests"
]
```

### 3. Create Context Bridge (Critical)
```bash
# Save TodoWrite state for crash recovery
mcp__todo-mcp__context_set key:"task_#N_steps" value:"Research|Design|Implement|Tests"
```

### 4. Work and Update
- Work through TodoWrite steps
- Mark completed: ✓
- Update context bridge after major steps
- Promote discoveries to new MCP tasks if needed

### 5. Complete and Clean
```bash
mcp__todo-mcp__todo_complete position_id:1
TodoWrite: []  # Clear for next task
mcp__todo-mcp__context_delete pattern:"task_#N_*"  # Clean context
```

## Task Switching

```bash
# Pause current
mcp__todo-mcp__context_set key:"task_#42_steps" value:"✓Step1|→Step2|Step3"
mcp__todo-mcp__todo_pause position_id:1 reason:"Blocked"
TodoWrite: []

# Resume later
mcp__todo-mcp__todo_resume position_id:1
# Restore TodoWrite from context key task_#42_steps
```

## Recovery After Crash

```bash
mcp__todo-mcp__context_resume  # WHERE WAS I?
mcp__todo-mcp__context_get pattern:"task_#*_steps"  # Find saved TodoWrite
# Reconstruct TodoWrite from context
mcp__todo-mcp__todo_list  # See MCP tasks
```

## Quality Patterns

### Discovery Promotion
```bash
# Explore in TodoWrite (disposable)
TodoWrite: ["Quick test", "Document finding"]

# If important, promote to MCP
mcp__todo-mcp__todo_create content:"Fix critical bug found" estimate_minutes:60

# Clear TodoWrite after promotion
TodoWrite: []
```

### Filtered Work (v0.6.8.2)
```bash
# Work on high-priority only
mcp__todo-mcp__todo_next priority:"high"

# Tag-specific workflow
mcp__todo-mcp__todo_next tags:["backend"]
```

## Common Mistakes

❌ **Multiple MCP tasks in TodoWrite**: Causes confusion and quality degradation  
✅ **One MCP task at a time**: Clear focus, better quality

❌ **Not saving TodoWrite to context**: Lost state on crash  
✅ **Regular context bridges**: Survives anything

❌ **Keeping completed steps in TodoWrite**: Cluttered view  
✅ **Clear TodoWrite on MCP completion**: Fresh start each task

## Success Story: Manual Migration Excellence

The p2kb instance successfully migrated 31 tasks and 183 context keys through manual process in 1 hour (vs 6-8 hour failed automation). Key learnings:
- Human validation at each step
- Adaptive discovery of project-specific content
- Zero data loss through careful bridging
- Immediate expert-level operation after migration

This proves the dual system works when properly understood and applied.