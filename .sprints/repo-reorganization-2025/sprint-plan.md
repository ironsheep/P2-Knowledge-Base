# Repository Reorganization Sprint Plan

**Sprint Tag**: `repo-reorg-2025`  
**Start Date**: 2025-08-31  
**Purpose**: Transform repository structure for public release  
**Critical Goal**: Make repository appear intentionally designed and trustworthy for public consumption

## 🎯 Sprint Objectives

### Primary Goal
Transform the organically-grown repository structure into a clean, professional, audience-focused organization suitable for public release on GitHub.

### Success Criteria
- ✅ Reduced from ~40 directories to 2 main directories + README
- ✅ All content organized by audience and purpose
- ✅ Professional appearance - "intentionally shaped on purpose"
- ✅ Complete git history preservation via git mv
- ✅ All cross-references updated and functional
- ✅ Vision documents integrated into appropriate locations
- ✅ Public-ready structure that builds trust

## 🏗️ Final Structure

```
P2-Knowledge-Base/
├── README.md              # Audience-focused navigation
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── deliverables/          # What users came for
│   ├── ai-reference/
│   ├── developer-docs/    # Download-on-demand system
│   ├── learning-paths/
│   └── reference/
├── engineering/           # How we make it
│   ├── knowledge-base/
│   ├── ingestion/
│   ├── document-production/
│   ├── pdf-forge/
│   ├── tools/
│   ├── operations/
│   └── history/
└── pdf-forge-workspace/   # ⛔️ PROTECTED - Mounted share
```

## 📋 Execution Strategy

### Pattern-Based Sweeps (Ordered)
1. **Work Mode & Methodology Guides** - Clarifies document purposes
2. **Ingestion Materials** - Consolidates source-related content
3. **Dashboard/Status Documents** - Becomes clean READMEs + narrative ABOUT docs
4. **PDF/Document Production** - Organizes active work
5. **Sprint Historical Records** - Archives completed work
6. **Debt Tracking** - Consolidates technical debt
7. **Tool Documentation** - Utilities and scripts

### Critical Protections
- ⛔️ **NEVER TOUCH**: `pdf-forge-workspace/` (mounted share)
- 🔒 **Git Move Only**: Preserve all file history
- 📝 **Track Everything**: CSV mapping of all moves
- 🔗 **Fix References**: Update all cross-references

## 🗂️ Migration Tracking

```
engineering/operations/migration/
├── mapping.csv              # Every file movement
├── edge-cases.md           # Uncertain placements
├── uncertain/              # Temporary holding
├── references-to-fix.md   # Documents with broken refs
└── vision-documents.md     # Found vision docs to integrate
```

## ⚠️ Special Considerations

### Dashboard Cognitive Load Reduction (from Task #984)
During SWEEP 3, split each dashboard into:
- **README.md**: Scannable metrics, status, links only (hunt-and-find optimized)
- **ABOUT.md**: Narrative descriptions and explanations (the "why" context)
This dramatically reduces cognitive load by separating immediate needs from background context.

### Vision Documents
When found during migration, vision documents that describe project goals and system design should be:
1. Cataloged in `vision-documents.md`
2. Evaluated for integration into structure
3. Used to inform final organization
4. Potentially become section READMEs or guidance documents

### Public Release Preparation
- Remove personal observations (already gitignored)
- Clean up temporary/scratch content
- Ensure professional documentation tone
- Verify no sensitive information exposed

## 📊 Task Management

All tasks use tag: `["repo_reorg_2025"]`

### Task Generation Principles
- Paragraph-length descriptions with complete detail
- No edge cases left undefined
- Clear success criteria
- Proper ordering to minimize rework
- Each task self-contained and executable

## 🏁 Completion Verification

### Sprint Complete When:
- [ ] All uncertain/ items resolved
- [ ] No files remain in old locations (except protected)
- [ ] All cross-references updated
- [ ] All work mode guides accurate
- [ ] Vision documents integrated
- [ ] Repository suitable for public release
- [ ] Professional, intentional appearance achieved

---

*This sprint interrupts Sprint 005 but is necessary to enable continued efficient work*