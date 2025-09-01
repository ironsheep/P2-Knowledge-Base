# PDF Forge System Overview

**Created**: 2025-08-23  
**Purpose**: Complete documentation of PDF Forge system architecture and operation  
**Status**: Production system with full version control

## 🎯 Critical Understanding

**PDF Forge is under FULL VERSION CONTROL** - All scripts, templates, and configuration are versioned. Any changes can be reverted if needed.

## 📁 System Architecture

### Repository Structure (at PDF Forge root)
```
/                           # PDF Forge repository root
├── templates/             # LaTeX templates (.latex files)
├── filters/               # Pandoc Lua filters (.lua files)
├── scripts/               # Processing scripts (Node.js)
├── inbox/                 # Input files placed here
├── outbox/                # Generated PDFs output here
├── output/                # Working directory
└── config/                # Configuration files
```

### Core Scripts
| Script | Purpose | Status |
|--------|---------|--------|
| `generate-pdf.js` | Main PDF generation | **ENHANCED 2025-08-23** - Now supports pandoc_args |
| `process-inbox.sh` | Batch processing wrapper | Original |
| `validate-request.js` | Request validation | Original |
| `build-templates.js` | Template compilation | Original |
| `create-default-request.js` | Request generator | Original |
| `optimize-pdfs.js` | PDF optimization | Original |
| `setup.js` | Initial setup | Original |

## 🔧 Critical Fix Applied (2025-08-23)

### Problem Discovered
Original `generate-pdf.js` was **ignoring `pandoc_args`** from request.json, preventing:
- Lua filters from running
- Custom Pandoc options
- Output format specifications

### Solution Implemented
Enhanced `generate-pdf.js` to:
1. Accept `pandoc_args` array from request.json
2. Accept `metadata` object (preferred over `variables`)
3. Pass all arguments to Pandoc command
4. Display actual command for debugging

### Impact
- Lua filters now work
- Full control over Pandoc behavior
- Colored environment boxes enabled
- Complete feature parity with local Pandoc

## 📋 Request.json Format

### Full Feature Format (after enhancement)
```json
{
  "documents": [
    {
      "input": "document.md",
      "output": "document.pdf",
      "template": "p2kb-template-name",
      "pandoc_args": [           // NEW: Fully supported
        "--to=latex",
        "--lua-filter=filters/filter.lua"
      ],
      "metadata": {              // PREFERRED over variables
        "title": "Document Title",
        "author": "Author Name",
        "toc": true,
        "toc-depth": 2,
        // ... any Pandoc metadata
      },
      "variables": {             // LEGACY: Still supported
        "key": "value"
      }
    }
  ]
}
```

## 🔄 Version Control Integration

### Key Points
- **Full Git tracking** - Every change is versioned
- **Rollback capable** - Can revert to any previous version
- **Change history** - Full audit trail of modifications
- **Branch support** - Can test changes in branches

### Recovery Process
```bash
# If something breaks, on PDF Forge:
git status                    # Check current state
git diff                      # See what changed
git checkout -- generate-pdf.js  # Revert specific file
git reset --hard HEAD         # Full revert to last commit
```

## 🚀 Deployment Process - VERSION CONTROL AWARE

### 🔴 CRITICAL: Script Naming Rule
**NEVER rename scripts when upgrading features!**

⚠️ **Version Control Principle**: PDF Forge is fully version controlled. We maintain ONE script that evolves over time, not multiple scripts with different names for different features.

**✅ CORRECT Process**:
1. Take existing script name (e.g., `generate-pdf.js`)
2. Add new features to the script
3. Save with SAME NAME: `generate-pdf.js`
4. User drops over existing file on PDF Forge
5. OS prompts "Replace file?" → User says YES
6. Git tracks the evolution of that single script

**❌ WRONG Process**:
- Creating `generate-pdf-assets.js` for asset support
- Creating `generate-pdf-enhanced.js` for enhancements
- Creating `generate-pdf-v2.js` for new version

**Why This Matters**:
- Maintains clean version history
- Prevents script proliferation
- Git shows feature evolution
- No confusion about which script to use

### 📦 Universal Deployment Method
**Claude places ALL files in the outbound directory. User moves them to PDF Forge based on extension:**

| File Extension | PDF Forge Destination | Purpose |
|---------------|----------------------|----------|
| `.js` | `/scripts/` | Processing scripts |
| `.lua` | `/filters/` | Pandoc filters |
| `.latex` | `/templates/` | Document templates |
| `.md` | `/inbox/` | Source documents |
| `.json` | `/inbox/` | Request configuration |

### Workflow Steps
1. **Claude prepares files** in `/engineering/pdf-forge/production/[document]/`
2. **User identifies by extension** and moves to correct PDF Forge location
3. **User runs test** on PDF Forge
4. **User commits** if successful (Claude will suggest commit message)

### Example
```
# Claude places in outbound:
generate-pdf.js          → User moves to PDF Forge /scripts/
div-to-environment.lua   → User moves to PDF Forge /filters/
p2kb-template.latex      → User moves to PDF Forge /templates/
request.json            → User moves to PDF Forge /inbox/
document.md             → User moves to PDF Forge /inbox/
```

**This eliminates confusion about paths and makes deployment foolproof!**

## 📊 Processing Flow

```
1. User places files in /inbox/
   - document.md
   - request.json
   
2. Script reads request.json
   - Extracts document array
   - Reads pandoc_args (NEW!)
   - Reads metadata/variables
   
3. For each document:
   - Build Pandoc command with ALL arguments
   - Generate .tex for debugging
   - Generate .pdf
   
4. Output appears in /outbox/
   - PDF files
   - generation.log
```

## 🔍 Debugging Features

### Enhanced Logging
The enhanced script now shows:
- Input/output files
- Template being used
- **Pandoc arguments being passed**
- **Actual command being executed**
- Success/failure status

### TEX File Generation
- Always generates .tex alongside .pdf
- Allows inspection of LaTeX conversion
- Shows if Lua filters ran (look for comments)

## 📝 Local Development Mirror

**Local scripts location**: `/P2-Knowledge-Base/pdf-forge-scripts/`
- Complete copy of PDF Forge scripts
- Used for development and testing
- Changes deployed to PDF Forge after testing

## 🎯 Next Steps

With `pandoc_args` support enabled:
1. ✅ Lua filters will run
2. ✅ Colored environment boxes will work
3. ✅ Custom output formats supported
4. ✅ Full Pandoc feature access

## 🧪 Interactive Testing with PDF Forge Workspace

**CRITICAL**: The PDF Forge has a shared workspace for interactive testing without using the inbox/outbox workflow.

### Workspace Structure
```
pdf-forge-workspace/           # Local directory (bind-mounted to PDF Forge)
├── test-requests/            # Place test JSON requests here
│   └── processed/           # Completed requests get archived here
├── test-results/            # PDF Forge writes results here
│   ├── *.json              # Test result JSON files
│   └── *.tex               # Generated LaTeX for debugging
├── test-documents/          # Markdown test documents
├── filters/                 # Lua filters for testing
├── templates/               # LaTeX templates
├── output-pdfs/            # Generated PDFs
└── status/                 # Status and log files
```

### Test Request Format (for workspace testing)
```json
{
  "request_id": "unique-test-id",
  "template": "template-name.latex",
  "timestamp": "2025-08-31T06:00:00Z",
  "tests": [
    {
      "name": "test-name",
      "document": "test-document.md",
      "lua_filters": [           // CRITICAL: Use lua_filters array, not pandoc_args!
        "filter-name-without-lua",  // Don't include .lua extension
        "another-filter"
      ],
      "pandoc_args": [           // Optional: Additional pandoc arguments
        "--listings",
        "--number-sections"
      ]
    }
  ],
  "options": {
    "auto_fix_attempt": false,
    "cleanup": true
  }
}
```

### Key Differences from Inbox Workflow

| Aspect | Inbox Workflow | Workspace Testing |
|--------|---------------|-------------------|
| Request format | `documents` array | `tests` array |
| Filter specification | `pandoc_args` with `--lua-filter` | `lua_filters` array |
| Filter path | Must specify full path | Just filter name (no .lua) |
| Processing | Manual trigger | Auto-detected by watcher |
| Results location | `/outbox/` | `test-results/` |
| Response time | Varies | 2-4 seconds |

### Testing Workflow

1. **Place files in workspace**:
   ```bash
   # Copy your Lua filter
   cp my-filter.lua pdf-forge-workspace/filters/
   
   # Copy test document
   cp test.md pdf-forge-workspace/test-documents/
   
   # Create test request
   cat > pdf-forge-workspace/test-requests/my-test.json
   ```

2. **PDF Forge automatically processes** (watch-shared-workspace.js is running)
   - Detects new request in 1-2 seconds
   - Processes and generates PDF
   - Writes result to `test-results/`

3. **Check results**:
   ```bash
   # Check JSON result
   cat pdf-forge-workspace/test-results/my-test-result.json
   
   # Check generated .tex for debugging
   cat pdf-forge-workspace/test-results/test-name-*.tex
   
   # View PDF
   open pdf-forge-workspace/output-pdfs/test-name-*.pdf
   ```

### Common Issues and Solutions

**Issue**: "cannot open filter.lua: No such file or directory"
- **Cause**: Filter not found in workspace/filters/
- **Solution**: Copy filter to `pdf-forge-workspace/filters/`

**Issue**: "Missing required field: template"
- **Cause**: Using wrong request format
- **Solution**: Use `template` field (not nested in documents)

**Issue**: Filter not running despite being specified
- **Cause**: Using `pandoc_args` instead of `lua_filters`
- **Solution**: Use `lua_filters` array with filter names (no .lua extension)

### Debugging Tips

1. **Check daemon log** for processing details:
   ```bash
   tail -f pdf-forge-workspace/status/daemon.log
   ```

2. **Verify filter was copied to working directory**:
   - PDF Forge creates temp directories like `/tmp/pandoc-work-*`
   - Filters must be accessible from there

3. **Examine generated .tex file**:
   - Look for Lua filter comments (e.g., `% LUA FILTER: ...`)
   - Check if expected LaTeX environments were generated

4. **Review test result JSON**:
   - Contains error messages and processing details
   - Shows exact pandoc command attempted

## 📚 Related Documentation

- `/engineering/pdf-forge/production/pasm2-manual-v1/PDF-FORGE-SETUP-REQUIRED.md` - Installation requirements
- `/documentation/pipelines/pdf-generation-format-guide.md` - Format specifications
- `/pdf-forge-scripts/` - Local script development