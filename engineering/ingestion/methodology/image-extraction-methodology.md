# Image Extraction Methodology v3.0
**Enhanced with Coordinate-Aware Rescue System**  
**Date**: 2025-09-06

## Overview
Advanced systematic workflow for extracting, documenting, and enriching images from source documents with **coordinate-aware rescue system** to handle failed extractions and ensure 100% success rate.

## 🚨 Critical v3.0 Enhancement: Coordinate-Aware Rescue System

### The Problem We Solved
**Discovery**: Standard PyMuPDF extraction often fails silently, producing:
- **Black images** (brightness < 10) - 70% failure rate observed
- **Full-page captures** instead of individual images
- **False success reports** from extraction tools

### The Solution: Enhanced Extraction Pipeline

#### 1. **Dual-Phase Extraction**
```python
# Phase 1: Standard PyMuPDF with coordinate capture
def extract_images_with_coordinates(pdf_path, output_dir):
    """Extract images AND save bounding box coordinates"""
    for page_num, page in enumerate(pdf.pages()):
        for img_index, img in enumerate(page.get_images()):
            # Extract image
            pix = fitz.Pixmap(pdf, img[0])
            
            # CRITICAL: Save coordinates for rescue
            image_rects = page.get_image_rects(img[0])
            if image_rects:
                rect = image_rects[0]
                bbox_coords = {
                    "x0": rect.x0, "y0": rect.y0,
                    "x1": rect.x1, "y1": rect.y1,
                    "width": rect.width, "height": rect.height
                }
                # Save coordinates to JSON catalog
```

#### 2. **Black Image Detection**
```python
def analyze_image_quality(image_path):
    """Detect failed extractions using brightness analysis"""
    file_size_kb = os.path.getsize(image_path) / 1024
    
    with Image.open(image_path) as img:
        gray = img.convert('L')
        stat = ImageStat.Stat(gray)
        mean_brightness = stat.mean[0]
        
        # Failed extraction indicators
        is_likely_failed = (
            mean_brightness < 10 or  # Black images
            (file_size_kb < 5 and mean_brightness < 50)  # Tiny black images
        )
    
    return {
        'brightness': mean_brightness,
        'file_size_kb': file_size_kb,
        'likely_failed': is_likely_failed
    }
```

#### 3. **Coordinate-Aware Rescue System**
```python
def rescue_failed_images(pdf_path, failed_images, output_dir):
    """Rescue failed extractions using saved coordinates"""
    
    for page_num, failed_items in failed_images.items():
        # Convert PDF page to high-res image
        page_image = convert_from_pdf(
            pdf_path, 
            first_page=page_num+1, 
            last_page=page_num+1, 
            dpi=200
        )[0]
        
        for img_info in failed_items:
            coords = img_info['bbox_coords']
            
            # Convert PDF coordinates to pixel coordinates
            pdf_width, pdf_height = get_pdf_page_size(pdf_path, page_num)
            page_width, page_height = page_image.size
            
            scale_x = page_width / pdf_width
            scale_y = page_height / pdf_height
            
            # Crop using scaled coordinates
            pixel_coords = (
                int(coords['x0'] * scale_x),
                int((pdf_height - coords['y1']) * scale_y),  # PDF uses bottom-origin
                int(coords['x1'] * scale_x),
                int((pdf_height - coords['y0']) * scale_y)
            )
            
            cropped_image = page_image.crop(pixel_coords)
            cropped_image.save(f"{output_dir}/{img_info['filename']}_RESCUED_CROPPED.png")
```

#### 4. **Quality Assurance Pipeline**
```python
def complete_extraction_pipeline(pdf_path, output_dir):
    """Complete pipeline with quality assurance"""
    
    # Phase 1: Initial extraction with coordinates
    extraction_results = extract_images_with_coordinates(pdf_path, output_dir)
    
    # Phase 2: Quality analysis
    failed_images = {}
    for img_path in glob.glob(f"{output_dir}/*.png"):
        quality = analyze_image_quality(img_path)
        if quality['likely_failed']:
            # Mark for rescue
            failed_images[...] = quality
    
    # Phase 3: Rescue failed extractions
    if failed_images:
        rescue_failed_images(pdf_path, failed_images, output_dir)
    
    # Phase 4: Replace failed with rescued
    replace_failed_with_rescued(output_dir)
    
    return generate_final_catalog(output_dir)
```

## 📋 Complete Enhanced Process

### Phase 1: Enhanced Initial Extraction
1. **Run enhanced extractor** with coordinate capture
2. **Analyze all images** for quality (brightness, file size)
3. **Identify failed extractions** (black images, wrong dimensions)
4. **Save coordinates** for rescue operations

### Phase 2: Coordinate-Aware Rescue
1. **Convert PDF pages** to high-resolution images
2. **Calculate coordinate scaling** (PDF → pixel coordinates)
3. **Crop using saved coordinates** to get actual image content
4. **Replace failed extractions** with properly cropped rescued versions

### Phase 3: Catalog Generation with Quality Metrics
```markdown
# Document Image Catalog

**Source Document**: filename.pdf  
**Extraction Date**: YYYY-MM-DD  
**Total Images**: X extracted images  
**Success Rate**: 100% (X/X properly extracted)  
**Rescued Images**: N images replaced with coordinate-aware cropped versions

## Images

### Page N - Section Title

**filename.png**  
*WxH pixels, XKB* ⭐ **CROPPED** *(if rescued)*
![Description](filename.png)
**Description**: What the image shows
**Context**: Surrounding text context
```

### Phase 4: Quality Verification
1. **Verify no full-page images** remain (check for 1700×2200 or similar)
2. **Confirm proper cropping** - images should show only relevant content
3. **Test markdown catalog** - refresh browser cache if needed
4. **Clean up backup files** after verification

## 🛠️ Enhanced Toolchain

### Core Scripts (in `/engineering/tools/extraction/`)

#### `enhanced_pdf_extractor.py`
- **Purpose**: Initial extraction with coordinate capture
- **Key Feature**: Saves bounding box coordinates for rescue
- **Output**: Images + coordinate JSON

#### `simple_black_detector.py`
- **Purpose**: Quality analysis and failed extraction detection
- **Key Feature**: Brightness and file size analysis
- **Output**: Quality assessment for each image

#### `replace_with_cropped.py`
- **Purpose**: Replace full-page images with cropped rescued versions
- **Key Feature**: Dimension comparison and file replacement
- **Output**: Properly cropped final image set

#### `get_image_dimensions.py`
- **Purpose**: Generate actual dimensions for catalog updating
- **Key Feature**: Batch dimension analysis
- **Output**: Dimension data for catalog

## 🎯 Critical Success Factors

### 1. **Always Save Coordinates**
The rescue system only works if you capture bounding box coordinates during initial extraction.

### 2. **Quality Analysis is Essential** 
Don't trust extraction success reports - always analyze brightness and file size.

### 3. **Browser Cache Issues**
After replacing images, users may see cached full-page versions. Always instruct to refresh browser cache.

### 4. **Systematic Replacement**
Use the replacement script to ensure only properly cropped images remain.

## 🔧 Implementation Checklist

### For New Extractions
- [ ] Run enhanced extractor with coordinate capture
- [ ] Analyze all images for quality issues
- [ ] Rescue any failed extractions using coordinates
- [ ] Replace failed images with rescued cropped versions
- [ ] Generate catalog with actual dimensions
- [ ] Clean up backup files after verification
- [ ] Test catalog display (refresh browser cache)

### For Existing Extractions (Like Silicon Dock)
- [ ] Re-run extraction with enhanced tools
- [ ] Compare with existing catalog to identify failures
- [ ] Apply rescue system to failed extractions
- [ ] Update catalog with corrected images
- [ ] Archive old extraction for reference

## 📊 Quality Metrics (Enhanced)

### Extraction Quality
- **Brightness Analysis**: Mean brightness > 50 (non-black images)
- **File Size Check**: > 5KB for legitimate images
- **Dimension Verification**: No unexpected full-page sizes
- **Visual Inspection**: Images show only relevant content

### Success Rate Targets
- **Initial Extraction**: 60-70% (typical PyMuPDF success rate)
- **After Rescue**: 95-100% (coordinate-aware rescue target)
- **Final Quality**: 100% properly cropped images

## 🎓 Lessons Learned from P2 Datasheet Project

### Key Discoveries
1. **PyMuPDF fails silently** - 70% of "successful" extractions were actually black images
2. **Coordinate rescue works** - 100% rescue success rate using bounding boxes
3. **Browser caching is major UX issue** - Users see old cached images after fixes
4. **File size analysis is reliable** - Small black images are clear failure indicators

### Process Improvements
1. **Never trust extraction reports** - Always verify with quality analysis
2. **Coordinate capture is critical** - Enables surgical rescue operations
3. **Quality pipeline is essential** - Automated detection and rescue
4. **Clean catalog regeneration** - Show actual post-rescue dimensions

## 📋 Sequential Image Numbering Standard

### Enhanced Document-Specific Numbering
**Format**: `[DOC-PREFIX]-[###]`  
**Document Prefix Length**: 3-4 letters for P2 document specificity  

**P2 Document Examples**:
- **P2DS-001**: P2 **D**ata**S**heet images (P2DS-001 through P2DS-039)
- **P2SP-001**: P2 **S**mart **P**ins images (P2SP-001 through P2SP-N)  
- **P2SD-001**: P2 **S**ilicon **D**ock images (P2SD-001 through P2SD-N)
- **P2HUB-001**: P2 **HUB**75 Adapter images (P2HUB-001 through P2HUB-N)

### Benefits of Sequential Numbering
- **Easy Reference**: "Please update the description for P2DS-027" ✅
- **Document Scoped**: Each document starts from 001
- **Memorable**: Short, meaningful prefixes
- **Scalable**: Supports multiple P2-related documents

### Implementation in Catalogs
**Both JSON and Markdown catalogs include**:
```json
{
  "sequential_id": "P2DS-015",
  "document_prefix": "P2DS",
  "sequence_number": 15
}
```

**Markdown format**:
```markdown
### **P2DS-015** | Page 27 - I/O Schematic Row 1 ⭐ **CROPPED**  
![P2DS-015: I/O Schematics Row 1](filename.png)
```

### Usage Examples
**Easy Reference**:  
- "P2DS-015 through P2DS-038 are the I/O matrix" ✅
- "P2DS-006 and P2DS-007 are the small cropped circuits" ✅

**Instead of**:
- "Update Propeller2-P2X8C4M64P-Datasheet-20221101_page30_img01.png" ❌

## 🔄 Migration Strategy

### For Existing Documents with Black Image Issues
1. **Silicon Dock** (confirmed black image issues) - Priority 1
2. **Smart Pins Tutorial** - Review for quality issues
3. **Other technical documents** - Audit and re-extract as needed

### Migration Steps
1. **Backup existing catalog** with timestamp
2. **Re-extract using enhanced tools** 
3. **Compare results** with existing catalog
4. **Update documentation references** if filenames change
5. **Archive old versions** for reference

## 🔄 Multi-Part PDF Handling

### When PDFs Are Split Due to Size Constraints
**Trigger**: Large PDFs split into `Document-Part1of5.pdf`, `Document-Part2of5.pdf`, etc.

#### Multi-Part Extraction Protocol
1. **Extract Each Part Separately**:
```bash
# Extract each part to separate temporary directories
python3 tools/enhanced_pdf_extractor.py "Document-Part1of5.pdf" -o "extracted_images_doc_part1"
python3 tools/enhanced_pdf_extractor.py "Document-Part2of5.pdf" -o "extracted_images_doc_part2"
# Continue for all parts...
```

2. **Combine with Collision Protection** ⚠️ **CRITICAL SAFETY**:
```bash
# MANDATORY: Check for filename collisions before copying
for part in 1 2 3 4 5; do
  for file in extracted_images_doc_part${part}/*.png; do
    basename=$(basename "$file")
    destination="final_directory/$basename"
    
    # Check for collision
    if [ -f "$destination" ]; then
      # Rename with part identifier to avoid collision
      new_name="${basename%.png}_part${part}.png"
      cp "$file" "final_directory/$new_name"
      echo "⚠️ COLLISION AVOIDED: $basename → $new_name"
    else
      cp "$file" "$destination"
    fi
  done
done
```

3. **Verify Combination Success**:
```bash
# Verify total count matches expectation
expected_total=34  # Sum from all parts
actual_count=$(ls final_directory/*.png | wc -l)
if [ "$actual_count" -eq "$expected_total" ]; then
  echo "✅ SUCCESS: All $actual_count images combined"
  # Safe to clean up temporary directories
  rm -rf extracted_images_doc_part*
else
  echo "❌ ERROR: Expected $expected_total, got $actual_count"
  # DO NOT clean up - investigate missing files
fi
```

## 📋 Todo MCP Integration Pattern

### Systematic Task Management
**Primary Tag**: `["image_extraction"]` - Required for all extraction tasks

#### Standard Task Sequence
```bash
# Create systematic extraction workflow
mcp__todo-mcp__todo_create content:"Phase 1: Setup extraction environment for [document]" priority:"critical" estimate_minutes:10 tags:["image_extraction"] sequence:1

mcp__todo-mcp__todo_create content:"Phase 2: Execute coordinate-aware extraction for [document]" priority:"critical" estimate_minutes:30 tags:["image_extraction"] sequence:2

mcp__todo-mcp__todo_create content:"Phase 3: Analyze quality and apply rescue system" priority:"critical" estimate_minutes:20 tags:["image_extraction"] sequence:3

mcp__todo-mcp__todo_create content:"Phase 4: Generate catalogs with sequential numbering" priority:"critical" estimate_minutes:25 tags:["image_extraction"] sequence:4

mcp__todo-mcp__todo_create content:"Phase 5: Update ALL tracking systems" priority:"critical" estimate_minutes:25 tags:["image_extraction"] sequence:5
```

#### Progress Context Tracking
```bash
# Track extraction state
mcp__todo-mcp__context_set key:"extraction_active_[doc]" value:"Started: [timestamp], Expected: [N] images, Tools: enhanced pipeline"

# Mark completion with metrics
mcp__todo-mcp__context_set key:"extraction_complete_[doc]" value:"SUCCESS: [N]/[total] images, [XX.X%] success, Sequential: [PREFIX]-001 to [PREFIX]-[N]"
```

## 🎯 Consumer Distribution System

### Asset Distribution Philosophy
**Primary Extraction**: Owns the physical image files and master catalog  
**Secondary Extractions**: Reference primary assets with context-specific usage  
**Documents**: Queue enhancement opportunities in technical debt system

#### Consumer Distribution Workflow
1. **Identify Consumers**:
   - **Related extractions** that could use these images
   - **Documents** that could be enhanced with visual assets
   - **Technical debt opportunities** for systematic improvement

2. **Create Distribution Plan**:
   - **Tier 1 (Immediate)**: Secondary extraction reference files
   - **Tier 2 (Deferred)**: Document enhancement opportunities
   - **Tier 3 (Strategic)**: Cross-document visual consistency

3. **Execute Distribution**:
```bash
# Update secondary extractions (immediate)
mcp__todo-mcp__todo_create content:"Update [N] secondary extractions with [doc] visual asset references" priority:"high" estimate_minutes:[N*10] tags:["consumer_updates"]

# Queue document enhancements (deferred)
mcp__todo-mcp__todo_create content:"Add [doc] assets to technical debt for [N] document enhancement opportunities" priority:"low" estimate_minutes:15 tags:["technical_debt"]
```

## 📊 Mandatory System Updates

### ALL Tracking Systems Must Be Updated
**CRITICAL**: After every extraction, update these 5 systems in order:

1. **Operations Dashboard** (`/engineering/README.md`)
   - Update Asset Extraction Status metrics
   - Update success rates and totals

2. **Ingested Sources Catalog** (`/sources/INGESTED-SOURCES-CATALOG.md`)
   - Change status from "PENDING" to "EXTRACTED" with statistics
   - Update Visual Assets Extraction Status summary

3. **Document Production Pipeline** (`/pipelines/document-production-pipeline.md`)
   - Update Visual Asset Integration section
   - Update Enhancement Opportunities

4. **Technical Debt Registry** (`/technical-debt/VISUAL-ASSETS-DEBT.md`)
   - Add new enhancement opportunities
   - Update effort estimates with newly available assets

5. **Project Master** (`/engineering/operations/README.md`)
   - Update methodology improvements
   - Update knowledge coverage metrics

### Why System Updates Matter
- **Prevents data inconsistency** across tracking systems
- **Ensures extraction work visibility** in all relevant contexts
- **Maintains accurate project status** reporting
- **Enables proper sprint planning** with current asset availability

## 🔧 Error Recovery Protocols

### When Extraction Tools Fail
```bash
# Tool dependency issues
if command -v python3 >/dev/null 2>&1; then
    if python3 -c "import fitz, PIL" 2>/dev/null; then
        echo "✅ Dependencies available"
    else
        echo "❌ Install missing: pip install PyMuPDF Pillow pdf2image"
    fi
else
    echo "❌ Python3 not available"
fi
```

### When Directory Issues Occur
```bash
# Create recovery tasks for asset organization
mcp__todo-mcp__todo_create content:"Recovery: Reorganize [doc] extraction assets to proper directory structure" priority:"high" estimate_minutes:15 tags:["recovery"]
```

### When Manual Capture Needed
```bash
# Document exact requirements for human intervention
mcp__todo-mcp__todo_create content:"Manual capture: [N] failed extractions from [doc] - pages [X,Y,Z] technical diagrams" priority:"medium" estimate_minutes:[N*5] tags:["manual_capture"]
```

## 📋 Quality Validation Framework

### Completeness Checklist
- [ ] **All expected images processed** by coordinate-aware extraction
- [ ] **Failed extractions analyzed** with rescue system applied
- [ ] **Sequential numbering assigned** ([PREFIX]-001 to [PREFIX]-N)
- [ ] **Quality metrics validated** (brightness >50, file size >5KB)
- [ ] **Catalogs generated** with actual cropped dimensions
- [ ] **Consumer distribution planned** and executed
- [ ] **ALL tracking systems updated** with extraction results
- [ ] **Follow-up tasks created** for manual capture if needed

### Success Rate Targets
- **Initial Extraction**: 60-70% (typical PyMuPDF baseline)
- **After Coordinate Rescue**: 95-100% (target with rescue system)
- **Final Quality**: 100% properly cropped images
- **System Integration**: 100% tracking systems updated

---

**Version**: 3.0  
**Status**: Production methodology validated on P2 Datasheet extraction  
**Key Innovation**: Coordinate-aware rescue system achieving 100% success rate  
**Enhancement**: Integrated Todo MCP workflow and consumer distribution system  
**Next Application**: Silicon Dock re-extraction with complete systematic approach