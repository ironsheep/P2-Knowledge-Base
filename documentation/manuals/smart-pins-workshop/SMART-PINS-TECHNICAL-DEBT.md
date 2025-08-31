# Smart Pins Document - Technical Debt & Post-Processing Requirements

## Post-Processing Style Requirements

### 1. PASM Mnemonic Bolding
**Requirement**: All PASM mnemonics should be bold and uppercase in code blocks
**Status**: 🔴 Not Implemented
**Solution Options**:
1. **Listings package customization** (Recommended)
   - Define pasm2 language in p2kb-foundation.sty
   - Auto-bold keywords via keywordstyle
2. **Python preprocessor**
   - Process before LaTeX escape
3. **Lua filter**
   - Process during pandoc conversion

**Implementation**:
```latex
\lstdefinelanguage{pasm2}{
  morekeywords=[1]{MOV, ADD, SUB, WRPIN, WXPIN, WYPIN, DIRH, DIRL},
  keywordstyle=[1]\bfseries\uppercase,
  sensitive=false
}
```

### 2. Semantic Block Types (Div-Based)

**Currently Identified Block Types**:

| Markdown Div | LaTeX Environment | Purpose | Visual Style |
|---|---|---|---|
| `::: sidetrack` | `\begin{sidetrack}` | Tangential information | Gray box, dashed border |
| `::: spin2` | `\begin{spin2example}` | Spin2 code example | Blue header, code formatting |
| `::: pasm2` | `\begin{pasm2example}` | PASM2 code example | Green header, code formatting |
| `::: configuration` | `\begin{configbox}` | Configuration steps | Numbered list, highlighted |
| `::: antipattern` | `\begin{antipattern}` | What NOT to do | Red border, warning icon |

**Pattern Recognition for New Types**:

Opus should be instructed to:
1. **Identify recurring content patterns** that need distinct formatting
2. **Create new semantic div types** as needed
3. **Document the pattern** in a comment

**Example Opus Instruction**:
```markdown
When you identify a recurring pattern that needs special formatting:
1. Create a semantic div type: ::: pattern-name
2. Add a comment explaining what it is:
   <!-- NEW PATTERN: timing-critical - for time-sensitive code sections -->
3. Use consistently throughout the document
```

### 3. Potential New Block Types to Watch For

Based on Smart Pins content, Opus might identify:

| Potential Pattern | Suggested Div | Purpose |
|---|---|---|
| Timing diagrams | `::: timing` | ASCII or described timing |
| Pin connections | `::: pinout` | Physical connection diagrams |
| Mode comparison | `::: comparison` | Side-by-side mode features |
| Performance notes | `::: performance` | Speed/resource implications |
| Hardware limits | `::: limitation` | Physical constraints |
| Debug tips | `::: debug` | Troubleshooting help |
| Math formulas | `::: formula` | Calculation examples |

### 4. Post-Processing Pipeline

```
1. Opus generates with semantic divs
   ↓
2. LaTeX escape script (preserves divs)
   ↓
3. Lua filters convert divs to environments
   ↓
4. LaTeX styles render final appearance
```

### 5. Style Definition Location

**For each semantic block type, define in**:
1. **Lua filter**: `/pdf-forge-workspace/filters/smart-pins-blocks.lua`
   - Converts div to LaTeX environment
2. **LaTeX style**: `p2kb-smart-pins-content.sty`
   - Defines visual appearance

**Example Style Definition**:
```latex
% In p2kb-smart-pins-content.sty
\newtcolorbox{antipattern}{
  colback=red!5!white,
  colframe=red!75!black,
  title={⚠️ Anti-Pattern},
  fonttitle=\bfseries
}
```

## Implementation Priority

1. **High Priority** (Needed for first generation):
   - Sidetrack blocks
   - Spin2/PASM2 example blocks
   - Configuration blocks
   - Anti-pattern blocks

2. **Medium Priority** (Can add during generation):
   - New patterns Opus identifies
   - Performance/limitation blocks
   - Debug blocks

3. **Low Priority** (Enhancement pass):
   - PASM mnemonic bolding
   - Advanced syntax highlighting
   - Cross-reference automation

## Semantic Type Discovery Workflow

### Opus Generation Output

**Opus provides at END of document:**
1. Complete document with semantic divs used throughout
2. **Semantic Types Manifest** listing:
   - All div types used
   - Usage count for each
   - Description of purpose
   - Formatting suggestions

### Post-Processing Workflow

```
1. Receive document + manifest from Opus
   ↓
2. Review manifest for new semantic types
   ↓
3. Create LaTeX environments for each type
   ↓
4. Create Lua filter mappings
   ↓
5. Test with sample content
   ↓
6. Process full document
```

### Style Creation Template

For each semantic type in manifest:

```latex
% In p2kb-smart-pins-content.sty
\newtcolorbox{[semantic-name]}{
  colback=[background-color],
  colframe=[border-color],
  title={[icon] [Title]},
  fonttitle=\bfseries,
  breakable
}
```

```lua
-- In smart-pins-blocks.lua
if elem.classes[1] == "[semantic-name]" then
  return pandoc.RawBlock('latex', 
    '\\begin{[semantic-name]}\n' .. 
    elem.content .. 
    '\\end{[semantic-name]}')
end
```

## Notes for Opus Generation

**Instructions to include in Opus prompt**:
```
Use these semantic div blocks for special content:
- ::: sidetrack - for tangential information
- ::: spin2 - for Spin2 examples
- ::: pasm2 - for PASM2 examples  
- ::: configuration - for setup steps
- ::: antipattern - for what NOT to do

If you identify new recurring patterns that need special formatting:
1. Create a new ::: pattern-name div
2. Use consistently throughout

AT THE END of the document, provide a SEMANTIC TYPES MANIFEST:
- List all div types used
- Include usage counts
- Describe the purpose of each
- Suggest visual formatting

Don't worry about LaTeX formatting - just use clean markdown divs.
```

## Two-Book Generation Strategy (DECISION PENDING)

### The Relationship Between Blue and Green Books

**Shared Content (Extractable):**
- Mode specifications (register values, bit fields)
- Basic configuration sequences  
- Minimal working examples (1 per mode)
- Electrical specifications
- Pin assignments
- Timing parameters

**Green Book Unique:**
- Titus's tutorial narratives
- Progressive learning explanations
- Multiple examples per mode (348+ total)
- "Why" explanations
- Debugging scenarios
- Integration patterns
- Conceptual introductions

**Blue Book Unique:**
- Appendix E: Spin2 configuration constants (complete reference)
- Quick lookup formatting (tabs, indices)
- Decision trees/flowcharts for mode selection
- Condensed comparison matrices
- One-page cheat sheets per mode
- Cross-reference indices optimized for lookup

### Generation Strategy Options

#### Option 1: Generate Both Separately
```
Opus Pass 1: Generate Green Book (tutorial focus)
Opus Pass 2: Generate Blue Book (reference focus)
Post-Process: Synchronize cross-references between books
```
**Pros:** 
- Each book perfectly optimized for its audience
- Clean separation of concerns
- Can use different prompts/approaches

**Cons:** 
- Two Opus passes (expensive)
- Need to ensure consistency
- Cross-reference synchronization needed

#### Option 2: Generate Green + Extract + Augment
```
1. Opus generates Green Book (complete tutorial)
2. Extract shared specifications → Blue Book core
3. Add Blue Book unique content separately
4. Post-process cross-references
```
**Pros:** 
- Single source for specifications
- One Opus pass for main content
- Blue additions mostly mechanical

**Cons:** 
- Extraction logic complexity
- Still need some generation for Blue-unique content

#### Option 3: Generate Superset + Split
```
1. Opus generates COMPLETE SUPERSET with markers
   <!-- GREEN ONLY --> and <!-- BLUE ONLY -->
2. Post-process splits into two books
3. Auto-generate cross-references
```
**Pros:** 
- True single source
- Perfect consistency

**Cons:** 
- Complex prompt for Opus
- Opus thinking about both audiences
- Larger initial document

### Cross-Reference Synchronization Strategy

**For Option 1 (Separate Generation):**

1. **Establish Naming Conventions:**
   ```
   Green Book: "Smart-Pins-Tutorial-Ch3-Section2"
   Blue Book: "Smart-Pins-Ref-Mode-00010"
   ```

2. **Post-Process Cross-References:**
   ```python
   # Map Blue Book references to Green Book sections
   ref_map = {
     "Mode %00010": "Tutorial Chapter 3.2",
     "DAC Configuration": "Tutorial Section 5.4"
   }
   ```

3. **Auto-Generate Cross-Reference Appendix:**
   ```markdown
   ## Cross-Reference Guide
   | Blue Book Section | Green Book Section | Topic |
   |---|---|---|
   | Mode %00010 | Chapter 3.2 | DAC 124Ω Configuration |
   ```

4. **Smart Link Generation:**
   - Blue Book: "For tutorial, see Green Book Ch. 3.2"
   - Green Book: "For quick reference, see Blue Book Mode %00010"

### Recommended Approach (Start Simple)

**Phase 1: Generate Green Book First**
- Focus on getting Titus Plus tutorial perfect
- Don't worry about Blue Book yet
- Establish patterns and semantic types

**Phase 2: Evaluate Best Blue Book Path**
- After Green Book complete, assess:
  - How much is truly extractable?
  - How different is Blue Book structure?
  - Is separate generation cleaner?

**Phase 3: Implement Cross-Reference System**
- Post-process to ensure books reference each other
- Build reference mapping table
- Auto-generate cross-reference appendices

**Key Insight:** Cross-references can ALWAYS be fixed in post-processing, so generation strategy choice isn't locked in by this concern.

## Future Enhancements

- **Auto-index generation** from semantic blocks
- **Interactive elements** for PDF (links between modes)
- **Syntax validation** for code blocks
- **Automatic cross-references** between related modes