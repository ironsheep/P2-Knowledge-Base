# CORDIC Solver

## Overview
P2's CORDIC (COordinate Rotation DIgital Computer) provides hardware-accelerated mathematical operations.

## Operation Categories

### Trigonometric
- `rotate.yaml` - Vector rotation
- `vector.yaml` - Vector to polar conversion
- `sine-cosine.yaml` - Simultaneous sin/cos calculation

### Arithmetic
- `multiply.yaml` - 32x32 to 64-bit multiplication
- `divide.yaml` - 64/32 division with remainder
- `square-root.yaml` - Square root calculation

### Logarithmic
- `log.yaml` - Natural logarithm
- `exp.yaml` - Exponential function

## File Structure
Each operation includes:
- Command encoding
- Cycle count (36-58 cycles typical)
- Input/output specifications
- Precision characteristics
- PASM2 instruction interface (QROTATE, QVECTOR, etc.)
- Usage examples

## Pipeline Characteristics
- Non-blocking operation
- Result retrieval via GETQX/GETQY
- Multiple commands can be queued
- Automatic stall on result read if not ready