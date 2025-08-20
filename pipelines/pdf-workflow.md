# PDF Generation Workflow

**Standard process for generating professional PDFs from project documentation**

## 📁 Directory Structure

```
/exports/pdf-generation/
  /outbound/                    # Documents ready for PDF generation
    /[document-name-version]/   # Each document gets isolated folder
      - document.md             # Source markdown file
      - request.json            # PDF generation configuration
      - /images/               # Document-specific assets (if needed)
  /inbound/                     # Finished PDFs returned here
    /[document-name-version]/
      - Generated_PDF_Name.pdf  # Finished professional PDF
```

## 🔄 Workflow Process

### 1. Document Preparation (Claude)
- Study `pipelines/INTEGRATION_GUIDE.md` for doc-forge requirements
- Prepare source document with proper formatting/metadata
- Create `request.json` with PDF generation configuration
- Copy any required images to document's `/images/` folder
- Place complete package in `/exports/pdf-generation/outbound/[document-name-version]/`

### 2. PDF Generation (Human)
- Collect all folders from `/outbound/` for batch processing
- Process through doc-forge PDF generation system
- Place finished PDFs in matching `/inbound/[document-name-version]/` folders

### 3. Result Processing (Claude)
- Review generated PDFs in `/inbound/` folders
- Move successful PDFs to final locations (e.g., `/releases/pdfs/`)
- Clean up `/outbound/` request folders after successful generation
- Update project documentation with new PDF availability

## 🎯 Benefits

- **Isolation**: No asset mixing between documents
- **Clear Handoffs**: Distinct outbound/inbound separation
- **Easy Matching**: Folder names link requests to results  
- **Batch Processing**: Multiple documents can be processed simultaneously
- **Clean Workflow**: Clear indicators of when to clean up vs keep

## 📋 Document Naming Convention

**Folder Names**: `[document-name-version]`
- `terminal-window-manual-v1`
- `debug-manual-v1` 
- `release-notes-v1.0`

**PDF Output Names**: As specified in `request.json` output field
- `Professional_Terminal_Window_Manual_v1.0.pdf`
- `Professional_Debug_Manual_v1.0.pdf`
- `P2_Knowledge_Base_v1.0_Release_Notes.pdf`

## 🔗 Related Documentation

- `pipelines/INTEGRATION_GUIDE.md` - Doc-forge integration requirements
- `pipelines/pdf-generation-methodology.md` - General PDF methodology