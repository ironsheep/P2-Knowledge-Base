# PASM2 Manual Generation Workflow
*Template-based instruction documentation system*

## Overview
This workflow enables systematic documentation of all 491 PASM2 instructions using templates that can be individually edited, verified, and combined into a complete manual.

## Directory Structure

```
/engineering/document-production/manuals/pasm2-reference/
├── PASM2-MANUAL-WORKFLOW.md              (this file)
├── instruction-templates/                 (individual instruction files)
│   ├── categories/                       (category templates)
│   │   ├── math-instruction.md
│   │   ├── bit-operation.md
│   │   ├── indirection-instruction.md
│   │   ├── io-smart-pin.md
│   │   ├── branch-instruction.md
│   │   ├── directive.md
│   │   └── cordic-instruction.md
│   ├── completed/                        (reviewed & finalized)
│   ├── in-progress/                      (being edited)
│   └── generated/                        (auto-generated from data)
├── assembly/                              (manual assembly scripts)
│   ├── combine-instructions.py
│   ├── generate-toc.py
│   └── validate-templates.py
├── output/                                (generated manuals)
│   ├── pasm2-reference-manual.md
│   └── pasm2-reference-manual.pdf
└── tracking/
    ├── instruction-status.yaml           (tracks which instructions are done)
    └── coverage-report.md                (visual progress tracking)
```

## Instruction Categories & Templates

Based on the examples (ADDSX, ALIGNL, ALTI), we have different template structures:

### 1. Math Instructions (like ADDSX)
**Template sections:**
- Syntax
- Result
- Parameters
- Encoding table
- Explanation
- Related instructions
- Examples
- Use cases
- Notes

### 2. Directives (like ALIGNL)
**Template sections:**
- Syntax
- Result
- Parameters  
- Explanation
- Memory layout diagram
- Example
- Related directives
- Use cases
- Notes

### 3. Indirection Instructions (like ALTI)
**Template sections:**
- Syntax
- Result
- Parameters
- Encoding table
- Template format diagram
- Configuration format
- Control tables
- Explanation
- Examples
- Related instructions
- Use cases
- Notes

## Workflow Process

### Phase 1: Template Generation (Automated)
```python
# 1. Extract documented instructions from ingested PASM2 manual
# 2. Categorize each instruction by type
# 3. Generate initial template based on category
# 4. Populate with available data
# 5. Mark gaps that need manual input
```

### Phase 2: Manual Enhancement
1. **Review generated template**
   - Verify technical accuracy
   - Check encoding information
   - Validate examples

2. **Fill gaps**
   - Add missing explanations
   - Create practical examples
   - Document use cases
   - Add diagrams where helpful

3. **Quality checks**
   - Test code examples with pnut_ts compiler
   - Cross-reference with datasheet
   - Verify encoding against CSV data

### Phase 3: Assembly
1. **Organize by alphabet** (standard reference order)
2. **Generate table of contents**
3. **Add cross-references**
4. **Create index**
5. **Generate final markdown**
6. **Convert to PDF via PDF Forge**

## Template Status Tracking

```yaml
# instruction-status.yaml
instructions:
  ABS:
    status: completed
    category: math
    source: pasm2-manual
    reviewed_by: user
    review_date: 2025-01-19
    
  ADD:
    status: in-progress
    category: math
    source: pasm2-manual
    gaps: [examples, use_cases]
    
  ADDSX:
    status: completed
    category: math
    source: template-example
    reviewed_by: user
    review_date: 2025-01-19
```

## Generation Script Concept

```python
# combine-instructions.py
def generate_manual():
    # 1. Load all completed templates
    # 2. Sort alphabetically
    # 3. Generate section headers
    # 4. Insert category dividers
    # 5. Build cross-reference links
    # 6. Output complete manual
```

## Quality Assurance

### Validation Steps
1. **Syntax validation** - All templates follow structure
2. **Encoding verification** - Match CSV spreadsheet
3. **Example testing** - Compile with pnut_ts
4. **Cross-reference check** - All "Related" links valid
5. **Coverage audit** - Track missing instructions

### Review Process
1. Auto-generated → in-progress/
2. Manual review/edit
3. Technical validation
4. Move to completed/
5. Include in next manual build

## Benefits of This Approach

1. **Modular** - Each instruction is independent
2. **Trackable** - Clear progress visibility
3. **Reviewable** - Easy to verify individual instructions
4. **Reusable** - Templates can be updated independently
5. **Collaborative** - Multiple people can work on different instructions
6. **Version controlled** - Git tracks all changes
7. **Quality controlled** - Each instruction verified before inclusion

## Next Steps

1. **Generate category templates** for each instruction type
2. **Create extraction script** to populate from existing data
3. **Build tracking dashboard** for progress monitoring
4. **Implement validation tools** for quality assurance
5. **Design LaTeX template** for professional PDF output

## Manual Assembly Commands

```bash
# Generate initial templates from ingested data
python3 generate-templates.py

# Validate all templates in completed/
python3 validate-templates.py

# Combine into full manual
python3 combine-instructions.py

# Generate PDF via PDF Forge
# (copy to pdf-forge production folder)
```

## Estimated Coverage

From existing sources:
- **315 instructions** have descriptions (PASM2 manual)
- **176 instructions** need descriptions
- **491 total** instructions to document

With template approach:
- Week 1: Generate all 491 templates with available data
- Week 2-3: Fill gaps for 176 undocumented instructions
- Week 4: Review, validate, and assemble complete manual

## Success Metrics

- [ ] All 491 instructions have templates
- [ ] 100% encoding accuracy vs CSV
- [ ] All examples compile with pnut_ts
- [ ] Cross-references validated
- [ ] PDF generation successful
- [ ] Manual reviewed by P2 experts