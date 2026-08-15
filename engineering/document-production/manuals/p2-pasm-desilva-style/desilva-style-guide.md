# deSilva Style Guide - P2KB PASM Manual Configuration

## Document Purpose
This guide captures all pedagogical and formatting decisions for the P2 PASM manual in deSilva style, ensuring consistency across all chapters and future updates.

## Core Pedagogical Principles

### 1. Visual Consistency Creates Cognitive Clarity
- Every formatting choice should reduce cognitive load
- Inconsistency forces readers to wonder "why?" instead of learning "what"
- Patterns should be absolute with no exceptions that confuse

### 2. deSilva's Legacy, Enhanced
- We honor deSilva's conversational, encouraging tone
- We improve upon his occasional inconsistencies
- We maintain his "learn by doing" philosophy

## Instruction Mnemonic Formatting

### ABSOLUTE RULE: Always UPPERCASE + BOLD
**Every PASM2 instruction mnemonic appears as UPPERCASE + BOLD everywhere:**

- ✅ In prose text: "The **MOV** instruction copies values"
- ✅ In explanations: "Use **WAITX** for precise timing"
- ✅ In code blocks: `**MOV** pa, #5` (even though case-insensitive)
- ✅ In boxes: All instructions shown as **DRVH**, **DRVL**, etc.
- ✅ In inline refs: "parameters for **WAITX**"

**Rationale:** PASM2 is case-insensitive, so we optimize for learning. The bold uppercase creates instant recognition: "This is a COMMAND with POWER."

### Spin Method Names
- Always lowercase: `getct()`, `cogstart()`, `wrpin()`
- Not bolded (they're methods, not processor instructions)

## Box Types and Their Purposes

### Sidetrack (Lavender Pastel)
**Purpose:** Technical specifications, architecture details, implementation notes
**Visual:** Lavender background (`#F3E5F5`) with soft purple border (`#9575CD`)
**Title:** Always has bold title describing the sidetrack topic
**Color rationale:** Purple complements PASM green (opposite on color wheel)

Examples:
- "Why Pin 16?" - explaining safe pin choices
- "Cog Resources at a Glance" - specifications
- "Why 512 Longs?" - architecture decisions

### Medicine Cabinet (Tan/Beige)
**Purpose:** Simpler alternatives when learner feels overwhelmed
**Visual:** Warm cream background (`#FFF8F0`) with tan border (`#D2A679`)
**Title:** "The Medicine Cabinet"
**Color rationale:** Band-aid association for "remedy/help" semantic; distinct from all code block colors

### Interlude (Gray, No Border)
**Purpose:** Conceptual bridges, philosophical insights, "aha moments"
**Visual:** Gray background (`F5F5F5`), no border
**Title:** Bold title (optional), regular body text

Examples:
- "The Beauty of Deterministic Timing" - conceptual insight
- "Parallel Thinking" - philosophy behind the architecture
- Bridging paragraphs between major concepts

### Your Turn (Amber/Gold Pastel)
**Purpose:** Exercises, challenges, experimentation prompts
**Visual:** Cream background (`#FFF8E1`) with golden amber border (`#F9A825`)
**Title:** "Your Turn" followed by challenge descriptions

The warm amber color contrasts with cool green PASM code blocks, signaling "shift from reading to doing." Previously green, changed to avoid green-on-green conflict when containing PASM code.

### Missing Content (Lavender)
**Purpose:** Placeholder for content to be added
**Visual:** Lavender background (`E6E6FA`), thick violet border
**Title:** Generated from markdown content (not template)

### Review Needed (Peach/Orange)
**Purpose:** Content requiring technical review
**Visual:** Peach background (`FFE4B5`), thick orange border
**Title:** Generated from markdown content (not template)

### Diagram Needed (Sky Blue)
**Purpose:** Placeholder for diagrams/visuals
**Visual:** Sky blue background (`E0F2FF`), thick blue border
**Title:** Generated from markdown content (not template)

### Chapter End (Light Green)
**Purpose:** Chapter summary and preview of next chapter
**Visual:** Light green background (`F0FFF0`), no border
**Features:** 
- Celebration message (what you accomplished)
- Gray separator line (inside box)
- Preview of next chapter
- NO ITALICS on instructions

## Color Psychology and Visual Hierarchy

### Color Assignments (v1.2.0 Harmonized Pastel Palette)

**Code Blocks (IDE-aligned, brighter accents):**
- **Green** (`#EBFCEB`/`#4CB04C`): PASM2 code - most common
- **Blue** (`#E3F2FD`/`#1976D2`): Spin2 code - IDE-aligned
- **Purple** (`#F8F5FF`/`#A785C2`): CORDIC math operations
- **Teal** (`#E0F2F1`/`#00897B`): Multi-cog parallel examples
- **Red** (`#FFEBEE`/`#E53935`): Antipatterns - what NOT to do (unmistakable warning)

**Pedagogical Containers (softer pastels, don't compete with code):**
- **Tan/Beige** (`#FFF8F0`/`#D2A679`): Medicine Cabinet - band-aid association for "remedy"
- **Amber** (`#FFF8E1`/`#F9A825`): Your Turn - warm contrast to green code
- **Lavender** (`#F3E5F5`/`#9575CD`): Sidetrack - complements PASM green
- **Orange**: Interlude, Uff! environments
- **Green** (`F0FFF0`): Chapter End - success, completion

**Status/Placeholder Colors:**
- **Orange (`FFE4B5`)**: Attention needed, review required
- **Violet (`E6E6FA`)**: Missing, incomplete
- **Sky Blue (`E0F2FF`)**: Visual/diagram placeholder

### Visual Flow
1. **Main text** (white) → primary learning path
2. **Code blocks** (green/blue/purple) → examples to study (brighter accents)
3. **Sidetracks** (lavender) → optional deep dives (soft container)
4. **Your Turn** (amber) → active practice (warm call to action)
5. **Medicine Cabinet** (tan) → simpler alternatives (remedy/help)
6. **Chapter End** (green) → celebration and transition

## Code Block Formatting

### PASM2 Code Blocks
```pasm2
label   **MOV**     pa, #5          ' Instructions UPPERCASE + BOLD
        **ADD**     pa, pb          ' Operands normal
        **WAITX**   ##25_000_000    ' Comments in gray italic
        **JMP**     #label          ' Labels normal
```

### Key Elements
- Instructions: **UPPERCASE + BOLD**
- Labels: Regular text (not bolded)
- Operands: Regular text with proper P2 syntax (#, ##, etc.)
- Comments: Gray italic
- Background: **ALWAYS Yellow (`FFFACD`)** - even inside colored boxes!

### Code Block Color Consistency Rule
**Code blocks maintain yellow background EVERYWHERE:**
- Inside white main text → yellow code blocks
- Inside gray sidetracks → yellow code blocks
- Inside green chapter ends → yellow code blocks
- Inside blue Your Turn boxes → yellow code blocks

**Rationale:** "Yellow = Code" is a universal truth in the document. This visual consistency reduces cognitive load and maintains hierarchy (code is primary content, not subordinate to its container).

## Typography Rules

### Immediate Values and P2 Syntax
- `#` for immediate values (9-bit max)
- `##` for 32-bit immediate values
- `_` in numbers for readability: `25_000_000`
- Never escape these in code contexts

### Text Styling
- **Bold**: Instructions, important concepts, box titles
- *Italic*: Comments in code, emphasis in prose
- `Monospace`: Code, values, pin numbers, register names
- Never combine italic + bold for instructions

## Escaping Rules

### Context-Aware Escaping
The LaTeX escaping script must:
1. **Protect inline code** between backticks
2. **Protect code blocks** (triple backticks)
3. **Preserve P2 syntax** (#, ##, _, %, etc.)
4. **Escape normally** in regular prose

### Special P2 Patterns to Preserve
- `#16` - immediate value
- `##25_000_000` - 32-bit immediate
- `#%01_00` - binary with separators
- `$1F6` - hex addresses
- `@label` - address references

## Document Structure

### Chapter Organization
1. **Hook** - Engaging opening that motivates learning
2. **Concept Introduction** - What we're building
3. **Code Example** - Immediate hands-on
4. **Explanation** - Line-by-line understanding
5. **Deeper Concepts** - Advanced understanding
6. **Common Mistakes** - Learning from errors
7. **Your Turn** - Practice challenges
8. **Chapter End** - Celebration and preview

### Pedagogical Flow
- Start with success (working code)
- Build understanding incrementally
- Acknowledge mistakes as learning
- Celebrate progress explicitly
- Connect to next concept

## Writing Voice

> **Reference, never restate.** The manual's position on the four house voice rules
> (R1 calibrated confidence · R2 the payoff-sentence test · R3 the anti-pattern family ·
> R4 cadence budget) is declared in **`voice-guide.md`**, and the rules themselves are
> stated in `engineering/standards/documentation-standards/documentation-voices-catalog.md`.
> **This file remains the source of truth for FORMATTING.** The style notes below are the
> presentational face of the voice; they are not the voice rules and must not grow into a
> second copy of them.

### deSilva's Conversational Style
- Direct address: "You'll discover..."
- Encouragement: "You've got this!"
- Metaphors: "Eight cogs like eight musicians"
- No condescension: Respect reader intelligence
- Acknowledge complexity: "This is tricky, and that's okay"

### Avoiding Jargon Walls
- Introduce terms gradually
- Use analogies for complex concepts
- Define in context, not dictionary-style
- Show before explaining

## Version Control and Updates

### When to Update This Guide
- New box type introduced
- Color changes for clarity
- Formatting rule changes
- Pedagogical pattern discoveries

### Change Log
- 2025-08-21: Initial guide created
- 2025-08-21: Established UPPERCASE + BOLD rule for all mnemonics
- 2025-08-21: Changed Your Turn color from FFF8DC to E6F3FF
- 2025-08-21: Defined interlude vs sidetrack distinction
- 2025-12-12: v1.2.0 Harmonized Pastel Palette
  - Your Turn: Changed from blue to amber/gold (#FFF8E1/#F9A825) - eliminates green-on-green
  - Medicine Cabinet: Changed from teal to cyan (#E0F7FA/#00ACC1) - distinct from PASM green
  - Sidetrack: Softened to lavender (#F3E5F5/#9575CD) - complements PASM green
  - Added 5-color code block system documentation (IDE-aligned)

## Quick Reference Checklist

Before generating PDF:
- [ ] All mnemonics **UPPERCASE + BOLD** everywhere?
- [ ] Code blocks have yellow background?
- [ ] Your Turn boxes light blue (not yellow)?
- [ ] Sidetracks have dashed borders?
- [ ] Interludes have no borders?
- [ ] Chapter ends have no italics?
- [ ] P2 syntax preserved (# and _ not escaped)?
- [ ] Instructions never italic?
- [ ] Box titles not duplicated?

## Examples of Correct Formatting

### Prose Text
"The **MOV** instruction copies a value from source to destination. Unlike **ADD** which modifies the destination, **MOV** replaces it entirely."

### Code Block
```pasm2
loop    **MOV**     pa, #0          ' Initialize counter
        **ADD**     pa, #1          ' Increment
        **CMP**     pa, #100 wz     ' Check limit
  if_nz **JMP**     #loop          ' Continue if not zero
```

### Your Turn Box
\begin{yourturn}
**Challenge 1:** Make the LED blink twice as fast
**Challenge 2:** Add a second LED on pin 17
\end{yourturn}

### Sidetrack Box
\begin{sidetrack}
**Why 8 Cogs?**
Eight provides enough parallelism for most applications while keeping the hub arbitration simple...
\end{sidetrack}

---

*This guide is the single source of truth for P2KB PASM manual formatting decisions.*