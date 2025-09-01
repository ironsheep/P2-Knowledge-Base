# Marketing Document Style Guide

*Based on analysis of P2 Spec Sheet and Datasheet*

---

## 📊 Document Type Differentiation

### Spec Sheet Style (Marketing-Oriented)
**Purpose**: Quick evaluation and decision support
**Audience**: Technical decision makers, evaluators
**Length**: 1-2 pages maximum
**Focus**: Capabilities and benefits

### Datasheet Style (Technical Reference)
**Purpose**: Implementation guidance
**Audience**: Design engineers
**Length**: 10+ pages comprehensive
**Focus**: Specifications and details

---

## 🎯 Spec Sheet Style Template

### Structure:
```markdown
# [Product Name] Spec Sheet

[2-3 sentence positioning paragraph - performance claims, key differentiators, target applications]

[1 sentence about ecosystem/development environment benefits]

## Selected Specifications
● [Core count] processors @ [speed]
● [Memory size] of [type]
● [I/O count] with [capability]
● [Power specs]
● [Temperature range]

## Physical Characteristics
● Package: [type and dimensions]
● Temperature: [range with standard]
● Moisture: [MSL rating]

## Compliance
● [Standard]: [Number]
● [Standard]: [Number]

## Hardware Function Highlights
● [Feature Category]: [Impressive quantity/capability]
● [Feature Category]: [Multiple options listed]
● [Protocol Support]: [List of protocols]

[Website and contact information]
```

### Writing Rules:

1. **Lead with value proposition**
   - Compare to known technologies (FPGA, MPU)
   - Emphasize time/cost savings
   - Highlight unique capabilities

2. **Use "Selected Specifications"**
   - Cherry-pick impressive numbers
   - Round to memorable values
   - Group related features

3. **Maximize perceived capability**
   - List all supported protocols
   - Show breadth of features
   - Use quantity multipliers (64x, 8x)

4. **Simplify technical concepts**
   - "Smart I/Os" not "configurable pin modes"
   - "Shared RAM" not detailed memory architecture
   - Remove addressing complexity

5. **Include disclaimer for protocols**
   - "For R&D only" caveat
   - User licensing responsibility

---

## 🎨 Datasheet Style Template

### Structure:
```markdown
# [Product Name] Datasheet

[Single paragraph technical overview with architecture summary]

## Part Number Legend
[Table explaining part number breakdown]

## Features
[Comprehensive bulleted list organized by subsystem]

## Memory Configuration
[Detailed table with addresses, widths, depths]

## Pin Descriptions
[Complete pinout table with directions, voltages, descriptions]

## Hardware Connections
[Minimal connection requirements]
[Crystal configuration]
[Boot options]

## Electrical Specifications
[Absolute maximums]
[DC characteristics]
[AC characteristics]

## Physical Specifications
[Package details]
[Thermal considerations]

## System Architecture
[Detailed technical descriptions by subsystem]

## Compliance
[Complete regulatory information]
```

### Writing Rules:

1. **Maintain objectivity**
   - No marketing language
   - Precise specifications only
   - Technical accuracy paramount

2. **Use comprehensive tables**
   - Every parameter specified
   - Min/typ/max values
   - Units clearly stated

3. **Include all technical details**
   - Memory maps
   - Timing diagrams
   - Register descriptions
   - Bit-level specifications

4. **Provide implementation guidance**
   - Connection requirements
   - Design considerations
   - Thermal management

5. **Structure for reference**
   - Clear section hierarchy
   - Extensive TOC
   - Cross-references

---

## 📋 Content Selection Matrix

| Information Type | Spec Sheet | Datasheet |
|-----------------|------------|-----------|
| Performance claims | Yes (rounded) | Yes (precise) |
| Memory maps | No | Yes |
| Pin descriptions | Summary only | Complete |
| Electrical specs | Basic | Comprehensive |
| Protocols | Named list | Implementation |
| Applications | Suggested | Not covered |
| Comparisons | Yes | No |
| Compliance | Summary | Detailed |
| Examples | Application areas | Connection diagrams |

---

## 🔄 Style Conversion Guidelines

### Technical → Marketing:
1. Round specifications to memorable numbers
2. Group detailed features into categories
3. Add competitive comparisons
4. Emphasize development benefits
5. Simplify technical terminology

### Marketing → Technical:
1. Add precise specifications
2. Expand feature descriptions
3. Remove subjective claims
4. Add implementation details
5. Include all parameters

---

## 📊 Language Patterns

### Spec Sheet Language:
- "Delivers high-speed parallel processing"
- "Excelling at real-time applications"
- "Fastest time to market"
- "Free from complication"
- "Performance of an MPU"

### Datasheet Language:
- "Consists of 8 identical 32-bit processors"
- "Provides 512 KB of shared RAM"
- "Features per-instruction conditional execution"
- "Supports 64 smart I/O pins"
- "Operates at 180 MHz typical"

---

## ✅ Quality Checklist

### For Spec Sheets:
- [ ] Value proposition in first paragraph
- [ ] Competitive positioning included
- [ ] Protocols and features listed
- [ ] Round numbers used
- [ ] 1-2 pages maximum
- [ ] Contact information prominent

### For Datasheets:
- [ ] Complete specifications
- [ ] All parameters defined
- [ ] Implementation guidance
- [ ] No marketing language
- [ ] Comprehensive tables
- [ ] Regulatory compliance detailed

---

## 🚨 Common Pitfalls to Avoid

### In Spec Sheets:
- ❌ Too much technical detail
- ❌ Complex memory addressing
- ❌ Missing value propositions
- ❌ No competitive context

### In Datasheets:
- ❌ Marketing language
- ❌ Incomplete specifications
- ❌ Missing electrical specs
- ❌ No implementation guidance

---

*This style guide enables creation of appropriate marketing or technical documentation based on audience needs*