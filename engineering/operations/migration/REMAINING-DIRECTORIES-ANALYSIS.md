# Remaining Directories Analysis & Recommendations

*Based on content investigation - 2025-09-01*

## 📊 Directory Content Analysis & Placement Recommendations

### 1. `sources/` ⭐ MAJOR - Should be moved
**Content**: Complete ingestion system with originals, extractions, analysis
**Size**: Large, core to project
**Contains**:
- `originals/` - Source PDFs and documents
- `extractions/` - Extracted content
- `analysis/` - Instruction completion tracking
- `visual-assets/` - Image extraction matrices
- Various README and INDEX files

**Recommendation**: → `engineering/ingestion/sources/`
**Reason**: This is the heart of the ingestion pipeline and belongs with engineering

---

### 2. `pipelines/` - Should be moved
**Content**: Process documentation, methodologies, workflows
**Contains**:
- PDF generation workflows
- Document production pipeline
- Model selection strategies
- Market strategies
- Task generation processes

**Recommendation**: Split into:
- Methodology docs → `engineering/document-production/methodology/`
- PDF workflows → `engineering/pdf-forge/guides/`
- Strategy docs → `engineering/operations/planning/strategic/`
**Reason**: Content serves multiple purposes and should be distributed by function

---

### 3. `tasks/` - Should be moved
**Content**: Todo MCP backups and sprint tracking
**Contains**:
- `active/current-sprint.md`
- `backups/` with project dumps

**Recommendation**: → `engineering/operations/todo-mcp/`
**Reason**: These are Todo MCP operational files

---

### 4. `exports/` - Should be moved
**Content**: PDF generation exports and templates
**Contains**:
- `pdf-generation/` subdirectory
- `terminal-window-manual/`
- Various export iterations

**Recommendation**: → `engineering/pdf-forge/exports/`
**Reason**: Part of PDF forge system

---

### 5. `pdf-forge-workspace/` ⚠️ ACTIVE WORKSPACE
**Content**: Active PDF forge testing and development
**Contains**:
- `inbox/` for processing
- `output-pdfs/` results
- `templates/` and `filters/`
- Test documents and results

**Recommendation**: KEEP AT ROOT (for now)
**Reason**: This is an active workspace that user interacts with directly. Moving it might break workflows.

---

### 6. `p2-claude-knowledge/` - Should be moved
**Content**: Instruction knowledge matrices
**Contains**:
- Various instruction relationship matrices
- Knowledge framework documents

**Recommendation**: → `engineering/knowledge-base/instruction-matrices/`
**Reason**: These are knowledge base assets

---

### 7. `Scratchpad/` - Can be removed
**Content**: Temporary work files and backups
**Contains**:
- Deployment instructions
- Style work documents
- Archived templates

**Recommendation**: Distribute or archive:
- Deployment docs → `engineering/pdf-forge/deployment/`
- Style work → `engineering/document-production/workspace/`
- Then remove Scratchpad
**Reason**: As you noted, we have scratch areas in work folders where needed

---

### 8. `sprint-candidates/` - Should be moved
**Content**: Sprint planning documents
**Recommendation**: → `engineering/operations/planning/sprint-candidates/`

---

### 9. `markets/` - Should be moved
**Content**: Market analysis document
**Recommendation**: → `engineering/operations/planning/markets/`

---

### 10. `strategic-insights/` - Should be moved
**Content**: Session discoveries
**Recommendation**: → `engineering/history/insights/`

---

### 11. `for-human/` - Special case
**Content**: Bug report for Anthropic
**Recommendation**: → `engineering/operations/external-communications/`

---

### 12. `human-todos/` - Should be moved
**Content**: Human audit checklists
**Recommendation**: → `engineering/operations/human-tasks/`

---

### 13. `presentations/` - Should be moved
**Content**: Unknown (need to check)
**Recommendation**: → `engineering/operations/presentations/`

---

### 14. `documentation-standards/` - Should be moved
**Content**: Unknown (need to check)
**Recommendation**: → `engineering/operations/standards/documentation/`

---

### 15. `test_extraction/` - Should be moved
**Content**: Test extraction output
**Recommendation**: → `engineering/tools/extraction/test-output/`

---

### 16. `test_mini_breakout_images/` - Should be moved
**Content**: Test images
**Recommendation**: → `engineering/tools/extraction/test-images/`

---

### 17. `extracted_code/` - Should be moved
**Content**: Code extraction results
**Recommendation**: → `engineering/tools/extraction/code-output/`

---

### 18. `import/` - Keep or move?
**Content**: Unknown (likely source import files)
**Recommendation**: Check if active, then either:
- → `engineering/ingestion/import/` if part of pipeline
- Keep at root if actively used for imports

---

## 🎯 Priority Order for Movement

### Phase 1: Critical Moves
1. `sources/` → `engineering/ingestion/sources/`
2. `tasks/` → `engineering/operations/todo-mcp/`
3. `exports/` → `engineering/pdf-forge/exports/`

### Phase 2: Knowledge Organization
4. `p2-claude-knowledge/` → `engineering/knowledge-base/instruction-matrices/`
5. `pipelines/` → Split across multiple destinations

### Phase 3: Cleanup
6. `Scratchpad/` → Distribute and remove
7. Test directories → `engineering/tools/`
8. Small directories → Appropriate locations

### Phase 4: Decision Required
- `pdf-forge-workspace/` - Keep at root? (active workspace)
- `import/` - Check usage first

## ⚠️ Cautions

1. **pdf-forge-workspace/** appears to be actively used - moving might break user workflows
2. **import/** needs investigation before moving
3. Some **pipelines/** content belongs in multiple places - needs careful splitting
4. **Scratchpad/** has some deployment docs that might be important

## 📝 Next Steps

1. Confirm which directories are actively used
2. Create detailed move plan for pipelines/ content split
3. Backup before major moves
4. Execute in phases to minimize disruption

---
*This completes the remaining ~18 directories investigation*