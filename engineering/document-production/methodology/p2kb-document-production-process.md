# P2KB Document Production Process
## High-Quality Technical Documentation Pipeline

**Purpose**: Produce consistent, accurate, pedagogically effective P2 technical documentation ready for expert review.

**Last Updated**: 2025-08-21  
**Status**: OFFICIAL PROCESS - Follow for all P2KB documents

---

## Phase 1: Content Development (Accuracy First)

### Prerequisites
- [ ] Creation guide exists for document type
- [ ] Source validation rules defined
- [ ] P2 specifications reference available

### Content Writing Rules
1. **Source Validation - MANDATORY**
   
   **Fully Trusted Sources** (use freely):
   - P2 official datasheet (rev B/C silicon)
   - Chip Gracey's authoritative forum posts
   - P2 verified code from our knowledge base
   - Parallax official P2 documentation
   
   **Less Trusted Sources** (mark explicitly):
   - Community forum posts (non-Chip)
   - Example code without verification
   - Derived/calculated specifications
   
   **When using less trusted sources**:
   ```markdown
   :::review
   🔍 **NEEDS TECHNICAL REVIEW**
   
   Source: Community forum post by [user]
   Claims: CORDIC operation takes X cycles
   Needs verification against datasheet
   :::
   ```
   
   **NEVER use**: P1 specifications or assumptions
   **When uncertain**: Always mark with review box
   
2. **Semantic Markup**
   - Use markdown with clear semantic markers
   - Mark placeholders explicitly: `:::missing`
   - Focus on technical accuracy over formatting

3. **Common P1→P2 Errors to Avoid**
   - Clock speeds: P2 runs 160-300MHz typically (not 50-80MHz)
   - Hub RAM: P2 has 512KB (not 32KB)
   - I/O pins: P2 has 64 (not 32)
   - MIPS: P2 ~100 MIPS @ 200MHz (not 25 @ 50MHz)

### Output
- Markdown document with accurate content
- All uncertain areas marked for review

---

## Phase 2: Style Application (Visual Consistency)

### Setup
1. Verify template is working
2. Test escaping script with regression tests
3. Prepare tracking document

### Visual Pass Process
1. **Generate Initial PDF**
   ```bash
   ./tools/latex-escape-all.sh input.md output.md
   pandoc output.md -o document.pdf --template=template.latex
   ```

2. **Visual Review - Systematic**
   - Review each page noting issues
   - Categorize each issue:
     * **Template**: Fix in .latex file
     * **Content**: Fix in .md file  
     * **Script**: Fix in escaping/processing
   - Record in `visual-fixes-tracking.md`

3. **Fix by Category**
   - Template fixes first (highest leverage)
   - Script fixes second (affects all content)
   - Content fixes last (most numerous)

4. **Iterate Until Clean**
   - Regenerate PDF after each fix category
   - Continue passes until visually correct

### Visual Consistency Checklist
- [ ] Code blocks have correct background (yellow for P2)
- [ ] Inline code formatted correctly (bold, no background)
- [ ] Box types used consistently:
  - Sidetrack: Technical specs, quick facts
  - Interlude: Philosophical insights
  - Your Turn: Exercises (distinct color)
- [ ] No duplicate text in boxes
- [ ] P2 syntax preserved (`#`, `##`, `_` in code)
- [ ] Instructions formatted consistently

---

## Phase 3: Technical Draft Certification

### Quality Gates - ALL MUST PASS
- [ ] **Content Accuracy**
  - All P2 specifications verified against sources
  - No P1 specifications present
  - Technical details cross-checked
  
- [ ] **Visual Consistency**
  - Template styling applied correctly
  - Box usage follows style guide
  - Typography supports pedagogy
  
- [ ] **Completeness Markers**
  - Missing content clearly marked with `:::missing`
  - Review needs marked with `:::review`
  - Diagrams needed marked with `:::diagram`
  
- [ ] **Processing Validation**
  - Escaping script passes regression tests
  - PDF generates without errors
  - All special characters display correctly

### Certification Statement
```markdown
## Technical Draft Certification
Date: [DATE]
Certified by: [NAME]
- [ ] All quality gates passed
- [ ] Ready for technical review
- [ ] Tracking document complete
```

---

## Phase 4: Technical Review

### Preparation
1. Generate clean PDF (no editing marks)
2. Prepare question list for reviewer
3. Include source reference list

### Review Process
1. SME reviews for technical accuracy
2. Collect feedback systematically
3. Update content based on feedback
4. Re-run Phase 2 if structural changes

### Post-Review
- Update content with corrections
- Mark reviewed sections as validated
- Remove review boxes for validated content

---

## Supporting Documents

### Required for Each Document
1. **Creation Guide** (`creation-guide.md`)
   - Document-specific requirements
   - Style decisions
   - Pedagogical approach

2. **Visual Fixes Tracking** (`visual-fixes-tracking.md`)
   - Issue categorization
   - Fix status
   - Patterns discovered

3. **Source Reference** (`sources.md`)
   - List of authoritative sources used
   - Page/section references
   - Validation status

---

## Process Improvements

### Continuous Improvement
- Document friction points as they arise
- Update process based on learnings
- Share patterns across documents

### Regression Prevention
- Add new test cases to escaping script
- Update style guide with decisions
- Document anti-patterns discovered

---

## Quick Reference Card

```bash
# Phase 1: Write content (accuracy first)
- Use ONLY P2 sources
- Mark uncertainty with :::review

# Phase 2: Apply style (visual consistency)
- Generate PDF
- Visual pass → categorize issues
- Fix by category → regenerate
- Iterate until clean

# Phase 3: Certify for review
- Verify all quality gates
- Complete certification checklist

# Phase 4: Technical review
- SME validation
- Update based on feedback
```

---

## Version History
- **v1.0** (2025-08-21): Initial process from De Silva manual experience
- Discovered through iterative refinement on first major document
- Incorporates lessons from Pass 1 and Pass 2 visual reviews