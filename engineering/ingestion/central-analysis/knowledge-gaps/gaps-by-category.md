# P2 Knowledge Gaps - Master List
*Consolidated from spreadsheet analysis and PDF extraction*
*Date: 2025-08-14*

## 1. Specific Technical Questions for Chip Gracey

### Boot Process - State Machine Details (Document marked "needs more editing")

**Boot Detection Sequence**:
1. After power-on reset, what GPIO pins are checked and in what order to detect boot devices?
2. What are the exact voltage thresholds and timing requirements for detecting SD card presence on P58-P61?
3. For SPI flash detection on P58-P61, what is the exact command sequence sent and expected response?
4. What specific pull-up/pull-down resistor values trigger serial boot mode?
5. How many clock cycles does the boot ROM wait for each device detection before moving to the next?

**SPI Flash Boot Protocol**:
1. What is the exact SPI command sequence to read the boot image? (Commands, addresses, dummy cycles)
2. What SPI modes are supported (Mode 0/1/2/3) and at what clock frequency?
3. What is the boot image header format? (Magic bytes, size field, checksum format, entry point)
4. How does the boot ROM validate the image? (CRC32? Simple checksum? What polynomial?)
5. What memory address does the SPI boot image load to and what is the maximum size?

**SD Card Boot Protocol**:
1. Does boot ROM support SD or SDHC or both? What about SDXC?
2. What is the exact initialization sequence? (CMD0, CMD8, ACMD41 parameters?)
3. Does it look for a partition table or raw sectors? If partition, which type (MBR/GPT)?
4. What filename does it search for on FAT32? Is it case-sensitive?
5. What cluster size limitations exist for FAT32 boot?

**Serial Boot Protocol**:
1. What baud rate detection algorithm is used? (Autobaud on what character?)
2. What is the exact handshake sequence? ("> " then what response expected?)
3. For Prop_Hex mode: Is it Intel HEX, Motorola S-records, or custom format?
4. For Prop_Txt mode: What is the base64 encoding variant used? (Standard, URL-safe, custom?)
5. What is the maximum download size and timeout values?

**Boot Failure Behavior**:
1. If all boot sources fail, does it drop to serial terminal at a specific baud rate?
2. Is there a boot status register that can be read to determine failure reason?
3. Are there any GPIO pins that indicate boot status during the process?

### Bytecode Execution - XBYTE Mechanism (Document marked "to be completed")

**XBYTE Implementation**:
1. What are the exact 256 LUT addresses used for bytecode vectors? ($000-$0FF or $100-$1FF?)
2. How does XBYTE modify the pipeline? Does it inject instructions or replace them?
3. What is the exact format of the LUT entry? (Lower 10 bits = address, upper 22 bits = SKIPF pattern?)
4. Can XBYTE be interrupted? If so, how does resume work?
5. What is the overhead in clocks for each bytecode dispatch?

**Bytecode Performance**:
1. You mention "6-clock custom-bytecode executor" - is this 6 clocks per bytecode or 6 clocks overhead?
2. Can bytecodes call other bytecodes? Is there a bytecode stack?
3. How does SETQ interact with XBYTE for parameter passing?
4. Can bytecodes span across hub/LUT/cog execution boundaries?

**Practical Bytecode Usage**:
1. What bytecode interpreters have been implemented? (Forth, Basic, etc?)
2. Is there a recommended bytecode instruction set for common operations?
3. How do you debug bytecode execution? Any trace capability?

## 2. Questions Arising from PDF That Weren't Fully Answered

### Specific Timing Clarifications Needed from Chip

**CORDIC Pipeline Timing**:
1. The CORDIC is described as "54-stage pipeline" but results take "55 clocks" - is clock 1 used for command handoff from cog to CORDIC?
2. When pipelining multiple CORDIC operations, what is the exact formula for when results can be retrieved without collision?
3. If a cog misses reading a CORDIC result, how many clocks until it's overwritten by the next result?

**Hub Access Timing Precision**:
1. The "0-7 clocks wait" for 8-cog system - does this include the instruction fetch cycle or is it additional?
2. When hub exec crosses a long boundary, is the penalty exactly 1 clock or can it be more?
3. For RDLONG from hub, what is the exact cycle breakdown: wait for slot + read cycles + result availability?

**Interrupt Latency Exact Counts**:
1. From interrupt trigger to first ISR instruction execution: minimum clocks? maximum clocks?
2. Does STALLI actually prevent interrupt detection or just delay the branch?
3. If multiple interrupts trigger simultaneously, what is the exact priority resolution timing?

### Architecture Clarifications Needed
1. **"Egg Beater" Name**: Why this specific metaphor? Is there a visual that explains it?
2. **Cog Pairing**: How exactly do paired cogs share LUT RAM? What are the restrictions?
3. **Hub Slots**: In a 16-cog system, how does slot allocation differ from 8-cog?
4. **Memory Aliasing**: Why is upper 16KB always aliased to $FC000-$FFFFF?
5. **Write Protection**: Can individual regions be protected or only the upper 16KB?

### Smart Pin Deep Dive Questions
1. **All X/Y/Z Parameters**: Need complete specification for each of 32 modes
2. **Pin Pairing**: How do odd/even pin pairs interact in each mode?
3. **ADC/DAC Interaction**: Can ADC and DAC be used simultaneously on same pin?
4. **USB Mode**: Complete USB implementation details (mode %11011)
5. **Timing Resolution**: Minimum/maximum measurable times in each timing mode?
6. **Overflow Behavior**: What happens when Z register overflows in counting modes?

### Instruction Details Still Missing
1. **Condition Codes**: What are all 16 EEEE values and their exact conditions?
2. **Flag Behavior**: "C = parity" for logic ops - odd or even parity?
3. **SKIP Patterns**: How exactly do SKIPF patterns work with subroutines?
4. **REP Restrictions**: Why doesn't REP work with SKIPF?
5. **EXECF**: How does fast block execution actually work?
6. **ALT Cascading**: Practical examples of cascaded ALT operations?

## 3. Unanswered Questions from Original Spreadsheet Analysis

### System-Level Questions
1. **Clock Distribution**: How is the system clock distributed to all cogs?
2. **Reset Behavior**: What exactly happens during reset? Register states?
3. **Power Management**: Any power-saving modes beyond WAITINT?
4. **Temperature Effects**: How does temperature affect max frequency?
5. **Silicon Variations**: Differences between Rev B and Rev C silicon?

### Peripheral Integration
1. **Streamer + Smart Pins**: Can they work together? Restrictions?
2. **Multiple DACs**: How many DACs can output simultaneously?
3. **ADC Crosstalk**: Rev C fixes "adjacent-pin crosstalk" - what was the issue?
4. **Event Conflicts**: What happens if multiple events trigger simultaneously?
5. **Lock Contention**: Performance impact of heavy lock usage?

### Programming Model
1. **Stack Operations**: No hardware stack for data? Only return addresses?
2. **Context Switching**: Best practices for saving/restoring cog state?
3. **Inter-Cog Communication**: Besides locks and hub RAM, other mechanisms?
4. **Deterministic Timing**: How to guarantee exact timing with hub variability?
5. **Code Density**: Typical code size comparisons between modes?

## 4. Visual Content Needed (Screenshots from P2 Documentation v35 PDF)

### Architecture Diagrams (Estimated Pages based on 200 lines/page)
1. **Page ~2** (Lines 229-240): P2 overview block diagram if exists
2. **Page ~3** (Lines 571-608): Memory architecture diagram
3. **Page ~3-4** (Lines 622-650): 5-stage pipeline visualization
4. **Page ~33** (Lines 6632+): "Egg Beater" hub interface - rotating slice access pattern
5. **Page ~37** (Lines 7270-7350): CORDIC 54-stage pipeline diagram

### Tables That May Have Lost Formatting
6. **Page ~3** (Lines 575-590): Memory regions table with addresses - verify columns aligned
7. **Page ~33** (Lines 6490-6630): FPGA board hub RAM configurations table
8. **Page ~3-4** (Line 634): Instruction encoding format - EEEE/C/Z/L/D/S fields
9. **Page ~26** (Lines 5100-5120): 16 Event sources with numbers 0-15
10. **Page ~38** (Lines 7495-7520): Smart pin registers and bus width specifications

### Pin Configuration Circuit Schematics
**Text indicates "Below is a diagram" at Line 7869, then pages 76-84 referenced**
11. **Page 76**: Basic pin circuit with 3.3V supply
12. **Page 77**: Pin configuration mode schematic  
13. **Page 78**: Pin configuration mode schematic
14. **Page 79**: Pin configuration mode schematic
15. **Page 80**: Pin configuration mode schematic
16. **Page 81**: Pin configuration mode schematic
17. **Page 82**: Pin configuration mode schematic
18. **Page 83**: Pin configuration mode schematic
19. **Page 84**: Pin configuration mode schematic

### Missing Critical Tables/Info
20. **Condition Codes Table**: All 16 EEEE values (0000-1111) with conditions
    - Should show: if_never, if_nc_and_nz, if_nc_and_z, etc.
    - Not found in text extraction - must be in spreadsheet or missing

### Timing Diagrams If They Exist
21. **Hub slot rotation**: Shows 8 cogs accessing slices in sequence
22. **Interrupt response**: Clock-by-clock from trigger to ISR
23. **FIFO operation**: Fill/drain with (cogs+11) stages
24. **Streamer NCO**: Phase accumulator and rollover

### Boot Process Content Check
25. **Page ~2** (Lines 357-450): Check if ANY content exists beyond headers for:
    - Serial Loading Protocol
    - Prop_Chk, Prop_Clk  
    - Prop_Hex, Prop_Txt
    - PLL Example
    - Reset to Boot Clock Configuration

## 5. Practical Implementation Questions

### Getting Started
1. What's the minimal code to boot and blink an LED?
2. How to set up the PLL for different frequencies?
3. Basic multi-cog startup sequence?
4. How to properly initialize smart pins?
5. Recommended reset circuit?

### Best Practices
1. When to use cog vs LUT vs hub execution?
2. How to minimize hub access conflicts?
3. Optimal data placement strategies?
4. How to debug multi-cog applications?
5. Power consumption optimization techniques?

### Tool Chain
1. What assemblers support all P2 instructions?
2. How to generate bytecode?
3. Debugging tool capabilities?
4. Simulation options?
5. Performance profiling tools?

## 6. Documentation Improvement Suggestions

### Missing Sections
1. Complete instruction reference with examples
2. Application notes for common tasks
3. Migration guide from P1 to P2
4. Performance tuning guide
5. Troubleshooting guide

### Needed Examples
1. Multi-cog synchronization patterns
2. High-speed data acquisition
3. Video generation
4. USB communication
5. Smart pin application circuits

## 7. Specification Clarifications

### Electrical Specifications
1. Absolute maximum ratings?
2. Power consumption by frequency?
3. I/O drive strength options?
4. Input threshold voltages?
5. Temperature range specifications?

### Performance Specifications  
1. Maximum frequency by voltage?
2. Instruction throughput benchmarks?
3. Hub bandwidth limits?
4. Smart pin maximum rates?
5. ADC/DAC specifications (ENOB, SNR, etc.)?

## Summary Statistics

- **Total Questions**: ~100+
- **Author Must Provide**: 2 major sections (Boot, Bytecode)
- **Screenshots Needed**: 20 specific locations
- **Architecture Clarifications**: ~15 items
- **Practical Examples Needed**: ~25 scenarios
- **Specification Details**: ~20 items

## Priority Order for Resolution

### Critical (Blocks Understanding)
1. Boot process complete documentation
2. Condition codes table (16 values)
3. Smart pin X/Y/Z parameters for all modes
4. Basic examples for getting started

### Important (Needed for Development)
1. Complete instruction reference
2. Timing specifications
3. Multi-cog synchronization
4. Debug methodology

### Nice to Have (Optimization/Advanced)
1. Performance tuning guides
2. USB implementation
3. Video generation examples
4. Power optimization

## How to Use This Document

1. **For Chip Gracey**: Focus on sections 1 and 2 first
2. **For Screenshots**: Section 4 with page numbers
3. **For Community**: Sections 5-7 could be crowd-sourced
4. **For Priority**: Follow the priority order above

Place screenshots in `/import/p2/` and I'll process them immediately.