# P2 Instruction Timing Sample Extraction

**Created**: 2025-09-02  
**Source**: P2 Instructions v35 CSV  
**Purpose**: Demonstrate timing extraction for central repository

---

## Sample Instructions with Complete Timing

### ADD - Basic Addition
```
Encoding: EEEE 0001000 CZI DDDDDDDDD SSSSSSSSS
Group: Math and Logic
```

**Timing Table:**
| Mode | 8 COGs | 16 COGs | Notes |
|------|--------|---------|-------|
| COG Exec | 2 | 2 | Base timing |
| LUT Exec | same | same | Same as COG |
| HUB Exec | 2* | 2* | +1 if crosses hub long |

**Operation:**
- Syntax: `ADD D,{#}S {WC/WZ/WCZ}`
- Function: D = D + S
- C Flag: Carry of (D + S)
- Z Flag: Result == 0

---

### ADDX - Add with Carry
```
Encoding: EEEE 0001001 CZI DDDDDDDDD SSSSSSSSS
```

**Timing:** Same as ADD (2 cycles all modes)

**Critical for Extended Precision:**
- Used in 64-bit and 128-bit arithmetic
- Propagates carry through multi-word operations
- Z flag ANDs with previous (cumulative zero detection)

---

### MUL - Unsigned Multiply
```
Encoding: EEEE 1101000 0ZI DDDDDDDDD SSSSSSSSS
```

**Timing Table:**
| Mode | 8 COGs | 16 COGs | Notes |
|------|--------|---------|-------|
| COG Exec | 2 | 2 | Fast hardware multiply |
| LUT Exec | same | same | |
| HUB Exec | 2* | 2* | +1 if crosses hub long |

**Operation:**
- Returns low 32 bits of 64-bit product
- Use GETMULH for high 32 bits

---

### RDLONG - Read Long from Hub
```
Encoding: EEEE 1010110 CZI DDDDDDDDD SSSSSSSSS
```

**Timing Table:**
| Mode | 8 COGs | 16 COGs | Notes |
|------|--------|---------|-------|
| COG Exec | 9..16 | 17..32 | Hub sync required |
| LUT Exec | 9..16 | 17..32 | Hub sync required |
| HUB Exec | 9..16* | 17..32* | +1 if crosses hub long |

**Critical Timing Understanding:**
- Variable timing due to hub synchronization
- 8 COGs: 9-16 cycles depending on hub alignment
- 16 COGs: 17-32 cycles (double the window)
- This is the "egg-beater" hub access pattern

---

### JMP - Unconditional Jump
```
Encoding: EEEE 1101100 00I 000000000 SSSSSSSSS
```

**Timing Table:**
| Mode | 8 COGs | 16 COGs | Notes |
|------|--------|---------|-------|
| COG Exec | 4 | 4 | Pipeline flush |
| LUT Exec | 4 | 4 | Pipeline flush |
| HUB Exec | 13..20* | 13..20* | Hub fetch required |

**Pipeline Impact:**
- 4 cycles in COG/LUT due to pipeline flush
- Much longer in HUB due to instruction fetch

---

## 🔑 Key Timing Insights

### Execution Mode Impact
1. **COG/LUT Execution**: Generally deterministic
2. **HUB Execution**: Variable due to hub window alignment
3. **"*" notation**: Additional cycle if instruction crosses hub long boundary

### Hub Access Pattern ("Egg-beater")
- 8 COGs: Each COG gets 1/8 hub windows
- 16 COGs: Each COG gets 1/16 hub windows
- This explains RDLONG timing: 9..16 (8 COGs) vs 17..32 (16 COGs)

### Pipeline Effects
- Most ALU operations: 2 cycles
- Branches: 4+ cycles (pipeline flush)
- Hub access: 9+ cycles (synchronization)

---

## CSV Column Mapping Discovered

From the CSV structure:
- Column 8: "Clock Cycles (8 cogs) - Cog Exec Mode"
- Column 9: "Clock Cycles (8 cogs) - LUT Exec Mode"  
- Column 10: "Clock Cycles (8 cogs) - Hub Exec Mode"
- Column 11: "Clock Cycles (16 cogs) - Cog Exec Mode"
- Column 12: "Clock Cycles (16 cogs) - LUT Exec Mode"

Values found:
- Numeric (2, 4, etc): Exact cycle count
- "same": Same as previous column
- Range (9..16): Variable timing
- Asterisk (2*): Conditional extra cycle

---

## Next Steps

1. **Parse entire CSV** for all 491 instruction variants
2. **Create timing database** with all execution modes
3. **Cross-reference with Silicon Doc** for detailed explanations
4. **Add Chip's clarifications** for the 13 instructions
5. **Build complete repository** with all sources integrated

---

*This sample demonstrates the timing complexity we need to capture in our central repository*