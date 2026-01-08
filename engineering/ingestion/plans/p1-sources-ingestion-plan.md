# P1 Sources Ingestion Plan

**Created**: 2025-01-06  
**Status**: PLANNED - Ready for Ingestion  
**Source Location**: `engineering/ingestion/external-inputs/P1/`  
**Purpose**: Expand P1 (Propeller 1) knowledge base to enable P1→P2 migration guides and comprehensive P1 documentation coverage

---

## Overview

This plan covers ingestion of newly acquired P1 source materials placed in `external-inputs/P1/`. These documents supplement the existing P1 sources (P1 Propeller Manual v1.2 and P1 Datasheet v1.4.0) to provide comprehensive P1 coverage.

**Naming Convention**: All P1 source folders use the `p1-*` prefix for sorting and organization.

---

## Source Inventory

### Already Ingested P1 Sources

| Source Folder | Document | Status |
|---------------|----------|--------|
| `p1-propeller-manual-v1.2` | P1 Propeller Manual v1.2 | ✅ COMPLETE |
| `p1-datasheet-v1.4` | P1 Datasheet v1.4.0 | ✅ COMPLETE |

---

### New P1 Sources - Root Level Documents

| Source File | Planned Folder | Priority | Est. Pages | Authority |
|-------------|----------------|----------|------------|-----------|
| `122-32000-Propeller-Manual-v1.1-Supp-Errata.pdf` | `p1-propeller-manual-errata-v1.1` | HIGH | ~10-20 | 🏆 AUTHORITATIVE |
| `122-32305-PE-Labs-Fundamentals-Text-v1.2.pdf` | `p1-pe-labs-fundamentals-v1.2` | MEDIUM | ~100+ | 🏆 AUTHORITATIVE |
| `122-32450-XBeeTutorial-v1.0.1.pdf` | `p1-xbee-tutorial-v1.0.1` | MEDIUM | ~50+ | 🏆 AUTHORITATIVE |
| `122-32450-XBeeTutorialErrata-v1.0.pdf` | `p1-xbee-tutorial-errata-v1.0` | LOW | ~5-10 | 🏆 AUTHORITATIVE |
| `P1 P8X32A-Web-PropellerManual-v1.2.pdf` | *(duplicate of already ingested)* | - | - | - |
| `P8X32A-Propeller-Datasheet-v1.4.0_0.pdf` | *(duplicate of already ingested)* | - | - | - |

**Note**: The Propeller Manual and Datasheet appear to be duplicates of already-ingested sources. Verify these are identical before skipping.

---

### New P1 Sources - Application Notes (`AppNotes/`)

All application notes are official Parallax documents and carry **🏆 AUTHORITATIVE** trust level.

| Source File | Planned Folder | Topic | Priority |
|-------------|----------------|-------|----------|
| `AN001-P8X32ACounters-v2.0.pdf` | `p1-appnote-001-counters-v2.0` | P1 Counter Modules | HIGH |
| `AN002-GPS-NMEA0183-v1.0.pdf` | `p1-appnote-002-gps-nmea-v1.0` | GPS/NMEA Protocol | MEDIUM |
| `AN003-AbstractDataStructures-v1.0.pdf` | `p1-appnote-003-data-structures-v1.0` | Data Structures in Spin | HIGH |
| `AN004-GUI-StartVGA-v1.0.pdf` | `p1-appnote-004-vga-gui-start-v1.0` | VGA GUI Basics | MEDIUM |
| `AN005-SimpleVGAMenus-v1.0.pdf` | `p1-appnote-005-vga-menus-v1.0` | VGA Menu Systems | MEDIUM |
| `AN006-SD-FFS-Drivers-v1.0.pdf` | `p1-appnote-006-sd-filesystem-v1.0` | SD Card Filesystem | HIGH |
| `AN007-SoftLoadXBee-v1.0.pdf` | `p1-appnote-007-xbee-softload-v1.0` | XBee Soft Loading | MEDIUM |
| `AN008-SigmaDeltaADC-v1.0.pdf` | `p1-appnote-008-sigma-delta-adc-v1.0` | Sigma-Delta ADC | HIGH |
| `AN009-ExecutionTime-v1.0.pdf` | `p1-appnote-009-execution-time-v1.0` | Execution Timing | HIGH |
| `AN010-MixedVoltageInterface-v1.0.pdf` | `p1-appnote-010-mixed-voltage-v1.0` | Voltage Level Interfacing | MEDIUM |
| `AN011-SimpleTemplate-v1.0.pdf` | `p1-appnote-011-simple-template-v1.0` | Project Template | LOW |
| `AN012-SRAM-v1.0.pdf` | `p1-appnote-012-sram-v1.0` | External SRAM | MEDIUM |
| `AN013-WMF-Menus-v1.0.pdf` | `p1-appnote-013-wmf-menus-v1.0` | WMF Menu System | LOW |
| `AN014-Coroutines-v1.0.pdf` | `p1-appnote-014-coroutines-v1.0` | Coroutine Patterns | HIGH |
| `AN015-SchmittTrigger-v1.0.pdf` | `p1-appnote-015-schmitt-trigger-v1.0` | Schmitt Trigger | MEDIUM |
| `AN018-CommPC-v1.0.pdf` | `p1-appnote-018-pc-comm-v1.0` | PC Communication | HIGH |
| `AN019-StackSpace-v1.0.pdf` | `p1-appnote-019-stack-space-v1.0` | Stack Management | HIGH |

**Note**: AN016 and AN017 do not exist - these were never published by Parallax.

---

## Document Categories & Cross-Reference Value

### Core Language/Architecture
- **Propeller Manual Errata** - Corrections to official manual
- **AN001 Counters** - Counter module deep dive (P1→P2: counters → smart pins)
- **AN003 Data Structures** - Programming patterns applicable to P2
- **AN014 Coroutines** - Multi-cog coordination patterns
- **AN019 Stack Space** - Critical for multi-cog programming

### Hardware Interfacing
- **AN006 SD Filesystem** - Storage patterns (highly relevant to P2)
- **AN008 Sigma-Delta ADC** - Analog conversion techniques
- **AN010 Mixed Voltage** - Level shifting (applicable to P2)
- **AN012 SRAM** - External memory interfacing
- **AN015 Schmitt Trigger** - Input conditioning

### Communication
- **AN002 GPS NMEA** - Serial protocol parsing
- **AN007 XBee Softload** - Wireless programming
- **AN018 PC Communication** - Host interfacing
- **XBee Tutorial + Errata** - Wireless module integration

### Display/UI
- **AN004 VGA GUI Start** - VGA fundamentals
- **AN005 VGA Menus** - Menu system design
- **AN013 WMF Menus** - Alternative menu approach

### Educational
- **PE Labs Fundamentals** - Structured learning curriculum
- **AN011 Simple Template** - Project scaffolding
- **AN009 Execution Time** - Performance measurement

---

## Ingestion Priority Order

### Phase 1 - HIGH Priority (Core Technical)
1. `p1-propeller-manual-errata-v1.1` - Manual corrections
2. `p1-appnote-001-counters-v2.0` - Counter architecture
3. `p1-appnote-006-sd-filesystem-v1.0` - Storage patterns
4. `p1-appnote-008-sigma-delta-adc-v1.0` - ADC techniques
5. `p1-appnote-014-coroutines-v1.0` - Cog coordination
6. `p1-appnote-018-pc-comm-v1.0` - PC interfacing
7. `p1-appnote-019-stack-space-v1.0` - Stack management
8. `p1-appnote-003-data-structures-v1.0` - Programming patterns
9. `p1-appnote-009-execution-time-v1.0` - Timing analysis

### Phase 2 - MEDIUM Priority (Practical Applications)
10. `p1-pe-labs-fundamentals-v1.2` - Educational content
11. `p1-xbee-tutorial-v1.0.1` - XBee integration
12. `p1-appnote-002-gps-nmea-v1.0` - GPS protocols
13. `p1-appnote-004-vga-gui-start-v1.0` - VGA basics
14. `p1-appnote-005-vga-menus-v1.0` - Menu systems
15. `p1-appnote-007-xbee-softload-v1.0` - Wireless programming
16. `p1-appnote-010-mixed-voltage-v1.0` - Level shifting
17. `p1-appnote-012-sram-v1.0` - External memory
18. `p1-appnote-015-schmitt-trigger-v1.0` - Input conditioning

### Phase 3 - LOW Priority (Supplementary)
19. `p1-xbee-tutorial-errata-v1.0` - Tutorial corrections
20. `p1-appnote-011-simple-template-v1.0` - Template project
21. `p1-appnote-013-wmf-menus-v1.0` - Alternative menus

---

## P1→P2 Migration Relevance

| P1 Topic | P2 Equivalent | Migration Notes |
|----------|---------------|-----------------|
| P1 Counters (AN001) | Smart Pins | Counters evolved into smart pin modes |
| SD Filesystem (AN006) | flash_fs.spin2 | Similar concepts, new implementation |
| Sigma-Delta ADC (AN008) | Smart Pin ADC modes | Hardware ADC now available |
| Coroutines (AN014) | Spin2 multi-cog | Same principles, cleaner syntax |
| Stack Space (AN019) | Spin2 stack handling | Still relevant, better tools |
| VGA (AN004, AN005) | P2 video modes | Higher resolution, more modes |
| SRAM (AN012) | HyperRAM/HyperFlash | Modern external memory |

---

## Ingestion Workflow

For each document:
1. **Create source folder** in `sources/` with `p1-*` prefix
2. **Extract text** using PDF extraction tools
3. **Create audit document** (`*-complete-extraction-audit.md`)
4. **Extract code examples** if present
5. **Extract images/diagrams** if valuable
6. **Update INGESTION-AUDIT-MATRIX.md**
7. **Add to P1 Sources section** in README.md

---

## Statistics

| Category | Count |
|----------|-------|
| **New Root Documents** | 4 (excluding duplicates) |
| **New App Notes** | 17 |
| **Total New P1 Sources** | 21 |
| **Estimated Pages** | 300-500 |
| **Already Ingested** | 2 (Manual + Datasheet) |
| **Total P1 Sources After Completion** | 23 |

---

## Next Steps

1. [ ] Verify duplicate PDFs match already-ingested versions
2. [ ] Begin Phase 1 HIGH priority ingestions
3. [ ] Update INGESTION-AUDIT-MATRIX.md with P1 section
4. [ ] Create central-analysis P1 hub folder if not exists
5. [ ] Consider P1→P2 comparison documents as part of analysis

---

*This plan integrates P1 source material into the knowledge base ingestion pipeline. Priority reflects cross-reference value for P1→P2 migration guides.*
