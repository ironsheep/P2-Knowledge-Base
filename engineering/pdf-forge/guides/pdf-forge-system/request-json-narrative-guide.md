# Understanding request.json: A Complete Narrative Guide

**Created**: 2025-08-29
**Purpose**: Explain the WHY and HOW of request.json structure, not just examples

## The Core Concept: Document-Centric Design

The PDF Forge system is designed around a fundamental principle: **each document is an independent unit of work**. This isn't just a technical detail - it's a philosophical design choice that enables powerful workflows.

## Why Documents Are Objects, Not Strings

When you see this structure:
```json
"documents": [
  {
    "input": "manual.md",
    "output": "manual.pdf",
    "template": "p2kb-smart-pins"  // No .latex extension!
  }
]
```

Each document is an **object** because it carries its own complete context. Think of it like a work order in a print shop - each job has its own specifications, not shared specifications for all jobs.

### The Template Per Document Philosophy

**Why is template inside each document object?**

Consider this real-world scenario: You're generating a technical manual that combines three parts:
1. A cover page using a fancy marketing template
2. Technical content using a reference template
3. Appendices using a simplified template

```json
"documents": [
  {
    "input": "cover.md",
    "template": "marketing-template",
    "output": "final-manual.pdf"
  },
  {
    "input": "technical-content.md",
    "template": "reference-template",
    "output": "final-manual.pdf"  // Same output = append
  },
  {
    "input": "appendices.md",
    "template": "simple-template",
    "output": "final-manual.pdf"  // Same output = append
  }
]
```

The system was designed to handle this complexity. Each document knows its own template requirements.

## The Fallback Mechanism

If you don't specify a template, the system defaults to `admin-manual`. This isn't random - it's a safety net:

```javascript
doc.template || 'admin-manual'
```

This means: "Use the document's specified template, OR if none specified, use admin-manual as a safe default."

**Why admin-manual?** It's the most generic, least likely to fail template. Better to get SOME output than an error.

## Arrays Everywhere: Future-Proofing

### Why Documents Must Be an Array

Even for a single document:
```json
"documents": [{"input": "one-file.md", ...}]  // Still an array!
```

**Reason**: Consistency in parsing. The code doesn't need to check "is this one document or many?" It always loops through an array, even if that array has one item.

### Why Lua Filters Must Be an Array

```json
"lua_filters": ["single-filter"]  // Still an array!
```

**Reason**: Filters are applied in sequence. Even one filter is a sequence of one. The system applies them in order:
```javascript
for (filter of lua_filters) {
  applyFilter(filter);
}
```

## The Input/Output Paradigm

### Why Separate Input and Output Fields?

```json
{
  "input": "source.md",
  "output": "result.pdf"
}
```

**Not** just:
```json
{
  "document": "source.md"  // Where does output go?
}
```

**Reasoning**:
1. **Explicit naming control** - You decide the output filename
2. **Multiple inputs, single output** - Same output name = concatenation
3. **Batch processing** - Clear what goes where in bulk operations

## Metadata: Document vs System Level

```json
{
  "documents": [...],
  "metadata": {
    "title": "System Level",
    "date": "2025"
  }
}
```

**Metadata** sits at the root because it applies to the entire generation session, not individual documents. It's like the cover sheet on a print job - general information about the whole batch.

## The Complete Mental Model

Think of request.json as a **print shop work order**:

1. **Documents Array** = List of individual print jobs
2. **Each Document Object** = Complete specifications for that job
   - `input`: The source material
   - `output`: What to name the result
   - `template`: Which printing press (template) to use
   - `lua_filters`: Special processing instructions
3. **Root Level Settings** = Batch-wide settings
   - `metadata`: Information about the whole batch
   - `lua_filters`: Filters that apply to ALL documents

## Common Misconceptions Explained

### "Why can't template be at the root level?"

You CAN have shared settings by using the same template in each document. But the system needs to know PER DOCUMENT which template to use. It's checking `doc.template` not `request.template`.

### "Why do I need arrays for single items?"

Because the code processes arrays. It doesn't check "is this one or many?" It just processes what it gets. An array of one is still an array.

### "Why does it default to admin-manual?"

Because something is better than nothing. If template specification fails, at least try with a generic template rather than crash completely.

## The Generation Flow

1. **Parse request.json** → Validate structure
2. **For each document in documents array**:
   - Read `doc.input` from inbox/
   - Apply `doc.template` (or default to admin-manual)
   - Apply `doc.lua_filters` in sequence
   - Generate `doc.output` in output/
3. **Apply root-level settings** to all documents
4. **Report results** for the batch

## Debugging Your Request

When something goes wrong, check in this order:

1. **Is documents an array?** Even for one document?
2. **Does each document have input, output, and template?**
3. **Are lua_filters arrays?** Even for one filter?
4. **Are filter names bare?** (no paths, no .lua extension)
5. **Is the template name bare?** (NO .latex extension, just like filters!)

## The Future-Proof Structure

This design allows for future enhancements:
- Different templates per document ✓
- Multiple inputs to single output (concatenation)
- Per-document variables and settings
- Conditional processing based on document type
- Parallel processing of independent documents

The structure seems complex for simple cases, but it enables powerful workflows without breaking changes.

---

**Remember**: Every field has a reason. Every array has a purpose. Every object structure enables a workflow. This isn't over-engineering - it's thoughtful design for real-world document generation needs.