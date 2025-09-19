# YAML Quality Improvement Plan
## Path to Highest Quality Documentation

## Current State Assessment

### Overall Quality Score: 66.2%
- **Instructions**: 74.9% average quality
- **Directives**: 57.5% average quality
- **High Quality (80%+)**: 197 instructions (54.7%)
- **Adequate (60%+)**: 303 instructions (84.2%)
- **Needs Work (<60%)**: 57 instructions (15.8%)

## Critical Quality Gaps

### 1. 🚨 **No Examples: 327 files (91%)**
This is the MOST CRITICAL gap. AI models learn from examples. Without them:
- AI cannot understand proper syntax usage
- AI cannot learn context-appropriate application
- AI will generate incorrect code

### 2. 🚨 **Missing Brief Descriptions: 205 files (57%)**
Brief descriptions are essential for:
- Quick reference and understanding
- Heat map tooltips
- IDE autocomplete descriptions

### 3. 🚨 **Missing Flag Documentation: 171 files (47%)**
Critical for correctness because:
- Flags determine conditional execution
- Wrong flag usage = wrong program behavior
- Essential for optimization and debugging

### 4. 🚨 **No Parameters Documented: 161 files (45%)**
Without parameter documentation:
- AI doesn't know valid operand types
- Cannot validate instruction usage
- Missing critical constraints (immediate vs register)

## How We Know Current Quality

### What We've Validated:
1. ✅ **Manual extraction completed** for 143 instructions from pages 31-147
2. ✅ **Consistent structure** across all YAMLs
3. ✅ **Required fields present** in 84% of files
4. ✅ **Documentation source tracked** for traceability

### What's Still Missing:
1. ❌ **Examples** - Only 33 files have examples
2. ❌ **Complete flag effects** - 171 missing
3. ❌ **Comprehensive parameters** - 161 missing
4. ❌ **Full directive documentation** - 10/12 need work

## Path to Highest Quality (90%+)

### Phase 1: Add Examples (Highest Impact)
**Goal**: Add at least 1 working example to all 327 files

**Sources for examples:**
1. Official Parallax example code
2. OBEX repository patterns
3. P2 forum code snippets
4. Compiler test cases

**Example template:**
```yaml
examples:
  - code: "ADD result, value1, value2  ' Add two registers"
    description: "Basic addition of two register values"
  - code: "ADD counter, #1 WC  ' Increment with carry"
    description: "Increment counter and update carry flag"
```

### Phase 2: Complete Flag Documentation
**Goal**: Document C and Z flag effects for all 171 instructions

**Required information:**
- When flag is set (1) 
- When flag is cleared (0)
- Mathematical formula if applicable
- Special cases or exceptions

**Template:**
```yaml
flags_affected:
  C:
    formula: "Set if overflow/carry, cleared otherwise"
    description: "Indicates unsigned overflow"
  Z:
    formula: "Set if result = 0"
    description: "Zero result indicator"
```

### Phase 3: Document All Parameters
**Goal**: Clear parameter documentation for 161 files

**Must specify:**
- Parameter name and purpose
- Valid types (register, immediate, augmented)
- Constraints (9-bit literal, 32-bit augmented)
- Optional vs required

### Phase 4: Extract Missing Instructions
**Still missing from manual extraction:**
- 217 instructions without manual content
- Need to find documentation in:
  - Other manual sections
  - Silicon documentation
  - Compiler source comments

### Phase 5: Complete Directive Documentation
**10 directives need improvement:**
- ORG, ORGF, ORGH - memory organization
- RES, FIT - space allocation
- BYTE, WORD, LONG - data declarations

## Quality Verification Checklist

### For Each YAML, verify:
- [ ] **Instruction/directive name** matches official documentation
- [ ] **Syntax** shows all valid forms
- [ ] **Description** ≥ 100 characters of clear explanation
- [ ] **Brief description** ≥ 20 characters summary
- [ ] **Parameters** documented with types and constraints
- [ ] **At least 1 example** with working code
- [ ] **Encoding** present for instructions
- [ ] **Timing** information included
- [ ] **Flags** documented if affected
- [ ] **Related** instructions listed
- [ ] **Usage notes** for special cases
- [ ] **Documentation source** cited

## Success Metrics

### Target: 90%+ Quality Score
- All files score 60%+ (adequate)
- 80% of files score 80%+ (high quality)
- Zero files below 40% (poor)
- Average score ≥ 90%

### Validation Methods:
1. **Automated scoring** via quality assessment script
2. **Compiler validation** of all examples
3. **Cross-reference** with official documentation
4. **Community review** from P2 experts

## Priority Order

1. **Fix the 57 worst files** (score <60%)
2. **Add examples** to most-used instructions
3. **Complete flag documentation** for math/logic group
4. **Document parameters** for all I/O instructions
5. **Extract remaining content** from other sources

## Conclusion

**We know the current YAMLs are NOT at highest quality because:**
- 91% lack examples (critical for AI learning)
- 47% missing flag documentation (affects correctness)
- 45% missing parameter documentation (affects validity)
- Average quality score is only 74.9% (target: 90%+)

**To achieve highest quality, we need:**
- 327 files need examples added
- 171 files need flag documentation
- 161 files need parameter documentation
- 217 files need manual content extraction

**This is achievable through systematic improvement following this plan.**