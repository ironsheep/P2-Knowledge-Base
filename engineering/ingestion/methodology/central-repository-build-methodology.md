# Central Repository Build Methodology

## Task Management Tag
**Todo MCP Tag**: `central_repo_build`

All tasks related to this central repository build effort should be tagged with `central_repo_build` in Todo MCP. This allows focused execution on repository-specific tasks without interference from other project work.

```bash
# Example task creation
mcp__todo-mcp__todo_create \
  content:"Extract PASM2 instructions from CSV" \
  tags:["central_repo_build"] \
  estimate_minutes:120

# Filter to only repository tasks
mcp__todo-mcp__todo_next tags:["central_repo_build"]

# List all repository tasks
mcp__todo-mcp__todo_list tags:["central_repo_build"]
```

## Purpose
Build a unified P2 knowledge repository aggregating all technical facts from authoritative sources for:
1. AI consumption via download-on-demand API
2. Document generation pipelines
3. Knowledge validation and updates

## Scope

### Languages
- **PASM2**: All 491 assembly instructions with encoding, timing, flags, examples
- **Spin2**: High-level language methods, operators, control structures, compiler directives

### P2 Architecture Components (Comprehensive List)

**Core Processing**:
- **8 Symmetric COGs**: Independent 32-bit processors, 5-stage pipeline
- **Instruction Set**: 491 PASM2 instructions with conditional execution
- **XBYTE Engine**: Hardware bytecode execution (8-clock cycle)
- **ALT Instructions**: Register indirection and instruction synthesis
- **REP/SKIP/EXECF**: Hardware looping and instruction skipping

**Memory Architecture**:
- **COG RAM**: 512 longs (2KB) per COG, dual-port
- **LUT RAM**: 512 longs (2KB) per COG, dual-port, COG-pair sharing
- **Hub RAM**: 512KB shared, "egg beater" round-robin access
- **FIFO System**: 19-stage buffer for hub execution
- **PTRx Expressions**: Complex addressing modes

**Smart Pin System**:
- **64 Smart Pins**: 32+ autonomous operating modes
- **Repository/DAC Modes**: Long repository, ADC sample, DAC output
- **Pulse/NCO Modes**: Pulse, transition, frequency, duty cycle
- **PWM Modes**: Triangle, sawtooth, switch PWM
- **Counting Modes**: Edge, high, period, state, ADC accumulator
- **Timing Modes**: State timing, high/low measurement, timeout
- **ADC Modes**: SINC1/SINC2/SINC3 filtering, 14-bit resolution
- **Serial Modes**: Async/sync serial, USB host/device, SPI, I²C

**Math & Signal Processing**:
- **CORDIC Solver**: 54-stage pipeline (MUL, DIV, SQRT, ROTATE, LOG, EXP)
- **Pixel Operations**: ADDPIX, MULPIX, BLNPIX, MIXPIX (7-clock)
- **Colorspace Converter**: 3×3 matrix transformation with modulation
- **DDS/Goertzel**: Signal generation and single-frequency analysis

**I/O & Communication**:
- **Streamer Engine**: NCO-timed DMA, automatic hub transfers
- **Digital Video**: Hardware TMDS encoding for DVI/HDMI
- **DAC System**: 4 channels per COG, 8-bit resolution
- **Event System**: 16 hardware event trackers per COG
- **Interrupt System**: 3 priority levels + debug interrupt
- **COG Attention**: Inter-COG signaling mechanism
- **Locks**: 16 hardware semaphores for synchronization

**System Infrastructure**:
- **Clock System**: PLL, crystal, RC oscillators, 6 clock modes
- **Hub Configuration**: HUBSET for system control
- **PRNG**: Xoroshiro128** with unique streams per COG/pin
- **Debug System**: Hardware debugging with hub RAM preservation
- **Boot System**: Serial, flash, SD card boot options
- **Checksum Validation**: Boot integrity verification

### Hardware Documentation

**Edge Modules (2 P2 boards)**:
- **Edge Standard Module** (#64000-ES): Standard P2 module
- **Edge 32MB Module** (#64000-32MB): Enhanced with 32MB PSRAM

**Development Boards (4 boards for module insertion)**:
- **P2 Eval Board** (#64000): Primary development platform
- **Edge Module Breadboard** (#64020): Breadboard adapter
- **Edge Breakout Board** (#64029): Full breakout board
- **Edge Mini Breakout** (#64019): Compact breakout

**Add-on Modules & Adapters**:
- **WX WiFi Module**: ESP8266 wireless connectivity
- **P2-WX Adapter**: WiFi adapter for Eval boards
- **PropPlug Rev E**: USB programming interface
- **Universal Motor Driver**: Motor control board
- **HUB75 Adapter**: LED panel interface

**P2 Eval Add-on Boards (8 individual boards)**:
- **LED Array Board** (#64006A): 8 LEDs with current limiting
- **Switch Array Board** (#64006B): 8 momentary push switches
- **Potentiometer Board** (#64006C): 8 10kΩ potentiometers
- **Servo Header Board** (#64006D): 8 3-pin servo connectors
- **Sensor Board** (#64006E): Temperature, light, sound sensors
- **Prototyping Board** (#64006F): Breadboard area
- **Digital I/O Board** (#64006G): LEDs + switches combo
- **Analog I/O Board** (#64006H): Potentiometers + analog sensors

## Authoritative Sources for First Pass

### PASM2 Instruction Hierarchy (Layer-by-Layer Enhancement)

**CRITICAL**: PASM2 instructions require aggregation from FOUR layers to be complete:

```
1. BASE LAYER (Foundation):
   p2-instructions-csv/
   └── P2 Instructions v35...csv              # Basic list, encoding, flags

2. ENHANCEMENT LAYER (Electrical/Timing):
   p2-datasheet/
   ├── p2-datasheet-narrative.txt            # Raw extraction
   ├── p2-datasheet-walkthrough-analysis.md  # Human+Claude deep analysis
   └── p2-datasheet-critical-insights.md     # Key findings

3. NARRATIVE LAYER (Behavior & Context):
   silicon-doc/                              # NOTE: Split into 5 PDFs due to size
   ├── P2 Documentation v35 - Part1of5.pdf   # Pages 1-24
   ├── P2 Documentation v35 - Part2of5.pdf   # Pages 25-48
   ├── P2 Documentation v35 - Part3of5.pdf   # Pages 49-72
   ├── P2 Documentation v35 - Part4of5.pdf   # Pages 73-96
   ├── P2 Documentation v35 - Part5of5.pdf   # Pages 97-121
   ├── silicon-doc-v35-facts-only.md         # Pure facts extraction
   ├── silicon-doc-v35-walkthrough-audit.md  # Human+Claude deep analysis
   ├── silicon-doc-v35-critical-findings.md  # Key discoveries
   ├── INSTRUCTION-TIMING-AND-ENCODING.md    # Timing details
   └── COG-RAM-REGISTER-MAP.md              # Register context

4. CLARIFICATION LAYER (Edge Cases):
   chip-gracey-clarifications/
   ├── chip-instruction-clarifications...md  # Edge cases, corrections
   └── chip-gracey-programming-patterns...md # Best practices
```

**Two-Tier Extraction Approach**:
- **Tier 1**: Raw ingestion/extraction (automated, facts-only)
- **Tier 2**: Walkthrough/audit (human+Claude analysis, meta-knowledge)

**Aggregation Rule**: Each PASM2 instruction MUST combine:
1. CSV base structure
2. Datasheet timing (raw + walkthrough insights)
3. Silicon Doc narrative (raw + walkthrough understanding)
4. Chip clarifications for edge cases

**Filter**: Exclude marketing analysis found in walkthroughs, keep technical insights only.

### Spin2 Language (Comprehensive Documentation with Deep Analysis)

```
spin2-v51/                                     # 🏆 100% trust - COMPLETE
├── P2 Spin2 Documentation v51-250425.pdf     # Original PDF
├── SPIN2-CODING-REFERENCE.md                 # Full language specification
├── spin2-conceptual-framework.md             # Language concepts
├── spin2-v51-complete-extraction-audit.md    # Extraction verification
├── spin2-language-comprehensive.md           # Deep language analysis
├── spin2-pasm-integration-deep-dive.md       # PASM integration details
├── debug-comprehensive-guide.md              # DEBUG system analysis
└── terminal-window-completeness-audit.md     # Terminal features audit
```

**Two-Tier Knowledge**:
- **Raw Extraction**: Complete language reference, methods, operators
- **Deep Analysis**: Conceptual understanding, PASM integration, DEBUG system

**Note**: Spin2 documentation is self-contained but benefits from walkthrough insights for advanced features.

### Hardware Documentation Sources

#### 🏆 Edge Modules - P2 Boards (AUTHORITATIVE)
```
├── edge-standard-module/                     # 🏆 100% trust - #64000-ES
└── edge-32mb-module/                         # 🏆 100% trust - #64000-32MB
```

#### 🏆 Development Boards for Modules (AUTHORITATIVE)
```
├── p2-eval-board/                            # 🏆 100% trust - #64000
├── edge-module-breadboard/                   # 🏆 100% trust - #64020
├── edge-breakout-board/                      # 🏆 100% trust - #64029
└── edge-mini-breakout/                       # 🏆 100% trust - #64019
```

#### 🏆 Add-On Modules & Adapters (AUTHORITATIVE)
```
├── parallax-wx-wifi/                         # 🏆 100% trust - WiFi Module
├── p2-wx-adapter/                            # 🏆 100% trust - WiFi Adapter  
├── propplug-rev-e/                           # 🏆 100% trust - Programmer
├── universal-motor-driver/                   # 🏆 100% trust - Motor control
└── p2-eval-add-on-boards/                    # 🏆 100% trust - 8 I/O boards
    ├── #64006A - LED Array Board
    ├── #64006B - Switch Array Board
    ├── #64006C - Potentiometer Board
    ├── #64006D - Servo Header Board
    ├── #64006E - Sensor Board
    ├── #64006F - Prototyping Board
    ├── #64006G - Digital I/O Board
    └── #64006H - Analog I/O Board
```

### Analysis & Synthesis Documents
```
/engineering/ingestion/central-analysis/
├── P2-COMPLETE-INSTRUCTION-MATRIX.json       # Pre-aggregated instructions
├── P2-UNIFIED-AUTHORITATIVE-DESCRIPTION.md   # Architecture overview
└── SMART-PINS-SOURCE-COMPARISON.md          # Smart pin modes validated
```

## Repository Structure

### Output Location
```bash
/engineering/knowledge-base/P2/         # Central repository location
├── manifest.yaml                      # Global index with timestamps
├── instructions/
│   ├── pasm2/
│   │   ├── ADD.yaml                  # Aggregated from 4 layers
│   │   ├── ADDX.yaml
│   │   └── ...                       # 491 files total
│   └── spin2/
│       ├── methods/
│       │   ├── HUBSET.yaml
│       │   └── ...
│       ├── operators/
│       │   ├── addition.yaml
│       │   └── ...
│       └── control/
│           ├── IF.yaml
│           └── ...
├── architecture/
│   ├── cogs/
│   │   ├── overview.yaml
│   │   ├── pipeline.yaml
│   │   └── registers.yaml
│   ├── memory/
│   │   ├── cog-ram.yaml
│   │   ├── lut-ram.yaml
│   │   └── hub-ram.yaml
│   ├── smart-pins/
│   │   ├── overview.yaml
│   │   ├── modes/
│   │   │   ├── uart-tx.yaml
│   │   │   └── ...                  # 32+ mode files
│   │   └── configuration.yaml
│   ├── cordic/
│   │   ├── overview.yaml
│   │   └── operations.yaml
│   └── system/
│       ├── locks.yaml
│       ├── events.yaml
│       └── clocking.yaml
├── hardware/
│   ├── boards/
│   │   ├── p2-eval.yaml
│   │   ├── edge-standard.yaml
│   │   └── ...                      # 6 boards total
│   └── addons/
│       ├── wx-wifi.yaml
│       ├── p2-wx-adapter.yaml
│       ├── led-array-board.yaml     # #64006A
│       └── ...                      # 13+ addon modules
└── metadata/
    ├── sources.yaml                   # Source document registry
    ├── trust-levels.yaml              # Trust calculations
    └── update-log.yaml                # Change history
```

## Execution Plan

**Approach**: Rapid execution in 2.5-3 hour sessions, committing work at each session end.

### Session-Based Task Breakdown

**All tasks tagged with: `central_repo_build`**

#### Phase 1: Component Discovery & Setup
- [ ] Scan Silicon Doc + Datasheet for complete P2 component list
- [ ] Extract text from all 5 Silicon Doc PDFs (ensure narrative completeness)
- [ ] Verify all analysis documents are committed to Git
- [ ] Create repository directory structure at `/engineering/knowledge-base/P2/`
- [ ] Design and document rich YAML schema

#### Phase 2: Build Extraction Pipeline
- [ ] Create CSV instruction parser
- [ ] Create datasheet extractor (raw + walkthrough integration)
- [ ] Create silicon doc aggregator (facts + walkthrough + critical findings)
- [ ] Create Spin2 comprehensive extractor
- [ ] Create hardware documentation extractor
- [ ] Create marketing filter function

#### Phase 3: Extract & Aggregate
- [ ] Extract all 491 PASM2 instructions from CSV (Layer 1)
- [ ] Add datasheet timing/electrical specs (Layer 2)
- [ ] Add silicon doc narratives - INCLUDING rich descriptions (Layer 3)
- [ ] Add Chip Gracey clarifications (Layer 4)
- [ ] Extract complete Spin2 documentation
- [ ] Extract hardware board specifications
- [ ] Extract addon module documentation

#### Phase 4: Process & Output
- [ ] Aggregate all layers for each instruction
- [ ] Calculate completeness scores (two-tier)
- [ ] Run conflict detection
- [ ] Generate YAML files for all entities
- [ ] Create manifest.yaml
- [ ] Create metadata tracking files

#### Phase 5: Quality & Documentation
- [ ] Run comprehensive quality audit
- [ ] Generate audit reports
- [ ] Document gaps and conflicts
- [ ] Create initial tracking history
- [ ] Commit everything to Git with proper tags
- [ ] Document v1.0 baseline quality score

### Session Management
- **At session start**: Load context, check Git status, review progress
- [ ] Create context checkpoint before session end
- [ ] Commit all work with descriptive message
- [ ] Document next session starting point

### Critical Requirements
- **Rich descriptions from Silicon Doc MUST be captured**
- **All sources must be Git-committed before use**
- **Filter all marketing comparisons**
- **Track source attribution for every fact**

## Key Design Decisions

### Why 4-Layer Aggregation for PASM2?
- CSV alone is insufficient (basic structure only)
- Datasheet adds critical timing/electrical specs
- Silicon Doc provides essential narrative/context
- Chip clarifications resolve ambiguities
- Together they form complete understanding

### Why Single Source for Spin2?
- Spin2 v51 documentation is comprehensive
- Self-contained with all needed information
- No conflicting sources to reconcile

### Why Track Layers?
- Shows completeness of knowledge
- Identifies gaps needing attention
- Enables targeted updates
- Documents confidence level

## Notes
- **PASM2 requires 4-layer aggregation** - CSV → Datasheet → Silicon Doc → Clarifications
- **Spin2 is self-contained** - Use v51 documentation as-is
- **Track layer completeness** for each instruction
- **Filter marketing content** - Technical facts only
- **Repository location**: `/engineering/knowledge-base/P2/`
- **Git tracks all changes** - Enables incremental updates
- **Run audits after every update** - Track quality improvements
- **Use tag `central_repo_build`** for all Todo MCP tasks related to this effort