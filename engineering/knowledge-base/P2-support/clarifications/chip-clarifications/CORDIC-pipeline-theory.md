# CORDIC Pipeline Theory of Operations

**Source**: Chip Gracey clarification + `cordic_interleave.spin2` demonstration code
**Date**: 2025-11-26
**Status**: Authoritative - derived from P2 designer explanation

## Executive Summary

The P2's CORDIC is a **54-stage shared pipeline** accessed through the **hub rotation scheme**. Each COG gets a CORDIC access slot every 8 clocks, allowing each COG to maintain up to 7-8 operations in flight simultaneously. Understanding this model is essential for maximum CORDIC throughput.

## Hub Rotation Access Model

### The 8-Clock Slot

The CORDIC is accessed via the same hub rotation mechanism used for hub RAM:

- **8 COGs share the CORDIC** through round-robin arbitration
- **Each COG gets access every 8 system clocks**
- Clock 0: COG 0's slot → Clock 1: COG 1's slot → ... → Clock 7: COG 7's slot → Clock 8: COG 0 again

This means:
- A single COG can submit **at most one operation per 8 clocks**
- A single COG can retrieve **at most one result per 8 clocks**
- The 8-clock rhythm is fundamental to CORDIC programming

### Pipeline Depth and Latency

- **54 pipeline stages** - operations take 54 clocks to complete
- **Result availability**: ~54 clocks after submission
- **Pipeline capacity per COG**: 54 ÷ 8 ≈ **6-7 operations** can be in flight per COG

## Three Phases of CORDIC Usage

### Phase 1: Fill (Priming the Pipeline)

When starting CORDIC work, submit multiple operations before expecting any results:

```pasm2
' Submit 8 operations back-to-back (each waits for hub slot)
        SETQ    y+00
        QROTATE x+00, a+00      ' Op 0 enters pipeline

        SETQ    y+01
        QROTATE x+01, a+01      ' Op 1 enters pipeline

        ' ... continue for 6-8 operations ...

        SETQ    y+07
        QROTATE x+07, a+07      ' Op 7 enters - Op 0 result ready!
```

After ~54 clocks (7-8 submissions), the first result becomes available.

### Phase 2: Steady-State (Interleaved Operation)

Once the pipeline is primed, each 8-clock slot can both retrieve a result AND submit a new operation:

```pasm2
' Each iteration: 4 clocks to read + 4 clocks to submit = 8 clocks
        GETQY   y+00            ' 2 clocks - retrieve Y result
        GETQX   x+00            ' 2 clocks - retrieve X result

        SETQ    y+08            ' 2 clocks - setup next op
        QROTATE x+08, a+08      ' 2 clocks - submit next op

        ' Repeat pattern...
```

This achieves **maximum throughput**: one CORDIC operation completes every 8 clocks per COG.

### Phase 3: Drain (Emptying the Pipeline)

When no more operations to submit, retrieve remaining results:

```pasm2
' Final results - may have to wait for each
        GETQY   y+24            ' No wait if result ready
        GETQX   x+24

        GETQY   y+25            ' May wait ~8 clocks
        GETQX   x+25

        ' ... continue until pipeline empty ...
```

During drain, GETQX/GETQY may stall waiting for results to arrive.

## Instruction Timing Details

### Submission Instructions

| Pattern | Clocks | Notes |
|---------|--------|-------|
| SETQ + QROTATE | 4 + wait | Wait for hub slot if not aligned |
| QMUL D, S | 2 + wait | Simpler ops without SETQ |
| QDIV (with SETQ) | 4 + wait | 64÷32 division |

### Retrieval Instructions

| Instruction | Clocks | Behavior |
|-------------|--------|----------|
| GETQX | 2 (+ stall) | Stalls if result not ready |
| GETQY | 2 (+ stall) | Stalls if result not ready |
| POLLQMT | 2 | Non-blocking empty check |

### The 8-Clock Window

Within each COG's 8-clock hub slot:
- **GETQY + GETQX** = 4 clocks (retrieve one result)
- **SETQ + QOP** = 4 clocks (submit one operation)
- **Total** = 8 clocks - perfectly fills the slot

## Critical Warning: Pipeline Stalls

**Do NOT call GETQX/GETQY before results are ready!**

If you attempt to retrieve a result that hasn't completed the 54-clock journey:
- The COG **stalls** (blocks) until the result arrives
- This wastes cycles that could be doing useful work
- In extreme cases, can stall for up to 54 clocks

### Safe Patterns

**Pattern 1: Timing-based (demonstrated in cordic_interleave.spin2)**
- Calculate exactly when results will be ready
- Structure code so retrievals align with result availability

**Pattern 2: Event-based**
```pasm2
' Check if results are available before reading
        POLLQMT WC              ' C=1 if pipeline empty (bad!)
  if_c  jmp     #no_results     ' Don't read if empty
        GETQX   result
```

**Pattern 3: Known pipeline depth**
- Submit N operations
- Do other work for ~54 clocks
- Retrieve N results

## System-Wide View

With all 8 COGs using CORDIC simultaneously:

| Clock | COG 0 | COG 1 | COG 2 | ... | COG 7 |
|-------|-------|-------|-------|-----|-------|
| 0 | ACCESS | wait | wait | ... | wait |
| 1 | wait | ACCESS | wait | ... | wait |
| 2 | wait | wait | ACCESS | ... | wait |
| ... | ... | ... | ... | ... | ... |
| 7 | wait | wait | wait | ... | ACCESS |
| 8 | ACCESS | wait | wait | ... | wait |

**Total system throughput**: Up to 8 CORDIC operations per 8 clocks = **1 op/clock system-wide**

## Related Instructions Reference

### Submission
- **QMUL** - 32×32 multiply
- **QDIV** - 64÷32 divide (use with SETQ for upper 32 bits)
- **QFRAC** - Fractional multiply
- **QSQRT** - Square root
- **QROTATE** - Vector rotation (use with SETQ for angle)
- **QVECTOR** - Cartesian to polar
- **QLOG** - Natural logarithm
- **QEXP** - Exponential

### Retrieval
- **GETQX** - Get X result (stalls if not ready)
- **GETQY** - Get Y result (stalls if not ready)

### Status
- **POLLQMT** - Poll "Q empty" flag into C/Z, then clear
- **JQMT** - Jump if Q empty flag set
- **JNQMT** - Jump if Q empty flag clear

## Demonstration Code Reference

The file `cordic_interleave.spin2` demonstrates all three phases:
- Lines 26-48: Fill phase (8 operations)
- Lines 50-192: Steady-state interleaved phase (24 operations)
- Lines 194-216: Drain phase (8 results)

This code generates 32 simultaneous sine waves on P0-P31 using DACs, achieving maximum CORDIC throughput through careful pipeline management.

## Key Takeaways

1. **CORDIC access is hub-rotated** - 8-clock slots per COG
2. **54-stage pipeline** - plan for latency
3. **Fill before drain** - prime the pipeline with 7-8 ops
4. **Interleave for throughput** - read + submit in same slot
5. **Avoid stalls** - don't GETQX/GETQY before results ready
6. **Use POLLQMT** - for dynamic/unknown pipeline states
