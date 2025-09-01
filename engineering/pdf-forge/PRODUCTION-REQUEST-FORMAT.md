# Production Request Format Specification
**Document Generation Workflow for `generate-pdf.js`**

## 📋 Quick Reference

**Format Type**: `document_generation`  
**Script**: `generate-pdf.js`  
**Purpose**: Generate final deliverable PDFs for distribution and publication  
**Decision Guide**: See [AI-FORMAT-DECISION-GUIDE.md](AI-FORMAT-DECISION-GUIDE.md)

> **⚠️ Note**: This format is for **production document generation only**. For template testing and validation, use [TESTING-REQUEST-FORMAT.md](TESTING-REQUEST-FORMAT.md)

---

**LESSON LEARNED**: Multiple failures due to incorrect JSON format. ALWAYS use arrays!

## 🎯 Production Format Rules

### ✅ CORRECT Production Request Format
```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "P2-Smart-Pins-Complete-Reference.md",      // REQUIRED field!
      "output": "P2-Smart-Pins-Complete-Reference.pdf",     // REQUIRED field!
      "template": "p2kb-smart-pins"                      // REQUIRED - Per document! (NO .latex extension!)
    }
  ],                                                         // ARRAY of OBJECTS!
  "lua_filters": ["smart-pins-colored-blocks"],            // ARRAY! Even for single filter
  "metadata": {
    "title": "P2 Smart Pins Complete Reference",
    "subtitle": "Specifications and Implementation for All 32 Modes",
    "version": "Version 1.0",
    "date": "August 2025"
  }
}
```

**🔴 CRITICAL PRODUCTION RULES:**
- **format_type**: Always `"document_generation"` (for AI recognition)
- **Template per document**: Each document can have its own template
- **No top-level template**: Top-level template field ignored if present
- **Default fallback**: Falls back to 'admin-manual' if template not specified
- **Production focus**: Creates final deliverable PDFs with specific output names

### ❌ WRONG Formats That Will FAIL
```json
// WRONG - singular "document"
"document": "file.md"                        // ❌ FAILS IMMEDIATELY

// WRONG - string instead of array
"documents": "file.md"                       // ❌ FAILS IMMEDIATELY

// WRONG - pandoc_args instead of lua_filters
"pandoc_args": ["--lua-filter=filter-name"]  // ❌ FILTER NOT FOUND

// WRONG - string filter instead of array
"lua_filters": "filter-name"                 // ❌ FAILS
```

## THE GOLDEN RULES

1. **ALWAYS USE ARRAYS**
   - `"documents": []` - NEVER singular, NEVER string
   - `"lua_filters": []` - NEVER pandoc_args, NEVER string

2. **EVEN FOR SINGLE ITEMS**
   - One document? Still use array: `["document.md"]`
   - One filter? Still use array: `["filter-name"]`
   - No filters? Empty array: `[]` or omit the key

3. **FILTER NAMES ONLY**
   - Just the name: `"smart-pins-colored-blocks"`
   - NO path: NOT `"filters/smart-pins-colored-blocks"`
   - NO extension: NOT `"smart-pins-colored-blocks.lua"`

## 📚 Complete Production Examples

### Smart Pins Production Manual
```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "P2-Smart-Pins-Complete-Reference.md",
      "output": "P2-Smart-Pins-Complete-Reference.pdf",
      "template": "p2kb-smart-pins"        // Template PER DOCUMENT! (bare name, no extension!)
    }
  ],
  "lua_filters": ["smart-pins-colored-blocks"],
  "metadata": {
    "title": "P2 Smart Pins Complete Reference",
    "subtitle": "Specifications and Implementation for All 32 Modes",
    "version": "Version 1.0 - Technical Review Draft",
    "date": "August 2025"
  }
}
```

### DeSilva PASM2 Production Manual
```json
{
  "format_type": "document_generation",
  "documents": [
    {
      "input": "P2-PASM-deSilva-Style.md",
      "output": "P2-PASM-deSilva-Style.pdf",
      "template": "p2kb-pasm-desilva"        // Template PER DOCUMENT! (bare name, no extension!)
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

## ERROR HISTORY (How We Learned)
- 2025-08-26: Failed with `"document"` instead of `"documents"`
- 2025-08-27: Failed with `"pandoc_args"` instead of `"lua_filters"`
- 2025-08-28: Failed with `"document"` AGAIN
- 2025-08-29: Failed with documents as array of strings instead of objects
- 2025-08-29: Finally documented the correct format with input/output fields

## 🔍 Production Verification Checklist
Before deploying to PDF Forge for final deliverable generation:
- [ ] Uses `"format_type": "document_generation"`?
- [ ] Uses `"documents"` (plural) key?
- [ ] Documents value is an array `[]`?
- [ ] Each document has `input`, `output`, and `template` fields?
- [ ] Uses `"lua_filters"` (not pandoc_args)?
- [ ] Filters value is an array `[]`?
- [ ] Filter names have no path or extension?
- [ ] Output filenames are production-ready?

**REMEMBER**: Arrays for everything, even single items!

---

## 🔗 Related Documentation

- **[AI-FORMAT-DECISION-GUIDE.md](AI-FORMAT-DECISION-GUIDE.md)** - Choose between production and testing formats
- **[TESTING-REQUEST-FORMAT.md](TESTING-REQUEST-FORMAT.md)** - Template testing and validation format
- **PDF Forge System Documentation** - Complete system overview

---
Created: 2025-08-29  
Renamed: 2025-09-01 (from REQUEST-JSON-FORMAT-CRITICAL.md)  
Reason: Too many failures from wrong JSON format, clarified production scope