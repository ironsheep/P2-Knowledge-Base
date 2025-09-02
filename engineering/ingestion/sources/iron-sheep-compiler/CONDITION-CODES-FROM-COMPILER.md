# P2 Condition Codes - From TypeScript Compiler Source

**Source**: Stephen M Moraco, Iron Sheep Productions, LLC  
**Authority**: P2 TypeScript Compiler Implementation (pnut_ts)  
**Date**: 2025-09-02  
**Trust Level**: 🟢 PRIMARY - Compiler source code

---

## Complete EEEE Condition Codes Table with Aliases

The 4-bit EEEE field in P2 instructions specifies conditional execution. Here are all 16 values with their aliases:

| EEEE | Hex  | Primary Name | Aliases | Logic | Comparison Meaning |
|------|------|-------------|---------|-------|--------------------|
| 0000 | 0x00 | if_ret | if_return | (return) | Execute on return (P1: if_never) |
| 0001 | 0x01 | if_nc_and_nz | if_nz_and_nc, **if_a**, **if_gt** | !C AND !Z | Unsigned above / Signed greater than |
| 0010 | 0x02 | if_nc_and_z | if_z_and_nc | !C AND Z | Not carry AND zero |
| 0011 | 0x03 | if_nc | **if_ae**, **if_ge** | !C | Unsigned above/equal / Signed greater/equal |
| 0100 | 0x04 | if_c_and_nz | if_nz_and_c | C AND !Z | Carry AND not zero |
| 0101 | 0x05 | if_nz | **if_ne** | !Z | Not equal |
| 0110 | 0x06 | if_c_ne_z | if_z_ne_c | C ≠ Z | Carry not equal to zero |
| 0111 | 0x07 | if_nc_or_nz | if_nz_or_nc | !C OR !Z | Not carry OR not zero |
| 1000 | 0x08 | if_c_and_z | if_z_and_c | C AND Z | Carry AND zero |
| 1001 | 0x09 | if_c_eq_z | if_z_eq_c | C = Z | Carry equals zero |
| 1010 | 0x0A | if_z | **if_e** | Z | Equal (zero flag set) |
| 1011 | 0x0B | if_nc_or_z | if_z_or_nc | !C OR Z | Not carry OR zero |
| 1100 | 0x0C | if_c | **if_b**, **if_lt** | C | Unsigned below / Signed less than |
| 1101 | 0x0D | if_c_or_nz | if_nz_or_c | C OR !Z | Carry OR not zero |
| 1110 | 0x0E | if_c_or_z | if_z_or_c, **if_be**, **if_le** | C OR Z | Unsigned below/equal / Signed less/equal |
| 1111 | 0x0F | if_always | (none) | 1 | Always execute (unconditional) |

---

## TypeScript Source Code (as provided)

### Primary Condition Code Values
```typescript
// From pnut_ts compiler source - primary values
if_ret = 0,          // 0x00  (also, if_return) (P1 was if_never)
if_nc_and_nz = 1,    // 0x01
if_nc_and_z = 2,     // 0x02
if_nc = 3,           // 0x03
if_c_and_nz = 4,     // 0x04
if_nz = 5,           // 0x05
if_c_ne_z = 6,       // 0x06
if_nc_or_nz = 7,     // 0x07
if_c_and_z = 8,      // 0x08
if_c_eq_z = 9,       // 0x09
if_z = 10,           // 0x0a
if_nc_or_z = 11,     // 0x0b
if_c = 12,           // 0x0c
if_c_or_nz = 13,     // 0x0d
if_c_or_z = 14,      // 0x0e
if_always = 15,      // 0x0f
```

### Complete Alias List from Compiler
```typescript
// From pnut_ts compiler source - all condition aliases
IF_NC_AND_NZ = 'IF_NC_AND_NZ',  // 0x01 - primary form
IF_NZ_AND_NC = 'IF_NZ_AND_NC',  // 0x01 - commutative alias
IF_GT = 'IF_GT',                // 0x01 - signed greater than
IF_A = 'IF_A',                  // 0x01 - unsigned above

IF_NC_AND_Z = 'IF_NC_AND_Z',    // 0x02 - primary form
IF_Z_AND_NC = 'IF_Z_AND_NC',    // 0x02 - commutative alias

IF_NC = 'IF_NC',                // 0x03 - primary form
IF_GE = 'IF_GE',                // 0x03 - signed greater or equal
IF_AE = 'IF_AE',                // 0x03 - unsigned above or equal

IF_C_AND_NZ = 'IF_C_AND_NZ',    // 0x04 - primary form
IF_NZ_AND_C = 'IF_NZ_AND_C',    // 0x04 - commutative alias

IF_NZ = 'IF_NZ',                // 0x05 - primary form
IF_NE = 'IF_NE',                // 0x05 - not equal

IF_C_NE_Z = 'IF_C_NE_Z',        // 0x06 - primary form
IF_Z_NE_C = 'IF_Z_NE_C',        // 0x06 - commutative alias

IF_NC_OR_NZ = 'IF_NC_OR_NZ',    // 0x07 - primary form
IF_NZ_OR_NC = 'IF_NZ_OR_NC',    // 0x07 - commutative alias

IF_C_AND_Z = 'IF_C_AND_Z',      // 0x08 - primary form
IF_Z_AND_C = 'IF_Z_AND_C',      // 0x08 - commutative alias

IF_C_EQ_Z = 'IF_C_EQ_Z',        // 0x09 - primary form
IF_Z_EQ_C = 'IF_Z_EQ_C',        // 0x09 - commutative alias

IF_Z = 'IF_Z',                  // 0x0A - primary form
IF_E = 'IF_E',                  // 0x0A - equal

IF_NC_OR_Z = 'IF_NC_OR_Z',      // 0x0B - primary form
IF_Z_OR_NC = 'IF_Z_OR_NC',      // 0x0B - commutative alias

IF_C = 'IF_C',                  // 0x0C - primary form
IF_LT = 'IF_LT',                // 0x0C - signed less than
IF_B = 'IF_B',                  // 0x0C - unsigned below

IF_C_OR_NZ = 'IF_C_OR_NZ',      // 0x0D - primary form
IF_NZ_OR_C = 'IF_NZ_OR_C',      // 0x0D - commutative alias

IF_C_OR_Z = 'IF_C_OR_Z',        // 0x0E - primary form
IF_Z_OR_C = 'IF_Z_OR_C',        // 0x0E - commutative alias
IF_LE = 'IF_LE',                // 0x0E - signed less or equal
IF_BE = 'IF_BE',                // 0x0E - unsigned below or equal

IF_ALWAYS = 'IF_ALWAYS',        // 0x0F - always execute

// Special pattern aliases for flag testing
IF_00 = 'IF_00',                // Test for C=0, Z=0
IF_01 = 'IF_01',                // Test for C=0, Z=1
IF_10 = 'IF_10',                // Test for C=1, Z=0
IF_11 = 'IF_11',                // Test for C=1, Z=1
IF_X0 = 'IF_X0',                // Test for Z=0 (any C)
IF_X1 = 'IF_X1',                // Test for Z=1 (any C)
IF_0X = 'IF_0X',                // Test for C=0 (any Z)
IF_1X = 'IF_1X',                // Test for C=1 (any Z)
IF_NOT_00 = 'IF_NOT_00',        // Test for NOT(C=0, Z=0)
IF_NOT_01 = 'IF_NOT_01',        // Test for NOT(C=0, Z=1)
IF_NOT_10 = 'IF_NOT_10',        // Test for NOT(C=1, Z=0)
IF_NOT_11 = 'IF_NOT_11',        // Test for NOT(C=1, Z=1)
IF_SAME = 'IF_SAME',            // Test for C=Z
IF_DIFF = 'IF_DIFF',            // Test for C≠Z

// Direct binary pattern aliases
IF_0000 = 'IF_0000',            // 0x00 - if_ret
IF_0001 = 'IF_0001',            // 0x01 - if_nc_and_nz
IF_0010 = 'IF_0010',            // 0x02 - if_nc_and_z
IF_0011 = 'IF_0011',            // 0x03 - if_nc
IF_0100 = 'IF_0100',            // 0x04 - if_c_and_nz
IF_0101 = 'IF_0101',            // 0x05 - if_nz
IF_0110 = 'IF_0110',            // 0x06 - if_c_ne_z
IF_0111 = 'IF_0111',            // 0x07 - if_nc_or_nz
IF_1000 = 'IF_1000',            // 0x08 - if_c_and_z
IF_1001 = 'IF_1001',            // 0x09 - if_c_eq_z
IF_1010 = 'IF_1010',            // 0x0A - if_z
IF_1011 = 'IF_1011',            // 0x0B - if_nc_or_z
IF_1100 = 'IF_1100',            // 0x0C - if_c
IF_1101 = 'IF_1101',            // 0x0D - if_c_or_nz
IF_1110 = 'IF_1110',            // 0x0E - if_c_or_z
IF_1111 = 'IF_1111',            // 0x0F - if_always
```

---

## Alias Categories

### Comparison Aliases
These aliases make comparisons more intuitive:
- **if_e** (if_z, 0x0A) - Equal (Z flag set after CMP)
- **if_ne** (if_nz, 0x05) - Not Equal (Z flag clear)
- **if_a** (if_nc_and_nz, 0x01) - Unsigned Above
- **if_ae** (if_nc, 0x03) - Unsigned Above or Equal
- **if_b** (if_c, 0x0C) - Unsigned Below
- **if_be** (if_c_or_z, 0x0E) - Unsigned Below or Equal
- **if_gt** (if_nc_and_nz, 0x01) - Signed Greater Than
- **if_ge** (if_nc, 0x03) - Signed Greater or Equal
- **if_lt** (if_c, 0x0C) - Signed Less Than
- **if_le** (if_c_or_z, 0x0E) - Signed Less or Equal

### Special Pattern Aliases
These appear to be for special use cases (possibly for paired flag testing):
- **if_00, if_01, if_10, if_11** - Test specific flag combinations
- **if_x0, if_x1** - Test one flag regardless of other
- **if_0x, if_1x** - Test other flag regardless of first
- **if_not_00, if_not_01, if_not_10, if_not_11** - Inverted flag tests
- **if_same** - Flags have same value (C=Z)
- **if_diff** - Flags differ (C≠Z)

### Direct Binary Aliases
- **if_0000** through **if_1111** - Direct 4-bit EEEE values

## Usage Notes

1. **Default Condition**: Most assemblers default to EEEE=1111 (if_always) when no condition is specified
2. **P1 Compatibility**: Note that if_ret (0x00) was if_never in Propeller 1
3. **Common Patterns**:
   - if_z / if_e - Test for equality
   - if_nz / if_ne - Test for inequality
   - if_c / if_b / if_lt - Test for less than
   - if_nc / if_ae / if_ge - Test for greater or equal
4. **Signed vs Unsigned**: Same condition codes, different aliases for clarity
   - Unsigned: if_a, if_ae, if_b, if_be
   - Signed: if_gt, if_ge, if_lt, if_le

---

## Integration with Instruction Encoding

In the standard P2 instruction encoding:
```
EEEE OOOOOOO CZI DDDDDDDDD SSSSSSSSS
^^^^
These 4 bits select from the 16 conditions above
```

---

## Authority Note

This information comes directly from the TypeScript implementation of the P2 compiler (pnut_ts), which must correctly implement these values to generate working P2 machine code. As compiler source code, this represents ground truth for condition code values.

---

*Document created: 2025-09-02*  
*Source: Stephen M Moraco, Iron Sheep Productions, LLC*