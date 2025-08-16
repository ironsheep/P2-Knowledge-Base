# Image Extraction Methodology

## Overview
Systematic workflow for extracting, documenting, and enriching images from source documents to create informed visual sources for documentation.

## Process Steps

### 1. Claude Creates Consolidated Request
Document: `sources/analysis/screenshots-needed-master.md`

Each entry contains:
- **Image ID**: Sequential number for tracking
- **Source Document**: Which PDF/document it's from
- **Location**: Page number, section heading
- **Document Title**: Title as it appears in source
- **Extraction Target**: Which extraction needs this image
- **Purpose**: Why this image is needed
- **Expected Content**: What Claude expects to see
- **Usage Intent**: How it will be used in final documentation

Example:
```markdown
### Image #1
- **Source**: SPIN2 v51 Documentation
- **Location**: Page 125, Section "DEBUG SCOPE Display"
- **Title**: "Oscilloscope with Anti-aliasing"
- **For Extraction**: Terminal Window Focused Extraction
- **Purpose**: Demonstrates anti-aliasing feature in SCOPE display
- **Expected**: Sine wave with smooth edges showing AA effect
- **Usage**: Terminal Window Manual - Oscilloscope Features section
```

### 2. Stephen Creates Folder Structure
```
/import/p2/
├── parallax-info/     → (move to .personnel-observations/)
├── ironsheep-info/    → (move to .personnel-observations/)
└── images/            → (screenshots go here)
```

### 3. Stephen Captures Images
- Gather all images from source documents
- Save with meaningful names (e.g., `spin2-v51-p125-scope-antialiasing.png`)
- Drop in `/import/p2/images/`

### 4. Claude Generates Image Catalog
Document: `/import/p2/images/image-catalog.md`

Creates numbered markdown with:
- All images embedded
- Original context from request
- Space for Stephen's descriptions

```markdown
## Image #1: Oscilloscope with Anti-aliasing
![Image 1](./spin2-v51-p125-scope-antialiasing.png)

**Source Context**:
- From: SPIN2 v51, Page 125
- Purpose: Demonstrates anti-aliasing in SCOPE display
- For: Terminal Window Manual

**Visual Description**: [Stephen will add]

---
```

### 5. Stephen Provides Visual Descriptions
Reviews catalog and adds descriptions for each image:
- What's visible in the image
- Key features to notice
- How it demonstrates the concept
- Any important details

### 6. Claude Updates Catalog
Incorporates Stephen's descriptions to create final **Informed Image Source**

### 7. Use in Documentation
Images can now be intelligently referenced with:
- Full context of what they show
- Why they're important
- Where they belong in documentation

## Benefits

1. **Context Preservation**: Never lose why an image was captured
2. **Intelligent Usage**: Know exactly when/how to use each image
3. **Efficient Workflow**: Batch processing of images per document
4. **Rich Documentation**: Images become teaching tools, not just illustrations
5. **Traceable Lineage**: Always know source and purpose

## File Locations

- **Request List**: `sources/analysis/screenshots-needed-master.md`
- **Images**: `/import/p2/images/`
- **Catalog**: `/import/p2/images/image-catalog.md`
- **Company Info**: `.personnel-observations/` (after initial import)

## Notes

- Always include page numbers for easy location
- Use descriptive filenames for images
- Keep original titles from documents
- Note any special features visible in screenshots
- Flag any images that need enhancement or annotation