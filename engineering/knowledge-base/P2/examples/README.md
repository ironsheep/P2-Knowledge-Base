# P2 Code Examples

## Overview
Validated code examples demonstrating P2 features, instructions, and programming patterns.

## Organization

### By Category
- `basic/` - Simple, single-concept examples
- `intermediate/` - Multi-concept integration
- `advanced/` - Complex system examples
- `snippets/` - Small code fragments

### By Feature
- `smart-pins/` - Smart pin configuration and usage
- `cordic/` - CORDIC solver examples
- `multi-cog/` - Inter-cog communication
- `interrupts/` - Interrupt handling
- `hub-exec/` - Hub execution mode

## File Naming
- Pattern: `[feature]-[concept]-example.spin2` or `.pasm2`
- Examples:
  - `smart-pin-pwm-example.spin2`
  - `cordic-rotation-example.pasm2`
  - `multi-cog-mailbox-example.spin2`

## Example Schema
Each example includes:
```yaml
example_id: "smart-pin-pwm-basic"
title: "Basic PWM with Smart Pin"
description: "Demonstrates PWM generation using smart pin mode 7"
difficulty: "basic"
features_demonstrated:
  - "Smart pin configuration"
  - "PWM duty cycle control"
instructions_used:
  - WRPIN
  - WXPIN
  - WYPIN
  - RDPIN
related_entries:
  - "components/smart-pins/mode-07-pwm.yaml"
  - "instructions/pasm2/wrpin-instruction.yaml"
code: |
  ' Spin2 code here
  ...
tested: true
test_hardware: "P2 Eval Board Rev C"
```

## Validation Status
- All examples must compile successfully
- Hardware-tested examples marked with test results
- Simulation-compatible examples noted