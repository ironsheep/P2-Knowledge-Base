# Table Complex Test Document

This document tests the `\real{}` command issue we've been debugging.

## Complex Table with Calculations

| Operation | COG-Driven | Smart Pin | Performance |
|-----------|------------|-----------|-------------|
| Basic I/O | Manual timing | Automatic | 2.5x faster |
| PWM Generation | Software loops | Hardware PWM | 10x faster |  
| Pulse Measurement | Interrupt handling | Automatic capture | 5x faster |

## Another Table Structure

| Pin Mode | Configuration | Use Case |
|----------|---------------|----------|
| %00000 | Disabled | Power saving |
| %00001 | Repository | Smart pin off, cog drive |
| %00010 | DAC | Analog output |

This should test the table column width calculations that require the `\real{}` command in Pandoc 2.17.1.1.