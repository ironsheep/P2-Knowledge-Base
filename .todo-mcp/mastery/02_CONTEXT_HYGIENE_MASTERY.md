# Context Hygiene Mastery: Key-Value Management for Todo MCP v0.6.8.1

## Authority and Critical Importance

**Context system** is Todo MCP's persistent memory across sessions, crashes, and interruptions. Poor context hygiene causes:
- Memory crashes and forced compaction
- Lost work state during recovery
- Performance degradation
- Context bloat leading to system instability

## 🔴 CRITICAL: Context Purpose Classification

### Persistent Context (KEEP)
**Purpose**: Long-term learning and system knowledge
```bash
lesson_*         # Learning from mistakes and successes
workaround_*     # Solutions to known tool limitations  
recovery_*       # Emergency procedures and backup info
friction_*       # Tool improvement opportunities
```

### Temporary Context (DELETE after use)  
**Purpose**: Working memory for current tasks
```bash
temp_*           # Scratch calculations and temporary state
current_*        # Active work status (delete when work complete)
session_*        # Session-specific state (delete at session end)
task_#N_*        # Task-specific tracking (delete when task complete)
```

## 🎯 Managing Context Value Size (The Real Challenge)

### The Actual Problem
**It's not about KEY COUNT - it's about VALUE SIZE**
- 10 keys with huge values = system stress
- 100 keys with tiny values = runs fine
- No direct size measurement available (yet)

### Monitoring Without Size Visibility
```bash
# Regular health checks
mcp__todo-mcp__context_get_all

# Warning signs to watch for:
# - Output becoming unwieldy to read
# - Individual values spanning many lines
# - Context operations slowing down
# - Difficulty finding specific keys in the output
```

### Value Size Best Practices
```bash
# Keep values CONCISE
❌ Storing entire file contents or long analyses
✅ Storing pointers: "See analysis in /docs/task-42.md"

❌ Full TodoWrite with detailed descriptions
✅ Brief markers: "✓Auth|→API|Tests|Deploy"

❌ Complete error messages and stack traces
✅ Error type and key diagnostic: "TypeError line 42"
```

**Principle: Context is for POINTERS, not PAYLOADS**

## Context Lifecycle Management

### Task-Specific Context Bridge Pattern
```bash
# When starting MCP task - create context bridge
mcp__todo-mcp__todo_start position_id:1
mcp__todo-mcp__context_set key:"task_#N_steps" value:'["Step1","Step2","Step3"]'

# During work - update bridge after changes
mcp__todo-mcp__context_set key:"task_#N_steps" value:'["✓Step1","→Step2","Step3"]'

# When completing task - review context needs
mcp__todo-mcp__todo_complete position_id:1
# Consider: Is task_#N_* context still useful for related work?
# If not: mcp__todo-mcp__context_delete pattern:"task_#N_*"
```

### Session Handoff Management
```bash
# When pausing work for extended time
mcp__todo-mcp__context_set key:"session_handoff_YYMMDD" value:"[current work state summary]"

# When resuming (next day/session)
mcp__todo-mcp__context_get key:"session_handoff_YYMMDD"
# Use information, then delete
mcp__todo-mcp__context_delete key:"session_handoff_YYMMDD"
```

## Context Review Opportunities

### Task Completion: Context Review Opportunity

**Intent**: Task completion is a natural boundary to review and optimize your context storage.

**Why this moment?**
- You've just finished focused work and have perspective
- You know what information was actually useful vs speculative
- It's a clean break point before starting something new

**Suggested Review Process**:
```bash
# 1. See what you've accumulated
mcp__todo-mcp__context_get_all

# 2. Evaluate each key:
# - Still needed for upcoming work?
# - Contains insights worth preserving?
# - Could be updated with better information?
# - Should be externalized to documentation?

# 3. Take appropriate action:
# Delete stale: context_delete pattern:"task_#N_*"  # If those tasks are truly done
# Update: context_set key:"lesson_auth" value:"[refined insight]"
# Externalize: Move valuable patterns to docs, then delete context
# Keep: Leave keys that serve ongoing work
```

**Consider Externalizing When**:
- Information has long-term value beyond current session
- Pattern could help other instances or future work
- Context value is getting large but information is important
- Example: Moving accumulated lessons to a `LESSONS-LEARNED.md` file

**The Goal**: Keep context as **active working memory**, not an archive.

### Daily Hygiene Routine
```bash
# At session start
mcp__todo-mcp__context_resume                    # Check recent activity
mcp__todo-mcp__context_delete pattern:"temp_*"   # Clean scratch data

# During work
# Clean as you go - delete temp keys immediately after use

# At session end  
mcp__todo-mcp__context_delete pattern:"current_*"  # Clean active state
mcp__todo-mcp__context_delete pattern:"session_*"  # Clean session data
```

### Weekly Deep Clean
```bash
# Review persistent context for relevance
mcp__todo-mcp__context_get_all

# Questions to ask:
# - Are lesson_* keys still valuable?
# - Are workaround_* keys still needed?
# - Can friction_* be documented and removed?
# - Are recovery_* procedures up to date?

# Archive valuable insights to documentation before deleting
```

## Pattern-Based Cleanup Excellence

### Efficient Bulk Operations
```bash
# PREFER pattern deletion over individual keys
mcp__todo-mcp__context_delete pattern:"temp_*"     # vs individual temp keys
mcp__todo-mcp__context_delete pattern:"task_#N_*"  # vs manual task cleanup
mcp__todo-mcp__context_delete pattern:"old_*"      # vs selecting old keys

# Design keys for efficient cleanup from the start
```

### Context Key Design Strategy
```bash
# GOOD key design - enables pattern cleanup
temp_calculation_HHMMSS      # Can clean all temp_* 
task_#42_progress           # Can clean all task_#42_*
session_20250819_status     # Can clean all session_YYYYMMDD_*

# BAD key design - requires individual deletion
calculation_temp            # No clear pattern
progress_for_task_42        # Mixed format
status_today               # Ambiguous timeframe
```

## Context Purpose Discipline

### Before Storing Context - Purpose Check
```bash
PURPOSE CHECK:
- "Is this for crash recovery?" → Use structured key with task/session ID
- "Is this a lesson to remember?" → Use lesson_ prefix, consider documentation  
- "Is this temporary calculation?" → Use temp_ prefix + immediate cleanup plan
- "Is this session handoff?" → Use session_ prefix + expiry plan

# Context is working memory, not permanent storage
# If valuable long-term, document it instead of storing in context
```

### Quality Gates for Context Operations
```bash
# Before storing new context
✓ Clear purpose defined (recovery, lesson, temp, handoff)
✓ Appropriate prefix selected
✓ Cleanup plan established (when will this be deleted?)
✓ Not duplicating existing context

# Before deleting context
✓ Valuable insights documented elsewhere if needed
✓ No active dependencies on this context
✓ Pattern deletion preferred over individual keys
```

## Recovery and Context Restoration

### Post-Crash Context Assessment
```bash
# Step 1: Quick assessment
mcp__todo-mcp__context_resume  # May show incomplete/empty

# Step 2: Full verification (ALWAYS)
mcp__todo-mcp__context_get_all  # Full verification of context state

# Step 3: Identify recovery context
# Look for: task_#N_*, session_*, recovery_* keys

# Step 4: Reconstruct work state
# Use context to rebuild TodoWrite and continue work
```

### Context Bridge Recovery Pattern
```bash
# Standard recovery flow
steps = mcp__todo-mcp__context_get key:"task_#N_steps"
if (steps_found) {
    TodoWrite: [restore from context steps]
    mcp__todo-mcp__todo_resume position_id:1  # Continue where left off
} else {
    # Examine todo_list for in_progress tasks
    # Reconstruct work state from available information
}
```

## Anti-Pattern Prevention

### Critical Context Anti-Patterns
```bash
# 1. Context Value Bloat Crisis (large values, not key count)
PREVENTION: Keep values concise, store pointers not payloads, monitor readability

# 2. Manual Key-by-Key Cleanup  
PREVENTION: Design keys for pattern cleanup, use bulk operations

# 3. No Review After Task Completion
PREVENTION: Use task boundaries as review opportunities, evaluate context relevance

# 4. Storing Permanent Info in Context
PREVENTION: Document valuable insights, use context for working memory only

# 5. Trusting Empty Context Without Verification
PREVENTION: Always run context_get_all after context_resume shows empty
```

## Integration with Dual System Strategy

### Context as Communication Bridge
**TodoWrite ↔ Context ↔ Future Sessions**
- TodoWrite state saved to context for crash recovery
- Context preserves work state across interruptions
- Context enables perfect session handoffs

### Context Workflow Integration
```bash
# Standard workflow with context hygiene
1. Start MCP task → Create context bridge
2. Work in TodoWrite → Update context bridge after changes  
3. Complete MCP task → Clean task-specific context
4. Archive completed tasks → Clean session context
5. End session → Clean temporary context
```

## Summary: Context Excellence Formula

**Context = Working Memory + Recovery Bridge + Learning Repository**

**Key Principles:**
1. **Proactive monitoring** - Check health before it becomes critical
2. **Pattern-based cleanup** - Design for efficient bulk operations  
3. **Purpose discipline** - Clear purpose for every key stored
4. **Automated hygiene** - Systematic cleanup, not ad-hoc maintenance
5. **Recovery readiness** - Context enables perfect work continuation

**Success Metrics:**
- Context readability: Output remains manageable and easy to navigate
- Value sizes: Concise pointers rather than large payloads
- Recovery time: <2 minutes from any interruption
- Pattern-based cleanup rather than key-by-key
- Perfect work state preservation across sessions

Context hygiene is **crash prevention** and **productivity insurance** - invest in systematic maintenance for reliable, recoverable workflows.