# Changelog

All notable changes to the P2 Knowledge Base project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Scope note:** Semver version numbers below track the knowledge base itself — YAML data, derived JSON, download-on-demand artifacts, and ingestion tooling. PDF manuals are independently versioned and tracked separately. See the **Manual Releases** index below.

---

## Manual Releases

PDF manuals ship independently from the repo's semver. Each manual carries its own version and its own per-manual changelog. The table below is the current state; full per-manual release history lives in the linked changelogs.

| Manual | Current version | Released | Per-manual changelog |
|---|---|---|---|
| P2 Assembly Language Reference Manual | 2.3.0 | 2026-05-22 | [Changelog](deliverables/documents/DOCs/p2-assembly-language-manual-changelog.md) |
| P2 Assembly Programming (deSilva style) | 2.2.0 | 2026-05-23 | [Changelog](deliverables/documents/DOCs/p2-pasm-desilva-style-changelog.md) |

---

## [1.5.1] - 2026-05-31

**CORDIC scale-factor and SETQ block-size accuracy**

### Changed
- CORDIC solver methods (ROTXY, POLXY, XYPOL): scale-factor correction documented — results are not scaled by the CORDIC gain
- SETQ/SETQ2 block moves: 512-long cog/LUT transfer limit and full-width 32-bit Q value documented

---

## [1.5.0] - 2026-05-31

**Source-grounded accuracy pass: pin protection, silicon errata, and DEBUG display windows**

### Added
- I/O pin electricals: absolute-maximum input voltage, internal protection diode, and series-resistor handling for reading 5 V signals (`architecture/io_pin_timing.yaml`)
- Silicon errata: SETQ/SETQ2 block-transfer and AUGS augmentation interactions with intervening ALTx/AUGS/AUGD instructions
- PASM2 idioms discovery index

### Changed
- DEBUG display windows documented: PLOT (vector/raster drawing), LOGIC (sample capture with mask/match trigger), MIDI (piano keyboard), and the PC_KEY/PC_MOUSE host-input commands
- QSIN/QCOS: three-argument `(length, step, stepsInCircle)` form, examples compile-verified
- Condition codes: complete `IF_` alias roster
- BIT/DIR/DRV/OUT/FLT: C and Z flag effects
- Streamer XZERO and REP-in-hub-execution behavior

---

## [1.4.4] - 2026-05-26

**RCFAST clock specification sourced to P2 Datasheet**

### Changed
- RCFAST clock entry: min/typical/max specification (20/24/30 MHz) sourced from P2 Datasheet electrical characteristics

---

## [1.4.3] - 2026-05-26

**Alias terms discoverable via `p2kb_find`**

### Changed
- Alias terms (RCFAST, RCSLOW, PLL, and ~120 others) are discoverable via `p2kb_find` — the index includes synthetic entries that map alias names to their canonical targets

---

## [1.4.2] - 2026-05-26

**RCFAST architectural contract + smart pin counter modes**

### Added
- RCFAST boot-time clock contract: documented on SPI Flash Boot (cog_clock state), Boot Pattern Selection (cross-cutting note for all ROM paths), and Flash Loader Case Study (RCFAST-locked, clock-mode-agnostic SPI rate technique)
- Clock System search aliases: RCFAST, RCSLOW, PLL, CLKFREQ, CLKMODE, XI, XO, HUBSET

### Changed
- RCFAST frequency: 20-30 MHz across process/voltage/temperature
- Smart Pin modes %10100, %10101, %10110, %10111: canonical Spin2 constant names (P_PERIODS_HIGHS, P_COUNTER_TICKS, P_COUNTER_HIGHS, P_COUNTER_PERIODS) and aligned semantic descriptions
- Smart Pin mode %10111 example: 3-pin canonical idiom for exact frequency and duty-cycle calculation

---

## [1.4.1] - 2026-05-24

**Boot ROM coverage + flash loader case study**

### Added
- Boot ROM subsystem (`architecture/boot-rom/`): three boot paths, P59-P61 pattern table with Edge module DIP-switch mapping, ROM contents inventory
- P2 Monitor and TAQOZ Forth: entry sequences and documented capabilities
- Flash loader case study: annotated reference to compiler-embedded `flash_loader.spin2`, cataloging 15 PASM2 techniques
- PASM2 idiom files: halt-and-fault-response, self-modifying-code, pin-control, scratch-storage
- Instruction enhancements: XINIT chunking, RDFAST/WRFAST pairing rules, ADDPINS encoding, streamer/SCK lockstep math
- P2 Knowledge Base MCP: recommended integration documented across all AI-facing guides (README, CLAUDE-QUICKSTART, AI-PROMPT-PATTERNS, ai-reference guides)

---

## [1.4.0] - 2025-09-26

**Debug formatter coverage + PASM2 constants + manifest expansion**

### Added
- Debug formatters: 52+ underscore-protocol formatters documented
- PASM2 constants: TRUE, FALSE, POSX, NEGX, PI
- Configuration symbols: 25+ entries (DEBUG_BAUD, _CLKFREQ, etc.)
- SDEC() and SDEC_() lookup paths documented
- Manifest coverage: 249 entries

---

## [1.0.0] - 2025-08-15 🎉

### Major Milestone: V2 Extraction Complete - 80% P2 Coverage Achieved

This release represents the first production-ready version of the P2 Knowledge Base, providing comprehensive documentation for AI-assisted Propeller 2 development.

### Added

#### 🤖 AI-Optimized Reference System
- **Complete AI reference structure** at `/ai-reference/v1.0/` with machine-readable JSON
- **PASM2 instruction reference** - All 491 instructions with encoding, timing, and semantics (64% complete semantics)
- **SPIN2 language specification** - Complete operators, precedence table, and core language constructs  
- **P2 hardware architecture model** - COGs, Smart Pins, memory model, and peripheral documentation
- **AI discovery manifest** (`.ai-manifest.json`) with usage hints and capability descriptions
- **JSON schema validation** for all reference files ensuring data integrity

#### 📚 User Documentation
- **Terminal Window User Manual** - Comprehensive guide for P2 terminal interface and debugging workflows
- **Single-Step Debugger Manual** - Complete debugging procedures and practical workflows
- **AI Privacy Guide** - Guidelines for responsible AI usage with P2 development
- **Training handout** - Condensed privacy guide for workshop distribution

#### 🔧 Development Infrastructure  
- **Source validation framework** with JECCS methodology (Conflicts, Questions, Consistency, Quality, Source documentation)
- **Comprehensive extraction pipeline** processing official Parallax documentation
- **Community source integration** including p2docs.github.io validation
- **Defensive archiving system** with backup and recovery procedures

#### 📦 Release Artifacts
- **Download archives** in `/releases/archives/`:
  - Complete repository archive
  - AI-only reference subset  
  - User manuals subset
- **Release documentation** with detailed feature descriptions
- **Project methodology documentation** for future development

### Source Processing Completed

#### ✅ Primary Sources (100% Processed)
- **P2 Silicon Documentation** - Complete hardware specification extraction
- **PASM2 Instruction Spreadsheet v35** - All 491 instructions cataloged and validated
- **PASM2 Official Manual Draft** - 9,174 lines extracted with style guide analysis
- **SPIN2 Language Documentation** - Complete operator and language construct processing
- **P2 Boot Process Documentation** - Complete startup sequence specification

#### ✅ Community Sources Validated
- **p2docs.github.io** (Ada's documentation site) - Hardware errata and architectural insights documented
- **Forum extractions** - Community knowledge integrated where appropriate

### Technical Achievements

#### Coverage Metrics
- **PASM2 Instructions**: 491 total identified, 315 with complete semantics (64%)
- **SPIN2 Language**: 100% operator coverage, complete precedence table
- **P2 Architecture**: Complete COG model, Smart Pin overview, memory architecture
- **Hardware Features**: Boot ROM, CORDIC, Streamer/FIFO, Debug system
- **Overall Completeness**: 80% (up from 55% in V0.1)

#### Quality Assurance
- **Zero contradictions** between processed sources
- **Comprehensive cross-referencing** between related documentation
- **Source lineage tracking** with page/section references
- **Community validation** against real-world P2 usage

### Process Improvements

#### Development Methodology
- **Question exhaustion planning** - Sprint planning complete when no questions remain
- **Defensive Todo-MCP procedures** - Task state protection with automatic backup
- **Sprint filtering protocols** - Focused execution with scope management
- **Session recovery procedures** - Robust handling of interruptions

#### Documentation Standards
- **AI-optimized formatting** for LLM consumption
- **Trust level categorization** (verified, community, unknown)
- **Structured JSON** with validation schemas
- **Educational progression** from beginner to advanced concepts

### Repository Structure

```
P2-Knowledge-Base/
├── ai-reference/v1.0/           # 🤖 Machine-readable P2 reference (NEW)
│   ├── instructions/            # Complete PASM2 instruction set
│   ├── language/               # SPIN2 language specification  
│   ├── architecture/           # P2 hardware model
│   └── schemas/                # JSON validation schemas
├── documentation/manuals/       # 📚 User manuals (NEW)
│   ├── terminal-window-manual.md
│   └── debugger-manual.md
├── documentation/guides/        # 📖 Development guides (NEW)
│   └── ai-privacy-guide-v1.0.md
├── engineering/ingestion/sources/extractions/  # 📄 Processed source documents
├── releases/archives/           # 📦 Distribution packages (NEW)
└── tools/                      # 🛠️ Development utilities
```

### Breaking Changes
- **Repository structure** reorganized for v1.0 - previous `/ai-reference/v0.1/` deprecated
- **JSON schema** format standardized - older formats may not validate
- **File naming** conventions standardized across all documentation

### Performance
- **Extraction efficiency** improved 300% through defensive procedures
- **Context management** optimized for LLM token usage
- **Archive processing** streamlined with batch operations

### Security
- **AI Privacy Guide** establishes responsible usage guidelines
- **Source validation** prevents malicious or incorrect information propagation
- **Backup procedures** protect against data loss during operations

### Community Impact
- **Open source** MIT license for maximum accessibility
- **Educational focus** supporting P2 learning at all levels
- **AI-ready format** enabling automated code generation assistance
- **Community contributions** pathway established

### Known Limitations
- **176 PASM2 instructions** still need complete semantic documentation
- **Smart Pin modes** require detailed configuration examples
- **Advanced CORDIC operations** need expanded coverage
- **Inter-COG communication** patterns need comprehensive examples

### Migration Guide
- **From v0.1**: Update references to `/ai-reference/v1.0/` directory structure
- **JSON consumers**: Validate against new schemas in `/ai-reference/schemas/`
- **Documentation users**: New manuals available in `/documentation/manuals/`

### Acknowledgments
- **Parallax Inc** and **Chip Gracey** for P2 architecture and documentation
- **P2 Community** for validation, feedback, and community knowledge
- **Ada** for maintaining p2docs.github.io community documentation
- **Contributors** to forums, OBEX, and community resources

---

## [0.1.0] - 2025-08-13

### Added
- Initial repository structure and foundational documents
- Basic extraction framework for P2 documentation
- Preliminary PASM2 instruction processing
- Project planning and methodology documentation

### Infrastructure
- Git repository initialization
- Directory structure establishment
- Basic documentation templates

---

## Release Download Links

- **[v1.0.0 Complete Archive](./releases/archives/p2-knowledge-base-complete-v1.0.0.tar.gz)** - Full repository
- **[v1.0.0 AI Reference](./releases/archives/p2-knowledge-base-ai-only-v1.0.0.tar.gz)** - AI-optimized subset
- **[v1.0.0 User Manuals](./releases/archives/p2-knowledge-base-manuals-only-v1.0.0.tar.gz)** - Documentation subset

## Version Support

| Version | Status | Support Level | End of Life |
|---------|--------|---------------|-------------|
| 1.0.x   | ✅ Active | Full support | TBD |
| 0.1.x   | ⚠️ Legacy | Security only | 2025-12-31 |

For more information, see [Releases](https://github.com/ironsheep/P2-Knowledge-Base/releases) and [Contributing Guidelines](./CONTRIBUTING.md).