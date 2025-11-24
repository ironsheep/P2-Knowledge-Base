# Automated PDF Testing System Usage Guide

⚠️ **IMPORTANT**: Test patterns before trusting! This document contains patterns that have worked, but the system evolves. Always verify that a specific pattern (like `debug_tex: true`) actually works in the current system before relying on it.

**PURPOSE**:
- **Rapid iteration testing** for PDF template development and visual refinement
- **Temporary testing only** - Templates are NOT automatically deployed to production

## System Architecture

**CRITICAL CONNECTION:**
- **My Local Access**: /Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/pdf-forge/interactive-testing
- **PDF Forge Shared Workspace**: `/workspace/shared/` (on PDF Forge system)
- **Connection**: The local `engineering/pdf-forge/interactive-testing/` directory maps directly to `/workspace/shared/` on Forgs

**⚠️ CRITICAL MAPPING - AVOID CONFUSION:**

- ✅ **CORRECT**: engineering/pdf-forge/interactive-testing/` → `/workspace/shared/` on Forge
- ❌ **WRONG**: `engineering/pdf-forge/interactive-testing/shared/` → `/workspace/shared/shared/` on Forge (nested confusion!)
- **NEVER create a `shared/` subdirectory inside `engineering/pdf-forge/interactive-testing/`**

**Monitoring Script**: `watch-shared-workspace.js` (Enhanced by Claude v1.0)

- **Auto-detection**: Monitors for new test requests, processes them automatically
- **Result Format**: JSON files with detailed analysis and error reporting
- **Temporary testing**: Templates copied to `/tmp/` for testing, NOT installed permanently

## Directory Structure on PDF Forge

```
/workspace/shared/
├── test-requests/          # Drop test requests here
│   └── processed/          # Completed requests moved here
├── test-results/           # JSON results appear here
├── templates/              # All .latex and .sty files
├── test-documents/         # Test markdown files
├── assets/                # Images and other assets (PNG, JPG, etc.)
├── output-pdfs/           # Generated PDFs
└── status/                # Activity logs, ready signals
    ├── activity.log       # Real-time monitoring log
    ├── errors.log         # Error details
    └── forge-ready.txt    # System ready signal
```

## Usage Workflow

### 1. Start PDF Forge Listener
**You (Stephen) run on PDF Forge system:**
```bash
# Start the monitoring daemon
node /path/to/watch-shared-workspace.js

# Verify it's running
cat /workspace/shared/status/forge-ready.txt
```

### 2. Create Test Request (Claude drops files locally)
**Claude's Workflow:**
- Drop test markdown files in: `engineering/pdf-forge/interactive-testing/test-documents/`
- **CRITICAL**: Drop request JSON in: `engineering/pdf-forge/interactive-testing/test-requests/` (NOT in root!)
- Read results from: `engineering/pdf-forge/interactive-testing/test-results/`
- Templates (.sty files) go in: `engineering/pdf-forge/interactive-testing/templates/`
- **ASSETS**: Images (PNG, JPG) go in: `engineering/pdf-forge/interactive-testing/assets/`

**🔴 COMMON MISTAKE**: Creating a `shared/` subdirectory - remember `engineering/pdf-forge/interactive-testing/` itself IS the shared workspace!

**Test Request Format** (`test-request-YYYYMMDD-HHMM.json`):
```json
{
  "request_id": "smart-pins-list-test-001",
  "template": "p2kb-smart-pins.latex",
  "timestamp": "2025-08-26T12:34:56Z",
  "tests": [
    {
      "name": "list-formatting-test",
      "input": "smart-pins-test-sample.md"
    }
  ],
  "options": {
    "auto_fix_attempt": false,
    "cleanup": true
  },
  "notification": {
    "status_file": "current-test-status.txt"
  }
}
```

**🚨 CRITICAL: Test Request with Lua Filters (CORRECT FORMAT):**
```json
{
  "request_id": "test-with-filters",
  "template": "p2kb-smart-pins.latex",
  "tests": [
    {
      "name": "colored-code-blocks",
      "input": "test-document.md",
      "lua_filters": ["smart-pins-block-coloring"]  // ✅ CORRECT
    }
  ]
}
```

**Multiple Tests Comparison Example:**
```json
{
  "request_id": "comparison-test",
  "template": "p2kb-smart-pins.latex",
  "tests": [
    {
      "name": "without-filters",
      "input": "test-document.md"
    },
    {
      "name": "with-color-filters",
      "input": "test-document.md",
      "lua_filters": ["smart-pins-colored-blocks"]
    },
    {
      "name": "with-multiple-filters",
      "input": "test-document.md",
      "lua_filters": ["smart-pins-colored-blocks", "part-chapter-pagebreaks"]
    }
  ]
}
```

**Multi-Filter Success Pattern (De Silva Example):**
```json
{
  "template": "p2kb-pasm-desilva.latex",
  "tests": [{
    "name": "combined-filters",
    "input": "desilva-test.md",
    "lua_filters": [
      "part-chapter-pagebreaks",      // Page break control (runs first)
      "desilva-div-to-environment"    // ::: sidetrack → \begin{sidetrack} (runs second)
    ],
    "pandoc_args": ["--top-level-division=part"],
    "debug_tex": true  // Outputs .tex file for inspection
  }]
}
```

**Filter Processing Notes:**
- Filters process in the specified sequence (order matters!)
- Each filter can see the output of previous filters
- Use `debug_tex: true` to get .tex files showing filter execution

**❌ WRONG FORMAT (will fail):**
```json
{
  "tests": [
    {
      "pandoc_args": ["--lua-filter=smart-pins-block-coloring"]  // ❌ WRONG - daemon can't find filter
    }
  ]
}
```

**Key Points for Lua Filters:**
- Use `lua_filters` array, NOT `pandoc_args`
- Provide filter name only (no path, no .lua extension)
- Daemon builds path as: `/workspace/shared/filters/[name].lua`
- Multiple filters supported: `"lua_filters": ["filter1", "filter2"]`

### 3. Deploy Files to Forge
**Claude prepares, you deploy:**
- `templates/` - All .latex templates and .sty files
- `test-documents/` - Markdown test files
- `test-requests/` - JSON request files
- `assets/` - Image files referenced in markdown (PNG, JPG, etc.)

### 4. Monitor Results (Claude reads automatically)
**Result File** (`smart-pins-list-test-001-result.json`):
```json
{
  "request_id": "smart-pins-list-test-001",
  "status": "completed",
  "overall_result": "success|partial_failure|error",
  "test_results": [
    {
      "name": "list-formatting-test",
      "status": "✅ PASS|❌ FAIL|🔧 FIXED",
      "pdf_path": "output-pdfs/list-formatting-test-1234567890.pdf",
      "error": null,
      "error_analysis": {
        "recognized": true,
        "cause": "Missing \\real{} command",
        "solution": "Add \\newcommand*{\\real}[1]{#1}",
        "auto_fixable": true
      }
    }
  ],
  "performance": {
    "total_duration_ms": 2500,
    "tests_run": 1,
    "failures": 0
  }
}
```

## Testing vs Manual Production Deployment

### Why Automated Testing Helps Debug Path Issues

**Testing Environment Benefits:**
- ✅ System automatically finds filters in `/workspace/shared/filters/`
- ✅ Handles all path resolution internally for testing
- ✅ Tests multiple filters simultaneously
- ✅ Validates templates work correctly before production use

**Production Deployment (Manual):**
- 📦 User receives tested templates from Claude
- 🔧 User manually copies templates to PDF Forge `./templates/` directory
- 📄 User copies filters to PDF Forge `./filters/` directory if needed
- ⚡ User runs `generate-pdf.js` with tested, validated templates

**Key Insight:** Testing validates templates work correctly, but does NOT install them. Manual deployment to production is still required.

## Debug Information Available

When tests run, you get comprehensive debug information:

### TEX File Output (with `debug_tex: true`)
- Shows Lua filter debug comments
- Displays actual LaTeX commands generated
- Reveals filter processing sequence
- Includes timing and execution markers

### Filter Execution Tracking
- Verify which filters ran and in what order
- See the effects of each filter on the output
- Identify transformation points in the pipeline

### Error Isolation
- Pinpoint which specific filter failed (if any)
- See exact error messages from Pandoc
- Get line numbers and context for LaTeX errors
- Understand filter interaction issues

## Error Analysis Intelligence

**Built-in Pattern Recognition:**
- **Missing \\real{}**: LaTeX table calculations
- **lstset blocks**: Unclosed code highlighting
- **\\tightlist**: Missing Pandoc list command
- **Template paths**: .sty file dependency issues
- **Auto-fix capable**: High confidence errors

## 🔄 CRITICAL WORKFLOW UNDERSTANDING: Testing vs Production

**IMPORTANT**: Automated testing is **TEMPORARY ONLY** - it does NOT deploy templates!

**How Testing Works:**
1. **Templates copied FROM**: `/workspace/shared/templates/` (testing location)
2. **Templates copied TO**: `/tmp/pandoc-work-*/` (temporary working directory)
3. **After testing**: Temporary directory cleaned up, nothing installed permanently

**Testing vs Production Template Locations:**
- **Testing templates**: `/workspace/shared/templates/` - Used ONLY for testing
- **Production templates**: `./templates/` - Used by `generate-pdf.js` for final PDFs
- **No automatic sync**: Changes to testing templates do NOT affect production templates

### Manual Template Deployment Required
**After Claude completes automated testing:**
- ✅ **Templates debugged** - Testing validates templates work correctly
- ⚠️ **Manual deployment needed** - User must copy fixed templates to production
- 📄 **Deliverables include templates** - Fixed .sty/.latex files must be provided
- 🔧 **User installs templates** - Copy to PDF Forge production `./templates/` directory

**Workflow:**
1. Claude tests templates in `/workspace/shared/templates/` (temporary testing)
2. Claude provides fixed templates to user (outbound deliverables)
3. User manually copies templates to PDF Forge production location
4. User runs `generate-pdf.js` for final PDF generation

## Integration with Visual Refinement

### Smart Pins Visual Testing Example (with Color Blocks)
```json
{
  "request_id": "smart-pins-visual-v1",
  "template": "p2kb-smart-pins.latex",
  "tests": [
    {
      "name": "colored-blocks-test",
      "input": "smart-pins-test.md",
      "lua_filters": ["smart-pins-block-coloring"]  // Applies color environments
    },
    {
      "name": "plain-test",
      "input": "smart-pins-test.md"  // No filters for comparison
    }
  ]
}
```

**Result**: Two PDFs showing before/after list formatting for visual comparison.

### Template Change Testing
```json
{
  "request_id": "template-regression-test",
  "template": "p2kb-smart-pins-content.sty",
  "tests": [
    {
      "name": "minimal-doc",
      "input": "minimal-smart-pins.md"
    },
    {
      "name": "full-chapter",
      "input": "full-smart-pins-chapter.md"
    }
  ]
}
```

**Result**: Validates template changes don't break existing functionality.

## File Management Protocol

### Template Deployment
1. **All .sty files** must be in `templates/` directory
2. **Working directory setup** automatically copies all .sty files for each test
3. **Template paths** resolved automatically by monitoring script

### Test Document Creation
1. **Small samples** - Focus on specific issues (list formatting, code blocks)
2. **A/B testing** - Same content, different formatting approaches
3. **Regression testing** - Minimal docs that must always work

### Result Processing
1. **JSON parsing** - Claude reads results automatically
2. **PDF review** - You review visual output for approval
3. **Iteration** - Quick cycle: change → test → review → repeat

## Asset Handling for Images and Resources

### 🔴 CRITICAL: How Assets Work with PDF Generation

**The Two-Stage Process:**
1. **Pandoc Stage**: Converts markdown → LaTeX using `--resource-path`
2. **XeLaTeX Stage**: Converts LaTeX → PDF using `TEXINPUTS` environment variable

**Asset Resolution:**
- **Markdown references**: `![Image](assets/my-image.png)` 
- **Pandoc finds it**: Via `--resource-path=/workspace/shared` 
- **XeLaTeX finds it**: Via `TEXINPUTS=/workspace/shared//:...`

**CRITICAL for Images with Spaces:**
The monitoring script (`watch-shared-workspace.js`) now correctly sets the `TEXINPUTS` environment variable to handle images with spaces in filenames. This was fixed in version Enhanced by Claude v1.0.

**Example with spaces in filename:**
```markdown
![Smart Pin Mode](assets/P2 SmartPins-220809_mode01001_page21_img01.png)
```

**This now works correctly** because:
1. Pandoc handles the spaces during markdown→LaTeX conversion
2. XeLaTeX finds the file via TEXINPUTS environment variable
3. The Lua filter (if used) properly handles URL-encoded spaces (%20)

### Asset Directory Best Practices

1. **Always use `assets/` subfolder** for images
2. **Reference from markdown** as `assets/filename.png`
3. **Spaces in filenames** are now fully supported
4. **Supported formats**: PNG, JPG, PDF, EPS
5. **Path style**: Use forward slashes even on Windows

### Testing Asset Handling

**Test Request with Assets:**
```json
{
  "request_id": "asset-test",
  "template": "p2kb-smart-pins.latex",
  "tests": [
    {
      "name": "images-with-spaces",
      "input": "test-with-images.md"
    }
  ]
}
```

**Test Markdown (`test-with-images.md`):**
```markdown
# Image Test

## Image without spaces
![Test](assets/simple-image.png)

## Image with spaces in filename  
![Test](assets/P2 SmartPins-220809_page21_img01.png)
```

## Performance Characteristics

**Typical Response Times:**
- **Simple template test**: 2-5 seconds
- **Complex document**: 10-15 seconds
- **Template with .sty dependencies**: 5-10 seconds
- **Error analysis**: < 1 second additional

**Concurrent Testing**: Single request processing (queued if multiple)

## Ready Check Commands

**Verify system status:**
```bash
# Check if daemon is running
cat /workspace/shared/status/forge-ready.txt

# Monitor real-time activity
tail -f /workspace/shared/status/activity.log

# Check recent errors
tail -5 /workspace/shared/status/errors.log
```

**Emergency reset:**
```bash
# Clear all pending requests
rm /workspace/shared/test-requests/*.json

# Clear old results (optional)
rm /workspace/shared/test-results/*-result.json
```

## Integration with Smart Pins Visual Work

**Perfect for:**
- List formatting A/B testing
- Template regression validation
- Code block coloring experiments
- Quick visual iteration cycles

**Workflow Integration:**
1. Claude creates test request with current workspace content
2. You start PDF Forge listener (if not running)
3. Claude monitors results automatically
4. Visual comparison guides next iteration
5. Repeat until perfect

---

**This system transforms slow manual PDF cycles into rapid 30-second iterations.**
