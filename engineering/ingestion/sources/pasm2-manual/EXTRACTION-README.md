# PASM2 Instruction Decoding Table Extraction

## Overview

This folder contains tools and extracted data for the instruction decoding tables from the PASM2 Assembly Language Manual. These tables contain critical encoding information that was missing from the initial extraction.

## What Was Extracted

**Table Structure:**
Each instruction decoding table has 5 columns:
1. **COND INSTR FX DEST SRC** - Instruction encoding (binary/hex patterns)
2. **Write** - What register/location is written
3. **C Flag** - Carry flag behavior
4. **Z Flag** - Zero flag behavior  
5. **Clocks** - Clock cycle count

**Extraction Results:**
- **161 tables** extracted (one per instruction with encoding info)
- **260 total rows** across all tables
- **52 tables with footnotes** (important implementation notes)
- **72 multi-line rows** (encoding + flags split across 2 lines)

## Files

### Source Files
- `pasm2-manual-narrative.txt` - pdftotext output from PDF (source data)
- `image-examples/` - Screenshot examples of table formatting

### Extraction Tools
- `extract-instruction-tables.py` - Python script that extracts all tables
- Run: `python3 extract-instruction-tables.py`

### Output Files
- `extracted-instruction-tables.json` - Complete extracted data (JSON format)
- `extraction-summary.txt` - Quick reference summary of all tables

## Data Format

### JSON Structure

```json
{
  "line_number": 1796,
  "instruction": "AKPIN",
  "instruction_line": "AKPIN {#}Src",
  "header": "COND INSTR FX DEST SRC | Write | C Flag | Z Flag | Clocks",
  "rows": [
    {
      "line": " EEEE 1100000 01I 000000001 SSSSSSSSS    Ack Bus    —    —    2",
      "continuation": "                                               —    —    2",
      "parsed": {
        "encoding": "EEEE 1100000 01I 000000001 SSSSSSSSS",
        "write": "Ack Bus",
        "c_flag": "—",
        "z_flag": "—",
        "clocks": "2"
      }
    }
  ],
  "footnotes": [
    {
      "number": "1",
      "text": "Dest is post-adjusted by the auto-indexer value..."
    }
  ]
}
```

### Row Structure

**Single-line row:**
```
EEEE 1100000 01I 000000001 SSSSSSSSS    Ack Bus    —    —    2
```

**Multi-line row** (encoding + continuation):
```
Line:         EEEE 1001100 01I DDDDDDDDD SSSSSSSSS             D¹
Continuation:                                            —      —      2
```

### Footnotes

Footnotes appear after table rows:
```
1
    Dest is post-adjusted by the auto-indexer value; the sign-extended Src[17:9]. 
    In syntax 2, the auto-indexer value is 0.
```

## Key Patterns

### Pattern 1: Simple Instructions
- 1 row, no footnotes
- Example: **AKPIN** - Single encoding, straightforward flags

### Pattern 2: Multiple Syntax Forms
- 2+ rows, often with footnotes
- Example: **ALTB** - Two syntax variants with different encodings
- Example: **ALTD** - Two rows, both multi-line

### Pattern 3: Complex Instructions
- Multiple rows with continuation lines
- Footnotes explaining special behavior
- Example: **JNSE4** - 8 rows, 8 multi-line

## Column Parsing Challenges

The `parsed` field attempts automatic column extraction, but **may not be 100% accurate** due to:

1. **Variable spacing** - Columns aren't consistently aligned
2. **Superscript markers** - Footnote numbers (D¹) embedded in Write column
3. **Multi-line splits** - Encoding on line 1, flags on line 2
4. **Dash variations** - Different dash characters used (—, -, –)

**Recommendation:** Use the raw `line` and `continuation` fields for reliable data, and treat `parsed` as a convenience approximation.

## Usage Examples

### Find an instruction's encoding table:

```python
import json

with open('extracted-instruction-tables.json', 'r') as f:
    tables = json.load(f)

# Find AKPIN
akpin = [t for t in tables if t['instruction'] == 'AKPIN'][0]
print(f"AKPIN has {len(akpin['rows'])} row(s)")
for row in akpin['rows']:
    print(row['line'])
```

### Find all instructions with footnotes:

```python
with_footnotes = [t for t in tables if t['footnotes']]
print(f"{len(with_footnotes)} instructions have footnotes")
for t in with_footnotes:
    print(f"{t['instruction']}: {len(t['footnotes'])} footnote(s)")
```

### Find all multi-row instructions:

```python
multi_row = [t for t in tables if len(t['rows']) > 1]
print(f"{len(multi_row)} instructions have multiple encoding rows")
```

## Next Steps

To integrate this data into the YAML knowledge base:

1. **Review** `extracted-instruction-tables.json` for accuracy
2. **Map** instruction names to existing YAML files in `/data/pasm2/instructions/`
3. **Add fields** to YAML:
   ```yaml
   encoding:
     - pattern: "EEEE 1100000 01I 000000001 SSSSSSSSS"
       write: "Ack Bus"
       c_flag: "—"
       z_flag: "—"
       clocks: 2
   ```
4. **Include footnotes** as `encoding_notes` or similar field
5. **Validate** against actual instruction behavior

## Verification

To verify extraction quality, compare against the original PDF screenshots in `image-examples/`:

- `Screenshot 2025-10-16 at 16.20.46.png` - AKPIN (1 row)
- `Screenshot 2025-10-16 at 16.21.10.png` - ALTB (2 rows + footnote)
- `Screenshot 2025-10-16 at 16.21.24.png` - ALTD (2 rows + footnote)

All three examples are correctly extracted in `extracted-instruction-tables.json`.

## Known Issues

1. **Column parsing** - The automatic column splitting is approximate
2. **Superscripts** - Footnote markers (¹, ², etc.) are captured as plain text
3. **Dash characters** - Multiple dash representations (em dash, minus, etc.)
4. **Encoding patterns** - Binary/hex patterns need further parsing for programmatic use

These are acceptable for manual review and integration, but would need refinement for fully automated processing.
