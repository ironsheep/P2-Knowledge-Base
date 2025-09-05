# Propeller 2 (P2X8C4M64P) - Unified Authoritative Description

*Synthesized from official Parallax sources: Silicon Doc v35, P2 Datasheet, and P2 Spec Sheet*

## Executive Summary

The Propeller P2X8C4M64P (P2) is a multicore microcontroller with the performance of an MPU, excelling at real-time analog and digital applications. It consists of 8 identical 32-bit processors (called COGs), each capable of deterministic, independent operation while sharing common resources through a central hub.

---

## Core Architecture

### Processing Cores (COGs)
- **8 identical 32-bit processors** operating independently
- **Five-stage pipelined execution** architecture
- **2-clock execution** for most math and logic instructions
- **~350 unique PASM2 instructions** per COG
- **720 MIPs total** (90 MIPs per COG @ 180 MHz)
- **Deterministic timing** - no interrupts disturb execution flow

### Memory Architecture

#### Per-COG Private Memory
- **512 longs (2KB) Register RAM** - Dual-port, primary execution space
- **512 longs (2KB) Lookup RAM** - Dual-port, for code/data/streaming

#### Shared Hub Memory
- **512KB Hub RAM** shared by all COGs
- **32-bits-per-clock** access for each COG simultaneously  
- **720 MB/s per COG** bandwidth @ 180 MHz
- **Last 16KB** write-protectable and mirrored at 1MB boundary
- **Byte/Word/Long** addressable in little-endian format

#### Execution Modes
COGs can execute directly from:
1. **COG Register RAM** (addresses $00000-$001FF) - "COG execution"
2. **COG Lookup RAM** (addresses $00200-$003FF) - "LUT execution"  
3. **Hub RAM** (addresses $00400-$FFFFF) - "Hub execution" via FIFO

---

## Smart Pin System

### 64 Smart I/O Pins
Each pin is independently capable of:
- **Autonomous operation** without COG intervention
- **Hundreds of configurable modes** including:
  - ADC: 14-bit with SINC1/2/3 filtering
  - DAC: 16-bit with 3ns @ 75Ω drive
  - PWM: Triangle/Sawtooth/SMPS modes
  - Serial: UART/USART/SCI/SPI/I²C
  - USB: 12 Mbps host/device
  - Video: VGA/HDMI/HDTV/NTSC/PAL
  - Quadrature decoders
  - Frequency synthesis (NCO)
  - Pulse/transition detection
  - Time measurement
  - Protocol engines

### Pin Capabilities
- **Configurable drive strength**: 1.5kΩ, 15kΩ, 150kΩ, 1mA, 100µA, 10µA
- **Digital filtering** on inputs
- **Comparator modes** with feedback
- **All pins accessible** by every COG

---

## Hub Resources

### CORDIC Math Solver
- **54-stage pipeline** with scale-factor correction
- **8 operations**:
  - Rotate (X,Y) by angle
  - Polar to Cartesian conversion
  - Cartesian to Polar conversion  
  - 32×32 multiply → 64-bit result
  - 64÷32 divide → 32-bit quotient + remainder
  - 64-bit → 32-bit square root
  - Unsigned to logarithm
  - Logarithm to unsigned
- **Shared by all COGs** with pipelined access
- **55 clock latency** with results available to COGs

### System Resources
- **64-bit free-running counter** - increments every clock
- **16 semaphore locks** - atomic operations for COG coordination
- **Xoroshiro128** PRNG - true-random seeded, unique data per COG/pin
- **Streamer engine** per COG for high-speed data movement
- **FIFO hardware** for hub execution and streaming

---

## COG Features

### Per-COG Execution Resources
- **2-clock math/logic** including 16×16 multiply
- **6-clock bytecode executor** for interpreted languages
- **8-level hardware stack** for subroutines
- **Carry and Zero flags**
- **Hidden debug interrupt** for breakpoints and single-stepping

### Event and Interrupt System
- **16 unique event trackers** per COG
- **3 prioritized interrupts** triggered by selectable events
- **COG-to-COG attention signals** for coordination
- **POLLATN/WAITATN** instructions for inter-COG messaging

### Specialized Instructions
- **Pixel operations** with 8:8:8:8 blending
- **Colorspace conversion** via 3×3 matrix
- **Bit manipulation** on spans of bits
- **Pin operations** on spans of pins

### Analog Capabilities (Per COG)
- **4 fast DAC channels** with 16-bit resolution
- **4 fast ADC channels** with scope modes
- **Goertzel analysis** on 4 ADC bit streams

---

## Clocking and Power

### Clock System
- **DC to 320 MHz** operation (180 MHz typical)
- **Fractional PLL** with 3-stage design
- **6 configurable clock modes**
- **Internal ~24 MHz RC oscillator**
- **Internal ~20 kHz RC oscillator**  
- **External crystal/clock input** with programmable loading caps

### Power Architecture
- **Core voltage**: 1.8 VDC
- **I/O voltage**: 3.3 VDC
- **Low-power mode**: ~130 µA
- **Clock gating** reduces active power by ~40%

---

## Physical Specifications

### Package
- **100-pin TQFP** with exposed pad
- **14×14 mm** package size
- **Operating temperature**: -40°C to +105°C
- **Moisture Sensitivity Level**: MSL 3 (168 hours)

### Pin Groups
- **P0-P63**: 64 Smart I/O pins
- **P58-P63**: Boot configuration pins
- **VDD/VSS**: Core power (1.8V)
- **VIO/GIO**: I/O power groups (3.3V)
- **XI/XO**: Crystal oscillator pins
- **RESn**: Active-low reset

---

## Boot System

### Boot Process
1. **3ms after reset**: Bootloader loads into COG 0
2. **Boot sources checked** (P58-P63 configuration):
   - Serial (115,200 baud)
   - SPI Flash  
   - SD Card
3. **User code execution** begins after successful load
4. **Protected boot ROM**: 16KB with debug support

### Programming Interfaces
- **Serial loading** via PropPlug or USB
- **SPI Flash** for field updates
- **SD Card** for removable program storage

---

## Development Ecosystem

### Supported Protocols (Community Libraries)
1-WIRE, CANbus, DVI, HDMI, HDTV, HUB75, HyperFlash/RAM, I²C, QSPI/QSSI, RS485, SCI/SPI, SD CARD, UART/USART, USB 2.0 HOST/SLAVE, VGA, XBEE, and growing

### Programming Languages
- **PASM2**: Native assembly for maximum performance
- **Spin2**: High-level language with inline assembly support
- **C/C++**: Via FlexProp compiler
- **BASIC, Forth, MicroPython**: Community implementations

---

## Key Differentiators

### True Parallel Processing
- **8 independent processors** with no shared execution resources
- **No resource contention** except for hub access slots
- **Deterministic timing** for real-time applications
- **No interrupt latency** affecting critical code

### Smart Pin Autonomy
- **Offload I/O tasks** completely from COGs
- **Complex protocols** without CPU overhead
- **Simultaneous operation** of all 64 pins independently
- **Mixing analog and digital** functions freely

### Symmetric Multiprocessing
- **All COGs are identical** - no master/slave architecture
- **Any COG can control any resource**
- **Democratic hub access** - equal priority for all
- **Start/stop COGs dynamically** as needed

### Real-Time Capabilities
- **Deterministic instruction timing**
- **No cache misses** or pipeline stalls
- **Guaranteed hub access** windows
- **Video generation** while performing other tasks

---

## Compliance and Availability

### Regulatory Compliance
- **RoHS3 Compliant** (EU 2011/65/EU)
- **REACH Compliant** (EU EC 1907/2006)
- **ECCN**: 3A991A2 (EU EAR99)
- **HTSUS**: 8542.31.0001

### Product Information
- **Part Number**: P2X8C4M64P (standard) or P2X8C4M64P-ES (engineering sample)
- **Manufacturer**: Parallax Inc.
- **Documentation**: www.parallax.com/p2

---

*This unified description represents the authoritative specification of the Propeller 2 microcontroller as documented in official Parallax sources.*