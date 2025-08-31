# Todo MCP Mastery Interface Reference

## Core Functions Quick Reference

### Task Management
```bash
# Create & Start
mcp__todo-mcp__todo_create content:"Task" estimate_minutes:60 priority:"high"
mcp__todo-mcp__todo_start position_id:1        # OR task_id:"#42"

# State Changes  
mcp__todo-mcp__todo_pause position_id:1 reason:"Blocked"
mcp__todo-mcp__todo_resume position_id:1
mcp__todo-mcp__todo_complete position_id:1     # OR task_id:"#42"

# Smart Navigation
mcp__todo-mcp__todo_next                       # Next recommended task
mcp__todo-mcp__todo_next priority:"high"       # Filtered by priority
mcp__todo-mcp__todo_next tags:["backend"]      # Filtered by tags
```

### Context Operations (v0.6.8.2 Pattern Support)
```bash
# Pattern Discovery
mcp__todo-mcp__context_get pattern:"temp_*"              # Glob pattern
mcp__todo-mcp__context_get pattern:"/^task_#\d+_.*/"     # Regex pattern
mcp__todo-mcp__context_get pattern:"temp_*" minutes_back:60  # Temporal

# Bulk Operations
mcp__todo-mcp__context_delete pattern:"temp_*"           # After audit
mcp__todo-mcp__context_delete pattern:"task_#42_*"       # Specific task

# Essential Commands
mcp__todo-mcp__context_resume                            # WHERE WAS I?
mcp__todo-mcp__context_stats                             # Health check
```

### Project Operations
```bash
# Maintenance
mcp__todo-mcp__todo_archive                    # Archive completed tasks
mcp__todo-mcp__project_status                  # Overall health

# Backup & Recovery
mcp__todo-mcp__project_dump include_context:true
mcp__todo-mcp__project_restore file:"backup.json" mode:"replace"
```

## Parameter Patterns (v0.6.8.2)

### Dual-Parameter Resolution
Functions accepting BOTH position_id and task_id:
- `todo_complete`
- `todo_update`
- `todo_delete`
- `todo_tag_add`
- `todo_tag_remove`

```bash
# Both work identically
mcp__todo-mcp__todo_complete position_id:1      # By position
mcp__todo-mcp__todo_complete task_id:"#42"      # By ID (preferred for automation)
```

### Critical Data Types
```bash
estimate_minutes:60        # Number (not "60")
priority:"high"           # String, lowercase only
force:true               # Boolean (not "true")
tags:["urgent","bug"]    # Array of strings
pattern:"temp_*"         # String (glob or regex)
minutes_back:120         # Number for temporal filtering
```

## Discovery Workflows

### Finding Lost Context
```bash
# Can't remember key names? Use patterns!
mcp__todo-mcp__context_get pattern:"*pdf*"       # Find anything with pdf
mcp__todo-mcp__context_get pattern:"lesson_*"    # All lessons
mcp__todo-mcp__context_get pattern:"/escape.*/"  # Regex for complex search
```

### Temporal Context Analysis  
```bash
# What was I working on recently?
mcp__todo-mcp__context_resume                    # Shows recent activity window
mcp__todo-mcp__context_get pattern:"*" minutes_back:30  # Last 30 minutes
```

## Batch Operations (v0.6.8.2)

### Bulk Task Management
```bash
# Create multiple tasks
mcp__todo-mcp__todo_batch_create tasks:[
  {content:"Task 1", estimate_minutes:30},
  {content:"Task 2", estimate_minutes:45}
]

# Bulk operations
mcp__todo-mcp__todo_bulk operation:"add_tags" data:{tags:["urgent"]} task_ids:["#12","#15"]
mcp__todo-mcp__todo_bulk operation:"set_priority" data:{priority:"high"} position_ids:[1,2,3]
```

## Filtered Workflows (v0.6.8.2)

### Working by Priority or Tags
```bash
# High-priority workflow
mcp__todo-mcp__todo_list status:"created"       # See pending work
mcp__todo-mcp__todo_next priority:"high"        # Get next high-priority
mcp__todo-mcp__todo_start position_id:1

# Tag-based workflow (e.g., backend-only)
mcp__todo-mcp__todo_next tags:["backend"]       # Backend tasks only
```

### Cross-Boundary Protection
If filtering shows no tasks but dependencies exist outside filter:
- System prevents invalid recommendations
- Alerts you to dependency conflicts
- Maintains work integrity

## Session Management Excellence

### Perfect Session Start
```bash
mcp__todo-mcp__context_resume    # ALWAYS FIRST
mcp__todo-mcp__todo_list         # See current tasks
mcp__todo-mcp__todo_next         # Get recommendation
```

### Clean Session End
```bash
mcp__todo-mcp__todo_pause position_id:1 reason:"EOD"
mcp__todo-mcp__context_set key:"session_handoff_YYMMDD" value:"Status summary"
mcp__todo-mcp__context_delete pattern:"temp_*"
mcp__todo-mcp__todo_archive      # If many completed
```

## Error Recovery Patterns

### After Auto-Compaction
```bash
mcp__todo-mcp__context_resume                   # Check what survived
mcp__todo-mcp__context_get pattern:"task_#*_steps"  # Find TodoWrite state
mcp__todo-mcp__todo_list                       # Verify tasks intact
```

### Context Bloat Emergency
```bash
mcp__todo-mcp__context_stats                    # Check severity
mcp__todo-mcp__context_get pattern:"temp_*"     # Audit biggest offenders
mcp__todo-mcp__context_delete pattern:"temp_*"  # Targeted cleanup
```

## Performance Tips

- Use patterns instead of individual operations
- Keep context values under 500 chars
- Archive completed tasks regularly
- Use position_id for interactive, task_id for automation
- Audit before bulk delete operations

## Common Issues & Solutions

**"Empty" todo_list**: Run `todo_archive` to clear corrupted completed tasks  
**Lost context keys**: Use pattern search instead of guessing names  
**Slow operations**: Check context_stats, cleanup if >75 keys  
**Parameter errors**: Verify data types (number vs string vs boolean)