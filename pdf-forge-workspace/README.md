# PDF Forge Shared Workspace

**Purpose**: Communication bridge between Claude (P2-Knowledge-Base host) and PDF Forge container  
**Mount Target**: `/workspace/shared` (bind mount from this directory)

## Directory Structure

```
pdf-forge-workspace/
├── test-requests/           # JSON test requests from Claude → Forge
│   ├── *.json              # Active requests (watched by forge)
│   └── processed/          # Completed requests (archived)
├── test-results/           # JSON test results from Forge → Claude  
│   ├── *.json              # Test results and error reports
│   └── archives/           # Historical results
├── templates/              # Template files for testing
│   └── *.latex            # Templates developed by Claude
├── test-documents/         # Standard test markdown files
│   ├── minimal.md          # Basic functionality test
│   ├── tables-complex.md   # Table/\real{} command test
│   ├── code-blocks.md      # Code highlighting/lstset test
│   └── stress-test.md      # Comprehensive test
├── output-pdfs/           # Generated PDF outputs
│   └── *.pdf              # Test results for visual inspection
└── status/                # Communication/coordination files
    ├── forge-ready.txt    # Container startup indicator
    ├── claude-working.txt # Host development status
    └── last-activity.txt  # Latest activity timestamp
```

## Container Mount Configuration

Add this mount to your PDF Forge container configuration:

```json
"mounts": [
  "source=${localWorkspaceFolder}/inbox,target=/workspace/inbox,type=bind",
  "source=${localWorkspaceFolder}/outbox,target=/workspace/outbox,type=bind", 
  "source=/Users/stephen/Projects/Projects-ExtGit/IronSheepProductionsLLC/Propeller2/P2-Language-Study/P2-Knowledge-Base/pdf-forge-workspace,target=/workspace/shared,type=bind"
]
```

## Communication Protocol

### Request Format (Claude → Forge)
```json
{
  "request_id": "smart-pins-2025-08-25-001",
  "action": "test-template",
  "template": "p2kb-smart-pins.latex",
  "test_suite": "comprehensive",
  "options": {
    "generate_pdfs": true,
    "auto_fix": true,
    "regression_check": true
  },
  "tests": ["minimal", "tables", "code-blocks"]
}
```

### Response Format (Forge → Claude)
```json
{
  "request_id": "smart-pins-2025-08-25-001", 
  "status": "completed",
  "timestamp": "2025-08-25T14:32:15Z",
  "overall_result": "success",
  "test_results": [
    {
      "name": "minimal",
      "status": "✅ PASS",
      "pdf_path": "output-pdfs/minimal.pdf"
    }
  ]
}
```

## Usage

### From Claude (P2-Knowledge-Base)
```bash
# 1. Place template for testing
cp template.latex pdf-forge-workspace/templates/

# 2. Create test request
cat > pdf-forge-workspace/test-requests/test-$(date +%s).json << EOF
{"template": "template.latex", "action": "test-template"}
EOF

# 3. Monitor for results
tail -f pdf-forge-workspace/test-results/*.json
```

### From PDF Forge Container  
```bash
# Enhanced scripts watch /workspace/shared/
# - Detect new requests automatically
# - Process templates and run tests
# - Write results back to shared space
# - Archive completed requests
```

## Enhanced Scripts Integration

The PDF Forge container runs enhanced scripts that monitor this shared workspace:
- `watch-shared-workspace.js` - Main monitoring daemon
- `auto-fix-analyzer.js` - Intelligent error analysis  
- Enhanced `generate-pdf.js` - Testing mode capabilities

## Version Control

- **P2-Knowledge-Base repo**: Contains this workspace (templates, requests, results)
- **PDF-Forge repo**: Contains enhanced scripts that process this workspace
- **Bind mount**: Bridges both repos through filesystem sharing