# P2 Instruction Table - p2docs.github.io

**Source**: https://p2docs.github.io/p2_optable.html  
**Import Date**: 2025-08-15  
**Verification Status**: 🟡 NEEDS VERIFICATION - Community source, requires validation against official P2 documentation  
**Purpose**: Instruction reference for ADA video/emulation projects

## ⚠️ Verification Requirements

This community documentation requires verification against:
- Official Parallax P2 documentation
- P2 assembly manual
- Chip's official instruction specifications

Ada's work is generally very accurate, but verification is mandatory for instruction-level content.

## Instruction Table Overview

**Format**: 32-bit instruction format with standardized encoding

### Instruction Format Components
- **EEEE**: Encoding bits
- **CZI**: Condition/flag modification bits  
- **D**: Destination register (9 bits)
- **S**: Source register/immediate value (9 bits)

### Major Instruction Categories

#### 1. Math and Logic Operations
- **Shifts**: ROR, ROL, SHR, SHL
- **Arithmetic**: ADD, SUB, MUL
- **Bitwise**: AND, OR, XOR

#### 2. Memory and Hub Operations  
- **Read/Write**: RDLONG, WRLONG
- **FIFO operations**
- **Pointer manipulations**

#### 3. Branch and Control
- **Conditional jumps**
- **Subroutine calls**
- **Event-based branching**

#### 4. Pin and I/O Control
- **Smart pin configurations**
- **Direct pin manipulation**

#### 5. Special Functions
- **CORDIC operations**
- **Colorspace conversions**
- **Pixel mixing**

## ADA Video/Emulation Relevance

**Critical for:**
- Video signal generation (colorspace, pixel mixing)
- High-performance emulation (math operations, branching)
- Game controller input (pin control, event handling)
- Custom sound generation (CORDIC, arithmetic)

## Verification Action Items

1. Cross-reference with official P2 instruction manual
2. Validate opcode encodings against Parallax specifications
3. Verify clock cycle counts and behavioral descriptions
4. Check special function details (CORDIC, video operations)

## Next Steps
- Import opcode matrix for encoding verification
- Extract Smart Pin documentation
- Document video encoder instruction details