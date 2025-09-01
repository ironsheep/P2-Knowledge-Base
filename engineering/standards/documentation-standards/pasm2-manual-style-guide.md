# PASM2 Manual Style Guide

## Document Type
**Technical Reference Manual** - Parallax's authoritative PASM2 instruction documentation

## Core Style Characteristics

### 1. Architecture & Structure

#### Document Organization
- **Three-tier Structure**: Introduction → Instruction Categories → Alphabetical Reference
- **Reference-oriented Design**: Random access, not sequential reading
- **Fixed Template Adherence**: Every instruction follows identical format
- **Appendix Strategy**: Special topics isolated from main reference

#### Section Hierarchy
```
### INSTRUCTION_NAME
**Syntax:**
**Encoding:**
**Description:**
**Flags:**
**Timing:**
**See Also:**
```

### 2. Content Patterns

#### Information Architecture
- **High Density**: Maximum information, minimum words
- **Standalone Entries**: Each instruction self-contained
- **No Progressive Disclosure**: Flat complexity throughout
- **Zero Tutorial Content**: Pure reference, no learning path

#### Fixed Field Order
1. Instruction name as heading
2. Syntax notation
3. Binary encoding pattern
4. Technical description (2-3 sentences)
5. Flag effects
6. Timing specification
7. Cross-references

### 3. Voice & Tone

#### Third Person Passive
- "The instruction performs..." not "This performs..."
- "The result is written..." not "Write the result..."
- Never "you" or "we"
- No imperatives or commands

#### Professional Technical
- **Formality**: 9/10 - Highly technical
- **Assumed Knowledge**: Assembly programming expertise
- **No Explanations**: Technical terms used without definition
- **Precision Over Clarity**: Accuracy trumps accessibility

### 4. Micro-Patterns

#### Description Formula
```
[Subject] [action] [object] {[condition]}.
[Secondary effect] {[when clause]}.
```
- 20-50 words typical
- 2-3 sentences maximum
- Technical terms comprise 40% of words

#### Flag Documentation
```
C: [Subject] [becomes/is] [state/value]
Z: [Subject] [becomes/is] [state/value]
```
- Single line per flag
- 5-15 words each
- Even if "unaffected"

#### Encoding Presentation
```
EEEE OOOOOOO CZI DDDDDDDDD SSSSSSSSS
```
- Always shown
- Fixed-width font
- Bit positions explicit
- No simplification

### 5. Terminology Conventions

#### Consistent Technical Terms
- **D**: Destination register
- **S**: Source register/immediate
- **C**: Carry flag
- **Z**: Zero flag
- **cog**: Never COG or Cog
- **hub**: Never Hub or HUB

#### Notation Standards
- `{#}` for optional immediate
- `{,{#}D}` for optional destination
- `WC,WZ,WCZ` for flag options
- `$` prefix for hexadecimal
- `%` prefix for binary
- No prefix for decimal

### 6. Style Rules

#### Mandatory Elements
1. **Always show encoding** - Even if complex
2. **All fields present** - Even if "N/A"
3. **Exact field order** - Never vary
4. **Technical accuracy** - Never simplify
5. **Passive voice** - Throughout

#### Prohibited Elements
- ❌ Usage examples in entries
- ❌ Conceptual explanations
- ❌ Learning progressions
- ❌ Casual language
- ❌ First/second person
- ❌ Undefined terms inline

## Style Metrics

### Quantifiable Elements
- **Description Length**: 20-50 words (avg 35)
- **Sentences per Entry**: 2-3
- **Technical Term Density**: 40%
- **Cross-references**: 0-3 per instruction
- **Flag Descriptions**: 5-15 words
- **Timing Specs**: 3-10 words

### Consistency Targets
- Format Match: 100%
- Terminology: 100%
- Field Order: 100%
- Voice Consistency: 100%

## Example Application

### Correct Style:
```markdown
### ADD

**Syntax:**
ADD {#}S,{#}D {WC,WZ,WCZ}

**Encoding:**
EEEE 1000000 CZI DDDDDDDDD SSSSSSSSS

**Description:**
Adds S to D and writes the result to D. The operation treats
both operands as unsigned 32-bit values.

**Flags:**
C: Set if unsigned overflow occurs
Z: Set if result equals zero

**Timing:**
2 clocks

**See Also:**
ADDS, ADDX, SUB
```

### Style Violations:
- ❌ "You can use ADD to..." (second person)
- ❌ "This is useful for..." (tutorial content)
- ❌ Including code examples
- ❌ Explaining what overflow means
- ❌ Varying the field order

## Extraction Metadata
- **Source**: P2-Assembly-Language-PASM2-Manual-Draft (partial)
- **Author Style**: Parallax technical documentation team
- **Document Purpose**: Authoritative instruction reference
- **Audience**: Expert assembly programmers

## Key Differentiators from Other Styles

### vs. Spreadsheet (Chip Gracey)
- Manual: Adds descriptions and cross-references
- Spreadsheet: Pure enumeration

### vs. Silicon Doc
- Manual: Instruction-focused
- Silicon: Architecture-focused

### vs. DeSilva Tutorial
- Manual: Reference without teaching
- DeSilva: Teaching through examples

### vs. SmartPins Doc (Titus)
- Manual: Template consistency
- Titus: Progressive examples

## Implementation Guidelines

When extending the PASM2 manual:
1. **Never deviate** from the template
2. **Match existing terminology** exactly
3. **Maintain formality level** consistently
4. **Preserve field order** rigidly
5. **Keep descriptions terse** (under 50 words)
6. **Use passive voice** throughout
7. **Avoid any teaching** elements

This style serves as the **definitive reference standard** for PASM2 instruction documentation.