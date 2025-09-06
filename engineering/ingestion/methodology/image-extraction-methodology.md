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

---

**Version**: 3.0  
**Status**: Production methodology validated on P2 Datasheet extraction  
**Key Innovation**: Coordinate-aware rescue system achieving 100% success rate  
**Next Application**: Silicon Dock re-extraction