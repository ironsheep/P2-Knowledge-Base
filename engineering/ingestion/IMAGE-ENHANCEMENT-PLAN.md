# Image Enhancement Plan - Spin2 v51 & Silicon Doc
**Date**: 2025-09-01  
**Priority**: High - Both have .docx sources available

## Document Assessment

### 1. Spin2 Documentation v51
**Current State**:
- ✅ PDF extracted: 25 images in `/assets/images-20250824/`
- ✅ Basic catalog exists: `image-catalog.md`
- ✅ .docx available: `Parallax Spin2 Documentation v51.docx`
- ❌ No global IDs
- ❌ No .docx context mining
- ❌ No enhanced metadata

**Images Present**: 25 PNG files
- Debug terminal windows (pages 25-48)
- Primarily IDE screenshots and debug displays
- Terminal output examples

**Enhancement Opportunities**:
- Mine .docx for command descriptions
- Map images to specific debug commands
- Add terminal window context
- Create SPIN-IMG-XXX global IDs

### 2. Silicon Documentation v35
**Current State**:
- ✅ PDF available: 5-part document
- ✅ .docx available: `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx`
- ⚠️ Partial extraction in `/assets/`
- ❌ No consolidated image catalog
- ❌ No global IDs
- ❌ No .docx context mining

**Known Content**:
- Instruction timing diagrams
- Pipeline illustrations
- Memory maps
- Pin configuration diagrams
- Hub/Cog interaction diagrams

**Enhancement Opportunities**:
- Extract ALL images from 5-part PDF
- Mine .docx for technical descriptions
- Create SIL-IMG-XXX global IDs
- Map to instruction set documentation

## Enhancement Workflow

### Phase 1: Spin2 v51 Enhancement (2-3 hours)

#### Step 1: Extract .docx Narrative
```bash
# Extract clean text from Spin2 .docx
pandoc -f docx -t plain "Parallax Spin2 Documentation v51.docx" \
  -o spin2-v51-narrative.txt
```

#### Step 2: Create Enhanced Extractor
```python
# spin2_image_enhancer.py
class Spin2ImageEnhancer:
    def __init__(self):
        self.doc_id = "SPIN"
        self.debug_patterns = {
            'debug_commands': r'DEBUG\s+\w+',
            'terminal_modes': r'(PLOT|SCOPE|TERM|LOGIC)',
            'window_types': r'(Output|Input|Status|Watch)'
        }
```

#### Step 3: Apply Enhancements
- Global IDs: SPIN-IMG-001 through SPIN-IMG-025
- Context mapping from .docx narrative
- Debug command associations
- Terminal window type classification

#### Step 4: Generate Enhanced Catalog
```markdown
# Spin2 v51 - Enhanced Visual Asset Catalog
**Document ID**: SPIN
**Total Images**: 25 debug terminal windows
**Enhancement**: .docx narrative context added

### Debug Terminal Windows
#### SPIN-IMG-001 - Page 25
**Context**: DEBUG terminal output display
**Command**: DEBUG command with TERM mode
**Purpose**: Shows basic terminal output formatting
```

### Phase 2: Silicon Doc Enhancement (4-5 hours)

#### Step 1: Complete Image Extraction
```python
# Extract from all 5 PDF parts
for part in [1, 2, 3, 4, 5]:
    extract_images(f"Silicon-Part{part}of5.pdf")
```

#### Step 2: Extract .docx Narrative
```bash
# Extract narrative from Silicon .docx
pandoc -f docx -t plain \
  "Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx" \
  -o silicon-v35-narrative.txt
```

#### Step 3: Domain-Specific Enhancement
```python
# silicon_image_enhancer.py
class SiliconImageEnhancer:
    def __init__(self):
        self.doc_id = "SIL"
        self.technical_patterns = {
            'instructions': r'[A-Z]{3,6}\s+[SD],',
            'timing': r'\d+\s*clocks?',
            'pipeline': r'(stage|pipeline|fetch|decode|execute)',
            'memory': r'(hub|cog|lut|ram)'
        }
```

#### Step 4: Technical Context Mapping
- Instruction timing diagrams → specific PASM2 instructions
- Pipeline diagrams → execution stages
- Memory maps → address ranges
- Pin diagrams → I/O configurations

## Implementation Schedule

### Day 1: Spin2 v51 (Today)
**Morning**:
1. [ ] Set up enhanced extractor for Spin2
2. [ ] Extract .docx narrative
3. [ ] Create global ID mapping

**Afternoon**:
1. [ ] Apply context enhancements
2. [ ] Generate enhanced catalog
3. [ ] Archive old catalog
4. [ ] Update references

### Day 2: Silicon Doc
**Morning**:
1. [ ] Extract all images from 5-part PDF
2. [ ] Extract .docx narrative
3. [ ] Create initial catalog with global IDs

**Afternoon**:
1. [ ] Apply technical context mapping
2. [ ] Classify by instruction/component
3. [ ] Generate enhanced catalog
4. [ ] Update documentation

## Expected Outcomes

### Spin2 v51 Enhanced Catalog
- 25 images with SPIN-IMG-XXX IDs
- Debug command context for each image
- Terminal window type classification
- Narrative descriptions from .docx
- Searchable metadata for documentation

### Silicon Doc Enhanced Catalog
- Est. 40-60 images with SIL-IMG-XXX IDs
- Instruction timing associations
- Pipeline stage mappings
- Memory region classifications
- Technical narrative context

## Success Metrics

### Quality Indicators
- [ ] All images have global IDs
- [ ] All images have .docx context
- [ ] Domain-specific patterns applied
- [ ] Visual verification complete
- [ ] Catalogs human-readable

### Documentation Updates
- [ ] Old catalogs archived
- [ ] References updated
- [ ] Extraction audits updated
- [ ] Dashboard reflects enhancements

## Tools Required

### Scripts to Create
1. `spin2_image_enhancer.py` - Spin2-specific enhancement
2. `silicon_image_enhancer.py` - Silicon Doc enhancement
3. `extract_all_parts.py` - Multi-part PDF extraction

### Existing Tools to Use
- `pdf_image_extractor_enhanced.py` - Base extractor
- `generate_enhanced_catalog.py` - Catalog generator
- pandoc - .docx text extraction

## Risk Mitigation

### Potential Issues
1. **Large Silicon Doc** - 5 parts might have many images
   - Mitigation: Process in batches, create progress tracking

2. **Technical complexity** - Silicon Doc very technical
   - Mitigation: Focus on clear categories first

3. **Existing references** - Many documents reference current catalogs
   - Mitigation: Careful reference tracking, systematic updates

## Long-term Benefits

### For Spin2 v51
- Better debug documentation
- Searchable terminal examples
- Clear command-to-output mapping

### For Silicon Doc
- Complete technical reference
- Instruction timing clarity
- Architecture visualization improvement

### For Project
- Establishes pattern for remaining documents
- Improves AI understanding of P2 architecture
- Creates reusable enhancement tools

---

**Ready to Begin**: Spin2 v51 enhancement can start immediately  
**Next Session**: Silicon Doc after Spin2 complete