# P2 Instruction Master Repository Plan

**Created**: 2025-09-02  
**Purpose**: Establish central repository for all P2 instruction knowledge

---

## 🎯 Current State Analysis

### Sources We Have
1. **Silicon Doc v35** - 119 unique mnemonics with encoding (AUTHORITATIVE)
2. **P2 Instructions CSV** - 491 variants with timing columns
3. **Chip Clarifications** - 13 instructions with detailed semantics
4. **PASM2 Manual DOCX** - 219 tables (potentially ~45% coverage)
5. **Various extractions** - Scattered knowledge

### Problems to Solve
1. **No central repository** - Knowledge scattered across files
2. **Timing confusion** - Silicon Doc timing not properly extracted
3. **Missing semantics** - Many instructions lack descriptions
4. **No cross-referencing** - Sources not linked

---

## 📊 Proposed Master Repository Structure

### File: `INSTRUCTION-MASTER-REPOSITORY.md`

Each instruction should have:
```markdown
## INSTRUCTION_NAME

### Basic Information
- **Mnemonic**: ADD
- **Encoding**: EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS
- **Group**: Math and Logic
- **Category**: Arithmetic

### Timing Information
| Execution Mode | 8 COGs | 16 COGs | Notes |
|----------------|--------|---------|-------|
| COG Exec | 2 | 2 | |
| LUT Exec | 2 | same | |
| HUB Exec | 2* | 2* | +1 if crosses hub long |

### Operation
- **Syntax**: `ADD D,{#}S {WC/WZ/WCZ}`
- **Function**: Add S into D
- **Formula**: D = D + S
- **C Flag**: Carry of (D + S)
- **Z Flag**: Result == 0

### Semantics (from Chip/Silicon Doc)
[Detailed description of what the instruction does]

### Usage Patterns
[Examples and common use cases]

### Related Instructions
- ADDX (add with carry)
- ADDS (add with sign)
- ADDSX (add with sign extension)

### Source Attribution
- Encoding: Silicon Doc v35 (PRIMARY)
- Timing: P2 Instructions CSV v35
- Semantics: [Chip clarification 2025-09-02 | Silicon Doc | PASM2 Manual]
- Examples: [Generated | From manual]
```

---

## 🔄 Extraction Plan

### Phase 1: CSV Timing Analysis
1. Parse P2 Instructions CSV columns:
   - Column 8: "Clock Cycles (8 cogs) - Cog Exec Mode"
   - Column 9: "Clock Cycles (8 cogs) - LUT Exec Mode"
   - Column 10: "Clock Cycles (8 cogs) - Hub Exec Mode"
   - Column 11: "Clock Cycles (16 cogs) - Cog Exec Mode"
   - Column 12: "Clock Cycles (16 cogs) - LUT Exec Mode"

2. Decode timing values:
   - Numeric = cycle count
   - "same" = same as previous column
   - "*" suffix = conditional (+1 if crosses hub long)
   - "2..17" = variable timing range

### Phase 2: Silicon Doc Deep Dive
1. Re-examine Silicon Doc parts for timing details
2. Look for:
   - Pipeline information
   - Stall conditions
   - Hub synchronization
   - Special timing cases

### Phase 3: Consolidation
1. Create master repository file
2. Start with Chip's 13 clarified instructions
3. Add Silicon Doc encodings
4. Add CSV timing data
5. Cross-reference PASM2 Manual tables

---

## 📋 Implementation Steps

### Step 1: Create Parser for CSV
```python
# Parse CSV to extract:
- Instruction name
- Encoding
- Group/Category
- Timing for all execution modes
- Flag effects
- Basic operation description
```

### Step 2: Extract Silicon Doc Timing
- Search for timing-related sections
- Look for pipeline descriptions
- Find hub synchronization details
- Extract special cases

### Step 3: Build Repository
1. Start with template structure
2. Populate from CSV (all 491 variants)
3. Enhance with Silicon Doc
4. Add Chip's clarifications
5. Cross-reference PASM2 Manual

### Step 4: Validation
- Check for conflicts
- Verify timing makes sense
- Ensure encoding matches
- Validate flag behavior

---

## 🎯 Priority Instructions

### High Priority (Have Chip clarifications)
1. MODC, MODZ, MODCZ
2. SUMC, SUMNC, SUMZ, SUMNZ
3. INCMOD, DECMOD
4. ADDSX, SUBSX, CMPSX

### Critical Families
1. ADD/SUB/CMP (all variants)
2. JMP/CALL/RET (control flow)
3. RD*/WR* (memory access)
4. TEST* (bit operations)

---

## 📊 Success Metrics

### Completion Goals
- [ ] All 119 base mnemonics documented
- [ ] All 491 variants mapped
- [ ] Timing for all execution modes
- [ ] Chip's clarifications integrated
- [ ] PASM2 Manual cross-referenced

### Quality Metrics
- No timing conflicts
- All encodings verified
- Semantics clear and complete
- Examples provided
- Cross-references accurate

---

## 🔴 Critical Timing Understanding

### Execution Modes Matter
- **COG Exec**: Instructions in COG RAM
- **LUT Exec**: Instructions in LUT RAM
- **HUB Exec**: Instructions in HUB RAM

### COG Count Affects Timing
- **8 COGs**: Standard configuration
- **16 COGs**: FPGA emulation mode

### Special Cases
- "+1 if crosses hub long" - Hub alignment penalty
- Variable timing (2..17) - Depends on operation
- "same" - Inherits previous column's timing

---

*This plan establishes a path to creating the definitive P2 instruction reference*