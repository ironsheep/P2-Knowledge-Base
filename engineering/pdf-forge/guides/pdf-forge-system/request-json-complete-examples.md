# Request.json Complete Examples - Every Use Case

**Last Updated**: 2025-08-29
**Status**: Verified Working Examples

## 1. Interactive Testing (Automated Daemon)

### Basic Test - Single Document, No Filters
```json
{
  "request_id": "basic-test-001",
  "template": "p2kb-smart-pins.latex",
  "timestamp": "2025-08-29T12:00:00Z",
  "tests": [
    {
      "name": "basic-pdf-generation",
      "document": "test-document.md"
    }
  ]
}
```

### Test with Lua Filters
```json
{
  "request_id": "colored-blocks-test",
  "template": "p2kb-smart-pins.latex",
  "timestamp": "2025-08-29T12:00:00Z",
  "tests": [
    {
      "name": "test-with-colors",
      "document": "test-document.md",
      "lua_filters": ["smart-pins-colored-blocks"]
    }
  ]
}
```

### Multiple Tests in One Request
```json
{
  "request_id": "comparison-test",
  "template": "p2kb-smart-pins.latex",
  "timestamp": "2025-08-29T12:00:00Z",
  "tests": [
    {
      "name": "without-filters",
      "document": "test-document.md"
    },
    {
      "name": "with-color-filters",
      "document": "test-document.md",
      "lua_filters": ["smart-pins-colored-blocks"]
    },
    {
      "name": "with-pagebreak-filter",
      "document": "test-document.md",
      "lua_filters": ["part-chapter-pagebreaks"]
    }
  ],
  "options": {
    "auto_fix_attempt": false,
    "cleanup": true
  }
}
```

### Test with Multiple Filters
```json
{
  "request_id": "multi-filter-test",
  "template": "p2kb-smart-pins.latex",
  "tests": [
    {
      "name": "all-filters-applied",
      "document": "test-document.md",
      "lua_filters": [
        "smart-pins-colored-blocks",
        "part-chapter-pagebreaks"
      ]
    }
  ]
}
```

### Test with Different Templates
```json
{
  "request_id": "template-comparison",
  "tests": [
    {
      "name": "smart-pins-template",
      "template": "p2kb-smart-pins.latex",
      "document": "test-document.md",
      "lua_filters": ["smart-pins-colored-blocks"]
    },
    {
      "name": "desilva-template",
      "template": "p2kb-pasm-desilva.latex",
      "document": "test-document.md",
      "lua_filters": ["desilva-div-to-environment"]
    }
  ]
}
```

## 2. Full Manual PDF Generation

### Smart Pins Complete Manual
```json
{
  "template": "p2kb-smart-pins.latex",
  "documents": [
    {
      "input": "P2-Smart-Pins-Complete-Reference.md",
      "output": "P2-Smart-Pins-Complete-Reference.pdf"
    }
  ],
  "lua_filters": ["smart-pins-colored-blocks"],
  "metadata": {
    "title": "P2 Smart Pins Complete Reference",
    "subtitle": "Specifications and Implementation for All 32 Modes",
    "version": "Version 1.0 - Technical Review Draft",
    "date": "August 2025",
    "generated": "2025-08-29"
  }
}
```

### DeSilva Style PASM2 Manual
```json
{
  "template": "p2kb-pasm-desilva.latex",
  "documents": [
    {
      "input": "P2-PASM-deSilva-Style.md",
      "output": "P2-PASM-deSilva-Style.pdf"
    }
  ],
  "lua_filters": ["desilva-div-to-environment"],
  "metadata": {
    "title": "PASM2 Reference Manual",
    "subtitle": "De Silva Style Format",
    "version": "Version 1.0",
    "date": "August 2025"
  }
}
```

### Multiple Documents Combined (Future Feature)
```json
{
  "template": "p2kb-foundation.latex",
  "documents": [
    {
      "input": "part1-introduction.md",
      "output": "combined-manual.pdf"
    },
    {
      "input": "part2-instructions.md",
      "output": "combined-manual.pdf"
    },
    {
      "input": "part3-reference.md",
      "output": "combined-manual.pdf"
    }
  ],
  "lua_filters": ["smart-pins-colored-blocks"],
  "metadata": {
    "title": "P2 Complete Reference",
    "subtitle": "All Documentation Combined",
    "version": "Version 1.0"
  }
}
```

### Manual with Custom Options
```json
{
  "template": "p2kb-smart-pins.latex",
  "documents": [
    {
      "input": "P2-Smart-Pins-Complete-Reference.md",
      "output": "P2-Smart-Pins-Draft.pdf"
    }
  ],
  "lua_filters": ["smart-pins-colored-blocks"],
  "pandoc_options": {
    "toc": true,
    "toc-depth": 3,
    "number-sections": true
  },
  "metadata": {
    "title": "P2 Smart Pins Complete Reference",
    "subtitle": "DRAFT - Internal Review Only",
    "version": "Draft v0.9",
    "date": "August 2025",
    "draft": true,
    "watermark": "DRAFT"
  }
}
```

## 3. Key Format Rules (NEVER FORGET)

### ✅ ALWAYS Arrays
- `documents` - Array of objects (even for one document)
- `lua_filters` - Array of strings (even for one filter)
- `tests` - Array of test objects (for interactive testing)

### ✅ Document Objects Structure
```json
"documents": [
  {
    "input": "filename.md",   // REQUIRED
    "output": "filename.pdf"  // REQUIRED
  }
]
```

### ✅ Test Objects Structure
```json
"tests": [
  {
    "name": "test-name",           // REQUIRED
    "document": "filename.md",     // REQUIRED
    "template": "override.latex",  // Optional - overrides top-level
    "lua_filters": ["filter-name"] // Optional - array of filter names
  }
]
```

### ❌ Common Mistakes
```json
// WRONG - singular document
"document": "file.md"

// WRONG - documents as array of strings
"documents": ["file.md"]

// WRONG - missing input/output fields
"documents": [{"name": "file.md"}]

// WRONG - pandoc_args instead of lua_filters
"pandoc_args": ["--lua-filter=name"]

// WRONG - filter with path or extension
"lua_filters": ["filters/filter.lua"]
```

## 4. Quick Reference Decision Tree

```
Is this for automated testing?
├─ YES → Use "tests" array format
│   ├─ Need filters? → Add "lua_filters" array to each test
│   └─ Multiple tests? → Add multiple objects to tests array
│
└─ NO → Full manual generation
    ├─ Use "documents" array with input/output objects
    ├─ Need filters? → Add top-level "lua_filters" array
    └─ Need metadata? → Add "metadata" object
```

## 5. Validation Checklist

Before submitting any request.json:

- [ ] Using correct top-level structure (tests vs documents)?
- [ ] Arrays used for all multi-value fields?
- [ ] Document objects have both `input` and `output` fields?
- [ ] Filter names have no paths or extensions?
- [ ] Template name includes .latex extension?
- [ ] Request ID or timestamp included (for testing)?
- [ ] Metadata complete (for manual generation)?

---

**Remember**: When in doubt, check this document. Every failure taught us these formats!