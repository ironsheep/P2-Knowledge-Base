# P2 Datasheet - Narratives Around Diagrams

## Smart Pin Control Architecture

### Bus Architecture
- **34-bit input bus** from cogs to each smart pin
- **33-bit output bus** from each smart pin to cogs
- All cog inputs are **OR'd together** (like DIR/OUT bits)
- **Bus conflict warning**: Multiple cogs must access at different times

### Control Instructions (2-clock each)
- **WRPIN D/#,S/#**: Set smart pin mode, acknowledge pin
- **WXPIN D/#,S/#**: Set parameter X, acknowledge pin
- **WYPIN D/#,S/#**: Set parameter Y, acknowledge pin
- **RDPIN D,S/# {WC}**: Read result Z into D, flag into C, acknowledge pin
- **RQPIN D,S/# {WC}**: Read result Z into D, flag into C, NO acknowledge (safe for multi-cog)
- **AKPIN S/#**: Acknowledge pin only

### Event Signaling
- Smart pin raises **IN signal** when:
  - New data is ready
  - New data can be loaded
  - Process has finished
- Cog tests with **TESTP** instruction
- Acknowledgment via WRPIN/WXPIN/WYPIN/RDPIN/AKPIN clears IN
- **2-clock delay** after acknowledgment before IN can be polled again

### Smart Pin Reset
- **Quick reset**: Clear then set DIR bit (maintains configuration)
- **Full reset**: WRPIN #0,pin (returns to normal I/O mode)

## I/O Pin Circuit Key Behaviors

### Pin Pairing and 'OTHER' Signal
- **Adjacent pairs**: P0↔P1, P2↔P3, P4↔P5, etc.
- **Odd pins**: OTHER = even pin's inverted output (differential signaling)
- **Even pins**: OTHER = hardware random bit (noise/dithering source)

### Smart Pin Output Override Hierarchy
1. **Smart OFF + Non-DAC**: DIR enables, OUT or OTHER drives
2. **Smart OFF + DAC Mode**: Complex DAC/ADC control via mode bits
3. **Smart ON**: Smart pin overrides DIR, controls output enable
4. **BIT_DAC**: Special mode for high/low DAC patterns

### DAC Mode Special Behavior (M[12:10] = %101)
- **BIT_DAC**: Outputs {2{M[7:4]}} for high, {2{M[3:0]}} for low
- Four sub-modes controlled by additional bits:
  - DIR-controlled DAC with M[7:0] level
  - OUT-controlled ADC with cog DAC channel select
  - OUT/OTHER driving BIT_DAC patterns

## Communication Mode Insights

### USB Modes (Modes 20-23)
- **Even/odd pin pairs** used as DM/DP (D-/D+)
- Separate modes for:
  - Host low-speed (1.5 Mbps)
  - Host full-speed (12 Mbps)
  - Device low-speed
  - Device full-speed

### Serial Modes (Modes 24-27)
- **Synchronous**: A pin = data, B pin = clock
  - Separate TX and RX modes
- **Asynchronous**: Baud rate based
  - Separate TX and RX modes
  - Up to clock/3 baud rate

### ADC Modes (Modes 28-31)
- **Sample/filter/capture**:
  - Internal clock vs external clock
  - SINC2/SINC3 filtering options
- **Scope modes**:
  - Internal trigger
  - External trigger
  - Oscilloscope-like functionality

## Key Architectural Insights

### Multi-Layer Control
The pin behavior is determined by:
1. **Mode bits** (M[12:0]) - basic pin configuration
2. **Smart mode** (%SSSSS) - autonomous functionality
3. **DIR/OUT bits** - traditional I/O control
4. **Smart pin state** - X, Y, Z parameters
5. **Adjacent pin** - for differential/paired operations

### Hardware Acceleration Features
- **Differential signaling**: Built into odd/even pairs
- **Hardware noise**: Pseudo-random generator per even pin
- **Autonomous operation**: Smart pins run without CPU intervention
- **Multi-cog coordination**: OR'd buses allow shared control

### Power and Analog Considerations
- Each pin powered from its **local Vxxyy** supply
- Groups of 4 pins share supply for **isolated domains**
- ADC can sample own group's supply for **calibration**
- DAC and ADC modes can **coexist** on same pin

## Missing Diagram Analysis Areas
*These sections have diagrams in the original but only narrative text extracted:*
1. Equivalent Schematics for Pin Configurations
2. Timing diagrams for I/O operations
3. USB signaling diagrams
4. Serial communication timing
5. ADC/DAC circuit details
6. Smart pin state machines

---
*This document captures the narrative descriptions around circuit diagrams from the P2 datasheet extraction*