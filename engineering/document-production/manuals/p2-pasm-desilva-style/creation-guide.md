# P2 PASM De Silva Style - Creation Guide

**Canonical Name:** `p2-pasm-desilva-style`

## 🎯 Document Purpose
Creating a pedagogical PASM2 manual that captures deSilva's teaching philosophy: approachable, hands-on, and genuinely enjoyable assembly language learning.

### Modular Manual Strategy (2025-01-09 Addition)
This manual is part of a modular documentation system:
- **This Manual**: Core PASM2 assembly programming with basic I/O (250-300 pages)
- **P2 I/O & Smart Pins User Guide**: Comprehensive Smart Pin modes, applications, and
  advanced I/O (separate). This one document now covers both roles; the earlier Smart
  Pins Tutorial that split them is retired and superseded by it.
- **DEBUG Manual**: Debug system reference (separate or integrated)

**Rationale**: Cognitive load management - Core PASM2 alone is substantial enough for one focused manual.

## Code Line Budget

The colored code boxes do NOT wrap, so an over-long code line is an authorship
defect caught by the `prepare-manual` line-length audit
(`engineering/tools/validation/audit-code-line-length.py`).

- **Max code columns (K): 76**
- **Code-box style / font:** as of the 2026-06-09 platform migration this manual
  rides the shared **platform** code boxes (`IOSPBlock` green PASM2 / `Spin2Block`
  blue), Latin Modern Mono with the `numbers=left` gutter. It consumes the platform
  code-box stack unchanged, so it **inherits the platform reference K** (calibrated
  in `manuals/p2-layout-torture-test/creation-guide.md` → Code Line Budget).
  Re-measure only if this manual ever diverges its code font/box geometry.

## 📚 Content Sources & Production Method (2025-01-09 Addition)

### Primary Content Sources

#### 1. YAML Instruction Files (Technical Accuracy)
**Location**: `deliverables/ai/P2/language/pasm2/`
- Complete instruction set documentation
- Accurate timing and flag information  
- Hardware operation details
- Recently updated with DEBUG and Smart Pin reset requirements

#### 2. Opus Master (Pedagogical Structure)
**Location**: `engineering/document-production/manuals/p2-pasm-desilva-style/opus-master/`
- Chapters 1-6: Strong foundation to preserve
- Chapter structure and flow
- De Silva voice examples
- Working code examples

#### 3. Pattern Extractions (Code Examples)
**Location**: Recent pattern extraction work
- PASM2 idioms and patterns
- Common code structures
- Best practices

#### 4. Smart Pins & I/O Documentation
**For Chapter 8 Basic I/O only**:
- Extract only basic pin operations (DRVH, DRVL, TESTP)
- Reference the P2 I/O & Smart Pins User Guide for advanced features
- Keep focus on assembly, not peripheral complexity

### Production Method

#### Phase 1: Content Development
1. **Preserve Chapters 1-6** from Opus master (strong foundation)
2. **Enhance Chapter 7 (CORDIC)** using YAML cordic instructions
3. **Rewrite Chapter 8** as "Basic I/O" (no Smart Pins complexity)
4. **Develop Chapters 9-12** with core assembly focus
5. **Minimize Chapters 13-15** to brief examples with external references
6. **Enhance Chapter 16** (Multi-COG) with pattern examples

#### Phase 2: Pedagogical Enhancement
1. **Add Medicine Cabinet** sections to each chapter
2. **Enhance Your Turn** exercises with scaffolding
3. **Add celebration moments** at chapter ends
4. **Insert encouragement** during complex topics
5. **Connect chapters** with preview/review bridges

#### Phase 3: Quality Validation
1. **Test all code examples** with pnut-ts compiler
2. **Verify technical accuracy** against YAML sources
3. **Check pedagogical flow** for smooth progression
4. **Ensure voice consistency** throughout
5. **Validate cross-references** to other manuals

## 🔍 Content Verification Protocol (Hallucination Prevention)

**Added:** 2026-01-23
**Derived from:** PASM2 Manual Content Verification Sprint findings

### Why This Section Exists

The PASM2 technical reference audit discovered that **hallucinations occur at the moment of writing**, not after. Even pedagogical content can propagate technical errors if claims aren't verified. Tutorial voice makes false claims MORE dangerous because readers trust the friendly tone.

**Critical insight**: The voice tells you HOW to say things. This section tells you HOW TO VERIFY what you're about to say is true.

### Claim Types and Required Sources for Pedagogical PASM

| Claim Type | Required Source | Example Claim |
|------------|-----------------|---------------|
| **Instruction behavior** | YAML `description:` field | "ADD stores sum in Dest" |
| **Flag effects** | YAML `flags:` field | "C flag set on carry" |
| **Timing claims** | YAML `clocks:` field | "Takes 2 clock cycles" |
| **Architecture claims** | P2 Documentation v35 ONLY | "8 COGs share Hub" |
| **COG memory model** | P2 Documentation v35 ONLY | "512 longs of COG RAM" |
| **Hub access patterns** | P2 Documentation v35 ONLY | "Egg beater timing" |
| **Code example behavior** | pnut-ts compilation | "This blinks the LED" |

### Red-Flag Phrases for Pedagogical Content

**STOP and verify when you're about to write:**

| Phrase | Risk Level | Why Suspicious | Tutorial Danger |
|--------|------------|----------------|-----------------|
| "automatically" | **CRITICAL** | P2 rarely auto-anything | Learners assume it "just works" |
| "simply" / "just" | **HIGH** | Oversimplification may hide complexity | Learners confused when "simple" fails |
| "always" / "never" | **HIGH** | Absolute claims need verification | Creates wrong mental models |
| "similar to" | MEDIUM | Analogy may be misleading | Wrong assumptions transfer |
| "typically" | MEDIUM | What's the actual behavior? | Learners don't know exceptions. **Stop and verify — this is not a banned word.** If the behavior is fixed, say what it is; if it genuinely varies, "typically" is *required* accuracy under R1 (see `voice-guide.md` §2), and the exception belongs in the sentence. |
| "behind the scenes" | MEDIUM | Invented implementation details | Can't be verified by learner |

### The Verification Protocol for Tutorial Content

**Before writing ANY technical claim in tutorial voice:**

```
┌─────────────────────────────────────────────────────────────────┐
│           PEDAGOGICAL CONTENT VERIFICATION CHECKLIST            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. What am I claiming? (instruction/timing/architecture)       │
│                                                                 │
│  2. Can I cite a source?                                        │
│     □ YAML instruction file (for instruction claims)            │
│     □ P2 Documentation v35 (for hardware/architecture claims)   │
│     □ pnut-ts compilation (for code behavior claims)            │
│                                                                 │
│  3. Is my analogy accurate?                                     │
│     □ Does the comparison hold in ALL relevant ways?            │
│     □ Am I noting where the analogy breaks down?                │
│                                                                 │
│  4. Would a beginner be misled?                                 │
│     □ Is the simplification SAFE for learning?                  │
│     □ Will they need to UNLEARN this later?                     │
│                                                                 │
│  5. Does the code ACTUALLY work?                                │
│     □ Compiled with pnut-ts → no errors                         │
│     □ Produces the claimed result                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Pedagogical-Specific Verification Examples

**Example 1: Correct Simplification**

Claim to write: "Think of COGs as 8 workers in a kitchen, each with their own cutting board"

1. Claim type: Analogy for COG parallelism
2. Verify: Does analogy hold? COGs ARE parallel AND independent → YES
3. Check: Does analogy break? Workers can talk, COGs need explicit Hub → NOTE THIS
4. Safe for learning? YES, captures essential concept
5. Result: Write analogy, but add "unlike kitchen workers, COGs need explicit Hub to share data"

**Example 2: Dangerous Simplification**

Attempted claim: "Just add WC and the carry flag takes care of itself"

1. Claim type: Flag behavior simplification
2. Risk: "takes care of itself" implies automatic handling
3. Verify: What ACTUALLY happens? WC causes explicit flag write
4. Would beginner be misled? YES - they won't understand flag must be USED
5. Result: **REWRITE** → "Add WC to save the carry, then use IF_C to act on it"

### Code Example Verification

**Every code example MUST:**
1. Compile with `pnut-ts` without errors
2. Produce the claimed observable result
3. Be complete enough to run (no "..." snippets for working code)
4. Have comments that match actual behavior

### Full Audit Methodology Reference

For comprehensive post-write audit procedures, see:
`engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`

---

## 🧗 Technical Climbing Methodology Applied

This document follows the project-wide Technical Climbing Methodology, contributing to all four P2KB facets:

1. **Rich Trusted Source** - Each iteration incorporates newly validated P2 information
2. **Download-on-Demand** - Optimized for Claude instances helping P2 developers
3. **Human Documentation** - Pedagogically sound manuals for learning
4. **AI-Ingestible Format** - Structure supports future JSON schema extraction

### Regeneration Cycles: Our Climbing Strategy

**Why We Regenerate:**
- New trusted P2 sources become available
- Community feedback identifies gaps
- Pedagogical improvements discovered
- Technical corrections needed

**Protection Points (What We Preserve):**
- Successful pedagogical patterns Opus created
- Voice and tone that resonates
- Code examples that work
- Structure that flows

**Climbing Higher (What Improves):**
- Generation N: Base content with available sources
- Generation N+1: Enhanced with new trusted sources + process improvements
- Generation N+2: Refined with community feedback + proven patterns
- Result: Monotonic quality improvement

**Documentation as Protection:**
- Every success → Documented in this guide
- Every gap → Captured in technical-debt.md
- Every iteration → Builds on protected foundation
- No regression possible → Previous quality is our safety floor

---

# PART 1: CONTENT CREATION (What Authors Write)

## 📝 Content Philosophy

### The deSilva Voice (Document-Specific)

**Note**: This voice is specific to pedagogical manuals. Technical references will have different voice requirements.

**Voice Consistency Rule**: Every regeneration of THIS document must maintain THIS voice.

- **Conversational**: "Well, here we are! You're about to embark..."
- **Encouraging**: "Don't worry, we'll get through this together" / "Have Fun!"
- **Honest**: "This is complex, but here's the medicine cabinet"
- **Self-Deprecating**: "If you think this is terribly complicated, you are probably right..."
- **Playful**: "Uff!" when completing something hard
- **Human**: Acknowledge frustration, celebrate victories
- **Visual Awareness**: "When you belong to the 75% more visually oriented persons..."
- **Prerequisite Checking**: "You know SPIN, don't you?" - gentle knowledge checks
- **School Connections**: "Remember binoms from school? No?" - connects to past learning
- **Personality in Technical**: "Need an explanation? All right:" - responsive teaching

**Why This Voice for PASM2**:
1. **Assembly is Intimidating** - De Silva's conversational tone removes fear
2. **Abstract Concepts** - Friendly metaphors make parallel processing approachable
3. **High Cognitive Load** - Playfulness provides mental breaks
4. **Easy to Get Lost** - Encouragement keeps learners going
5. **P2 is Different** - Patience needed for paradigm shift
6. **Diverse Learning Styles** - Visual learners need diagrams, others need text
7. **Building on Prior Knowledge** - School references create familiar anchors
8. **Maintaining Engagement** - Personality and humor prevent dry technical monotony

### Progressive Learning Structure

**Pedagogical Foundation**: Constructivist Learning Theory (Piaget, Vygotsky)
- Learners build knowledge on existing foundations
- New knowledge must connect to prior understanding
- Active engagement creates deeper learning than passive reception

**Implementation Pattern**:
1. **Hook**: Start with working code
   - *Theory*: Experiential Learning (Kolb, 1984) - Concrete experience before abstract conceptualization
   - *Template*: 3-5 lines of immediately runnable code with visible result
   
2. **Explore**: Understand what just happened
   - *Theory*: Inquiry-Based Learning - Discovery after experience leads to retention
   - *Template*: "Let's see what each line actually did..."
   
3. **Expand**: Add complexity gradually
   - *Theory*: Zone of Proximal Development (Vygotsky) - Stay within reach of current ability
   - *Template*: Add ONE new element, keeping 80% familiar
   
4. **Practice**: "Your Turn" exercises
   - *Theory*: Active Learning - Doing > Watching > Reading > Listening
   - *Template*: Modify working code before creating from scratch
   
5. **Medicine**: Simpler alternatives when overwhelmed
   - *Theory*: Cognitive Load Theory - Provide escape route when working memory saturates
   - *Template*: "Feeling overwhelmed? Here's the 3-line version that just works..."

## 📚 Content Requirements

### Modular Scope Boundaries (2025-01-09 Addition)

#### What This Manual Covers
- **Core PASM2 Instructions**: Complete instruction set with examples
- **COG Architecture**: 8-processor parallel model, hub/cog relationship
- **Basic I/O**: DRVH, DRVL, TESTP, FLTL, WAITP (no Smart Pins)
- **Hub Operations**: RDLONG, WRLONG, block transfers
- **Math & Logic**: Hardware multiply/divide, boolean operations
- **CORDIC Basics**: Unique P2 feature for trig/rotation
- **Multi-COG Patterns**: Communication, synchronization, orchestration
- **Assembly Optimization**: Pipeline, timing, efficiency

#### What This Manual References (Not Covers)
- **Smart Pin Details** → "See the P2 I/O & Smart Pins User Guide for PWM, UART, etc."
- **Complex Protocols** → "See the P2 I/O & Smart Pins User Guide for SPI, I2C implementations"
- **Video Generation** → "See Video Guide for VGA/HDMI details"
- **DEBUG System** → "See DEBUG Manual for visualization tools"
- **Advanced Signal Processing** → "See DSP Guide for filters, FFT"

#### Cross-Reference Pattern
When encountering out-of-scope topics:
```markdown
## Simple UART Example
Here's basic bit-banged UART to understand timing:
[code example]

📚 **For Hardware UART**: See the P2 I/O & Smart Pins User Guide (Serial
Transmit / Serial Receive) for configuring Smart Pins as UART with automatic
baud rate generation.
```

### Chapter Structure Template

**Pedagogical Foundation**: Gagne's Nine Events of Instruction (Gagne, 1985)
- Gain attention → Inform objectives → Recall prior learning → Present content → Provide guidance → Elicit performance → Provide feedback → Assess → Enhance retention

**How This Template Embodies The Theory**:

```markdown
# Chapter N: Catchy Title

*Italicized tagline that captures the essence*

## The Hook: Immediate Engagement
[Theory: Gain Attention - Create curiosity gap]
Start with working code that does something surprising/useful in 3-5 lines
"Look at this - just three instructions and your LED is blinking!"

## What Just Happened?
[Theory: Inform Objectives - Set expectations]
"By the end of this chapter, you'll be able to..."
Break down the hook code line by line

## Core Concept 1
[Theory: Present New Content + Recall Prior Learning]
Connect to previous chapter: "Remember how we..."
Introduce ONE new idea building on that foundation
Show code example with ONE thing changed

## The Medicine Cabinet
[Theory: Provide Learning Guidance - Scaffold for different levels]
"If that's too much, here's the absolute minimum:"
Provide simpler alternative that still works

## Your Turn: Experiments
[Theory: Elicit Performance - Active practice]

### Experiment 1: Simple Modification
Change ONE thing from the example
Success is immediately visible

## Common Gotchas
[Theory: Provide Feedback - Address misconceptions]
"If your LED isn't blinking, check..."
Each gotcha has a clear fix

## What We've Learned
[Theory: Assess Performance - Self-check understanding]
- ✅ Concrete achievement they can demonstrate
- ✅ Skill they can now apply

## Coming Up Next
[Theory: Enhance Retention and Transfer]
"Now that you can X, we'll use it to build Y..."

---

**Have Fun!** [Emotional engagement improves retention]

---
```

### Special Content Sections

#### Section Numbering Conventions

**CRITICAL**: Maintain consistent numbering/lettering throughout the manual:

- **Chapters**: Numbered 1, 2, 3... (standard chapter numbering)
- **Sidetracks**: Lettered A, B, C, D, E, F... across the entire manual
  - Example: "Sidetrack A: Why Start at Address 0?"
  - Example: "Sidetrack B: The Philosophy of Parallel Processing"
- **Interludes**: Numbered 1, 2, 3... across the entire manual
  - Example: "Interlude 1: A Brief History of the Propeller"
  - Example: "Interlude 2: What Makes P2 Different"

**Implementation Notes**:
- Track sidetrack letters globally (not per chapter)
- Track interlude numbers globally (not per chapter)
- Add letter/number to the title within the content
- Template will style appropriately

#### Missing Content Placeholder
```markdown
:::missing
🚧 **CONTENT MISSING - COMING SOON**

This section will cover [specific topic]...
[Expected content: instruction tables, timing diagrams, etc.]
:::
```

#### Technical Review Needed
```markdown
:::review
🔍 **NEEDS TECHNICAL REVIEW**

[Specific claim needing verification]
Source: [where this came from]
Question: [what needs checking]
:::
```

#### Diagram Placeholder
```markdown
:::diagram
🎨 **DIAGRAM NEEDED**

[Description of diagram: e.g., "8-COG hub access timing"]
Key elements to show:
- Element 1
- Element 2
:::
```

#### Your Turn Exercise

**Pedagogical Foundation**: Scaffolded Practice (Wood, Bruner, Ross, 1976)
- Start with high support, gradually remove scaffolding
- Success builds confidence for next challenge
- Clear success criteria prevents frustration

```markdown
::: your-turn
**Your Turn:** [Action verb + specific task]

Starting code:
```pasm2
        mov     x, #0  ' [What this gives them]
```

Goal: [Observable outcome - "Make the LED blink twice as fast"]
Hint: [One specific thing to focus on - "Which line controls timing?"]
Success Check: [How they know it worked - "LED toggles every 0.125 seconds"]
:::
```

#### Chapter Conclusion
```markdown
:::chapterend
**Congratulations!** [Specific achievement]

You now understand:
- Key concept 1
- Key concept 2

**Next:** [Preview of next chapter]
:::
```

## 📖 Code Example Design Principles

**Pedagogical Foundation**: Cognitive Load Theory (Sweller, 1988)
- Working memory capacity is limited (7±2 items)
- Intrinsic load (complexity) + Extraneous load (presentation) must not exceed capacity
- Examples should minimize extraneous load to maximize learning

### The "First Exposure" Pattern

**Theory Applied**: One new element at a time
```pasm2
' GOOD: Introducing ADD (only instruction is new)
        add     x, #1         ' Everything else familiar
        
' BAD: Introducing ADD (too many new things)
        add     value, delta wc  ' New instruction, new registers, new flag
```

### Code Example Naming Convention

**Decision**: Use semantic naming, NOT numerical sequencing

**Rationale** (differs from original deSilva college course approach):
- **Our Context**: AI knowledge base + reference manual, not linear course
- **Access Pattern**: Non-linear, search-based, jump-to-what-you-need
- **AI Optimization**: Semantic names provide context for LLM understanding
- **Maintainability**: Adding examples doesn't cascade numbering changes
- **Modern Practice**: Aligns with MDN, React docs, etc.

**Two Types of Code Display**:

1. **Complete Program Blocks** (full working examples):
   - Start with descriptive comment: `' LED Blinker - Basic`
   - Semantic naming throughout
   - These are complete, runnable programs
   
2. **Code Snippets** (1-2 lines discussed inline):
   - No header needed
   - Still use code highlighting
   - For discussing specific instructions or concepts

**Example of Named Program Block**:
```pasm2
' LED Blinker - Your first PASM2 program!
        org     0
        drvh    #56
        waitx   ##25_000_000
        drvl    #56
        waitx   ##25_000_000
        jmp     #$-4
```

**Example of Inline Snippet**:
```pasm2
        add     x, #1    ' Just showing this instruction
```

**Naming Pattern Guidelines**:
- Format: `' [Function] - [Variant/Detail]`
- Examples:
  - `' LED Blinker - Basic`
  - `' LED Blinker - With Register`
  - `' LED Pattern - SOS`
  - `' PWM Fader - Triangle Wave`
  - `' Multi-COG Example - Synchronized LEDs`

**Why This Matters for P2KB**:
- Searchable by concept ("Find all PWM examples")
- Self-documenting for future maintainers
- Claude/GPT can understand intent from name
- Readers can skip to relevant examples

### The "Complete Concept" Principle

**Pedagogical Foundation**: Functional Completeness
- Every example must complete the path from idea → concept → working code
- No broken examples that "would work if..."
- Simplification must never break functionality

**Example**:
```pasm2
' GOOD: Simple but complete
        drvh    #56         ' LED on - works immediately

' BAD: Simple but incomplete
        add     x, #1       ' What's x? Where's initialization? What happens next?
```

### The "Progression" Pattern

**Theory Applied**: Zone of Proximal Development - Each step within reach
```markdown
Step 1: Simplest form
        add     x, #1

Step 2: Add one variation  
        add     x, y

Step 3: Add one feature
        add     x, y wc
```

### The "Success Visibility" Pattern

**Theory Applied**: Immediate feedback improves learning
```pasm2
' GOOD: Result immediately visible
        drvh    #56          ' LED turns on - you can see it!

' BAD: Result hidden in register
        mov     x, #42       ' What happened? Can't tell without debugger
```

## 💊 The Medicine Cabinet Pattern

**Pedagogical Foundation**: Differentiated Instruction (Tomlinson, 1999)
- Learners have different readiness levels
- Provide multiple paths to understanding
- Not "dumbing down" but "different door in"

### Types of Medicine

**Type 1: Minimum Viable Version**
```markdown
Feeling overwhelmed by CORDIC calculations?
Medicine: Just use MUL for now - it's good enough for most cases
```

**Type 2: Concrete Analogy**
```markdown
COGs seem confusing?
Medicine: Think of it like 8 people in a kitchen, each with their own cutting board
```

**Type 3: Just Make It Work**
```markdown
Timing calculations hurting your brain?
Medicine: Use ##25_000_000 for 0.25 seconds at 100MHz. Always works.
```

**When to Provide Medicine**:
- After introducing complex concept
- When multiple approaches exist
- Before learner frustration point (not after!)

## 🚫 Content DON'Ts

### NEVER Include Style Information
❌ "This should be in a gray box"
❌ "Make this text yellow"
❌ "Use dashed border here"
✅ Just write the content - template handles appearance

### NEVER Use LaTeX Commands
❌ `\textbf{important}`
❌ `\begin{sidetrack}`
❌ `\section{Title}`
✅ Use markdown: `**important**`, `:::sidetrack`, `## Title`

### NEVER Escape Special Characters
❌ `2\^9` 
❌ `\#define`
❌ `\_underscore`
✅ Write naturally: `2^9`, `#define`, `_underscore`

### NEVER Duplicate Box Titles
❌ 
```markdown
:::sidetrack
### Sidetrack: Philosophy
```
✅ 
```markdown
:::sidetrack
Philosophy content directly...
```

---

# PART 2: STYLE IMPLEMENTATION (What Template Does)

## 🔄 Template Evolution Protocol

**Reality**: Style requirements emerge DURING document production, not before.

### The Discovery Cycle

**Part 1 Generation:**
1. Generate content with known patterns
2. **Discover** new style need (e.g., "warning box")
3. **Mark** with generic pattern: `:::warning`
4. **Continue** generating (don't stop for style)

**Template Update:**
1. **Collect** all new patterns from Part 1
2. **Design** style for each pattern
3. **Update** template with new styles
4. **Document** in this guide

**Part 2+ Generation:**
1. Use expanded pattern set
2. Discover fewer new patterns
3. By Part 3-4, discovery usually stops
4. Template stabilizes

### Style Discovery Workflow

```markdown
CONTENT CREATION:
1. Need new visual element
2. Create semantic marker (:::newtype)
3. Document what it should convey
4. Keep writing

TEMPLATE ENHANCEMENT:
1. Find all :::newtype instances
2. Design appropriate style
3. Add to template
4. Update this guide

REGENERATION:
1. New patterns available
2. Consistent styling throughout
3. No manual style fixes needed
```

### Pattern Maturity Levels

- **Part 1**: 60-70% of patterns discovered
- **Part 2**: 85-90% of patterns discovered  
- **Part 3**: 95-99% of patterns discovered
- **Part 4+**: Template essentially complete

### Key Principle

**DON'T let style block content generation!**
- Mark semantically
- Style later
- Keep momentum

## 🎨 Visual Style Rules (AUTOMATIC)

### Color Scheme (v1.2.0 Harmonized Pastel Palette)

**5-Color Code Block System (IDE-aligned):**
- **Green** (`#EBFCEB`/`#4CB04C`): PASM2 code - most common
- **Blue** (`#E3F2FD`/`#1976D2`): Spin2 code - IDE-aligned
- **Purple** (`#F8F5FF`/`#A785C2`): CORDIC math operations
- **Teal** (`#E0F2F1`/`#00897B`): Multi-COG parallel examples
- **Red** (`#FFF5F5`/`#C08080`): Antipatterns - what NOT to do

**Pedagogical Environment Pastels:**
- **Cyan** (`#E0F7FA`/`#00ACC1`): Medicine Cabinet - distinct from PASM green
- **Amber** (`#FFF8E1`/`#F9A825`): Your Turn - warm contrast to green code
- **Lavender** (`#F3E5F5`/`#9575CD`): Sidetrack - complements PASM green
- **Orange**: Interlude, Uff! environments
- **Blue**: Chapter Summary, Well... environments

**Other Colors:**
- **Violet**: Missing content warnings
- **Orange**: Technical review needs
- **Bold only**: Inline code (no background)

### Box Styles (AUTOMATIC)
| Box Type | Background | Border | Title |
|----------|------------|--------|-------|
| `:::medicine-cabinet` | Cyan pastel | Cyan | "The Medicine Cabinet" |
| `:::your-turn` | Amber pastel | Golden | "Your Turn" |
| `:::sidetrack` | Lavender pastel | Purple | "Sidetrack" |
| `:::interlude` | Orange tint | Orange | "Interlude" |
| `:::missing` | Violet | Thick | Auto-generated |
| `:::review` | Orange | Thick | Auto-generated |

### Typography (AUTOMATIC)
- Chapter numbers: Large, bold
- Section headers: Progressive sizing
- Inline code: Bold (via `\texttt{\textbf{}}`)
- Code blocks: Monospace on yellow
- Emphasis: Italic for taglines

## 🔧 Technical Processing

### File Workflow
```
1. AUTHOR writes: Part1-WORKING.md (with markers, notes)
   ↓
2. CLEAN via: uppercase-instructions-latex.py
   ↓
3. RESULT: Part1-READY.md (clean, no markers)
   ↓
4. ESCAPE via: latex-escape-all.sh
   ↓
5. OUTPUT: Part1-ESCAPED.md (LaTeX-ready)
   ↓
6. GENERATE: PDF via pandoc + template
```

### Size Guidelines
- **Optimal part size**: 12-15KB markdown
- **Maximum part size**: 50KB markdown
- **Split points**: Natural chapter boundaries
- **Typical structure**:
  - Part 1: Chapters 1-4 (Getting Started)
  - Part 2a: Chapters 5-8 (Core Concepts)
  - Part 2b: Chapters 9-12 (Advanced Topics)
  - Part 2c: Chapters 13-16 (Expert Material)

---

# PART 3: WORKING WITH EXISTING OPUS CONTENT

## 🔍 Recognizing Opus Strengths

When reviewing Opus-generated content, preserve these natural strengths:

### What Opus Does Well Naturally
- **Transitions**: Smoothly connects chapters and concepts
- **Voice consistency**: Maintains conversational tone throughout
- **Progressive complexity**: Naturally scaffolds from simple to complex
- **Celebration moments**: Includes "Look what you've learned" sections
- **Practical examples**: Tends toward working code over theory

### Enhancement Opportunities

**Where to focus improvements:**
1. **Missing content blocks** - Fill with newly trusted P2 sources
2. **Technical accuracy** - Verify against latest P2 documentation
3. **Exercise progression** - Ensure difficulty ladder is smooth
4. **Medicine Cabinet** - Add more alternatives for complex topics
5. **Visual elements** - Mark where diagrams would help

### Regeneration Decision Framework

**Regenerate when (CONTENT changes):**
- New trusted P2 sources become available
- Technical errors discovered in core concepts
- Community feedback identifies systematic gaps
- Pedagogical improvements would significantly help

**Edit only when (STYLE changes):**
- Visual presentation issues
- Template/formatting problems
- Typography or layout fixes
- Box styling adjustments

**Critical Principle**: **Edit the opus-master in place — never the workspace render.**
`opus-master/` is canonical; the workspace copy is a regenerable artifact and an edit
made there is lost on the next assembly (see `READ-ONLY-PROTECTION.md`).

A **content** fix — a wrong claim, a stale section, a correction from an audit — is an
ordinary surgical edit to the opus-master. Regeneration is for a *structural* change:
when the chapter plan, the sources, or the guide itself changed enough that re-deriving
the chapter is cheaper and safer than patching it. Regenerating a shipped 6,000-line
manual to correct two sections is not the practice and never was.

---

# PART 4: QUALITY CHECKLIST

## ✅ Content Quality
- [ ] Follows deSilva voice (conversational, encouraging)
- [ ] Each chapter has clear Hook → Learn → Practice flow
- [ ] Code examples are complete and tested
- [ ] "Your Turn" exercises are achievable
- [ ] Medicine Cabinet provides simpler alternatives
- [ ] Common Gotchas prevent real frustrations

## ✅ Technical Quality
- [ ] No LaTeX commands in markdown
- [ ] No manual escaping of characters
- [ ] No style hints in content
- [ ] Box patterns used correctly
- [ ] File sizes within limits

## ✅ Visual Quality (After PDF Generation)
- [ ] Inline code is bold without yellow
- [ ] Code blocks have yellow background
- [ ] Special boxes show correct styling
- [ ] No duplicate titles in boxes
- [ ] Chapter numbers are sequential
- [ ] Page headers show chapter names
- [ ] Chapter/section numbering follows pedagogical pattern
- [ ] Draft warning page is professional (no emojis)
- [ ] Colored environment boxes render correctly

---

# Part 12: Document Structure & Numbering

## Pedagogical Numbering Scheme

### What We Use
- **Chapter Titles**: "Chapter 1: Your First Blink"
- **Section Numbers**: "1.1 The Hook", "1.2 Let's Build Something"
- **Depth**: Stop at section level (no 1.2.3.4 subsections)

### Why This Works
1. **Clear Learning Path**: Sequential chapters create natural progression
2. **Perfect Hierarchy**: Major concepts (chapters) with subtopics (sections)
3. **Easy Navigation**: "See section 2.3" is clearer than searching by title
4. **Not Overwhelming**: Avoids academic paper feel while maintaining structure
5. **Confidence Building**: Numbered progress gives psychological rewards
6. **Cross-Reference Friendly**: Enables quick lookups

### LaTeX Configuration
```latex
\setcounter{secnumdepth}{1}  % Number chapters and sections only
\titleformat{\chapter}
  {\normalfont\huge\bfseries}
  {\thechapter}  % Show chapter number
  {1em}          % Space between number and title
  {\Huge}
```

## Professional Draft Warning Page

### Design Principles
- **No emojis** (🚧, 🔍, 🎨) - Clean professional look
- **Clear hierarchy** - DRAFT warning, title, version, warning box
- **Red color scheme** - Immediate visual signal of draft status
- **Warning box** - Explains colored flags for incomplete sections

### Template Implementation
```latex
% Title page - Professional Draft Warning Style
{\fontsize{28}{34}\selectfont\bfseries\color{red}DRAFT - TECHNICAL REVIEW ONLY\par}
{\Large\color{red}NOT FOR RELEASE OR DISTRIBUTION\par}
```

## Technical Workflow Updates

### Markdown to PDF Pipeline
1. **Write clean markdown** using `::: sidetrack` div syntax
2. **Run LaTeX escape script** before PDF generation
3. **Use Lua filters** to convert divs to LaTeX environments
4. **Deploy to PDF Forge** with enhanced script

### Enhanced Request Format
```json
{
  "documents": [{
    "input": "document.md",
    "output": "document.pdf",
    "template": "p2kb-pasm-desilva",  // No path or extension
    "pandoc_args": [
      "--lua-filter=div-to-environment"  // No path or extension
    ],
    "variables": {
      "title": "Discovering P2 Assembly",
      "version": "0.1-DRAFT"
    }
  }]
}
```

### Key Improvements
- **Declarative requests** - No PDF Forge structure knowledge needed
- **Consistent patterns** - Templates and filters work the same way
- **Clean markdown** - Div syntax instead of raw LaTeX
- **Proper escaping** - Automated handling of LaTeX special characters

---

# APPENDIX: Common Issues & Solutions

## Issue: Box Title Duplication
**Problem**: "Sidetrack: Sidetrack: Content"
**Cause**: Adding title inside box content
**Solution**: Let template add the title

## Issue: Yellow Inline Code
**Problem**: Inline code has yellow background
**Cause**: Wrong template command
**Solution**: Use `\texttt{\textbf{}}` not `\colorbox`

## Issue: Escaped Characters in Output
**Problem**: Seeing `\^` instead of `^`
**Cause**: Manual escaping or double-escaping
**Solution**: Write naturally, let script escape once

## Issue: Missing Content Not Visible
**Problem**: Missing sections blend into text
**Cause**: Not using `:::missing` pattern
**Solution**: Always mark missing content explicitly

---

## 🧗 Living Document Protocol

This creation guide follows Technical Climbing Methodology:

### Protection Points (What This Guide Preserves)
- ✅ Successful patterns from each generation
- ✅ Pedagogical approaches that work
- ✅ Voice elements that resonate
- ✅ Technical accuracy methods

### Climbing Higher (How This Guide Improves)
- 📝 Each use reveals new patterns → Document them here
- 🔍 Each review finds gaps → Add to technical-debt.md
- 📚 Each new P2 source → Update content requirements
- 🎯 Each generation → Refine the guide itself

### Using This Guide for Next Generation

**Before regenerating:**
1. Review technical-debt.md for accumulated improvements
2. Check for new trusted P2 sources to incorporate
3. Update this guide with lessons from current generation
4. Set clear goals for what should improve

**During generation:**
- Add metadata comment to document:
  ```markdown
  <!-- Generated with creation-guide v2025-08-23 -->
  <!-- P2 Trust Level: 80% coverage -->
  ```

**After regenerating:**
1. Compare to previous generation (did we climb higher?)
2. Document what worked better
3. Note what still needs improvement
4. Update this guide with new insights
5. Tag release if significant content change

**Remember**: This guide is a piton - it prevents regression while enabling progress.

---

## Version History

### 2025-08-23 - Technical Climbing Integration
- Added regeneration cycles section
- Created "Working with Existing Opus Content" section
- Integrated 4-facet P2KB context
- Added living document protocol

### 2025-08-23 - Pedagogical Foundation Integration
- Added learning theory citations for each pattern
- Created theory-informed code example principles
- Expanded Medicine Cabinet with differentiation theory
- Restructured for Claude Opus generation optimization

### 2025-08-23 - Major Reorganization
- Separated content creation from style implementation
- Added clear DON'T rules with examples
- Created comprehensive quality checklist
- Added common issues appendix

### 2025-08-21 - Initial Creation
- Documented template/markdown boundary
- Established yellow background rule
- Defined special box patterns