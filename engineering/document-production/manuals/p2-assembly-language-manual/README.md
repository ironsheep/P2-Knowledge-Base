# P2 Assembly Language PASM2 Manual

**Document Title:** P2 Assembly Language (PASM2) Manual
**Canonical Folder Name:** `p2-assembly-language-manual`

## Purpose

This folder contains the work-in-progress replacement for the Parallax P2 Assembly Language Manual. The goal is to generate a complete, high-quality reference manual documenting all 491 PASM2 instructions with:

- Accurate syntax and encoding information
- Clear explanations of each instruction's behavior
- Practical code examples (validated with pnut_ts compiler)
- Use cases and related instruction cross-references

## Source Material

This manual is based on and replaces the partial draft from Parallax:

**Original Source Location:**
`/engineering/ingestion/sources/pasm2-manual/`

**Original Document:**
`P2-Assembly-Language-PASM2-Manual-Draft-221117.pdf`

The ingested source contains:
- 315 instructions with descriptions
- 176 instructions needing descriptions
- Extracted instruction tables and encodings
- Updated YAML files for knowledge base integration

## Directory Structure

```
p2-assembly-language-manual/
├── README.md                      # This file
├── PASM2-MANUAL-WORKFLOW.md       # Detailed workflow documentation
├── WORKFLOW-SUMMARY.md            # Quick reference workflow
├── extract-weak-instructions.py   # Tool: identify instructions needing work
├── extract-from-tables.py         # Tool: extract from ingested tables
├── extracted-from-manual/         # Raw extractions (YAML/TXT pairs)
│   ├── ADDCT1.yaml
│   ├── ADDCT1.txt
│   └── ... (339 files)
└── instruction-templates/         # Template examples for documentation
    ├── MODCZ-example.md
    ├── SETBYTE-example.md
    ├── ADDSX-template.md
    ├── ALIGNL-template.md
    └── ALTI-template.md
```

## Workflow Overview

1. **Template Generation** - Auto-generate templates from extracted data
2. **Manual Enhancement** - Fill gaps, add examples, verify accuracy
3. **Validation** - Test all code examples with pnut_ts compiler
4. **Assembly** - Combine into complete alphabetical reference
5. **PDF Generation** - Deploy to PDF Forge for final output

See `PASM2-MANUAL-WORKFLOW.md` for detailed process documentation.

## PDF Production & Release Process

For PDF generation workflow and version release procedures, see the **workspace README**:

`../../workspace/p2-assembly-language-manual/README.md`

Key sections:
- **PDF Forge Workflow** - Escape, stage, deploy cycle
- **Release Process** - Changelog updates, deliverables promotion, version tagging

## Relationship to Other Manuals

| Manual | Purpose | Style |
|--------|---------|-------|
| **This manual** (`p2-assembly-language-manual`) | Instruction reference (491 instructions) | Technical/Formal |
| `p2-pasm-desilva-style` | Tutorial - "Discovering P2 Assembly" | Friendly/Pedagogical |

These are complementary documents:
- **This manual** = "What does instruction X do?" (reference)
- **DeSilva manual** = "How do I learn P2 assembly?" (tutorial)

## Status

- [ ] All 491 instructions have templates
- [ ] 100% encoding accuracy vs CSV
- [ ] All examples compile with pnut_ts
- [ ] Cross-references validated
- [ ] PDF generation successful

---

*Last Updated: 2026-01-23*
