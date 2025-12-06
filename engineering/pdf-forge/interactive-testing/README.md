# PDF Forge Shared Workspace (Interactive Testing)

**Purpose**: Communication bridge between Claude (P2-Knowledge-Base host) and PDF Forge container
**Mount Target**: `/workspace/shared` (bind mount from THIS directory: `engineering/pdf-forge/interactive-testing/`)
**Workflow**: Template testing only

📚 **COMPREHENSIVE GUIDE**: For complete usage instructions, request format, result format, and examples, see:
**[../REMOTE-TESTING-GUIDE.md](../REMOTE-TESTING-GUIDE.md)**

## Directory Structure

⚠️ **IMPORTANT**: This directory (`engineering/pdf-forge/interactive-testing/`) maps directly to `/workspace/shared/` on PDF Forge. Don't create a separate `shared/` subdirectory!

```
interactive-testing/  (this directory)
├── test-requests/           # JSON test requests from Claude → Forge
│   ├── *.json              # Active requests (watched by forge)
│   └── processed/          # Completed requests (archived)
├── test-runs/              # Output: one folder per request
│   └── {request-id}_{timestamp}/
│       ├── request.json    # Copy of original request
│       ├── summary.json    # Overall run result
│       └── {test-name}/    # One folder per test
│           ├── result.json     # Test result with file paths
│           ├── output.pdf      # Generated PDF
│           ├── output.tex      # Generated TeX (for debugging)
│           └── thumbnail.png   # PNG of first page
├── templates/              # Template files for testing
│   └── *.latex            # Templates and .sty files
├── filters/               # Lua filters for Pandoc
│   └── *.lua              # Filter files
├── test-documents/         # Standard test markdown files
│   ├── minimal.md          # Basic functionality test
│   ├── tables-complex.md   # Table/\real{} command test
│   ├── code-blocks.md      # Code highlighting/lstset test
│   └── *.md               # Other test documents
└── status/                # Communication/coordination files
    ├── forge-ready.txt        # Container startup indicator
    ├── queue-status.json      # Current queue state
    ├── activity.log           # Real-time activity log
    └── errors.log             # Error-specific log
```

## Container Mount Configuration

Add this mount to your PDF Forge container configuration:

```json
"mounts": [
  "source=${localWorkspaceFolder}/inbox,target=/workspace/inbox,type=bind",
  "source=${localWorkspaceFolder}/outbox,target=/workspace/outbox,type=bind", 
  "source=/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/engineering/pdf-forge/interactive-testing,target=/workspace/shared,type=bind"
]
```

## Related Documentation

| Document | Purpose |
|----------|---------|
| **[REMOTE-TESTING-GUIDE.md](../REMOTE-TESTING-GUIDE.md)** | Complete testing workflow and result format |
| **[TESTING-REQUEST-FORMAT.md](../TESTING-REQUEST-FORMAT.md)** | Detailed request format specification |
| **[AI-FORMAT-DECISION-GUIDE.md](../AI-FORMAT-DECISION-GUIDE.md)** | Choose between production and testing workflows |

## Quick Reference

### Request Processing Flow

1. **Claude** places templates in `templates/`, test docs in `test-documents/`
2. **Claude** creates test request JSON in `test-requests/`
3. **PDF Forge daemon** detects and processes request
4. **Results** appear in `test-runs/{request-id}_{timestamp}/`
5. **Claude** reads `summary.json` and per-test `result.json` files

### Minimal Test Request

```json
{
  "template": "my-template.latex",
  "tests": [
    {
      "name": "basic-test",
      "input": "test-document.md"
    }
  ]
}
```

See **[REMOTE-TESTING-GUIDE.md](../REMOTE-TESTING-GUIDE.md)** for complete examples and result format.