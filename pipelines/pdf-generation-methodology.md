# PDF Generation Methodology

## Overview
Systematic workflow for converting markdown documentation to professional PDFs using doc-forge LaTeX templates and the outbound/inbound directory system.

## P2KB Template Naming Convention

**All P2 Knowledge Base templates MUST use the P2KB prefix:**

**Format**: `p2kb-[purpose].latex`
- **Prefix**: `p2kb-` (Papa Two Kilo Bravo)
- **Purpose**: Descriptive name (pasm2-manual, user-guide, debug-manual)
- **Extension**: `.latex` for LaTeX template files

**Examples**:
- `p2kb-pasm2-manual.latex` - PASM2 instruction documentation
- `p2kb-user-guide.latex` - User guide formatting  
- `p2kb-debug-manual.latex` - Debug/terminal documentation

**Benefits**:
- Prevents conflicts with existing doc-forge templates
- Clear P2 Knowledge Base ownership
- Easy identification and grouping
- Consistent project branding

## Process Steps

### 1. Prepare Export Directory Structure
Create organized export directory for each document:
```
/exports/[document-name]/
├── [document-name].docx          ← Generated from markdown
├── pages-template-setup.md       ← Template creation instructions  
├── README.md                     ← Import and generation instructions
└── [document-name].pdf           ← Final output (after Stephen generates)
```

### 2. Generate Docx from Markdown
**Command**: `pandoc [source].md -o [target].docx`
- Preserves formatting and image placeholders
- Maintains structural hierarchy
- Creates importable content for Pages

### 3. Create Pages Template Setup Instructions
**Based on research findings**:
- Pages templates must be created within Pages application
- Cannot be distributed as standalone files
- Require manual setup following detailed specifications

**Template Creation Process**:
1. Create blank Pages document
2. Configure page layout (US Letter, margins)
3. Set up typography styles with proper naming
4. Configure headers/footers with brand elements
5. Add image placeholders
6. Save as template within Pages

### 4. Document Template Specifications
**Typography Hierarchy**:
- **H1**: Helvetica Neue Bold, 24pt, P2 Blue (#1E3A8A)
- **H2**: Helvetica Neue Semibold, 18pt, Dark Gray (#374151)  
- **H3**: Helvetica Neue Medium, 14pt, Medium Gray (#6B7280)
- **Body**: Helvetica Neue Regular, 11pt, Black
- **Code**: SF Mono Regular, 10pt, Light Gray background

**Page Elements**:
- **Header**: Document title (left), P2 Knowledge Base v1.0 (right)
- **Footer**: Copyright (left), page numbers (center), version (right)
- **Margins**: 1" top/bottom, 1.25" left/right

### 5. Create Import Instructions
**README.md contents**:
1. Template setup instructions (one-time)
2. Docx import process
3. PDF generation steps
4. Feedback/iteration cycle

### 6. Establish Feedback Cycle
**Iteration Process**:
- Stephen generates PDF using template + docx
- Reviews PDF, provides feedback
- Claude makes changes to source markdown
- Claude re-exports docx
- Stephen regenerates PDF
- Repeat until approved

**Final Asset Integration**:
- Approved PDF becomes available asset
- Added to document's asset inventory
- Referenced in technical debt for other consumers

## Pages Template Research Summary

### Key Findings:
- Templates use `.template` extension
- Must be created within Pages application
- Cannot be programmatically generated
- Shared via "My Templates" or template chooser
- Image placeholders created via Format → Advanced → Define as Media Placeholder

### Template Creation Method:
1. **File → New** (blank template)
2. **Format document** with specifications
3. **File → Save as Template**
4. **Name and save** to template chooser

### Template Installation:
- Double-click `.template` file → "Add to Template Chooser"
- Appears in "My Templates" section
- Available for document creation

## File Naming Conventions

### Export Directory: `/exports/[document-name]/`
- `terminal-window-manual` (use hyphens)
- `debugger-manual`
- `ai-privacy-guide`

### Generated Files:
- `[document-name].docx` (source content)
- `pages-template-setup.md` (template instructions)
- `README.md` (import guide)
- `[document-name].pdf` (final output)

## Quality Standards

### Template Requirements:
- Professional typography hierarchy
- Consistent brand colors (P2 Blue theme)
- Proper headers/footers with pagination
- Image placeholder functionality
- Reusable across multiple documents

### PDF Output Standards:
- US Letter format, professional layout
- Consistent styling throughout
- High-quality image rendering
- Proper table of contents (if applicable)
- Print-ready quality

## Reusability Notes

### Template Reuse:
- Same template works for all P2 user manuals
- One-time setup per Stephen's Pages installation
- Consistent branding across all documents

### Process Reuse:
- Same methodology for any markdown → PDF conversion
- Scalable to multiple simultaneous documents
- Standardized feedback/iteration cycle

## Benefits

1. **Consistency**: All P2 documents use same professional template
2. **Efficiency**: Reusable template and process
3. **Quality**: Professional PDF output suitable for distribution
4. **Iteration**: Clean feedback cycle for document improvement
5. **Asset Management**: PDFs become available assets for consumers

## Success Metrics

- PDF quality meets professional distribution standards
- Template successfully reusable across documents  
- Feedback cycle enables rapid iteration
- Final PDFs integrate into knowledge base asset system

---

**Usage**: Reference this methodology whenever converting P2 documentation to PDF format. Update process based on learnings from each document generation cycle.