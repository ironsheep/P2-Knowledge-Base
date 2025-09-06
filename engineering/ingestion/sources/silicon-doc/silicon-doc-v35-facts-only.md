# P2 Silicon Documentation v35 - Technical Facts
*Pure P2 technical specifications and features extracted from Silicon Doc v35*

## Document Structure
- **Total Parts**: 5 separate PDFs
- **Format**: Rev B/C Silicon documentation by Chip Gracey
- **Pages**: 121 total across all parts

---

## Hardware Specifications

### Known Bugs
1. **ALTx/AUGS/AUGD with SETQ block transfers**: Intervening instructions cancel special PTRx deltas
2. **AUGS with immediate ALTx**: Unintended AUGS value usage
- Both bugs have documented workarounds

### Pin Descriptions

**Pin Groups**:
- Pins grouped in sets of 4 (0-3, 4-7, 8-11, etc.)
- VIO_{x}_{y} = Power (3.3V) for pins x through y
- GIO_{x}_{y} = Ground for pins x through y

**Pin Types**:
- TEST: Tied to ground
- VDD: 1.8V core power
- VSS: Ground
- P0-P63: Smart pins (I/O, 0-3.3V)
- P58-P63: Boot source pins
- XI/XO: Crystal pins (no external components needed)
- RESn: Active-low reset

### Memory Architecture

| Memory Region | Width | Depth | D/S Address | PC Range |
|--------------|-------|-------|-------------|----------|
| COG | 32 bits | 512 | $000..$1FF | $00000..$001FF |
| LOOKUP | 32 bits | 512 | $000..$1FF | $00200..$003FF |
| HUB | 8 bits | 1MB max* | $00000..$FFFFF | $00400..$FFFFF |

*P2X8C4M64P has 512KB

**Execution Modes**:

| PC Address | Instruction Source | Memory Width | PC Increment |
|------------|-------------------|--------------|--------------|
| $00000..$001FF | cog register RAM | 32 bits | 1 |
| $00200..$003FF | cog lookup RAM | 32 bits | 1 |
| $00400..$FFFFF | hub RAM | 8 bits | 4 |

### Instruction Encoding

- EEEE: Conditional execution (4 bits)
- C/Z: Flag update control (2 bits)
- I/L: Immediate vs register operands (1 bit)
- R: Relative vs absolute addressing (1 bit)
- WW: Special register index (2 bits)
- DDDDDDDDD/SSSSSSSSS: 9-bit operand fields

---

## COG Architecture

### Pipeline
- 5-stage pipeline architecture
- 2-clock execution when pipeline full
- Branches flush pipeline (5+ clock penalty)
- Each COG independent with own RAM
- Shared resources: system clock, HUB RAM, I/O pins

### Starting and Stopping COGs

**COGINIT Encoding**:
- D[5]: 0=load from HUB, 1=direct start
- D[4]: 0=specific COG, 1=find free
- D[3:0]: COG ID when D[4]=0
- D[0]: when D[4]=1, 0=single, 1=pair
- SETQ value → PTRA, S/# address → PTRB

### COG RAM Organization

**RAM Layout**:
- $000-$1EF: General purpose (496 registers)
- $1F0-$1F7: Dual-purpose (RAM or interrupt/call vectors)
- $1F8-$1FF: Special-purpose (hardware registers, not RAM)

**Special Registers**:
- PTRA/PTRB: HUB pointers
- DIRA/DIRB: Pin output enables
- OUTA/OUTB: Pin output states
- INA/INB: Pin input states (also debug vectors)

### LOOKUP RAM

**Access Methods**:
- RDLUT/WRLUT instructions (load/store)
- Not directly addressable like COG RAM

**Uses**:
- Streamer source/destination
- Bytecode lookup tables
- Smart pin data source
- COG pair sharing (0&1, 2&3, 4&5, 6&7)
- Program execution

**Sharing Mechanism**:
- SETLUTS enables adjacent COG writes
- Uses 2nd port (conflicts with streamer DDS/LUT)
- SETSE1-4 for handshaking events

---

## Register Indirection

### ALT Instructions
- ALTS/ALTD/ALTR: Modify next instruction's S/D/Result fields
- ALTB: Bit field access across registers
- ALTxN/ALTxB/ALTxW: Nibble/Byte/Word specialized access
- ALTI: Complex multi-field modifier with auto-increment

**Capabilities**:
- Dynamic instruction field modification at runtime
- Base + scaled index addressing
- Auto-incrementing pointers with masking
- Instruction synthesis (executing data as instructions)

---

## Branch Addressing

### Instruction Categories

**Register Absolute Branches**:
- JMP/CALL/CALLA/CALLB D
- Always use D[19:0] as absolute address

**JMPREL - Register-Based Relative Jump**:
- COG: Adds D[19:0] to PC
- HUB: Adds D[17:0]<<2 to PC

**S-Field Dual Mode Branches**:
- Register S: Absolute using S[19:0]
- Immediate #S: Relative using sign-extended 9 bits (-256 to +255)
- Includes: CALLPA/CALLPB, CALLD, conditional jumps

**20-bit Immediate Branches**:
- JMP/CALL/CALLA/CALLB/CALLD/LOC #A
- Default relative, '\' forces absolute

### Domain-Crossing Rules
- COG→HUB: Forces absolute
- HUB→COG: Forces absolute
- Same→Same: Defaults to relative
- `\` after # forces absolute
- `@` gets hub address of cog label

---

## Instruction Repeating

### REP Instruction
`REP {#}D,{#}S` - Repeat D[8:0] instructions S[31:0] times

**Features**:
- S=0 creates infinite loops
- Zero-overhead in COG/LUT
- Hidden jump in HUB
- Any branch cancels REP
- Interrupts blocked during REP

**Assembler Support**:
```pasm
REP @.end,count
    ; code block
.end
```

---

## Instruction Skipping

### Three Skip Instructions

**SKIP {#}D**:
- Cancel instructions per D[31:0] bit pattern
- Works in HUB and COG/LUT
- Canceled instructions become 2-clock NOPs

**SKIPF {#}D**:
- Fast skip by PC stepping (COG/LUT only)
- Can step over 1-7 instructions at once
- Zero overhead for skipped instructions

**EXECF {#}D**:
- Combines JMP D[9:0] + SKIPF D[31:10]
- 22-bit skip pattern

### Skip Pattern Mechanics
- LSB-first consumption of pattern
- Shift right by 1 for each instruction
- Bit=1: Skip, Bit=0: Execute
- CALL/RET behavior preserves skip context

### SKIPF Special Rules
- Must use absolute addressing if next instruction might be skipped for CALLs
- Register addresses work (they're absolute)
- CALL can use '#\address' for absolute immediate
- Immediate-relative branches work naturally for other branches
- Absolute branches: Don't skip first instruction after branch

---

## XBYTE - Bytecode Execution Engine

### 8-Clock Bytecode Cycle

| Clock | Phase | Activity | Description |
|-------|-------|----------|-------------|
| 1 | go | RFBYTE bytecode, SKIPF #0 | Fetch bytecode from FIFO, cancel any SKIPF |
| 2 | get | MOV PA,bytecode, RDLUT | Write bytecode to PA ($1F6), read LUT |
| 3 | go | RDLUT (data → D) | Get LUT long into D for EXECF |
| 4 | get | EXECF D (begin) | Execute EXECF |
| 5 | go | MOV PB,(GETPTR), MODCZ | Write FIFO ptr to PB, optionally set C,Z |
| 6 | get | flush pipeline | Pipeline flush for branch |
| 7 | go | reload pipeline | Pipeline reload |
| 8 | get | (first instruction) | First instruction of bytecode routine |

**Total: 6 clocks overhead + routine execution time**

### XBYTE Configuration

**Starting XBYTE**: `_RET_ SETQ {#}D` with $1FF on stack

**Configuration Patterns**:

| Bits | SETQ Value | LUT Base | Index Calculation | Use Case |
|------|------------|----------|-------------------|----------|
| 8 | %A000000xF | %A00000000 | I = b[7:0] | Full 256 bytecodes |
| 8 | %ABBBB00xF | %A00000000 | Conditional on b[7:4] | Compressed sets of 16 |
| 7 | %AAxx0010F | %AA0000000 | I = b[6:0] | 128 bytecodes |
| 7 | %AAxx0011F | %AA0000000 | I = b[7:1] | 128 bytecodes, shifted |
| 6 | %AAAx1010F | %AAA000000 | I = b[5:0] | 64 bytecodes |
| 5 | %AAAAx100F | %AAAA00000 | I = b[4:0] | 32 bytecodes |
| 4 | %AAAAA110F | %AAAAA0000 | I = b[3:0] | 16 bytecodes |

**%F Flag Bit**:
- 0: Don't affect flags
- 1: Write bytecode index LSBs to C and Z

### Compression Feature (%ABBBB00xF)
- If b[7:4] < %BBBB: Use full bytecode as index
- If b[7:4] >= %BBBB: Use compressed index (b[7:4] - %BBBB)
- Bytecode always written to PA for use as operand

---

## SETQ/Q Register

### Q Register Modified by:
- **XORO32**: Q = XORO32 result
- **RDLUT**: Q = data read from LUT
- **GETXACC**: Q = Goertzel sine accumulator
- **CRCNIB**: Q shifts left by 4 bits (reads and writes Q)
- **COGINIT/QDIV/QFRAC/QROTATE** without SETQ: Q = 0

### Protection
- SETQ/SETQ2 shields next instruction from interruption
- CRCNIB must not be interrupted between SETQ and CRCNIB
- Use STALLI/ALLOWI bracket or REP block for protection

### Retrieving Q Value
```pasm
MOV     qval,#0
MUXQ    qval,##$FFFFFFFF
```

---

## Pixel Operations

### Core Instructions (7-clock operations)
- **ADDPIX D,S/#** - Add bytes with saturation
- **MULPIX D,S/#** - Multiply bytes ($FF = 1.0)
- **BLNPIX D,S/#** - Alpha-blend bytes using SETPIV value
- **MIXPIX D,S/#** - Mix bytes using SETPIX/SETPIV configuration

### Setup Instructions
- **SETPIV D/#** - Set blend factor V[7:0]
- **SETPIX D/#** - Set MIXPIX mode M[5:0]

### Pixel Format
- 32-bit register contains 4 bytes (RGBA or similar)
- Operations work on corresponding byte pairs
- Sum-of-products with saturation: `D[byte] = ((D[byte] * DMIX + S[byte] * SMIX + $FF) >> 8) max $FF`

### DMIX/SMIX Terms

| Instruction | DMIX | SMIX |
|------------|------|------|
| ADDPIX | $FF | $FF |
| MULPIX | S[byte] | $00 |
| BLNPIX | !V | V |
| MIXPIX | Configurable via M[5:3] | Configurable via M[2:0] |

### MIXPIX Configuration
- M[5:3] controls DMIX: $00, $FF, V, !V, S[byte], !S[byte], D[byte], !D[byte]
- M[2:0] controls SMIX: Same options
- 64 different blend modes (8×8 combinations)

---

## DACs

### Four 8-bit DAC Channels per COG
- DAC0: Drives pins %XXXX00 (every 4th pin starting at 0)
- DAC1: Drives pins %XXXX01 (every 4th pin starting at 1)
- DAC2: Drives pins %XXXX10 (every 4th pin starting at 2)
- DAC3: Drives pins %XXXX11 (every 4th pin starting at 3)

### SETDACS Instruction
- Sets background DAC values for all 4 channels
- Format: `SETDACS D/#` - Bytes 3/2/1/0 → DAC3/DAC2/DAC1/DAC0
- Values output constantly except when overridden by streamer/colorspace

---

## Streamer

### Core Instructions
- **SETXFRQ D/#** - Set NCO frequency (32-bit value)
- **XINIT D/#,S/#** - Start immediately, zero phase
- **XZERO D/#,S/#** - Start on NCO rollover, zero phase
- **XCONT D/#,S/#** - Start on NCO rollover, continue phase
- **GETXACC D** - Get Goertzel X→D, Y→next S, clear accumulators

### NCO Operation
- 32-bit phase accumulator
- Phase = (phase & $7FFF_FFFF) + frequency
- Rollover triggers data transfer
- D[15:0] = transfer count (1-65535, $FFFF = perpetual)

### Command Format D[31:16]
- D[31:28]: Mode (defines operation type)
- D[27:24]: DAC channel mapping (%dddd)
- D[23]: Enable bit (e=pin output, w=write to hub)
- D[22:20]: Pin group selection (%ppp, 8-pin increments)
- D[19:16]: Mode-specific (base address, pin selection, etc.)

### Streamer Mode Categories
1. Immediate → LUT → Pins/DACs
2. Immediate → Pins/DACs
3. RDFAST → LUT → Pins/DACs
4. RDFAST → Pins/DACs
5. RDFAST → RGB → Pins/DACs
6. Pins → DACs/WRFAST
7. ADCs/Pins → DACs/WRFAST
8. DDS/Goertzel

### Features
- Automatic RFBYTE/RFWORD/RFLONG from hub
- Automatic WFBYTE/WFWORD/WFLONG to hub
- Pin groups wrap around
- Bit order control (LSB or MSB first)
- Seamless command chaining with XZERO/XCONT

### DAC Channel Mapping (%dddd field)

| dddd | DAC3 | DAC2 | DAC1 | DAC0 | Description |
|------|------|------|------|------|-------------|
| 0000 | -- | -- | -- | -- | No DAC output |
| 0001 | X0 | X0 | X0 | X0 | X0 on all channels |
| 1000 | !X0 | X0 | !X0 | X0 | X0 differential pairs |
| 1011 | X1 | X0 | X1 | X0 | X1,X0 pairs |
| 1111 | X3 | X2 | X1 | X0 | All four channels |

### RGB Modes (Pixel Format Conversion)
- **LUMA8**: 8-bit luminance with S[2:0] color selection
- **RGBI8**: 8-bit RGBI format
- **RGB8**: 3:3:2 format
- **RGB16**: 5:6:5 format
- **RGB24**: 8:8:8 format

All convert to 32-bit %RRRRRRRR_GGGGGGGG_BBBBBBBB_00000000 output.

---

## DDS/Goertzel - Signal Generation and Analysis

### DDS (Direct Digital Synthesis)
- Generates waveforms from LUT samples
- Up to 4 independent DAC outputs
- NCO-driven phase accumulator
- Signed byte samples, MSB-inverted for unsigned DACs

### Goertzel Analysis
- Single-frequency energy detection
- Simultaneous analysis while generating
- Hardware multiply-accumulate
- Sine and cosine accumulations

### Input Configuration (S[19:12])
- Select 1-4 ADC pins for summation
- Invert individual channels (add/subtract)
- Bitstream values: '0'→-1, '1'→+1

### LUT Configuration (S[11:0])

| S[11:0] Pattern | Loop Size | NCO Bits Used | LUT Range |
|-----------------|-----------|---------------|-----------||
| %000_TTTTTTTTT | 512 | 30..22 | Full LUT |
| %001_ATTTTTTTT | 256 | 30..23 | Half LUT |
| %010_AATTTTTTT | 128 | 30..24 | Quarter LUT |
| %111_AAAAAAATT | 4 | 30..29 | 4 entries |

### SINC Modes (D[23])
- SINC1: Direct accumulation
- SINC2: Double accumulation (better noise filtering)

---

## Digital Video Output (DVI/HDMI)

### Hardware TMDS Encoding

**SETCMOD Configuration**:
- CMOD[8:7] = %10: DVI forward (RED+, RED-, GRN+, GRN-, BLU+, BLU-, CLK+, CLK-)
- CMOD[8:7] = %11: DVI reverse (pin order reversed)

**Data Encoding**:
- P[1] = 0: RGB bytes get TMDS encoded (for pixel data)
- P[1] = 1: 10-bit patterns sent literally (for sync/control)

**Requirements**:
- P2 clock = 10x pixel rate (250MHz for 25MHz pixels)
- NCO frequency = $0CCCCCCC+1 (1/10th clock rate)
- 8 consecutive pins for differential pairs

---

## Colorspace Converter

### Matrix Transformation
```
Y = (DAC3 * CY[31:24] + DAC2 * CY[23:16] + DAC1 * CY[15:8]) / 128
I = (DAC3 * CI[31:24] + DAC2 * CI[23:16] + DAC1 * CI[15:8]) / 128
Q = (DAC3 * CQ[31:24] + DAC2 * CQ[23:16] + DAC1 * CQ[15:8]) / 128
```

### Configuration Instructions
- **SETCY D** - Set Y coefficients
- **SETCI D** - Set I coefficients
- **SETCQ D** - Set Q coefficients
- **SETCFRQ D** - Set modulation frequency
- **SETCMOD D** - Set mode and options

### Modulation
- Uses CORDIC rotator for I,Q modulation
- Scales by 1.646 (must account for in coefficients)
- Frequency: CFRQ = $1_0000_0000 * desired_freq / clock_freq

### Output Modes (CMOD[6:5])

| Mode | Description | DAC3 | DAC2 | DAC1 | DAC0 |
|------|-------------|------|------|------|------|
| 00 | Off (bypass) | DAC3 | DAC2 | DAC1 | DAC0 |
| 01 | VGA/HDTV | R/Y | G/Pb | B/Pr | H-Sync |
| 02 | NTSC/PAL S-Video | Composite | Composite | Chroma | Luma |
| 11 | NTSC/PAL Composite | Composite | Composite | Composite | Composite |

---

## I/O Pin Timing
- 3-clock delay from instruction to pin change
- 3-clock delay from pin to register read
- TESTP/TESTPN gets fresher data (2-clock delay)

---

## Cog Attention
- COGATN for inter-cog signaling
- 16-bit mask for targeting multiple cogs
- Used for lightweight synchronization

---

## Events System

### 16 Hardware Events Per COG

**System Events (0-3)**:
- 0: Interrupt occurred (INT 1/2/3, not debug)
- 1: CT passed CT1 target
- 2: CT passed CT2 target
- 3: CT passed CT3 target

**Selectable Events (4-7)**:
- User-configurable: LUT access, hub locks, pin edges
- Each COG configures independently

**I/O & Streaming Events (8-13)**:
- 8: Pin pattern match/mismatch
- 9: Hub FIFO block wrap
- 10: Streamer empty
- 11: Streamer finished
- 12: Streamer NCO rollover
- 13: Streamer read LUT $1FF

**Communication Events (14-15)**:
- 14: COG attention requested
- 15: CORDIC read but empty

### Three Response Mechanisms

**POLLxxx - Non-blocking Check**:
```pasm
POLLCT1 WC    'Check event, result in C, clear flag
```

**WAITxxx - Blocking Wait**:
```pasm
SETQ timeout   'Optional timeout
WAITCT1 WC    'Wait for event, C=1 if timeout
```

**Jxxx/JNxxx - Conditional Branch**:
```pasm
JCT1 #handler  'Jump if event occurred, clear flag
```

### Features
- Always active hardware tracking
- Auto-clear on read (unless being set)
- Race-free handling of simultaneous set/clear
- Independent per COG
- WAITINT stalls COG to save power

---

## Interrupt System

### Main Interrupts (INT1/INT2/INT3)

**Priority Architecture**:
- INT1: Highest priority, can interrupt INT2 and INT3
- INT2: Middle priority, can interrupt INT3 only
- INT3: Lowest priority, can only interrupt main code

**Interrupt Vectors**:
```
$1F0: IJMP3 - INT3 jump address
$1F1: IRET3 - INT3 return address (includes C/Z)
$1F2: IJMP2 - INT2 jump address
$1F3: IRET2 - INT2 return address (includes C/Z)
$1F4: IJMP1 - INT1 jump address
$1F5: IRET1 - INT1 return address (includes C/Z)
```

**Key Instructions**:
- `SETINTx #0-15`: Select event source for interrupt
- `STALLI/ALLOWI`: Global interrupt enable/disable
- `RETIx`: Return from interrupt (CALLD INB,IRETx WCZ)
- `RESIx`: Resume interrupt at next instruction
- `TRGINTx`: Software trigger interrupt
- `NIXINTx`: Cancel pending interrupt

**Branch Conditions**:
Must wait for clean instruction boundary:
- No ALTxx, AUGS, AUGD, REP active
- No XBYTE, GETXACC, SETQ/SETQ2 executing
- Not stalled in WAITx instruction
- STALLI not active

### Debug Interrupt System

**Architecture**:
- Highest priority, overrides INT1/2/3
- Invisible to normal code
- Uses last 16KB hub RAM for state preservation
- Execute-only ROM at $1F8-$1FF for entry/exit

**Features**:
- Register remapping: INA/INB become IJMP0/IRET0 during debug ISR
- Automatic state save: ROM routine saves $000-$00F to hub
- Per-COG debug areas: Each COG gets 128 bytes in upper hub
- Write protection: Debug area can be locked after init

**BRK Instruction Dual Mode**:
- Normal mode: Triggers debug interrupt with 8-bit code
- Debug ISR mode: Configures next debug conditions

---

## Hub Configuration

### HUBSET Instruction Functions

**Clock Generation**:
- RCFAST: 20MHz+ guaranteed (boot default)
- RCSLOW: ~20kHz low power
- Crystal: 10-20MHz with loading caps
- PLL: 1-64 input divider, 1-1024 multiplier
- VCO: 100-200MHz nominal, 350MHz overclock

**System Control**:
- Hard reset (chip reboot)
- Write protection for debug area
- Debug enable per COG
- Filter configuration
- PRNG seeding (Xoroshiro128**)

**Clock Modes**:
```
%CC: Crystal control
  00: Hi-Z (disabled)
  01: 1M-ohm, no caps
  10: 1M-ohm, 15pF caps
  11: 1M-ohm, 30pF caps

%SS: Source select
  00: RCFAST (boot default)
  01: RCSLOW (low power)
  10: XI crystal
  11: PLL output
```

---

## Hub "Egg Beater" Memory Access

### Round-Robin Architecture
- 8 COGs access hub in rotating sequence
- Each COG gets 1/8 of hub bandwidth
- Access window every 8 clocks
- Automatic synchronization
- No arbitration delays for scheduled slot

### FIFO Interface
- 19-stage buffer between COG and hub
- RDFAST/WRFAST instructions for setup
- Automatic RFBYTE/RFWORD/RFLONG operations
- PTRx expressions for complex addressing

---

## CORDIC Solver

### 54-Stage Pipeline
- Fully pipelined operation
- New operation every clock
- 54-clock latency for results
- Supports multiple operations in flight

### Operations
- QMUL: 32×32 multiply
- QDIV: 64÷32 divide
- QFRAC: 32×32 fractional multiply
- QSQRT: 32-bit square root
- QROTATE: Vector rotation
- QVECTOR: Cartesian to polar
- QLOG: Natural logarithm
- QEXP: Exponential

### Result Retrieval
- GETQX: Get X result
- GETQY: Get Y result
- Automatic stall if result not ready

---

## Locks System

### 16 Hardware Locks
- Shared between all COGs
- Atomic test-and-set operations
- No busy-waiting required

### Lock Instructions
- LOCKNEW: Allocate free lock
- LOCKRET: Return lock to pool
- LOCKTRY: Non-blocking acquire
- LOCKREL: Release owned lock

---

## Smart Pins Overview

### 32 Operating Modes

**Repository/DAC Modes (3)**:
- Long repository
- ADC sample repository
- DAC output

**Pulse/NCO Modes (4)**:
- Pulse output
- Transition output
- NCO frequency
- NCO duty

**PWM Modes (3)**:
- Triangle PWM
- Sawtooth PWM
- Switch PWM

**Counting Modes (5)**:
- Count edges
- Count highs
- Count periods
- State counter
- ADC accumulator

**Timing Modes (8)**:
- Time states
- Time high/low states
- Timeout
- Pin-to-pin timing
- Various measurement modes

**ADC Modes (3)**:
- SINC1/SINC2/SINC3 filtering
- Different sample rates

**Serial Modes (5)**:
- Async serial transmit/receive
- Sync serial transmit/receive
- USB host/device

### Smart Pin Features
- Every pin identical capabilities
- 27-bit accumulators
- ±3 pin routing for inputs
- Independent operation from COGs
- 16-bit configuration per pin

---

## Boot Process

### Boot Sequence
1. Check for pull-up on P61 (serial boot)
2. If P61 pulled up: Wait for serial command
3. Check P60 (flash), P59 (SD card)
4. Load from first valid source
5. Execute from hub $00000

### Boot Sources
- **Serial**: Auto-baud detection, plain ASCII protocol
- **Flash**: SPI flash on P61-P58
- **SD Card**: FAT32 boot files

### Checksum Validation
- "Prop" marker at offset 0
- Checksum at offset 4
- Data length at offset 8
- All validated before execution

---

## Serial Loading Protocol

### Protocol Features
- Plain ASCII text-based
- Auto-baud detection (9600 to 2Mbaud)
- Terminal-friendly (visible commands)
- 4 simple commands

### Commands

**Prop_Chk**:
- Response: "Prop_Ver Au" (version A silicon)
- Validates communication

**Prop_Clk**:
- Format: Prop_Clk P1 P2 P3
- P1: 0=RCFAST, 1=RCSLOW, 2=crystal/XI
- P2: Multiply factor (crystal mode)
- P3: Divider (crystal mode)
- Updates system clock

**Prop_Hex**:
- Loads Intel hex format data
- Standard hex record format
- Automatic address handling

**Prop_Txt**:
- Base64 encoded binary
- ~2.25x more efficient than hex
- Uses RFC 4648 alphabet
- Terminal-safe encoding

### Loading Process
1. "> " prompt indicates ready
2. Send command (terminated with CR)
3. "." response indicates processing
4. "?" indicates error
5. Multiple chips supported via INA/INB masking

---

## PASM2 Instruction Set

### Instruction Count
- 169 unique instruction encodings
- Multiple variants per mnemonic (490 total)
- Conditional execution on all instructions

### Instruction Categories

**Memory Operations**:
- RDLONG/WRLONG: Hub long access
- RDWORD/WRWORD: Hub word access
- RDBYTE/WRBYTE: Hub byte access
- RDLUT/WRLUT: LUT access

**Math Operations**:
- ADD/SUB: Basic arithmetic
- MUL/MULS: Multiply operations
- SCA/SCAS: Scale operations
- Various bit operations

**Control Flow**:
- JMP/CALL: Branches
- RET/RETA/RETB: Returns
- REP: Hardware loops
- SKIP/SKIPF/EXECF: Instruction skipping

**Special Operations**:
- ALTx: Register indirection
- XBYTE: Bytecode execution
- CORDIC operations: QMUL/QDIV/QROTATE
- Pixel operations: ADDPIX/MULPIX/BLNPIX

**I/O Operations**:
- DIRx/OUTx/INx: Pin control
- WRPIN/WXPIN/WYPIN: Smart pin control
- TESTP/TESTPN: Pin testing

### Instruction Timing
- Most instructions: 2 clocks
- Hub operations: Variable (depends on hub window)
- CORDIC operations: 54 clocks latency
- Pixel operations: 7 clocks
- Branches: 5+ clocks (pipeline flush)

---

## Key Architectural Features Summary

1. **8 Symmetric COGs**: True parallel processing
2. **Smart Pins**: 64 autonomous I/O processors
3. **Streamer**: NCO-timed DMA engine
4. **CORDIC**: 54-stage math pipeline
5. **XBYTE**: Hardware bytecode engine
6. **Hub Egg Beater**: Deterministic memory access
7. **Events System**: 16 hardware trackers per COG
8. **Pixel Mixer**: Hardware graphics operations
9. **Colorspace Converter**: Real-time video processing
10. **Debug System**: Invisible hardware debugging