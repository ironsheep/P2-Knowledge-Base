# PASM2 Instruction Database Version Comparison

**Analysis Date**: 2025-09-13  
**Comparison**: Old vs New PNUT-TS instruction database versions

## File Statistics

| Metric | Old Version | New Version | Delta |
|--------|-------------|-------------|-------|
| **File Size** | 297,225 bytes | 302,895 bytes | +5,670 bytes |
| **Line Count** | 12,254 lines | 12,508 lines | +254 lines |
| **Instructions** | 359 | 359 | No change |
| **Effects Arrays** | 718 | 718 | No change |
| **BitPattern Fields** | 0 | 4 | +4 fields |

## Key Findings

### 🚨 CRITICAL: WC/WZ Value Reversal Detected

**New Database Contains Alternate WC/WZ Assignment:**

| Flag | New DB Value | New DB BitPattern | Our Current Value | Our Current BitPattern |
|------|--------------|-------------------|-------------------|------------------------|
| **WC** | 2 | "0010" | 1 | "01" |
| **WZ** | 1 | "0001" | 2 | "10" |
| **WCZ** | 3 | "0011" | 3 | "11" |

### Metadata Enhancements

**New Version Added:**
```json
"lastUpdated": "2025-09-13T06:48:56.555Z",
"totalConditionCodes": 16,
"totalEffectFlags": 4
```

**Old Version Had:**
```json
// Only totalInstructions: 359
```

### Structural Additions

**New Global Effect Flags Section:**
The new version includes a complete effect flags definition with bit patterns:

```json
"effectFlags": [
  {
    "name": "none",
    "symbol": "",
    "value": 0,
    "description": "No effect flags - instruction does not modify flags",
    "bitPattern": "0000"
  },
  {
    "name": "wz",
    "symbol": "WZ", 
    "value": 1,
    "description": "Write Zero flag - update Z flag based on result",
    "bitPattern": "0001"
  },
  {
    "name": "wc",
    "symbol": "WC",
    "value": 2, 
    "description": "Write Carry flag - update C flag based on result",
    "bitPattern": "0010"
  },
  {
    "name": "wcz",
    "symbol": "WCZ",
    "value": 3,
    "description": "Write Carry and Zero flags - update both C and Z flags", 
    "bitPattern": "0011"
  }
]
```

## Impact Assessment

### 🔴 CONFLICT ALERT: This Contradicts Our Integration

**What We've Done:**
- Enhanced 4 YAML files with WC=1, WZ=2 pattern (from condition codes file)
- Created comprehensive integration report based on these values
- Marked condition codes integration as COMPLETED

**What New Database Shows:**
- WC=2, WZ=1 pattern (opposite assignment)
- Same conflict we resolved earlier, but now in primary instruction database

### Data Lineage Conflict

1. **First Integration**: Used instruction database with WC=1, WZ=2
2. **Condition Codes File (Original)**: Had WC=2, WZ=1 (we got corrected version)
3. **New Instruction Database**: Has WC=2, WZ=1 (matches original condition codes)

**QUESTION**: Which source is authoritative?

## Technical Implications

### If New Database is Correct (WC=2, WZ=1):
- Our 4 enhanced YAML files have incorrect bit patterns
- Our condition codes integration used wrong values  
- Need to reverse WC/WZ assignments in enhanced files

### If Our Current Values are Correct (WC=1, WZ=2):
- New database has error that needs correction
- Our integration stands as completed
- User provided correct condition codes file override

## Recommendations

### 🚨 IMMEDIATE ACTION REQUIRED

1. **PAUSE Integration**: Do not apply new database until WC/WZ conflict resolved
2. **User Consultation**: Confirm which WC/WZ assignment is authoritative
3. **Compiler Validation**: Test both assignments against actual PNUT-TS compiler
4. **Rollback Preparation**: Ready to reverse our bit patterns if needed

### Investigation Questions

1. **Which file reflects actual compiler behavior?**
2. **Was the "corrected" condition codes file actually incorrect?**
3. **Should we trust instruction database over condition codes file?**
4. **Has compiler changed WC/WZ assignment between versions?**

## Integration Strategy Options

### Option A: New Database is Authoritative
- Reverse our WC/WZ bit patterns in 4 YAML files
- Update integration report to reflect WC=2, WZ=1
- Mark previous integration as corrected

### Option B: Current Values are Authoritative  
- Document discrepancy in new database
- Maintain our current WC=1, WZ=2 assignments
- Request updated database from PNUT-TS team

### Option C: Dual Validation
- Test both assignments against live compiler
- Use empirical evidence to determine correct values
- Update knowledge base based on actual behavior

## Conclusion

**Status**: ⚠️ INTEGRATION BLOCKED pending WC/WZ resolution

The new database contains valuable metadata enhancements but introduces a critical conflict with our completed integration work. Resolution required before proceeding.

**Next Step**: User decision on authoritative WC/WZ assignment.