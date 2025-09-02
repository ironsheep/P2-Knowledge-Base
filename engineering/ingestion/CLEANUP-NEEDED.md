# Ingestion Cleanup Tracking

**Created**: 2025-09-02  
**Purpose**: Track duplicate extractions and other cleanup needs discovered during reconnection

---

## ⚠️ CRITICAL: Source Fidelity Assessment

**KEY FINDING**: Multiple extractions often exist because DOCX vs PDF extraction yields different fidelity
- **DOCX**: Better narrative flow, formatted text, table structure
- **PDF**: Better visual layout, exact positioning, may lose tables/formatting in extraction
- **DECISION RULE**: Always keep the RICHEST source (most complete information)

### Fidelity Comparison Needed
Before consolidating, we must:
1. Compare information completeness between DOCX and PDF extractions
2. Identify unique content in each version
3. Merge to create richest possible composite
4. Document which source was authoritative for which sections

---

## 🔴 DUPLICATE EXTRACTIONS (Need Consolidation)

### spin2-v51/
**Multiple Audit Documents Found**:
- `spin2-v51-complete-extraction-audit.md` ← Should be PRIMARY
- `spin2-extraction-audit.md` ← Older version, merge and remove
- `spin-manual-draft-2024-complete-audit.md` ← Draft version, check for unique content
- `spin-manual-draft-2024-extraction.md` ← Draft extraction, merge if needed
- `terminal-window-completeness-audit.md` ← Specialized, might keep separate
**Action**: Consolidate into single `spin2-v51-complete-extraction-audit.md`

### silicon-doc/
**Multiple Audit Documents Found**:
- `silicon-doc-complete-extraction-audit.md` ← Should be PRIMARY
- `silicon-extraction-audit.md` ← Older version, merge and remove
- `assets/extraction-audit.md` ← Misplaced, should be in assets readme
**Multiple Text Extractions**:
- `p2-documentation.txt` ← Should be PRIMARY narrative
- `silicon-doc-complete-sample.txt` ← Sample only, clarify purpose
- `assets/part3-text.txt` ← Partial, should be consolidated
- `assets/part4-text.txt` ← Partial, should be consolidated
- `assets/part5-text.txt` ← Partial, should be consolidated
**Action**: Consolidate audits, merge text files into single narrative

### smart-pins/
**Multiple Text Files**:
- `smartpins-narrative-from-docx.txt` ← From DOCX source
- `smartpins-text-fresh.txt` ← Unclear which is authoritative
- `smartpins-text.txt.deprecated` ← Should be removed
**Nested Extraction Directory**:
- `smart-pins-manual-extraction/` ← Contains another extraction-audit.md
**Action**: Determine authoritative text, remove deprecated, flatten structure

### pasm2-manual/ 🚨 CRITICAL - DOCX IS GOLD
**Multiple Documents**:
- `pasm2-manual-complete-extraction-audit.md` ← Current primary
- `PASM2-MANUAL-EXTRACTION-AUDIT.md` ← Older format
- `pasm2-manual-docx-extraction.md` ← **10,771 PARAGRAPHS! KEEP AT ALL COSTS!**
**CRITICAL FINDING**: DOCX has 10,771 paragraphs, 219 tables, 362 code examples
**Action**: DOCX extraction is authoritative - merge others INTO it, not vice versa

### p2-eval-board/
**Multiple Audit Documents**:
- `p2-eval-board-rev-c-complete-extraction-audit.md` ← Hardware specific
- `p2-hardware-manual-complete-extraction-audit.md` ← Different document?
**Action**: Verify if these are different documents or duplicates

---

## 🟡 STRUCTURAL ISSUES

### Missing Standardization
- **Inconsistent Naming**: Some use CAPS, some lowercase, some mixed
- **File Extensions**: Some `.md` files should clarify their purpose
- **Directory Structure**: Some have nested `assets/`, some don't

### Misplaced Files
- `extraction-audit.md` files in assets directories
- Code examples as individual .txt files instead of consolidated
- Style analysis only in 2 sources (p2-datasheet, p2-spec-sheet)

---

## 🟢 CLEANUP PRIORITIES

### Phase 1: Consolidate Duplicates
1. For each source with multiple extractions:
   - Identify the most complete/recent version
   - Merge unique content from others
   - Create single authoritative document
   - Archive or delete duplicates

### Phase 2: Standardize Naming
1. Adopt consistent pattern:
   - `[source-name]-complete-extraction-audit.md` - Main audit
   - `[source-name]-narrative.txt` - Full text extraction
   - `[source-name]-cross-source-analysis.md` - Hub connection
   - `[source-name]-style-analysis.md` - Style analysis

### Phase 3: Structural Cleanup
1. Flatten unnecessary nesting
2. Consolidate code examples into organized directories
3. Move misplaced files to correct locations

---

## 📋 Sources Needing Cleanup

| Source | Duplicates | Text Files | Structure | Priority |
|--------|------------|------------|-----------|----------|
| spin2-v51 | 4-5 docs | 2 files | OK | HIGH |
| silicon-doc | 3 audits | 5+ texts | Scattered | HIGH |
| smart-pins | 1 audit | 3 texts | Nested | MEDIUM |
| pasm2-manual | 3 docs | Unknown | OK | MEDIUM |
| p2-eval-board | 2 audits | None | OK | LOW |

---

## 🎯 Expected Outcome

After cleanup:
- **One audit document per source** (complete-extraction-audit)
- **One narrative text per source** (if applicable)
- **One cross-source analysis per source** (new)
- **Clear, consistent naming** across all sources
- **No deprecated or duplicate files**

---

*This document will be updated as more cleanup needs are discovered*