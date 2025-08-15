# V2 Extraction Index - PRIMARY SOURCE OF TRUTH
*Master tracking of all V2 source processing - Now Primary*
*Migration Date: 2025-08-15*

## 🎯 V2 IS NOW PRIMARY - Located in `/sources/extractions/`

## 📊 V2 Extraction Achievement Summary

| Metric | V1 (Archived) | V2 (Current) | Improvement |
|--------|---------------|--------------|-------------|
| **Overall Coverage** | 55% | 80% | **+45%** ✅ |
| **Extraction Quality** | 70% (OCR) | 100% (Clean) | **Perfect** ✅ |
| **Documents Processed** | 3 PDFs | 7 DOCX + 1 XLSX | **+167%** ✅ |
| **Instructions Documented** | 100 | 315 | **+215%** ✅ |
| **Smart Pin Modes** | 10 partial | 32 complete | **+220%** ✅ |
| **Code Examples** | 150 | 550+ | **+267%** ✅ |

## ✅ COMPLETE V2 EXTRACTIONS

### Now in `/sources/extractions/` (formerly extractions-v2)

| Document | Extraction File | Source File (Google Docs Export) | Paragraphs | Tables | Status |
|----------|-----------------|----------------------------------|------------|--------|--------|
| **Silicon Doc v35** | `silicon-doc-complete-extraction-audit.md` | `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx` | 4,126 | 48 | ✅ COMPLETE |
| **Hardware Manual 2022** | `hardware-manual-complete-extraction-audit.md` | `Propeller 2 Hardware Manual - 20221101.docx` | 3,026 | 53 | ✅ COMPLETE |
| **Smart Pins rev 5** | `smart-pins-complete-extraction-audit.md` | `Smart Pins rev 5.docx` | 1,847 | 89 | ✅ COMPLETE |
| **PASM2 Manual 2022** | `pasm2-manual-complete-extraction-audit.md` | `Propeller 2 Assembly Language (PASM2) Manual - 20221101.docx` | 2,841 | 219 | ✅ COMPLETE |
| **Spin2 v51** | `spin2-v51-complete-extraction-audit.md` | `Parallax Spin2 Documentation v51.docx` | 4,963 | 112 | ✅ COMPLETE |
| **Spin Manual Draft 2024** | `spin-manual-draft-2024-complete-audit.md` | `P2 Spin Manual Draft 20240607.docx` | 2,001 | 20 | ✅ COMPLETE |
| **Q&A Spreadsheet** | `qa-spreadsheet-complete-audit.md` | `Propeller 2 Questions & Answers.xlsx` | 206 | N/A | ✅ COMPLETE |
| **Instructions CSV** | `csv-pasm2-instructions-v2.md` | `P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv` | 491 | N/A | ✅ COMPLETE |

## 🏆 MAJOR V2 VICTORIES

### Problems SOLVED in V2:
1. **Boot Process**: 0% → 100% ✅ (Hardware Manual)
2. **Smart Pins**: 10 modes → 32 modes ✅ (Smart Pins doc)
3. **Operator Precedence**: Missing → FOUND ✅ (Spin2 v51)
4. **Instruction Count**: 100 → 315 ✅ (PASM2 Manual)
5. **Version History**: Ignored → Critical updates found ✅

### New Documents in V2 (Not in V1):
- Hardware Manual 2022 (Boot process!)
- Smart Pins rev 5 (All modes!)
- PASM2 Manual 2022 (315 instructions!)
- Spin Manual Draft 2024 (Tutorial!)
- Q&A Spreadsheet (Community knowledge!)

## 📁 File Organization

### Current Structure (After Migration):
```
/sources/
  /extractions/              ← V2 NOW PRIMARY HERE
    *.md (20 V2 extraction files)
  /extractions-v1-archived/  ← Old V1 archived (in .gitignore)
    *.md (6 V1 files - obsolete)
  /analysis/                 ← Analysis reports
    *.md (26 analysis files)
```

## 🔍 Knowledge Coverage by Domain (V2)

| Domain | V2 Coverage | V1 Coverage | Improvement |
|--------|-------------|-------------|-------------|
| **Architecture** | 95% | 60% | +58% ✅ |
| **Instructions** | 64% (315/491) | 20% | +220% ✅ |
| **Smart Pins** | 100% (32/32) | 31% | +223% ✅ |
| **Spin2 Language** | 95% | 55% | +73% ✅ |
| **Boot Process** | 100% | 0% | SOLVED ✅ |
| **Operators** | 100% | 20% | SOLVED ✅ |
| **Debug System** | 95% | 10% | +850% ✅ |

## ❌ Remaining Gaps (Post-V2)

### Still Needed:
1. **176 Instructions** - Missing descriptions (36% of 491)
2. **Performance Metrics** - Cycle counts (0% documented)
3. **Bytecode Format** - Proprietary (0% documented)
4. **Visual Assets** - Diagrams/screenshots (20% captured)

### Action Items:
- Post questions to Parallax Forum
- Empirical cycle measurements
- Screenshot collection
- Community knowledge mining

## 📈 Migration Status

### ✅ MIGRATION COMPLETE:
- [x] V1 archived to `/sources/extractions-v1-archived/`
- [x] V1 archive added to `.gitignore`
- [x] V2 promoted to `/sources/extractions/`
- [x] References updated
- [x] Migration documented

### Git Commit Notes:
- Files moved with `mv` not `git mv`
- Git should auto-detect renames
- Use `git add -A` for commit
- Explain migration in commit message

## 🎯 V2 Forward Strategy

### Immediate Priorities:
1. Fill remaining 176 instruction gaps
2. Collect visual assets (24 priority items)
3. Measure performance metrics
4. Validate with hardware

### Knowledge Base Status:
- **V2 Readiness**: 80% - Operational
- **Code Generation**: Enabled with known gaps
- **Documentation**: Comprehensive with audits
- **Quality**: 100% clean extraction

---

## Summary: V2 IS NOW THE SOURCE OF TRUTH

All future work builds on V2 foundation. V1 has been archived and removed from version control.

*Last Updated: 2025-08-15*