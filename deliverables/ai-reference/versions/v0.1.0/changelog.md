# P2 AI Reference Changelog

## Version 0.1.0 (2025-08-14)

### Initial Release
First public release of P2 AI-optimized reference documentation.

### What's Included
- **Architecture**: Complete COG, Hub, and memory model documentation (90% complete)
- **PASM2 Instructions**: 491 instructions categorized and documented (65% complete)
- **Smart Pins**: Basic 10 modes documented (31% of 32 modes)
- **CORDIC**: Core operations documented with timing
- **Memory Model**: Complete COG/LUT/Hub addressing
- **Condition Codes**: All conditional execution prefixes

### Known Gaps
- **Boot Process**: Not documented (awaiting Chip Gracey)
- **USB Support**: Not documented 
- **Smart Pins**: 22 modes undocumented (awaiting Jon Titus documentation)
- **SPIN2 Language**: Not included (awaiting documentation)
- **Bytecode Interpreter**: Not documented
- **Streamer/FIFO**: Partial documentation only

### Sources
- P2 Documentation v35 - Rev B/C Silicon (Chip Gracey, Parallax)
- P2 Instructions v35 Spreadsheet (Parallax)
- Community contributions pending

### Usage Notes
- This version is NOT stable - expect breaking changes
- Suitable for basic P2 assembly generation
- Not suitable for production code generation
- Check `gaps` section before using any feature

### Next Version Plans (v0.2.0)
- Add SPIN2 language specification
- Complete Smart Pins documentation (Jon Titus)
- Add boot process documentation
- Improve timing specifications
- Add more code examples