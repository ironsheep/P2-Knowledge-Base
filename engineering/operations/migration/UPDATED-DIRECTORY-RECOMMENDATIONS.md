# Updated Directory Recommendations

*Based on investigation - 2025-09-01*

## ✅ Already Handled
- `tasks/` - Now untracked from git and added to .gitignore (Todo MCP working directory)

## 📊 Revised Recommendations

### 1. `sources/` ⭐ CRITICAL - Must be moved
**Content**: Complete ingestion system (originals, extractions, analysis)
**Action**: → `engineering/ingestion/sources/`
**Reason**: Core ingestion assets belong in engineering

---

### 2. `import/` - External inputs, needs organization
**Content**: External contributions from multiple sources:
- `p2docs-github-io/` - Imported documentation from Ada's site
- `from-pdf-forge/` - PDF forge setup scripts
- `source-code/` - External code samples
- `requirements/` - Project requirements documents
- **Empty dirs to remove**: `parallax-info/`, `pasm2-details/`, `process/`, `p2/images/`

**Action**: → `engineering/ingestion/external-inputs/`
**Reason**: These are external inputs that feed the ingestion pipeline

---

### 3. `Scratchpad/` - Has valuable content to preserve
**Content Found**:
- `DEPLOYMENT-INSTRUCTIONS.md` - PDF deployment guide
- `Part2-StyleWork.md` - De Silva manual chapter work
- `TEST-CHECKLIST.md` - PDF generation testing checklist
- `STACK-RESTORATION-COMPLETE.md` - Session recovery notes

**Action**: 
- Move deployment docs → `engineering/pdf-forge/deployment/`
- Move style work → `engineering/document-production/workspace/desilva-manual/`
- Move test checklist → `engineering/pdf-forge/testing/`
- Then remove Scratchpad/

---

### 4. `pipelines/` - Split by function
**Content**: Mixed methodologies and workflows
**Action**: 
- PDF workflows → `engineering/pdf-forge/guides/`
- Document pipeline → `engineering/document-production/methodology/`
- Model strategies → `engineering/operations/planning/strategies/`
- Task generation → `engineering/operations/methodology/`

---

### 5. `exports/` - PDF generation exports
**Action**: → `engineering/pdf-forge/exports/`

---

### 6. `p2-claude-knowledge/` - Instruction matrices
**Action**: → `engineering/knowledge-base/instruction-matrices/`

---

### 7. `pdf-forge-workspace/` ⚠️ KEEP AT ROOT
**Reason**: Active workspace, user interacts directly with it
**Consider**: Add note in README about this being a working directory

---

### 8. Small directories to move:
- `sprint-candidates/` → `engineering/operations/planning/sprint-candidates/`
- `markets/` → `engineering/operations/planning/markets/`
- `strategic-insights/` → `engineering/history/insights/`
- `for-human/` → `engineering/operations/external-communications/`
- `human-todos/` → `engineering/operations/human-tasks/`
- `presentations/` → `engineering/operations/presentations/`
- `documentation-standards/` → `engineering/operations/standards/documentation/`
- `test_extraction/` → `engineering/tools/extraction/test-output/`
- `test_mini_breakout_images/` → `engineering/tools/extraction/test-images/`
- `extracted_code/` → `engineering/tools/extraction/code-output/`

---

## 🎯 Execution Priority

### Phase 1: Critical Mass Moves
1. `sources/` → engineering/ingestion/sources/
2. `import/` → engineering/ingestion/external-inputs/
3. `exports/` → engineering/pdf-forge/exports/

### Phase 2: Content Organization
4. `pipelines/` → Split across destinations
5. `p2-claude-knowledge/` → engineering/knowledge-base/
6. `Scratchpad/` → Distribute content then remove

### Phase 3: Small Directory Cleanup
7. All remaining small directories

### Keep at Root
- `tasks/` (Todo MCP - now in .gitignore)
- `pdf-forge-workspace/` (active workspace)
- Hidden directories (.personnel-observations/, .strategic-commentary/, etc.)

## 📝 Summary

**After these moves:**
- Root will have ~8 directories (down from current ~25)
- Two main directories (deliverables/, engineering/) + working areas
- All ingestion materials consolidated in engineering/ingestion/
- All PDF work consolidated in engineering/pdf-forge/
- External inputs properly categorized

**Special Notes:**
- `tasks/` now properly untracked from git
- Several empty directories can be removed during migration
- Scratchpad content should be preserved before removal
- pdf-forge-workspace stays as active working area

---
*This completes the directory analysis with your inputs incorporated*