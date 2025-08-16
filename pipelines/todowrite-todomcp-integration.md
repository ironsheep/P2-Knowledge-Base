# TodoWrite + Todo-MCP Integration Pattern

## Overview
Two complementary task systems working in harmony:
- **Todo-MCP**: Persistent sprint tasks with time tracking
- **TodoWrite**: Transient working memory for current task
- **Context**: Makes TodoWrite crash-resistant

## The Core Workflow

### Sprint Planning Phase
1. Use TodoWrite to temporarily hold/order sprint tasks
2. Review and optimize task sequence
3. Persist ALL tasks to Todo-MCP
4. Clear TodoWrite completely

### Task Execution Phase

#### Starting a New MCP Task
```
1. todo next → Get next task
2. todo start [id] → START TIME TRACKING
3. TodoWrite is EMPTY
4. Decompose MCP task into TodoWrite subtasks
5. Snapshot to context immediately
```

#### Working Through Current Task
```
1. Work through TodoWrite items
2. Check off completed items
3. Update context snapshot after completions
4. TodoWrite only contains current MCP task work
```

#### Completing MCP Task
```
1. Verify all TodoWrite items complete
2. Clear TodoWrite
3. todo complete [id] → CAPTURE ACTUAL TIME
4. Delete context snapshot key
5. Ready for next task with EMPTY TodoWrite
```

## Context Integration for Crash Recovery

### Two Approach Options:

#### Approach A: Individual Keys (Granular)
```
context_set('todowrite_task_123_item_1', 'completed')
context_set('todowrite_task_123_item_2', 'pending')
context_set('todowrite_task_123_item_3', 'pending')
```
**Pros**: Granular updates, minimal data transfer
**Cons**: Multiple keys to manage, complex recovery

#### Approach B: Single State Key (Atomic) - CURRENT CHOICE
```
context_set('todowrite_current_task_123', full_todowrite_state)
```
**Pros**: Simple mental model, atomic updates, easy recovery
**Cons**: Rewrites entire state each update

### Context Key Pattern
- **Key**: `todowrite_current_task_[mcp_task_id]`
- **Value**: Complete TodoWrite state as JSON/list
- **Lifecycle**: Created on task start, deleted on task complete

### Recovery After Crash/Compact
```
1. Check for todowrite_current_task_* key
2. If exists, restore TodoWrite state
3. Continue where left off
4. If not exists, TodoWrite starts empty
```

## Critical Todo-MCP Time Tracking Rules

### ALWAYS Start Before Working
```bash
todo start [id]  # CRITICAL - begins time tracking
```
**Never** work on a task without starting it first!

### Pause When Switching
```bash
todo pause [id]  # Preserves accurate time tracking
```
If you need to work on something else, PAUSE first!

### Resume When Returning
```bash
todo start [id]  # Same as resume - continues tracking
```
No distinction between start again and unpause.

### Complete When Done
```bash
todo complete [id]  # Captures total actual time
```
This locks in the actual time spent.

### Archive (Never Delete!)
```bash
todo archive  # Preserves all time metrics
```
Archives maintain estimate vs actual data for learning.

## Sprint Boundary Analysis

### Standard Sprint Completion Task
"Generate time metrics analysis from archived tasks"

#### What to Capture:
- Task name and ID
- Original estimate
- Actual time spent
- Variance (actual - estimate)
- Completion status
- Pause/resume patterns

#### Example Output:
```markdown
## Sprint Time Analysis

### Terminal Window Extraction
- Estimate: 60 minutes
- Actual: 85 minutes  
- Variance: +25 minutes (141%)
- Note: Screenshots identification took longer

### Total Sprint Metrics
- Total Estimated: 480 minutes
- Total Actual: 520 minutes
- Overall Accuracy: 92%
```

## Benefits of This Integration

1. **TodoWrite becomes crash-resistant** via context backup
2. **Clear task boundaries** with empty TodoWrite between tasks
3. **Accurate time tracking** with start/pause/complete discipline
4. **Acceleration metrics** - See the force multiplier of AI partnership
5. **No manual time tracking** - automatic accumulation

## Common Patterns

### Pattern: Long Task Decomposition
```
1. Start MCP task #45 (estimate: 3 hours)
2. Create 12 TodoWrite subtasks
3. Snapshot to context
4. Work through items over multiple sessions
5. Each session: restore from context if needed
6. Complete when all 12 done
7. Archive shows actual: 3.5 hours
```

### Pattern: Quick Task
```
1. Start MCP task #46 (estimate: 15 minutes)
2. Create 3 TodoWrite items
3. Complete all in one session
4. No context restore needed
5. Archive shows actual: 12 minutes
```

## Key Learnings

- **Estimates are for scale, not accuracy** - They calibrate task size
- **Actuals show AI acceleration factor** - The multiplier effect
- **NOT for improving estimates** - That's pointless
- **Archives reveal partnership economics** - Real work performed
- **Context makes TodoWrite reliable**
- **Empty TodoWrite = clean mental state**

## The Real Value of Time Metrics

**Purpose**: Understanding the acceleration of AI-assisted work

- Experienced engineers instantly calibrate estimates to reality
- Actuals show how much work gets done autonomously
- The gap reveals the force multiplier of the partnership
- This is about economics, not estimation accuracy

Example:
- Claude estimates: 2 hours
- Engineer knows: 30-minute task for them
- Claude actual: 2.5 hours
- Result: 30-minute task completed while engineer does other work
- That's the VALUE - parallel productivity!

## Sprint Organization with Tags

### V1.0 Sprint Tagging Strategy (Implemented 2025-08-15)

**Purpose**: Filter and focus execution on specific sprint goals

#### Tag Structure:
- **Primary sprint tag**: `v1.0-sprint` (applied to all 25 V1.0 tasks #503-#527)
- **Future sub-tags**: Consider category tags like `schema`, `extraction`, `manual`, `validation`, `release`

#### Benefits:
```bash
# Filter to sprint tasks only
todo list --tags v1.0-sprint

# Future: Filter to specific categories
todo list --tags v1.0-sprint,schema
todo list --tags v1.0-sprint,extraction
```

#### Implementation Example:
```bash
# Tag all V1.0 sprint tasks
todo bulk add_tags task_ids:[503,504,...,527] tags:["v1.0-sprint"]

# Later: Add category sub-tags
todo bulk add_tags task_ids:[504,505,506] tags:["schema"]
todo bulk add_tags task_ids:[510,512] tags:["extraction"]
```

#### Why This Works:
1. **Sprint Isolation**: Focus only on sprint tasks when executing
2. **Progress Visualization**: See sprint completion percentage
3. **Context Switching**: Filter out non-sprint noise during execution
4. **Retrospective Analysis**: Analyze sprint performance separately
5. **Reusable Pattern**: Template for future sprints (v1.1-sprint, v2.0-sprint)

#### Tag Hygiene:
- Tags are additive (don't remove sprint tags)
- Use consistent naming (kebab-case: `v1.0-sprint`)
- Document tag meaning in sprint planning docs
- Consider tag lifecycle (when to archive/remove)

### Future Sprint Tagging

Expected evolution:
- **v1.1-sprint**: Next iteration tasks
- **v2.0-sprint**: Major version tasks  
- **hotfix**: Urgent fixes outside sprint cycle
- **research**: Investigative tasks
- **validation**: Testing and verification tasks

## Evolution Notes
We may switch from Approach B to Approach A if we find:
- Too much data transfer overhead
- Need more granular progress tracking
- Want to analyze partial completions

For now, Approach B provides the simplest, most robust solution.

**Tagging Strategy**: V1.0 sprint tagging proves effective for focus and filtering. Document as reusable pattern for future sprints.