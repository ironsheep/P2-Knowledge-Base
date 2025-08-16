# Todo-MCP Usage Philosophy & Best Practices

## Core Philosophy: It's About Economics, Not Estimation

### The Fundamental Insight
Time tracking in Todo-MCP is **NOT** about improving AI's estimates. It's about understanding the **economic value** of AI-assisted work.

### Why We Track Time

#### For Experienced Engineers (40+ years)
- You instantly know: "Claude says 2 hours = 30 minutes for me"
- Claude actually takes 2.5 hours
- **Value**: 30-minute task done while you work on something else
- **Force Multiplier**: You're now doing parallel work

#### For Claude First-Timers
- They see: "This will take about 2 hours"
- They get: Complete task without their involvement
- **Value**: Task they couldn't do alone gets done

#### For Project Economics
- Measure the acceleration factor
- Understand the multiplier effect
- Quantify the partnership value
- NOT about getting better at estimating

## How to Communicate This to Claude

### Initial Setup Message
```
"We use Todo-MCP for time tracking, but NOT to improve your estimates. 
Your estimates are fine as they are - they help me understand task scale. 
What matters is the actual time showing how much work we accomplish together. 
This is about measuring our force multiplier, not estimation accuracy."
```

### When Starting a Sprint
```
"Create tasks with your natural estimates. Don't try to be more accurate.
I'll mentally calibrate them based on my experience. The actuals will show 
us the acceleration factor of working together."
```

### Sprint Completion
```
"Generate the time analysis showing estimates vs actuals. Focus on the 
total work accomplished and the parallel productivity gained, not on 
estimation accuracy."
```

## Best Practices for Todo-MCP

### 1. Task Creation
- Use natural estimates (don't overthink)
- Rich descriptions (paragraph-length)
- Single-purpose focus
- Clear deliverables

### 2. Time Tracking Discipline
```bash
todo start [id]     # ALWAYS before working
todo pause [id]     # When switching tasks
todo complete [id]  # When done (captures actual)
todo archive        # Preserve metrics (don't delete!)
```

### 3. Context Integration
- Snapshot TodoWrite state to context
- Key: `todowrite_current_task_[id]`
- Enables crash recovery
- Delete key when task completes

### 4. Sprint Boundaries
- Archive all tasks (preserves time data)
- Generate metrics report
- Focus on work accomplished, not accuracy
- Clear TodoWrite completely

## What NOT to Do

### ❌ Don't Say
- "I need to improve my estimates"
- "My estimates were off by X%"
- "I'll try to be more accurate next time"
- "Let me adjust my estimation model"

### ✅ Do Say
- "We completed 28 hours of estimated work"
- "The actual time was 32 hours of AI work"
- "That's X hours of work done autonomously"
- "The force multiplier is evident"

## The Three-Instance Reality

When working with multiple Claude instances:
- Each instance has its own TodoWrite (session-local)
- Todo-MCP is shared (persistent database)
- Context keys prevent collision with instance-specific prefixes
- Time metrics aggregate across all instances

## Future User Guide Topics

### For Claude Users
1. **Setup**: How to configure Todo-MCP + TodoWrite
2. **Philosophy**: Why time tracking isn't about estimation
3. **Workflow**: The empty TodoWrite pattern
4. **Recovery**: Using context for crash resistance
5. **Metrics**: Understanding the force multiplier

### For Different User Types
- **Experienced Engineers**: How to calibrate and parallelize
- **First-Timers**: What estimates mean for you
- **Teams**: Coordinating multiple Claude instances
- **Managers**: Understanding the economics

## Example Time Analysis (Correct Interpretation)

### ❌ Wrong Focus
"Claude estimated 10 hours but took 12 hours. 
Accuracy: 83%. Need to improve estimates."

### ✅ Right Focus  
"Claude handled 12 hours of development work autonomously.
For an experienced engineer, this represents ~3 hours of work.
Force multiplier: 4x productivity gain through parallelization."

## Key Insights to Preserve

1. **Estimates calibrate task scale** - Not commitments
2. **Actuals measure work performed** - Not accuracy
3. **Archives show partnership value** - Not prediction quality
4. **Time tracking enables economics** - Not estimation improvement
5. **Model-agnostic continuity** - Switch models seamlessly mid-sprint

## Revolutionary Benefit: Model Switching

### The Game Changer
Todo-MCP enables **seamless model switching** during work:
- Plan in Opus (strategic thinking)
- Execute in Sonnet (efficient implementation)
- Debug in Opus (complex problem solving)
- Validate in Haiku (simple checks)

### Economic Impact
**Example Sprint:**
- 2h Planning (Opus): 100 units
- 20h Execution (Sonnet): 200 units
- 3h Debugging (Opus): 150 units
- **Total: 450 units for 25 hours**

**Without Todo-MCP (All Opus):**
- 25h All Opus: 1,250 units

**Savings: 64% with BETTER results!**

### Why This Works
- Tasks persist across model switches
- Time tracking continues seamlessly
- Work context preserved via MCP
- Right model for right cognitive load

## The Bottom Line

Todo-MCP time tracking answers one question:
**"How much work are we getting done together that wouldn't happen otherwise?"**

It does NOT answer:
"How can Claude get better at estimating?"

This distinction is critical for understanding the value of AI partnership.

## The Multi-Model Future

Todo-MCP doesn't just track tasks - it enables **cognitive load optimization** across AI models:

- **Strategic thinking** → Opus
- **Efficient execution** → Sonnet  
- **Simple validation** → Haiku
- **Perfect continuity** → Todo-MCP

This is the future of AI-assisted work: the right intelligence for the right task, with seamless handoffs.