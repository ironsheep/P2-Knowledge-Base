# P2 Architecture Topology Map

**Generated**: 2025-09-06T14:50:17.441162

## Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                    P2 Architecture                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐ ┌──────────┐         ┌──────────┐       │
│  │  COG 0   │ │  COG 1   │  . . .  │  COG 7   │       │
│  └────┬─────┘ └────┬─────┘         └────┬─────┘       │
│       │            │                     │             │
│  ┌────┴────────────┴─────────────────────┴──────┐      │
│  │              Hub Memory (512KB)              │      │
│  │         (Egg-beater access rotation)         │      │
│  └───────────────┬──────────────────────────────┘      │
│                  │                                      │
│  ┌───────────────┴──────────────────────────────┐      │
│  │  Shared Resources:                           │      │
│  │  • CORDIC Solver (54-stage pipeline)         │      │
│  │  • 16 Hardware Locks                         │      │
│  │  • Event System                              │      │
│  │  • Streamer/FIFO                             │      │
│  └───────────────┬──────────────────────────────┘      │
│                  │                                      │
│  ┌───────────────┴──────────────────────────────┐      │
│  │         64 Smart Pins (P0-P63)               │      │
│  └───────────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Component Relationships

### Cog
Connects to:
  - Hub RAM
  - Smart Pin System
  - Lock System
  - Event System

### Hub Memory
Connects to:
  - COG Processor
  - FIFO System
  - Streamer

### Cordic
Connects to:
  - COG Processor

### Smart Pins
Connects to:
  - COG Processor
  - Event System

### Streamer
Connects to:
  - Hub RAM
  - FIFO System
  - Smart Pin System

### Fifo
Connects to:
  - Hub RAM
  - Streamer
  - COG Processor

### Events
Connects to:
  - COG Processor
  - Smart Pin System
  - CORDIC Solver

### Locks
Connects to:
  - COG Processor
  - Hub RAM

## Data Flow Paths

1. **Cog ↔ Hub Memory**: Via egg-beater rotation windows
2. **Cog → CORDIC**: Start operations, read results after 54 clocks
3. **Hub Memory → Streamer → Pins**: DMA streaming for video/audio
4. **Pins → Smart Pin → Cog**: Input capture and measurement
5. **Cog ↔ Cog**: Via Hub RAM or ATN events
6. **FIFO ↔ Hub Memory**: Fast sequential access

## Performance Characteristics

- **Cog Execution**: 2 clocks per instruction (pipeline full)
- **Hub Access**: 13-20 clocks (window dependent)
- **FIFO Streaming**: 1 long per clock
- **CORDIC Result**: 54 clocks latency
- **Smart Pin Response**: 2 clocks typical
