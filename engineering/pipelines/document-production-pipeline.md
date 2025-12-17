# Document Production Pipeline Tracker

*Last Updated: 2025-12-17*

## Purpose
Track documents we've committed to producing, their current status, and readiness for production.
This is NOT a task list - it's a state tracker for document deliverables.

**Image Asset Integration**: Documents can leverage [Image Extraction Pipeline](../sources/visual-assets/INGESTION-IMAGE-EXTRACTION-MATRIX.md) for visual enhancement - technical debt system tracks available images for each document type.

## Document Production States
- **🔴 Planned**: Identified need, not started
- **🟡 Content Ready**: Source material available, awaiting production
- **🟢 In Production**: Actively being generated
- **✅ Released**: Published and available
- **⏸️ Deferred**: Valid but not current priority

## Documents in Pipeline

### 🔥 **Priority Queue** (September 9th Presentation)

#### P2 Smart Pins Complete Reference  
**Status**: 🟢 In Production (Visual Refinement Phase)  
**Started**: 2025-08-24  
**Source**: Smart Pins rev 5 + 156 total code examples (98 extracted + 58 created)  
**Format**: Professional reference (Content complete, iterating visual presentation)  
**Audience**: P2 developers needing Smart Pin implementation  
**Scope**: All 32 Smart Pin modes with 100% bilingual examples (Spin2 + PASM2)  
**Working Copy**: `workspace/smart-pins-manual/P2-Smart-Pins-Complete-Reference-WORKING.md`  
**Size**: 400+ pages (84KB working copy)  
**Current Work**: Visual refinement using focused methodology (template-only/markdown-only/coupled patterns)  
**Template Stack**: p2kb-foundation + p2kb-smart-pins-content + iron-sheep-tech-review  
**Methodology**: `/documentation/work-mode-guides/smart-pins-visual-refinement.md`  
**Priority**: 🔥 **Validating visual refinement methodology for all future documents**

#### PASM2 User Manual (DeSilva-style)
**Status**: 🟡 Queued (Awaiting Smart Pins Methodology Validation)  
**Source**: Synthesized from extractions + deSilva pedagogical approach  
**Format**: Tutorial document with pedagogical features (multi-part structure)  
**Audience**: Beginning P2 assembly programmers  
**Working Files**: `workspace/desilva-manual/P2-PASM-deSilva-Style-Part*.md` (4 parts)  
**Current Work**: Ready to apply proven visual refinement methodology  
**Template Stack**: p2kb-foundation + p2kb-pasm-desilva-content + iron-sheep-tech-review  
**Methodology**: `/documentation/work-mode-guides/desilva-visual-refinement.md` (adapted)  
**Priority**: 🔥 **Second document to validate cross-document methodology**  
**Workflow**: Multi-part editing → combine → escape → PDF generation

### 📋 **Active Queue**

#### Terminal Window User Guide
**Status**: 🟡 Content Ready  
**Source**: Spin2 documentation extractions  
**Format**: User guide  
**Audience**: Human developers learning P2 debugging  
**Template Stack**: p2kb-foundation + user-guide + iron-sheep-draft  
**Note**: Small manual, good for testing user-guide content layer

#### Single Step Debugger User Guide  
**Status**: 🟡 Content Ready  
**Source**: Spin2 debugger extractions  
**Format**: User guide  
**Audience**: Human developers using P2 debugging tools  
**Template Stack**: p2kb-foundation + user-guide + iron-sheep-draft  
**Note**: Small manual, pairs with Terminal Window guide

#### PASM2 Reference Manual (Parallax Foundation)
**Status**: 🔴 Planned  
**Source**: Parallax foundation + P2KB completion  
**Format**: Official reference documentation  
**Audience**: P2 assembly developers  
**Template Stack**: p2kb-foundation + reference-manual + parallax-official  
**Note**: Large manual, will transition to Parallax branding  
**⚠️ SOURCE CONSIDERATION**: PDF version available (`P2 Spin2 Documentation v51-250425.pdf`) - consider re-ingesting from PDF vs DOCX for better formatting fidelity and visual preservation

#### Spin2 Reference Manual (Parallax Foundation)
**Status**: 🔴 Planned
**Source**: Parallax foundation + P2KB completion
**Format**: Official reference documentation
**Audience**: P2 Spin developers
**Template Stack**: p2kb-foundation + reference-manual + parallax-official
**Note**: Large manual, will transition to Parallax branding

#### P2 XBYTE Bytecode Engine Guide
**Status**: 🔴 Planned
**Source**: Silicon Documentation v35 (lines 1964-2500, 5674, 5991-5997)
**Format**: Tutorial/reference hybrid (like Smart Pins manual)
**Audience**: P2 developers building interpreters, VMs, or bytecode-based systems
**Template Stack**: p2kb-foundation + tutorial-manual + iron-sheep-tech-review
**Scope**: Complete XBYTE subsystem documentation with working examples
**Content Outline**: See `manuals/p2-assembly-language-manual/audit/user-feedback-audit-2025-12-17.md` § "Opinion: XBYTE Warrants a Dedicated Manual"
**Draft Content**: Full chapter draft in same audit document § "XBYTE Chapter - Complete Rewrite" (relocated from Assembly manual)
**Proposed Chapters**:
1. Introduction (bytecode interpretation concepts)
2. XBYTE Mechanism (8-phase cycle, timing)
3. LUT Table Design (entry format, skip patterns)
4. Configuration Modes (all 9 modes with use cases)
5. Bytecode Routines (design patterns, parameters)
6. Branching & Control (relative/absolute, subroutines)
7. Multiple Bytecode Sets (SETQ2 alternate tables)
8. Debugging (GETBRK state, single-step technique)
9. Complete Examples (Forth inner interpreter, VM, parser)
10. Performance (optimization, cycle counting)

**Rationale**: XBYTE is comparable in scope to Smart Pins - a complete subsystem enabling interpreters, Forth systems, and custom VMs. Too detailed for the Assembly Reference Manual's Part I overview.
**Note**: Medium manual (~50-80 pages estimated)

**Potential Approach - Spin2 Interpreter Integration:**
The Spin2 interpreter source (v51) has been fully analyzed (`sources/spin2-v51/spin-interpreter-v51-complete-analysis.md`). The Spin2 interpreter uses a *traditional* dispatch architecture (word-based vector table, ~20-40 clock overhead) rather than XBYTE (LUT-based EXECF entries, 6-clock overhead). A potential expanded structure:
```
Part I: XBYTE Hardware Engine (Chapters 1-10)
Part II: Case Studies
  - Traditional Dispatch (Spin2 Interpreter TOO)
  - XBYTE vs Traditional Comparison
  - Converting Traditional to XBYTE
```
This would make the manual comprehensive for anyone building bytecode systems, showing both approaches. Decision deferred - noting here to preserve the thought.

### ⏸️ **Deferred Queue**

#### AI Privacy Guide
**Status**: ⏸️ Deferred  
**Source**: To be created  
**Format**: PDF  
**Audience**: Organizations evaluating AI tools  
**Note**: Not P2-related, lower priority for Sep 9th presentation

#### Release Notes v1.0
**Status**: ⏸️ Deferred  
**Source**: Sprint accomplishments  
**Format**: PDF  
**Audience**: Community and stakeholders  
**Note**: Will create after Sep 9th presentation

## 🏗️ Template Architecture Support

### Layered Template System
**Purpose**: Enable rapid, reliable document production  
**Components**:
- **Foundation Layer**: p2kb-foundation.sty (Pandoc compatibility)
- **Content Layers**: reference-manual.sty, tutorial-manual.sty, user-guide.sty  
- **Presentation Layers**: iron-sheep-draft.sty, iron-sheep-tech-review.sty, parallax-official.sty

### Document-Template Matrix
| Document Type | Content Layer | Typical Presentation |
|---------------|---------------|---------------------|
| Reference Manual | reference-manual | iron-sheep-tech-review → parallax-official |
| Tutorial/Pedagogical | tutorial-manual | iron-sheep-tech-review |  
| User Guide | user-guide | iron-sheep-draft |

### Release Lifecycle
```
Draft → Technical Review → Content Release → Parallax Official
  ↓           ↓                 ↓               ↓
draft.sty → tech-review.sty → content.sty → parallax.sty
```

## Production Triggers
Documents move to "In Production" when:
1. Content is fully validated
2. Template stack is tested and ready
3. Audience need is confirmed  
4. Production sprint is scheduled
5. September 9th deadline considerations
6. **Visual assets assessed**: [Image extraction status](../sources/visual-assets/INGESTION-IMAGE-EXTRACTION-MATRIX.md) reviewed for enhancement opportunities

## Visual Asset Integration
**Available Assets**: P2 Edge ecosystem (60 images), Smart Pins documentation (21 images), Spin2 v51 documentation (24 images), P2 Datasheet (40 images), additional extractions pending  
**Enhancement Opportunities**: Documents can be improved with extracted images via [technical debt queue](../technical-debt/VISUAL-ASSETS-DEBT.md)  
**Consumer Registry**: Each image extraction automatically identifies which documents could benefit

## Success Metrics
- **Template reliability**: 100% consistent PDF generation
- **Production speed**: <1 day from content-ready to PDF
- **Branding flexibility**: <30 seconds to change presentation layer
- **Quality**: Zero template debugging cycles per document

## Notes
- **September 9th Priority**: Smart Pins and DeSilva must be production-ready
- **Template System**: Being built concurrently with Smart Pins production
- **Proven Architecture**: Each subsequent document benefits from tested layers
- **Parallax Transition**: Template system enables easy Iron Sheep → Parallax branding