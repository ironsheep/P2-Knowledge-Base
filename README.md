# P2 Knowledge Base

> Comprehensive documentation and resources for the Parallax Propeller 2 (P2) multicore microcontroller

[![Version](https://img.shields.io/badge/version-1.4.2-blue.svg)](https://github.com/ironsheep/P2-Knowledge-Base/releases)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

## 🤖 Using with AI Assistants (Claude, GPT, etc.)

### ⭐ Best experience: P2 Knowledge Base MCP

For Claude Code, Claude Desktop, and other agents that support the Model Context Protocol (the standard interface that lets AI agents call external services as native tools), install the **[P2 Knowledge Base MCP](https://github.com/ironsheep/P2-Knowledge-Base-MCP)**. The MCP gives your agent native tool calls to query the knowledge base directly — search by topic, fetch instructions by name, browse OBEX community objects — without downloading files or burning context on retrieval.

**[→ Install instructions](https://github.com/ironsheep/P2-Knowledge-Base-MCP/blob/main/INSTALL.md)**

### Without MCP support

**[→ BOOTSTRAP (Quick Setup)](deliverables/ai-reference/BOOTSTRAP.md)**
**One-command setup for AI assistants.** Single entry point for both Unix/macOS and Windows. Downloads everything automatically.

**[→ COMPLETE GUIDE](deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md)**
Comprehensive guide on using this knowledge base with AI systems, including example prompts and usage patterns.

**[→ PRIVACY GUIDE FOR DEVELOPERS](deliverables/developer-docs/ai-development/Claude-Code-Privacy-Guide-for-P2-Developers.pdf)** 📔
**Essential reading before using AI tools!** Learn how to protect your intellectual property and follow best practices for AI-assisted P2 development.

## 🎯 Find What You Need

### PDF Manuals (Community Review)
**[→ Generated Documents](deliverables/documents/)**
P2 Assembly Language Reference Manual and P2 Assembly Programming tutorial available for community technical review.

### For AI Systems & Code Generation
**→ AI Reference Documentation**
(Work in progress) Complete P2 instruction set, architecture details, and code patterns optimized for LLM consumption. Structured for accurate code generation with comprehensive examples and constraints.

## About the Propeller 2

The Propeller 2 (P2X8C4M64P) is a symmetric multicore microcontroller featuring **8 identical 32-bit processors** (COGs) that execute independently while sharing resources. Unlike traditional microcontrollers, the P2 provides true parallel processing with deterministic timing, making it ideal for real-time applications.

### Core Architecture
- **8 Independent COGs**: 90 MIPS each (720 MIPS total @ 180 MHz), true parallel execution
- **Dual Memory Model**: Each COG has 4KB private RAM; all share 512KB Hub RAM
- **Execute from Anywhere**: COGs can run code from COG RAM, LUT RAM, or Hub RAM
- **No Resource Contention**: Each COG has dedicated registers, no cache misses or pipeline stalls

### Smart Pin System  
- **64 Autonomous I/O Pins**: Each pin independently handles complex operations
- **Built-in Protocols**: UART, SPI, I²C, USB, quadrature decoding without CPU overhead
- **Analog & Digital**: 14-bit ADC, 16-bit DAC, PWM, and video generation per pin
- **Offload Everything**: Smart Pins run autonomously, freeing COGs for application logic

### Developer Advantages
- **Deterministic Timing**: Count cycles exactly, no interrupt latency
- **Hardware Parallelism**: No RTOS needed - hardware handles multiprocessing
- **CORDIC Math Engine**: Hardware multiply, divide, trig, and logarithms
- **Mixed Languages**: Spin2 (high-level), PASM2 (assembly), C/C++, Python

## About This Project

The P2 Knowledge Base provides comprehensive, AI-optimized documentation for the Propeller 2. Our goal is enabling both human developers and AI systems to effectively utilize the P2's unique parallel processing capabilities through accurate, structured documentation.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project uses dual licensing:

- **Code and Data** (YAML, Python, scripts): [MIT License](LICENSE)
- **Documentation** (manuals, PDFs, guides): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

Copyright © 2025 Iron Sheep Productions, LLC and Parallax Inc.

See individual files for specific licensing. Propeller 2, P2, and Parallax are trademarks of Parallax Inc.

---

*Built with intention for the P2 community*
