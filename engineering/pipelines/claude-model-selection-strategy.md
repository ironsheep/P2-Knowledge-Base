# Claude Model Selection Strategy for P2 Knowledge Base

## Model Capabilities & Costs

### Opus 4.1
**Cost**: Highest (~3x Sonnet)
**Strengths**: Complex reasoning, strategy, nuance, creativity
**Speed**: Slower but deeper

### Sonnet 3.5
**Cost**: Medium (~1/3 of Opus)
**Strengths**: Execution, structured tasks, speed
**Speed**: Very fast

### Haiku 3.5
**Cost**: Lowest (~1/10 of Opus)
**Strengths**: Simple queries, quick lookups
**Speed**: Extremely fast

## Project Phase Model Selection

### Phase 1: Sprint Planning & Strategy (OPUS)
**Start your day here when doing:**
- Sprint planning and methodology design
- Discovering new document types or voices
- Working through privacy/legal/strategic issues
- Designing workflows and integration patterns
- Question exhaustion methodology
- Resolving philosophical misunderstandings
- Any "I'm not sure how to..." situations

**Today's Examples**:
- Privacy strategy for Ken/Chip observations
- Discovering 7 documentation voices
- Image extraction workflow design
- TodoWrite+MCP integration pattern
- Understanding metrics philosophy

### Phase 2: Task Generation & Review (OPUS → SONNET)
**Transition point when:**
- Sprint plan is complete
- Tasks are being defined
- Ready to create rich task descriptions

**Can use Sonnet if**:
- Following established task template
- No ambiguity in requirements

### Phase 3: Execution & Generation (SONNET)
**Switch to Sonnet for:**
- Extracting from documents following methodology
- Generating JSON from schemas
- Writing manuals from templates
- Creating documentation from patterns
- Running audits with checklists
- Bulk content processing

**Today's Tasks**: All 25 v1.0 sprint tasks are Sonnet-appropriate

### Phase 4: Validation & Testing (SONNET or HAIKU)
**Can even use Haiku for:**
- Simple validation checks
- Running test queries
- Formatting cleanup
- Checklist verification

### Phase 5: Complex Debugging (OPUS)
**Switch back to Opus when:**
- Something unexpected happens
- Integration issues arise
- Need creative problem-solving
- Ambiguous errors occur

## Daily Model Plan

### Morning Start (Default: OPUS)
**Why**: Most creative/strategic work happens fresh
- Review what needs doing
- Plan the day's approach
- Resolve any overnight thoughts
- Handle new requirements

**Transition Trigger**: "Tasks are clear, let's execute"

### Midday Execution (SONNET)
**Why**: Bulk of defined work
- Execute planned tasks
- Generate content
- Process documents
- Follow methodologies

**Transition Trigger**: "I hit something ambiguous"

### Problem Solving (OPUS)
**Why**: Need strategic thinking
- Debug complex issues
- Resolve ambiguities
- Make architectural decisions
- Creative solutions needed

**Transition Trigger**: "Problem resolved, back to execution"

### End of Day Wrap-up (SONNET)
**Why**: Routine documentation
- Update progress docs
- Archive completed work
- Generate summaries
- Prepare for tomorrow

## Project-Specific Guidance

### P2 Knowledge Base Patterns

**OPUS Territory**:
- "How should we handle..."
- "What's the best way to..."
- "I'm concerned about..."
- "Let's design a..."
- Discovering new patterns
- Resolving contradictions

**SONNET Territory**:
- "Extract all X from document Y"
- "Generate JSON following schema"
- "Create manual using template"
- "Run audit checklist"
- "Update documentation"
- Following established patterns

## Cost Optimization Strategy

### Maximum Value Approach
1. **Front-load Opus work** in morning when fresh
2. **Batch similar tasks** for Sonnet execution
3. **Save complex problems** for dedicated Opus sessions
4. **Use Haiku** for simple validations

### Budget-Conscious Days
- Start with 30 minutes of Opus planning
- Switch to Sonnet for entire day
- Return to Opus only if blocked

## Switching Checklist

### Before Switching TO Sonnet:
- [ ] Tasks are clearly defined
- [ ] Methodologies are documented
- [ ] Templates exist to follow
- [ ] No strategic decisions needed
- [ ] Save any TodoWrite state to context

### Before Switching TO Opus:
- [ ] Document what's ambiguous
- [ ] Note what creative solution is needed
- [ ] Prepare context of the problem
- [ ] Archive any Sonnet progress

## Model Memory Aids

### Reminder Context Keys
Set these to help next session know which model:
```
context_set('model_phase', 'execution')  # Use Sonnet
context_set('model_phase', 'planning')   # Use Opus
context_set('model_phase', 'debugging')  # Use Opus
```

### Session Start Protocol
1. Check `model_phase` context key
2. Confirm with user if right model
3. Suggest switch if phase changed

## The Economics

### Typical Sprint Costs (Relative)
- Planning (Opus): 100 units
- Execution (Sonnet): 100 units (but 3x the work!)
- Total: 200 units for 4x productivity

### Without Strategy (All Opus)
- Everything: 300+ units
- Same productivity

**Savings: 33-50% with smart switching**

## Quick Reference

**"Should I switch?" Decision Tree**:
```
Is the task clearly defined?
├─ NO → Stay in Opus
└─ YES → 
    │
    Does it follow a template/methodology?
    ├─ NO → Stay in Opus
    └─ YES → 
        │
        Is it bulk processing/generation?
        ├─ YES → Switch to Sonnet
        └─ NO → Probably stay in Opus
```

## Today's Recommendation

You've done ALL the Opus work needed for v1.0:
- Sprint planned ✓
- Tasks defined ✓
- Methodologies established ✓
- Templates created ✓

**Perfect time to switch to Sonnet for execution!**

This morning was 100% Opus-appropriate work.
This afternoon/evening is 100% Sonnet-appropriate work.