# P2 Meta-Knowledge Index

**Generated**: 2025-09-06T14:45:53.170295
**Total Insights**: 18

## Architectural Insights

### Hub/Cog Interaction
Hub memory uses egg-beater rotation for fair access. Each cog gets a hub window every 8 clocks.
- **Related Instructions**: RDBYTE, RDWORD, RDLONG, WRBYTE, WRWORD, WRLONG
- **Impact**: timing_critical

### CORDIC Solver
CORDIC uses 54-stage pipeline. Multiple operations can be pipelined for throughput.
- **Related Instructions**: QROTATE, QVECTOR, QMUL, QDIV, QSQRT, QLOG, QEXP
- **Impact**: performance

## Common Gotchas

### Pipeline Flush on Branches
Branch instructions flush the 5-stage pipeline, causing 3+ cycle penalty
- **Affected**: JMP, CALL, RET, Jxx conditional jumps
- **Mitigation**: Use conditional execution (IF_xx) for short sequences instead of branches

### Hub Window Alignment
Hub access timing varies 13-20 cycles based on window alignment
- **Affected**: All RDxxxx/WRxxxx hub operations
- **Mitigation**: Use RDFAST/WRFAST with FIFO for predictable streaming

## Optimization Techniques

### Instruction Pairing
ALTx instructions modify the next instruction without pipeline stall
- **Examples**: ALTS + MOV for indexed access, ALTD + ADD for destination indexing
- **Benefit**: Avoid self-modifying code penalties

### Block Transfers
SETQ/SETQ2 enable fast block transfers between cog/lut/hub
- **Examples**: SETQ + RDLONG for hub->cog block read, SETQ2 + RDLONG for hub->lut
- **Benefit**: Transfer 1 long per clock after initial setup

## Instruction Categories

### Math Basic
- **Instructions**: ADD, SUB, CMP, NEG, ABS...
- **Characteristics**: Fixed 2-cycle execution, affects C/Z flags
- **Common Usage**: Loop counters, address calculations, arithmetic

### Math Multiply
- **Instructions**: MUL, MULS, SCA, SCAS...
- **Characteristics**: 2-cycle for 16x16 bit, special scaling modes
- **Common Usage**: Fixed-point math, scaling operations

### Bit Operations
- **Instructions**: AND, OR, XOR, NOT, TEST...
- **Characteristics**: Bit manipulation, flag testing, mask operations
- **Common Usage**: Flag manipulation, bit fields, masks

### Memory Cog
- **Instructions**: MOV, MOVBYTS, SETBYTE, GETBYTE...
- **Characteristics**: 2-cycle cog RAM access
- **Common Usage**: Register operations, byte manipulation

### Memory Hub
- **Instructions**: RDBYTE, RDWORD, RDLONG, WRBYTE, WRWORD...
- **Characteristics**: Variable timing (13-20 cycles), hub window dependent
- **Common Usage**: Main memory access, data structures

### Memory Streaming
- **Instructions**: RDFAST, WRFAST, RFBYTE, RFWORD, RFLONG...
- **Characteristics**: FIFO-based streaming, predictable timing
- **Common Usage**: Video, audio, bulk data transfer

### Branch Unconditional
- **Instructions**: JMP, CALL, RET, CALLA, CALLB...
- **Characteristics**: Pipeline flush, 5+ cycle cost
- **Common Usage**: Program flow, subroutines

### Branch Conditional
- **Instructions**: TJZ, TJNZ, TJF, TJNF, DJZ...
- **Characteristics**: Test-and-jump, decrement-and-jump patterns
- **Common Usage**: Loop control, conditional execution

### Smart Pin
- **Instructions**: WRPIN, WXPIN, WYPIN, RDPIN, RQPIN...
- **Characteristics**: Smart pin configuration and control
- **Common Usage**: PWM, serial, ADC, DAC, counters

### Cordic
- **Instructions**: QROTATE, QVECTOR, QMUL, QDIV, QSQRT...
- **Characteristics**: 54-stage pipeline, concurrent operations possible
- **Common Usage**: Math acceleration, DSP, graphics transforms

### Special
- **Instructions**: GETCT, WAITX, WAITCT1, COGID, COGINIT...
- **Characteristics**: System control, timing, cog management
- **Common Usage**: Timing, multi-cog coordination

