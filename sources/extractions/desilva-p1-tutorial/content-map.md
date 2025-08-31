# DeSilva P1 Assembly Tutorial - Content Map

**Source**: P1 DeSilvaAssemblyTutorial.pdf (2007)  
**Author**: deSilva © 2007  
**Version**: 1.21 (2007-08-21)  
**Pages**: 40  
**Extraction Date**: 2025-08-20

## Document Overview

### Target Audience & Prerequisites
- **Level**: Intermediate (not for beginners)
- **Prerequisites**: 
  - Good understanding of Propeller architecture
  - Successful SPIN programming background
  - Familiarity with PropellerTool IDE
  - Knowledge of PropTerminal tool

### Teaching Philosophy
- Practical approach to overcome "first frustrations" with machine language
- Focus on Propeller-specific peculiarities
- Emphasis on understanding hardware concepts
- Progressive complexity with working examples

---

## P1 Architecture Coverage

### Hardware Architecture (Comprehensive)
- **COG System**: 8 processors @ 20 MIPS each
- **Memory Structure**: 
  - 32KB Hub RAM
  - 2KB (512 x 32-bit) COG RAM per processor
  - 32KB ROM (Bootstrap + SPIN interpreter)
- **I/O System**: 32-bit I/O port (INA, OUTA, DIRA)
- **Timing**: System clock (CNT), hub slot timing (16-tick cycles)
- **Synchronization**: 8 semaphores (LOCKs)
- **Specialized Hardware**:
  - 2 timers/counters per COG (CTRA/CTRB with PHSA/B, FRQA/B) 
  - Video processor per COG (VCFG, VSCL connected to Timer A)
  - Performance calculation: 160 x 32-bit MIPS, 48kB static RAM, 16 timers, 8-fold video logic

### Memory System Deep Dive
- **COG Memory**: 496 instruction cells + 16 I/O registers (addresses 496-511)
- **Hub-COG Interface**: Hub rotation every 16 clock cycles
- **Bootstrap Process**: ROM → COG #0 → SPIN interpreter → program loading
- **COGNEW Mechanism**: Loading 2000 bytes (500 cells) in 100 microseconds
- **Memory Access Timing**: Variable 7-22 clock ticks for hub operations

### Instruction Set Architecture
- **Format**: 32-bit fixed-width instructions
- **Addressing**: Two-address format with systematic immediate addressing (0-511)
- **Instruction Encoding**: 6+3+1+4+9+9 bits (opcode, flags, immediate, condition, dest, source)
- **Condition Codes**: 16 possible conditions using C and Z flags
- **Pipeline**: 6-tick execution with 4-tick apparent speed via pipelining

---

## P1 Instruction Coverage

### Basic Instructions (Detailed Examples)
- **Data Movement**: MOV, MOVI, MOVS, MOVD
- **Arithmetic**: ADD, SUB, NEG, ABS, ABSNEG
- **Logical**: AND, ANDN, OR, XOR, NOT, TEST
- **Comparison**: CMP, CMPS (signed/unsigned)
- **Bit Operations**: Complete shift family (ROR, ROL, SHR, SHL, RCR, RCL, SAR)

### Advanced Instructions (P1-Specific)
- **Specialized Math**: 
  - MAX/MIN (clipping operations - noted naming confusion)
  - MAXS/MINS (signed variants)
  - CMPSUB (conditional subtraction for division)
  - REV (bit reversal with configurable width)
  - SUBABS (subtract absolute value)
- **Conditional Operations**:
  - MUX* family (MUXC, MUXNC, MUXZ, MUXNZ)
  - NEG* family (conditional negate/move)
  - SUM* family (conditional add/subtract)

### Control Flow (Comprehensive)
- **Jumps**: JMP (direct/indirect), conditional execution
- **Subroutines**: CALL/RET shortcuts for JMPRET/JMP combinations
- **JMPRET**: Self-modifying return address storage
- **Conditional Branches**: 
  - DJNZ (decrement and jump if not zero)
  - TJZ/TJNZ (test and jump if zero/not zero)
- **Flag System**: WC/WZ postfixes, systematic flag control

### Memory Operations (Hub Interface)
- **Hub Access**: RDBYTE, RDWORD, RDLONG, WRBYTE, WRWORD, WRLONG
- **Timing Considerations**: Variable timing due to hub rotation
- **Address Management**: PAR register, computed addresses
- **Communication Patterns**: COG-to-COG via hub memory

### System Instructions
- **COG Management**: COGID, COGINIT, COGSTOP
- **Timing**: WAITCNT, CNT register usage
- **Synchronization**: LOCKNEW, LOCKRET, LOCKCLR, LOCKSET
- **Configuration**: CLKSET

---

## Programming Concepts & Patterns

### Self-Modifying Code (Essential P1 Technique)
- **Necessity**: No traditional addressing modes
- **Tools**: MOVI, MOVS, MOVD for instruction modification
- **Rules**: Never modify the next instruction (pipeline safety)
- **Applications**: Indexed addressing, loop optimization
- **Examples**: Array access, byte packing/unpacking

### Parallel Programming Concepts
- **Semaphore Usage**: Critical sections, resource protection
- **Communication Patterns**: Hub memory sharing, PAR parameter passing
- **Synchronization**: Lock-based coordination between COGs
- **Real-world Example**: Department store customer counting system

### Video System (Hardware-Specific)
- **Video Logic**: PIXELS and COLORS registers
- **WAITVID Instruction**: Core video output mechanism
- **Modes**: 2-color and 4-color modes
- **Clock Generation**: Timer A configuration, PLL usage (4-8 MHz input, ×16 multiplication)
- **Performance**: Up to 80 Mbit/s single channel output
- **Frame Concepts**: Register frames of 4, 8, 16, or 32 elements

### Timing & Performance
- **Instruction Timing**: Standard 4 clocks (6-tick pipeline)
- **Hub Access**: 7-22 clocks variable timing
- **Pipeline Details**: Fetch, decode, operand fetch, execute, store
- **Performance Examples**: 
  - Basic arithmetic: 333ns per instruction @ 12MHz RCFAST
  - Video output: 10-40 MB/s depending on method
  - Hub access limitations and optimization strategies

---

## Assembly Language Syntax & Conventions

### Syntax Rules (BNF Grammar Provided)
- **Directives**: ORG 0, FIT 496, RES n
- **Labels**: Local (:label) vs Global (label) scope
- **Operands**: Register addressing, immediate addressing (#value)
- **Comments**: SPIN-style commenting
- **Data Definition**: LONG, WORD, BYTE with initialization

### Programming Style & Conventions
- **Register Naming**: r1-r99 or A-Z for temporaries
- **Label Management**: Local labels for reusable names
- **Memory Layout**: ORG 0 mandatory, FIT 496 safety check
- **Flag Management**: Explicit WC/WZ postfixes
- **Code Organization**: Clear separation of code and data sections

---

## Teaching Methodology & Voice Analysis

### Pedagogical Approach
- **Progression**: Hardware concepts → Basic instructions → Advanced techniques → Real applications
- **Example Strategy**: 
  - Start with LED blinking (ex01)
  - Progress to communication between COGs (ex02)
  - Build to complex algorithms (multiplication, division, square root)
- **Explanation Style**: 
  - Technical accuracy with accessible analogies
  - Acknowledges complexity while providing clear paths forward
  - Uses humor and personality to engage ("Real Programmers don't use SPIN!? O yes, they do!")

### Voice Characteristics
- **Tone**: Experienced, slightly opinionated, but helpful
- **Audience Awareness**: Assumes intermediate knowledge, doesn't start from basics
- **Teaching Philosophy**: "Help you over the first frustrations" rather than comprehensive coverage
- **Cultural Context**: German author writing for English audience (acknowledges language privilege)
- **Historical Perspective**: 30 years of microprocessor experience, references to computing history

### Example Patterns
- **Incremental Complexity**: Each example builds on previous concepts
- **Multiple Solutions**: Shows different approaches (ex08A vs ex08B vs ex08C)
- **Performance Awareness**: Always discusses timing and efficiency implications
- **Practical Focus**: Department store example for semaphores, video without video for learning

### Encouragement Techniques
- **Realistic Expectations**: Acknowledges learning curve and common mistakes
- **Problem Prevention**: Warns about common pitfalls before they occur
- **Confidence Building**: "This is fast! And imagine, we can run the Prop even 7 times faster!"
- **Community Connection**: References Phil Pilgrim's complementary work, forum discussions

---

## P1-to-P2 Mapping Potential

### Direct Transfers (Concepts that Apply)
- **COG Architecture**: P2 has similar but enhanced COG concept
- **Memory Hierarchy**: Hub-COG relationship transfers
- **Instruction Format**: P2 uses similar but enhanced 32-bit format
- **Conditional Execution**: P2 maintains this key feature
- **Self-Modifying Code**: Still relevant in P2 (though less necessary)

### Major Differences (P1→P2 Evolution)
- **Instruction Set**: P2 has 400+ vs P1's smaller set
- **Memory Size**: P2 has much larger hub and COG memory
- **Smart Pins**: P2's major innovation not present in P1
- **CORDIC**: P2 hardware math unit not in P1
- **Events System**: P2's enhanced event architecture
- **Clock Speed**: P2 runs much faster than P1's 80MHz

### Teaching Transfer Value
- **Hardware Understanding**: Fundamental concepts of parallel processing
- **Assembly Mindset**: Thinking in terms of registers, timing, flags
- **Self-Modifying Code**: Techniques transfer even if less needed
- **Performance Optimization**: Cycle counting and efficiency focus
- **Parallel Programming**: Semaphore usage and COG coordination

---

## Document Completeness Assessment

### Covered Thoroughly
- ✅ Basic instruction set with examples
- ✅ Hardware architecture fundamentals  
- ✅ Self-modifying code techniques
- ✅ Video system operation
- ✅ Parallel programming with locks
- ✅ Assembly syntax and conventions
- ✅ Performance considerations and timing

### Mentioned But Not Detailed
- ⚠️ Complex math algorithms (multiplication, division, square root - code provided but minimal explanation)
- ⚠️ Advanced video applications (color, NTSC specifics)
- ⚠️ SPIN integration details
- ⚠️ Debugging techniques

### Explicitly Missing (Author's Notes)
- ❌ Best Practices chapter (planned but not written)
- ❌ Efficient multi-COG usage
- ❌ Time vs Space optimization
- ❌ Debugging with PASD
- ❌ Advanced video applications
- ❌ NR postfix details
- ❌ OUTB tricks

---

## Value for P2 Manual Creation

### High-Value Elements
1. **Teaching Progression**: Hardware → Instructions → Techniques → Applications
2. **Example Strategy**: Working code with performance analysis
3. **Voice**: Experienced but approachable, acknowledges complexity
4. **Practical Focus**: Real-world applications and common pitfalls
5. **Performance Consciousness**: Always discusses timing implications

### Adaptation Notes for P2
- **Scale Adjustment**: P2's much larger instruction set needs different organization
- **New Concepts**: Smart Pins, CORDIC, Events require new pedagogical approaches
- **Maintained Elements**: Hardware-first approach, example-driven learning, performance focus
- **Enhanced Features**: P2's deterministic timing vs P1's variable hub timing

This content map provides the foundation for analyzing DeSilva's teaching voice and creating P2 documentation that captures his effective pedagogical approach while addressing P2's significantly enhanced capabilities.