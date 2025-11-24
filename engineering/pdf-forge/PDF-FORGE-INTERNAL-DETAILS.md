# PDF Forge Internal Details - Reference Documentation

**Audience**: Developers maintaining the PDF Forge system
**Purpose**: Technical details about how PDF Forge works internally
**For users**: See `PRODUCTION-PROCESS-RULES.md` and `production-pdf-generation.md` instead

---

## System Architecture

### Main Production Script: `process-inbox.sh`

The entry point for PDF generation that orchestrates the entire workflow:

```bash
#!/bin/bash
# Location: /workspace/scripts/process-inbox.sh
# Purpose: Process markdown files from inbox/ to create PDFs in outbox/
```

**Workflow Steps:**

1. **Check for request.json** (line 48)
   - Looks in `inbox/` directory
   - If missing, creates default request automatically

2. **Validate Request** (line 63)
   - Calls `validate-request.js`
   - Validates JSON structure and required fields
   - Exits with error if validation fails

3. **Generate PDFs** (line 71)
   - Calls `generate-pdf.js`
   - Processes each document in request
   - Creates PDFs in output/ directory

4. **Move to Outbox** (line 77)
   - Moves generated PDFs to outbox/
   - Copies generation.log for audit

5. **Optional Archival** (line 93)
   - Prompts user: "Archive processed files? (y/n)"
   - Creates `processed/YYMMDD_HHMM/` subdirectory
   - Moves source files to archive to prevent reprocessing

### Script Components

#### `generate-pdf.js` - Core PDF Generation

**Key Features:**
- Reads `inbox/request.json` for configuration
- Processes `documents` array from request
- Uses Pandoc 2.17.1.1 with XeLaTeX engine
- Supports per-document templates, filters, and metadata
- Generates both `.tex` (debug) and `.pdf` (output) files

**Template Resolution:**
```javascript
const templatePath = `templates/${template}.latex`;
// Falls back to 'admin-manual' if template not specified
```

**Resource Path Configuration:**
```javascript
const resourcePath = `--resource-path="${inputDir}"`;
// Allows pandoc to find assets/ relative to markdown file
```

**TEXINPUTS Environment:**
```javascript
TEXINPUTS: `./templates//:${process.env.TEXINPUTS || ''}`
// Allows LaTeX to find .sty files in templates/ directory
```

#### `validate-request.js` - Request Validation

Validates request.json structure before processing:
- Checks for `documents` array
- Validates required document fields (input, output)
- Checks template and filter file existence
- Provides clear error messages for common mistakes

#### `create-default-request.js` - Automatic Request Creation

Called by `process-inbox.sh` when request.json is missing:
- Scans inbox/ for `.md` files
- Creates basic request.json structure
- Uses 'admin-manual' template as default
- Generates output filenames from input filenames

**When This Happens:**
- User drops only markdown files without request.json
- Fallback behavior to prevent complete failure
- **Users should provide request.json** for proper configuration

### Testing System: `watch-shared-workspace.js`

Separate daemon for template testing (NOT production):

**Location:** `/workspace/shared/` (bind mount)
**Purpose:** Rapid iteration testing for templates and filters
**Script:** Enhanced monitoring daemon with auto-detection

**Key Differences from Production:**
- Uses `/workspace/shared/` instead of `/workspace/inbox/`
- Tests go to `/tmp/pandoc-work-*/` temporary directories
- Results written to `/workspace/shared/test-results/`
- Multiple tests per request supported
- Generates `.tex` files for debugging
- **DOES NOT install templates permanently**

**Working Directory Behavior:**
```javascript
// Creates temporary directory
const workDir = path.join('/tmp', `pandoc-work-${testName}-${Date.now()}`);

// Copies templates FROM /workspace/shared/templates/
// Copies TO /tmp/pandoc-work-*/
// After test: temporary directory cleaned up
```

## File Persistence Model

### Production Template Storage

**Location:** `/workspace/templates/`
**Behavior:** Persistent across sessions

When user sends files to inbox/:
- `.latex` files copied to `/workspace/templates/`
- `.sty` files copied to `/workspace/templates/`
- `.lua` files copied to `/workspace/filters/` (if that directory exists)
- Files remain until manually replaced or deleted

**Last File Wins:**
- Sending same filename replaces previous version
- No version control - most recent copy is used
- Timestamp or checksums not tracked

### Why Persistence Matters

**Initial Setup (Day 1):**
```
inbox/
├── request.json
├── document.md
├── my-template.latex              # Root level - copied to /workspace/templates/
├── my-styles.sty                  # Root level - copied to /workspace/templates/
├── my-filter.lua                  # Root level - copied to /workspace/filters/
└── assets/                        # Subdirectory - images stay here
    └── image.png
```
All files copied from inbox root to appropriate permanent locations.

**Subsequent Runs (Day 2+):**
```
inbox/
├── updated-document.md
└── request.json
```
Only new content needed - previously installed files reused.

**Fixing a Bug (Day 5):**
```
inbox/
├── request.json
└── fixed-filter.lua
```
Only changed filter sent - replaces previous version.

## Archival System

### Purpose
Prevents reprocessing of already-generated documents by moving source files out of inbox/.

### Behavior
After successful PDF generation, `process-inbox.sh` prompts:
```
Archive processed files? (y/n)
```

**If Yes:**
- Creates directory: `inbox/processed/YYMMDD_HHMM/`
- Moves all `.md` files to archive
- Moves `request.json` to archive
- Leaves templates/filters/styles in place (remain installed)

**If No:**
- Files remain in inbox/
- Next run of process-inbox.sh will reprocess them
- Useful for iterative testing

### Archive Format
```
inbox/processed/
├── 250903_1430/        # Sept 3, 2025 at 14:30
│   ├── document.md
│   └── request.json
└── 250903_1445/        # Sept 3, 2025 at 14:45
    ├── updated-doc.md
    └── request.json
```

**Why YYMMDD_HHMM format:**
- Prevents same-day overwrites (multiple runs per day)
- Chronological sorting
- Easy to identify when documents were processed

## Pandoc Version Constraints

### Critical Version Difference

**Local Machine (Host):**
- Pandoc 1.19.2.1 (pre-2016 version)
- Location: `/Users/stephen/anaconda3/bin/pandoc`
- **NO Lua filter support**
- **DO NOT use for testing**
- Ancient version, incompatible with modern workflow

**PDF Forge (Container):**
- Pandoc 2.17.1.1 (modern version)
- Full Lua filter support
- Proper LaTeX integration
- **This is the ONLY Pandoc that matters**

### Implications

1. **Cannot test locally** - Lua filters fail with "unrecognized option"
2. **All testing must go through PDF Forge** (production or testing system)
3. **Local pandoc output misleading** - different version = different behavior
4. **Filter errors only show on Forge** - where they actually execute

### Why Local Pandoc Exists

Anaconda installation included old pandoc version. Cannot be removed easily without breaking Anaconda environment. **Solution: Ignore its existence.**

## Request.json Structure Deep Dive

### Document-Level vs Request-Level

**CRITICAL:** `generate-pdf.js` reads from document objects, NOT root level.

**❌ WRONG (ignored by script):**
```json
{
  "template": "my-template",           // IGNORED!
  "lua_filters": ["filter1"],          // IGNORED!
  "metadata": {"title": "Doc"},        // IGNORED!
  "documents": [{
    "input": "doc.md",
    "output": "doc.pdf"
  }]
}
```

**✅ CORRECT (script reads these):**
```json
{
  "documents": [{
    "input": "doc.md",
    "output": "doc.pdf",
    "template": "my-template",         // READ HERE
    "lua_filters": ["filter1"],        // READ HERE
    "metadata": {"title": "Doc"}       // READ HERE
  }]
}
```

**Code Evidence:**
```javascript
// From generate-pdf.js line 60:
template = doc.template || 'admin-manual'
// Falls back to 'admin-manual' if doc.template missing
```

### Metadata vs Variables

Both supported, metadata preferred:
```javascript
// From generate-pdf.js line 95:
const allVariables = { ...variables, ...metadata };
// metadata takes precedence over variables
```

**Recommendation:** Use `metadata` for new documents, maintain `variables` for backward compatibility.

## Debug and Logging

### Generation Logs

**Location:** `outbox/generation.log`
**Contains:**
- Pandoc commands executed
- Template paths used
- Filter applications
- Error messages if any
- Timestamp of generation

### TEX File Generation

For debugging template issues, generate-pdf.js creates `.tex` files:
```javascript
const texOutputFile = outputFile.replace(/\.pdf$/, '.tex');
// Generates alongside PDF for inspection
```

**Use Case:**
- See actual LaTeX commands Pandoc generated
- Debug template macro expansion
- Verify filter transformations
- Troubleshoot LaTeX compilation errors

### Activity Logs (Testing System)

**Location:** `/workspace/shared/status/activity.log`
**Purpose:** Real-time monitoring of watch-shared-workspace.js

Shows:
- Request detection
- Template copying
- Test execution
- PDF generation status
- Error details

## Error Handling

### Common Error Patterns

**"Template not found: X"**
- Cause: Template file not in `/workspace/templates/`
- Solution: Copy template to templates directory

**"Filter not found: Y"**
- Cause: Lua filter file not in `/workspace/filters/` or `/workspace/shared/filters/`
- Solution: Copy filter to appropriate directory

**"Template: admin-manual" (unexpected)**
- Cause: `template` field at wrong level in request.json
- Solution: Move template specification inside document object

**"Missing number, treated as zero"**
- Cause: LaTeX `\real{}` command not defined in template
- Common in table calculations
- Solution: Add `\newcommand*{\real}[1]{#1}` to template

### Timeout Settings

From watch-shared-workspace.js:
```javascript
execSync(texCmd, {
  stdio: 'pipe',
  timeout: 300000  // 5 minutes for .tex generation
});

execSync(pandocCmd, {
  stdio: 'pipe',
  timeout: 600000  // 10 minutes for PDF generation
});
```

**Why Long Timeouts:**
- Large documents can take several minutes
- LaTeX compilation is CPU-intensive
- Multiple passes may be required
- Better to wait than fail prematurely

## Directory Structure Reference

### Production System
```
/workspace/
├── inbox/                    # User drops files here
│   ├── request.json         # Required
│   ├── *.md                 # Markdown documents
│   ├── assets/              # Images (optional)
│   └── processed/           # Archives (after generation)
├── outbox/                  # Generated PDFs appear here
│   ├── *.pdf
│   └── generation.log
├── templates/               # Persistent template storage
│   ├── *.latex
│   └── *.sty
├── filters/                 # Persistent filter storage (if exists)
│   └── *.lua
└── scripts/                 # System scripts
    ├── process-inbox.sh
    ├── generate-pdf.js
    ├── validate-request.js
    └── create-default-request.js
```

### Testing System
```
/workspace/shared/           # Bind mount for testing
├── test-requests/          # Test requests drop here
│   └── processed/          # Completed tests
├── test-results/           # JSON results + .tex files
├── templates/              # Test templates (temporary)
├── filters/                # Test filters (temporary)
├── test-documents/         # Test markdown files
├── output-pdfs/           # Test PDF outputs
└── status/                # Logs and status files
```

### Temporary Execution
```
/tmp/pandoc-work-[test]-[timestamp]/
├── template.latex          # Copied from source
├── *.sty                  # All style files copied
└── [working files]        # Pandoc execution context
```

## Performance Characteristics

**Typical Generation Times:**
- Simple document (< 10 pages): 5-15 seconds
- Medium document (50-100 pages): 30-60 seconds
- Large document (300+ pages): 2-5 minutes
- Complex templates with many filters: Add 10-20%

**What Affects Speed:**
- Document length
- Number of images
- LaTeX compilation passes required
- Filter complexity
- System load

## Maintenance Notes

### When to Update Scripts

Scripts copied to this repository are **snapshots** from PDF Forge:
- Update when Forge scripts change
- Document version/date in commit message
- Test compatibility with existing documents

### Version Tracking

Current script versions documented:
- `process-inbox.sh` - Copied: Aug 16, 2024
- `generate-pdf.js` - Copied: Sept 4, 2024 (enhanced metadata support)
- `watch-shared-workspace.js` - Copied: Sept 4, 2024 (v2.3 with Lua filters)

### Backward Compatibility

**Must maintain:**
- request.json `documents` array format
- Template naming conventions
- Filter resolution paths
- Metadata vs variables support

**Can change:**
- Internal implementation details
- Logging format
- Performance optimizations
- Error messages

---

## Summary

This document captures **how PDF Forge works internally**. Users preparing documents should reference:
- `PRODUCTION-PROCESS-RULES.md` - What files to prepare
- `production-pdf-generation.md` - Step-by-step workflow
- `PRODUCTION-REQUEST-FORMAT.md` - request.json format

These internal details are primarily useful for:
- Debugging unexpected behavior
- Understanding why certain patterns are recommended
- Maintaining the PDF Forge system itself
- Troubleshooting edge cases
