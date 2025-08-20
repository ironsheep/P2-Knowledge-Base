# P2 User Manual Pages Template Setup

**Purpose**: Create a reusable Pages template for P2 user manuals  
**Based on**: Template design specifications from `/exports/templates/p2-user-manual-template-design.md`

## Template Creation Instructions

### Step 1: Create Base Template Document in Pages

1. **Open Pages** and create a new document using "Blank" template
2. **Set page layout**:
   - Format → Document → Page Size: US Letter (8.5" × 11")
   - Format → Document → Margins: Top/Bottom: 1", Left/Right: 1.25"

### Step 2: Configure Typography Styles

Create the following paragraph styles:

#### Primary Heading (H1)
- **Font**: Helvetica Neue Bold, 24pt
- **Color**: #1E3A8A (P2 Blue)
- **Spacing**: 24pt before, 12pt after
- **Name Style**: "P2 Primary Heading"

#### Secondary Heading (H2)
- **Font**: Helvetica Neue Semibold, 18pt  
- **Color**: #374151 (Dark Gray)
- **Spacing**: 18pt before, 9pt after
- **Name Style**: "P2 Secondary Heading"

#### Tertiary Heading (H3)
- **Font**: Helvetica Neue Medium, 14pt
- **Color**: #6B7280 (Medium Gray)
- **Spacing**: 14pt before, 7pt after
- **Name Style**: "P2 Tertiary Heading"

#### Body Text
- **Font**: Helvetica Neue Regular, 11pt
- **Color**: Black (#000000)
- **Line Height**: 1.4
- **Spacing**: 6pt after paragraphs
- **Name Style**: "P2 Body Text"

#### Code Text
- **Font**: SF Mono Regular, 10pt
- **Background**: #F9FAFB (Light Gray)
- **Border**: 1pt solid #E5E7EB
- **Padding**: 8pt all sides
- **Name Style**: "P2 Code Text"

### Step 3: Set Up Headers and Footers

#### Header Setup
- **Insert → Header & Footer → Header**
- **Left side**: "Terminal Window User Manual" (Helvetica Neue Medium, 10pt)
- **Right side**: "P2 Knowledge Base v1.0" (Helvetica Neue Medium, 10pt)
- **Add border**: 0.5pt line below header

#### Footer Setup  
- **Insert → Header & Footer → Footer**
- **Left side**: "© 2025 IronSheep Productions LLC" (Helvetica Neue Regular, 9pt)
- **Center**: Insert → Page Numbers (Helvetica Neue Regular, 9pt)
- **Right side**: "v1.0" (Helvetica Neue Regular, 9pt)
- **Add border**: 0.5pt line above footer

### Step 4: Create Sample Content Structure

Add placeholder sections with proper styling:

```
P2 Terminal Window User Manual [P2 Primary Heading]

Table of Contents [P2 Secondary Heading]

Introduction [P2 Secondary Heading]
Overview [P2 Tertiary Heading]
[P2 Body Text placeholder paragraph]

Prerequisites [P2 Tertiary Heading] 
[P2 Body Text placeholder paragraph]

Terminal Window Basics [P2 Secondary Heading]
Getting Started [P2 Tertiary Heading]
[P2 Body Text placeholder paragraph]

DEBUG Terminal [P2 Tertiary Heading]
[P2 Body Text placeholder paragraph]

[Code example placeholder in P2 Code Text style]

SCOPE Terminal [P2 Tertiary Heading]
[P2 Body Text placeholder paragraph]
```

### Step 5: Add Image Placeholders

1. **Insert → Choose** sample images for layout
2. **Select each image → Format → Advanced → Define as Media Placeholder**
3. **Position**: Center-aligned with captions
4. **Caption style**: Helvetica Neue Italic, 10pt, #6B7280

### Step 6: Save as Template

1. **File → Save as Template**
2. **Template name**: "P2 User Manual Template"
3. **Description**: "Professional template for P2 technical documentation"
4. **Click Save**

## Template Verification

After creating the template, verify:
- ✅ All paragraph styles are properly named and configured
- ✅ Headers and footers appear correctly
- ✅ Image placeholders work properly
- ✅ Typography matches design specifications
- ✅ Color scheme uses P2 brand colors
- ✅ Template appears in "My Templates" section

## Color Reference

For easy copying during setup:
- **P2 Blue**: #1E3A8A
- **Dark Gray**: #374151  
- **Medium Gray**: #6B7280
- **Light Gray Background**: #F9FAFB
- **Border Gray**: #E5E7EB

## File Output

Once template is created and verified, it will be available for:
1. Importing `terminal-window-manual.docx` content
2. Generating professional PDF output
3. Reusing for other P2 user manuals (debugger manual, etc.)

---

**Next Step**: After template creation, follow instructions in `README.md` for importing docx content and generating PDF.