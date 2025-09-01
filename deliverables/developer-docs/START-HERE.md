# P2 Developer Documentation - Start Here

Welcome to the P2 Knowledge Base developer documentation. This guide helps you quickly get productive with the Propeller 2 (P2) microcontroller.

## 🚀 Quick Start

### What is P2?
The Propeller 2 is a unique 8-core microcontroller designed for real-time, parallel processing applications. Each core (called a "cog") runs independently at 180MHz+, sharing access to 512KB of hub RAM and 64 Smart Pins.

### Why P2?
- **True Parallelism**: 8 independent processors, no interrupts needed
- **Smart Pins**: Hardware-accelerated I/O for any protocol
- **Deterministic Timing**: Predictable, jitter-free operation
- **CORDIC Solver**: Hardware math acceleration for DSP/graphics

## 📚 Learning Paths

Choose your path based on your background:

### For Beginners
Start with fundamentals and work through progressively:
1. [Getting Started Guide](../learning-paths/01-fundamentals/getting-started.md)
2. Basic P2 architecture concepts
3. Your first Spin2 program
4. Introduction to Smart Pins

### For P1 Developers
Leverage your existing Propeller knowledge:
1. [P1 to P2 Migration Framework](../learning-paths/p1-to-p2-migration-framework.md)
2. Key architectural differences
3. Enhanced instruction set
4. Smart Pin advantages over P1 counters

### For Embedded Developers
Apply your embedded experience to P2:
1. P2 vs traditional MCU architectures
2. Multi-core programming patterns
3. Real-time system design with P2
4. Peripheral integration strategies

## 🛠️ Development Tools

### Official Tools
- **Propeller Tool**: Windows IDE with integrated compiler
- **FlexProp**: Cross-platform IDE supporting multiple languages
- **PNut**: Command-line compiler

### AI-Assisted Development
This knowledge base is optimized for AI-assisted development:
- Use with Claude, GitHub Copilot, or other AI coding assistants
- Structured documentation enables accurate code generation
- Complete instruction reference for PASM2 programming

## 📖 Core Documentation

### Architecture & Languages
- [PASM2 Essentials](../reference/pasm2-essentials.md) - Core assembly instructions
- [Architecture Overview](../reference/architecture-overview.md) - P2 system architecture
- [AI Reference Guide](../ai-reference/AI-P2-Reference-V2.md) - Comprehensive P2 reference

### Programming Patterns
- Multi-cog coordination strategies
- Event system usage
- Hub memory sharing patterns
- Smart Pin configuration sequences

## 💡 Use Cases & Examples

### Common Applications
- **Motor Control**: Precise PWM, encoder reading, closed-loop control
- **Communication**: UART, SPI, I2C, custom protocols
- **Signal Processing**: Audio/video, DSP with CORDIC
- **Instrumentation**: Data acquisition, real-time monitoring
- **IoT Devices**: Sensor integration, wireless communication

### Code Examples
Browse working examples in our repository:
- Basic patterns and templates
- Protocol implementations
- Hardware interfacing
- Complete project examples

## 🔗 Resources

### Official Resources
- [Parallax P2 Documentation](https://www.parallax.com/propeller-2/)
- [P2 Community Forum](https://forums.parallax.com/categories/propeller-2-multicore-microcontroller)
- [OBEX P2 Object Exchange](https://github.com/parallaxinc/propeller)

### Community Resources
- [P2 Tricks and Traps](https://p2docs.github.io/)
- Community tutorials and guides
- Open source P2 projects

## 🎯 Next Steps

1. **Choose Your Path**: Select the learning path that matches your experience
2. **Set Up Tools**: Install development environment 
3. **Try Examples**: Start with working code and modify
4. **Join Community**: Get help and share your projects
5. **Build Something**: Apply your knowledge to real projects

## 📦 Download Resources

### Knowledge Packages
For AI-enhanced development or offline reference:
- [Complete Instruction Set (JSON)](download/pasm2-instructions.json)
- [Smart Pin Reference (JSON)](download/smart-pins-reference.json)
- [Code Pattern Library](download/p2-patterns.zip)

### Quick References
- [PASM2 Quick Card (PDF)](download/pasm2-quick-reference.pdf)
- [Smart Pin Mode Table](download/smart-pin-modes.pdf)
- [P2 Pinout Diagram](download/p2-pinout.pdf)

## 🤝 Contributing

This knowledge base is a community effort. Contributions welcome:
- Report issues or gaps in documentation
- Submit code examples and patterns
- Share your P2 projects and learnings
- Help improve explanations and tutorials

---

*Ready to start? Choose your [learning path](#-learning-paths) above and begin your P2 journey!*