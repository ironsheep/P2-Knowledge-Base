# PASM2 Grouped Instruction Documentation Analysis

## Summary
Found **48 grouped instruction patterns** covering **116 instructions** that share documentation in the PASM2 manual.

## Categories of Grouped Instructions

### 1. Slash-Separated Binary Groups (31 groups, 62 instructions)
Instructions with positive and negative variants that share documentation:

#### Bit Operations
- **AND / ANDN** - Logical AND with normal and inverted source
- **BITC / BITNC** - Copy bit to C flag with normal and inverted
- **BITH / BITL** - Set bit high or low
- **BITZ / BITNZ** - Copy bit to Z flag with normal and inverted

#### Subroutine Calls
- **CALLA / CALLB** - Call using PTRA/PTRB for context storage
- **CALLPA / CALLPB** - Call with parameter passing via PTRA/PTRB

#### Pin Control
- **DIRC / DIRNC** - Set pin direction based on C flag
- **DIRH / DIRL** - Set pin direction high or low
- **DIRZ / DIRNZ** - Set pin direction based on Z flag
- **DRVC / DRVNC** - Drive pin based on C flag
- **DRVZ / DRVNZ** - Drive pin based on Z flag
- **OUTC / OUTNC** - Output to pin based on C flag
- **OUTH / OUTL** - Output high or low to pin
- **OUTZ / OUTNZ** - Output to pin based on Z flag

#### Floating Point Control
- **FLTC / FLTNC** - Float pin based on C flag
- **FLTH / FLTL** - Float pin high or low
- **FLTZ / FLTNZ** - Float pin based on Z flag

#### Conditional Jumps
- **DJF / DJNF** - Decrement and jump if full/not full
- **DJZ / DJNZ** - Decrement and jump if zero/not zero
- **IJZ / IJNZ** - Increment and jump if zero/not zero
- **JATN / JNATN** - Jump if ATN event flag set/clear
- **JFBW / JNFBW** - Jump if FIFO block wrap set/clear
- **JINT / JNINT** - Jump if interrupt flag set/clear
- **JPAT / JNPAT** - Jump if pin pattern matches/doesn't match
- **JQMT / JNQMT** - Jump if CORDIC queue empty/not empty
- **JXFI / JNXFI** - Jump if XCH FIFO ready/not ready
- **JXMT / JNXMT** - Jump if transmit buffer empty/not empty
- **JXRL / JNXRL** - Jump if receive line low/high
- **JXRO / JNXRO** - Jump if receive overrun/no overrun

#### Flag Operations
- **MUXC / MUXNC** - Mux bit based on C flag
- **MUXZ / MUXNZ** - Mux bit based on Z flag

### 2. Numbered Variant Groups (17 groups, 54+ instructions)

#### Event Handling (3-variant groups)
- **ADDCT1/2/3** - Add counter event trigger times
- **JCT1/2/3** - Jump if counter event flag set
- **JNCT1/2/3** - Jump if counter event flag clear
- **POLLCT1/2/3** - Poll and clear counter event flags
- **WAITCT1/2/3** - Wait for counter event

#### Selectable Events (4-variant groups)
- **JSE1/2/3/4** - Jump if selectable event flag set
- **JNSE1/2/3/4** - Jump if selectable event flag clear
- **POLLSE1/2/3/4** - Poll and clear selectable event flags
- **SETSE1/2/3/4** - Set selectable event configuration
- **WAITSE1/2/3/4** - Wait for selectable event

#### Interrupt Handling (3-variant groups)
- **SETINT1/2/3** - Set interrupt source configuration
- **TRGINT1/2/3** - Trigger interrupt
- **NIXINT1/2/3** - Cancel interrupt
- **RETI1/2/3** - Return from interrupt
- **RESI1/2/3** - Resume from interrupt
- **IJMP1/2/3** - Indirect jump via interrupt vector
- **IRET1/2/3** - Interrupt return

### 3. Additional Multi-Instruction Groups Found

#### Test and Jump Groups
- **TJF / TJNF** - Test and jump if full/not full (lines 7330+)
- **TJS / TJNS** - Test and jump if signed/not signed (lines 7365+)
- **TJZ / TJNZ** - Test and jump if zero/not zero (lines 7428+)
- **TJV** - Test and jump if overflow (standalone but related)

#### Flag Modification Groups
- **MODC / MODZ / MODCZ** - Modify C, Z, or both flags (lines 5200+)

#### Sum Operations
- **SUMC / SUMNC** - Sum based on C flag state (lines 7124+)
- **SUMZ / SUMNZ** - Sum based on Z flag state (lines 7155+)

## Instructions That Were Missed Initially

The following instruction groups share documentation but were not immediately obvious:

1. **MODC / MODZ / MODCZ** - Three instructions documented together for flag modification
2. **TJF / TJNF** - Test jump full/not full pair
3. **TJS / TJNS** - Test jump signed/not signed pair
4. **SUMC / SUMNC** - Sum with C/not C pair
5. **SUMZ / SUMNZ** - Sum with Z/not Z pair

## Implications for Documentation System

### Total Impact
- **116+ instructions** benefit from grouped documentation
- This represents approximately **25-30%** of all PASM2 instructions
- Significant duplication can be avoided with proper group references

### Recommended Two-Tier Structure
1. **Individual YAML files** - Minimal with group reference
2. **Group documentation files** - Rich shared narrative

### Example Structure
```yaml
# Individual: JCT1.yaml
mnemonic: JCT1
name: Jump if Counter 1 Event
group_ref: counter_event_jumps
counter_number: 1
brief: Jump if counter 1 event flag is set

# Group: groups/counter_event_jumps.yaml
group_name: Counter Event Jump Instructions
members: [JCT1, JCT2, JCT3, JNCT1, JNCT2, JNCT3]
shared_description: |
  These instructions test counter event flags and conditionally jump...
  [Full rich documentation here]
```

## Next Steps
1. ✅ Found all grouped instruction patterns
2. 🔄 Document all grouped instructions comprehensively (in progress)
3. ⏳ Update extraction scripts for all grouped patterns
4. ⏳ Fix heat map scoring algorithm to recognize group references
5. ⏳ Regenerate accurate heat maps