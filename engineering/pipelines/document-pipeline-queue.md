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

### 4. Complete PASM2 Reference Manual
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