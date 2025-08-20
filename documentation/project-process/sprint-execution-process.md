# Sprint Execution Process

**Version**: 1.0
**Created**: 2025-08-20
**Status**: Living Document

---

## Overview

Sprint execution transforms our carefully generated tasks into completed deliverables. This process emphasizes quality checkpoints, systematic progression, and clean commit boundaries.

---

## Execution Phases

### Phase 1: Pre-Sprint Checkpoint

**Purpose**: Create clean starting point for sprint work

**Git Checkpoint Protocol**:
```bash
# 1. Check current status
git status

# 2. Add all pending changes
git add .

# 3. Create checkpoint commit
git commit -m "🔖 CHECKPOINT: Pre-Sprint 005 - All work preserved before sprint execution"

# 4. Optionally tag for easy reference
git tag checkpoint-sprint-005-start
```

**Why**: 
- Clean slate for sprint work
- Easy rollback if needed
- Clear boundary between exploratory and sprint work
- Historical marker for sprint beginning

**Note**: We haven't committed in a while, so Sprint 005 will start with this checkpoint.

---

### Phase 2: Task Execution

**Starting Work**:
```bash
# 1. Verify checkpoint complete
git log -1

# 2. Load tasks from MCP
mcp__todo-mcp__todo_list

# 3. Activate sprint tracking
echo "Active Sprint: 005" > tasks/active/current-sprint.md
echo "Started: $(date)" >> tasks/active/current-sprint.md

# 4. Begin first task
mcp__todo-mcp__todo_start position_id:1
```

**During Execution**:

### Working Through Tasks

**Task Lifecycle**:
1. **Start**: Mark task as in_progress
2. **Execute**: Follow the exhaustive description
3. **Validate**: Check against success criteria
4. **Complete**: Mark done, move to next

**Quality Checks Per Task**:
- Did I create all specified deliverables?
- Are file paths correct?
- Does output meet validation criteria?
- Is the work complete and atomic?

### Progress Tracking

**Continuous Updates**:
- Update task status in MCP immediately
- Document discoveries in sprint folder
- Note any blockers or issues
- Capture lessons learned in real-time

**If Context Lost** (compaction/clear):
```bash
# Recovery sequence
mcp__todo-mcp__context_resume
cat tasks/active/current-sprint.md
mcp__todo-mcp__todo_list
# Resume from last in_progress task
```

### Model Switching

**When Switch Required**:
1. Complete all current model tasks
2. Ensure work is saved
3. Request model switch from user
4. Resume with new model's task batch

**Switch Communication**:
```
All Sonnet tasks complete. Ready to switch to Opus 4.1 for creative analysis tasks.
Current progress: 8/12 tasks complete
Next: DeSilva voice analysis (requires Opus)
Shall we switch models now?
```

---

### Phase 3: Quality Certification

**Before Sprint Completion**:

**Verification Checklist**:
- [ ] All tasks marked complete in MCP
- [ ] All deliverables exist at specified paths
- [ ] Validation criteria met for each task
- [ ] No uncommitted work remains
- [ ] Sprint documents updated

**Quality Commands**:
```bash
# Check all deliverables exist
ls -la [each deliverable path]

# Verify no uncommitted changes except sprint work
git status

# Review what was created/modified
git diff --stat

# Check task completion
mcp__todo-mcp__todo_list status:completed
```

---

### Phase 4: Sprint Completion & Analysis

**Archive Completed Tasks**:
```bash
# Archive all completed tasks for analysis
mcp__todo-mcp__todo_archive

# Copy archive to sprint folder
cp [archive_location] .sprints/sprint-005/task-archive.json

# Analyze estimates vs actuals
# Document learnings about estimation accuracy
```

### Phase 5: Sprint Commit

**Final Commit Protocol**:

```bash
# 1. Verify all work complete
git status

# 2. Add all sprint work
git add .

# 3. Create detailed sprint commit
git commit -m "✅ SPRINT 005 COMPLETE: Documentation Accessibility & Discovery

Completed Items:
- AD-007: PASM2 Master Instruction Table created
- AD-001: Instruction Completion Matrix established  
- AD-003: DeSilva PDF extraction and analysis
- AD-013: 550+ code examples cataloged
- Audit Bundle: Cross-ingestion reconciliation

Key Deliverables:
- Master instruction table with gap tracking
- Completion matrix with source attribution
- DeSilva voice analysis and P2 guide framework
- Organized code example catalog
- Consolidated knowledge state

Metrics:
- Coverage improved from X% to Y%
- N questions answered with citations
- M new gaps identified for tracking

See .sprints/sprint-005/ for complete documentation"

# 4. Tag the completion
git tag sprint-005-complete
```

---

## Execution Best Practices

### 1. Atomic Progress
- Complete entire tasks, not partial work
- Each task should leave system in valid state
- Commit readiness after each task

### 2. Documentation Discipline
- Update sprint docs as you work
- Capture discoveries immediately
- Document blockers and resolutions
- Note process improvements

### 3. Quality Focus
- Follow task descriptions exactly
- Validate against success criteria
- Don't skip verification steps
- Fix issues before moving on

### 4. Model Efficiency
- Batch all work for current model
- Complete model's work before switching
- Communicate switch needs clearly
- Minimize total switches

---

## Common Execution Patterns

### Pattern: Discovery During Execution
```markdown
When you discover new information:
1. Complete current task
2. Add discovery to SPRINT-PLAN.md (Discoveries section)
3. Assess if it changes upcoming tasks
4. Create new tasks if needed (with rationale)
5. Document in "plan evolution" why changes needed
6. Continue execution
```

### Pattern: Task Priority Override
```markdown
When you need different execution order:
1. Pause current task (stops time accumulation)
2. If same priority: Re-sequence
3. If different priority: Add dependency
4. Document why in sprint plan
5. Execute higher priority work
6. Return to paused task
```

### Pattern: Validation Best Practices
```markdown
Prioritize staying alive:
1. Check file size before loading (avoid crashes)
2. Use appropriate ingestion technique
3. Verify paths exist before operations
4. Test with small samples first if uncertain
5. Document any crash-avoidance discoveries
```

### Pattern: Blocked Task
```markdown
When blocked:
1. Document blocker clearly
2. Mark task as paused with reason
3. Skip to next non-dependent task
4. Return when unblocked
5. Document resolution
```

### Pattern: Quality Issue Found
```markdown
When quality issue discovered:
1. Stop current task
2. Fix the issue
3. Verify fix doesn't break other work
4. Document what happened and why
5. Resume task execution
```

---

## Integration Points

### With Task Generation
- Receives ordered task list
- Follows model grouping
- Uses priority assignments
- Respects advisory ordering

### With MCP Todo
- Real-time status updates
- Progress tracking
- Blocker documentation
- Completion recording

### With Git
- Checkpoint before sprint
- Clean commit after sprint
- Tagged milestones
- Clear history

### With Sprint Documents
- Living updates during execution
- Discovery capture
- Metrics collection
- Retrospective preparation

---

## Emergency Procedures

### Context Loss (Compaction)
1. Run: `mcp__todo-mcp__context_resume`
2. Check: `tasks/active/current-sprint.md`
3. Review: Current MCP tasks
4. Resume: From last in_progress

### Git Issues
1. Always: `git status` first
2. If merge conflicts: Resolve favoring sprint work
3. If accidental commit: Use checkpoint tag to reset
4. If lost work: Check git reflog

### Task Confusion
1. Re-read task description completely
2. Check sprint plan for context
3. Verify file paths exist
4. Ask user for clarification if needed

---

## Success Metrics

### Execution Quality
- Tasks completed as described
- No rework required
- Quality criteria met
- Clean git history

### Execution Efficiency  
- Minimal model switches
- No blocked time
- Smooth progression
- Clear documentation

### Sprint Success
- All planned items delivered
- Discoveries documented
- Metrics captured
- Knowledge advanced

---

## Post-Sprint Activities

After sprint commit:

1. **Create Sprint Summary**
   - What was accomplished
   - Metrics and measurements
   - Key discoveries

2. **Write Retrospective**
   - What went well
   - What was challenging  
   - Process improvements

3. **Update Project State**
   - Operations Dashboard
   - README if needed
   - Master documents

4. **Archive Sprint**
   - Move to completed state
   - Update active pointer
   - Prepare for next sprint

---

*This is a living document. Each sprint execution should contribute lessons and improvements.*