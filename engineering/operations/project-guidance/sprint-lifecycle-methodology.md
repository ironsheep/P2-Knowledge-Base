# Sprint Lifecycle Methodology

**Purpose**: Complete sprint lifecycle from capability planning through public integration and version milestones

---

## 📋 PHASE 1: Sprint Planning & Refinement

### 1.1 Capability Definition
**What knowledge/understanding are we adding?**
- Define sprint capabilities (the "features" we're adding)
- Specify value and integration with existing knowledge
- Identify how this strengthens the foundation

### 1.2 Iterative Planning Refinement
**Question Exhaustion Method:**
1. Initial capability specifications
2. Question/answer cycles until no questions remain
3. Scope refinement based on discoveries
4. Final capability specs when both parties have no questions

### 1.3 Task Breakdown
**From Capabilities to Tasks:**
- Break capabilities into implementation tasks
- Create todo-mcp tracked items
- Define success criteria for each task

### 1.4 Task Detail Generation
**Implementation Instructions:**
- Generate detailed task instructions (formerly "MCPs")
- Include all context needed for independent execution
- Validate completeness (can someone else execute this?)

**GATE**: Ready for independent execution when:
- ✅ Capabilities fully specified
- ✅ Tasks clearly defined in todo-mcp
- ✅ Task details comprehensive
- ✅ No remaining questions

---

## 🚀 PHASE 2: Sprint Execution

### 2.1 Independent Work
- Execute tasks using detailed instructions
- Track progress in todo-mcp
- Document discoveries and patterns

### 2.2 Continuous Documentation
- Capture learnings as they emerge
- Note "should have considered" items
- Track actual vs estimated effort

---

## ✅ PHASE 3: Sprint Integration & Wrap-up

### 3.1 Goal Achievement Audit
**Did we achieve our sprint goals?**
- Compare delivered capabilities vs planned
- Document any gaps or exceeded expectations
- Capture lessons learned

### 3.2 Public Documentation Update Audit
**Have we updated everything that should be updated?**

#### Update Checklist:
- [ ] README.md - New capabilities visible?
- [ ] engineering/operations/README.md - Current state accurate?
- [ ] /ai-reference/ - New knowledge integrated?
- [ ] Documentation indexes - All new content indexed?
- [ ] Cross-references - Links updated?

#### Audit Questions:
- Is every new capability reflected in public docs?
- Are all improvements visible to users?
- Did we miss any documentation that should be updated?

### 3.3 Capability Communication
**"New and Wonderful Has Arrived"**

Create announcement/highlight of new capabilities:
- What's new and why it matters
- How it enhances the knowledge base
- What users can now do that they couldn't before

Example: "Sprint Update: AI Foundation Validation Complete"
- ✨ NEW: Canonical P2 programming patterns documented
- ✨ NEW: Production code examples from runtime interpreter
- ✨ ENHANCED: AI can now generate P2 code with proven patterns

### 3.4 Git Integration & Version Milestone

#### Comprehensive Commit Process:
```bash
# Stage all changes
git add -A

# Comprehensive commit message
git commit -m "Sprint: [Sprint Name] - [Major Capabilities Added]

Capabilities Added:
- Capability 1: [description]
- Capability 2: [description]

Documentation Updates:
- Updated X documents with new knowledge
- Added Y new examples/patterns
- Enhanced Z existing sections

Validation Results:
- [Key validation outcomes]

Lessons Learned:
- [Major insights from sprint]"
```

#### Release/Milestone Creation:
```bash
# Create tagged release for learning milestone
git tag -a "v0.2.0-ai-validation" -m "AI Foundation Validation Sprint Complete

Major Achievements:
- Validated foundation knowledge with production code
- Extracted canonical patterns from runtime interpreter
- Enhanced AI code generation capability

This release represents significant foundation strengthening."
```

---

## 📊 PHASE 4: Post-Sprint Analysis

### 4.1 Sprint Metrics
- Planned vs Actual capabilities delivered
- Effort estimates vs actuals (from todo-mcp tracking)
- Documentation coverage improvements
- Quality enhancements achieved

### 4.2 Release Comparison
**What changed from last release?**
- Knowledge base growth metrics
- Quality improvements
- New capabilities enabled
- Gap closures achieved

### 4.3 Learning Evolution
**How have we improved?**
- Process improvements identified
- Methodology enhancements
- Tool/template updates needed
- Planning accuracy trends

---

## 🔄 Continuous Improvement Loop

### From Each Sprint:
1. **Process Refinements** → Update methodology documents
2. **Template Improvements** → Enhance planning templates
3. **Lesson Integration** → Add to planning checklists
4. **Pattern Recognition** → Identify recurring success factors

### Release-to-Release Learning:
- Track methodology evolution through releases
- Identify productivity trends
- Measure quality improvements
- Document capability growth rate

---

## ✅ Sprint Completion Checklist

### Before Marking Sprint Complete:
- [ ] All todo-mcp tasks completed
- [ ] Sprint summary documented
- [ ] Public documentation updated
- [ ] Capability announcements created
- [ ] Comprehensive commit with message
- [ ] Release tagged if milestone
- [ ] Lessons learned captured
- [ ] Next sprint opportunities identified

### Quality Gates:
- [ ] No orphaned documentation
- [ ] All cross-references updated
- [ ] Public visibility of new capabilities
- [ ] Clear communication of improvements

---

## 🎯 Success Metrics

### Sprint Success Indicators:
- Capabilities delivered match/exceed plan
- Documentation comprehensively updated
- Clear value communication
- Clean git history with learning trail
- Process improvements identified

### Anti-patterns to Avoid:
- Hidden improvements (not updating public docs)
- Orphaned documentation (creating without linking)
- Silent completion (no communication of value)
- Lost learnings (not capturing lessons)

---

*This methodology ensures every sprint strengthens both the knowledge base AND our ability to deliver future sprints*