# P2 Architecture Components

## Overview
Detailed specifications for P2's architectural components and systems.

## Component Categories

### Core Architecture
- `cog-system.yaml` - 8-cog multiprocessor architecture
- `hub-memory.yaml` - 512KB hub RAM system
- `hub-execution.yaml` - Hub execution mode (hubexec)
- `pipeline.yaml` - Instruction pipeline details

### Memory Systems
- `cog-ram.yaml` - 512 longs of cog RAM
- `lut-memory.yaml` - 512 longs of lookup table RAM
- `memory-map.yaml` - Complete memory organization
- `special-registers.yaml` - System register definitions

### Timing and Synchronization
- `clock-system.yaml` - Clock generation and PLLs
- `hub-timing.yaml` - Hub window and egg beater
- `instruction-timing.yaml` - Execution timing rules

### Inter-Cog Communication
- `locks.yaml` - 16 semaphore locks
- `events.yaml` - Event system
- `interrupts.yaml` - Interrupt handling

## YAML Schema
Architecture files include:
- Specifications
- Block diagrams (referenced)
- Programming model
- Timing characteristics
- Related components
- Usage examples