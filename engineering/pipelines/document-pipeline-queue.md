# Document Pipeline Queue

## Pipeline Strategy
When reviewing sprints, we ask: "We're going breadth first, which one of these do we want to do next? What's next up in importance?"

## Ingestion Analysis Tasks (Pre-Document Generation)

### 1. Titus Smart Pins Narrative Extraction Validation
**Purpose**: Ensure 100% capture of Jon Titus's pedagogical content before Green Book generation
**Status**: Ready to execute
**Instructions**: `/sources/extractions/smart-pins-complete-extraction-audit/NARRATIVE-EXTRACTION-VALIDATION.md`
**Critical Focus**:
- Verify ALL narrative explanations extracted (not just specs/code)
- Check "why" explanations for configurations
- Confirm tutorial progression preserved
- Validate all 174 examples have context
**Output**: `narrative-gaps-found.md` listing any missing content
**Next Step**: Once validated, proceed to Green Book generation with Opus
**Priority**: IMMEDIATE - Blocks Smart Pins Green Book generation

## Currently Queued Documents

### 1. Terminal Window User's Manual
**Purpose**: Document P2's built-in debug visualization capabilities
**Content**:
- Software oscilloscopes
- FFT displays  
- Logic analyzers
- Multi-channel scopes
- Plots and bitmap displays
- Live memory windows
**Voice**: Stephen/IronSheep (making debug accessible)
**Priority**: High - Major differentiator few know about
**Enablement**: May already be possible from existing extractions

### 2. Single Step Debugger User's Manual
**Purpose**: Document P2's debugging capabilities
**Content**:
- COG-to-COG monitoring (non-invasive)
- Breakpoints in PASM2/SPIN2
- Single-stepping execution
- Memory inspection
- Register viewing
- Performance monitoring without impact
**Voice**: Stephen/IronSheep or Parallax Educational
**Priority**: High - Critical for development
**Enablement**: May already be possible from existing extractions

### 3. P2 Functional Decomposition Case Studies
**Purpose**: Teach "P2 way of thinking" through examples
**Content**:
- When to use multiple COGs vs single COG
- When to use Smart Pins vs bit-banging
- When to use SPIN2 vs inline PASM2
- How to partition work across COGs
- Memory architecture decisions
- Communication pattern selection
- Real-world trade-off examples
**Voice**: Narrative/Story combined with Stephen/IronSheep
**Priority**: Very High - Teaches architectural thinking
**Enablement**: Requires pattern extraction from examples

### 4. P2 Eval HUB75 Adapter Board Datasheet (SKU 64032)
**Purpose**: Document Iron Sheep Productions' HUB75 LED panel adapter for P2 Eval board
**Content**:
- Physical specifications and pinout
- P2 pin mapping to HUB75 signals (R1/G1/B1/R2/G2/B2/CLK/LAT/OE/A/B/C/D/E)
- Power requirements and distribution
- Maximum panel size/count supported
- Timing specifications
- Example driver code for common panel sizes
- Daisy-chaining configuration
**Voice**: Parallax technical documentation style
**Priority**: HIGH - Product exists without documentation
**Author**: Stephen/IronSheep (product creator)
**Enablement**: Ready - Stephen has all technical details

### 5. Complete PASM2 Reference Manual
**Status**: Sprint planned, ready to execute
**Voice**: Chip (technical accuracy) with examples

### 5. P2-for-P1 Users Guide (deSilva style)
**Status**: Sprint planned, ready to execute  
**Voice**: deSilva (gentle teacher)

### 6. AI-Optimized P2 Reference
**Status**: v1.0 partially complete
**Voice**: Claude (AI-pedagogical)

### 7. Claude Best Practices for P2 Development Guide
**Purpose**: Safe, effective, cost-conscious Claude usage for P2 community
**Content**:
- Model selection for different P2 tasks (Opus/Sonnet/Haiku)
- P2-specific Claude limitations and validation needs
- Safe code generation practices for PASM2/SPIN2
- Cost optimization strategies for community members
- What Claude knows well vs knowledge gaps
- When to use Claude vs community forums
**Voice**: Stephen/IronSheep (practical guidance)
**Priority**: URGENT - Needed before live P2 community demo
**Scheduling**: Must complete before Stephen's live demo to P2 community
**Enablement**: Can be written immediately using project learnings

## Selection Criteria for Next Document
1. **Immediate Value**: What unblocks the most users?
2. **Enablement**: Do we have sufficient extracted knowledge?
3. **Breadth Impact**: Does it serve multiple audiences?
4. **Unique Value**: Does it document something nowhere else does?
5. **Community Need**: What are people asking for most?
6. **Timing Constraints**: Live demo commitments

## URGENT Priority
**Claude Best Practices Guide** - Required before community demo!
- Prevents unsafe usage patterns
- Manages cost expectations
- Sets realistic Claude capabilities
- Critical for responsible community rollout

## Notes on Enablement
Stephen notes: "A couple of these documents might already be enabled depending on the quality of your ingestion"
- Check existing extractions for debug/terminal content
- ROM Monitor documentation may enable debugger manual
- SPIN2 v51 may have terminal window details
- Silicon doc might have debug architecture

## Magazine Articles Pipeline (Market Awareness)

### Purpose
Expand P2 awareness beyond existing embedded community through targeted feature articles in technical magazines.

### Hero Articles (Cross-Platform Appeal)

#### 1. "The Death of RTOS: How 8 Hardware Cores Change Everything"
**Target**: Embedded Systems Design, Circuit Cellar
**Angle**: Challenge fundamental assumption that RTOS is necessary
**Key Points**:
- No scheduler overhead or priority inversions
- Each peripheral gets dedicated CPU
- Deterministic by default
**Enablement**: Ready - have core architecture understanding

#### 2. "Your Variables Are Already In Registers: The Spin2 Magic Trick"
**Target**: Dr. Dobb's successor publications, Hackaday
**Angle**: Revolutionary inline assembly with auto-sync
**Demo**: C complexity vs Spin2 simplicity comparison
**Enablement**: Ready - deep understanding from language study

#### 3. "Built-In Oscilloscope: Debug Like It's 2025"
**Target**: Elektor, Make Magazine
**Angle**: DEBUG as complete instrument suite
**Visual**: Live waveform screenshots
**Enablement**: Needs Terminal Window extraction validation

### Audience-Specific Series

#### ARM Developer Series
1. "Escape from Interrupt Hell: The P2 Way"
2. "No Cache, No Problem: When Every Core Has Local RAM"
3. "DMA Is Dead, Long Live Smart Pins"
**Target**: Embedded.com, EE Times

#### Raspberry Pi Developer Series  
1. "Real-Time Pi: What If Linux Wasn't In The Way?"
2. "The 40-Pin Alternative: P2 vs Pi GPIO"
3. "Headless From Birth: When You Don't Need An OS"
**Target**: MagPi, Linux Journal

#### Arduino Developer Series
1. "Arduino×8: Your First Multi-Core Experience"
2. "From pinMode to Smart Pins: The Evolution"
3. "Debug Without Serial.print: Welcome to the Future"
**Target**: Make Magazine, Hackspace

### Specialty Articles

#### Motor Control
"32 Simultaneous Quadrature Decoders: Not A Typo"
**Target**: Motion Control magazine, Servo Magazine

#### Signal Processing
"CORDIC In Silicon: When Math Becomes Hardware"
**Target**: DSP Related, Signal Processing Magazine

#### Robotics
"The Sensor-Per-Core Architecture"
**Target**: Robot Magazine, IEEE Robotics

### Article Enablement Status

| Article | Knowledge Ready | Needs | Priority |
|---------|----------------|-------|----------|
| Death of RTOS | ✅ Yes | Examples | HIGH |
| Variables in Registers | ✅ Yes | Code demos | HIGH |
| Built-In Oscilloscope | 🔶 Partial | Terminal Window details | MEDIUM |
| Arduino×8 | ✅ Yes | Comparison code | HIGH |
| Smart Pins vs pinMode | 🔶 Partial | Complete Smart Pin ref | MEDIUM |
| CORDIC Hardware | ✅ Yes | Math examples | LOW |

### Quick Win Blog Posts (Immediate)
1. "5 Things You Can't Do on Arduino (But Can on P2)"
2. "Watch 8 LEDs Blink Independently (No Interrupts!)"
3. "Your First Multi-Core 'Hello World'"
4. "Why SEND/RECV Changes Everything"
5. "From digitalWrite to PINH: A Journey"

### Article Production Strategy

**Phase 1**: Blog posts on P2 forum and Hackaday (immediate)
**Phase 2**: Hero articles submission to major publications (Q1)
**Phase 3**: Series development for specific audiences (Q2)
**Phase 4**: Video companions for YouTube/social (ongoing)

### Success Metrics
- Article views/shares
- Forum traffic from articles
- New user inquiries mentioning articles
- P2 sales correlation with article publication

## "Discover the P2" Progressive Tutorial Series

### Purpose
Introduce P2 capabilities progressively through a 9-part series that builds knowledge incrementally while maintaining engagement through practical "WOW" moments.

### Series Architecture
- **Audience**: Complete beginners to experienced makers
- **Format**: Each article builds on previous knowledge only
- **Structure**: Problem → Traditional solution → P2 elegant approach → WOW demonstration
- **Distribution**: Sequential release (weekly/biweekly)

### Complete Series Outline

#### Article 1: "8 Brains Are Better Than 1"
**Hook**: What if your microcontroller could actually multitask?
**Core Concept**: Introduction to 8 independent cores
**Demo**: 8 LEDs with different patterns + 8 buttons + serial communication
**WOW**: Everything runs smoothly with no interrupts, timing conflicts, or complexity
**Enablement**: ✅ Ready - core architecture well understood

#### Article 2: "Smart Pins: Your Hardware Assistants"
**Hook**: Set it and forget it hardware
**Core Concept**: Autonomous peripheral processors
**Demo**: 8 servos controlled while CPU does complex calculations
**WOW**: Robot arm moves smoothly while display shows CPU 100% free
**Enablement**: 🔶 Partial - need complete Smart Pin examples

#### Article 3: "The CORDIC Engine: Math at Hardware Speed"
**Hook**: Complex math without the wait
**Core Concept**: Hardware acceleration for trigonometry/coordinates
**Demo**: Real-time 3D wireframe rotation
**WOW**: Multiple 3D objects rotating at 60 FPS, comparison with software math
**Enablement**: ✅ Ready - CORDIC well documented

#### Article 4: "Video Output Without Breaking a Sweat"
**Hook**: Built-in video, no shield required
**Core Concept**: Direct VGA/HDMI generation via Streamer
**Demo**: Live sensor dashboard on VGA monitor
**WOW**: Full 640x480 display with graphs while cores remain available
**Enablement**: 🔶 Partial - need Streamer examples

#### Article 5: "Real-time Signal Processing"
**Hook**: DSP capabilities built in
**Core Concept**: Integrated ADC + Smart Pins + CORDIC
**Demo**: Live audio spectrum analyzer
**WOW**: Simultaneous recording, analyzing, displaying, generating
**Enablement**: 🔶 Partial - need integrated examples

#### Article 6: "Debug Like You're From the Future"
**Hook**: See inside your code while it runs
**Core Concept**: Built-in DEBUG visualization system
**Demo**: Multiple live debug windows (scope, logic, FFT)
**WOW**: "$25 chip includes $5000 worth of test equipment"
**Enablement**: ✅ Ready - DEBUG system fully cataloged

#### Article 7: "Precision Timing Across 8 Cores"
**Hook**: Orchestra conductor precision
**Core Concept**: Hardware synchronization between cores
**Demo**: 8-channel LED music visualizer with perfect sync
**WOW**: Slow-motion proof of microsecond coordination
**Enablement**: 🔶 Partial - need sync examples

#### Article 8: "Hub RAM: The Grand Central Station"
**Hook**: Teamwork at 180 MHz
**Core Concept**: Elegant shared memory architecture
**Demo**: Pipeline processing with each cog as one stage
**WOW**: Visualization of data flowing through 8-core pipeline
**Enablement**: ✅ Ready - Hub architecture understood

#### Article 9: "From Prototype to Product"
**Hook**: Now you're thinking in parallel
**Core Concept**: Complete system integration
**Demo**: Full pinball machine controller
**WOW**: Professional system built with clean architecture
**Enablement**: 🔶 Needs complete example project

### Production Requirements

#### Per Article Needs
- Working code examples (tested on hardware)
- Video demonstrations of WOW element
- Circuit diagrams/wiring guides
- Progressive complexity management
- "What's Next" teaser for following article

#### Series-Wide Assets
- Consistent visual branding
- GitHub repo with all code
- Video playlist
- Forum discussion thread per article
- "Series roadmap" graphic

### Distribution Strategy

**Primary Channels**:
1. Parallax Forums (home base)
2. Hackaday.io project pages
3. YouTube (video companions)
4. Medium/Dev.to (text versions)

**Secondary Channels**:
1. Reddit (r/embedded, r/microcontrollers)
2. Twitter/X thread summaries
3. LinkedIn articles
4. Instructables (project versions)

### Success Metrics
- Completion rate (how many read all 9)
- Code download/fork statistics  
- Video view completion rates
- Forum engagement per article
- New P2 purchases tracked to series

### Enablement Summary

| Article | Knowledge Ready | Needs | Priority |
|---------|----------------|-------|----------|
| 1. 8 Brains | ✅ Full | Hardware demos | HIGH |
| 2. Smart Pins | 🔶 Partial | Complete examples | HIGH |
| 3. CORDIC | ✅ Full | 3D demo code | MEDIUM |
| 4. Video | 🔶 Partial | Streamer examples | MEDIUM |
| 5. Signal | 🔶 Partial | Integration demo | LOW |
| 6. Debug | ✅ Full | Screen recordings | HIGH |
| 7. Timing | 🔶 Partial | Sync examples | LOW |
| 8. Hub RAM | ✅ Full | Pipeline demo | MEDIUM |
| 9. Complete | 🔶 Partial | Full project | LOW |

### Launch Timeline Recommendation
1. **Immediate**: Write articles 1, 3, 6, 8 (fully enabled)
2. **Next Sprint**: Gather examples for 2, 4
3. **Following Sprint**: Develop integrated demos for 5, 7, 9
4. **Launch**: Begin weekly release after first 4 articles complete