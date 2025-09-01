# PDF Forge Deployment Workflow - CRITICAL UNDERSTANDING

**Last Updated**: 2025-08-31  
**Purpose**: Clarify the persistent file system behavior of PDF Forge

## 🔴 CRITICAL CONCEPT: PDF Forge is a PERSISTENT INSTALLATION

The PDF Forge is NOT a stateless system. It maintains a persistent file store where:
- **Last file wins**: The most recent version of each file type (.lua, .sty, .latex) becomes the "installed" version
- **Files persist across sessions**: Once deployed, files remain available for all future PDF generations
- **Updates replace**: Sending a file with the same name replaces the previous version

## Workflow Phases

### Phase 1: Initial Installation (First Deployment)
When setting up a new document type for the first time:

**Send ALL required files:**
```
/exports/pdf-generation/outbound/[document-name]/
├── request.json                    # Always needed
├── document.md                     # The content
├── template.latex                  # Main template
├── required-style1.sty            # All style files
├── required-style2.sty            
├── filter1.lua                    # All Lua filters
├── filter2.lua
└── assets/                        # Images if needed
```

**These files become "installed" on PDF Forge.**

### Phase 2: Production Use (Subsequent Runs)
For normal PDF generation after initial setup:

**Send ONLY:**
```
/exports/pdf-generation/outbound/[document-name]/
├── request.json                    # Always needed
└── document.md                     # Updated content
```

**PDF Forge uses:**
- The NEW request.json and document.md you just sent
- The PREVIOUSLY INSTALLED .latex, .sty, and .lua files

### Phase 3: Updates/Fixes (Replacing Installed Files)
When you need to fix or update the installed files:

**Send ONLY the changed files:**
```
/exports/pdf-generation/outbound/[document-name]/
├── request.json                    # Always needed
└── fixed-filter.lua               # ONLY the files that changed
```

**Do NOT send:**
- Files that haven't changed
- Files already "installed" on PDF Forge
- Redundant copies of working files

## Common Mistakes to Avoid

### ❌ WRONG: Sending everything every time
```
# DON'T DO THIS after initial setup:
cp all-templates/*.sty outbound/     # Unnecessary
cp all-filters/*.lua outbound/       # Wasteful
cp template.latex outbound/          # Redundant
```

### ✅ RIGHT: Send only what's new or changed
```
# DO THIS for updates:
cp fixed-filter.lua outbound/        # Only the fix
cp request.json outbound/            # Always needed
```

## Understanding File Persistence

### What stays on PDF Forge:
- **.latex templates** - Until replaced with same filename
- **.sty style files** - Until replaced with same filename  
- **.lua filters** - Until replaced with same filename

### What must be sent each time:
- **request.json** - Specifies what to generate
- **markdown files** - The content to process
- **assets** - If referenced by markdown and not already there

## Request.json Structure - CRITICAL

### ⚠️ WRONG Structure (causes admin-manual fallback):
```json
{
  "template": "my-template.latex",  // WRONG: Top level
  "lua_filters": ["filter1", "filter2"],  // WRONG: Top level
  "metadata": {...},  // WRONG: Top level
  "documents": [{
    "input": "doc.md",
    "output": "doc.pdf"
  }]
}
```

### ✅ CORRECT Structure (per generate-pdf.js):
```json
{
  "documents": [{
    "input": "doc.md",
    "output": "doc.pdf",
    "template": "my-template",  // RIGHT: Inside document
    "lua_filters": ["filter1", "filter2"],  // RIGHT: Inside document
    "metadata": {  // RIGHT: Inside document
      "title": "Document Title",
      "subtitle": "Document Subtitle",
      "version": "1.0"
    }
  }]
}
```

**Key insights from generate-pdf.js**: 
- Template is read from `doc.template` (falls back to 'admin-manual' if missing)
- lua_filters is read from `doc.lua_filters` 
- metadata is read from `doc.metadata`
- ALL document-specific settings go INSIDE the document object
- When you see "Template: admin-manual" in the log, it means template is missing from the document object!

## Debugging File Issues

### Symptom: "Filter not found"
**Cause**: Filter was never installed or has different name
**Fix**: Send the .lua file to install it

### Symptom: "Template: admin-manual" (wrong template)
**Cause**: lua_filters at wrong level in request.json
**Fix**: Move lua_filters inside document object

### Symptom: Old version of template being used
**Cause**: Updated file never sent to PDF Forge
**Fix**: Send the updated file to replace installed version

### Symptom: Styles not applying
**Cause**: .sty file not installed or wrong name
**Fix**: Send the .sty file with exact name template expects

## Best Practices

1. **Track installed versions**: Keep notes on what's been deployed
2. **Name files consistently**: Same name = replacement, different name = new file
3. **Minimize deployments**: Only send what's actually changed
4. **Test incrementally**: When debugging, change one file at a time
5. **Clear naming**: Use descriptive names to avoid confusion

## Example Workflow

### Day 1: Initial Setup
```bash
# First time - send everything
cp template.latex outbound/
cp *.sty outbound/
cp *.lua outbound/
cp document.md outbound/
cp request.json outbound/
# → PDF Forge now has all files installed
```

### Day 2: Update Content
```bash
# Just new content
cp updated-document.md outbound/
cp request.json outbound/
# → PDF Forge uses new content with existing templates/filters
```

### Day 3: Fix a Filter
```bash
# Just the fix
cp fixed-filter.lua outbound/
cp request.json outbound/
# → PDF Forge replaces old filter with fixed version
```

## Summary

**Think of PDF Forge like installing software:**
- First time: Install all components
- Daily use: Just provide the data (markdown)
- Updates: Only send patches/fixes

**NOT like a stateless API where you send everything every time!**

This persistent model is why:
- We can fix one filter without resending all files
- Templates stay installed across multiple document generations
- The system gets more efficient over time as files accumulate

## Key Takeaway

> 📌 **The outbound directory should contain the MINIMUM needed for the current operation, not everything needed for PDF generation.**

The PDF Forge remembers what you've sent before!