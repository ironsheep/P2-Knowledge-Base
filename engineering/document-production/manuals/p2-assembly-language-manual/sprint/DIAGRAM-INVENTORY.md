# PASM2 Manual - Diagram Inventory

**Purpose:** Complete inventory of TikZ diagrams needed for the P2 Assembly Language Manual.

**Status:** Phase 1.1 - Initial inventory created

---

## Summary

| Category | Count | Macro Available |
|----------|-------|-----------------|
| Part I Architectural | 11 | Partial |
| Directive Memory | 5 | Yes |
| Bit Reordering | 12 | Yes |
| Special Registers | 4 | Yes |
| CORDIC | 2 | No |
| SmartPin Config | 2 | No |
| Streamer Config | 1 | No |
| **Total** | **37** | |

---

## Part I: Architectural Diagrams

### Chapter 1: Execution Model

| ID | Description | Type | Complexity | Macro |
|----|-------------|------|------------|-------|
| D1.1 | 8-COG overview with shared Hub | Architecture | High | Custom |
| D1.2 | COG memory map ($000-$1FF) | Memory Map | Medium | `\CogMemoryMap` |
| D1.3 | Special registers ($1F0-$1FF) detail | Memory Map | Medium | `\SpecialRegistersMap` |
| D1.4 | Hub memory layout (512KB) | Memory Map | Medium | `\HubMemoryMap` |
| D1.5 | LUT memory layout | Memory Map | Low | `\MemoryMap` |
| D1.6 | COG-Hub relationship | Architecture | High | `\CogHubRelationship` |

### Chapter 2: Instruction Format

| ID | Description | Type | Complexity | Macro |
|----|-------------|------|------------|-------|
| D2.1 | 32-bit instruction word anatomy | Bit Field | Medium | `\InstructionEncoding` |

### Chapter 4: Timing

| ID | Description | Type | Complexity | Macro |
|----|-------------|------|------------|-------|
| D4.1 | Egg beater Hub timing | Timing | High | Custom |
| D4.2 | Branch timing (taken vs not taken) | Timing | Medium | Custom |
| D4.3 | Burst transfer timing | Timing | Medium | Custom |

### Chapter 5: Hardware

| ID | Description | Type | Complexity | Macro |
|----|-------------|------|------------|-------|
| D5.1 | CORDIC operation pipeline | Flow | Medium | Custom |
| D5.2 | Smart Pin block diagram | Architecture | High | Custom |

---

## Part II: Instruction-Specific Diagrams

### Bit Reordering Instructions

These diagrams use the `\BitReorder` and related macros from `p2kb-pasm2-diagrams.sty`.

| ID | Instruction | Description | Macro |
|----|-------------|-------------|-------|
| D-SPLITB | SPLITB | Extract every 4th bit to bytes | `\SplitBDiagram` |
| D-SPLITW | SPLITW | Split words | Custom |
| D-MERGB | MERGB | Merge bits from bytes | Custom |
| D-MERGW | MERGW | Merge words | Custom |
| D-MOVBYTS | MOVBYTS | Byte shuffle within long | `\MovbytsDiagram` |
| D-ROLNIB | ROLNIB | Nibble rotation | Custom |
| D-ROLBYTE | ROLBYTE | Byte rotation | Custom |
| D-ROLWORD | ROLWORD | Word rotation | Custom |
| D-SETNIB | SETNIB | Insert nibble | Custom |
| D-SETBYTE | SETBYTE | Insert byte | Custom |
| D-SETWORD | SETWORD | Insert word | Custom |
| D-REV | REV | Bit reversal | `\RevDiagram` |

### Register Bit Field Diagrams

| ID | Instruction | Description | Macro |
|----|-------------|-------------|-------|
| D-COGINIT | COGINIT | Dest field format | `\CoginitDestField` |
| D-DIRA | DIRA/DIRB | Direction register | `\DirRegisterField` |
| D-PTRA | PTRA/PTRB | Pointer register | Custom |
| D-CRCBIT | CRCBIT | CRC bit field | Custom |

---

## Part II: Directive Diagrams

### Memory Alignment Diagrams

| ID | Directive | Description | Macro |
|----|-----------|-------------|-------|
| D-BYTE | BYTE | Byte in memory | `\MemoryMap` |
| D-WORD | WORD | Word alignment | `\MemoryMap` |
| D-LONG | LONG | Long alignment | `\MemoryMap` |
| D-ALIGNW | ALIGNW | Word alignment effect | `\MemoryMap` |
| D-ALIGNL | ALIGNL | Long alignment effect | `\MemoryMap` |

---

## Macro Availability Status

### Available in p2kb-pasm2-diagrams.sty

| Macro | Purpose | Status |
|-------|---------|--------|
| `\CogMemoryMap` | COG memory layout | Complete |
| `\HubMemoryMap` | Hub memory layout | Complete |
| `\SpecialRegistersMap` | $1F0-$1FF registers | Complete |
| `\CogHubRelationship` | COG-Hub interaction | Complete |
| `\InstructionEncoding` | 32-bit encoding diagram | Complete |
| `\MemoryMap{}` | Generic memory region | Complete |
| `\MemRegion{}` | Memory region component | Complete |
| `\SplitBDiagram` | SPLITB operation | Complete |
| `\RevDiagram` | REV operation | Complete |
| `\MovbytsDiagram{}` | MOVBYTS with pattern | Complete |
| `\BitValueBar{}` | 32-bit value with bytes | Complete |
| `\CoginitDestField` | COGINIT field | Complete |
| `\DirRegisterField` | DIRA/DIRB field | Complete |
| `\RegisterBitField{}` | Generic bit field | Complete |

### Need to Create

| Macro | Purpose | Priority |
|-------|---------|----------|
| `\EggBeaterDiagram` | Hub timing visualization | High |
| `\CordicPipeline` | CORDIC operation flow | Medium |
| `\SmartPinBlock` | Smart Pin architecture | Medium |
| `\SplitWDiagram` | SPLITW operation | Low |
| `\MergBDiagram` | MERGB operation | Low |
| `\MergWDiagram` | MERGW operation | Low |
| `\RolNibDiagram` | Nibble rotation | Low |
| `\RolByteDiagram` | Byte rotation | Low |
| `\RolWordDiagram` | Word rotation | Low |
| `\BurstTimingDiagram` | Burst transfer timing | Medium |

---

## Implementation Notes

### Diagram Generation Strategy

1. **Part I diagrams:** Generate during Phase 5 (Part I content writing)
2. **Bit reordering:** Generate during Phase 2-4 as instructions are documented
3. **Directive diagrams:** Generate during Phase 2.3 (directive entries)

### Color Palette

All diagrams use colors defined in `p2kb-pasm2-diagrams.sty`:

```latex
\definecolor{mem-cog}{HTML}{E0F0E0}       % Light green - COG
\definecolor{mem-hub}{HTML}{E0E0F0}       % Light blue - Hub
\definecolor{mem-lut}{HTML}{F0E0E0}       % Light red - LUT
\definecolor{mem-special}{HTML}{F0F0E0}   % Light yellow - Special
\definecolor{encoding-cond}{HTML}{E8E8E8} % Condition field
\definecolor{encoding-op}{HTML}{D0D0D0}   % Opcode field
\definecolor{encoding-flag}{HTML}{E8E0E0} % Flag field
\definecolor{encoding-dest}{HTML}{E0E8E0} % Dest field
\definecolor{encoding-src}{HTML}{E0E0E8}  % Src field
```

### Complexity Ratings

| Rating | Meaning |
|--------|---------|
| Low | Simple shapes, few elements, can use existing macros |
| Medium | Multiple elements, some custom positioning |
| High | Complex layout, animations/arrows, requires new macro |

---

*Created: 2025-11-28*
*Sprint: PASM2 Manual Generation Phase 1.1*
