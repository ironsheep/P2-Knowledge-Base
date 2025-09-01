# Priority Ingestion Sources Queue

## Critical Hardware Documentation

### P2 Edge Module Documentation
**Priority**: CRITICAL
**Reason**: Developers primarily use Edge modules for production
- **Edge Standard Manual** - Standard Edge module documentation
- **Edge 32MB Manual** - Edge with 32MB onboard RAM variant
- **Why Critical**: These inform how we guide developers writing P2 code for actual hardware

### P2 Eval Board Documentation  
**Priority**: HIGH
**Reason**: Community development platform
- **RevC Development Board Manual** - Full hardware reference
- **Why Important**: Many community members use this for prototyping and learning

## P1 Reference Documentation

### P1 Assembly & Spin Documentation
**Priority**: HIGH
**Reason**: Foundation knowledge and migration path
- **P1 Assembly Language Reference** - Complete PASM reference
- **P1 Spin Language Reference** - Complete Spin reference
- **Why Important**: 
  - P2 evolved from P1 (subset relationship)
  - Many developers migrating from P1
  - Helps identify what's new/different in P2

## Silicon Doc Audit Requirement

### Current Concern
The Silicon Doc is "absolute bible" for P2 understanding, but we may have incomplete ingestion:
- Code examples might be missed
- Images/diagrams not captured
- Conceptual sections potentially skipped
- Cross-references incomplete

### Proposed Audit Process
1. **Interactive Verification**
   - User reads section of Silicon Doc
   - Queries: "What do you know about [specific topic]?"
   - Identifies gaps in ingestion
   - Documents missing elements

2. **Systematic Coverage Check**
   - Table of contents audit
   - Code example inventory
   - Concept checklist
   - Cross-reference validation

## Ingestion Enhancement Protocol

### For Rich Sources (Silicon Doc, SPIN2 Reference)
**Add Post-Ingestion Audit Phase:**

```markdown
1. Initial Ingestion
   - Extract text, code, structure
   - Create knowledge entries

2. Coverage Audit (NEW)
   - User-guided section verification
   - "What do you know about X?" queries
   - Gap identification

3. Targeted Re-ingestion
   - Focus on identified gaps
   - Extract missed examples
   - Capture missing concepts

4. Validation
   - Confirm gaps filled
   - Cross-reference check
   - Trust level assignment
```

### Audit Questions Template
```markdown
For Section: [Section Name]
- Can you explain the concept of [X]?
- Show me code examples for [Y]
- What are the parameters for [Z]?
- How does [A] relate to [B]?
```

## Implementation Priority

### 🔴 CRITICAL - Do These First (Maximum P2 Advancement)
1. **Silicon Doc Audit** - Absolute bible, must be >95% complete
2. **SPIN2 Language Reference Audit** - Core language understanding

These two sources will provide the most dramatic and immediate advancement in P2 understanding.

### Following Priority
3. **Edge Module Manuals** - Hardware developers use daily
4. **RevC Board Manual** - Community development platform
5. **P1 Documentation** - Migration and reference

## Success Metrics

- Silicon Doc: >95% concept coverage
- Hardware Manuals: 100% specification coverage
- P1 Docs: Core instruction set fully mapped
- Cross-references: All P1→P2 migrations documented

---

*Created: 2025-08-23*
*Purpose: Ensure no critical sources are forgotten*
*Note: Showering is indeed excellent for planning! 🚿💡*