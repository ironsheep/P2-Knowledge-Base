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

### Sidetrack (Gray with Dashed Border)
**Purpose:** Technical specifications, architecture details, implementation notes
**Visual:** Gray background (`F5F5F5`) with dashed border
**Title:** Always has bold title describing the sidetrack topic

Examples:
- "Why Pin 16?" - explaining safe pin choices
- "Cog Resources at a Glance" - specifications
- "Why 512 Longs?" - architecture decisions

### Interlude (Gray, No Border)
**Purpose:** Conceptual bridges, philosophical insights, "aha moments"
**Visual:** Gray background (`F5F5F5`), no border
**Title:** Bold title (optional), regular body text

Examples:
- "The Beauty of Deterministic Timing" - conceptual insight
- "Parallel Thinking" - philosophy behind the architecture
- Bridging paragraphs between major concepts

### Your Turn (Light Blue)
**Purpose:** Exercises, challenges, experimentation prompts
**Visual:** Light blue background (`E6F3FF`)
**Title:** "Your Turn" followed by challenge descriptions

The blue color is intentionally distinct from yellow code blocks to signal "shift from reading to doing."

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

### Color Assignments
- **Yellow (`FFFACD`)**: Active code, immediate attention
- **Blue (`E6F3FF`)**: Your turn to practice, exploration
- **Gray (`F5F5F5`)**: Supplemental information, asides
- **Green (`F0FFF0`)**: Success, completion, moving forward
- **Orange (`FFE4B5`)**: Attention needed, review required
- **Violet (`E6E6FA`)**: Missing, incomplete
- **Sky Blue (`E0F2FF`)**: Visual/diagram placeholder

### Visual Flow
1. **Main text** (white) → primary learning path
2. **Code blocks** (yellow) → examples to study
3. **Sidetracks** (gray/dashed) → optional deep dives
4. **Your Turn** (blue) → active practice
5. **Chapter End** (green) → celebration and transition

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