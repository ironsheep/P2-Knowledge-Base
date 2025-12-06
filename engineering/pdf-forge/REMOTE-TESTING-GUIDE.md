# Remote Claude Interactive Testing Guide

**For Claude Instances Using Doc Forge Template Testing**

This document explains how to use the Doc Forge interactive template testing workflow from Claude's perspective. Claude submits test requests and reads results; the human operator manages the daemon on the PDF Forge system.

---

## System Overview

Doc Forge runs in a devcontainer with full LaTeX/Pandoc tooling. The **interactive testing system** allows Claude to:

1. Submit template test requests via JSON files
2. Get PDF generation results with full diagnostics
3. View generated PDFs via PNG thumbnails
4. Access `.tex` files for debugging
5. Track request status in real-time

### Key Features

- **Request Queue**: Requests are never lost - they're queued and processed in FIFO order
- **Hierarchical Output**: Each test run gets its own directory with all artifacts
- **Per-Test Results**: Individual result files for each test with complete file manifests
- **Visual Verification**: PNG thumbnails of generated PDFs
- **Error Recovery**: Daemon survives errors and continues processing

---

## Directory Structure

**Local Path**: `engineering/pdf-forge/interactive-testing/`
**Maps To**: `/workspace/shared/` on PDF Forge

```
/workspace/shared/
├── templates/           # LaTeX templates (.latex) and styles (.sty)
├── filters/             # Lua filters for Pandoc (.lua)
├── test-documents/      # Markdown test input files (.md)
├── test-requests/       # Submit JSON test requests here
│   └── processed/       # Completed requests archived here
├── test-runs/           # Output: one folder per request
│   └── {request-id}_{timestamp}/
│       ├── request.json     # Copy of original request
│       ├── summary.json     # Overall run result
│       └── {test-name}/     # One folder per test
│           ├── result.json  # Test result with file paths
│           ├── output.pdf   # Generated PDF
│           ├── output.tex   # Generated TeX (for debugging)
│           └── thumbnail.png # PNG of first page
└── status/
    ├── forge-ready.txt      # Created when daemon is ready
    ├── queue-status.json    # Current queue state
    ├── request-{id}.status.json  # Per-request status
    ├── activity.log         # Real-time activity log
    └── errors.log           # Error-specific log
```

---

## Test Request Format

Create a JSON file in `/workspace/shared/test-requests/`:

```json
{
  "format_type": "template_testing",
  "request_id": "my-test-001",
  "template": "p2kb-sp-template.latex",
  "metadata": {
    "title": "Test Document",
    "author": "Test Author"
  },
  "tests": [
    {
      "name": "basic-test",
      "input": "test-input.md",
      "lua_filters": ["p2kb-sp-code-coloring"],
      "pandoc_args": ["--toc"],
      "metadata": {
        "subtitle": "Test-specific metadata"
      }
    },
    {
      "name": "advanced-test",
      "input": "complex-input.md",
      "lua_filters": ["p2kb-sp-code-coloring", "p2kb-sp-pagination"]
    }
  ]
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `template` | Template filename with `.latex` extension |
| `tests` | Array of test configurations |
| `tests[].name` | Unique test identifier (becomes folder name) |
| `tests[].input` | Markdown file in `test-documents/` |

### Optional Fields

| Field | Description |
|-------|-------------|
| `request_id` | Custom ID (defaults to filename without .json) |
| `metadata` | Request-level metadata (applies to all tests) |
| `tests[].lua_filters` | Array of filter names (without `.lua`) |
| `tests[].pandoc_args` | Additional pandoc arguments |
| `tests[].metadata` | Test-specific metadata (overrides request-level) |
| `tests[].variables` | Legacy support for variables |

### Metadata Hierarchy

Metadata merges in this priority order (highest wins):
1. Test-level `metadata` and `variables`
2. Request-level `metadata`
3. Default metadata (title, author, date, documentclass, etc.)

---

## Workflow

### 1. Prepare Test Documents

Place Markdown files in `engineering/pdf-forge/interactive-testing/test-documents/`:

```markdown
# Test Document

This tests the template rendering.

## Code Block Test

```spin2
PUB main()
  repeat
    waitms(1000)
```

## Table Test

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
```

### 2. Prepare Templates and Filters

Copy your `.latex` template and `.sty` files to `interactive-testing/templates/`.

Copy any `.lua` filters to `interactive-testing/filters/`.

### 3. Submit Test Request

Create a JSON file in `interactive-testing/test-requests/`:

```json
{
  "template": "p2kb-sp-template.latex",
  "tests": [
    {
      "name": "basic",
      "input": "my-test.md"
    }
  ]
}
```

### 4. Check Results

After the daemon processes the request, find results in `interactive-testing/test-runs/`:

- **Summary**: `test-runs/{request-id}_{timestamp}/summary.json`
- **Per-test result**: `test-runs/{request-id}_{timestamp}/{test-name}/result.json`
- **PDF output**: `test-runs/{request-id}_{timestamp}/{test-name}/output.pdf`
- **Thumbnail**: `test-runs/{request-id}_{timestamp}/{test-name}/thumbnail.png`

### 5. Monitor Status (Optional)

Read status files to check processing state:
- `status/queue-status.json` - Current queue state
- `status/request-{id}.status.json` - Per-request status
- `status/activity.log` - Activity log

---

## Output Files

### Summary File (`summary.json`)

Located at `test-runs/{run-id}/summary.json`:

```json
{
  "request_id": "my-test-001",
  "run_id": "my-test-001_1699123456",
  "run_path": "/workspace/shared/test-runs/my-test-001_1699123456",
  "status": "completed",
  "started_at": "2025-01-15T10:30:00.000Z",
  "completed_at": "2025-01-15T10:30:15.000Z",
  "template": "p2kb-sp-template.latex",
  "tests": {
    "basic": {
      "result": "✅ PASS",
      "result_file": "basic/result.json",
      "has_pdf": true,
      "has_thumbnail": true,
      "duration_ms": 3500
    },
    "advanced": {
      "result": "❌ FAIL",
      "result_file": "advanced/result.json",
      "has_pdf": false,
      "has_thumbnail": false,
      "duration_ms": 1200
    }
  },
  "overall_result": "partial_failure",
  "pass_count": 1,
  "fail_count": 1,
  "total_duration_ms": 4700
}
```

### Per-Test Result File (`result.json`)

Located at `test-runs/{run-id}/{test-name}/result.json`:

```json
{
  "request_id": "my-test-001_1699123456",
  "test_name": "basic",
  "status": "completed",
  "result": "✅ PASS",
  "started_at": "2025-01-15T10:30:00.000Z",
  "completed_at": "2025-01-15T10:30:03.500Z",
  "duration_ms": 3500,
  "template": "p2kb-sp-template.latex",
  "input_file": "test-input.md",
  "lua_filters": ["p2kb-sp-code-coloring"],
  "pandoc_args": ["--toc"],
  "generated_files": {
    "pdf": {
      "path": "/workspace/shared/test-runs/my-test-001_1699123456/basic/output.pdf",
      "relative_path": "basic/output.pdf",
      "size_bytes": 45231,
      "exists": true
    },
    "tex": {
      "path": "/workspace/shared/test-runs/my-test-001_1699123456/basic/output.tex",
      "relative_path": "basic/output.tex",
      "exists": true
    },
    "thumbnail": {
      "path": "/workspace/shared/test-runs/my-test-001_1699123456/basic/thumbnail.png",
      "relative_path": "basic/thumbnail.png",
      "exists": true
    }
  },
  "pdf_info": {
    "pages": "5",
    "page_size": "595.276 x 841.89 pts (A4)",
    "pdf_version": "1.5"
  },
  "error": null,
  "error_analysis": null
}
```

### On Failure

```json
{
  "test_name": "advanced",
  "status": "completed",
  "result": "❌ FAIL",
  "generated_files": {
    "pdf": {
      "exists": false
    },
    "tex": {
      "path": "/workspace/shared/test-runs/.../advanced/output.tex",
      "exists": true
    },
    "thumbnail": {
      "exists": false
    }
  },
  "error": "! LaTeX Error: Missing \\begin{document}...",
  "error_analysis": {
    "recognized": true,
    "cause": "Template structure error - document body not started",
    "solution": "Ensure template has \\begin{document} before $body$",
    "confidence": 0.95,
    "auto_fixable": true
  }
}
```

---

## Viewing Generated PDFs

The system generates PNG thumbnails of the first page for each successful PDF. To view:

1. **Read the thumbnail directly** (Claude can view PNG images):
   ```
   interactive-testing/test-runs/{run-id}/{test-name}/thumbnail.png
   ```

2. **Check PDF metadata** in `result.json`:
   - `pdf_info.pages` - number of pages
   - `generated_files.pdf.size_bytes` - file size

3. **Examine the .tex file** for debugging:
   ```
   interactive-testing/test-runs/{run-id}/{test-name}/output.tex
   ```

---

## Error Patterns

The system recognizes common LaTeX errors and provides solutions:

| Error Pattern | Cause | Solution |
|---------------|-------|----------|
| `Missing number, treated as zero` | Missing `\real{}` command | Add `\newcommand*{\real}[1]{#1}` |
| `Paragraph ended before \lstset@ was complete` | Unclosed lstset block | Check for missing `}` |
| `Undefined control sequence.*tightlist` | Missing tightlist definition | Add `\providecommand{\tightlist}{...}` |
| `File .* not found` | Missing file reference | Verify all files exist |
| `Environment .* undefined` | Missing package | Include required package |
| `Missing \begin{document}` | Template structure error | Add `\begin{document}` before `$body$` |

---

## Timeouts

| Operation | Timeout |
|-----------|---------|
| TEX generation | 5 minutes |
| PDF generation | 10 minutes |
| Thumbnail generation | 30 seconds |

---

## Troubleshooting

### Request Not Processing

1. Check queue status file:
   ```
   interactive-testing/status/queue-status.json
   ```

2. Check if request was archived (already processed):
   ```
   interactive-testing/test-requests/processed/
   ```

3. Check activity log:
   ```
   interactive-testing/status/activity.log
   ```

### Template Not Found

Verify template exists with exact filename in `interactive-testing/templates/`.

### Test Input Not Found

Verify input file exists in `interactive-testing/test-documents/`.

### PDF Generated But Looks Wrong

1. View the thumbnail:
   ```
   test-runs/{run-id}/{test-name}/thumbnail.png
   ```

2. Check the `.tex` file for what Pandoc generated:
   ```
   test-runs/{run-id}/{test-name}/output.tex
   ```

3. Verify Lua filters are in `interactive-testing/filters/`.

---

## Complete Example

### 1. Place Template Files

Copy to `interactive-testing/templates/`:
- `my-template.latex`
- Any required `.sty` files

### 2. Place Lua Filters

Copy to `interactive-testing/filters/`:
- `my-filter.lua`

### 3. Create Test Document

Create `interactive-testing/test-documents/my-test.md`:

```markdown
# My Test Document

Testing template functionality.

## Section One

Some content here.
```

### 4. Submit Test Request

Create `interactive-testing/test-requests/my-test-request.json`:

```json
{
  "template": "my-template.latex",
  "tests": [
    {
      "name": "basic",
      "input": "my-test.md",
      "lua_filters": ["my-filter"]
    }
  ]
}
```

### 5. Check Results

After processing, read:
- `test-runs/my-test-request_{timestamp}/summary.json` - Overall result
- `test-runs/my-test-request_{timestamp}/basic/result.json` - Test details
- `test-runs/my-test-request_{timestamp}/basic/thumbnail.png` - Visual preview
