# Sprint Execution Methodology

## The Problem We're Solving
Context switching kills productivity. When you pick up a task after days/weeks, you shouldn't need to:
- Re-research what the task was about
- Figure out where to find resources  
- Rediscover the approach you planned
- Ask questions that were already answered

## Our Solution: Three-Phase Approach

### Phase 1: Exhaustive Sprint Planning
**Goal**: Eliminate all ambiguity before work begins

**Process**:
1. **Sprint Identification**: Define what each sprint accomplishes
2. **Dependency Mapping**: Understand what blocks/enables each sprint  
3. **Action Brainstorming**: Identify all possible actions within the sprint
4. **Interactive Refinement**: Discuss, challenge, refine until no questions remain

**Output**: Crystal-clear understanding of sprint scope and approach

**Quality Gate**: Can explain the sprint to someone else without questions

---

### Phase 2: Detailed MCP Generation  
**Goal**: Create complete execution context for each sprint

**Process**:
1. **Convert Planning into MCPs**: Transform understanding into actionable checklists
2. **Add Execution Details**: Include file paths, commands, decision criteria
3. **Include All Context**: References, examples, troubleshooting, success criteria
4. **Validate Completeness**: Could someone else execute this MCP successfully?

**Output**: Master Checklists ready for immediate execution

**Quality Gate**: MCP contains everything needed to start work immediately

---

### Phase 3: Focused Execution
**Goal**: Execute efficiently without planning interruptions

**Process**:
1. **Pick Up MCP**: All context immediately available
2. **Execute Systematically**: Follow checklist, update progress
3. **Capture Learnings**: Note what worked, what didn't, what was missing
4. **Complete with Handoffs**: Deliver outputs as specified

**Output**: Sprint deliverables plus lessons for next sprint

**Quality Gate**: Deliverables enable dependent sprints to start

---

#### Autonomous Execution Defense Strategy
**Critical for Independent Operation**: Protect against compaction/crashes during autonomous work

**When to Update Context Keys**:
- **New Understanding Achieved** - Store insights immediately
- **Sub-step Completion** - Record progress milestones  
- **Something Worth Investigating** - Note for later (even if not TodoWrite-worthy)
- **Decision Points** - Document choices made and reasoning
- **TodoWrite Changes** - Mirror critical state to persistent storage

**Warning Signs to Watch For**:
- TodoWrite list suddenly disappears (major crash indicator)
- Thinking feels fuzzy about current task
- Can't remember what I was just working on
- Uncertainty about progress made

**Recovery Protocol**:
1. **STOP** immediately when something feels wrong
2. Run `context_resume` to get full state
3. Read most recent context keys
4. Check for `todowrite_current_task_*` key
5. Reconstruct TodoWrite from context if needed
6. Resume from last known good state

**Defensive Context Patterns**:
- `todowrite_current_task_[id]` - Atomic TodoWrite backup
- `current_understanding_[topic]` - Insights and discoveries
- `progress_milestone_[task]` - Completion records
- `investigation_queue` - Things to look at later
- `decision_log_[context]` - Choices and reasoning

**Benefits**: Enables true autonomous operation with crash resilience

---

### Phase 4: Sprint Retrospective and Pattern Capture
**Goal**: Improve future sprint planning with discovered insights

**During Execution - Capture Real-Time Insights**:
- "We should have considered X perspective from the beginning"
- "This analysis approach revealed Y that we didn't expect"
- "Looking at it from Z angle gives much more detail"
- "We forgot to plan for W scenario"

**Post-Sprint - Pattern Documentation**:
1. **What Perspectives Were Missing?**: What viewpoints would have improved our initial planning?
2. **What Analysis Angles Emerged?**: What ways of looking at the problem proved most valuable?
3. **What Planning Gaps Appeared?**: What considerations should be standard for this type of sprint?
4. **What Worked Unexpectedly Well?**: What approaches exceeded expectations?

**Integration with Future Planning**:
- Add discovered perspectives to planning question templates
- Update MCP templates with newly identified considerations
- Build "lessons learned" checklist for similar sprint types
- Create planning triggers: "For inventory sprints, also consider..."

**Output**: Enhanced planning templates and perspective checklists for future sprints

---

## Sprint Planning Template

### Current Sprint Focus: [Sprint Name]

#### 1. Sprint Definition
- **Primary Objective**: What are we accomplishing?
- **Success Criteria**: How do we know we're done?  
- **Why Now**: Why is this sprint prioritized?
- **Scope Boundaries**: What's included/excluded?

#### 2. Action Brainstorming
*Exhaustively list potential actions - quantity over quality initially*

**Data Collection Actions**:
- [ ] Action 1
- [ ] Action 2
- [ ] Action 3

**Analysis Actions**:
- [ ] Action A
- [ ] Action B  
- [ ] Action C

**Documentation Actions**:
- [ ] Action X
- [ ] Action Y
- [ ] Action Z

#### 3. Interactive Refinement Questions
*Challenge every assumption until crystal clear*

**Scope Questions**:
- Are we trying to do too much?
- Are we missing critical actions?
- What would "good enough" look like?

**Resource Questions**:  
- Do we have access to everything needed?
- Are there tools we should build first?
- What expertise gaps exist?

**Output Questions**:
- Who will use the outputs and how?
- What format is most useful?
- How do we validate quality?

**Risk Questions**:
- What typically goes wrong with this type of work?
- What would block us completely?
- How do we stay on track?

#### 4. Planning Resolution: Question Exhaustion Method
*Continue interactive questioning until reaching the "dead end"*

**The Rule**: Planning is complete when:
- I have no more questions because you've answered them all
- You have no more questions because I've answered them all  
- We've hit the "dead end" of mutual question exhaustion

**Process**:
1. I ask all my questions about scope, approach, outputs, risks
2. You answer and ask your own questions about my understanding  
3. I clarify and ask follow-up questions based on your answers
4. Continue until neither of us has more questions
5. **Only then** move to MCP task detail extraction

**Quality Gate**: Both parties say "I don't have any more questions" simultaneously

#### 5. Planning Validation Checklist
*After reaching question exhaustion, verify:*

- [ ] Scope is clear and bounded
- [ ] Actions are concrete and doable  
- [ ] Resources are identified and available
- [ ] Outputs are well-defined and useful
- [ ] Risks are understood and mitigated
- [ ] Success criteria are measurable
- [ ] We could start executing immediately
- [ ] **Neither party has remaining questions**

---

## Example: Sprint A1 Planning Session

### Sprint Definition ✅
**Objective**: Catalog all P2 objects with metadata for pattern extraction  
**Success Criteria**: Complete inventory enables pattern mining teams  
**Why Now**: Blocks all pattern extraction work  
**Scope**: GitHub repo only, OBEX comparison later

### Action Brainstorming ✅
*[Already completed in MCP creation]*

### Refinement Questions Discussion:

**Q**: Should we analyze code quality deeply or just surface-level?  
**A**: Surface-level sufficient for pattern team prioritization

**Q**: How do we handle objects with unclear functionality?  
**A**: Document as "needs analysis", don't guess

**Q**: What if we find objects that don't compile?  
**A**: Note compatibility issues, include in inventory anyway

**Q**: Should we contact original authors for clarification?  
**A**: No - use available information only, note gaps

### Planning Resolution ✅
All questions answered, MCP created, ready to execute.

---

## Benefits of This Approach

### For Individual Productivity
- **No Context Switching Delays**: Pick up tasks immediately
- **Higher Quality Output**: Thoughtful planning shows in results
- **Reduced Stress**: Know exactly what to do and how to do it
- **Better Learning**: Capture insights for continuous improvement

### For Project Success  
- **Predictable Progress**: Well-planned sprints deliver as expected
- **Knowledge Preservation**: MCPs become organizational memory
- **Scalable Execution**: Others can pick up work using same MCPs
- **Risk Mitigation**: Planning identifies and addresses problems early

### For Team Coordination
- **Clear Dependencies**: Everyone knows what blocks what
- **Standardized Handoffs**: Consistent output formats and expectations
- **Transparent Progress**: MCPs make current status obvious
- **Quality Assurance**: Built-in validation at every phase

---

## Documentation Evolution

As we refine this approach:

1. **Capture What Works**: Note successful MCP patterns
2. **Identify Gaps**: What context was missing from MCPs?
3. **Improve Templates**: Update templates based on experience
4. **Build Libraries**: Reusable MCP components for common tasks
5. **Share Learnings**: Document insights for future sprints

This methodology transforms "winging it" into systematic, high-quality knowledge work.

---

**Next Step**: Apply this methodology to Sprint A1 planning refinement and MCP validation.