# Process Augmentation Methodology

**Version**: 1.0
**Created**: 2025-08-20
**Status**: Living Document

---

## Overview

How we learn from other Claude instances and external methodologies while maintaining our unique project needs. External sources inform but don't drive our process.

---

## Core Philosophy

### Principles
1. **We own our process** - External sources are advisory
2. **Pick and choose** - Take what improves, leave what doesn't
3. **Adapt don't adopt** - Customize for our context
4. **Document rationale** - Why we took or left each element

### Key Insight
"The other instances don't drive our process, they help us make our process better"

---

## Augmentation Workflow

### 1. Input Collection

**Location**: `/documentation/project-process/inputs/`

**Sources**:
- Other Claude instance methodologies
- Industry best practices
- Team member contributions
- External frameworks

**Protocol**:
1. Save external documents to inputs folder
2. Don't apply immediately
3. Review and assess first
4. Document source and date

### 2. Assessment Process

**For each input document**:

#### Step 1: Study
- Read completely
- Understand context it was created for
- Identify core concepts
- Note unique insights

#### Step 2: Evaluate
Questions to ask:
- What problems does this solve?
- Do we have these problems?
- How does this fit our project?
- What would need adaptation?

#### Step 3: Extract
- Pull relevant concepts
- Adapt terminology to ours
- Adjust for our context
- Maintain attribution

### 3. Integration Patterns

#### Pattern A: New Process
When we don't have an existing process:
1. Extract applicable elements
2. Adapt to our terminology
3. Customize for our needs
4. Create our version
5. Archive source

#### Pattern B: Process Enhancement
When we have an existing process:
1. Compare approaches
2. Identify improvements
3. Merge best elements
4. Update our document
5. Document what changed
6. Archive source

#### Pattern C: Validation Only
When source confirms our approach:
1. Note validation in our doc
2. Add "validated by" citation
3. Archive source
4. Continue as is

### 4. Documentation

**In our process docs**:
```markdown
## Methodology Notes
- Originally inspired by: [source]
- Adapted on: [date]
- Key adaptations:
  - Changed X to fit our Y
  - Added Z for our needs
  - Removed A as not applicable
```

**In archive**:
- Keep original documents
- Add notes on what we took
- Record why we left other parts
- Date of review

---

## Practical Examples

### Example 1: Task Generation Process
**Scenario**: Found task generation doc from another instance

**Assessment**:
- They use strict priority ordering
- We need model-aware ordering
- They have single owner
- We have human-AI collaboration

**Integration**:
- Take: Rework prevention concepts
- Adapt: Add model switching awareness
- Leave: Strict priority (we batch by model)
- Add: Human availability consideration

### Example 2: Sprint Planning
**Scenario**: Industry standard sprint planning

**Assessment**:
- Fixed 2-week sprints
- Story points estimation
- Daily standups
- Retrospectives

**Integration**:
- Adapt: Variable sprint length for our needs
- Take: Retrospective concept as lessons learned
- Leave: Story points (use our estimation)
- Modify: Standups → progress documentation

---

## Quality Criteria

### What makes external input valuable?
- Solves a problem we have
- Improves efficiency
- Adds missing perspective
- Validates our approach
- Provides new tools/techniques

### What suggests we should skip it?
- Designed for different context
- Adds complexity without value
- Conflicts with our principles
- Requires tools we don't have
- Over-engineers our needs

---

## Archive Management

### Structure
```
/documentation/project-process/inputs/
  archived/
    [date]-[source]-[status].md
    notes/
      [date]-[source]-integration-notes.md
```

### Status Labels
- `integrated` - Merged into our process
- `reviewed` - Assessed but not used
- `pending` - Awaiting review
- `reference` - Keep for reference only

### Integration Notes Template
```markdown
# Integration Notes: [Source Document]

**Date Reviewed**: 
**Reviewer**: 
**Source**: 
**Status**: 

## What we took:
- 

## What we adapted:
- 

## What we left:
- 

## Why:
```

---

## Continuous Improvement

### Regular Review
- Check inputs folder weekly
- Process pending items
- Archive processed items
- Update our processes

### Learning Capture
- Document why adaptations worked
- Note what didn't work
- Share insights with team
- Build institutional knowledge

### Success Metrics
- Process improvements implemented
- Time saved through better methods
- Problems solved by new approaches
- Team satisfaction with processes

---

## Key Reminders

**Our Context is Unique**:
- P2 documentation project
- AI-human collaboration
- Model switching requirements
- Living document philosophy

**Freedom to Choose**:
- Not everything applies to us
- We can say no to good ideas
- Our needs drive decisions
- Simplicity often wins

**Attribution Matters**:
- Credit sources
- Document adaptations
- Explain rationale
- Build on others' work respectfully

---

*This is a living document. As we process more external inputs, we refine our approach.*