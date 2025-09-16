# P2 Knowledge Base Package Changelog

This changelog documents customer-facing changes for external package users.

## v1.3.0 - 2025-01-16 (In Progress)

### New Features
- **Architectural Code Patterns**: Added 28 patterns discovered from analysis of 730+ Spin2 source files
  - Object composition patterns (5): How P2 developers structure object dependencies (no_objects, single_object, few_objects, several_objects, framework)
  - Hardware utilization patterns (8): Common resource management strategies (buffer_management, timing_control, protocol_implementation, pin_control, state_machine, error_handling, memory_allocation, cog_management)
  - Domain-specific patterns (9): Application-focused patterns (display_driver, sensor_reader, motor_controller, communication_handler, data_logger, audio_processor, test_harness, configuration_manager, utility_library)
  - Specialized patterns (6): Advanced architectural approaches (shared_memory, diagnostic_output, event_dispatcher, resource_pool, mailbox_communication, layered_architecture, plugin_system)

### Improvements
- Enhanced patterns manifest to support both implementation patterns (how to do X) and architectural patterns (how code is structured)
- Minimized YAML file sizes for Download On Demand efficiency (~85% size reduction, now 300-500 bytes each)
- Connected architectural patterns to main manifest hierarchy for seamless discovery
- Pattern usage statistics from real-world code analysis (e.g., 51% use no_objects pattern, 82% use buffer_management)

### Documentation
- Complete pattern audit documenting 25+ pattern categories from 730 source files
- Pattern selection guide for AI code generation
- Pattern composition guidance showing how patterns combine

## v1.2.0 - 2025-09-13

### New Features
- PNUT_TS compiler integration with enhanced operand format definitions
- 39 unique operand patterns with pipe symbol alternatives (e.g., `#S | D`)
- Comprehensive PASM2 instruction documentation (360 instructions + 17 concepts)
- Enhanced compiler encoding details with raw values and bit patterns

### Improvements  
- Operand format patterns properly categorized (no operands, register operations, immediate values)
- Compiler compatibility tracking with PNUT_TS v1.51.5
- Documentation level upgraded to "comprehensive" across instruction set
- Enhanced flag effects with detailed bit patterns (WC, WZ, WCZ)

### Coverage
- 377 total PASM2 files (360 instructions + 17 concept files)
- Complete SPIN2 language specification integration
- Real-world validation with community OBEX projects

---
*This changelog focuses on user-visible changes in the knowledge base packages.*