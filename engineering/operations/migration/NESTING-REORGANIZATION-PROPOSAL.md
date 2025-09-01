# Sources/Sources Nesting Reorganization Proposal

**Date**: 2025-09-01
**Purpose**: Fix improper nesting and establish logical structure for ingestion materials

## Current Situation

We have `/engineering/ingestion/sources/sources/` which contains central infrastructure that should be at the same level as individual project directories.

## Key Insight

Your observation is correct: We have two distinct types of content:
1. **Central/Cross-Ingestion Analysis** - Questions and tracking that span ALL ingestions
2. **Individual Project Ingestions** - Specific extractions for each source document

## REVISED Proposed Reorganization (After Careful Analysis)

### 1. INDIVIDUAL INGESTION AUDITS (Move to respective project folders)

**These are project-specific audits that belong with their sources:**

- `PASM2-MANUAL-EXTRACTION-AUDIT.md` → `/engineering/ingestion/sources/pasm2-manual/`
- `silicon-extraction-audit.md` → `/engineering/ingestion/sources/silicon-doc/`
- `spin2-extraction-audit.md` → `/engineering/ingestion/sources/spin2-v51/`
- `datasheet-audit-report.md` → `/engineering/ingestion/sources/[datasheet-project]/`
- `spec-sheet-audit-report.md` → `/engineering/ingestion/sources/[spec-sheet-project]/`
- `p2docs-validation-report.md` → `/engineering/ingestion/sources/[p2docs-project]/`
- `pasm2-spreadsheet-audit.md` → `/engineering/ingestion/sources/p2-instructions-csv/`
- `terminal-window-completeness-audit.md` → `/engineering/ingestion/sources/[terminal-project]/`
- `marketing-docs-knowledge-contributions.md` → `/engineering/ingestion/sources/[marketing-project]/`

### 2. CENTRAL ANALYSIS HUB (Cross-Ingestion Infrastructure)
**Create**: `/engineering/ingestion/central-analysis/`

**Move these MASTER tracking files from sources/sources/analysis/:**
- `FINAL-REMAINING-QUESTIONS-CONSOLIDATED.md` → Master question tracking
- `INSTRUCTION-COMPLETION-MASTER-TRACKING.md` → Cross-source instruction tracking
- `comprehensive-questions-master.md` → Compiled from ALL sources
- `knowledge-gaps-consolidated.md` → Consolidated gaps from all ingestions
- `p2-knowledge-gaps-master.md` → Master P2 knowledge tracking
- `source-conflicts-trust-zones.md` → Cross-source conflict resolution
- `V2-MASTER-SUMMARY-REPORT.md` → Overall V2 extraction summary
- `all-questions-with-sources-categorized.md` → Categorized question matrix
- `FINAL-SCREENSHOT-NEEDS-V2.md` → Screenshots needed across all docs
- `who-to-ask-remaining-questions.md` → Contact routing for questions
- `marketing-docs-cross-source-qa.md` → Cross-source Q&A validation

### 3. Files Needing Further Classification

**These need review to determine if project-specific or cross-ingestion:**
- `code-generation-vs-deployment-gaps.md` - Likely cross-ingestion
- `instruction-description-status.md` - Could be either
- `missing-content-requests.md` - Likely cross-ingestion  
- `p2-documentation-audit.md` - Needs review
- `p2-market-applications.md` - Different category (marketing?)
- `questions-for-chip-language-focused.md` - Cross-ingestion questions
- `screenshot-requirements-comprehensive.md` - Cross-ingestion needs
- `datasheet-style-analysis.md` - Style guide (different category?)
- `spec-sheet-style-analysis.md` - Style guide (different category?)
- `work-session-summary-20250814.md` - Work log (operations?)
- `extraction-audit-report.md` - Needs review
- `pasm-formatting-reference/` - Reference material (different category?)

### 2. INGESTION METADATA
**Create**: `/engineering/ingestion/ingestion-metadata/`

**Move these from sources/sources/:**
- `EXTRACTION-INDEX-V2.md` → Index of all V2 extractions
- `EXTRACTION-INDEX.md` → Original extraction index
- `V1-TO-V2-MIGRATION-AUDIT.md` → Migration tracking
- `V2-MIGRATION-COMPLETE.md` → Migration completion status
- `extraction-health-status.md` → Overall extraction health
- `README.md` → Sources documentation

**Rationale**: These track the ingestion process itself, not specific content.

### 3. VISUAL ASSETS CATALOG
**Create**: `/engineering/ingestion/visual-assets-catalog/`

**Move from sources/sources/visual-assets/:**
- All image catalog files
- Extraction matrices for images
- Visual asset tracking documents
- Actual image files

**Rationale**: Visual assets span multiple ingestions and need central tracking.

### 4. PASM2 MANUAL DEVELOPMENT
**Keep at**: `/engineering/ingestion/sources/pasm2-manual-development/`

**Move from sources/sources/pasm2-manual-development/:**
- Move the subdirectory up one level to be peer with other projects

**Rationale**: This is actually a specific ingestion project, should be at same level as other projects.

### 5. DIRECTORIES TO REMOVE (Empty or Obsolete)

**Remove these empty directories:**
- `sources/sources/extractions/` → Empty
- `sources/sources/extractions-v1-archived/` → V1 archived, in .gitignore
- `sources/sources/format-analysis/` → Empty
- `sources/sources/originals/` → Only has .DS_Store
- `sources/sources/working/` → Empty

**Then remove:**
- `sources/sources/` → Will be empty after all moves

## Summary of New Structure

```
/engineering/ingestion/
├── central-analysis/          # Cross-ingestion questions & tracking
│   ├── questions/             # All question tracking files
│   ├── gaps/                  # Knowledge gap analysis
│   └── conflicts/             # Cross-source conflicts
├── ingestion-metadata/        # Process tracking & indices
├── visual-assets-catalog/     # Central image & visual tracking
└── sources/                   # Individual project ingestions
    ├── desilva-p1-tutorial/
    ├── edge-32mb-module/
    ├── pasm2-manual/
    ├── pasm2-manual-development/  # Moved up from nested
    ├── smart-pins/
    └── [other projects...]
```

## Key Discovery!

✅ **We FOUND the individual ingestion audits!** They were mixed in with the cross-ingestion files in `sources/sources/analysis/`. Files like:
- `PASM2-MANUAL-EXTRACTION-AUDIT.md` (specific to PASM2 manual)
- `silicon-extraction-audit.md` (specific to Silicon Doc)
- `spin2-extraction-audit.md` (specific to Spin2 docs)

These need to be moved to their respective project folders!

## Benefits

1. **Clear Separation**: Central analysis vs. individual ingestions
2. **No More Nesting**: Eliminates confusing sources/sources/ structure  
3. **Individual Audits with Projects**: Each ingestion gets its audit report
4. **Central Tracking Preserved**: Master questions and gaps stay central
5. **Logical Organization**: Easy to find both project-specific and cross-project info
6. **Scalable**: Can add new ingestions without affecting central tracking
7. **Discoverable**: Clear where to look for master questions/gaps

## Execution Plan

1. Create new directories
2. Move files in logical groups
3. Update all references in documentation
4. Remove empty directories
5. Update mapping.csv with all moves
6. Verify no broken references

## Questions for User

1. Does this structure make sense for your workflow?
2. Should we further subdivide central-analysis into subdirectories?
3. Any specific files you want handled differently?
4. Should visual-assets-catalog be under document-production instead?

**Ready for your review and approval!**