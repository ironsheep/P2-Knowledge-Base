# Ingested Sources Catalog - Complete Knowledge Base Inventory
*Master record of all ingested documents, extractions, and post-processing*
*Generated: 2025-08-29 (Major Update: Silicon Doc v35 PDF Integration)*

## 📊 Summary Statistics
- **Primary Sources**: 21 documents (7 DOCX, 1 XLSX, 1 CSV, 1 SPIN2, 11 PDF)
- **Post-Extraction Sources**: 21 derived analyses
- **Total Paragraphs Processed**: 19,216+
- **Total Tables Processed**: 531+
- **Total Code Examples**: 681+ (151 extracted + validated, 267 cataloged from Spin2, 263 in various analyses)
- **Coverage Achievement**: 90% of P2 knowledge (**MAJOR MILESTONE: Silicon Doc v35 PDF authoritative source integrated)**
- **Instruction Coverage**: 119/119 unique mnemonics (100% Silicon-verified) + 490 encoding variants tracked

## 📚 PRIMARY INGESTED SOURCES

### Parallax Official Documents (Google Docs Exports)

| Document | Source | File Size | Doc Date | Ingestion Date | Status | Image Extraction | Original Filename |
|----------|--------|-----------|----------|----------------|--------|---------------|------------------|
| **P2 Silicon Documentation v35** | Parallax (Chip Gracey) | 2.8 MB | 2020-10-15 | 2025-08-14 | ✅ COMPLETE | 🔴 **CRITICAL PENDING** (20-30 est.) | `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx` |
| **P2 Hardware Manual** | Parallax | 1.9 MB | 2022-11-01 | 2025-08-14 | ✅ COMPLETE | 🔴 **CRITICAL PENDING** (15-25 est.) | `Propeller 2 Hardware Manual - 20221101.docx` |
| **Smart Pins Documentation rev 5** | Jon Titus/Parallax | 856 KB | 2020-09-01 | 2025-08-14 | ✅ **COMPLETE + VERIFIED** + ✅ **CODE EXTRACTED** | ✅ **EXTRACTED + CATALOGED** (21/21, 100%) | `Smart Pins rev 5.docx` |
| **PASM2 Language Manual** | Parallax | 3.2 MB | 2022-11-01 | 2025-08-14 | ⚠️ PARTIAL (315/491) | 🟡 **HIGH PENDING** (30-40 est.) | `Propeller 2 Assembly Language (PASM2) Manual - 20221101.docx` |
| **Spin2 Documentation v51** | Parallax (Jeff Martin) | 4.1 MB | 2025-07-30 | 2025-08-14 | ✅ COMPLETE + ✅ **CODE EXTRACTED** | ✅ **EXTRACTED + CATALOGED** (24/24, 100%) | `Parallax Spin2 Documentation v51.docx` |
| **P2 Spin Manual Draft** | Parallax | 1.4 MB | 2024-06-07 | 2025-08-14 | ✅ COMPLETE | 🟡 **HIGH PENDING** (15-20 est.) | `P2 Spin Manual Draft 20240607.docx` |
| **P2 Q&A Spreadsheet** | Parallax Community | 124 KB | 2020-2021 | 2025-08-14 | ✅ COMPLETE | `Propeller 2 Questions & Answers.xlsx` |
| **P2 Instructions CSV** | Parallax | 98 KB | 2020-10-15 | 2025-08-14 | ✅ COMPLETE | `P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv` |

### Parallax Source Code

| Document | Source | File Size | Version | Ingestion Date | Status | Original Filename |
|----------|--------|-----------|---------|----------------|--------|------------------|
| **Flash Filesystem** | Chip Gracey | 156 KB | v2.0.0 | 2025-08-15 | ✅ COMPLETE | `flash_fs.spin2` |
| **Spin2 Interpreter v51** | Chip Gracey | ~400 KB | v51 | 2025-08-15 | ✅ ANALYZED | `Spin2_interpreter.spin2` |
| **Spin2 Debugger** | Chip Gracey | ~100 KB | v51 | 2025-08-16 | ✅ ANALYZED | `Spin2_debugger.spin2` |
| **Spin2 Flash Loader** | Chip Gracey | ~50 KB | v51 | 2025-08-16 | ✅ ANALYZED | `Spin2_flash_loader.spin2` |

### P2 Hardware Modules

| Document | Source | File Size | Doc Date | Ingestion Date | Status | Image Extraction | Original Filename |
|----------|--------|-----------|----------|----------------|--------|---------------|-----------|
| **P2 Edge 32MB Module Guide** | Parallax | 1.18 MB | 2022-05-31 | 2025-08-24 | ✅ COMPLETE | ✅ **EXTRACTED + CATALOGED** (6/6, 100%) | `P2-EC32MB-Edge-Module-Rev-B-Guide-v2.0.pdf` |
| **P2 Edge Standard Module Guide** | Parallax | 2.01 MB | 2021-08-30 | 2025-08-24 | ✅ COMPLETE | ✅ **EXTRACTED + CATALOGED** (6/6, 100%) | `P2-EC-Edge-Module-RevD-Product-Guide-3.0.pdf` |
| **P2 Edge Mini Breakout Guide** | Parallax | 1.3 MB | 2020-11-30 | 2025-08-24 | ✅ COMPLETE | ⚠️ EXTRACTED (13/16, 81%) | `64019-P2-Edge-MiniBreakoutBoardGuide-v1.1.pdf` |
| **P2 Edge Standard Breakout Guide** | Parallax | 1.4 MB | 2023-03-01 | 2025-08-24 | ✅ COMPLETE | ✅ **EXTRACTED + CATALOGED** (17/17, 100%) | `64029-P2-Edge-Breakout-Board-Guide-20230301.pdf` |
| **P2 Edge Module Breadboard Guide** | Parallax | 2.1 MB | 2021-04-15 | 2025-08-24 | ✅ COMPLETE | ✅ **EXTRACTED + CATALOGED** (18/18, 100%) | `64020-P2-Edge-Module-Breadboard-Product-Guide-REVB.pdf` |
| **P2 Eval Board Rev C Guide** | Parallax | 4.9 MB | 2020-06-29 | 2025-08-29 | ✅ COMPLETE | ✅ **EXTRACTED + CATALOGED** (15/15, 100%) | `64000 Propeller 2 Eval Board Rev C Guide.pdf` |
| **P2 Eval Add-on Boards Product Guide** | Parallax | 1.6 MB | 2020-06-29 | 2025-08-28 | ✅ COMPLETE | ❌ **PENDING** (12-16 est.) | `64006-P2-Eval-Add-on-Boards-Product-Guide.pdf` |
| **Universal Motor Driver P2 Add-on Board** | Parallax | 4.0 MB | 2022-05-05 | 2025-08-28 | ✅ COMPLETE | ❌ **PENDING** (8-12 est.) | `64010-UniversalMotorDriverP2AddOnGuide-RevB-v2.0.pdf` |
| **PropPlug Rev E Programming Interface** | Parallax | 502 KB | 2021-02-03 | 2025-08-29 | ✅ COMPLETE | 🟡 **PENDING** (2-4 est.) | `32201-PropPlugRev-Guide-RevE.pdf` |
| **P2 WX Adapter Add-on Board** | Parallax | 924 KB | 2020-11-12 | 2025-08-29 | ✅ COMPLETE | 🟡 **HIGH PENDING** (8+ est.) | `64007-P2-WX-Adapter-Guide-v1.0.pdf` |
| **Parallax WX ESP8266 WiFi Module** | Parallax | 4.9 MB | 2016-05-12 | 2025-08-29 | ✅ COMPLETE | 🟡 **HIGH PENDING** (12+ est.) | `32420-Parallax-WX-WiFi-Module-Guide-v1.0.pdf` |

### Official Silicon Documentation (PDF Authority Source)

| Document | Source | File Size | Doc Date | Ingestion Date | Status | Image Extraction | Original Filename |
|----------|--------|-----------|----------|----------------|--------|-----------------|---------|
| **P2 Silicon Documentation v35 PDF** | 🏆 **PRIMARY AUTHORITY** (Parallax/Chip Gracey) | 3.38 MB | 2020-10-15 | 2025-08-29 | ✅ **COMPLETE + AUTHORITATIVE** | ✅ **EXTRACTED** (34/34, 100%) | `P2 Documentation v35 - Rev B_C Silicon.pdf` (5-part extraction) |

**Silicon Doc Authority Status**: 🔥 **AUTHORITATIVE SOURCE** - This PDF version supersedes the DOCX version for all P2 specifications. Complete 114-page silicon documentation with 100% instruction coverage (119 unique mnemonics) and full system specifications. Serves as the definitive source for all P2 programming, system architecture, and hardware integration.

### Community Documents (Never Ingested)

| Document | Source | Status | Notes |
|----------|--------|--------|-------|
| **P1 DeSilva Assembly Tutorial** | deSilva | ❌ NOT EXTRACTED | PDF exists at `sources/originals/P1 DeSilvaAssemblyTutorial.pdf` - only style guide created |

## 🔄 POST-EXTRACTION SOURCES (Derived Analyses)

### Content Extraction Audits
*These extract and catalog content from primary sources*

| Extraction | Primary Source | Content | Status | Location |
|-----------|----------------|---------|--------|----------|
| **Silicon Doc Audit** | P2 Silicon v35 | 4,126 paragraphs, 48 tables | ✅ COMPLETE | `/sources/extractions/silicon-doc-complete-extraction-audit.md` |
| **Hardware Manual Audit** | Hardware Manual 2022 | 3,026 paragraphs, 53 tables | ✅ COMPLETE | `/sources/extractions/hardware-manual-complete-extraction-audit.md` |
| **Smart Pins Audit** | Smart Pins rev 5 | 1,847 paragraphs, 89 tables | ✅ COMPLETE | `/sources/extractions/smart-pins-complete-extraction-audit.md` |
| **PASM2 Manual Audit** | PASM2 Manual 2022 | 2,841 paragraphs, 219 tables | ✅ COMPLETE | `/sources/extractions/pasm2-manual-complete-extraction-audit.md` |
| **Spin2 v51 Audit** | Spin2 Doc v51 | 4,963 paragraphs, 112 tables | ✅ COMPLETE | `/sources/extractions/spin2-v51-complete-extraction-audit.md` |
| **Spin Manual Draft Audit** | P2 Spin Manual 2024 | 2,001 paragraphs, 20 tables | ✅ COMPLETE | `/sources/extractions/spin-manual-draft-2024-complete-audit.md` |
| **Q&A Spreadsheet Audit** | Q&A Spreadsheet | 206 Q&A pairs | ✅ COMPLETE | `/sources/extractions/qa-spreadsheet-complete-audit.md` |
| **Instructions CSV Extract** | Instructions CSV | 491 instructions | ✅ COMPLETE | `/sources/extractions/csv-pasm2-instructions-v2.md` |
| **Silicon Doc PDF Audit (v35)** | P2 Silicon Doc v35 PDF | 114 pages, 119 instruction mnemonics, complete system specs | ✅ **COMPLETE + AUTHORITATIVE** | `/sources/extractions/silicon-doc-complete-extraction-audit/` |

### Code Example Extractions (NEW 2025-08-24)
*Systematic extraction of compilable code examples from PDF documentation*

| Extraction | Primary Source | Examples Extracted | Compilation Success | Status | Location |
|-----------|----------------|--------------------|--------------------|---------|-----------|
| **Spin2 v51 Code Examples** | P2 Spin2 Documentation v51 (PDF) | 32 examples | 100% (32/32) | ✅ COMPLETE | `/sources/extractions/spin2-v51.../assets/code-20250824/` |
| **Smart Pins Code Examples** | P2 SmartPins Documentation (PDF) | 98 examples | 100% (64/64 compilable) | ✅ COMPLETE | `/sources/extractions/smart-pins.../assets/code-20250824/` |

| **Smart Pins Manual Examples** | P2 Smart Pins Complete Reference | 58 examples | 100% (31/31 Spin2) | ✅ COMPLETE | `/sources/extractions/smart-pins-manual.../assets/code-20250824/` |
**Code Example Totals**: **188 validated examples** (64 Spin2, 90 PASM2, 34 config patterns)

### Code Analysis Extractions
*These analyze source code for patterns and implementation details*

| Extraction | Primary Source | Content | Status | Location |
|-----------|----------------|---------|--------|----------|
| **Flash FS Analysis** | flash_fs.spin2 | Complete API, patterns | ✅ COMPLETE | `/sources/extractions/chip-flash-filesystem-complete-analysis.md` |
| **Interpreter Analysis** | Spin2_interpreter.spin2 | Bytecode, patterns | ✅ COMPLETE | `/sources/extractions/spin-interpreter-v51-complete-analysis.md` |
| **Debugger Analysis** | Spin2_debugger.spin2 | Debug protocol, UI | ✅ COMPLETE | `/sources/extractions/spin-debugger-v51-complete-analysis.md` |
| **Flash Loader Analysis** | Spin2_flash_loader.spin2 | Boot, programming | ✅ COMPLETE | `/sources/extractions/spin-flash-loader-v51-complete-analysis.md` |

### Hardware Module Extractions  
*These analyze hardware modules and breakout boards for system integration*

| Extraction | Primary Source | Content | Status | Location |
|-----------|----------------|---------|--------|-----------|
| **Edge 32MB Analysis** | P2 Edge 32MB Guide | Module specs, pinout | ✅ COMPLETE | `/sources/extractions/edge-32mb-complete-extraction-audit.md` |
| **Edge Standard Analysis** | P2 Edge Standard Guide | Standard module specs | ✅ COMPLETE | `/sources/extractions/edge-standard-complete-extraction-audit.md` |
| **Mini Breakout Analysis** | P2 Edge Mini Breakout Guide | Compact breakout (#64019) | ✅ COMPLETE | `/sources/extractions/edge-mini-breakout-complete-extraction-audit.md` |
| **Standard Breakout Analysis** | P2 Edge Standard Breakout Guide | Full 64-pin access (#64029) | ✅ COMPLETE | `/sources/extractions/edge-standard-breakout-complete-extraction-audit.md` |
| **Module Breadboard Analysis** | P2 Edge Module Breadboard Guide | Johnny Mac Board (#64020) | ✅ COMPLETE | `/sources/extractions/edge-module-breadboard-complete-extraction-audit.md` |
| **P2 Eval Board Rev C Analysis** | P2 Eval Board Rev C Guide | Evaluation platform (#64000) | ✅ COMPLETE | `/sources/extractions/p2-eval-board-rev-c-complete-extraction-audit.md` |
| **P2 Eval Add-on Boards Analysis** | P2 Eval Add-on Boards Product Guide | Accessory boards (#64006A-H, #64006-ES) | ✅ COMPLETE | `/sources/extractions/p2-eval-add-on-boards-complete-extraction-audit.md` |
| **Universal Motor Driver Analysis** | Universal Motor Driver P2 Add-on Board | High-power motor controller (#64010) | ✅ COMPLETE | `/sources/extractions/universal-motor-driver-p2-complete-extraction-audit.md` |
| **PropPlug Rev E Analysis** | PropPlug Rev E Programming Interface | USB-to-serial programming tool (#32201) | ✅ COMPLETE | `/sources/extractions/propplug-rev-e-complete-extraction-audit.md` |
| **P2 WX Adapter Analysis** | P2 WX Adapter Add-on Board | WiFi programming & communication adapter (#64007) | ✅ COMPLETE | `/sources/extractions/p2-wx-adapter-complete-extraction-audit.md` |
| **Parallax WX ESP8266 Module Analysis** | Parallax WX ESP8266 WiFi Module | ESP8266 WiFi module foundation for P2 wireless (#32420S/D) | ✅ COMPLETE | `/sources/extractions/parallax-wx-esp8266-wifi-module-complete-extraction-audit.md` |
| **Complete Ecosystem Matrix** | All hardware guides | Full compatibility analysis | ✅ COMPLETE | `/sources/extractions/p2-edge-complete-ecosystem-compatibility-matrix.md` |

### Targeted Content Extractions (PLANNED)
*These will extract specific content types from primary sources*

| Extraction | Primary Source | Target Content | Status | Purpose |
|-----------|----------------|----------------|--------|---------|
| **Code Examples Catalog** | Spin2 v51 + PASM2 Manual | 550+ code examples | 🔄 PLANNED | Individual example retrieval |
| **Instruction Timing Tables** | PASM2 Manual | Clock cycles per instruction | 🔄 PLANNED | Performance optimization |
| **Instruction Narratives** | PASM2 Manual tail sections | Missing instruction descriptions | 🔄 PLANNED | Complete 491 instruction set |
| **Terminal Windows Content** | Spin2 v51 | Debug UI components | ✅ PARTIAL | `/sources/extractions/spin2-terminal-windows.md` |

## 🖼️ VISUAL ASSETS EXTRACTION STATUS

### Image Extraction Pipeline Integration
**Work Mode Guide**: [Image Extraction Focused](../documentation/work-mode-guides/image-extraction-focused.md)  
**Complete Matrix**: [Image Extraction Matrix](visual-assets/INGESTION-IMAGE-EXTRACTION-MATRIX.md)  
**Total Assets Available**: 94/97+ images extracted (60 from P2 Edge ecosystem + 34 from Silicon Doc) (96.9% success rate)

#### Extraction Status Summary:
| Priority | Documents | Expected Images | Completed | Status |
|----------|-----------|-----------------|-----------|--------|
| 🔴 **Critical** | 3 (Silicon, Hardware, Smart Pins) | 60-90 images | 34 | 🟡 **IN PROGRESS** - Silicon Doc complete |
| 🟡 **High** | 6 (PASM2, Spin2, Tutorial + Eval boards) | 85-110 images | 0 | ❌ Pending extraction |
| ✅ **Complete** | 5 (P2 Edge ecosystem) | 60 images | 60 | ✅ Extracted & catalogued |

#### Consumer Integration:
- **Asset Distribution**: Systematic consumer registry tracks which extractions/documents can use each image
- **Technical Debt Integration**: Document enhancement opportunities automatically queued
- **Multi-session Support**: Large documents can be processed incrementally
- **Quality Validation**: Completeness validation ensures no missing assets

#### Available Asset Categories:
- **Technical Diagrams**: 50 images (pinouts, schematics, feature callouts)
- **Product Photos**: 10 images (hero shots, beauty images for marketing)
- **High-Resolution**: 27 images (≥800 pixels for detailed technical work)
- **Failed Extractions**: 3 images need manual capture (Mini Breakout xref 34 issues)

**Next Actions**: [Image Extraction Matrix](visual-assets/INGESTION-IMAGE-EXTRACTION-MATRIX.md) shows 9 high-value documents ready for extraction

## 📈 EXTRACTION RELATIONSHIPS

### Primary → Extraction → Analysis Flow

```
Parallax Spin2 Documentation v51.docx
├── spin2-v51-complete-extraction-audit.md (audit)
├── spin2-terminal-windows.md (specific extraction)
└── [PLANNED] spin2-code-examples-catalog.md (267 examples)

Propeller 2 Assembly Language Manual.docx  
├── pasm2-manual-complete-extraction-audit.md (audit)
├── [PLANNED] pasm2-instruction-timing-tables.md
├── [PLANNED] pasm2-instruction-narratives.md
└── [PLANNED] pasm2-code-examples-catalog.md

flash_fs.spin2 (source code)
├── chip-flash-filesystem-complete-analysis.md
└── chip-flash-filesystem-complete-analysis/ (detailed breakdowns)

Spin2_interpreter.spin2 (source code)
├── spin-interpreter-v51-complete-analysis.md
└── [PLANNED] interpreter-pattern-library.md
```

## 🎯 KNOWLEDGE COVERAGE BY SOURCE

### What Each Source Provides:

| Source | Primary Knowledge | Unique Content | Trust Level |
|--------|------------------|----------------|-------------|
| **Silicon Doc v35** | Architecture, instruction encodings | COG/Hub details | ✅ Authoritative |
| **Hardware Manual** | Boot process, pin descriptions | Physical specs | ✅ Authoritative |
| **Smart Pins rev 5** | All 32 pin modes | Configuration details | ✅ Complete |
| **PASM2 Manual** | 315 instruction details | Assembly patterns | ⚠️ Partial (64%) |
| **Spin2 v51** | Complete language spec | 267 code examples | ✅ Complete |
| **Spin Manual Draft** | Tutorial approach | Learning progression | ✅ Complete |
| **Q&A Spreadsheet** | Community knowledge | Folklore → Facts | ⚠️ Community |
| **Instructions CSV** | All 491 instructions | Encodings, flags | ✅ Authoritative |
| **Flash FS Code** | Production patterns | Real-world usage | ✅ Production |
| **P2 Edge 32MB Manual** | Module integration | System power, pinout | ✅ Authoritative |

## 📊 EXTRACTION METRICS

### Document Processing Statistics:

| Metric | Count | Notes |
|--------|-------|-------|
| **Total Primary Sources** | 11 | All Parallax official except DeSilva |
| **Total Extractions** | 13 | Completed audits and analyses |
| **Planned Extractions** | 5 | Code examples, timing, narratives |
| **Total Paragraphs** | 19,216+ | Structured content |
| **Total Tables** | 531+ | Data tables processed |
| **Code Examples Found** | 550+ | 267 in Spin2, others scattered |
| **Instructions Documented** | 315/491 | 64% complete |
| **Smart Pin Modes** | 32/32 | 100% complete |

## 🔍 GAPS AND OPPORTUNITIES

### Critical Missing Extractions:
1. **P1 DeSilva Tutorial Content** - PDF exists but never extracted (only style guide)
2. **Instruction Timing Data** - Rightmost column in PASM2 tables
3. **Code Example Catalog** - 550+ examples found but not individually accessible
4. **Instruction Narratives** - Tail sections of PASM2 manual

### Missing External Sources:
1. **OBEX Objects** - Awaiting selection/API access
2. **Forum Knowledge** - Not systematically extracted
3. **Chip's Engineering Notebooks** - Historical context
4. **Community Tutorials** - External educational content

## 🚀 OPERATIONS DASHBOARD INTEGRATION

### Quick Access Links:
- [V2 Extraction Index](EXTRACTION-INDEX-V2.md) - Primary tracking
- [Analysis Debt Master](../analysis-debt/ANALYSIS-DEBT-MASTER.md) - Research needs
- [Human TODOs](../human-todos/) - Audit preparation
- [Sprint Candidates](../sprint-candidates/) - Planning documents

### Current Sprint Focus:
- AD-007: Narrative consistency audit (FIRST)
- AD-001: Instruction relationship matrix
- AD-003: DeSilva P1 analysis → P2 guide
- AD-013: Code example extraction system
- Audit preparation bundle

### Repository Health:
- **Coverage**: 80% of P2 knowledge captured
- **Quality**: 100% clean extraction (V2)
- **Trust Levels**: 60% green, 30% yellow, 10% red
- **Active Gaps**: 176 instructions, timing data, code examples
- **Visual Assets**: 60/63 P2 Edge images extracted, 200+ additional images identified across 9 pending documents
- **Consumer Integration**: Asset registry system operational, technical debt tracking active

---

## Update Protocol

This catalog should be updated when:
1. New sources are ingested
2. Post-extraction analyses are completed  
3. Relationships between sources are identified
4. Gap discoveries are made
5. External sources become available

*Last Updated: 2025-08-19*
*Next Review: After code example extraction*