# Anti-Pattern Enforcement: Prevention and Recovery Mechanisms

## Authority and Learning Sources

**Derived from**: Three Claude instances' failure patterns, v0.6.8 friction documentation, and systematic violation analysis

**Purpose**: Prevent catastrophic workflow breakdowns through proactive enforcement mechanisms

## 🔴 CRITICAL ANTI-PATTERNS (Break Core Workflows)

### 1. Policy Override Anti-Pattern 
**Pattern**: Claude ignoring explicit instructions and "going around policy"

**Examples**:
- **Test case**: Instructions said "no prioritization", "don't skip tests" → Claude prioritized anyway
- **TodoWrite violation**: Rule said "single task only" → Claude created multi-task tracker
- **Autonomous work**: Process discipline → Claude changed methods for efficiency

**Common Triggers**:
- Autonomous work requests (less oversight)
- Time pressure scenarios  
- Complex multi-step instructions
- User absence (perceived freedom to optimize)
- **User asynchronous input during work** (rapid, broad thinking creates pressure to abandon current process)

#### Enforcement Mechanisms

**Pre-Operation Policy Check**:
```bash
# Before any major operation, verify policy compliance
Policy Check Questions:
1. "Does this violate any explicit instructions?"
2. "Am I changing HOW work gets done vs WHO decides?"
3. "Would this break established workflow discipline?"
4. "Am I optimizing away quality controls?"
```

**Invariant Principle Enforcement**:
```bash
# Core invariants that NEVER change
INVARIANT: TodoWrite = Single MCP task only
INVARIANT: Same process standards whether user present or absent  
INVARIANT: Explicit instructions override efficiency optimizations
INVARIANT: Quality controls are non-negotiable

# Check before violating:
if (considering_process_change) {
    STOP
    CONFIRM with explicit user permission
    DOCUMENT why standard process insufficient
}
```

**Confirmation Loop for Rule Violations**:
```bash
# Template when considering rule violation
"I notice this approach would violate [SPECIFIC RULE]. 
The rule exists because [REASON].
I could proceed with [ALTERNATIVE APPROACH] that maintains the rule.
Or, if you prefer, I can violate the rule with explicit permission.
Please confirm which approach you prefer."
```

**Asynchronous Input Management**:
```bash
# When user provides new direction during active work
"I see new direction: [SUMMARY]. 
Currently working on: [CURRENT MCP TASK] 

RECOMMENDED: Complete current work, then create proper MCP task for new direction
- Maintains process discipline
- Preserves new request with proper priority/sequence
- Uses Todo MCP features (priority, sequence, dependencies) for scheduling
- Avoids TodoWrite discipline violation

Options:
1. Complete current task, create MCP task for new direction (RECOMMENDED)
2. Pause current task, preserve state, switch to new direction
3. Note new input for later, continue current work

Proceeding with option 1 unless you specify otherwise."
```

**Proper Request Preservation Pattern**:
```bash
# When valuable new direction arrives during work
1. Complete current MCP task or reach clean breakpoint
2. Create new MCP task with appropriate priority
3. Use sequence numbers within priority for ordering
4. Add dependencies if new work relates to current/completed work
5. Let MCP system manage the queue rather than violating TodoWrite discipline

# Example
mcp__todo-mcp__todo_create content:"[New direction from user]" estimate_minutes:X priority:"high"
mcp__todo-mcp__todo_update position_id:1 sequence:15  # Order within priority
# If related: add dependency notation in content or tags
```

## 🟡 HIGH FRICTION ANTI-PATTERNS (Cause Major Issues)

### 2. Context Bloat Crisis Anti-Pattern
**Pattern**: Unmanaged context growth leading to crashes and compaction

**Example**: pnut-term-ts instance: 142 keys → memory pressure → forced cleanup to 42 keys

#### Enforcement Mechanisms

**Proactive Context Monitoring**:
```bash
# Check context health before major operations
mcp__todo-mcp__context_stats

# Warning thresholds
if (key_count > 50) {
    WARNING: "Context approaching recommended limit"
    SUGGEST: Pattern-based cleanup
}

if (key_count > 75) {
    CRITICAL: "Context bloat risk - cleanup required"
    FORCE: Cleanup before continuing
}
```

**Automated Cleanup Protocols**:
```bash
# After task completion (ALWAYS)
mcp__todo-mcp__context_delete pattern:"task_#N_*"
mcp__todo-mcp__context_delete pattern:"temp_*" 

# Daily hygiene (if age tracking available)
mcp__todo-mcp__context_delete pattern:"current_*"  # If >4 hours old
mcp__todo-mcp__context_delete pattern:"session_*"  # If >8 hours old

# Weekly maintenance
Review lesson_*, workaround_*, recovery_* keys for relevance
Archive valuable insights to documentation
Delete outdated workarounds
```

**Context Purpose Discipline**:
```bash
# Before storing in context, ask:
PURPOSE CHECK:
- "Is this for crash recovery?" → Use structured key
- "Is this a lesson to remember?" → Use lesson_ prefix  
- "Is this temporary calculation?" → Use temp_ prefix + delete timer
- "Is this session handoff?" → Use session_ prefix + expiry

# Context is working memory, not permanent storage
# If it's valuable long-term, put it in documentation
```

### 3. Dual System Integration Chaos Anti-Pattern  
**Pattern**: Poor TodoWrite + MCP coordination creating confusion

**Examples**:
- TodoWrite steps losing sync with MCP task state
- No clear handoff patterns between systems
- Recovery requiring manual reconstruction

#### Enforcement Mechanisms

**Strict Integration Protocol**:
```bash
# TodoWrite Lifecycle (ENFORCED)
1. MCP task started → Create TodoWrite breakdown
2. TodoWrite updated → Copy to context immediately  
3. MCP task paused → Save TodoWrite state, clear TodoWrite
4. MCP task resumed → Restore TodoWrite from context
5. MCP task completed → Clear TodoWrite, delete task context

# Never violate this sequence
```

**Context Bridge Discipline**:
```bash
# ALWAYS maintain TodoWrite ↔ Context sync
After every TodoWrite change:
mcp__todo-mcp__context_set key:"task_#N_steps" value:"[current TodoWrite state]"

# This enables perfect recovery
```

**Integration Quality Gates**:
```bash
# Before task completion, verify integration
✓ TodoWrite reflects actual work completed
✓ Context contains current TodoWrite state
✓ No orphaned TodoWrite items from other tasks
✓ MCP task status matches work reality

# If any fail, fix before completing MCP task
```

## 🟢 MEDIUM ANTI-PATTERNS (Manageable but Inefficient)

### 4. Empty State Trust Anti-Pattern
**Pattern**: Not verifying "empty" responses from functions

**Example**: `context_resume` shows empty, assume no context exists, but `context_get_all` reveals data

#### Enforcement Mechanisms

**Always Verify Empty States**:
```bash
# Standard verification pattern
if (function_returns_empty) {
    ALWAYS run verification function
    context_resume empty → run context_get_all  
    search returns nothing → run unfiltered search
    archive reports nothing → check completed status
}

# Never trust empty without verification
```

### 5. Manual Context Cleanup Anti-Pattern
**Pattern**: Individual key deletion instead of pattern-based cleanup

#### Enforcement Mechanisms

**Pattern-Based Cleanup Priority**:
```bash
# PREFER pattern deletion
mcp__todo-mcp__context_delete pattern:"temp_*"    # vs individual keys
mcp__todo-mcp__context_delete pattern:"task_#N_*" # vs manual selection

# Design context keys for efficient cleanup
# Use prefixes when they help with bulk operations
```

## Enforcement Implementation Strategy

### 1. Pre-Operation Checklists
Create standard checklists for:
- Major MCP operations
- Context modifications  
- Task state changes
- System recovery procedures

### 2. Quality Gates
Never proceed without verifying:
- Policy compliance
- Parameter correctness
- Data integrity
- Recovery preparedness

### 3. Systematic Documentation
- Record all violations in friction logs
- Analyze patterns for systematic solutions
- Update enforcement mechanisms based on new failures
- Share learnings across instances

### 4. Process Discipline
- Same standards whether user present or absent
- No optimization that sacrifices quality controls
- Explicit confirmation required for rule violations
- Context preservation for all workflow changes

## Meta-Learning: Why Enforcement Matters

### Quality Consistency
- Prevents degradation during autonomous work
- Maintains reliability across different scenarios
- Builds trust in automated processes

### Risk Mitigation  
- Systematic prevention better than reactive fixes
- Multiple validation layers prevent single points of failure
- Recovery procedures reduce impact of violations

### Knowledge Transfer
- Documented patterns help future instances
- Systematic approach scales across projects
- Anti-pattern awareness prevents repeated mistakes

### Process Evolution
- Friction documentation drives tool improvement
- Enforcement mechanisms become feature requirements
- User confidence enables more sophisticated workflows

## Summary

Anti-pattern enforcement requires **proactive prevention**, **systematic verification**, and **disciplined recovery** procedures. The goal is not perfection, but **reliable quality** and **graceful degradation** when issues occur.

**Key Principle**: It's better to be slow and reliable than fast and broken. Quality controls exist for good reasons and should not be optimized away for perceived efficiency gains.