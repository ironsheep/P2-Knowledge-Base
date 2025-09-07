# P2 Instruction Learning Paths

Structured progression through P2 instruction set

## Beginner Path

### Step 1: Basic Data Movement
**Instructions**: MOV, MOVBYTS

**Concepts**:
- Register operations
- Immediate values

**Exercises**:
- Copy register
- Load constants

### Step 2: Basic Arithmetic
**Instructions**: ADD, SUB, CMP

**Concepts**:
- ALU operations
- Flag effects

**Exercises**:
- Simple calculations
- Loop counters

### Step 3: Conditional Execution
**Instructions**: IF_Z, IF_NZ, IF_C, IF_NC

**Concepts**:
- Flags
- Conditional prefixes

**Exercises**:
- Conditional moves
- Min/max operations

### Step 4: Basic Branching
**Instructions**: JMP, TJZ, DJNZ

**Concepts**:
- Program flow
- Loop control

**Exercises**:
- Simple loops
- Conditional jumps

### Step 5: Hub Memory Access
**Instructions**: RDBYTE, RDWORD, RDLONG, WRBYTE, WRWORD, WRLONG

**Concepts**:
- Hub timing
- Memory addressing

**Exercises**:
- Read/write variables
- Array access

---

## Intermediate Path

### Step 1: ALTx Instructions
**Instructions**: ALTS, ALTD, ALTI, ALTR

**Concepts**:
- Instruction modification
- Indexing

**Exercises**:
- Table lookup
- Indirect addressing

### Step 2: Block Transfers
**Instructions**: SETQ, SETQ2, RDLONG, WRLONG

**Concepts**:
- Fast block moves
- FIFO operations

**Exercises**:
- Buffer copies
- Stack operations

### Step 3: Bit Manipulation
**Instructions**: BITC, BITH, BITL, BITNC, BITZ, BITNZ

**Concepts**:
- Bit fields
- Flag manipulation

**Exercises**:
- Bit masks
- State machines

### Step 4: Streaming Operations
**Instructions**: RDFAST, WRFAST, RFBYTE, WFBYTE

**Concepts**:
- FIFO streaming
- Predictable timing

**Exercises**:
- Video output
- Data streaming

---

## Advanced Path

### Step 1: Smart Pin Programming
**Instructions**: WRPIN, WXPIN, WYPIN, RDPIN, AKPIN

**Concepts**:
- Pin modes
- Smart pin configuration

**Exercises**:
- PWM generation
- Serial communication

### Step 2: CORDIC Operations
**Instructions**: QROTATE, QMUL, QDIV, QSQRT, GETQX, GETQY

**Concepts**:
- Pipeline usage
- Math acceleration

**Exercises**:
- Coordinate transforms
- DSP operations

### Step 3: Multi-Cog Programming
**Instructions**: COGINIT, COGSTOP, COGID, LOCKNEW, LOCKREL

**Concepts**:
- Parallel processing
- Synchronization

**Exercises**:
- Task distribution
- Resource sharing

### Step 4: Interrupt Handling
**Instructions**: SETINT1, SETINT2, SETINT3, TRGINT1, NIXINT1

**Concepts**:
- Event handling
- Interrupt vectors

**Exercises**:
- Timer interrupts
- Pin events

---

