# PASM2 Instruction Spreadsheet Style Guide

## Document Type
**Reference Spreadsheet** - Chip Gracey's authoritative instruction set documentation

## Core Style Characteristics

### 1. Architecture & Structure
- **Categorical Organization**: Instructions grouped by functional purpose (10+ major categories)
- **Statistical Headers**: Each section begins with counts (e.g., "115+ instructions")
- **Progressive Disclosure**: Category → Subcategory → Instruction list → Details
- **Enumeration Pattern**: Numbered sections with named subsections

### 2. Content Patterns

#### Instruction Presentation
```
**Subcategory**: INSTRUCTION1, INSTRUCTION2, INSTRUCTION3
```
- **Bold subcategory labels** followed by colon
- Instruction names in UPPERCASE
- Comma-separated lists for related instructions
- No descriptions at list level (pure reference)

#### Categorical Grouping Logic
1. **Functional Cohesion**: Instructions grouped by what they do, not how they're encoded
2. **Pattern Families**: Related operations listed together (e.g., DIRL, DIRH, DIRC, DIRNC...)
3. **Hardware Mapping**: Categories align with P2 hardware units (Smart Pins, CORDIC, etc.)

### 3. Voice & Tone

#### Authority Without Explanation
- **Assumes Knowledge**: No "what is" or "why" - pure "what exists"
- **Designer's Perspective**: Organization reflects hardware architecture thinking
- **Zero Tutorial Content**: Reference-only, no learning path

#### Precision Over Accessibility
- **Technical Accuracy**: Every detail matters (bit positions, cycle counts)
- **No Simplification**: Complex concepts presented as-is
- **Completeness**: Every instruction variant listed

### 4. Micro-Patterns

#### Visual Encoding Diagrams
```
EEEE OOOOOOO CZI DDDDDDDDD SSSSSSSSS
│    │       │││ │         │
│    │       │││ │         └─ 9-bit Source
│    │       │││ └─────────── 9-bit Destination
```
- Box-drawing characters for structure
- Right-aligned descriptions with └─ connectors
- Bit field labels above, explanations below
- Visual hierarchy through alignment

#### Numeric Specifications
- **Exact Counts**: "491 entries (365 core instructions + aliases/variants)"
- **Bit Widths**: Always specified (32-bit, 9-bit, etc.)
- **Address Ranges**: Hex notation with explicit ranges ($000-$1FF)
- **Parenthetical Details**: Core info + (clarification)

#### Naming Conventions
- **UPPERCASE**: All instruction mnemonics
- **Mixed Notation**: Hex ($1FF), decimal (512), binary when relevant
- **Suffix Patterns**: Direction (L/H), condition (C/NC/Z/NZ), operation (RND/NOT)
- **Numbered Series**: SE1-4, CT1-3, INT1-3

### 5. Information Density

#### Maximum Information, Minimum Words
- Lists over prose
- Tables over paragraphs  
- Patterns over repetition
- Structure conveys meaning

#### Systematic Completeness
- Every category enumerated
- Every variant listed
- Every bit field documented
- Nothing left implicit

### 6. Reference Optimizations

#### Quick Scanning
- **Bold Headers**: Visual anchors for navigation
- **Bullet Lists**: Fast enumeration of options
- **Consistent Format**: Same structure throughout
- **Category Counts**: Size indicators (60+ instructions)

#### Cross-Reference Preparation
- Categories set up for linking
- Instruction names ready for indexing
- Bit patterns ready for encoding tables
- Groups ready for relationship mapping

## Style Application Guidelines

### When to Use This Style
- Instruction set references
- Register maps
- Bit field documentation  
- Hardware feature enumerations
- Complete API listings

### When NOT to Use This Style
- Learning materials
- Conceptual explanations
- Tutorial content
- Migration guides
- Best practices documentation

## Extraction Metadata
- **Source**: P2 Instructions v35 - Rev B/C Silicon spreadsheet
- **Author Style**: Chip Gracey (P2 designer)
- **Document Purpose**: Authoritative instruction reference
- **Audience**: Assembler writers, compiler developers, expert users

## Key Differentiators from Other Styles

### vs. Silicon Doc (Parallax Official)
- Spreadsheet: Pure enumeration
- Silicon: Adds context and explanation

### vs. DeSilva Tutorial
- Spreadsheet: Reference without teaching
- DeSilva: Teaching through exploration

### vs. SmartPins Doc (Jon Titus)
- Spreadsheet: Complete listing
- Titus: Practical examples and use cases

## Implementation Notes

When replicating this style:
1. Start with complete enumeration
2. Organize by functional categories
3. Use consistent naming patterns
4. Provide visual structure diagrams
5. Include exact specifications
6. Avoid explanatory text
7. Maximize information density
8. Optimize for scanning and lookup

This style serves as the **authoritative reference backbone** that other documentation styles build upon.