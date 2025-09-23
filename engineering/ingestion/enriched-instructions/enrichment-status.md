# PASM2 Instruction Enrichment Status

## Date: 2025-09-22
## Location: `/engineering/ingestion/enriched-instructions/pasm2-narratives/`
## Total Instructions for Enrichment: 115

## Priority Levels Based on Heat Map Scores

### 🔴 CRITICAL - Score 35 (2 instructions)
These have the poorest documentation and need immediate attention:

| Instruction | Current Status | Enrichment Needed |
|-------------|----------------|-------------------|
| PUSHA | Basic description only | Full narrative, stack examples, PTRA usage |
| PUSHB | Basic description only | Full narrative, stack examples, PTRB usage |

### 🟧 HIGH - Score 40 (34 instructions)
These need comprehensive documentation:

#### Stack Operations (2)
- [ ] POPA - Pop using PTRA
- [ ] POPB - Pop using PTRB

#### Interrupt System (9)
- [ ] NIXINT1 - Clear interrupt 1
- [ ] NIXINT2 - Clear interrupt 2
- [ ] NIXINT3 - Clear interrupt 3
- [ ] TRGINT1 - Trigger interrupt 1
- [ ] TRGINT2 - Trigger interrupt 2
- [ ] TRGINT3 - Trigger interrupt 3
- [ ] SETINT1 - Setup interrupt 1
- [ ] SETINT2 - Setup interrupt 2
- [ ] SETINT3 - Setup interrupt 3

#### CRC Operations (2)
- [ ] CRCBIT - CRC bit calculation
- [ ] CRCNIB - CRC nibble calculation

#### Color Space Converter (5)
- [ ] SETCY - Set color Y component
- [ ] SETCFRQ - Set color frequency
- [ ] SETCQ - Set color Q component
- [ ] SETCI - Set color I component
- [ ] SETCMOD - Set color mode

#### Pixel Operations (7)
- [ ] MULPIX - Multiply pixels
- [ ] SETPIX - Set pixel value
- [ ] SETPIV - Set pixel inverse
- [ ] BLNPIX - Blend pixels
- [ ] MIXPIX - Mix pixels
- [ ] RGBEXP - RGB expand
- [ ] RGBSQZ - RGB squeeze

#### Event System (4)
- [ ] SETSE1 - Set selectable event 1
- [ ] SETSE2 - Set selectable event 2
- [ ] SETSE3 - Set selectable event 3
- [ ] SETSE4 - Set selectable event 4

#### DAC/Streamer (2)
- [ ] SETDACS - Configure DACs
- [ ] SETXFRQ - Set streamer frequency

#### Hub Write (3)
- [ ] WRC - Write byte with C
- [ ] WRBYTE - Write byte to hub
- [ ] WRZ - Write byte with Z

### 🟨 MEDIUM - Score 50 (79 instructions)
These have basic documentation but need examples and practical notes:

#### Hub Operations (20)
- [ ] WMLONG - Write multiple longs
- [ ] WRLONG - Write long
- [ ] WRWORD - Write word
- [ ] WRFAST - Start fast write
- [ ] WFBYTE - Write FIFO byte
- [ ] WFWORD - Write FIFO word
- [ ] WFLONG - Write FIFO long
- [ ] HUBSET - Hub setup
- [ ] LOCKRET - Return lock
- [ ] LOCKNEW - Get new lock
- [ ] RDBYTE - Read byte
- [ ] RDPIN - Read pin
- [ ] RQPIN - Request pin state
- [ ] RDLUT - Read lookup table
- [ ] WRLUT - Write lookup table
- [ ] RFBYTE - Read FIFO byte
- [ ] RFWORD - Read FIFO word
- [ ] RFLONG - Read FIFO long
- [ ] RFVAR - Read FIFO variable
- [ ] RFVARS - Read FIFO variable signed

#### Control Flow (24)
- [ ] SETQ - Set Q register
- [ ] TJNZ - Test and jump if not zero
- [ ] TJF - Test and jump if false
- [ ] TJS - Test and jump if set
- [ ] TJZ - Test and jump if zero
- [ ] SKIP - Skip instructions
- [ ] REP - Repeat block
- [ ] SKIPF - Skip forward
- [ ] JMP - Jump
- [ ] JMPREL - Jump relative
- [ ] JPAT - Jump on pattern match
- [ ] JINT - Jump on interrupt
- [ ] JNINT - Jump on no interrupt
- [ ] JXRO - Jump on XRO
- [ ] JNXRO - Jump on no XRO
- [ ] JXFI - Jump on XFI
- [ ] JNXFI - Jump on no XFI
- [ ] JATN - Jump on attention
- [ ] JNATN - Jump on no attention
- [ ] JNPAT - Jump on no pattern
- [ ] RET - Return
- [ ] RETA - Return via RETA
- [ ] RETB - Return via RETB
- [ ] EXECF - Execute FIFO

#### Data Operations (16)
- [ ] LOC - Load constant
- [ ] GETCT - Get counter
- [ ] GETPTR - Get pointer
- [ ] TESTB - Test bit
- [ ] SETPAT - Set pattern
- [ ] MERGEB - Merge bytes
- [ ] MERGEW - Merge words
- [ ] MOVBYTS - Move bytes
- [ ] SPLITB - Split bytes
- [ ] SPLITW - Split words
- [ ] SUMZ - Sum with Z
- [ ] SUMC - Sum with C
- [ ] GETQX - Get Q X component
- [ ] GETQY - Get Q Y component
- [ ] GETXACC - Get X accumulator
- [ ] MUXC - Mux with C
- [ ] MUXNC - Mux with not C

#### Streamer (4)
- [ ] XSTOP - Stop streamer
- [ ] XCONT - Continue streamer
- [ ] XZERO - Zero streamer
- [ ] XINIT - Initialize streamer

#### Pin Operations (3)
- [ ] WXPIN - Write extended pin
- [ ] WRNC - Write with not C
- [ ] WRNZ - Write with not Z

#### Special Operations (12)
- [ ] NOP - No operation
- [ ] ASMCLK - Assembly clock
- [ ] DEBUG - Debug breakpoint
- [ ] SETSCP - Set scope
- [ ] GETSCP - Get scope
- [ ] SETLUTS - Set LUT sharing
- [ ] SEUSSR - Set user
- [ ] SEUSSF - Set user flags
- [ ] GETRND - Get random
- [ ] XORO32 - XOR oscillator 32
- [ ] FBLOCK - FIFO block mode
- [ ] SETPAT - Set pattern

## Enrichment Template

Each instruction needs:

```yaml
instruction: NAME
syntax: [existing]
encoding: [existing]
timing: [existing]
group: [existing]
description: |
  [Multi-paragraph description explaining:]
  - What the instruction does in detail
  - When and why to use it
  - How it interacts with other P2 features
  - Common applications and use cases
  
flags_affected: [if applicable]

examples:
- name: Basic Usage
  description: Simple example showing fundamental operation
  code: |
    ' Code with detailed comments
    instruction operands  ' What this does
  source: basic_example

- name: Practical Application
  description: Real-world usage scenario
  code: |
    ' More complex example
    ' Showing integration with other instructions
  source: application_example

- name: Advanced Technique
  description: Expert-level usage pattern
  code: |
    ' Advanced example with optimization
  source: advanced_example

related_instructions:
- INSTRUCTION1: How it relates
- INSTRUCTION2: Alternative approach
- INSTRUCTION3: Complementary operation

notes:
- Important timing consideration
- Common pitfall to avoid
- Performance tip
- Hardware limitation
- Best practice recommendation

documentation_level: comprehensive
documentation_source: enhanced_2025
last_updated: 2025-09-22
```

## Work Plan

### Today's Focus
1. **Start with PUSHA/PUSHB** - These are critical (score 35)
2. **Complete stack operations** - POPA/POPB to have complete set
3. **Interrupt system** - Complete NIXINT/TRGINT/SETINT families
4. **CRC operations** - CRCBIT/CRCNIB with practical examples

### Success Metrics
- [ ] All Score 35 → Score 80+ (comprehensive)
- [ ] All Score 40 → Score 70+ (good with examples)
- [ ] All Score 50 → Score 60+ (good basic)
- [ ] Zero instructions below Score 40

## Notes
- Working copies only - DO NOT modify `/engineering/knowledge-base/P2/`
- These will be integrated in future release after review
- Focus on practical, real-world examples from P2 projects
- Reference existing high-quality instructions like WAITX as models