# Model Switching Best Practices

## The Human Process for Safe Model Switching

### When You Notice Wrong Model

**Your Magic Phrase:**
> "Save your context, we're going to switch models, then we'll resume work."

### What Claude Should Do When You Say This

#### 1. Immediate State Preservation
```bash
# Save current TodoWrite state (if any)
context_set('todowrite_current_task_[id]', '[full TodoWrite state]')

# Save what we were doing
context_set('switch_handoff', 'Was working on: [specific task and progress]')

# Mark the phase
context_set('model_phase', 'execution')  # or 'planning' or 'debugging'

# Save any critical conversation context
context_set('important_context', '[anything critical from this conversation]')
```

#### 2. Complete Current Micro-Task
- Finish the current thought/paragraph/section
- Don't start anything new
- Get to a natural stopping point
- Ensure files are saved

#### 3. Provide Clean Handoff
Claude responds with:
```
✅ Context saved!
✅ TodoWrite state preserved
✅ Current task: [Task #X - description]
✅ Progress: [what's done, what's next]
✅ Ready to switch models

To resume after switching:
1. Use /model command
2. First message: "Check context_resume"
3. I'll pick up exactly where we left off
```

## Bad Times to Switch (Claude Should Warn)

### 🔴 TERRIBLE Times:
- Mid-extraction with partial content
- Complex reasoning chain incomplete
- TodoWrite has 5+ active items
- Just discovered something important
- In middle of debugging session

**Claude should say:**
> "WARNING: We're in the middle of [specific work]. 
> Can we complete [specific task] first? (Est: X minutes)
> Or should I save partial progress?"

### 🟡 OKAY But Not Ideal:
- Between subtasks in TodoWrite
- After completing one file but before next
- Middle of a sprint but task complete

### 🟢 PERFECT Times:
- MCP task just completed
- TodoWrite is empty
- Natural phase transition
- All files saved and committed
- Clear handoff point reached

## The Context Keys for Switching

### Standard Keys to Set:
```python
# Always set these
'model_phase': 'planning|execution|debugging|validation'
'switch_handoff': 'Specific description of where we are'
'next_mcp_task': 'Task #XXX ready to start'

# If mid-task
'todowrite_current_task_[id]': 'Full TodoWrite state'
'partial_progress': 'What's been done so far'

# If important context
'important_decisions': 'Key decisions made this session'
'blocking_issues': 'Any blockers discovered'
```

## The Recovery Protocol

### In New Model Session:
```
Human: "Check context_resume"

Claude: 
"✅ I'm running on [Model Name]
✅ Previous session was in [phase] phase
✅ Handoff note: [switch_handoff content]
✅ Next task: [next_mcp_task]
✅ TodoWrite state: [Restored if exists]

Ready to continue with [specific next action]?"
```

## Examples of Good Human Direction

### Example 1: Planning → Execution
> "We've finished planning. Save your context, we're switching to Sonnet for execution."

### Example 2: Hit Unexpected Complexity
> "This is more complex than expected. Save your context, we're switching to Opus."

### Example 3: Quick Validation Needed
> "Just need simple validation. Save context, switching to Haiku."

## The Economics Reminder

Remember WHY we switch:
- **Opus → Sonnet**: Save 66% for defined work
- **Opus → Haiku**: Save 90% for simple tasks
- **Smart switching**: 2-3x more work for same cost

## Emergency Switches

If human needs to switch immediately:
```
Human: "Emergency switch needed"

Claude: [Saves only critical state in 30 seconds]
- Current MCP task ID
- One-line progress note
- model_phase
```

## The Golden Rule

**Better to spend 2 minutes on clean handoff than 10 minutes reconstructing context**

This is why "Save your context, we're going to switch models" is the perfect phrase - it triggers the full preservation protocol!