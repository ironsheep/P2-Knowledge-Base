# P2 I/O & Smart Pins User Guide

## Project Overview

Creating a comprehensive user guide for the Propeller 2 pin I/O system, from fundamental Direct I/O through the 32 Smart Pin modes. This document serves as the complete reference for all P2 pin operations.

## Document Philosophy

**"Complete I/O Coverage with Practical Focus"**

- Pedagogical progression: Direct I/O → Enhanced I/O → Smart Pins
- Task-oriented: "I need to do X" → here are your options
- Rich configuration coverage: all P_ constants, all register options
- Bilingual examples throughout (Spin2 + PASM2)

## Scope

### Part I: P2 Pin System Fundamentals
- **Direct I/O** - DIR/OUT/IN registers, pin instructions
- **Enhanced Direct I/O** - P_ constants without Smart Pin modes (drive strength, Schmitt, basic DAC/ADC)
- **Smart Pin Architecture** - What Smart Pins add, when to use them
- **Configuration Model** - The layered system, how constants combine

### Part II: Output Modes (simple → complex)
- Digital output, pulse/transition, NCO, PWM, DAC, serial TX

### Part III: Input Modes (simple → complex)
- Digital input, timing measurement, counting, quadrature, period/frequency, ADC, serial RX

### Part IV: Special Modes
- Repository (inter-COG data), USB

### Part V: Appendices
- Intent Index ("I want to...")
- P_ Constants Reference
- Formulas Reference
- Mode Comparison Charts
- Troubleshooting

## Key Features

- Complete Direct I/O coverage (foundation)
- All 32 Smart Pin modes documented
- All P_ constants explained with usage context
- Intent-based navigation ("I need a SPI bus" → here's how)
- Configuration "considerations" for each mode
- Decision guidance when multiple modes apply
- Bilingual examples (Spin2 + PASM2)

## Current Status

- [x] Project kickoff
- [x] Folder structure created
- [x] Voice guide established
- [x] Creation guide established
- [ ] Content guide with full TOC
- [ ] Direct I/O chapters
- [ ] Smart Pin mode chapters
- [ ] Appendices
- [ ] Technical review

## Files in This Directory

| File | Purpose |
|------|---------|
| `README.md` | This file - project overview |
| `creation-guide.md` | How to create and verify content |
| `voice-guide.md` | Writing voice and tone conventions |
| `content-guide.md` | Complete content outline (TODO) |
| `audit/` | Verification and audit tracking |

## Source Materials

- P2 Silicon Documentation (Rev B)
- Smart Pins documentation (all revisions)
- Spin2 v51 Language Manual (P_ constants)
- John Titus Smart Pins extracts
- YAML knowledge base entries
- Validated code examples from OBEX

## Source Locations

| Source | Path |
|--------|------|
| Smart Pins catalog | `/engineering/ingestion/smart-pins-catalog/ingestionSources/` |
| Spin2 v51 sources | `/engineering/ingestion/sources/spin2-v51/` |
| P_ constants | `/engineering/ingestion/sources/spin2-v51/smartpin-symbols.txt` |

## Related Documents

- **Tutorial (Green Book):** `../p2-smart-pins-tutorial/` - Learning-focused companion
- **PASM2 Manual:** `../p2-assembly-language-manual/` - Instruction reference
- **Template Reference:** `../../templates/` - Shared template resources
- **PDF Forge Rules:** `/engineering/pdf-forge/PDF-CLAUDE-RULES.md`

## Document Differentiation

| Document | Purpose | Audience |
|----------|---------|----------|
| **This guide** | Complete I/O reference, practical usage | Developers implementing I/O |
| **Green Book** | Tutorial, learning journey | Those learning Smart Pins |
| **PASM2 Manual** | Instruction reference | Those needing instruction details |
| **Silicon Doc** | Hardware truth | Those needing electrical specs |

---

*Created: 2026-01-24*
*Renamed: 2026-01-24 (from p2-smart-pins-user-guide)*
*Status: Project initialization, structure defined*
