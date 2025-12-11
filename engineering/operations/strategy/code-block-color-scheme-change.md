# Code Block Color Scheme Change - IDE Alignment

**Created**: 2025-12-11
**Status**: Planned (Todo #466)
**Priority**: Low
**Estimate**: 30 minutes

---

## Background

Community feedback question: **"Why wouldn't PASM be green and Spin be blue? That would more closely match Propeller Tool and Spin Tools."**

This is a reasonable request - matching established IDE conventions reduces cognitive load for readers already familiar with the tools.

---

## Current Color Scheme

| Language | Background | Border | Visual |
|----------|-----------|--------|--------|
| **Spin2** | `#F8FCF8` (soft green) | `#85B985` (muted green) | Green tint |
| **PASM2** | `#FFFEF5` (soft cream) | `#D4B896` (muted tan) | Yellow/cream tint |

## Proposed Color Scheme (IDE-aligned)

| Language | Background | Border | Visual |
|----------|-----------|--------|--------|
| **Spin2** | `#E3F2FD` (light blue) | `#1976D2` (blue) | Blue tint |
| **PASM2** | `#E8F5E9` (light green) | `#4CAF50` (green) | Green tint |

---

## Affected Documents

| Document | Template File | Lua Filter(s) |
|----------|--------------|---------------|
| **Smart Pins Tutorial** | `p2kb-sp-styles.sty` | `p2kb-sp-code-coloring.lua` |
| **DeSilva PASM Manual** | `p2kb-desilva-content.sty` | `p2kb-desilva-code-coloring.lua`, `p2kb-desilva-div-blocks.lua` |
| **Debug Window Manual** | `p2kb-debugwin-content.sty` | `p2kb-debugwin-div-blocks.lua` |

---

## Change Scope

### What Changes (Small)

**Per document (3 documents):**
- **4 lines** in `.sty` template - swap the hex color values

```latex
% BEFORE (current):
\definecolor{XXX-spin2-bg}{HTML}{F8FCF8}      % green
\definecolor{XXX-spin2-border}{HTML}{85B985}  % green border
\definecolor{XXX-pasm2-bg}{HTML}{FFFEF5}      % cream
\definecolor{XXX-pasm2-border}{HTML}{D4B896}  % tan border

% AFTER (IDE-aligned):
\definecolor{XXX-spin2-bg}{HTML}{E3F2FD}      % light blue
\definecolor{XXX-spin2-border}{HTML}{1976D2}  % blue border
\definecolor{XXX-pasm2-bg}{HTML}{E8F5E9}      % light green
\definecolor{XXX-pasm2-border}{HTML}{4CAF50}  % green border
```

### What Stays the Same

- Lua filters (reference environment names, not colors)
- Markdown source files (use `::: spin2` and `::: pasm2`)
- Environment names (Spin2Block, PASM2Block unchanged)
- All other template infrastructure

---

## Implementation Summary

| Item | Count |
|------|-------|
| Files to edit | **3** `.sty` files |
| Lines to change | **~12** total (4 per file) |
| Documentation to update | **~6** markdown files (comments only) |

---

## Files to Modify

1. `engineering/document-production/workspace/p2-smart-pins-tutorial/templates/p2kb-sp-styles.sty`
   - Lines 87-90: `smartpins-spin2-*` and `smartpins-pasm2-*` colors

2. `engineering/document-production/workspace/p2-pasm-desilva-style/templates/p2kb-desilva-content.sty`
   - Lines 39-42: `desilva-spin2-*` and `desilva-pasm2-*` colors

3. `engineering/document-production/workspace/p2-debug-window-manual/templates/p2kb-debugwin-content.sty`
   - Lines 31-34: `debugwin-spin2-*` and `debugwin-pasm2-*` colors

---

## Verification After Change

1. Regenerate PDFs for all three documents
2. Visual inspection of code blocks
3. Confirm Spin2 = blue, PASM2 = green matches IDE expectations

---

## Decision Notes

- May want to confirm exact IDE colors with community before implementing
- Consider whether cream/yellow for PASM had any intentional meaning (deSilva style?)
- All three documents should use consistent colors

---

*This document prepared for future implementation. See Todo #466.*
