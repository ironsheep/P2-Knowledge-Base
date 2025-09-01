# Ingestion Audit Protocol

## Purpose
Verify completeness of critical source ingestion through interactive audit sessions.

## The "Silicon Doc Problem"
We have "absolute bible" sources that may be incompletely ingested:
- Silicon Doc (P2 hardware reference)
- SPIN2 Language Reference
- Critical instruction sets

Missing even 5% means knowledge gaps at crucial moments.

## Interactive Audit Process

### Phase 1: Section-by-Section Verification

**User Process:**
1. Open source document (e.g., Silicon Doc)
2. Pick a section/chapter
3. Query: "What do you know about [specific topic from section]?"
4. Note response quality:
   - ✅ Complete: Full understanding with examples
   - ⚠️ Partial: Basic understanding, missing details
   - ❌ Missing: No knowledge or wrong section

### Phase 2: Gap Documentation

**For Each Gap Found:**
```markdown
Source: Silicon Doc
Section: 3.4.2 Pin Modes
Gap Type: [Missing|Partial|Wrong]
Expected: Explanation of smart pin mode %01011
Actual: No knowledge of this mode
Priority: [Critical|High|Medium|Low]
```

### Phase 3: Targeted Re-ingestion

**Focus Areas:**
- Code examples that were skipped
- Tables and specifications
- Diagrams and their descriptions
- Cross-references between sections
- Footnotes and warnings

## Audit Question Templates

### Concept Understanding
"Explain the concept of [X] from section [Y]"
- Tests: Conceptual knowledge ingested
- Good response: Clear explanation with context
- Bad response: Vague or missing

### Code Examples
"Show me code examples for [feature] from the manual"
- Tests: Code extraction completeness
- Good response: Actual examples from manual
- Bad response: Generic or missing examples

### Specifications
"What are the parameters for [instruction/mode]?"
- Tests: Technical detail ingestion
- Good response: Complete parameter list with ranges
- Bad response: Partial or missing parameters

### Cross-References
"How does [A] relate to [B] according to the manual?"
- Tests: Relationship understanding
- Good response: Explains connection
- Bad response: No relationship knowledge

## Success Metrics

### Coverage Levels
- **Critical (>95%)**: Core instructions, basic operations
- **High (>90%)**: Common use cases, standard patterns
- **Medium (>80%)**: Advanced features, edge cases
- **Acceptable (>70%)**: Exotic features, rarely used

### Trust Levels After Audit
- **Verified**: Audited and gaps filled
- **Partial**: Audited with known gaps documented
- **Unverified**: Not yet audited
- **Suspect**: Failed audit, needs complete re-ingestion

## Shower Thoughts Integration 🚿

*"Best planning happens in the shower"* - Truth!

### Capture Process
1. Shower insight → Immediate note
2. Note → Audit question
3. Question → Gap discovery
4. Gap → Enhancement task

### Example Shower Insight
"Wait, do we have all the smart pin modes?"
→ Audit question: "List all smart pin modes from Silicon Doc"
→ Gap found: Missing modes %01011, %10110
→ Task: Re-ingest smart pin section with focus on tables

## Technical Climbing Applied

**This audit process is technical climbing:**
- Current ingestion = current position
- Audit = checking our protection
- Gaps = route ahead to climb
- Re-ingestion = placing new protection
- Verified source = protected height achieved

## Implementation Schedule

### Immediate (This Sprint)
1. Silicon Doc audit - highest priority
2. Document all gaps found
3. Create re-ingestion tasks

### Next Sprint
1. SPIN2 Reference audit
2. Fill Silicon Doc gaps
3. Edge manual ingestion

### Future
1. P1 documentation audit
2. Cross-reference verification
3. Trust level certification

## The Payoff

**Short Term**: Know exactly what we're missing
**Medium Term**: Targeted improvements, efficient use of time
**Long Term**: >95% coverage of critical sources, high trust level

---

*Remember: An unaudited ingestion is an unknown quantity. An audited ingestion is a trusted foundation.*

---

*Created: 2025-08-23*
*Inspired by: Shower planning session*