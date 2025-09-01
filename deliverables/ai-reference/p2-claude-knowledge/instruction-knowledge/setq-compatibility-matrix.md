# SETQ/SETQ2 Compatibility Matrix

**Purpose**: Documents SETQ vs SETQ2 usage patterns and instruction compatibility.

## SETQ vs SETQ2 Instruction Differences

### SETQ - Standard Queue Setup
```pasm2
SETQ    #count-1            ' Setup for count longs
RDLONG  dest, source        ' Read count longs starting at source
```

### SETQ2 - Extended Queue Setup  
```pasm2
SETQ2   #count-1            ' Setup for count longs (extended mode)
RDLONG  dest, source        ' Read with extended addressing/modes
```

### Key Behavioral Differences
- **SETQ**: Standard block operations, basic addressing
- **SETQ2**: Extended addressing modes, additional features
- **Compatibility**: Not all instructions work with both SETQ variants

## Instruction Compatibility Matrix

### SETQ Compatible Instructions
```pasm2
' Memory Operations
SETQ    #7                  ' Setup for 8 longs
RDLONG  buffer, hub_addr    ' ✅ Compatible
WRLONG  buffer, hub_addr    ' ✅ Compatible
WMLONG  buffer, hub_addr    ' ✅ Compatible

' LUT Operations  
SETQ    #3                  ' Setup for 4 longs
RDLUT   dest, lut_addr      ' ✅ Compatible
WRLUT   source, lut_addr    ' ✅ Compatible
```

### SETQ2 Exclusive Instructions
```pasm2
' Extended addressing modes
SETQ2   #extended_count     ' Setup with extended parameters
RDLONG  dest, source        ' ✅ Extended mode features
' (Specific SETQ2-only instructions TBD via research)
```

### Incompatible Instructions
```pasm2
' Instructions that ignore SETQ/SETQ2
MOV     dest, source        ' ❌ Not affected by SETQ
ADD     dest, source        ' ❌ Not affected by SETQ
JMP     #label              ' ❌ Not affected by SETQ
```

## Usage Pattern Requirements

### Count Parameter Encoding
```pasm2
SETQ    #0                  ' Transfer 1 long (count-1)
SETQ    #1                  ' Transfer 2 longs  
SETQ    #31                 ' Transfer 32 longs (maximum?)
```

### Address Alignment Requirements
- **Long transfers**: Source/destination must be long-aligned
- **Word transfers**: Source/destination must be word-aligned  
- **Byte transfers**: No alignment requirements

### Timing and Performance
- **Setup overhead**: SETQ/SETQ2 instruction cost
- **Transfer efficiency**: Block vs individual operation performance
- **Hub timing**: SETQ operations vs hub access patterns

## Research Gaps - DEMO CRITICAL

### High Priority (Demo Impact)
1. **SETQ vs SETQ2 feature differences** (3 hours)
   - Specific capabilities unique to SETQ2
   - When to use SETQ vs SETQ2
   - Performance implications of each variant

2. **Instruction compatibility enumeration** (4 hours)
   - Complete list of SETQ-compatible instructions
   - Instructions that work with SETQ2 but not SETQ
   - Instructions that ignore SETQ setup entirely

3. **Count limits and encoding** (2 hours)
   - Maximum transfer counts for SETQ/SETQ2
   - Count parameter encoding rules  
   - Edge cases and boundary conditions

### Medium Priority (Development Important)
4. **Performance optimization patterns** (4 hours)
   - When block transfers are more efficient than individual
   - Hub timing optimization with SETQ operations
   - Memory bandwidth utilization techniques

5. **Address alignment impact** (3 hours)
   - Alignment requirements for different transfer types
   - Performance penalties for misaligned access
   - Alignment checking and correction techniques

### Low Priority (Documentation Complete)
6. **Advanced SETQ patterns** (6 hours)
   - Complex block transfer sequences
   - SETQ coordination with other P2 subsystems
   - Edge case handling and error recovery

**Total Research Required**: 22 hours
**Demo Critical Subset**: 9 hours (41% of total)

## Integration Notes

**Cross-References**:
- State Setup Matrix: SETQ/SETQ2 as quintessential setup instructions
- FIFO/Queue Matrix: SETQ relationship to FIFO operations
- Instruction Sequence Matrix: SETQ timing and following instruction coordination

**Documentation Sources Needed**:
- P2 memory subsystem documentation
- SETQ/SETQ2 instruction reference with complete feature lists
- Performance timing documentation for block operations
- Hub access pattern optimization guides