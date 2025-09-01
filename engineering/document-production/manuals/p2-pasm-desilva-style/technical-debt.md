# Technical Debt: De Silva Style Manual

## Purpose
Track improvement opportunities identified during MVP development that we're intentionally deferring to maintain velocity.

**Critical Rule**: NEVER lose an observation. When in doubt, write it down here immediately. We can prioritize later, but we can't recover lost insights.

## Quick Capture Section (Unprocessed Observations)
*Drop new observations here immediately, organize later*

- [2025-08-23] Consider how error messages could teach rather than just report
- [2025-08-23] What if each chapter had a "confidence check" before proceeding?
- [2025-08-23] Pattern noticed: Learners need "permission" to experiment
- [Add new observations here with date]

## MVP Definition (What We're Shipping First)
- ✅ Complete pedagogical structure (Chapters 1-16)
- ✅ All code examples work
- ✅ Basic exercises present
- ✅ Medicine Cabinet for complex topics
- ✅ Consistent deSilva voice
- ✅ LaTeX/PDF generation working

## Deferred Enhancements (Post-MVP)

### 1. Enhanced Pedagogical Patterns
**Opportunity**: Add more learning theory applications
- Spaced repetition in review sections
- Misconception theory for error messages
- Learning dependency graphs for prerequisites
**Value**: Better retention and learning paths
**Effort**: Medium
**Priority**: P2

### 2. Content Maturity Tracking
**Opportunity**: Mark each section's completeness level
- Skeleton → Draft → Complete → Polished → Production
**Value**: Clear progress visibility
**Effort**: Low
**Priority**: P3

### 3. Exercise Progression Framework
**Opportunity**: Formalize exercise difficulty ladder
- Observation → Modification → Extension → Creation → Investigation
**Value**: Better skill building
**Effort**: Medium
**Priority**: P2

### 4. Cross-Reference System
**Opportunity**: Systematic forward/backward references
- "See Chapter X" standardization
- Prerequisite mapping
**Value**: Better navigation and learning paths
**Effort**: High
**Priority**: P3

### 5. Voice Calibration Library
**Opportunity**: Create phrase book for consistency
- Common transitions
- Explanation patterns
- Encouragement phrases
**Value**: Consistency across sessions/authors
**Effort**: Low
**Priority**: P2

### 6. Expanded Medicine Cabinet
**Opportunity**: More types of simplification
- Analogy medicine
- Black-box medicine  
- Good-enough medicine
**Value**: Better differentiation for learners
**Effort**: Low per instance
**Priority**: P1 (can add incrementally)

### 7. Visual Learning Aids
**Opportunity**: Diagrams and visualizations
- COG/Hub interaction diagrams
- Timing diagrams
- Pin state visualizations
**Value**: Multiple learning styles supported
**Effort**: High
**Priority**: P2

### 8. Interactive Elements
**Opportunity**: If platform supports
- Inline code runners
- Interactive timing calculators
- Visual flag simulators
**Value**: Active learning
**Effort**: Very High
**Priority**: P3

### 9. Community Feedback Integration
**Opportunity**: Process for incorporating user feedback
- Common stumbling blocks
- Frequently asked clarifications
- Success stories
**Value**: Continuous improvement
**Effort**: Ongoing
**Priority**: P1 (post-release)

### 10. Completeness Verification
**Opportunity**: Systematic coverage checking
- All instructions documented
- All addressing modes shown
- All flags explained
**Value**: Reference completeness
**Effort**: Medium
**Priority**: P1 (before final release)

## Decision Log

### Why MVP First?
1. **Get to technical review faster** - Find real issues early
2. **Validate approach** - Ensure format works before perfecting
3. **Maintain momentum** - Ship something useful now
4. **Learn from use** - Real feedback better than speculation

### What Makes It "Viable"?
- Learner can actually learn PASM2
- Examples actually run
- Progression actually works
- Voice is actually engaging

### What We're NOT Compromising On
- Code correctness
- Basic pedagogical flow
- deSilva voice/spirit
- Visual formatting (as defined in template)

## Implementation Strategy

**Phase 1 (MVP)**: Get it complete and correct
**Phase 2 (Post-Review)**: Add P1 items based on review feedback  
**Phase 3 (Community)**: Add P2 items based on usage patterns
**Phase 4 (Polish)**: P3 items if demand justifies

## Success Metrics

**MVP Success**:
- Technical reviewer can follow along
- Code examples execute correctly
- No major pedagogical gaps
- PDF generates cleanly

**Future Success**:
- Community adoption
- Reduced support questions
- Positive feedback on learning experience
- Completion rates

---

*Last Updated: 2025-08-23*
*Status: Actively collecting debt during MVP development*