# Sprint Candidates Registry

*Last Updated: 2025-08-19*

## Purpose
Work intentions and high-level goals awaiting proper sprint planning. These are NOT tasks - they're candidates for future sprint investigation and task generation.

## How This Works
1. **Candidates accumulate here** by category
2. **Sprint planning** selects candidates to investigate
3. **Deep investigation** generates actual tasks
4. **Real tasks** go to sprint backlog (not here)

---

## 🤖 AI Optimization Candidates
*Goal: Direct improvements to AI's P2 code generation ability*

### AO-001: P2 AI Development Assistant Architecture
- **Effort Estimate**: 2 hours (planning only)
- **Intent**: Structure knowledge base for virgin Claude instances
- **From**: Task #924
- **Needs**: Architecture design, selective discovery strategy

### AO-002: Generate AI-Optimized Reference Documentation
- **Effort Estimate**: 1.5 hours
- **Intent**: Create reference specifically for AI consumption
- **From**: Task #914
- **Needs**: Format specification, content selection

### AO-003: Update Gap Tracking
- **Effort Estimate**: 20 minutes
- **Intent**: Track 176→165 instruction reduction
- **From**: Task #902
- **Needs**: Source attribution, gap analysis

---

## 🔍 Pattern Extraction Candidates
*Goal: Mine P2 code for reusable patterns*

### PE-001: Object Inventory Sprint
- **Effort Estimate**: 4 hours
- **Intent**: Catalog all GitHub P2 objects with metadata
- **From**: Task #912
- **Needs**: Inventory methodology, metadata schema

### PE-002: Structural Patterns Extraction
- **Effort Estimate**: 5 hours
- **Intent**: Extract Start/Stop, CON/VAR, lifecycle patterns
- **From**: Task #922
- **Needs**: Pattern identification criteria, extraction method

### PE-003: Communication Patterns Extraction
- **Effort Estimate**: 5 hours
- **Intent**: Extract mailbox, protocols, inter-cog patterns
- **From**: Task #921
- **Needs**: Communication pattern taxonomy

### PE-004: Smart Pin Patterns Extraction
- **Effort Estimate**: 5 hours
- **Intent**: Extract Smart Pin and hardware interface patterns
- **From**: Task #920
- **Needs**: Pin configuration analysis methodology

---

## ✅ Trust Validation Candidates
*Goal: Verify knowledge accuracy against silicon*

### TV-001: Audit v1.0 Materials
- **Effort Estimate**: 1 hour
- **Intent**: Quality and consistency audit
- **From**: Task #903
- **Needs**: Audit criteria, validation checklist

---

## 📚 Document Production Candidates
*Goal: Create user-facing documentation (requires Opus 4.1)*

### DP-001: P2 Assembly Tutorial (DeSilva-style)
- **Effort Estimate**: 3 hours
- **Intent**: Study P1 tutorial, create P2 version
- **From**: Task #913
- **Needs**: Voice analysis, content adaptation strategy

### DP-002: Branded PDF Materials
- **Effort Estimate**: 30 minutes
- **Intent**: AI Privacy Guide, Release Notes
- **From**: Task #895
- **Needs**: Content finalization, branding assets

### DP-003: Community Impact Rationale
- **Effort Estimate**: 30 minutes
- **Intent**: Add rationale to document generation sprints
- **From**: Task #919
- **Needs**: Impact assessment framework

---

## 🔧 Process Infrastructure Candidates
*Goal: Improve internal workflows and tooling*

### PI-001: Documentation Style Guide
- **Effort Estimate**: 45 minutes
- **Intent**: Enrich style guide planning and standards
- **From**: Task #911
- **Needs**: Style analysis, standard definitions

### PI-002: Communications Directory Strategy
- **Effort Estimate**: 10 minutes
- **Intent**: Document in PROJECT-MASTER.md
- **From**: Task #918
- **Needs**: Strategy clarification

### PI-003: Pipeline Status Documentation
- **Effort Estimate**: 15 minutes
- **Intent**: Show complete pipeline status
- **From**: Task #916
- **Needs**: Pipeline inventory, status format

---

## 🚧 Blocked/Deferred Candidates

### BD-001: TAQOZ ROM Forth Processing
- **Status**: BLOCKED - needs OCR solution
- **From**: Task #926
- **Blocker**: PDF extraction technology

### BD-002: Final v1.0 Commit
- **Status**: DEFERRED - awaiting v1.0 completion
- **From**: Task #917
- **Dependencies**: All v1.0 materials complete

---

## Selection Criteria for Sprint Planning

When selecting candidates for a sprint:
1. **Alignment**: Does it serve our primary audience (AI/developers)?
2. **Dependencies**: Are prerequisites complete?
3. **Capacity**: Do we have the right resources (time, model, knowledge)?
4. **Impact**: What's the value delivered?
5. **Coherence**: Does it fit with other sprint work?

## Adding New Candidates

When adding a candidate:
- Give it a category code (AO, PE, TV, DP, PI, BD)
- Estimate effort for investigation (not implementation)
- Note what investigation is needed
- Link to source if applicable
- Keep description high-level (details come in sprint planning)