# Smart Pins Subsystem

## Overview
P2's 64 smart pins provide autonomous I/O processing capabilities with 30+ operational modes.

## File Organization
Each smart pin mode gets its own YAML file:
- `mode-00-off.yaml` - Smart pin disabled
- `mode-01-dac-noise.yaml` - DAC noise generator
- `mode-02-dac-16bit-dither.yaml` - 16-bit DAC with dithering
- ... (one file per mode)

## Mode Categories

### Analog Modes
- DAC output modes
- ADC input modes
- Comparator modes
- Sigma-delta modes

### Digital Timing
- Pulse generation
- PWM output
- Frequency measurement
- Period measurement

### Serial Communication
- Asynchronous serial
- Synchronous serial
- SPI modes
- I2C support

### Special Functions
- USB support
- Quadrature encoder
- Edge detection
- State machines

## Configuration Schema
Each mode file includes:
- Mode number and name
- Configuration bit patterns
- Timing specifications
- Pin pairing requirements
- Usage examples
- Related PASM2 instructions (WRPIN, RDPIN, etc.)