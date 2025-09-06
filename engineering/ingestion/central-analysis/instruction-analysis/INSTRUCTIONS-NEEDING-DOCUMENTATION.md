# P2 Instructions Needing Documentation - Organized by Documentation Approach

**Generated**: 2025-09-05  
**Purpose**: Complete inventory of instructions lacking documentation, organized for efficient information gathering  
**Total Missing**: ~290 instructions (66% of 491 total)  

## 📋 Organization Strategy

Instructions are grouped by:
1. **Related functionality** - Document instruction families together
2. **Similar documentation needs** - Group by type of information missing
3. **Source requirements** - What we can figure out vs need from Chip Gracey
4. **Documentation complexity** - Simple descriptions vs complex state machines

---

## 🔧 Group 1: Flag Modification Family
**Documentation Need**: Operational semantics - what test conditions are used?  
**Can derive from**: Testing with hardware or asking Chip Gracey  
**Document together because**: Same underlying flag manipulation system

### Instructions Missing Semantics
- **MODC** D,{#}S - Modify C flag (timing: 2)
- **MODZ** D,{#}S - Modify Z flag (timing: 2)  
- **MODCZ** D,{#}S - Modify C and Z flags (timing: 2)

### What We Have
- Timing information: 2 clocks
- Basic description: "Modify flags"

### What We Need
- What are the test conditions/operands?
- How does D specify the modification?
- How does S affect the operation?
- Truth table or formula for flag changes

---

## 🔧 Group 2: Comparison Operation Variants
**Documentation Need**: Operational differences between variants  
**Can derive from**: Testing or designer clarification  
**Document together because**: All comparison-based operations

### Instructions Missing Semantics
- **CMPSUB** D,{#}S - Compare and subtract conditionally (timing: 2)
- **SUBR** D,{#}S - Reverse subtract (timing: 2)
- **CMPR** D,{#}S - Compare with reverse (timing: 2)
- **TESTBN** D,{#}S - Test bit variant (timing: 2)
- **TESTB** D,{#}S - Test bit (timing: 2)

### What We Have
- Names suggest relationship to CMP/SUB/TEST
- All have 2-clock timing

### What We Need
- CMPSUB: When does subtraction occur? What's the condition?
- SUBR: Is this D = S - D instead of D = D - S?
- CMPR: How does "reverse" differ from regular CMP?
- TESTB vs TESTBN: What's the difference?

---

## 🔧 Group 3: Smart Pin Configuration Suite
**Documentation Need**: Configuration sequences and parameter meanings  
**Can derive from**: Smart Pin documentation + examples  
**Document together because**: Must be used as a coordinated set

### Core Configuration Instructions
- **WRPIN** D,{#}S - Set pin mode and configuration
- **WXPIN** D,{#}S - Set X parameter for pin
- **WYPIN** D,{#}S - Set Y parameter for pin
- **AKPIN** {#}S - Acknowledge pin
- **RDPIN** D,{#}S - Read pin result
- **RQPIN** D,{#}S - Read pin status

### What We Have
- Basic descriptions from datasheet
- 32 Smart Pin modes enumerated
- Timing: all 2 clocks

### What We Need
- Complete mode configuration bit patterns
- X parameter meaning for each of 32 modes
- Y parameter meaning for each of 32 modes
- When/why to acknowledge with AKPIN
- Result format from RDPIN for each mode
- Status bit definitions from RQPIN
- Complete configuration sequence examples

---

## 🔧 Group 4: Event System Configuration
**Documentation Need**: Event source encoding and setup patterns  
**Can derive from**: Event system documentation  
**Document together because**: Interconnected event configuration

### Selectable Event Configuration
- **SETSE1** D,{#}S - Configure selectable event 1
- **SETSE2** D,{#}S - Configure selectable event 2
- **SETSE3** D,{#}S - Configure selectable event 3
- **SETSE4** D,{#}S - Configure selectable event 4
- **SETPAT** D,{#}S - Set pattern for matching

### What We Have
- 16 event types documented
- Basic "configure event" descriptions

### What We Need
- Event source selection encoding (D parameter format)
- How S parameter affects configuration
- Pattern format for SETPAT (mask vs match bits)
- Interaction between multiple events
- Complete setup examples

---

## 🔧 Group 5: ALT (Indirect Addressing) Family
**Documentation Need**: Complete modifier patterns for all 22 variants  
**Can derive from**: Silicon doc has some info, need complete patterns  
**Document together because**: All modify subsequent instruction execution

### ALT Instruction Variants (22 total)
- **ALTR** - Modify result
- **ALTD** - Modify destination
- **ALTS** - Modify source
- **ALTB** - Modify both
- **ALTI** - Modify instruction
- **ALTSN** - Modify source nibble
- **ALTGN** - Modify get nibble
- **ALTSB** - Modify source byte
- **ALTGB** - Modify get byte
- **ALTSW** - Modify source word
- **ALTGW** - Modify get word
- (+ 11 more variants)

### What We Have
- Basic "modifies next instruction" concept
- Some examples in silicon doc

### What We Need
- Complete modification patterns for each variant
- Index calculation formulas
- Interaction with different instruction types
- Complete examples for each variant

---

## 🔧 Group 6: Pixel Mixer Operations
**Documentation Need**: Pixel format and blending mathematics  
**Can derive from**: Graphics programming documentation  
**Document together because**: Integrated pixel processing pipeline

### Pixel Operations
- **ADDPIX** D,{#}S - Add pixels
- **MULPIX** D,{#}S - Multiply pixels
- **BLNPIX** D,{#}S - Blend pixels
- **MIXPIX** D,{#}S - Mix pixels
- **SETPIV** D,{#}S - Set pixel initial value
- **SETPIX** D,{#}S - Set pixel mode

### What We Have
- Names suggest pixel operations
- All 2-clock timing

### What We Need
- Pixel format (RGBA? 8888? 565?)
- Blending equations
- Saturation/overflow handling
- Mode configurations for SETPIX
- What is PIV (pixel initial value)?

---

## 🔧 Group 7: Color Space Converter
**Documentation Need**: Color space mathematics and configuration  
**Can derive from**: Video/color theory documentation  
**Document together because**: Complete color conversion system

### Color Space Operations
- **SETCY** D,{#}S - Set color Y parameter
- **SETCI** D,{#}S - Set color I parameter
- **SETCQ** D,{#}S - Set color Q parameter
- **SETCFRQ** D,{#}S - Set color frequency
- **SETCMOD** D,{#}S - Set color mode

### What We Have
- YIQ color space implied
- All 2-clock timing

### What We Need
- YIQ ↔ RGB conversion formulas
- Fixed-point format specifications
- Frequency parameter purpose
- Available color modes
- Complete configuration sequence

---

## 🔧 Group 8: Streamer Control
**Documentation Need**: Command formats and sequencing rules  
**Can derive from**: Streamer documentation section  
**Document together because**: Coordinated streaming control

### Streamer Operations
- **XINIT** D,{#}S - Initialize and start streamer
- **XSTOP** - Stop streamer
- **XCONT** D,{#}S - Continue streamer
- **XZERO** D,{#}S - Start at zero phase
- **SETXFRQ** D,{#}S - Set streamer frequency
- **GETXACC** D - Get streamer accumulators

### What We Have
- Basic start/stop/continue concept
- NCO-based streaming mentioned

### What We Need
- Command format in D parameter
- Mode bits encoding
- Phase relationship (XZERO vs XCONT)
- Frequency setting formula
- Accumulator format
- Complete streaming examples

---

## 🔧 Group 9: Scrambler/Security Operations
**Documentation Need**: Algorithm and key management  
**Can derive from**: Only from Chip Gracey (proprietary?)  
**Document together because**: Paired forward/reverse operations

### Scrambler Instructions
- **SEUSSF** D,{#}S - Forward scramble
- **SEUSSR** D,{#}S - Reverse scramble

### What We Have
- Names suggest Dr. Seuss-inspired scrambling
- 2-clock timing

### What We Need
- Scrambling algorithm
- Key source and format
- Block size
- Use cases/applications
- Security properties

---

## 🔧 Group 10: Advanced Math Operations
**Documentation Need**: Algorithms and overflow behavior  
**Can derive from**: Testing and mathematical analysis  
**Document together because**: Related mathematical operations

### Missing Math Operations
- **FRAC** D,{#}S - Fractional multiply
- **SCA** D,{#}S - Scale operation
- **SCAS** D,{#}S - Scale signed
- **INCMOD** D,{#}S - Increment modulo
- **DECMOD** D,{#}S - Decrement modulo

### What We Have
- Basic operation names
- 2-clock timing

### What We Need
- Exact mathematical formulas
- Fixed-point formats
- Overflow/underflow behavior
- Modulo boundaries
- Signed vs unsigned differences

---

## 📊 Documentation Completeness by Group

| Group | Instructions | Have Basic Info | Need Semantics | Need Examples |
|-------|-------------|-----------------|----------------|---------------|
| Flag Modification | 3 | ✓ | ✗ | ✗ |
| Comparison Variants | 5 | ✓ | ✗ | ✗ |
| Smart Pin Config | 6 | ✓ | ✗ | ✗ |
| Event System | 5 | ✓ | ✗ | ✗ |
| ALT Family | 22 | Partial | ✗ | ✗ |
| Pixel Mixer | 6 | Names only | ✗ | ✗ |
| Color Space | 5 | Names only | ✗ | ✗ |
| Streamer | 6 | Partial | ✗ | ✗ |
| Scrambler | 2 | Names only | ✗ | ✗ |
| Advanced Math | 5 | Names only | ✗ | ✗ |

---

## 🎯 Information Gathering Strategy

### What We Can Test/Derive
1. **Flag modifications** - Test with simple code
2. **Comparison variants** - Test behavior with examples
3. **Math operations** - Verify formulas with tests
4. **ALT patterns** - Test modification effects

### What We Need from Documentation
1. **Smart Pin parameters** - Mode-specific X/Y meanings
2. **Event encoding** - Source selection bits
3. **Pixel formats** - Exact bit layouts
4. **Color space math** - Conversion formulas
5. **Streamer modes** - Command encoding

### What Only Chip Gracey Can Answer
1. **SEUSSF/SEUSSR** - Scrambling algorithm
2. **Ambiguous operations** - CMPSUB conditions
3. **Design intent** - Why certain variants exist
4. **Edge cases** - Undefined behaviors

---

## 📋 Documentation Template for Each Group

```markdown
## [Group Name] Instructions

### Overview
- Purpose of this instruction family
- How instructions work together
- Common use cases

### Instruction Details
[For each instruction:]
- **Name**: Full syntax with operands
- **Operation**: Exact behavior/formula
- **Parameters**: 
  - D: [meaning, range, special values]
  - S: [meaning, range, special values]
- **Timing**: Clock cycles
- **Flags**: C and Z effects
- **Notes**: Special cases, restrictions

### Configuration Sequences
[Step-by-step setup examples]

### Complete Examples
[Working code showing typical usage]

### See Also
[Related instructions and alternatives]
```

---

## 📊 Impact When Documented

### Smart Pin Group Completion
- Enables 64 pins × 32 modes = 2048 configurations
- Opens ADC, DAC, PWM, serial, counter modes

### Event System Completion  
- Enables real-time event response
- Allows interrupt-free event handling

### Pixel/Color/Streamer Completion
- Enables video generation
- Opens graphics capabilities
- Allows DVI/HDMI output

### Math/Comparison Completion
- Enables optimized algorithms
- Clarifies conditional logic

---

*This organization focuses on efficient documentation gathering by grouping related instructions that share documentation needs and should be understood together.*