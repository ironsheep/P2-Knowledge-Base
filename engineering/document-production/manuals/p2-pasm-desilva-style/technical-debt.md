# Technical Debt: De Silva Style Manual

## Purpose
Track improvement opportunities identified during MVP development that we're intentionally deferring to maintain velocity.

**Critical Rule**: NEVER lose an observation. When in doubt, write it down here immediately. We can prioritize later, but we can't recover lost insights.

## Quick Capture Section (Unprocessed Observations)
*Drop new observations here immediately, organize later*

- [2025-08-23] Consider how error messages could teach rather than just report
- [2025-08-23] What if each chapter had a "confidence check" before proceeding?
- [2025-08-23] Pattern noticed: Learners need "permission" to experiment
- [2025-12-09] ~~Consider reducing base font size from 12pt to 11pt to match P2 Assembly Language Manual~~ **DONE 2025-12-12**: Changed to 11pt in p2kb-desilva.latex
- [2025-12-12] **USER REQUEST**: Copy button for code blocks - users report difficulty copying code from PDFs
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

### 11. Code Block Copy Functionality (USER REQUEST)
**User Feedback**: Users report difficulty copying code from the PDF. They want a "copy button" on code blocks.

**The Challenge**: PDFs are static documents - they don't support JavaScript interactivity like web pages. A copy button requires JavaScript to capture clicks and write to clipboard.

**Specific Problems with PDF Copy/Paste**:
1. **Line numbers get copied** - When selecting code, the line numbers rendered in the margin are included in the clipboard, requiring manual cleanup
2. **Leading whitespace not preserved** - The indentation critical for both PASM2 and Spin2 is not accurately captured during copy/paste operations

These issues make copied code unusable without significant manual editing - a major friction point for learners trying to experiment with examples.

**Potential Options**:

1. **Improve PDF text selection** (Low effort)
   - Verify code blocks render as selectable text (not images)
   - Test across PDF readers (Adobe, Preview, browser-based)
   - Document best practices for users ("select all text in block, Cmd+C")

2. **Companion HTML version** (Medium effort)
   - Generate HTML alongside PDF using Pandoc
   - Add JavaScript copy buttons (highlight.js, Prism, or custom)
   - Host on GitHub Pages or similar
   - Users choose PDF for reading, HTML for copying

3. **Companion code repository** (Medium effort)
   - Create GitHub repo with all code examples as downloadable files
   - Organize by chapter/section
   - Link from PDF (static URLs) or README

4. **Local file links in PDF** (Medium effort) - PROMISING
   - Distribute PDF with companion `code-examples/` folder (as ZIP download)
   - Each code block includes hyperlink to `./code-examples/chapter-03/example.spin2`
   - User clicks link → file opens in their editor with proper formatting preserved
   - Could automate link generation via Lua filter during PDF build
   - **Caveat**: Links resolve relative to PDF location; if user moves PDF without folder, links break
   - **Caveat**: PDF reader support varies (Adobe Reader handles relative links well, others may differ)
   - **Advantage**: Self-contained distribution, no web hosting needed, works offline

5. **QR codes linking to web-hosted code** (High effort)
   - Generate QR code for each significant code block
   - QR links to web page with copyable version
   - Complex to implement and maintain

6. **PDF JavaScript via insDLJS/AcroTeX** (Medium-High effort)
   - LaTeX package `insDLJS` (part of AcroTeX bundle) CAN embed JavaScript in PDFs
   - See: [JavaScript in PDF using LaTeX](https://gehrcke.de/2010/11/javascript-in-pdf-using-latex/)
   - See: [Techniques of Introducing Document-level JavaScript](https://tug.org/TUGboat/tb22-3/tb72story.pdf)
   - **MAJOR CAVEAT**: Only works in Adobe Acrobat/Reader
   - Preview (Mac), browser viewers, Foxit, etc. do NOT support PDF JavaScript
   - Security settings often block functionality
   - Would require users to use Adobe Reader specifically
   - **Worth investigating** but may not be practical for broad audience

**Recommended Investigation Path**:
1. First verify current PDF text selection works well
2. If selection is problematic, investigate HTML companion
3. Consider companion repo for complete examples

**Value**: Significantly improved user experience for code reuse
**Effort**: Varies by approach (Low to High)
**Priority**: P1 - Direct user feedback
**Status**: Needs investigation

### 12. Tables and Blocks Rendering Issues (Known Limitation)
**Issue**: Several tables and tcolorbox blocks have rendering problems in the PDF output.

**Observed Problems**:
1. **Tables inside tcolorbox** - Tables inside Medicine Cabinet, Your Turn, and other pedagogical boxes may not render correctly. LaTeX longtable and tcolorbox don't interact well by default.
2. **Wide tables with many columns** - Tables with 4+ columns can cause column overlap when content is too wide for page margins.
3. **Code blocks inside nested environments** - Code blocks inside antipattern divs were rendering with wrong colors (fixed in v1.1.0 via Lua filter changes).

**Root Causes**:
- Pandoc generates longtable for markdown tables, which doesn't work well inside tcolorbox
- No explicit column width control in markdown pipe table syntax
- Multiple Lua filters processing nested content can cause unexpected interactions

**Potential Solutions** (for future releases):
1. **Custom Lua filter for tables** - Detect tables inside tcolorbox and convert to tabular with explicit widths
2. **Markdown table width hints** - Use HTML comments or attributes to suggest column widths
3. **Pre-processor for problematic tables** - Convert specific tables to raw LaTeX in markdown
4. **tcolorbox configuration** - Investigate `before upper` hooks to handle tables

**Workarounds for v1.1.0**:
- Reduce column count where possible (EVENT_* table: 4→3 columns)
- Keep table content brief
- Avoid complex tables inside pedagogical boxes

**Value**: Consistent professional rendering across all content types
**Effort**: High - requires LaTeX expertise and filter development
**Priority**: P2 - Deferred to post-release
**Status**: Documented, not blocking v1.1.0 release

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

*Last Updated: 2025-12-12*
*Status: Actively collecting debt during MVP development*