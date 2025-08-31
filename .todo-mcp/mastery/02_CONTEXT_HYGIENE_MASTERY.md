# Context Hygiene Mastery: Key-Value Management for Todo MCP

## Critical Understanding: Value Size > Key Count

**The Real Challenge**: It's not about KEY COUNT - it's about VALUE SIZE
- 10 keys with huge values = system stress and auto-compaction risk
- 100 keys with tiny values = runs fine
- Context system has no direct size measurement (yet)

**Core Principle**: Context is for POINTERS, not PAYLOADS

### Value Size Best Practices
```bash
✅ Brief markers: "✓Auth|→API|Tests|Deploy"
❌ Full TodoWrite with detailed descriptions

✅ Error type and line: "TypeError line 42"
❌ Complete error messages and stack traces

✅ File pointer: "See analysis in /docs/task-42.md"
❌ Storing entire file contents or long analyses
```

## Context Purpose Classification

### Persistent Context (KEEP)
```bash
lesson_*         # Learning from mistakes and successes
workaround_*     # Solutions to known tool limitations  
recovery_*       # Emergency procedures and backup info
friction_*       # Tool improvement opportunities
```

### Temporary Context (DELETE after use)
```bash
temp_*           # Scratch calculations and temporary state
current_*        # Active work status
session_*        # Session-specific state
task_#N_*        # Task-specific tracking
```

## Pattern Operations (v0.6.8.2)

### ALWAYS Audit Before Delete
```bash
# Step 1: Audit what exists
mcp__todo-mcp__context_get pattern:"temp_*"         # Review temp keys
mcp__todo-mcp__context_get pattern:"task_#*_*"      # Check task keys

# Step 2: Delete only after verification
mcp__todo-mcp__context_delete pattern:"temp_*"      # Safe cleanup
```

### Temporal Filtering
```bash
# Find recently modified keys
mcp__todo-mcp__context_get pattern:"temp_*" minutes_back:60     # Last hour
mcp__todo-mcp__context_get pattern:"session_*" minutes_back:30   # Last 30 mins
```

### Pattern Types
```bash
# Glob patterns (simple)
pattern:"lesson_*"        # All lessons
pattern:"task_#*_*"       # All task contexts

# Regex patterns (advanced)
pattern:"/^session_\d{8}$/"     # Session_YYYYMMDD
pattern:"/^task_#\d+_.*/"       # Task #N contexts
```

## Auto-Compaction Protection

### During Active Work
```bash
# Save TodoWrite state frequently
TodoWrite: ["✓Step1", "→Step2", "Step3", "Step4"]
mcp__todo-mcp__context_set key:"task_#N_steps" value:"✓Step1|→Step2|Step3|Step4"

# Use brief markers, pipes for separation, under 200 chars
```

### Essential Recovery Keys
```bash
session_focus_YYYYMMDD     # What you're working on today
task_#N_steps              # Current TodoWrite state
task_#N_progress           # Progress within current task
recovery_next_action       # Exact next step to take
```

### Recovery After Auto-Compaction
```bash
# Step 1: ALWAYS run this first
mcp__todo-mcp__context_resume

# Step 2: If limited info shown, get full context
mcp__todo-mcp__context_get_all

# Step 3: Reconstruct TodoWrite from task_#N_steps
# Step 4: Continue work
mcp__todo-mcp__todo_resume position_id:1
```

## Context Resume Window Understanding

**"N active from last 10 minute(s)"** means:
- Shows keys updated within 10 minutes **BEFORE the most recent key**
- It's a **relative window** from the newest key, NOT from current time
- Helps identify the "hot zone" of activity when work stopped

Example:
- "0 active" = Session ended cleanly, no last-minute scramble
- "5 active" = Active work in progress, these 5 keys are your best resume clues

## Task Lifecycle Pattern

### Task-Specific Context Bridge
```bash
# Start task - create bridge
mcp__todo-mcp__todo_start position_id:1
mcp__todo-mcp__context_set key:"task_#N_steps" value:'["Step1","Step2","Step3"]'

# During work - update bridge
mcp__todo-mcp__context_set key:"task_#N_steps" value:'["✓Step1","→Step2","Step3"]'

# Complete task - audit then clean
mcp__todo-mcp__context_get pattern:"task_#N_*"      # Review all
mcp__todo-mcp__todo_complete position_id:1
mcp__todo-mcp__context_delete pattern:"task_#N_*"   # Clean all
```

## Daily Hygiene Routine

```bash
# Session start
mcp__todo-mcp__context_resume                              # Check state
mcp__todo-mcp__context_get pattern:"temp_*" minutes_back:1440  # Yesterday's temp
mcp__todo-mcp__context_delete pattern:"temp_*"             # Clean after audit

# Session end  
mcp__todo-mcp__context_get pattern:"current_*"             # Audit
mcp__todo-mcp__context_delete pattern:"current_*"          # Clean
```

## Emergency Procedures

### Context Bloat Crisis (>100 keys or performance issues)
```bash
# Step 1: Backup everything
mcp__todo-mcp__project_dump include_context:true

# Step 2: Audit biggest offenders
mcp__todo-mcp__context_get pattern:"temp_*"        # Usually largest
mcp__todo-mcp__context_get pattern:"session_*"     # Often accumulates

# Step 3: Aggressive cleanup
mcp__todo-mcp__context_delete pattern:"temp_*"
mcp__todo-mcp__context_delete pattern:"session_*"

# Step 4: Verify reduction
mcp__todo-mcp__context_stats
```

## Key Design Strategy

```bash
# EXCELLENT - enables pattern operations
temp_calculation_HHMMSS      # Clean: pattern:"temp_*"
task_#42_progress           # Clean: pattern:"task_#42_*"  
session_20250819_status     # Clean: pattern:"session_20250819_*"

# POOR - requires individual deletion
calculation_temp            # No clear pattern prefix
progress_for_task_42        # Mixed format
status_today               # Ambiguous, no timestamp
```

## Optional: Filesystem MCP Optimization

If `mcp__filesystem__` tools are available in your instance:

```bash
# Check availability
mcp__filesystem__list_directory path:"."

# If available, prefer for file operations:
mcp__filesystem__read_text_file     # Instead of: cat, Read tool
mcp__filesystem__write_file         # Instead of: echo, Write tool  
mcp__filesystem__search_files       # Instead of: find, grep

# Benefits: No approval interruptions, faster response, structured output
```

## Success Metrics

- **Value size**: Keep individual values under 500 chars
- **Key count**: Target ≤40 keys (secondary to value size)
- **Cleanup efficiency**: 90% pattern-based operations
- **Recovery speed**: <30 seconds with context_resume
- **Auto-compaction survival**: State preserved through TodoWrite bridging