# SmartPins Documentation Style Guide

**Source Document**: P2 SmartPins-220809.pdf / smartpins-text.txt
**Author**: Jon Titus
**Document Type**: Technical Reference with Tutorial Elements

---

## 📊 Style Analysis

### Document Architecture
- **Structure**: Feature-based organization (not alphabetical)
- **Hierarchy**: Topic → Concept → Instructions → Examples
- **Flow**: Progressive from basic I/O to complex Smart Pin modes
- **Navigation**: Section headers with clear topic boundaries

### Content Patterns
- **Density**: Moderate - balances technical detail with explanation
- **Examples**: Integrated throughout, showing actual usage
- **Visuals**: Schematic diagrams mentioned (ExpressPCB)
- **Progression**: Basic pins → Smart Pin modes → Complex applications

### Voice & Tone
- **Perspective**: Mix of second person ("you") and technical description
- **Formality**: 6/10 - Technical but conversational
- **Audience**: Experienced programmers new to P2
- **Instructions**: Direct and practical ("Software can wait in a loop...")

### Micro-patterns
- **Sentences**: Moderate length, 15-20 words average
- **Terminology**: Defined inline with practical context
- **Emphasis**: Uses CAPS for register names, quotes for specifics
- **Alerts**: "Notes to writers" shows work-in-progress nature

---

## 🎨 Distinctive Features

### 1. **Practical Orientation**
- Focuses on "how to use" not just "what it is"
- Shows real code patterns
- Addresses common questions inline

### 2. **Progressive Disclosure**
```
Basic I/O pins → Pin groups → Smart Pin introduction → Mode details
```

### 3. **Instruction Groupings**
Groups related instructions together:
```
Pin-Direction Instructions
DIRL    {#}D    Set direction bit(s) to logic 0 (input)
DIRH    {#}D    Set direction bit(s) to logic 1 (output)
[etc...]
```

### 4. **Inline Examples**
```
Example: DIRL #20 'Set P20 as an input pin
```

### 5. **Author's Questions**
Shows areas needing clarification:
- "Should the docs say that, or just mention RDPIN?"
- Highlights ambiguities for resolution

---

## 📋 Replication Guidelines

### To Write in SmartPins Style:

#### 1. Start with Context
```markdown
The basic unit measure of time is the period of the system-clock frequency...
```

#### 2. Group Related Instructions
```markdown
### [Function] Instructions
INSTRUCTION1  {params}  Description
INSTRUCTION2  {params}  Description
Example: [immediate usage example]
```

#### 3. Use Progressive Examples
```markdown
Simple case:
DRVH #8           'Drive P8 high

Advanced case:
DRVH #10 ADDPINS 7  'Drive P10..P17 high
```

#### 4. Address Practical Concerns
- What the programmer needs to know
- Common pitfalls
- When to use which variant

#### 5. Mixed Technical Levels
- Register-level details for precision
- Conceptual explanations for understanding
- Usage patterns for implementation

---

## 📊 Style Metrics

### Quantifiable Elements:
- **Instruction entries**: Name, syntax, description, example
- **Example frequency**: 1 per instruction group minimum
- **Explanation depth**: 2-3 sentences per concept
- **Code comments**: Always present and meaningful

### Information Order:
1. Concept introduction
2. Related instructions table
3. Parameter explanation
4. Usage example
5. Special notes/warnings

---

## ✅ When to Use This Style

### Best For:
- Feature-focused documentation
- Progressive learning materials
- Practical implementation guides
- Mixed audience (learning + reference)

### Not Ideal For:
- Pure reference documentation
- Quick lookup guides
- Theoretical explanations

---

## 🔄 SmartPins vs Other Styles

### vs Silicon Doc:
- SmartPins: More examples, more explanation
- Silicon: More terse, more precise

### vs PASM2 Manual:
- SmartPins: Feature-grouped, practical
- PASM2: Alphabetical, comprehensive

### vs DeSilva:
- SmartPins: Technical with examples
- DeSilva: Tutorial with progression

---

## 📝 Key Takeaways for PASM2 Manual

From SmartPins style, consider adopting:
1. **Instruction grouping** by function (not just alphabetical)
2. **Inline examples** immediately after instruction definition
3. **Practical notes** about usage patterns
4. **Progressive complexity** in examples
5. **Author questions** to identify gaps (during development)

---

*This style guide captures Jon Titus's practical, example-rich approach to technical documentation*