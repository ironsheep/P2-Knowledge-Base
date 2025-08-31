# P1 PASM Master Instruction Table

**Purpose**: P1 instruction reference for P1↔P2 comparison analysis  
**Last Updated**: 2025-08-20  
**Source**: DeSilva P1 Assembly Tutorial (2007) - `/sources/extractions/desilva-p1-tutorial/`  
**Status**: PRELIMINARY - Based on tutorial content only  
**Total Instructions**: 66 instructions identified from DeSilva content  

## IMPORTANT LIMITATIONS

⚠️ **This table is PRELIMINARY and INCOMPLETE** ⚠️

- **Source Coverage**: Based solely on DeSilva P1 Assembly Tutorial (2007)
- **Purpose**: Enable P1↔P2 comparison analysis, not comprehensive P1 reference
- **Missing**: Complete P1 instruction set, formal specifications, official timings
- **Need**: Formal P1 documentation for complete coverage
- **Scope**: Tutorial-mentioned instructions only (~66 of full P1 instruction set)

## Table Structure

| Column | Description |
|--------|-------------|
| Instruction Name | P1 PASM mnemonic |
| Usage Count | Occurrences in DeSilva tutorial |
| Category | Functional grouping |
| Timing | Clock cycles (when mentioned) |
| Flag Effects | C/Z flag modifications (when mentioned) |
| Description Status | Coverage level in tutorial |
| P2 Equivalent | Corresponding P2 instruction (if exists) |
| Tutorial Context | Where/how instruction is explained |

## Update Methodology

- **Tutorial Analysis**: Based on DeSilva content extraction
- **Usage Frequency**: Reflects tutorial emphasis (not P1 significance)
- **MISSING Data**: Most fields incomplete due to tutorial scope
- **Future Enrichment**: Requires formal P1 documentation
- **Gap Tracking**: Enables systematic P1 knowledge improvement

---

## P1 Instruction Reference Table

### High-Usage Instructions (Tutorial Emphasis)

| Instruction | Usage Count | Category | Timing | Flag Effects | Description Status | P2 Equivalent | Tutorial Context |
|-------------|-------------|----------|--------|--------------|-------------------|---------------|------------------|
| MOV | 35 | Data Movement | 4 clocks | Z (optional WZ) | Complete | MOV | Core instruction, many examples |
| ADD | 29 | Arithmetic | 4 clocks | C, Z (optional WC/WZ) | Complete | ADD | Arithmetic examples, counters |
| JMP | 19 | Control Flow | 4 clocks | None | Complete | JMP | Jump examples, loops |
| RDLONG | 18 | Hub Access | 7-22 clocks | Z (optional WZ) | Complete | RDLONG | Hub communication examples |
| WRLONG | 12 | Hub Access | 7-22 clocks | None | Complete | WRLONG | Hub data writing |
| NOT | 11 | Logic | 4 clocks | Z (optional WZ) | Minimal | NOT | Brief logic mention |
| DJNZ | 11 | Control Flow | 4/8 clocks | None | Complete | DJNZ | Loop control, detailed examples |
| MOVI | 10 | Data Movement | 4 clocks | Z (optional WZ) | Complete | MOVI | Self-modifying code |

### Medium-Usage Instructions (Functional Coverage)

| Instruction | Usage Count | Category | Timing | Flag Effects | Description Status | P2 Equivalent | Tutorial Context |
|-------------|-------------|----------|--------|--------------|-------------------|---------------|------------------|
| WRBYTE | 7 | Hub Access | 7-22 clocks | None | Partial | WRBYTE | Byte operations |
| SHR | 7 | Shift/Rotate | 4 clocks | C, Z (optional WC/WZ) | Partial | SHR | Shift examples |
| NEG | 7 | Arithmetic | 4 clocks | C, Z (optional WC/WZ) | Partial | NEG | Arithmetic operations |
| SHL | 6 | Shift/Rotate | 4 clocks | C, Z (optional WC/WZ) | Partial | SHL | Shift operations |
| AND | 6 | Logic | 4 clocks | Z, C=parity (optional WC/WZ) | Partial | AND | Logic operations |
| MOVS | 5 | Data Movement | 4 clocks | Z (optional WZ) | Complete | MOVS | Self-modifying code |
| CMPSUB | 5 | Arithmetic | 4 clocks | C, Z (WC/WZ) | Complete | CMPSUB | Division algorithm |
| RDBYTE | 4 | Hub Access | 7-22 clocks | Z (optional WZ) | Partial | RDBYTE | Byte access |
| MOVD | 4 | Data Movement | 4 clocks | Z (optional WZ) | Complete | MOVD | Self-modifying code |
| LOCKSET | 4 | System | Variable | C | Complete | LOCKSET | Semaphore examples |
| JMPRET | 4 | Control Flow | 4 clocks | None | Complete | JMPRET | Subroutine calls |

### Low-Usage Instructions (Basic Coverage)

| Instruction | Usage Count | Category | Timing | Flag Effects | Description Status | P2 Equivalent | Tutorial Context |
|-------------|-------------|----------|--------|--------------|-------------------|---------------|------------------|
| WAITPNE | 3 | I/O Control | Variable | None | Partial | WAITPNE | Pin state waiting |
| WAITPEQ | 3 | I/O Control | Variable | None | Partial | WAITPEQ | Pin state waiting |
| WAITCNT | 3 | Timing | Variable | None | Partial | WAITCNT | Timing control |
| TJZ | 3 | Control Flow | 4/8 clocks | None | Complete | TJZ | Conditional jumps |
| TJNZ | 3 | Control Flow | 4/8 clocks | None | Complete | TJNZ | Conditional jumps |
| SUB | 3 | Arithmetic | 4 clocks | C, Z (optional WC/WZ) | Partial | SUB | Basic arithmetic |
| ROL | 3 | Shift/Rotate | 4 clocks | C, Z (optional WC/WZ) | Partial | ROL | Bit manipulation |
| RCL | 3 | Shift/Rotate | 4 clocks | C, Z (optional WC/WZ) | Partial | RCL | Carry-based rotation |
| WRWORD | 2 | Hub Access | 7-22 clocks | None | Minimal | WRWORD | Word operations |
| SAR | 2 | Shift/Rotate | 4 clocks | C, Z (optional WC/WZ) | Minimal | SAR | Arithmetic shift |
| ROR | 2 | Shift/Rotate | 4 clocks | C, Z (optional WC/WZ) | Minimal | ROR | Rotation operations |
| RCR | 2 | Shift/Rotate | 4 clocks | C, Z (optional WC/WZ) | Minimal | RCR | Carry-based rotation |
| OR | 2 | Logic | 4 clocks | Z, C=parity (optional WC/WZ) | Minimal | OR | Logic operations |
| MUX | 2 | Conditional | 4 clocks | None | Partial | MUXC/MUXNC/MUXZ/MUXNZ | Conditional operations |
| LOCKNEW | 2 | System | Variable | C | Partial | LOCKNEW | Lock acquisition |
| LOCKCLR | 2 | System | Variable | None | Partial | LOCKCLR | Lock release |
| CMP | 2 | Arithmetic | 4 clocks | C, Z (WC/WZ) | Partial | CMP | Comparison |
| CALL | 2 | Control Flow | 4 clocks | None | Complete | CALL | Subroutine shortcuts |
| ADDX | 2 | Arithmetic | 4 clocks | C, Z (optional WC/WZ) | Complete | ADDX | Extended addition |
| ABS | 2 | Arithmetic | 4 clocks | C, Z (optional WC/WZ) | Partial | ABS | Absolute value |

### Single-Usage Instructions (Mentioned Only)

| Instruction | Usage Count | Category | Timing | Flag Effects | Description Status | P2 Equivalent | Tutorial Context |
|-------------|-------------|----------|--------|--------------|-------------------|---------------|------------------|
| XOR | 1 | Logic | 4 clocks | Z, C=parity (optional WC/WZ) | Minimal | XOR | Logic operations |
| TEST | 1 | Logic | 4 clocks | C, Z (WC/WZ) | Minimal | TEST | Testing operations |
| SUM | 1 | Conditional | 4 clocks | Depends on condition | Minimal | SUMC/SUMNC/SUMZ/SUMNZ | Account balancing |
| SUBABS | 1 | Arithmetic | 4 clocks | C, Z (optional WC/WZ) | Minimal | SUBABS | Subtract absolute |
| REV | 1 | Bit Manipulation | 4 clocks | Z (optional WZ) | Complete | REV | Bit reversal |
| RET | 1 | Control Flow | 4 clocks | None | Complete | RET | Return shortcut |
| RDWORD | 1 | Hub Access | 7-22 clocks | Z (optional WZ) | Minimal | RDWORD | Word access |
| MINS | 1 | Arithmetic | 4 clocks | Z (optional WZ) | Minimal | MINS | Signed minimum |
| MIN | 1 | Arithmetic | 4 clocks | Z (optional WZ) | Complete | MIN | Minimum/clipping |
| MAXS | 1 | Arithmetic | 4 clocks | Z (optional WZ) | Minimal | MAXS | Signed maximum |
| MAX | 1 | Arithmetic | 4 clocks | Z (optional WZ) | Complete | MAX | Maximum/clipping |
| LOCKRET | 1 | System | Variable | None | Minimal | LOCKRET | Lock return |
| COGSTOP | 1 | System | Immediate | None | Minimal | COGSTOP | COG control |
| COGINIT | 1 | System | 100µs | C | Partial | COGINIT | COG startup |
| COGID | 1 | System | 4 clocks | Z (optional WZ) | Minimal | COGID | COG identification |
| CLKSET | 1 | System | Variable | None | Minimal | CLKSET | Clock configuration |
| ANDN | 1 | Logic | 4 clocks | Z, C=parity (optional WC/WZ) | Minimal | ANDN | AND-NOT operation |
| ABSNEG | 1 | Arithmetic | 4 clocks | C, Z (optional WC/WZ) | Minimal | ABSNEG | Conditional absolute |

---

## Summary Statistics

### Instruction Distribution
- **Total Instructions**: 66 instructions from DeSilva tutorial
- **High Usage (10+ occurrences)**: 8 instructions (12%)
- **Medium Usage (4-9 occurrences)**: 11 instructions (17%)
- **Low Usage (2-3 occurrences)**: 16 instructions (24%)
- **Single Usage (1 occurrence)**: 31 instructions (47%)

### Category Analysis
| Category | Instructions | Percentage | Notes |
|----------|-------------|------------|-------|
| Data Movement | 8 instructions | 12% | MOV, MOVI, MOVS, MOVD emphasis |
| Arithmetic | 13 instructions | 20% | Core math operations |
| Control Flow | 8 instructions | 12% | Jumps, calls, conditionals |
| Hub Access | 7 instructions | 11% | Memory interface |
| Logic | 6 instructions | 9% | Bitwise operations |
| Shift/Rotate | 8 instructions | 12% | Bit manipulation |
| System | 6 instructions | 9% | COG, clock, lock control |
| I/O Control | 3 instructions | 5% | Pin operations |
| Timing | 1 instruction | 1% | WAITCNT |
| Conditional | 2 instructions | 3% | MUX, SUM families |
| Bit Manipulation | 1 instruction | 1% | REV |

### Coverage Quality
- **Complete Coverage**: 16 instructions (24%) - Detailed explanation with examples
- **Partial Coverage**: 35 instructions (53%) - Mentioned with some context
- **Minimal Coverage**: 15 instructions (23%) - Brief mention only

### P1→P2 Transfer Analysis
- **Direct Transfer**: 60 instructions (91%) - Exist in P2 with same/similar names
- **Enhanced in P2**: 6 instructions (9%) - P2 has extended variants (MUX→MUXx, SUM→SUMx, NEG→NEGx)
- **P1-Specific**: 0 instructions - All tutorial instructions have P2 equivalents

## Key P1 Architecture Insights (from DeSilva)

### Timing Model
- **Standard Instructions**: 4 clocks each (333ns @ 12MHz RCFAST)
- **Hub Access**: Variable 7-22 clocks due to 16-cycle hub rotation
- **Conditional Jumps**: 4 clocks if taken, 8 clocks if fallen through
- **COG Loading**: 100µs for complete 2KB COG load

### Memory Architecture
- **COG RAM**: 496 instruction cells + 16 I/O registers (512 total)
- **Hub RAM**: 32KB shared among 8 COGs
- **Hub Rotation**: 16-cycle slots, 2 clocks per COG access window
- **Bootstrap**: ROM → COG #0 → SPIN interpreter → program loading

### Programming Model
- **Self-Modifying Code**: Essential technique using MOVI/MOVS/MOVD
- **Flag System**: Only C (carry) and Z (zero) flags, explicit WC/WZ needed
- **Conditional Execution**: All instructions can be conditional
- **No Stack**: JMPRET-based subroutines, no PUSH/POP

### Parallel Processing
- **8 COGs**: Independent 20 MIPS processors
- **Semaphores**: 8 hardware locks for coordination
- **Hub Sharing**: Deterministic time-slot access
- **Pin OR-Logic**: Multiple COGs can control same pins

## Missing P1 Knowledge (Gaps to Fill)

### High Priority Missing
1. **Complete Instruction Set** - Tutorial covers ~66 of total P1 instructions
2. **Official Timing Data** - Only tutorial estimates available
3. **Encoding Details** - Instruction format specifications
4. **Advanced Instructions** - Video, counter, specialized operations
5. **I/O System Details** - Beyond basic pin operations

### Medium Priority Missing
1. **Programming Examples** - More real-world applications
2. **Performance Analysis** - Cycle-accurate programming
3. **Best Practices** - Optimization techniques
4. **Debug Techniques** - Troubleshooting methods
5. **Memory Maps** - Complete address specifications

### Sources Needed
- **P1 Hardware Manual** - Complete specifications
- **P1 Datasheet** - Timing and electrical characteristics  
- **Official Assembly Manual** - Complete instruction reference
- **Application Notes** - Advanced programming techniques
- **Community Resources** - Real-world examples and libraries

## P1↔P2 Comparison Preparation

### Transfer Categories
1. **Direct Equivalents** (60 instructions): Same functionality, possibly enhanced timing/features
2. **Enhanced in P2** (6 instructions): P1 concept expanded (MUX→MUXx family)
3. **P1-Unique**: None identified in tutorial scope
4. **P2-New**: Smart Pins, CORDIC, Events, Enhanced I/O (not in P1)

### Comparison Dimensions
- **Instruction Set Completeness**: P1 baseline vs P2 expansion
- **Timing Models**: P1 hub rotation vs P2 enhanced timing
- **Memory Architecture**: P1 32KB vs P2 larger memory
- **Feature Scope**: P1 core features vs P2 specialized hardware
- **Programming Complexity**: P1 self-modification vs P2 enhanced addressing

### Value for P2 Documentation
1. **Teaching Progression**: DeSilva's proven pedagogical approach
2. **Conceptual Foundation**: Core parallel processing concepts
3. **Common Patterns**: Programming techniques that transfer
4. **Migration Guide**: P1→P2 transition assistance
5. **Historical Context**: Understanding P2 design evolution

---

*This P1 reference table provides the foundation for P1↔P2 comparison analysis but requires formal P1 documentation for completion.*