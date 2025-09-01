# P2docs.github.io - Main Page Import

**Source**: https://p2docs.github.io/
**Import Date**: 2025-08-15
**Purpose**: Community-driven P2 technical documentation for video/emulation projects

## Site Overview

IRQsoft Propeller 2 Docs - Unofficial documentation page for the Propeller 2 microcontroller.

### Key Features
- HyperJump search technology
- Community-driven via GitHub contributions
- Comprehensive technical specifications

## What's a Propeller 2?

The _Propeller 2_ is a high-performance microcontroller developed by Parallax Inc.

### Technical Specifications:

**Performance:**
- High Speed (180 MHz spec, 320+MHz overclock easily attainable)

**Processing:**
- 8 CPU cores
- Custom RISC-ish architecture
- 2 cycles for ALU instructions (including 16x16 multiply)

**Memory Architecture:**
- 512x32 bits of "Cog RAM" (used as register file)
- 512x32 bits of "Lookup RAM" per Cog
- 512Kx8 bits of shared Hub RAM

**Advanced Features:**
- Hardware accelerated custom bytecode executor
- 3 prioritized interrupts (mappable to many event sources)
- 64 "Smart Pins" with advanced capabilities
- Fast streaming DMA
- Built-in video signal encoders

## Key Documentation Sections

### Core References
- Assembly Symbol List (asm_index.html)
- Instruction Table (p2_optable.html)
- Opcode Matrix (p2_opmatrix.html)
- Sitemap (sitemap.html)

### Content Areas
- Technical documentation pages
- Auxiliary topics
- Recent changes tracking

## Relevance to ADA Projects

This source is highly relevant for:
- **Video Output**: Built-in video signal encoders, Smart Pins for timing
- **Game System Porting**: 8-core architecture, high-speed processing
- **Custom Emulation**: Bytecode executor, flexible memory architecture
- **Input Systems**: Smart Pins for controller interfaces
- **Performance**: 320+MHz overclock capability for demanding emulation

## Next Steps
1. Import instruction table and opcode matrix
2. Extract Smart Pin documentation for video/input projects
3. Document video encoder capabilities
4. Analyze bytecode executor for emulation applications