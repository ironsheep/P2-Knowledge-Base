# P2 Datasheet Critical Insights
**Document**: High-level architectural insights from P2 Datasheet walkthrough  
**Date**: 2025-09-05

## 🎯 Memory Architecture & Execution Performance

### Three Execution Regions with Vastly Different Characteristics

| Region | Address Range | Width | PC Inc | Branch Cost | Special Constraints |
|--------|--------------|-------|--------|-------------|-------------------|
| Register RAM | $00000-$001FF | 32-bit | 1 | 5 clocks | None - fastest |
| Lookup RAM | $00200-$003FF | 32-bit | 1 | 5 clocks | None - fast |
| Hub RAM | $00400-$7FFFF | 8-bit | 4 | 13+ clocks | FIFO occupied, no streaming |

### Critical Hub Execution Penalties
1. **13+ clock branch penalty** to enter Hub execution (vs 5 for Cog-internal)
2. **FIFO completely dedicated** to instruction fetch - blocks all FIFO operations
3. **Address shadowing** - Hub $00000-$003FF inaccessible (shadowed by Cog RAM)
4. **No auto-transition** - PC wrap at $003FF returns to $00000, not Hub

**Performance Impact**: Hot loops and time-critical code MUST be in Cog RAM (Register or LUT).

## 🎯 Lookup RAM (LUT) - The Swiss Army Knife

### Six Distinct Uses:
1. **Scratch space** - Load/Store architecture (RDLUT/WRLUT)
2. **Streamer source** - Feed DACs, pins, HDMI
3. **Bytecode tables** - For interpreted languages
4. **Smart Pin data** - Direct pin data source
5. **Paired-Cog comm** - Adjacent cogs share LUT (0-1, 2-3, etc.)
6. **Code execution** - Full-speed execution like Register RAM

### Critical Constraints:
- **Dual-port conflict**: Can't use paired-cog sharing AND streamer simultaneously
- **No direct access**: Most instructions need RDLUT/WRLUT (unlike Register RAM)
- **Address mapping**: $200-$3FF in PC space, but $000-$1FF for RDLUT/WRLUT

## 🎯 Pipeline Architecture

### 5-Stage Pipeline Behavior:
- **Normal**: 2 clocks per instruction when pipeline full
- **Stalls cascade**: One stall affects entire pipeline
- **Branches flush**: 5+ clock penalty for first instruction after branch
- **Conditionals free**: Cancelled instructions don't stall

**Optimization Strategy**: Prefer conditional execution over branching.

## 🎯 Cog Control & Coordination

### Starting/Stopping Cogs:
- **Any cog can control any cog** - start, stop, restart (including itself)
- **Dynamic allocation** - Start "free" cogs without knowing IDs
- **Cog pool** - Stopped cogs return to free pool automatically
- **PTRA initialization** - SETQ before COGINIT sets target's PTRA (for startup params)

### Cog Attention System:
- **COGATN instruction** - Signal one or multiple cogs simultaneously
- **8-bit mask** - Each bit corresponds to a cog (0-7)
- **OR'd strobes** - All attention signals combine, each cog sees its own
- **Event detection** - POLLATN/WAITATN/JATN/JNATN instructions
- **Messaging needed** - For multi-source attention, implement Hub RAM protocol

## 🎯 Hub RAM Architecture

### Access Characteristics:
- **Byte-addressable** - No alignment requirements for words/longs
- **Little-endian** format
- **Execution from any address** ≥ $400 (no long-alignment needed)

### Special 16KB Region (Top of Hub):
- **Dual mapping**: Normal address AND $FC000-$FFFFF
- **Boot ROM cache** - ROM loads here on startup
- **Write-protect capable** - Can make it ROM-like
- **Debug space** - Protected RAM for debugger use

### Hub RAM Slicing (Critical for Performance):
- **8 slices** - One per cog on P2X8C4M64P
- **Round-robin access** - Each cog sees next slice each clock
- **Initial wait**: 0-7 clocks to align with target slice
- **Then streaming**: Sequential longs every clock after alignment
- **Every 8th long** - Each slice holds every 8th long in Hub

**Performance Insight**: Once aligned, Hub can stream at full speed (1 long/clock)!

## 🏗️ Architectural Implications for P2 Software Design

### Multi-Cog Architecture Patterns Enabled:
1. **Event-Driven Coordination** - Attention system eliminates Hub polling overhead
   - Master cog signals workers via COGATN
   - Workers WAITATN for tasks
   - No Hub RAM bandwidth wasted on status checks

2. **Dynamic Task Allocation** - Cog pool management
   - Start "free" cogs on demand
   - Self-terminating worker pattern
   - Load balancing across available cogs

3. **Specialized Cog Roles** - Based on memory/execution characteristics
   - **Driver Cogs**: Time-critical I/O in Register RAM
   - **Compute Cogs**: Algorithm kernels in Register+LUT
   - **Manager Cogs**: Orchestration from Hub RAM
   - **Streaming Cogs**: Dedicated FIFO operations

### Data Structure Organization:
1. **Sequential > Random** - Hub slicing favors streaming
   - Arrays/buffers for bulk data
   - Linked structures have variable latency
   - Align data for cog access patterns

2. **Memory Hierarchy Placement**:
   - **Register RAM**: Inner loops, ISRs, critical variables
   - **LUT RAM**: Working buffers, lookup tables, inter-cog mailboxes
   - **Hub RAM**: Program bulk, shared data, message queues

3. **FIFO Awareness**:
   - Can't mix Hub execution with streaming
   - Plan cog roles: executors OR streamers, not both
   - Consider dedicated streaming cogs

### Performance Optimization Strategy:
1. **Minimize Hub execution transitions** (13+ clock penalty)
2. **Keep hot paths in Cog RAM** (2 clock/instruction)
3. **Use conditional execution over branching** (no pipeline flush)
4. **Align Hub data access to slice timing** (stream when possible)
5. **Use Attention for cog coordination** (hardware is faster than polling)

**KEY INSIGHT**: The P2 rewards designs that work WITH its architecture - distributed processing with specialized cogs, streaming data patterns, and hardware-assisted coordination.

## 🎯 FIFO Architecture Details

### FIFO Characteristics:
- **Size**: (#cogs+11) stages = 19 stages on P2X8C4M64P
- **Auto-loading**: Fills when <(#cogs+7) stages full
- **Three exclusive uses**:
  1. Hub execution (PC ≥ $400)
  2. Streamer operations (background DMA)
  3. Software sequential access (RFxxxx/WFxxxx)
- **Can't mix uses** - Choose one mode at a time

### FIFO Setup:
- Must use RDFAST/WRFAST from Cog RAM to establish
- Then can stream or use RF/WF instructions
- Smooths data flow for <32 bits/clock access

## 🎯 Clock System Configuration

### HUBSET Instruction Format:
`##%0000_000E_DDDD_DDMM_MMMM_MMMM_PPPP_CCSS`

### Clock Sources (%SS field):
- %00: RCFAST (20+ MHz minimum, ~24 MHz nominal)
- %01: RCSLOW (~20 kHz low power)
- %10: XI pin direct
- %11: PLL output

### PLL Configuration:
- **VCO range**: 100-200 MHz (critical constraint)
- **Input divider**: /1 to /64 (%DDDDDD)
- **Feedback divider**: /1 to /1024 (%MMMMMMMMMM)
- **Output divider**: /1 to /30 in steps of 2 (%PPPP)
- **Stabilization**: 10ms for crystal+PLL

### Crystal Configuration (%CC field):
- Loading capacitors: Off/15pF/30pF per pin
- 1M-ohm feedback resistor options
- 600-ohm drive strength

## 🔒 Locks System - Hardware Semaphores

### Core Characteristics:
- **16 hardware semaphore bits** - Precious resource, plan carefully
- **Truly symmetric** - Any cog can allocate/acquire/release any lock
- **Pure hardware** - No OS overhead, deterministic timing
- **Auto-cleanup** - Locks release when owner cog stops (prevents deadlock)

### Lock Instructions:
- **LOCKNEW** - Allocate from pool
- **LOCKTRY** - Atomic test-and-set
- **LOCKREL** - Release (owner only)
- **LOCKRET** - Return to pool

### P2 Locks vs Other Systems:
- **No OS kernel** - Pure hardware, no context switches
- **No priority inheritance** - Simple and deterministic
- **Fixed pool of 16** - Forces thoughtful design
- **Auto-release on failure** - Self-healing architecture

## 🎯 Coordination Architecture - The Three Pillars

### 1. Hub RAM - Shared Workspace
- Mailboxes, queues, shared data structures
- Byte-addressable, unaligned access OK

### 2. Locks - Exclusion Mechanism
- Protect shared resources
- Ensure atomic operations
- Coordinate role ownership

### 3. Attention - Signaling Mechanism
- Hardware-level cog-to-cog signals
- No polling overhead
- Event-driven coordination

## 🌐 Community Perspectives

### For Traditional Embedded Engineers:
- **Mental shift**: Event-driven pull model vs interrupt push model
- **Advantage**: Deterministic timing, no ISR overhead
- **Pattern**: Lock+Attention replaces ISR+mutex

### For FPGA/Hardware Designers:
- Think of cogs as state machines
- Locks as hardware semaphore blocks
- Attention as custom signal lines
- Design cog roles like FPGA partitioning

### For Real-Time Systems:
- **Guaranteed determinism** - Calculate exact worst-case
- No priority inversion with locks
- Known Hub access timing (0-7 clocks)
- Suitable for hard real-time

### For Makers/Hobbyists:
- Simple pattern: One lock per shared resource
- Cogs are like Arduino tasks that truly run in parallel
- Start simple, add coordination as needed

### For High-Level Developers:
- Cogs = Web Workers
- Locks = Mutex
- Attention = postMessage
- Hub RAM = SharedArrayBuffer

## 🏗️ Architectural Patterns

### Lock Usage Patterns:
1. **Shared Resource Protection** - SPI/I2C/UART arbitration
2. **Data Structure Guards** - Circular buffers, queues
3. **Role Ownership** - "I'm the display driver" lock
4. **State Machine Coordination** - Boot sequencing

### Lock+Attention Combinations:
1. **Producer/Consumer** - Lock protects buffer, attention signals data ready
2. **Ping-Pong Buffers** - Lock for swap, attention for frame complete
3. **Job Queue** - Lock for queue access, attention for job available
4. **Resource Manager** - Lock for allocation table, attention for requests

### Design Principles:
- **Minimize lock hold time** - Get in, update, get out
- **Document lock purposes** - Clear naming/constants
- **Plan for 16 locks max** - Group related resources
- **Use timeout patterns** - Don't wait forever
- **Leverage auto-release** - Design for self-healing

## 🚀 The P2 Advantage

**"Cooperative Autonomy" Model:**
- 8 identical, independent processors
- Hardware coordination primitives
- No OS overhead or complexity
- Deterministic, predictable timing
- Self-healing from failures

This enables parallel processing patterns that are difficult or impossible on traditional architectures, with timing guarantees suitable for hard real-time systems.

## 🧮 CORDIC Solver - Shared Math Engine

### Architecture:
- **54-stage pipeline** - Deep pipeline for complex operations
- **Shared resource** - One CORDIC engine serves all 8 cogs
- **Non-blocking** - Each cog's operations isolated from others
- **Hub-synchronized** - One operation per hub window (every 8 clocks)

### Eight Operations Available:
1. **Multiply** - 32×32 unsigned → 64-bit product
2. **Divide** - 64÷32 unsigned → 32-bit quotient + remainder
3. **Square Root** - √64-bit → 32-bit result
4. **Rotation** - Rotate (X,Y) by angle → new (X,Y)
5. **Cartesian→Polar** - (X,Y) → (length, angle)
6. **Polar→Cartesian** - (length, angle) → (X,Y)
7. **Integer→Log** - 32-bit → 5.27 logarithm
8. **Log→Integer** - 5.27 logarithm → 32-bit

### Critical Timing:
- **Issue rate**: One operation per 8 clocks (hub window)
- **Latency**: 55 clocks to result
- **Throughput**: Up to 1 result per 8 clocks when pipelined
- **Result retrieval**: Must get result on time or it's overwritten!

### Instructions:
- **Issue**: QMUL, QDIV, QFRAC, QSQRT, QROTATE, QVECTOR, QLOG, QEXP
- **Retrieve**: GETQX (lower/X/primary), GETQY (upper/Y/secondary)
- **Setup**: SETQ often precedes to provide second operand

### Architectural Implications:

**1. Pipeline Interleaving Pattern:**
```
Clock 0:   Issue op1        
Clock 8:   Issue op2
Clock 16:  Issue op3
...
Clock 55:  Get op1 result, Issue op8
Clock 63:  Get op2 result, Issue op9
```
Achieve continuous math at 1 result per 8 clocks!

**2. Shared but Non-Blocking:**
- Each cog gets fair access (round-robin via hub windows)
- No cog can monopolize the CORDIC
- Operations don't interfere between cogs
- But within a cog, must manage pipeline carefully

**3. Result Overwrite Hazard:**
- **CRITICAL**: Results must be retrieved when ready
- If you issue another operation, previous result is lost
- Can't "queue up" results - it's use-it-or-lose-it

### Use Case Patterns:

**DSP/Signal Processing:**
- Continuous multiply-accumulate via pipelined QMULs
- Complex number operations (rotation, polar conversion)
- FFT butterflies using rotate operations

**Graphics/Gaming:**
- 2D rotation for sprites
- Polar coordinates for circular motion
- Distance calculations (vector length)

**Control Systems:**
- Logarithmic scaling for PID controllers
- Square root for RMS calculations
- Angle calculations for motor control

**Scientific Computing:**
- High-precision math without software libraries
- Coordinate transformations
- Trigonometric operations via rotation

### Design Considerations:

**When to use CORDIC:**
- Complex math that would take many instructions
- Need deterministic timing (always 55 clocks)
- Can pipeline multiple operations

**When NOT to use CORDIC:**
- Simple operations (basic add/subtract)
- Can't wait 55 clocks for result
- Random access pattern prevents pipelining

**Optimization Strategy:**
- Batch similar operations for pipelining
- Interleave CORDIC ops with other work during 55-clock wait
- Dedicate a cog for math-intensive streaming operations

**Key Insight:** The CORDIC is like a math coprocessor shared via time-division multiplexing. Design your algorithms to stream operations through it rather than random one-off calculations.

---
*This document captures critical performance and architectural insights for P2 development*