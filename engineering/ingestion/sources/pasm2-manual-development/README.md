# PASM2 Manual Development Directory

**Consolidated materials for developing the official PASM2 instruction manual**

This directory contains all materials related to creating a PASM2 manual that matches the official Parallax format.

---

## Contents

### 📸 **Reference Screenshots**
- `Screenshot 2025-08-18 at 01.44.15.png` - Title page layout
- `Screenshot 2025-08-18 at 01.44.27.png` - Body page with tables  
- `Screenshot 2025-08-18 at 01.44.42.png` - Table of contents
- `Screenshot 2025-08-18 at 01.45.07.png` - Convention/content page

*These screenshots show the official Parallax PASM2 Manual format that we need to replicate*

### 📋 **Format Analysis**
- `format-specifications.md` - Detailed analysis of official format extracted from screenshots
- Contains typography, color scheme, layout specifications

### 🎨 **Template Development**
- Template files are maintained in `/pipelines/templates/p2kb-catalog/`
- `p2kb-pasm2-manual.latex` - Official P2KB template for PASM2 documentation

### 📄 **Test Materials**
- Test content and generation files in `/engineering/pdf-forge/production/pasm2-instruction-test-v1/`

### 🎯 **ADD Instruction Table Examples** *(Missing - Need to Locate)*
- User mentioned two PNG files showing ADD instruction table layouts
- These need to be located and added to this directory

---

## Development Status

### ✅ **Completed**
- Screenshot analysis and format specification extraction
- Basic P2KB template created 
- Test content generation workflow established
- Format specifications documented

### 🔄 **In Progress**
- Consolidating all materials in this directory
- Locating missing ADD instruction table images

### 📋 **Next Steps**
- Find and add the ADD instruction table layout images
- Update P2KB template based on complete format analysis
- Test PDF generation with official format matching
- Refine template based on output quality

---

## Related Locations

- **Template Catalog**: `/pipelines/templates/p2kb-catalog/`
- **PDF Generation**: `/engineering/pdf-forge/production/pasm2-instruction-test-v1/`
- **Original Screenshots**: `/import/images/` (source location)
- **PASM2 Data**: `/sources/extractions/csv-pasm2-instructions-v2.md`

This consolidated approach ensures all PASM2 manual development materials are organized together for efficient development and maintenance.