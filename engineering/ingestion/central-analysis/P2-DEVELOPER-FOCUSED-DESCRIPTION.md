# Propeller 2 - Developer-Focused Description

*Essential P2 architecture and capabilities for software developers*

## What is the Propeller 2?

The Propeller 2 (P2X8C4M64P) is a symmetric multicore microcontroller featuring **8 identical 32-bit processors** (COGs) that execute independently while sharing common resources. Unlike traditional microcontrollers, the P2 provides true parallel processing with deterministic timing, making it ideal for real-time applications that need to handle multiple tasks simultaneously.

## Core Architecture

### 8 Independent Processors (COGs)
- **True parallel execution** - All 8 COGs run simultaneously at full speed
- **90 MIPs per COG** (720 MIPs total @ 180 MHz)  
- **No resource contention** - Each COG has its own registers and memory
- **Deterministic timing** - No interrupts or cache misses affecting execution
- **Democratic architecture** - Any COG can start/stop any other COG

### Memory Model

**Per-COG Private Memory:**
- **2KB Register RAM** - Fast execution and data storage
- **2KB Lookup RAM** - Code, data tables, and streaming buffers

**Shared Hub Memory:**
- **512KB Hub RAM** accessible by all COGs
- **32 bits per clock** bandwidth for each COG
- **Equal access** - Every COG gets guaranteed hub windows
- **Execute from anywhere** - COGs can run code from their own RAM or Hub RAM

**Memory Map:**
```
$00000-$001FF  COG Register RAM (COG execution)
$00200-$003FF  COG Lookup RAM (LUT execution)  
$00400-$FFFFF  Hub RAM (Hub execution)
```

## Smart Pin System

### Autonomous I/O Processing
The P2's revolutionary Smart Pin system provides **64 independent I/O pins**, each capable of complex operations without using COG resources:

**Key Capabilities:**
- **Serial protocols**: UART, SPI, I²C automatically handled
- **PWM generation**: Motor control, LED dimming, audio
- **ADC/DAC**: 14-bit ADC, 16-bit DAC per pin
- **Quadrature decoding**: Direct encoder interfacing
- **USB host/device**: 12 Mbps communication
- **Video generation**: VGA, HDMI, composite video

**Developer Impact:** Offload entire I/O tasks to Smart Pins, freeing COGs for application logic.

## Programming Model

### Instruction Set (PASM2)
- **~350 unique instructions** optimized for real-time control
- **2-clock execution** for most instructions
- **Single-cycle multiply** (16×16 bits)
- **Specialized operations**: Bit manipulation, pixel blending, CORDIC math

### Development Languages
- **Spin2**: High-level language designed for P2, with inline PASM2 support
- **PASM2**: Native assembly for maximum performance
- **C/C++**: Via FlexProp compiler with full P2 feature access
- **MicroPython, BASIC, Forth**: Community implementations

### Inter-COG Communication
- **Shared Hub RAM** for data exchange
- **16 hardware locks** for synchronization
- **Attention signals** for event notification
- **Adjacent COG LUT sharing** for high-speed data transfer

## Key Developer Features

### Hardware Math Acceleration (CORDIC)
54-stage pipelined solver shared by all COGs:
- Multiply, divide, square root
- Trigonometric functions (rotate, sin, cos)
- Logarithms and exponentials
- Coordinate conversions (polar ↔ cartesian)

### Event System
Each COG has **16 event detectors** monitoring:
- Pin state changes
- Timer matches
- Pattern detection
- Inter-COG signals

### Streaming Engine
High-speed data movement without CPU overhead:
- Hub RAM ↔ Pins
- LUT RAM ↔ Pins  
- Automatic pixel formatting
- Colorspace conversion

### Debug Support
- Hardware single-stepping
- Breakpoints
- Real-time state inspection
- No debug pods required

## Real-World Application Patterns

### Parallel Task Allocation
```
COG 0: Main application logic
COG 1: USB communication handler
COG 2: Display driver (VGA/HDMI)
COG 3: Motor control loop
COG 4: Sensor data acquisition
COG 5: Signal processing (using CORDIC)
COG 6: Network stack
COG 7: Debug monitor
```

### Deterministic Timing Example
```pasm2
' Generate precise 1MHz square wave
loop    drvnot  #0          ' Toggle pin 0 (2 clocks)
        waitx   #48         ' Wait 48 clocks
        jmp     #loop       ' Jump back (4 clocks)
' Total: 54 clocks = 1MHz @ 180MHz clock
```

### Smart Pin Configuration
```spin2
' Configure pin 0 as UART transmit, 115200 baud
pinstart(0, P_ASYNC_TX | P_OE, 115_200, %0000)
wypin(0, "H")  ' Send 'H' - Smart Pin handles timing
```

## Why P2 for Your Project?

### True Parallel Processing
- **No task scheduling overhead** - COGs run independently
- **No interrupt latency** - Deterministic response times
- **No resource conflicts** - Each COG has private resources

### Simplified Development
- **Offload I/O completely** to Smart Pins
- **Mix languages** - Spin2 for logic, PASM2 for speed
- **No RTOS needed** - Hardware handles parallelism

### Real-Time Guarantees
- **Predictable execution** - Count cycles exactly
- **Guaranteed hub access** - No bus arbitration delays
- **Jitter-free operation** - Perfect for signal generation

### Flexible Architecture
- **Start COGs as needed** - Dynamic processor allocation
- **Any COG can do anything** - No dedicated roles
- **Scale from 1 to 8 COGs** - Use only what you need

## Getting Started

The P2 excels at applications requiring:
- Multiple simultaneous real-time tasks
- Mixed signal processing (analog + digital)
- Complex I/O without CPU overhead
- Deterministic timing requirements
- Video generation with computation

**Next Steps:**
- Explore the [PASM2 Instruction Set](../reference/pasm2/)
- Learn [Spin2 Programming](../developer-docs/spin2/)
- Review [Smart Pin Modes](../reference/smart-pins/)
- Join the [P2 Community Forum](https://forums.parallax.com/categories/propeller-2)

---

*This developer-focused description covers approximately 75% of the complete P2 specifications, emphasizing software development capabilities while omitting physical, electrical, and compliance details.*