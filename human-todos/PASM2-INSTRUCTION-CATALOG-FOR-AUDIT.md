# PASM2 Instruction Catalog for Audit
*Instructions we extracted in alphabetical order for verification and enrichment*

## HOW THIS AUDIT WORKS
1. I list instructions we think we have with current metadata
2. You verify presence and completeness
3. You add missing metadata (especially clock timing!)
4. We build complete instruction consulting knowledge base

---

## INSTRUCTION CATALOG
*Format: [Instruction] - What We Have - What We're Missing*

### A Instructions

#### ABS - Absolute Value
**What We Have**:
- Syntax: `ABS D,{#}S {WC/WZ/WCZ}`
- Encoding: EEEE 1010110 CZI DDDDDDDDD SSSSSSSSS
- Description: Get absolute value
- Flags: C = source was negative, Z = result is zero

**What We're MISSING**:
- [ ] Clock cycles: _______
- [ ] Complete narrative
- [ ] Usage patterns
- [ ] When to use vs alternatives

**Your Additional Metadata**: _______________

#### ADD - Add
**What We Have**:
- Syntax: `ADD D,{#}S {WC/WZ/WCZ}`
- Encoding: EEEE 1000000 CZI DDDDDDDDD SSSSSSSSS
- Description: Add S to D
- Flags: C = carry out, Z = result is zero

**What We're MISSING**:
- [ ] Clock cycles: _______
- [ ] Extended narrative
- [ ] Common patterns

**Your Additional Metadata**: _______________

#### ADDCT1 - Add to CT1
**What We Have**:
- Syntax: `ADDCT1 D,{#}S`
- Encoding: EEEE 1001000 101 DDDDDDDDD SSSSSSSSS
- Description: Add S to CT1 timer

**What We're MISSING**:
- [ ] Clock cycles: _______
- [ ] When to use for timing
- [ ] Relationship to WAITCT1

**Your Additional Metadata**: _______________

[GAP CHECK: Any A instructions between ADDCT1 and ADDPIX?] _______________

#### ADDPIX - Add Pixels
**What We Have**:
- Syntax: `ADDPIX D,{#}S`
- Encoding: [Missing encoding]
- Description: Add pixels with saturation

**What We're MISSING**:
- [ ] Complete encoding
- [ ] Clock cycles: _______
- [ ] Pixel format details
- [ ] Saturation behavior

**Your Additional Metadata**: _______________

### B Instructions

#### BITL - Bit Low
**What We Have**:
- Syntax: `BITL D,{#}S {WCZ}`
- Encoding: EEEE 1000001 CZI DDDDDDDDD SSSSSSSSS
- Description: Set bit S[4:0] in D to 0

**What We're MISSING**:
- [ ] Clock cycles: _______
- [ ] Why use vs ANDN
- [ ] Performance implications

**Your Additional Metadata**: _______________

[Continue alphabetically...]

### W-Z Instructions (Likely Missing!)

#### WAITCT1 - Wait for CT1
**What We Have**: ❓ Possibly nothing
**What We Need**:
- [ ] Complete syntax
- [ ] Encoding
- [ ] Clock cycles: _______
- [ ] Power implications
- [ ] Use cases

**Your Additional Metadata**: _______________

#### WRLONG - Write Long to Hub
**What We Have**:
- Syntax: `WRLONG {#}D,{#}S/P`
- Description: Write long to hub

**What We're MISSING**:
- [ ] Complete encoding
- [ ] Clock cycles: _______ (hub-dependent?)
- [ ] Hub timing windows
- [ ] FIFO interaction

**Your Additional Metadata**: _______________

---

## CRITICAL MISSING DATA TO CAPTURE

### Clock Timing Patterns
Please note ALL timing patterns you see:
- Simple: "2 clocks"
- Range: "2..9 clocks"  
- Conditional: "2 + hub window"
- Special: "CORDIC-dependent"
- Complex: _______

### Instruction Relationships
Please note setup/dependency patterns:
- SETQ before RDLONG: _______
- WRPIN before pin ops: _______
- SETSE before WAITSE: _______
- Others: _______

### Performance Hints
Please note any performance guidance:
- "Use X instead of Y for speed"
- "Avoid in tight loops"
- "Hub window sensitive"
- Others: _______

---

## METADATA ENRICHMENT TEMPLATE

For each instruction, please provide:

```
Instruction: _______
Page in Manual: _______
Clock Cycles: _______
Power State: Active/Wait/Sleep
Common Usage: _______
Pairs With: _______ (related instructions)
Avoid When: _______
Prefer When: _______
Real Example: _______
Gotchas: _______
```

---

## SPECIAL FOCUS AREAS

### Hub Timing Instructions
These MUST have timing info:
- [ ] RDLONG - hub window dependency
- [ ] WRLONG - hub window dependency  
- [ ] RDWORD/WRWORD - timing
- [ ] RDBYTE/WRBYTE - timing
- [ ] WMLONG - special timing

### Event Instructions
Critical for real-time:
- [ ] WAITCTx - exact wait behavior
- [ ] WAITATx - attention timing
- [ ] WAITPAT - pattern matching time
- [ ] All POLL variants - polling overhead

### CORDIC Instructions
Complex timing:
- [ ] QMUL - multiplication time
- [ ] QDIV - division time
- [ ] QROTATE - rotation time
- [ ] QSQRT - square root time

---

## AUDIT QUESTIONS

1. **Total instructions in manual**: _______
2. **Instructions with timing data**: _______
3. **Instructions with full narratives**: _______
4. **Instructions in tables only**: _______
5. **Instructions missing completely**: _______

---

## OUTCOME

After this audit, we'll have:
- Complete instruction timing database
- Full narrative coverage map
- Performance optimization guidance
- Instruction relationship matrix
- Trust level elevation (red→green)

---

*This catalog format enables systematic verification and enrichment of instruction knowledge*