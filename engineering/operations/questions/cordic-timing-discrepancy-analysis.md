# CORDIC Timing Discrepancy Analysis

**For Review by**: Chip Gracey  
**Date**: September 11, 2025  
**Author**: P2 Knowledge Base Team  
**Purpose**: Request clarification on CORDIC instruction timing documentation discrepancy

---

## Executive Summary

We have discovered a significant timing discrepancy in CORDIC operation documentation that violates expected performance principles. PASM2 instructions show 55-clock timing while Spin2 methods show 38-clock timing for the same CORDIC operations. Since interpreted code should never outperform direct hardware access, we need clarification on what these timing measurements actually represent.

---

## The Discrepancy

### PASM2 CORDIC Instructions: 55 Clocks
**Source**: P2 Datasheet - `/engineering/ingestion/sources/p2-datasheet/p2-datasheet-narrative.txt`

**Quote**: 
> "Each cog can issue one CORDIC instruction per its hub access window (which occurs once every eight clocks) and retrieve the result **55 clocks later** via the GETQX and GETQY instructions."

**Instructions Affected**:
- QMUL, QDIV, QFRAC, QSQRT, QROTATE, QVECTOR, QLOG, QEXP
- All documented as taking 55 clocks from issue to result availability

### Spin2 CORDIC Methods: 38 Clocks  
**Sources**: Knowledge Base YAML files in `/engineering/knowledge-base/P2/language/spin2/methods/`

**Specific Examples**:

**File**: `qcos.yaml`
```yaml
timing:
  description: "CORDIC operation"
  cycles: "38 clock cycles"
```

**File**: `qsin.yaml`  
```yaml
timing:
  description: "CORDIC operation"
  cycles: "38 clock cycles"
```

**File**: `qlog.yaml`
```yaml
timing:
  description: "CORDIC operation" 
  cycles: "38 clock cycles"
```

**File**: `qexp.yaml`
```yaml
timing:
  description: "CORDIC operation"
  cycles: "38 clock cycles"
```

**Additional Methods with 38-Clock Timing**:
- POLXY (polar to cartesian)
- XYPOL (cartesian to polar) 
- ROTXY (rotation)

---

## Why This Is Problematic

### Fundamental Computer Science Principle Violation
**Expected Performance Hierarchy**:
1. **Direct Hardware** (PASM2): Fastest baseline
2. **Interpreted Code** (Spin2): Slower due to interpreter overhead

**What We're Seeing**:
1. **PASM2**: 55 clocks 
2. **Spin2**: 38 clocks ← **This should be impossible**

### Technical Logic
- Spin2 methods must ultimately use the same CORDIC hardware
- Interpreter overhead should add time, not reduce it
- A 17-clock improvement (55-38=17) through interpretation defies explanation

---

## Our Current Hypotheses

### Hypothesis 1: Different Measurement Points ⭐ (Most Likely)
**Theory**: The timings measure different phases of execution

**PASM2 (55 clocks)**:
- Time from instruction issue to hardware result ready
- Includes full CORDIC pipeline completion
- Measures when GETQX/GETQY can retrieve valid data

**Spin2 (38 clocks)**:
- Time for method call to complete and return
- May return before CORDIC hardware finishes
- Does not include waiting for actual mathematical result

### Hypothesis 2: Asynchronous Method Design
**Possible Spin2 Pattern**:
```spin2
PUB QLOG(value) : result
  ' Issue CORDIC operation (2 clocks)
  ' Do method housekeeping (35 clocks)
  ' Return placeholder/cached result (1 clock)
  ' Total: 38 clocks
  ' Note: Actual CORDIC result ready at 55 clocks
```

### Hypothesis 3: Documentation Error
- One timing figure may be incorrect
- 38-clock timing might measure something unrelated to CORDIC execution

### Hypothesis 4: Advanced Optimization (Unlikely)
- Spin2 compiler performs optimizations we don't understand
- Pre-computation or caching mechanisms
- Seems implausible for mathematical operations requiring specific inputs

---

## Architecture Context

### CORDIC Hardware Specifications
**Pipeline**: 54-stage pipelined CORDIC solver  
**Throughput**: One operation per clock (after pipeline fill)  
**Latency**: 54 stages + overhead = 55 clocks total

**This aligns with PASM2 timing but not Spin2 timing.**

---

## Questions for Chip Gracey

### Primary Questions
1. **What exactly do these timing measurements represent?**
   - Does PASM2's "55 clocks" measure instruction-to-result-ready?
   - Does Spin2's "38 clocks" measure method-call-to-return?

2. **Are Spin2 CORDIC methods asynchronous?**
   - Do they return before the CORDIC result is actually ready?
   - How does the user know when the mathematical result is valid?

3. **Is there a documentation error?**
   - Should one of these timing figures be different?
   - Are we comparing equivalent operations?

### Secondary Questions
4. **How do Spin2 CORDIC methods work internally?**
   - Do they use the same PASM2 instructions?
   - Is there any optimization or special handling?

5. **What should AI code generation use?**
   - For timing-critical code, which figure is accurate?
   - Should we document both with clear distinctions?

### Additional CORDIC Questions

6. **Spin2 Method Implementation Details**
   - How are Spin2 CORDIC methods actually implemented?
   - Do they use the same PASM2 instructions internally?
   - What is the actual timing from method call to mathematical result availability?
   - Are there any caching or optimization mechanisms?

7. **CORDIC Pipeline Utilization**
   - Can multiple cogs issue CORDIC instructions simultaneously?
   - How does the 8-clock hub window interact with the 54-stage pipeline?
   - What happens if a cog tries to issue a second CORDIC instruction before retrieving the first result?

8. **Result Management and Timing Safety**
   - Is it safe to issue back-to-back CORDIC instructions in the same cog?
   - How should code handle the timing between instruction issue and result retrieval?
   - What happens if GETQX/GETQY are called before the 55-clock period?

9. **Multi-Cog Coordination**
   - Can different cogs use CORDIC simultaneously without interference?
   - Are there any shared resources or potential conflicts?
   - How should multi-cog real-time applications coordinate CORDIC usage?

10. **Advanced Usage Patterns**
    - Can CORDIC operations be chained or pipelined efficiently?
    - Are there optimal patterns for mathematical sequences?
    - How do interrupts interact with pending CORDIC operations?

### Boundary Cases and Edge Cases

11. **Input Value Limits and Overflow**
    - What are the precise input range limits for each CORDIC instruction?
    - What happens with overflow conditions (e.g., very large inputs to QMUL)?
    - How does the hardware handle edge cases like division by zero in QDIV?
    - Are there specific input values that cause unexpected behavior?

12. **Precision and Accuracy Boundaries**
    - What is the actual precision loss for very small or very large values?
    - At what input magnitudes does accuracy degrade significantly?
    - How do successive CORDIC operations accumulate error?
    - Are there input patterns that maximize or minimize precision loss?

13. **Timing Edge Cases**
    - What happens if a cog is reset while CORDIC operation is in progress?
    - How do CORDIC operations interact with waitx, hubset, or other timing-critical instructions?
    - Can clock frequency changes affect in-progress CORDIC operations?
    - What happens with CORDIC instructions issued just before/after cog synchronization events?

14. **Pipeline Conflict Scenarios**
    - What happens if multiple CORDIC instructions are issued within the 55-clock window?
    - How does the hardware handle rapid-fire CORDIC instruction sequences?
    - Are there instruction combinations that cause pipeline stalls or conflicts?
    - What is the behavior when mixing different CORDIC instruction types rapidly?

15. **Result Retrieval Edge Cases**
    - What happens if GETQX is called but GETQY is not (or vice versa)?
    - Can results be retrieved out of order or multiple times?
    - What values do GETQX/GETQY return if called when no CORDIC operation is pending?
    - How long do CORDIC results remain valid in the result registers?

16. **Mathematical Edge Cases**
    - How does QVECTOR handle (0,0) input?
    - What does QLOG return for zero or negative inputs?
    - How does QEXP handle very large exponents that would overflow?
    - What angle values does QROTATE handle at the boundaries (±π, ±2π)?
    - How does QSQRT handle negative inputs?

17. **Format and Conversion Boundaries**
    - What happens at the boundaries of the 5.27 fixed-point format?
    - How does the hardware handle the transition between different numeric ranges?
    - Are there conversion artifacts at format boundaries that affect results?
    - What happens with inputs that don't align well with the internal format?

18. **System Integration Edge Cases**
    - How do CORDIC operations interact with smart pin operations?
    - Can CORDIC and streamer operations conflict?
    - What happens to CORDIC state during cog restart or mode changes?
    - How do debug/trace operations interact with pending CORDIC results?

---

## Impact on Knowledge Base

This discrepancy affects:
- **Code Generation**: AI needs accurate timing for real-time applications
- **Documentation Quality**: We can't explain impossible performance characteristics  
- **User Education**: Developers need to understand actual performance implications

---

## Requested Action

**We request Chip's analysis of:**
1. The technical explanation for this timing difference
2. Clarification of what each measurement actually represents  
3. Guidance on which timing figures AI code generation should use
4. Any corrections needed to our documentation

**This analysis will help us provide accurate, explainable documentation for P2 developers and AI systems.**

---

## Appendix: Source File References

### PASM2 Timing Sources
- `/engineering/ingestion/sources/p2-datasheet/p2-datasheet-narrative.txt`
- `/engineering/ingestion/sources/p2-datasheet/pasm2-complete-instruction-tables.md`

### Spin2 Timing Sources  
- `/engineering/knowledge-base/P2/language/spin2/methods/qcos.yaml`
- `/engineering/knowledge-base/P2/language/spin2/methods/qsin.yaml`
- `/engineering/knowledge-base/P2/language/spin2/methods/qlog.yaml`
- `/engineering/knowledge-base/P2/language/spin2/methods/qexp.yaml`
- `/engineering/knowledge-base/P2/language/spin2/methods/polxy.yaml`
- `/engineering/knowledge-base/P2/language/spin2/methods/xypol.yaml`
- `/engineering/knowledge-base/P2/language/spin2/methods/rotxy.yaml`

### Architecture Sources
- `/engineering/knowledge-base/P2/architecture/cordic.yaml`
- `/engineering/ingestion/sources/p2-datasheet/p2-datasheet-critical-insights.md`