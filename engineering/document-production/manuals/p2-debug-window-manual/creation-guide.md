# P2 Debug Window Manual - Creation Guide

**Canonical Name:** `p2-debug-window-manual`

## 🎯 Document Purpose
The complete practical reference for the P2 DEBUG window system: the nine built-in
display windows, their commands and parameters, and how to use them while developing.

### Document Philosophy

> **Voice note.** This guide is written in the register it asks authors to write in —
> Authoritative + Comprehensive + Practical, per `voice-guide.md`. It previously opened
> in the superseded "Discovery Guide" voice while its own §Voice section forbade that
> voice, which taught the banned register by example. An author absorbs register by
> reading a guide, not by reading its rules.

- **Document all nine window types completely** — every command and parameter, not the
  subset the Spin2 documentation illustrates.
- **Document parameter combinations**, which are where the windows' real behavior lives
  and where the source material is thinnest.
- **Pair every code example with a screenshot** of what it actually produces.
- **Close the gap between basic and complete use** — the syntax most developers already
  know covers a small part of what the windows do.

### Core Problem This Manual Solves

The DEBUG statement most developers use is a small entry point to a much larger system.
Undocumented or thinly documented from the reader's side:

- nine specialized window types, each with its own parameter set
- PASM-level debugging
- multi-window coordination
- parameter interactions that change what a window displays

**The approach:** document each window from its theory of operations, and show visual
proof of every technique rather than describing it.

## 🚫 No Handwaving Principle

### Fundamental Documentation Rule

**Technical documentation must be based on verified sources, not assumptions about what "should" exist.**

This principle is MANDATORY for all P2 documentation to prevent the creation of plausible but non-existent features.

### Examples of Handwaving (FORBIDDEN)

❌ **Assuming features because similar systems have them:**
- "The LOGIC window probably has protocol decoders like professional logic analyzers"
- "There must be automatic measurements since all scopes have them"
- "Resource limits should be around 16 windows like typical systems"

❌ **Filling gaps with plausible speculation:**
- "Maximum terminal size is likely 80x50 based on USB bandwidth"
- "Each instance uses approximately 16 bytes of P2 RAM"
- "Update rates of 10-20Hz are optimal for performance"

❌ **Stating assumptions as facts:**
- "The system supports up to 16 simultaneous windows"
- "Protocol decoders automatically identify I2C, SPI, and UART"
- "Automatic measurements include Vpp, frequency, and rise time"

### Proper Documentation (REQUIRED)

✅ **Citing sources:**
- "According to Spin2 v5.1 reference, DEBUG supports 9 window types"
- "Pascal source code examination reveals hover coordinate display"
- "Testing confirms TRACE modes range from 0-15"

✅ **Marking unknowns as unknown:**
- "Resource limits are not documented in available sources"
- "Maximum window count is application-specific, not system-defined"
- "Protocol decoding capabilities not found in documentation"

✅ **Documenting only verified features:**
- "LOGIC window displays digital signals (no automatic decoding found)"
- "Mouse hover shows coordinates (discovered in Pascal source)"
- "SPRITE commands use first 8 of 16 TRACE modes (tested)"

### Why This Matters

Handwaving has caused significant documentation errors:
- Protocol decoder speculation misled users about LOGIC capabilities
- Automatic measurement assumptions created false expectations
- Resource limit guesses provided incorrect constraints
- Hover behavior speculation added non-existent GUI features

### Implementation Checklist

Before documenting ANY feature:
1. ☐ Is this explicitly stated in official documentation?
2. ☐ Has this been verified through testing?
3. ☐ Is the source clearly cited?
4. ☐ Are assumptions clearly marked as speculation?
5. ☐ Are gaps acknowledged rather than filled?

**REMEMBER**: It's better to document a gap than to fill it with plausible fiction. Users need accurate information about what DOES exist, not speculation about what MIGHT exist.

### Formal Claim Verification Protocol

**Added:** 2026-01-23
**Derived from:** PASM2 Manual Content Verification Sprint findings

This section formalizes the No Handwaving Principle into a systematic verification process.

#### Claim Types and Required Sources for Debug Windows

| Claim Type | Required Source | Example Claim |
|------------|-----------------|---------------|
| **Window type capability** | Spin2 v5.1 docs + Phase 1 studies | "LOGIC window displays 8 channels" |
| **Command syntax** | Spin2 v5.1 docs | "DEBUG(\`window BITMAP SIZE 100 100)" |
| **Parameter values** | Testing + documentation | "TRACE modes range 0-15" |
| **Visual behavior** | Screenshot verification | "Grid overlay appears when..." |
| **Performance claims** | Tested benchmarks, **quoted with their conditions** | "Full-window redraw measured at *N* ms on *host/version*; layer updates at *M* ms for the same frame" — a bare multiplier ("20× faster") is not a sourced claim, it is the marketing `voice-guide.md` §3.2 forbids |
| **PC integration** | Pascal source + testing | "Mouse coordinates reported via..." |
| **Capability limits** | Testing ONLY | "Maximum simultaneous windows is..." |

#### Red-Flag Phrases for Debug Documentation

| Phrase | Risk Level | Why Suspicious | Debug-Specific Concern |
|--------|------------|----------------|------------------------|
| "like professional tools" | **CRITICAL** | Comparing to unverified capabilities | Logic analyzers have protocol decoders; DEBUG may not |
| "automatically detects" | **CRITICAL** | Auto-detection is complex | DEBUG is display-focused, not analysis-focused |
| "maximum of N" | **HIGH** | Limits must be tested | Resource limits vary by application |
| "approximately" | MEDIUM | Vague numbers suggest guessing | Get exact values from testing |
| "internally" | MEDIUM | Internal behavior needs source | Check Pascal source or P2 Documentation v35 |
| "supports" (vague) | MEDIUM | What exactly is supported? | List specific capabilities |

#### The Verification Protocol for Debug Content

```
┌─────────────────────────────────────────────────────────────────┐
│ DEBUG WINDOW CLAIM VERIFICATION CHECKLIST                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. What am I claiming? (capability/syntax/parameter/visual)     │
│                                                                 │
│ 2. Which source should contain this?                            │
│ □ Spin2 v5.1 Reference: command syntax, parameters              │
│ □ Phase 1 Studies: discovered capabilities, patterns            │
│ □ Pascal Source: internal behavior, PC integration              │
│ □ Direct Testing: visual behavior, limits, performance          │
│                                                                 │
│ 3. Can I prove this claim?                                      │
│ □ Screenshot showing the behavior                               │
│ □ Code example that demonstrates it                             │
│ □ Documentation citation                                        │
│                                                                 │
│ 4. Am I speculating from similar systems?                       │
│ □ If YES → DON'T WRITE IT                                       │
│ □ Mark as "not found" if feature doesn't exist                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Prevention Example: Protocol Decoder Fabrication

**The fabricated claim**: "LOGIC window includes protocol decoders for I2C, SPI, and UART"

**Applying the protocol**:
1. Claim type: Capability claim
2. Required source: Spin2 v5.1 LOGIC section + Phase 1 LOGIC study
3. Check Spin2 docs: Lists display parameters, no protocol mention
4. Check Phase 1 study: Documents multi-signal display, no decoding found
5. Check Pascal source: Display rendering, no protocol analysis code
6. Result: **CLAIM BLOCKED** - Feature was assumed because "logic analyzers have this"

**Correct documentation**: "LOGIC window displays digital signal transitions. Protocol analysis requires separate software tools or manual interpretation."

#### Full Audit Methodology Reference

For comprehensive post-write audit procedures, see:
`engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`

## 📚 Content Sources & Production Method

### Primary Content Sources

#### 0. Per-Window Theory of Operations — authoritative grounding source ("the Bible")
**Location**: `./REF/theory-of-operations/` (this manual's folder)
- Nine source-derived theory-of-operations documents, one per window type: TERM,
 BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, MIDI. **Current as of PNut v55.**
- Cover data structures, configuration, update/rendering, command protocols, color
 systems, and performance — derived from the PNut implementation.
- **This is the primary grounding source for the periodic audit** (Dimensions A, B,
 #1, #5, C). Where a manual claim conflicts with the relevant window's theory-of-
 operations, the theory-of-operations wins.

#### 1. SPIN-2 Language Reference Manual v5.1 (Primary Technical Foundation)
**Location**: `engineering/ingestion/sources/spin2-v51/` (relocated 2025-09; the former
`/sources/extractions/spin2-v51-complete-extraction-audit/` path is dead). Key DEBUG
files: `debug-displays-complete-catalog.md`, `debug-section.txt`,
`debug-comprehensive-guide.md`, `spin2-terminal-windows.md`, and the source PDF
`P2 Spin2 Documentation v51-250425.pdf`.
- Complete DEBUG instruction specifications
- Debug formatting options and syntax
- Built-in debug methods and functions
- Terminal output control and formatting
- Debug system architecture and capabilities
- Performance characteristics of debug operations

#### 2. Phase 1 Comprehensive Window Studies
**Location**: `engineering/document-production/manuals/p2-debug-window-manual/studies/`
- **12 study documents** covering all 9 window types
- **The layer system** — sprite-based partial updates. *(The studies record a large
  redraw-cost reduction. Any figure carried into the manual must come with its
  measurement conditions — see the performance-claim row in the verification protocol
  above; an unconditioned multiplier is the marketing this manual's voice guide forbids.)*
- **PC input integration** — the host reports keyboard and mouse back to the P2
- **The CROP command** — selective region updates
- **45 YAML knowledge gaps**, documented and prioritized
- **Multi-window coordination patterns**
- **Complete syntax reference** — unified command reference from all studies

#### 3. OBEX and Source Code Projects (Real-World Implementation Patterns)
**Location**: Various ingested project sources throughout P2 knowledge base
- Working debug implementations in real applications
- Common debug patterns and techniques
- Best practices discovered across projects
- Integration examples with different system types
- Proven debugging workflows from production code
- Performance monitoring in actual applications

#### 4. Community Examples (Supplementary Usage Patterns)
**Location**: Forum posts, tutorials, community code
- Additional debugging scenarios
- Alternative approaches and techniques
- Troubleshooting patterns from field experience
- Specialized debug applications

### Production Method

#### Phase 1: Systematic Discovery ✅ COMPLETED
1. **Cataloged all 9 debug window types** - TERM, BITMAP, PLOT, LOGIC, SCOPE, SCOPE_XY, FFT, SPECTRO, MIDI
2. **Extracted SPIN-2 v5.1 minimal examples** as baseline reference points
3. **Parameter matrix exploration** - Discovered layer patterns, CROP commands, layer system
4. **Pattern extraction from source code** - sprite-based partial-update patterns found,
   with a large measured redraw-cost reduction (carry the figure only with its conditions)
5. **Developed complementary examples** - Software-only demonstrations for accessibility
6. **PASM debugging integration** - Assembly-level debug capabilities documented
7. **Created 12 comprehensive study documents** - ~400KB of discoveries and analysis
8. **Verified documented features** - SPRITEDEF/SPRITE for PLOT, 16 TRACE modes (0-15)

#### Phase 2: Manual Generation (CURRENT PHASE)
1. **Generate chapters using Opus 4.1** - Leveraging Phase 1 discoveries
2. **Create 50+ working examples** - All pnut-ts validated
3. **Document layer patterns** - Layer system, CROP commands
4. **Document PLOT sprites** - SPRITEDEF/SPRITE commands with 0-255 IDs, 1-32 pixel dimensions
5. **Include PC input integration** - Mouse and keyboard debug control
6. **Build professional workflows** - Multi-window coordination patterns
7. **Document only verified features** - No speculation about undocumented capabilities

#### Phase 3: Quality Validation
1. **Test all examples** with pnut-ts compiler
2. **Verify debug outputs** match discovered behaviors
3. **Validate layer techniques** for performance claims
4. **Check cross-references** to Phase 1 studies
5. **Ensure minimal hardware philosophy** throughout

## 🧗 Technical Climbing Methodology Applied

This document follows the project-wide Technical Climbing Methodology, contributing to all four P2KB facets:

1. **Rich Trusted Source** - Each iteration incorporates validated P2 debug information
2. **Download-on-Demand** - Optimized for developers needing debug capabilities
3. **Human Documentation** - Clear debugging workflows for learning
4. **AI-Ingestible Format** - Structure supports automated debugging assistance

---

# PART 1: CONTENT CREATION (What Authors Write)

## 📝 Content Philosophy

### Voice

**The authoritative voice for this manual is defined in `voice-guide.md`** (adopted
2026-05-31): **Authoritative + Comprehensive + Practical**, second person, with **no
marketing or celebration**. It is modeled on the P2 I/O & Smart Pins User Guide voice.
Author all content per that guide; its §3 (rules), §4 (debug-domain content rules), and
§5 (terminology) govern.

> **Superseded:** the earlier "Discovery Guide" voice — exploratory excitement,
> "Look at that!", superlatives, and the "Debug Iceberg" framing — is **out of the house
> standard** and must not be used. Every house voice guide forbids marketing/celebration.
> Where older drafts use it, bring them into conformance with `voice-guide.md`.

### Progressive Debug Learning Structure

**Implementation Pattern:**
1. **Problem**: Start with a debugging challenge
 - *Template*: "Your LEDs aren't blinking correctly..."

2. **Debug Tool**: Introduce the specific debug capability
 - *Template*: "The DEBUG instruction lets us monitor..."

3. **Apply**: Show the debug tool solving the problem
 - *Template*: "Adding DEBUG statements reveals..."

4. **Interpret**: Explain what the debug output means
 - *Template*: "The pattern shows that..."

5. **Solve**: Use debug insights to fix the issue
 - *Template*: "Adjusting the timing resolves..."

## 📚 Content Requirements

### Document Scope Boundaries

#### What This Manual Covers
- **DEBUG Instructions**: Complete debug instruction set usage
- **Debug Window Operation**: Terminal display, formatting, controls
- **Visualization Techniques**: Graphical debug outputs, plots, scopes
- **Performance Monitoring**: Timing analysis, resource usage
- **System State Display**: Register contents, memory, flags
- **Multi-cog Debugging**: Coordinated debugging across cogs
- **PASM Assembly Debugging**: Debug capabilities within assembly language code
- **Debug Workflows**: Systematic debugging methodologies
- **Integration Patterns**: Debug with other development tools

#### What This Manual References (Not Covers)
- **Basic P2 Programming** → "See PASM2 Manual for instruction details"
- **Smart Pin Operation** → "See the P2 I/O & Smart Pins User Guide for pin debugging"
- **Hardware Setup** → "See Hardware Manual for physical connections"
- **Advanced Applications** → "See specific application guides"

#### Cross-Reference Pattern
When encountering out-of-scope topics:
```markdown
## Debugging Smart Pin Timing
Here's how to monitor Smart Pin state changes:
[debug example]

📚 **For Smart Pin Configuration**: See the P2 I/O & Smart Pins User Guide
(Smart Pin Configuration) for proper Smart Pin setup and operation details.
```

### Chapter Structure Template

```markdown
# Chapter N: Descriptive Title

*Brief explanation of the debugging challenge this chapter solves*

## The Problem: Real Debugging Scenario
[Start with actual debugging situation developers face]
"Your serial communication is dropping characters..."

## Debug Strategy
[Introduce the debugging approach for this scenario]
"To solve this, we'll monitor the timing and data flow..."

## Debug Tools for This Challenge
[Present the specific P2 debug capabilities that apply]
Show debug instruction usage with immediate results

## Interpreting the Output
[Explain what the debug information tells us]
Connect debug display to actual program behavior

## Common Patterns
[Show typical debug outputs for this scenario]
Help readers recognize similar situations

## Your Turn: Debug Challenge
[Hands-on exercise with broken code to debug]
Provide code with issues for reader to identify and fix

## Advanced Techniques
[Further techniques for this scenario — multi-window coordination, PASM-level
debugging, parameter combinations beyond the common case]

## Summary: Debug Checklist
[Quick reference for this type of debugging]
Step-by-step process for similar future issues

---
```

### Special Content Sections

#### Debug Output Examples
```markdown
:::debug-output
```
DEBUG: COG0 Counter = 1247, Status = %00001010
DEBUG: COG1 Counter = 1249, Status = %00001011
DEBUG: Timing delta = 2 clocks
```
:::
```

#### Debug Workflow Boxes
```markdown
:::workflow
**Debug Workflow: Serial Communication Issues**

1. Add timing markers at key points
2. Monitor data buffers before/after transmission
3. Check for timing conflicts between cogs
4. Verify protocol timing requirements
5. Compare expected vs. actual data patterns
:::
```

#### Common Debug Patterns
```markdown
:::pattern
**Pattern**: Intermittent Timing Issues
**Symptoms**: Occasional failures, works most of the time
**Debug Approach**: Continuous monitoring with statistics
**Key Indicators**: Timing variation, resource conflicts
:::
```

#### Debug Tips
```markdown
:::debug-tip
💡 **Pro Tip**: Use different debug channels for different cogs to avoid output conflicts.
:::
```

## 🔧 **CRITICAL: Minimal Hardware Design Philosophy**

### Universal Accessibility Requirement

**Core Principle**: Examples must be accessible to beginners with minimal external hardware requirements. Focus on simple-to-generate projects that demonstrate rich visualization techniques without specialized equipment.

### Hardware Accessibility Levels

**Level 0: Software-Only Examples** (Preferred)
- **Built-in P2 resources only**: 2 LEDs, CORDIC engine, multiple cogs, RNG, internal timers
- **Mathematical demonstrations**: Waveform generation, signal processing, algorithm visualization
- **Software simulation**: Protocol patterns, sensor networks, control systems
- **Learning focus**: Debug techniques and visualization concepts

**Level 1: Built-in Hardware Only**
- **P2 board resources**: LED1, LED2 for binary visualization
- **Simple demonstrations**: PWM visualization, binary patterns, state indication
- **Interactive examples**: PC mouse/keyboard control of LED patterns

**Level 2: Minimal External Components** (Optional)
- **Single wire connections**: Simple switches, basic sensors
- **Clear documentation**: Exact wiring diagrams and component specifications
- **Alternative provided**: Software simulation version always included

**Level 3: Advanced Projects** (Reference Only)
- **Complex hardware setups**: For experienced developers who want to extend
- **Professional applications**: Real-world integration examples
- **Not required for learning**: Core concepts taught in Levels 0-1

### Software Simulation Strategy

**Rich Scenarios from Simple Sources**:
```spin2
' Motor control analysis - no motor required!
PRI simulate_motor_system
 repeat
 ' Software-generated encoder feedback
 encoder_pos := (encoder_pos + pwm_duty/100) & $FFFF
 ' Simulated load variation
 load_torque := GETRND & $FF
 ' Debug with multiple windows
 DEBUG(`motor_scope SCOPE_XY `(pwm_duty) `(encoder_pos))
```

**Educational Benefits**:
- ✅ **Immediate accessibility**: Copy, paste, run - see results instantly
- ✅ **Concept focus**: Visualization techniques, not hardware debugging
- ✅ **Rapid experimentation**: Try variations without rewiring
- ✅ **Universal applicability**: Anyone with P2 board can follow along
- ✅ **Professional transfer**: Simulation skills apply to real projects

### Implementation Guidelines

**Every example must include**:
1. **Software-only version** demonstrating the core debug concept
2. **Clear learning objective** focusing on debug visualization technique
3. **Immediate executability** with just P2 board + PC connection
4. **Progressive complexity** within each accessibility level
5. **Hardware extension notes** showing how to apply to real sensors (optional)

**Avoid**:
- ❌ **Complex external hardware** requirements
- ❌ **Specialized test equipment** dependencies
- ❌ **Expensive sensors or components**
- ❌ **Complex wiring** that distracts from debug learning
- ❌ **Platform-specific tools** or development environments

## 📖 Code Example Design Principles

### The "Debug-Driven" Pattern

**Show the problem FIRST, then the debug solution:**
```pasm2
' PROBLEM: LED blinks too fast
 drvh #56
 waitx #1000 ' Intended 1ms delay
 drvl #56
 waitx #1000
 jmp #$-4

' DEBUG SOLUTION: Monitor actual timing
 drvh #56
 debug "LED ON at ", udec_(getct)
 waitx #1000
 drvl #56
 debug "LED OFF at ", udec_(getct)
 waitx #1000
 jmp #$-8
```

### The "Before and After" Pattern

**Show program behavior without debug, then with debug:**
```markdown
**Without Debug**: Program runs but doesn't work correctly
**With Debug**: Clear visibility into what's actually happening
**Result**: Quick identification and resolution of the issue
```

### Code Example Naming Convention

**Format**: `' Debug Example - [Scenario] - [Technique]`

**Examples:**
- `' Debug Example - Serial Dropouts - Buffer Monitoring`
- `' Debug Example - cog Timing - Synchronization Check`
- `' Debug Example - Memory Issues - Address Validation`
- `' Debug Example - Interrupt Problems - State Logging`

## 💊 The Debug Medicine Cabinet Pattern

### Types of Debug Medicine

**Type 1: Quick Debug Check**
```markdown
Overwhelmed by complex debug output?
Medicine: Start with simple DEBUG statements showing just one variable
```

**Type 2: Visual Debug Alternative**
```markdown
Hard to interpret numerical debug output?
Medicine: Use LED patterns or terminal graphics for visual feedback
```

**Type 3: Systematic Debug Process**
```markdown
Don't know where to start debugging?
Medicine: Follow the "Half-Split" method - eliminate half the code as source
```

## 🚫 Content DON'Ts

### NEVER Include Style Information
❌ "This debug output should be in a monospace box"
❌ "Make the debug tip yellow"
❌ "Use red text for error messages"
✅ Just show the debug content - template handles appearance

### NEVER Use Platform-Specific Debug Tools
❌ References to specific terminal programs
❌ Assume particular development environment
❌ Platform-specific debug utilities
✅ Focus on P2 built-in debug capabilities

### NEVER Assume Debug Hardware
❌ "Connect your logic analyzer..."
❌ "Using an oscilloscope, measure..."
❌ "Set up your JTAG debugger..."
✅ Use P2's built-in debug system exclusively

---

# PART 2: STYLE IMPLEMENTATION (What Template Does)

## 🎨 Visual Style Rules (AUTOMATIC)

### Color Scheme
- **Green**: Debug output displays (monospace background)
- **Blue**: Debug workflow boxes
- **Orange**: Debug tip highlights
- **Yellow**: Code examples with debug additions
- **Gray**: Pattern identification boxes
- **Purple**: Advanced technique sections

### Box Styles (AUTOMATIC)
| Box Type | Background | Border | Usage |
|----------|------------|--------|-------|
| `:::debug-output` | Light green | Monospace | Actual debug terminal output |
| `:::workflow` | Light blue | Solid | Step-by-step debug processes |
| `:::pattern` | Light gray | Dashed | Common debug patterns |
| `:::debug-tip` | Light orange | None | Professional debugging tips |
| `:::advanced` | Light purple | Thick | Advanced debugging techniques |

---

# PART 3: DOCUMENT STRUCTURE

## 📖 Chapter Outline (current — window-reference structure)

The manual is a per-window reference in four parts. Each window chapter follows the
template in `voice-guide.md` §2.2 (what it shows → config command + all parameters →
data commands → control commands → one compilable example → when-to-use/considerations).

### Part I — Foundation
1. **The DEBUG Display Windows** — the shared create-by-name/feed-by-name model, the nine
 windows, the values-vs-command-codes rule, the boundary with the single-step debugger.
2. **Getting Started** — tooling (`pnut-ts -d`, `pnut-term-ts`), your first window, the
 no-hardware philosophy, optional DEBUG configuration symbols.

### Part II — The Windows (one chapter each, simplest to richest)
3. **TERM** · 4. **BITMAP** · 5. **PLOT** · 6. **LOGIC** · 7. **SCOPE** · 8. **SCOPE_XY** ·
9. **FFT** · 10. **SPECTRO** · 11. **MIDI**.

### Part III — Integration
12. **Bidirectional Control** (`PC_KEY` / `PC_MOUSE`) · 13. **Packed Data** (compact
high-rate transfers) · 14. **Multiple Windows and PASM Debugging**.

### Part IV — Appendices
A: Command Reference · B: Packed-Data Format Reference · C: Color and Coordinate Reference.

> Source of truth for each window is its `REF/theory-of-operations/<WINDOW>_Theory_of_Operations.md`
> (**PNut v55**). The legacy narrative outline (vision-gap / layer-composition / professional-
> instruments / production-workflows) is **superseded**; valuable patterns from it are tracked
> in `SALVAGE-CANDIDATES.md` for clean-room re-authoring into the window chapters above.

## 📏 Size Guidelines
**As shipped (v1.1.2, 2026-08-08): 168 pages, 15 chapters + 3 appendices.** These are the
verified figures from the render and the publication roster, not a target. The original
targets (200–250 pages, 16 chapters) were never met and are not goals to restore — the
manual covers all nine windows in the pages it has.

- **Chapter size**: 10–15 pages each
- **Example density**: 2-3 working examples per chapter
- **Practical focus**: 70% examples, 30% explanation

---

# PART 4: PRODUCTION SPECIFICATIONS

## 🔧 Technical Requirements

### Code Validation
- **MUST compile with pnut-ts** without errors or warnings
- **MUST produce actual debug output** when run
- **MUST be complete programs** (not code fragments)
- **MUST use consistent debug formatting** throughout manual
- **MUST capture window screenshots** using P2's built-in bitmap save capability
- **MUST include visual verification** - code example + actual screenshot output

### Debug Output Standards
```pasm2
' GOOD: Consistent debug formatting
 debug "Timer: ", udec_(timer_value), " Status: ", uhex_(status)

' GOOD: Clear debug labels
 debug "cog", udec_(cogid), ": Starting main loop"

' BAD: Unclear debug output
 debug udec_(x) ' What is x? When does this print?
```

### Example Verification Process
1. **Compile** all examples with latest pnut-ts
2. **Run** examples on P2 hardware or P2 emulator
3. **Capture debug window screenshots** using P2's built-in bitmap save
4. **Include screenshot alongside code** for visual verification
5. **Verify** debug output matches explanation in text
6. **Test** debug techniques solve stated problems
7. **Document screenshot capture process** for reproducibility

---

# PART 5: QUALITY CHECKLIST

## ✅ Content Quality
- [ ] Each chapter solves a real debugging problem
- [ ] Debug techniques are immediately practical
- [ ] Examples produce verifiable debug output
- [ ] Workflows are systematic and repeatable
- [ ] Cross-references to other manuals are accurate

## ✅ Technical Quality
- [ ] All debug code compiles and runs correctly
- [ ] Debug output examples match actual P2 output
- [ ] Every code example has corresponding screenshot
- [ ] Screenshot capture process is documented and reproducible
- [ ] Debug techniques don't interfere with program function
- [ ] Performance impact of debug code is documented
- [ ] Debug approaches work across different P2 applications
- [ ] Visual verification validates all claims about window behavior

## ✅ Practical Quality
- [ ] Debug scenarios reflect real development challenges
- [ ] Solutions are efficient and professional
- [ ] Troubleshooting guides prevent common mistakes
- [ ] Advanced techniques provide genuine debugging power
- [ ] Manual serves as daily-use debug reference

---

# PART 6: SUCCESS METRICS

## Quantitative Goals
- **Every example compiles**, and every example file is byte-identical to its code
  block in the manual *(met: 34 programs, all verified on real silicon as of v1.1.1)*
- **All nine window types documented completely** — every command and parameter
- A worked, screenshot-backed example for each window
- *(As shipped: 168 pages, 15 chapters + 3 appendices. Recorded, not targeted.)*

## Qualitative Goals
- **Every claim traceable** to the Spin2 documentation, a per-window theory of
  operations, a study, or a test — the No Handwaving Principle above is the standard
- **Complete rather than selective** — all options documented, not the impressive ones
- **Usable as a reference** — a reader who knows which window they need can find the
  parameter they need without reading the chapter

---

# APPENDIX: P2 Debug System Overview

## Key Debug Capabilities to Document
- DEBUG instruction variants and formatting
- Terminal window interaction and display
- Debug performance monitoring
- Multi-cog debug coordination
- Visual debug output (plots, scopes)
- Debug integration with development workflow
- Advanced debug techniques for complex systems

## Source Material Integration
- Official P2 debug documentation
- Community debug examples and patterns
- Proven debug workflows from other projects
- Advanced debug techniques from expert developers

---

## Code Line Budget

Code boxes do **not** wrap — a typeset wrap can't break a comment and re-indent it,
nor add a language line-continuation, so over-long code lines are an authorship
defect to fix in source, not a template concern. The `prepare-manual` line-length
audit (`engineering/tools/validation/audit-code-line-length.py`) flags any source
code line wider than the budget below.

- **Max code columns (K): 76**
- **Code-box style / font:** the shared platform code-box family (`p2kb-platform-content.sty`
 — ```` ```spin2 ```` / ```` ```pasm2 ```` colored boxes), Latin Modern Mono at the box's
 code size with the `numbers=left` gutter. Debug Window is a **twin** that, as of the
 2026-06-07 platform-stack migration, consumes the platform code-box stack unchanged
 (identical page margins `left/right=1in`, `IOSPBlock left=30pt,right=10pt`, same code
 `Verbatim`), so it **inherits the platform reference K = 76** rather than measuring its own.
- **Provenance:** K calibrated on the layout-torture-test instrument's case-2.2 column ruler
 (see `manuals/p2-layout-torture-test/creation-guide.md` → Code Line Budget) and shared by
 every twin on the platform stack.

---

## Version Control

- **Version**: 2.0 (Post-Phase 1 Update)
- **Date**: 2025-09-14
- **Status**: Phase 2 Manual Generation Ready
- **Phase 1**: ✅ COMPLETED - 12 comprehensive window studies
- **Phase 2**: 🚧 IN PROGRESS - Opus 4.1 manual generation
- **Major findings**: the layer system (sprite-based partial updates), PC input
  integration, CROP commands
- **Next Step**: Generate chapters 1-14 using Opus 4.1

> **Historical record — this status block describes 2025-09-14, not today.** The manual
> shipped v1.0.0 on 2026-06-16 and is at **v1.1.2 (168pp, 15 chapters + 3 appendices)**.
> Kept because the phase history is genuine provenance; read it as history, not state.