# Part I: Smart Pin Fundamentals

## Chapter 1: Smart Pin Architecture

### Overview

The Propeller 2 incorporates 64 Smart Pins, one for each I/O pin. Each Smart Pin contains independent hardware that can be configured to perform one of 32 specialized modes without COG intervention. Once configured, Smart Pins operate autonomously, freeing COG resources for other tasks.

### Smart Pin Block Diagram

![Smart Pin Block Diagram](assets/smart-pins-master-trimmed.png)

**Figure 1.1: Smart Pin Block Diagram**  
*Signal Path for Even/Odd Pin Pairs*  
*Original design and diagram by Chip Gracey, Parallax Inc.*

This comprehensive diagram reveals the sophisticated dual-pin architecture at the heart of P2's Smart Pin system. The diagram shows how even pins (0,2,4...62) and odd pins (1,3,5...63) are organized as pairs with shared resources.

**Understanding This Architecture Diagram:**

The density of this diagram is intentional—it captures every signal path and processing option available in the Smart Pin system. Three key insights emerge:

1. **Pin Pairs Share Resources** - Even/odd pins (like 0-1, 2-3, etc.) share certain hardware blocks, which explains why some operations (like differential signaling) work best on pin pairs.

2. **Three-Layer Processing Architecture**:
   - **Analog Layer** (Yellow/left): Physical pin interface with DACs, ADCs, comparators—where real-world signals meet silicon
   - **Digital Core** (Blue/right): The synthesized logic implementing the 32 operating modes
   - **COG Interface** (Top): How all 8 COGs can stream data to any pin's DAC or exchange data with Smart Pin cores

3. **Flexible Signal Routing** - The PinA/PinB routing system allows any Smart Pin to read from its neighbors (±3 pins), enabling complex multi-pin operations without COG involvement.

**Practical Implications:**

- **Differential Protocols**: Use adjacent pins for best performance
- **Analog Feedback Loops**: Create between pins using internal routing
- **Pin Monitoring**: One pin can watch another's output automatically
- **COG Streaming**: Any COG can drive any pin's DAC directly

This architecture enables capabilities like running USB on one pin pair while simultaneously sampling analog on another, all while a third pair generates precise PWM—with zero COG overhead after configuration.

**Key Architectural Components:**

**Custom I/O Pad Ring (Left Section - Yellow):**
- **Physical Pin Interface**: Direct connection to package pins
- **Flash DAC Network**: 8-bit resistor DAC for analog output
- **Logic Drive**: Digital output driver with selectable drive modes
- **Comparator & Logic & Schmitt**: Input conditioning with analog comparison and Schmitt trigger hysteresis
- **Sigma-Delta ADC**: Analog-to-digital conversion for reading analog signals
- **PinA/PinB Routing**: Flexible input selection from physical pins

**Synthesized Core Logic (Right Section - Blue):**
- **COG_DAC Bus**: All 8 COGs can stream data directly to any Smart Pin's DAC
- **DAC Bus Select**: Multiplexer choosing between COG streamers and Smart Pin DAC
- **Logic Output Block**: Controls digital pin state with enable/output/direction
- **Smart Pin Core (Red Blocks)**: 
  - 32-bit WXPIN/WYPIN/RDPIN interface for COG communication
  - Mode-specific processing logic (%SSSSS_0)
  - Internal state machines for autonomous operation

**Inter-Pin Connectivity:**
- **±3 Pin Access**: Each Smart Pin can read from neighbors
- **Differential Pair Support**: Even/odd pins work together
- **Shared Resources**: Optimized for pin-pair operations

### Hardware Architecture Details

Each Smart Pin consists of:
- **Mode Control Logic**: Determines pin function based on 6-bit mode selection
- **X Register**: 32-bit parameter register (mode-specific function)
- **Y Register**: 32-bit parameter register (mode-specific function)  
- **Z Register**: 32-bit result register (read via RDPIN/RQPIN)
- **Input Selector**: Routes signals from any pin or internal source
- **Output Driver**: Configurable drive strength and modes