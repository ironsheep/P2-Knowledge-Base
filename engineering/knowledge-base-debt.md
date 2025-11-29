# P2 Knowledge Base Technical Debt

*Technical debt tracking for the P2 Knowledge Base YAML content and JSON reference generation*

## Overview

This document tracks technical debt related to the P2 Knowledge Base content (YAML files) and the tools that process them, distinct from ingestion pipeline debt which is tracked separately in `/engineering/ingestion/debt.md`.

---

## JSON Reference Generation

### SPIN2 Reference Document Misclassification

**Status**: Open
**Priority**: LOW
**Discovered**: 2025-11-29

**Issue**: Reference/documentation YAML files that don't contain actual language elements are being included in the `p2-reference.json` output as "unknown" elements.

**Affected Categories**:
- `operators`: 1 "unknown" entry (from `precedence.yaml` - operator precedence reference table)
- `debug_commands`: 1 "unknown" entry (from `debug-formatters-hexadecimal.yaml` - formatter reference doc)

**Root Cause**: The `update-p2-reference-complete.py` script collects all YAML files in category directories. Files without the expected identifier field (`operator`, `command`, etc.) are assigned `name = "unknown"` as a fallback.

**Impact**: Cosmetic issue only. Core reference data (359 PASM2 instructions, 256 SPIN2 elements) is correct. The "unknown" entries contain valid reference information but are miscategorized.

**Recommended Fix**: Update `update-p2-reference-complete.py` to:
1. Skip YAML files that don't have the expected identifier field for their category
2. OR create a separate "reference_docs" category for these files
3. OR add the expected field to these reference documents

**Files to Modify**:
- `engineering/tools/update-p2-reference-complete.py`

**Workaround**: None needed - the extra entries don't break functionality.

---

## YAML Content Quality

### Cross-Hierarchy References

**Status**: Open
**Priority**: LOW
**Discovered**: 2025-11-29 (via `verify-manifest-linkages.py`)

**Issue**: One cross-hierarchy reference exists where a language file references an architecture file:
- `engineering/knowledge-base/P2/language/pasm2/conventions/pasm2-getting-started.yaml` references `engineering/knowledge-base/P2/architecture/smart_pins.yaml`

**Impact**: Minor - creates coupling between hierarchies. Not a functional issue but a refactoring opportunity.

**Recommended Fix**: Consider creating hierarchy-specific versions of shared content, or document the intentional cross-reference.

---

## Future Debt Items

*Add new items here as discovered*

---

## Resolved Items

*Move items here when fixed, with resolution date and commit reference*

---

## Notes

- This debt document focuses on knowledge base content and tooling
- Ingestion/extraction debt is tracked in `/engineering/ingestion/debt.md`
- Document production debt is tracked in `/engineering/document-production/debt.md`
- Operations debt is tracked in `/engineering/operations/technical-debt/debt.md`

---

*Last Updated: 2025-11-29*
