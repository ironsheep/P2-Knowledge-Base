# PASM2 Manual Style Extraction Plan

**Purpose**: Extract and codify the Parallax documentation style from existing partial manual
**Source**: P2-Assembly-Language-PASM2-Manual-Draft-221117.pdf (9174 lines)

---

## 📊 Style Analysis Framework Application

### Level 1: Document Architecture
- **Overall Structure**: 
  - Introduction → Instruction Categories → Alphabetical Reference
  - Appendices for special topics (conditions, flags, addressing)
- **Section Hierarchy**: 
  - Major sections with ### headings
  - Instructions as subsections
  - Consistent depth throughout
- **Flow Pattern**: 
  - Reference-oriented, not tutorial
  - Random access design
  - Category groupings with alphabetical fallback
- **Navigation Aids**: 
  - Table of contents
  - Category listings
  - "See Also" cross-references

### Level 2: Content Patterns
- **Information Density**: 
  - High - assumes assembly programming knowledge
  - Terse descriptions, maximum information
- **Example Strategy**: 
  - Minimal examples in v1.0
  - Syntax examples only, not usage examples
- **Visual Elements**: 
  - Encoding bit pattern tables
  - Flag effect tables
  - No diagrams in instruction entries
- **Progressive Disclosure**: 
  - Flat - each instruction standalone
  - No complexity progression

### Level 3: Voice & Tone
- **Perspective**: 
  - Third person passive ("The instruction performs...")
  - Never first or second person
- **Formality Level**: 
  - 9/10 - Highly technical, professional
  - No colloquialisms or casual language
- **Audience Assumptions**: 
  - Experienced assembly programmers
  - Familiar with processor architecture
  - Understanding of binary/hex notation
- **Instruction Style**: 
  - Descriptive, not prescriptive
  - States what happens, not what to do

### Level 4: Micro-patterns
- **Sentence Structure**: 
  - Short, declarative sentences
  - Average 10-15 words
  - Subject-verb-object predominant
- **Terminology Usage**: 
  - Defined in introduction
  - Used consistently throughout
  - Technical terms not explained inline
- **Emphasis Techniques**: 
  - **Bold** for section headers and keywords
  - `Monospace` for instruction names and code
  - No italics, no CAPS for emphasis
- **Warning/Note Style**: 
  - "Note:" prefix for important points
  - Set apart from main text
  - Minimal use, only when critical

---

## 🎨 Extracted Style Template

### Instruction Entry Template:
```markdown
### INSTRUCTION_NAME

**Syntax:**
INSTRUCTION_NAME [{#}]S{,{#}D}

**Encoding:**
EEEE OOOOOOO CZI DDDDDDDDD SSSSSSSSS

**Description:**
[Single paragraph, 2-3 sentences maximum. State what the instruction 
does in technical terms. Use passive voice. Reference register names 
and flags precisely.]

**Flags:**
C: [Effect on C flag, one line]
Z: [Effect on Z flag, one line]

**Timing:**
[Number] clock(s) [conditions if applicable]

**See Also:**
[Related instructions, comma-separated]
```

### Distinctive Features:
1. **Bit-level precision** in encoding descriptions
2. **Fixed information order** (never varies)
3. **Minimal prose** between data elements
4. **Technical accuracy** over readability
5. **Consistent field presence** (all fields always shown)

---

## 📋 Style Extraction Checklist

### From Existing Manual, Extract:
- [x] Section organization pattern
- [x] Instruction entry format
- [x] Terminology conventions
- [x] Cross-reference style
- [x] Flag description format
- [x] Timing notation style
- [x] Encoding presentation format
- [ ] Introduction writing style
- [ ] Category description style
- [ ] Appendix format

### Style Rules to Document:
1. **Never use examples** in instruction entries (v1.0)
2. **Always show encoding** even if complex
3. **Maintain exact field order** in every entry
4. **Use technical terms** without explanation
5. **Keep descriptions under 50 words**
6. **Reference other instructions** in "See Also"
7. **State flag effects** even if "unaffected"

---

## 🔄 Application Strategy

### When Extending the Manual:

1. **For Missing Instructions**:
   - Apply template exactly
   - No creative deviation
   - Match terminology from existing entries
   - Maintain same description depth

2. **For Incomplete Entries**:
   - Preserve existing content
   - Add missing fields in correct position
   - Match style of surrounding entries
   - Don't improve, just complete

3. **For Consistency Issues**:
   - Existing manual style wins
   - Fix only obvious errors
   - Document inconsistencies separately
   - Maintain original author's voice

---

## ✅ Style Validation Criteria

### Every New Entry Must:
- [ ] Match exact formatting of existing entries
- [ ] Use same terminology as established
- [ ] Maintain same level of detail
- [ ] Follow field order precisely
- [ ] Have all required fields present
- [ ] Use passive voice consistently
- [ ] Avoid any tutorial elements

### Red Flags (Style Violations):
- ❌ Using "you" or "we" anywhere
- ❌ Adding usage examples
- ❌ Explaining basic concepts
- ❌ Varying field order
- ❌ Inconsistent terminology
- ❌ Different formatting style
- ❌ Tutorial-style explanations

---

## 📊 Style Metrics

### Quantifiable Style Elements:
- **Description length**: 20-50 words typical
- **Sentence count**: 2-3 per description
- **Technical term density**: 40% of words
- **Cross-references**: 0-3 per instruction
- **Flag descriptions**: 5-15 words each
- **Timing description**: 3-10 words

### Style Consistency Score:
Track for each new entry:
- Formatting match: 0-100%
- Terminology consistency: 0-100%
- Field completeness: 0-100%
- Style adherence: 0-100%

Target: 95%+ on all metrics

---

*This style extraction ensures seamless extension of the PASM2 manual*