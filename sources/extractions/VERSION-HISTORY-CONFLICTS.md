# Version History Conflicts & Superseded Information

## Critical Discovery: Version History Takes Precedence
*When revision notes contradict main text, the revision history is authoritative*

## Document Analysis for Version Conflicts

### 1. Silicon Documentation v35

#### Major Version Conflicts Found:

**XORO32 Instruction**
- Main Text: Original implementation described
- Version History (2019_04_11): "XORO32 improved"
- **PRECEDENCE**: New XORO32 implementation in Rev B/C

**PRNG Algorithm** 
- Main Text: References older PRNG
- Version History: "Main PRNG upgraded to Xoroshiro128**"
- **PRECEDENCE**: Xoroshiro128** is current

**System Counter**
- Main Text: 32-bit counter implied
- Version History: "System counter extended to 64 bits. GETCT WC retrieves upper 32-bits"
- **PRECEDENCE**: 64-bit counter in Rev B/C

**Smart Pin Modes**
- Main Text: Original modes listed
- Version History: "SINC2/SINC3 filters added", "SCOPE modes added"
- **PRECEDENCE**: Additional modes in Rev B/C

**Power Consumption**
- Early Text: Higher power estimates
- Version History (2019_08_01): "Power is reduced by ~50%"
- **PRECEDENCE**: Rev B/C has 50% lower power

**Clock Speed**
- Conservative estimates in main text
- Version History (2019_08_01): "silicon runs at 390MHz"
- **PRECEDENCE**: 390MHz verified on Rev B/C

**PLL Performance**
- Main Text: Older PLL characteristics
- Version History: "PLL jitter is <2ns @100us"
- **PRECEDENCE**: Improved PLL in Rev B/C

### 2. Hardware Manual 2022

#### Boot Process Updates:
- Main Text: Basic boot description
- Appendix/Revisions: Detailed boot patterns for Rev B/C
- **PRECEDENCE**: Rev B/C boot patterns authoritative

### 3. PASM2 Manual

#### Instruction Changes:
- **PTRx Expressions**: 
  - Original: Limited range
  - Updated: "-16..+16 with updating and -32..+31 without"
  - **PRECEDENCE**: Extended ranges in Rev B/C

- **BIT Instructions**:
  - Original: Single bit operations
  - Updated: "can now work on a span of bits (+S[9:5] bits)"
  - **PRECEDENCE**: Multi-bit operations in Rev B/C

- **DIRx/OUTx/FLTx/DRVx**:
  - Original: Single pin
  - Updated: "can now work on a span of pins (+D[10:6] pins)"
  - **PRECEDENCE**: Multi-pin operations in Rev B/C

### 4. Smart Pins Documentation

#### Mode Additions:
- Original: 29 modes documented
- Rev B/C additions:
  - SINC2 filtering modes
  - SINC3 filtering modes  
  - SCOPE modes (4 channels)
  - USB mode improvements
- **PRECEDENCE**: 32 total modes in Rev B/C

### 5. Spin2 Documentation v51

#### Bytecode Changes:
- Earlier versions: Different bytecode
- v51: Current bytecode format
- **PRECEDENCE**: v51 bytecode is authoritative

## Critical Technical Updates (Rev A → Rev B/C)

### Silicon Bugs Fixed:
1. ✅ Sign-extension problems in IQ modulators
2. ✅ Smart pin measurement +1/+3 error
3. ✅ ALTx sign-extension of S[17:09]
4. ✅ DIR/OUT race condition on I/O pins
5. ✅ LUT sharing glitches

### Performance Improvements:
1. ✅ Clock gating: ~40% power reduction
2. ✅ PLL filter: Reduced jitter, better lock
3. ✅ Maximum frequency: 390MHz verified
4. ✅ Temperature: "barely warm to the touch"

### Feature Additions:
1. ✅ 64-bit system counter
2. ✅ HDMI streaming mode
3. ✅ SINC2/SINC3 ADC filters
4. ✅ SCOPE modes (8-bit/clock ADC)
5. ✅ Multi-bit/pin operations
6. ✅ Improved XORO32
7. ✅ Xoroshiro128** PRNG

## Documentation Priority Order

When conflicts arise, use this precedence:

1. **Silicon Rev B/C Notes** (2019 updates)
2. **Version History Sections** 
3. **Revision Tables/Appendices**
4. **Latest Document Versions** (v35, v51, 2022)
5. **Main Body Text**
6. **Original/Draft Content**

## Action Items for Knowledge Base

### Must Update/Clarify:
- [ ] PRNG is Xoroshiro128** not older algorithm
- [ ] System counter is 64-bit not 32-bit
- [ ] Power consumption is 50% lower than Rev A
- [ ] Maximum frequency is 390MHz proven
- [ ] PTRx expressions have extended ranges
- [ ] BIT operations work on spans
- [ ] PIN operations work on spans
- [ ] 32 Smart Pin modes not 29

### Must Note as Rev B/C Only:
- SINC2/SINC3 filters
- SCOPE modes
- HDMI streaming
- Clock gating
- Extended counters
- Span operations

## Extraction Rule Going Forward

**ALWAYS CHECK VERSION HISTORY FIRST**

When extracting any P2 document:
1. Read revision history completely
2. Note all updates/changes
3. Flag contradictions with main text
4. Use latest revision as authoritative
5. Mark Rev A vs Rev B/C differences

## Silicon Version Summary

### Rev A (2018)
- First silicon
- Had bugs
- Limited availability
- **DO NOT USE FOR REFERENCE**

### Rev B/C (2019+)
- Production silicon
- All bugs fixed
- Enhanced features
- **THIS IS THE REFERENCE**

## Conclusion

Many "unknowns" in our extraction are actually KNOWN in version history:
- Power: 50% reduction achieved
- Speed: 390MHz verified
- Jitter: <2ns measured
- Features: Significantly expanded

**Version history contains critical facts not in main text!**