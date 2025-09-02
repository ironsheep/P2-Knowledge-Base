# Narrative Text File Status Report

**Created**: 2025-09-02  
**Purpose**: Track which sources have narrative text files and where they are

---

## ✅ FOUND - Narrative Text Files Exist (7 sources)

### In Correct Location:
1. **smart-pins**
   - `smartpins-narrative-from-docx.txt` ← FROM DOCX (richer)
   - `smartpins-text-fresh.txt` ← Needs comparison
   
2. **spin2-v51**
   - `spin2-v51-narrative.txt` ← Primary
   - `spin2-text.txt` ← Duplicate?

3. **silicon-doc**
   - `p2-documentation.txt` ← Should be primary
   - `silicon-doc-complete-sample.txt` ← Sample only
   - `assets/part3-text.txt` ← Needs consolidation
   - `assets/part4-text.txt` ← Needs consolidation
   - `assets/part5-text.txt` ← Needs consolidation

4. **propplug-rev-e**
   - `32201-PropPlugRev-Guide-RevE.txt` ← Has narrative!

5. **universal-motor-driver**
   - `64010-UniversalMotorDriverP2AddOnGuide-RevB-v2.0.txt` ← Has narrative!

### Found in external-inputs (need moving):
6. **pasm2-manual**
   - `/external-inputs/p2/pasm2-manual-extracted.txt` ← NEEDS MOVING!
   
7. **p2-datasheet** (maybe?)
   - `/external-inputs/archive/datasheet-extracted.txt` ← NEEDS VERIFICATION & MOVING

8. **p2-spec-sheet** (maybe?)
   - `/external-inputs/archive/spec-sheet-extracted.txt` ← NEEDS VERIFICATION & MOVING

---

## ❌ MISSING - No Narrative Text Found (16 sources)

### Edge Modules (5):
- edge-32mb-module
- edge-breakout-board  
- edge-mini-breakout
- edge-module-breadboard
- edge-standard-module

### Eval Boards (2):
- p2-eval-board
- p2-eval-add-on-boards

### Communication (2):
- p2-wx-adapter
- parallax-wx-wifi

### Data Sources (2):
- p2-instructions-csv
- p2-qa-spreadsheet

### Missing Sources (5):
- desilva-p1-tutorial
- marketing-materials
- p2docs-github-io
- rom-booter
- pasm2-manual-development

---

## 🎯 IMMEDIATE ACTIONS NEEDED

### Phase 1: Move Misplaced Narratives
1. **MOVE** `pasm2-manual-extracted.txt` → `sources/pasm2-manual/pasm2-manual-narrative.txt`
2. **MOVE** `datasheet-extracted.txt` → `sources/p2-datasheet/p2-datasheet-narrative.txt`
3. **MOVE** `spec-sheet-extracted.txt` → `sources/p2-spec-sheet/p2-spec-sheet-narrative.txt`

### Phase 2: Consolidate Multiple Files
1. **silicon-doc**: Merge part3, part4, part5 into main `p2-documentation.txt`
2. **smart-pins**: Compare DOCX vs fresh, keep richest
3. **spin2-v51**: Compare two versions, consolidate

### Phase 3: Generate Missing Narratives
For 16 sources without narratives:
1. Check if PDF exists in source directory
2. Use `pdftotext` to extract
3. If no PDF, check for other source formats
4. Create `[source-name]-narrative.txt`

---

## 📊 Summary Statistics

| Status | Count | Percentage |
|--------|-------|------------|
| **Have Narrative** | 7 | 29% |
| **Found Misplaced** | 3 | 13% |
| **Missing Entirely** | 14 | 58% |
| **TOTAL** | 24 | 100% |

**Critical Finding**: 58% of sources have NO narrative text extraction!

---

## 🔄 Git Moves Needed

```bash
# Move pasm2-manual narrative
git mv engineering/ingestion/external-inputs/p2/pasm2-manual-extracted.txt \
       engineering/ingestion/sources/pasm2-manual/pasm2-manual-narrative.txt

# Move datasheet narrative
git mv engineering/ingestion/external-inputs/archive/datasheet-extracted.txt \
       engineering/ingestion/sources/p2-datasheet/p2-datasheet-narrative.txt

# Move spec-sheet narrative
git mv engineering/ingestion/external-inputs/archive/spec-sheet-extracted.txt \
       engineering/ingestion/sources/p2-spec-sheet/p2-spec-sheet-narrative.txt
```

---

*This explains why our ingestion seemed incomplete - majority lack narrative text!*