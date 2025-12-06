# Testing Request Format Specification
**Template Testing Workflow for `watch-shared-workspace.js`**

## 📋 Quick Reference

**Format Type**: `template_testing`  
**Script**: `watch-shared-workspace.js`  
**Purpose**: Test template behavior and validate template development  
**Decision Guide**: See [AI-FORMAT-DECISION-GUIDE.md](AI-FORMAT-DECISION-GUIDE.md)

---

## 🎯 Complete Format Specification

### Basic Structure
```json
{
  "format_type": "template_testing",
  "template": "template-name.latex",
  "metadata": {
    "title": "Default title for all tests",
    "author": "Default author"
  },
  "tests": [
    {
      "name": "test-case-name",
      "input": "test-input.md",
      "metadata": {...},
      "pandoc_args": [...],
      "lua_filters": [...],
      "variables": {...}
    }
  ],
  "options": {...},
  "notification": {...}
}
```

### Required Fields
- **`template`** *(string)*: LaTeX template filename (must exist in `/workspace/shared/templates/`)
- **`tests`** *(array)*: Array of test case objects

### Optional Fields
- **`format_type`** *(string)*: Always `"template_testing"` (for AI recognition)
- **`metadata`** *(object)*: Default metadata for all tests
- **`options`** *(object)*: Processing options
- **`notification`** *(object)*: Status notification settings

---

## 📝 Field-by-Field Documentation

### `format_type` *(optional string)*
**Purpose**: AI recognition marker (ignored by script)  
**Value**: Always `"template_testing"`  
**Example**: `"format_type": "template_testing"`

### `template` *(required string)*
**Purpose**: Specifies which LaTeX template to test  
**Location**: Must exist in `/workspace/shared/templates/`  
**Example**: `"template": "p2kb-smart-pins.latex"`

### `metadata` *(optional object)*
**Purpose**: Default metadata applied to all tests  
**Hierarchy**: Request metadata < Test metadata < Test variables  
**Common Fields**:
```json
"metadata": {
  "title": "Smart Pins Template Test Suite",
  "author": "PDF Forge Test System",
  "date": "2025",
  "documentclass": "book",
  "fontsize": "11pt",
  "papersize": "a4paper"
}
```

### `tests` *(required array)*
**Purpose**: Defines test cases to run against the template  
**Minimum**: At least one test object required

#### Test Object Structure
```json
{
  "name": "descriptive-test-name",
  "input": "input-file.md",
  "metadata": {...},
  "pandoc_args": [...],
  "lua_filters": [...],
  "variables": {...}
}
```

#### Test Object Fields

**`name` *(required string)***: Unique identifier for test case
- Used for output file naming
- Should be descriptive and filesystem-safe
- Example: `"basic-functionality"`, `"code-blocks-test"`

**`input` *(required string)***: Input markdown file
- Must exist in `/workspace/shared/test-documents/`
- File extension typically `.md`
- Example: `"smart-pins-sample.md"`

**`metadata` *(optional object)***: Test-specific metadata
- Overrides request-level metadata
- Same format as request metadata
- Example: `"metadata": {"title": "Specific Test Title"}`

**`pandoc_args` *(optional array)***: Additional pandoc arguments
- Passed directly to pandoc command
- Array of strings
- Example: `["--toc", "--number-sections"]`

**`lua_filters` *(optional array)***: Lua filter names
- Files must exist in `/workspace/shared/filters/`
- `.lua` extension added automatically if missing
- Example: `["div-to-env", "code-blocks"]`

**`variables` *(optional object)***: Template variables
- Highest priority in metadata hierarchy
- Passed as pandoc variables
- Example: `"variables": {"custom_var": "test_value"}`

### `options` *(optional object)*
**Purpose**: Processing and behavior options

#### Available Options
```json
"options": {
  "auto_fix_attempt": true,
  "fail_fast": false,
  "debug_tex": true
}
```

**`auto_fix_attempt` *(boolean)***: Attempt automatic error fixes  
**`fail_fast` *(boolean)***: Stop on first test failure  
**`debug_tex` *(boolean)***: Generate .tex files for debugging

### `notification` *(optional object)*
**Purpose**: Status file creation for monitoring

```json
"notification": {
  "status_file": "test-complete.txt"
}
```

**`status_file` *(string)***: Creates status file in `/workspace/shared/status/`

---

## 🧪 Testing Scenario Examples

### Scenario 1: Basic Template Validation
**Use Case**: Verify template compiles with minimal content

```json
{
  "format_type": "template_testing",
  "template": "p2kb-smart-pins.latex",
  "metadata": {
    "title": "Smart Pins Template Basic Test",
    "author": "PDF Forge"
  },
  "tests": [
    {
      "name": "minimal-content",
      "input": "minimal-test.md"
    }
  ]
}
```

### Scenario 2: Multiple Document Testing
**Use Case**: Test template against various content types

```json
{
  "format_type": "template_testing",
  "template": "p2kb-desilva.latex",
  "metadata": {
    "title": "DeSilva Template Comprehensive Test",
    "documentclass": "book"
  },
  "tests": [
    {
      "name": "basic-text",
      "input": "text-only.md"
    },
    {
      "name": "code-heavy",
      "input": "code-examples.md"
    },
    {
      "name": "image-heavy",
      "input": "diagrams-test.md"
    },
    {
      "name": "mixed-content",
      "input": "comprehensive.md"
    }
  ]
}
```

### Scenario 3: Lua Filter Testing
**Use Case**: Validate custom div-to-environment conversion

```json
{
  "format_type": "template_testing",
  "template": "p2kb-smart-pins.latex",
  "tests": [
    {
      "name": "div-conversion-test",
      "input": "div-wrapped-content.md",
      "lua_filters": ["div-to-env"],
      "pandoc_args": ["--verbose"]
    }
  ],
  "options": {
    "debug_tex": true
  }
}
```

### Scenario 4: Variable Override Testing
**Use Case**: Test template with different variable configurations

```json
{
  "format_type": "template_testing",
  "template": "p2kb-foundation.latex",
  "metadata": {
    "documentclass": "book",
    "fontsize": "11pt"
  },
  "tests": [
    {
      "name": "default-variables",
      "input": "sample-content.md"
    },
    {
      "name": "custom-fonts",
      "input": "sample-content.md",
      "variables": {
        "mainfont": "Times New Roman",
        "monofont": "Courier New"
      }
    },
    {
      "name": "different-paper",
      "input": "sample-content.md",
      "variables": {
        "papersize": "letter",
        "fontsize": "12pt"
      }
    }
  ]
}
```

### Scenario 5: Comprehensive Test Suite
**Use Case**: Full template validation with all features

```json
{
  "format_type": "template_testing",
  "template": "p2kb-smart-pins.latex",
  "metadata": {
    "title": "Smart Pins Complete Validation Suite",
    "author": "P2 Knowledge Base",
    "date": "2025",
    "toc": true,
    "toc-depth": 3
  },
  "tests": [
    {
      "name": "basic-functionality",
      "input": "basic-test.md"
    },
    {
      "name": "code-blocks",
      "input": "pasm2-examples.md",
      "lua_filters": ["div-to-env"]
    },
    {
      "name": "advanced-formatting",
      "input": "complex-formatting.md",
      "pandoc_args": ["--number-sections"],
      "variables": {
        "custom_header": "Advanced Test"
      }
    },
    {
      "name": "error-conditions",
      "input": "edge-cases.md",
      "metadata": {
        "title": "Edge Case Testing"
      }
    }
  ],
  "options": {
    "auto_fix_attempt": true,
    "debug_tex": true
  },
  "notification": {
    "status_file": "smart-pins-test-complete.txt"
  }
}
```

---

## 🔧 Metadata Hierarchy & Processing

### Hierarchy Order (lowest to highest priority)
1. **Default Values** (hardcoded in script)
2. **Request Metadata** (`metadata` at root level)
3. **Test Metadata** (`metadata` in test object)
4. **Test Variables** (`variables` in test object)

### Example Hierarchy Resolution
```json
{
  "metadata": {
    "title": "Request Level Title",
    "author": "Request Author",
    "fontsize": "11pt"
  },
  "tests": [
    {
      "name": "test1",
      "input": "test.md",
      "metadata": {
        "title": "Test Level Title"
      },
      "variables": {
        "fontsize": "12pt"
      }
    }
  ]
}
```

**Final Variables for test1**:
- `title`: "Test Level Title" (test metadata overrides request)
- `author`: "Request Author" (from request metadata)
- `fontsize`: "12pt" (variables override everything)

---

## 📁 File Path Requirements

### Required Directory Structure
```
/workspace/shared/
├── templates/           # LaTeX templates (.latex files)
├── test-documents/      # Input markdown files (.md files)
├── filters/            # Lua filters (.lua files)
├── test-requests/      # Request JSON files
├── test-results/       # Output result files
├── output-pdfs/        # Generated PDF files
└── status/            # Status notification files
```

### File Naming Conventions
- **Templates**: `template-name.latex`
- **Test Inputs**: `descriptive-name.md`
- **Lua Filters**: `filter-name.lua`
- **Request Files**: `request-name.json`
- **Results**: `request-name-result.json`

---

## ⚠️ Error Handling & Troubleshooting

### Common Request Format Errors

#### Missing Required Fields
```json
// ❌ WRONG - Missing template field
{
  "tests": [{"name": "test1", "input": "file.md"}]
}

// ✅ CORRECT
{
  "template": "my-template.latex",
  "tests": [{"name": "test1", "input": "file.md"}]
}
```

#### Invalid Test Structure
```json
// ❌ WRONG - Missing required test fields
{
  "template": "test.latex",
  "tests": [{"name": "test1"}]  // Missing 'input' field
}

// ✅ CORRECT
{
  "template": "test.latex",
  "tests": [{"name": "test1", "input": "test.md"}]
}
```

#### File Path Errors
```json
// ❌ WRONG - File doesn't exist
{
  "template": "nonexistent.latex",
  "tests": [{"name": "test1", "input": "missing.md"}]
}

// ✅ CORRECT - Verify files exist
{
  "template": "existing-template.latex",  // Must exist in /templates/
  "tests": [{"name": "test1", "input": "existing-file.md"}]  // Must exist in /test-documents/
}
```

### Script Error Messages

**Template Not Found**:
```
❌ FATAL: Template not found: template-name.latex
```
**Resolution**: Verify template exists in `/workspace/shared/templates/`

**Test Input Not Found**:
```
❌ Test input file not found: input-name.md
```
**Resolution**: Verify input file exists in `/workspace/shared/test-documents/`

**Invalid JSON**:
```
❌ FATAL: Invalid JSON in request file: Unexpected token
```
**Resolution**: Validate JSON syntax with linter

**Missing Tests Field**:
```
❌ FATAL: Invalid request format - missing tests field
Expected format: {"template": "name.latex", "tests": [{"name": "test-name", "input": "file.md"}]}
```
**Resolution**: Add `tests` array with at least one test object

### Pandoc Errors

**Common pandoc errors and solutions**:

```
Missing number, treated as zero
→ Add \newcommand*{\real}[1]{#1} to template

Undefined control sequence \tightlist
→ Add \providecommand{\tightlist}{...} to template

Package not found
→ Ensure .sty files are in templates directory
```

---

## 🔍 Validation Checklist

Before submitting testing request:

- [ ] **JSON Syntax Valid** (use linter to verify)
- [ ] **Required Fields Present** (`template`, `tests`)
- [ ] **Template File Exists** (in `/workspace/shared/templates/`)
- [ ] **Test Input Files Exist** (in `/workspace/shared/test-documents/`)
- [ ] **Lua Filters Exist** (in `/workspace/shared/filters/` if specified)
- [ ] **Test Names Unique** (within same request)
- [ ] **Test Names Filesystem-Safe** (no spaces, special chars)
- [ ] **Metadata Structure Valid** (object format)
- [ ] **Pandoc Args Array** (if specified)
- [ ] **Variables Object Format** (if specified)

---

## 📊 Expected Output

Results appear in `interactive-testing/test-runs/{request-id}_{timestamp}/`.

### Directory Structure Per Run
```
test-runs/{request-id}_{timestamp}/
├── request.json     # Copy of original request
├── summary.json     # Overall run result
└── {test-name}/     # One folder per test
    ├── result.json      # Test result with file paths
    ├── output.pdf       # Generated PDF
    ├── output.tex       # Generated TeX (for debugging)
    └── thumbnail.png    # PNG of first page
```

### Summary File (`summary.json`)
```json
{
  "request_id": "my-test-001",
  "run_id": "my-test-001_1699123456",
  "run_path": "/workspace/shared/test-runs/my-test-001_1699123456",
  "status": "completed",
  "started_at": "2025-01-15T10:30:00.000Z",
  "completed_at": "2025-01-15T10:30:15.000Z",
  "template": "p2kb-smart-pins.latex",
  "tests": {
    "basic": {
      "result": "✅ PASS",
      "result_file": "basic/result.json",
      "has_pdf": true,
      "has_thumbnail": true,
      "duration_ms": 3500
    }
  },
  "overall_result": "success",
  "pass_count": 1,
  "fail_count": 0,
  "total_duration_ms": 4700
}
```

### Per-Test Result File (`{test-name}/result.json`)
```json
{
  "request_id": "my-test-001_1699123456",
  "test_name": "basic",
  "status": "completed",
  "result": "✅ PASS",
  "started_at": "2025-01-15T10:30:00.000Z",
  "completed_at": "2025-01-15T10:30:03.500Z",
  "duration_ms": 3500,
  "template": "p2kb-smart-pins.latex",
  "input_file": "test-input.md",
  "lua_filters": ["p2kb-sp-code-coloring"],
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
  "error": null
}
```

### Failed Test Result
```json
{
  "test_name": "advanced",
  "status": "completed",
  "result": "❌ FAIL",
  "generated_files": {
    "pdf": { "exists": false },
    "tex": {
      "path": "/workspace/shared/test-runs/.../advanced/output.tex",
      "exists": true
    },
    "thumbnail": { "exists": false }
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

## 🔗 Related Documentation

- **[REMOTE-TESTING-GUIDE.md](REMOTE-TESTING-GUIDE.md)** - Complete testing workflow guide
- **[AI-FORMAT-DECISION-GUIDE.md](AI-FORMAT-DECISION-GUIDE.md)** - Choose between testing and production formats
- **[PRODUCTION-REQUEST-FORMAT.md](PRODUCTION-REQUEST-FORMAT.md)** - Production document generation format

---

## 📝 Quick Examples for Common Tasks

### Just Test Template Compiles
```json
{
  "template": "my-template.latex",
  "tests": [{"name": "basic", "input": "minimal.md"}]
}
```

### Test with Lua Filter
```json
{
  "template": "my-template.latex",
  "tests": [{
    "name": "filtered",
    "input": "content.md",
    "lua_filters": ["div-to-env"]
  }]
}
```

### Test Multiple Scenarios
```json
{
  "template": "my-template.latex",
  "tests": [
    {"name": "test1", "input": "file1.md"},
    {"name": "test2", "input": "file2.md"},
    {"name": "test3", "input": "file3.md"}
  ]
}
```

This specification provides complete documentation for all testing request scenarios and eliminates guesswork in format construction.