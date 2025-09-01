# P2KB Template Catalog

**Master repository of P2 Knowledge Base LaTeX templates**

This directory maintains the definitive copies of all P2KB templates used for PDF generation.

---

## Template Management Strategy

### Directory Structure
```
pipelines/templates/p2kb-catalog/
├── README.md                     ← This file
├── p2kb-pasm2-manual.latex       ← PASM2 instruction documentation
├── p2kb-user-guide.latex         ← User guide formatting (future)
├── p2kb-debug-manual.latex       ← Debug/terminal documentation (future)
└── template-changelog.md         ← Version history for all templates
```

### Version Control Workflow
1. **Master copies** live in this catalog directory
2. **Working copies** are deployed to PDF generation requests
3. **Changes** are made to master copies first
4. **Updated templates** are included with each PDF generation request
5. **Doc-forge copies** are updated from our working copies

### Template Ownership
- **P2KB prefix**: All templates use `p2kb-[purpose].latex` naming
- **Unique ownership**: P2KB templates are exclusive to P2 Knowledge Base
- **Separation**: Different Claude instances maintain their own prefixes
- **No conflicts**: Clear ownership prevents template mixing

---

## Active Templates

### `p2kb-pasm2-manual.latex`
**Purpose**: PASM2 assembly instruction documentation  
**Status**: Active (v1.0)  
**Features**:
- Parallax official color scheme (Blues: #0066CC, #003366)
- PASM2 syntax highlighting for code blocks
- Instruction reference table formatting
- Professional headers/footers with version info
- Optimized for technical instruction documentation

**Usage Pattern**:
```json
{
  "template": "p2kb-pasm2-manual",
  "variables": {
    "title": "Document Title",
    "version": "1.0",
    "date": "2025-08-18",
    "author": "P2 Knowledge Base System",
    "company": "Propeller 2 Documentation Project"
  }
}
```

---

## Development Templates (Planned)

### `p2kb-user-guide.latex`
**Purpose**: End-user documentation and guides  
**Status**: Planned  
**Target**: Friendly, accessible formatting for user-facing content

### `p2kb-debug-manual.latex`
**Purpose**: Debug interface and terminal documentation  
**Status**: Planned  
**Target**: Technical reference with console/terminal styling

### `p2kb-reference-card.latex`
**Purpose**: Quick reference cards and cheat sheets  
**Status**: Planned  
**Target**: Compact, high-density information formatting

---

## Deployment Process

### When Creating PDF Requests
1. **Copy master template** from this catalog to PDF request directory
2. **Update request.json** to reference the template
3. **Include template** in outbound directory alongside content
4. **Stephen processes** the complete package through doc-forge
5. **Doc-forge updates** its template library from our working copy

### When Modifying Templates
1. **Edit master copy** in this catalog first
2. **Test changes** with sample content
3. **Update template-changelog.md** with changes
4. **Deploy updated template** with next PDF generation request
5. **Verify** doc-forge receives the updated version

---

## Benefits

### For P2 Knowledge Base
- **Centralized management**: All templates in one location
- **Version control**: Change history and template evolution
- **Consistency**: Standardized formatting across all documents
- **Independence**: No dependency on external template sources

### For Multi-Claude Environment
- **Clear ownership**: P2KB prefix prevents conflicts
- **Isolation**: Each Claude instance manages its own templates
- **Flexibility**: Templates can evolve independently
- **Scalability**: New document types get dedicated templates

### For PDF Generation
- **Reliability**: Master copies prevent template loss
- **Freshness**: Always deploy latest template versions
- **Quality**: Consistent professional output
- **Maintenance**: Easy template updates and improvements

---

## Usage Instructions

**For Claude**: Always copy templates from this catalog when creating PDF requests  
**For Stephen**: P2KB-prefixed templates in requests should update doc-forge copies  
**For Development**: Modify master copies here, then deploy to requests

This catalog ensures P2 Knowledge Base maintains control over its document formatting while preventing conflicts with other Claude instances managing their own template libraries.