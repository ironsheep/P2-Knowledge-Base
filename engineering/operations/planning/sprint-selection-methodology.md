# Sprint Selection Methodology

*Capturing our thinking on how to select the next sprint*

## Original Exploration (2025-08-19)

### The Core Problem
We have multiple feeds (Analysis Debt, Sprint Candidates, Document Pipeline) but no clear decision framework for "What sprint should we do next?"

### Key Factors to Consider
1. **Dependency Chains** - Some work blocks other work (AD-001 blocks PASM2 Manual)
2. **Audience Impact** - AI optimization vs human documentation 
3. **Model Availability** - Document sprints need Opus 4.1
4. **Momentum** - Sometimes finishing a category builds valuable context
5. **External Triggers** - Community needs, new P2 releases, etc.

### Approaches Considered

#### 1. Sprint Selection Matrix (SELECTED ✓)
Create a decision document that scores potential sprints on:
- **Urgency**: Is something time-sensitive?
- **Impact**: How many downstream items does it unblock?
- **Readiness**: Are dependencies met?
- **Effort**: Can we complete it in available time?
- **Strategic Alignment**: Does it serve our primary audience?

**Why this works**: 
- Transparent scoring criteria
- Dynamic reordering as conditions change
- Guides decisions with clear rationale
- Always reflects current state

#### 2. Priority Queues (REJECTED)
- Must Do Queue
- Should Do Queue  
- Could Do Queue
- Parking Lot

**Why rejected**: Hides reasoning, assumes we keep decision criteria in our heads

#### 3. Sprint Triggers (SUPPLEMENTAL ✓)
"When X happens, do Y sprint type"
- When knowledge gaps block progress → Analysis Sprint
- When patterns are needed for AI → Pattern Extraction Sprint
- When community asks for docs → Document Sprint (with Opus)
- When process is painful → Infrastructure Sprint

**How we'll use this**: As enablement notifications alongside the decision matrix

## Our Approach: Decision Matrix + Enablement Triggers

### Decision Matrix Document
- Live document that scores all potential sprints
- Updates as conditions change (dependencies met, urgency shifts)
- Transparent scoring shows WHY something ranks high
- Always gives us the "next best sprint" recommendation

### Enablement Triggers
- When we complete something that unblocks other work
- System reminds us: "Hey, completing X just enabled Y and Z"
- Updates decision matrix scores
- Alerts us to new possibilities

### Benefits of Combined Approach
1. **Always have a recommendation** - Decision matrix shows best next sprint
2. **Know when options open up** - Triggers alert us to new possibilities
3. **Transparent reasoning** - Can see exactly why something scores high
4. **Dynamic adaptation** - Scores change as we progress
5. **No hidden logic** - Everything is documented and visible

## Implementation Plan
1. Create Sprint Decision Matrix document
2. Define scoring criteria and weights
3. Score all current sprint candidates
4. Create trigger tracking for enablement events
5. Link from Operations Dashboard for visibility

---

*This methodology ensures we always make informed sprint selections based on current conditions and strategic priorities.*