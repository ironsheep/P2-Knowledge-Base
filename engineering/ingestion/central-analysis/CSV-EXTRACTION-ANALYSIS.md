# CSV Instruction File Extraction Analysis

## File Overview
- **File**: P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv
- **Total Lines**: 514 (including header)
- **Instructions**: 491 entries (including aliases and MODCZ operands)
- **Source Authority**: Official Parallax instruction reference

## Column Structure Analysis

### Identified Columns (from header and data):
1. **Order** - Row number (1-491)
2. **Assembly Syntax** - Complete instruction format with operands
3. **Group** - Instruction category (Math and Logic, Branch, Hub Memory, etc.)
4. **Encoding** - Complete 32-bit instruction encoding
5. **Alias** - Marks instruction aliases/variants
6. **Description** - Detailed operation description
7. **Interrupt Shield** - Next instruction shielded from interrupt
8. **COG/LUT Timing** - Clock cycles for COG/LUT execution
9. **Hub Timing** - Clock cycles for Hub execution  
10. **Write Location** - Where result is written (D, S, etc.)
11. **Additional Notes** - Special conditions, flags affected

## What We've Extracted So Far

### Successfully Captured:
1. ✅ Sample instructions (ADD, SUB, ROR, ROL, etc.)
2. ✅ Encoding format understanding
3. ✅ Timing columns identified (H & I)
4. ✅ GETPTR instruction found (row 328)
5. ✅ MODCZ operands (rows 472-491)

### Not Yet Fully Extracted:
1. ❌ Complete instruction set (all 491 entries)
2. ❌ All timing data systematically
3. ❌ All flag effects (C/Z modifications)
4. ❌ Interrupt shielding information
5. ❌ Complete alias mappings

## Critical Data Available in CSV

### 1. Complete Instruction Encodings
Every instruction has its 32-bit encoding:
- Example: `EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS` (ADD)
- Critical for: Assemblers, disassemblers, emulators

### 2. Timing Information (Two Columns!)
- **Column H**: COG/LUT execution cycles
- **Column I**: Hub execution cycles
- Examples: "2" for simple ops, "9-16" for hub reads
- Critical for: Performance optimization, timing analysis

### 3. Flag Effects
Description column specifies:
- C flag behavior
- Z flag behavior  
- Example: "C = carry of (D + S)"

### 4. Instruction Groupings
Groups include:
- Math and Logic
- Branch
- Hub Memory
- Smart Pins
- Hub FIFO
- Events
- Interrupts
- Miscellaneous

### 5. Special Cases
- Alias instructions marked
- MODCZ operands (rows 472-491)
- Condition codes
- Special addressing modes

## What We Should Extract

### Priority 1 - Core Instruction Data
```csv
Order, Instruction, Group, Encoding, Description, COG_Timing, Hub_Timing
```
This gives us the essential instruction reference.

### Priority 2 - Flag and Interrupt Data
```csv
Instruction, C_Flag_Effect, Z_Flag_Effect, Interrupt_Shield
```
Critical for accurate emulation and programming.

### Priority 3 - Aliases and Variants
```csv
Primary_Instruction, Alias_Name, Alias_Type
```
Helps understand instruction relationships.

### Priority 4 - Detailed Behavioral Data
- PTR expression encodings
- Condition code mappings
- Special operand formats

## Extraction Strategy

### Systematic Approach:
1. **Parse all 491 rows** into structured format
2. **Group by instruction category** for analysis
3. **Extract timing ranges** (parse "9-16" format)
4. **Map aliases** to primary instructions
5. **Document flag effects** from descriptions

### Key Patterns to Parse:
- Timing: "2", "2*", "9-16", "same"
- Flags: "C = ...", "Z = ...", "WC/WZ/WCZ"
- Groups: Categorize for reference
- Encodings: Validate against Silicon Doc

## Value of Complete Extraction

### Would Provide:
1. **100% instruction encoding coverage**
2. **Complete timing specifications**
3. **All flag behaviors documented**
4. **Authoritative instruction reference**
5. **Alias/variant mappings**

### Current Coverage:
- Estimated 30-40% of CSV data extracted
- Key instructions sampled but not systematic
- Timing understanding partial
- Flag effects incomplete

## Recommended Actions

### Immediate:
1. **Extract all 491 rows** systematically
2. **Parse timing columns** completely
3. **Map all encodings** to instruction names
4. **Document all flag effects**

### Analysis Needed:
1. Compare encodings with Silicon Doc
2. Verify timing against hardware tests
3. Check aliases against compiler sources
4. Validate special cases

### Documentation Output:
1. Complete instruction reference table
2. Timing specification matrix
3. Flag effect reference
4. Encoding validation report

## Questions for User

1. **Should we extract all 491 rows now?** (High value)
2. **Any specific instruction groups to prioritize?**
3. **Need help parsing specific column formats?**
4. **Want timing data in specific format?**

## Conclusion

The CSV contains **authoritative instruction data** we haven't fully captured. Complete extraction would provide:
- Definitive encodings for all instructions
- Complete timing specifications
- Flag behavior documentation
- Authoritative instruction reference

This would increase our instruction coverage from ~68% to potentially **95%+**.