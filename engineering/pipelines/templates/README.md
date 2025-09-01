# P2KB Template Catalog

**LaTeX style sheets for PDF generation with doc-forge**

---

## Available Templates

### `p2kb-pasm2-manual.latex`
**Purpose**: PASM2 Assembly Manual formatting  
**Style**: Official Parallax documentation format  
**Features**:
- Gray-background instruction encoding tables
- Blue hyperlinks matching official style  
- Large bold instruction names
- Code blocks with gray backgrounds
- Professional page layout with headers/footers
- Optimized for instruction reference documentation

**Usage**: 
```json
{
  "template": "p2kb-pasm2-manual",
  "variables": {
    "title": "PASM2 Manual Title",
    "version": "1.0",
    "date": "2025-08-17",
    "author": "Author Name",
    "company": "Company Name"
  }
}
```

### `p2kb-desilva-manual.latex` *(planned)*
**Purpose**: DeSilva documentation style formatting  
**Style**: Based on DeSilva P2 content patterns  
**Status**: In development

---

## Template Naming Convention

**Format**: `p2kb-[purpose].latex`

**Prefix**: `p2kb-` (P2 Knowledge Base)
- Prevents conflicts with existing doc-forge templates
- Clear project ownership
- Easy identification and grouping

**Purpose Examples**:
- `pasm2-manual` - Assembly instruction documentation
- `desilva-manual` - DeSilva style documentation  
- `user-guide` - User guide formatting
- `reference-card` - Quick reference cards
- `debug-manual` - Debug/terminal documentation

---

## Usage Workflow

1. **Copy template** to doc-forge templates directory
2. **Reference in request.json** using template name (without .latex extension)
3. **Provide variables** for title, version, author, etc.
4. **Generate PDF** through standard doc-forge process

---

## Template Development

All templates include required Pandoc compatibility fixes and follow LaTeX best practices for PDF generation. Each template is optimized for specific document types and visual styles.

**Source**: Generated from P2 Knowledge Base project  
**Maintenance**: Update internal copies when templates are modified