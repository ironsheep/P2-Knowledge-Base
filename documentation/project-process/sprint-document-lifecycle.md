# Sprint Document Lifecycle

**Version**: 1.0
**Created**: 2025-08-20
**Status**: Living Document
**Source Note**: Adapted from external lifecycle pattern, merged with our established practices

---

## Overview

Sprint documentation evolves through the sprint lifecycle while maintaining both working state and historical record. This pattern ensures compaction safety, progress visibility, and knowledge preservation.

---

## Document Structure

### Sprint Folder Organization

```
.sprints/sprint-XXX/
├── SPRINT-PLAN.md              # Detailed plan (living document)
├── sprint-summary.md           # Execution summary (created at completion)
├── retrospective.md            # Lessons learned
├── metrics.md                  # Quantified progress
└── [other deliverables]        # Item-specific outputs

tasks/active/                   # Compaction-safe pointer
└── current-sprint.md          # Link to active sprint status
```

### Active Work Tracking

**During Sprint Execution**:
- Primary work happens in sprint folder
- `tasks/active/current-sprint.md` points to active sprint
- Survives compaction for quick recovery
- Contains sprint ID and quick status

---

## Lifecycle Phases

### Phase 1: Sprint Planning

**Location**: `.sprints/sprint-XXX/SPRINT-PLAN.md`

**Characteristics**:
- Created during detailed planning sessions
- Living document - can be updated during execution
- Contains all items, deliverables, and guidance
- Model strategy documented

**Our Approach**:
- Plan provides advisory guidance, not mandates
- Extreme resolution achieved during planning
- Updates captured as we learn

### Phase 2: Sprint Activation

**Action**: Create active sprint pointer

```bash
# Create compaction-safe pointer
echo "Active Sprint: 005" > tasks/active/current-sprint.md
echo "Status: In Progress" >> tasks/active/current-sprint.md
echo "Started: 2025-08-20" >> tasks/active/current-sprint.md
echo "See: .sprints/sprint-005/" >> tasks/active/current-sprint.md
```

**Purpose**:
- Quick recovery after compaction
- Clear indication of current work
- Simple status check location

### Phase 3: Active Execution

**Primary Location**: `.sprints/sprint-XXX/`

**Working Documents**:
- SPRINT-PLAN.md gets updated with discoveries
- Item-specific outputs created as work progresses
- Progress tracked via MCP todo system

**Compaction Recovery**:
```bash
# After compaction, Claude runs:
mcp__todo-mcp__context_resume
cat tasks/active/current-sprint.md
# Then navigates to active sprint folder
```

### Phase 4: Sprint Completion

**Actions**:
1. Create `sprint-summary.md` with outcomes
2. Create `retrospective.md` with lessons
3. Create `metrics.md` with measurements
4. Update `tasks/active/current-sprint.md` to "Completed"
5. Update Operations Dashboard
6. Update README if needed

**Deliverables Preserved**:
- Original plan (with updates showing evolution)
- Completion summary
- Retrospective insights
- All work products

### Phase 5: Archive State

**Location**: `.sprints/sprint-XXX/` (permanent home)

**Contains**:
- Complete sprint history
- All deliverables
- Lessons for future reference
- Metrics for tracking progress

**Usage**:
- Reference for future sprints
- Learning from past decisions
- Building institutional knowledge

---

## Key Patterns

### Compaction Safety

**The Problem**: Context loss during conversation compaction

**Our Solution**:
- `tasks/active/` survives as working directory
- Quick pointer to current sprint
- Context keys in MCP for critical state
- Clear recovery path documented

### Living Documentation

**Philosophy**: Documents evolve with understanding

**Implementation**:
- Plans update during execution
- Discoveries recorded immediately
- Retrospectives capture changes
- Version control shows evolution

### Progress Tracking

**Multiple Layers**:
1. MCP todo for task-level tracking
2. Sprint documents for narrative progress
3. Context keys for session continuity
4. Git commits for version history

---

## Integration Points

### With MCP Todo System
- Sprint items become MCP tasks
- Progress tracked in todo system
- Context keys preserve state
- Completion triggers document updates

### With Git
- Each sprint completion can be tagged
- Significant milestones get releases
- Commit messages reference sprint IDs
- History shows sprint progression

### With Operations Dashboard
- Sprint status reflected
- Metrics aggregated
- Progress visualized
- Links to active work

---

## Quick Reference Commands

### Start Sprint
```bash
# Create sprint folder
mkdir .sprints/sprint-006

# Create plan
# [Create SPRINT-PLAN.md with details]

# Activate sprint
echo "Active Sprint: 006" > tasks/active/current-sprint.md

# Create MCP tasks
mcp__todo-mcp__todo_create content:"Sprint 006: [Name]" 
```

### During Sprint
```bash
# Check status
cat tasks/active/current-sprint.md

# Update progress
# [Update SPRINT-PLAN.md with discoveries]

# Track via MCP
mcp__todo-mcp__todo_list
```

### Complete Sprint
```bash
# Create summary documents
# [Create sprint-summary.md, retrospective.md, metrics.md]

# Mark complete
echo "Status: Completed" >> tasks/active/current-sprint.md

# Update dashboard
# [Update operations dashboard]
```

### After Compaction
```bash
# Recover context
mcp__todo-mcp__context_resume

# Find active sprint
cat tasks/active/current-sprint.md

# Resume work
# [Navigate to indicated sprint folder]
```

---

## Advantages of This Approach

1. **Simplicity**: No complex file copying
2. **Flexibility**: Living documents can evolve
3. **Safety**: Compaction-resistant design
4. **Clarity**: Clear current vs archived state
5. **Integration**: Works with our tools (MCP, Git)
6. **Learning**: Preserves history and insights

---

## Differences from Source Pattern

**What We Took**:
- Compaction safety concept
- Working vs archive states
- Completion artifacts

**What We Adapted**:
- Simplified to single location (.sprints/)
- Living documents instead of frozen
- Integrated with MCP todo
- Added retrospectives throughout

**What We Left**:
- Complex file copying workflow
- Rigid separation of DOCs/ and tasks/
- "Never modify" philosophy
- Prescriptive naming conventions

---

*This is a living document. Updates based on actual sprint execution experience.*