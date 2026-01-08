# P1 vs P2 Feature Comparison

**Created**: 2025-01-06  
**Purpose**: Comprehensive comparison of Propeller 1 (P8X32A) and Propeller 2 (P2X8C4M64P) specifications  
**Status**: AUTHORITATIVE - Derived from official Parallax documentation  
**Use Case**: Reference for PASM2 manual "What's New in P2" section and P1→P2 migration guides

---

## Executive Summary

The Propeller 2 represents a generational leap from the Propeller 1, with significant improvements across all dimensions while maintaining the core 8-cog symmetric multiprocessor architecture that defines the Propeller family.

| Metric | P1 | P2 | Improvement |
|--------|----|----|-------------|
| Clock Speed | 80 MHz max | 320 MHz max | **4x** |
| I/O Pins | 32 | 64 Smart Pins | **2x + Smart** |
| Hub RAM | 32 KB | 512 KB | **16x** |
| Cog RAM | 2 KB | 4 KB (2 KB + 2 KB LUT) | **2x** |
| MIPS | 160 total | 1,280 total @ 320 MHz | **8x** |
| ADC | None | 64x 14-bit | **New** |
| DAC | None | 64x 16-bit | **New** |
| Math Engine | None | CORDIC (54-stage) | **New** |

---

## Core Architecture Comparison

### Processor Cores (Cogs)

| Feature | P1 (P8X32A) | P2 (P2X8C4M64P) |
|---------|-------------|-----------------|
| **Number of Cogs** | 8 symmetric 32-bit[^1] | 8 symmetric 32-bit[^2] |
| **Cog Independence** | Fully independent[^1] | Fully independent[^2] |
| **Hub Access** | Round-robin, 16 cycles window[^3] | Round-robin, 8 cycles window[^4] |
| **Instruction Width** | 32-bit fixed[^1] | 32-bit fixed[^2] |
| **Pipeline** | 4-stage[^1] | 5-stage with 2-clock throughput[^4] |

### Clock System

| Feature | P1 | P2 |
|---------|----|----|
| **Maximum Clock** | 80 MHz[^3] | 320 MHz (extended)[^5] |
| **Typical Operating** | 80 MHz[^3] | 180 MHz[^5] |
| **Internal RC Fast** | ~12 MHz[^3] | ~24 MHz[^5] |
| **Internal RC Slow** | ~20 kHz[^3] | ~20 kHz[^5] |
| **PLL Multiplication** | 1x-16x[^3] | Fractional, 3-stage[^5] |
| **Crystal Range** | 4-8 MHz (with PLL)[^3] | Configurable[^5] |
| **Clock Modes** | 8 modes[^1] | 6 modes (32-bit each)[^5] |

### Performance Metrics

| Metric | P1 | P2 |
|--------|----|----|
| **Total MIPS @ Max Clock** | 160 MIPS (20/cog)[^3] | 1,280 MIPS (160/cog) @ 320 MHz[^5] |
| **Total MIPS @ Typical** | 160 MIPS @ 80 MHz[^3] | 720 MIPS (90/cog) @ 180 MHz[^5] |
| **Hub Access Speed** | ~2.5 MB/s/cog @ 80 MHz[^1] | 720 MB/s/cog @ 180 MHz[^5] |
| **Instructions/Clock** | 0.25 (4-clock)[^1] | 0.5 (2-clock pipeline)[^4] |

---

## Memory Architecture

### Hub Memory (Shared)

| Feature | P1 | P2 |
|---------|----|----|
| **Hub RAM Size** | 32 KB[^3] | 512 KB[^5] |
| **Hub ROM Size** | 32 KB[^1] | ROM in upper 16 KB region[^4] |
| **Total Main Memory** | 64 KB[^3] | 512 KB+ (with ROM overlay)[^5] |
| **Address Range** | $0000-$FFFF[^1] | $00000-$7FFFF[^4] |
| **Memory Width** | Byte-addressable[^1] | Byte-addressable[^4] |
| **Alignment** | Long-aligned for longs[^1] | No alignment required[^4] |

### Cog Memory (Private per Cog)

| Feature | P1 | P2 |
|---------|----|----|
| **Register RAM** | 512 longs (2 KB)[^1] | 512 longs (2 KB)[^4] |
| **Lookup RAM (LUT)** | None | 512 longs (2 KB)[^4] |
| **Total Cog Memory** | 2 KB[^1] | 4 KB (Register + LUT)[^4] |
| **Register Address Range** | $000-$1EF general, $1F0-$1FF special[^1] | $000-$1EF general, $1F0-$1FF special[^4] |
| **LUT Address Range** | N/A | $200-$3FF[^4] |
| **LUT Sharing** | N/A | Adjacent cog pairs can share[^4] |

### ROM Contents

| Content | P1 | P2 |
|---------|----|----|
| **Boot Loader** | Yes[^1] | Yes (includes P2 Monitor, TAQOZ)[^4] |
| **Interpreter** | Spin interpreter[^1] | Spin2 interpreter[^2] |
| **Character Set** | 256 chars, 16x32 pixels[^1] | Enhanced character set[^2] |
| **Math Tables** | Log, antilog, sine[^1] | Available via CORDIC[^4] |

---

## I/O Architecture

### Pin Count and Organization

| Feature | P1 | P2 |
|---------|----|----|
| **Total I/O Pins** | 32 (P0-P31)[^3] | 64 (P0-P63)[^5] |
| **Pin Architecture** | General-purpose I/O[^1] | Smart Pins (autonomous)[^5] |
| **Pins per Register** | 32 (single DIRA/OUTA/INA)[^1] | 32+32 (A/B pairs)[^4] |
| **Boot Pins** | P28-P31 (I2C/Serial)[^3] | P58-P63 (configurable)[^4] |

### Pin Electrical Characteristics

| Feature | P1 | P2 |
|---------|----|----|
| **I/O Voltage** | 3.3V (2.7-3.6V range)[^3] | 3.3V (I/O)[^5] |
| **Core Voltage** | 3.3V (same as I/O)[^3] | 1.8V (separate from I/O)[^5] |
| **Current per Pin** | 40 mA source/sink[^3] | Configurable drive[^5] |
| **Logic Levels** | CMOS (0.3/0.6 VDD)[^3] | CMOS compatible[^5] |
| **ESD Protection** | 8 kV (HBM)[^3] | Protected[^5] |
| **Drive Modes** | Push-pull only[^1] | 1.5k, 15k, 150k, 1mA, 100µA, 10µA[^5] |

### Smart Pins (P2 Only)

The P2 introduces **Smart Pins** - each of the 64 I/O pins contains autonomous hardware that can execute complex functions independently.[^5]

| Smart Pin Feature | P1 Equivalent | P2 Capability |
|-------------------|---------------|---------------|
| **ADC** | None | 14-bit, multiple modes (Delta-Sigma, SINC1/2/3, Scope)[^5] |
| **DAC** | None | 16-bit, 3 ns, 75 ohm[^5] |
| **PWM** | Software-generated | Hardware: Triangle, Sawtooth, SMPS[^5] |
| **Quadrature** | Software decode | Hardware decoder[^5] |
| **Serial** | Software bitbang | Hardware UART/SPI/I2C[^5] |
| **USB** | Not supported | 12 Mbps[^5] |
| **Digital Filter** | None | Hardware input filter[^5] |
| **Comparator** | None | With feedback modes[^5] |

---

## Hardware Peripherals

### Counter/Timer System

| Feature | P1 | P2 |
|---------|----|----|
| **Counters per Cog** | 2 (CTRA/CTRB)[^1] | 28 counter modes[^5] |
| **Global Counter** | 32-bit system counter[^1] | 64-bit hub global counter[^5] |
| **Counter Modes** | ~8 modes[^1] | 28 modes per cog[^5] |
| **Event/Timer Modes** | Limited[^1] | 16 per cog[^5] |

### Math/CORDIC Engine

| Feature | P1 | P2 |
|---------|----|----|
| **Hardware Math** | None | CORDIC solver (54-stage pipeline)[^5][^4] |
| **Multiply** | Software or 1-clock MUL[^1] | 32×32→64 bit hardware[^4] |
| **Divide** | Software[^1] | 64÷32 hardware[^4] |
| **Square Root** | Software/table lookup[^1] | Hardware √64-bit[^4] |
| **Rotation** | Software[^1] | Hardware (X,Y) rotation[^4] |
| **Polar/Cartesian** | Software[^1] | Hardware conversion[^4] |
| **Log/Exp** | ROM table lookup[^1] | Hardware 5.27 format[^4] |
| **Trig Functions** | ROM sine table[^1] | Hardware SIN, LOG, TAN, ARC[^5] |

### Video Generation

| Feature | P1 | P2 |
|---------|----|----|
| **Video Generator** | 1 per cog (VCFG/VSCL/WAITVID)[^1] | Enhanced per-cog capability[^5] |
| **Analog Video** | RGB VGA, Composite NTSC/PAL[^1] | VGA, HDTV, NTSC, PAL[^5] |
| **Digital Video** | None | HDMI 480p@60fps, 720p@24fps[^5] |
| **Color Depth** | 4-bit (16 colors from 64)[^1] | Enhanced via DAC/Streamer[^5] |

### Interrupts and Events

| Feature | P1 | P2 |
|---------|----|----|
| **Interrupts per Cog** | None (polling model)[^1] | 3 per cog[^5] |
| **Event Sources** | N/A | 16 per cog[^5] |
| **Debug Interrupt** | None | Single-stepping, breakpoint[^5] |
| **Cog Attention** | None | COGATN signaling system[^4] |

### Synchronization

| Feature | P1 | P2 |
|---------|----|----|
| **Hardware Locks** | 8 semaphore bits[^1] | 16 atomic locks[^5] |
| **Lock Instructions** | LOCKNEW/LOCKRET/LOCKSET/LOCKCLR[^1] | LOCKNEW/LOCKTRY/LOCKREL/LOCKRET[^4] |
| **Inter-Cog Signaling** | Via Hub memory only[^1] | COGATN hardware attention[^4] |

---

## Streaming and DMA (P2 Only)

The P2 introduces dedicated streaming hardware not present in P1.[^4]

| Feature | Description |
|---------|-------------|
| **FIFO** | 19-stage automatic buffer[^4] |
| **Streamer** | Background DMA for Hub↔LUT↔Pins[^4] |
| **XBYTE** | 8-clock bytecode execution engine[^4] |
| **Auto-loading** | Automatic FIFO refill[^4] |
| **Hub Slicing** | 8 slices for 1-long/clock throughput[^4] |

---

## Package Options

### P1 Packages

| Package | Part Number | Pins | Size |
|---------|-------------|------|------|
| DIP | P8X32A-D40 | 40 | Through-hole[^3] |
| LQFP | P8X32A-Q44 | 44 | SMD[^3] |
| QFN | P8X32A-M44 | 44 | SMD[^3] |

### P2 Packages

| Package | Part Number | Pins | Size |
|---------|-------------|------|------|
| TQFP | P2X8C4M64P | 100 | 14×14 mm exposed-pad[^5] |

---

## Power Characteristics

| Characteristic | P1 | P2 |
|----------------|----|----|
| **Core Voltage** | 3.3V (VDD)[^3] | 1.8V[^5] |
| **I/O Voltage** | 3.3V (same as core)[^3] | 3.3V[^5] |
| **VDD Range** | 2.7V - 3.6V[^3] | TBD[^5] |
| **Low Power Mode** | ~600 nA (quiescent)[^3] | ~130 µA[^5] |
| **Power per MIPS** | ~500 µA/MIPS[^1] | Improved efficiency[^5] |
| **Operating Temp** | -55°C to +125°C[^3] | -40°C to +105°C[^5] |

---

## Programming Model Differences

### Instruction Set

| Aspect | P1 (PASM1) | P2 (PASM2) |
|--------|------------|------------|
| **Total Instructions** | ~60 opcodes[^1] | ~300+ opcodes[^2] |
| **Conditional Execution** | All instructions[^1] | All instructions[^2] |
| **Effects** | WC, WZ, WR, NR[^1] | WC, WZ, WCZ, ANDC, etc.[^2] |
| **Addressing Modes** | Register, Immediate[^1] | Register, Immediate, PTRx, Indirect[^4] |
| **Hub Access** | RDBYTE/WORD/LONG[^1] | RDBYTE/WORD/LONG + FIFO ops[^4] |
| **LUT Access** | N/A | RDLUT/WRLUT[^4] |
| **Register Indirection** | None | ALTS/ALTD/ALTR/ALTB[^4] |
| **Instruction Skipping** | None | SKIP/SKIPF/EXECF[^4] |

### High-Level Language

| Aspect | P1 (Spin) | P2 (Spin2) |
|--------|-----------|------------|
| **Block Designators** | CON, VAR, OBJ, PUB, PRI, DAT[^1] | Same + enhanced[^2] |
| **Inline Assembly** | DAT section only[^1] | ORG/END inline in methods[^2] |
| **Debugging** | Limited[^1] | Enhanced DEBUG directive[^2] |
| **Smart Pin Access** | N/A | Native PINREAD/PINWRITE/etc.[^2] |

---

## Migration Considerations

### Preserved Concepts (P1 → P2)

1. **8-Cog Architecture**: Same symmetric multiprocessor model
2. **Hub/Cog Memory Model**: Shared hub, private cog RAM
3. **Round-Robin Hub Access**: Deterministic timing (faster in P2)
4. **Wired-OR I/O**: Prevents electrical contention
5. **Lock Mechanism**: Hardware semaphores (more in P2)
6. **Spin/PASM Duality**: High-level and assembly languages

### New P2 Concepts (Not in P1)

1. **Smart Pins**: Autonomous I/O with ADC/DAC/protocols
2. **Lookup RAM (LUT)**: Second 2 KB per cog
3. **CORDIC Engine**: Hardware math acceleration
4. **Streamer/FIFO**: DMA and streaming operations
5. **Interrupts**: 3 per cog with 16 event sources
6. **Cog Attention**: Hardware inter-cog signaling
7. **Register Indirection**: ALTS/ALTD addressing
8. **Instruction Skipping**: SKIP/SKIPF/EXECF flow control
9. **XBYTE**: Bytecode execution engine
10. **Enhanced Hub Access**: Slicing, faster throughput

### Removed/Changed P1 Features

1. **Video Generator Registers**: Different approach in P2
2. **Counter Modes**: Expanded but different organization
3. **ROM Tables**: Replaced by CORDIC operations
4. **Boot Process**: Different boot pin assignments

---

## Source References

[^1]: P1 Propeller Manual v1.2 (2011-06-14) - Official Parallax P1 software reference. `sources/p1-propeller-manual-v1.2/`

[^2]: Spin2 Documentation v51 (2025-07-30) - Official Parallax Spin2 language reference. `sources/spin2-v51/`

[^3]: P1 Datasheet v1.4.0 (2011-06-14) - Official Parallax P1 hardware specifications. `sources/p1-datasheet-v1.4/`

[^4]: P2 Silicon Documentation v35 (2020-10-15) - Chip Gracey's P2 architecture reference. `sources/silicon-doc/`

[^5]: P2 Spec Sheet (2021-10-13) - Official Parallax P2 specifications summary. `sources/p2-spec-sheet/`

[^6]: P2 Datasheet (2022-11-01) - Official Parallax P2 hardware datasheet. `sources/p2-datasheet/`

---

## Document Usage

This comparison serves as:

1. **PASM2 Manual Reference**: "What's New in P2" content source
2. **Migration Guide Foundation**: P1→P2 porting assistance
3. **Feature Discovery**: Quick lookup of P2 enhancements
4. **Architecture Understanding**: Side-by-side capability analysis

---

*This document synthesizes information from authoritative Parallax sources ingested into the P2 Knowledge Base. All specifications are derived from official documentation.*
