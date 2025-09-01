# Sprint Lifecycle

**Version**: 1.0
**Created**: 2025-08-20
**Status**: Living Document

---

## Overview

This document defines how we execute sprints from inception to completion. Each phase has specific objectives, processes, and deliverables that ensure systematic progress toward our goals.

---

## Sprint Startup Protocol

### 1. Survey Documentation Strategy

**Recommended Approach: Progressive Loading**

When starting a sprint:
1. **First**: Read this sprint-lifecycle.md for complete overview
2. **Then**: Read the NEXT process document you're about to execute
3. **Just-in-time**: Load each process document as you enter that phase

**Why Progressive Loading**:
- Keeps context focused on current work
- Reduces cognitive load
- Documentation stays fresh when needed
- Allows for process updates between phases

**Alternative: Full Pre-load**
- Read ALL process documents at sprint start
- Better for: Experienced practitioners, shorter sprints
- Risk: Information overload, forgetting details by execution time

### 2. Git Checkpoint (if needed)

**Purpose**: Clean boundary before sprint work

```bash
# Check if uncommitted work exists
git status

# If changes exist, create checkpoint
git add .
git commit -m "🔖 CHECKPOINT: Pre-sprint work preserved"
```

### 3. Create Sprint Folder

**When**: BEFORE planning begins (planning needs the folder)

**Naming Convention**:
```
.sprints/[descriptive-name]-sprint-XXX/
```

**Examples**:
- `.sprints/accessibility-discovery-sprint-005/`
- `.sprints/pasm2-manual-sprint-006/`
- `.sprints/code-examples-sprint-007/`

**Why Descriptive Names**:
- Instant recognition of sprint purpose
- Easy navigation through sprint history
- Better than pure numbers for finding past work
- Number suffix maintains chronological order

**Initial Setup**:
```bash
# Create sprint folder with descriptive name
mkdir .sprints/accessibility-discovery-sprint-005

# Create active pointer
echo "Sprint: accessibility-discovery-sprint-005" > tasks/active/current-sprint.md
echo "Status: Planning" >> tasks/active/current-sprint.md

# Planning documents will go here
```

---

## Sprint Phases

### 1. Sprint Initiation

**Trigger**: Knowledge gaps identified or strategic objectives set

**Process**:
1. **Git checkpoint** if uncommitted work exists
2. **Create sprint folder** with descriptive name
3. **Nominate candidates** for sprint inclusion
4. **Review strategic priorities**
5. **Consider dependencies** between items
6. **Form initial sprint scope**

**Deliverables**:
- Sprint folder created
- Candidate list
- Priority rationale
- Initial scope statement

---

### 2. Sprint Planning

**Reference**: See `sprint-planning-methodology.md`

**Summary**:
- Detailed iteration on each candidate
- Extreme resolution achieved
- Model requirements identified
- Advisory guidance documented

**Deliverables**:
- `SPRINT-PLAN.md` with full details
- Model switching strategy
- Execution guidance (advisory)

---

### 3. Task Generation

**Reference**: See `task-generation-process.md` (when available)

**Key Principles**:
- Plan provides advice, not mandates
- Freedom to optimize execution order
- Minimize rework through careful ordering
- Consider model availability

**Considerations**:
- Tag creation for grouping
- Dependency management
- Model batching
- Human availability

**Deliverables**:
- Ordered task list
- Tags/groups defined
- Dependencies mapped
- Model requirements per task

---

### 4. Sprint Execution

**Reference**: See `sprint-execution-process.md`

**Key Activities**:
- Use todo_next for intelligent task selection
- Break tasks into TodoWrite steps
- Defensive context saving at every step
- Document discoveries in SPRINT-PLAN.md
- Handle blockers proactively

**Model Management**:
- Opportunistic execution based on current model
- Filter tasks by model tag
- Minimize switch requests
- Continue working if model auto-switches

**Quality Focus**:
- Prioritize staying alive (check file sizes, use right techniques)
- Same quality as human, more efficient
- Validate thoroughly
- Document all frictions

**Deliverables**:
- Completed work items
- Updated SPRINT-PLAN.md with discoveries
- Archived tasks for analysis
- Progress metrics

---

### 5. Sprint Wrap-up

**Purpose**: Ensure completeness and capture learnings

**Activities**:
1. **Verify Deliverables**
   - Check all items complete
   - Validate quality standards
   - Ensure documentation updated

2. **Update Project State**
   - Update README.md
   - Refresh Operations Dashboard
   - Update master documents
   - Commit changes

3. **Document Learnings**
   - What worked well
   - What was challenging
   - Process improvements
   - Knowledge gained

4. **Metrics & Reporting**
   - Coverage improvements
   - Questions answered
   - Gaps remaining
   - Time invested

5. **Communication** (when applicable)
   - Announce completions
   - Share new capabilities
   - Update stakeholders

**Deliverables**:
- Sprint summary document
- Updated project metrics
- Lessons learned
- Announcement (if warranted)

---

## Cross-Sprint Considerations

### Model Strategy

**Daily Planning**:
- Morning: Opus availability window
- Assess work needing Opus
- Batch Opus work together
- Switch to Sonnet for remainder

**Sprint Planning**:
- Identify model needs per item
- Order to minimize switches
- Document in plan
- Communicate to task generation

### Documentation

**Living Documents**:
- All process docs evolve
- Update immediately when learning
- Don't wait for "perfect"
- Version control captures history

**Sprint Records**:
- Each sprint gets dedicated folder
- Plans, summaries, learnings preserved
- Reference for future sprints
- Build institutional knowledge

### Continuous Improvement

**Sources**:
- Internal experience
- External methodologies (adapted)
- Team feedback
- Execution discoveries

**Process**:
1. Capture insight immediately
2. Update relevant document
3. Apply in next sprint
4. Share with team

---

## Sprint Artifacts

### Required Documents

Per sprint folder (`/.sprints/sprint-XXX/`):
- `SPRINT-PLAN.md` - Detailed plan
- `sprint-summary.md` - Execution summary
- `lessons-learned.md` - Discoveries and improvements
- `metrics.md` - Quantified progress

### Optional Documents
- `blockers-resolutions.md` - How we handled issues
- `model-switching-log.md` - When and why we switched
- `questions-answered.md` - Knowledge gaps filled

---

## Communication Strategy

### Internal (Team)
- Daily progress updates
- Blocker identification
- Discovery sharing
- Process improvements

### External (When Applicable)

**Version Announcements**:
- Significant capability additions
- Major milestone completion
- New resources available

**AI Assistant Updates**:
- New knowledge available
- Improved coverage areas
- Example code accessibility
- Pattern recognition improvements

**Considerations**:
- Version change triggers
- Quick guide of changes
- Region change identification
- Audience-appropriate messaging

---

## Success Metrics

### Sprint Level
- Items completed vs planned
- Questions answered
- Coverage improvement
- Time efficiency

### Project Level
- Knowledge completeness
- Documentation quality
- Process maturity
- Stakeholder satisfaction

---

## Advisory Notes

**Remember**:
- This process guides but doesn't constrain
- Adapt based on sprint needs
- Document adaptations for future reference
- Every sprint improves the process

**Model Wisdom**:
- Beginning of day = Opus window
- Batch by model to reduce switches
- Switches require human interaction
- Plan accordingly

---

*This is a living document. Each sprint should contribute improvements based on experience.*