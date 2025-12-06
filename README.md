# P2 Knowledge Base

> Comprehensive documentation and resources for the Parallax Propeller 2 (P2) multicore microcontroller

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/ironsheep/P2-Knowledge-Base/releases)
[![Coverage](https://img.shields.io/badge/P2%20Coverage-80%25-green.svg)](deliverables/reference/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

## 🤖 Using with AI Assistants (Claude, GPT, etc.)

**[→ USING WITH AI GUIDE](deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md)**  
**Start here if you're using Claude Code, GitHub Copilot, or other AI assistants!** Complete guide on how to set up and use this knowledge base with AI systems, including example prompts and usage patterns.

**[→ PRIVACY GUIDE FOR DEVELOPERS](deliverables/developer-docs/ai-development/Claude-Code-Privacy-Guide-for-P2-Developers.pdf)** 📔  
**Essential reading before using AI tools!** Learn how to protect your intellectual property, understand data handling policies, and follow best practices for AI-assisted P2 development.

## 🎯 Find What You Need

### For AI Systems & Code Generation
**→ AI Reference Documentation**  
(Work in progress) Complete P2 instruction set, architecture details, and code patterns optimized for LLM consumption. Structured for accurate code generation with comprehensive examples and constraints.

## The following sections are planned for future updates, but currently contain NO content!

### For Developers
**→ Developer Documentation**  
Intended to be Quick-start guides, programming patterns, and practical examples. Everything needed to begin P2 development, from basic concepts to advanced multicore techniques.

### For Learners
**→ Learning Paths**  
Intended to be Structured tutorials progressing from fundamentals to expertise. Includes migration guides for P1 developers and hands-on exercises for mastering P2 capabilities.

### For Reference
**→ Technical Reference**  
Intended to be QAuthoritative instruction set documentation, hardware specifications, and architectural details. The definitive source for P2 technical information.

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

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

*Built with intention for the P2 community*
