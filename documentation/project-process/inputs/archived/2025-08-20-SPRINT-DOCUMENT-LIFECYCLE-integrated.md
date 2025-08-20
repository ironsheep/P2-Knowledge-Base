# Sprint Document Lifecycle

## Overview
Sprint documentation moves through specific locations as it transitions from planning to active work to completion.

## Document Flow Pattern

### 1. Sprint Planning Phase
**Location**: `DOCs/project-sprints/sprint-X/`
- Initial sprint plan created here
- Reference documentation stays here
- Original planning documents remain untouched

### 2. Sprint Start (Active Work)
**Action**: Copy sprint plan to `tasks/`
- `cp DOCs/project-sprints/sprint-1/SPRINT_1_PLAN.md tasks/SPRINT_1_ACTIVE.md`
- Working copy in tasks/ gets updated during implementation
- Progress tracking happens in tasks/ version
- Daily updates and discoveries recorded here

### 3. During Sprint (Daily Work)
**Location**: `tasks/`
- Active sprint documents live here during work
- Updated with: completed items, blockers, discoveries
- New findings documented as they occur
- Test results and implementation notes added
- This is the "working copy" that gets compacted/reloaded

### 4. Sprint Completion
**Action**: Move completed sprint docs back to archive
1. Final update to tasks/ version with completion status
2. Copy back to sprints folder with completion suffix:
   - `cp tasks/SPRINT_1_ACTIVE.md DOCs/project-sprints/sprint-1/SPRINT_1_COMPLETED.md`
3. Add retrospective document to sprint folder
4. Clean up tasks/ folder for next sprint

### 5. Sprint Archive (Post-Completion)
**Location**: `DOCs/project-sprints/sprint-X/`
- Contains both original plan AND completed version
- Retrospective and lessons learned
- Becomes reference for future sprints
- Never modified after sprint closes

## File Naming Convention

```
DOCs/project-sprints/sprint-1/
├── SPRINT_1_PLAN.md           # Original plan (never modified)
├── SPRINT_1_COMPLETED.md      # Final state from tasks/
├── SPRINT_1_RETROSPECTIVE.md  # Post-sprint analysis
└── SPRINT_1_DELIVERABLES.md   # What was actually delivered

tasks/ (during active sprint)
├── SPRINT_1_ACTIVE.md         # Working copy (daily updates)
├── SPRINT_1_PROGRESS.md       # Progress tracking
└── SPRINT_1_BLOCKERS.md       # Current issues/blockers
```

## Why This Pattern?

1. **Separation of Concerns**:
   - `DOCs/` = permanent record, documentation
   - `tasks/` = active workspace, ephemeral

2. **Compaction Safety**:
   - Active work in tasks/ survives compaction
   - Can quickly resume by reading tasks/ files
   - "Show me tasks/SPRINT_1_ACTIVE.md" restores context

3. **Historical Record**:
   - Original plan preserved for comparison
   - Completed version shows what actually happened
   - Retrospective captures lessons learned

4. **Clean Workspace**:
   - tasks/ stays focused on current work
   - Completed sprints don't clutter active workspace
   - Clear signal of what's active vs archived

## Commands for Sprint Transitions

### Starting a Sprint
```bash
# Copy sprint plan to active workspace
cp DOCs/project-sprints/sprint-2/SPRINT_2_PLAN.md tasks/SPRINT_2_ACTIVE.md
echo "Sprint 2 started: $(date)" >> tasks/SPRINT_2_ACTIVE.md
```

### Ending a Sprint
```bash
# Mark completion in active document
echo "Sprint completed: $(date)" >> tasks/SPRINT_2_ACTIVE.md

# Copy back to archive with completion status
cp tasks/SPRINT_2_ACTIVE.md DOCs/project-sprints/sprint-2/SPRINT_2_COMPLETED.md

# Clean up tasks folder
rm tasks/SPRINT_2_*.md
```

### Quick Context Recovery (after compaction)
```bash
# Claude command after compaction:
"Show me all files in tasks/ that start with SPRINT"
"Read tasks/SPRINT_2_ACTIVE.md"
```

## Integration with MCP Todo System

- Sprint-level tasks in MCP (persistent across sessions)
- Implementation details in tasks/ documents
- Progress updates flow: tasks/ docs → MCP task updates → sprint completion

This pattern ensures smooth workflow during active development while maintaining clean historical records for future reference.