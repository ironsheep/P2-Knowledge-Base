# P2 Components

## Overview
Specialized subsystems and components that provide P2's advanced capabilities.

## Component Categories

### Smart Pins (`smart-pins/`)
- 64 independent smart pins
- 30+ operational modes
- Autonomous signal generation and measurement
- See `smart-pins/README.md` for details

### CORDIC Solver (`cordic/`)
- Hardware math coprocessor
- Trigonometric, logarithmic, and arithmetic operations
- 32-bit and 64-bit operations
- See `cordic/README.md` for details

### Streamers
- `streamer.yaml` - DMA streaming engine
- `fifo.yaml` - FIFO buffer system
- `colorspace.yaml` - Color space converter

### Signal Generation
- `dac.yaml` - Digital-to-analog converters
- `adc.yaml` - Analog-to-digital converters
- `nco.yaml` - Numerically controlled oscillators

### Debug Support
- `debug.yaml` - Debug interrupt system
- `trace.yaml` - Execution trace capabilities

## YAML Schema
Component files include:
- Functional specifications
- Configuration registers
- Operational modes
- Timing characteristics
- Usage examples
- Related instructions