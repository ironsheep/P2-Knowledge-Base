# Source Code Extraction Methodology

## Overview
Systematic workflow for extracting, validating, and cataloging source code snippets from P2 documentation to create validated code libraries for manual generation and AI training.

## Core Principle
**Extract exactly, validate automatically, human review only failures.**

- **Extraction**: Character-for-character faithful reproduction from documents
- **Validation**: Let `pnut_ts` compiler determine code validity
- **Human Review**: Only address compilation failures or extraction accuracy issues

## Process Steps

### 1. Format Assessment & Preparation

**PDF-First Strategy**: Always prefer PDF format for code extraction

**Why PDF is Critical**:
- **Exact whitespace preservation** - Critical for Spin2 (deeply whitespace sensitive) and PASM2 (whitespace sensitive)
- **Visual fidelity** - What you see is what you extract, no interpretation layer
- **Font-based detection** - Can identify code blocks by monospace font properties
- **No conversion artifacts** - Direct extraction from final formatted document

**Format Decision Tree**:
1. **PDF Available** → Proceed with extraction
2. **DOCX Only** → Request human intervention for PDF
3. **No Source** → Document not ready for code extraction

**Human Escalation Protocol**:
- **Trigger**: Target document only available as DOCX
- **Request**: "Please provide PDF version of [Document] for code extraction"
- **Rationale**: "PDF format ensures exact whitespace preservation critical for P2 code accuracy"
- **Action**: Wait for PDF provision before proceeding

### 2. Automated Code Detection & Extraction

**Input**: PDF documents with embedded source code examples (preferred format)

**Detection Strategy**:
- Scan for monospace font blocks
- Identify indentation patterns consistent with code structure
- Detect language indicators (Spin2 keywords: `PUB`, `PRI`, `VAR`, etc.)
- Recognize PASM2 instruction patterns (`MOV`, `JMP`, `WRLONG`, etc.)

**Extraction Requirements**:
- **Preserve exact whitespace** - tabs stay tabs, spaces stay spaces, exact count
- **Character-for-character accuracy** - no interpretation or "fixing"
- **Complete block extraction** - include all visible code, comments, blank lines

**🔴 CRITICAL: Complete Program Extraction Protocol**

**Issue Identified**: Code programs may span multiple sections or have separated data definitions, leading to incomplete extraction and "Expected a unique name" compilation errors.

**Prevention Strategy**:
1. **Context Scanning**: When extracting any code block, scan ±5 pages for:
   - Variable/constant definitions (`CON` sections)
   - Data declarations (`DAT` sections with values)
   - Method dependencies (referenced `PUB`/`PRI` methods)
   - Include files or dependencies mentioned in comments

2. **Completeness Verification**:
   ```bash
   # Before saving any extracted program:
   # 1. Scan for undefined symbols in comments or error patterns
   # 2. Check for referenced constants/variables not defined in extracted code
   # 3. Look for method calls to undefined procedures
   # 4. Search nearby pages for matching definitions
   ```

3. **Multi-Section Programs**:
   - **CON sections**: Often separated from main program logic
   - **DAT sections**: May contain lookup tables, sync patterns, streamer modes
   - **Method definitions**: Supporting PUB/PRI methods may be on different pages
   - **Assembly blocks**: PASM2 code may reference constants defined elsewhere

4. **Documentation Patterns to Watch**:
   - "Complete program is shown below" → expect all dependencies included
   - "Add these constants" → separate CON section likely exists
   - "Supporting data:" → separate DAT section with required values
   - References to external files (`.bmp`, `.wav`) → note as data dependencies

5. **Extraction Verification Questions**:
   - [ ] Does this program compile without external dependencies?
   - [ ] Are all referenced symbols defined within the extracted code?
   - [ ] Have I captured complete CON/DAT/OBJ sections if present?
   - [ ] Are there hints in surrounding text about missing components?

**Context Capture**:
- **Purpose**: Extract surrounding explanatory text
- **Suggested Filenames**: Capture any filename references in documentation
- **Page/Section Location**: Record source location for traceability
- **Related Assets**: Note any associated images (oscilloscope traces, circuit diagrams)
- **Completeness Indicators**: Note any references to "complete program" or "full listing"

### 2. Metadata & Context Documentation

**Output Format** (Updated - No JSON, Human-Readable Only):

**Individual Source Files**:
- `req01-led-blinking-example.spin2` - Compilable source code
- `req02-smart-pin-config.pasm2` - Assembly code blocks  
- `req03-mixed-spin-pasm.spin2` - Combined language examples

**Human-Readable Catalog** (`code-catalog.md`):
```markdown
## req01: LED Blinking Example
- **File**: `req01-led-blinking-example.spin2`
- **Page**: 45, Lines 23-47
- **Language**: Spin2 | **Type**: Complete Program | **Lines**: 25
- **Validation**: ✅ Compiled successfully
- **Context**: Basic GPIO control demonstration using smart pins
```

**Directory Structure**:
```
/sources/extractions/[document-name]/assets/code-YYYYMMDD/
├── req01-led-blinking-example.spin2
├── req02-smart-pin-config.pasm2
├── req03-mixed-spin-pasm.spin2
└── code-catalog.md
```
```spin2
PUB main()
    pinstart(56, P_HIGH_1MA, 0, 0)    ' Configure P56 as output
    repeat
        pinw(56, 1)                    ' LED on
        waitms(500)
        pinw(56, 0)                    ' LED off  
        waitms(500)
```

**Extraction Status**: Pending validation
```

### 3. Automated Validation Pipeline

**Compilation Testing Process**:
```bash
# Save extracted code with suggested filename or auto-generated name
echo "[extracted code]" > blink_led.spin2

# Attempt compilation with pnut_ts
pnut_ts blink_led.spin2

# Capture results and classify:
# - Exit code 0: Compilation success
# - Exit code 1: Compilation errors  
# - Special handling: Very short blocks (<5 lines) classified as snippets
```

**Classification Logic**:

#### **✅ Complete Programs** 
- Compile successfully with `pnut_ts`
- Typically >10 lines with method definitions
- Can be used as-is for examples or testing

#### **⚠️ Code Snippets**
- <5-10 lines, obviously incomplete fragments
- Examples: single instruction demos, variable declarations
- Document as educational examples, not compilable programs
- **No compilation attempted** - classified by inspection

#### **❌ Compilation Failures**
- Code >10 lines that fails `pnut_ts` validation  
- May indicate extraction errors or missing context
- **Requires human review** for accuracy verification

#### **🔀 Mixed Language Code**
- Spin2 with inline PASM2 blocks
- `pnut_ts` handles mixed code automatically
- Same validation process applies

### 4. Human Review Workflow (Failures Only)

**When compilation fails, create human review entry**:

```markdown
## COMPILATION FAILURE - Human Review Required

### Code req15: Timer Setup Example
**Source**: Smart Pins Documentation, Page 67
**Extracted Filename**: `timer_example.spin2`
**Compilation Error**: 
```
Line 12: Undefined symbol 'CLKFREQ'
Line 18: Expected method declaration
```

**Review Actions Required**:
- [ ] **Visual Comparison**: Compare extracted code against PDF page 67
- [ ] **Context Check**: Look for missing constants, method definitions above/below
- [ ] **Extraction Accuracy**: Verify whitespace, special characters preserved exactly

**Human Decisions**:
- [ ] **Re-extract with more context** (include surrounding code)
- [ ] **Fix obvious extraction error** (missing line, wrong character)
- [ ] **Reclassify as snippet** (incomplete by design, not meant to compile)
- [ ] **Document as broken example** (original documentation has errors)

**Resolution**: [Human fills in after review]
```

### 5. Integration into Knowledge Base Structure

**Directory Structure** (parallel to image extraction):
```
/sources/extractions/[document-name]/
├── assets/
│   ├── images-20250824/           # Image assets  
│   └── code-20250824/             # Code assets (NEW)
│       ├── complete-programs/     # Validated, compilable code
│       ├── code-snippets/         # Educational fragments
│       ├── compilation-failures/  # Code requiring human review
│       └── code-catalog.md        # Master catalog with req## numbering
└── [document-extraction].md       # Main extraction document
```

**Code Asset Integration**:
- **Primary Extraction Owns Code** (same model as images)
- **Specialized Extractions Reference** code assets from primary
- **Consumer Registry System** tracks which documents/manuals need specific code examples
- **req## Numbering** consistent with image extraction (req01, req02, etc.)

### 6. Code Catalog Format

**Master catalog structure**:

```markdown
# P2 Silicon Documentation v35 - Code Catalog
**Extracted**: 2025-08-24
**Source**: P2 Documentation v35 - Rev B_C Silicon.pdf  
**Total Code Blocks**: 15 extracted
**Validation Results**: 8 complete programs, 5 snippets, 2 failures

---

## Code req01: Basic COG Startup ✅
**Type**: Complete Program | **Language**: Spin2 | **Validation**: PASSED

**Source Context**:
- From: P2 Documentation v35, Page 23, Section 2.1
- Purpose: Demonstrates minimal COG initialization
- Filename: `cog_startup.spin2`

**Context Description**:
Basic example showing how to start a new COG with parameter passing...

**Compilation Result**: ✅ Successfully compiles with pnut_ts
**Binary Size**: 1.2KB
**Usage Notes**: Suitable for beginner tutorials, minimal resource usage

---

## Code req02: Hub RAM Access Pattern ⚠️  
**Type**: Code Snippet | **Language**: PASM2 | **Validation**: SKIPPED

**Source Context**:
- From: P2 Documentation v35, Page 45, Section 3.4  
- Purpose: Shows efficient hub RAM reading technique
- Lines: 3 lines (fragment)

**Context Description**:
Demonstrates the RDLONG sequence for burst hub reads...

**Validation Result**: ⚠️ Fragment only - not compilable standalone
**Usage Notes**: Educational example, requires integration into larger program

---

## Code req03: Smart Pin Configuration ❌
**Type**: Compilation Failure | **Language**: Spin2 | **Validation**: FAILED

**Source Context**:
- From: P2 Documentation v35, Page 78, Section 5.2
- Purpose: Complete smart pin setup for PWM output
- Filename: `pwm_setup.spin2`

**Compilation Error**:
```
Line 8: Undefined symbol 'PWM_TRIANGLE'  
Line 15: Method 'configure_pin' not found
```

**Human Review Status**: ❌ PENDING REVIEW
**Suspected Issue**: Missing constant definitions or method dependencies
```

### 7. Consumer Update Automation

**Following image extraction model**:

#### **Primary Extraction Updates** (Immediate)
When code is extracted and validated:
1. **Update code catalog** with new req## entries
2. **Update extraction document** with "CODE ASSETS EXTRACTED" section
3. **Update consumer registry** with available code examples

#### **Secondary Extraction Updates** (Automated)
For specialized extractions referencing primary code:
1. **Update reference files** (`assets/code-20250824.md`) 
2. **Include relevant code examples** automatically
3. **Cross-reference with related images** when applicable

#### **Document Updates** (Technical Debt)
For documentation/manuals consuming code examples:
1. **Add to technical debt queue** for sprint selection
2. **Aggregate available examples** across multiple extraction sessions
3. **Strategic integration** based on manual creation priorities

### 8. Validation Tools Integration

**pnut_ts Integration Points**:
```bash
# Basic validation
pnut_ts extracted_code.spin2

# Generate listings for analysis  
pnut_ts -l extracted_code.spin2

# Quiet mode for batch processing
pnut_ts -q extracted_code.spin2

# Integration with existing validation tools
./tools/validate-pasm-code.sh assets/code-20250824/complete-programs/
```

**Batch Processing Support**:
- Process entire code directories
- Generate validation reports
- Track success/failure rates across extractions
- Identify common failure patterns

### 9. Multi-Session Code Extraction

**Incremental Extraction Process**:
When additional code is found in same document:
1. **Create new timestamped folder**: `/assets/code-20250825/`
2. **Continue req## numbering**: Start from last session's final number
3. **Update master catalog**: Add new session section
4. **Cross-reference**: Link related code examples across sessions

**Session Aggregation**:
```markdown
## Multi-Session Code Assets:
- **Session 1** (2025-08-24): req01-req15 (15 code examples)
- **Session 2** (2025-08-25): req16-req23 (8 additional examples)  
- **Total Available**: 23 validated code examples ready for integration
```

## Benefits Over Manual Code Collection

1. **Systematic Coverage**: No code examples missed from documentation
2. **Validation Confidence**: All code verified by actual P2 compiler
3. **Context Preservation**: Purpose and usage clearly documented
4. **Failure Tracking**: Clear workflow for handling edge cases
5. **Integration Ready**: Direct path from extraction to manual generation
6. **Tool Integration**: Leverages existing `pnut_ts` development environment
7. **Consumer Awareness**: Automated updates to all code consumers
8. **Quality Assurance**: Human review only where automatic validation fails

## Critical Success Factors

### **Extraction Accuracy Requirements**:
- **Character-level precision** in whitespace preservation
- **Complete context capture** including comments and formatting
- **No interpretation** - extract exactly what's written

### **Validation Pipeline Reliability**:
- **pnut_ts integration** must be robust and automated
- **Clear classification** of complete programs vs snippets vs failures
- **Efficient batch processing** for large code collections

### **Human Review Efficiency**:  
- **Minimal human intervention** - only for actual failures
- **Clear problem identification** - specific compilation errors
- **Actionable review workflow** - visual comparison, context checking

### **Integration with Existing Systems**:
- **Directory structure** consistent with image extraction
- **Consumer registry** manages downstream dependencies  
- **Technical debt** system handles strategic manual integration

## File Locations & Organization

### **Source Documents** (Read-only):
- `/sources/originals/*.pdf` - Source PDFs with embedded code
- `/import/p2/*.pdf` - Additional document sources

### **Extracted Code Assets** (Generated):
- `/sources/extractions/[document]/assets/code-YYYYMMDD/complete-programs/`
- `/sources/extractions/[document]/assets/code-YYYYMMDD/code-snippets/`  
- `/sources/extractions/[document]/assets/code-YYYYMMDD/compilation-failures/`
- `/sources/extractions/[document]/assets/code-YYYYMMDD/code-catalog.md`

### **Tools Integration**:
- `tools/pnut_ts` - P2 compiler for validation
- `tools/validate-pasm-code.sh` - Batch validation script
- `tools/source-code-extractor.py` - Code extraction tool (to be developed)

### **Consumer Registry** (Automated Updates):
- `/sources/extractions/[primary]/CODE-CONSUMERS.md`
- `/technical-debt/CODE-ASSETS-DEBT.md`

## Notes

- **Whitespace Sensitivity**: Spin2 is deeply left-edge whitespace sensitive, PASM2 somewhat sensitive
- **Extraction Accuracy Critical**: Wrong indentation = different code meaning  
- **Compiler Authority**: `pnut_ts` is definitive truth for code validity
- **PDF Size Limits**: Same 5MB limits apply as with image extraction
- **Human Review Minimal**: Only compilation failures need human attention
- **Context Rich**: Every code example includes purpose, location, related assets
- **Dashboard Integration**: All extraction work tracked in Operations Dashboard
- **Consumer Awareness**: Extraction results automatically update downstream consumers

*This methodology ensures systematic, validated code extraction with minimal human intervention while maintaining the quality and context needed for effective manual generation and AI training.*

## Dashboard Integration & Operational Tracking

### **Operations Dashboard Updates**

**Location**: `engineering/README.md` → Asset Extraction Status → Code Example Extraction Pipeline

**Metrics to Track**:
- **Extraction Rate**: Documents processed / Total documents with code
- **Validation Success**: Complete programs / Total extractions  
- **Code Asset Count**: Total validated examples available
- **Compilation Rate**: Successful compilations / Attempted validations

**Update Triggers**:
1. **After each document extraction**: Update document status, code counts
2. **After validation batch**: Update success/failure rates
3. **After human review**: Update final validation status

**Dashboard Status Indicators**:
- 🔴 **Critical Gap**: <20% documents processed (urgent action needed)
- 🟡 **In Progress**: 20-80% documents processed (active work phase)  
- 🟢 **Operational**: >80% documents processed (maintenance mode)

### **Code Extraction Matrix Updates**

**Location**: `sources/visual-assets/CODE-EXAMPLE-EXTRACTION-MATRIX.md` (new document)

**Parallel Structure to Image Extraction Matrix**:
```markdown
| Document | Code Examples | Extracted | Validated | Language | Priority |
|----------|---------------|-----------|-----------|----------|-----------|
| **Spin2 Documentation v51** | 267 | 0 → 267 | 245 | Spin2/PASM2 | ✅ Complete |
| **PASM2 Language Manual** | 231 | 0 → 231 | 198 | PASM2/Spin2 | ✅ Complete |
```

**Update Process**:
1. **Before Extraction**: Count estimated code blocks in document
2. **After Extraction**: Update extracted count, note any failures
3. **After Validation**: Update validated count, compilation success rate
4. **Final Status**: Mark as Complete, note human review results

### **Ingestion Source Status Tracking**

**Every extraction document must track code extraction status and human attention needs:**

#### **Main Extraction Document Updates**
**Location**: `/sources/extractions/[document-extraction].md`

**Add these sections to existing extraction documents**:

```markdown
## CODE ASSETS EXTRACTED

### Code Example Collection (2025-08-24)
- **Source**: [Document] code examples extracted and validated
- **Examples Found**: [N] code blocks identified in document
- **Successfully Extracted**: [M] code blocks with preserved formatting
- **Validation Results**: [X] complete programs, [Y] snippets, [Z] failures
- **Asset Location**: `/sources/extractions/[extraction]/assets/code-20250824/`
- **Languages**: Spin2: [A] examples, PASM2: [B] examples, Mixed: [C] examples
- **Compilation Success**: [85%] - [X] programs compile, [Y] snippets (no compilation attempted)
- **Human Review Completed**: [X] failures resolved, [Y] reclassified as snippets
- **Integration Status**: ✅ Assets cataloged and ready for manual generation

### Code Extraction Failures Requiring Human Attention

#### RESOLVED FAILURES ✅
- **req15**: Timer setup example → FIXED: Missing CLKFREQ constant added
- **req23**: Smart pin config → RECLASSIFIED: Fragment only, marked as snippet

#### PENDING HUMAN REVIEW ❌
- **req31**: DMA transfer example (Page 145)
  - **Error**: "Undefined method 'setup_dma'"
  - **Action Needed**: Visual comparison with source PDF
  - **Status**: Awaiting human verification of extraction accuracy

- **req38**: CORDIC calculation (Page 167)  
  - **Error**: "Symbol 'CORDIC_MODE' not found"
  - **Action Needed**: Check for missing context above/below code block
  - **Status**: May need re-extraction with broader context

#### EXTRACTION STATUS SUMMARY
- **Total Code Blocks**: 45 identified
- **Successfully Extracted**: 43 (96% extraction success)
- **Validation Attempted**: 35 (complete programs only)
- **Compilation Success**: 31/35 (89% validation success)
- **Human Review Needed**: 2 failures pending
- **Ready for Integration**: 41 validated examples
```

#### **Status Tracking Files**
**Location**: `/sources/extractions/[document]/assets/code-[date]/`

**Required Status Files**:

1. **`extraction-status.md`** - Master status tracking:
```markdown
# Code Extraction Status - [Document Name]
**Extraction Date**: 2025-08-24
**Document Source**: [PDF/DOCX location]
**Total Pages Processed**: 145

## Extraction Progress
- ✅ **Pages 1-50**: Complete (12 code blocks extracted)
- ✅ **Pages 51-100**: Complete (18 code blocks extracted)  
- ⚠️ **Pages 101-145**: Partial (13 extracted, 2 failed)
- ❌ **Pages 146-162**: Not processed (PDF split required)

## Human Attention Required
### HIGH PRIORITY (Blocks Manual Creation)
- **req31, req38**: Failed compilation, manual review needed
- **Pages 146-162**: PDF too large, requires splitting before extraction

### MEDIUM PRIORITY (Quality Improvement)
- **req12**: Compiles but uses deprecated syntax
- **req25**: Missing explanatory comments

## Next Actions
1. Human review of 2 failed compilations
2. Split PDF pages 146-162 and re-extract  
3. Update deprecated syntax in req12
4. Add context comments to req25
```

2. **`human-review-queue.md`** - Active items needing attention:
```markdown
# Human Review Queue - [Document Name]
**Updated**: 2025-08-24

## IMMEDIATE ACTION REQUIRED ❌

### req31: DMA Transfer Example
**Priority**: 🔴 HIGH (needed for hardware manual)
**Source**: Page 145, Section 8.3
**Error**: "Undefined method 'setup_dma'"
**Estimated Fix Time**: 5-10 minutes
**Action**: Visual comparison with PDF, check for missing context

### req38: CORDIC Calculation  
**Priority**: 🟡 MEDIUM
**Source**: Page 167, Section 9.1
**Error**: "Symbol 'CORDIC_MODE' not found"
**Estimated Fix Time**: 10-15 minutes  
**Action**: Re-extract with broader context, check for constant definitions

## COMPLETED THIS SESSION ✅
- req15: Fixed missing CLKFREQ constant (3 minutes)
- req23: Reclassified as snippet (1 minute)

## TOTAL TIME NEEDED: 15-25 minutes human attention
```

3. **`integration-ready.md`** - Examples ready for use:
```markdown
# Integration Ready Code Examples
**Document**: [Name]
**Ready Examples**: 41 validated code examples

## By Category
### Complete Programs (25 examples)
- req01-req08: Basic GPIO control (LED blinking, button input)
- req15-req22: Smart pin configurations (PWM, ADC, timing)
- req30-req37: CORDIC and math operations

### Code Snippets (16 examples)  
- req09-req14: Single instruction demos
- req23-req29: Variable declaration patterns
- req38-req41: Configuration fragments

## Consumer Notifications
**These examples are now available for**:
- PASM2 Manual v1.0: 15 examples applicable
- Hardware Integration Guide: 8 examples applicable  
- AI Training Corpus: All 41 examples applicable
```

#### **Integration into Existing Extraction Documents**
**Process**: Add "CODE ASSETS EXTRACTED" section alongside existing "VISUAL ASSETS EXTRACTED" sections

**Template for Updates**:
```markdown
[Existing extraction content...]

## VISUAL ASSETS EXTRACTED
[Existing image extraction content...]

## CODE ASSETS EXTRACTED  
[New code extraction content using templates above...]

## COMBINED ASSET SUMMARY
- **Images**: [N] extracted and cataloged
- **Code Examples**: [M] extracted and validated  
- **Integration Status**: Both asset types ready for manual generation
- **Human Review**: [X] images need descriptions, [Y] code examples need review
```

### **Status File Maintenance Protocol**

**Update Schedule**:
1. **During Extraction**: Update `extraction-status.md` after each page batch
2. **After Validation**: Update compilation results, move items between status files
3. **After Human Review**: Mark items complete, update time estimates
4. **Session End**: Final status summary, next session planning

**File Lifecycle**:
- **extraction-status.md**: Permanent record, maintained across sessions
- **human-review-queue.md**: Active work list, items removed when completed  
- **integration-ready.md**: Growing list of available examples

**Cross-Reference Updates**:
- Update main extraction document with summary
- Update dashboard metrics with current status
- Update consumer registry with newly available examples

### **Sprint Planning Integration**

**Code Extraction Work Feeds**:
- **Asset Extraction Pipeline** → Code Example extraction sessions
- **Analysis Debt** → Code pattern analysis and categorization  
- **Technical Debt** → Failed compilation resolution
- **Document Pipeline** → Code examples ready for manual integration

**Sprint Selection Criteria**:
- **High Impact**: Documents with 100+ code examples
- **Developer Value**: Examples that enable production code generation
- **Completion Multiplier**: Extraction sessions that unlock multiple manuals

### **Work Feed Routing Rules** (Updated)

When discovering code extraction needs:
1. **Systematic Extraction Needed** → Asset Extraction Pipeline (Code Matrix)
2. **Code Pattern Analysis** → Analysis Debt  
3. **Validation Tooling Issues** → Technical Debt
4. **Manual Integration Planning** → Document Pipeline
5. **Future Extraction Sessions** → Sprint Candidates (by document priority)

### **Quality Metrics Integration**

**Add to Dashboard Metrics**:
```markdown
### Code Asset Metrics
- **Code Examples Available**: [N] validated examples across [M] documents
- **Compilation Success Rate**: [X%] of extracted code compiles successfully  
- **Language Distribution**: Spin2: [A], PASM2: [B], Mixed: [C]
- **Validation Pipeline Health**: ✅ pnut_ts integration operational
```

**Coverage Enhancement**:
- **Example Coverage**: Track examples per instruction/concept
- **Pattern Coverage**: Code examples demonstrate key P2 patterns
- **Education Coverage**: Examples suitable for learning progression

### **Pipeline Status Integration**

**Add Code Extraction to Active Pipelines**:
```markdown
#### 💻 Code Example Extraction Pipeline
**Status**: 🟢 Operational (methodology established)
**Current**: Processing [Document Name] - [X] examples extracted
**Methodology**: [Source Code Extraction Methodology](pipelines/source-code-extraction-methodology.md)
**Trust Level**: 🟢 pnut_ts validation provides definitive code quality
```

**Pipeline Health Indicators**:
- 🟢 **Operational**: Methodology proven, tools working, regular extractions
- 🟡 **Functional with Issues**: Some documents causing problems, workarounds needed
- 🔴 **Critical Issues**: Extraction failures, validation pipeline broken

### **Consumer Registry Dashboard**

**Track which documents/manuals consume extracted code**:
```markdown
### Code Asset Consumers
- **PASM2 Manual v1.0**: 45 examples ready for integration
- **Spin2 Developer Guide**: 67 examples available
- **Hardware Integration Tutorial**: 23 examples ready
- **AI Training Corpus**: 235 validated examples available
```

**Technical Debt Tracking**:
- Code examples needed but not yet extracted
- Manual sections waiting for specific code examples
- AI training gaps filled by extracted code

This dashboard integration ensures code extraction work is visible, measurable, and properly prioritized alongside other project activities.