# P2 Smart Pins Complete Reference - Creation Guide

**Canonical Name:** `p2-smart-pins-tutorial`

## Document Identity - TWO BOOK STRATEGY

### The Two-Book Ecosystem (Updated 2025-08-30)

**Blue Book**: P2 Smart Pins Quick Reference  
**Green Book**: P2 Smart Pins Complete Tutorial ("Titus Plus")

#### Blue Book - Quick Reference
**Title**: P2 Smart Pins Quick Reference  
**Subtitle**: Specifications and Configuration for All 32 Modes  
**Document Type**: Professional Technical Reference  
**Target Audience**: Experienced P2 developers needing quick lookup  
**Size**: ~230 pages (desk reference friendly)  
**Philosophy**: "Find the answer in under 30 seconds"

#### Green Book - Titus Plus Tutorial  
**Title**: P2 Smart Pins Complete Tutorial  
**Subtitle**: Master Every Smart Pin Mode Through Progressive Learning  
**Document Type**: Enhanced Tutorial Guide (Titus Remastered)  
**Target Audience**: Anyone learning Smart Pins or implementing advanced features  
**Size**: ~450 pages (comprehensive learning resource)  
**Philosophy**: "Understand deeply, implement confidently"

### Why Two Books?
- **700+ pages combined would be unwieldy**
- **Different audiences with different needs**
- **80/20 rule: Quick lookup vs. deep learning**
- **Preserves Titus's pedagogical legacy while serving reference needs**

## Voice and Tone Guidelines

### Voice Characteristics
- **Direct and Technical**: "Configure pin 20 as DAC" not "Let's configure..."
- **Authoritative**: State facts, don't hedge
- **Efficient**: Every word serves a purpose
- **Professional**: Assume competence, respect time

### What We DON'T Say
❌ "Let's explore how Smart Pins work"  
❌ "You might be wondering why..."  
❌ "First, we'll learn about..."  
❌ "Congratulations! You've configured..."  
❌ Progressive difficulty language  

### What We DO Say
✅ "Mode %00010 provides 16-bit DAC output"  
✅ "Configure using WRPIN with value ##P_DAC_124R_3V"  
✅ "Common applications include audio output"  
✅ "Performance limitation: 10mA maximum drive"  
✅ Direct, factual statements  

## Pedagogical Framework - Building on Titus

### 🎯 Baseline: Jon Titus's Proven Pedagogical Approach

**From extraction audit (sources/extractions/smart-pins-complete-extraction-audit.md):**

Titus successfully employed these pedagogical principles:

1. **Tutorial-Style Learning Path**
   - Not just "what" but "how" and "why"
   - Narrative explanations that connect concepts
   - Learning by doing, not just reading specs

2. **Progressive Complexity**
   - Start with simplest form of each mode
   - Build to advanced applications
   - Each example slightly more sophisticated

3. **Practical-First Approach**
   - Real-world applications for every mode
   - "When would I use this?" answered immediately
   - Common pitfalls and solutions included

4. **Complete Working Examples (174!)**
   - Every example compiles and runs
   - Self-contained - no external dependencies
   - Shows complete configuration sequence

5. **Step-by-Step Configuration**
   - WRPIN → WXPIN → WYPIN → DIRH sequence
   - Explain what each step accomplishes
   - Show the "why" behind parameter values

### 🔍 Evaluation: Why Titus's Approach Works

**Strengths to Preserve:**
- **Reduces cognitive load** - One concept at a time
- **Builds confidence** - Success with simple before complex
- **Creates mental models** - Narrative helps understanding
- **Enables quick success** - Working code immediately
- **Supports different learning styles** - Visual (diagrams), verbal (narrative), kinesthetic (hands-on examples)

**Areas for Enhancement:**
- Could benefit from more visual organization
- Reference lookup could be faster
- Advanced users might want to skip basics
- Cross-referencing between modes could be stronger

### ✨ Enhanced Pedagogical Best Practices to Add

**Building on Titus's foundation, add these research-based practices:**

1. **Dual-Path Documentation**
   - **Learning Path**: Titus's tutorial approach for first-time users
   - **Reference Path**: Quick lookup for experienced users
   - Visual indicators for which path you're on

2. **Cognitive Scaffolding**
   - **Conceptual Overview**: Big picture before details
   - **Mental Model Building**: Diagrams showing how modes relate
   - **Chunking**: Group related modes conceptually
   - **Analogies**: Compare to familiar concepts

3. **Active Learning Elements**
   - **"Try This" Boxes**: Immediate experiments
   - **Predict-Observe-Explain**: What should happen and why
   - **Common Mistakes**: What goes wrong and how to fix
   - **Debug Challenges**: Broken code to fix

4. **Multiple Representations**
   - **Visual**: Block diagrams, timing diagrams, flowcharts
   - **Textual**: Titus's narrative explanations
   - **Mathematical**: Formulas where applicable
   - **Code**: Both Spin2 and PASM2 perspectives

5. **Retrieval Practice**
   - **Quick Check Questions**: After each mode
   - **Mode Comparison Tables**: See relationships
   - **Decision Trees**: "Which mode should I use?"
   - **Cheat Sheets**: One-page summaries

6. **Metacognitive Support**
   - **Learning Objectives**: What you'll be able to do
   - **Difficulty Indicators**: 🟢 Easy 🟡 Moderate 🔴 Advanced
   - **Time Estimates**: "5 minutes to first success"
   - **Prerequisites**: What you need to know first

### 📋 Implementation Strategy

**For each mode, provide:**

1. **Quick Reference Box** (for experienced users)
   - Mode number, name, one-line description
   - Key parameters table
   - Minimal working example

2. **Tutorial Section** (Titus's approach)
   - Conceptual introduction with narrative
   - Progressive examples with explanations
   - Real-world applications

3. **Deep Dive** (enhanced content)
   - Advanced techniques
   - Performance optimization
   - Integration with other modes

4. **Visual Aids** (new additions)
   - Mode operation diagram
   - Timing diagrams where relevant
   - Pin connection schematics

5. **Practice & Verification**
   - "Try This" experiment
   - Common pitfalls to avoid
   - Debugging tips

### 🎓 Pedagogical Principles Summary

**Core Philosophy**: Start with Titus's successful tutorial approach, enhance with modern pedagogical best practices, provide multiple paths through the material.

**Key Principles:**
1. **Honor Different Learning Styles** - Visual, verbal, hands-on
2. **Progressive Disclosure** - Simple to complex
3. **Active Engagement** - Learn by doing
4. **Multiple Use Cases** - Tutorial for learning, reference for doing
5. **Scaffold Understanding** - Build mental models incrementally

**Success Metric**: A beginner can implement their first Smart Pin in 5 minutes, an expert can find any parameter in 30 seconds.

## Content Structure - Two Books

### Blue Book Structure (Quick Reference)
```
P2-Smart-Pins-Quick-Reference.pdf (~230 pages)
├── Part I: Smart Pin Architecture (20 pages)
│   ├── Overview and Block Diagram
│   ├── Configuration Sequence
│   └── Register Structure
├── Part II: Mode Reference (160 pages, 5 per mode)
│   ├── Mode %00000 - Smart Pin OFF
│   ├── Mode %00001 - Repository Mode
│   ├── [... all 32 modes ...]
│   └── Each: Specs, Registers, Minimal Example, Timing
├── Part III: Appendices (50 pages)
│   ├── A: Mode Selection Matrix
│   ├── B: Configuration Calculator
│   ├── C: Register Reference
│   ├── D: Electrical Specifications
│   └── E: Spin2 Configuration Constants
└── Index
```

### Green Book Structure (Titus Plus Tutorial)
```
P2-Smart-Pins-Complete-Tutorial.pdf (~450 pages)
├── Part I: Understanding Smart Pins (50 pages)
│   ├── The Smart Pin Concept (Titus narrative)
│   ├── Architecture Deep Dive
│   ├── Your First Smart Pin
│   └── Common Patterns
├── Part II: Progressive Mode Tutorials (300 pages)
│   ├── Chapter 1: Output Modes
│   │   ├── Repository Mode (tutorial + 5 examples)
│   │   ├── DAC Modes (tutorial + 8 examples)
│   │   └── [... progressive complexity ...]
│   ├── Chapter 2: Measurement Modes
│   ├── Chapter 3: Serial Communication
│   └── Chapter 4: Advanced Modes
├── Part III: Advanced Techniques (75 pages)
│   ├── Multi-Pin Coordination
│   ├── Performance Optimization
│   ├── Debugging Smart Pins
│   └── Integration Patterns
├── Part IV: Complete Projects (25 pages)
└── Appendices (same as Blue Book for consistency)
```

## Content Requirements

### For Every Mode (All 32)
1. **Mode Header**: Binary value, name, one-line function
2. **Specifications**: Bullet-point technical details
3. **Configuration**: Exact register values and bit definitions
4. **Spin2 Example**: Complete, compilable, <30 lines
5. **PASM2 Example**: Complete, compilable, <30 lines
6. **Applications**: Real-world uses, limitations, tips

### Code Standards
- **MUST compile with pnut_ts** without errors
- **MUST be complete** (no "..." or snippets)
- **MUST use consistent pins** (20 for single, 20-27 for arrays)
- **MUST include minimal comments** (only non-obvious operations)
- **MUST demonstrate core functionality** in simplest form

### Example Code Style
```spin2
' Good - Direct and complete
PUB setup_dac()
  pinstart(20, P_DAC_124R_3V | P_OE, 0, 0)
  wypin(20, $8000)  ' Output 1.65V

' Bad - Too tutorial-like
PUB setup_dac()
  ' First, let's configure our Smart Pin
  ' We'll use pin 20 for this example
  pinstart(20, P_DAC_124R_3V | P_OE, 0, 0)  ' Start the Smart Pin
  wypin(20, $8000)  ' Now output mid-scale
```

## Source Information Matrix

### Smart Pins Content Sources Overview

| Source Document | Location | What We Extract | Why This Source | Unique Value |
|---|---|---|---|---|
| **Jon Titus Smart Pins Manual** | `/sources/extractions/smart-pins-complete-extraction-audit/` | • Tutorial narratives<br>• Progressive examples<br>• Pedagogical flow<br>• 174 code examples<br>• Application context | Primary pedagogical foundation - proven teaching approach | Tutorial-style explanations that make complex modes accessible |
| **Silicon Doc v35** | `/sources/extractions/silicon-doc-complete-extraction-audit/` | • Technical specifications<br>• Electrical characteristics<br>• Timing parameters<br>• Register bit definitions<br>• Hardware constraints | Authoritative hardware reference from Parallax | Most accurate technical specifications and latest updates (re-ingested 2025-08-30) |
| **Spin2 Interpreter Docs** | `/sources/extractions/spin2-v51-complete-extraction-audit/` | • P_ configuration constants<br>• Built-in symbols<br>• Language integration<br>• Method signatures | Shows how Smart Pins integrate with Spin2 | Complete constant definitions for easy configuration |
| **PASM2 Manual** | `/sources/extractions/pasm2-manual-complete-extraction-audit/` | • WRPIN/WXPIN/WYPIN details<br>• Assembly examples<br>• Instruction timing<br>• Low-level control | Assembly-level Smart Pin control | Direct hardware manipulation patterns |
| **Hardware Manual** | `/sources/extractions/hardware-manual-complete-extraction-audit/` | • Pin electrical specs<br>• Board-level integration<br>• Physical constraints<br>• Power considerations | System integration context | Real-world implementation constraints |
| **Opus Master Diagrams** | `/documentation/manuals/smart-pins-workshop/opus-master/` | • Enhanced block diagrams<br>• Timing diagrams<br>• Signal flow visualizations<br>• Conceptual illustrations | Visual learning support | Clear visual representations of complex concepts |

### Content Extraction Priority

**CRITICAL EXTRACTION REQUIREMENTS:**

1. **From Titus Manual - MUST EXTRACT ALL:**
   - ⚠️ **Narrative explanations** (currently missing!)
   - ⚠️ **Tutorial introductions** for each mode
   - ⚠️ **Practical application descriptions**
   - ✅ Code examples (already extracted)
   - ✅ Mode descriptions (already extracted)

2. **From Silicon Doc v35 - NEW CONTENT TO REVIEW:**
   - Additional Smart Pin details not in Titus
   - Updated electrical specifications
   - Timing refinements since original docs
   - Any new mode clarifications

3. **From Spin2 Docs - APPENDIX MATERIAL:**
   - Complete P_ constant reference (for new Appendix E)
   - Configuration bit masks
   - Helper method documentation

### Why Multiple Sources Matter

**Titus Manual**: Provides the "teaching voice" - explains WHY and HOW in accessible terms  
**Silicon Doc**: Provides the "engineering truth" - exact specs and parameters  
**Spin2/PASM2**: Provides the "implementation path" - how to actually use Smart Pins  
**Hardware Manual**: Provides the "system context" - integration considerations  
**Opus Diagrams**: Provides the "visual clarity" - complex concepts made visible  

**Combined Result**: Complete, accurate, accessible, and practical Smart Pins reference

## Source Material Usage

### Primary Sources (Mark as Consumer)
1. **Smart Pins rev 5 documentation** (Jon Titus)
   - Mode descriptions and theory
   - Configuration sequences
   - Base examples to adapt
   - **⚠️ CRITICAL REQUIREMENT (Added 2025-08-29)**: 
     - **MUST extract and incorporate ALL narrative content from the original Titus manual**
     - **Current Issue**: Document has diagrams and generated code but MISSING the explanatory narrative
     - **Action Required**: Verify complete ingestion of Titus manual narrative sections
     - **Integration**: Blend Titus's explanations with enhanced content, not replace them

2. **Enhanced Architecture Diagram Narratives** (NEW - Added 2025-08-29)
   - **Location**: `/exports/pdf-generation/workspace/smart-pins-manual/`
   - **Files**:
     - `enhanced-diagram-section.md` - Complete architecture section with full details
     - `diagram-update.md` - Focused diagram explanation
   - **Usage**: Choose the most pedagogically appropriate narrative based on document flow
   - **Content**: Explains the Smart Pin block diagram (smart-pins-master-trimmed.png)
   - **Key Topics**: Three-layer architecture, pin pair resource sharing, signal routing
   - **Integration Point**: Chapter 1 - Smart Pin Architecture section

3. **Extracted Code Examples** (98 examples from `/sources/extractions/smart-pins-complete-extraction-audit/assets/code-20250824/`)
   - Validate and adapt for manual
   - Ensure bilingual coverage
   - Fix any extraction artifacts

4. **Extracted Images** (21 images from `/sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/`)
   - Use for timing diagrams
   - Mode visualization
   - Connection diagrams

5. **Silicon Documentation** 
   - Electrical specifications
   - Timing requirements
   - Register bit definitions

### Asset Integration Rules
- **Images**: Reference as `![Mode diagram](assets/smart-pins-images/req##-description.png)`
- **Code**: Adapt from extracted examples, ensuring both languages
- **Attribution**: Credit Jon Titus in acknowledgments
- **Validation**: All code tested with pnut_ts before inclusion

## Presentation Style Specifications

### Design Philosophy
**"Technical Elegance Through Clarity"**
- Clean, modern technical documentation aesthetic
- High information density without clutter
- Quick visual scanning capability
- Professional without being sterile

### Typography and Layout
- **Title Font**: Source Sans Pro Bold, 24pt (Mode Headers)
- **Section Font**: Source Sans Pro Semibold, 14pt
- **Body Font**: Source Serif Pro, 11pt
- **Code Font**: Fira Code, 10pt (monospace with ligatures)
- **Page Format**: US Letter (8.5" × 11"), 0.75" margins
- **Layout**: Single column for code readability

### Color Palette
- **Primary Text**: #1a1a1a (softer than pure black)
- **Headers**: #004B87 (professional blue)
- **Code Background**: #f8f9fa (subtle gray)
- **Accent**: #ff6b00 (Iron Sheep orange, sparingly)

### Branding
- **Front**: No branding, pure technical content
- **Copyright Page**: Small "Produced by Iron Sheep Productions, LLC"
- **Back Matter**: Professional "About" section with logo
- **Version**: "Initial Edition - Version 1.0"

## What's Actually Missing vs. Already Present (2025-08-30)

### Content Gap Analysis

**⚠️ TRULY MISSING - Must Add:**

1. **Titus's Tutorial Narratives**
   - All explanatory text that teaches concepts
   - The "why" behind each mode's design
   - Step-by-step reasoning for configurations
   - Practical insights and tips

2. **Appendix E: Smart Pin Configuration Constants**
   - Complete P_ constant reference from Spin2
   - Example: `P_REPOSITORY`, `P_DAC_124R_3V`, `P_ASYNC_TX`
   - Bit field constants for configuration
   - Usage examples with each constant

3. **Silicon Doc v35 Enhancements**
   - Cross-reference for additional Smart Pin details
   - Any specifications updated since Titus manual
   - Clarifications on edge cases
   - Timing refinements

**✅ ALREADY PRESENT - Do Not Duplicate:**
- All 32 mode technical descriptions
- Code examples for each mode (174 total)
- Mode Selection Guide (Appendix A)
- Configuration Calculator (Appendix B)  
- Register Reference (Appendix C)
- Electrical Specifications (Appendix D)
- Smart Pin capabilities overview
- Configuration sequence and formulas
- Mode comparison matrix
- Block diagrams and timing diagrams

### Markdown Processing Strategy

**Pre-Processing (During Creation):**
- Use clean div syntax: `::: sidetrack` not `\begin{sidetrack}`
- Consistent heading hierarchy: # Part, ## Chapter, ### Section
- Mode numbers in headers: `### Mode %00010 - DAC 124Ω, 3.3V`
- Clean code blocks with proper language tags
- Use semantic divs for special content (see below)

**Semantic Block Types for Opus to Use:**

| Markdown Syntax | Purpose | When to Use |
|---|---|---|
| `::: sidetrack` | Tangential information | Background info not critical to main flow |
| `::: spin2` | Spin2 example block | Highlighting Spin2-specific implementations |
| `::: pasm2` | PASM2 example block | Highlighting assembly implementations |
| `::: configuration` | Setup/config steps | Step-by-step configuration sequences |
| `::: antipattern` | What NOT to do | Common mistakes and how to avoid them |

**Pattern Discovery Instructions for Opus:**
```markdown
If you identify recurring content patterns that need special formatting:
1. Create a new semantic div: ::: pattern-name
2. Add a comment explaining it: <!-- NEW PATTERN: name - description -->
3. Use consistently throughout the document

Example new patterns you might identify:
- ::: timing - for timing-critical sections
- ::: performance - for performance implications
- ::: debug - for troubleshooting tips
- ::: limitation - for hardware constraints
```

**CRITICAL: Semantic Type Manifest Requirement**

At the END of document generation, Opus MUST provide:
```markdown
## SEMANTIC TYPES MANIFEST
<!-- This section is for post-processing setup, not publication -->

### Used Semantic Types:
1. `sidetrack` - Used 23 times - Tangential information boxes
2. `spin2` - Used 45 times - Spin2 code example blocks
3. `pasm2` - Used 67 times - PASM2 code example blocks
4. `configuration` - Used 32 times - Step-by-step setup sequences
5. `antipattern` - Used 12 times - Common mistakes to avoid
6. `timing` (NEW) - Used 8 times - Timing-critical code sections
7. `performance` (NEW) - Used 15 times - Performance implications
8. `debug` (NEW) - Used 9 times - Debugging/troubleshooting tips

### Formatting Suggestions:
- `timing`: Consider yellow background with clock icon
- `performance`: Consider benchmark/graph icon
- `debug`: Consider magnifying glass icon
```

This manifest enables:
1. **Systematic style creation** - We know all types before formatting
2. **Consistency checking** - Verify all instances formatted correctly
3. **Documentation** - Clear record of semantic types used
4. **Efficient post-processing** - Build all styles at once

**Post-Processing (Before PDF):**
- Run LaTeX escape script: `/tools/latex-escape-all.sh`
- Lua filters convert semantic divs to LaTeX environments
- LaTeX styles (in .sty files) control final appearance
- PASM mnemonics auto-bolded via listings configuration

**Rationale**: 
- Pre-processing keeps markdown semantic and maintainable
- Opus focuses on content structure, not visual formatting
- Post-processing handles all LaTeX/PDF presentation details
- New patterns can be added without changing generation approach

## Knowledge Gaps and Update Tracking

### Areas Requiring Future Enhancement

#### 🔴 CRITICAL GAPS (Mark with ⚠️ in text)
1. **USB Mode (%11011)**
   - Current: Basic configuration only
   - Missing: Host/device protocols, packet handling, complete stack
   - Mark as: "⚠️ USB mode documentation preliminary - await silicon validation"

2. **Electrical Specifications**
   - Current: Typical values from various sources
   - Missing: Complete min/typ/max specifications
   - Mark as: "⚠️ Electrical specifications subject to revision"

#### 🟡 MODERATE GAPS (Mark with 📌 in text)
3. **SMPS Mode (%01010)**
   - Current: Basic examples
   - Missing: Advanced switching patterns, efficiency curves
   - Mark as: "📌 SMPS applications require external validation"

4. **ADC Calibration**
   - Current: Default calibration info
   - Missing: Temperature compensation, linearity correction
   - Mark as: "📌 ADC calibration procedures under development"

5. **Multi-COG Synchronization**
   - Current: Basic coordination patterns
   - Missing: Complex timing scenarios, race conditions
   - Mark as: "📌 Advanced synchronization patterns being validated"

#### 🟢 MINOR GAPS (Note in appendix)
6. **Performance Metrics**
   - Current: Theoretical maximums
   - Missing: Real-world benchmarks across temperature
   - Track in appendix for future updates

7. **Power Consumption**
   - Current: Typical values
   - Missing: Per-mode detailed measurements
   - Track in appendix for future updates

### Update Protocol

When better sources become available:
1. **Search for gap markers** (⚠️, 📌)
2. **Update content** with validated information
3. **Remove or downgrade markers** as appropriate
4. **Note update** in revision history
5. **Increment version** (1.0 → 1.1 for minor, 2.0 for major)

### Gap Tracking Table

Include this table in the appendix:

```markdown
## Knowledge Gap Tracker

| Mode | Topic | Current Status | Gap Level | Update Priority |
|------|-------|---------------|-----------|----------------|
| %11011 | USB Implementation | Basic only | 🔴 Critical | High |
| All | Electrical Specs | Typical values | 🔴 Critical | High |
| %01010 | SMPS Patterns | Limited examples | 🟡 Moderate | Medium |
| %11000-2 | ADC Calibration | Default only | 🟡 Moderate | Medium |
| Multiple | COG Sync | Basic patterns | 🟡 Moderate | Low |
| All | Power Data | Estimates | 🟢 Minor | Low |
```

### Version Control for Updates

- **v1.0**: Initial release with marked gaps
- **v1.1**: USB mode enhancement (when available)
- **v1.2**: Electrical specifications complete (when validated)
- **v2.0**: All critical gaps resolved

## Production Specifications

### Markdown Structure
```markdown
# Mode %MMMMM - [Mode Name]

## Specifications

- **Function**: [One sentence description]
- **Resolution**: [If applicable]
- **Range**: [Operating range]
- **Timing**: [Key timing specs]
- **Power**: [Current consumption]

## Configuration

**Mode Register (WRPIN)**:
```
Bit definition table or description
```

**X Register (WXPIN)**: [Function in this mode]

**Y Register (WYPIN)**: [Function in this mode]

**Z Register (RDPIN)**: [What it returns]

## Spin2 Implementation

```spin2
[Complete working example]
```

## PASM2 Implementation

```pasm2
[Complete working example]
```

## Applications

**[Application 1]**: [Description and considerations]

**[Application 2]**: [Description and considerations]

**Performance Notes**: [Any limitations or optimization tips]
```

### Eisvogel Template Compatibility
- Use standard markdown headers (# ## ###)
- Code blocks with language tags (```spin2, ```pasm2)
- Tables in pipe format when needed
- Bullet lists with - or * 
- Bold with ** for emphasis
- Avoid HTML tags or special formatting

### Visual Elements
- **Timing diagrams**: Include where critical to understanding
- **Register bit diagrams**: For complex configurations
- **Pin connection diagrams**: For multi-pin modes
- **NO screenshots**: Use extracted vector diagrams
- **NO photos**: Technical drawings only

## Quality Checklist

### Per-Mode Validation
- [ ] Mode number and name correct
- [ ] Specifications match silicon docs
- [ ] Both code examples compile
- [ ] Both code examples < 30 lines
- [ ] Applications are practical
- [ ] No tutorial language present
- [ ] Images properly referenced

### Document-Level Validation
- [ ] All 32 modes documented
- [ ] Consistent formatting throughout
- [ ] No external dependencies
- [ ] Professional tone maintained
- [ ] Complete index generated
- [ ] Cross-references valid

## Consumer Registry

This document consumes:
- `/sources/extractions/smart-pins-complete-extraction-audit/` (primary source)
- `/sources/extractions/smart-pins-complete-extraction-audit/assets/code-20250824/` (code examples)
- `/sources/extractions/smart-pins-complete-extraction-audit/assets/images-20250824/` (diagrams)
- `/sources/extractions/silicon-doc-complete-extraction-audit/` (specifications)
- `/sources/extractions/hardware-manual-complete-extraction-audit/` (electrical specs)

## Gap Acknowledgment Standards

### In-Text Markers
```markdown
⚠️ **Note**: USB mode documentation is preliminary pending complete protocol specifications.

📌 **Note**: SMPS efficiency curves require external validation with production hardware.

💡 **Tip**: Check Iron Sheep Productions website for updates to this reference.
```

### Footer Note for Gap Sections
```markdown
---
*This section contains preliminary information that will be enhanced in future editions as validated sources become available.*
---
```

## Success Metrics

### Quantitative
- 32/32 modes documented
- 64 working code examples (32 Spin2 + 32 PASM2)
- 100% compilation success rate
- <5 minutes to implement any mode
- 230 pages ±10%

### Qualitative
- Professional appearance
- No ambiguity in specifications
- Code clarity without excessive comments
- Complete without verbosity
- Authoritative reference status

## Visual Design Standards (Green Book)

### Color Philosophy
- **Pastel backgrounds** for extended reading comfort
- **Distinct visual treatment** for semantic markers vs code blocks
- **Accessibility** through border styles (solid/dashed/dotted)

### Semantic Marker Usage

**When to use each marker:**
- `needs-diagram`: Visual would clarify timing, signals, or architecture
- `preliminary-content`: Feature awaiting silicon validation or development
- `needs-verification`: Information requiring fact-checking
- `needs-examples`: Section would benefit from more code samples
- `needs-technical-review`: Technical specs needing expert validation
- `needs-code-review`: Code requiring verification
- `tip`: Helpful hints and best practices

**Visual Implementation:**
- Full borders (not just left edge like code blocks)
- Title bars with descriptive text (no icons)
- Distinct border patterns for accessibility
- See `/exports/pdf-generation/workspace/smart-pins-manual/green-book-visual-specifications.md` for exact specs

### Typography Standards
- Body text: 10.5pt (5% larger than reference)
- Line spacing: 1.25x for readability
- Code blocks: 9pt monospace
- Digital-first margins: 0.75" with 1" binding edge

## Document Generation Process - DUAL BOOK WORKFLOW

### Generation Strategy: One Pass, Two Books

**KEY INSIGHT**: Generate Green Book (Titus Plus) with Opus FIRST, then extract Blue Book with Sonnet

```
OPUS GENERATION (Green Book)
    ↓
Rich tutorial content with narratives
    ↓
SONNET EXTRACTION (Blue Book)
    ↓  
Distilled reference specifications
```

### Phase 1: Green Book Generation (Opus 4.1)
**Generate the complete tutorial guide with rich content:**
- [ ] Extract ALL Titus narratives and explanations
- [ ] Generate enhanced tutorials for all 32 modes
- [ ] Create 348+ progressive examples with explanations
- [ ] Write conceptual introductions and transitions
- [ ] Develop debugging scenarios and troubleshooting
- [ ] Add integration patterns and advanced techniques
- [ ] Incorporate Silicon Doc v35 updates seamlessly

**Why Opus**: Superior narrative flow, pedagogical reasoning, engaging explanations

### Phase 2: Blue Book Extraction (Sonnet 4)
**Extract and reorganize from Green Book content:**
- [ ] Extract mode specifications into reference format
- [ ] Select one minimal example per mode
- [ ] Pull configuration formulas and calculations
- [ ] Create quick reference tables and matrices
- [ ] Build comprehensive index and cross-references
- [ ] Format for rapid lookup (tabs, margins, headers)
- [ ] Add Appendix E (Spin2 constants)

**Why Sonnet**: Mechanical extraction, reformatting, organization - no creativity needed

### Phase 3: Validation (Both Books)
- [ ] Compile all code examples
- [ ] Verify spec consistency between books
- [ ] Technical accuracy review
- [ ] Cross-reference validation
- [ ] Size and usability testing

### Phase 4: Production
- [ ] Apply p2kb-smart-pins template (Blue Book)
- [ ] Apply p2kb-smart-pins-tutorial template (Green Book)
- [ ] Generate PDFs using PDF Forge
- [ ] Final review and deployment

### Phase 5: Deployment
**MANDATORY DEPLOYMENT FOLDER**: `/exports/pdf-generation/outbound/P2-Smart-Pins-Reference/`

**NEVER use any other folder name** - This is the established path for Smart Pins PDF generation.

**Deployment Package Contents (ONLY THESE FILES)**:
- `P2-Smart-Pins-Complete-Reference.md` - LaTeX-escaped document markdown
- `request.json` - With `--top-level-division=part` argument  
- `last-deployed/` - Backup copies (system-managed)
- `assets/` - Images (if needed)

**NO OTHER MARKDOWN FILES** - No deployment instructions, README files, or documentation
**ONLY the document markdown and JSON files needed for PDF generation**

**Template Requirements (on PDF Forge)**:
- Main template: `p2kb-smart-pins.latex`
- Foundation layer: `p2kb-foundation.sty`
- Content layer: `p2kb-smart-pins-content.sty`  
- Presentation layer: `p2kb-tech-review.sty`

## Notes for AI Generation

When generating content:
1. **Be concise** - Minimum words, maximum information
2. **Be precise** - Exact values, not approximations
3. **Be practical** - Real applications, not contrived examples
4. **Be complete** - Self-contained examples
5. **Be consistent** - Same style throughout

Remember: This is a reference document, not a tutorial. Every sentence should provide value to a developer who already understands embedded systems and needs P2-specific information.

## Version Control

- **Version**: 1.0 (First Complete Draft)
- **Date**: 2025-08-24
- **Status**: Content generation phase
- **Next Review**: After 10 mode chapters complete