# Anti-Pattern Enforcement: Quality Protection Mechanisms

## Critical Anti-Patterns That Break Everything

### 1. Multiple MCP Tasks in TodoWrite
**Anti-Pattern**: 
```bash
TodoWrite: ["#42: Fix auth", "#43: Add tests", "#44: Update docs"]
```

**Why It Breaks**: 
- Cognitive overload
- Lost focus
- Quality degradation
- Context confusion

**Correct Pattern**:
```bash
mcp__todo-mcp__todo_start position_id:1
TodoWrite: ["Research auth", "Fix implementation", "Test thoroughly"]
# Only steps for current MCP task #42
```

### 2. Context Value Bloat
**Anti-Pattern**:
```bash
mcp__todo-mcp__context_set key:"analysis" value:"[5000 chars of analysis text...]"
```

**Why It Breaks**:
- Triggers auto-compaction
- Slows operations
- Memory pressure
- Unreadable output

**Correct Pattern**:
```bash
mcp__todo-mcp__context_set key:"analysis" value:"Complete analysis in docs/analysis-42.md"
# Store pointer, not payload
```

### 3. Delete Without Audit
**Anti-Pattern**:
```bash
mcp__todo-mcp__context_delete pattern:"*"  # NEVER DO THIS
```

**Why It Breaks**:
- Irreversible data loss
- Lost lessons/workarounds
- No recovery path

**Correct Pattern**:
```bash
mcp__todo-mcp__context_get pattern:"temp_*"     # Audit first
mcp__todo-mcp__context_delete pattern:"temp_*"  # Then delete
```

### 4. Ignoring context_resume
**Anti-Pattern**:
```bash
# Starting work without checking state
mcp__todo-mcp__todo_create content:"New feature" estimate_minutes:120
```

**Why It Breaks**:
- Duplicate work
- Lost context from previous session
- Missed in-progress tasks

**Correct Pattern**:
```bash
mcp__todo-mcp__context_resume  # ALWAYS FIRST
# Now you know where you were
```

## Enforcement Mechanisms

### Automatic Prevention
- Todo MCP enforces single in_progress task
- Pattern operations require explicit patterns (no wildcards by accident)
- Context operations show counts before deletion

### Manual Discipline Required
- TodoWrite management (you must clear it)
- Context value size (you must keep small)
- Audit before delete (you must check first)
- Session start protocol (you must run context_resume)

## Recovery Procedures

### From TodoWrite Confusion
```bash
TodoWrite: []  # Clear immediately
mcp__todo-mcp__todo_list  # See real tasks
mcp__todo-mcp__todo_next  # Get proper recommendation
# Start fresh with single task
```

### From Context Bloat
```bash
mcp__todo-mcp__context_stats  # Assess damage
mcp__todo-mcp__context_get_all  # Find large values
mcp__todo-mcp__project_dump include_context:true  # Backup
# Archive large values to files
mcp__todo-mcp__context_delete pattern:"bloated_*"
```

### From Lost State
```bash
mcp__todo-mcp__context_resume  # Try automated recovery
mcp__todo-mcp__context_get pattern:"*" minutes_back:60  # Recent activity
mcp__todo-mcp__context_get pattern:"recovery_*"  # Emergency procedures
mcp__todo-mcp__project_status  # Overall health check
```

## Policy Override Prevention

**Never ignore explicit instructions** for perceived efficiency
- Maintain same standards whether user present or absent
- Confirm before violating established patterns
- Document any necessary deviations

## Quality Metrics

Track these to ensure pattern compliance:
- TodoWrite never contains task IDs
- Context values stay under 500 chars
- All deletes preceded by audit
- context_resume run every session start
- Single task in_progress at all times

## The Cost of Anti-Patterns

From real instance experiences:
- **6-8 hours** failed automation from ignoring patterns
- **Multiple compactions** from context bloat
- **Lost work** from skipping context_resume
- **Confusion and rework** from multiple tasks in TodoWrite

## Success Through Discipline

The p2kb instance proved that following these patterns strictly leads to:
- **1 hour** successful migration (vs 6-8 hour failure)
- **Zero data loss** across 31 tasks and 183 context keys
- **Immediate mastery** without learning curve
- **Sustained productivity** through proper state management

The patterns work when followed. The anti-patterns always fail.