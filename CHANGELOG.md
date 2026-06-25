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

## [1.11.2] - 2026-06-25

**CORDIC rotation, COGINIT, and LSTRING reference accuracy**

### Changed
- CORDIC vector rotation (QROTATE): the X coordinate comes from the D operand, the Y coordinate from the SETQ value, and the rotation angle from the S operand, with results retrieved via GETQX/GETQY.
- COGINIT loads 504 longs ($000–$1F7) from hub into the target cog's registers.
- LSTRING() documents its `{Spin2_v43}` version directive — the string composer is enabled once that directive (or later) leads the source file.

## [1.11.1] - 2026-06-25

**PASM2 reference accuracy: GETBRK, the program counter, and signed flag semantics**

### Changed
- GETBRK: complete per-flag-effect reference — cog internal status and the debug break code (WCZ), skip/XBYTE state and CALL depth (WC), and queued skip/XBYTE pattern detection (WZ), each with a worked example.
- Program counter: access documented as the return address saved by CALLD/CALL/CALLPA/CALLPB.
- Signed add and subtract: the C flag is documented as the true sign of the full-precision, overflow-corrected result.

## [1.11.0] - 2026-06-24

**Eval add-on board model and hub/LUT immediate-addressing contract**

### Added
- Eval add-on boards: a standardized, self-contained reference shape across the add-on board line, including a new HyperRAM/HyperFlash board.
- RDLUT/WRLUT: the plain-immediate address range (0–255) is documented, with full 512-long LUT access via register or PTRA/PTRB operands.
- Hub memory instructions (RDLONG/WRLONG, RDBYTE/WRBYTE, RDWORD/WRWORD, WMLONG): the shared plain-immediate addressing contract is documented.

## [1.10.1] - 2026-06-20

**Smart Pin reference depth and language accuracy, with new silicon-grounded detail**

### Added
- WRPIN: A/B input-selector encoding documented — relative-pin routing (±1..±3), own-OUT-bit select, and invert, the basis for clock-from-adjacent-pin wiring.
- USB host/device (%11011): full register layer documented — WXPIN config word, WYPIN line-state commands, the 16-bit receiver status word, and per-pin IN semantics.
- Smart-pin timing modes (%10000–%10011): the DIR=0 `Z` preload value is documented for each.
- DAC dither modes (%00010/%00011): the nominal, time-averaged nature of the 16-bit output is documented.
- Async serial transmit (%11110): the first-byte line-state behavior is documented with its pre-clear workaround.
- TASKCONT: task-continuation method documented.

### Changed
- Smart-pin usage patterns aligned with the per-mode register reference (repository, ADC, quadrature, initialization order).
- CORDIC, interrupt, and addressing-mode references aligned with the silicon documentation.
- Operator and precedence references aligned with Spin2 v55 (post-clear/post-set operators, ADDBITS/ADDPINS, P2 precedence ordering).
- Streamer pin-group and DEBUG SCOPE/PLOT references aligned with the silicon documentation.
- Edge module flash and PSRAM details aligned across the hardware comparison, selection, and compatibility references.

## [1.10.0] - 2026-06-18

**DEBUG display feed idioms and smart-pin example sequencing, hardware-verified**

### Added
- DEBUG display windows: window placement is optional — omit `POS` to let the display host auto-arrange windows without overlap; supply `POS` only for a fixed position.
- TERM: value display documented — substitute a value's decimal text into single-quoted window text with `` `(value) ``.
- LOGIC: `HOLDOFF` semantics documented — initial value, counter reset on a supplied count, and the bare-form no-op.
- MIDI: a velocity-0 Note-On does not release a key in this window; send an explicit Note-Off.
- Smart pin %00101 (transition output): a non-zero Y drives that many transitions; Y=0 holds the pin idle.

### Changed
- DEBUG display windows: channel and trigger setup (SCOPE, FFT) is a one-time configuration message sent after the window is created, separate from the create line.
- Smart-pin examples: unified initialization order across all modes — configure, enable, then operate (`WYPIN` follows enable).

## [1.9.1] - 2026-06-14

**DEBUG display directive accuracy across all nine windows**

### Added
- DEBUG display windows: per-window `CLOSE` directive documented for all nine windows (LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, PLOT, TERM, BITMAP, MIDI) and the DEBUG statement reference — closes one named window, distinct from ending the whole DEBUG session.

### Changed
- DEBUG statement reference: formatter vocabulary documented as the working set (`UDEC`/`SDEC`, `UHEX`/`SHEX`, `UBIN`/`SBIN`, `FDEC`, `ZSTR`/`LSTR`, with size and value-only variants), cross-linked to the formatters overview; examples use the create-then-feed display syntax.
- DEBUG display directive parameters documented to the PNut v55 source: SCOPE_XY window size and POLAR `twopi` winding (0 vs −1), PLOT `SPRITEDEF`/`LUTCOLORS` palette sizing (supply the colors your pixels reference, up to 256).

## [1.9.0] - 2026-06-13

**Smart-pin and DEBUG accuracy, plus hardware findability**

### Added
- DEBUG string quoting: the single-quote rule for backtick display-command text (window `TITLE`, `SAVE`/layer filenames) versus the double-quote rule for data/formatter `debug()`, including the silent-failure case where a double-quoted display argument is dropped at runtime with no compile error.
- Hardware findability: natural-language `aliases:` on every hardware entry plus category browsing for development boards, Edge modules, carriers, add-on boards, and adapters, with the board/adapter compatibility matrix surfaced as the hub.

### Changed
- Smart-pin documentation aligned with the silicon: long-repository mode writes via WXPIN; ADC X[5:4] selects SINC2 sampling / SINC2 filtering / SINC3 filtering / bitstream capture; DAC-noise behavior and the mode-summary serial/counter labels.

## [1.8.0] - 2026-06-11

**DEBUG display windows: a complete PNut v55 directive reference for all nine visualizers**

### Added
- DEBUG display windows (`language/spin2/debug-displays/`): all nine visualizers — TERM, SCOPE, SCOPE_XY, FFT, SPECTRO, BITMAP, LOGIC, PLOT, MIDI — carry the PNut v55 directive surface: configuration and display directives with parameter ranges and defaults, the supported color and sample-packing modes, channel/geometry grammar, and a `not_supported:` block per window stating each window's real boundaries.
- SCOPE_XY window: XY / Lissajous / polar (rho-theta) display documented as its own window, including persistence-on-SAMPLES and the polar twopi/theta controls.
- Compile-verified examples for every window (all examples build under the pnut_ts v1.55.0 DEBUG compiler).

### Changed
- DEBUG display findability: natural-language `aliases:` on every window (e.g. "logic analyzer", "oscilloscope", "spectrogram", "piano keyboard"), a `spin2.debug_displays` category, and direct `related:` links from the DEBUG statement entry to all nine windows — so an agent querying by intent lands on the right window.

## [1.7.0] - 2026-06-11

**Decomposition reasoning layer: a generative method for cutting a P2 design across cogs, smart pins, and the parallel fabric**

### Added
- Decomposition reasoning layer (`architecture/decomposition/`): a generative method that derives a design's cog and resource boundaries from four forces — resource ownership, data-flow contracts, rate adaptation, and altitude layering — alongside the cross-cutting forces, a shared glossary, and an ordered first-contact procedure for approaching an unfamiliar build.
- Evaluation-vocabulary, resource-budget, and spatial-computing lenses for judging a decomposition (coupling, connascence, back-pressure, and pushing work to the autonomous pin edge).
- End-to-end worked derivation — a walking robot taken from first contact to a concrete cog map — showing the method applied in full.
- Four Spin2 implementation patterns, each compile-verified with pnut_ts: a latest-wins command mailbox with seq/ack handshake, a rate-domain decoupler, a slew/easing engine, and in-cog cooperative tasking.
- The layer is cross-linked with the existing Spin2 pattern library and the P2 architecture mental model, so an agent building a system reaches the method from where it already is.

## [1.6.3] - 2026-06-10

**Knowledge-base accuracy pass: PASM2 instructions, assembler directives, and clock/architecture entries aligned to compiler and silicon ground truth**

### Changed
- PASM2 instruction flags and timing aligned with the pnut-ts compiler and P2 Instructions CSV: signed add/subtract C is the sign of the result; conditional/event jumps and lock/hub-write instructions carry their variable timing; GETSCP, RDLONG, and the LOCK instructions carry their correct write and flag effects.
- NEXT/QUIT loop control documented as `NEXT level` / `QUIT level` (1-15, counting outward from the current loop).
- Assembler directives ORG, ORGF, ORGH, FIT, and BYTE/WORD/LONG/FILE documented to current compiler behavior: COG+LUT address ranges, auto-limits, hub-origin defaults and the $100000 ceiling, and filename rules.
- HUBSET clock-configuration operand map, crystal/cap and clock-source fields, and PLL examples aligned with the silicon documentation; XI direct-input limit is 200 MHz.
- GETCT documented as a 64-bit counter (WC selects the upper 32 bits); CORDIC QLOG/QEXP as base-2 log/antilog in 5:27 fixed-point.
- HUBEXEC value, XBYTE/EXECF LUT layout, chip-reset HUBSET mode, and smart-pin ADC gains (sqrt-10-spaced ladder) aligned with silicon.
- PASM2 encoding reference Flags column reflects each instruction's actual C/Z effects.

### Added
- DEBUG_END_SESSION behavior and AI-assisted-development purpose documented from the Spin2 v55 specification.
- Silicon errata for the SETQ-block / AUGS-AUGD interaction on PASM2 augment instructions.

## [1.6.2] - 2026-06-03

**Streamer NCO timing and mode-configuration coverage**

### Added
- Streamer mode table: immediate 4×8 / 2×16 / 1×32 and multi-DAC capture configurations now enumerated (`X_IMM_4X8_*`, `X_IMM_2X16_*`, `X_IMM_1X32_4DAC8`, `X_*P_*DAC*_WFBYTE`)

### Changed
- Streamer NCO frequency: SETXFRQ word, video pixel-rate tables, and DDS/Goertzel synthesis use the `$8000_0000` (2³¹) system-clock multiplier
- Goertzel analysis: SINC1/SINC2 mode selected at D[23]; SINC2 small-amplitude (±10) operation documented

## [1.6.1] - 2026-06-02

**Index integrity verification**

### Added
- Published index: each entry carries a SHA-256 content hash, letting consumers verify fetched content matches the index

## [1.6.0] - 2026-06-02

**XBYTE dispatch-mode control via SETQ and SETQ2**

### Added
- XBYTE engine: SETQ arms the persistent dispatch mode; SETQ2 sets a one-shot mode for the next bytecode, then reverts — the mechanism for two-table bytecode VMs
- SETQ / SETQ2: XBYTE mode-control role documented alongside their block-transfer use

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