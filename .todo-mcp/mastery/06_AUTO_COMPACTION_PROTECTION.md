# Auto-Compaction Protection Pattern

## The Auto-Compaction Challenge

When Claude auto-compacts due to context limits, you lose:
- Current TodoWrite state
- Working memory about active tasks
- Session-specific context
- Progress markers

## Protection Strategy: Frequent Context Bridging

### During Active Work
```bash
# Every time TodoWrite changes significantly
TodoWrite: ["✓Step1", "→Step2", "Step3", "Step4"]
mcp__todo-mcp__context_set key:"task_#N_steps" value:"✓Step1|→Step2|Step3|Step4"

# Use brief markers, not full descriptions
# Pipes or commas for separation
# Keep value under 200 chars
```

### Key Design for Auto-Compaction Recovery
```bash
# Essential recovery keys (always reconstruct these)
session_focus_YYYYMMDD     # What you're working on today
task_#N_steps              # Current TodoWrite state
task_#N_progress           # Progress within current task
recovery_next_action       # Exact next step to take
```

### Recovery After Auto-Compaction

**The Golden Rule**: `context_resume` is MANDATORY after any interruption.

```bash
# Step 1: ALWAYS run this first
mcp__todo-mcp__context_resume

# Step 2: If context_resume shows limited info
mcp__todo-mcp__context_get_all

# Step 3: Reconstruct TodoWrite from context
# Look for task_#N_steps or similar patterns
# Rebuild your working state

# Step 4: Continue work
mcp__todo-mcp__todo_resume position_id:1
```

## Frequency Guidelines

### Save to Context When:
- Starting a new phase of work
- Completing a significant step
- Before potentially risky operations
- Every 10-15 minutes during complex work
- Switching between major tasks
- User provides new direction mid-work

### What to Save:
- Brief progress markers (not full text)
- Next action pointers
- Critical decision points
- Blocking issues encountered
- Key discoveries or insights

## Example: Protected Workflow

```bash
# Start task
mcp__todo-mcp__todo_start position_id:1
TodoWrite: ["Analyze requirements", "Design solution", "Implement", "Test"]
mcp__todo-mcp__context_set key:"task_#915_steps" value:"Analyze|Design|Implement|Test"

# After completing first step
TodoWrite: ["✓Analyze requirements", "→Design solution", "Implement", "Test"]
mcp__todo-mcp__context_set key:"task_#915_steps" value:"✓Analyze|→Design|Implement|Test"

# If auto-compaction happens here, you can recover:
# - Run context_resume to see task #915 in progress
# - Get task_#915_steps to reconstruct TodoWrite
# - Continue from "Design solution"

# Complete work
mcp__todo-mcp__todo_complete position_id:1
mcp__todo-mcp__context_delete pattern:"task_#915_*"
TodoWrite: []
```

## Anti-Patterns to Avoid

### ❌ Storing Full TodoWrite Arrays
```bash
# BAD: Too verbose, wastes space
context_set key:"todo" value:'["Complete full analysis of requirements document", "Design comprehensive solution architecture", ...]'
```

### ✅ Store Brief Markers Instead
```bash
# GOOD: Concise, recoverable
context_set key:"todo" value:"✓Analysis|→Design|Architecture|Testing"
```

### ❌ Infrequent Saves
```bash
# BAD: Only saving at task completion
# Risk: Lose all progress if compaction happens mid-work
```

### ✅ Regular Checkpoint Saves
```bash
# GOOD: Save after each significant step
# Ensures maximum 1 step lost on compaction
```

## Integration with CLAUDE.md

This pattern is why CLAUDE.md mandates:
1. **Session start**: Always run `context_resume` first
2. **During work**: Bridge TodoWrite to context frequently  
3. **Task completion**: Clean task-specific context
4. **Recovery**: Trust context over memory

## Summary

**Auto-compaction is inevitable. Protection is systematic.**

Key principles:
1. Save progress markers frequently (every significant step)
2. Keep context values brief (pointers not payloads)
3. Design keys for easy pattern matching
4. Always run context_resume after any interruption
5. Trust the context bridge pattern

With proper protection, auto-compaction becomes a minor inconvenience rather than a work-destroying event.