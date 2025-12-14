# Repository Technical Debt

**Purpose**: Track known issues that need cleanup but aren't blocking current work.

**Last Updated**: 2025-12-06

---

## Active Debt Items

### 1. Hardcoded Local Paths in Scripts

**Status**: Open
**Priority**: Medium
**Discovered**: 2025-12-06

**Problem**: ~100 Python scripts contain hardcoded absolute paths like:
```python
Path("/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/...")
```

**Impact**:
- Scripts won't work if repo is cloned to different location
- Paths reference old organization name (IronSheepProductionsLLC vs ironsheep)
- Not portable across machines

**Affected Locations**:
- `engineering/scripts/extraction/*.py`
- `engineering/scripts/cleanup/*.py`
- `engineering/scripts/analysis/*.py`
- `engineering/knowledge-base/P2-support/extractors/*.py`
- `engineering/tools/obex-integration/*.py`
- Various other internal scripts

**Fix Required**:
- Convert to relative paths from repository root
- Use `Path(__file__).parent` pattern for script-relative paths
- Or use environment variable for base path

**Cleanup Approach**:
- Fix scripts as we encounter them during normal work
- When entering an area with hardcoded paths, convert to relative paths
- No need for bulk fix - incremental cleanup is acceptable

---

### 2. Sprint History JSON References

**Status**: Open
**Priority**: Low
**Discovered**: 2025-12-06

**Problem**: `engineering/history/sprints/checkpoint-new-published-data/checkpoint-new-published-data-plan.md` contains:
```json
"$schema": "https://github.com/IronSheepProductionsLLC/P2-Knowledge-Base/schemas/p2-v1.0.json"
```

**Impact**: Historical document, schema URL is wrong but document is archival

**Fix**: Low priority - document is historical reference only

---

### 3. Environment Protocols Not Externalized

**Status**: Open
**Priority**: Low
**Discovered**: 2025-12-06

**Problem**: Container vs host-native environment detection rules are summarized in CLAUDE.md (~15 lines) but could be a standalone document for completeness.

**Impact**: Minor - current summary is functional, just not as detailed as other externalized content.

**Fix**: Extract to `engineering/operations/ENVIRONMENT-PROTOCOLS.md` when time permits.

---

### 4. Ingestion Work Modes Too Heavy

**Status**: Open
**Priority**: Low
**Discovered**: 2025-12-06

**Problem**: Two ingestion work mode files are oversized for "quick guides":
- `document-ingestion-focused.md` - 631 lines
- `image-extraction-focused.md` - 698 lines

**Impact**: These load more context than necessary for session start. Should be ~200-400 lines for quick guides.

**Fix**: Split each into quick guide (~200 lines) + full methodology (remainder). Do when next working on ingestion.

---

### 5. PDF Directory Structure Inconsistency (RESOLVED 2025-12-06)

**Status**: Resolved
**Priority**: Medium
**Discovered**: 2025-12-06

**Problem**: Some inconsistency between documentation on PDF directory naming conventions.

**Resolution**:
- Created `PDF-PRODUCTION-ARCHITECTURE.md` as central reference
- Updated `PDF-CLAUDE-RULES.md` with cardinal rule about edit locations
- Updated `STARTUP-BY-WORK-TYPE.md` to route to architecture doc first
- Cleaned up folder alignment (removed `color-bar-test`, created `p2-single-step-debugger-manual` outbound)

---

### 6. work-mode-lifecycle.md May Need Update

**Status**: Open
**Priority**: Low
**Discovered**: 2025-12-06

**Problem**: May need update to reference new refactored CLAUDE.md appropriately.

**Impact**: Minor - document may have stale references.

**Fix**: Review and update during next operational work.

---

### 7. DOD v3.2 Bootstrap System - Legacy Cleanup

**Status**: Open
**Priority**: Low
**Discovered**: 2025-12-14

**Problem**: After implementing the v3.2 single-bounce bootstrap system (`deliverables/ai-reference/BOOTSTRAP.md`), several legacy files and references remain from the old v2.x two-stage bootstrap approach.

**Legacy Files to Remove**:
```
manifests/
├── ai-bootstrap-unix.yaml       # OLD - replaced by BOOTSTRAP.md
├── ai-bootstrap-windows.yaml    # OLD - replaced by BOOTSTRAP.md
├── ai-bootstrap-ultra-minimal.yaml  # OLD - no longer needed
└── ai-instructions.yaml         # Review - refresh-kb.sh may still reference
```

**Files with Outdated References**:
- `engineering/ai-integration/README.md` - References old `manifests/ai-instructions.yaml` system
- `engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md` - References ai-instructions.yaml
- `manifests/propeller-knowledge-root.yaml` - May need update or removal

**What Changed**:
- v3.2 uses single `BOOTSTRAP.md` file (markdown, not YAML) for both platforms
- WebFetch returns markdown verbatim (unlike YAML which gets summarized)
- `refresh-kb.sh` handles all downloads (scripts, index, common files)
- No more two-stage bootstrap or heredoc script creation

**Fix Approach**:
- Remove old bootstrap YAML files from manifests/
- Update `engineering/ai-integration/README.md` to document v3.2 system
- Verify `refresh-kb.sh` doesn't depend on removed files
- Keep `engineering/operations/sprints/dod-v3-sprint-plan.md` as historical reference

**Impact**: Low - old files don't break anything, just clutter

---

## Resolved Debt Items

### GitHub URL Organization Name (FIXED 2025-12-06)

**Problem**: Public-facing URLs used `IronSheepProductionsLLC` instead of `ironsheep`

**Fixed Files**:
- README.md
- CHANGELOG.md
- CLAUDE.md, CLAUDE-REFACTORED.md, CLAUDE-QUICKSTART.md
- manifests/ai-instructions.yaml
- manifests/propeller-knowledge-root.yaml
- deliverables/ai-reference/README.md
- deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md
- engineering/operations/guides/ai-privacy-guide-v1.0.md
- engineering/release-prep/ai-packages/README-template.md
- engineering/history/releases/v1.0-release-notes.md
- engineering/operations/obex-path-analysis.md

**Correct URL**: `https://github.com/ironsheep/P2-Knowledge-Base`

---

## Adding New Debt Items

When you discover technical debt:

1. Add entry to this document with:
   - Status (Open/In Progress/Resolved)
   - Priority (High/Medium/Low)
   - Discovery date
   - Problem description
   - Impact assessment
   - Affected locations
   - Fix approach

2. Don't block current work for cleanup
3. Fix incrementally as you work in affected areas

---

*Technical debt is normal. Tracking it prevents forgetting. Fixing it incrementally prevents accumulation.*
