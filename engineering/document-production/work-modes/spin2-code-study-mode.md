# Spin2/PASM2 Code Study Mode
*Work mode guide for extracting patterns and insights from P2 codebases*

## Activation Phrase
"We're going to study some code today" / "Let's analyze this codebase" / "Study this Spin2/PASM2 code"

## Primary Objective
Extract reusable patterns, idioms, and insights from real Spin2/PASM2 codebases to improve AI code generation capabilities.

## Filter Keys for Todo MCP
```yaml
tags: ["spin2_study"]  # Primary tag for all code study work
# Additional tags can include: pattern_extraction, spin2_analysis
```

## Initial Assessment Protocol

### 1. Codebase Overview (First Pass)
```bash
# Get structure
find . -name "*.spin2" -o -name "*.spin" | head -20
ls -la *.spin2 *.spin 2>/dev/null

# Check size and scope
wc -l *.spin2 *.spin 2>/dev/null

# Identify main entry points
grep -l "PUB main\|PUB start" *.spin2 *.spin
```

### 2. Identify Code Categories
- **Drivers**: Serial, SPI, I2C, display, sensor interfaces
- **Applications**: Main programs, demos, examples  
- **Libraries**: Utility functions, math libraries, string handling
- **Hardware**: Pin management, COG coordination, timing

## Extraction Methodology

### Phase 1: Structural Analysis
Focus on discovering:
```yaml
program_structure:
  - Block organization (CON/VAR/OBJ/DAT/PUB/PRI)
  - Object composition patterns
  - File organization strategies
  - Naming conventions

memory_patterns:
  - VAR vs DAT usage decisions
  - Buffer allocation strategies
  - Stack size patterns
  - Shared memory structures
```

### Phase 2: Pattern Extraction

#### A. Object Lifecycle Patterns
Look for:
```spin2
' Initialization patterns
PUB start(params) : success
PUB stop()
PUB init()

' Resource management
cog := COGNEW(...) + 1
IF cog
  COGSTOP(cog - 1)
```

#### B. COG Communication Patterns
Identify:
- Mailbox structures in DAT
- Command/response protocols
- Synchronization methods
- Shared buffer management

#### C. Pin I/O Patterns
Extract:
- Pin configuration sequences
- Pin group handling (ADDPINS usage)
- Smart pin setup patterns
- Timing-critical I/O

#### D. Timing Patterns
Document:
- Delay implementations
- Periodic event handling
- Timeout mechanisms
- Real-time constraints

#### E. Error Handling
Capture:
- Return value conventions
- Error propagation
- Recovery strategies
- Validation patterns

### Phase 3: Spin2-Specific Idioms

#### Critical Operators to Track
```spin2
' Clamping idioms
value := 0 #> value <# 100

' Rotation idioms  
value <- bits
value -> bits

' Post-operators
value++
value--
```

#### Language-Specific Patterns
- REPEAT variations
- CASE statement usage
- String handling approaches
- Float vs integer operations

### Phase 4: PASM2 Integration

#### Inline PASM Patterns
```spin2
PUB method() | local
  ORG
    ' PASM2 code
  END
```

#### COG Driver Patterns
```spin2
DAT
  ORG 0
entry
  ' Driver code
```

Document:
- When inline vs DAT PASM2
- Register usage conventions
- Hub/COG execution decisions
- Performance optimizations

## Documentation Format

### Pattern Template
```markdown
## Pattern: [Pattern Name]
**Category**: [Driver/Application/Utility/Hardware]
**Frequency**: [Common/Occasional/Rare]
**Purpose**: [What problem it solves]

### Implementation
```spin2
[Actual code from codebase]
```

### Key Insights
- [Why this pattern is used]
- [When to apply it]
- [Variations observed]

### Performance Notes
- [Timing characteristics]
- [Memory usage]
- [COG requirements]
```

## Extraction Outputs

### 1. Pattern Library Document
Create: `spin2-patterns-from-[codebase-name].md`
- Categorized patterns
- Usage frequency
- Implementation examples
- Decision criteria

### 2. Idiom Database
Create: `spin2-idioms-extracted.yaml`
```yaml
idioms:
  - pattern: "value := 0 #> value <# 100"
    meaning: "Clamp value between 0 and 100"
    frequency: "very_common"
    contexts: ["sensor_readings", "pwm_values"]
```

### 3. Template Collection
Create: `spin2-templates/`
- driver-template.spin2
- application-template.spin2
- library-template.spin2

### 4. Insights Summary
Create: `codebase-insights.md`
- Architectural decisions
- Performance strategies
- Common pitfalls avoided
- Best practices observed

## Analysis Checklist

### For Each File Studied
- [ ] Document file purpose and category
- [ ] Extract initialization pattern
- [ ] Identify COG usage strategy
- [ ] Note memory allocation approach
- [ ] Capture error handling method
- [ ] Record Spin2-specific idioms
- [ ] Document PASM2 integration points
- [ ] Note timing/synchronization methods

### For Overall Codebase
- [ ] Identify common patterns across files
- [ ] Document architectural decisions
- [ ] Extract reusable templates
- [ ] Note performance optimizations
- [ ] Capture domain-specific knowledge
- [ ] Build idiom frequency table

## Quality Metrics

### Pattern Quality
- **Completeness**: Full context included
- **Reusability**: Can be applied to similar problems
- **Clarity**: Purpose and usage are clear
- **Performance**: Timing/memory characteristics documented

### Coverage Goals
- Minimum 80% of files analyzed
- All major patterns documented
- Common idioms catalogued
- Template for each category

## Context Keys to Maintain

```bash
# Track progress
context_set key:"code_study_progress_[codebase]" value:"files: X/Y, patterns: N"

# Save key insights
context_set key:"lesson_[pattern]" value:"[insight]"

# Record architectural decisions
context_set key:"architecture_[codebase]" value:"[key decision]"
```

## Success Criteria

1. **Pattern Extraction**: ≥20 reusable patterns documented
2. **Idiom Coverage**: Common operators and constructs catalogued
3. **Template Creation**: Working templates for major categories
4. **Insight Generation**: Architectural understanding documented
5. **Example Collection**: Real code examples for each construct

## Post-Study Actions

1. Consolidate patterns into master library
2. Update Spin2 code generation rules
3. Create quick reference guide
4. Document lessons learned
5. Prepare for next codebase study

## Model Recommendations
- **Opus 4.1**: Initial analysis and pattern recognition
- **Sonnet 4**: Detailed extraction and documentation
- **Either**: Follow-up studies with established patterns