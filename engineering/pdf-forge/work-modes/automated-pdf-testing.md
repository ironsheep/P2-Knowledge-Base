# Automated PDF Testing System Usage Guide

**DUAL PURPOSE**: 
1. **Rapid iteration testing** for PDF template development and visual refinement
2. **Automatic template deployment** - Forge updates its permanent template library during testing

## System Architecture

**CRITICAL CONNECTION:**
- **My Local Access**: `/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/pdf-forge-workspace`
- **PDF Forge Shared Workspace**: `/workspace/shared/` (on PDF Forge system)
- **Connection**: The local `pdf-forge-workspace/` directory maps directly to `/workspace/shared/` on Forge

**⚠️ CRITICAL MAPPING - AVOID CONFUSION:**
- ✅ **CORRECT**: `pdf-forge-workspace/` → `/workspace/shared/` on Forge
- ❌ **WRONG**: `pdf-forge-workspace/shared/` → `/workspace/shared/shared/` on Forge (nested confusion!)
- **NEVER create a `shared/` subdirectory inside `pdf-forge-workspace/`**

**Monitoring Script**: `watch-shared-workspace.js` (Enhanced by Claude v1.0)
- **Auto-detection**: Monitors for new test requests, processes them automatically
- **Result Format**: JSON files with detailed analysis and error reporting
- **🔴 CRITICAL**: Automatically updates Forge's permanent template collection with any .sty/.latex files from testing

## Directory Structure on PDF Forge

```
/workspace/shared/
├── test-requests/          # Drop test requests here
│   └── processed/          # Completed requests moved here
├── test-results/           # JSON results appear here
├── templates/              # All .latex and .sty files
├── test-documents/         # Test markdown files
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
- Drop test markdown files in: `pdf-forge-workspace/test-documents/`
- **CRITICAL**: Drop request JSON in: `pdf-forge-workspace/test-requests/` (NOT in root!)
- Read results from: `pdf-forge-workspace/test-results/`
- Templates (.sty files) go in: `pdf-forge-workspace/templates/`

**🔴 COMMON MISTAKE**: Creating a `shared/` subdirectory - remember `pdf-forge-workspace/` itself IS the shared workspace!

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

## Error Analysis Intelligence

**Built-in Pattern Recognition:**
- **Missing \\real{}**: LaTeX table calculations 
- **lstset blocks**: Unclosed code highlighting
- **\\tightlist**: Missing Pandoc list command
- **Template paths**: .sty file dependency issues
- **Auto-fix capable**: High confidence errors

## 🔄 CRITICAL WORKFLOW INSIGHT: Testing = Automatic Deployment

**DISCOVERY**: Automated testing serves dual functions:
1. **Debug templates** through rapid iteration
2. **Deploy fixes** automatically to Forge's permanent template library

**RESULT**: By completion of automated testing cycles, **Forge has updated templates**!

### Streamlined Human Workflow
**After Claude completes automated testing:**
- ✅ **Forge templates updated** - All .sty/.latex fixes absorbed into permanent collection
- 📄 **Human gets clean deliverables** - Just markdown + request.json
- ❌ **No .sty file management** - Forge already has corrected templates
- ⚡ **Immediate PDF generation** - Human can generate full documents without template setup

**Before this discovery**: Human managed .sty files manually  
**After this discovery**: Claude's testing auto-deploys templates, human gets content-only deliverables

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