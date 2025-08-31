# Todo MCP Mastery Operations for CLAUDE.md

## DEPLOYMENT INSTRUCTIONS FOR CLAUDE

1. **FIRST**: Remove ALL existing Todo MCP content from CLAUDE.md:
   - Delete any sections about Todo MCP v0.6.8, v0.6.8.1
   - Remove all TodoWrite guidance
   - Clear any context management patterns related to todo-mcp
   - Keep only: Project info, build process, general rules

2. **THEN**: Insert everything below the line into CLAUDE.md
   - **CRITICAL PLACEMENT**: Insert IMMEDIATELY after project info
   - **MUST BE EARLY**: Enables automatic recovery from auto-compaction
   - This replaces all previous Todo MCP documentation
   - Single source of truth, no version conflicts

**WHY PLACEMENT MATTERS**: When Claude auto-compacts or conversation resets, having `context_resume` early in CLAUDE.md means Claude automatically recovers state without human intervention.

---

## 🎯 CRITICAL: SESSION START PROTOCOL (EXECUTE IMMEDIATELY)

**MANDATORY ON SESSION START/RESUME:**
```bash
mcp__todo-mcp__context_resume    # Primary recovery command - WHERE WAS I?
# Provides: current tasks, context state, next recommendations
```

**ALWAYS execute this command FIRST before any other work.**

## Todo MCP Mastery Operations

### Dual System Strategy
**MCP Tasks**: Persistent, session-spanning, permanent ID «#N»  
**TodoWrite**: Current task breakdown only, cleared on completion

```bash
# CORRECT workflow
mcp__todo-mcp__todo_create content:"Feature implementation" estimate_minutes:180
mcp__todo-mcp__todo_start position_id:1
TodoWrite: ["Step 1", "Step 2", "Step 3"]  # Single task breakdown only
# Work through steps...
mcp__todo-mcp__todo_complete position_id:1
TodoWrite: []  # Clear for next task
```

### Core Parameters
```bash
# Most functions use position_id OR task_id
mcp__todo-mcp__todo_start position_id:1          # Interactive
mcp__todo-mcp__todo_complete task_id:"#22"       # Automation

# Critical data types
estimate_minutes:60        # Number, not string
priority:"high"           # lowercase: critical/high/medium/low/backlog
force:true               # Boolean, not string
```

### Context Hygiene (40-Key Target)

**VALUE SIZE matters more than key count**:
- Keep values under 500 chars (pointers, not payloads)
- Use patterns for bulk operations

```bash
# Pattern-based cleanup (v0.6.8.2)
mcp__todo-mcp__context_get pattern:"temp_*"        # Audit first
mcp__todo-mcp__context_delete pattern:"temp_*"     # Then delete

# Temporal filtering
mcp__todo-mcp__context_get pattern:"temp_*" minutes_back:60  # Last hour

# Auto-compaction protection
mcp__todo-mcp__context_set key:"task_#N_steps" value:"✓Step1|→Step2|Step3"
```

### Quick Commands
```bash
# Recovery
mcp__todo-mcp__context_resume     # "WHERE WAS I?"
mcp__todo-mcp__todo_next          # Smart task recommendation

# Cleanup
mcp__todo-mcp__todo_archive       # Archive completed tasks
mcp__todo-mcp__context_delete pattern:"temp_*"    # Clean temporary

# Backup
mcp__todo-mcp__project_dump include_context:true  # Complete backup
```

### Task Lifecycle
1. **Start** before work: `todo_start position_id:1`
2. **Complete** after work: `todo_complete position_id:1`
3. **Archive** when done: `todo_archive`
4. Only ONE task `in_progress` at a time (auto-enforced)

### Anti-Patterns to Avoid
- ❌ Multiple MCP task IDs in TodoWrite
- ❌ Large values in context (>500 chars)
- ❌ Deleting without audit
- ❌ Ignoring context_resume on start

### Optional: Filesystem MCP (If Available)
```bash
# Check availability
mcp__filesystem__list_directory path:"."

# If available, prefer for file operations:
mcp__filesystem__read_text_file     # Instead of cat
mcp__filesystem__write_file         # Instead of echo
# Benefits: No approval prompts, faster, structured output
```

### Deep Learning Resources
Study `.todo-mcp/mastery/` documentation for comprehensive patterns:
- `01_DUAL_SYSTEM_MASTERY_STRATEGY.md`
- `02_CONTEXT_HYGIENE_MASTERY.md`
- `03_TODO_MCP_MASTERY_INTERFACE.md`
- `04_ANTI_PATTERN_ENFORCEMENT.md`