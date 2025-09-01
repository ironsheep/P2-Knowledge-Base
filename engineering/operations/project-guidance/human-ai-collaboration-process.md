# Human-AI Collaboration Process
*Full round-trip workflow for collaborative knowledge ingestion*

## Overview
This process manages tasks requiring human input (audits, images, verification) through a complete lifecycle from request to integration.

---

## Phase 1: Request Generation (AI Autonomous)

### 1.1 Identify Need
- During extraction/analysis, identify gaps requiring human input
- Categories: Images, Audits, Verification, Metadata enrichment

### 1.2 Create Request Document
Generate structured request in `human-todos/` folder:
- Clear identification system (IDs for tracking)
- Specific ask with context
- Template for human response
- Priority and impact assessment

### 1.3 Update Human ToDos Index
Update `human-todos/README.md` with:
- New request added
- Priority ranking
- Expected value/impact
- Time estimate

---

## Phase 2: Joint Review Session (Human-AI Collaborative)

### 2.1 Human Initiates Review
- Human: "Let's do the PASM2 audit" (or similar)
- AI presents prepared materials
- Human reviews materials offline first (optional)
- Human returns ready to discuss

### 2.2 Interactive Review Process
**Together, we go through the catalog:**

**For Instruction Audits**:
- AI: "Instruction ABS - we have X, missing Y"
- Human: "Clock timing is 2 cycles, narrative should include Z"
- AI: Records additions in real-time
- Continue through entire list

**For Code Examples**:
- AI: "Example SPIN2-001 shows constant declaration"
- Human: "This teaches underscore formatting, beginner level"
- AI: Records metadata enrichment
- Continue through all examples

**For Images**:
- AI: "Image IMG-001 requested for terminal output"
- Human: "Captured as terminal-debug-001.png, shows basic DEBUG"
- AI: Records location and metadata
- Continue through collection

### 2.3 Completion Confirmation
- Review any unclear items together
- Human: "That's everything" or "No more questions"
- AI: "No remaining questions"
- **This enables post-processing sprint**

---

## Phase 3: Integration (AI Autonomous)

### 3.1 Process Human Input
- Read completed audit/review document
- Parse human additions and corrections
- Validate data consistency

### 3.2 Update Knowledge Base
Based on input type:

**Images**:
- Generate markdown catalog
- Create extraction documents
- Update visual assets tracking
- Link to relevant documents

**Instruction Audits**:
- Update instruction reference with timing
- Elevate trust levels (red→yellow→green)
- Create performance consulting data
- Update instruction matrices

**Code Examples**:
- Build searchable pattern library
- Tag with metadata (difficulty, concepts)
- Create recommendation mappings
- Generate "show me" responses

### 3.3 Update All Matrices
- Trust elevation metrics
- Coverage percentages
- Gap analysis updates
- Sprint candidate adjustments

### 3.4 Archive Completed Request
- Move from `human-todos/` to `human-todos/completed/`
- Add completion timestamp
- Note integration results
- Update metrics

---

## Phase 4: Validation & Metrics

### 4.1 Verify Integration
- Confirm data accessible in knowledge base
- Test queries against new content
- Validate trust level changes

### 4.2 Update Project Metrics
- Coverage percentage changes
- Trust distribution updates
- Sprint velocity tracking
- Value delivered assessment

### 4.3 Report Results
Generate summary:
- What was integrated
- Coverage improvement
- Trust elevation achieved
- New capabilities enabled

---

## Standard Request Templates

### Image Request Template
```markdown
# Image Request: [Topic]
Request ID: IMG-XXX
Priority: High/Medium/Low
Impact: [What this enables]

## Images Needed:
1. [Description] - Purpose: ___
2. [Description] - Purpose: ___

## Capture Instructions:
- Settings: ___
- Context: ___

## Human Response:
Image 1: [filename] - [metadata]
Image 2: [filename] - [metadata]
```

### Audit Request Template
```markdown
# Audit Request: [Source Document]
Request ID: AUD-XXX
Priority: High/Medium/Low
Impact: [Trust elevation potential]

## Items to Verify:
- [ ] Item 1 - Current: ___ Actual: ___
- [ ] Item 2 - Current: ___ Actual: ___

## Metadata to Add:
- Clock cycles: ___
- Context: ___
- Prerequisites: ___
```

---

## Key Principles

1. **Clear Handoffs**: Each phase has clear completion criteria
2. **Trackable Progress**: IDs and status for every request
3. **Value Focus**: Always note impact/value of completion
4. **Archive Everything**: Completed work archived for reference
5. **Metrics Drive Decisions**: Update coverage/trust metrics

---

## Current Active Requests

Check `human-todos/README.md` for current list

## Completed Requests

Check `human-todos/completed/` for history

---

*This process ensures systematic collaboration with full tracking and value delivery*