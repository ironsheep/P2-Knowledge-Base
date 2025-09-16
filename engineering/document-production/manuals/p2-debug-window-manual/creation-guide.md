# P2 Debug Window Manual - Creation Guide

**Canonical Name:** `p2-debug-window-manual`

## 🎯 Document Purpose
Creating a comprehensive practical guide to P2's Debug Window system - the built-in visualization and monitoring capabilities that make P2 development uniquely interactive and accessible.

### Document Philosophy
**"Visual Discovery Through Systematic Exploration"**
- **Transform basic DEBUG usage into expert-level debugging strategies**
- **Explore all 9 window types beyond SPIN-2 v5.1's minimal examples**
- **Discover rich parameter combinations through systematic experimentation**
- **Provide immediate visual verification** - every code example paired with actual screenshot
- **Bridge the capability gap** - users know basics but miss the sophisticated possibilities

### Core Problem This Manual Solves
**The "Iceberg Effect"**: Developers use basic `DEBUG()` syntax but remain unaware of:
- 9 specialized window types with rich parameter systems
- Advanced visualization capabilities hiding in plain sight
- PASM assembly debugging possibilities
- Professional debugging workflows and patterns
- Parameter interactions that create powerful debugging displays

**Our Solution**: Systematic capability discovery with visual proof of every technique.

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

## 📚 Content Sources & Production Method

### Primary Content Sources

#### 1. SPIN-2 Language Reference Manual v5.1 (Primary Technical Foundation)
**Location**: `/sources/extractions/spin2-v51-complete-extraction-audit/`
- Complete DEBUG instruction specifications
- Debug formatting options and syntax
- Built-in debug methods and functions
- Terminal output control and formatting
- Debug system architecture and capabilities
- Performance characteristics of debug operations

#### 2. Phase 1 Comprehensive Window Studies (Revolutionary Discoveries)
**Location**: `/engineering/document-production/manuals/p2-debug-window-manual/studies/`
- **12 comprehensive study documents** covering all 9 window types
- **JonnyMac's Layer System Discovery**: 20× performance improvement through sprite-based updates
- **PC Input Integration**: Bidirectional debugging unique to P2
- **CROP Command Mastery**: Selective display updates for efficiency
- **45 YAML Knowledge Gaps**: Documented and prioritized for AI capability enhancement
- **Multi-Window Coordination Patterns**: Professional debugging workflows
- **Complete Syntax Reference**: Unified command reference from all studies

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
3. **Parameter matrix exploration** - Discovered JonnyMac patterns, CROP commands, layer system
4. **Pattern extraction from source code** - Revolutionary 20× performance improvements found
5. **Developed complementary examples** - Software-only demonstrations for accessibility
6. **PASM debugging integration** - Assembly-level debug capabilities documented
7. **Created 12 comprehensive study documents** - ~400KB of discoveries and analysis
8. **Verified documented features** - SPRITEDEF/SPRITE for PLOT, 16 TRACE modes (0-15)

#### Phase 2: Manual Generation (CURRENT PHASE)
1. **Generate chapters using Opus 4.1** - Leveraging Phase 1 discoveries
2. **Create 50+ working examples** - All pnut_ts validated
3. **Document JonnyMac patterns** - Layer system, CROP commands
4. **Document PLOT sprites** - SPRITEDEF/SPRITE commands with 0-255 IDs, 1-32 pixel dimensions
5. **Include PC input integration** - Mouse and keyboard debug control
6. **Build professional workflows** - Multi-window coordination patterns
7. **Document only verified features** - No speculation about undocumented capabilities

#### Phase 3: Quality Validation
1. **Test all examples** with pnut_ts compiler
2. **Verify debug outputs** match discovered behaviors
3. **Validate JonnyMac techniques** for performance claims
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

### The "Discovery Guide" Voice

**Voice Identity**: Professional Explorer - Systematic discovery with visual excitement

**Core Characteristics:**
- **Exploratory Excitement**: "Let's see what this parameter combination does..."
- **Visual Revelation**: "Watch what happens when we change this setting..."
- **Professional Discovery**: "This technique reveals..." / "The output shows us..."
- **Systematic Exploration**: "Now let's try the next parameter..."
- **Immediate Gratification**: "Look at that - instant visualization!"
- **Visual Confidence**: "This screenshot shows exactly what your debug window should display"

**Why This Voice Works:**
- **Matches Discovery Content**: Exploration-focused manual needs exploration-focused voice
- **Celebrates Visual Learning**: Voice reinforces "aha!" moments screenshots provide
- **Professional yet Engaging**: Reference-quality but maintains discovery excitement
- **Problem-Solving Oriented**: Each technique solves real debugging challenges

**Voice Pattern Examples:**
- ✅ "Here's a technique most developers haven't discovered..."
- ✅ "The visual difference is immediately apparent - no guessing needed"
- ✅ "When we set the plot style to 2, watch how the dual axes transform our data view..."
- ✅ "This parameter combination creates something remarkable..."
- ✅ "The screenshot reveals exactly what's happening in your program"

**Voice DON'Ts:**
- ❌ Overly tutorial language ("Let's learn about debug windows together")
- ❌ Dry reference style ("Parameter 2 accepts values 0-7")
- ❌ Uncertainty hedging ("This might help with debugging")
- ❌ Academic formality ("One observes that the visualization demonstrates...")

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
- **Multi-COG Debugging**: Coordinated debugging across COGs
- **PASM Assembly Debugging**: Debug capabilities within assembly language code
- **Debug Workflows**: Systematic debugging methodologies
- **Integration Patterns**: Debug with other development tools

#### What This Manual References (Not Covers)
- **Basic P2 Programming** → "See PASM2 Manual for instruction details"
- **Smart Pin Operation** → "See Smart Pins Manual for pin debugging"
- **Hardware Setup** → "See Hardware Manual for physical connections"
- **Advanced Applications** → "See specific application guides"

#### Cross-Reference Pattern
When encountering out-of-scope topics:
```markdown
## Debugging Smart Pin Timing
Here's how to monitor Smart Pin state changes:
[debug example]

📚 **For Smart Pin Configuration**: See Smart Pins Manual Chapter 5 for 
proper Smart Pin setup and operation details.
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
[More sophisticated debugging for this scenario]
Professional-level debugging approaches

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
3. Check for timing conflicts between COGs
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
💡 **Pro Tip**: Use different debug channels for different COGs to avoid output conflicts.
:::
```

## 🔧 **CRITICAL: Minimal Hardware Design Philosophy**

### Universal Accessibility Requirement

**Core Principle**: Examples must be accessible to beginners with minimal external hardware requirements. Focus on simple-to-generate projects that demonstrate rich visualization techniques without specialized equipment.

### Hardware Accessibility Levels

**Level 0: Software-Only Examples** (Preferred)
- **Built-in P2 resources only**: 2 LEDs, CORDIC engine, multiple COGs, RNG, internal timers
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
PRI simulate_motor_system()
  repeat
    ' Software-generated encoder feedback
    encoder_pos := (encoder_pos + pwm_duty/100) & $FFFF
    ' Simulated load variation  
    load_torque := GETRND() & $FF
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
        drvh    #56
        waitx   #1000      ' Intended 1ms delay
        drvl    #56
        waitx   #1000
        jmp     #$-4

' DEBUG SOLUTION: Monitor actual timing
        drvh    #56
        debug   "LED ON at ", udec_(getct())
        waitx   #1000
        drvl    #56  
        debug   "LED OFF at ", udec_(getct())
        waitx   #1000
        jmp     #$-8
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
- `' Debug Example - COG Timing - Synchronization Check`
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

## 📖 Finalized Chapter Outline (Based on Phase 1 Discoveries)

### PART I: FOUNDATION - From Basic DEBUG to Visual Discovery
1. **Beyond Basic DEBUG - The Vision Gap** - The Debug Iceberg Effect and capability discovery
2. **Terminal Mastery - Interactive Text Debugging** - PC Input Integration and bidirectional communication
3. **Graphics Breakthrough - From Text to Visuals** - When text isn't enough, BITMAP and display emulation

### PART II: INTERACTIVE APPLICATIONS - Revolutionary Debug GUIs
4. **Layer Composition System - Sprite-Based Debugging** - JonnyMac's 20× performance revolution
5. **PC Input Integration - Bidirectional Debug Control** - Mouse and keyboard interactive debugging
6. **Professional Debug Instruments** - Analog meters, LED panels, interactive switches

### PART III: DATA EFFICIENCY - High-Performance Debugging
7. **Packed Data Revolution - 16x Compression** - Performance transformation scenarios
8. **Data Visualization Mastery - PLOT Window** - Beyond simple plotting, multi-series relationships

### PART IV: ADVANCED ANALYSIS - Professional Development Tools
9. **Digital Signal Analysis - LOGIC Window Applications** - Multi-signal analysis and protocol debugging
10. **Waveform Analysis - SCOPE and SCOPE_XY Windows** - Analog signal debugging and phase relationships
11. **Frequency Domain Analysis - FFT and SPECTRO Windows** - Beyond time domain debugging

### PART V: INTEGRATION MASTERY - Professional Workflows
12. **Multi-Window Coordination** - Synchronized debugging displays and workflow automation
13. **PASM Assembly Integration** - Assembly debug patterns and multi-COG coordination
14. **Production Integration Workflows** - Screenshot-driven documentation and automated testing

### Appendices (Updated Based on Phase 1)
- A: Complete Command Reference - All discovered commands from Phase 1 studies
- B: Packed Data Format Reference - Compression specifications and performance gains
- C: Performance Optimization Guide - Efficiency patterns across all window types
- D: Professional Examples Library - 50+ validated working examples

## 📏 Size Guidelines
- **Target length**: 200-250 pages
- **Chapter size**: 10-15 pages each
- **Example density**: 2-3 working examples per chapter
- **Practical focus**: 70% examples, 30% explanation

---

# PART 4: PRODUCTION SPECIFICATIONS

## 🔧 Technical Requirements

### Code Validation
- **MUST compile with pnut_ts** without errors or warnings
- **MUST produce actual debug output** when run
- **MUST be complete programs** (not code fragments)
- **MUST use consistent debug formatting** throughout manual
- **MUST capture window screenshots** using P2's built-in bitmap save capability
- **MUST include visual verification** - code example + actual screenshot output

### Debug Output Standards
```pasm2
' GOOD: Consistent debug formatting
        debug   "Timer: ", udec_(timer_value), " Status: ", uhex_(status)

' GOOD: Clear debug labels
        debug   "COG", udec_(cogid()), ": Starting main loop"

' BAD: Unclear debug output  
        debug   udec_(x)        ' What is x? When does this print?
```

### Example Verification Process
1. **Compile** all examples with latest pnut_ts
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
- 32+ complete debug examples
- 16 chapters with systematic coverage
- 100% code compilation success
- <10 minutes to implement any debug technique
- 200-250 pages of practical content

## Qualitative Goals
- **Transforms debugging from frustration to insight**
- **Makes P2's debug capabilities accessible to all skill levels**
- **Serves as the definitive reference for P2 debugging**
- **Enables confident debugging of complex P2 systems**
- **Showcases P2's unique debugging advantages**

---

# APPENDIX: P2 Debug System Overview

## Key Debug Capabilities to Document
- DEBUG instruction variants and formatting
- Terminal window interaction and display
- Debug performance monitoring
- Multi-COG debug coordination
- Visual debug output (plots, scopes)
- Debug integration with development workflow
- Advanced debug techniques for complex systems

## Source Material Integration
- Official P2 debug documentation
- Community debug examples and patterns  
- Proven debug workflows from other projects
- Advanced debug techniques from expert developers

---

## Version Control

- **Version**: 2.0 (Post-Phase 1 Update)
- **Date**: 2025-09-14
- **Status**: Phase 2 Manual Generation Ready
- **Phase 1**: ✅ COMPLETED - 12 comprehensive window studies
- **Phase 2**: 🚧 IN PROGRESS - Opus 4.1 manual generation
- **Major Discoveries**: JonnyMac Layer System (20× performance), PC Input Integration, CROP Commands
- **Next Step**: Generate chapters 1-14 using Opus 4.1