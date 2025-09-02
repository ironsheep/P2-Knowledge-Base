# Standard Ingestion Update Workflow

## Purpose
Systematic process to ensure all central analysis documents are updated after new information is ingested.

## When to Execute
- After receiving new clarifications from Chip Gracey
- After extracting new source documents
- After completing cross-source analysis
- After any significant new findings

## Workflow Steps

### 1. Initial Assessment
- [ ] Identify what new information was obtained
- [ ] List affected knowledge areas
- [ ] Note source authority level (Chip > Silicon Doc > CSV > Others)

### 2. Update Central Analysis Documents

#### Primary Coverage Matrices
- [ ] `/central-analysis/P2-FEATURE-COVERAGE-MATRIX.md`
  - Update coverage percentages
  - Add new discoveries section
  - Update priority gaps
  
- [ ] `/central-analysis/instruction-analysis/instruction-completion-matrix.md`
  - Mark answered questions
  - Update coverage statistics
  - Add new findings section

#### Knowledge Status Documents
- [ ] `/central-analysis/AREAS-NOW-UNDERSTOOD.md`
  - Add newly understood areas
  - Update coverage percentages
  - Document breakthroughs

- [ ] `/central-analysis/knowledge-gaps/gaps-consolidated.md`
  - Strike through resolved gaps
  - Update percentages
  - Add "Recently Resolved" section

#### Instruction Documentation
- [ ] `/central-analysis/P2-COMPLETE-INSTRUCTION-MATRIX.md`
  - Add new instruction details
  - Update group summaries
  - Note timing discoveries

- [ ] `/central-analysis/P2-INSTRUCTION-COVERAGE-REPORT.md`
  - Update instruction counts
  - Revise coverage percentages

#### Specialized Documents
- [ ] `/central-analysis/instruction-analysis/PTRA-PTRB-FINDINGS.md`
  - Add pointer-related discoveries
  
- [ ] `/central-analysis/SMART-PINS-SOURCE-COMPARISON.md`
  - Update mode coverage
  - Note conflicts/confirmations

- [ ] `/central-analysis/instruction-analysis/KNOWN-BUGS-CRITICAL.md`
  - Add newly discovered bugs
  - Update workarounds

### 3. Update Source Documents

#### For New Clarifications
- [ ] Create/update `/sources/chip-gracey-clarifications/[date].md`
- [ ] Update ingestion README with new source

#### For New Extractions
- [ ] Create narrative file in appropriate source directory
- [ ] Update source README
- [ ] Create cross-source connections

### 4. Cross-Reference Updates

#### Question Tracking
- [ ] Update questions marked as answered
- [ ] Cross-reference answer sources
- [ ] Update "who to ask" documents

#### Gap Analysis
- [ ] Review and update gap categories
- [ ] Adjust priority rankings
- [ ] Update recommended next steps

### 5. Documentation Quality

#### Verification Steps
- [ ] Ensure dates are updated
- [ ] Check percentage calculations
- [ ] Verify cross-references work
- [ ] Confirm no contradictions introduced

#### Consistency Checks
- [ ] Coverage percentages consistent across docs
- [ ] Terminology consistent
- [ ] Authority levels properly noted

### 6. Commit and Track

#### Git Operations
- [ ] Stage all updated files
- [ ] Create descriptive commit message
- [ ] Reference source of new information

#### Progress Tracking
- [ ] Update project dashboard if needed
- [ ] Note in sprint documentation
- [ ] Update roadmap if applicable

## Example Execution

### Chip Gracey Clarification Example (2025-09-02)
1. **New Info**: Extended precision patterns, 6 instructions
2. **Updated**:
   - P2-FEATURE-COVERAGE-MATRIX: Added Extended Precision Math at 95%
   - instruction-completion-matrix: Marked 14 questions answered
   - AREAS-NOW-UNDERSTOOD: Added section 9 for extended precision
   - gaps-consolidated: Added "Recently Resolved" section
3. **Result**: Coverage improved from 75% to 76%+

## Automation Opportunities

### Future Improvements
- Script to check all central docs for date staleness
- Automated coverage percentage calculator
- Cross-reference validator
- Gap tracker with automatic updates

## Best Practices

1. **Always update coverage matrices first** - They're the primary reference
2. **Keep historical context** - Use strikethrough, don't delete
3. **Date everything** - Include update dates in documents
4. **Source attribution** - Always note where information came from
5. **Incremental updates** - Small, focused changes are better than wholesale rewrites

## Quality Checklist

Before considering update complete:
- [ ] All percentages add up correctly
- [ ] No conflicting information introduced
- [ ] Dates updated everywhere
- [ ] New findings properly attributed
- [ ] Cross-references still valid
- [ ] Commit message describes changes
- [ ] No documents forgotten

---

*This workflow ensures comprehensive, consistent updates across the P2 knowledge base whenever new information is ingested.*