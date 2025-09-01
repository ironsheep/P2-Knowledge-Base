# Document Production Pipeline

*Last Updated: 2025-08-25 | September 9th Presentation Target*

## Production States

| State | Symbol | Description |
|-------|--------|-------------|
| Planned | 🔴 | Identified need, not started |
| Content Ready | 🟡 | Source material available |
| In Production | 🟢 | Actively being generated |
| Released | ✅ | Published and available |
| Deferred | ⏸️ | Valid but not current priority |

## Priority Queue (September 9th)

| Document | Status | Size | Template Stack | Priority |
|----------|--------|------|----------------|----------|
| **Smart Pins Reference** | 🟢 Production | 400+ pages | foundation + smart-pins + tech-review | 🔥 Methodology validation |
| **PASM2 DeSilva Manual** | 🟡 Queued | 4 parts | foundation + pasm-desilva + tech-review | 🔥 Cross-doc validation |

## Active Queue

| Document | Status | Source | Template Stack |
|----------|--------|--------|----------------|
| **Terminal Window Guide** | 🟡 Ready | Spin2 extractions | foundation + user-guide + draft |
| **Debugger Guide** | 🟡 Ready | Debugger extractions | foundation + user-guide + draft |
| **PASM2 Reference** | 🔴 Planned | Parallax foundation | foundation + reference + official |
| **Spin2 Reference** | 🔴 Planned | Parallax foundation | foundation + reference + official |

## Deferred Queue

| Document | Status | Reason |
|----------|--------|--------|
| **AI Privacy Guide** | ⏸️ Deferred | Not P2-related |
| **Release Notes v1.0** | ⏸️ Deferred | Post-presentation |

## Document Details

### Smart Pins Complete Reference
- **Working**: `workspace/smart-pins-manual/P2-Smart-Pins-Complete-Reference-WORKING.md`
- **Examples**: 156 total (98 extracted + 58 created)
- **Coverage**: All 32 modes with bilingual examples
- **Current**: Visual refinement iteration

### PASM2 DeSilva Manual
- **Working**: `workspace/desilva-manual/P2-PASM-deSilva-Style-Part*.md`
- **Parts**: 4 markdown files
- **Approach**: Pedagogical tutorial style
- **Next**: Apply Smart Pins methodology

## Template Architecture

### Layer Stack
```
Foundation → Content Type → Presentation Style
p2kb-foundation → [reference/tutorial/user-guide] → [draft/tech-review/official]
```

### Document-Template Matrix

| Type | Content Layer | Presentation Flow |
|------|--------------|-------------------|
| Reference Manual | reference-manual | tech-review → official |
| Tutorial | tutorial-manual | tech-review |
| User Guide | user-guide | draft → tech-review |

## Visual Assets

| Source | Available | Status |
|--------|-----------|--------|
| P2 Edge Ecosystem | 60 images | ✅ Complete |
| Smart Pins | 21 images | ✅ Complete |
| Spin2 v51 | 24 images | ✅ Complete |
| Silicon Doc | 34 images | ✅ Complete |
| **Total Available** | **139 images** | Ready for use |

## Production Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Template Reliability | 100% | ✅ Achieved |
| Production Speed | <1 day | ✅ Achieved |
| Branding Switch | <30 sec | ✅ Achieved |
| Template Debug Cycles | 0 | ✅ Achieved |

## Production Triggers

Document enters production when:
- [x] Content fully validated
- [x] Template stack tested
- [x] Audience need confirmed
- [x] Sprint scheduled
- [x] Visual assets assessed

## Quick Links

- [Working Documents](workspace/)
- [Template Masters](../pdf-templates-master/)
- [Visual Assets Matrix](../ingestion/visual-assets/INGESTION-IMAGE-EXTRACTION-MATRIX.md)
- [Technical Debt](../technical-debt/VISUAL-ASSETS-DEBT.md)

---

[→ Methodology & Details](ABOUT.md) | [→ Operations Dashboard](../README.md)