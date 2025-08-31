# Work Mode Lifecycle Guide

**Single Purpose**: Systematic approach to work mode transitions ensuring quality and completeness

## 🎯 The Three States of Work Mode Management

```
First Time Work → PLANNING MODE → Generate Tasks → EXECUTION MODE
                                                        ↓
Existing Work ← Context Switch ← EXECUTION MODE ← Resume Tasks
```

## 📊 State Detection & Response Matrix

| Filtered Tasks Found | Mode | Primary Action | Quality Control |
|---------------------|------|----------------|-----------------|
| **0 tasks** | PLANNING | Generate systematic task breakdown | Avoid artifact hunting |
| **1+ tasks** | EXECUTION | Resume focused work with filtering | Add new tasks if priorities shifted |
| **Context Switch** | TRANSITION | Save state, detect new mode state | Clean handoffs between work types |

---

## 🧠 STATE 1: PLANNING MODE (First Time Work)

### Trigger Conditions
- `mcp__todo-mcp__todo_next tags:["work_mode"]` returns 0 tasks
- New work area never systematically planned before
- User requests work we haven't organized properly

### Planning Mode Protocol

#### Step 1: Information Gathering
```markdown
**Read Required Documents** (from work mode guide):
- Work mode specific guide (e.g., smart-pins-visual-refinement.md)
- Referenced methodology documents
- Current workspace analysis

**Analyze Current State:**
- What workspace directories exist?
- What's the current state of templates/documents?  
- What obvious work needs to be done?
- What are the success criteria?
```

#### Step 2: Systematic Task Generation
```markdown
**Task Categories to Consider:**
1. **Setup/Infrastructure** (templates, workspace prep)
2. **Content Work** (document editing, fixes)
3. **Testing/Validation** (PDF generation, verification)  
4. **Integration/Deployment** (escaping, outbound prep)
5. **Quality Control** (review cycles, standards compliance)

**Task Generation Rules:**
- Each task gets proper work mode tag
- Realistic time estimates (5m-60m typically)
- Clear success criteria
- Proper priority assignment (critical → high → medium → low)
- Dependencies identified where relevant
```

#### Step 3: Task Creation
```bash
mcp__todo-mcp__todo_batch_create tasks:[
  {
    "content": "[Specific actionable task] [work_mode_tag]",
    "estimate_minutes": [realistic_estimate],
    "priority": "[critical|high|medium|low]"
  }
]
```

#### Step 4: Validation & Transition
```markdown
**Quality Checks:**
- [ ] Tasks cover obvious work scope
- [ ] No major gaps in workflow
- [ ] All tasks properly tagged for filtering
- [ ] Estimates seem realistic
- [ ] Priorities make sense for execution order

**Transition to Execution:**
- Save planning process in context
- Run filtered todo_next to get first task
- Begin execution mode protocols
```

### Planning Mode Examples

#### Example A: Smart Pins Visual (First Time)
```
User: "Smart Pins visual work"
Found: 0 smart_pins_visual tasks → PLANNING MODE

Analysis:
- Workspace exists at /exports/pdf-generation/workspace/smart-pins-manual/
- WORKING.md needs visual refinement based on user feedback
- Templates need testing and iteration
- PDF generation workflow needs validation

Generated Tasks:
1. Remove mini-TOC from workspace WORKING.md [smart_pins_visual] (5m)
2. Fix list formatting issues throughout document [smart_pins_visual] (20m)  
3. Test visual improvements with PDF generation [smart_pins_visual] (15m)
4. Address user feedback on section numbering [smart_pins_visual] (30m)
```

#### Example B: De Silva Template (First Time)
```
User: "De Silva template adaptation"
Found: 0 desilva_manual tasks → PLANNING MODE

Analysis:
- Need to migrate to layered template stack
- Multi-part document structure (Part 1, 2a, 2b, 2c, Appendices)
- Legacy template needs modernization
- Content cleanup required after template migration

Generated Tasks:
1. Analyze current De Silva template architecture [desilva_manual] (20m)
2. Create p2kb-desilva-content.sty with extracted functionality [desilva_manual] (45m)
3. Test new template stack with Part 1 [desilva_manual] (30m)
4. Migrate all parts to new template system [desilva_manual] (60m)
```

---

## ⚡ STATE 2: EXECUTION MODE (Existing Work)

### Trigger Conditions
- `mcp__todo-mcp__todo_next tags:["work_mode"]` returns 1+ tasks
- Systematic task breakdown already exists
- Resuming work from previous sessions

### Execution Mode Protocol

#### Step 1: Task Filtering & Selection
```bash
mcp__todo-mcp__todo_next tags:["work_mode_tag"]
```

#### Step 2: Priority Assessment
```markdown
**Check for New Priorities:**
- Has user feedback changed priorities?
- Are there blocking issues that need immediate attention?
- Do existing tasks still match current work needs?

**Add New Tasks if Needed:**
- User provides new requirements mid-stream
- Discovered issues during execution  
- Scope expansion or refinement
```

#### Step 3: Focused Execution
```markdown
**Work with Proper Context:**
- Use work mode guide protocols
- Maintain workspace organization
- Document progress in context keys
- Apply creation guide requirements
- Follow quality standards for the work mode
```

#### Step 4: Progress Tracking
```markdown
**As Tasks Complete:**
- Mark tasks completed immediately
- Document learnings in context
- Update user on progress
- Generate follow-up tasks if needed
```

### Execution Mode Examples

#### Example A: Smart Pins Resume
```
User: "Smart Pins visual work"
Found: 3 smart_pins_visual tasks → EXECUTION MODE

Next Task: "Test visual improvements with PDF generation [smart_pins_visual] (15m)"
→ Resume focused work on PDF testing
→ Apply smart-pins-visual-refinement.md protocols  
→ Use workspace at /exports/pdf-generation/workspace/smart-pins-manual/
```

#### Example B: De Silva Resume  
```
User: "Continue De Silva work"
Found: 7 desilva_manual tasks → EXECUTION MODE

Next Task: "Test new template stack with Part 1 [desilva_manual] (30m)"
→ Resume template testing workflow
→ Apply desilva-manual-mode.md protocols
→ Focus on multi-part document structure
```

---

## 🔄 STATE 3: CONTEXT SWITCHING (Clean Transitions)

### Trigger Conditions
- User requests different work type mid-session
- Completing one work mode, moving to another
- Session restart with different focus

### Context Switching Protocol

#### Step 1: Current Work State Save
```markdown
**Save Current Progress:**
- Update context keys with current state
- Note any in-progress tasks
- Document any discoveries or blockers
- Mark clear stopping point
```

#### Step 2: Mode Transition
```markdown
**Clean Handoff:**
- Follow new work mode detection (Planning vs Execution)
- Read new work mode guide
- Apply new filtering and protocols
- Avoid mixing work mode contexts
```

#### Step 3: State Detection for New Mode
```markdown
**Apply Standard Protocol:**
- Check for existing tasks with new mode tags
- Enter Planning Mode if empty
- Enter Execution Mode if tasks exist
- Maintain proper separation between work types
```

### Context Switching Examples

#### Example A: Smart Pins → De Silva
```
Current: Working on Smart Pins visual refinement
Switch: User says "Let's work on De Silva template adaptation"

Process:
1. Save smart_pins context: "List formatting fixes applied, ready for PDF test"
2. Switch to De Silva work mode detection
3. Find 0 desilva_manual tasks → Enter Planning Mode
4. Generate De Silva task breakdown
5. Begin De Silva execution with proper filtering
```

#### Example B: Planning → Execution Transition
```
Current: Just finished generating 5 new smart_pins_visual tasks  
Transition: Move from Planning Mode to Execution Mode

Process:
1. Validate task generation quality
2. Run filtered todo_next to get first task
3. Switch to execution mode protocols
4. Begin focused work with proper context
```

---

## 🛡️ Quality Control & Anti-Patterns

### ✅ Best Practices

**Planning Mode:**
- Always read work mode guide first
- Generate comprehensive task breakdown
- Use proper tagging for filtering
- Create realistic estimates
- Identify dependencies

**Execution Mode:**  
- Always use filtered task lists
- Complete tasks before moving to next
- Document progress in context
- Follow work mode guide protocols
- Maintain workspace organization

**Context Switching:**
- Save current state clearly
- Clean separation between work modes
- Apply proper state detection
- Don't mix work contexts

### ❌ Anti-Patterns to Avoid

**"Artifact Hunting"**
```
❌ BAD: "Let me look around the workspace and find something to work on"
✅ GOOD: "Let me plan this work systematically first"
```

**"Mode Confusion"**
```
❌ BAD: Mix Smart Pins tasks with De Silva tasks
✅ GOOD: Clean separation with proper filtering
```

**"Task Skipping"**
```  
❌ BAD: Skip planned tasks to work on something else
✅ GOOD: Follow filtered task sequence, add new tasks if priorities change
```

**"Legacy Bias"**
```
❌ BAD: Base new work on old artifacts that might be sloppy
✅ GOOD: Plan from current needs and proper requirements
```

---

## 🚀 Integration with Session Start Protocol

**This guide provides the detailed protocols referenced in CLAUDE.md SESSION START PROTOCOL Step 3.5.**

**Quick Reference:**
- 0 filtered tasks = Planning Mode (this guide Sections 1-2)
- 1+ filtered tasks = Execution Mode (this guide Sections 3-4)  
- Context switching = Transition protocols (this guide Section 5)

**The goal**: Every work session starts systematically and proceeds with focused, quality execution.