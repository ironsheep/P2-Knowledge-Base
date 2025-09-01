# Sprint Planning Methodology

**Version**: 1.0
**Created**: 2025-08-20
**Status**: Living Document

---

## Overview

Sprint planning is an iterative process that transforms initial ideas into detailed, actionable plans. This methodology captures our approach to systematic planning that ensures comprehensive coverage while maintaining flexibility.

---

## Planning Phases

### Phase 1: Candidate Identification

**Purpose**: Identify work items that could be included in the sprint.

**Process**:
1. Review outstanding questions and gaps
2. Consider strategic priorities
3. Identify related work that could be bundled
4. Create initial list of candidates

**Output**: List of potential sprint items with brief descriptions

---

### Phase 2: Detailed Iteration

**Purpose**: Achieve extreme resolution on each sprint item.

**Process**:
1. **Present each item** for review
2. **Gather observations** from planning participants
3. **Ask clarifying questions** about scope and intent
4. **Refine and expand** based on feedback
5. **Repeat** until no questions remain

**Key Principles**:
- Don't assume - ask for clarification
- Capture all details during discussion
- Record decisions and rationale
- Build rich context for execution

**Example Questions to Address**:
- What specific files/documents are involved?
- What's the expected output format?
- Are there dependencies between items?
- What model is optimal for this work?
- What could go wrong?

---

### Phase 3: Plan Documentation

**Purpose**: Capture all planning decisions in permanent form.

**Document Structure**:
```markdown
# Sprint [ID]: [Name]

## Overview
- Purpose and objectives
- Key deliverables
- Model strategy

## Sprint Items
### Item 1: [ID] - [Name]
- Purpose
- Deliverables
- Process/Phases
- Location
- Model recommendation
- Advisory notes

## Execution Guidance
- Model optimization
- Task generation suggestions
- Dependencies

## Success Criteria
```

**Key Elements**:
- Every detail from planning discussion
- Clear deliverables per item
- File locations and structure
- Model requirements
- Advisory guidance (not mandates)

---

## Planning Best Practices

### 1. Extreme Resolution
- Push for complete clarity on each item
- Don't leave ambiguity for execution phase
- Document all assumptions explicitly

### 2. Living Documentation
- Plans can be updated during execution
- Capture learnings immediately
- Reflect changes back to methodology

### 3. Advisory vs Mandatory
- **Plan provides advice, not requirements**
- Task generation has freedom to optimize
- Suggest opportunities, don't mandate approach
- Document as "consider" not "must"

### 4. Model Awareness
- Identify which model each item needs
- Plan to minimize model switches
- Batch work by model when possible
- Note: switches require human interaction

### 5. Historical Learning
- Review previous sprint plans
- Learn from directory structures used
- Understand file naming patterns
- Build on established conventions

---

## Interaction Protocol

### Planning Session Flow
1. **Start**: "Let's review the sprint plan section by section"
2. **Per Section**:
   - Present current understanding
   - Ask: "Do you have observations?"
   - Ask: "Do I have questions?"
   - Refine based on feedback
   - Move to next when complete
3. **Complete**: "We have no remaining questions"

### Question Handling
- Planning participants can ask questions at any time
- No question is too small during planning
- Better to over-specify than under-specify
- Capture rationale for decisions

---

## Documentation Locations

**Sprint Plans**: `/.sprints/sprint-[number]/SPRINT-PLAN.md`
**Process Docs**: `/documentation/project-process/`
**Inputs**: `/documentation/project-process/inputs/`

---

## Relationship to Other Processes

This planning methodology feeds into:
- **Task Generation Process**: Receives detailed plan, creates tasks
- **Sprint Execution Process**: Uses plan as reference
- **Sprint Wrap-up Process**: Compares outcomes to plan

---

## Continuous Improvement

### After Each Sprint
1. Review what worked in planning
2. Identify what was missing
3. Update this methodology
4. Share learnings

### Sources of Improvement
- Internal experience
- External methodologies (studied and adapted)
- Team feedback
- Execution discoveries

---

## Key Insights

**From Sprint 005 Planning**:
- Items often have hidden complexity
- Model switching strategy crucial
- Retroactive audits valuable
- Human review cycles important
- Source attribution essential

**General Principles**:
- Plans guide but don't constrain
- Freedom at execution preserves agility
- Rich plans enable better execution
- Historical context prevents repetition

---

*This is a living document. Each sprint planning session should contribute improvements.*