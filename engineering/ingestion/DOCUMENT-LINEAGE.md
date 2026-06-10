# P2 Knowledge Base - Document Lineage & Trust Map

**Purpose**: Track how all documents relate, their sources, and trust levels  
**Living Document**: Updated every time we add new documents  
**Last Updated**: June 10, 2026

## Lineage Philosophy

Every document in our knowledge base has:
- **Source lineage**: What it was derived from
- **Trust lineage**: How reliable the information is
- **Dependency chain**: What depends on this document
- **Overall trust**: Combined assessment for user confidence

## Supersessions

- **Spin2 language reference: v51a → v55 (2026-06-10).** `spin2_lang_ref_v55`
  (Parallax Spin2 Documentation v55, 2026-05-07) supersedes `spin2-v51` as the
  authoritative source for **Spin2 language facts** — it is the **matched-compiler
  edition** (pnut-ts v1.55.0 is ratified against PNut v55). Ingested as a *delta*
  (v52→v55) via the `ingest-source` skill; the v51 extraction is retained for
  lineage/diff. Delta features (`ENDIANL`/`ENDIANW`/`OFFSETOF`/`MOVBYTS`,
  structure bitfields, `NEXT`/`QUIT` levels, `DEBUG_END_SESSION`) were already
  in the KB; the audit confirmed 4 and routed 3 defects to the corrections
  register (F-098..F-100). See `sources/spin2_lang_ref_v55/spin2-v55-complete-extraction-audit.md`.

## Precise Source Attribution

### Import Source Files (Physical Sources)
```
📂 /import/
├── p2/
│   ├── pasm2-manual-extracted.txt
│   │   ├── Origin: Propeller 2 Assembly Language (PASM2) Manual.docx
│   │   ├── Date: November 1, 2022
│   │   ├── Status: PRELIMINARY (Parallax)
│   │   ├── Authority: Parallax Inc. official (incomplete)
│   │   └── Size: 10,771 paragraphs, 219 tables
│   │
│   ├── spin2-v51-documentation.pdf (EXPECTED)
│   │   ├── Origin: SPIN2 v51 Documentation Package
│   │   ├── Date: 2025
│   │   ├── Status: PRODUCTION RELEASE
│   │   ├── Authority: Parallax Inc. official
│   │   └── Contains: Debugger, Terminal Windows, Language Reference
│   │
│   └── p2-silicon-documentation.pdf (EXPECTED)
│       ├── Origin: P2 Hardware Documentation
│       ├── Date: Latest silicon revision
│       ├── Status: PRODUCTION
│       └── Authority: Parallax Inc. official
│
├── source-code/
│   ├── spin-interpreter/v51/Spin2_interpreter.spin2
│   │   ├── Origin: SPIN2 v51 Distribution
│   │   ├── Authority: Parallax Inc. official production source
│   │   ├── Analysis: /sources/extractions/spin-interpreter-v51-complete-analysis.md
│   │   └── Trust: 🟢 GREEN SOURCE VALIDATED
│   │
│   ├── chip-flash-filesystem/flash_fs_v2.0.0.spin2
│   │   ├── Origin: Chip Gracey's P2 Edge Module filesystem
│   │   ├── Core System: Chip Gracey (P2 architect, flash algorithms)
│   │   ├── Production Enhancements: Stephen M. Moraco (Iron Sheep Productions, LLC)
│   │   │   ├── Full File System API wrapper
│   │   │   ├── Multi-COG locking system implementation
│   │   │   ├── Comprehensive unit testing framework (1000+ tests)
│   │   │   └── System integration and robustness validation
│   │   ├── Additional Contributors: Jon McPhalen
│   │   ├── Analysis: /sources/extractions/chip-flash-filesystem-complete-analysis.md
│   │   └── Trust: 🟢 GREEN SOURCE VALIDATED
│   │
│   ├── spin-debugger/v51/ (PENDING)
│   └── spin-flash-loader/v51/ (PENDING)
│
└── screenshots/ (CRITICAL - IN PROGRESS)
    ├── debugger-windows/ (Priority 1-6)
    ├── terminal-windows/ (Priority 7-12)
    ├── architecture-diagrams/ (Priority 13-18)
    └── timing-diagrams/ (Priority 19-24)
```

### Source-to-Extraction Mapping
```
Source Attribution Chain:

/import/p2/pasm2-manual-extracted.txt
    ↓ extracted_to
/sources/extractions/pasm2-manual-complete-extraction-audit.md
    ↓ powers
/ai-reference/v1.0/instructions/pasm2-instruction-reference.json (incomplete)
    ↓ intended_for
/documents/pasm2-user-manual/ (FUTURE)

/import/source-code/spin-interpreter/v51/Spin2_interpreter.spin2
    ↓ analyzed_with
7-Phase Enhanced Source Code Ingestion Methodology v2.0
    ↓ produced
/sources/extractions/spin-interpreter-v51-complete-analysis.md
    ↓ enables
P2 Bytecode Specification Document (PIPELINE)
    ↓ creates
Binary Decoder Tool for PNut Term Integration

/import/source-code/chip-flash-filesystem/flash_fs_v2.0.0.spin2
    ↓ analyzed_with
7-Phase Enhanced Source Code Ingestion Methodology v2.0
    ↓ produced
/sources/extractions/chip-flash-filesystem-complete-analysis.md
    ↓ provides
35+ Production P2 Patterns for Developer Reference
```

## Primary Source Materials (Root Level)

### 🟢 **Official Parallax Documentation** (Trust: VERIFIED)
```
📄 P2 Silicon Documentation
├── Hub Memory Architecture
├── COG Instruction Processing  
├── Smart Pin Subsystem
└── CORDIC Math Engine

📄 P2 SPIN2 Documentation v51
├── SPIN2 Language Reference
├── Terminal Window System  
├── Single-Step Debugger
└── DEBUG Output System

📄 P2 Assembly Language (PASM2) Manual
├── Instruction Set (491 instructions)
├── Assembly Syntax & Directives
├── Memory Organization
└── Programming Patterns

📄 P2 Hardware Manual  
├── Physical Specifications
├── Pin Configurations
├── Power Requirements
└── Package Information

📄 P2 Instruction Spreadsheet
├── Complete instruction catalog
├── Opcode mappings
├── Parameter definitions
└── Encoding details
```

### 🟡 **Community Documentation** (Trust: FOLKLORE→FACT)
```
📄 Smart Pins Documentation (Jon Titus)
├── Pin Mode Descriptions
├── Configuration Examples
├── Timing Specifications
└── Application Notes

📄 Forum Knowledge Base
├── Usage patterns and tips
├── Common problems/solutions  
├── Community best practices
└── Real-world examples
```

## Extraction Layer (Level 2)

### From SPIN2 v51 Documentation
```
📄 SPIN2 v51 Documentation
├── sources/extractions/spin2-terminal-windows.md (✅ COMPLETE)
│   ├── Trust: 🟢 VERIFIED (direct extraction)
│   ├── Completeness: 95% (missing advanced features)
│   └── Dependencies: → Terminal Window Manual
│
├── sources/extractions/spin2-debugger.md (✅ COMPLETE)
│   ├── Trust: 🟡 MOSTLY-VERIFIED (multi-COG gaps)
│   ├── Completeness: 85% (needs validation)
│   └── Dependencies: → Debugger Manual
│
└── sources/extractions/spin2-language-core.md (🟡 PLANNED)
    ├── Trust: 🟢 VERIFIED (when complete)
    ├── Completeness: 0% (not started)
    └── Dependencies: → SPIN2 Language JSON
```

### From PASM2 Manual
```
📄 PASM2 Manual
├── sources/extractions/pasm2-manual-complete-extraction-audit.md (🔴 SHALLOW)
│   ├── Trust: 🔴 SEVERELY INCOMPLETE - Syntax-only documentation
│   ├── Deep Documentation: 0.4% (1 of 272 instructions with deep explanatory content)
│   ├── Syntax Coverage: 55% (272 of 491 instructions have basic syntax entries)
│   ├── Source: Propeller 2 Assembly Language (PASM2) Manual, November 1, 2022 (PRELIMINARY)
│   ├── Reality Check: Mostly basic syntax, lacks deep descriptive paragraphs
│   ├── Gaps: 219 instructions missing entirely, 271 lack comprehensive explanation
│   └── Dependencies: → PASM2 Instruction JSON (severely incomplete for AI use)
│
└── sources/extractions/pasm2-programming-patterns.md (🔴 PLANNED)
    ├── Trust: 🟢 VERIFIED (when complete)
    ├── Completeness: 0% (not started)
    └── Dependencies: → Pattern Library
```

### From Hardware Manual
```
📄 Hardware Manual
├── sources/extractions/hardware-architecture.md (✅ COMPLETE)
│   ├── Trust: 🟢 VERIFIED (official source)
│   ├── Completeness: 90% (missing some timing details)
│   └── Dependencies: → Architecture JSON
│
└── sources/extractions/hardware-pinout.md (🔴 PLANNED)
    ├── Trust: 🟢 VERIFIED (when complete)
    ├── Completeness: 0% (not started)
    └── Dependencies: → Hardware Interface Guide
```

## AI-Optimized Layer (Level 3)

### JSON Schema References
```
📄 AI Reference JSONs
├── ai-reference/v1.0/instructions/pasm2-instruction-reference.json (🔴 INCOMPLETE)
│   ├── Sources: pasm2-manual-complete-extraction-audit.md + P2 Instruction Spreadsheet
│   ├── Trust: 🔴 INCOMPLETE (only 5 complete entries + category lists)
│   ├── Completeness: ~1% (5 detailed instructions of 491, category summaries only)
│   ├── Source Files: 
│   │   ├── PASM2 Manual November 1, 2022 (PRELIMINARY) → 315 instructions
│   │   └── P2 Instruction Spreadsheet → Encoding reference
│   └── Dependencies: → AI Code Generation Tools (BLOCKED - insufficient data)
│
├── ai-reference/v1.0/language/spin2-language.json (🟡 IN PROGRESS)  
│   ├── Sources: spin2-language-core.md + SPIN2 v51 Documentation
│   ├── Trust: 🟡 PARTIAL (in development)
│   ├── Completeness: 60% (core language done)
│   └── Dependencies: → AI Syntax Assistance
│
└── ai-reference/v1.0/architecture/p2-architecture.json (🟡 IN PROGRESS)
    ├── Sources: hardware-architecture.md + Silicon Documentation
    ├── Trust: 🟡 PARTIAL (in development)
    ├── Completeness: 70% (major subsystems done)
    └── Dependencies: → AI System Design Tools
```

## User Manual Layer (Level 4)

### Professional Documentation
```
📄 User Manuals
├── documentation/manuals/debugger-manual.md (✅ COMPLETE)
│   ├── Sources: spin2-debugger.md + Screenshots + Version History
│   ├── Trust: 🟡 READY-FOR-V1.0 (multi-COG needs validation)
│   ├── Completeness: 90% (comprehensive with history appendix)
│   └── Dependencies: → Professional PDF via Pages
│
├── documentation/manuals/terminal-window-manual.md (🔴 PLANNED)
│   ├── Sources: spin2-terminal-windows.md + Screenshots
│   ├── Trust: 🟢 HIGH (when complete)
│   ├── Completeness: 0% (not started)
│   └── Dependencies: → Professional PDF via Pages
│
└── documentation/manuals/hardware-interface-guide.md (🔴 FUTURE)
    ├── Sources: hardware-pinout.md + Smart Pins docs + Examples
    ├── Trust: 🟢 HIGH (when complete)
    ├── Completeness: 0% (V1.1+ target)
    └── Dependencies: → Professional PDF via Pages
```

## Visual Assets Layer (Cross-cutting)

### Screenshot Integration
```
📄 Visual Documentation
├── exports/images/v1.0/ (🟡 IN PROGRESS - Stephen capturing)
│   ├── Sources: FINAL-SCREENSHOT-NEEDS-V2.md priorities
│   ├── Trust: 🟢 VERIFIED (primary source captures)
│   ├── Completeness: 0% → 100% (24 priority assets)
│   └── Dependencies: → ALL manuals (critical for understanding)
│
├── Architecture diagrams (🔴 CRITICAL - 6 assets)
│   ├── Hub Memory Architecture
│   ├── Smart Pin Block Diagram  
│   ├── Pipeline Execution
│   └── Dependencies: → Debugger Manual, AI Architecture JSON
│
├── Timing diagrams (🟡 IMPORTANT - 8 assets)  
│   ├── Boot Sequence Timing
│   ├── Streamer Modes
│   ├── Event System
│   └── Dependencies: → All technical manuals
│
└── IDE screenshots (🟢 HELPFUL - 10 assets)
    ├── PropellerTool Layout
    ├── Debug Windows
    ├── Error Examples  
    └── Dependencies: → All user manuals
```

## Trust Propagation Rules

### Trust Level Inheritance
1. **🟢 VERIFIED**: Direct from official Parallax sources
2. **🟡 FOLKLORE→FACT**: Community knowledge being validated  
3. **🟡 MOSTLY-VERIFIED**: Official source with identified gaps
4. **🟡 PARTIAL**: Work in progress, incomplete
5. **🔴 PLANNED**: Not started, trust TBD

### Trust Enhancement Paths
```
🔴 PLANNED → 🟡 PARTIAL → 🟡 MOSTLY-VERIFIED → 🟢 VERIFIED
                ↓
🟡 FOLKLORE→FACT (community validation) → 🟢 VERIFIED
```

### Overall Document Trust Assessment
```
Debugger Manual v1.0:
├── Source lineage: spin2-debugger.md (🟡) + Screenshots (🟢) + History (🟢)
├── Combined trust: 🟡 READY-FOR-V1.0  
├── Confidence: High for basic debugging, gaps noted for multi-COG
└── Recommendation: Ship V1.0, enhance V1.1 with community validation
```

## Dependency Impact Analysis

### Critical Path Dependencies
```
📄 PASM2 Instruction JSON (COMPLETE) 
    ↓ enables
🤖 AI Code Generation (ACTIVE)
    ↓ proves
🎯 P2 Production Development (SUCCESS METRIC)

📄 Screenshots (IN PROGRESS - Stephen)
    ↓ enhances  
📚 All User Manuals (BLOCKED until images)
    ↓ enables
🎯 Professional Documentation (SUCCESS METRIC)
```

### Document Interdependencies
```
SPIN2 Language JSON ←→ Debugger Manual (cross-references)
Architecture JSON ←→ Hardware Guide (shared concepts)  
Pattern Library ←→ All Manuals (example code)
Screenshots ←→ All Manuals (visual understanding)
```

## Living Lineage Maintenance

### When Adding New Documents
1. **Identify sources**: What was this derived from?
2. **Assess trust**: How reliable is the source material?
3. **Map dependencies**: What depends on this document?
4. **Update lineage**: Add to this mapping document
5. **Propagate trust**: Update dependent document trust levels

### Example New Document Addition
```
📄 NEW: Smart Pins Advanced Guide
├── Sources: Smart Pins Documentation (🟡) + Forum Examples (🟡) + Testing (🟢)
├── Trust: 🟡 MOSTLY-VERIFIED (needs expert validation)
├── Dependencies: → Hardware Interface Guide, AI Architecture JSON
├── Added to: DOCUMENT-LINEAGE.md (this file)
└── Trust update: Hardware Interface Guide trust level reassessed
```

## Release Trust Assessment

### V1.0 Release Trust Summary
| Document | Trust Level | Release Ready | Notes |
|----------|-------------|---------------|-------|
| Debugger Manual | 🟡 READY-FOR-V1.0 | ✅ YES | Multi-COG gaps noted |
| PASM2 JSON | 🟢 VERIFIED | ✅ YES | Complete and accurate |
| SPIN2 JSON | 🟡 PARTIAL | ⚠️ MAYBE | Core features ready |
| Architecture JSON | 🟡 PARTIAL | ⚠️ MAYBE | Major subsystems ready |

### Trust Improvement Roadmap
- **V1.0**: Ship with clear gap documentation
- **V1.1**: Fill gaps with community validation
- **V1.2**: Expert review (Chip) for technical accuracy
- **V2.0**: Comprehensive validation across all documents

## Visual Lineage Map

```
[Official Parallax Docs] 🟢
        ↓
[V2 Extractions] 🟢→🟡
        ↓
[AI-Optimized JSONs] 🟡→🟢
        ↓
[User Manuals] 🟡
        ↓
[Professional PDFs] 🟢

[Screenshots] 🟢 → [All Manuals] (cross-cutting enhancement)
[Community Knowledge] 🟡 → [All Documents] (validation layer)
[Expert Review] 🟢 → [All Documents] (accuracy verification)
```

## Maintenance Schedule

- **Weekly**: Update during active development
- **Per release**: Comprehensive trust assessment  
- **Per new document**: Immediate lineage addition
- **Quarterly**: Full dependency review and optimization

---

**Lineage Authority**: Based on documented extraction process and source analysis  
**Trust Methodology**: Combination of source reliability and validation status  
**Update Responsibility**: Claude maintains during development, Stephen approves for releases