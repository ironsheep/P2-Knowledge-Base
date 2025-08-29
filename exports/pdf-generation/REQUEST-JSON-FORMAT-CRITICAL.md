# 🔴 CRITICAL: request.json Format Rules

**LESSON LEARNED**: Multiple failures due to incorrect JSON format. ALWAYS use arrays!

## MANDATORY FORMAT RULES

### ✅ CORRECT request.json Format
```json
{
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

**🔴 CRITICAL: Template goes INSIDE each document object!**
- Each document can have its own template
- No top-level template field (ignored if present)
- Falls back to 'admin-manual' if not specified

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

## Complete Working Examples

### Smart Pins Manual Generation
```json
{
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

### DeSilva PASM2 Manual Generation
```json
{
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

## VERIFICATION CHECKLIST
Before deploying to PDF Forge:
- [ ] Uses `"documents"` (plural) key?
- [ ] Documents value is an array `[]`?
- [ ] Uses `"lua_filters"` (not pandoc_args)?
- [ ] Filters value is an array `[]`?
- [ ] Filter names have no path or extension?

**REMEMBER**: Arrays for everything, even single items!

---
Created: 2025-08-29
Reason: Too many failures from wrong JSON format