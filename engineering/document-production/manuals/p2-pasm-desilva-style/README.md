# P2 PASM De Silva Style Manual Specifications

This directory contains the complete specification for the De Silva PASM2 Manual.

## Directory Structure

### Specification Documents (This Directory)
- **`creation-guide.md`** - How to create/regenerate the manual content
- **`desilva-style-guide.md`** - Visual and formatting specifications
- **`opus-master-gap-analysis.md`** - Analysis of what needs enhancement
- **`READ-ONLY-PROTECTION.md`** - Protection notice for opus-master
- **`README.md`** - This file

### Opus Master (Protected Subdirectory)
- **`opus-master/`** - Original Opus 4.1 generation (READ-ONLY REFERENCE)
  - `COMPLETE-OPUS-MASTER.md` - Full original manual
  - `README-SACRED.md` - Original protection notice

## Purpose of Each Document

### creation-guide.md
- Pedagogical approach (De Silva voice + enhancements)
- Chapter structure templates
- Content sources (YAML, patterns, etc.)
- Production method phases
- Modular manual strategy
- Quality checklists

### desilva-style-guide.md
- Instruction formatting rules (UPPERCASE + BOLD)
- Box types and colors
- Code block formatting
- Typography rules
- Visual hierarchy
- Quick reference checklist

### opus-master-gap-analysis.md
- Current state assessment (strong chapters 1-6)
- Gap identification (weak chapters 7-16)
- Modular manual strategy
- Pedagogical approach documentation
- Content sources and production method
- Recommendations for enhancement

### opus-master/
- Chapters 1-6: Strong foundation to preserve
- Original De Silva voice examples
- Chapter flow and structure
- Reference for regeneration

## Workflow

1. **Planning**: Review creation-guide.md for approach
2. **Reference**: Check opus-master for foundation
3. **Writing**: Follow creation-guide.md templates
4. **Formatting**: Apply desilva-style-guide.md rules
5. **Production**: Use workspace for active files
6. **Deployment**: Stage in outbound directory

## Important Notes

- **DO NOT EDIT** opus-master files - they are reference only
- **Workspace** is for active editing of manual parts
- **These specs** define the manual but aren't part of it
- **Version together** - creation and style guides evolve as a pair

## Related Locations

- **Working files**: `/engineering/document-production/workspace/p2-pasm-desilva-style/`
- **Deployment**: `/engineering/document-production/outbound/p2-pasm-desilva-style/`
- **Templates**: `/engineering/document-production/shared-assets/templates/`

---

Last Updated: 2025-01-09